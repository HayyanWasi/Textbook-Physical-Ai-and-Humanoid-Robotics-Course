# Research: RAG Pipeline — Phase 0 Findings

**Feature**: `005-rag-pipeline` | **Date**: 2026-06-14  
**Purpose**: Resolve all NEEDS CLARIFICATION items and establish key technical decisions before Phase 1 design.

---

## 1. Cohere API — Embedding

**Decision**: Use `embed-v4.0` with `input_type="search_document"` for ingestion and `"search_query"` for queries.

**Rationale**: `embed-v4.0` is the latest available model on the free Developer Tier. It produces 1536-dimension vectors by default (configurable to 256/512/1024/1536). The `input_type` parameter instructs the model to optimize representations for the correct use case, improving retrieval quality with no extra cost.

**Rate limits**: Free tier allows 5 embed calls per minute, maximum 96 texts per synchronous call.

**Batch strategy**: Use batch size of 90 texts per call (safely under 96 limit) with a 13-second inter-batch sleep (safely under 5 calls per 60 seconds). At ~48 initial chunks, ingestion completes in 1–2 batches (~13–26 seconds total).

**SDK call pattern**:
```python
import cohere
co = cohere.ClientV2(api_key=os.getenv("COHERE_API_KEY"))
response = co.embed(
    model="embed-v4.0",
    input_type="search_document",   # or "search_query" for queries
    texts=batch_of_texts,
    embedding_types=["float"],
)
vectors = response.embeddings.float_
```

**Alternatives considered**:
- `embed-english-v3.0` — older, 1024 dims — rejected in favour of newer v4.0
- OpenAI `text-embedding-3-small` — requires paid tier; spec calls for Cohere

---

## 2. Generation Model (SUPERSEDED — see §8)

> **Superseded 2026-06-14**: The decision below (Cohere `command-r-plus-08-2024`) was the original choice. Per the 2026-06-14 clarification session, generation now uses the OpenAI Agents SDK with Gemini (`gemini-2.5-flash`) — see §8. This section is retained for historical context only.

**Original decision**: Use `command-r-plus-08-2024` with the `documents` parameter (native RAG mode).

**Rationale**: This is the most capable model available on the free Developer Tier (20 chat calls/min). Cohere's `chat()` endpoint accepts a `documents` list that it uses as grounding context — this is native RAG support, no prompt assembly required. The model automatically cites source documents when `documents` is supplied.

**SDK call pattern**:
```python
response = co.chat(
    model="command-r-plus-08-2024",
    messages=[{"role": "user", "content": question}],
    documents=[
        {"id": chunk.id, "data": {"title": chunk.heading, "text": chunk.text}}
        for chunk in top_chunks
    ],
)
answer = response.message.content[0].text
```

**Alternatives considered**:
- `command-r-08-2024` — lighter model, lower quality for grounded answers
- Gemini API — key is present in `.env` but spec specifies Cohere integration
- Building prompt manually — Cohere's native `documents` parameter is simpler and produces better citations

---

## 3. Qdrant — Deployment Mode

**Decision**: Use the already-provisioned Qdrant Cloud instance.

**URL**: `https://d7f4496d-b1fa-4726-95b2-c9871859b806.us-east-1-1.aws.cloud.qdrant.io:6333`

**Rationale**: The `backend/.env` file already contains a valid Qdrant Cloud API key and URL. Using the cloud instance means zero local setup (no Docker, no local process) and data persists across backend restarts. The spec assumption of local-only was incorrect — cloud is already the target.

**Connection pattern**:
```python
from qdrant_client import QdrantClient
client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)
```

**Alternatives considered**:
- `QdrantClient(":memory:")` — data lost on restart; rejected since cloud is provisioned
- `QdrantClient(path="./qdrant_storage")` — disk-based local; rejected in favour of cloud

---

## 4. Qdrant — Collection Design

**Decision**: Single collection named `textbook-chunks`, Cosine distance, 1536-dim vectors.

**Rationale**: All textbook content is homogeneous (same embedding model, same domain). A single collection simplifies ingestion and allows cross-module retrieval for capstone queries. Module scoping (optional `context` filter) is applied at query time via payload filter, not via separate collections.

**Idempotency**: Point IDs are deterministic UUIDs derived from `uuid5(NAMESPACE_URL, f"{file_path}#{heading}")`. Re-running ingest replaces existing points for the same heading rather than duplicating them.

**Create pattern**:
```python
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid

NAMESPACE = uuid.NAMESPACE_URL

if not client.collection_exists("textbook-chunks"):
    client.create_collection(
        "textbook-chunks",
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
    )

def chunk_id(file_path: str, heading: str) -> str:
    return str(uuid.uuid5(NAMESPACE, f"{file_path}#{heading}"))
```

---

## 5. MDX Parsing Strategy

**Decision**: Python `re` module — strip YAML frontmatter and JSX tags, then split on `## ` boundaries.

**Rationale**: MDX files use a consistent format (YAML frontmatter, `import` statements, H2 sections, JSX components at the end). Simple regex is sufficient, zero external dependencies.

**Algorithm**:
```python
import re, pathlib

FRONTMATTER = re.compile(r"^---[\s\S]*?---\n", re.MULTILINE)
JSX_TAGS    = re.compile(r"<[A-Z][^>]*/>|<[A-Z][^>]*>[\s\S]*?</[A-Z][^>]*>")
IMPORTS     = re.compile(r"^import .+$", re.MULTILINE)
HEADING_RE  = re.compile(r"^## (.+)$", re.MULTILINE)

def parse_mdx(path: pathlib.Path) -> list[dict]:
    raw = path.read_text(encoding="utf-8")
    text = FRONTMATTER.sub("", raw)
    text = IMPORTS.sub("", text)
    text = JSX_TAGS.sub("", text)
    
    # split on ## headings
    sections = HEADING_RE.split(text)
    # sections = [pre_heading_text, heading1, body1, heading2, body2, ...]
    chunks = []
    for i in range(1, len(sections), 2):
        heading = sections[i].strip()
        body = sections[i + 1].strip() if i + 1 < len(sections) else ""
        if body:
            chunks.append({"heading": heading, "text": f"## {heading}\n\n{body}"})
    return chunks
```

**Alternatives considered**:
- `mdx-py` / `mistletoe` — adds dependencies with no meaningful benefit for this use case
- LangChain `TextSplitter` — too heavyweight; spec doesn't require LangChain

---

## 6. Security Gap Identified

**Finding**: `backend/.env` contains live API keys. The root `.gitignore` has `.env` which only matches a file named `.env` at the repository root, not `backend/.env`.

**Decision**: Add `backend/.env` (and `**/.env` pattern for future-proofing) to `.gitignore` in the first implementation task.

**Note**: Keys may already be committed to history. Rotation is recommended but outside the scope of this feature.

---

## 7. RagChatbot.jsx Update Scope

**Finding**: `frontend/src/components/RagChatbot.jsx` is currently a stub (6 lines, renders a placeholder div). It accepts `context` and `placeholder` props.

**Decision**: Minimal update — add `useState` + `fetch()` inside the existing function. Keep the same props interface. No new files, no new components.

**New behaviour**:
- Text input + submit button
- Loading spinner while fetch is in-flight
- Renders `answer` text on success
- Renders error message on failure
- Sends `{ "question": inputValue, "context": context }` to `http://localhost:8000/api/chat`

---

## 8. OpenAI Agents SDK — Gemini Integration (2026-06-14 update)

**Decision**: Use the OpenAI Agents SDK (`openai-agents` package) with a custom `AsyncOpenAI` client pointed at Gemini's OpenAI-compatible endpoint, set as the SDK's default client. Define one `function_tool` (`search_textbook`) wrapping the existing Qdrant `query_points` retrieval, and one `Agent` that calls it.

**Rationale**: This is the documented pattern (`agents.set_default_openai_client`) for running the Agents SDK against any OpenAI-compatible provider. It requires no changes to embeddings, Qdrant, or the response schema — only the generation step inside `/api/chat` changes.

**Client setup** (`backend/agent.py`):
```python
from openai import AsyncOpenAI
from agents import (
    Agent, Runner, function_tool,
    set_default_openai_client, set_default_openai_api, set_tracing_disabled,
)

gemini_client = AsyncOpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GEMINI_API_KEY"),
)
set_default_openai_client(client=gemini_client, use_for_tracing=False)
set_default_openai_api("chat_completions")
set_tracing_disabled(disabled=True)  # no OpenAI tracing key available
```

**Tool definition** — wraps the existing Qdrant query, preserving the `module_num` filter (FR-008):
```python
@function_tool
def search_textbook(query: str, module_num: int | None = None) -> str:
    """Search the textbook for passages relevant to `query`,
    optionally scoped to a single module."""
    vector = embed_query(query)  # existing Cohere embed-v4.0 call
    query_filter = (
        Filter(must=[FieldCondition(key="module_num", match=MatchValue(value=module_num))])
        if module_num is not None else None
    )
    hits = qdrant.query_points(
        collection_name=COLLECTION, query=vector, limit=TOP_K, query_filter=query_filter,
    ).points
    return json.dumps([
        {"heading": h.payload["heading"], "file_path": h.payload["file_path"],
         "module_num": h.payload["module_num"], "text": h.payload["text"]}
        for h in hits
    ])
```

**Agent definition**:
```python
textbook_agent = Agent(
    name="Textbook Assistant",
    instructions=(
        "You answer student questions about a robotics textbook. "
        "Always call search_textbook to find relevant passages before answering. "
        "Synthesize a concise answer from the retrieved passages; do not invent facts."
    ),
    model="gemini-2.5-flash",
    tools=[search_textbook],
)
```

**Endpoint usage** (`main.py`):
```python
result = await Runner.run(
    textbook_agent,
    input=request.question,
    context={"module_num": module_num},  # if context resolved from request
)
answer = result.final_output
```

Sources are recovered from the tool-call output captured in `result.new_items` (the `search_textbook` tool return value), parsed back into `SourceReference` objects — preserving the existing `ChatResponse` schema (FR-010).

**Model**: `gemini-2.5-flash` — selected for latency (SC-003: <10s) over `gemini-2.5-pro`.

**Alternatives considered**:
- LiteLLM-style `model="litellm/gemini/gemini-2.5-flash"` — requires extra `litellm` dependency; rejected since the OpenAI-compatible endpoint approach needs no extra package.
- Per-agent `OpenAIChatCompletionsModel` instance instead of `set_default_openai_client` — viable, but global default keeps configuration centralized in one place per clarification Q4.
- Keeping Cohere `command-r-plus` for generation — rejected; user explicitly mandated OpenAI Agents SDK + Gemini.

**New dependency**: `openai-agents` (pulls in `openai` SDK as a transitive dependency for `AsyncOpenAI`).


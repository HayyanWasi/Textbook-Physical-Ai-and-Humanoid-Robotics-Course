# Data Model: RAG Question-Answering Pipeline

**Feature**: `005-rag-pipeline` | **Date**: 2026-06-14

---

## Entities

### 1. Chunk (Qdrant Point)

The core storage unit — one `##`-level section from a textbook MDX file.

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| `id` | `UUID` (string) | `uuid5(NAMESPACE_URL, "{file_path}#{heading}")` | Deterministic — allows idempotent re-ingestion |
| `vector` | `float[1536]` | Cohere `embed-v4.0` | Semantic embedding of chunk text |
| `text` | `str` | MDX section body | Full prose text of the `##` section |
| `file_path` | `str` | MDX filename (relative to `frontend/docs/`) | e.g., `module-1/chapter-1-middleware` |
| `chapter_num` | `int` | Parsed from filename | e.g., `1` from `chapter-1-*` |
| `module_num` | `int` | Parsed from directory | e.g., `1` from `module-1/` |
| `heading` | `str` | `##` heading text | e.g., `"How ROS 2 Works as Robotic Middleware"` |

**Qdrant collection**: `textbook-chunks`  
**Distance metric**: Cosine  
**Vector size**: 1536

**Validation rules**:
- `text` must be non-empty after stripping (skip chunks with empty body)
- `file_path` must be a relative path string without leading `/`
- `chapter_num` and `module_num` must be positive integers

**Payload stored in Qdrant** (everything except `id` and `vector`):
```json
{
  "text": "## How ROS 2 Works as Robotic Middleware\n\nROS 2 is the dominant...",
  "file_path": "module-1/chapter-1-middleware",
  "chapter_num": 1,
  "module_num": 1,
  "heading": "How ROS 2 Works as Robotic Middleware"
}
```

---

### 2. Question (API Request Body)

The student's query submitted by `RagChatbot.jsx`.

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `question` | `str` | Yes | 1–2000 characters; reject if empty or > 2000 chars |
| `context` | `str` | No | If provided, one of `"module-1"`, `"module-2"`, `"module-3"`, `"module-4"`; used to pre-filter Qdrant results |

**Validation**:
- Empty `question` → `400 Bad Request`
- `question` > 2000 characters → `400 Bad Request` with message "Question too long (max 2000 characters)"
- Unknown `context` value → silently ignore, perform unfiltered search

---

### 3. Source Reference

A lightweight struct embedded in the API response indicating which chunk contributed to the answer.

| Field | Type | Description |
|-------|------|-------------|
| `file` | `str` | `file_path` value from Qdrant payload |
| `heading` | `str` | `heading` value from Qdrant payload |
| `module_num` | `int` | Module number for display |

---

### 4. Answer (API Response Body)

| Field | Type | Always present | Description |
|-------|------|----------------|-------------|
| `answer` | `str` | On success | Generated answer text from the OpenAI Agents SDK `Agent` (Gemini `gemini-2.5-flash`) |
| `sources` | `SourceReference[]` | On success | List of chunks used as grounding context (1–5 items) |
| `error` | `str` | On failure | Human-readable error message |

---

## State Transitions

### Ingestion State Machine

```
[MDX files on disk]
    │ ingest.py starts
    ▼
PARSING: strip frontmatter, JSX, imports → extract chunks
    │ chunk.text is non-empty
    ▼
BATCHING: group chunks into batches of 90
    │ each batch
    ▼
EMBEDDING: send batch to Cohere embed-v4.0
    │ success → vectors returned
    │ rate-limit error → retry with backoff (max 3 retries)
    ▼
UPSERTING: send PointStruct list to Qdrant
    │ success
    ▼
[Collection "textbook-chunks" populated]
    │ 13s delay before next batch
    ▼
[repeat for all batches]
    ▼
COMPLETE: log total chunks, elapsed time
```

### Query State Machine

```
POST /api/chat { question, context? }
    │ validation: question non-empty, length ≤ 2000
    │ invalid → 400
    ▼
EMBEDDING: Cohere embed-v4.0 (input_type="search_query")
    │ error → 503 with "Embedding service unavailable"
    ▼
AGENT RUN: OpenAI Agents SDK Agent (Gemini gemini-2.5-flash)
    │ Agent calls search_textbook(query, module_num?) tool
    ▼
RETRIEVAL (inside tool): Qdrant query_points(limit=5, filter=module_num?)
    │ 0 results (empty collection) → 503 with "Knowledge base not populated"
    ▼
GENERATION: Agent synthesizes answer from tool output
    │ error → 503 with "Generation service unavailable"
    ▼
200 { answer, sources }
```

---

## Qdrant Payload Filter (optional context scoping)

When `context` is provided in the request:

```python
from qdrant_client.models import Filter, FieldCondition, MatchValue

module_num = int(context.split("-")[1])  # "module-2" → 2
query_filter = Filter(
    must=[FieldCondition(key="module_num", match=MatchValue(value=module_num))]
)
```

When `context` is absent or unrecognised: no filter applied, search across all modules.

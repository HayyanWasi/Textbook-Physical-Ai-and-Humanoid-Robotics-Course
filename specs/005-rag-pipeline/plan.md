# Implementation Plan: RAG Question-Answering Pipeline (OpenAI Agents SDK + Gemini)

**Branch**: `005-rag-pipeline` | **Date**: 2026-06-14 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-rag-pipeline/spec.md`

**Note**: This update supersedes the original Cohere-only generation design captured in `research.md` §2. Embeddings (Cohere `embed-v4.0`) and retrieval (Qdrant) are unchanged; only the answer-generation step is replaced with an agentic flow.

## Summary

The backend already implements ingestion (`backend/ingest.py`) and a `/api/chat` endpoint (`backend/main.py`) using Cohere for embeddings and Qdrant for retrieval. Per the 2026-06-14 clarification session, the generation step is replaced with an **OpenAI Agents SDK `Agent`** running on **Google Gemini (`gemini-2.5-flash`)** via a custom `AsyncOpenAI` client pointed at Gemini's OpenAI-compatible endpoint. The Agent is given a `search_textbook` function tool backed by the existing Qdrant `query_points` retrieval (including the `module_num` filter), and decides when to call it to ground its answer. Embeddings, retrieval, payload schema, and the frontend widget are unchanged from the current working implementation.

## Technical Context

**Language/Version**: Python 3.11+ (existing `backend/.venv`)
**Primary Dependencies**: FastAPI, uvicorn, `cohere` (embeddings only), `qdrant-client`, `python-dotenv`, **`openai-agents`** (new), `openai` (transitive, used for `AsyncOpenAI` custom client)
**Storage**: Qdrant Cloud collection `textbook-chunks` (1536-dim, Cosine) — unchanged
**Testing**: Manual `curl` + Playwright smoke test against `/api/chat` (existing pattern in `quickstart.md`)
**Target Platform**: Local FastAPI server (`uvicorn`, port 8000) + Docusaurus dev server (port 3000)
**Project Type**: Web application (backend + frontend, existing structure)
**Performance Goals**: Answer returned within 10s (SC-003); `gemini-2.5-flash` chosen specifically for low latency
**Constraints**: Embedding model/vector dimensions must not change (no re-ingestion); Gemini accessed only via OpenAI-compatible endpoint + `GEMINI_API_KEY` (already present in `backend/.env`); module-scoping behavior (FR-008) must be preserved
**Scale/Scope**: Single `/api/chat` endpoint, single Agent, single tool (`search_textbook`), ~70 indexed chunks across 12 chapters

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The project constitution (`.specify/memory/constitution.md`) is an unfilled template — no project-specific principles or gates are defined. No gate violations to evaluate. ✅ PASS (no constraints to check against).

## Project Structure

### Documentation (this feature)

```text
specs/005-rag-pipeline/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output — updated with §8 (Agents SDK + Gemini)
├── data-model.md         # Phase 1 output — updated (no entity shape changes)
├── quickstart.md        # Phase 1 output — updated with GEMINI_API_KEY + new dependency
├── contracts/           # Phase 1 output — chat-api.yaml unchanged (response shape stable)
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
backend/
├── main.py              # FastAPI app — /api/chat handler updated to call the Agent
├── ingest.py            # Unchanged (Cohere embeddings, Qdrant upsert, module_num index)
├── agent.py             # NEW — Agents SDK setup: custom AsyncOpenAI client (Gemini),
│                         #       search_textbook function tool, Agent definition
├── requirements.txt     # + openai-agents
└── .env                 # + GEMINI_API_KEY (already present)

frontend/
└── src/components/RagChatbot.jsx   # Unchanged — response shape (answer + sources) is stable
```

**Structure Decision**: Existing `backend/` + `frontend/` web-application layout is retained. The only structural addition is `backend/agent.py`, isolating Agents SDK / Gemini client setup and the `search_textbook` tool from the FastAPI request-handling code in `main.py`. This keeps `main.py` focused on HTTP concerns (validation, CORS, error mapping) while `agent.py` owns the agentic generation logic — consistent with the existing single-file-per-concern style of `backend/`.

## Complexity Tracking

*No constitution violations — table not required.*

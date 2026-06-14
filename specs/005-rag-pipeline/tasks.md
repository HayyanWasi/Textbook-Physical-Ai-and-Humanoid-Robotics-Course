# Tasks: RAG Question-Answering Pipeline — OpenAI Agents SDK + Gemini Generation

**Input**: Design documents from `specs/005-rag-pipeline/`
**Branch**: `005-rag-pipeline` | **Date**: 2026-06-14
**Prerequisites**: plan.md ✅ | spec.md ✅ (Clarifications 2026-06-14) | research.md ✅ (§8) | data-model.md ✅ | contracts/chat-api.yaml ✅ | quickstart.md ✅

**Tests**: Not requested — no test tasks generated. Smoke-test steps are in Phase 6 (Polish).

**Scope**: This task list covers the **generation-step replacement** only (Cohere `command-r-plus` → OpenAI Agents SDK Agent on Gemini `gemini-2.0-flash`). Ingestion (US2), embeddings, Qdrant retrieval/module-scoping, and the frontend widget (US3) are already implemented and unchanged — see `specs/005-rag-pipeline/tasks.md` (prior round, all complete).

**Organization**: Tasks grouped by user story (US1: Student Q&A API is the only story affected; US2/US3 have no new tasks).

---

## Format: `[ID] [P?] [Story?] Description — file path`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[US#]**: Which user story this task delivers
- No [P] marker on tasks within the same file — they must run sequentially

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Declare the new dependency and document the new required environment variable before any code changes.

- [x] T001 [P] Add `openai-agents>=0.0.1` to `backend/requirements.txt` (pulls in `openai` SDK transitively for `AsyncOpenAI`)
- [x] T002 [P] Add `GEMINI_API_KEY=your-gemini-key-here` to `backend/.env.example` (or create the file if it does not exist, documenting all four required vars: `COHERE_API_KEY`, `GEMINI_API_KEY`, `QDRANT_URL`, `QDRANT_API_KEY`)
- [x] T003 Run `pip install -r backend/requirements.txt` inside `backend/.venv` to install `openai-agents` and verify `import agents` succeeds

**Checkpoint**: `openai-agents` is installed in `backend/.venv`; `GEMINI_API_KEY` documented and present in `backend/.env` (already confirmed present).

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Create the new `backend/agent.py` module — Gemini client wiring, the `search_textbook` function tool, and the `Agent` definition. This is shared infrastructure that the US1 endpoint (Phase 3) depends on.

**⚠️ CRITICAL**: Phase 3 cannot be implemented until T004–T006 complete.

- [x] T004 [P] Create `backend/agent.py` — configure the custom Gemini client per `research.md` §8: instantiate `AsyncOpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai/", api_key=os.getenv("GEMINI_API_KEY"))`, call `set_default_openai_client(client=gemini_client, use_for_tracing=False)`, `set_default_openai_api("chat_completions")`, and `set_tracing_disabled(disabled=True)`
- [x] T005 [US1] In `backend/agent.py`, implement the `search_textbook` `@function_tool` — accepts `query: str` and optional `module_num: int | None`, embeds `query` via the existing Cohere `embed-v4.0` (`input_type="search_query"`), builds an optional `Filter(must=[FieldCondition(key="module_num", match=MatchValue(value=module_num))])`, calls `qdrant.query_points(collection_name="textbook-chunks", query=vector, limit=5, query_filter=query_filter).points`, and returns a JSON string of `[{"heading", "file_path", "module_num", "text"}, ...]` for each hit
- [x] T006 [US1] In `backend/agent.py`, define `textbook_agent = Agent(name="Textbook Assistant", instructions="...", model="gemini-2.5-flash", tools=[search_textbook])` per `research.md` §8, with instructions directing the agent to always call `search_textbook` before answering and to avoid inventing facts

**Checkpoint**: `backend/agent.py` exports `textbook_agent` and `search_textbook`; `python -c "from backend.agent import textbook_agent"` (or equivalent from `backend/`) imports without error.

---

## Phase 3: User Story 1 — Student Q&A API (Priority: P1) 🎯 MVP

**Goal**: `POST /api/chat` generates its answer via the OpenAI Agents SDK `Agent` (Gemini `gemini-2.0-flash`) instead of Cohere `command-r-plus`, while preserving the existing request/response contract (`{question, context?}` → `{answer, sources}`) and module-scoping behavior.

**Independent Test**: With the Qdrant collection populated (already done), `curl -X POST http://localhost:8000/api/chat -H "Content-Type: application/json" -d '{"question":"What is ROS 2?","context":"module-1"}'` returns a non-empty `answer` and `sources` referencing `module-1` content, generated via Gemini (not Cohere chat).

### Implementation for User Story 1

- [x] T007 [US1] In `backend/main.py`, remove the direct Cohere `co.chat(...)` call and the inline Qdrant `query_points` retrieval from the `/api/chat` handler; import `textbook_agent` and `Runner` from `backend.agent` / `agents`
- [x] T008 [US1] In `backend/main.py`, in the `/api/chat` handler, resolve `module_num` from `request.context` (existing `"module-N"` parsing logic) and call `result = await Runner.run(textbook_agent, input=request.question, context={"module_num": module_num})`; set `answer = result.final_output`
- [x] T009 [US1] In `backend/main.py`, extract `sources` for the `ChatResponse` by parsing the JSON returned by the `search_textbook` tool call captured in `result.new_items` (per `research.md` §8), mapping each retrieved chunk to a `SourceReference(file=..., heading=..., module_num=...)`
- [x] T010 [US1] In `backend/main.py`, update error handling in `/api/chat`: catch exceptions from `Runner.run` (Gemini/Agent failures) and the Cohere embed call (inside `search_textbook`, surfaced via tool error) and map both to `503` responses with the existing user-friendly messages ("Embedding service temporarily unavailable" / "Answer generation temporarily unavailable")
- [x] T011 [US1] Convert the `/api/chat` route handler in `backend/main.py` to `async def` (required for `await Runner.run(...)`)

**Checkpoint**: `POST /api/chat` returns `{answer, sources}` generated by Gemini via the Agents SDK; module-scoped (`context: "module-N"`) and unscoped requests both work; all three error paths (empty DB, embedding down, generation down) still return structured `503`/`400` JSON, not stack traces.

---

## Phase 4: User Story 2 — Admin Ingestion (Priority: P2)

**No new tasks.** Ingestion (`backend/ingest.py`), the Cohere `embed-v4.0` embedding pipeline, and the `module_num` payload index are unchanged by this update — see prior `tasks.md` (T008–T010, complete).

---

## Phase 5: User Story 3 — Widget Integration (Priority: P3)

**No new tasks.** `frontend/src/components/RagChatbot.jsx` is unaffected — the `/api/chat` response shape (`{answer, sources}`) is unchanged, so no frontend changes are required.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: End-to-end validation of the new Gemini-backed generation path and final consistency checks.

- [x] T012 Run end-to-end smoke test: start `uvicorn backend.main:app --port 8000`, confirm `GET /health` returns `{"status":"ok"}`, then run the `curl` from Phase 3's Independent Test and confirm the `answer` text is coherent and `sources` reference real chapters
- [x] T013 [P] Verify no secrets in tracked files: `git grep -i "GEMINI_API_KEY\s*=" -- ':!backend/.env*'` and equivalent for `COHERE_API_KEY`/`QDRANT_API_KEY` return zero matches (keys only in `backend/.env`, which is gitignored)
- [x] T014 [P] Test in browser per `specs/005-rag-pipeline/quickstart.md`: with both servers running, open a chapter page, ask a question via the widget, confirm the answer renders and matches the `curl` output style (no regressions from the agentic generation change)

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup)        → No dependencies — start immediately
Phase 2 (Foundational) → Depends on Phase 1 (T001, T003 — openai-agents installed)
Phase 3 (US1 - API)    → Depends on Phase 2 (T004-T006 — backend/agent.py exists)
Phase 4 (US2 - Ingest) → No new tasks; already complete
Phase 5 (US3 - Widget) → No new tasks; already complete
Phase 6 (Polish)       → Depends on Phase 3
```

### User Story Dependencies

- **US1 (P1)**: All new work for this round lives here — Phases 1, 2, and 3 are effectively one continuous chain for US1.
- **US2 (P2)**: Unaffected; no dependency on this round's changes.
- **US3 (P3)**: Unaffected; no dependency on this round's changes.

### Within User Story 1

- T004 (Gemini client config) → T005 (search_textbook tool, needs client configured) → T006 (Agent, needs tool) → T007–T011 (main.py integration, sequential same-file edits)

### Parallel Opportunities

- T001 + T002 can run in parallel (different files)
- T013 + T014 can run in parallel (independent verification steps, after T012)

---

## Parallel Example: Phase 1

```bash
# T001 and T002 can run in parallel (different files):
Task A: Add openai-agents to backend/requirements.txt
Task B: Add GEMINI_API_KEY to backend/.env.example
```

---

## Implementation Strategy

### MVP First (This Round)

1. Complete Phase 1 (Setup) — install `openai-agents`
2. Complete Phase 2 (Foundational) — build `backend/agent.py`
3. Complete Phase 3 (US1) — wire `/api/chat` to the Agent
4. **STOP and VALIDATE**: `curl -X POST http://localhost:8000/api/chat -d '{"question":"What is ROS 2?","context":"module-1"}' -H "Content-Type: application/json"` returns a Gemini-generated answer with correct `sources`
5. Complete Phase 6 (smoke test + secrets check + browser check)

---

## Notes

- **Backwards compatibility**: The `ChatRequest`/`ChatResponse` Pydantic models and `/api/chat` route signature do not change — only the implementation inside the handler.
- **GEMINI_API_KEY** is already present in `backend/.env`; no new secret needs to be sourced.
- **Tracing**: `set_tracing_disabled(disabled=True)` is required because no OpenAI API key is configured for the Agents SDK's default tracing exporter.
- [P] tasks = different files, no blocking dependencies between them
- [US#] label maps each task to its user story for traceability

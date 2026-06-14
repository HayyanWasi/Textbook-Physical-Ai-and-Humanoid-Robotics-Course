---
id: "003"
title: RAG Pipeline Tasks Generation
stage: tasks
date: 2026-06-14
surface: agent
model: claude-sonnet-4-6
feature: 005-rag-pipeline
branch: 005-rag-pipeline
user: HayyanWasi
command: /sp.tasks
labels: ["tasks","rag","fastapi","qdrant","cohere","backend","chatbot","ingestion","widget"]
links:
  spec: specs/005-rag-pipeline/spec.md
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - specs/005-rag-pipeline/tasks.md
tests:
  - "null"
---

## Prompt

# Implementation Tasks: RAG Backend Connection

## Objective
Build the FastAPI server, ingest the textbook markdown into Qdrant using Cohere embeddings, and connect the frontend widget.

## Prerequisites
- Docusaurus contains valid markdown for Modules 1, 2, and 3.

## Task Checklist

### 1. Environment Setup
- [ ] Create `/backend` directory.
- [ ] Create `requirements.txt` with `fastapi`, `uvicorn`, `qdrant-client`, `cohere`, `python-dotenv`, `pydantic`.
- [ ] Create `.env.example` file outlining required keys (`COHERE_API_KEY`, `QDRANT_URL`, `QDRANT_API_KEY`).

### 2. Data Ingestion Pipeline
- [ ] Create `/backend/ingest.py`.
- [ ] Write logic to read all `.mdx` files in `../docs/`.
- [ ] Split the text strictly using Markdown headings (`##`) as boundaries.
- [ ] Connect to Cohere using the `cohere` SDK. Batch the text chunks.
- [ ] Generate embeddings and add a `time.sleep()` between batches to respect free tier limits.
- [ ] Connect to Qdrant and upload the vectors alongside their metadata (module ID, chapter title).

### 3. API Development
- [ ] Create `/backend/main.py` and initialize FastAPI with CORS middleware.
- [ ] Create a Pydantic model for the incoming request (`query`, `context`, `selected_text`).
- [ ] Build the `POST /api/chat` endpoint. It must embed the user query via Cohere, search Qdrant using the context filter, and return a final generated text response.

### 4. Frontend Wiring
- [ ] Modify the Docusaurus `<RagChatbot />` component to send its payload to `http://localhost:8000/api/chat`.
- [ ] Ensure the widget gracefully displays a loading state and the AI response.

## Execution Rules
- Never hardcode API keys.
- Commit using: `feat(backend): implement FastAPI RAG pipeline with Cohere and Qdrant`.

## Response snapshot

Generated `specs/005-rag-pipeline/tasks.md` with 13 tasks across 6 phases organized by user story.

**Phase breakdown**:
- Phase 1 (Setup): T001–T003 — gitignore security fix, requirements.txt, .env.example
- Phase 2 (Foundational): T004 — FastAPI app scaffold with CORS, health check, client singletons
- Phase 3 (US1 P1): T005–T007 — POST /api/chat Pydantic models, core embed+search+generate logic, error handling
- Phase 4 (US2 P2): T008–T010 — MDX parser, Qdrant collection setup + file scan, batch embed + upsert
- Phase 5 (US3 P3): T011 — RagChatbot.jsx fetch() implementation
- Phase 6 (Polish): T012–T013 — end-to-end smoke test, secret scan

**Key notes encoded in tasks**:
- T001 is highest priority (live keys in backend/.env not covered by gitignore)
- Env var casing mismatch flagged (lowercase `qdrant_api_key` in .env vs uppercase in code)
- Cohere SDK v2 interface (`ClientV2`, not `Client`) called out explicitly
- Parallel opportunities: T002+T003 in Phase 1; T004+T008 across Phases 2 & 4; T011 anytime
- User-provided commit message preserved: `feat(backend): implement FastAPI RAG pipeline with Cohere and Qdrant`

## Outcome

- ✅ Impact: 13 immediately-executable tasks covering all 3 user stories; MVP scope = Phases 1-4 (backend only)
- 🧪 Tests: None generated (not requested in spec)
- 📁 Files: specs/005-rag-pipeline/tasks.md
- 🔁 Next prompts: /sp.implement
- 🧠 Reflection: Ordering US2 (ingestion) code after US1 (API) in task file matches spec priority; but MVP delivery note correctly guides developer to run ingestion before testing API end-to-end

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Format validation — all 13 tasks have checkbox + ID + story label (where applicable) + file path — PASS
- Prompt variant (if applicable): User provided a detailed task checklist; tasks.md synthesizes this with the design docs (data model, API contracts) for more precise implementation detail
- Next experiment: N/A

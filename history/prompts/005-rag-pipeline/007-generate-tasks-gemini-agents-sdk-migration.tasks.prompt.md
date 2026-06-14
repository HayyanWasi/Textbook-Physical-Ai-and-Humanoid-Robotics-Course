---
id: 007
title: Generate tasks for Gemini Agents SDK migration
stage: tasks
date: 2026-06-14
surface: agent
model: claude-sonnet-4-6[1m]
feature: 005-rag-pipeline
branch: 005-rag-pipeline
user: HayyanWasi
command: /sp.tasks
labels: ["tasks", "agents-sdk", "gemini", "rag"]
links:
  spec: specs/005-rag-pipeline/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/005-rag-pipeline/tasks.md
tests:
 - none
---

## Prompt

(empty — /sp.tasks invoked with no additional arguments, following the plan update from the previous turn)

## Response snapshot

Ran `check-prerequisites.ps1 -Json` (FEATURE_DIR=specs/005-rag-pipeline, AVAILABLE_DOCS: research.md, data-model.md, contracts/, quickstart.md). Read the existing `tasks.md` (all 13 prior tasks marked complete — Cohere-based implementation already shipped) and the updated `plan.md`/`research.md` §8 from the previous /sp.plan run.

Rewrote `tasks.md` to cover only the **incremental generation-step replacement** (Cohere `command-r-plus` → OpenAI Agents SDK Agent on Gemini `gemini-2.0-flash`), since ingestion (US2) and the frontend widget (US3) are unaffected and already complete:

- **Phase 1 (Setup)**: T001 add `openai-agents` dependency, T002 document `GEMINI_API_KEY` in `.env.example`, T003 install and verify import.
- **Phase 2 (Foundational)**: T004-T006 create new `backend/agent.py` — custom `AsyncOpenAI` Gemini client via `set_default_openai_client`, `search_textbook` function tool wrapping Cohere embed + Qdrant `query_points` with `module_num` filter, and the `textbook_agent` Agent definition (`gemini-2.0-flash`).
- **Phase 3 (US1)**: T007-T011 rewire `/api/chat` in `backend/main.py` to call `Runner.run(textbook_agent, ...)`, extract sources from the tool-call result, preserve error-handling/503 paths, convert handler to `async def`.
- **Phase 4/5 (US2/US3)**: explicitly marked "no new tasks" — unaffected by this change.
- **Phase 6 (Polish)**: T012-T014 smoke test, secrets grep, browser check.

All tasks follow the strict checklist format (`- [ ] T0XX [P?] [US#?] Description — file path`). Dependencies, parallel opportunities, and an MVP-first implementation strategy were documented.

## Outcome

- ✅ Impact: tasks.md now provides an executable, dependency-ordered checklist for implementing the OpenAI Agents SDK + Gemini generation swap without disturbing the working Cohere-embeddings/Qdrant/frontend stack.
- 🧪 Tests: none (tests not requested; smoke-test steps in Phase 6)
- 📁 Files: specs/005-rag-pipeline/tasks.md
- 🔁 Next prompts: /sp.implement to execute T001-T014
- 🧠 Reflection: Scoping tasks.md to only the delta (vs. regenerating all ~14 original tasks) kept the checklist focused and avoided re-doing already-shipped US2/US3 work.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): n/a
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): n/a

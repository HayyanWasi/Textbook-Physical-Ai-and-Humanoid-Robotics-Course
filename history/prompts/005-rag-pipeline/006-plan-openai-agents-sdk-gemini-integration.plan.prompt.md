---
id: 006
title: Plan OpenAI Agents SDK Gemini integration
stage: plan
date: 2026-06-14
surface: agent
model: claude-sonnet-4-6[1m]
feature: 005-rag-pipeline
branch: 005-rag-pipeline
user: HayyanWasi
command: /sp.plan
labels: ["plan", "agents-sdk", "gemini", "rag"]
links:
  spec: specs/005-rag-pipeline/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/005-rag-pipeline/plan.md
 - specs/005-rag-pipeline/research.md
 - specs/005-rag-pipeline/data-model.md
 - specs/005-rag-pipeline/quickstart.md
 - CLAUDE.md
tests:
 - none
---

## Prompt

pdate the implementation plan with the OpenAI Agents SDK + Gemini integration details (client setup, agent/tool
  definitions, dependency additions).

## Response snapshot

Ran `setup-plan.ps1`, loaded `spec.md` (with the 2026-06-14 Clarifications section), the existing `research.md`/`data-model.md`/`contracts/chat-api.yaml`/`quickstart.md`, and the (unfilled) project constitution. Queried Context7 for the OpenAI Agents Python SDK to confirm the `set_default_openai_client` + custom `AsyncOpenAI` pattern for non-OpenAI providers.

Rewrote `plan.md` from the template:
- Technical Context updated: added `openai-agents` + `openai` (transitive) dependencies, noted Gemini access via `GEMINI_API_KEY` and OpenAI-compatible endpoint, preserved Cohere-embeddings/Qdrant/frontend as unchanged.
- Constitution Check: PASS (constitution file is an unfilled template, no gates to evaluate).
- Project Structure: added new `backend/agent.py` (Agents SDK client setup, `search_textbook` function tool, Agent definition), `main.py` updated to call `Runner.run`, `requirements.txt` +`openai-agents`.

Phase 0 (`research.md`): added §8 "OpenAI Agents SDK — Gemini Integration" with concrete code for the custom `AsyncOpenAI` client (`set_default_openai_client`, `set_default_openai_api("chat_completions")`, `set_tracing_disabled`), the `search_textbook` function tool wrapping the existing Qdrant `query_points` + `module_num` filter, the `Agent` definition (`gemini-2.0-flash`), and endpoint usage via `Runner.run`. Marked §2 (Cohere generation) as superseded with a pointer to §8.

Phase 1 (`data-model.md`): updated the Answer entity description and the Query State Machine diagram to show the Agent run + tool-call retrieval flow instead of a direct Cohere chat call. `contracts/chat-api.yaml` response schema unchanged (still `{answer, sources}`).

`quickstart.md`: added `GEMINI_API_KEY` to prerequisites and `.env` example, added `openai-agents>=0.0.1` to expected `requirements.txt`.

Ran `update-agent-context.ps1 -AgentType claude` to refresh `CLAUDE.md` with the new tech stack (Python 3.11+, FastAPI/cohere/qdrant-client/openai-agents/openai, Qdrant Cloud `textbook-chunks`).

## Outcome

- ✅ Impact: Plan now fully specifies the OpenAI Agents SDK + Gemini generation architecture (client setup, tool, agent, endpoint wiring) while preserving Cohere embeddings, Qdrant retrieval, and the existing response contract.
- 🧪 Tests: none (planning only)
- 📁 Files: specs/005-rag-pipeline/{plan.md, research.md, data-model.md, quickstart.md}, CLAUDE.md
- 🔁 Next prompts: /sp.tasks to regenerate tasks.md for backend/agent.py + main.py + requirements.txt changes
- 🧠 Reflection: Constitution file is still a template — future features may need a filled-in constitution to drive real gate checks.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): n/a
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): n/a

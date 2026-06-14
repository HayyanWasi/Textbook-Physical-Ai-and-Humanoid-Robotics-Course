---
id: 005
title: Clarify Gemini Agents SDK integration
stage: spec
date: 2026-06-14
surface: agent
model: claude-sonnet-4-6[1m]
feature: 005-rag-pipeline
branch: 005-rag-pipeline
user: HayyanWasi
command: /sp.clarify
labels: ["clarification", "agents-sdk", "gemini", "rag"]
links:
  spec: specs/005-rag-pipeline/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/005-rag-pipeline/spec.md
tests:
 - none
---

## Prompt

Use Openai agents sdk compulsory  with external (Gemini api key)

## Response snapshot

Ran the clarification workflow against `specs/005-rag-pipeline/spec.md`. The existing spec was built around Cohere for both embedding and generation; the user's instruction to use the OpenAI Agents SDK with a Gemini API key required resolving five architectural ambiguities before the spec could remain implementable:

1. **Integration shape** → Agentic retrieval: a `search_textbook` tool backed by Qdrant, called by an OpenAI Agents SDK `Agent`.
2. **Embedding model** → Stay on Cohere `embed-v4.0` for embeddings (no re-ingestion needed); only generation moves to Gemini.
3. **Module-scoping** → `search_textbook` tool accepts optional `module_num` filter set by FastAPI from the request's `context` field.
4. **Gemini wiring** → Custom `AsyncOpenAI` client pointed at Gemini's OpenAI-compatible endpoint (`https://generativelanguage.googleapis.com/v1beta/openai/`) with `GEMINI_API_KEY`, set as default model provider.
5. **Model choice** → `gemini-2.0-flash`.

Added a `## Clarifications` / `### Session 2026-06-14` section recording all five Q&A pairs, and updated FR-007, FR-008, FR-009, FR-016, FR-017, and the Assumptions section to reflect the agentic Gemini-based generation flow while preserving the Cohere embedding pipeline and module-scoped retrieval.

## Outcome

- ✅ Impact: Spec now reflects an OpenAI Agents SDK + Gemini generation architecture with Cohere embeddings retained; ready for `/sp.plan`.
- 🧪 Tests: none
- 📁 Files: specs/005-rag-pipeline/spec.md
- 🔁 Next prompts: /sp.plan to update implementation plan for Agents SDK + Gemini integration
- 🧠 Reflection: All 5 questions were used; no Outstanding/Deferred categories — coverage was reduced to architecture-impacting decisions only.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): n/a
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): n/a

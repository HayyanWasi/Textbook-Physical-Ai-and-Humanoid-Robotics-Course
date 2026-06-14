---
id: "002"
title: RAG Pipeline Implementation Plan
stage: plan
date: 2026-06-14
surface: agent
model: claude-sonnet-4-6
feature: 005-rag-pipeline
branch: 005-rag-pipeline
user: HayyanWasi
command: /sp.plan
labels: ["plan","rag","fastapi","qdrant","cohere","backend","chatbot","ingestion","openapi"]
links:
  spec: specs/005-rag-pipeline/spec.md
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - specs/005-rag-pipeline/plan.md
  - specs/005-rag-pipeline/research.md
  - specs/005-rag-pipeline/data-model.md
  - specs/005-rag-pipeline/quickstart.md
  - specs/005-rag-pipeline/contracts/chat-api.yaml
tests:
  - "null"
---

## Prompt

read the sp.constitution and /sp.specify for rag-pipeline and generate plan

## Response snapshot

Generated full Phase 0 + Phase 1 plan artifacts for feature `005-rag-pipeline`:

**Phase 0 — research.md**: Resolved all technical decisions:
- Embedding: Cohere `embed-v4.0` (1536 dims), batch 90, 13s inter-batch delay (free tier: 5 calls/min)
- Generation: Cohere `command-r-plus-08-2024` (free tier: 20 calls/min, native RAG `documents` param)
- Vector store: Qdrant Cloud instance (already provisioned in `backend/.env`) — NOT local/Docker
- Idempotent ingestion: `uuid5(NAMESPACE_URL, file_path + heading)` deterministic point IDs
- MDX parsing: Python `re` module to strip frontmatter + JSX + imports, split on `## ` boundaries
- Security gap flagged: `backend/.env` not covered by root `.gitignore`

**Phase 1 artifacts**:
- `data-model.md`: Chunk entity (7 fields), Question/Answer/SourceReference request-response shapes, ingestion and query state machines, Qdrant payload filter for module scoping
- `contracts/chat-api.yaml`: OpenAPI 3.1 spec for `POST /api/chat` and `GET /health`; 3 error conditions (400, 503 × 3)
- `quickstart.md`: 6-step developer setup guide (venv, ingest, backend start, curl test, frontend start, troubleshooting table)
- `plan.md`: Full Technical Context, Constitution Check (6 gates, all PASS), project structure, data flow diagram, endpoint contract summary
- Agent context updated via `update-agent-context.ps1` (Python 3.11+, FastAPI, Cohere, Qdrant Cloud added to CLAUDE.md)

**Key discovery**: `backend/.env` already exists with cloud Qdrant URL + live API keys for Cohere, Qdrant, Gemini, and Neon — plan adjusted to use cloud Qdrant (not local). Security fix required in Task 1.

## Outcome

- ✅ Impact: Complete implementation blueprint ready for /sp.tasks; backend architecture is fully specified with no open decisions
- 🧪 Tests: No tests run (plan stage); manual smoke-test steps documented in quickstart.md
- 📁 Files: plan.md, research.md, data-model.md, quickstart.md, contracts/chat-api.yaml
- 🔁 Next prompts: /sp.tasks, /sp.implement
- 🧠 Reflection: Critical insight — existing backend/.env uses cloud Qdrant not local; spec assumption of local was incorrect; plan corrected accordingly. Also, both Cohere and Gemini keys present — plan stays Cohere-only per spec intent

## Evaluation notes (flywheel)

- Failure modes observed: None — all scripts ran successfully; setup-plan.ps1 and update-agent-context.ps1 both clean
- Graders run and results (PASS/FAIL): Constitution Check — 6 gates, all PASS
- Prompt variant (if applicable): N/A
- Next experiment: Verify Qdrant env var name casing (backend/.env uses lowercase `qdrant_api_key` but code should use `QDRANT_API_KEY`; quickstart.md flags this mismatch)

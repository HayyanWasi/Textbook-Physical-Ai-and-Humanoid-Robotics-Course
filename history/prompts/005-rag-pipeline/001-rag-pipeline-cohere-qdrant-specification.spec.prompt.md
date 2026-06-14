---
id: "001"
title: RAG Pipeline Cohere Qdrant Specification
stage: spec
date: 2026-06-14
surface: agent
model: claude-sonnet-4-6
feature: 005-rag-pipeline
branch: 005-rag-pipeline
user: HayyanWasi
command: /sp.specify
labels: ["spec","rag","fastapi","qdrant","cohere","backend","chatbot","ingestion"]
links:
  spec: specs/005-rag-pipeline/spec.md
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - specs/005-rag-pipeline/spec.md
  - specs/005-rag-pipeline/checklists/requirements.md
tests:
  - "null"
---

## Prompt

FastAPI & Qdrant RAG Pipeline (Cohere Integration)

## Part 1: Reference Architecture Analysis
- The system requires a backend to process user questions, search the textbook content, and return AI-generated answers.
- We are replacing OpenAI embeddings with Cohere's embedding models to utilize their free Developer Tier.

## Part 2: Current Architecture Analysis
Current state: Docusaurus renders 12 chapters of markdown. The frontend React component is currently disconnected.

Files to be created/affected:
- `/backend/main.py`
- `/backend/ingest.py`
- `/backend/requirements.txt`
- `.env`

## Part 3: Implementation Plan
Phase 1: Setup FastAPI environment and routing.
Phase 2: Write `ingest.py` to parse `.mdx` files and split them by `##` headings. It must batch chunks and apply time delays to respect Cohere's free tier rate limits before uploading vectors to Qdrant.
Phase 3: Write the `/api/chat` endpoint. It must embed the query using Cohere, search Qdrant, and generate a text response.
Phase 4: Update the Docusaurus frontend widget to send POST requests to the local server.

## Constraints
- FastAPI must run on `localhost:8000`.
- CORS must allow requests from `localhost:3000`.
- `ingest.py` MUST batch text inputs to avoid Cohere API rate limits.
- No user authentication system is required.

## Success Criteria
- Running `python backend/ingest.py` populates Qdrant with the text from Modules 1, 2, and 3 without crashing from rate limits.
- The Docusaurus widget successfully returns an answer generated via the FastAPI backend.

## Response snapshot

Created branch `005-rag-pipeline` and wrote a full feature specification at `specs/005-rag-pipeline/spec.md`. The spec defines:
- 3 user stories (P1–P3): student Q&A flow, administrator ingestion, widget integration
- 17 functional requirements (FR-001–FR-017) across three areas: ingestion pipeline, query/answer API, and frontend widget
- 5 key entities: Chunk, Question, Answer, Batch, Vector Database Collection
- 7 measurable success criteria (SC-001–SC-007) all technology-agnostic
- 7 clearly stated assumptions (Cohere tier capabilities, Qdrant local setup, port conventions, auth scope)
- 5 edge cases including empty DB, embedding service outage, JSX tag stripping, re-ingestion, oversized queries
- Spec quality checklist at `specs/005-rag-pipeline/checklists/requirements.md` — all items pass

Implementation-specific constraints (port 8000, CORS localhost:3000, batch rate limiting) are recorded as Assumptions, keeping FRs technology-agnostic.

## Outcome

- ✅ Impact: Full RAG pipeline specification ready; covers ingestion, retrieval, generation, and widget integration
- 🧪 Tests: No tests run (spec stage)
- 📁 Files: specs/005-rag-pipeline/spec.md, specs/005-rag-pipeline/checklists/requirements.md
- 🔁 Next prompts: /sp.plan, /sp.tasks, /sp.implement
- 🧠 Reflection: Spec deliberately separates technical constraints (ports, CORS) into Assumptions rather than FRs to keep the spec stakeholder-readable; the plan stage can translate these back into technical decisions

## Evaluation notes (flywheel)

- Failure modes observed: create-new-feature.ps1 positional parameter binding error (non-blocking; branch and spec stub still created successfully)
- Graders run and results (PASS/FAIL): Spec quality checklist — all 12 items PASS
- Prompt variant (if applicable): N/A
- Next experiment: Check whether Cohere free tier includes a `/generate` or `/chat` endpoint before /sp.plan to avoid mid-plan assumption failure

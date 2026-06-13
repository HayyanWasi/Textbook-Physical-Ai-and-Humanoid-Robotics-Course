---
id: "001"
title: Initial Constitution Ratification
stage: constitution
date: 2026-06-13
surface: agent
model: claude-sonnet-4-6
feature: none
branch: clean-start
user: HayyanWasi
command: /sp.constitution
labels: ["constitution","architecture","setup","textbook","fastapi","docusaurus","rag"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - history/prompts/constitution/001-initial-constitution-ratification.constitution.prompt.md
tests:
  - N/A
---

## Prompt

Physical AI & Humanoid Robotics Textbook

## Architecture Principles

- **Strict Decoupling:** The Docusaurus frontend and FastAPI backend remain completely separate entities. The frontend is a static site; the backend is a standalone API service.
- **Context-Bound RAG:** The retrieval pipeline must filter vector searches in Qdrant using metadata (chapter ID or section ID) before sending payloads to OpenAI. It must strictly prioritize user-selected text over general chapter context.
- **API Gateway Pattern:** The embedded frontend chat widget communicates exclusively with the FastAPI backend. The frontend never calls OpenAI or Qdrant directly.

## Technology Constraints

- **Frontend:** Docusaurus deployed to GitHub Pages. The chat widget must be a lightweight React component embedded into the standard Docusaurus documentation layout.
- **Backend:** Python 3.12+ using FastAPI.
- **Databases:** Qdrant Cloud Free Tier exclusively for vector embeddings; Neon Serverless Postgres for system metadata and rate-limit tracking.
- **LLM Integration:** OpenAI Agents / ChatKit SDKs handled strictly on the backend.
- **Security & Cost Control:** Because the API is unauthenticated, FastAPI must implement strict IP-based rate limiting (e.g., token-bucket) to prevent OpenAI API abuse and cost overruns.

## Content Quality Standards (Textbook)

- **Length & Density:** Fixed at exactly 16 chapters (4 modules, 4 chapters each). Content must be high-signal and conceptual. Eliminate repetitive filler to stay within the 150-page limit.
- **Math Constraint:** Zero heavy mathematical derivations. Explain ROS 2 kinematics, physics engines, and VSLAM path planning using system logic and architectural concepts.
- **Formatting:** Use strict MDX/Markdown. Code blocks must be properly tagged. Use Docusaurus admonitions (notes, warnings, tips) to break up text visually.

## Code Quality Standards (Backend)

- **Type Safety:** Strict type hinting required on all Python functions and parameters. Use Pydantic models for all API request and response validation.
- **Error Handling:** Implement graceful degradation. If Qdrant or OpenAI times out or fails, the FastAPI backend must return a clean, handled error to the frontend widget, never a raw stack trace.
- **Environment Variables:** All API keys and database URIs (OpenAI, Qdrant, Neon) must be loaded via `.env` files. Never commit secrets.

## Workflow Rules

- **Paced Execution:** Do not write code or content in bulk. Generate the backend plan and table of contents first, wait for approval, then execute sequentially.
- **Spec-Driven Consistency:** Flag any deviation from this constitution immediately. Do not silently ignore the math constraints or the rate-limiting requirements.
- **Commit Standards:** Commit after each completed chapter or API route using the format: `type(scope): description`.

## Response snapshot

Constitution v1.0.0 ratified and written to `.specify/memory/constitution.md`. Template
placeholders replaced with project-specific content across 6 sections: Core Principles (3),
Technology Constraints, Content Quality Standards, Code Quality Standards, Workflow Rules,
and Governance. All "should" language upgraded to MUST/MUST NOT. Sync Impact Report prepended
as HTML comment. No placeholders remain. Templates (plan, spec, tasks) are compatible without
structural changes.

## Outcome

- ✅ Impact: Constitution v1.0.0 ratified for Physical AI & Humanoid Robotics Textbook project
- 🧪 Tests: N/A — governance document, no executable tests
- 📁 Files: .specify/memory/constitution.md (created), history/prompts/constitution/001-initial-constitution-ratification.constitution.prompt.md (created)
- 🔁 Next prompts: /sp.specify to define a feature spec; /sp.plan to generate backend architecture plan
- 🧠 Reflection: User supplied complete principle set; no clarifiers needed. All bracket tokens resolved.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A

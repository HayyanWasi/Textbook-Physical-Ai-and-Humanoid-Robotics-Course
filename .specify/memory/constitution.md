<!--
SYNC IMPACT REPORT
==================
Version change: [NEW] → 1.0.0
Modified principles: N/A — initial ratification
Added sections:
  - Core Principles (3 architecture principles)
  - Technology Constraints
  - Content Quality Standards (Textbook)
  - Code Quality Standards (Backend)
  - Workflow Rules
  - Governance
Removed sections: N/A
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ compatible (no structural changes required)
  - .specify/templates/spec-template.md ✅ compatible (no structural changes required)
  - .specify/templates/tasks-template.md ✅ compatible (no structural changes required)
  - .specify/templates/commands/ ✅ no command files found — no action needed
Deferred TODOs: None. All fields resolved.
-->

# Physical AI & Humanoid Robotics Textbook Constitution

## Core Principles

### I. Strict Decoupling

The Docusaurus frontend and FastAPI backend MUST remain completely separate entities at all times.
The frontend is a static site deployed to GitHub Pages; it MUST NOT contain any server-side logic.
The backend is a standalone FastAPI service; it MUST NOT serve static frontend assets.
Any coupling between these layers MUST be routed exclusively through the defined API contract.

**Rationale**: Prevents tight coupling that makes independent deployment, scaling, and testing
impossible. Enables the frontend to be a pure CDN artifact while the backend is a managed service.

### II. Context-Bound RAG

The retrieval pipeline MUST filter all vector searches in Qdrant using metadata (chapter ID or
section ID) before constructing any payload sent to OpenAI. User-selected text MUST be
prioritized over general chapter context in all retrieval operations. Unfiltered vector searches
across the entire corpus are prohibited.

**Rationale**: Prevents irrelevant context injection into LLM prompts, which degrades answer
quality and inflates token costs. Metadata filtering keeps responses grounded to the reader's
current location in the textbook.

### III. API Gateway Pattern

The embedded frontend chat widget MUST communicate exclusively with the FastAPI backend.
The frontend MUST NOT call OpenAI, Qdrant, or any other external service directly.
All LLM orchestration, vector retrieval, and rate limiting MUST execute server-side.

**Rationale**: Protects API keys from client-side exposure, centralizes rate-limit enforcement,
and ensures all requests pass through a single auditable gateway.

## Technology Constraints

- **Frontend**: Docusaurus deployed to GitHub Pages. The chat widget MUST be a lightweight
  React component embedded in the standard Docusaurus documentation layout. No SSR frameworks.
- **Backend**: Python 3.12+ using FastAPI. No alternative Python web frameworks are permitted.
- **Vector Database**: Qdrant Cloud Free Tier exclusively for vector embeddings.
  No self-hosted Qdrant instances or alternative vector stores.
- **Relational Database**: Neon Serverless Postgres for system metadata and rate-limit tracking.
- **LLM Integration**: OpenAI Agents / ChatKit SDKs handled strictly on the backend.
  No direct browser-side LLM SDK usage.
- **Security & Cost Control**: Because the API is unauthenticated, FastAPI MUST implement
  strict IP-based rate limiting (token-bucket algorithm) to prevent OpenAI API abuse and
  cost overruns. Rate-limit logic MUST be validated before any public deployment.

## Content Quality Standards (Textbook)

- **Structure**: Fixed at exactly 16 chapters (4 modules × 4 chapters). No additions or
  removals are permitted without a constitution amendment.
- **Length & Density**: Total content MUST remain within the 150-page limit. Content MUST be
  high-signal and conceptual. Repetitive filler, redundant introductions, and padded summaries
  are prohibited.
- **Math Constraint**: Zero heavy mathematical derivations are permitted. ROS 2 kinematics,
  physics engines, and VSLAM path planning MUST be explained using system logic and
  architectural concepts only. Equations beyond basic notation are not permitted.
- **Formatting**: All content MUST use strict MDX/Markdown. Code blocks MUST be properly
  tagged with the correct language identifier. Docusaurus admonitions (`:::note`, `:::warning`,
  `:::tip`) MUST be used to break up dense text visually.

## Code Quality Standards (Backend)

- **Type Safety**: Strict type hinting is REQUIRED on all Python functions and parameters.
  Pydantic models MUST be used for all API request and response validation. Untyped function
  signatures are a build violation.
- **Error Handling**: Graceful degradation MUST be implemented. If Qdrant or OpenAI times out
  or returns an error, the FastAPI backend MUST return a clean, structured error response to
  the frontend widget. Raw stack traces MUST NEVER be exposed in API responses.
- **Environment Variables**: All API keys and database URIs (OpenAI, Qdrant, Neon) MUST be
  loaded via `.env` files using a library such as `python-dotenv`. Secrets MUST NEVER be
  committed to version control.

## Workflow Rules

- **Paced Execution**: Code and content MUST NOT be generated in bulk without prior approval.
  The backend plan and table of contents MUST be generated first and approved before any
  implementation begins. Execution then proceeds sequentially.
- **Spec-Driven Consistency**: Any deviation from this constitution MUST be flagged immediately.
  Math constraint violations and missing rate-limiting are never silently ignored.
- **Commit Standards**: A commit MUST be made after each completed chapter or API route.
  Commit message format: `type(scope): description` (e.g., `feat(ch01): add introduction to
  physical AI`, `feat(api): implement /chat rate-limit middleware`).

## Governance

This constitution is the authoritative source of truth for all architectural, content, and
workflow decisions on this project. It supersedes all other practices, conventions, or ad-hoc
agreements.

**Amendment Procedure**: Amendments require (1) a written rationale, (2) explicit identification
of all affected artifacts, and (3) an updated version line. Amendments that remove or redefine
existing principles constitute MAJOR version bumps. New sections or materially expanded guidance
constitute MINOR bumps. Clarifications and wording fixes are PATCH bumps.

**Compliance Review**: All PRs MUST verify compliance with the applicable principles before
merge. Complexity violations MUST be justified in the plan's Complexity Tracking table.

**Version**: 1.0.0 | **Ratified**: 2026-06-13 | **Last Amended**: 2026-06-13

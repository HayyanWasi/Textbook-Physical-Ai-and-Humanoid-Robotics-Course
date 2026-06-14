# Feature Specification: RAG Question-Answering Pipeline

**Feature Branch**: `005-rag-pipeline`  
**Created**: 2026-06-14  
**Status**: Draft  
**Input**: User description: "FastAPI & Qdrant RAG Pipeline (Cohere Integration) — A backend system that ingests textbook MDX chapters, stores them as searchable vectors, and answers student questions by retrieving relevant passages and generating a contextual response. The Docusaurus frontend widget connects to this backend."

---

## Clarifications

### Session 2026-06-14

- Q: How should the OpenAI Agents SDK be integrated into the RAG pipeline's answer-generation step? → A: Agentic retrieval — define a `search_textbook` tool backed by Qdrant; an OpenAI Agents SDK `Agent` (running on Gemini) decides when to call it and synthesizes the answer
- Q: Should embeddings also switch to Gemini, or stay on Cohere? → A: Keep Cohere `embed-v4.0` for embeddings; only the answer-generation Agent runs on Gemini via OpenAI Agents SDK
- Q: How should module-scoping (per-chapter context) work in the new agentic design? → A: `search_textbook` tool accepts an optional `module_num` filter; FastAPI sets it from the request's `context` field, agent always searches within that scope when provided
- Q: Should the Gemini model be configured as a global default for the SDK, or scoped per-agent? → A: Configure a custom `AsyncOpenAI` client pointed at Gemini's OpenAI-compatible endpoint (`https://generativelanguage.googleapis.com/v1beta/openai/`) with `GEMINI_API_KEY`, set as the default model provider for the Agent
- Q: Which Gemini model should the Agent use for answer generation? → A: `gemini-2.5-flash`

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Student Asks a Question and Receives a Contextual Answer (Priority: P1)

A student reading any chapter opens the embedded chatbot widget, types a question (e.g., "What is the difference between Nav2 and MoveIt?"), and within a few seconds receives a written answer that draws on content from the textbook chapters they have been reading.

**Why this priority**: This is the entire value proposition of the feature. Without a working answer flow, everything else is irrelevant.

**Independent Test**: With the backend running and the vector database pre-populated, a student can type a question in the widget and receive a relevant, non-empty answer — no other configuration needed.

**Acceptance Scenarios**:

1. **Given** the vector database is populated with chapter content, **When** a student submits a question via the chatbot widget, **Then** a text answer is displayed within the widget in under 10 seconds.
2. **Given** a student asks a question whose answer spans multiple chapters, **When** the system processes the query, **Then** the returned answer synthesizes information from the most relevant passages rather than quoting a single sentence.
3. **Given** a student submits a completely off-topic question, **When** the system processes it, **Then** the response either redirects to the textbook scope or provides a graceful "not covered here" message rather than crashing.

---

### User Story 2 — Content Administrator Ingests All Textbook Chapters (Priority: P2)

A content administrator (or developer) runs a single ingestion command that reads all MDX chapter files, splits them into retrievable chunks, and populates the vector database — completing without errors or rate-limit crashes.

**Why this priority**: The student query flow cannot work until the knowledge base is populated. This is the prerequisite for Story 1, but it runs once at setup time rather than on every user interaction.

**Independent Test**: After running the ingestion command on a clean database, querying the vector store for any major textbook concept returns at least one matching chunk.

**Acceptance Scenarios**:

1. **Given** all 12 (later 16) chapter MDX files are present, **When** the ingestion command is run, **Then** all chapter text is split into chunks and stored in the vector database without any error or unhandled exception.
2. **Given** the external embedding service enforces rate limits, **When** the ingestion command batches and paces its requests, **Then** the process completes without hitting a rate-limit error, even if it takes longer than an unbatched run.
3. **Given** the ingestion has already been run once, **When** it is run again, **Then** the system either skips existing chunks or replaces them cleanly without duplicating content.
4. **Given** a single MDX file is malformed or empty, **When** the ingestion encounters it, **Then** it logs a warning and continues processing the remaining files rather than aborting the entire run.

---

### User Story 3 — Widget Integrates Transparently into the Reading Experience (Priority: P3)

A student reading a chapter on the Docusaurus site does not need to navigate away or open a separate tool. The chatbot widget is embedded at the bottom of each chapter page and sends questions to the backend without any manual configuration.

**Why this priority**: Discoverability and friction determine whether students actually use the feature. A disconnected or broken widget silently kills adoption.

**Independent Test**: With the backend running locally, a student can ask a question directly from a chapter page and see the answer in the same browser tab — verifiable without inspecting network traffic.

**Acceptance Scenarios**:

1. **Given** the backend is running, **When** a student submits a question from the embedded widget, **Then** the widget displays a loading indicator and then shows the answer — no browser console errors related to the API request.
2. **Given** the backend is not running, **When** a student submits a question, **Then** the widget displays a user-friendly error message rather than an empty state or unhandled exception.
3. **Given** the Docusaurus dev server runs on its standard local port, **When** the widget makes a request to the backend, **Then** no cross-origin errors appear — the backend explicitly allows the frontend's origin.

---

### Edge Cases

- What happens if the vector database is empty when a student submits a question? The backend must return a graceful "knowledge base not yet populated" message rather than a server error.
- What happens if the embedding service is temporarily unavailable during a student query? The backend must return a user-readable error message; the widget must display it without crashing.
- What happens if a student's question is extremely long (> 500 words)? The system must truncate or reject with a clear message rather than submitting an oversized payload.
- What happens when a chapter is updated and re-ingested while the backend is running? The database should accept the new vectors; stale chunks from the same source may persist until an explicit refresh is run (acceptable at this scale).
- What happens if MDX files contain JSX component syntax (e.g., `<RagChatbot />`) in the source? The text extractor must strip or ignore JSX tags rather than including them as chunk text, to avoid polluting search results with component markup.

---

## Requirements *(mandatory)*

### Functional Requirements

**Ingestion Pipeline**

- **FR-001**: The ingestion process MUST read all MDX chapter files from the textbook source directory and extract their plain-text content, stripping JSX tags and markdown formatting artifacts.
- **FR-002**: The ingestion process MUST split each chapter's text into chunks by `##`-level heading boundaries, so each chunk is independently retrievable by topic.
- **FR-003**: The ingestion process MUST batch chunks before sending them to the embedding service, with configurable batch size and inter-batch delay to respect the service's request-rate limits.
- **FR-004**: The ingestion process MUST store each embedded chunk in the vector database with metadata including: source chapter file path, chapter number, module number, and heading title.
- **FR-005**: The ingestion process MUST log progress (chunks processed, batches sent, errors encountered) to standard output so an administrator can monitor the run.
- **FR-006**: The ingestion process MUST complete without crashing due to rate-limit errors when run against Modules 1–3 (12 chapters).

**Query & Answer API**

- **FR-007**: The backend MUST expose a single question-answering endpoint that accepts a plain-text question (and optional module context) as input and returns a structured answer as output.
- **FR-008**: The backend MUST embed the incoming question using Cohere `embed-v4.0` (the same embedding model used during ingestion), then retrieve the top-N most semantically similar chunks from the vector database via a `search_textbook` tool that accepts an optional `module_num` filter derived from the request's `context` field.
- **FR-009**: The backend MUST generate the answer using an OpenAI Agents SDK `Agent` running on Google Gemini (`gemini-2.5-flash`, accessed via a custom `AsyncOpenAI` client pointed at Gemini's OpenAI-compatible endpoint and `GEMINI_API_KEY`). The Agent MUST call the `search_textbook` tool to retrieve context and synthesize a coherent, human-readable answer — not return raw chunk text verbatim.
- **FR-010**: The backend MUST return a structured response containing at minimum: the generated answer text and the source references (chapter title / file path) of the chunks used.
- **FR-011**: The backend MUST return a graceful error response (not a server crash) when the vector database is empty, the embedding service is unavailable, or the input question is malformed.
- **FR-012**: The backend MUST allow requests from the Docusaurus frontend's local development origin without cross-origin errors.

**Frontend Widget**

- **FR-013**: The Docusaurus chatbot widget MUST send the student's question to the backend question-answering endpoint and display the returned answer text in the widget UI.
- **FR-014**: The widget MUST show a loading/pending state while the backend processes the request, so the student knows a response is in progress.
- **FR-015**: The widget MUST display a user-friendly error message if the backend request fails, rather than an empty response or unhandled JavaScript error.

**Configuration**

- **FR-016**: All external service credentials (Cohere embedding API key, Gemini API key, vector database connection details) MUST be supplied via environment variables, not hardcoded in source files.
- **FR-017**: A dependency list MUST be provided so the backend environment can be reproduced with a single install command, including the OpenAI Agents SDK.

### Key Entities

- **Chunk**: A unit of textbook text corresponding to one `##`-level section of a chapter. Attributes: text content, chapter file path, chapter number, module number, heading title, embedding vector.
- **Question**: A natural-language string submitted by a student via the chatbot widget. Attributes: text, optional module context scope.
- **Answer**: The generated response returned to the student. Attributes: answer text, list of source chunk references (chapter path + heading).
- **Batch**: A group of chunks sent to the embedding service in a single API call. Size is configurable to respect rate limits.
- **Vector Database Collection**: The stored set of all embedded chunks, queryable by semantic similarity to an incoming question embedding.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Running the ingestion command against all 12 existing chapters completes without any unhandled error or rate-limit exception, even on the free embedding tier.
- **SC-002**: After ingestion, a student asking "What is ROS 2?" receives an answer that references content from at least one Module 1 chapter — verifiable by checking the source references in the response.
- **SC-003**: Student questions receive a complete answer within 10 seconds under normal local network conditions.
- **SC-004**: The widget displays a visible loading state for the full duration of any request that takes longer than 1 second.
- **SC-005**: Asking 10 representative textbook questions returns relevant, on-topic answers for at least 8 of them (80% relevance rate), validated by a human reviewer spot-check.
- **SC-006**: The backend continues serving requests after encountering a single malformed chapter file during ingestion — the bad file is logged and skipped, not crashing the process.
- **SC-007**: A grep scan of all tracked source files finds zero API keys or connection strings hardcoded in any file.

### Assumptions

- The Cohere Developer Tier provides the embedding endpoint (`embed-v4.0`) used for both ingestion and query-time embedding; text generation is handled separately by an OpenAI Agents SDK Agent running on Gemini (`gemini-2.5-flash`), not Cohere's chat endpoint.
- The Docusaurus frontend already has the `<RagChatbot />` component wired up structurally; this feature only updates its API endpoint configuration (changing it from a placeholder URL to the live backend URL).
- Qdrant will run locally (Docker or native process) for development; no cloud Qdrant account is required for the initial implementation.
- MDX chapter files all live under `frontend/docs/` — the ingestion script discovers them recursively from that root.
- The ingestion command is designed to be run manually by a developer at setup time, not on an automated schedule.
- The endpoint is intentionally unauthenticated; this is acceptable for a local-development / academic-demo context with no sensitive data.
- The backend runs on port 8000 and the Docusaurus dev server runs on port 3000; both are local-only for this implementation.

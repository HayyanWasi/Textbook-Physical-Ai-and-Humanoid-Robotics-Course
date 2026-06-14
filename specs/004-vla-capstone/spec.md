# Feature Specification: Module 4 — Vision-Language-Action (VLA) Capstone

**Feature Branch**: `004-vla-capstone`  
**Created**: 2026-06-14  
**Status**: Draft  
**Input**: User description: "Specification: Vision-Language-Action (VLA) — Module 4 Capstone covering Chapters 13–16 with a three-tier Perception / Cognition / Action architecture, Voice-to-Action via Whisper, LLM cognitive planning with JSON output, and a full capstone project synthesizing all four modules."

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Understand the VLA Architecture (Priority: P1)

A student who has completed Modules 1–3 reads Chapter 13 and can clearly explain why classical robotics pipelines are insufficient for open-ended tasks, and how modern Vision-Language-Action models close that gap by treating perception, cognition, and action as three separable, debuggable tiers.

**Why this priority**: This is the conceptual foundation for the entire module. A student who cannot articulate the three-tier split will misread every subsequent chapter.

**Independent Test**: The chapter stands alone — a student who skips Chapters 14–16 should still be able to pass a short-answer quiz identifying which tier (Perception/Cognition/Action) each system component belongs to.

**Acceptance Scenarios**:

1. **Given** a student has read Chapter 13, **When** asked "where does the LLM's role end in a VLA pipeline?", **Then** they can correctly identify that the LLM produces structured instructions consumed by a separate Action tier, not raw motor commands.
2. **Given** a student reads the chapter's RT-2 / PaLM-E contrast, **When** asked to compare classical robot FSM with a VLA cognitive planner, **Then** they can list at least two advantages (generalization, natural-language interface) and one limitation (latency, compute cost).
3. **Given** a learner opens the chapter sidebar, **When** they navigate to Chapter 13, **Then** the chapter appears under a "Module 4: Vision-Language-Action" sidebar category.

---

### User Story 2 — Trace a Voice Command End-to-End (Priority: P2)

A student reads Chapter 14 and can trace the path of a spoken command — from raw audio bytes, through Whisper's transcription pipeline, to a clean natural-language string handed off to the LLM — without needing to run any code.

**Why this priority**: Voice is the primary human-robot interface in the capstone. Students must understand where ambiguity enters (acoustic noise, homophones) and how it propagates, before they can reason about failure modes in Chapter 16.

**Independent Test**: Given only Chapter 14, a student should be able to draw a block diagram of the audio ingestion pipeline labelling each transformation stage, verifiable against the chapter's own block diagram.

**Acceptance Scenarios**:

1. **Given** a student has read the audio token ingestion section, **When** presented with a noisy audio sample scenario, **Then** they can describe at least two pre-processing steps Whisper applies before generating a transcript.
2. **Given** a student reads the string-parsing subsection, **When** asked what data type exits the Perception tier, **Then** they answer "natural-language string" (not audio bytes, not JSON).
3. **Given** a student accesses Chapter 14 via the RAG chatbot with the query "how does Whisper handle background noise?", **Then** the chatbot surfaces a relevant excerpt from Chapter 14.

---

### User Story 3 — Convert Natural Language to Executable JSON (Priority: P3)

A student reads Chapter 15 and can, given a high-level command ("Clean the room"), manually decompose it into a valid JSON action sequence matching the schema used by the ROS 2 Action Bridge described in Chapter 16.

**Why this priority**: This is the most technically complex step in the pipeline. Students who cannot trace string → structured JSON will be unable to debug the capstone simulation when a command fails.

**Independent Test**: Chapter 15 must contain a worked example: input string → intermediate reasoning steps → final JSON array. A student can reproduce this decomposition for a novel command without reading Chapter 16.

**Acceptance Scenarios**:

1. **Given** a student reads the prompt-engineering section, **When** they design a system prompt for the LLM cognitive planner, **Then** their prompt includes at minimum: a schema definition, a role description, and an output-format constraint.
2. **Given** a student reads the JSON output section, **When** presented with the command "Bring me a glass of water", **Then** they can produce a 3–5 step JSON action array referencing `navigate_to`, `grasp`, and `return_to` primitive skills.
3. **Given** a student sees an invalid JSON output from an LLM, **When** asked how to handle the failure, **Then** they can describe the retry-with-feedback loop shown in the chapter's flowchart.

---

### User Story 4 — Build the Capstone Integration Map (Priority: P4)

A student reads Chapter 16 and can assemble the full system — Whisper → LLM → ROS 2 Bridge → Nav2 / MoveIt / Gazebo — by referencing concepts from all four modules, guided by the capstone's integration map and the embedded Mermaid pipeline diagram.

**Why this priority**: Chapter 16 is the payoff for the entire textbook. It must explicitly anchor each component in a prior module so students see the full learning arc.

**Independent Test**: A student with all four modules read should be able to walk through the Mermaid diagram and name the specific chapter where each node was introduced.

**Acceptance Scenarios**:

1. **Given** a student reads Chapter 16's integration map, **When** they locate the "Nav2 Path Planner" node, **Then** the chapter contains a visible cross-reference to Module 3 / Chapter 12 (Nav2 bipedal planning).
2. **Given** a student reads the simulation setup section, **When** they look for environment configuration, **Then** they find an explicit reference to Module 2's Gazebo / Isaac digital-twin chapters (Chapters 5–8).
3. **Given** a student sees the ROS 2 Action Bridge description, **When** they trace its topic/service contracts, **Then** the chapter references Module 1's ROS 2 nodes and topics chapter (Chapter 2).
4. **Given** a student opens any Chapter 13–16 page, **When** they scroll to the bottom, **Then** the `<RagChatbot context="module-4" />` component is present and scoped to Module 4.

---

### Edge Cases

- What happens if a student accesses the RAG chatbot with a cross-module question (e.g., "How does Nav2 from Module 3 connect to the VLA planner in Module 4")? The chatbot must synthesize answers across modules since `context="module-4"` scopes the primary results but does not exclude cross-references.
- What if the Mermaid diagram in Chapter 16 fails to render (unsupported browser / Docusaurus version mismatch)? The surrounding prose must contain enough textual description that the pipeline is understandable without the diagram.
- What if the sidebars.ts update introduces a conflict with Module 3's existing sidebar entries? Each module's sidebar category must be independently defined so adding Module 4 does not reorder or break existing entries.
- What if a student reads Chapter 16 before Chapters 13–15? Cross-references and a brief recap paragraph at the start of Chapter 16 must make the integration map navigable even in non-linear reading order.

---

## Requirements *(mandatory)*

### Functional Requirements

**Chapter 13 — The VLA Paradigm**

- **FR-001**: Chapter 13 MUST explain the limitations of classical isolated-loop robotics pipelines (perception → planning → control as disconnected programs) using a concrete failure scenario.
- **FR-002**: Chapter 13 MUST introduce the three-tier VLA architecture — Perception (Whisper/Vision), Cognition (LLM state machine), Action (ROS 2 primitives library) — as separable, independently debuggable tiers.
- **FR-003**: Chapter 13 MUST contrast at least two embodied foundation models (e.g., RT-2, PaLM-E) to illustrate how the field has converged on multi-modal LLM-driven control.
- **FR-004**: Chapter 13 MUST include a visual or textual diagram showing the three-tier boundary, clearly marking where string data crosses each tier boundary.

**Chapter 14 — Voice-to-Action**

- **FR-005**: Chapter 14 MUST describe the audio streaming and tokenization pipeline of a Whisper-class model conceptually, without requiring students to run inference.
- **FR-006**: Chapter 14 MUST explain how raw audio is transformed into a natural-language string, naming each processing stage (audio chunking, spectrogram, token decoding).
- **FR-007**: Chapter 14 MUST identify at least two failure modes in the Perception tier (background noise, homophone ambiguity) and describe how downstream tiers detect and recover from them.

**Chapter 15 — Cognitive LLM Planning**

- **FR-008**: Chapter 15 MUST teach prompt engineering for structured output, including: role definition, schema injection, and output-format constraints, using a concrete worked example.
- **FR-009**: Chapter 15 MUST show — via a text-based flowchart — how a high-level command string is decomposed into an ordered JSON array of primitive skill invocations.
- **FR-010**: Chapter 15 MUST define a minimal JSON action schema (fields: `skill`, `target`, `parameters`) usable by the ROS 2 Action Bridge in Chapter 16.
- **FR-011**: Chapter 15 MUST include a retry-with-feedback loop description: what to do when the LLM emits malformed or out-of-schema JSON.

**Chapter 16 — Capstone: Autonomous Humanoid**

- **FR-012**: Chapter 16 MUST embed the Mermaid pipeline diagram showing: Voice → Whisper → LLM → ROS 2 Bridge → Nav2 / Motor, with the Vision input feeding into the LLM node.
- **FR-013**: Chapter 16 MUST contain explicit cross-references to prior modules: Module 1 (ROS 2 topics, Chapter 2), Module 2 (Gazebo/Isaac simulation config, Chapters 5–8), Module 3 (Nav2 bipedal path planning, Chapter 12).
- **FR-014**: Chapter 16 MUST present a step-by-step capstone blueprint — a numbered assembly sequence a student can follow to understand how all four subsystems are wired together in the simulated environment.
- **FR-015**: Chapter 16 MUST describe the ROS 2 Action Bridge interface: how the JSON action array is consumed, how each skill maps to a Nav2 goal or MoveIt trajectory, and how feedback is returned to the LLM for replanning.

**Sidebar & Integration**

- **FR-016**: `frontend/sidebars.ts` MUST be updated to add a "Module 4: Vision-Language-Action" category containing all four chapter entries in order (Chapters 13–16), without altering existing Module 1–3 entries.
- **FR-017**: The `<RagChatbot context="module-4" />` component MUST be appended at the end of each of the four chapter MDX files.
- **FR-018**: All four chapter files MUST be placed at `frontend/docs/module-4/chapter-{13,14,15,16}-*.mdx` to match the established naming convention.

### Key Entities

- **Chapter**: A self-contained educational document (MDX file) within a module, teaching one major concept. Attributes: title, chapter number, module number, cross-references, RagChatbot context tag.
- **Tier**: One of Perception, Cognition, or Action. Defines a processing boundary in the VLA architecture where data type changes (audio → string → JSON → ROS 2 actions).
- **Primitive Skill**: An atomic, reusable robot capability (e.g., `navigate_to`, `grasp`, `place`) referenced by name in the JSON action schema and executed by the ROS 2 Action Bridge.
- **Action JSON Array**: The structured output of the LLM cognitive planner — an ordered list of primitive skill invocations with target and parameters fields.
- **RagChatbot Widget**: A React component (`<RagChatbot context="..." />`) embedded at the chapter foot, scoping the chatbot's retrieval to the declared module context.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All four chapter files exist at the correct paths under `frontend/docs/module-4/` and render without errors in the Docusaurus build.
- **SC-002**: A student reading Chapter 13 can correctly assign every component in the Part 5 Mermaid diagram to one of the three tiers (Perception / Cognition / Action) — verifiable by a 5-question matching exercise embedded or referenced in the chapter.
- **SC-003**: A student can, after reading Chapter 15, produce a valid JSON action array for a novel command without referring to other chapters — measured by the worked example being fully self-contained within Chapter 15.
- **SC-004**: Chapter 16 contains at least three numbered cross-references to prior modules (one per module, Modules 1–3), verifiable by manual inspection of the markdown source.
- **SC-005**: The `frontend/sidebars.ts` update introduces a Module 4 category with exactly four entries and does not alter the ordering or labels of the existing Module 1–3 sidebar entries.
- **SC-006**: The RAG chatbot, when queried with "What is the VLA three-tier architecture?", returns a relevant excerpt sourced from Module 4 content, confirming the `context="module-4"` scope is correctly wired.
- **SC-007**: All four chapter MDX files end with the `<RagChatbot context="module-4" />` component — verifiable by string search across the four files.

### Assumptions

- The `<RagChatbot />` component is already implemented in the frontend codebase (from prior modules); this feature only adds the `context="module-4"` instance.
- The Docusaurus build pipeline already supports Mermaid diagram rendering (enabled in prior modules).
- Cross-references are text-based links (relative MDX links or bolded chapter names), not code imports.
- The JSON action schema defined in Chapter 15 is illustrative/conceptual; no actual ROS 2 code needs to be implemented within this feature.
- Chapter 16's "step-by-step capstone blueprint" is an architectural walkthrough narrative, not a runnable code tutorial.

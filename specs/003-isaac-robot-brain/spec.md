# Feature Specification: Module 3 — The AI-Robot Brain (NVIDIA Isaac™)

**Feature Branch**: `003-isaac-robot-brain`
**Created**: 2026-06-14
**Status**: Draft
**Input**: User description: "The AI-Robot Brain (NVIDIA Isaac™)"

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Read Chapter 9: Why Standard Sensors Are Not Enough (Priority: P1)

A student who has completed Modules 1 and 2 opens Chapter 9 and learns why the sensors
used in basic robotics — simple cameras, ultrasonic rangefinders, basic IMUs — are
fundamentally insufficient for the perception demands of autonomous humanoid robots.
They leave the chapter with a clear mental model of NVIDIA Isaac as an integrated
ecosystem: the "Visual Cortex" that sits on top of the ROS 2 communication layer they
already understand.

**Why this priority**: This is the conceptual gateway for the entire module. Without
understanding the perception gap, students have no motivational anchor for why Isaac Sim,
Isaac ROS, or Nav2 exist. A student who reads only this chapter still walks away with a
transferable insight about the limits of naive sensing.

**Independent Test**: A student can open Chapter 9 without reading Chapters 10–12 and
correctly explain to a peer: "Here is the sensing problem humanoid robots face, and here
is the family of tools NVIDIA built to solve it." The explanation requires no equations
or hardware knowledge.

**Acceptance Scenarios**:

1. **Given** a student has completed Modules 1 and 2, **When** they read Chapter 9,
   **Then** they can articulate the difference between a proximity sensor and a
   perception system without referencing GPU specs or driver code.
2. **Given** the chapter is rendered in the textbook, **When** a reviewer inspects it,
   **Then** no CUDA code, tensor operations, or kernel configurations appear anywhere.
3. **Given** the RAG knowledge base processes the chapter, **When** it splits on `##`
   headings, **Then** each chunk maps to exactly one perception concept with no
   ambiguous overlap into simulation or navigation topics.

---

### User Story 2 — Read Chapter 10: Simulation as a Training Ground (Priority: P2)

A student reads Chapter 10 and builds a clear mental model of the distinction between
Gazebo (physics simulation for testing robot behavior) and Isaac Sim (photorealistic
simulation for training AI perception models). They understand the "sim-to-real gap"
problem and how synthetic data bridges it — all without examining a single line of
rendering configuration.

**Why this priority**: This is the pivotal conceptual differentiation that prevents
students from conflating Module 2's content with Module 3's content. P2 because it
depends on the framing established in Chapter 9.

**Independent Test**: A student who has read only Chapters 9 and 10 can correctly
answer: "If I want to teach my robot to recognize a chair in any lighting condition,
which simulator do I use and why?" without consulting external material.

**Acceptance Scenarios**:

1. **Given** a student reads Chapter 10, **When** asked to compare Gazebo and Isaac Sim,
   **Then** they can state the functional distinction (behavior testing vs. perception
   training) using the textbook's own framing, without referencing rendering APIs.
2. **Given** the chapter is rendered, **When** a reviewer checks it, **Then** a
   side-by-side comparison of Gazebo's role versus Isaac Sim's role appears in at least
   one clearly marked section.
3. **Given** the RAG chatbot receives a query about "synthetic data," **When** it
   retrieves the Chapter 10 chunk, **Then** the answer is self-contained and does not
   bleed into VSLAM or Nav2 concepts.

---

### User Story 3 — Read Chapter 11: How a Robot Builds a Map (Priority: P3)

A student reads Chapter 11 and understands Visual SLAM — the process by which a robot
simultaneously builds a map of its environment and tracks its own position within it —
entirely through conceptual analogies. They grasp the core insight (cameras as the
primary sensor, visual landmarks as reference points) without encountering a single
matrix equation or covariance formula.

**Why this priority**: This is the hardest conceptual leap in the module. P3 because it
builds directly on the perception foundation of Chapter 9 and the simulation context of
Chapter 10.

**Independent Test**: A student who has never studied linear algebra can read Chapter 11
and correctly describe the VSLAM process using an analogy of their own construction
(not borrowed from the text). If they can generate a novel analogy, the abstraction
succeeded.

**Acceptance Scenarios**:

1. **Given** a student reads Chapter 11, **When** asked "how does the robot know where
   it is?", **Then** they can explain the concept of visual landmarks and loop closure
   in plain language with no reference to matrices, Jacobians, or covariance.
2. **Given** the chapter is rendered, **When** a technical reviewer inspects it,
   **Then** no mathematical derivations, matrix notation, or algorithm pseudocode appear
   anywhere in the file.
3. **Given** the RAG knowledge base ingests the chapter, **When** a query about "robot
   localization" arrives, **Then** the retrieved chunk cleanly separates mapping
   concepts from navigation/planning concepts based on `##` heading boundaries.

---

### User Story 4 — Read Chapter 12: Moving a Two-Legged Robot Without It Falling (Priority: P4)

A student reads Chapter 12 and understands the unique planning challenges of bipedal
humanoid navigation — why a path-planning algorithm designed for a wheeled robot is
dangerous when applied to a two-legged one — and how Nav2 addresses stability, terrain
assessment, and gait-aware routing. They leave with a conceptual model of the full
Isaac-to-Nav2 pipeline.

**Why this priority**: This is the synthesis chapter. P4 because it requires the
perception and mapping understanding from all prior chapters to make sense of the
planning decisions.

**Independent Test**: A student can read Chapter 12 and construct a verbal walkthrough
of the complete pipeline from "the robot's cameras detect an obstacle" to "the robot
decides to step over rather than around it," citing the roles of Isaac ROS and Nav2
without assistance.

**Acceptance Scenarios**:

1. **Given** a student reads Chapter 12, **When** asked why wheeled navigation
   algorithms fail for bipedal robots, **Then** they can articulate at least two
   structural reasons (e.g., center-of-mass dynamics, footstep discretization) in plain
   language.
2. **Given** the chapter is rendered, **When** a reviewer inspects it, **Then** the
   Nav2 explanation explicitly references the robot's need to maintain balance as a
   first-class planning constraint, not an afterthought.
3. **Given** all four chapters are published, **When** a student reads them in sequence,
   **Then** they can trace the complete conceptual pipeline: sensor gap → perception
   training → map building → movement decision.

---

### Edge Cases

- What happens when a student arrives at Chapter 9 without completing Module 2? Each
  chapter must be readable in isolation, with a brief callout box noting prerequisite
  concepts rather than assuming the reader has prior context.
- What if the RAG chatbot receives a cross-module question spanning Module 2 (Gazebo)
  and Module 3 (Isaac Sim)? The module-3 context attribute must not suppress retrieval
  from other modules; the chatbot must handle cross-boundary queries gracefully.
- What if a student asks about CUDA or GPU optimization? The chatbot's module-3 context
  should redirect to conceptual explanations rather than surface hardware-level content
  that was intentionally excluded from the chapters.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The textbook MUST display four new navigable chapter pages under a
  "Module 3: The AI-Robot Brain" grouping in the sidebar.
- **FR-002**: Each chapter MUST be readable as a standalone unit, including a brief
  prerequisite callout that names which prior module concepts are assumed.
- **FR-003**: Chapter 10 MUST contain an explicit, clearly labeled section comparing
  Gazebo (physics simulation / behavior testing) against Isaac Sim (photorealistic
  simulation / perception training) so a reader cannot confuse their roles.
- **FR-004**: Chapter 11 MUST explain Visual SLAM exclusively through conceptual
  analogies and diagrams — zero matrix notation, pseudocode, or algorithm derivations
  are permitted.
- **FR-005**: Chapter 12 MUST distinguish bipedal path planning from wheeled path
  planning by addressing balance constraints and footstep-aware routing as distinct
  requirements.
- **FR-006**: Every chapter MUST include an interactive AI assistant component
  pre-configured to answer questions scoped to Module 3 content.
- **FR-007**: All heading levels MUST follow a strict hierarchy (`##` for major
  concepts, `###` for sub-concepts) to ensure reliable semantic chunking for the
  knowledge retrieval system.
- **FR-008**: No chapter MUST reference GPU architecture internals, CUDA programming,
  matrix algebra, or hardware-level optimization.
- **FR-009**: Chapter 9 MUST introduce all four tools (Isaac Sim, Isaac ROS, Isaac Lab,
  Nav2) at a conceptual level so students understand the ecosystem before diving into
  individual chapters.

### Key Entities

- **Module 3 Chapter**: A self-contained textbook page covering one conceptual area
  (perception, simulation, VSLAM, or navigation), rendered in the site as a navigable
  document with prerequisite callouts and an embedded AI assistant.
- **Gazebo vs. Isaac Sim Comparison**: A structured side-by-side explanation of the two
  simulation environments, present in Chapter 10, serving as the primary disambiguation
  artifact for students crossing from Module 2 to Module 3.
- **RAG Context Attribute**: The `module-3` tag embedded in the AI assistant component
  on each chapter page, used by the retrieval system to scope knowledge base searches
  to Module 3 content.
- **VSLAM Conceptual Model**: The set of analogies and diagrams in Chapter 11 that
  stand in for mathematical derivations, representing the core pedagogical artifact of
  that chapter.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: After reading Chapter 10, at least 90% of students can correctly
  distinguish Gazebo's purpose from Isaac Sim's purpose in a post-chapter comprehension
  check (two-sentence written response or multiple-choice question).
- **SC-002**: All four Module 3 chapters appear in the textbook sidebar under a single
  "Module 3" group, navigable within two clicks from any other module.
- **SC-003**: A student with no GPU or CUDA background can read all four chapters
  without encountering any term that requires hardware-specific prerequisite knowledge
  to understand.
- **SC-004**: The AI assistant on each chapter page responds to at least five distinct
  conceptual questions about that chapter's topic without returning hardware-specific or
  mathematically dense answers.
- **SC-005**: The knowledge retrieval system can return semantically distinct, non-
  overlapping results for the query pairs: ("Gazebo" vs. "Isaac Sim"), ("mapping" vs.
  "path planning"), and ("perception" vs. "navigation").
- **SC-006**: After completing all four chapters, a student can verbally trace the
  complete pipeline — from camera input, through perception model, through map
  construction, to movement decision — in under three minutes with no reference
  material.

## Assumptions

- Students have completed Module 1 (ROS 2 architecture) and Module 2 (Gazebo physics
  simulation) before arriving at Module 3. Chapter prerequisite callouts will reinforce
  but not re-teach these concepts.
- The AI assistant component (`<RagChatbot>`) is already implemented and accepts a
  `context` attribute that scopes its knowledge retrieval. Module 3 chapters need only
  set `context="module-3"` to activate correct scoping.
- The Qdrant chunking pipeline ingests documents by splitting on `##` headings.
  Chapters that follow the `##`/`###` heading hierarchy will chunk correctly without
  additional configuration.
- The textbook sidebar is configured via a single `sidebars.js` file, and adding a
  Module 3 category there is sufficient to surface all four chapters in navigation.
- Chapter density is bounded at approximately 2,000–3,000 words per chapter to stay
  within the "~10 pages" constraint and maintain high-signal prose.

## Dependencies

- Module 1 spec (`001-ros2-nervous-system`) — conceptual ROS 2 vocabulary referenced in
  Chapter 9 (nodes, topics, messages).
- Module 2 spec (`002-digital-twin`) — Gazebo simulation concepts that Chapter 10 must
  contrast against Isaac Sim.
- Existing Docusaurus sidebar configuration (`sidebars.js`) — must be extended, not
  replaced, to preserve Module 1 and Module 2 navigation.
- RAG chatbot component — must be deployed and functional before Module 3 pages can be
  verified end-to-end.

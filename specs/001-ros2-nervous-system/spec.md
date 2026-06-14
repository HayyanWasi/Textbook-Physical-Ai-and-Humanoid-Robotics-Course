# Feature Specification: Module 1 — The Robotic Nervous System (ROS 2)

**Feature Branch**: `001-ros2-nervous-system`
**Created**: 2026-06-13
**Status**: Draft
**Input**: User description: "The Robotic Nervous System (ROS 2)"

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Read Chapter 1: Why Robots Need a Middleware (Priority: P1)

A student with basic Python knowledge but no robotics background opens Chapter 1 and learns
why hardware-to-software decoupling is necessary. They understand the problem that ROS 2 solves
before encountering any tooling or syntax. They leave the chapter able to explain the role
of middleware to someone else using a non-technical analogy.

**Why this priority**: This is the conceptual foundation. Without it, Chapters 2–4 have no
motivational anchor. It is the MVP — a student who reads only this chapter still gains
transferable insight.

**Independent Test**: A reader can open the rendered Docusaurus page, read it without any
additional context, and answer: "Why can't software talk directly to a robotic arm's motor
driver?" If they can, the chapter succeeds independently.

**Acceptance Scenarios**:

1. **Given** a student opens `chapter-1-middleware.mdx` in Docusaurus, **When** they read
   to the end, **Then** they can articulate the hardware-abstraction problem in plain language
   without referencing any code or equations.
2. **Given** the chapter is rendered, **When** a reviewer checks it, **Then** every key concept
   is highlighted using a Docusaurus admonition (`:::note`, `:::warning`, or `:::tip`).
3. **Given** the RAG chunking script processes the file, **When** it splits on `##` headings,
   **Then** each chunk maps to exactly one semantic concept with no ambiguous bleed-over.

---

### User Story 2 — Read Chapter 2: Nodes, Topics, and Services (Priority: P2)

A student reads Chapter 2 and builds a clear mental model of the publish-subscribe architecture.
They can distinguish between Topics (one-way data streams) and Services (request-response calls)
and understand when each is appropriate. The biological "Nervous System" analogy introduced
in Chapter 1 is extended here — Nodes become organs, Topics become neural pathways.

**Why this priority**: This is the architectural core of ROS 2. All subsequent chapters
(rclpy integration, URDF) assume the student already understands the graph of communicating
nodes. P2 because it depends on P1's framing.

**Independent Test**: A student who has read only Chapters 1 and 2 can sketch a diagram showing
two Nodes communicating over a Topic and label the publisher, subscriber, and message type.

**Acceptance Scenarios**:

1. **Given** a student reads Chapter 2, **When** asked to contrast Topics vs. Services,
   **Then** they can state the use-case difference using the textbook's own bullet-point
   comparison without consulting external sources.
2. **Given** the chapter is rendered, **When** a reviewer inspects it, **Then** no kinematic
   math or C++ code appears anywhere in the file.
3. **Given** the RAG chatbot receives a query about "what is a ROS 2 topic," **When** it
   retrieves the chapter-2 chunk, **Then** the answer is self-contained within that chunk.

---

### User Story 3 — Read Chapter 3: Connecting the AI Brain with rclpy (Priority: P3)

A student reads Chapter 3 and understands how Python (via the `rclpy` library) acts as the
bridge between an AI decision engine and the ROS 2 graph. They see conceptual code blocks
showing the structure of a minimal publisher and subscriber node — no boilerplate or workspace
compilation steps required.

**Why this priority**: Builds directly on Chapter 2's graph model. Students must understand
the communications layer before seeing how Python plugs into it.

**Independent Test**: A student can read the conceptual Python logic blocks and explain
what each labeled section does (node initialization, topic subscription, callback function)
without needing to run the code.

**Acceptance Scenarios**:

1. **Given** a student reads Chapter 3, **When** they examine the code blocks, **Then** every
   block has a language tag (`python`) and inline comments explaining architectural intent,
   not syntax.
2. **Given** the chapter is rendered, **When** a reviewer checks it, **Then** no `colcon build`
   commands, workspace setup steps, or C++ snippets are present.
3. **Given** the RAG chatbot receives a query about "how does Python connect to ROS 2,"
   **Then** the retrieved chunk explains the rclpy bridge conceptually without referencing
   installation procedures.

---

### User Story 4 — Read Chapter 4: Defining the Physical Form with URDF (Priority: P4)

A student reads Chapter 4 and understands what URDF (Unified Robot Description Format) is
and how it separates a robot's visual representation from its collision model. They can
identify the purpose of `<visual>`, `<collision>`, and `<inertial>` XML tags without deriving
any physics equations.

**Why this priority**: This chapter completes Module 1. It can be read after Chapter 2 and 3
but is the least foundational — a student could understand the rest of the textbook without it.

**Independent Test**: A student can read a sample URDF snippet and explain why a robot needs
both a visual mesh and a separate collision mesh, without referencing dynamics equations.

**Acceptance Scenarios**:

1. **Given** a student reads Chapter 4, **When** they examine the XML snippets, **Then** they
   can distinguish the role of each tag (`<link>`, `<joint>`, `<visual>`, `<collision>`)
   from the surrounding prose alone.
2. **Given** the chapter is rendered, **When** a reviewer checks it, **Then** no moment of
   inertia tensors, Denavit-Hartenberg parameters, or kinematic chain derivations appear.
3. **Given** the Docusaurus sidebar is updated, **When** a user navigates to Module 1,
   **Then** Chapter 4 is listed and links correctly to the rendered page.

---

### User Story 5 — RAG Chatbot Widget Embedded on All Four Pages (Priority: P5)

A student reading any of the four chapters can open the embedded RAG chatbot widget and ask
a question about the content they are currently reading. The widget passes the correct
`context` prop so that the backend scopes its Qdrant retrieval to Module 1 only.

**Why this priority**: This is a cross-cutting integration concern. The pages deliver value
without the widget; the widget enhances but does not gate comprehension.

**Independent Test**: On any of the four chapter pages, the `<RagChatbot context="module-1" />`
component renders visibly. A reviewer can confirm the correct `context` prop is passed by
inspecting the MDX source of each file.

**Acceptance Scenarios**:

1. **Given** any of the four `.mdx` files is rendered, **When** a reviewer inspects its
   source, **Then** the line `<RagChatbot context="module-1" />` appears exactly once
   at the bottom of each file.
2. **Given** the `sidebars.js` is updated, **When** Docusaurus builds, **Then** all four
   chapter links appear under a "Module 1: The Robotic Nervous System" category with no
   broken links.

---

### Edge Cases

- What happens when a student navigates directly to a chapter URL without going through the
  sidebar? The page MUST render correctly as a standalone document with no broken internal links.
- What happens if the `<RagChatbot>` component is not yet implemented when the MDX files are
  written? The component MUST be included as a placeholder import; the build MUST NOT fail due
  to its absence if the component file does not yet exist (use a conditional import or stub).
- What happens if a heading inside a chapter is vague (e.g., "Introduction")? All `##` headings
  MUST include the chapter topic as a qualifier (e.g., "## Introduction to Middleware") so that
  RAG chunks are unambiguously identifiable.
- What happens if content exceeds the 10-page density limit per chapter? A chapter review gate
  MUST flag this; excess content is removed, not summarized into a new section.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST produce four MDX files at the paths specified:
  `docs/module-1/chapter-1-middleware.mdx`, `docs/module-1/chapter-2-nodes-topics.mdx`,
  `docs/module-1/chapter-3-rclpy.mdx`, `docs/module-1/chapter-4-urdf.mdx`.
- **FR-002**: Every chapter file MUST begin with a "Learning Objectives" section listing
  3–5 concrete, testable things the reader will understand after completing the chapter.
- **FR-003**: Every chapter MUST use Docusaurus admonitions (`:::note`, `:::tip`, `:::warning`)
  at least once to visually separate a key concept from surrounding prose.
- **FR-004**: All `##` and `###` headings MUST be descriptive enough that a RAG chunking
  script can identify their topic without reading surrounding text.
- **FR-005**: No chapter MUST contain heavy mathematical derivations; kinematics, physics
  engines, and path planning MUST be explained using system logic and data-flow descriptions only.
- **FR-006**: Every chapter MUST embed `<RagChatbot context="module-1" />` exactly once,
  at the bottom of the file, after all prose content.
- **FR-007**: All code blocks MUST carry a language tag (e.g., ` ```python `, ` ```xml `);
  untagged code blocks are prohibited.
- **FR-008**: `sidebars.js` MUST be updated to include all four chapters under a top-level
  "Module 1: The Robotic Nervous System" category.
- **FR-009**: The local Docusaurus build MUST complete without errors or broken-link warnings
  for any of the four new pages after all files are written.

### Key Entities

- **Chapter**: A single `.mdx` file covering one conceptual topic. Attributes: title,
  learning objectives, section headings (`##`), admonitions, code blocks (tagged), RAG widget.
- **Module**: A group of four chapters sharing a top-level sidebar category. Module 1 contains
  Chapters 1–4.
- **RAG Context Scope**: The `context` prop value (`"module-1"`) used by the chat widget to
  restrict Qdrant retrieval to the current module's vector embeddings only.
- **Heading Chunk**: A semantic unit produced by the RAG chunking script, bounded by `##`
  headings. Each chunk MUST correspond to exactly one concept.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A reader with basic Python knowledge and zero robotics experience can describe
  the ROS 2 publish-subscribe model correctly after reading Chapters 1 and 2 — verified by
  a peer comprehension check (no tools required).
- **SC-002**: All four chapter pages render without errors in a local Docusaurus build; zero
  broken links reported.
- **SC-003**: The `<RagChatbot context="module-1" />` component is present and the correct
  `context` prop is verifiable by source inspection on all four pages.
- **SC-004**: The RAG chunking script produces at least 3 distinct, non-overlapping semantic
  chunks per chapter from the `##` heading structure.
- **SC-005**: No chapter exceeds the equivalent of 10 dense pages of content (approximately
  3,000–3,500 words); measured by word count before publishing.
- **SC-006**: Zero mathematical derivations, kinematic equations, or physics formulas appear
  in any of the four chapters — verified by a manual review pass before merge.
- **SC-007**: The Module 1 sidebar category is visible and all four chapter links are
  functional in the local Docusaurus navigation.

## Assumptions

- The `<RagChatbot>` React component exists or will exist at the time of Docusaurus build;
  if not yet implemented, a stub component at `src/components/RagChatbot.jsx` MUST be created
  to prevent build failures.
- `sidebars.js` follows the standard Docusaurus autogenerated or manual sidebar format;
  no non-standard sidebar plugin is assumed.
- The Qdrant chunking script uses `##` headings as split boundaries; this assumption is baked
  into the heading-density requirement (FR-004).
- Chapter content density of "10 pages" is operationalized as ≤3,500 words per chapter file.

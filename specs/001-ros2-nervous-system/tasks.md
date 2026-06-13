---
description: "Task list for Module 1 — The Robotic Nervous System (ROS 2)"
---

# Tasks: Module 1 — The Robotic Nervous System (ROS 2)

**Input**: Design documents from `/specs/001-ros2-nervous-system/`
**Prerequisites**: plan.md ✅ | spec.md ✅ | research.md ✅ | data-model.md ✅ | contracts/content-contract.md ✅

**Tests**: No test tasks — content feature validated by build check and manual review (not explicitly requested in spec).

**Organization**: Tasks grouped by user story (P1 → P5) to enable independent chapter authoring and validation.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1–US5)
- Exact file paths included in every task description

## Path Conventions

- Content: `docs/module-1/`
- Widget stub: `src/components/RagChatbot.jsx`
- Sidebar: `sidebars.js` (repo root)

---

## Phase 1: Setup

**Purpose**: Create the directory structure required before any content can be written.

- [x] T001 Create directory `docs/module-1/` at repository root
- [x] T002 Create `src/components/RagChatbot.jsx` stub — zero-dependency placeholder that renders a visible `[RAG Chatbot — backend integration pending]` div; MUST NOT throw; required before any `npm run build` can succeed

**Checkpoint**: `docs/module-1/` exists and `src/components/RagChatbot.jsx` is present with a valid default export.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared infrastructure that must exist before any chapter can be validated via build.

**⚠️ CRITICAL**: No chapter build verification can pass until this phase is complete.

- [x] T003 Verify `.gitignore` exists at repo root; if missing, create it with Node.js/Docusaurus patterns: `node_modules/`, `build/`, `.docusaurus/`, `.cache-loader/`, `*.log`, `.env*`, `.DS_Store`

**Checkpoint**: `.gitignore` present; RagChatbot stub confirmed importable.

---

## Phase 3: User Story 1 — Chapter 1: The Need for Robotic Middleware (Priority: P1) 🎯 MVP

**Goal**: Deliver a fully renderable Chapter 1 that explains hardware-to-software decoupling using the "robot as a city" analogy, with zero math.

**Independent Test**: Open `docs/module-1/chapter-1-middleware.mdx` in a local Docusaurus build. A reader with Python knowledge but no robotics experience can answer "Why can't software talk directly to a robotic arm's motor driver?" after reading it.

### Implementation for User Story 1

- [x] T004 [US1] Write `docs/module-1/chapter-1-middleware.mdx` with the following structure and content:
  - **Frontmatter**: `title: "Chapter 1 — The Need for Robotic Middleware"`
  - **H1**: `# Chapter 1 — The Need for Robotic Middleware`
  - **`## Learning Objectives`** (first H2): 4 bullet points — (1) explain why direct hardware control fails at scale, (2) define middleware in the context of robotics, (3) describe what ROS 2 provides as a middleware layer, (4) articulate the hardware abstraction benefit using a non-technical analogy
  - **`## Why Direct Hardware Control Fails in Robotics`**: Explain that every hardware vendor (motor, sensor, camera) speaks a different protocol. Without a unifying layer, software must be rewritten for every device swap. Analogy: imagine a city where every road uses a different vehicle standard — a bus can't drive on a bicycle lane.
  - **`## The Hardware Abstraction Layer`**: Define the HAL concept. ROS 2 sits between hardware drivers and application logic, exposing a uniform interface. :::note admonition: "Swapping a sensor in ROS 2 only requires updating its driver node — the rest of the system is unaware of the change."
  - **`## How ROS 2 Works as Robotic Middleware`**: Describe ROS 2 as the "city road network" — it doesn't build the buildings (hardware) or run the shops (AI logic), it provides the infrastructure for them to communicate. Key role: message passing, process isolation, hardware-agnostic communication.
  - **`## The DDS Transport System`**: Explain DDS (Data Distribution Service) as the underlying protocol ROS 2 uses — a publish-subscribe messaging standard. :::tip admonition: "You don't need to configure DDS directly. ROS 2 handles transport automatically — think of it as the city's underground plumbing." Do NOT derive any DDS mathematics.
  - **`## Summary`** (last H2): 4-sentence recap covering: direct control failure → HAL concept → ROS 2 as infrastructure → DDS as transport.
  - **Widget**: `<RagChatbot context="module-1" />` as the very last line after Summary
  - **Constraint**: ≤3,500 prose words; zero equations; all H2s are self-describing

**Checkpoint**: Chapter 1 renders in Docusaurus; all H2 headings are topic-qualified; at least 2 admonitions present; no math content.

---

## Phase 4: User Story 2 — Chapter 2: Nodes, Topics, and Services (Priority: P2)

**Goal**: Deliver a fully renderable Chapter 2 that teaches the ROS 2 publish-subscribe graph using the "Nervous System" analogy, with a clear bullet-point comparison of Topics vs. Services.

**Independent Test**: A student who has read only Chapters 1 and 2 can sketch two Nodes communicating over a Topic and label the publisher, subscriber, and message type.

### Implementation for User Story 2

- [x] T005 [US2] Write `docs/module-1/chapter-2-nodes-topics.mdx` with the following structure and content:
  - **Frontmatter**: `title: "Chapter 2 — Nodes, Topics, and Services"`
  - **H1**: `# Chapter 2 — Nodes, Topics, and Services`
  - **`## Learning Objectives`**: 4 bullets — (1) define a ROS 2 Node using the organ analogy, (2) explain how Topics enable one-way data streaming, (3) explain how Services enable request-response communication, (4) choose between a Topic and a Service for a given scenario
  - **`## The ROS 2 Computation Graph`**: Describe the graph as a network of Nodes connected by Topics and Services. Analogy: the nervous system — the graph is the body's neural network. :::note: "In ROS 2, you never call a hardware driver directly. You send messages through the graph."
  - **`## Nodes as Processing Organs`**: Each Node is a single-purpose process (e.g., camera driver, object detector, motor controller). Nodes are independent — they start, stop, and fail without crashing the whole system. Analogy: organs can be transplanted; the body adapts.
  - **`## Topics as Neural Pathways`**: Topics are named, typed channels. A publisher Node sends messages to a Topic; any number of subscriber Nodes can receive them. One-way, asynchronous. Example topic names: `/camera/image`, `/lidar/scan`, `/cmd_vel`. :::tip: "Topics are fire-and-forget. The publisher doesn't know or care who is listening."
  - **`## Services as Request-Response Reflexes`**: Services are synchronous: one Node sends a request, waits for a response. Analogy: a reflex arc — stimulus in, response out. Use for: configuration queries, one-shot actions, status checks.
  - **`## Choosing Between Topics and Services`**: Bullet-point comparison table in prose:
    - Use a **Topic** when: data flows continuously (sensor streams, odometry), multiple consumers exist, the sender doesn't need confirmation
    - Use a **Service** when: a discrete action must complete before proceeding, a single response is expected, the interaction is request-reply in nature
    - :::warning: "A common mistake is using a Service for high-frequency sensor data. This blocks the caller and degrades system performance."
  - **`## Summary`**: 4-sentence recap: graph concept → Nodes as organs → Topics as pathways → Services as reflexes.
  - **Widget**: `<RagChatbot context="module-1" />` as last line
  - **Constraint**: ≤3,500 prose words; no C++ code; no kinematic math; all H2s self-describing

**Checkpoint**: Chapter 2 renders; Topics vs. Services comparison is clear without referencing any math; H2 headings are RAG-chunk-ready.

---

## Phase 5: User Story 3 — Chapter 3: Connecting the AI Brain with rclpy (Priority: P3)

**Goal**: Deliver a fully renderable Chapter 3 that explains how Python's `rclpy` library bridges AI decision logic to the ROS 2 graph, using conceptual code blocks (no workspace setup, no colcon).

**Independent Test**: A student can read the conceptual Python blocks and explain what each labeled section does — node initialization, topic subscription, callback — without needing to run the code.

### Implementation for User Story 3

- [x] T006 [US3] Write `docs/module-1/chapter-3-rclpy.mdx` with the following structure and content:
  - **Frontmatter**: `title: "Chapter 3 — Connecting the AI Brain with rclpy"`
  - **H1**: `# Chapter 3 — Connecting the AI Brain with rclpy`
  - **`## Learning Objectives`**: 4 bullets — (1) explain what rclpy is and why Python is used for AI-ROS integration, (2) identify the three structural parts of a ROS 2 Node in Python, (3) describe the publisher pattern in rclpy, (4) describe the subscriber/callback pattern in rclpy
  - **`## The Role of rclpy in ROS 2`**: rclpy is the Python client library for ROS 2. It wraps the underlying C++ ROS 2 core and exposes Pythonic APIs for creating Nodes, Publishers, Subscribers, and Services. :::note: "rclpy is the bridge between your AI model's Python logic and the ROS 2 communication graph. It translates Python function calls into ROS 2 messages."
  - **`## Anatomy of a ROS 2 Node in Python`**: Show a conceptual Python block (tagged ```python) with inline architectural comments explaining each section:
    ```python
    # 1. INITIALIZATION — register this process with the ROS 2 graph
    rclpy.init()
    node = rclpy.create_node('ai_decision_node')

    # 2. PUBLISHER — declare an outbound channel on the graph
    publisher = node.create_publisher(String, '/command_topic', 10)

    # 3. SPIN — keep the node alive and processing incoming messages
    rclpy.spin(node)
    ```
    Explain each numbered section in prose beneath the block. No installation steps. No colcon.
  - **`## The Publisher Pattern in rclpy`**: Conceptual explanation of how a Node publishes data. An AI inference engine detecting an object publishes the result to `/detections`. Code block showing only the publish call with comment. :::tip: "Think of publishing as placing a message on a bulletin board. Any subscriber watching that board will receive it automatically."
  - **`## The Subscriber Pattern in rclpy`**: Conceptual explanation of how a Node subscribes to a topic and processes data via a callback function. Code block showing subscription creation and a minimal callback function stub, fully commented. :::note: "The callback is triggered automatically by rclpy whenever a new message arrives on the topic. You write the logic; rclpy handles the delivery."
  - **`## Connecting an AI Decision Engine to ROS 2`**: Describe the architectural pattern: AI model runs inference → publishes result to a ROS 2 topic → a downstream Node subscribes and acts on it. No full example — just the data-flow description in prose. :::warning: "Never import OpenAI, TensorFlow, or PyTorch directly into a ROS 2 Node's callback. Keep inference in a separate process and communicate results via topics to avoid blocking the ROS 2 spin loop."
  - **`## Summary`**: 4-sentence recap: rclpy's role → Node anatomy → publisher pattern → subscriber/callback pattern.
  - **Widget**: `<RagChatbot context="module-1" />` as last line
  - **Constraint**: ≤3,500 prose words; no colcon/workspace setup; no C++ code; all code blocks tagged ```python; no installation commands

**Checkpoint**: Chapter 3 renders; all code blocks have `python` tag; no workspace/build commands present; :::warning about callback blocking is visible.

---

## Phase 6: User Story 4 — Chapter 4: Defining the Physical Form with URDF (Priority: P4)

**Goal**: Deliver a fully renderable Chapter 4 that explains URDF XML structure — visual vs. collision geometry — without physics equations or Denavit-Hartenberg parameters.

**Independent Test**: A student can read a URDF snippet and explain why a robot needs both a visual mesh and a separate collision mesh, without referencing dynamics equations.

### Implementation for User Story 4

- [x] T007 [US4] Write `docs/module-1/chapter-4-urdf.mdx` with the following structure and content:
  - **Frontmatter**: `title: "Chapter 4 — Defining the Physical Form with URDF"`
  - **H1**: `# Chapter 4 — Defining the Physical Form with URDF`
  - **`## Learning Objectives`**: 4 bullets — (1) define URDF and explain its role in robotics software, (2) distinguish between a Link and a Joint in a robot skeleton, (3) explain the difference between visual and collision geometry, (4) identify the purpose of the `<inertial>` tag without deriving its mathematics
  - **`## What is URDF and Why It Exists`**: URDF = Unified Robot Description Format. An XML file that describes a robot's physical structure. ROS 2 reads it to understand the robot's body — where its joints are, what its arms look like, how its sensors are positioned. Analogy: a blueprint — the architect's drawing versus the structural engineer's load model. :::note: "URDF is not a simulation format. It is a description format. Physics engines and simulators read URDF, but URDF itself contains no physics."
  - **`## Links and Joints — The Robot Skeleton`**: A Link is a rigid body part (arm segment, torso, wheel). A Joint connects two Links and defines how one moves relative to the other (revolute = rotates, prismatic = slides, fixed = no movement). Show a minimal XML snippet tagged ```xml with a `<link>` and a `<joint>` element, fully commented. No math.
  - **`## Visual Geometry vs Collision Geometry`**: Visual geometry is what the 3D renderer draws — the detailed mesh that looks realistic. Collision geometry is the simplified shape the physics engine uses to detect contact — usually a box, cylinder, or sphere wrapping the real shape. :::tip: "Using the full visual mesh for collision detection would be computationally prohibitive. A robot arm with 50,000 polygon fingers uses a cylinder for collision — it's fast and accurate enough." Show an XML snippet with `<visual>` and `<collision>` siblings under a `<link>`, tagged ```xml, commented.
  - **`## The Inertial Tag and Why It Matters`**: The `<inertial>` tag tells physics simulators how mass is distributed in a Link. It is required for simulation but NOT for visualization or joint control. :::warning: "Do not derive the inertia tensor manually. Use your robot manufacturer's datasheet or a mesh-analysis tool to extract these values. The numbers go into the XML; you do not calculate them by hand." Show the XML tag structure only — no tensor mathematics, no derivations.
  - **`## Building a Robot Description Step by Step`**: Walk through the logical order: define Links → define Joints connecting them → add Visual geometry → add Collision geometry → add Inertial properties for simulation. Prose only — no full URDF file dump.
  - **`## Summary`**: 4-sentence recap: URDF's role → Links and Joints as skeleton → visual vs collision geometry → inertial tag for simulation.
  - **Widget**: `<RagChatbot context="module-1" />` as last line
  - **Constraint**: ≤3,500 prose words; zero inertia tensor math; zero D-H parameters; all code blocks tagged ```xml; no physics derivations

**Checkpoint**: Chapter 4 renders; :::warning about inertia tensor is present; no equations appear anywhere; all XML blocks tagged.

---

## Phase 7: User Story 5 — RAG Chatbot Widget + Sidebar Registration (Priority: P5)

**Goal**: Register all four chapters in `sidebars.js` under a Module 1 category and confirm `<RagChatbot context="module-1" />` is present at the bottom of every chapter file.

**Independent Test**: A reviewer can grep all four `.mdx` files for `context="module-1"` and find exactly one match per file. Opening `sidebars.js` shows the Module 1 category with all four chapter doc IDs.

### Implementation for User Story 5

- [x] T008 [US5] Update `sidebars.js` at repository root: add a Module 1 category object to the sidebar items array with `type: 'category'`, `label: 'Module 1: The Robotic Nervous System'`, `collapsed: false`, and `items` array containing the four doc IDs: `'module-1/chapter-1-middleware'`, `'module-1/chapter-2-nodes-topics'`, `'module-1/chapter-3-rclpy'`, `'module-1/chapter-4-urdf'`. If `sidebars.js` does not yet exist, create it as a standard Docusaurus v3 manual sidebar file exporting a `sidebars` object.
- [x] T009 [P] [US5] Verify `<RagChatbot context="module-1" />` appears exactly once at the bottom of `docs/module-1/chapter-1-middleware.mdx` (after `## Summary`, no trailing content after widget)
- [x] T010 [P] [US5] Verify `<RagChatbot context="module-1" />` appears exactly once at the bottom of `docs/module-1/chapter-2-nodes-topics.mdx`
- [x] T011 [P] [US5] Verify `<RagChatbot context="module-1" />` appears exactly once at the bottom of `docs/module-1/chapter-3-rclpy.mdx`
- [x] T012 [P] [US5] Verify `<RagChatbot context="module-1" />` appears exactly once at the bottom of `docs/module-1/chapter-4-urdf.mdx`

**Checkpoint**: All four chapters have the widget line; `sidebars.js` contains the Module 1 category; all four doc IDs in the sidebar match the actual file paths.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Quality gates that span all chapters before merge.

- [x] T013 [P] Word count validation: confirm each of the four `.mdx` files has ≤3,500 prose words — check `docs/module-1/chapter-1-middleware.mdx`
- [x] T014 [P] Word count validation — check `docs/module-1/chapter-2-nodes-topics.mdx`
- [x] T015 [P] Word count validation — check `docs/module-1/chapter-3-rclpy.mdx`
- [x] T016 [P] Word count validation — check `docs/module-1/chapter-4-urdf.mdx`
- [x] T017 Math content scan: confirm zero equations, zero LaTeX notation, zero Denavit-Hartenberg references across all four chapter files
- [x] T018 H2 heading audit: confirm all `##` headings in all four files include a topic qualifier (not bare "Introduction", "Overview", etc.) — required for RAG chunk quality (FR-004)
- [x] T019 Code block tag audit: confirm all fenced code blocks in all four files carry a language tag (`python` or `xml`) — no untagged triple-backtick blocks
- [x] T020 Run `npm run build` (or equivalent Docusaurus build command) and confirm zero errors and zero broken-link warnings for the module-1 pages

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 — `.gitignore` check
- **US1/Chapter 1 (Phase 3)**: Depends on Phase 1 (directory + stub must exist)
- **US2/Chapter 2 (Phase 4)**: Depends on Phase 1; can start after Phase 3 is complete (recommended) or in parallel with Phase 3
- **US3/Chapter 3 (Phase 5)**: Depends on Phase 1; independent of Phases 3–4
- **US4/Chapter 4 (Phase 6)**: Depends on Phase 1; independent of Phases 3–5
- **US5/Sidebar (Phase 7)**: Depends on Phases 3–6 (all four chapter files must exist)
- **Polish (Phase 8)**: Depends on all chapter files and sidebar being complete

### Chapter Independence

- Chapters 1–4 are content-independent — they can be drafted in parallel if multiple authors are available
- Each chapter is independently renderable in Docusaurus once the stub (T002) is in place
- Chapter 2's analogy builds on Chapter 1's framing — recommended to draft in order for narrative coherence, but technically independent

### Within Each Chapter Phase

- Write frontmatter + H1 → Write Learning Objectives → Write content H2s in order → Write Summary → Add widget line

### Parallel Opportunities

- T009–T012 (widget verification): all [P] — run together once all four chapters are written
- T013–T016 (word count): all [P] — run together in Polish phase
- Chapters 1–4 themselves can be drafted in parallel if staffed accordingly

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001–T002)
2. Complete Phase 2: Foundational (T003)
3. Complete Phase 3: Chapter 1 (T004)
4. **STOP and VALIDATE**: Does a reader understand middleware after reading Chapter 1?
5. If yes, proceed to Chapter 2

### Incremental Delivery

1. Phase 1 + 2 → Foundation ready
2. Chapter 1 (T004) → MVP — one standalone conceptual chapter
3. Chapter 2 (T005) → Adds publish-subscribe model
4. Chapter 3 (T006) → Adds Python/AI integration
5. Chapter 4 (T007) → Completes Module 1 physical form
6. Phase 7 (T008–T012) → Sidebar + widget verification
7. Phase 8 (T013–T020) → Quality gates before merge commit

### Commit After Each Chapter

Per the constitution's commit standard:
```
content(ch01): add Chapter 1 — The Need for Robotic Middleware
content(ch02): add Chapter 2 — Nodes, Topics, and Services
content(ch03): add Chapter 3 — Connecting the AI Brain with rclpy
content(ch04): add Chapter 4 — Defining the Physical Form with URDF
feat(module-1): add sidebars.js Module 1 category and widget verification
```

---

## Notes

- [P] tasks = different files, no dependencies — safe to run in parallel
- [Story] label maps each task to its user story for independent traceability
- Every chapter MUST independently render in Docusaurus before marking complete
- T002 (RagChatbot stub) is a hard blocker — do not skip
- Math content check (T017) is mandatory before any merge — constitution non-negotiable
- Total tasks: 20 | Parallel-eligible: 8 | Sequential gates: 3 (T001→T002→T004 chain)

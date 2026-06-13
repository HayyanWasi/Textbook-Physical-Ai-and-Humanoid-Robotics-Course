# Feature Specification: Module 2 — The Digital Twin (Gazebo & Unity)

**Feature Branch**: `003-digital-twin`
**Created**: 2026-06-13
**Status**: Draft
**Input**: User description: "The Digital Twin (Gazebo & Unity)"

## User Scenarios & Testing *(mandatory)*

### User Story 1 — The Digital Twin Concept and Gazebo Fundamentals (Priority: P1)

An AI engineering student who has completed Module 1 reads Chapter 5 and can explain what a digital twin is, why it matters for physical AI development, and how Gazebo acts as the deterministic physics anchor in a simulation pipeline — without needing to understand the mathematics of rigid-body dynamics.

**Why this priority**: The digital twin concept is the foundational prerequisite for all subsequent simulation content. Without understanding why a virtual robot must mirror a physical one, Chapters 6–8 lack motivational context. This is the MVP chapter for the module.

**Independent Test**: A student who has read only Chapter 5 can answer: "What is a digital twin?" and "Why can't engineers test a physical humanoid robot at full speed without a simulation first?" — both correctly, without referencing any equations.

**Acceptance Scenarios**:

1. **Given** a student has read Chapter 5, **When** they are asked to explain what Gazebo provides that a CAD tool does not, **Then** they can articulate that Gazebo simulates real-time physics (gravity, collision, joint torque) while a CAD tool only describes geometry.
2. **Given** the chapter content is loaded by the RAG pipeline, **When** a student asks "What is the relationship between Gazebo and ROS 2?", **Then** the chatbot can retrieve a chunk from Chapter 5 that correctly describes Gazebo as a physics simulator that publishes sensor and state data onto ROS 2 topics.

---

### User Story 2 — Simulating Physics and Collision Configuration (Priority: P2)

A student reads Chapter 6 and understands how Gazebo models physical behaviour — gravity, friction, collisions — using configuration parameters rather than manual mathematical derivation. They can interpret a basic Gazebo world configuration and explain what each physics parameter controls.

**Why this priority**: Physics simulation is the mechanism that makes a digital twin deterministic and trustworthy. Without understanding how gravity and collision parameters work conceptually, students cannot reason about why simulation results match or diverge from physical hardware.

**Independent Test**: A student can read a Gazebo world configuration snippet and explain, in plain language, what the `<gravity>` parameter does and why the collision geometry of a robot link uses a simplified cylinder rather than the full visual mesh.

**Acceptance Scenarios**:

1. **Given** a student has read Chapter 6, **When** shown a Gazebo world file with `<gravity>0 0 -9.8</gravity>`, **Then** they can explain that this configures Earth-standard downward acceleration and that changing it simulates a different gravitational environment (e.g., lunar).
2. **Given** the chapter content, **When** a student asks why collision geometry uses primitives instead of detailed meshes, **Then** they can explain the computational cost tradeoff without referencing any physics formulas.

---

### User Story 3 — Unity for High-Fidelity Rendering and Human-Robot Interaction (Priority: P3)

A student reads Chapter 7 and understands why Unity is used alongside Gazebo — not as a replacement, but as the photorealistic layer for rendering environments, simulating human presence, and testing human-robot interaction scenarios that Gazebo's physics engine cannot render convincingly.

**Why this priority**: The Gazebo-and-Unity complementary framing is the key pedagogical insight of this module. Without it, students treat them as competing tools and miss the modern engineering pipeline.

**Independent Test**: A student can explain why a roboticist would run Gazebo and Unity simultaneously on the same robot model, and name one scenario that requires Unity's rendering capabilities that Gazebo alone cannot support.

**Acceptance Scenarios**:

1. **Given** a student has read Chapter 7, **When** asked "Which tool runs the physics simulation — Gazebo or Unity?", **Then** they correctly answer Gazebo, and can explain that Unity provides the visual environment and human-facing interface while Gazebo provides the physics ground truth.
2. **Given** a student has read Chapter 7, **When** asked to describe a use case for Unity in a robotics pipeline, **Then** they name a scenario involving high-fidelity visual rendering, human avatar simulation, or interactive human-robot testing that requires photorealistic environments.

---

### User Story 4 — Sensor Simulation and ROS 2 Topic Mapping (Priority: P4)

A student reads Chapter 8 and understands how simulated sensors (LiDAR, depth camera, IMU) produce output that is structurally identical to real hardware sensor data, published on the same ROS 2 topics defined in Module 1. They can identify the ROS 2 topic name for each sensor type and explain what data it carries.

**Why this priority**: Sensor simulation closes the loop between Module 1 (communication graph) and Module 2 (simulation). This is the chapter that makes the module technically coherent — students see how everything connects. It is lower priority than the foundational chapters but essential for completeness.

**Independent Test**: A student can name the ROS 2 topic that carries simulated LiDAR data, identify the message type, and explain that swapping a simulated sensor for a real one requires only changing the driver node — not the perception pipeline — because the topic interface is identical.

**Acceptance Scenarios**:

1. **Given** a student has read Chapters 1–4 (Module 1) and Chapter 8, **When** asked "How does a simulated depth camera differ from a real one from the ROS 2 graph's perspective?", **Then** they answer that it does not differ — both publish the same message type on the same topic, and downstream nodes cannot tell the difference.
2. **Given** the chapter content is chunked by the RAG pipeline, **When** a student asks "What ROS 2 topic does the simulated IMU publish to?", **Then** the chatbot retrieves the correct answer from Chapter 8 with the topic name and message type.

---

### Edge Cases

- What happens when a student expects Gazebo to replace Unity, or vice versa? Chapter 7 must explicitly prevent this misconception with clear framing of their complementary roles.
- What happens if a student with no Python background reads Chapter 8? Sensor data descriptions must be conceptual — no code required to understand what the data carries.
- What if the `<RagChatbot>` component is not yet backed by a live API? The stub from Module 1 (`src/components/RagChatbot.jsx`) already handles this — it renders a visible placeholder without throwing.
- What happens if a student skips Module 1? Chapter 5 must briefly re-anchor the ROS 2 topic concept so Module 2 is independently readable, while Chapter 8 deepens the connection for students who have read Module 1.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The textbook MUST deliver exactly four MDX chapter files under `docs/module-2/`: Chapter 5 (digital twin concept), Chapter 6 (physics and collisions), Chapter 7 (Unity rendering), and Chapter 8 (sensor simulation).
- **FR-002**: Every chapter MUST begin with a "Learning Objectives" section containing exactly 4 testable outcome bullets, and end with a "Summary" section containing a 3–5 sentence recap.
- **FR-003**: All `##` (H2) headings MUST be self-describing and topic-qualified — no bare headings such as "Introduction", "Overview", or "Background" — to ensure clean RAG chunking boundaries.
- **FR-004**: Every chapter MUST contain at least 2 Docusaurus admonitions (`:::note`, `:::tip`, or `:::warning`) to highlight key insights and common misconceptions.
- **FR-005**: The textbook content MUST NOT contain any mathematical derivations, physics equations, matrix transformations, or LaTeX notation. Parameters and configuration values may appear in code blocks with plain-language prose explanations only.
- **FR-006**: Every chapter MUST include `<RagChatbot context="module-2" />` as the final element, after the Summary section.
- **FR-007**: Chapter 8 MUST explicitly map each simulated sensor type (LiDAR, depth camera, IMU) to its ROS 2 topic name and message type, cross-referencing the topic names introduced in Module 1 (e.g., `/lidar/scan`, `/camera/image_raw`).
- **FR-008**: Chapter 7 MUST explicitly frame Gazebo and Unity as complementary — not competing — tools in a single engineering pipeline, and state clearly which tool owns physics simulation and which owns visual rendering.
- **FR-009**: Each chapter MUST stay within approximately 10 pages of content density (≤3,500 prose words), with all fenced code blocks carrying a language tag (e.g., `xml`, `yaml`, `python`).
- **FR-010**: The Docusaurus sidebar (`sidebars.ts`) MUST be updated to include a Module 2 category with all four chapter doc IDs, appearing after the Module 1 category.

### Key Entities

- **Chapter**: A single MDX file covering one coherent sub-topic of Module 2. Each chapter is an independently renderable, RAG-chunkable unit with defined H2 boundaries.
- **Digital Twin**: The concept of a virtual robot model whose state mirrors a physical robot in real time, enabling safe testing and development.
- **Simulated Sensor**: A software component within the simulation environment that produces data structurally identical to physical hardware, published on a ROS 2 topic.
- **ROS 2 Topic Mapping**: The correspondence between a simulated sensor's output and the ROS 2 topic name and message type that downstream perception nodes expect.
- **RAG Chunk**: A semantically bounded section of text produced by splitting a chapter at H2 heading boundaries, used for retrieval by the chatbot backend.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A student with Python knowledge but no robotics background can read Chapter 5 and correctly explain the digital twin concept and Gazebo's role in one paragraph — without referencing equations.
- **SC-002**: All four chapter files pass a zero-math audit: no LaTeX, no equations, no matrix notation appears anywhere in the prose or code blocks.
- **SC-003**: All four chapter files compile successfully in Docusaurus (`npm run build`) with zero errors and zero broken-link warnings.
- **SC-004**: Each chapter file contains exactly one `<RagChatbot context="module-2" />` element at the end of the file — verifiable by grep.
- **SC-005**: All `##` headings across all four files are topic-qualified — a reviewer can read any heading in isolation and identify the subject without reading surrounding context.
- **SC-006**: Chapter 8 explicitly names and maps a minimum of 3 simulated sensor types (LiDAR, depth camera, IMU) to their corresponding ROS 2 topic names and message types.
- **SC-007**: Chapter 7 contains an explicit statement identifying Gazebo as the physics simulation layer and Unity as the visual/interactive rendering layer, preventing the most common student misconception.

## Assumptions

- The `RagChatbot.jsx` stub created in Module 1 is already present at `frontend/src/components/RagChatbot.jsx` and will be used without modification for Module 2.
- The Docusaurus sidebar config is at `frontend/sidebars.ts` (TypeScript format), not `sidebars.js` — confirmed by Module 1 implementation.
- Chapters are written for an audience that has completed Module 1 (familiar with ROS 2 nodes, topics, and URDF). Brief re-anchoring of key terms is acceptable but not a full re-explanation.
- No Gazebo or Unity installation is required by the reader — all content is conceptual and configuration-level, not hands-on tutorial.
- The "module-2" RAG context scope will be configured in the FastAPI backend in a future feature; this spec only governs the content and `context` prop value.

## Dependencies

- **Module 1 (003-digital-twin depends on 002-ros2-nervous-system)**: The ROS 2 topic names introduced in Module 1 (`/lidar/scan`, `/camera/image_raw`, `/odom`, `/cmd_vel`, `/detections`) are assumed knowledge in Chapter 8. Chapter 5 makes a brief back-reference to the ROS 2 graph concept.
- **`frontend/src/components/RagChatbot.jsx`**: Must exist before `npm run build` can succeed for Module 2 pages. Satisfied by Module 1 implementation.
- **`frontend/sidebars.ts`**: Must contain the Module 1 category before Module 2 is appended. Satisfied by Module 1 implementation.

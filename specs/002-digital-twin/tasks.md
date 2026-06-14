---
description: "Task list for Module 2 — The Digital Twin (Gazebo & Unity)"
---

# Tasks: Module 2 — The Digital Twin (Gazebo & Unity)

**Input**: Design documents from `/specs/002-digital-twin/`
**Prerequisites**: plan.md ✅ | spec.md ✅ | research.md ✅ | data-model.md ✅ | contracts/content-contract.md ✅

**Tests**: No test tasks — content feature validated by build check and manual review (not explicitly requested in spec).

**Organization**: Tasks grouped by user story (P1 → P4) to enable independent chapter authoring and validation.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1–US5)
- Exact file paths included in every task description

## Path Conventions

- Content: `frontend/docs/module-2/`
- Sidebar: `frontend/sidebars.ts`
- Widget stub: `frontend/src/components/RagChatbot.jsx` (already exists from Module 1)

---

## Phase 1: Setup

**Purpose**: Create the directory structure required before any content can be written.

- [x] T001 Create directory `frontend/docs/module-2/` at repository root

**Checkpoint**: `frontend/docs/module-2/` exists and is empty.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Verify shared infrastructure before any chapter can be validated via build.

**⚠️ CRITICAL**: No chapter build verification can pass until this phase is complete.

- [x] T002 Verify `frontend/src/components/RagChatbot.jsx` exists with a valid default export (created in Module 1); if missing for any reason, recreate the stub: `export default function RagChatbot({ context }) { return <div style={{border:'1px dashed #ccc',padding:'1rem',marginTop:'2rem'}}>RAG Chatbot [{context}] — backend integration pending</div>; }`

**Checkpoint**: `RagChatbot.jsx` is present and renders without throwing; `frontend/sidebars.ts` contains the Module 1 category.

---

## Phase 3: User Story 1 — Chapter 5: The Digital Twin and Gazebo (Priority: P1) 🎯 MVP

**Goal**: Deliver a fully renderable Chapter 5 that explains what a digital twin is, why it exists, and how Gazebo acts as the physics simulation anchor in a robotics engineering pipeline — with zero math and using the "shadow clone" / "stunt double" analogy.

**Independent Test**: A student who has read only Chapter 5 can correctly answer "What is a digital twin?" and "Why can't you test a full-speed humanoid robot without a simulation?" — both without referencing any equations.

### Implementation for User Story 1

- [x] T003 [US1] Write `frontend/docs/module-2/chapter-5-digital-twin-gazebo.mdx` with the following structure and content:
  - **File header**: `---\ntitle: "Chapter 5 — The Digital Twin and Gazebo"\n---\n\nimport RagChatbot from '@site/src/components/RagChatbot';`
  - **H1**: `# Chapter 5 — The Digital Twin and Gazebo`
  - **`## Learning Objectives`** (first H2): exactly 4 bullets — (1) define a digital twin and explain why physical AI development requires one, (2) describe Gazebo's role as a physics simulation layer in a robotics pipeline, (3) explain how Gazebo connects to the ROS 2 graph, (4) articulate the limits of simulation and why a physical robot is still required
  - **`## What is a Digital Twin`**: Define digital twin: a virtual replica of a physical system whose simulated state mirrors the real system in real time (or near-real time). The "shadow clone" analogy — you test the dangerous maneuver on the clone; the real robot only executes what the clone has proven safe. Physical robots are expensive, fragile, and dangerous at full speed. The digital twin absorbs the risk of development. :::note admonition: "A digital twin is not a 3D model or a CAD drawing. A CAD drawing shows what a robot looks like; a digital twin simulates what a robot does — how it moves under gravity, how its joints respond to torque, how its sensors react to the world."
  - **`## Why Physical AI Development Requires Simulation`**: Explain the three core reasons: (1) Safety — testing a 1.5-metre humanoid at full walking speed on concrete risks hardware damage and injury; (2) Cost — destroying a physical robot arm during a failed grasp experiment costs thousands of dollars; (3) Speed — a simulation can run faster than real time, compressing months of real-world trial-and-error into hours. :::tip admonition: "Engineers at Boston Dynamics and Figure run millions of simulation steps overnight. The robot walks in simulation for thousands of hours before it takes a single real step."
  - **`## Gazebo as the Physics Simulation Layer`**: Introduce Gazebo (the current release is named Gz Harmonic) as an open-source robotics simulator. It is not a 3D renderer — it is a physics engine. Gazebo models: gravity (objects fall at the correct acceleration), rigid-body dynamics (robot links move as solid objects), joint constraints (joints respect their limits), and contact detection (objects collide rather than pass through each other). Analogy: if Unity is the "eyes" (what the environment looks like), Gazebo is the "muscles and gravity" (what the robot feels and how the world pushes back). :::warning admonition: "Gazebo is not a visual rendering tool — its default graphics are intentionally simple. Do not judge Gazebo's output by how realistic it looks. Judge it by how accurately the physics matches real hardware."
  - **`## How Gazebo Connects to the ROS 2 Graph`**: Explain that Gazebo does not operate in isolation. It connects to ROS 2 via a bridge (ros_gz_bridge or the equivalent for the installed version). Once bridged, Gazebo publishes simulated sensor data onto the same ROS 2 topics that real hardware uses. A simulated LiDAR publishes to `/lidar/scan`; a simulated camera publishes to `/camera/image_raw`. The rest of the ROS 2 system — the perception nodes, the path planner, the motor controller — receives these messages and cannot distinguish simulated data from real data. This is the key architectural property: the ROS 2 graph is the abstraction boundary between real and simulated worlds.
  - **`## The Limits of Simulation and the Reality Gap`**: Acknowledge that simulation is not perfect. The "reality gap" is the difference between simulated and real-world behaviour. A robot that walks perfectly in Gazebo may stumble on a real floor because: (1) the simulated floor has no micro-texture friction variation, (2) simulated motors respond instantly while real motors have electrical delay, (3) simulated sensors have no noise while real sensors always do. :::note admonition: "The goal of a good simulation is not perfection — it is to reduce the number of dangerous experiments on real hardware. A 90% accurate simulation that prevents 90% of real-world failures is enormously valuable."
  - **`## Summary`** (last H2): 4-sentence recap covering: what a digital twin is → why simulation is required for physical AI → Gazebo's role as the physics layer connected to ROS 2 → the reality gap as an inherent limitation.
  - **Widget**: `<RagChatbot context="module-2" />` as the very last line after Summary
  - **Constraint**: ≤3,500 prose words; zero equations; all H2s self-describing; minimum 2 admonitions (3 present in spec above)

**Checkpoint**: Chapter 5 renders in Docusaurus; "shadow clone" analogy is present; Gazebo/Unity muscles-vs-eyes framing is introduced; no math content; ≥2 admonitions visible.

---

## Phase 4: User Story 2 — Chapter 6: Simulating Physics and Collisions (Priority: P2)

**Goal**: Deliver a fully renderable Chapter 6 that teaches how Gazebo models physics — gravity, collisions, friction — using configuration parameters in SDF world files, without requiring students to understand the underlying mathematics.

**Independent Test**: A student can read a Gazebo world file snippet containing `<gravity>0 0 -9.8</gravity>` and correctly explain what it configures, and can explain why collision geometry uses simplified primitives (cylinder, box, sphere) rather than the full visual mesh.

### Implementation for User Story 2

- [x] T004 [US2] Write `frontend/docs/module-2/chapter-6-physics-collisions.mdx` with the following structure and content:
  - **File header**: `---\ntitle: "Chapter 6 — Simulating Physics and Collisions in Gazebo"\n---\n\nimport RagChatbot from '@site/src/components/RagChatbot';`
  - **H1**: `# Chapter 6 — Simulating Physics and Collisions in Gazebo`
  - **`## Learning Objectives`**: 4 bullets — (1) distinguish SDF (world description) from URDF (robot description) introduced in Module 1, (2) interpret a Gazebo world file's gravity and physics parameters in plain language, (3) explain how Gazebo detects collisions between objects using simplified geometry, (4) describe what happens when a robot's physics parameters are incorrect in simulation
  - **`## What a Gazebo World File Describes`**: Introduce SDF (Simulation Description Format) as the native format Gazebo uses for world files — distinct from URDF (which describes robot bodies, as covered in Module 1 Chapter 4). SDF describes the environment: gravity, ground plane, ambient lighting, objects in the world, and physics engine parameters. Show a minimal SDF world snippet tagged `xml` with inline comments: `<world name="simulation_world">`, `<gravity>0 0 -9.8</gravity>` (Earth standard, XYZ vector in m/s²), `<physics type="ode">` (the physics solver). Explain each element in prose beneath the block — no derivations. :::note admonition: "URDF describes the robot. SDF describes the world the robot lives in. In a Gazebo simulation, your robot URDF is loaded into an SDF world file — the two formats are complementary, not competing."
  - **`## Configuring Gravity and Environmental Physics Parameters`**: Explain that the gravity vector `<gravity>0 0 -9.8</gravity>` sets downward acceleration. Changing the Z component to `-1.62` simulates the Moon; setting all components to 0 simulates microgravity. Engineers change this to test robots designed for space or underwater environments. Other world parameters: `<max_step_size>` controls simulation time resolution (smaller = more accurate, more computationally expensive); `<real_time_factor>` controls how fast simulation runs relative to real time (2.0 = runs twice as fast as wall clock). :::tip admonition: "You don't need to understand the physics solver equations. You need to understand what each parameter controls in plain English. The Gazebo documentation describes every parameter with a one-sentence explanation — you set the knobs, Gazebo does the physics."
  - **`## How Gazebo Detects Collisions Between Objects`**: Explain collision detection at the conceptual level. Gazebo uses a physics engine (ODE, Bullet, or DART) to check whether two collision geometries are intersecting at each simulation timestep. The collision geometry of each robot link is the simplified mesh from URDF's `<collision>` element (introduced in Module 1, Chapter 4). Show an SDF friction surface snippet tagged `xml` explaining surface contact parameters (friction coefficients as named parameters, not derived). :::warning admonition: "If your robot's collision geometry is too complex (high-polygon mesh), collision detection becomes computationally prohibitive. This is why Module 1's Chapter 4 taught simplified collision primitives — boxes, cylinders, spheres. The benefit is not just visual cleanliness; it is simulation performance."
  - **`## What Happens When Physics Parameters Are Wrong`**: Describe common misconfiguration symptoms in plain language: (1) Wrong mass in `<inertial>` → robot tumbles or floats as if in zero gravity; (2) Missing collision geometry → robot falls through the floor; (3) Wrong friction → robot slides as if on ice or sticks to surfaces; (4) Wrong joint limits → joints reach impossible angles before the constraint engages. Frame these as diagnostic signals, not physics derivations. :::note admonition: "Simulation debugging is pattern recognition, not equation solving. Each symptom maps to a parameter. If the robot falls through the floor, you have missing collision geometry. If it spins in place, check the friction values."
  - **`## Summary`**: 4-sentence recap: SDF = world description (distinct from URDF) → gravity and physics parameters as configuration knobs → simplified collision geometry for performance → misconfiguration symptoms as diagnostic patterns.
  - **Widget**: `<RagChatbot context="module-2" />` as last line
  - **Constraint**: ≤3,500 prose words; zero physics equations; all XML blocks tagged `xml`; no derivation of ODE/Bullet equations; minimum 2 admonitions

**Checkpoint**: Chapter 6 renders; SDF/URDF distinction is clear; `<gravity>` snippet present and explained; :::warning about collision geometry complexity is visible; no math.

---

## Phase 5: User Story 3 — Chapter 7: Unity and High-Fidelity Rendering (Priority: P3)

**Goal**: Deliver a fully renderable Chapter 7 that establishes Gazebo and Unity as complementary tools in a single pipeline — Gazebo owns physics, Unity owns photorealistic visual rendering — and identifies the specific use cases that require Unity's capabilities.

**Independent Test**: A student can answer "Which tool simulates physics — Gazebo or Unity?" (Gazebo), and name one robotics use case that requires Unity's rendering capabilities (e.g., training vision models with photorealistic datasets, HRI testing with human avatars).

### Implementation for User Story 3

- [x] T005 [US3] Write `frontend/docs/module-2/chapter-7-unity-rendering.mdx` with the following structure and content:
  - **File header**: `---\ntitle: "Chapter 7 — Unity and High-Fidelity Rendering"\n---\n\nimport RagChatbot from '@site/src/components/RagChatbot';`
  - **H1**: `# Chapter 7 — Unity and High-Fidelity Rendering`
  - **`## Learning Objectives`**: 4 bullets — (1) explain why Gazebo's default rendering is insufficient for some robotics tasks, (2) describe the role of Unity as the visual and interactive layer in a robotics pipeline, (3) explain how Unity connects to the ROS 2 graph via the ROS–Unity bridge, (4) identify at least two use cases that require Unity that Gazebo alone cannot support
  - **`## Why Gazebo Alone Is Insufficient for High-Fidelity Rendering`**: Gazebo's physics accuracy is excellent, but its renderer produces simple, flat visuals — adequate for confirming that a robot arm reaches a target position, but inadequate for tasks that depend on realistic visual appearance. A computer vision model trained to detect a pedestrian in Gazebo's flat rendering will fail on a real-world camera feed with lighting variation, shadow, texture, and motion blur. The gap between Gazebo's simplified rendering and the real world is too large for visual perception tasks. :::note admonition: "Gazebo's goal is physics accuracy, not visual realism. Its renderer is a debugging tool, not a training data generator. For tasks that depend on what the robot sees, you need a photorealistic renderer."
  - **`## Unity as the Visual and Interactive Layer`**: Unity is a real-time 3D rendering engine used across gaming, architecture, and robotics. In a robotics pipeline it serves as the photorealistic environment layer: it renders what Gazebo's physics engine computes but cannot show convincingly. The key principle: **Gazebo simulates physics; Unity renders the world.** In a combined pipeline, the robot's physical state (joint positions, velocities, sensor readings) is computed in Gazebo. Unity receives that state via the ROS 2 graph and renders a photorealistic view of the robot in its environment. :::warning admonition: "Unity does not run the physics simulation. Gazebo does. If you use Unity without Gazebo, your robot's visual appearance is perfect but its movement is physically wrong. Always pair them."
  - **`## How Unity Connects to the ROS 2 Graph`**: The Unity Robotics Hub (an open-source Unity package from Unity Technologies) includes a ROS–TCP bridge. This bridge runs a ROS 2 node on the machine running Gazebo that accepts TCP connections from Unity. The data flow is: (1) Gazebo computes the robot's new joint positions at each physics timestep; (2) the joint states are published to `/joint_states` on the ROS 2 graph; (3) the ROS–TCP bridge forwards this message to Unity over a local TCP connection; (4) Unity receives the joint positions and updates the visual representation of the robot. The student does not need to install or configure this bridge — understanding the architecture is sufficient. :::tip admonition: "The ROS 2 graph is the integration point between Gazebo and Unity. Both tools are subscribers to the same topics. Gazebo produces physics data; Unity consumes it for rendering. ROS 2 is the shared language between them."
  - **`## Use Cases Where Unity Is Essential`**: Enumerate specific scenarios. Prose only — no code: (1) **Training computer vision models**: A robot's perception model needs thousands of training images with realistic lighting, textures, and shadows. Gazebo cannot produce these. Unity renders photorealistic images of synthetic environments that can augment or replace real-world training data. (2) **Human-robot interaction (HRI) testing**: Testing how a robot navigates around human pedestrians requires simulated human avatars that move naturally. Unity provides humanoid avatar systems; Gazebo does not. (3) **Accessibility and safety evaluation**: Simulating environments with users in wheelchairs, with children, or with fragile objects requires believable visual fidelity that affects decision logic. (4) **Public demonstration and stakeholder communication**: Showing a robot performing a task in a photorealistic environment is more compelling to non-technical stakeholders than Gazebo's flat rendering.
  - **`## Gazebo and Unity as Complementary Tools in One Pipeline`**: Summarise the pipeline explicitly. The two tools are not alternatives — they solve different problems. A well-equipped robotics team uses both: Gazebo for physics simulation and algorithm validation, Unity for visual training data generation and HRI testing. Choosing one and ignoring the other creates blind spots. :::note admonition: "A robotics engineer's mental model: Gazebo is your physics lab. Unity is your photography studio. You need both. The robot's brain (ROS 2) connects them."
  - **`## Summary`**: 4-sentence recap: Gazebo's renderer is not the right tool for visual fidelity tasks → Unity provides photorealistic rendering as the visual layer in the pipeline → the ROS–Unity bridge connects Unity to the ROS 2 graph using the same topic interface → Gazebo and Unity are complementary, never competing.
  - **Widget**: `<RagChatbot context="module-2" />` as last line
  - **Constraint**: ≤3,500 prose words; zero rendering/ray-tracing equations; all H2s self-describing; minimum 2 admonitions; FR-008 must be satisfied — an explicit statement that "Gazebo simulates physics; Unity renders the world" must appear verbatim or paraphrased clearly in `## Unity as the Visual and Interactive Layer`

**Checkpoint**: Chapter 7 renders; the Gazebo/Unity roles are stated explicitly in the second content H2; :::warning about Unity not running physics is present; no math content.

---

## Phase 6: User Story 4 — Chapter 8: Simulating Sensors and the ROS 2 Bridge (Priority: P4)

**Goal**: Deliver a fully renderable Chapter 8 that explains how simulated sensors produce output structurally identical to real hardware, maps LiDAR, depth camera, and IMU to their ROS 2 topic names and message types (cross-referencing Module 1), and establishes the "sensor-agnostic perception pipeline" principle.

**Independent Test**: A student can name the ROS 2 topic and message type for simulated LiDAR, depth camera, and IMU; and can explain why a perception node cannot distinguish simulated data from real sensor data.

### Implementation for User Story 4

- [x] T006 [US4] Write `frontend/docs/module-2/chapter-8-sensor-simulation.mdx` with the following structure and content:
  - **File header**: `---\ntitle: "Chapter 8 — Simulating Sensors and the ROS 2 Bridge"\n---\n\nimport RagChatbot from '@site/src/components/RagChatbot';`
  - **H1**: `# Chapter 8 — Simulating Sensors and the ROS 2 Bridge`
  - **`## Learning Objectives`**: 4 bullets — (1) explain how a simulated sensor's output is structurally identical to a real sensor's output on the ROS 2 graph, (2) identify the ROS 2 topic name and message type for a simulated LiDAR, depth camera, and IMU, (3) explain the "sensor-agnostic perception pipeline" principle and why it matters for testing, (4) connect the simulated sensor topic names in Chapter 8 to the example topics introduced in Module 1 Chapter 2
  - **`## How Simulated Sensors Mirror Real Hardware`**: Introduce the "stunt double" analogy. A film stunt double performs the dangerous scene instead of the lead actor — they are trained to replicate every movement so precisely that the audience cannot tell the difference. Simulated sensors are the stunt doubles for real sensors. A Gazebo LiDAR plugin reads the virtual environment geometry and produces a point cloud or scan — the same data structure, with the same field layout, published on the same ROS 2 topic type, that a real LiDAR would produce. The perception node subscribed to `/lidar/scan` receives the message and processes it identically regardless of source. :::note admonition: "The Gazebo sensor plugin is the only component aware that the data is simulated. Every other Node in the ROS 2 graph — the object detector, the path planner, the logger — receives real-looking data and responds as it would in the real world. This is why simulation is useful for testing: the algorithms run unmodified."
  - **`## LiDAR Simulation and the ROS 2 Topic Interface`**: Describe a simulated 2D LiDAR (rotating laser scanner). In Gazebo, the LiDAR plugin sweeps a virtual laser beam across the simulated environment and records the distance to every surface it hits. This data is published to the ROS 2 graph as a `sensor_msgs/LaserScan` message on the topic `/scan` (or `/lidar/scan` depending on configuration). In Module 1 Chapter 2, `/lidar/scan` was introduced as an example topic name — Chapter 8 explains what it actually carries. The `LaserScan` message contains an array of distance values, one per beam angle, along with range limits and angular resolution — all without any knowledge of the physical device that generated them. :::tip admonition: "Swapping a simulated LiDAR for a real one requires only changing which driver node publishes the data. The topic name, message type, and all downstream Nodes remain unchanged. This is the power of the ROS 2 abstraction."
  - **`## Depth Camera Simulation and the ROS 2 Topic Interface`**: Describe a simulated depth camera. The Gazebo depth camera plugin produces two output streams: (1) an RGB image published as `sensor_msgs/Image` on `/camera/image_raw` — the same topic introduced in Module 1 Chapter 2; (2) a depth image published as `sensor_msgs/Image` on `/camera/depth/image_raw`, where each pixel value is the distance from the camera to the nearest surface at that pixel's viewing angle. A depth camera is the combination of a regular camera and a per-pixel distance sensor. Simulated depth data replicates the structure of real sensor output; it does not replicate real-world noise (slight variation in depth values) or lens distortion without additional plugin configuration. :::note admonition: "A depth camera produces two ROS 2 topics, not one. The RGB image topic is used by object detection nodes; the depth image topic is used by 3D mapping and obstacle avoidance nodes. Both are present in simulation and on real hardware."
  - **`## IMU Simulation and the ROS 2 Topic Interface`**: Describe a simulated IMU (Inertial Measurement Unit). An IMU measures acceleration and angular velocity — it is the robot's sense of balance and orientation change. In Gazebo, the IMU plugin reads the robot link's linear and angular velocity from the physics engine and publishes this as a `sensor_msgs/Imu` message on `/imu/data`. The message contains three fields: linear acceleration (X, Y, Z in m/s²), angular velocity (X, Y, Z in rad/s), and orientation quaternion. :::warning admonition: "Do not derive the quaternion mathematics. The orientation field in a `sensor_msgs/Imu` message is a unit quaternion representing rotation — your code reads it as four numbers (x, y, z, w) and passes it to a library (tf2 in ROS 2) that handles the geometry. You never manually compute quaternion products."
  - **`## The Sensor-Agnostic Perception Pipeline`**: Summarise the architectural principle. A well-designed ROS 2 perception pipeline subscribes to standard topic names and message types. It does not import the sensor's driver library; it does not query the hardware directly. Because the interface is standard, the entire perception pipeline — every subscriber node from object detector to path planner — can be tested in Gazebo without modification and then deployed on real hardware by simply starting the real sensor driver instead of the simulation plugin. This is the full circle connecting Module 1's ROS 2 graph (communication layer) → Module 1's URDF (robot body) → Module 2's digital twin (Gazebo physics) → Module 2's sensor simulation (ROS 2 topic bridge). Show a reference table of all three sensors:

    | Sensor | ROS 2 Topic | Message Type | Module 1 Reference |
    |---|---|---|---|
    | 2D LiDAR | `/scan` or `/lidar/scan` | `sensor_msgs/LaserScan` | Ch. 2 example topic |
    | Depth Camera (color) | `/camera/image_raw` | `sensor_msgs/Image` | Ch. 2 example topic |
    | Depth Camera (depth) | `/camera/depth/image_raw` | `sensor_msgs/Image` | (new in Module 2) |
    | IMU | `/imu/data` | `sensor_msgs/Imu` | (new in Module 2) |
    | Odometry | `/odom` | `nav_msgs/Odometry` | Ch. 2 example topic |

  - **`## Summary`**: 4-sentence recap: simulated sensors as stunt doubles publishing identical message types → LiDAR produces `sensor_msgs/LaserScan` on `/lidar/scan` → depth camera produces two streams (RGB + depth) → IMU produces `sensor_msgs/Imu` on `/imu/data` → the sensor-agnostic pipeline runs unmodified in simulation and on real hardware.
  - **Widget**: `<RagChatbot context="module-2" />` as last line
  - **Constraint**: ≤3,500 prose words; zero equations; sensor-to-topic table MUST be present; all H2s self-describing; minimum 2 admonitions; cross-references to Module 1 Chapter 2 topic names required

**Checkpoint**: Chapter 8 renders; sensor-to-topic table present with at least LiDAR + depth camera + IMU; :::warning about quaternions is present; cross-references to `/lidar/scan` and `/camera/image_raw` from Module 1 are explicit.

---

## Phase 7: User Story 5 — Sidebar Registration + Widget Verification (Priority: P5)

**Goal**: Register all four chapters in `frontend/sidebars.ts` under a Module 2 category and confirm `<RagChatbot context="module-2" />` is present at the bottom of every chapter file.

**Independent Test**: A reviewer can grep all four `.mdx` files for `context="module-2"` and find exactly one match per file. Opening `frontend/sidebars.ts` shows the Module 2 category with all four chapter doc IDs, appearing after the Module 1 category.

### Implementation for User Story 5

- [x] T007 [US5] Update `frontend/sidebars.ts`: append a Module 2 category object to the `tutorialSidebar` array, after the existing Module 1 category. The addition: `{ type: 'category', label: 'Module 2: The Digital Twin', collapsed: false, items: ['module-2/chapter-5-digital-twin-gazebo', 'module-2/chapter-6-physics-collisions', 'module-2/chapter-7-unity-rendering', 'module-2/chapter-8-sensor-simulation'] }`
- [x] T008 [P] [US5] Verify `<RagChatbot context="module-2" />` appears exactly once at the bottom of `frontend/docs/module-2/chapter-5-digital-twin-gazebo.mdx` (after `## Summary`, no trailing content after widget)
- [x] T009 [P] [US5] Verify `<RagChatbot context="module-2" />` appears exactly once at the bottom of `frontend/docs/module-2/chapter-6-physics-collisions.mdx`
- [x] T010 [P] [US5] Verify `<RagChatbot context="module-2" />` appears exactly once at the bottom of `frontend/docs/module-2/chapter-7-unity-rendering.mdx`
- [x] T011 [P] [US5] Verify `<RagChatbot context="module-2" />` appears exactly once at the bottom of `frontend/docs/module-2/chapter-8-sensor-simulation.mdx`

**Checkpoint**: All four chapters have the widget line; `frontend/sidebars.ts` contains the Module 2 category; all four doc IDs in the sidebar match the actual file paths.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Quality gates that span all chapters before merge.

- [x] T012 [P] Word count validation: confirm `frontend/docs/module-2/chapter-5-digital-twin-gazebo.mdx` has ≤3,500 prose words (`wc -w` total must be under 4,500)
- [x] T013 [P] Word count validation — check `frontend/docs/module-2/chapter-6-physics-collisions.mdx`
- [x] T014 [P] Word count validation — check `frontend/docs/module-2/chapter-7-unity-rendering.mdx`
- [x] T015 [P] Word count validation — check `frontend/docs/module-2/chapter-8-sensor-simulation.mdx`
- [x] T016 Math content scan: confirm zero equations, zero LaTeX notation, zero Denavit-Hartenberg references, zero matrix expressions across all four chapter files (`grep -E '\$|\\frac|\\theta|\\sum|D-H|Denavit' frontend/docs/module-2/*.mdx`)
- [x] T017 H2 heading audit: confirm all `##` headings in all four files include a topic qualifier (not bare "Introduction", "Overview", "Background", "Summary" alone at start) — required for RAG chunk quality (FR-003)
- [x] T018 Code block tag audit: confirm all fenced code blocks in all four files carry a language tag (`xml`, `yaml`, or `python`) — no untagged triple-backtick blocks
- [x] T019 Admonition count audit: confirm each of the four files contains at least 2 admonition blocks (`:::note`, `:::tip`, or `:::warning`) — required by FR-004
- [x] T020 Run `npm run build` from `frontend/` directory and confirm zero errors and zero broken-link warnings for all module-2 pages

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 — verify stub exists
- **US1/Chapter 5 (Phase 3)**: Depends on Phase 1 (directory must exist); is the MVP
- **US2/Chapter 6 (Phase 4)**: Depends on Phase 1; independent of Phase 3 (recommended to draft Ch5 first for narrative continuity, but technically independent)
- **US3/Chapter 7 (Phase 5)**: Depends on Phase 1; independent of Phases 3–4
- **US4/Chapter 8 (Phase 6)**: Depends on Phase 1; independent of Phases 3–5 (references Module 1 topic names, not Module 2 chapters)
- **US5/Sidebar (Phase 7)**: Depends on Phases 3–6 (all four chapter files must exist before sidebar verification)
- **Polish (Phase 8)**: Depends on all chapter files and sidebar being complete

### Chapter Independence

- Chapters 5–8 are content-independent — they can be drafted in parallel if multiple authors available
- Each chapter is independently renderable in Docusaurus once the `RagChatbot.jsx` stub exists (T002)
- Chapter 6 builds on Chapter 4 (Module 1) collision geometry concepts — recommended to read Chapter 4 before drafting, but technically independent
- Chapter 8 references Module 1 Chapter 2 topic names — these are fixed, external references; Chapter 8 does not depend on Chapters 5–7

### Within Each Chapter Phase

- Write frontmatter + H1 → Write Learning Objectives → Write content H2s in order → Write Summary → Add widget line

### Parallel Opportunities

- T008–T011 (widget verification): all [P] — run together once all four chapters are written
- T012–T015 (word count): all [P] — run together in Polish phase
- T016–T019 (audit tasks): can run together after all chapters are written
- Chapters 5–8 themselves can be drafted in parallel if staffed accordingly

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001)
2. Complete Phase 2: Foundational (T002)
3. Complete Phase 3: Chapter 5 (T003)
4. **STOP and VALIDATE**: Does a student understand digital twins and Gazebo after reading Chapter 5?
5. If yes, proceed to Chapter 6

### Incremental Delivery

1. Phase 1 + 2 → Foundation ready
2. Chapter 5 (T003) → MVP — one standalone conceptual chapter
3. Chapter 6 (T004) → Adds physics simulation understanding
4. Chapter 7 (T005) → Adds Unity/rendering pipeline framing
5. Chapter 8 (T006) → Completes Module 2 with sensor-ROS 2 cross-reference
6. Phase 7 (T007–T011) → Sidebar + widget verification
7. Phase 8 (T012–T020) → Quality gates before merge commit

### Commit After Each Chapter

Per the constitution's commit standard:
```
content(ch05): add Chapter 5 — The Digital Twin and Gazebo
content(ch06): add Chapter 6 — Simulating Physics and Collisions in Gazebo
content(ch07): add Chapter 7 — Unity and High-Fidelity Rendering
content(ch08): add Chapter 8 — Simulating Sensors and the ROS 2 Bridge
feat(module-2): add Module 2 sidebar category and widget verification
```

---

## Notes

- [P] tasks = different files, no dependencies — safe to run in parallel
- [Story] label maps each task to its user story for independent traceability
- Every chapter MUST independently render in Docusaurus before marking complete
- T002 (RagChatbot stub verification) is a hard blocker — do not skip
- Math content check (T016) is mandatory before any merge — constitution non-negotiable
- FR-008 enforcement: Chapter 7 MUST explicitly state "Gazebo simulates physics; Unity renders the world" (or equivalent clear statement)
- Total tasks: 20 | Parallel-eligible: 9 | Sequential gates: 3 (T001→T002→T003 chain)

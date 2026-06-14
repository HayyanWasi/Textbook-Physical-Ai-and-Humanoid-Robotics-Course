---
description: "Task list for Module 3 — The AI-Robot Brain (NVIDIA Isaac™)"
---

# Tasks: Module 3 — The AI-Robot Brain (NVIDIA Isaac™)

**Input**: Design documents from `/specs/003-isaac-robot-brain/`
**Prerequisites**: plan.md ✅ | spec.md ✅ | research.md ✅ | data-model.md ✅ | contracts/content-contract.md ✅ | quickstart.md ✅

**Tests**: No test tasks — content feature validated by Docusaurus build check, word-count checks, and prohibited-term grep (not TDD — no logic to test-drive).

**Organization**: Tasks grouped by user story (P1 → P4, mapping to Chapters 9–12) to enable independent chapter authoring and validation.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no shared dependencies)
- **[Story]**: Which user story this task belongs to (US1–US4)
- Exact file paths included in every task description

## Path Conventions

- Content: `frontend/docs/module-3/`
- Sidebar: `frontend/sidebars.ts`
- RagChatbot component: `frontend/src/components/RagChatbot.jsx` (already exists — do not modify)

---

## Phase 1: Setup

**Purpose**: Create directory structure before any content can be written or built.

- [x] T001 Create directory `frontend/docs/module-3/` — run `mkdir -p frontend/docs/module-3/`

**Checkpoint**: `frontend/docs/module-3/` directory exists.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Verify the shared infrastructure needed by all four chapters before writing begins.

**⚠️ CRITICAL**: No chapter can be build-verified until these pass.

- [x] T002 Verify `frontend/src/components/RagChatbot.jsx` has a valid default export — run `node -e "require('./frontend/src/components/RagChatbot.jsx')"` or confirm file exists and exports a function; if missing, create a minimal stub: `export default function RagChatbot({ context }) { return <div>RAG [{context}] — pending</div>; }`
- [x] T003 Verify `frontend/sidebars.ts` is syntactically valid and Module 1 + Module 2 entries are intact — open `frontend/sidebars.ts` and confirm the file has exactly two category entries (Module 1 and Module 2) before any modification; do NOT edit it yet

**Checkpoint**: `RagChatbot.jsx` confirmed importable; `sidebars.ts` confirmed valid with 2 existing categories.

---

## Phase 3: User Story 1 — Chapter 9: Advanced Perception (Priority: P1) 🎯 MVP

**Goal**: Deliver a fully renderable Chapter 9 that establishes WHY standard sensors fail for humanoid autonomy and introduces the NVIDIA Isaac ecosystem as an integrated solution — the "Visual Cortex" framing. A student who reads only this chapter can explain the perception gap and name all four Isaac tools at a conceptual level.

**Independent Test**: Open `http://localhost:3000` after `cd frontend && npm start`. Navigate to the Chapter 9 page. A reader with no GPU knowledge can answer: "What is the sensing problem that NVIDIA Isaac solves?" and "What is the difference between a sensor and a perception system?" after reading to the end.

### Implementation for User Story 1

- [x] T004 [US1] Write `frontend/docs/module-3/chapter-9-advanced-perception.mdx` with the following exact structure and content:

  **Frontmatter + import**:
  ```
  ---
  title: "Chapter 9 — Advanced Perception for Humanoid Robots"
  ---

  import RagChatbot from '@site/src/components/RagChatbot';
  ```

  **H1**: `# Chapter 9 — Advanced Perception for Humanoid Robots`

  **## Learning Objectives** (must be first H2):
  - 4–5 bullets stating: understand why proximity sensors fail for humanoid autonomy; distinguish between raw sensing (detecting signals) and perception (understanding meaning); identify the four tools in the NVIDIA Isaac ecosystem and their roles; explain why humanoid robots require perception systems that exceed the capabilities of mobile robots.

  **## The Perception Gap in Humanoid Robotics**:
  Explain the conceptual difference between a *sensor* (a device that measures a physical signal — light, sound, distance) and a *perception system* (a system that interprets that signal to extract meaning). Use the analogy: a microphone detects sound waves; the human auditory cortex understands speech. A robot with only sensors can detect the world; a robot with perception can understand it. Frame this as the fundamental gap that prevents basic-sensor robots from operating autonomously in unstructured human environments. Include a `:::note` admonition comparing the sensing stack of a simple wheeled robot (ultrasonic, infrared, basic RGB camera) with what a humanoid needs (stereo depth, tactile, proprioception, fused 3D understanding). Build on Module 2 context — note that Gazebo simulated a robot that reacts to physics, but could not teach the robot to *recognise* what it was looking at.

  **## Why Standard Sensors Are Not Enough for Autonomous Humanoids**:
  Detail three specific failure modes of standard sensors in humanoid contexts: (1) *Static scene assumption* — a proximity sensor tells you an object is 0.5m away but not whether it is a glass table or a child's toy; the action taken must differ. (2) *Occlusion blindness* — a single 2D camera cannot see behind objects or around corners; humanoids navigating crowded environments require spatial awareness in 3D. (3) *Lighting dependency* — standard RGB cameras degrade sharply in low light, direct sunlight, or high-contrast scenes; a humanoid must operate reliably across all conditions. For each failure mode, give a concrete humanoid-specific scenario (e.g., reaching for a cup on a reflective surface, walking through a doorway with a box in hand, operating in a warehouse with bright overhead skylights).

  **## The NVIDIA Isaac Ecosystem**:
  Frame NVIDIA Isaac not as a single product but as a coordinated family of four tools, each addressing a different layer of the perception-to-movement pipeline. Use a brief paragraph per tool:
  - **Isaac Sim**: A photorealistic simulation environment used to generate synthetic training data for perception AI models. Think of it as a virtual film studio — it renders the robot's world so realistically that AI trained inside it can recognise objects in the real world. Covered in depth in Chapter 10.
  - **Isaac ROS**: A collection of hardware-accelerated processing packages that run on the robot in real time, handling tasks like visual mapping and 3D scene understanding. It is the live perception engine. Covered in Chapter 11.
  - **Isaac Lab**: A reinforcement learning framework for training robot *behaviour* policies — teaching the robot how to move, balance, and manipulate objects. Out of scope for this module; referenced for completeness.
  - **Nav2**: The navigation stack that translates perception data into movement commands — planning paths, avoiding obstacles, and issuing footstep instructions. Covered in Chapter 12.
  Include a `:::tip` admonition: "Think of the four tools as a pipeline: Isaac Sim trains the eyes → Isaac ROS runs the eyes in real time → Nav2 decides where to walk → Isaac Lab taught the robot how to walk."

  **## From Sensor Input to Understood Scene**:
  Describe the conceptual journey a signal takes from a camera lens to a meaningful scene understanding. Walk through: (1) raw pixel data arrives from a stereo camera; (2) Isaac ROS processes the stream to extract depth and identify features; (3) recognised objects are classified and located in 3D space; (4) the resulting scene model is passed to Nav2 for planning. Use plain-language descriptions only — no algorithm names or mathematical notation. Reinforce that this pipeline replaces the naive "if obstacle detected, stop" logic of simple wheeled robots with "this is a chair, 1.2m away, navigable to the left, with a child standing 0.8m behind it."

  **## Summary** (must be last H2 before component):
  4-sentence recap: (1) Standard sensors provide raw measurements but cannot interpret what those measurements mean — a gap that becomes critical in unstructured humanoid environments. (2) Three failure modes — static scene assumption, occlusion blindness, and lighting dependency — demonstrate why humanoid robots require full perception systems, not just improved sensors. (3) The NVIDIA Isaac ecosystem addresses this with four coordinated tools: Isaac Sim (training data), Isaac ROS (real-time perception), Isaac Lab (behaviour learning), and Nav2 (navigation). (4) The following chapters explore each tool in turn, building toward a complete picture of how a humanoid robot processes the world and decides how to move through it.

  **Final line**: `<RagChatbot context="module-3" />`

- [x] T005 [US1] Run quality checks on `frontend/docs/module-3/chapter-9-advanced-perception.mdx`:
  - Word count: `wc -w frontend/docs/module-3/chapter-9-advanced-perception.mdx` — must be ≤ 4,500 (total file words)
  - Prohibited terms: `grep -in "cuda\|matrix\|jacobian\|covariance\|eigenvalue\|kalman\|pseudocode\|gpu kernel" frontend/docs/module-3/chapter-9-advanced-perception.mdx` — must return zero results
  - RagChatbot check: `grep "RagChatbot" frontend/docs/module-3/chapter-9-advanced-perception.mdx` — must return exactly one line: `<RagChatbot context="module-3" />`
  - Confirm 5+ H2 sections and at least one `:::` admonition present in file

**Checkpoint**: Chapter 9 file passes all quality checks. Build check deferred to Phase 7.

---

## Phase 4: User Story 2 — Chapter 10: Isaac Sim & Synthetic Data (Priority: P2)

**Goal**: Deliver Chapter 10 that permanently disambiguates Gazebo (behavior testing) from Isaac Sim (perception training) in the student's mental model. The mandatory `## Gazebo vs. Isaac Sim: A Direct Comparison` section must exist as a standalone H2 for RAG chunk isolation. A student who reads only Chapters 9 and 10 can correctly answer "which simulator do I use to train my robot to recognise a chair in any lighting condition, and why?"

**Independent Test**: Navigate to Chapter 10 in the local dev server. Ask a peer who has read Chapter 8 (Gazebo sensor simulation): "After reading Chapter 10, can you explain why you would use Isaac Sim instead of Gazebo for teaching a robot to see?" If they can answer from memory, the chapter has achieved its disambiguation goal.

### Implementation for User Story 2

- [x] T006 [US2] Write `frontend/docs/module-3/chapter-10-isaac-sim-synthetic-data.mdx` with the following exact structure and content:

  **Frontmatter + import**:
  ```
  ---
  title: "Chapter 10 — Isaac Sim and Synthetic Training Data"
  ---

  import RagChatbot from '@site/src/components/RagChatbot';
  ```

  **H1**: `# Chapter 10 — Isaac Sim and Synthetic Training Data`

  **## Learning Objectives** (first H2):
  - 4–5 bullets: explain the sim-to-real gap and why it exists; distinguish between physics simulation (Gazebo) and photorealistic simulation (Isaac Sim) by purpose, not by appearance; describe what synthetic training data is and why it is preferable to collected real-world data for many perception tasks; explain at a conceptual level how AI models trained in Isaac Sim can transfer to a real robot.

  **## Two Simulators, Two Different Jobs**:
  Open with the core reframe: both Gazebo and Isaac Sim are simulators, but they solve fundamentally different problems. A simulator is a tool; you must ask "what is this tool designed to produce?" Gazebo produces realistic *physics* — it tells you how a robot will move, fall, or collide. Isaac Sim produces realistic *images* — it tells you what the robot will see when its cameras look at the world. One trains robot behaviour; the other trains robot vision. Use the analogy: a driving simulator trains your *judgment* — when to brake, how to merge. A visual recognition app trains your ability to *identify* road signs. Both involve simulated environments; neither trains the same skill. Include a `:::note` admonition: "If you completed Module 2, you used Gazebo to test how your robot moves through space. In this chapter, Isaac Sim is used for a completely different purpose: teaching the robot what to see, not how to move."

  **## Gazebo as a Physics Classroom (Module 2 in Context)**:
  Briefly recap Gazebo's role (2–3 paragraphs): it simulates rigid body dynamics, joint torques, sensor noise models, and collision geometry. Its output is robot motion and sensor readings under physical laws. A student used Gazebo to verify that a robot navigates around obstacles without tipping over. Gazebo is not designed to produce photorealistic renders — its visual output is intentionally abstract because the physics, not the visuals, are what matter. Robots trained in Gazebo learn *what to do*; they do not learn *what they are looking at*.

  **## Isaac Sim as a Perception Training Ground**:
  Introduce Isaac Sim's purpose: it renders the robot's environment with photorealistic accuracy — realistic lighting, shadows, material reflections, object textures — specifically to generate images that look like what a real camera would capture. Perception AI models (object detectors, depth estimators, scene classifiers) require enormous quantities of labelled images to learn from. Collecting these images in the real world is expensive, slow, and dangerous for a humanoid robot. Isaac Sim generates them synthetically — the virtual scene is rendered, and every object's location, class, and depth is automatically known without any human labelling effort. Explain the scale advantage: a real-world team might photograph 1,000 chairs over weeks; Isaac Sim can render 100,000 chairs in varied lighting, angles, and room configurations in hours. Include a `:::tip` admonition: "Synthetic data is not 'fake' data — it is precisely labelled data generated in a controlled environment. The AI model does not know whether its training images came from a camera or a renderer; it only sees pixels."

  **## Gazebo vs. Isaac Sim: A Direct Comparison**:
  **(MANDATORY standalone H2 — do not nest inside another section)**
  Present a comparison table with the following rows and columns:

  | Dimension | Gazebo | Isaac Sim |
  |---|---|---|
  | Primary Purpose | Physics simulation for testing robot behaviour | Photorealistic rendering for training perception AI |
  | Output | Robot joint states, collision data, sensor noise | Rendered images, depth maps, labelled scene data |
  | What it Trains | Robot motion policies (when to stop, turn, balance) | Vision models (what objects are, where they are) |
  | Typical Use In This Course | Module 2 — testing navigation and physics | Module 3 — generating synthetic training data |
  | Realism Goal | Accurate forces, torques, and contacts | Accurate lighting, materials, and textures |
  | What It Does NOT Do | Teach the robot to recognise objects visually | Simulate physics realistically for motion testing |

  Follow the table with a paragraph reinforcing: "These tools are not competitors — they address different stages of building a capable humanoid robot. A complete development pipeline uses both: Gazebo to test how the robot moves, Isaac Sim to train what the robot sees."

  **## The Sim-to-Real Gap and How Synthetic Data Bridges It**:
  Explain the sim-to-real gap: when an AI model is trained entirely in simulation and then deployed on a real robot, it sometimes fails because the simulated images look subtly different from real camera images (lighting artefacts, perfect geometry, missing lens distortion). Isaac Sim addresses this by: (1) adding configurable noise and distortion to rendered images to mimic real camera imperfections; (2) randomising scene parameters (lighting direction, object colours, background textures) so the model never memorises a single scene configuration; (3) rendering at sufficient fidelity that the gap between simulation and reality is smaller than older renderers produced. Do not describe the technical implementation of domain randomisation — explain the *concept*: "If you train on a thousand variations of the same chair in different lighting conditions, your model becomes robust to lighting changes in the real world." Include a `:::warning` admonition: "The sim-to-real gap is a real engineering challenge — it does not disappear automatically. Domain randomisation reduces it; it does not eliminate it. Real-world fine-tuning is often still required."

  **## Summary** (last H2):
  4-sentence recap: (1) Gazebo and Isaac Sim are both simulators, but they serve opposite purposes — Gazebo trains robot *behaviour* through physics, while Isaac Sim trains robot *vision* through photorealistic rendering. (2) Synthetic training data generated by Isaac Sim is not a shortcut — it is a scalable alternative to expensive, slow real-world data collection, with the added benefit of automatic labelling. (3) The sim-to-real gap describes the risk that a model trained in simulation may fail in the real world; domain randomisation in Isaac Sim reduces this risk by exposing the model to varied scene conditions during training. (4) Chapter 11 moves from training the robot's vision to running it: how Isaac ROS processes camera streams in real time to let the robot understand and map the space around it.

  **Final line**: `<RagChatbot context="module-3" />`

- [x] T007 [US2] Run quality checks on `frontend/docs/module-3/chapter-10-isaac-sim-synthetic-data.mdx`:
  - Word count ≤ 4,500 total words
  - Confirm `## Gazebo vs. Isaac Sim: A Direct Comparison` exists as a standalone H2 (run `grep "## Gazebo vs" frontend/docs/module-3/chapter-10-isaac-sim-synthetic-data.mdx`)
  - Prohibited terms check: `grep -in "cuda\|matrix\|jacobian\|gpu kernel" frontend/docs/module-3/chapter-10-isaac-sim-synthetic-data.mdx` — zero results
  - RagChatbot context check: `grep "context=" frontend/docs/module-3/chapter-10-isaac-sim-synthetic-data.mdx` — must return `context="module-3"`

**Checkpoint**: Chapter 10 includes the mandatory Gazebo vs. Isaac Sim comparison H2 and passes all quality checks.

---

## Phase 5: User Story 3 — Chapter 11: Isaac ROS & Visual SLAM (Priority: P3)

**Goal**: Deliver Chapter 11 that explains Visual SLAM entirely through the "city navigation by photographing landmarks" analogy — zero matrix notation, zero algorithm pseudocode, zero mentions of Jacobians, Kalman filters, or covariance. A student who has never studied linear algebra can read this chapter and correctly describe the VSLAM process using a novel analogy of their own construction.

**Independent Test**: Ask a non-technical reader to explain loop closure using their own words after reading Chapter 11. If they can describe "recognising a place you've been before and correcting your map accordingly" without being prompted, the conceptual abstraction succeeded.

### Implementation for User Story 3

- [x] T008 [US3] Write `frontend/docs/module-3/chapter-11-isaac-ros-vslam.mdx` with the following exact structure and content:

  **Frontmatter + import**:
  ```
  ---
  title: "Chapter 11 — Visual SLAM: How a Robot Builds Its Map"
  ---

  import RagChatbot from '@site/src/components/RagChatbot';
  ```

  **H1**: `# Chapter 11 — Visual SLAM: How a Robot Builds Its Map`

  **## Learning Objectives** (first H2):
  - 4–5 bullets: define SLAM (Simultaneous Localisation and Mapping) in plain language; explain why a robot cannot rely on GPS for indoor navigation; describe the concept of a visual landmark and how a robot uses it to track its position; explain loop closure using a real-world analogy; describe how Isaac ROS cuVSLAM fits into the perception pipeline without referencing its internal algorithms.

  **## What SLAM Means and Why Robots Need It**:
  Define SLAM conversationally: "Simultaneous Localisation and Mapping" is the process of building a map of an unknown environment *while at the same time* figuring out where you are within that map. The challenge is circular — you need the map to know your position, but you need your position to build the map correctly. Humans do this unconsciously when exploring a new building: you mentally note "I turned left at the reception desk, then went through two doors," and you build a mental map as you move. GPS solves this for outdoor navigation by providing an external position reference. Indoors, GPS signals are too weak and inaccurate for centimetre-level robot positioning. SLAM replaces GPS with observations from the robot's own cameras. Include a `:::note` admonition: "SLAM is not unique to robots — your smartphone's augmented reality features and autonomous vehicle lane-keeping systems both use variants of this same concept."

  **## Visual Landmarks as the Robot's Reference Points**:
  Explain the concept of a *visual landmark*: a distinctive, recognisable feature in the camera image that the robot can identify reliably from multiple viewpoints. Examples: a unique poster on a wall, the corner of a door frame, a distinctive junction where two floor tiles meet. The robot does not need to *understand* what a landmark is (it does not know it is a poster); it only needs to recognise that this cluster of visual features appeared in a previous image and matches a known pattern. Walk through the analogy: "Imagine photographing a landmark in a city — the Eiffel Tower, a specific fountain. When you photograph it again from a different angle, you can immediately compare your current position to your previous photographs and estimate how far you have walked and in which direction. The robot does the same, but with arbitrary indoor features instead of famous monuments." Explain that not all features make good landmarks — flat walls with no texture give the robot nothing to recognise; detailed, textured surfaces with edges and corners provide rich feature sets.

  **## Building the Map Step by Step**:
  Walk through the map-building process as a sequence of conceptual steps (use numbered list or short prose paragraphs, not pseudocode): (1) The robot's stereo camera captures a frame. It identifies distinctive visual features — edges, corners, textured patches. (2) These features are matched against features seen in the previous frame to estimate how much the robot has moved between the two frames (this is called *odometry* — estimating motion from visual change). (3) The estimated motion is used to update the robot's position estimate on the growing map. (4) New features that have never been seen before are added to the map. (5) Features that have been seen before are matched to their map positions to correct any accumulated drift. Emphasise that this is iterative and imperfect — each step introduces small errors that compound over time, which is why loop closure (next section) is critical. Include a `:::tip` admonition: "Think of this as building a sketch map while walking through a dark house with a torch — each step adds to the sketch, but small wobbles in your step introduce small inaccuracies. The more steps you take, the more the sketch drifts from reality."

  **## Loop Closure — When the Robot Recognises Where It Has Been**:
  Introduce loop closure as the mechanism that corrects accumulated drift. When the robot re-enters a part of the environment it has previously mapped, it recognises familiar visual landmarks in its camera feed. It can now compare its *current estimated position* (from all the incremental steps above) with its *known position from earlier in the map* at that landmark. If there is a discrepancy — for example, the robot estimates it is 0.3m to the left of where it was before — it corrects the entire recent trajectory to eliminate the accumulated error. Use the analogy: "Imagine walking around an unfamiliar city block, sketching your path as you go. When you arrive back at a building you photographed earlier, you compare your sketch to your original photograph. If your sketch shows the building in the wrong position, you correct your entire sketch to match. The robot does the same thing, automatically, every time it revisits a familiar area." Explain that loop closure is what allows a robot to maintain a consistent, accurate map over long exploration periods — without it, errors compound until the map becomes unusable.

  **## How Isaac ROS cuVSLAM Fits the Bigger Picture**:
  Position Isaac ROS cuVSLAM (short for Visual SLAM) within the Isaac ecosystem pipeline: it is the live perception component that runs on the robot during deployment. While Isaac Sim (Chapter 10) was used to *train* the robot's vision, Isaac ROS cuVSLAM is what *runs* that vision in real time. It takes the stereo camera stream, performs feature extraction, landmark matching, map updates, and loop closure continuously as the robot moves. Its output is a constantly updated 3D map and a real-time position estimate within that map. This position estimate is then consumed by Nav2 (Chapter 12) to plan safe, balanced movement through the environment. Include a `:::note` admonition: "cuVSLAM is named for its use of GPU hardware acceleration internally — but you do not need to understand GPU programming to understand what it does. Its role in the pipeline is simple: cameras in, map and position out."

  **## Summary** (last H2):
  4-sentence recap: (1) SLAM (Simultaneous Localisation and Mapping) solves the circular problem of building a map while simultaneously locating yourself within it — the indoor equivalent of GPS navigation. (2) Visual SLAM uses distinctive features in camera images as landmarks, matching them across frames to estimate motion and incrementally build a 3D map of the environment. (3) Loop closure prevents accumulated drift from making the map unusable — whenever the robot recognises a previously visited area, it corrects its entire trajectory to maintain consistency. (4) Isaac ROS cuVSLAM runs this pipeline in real time on the deployed robot, providing the position estimate and 3D map that Nav2 uses in Chapter 12 to plan how the humanoid will move through the world.

  **Final line**: `<RagChatbot context="module-3" />`

- [x] T009 [US3] Run quality checks on `frontend/docs/module-3/chapter-11-isaac-ros-vslam.mdx`:
  - Prohibited math terms: `grep -in "matrix\|jacobian\|covariance\|kalman\|eigenvalue\|pseudocode\|bundle adjustment\|factor graph" frontend/docs/module-3/chapter-11-isaac-ros-vslam.mdx` — must return zero results
  - Word count ≤ 4,500 total words
  - Confirm `## Loop Closure` and `## Building the Map` exist as standalone H2 sections
  - RagChatbot context check returns `context="module-3"`

**Checkpoint**: Chapter 11 contains zero mathematical notation. Loop closure and map-building are standalone H2 sections for RAG chunk isolation.

---

## Phase 6: User Story 4 — Chapter 12: Nav2 & Bipedal Path Planning (Priority: P4)

**Goal**: Deliver Chapter 12 that synthesises the full pipeline (Isaac Sim → Isaac ROS → Nav2) and clearly distinguishes bipedal path planning from wheeled navigation through the three-constraint frame (balance, footstep placement, gait cycle). A student who reads all four chapters can trace the complete pipeline from "camera input" to "footstep decision" in under three minutes.

**Independent Test**: After reading Chapter 12, a student can verbally explain: (1) why a standard wheeled navigation algorithm would be dangerous for a bipedal robot, and (2) how Nav2 addresses at least two of the three bipedal-specific constraints. If they can answer without notes, the synthesis is complete.

### Implementation for User Story 4

- [x] T010 [US4] Write `frontend/docs/module-3/chapter-12-nav2-bipedal-planning.mdx` with the following exact structure and content:

  **Frontmatter + import**:
  ```
  ---
  title: "Chapter 12 — Nav2 and Bipedal Path Planning"
  ---

  import RagChatbot from '@site/src/components/RagChatbot';
  ```

  **H1**: `# Chapter 12 — Nav2 and Bipedal Path Planning`

  **## Learning Objectives** (first H2):
  - 4–5 bullets: explain why path-planning algorithms designed for wheeled robots are insufficient and potentially dangerous for bipedal humanoids; identify the three structural constraints unique to bipedal navigation (centre-of-mass stability, footstep placement, gait cycle timing); describe Nav2's role in the NVIDIA Isaac pipeline; trace the complete conceptual pipeline from camera input to movement command; articulate the difference between path planning (where to go) and motion control (how to physically execute each step).

  **## Navigation for Legs Is Not Navigation for Wheels**:
  Open with the core reframe: most robotics navigation literature assumes the robot is either a differential-drive robot (two wheels) or a holonomic platform (moves freely in any direction). The planning algorithms for these platforms assume the robot can stop instantly, turn in place, and follow any computed path as long as it avoids obstacles. None of these assumptions hold for a bipedal humanoid. Introduce the three-constraint frame with brief definitions:
  - **Constraint 1 — Centre-of-Mass Stability**: A wheeled robot's centre of mass does not change as it moves. A bipedal robot's centre of mass shifts with every step. If the planned path causes the centre of mass to fall outside the robot's support polygon (the area defined by its feet), the robot falls. Path planning must account for where the robot's weight will be at every point in its trajectory, not just whether the path is obstacle-free.
  - **Constraint 2 — Footstep Placement**: A wheeled robot occupies a 2D footprint and can be treated as a moving circle or rectangle. A bipedal robot must place each foot on a surface that can support it — flat, stable, load-bearing. Stairs, curbs, gravel, and wet tiles all require different foot placement strategies. The planner cannot simply route through a grid; it must select valid footstep locations.
  - **Constraint 3 — Gait Cycle Timing**: A wheeled robot can pause mid-path and resume. A bipedal robot in mid-stride cannot pause without falling — the gait cycle (swing phase, stance phase, weight transfer) has momentum that must be respected. Path plans must be feasible to execute within the mechanical constraints of the walking gait.
  Include a `:::warning` admonition: "A path that is geometrically collision-free is not necessarily safe for a bipedal robot. A path that requires the robot to stop suddenly on a slope, place a foot on an edge, or change direction faster than its balance controller allows can cause a fall even with no obstacles present."

  **## The Role of Nav2 in the Isaac Stack**:
  Introduce Nav2 as the navigation middleware that sits above Isaac ROS in the pipeline. Isaac ROS provides the map and position; Nav2 consumes them to plan and execute movement. Describe Nav2's two primary functions:
  - **Path planning**: Given the robot's current position (from Isaac ROS VSLAM) and a target destination, compute a route through the map that avoids obstacles. For bipedal robots, this route is a sequence of *footstep positions* rather than a continuous trajectory.
  - **Behaviour control**: Monitor the robot's progress along the planned path, detect when replanning is needed (an unexpected obstacle appears, a footstep position becomes invalid), and issue updated commands to the motion controller.
  Clarify the scope boundary: Nav2 decides *where* the robot should place its next foot; the low-level motion controller (separate system, out of scope) decides *how* to physically execute the step while maintaining balance. Include a `:::tip` admonition: "Think of Nav2 as the 'navigator' in a car — it gives turn-by-turn directions. The driver (the robot's balance and motion controller) decides how fast to turn the wheel. Nav2 tells the robot where to step; the robot's body handles the mechanics of stepping."

  **## Planning Around Stability Constraints**:
  Describe how a bipedal-aware planner addresses the centre-of-mass stability constraint. The planner maintains a model of the robot's *support polygon* — the convex hull of the foot contact points at each moment. A valid step is one that keeps the projected centre of mass inside this polygon throughout the step transition. The planner evaluates candidate footstep sequences and rejects those that would destabilise the robot, even if they are geometrically shorter or faster. Explain that this is why bipedal navigation is inherently slower and more conservative than wheeled navigation — the safety constraint eliminates many routes that a wheeled robot would happily take.

  **## Footstep-Aware Path Planning**:
  Describe footstep planning as the process of selecting a discrete sequence of foot placements that connect the robot's current position to its goal. Unlike a wheeled robot path (a smooth curve through free space), a bipedal path is a series of landing zones — each footstep is a decision: which foot, where, in what orientation. The footstep planner evaluates terrain: it prefers flat, textured surfaces (good grip) and avoids edges, slopes above a threshold, and surfaces marked as unstable in the map. The output is an ordered list of footstep positions that Nav2 passes to the motion controller. Reinforce that the map provided by Isaac ROS cuVSLAM (Chapter 11) includes surface classification data that the footstep planner depends on — this is the direct conceptual link between the VSLAM chapter and this one.

  **## The Full Pipeline: From Camera Input to Footstep Decision**:
  Synthesise all four chapters into a single conceptual walkthrough. Write it as a numbered prose sequence (not pseudocode):
  1. The robot's stereo cameras capture the environment in real time.
  2. Isaac ROS cuVSLAM processes the camera stream: it identifies visual landmarks, estimates the robot's position, and updates the 3D map of the surrounding space.
  3. The 3D map is passed to Nav2, along with the robot's current position and the desired destination.
  4. Nav2's path planner computes a sequence of footstep positions that lead from the current position to the goal — selecting terrain that satisfies the stability and footstep placement constraints described above.
  5. Each footstep position is sent to the robot's motion controller, which executes the physical step while the balance system maintains the centre-of-mass within the support polygon.
  6. As the robot moves, step 2 repeats continuously — the map updates, the robot's position estimate updates, and Nav2 replans if an obstacle appears or a planned footstep becomes invalid.
  Include a `:::note` admonition: "Isaac Sim (Chapter 10) is not part of this real-time pipeline — it was used *before deployment* to train the vision models that Isaac ROS now runs. Synthetic data generation happens once, in the lab; real-time perception and navigation happen continuously, on the robot."

  **## Summary** (last H2):
  4-sentence recap: (1) Bipedal path planning is structurally different from wheeled navigation — it must respect three constraints absent in wheeled systems: centre-of-mass stability, valid footstep placement, and gait cycle continuity. (2) Nav2 serves as the navigation middleware that consumes the 3D map and position data from Isaac ROS and produces a sequence of footstep decisions that guide the humanoid to its goal. (3) The planning process is inherently conservative — many geometrically valid paths are rejected because they would compromise the robot's balance, which is why safety, not speed, is the primary constraint in bipedal navigation. (4) With Chapter 12 complete, the full Module 3 pipeline is clear: Isaac Sim trains the eyes, Isaac ROS runs the eyes in real time and builds the map, and Nav2 reads the map to plan where the feet go next.

  **Final line**: `<RagChatbot context="module-3" />`

- [x] T011 [US4] Run quality checks on `frontend/docs/module-3/chapter-12-nav2-bipedal-planning.mdx`:
  - Prohibited terms: `grep -in "cuda\|matrix\|jacobian\|kalman\|pseudocode\|algorithm" frontend/docs/module-3/chapter-12-nav2-bipedal-planning.mdx` — zero results (note: "algorithm" used generically is acceptable in non-code context; only flag if it appears with mathematical notation)
  - Confirm `## The Full Pipeline` section exists as standalone H2 (cross-module synthesis section)
  - Confirm the three constraints (centre-of-mass, footstep placement, gait cycle) are named explicitly
  - RagChatbot context check returns `context="module-3"`

**Checkpoint**: Chapter 12 names all three bipedal constraints, includes the full pipeline synthesis section, and passes quality checks.

---

## Phase 7: Navigation Integration & Verification

**Purpose**: Wire all four chapters into the sidebar, run the Docusaurus build, and verify the complete Module 3 experience end-to-end.

- [x] T012 Update `frontend/sidebars.ts` — open the file and append the following category object as the third entry in the `tutorialSidebar` array, after the Module 2 category closing brace:
  ```typescript
  {
    type: 'category',
    label: 'Module 3: The AI-Robot Brain',
    collapsed: false,
    items: [
      'module-3/chapter-9-advanced-perception',
      'module-3/chapter-10-isaac-sim-synthetic-data',
      'module-3/chapter-11-isaac-ros-vslam',
      'module-3/chapter-12-nav2-bipedal-planning',
    ],
  },
  ```
  Verify the existing Module 1 and Module 2 entries are unchanged.

- [x] T013 [P] Run cross-chapter quality sweep:
  - `grep -rh "RagChatbot" frontend/docs/module-3/` — must return exactly 4 lines, each `<RagChatbot context="module-3" />`
  - `grep -rin "cuda\|gpu kernel\|tensor" frontend/docs/module-3/` — zero results
  - `grep -n "## " frontend/docs/module-3/chapter-9-advanced-perception.mdx` — confirm 5+ H2 sections
  - `grep -n "## Gazebo vs\." frontend/docs/module-3/chapter-10-isaac-sim-synthetic-data.mdx` — confirm line exists
  - `grep -n "## Loop Closure" frontend/docs/module-3/chapter-11-isaac-ros-vslam.mdx` — confirm line exists
  - `grep -n "## The Full Pipeline" frontend/docs/module-3/chapter-12-nav2-bipedal-planning.mdx` — confirm line exists

- [x] T014 Run the Docusaurus production build: `cd frontend && npm run build` — must complete with zero errors; any build error reveals a broken import, malformed MDX, or invalid sidebar entry

- [x] T015 Start the local dev server: `cd frontend && npm start` — navigate to `http://localhost:3000`; verify:
  - "Module 3: The AI-Robot Brain" appears in the left sidebar
  - All four chapter links are visible and navigable
  - Each chapter renders without errors
  - The RagChatbot stub appears at the bottom of each chapter page
  - Module 1 and Module 2 sidebar entries are unchanged

**Checkpoint — Definition of Done**:
- `frontend/docs/module-3/` contains exactly 4 `.mdx` files
- `frontend/sidebars.ts` has exactly 3 category entries
- `npm run build` exits with code 0
- All four chapters visible and navigable in local dev server
- Cross-chapter quality sweep passes all grep checks

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 — BLOCKS all chapter work
- **US1 Chapter 9 (Phase 3)**: Depends on Phase 2
- **US2 Chapter 10 (Phase 4)**: Depends on Phase 2; can run in parallel with Phase 3
- **US3 Chapter 11 (Phase 5)**: Depends on Phase 2; can run in parallel with Phases 3 and 4
- **US4 Chapter 12 (Phase 6)**: Conceptually builds on Chapters 9–11 (references their content); should be written last
- **Navigation + Verification (Phase 7)**: Depends on all four chapters being complete

### User Story Dependencies

- **US1 (P1, Chapter 9)**: No story dependencies — can start after Phase 2
- **US2 (P2, Chapter 10)**: No story dependencies — can start after Phase 2 in parallel with US1
- **US3 (P3, Chapter 11)**: No story dependencies — can start after Phase 2 in parallel with US1/US2
- **US4 (P4, Chapter 12)**: Should be written after US1–US3 are drafted, since it references their content in the full-pipeline synthesis section

### Within Each Story

- Write content task (T004/T006/T008/T010) → then quality-check task (T005/T007/T009/T011)
- Quality check must pass before the chapter is considered story-complete

### Parallel Opportunities

- T006 (Ch10) and T008 (Ch11) can be written in parallel with T004 (Ch09) — different files, no shared dependencies
- T013 (cross-chapter grep sweep) and T014 (build) can begin as soon as all four chapter files and sidebar update are complete

---

## Parallel Example: Content Writing Sprint

```bash
# After Phase 2 completes, all three of these can start simultaneously:
Task T004: Write chapter-9-advanced-perception.mdx
Task T006: Write chapter-10-isaac-sim-synthetic-data.mdx
Task T008: Write chapter-11-isaac-ros-vslam.mdx

# After those are drafted:
Task T010: Write chapter-12-nav2-bipedal-planning.mdx (references the above)

# After all four chapters exist:
Task T012: Update sidebars.ts
Task T013: Run cross-chapter quality sweep [P with T012]
Task T014: Run npm run build
Task T015: Manual dev-server verification
```

---

## Implementation Strategy

### MVP First (User Story 1 Only — Chapter 9)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3 (T004 + T005): Chapter 9 only
4. Run `npm run build` with only Chapter 9 present
5. **STOP and VALIDATE**: Chapter 9 renders, RagChatbot stub visible, no build errors
6. Proceed to remaining chapters

### Full Delivery Order (Priority Sequence)

1. Phase 1 + Phase 2 → Foundation ready
2. Phase 3 (Ch9) → MVP deliverable
3. Phase 4 (Ch10) → Gazebo disambiguation complete
4. Phase 5 (Ch11) → VSLAM conceptual model complete
5. Phase 6 (Ch12) → Full pipeline synthesis complete
6. Phase 7 → Build verified, sidebar live, Module 3 shipped

---

## Notes

- No new React components required — `RagChatbot.jsx` already exists
- Sidebar file is `frontend/sidebars.ts` (TypeScript) — NOT `sidebars.js`
- Content goes in `frontend/docs/module-3/` — NOT `docs/module-3/` at repo root
- Each chapter must have `import RagChatbot from '@site/src/components/RagChatbot';` as line 1 after frontmatter
- `## Gazebo vs. Isaac Sim: A Direct Comparison` in Chapter 10 MUST be a standalone H2 (not nested)
- Chapter 11 must never use the words: matrix, Jacobian, covariance, Kalman, eigenvalue
- Chapter 12's `## The Full Pipeline` section is the cross-module synthesis — it is the most important section for SC-006 (student traces complete pipeline in under 3 minutes)

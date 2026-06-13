# Implementation Plan: Module 2 — The Digital Twin (Gazebo & Unity)

**Branch**: `002-digital-twin` | **Date**: 2026-06-13 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-digital-twin/spec.md`

## Summary

Produce four MDX chapter files for Docusaurus (Module 2: Digital Twin) that teach Gazebo physics
simulation and Unity rendering as complementary tools in a modern robotics engineering pipeline,
using the "Gazebo = muscles/gravity, Unity = eyes/environment" framing. All sensor simulations
are mapped to the ROS 2 topics established in Module 1. Zero mathematical derivations permitted.
The module is integrated into the Docusaurus sidebar and RAG context as `"module-2"`.

## Technical Context

**Language/Version**: MDX 3.x (Docusaurus v3.10.1) + React 18 (chat widget stub)
**Primary Dependencies**: Docusaurus v3 (`frontend/`), React 18, remark-mdx (built-in)
**Storage**: N/A — static content; Qdrant vector store is downstream (separate pipeline)
**Testing**: Manual Docusaurus build (`npm run build` from `frontend/`), word-count check per chapter, math-content grep, admonition count grep
**Target Platform**: GitHub Pages (static hosting); local dev via `npm start` in `frontend/`
**Project Type**: web (frontend static site — same Docusaurus instance as Module 1)
**Performance Goals**: Docusaurus build completes in under 60 seconds for all module pages
**Constraints**: ≤3,500 prose words per chapter; zero math derivations; all `##` headings self-describing for RAG chunking; minimum 2 admonitions per chapter; all code blocks tagged
**Scale/Scope**: 4 MDX files, 1 sidebar update, 0 new React components (reuse Module 1 stub)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Gate | Status |
|---|---|---|
| Strict Decoupling | MDX files MUST NOT contain any API calls, server logic, or direct Qdrant/OpenAI references | ✅ PASS — chapters are static prose; widget delegates to backend |
| Context-Bound RAG | The `<RagChatbot>` component MUST receive `context="module-2"` so backend scopes Qdrant retrieval to this module | ✅ PASS — `context` prop required by FR-006 |
| API Gateway Pattern | MDX files MUST NOT import any LLM SDK or vector-search client | ✅ PASS — only `import RagChatbot from '@site/src/components/RagChatbot'` allowed |
| Content Quality: Math | Zero heavy mathematical derivations permitted in any chapter | ✅ PASS — FR-005, SC-002 explicitly prohibit this |
| Content Quality: Structure | Exactly 4 chapters under Module 2; all `##` headings descriptive for RAG chunking | ✅ PASS — FR-001, FR-003 enforce this |
| Code Quality: Type Safety | N/A for MDX content files | ✅ N/A |
| Workflow: Paced Execution | Plan generated first, awaiting approval before content generation begins | ✅ PASS |
| Commit Standards | Each chapter committed separately as `content(ch0N): …` | ✅ PLANNED |

**Post-design re-check**: All gates pass. No constitution violations.

## Project Structure

### Documentation (this feature)

```text
specs/002-digital-twin/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output ✅
├── data-model.md        # Phase 1 output ✅
├── quickstart.md        # Phase 1 output ✅
├── contracts/           # Phase 1 output ✅
│   └── content-contract.md
└── tasks.md             # Phase 2 output (/sp.tasks command — NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/
└── docs/
    └── module-2/
        ├── chapter-5-digital-twin-gazebo.mdx
        ├── chapter-6-physics-collisions.mdx
        ├── chapter-7-unity-rendering.mdx
        └── chapter-8-sensor-simulation.mdx

frontend/sidebars.ts     # Updated to add Module 2 category (append after Module 1)
```

No new React components. `frontend/src/components/RagChatbot.jsx` from Module 1 is reused.

**Structure Decision**: Web app layout (frontend only). Same Docusaurus instance as Module 1.
No backend changes in scope.

## Phase 0: Research Findings

*See [research.md](./research.md) for full detail. Key decisions:*

- **Gazebo versioning**: Refer to "Gazebo" generically; note Gz Harmonic as current release in
  a parenthetical. World file format is SDF — distinct from URDF (which Module 1 covers).
- **Unity integration**: Describe the ROS–Unity bridge (Unity Robotics Hub / ROS-TCP-Connector)
  at the architecture level. Data flow: Gazebo → ROS 2 topics → Unity (via TCP bridge) → rendered scene.
- **SDF vs URDF**: URDF = robot description (taught in Module 1, Ch. 4); SDF = world description
  (gravity, physics engine parameters, environment objects). Chapter 6 introduces SDF.
- **Sensor topic mapping**: Standard ROS 2 topic names and message types documented in research.md
  and data-model.md. Chapter 8 MUST include at minimum: LiDAR, depth camera, IMU.
- **MDX import pattern**: Per-file import (consistent with Module 1 actuals, not the planned global
  registration). Each chapter includes `import RagChatbot from '@site/src/components/RagChatbot';`.
- **Sidebar append**: Append Module 2 category to `tutorialSidebar` array in `frontend/sidebars.ts`.

## Phase 1: Design

### Content Architecture

Each chapter follows the same rigid internal structure as Module 1:

```text
---
title: "Chapter N — [Title]"
---

import RagChatbot from '@site/src/components/RagChatbot';

# Chapter N — [Title]                         ← exactly one H1

## Learning Objectives                        ← MUST be first H2; exactly 4 bullets

## [Section A — Self-Describing Heading]      ← content H2 (topic-qualified)
prose + :::admonition (at least 2 per file total)

## [Section B — Self-Describing Heading]      ← content H2
prose + optional tagged code block (xml or yaml only)

## [Section C — Self-Describing Heading]      ← content H2 (minimum 3 content H2s)

## Summary                                    ← MUST be last H2
3–5 sentence recap

<RagChatbot context="module-2" />             ← after all prose, end of file
```

### Chapter Content Plan

| Chapter | File | Core Analogy | Primary H2 Sections |
|---|---|---|---|
| 5 | `chapter-5-digital-twin-gazebo.mdx` | Digital twin as "shadow clone" that absorbs risk | What is a Digital Twin; Why Engineers Need a Digital Twin; Gazebo as the Physics Simulation Layer; How Gazebo Connects to the ROS 2 Graph; The Limits of Simulation; Summary |
| 6 | `chapter-6-physics-collisions.mdx` | Physics parameters as "rules of the world" (not equations) | What a Gazebo World File Describes; Configuring Gravity and Environmental Physics; How Gazebo Models Collision Between Objects; Friction and Contact in Gazebo Without the Math; Summary |
| 7 | `chapter-7-unity-rendering.mdx` | Gazebo = muscles/gravity; Unity = eyes/environment | Why Photorealistic Rendering Requires Unity; How Unity Connects to the ROS 2 Graph; Use Cases Where Unity Is Essential; Gazebo and Unity as Complementary Tools in One Pipeline; Summary |
| 8 | `chapter-8-sensor-simulation.mdx` | Simulated sensors as "stunt doubles" for real hardware | How Simulated Sensors Mirror Real Hardware; LiDAR Simulation and the ROS 2 Topic Interface; Depth Camera Simulation and the ROS 2 Topic Interface; IMU Simulation and the ROS 2 Topic Interface; The Sensor-Agnostic Perception Pipeline; Summary |

### Analogy Architecture

The module uses two primary analogies that must be introduced in Chapter 5 and carried through:

1. **"Shadow Clone" / "Stunt Double"**: The digital twin is a perfect copy that absorbs all the
   risk. You test the dangerous maneuver on the clone; the real robot only executes what is proven safe.
2. **"Muscles and Gravity" vs "Eyes and Environment"**: Gazebo simulates what the robot *feels*
   (physics forces, collisions, sensor responses). Unity simulates what the environment *looks like*
   (photorealistic rendering, human avatars, lighting conditions). Both are needed for a complete
   test environment.

### RagChatbot Component Interface (Module 2)

Defined in [contracts/content-contract.md](./contracts/content-contract.md).

| Prop | Type | Required | Value for Module 2 |
|---|---|---|---|
| `context` | string | Yes | `"module-2"` |
| `placeholder` | string | No | `"Ask about this chapter…"` |

### Sidebar Structure

```typescript
// sidebars.ts — addition after Module 1 category
{
  type: 'category',
  label: 'Module 2: The Digital Twin',
  collapsed: false,
  items: [
    'module-2/chapter-5-digital-twin-gazebo',
    'module-2/chapter-6-physics-collisions',
    'module-2/chapter-7-unity-rendering',
    'module-2/chapter-8-sensor-simulation',
  ],
},
```

### Module 1 Cross-References (Chapter 8 Required)

Chapter 8 MUST explicitly cross-reference these Module 1 topic names:

| Topic Name | Message Type | Module 1 Source | Chapter 8 Teaching Point |
|---|---|---|---|
| `/camera/image_raw` | `sensor_msgs/Image` | Ch. 2 | Simulated camera publishes identical type |
| `/lidar/scan` | `sensor_msgs/LaserScan` | Ch. 2 | Simulated LiDAR publishes identical type |
| `/odom` | `nav_msgs/Odometry` | Ch. 2 | Simulated differential drive publishes identical type |

## Complexity Tracking

> No constitution violations were identified. This section is intentionally empty.

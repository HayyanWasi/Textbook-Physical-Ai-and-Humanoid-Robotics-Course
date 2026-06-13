# Data Model: Module 2 — The Digital Twin (Gazebo & Unity)

**Branch**: `003-digital-twin` | **Date**: 2026-06-13
**Phase**: 1 — Design

This module is a content feature (static MDX files), not a database-backed feature. The "data
model" describes the structural schema of content entities and their validation rules — the same
role a database schema plays for a CRUD feature.

---

## Entity 1: Chapter (MDX File)

**Represents**: A single renderable documentation page covering one sub-topic of Module 2.

**Required fields** (all must be present for a chapter to pass review):

| Field | Type | Constraint |
|---|---|---|
| `title` frontmatter | string | Format: `"Chapter N — [Full Title]"` |
| `title` (H1) | string | Exactly one H1 per file; must match frontmatter title |
| `## Learning Objectives` | H2 section | MUST be first H2; exactly 4 testable outcome bullets |
| Content H2 sections | H2 sections | Minimum 3 distinct H2 sections after Learning Objectives; each heading MUST include topic as qualifier |
| `## Summary` | H2 section | MUST be last H2 before the widget; 3–5 sentences |
| Admonition | MDX block | At least 2 `:::note`, `:::tip`, or `:::warning` blocks per file |
| Code blocks | fenced blocks | ALL code/config blocks MUST carry a language tag (`xml`, `yaml`, `python`); no bare triple-backtick |
| RagChatbot widget | JSX element | `<RagChatbot context="module-2" />` MUST appear exactly once, after `## Summary` |
| Import statement | MDX import | `import RagChatbot from '@site/src/components/RagChatbot';` MUST appear at top of file |
| Word count | integer | Prose words ≤ 3,500 per file |
| Math content | boolean | MUST be `false` — zero equations, zero derivations, zero LaTeX |

**Instances** (one per chapter in this module):

| ID | File | H1 Title | Core Analogy |
|---|---|---|---|
| `ch05` | `docs/module-2/chapter-5-digital-twin-gazebo.mdx` | Chapter 5 — The Digital Twin and Gazebo | Digital twin as a "shadow clone" that absorbs risk |
| `ch06` | `docs/module-2/chapter-6-physics-collisions.mdx` | Chapter 6 — Simulating Physics and Collisions in Gazebo | Physics parameters as "rules of gravity" |
| `ch07` | `docs/module-2/chapter-7-unity-rendering.mdx` | Chapter 7 — Unity and High-Fidelity Rendering | Gazebo = muscles/gravity; Unity = eyes/environment |
| `ch08` | `docs/module-2/chapter-8-sensor-simulation.mdx` | Chapter 8 — Simulating Sensors and the ROS 2 Bridge | Simulated sensors as "stunt doubles" for real hardware |

---

## Entity 2: Module (Sidebar Category)

**Represents**: A named group of four chapters listed together in the Docusaurus sidebar.

| Field | Type | Constraint |
|---|---|---|
| `label` | string | `"Module 2: The Digital Twin"` — exact string |
| `items` | string[] | Array of 4 Docusaurus doc IDs, ordered ch05 → ch08 |
| `type` | string | `"category"` |
| `collapsed` | boolean | `false` — module is open by default |

**Doc ID format**: `module-2/chapter-N-slug` (relative to `docs/`, no `.mdx` extension).

**Sidebar position**: Module 2 category MUST appear after the Module 1 category in `tutorialSidebar`.

---

## Entity 3: RagChatbot Component (Module 2 Instance)

**Represents**: The React component embedded at the bottom of each chapter, routing questions to
the FastAPI RAG backend scoped to Module 2.

| Field | Type | Constraint |
|---|---|---|
| `context` | string (prop) | REQUIRED. Value for Module 2: `"module-2"`. Qdrant metadata filter. |
| `placeholder` | string (prop) | OPTIONAL. Default: `"Ask about this chapter…"` |

**Stub behaviour**: The existing `frontend/src/components/RagChatbot.jsx` stub from Module 1
handles all module contexts — the `context` prop is rendered in the placeholder text but no
API call is made. No changes to the stub are required for Module 2.

---

## Entity 4: Heading Chunk (RAG Retrieval Unit)

**Represents**: The semantic unit extracted from each chapter by the Qdrant chunking script.

| Field | Type | Constraint |
|---|---|---|
| `module_id` | string | `"module-2"` — top-level Qdrant filter |
| `chapter_id` | string | e.g., `"module-2/chapter-5-digital-twin-gazebo"` |
| `heading` | string | The H2 text that opened this chunk |
| `content` | string | All prose between this H2 and the next H2 |

**Validation rules**:
- `heading` MUST NOT be a single generic word. `"Summary"` and `"Learning Objectives"` are
  metadata chunks, not content chunks.
- Each chapter MUST produce ≥ 3 retrievable content chunks (H2 sections excluding Learning
  Objectives and Summary).
- Heading text MUST be unique within a chapter file.

---

## Entity 5: Simulated Sensor (Content Reference Table)

**Represents**: A named sensor type with its Gazebo plugin, ROS 2 topic, and message type.
Not stored as a file — this entity is a content model that Chapter 8 must accurately represent.

| Sensor Type | Gazebo Plugin Category | ROS 2 Topic | ROS 2 Message Type |
|---|---|---|---|
| 2D LiDAR | Ray sensor plugin | `/scan` or `/lidar/scan` | `sensor_msgs/LaserScan` |
| 3D LiDAR / Point Cloud | GPU ray sensor plugin | `/points` or `/lidar/points` | `sensor_msgs/PointCloud2` |
| RGB Camera | Camera sensor plugin | `/camera/image_raw` | `sensor_msgs/Image` |
| Depth Camera | Depth camera plugin | `/camera/depth/image_raw` | `sensor_msgs/Image` |
| IMU | IMU sensor plugin | `/imu/data` | `sensor_msgs/Imu` |
| Odometry | Differential drive plugin | `/odom` | `nav_msgs/Odometry` |
| Joint States | Joint state publisher | `/joint_states` | `sensor_msgs/JointState` |

**Chapter 8 minimum coverage**: MUST document LiDAR, depth camera, and IMU with their topic
names and message types. Other entries are optional enrichment.

---

## State Transitions

This is a content feature; there are no runtime state machines. The authoring lifecycle is:

```
[Draft MDX] → [Math scan] → [Word count check] → [Build check: npm run build] → [Merged]
```

Each chapter transitions independently. Chapter 5 (MVP) can be merged before Chapter 6 is drafted.

---

## Dependency Map

```
Module 1 (002-ros2-nervous-system) — provides:
  ├── RagChatbot.jsx stub (frontend/src/components/)
  ├── sidebars.ts with Module 1 category (append Module 2 after)
  └── ROS 2 topic names referenced in Chapter 8:
      ├── /camera/image_raw  (introduced in Ch. 2)
      ├── /lidar/scan        (introduced in Ch. 2)
      ├── /odom              (introduced in Ch. 2)
      └── /cmd_vel           (introduced in Ch. 2)

Module 2 (003-digital-twin) — produces:
  ├── docs/module-2/chapter-5-digital-twin-gazebo.mdx
  ├── docs/module-2/chapter-6-physics-collisions.mdx
  ├── docs/module-2/chapter-7-unity-rendering.mdx
  ├── docs/module-2/chapter-8-sensor-simulation.mdx
  └── frontend/sidebars.ts (Module 2 category appended)
```

# Content Contract: Module 2 — The Digital Twin (Gazebo & Unity)

**Branch**: `002-digital-twin` | **Date**: 2026-06-13
**Phase**: 1 — Design
**Extends**: `specs/001-ros2-nervous-system/contracts/content-contract.md` v1.0.0

This contract defines the interface between the static MDX content layer (Docusaurus) and the
downstream systems that consume it: the RAG ingestion pipeline (Qdrant) and the chat widget
(FastAPI backend). It extends the Module 1 contract with Module 2-specific values.

---

## Contract 1: Chapter MDX File Structure

**Producer**: Content author (this feature)
**Consumer**: Docusaurus build system; Qdrant chunking script

### Required File Header

```mdx
---
title: "Chapter N — [Full Title]"
---

import RagChatbot from '@site/src/components/RagChatbot';
```

Note: The `id` and `sidebar_position` frontmatter fields are optional when using manual
`sidebars.ts` configuration (confirmed from Module 1 implementation). The `title` field
drives the `<title>` HTML tag and the sidebar item label if not overridden.

### Required Internal Structure

```
# Chapter N — [Title]                       ← exactly one H1

## Learning Objectives                      ← MUST be first H2; exactly 4 bullets

## [Section A — Self-Describing Heading]    ← content H2 (topic-qualified)
[prose + at least one :::admonition]

## [Section B — Self-Describing Heading]    ← content H2
[prose + optional tagged code block]

## [Section C — Self-Describing Heading]    ← content H2 (minimum 3 content H2s)

## Summary                                  ← MUST be last H2
[3–5 sentence recap]

<RagChatbot context="module-2" />           ← after all prose, NO trailing content
```

### Chapter-Specific H2 Structure

| Chapter | Required H2 Sections (minimum) |
|---|---|
| Ch. 5 — Digital Twin & Gazebo | Learning Objectives; What is a Digital Twin; Gazebo as the Physics Simulation Layer; How Gazebo Connects to ROS 2; [1+ additional]; Summary |
| Ch. 6 — Physics & Collisions | Learning Objectives; What a Gazebo World File Describes; Configuring Gravity and Physics Parameters; Collision Detection in Gazebo; [1+ additional]; Summary |
| Ch. 7 — Unity Rendering | Learning Objectives; Why Gazebo Alone Is Insufficient for High-Fidelity Rendering; How Unity Connects to ROS 2; Use Cases for Unity in a Robotics Pipeline; Gazebo and Unity as Complementary Tools; Summary |
| Ch. 8 — Sensor Simulation | Learning Objectives; How Simulated Sensors Mirror Real Hardware; LiDAR Simulation and the ROS 2 Topic Interface; Depth Camera Simulation and the ROS 2 Topic Interface; IMU Simulation and the ROS 2 Topic Interface; [1+ additional]; Summary |

### Prohibited Content (inherits from Module 1 + Module 2 additions)

- Mathematical equations, derivations, or formulas of any kind
- Physics proofs (friction coefficients, rigid-body dynamics, ray-tracing equations)
- Matrix transformations or tensor mathematics
- Raw HTML (`<div>`, `<span>`, etc.) — use `:::` syntax for admonitions
- Untagged fenced code blocks
- Generic H2 headings without topic qualifiers
- Shell commands for installing Gazebo or Unity (this is a conceptual textbook)
- C++ code (all code examples, if any, MUST be `xml` or `yaml` configuration snippets)

---

## Contract 2: RagChatbot Component Props (Module 2)

**Producer**: This feature / Future backend feature
**Consumer**: MDX chapter files

### Prop Schema (unchanged from Module 1)

```typescript
interface RagChatbotProps {
  context: string;       // Required. Module-scoped Qdrant filter. Value: "module-2"
  placeholder?: string;  // Optional. Default: "Ask about this chapter…"
}
```

### Usage in MDX

```mdx
<RagChatbot context="module-2" />
```

The `context` prop MUST be `"module-2"` for all four chapters in this module. This value is
forwarded by the FastAPI backend as the `chapter_context` filter to scope Qdrant vector
retrieval to Module 2 documents only.

---

## Contract 3: Sidebar Registration (Module 2)

**Producer**: This feature
**Consumer**: Docusaurus routing and navigation

### sidebars.ts Addition

```typescript
// Append inside the tutorialSidebar array, after the Module 1 category:
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

**Doc ID derivation rule**: Docusaurus derives doc IDs from the file path relative to `docs/`,
stripping the `.mdx` extension. Example: `docs/module-2/chapter-5-digital-twin-gazebo.mdx`
→ doc ID `module-2/chapter-5-digital-twin-gazebo`.

---

## Contract 4: Qdrant Chunk Metadata Schema (Module 2)

**Producer**: Downstream RAG ingestion script (out of scope)
**Consumer**: FastAPI `/chat` endpoint

### Metadata Keys

| Key | Source | Example Value |
|---|---|---|
| `module_id` | Directory name (`module-2`) | `"module-2"` |
| `chapter_id` | Filename (no `.mdx`) | `"chapter-5-digital-twin-gazebo"` |
| `section` | H2 heading text | `"How Gazebo Connects to ROS 2"` |
| `content` | Prose between this H2 and next H2 | (prose string) |

### Constraint on Heading Text

H2 heading text becomes the `section` metadata key. It MUST be:
- Unique within a chapter file (no duplicate H2 text)
- Descriptive in isolation (a search engine must understand the topic without surrounding context)
- Topic-qualified (include the subject: `## Gazebo Physics Parameters` not `## Parameters`)

---

## Contract 5: Sensor-to-Topic Mapping (Chapter 8 Required Content)

Chapter 8 MUST accurately represent the following sensor-to-topic table. This is the primary
technical contract for the sensor simulation chapter — the table is verifiable against official
ROS 2 and Gazebo documentation.

| Sensor | ROS 2 Topic | Message Type | Reference in Module 1 |
|---|---|---|---|
| 2D LiDAR | `/scan` (also `/lidar/scan`) | `sensor_msgs/LaserScan` | Ch. 2: example topic `/lidar/scan` |
| Depth Camera (color) | `/camera/image_raw` | `sensor_msgs/Image` | Ch. 2: example topic `/camera/image_raw` |
| Depth Camera (depth) | `/camera/depth/image_raw` | `sensor_msgs/Image` | (new in Module 2) |
| IMU | `/imu/data` | `sensor_msgs/Imu` | (new in Module 2) |
| Odometry | `/odom` | `nav_msgs/Odometry` | Ch. 2: example topic `/odom` |

---

## Versioning

This contract version is `1.0.0` for Module 2. It extends Module 1's content contract (`1.0.0`).

Changes to the RagChatbot prop interface or Qdrant metadata schema that affect already-published
Module 1 content require a constitution amendment. Module 2-only changes only require updating
this document.

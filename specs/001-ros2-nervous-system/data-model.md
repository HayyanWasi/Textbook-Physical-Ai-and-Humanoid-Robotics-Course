# Data Model: Module 1 — The Robotic Nervous System (ROS 2)

**Branch**: `001-ros2-nervous-system` | **Date**: 2026-06-13
**Phase**: 1 — Design

This module is a content feature (static MDX files), not a database-backed feature. The "data
model" here describes the structural schema of content entities and their validation rules —
the same role a database schema plays for a CRUD feature.

---

## Entity 1: Chapter (MDX File)

**Represents**: A single renderable documentation page covering one conceptual ROS 2 topic.

**Required fields** (all must be present for a chapter to pass review):

| Field | Type | Constraint |
|---|---|---|
| `title` (H1) | string | Exactly one H1 per file; format: `Chapter N — [Title]` |
| `## Learning Objectives` | H2 section | MUST be first H2; 3–5 bullet points; each point is a testable outcome |
| Content H2 sections | H2 sections | Minimum 3 distinct H2 sections after Learning Objectives; each heading MUST include chapter topic as qualifier |
| `## Summary` | H2 section | MUST be last H2 before the widget |
| Admonition | MDX block | At least one `:::note`, `:::tip`, or `:::warning` block per file |
| Code blocks | fenced blocks | ALL code/XML blocks MUST include a language tag; no bare triple-backtick blocks |
| RagChatbot widget | JSX element | `<RagChatbot context="module-1" />` MUST appear exactly once, after `## Summary` |
| Word count | integer | Prose words ≤ 3,500 per file |
| Math content | boolean | MUST be `false` — zero equations, zero derivations |

**Instances** (one per chapter in this module):

| ID | File | H1 Title |
|---|---|---|
| `ch01` | `docs/module-1/chapter-1-middleware.mdx` | Chapter 1 — The Need for Robotic Middleware |
| `ch02` | `docs/module-1/chapter-2-nodes-topics.mdx` | Chapter 2 — Nodes, Topics, and Services |
| `ch03` | `docs/module-1/chapter-3-rclpy.mdx` | Chapter 3 — Connecting the AI Brain with rclpy |
| `ch04` | `docs/module-1/chapter-4-urdf.mdx` | Chapter 4 — Defining the Physical Form with URDF |

---

## Entity 2: Module (Sidebar Category)

**Represents**: A named group of four chapters listed together in the Docusaurus sidebar.

| Field | Type | Constraint |
|---|---|---|
| `label` | string | `"Module 1: The Robotic Nervous System"` — exact string |
| `items` | string[] | Array of 4 Docusaurus doc IDs, ordered ch01 → ch04 |
| `type` | string | `"category"` |

**Doc ID format**: `module-1/chapter-N-slug` (relative to `docs/`, no `.mdx` extension).

---

## Entity 3: RagChatbot Component

**Represents**: The React component embedded at the bottom of each chapter that routes student
questions to the FastAPI RAG backend.

| Field | Type | Constraint |
|---|---|---|
| `context` | string (prop) | REQUIRED. Value for Module 1: `"module-1"`. Passed to backend as Qdrant metadata filter. |
| `placeholder` | string (prop) | OPTIONAL. Default: `"Ask about this chapter…"` |

**State**: The stub component is stateless. The full implementation will hold `messages[]`,
`loading` boolean, and `error` string in local React state (out of scope for this feature).

---

## Entity 4: Heading Chunk (RAG Retrieval Unit)

**Represents**: The semantic unit that the Qdrant chunking script extracts from each chapter.
Not stored in the MDX files directly — derived at ingestion time.

| Field | Type | Constraint |
|---|---|---|
| `chapter_id` | string | e.g., `"module-1/chapter-1-middleware"` — used as Qdrant metadata filter |
| `heading` | string | The H2 text that opened this chunk |
| `content` | string | All prose between this H2 and the next H2 |
| `module_id` | string | `"module-1"` — top-level Qdrant filter for the widget's `context` prop |

**Validation rules**:
- `heading` MUST NOT be a single generic word (e.g., `"Introduction"` alone is invalid).
- Each chapter MUST produce ≥ 3 content chunks (Learning Objectives and Summary count as
  metadata; content sections count as retrievable chunks).

---

## State Transitions

This is a content feature; there are no runtime state machines. The authoring lifecycle is:

```
[Draft MDX] → [Review: word count + math check] → [Build check: npm run build] → [Merged]
```

Each chapter transitions independently. A chapter can be merged before the next one is drafted.

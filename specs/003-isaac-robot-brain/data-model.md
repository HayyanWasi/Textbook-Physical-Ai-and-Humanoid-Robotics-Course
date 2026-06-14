# Data Model: Module 3 — The AI-Robot Brain (NVIDIA Isaac™)

**Branch**: `003-isaac-robot-brain` | **Date**: 2026-06-14

This module produces static content, not a data-driven application. The "data model" here
describes the **content schema** — the structural contract each chapter file must satisfy.

## Content Entity: Module 3 Chapter

A Module 3 Chapter is an MDX document that teaches one conceptual area of the NVIDIA Isaac
ecosystem. It is the primary deliverable of this feature.

### Required Fields (Frontmatter)

| Field | Type | Constraint |
|---|---|---|
| `title` | string | Format: `"Chapter N — [Title]"` where N ∈ {9, 10, 11, 12} |

### Required Structure (File Body)

| Element | Type | Position | Constraint |
|---|---|---|---|
| RagChatbot import | MDX import statement | Line 1 after frontmatter | `import RagChatbot from '@site/src/components/RagChatbot';` |
| H1 title | Markdown heading | First content line | Must match frontmatter `title` value |
| `## Learning Objectives` | H2 section | First H2 | Must contain 3–5 bullet points as testable outcomes |
| Content H2 sections | H2 sections | After Learning Objectives | 3–4 sections; each heading must be self-describing (topic-qualified, not generic) |
| At least one admonition | Docusaurus admonition block | Anywhere in content | `:::note`, `:::tip`, or `:::warning` |
| `## Summary` | H2 section | Final H2 before component | 3–5 sentence recap of the chapter |
| RagChatbot component | JSX component | Final line of file | `<RagChatbot context="module-3" />` |

### Prohibited Content

| Prohibited Element | Applies To | Requirement Source |
|---|---|---|
| CUDA code snippets | All chapters | FR-008 |
| Matrix notation (e.g., `A = ...`, `Σ`, `J`) | All chapters | FR-004, FR-008 |
| Algorithm pseudocode | All chapters | FR-004 |
| GPU architecture internals | All chapters | FR-008 |
| Terms: "matrix", "Jacobian", "covariance", "Kalman", "eigenvalue" | Chapter 11 | FR-004, Research Q5 |

### Word Count Constraint

| Measure | Limit |
|---|---|
| Prose words per chapter | ≤ 3,500 |
| Total file size (including frontmatter + code) | ≤ 4,500 words equivalent |

---

## Content Entity: Sidebar Category (Module 3)

The sidebar category is the navigation entry that surfaces all four chapters to readers.

| Field | Value | Constraint |
|---|---|---|
| `type` | `'category'` | Must match Docusaurus `SidebarsConfig` type |
| `label` | `'Module 3: The AI-Robot Brain'` | Displayed in sidebar UI |
| `collapsed` | `false` | Chapters visible by default, matching Module 1 and 2 behaviour |
| `items` | Array of 4 doc IDs | Order: ch09, ch10, ch11, ch12 |

Doc ID format: `'module-3/chapter-N-slug'` (no `.mdx` extension, relative to `frontend/docs/`).

---

## Content Entity: Gazebo vs. Isaac Sim Comparison (Chapter 10 Artefact)

This is the mandatory disambiguation section in Chapter 10. It must be independently
retrievable by the RAG knowledge base.

| Attribute | Value |
|---|---|
| H2 heading | `## Gazebo vs. Isaac Sim: A Direct Comparison` |
| Placement | Standalone H2 — not nested inside another section |
| Required content | Side-by-side contrast of: primary purpose, input data type, output, typical use case |
| Format | Comparison table OR two clearly labelled sub-sections (`### Gazebo` / `### Isaac Sim`) |

---

## Chapter-to-Concept Mapping

Defines the semantic boundaries that prevent RAG chunk contamination across chapters.

| Chapter | Owns These Concepts | Must NOT Cover These Concepts |
|---|---|---|
| 9 | Perception gap, sensor limitations, Isaac ecosystem overview, tool introductions | Synthetic data generation details, VSLAM derivations, Nav2 internals |
| 10 | Synthetic data, sim-to-real gap, photorealistic simulation, Gazebo vs. Isaac Sim | VSLAM, Nav2, gait planning |
| 11 | Visual SLAM (conceptual), landmarks, loop closure, map building | Synthetic data, Nav2 path planning, balance constraints |
| 12 | Bipedal path planning, Nav2, balance constraints, footstep placement, full pipeline recap | VSLAM internals, synthetic data, GPU details |

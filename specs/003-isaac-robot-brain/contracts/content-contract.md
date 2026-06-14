# Content Contract: Module 3 — The AI-Robot Brain (NVIDIA Isaac™)

**Branch**: `003-isaac-robot-brain` | **Date**: 2026-06-14
**Type**: Content + Component Interface Contract

---

## 1. RagChatbot Component Contract

The `RagChatbot` component is already implemented at `frontend/src/components/RagChatbot.jsx`.
This contract defines how Module 3 chapters MUST use it.

### Props

| Prop | Type | Required | Module 3 Value | Description |
|---|---|---|---|---|
| `context` | `string` | **Yes** | `"module-3"` | Scopes the RAG retrieval to Module 3 chunks in the vector store |
| `placeholder` | `string` | No | (use default) | Hint text shown inside the chat input field |

### Usage in MDX

```mdx
import RagChatbot from '@site/src/components/RagChatbot';

{/* ... chapter content ... */}

<RagChatbot context="module-3" />
```

### Placement Rule

The component MUST appear as the **final line** of every Module 3 chapter file, after the
`## Summary` section. It MUST NOT appear mid-chapter (breaks RAG chunking) or before the
Summary (breaks reading flow).

### Context Attribute Integrity

The `context` prop MUST be exactly `"module-3"` — no trailing whitespace, no uppercase, no
version suffix. Deviation causes the RAG backend to route queries to an unscoped index.

---

## 2. Chapter File Contract

### File Naming

| Chapter | File Name | Docusaurus Doc ID |
|---|---|---|
| 9 | `chapter-9-advanced-perception.mdx` | `module-3/chapter-9-advanced-perception` |
| 10 | `chapter-10-isaac-sim-synthetic-data.mdx` | `module-3/chapter-10-isaac-sim-synthetic-data` |
| 11 | `chapter-11-isaac-ros-vslam.mdx` | `module-3/chapter-11-isaac-ros-vslam` |
| 12 | `chapter-12-nav2-bipedal-planning.mdx` | `module-3/chapter-12-nav2-bipedal-planning` |

### File Location

All four files reside at `frontend/docs/module-3/`.

### Heading Hierarchy Contract

```
H1  — One per file. Matches frontmatter title.
H2  — Major concept sections. Must be self-describing (topic-qualified).
H3  — Sub-sections within a major concept. Optional.
H4+ — Prohibited. Degrades RAG chunk quality.
```

### Frontmatter Contract

```yaml
---
title: "Chapter N — [Title]"
---
```

No additional frontmatter fields are required. Do not add `sidebar_position` (ordering is
controlled by `sidebars.ts`).

---

## 3. Sidebar Contract

### File Location

`frontend/sidebars.ts`

### Addition (append to `tutorialSidebar` array)

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

### Non-Regression Rule

The existing Module 1 and Module 2 category objects in `sidebars.ts` MUST NOT be modified.
This is an additive-only change.

---

## 4. RAG Chunking Contract

The Qdrant chunking pipeline splits documents on `##` H2 headings. The following constraints
ensure each chunk is semantically distinct and independently retrievable.

| Rule | Constraint |
|---|---|
| Minimum H2 sections per chapter | 5 (Learning Objectives + 3 content + Summary) |
| H2 heading specificity | Must be topic-qualified (e.g., `## Gazebo vs. Isaac Sim: A Direct Comparison`, not `## Comparison`) |
| Cross-concept bleed | A chunk must not contain substantive discussion of concepts owned by another chapter (see data-model.md chapter-to-concept mapping) |
| Chapter 10 disambiguation chunk | `## Gazebo vs. Isaac Sim: A Direct Comparison` MUST be a standalone H2 |
| Chapter 11 math-free guarantee | Sections `## Building the Map Step by Step` and `## Loop Closure` must contain zero mathematical notation |

---

## 5. Content Quality Contract

### Mandatory Inclusions (per chapter)

- [ ] At least one Docusaurus admonition (`:::note`, `:::tip`, or `:::warning`)
- [ ] `## Learning Objectives` as first H2 with 3–5 testable bullets
- [ ] `## Summary` as last H2 before the RagChatbot component
- [ ] Prerequisite callout naming Module 1 and/or Module 2 concepts assumed

### Mandatory Exclusions (all chapters)

- [ ] No CUDA code blocks
- [ ] No matrix/tensor notation
- [ ] No algorithm pseudocode
- [ ] No terms: "CUDA core", "GPU kernel", "tensor", "gradient descent" (in non-quoted context)
- [ ] No terms in Chapter 11: "matrix", "Jacobian", "covariance", "Kalman", "eigenvalue"

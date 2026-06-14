# Content Contract: Module 1 — The Robotic Nervous System (ROS 2)

**Branch**: `001-ros2-nervous-system` | **Date**: 2026-06-13
**Phase**: 1 — Design

This contract defines the interface between the static MDX content layer (Docusaurus) and the
downstream systems that consume it: the RAG ingestion pipeline (Qdrant) and the chat widget
(FastAPI backend).

---

## Contract 1: Chapter MDX File Structure

**Producer**: Content author (this feature)
**Consumer**: Docusaurus build system; Qdrant chunking script

### Required File Header

```mdx
---
id: chapter-N-slug
title: "Chapter N — [Full Title]"
sidebar_position: N
---
```

The `id` field MUST match the Docusaurus doc ID used in `sidebars.js`.
The `sidebar_position` field controls ordering within the Module 1 category (1–4).

### Required Internal Structure

```
# Chapter N — [Title]                    ← exactly one H1

## Learning Objectives                   ← MUST be first H2
- After reading this chapter, you will understand [X]
- After reading this chapter, you will be able to [Y]
(3–5 bullets, each a complete testable outcome)

## [Section A — Self-Describing Heading] ← content H2
[prose + optional :::admonition]

## [Section B — Self-Describing Heading] ← content H2
[prose + optional code block with language tag]

## [Section C — Optional Additional Section] ← content H2

## Summary                               ← MUST be last H2
[3–5 sentence recap of key concepts]

<RagChatbot context="module-1" />        ← after all prose, NO trailing content
```

### Prohibited Content

- Mathematical equations, derivations, or formulas of any kind
- C++ code snippets
- `colcon build`, `ros2 run`, or workspace setup shell commands
- Raw HTML (`<div>`, `<span>`, etc.) — Docusaurus admonitions MUST use `:::` syntax
- Untagged fenced code blocks (` ``` ` without a language identifier)
- Generic H2 headings (e.g., `## Introduction` without a topic qualifier)

---

## Contract 2: RagChatbot Component Props

**Producer**: This feature (stub) / Future backend feature (full implementation)
**Consumer**: MDX chapter files (as a JSX element)

### Prop Schema

```typescript
interface RagChatbotProps {
  context: string;       // Required. Qdrant metadata filter key. Value: "module-1"
  placeholder?: string;  // Optional. Input placeholder text. Default: "Ask about this chapter…"
}
```

### Usage in MDX

```mdx
<RagChatbot context="module-1" />
```

The `context` prop MUST always be `"module-1"` for all four chapters in this module.
The prop value is passed as-is to the FastAPI `/chat` endpoint as the `chapter_context`
request field, which the backend uses to pre-filter Qdrant results to this module's vectors.

### Error Handling (stub)

The stub component MUST NOT throw; it MUST render a visible placeholder even when the backend
is unavailable. The full component's error handling is defined in the backend feature contract
(out of scope here).

---

## Contract 3: Sidebar Registration

**Producer**: This feature
**Consumer**: Docusaurus routing and navigation

### sidebars.js Addition

```js
// Add to the sidebarItems array in sidebars.js
{
  type: 'category',
  label: 'Module 1: The Robotic Nervous System',
  collapsed: false,
  items: [
    'module-1/chapter-1-middleware',
    'module-1/chapter-2-nodes-topics',
    'module-1/chapter-3-rclpy',
    'module-1/chapter-4-urdf',
  ],
},
```

**Doc ID derivation rule**: Docusaurus derives doc IDs from file path relative to `docs/`,
stripping the `.mdx` extension. Verify with the `id` frontmatter field if using custom IDs.

---

## Contract 4: Qdrant Chunk Metadata Schema

**Producer**: Downstream RAG ingestion script (out of scope — defined here as a constraint)
**Consumer**: FastAPI `/chat` endpoint (uses `module_id` and `chapter_id` to filter)

This contract defines what the MDX files MUST provide to enable correct downstream chunking.
The ingestion script is not written in this feature; this contract is a constraint on content
structure.

### Metadata Keys (set at ingestion time from file structure)

| Key | Source | Example Value |
|---|---|---|
| `module_id` | Derived from directory name (`module-1`) | `"module-1"` |
| `chapter_id` | Derived from filename | `"chapter-1-middleware"` |
| `section` | H2 heading text | `"The Hardware Abstraction Problem in Robotics"` |
| `content` | Text between this H2 and the next H2 | (prose string) |

### Constraint on Heading Text

H2 heading text becomes the `section` metadata value. It MUST be unique within a chapter
(no two H2s in the same file may have identical text) and MUST be descriptive enough for
semantic search without surrounding context.

---

## Versioning

This contract version is `1.0.0`. It governs Module 1 content only. Module 2–4 contracts
will extend this with their respective `context` prop values (`"module-2"`, etc.).

Changes to the `RagChatbot` prop interface or the Qdrant metadata schema require a
constitution amendment if they affect Module 1 content already published.

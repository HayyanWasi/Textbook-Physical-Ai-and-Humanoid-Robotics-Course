# Implementation Plan: Module 3 — The AI-Robot Brain (NVIDIA Isaac™)

**Branch**: `003-isaac-robot-brain` | **Date**: 2026-06-14 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-isaac-robot-brain/spec.md`

## Summary

Produce four MDX chapter files for Docusaurus (Module 3: NVIDIA Isaac) that frame the Isaac
ecosystem as the robot's "Visual Cortex and Navigation Center." All content is conceptual — zero
matrix algebra, zero CUDA code. Chapter 10 contains a mandatory Gazebo vs. Isaac Sim
disambiguation section. Each file imports the existing `RagChatbot` component and sets
`context="module-3"`. The `frontend/sidebars.ts` sidebar config is extended with a Module 3
category linking Chapters 9–12.

## Technical Context

**Language/Version**: MDX 3.x (Docusaurus v3, TypeScript config) + React 18 (RagChatbot stub)
**Primary Dependencies**: Docusaurus v3, React 18, per-file MDX import of `RagChatbot`
**Storage**: N/A — static content; Qdrant vector store is downstream (separate chunking pipeline)
**Testing**: Manual Docusaurus build (`npm run build` in `frontend/`), word-count check per chapter, manual math/CUDA content review
**Target Platform**: GitHub Pages (static); local dev via `npm start` inside `frontend/`
**Project Type**: Web (frontend static site — decoupled from backend per constitution)
**Performance Goals**: Docusaurus build completes in under 60 seconds for all module-3 pages
**Constraints**: ≤3,500 prose words per chapter; zero math derivations; zero CUDA references; all `##` headings self-describing for RAG chunking
**Scale/Scope**: 4 MDX files, 1 sidebar update (`frontend/sidebars.ts`), zero new components

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Gate | Status |
|---|---|---|
| Strict Decoupling | MDX chapter files MUST NOT contain any API calls, LLM SDK imports, or direct Qdrant references | ✅ PASS — chapters are static prose; `RagChatbot` delegates all backend calls |
| Context-Bound RAG | The `<RagChatbot>` component MUST receive `context="module-3"` on every chapter page | ✅ PASS — FR-006 requires this on all four chapters |
| API Gateway Pattern | MDX files MUST NOT import any LLM SDK or vector-search client | ✅ PASS — only `RagChatbot.jsx` is imported, which calls the backend gateway |
| Content Quality: No Math | Zero matrix notation, pseudocode, or algorithm derivations in any chapter | ✅ PASS — FR-004 (Chapter 11 VSLAM), FR-008 (all chapters) prohibit this |
| Content Quality: No CUDA | Zero CUDA code snippets or GPU architecture internals | ✅ PASS — FR-008 explicitly prohibits this |
| Content Quality: Gazebo Disambiguation | Chapter 10 MUST contain a clearly labeled Gazebo vs. Isaac Sim comparison section | ✅ PASS — FR-003 mandates this; failure point tracked in SC-001 |
| Content Quality: Structure | Exactly 4 chapters under Module 3; all `##` headings self-describing | ✅ PASS — FR-001, FR-007 enforce this |
| Sidebar Extension | `frontend/sidebars.ts` MUST be extended (not replaced) to preserve Modules 1 and 2 | ✅ PASS — additive change only |
| Workflow: Paced Execution | Plan generated first, awaiting approval before content generation begins | ✅ PASS |

**Post-design re-check**: All gates pass. No constitution violations. No Complexity Tracking entries required.

## Project Structure

### Documentation (this feature)

```text
specs/003-isaac-robot-brain/
├── plan.md              ← This file
├── research.md          ← Phase 0 output
├── data-model.md        ← Phase 1 output
├── quickstart.md        ← Phase 1 output
├── contracts/
│   └── content-contract.md   ← Phase 1 output
└── tasks.md             ← Phase 2 output (/sp.tasks — NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/
├── docs/
│   ├── module-1/              ← existing, DO NOT TOUCH
│   ├── module-2/              ← existing, DO NOT TOUCH
│   └── module-3/              ← NEW
│       ├── chapter-9-advanced-perception.mdx
│       ├── chapter-10-isaac-sim-synthetic-data.mdx
│       ├── chapter-11-isaac-ros-vslam.mdx
│       └── chapter-12-nav2-bipedal-planning.mdx
├── src/
│   └── components/
│       └── RagChatbot.jsx     ← existing stub, no changes needed
└── sidebars.ts                ← additive update to add Module 3 category
```

**Structure Decision**: Mirrors the established Module 1 and 2 layout exactly. `frontend/` is
the Docusaurus root. `RagChatbot.jsx` already exists as a stub — no new components required.
The sidebar file is `frontend/sidebars.ts` (TypeScript, not JS as in Module 1's plan — confirmed
by reading the live file).

## Phase 0: Research Findings

*See [research.md](./research.md) for full detail. Key decisions:*

- **RagChatbot import strategy**: Per-file import confirmed (not global registration). Existing
  pattern established in Module 1 and Module 2 chapters — every `.mdx` file opens with
  `import RagChatbot from '@site/src/components/RagChatbot';`. Module 3 follows the same pattern.
- **Sidebar format**: `frontend/sidebars.ts` uses TypeScript-typed manual category definitions.
  Module 3 appended as a third category with explicit `items` array (ch09 → ch12 ordering).
- **Docusaurus doc IDs**: Derived from file path relative to `frontend/docs/` — e.g.,
  `module-3/chapter-9-advanced-perception` (no file extension in the items array).
- **RAG chunking boundary**: `##` H2 headings confirmed as the split boundary. Minimum 5 H2
  sections per chapter: `Learning Objectives`, three or four content sections, `Summary`.
- **Gazebo disambiguation**: Chapter 10 must contain a `## Gazebo vs. Isaac Sim` section as a
  named H2 — not embedded inside another section — so the RAG system can retrieve it as a
  standalone chunk when a student asks "what is the difference between Gazebo and Isaac Sim?"
- **Word count gate**: ≤3,500 prose words per chapter (≤4,500 total including frontmatter).
- **VSLAM constraint**: Chapter 11 must not contain the words "matrix," "Jacobian," "covariance,"
  "eigenvalue," or "Kalman" in any non-quoted context.

## Phase 1: Design

### Content Architecture

Each chapter follows the same internal structure as Modules 1 and 2 to ensure consistency:

```text
---
title: "Chapter N — [Title]"
---

import RagChatbot from '@site/src/components/RagChatbot';

# Chapter N — [Title]                          ← exactly one H1

## Learning Objectives                         ← MUST be first H2
- 3–5 testable outcome bullets

## [Section A — Self-Describing Heading]       ← content H2
prose + :::admonition (at least one per file)

## [Section B — Self-Describing Heading]       ← content H2

## [Section C — Self-Describing Heading]       ← content H2

## [Section D — Self-Describing Heading]       ← optional 4th content H2

## Summary                                     ← MUST be last H2
3–5 sentence recap

<RagChatbot context="module-3" />             ← after all prose, end of file
```

### Chapter Content Plan

| Chapter | File | Core Pedagogical Hook | Key H2 Sections |
|---|---|---|---|
| 9 | `chapter-9-advanced-perception.mdx` | Standard sensors are input devices; perception is understanding — the difference between seeing and knowing | The Perception Gap in Humanoid Robotics; Why Standard Sensors Are Not Enough; The NVIDIA Isaac Ecosystem; Isaac Sim, Isaac ROS, Isaac Lab, and Nav2 Explained; Summary |
| 10 | `chapter-10-isaac-sim-synthetic-data.mdx` | A driving simulator trains your judgment, not your car's physics — Isaac Sim trains the robot's eyes, Gazebo trains its reflexes | Two Simulators, Two Jobs; Gazebo as a Physics Classroom (Module 2 Recap); Isaac Sim as a Perception Training Ground; Gazebo vs. Isaac Sim: A Direct Comparison; The Sim-to-Real Gap and Synthetic Data; Summary |
| 11 | `chapter-11-isaac-ros-vslam.mdx` | Navigating an unfamiliar city by photographing landmarks and building a mental map — with no GPS | What SLAM Means and Why Robots Need It; Using Visual Landmarks Instead of GPS; Building the Map Step by Step; Loop Closure — When the Robot Recognises Where It Has Been; How Isaac ROS cuVSLAM Fits the Bigger Picture; Summary |
| 12 | `chapter-12-nav2-bipedal-planning.mdx` | A tightrope walker plans each step for balance; a car driver plans for speed — same destination, fundamentally different problem | Navigation for Legs Is Not Navigation for Wheels; The Nav2 Stack and Its Role in the Isaac Pipeline; Planning Around Stability Constraints; Footstep-Aware Path Planning; The Full Pipeline: From Camera Input to Footstep Decision; Summary |

### RagChatbot Component Interface

Defined fully in [contracts/content-contract.md](./contracts/content-contract.md).

| Prop | Type | Required | Value for Module 3 |
|---|---|---|---|
| `context` | string | Yes | `"module-3"` |
| `placeholder` | string | No | `"Ask about this chapter…"` |

### Sidebar Addition

```typescript
// frontend/sidebars.ts — append inside tutorialSidebar array
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

## Complexity Tracking

> No constitution violations were identified. This section is intentionally empty.

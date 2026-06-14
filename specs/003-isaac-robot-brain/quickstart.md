# Quickstart: Module 3 — The AI-Robot Brain (NVIDIA Isaac™)

**Branch**: `003-isaac-robot-brain` | **Date**: 2026-06-14

## Prerequisites

- Node.js ≥ 18 installed
- `frontend/` dependencies installed: `cd frontend && npm install`
- You are on branch `003-isaac-robot-brain`
- Module 1 and Module 2 chapters already exist in `frontend/docs/`

## Step 1: Create the Module 3 Directory

```bash
mkdir -p frontend/docs/module-3
```

## Step 2: Verify the RagChatbot Component Exists

```bash
ls frontend/src/components/RagChatbot.jsx
```

Expected output: the file path. If missing, the build will fail for all four chapters.

## Step 3: Write Each Chapter File

Each file at `frontend/docs/module-3/chapter-N-*.mdx` must follow this skeleton:

```mdx
---
title: "Chapter N — [Title]"
---

import RagChatbot from '@site/src/components/RagChatbot';

# Chapter N — [Title]

## Learning Objectives

- [3–5 testable outcome bullets]

## [Section A]

[prose]

:::note
[At least one admonition per file]
:::

## [Section B]

[prose]

## [Section C]

[prose]

## Summary

[3–5 sentence recap]

<RagChatbot context="module-3" />
```

See [contracts/content-contract.md](./contracts/content-contract.md) for prohibited content
rules and heading constraints.

## Step 4: Update the Sidebar

Open `frontend/sidebars.ts` and append the Module 3 category inside `tutorialSidebar`:

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

Do not modify the Module 1 or Module 2 entries.

## Step 5: Run the Local Dev Server

```bash
cd frontend && npm start
```

Navigate to `http://localhost:3000` and verify:
- "Module 3: The AI-Robot Brain" appears in the sidebar
- All four chapters are accessible via the sidebar links
- Each chapter displays the RagChatbot stub at the bottom

## Step 6: Verify the Production Build

```bash
cd frontend && npm run build
```

Expected: build completes with zero errors. Any broken MDX import or malformed frontmatter
will surface here.

## Step 7: Content Quality Checks

Run these checks manually before considering a chapter complete:

```bash
# Word count per chapter (should be ≤ 3,500 prose words)
wc -w frontend/docs/module-3/chapter-9-advanced-perception.mdx
wc -w frontend/docs/module-3/chapter-10-isaac-sim-synthetic-data.mdx
wc -w frontend/docs/module-3/chapter-11-isaac-ros-vslam.mdx
wc -w frontend/docs/module-3/chapter-12-nav2-bipedal-planning.mdx

# Check for prohibited terms in Chapter 11
grep -in "matrix\|jacobian\|covariance\|kalman\|eigenvalue" \
  frontend/docs/module-3/chapter-11-isaac-ros-vslam.mdx

# Check for CUDA references in any chapter
grep -in "cuda\|gpu kernel\|tensor" frontend/docs/module-3/

# Verify RagChatbot context attribute on all chapters
grep -h "RagChatbot" frontend/docs/module-3/*.mdx
# Expected: <RagChatbot context="module-3" /> on each line
```

## Rollback

If any chapter fails quality checks, delete only the affected file — the other chapters and
the sidebar update are independent. The `frontend/docs/module-3/` directory is isolated from
Modules 1 and 2.

```bash
# Remove only a specific chapter if needed
rm frontend/docs/module-3/chapter-11-isaac-ros-vslam.mdx
```

Revert the sidebar entry only if all four chapters are being rolled back.

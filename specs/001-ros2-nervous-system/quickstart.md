# Quickstart: Module 1 — The Robotic Nervous System (ROS 2)

**Branch**: `001-ros2-nervous-system` | **Date**: 2026-06-13

This quickstart covers how to write, validate, and integrate a new chapter for Module 1 into
the Docusaurus site.

---

## Prerequisites

- Node.js 18+ installed
- Docusaurus project initialized at repository root (or `website/` if using monorepo layout)
- `npm install` completed in the Docusaurus root

---

## Step 1: Create the Chapter File

Create a new `.mdx` file in `docs/module-1/`:

```bash
touch docs/module-1/chapter-N-slug.mdx
```

Open it and add the required frontmatter header:

```mdx
---
id: chapter-N-slug
title: "Chapter N — Your Title Here"
sidebar_position: N
---
```

---

## Step 2: Follow the Chapter Structure

Every chapter MUST open with an H1 that matches the `title` frontmatter, followed immediately
by the `## Learning Objectives` section:

```mdx
# Chapter N — Your Title Here

## Learning Objectives

After completing this chapter, you will:

- Understand [concept A] and why it matters for physical AI systems
- Be able to describe [concept B] using the Nervous System analogy
- Distinguish between [X] and [Y] without referencing any mathematical derivations
```

Add your content sections. Each H2 MUST be self-describing:

```mdx
## The [Topic] Problem in Robotics

[Prose. Use the Nervous System analogy. No equations.]

:::tip Key Insight
[One key takeaway that a student should remember from this section.]
:::

## How ROS 2 Solves [Topic]

[Prose. Architectural explanation only.]
```

Close with a summary and the widget:

```mdx
## Summary

[3–5 sentences recapping the chapter's key architectural concepts.]

<RagChatbot context="module-1" />
```

---

## Step 3: Add Tagged Code Blocks

If including Python or XML examples, always tag the language:

```mdx
\`\`\`python
# This is a conceptual example — not a runnable script
class SensorNode:
    """Represents a ROS 2 Node that reads sensor data."""
    def __init__(self):
        self.topic = "/sensor_data"  # The Topic this node publishes to
\`\`\`
```

**Never** use an untagged fenced block (` ``` ` alone). The Docusaurus build will succeed but
RAG chunking quality degrades for untagged blocks.

---

## Step 4: Validate Word Count

Before committing, check the prose word count:

```bash
# Rough check — includes code block words; keep total under 4,500
wc -w docs/module-1/chapter-N-slug.mdx
```

Target: ≤3,500 prose words. If over, remove filler and redundant restatements — do not add
a new summary section.

---

## Step 5: Check for Math Content

Scan the file for any mathematical notation:

```bash
# Flag any LaTeX or equation-like patterns
grep -n '\\[\\|\\$\\|\\\\frac\\|\\\\sum\\|\\\\int' docs/module-1/chapter-N-slug.mdx
```

If any matches found, rewrite those sections as architectural prose before proceeding.

---

## Step 6: Update sidebars.js

Open `sidebars.js` and add the new chapter's doc ID to the Module 1 category:

```js
{
  type: 'category',
  label: 'Module 1: The Robotic Nervous System',
  collapsed: false,
  items: [
    'module-1/chapter-1-middleware',      // existing
    'module-1/chapter-2-nodes-topics',    // existing
    'module-1/chapter-3-rclpy',           // existing
    'module-1/chapter-4-urdf',            // add new chapters here
  ],
},
```

---

## Step 7: Verify the Build

Run the local Docusaurus build to catch broken links, MDX parse errors, and missing imports:

```bash
npm run build
```

A successful build outputs zero errors and zero broken-link warnings for the new chapter.
If the `<RagChatbot>` component is not yet registered globally, ensure the stub exists at
`src/components/RagChatbot.jsx` before running the build.

---

## Step 8: Commit

Commit the chapter (and only the chapter) after the build passes:

```bash
git add docs/module-1/chapter-N-slug.mdx sidebars.js
git commit -m "content(ch0N): add Chapter N — [Title]"
```

---

## RagChatbot Global Registration (one-time setup)

If `<RagChatbot>` is not yet globally registered in Docusaurus, add it to
`docusaurus.config.js`:

```js
// docusaurus.config.js
const config = {
  // ...
  themes: [
    // ...
  ],
  // Option A: Use MDX global components (Docusaurus v3)
  // Wrap in a custom theme component or use swizzling
};
```

Alternatively, confirm with the platform team whether the component should be auto-imported
via a remark plugin or registered as a global MDX component. Until confirmed, the per-file
import approach works:

```mdx
import RagChatbot from '@site/src/components/RagChatbot';
```

Add this import line at the top of each chapter file if global registration is not yet set up.

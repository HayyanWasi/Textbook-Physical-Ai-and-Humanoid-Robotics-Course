# Quickstart: Module 2 — The Digital Twin (Gazebo & Unity)

**Branch**: `002-digital-twin` | **Date**: 2026-06-13

This quickstart covers how to write, validate, and integrate a new chapter for Module 2 into
the Docusaurus site. It extends the Module 1 quickstart with Module 2-specific conventions.

---

## Prerequisites

- Node.js 18+ installed; `npm install` completed in `frontend/`
- Module 1 implementation complete (RagChatbot stub exists at `frontend/src/components/RagChatbot.jsx`)
- `frontend/sidebars.ts` contains the Module 1 category (confirmed present)
- Working directory: `frontend/` for all build commands

---

## Step 1: Create the Module 2 Directory and Chapter File

```bash
mkdir -p frontend/docs/module-2
touch frontend/docs/module-2/chapter-N-slug.mdx
```

Open the file and add the required header:

```mdx
---
title: "Chapter N — Your Title Here"
---

import RagChatbot from '@site/src/components/RagChatbot';

# Chapter N — Your Title Here
```

---

## Step 2: Follow the Chapter Structure

Every chapter MUST open with an H1, then immediately the Learning Objectives H2 (exactly 4 bullets):

```mdx
## Learning Objectives

After completing this chapter, you will be able to:

- Explain what [concept A] is and how it differs from [adjacent concept]
- Describe [concept B] using the [analogy] framing from this module
- Identify [technical element] and explain what it controls
- Connect [Module 2 concept] to the ROS 2 communication graph from Module 1
```

Add content sections. All H2 headings MUST be topic-qualified:

```mdx
## What a Digital Twin Provides That a CAD Model Cannot

[Prose. Conceptual framing only. No physics equations.]

:::note
[Key insight the student should retain from this section.]
:::

## How Gazebo Connects to the ROS 2 Graph

[Prose. Reference the topics introduced in Module 1 (e.g., /lidar/scan).]
```

Close with Summary and widget:

```mdx
## Summary

[3–5 sentences. Cover: key concept → core analogy → connection to prior/next chapter.]

<RagChatbot context="module-2" />
```

---

## Step 3: Configuration and Code Block Tags

When showing Gazebo SDF/world configuration snippets, always tag the language:

```mdx
\`\`\`xml
<world name="simulation_world">
  <gravity>0 0 -9.8</gravity>
  <!-- Earth-standard gravity: 9.8 m/s² downward -->
</world>
\`\`\`
```

For YAML (e.g., ROS 2 parameter files):

```mdx
\`\`\`yaml
# ros2_control configuration example
robot_description:
  ros__parameters:
    use_sim_time: true
\`\`\`
```

**Never** use untagged fenced blocks. Acceptable tags: `xml`, `yaml`, `python`. No `bash`
installation commands in chapter content.

---

## Step 4: Chapter-Specific Authoring Notes

### Chapter 5 — Digital Twin & Gazebo
- Lead with the "shadow clone" or "test dummy" analogy before introducing the technical definition.
- Explicitly state that Gazebo owns physics (not Unity) in the opening framing.
- Briefly re-anchor the ROS 2 topic/node concept from Module 1 for students who may have skipped it.

### Chapter 6 — Physics & Collisions
- Introduce SDF (Simulation Description Format) as the Gazebo world format — distinct from URDF.
- Show the `<gravity>` element with a plain-English explanation. Do NOT derive acceleration.
- Explain collision geometry primitives (boxes, cylinders, spheres) using the Module 1 "mesh vs
  simplified shape" analogy from Chapter 4.

### Chapter 7 — Unity Rendering
- The single most important sentence in this chapter: "Gazebo simulates physics; Unity renders the world."
- Explain the ROS–Unity bridge (Unity Robotics Hub / ROS-TCP-Connector) at the architecture level
  — student does not need to install or configure it.
- Name at least one specific use case that requires Unity (photorealistic visual training datasets,
  human avatar HRI testing).

### Chapter 8 — Sensor Simulation
- Include the full sensor-to-topic mapping table (at minimum: LiDAR, depth camera, IMU).
- Cross-reference topic names that appeared in Module 1 Chapter 2 (`/camera/image_raw`, `/lidar/scan`,
  `/odom`) to reinforce the "identical interface" principle.
- The key teaching point: a perception Node subscribed to `/lidar/scan` cannot distinguish simulated
  data from real sensor data — the ROS 2 message type is identical.

---

## Step 5: Validate Word Count

```bash
# From repo root — rough total word count (includes code blocks)
wc -w frontend/docs/module-2/chapter-N-slug.mdx
```

Target: prose words ≤ 3,500. Total file words (including code) should stay under 4,500.

---

## Step 6: Math Content Scan

```bash
grep -n -E '\$|\\\[|\\\]|\\\\frac|\\\\theta|\\\\sum|D-H|Denavit|inertia tensor math' \
  frontend/docs/module-2/chapter-N-slug.mdx
```

Zero matches required before committing. If any match found, rewrite that section as prose.

---

## Step 7: Admonition Count Check

Each chapter MUST have at least 2 admonitions. Verify:

```bash
grep -c ':::' frontend/docs/module-2/chapter-N-slug.mdx
```

Minimum count: 4 (each `:::type` opens and `::: ` closes — two admonitions = 4 lines).

---

## Step 8: Update sidebars.ts

Open `frontend/sidebars.ts` and append the Module 2 category after Module 1:

```typescript
import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
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
  ],
};

export default sidebars;
```

---

## Step 9: Verify the Build

```bash
cd frontend && npm run build
```

Zero errors and zero broken-link warnings required. Common failure modes:
- Missing `import RagChatbot` at top of file → add the import line
- Doc ID in `sidebars.ts` doesn't match filename → verify spelling matches exactly
- Untagged code block → add language tag

---

## Step 10: Commit

Commit each chapter separately after its build passes:

```bash
git add frontend/docs/module-2/chapter-N-slug.mdx
git commit -m "content(ch0N): add Chapter N — [Title]"
```

Commit the sidebar update separately or with the final chapter:

```bash
git add frontend/sidebars.ts
git commit -m "feat(module-2): add Module 2 sidebar category"
```

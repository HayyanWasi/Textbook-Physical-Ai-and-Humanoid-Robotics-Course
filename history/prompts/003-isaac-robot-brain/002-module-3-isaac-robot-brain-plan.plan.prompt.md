---
id: "002"
title: "Module 3 Isaac Robot Brain Plan"
stage: plan
date: 2026-06-14
surface: agent
model: claude-sonnet-4-6
feature: 003-isaac-robot-brain
branch: 003-isaac-robot-brain
user: HayyanWasi
command: /sp.plan
labels: ["module-3", "isaac", "nvidia", "plan", "docusaurus", "rag", "nav2", "vslam"]
links:
  spec: specs/003-isaac-robot-brain/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-isaac-robot-brain/plan.md
  - specs/003-isaac-robot-brain/research.md
  - specs/003-isaac-robot-brain/data-model.md
  - specs/003-isaac-robot-brain/quickstart.md
  - specs/003-isaac-robot-brain/contracts/content-contract.md
tests:
  - Constitution check — 9/9 gates PASS
  - Research Q1-Q6 all resolved
---

## Prompt

/sp.plan (no additional arguments — runs against current branch 003-isaac-robot-brain)

## Response snapshot

Generated full Phase 0 + Phase 1 planning artifacts for Module 3:

- **plan.md**: Technical context confirmed (MDX 3.x, Docusaurus v3 TypeScript config, per-file RagChatbot import). Constitution check: 9/9 gates pass. Chapter content plan for Ch9–12 with core pedagogical hooks and H2 section outlines. Sidebar TypeScript addition documented.
- **research.md**: 6 research questions resolved — RagChatbot import strategy (per-file, not global), sidebars.ts TypeScript format confirmed, Gazebo disambiguation as standalone H2 required, VSLAM prohibited-term list established, bipedal navigation three-constraint frame documented.
- **data-model.md**: Content schema for Module 3 Chapter entity (required frontmatter, required structure, prohibited content, word count limits). Chapter-to-concept ownership mapping for RAG semantic boundaries. Gazebo vs. Isaac Sim comparison artefact defined.
- **contracts/content-contract.md**: RagChatbot prop contract (`context="module-3"`, placement rule, integrity constraint). File naming and doc ID contract. Sidebar addition contract. RAG chunking contract. Content quality checklist.
- **quickstart.md**: Step-by-step developer guide covering directory creation, chapter skeleton, sidebar update, dev server verification, production build, and content quality grep commands.

Key discovery: sidebars file is `frontend/sidebars.ts` (TypeScript), not `sidebars.js` as documented in Module 1's plan. RagChatbot is per-file import, not globally registered.

## Outcome

- ✅ Impact: Complete implementation blueprint ready for /sp.tasks — all ambiguities resolved, no NEEDS CLARIFICATION markers remain
- 🧪 Tests: Constitution check 9/9 PASS; research questions 6/6 resolved
- 📁 Files: plan.md, research.md, data-model.md, quickstart.md, contracts/content-contract.md
- 🔁 Next prompts: /sp.tasks to generate implementation task list
- 🧠 Reflection: The sidebars.ts vs sidebars.js discrepancy (Module 1 plan was wrong about file extension) is a reminder to always read the live file, not rely on prior spec documentation

## Evaluation notes (flywheel)

- Failure modes observed: setup-plan.ps1 script not found in bash PATH — fell back to agent-native reads successfully
- Graders run and results (PASS/FAIL): Constitution check PASS (9/9)
- Prompt variant (if applicable): null
- Next experiment: null

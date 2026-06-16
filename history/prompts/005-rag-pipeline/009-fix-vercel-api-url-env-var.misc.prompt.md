---
id: "009"
title: Fix Vercel API_URL env var for deployed frontend
stage: misc
date: 2026-06-16
surface: agent
model: claude-sonnet-4-6
feature: 005-rag-pipeline
branch: 005-rag-pipeline
user: HayyanWasi
command: null
labels: ["deploy", "vercel", "render", "env-var", "debug"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - (no files modified — env var set in Vercel dashboard)
tests:
  - (none — manual verification via live site)
---

## Prompt

i did deploy the project's frontend on vercel and backend on render i got this error on frontend because i instantly check the app Could not reach the backend. Make sure the server is running on port 8000.

## Response snapshot

Investigated the error by reading `RagChatbot.jsx` and `docusaurus.config.ts`. Found that:

1. The chatbot reads `siteConfig.customFields.apiUrl` which falls back to `http://localhost:8000` if `API_URL` env var is not set at Vercel build time.
2. Inspected the deployed Vercel build artifact (minified JS) and confirmed `http://localhost:8000` was hardcoded — proving `API_URL` was never set in Vercel's environment variables.

Resolution: Set `API_URL=https://<render-backend-url>` in Vercel Dashboard → Settings → Environment Variables, then trigger a redeploy. Since Docusaurus is a static site, the env var is baked in at build time and a rebuild is required.

## Outcome

- ✅ Impact: Frontend chatbot will correctly reach Render backend after redeploy with env var set
- 🧪 Tests: Manual — user confirmed fix by setting env var in Vercel and redeploying
- 📁 Files: No code changes needed; fix was a Vercel dashboard configuration
- 🔁 Next prompts: Verify chatbot works end-to-end on live Vercel URL
- 🧠 Reflection: Docusaurus bakes env vars at build time (not runtime), so deployment env vars must be set before build — not just at runtime like a Node.js server.

## Evaluation notes (flywheel)

- Failure modes observed: Deployed build had localhost URL hardcoded due to missing Vercel env var; error message referenced port 8000 making it look like a backend issue but root cause was frontend misconfiguration
- Graders run and results (PASS/FAIL): none
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Add a visible config-check or fallback warning in RagChatbot when apiUrl still points to localhost in production

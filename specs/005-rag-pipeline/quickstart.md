# Quickstart: RAG Pipeline — Local Development Setup

**Feature**: `005-rag-pipeline` | **Date**: 2026-06-14

---

## Prerequisites

- Python 3.11 or later
- `backend/.env` file with credentials (already present in repo):
  - `COHERE_API_KEY` — Cohere Developer Tier key (embeddings only)
  - `GEMINI_API_KEY` — Google Gemini API key (used for answer generation via OpenAI Agents SDK)
  - `QDRANT_URL` — Cloud Qdrant instance URL
  - `QDRANT_API_KEY` — Cloud Qdrant API key

> ⚠️ **Security**: Ensure `backend/.env` is listed in `.gitignore` before pushing. The root `.gitignore` currently does not cover this path.

---

## Step 1: Set Up Python Environment

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

**Expected `requirements.txt` contents**:
```
fastapi==0.115.0
uvicorn[standard]==0.30.6
cohere>=5.0.0
qdrant-client>=1.9.0
python-dotenv>=1.0.0
openai-agents>=0.0.1
```

---

## Step 2: Verify Environment Variables

The `.env` file must contain (rename variables if needed to match the code):

```ini
COHERE_API_KEY=<your-cohere-key>
GEMINI_API_KEY=<your-gemini-key>
QDRANT_URL=https://d7f4496d-b1fa-4726-95b2-c9871859b806.us-east-1-1.aws.cloud.qdrant.io:6333
QDRANT_API_KEY=<your-qdrant-key>
```

> The existing `.env` uses `qdrant_api_key` (lowercase). The code will read it as `os.getenv("QDRANT_API_KEY")` — confirm casing matches or update accordingly.

---

## Step 3: Run Ingestion

From the repo root:

```bash
python backend/ingest.py
```

**What this does**:
1. Scans `frontend/docs/**/*.mdx` recursively
2. Strips YAML frontmatter, `import` statements, and JSX tags from each file
3. Splits each file into chunks on `##` heading boundaries
4. Batches chunks (90 per batch, 13-second inter-batch delay)
5. Sends each batch to Cohere `embed-v4.0` for embedding
6. Upserts resulting vectors into the `textbook-chunks` Qdrant collection

**Expected output**:
```
[ingest] Found 12 MDX files
[ingest] Extracted 48 chunks total
[ingest] Batch 1/1 (48 chunks) — embedding...
[ingest] Batch 1/1 — upserting 48 points to Qdrant...
[ingest] ✓ Ingestion complete. 48 points in collection 'textbook-chunks'.
```

**To verify**:
```bash
python -c "
from qdrant_client import QdrantClient
import os; from dotenv import load_dotenv; load_dotenv('backend/.env')
c = QdrantClient(url=os.getenv('QDRANT_URL'), api_key=os.getenv('QDRANT_API_KEY'))
print(c.get_collection('textbook-chunks').vectors_count)
"
```
Expected: a number > 0.

---

## Step 4: Start the Backend

```bash
uvicorn backend.main:app --reload --port 8000
```

Or from inside `backend/`:
```bash
uvicorn main:app --reload --port 8000
```

**Verify the backend is running**:
```bash
curl http://localhost:8000/health
# → {"status": "ok"}
```

---

## Step 5: Test the `/api/chat` Endpoint

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is ROS 2?", "context": "module-1"}'
```

**Expected response shape**:
```json
{
  "answer": "ROS 2 (Robot Operating System 2) is a middleware platform...",
  "sources": [
    {
      "file": "module-1/chapter-1-middleware",
      "heading": "How ROS 2 Works as Robotic Middleware",
      "module_num": 1
    }
  ]
}
```

---

## Step 6: Start the Docusaurus Frontend

```bash
cd frontend
npm install
npm start
```

Navigate to `http://localhost:3000` and open any chapter. The chatbot widget at the bottom of the page will now submit real questions to the backend.

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| `503: Knowledge base not populated` | Ingestion not yet run | Run `python backend/ingest.py` |
| `CORS error in browser console` | Backend not started | Run `uvicorn backend.main:app --port 8000` |
| `RateLimitError` during ingestion | Batch too large or delay too short | Reduce `BATCH_SIZE` or increase `BATCH_DELAY_SECONDS` in `ingest.py` |
| `Collection already exists` error | Re-running ingest after manual collection delete | The code checks `collection_exists()` before creating; re-run safely |
| Widget shows no loading state | Frontend not yet updated | Ensure `RagChatbot.jsx` has been updated (fetch logic added) |

---

## Re-Ingesting After Content Updates

Simply re-run `python backend/ingest.py`. Point IDs are deterministic (based on file path + heading), so existing chunks are replaced rather than duplicated. New headings added to existing chapters will be added as new points.

# Physical AI & Humanoid Robotics — Interactive Textbook

An interactive, web-based textbook covering the full stack of Physical AI and humanoid robotics — from ROS 2 fundamentals to Vision-Language-Action (VLA) capstone integration — with an embedded RAG chatbot that answers student questions from the textbook content.

---

## What's Inside

### 16 Chapters Across 4 Modules

| Module | Chapters | Topics |
|---|---|---|
| **Module 1: The Robotic Nervous System** | 1–4 | ROS 2 middleware, nodes & topics, rclpy, URDF |
| **Module 2: The Digital Twin** | 5–8 | Gazebo physics, collision simulation, Unity rendering, sensor simulation |
| **Module 3: The AI-Robot Brain** | 9–12 | Advanced perception, Isaac Sim synthetic data, Isaac ROS Visual SLAM, Nav2 bipedal planning |
| **Module 4: Vision-Language-Action** | 13–16 | VLA three-tier architecture, Whisper voice interface, LLM cognitive planning, autonomous humanoid capstone |

### RAG Chatbot

Every chapter has an embedded **Ask about this chapter** widget. Students type a question; the backend retrieves the most relevant passages from the textbook using Cohere embeddings + Qdrant vector search, then synthesises a concise answer using Google Gemini via the OpenAI Agents SDK.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | [Docusaurus v3](https://docusaurus.io/) + React (MDX content) |
| RAG Backend | FastAPI + Cohere `embed-v4.0` + Qdrant Cloud |
| Answer Synthesis | Google Gemini 2.5 Flash via OpenAI Agents SDK |
| Vector Store | Qdrant Cloud (managed) |

---

## Project Structure

```
.
├── frontend/               # Docusaurus site
│   ├── docs/
│   │   ├── module-1/       # Chapters 1–4
│   │   ├── module-2/       # Chapters 5–8
│   │   ├── module-3/       # Chapters 9–12
│   │   └── module-4/       # Chapters 13–16
│   ├── src/components/
│   │   └── RagChatbot.jsx  # Embedded chatbot widget
│   └── sidebars.ts         # Navigation configuration
├── backend/                # FastAPI RAG server
│   ├── main.py             # API endpoints (/health, /api/chat)
│   ├── agent.py            # OpenAI Agents SDK + Gemini integration
│   └── ingest.py           # Chunk and embed textbook content → Qdrant
└── specs/                  # Feature specifications and task lists
```

---

## Running Locally

### 1. Frontend (Docusaurus)

```bash
cd frontend
npm install
npm start
# → http://localhost:3000
```

### 2. Backend (FastAPI)

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Create `backend/.env`:

```env
COHERE_API_KEY=your_cohere_api_key
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
GEMINI_API_KEY=your_gemini_api_key
```

```bash
uvicorn main:app --reload --port 8000
# → http://localhost:8000/health
```

### 3. Ingest Textbook Content

Run once after the backend is up to embed the MDX chapters into Qdrant:

```bash
cd backend
python ingest.py
```

---

## API

### `POST /api/chat`

```json
// Request
{ "question": "What is the three-tier VLA architecture?", "context": "module-4" }

// Response
{
  "answer": "The three-tier VLA architecture separates...",
  "sources": [
    { "file": "module-4/chapter-13-vla-convergence.mdx", "heading": "The Three-Tier VLA Architecture", "module_num": 4 }
  ]
}
```

`context` scopes retrieval to a specific module (`"module-1"` through `"module-4"`). Omit for cross-module search.

---

## Development Notes

- The RAG chatbot requires both the frontend dev server **and** the FastAPI backend running simultaneously.
- `ingest.py` must be run at least once (or after adding new chapters) to populate the Qdrant collection.
- The `context` prop on `<RagChatbot context="module-4" />` scopes retrieval — students on a Module 4 chapter get answers from Module 4 content first.

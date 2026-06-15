import os
import logging
from typing import Optional
from contextlib import asynccontextmanager

import cohere
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from qdrant_client import QdrantClient

from agents import Runner
from agent import textbook_agent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

co: cohere.ClientV2 = None
qdrant: QdrantClient = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global co, qdrant
    cohere_key = os.getenv("COHERE_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_key = os.getenv("QDRANT_API_KEY")

    if not cohere_key:
        raise RuntimeError("COHERE_API_KEY is not set in the environment")
    if not qdrant_url or not qdrant_key:
        raise RuntimeError("QDRANT_URL and QDRANT_API_KEY must both be set in the environment")

    co = cohere.ClientV2(api_key=cohere_key)
    qdrant = QdrantClient(url=qdrant_url, api_key=qdrant_key)
    log.info("Cohere and Qdrant clients initialised")
    yield
    log.info("Shutting down")


app = FastAPI(title="Textbook RAG API", version="1.0.0", lifespan=lifespan)

_raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
_allowed_origins = [o.strip() for o in _raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


# ── Models ────────────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    question: str
    context: Optional[str] = None

    @field_validator("question")
    @classmethod
    def validate_question(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Question must not be empty")
        if len(v) > 2000:
            raise ValueError("Question too long (max 2000 characters)")
        return v


class SourceReference(BaseModel):
    file: str
    heading: str
    module_num: int


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceReference]


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    module_num = None
    if request.context and request.context.startswith("module-"):
        try:
            module_num = int(request.context.split("-")[1])
        except (IndexError, ValueError):
            pass

    run_context = {
        "cohere_client": co,
        "qdrant_client": qdrant,
        "module_num": module_num,
        "last_hits": None,
    }

    try:
        result = await Runner.run(textbook_agent, input=request.question, context=run_context)
        answer = result.final_output
    except Exception as exc:
        log.error("Agent run error: %s", exc)
        raise HTTPException(status_code=503, detail="Answer generation temporarily unavailable")

    hits = run_context["last_hits"]
    if hits is not None and not hits:
        raise HTTPException(
            status_code=503,
            detail="Knowledge base not populated. Please run ingest.py first.",
        )

    sources = [
        SourceReference(
            file=hit["file_path"],
            heading=hit["heading"],
            module_num=hit["module_num"],
        )
        for hit in (hits or [])
    ]

    return ChatResponse(answer=answer, sources=sources)

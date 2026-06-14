"""OpenAI Agents SDK + Gemini integration for the textbook RAG pipeline.

Embeddings and retrieval still use Cohere `embed-v4.0` and Qdrant; only the
final answer-synthesis step runs through an Agents SDK `Agent` backed by
Google Gemini via its OpenAI-compatible endpoint.
"""

import json
import logging
import os

import cohere
from dotenv import load_dotenv
from openai import AsyncOpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue

from agents import (
    Agent,
    RunContextWrapper,
    function_tool,
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
)

log = logging.getLogger(__name__)

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

COLLECTION = "textbook-chunks"
EMBED_MODEL = "embed-v4.0"
GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
TOP_K = 5

gemini_client = AsyncOpenAI(
    base_url=GEMINI_BASE_URL,
    api_key=os.getenv("GEMINI_API_KEY"),
)
set_default_openai_client(client=gemini_client, use_for_tracing=False)
set_default_openai_api("chat_completions")
set_tracing_disabled(disabled=True)


@function_tool
def search_textbook(wrapper: RunContextWrapper, query: str) -> str:
    """Search the textbook for passages relevant to the given query.

    Args:
        query: The search query — typically the student's question or a
            key phrase from it.
    """
    co: cohere.ClientV2 = wrapper.context["cohere_client"]
    qdrant: QdrantClient = wrapper.context["qdrant_client"]
    module_num = wrapper.context.get("module_num")

    embed_response = co.embed(
        model=EMBED_MODEL,
        input_type="search_query",
        texts=[query],
        embedding_types=["float"],
    )
    query_vector = embed_response.embeddings.float_[0]

    query_filter = None
    if module_num is not None:
        query_filter = Filter(
            must=[FieldCondition(key="module_num", match=MatchValue(value=module_num))]
        )

    hits = qdrant.query_points(
        collection_name=COLLECTION,
        query=query_vector,
        limit=TOP_K,
        query_filter=query_filter,
    ).points

    results = [
        {
            "heading": hit.payload.get("heading", ""),
            "file_path": hit.payload.get("file_path", ""),
            "module_num": hit.payload.get("module_num", 0),
            "text": hit.payload.get("text", ""),
        }
        for hit in hits
    ]

    # Side-channel for the FastAPI layer to extract source references
    # without re-parsing the agent's run items.
    wrapper.context["last_hits"] = results

    return json.dumps(results)


textbook_agent = Agent(
    name="Textbook Assistant",
    instructions=(
        "You answer student questions about a robotics textbook. "
        "Always call search_textbook to find relevant passages before answering. "
        "Synthesize a concise, coherent answer from the retrieved passages; "
        "do not invent facts or quote raw passages verbatim. "
        "If the retrieved passages are insufficient to answer, say so honestly "
        "instead of guessing. "
        "If the question is unrelated to the textbook content (e.g. general "
        "trivia, arithmetic, or topics outside robotics/AI), reply exactly: "
        "'I cannot answer irrelevant questions.'"
    ),
    model=GEMINI_MODEL,
    tools=[search_textbook],
)

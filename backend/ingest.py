"""
ingest.py — Scan all textbook MDX files, embed them with Cohere, and upsert
into the Qdrant 'textbook-chunks' collection.

Usage (from the repo root):
    python backend/ingest.py

Rate-limit safety: Cohere free tier allows 5 embed calls/min (max 96 texts/call).
BATCH_SIZE=90 and BATCH_DELAY_SECONDS=13 keep well within that limit.
"""

import os
import re
import time
import uuid
import logging
from pathlib import Path

import cohere
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, PayloadSchemaType

# ── Config ───────────────────────────────────────────────────────────────────

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

logging.basicConfig(level=logging.INFO, format="[ingest] %(message)s")
log = logging.getLogger(__name__)

COLLECTION = "textbook-chunks"
VECTOR_SIZE = 1536
EMBED_MODEL = "embed-v4.0"
BATCH_SIZE = 90
BATCH_DELAY_SECONDS = 13

DOCS_ROOT = Path(__file__).parent.parent / "frontend" / "docs"
UUID_NAMESPACE = uuid.NAMESPACE_URL

# ── Regex patterns ────────────────────────────────────────────────────────────

_FRONTMATTER = re.compile(r"^---[\s\S]*?---\s*\n", re.MULTILINE)
_IMPORTS = re.compile(r"^import\s.+$", re.MULTILINE)
_JSX_SELF_CLOSE = re.compile(r"<[A-Z][A-Za-z0-9]*[^>]*/\s*>")
_JSX_BLOCK = re.compile(r"<[A-Z][A-Za-z0-9]*[^>]*>[\s\S]*?</[A-Z][A-Za-z0-9]*>")
_H2_SPLIT = re.compile(r"^## (.+)$", re.MULTILINE)
_MODULE_RE = re.compile(r"module-(\d+)")
_CHAPTER_RE = re.compile(r"chapter-(\d+)")


# ── MDX parser ────────────────────────────────────────────────────────────────

def parse_mdx(path: Path) -> list[dict]:
    """Return a list of chunk dicts for each ## section in an MDX file."""
    raw = path.read_text(encoding="utf-8")

    text = _FRONTMATTER.sub("", raw)
    text = _IMPORTS.sub("", text)
    text = _JSX_BLOCK.sub("", text)
    text = _JSX_SELF_CLOSE.sub("", text)

    rel = path.relative_to(DOCS_ROOT.parent.parent)
    rel_str = rel.as_posix().replace("frontend/docs/", "").replace(".mdx", "")

    m_mod = _MODULE_RE.search(str(path))
    m_chap = _CHAPTER_RE.search(str(path))
    module_num = int(m_mod.group(1)) if m_mod else 0
    chapter_num = int(m_chap.group(1)) if m_chap else 0

    parts = _H2_SPLIT.split(text)
    # parts = [pre_text, heading1, body1, heading2, body2, ...]
    chunks = []
    for i in range(1, len(parts), 2):
        heading = parts[i].strip()
        body = parts[i + 1].strip() if i + 1 < len(parts) else ""
        if not body:
            continue
        chunks.append(
            {
                "text": f"## {heading}\n\n{body}",
                "heading": heading,
                "file_path": rel_str,
                "module_num": module_num,
                "chapter_num": chapter_num,
            }
        )
    return chunks


def chunk_id(file_path: str, heading: str) -> str:
    return str(uuid.uuid5(UUID_NAMESPACE, f"{file_path}#{heading}"))


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    cohere_key = os.getenv("COHERE_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_key = os.getenv("QDRANT_API_KEY")

    if not cohere_key:
        raise SystemExit("ERROR: COHERE_API_KEY not set in environment")
    if not qdrant_url or not qdrant_key:
        raise SystemExit("ERROR: QDRANT_URL and QDRANT_API_KEY must both be set in environment")

    co = cohere.ClientV2(api_key=cohere_key)
    qdrant = QdrantClient(url=qdrant_url, api_key=qdrant_key)

    # ── Ensure collection exists ──────────────────────────────────────────────
    if not qdrant.collection_exists(COLLECTION):
        qdrant.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )
        qdrant.create_payload_index(
            collection_name=COLLECTION,
            field_name="module_num",
            field_schema=PayloadSchemaType.INTEGER,
        )
        log.info("Created collection '%s'", COLLECTION)
    else:
        log.info("Collection '%s' already exists — upserting (will replace matching IDs)", COLLECTION)

    # ── Scan MDX files ────────────────────────────────────────────────────────
    mdx_files = sorted(DOCS_ROOT.glob("**/*.mdx"))
    if not mdx_files:
        raise SystemExit(f"ERROR: No .mdx files found under {DOCS_ROOT}")

    all_chunks: list[dict] = []
    for path in mdx_files:
        try:
            chunks = parse_mdx(path)
            all_chunks.extend(chunks)
        except Exception as exc:
            log.warning("Skipping %s — parse error: %s", path, exc)

    log.info("Found %d MDX files → %d chunks total", len(mdx_files), len(all_chunks))

    if not all_chunks:
        raise SystemExit("ERROR: No chunks extracted — check MDX file format")

    # ── Batch embed + upsert ──────────────────────────────────────────────────
    total_batches = (len(all_chunks) + BATCH_SIZE - 1) // BATCH_SIZE

    for batch_idx in range(total_batches):
        batch = all_chunks[batch_idx * BATCH_SIZE : (batch_idx + 1) * BATCH_SIZE]
        log.info("Batch %d/%d (%d chunks) — embedding...", batch_idx + 1, total_batches, len(batch))

        embed_response = co.embed(
            model=EMBED_MODEL,
            input_type="search_document",
            texts=[c["text"] for c in batch],
            embedding_types=["float"],
        )
        vectors = embed_response.embeddings.float_

        points = [
            PointStruct(
                id=chunk_id(chunk["file_path"], chunk["heading"]),
                vector=vec,
                payload={
                    "text": chunk["text"],
                    "heading": chunk["heading"],
                    "file_path": chunk["file_path"],
                    "module_num": chunk["module_num"],
                    "chapter_num": chunk["chapter_num"],
                },
            )
            for chunk, vec in zip(batch, vectors)
        ]

        qdrant.upsert(collection_name=COLLECTION, points=points)
        log.info("Batch %d/%d — upserted %d points", batch_idx + 1, total_batches, len(points))

        if batch_idx < total_batches - 1:
            log.info("Waiting %ds before next batch (rate-limit safety)...", BATCH_DELAY_SECONDS)
            time.sleep(BATCH_DELAY_SECONDS)

    count = qdrant.count(collection_name=COLLECTION).count
    log.info("✓ Ingestion complete. %d points now in '%s'.", count, COLLECTION)


if __name__ == "__main__":
    main()

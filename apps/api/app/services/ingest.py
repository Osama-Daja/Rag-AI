from __future__ import annotations

import re
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.api.deps import get_ollama_client, get_qdrant_service
from app.core.config import Settings, get_settings
from app.schemas.documents import IngestResponse
from app.services.chunking import chunk_text

ALLOWED_SUFFIXES = {".txt", ".md"}


class IngestError(ValueError):
    """Raised when ingest input is invalid."""


def _safe_filename(name: str) -> str:
    base = Path(name).name
    cleaned = re.sub(r"[^\w.\- ]+", "_", base).strip()
    return cleaned or f"upload-{uuid4().hex}.txt"


async def ingest_upload(file: UploadFile, settings: Settings | None = None) -> IngestResponse:
    settings = settings or get_settings()
    filename = _safe_filename(file.filename or "upload.txt")
    suffix = Path(filename).suffix.lower()
    if suffix not in ALLOWED_SUFFIXES:
        raise IngestError("Only .txt and .md files are supported")

    raw_bytes = await file.read()
    try:
        text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise IngestError("File must be valid UTF-8 text") from exc

    chunks = chunk_text(
        text,
        size=settings.rag_chunk_size,
        overlap=settings.rag_chunk_overlap,
    )
    if not chunks:
        raise IngestError("File is empty after parsing")

    raw_dir = Path(settings.data_raw_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)
    dest = raw_dir / filename
    dest.write_bytes(raw_bytes)

    ollama = get_ollama_client()
    qdrant = get_qdrant_service()
    await qdrant.ensure_collection(settings.ollama_embed_dim)
    vectors = await ollama.embed(chunks)

    points = [
        {
            "id": str(uuid4()),
            "vector": vector,
            "payload": {
                "text": chunk,
                "source": filename,
                "chunk_index": index,
            },
        }
        for index, (chunk, vector) in enumerate(zip(chunks, vectors))
    ]
    await qdrant.upsert(points)

    return IngestResponse(
        filename=filename,
        chunks_upserted=len(points),
        collection=qdrant.collection_name,
    )

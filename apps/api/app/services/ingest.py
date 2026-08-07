from __future__ import annotations

import re
from pathlib import Path
from uuid import uuid4

import httpx
from fastapi import UploadFile

from app.api.deps import get_ollama_client, get_qdrant_service
from app.core.config import Settings, get_settings
from app.schemas.documents import IngestResponse, ScanFileResult, ScanFolderResponse
from app.services.chunking import chunk_text
from app.services.ollama import OllamaError
from app.services.qdrant import QdrantServiceError
from app.services.scan import (
    ScanError,
    UnsupportedFileError,
    list_raw_files,
    scan_bytes,
    scan_path,
)


class IngestError(ValueError):
    """Raised when ingest input is invalid."""


class IngestDependencyError(RuntimeError):
    """Raised when Ollama/Qdrant dependencies fail during ingest."""


def _safe_filename(name: str) -> str:
    base = Path(name).name
    cleaned = re.sub(r"[^\w.\- ]+", "_", base).strip()
    return cleaned or f"upload-{uuid4().hex}.txt"


async def _embed_and_upsert(text: str, source: str, settings: Settings) -> IngestResponse:
    chunks = chunk_text(
        text,
        size=settings.rag_chunk_size,
        overlap=settings.rag_chunk_overlap,
    )
    if not chunks:
        raise IngestError("File is empty after chunking")

    ollama = get_ollama_client()
    qdrant = get_qdrant_service()

    try:
        vectors = await ollama.embed(chunks)
    except (OllamaError, httpx.HTTPError) as exc:
        raise IngestDependencyError(
            "Ollama embedding failed. Is Ollama running and is "
            f"'{settings.ollama_embed_model}' pulled?"
        ) from exc

    if not vectors:
        raise IngestError("Embedding returned no vectors")

    vector_size = len(vectors[0])
    try:
        await qdrant.ensure_collection(vector_size)
        points = [
            {
                "id": str(uuid4()),
                "vector": vector,
                "payload": {
                    "text": chunk,
                    "source": source,
                    "chunk_index": index,
                },
            }
            for index, (chunk, vector) in enumerate(zip(chunks, vectors))
        ]
        await qdrant.upsert(points)
    except QdrantServiceError as exc:
        raise IngestDependencyError(f"Qdrant ingest failed: {exc}") from exc

    return IngestResponse(
        filename=source,
        chunks_upserted=len(points),
        collection=qdrant.collection_name,
    )


async def ingest_upload(file: UploadFile, settings: Settings | None = None) -> IngestResponse:
    settings = settings or get_settings()
    filename = _safe_filename(file.filename or "upload.txt")
    raw_bytes = await file.read()

    try:
        scanned = scan_bytes(filename, raw_bytes)
    except UnsupportedFileError as exc:
        raise IngestError(str(exc)) from exc
    except ScanError as exc:
        raise IngestError(str(exc)) from exc

    raw_dir = Path(settings.data_raw_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)
    dest = raw_dir / filename
    dest.write_bytes(raw_bytes)

    return await _embed_and_upsert(scanned.text, scanned.source, settings)


async def ingest_path(path: Path, settings: Settings | None = None) -> IngestResponse:
    settings = settings or get_settings()
    try:
        scanned = scan_path(path)
    except UnsupportedFileError as exc:
        raise IngestError(str(exc)) from exc
    except ScanError as exc:
        raise IngestError(str(exc)) from exc
    except OSError as exc:
        raise IngestError(f"Cannot read file: {exc}") from exc

    return await _embed_and_upsert(scanned.text, scanned.source, settings)


async def ingest_raw_folder(settings: Settings | None = None) -> ScanFolderResponse:
    settings = settings or get_settings()
    raw_dir = Path(settings.data_raw_dir)
    files = list_raw_files(raw_dir)

    results: list[ScanFileResult] = []
    ingested = 0
    failed = 0

    for path in files:
        try:
            response = await ingest_path(path, settings)
            results.append(
                ScanFileResult(
                    filename=response.filename,
                    chunks_upserted=response.chunks_upserted,
                    status="ok",
                )
            )
            ingested += 1
        except (IngestError, IngestDependencyError) as exc:
            results.append(
                ScanFileResult(
                    filename=path.name,
                    chunks_upserted=0,
                    status="failed",
                    error=str(exc),
                )
            )
            failed += 1

    return ScanFolderResponse(
        scanned=len(files),
        ingested=ingested,
        failed=failed,
        results=results,
    )

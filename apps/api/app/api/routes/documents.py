from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.documents import IngestResponse, ScanFolderResponse
from app.services.ingest import (
    IngestDependencyError,
    IngestError,
    ingest_raw_folder,
    ingest_upload,
)

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/ingest", response_model=IngestResponse)
async def ingest_document(file: UploadFile = File(...)) -> IngestResponse:
    try:
        return await ingest_upload(file)
    except IngestError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except IngestDependencyError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.post("/scan", response_model=ScanFolderResponse)
async def scan_raw_folder() -> ScanFolderResponse:
    try:
        return await ingest_raw_folder()
    except IngestDependencyError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

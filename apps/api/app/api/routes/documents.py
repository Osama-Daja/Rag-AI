from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.documents import IngestResponse
from app.services.ingest import IngestError, ingest_upload

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/ingest", response_model=IngestResponse)
async def ingest_document(file: UploadFile = File(...)) -> IngestResponse:
    try:
        return await ingest_upload(file)
    except IngestError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

from __future__ import annotations

from io import BytesIO

from pypdf import PdfReader

from app.services.scan.types import ScanResult


def extract_pdf(filename: str, data: bytes, suffix: str) -> ScanResult:
    reader = PdfReader(BytesIO(data))
    pages: list[str] = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        cleaned = page_text.replace("\r\n", "\n").strip()
        if cleaned:
            pages.append(cleaned)

    text = "\n\n".join(pages).strip()
    if not text:
        raise ValueError("PDF produced no extractable text")
    return ScanResult(
        text=text,
        source=filename,
        suffix=suffix,
        page_count=len(reader.pages),
    )

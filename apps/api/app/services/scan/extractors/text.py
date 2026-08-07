from __future__ import annotations

from app.services.scan.types import ScanResult


def extract_text(filename: str, data: bytes, suffix: str) -> ScanResult:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("File must be valid UTF-8 text") from exc
    cleaned = text.replace("\r\n", "\n").strip()
    if not cleaned:
        raise ValueError("File is empty after parsing")
    return ScanResult(text=cleaned, source=filename, suffix=suffix)

from __future__ import annotations

from collections.abc import Callable

from app.services.scan.extractors.pdf import extract_pdf
from app.services.scan.extractors.text import extract_text
from app.services.scan.types import ScanResult

Extractor = Callable[[str, bytes, str], ScanResult]

EXTRACTORS: dict[str, Extractor] = {
    ".txt": extract_text,
    ".md": extract_text,
    ".pdf": extract_pdf,
}


def get_extractor(suffix: str) -> Extractor:
    try:
        return EXTRACTORS[suffix]
    except KeyError as exc:
        raise ValueError(f"No extractor registered for '{suffix}'") from exc

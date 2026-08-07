from __future__ import annotations

from pathlib import Path

SUPPORTED_SUFFIXES = {".txt", ".md", ".pdf"}


class UnsupportedFileError(ValueError):
    """Raised when a file type is not supported by the scan layer."""


def detect_suffix(filename: str) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix not in SUPPORTED_SUFFIXES:
        supported = ", ".join(sorted(SUPPORTED_SUFFIXES))
        raise UnsupportedFileError(
            f"Unsupported file type '{suffix or '(none)'}'. Supported: {supported}"
        )
    return suffix

from __future__ import annotations

from pathlib import Path

from app.services.scan.detector import SUPPORTED_SUFFIXES, UnsupportedFileError, detect_suffix
from app.services.scan.extractors import get_extractor
from app.services.scan.types import ScanResult


class ScanError(ValueError):
    """Raised when scanning/extracting a file fails."""


def scan_bytes(filename: str, data: bytes) -> ScanResult:
    try:
        suffix = detect_suffix(filename)
        extractor = get_extractor(suffix)
        return extractor(filename, data, suffix)
    except UnsupportedFileError:
        raise
    except ValueError as exc:
        raise ScanError(str(exc)) from exc
    except Exception as exc:
        raise ScanError(f"Failed to scan '{filename}': {exc}") from exc


def scan_path(path: Path) -> ScanResult:
    data = path.read_bytes()
    return scan_bytes(path.name, data)


def list_raw_files(directory: Path) -> list[Path]:
    if not directory.exists():
        return []
    files = [
        path
        for path in directory.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES
    ]
    return sorted(files, key=lambda p: p.name.lower())

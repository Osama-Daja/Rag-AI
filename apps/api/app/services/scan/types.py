from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScanResult:
    text: str
    source: str
    suffix: str
    page_count: int | None = None

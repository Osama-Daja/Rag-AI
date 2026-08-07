# Scan service

**Status:** active

## Job

Extract text from files **before** chunking and embedding.

```text
file bytes → detect type → extract text → ScanResult
```

## Supported types

| Suffix | Extractor |
|--------|-----------|
| `.txt` | UTF-8 text |
| `.md` | UTF-8 text |
| `.pdf` | `pypdf` page text |

## Layout

```text
scan/
  detector.py
  types.py
  scanner.py           scan_bytes / scan_path / list_raw_files
  extractors/
    text.py
    pdf.py
```

## Used by

- `services/ingest.py` — upload + folder scan orchestration
- `POST /documents/ingest`
- `POST /documents/scan` (lists `data/raw`)

## Rules

- Keep extractors here; ingest only orchestrates
- Unsupported types raise clear errors
- Empty extract is an error

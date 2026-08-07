# Data

Local document storage for ingest.

## Folders

| Path | Purpose |
|------|---------|
| `raw/` | Original uploaded files |
| `processed/` | Chunks or intermediate artifacts if needed on disk |

## Rules

- Do not commit large or private documents
- Prefer gitignoring contents of `raw/` and `processed/` later
- Vector data lives in Qdrant, not as the primary store here

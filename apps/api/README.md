# Backend (`apps/api`)

FastAPI service for Rag-AI: scan, ingest, chat, and pipeline registry.

## Status

Scan layer active: `.txt` / `.md` / `.pdf` extractors + folder scan. Simple RAG chat is live.

## Run

From repo root:

```bat
scripts\start-api.bat
```

- API: http://localhost:8000
- Health: http://localhost:8000/health
- Docs: http://localhost:8000/docs

## Endpoints

### Health

`GET /health` — API + Ollama + Qdrant status.

### Ingest (txt / md / pdf)

```bat
curl -X POST http://localhost:8000/documents/ingest -F "file=@sample.txt"
```

Saves to `data/raw`, scans/extracts text, chunks, embeds, upserts into Qdrant.

### Scan folder (`data/raw`)

```bat
curl -X POST http://localhost:8000/documents/scan
```

Scans supported files in `data/raw` and ingests each (per-file errors collected).

### Chat (simple RAG)

```bat
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d "{\"message\":\"What is in the document?\",\"mode\":\"simple\"}"
```

Other modes return `400` until implemented.

## Layout

```text
app/
  main.py
  api/
    deps.py
    routes/            health, documents, chat
  core/                config
  schemas/             chat, documents
  services/
    scan/              extract text (txt/md/pdf) + list raw files
    ollama/            embed + chat
    qdrant/            upsert + search
    chunking.py
    ingest.py          orchestrates scan → chunk → embed → upsert
  rag/
    base.py
    registry.py
    simple/            active pipeline
```

## Performance knobs

Defaults favor fewer, larger chunks and batched embeds:

| Env | Default | Effect |
| --- | --- | --- |
| `OLLAMA_EMBED_BATCH_SIZE` | `32` | texts per `/api/embed` call |
| `RAG_CHUNK_SIZE` / `RAG_CHUNK_OVERLAP` | `1200` / `150` | fewer chunks → faster ingest |
| `RAG_TOP_K` | `4` | fewer hits in chat context |
| `RAG_SOURCE_PREVIEW_CHARS` | `500` | truncates retrieved text sent to the LLM |

Restart the API after changing `.env`.

## Owned by

- Wiring/routes: Backend agent — `.cursor/agents/BACKEND.md`
- Pipeline / scan extractors: RagAI agent — `.cursor/agents/RAGAI.md`

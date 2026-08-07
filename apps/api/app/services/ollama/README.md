# Ollama service

**Status:** active

## Job

Local client for:

- Chat completions
- Text embeddings (batched)
- Connectivity ping

## Config

- `OLLAMA_BASE_URL` — `http://localhost:11434`
- `OLLAMA_CHAT_MODEL`
- `OLLAMA_EMBED_MODEL`
- `OLLAMA_EMBED_DIM` — vector size (default `768` for `nomic-embed-text`)
- `OLLAMA_EMBED_BATCH_SIZE` — texts per `/api/embed` call (default `32`)

## Code

- `client.py` — `OllamaClient` (`ping`, `embed`, `chat`)
- `embed()` uses `POST /api/embed` with an `input` array; falls back to legacy `/api/embeddings` per text if needed
- Wired via `app.api.deps.get_ollama_client`

## Used by

- `GET /health` (ping)
- Ingest + RAG pipelines

## Rules

- Local Ollama only for v1
- Keep model names in config, not scattered in pipelines

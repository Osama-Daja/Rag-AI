# Ollama service

**Status:** active (Phase 3)

## Job

Local client for:

- Chat completions
- Text embeddings
- Connectivity ping

## Config

- `OLLAMA_BASE_URL` — `http://localhost:11434`
- `OLLAMA_CHAT_MODEL`
- `OLLAMA_EMBED_MODEL`
- `OLLAMA_EMBED_DIM` — vector size (default `768` for `nomic-embed-text`)

## Code

- `client.py` — `OllamaClient` (`ping`, `embed`, `chat`)
- Wired via `app.api.deps.get_ollama_client`

## Used by

- `GET /health` (ping)
- RAG pipelines under `app/rag/*` (Phase 4+)

## Rules

- Local Ollama only for v1
- Keep model names in config, not scattered in pipelines

# Ollama service

**Status:** planned

## Job

Local client for:

- Chat completions
- Text embeddings

## Planned config

- `OLLAMA_BASE_URL` — `http://localhost:11434`
- `OLLAMA_CHAT_MODEL`
- `OLLAMA_EMBED_MODEL`

## Used by

RAG pipelines under `app/rag/*` (via RagAI). Wired by Backend agent into the API app.

## Rules

- Local Ollama only for v1
- Keep model names in config, not scattered in pipelines

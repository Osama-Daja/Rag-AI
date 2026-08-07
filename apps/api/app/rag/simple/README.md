# Simple RAG

**Status:** active (Phase 4)

## Job

Classic retrieve-then-generate:

1. Embed the user query (Ollama)
2. Search top-k chunks in Qdrant
3. Build a prompt with context
4. Generate answer (Ollama)
5. Return answer + sources

## Code

- `pipeline.py` — `SimpleRagPipeline`
- `prompt.py` — grounded system/user prompts

## Depends on

- `services/ollama` — embed + chat
- `services/qdrant` — vector search
- `services/chunking.py` — used at ingest time

## Owned by

RagAI agent — `.cursor/agents/RAGAI.md`

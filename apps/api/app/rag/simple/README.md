# Simple RAG

**Status:** planned (first mode to implement)

## Job

Classic retrieve-then-generate:

1. Embed the user query (Ollama)
2. Search top-k chunks in Qdrant
3. Build a prompt with context
4. Generate answer (Ollama)
5. Return answer + sources

## Belongs here

- Retriever helpers for simple top-k
- Prompt template for grounded answers
- `SimpleRagPipeline` entry (later)

## Depends on

- `services/ollama` — embed + chat
- `services/qdrant` — vector search

## Owned by

RagAI agent — `.cursor/agents/RAGAI.md`

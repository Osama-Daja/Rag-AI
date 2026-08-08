# Multi-hop RAG

**Status:** active (Phase 6)

## Job

Answer questions that need chained facts with a fixed 2-hop loop:

1. Dense retrieve (hop 1)
2. LLM writes one follow-up search query
3. Dense retrieve (hop 2), skip hop-1 ids
4. Merge contexts → generate answer

## Code

- `pipeline.py` — `MultiHopRagPipeline`
- `planner.py` — follow-up query prompt + `parse_follow_up`

## Config

- `RAG_MULTI_HOP_TOP_K` — per-hop retrieve size (default `4`)
- Reuses `RAG_SOURCE_PREVIEW_CHARS` for truncated context

## Depends on

- `services/ollama` — embed + chat
- `services/qdrant` — dense search
- `rag/simple/prompt.py` — final grounded answer prompt

## Owned by

RagAI agent — `.cursor/agents/RAGAI.md`

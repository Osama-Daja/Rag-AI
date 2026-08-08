# Agentic RAG

**Status:** active (Phase 6)

## Job

Bounded ReAct-lite loop: the LLM chooses `search` or `finish` each step before answering.

## Flow

1. Model emits `ACTION: search` + `QUERY` or `ACTION: finish` + `ANSWER`
2. Search → dense Qdrant retrieve → append observation
3. Loop until finish or `RAG_AGENTIC_MAX_STEPS`
4. On max steps → forced final answer from accumulated sources

## Code

- `pipeline.py` — `AgenticRagPipeline`
- `actions.py` — parse ACTION blocks
- `prompts.py` — agent system/user prompts + observation formatting

## Config

- `RAG_AGENTIC_MAX_STEPS` — decision rounds (default `3`)
- `RAG_AGENTIC_TOP_K` — hits per search (default `4`)
- Reuses `RAG_SOURCE_PREVIEW_CHARS`

## Depends on

- `services/ollama` — embed + chat
- `services/qdrant` — dense search
- `rag/simple/prompt.py` — forced final answer

## Owned by

RagAI agent — `.cursor/agents/RAGAI.md`

from __future__ import annotations

SYSTEM_PROMPT = (
    "You are a helpful assistant for Rag-AI. "
    "Answer using only the provided context. "
    "If the context is insufficient, say you do not know. "
    "Be concise and factual."
)


def build_user_prompt(question: str, contexts: list[str]) -> str:
    if contexts:
        joined = "\n\n---\n\n".join(contexts)
    else:
        joined = "(no context retrieved)"
    return (
        f"Context:\n{joined}\n\n"
        f"Question: {question}\n\n"
        "Answer:"
    )

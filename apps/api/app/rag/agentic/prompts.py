from __future__ import annotations

AGENT_SYSTEM_PROMPT = (
    "You are a retrieval agent for Rag-AI. "
    "You may search a document store, then answer using only observations. "
    "Respond with exactly one action in this format:\n\n"
    "ACTION: search\n"
    "QUERY: <one-line search query>\n\n"
    "or\n\n"
    "ACTION: finish\n"
    "ANSWER: <final answer>\n\n"
    "Rules:\n"
    "- Prefer search when context is missing or incomplete.\n"
    "- Prefer finish when observations are enough to answer.\n"
    "- Do not invent facts outside observations.\n"
    "- If observations are insufficient, finish and say you do not know.\n"
    "- Output only the ACTION block (no extra commentary)."
)


def build_agent_user_prompt(question: str, observations: list[str]) -> str:
    if observations:
        joined = "\n\n".join(observations)
    else:
        joined = "(no observations yet)"
    return (
        f"Question: {question}\n\n"
        f"Observations so far:\n{joined}\n\n"
        "Choose the next ACTION:"
    )


def format_observation(snippets: list[str]) -> str:
    if not snippets:
        return "Observation:\n(no results)"
    lines = [f"{index}. {snippet}" for index, snippet in enumerate(snippets, start=1)]
    return "Observation:\n" + "\n".join(lines)

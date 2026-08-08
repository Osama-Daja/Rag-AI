from __future__ import annotations

import re

import networkx as nx

from app.rag.graph.extract import Triple

_TOKEN_RE = re.compile(r"[a-z0-9]+", re.IGNORECASE)


def build_graph(triples: list[Triple]) -> nx.DiGraph:
    graph = nx.DiGraph()
    for triple in triples:
        graph.add_node(triple.subject)
        graph.add_node(triple.object)
        graph.add_edge(triple.subject, triple.object, relation=triple.relation)
    return graph


def seed_entities(query: str, triples: list[Triple]) -> list[str]:
    if not triples:
        return []

    all_entities: list[str] = []
    seen_lower: set[str] = set()
    for triple in triples:
        for name in (triple.subject, triple.object):
            key = name.lower()
            if key in seen_lower:
                continue
            seen_lower.add(key)
            all_entities.append(name)

    query_tokens = {token.lower() for token in _TOKEN_RE.findall(query)}
    if not query_tokens:
        return all_entities

    matched: list[str] = []
    for name in all_entities:
        name_tokens = {token.lower() for token in _TOKEN_RE.findall(name)}
        if name_tokens & query_tokens or any(
            token in name.lower() for token in query_tokens if len(token) >= 3
        ):
            matched.append(name)

    return matched or all_entities


def expand_entities(
    graph: nx.DiGraph,
    seeds: list[str],
    *,
    hops: int = 1,
) -> list[str]:
    if graph.number_of_nodes() == 0 or not seeds:
        return []

    # Resolve seed names case-insensitively to graph nodes.
    node_by_lower = {str(node).lower(): str(node) for node in graph.nodes}
    frontier: set[str] = set()
    for seed in seeds:
        resolved = node_by_lower.get(seed.lower())
        if resolved is not None:
            frontier.add(resolved)

    if not frontier:
        return []

    reached = set(frontier)
    current = set(frontier)
    steps = max(0, hops)
    for _ in range(steps):
        nxt: set[str] = set()
        for node in current:
            nxt.update(str(n) for n in graph.successors(node))
            nxt.update(str(n) for n in graph.predecessors(node))
        nxt -= reached
        if not nxt:
            break
        reached |= nxt
        current = nxt

    # Prefer expanded neighbors first, then seeds.
    expanded = [node for node in reached if node not in frontier]
    return expanded + sorted(frontier)

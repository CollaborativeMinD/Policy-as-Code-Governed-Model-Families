"""PCC-10 — Quarantine Boundary, blast radius."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('network-and-compute/network_execution_bounds/quarantine_blast_radius')


from collections import deque
from collections.abc import Iterable, Mapping


def symbolic_expression() -> str:
    return 'd'


def lambdified_distance_identity():
    @_policy.evaluator("lambdified_distance_identity.evaluate")
    def evaluate(d):
        return d

    return evaluate


def _adj(edges: Iterable[tuple[str, str]]) -> dict[str, set[str]]:
    adj: dict[str, set[str]] = {}
    for a, b in edges:
        a, b = str(a), str(b)
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)
    return adj


def shortest_hop_distances(source: str, edges: Iterable[tuple[str, str]]) -> dict[str, int]:
    source = str(source)
    adj = _adj(edges)
    if source not in adj:
        return {source: 0}
    dist = {source: 0}
    q = deque([source])
    while q:
        node = q.popleft()
        for nbr in adj[node]:
            if nbr not in dist:
                dist[nbr] = dist[node] + 1
                q.append(nbr)
    return dist


def compute_blast_radius(source: str, affected_nodes: Iterable[str], edges: Iterable[tuple[str, str]]) -> int:
    affected = [str(n) for n in affected_nodes]
    distances = shortest_hop_distances(source, edges)
    missing = [n for n in affected if n not in distances]
    if missing:
        raise ValueError(f"affected nodes unreachable from source: {missing}")
    if not affected:
        return 0
    return int(max(distances[n] for n in affected))


__all__ = [
    "symbolic_expression",
    "lambdified_distance_identity",
    "shortest_hop_distances",
    "compute_blast_radius",
]

_policy.bind(globals())

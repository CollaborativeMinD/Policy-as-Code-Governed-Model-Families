"""PCC-09 — Single Point of Failure Law, k-connectivity."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('network-and-compute/network_execution_bounds/k_connectivity_survival')


from collections import deque
from collections.abc import Iterable


def symbolic_expression() -> str:
    return 'kappa - 2'


def lambdified_margin():
    @_policy.evaluator("lambdified_margin.evaluate")
    def evaluate(kappa):
        return kappa - 2

    return evaluate


def _adjacency(nodes: Iterable[str], edges: Iterable[tuple[str, str]], removed: str | None = None) -> dict[str, set[str]]:
    adj = {str(n): set() for n in nodes if str(n) != removed}
    for a, b in edges:
        a, b = str(a), str(b)
        if a == removed or b == removed or a not in adj or b not in adj:
            continue
        adj[a].add(b)
        adj[b].add(a)
    return adj


def _connected(adj: dict[str, set[str]]) -> bool:
    if not adj:
        return True
    start = next(iter(adj))
    seen = {start}
    q = deque([start])
    while q:
        node = q.popleft()
        for nbr in adj[node]:
            if nbr not in seen:
                seen.add(nbr)
                q.append(nbr)
    return len(seen) == len(adj)


def has_two_independent_paths(nodes: Iterable[str], edges: Iterable[tuple[str, str]]) -> bool:
    nodes = [str(n) for n in nodes]
    if len(nodes) < 3:
        return False
    if not _connected(_adjacency(nodes, edges)):
        return False
    for removed in nodes:
        if not _connected(_adjacency(nodes, edges, removed)):
            return False
    return True


__all__ = [
    "symbolic_expression",
    "lambdified_margin",
    "has_two_independent_paths",
]

_policy.bind(globals())

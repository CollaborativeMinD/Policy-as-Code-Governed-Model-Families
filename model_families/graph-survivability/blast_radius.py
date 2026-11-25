"""M2.2 — Blast radius over graph topology"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('graph-survivability/blast_radius')


from collections import deque
from typing import Dict, Sequence


def compute_blast_radius(graph: Dict[str, Sequence[str]], v: str) -> int:
    """Compute the blast radius of a node in an unweighted graph.

    Parameters
    ----------
    graph : Dict[str, Sequence[str]]
        Adjacency list representation of the graph.  Keys are node
        identifiers and values are sequences of neighbor identifiers.
    v : str
        The source node for which to compute the blast radius.

    Returns
    -------
    int
        The maximum shortest‑path distance from ``v`` to any node
        reachable within the graph.  If ``v`` is isolated, the result
        is ``0``.

    Raises
    ------
    KeyError
        If ``v`` is not present in ``graph``.
    """
    if v not in graph:
        raise KeyError(f"Node {v} is not present in the graph")
    # BFS to compute distances
    visited = {v: 0}
    queue = deque([v])
    while queue:
        current = queue.popleft()
        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                visited[neighbor] = visited[current] + 1
                queue.append(neighbor)
    # The blast radius is the maximum of all distances
    return max(visited.values()) if visited else 0


__all__ = ['compute_blast_radius']

_policy.bind(globals())

"""M2.3 — Critical connectivity after node loss"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('graph-survivability/graph_survivability')


from collections import deque
from collections.abc import Mapping, Iterable, Hashable


def _disjoint_paths(neighbors, source, target, upper_bound):
    """Count vertex-disjoint paths by sending unit flow through split nodes."""
    residual = {}
    def edge(u, v, capacity):
        residual.setdefault(u, {})[v] = capacity
        residual.setdefault(v, {}).setdefault(u, 0)

    for u, adjacent in neighbors.items():
        edge((u, 0), (u, 1), 1)
        for v in adjacent:
            edge((u, 1), (v, 0), upper_bound)
    start, end = (source, 1), (target, 0)
    for flow in range(upper_bound):
        parent = {start: None}
        queue = deque([start])
        while queue and end not in parent:
            u = queue.popleft()
            for v, capacity in residual[u].items():
                if capacity and v not in parent:
                    parent[v] = u
                    queue.append(v)
        if end not in parent:
            return flow
        v = end
        while v != start:
            u = parent[v]
            residual[u][v] -= 1
            residual[v][u] += 1
            v = u
    return upper_bound


def compute_vertex_connectivity(graph: Mapping[Hashable, Iterable[Hashable]]) -> int:
    """Minimum vertex cut of a simple undirected graph supplied as adjacency lists."""
    neighbors = {node: set(graph[node]) - {node} for node in graph}
    if any(node not in neighbors.get(other, ()) for node, row in neighbors.items() for other in row):
        raise ValueError("adjacency must describe an undirected graph")
    if not neighbors:
        raise ValueError("connectivity is undefined for the empty graph")
    bound = min(map(len, neighbors.values()))
    nodes = list(neighbors)
    for i, source in enumerate(nodes):
        for target in nodes[i+1:]:
            if target not in neighbors[source]:
                bound = _disjoint_paths(neighbors, source, target, bound)
                if bound == 0:
                    return 0
    return bound


def is_graph_survivable(graph: Mapping[Hashable, Iterable[Hashable]], threshold: int = _policy.default) -> bool:
    """Check whether the graph meets the survivability threshold.

    The graph is considered survivable if its vertex connectivity is
    greater than or equal to ``threshold``.

    Parameters
    ----------
    graph : adjacency mapping
        The graph to evaluate.
    threshold : int, optional
        Minimum required vertex connectivity.  Default is ``2``.

    Returns
    -------
    bool
        ``True`` if κ(G) ≥ threshold; ``False`` otherwise.
    """
    return compute_vertex_connectivity(graph) >= threshold


__all__ = ['compute_vertex_connectivity', 'is_graph_survivable']

_policy.bind(globals())

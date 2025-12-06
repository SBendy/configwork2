# dfs.py
from dataclasses import dataclass
from typing import List, Set

from graph import DependencyGraph, NodeId, node_key


@dataclass
class DFSOptions:
    max_depth: int


@dataclass
class DFSResult:
    order: List[str]
    cycles: List[List[str]]


def dfs_iterative(graph: DependencyGraph, start: NodeId, options: DFSOptions) -> DFSResult:
    start_key = node_key(start)
    visited: Set[str] = set()
    stack = [{
        "node_key": start_key,
        "depth": 0,
        "path": [start_key],
    }]
    order: List[str] = []
    cycles: List[List[str]] = []

    while stack:
        frame = stack.pop()
        current = frame["node_key"]
        depth = frame["depth"]
        path = frame["path"]

        if current in visited:
            continue
        visited.add(current)
        order.append(current)

        if depth >= options.max_depth:
            continue

        neighbors = graph.adjacency.get(current, [])
        for neigh in neighbors:
            if neigh in path:
                # цикл
                idx = path.index(neigh)
                cycles.append(path[idx:] + [neigh])
                continue
            stack.append({
                "node_key": neigh,
                "depth": depth + 1,
                "path": path + [neigh],
            })

    return DFSResult(order=order, cycles=cycles)

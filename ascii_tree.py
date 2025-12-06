# ascii_tree.py
from typing import Set

from graph import DependencyGraph


def print_ascii_tree(graph: DependencyGraph, root_key: str, max_depth: int) -> None:
    """
    Печать графа в виде дерева (простой обход).
    Циклы помечаем (*) и не раскрываем повторно.
    """
    visited: Set[str] = set()

    class Frame:
        def __init__(self, node: str, depth: int, prefix: str, is_last: bool):
            self.node = node
            self.depth = depth
            self.prefix = prefix
            self.is_last = is_last

    stack = [Frame(root_key, 0, "", True)]

    while stack:
        frame = stack.pop()
        node = frame.node
        depth = frame.depth
        prefix = frame.prefix
        is_last = frame.is_last

        is_root = depth == 0
        line_prefix = "" if is_root else prefix + ("└─ " if is_last else "├─ ")
        mark = " (*)" if node in visited else ""

        print(f"{line_prefix}{node}{mark}")

        if node in visited:
            continue
        visited.add(node)

        if depth >= max_depth:
            continue

        neighbors = graph.adjacency.get(node, [])
        total = len(neighbors)

        for i in range(total - 1, -1, -1):
            child = neighbors[i]
            child_is_last = (i == total - 1)
            child_prefix = "" if is_root else prefix + ("   " if is_last else "│  ")
            stack.append(Frame(child, depth + 1, child_prefix, child_is_last))

# d2_export.py
from graph import DependencyGraph


def graph_to_d2(graph: DependencyGraph) -> str:
    """
    Простое текстовое представление графа в формате D2.
    """
    lines = []

    # Объявляем узлы
    for node in graph.adjacency.keys():
        lines.append(f"\"{node}\"")

    # Ребра
    for from_key, neighbors in graph.adjacency.items():
        for to_key in neighbors:
            lines.append(f"\"{from_key}\" -> \"{to_key}\"")

    return "\n".join(lines)

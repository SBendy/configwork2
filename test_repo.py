# test_repo.py
from typing import Tuple

from graph import DependencyGraph, NodeId


def load_test_graph(file_path: str) -> Tuple[DependencyGraph, NodeId]:
    """
    Загружаем тестовый граф из файла.
    Формат строк: A: B C
    Пакеты — заглавные латинские буквы.
    Версию фиктивно задаём как '1.0.0'.
    """
    graph = DependencyGraph()
    root: NodeId | None = None

    with open(file_path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" not in line:
                raise ValueError(f"Неверная строка в тестовом репо: {line}")

            left, right = line.split(":", 1)
            left = left.strip()
            right = right.strip()

            if not left:
                continue

            from_node = NodeId(name=left, version="1.0.0")
            graph.add_node(from_node)

            if root is None:
                root = from_node

            if not right:
                # без зависимостей
                continue

            deps = right.split()
            for dep_name in deps:
                dep_node = NodeId(name=dep_name, version="1.0.0")
                graph.add_edge(from_node, dep_node)

    if root is None:
        raise ValueError("Файл тестового репозитория пуст или не содержит пакетов")

    return graph, root

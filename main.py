# main.py
import sys

from config import AppConfig, parse_args, print_config, ConfigError
from graph import DependencyGraph, NodeId, node_key, build_reverse_graph
from dfs import dfs_iterative, DFSOptions
from ascii_tree import print_ascii_tree
from d2_export import graph_to_d2
from npm_reader import get_direct_dependencies, RegistryError
from test_repo import load_test_graph


def build_real_graph(cfg: AppConfig) -> tuple[DependencyGraph, NodeId]:
    """
    Реальный режим: строим граф зависимостей через npm registry.
    Алгоритм:
      - Нерекурсивный обход с учётом max_depth.
      - На каждом шаге берём прямые зависимости через npm_reader.get_direct_dependencies.
    """
    graph = DependencyGraph()
    root = NodeId(name=cfg.package_name, version=cfg.version)

    stack: list[tuple[NodeId, int]] = [(root, 0)]
    visited: set[str] = set()

    while stack:
        node, depth = stack.pop()
        key = node_key(node)
        if key in visited:
            continue
        visited.add(key)
        graph.add_node(node)

        if depth >= cfg.max_depth:
            continue

        try:
            deps = get_direct_dependencies(node)
        except RegistryError as e:
            print(f"Ошибка при получении зависимостей для {key}: {e}", file=sys.stderr)
            continue

        for dep_name, dep_version in deps.items():
            dep_node = NodeId(name=dep_name, version=dep_version)
            graph.add_edge(node, dep_node)
            stack.append((dep_node, depth + 1))

    return graph, root


def build_test_graph(cfg: AppConfig) -> tuple[DependencyGraph, NodeId]:
    """
    Тестовый режим: загружаем граф из файла и игнорируем version/package_name
    (root берём из файла).
    """
    graph, root = load_test_graph(cfg.repo)
    return graph, root


def print_direct_dependencies(graph: DependencyGraph, root_key: str) -> None:
    """
    Этап 2: вывод всех прямых зависимостей заданного пакета.
    Берём их из списка соседей root в графе.
    """
    print(f"Прямые зависимости {root_key}:")
    neighbors = graph.adjacency.get(root_key, [])
    if not neighbors:
        print("  (нет прямых зависимостей)")
        print()
        return
    for n in neighbors:
        print(f"  {n}")
    print()


def main(argv=None) -> None:
    try:
        cfg = parse_args(argv)
    except ConfigError as e:
        print(f"Ошибка конфигурации: {e}", file=sys.stderr)
        sys.exit(1)
    except SystemExit:
        # argparse уже всё напечатал (help/usage)
        raise

    # Этап 1: вывести параметры
    print_config(cfg)

    # Этап 2–3: построить граф
    if cfg.mode == "real":
        graph, root = build_real_graph(cfg)
    else:
        graph, root = build_test_graph(cfg)

    root_key = node_key(root)

    # Этап 2: вывести прямые зависимости
    print_direct_dependencies(graph, root_key)

    # Этап 3: DFS с учётом max_depth + обработка циклов
    if not cfg.reverse:
        print(f"Обход графа зависимостей (DFS) от {root_key}, глубина <= {cfg.max_depth}")
        dfs_result = dfs_iterative(graph, root, DFSOptions(max_depth=cfg.max_depth))
        print("Порядок обхода:")
        for k in dfs_result.order:
            print(f"  {k}")
        print()

        if dfs_result.cycles:
            print("Обнаружены циклы:")
            for cycle in dfs_result.cycles:
                print("  " + " -> ".join(cycle))
            print()
        else:
            print("Циклы не обнаружены.\n")

        # Этап 5: ASCII-дерево (если включено)
        if cfg.ascii_tree:
            print("ASCII-дерево зависимостей:")
            print_ascii_tree(graph, root_key, cfg.max_depth)
            print()

    # Этап 4: обратные зависимости
    if cfg.reverse:
        print(f"Режим обратных зависимостей для {root_key}")
        rev_graph = build_reverse_graph(graph)
        dfs_result = dfs_iterative(
            rev_graph, root, DFSOptions(max_depth=cfg.max_depth)
        )
        # Первый элемент — сам root, остальные — пакеты, зависящие от него
        dependents = [k for k in dfs_result.order if k != root_key]
        if not dependents:
            print("От этого пакета никто не зависит (в пределах построенного графа).\n")
        else:
            print("Пакеты, зависящие от него:")
            for k in dependents:
                print(f"  {k}")
            print()

        if cfg.ascii_tree:
            print("ASCII-дерево обратных зависимостей:")
            print_ascii_tree(rev_graph, root_key, cfg.max_depth)
            print()

        if dfs_result.cycles:
            print("Циклы (в графе обратных зависимостей):")
            for cycle in dfs_result.cycles:
                print("  " + " -> ".join(cycle))
            print()
        else:
            print("Циклов в графе обратных зависимостей не обнаружено.\n")

    # Этап 5: D2-описание графа
    if cfg.d2:
        print("--- D2 описание графа ---")
        d2_text = graph_to_d2(graph)
        print(d2_text)
        print()


if __name__ == "__main__":
    main()

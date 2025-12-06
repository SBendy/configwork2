# graph.py
from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class NodeId:
    name: str
    version: str


def node_key(node: NodeId) -> str:
    return f"{node.name}@{node.version}"


@dataclass
class DependencyGraph:
    adjacency: Dict[str, List[str]] = field(default_factory=dict)

    def add_node(self, node: NodeId) -> None:
        key = node_key(node)
        if key not in self.adjacency:
            self.adjacency[key] = []

    def add_edge(self, from_node: NodeId, to_node: NodeId) -> None:
        from_key = node_key(from_node)
        to_key = node_key(to_node)
        if from_key not in self.adjacency:
            self.adjacency[from_key] = []
        if to_key not in self.adjacency:
            self.adjacency[to_key] = []
        if to_key not in self.adjacency[from_key]:
            self.adjacency[from_key].append(to_key)


def split_key(key: str) -> Tuple[str, str]:
    """Обратная операция к node_key."""
    if "@" in key:
        name, version = key.split("@", 1)
    else:
        name, version = key, ""
    return name, version


def build_reverse_graph(graph: DependencyGraph) -> DependencyGraph:
    reverse = DependencyGraph()
    for key in graph.adjacency.keys():
        name, version = split_key(key)
        reverse.add_node(NodeId(name=name, version=version))
    for from_key, neighbors in graph.adjacency.items():
        from_name, from_ver = split_key(from_key)
        from_node = NodeId(from_name, from_ver)
        for to_key in neighbors:
            to_name, to_ver = split_key(to_key)
            to_node = NodeId(to_name, to_ver)
            reverse.add_edge(to_node, from_node)
    return reverse

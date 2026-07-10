from typing import Dict, List, Set, Any, Optional
import asyncio
from dataclasses import dataclass, field

@dataclass(frozen=True)
class TaskNode:
    """Represents a discrete unit of work within the topological manifold."""
    id: str
    agent: str
    action: str
    dependencies: Set[str] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)

class TaskGraph:
    """
    The Weaver's Loom. 
    A Directed Acyclic Graph (DAG) managing relational task dependencies.
    """
    def __init__(self):
        self.nodes: Dict[str, TaskNode] = {}
        self.edges: Dict[str, Set[str]] = {} # adjacency list

    def add_task(self, node: TaskNode):
        self.nodes[node.id] = node
        if node.id not in self.edges:
            self.edges[node.id] = set()
        for dep in node.dependencies:
            if dep not in self.edges:
                self.edges[dep] = set()
            self.edges[dep].add(node.id)

    def get_ready_tasks(self, completed_ids: Set[str]) -> List[TaskNode]:
        """Returns tasks whose dependencies are all satisfied."""
        ready = []
        for node in self.nodes.values():
            if node.id not in completed_ids and node.dependencies.issubset(completed_ids):
                ready.append(node)
        return ready

    def is_complete(self, completed_ids: Set[str]) -> bool:
        return len(completed_ids) == len(self.nodes)

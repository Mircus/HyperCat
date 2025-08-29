
from dataclasses import dataclass
from typing import Tuple, Callable, List

@dataclass(frozen=True)
class ArchGraph:
    nodes: Tuple[str, ...]
    edges: Tuple[Tuple[str, str], ...]

@dataclass(frozen=True)
class Rewrite:
    name: str
    predicate: Callable[[ArchGraph], bool]
    apply: Callable[[ArchGraph], ArchGraph]

class ArchCat:
    def __init__(self):
        self.rewrites: List[Rewrite] = []
    def register(self, r: Rewrite): self.rewrites.append(r)
    def try_apply(self, g: ArchGraph):
        for r in self.rewrites:
            if r.predicate(g): return r.apply(g), r.name
        return g, None

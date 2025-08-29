
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Iterable

Path = Tuple[str, ...]

@dataclass(frozen=True)
class Diagram:
    left: Path
    right: Path

@dataclass(frozen=True)
class Relation:
    lhs: Path
    rhs: Path
    name: str

@dataclass
class Certificate:
    steps: List[Tuple[str, int, str]]  # (relation_name, offset, direction "→"/"←")
    def is_empty(self) -> bool: return len(self.steps) == 0

class CommutativityChecker:
    """Tiny, bounded subpath-rewriting checker for equality of two paths of labels.
    Does not override the enhanced checker; import explicitly if you want subpath proofs.
    """
    def __init__(self, relations: Iterable[Relation]):
        self.rels: List[Relation] = list(relations)

    def _subs(self, path: Path):
        n = len(path)
        for r in self.rels:
            for direction, pat, rep in [("→", r.lhs, r.rhs), ("←", r.rhs, r.lhs)]:
                L = len(pat)
                if L == 0 or L > n: continue
                for i in range(0, n - L + 1):
                    if path[i:i+L] == pat:
                        newp = path[:i] + rep + path[i+L:]
                        yield newp, (r.name, i, direction)

    def check(self, diagram: Diagram, budget: int = 2048):
        from collections import deque
        if diagram.left == diagram.right:
            return True, Certificate([])
        q = deque([(diagram.left, [])]); seen = {diagram.left}; steps=0
        while q and steps < budget:
            steps += 1
            path, cert = q.popleft()
            for newp, info in self._subs(path):
                if newp == diagram.right:
                    return True, Certificate(cert + [info])
                if newp not in seen:
                    seen.add(newp); q.append((newp, cert + [info]))
        return False, Certificate([])

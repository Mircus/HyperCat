
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from .computad import Generator, Relation
Path = Tuple[int, ...]

@dataclass
class FiniteWeakNCategory:
    n: int
    generators: Dict[int, List[Generator]] = field(default_factory=dict)
    relations: Dict[int, List[Relation]] = field(default_factory=dict)

    def __post_init__(self):
        for k in range(1, self.n + 1):
            self.generators.setdefault(k, [])
            self.relations.setdefault(k, [])

    def add_generator(self, g: Generator) -> int:
        assert 1 <= g.dim <= self.n, "generator dim must be 1..n"
        idx = len(self.generators[g.dim])
        self.generators[g.dim].append(g)
        return idx

    def add_relation(self, r: Relation) -> int:
        assert 1 <= r.dim <= self.n, "relation dim must be 1..n"
        idx = len(self.relations[r.dim])
        self.relations[r.dim].append(r)
        return idx

    def _substitutions(self, dim: int, path: Path):
        rels = self.relations.get(dim, [])
        n = len(path)
        for r in rels:
            for direction, pat, rep in [("→", r.lhs, r.rhs), ("←", r.rhs, r.lhs)]:
                L = len(pat)
                if L == 0 or L > n: continue
                for i in range(0, n - L + 1):
                    if path[i:i+L] == pat:
                        newp = path[:i] + rep + path[i+L:]
                        yield newp, (r.name, i, direction)

    def certificate(self, dim: int, lhs: Path, rhs: Path, budget: int = 2048):
        from collections import deque
        if lhs == rhs: return []
        seen = {lhs}
        q = deque([(lhs, [])])
        steps = 0
        while q and steps < budget:
            steps += 1
            path, cert = q.popleft()
            for newp, info in self._substitutions(dim, path):
                if newp == rhs:
                    return cert + [info]
                if newp not in seen:
                    seen.add(newp); q.append((newp, cert + [info]))
        return []

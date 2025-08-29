
from __future__ import annotations
from dataclasses import dataclass
from typing import List
from .transcat import ModelHandle

@dataclass
class PathSpace:
    points: List[ModelHandle]
    def sample(self, n: int) -> "PathSpace":
        if len(self.points) <= 1 or n <= 1: return self
        idxs = [int(i*(len(self.points)-1)/(n-1)) for i in range(n)]
        return PathSpace([self.points[i] for i in idxs])

@dataclass
class Deformation:
    @staticmethod
    def between(a: ModelHandle, b: ModelHandle, steps: int = 5) -> PathSpace:
        assert a.arch == b.arch
        keys = list(a.weights.keys()); pts = []
        for t in range(steps):
            lam = t/(steps-1) if steps>1 else 0.0
            w = {k: (1-lam)*a.weights[k] + lam*b.weights[k] for k in keys}
            pts.append(ModelHandle(a.arch, w))
        return PathSpace(pts)

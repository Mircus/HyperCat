
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

@dataclass
class FiniteTruncatedSSet:
    n: int
    simplices: Dict[int, List[object]] = field(default_factory=dict)
    d: Dict[Tuple[int,int], Dict[int,int]] = field(default_factory=dict)
    s: Dict[Tuple[int,int], Dict[int,int]] = field(default_factory=dict)

    def __post_init__(self):
        for k in range(self.n + 1):
            self.simplices.setdefault(k, [])

    def add_simplex(self, k: int, data: object) -> int:
        assert 0 <= k <= self.n
        idx = len(self.simplices[k])
        self.simplices[k].append(data)
        return idx

    def set_face(self, k: int, i: int, sigma: int, face: int):
        self.d.setdefault((k,i), {})[sigma] = face

    def set_degeneracy(self, k: int, i: int, sigma: int, deg: int):
        self.s.setdefault((k,i), {})[sigma] = deg

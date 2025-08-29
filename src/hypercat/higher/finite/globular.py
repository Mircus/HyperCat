
from dataclasses import dataclass, field
from typing import Dict, List, Any

@dataclass
class FiniteGlobularSet:
    n: int
    cells: Dict[int, List[Any]] = field(default_factory=dict)
    s: Dict[int, Dict[int, int]] = field(default_factory=dict)
    t: Dict[int, Dict[int, int]] = field(default_factory=dict)

    def __post_init__(self):
        for k in range(self.n + 1):
            self.cells.setdefault(k, [])
        for k in range(1, self.n + 1):
            self.s.setdefault(k, {})
            self.t.setdefault(k, {})

    def add_cell(self, k: int, payload: Any, src: int = None, tgt: int = None) -> int:
        assert 0 <= k <= self.n, "dimension out of bounds"
        idx = len(self.cells[k])
        self.cells[k].append(payload)
        if k > 0:
            assert src is not None and tgt is not None, "need src/tgt for k>0"
            self.s[k][idx] = src
            self.t[k][idx] = tgt
        return idx


from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class Generator:
    dim: int
    name: str
    src: int
    tgt: int

@dataclass(frozen=True)
class Relation:
    dim: int
    lhs: Tuple[int, ...]
    rhs: Tuple[int, ...]
    name: str

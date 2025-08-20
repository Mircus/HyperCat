from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class Obj:
	name: str
	data: Optional[object] = None


@dataclass(frozen=True)
class ArrowGen:
	name: str
	source: str
	target: str


@dataclass(frozen=True)
class Formal1:
	# h∘...∘g∘f (rightmost applied first)
	factors: Tuple[str, ...]


@dataclass(frozen=True)
class Presentation:
	objects: Tuple[Obj, ...]
	arrows: Tuple[ArrowGen, ...]
	relations: Tuple[Tuple[Formal1, Formal1], ...] = ()


from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

from .presentation import Obj, ArrowGen, Formal1, Presentation


@dataclass(frozen=True)
class Cat:
	objects: Tuple[Obj, ...]
	arrows: Tuple[ArrowGen, ...]
	composition: Dict[Tuple[str, str], str]
	identities: Dict[str, str]

	@staticmethod
	def from_presentation(p: Presentation) -> "Cat":
		ids = {o.name: f"id:{o.name}" for o in p.objects}
		return Cat(p.objects, p.arrows, {}, ids)

	def compose(self, left: str, right: str) -> str:
		key = (left, right)
		if key not in self.composition:
			raise KeyError(f"composition not defined for ({left},{right})")
		return self.composition[key]

	def identity(self, obj_name: str) -> str:
		try:
			return self.identities[obj_name]
		except KeyError as e:
			raise KeyError(f"no identity for object {obj_name}") from e


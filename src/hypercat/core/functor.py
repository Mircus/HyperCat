from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Mapping, Tuple

from .presentation import Formal1
from .category import Cat


@dataclass(frozen=True)
class Functor:
	name: str
	object_map: Dict[str, str]
	morphism_map: Dict[str, str]


def apply_functor(F: Functor, path: Formal1) -> Formal1:
	factors = tuple(F.morphism_map[f] for f in path.factors)
	return Formal1(factors)


@dataclass(frozen=True)
class CatFunctor:
	name: str
	source: Cat
	target: Cat
	object_map: Mapping[str, str]
	morphism_map: Mapping[str, str]


class FunctorBuilder:
	def __init__(self, name: str, source: Cat, target: Cat):
		self.name = name
		self.source = source
		self.target = target
		self._obj: Dict[str, str] = {}
		self._mor: Dict[str, str] = {}

	def on_objects(self, mapping: Dict[str, str]) -> "FunctorBuilder":
		for s_name, t_name in mapping.items():
			self._obj[s_name] = t_name
		return self

	def on_morphisms(self, mapping: Dict[str, str]) -> "FunctorBuilder":
		for s_name, t_name in mapping.items():
			self._mor[s_name] = t_name
		return self

	def build(self) -> CatFunctor:
		# identities: ensure mapped
		for obj_name, id_src in self.source.identities.items():
			FX = self._obj.get(obj_name)
			if FX is None:
				raise AssertionError(f"missing object map for {obj_name}")
			id_tgt = self.target.identities.get(FX)
			if id_tgt is None:
				raise AssertionError(f"missing identity in target for {FX}")
			self._mor[id_src] = id_tgt

		# composition closure: add images of known composites
		changed = True
		while changed:
			changed = False
			for (g, f), gf in self.source.composition.items():
				if g in self._mor and f in self._mor and gf not in self._mor:
					self._mor[gf] = self.target.compose(self._mor[g], self._mor[f])
					changed = True

		F = CatFunctor(self.name, self.source, self.target, dict(self._obj), dict(self._mor))

		# Law checks: identities and composition preservation (fail-fast)
		for obj_name, id_src in self.source.identities.items():
			FX = F.object_map[obj_name]
			id_tgt = self.target.identities[FX]
			if F.morphism_map[id_src] != id_tgt:
				raise AssertionError(f"F(id_{obj_name}) ≠ id_{FX}")
		for (g, f), gf in self.source.composition.items():
			lhs = F.morphism_map.get(gf)
			if lhs is None:
				raise AssertionError(f"F not defined on composite {gf}")
			rhs = self.target.compose(F.morphism_map[g], F.morphism_map[f])
			if lhs != rhs:
				raise AssertionError(f"F(g∘f) ≠ F(g)∘F(f) for g={g}, f={f}")

		return F


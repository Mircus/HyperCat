from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .category import Cat
from .functor import CatFunctor


@dataclass(frozen=True)
class Natural:
	source: CatFunctor  # F
	target: CatFunctor  # G
	components: Mapping[str, str]  # key: object name X, value: morph name η_X in target cat


def check_naturality(eta: Natural) -> None:
	F, G = eta.source, eta.target
	if not (F.source is G.source and F.target is G.target):
		raise AssertionError("Functors must have same source/target for naturality")
	S: Cat = F.source
	T: Cat = F.target
	# Build arrow index for source to get endpoints
	name_to_arrow = {a.name: a for a in S.arrows}
	for a in S.arrows:
		f = a.name
		X = a.source
		Y = a.target
		if X not in eta.components or Y not in eta.components:
			raise AssertionError(f"Missing natural component for object {X or Y}")
		eta_X = eta.components[X]
		eta_Y = eta.components[Y]
		Ff = F.morphism_map.get(f)
		Gf = G.morphism_map.get(f)
		if Ff is None or Gf is None:
			raise AssertionError(f"Functor not defined on morphism {f}")
		# Check η_Y ∘ F(f) == G(f) ∘ η_X in target category
		try:
			left = T.compose(eta_Y, Ff)
			right = T.compose(Gf, eta_X)
		except KeyError as e:
			raise AssertionError(f"Composition missing while checking naturality for {f}: {e}")
		if left != right:
			raise AssertionError(f"Naturality failed on {f}: η_Y ∘ F(f) != G(f) ∘ η_X")


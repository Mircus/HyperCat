from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Sequence

from .category import Cat
from .laws import Law, LawResult, Violation, LawSuite


def _composable(C: Cat, f: str, g: str) -> bool:
	try:
		# Compose g ∘ f means (g,f) key
		C.compose(f, g)  # will raise if not defined
		return True
	except Exception:
		return False


@dataclass(frozen=True)
class _IdentitiesLaw(Law[Cat]):
	name: str = "identities"
	tags: Sequence[str] = ("category", "core")

	def run(self, C: Cat, config: Dict[str, object]) -> LawResult[Cat]:
		violations: List[Violation[Cat]] = []
		for obj_name, id_name in C.identities.items():
			# right and left identity for any morphism incident to obj
			for (left, right), h in C.composition.items():
				# right identity: (f, id_src) = f
				if right == id_name and h != left:
					violations.append(Violation(self.name, "f ∘ id_src ≠ f", {"f": left}))
				# left identity: (id_tgt, f) = f
				if left == id_name and h != right:
					violations.append(Violation(self.name, "id_tgt ∘ f ≠ f", {"f": right}))
		return LawResult(self.name, passed=(len(violations) == 0), violations=violations)


@dataclass(frozen=True)
class _AssociativityLaw(Law[Cat]):
	name: str = "associativity"
	tags: Sequence[str] = ("category", "core")

	def run(self, C: Cat, config: Dict[str, object]) -> LawResult[Cat]:
		limit = int(config.get("assoc_sample_limit", 0))  # 0 = exhaustive
		count = 0
		violations: List[Violation[Cat]] = []
		pairs = list(C.composition.keys())
		# iterate composable triples via composition table keys
		for (g, f) in pairs:
			for (h, g2) in pairs:
				if g2 != g:
					continue
				if limit and count >= limit:
					break
				count += 1
				try:
					left = C.composition[(h, C.composition[(g, f)])]
					right = C.composition[(C.composition[(h, g)], f)]
					if left != right:
						violations.append(
							Violation(self.name, "(h∘g)∘f ≠ h∘(g∘f)", {"h": h, "g": g, "f": f})
						)
				except Exception as e:
					violations.append(
						Violation(self.name, f"compose error: {e}", {"h": h, "g": g, "f": f})
					)
		return LawResult(self.name, passed=(len(violations) == 0), violations=violations)


CATEGORY_SUITE = LawSuite[Cat]("category-core", laws=[_IdentitiesLaw(), _AssociativityLaw()])



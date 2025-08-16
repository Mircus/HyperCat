from __future__ import annotations

from typing import List

from .laws import Law, LawResult, Violation, LawSuite
from .category import Cat
from .functor import CatFunctor


class _FunctorIds(Law[CatFunctor]):
    name = "functor-identities"
    tags = ("functor", "core")

    def run(self, F: CatFunctor, config):
        V: List[Violation] = []
        S, T = F.source, F.target
        for X in S.objects:
            id_src = S.identities[X.name] if isinstance(S.identities, dict) else S.identities[X]
            id_tgt = T.identities[F.object_map[X.name]] if isinstance(T.identities, dict) else T.identities[F.object_map[X]]
            if F.morphism_map.get(id_src) != id_tgt:
                V.append(Violation(self.name, f"F(id_{X.name}) ≠ id_{F.object_map.get(X.name, X)}", {"X": X.name}))
        return LawResult(self.name, passed=(len(V) == 0), violations=V)


class _FunctorComp(Law[CatFunctor]):
    name = "functor-composition"
    tags = ("functor", "core")

    def run(self, F: CatFunctor, config):
        V: List[Violation] = []
        S, T = F.source, F.target
        for (g, f), gf in S.composition.items():
            lhs = F.morphism_map.get(gf)
            try:
                rhs = T.compose(F.morphism_map[g], F.morphism_map[f])
            except Exception as e:
                V.append(Violation(self.name, f"compose error: {e}", {"g": g, "f": f}))
                continue
            if lhs != rhs:
                V.append(Violation(self.name, "F(g∘f) ≠ F(g)∘F(f)", {"g": g, "f": f}))
        return LawResult(self.name, passed=(len(V) == 0), violations=V)


FUNCTOR_SUITE = LawSuite[CatFunctor]("functor-core", laws=[_FunctorIds(), _FunctorComp()])



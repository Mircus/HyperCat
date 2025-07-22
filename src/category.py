
from typing import Set, Dict, Tuple, Optional
from .core import Object, Morphism

class Category:
    def __init__(self, name: str):
        self.name = name
        self.objects: Set[Object] = set()
        self.morphisms: Set[Morphism] = set()
        self.composition: Dict[Tuple[Morphism, Morphism], Morphism] = {}
        self.identities: Dict[Object, Morphism] = {}

    def add_object(self, obj: Object) -> 'Category':
        self.objects.add(obj)
        id_morph = Morphism(f"id_{obj.name}", obj, obj)
        self.morphisms.add(id_morph)
        self.identities[obj] = id_morph
        return self

    def add_morphism(self, morph: Morphism) -> 'Category':
        self.morphisms.add(morph)
        self.objects.add(morph.source)
        self.objects.add(morph.target)
        return self

    def set_composition(self, f: Morphism, g: Morphism, h: Morphism) -> 'Category':
        if f.target != g.source:
            raise ValueError("Cannot compose: source/target mismatch")
        if h.source != f.source or h.target != g.target:
            raise ValueError("Composition result has wrong source/target")
        self.composition[(g, f)] = h
        return self

    def compose(self, f: Morphism, g: Morphism) -> Optional[Morphism]:
        return self.composition.get((g, f))

    def is_valid(self) -> bool:
        for obj in self.objects:
            id_morph = self.identities.get(obj)
            if not id_morph:
                return False
            for f in self.morphisms:
                if f.source == obj and self.compose(f, id_morph) != f:
                    return False
                if f.target == obj and self.compose(id_morph, f) != f:
                    return False
        for f in self.morphisms:
            for g in self.morphisms:
                if f.target == g.source:
                    for h in self.morphisms:
                        if g.target == h.source:
                            hg = self.compose(g, h)
                            gf = self.compose(f, g)
                            if hg and gf:
                                if self.compose(f, hg) != self.compose(gf, h):
                                    return False
        return True

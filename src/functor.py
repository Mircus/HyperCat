
from typing import Dict, Optional
from .core import Object, Morphism
from .category import Category

class Functor:
    def __init__(self, name: str, source: Category, target: Category):
        self.name = name
        self.source = source
        self.target = target
        self.object_map: Dict[Object, Object] = {}
        self.morphism_map: Dict[Morphism, Morphism] = {}

    def map_object(self, obj: Object, target_obj: Object) -> 'Functor':
        if obj not in self.source.objects:
            raise ValueError(f"{obj} not in source category")
        if target_obj not in self.target.objects:
            raise ValueError(f"{target_obj} not in target category")
        self.object_map[obj] = target_obj
        return self

    def map_morphism(self, morph: Morphism, target_morph: Morphism) -> 'Functor':
        if morph not in self.source.morphisms:
            raise ValueError(f"{morph} not in source category")
        if target_morph not in self.target.morphisms:
            raise ValueError(f"{target_morph} not in target category")
        if self.object_map.get(morph.source) != target_morph.source or            self.object_map.get(morph.target) != target_morph.target:
            raise ValueError("Morphism mapping inconsistent with object mapping")
        self.morphism_map[morph] = target_morph
        return self

    def apply_to_object(self, obj: Object) -> Optional[Object]:
        return self.object_map.get(obj)

    def apply_to_morphism(self, morph: Morphism) -> Optional[Morphism]:
        return self.morphism_map.get(morph)

    def preserves_composition(self) -> bool:
        for (g, f), h in self.source.composition.items():
            F_f = self.apply_to_morphism(f)
            F_g = self.apply_to_morphism(g)
            F_h = self.apply_to_morphism(h)
            if F_f and F_g and F_h:
                if self.target.compose(F_f, F_g) != F_h:
                    return False
        return True

    def preserves_identities(self) -> bool:
        for obj, id_morph in self.source.identities.items():
            F_obj = self.apply_to_object(obj)
            F_id = self.apply_to_morphism(id_morph)
            if F_obj and F_id and self.target.identities.get(F_obj) != F_id:
                return False
        return True

    def is_valid(self) -> bool:
        return self.preserves_composition() and self.preserves_identities()

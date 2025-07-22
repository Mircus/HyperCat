
from typing import Dict, Optional
from .core import Object, Morphism
from .functor import Functor

class NaturalTransformation:
    def __init__(self, name: str, source_functor: Functor, target_functor: Functor):
        if source_functor.source != target_functor.source or source_functor.target != target_functor.target:
            raise ValueError("Functors must share domain and codomain")
        self.name = name
        self.source_functor = source_functor
        self.target_functor = target_functor
        self.components: Dict[Object, Morphism] = {}
        self.category = source_functor.source

    def set_component(self, obj: Object, morph: Morphism) -> 'NaturalTransformation':
        F_obj = self.source_functor.apply_to_object(obj)
        G_obj = self.target_functor.apply_to_object(obj)
        if morph.source != F_obj or morph.target != G_obj:
            raise ValueError("Component morphism has wrong source/target")
        self.components[obj] = morph
        return self

    def get_component(self, obj: Object) -> Optional[Morphism]:
        return self.components.get(obj)

    def is_natural(self) -> bool:
        for morph in self.category.morphisms:
            if morph.source in self.components and morph.target in self.components:
                alpha_A = self.components[morph.source]
                alpha_B = self.components[morph.target]
                F_f = self.source_functor.apply_to_morphism(morph)
                G_f = self.target_functor.apply_to_morphism(morph)
                if F_f and G_f:
                    left = self.source_functor.target.compose(F_f, alpha_B)
                    right = self.source_functor.target.compose(alpha_A, G_f)
                    if left != right:
                        return False
        return True

from typing import Set, Dict, Tuple
from hypercat.core.core import Category, Object, Morphism

class EnrichedCategory:
    """Category enriched over a monoidal category."""
    
    def __init__(self, name: str, enriching_category: Category):
        self.name = name
        self.enriching_category = enriching_category
        self.objects: Set[Object] = set()
        self.hom_objects: Dict[Tuple[Object, Object], Object] = {}
        self.composition_morphisms: Dict[Tuple[Object, Object, Object], Morphism] = {}
        self.unit_morphisms: Dict[Object, Morphism] = {}
    
    def add_object(self, obj: Object) -> 'EnrichedCategory':
        """Add an object to the enriched category."""
        self.objects.add(obj)
        return self
    
    def set_hom_object(self, A: Object, B: Object, hom_obj: Object) -> 'EnrichedCategory':
        """Set the hom-object [A,B] in the enriching category."""
        self.hom_objects[(A, B)] = hom_obj
        return self
    
    def set_composition(self, A: Object, B: Object, C: Object, 
                       comp_morph: Morphism) -> 'EnrichedCategory':
        """Set composition morphism [B,C] ⊗ [A,B] -> [A,C]."""
        self.composition_morphisms[(A, B, C)] = comp_morph
        return self


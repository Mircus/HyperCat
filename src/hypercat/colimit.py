class Colimit:
    """Represents a colimit of a diagram."""
    
    def __init__(self, colimiting_cocone: Cocone):
        self.cocone = colimiting_cocone
        self.colimit_object = colimiting_cocone.nadir
        self.injections = colimiting_cocone.injections
    
    def universal_property(self, other_cocone: Cocone, category: Category) -> Optional[Morphism]:
        """Find the unique morphism from colimit to other cocone's nadir (if exists)."""
        for morph in category.morphisms:
            if (morph.source == self.colimit_object and 
                morph.target == other_cocone.nadir):
                return morph
        return None


# Adjunctions

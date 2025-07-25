class Limit:
    """Represents a limit of a diagram."""
    
    def __init__(self, limiting_cone: Cone):
        self.cone = limiting_cone
        self.limit_object = limiting_cone.apex
        self.projections = limiting_cone.projections
    
    def universal_property(self, other_cone: Cone, category: Category) -> Optional[Morphism]:
        """Find the unique morphism from other cone's apex to limit (if exists)."""
        # This is a simplified implementation
        # In practice, you'd need more sophisticated checking
        for morph in category.morphisms:
            if (morph.source == other_cone.apex and 
                morph.target == self.limit_object):
                return morph
        return None

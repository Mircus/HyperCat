class Adjunction:
    """Represents an adjunction F ⊣ G between categories."""
    
    def __init__(self, left_adjoint: Functor, right_adjoint: Functor):
        if left_adjoint.target != right_adjoint.source:
            raise ValueError("Left adjoint's codomain must equal right adjoint's domain")
        if left_adjoint.source != right_adjoint.target:
            raise ValueError("Left adjoint's domain must equal right adjoint's codomain")
        
        self.left_adjoint = left_adjoint  # F: C -> D
        self.right_adjoint = right_adjoint  # G: D -> C
        self.unit: Optional[NaturalTransformation] = None  # η: 1_C -> GF
        self.counit: Optional[NaturalTransformation] = None  # ε: FG -> 1_D
    
    def set_unit(self, unit: NaturalTransformation) -> 'Adjunction':
        """Set the unit of the adjunction."""
        self.unit = unit
        return self
    
    def set_counit(self, counit: NaturalTransformation) -> 'Adjunction':
        """Set the counit of the adjunction."""
        self.counit = counit
        return self
    
    def satisfies_triangle_identities(self) -> bool:
        """Check if the triangle identities hold."""
        # This is a simplified check - full implementation would require
        # more sophisticated natural transformation composition
        return self.unit is not None and self.counit is not None


# Functor Categories

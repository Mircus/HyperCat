class NaturalTransformation:
    """Represents a natural transformation between functors."""
    
    def __init__(self, name: str, source_functor: Functor, target_functor: Functor):
        if source_functor.source != target_functor.source or \
           source_functor.target != target_functor.target:
            raise ValueError("Source and target functors must have same domain and codomain")
        
        self.name = name
        self.source_functor = source_functor
        self.target_functor = target_functor
        self.components: Dict[Object, Morphism] = {}
        self.category = source_functor.source
    
    def set_component(self, obj: Object, morph: Morphism) -> 'NaturalTransformation':
        """Set the component of the natural transformation at an object."""
        F_obj = self.source_functor.apply_to_object(obj)
        G_obj = self.target_functor.apply_to_object(obj)
        
        if not F_obj or not G_obj:
            raise ValueError(f"Functors not defined on object {obj}")
        
        if morph.source != F_obj or morph.target != G_obj:
            raise ValueError(f"Component morphism {morph} has wrong source/target")
        
        self.components[obj] = morph
        return self
    
    def get_component(self, obj: Object) -> Optional[Morphism]:
        """Get the component at an object."""
        return self.components.get(obj)
    
    def is_natural(self) -> bool:
        """Check if this transformation is natural (satisfies naturality condition)."""
        for morph in self.category.morphisms:
            if morph.source in self.components and morph.target in self.components:
                # Get components
                alpha_A = self.components[morph.source]  # α_A : F(A) -> G(A)
                alpha_B = self.components[morph.target]  # α_B : F(B) -> G(B)
                
                # Get functor applications
                F_f = self.source_functor.apply_to_morphism(morph)  # F(f) : F(A) -> F(B)
                G_f = self.target_functor.apply_to_morphism(morph)  # G(f) : G(A) -> G(B)
                
                if F_f and G_f:
                    target_cat = self.source_functor.target
                    
                    # Check naturality: α_B ∘ F(f) = G(f) ∘ α_A
                    left_comp = target_cat.compose(F_f, alpha_B)   # α_B ∘ F(f)
                    right_comp = target_cat.compose(alpha_A, G_f)  # G(f) ∘ α_A
                    
                    if left_comp != right_comp:
                        return False
        
        return True


# Limits and Colimits

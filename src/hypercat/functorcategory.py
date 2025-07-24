class FunctorCategory(Category):
    """Represents a functor category [C, D] of functors from C to D."""
    
    def __init__(self, source: Category, target: Category):
        super().__init__(f"[{source.name},{target.name}]")
        self.source_category = source
        self.target_category = target
        self._build_functor_category()
    
    def _build_functor_category(self):
        """Build the functor category structure."""
        # Objects are functors from source to target
        # This is a simplified version - in practice you'd want to enumerate
        # or construct functors more systematically
        pass
    
    def add_functor_object(self, functor: Functor) -> 'FunctorCategory':
        """Add a functor as an object in this functor category."""
        if functor.source != self.source_category or functor.target != self.target_category:
            raise ValueError("Functor doesn't match the functor category's source/target")
        
        functor_obj = Object(functor.name, functor)
        self.add_object(functor_obj)
        return self
    
    def add_natural_transformation(self, nat_trans: NaturalTransformation) -> 'FunctorCategory':
        """Add a natural transformation as a morphism."""
        source_obj = None
        target_obj = None
        
        # Find the functor objects corresponding to the source and target functors
        for obj in self.objects:
            if isinstance(obj.data, Functor):
                if obj.data == nat_trans.source_functor:
                    source_obj = obj
                elif obj.data == nat_trans.target_functor:
                    target_obj = obj
        
        if not source_obj or not target_obj:
            raise ValueError("Source or target functor not found in category")
        
        nat_trans_morph = Morphism(nat_trans.name, source_obj, target_obj, nat_trans)
        self.add_morphism(nat_trans_morph)
        return self
    
    def get_evaluation_functor(self, obj: Object) -> Functor:
        """Get the evaluation functor ev_A: [C,D] -> D."""
        if obj not in self.source_category.objects:
            raise ValueError("Object not in source category")
        
        eval_functor = Functor(f"ev_{obj.name}", self, self.target_category)
        
        # Map each functor F to F(obj)
        for functor_obj in self.objects:
            if isinstance(functor_obj.data, Functor):
                F = functor_obj.data
                F_obj = F.apply_to_object(obj)
                if F_obj:
                    eval_functor.map_object(functor_obj, F_obj)
        
        return eval_functor

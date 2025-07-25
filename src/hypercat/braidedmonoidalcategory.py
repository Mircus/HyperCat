class BraidedMonoidalCategory(MonoidalCategory):
    """Represents a braided monoidal category."""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.braiding: Dict[Tuple[Object, Object], Morphism] = {}
    
    def set_braiding(self, obj1: Object, obj2: Object, braiding_morph: Morphism) -> 'BraidedMonoidalCategory':
        """Set the braiding morphism β_{A,B}: A⊗B -> B⊗A."""
        self.braiding[(obj1, obj2)] = braiding_morph
        return self

class TwoCell:
    """Represents a 2-cell (2-morphism) in a 2-category."""
    
    def __init__(self, name: str, source: Morphism, target: Morphism):
        if source.source != target.source or source.target != target.target:
            raise ValueError("2-cell source and target must be parallel 1-morphisms")
        self.name = name
        self.source = source  # source 1-morphism
        self.target = target  # target 1-morphism
    
    def __str__(self):
        return f"{self.name}: {self.source.name} ⇒ {self.target.name}"

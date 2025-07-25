class Morphism:
    """Represents a morphism (arrow) between objects in a category."""
    
    def __init__(self, name: str, source: Object, target: Object, data: Any = None):
        self.name = name
        self.source = source
        self.target = target
        self.data = data
    
    def __str__(self):
        return f"{self.name}: {self.source} -> {self.target}"
    
    def __repr__(self):
        return f"Morphism({self.name}, {self.source.name}, {self.target.name})"
    
    def __eq__(self, other):
        return (isinstance(other, Morphism) and 
                self.name == other.name and 
                self.source == other.source and 
                self.target == other.target)
    
    def __hash__(self):
        return hash((self.name, self.source, self.target))

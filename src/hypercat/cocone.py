class Cocone:
    """Represents a cocone under a diagram."""
    
    def __init__(self, nadir: Object, diagram: Dict[Object, Object],
                 injections: Dict[Object, Morphism]):
        self.nadir = nadir
        self.diagram = diagram
        self.injections = injections
    
    def is_valid(self, category: Category) -> bool:
        """Check if this is a valid cocone."""
        # All injections must end at nadir
        for obj, inj in self.injections.items():
            if inj.target != self.nadir:
                return False
            if inj.source != self.diagram.get(obj):
                return False
        return True

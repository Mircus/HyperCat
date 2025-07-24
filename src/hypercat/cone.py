class Cone:
    """Represents a cone over a diagram."""
    
    def __init__(self, apex: Object, diagram: Dict[Object, Object], 
                 projections: Dict[Object, Morphism]):
        self.apex = apex
        self.diagram = diagram
        self.projections = projections
    
    def is_valid(self, category: Category) -> bool:
        """Check if this is a valid cone."""
        # All projections must start from apex
        for obj, proj in self.projections.items():
            if proj.source != self.apex:
                return False
            if proj.target != self.diagram.get(obj):
                return False
        return True

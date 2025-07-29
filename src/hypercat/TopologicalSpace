class TopologicalSpace:
    """Represents a topological space."""
    
    def __init__(self, name: str):
        self.name = name
        self.points: Set = set()
        self.open_sets: Set = set()
    
    def fundamental_groupoid(self) -> 'Groupoid':
        """Compute the fundamental groupoid."""
        return Groupoid(f"Π₁({self.name})")

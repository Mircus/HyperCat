class InfinityCategory:
    """Represents an (∞,1)-category."""
    
    def __init__(self, name: str):
        self.name = name
        self.objects: Set[Object] = set()
        self.morphisms: Dict[int, Set] = defaultdict(set)  # n-morphisms by dimension
        self.higher_compositions: Dict = {}
    
    def add_object(self, obj: Object) -> 'InfinityCategory':
        """Add an object (0-morphism)."""
        self.objects.add(obj)
        return self
    
    def add_n_morphism(self, n: int, morph: Any) -> 'InfinityCategory':
        """Add an n-morphism."""
        self.morphisms[n].add(morph)
        return self
    
    def nerve(self) -> 'SimplicalSet':
        """Compute the nerve of the ∞-category."""
        # Simplified implementation
        return SimplicalSet(f"Nerve({self.name})")

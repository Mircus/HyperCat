class SimplicialSet:
    """Represents a simplicial set."""
    
    def __init__(self, name: str):
        self.name = name
        self.simplices: Dict[int, Set] = defaultdict(set)  # n-simplices
        self.face_maps: Dict = {}
        self.degeneracy_maps: Dict = {}
    
    def add_simplex(self, n: int, simplex: Any) -> 'SimplicalSet':
        """Add an n-simplex."""
        self.simplices[n].add(simplex)
        return self
    
    def geometric_realization(self) -> 'TopologicalSpace':
        """Compute geometric realization (simplified)."""
        return TopologicalSpace(f"|{self.name}|")

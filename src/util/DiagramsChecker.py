class Path:
    """Represents a path of composable morphisms in a category."""
    
    def __init__(self, morphisms: List[Morphism]):
        if not morphisms:
            raise ValueError("Path cannot be empty")
        
        # Verify morphisms are composable
        for i in range(len(morphisms) - 1):
            if morphisms[i].target != morphisms[i + 1].source:
                raise ValueError(f"Morphisms not composable: {morphisms[i]} and {morphisms[i + 1]}")
        
        self.morphisms = morphisms
        self.source = morphisms[0].source
        self.target = morphisms[-1].target
    
    def __str__(self):
        if len(self.morphisms) == 1:
            return self.morphisms[0].name
        return " ∘ ".join(morph.name for morph in reversed(self.morphisms))
    
    def __eq__(self, other):
        return isinstance(other, Path) and self.morphisms == other.morphisms
    
    def __hash__(self):
        return hash(tuple(self.morphisms))
    
    def compose_with(self, other: 'Path') -> 'Path':
        """Compose this path with another: other ∘ self."""
        if self.target != other.source:
            raise ValueError("Paths not composable")
        return Path(self.morphisms + other.morphisms)
    
    def reverse(self) -> 'Path':
        """Return the reverse path (assuming all morphisms are invertible)."""
        # This assumes we have inverse morphisms available
        # In practice, you'd need to check if inverses exist
        return Path([morph for morph in reversed(self.morphisms)])


class CommutativeDiagram:
    """Represents a commutative diagram in a category."""
    
    def __init__(self, name: str, category: Category):
        self.name = name
        self.category = category
        self.objects: Set[Object] = set()
        self.morphisms: Set[Morphism] = set()
        self.paths: Dict[Tuple[Object, Object], List[Path]] = defaultdict(list)
        self.required_commutations: List[Tuple[Path, Path]] = []
        self.positions: Dict[Object, Tuple[int, int]] = {}  # For layout
    
    def add_object(self, obj: Object, position: Optional[Tuple[int, int]] = None) -> 'CommutativeDiagram':
        """Add an object to the diagram."""
        if obj not in self.category.objects:
            raise ValueError(f"Object {obj} not in category {self.category.name}")
        self.objects.add(obj)
        if position:
            self.positions[obj] = position
        return self
    
    def add_morphism(self, morph: Morphism) -> 'CommutativeDiagram':
        """Add a morphism to the diagram."""
        if morph not in self.category.morphisms:
            raise ValueError(f"Morphism {morph} not in category {self.category.name}")
        self.morphisms.add(morph)
        self.objects.add(morph.source)
        self.objects.add(morph.target)
        
        # Add as a single-morphism path
        path = Path([morph])
        self.paths[(morph.source, morph.target)].append(path)
        return self
    
    def add_path(self, morphisms: List[Morphism]) -> 'CommutativeDiagram':
        """Add a composite path to the diagram."""
        path = Path(morphisms)
        self.paths[(path.source, path.target)].append(path)
        
        # Add all morphisms and objects
        for morph in morphisms:
            self.add_morphism(morph)
        return self
    
    def require_commutativity(self, path1: Path, path2: Path) -> 'CommutativeDiagram':
        """Require that two paths commute (are equal)."""
        if path1.source != path2.source or path1.target != path2.target:
            raise ValueError("Paths must have same source and target to commute")
        self.required_commutations.append((path1, path2))
        return self
    
    def require_commutativity_by_morphisms(self, morphisms1: List[Morphism], 
                                         morphisms2: List[Morphism]) -> 'CommutativeDiagram':
        """Require commutativity between two paths specified by morphism lists."""
        path1 = Path(morphisms1)
        path2 = Path(morphisms2)
        return self.require_commutativity(path1, path2)
    
    def find_all_paths(self, source: Object, target: Object, max_length: int = 5) -> List[Path]:
        """Find all paths from source to target up to given length."""
        if source == target:
            # Identity path
            if source in self.category.identities:
                return [Path([self.category.identities[source]])]
            return []
        
        all_paths = []
        visited = set()
        
        def dfs(current_obj: Object, current_path: List[Morphism], remaining_length: int):
            if remaining_length <= 0:
                return
            
            if current_obj == target and current_path:
                all_paths.append(Path(list(current_path)))
                return
            
            for morph in self.morphisms:
                if morph.source == current_obj and morph not in current_path:
                    current_path.append(morph)
                    dfs(morph.target, current_path, remaining_length - 1)
                    current_path.pop()
        
        dfs(source, [], max_length)
        return all_paths
    
    def is_commutative(self) -> bool:
        """Check if all required commutations hold in the category."""
        for path1, path2 in self.required_commutations:
            if not self._paths_equal(path1, path2):
                return False
        return True
    
    def _paths_equal(self, path1: Path, path2: Path) -> bool:
        """Check if two paths are equal via category composition."""
        # Compose path1
        result1 = self._compose_path(path1)
        result2 = self._compose_path(path2)
        
        return result1 == result2
    
    def _compose_path(self, path: Path) -> Optional[Morphism]:
        """Compose a path to get the resulting morphism."""
        if len(path.morphisms) == 1:
            return path.morphisms[0]
        
        result = path.morphisms[0]
        for morph in path.morphisms[1:]:
            result = self.category.compose(result, morph)
            if result is None:
                return None
        return result
    
    def auto_detect_commutations(self, max_path_length: int = 3) -> 'CommutativeDiagram':
        """Automatically detect potential commutative squares/triangles."""
        # Find all pairs of objects
        for source in self.objects:
            for target in self.objects:
                if source != target:
                    paths = self.find_all_paths(source, target, max_path_length)
                    # If there are multiple paths, they might commute
                    for i in range(len(paths)):
                        for j in range(i + 1, len(paths)):
                            if len(paths[i].morphisms) > 1 or len(paths[j].morphisms) > 1:
                                self.require_commutativity(paths[i], paths[j])
        return self
    
    def set_object_position(self, obj: Object, x: int, y: int) -> 'CommutativeDiagram':
        """Set the position of an object for diagram layout."""
        self.positions[obj] = (x, y)
        return self
    
    def auto_layout(self) -> 'CommutativeDiagram':
        """Automatically layout objects in a grid."""
        objects_list = list(self.objects)
        n = len(objects_list)
        cols = int(n ** 0.5) + 1
        
        for i, obj in enumerate(objects_list):
            x = i % cols
            y = i // cols
            self.positions[obj] = (x, y)
        
        return self


class DiagramChecker:
    """Utilities for checking diagram properties."""
    
    @staticmethod
    def is_pullback_square(diagram: CommutativeDiagram, 
                          A: Object, B: Object, C: Object, P: Object,
                          f: Morphism, g: Morphism, p1: Morphism, p2: Morphism) -> bool:
        """Check if a square is a pullback."""
        # Basic checks
        if not (p1.source == P and p1.target == A and
                p2.source == P and p2.target == B and
                f.source == A and f.target == C and
                g.source == B and g.target == C):
            return False
        
        # Check commutativity: f ∘ p1 = g ∘ p2
        path1 = Path([p1, f])
        path2 = Path([p2, g])
        
        return diagram._paths_equal(path1, path2)
    
    @staticmethod
    def is_pushout_square(diagram: CommutativeDiagram,
                         A: Object, B: Object, C: Object, Q: Object,
                         f: Morphism, g: Morphism, i1: Morphism, i2: Morphism) -> bool:
        """Check if a square is a pushout."""
        # Basic checks
        if not (f.source == A and f.target == B and
                g.source == A and g.target == C and
                i1.source == B and i1.target == Q and
                i2.source == C and i2.target == Q):
            return False
        
        # Check commutativity: i1 ∘ f = i2 ∘ g
        path1 = Path([f, i1])
        path2 = Path([g, i2])
        
        return diagram._paths_equal(path1, path2)
    
    @staticmethod
    def find_commutative_triangles(diagram: CommutativeDiagram) -> List[Tuple[Object, Object, Object]]:
        """Find all commutative triangles in the diagram."""
        triangles = []
        objects = list(diagram.objects)
        
        for i in range(len(objects)):
            for j in range(i + 1, len(objects)):
                for k in range(j + 1, len(objects)):
                    A, B, C = objects[i], objects[j], objects[k]
                    
                    # Check if triangle A->B->C->A exists and commutes
                    paths_AB = diagram.find_all_paths(A, B, 2)
                    paths_BC = diagram.find_all_paths(B, C, 2)
                    paths_CA = diagram.find_all_paths(C, A, 2)
                    
                    if paths_AB and paths_BC and paths_CA:
                        # Check various combinations for commutativity
                        for path_AB in paths_AB:
                            for path_BC in paths_BC:
                                for path_CA in paths_CA:
                                    try:
                                        full_path = path_AB.compose_with(path_BC).compose_with(path_CA)
                                        if A in diagram.category.identities:
                                            id_path = Path([diagram.category.identities[A]])
                                            if diagram._paths_equal(full_path, id_path):
                                                triangles.append((A, B, C))
                                    except ValueError:
                                        continue
        
        return triangles


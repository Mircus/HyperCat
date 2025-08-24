from typing import Dict, Set, Optional, Any
from collections import defaultdict
from hypercat.core.core import Object, Morphism

# Operads and Algebraic Structures
class Operad:
    """Represents an operad."""
    
    def __init__(self, name: str):
        self.name = name
        self.operations: Dict[int, Set] = defaultdict(set)  # n-ary operations
        self.composition: Dict = {}
        self.unit: Optional[Any] = None
    
    def add_operation(self, arity: int, operation: Any) -> 'Operad':
        """Add an operation of given arity."""
        self.operations[arity].add(operation)
        return self
    
    def set_unit(self, unit_op: Any) -> 'Operad':
        """Set the unit operation."""
        self.unit = unit_op
        return self


class Algebra:
    """Represents an algebra over an operad."""
    
    def __init__(self, name: str, operad: Operad, underlying_object: Object):
        self.name = name
        self.operad = operad
        self.underlying_object = underlying_object
        self.structure_maps: Dict = {}
    
    def set_structure_map(self, operation: Any, structure_morph: Morphism) -> 'Algebra':
        """Set how an operad operation acts on the algebra."""
        self.structure_maps[operation] = structure_morph
        return self

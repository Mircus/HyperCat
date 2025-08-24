from typing import Dict, Tuple, Any

# Homotopy Type Theory Elements  
class HomotopyType:
    """Represents a homotopy type."""
    
    def __init__(self, name: str, level: int = 0):
        self.name = name
        self.level = level  # h-level: 0=contractible, 1=proposition, 2=set, etc.
        self.paths: Dict[Tuple[Any, Any], 'HomotopyType'] = {}
    
    def add_path_type(self, a: Any, b: Any, path_type: 'HomotopyType') -> 'HomotopyType':
        """Add a path type between two points."""
        self.paths[(a, b)] = path_type
        return self
    
    def is_contractible(self) -> bool:
        """Check if this is a contractible type (h-level 0)."""
        return self.level == 0
    
    def is_proposition(self) -> bool:
        """Check if this is a proposition (h-level 1)."""
        return self.level <= 1

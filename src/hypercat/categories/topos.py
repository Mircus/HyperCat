from typing import *
from hypercat.core.core import Category, Object, Morphism

class Topos(Category):
    """Represents an elementary topos."""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.terminal_object: Optional[Object] = None
        self.subobject_classifier: Optional[Object] = None
        self.truth_morphism: Optional[Morphism] = None
    
    def set_terminal_object(self, obj: Object) -> 'Topos':
        """Set the terminal object."""
        self.terminal_object = obj
        return self
    
    def set_subobject_classifier(self, omega: Object, true_morph: Morphism) -> 'Topos':
        """Set the subobject classifier Ω and true: 1 -> Ω."""
        self.subobject_classifier = omega
        self.truth_morphism = true_morph
        return self
    
    def has_finite_limits(self) -> bool:
        """Check if the topos has finite limits (simplified check)."""
        return self.terminal_object is not None
    
    def has_exponentials(self) -> bool:
        """Check if the topos has exponentials (simplified check)."""
        # In a real implementation, you'd check for exponential objects
        return True  # Assume true for elementary toposes


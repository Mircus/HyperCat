# Core classes
from .core import Object, Morphism, Category, Functor, NaturalTransformation

# Categories
from .categories import (
    StandardCategories,
    FunctorCategory,
    MonoidalCategory,
    BraidedMonoidalCategory,
    EnrichedCategory,
    Topos
)

# Higher categories
from .higher import (
    TwoCategory,
    TwoCell,
    InfinityCategory,
    HomotopyType,
    SimplicialSet
)

# Diagram tools
from .diagram import CommutativityChecker

# Algebraic structures
from .algebraic import Operad

__version__ = "0.1.0"

__all__ = [
    # Core
    'Object', 'Morphism', 'Category', 'Functor', 'NaturalTransformation',
    # Categories
    'StandardCategories', 'FunctorCategory', 'MonoidalCategory',
    'BraidedMonoidalCategory', 'EnrichedCategory', 'Topos',
    # Higher
    'TwoCategory', 'TwoCell', 'InfinityCategory', 'HomotopyType', 'SimplicialSet',
    # Diagram
    'CommutativityChecker',
    # Algebraic
    'Operad'
]

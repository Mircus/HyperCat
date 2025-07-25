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
        return self"""
Category Theory and Hypercategory Library

A comprehensive Python library for working with categories, functors, 
natural transformations, hypercategories, limits, colimits, adjunctions,
and functor categories.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Set, Tuple, Optional, Callable, Union, Generic, TypeVar
from dataclasses import dataclass
import itertools
import copy
from collections import defaultdict

T = TypeVar('T')
U = TypeVar('U')

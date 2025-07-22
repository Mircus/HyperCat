
from typing import Dict, Set, Tuple
from .core import Morphism
from .category import Category

class TwoCell:
    def __init__(self, name: str, source: Morphism, target: Morphism):
        if source.source != target.source or source.target != target.target:
            raise ValueError("2-cell source and target must be parallel")
        self.name = name
        self.source = source
        self.target = target

    def __str__(self):
        return f"{self.name}: {self.source.name} ⇒ {self.target.name}"

class TwoCategory(Category):
    def __init__(self, name: str):
        super().__init__(name)
        self.two_cells: Set[TwoCell] = set()
        self.vertical_composition: Dict[Tuple[TwoCell, TwoCell], TwoCell] = {}
        self.horizontal_composition: Dict[Tuple[TwoCell, TwoCell], TwoCell] = {}

    def add_two_cell(self, two_cell: TwoCell) -> 'TwoCategory':
        self.two_cells.add(two_cell)
        return self

    def set_vertical_composition(self, alpha: TwoCell, beta: TwoCell, gamma: TwoCell):
        if alpha.target != beta.source:
            raise ValueError("Vertical composition mismatch")
        self.vertical_composition[(beta, alpha)] = gamma
        return self

    def set_horizontal_composition(self, alpha: TwoCell, beta: TwoCell, gamma: TwoCell):
        self.horizontal_composition[(beta, alpha)] = gamma
        return self

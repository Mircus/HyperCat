from __future__ import annotations

from typing import Tuple

from .presentation import Formal1


def identity(name: str) -> Formal1:
	return Formal1((f"id:{name}",))


def compose(*paths: Formal1) -> Formal1:
	if not paths:
		raise ValueError("compose requires at least one path")
	factors: Tuple[str, ...] = tuple().__add__(())
	for p in paths:
		factors = factors + p.factors
	return Formal1(factors)


def normalize(path: Formal1) -> Formal1:
	return Formal1(tuple(f for f in path.factors if f))


from typing import Final
from ..core.presentation import Formal1


def action(name: str) -> str:
    return name


def seq(*skills: str) -> Formal1:
    return Formal1(tuple(skills))


PLAN_MODE: Final[str] = "sequential"


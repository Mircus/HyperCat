from dataclasses import dataclass
from typing import Final, Tuple, Union
from ..core.presentation import Formal1


def action(name: str) -> str:
    return name


def seq(*actions: str) -> Formal1:
    return Formal1(tuple(actions))


PLAN_MODE: Final[str] = "sequential"


# Structured, composable plan algebra for agents
@dataclass(frozen=True)
class Task:
    name: str


@dataclass(frozen=True)
class Sequence:
    items: Tuple["Plan", ...]


@dataclass(frozen=True)
class Parallel:
    items: Tuple["Plan", ...]


@dataclass(frozen=True)
class Choose:
    items: Tuple["Plan", ...]


Plan = Union[Task, Sequence, Parallel, Choose]


def task(name: str) -> Plan:
    return Task(name)


def _as_plan(item: Union[Plan, str]) -> Plan:
    return item if isinstance(item, (Task, Sequence, Parallel, Choose)) else Task(str(item))


def seqp(*items: Union[Plan, str]) -> Plan:
    return Sequence(tuple(_as_plan(i) for i in items))


def par(*items: Union[Plan, str]) -> Plan:
    return Parallel(tuple(_as_plan(i) for i in items))


def choose(*items: Union[Plan, str]) -> Plan:
    return Choose(tuple(_as_plan(i) for i in items))


# Preferred explicit name for parallel composition (alias of par)
def parallel(*items: Union[Plan, str]) -> Plan:
    return Parallel(tuple(_as_plan(i) for i in items))


# Preferred explicit name for sequential composition (alias of seqp)
def sequence(*items: Union[Plan, str]) -> Plan:
    return Sequence(tuple(_as_plan(i) for i in items))


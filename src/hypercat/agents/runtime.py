from typing import Any, Callable, Dict, Protocol
from inspect import signature
from ..core.presentation import Formal1


class Skill(Protocol):
    def __call__(self, x: Any, ctx: Any | None = None) -> Any: ...


def _call_skill(fn: Callable[..., Any], x: Any, ctx: Any | None) -> Any:
    sig = signature(fn)
    params = list(sig.parameters.values())
    # Accept exactly 1 or 2 parameters; anything else is an error
    if len(params) == 1:
        return fn(x)
    if len(params) == 2:
        return fn(x, ctx)
    raise TypeError("Skill must accept 1 (x) or 2 (x, ctx) parameters")


def strong_monoidal_functor(implementation: Dict[str, Skill], mode: str = "sequential"):
    if mode != "sequential":
        raise ValueError("Only sequential mode is supported")

    def F(plan: Formal1):
        def run(x: Any, ctx: Any | None = None):
            value = x
            for step in plan.factors:
                fn = implementation[step]
                value = _call_skill(fn, value, ctx)
            return value
        return run

    return F

# Re-export helper for agents
call_skill = _call_skill


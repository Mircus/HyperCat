from typing import Any, Callable, Dict, List, Protocol, Sequence
from inspect import signature
from ..core.presentation import Formal1
from .actions import Task, Sequence, Parallel, Choose, Plan


class Action(Protocol):
    def __call__(self, x: Any, ctx: Any | None = None) -> Any: ...


def _call_action(fn: Callable[..., Any], x: Any, ctx: Any | None) -> Any:
    sig = signature(fn)
    params = list(sig.parameters.values())
    # Accept exactly 1 or 2 parameters; anything else is an error
    if len(params) == 1:
        return fn(x)
    if len(params) == 2:
        return fn(x, ctx)
    raise TypeError("Action must accept 1 (x) or 2 (x, ctx) parameters")


def strong_monoidal_functor(implementation: Dict[str, Action], mode: str = "sequential"):
    if mode != "sequential":
        raise ValueError("Only sequential mode is supported")

    def F(plan: Formal1):
        def run(x: Any, ctx: Any | None = None):
            value = x
            for step in plan.factors:
                fn = implementation[step]
                value = _call_action(fn, value, ctx)
            return value
        return run

    return F

# Re-export helper for agents
call_action = _call_action


# Structured plan interpreter (Seq / Par / Choose)
ChooseFn = Callable[[List[Any]], int]
AggregateFn = Callable[[List[Any]], Any]


def _compile_plan(
    implementation: Dict[str, Action],
    plan: Plan,
    *,
    choose_fn: ChooseFn | None,
    aggregate_fn: AggregateFn | None,
):
    if isinstance(plan, Task):
        fn = implementation[plan.name]

        def run_atom(x: Any, ctx: Any | None = None) -> Any:
            return _call_action(fn, x, ctx)

        return run_atom

    if isinstance(plan, Sequence):
        runners = tuple(_compile_plan(implementation, p, choose_fn=choose_fn, aggregate_fn=aggregate_fn) for p in plan.items)

        def run_seq(x: Any, ctx: Any | None = None) -> Any:
            value = x
            for r in runners:
                value = r(value, ctx)
            return value

        return run_seq

    if isinstance(plan, Parallel):
        if aggregate_fn is None:
            raise AssertionError("Parallel requires an aggregate_fn to combine branch outputs")
        runners = tuple(_compile_plan(implementation, p, choose_fn=choose_fn, aggregate_fn=aggregate_fn) for p in plan.items)

        def run_par(x: Any, ctx: Any | None = None) -> Any:
            outputs = [r(x, ctx) for r in runners]
            return aggregate_fn(outputs)

        return run_par

    if isinstance(plan, Choose):
        if choose_fn is None:
            raise AssertionError("Choose requires a choose_fn to select a branch")
        runners = tuple(_compile_plan(implementation, p, choose_fn=choose_fn, aggregate_fn=aggregate_fn) for p in plan.items)

        def run_choose(x: Any, ctx: Any | None = None) -> Any:
            outputs = [r(x, ctx) for r in runners]
            idx = choose_fn(outputs)
            if not (0 <= idx < len(outputs)):
                raise AssertionError("choose_fn returned invalid index")
            return outputs[idx]

        return run_choose

    raise TypeError("Unknown Plan node")


def compile_structured_plan(
    implementation: Dict[str, Action],
    plan: Plan,
    *,
    choose_fn: ChooseFn | None = None,
    aggregate_fn: AggregateFn | None = None,
):
    return _compile_plan(implementation, plan, choose_fn=choose_fn, aggregate_fn=aggregate_fn)


from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, List, Mapping, Sequence, Tuple

from .actions import seq
from .runtime import strong_monoidal_functor, call_skill
from ..core.presentation import Formal1


Score = Any


@dataclass(frozen=True)
class StepTrace:
    name: str
    ok: bool
    duration_ms: float
    input_snapshot: Any | None
    output_snapshot: Any | None


@dataclass(frozen=True)
class RunReport:
    output: Any
    score: Score
    trace: Sequence[StepTrace]


def _now_ms() -> float:
    return time.perf_counter() * 1000.0


def run_plan(
    plan: Formal1,
    implementation: Mapping[str, Callable[..., Any]],
    input_value: Any,
    *,
    ctx: Any | None = None,
    evaluator: Callable[[Any], Score] | None = None,
    snapshot: bool = False,
) -> RunReport:
    F = strong_monoidal_functor(dict(implementation))
    value = input_value
    traces: List[StepTrace] = []
    for step in plan.factors:
        fn = implementation[step]
        before = value if snapshot else None
        t0 = _now_ms()
        try:
            value = call_skill(fn, value, ctx)
            ok = True
        except Exception:
            ok = False
            raise
        finally:
            duration = _now_ms() - t0
        after = value if snapshot else None
        traces.append(StepTrace(step, ok, duration, before, after))

    score: Score = evaluator(value) if evaluator is not None else None
    return RunReport(output=value, score=score, trace=tuple(traces))


def choose_best(
    candidates: Sequence[Formal1],
    implementation: Mapping[str, Callable[..., Any]],
    input_value: Any,
    *,
    ctx: Any | None = None,
    evaluator: Callable[[Any], Score],
    snapshot: bool = False,
) -> Tuple[Formal1, RunReport]:
    best: Tuple[Formal1, RunReport] | None = None
    for plan in candidates:
        report = run_plan(plan, implementation, input_value, ctx=ctx, evaluator=evaluator, snapshot=snapshot)
        if best is None or (report.score is not None and report.score > best[1].score):
            best = (plan, report)
    assert best is not None
    return best


def quick_functor_laws(
    implementation: Mapping[str, Callable[..., Any]],
    *,
    id_name: str | None = None,
    samples: Sequence[Any] = (),
    ctx: Any | None = None,
) -> None:
    # Check composition: running (f,g) equals applying f then g on samples
    names = list(implementation.keys())
    for f in names:
        for g in names:
            comp = seq(f, g)
            for x in samples:
                left = run_plan(comp, implementation, x, ctx=ctx).output
                right = call_skill(implementation[g], call_skill(implementation[f], x, ctx), ctx)
                if left != right:
                    raise AssertionError(f"Functor law failed: F({g}∘{f}) != F({g})∘F({f}) on {x}")
    # Identity if provided
    if id_name is not None:
        if id_name not in implementation:
            raise AssertionError(f"identity skill '{id_name}' not in implementation")
        for x in samples:
            if run_plan(seq(id_name), implementation, x, ctx=ctx).output != x:
                raise AssertionError("Identity law failed: F(id)(x) != x")


@dataclass(frozen=True)
class Agent:
    implementation: Mapping[str, Callable[..., Any]]
    evaluator: Callable[[Any], Score] | None = None
    snapshot: bool = False

    def run(self, plan: Formal1, input_value: Any, *, ctx: Any | None = None) -> RunReport:
        return run_plan(plan, self.implementation, input_value, ctx=ctx, evaluator=self.evaluator, snapshot=self.snapshot)

    def choose_best(
        self,
        candidates: Sequence[Formal1],
        input_value: Any,
        *,
        ctx: Any | None = None,
    ) -> Tuple[Formal1, RunReport]:
        if self.evaluator is None:
            raise AssertionError("Agent.choose_best requires an evaluator")
        return choose_best(candidates, self.implementation, input_value, ctx=ctx, evaluator=self.evaluator, snapshot=self.snapshot)


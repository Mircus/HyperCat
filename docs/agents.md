# Agents

Minimal, composable pipelines built from named actions.

## Terminology

- **Action**: a pure function `(x) -> y` or `(x, ctx) -> y` that transforms data. You implement actions.
- **Task**: a plan leaf that calls a named action. You compose tasks into plans.
- **Plan**: a composition of tasks. Two styles:
  - Sequential plan (`seq(...)`) over formal words (`Formal1`)
  - Structured plan using builders: `task`, `seqp`, `parallel`, `choose`
- **Sequence**: run child plans left-to-right.
- **Parallel**: run child plans concurrently and combine outputs via an explicit `aggregate_fn`.
- **Choose**: evaluate child plans and pick one via an explicit `choose_fn`.
- **Agent**: convenience wrapper for running plans and selecting the best among candidates with an evaluator.

If the names feel similar, remember: Task calls an Action. Actions are functions; Tasks are nodes in a plan.

## Define actions
```python
actions = {
  'denoise': lambda s, ctx=None: s.replace('~',''),
  'edges':   lambda s, ctx=None: ''.join(ch for ch in s if ch.isalpha()),
  'segment': lambda s, ctx=None: s.upper(),
  'merge':   lambda s, ctx=None: f"[{s}]",
}
```

## Compose a plan
```python
from hypercat.agents import seq
plan = seq('denoise','edges','segment','merge')
```

## Run and score
```python
from hypercat.agents import Agent
agent = Agent(actions, evaluator=lambda o: -len(o), snapshot=True)
report = agent.run(plan, "~a~b_c-1")
print(report.output, report.score)
```

## Choose best among candidates
```python
from hypercat.agents import choose_best
best_plan, best_report = choose_best(
  [plan, seq('denoise','segment','merge')],
  actions,
  "~a~b_c-1",
  evaluator=lambda o: -len(o),
)
```

## Structured plans (Sequence / Parallel / Choose)

```python
from hypercat.agents.actions import task, seqp, parallel, choose
from hypercat.agents.eval import run_structured_plan

structured = seqp(
  task('denoise'),
  parallel(task('edges'), task('segment')),
  task('merge'),
)

report = run_structured_plan(
  structured,
  actions,
  input_value="~a~b_c-1",
  aggregate_fn=lambda outs: ''.join(outs),   # combine Parallel outputs
  choose_fn=None,                            # not used here
  snapshot=True,
)
print(report.output)
```

```python
# Choose example: pick best branch by a custom chooser
branching = choose(task('segment'), task('merge'))
best = run_structured_plan(
  branching,
  actions,
  input_value="ab",
  choose_fn=lambda outs: max(range(len(outs)), key=lambda i: len(str(outs[i]))),
  aggregate_fn=None,
)
print(best.output)
```

## Functor sanity checks (empirical)
```python
from hypercat.agents import quick_functor_laws
quick_functor_laws({'f': lambda x: x+1, 'g': lambda x: x*2, 'id': lambda x: x}, id_name='id', samples=[0,1,2])
```

## Design constraints
- Actions must accept `(x)` or `(x, ctx)`
- Unsupported modes raise
- Deterministic execution; traces carry per-step timings and snapshots

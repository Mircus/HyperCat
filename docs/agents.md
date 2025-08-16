# Agents

Minimal, composable pipelines built from named skills.

## Define skills
```python
skills = {
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
agent = Agent(skills, evaluator=lambda o: -len(o), snapshot=True)
report = agent.run(plan, "~a~b_c-1")
print(report.output, report.score)
```

## Choose best among candidates
```python
from hypercat.agents import choose_best
best_plan, best_report = choose_best(
  [plan, seq('denoise','segment','merge')],
  skills,
  "~a~b_c-1",
  evaluator=lambda o: -len(o),
)
```

## Functor sanity checks (empirical)
```python
from hypercat.agents import quick_functor_laws
quick_functor_laws({'f': lambda x: x+1, 'g': lambda x: x*2, 'id': lambda x: x}, id_name='id', samples=[0,1,2])
```

## Design constraints
- Skills must accept `(x)` or `(x, ctx)`
- Unsupported modes raise
- Deterministic execution; traces carry per-step timings and snapshots

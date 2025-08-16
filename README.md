<p align="center">
  <img src="./HyperCat_logo.png" alt="HyperCat Logo" width="450"/>
</p>

# 🐾 HyperCat (minimal functional core)

> Typed, fail-fast core with a clean functional surface and optional agents. Core stays tiny; extras are opt-in.

---

## ✨ Features

- ✅ Object and morphism modeling  
- 🔁 Functors with composition and identity preservation  
- 🌀 Natural transformations with full naturality condition checks  
- 1️⃣ Focused on 1-categories; optional 2-cell diagram rendering via extras (no 2-category core)  
- 📦 Built-in standard categories: `Δⁿ`, terminal, discrete, walking isomorphism

---

## 🧠 Philosophy

**HyperCat** is built on the structural elegance of category theory and the agility of abstraction. It’s designed for:

- 📐 Research in category theory  
- 🧮 Computational modeling of categorical structures  
- 🧠 Experimental algebraic topology and homotopy  
- 🤖 Categorical foundations for machine learning and AI systems

---

## 🛠️ Setup (recommended: editable install)

Create a virtual environment and install the package locally (no publishing required):

```bash
cd hypercat
python -m venv .venv
source ./.venv/bin/activate
pip install -U pip
pip install -e .
```

---

## 📚 Getting Started (Core)

See `docs/getting-started.md`, or run:

```python
from hypercat.core.presentation import Obj, ArrowGen, Formal1, Presentation

objects = (Obj("A"), Obj("B"))
arrows = (ArrowGen("f","A","B"),)
pres = Presentation(objects, arrows)
```

## ▶️ Run & Develop

- Quick demo:

```python
from hypercat.core.standard import discrete
from hypercat.core.ops import identity

Disc = discrete(["A","B"])  # 1-category with only identities
print(Disc.objects)
print(identity("A"))
```

- Optional: run tests (requires `pytest`):

```bash
pytest -q
```

- Optional: type-check and lint (requires `mypy`, `ruff`):

```bash
mypy --strict src
ruff check .
```

- Generate Mermaid diagrams (no install needed):

```python
from hypercat.core.standard import simplex, walking_isomorphism, terminal_category, discrete
from hypercat.core.functor import FunctorBuilder
from hypercat.core.natural import Natural
from hypercat.extras.viz_mermaid import render_all, TwoCellView

Delta3 = simplex(3)
Iso    = walking_isomorphism()
Term   = terminal_category()
DiscAB = discrete(["A","B"]) 

F = (FunctorBuilder('F', source=Delta3, target=Iso)
     .on_objects({"0":"A","1":"A","2":"B","3":"B"})
     .on_morphisms({"0->1":"id:A","1->2":"f","2->3":"id:B","0->3":"f"})
     .build())
eta = Natural(source=F, target=F, components={"0":"id:A","1":"id:A","2":"id:B","3":"id:B"})
alpha = TwoCellView('α','X','Y','f','g')

render_all({
  'Delta3': Delta3,
  'Iso': Iso,
  'Terminal': Term,
  'DiscreteAB': DiscAB,
  'F': F,
  'eta': eta,
  'alpha': alpha,
}, out_dir='docs/diagrams')
```

## 🤖 Run the agent

Minimal end-to-end example with a runner and scorer:

```python
from hypercat.agents.actions import seq
from hypercat.agents.eval import Agent

actions = {
  'denoise': lambda s, ctx=None: s.replace('~',''),
  'edges':   lambda s, ctx=None: ''.join(ch for ch in s if ch.isalpha()),
  'segment': lambda s, ctx=None: s.upper(),
  'merge':   lambda s, ctx=None: f"[{s}]",
}

agent = Agent(implementation=actions, evaluator=lambda out: len(out))
plan1 = seq('denoise','merge')
plan2 = seq('denoise','edges','segment','merge')

best_plan, report = agent.choose_best([plan1, plan2], "~a~b_c-1")
print(best_plan.factors)  # ('denoise','edges','segment','merge')
print(report.output)      # [ABC]
print(report.score)       # e.g., 5
```

Generate a Mermaid Gantt of the execution trace:

```python
from hypercat.extras.viz_mermaid import exec_gantt_mermaid
print(exec_gantt_mermaid(report))
```

## 🤖 Agents (sample)

```python
from hypercat.agents.actions import seq
from hypercat.agents.runtime import strong_monoidal_functor

actions = {
  'denoise': lambda s: s.replace('~',''),
  'edges':   lambda s: ''.join(ch for ch in s if ch.isalpha()),
  'segment': lambda s: s.upper(),
  'merge':   lambda s: f"[{s}]",
}

plan = seq('denoise','edges','segment','merge')
F = strong_monoidal_functor(actions)
print(F(plan)("~a~b_c-1"))  # -> [ABC]
```

More tutorials and notebooks coming soon.

---

## 🔭 Future upgrade: n-categories (non-breaking roadmap)

- Guiding principles
  - Keep the 1-category core unchanged (`src/hypercat/core/{presentation.py, category.py, ops.py, functor.py, natural.py, laws_*.py}`).
  - Add higher-dimensional code in new modules; pure functions only; fail-fast checks.

- Data model (strict n-cats as computads)
  - Generators per dimension (k-cells), boundary maps, and formal composites.
  - Validate boundaries at composition time; no placeholder fallbacks.

- Package layout (new)
  - `src/hypercat/core/ncat/`: `presentation_n.py`, `ops_n.py`, `functor_n.py`, `laws_ncategory.py`, `convert_n.py`.

- Laws and checks
  - Suites per k for units/associativity; 2D interchange; aggregate `NCATEGORY_SUITE(n)`.

- Phase 1: strict 2-categories
  - Operations: `vcompose2`, `hcompose2`, whiskering, identities `id2(f)`.
  - Laws: unit/assoc for vertical; functoriality of horizontal; strict interchange.

- Visualization (optional)
  - Extend `extras/viz_mermaid.py` with whiskering/hcomp helpers; extras remain opt-in.

- Testing
  - New tests alongside existing suites (no API breaks); property/meta tests for boundaries.

---

## 🔬 Future enhancement: composable agents (functional algebra)

- Guiding principles
  - Keep the 1-category core unchanged and tiny; all agent orchestration remains optional and fail-fast.
  - Pure functions only; strong typing (no `Any` in public APIs); no hidden fallbacks.

- Plan algebra (typed, composable)
  - Concepts:
    - **Action**: a pure function `(state) -> state` or `(state, ctx) -> state`.
    - **Task**: a plan leaf that invokes a named action.
    - **Plan**: a tree describing how tasks compose.
  - Nodes:
    - `Task`: run a single named action.
    - `Sequence`: run child plans left-to-right.
    - `Parallel`: run child plans in parallel and aggregate outputs via an explicit `aggregate_fn`.
    - `Choose`: evaluate child plans and select one by an explicit `choose_fn` (or evaluator wiring at the agent layer).
  - Builders: `task(name)`, `sequence(...)`, `parallel(..., aggregate_fn=...)`, `choose(..., choose_fn=...)`.
  - Strict invariants: `Parallel` requires an aggregator; `Choose` requires a chooser; both validated fail-fast.

- Focused transforms with lenses
  - `Lens[S, A]` to zoom into a substate; `focus(lens, plan)` composes inner plans on `A` and lifts back to `S` immutably.

- Loops/recursion
  - `loop_while(predicate, body_plan)` applies `body_plan` while the predicate holds; pure and deterministic.

- Tracing and durability
  - Hierarchical `TraceNode` tree mirroring plan structure with timestamps and optional snapshots.
  - Optional durable event log and time-travel debugging implemented in `extras/` (opt-in, never imported by core).

- Concurrency (optional)
  - Async interpreter for `Parallel` with deterministic aggregation; sync remains the default. Fail-fast if used without async support.

- Decision wiring
  - `Choose` can use an explicit `choose_fn` or an agent-level evaluator to pick branches (no silent defaults).

- Resilience utilities (extras only)
  - Pure decorators: `retry`, `throttle`, `cache`; explicit parameters, no global state.
  - Robust JSON extraction helpers for LLM outputs (schema-driven), kept out of core.

- Sample usage (sketch)
  
  ```python
  from hypercat.agents.actions import task, seqp, parallel, choose  # optional module
  from hypercat.agents.eval import run_structured_plan         # optional module

  impl = {
    'clean':   lambda s, ctx=None: s.strip(),
    'upper':   lambda s, ctx=None: s.upper(),
    'summ':    lambda s, ctx=None: s,        # placeholder pure actions
    'keywords':lambda s, ctx=None: s,
  }

  plan = sequence(
    task('clean'),
    parallel(task('summ'), task('keywords')),   # requires aggregate_fn at run time
    choose(task('upper'), task('clean'))   # requires choose_fn at run time
  )

  report = run_structured_plan(
    plan,
    impl,
    input_value="  hello world  ",
    aggregate_fn=lambda outs: tuple(outs),
    choose_fn=lambda outs: 0,  # pick first branch
    snapshot=True,
  )
  print(report.output)
  ```

This roadmap keeps HyperCat’s core categorical model pristine while offering a principled, typed, and composable agent layer as an optional enhancement.

### Future improvements (prioritized)

1) Strong typing for agents
- Introduce generics: `Action[State, Ctx, Out]`, parameterized `Plan[State, Ctx, Out]`.
- Reduce/eradicate `Any` in public agent APIs.

2) Structured trace tree
- Hierarchical `TraceNode` per plan node with event ids, timestamps, before/after snapshots.

3) Extras: helpers for explicit composition
- Aggregators: `aggregate_tuple`, `aggregate_concat`, `aggregate_merge_dicts`.
- Choosers: `choose_argmax`, `choose_argmin` by scoring function.

4) Async parallel interpreter (optional)
- `compile_structured_plan_async` with deterministic aggregation order.

5) Lenses and loops
- `Lens[S, A]` and `focus(lens, plan)` for substate transforms.
- `loop_while(predicate, body_plan)` for bounded iteration.

6) Agent quality-of-life
- Let `Agent` provide an evaluator-backed `choose_fn` wiring for `Choose`.
- Add end-to-end examples mixing seq/parallel/choose/focus/loop.

## 🧵 Motto

<p align="center">
  <em>"The fabric of higher structures"</em>
</p>

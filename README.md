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

skills = {
  'denoise': lambda s, ctx=None: s.replace('~',''),
  'edges':   lambda s, ctx=None: ''.join(ch for ch in s if ch.isalpha()),
  'segment': lambda s, ctx=None: s.upper(),
  'merge':   lambda s, ctx=None: f"[{s}]",
}

agent = Agent(implementation=skills, evaluator=lambda out: len(out))
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

skills = {
  'denoise': lambda s: s.replace('~',''),
  'edges':   lambda s: ''.join(ch for ch in s if ch.isalpha()),
  'segment': lambda s: s.upper(),
  'merge':   lambda s: f"[{s}]",
}

plan = seq('denoise','edges','segment','merge')
F = strong_monoidal_functor(skills)
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

## 🧵 Motto

<p align="center">
  <em>"The fabric of higher structures"</em>
</p>

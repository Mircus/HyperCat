# Core (deep dive)

Minimal, functional, law‑centric core. No side‑effects; fail‑fast on invalid state. Everything composes via small typed dataclasses and plain dictionaries.

## Design principles
- Functional and composable: tiny pure functions; orchestration at the edges
- Law‑centric: category laws shipped as suites; proofs helpers for universal properties
- Fail‑fast: no silent fallbacks; raise on invalid inputs or missing data
- Names as primary keys: arrows and identities are addressed by names for clarity and portability
- Strong typing: frozen dataclasses; narrow APIs; explicit mappings

## Data model at a glance
- Objects are named (`Obj.name: str`)
- Arrows (generators) are named with `source` and `target` object names
- Formal paths (`Formal1`) are tuples of arrow names (rightmost applied first)
- Categories (`Cat`) are explicit tables over names:
  - `objects: Tuple[Obj, ...]`
  - `arrows: Tuple[ArrowGen, ...]`
  - `composition: Dict[Tuple[str,str], str]` mapping `(g,f) → h` by names
  - `identities: Dict[str,str]` mapping `object_name → id:object_name`

Identity naming convention: `id:<ObjName>`

---

## `presentation.py`
Purpose: immutable, minimal syntax for presentations and formal paths.

Key types:
- `Obj(name: str, data: object | None = None)`
- `ArrowGen(name: str, source: str, target: str)`
- `Formal1(factors: Tuple[str, ...])` — factors are arrow/identity names
- `Presentation(objects, arrows, relations)` where `relations` are pairs of `Formal1`

Invariants:
- Names must be unique per presentation layer
- `Formal1` contains only names; no evaluation

Failure modes: none (structural container only)

---

## `builder.py`
Purpose: helpers to build well‑formed presentations and auto‑inject identities.

API:
- `obj(name, data=None) -> Obj`
- `arrow(name, source, target) -> ArrowGen`
- `build_presentation(objects, arrows, relations=()) -> Presentation`
  - Adds identities `id:<ObjName>` for every object
  - Validates duplicate arrow names and raises `ValueError` on conflict

Invariants:
- Identity arrows are always present in returned `Presentation`

Failure modes:
- Duplicate generator names → `ValueError("Duplicate arrow name: ...")`

---

## `category.py`
Purpose: explicit category instance (small, finite) with composition/identities tables.

Type:
- `Cat(objects, arrows, composition, identities)` (all immutable/frozen)

Helpers:
- `Cat.from_presentation(presentation) -> Cat` (prepopulates identities by convention; empty composition)
- `compose(left: str, right: str) -> str` on the `Cat` instance
- `identity(obj_name: str) -> str`

Conventions:
- Composition uses names: calling `C.compose("f","g")` looks up key `("f","g")` in `C.composition`

Failure modes (fail‑fast):
- Unknown composition key → `KeyError("composition not defined for (...))")`
- Missing identity → `KeyError("no identity for object ...")`

Notes:
- `Cat` does not attempt to infer/complete compositions; you must specify the table entries you need

---

## `ops.py`
Purpose: path‑level utilities over `Formal1`.

API:
- `identity(object_name: str) -> Formal1` returns `("id:<ObjName>",)`
- `compose(*paths: Formal1) -> Formal1` concatenates factors, rightmost applied first
- `normalize(path: Formal1) -> Formal1` removes empty factors (no rewrite semantics)

Semantics:
- These are syntactic path ops, independent of any `Cat`; evaluation is your responsibility

Failure modes:
- `compose()` without arguments → `ValueError`

---

## `functor.py`
Two layers depending on your needs.

1) Minimal path functor
- `Functor(name, object_map: Dict[str,str], morphism_map: Dict[str,str])`
- `apply_functor(F, path: Formal1) -> Formal1` maps factors by name

2) Category functor (with law checks)
- `CatFunctor(name, source: Cat, target: Cat, object_map, morphism_map)`
- `FunctorBuilder(name, source, target)`:
  - `.on_objects({"A":"A", ...})`
  - `.on_morphisms({"f":"f", ...})`
  - `.build()` populates identities, closes over known composites, and checks laws

Fail‑fast checks in `build()`:
- Missing object map for a source object → `AssertionError`
- Identity preservation fails → `AssertionError("F(id_X) ≠ id_{F(X)}")`
- Composition preservation fails or composite missing → `AssertionError`

---

## `natural.py`
Purpose: minimal natural transformation and a checker.

Types:
- `Natural(source: CatFunctor, target: CatFunctor, components: Mapping[str,str])`
  - `components` maps object names `X` to morphism names `η_X` in the target category

Checker:
- `check_naturality(eta)` enforces that for every arrow `f: X→Y` in the source,
  `η_Y ∘ F(f) == G(f) ∘ η_X` in the target (via `Cat.composition` tables)

Failure modes:
- Different source/target functors → `AssertionError`
- Missing components or missing composition entries in target → `AssertionError`

Limitations (by design):
- Works over named tables; no term rewriting or higher structure assumed

---

## `convert.py`
Purpose: JSON‑ish serialization helpers for presentations.

API:
- `to_dict(p: Presentation) -> Dict[str, Any]`
- `from_dict(d: Dict[str, Any]) -> Presentation`

Notes:
- Only presentations, not `Cat` (since `Cat` requires explicit composition semantics)

---

## `laws.py` (engine)
Purpose: generic law engine with no CT specifics.

Types/APIs:
- `Violation(law, message, witness, severity)`
- `LawResult(law, passed, violations)`
- `Law` protocol: `.run(ctx, config) -> LawResult`
- `LawSuite(name, laws)`
- `SuiteReport(suite, results)`, with `.ok` and `.to_text()`
- `run_suite(ctx, suite, config=None) -> SuiteReport`

Usage:
- Compose suites per structure (categories, functors, adapters) without bloating core modules

---

## `laws_category.py`
Purpose: ready‑to‑run category laws built on the engine.

Suite:
- `CATEGORY_SUITE` with two laws:
  - Identities: left/right unit behavior using `Cat.composition`
  - Associativity: checks available triples in the composition table, with sampling control (`assoc_sample_limit`)

---

## `proofs.py`
Purpose: pragmatic, math‑friendly checkers and certificate formatting.

Checkers:
- Axioms: `check_category_axioms(C)`
- Universal properties: `is_terminal_object(C, T_name)`, `is_product(C, X, Y, P, pi1, pi2)`, `is_iso(C, f, g)`
- Thinness: `check_simplex_thin(C)`
- Functor/naturality: `check_functor_axioms(F)`, `check_naturality(η)`

Certificates:
- `certificate(label, *reports) -> str` yields human‑readable summary for PRs/CI logs

When to pick `proofs.py` vs `laws.py`:
- `laws.py`: reusable, structured, per‑suite results
- `proofs.py`: quick sanity with strong mathematical vocabulary and a single OK/FAIL line

---

## How modules compose
- Start with `Presentation` (syntax) using `builder.py`
- Lift to `Cat` with `Cat.from_presentation` (identities prefilled; you define `composition` entries you need)
- Evaluate/transform paths with `ops.py` or map them with `functor.py`
- Enforce correctness with `laws_category.CATEGORY_SUITE` or `proofs.py` helpers

---

## Failure behavior summary (fail‑fast)
- Duplicate arrow names in builder → `ValueError`
- Missing composition entry in `Cat.compose` → `KeyError`
- Missing identity in `Cat.identity` → `KeyError`
- Functor build without object maps or broken laws → `AssertionError`
- Naturality with missing components or missing target compositions → `AssertionError`
- Path ops misuse (e.g., `compose()` with no args) → `ValueError`

---

## Extension points
- Add new law suites with `laws.py` against any context `T`
- Define new structures under `core/` as pure modules (e.g., enrichment, standard categories) and pair with a `LawSuite`
- For runtime adapters or integrations, place orchestration code under `agents/` or `plugins/`, never in `core/`

---

## Examples (quick)
```python
# Build a tiny category with h = g∘f
from hypercat.core.presentation import Obj, ArrowGen
from hypercat.core.category import Cat
from hypercat.core import run_suite, CATEGORY_SUITE

A,B,C = Obj('A'), Obj('B'), Obj('C')
arrows = (
  ArrowGen('id:A','A','A'), ArrowGen('id:B','B','B'), ArrowGen('id:C','C','C'),
  ArrowGen('f','A','B'), ArrowGen('g','B','C'), ArrowGen('h','A','C'),
)
comp = { ('g','f'): 'h' }
ids  = { 'A':'id:A', 'B':'id:B', 'C':'id:C' }
Ccat = Cat((A,B,C), arrows, comp, ids)

report = run_suite(Ccat, CATEGORY_SUITE)
assert report.ok, report.to_text()
```

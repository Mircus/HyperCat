
# HyperCat Action List
**Assignee: Kishore**

This document lists the cleanup and consolidation steps required to make HyperCat ready for an official release. Focus areas: structure, imports, and deduplication.

---

## 1. Repository Structure
- **Keep `src/` layout** and normalize into:
  - `src/hypercat/core/` → *single* source of truth for `Category`, `Object`, `Morphism`, composition, identity, base Functor, base Natural Transformation.
  - `src/hypercat/categories/` → ready-to-use categories (Set, FinSet, Top, Ab, …) and enriched structures (Monoidal, Braided, FunctorCategory).
  - `src/hypercat/higher/` → higher categories: 2-categories, ∞-categories, homotopy/simplicial (SimplicialSet, HomotopyType).
  - `src/hypercat/diagram/` → diagram drawing and commutativity checking.
  - `src/hypercat/algebraic/` → operads and algebraic structures, if needed.
  - `examples/` (merge `demo/` into `examples/`). Remove `demo/`.

- **Rename files to snake_case** (avoid capital letters):
  - `EnrichedCategory.py` → `enriched_category.py`
  - `HomotopyType.py` → `homotopy_type.py`
  - `TopologicalSpace.py` → `topological_space.py`

- **Remove redundant dirs**:
  - Merge `demo/` into `examples/`.
  - If `dsl/` is an experiment, move to `experimental/` or archive it.

---

## 2. Imports
- **Golden rule**: all base objects come from `hypercat.core`.
  - Example allowed:
    ```python
    from hypercat.core import Category, Object, Morphism, Functor, NaturalTransformation, compose, id
    ```
  - Higher-level modules can import from `hypercat.categories`, `hypercat.higher`, `hypercat.diagram`.

- **Normalize imports**: use absolute imports only (`from hypercat...`). No relative imports.

- **Remove redefinitions**: if modules redefine `Category`, `Object`, `Morphism`, remove them and import from `hypercat.core` instead.

---

## 3. Deduplication
- **Duplicate classes**: For each duplicate (see analysis table), pick a canonical definition (usually in `core/`). Delete other copies and replace with imports.

- **Standard categories**: `standardcategories.py` vs `core/standardcats.py` → keep only one, ideally `hypercat/categories/standard.py`.

- **Monoidal & Braided**:
  - Move `monoidalcategory.py` → `hypercat/categories/monoidal.py`.
  - Move `braidedmonoidalcategory.py` → `hypercat/categories/braided.py`.

- **Topos & FunctorCategory**: move to `hypercat/categories/`. They must only import from `core`.

- **Higher categories**: move `twocategory.py` and `infinitycategory.py` to `hypercat/higher/`. Depend only on `core` interfaces.

- **Diagram**: keep `diagram/` isolated, depends only on `core`.

---

## 4. Packaging & Build
- Choose one build system: prefer `pyproject.toml` with setuptools/PEP 517. Archive `setup.py` and keep `MANIFEST.in` only if strictly necessary.

- `__init__.py`: export a minimal public API, re-exporting canonical symbols from the new locations.

---

## 5. Execution Order
1. **Phase 1 – Mapping & Renaming**
   - Rename files to snake_case.
   - Move files to new folders without changing public signatures.
   - Add temporary re-exports in `__init__.py` for compatibility.

2. **Phase 2 – Canonicalization**
   - Pick canonical class definitions and remove duplicates.
   - Fix all suspicious imports → they must go through `hypercat.core` or new modules.

3. **Phase 3 – Remove Compatibility Aliases**
   - Once tests pass, remove temporary aliases.

4. **Phase 4 – Examples**
   - Merge `demo/` into `examples/`.
   - Update notebooks with the new import paths.

---

## 6. Definition of Done
- No filenames with capital letters.
- No base classes defined outside `hypercat.core`.
- Zero duplicate class definitions.
- Zero suspicious imports.
- All imports are absolute (`from hypercat...`).
- `examples/` is the single examples directory, notebooks runnable with new imports.



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


---

## 7. Import Validation Test
After restructuring and fixing imports, verify that the package can be imported cleanly:

```bash
# From repo root
pip install -e .

# In Python REPL
import hypercat
print(hypercat.__version__)
```

- Ensure no `ImportError` or circular import issues occur.
- Run `pytest` to confirm that the test suite executes without errors.

---

## 8. Documentation & Examples Validation
- **README.md**: Update to reflect the new folder structure and correct import paths.
- **Notebooks** (`examples/`):
  - Run each notebook end-to-end and confirm it executes without modification.
  - Ensure outputs are consistent and explanatory.
- **Docs folder**:
  - Remove outdated files (`HyperCat Manual-v1.0.pdf`, `documentation.txt`) or rewrite them in Markdown/Sphinx.
  - Cross-link notebooks and examples in README or a dedicated docs index.
- **Contributing guide**: Update `CONTRIBUTING.md` with testing instructions and coding standards.

---

## 9. Final Checklist
- [ ] Repo installs with `pip install -e .` and imports cleanly.
- [ ] All notebooks run successfully under the new structure.
- [ ] Documentation matches actual code (no stale instructions).
- [ ] Old/duplicate docs removed or archived.
- [ ] Public API documented in README and/or Sphinx.

---

## 7. Verification & QA (Imports, Docs, Examples)

### 7.1 Package Import Smoke Test (must pass locally and in CI)
- Create a clean virtual environment and install the package in editable mode:
  - `python -m venv .venv && source .venv/bin/activate` (Windows: `.\.venv\Scriptsctivate`)
  - `pip install -U pip`
  - `pip install -e .`
- **Smoke test**: verify base imports and version are reachable:
  - `python - <<'PY'
import hypercat
from hypercat.core import Category, Object, Morphism
print('hypercat ok:', getattr(hypercat, '__version__', 'unknown'))
PY`
- Ensure no import relies on the working directory (i.e., `cd` anywhere and re-run).
- Repeat under the supported Python versions (see Test Matrix).

### 7.2 CI: Automated Import Test
- Add a GitHub Actions workflow that runs on pull requests and `main`:
  - Strategy matrix: `os: [ubuntu-latest, macos-latest, windows-latest]`, `python: [3.9, 3.10, 3.11, 3.12]`.
  - Steps: checkout → setup Python → `pip install -e .` → run the **Smoke test** script.
- Cache pip to speed builds.

### 7.3 Examples & Notebooks Validation
- Unify all examples under `examples/`.
- For each notebook:
  - Update imports to match the new structure (absolute `from hypercat...`).
  - Execute notebooks in CI using `nbclient` or `papermill` to ensure they run headless.
  - Fail CI if any cell errors.
  - Save executed outputs (HTML or executed `.ipynb`) as build artifacts for review.
- Provide a **Quickstart** notebook (`examples/00_quickstart.ipynb`) that:
  - Imports core constructs
  - Builds a tiny category and a simple commutative diagram
  - Runs without external data
  - Mirrors the README Quickstart

### 7.4 Documentation Consistency
- Choose a docs toolchain (Sphinx + autodoc or MkDocs + mkdocstrings).
- Autogenerate API docs from **canonical** modules only.
- Ensure the following are consistent and up-to-date:
  - Project name, short description, Python version support
  - Install instructions (`pip install hypercat` or `pip install -e .` for dev)
  - Quickstart code mirrored from the Quickstart notebook
  - Links to examples and badges (PyPI, CI, license)
- Remove or archive outdated docs:
  - `docs/HyperCat Manual-v1.0.pdf`
  - `docs/documentation.txt`
  - Any design notes not aligned with the codebase (move to `docs/design/` with a clear “historical” tag)

### 7.5 Readme Sanity Checks
- README must include:
  - Short elevator pitch and scope
  - Supported Python versions and OSes
  - Install instructions and a minimal Quickstart
  - Pointers to examples and docs site
  - Contributing and license links
- Verify all links work (no dead links or images).

### 7.6 Test Matrix (support statement)
- OS: Linux, macOS, Windows (latest stable).
- Python: 3.9, 3.10, 3.11, 3.12.
- Optional extra job: `pypy-3.10` (allow-fail).

### 7.7 Definition of Done (Verification)
- `pip install -e .` succeeds on all matrix entries.
- Import smoke test passes on all matrix entries.
- All example notebooks execute successfully in CI.
- README quickstart runs as-is in a clean environment.
- Docs build without warnings and reflect the canonical module layout.


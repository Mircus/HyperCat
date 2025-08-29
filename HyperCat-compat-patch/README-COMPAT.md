
# HyperCat Compatibility Patch (Finite n-cats, Higher Diagram Validation, Hyper-Transformers)

This patch **fits the current HyperCat repo** at `src/hypercat/` without touching your core API.
- It **adds** finite, ultrafinitist modules under `higher/finite/`.
- It keeps `higher/twocategory.py` and `diagram/enhanced_diagram_checker.py` intact.
- It provides a safer `InfinityCategory` adapter that is n-truncated internally (ultrafinitist).

## Apply
Unzip at the root of your HyperCat repo (the one containing `src/hypercat/...`).

## New modules
- `src/hypercat/higher/finite/globular.py` — `FiniteGlobularSet`
- `src/hypercat/higher/finite/computad.py` — `Generator`, `Relation`
- `src/hypercat/higher/finite/ncat.py` — `FiniteWeakNCategory` with bounded subpath certificates
- `src/hypercat/higher/finite/nsset.py` — finite **n-truncated simplicial set**
- `src/hypercat/higher/finite/duskin.py` — tiny **Duskin nerve** (`nerve2`) for bicategories
- `src/hypercat/diagram/commutativity_checker.py` — subpath rewrite checker with proof certificates (optional add-on; does not override existing)
- `src/hypercat/ml/` — `transcat.py`, `archcat.py`, `deform.py` (Hyper-Transformer basics)

## Updated (backward compatible)
- `src/hypercat/higher/infinitycategory.py` — now a **finite wrapper**; preserves class name but truncates to n.

## Demo
- `src/demos/hyper/01_nat_cert_and_deform.py` — ε-certificate + deformation path demo (uses only new modules).

## Tests (optional)
- `src/tests/test_compat_finite_ncat.py`
- `src/tests/test_compat_diagram_checker.py`
- `src/tests/test_compat_ml.py`

Nothing in core is removed. Your existing imports continue to work.

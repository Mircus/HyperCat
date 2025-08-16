# Laws and Proofs

## Law Engine
- `Violation`, `LawResult`, `Law`, `LawSuite`, `run_suite`
- Use suites to verify laws without core bloat.

```python
from hypercat.core.laws import LawSuite, run_suite
from hypercat.core.laws_category import CATEGORY_SUITE

report = run_suite(C, CATEGORY_SUITE, config={"assoc_sample_limit": 0})
print(report.to_text())
```

## Category Laws
- Identities act as units
- Associativity over composition table

## Certificates
- Machine-checkable summaries of axioms/universal properties

```python
from hypercat.core.proofs import (
  AxReport, check_category_axioms, is_terminal_object, is_product, is_iso, check_simplex_thin, certificate
)

rep_cat = check_category_axioms(C)
print(certificate("Core/C", rep_cat))
```

## Universal properties
- `is_terminal_object(C, T_name)`
- `is_product(C, X_name, Y_name, P_name, pi1_name, pi2_name)`
- `is_iso(C, f_name, g_name)`

## Functor and Naturality
```python
from hypercat.core.functor import FunctorBuilder
from hypercat.core.proofs import check_functor_axioms, check_naturality

F = FunctorBuilder("F", C, C).on_objects({"A":"A","B":"B"}).on_morphisms({"f":"f"}).build()
print(check_functor_axioms(F))
# build a Natural and run check_naturality when needed
```

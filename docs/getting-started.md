# Getting Started

Install (core only):

```bash
pip install hypercat
```

Minimal usage:

```python
from hypercat.core.presentation import Obj, ArrowGen, Presentation

A, B = Obj("A"), Obj("B")
f = ArrowGen("f", "A", "B")
p = Presentation((A,B), (f,))
```

Run tests locally:

```bash
pytest -q
```

# 🤝 Contributing to HyperCat

First of all, thank you for your interest in contributing to **HyperCat** — a project at the frontier of **computational category theory**.

We believe mathematics should be **executable**, **collaborative**, and **beautiful** — and you can help make that happen.

---

## 📐 What Is HyperCat?

HyperCat is a library for:
- Building and analyzing **commutative diagrams**
- Computing **(co)limits**, **natural transformations**, and **adjunctions**
- Exploring the **semantics** of categories through code
- Bridging symbolic logic and diagrammatic reasoning

If that excites you, you're in the right place.

---

## 🧱 How to Contribute

### 🔧 1. Code Contributions

We welcome:
- New modules: `limits`, `functors`, `transformations`, `visualization`, etc.
- Extensions to the diagram-checker (e.g., path simplification, morphism rewriting)
- Bug fixes and code refactoring
- Jupyter notebooks with examples or theory demos

Before submitting:
- Follow [PEP8](https://peps.python.org/pep-0008/)
- Write clear docstrings and inline comments
- Include minimal unit tests for new features (we use `pytest`)

### 🧪 Testing Instructions

**Setup Development Environment:**
```bash
# Clone the repository
git clone https://github.com/yourusername/HyperCat.git
cd HyperCat

# Install in editable mode
pip install -e .

# Install development dependencies
pip install pytest jupyter nbclient
```

**Run Tests:**
```bash
# Run all tests
pytest

# Run specific test file
pytest src/tests/testcat.py

# Run with verbose output
pytest -v
```

**Test Notebooks:**
```bash
# Test that all notebooks run without errors
jupyter nbconvert --execute --to notebook examples/*.ipynb

# Test specific notebook
jupyter nbconvert --execute --to notebook examples/00_quickstart.ipynb
```

**Import Smoke Test:**
```bash
# Verify package imports correctly
python -c "
import hypercat
from hypercat.core import Category, Object, Morphism
print('hypercat ok:', getattr(hypercat, '__version__', 'unknown'))
"
```

**Code Quality Checks:**
```bash
# Check import structure (no circular imports)
python -c "import hypercat; print('All imports successful')"

# Check that core classes are properly exposed
python -c "
from hypercat import Category, Object, Morphism, Functor, NaturalTransformation
from hypercat.categories import StandardCategories
from hypercat.higher import TwoCategory
print('All key classes accessible')
"

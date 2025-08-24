<p align="center">
  <img src="./HyperCat_logo.png" alt="HyperCat Logo" width="450"/>
</p>

# 🐾 HyperCat

> *A sleek and expressive Python library for modeling categories, functors, natural transformations, and higher categorical structures.*

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ Features

- 📦 **Core Structures**: Objects, morphisms, categories with full composition laws
- 🔄 **Functors**: Map between categories while preserving structure
- 🌀 **Natural Transformations**: Morphisms between functors with naturality checking
- 2️⃣ **Higher Categories**: 2-categories, ∞-categories, simplicial sets
- 🧮 **Advanced Constructions**: Monoidal, braided, enriched categories, and toposes
- 🔧 **Algebraic Structures**: Operads and algebras
- 📊 **Diagram Tools**: Automated commutativity checking
- 🏗️ **Standard Categories**: Pre-built categories (terminal, initial, discrete, etc.)

---

## 🧠 Philosophy

**HyperCat** brings the mathematical elegance of category theory to Python, designed for:

- 📐 Research in pure and applied category theory  
- 🧮 Computational modeling of categorical structures  
- 🧠 Algebraic topology and homotopy theory
- 🤖 Categorical foundations for functional programming and type theory
- 🔬 Mathematical foundations for machine learning and AI systems

---

## 🛠️ Installation

### From Source (Recommended)

```bash
git clone https://github.com/Mircus/HyperCat.git

cd HyperCat
pip install -e .
```

### Requirements

- Python 3.8 or higher
- Dependencies: `networkx`, `matplotlib`, `jupyter`, `pytest`

---

## 📚 Quick Start

### Basic Usage

```python
import hypercat
from hypercat import Category, Object, Morphism, Functor

# Create a category
cat = Category("Sets")

# Add objects
A = Object("A")
B = Object("B")
cat.add_object(A)
cat.add_object(B)

# Add morphisms
f = Morphism("f", A, B)
cat.add_morphism(f)

# Compose morphisms
g = Morphism("g", B, A)
cat.add_morphism(g)
h = cat.compose(f, g)  # h: A → A

print(f"Composed morphism: {h}")
```

### Functors

```python
# Create another category
cat2 = Category("Groups")
cat2.add_object(A)
cat2.add_object(B)
cat2.add_morphism(f)

# Create a functor
F = Functor("F", cat, cat2)
F.map_object(A, A)
F.map_object(B, B)
F.map_morphism(f, f)

# Check functor laws
print(f"Preserves composition: {F.is_functor()}")
```

### Natural Transformations

```python
from hypercat import NaturalTransformation

# Create two functors F, G: cat → cat2
G = Functor("G", cat, cat2)
# ... set up G's mappings ...

# Create natural transformation η: F ⇒ G
eta = NaturalTransformation("η", F, G)
# ... set up components ...

# Verify naturality
print(f"Is natural: {eta.is_natural()}")
```

### Standard Categories

```python
from hypercat import StandardCategories

# Pre-built categories
terminal = StandardCategories.terminal_category()  # Single object, single morphism
initial = StandardCategories.initial_category()    # Empty category
discrete = StandardCategories.discrete_category(["X", "Y", "Z"])  # Only identity morphisms
```

---

## 📖 Documentation

### Interactive Examples

Start with our interactive Jupyter notebooks in the `examples/` directory:

- **[00_quickstart.ipynb](examples/00_quickstart.ipynb)**: Complete introduction to HyperCat
- **[HyperCatDemo.ipynb](examples/HyperCatDemo.ipynb)**: Advanced features demonstration
- **[hypercat_algebraic_topology_demo.ipynb](examples/hypercat_algebraic_topology_demo.ipynb)**: Algebraic topology applications
- **[hypercats.ipynb](examples/hypercats.ipynb)**: Working with higher categories

### Module Structure

```
hypercat/
├── core/           # Core classes: Category, Object, Morphism, Functor
├── categories/     # Specialized categories: Monoidal, Braided, Enriched, Topos
├── higher/         # Higher categories: 2-categories, ∞-categories
├── diagram/        # Diagram and commutativity checking tools
└── algebraic/      # Operads and algebraic structures
```

### Key Classes

- **`Category`**: The fundamental structure with objects and morphisms
- **`Functor`**: Structure-preserving mappings between categories
- **`NaturalTransformation`**: Morphisms between functors
- **`TwoCategory`**: Categories with 2-cells (morphisms between morphisms)
- **`MonoidalCategory`**: Categories with tensor products
- **`Topos`**: Categories with all finite limits and power objects

---

## 🧪 Testing

Run the test suite:

```bash
pytest
```

---

## 🔭 Roadmap

See [ROADMAP.md](./ROADMAP.md) for planned features:

- Universal properties and (co)limits
- Kan extensions
- Model categories
- Higher topos theory
- Categorical logic
- Integration with proof assistants

---

## 🔭 What's Next?

Check out our [ROADMAP.md](./ROADMAP.md) for upcoming features, including:

- (Co)limits and universal constructions
- Functorial logic and transformation categories


---

## 🤝 Contribute

We welcome contributions! See [CONTRIBUTING.md](./CONTRIBUTING.md) for how to get started.

---

## 🧵 Motto

<p align="center">
  <em>"The fabric of higher structures"</em>
</p>

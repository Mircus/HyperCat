<p align="center">
  <img src="./HyperCat_logo.png" alt="HyperCat Logo" width="340"/>
</p>

# 🐾 HyperCat

> *A sleek and expressive Python library for modeling categories, functors, natural transformations, and 2-categories (hypercategories).*

---

## ✨ Features

- ✅ Object and morphism modeling  
- 🔁 Functors with composition and identity preservation  
- 🌀 Natural transformations with full naturality condition checks  
- 2️⃣ Support for 2-categories with vertical and horizontal 2-cell composition  
- 📦 Built-in standard categories: `Δⁿ`, terminal, discrete, walking isomorphism

---

## 🧠 Philosophy

**HyperCat** is built on the structural elegance of category theory and the agility of abstraction. It’s designed for:

- 📐 Research in category theory  
- 🧮 Computational modeling of categorical structures  
- 🧠 Experimental algebraic topology and homotopy  
- 🤖 Categorical foundations for machine learning and AI systems

---

## 🛠️ Installation

```bash
git clone https://github.com/Mircus/HyperCat.git
cd HyperCat
pip install -e .
```

---

## 📚 Getting Started

Try out the examples in the `examples/` folder, or run:

```python
from hypercat import Category

C = Category("MyCat")
A = C.add_object("A")
B = C.add_object("B")
f = C.add_morphism("f", A, B)
```

More tutorials and notebooks coming soon.

---

## 🔭 What's Next?

Check out our [ROADMAP.md](./ROADMAP.md) for upcoming features, including:

- Commutative diagram validation
- (Co)limits and universal constructions
- Functorial logic and transformation categories
- Visual diagram rendering and export to LaTeX

---

## 🤝 Contribute

We welcome contributions! See [CONTRIBUTING.md](./CONTRIBUTING.md) for how to get started.

---

## 🧵 Motto

<p align="center">
  <em>"The fabric of higher structures"</em>
</p>

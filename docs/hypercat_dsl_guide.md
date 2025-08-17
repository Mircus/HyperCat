# HyperCat Functional DSL Reference Guide

A complete reference for the HyperCat functional Domain-Specific Language (DSL) for category construction and manipulation.

## 🎯 Overview

The HyperCat DSL provides a clean, functional approach to building categories, objects, morphisms, and functors. It emphasizes immutability, composability, and mathematical correctness while maintaining readability.

## 🏗️ Core DSL Components

### Basic Types

```python
from hypercat_dsl import Cat, Obj, Mor, Fun, pipe, cat

# Immutable category representation
@dataclass(frozen=True)
class Cat:
    name: str
    objects: frozenset
    morphisms: frozenset
    composition: frozendict
    identities: frozendict

# Immutable object with optional data
@dataclass(frozen=True)
class Obj:
    name: str
    data: Any = None

# Immutable morphism between objects
@dataclass(frozen=True)
class Mor:
    name: str
    source: Obj
    target: Obj
    data: Any = None
```

### The Pipe Operator

The fundamental composition operator for functional style:

```python
# Basic pipe usage
result = pipe(
    initial_value,
    function1,
    function2,
    function3
)

# Equivalent to: function3(function2(function1(initial_value)))

# Example with category building
simple_cat = pipe(
    cat("MyCategory"),           # Start with category builder
    objects("A", "B", "C"),      # Add objects
    morphisms(("f", "A", "B")),  # Add morphisms
    free_composition()           # Add all compositions
).build()                        # Build immutable category
```

## 📦 Object Creation

### Simple Objects

```python
from hypercat_dsl import objects

# String names (simplest)
simple_category = pipe(
    cat("Simple"),
    objects("A", "B", "C", "D")
).build()

# Objects with data
data_category = pipe(
    cat("WithData"),
    objects(
        ("Point", {"x": 1, "y": 2}),
        ("Vector", [1, 0, -1]),
        ("Matrix", [[1, 0], [0, 1]])
    )
).build()

# Direct object instances
obj_A = Obj("A", {"type": "vertex"})
obj_B = Obj("B", {"type": "edge"})

direct_category = pipe(
    cat("Direct"),
    objects(obj_A, obj_B)
).build()
```

### Finite Sets as Objects

```python
from hypercat_dsl import finite_sets

# FinSet category with sets up to size 3
finset_cat = pipe(
    cat("FinSet"),
    finite_sets(3)  # Creates ∅, {1}, {1,2}, {1,2,3}
).build()

print("FinSet objects:")
for obj in finset_cat.objects:
    print(f"  {obj.name}: {obj.data}")
# Output:
#   ∅: set()
#   {1}: {1}
#   {1,2}: {1, 2}
#   {1,2,3}: {1, 2, 3}
```

### Poset Objects

```python
from hypercat_dsl import poset

# Diamond lattice
diamond = pipe(
    cat("Diamond"),
    poset(
        elements=["⊥", "a", "b", "⊤"],
        order=[
            ("⊥", "⊥"), ("a", "a"), ("b", "b"), ("⊤", "⊤"),  # Reflexive
            ("⊥", "a"), ("⊥", "b"),                           # Bottom relations
            ("a", "⊤"), ("b", "⊤"),                           # Top relations
            ("⊥", "⊤")                                        # Transitive closure
        ]
    )
).build()

# Chain poset 0 ≤ 1 ≤ 2 ≤ 3
chain = pipe(
    cat("Chain4"),
    poset(
        elements=[0, 1, 2, 3],
        order=[(i, j) for i in range(4) for j in range(i, 4)]
    )
).build()
```

## ➡️ Morphism Creation

### Basic Morphisms

```python
from hypercat_dsl import morphisms

# Simple morphism specifications
basic_morphisms = pipe(
    cat("WithMorphisms"),
    objects("A", "B", "C"),
    morphisms(
        ("f", "A", "B"),                    # f: A → B
        ("g", "B", "C"),                    # g: B → C
        ("h", "A", "C"),                    # h: A → C
        ("id_A", "A", "A")                  # Identity morphism
    )
).build()

# Morphisms with data
data_morphisms = pipe(
    cat("DataMorphisms"),
    objects("X", "Y"),
    morphisms(
        ("linear", "X", "Y", {"type": "linear_map", "matrix": [[2, 0], [0, 3]]}),
        ("proj", "Y", "X", {"type": "projection", "components": [0]})
    )
).build()
```

### Functions Between Finite Sets

```python
from hypercat_dsl import with_functions

# Define actual functions
def double(x):
    return 2 * x

def mod3(x):
    return x % 3

# Create category with function morphisms
func_cat = pipe(
    cat("Functions"),
    finite_sets(3),
    with_functions({
        "double": double,
        "mod3": mod3,
        "successor": lambda x: x + 1
    })
).build()
```

### All Morphisms Between Objects

```python
from hypercat_dsl import with_all_morphisms_between

# Create complete bipartite morphism structure
complete_cat = pipe(
    cat("Complete"),
    objects("A1", "A2", "B1", "B2"),
    with_all_morphisms_between(
        source_names=["A1", "A2"],
        target_names=["B1", "B2"]
    )
).build()

# Creates: A1→B1, A1→B2, A2→B1, A2→B2
```

## 🔗 Composition

### Free Composition

```python
from hypercat_dsl import free_composition

# Automatically generate all possible compositions
free_cat = pipe(
    cat("FreeCategory"),
    objects("A", "B", "C", "D"),
    morphisms(
        ("f", "A", "B"),
        ("g", "B", "C"),
        ("h", "C", "D")
    ),
    free_composition()  # Creates g∘f, h∘g, h∘g∘f, etc.
).build()

print(f"Morphisms: {len(free_cat.morphisms)}")  # Includes all compositions
```

### Custom Composition Rules

```python
from hypercat_dsl import with_compositions

# Manually specify compositions
custom_comp = pipe(
    cat("CustomComposition"),
    objects("A", "B", "C"),
    morphisms(
        ("f", "A", "B"),
        ("g", "B", "C"),
        ("gf", "A", "C")  # Pre-define composite
    ),
    with_compositions(
        ("f", "g", "gf")  # g ∘ f = gf
    )
).build()
```

## 🏛️ Category Builders

### CategoryBuilder Methods

```python
from hypercat_dsl import CategoryBuilder

# Direct builder usage (without pipe)
builder = CategoryBuilder("Manual")
builder.with_objects("X", "Y", "Z")
builder.with_morphisms(("f", "X", "Y"), ("g", "Y", "Z"))
builder.with_free_composition()
manual_cat = builder.build()

# Functional builder usage (with pipe)
functional_cat = pipe(
    cat("Functional"),
    objects("X", "Y", "Z"),
    morphisms(("f", "X", "Y"), ("g", "Y", "Z")),
    free_composition()
).build()
```

### Chaining Builder Operations

```python
# Complex category with multiple operations
complex_cat = pipe(
    cat("Complex"),
    # Add basic structure
    objects("A", "B", "C", "D"),
    morphisms(
        ("f", "A", "B"),
        ("g", "B", "C"),
        ("h", "C", "D")
    ),
    # Add all morphisms between specific objects
    with_all_morphisms_between(["A"], ["D"]),
    # Add custom compositions
    with_compositions(
        ("f", "g", "gf"),
        ("g", "h", "hg")
    ),
    # Generate free compositions for the rest
    free_composition()
).build()
```

## 🎨 Standard Categories

### Built-in Standard Categories

```python
from hypercat_dsl import DSLStandardCategories

# Finite sets
finset = DSLStandardCategories.finite_sets(max_size=4)
print(f"FinSet: {[obj.name for obj in finset.objects]}")

# Chain posets
chain5 = DSLStandardCategories.chain_poset(length=5)
print(f"Chain: {[obj.name for obj in chain5.objects]}")

# Diamond lattice
diamond = DSLStandardCategories.diamond_poset()
print(f"Diamond: {[obj.name for obj in diamond.objects]}")

# Discrete categories
discrete = DSLStandardCategories.discrete_category(["Red", "Blue", "Green"])
print(f"Discrete: {[obj.name for obj in discrete.objects]}")

# Terminal category
terminal = DSLStandardCategories.terminal_category()
print(f"Terminal: {[obj.name for obj in terminal.objects]}")  # Just "*"
```

## ➡️ Functors

### Basic Functor Construction

```python
from hypercat_dsl import functor

# Source and target categories
source_cat = pipe(
    cat("Source"),
    objects("A", "B"),
    morphisms(("f", "A", "B"))
).build()

target_cat = pipe(
    cat("Target"),
    objects("X", "Y", "Z"),
    morphisms(("g", "X", "Y"), ("h", "Y", "Z"))
).build()

# Build functor
F = pipe(
    functor("F", source_cat, target_cat),
    lambda f: f.on_objects({"A": "X", "B": "Y"}),  # Map objects
    lambda f: f.on_morphisms({"f": "g"})           # Map morphisms
).build()

print(f"Functor {F.name}: {F.source.name} → {F.target.name}")
```

### Functor Composition

```python
# Compose functors F: A → B and G: B → C to get G∘F: A → C
def compose_functors(F, G):
    # Object composition: (G∘F)(A) = G(F(A))
    composed_objects = {
        obj: G.object_map[F.object_map[obj]]
        for obj in F.object_map
    }
    
    # Morphism composition: (G∘F)(f) = G(F(f))
    composed_morphisms = {
        mor: G.morphism_map[F.morphism_map[mor]]
        for mor in F.morphism_map
    }
    
    return Fun(
        name=f"{G.name}∘{F.name}",
        source=F.source,
        target=G.target,
        object_map=frozendict(composed_objects),
        morphism_map=frozendict(composed_morphisms)
    )
```

## 🔄 Category Operations

### Product Categories

```python
from hypercat_dsl import product_category

cat1 = pipe(cat("A"), objects("a1", "a2")).build()
cat2 = pipe(cat("B"), objects("b1", "b2")).build()

# Cartesian product A × B
prod = product_category(cat1, cat2)
print(f"Product objects: {[obj.name for obj in prod.objects]}")
# Output: ['(a1,b1)', '(a1,b2)', '(a2,b1)', '(a2,b2)']
```

### Opposite Categories

```python
from hypercat_dsl import opposite_category

# Original category A → B → C
original = pipe(
    cat("Original"),
    objects("A", "B", "C"),
    morphisms(("f", "A", "B"), ("g", "B", "C"))
).build()

# Opposite category C ← B ← A (arrows reversed)
opposite = opposite_category(original)
print(f"Opposite: {opposite.name}")
for mor in opposite.morphisms:
    print(f"  {mor.name}: {mor.source.name} → {mor.target.name}")
```

### Slice Categories

```python
from hypercat_dsl import slice_category

base_cat = pipe(
    cat("Base"),
    objects("A", "B", "C"),
    morphisms(("f", "A", "C"), ("g", "B", "C"))
).build()

C_obj = next(obj for obj in base_cat.objects if obj.name == "C")

# Slice category Base/C (objects are morphisms to C)
slice_cat = slice_category(base_cat, C_obj)
print(f"Slice objects: {[obj.name for obj in slice_cat.objects]}")
# Objects represent morphisms A→C and B→C
```

## 🎯 Advanced DSL Patterns

### Conditional Category Building

```python
def build_category_conditionally(include_extra_objects=False, add_morphisms=True):
    builder = pipe(
        cat("Conditional"),
        objects("A", "B")
    )
    
    if include_extra_objects:
        builder = pipe(builder, objects("C", "D"))
    
    if add_morphisms:
        builder = pipe(
            builder,
            morphisms(("f", "A", "B")),
            free_composition() if include_extra_objects else lambda x: x
        )
    
    return builder.build()

# Different configurations
minimal = build_category_conditionally(False, False)
with_morphisms = build_category_conditionally(False, True)
full_category = build_category_conditionally(True, True)
```

### Category Families

```python
def create_chain_family(max_length=5):
    """Create family of chain categories of different lengths"""
    chains = {}
    for n in range(1, max_length + 1):
        chains[f"Chain{n}"] = pipe(
            cat(f"Chain{n}"),
            poset(
                elements=list(range(n)),
                order=[(i, j) for i in range(n) for j in range(i, n)]
            )
        ).build()
    return chains

chain_family = create_chain_family(4)
for name, chain in chain_family.items():
    print(f"{name}: {len(chain.objects)} objects")
```

### Parameterized Category Construction

```python
def symmetric_group_category(n):
    """Build category representing symmetric group S_n"""
    from itertools import permutations
    
    # Objects are permutations
    perms = list(permutations(range(n)))
    perm_objects = [f"σ{i}" for i in range(len(perms))]
    
    return pipe(
        cat(f"S_{n}"),
        objects(*perm_objects),
        # Add morphisms for group multiplication
        with_all_morphisms_between(perm_objects, perm_objects),
        # Note: would need custom composition for group law
    ).build()

S3 = symmetric_group_category(3)
print(f"S_3: {len(S3.objects)} objects, {len(S3.morphisms)} morphisms")
```

## 🔍 Debugging and Introspection

### Category Analysis

```python
def analyze_category(cat):
    """Comprehensive category analysis"""
    analysis = {
        "name": cat.name,
        "objects": len(cat.objects),
        "morphisms": len(cat.morphisms),
        "object_names": [obj.name for obj in cat.objects],
        "morphism_summary": []
    }
    
    for mor in cat.morphisms:
        analysis["morphism_summary"].append({
            "name": mor.name,
            "source": mor.source.name,
            "target": mor.target.name,
            "has_data": mor.data is not None
        })
    
    return analysis

# Analyze a category
cat_info = analyze_category(diamond)
print(f"Category analysis: {cat_info}")
```

### Validation

```python
def validate_category(cat):
    """Validate category laws"""
    errors = []
    
    # Check identity morphisms exist
    for obj in cat.objects:
        if obj not in cat.identities:
            errors.append(f"Missing identity for {obj.name}")
    
    # Check composition associativity (simplified)
    # Note: Full check would require testing all composable triples
    
    # Check composition domains/codomains
    for (f, g), h in cat.composition.items():
        if f.target != g.source:
            errors.append(f"Composition {g.name}∘{f.name}: domain mismatch")
        if h.source != f.source or h.target != g.target:
            errors.append(f"Composition {g.name}∘{f.name}: codomain mismatch")
    
    return errors

# Validate a category
validation_errors = validate_category(simple_cat)
if validation_errors:
    print("Validation errors:", validation_errors)
else:
    print("Category is valid!")
```

## 📖 Quick Reference

### Core Functions

| Function | Purpose | Example |
|----------|---------|---------|
| `cat(name)` | Start category builder | `cat("MyCategory")` |
| `objects(*specs)` | Add objects | `objects("A", "B", ("C", data))` |
| `morphisms(*specs)` | Add morphisms | `morphisms(("f", "A", "B"))` |
| `finite_sets(n)` | Add finite sets ≤ n | `finite_sets(3)` |
| `poset(elements, order)` | Add poset structure | `poset([0,1,2], [(0,1),(1,2)])` |
| `free_composition()` | Generate compositions | `free_composition()` |
| `pipe(initial, *funcs)` | Function composition | `pipe(cat("A"), objects("X"))` |
| `.build()` | Build immutable category | `builder.build()` |

### Standard Categories

| Function | Creates | Example |
|----------|---------|---------|
| `DSLStandardCategories.finite_sets(n)` | FinSet≤n | `finite_sets(3)` |
| `DSLStandardCategories.chain_poset(n)` | Chain of length n | `chain_poset(5)` |
| `DSLStandardCategories.diamond_poset()` | Diamond lattice | `diamond_poset()` |
| `DSLStandardCategories.discrete_category(objs)` | Discrete category | `discrete_category(["A","B"])` |
| `DSLStandardCategories.terminal_category()` | Terminal category | `terminal_category()` |

### Category Operations

| Function | Purpose | Example |
|----------|---------|---------|
| `product_category(C, D)` | Product C × D | `product_category(cat1, cat2)` |
| `opposite_category(C)` | Opposite C^op | `opposite_category(cat)` |
| `slice_category(C, obj)` | Slice C/obj | `slice_category(cat, base_obj)` |

### Functor Operations

| Function | Purpose | Example |
|----------|---------|---------|
| `functor(name, source, target)` | Start functor builder | `functor("F", cat1, cat2)` |
| `.on_objects(mapping)` | Map objects | `.on_objects({"A": "X"})` |
| `.on_morphisms(mapping)` | Map morphisms | `.on_morphisms({"f": "g"})` |

This reference provides everything needed to build sophisticated categorical structures using the HyperCat functional DSL!
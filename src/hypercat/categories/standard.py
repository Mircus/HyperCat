"""
Standard category implementations with concrete examples.
Provides working categories for finite sets, posets, types, and groups.
"""

from typing import List, Dict, Set, Tuple, Any, Optional, Callable, Union
from hypercat.core.core import Category, Object, Morphism, Functor
# from basic_constructor import BasicConstructor, add_basic_constructor_to_category
import itertools
from functools import partial

class FiniteSetCategory(Category):
    """Category of finite sets with REAL set operations"""
    
    def __init__(self, max_size: int = 5):
        super().__init__(f"FinSet({max_size})")
        self.max_size = max_size
        self.sets_by_size: Dict[int, List[Object]] = {}
        self._build_finite_sets()
        self._build_functions()
        
        # Add constructor methods
        # add_basic_constructor_to_category()
    
    def _build_finite_sets(self):
        """Build actual finite sets as objects"""
        for size in range(self.max_size + 1):
            self.sets_by_size[size] = []
            
            if size == 0:
                # Empty set
                empty = Object("∅", set())
                self.add_object(empty)
                self.sets_by_size[0].append(empty)
            else:
                # Standard set {1, 2, ..., size}
                elements = set(range(1, size + 1))
                std_set = Object(f"Set{size}", elements)
                self.add_object(std_set)
                self.sets_by_size[size].append(std_set)
                
                # Add some variants for interesting examples
                if size == 2:
                    # {a, b} for variety
                    alt_set = Object("{a,b}", {"a", "b"})
                    self.add_object(alt_set)
                    self.sets_by_size[2].append(alt_set)
                elif size == 3:
                    # {x, y, z}
                    alt_set = Object("{x,y,z}", {"x", "y", "z"})
                    self.add_object(alt_set)
                    self.sets_by_size[3].append(alt_set)
    
    def _build_functions(self):
        """Build actual functions between finite sets"""
        
        # Build some standard functions
        for source_size in range(self.max_size + 1):
            for target_size in range(self.max_size + 1):
                
                # Get representative sets
                if not self.sets_by_size[source_size] or not self.sets_by_size[target_size]:
                    continue
                
                source = self.sets_by_size[source_size][0]
                target = self.sets_by_size[target_size][0]
                
                # Build interesting functions
                functions = self._generate_functions(source, target)
                
                for func_name, func_data in functions:
                    morphism = Morphism(func_name, source, target, {
                        'type': 'function',
                        'function': func_data,
                        'source_set': source.data,
                        'target_set': target.data
                    })
                    self.add_morphism(morphism)
    
    def _generate_functions(self, source: Object, target: Object) -> List[Tuple[str, Callable]]:
        """Generate interesting functions between two finite sets"""
        functions = []
        
        source_set = source.data if source.data else set()
        target_set = target.data if target.data else set()
        
        if not source_set:
            # From empty set - unique function
            functions.append((f"!_{source.name}→{target.name}", lambda x: None))
            return functions
        
        if not target_set:
            # To empty set - only from empty set
            return functions
        
        # Constant functions
        for target_elem in list(target_set)[:2]:  # Limit to first 2 for simplicity
            const_name = f"const_{target_elem}"
            functions.append((const_name, lambda x, val=target_elem: val))
        
        # Inclusion if source ⊆ target
        if source_set.issubset(target_set):
            functions.append((f"inc_{source.name}→{target.name}", lambda x: x))
        
        # Projection if target ⊆ source
        if target_set.issubset(source_set) and len(target_set) > 0:
            target_elem = next(iter(target_set))
            functions.append((f"proj_{source.name}→{target.name}", 
                            lambda x, default=target_elem: x if x in target_set else default))
        
        # Characteristic function to {0, 1} if target has 0,1
        if target_set >= {0, 1} or target_set >= {1, 2}:
            zero_elem = 0 if 0 in target_set else min(target_set)
            one_elem = 1 if 1 in target_set else max(target_set)
            
            # Pick a subset to be characteristic of
            if len(source_set) > 1:
                subset = {next(iter(source_set))}
                functions.append((f"χ_{subset}", 
                               lambda x, s=subset, zero=zero_elem, one=one_elem: 
                               one if x in s else zero))
        
        return functions
    
    def get_set(self, size: int, index: int = 0) -> Optional[Object]:
        """Get a finite set of given size"""
        if size in self.sets_by_size and index < len(self.sets_by_size[size]):
            return self.sets_by_size[size][index]
        return None
    
    def get_empty_set(self) -> Object:
        """Get the empty set"""
        return self.get_set(0, 0)
    
    def get_singleton(self) -> Object:
        """Get a singleton set"""
        return self.get_set(1, 0)
    
    def has_products(self) -> bool:
        """Check if category has all finite products"""
        # Test a few cases
        A = self.get_set(1)
        B = self.get_set(2)
        if A and B:
            product = self.compute_product([A, B])
            return product is not None
        return False
    
    def has_coproducts(self) -> bool:
        """Check if category has all finite coproducts"""
        A = self.get_set(1)
        B = self.get_set(2)
        if A and B:
            coproduct = self.compute_coproduct([A, B])
            return coproduct is not None
        return False
    
    def is_cartesian_closed(self) -> bool:
        """Check if category is cartesian closed (has exponentials)"""
        # FinSet is not cartesian closed, but we can check
        return False  # Known result
    
    def display_summary(self) -> str:
        """Display what's in this category"""
        summary = [f"=== {self.name} ==="]
        summary.append(f"Objects: {len(self.objects)}")
        summary.append(f"Morphisms: {len(self.morphisms)}")
        summary.append("")
        
        summary.append("Sets by size:")
        for size, sets in self.sets_by_size.items():
            set_names = [s.name for s in sets]
            summary.append(f"  Size {size}: {set_names}")
        
        summary.append("")
        summary.append("Properties:")
        summary.append(f"  Has products: {self.has_products()}")
        summary.append(f"  Has coproducts: {self.has_coproducts()}")
        summary.append(f"  Has initial: {self.find_initial() is not None}")
        summary.append(f"  Has terminal: {self.find_terminal() is not None}")
        
        return "\n".join(summary)


class PosetCategory(Category):
    """Category from a partially ordered set"""
    
    def __init__(self, name: str, elements: Set[Any], order_relation: Set[Tuple[Any, Any]]):
        super().__init__(f"Poset({name})")
        self.elements = elements
        self.order = order_relation
        self._build_poset_category()
        
        # add_basic_constructor_to_category()
    
    def _build_poset_category(self):
        """Build category from poset"""
        # Objects are elements
        element_objects = {}
        for elem in self.elements:
            obj = Object(str(elem), elem)
            self.add_object(obj)
            element_objects[elem] = obj
        
        # Morphisms are order relations
        for (a, b) in self.order:
            if a in element_objects and b in element_objects:
                morph_name = f"{a}≤{b}" if a != b else f"id_{a}"
                morphism = Morphism(morph_name, element_objects[a], element_objects[b], {
                    'type': 'order',
                    'relation': (a, b)
                })
                self.add_morphism(morphism)
        
        # Add reflexive and transitive morphisms
        self._complete_order_morphisms(element_objects)
    
    def _complete_order_morphisms(self, element_objects: Dict[Any, Object]):
        """Add transitive closure of order relation"""
        # This is simplified - full implementation would compute transitive closure
        
        # Add reflexive morphisms (identities are already added by Category)
        # Add some transitive morphisms for demonstration
        order_dict = {}
        for (a, b) in self.order:
            if a not in order_dict:
                order_dict[a] = set()
            order_dict[a].add(b)
        
        # Simple transitive closure (not optimal, but works for small posets)
        changed = True
        while changed:
            changed = False
            for a in order_dict:
                for b in order_dict[a].copy():
                    if b in order_dict:
                        for c in order_dict[b]:
                            if c not in order_dict[a]:
                                order_dict[a].add(c)
                                
                                # Add morphism a → c
                                if a != c:
                                    morph_name = f"{a}≤{c}"
                                    # Check if morphism already exists
                                    existing = any(m.name == morph_name for m in self.morphisms)
                                    if not existing:
                                        morphism = Morphism(morph_name, 
                                                          element_objects[a], 
                                                          element_objects[c], {
                                            'type': 'order',
                                            'relation': (a, c)
                                        })
                                        self.add_morphism(morphism)
                                        changed = True
    
    def is_connected(self) -> bool:
        """Check if underlying poset is connected"""
        # Simplified connectivity check
        return len(self.objects) <= 1 or len(self.morphisms) > len(self.objects)
    
    def find_minimal_elements(self) -> List[Object]:
        """Find minimal elements (potential initial objects)"""
        minimal = []
        for obj in self.objects:
            # Check if there are morphisms TO this object from others
            incoming = [m for m in self.morphisms 
                       if m.target == obj and m.source != obj]
            if not incoming:
                minimal.append(obj)
        return minimal
    
    def find_maximal_elements(self) -> List[Object]:
        """Find maximal elements (potential terminal objects)"""
        maximal = []
        for obj in self.objects:
            # Check if there are morphisms FROM this object to others
            outgoing = [m for m in self.morphisms 
                       if m.source == obj and m.target != obj]
            if not outgoing:
                maximal.append(obj)
        return maximal
    
    @staticmethod
    def create_chain(length: int) -> 'PosetCategory':
        """Create a chain poset 0 ≤ 1 ≤ 2 ≤ ... ≤ length-1"""
        elements = set(range(length))
        order = {(i, j) for i in range(length) for j in range(i, length)}
        return PosetCategory(f"Chain{length}", elements, order)
    
    @staticmethod
    def create_discrete(elements: Set[Any]) -> 'PosetCategory':
        """Create discrete poset (only identity relations)"""
        order = {(x, x) for x in elements}
        return PosetCategory("Discrete", elements, order)
    
    @staticmethod
    def create_diamond() -> 'PosetCategory':
        """Create diamond poset: bottom ≤ left, right ≤ top"""
        elements = {"⊥", "left", "right", "⊤"}
        order = {
            ("⊥", "⊥"), ("left", "left"), ("right", "right"), ("⊤", "⊤"),  # reflexive
            ("⊥", "left"), ("⊥", "right"), ("⊥", "⊤"),  # from bottom
            ("left", "⊤"), ("right", "⊤")  # to top
        }
        return PosetCategory("Diamond", elements, order)


class TypeCategory(Category):
    """Category of types with type operations"""
    
    def __init__(self):
        super().__init__("Types")
        self._build_basic_types()
        self._build_type_constructors()
        
        # add_basic_constructor_to_category()
    
    def _build_basic_types(self):
        """Build basic types"""
        # Primitive types
        self.unit_type = Object("Unit", {"type": "unit", "inhabitants": {()}})
        self.bool_type = Object("Bool", {"type": "bool", "inhabitants": {True, False}})
        self.nat_type = Object("ℕ", {"type": "nat", "inhabitants": "infinite"})
        self.int_type = Object("ℤ", {"type": "int", "inhabitants": "infinite"})
        self.string_type = Object("String", {"type": "string", "inhabitants": "infinite"})
        
        # Bottom type (uninhabited)
        self.bottom_type = Object("⊥", {"type": "bottom", "inhabitants": set()})
        
        # Add to category
        for type_obj in [self.unit_type, self.bool_type, self.nat_type, 
                        self.int_type, self.string_type, self.bottom_type]:
            self.add_object(type_obj)
    
    def _build_type_constructors(self):
        """Build some type constructor morphisms"""
        
        # Coercions
        nat_to_int = Morphism("ℕ→ℤ", self.nat_type, self.int_type, {
            'type': 'coercion',
            'function': lambda n: n
        })
        self.add_morphism(nat_to_int)
        
        # Absurdity (from bottom type)
        for target_type in [self.unit_type, self.bool_type, self.nat_type]:
            absurd = Morphism(f"absurd→{target_type.name}", self.bottom_type, target_type, {
                'type': 'absurdity',
                'function': lambda x: None  # Never called since bottom is uninhabited
            })
            self.add_morphism(absurd)
        
        # Terminal morphisms (to unit)
        for source_type in [self.bool_type, self.nat_type, self.int_type, self.string_type]:
            terminal = Morphism(f"{source_type.name}→Unit", source_type, self.unit_type, {
                'type': 'terminal',
                'function': lambda x: ()
            })
            self.add_morphism(terminal)
    
    def create_product_type(self, type1: Object, type2: Object) -> Object:
        """Create product type A × B"""
        product_name = f"{type1.name}×{type2.name}"
        
        # Compute inhabitants if possible
        if (type1.data.get("inhabitants") != "infinite" and 
            type2.data.get("inhabitants") != "infinite"):
            
            inhabitants1 = type1.data["inhabitants"]
            inhabitants2 = type2.data["inhabitants"]
            product_inhabitants = {(a, b) for a in inhabitants1 for b in inhabitants2}
        else:
            product_inhabitants = "infinite"
        
        product_type = Object(product_name, {
            "type": "product",
            "components": [type1, type2],
            "inhabitants": product_inhabitants
        })
        
        self.add_object(product_type)
        
        # Add projection morphisms
        proj1 = Morphism(f"π₁_{product_name}", product_type, type1, {
            'type': 'projection',
            'index': 0,
            'function': lambda pair: pair[0]
        })
        proj2 = Morphism(f"π₂_{product_name}", product_type, type2, {
            'type': 'projection', 
            'index': 1,
            'function': lambda pair: pair[1]
        })
        
        self.add_morphism(proj1)
        self.add_morphism(proj2)
        
        return product_type
    
    def create_sum_type(self, type1: Object, type2: Object) -> Object:
        """Create sum type A + B"""
        sum_name = f"{type1.name}+{type2.name}"
        
        # Compute inhabitants
        if (type1.data.get("inhabitants") != "infinite" and 
            type2.data.get("inhabitants") != "infinite"):
            
            inhabitants1 = type1.data["inhabitants"]
            inhabitants2 = type2.data["inhabitants"]
            sum_inhabitants = {("left", a) for a in inhabitants1} | {("right", b) for b in inhabitants2}
        else:
            sum_inhabitants = "infinite"
        
        sum_type = Object(sum_name, {
            "type": "sum",
            "components": [type1, type2],
            "inhabitants": sum_inhabitants
        })
        
        self.add_object(sum_type)
        
        # Add injection morphisms
        inj1 = Morphism(f"inl_{sum_name}", type1, sum_type, {
            'type': 'injection',
            'side': 'left',
            'function': lambda a: ("left", a)
        })
        inj2 = Morphism(f"inr_{sum_name}", type2, sum_type, {
            'type': 'injection',
            'side': 'right', 
            'function': lambda b: ("right", b)
        })
        
        self.add_morphism(inj1)
        self.add_morphism(inj2)
        
        return sum_type
    
    def create_function_type(self, domain: Object, codomain: Object) -> Object:
        """Create function type A → B"""
        function_name = f"{domain.name}→{codomain.name}"
        
        # For finite types, we can count functions
        domain_inhabitants = domain.data.get("inhabitants", "infinite")
        codomain_inhabitants = codomain.data.get("inhabitants", "infinite")
        
        if (domain_inhabitants != "infinite" and codomain_inhabitants != "infinite"):
            # Number of functions is |B|^|A|
            num_functions = len(codomain_inhabitants) ** len(domain_inhabitants)
            function_inhabitants = f"finite({num_functions})"
        else:
            function_inhabitants = "infinite"
        
        function_type = Object(function_name, {
            "type": "function",
            "domain": domain,
            "codomain": codomain,
            "inhabitants": function_inhabitants
        })
        
        self.add_object(function_type)
        return function_type
    
    def get_type(self, name: str) -> Optional[Object]:
        """Get a basic type by name"""
        type_map = {
            "Unit": self.unit_type,
            "Bool": self.bool_type,
            "ℕ": self.nat_type,
            "ℤ": self.int_type,
            "String": self.string_type,
            "⊥": self.bottom_type
        }
        return type_map.get(name)


class GroupCategory(Category):
    """One-object category from a group"""
    
    def __init__(self, group_name: str, elements: Set[Any], operation: Callable[[Any, Any], Any], identity: Any):
        super().__init__(f"Group({group_name})")
        self.group_elements = elements
        self.group_op = operation
        self.group_identity = identity
        self._build_group_category()
        
        # add_basic_constructor_to_category()
    
    def _build_group_category(self):
        """Build one-object category from group"""
        # Single object
        star = Object("*", {"type": "group_object"})
        self.add_object(star)
        
        # Morphisms are group elements
        for elem in self.group_elements:
            elem_name = str(elem)
            morphism = Morphism(elem_name, star, star, {
                'type': 'group_element',
                'element': elem,
                'is_identity': (elem == self.group_identity)
            })
            self.add_morphism(morphism)
        
        # Set compositions according to group operation
        for g in self.group_elements:
            for h in self.group_elements:
                result = self.group_op(g, h)
                
                # Find morphisms
                morph_g = next(m for m in self.morphisms if m.data['element'] == g)
                morph_h = next(m for m in self.morphisms if m.data['element'] == h)
                morph_result = next(m for m in self.morphisms if m.data['element'] == result)
                
                # Set composition h ∘ g = result
                self.set_composition(morph_g, morph_h, morph_result)
    
    @staticmethod
    def create_cyclic_group(n: int) -> 'GroupCategory':
        """Create cyclic group Z/nZ"""
        elements = set(range(n))
        operation = lambda a, b: (a + b) % n
        return GroupCategory(f"Z/{n}Z", elements, operation, 0)
    
    @staticmethod
    def create_symmetric_group(n: int) -> 'GroupCategory':
        """Create symmetric group S_n (simplified for small n)"""
        if n <= 3:
            # For S_2: elements are identity and swap
            if n == 2:
                elements = {"id", "swap"}
                
                def s2_op(a, b):
                    if a == "id": return b
                    if b == "id": return a
                    return "id"  # swap ∘ swap = id
                
                return GroupCategory("S_2", elements, s2_op, "id")
        
        # For larger groups, this gets complex - simplified version
        elements = {f"σ_{i}" for i in range(n)}
        operation = lambda a, b: f"({a}∘{b})"  # Simplified
        return GroupCategory(f"S_{n}", elements, operation, "σ_0")


# FACTORY FUNCTIONS FOR EASY CREATION

class StandardCategories:
    """Factory for creating standard categories easily"""
    
    @staticmethod
    def finite_sets(max_size: int = 4) -> FiniteSetCategory:
        """Create FinSet with sets up to given size"""
        return FiniteSetCategory(max_size)
    
    @staticmethod
    def chain_poset(length: int) -> PosetCategory:
        """Create chain poset 0 ≤ 1 ≤ ... ≤ n-1"""
        return PosetCategory.create_chain(length)
    
    @staticmethod
    def diamond_poset() -> PosetCategory:
        """Create diamond poset"""
        return PosetCategory.create_diamond()
    
    @staticmethod
    def discrete_poset(elements: List[Any]) -> PosetCategory:
        """Create discrete poset"""
        return PosetCategory.create_discrete(set(elements))
    
    @staticmethod
    def basic_types() -> TypeCategory:
        """Create category of basic types"""
        return TypeCategory()
    
    @staticmethod
    def cyclic_group(n: int) -> GroupCategory:
        """Create cyclic group Z/nZ as category"""
        return GroupCategory.create_cyclic_group(n)
    
    @staticmethod
    def boolean_algebra() -> PosetCategory:
        """Create Boolean algebra as poset"""
        elements = {"⊥", "⊤"}
        order = {("⊥", "⊥"), ("⊤", "⊤"), ("⊥", "⊤")}
        return PosetCategory("Bool", elements, order)
    
    @staticmethod
    def terminal_category():
        """Create the terminal category 1 (one object, one morphism)"""
        from hypercat.core.core import Category, Object
        cat = Category("1")
        obj = Object("*")
        cat.add_object(obj)
        return cat
    
    @staticmethod
    def initial_category():
        """Create the initial category 0 (no objects, no morphisms)"""
        from hypercat.core.core import Category
        return Category("0")
    
    @staticmethod
    def discrete_category(objects):
        """Create discrete category from list of object names"""
        from hypercat.core.core import Category, Object
        cat = Category("Discrete")
        for obj_name in objects:
            obj = Object(str(obj_name))
            cat.add_object(obj)
        return cat
    
    @staticmethod
    def arrow_category():
        """Create the arrow category → (two objects, one non-identity morphism)"""
        from hypercat.core.core import Category, Object, Morphism
        cat = Category("→")
        
        zero = Object("0")
        one = Object("1") 
        cat.add_object(zero)
        cat.add_object(one)
        
        arrow = Morphism("→", zero, one)
        cat.add_morphism(arrow)
        
        return cat


# DEMONSTRATION FUNCTION

def demonstrate_standard_categories():
    """Show off all the standard categories"""
    
    print("🏗️  Standard Categories Demo")
    print("=" * 50)
    
    # 1. Finite Sets
    print("\n1. 📦 Finite Sets Category")
    finset = StandardCategories.finite_sets(3)
    print(finset.display_summary())
    
    # Test operations
    A = finset.get_set(1)  # {1}
    B = finset.get_set(2)  # {1, 2}
    if A and B:
        print(f"\nTesting A = {A.name}, B = {B.name}")
        
        product = finset.compute_product([A, B])
        print(f"A × B = {product.name if product else 'None'}")
        if product:
            print(f"  Elements: {product.data}")
        
        coproduct = finset.compute_coproduct([A, B])
        print(f"A + B = {coproduct.name if coproduct else 'None'}")
        if coproduct:
            print(f"  Elements: {coproduct.data}")
    
    # 2. Poset Categories
    print("\n\n2. 📊 Poset Categories")
    
    # Chain
    chain = StandardCategories.chain_poset(4)
    print(f"Chain poset: {len(chain.objects)} objects, {len(chain.morphisms)} morphisms")
    print(f"Initial: {chain.find_initial()}")
    print(f"Terminal: {chain.find_terminal()}")
    
    # Diamond
    diamond = StandardCategories.diamond_poset()
    print(f"\nDiamond poset: {len(diamond.objects)} objects, {len(diamond.morphisms)} morphisms")
    print(f"Minimal elements: {[obj.name for obj in diamond.find_minimal_elements()]}")
    print(f"Maximal elements: {[obj.name for obj in diamond.find_maximal_elements()]}")
    
    # 3. Type Category
    print("\n\n3. 🔢 Type Category")
    types = StandardCategories.basic_types()
    print(f"Basic types: {len(types.objects)} objects, {len(types.morphisms)} morphisms")
    
    # Create some composite types
    bool_type = types.get_type("Bool")
    unit_type = types.get_type("Unit")
    
    if bool_type and unit_type:
        product_type = types.create_product_type(bool_type, unit_type)
        print(f"Bool × Unit = {product_type.name}")
        print(f"  Inhabitants: {product_type.data['inhabitants']}")
        
        sum_type = types.create_sum_type(bool_type, unit_type)
        print(f"Bool + Unit = {sum_type.name}")
        print(f"  Inhabitants: {sum_type.data['inhabitants']}")
    
    # 4. Group Category
    print("\n\n4. 🔄 Group Category")
    z3 = StandardCategories.cyclic_group(3)
    print(f"Z/3Z: {len(z3.objects)} object, {len(z3.morphisms)} morphisms")
    print(f"Object: {[obj.name for obj in z3.objects]}")
    print(f"Morphisms: {[m.name for m in z3.morphisms]}")
    
    # Test group composition
    morphisms = list(z3.morphisms)
    if len(morphisms) >= 2:
        m1, m2 = morphisms[0], morphisms[1]
        composition = z3.compose(m1, m2)
        print(f"Composition {m1.name} ∘ {m2.name} = {composition.name if composition else 'None'}")
    
    print("\n✅ Standard categories demonstration complete!")
    print("\nNow you have REAL categories to work with!")


if __name__ == "__main__":
    demonstrate_standard_categories()

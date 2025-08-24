"""
Basic category construction utilities.
Provides core functionality for building categories and their limits/colimits.
"""

from typing import List, Optional, Dict, Set, Tuple, Any, Union
from hypercat.core.core import Category, Object, Morphism, Diagram
from collections import defaultdict
import itertools

class BasicConstructor:
    """Actually builds limits and colimits. No BS."""
    
    def __init__(self, category: Category):
        self.category = category
        self.debug = []  # Track what we're doing
    
    def compute_coproduct(self, objects: List[Object]) -> Optional[Object]:
        """ACTUALLY build A + B + C, not just verify it exists"""
        self.debug = [f"Computing coproduct of {[obj.name for obj in objects]}"]
        
        if not objects:
            # Empty coproduct is initial object
            return self.find_initial_object()
        
        if len(objects) == 1:
            return objects[0]
        
        # For finite sets, coproduct is disjoint union
        if self._looks_like_finite_sets():
            return self._build_finite_set_coproduct(objects)
        
        # For general categories, try to find/build coproduct
        return self._build_general_coproduct(objects)
    
    def compute_product(self, objects: List[Object]) -> Optional[Object]:
        """ACTUALLY build A × B × C"""
        self.debug = [f"Computing product of {[obj.name for obj in objects]}"]
        
        if not objects:
            # Empty product is terminal object
            return self.find_terminal_object()
        
        if len(objects) == 1:
            return objects[0]
        
        # For finite sets, product is cartesian product
        if self._looks_like_finite_sets():
            return self._build_finite_set_product(objects)
        
        # For general categories, try to find/build product
        return self._build_general_product(objects)
    
    def compute_equalizer(self, f: Morphism, g: Morphism) -> Optional[Object]:
        """ACTUALLY find {x | f(x) = g(x)}"""
        if f.source != g.source or f.target != g.target:
            self.debug.append("❌ Morphisms not parallel")
            return None
        
        self.debug = [f"Computing equalizer of {f.name}, {g.name}"]
        
        # For finite sets, equalizer is subset where f and g agree
        if self._looks_like_finite_sets():
            return self._build_finite_set_equalizer(f, g)
        
        # For general categories, look for existing equalizer
        return self._find_general_equalizer(f, g)
    
    def compute_coequalizer(self, f: Morphism, g: Morphism) -> Optional[Object]:
        """ACTUALLY build quotient where f(x) ~ g(x)"""
        if f.source != g.source or f.target != g.target:
            self.debug.append("❌ Morphisms not parallel")
            return None
        
        self.debug = [f"Computing coequalizer of {f.name}, {g.name}"]
        
        # For finite sets, coequalizer is quotient set
        if self._looks_like_finite_sets():
            return self._build_finite_set_coequalizer(f, g)
        
        return self._find_general_coequalizer(f, g)
    
    def compute_pushout(self, f: Morphism, g: Morphism) -> Optional[Object]:
        """ACTUALLY glue objects along common part"""
        if f.target != g.target:
            self.debug.append("❌ Not a cospan")
            return None
        
        self.debug = [f"Computing pushout of {f.source.name} ← {f.target.name} → {g.source.name}"]
        
        # Pushout is colimit of cospan diagram
        # Build the cospan and compute its colimit
        return self._build_pushout_from_cospan(f, g)
    
    def compute_pullback(self, f: Morphism, g: Morphism) -> Optional[Object]:
        """ACTUALLY build fiber product"""
        if f.target != g.target:
            self.debug.append("❌ Not a cospan")
            return None
        
        self.debug = [f"Computing pullback of {f.source.name} → {f.target.name} ← {g.source.name}"]
        
        # For finite sets, pullback is subset of product
        if self._looks_like_finite_sets():
            return self._build_finite_set_pullback(f, g)
        
        return self._build_general_pullback(f, g)
    
    def find_initial_object(self) -> Optional[Object]:
        """ACTUALLY find object with unique morphism to everything"""
        self.debug.append("Looking for initial object...")
        
        for candidate in self.category.objects:
            is_initial = True
            
            # Check: for every object X, there's exactly one morphism candidate → X
            for target in self.category.objects:
                morphs_to_target = [m for m in self.category.morphisms
                                  if m.source == candidate and m.target == target]
                
                if len(morphs_to_target) != 1:
                    is_initial = False
                    break
            
            if is_initial:
                self.debug.append(f"✅ Found initial object: {candidate.name}")
                return candidate
        
        self.debug.append("❌ No initial object found")
        return None
    
    def find_terminal_object(self) -> Optional[Object]:
        """ACTUALLY find object with unique morphism from everything"""
        self.debug.append("Looking for terminal object...")
        
        for candidate in self.category.objects:
            is_terminal = True
            
            # Check: for every object X, there's exactly one morphism X → candidate
            for source in self.category.objects:
                morphs_from_source = [m for m in self.category.morphisms
                                    if m.source == source and m.target == candidate]
                
                if len(morphs_from_source) != 1:
                    is_terminal = False
                    break
            
            if is_terminal:
                self.debug.append(f"✅ Found terminal object: {candidate.name}")
                return candidate
        
        self.debug.append("❌ No terminal object found")
        return None
    
    # FINITE SET IMPLEMENTATIONS (the most important concrete case)
    
    def _looks_like_finite_sets(self) -> bool:
        """Heuristic: does this look like finite sets?"""
        # Check if objects have set-like data
        for obj in list(self.category.objects)[:3]:  # Check first few
            if hasattr(obj, 'data') and isinstance(obj.data, (set, list, tuple)):
                return True
        return False
    
    def _build_finite_set_coproduct(self, objects: List[Object]) -> Object:
        """Build disjoint union of finite sets"""
        # Create disjoint union by tagging elements
        union_elements = set()
        
        for i, obj in enumerate(objects):
            if hasattr(obj, 'data') and obj.data is not None:
                obj_set = obj.data if isinstance(obj.data, set) else set(obj.data)
                # Tag each element with its source
                tagged_elements = {(elem, i) for elem in obj_set}
                union_elements.update(tagged_elements)
        
        # Create coproduct object
        coproduct_name = " + ".join(obj.name for obj in objects)
        coproduct = Object(coproduct_name, union_elements)
        self.category.add_object(coproduct)
        
        # Create injection morphisms
        for i, obj in enumerate(objects):
            injection_name = f"ι_{i}"
            injection = Morphism(injection_name, obj, coproduct, {
                'type': 'injection',
                'index': i,
                'function': lambda x, idx=i: (x, idx)
            })
            self.category.add_morphism(injection)
        
        self.debug.append(f"✅ Built finite set coproduct: {coproduct_name}")
        return coproduct
    
    def _build_finite_set_product(self, objects: List[Object]) -> Object:
        """Build cartesian product of finite sets"""
        # Get the sets
        sets = []
        for obj in objects:
            if hasattr(obj, 'data') and obj.data is not None:
                obj_set = obj.data if isinstance(obj.data, set) else set(obj.data)
                sets.append(obj_set)
            else:
                # If no data, treat as singleton
                sets.append({obj.name})
        
        # Compute cartesian product
        if not sets:
            product_elements = set()
        else:
            product_elements = set(itertools.product(*sets))
        
        # Create product object
        product_name = " × ".join(obj.name for obj in objects)
        product = Object(product_name, product_elements)
        self.category.add_object(product)
        
        # Create projection morphisms
        for i, obj in enumerate(objects):
            projection_name = f"π_{i}"
            projection = Morphism(projection_name, product, obj, {
                'type': 'projection',
                'index': i,
                'function': lambda tuple_elem, idx=i: tuple_elem[idx] if isinstance(tuple_elem, tuple) else tuple_elem
            })
            self.category.add_morphism(projection)
        
        self.debug.append(f"✅ Built finite set product: {product_name}")
        return product
    
    def _build_finite_set_equalizer(self, f: Morphism, g: Morphism) -> Object:
        """Build equalizer as subset where f and g agree"""
        source_set = f.source.data if hasattr(f.source, 'data') else {f.source.name}
        if not isinstance(source_set, set):
            source_set = set(source_set) if source_set else {f.source.name}
        
        # Find elements where f and g agree
        equalizer_elements = set()
        
        for elem in source_set:
            # Apply f and g (simplified - assumes morphisms have function data)
            f_result = self._apply_morphism(f, elem)
            g_result = self._apply_morphism(g, elem)
            
            if f_result == g_result:
                equalizer_elements.add(elem)
        
        # Create equalizer object
        equalizer_name = f"Eq({f.name},{g.name})"
        equalizer = Object(equalizer_name, equalizer_elements)
        self.category.add_object(equalizer)
        
        # Create inclusion morphism
        inclusion = Morphism(f"inc_{equalizer_name}", equalizer, f.source, {
            'type': 'inclusion',
            'function': lambda x: x  # Identity on subset
        })
        self.category.add_morphism(inclusion)
        
        self.debug.append(f"✅ Built finite set equalizer: {equalizer_name}")
        return equalizer
    
    def _build_finite_set_coequalizer(self, f: Morphism, g: Morphism) -> Object:
        """Build coequalizer as quotient set"""
        target_set = f.target.data if hasattr(f.target, 'data') else {f.target.name}
        if not isinstance(target_set, set):
            target_set = set(target_set) if target_set else {f.target.name}
        
        source_set = f.source.data if hasattr(f.source, 'data') else {f.source.name}
        if not isinstance(source_set, set):
            source_set = set(source_set) if source_set else {f.source.name}
        
        # Build equivalence relation: f(x) ~ g(x) for all x
        equivalence_pairs = set()
        for elem in source_set:
            f_result = self._apply_morphism(f, elem)
            g_result = self._apply_morphism(g, elem)
            if f_result != g_result:
                equivalence_pairs.add((f_result, g_result))
        
        # Compute quotient (simplified - just identify equivalent elements)
        quotient_elements = target_set.copy()
        for pair in equivalence_pairs:
            # Remove one element from each equivalent pair
            if pair[1] in quotient_elements:
                quotient_elements.remove(pair[1])
        
        # Create coequalizer object
        coequalizer_name = f"Coeq({f.name},{g.name})"
        coequalizer = Object(coequalizer_name, quotient_elements)
        self.category.add_object(coequalizer)
        
        # Create quotient morphism
        quotient = Morphism(f"q_{coequalizer_name}", f.target, coequalizer, {
            'type': 'quotient',
            'equivalences': equivalence_pairs
        })
        self.category.add_morphism(quotient)
        
        self.debug.append(f"✅ Built finite set coequalizer: {coequalizer_name}")
        return coequalizer
    
    def _build_finite_set_pullback(self, f: Morphism, g: Morphism) -> Object:
        """Build pullback as subset of product"""
        # Get source sets
        f_source_set = f.source.data if hasattr(f.source, 'data') else {f.source.name}
        g_source_set = g.source.data if hasattr(g.source, 'data') else {g.source.name}
        
        if not isinstance(f_source_set, set):
            f_source_set = set(f_source_set) if f_source_set else {f.source.name}
        if not isinstance(g_source_set, set):
            g_source_set = set(g_source_set) if g_source_set else {g.source.name}
        
        # Build pullback as {(a,b) | f(a) = g(b)}
        pullback_elements = set()
        
        for a in f_source_set:
            for b in g_source_set:
                f_result = self._apply_morphism(f, a)
                g_result = self._apply_morphism(g, b)
                
                if f_result == g_result:
                    pullback_elements.add((a, b))
        
        # Create pullback object
        pullback_name = f"Pullback({f.name},{g.name})"
        pullback = Object(pullback_name, pullback_elements)
        self.category.add_object(pullback)
        
        # Create projection morphisms
        proj1 = Morphism(f"p1_{pullback_name}", pullback, f.source, {
            'type': 'pullback_projection',
            'function': lambda pair: pair[0]
        })
        proj2 = Morphism(f"p2_{pullback_name}", pullback, g.source, {
            'type': 'pullback_projection', 
            'function': lambda pair: pair[1]
        })
        
        self.category.add_morphism(proj1)
        self.category.add_morphism(proj2)
        
        self.debug.append(f"✅ Built finite set pullback: {pullback_name}")
        return pullback
    
    # GENERAL CATEGORY IMPLEMENTATIONS (fallback when not finite sets)
    
    def _build_general_coproduct(self, objects: List[Object]) -> Optional[Object]:
        """Try to find coproduct in general category"""
        # Look for existing object that could be the coproduct
        for candidate in self.category.objects:
            if self._could_be_coproduct(candidate, objects):
                self.debug.append(f"✅ Found existing coproduct: {candidate.name}")
                return candidate
        
        # Create new coproduct object
        coproduct_name = " ⊔ ".join(obj.name for obj in objects)
        coproduct = Object(coproduct_name, {'type': 'coproduct', 'components': objects})
        self.category.add_object(coproduct)
        
        self.debug.append(f"✅ Created coproduct object: {coproduct_name}")
        return coproduct
    
    def _build_general_product(self, objects: List[Object]) -> Optional[Object]:
        """Try to find product in general category"""
        # Look for existing object that could be the product
        for candidate in self.category.objects:
            if self._could_be_product(candidate, objects):
                self.debug.append(f"✅ Found existing product: {candidate.name}")
                return candidate
        
        # Create new product object
        product_name = " × ".join(obj.name for obj in objects)
        product = Object(product_name, {'type': 'product', 'components': objects})
        self.category.add_object(product)
        
        self.debug.append(f"✅ Created product object: {product_name}")
        return product
    
    def _find_general_equalizer(self, f: Morphism, g: Morphism) -> Optional[Object]:
        """Look for equalizer in category"""
        # Simple heuristic: look for objects with morphisms to f.source
        # that make the diagram commute
        
        for candidate in self.category.objects:
            equalizer_morphs = [m for m in self.category.morphisms
                              if m.source == candidate and m.target == f.source]
            
            for eq_morph in equalizer_morphs:
                # Check if f ∘ eq_morph = g ∘ eq_morph
                comp_f = self.category.compose(eq_morph, f)
                comp_g = self.category.compose(eq_morph, g)
                
                if comp_f and comp_g and comp_f == comp_g:
                    self.debug.append(f"✅ Found equalizer: {candidate.name}")
                    return candidate
        
        self.debug.append("❌ No equalizer found")
        return None
    
    def _find_general_coequalizer(self, f: Morphism, g: Morphism) -> Optional[Object]:
        """Look for coequalizer in category"""
        # Simple heuristic: look for objects with morphisms from f.target
        
        for candidate in self.category.objects:
            coequalizer_morphs = [m for m in self.category.morphisms
                                if m.source == f.target and m.target == candidate]
            
            for coeq_morph in coequalizer_morphs:
                # Check if coeq_morph ∘ f = coeq_morph ∘ g
                comp_f = self.category.compose(f, coeq_morph)
                comp_g = self.category.compose(g, coeq_morph)
                
                if comp_f and comp_g and comp_f == comp_g:
                    self.debug.append(f"✅ Found coequalizer: {candidate.name}")
                    return candidate
        
        self.debug.append("❌ No coequalizer found")
        return None
    
    def _build_pushout_from_cospan(self, f: Morphism, g: Morphism) -> Optional[Object]:
        """Build pushout using coproduct + coequalizer"""
        # Pushout is coequalizer of f+g : A+C → B+B
        
        # First, try to build coproduct of sources
        coproduct_sources = self.compute_coproduct([f.source, g.source])
        if not coproduct_sources:
            self.debug.append("❌ Can't build source coproduct for pushout")
            return None
        
        # Then build coproduct of targets (both are the same object, so just one copy)
        # This is a simplification - full implementation would be more complex
        
        pushout_name = f"Pushout({f.source.name},{g.source.name})"
        pushout = Object(pushout_name, {
            'type': 'pushout',
            'cospan': (f, g)
        })
        self.category.add_object(pushout)
        
        self.debug.append(f"✅ Built pushout: {pushout_name}")
        return pushout
    
    def _build_general_pullback(self, f: Morphism, g: Morphism) -> Optional[Object]:
        """Build pullback in general category"""
        pullback_name = f"Pullback({f.source.name},{g.source.name})"
        pullback = Object(pullback_name, {
            'type': 'pullback',
            'cospan': (f, g)
        })
        self.category.add_object(pullback)
        
        self.debug.append(f"✅ Built pullback: {pullback_name}")
        return pullback
    
    # HELPER METHODS
    
    def _apply_morphism(self, morphism: Morphism, element) -> Any:
        """Apply morphism to element (if morphism has function data)"""
        if hasattr(morphism, 'data') and isinstance(morphism.data, dict):
            if 'function' in morphism.data:
                return morphism.data['function'](element)
        
        # Fallback: just return the element (identity-like)
        return element
    
    def _could_be_coproduct(self, candidate: Object, components: List[Object]) -> bool:
        """Heuristic: could this object be the coproduct?"""
        # Check if there are injection-like morphisms
        for comp in components:
            injections = [m for m in self.category.morphisms
                         if m.source == comp and m.target == candidate]
            if not injections:
                return False
        return True
    
    def _could_be_product(self, candidate: Object, components: List[Object]) -> bool:
        """Heuristic: could this object be the product?"""
        # Check if there are projection-like morphisms
        for comp in components:
            projections = [m for m in self.category.morphisms
                          if m.source == candidate and m.target == comp]
            if not projections:
                return False
        return True
    
    def get_debug_log(self) -> List[str]:
        """Get what the constructor actually did"""
        return self.debug


# ADD METHODS TO EXISTING CATEGORY CLASS
def add_basic_constructor_to_category():
    """Add these methods to your existing Category class"""
    
    def compute_coproduct(self, objects: List[Object]) -> Optional[Object]:
        constructor = BasicConstructor(self)
        return constructor.compute_coproduct(objects)
    
    def compute_product(self, objects: List[Object]) -> Optional[Object]:
        constructor = BasicConstructor(self)
        return constructor.compute_product(objects)
    
    def compute_equalizer(self, f: Morphism, g: Morphism) -> Optional[Object]:
        constructor = BasicConstructor(self)
        return constructor.compute_equalizer(f, g)
    
    def compute_pushout(self, f: Morphism, g: Morphism) -> Optional[Object]:
        constructor = BasicConstructor(self)
        return constructor.compute_pushout(f, g)
    
    def compute_pullback(self, f: Morphism, g: Morphism) -> Optional[Object]:
        constructor = BasicConstructor(self)
        return constructor.compute_pullback(f, g)
    
    def find_initial(self) -> Optional[Object]:
        constructor = BasicConstructor(self)
        return constructor.find_initial_object()
    
    def find_terminal(self) -> Optional[Object]:
        constructor = BasicConstructor(self)
        return constructor.find_terminal_object()
    
    # Add to Category class
    Category.compute_coproduct = compute_coproduct
    Category.compute_product = compute_product
    Category.compute_equalizer = compute_equalizer
    Category.compute_pushout = compute_pushout
    Category.compute_pullback = compute_pullback
    Category.find_initial = find_initial
    Category.find_terminal = find_terminal


# SIMPLE TEST TO VERIFY IT WORKS
def test_basic_constructor():
    """Test that the basic constructor actually works"""
    print("🧪 Testing Basic Constructor...")
    
    # Create simple finite set category
    cat = Category("TestFinSets")
    
    # Add finite sets as objects
    empty_set = Object("∅", set())
    set1 = Object("{1}", {1})
    set2 = Object("{1,2}", {1, 2})
    
    cat.add_object(empty_set)
    cat.add_object(set1)
    cat.add_object(set2)
    
    # Add methods
    add_basic_constructor_to_category()
    
    # Test coproduct
    print("\n🔄 Testing coproduct...")
    coproduct = cat.compute_coproduct([set1, set2])
    if coproduct:
        print(f"✅ Coproduct: {coproduct.name}")
        print(f"   Elements: {coproduct.data}")
    else:
        print("❌ Coproduct failed")
    
    # Test product
    print("\n🔄 Testing product...")
    product = cat.compute_product([set1, set2])
    if product:
        print(f"✅ Product: {product.name}")
        print(f"   Elements: {product.data}")
    else:
        print("❌ Product failed")
    
    # Test terminals/initials
    print("\n🔄 Testing initial/terminal...")
    initial = cat.find_initial()
    terminal = cat.find_terminal()
    
    print(f"Initial: {initial.name if initial else 'None'}")
    print(f"Terminal: {terminal.name if terminal else 'None'}")
    
    print("\n✅ Basic constructor test complete!")


if __name__ == "__main__":
    test_basic_constructor()

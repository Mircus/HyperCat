"""
Basic analysis tools for categories and morphisms.
Provides functionality to analyze categorical properties and structures.
"""

from typing import List, Dict, Set, Tuple, Any, Optional, Callable, Union
from hypercat.core.core import Category, Object, Morphism, Functor
from basic_constructor import BasicConstructor
from week2_standard_categories import StandardCategories, FiniteSetCategory, PosetCategory, TypeCategory
from collections import defaultdict
from dataclasses import dataclass

@dataclass
class MorphismAnalysis:
    """Complete analysis of a morphism"""
    morphism: Morphism
    is_monomorphism: bool
    is_epimorphism: bool
    is_isomorphism: bool
    is_endomorphism: bool
    is_automorphism: bool
    is_identity: bool
    analysis_notes: List[str]

@dataclass
class CategoryAnalysis:
    """Complete analysis of a category"""
    category: Category
    num_objects: int
    num_morphisms: int
    has_initial: bool
    has_terminal: bool
    has_zero: bool
    has_products: bool
    has_coproducts: bool
    has_equalizers: bool
    has_coequalizers: bool
    has_pullbacks: bool
    has_pushouts: bool
    is_preorder: bool
    is_groupoid: bool
    is_skeletal: bool
    connected_components: int
    analysis_summary: str

class MorphismAnalyzer:
    """Analyze individual morphisms"""
    
    def __init__(self, category: Category):
        self.category = category
        self.analysis_cache: Dict[Morphism, MorphismAnalysis] = {}
    
    def analyze_morphism(self, f: Morphism) -> MorphismAnalysis:
        """Complete analysis of a single morphism"""
        
        if f in self.analysis_cache:
            return self.analysis_cache[f]
        
        notes = []
        
        # Basic checks
        is_endo = f.source == f.target
        is_identity = self._is_identity(f)
        is_mono = self.is_monomorphism(f)
        is_epi = self.is_epimorphism(f)
        is_iso = self.is_isomorphism(f)
        is_auto = is_endo and is_iso
        
        # Add analysis notes
        if is_identity:
            notes.append("Identity morphism")
        if is_endo and not is_identity:
            notes.append("Non-trivial endomorphism")
        if is_mono and not is_iso:
            notes.append("Monomorphism (injective)")
        if is_epi and not is_iso:
            notes.append("Epimorphism (surjective)")
        if is_iso:
            notes.append("Isomorphism (bijective)")
        if is_auto:
            notes.append("Automorphism")
        
        # Special properties for concrete categories
        self._add_concrete_analysis(f, notes)
        
        analysis = MorphismAnalysis(
            morphism=f,
            is_monomorphism=is_mono,
            is_epimorphism=is_epi,
            is_isomorphism=is_iso,
            is_endomorphism=is_endo,
            is_automorphism=is_auto,
            is_identity=is_identity,
            analysis_notes=notes
        )
        
        self.analysis_cache[f] = analysis
        return analysis
    
    def is_monomorphism(self, f: Morphism) -> bool:
        """Check if morphism is monic (left-cancellative)"""
        
        # For concrete categories with functions, check injectivity
        if self._has_concrete_function(f):
            return self._check_injectivity(f)
        
        # General categorical definition: f is monic if
        # for all g, h: X → A, if f∘g = f∘h then g = h
        
        # Find all morphisms to f.source
        morphs_to_source = [m for m in self.category.morphisms if m.target == f.source]
        
        # Group by source object
        by_source = defaultdict(list)
        for m in morphs_to_source:
            by_source[m.source].append(m)
        
        # Check cancellation property
        for source_obj, morphs in by_source.items():
            if len(morphs) >= 2:
                for i, g in enumerate(morphs):
                    for h in morphs[i+1:]:
                        # Check if f∘g = f∘h
                        fg = self.category.compose(g, f)
                        fh = self.category.compose(h, f)
                        
                        if fg and fh and fg == fh and g != h:
                            return False  # Found counterexample
        
        return True
    
    def is_epimorphism(self, f: Morphism) -> bool:
        """Check if morphism is epic (right-cancellative)"""
        
        # For concrete categories with functions, check surjectivity
        if self._has_concrete_function(f):
            return self._check_surjectivity(f)
        
        # General categorical definition: f is epic if
        # for all g, h: B → X, if g∘f = h∘f then g = h
        
        # Find all morphisms from f.target
        morphs_from_target = [m for m in self.category.morphisms if m.source == f.target]
        
        # Group by target object
        by_target = defaultdict(list)
        for m in morphs_from_target:
            by_target[m.target].append(m)
        
        # Check cancellation property
        for target_obj, morphs in by_target.items():
            if len(morphs) >= 2:
                for i, g in enumerate(morphs):
                    for h in morphs[i+1:]:
                        # Check if g∘f = h∘f
                        gf = self.category.compose(f, g)
                        hf = self.category.compose(f, h)
                        
                        if gf and hf and gf == hf and g != h:
                            return False  # Found counterexample
        
        return True
    
    def is_isomorphism(self, f: Morphism) -> bool:
        """Check if morphism is an isomorphism"""
        
        # Look for inverse morphism
        inverse = self.find_inverse(f)
        return inverse is not None
    
    def find_inverse(self, f: Morphism) -> Optional[Morphism]:
        """Find inverse morphism if it exists"""
        
        # Look for g: B → A such that g∘f = id_A and f∘g = id_B
        candidates = [m for m in self.category.morphisms 
                     if m.source == f.target and m.target == f.source]
        
        for g in candidates:
            # Check g∘f = id_A
            gf = self.category.compose(f, g)
            id_A = self.category.identities.get(f.source)
            
            # Check f∘g = id_B  
            fg = self.category.compose(g, f)
            id_B = self.category.identities.get(f.target)
            
            if gf == id_A and fg == id_B:
                return g
        
        return None
    
    def _is_identity(self, f: Morphism) -> bool:
        """Check if morphism is an identity"""
        return f in self.category.identities.values()
    
    def _has_concrete_function(self, f: Morphism) -> bool:
        """Check if morphism has concrete function data"""
        return (hasattr(f, 'data') and isinstance(f.data, dict) and 
                'function' in f.data and callable(f.data['function']))
    
    def _check_injectivity(self, f: Morphism) -> bool:
        """Check injectivity for concrete function"""
        if not self._has_concrete_function(f):
            return False
        
        func = f.data['function']
        source_data = getattr(f.source, 'data', None)
        
        if not isinstance(source_data, (set, list, tuple)):
            return True  # Can't check, assume true
        
        # Check if function is injective on the domain
        seen_outputs = set()
        for input_val in source_data:
            try:
                output = func(input_val)
                if output in seen_outputs:
                    return False
                seen_outputs.add(output)
            except:
                continue
        
        return True
    
    def _check_surjectivity(self, f: Morphism) -> bool:
        """Check surjectivity for concrete function"""
        if not self._has_concrete_function(f):
            return False
        
        func = f.data['function']
        source_data = getattr(f.source, 'data', None)
        target_data = getattr(f.target, 'data', None)
        
        if not isinstance(source_data, (set, list, tuple)) or not isinstance(target_data, (set, list, tuple)):
            return True  # Can't check, assume true
        
        # Check if every target element is hit
        hit_targets = set()
        for input_val in source_data:
            try:
                output = func(input_val)
                hit_targets.add(output)
            except:
                continue
        
        return hit_targets >= set(target_data)
    
    def _add_concrete_analysis(self, f: Morphism, notes: List[str]):
        """Add analysis notes for concrete categories"""
        
        # Finite set analysis
        if hasattr(f.source, 'data') and isinstance(f.source.data, (set, list, tuple)):
            source_size = len(f.source.data) if f.source.data else 0
            target_size = len(f.target.data) if hasattr(f.target, 'data') and f.target.data else 0
            
            if source_size > target_size and self.is_monomorphism(f):
                notes.append("Impossible: injective from larger to smaller finite set")
            elif source_size < target_size and self.is_epimorphism(f):
                notes.append("Impossible: surjective from smaller to larger finite set")
        
        # Type analysis
        if (hasattr(f.source, 'data') and isinstance(f.source.data, dict) and 
            f.source.data.get('type') in ['unit', 'bool', 'bottom']):
            type_name = f.source.data['type']
            notes.append(f"Type morphism from {type_name}")
        
        # Group analysis
        if (hasattr(f.source, 'data') and isinstance(f.source.data, dict) and 
            f.source.data.get('type') == 'group_object'):
            notes.append("Group morphism (always isomorphism in group category)")

    def find_all_monomorphisms(self) -> List[Morphism]:
        """Find all monomorphisms in the category"""
        return [m for m in self.category.morphisms if self.is_monomorphism(m)]
    
    def find_all_epimorphisms(self) -> List[Morphism]:
        """Find all epimorphisms in the category"""
        return [m for m in self.category.morphisms if self.is_epimorphism(m)]
    
    def find_all_isomorphisms(self) -> List[Morphism]:
        """Find all isomorphisms in the category"""
        return [m for m in self.category.morphisms if self.is_isomorphism(m)]
    
    def find_all_automorphisms(self, obj: Object) -> List[Morphism]:
        """Find all automorphisms of an object"""
        endomorphisms = [m for m in self.category.morphisms 
                        if m.source == obj and m.target == obj]
        return [m for m in endomorphisms if self.is_isomorphism(m)]
    
    def compute_endomorphism_monoid(self, obj: Object) -> Dict[str, Any]:
        """Compute the endomorphism monoid End(X)"""
        endomorphisms = [m for m in self.category.morphisms 
                        if m.source == obj and m.target == obj]
        
        # Build composition table
        composition_table = {}
        for f in endomorphisms:
            for g in endomorphisms:
                comp = self.category.compose(f, g)
                if comp:
                    composition_table[(f.name, g.name)] = comp.name
        
        # Find identity
        identity = self.category.identities.get(obj)
        
        return {
            'object': obj.name,
            'endomorphisms': [m.name for m in endomorphisms],
            'composition_table': composition_table,
            'identity': identity.name if identity else None,
            'size': len(endomorphisms)
        }


class CategoryAnalyzer:
    """Analyze entire categories"""
    
    def __init__(self, category: Category):
        self.category = category
        self.morphism_analyzer = MorphismAnalyzer(category)
        self.constructor = BasicConstructor(category)
    
    def analyze_category(self) -> CategoryAnalysis:
        """Complete analysis of the category"""
        
        # Basic counts
        num_objects = len(self.category.objects)
        num_morphisms = len(self.category.morphisms)
        
        # Universal properties
        initial = self.constructor.find_initial_object()
        terminal = self.constructor.find_terminal_object()
        has_initial = initial is not None
        has_terminal = terminal is not None
        has_zero = has_initial and has_terminal and initial == terminal
        
        # Limits and colimits (test on small examples)
        has_products = self._test_has_products()
        has_coproducts = self._test_has_coproducts()
        has_equalizers = self._test_has_equalizers()
        has_coequalizers = self._test_has_coequalizers()
        has_pullbacks = self._test_has_pullbacks()
        has_pushouts = self._test_has_pushouts()
        
        # Structural properties
        is_preorder = self._is_preorder()
        is_groupoid = self._is_groupoid()
        is_skeletal = self._is_skeletal()
        connected_components = self._count_connected_components()
        
        # Generate summary
        summary = self._generate_summary(
            num_objects, num_morphisms, has_initial, has_terminal, has_zero,
            has_products, has_coproducts, is_preorder, is_groupoid, is_skeletal
        )
        
        return CategoryAnalysis(
            category=self.category,
            num_objects=num_objects,
            num_morphisms=num_morphisms,
            has_initial=has_initial,
            has_terminal=has_terminal,
            has_zero=has_zero,
            has_products=has_products,
            has_coproducts=has_coproducts,
            has_equalizers=has_equalizers,
            has_coequalizers=has_coequalizers,
            has_pullbacks=has_pullbacks,
            has_pushouts=has_pushouts,
            is_preorder=is_preorder,
            is_groupoid=is_groupoid,
            is_skeletal=is_skeletal,
            connected_components=connected_components,
            analysis_summary=summary
        )
    
    def _test_has_products(self) -> bool:
        """Test if category has binary products"""
        objects_list = list(self.category.objects)
        
        # Test a few pairs
        for i, obj1 in enumerate(objects_list[:3]):
            for obj2 in objects_list[i:i+3]:
                product = self.constructor.compute_product([obj1, obj2])
                if product is None:
                    return False
        return True
    
    def _test_has_coproducts(self) -> bool:
        """Test if category has binary coproducts"""
        objects_list = list(self.category.objects)
        
        # Test a few pairs
        for i, obj1 in enumerate(objects_list[:3]):
            for obj2 in objects_list[i:i+3]:
                coproduct = self.constructor.compute_coproduct([obj1, obj2])
                if coproduct is None:
                    return False
        return True
    
    def _test_has_equalizers(self) -> bool:
        """Test if category has equalizers"""
        # Find parallel morphism pairs and test
        morphisms = list(self.category.morphisms)
        
        for i, f in enumerate(morphisms[:5]):
            for g in morphisms[i+1:i+5]:
                if f.source == g.source and f.target == g.target and f != g:
                    equalizer = self.constructor.compute_equalizer(f, g)
                    return equalizer is not None  # If we find one, good enough for test
        
        return True  # No parallel pairs to test, vacuously true
    
    def _test_has_coequalizers(self) -> bool:
        """Test if category has coequalizers"""
        # Similar to equalizers
        morphisms = list(self.category.morphisms)
        
        for i, f in enumerate(morphisms[:5]):
            for g in morphisms[i+1:i+5]:
                if f.source == g.source and f.target == g.target and f != g:
                    coequalizer = self.constructor.compute_coequalizer(f, g)
                    return coequalizer is not None
        
        return True
    
    def _test_has_pullbacks(self) -> bool:
        """Test if category has pullbacks"""
        # Find cospan and test
        morphisms = list(self.category.morphisms)
        
        for i, f in enumerate(morphisms[:5]):
            for g in morphisms[i+1:i+5]:
                if f.target == g.target and f.source != g.source:
                    pullback = self.constructor.compute_pullback(f, g)
                    return pullback is not None
        
        return True
    
    def _test_has_pushouts(self) -> bool:
        """Test if category has pushouts"""
        # Find span and test
        morphisms = list(self.category.morphisms)
        
        for i, f in enumerate(morphisms[:5]):
            for g in morphisms[i+1:i+5]:
                if f.source == g.source and f.target != g.target:
                    pushout = self.constructor.compute_pushout(f, g)
                    return pushout is not None
        
        return True
    
    def _is_preorder(self) -> bool:
        """Check if category is a preorder (at most one morphism between any two objects)"""
        object_pairs = {}
        
        for morph in self.category.morphisms:
            if morph.source != morph.target:  # Skip identities
                pair = (morph.source, morph.target)
                if pair in object_pairs:
                    return False  # Found second morphism between same objects
                object_pairs[pair] = morph
        
        return True
    
    def _is_groupoid(self) -> bool:
        """Check if category is a groupoid (all morphisms are isomorphisms)"""
        for morph in self.category.morphisms:
            if not self.morphism_analyzer.is_isomorphism(morph):
                return False
        return True
    
    def _is_skeletal(self) -> bool:
        """Check if category is skeletal (isomorphic objects are equal)"""
        isomorphisms = self.morphism_analyzer.find_all_isomorphisms()
        
        # Check if any non-identity isomorphism exists
        for iso in isomorphisms:
            if iso.source != iso.target:
                return False
        
        return True
    
    def _count_connected_components(self) -> int:
        """Count connected components (objects reachable by morphisms)"""
        if not self.category.objects:
            return 0
        
        # Build adjacency for undirected graph
        adjacent = defaultdict(set)
        for morph in self.category.morphisms:
            if morph.source != morph.target:  # Skip identities
                adjacent[morph.source].add(morph.target)
                adjacent[morph.target].add(morph.source)
        
        # DFS to find components
        visited = set()
        components = 0
        
        for obj in self.category.objects:
            if obj not in visited:
                components += 1
                # DFS from this object
                stack = [obj]
                while stack:
                    current = stack.pop()
                    if current not in visited:
                        visited.add(current)
                        stack.extend(adjacent[current] - visited)
        
        return components
    
    def _generate_summary(self, num_objects: int, num_morphisms: int, 
                         has_initial: bool, has_terminal: bool, has_zero: bool,
                         has_products: bool, has_coproducts: bool,
                         is_preorder: bool, is_groupoid: bool, is_skeletal: bool) -> str:
        """Generate human-readable summary"""
        
        summary = []
        
        # Basic structure
        summary.append(f"Category with {num_objects} objects and {num_morphisms} morphisms")
        
        # Universal objects
        if has_zero:
            summary.append("Has zero object (initial = terminal)")
        elif has_initial and has_terminal:
            summary.append("Has both initial and terminal objects")
        elif has_initial:
            summary.append("Has initial object")
        elif has_terminal:
            summary.append("Has terminal object")
        else:
            summary.append("No initial or terminal objects")
        
        # Limits and colimits
        limit_info = []
        if has_products:
            limit_info.append("products")
        if has_coproducts:
            limit_info.append("coproducts")
        
        if limit_info:
            summary.append(f"Has {', '.join(limit_info)}")
        
        # Special types
        if is_groupoid:
            summary.append("Groupoid (all morphisms invertible)")
        elif is_preorder:
            summary.append("Preorder (at most one morphism between objects)")
        
        if is_skeletal:
            summary.append("Skeletal (no non-trivial isomorphisms)")
        
        return "; ".join(summary)
    
    def find_interesting_morphisms(self) -> Dict[str, List[Morphism]]:
        """Find morphisms of interest"""
        result = {
            'monomorphisms': self.morphism_analyzer.find_all_monomorphisms(),
            'epimorphisms': self.morphism_analyzer.find_all_epimorphisms(),
            'isomorphisms': self.morphism_analyzer.find_all_isomorphisms(),
            'non_identity_endomorphisms': []
        }
        
        # Find non-identity endomorphisms
        for morph in self.category.morphisms:
            if (morph.source == morph.target and 
                not self.morphism_analyzer._is_identity(morph)):
                result['non_identity_endomorphisms'].append(morph)
        
        return result
    
    def generate_morphism_report(self) -> str:
        """Generate detailed morphism analysis report"""
        interesting = self.find_interesting_morphisms()
        
        report = [f"=== Morphism Analysis for {self.category.name} ===\n"]
        
        for category_name, morphisms in interesting.items():
            if morphisms:
                report.append(f"{category_name.replace('_', ' ').title()} ({len(morphisms)}):")
                for morph in morphisms[:5]:  # Show first 5
                    analysis = self.morphism_analyzer.analyze_morphism(morph)
                    notes = ", ".join(analysis.analysis_notes) if analysis.analysis_notes else "No special properties"
                    report.append(f"  {morph.name}: {notes}")
                
                if len(morphisms) > 5:
                    report.append(f"  ... and {len(morphisms) - 5} more")
                report.append("")
        
        return "\n".join(report)


# ADD ANALYSIS METHODS TO CATEGORY CLASS

def add_analysis_to_category():
    """Add analysis methods to existing Category class"""
    
    def is_monomorphism(self, f: Morphism) -> bool:
        analyzer = MorphismAnalyzer(self)
        return analyzer.is_monomorphism(f)
    
    def is_epimorphism(self, f: Morphism) -> bool:
        analyzer = MorphismAnalyzer(self)
        return analyzer.is_epimorphism(f)
    
    def is_isomorphism(self, f: Morphism) -> bool:
        analyzer = MorphismAnalyzer(self)
        return analyzer.is_isomorphism(f)
    
    def find_all_isomorphisms(self) -> List[Morphism]:
        analyzer = MorphismAnalyzer(self)
        return analyzer.find_all_isomorphisms()
    
    def analyze_morphism(self, f: Morphism) -> MorphismAnalysis:
        analyzer = MorphismAnalyzer(self)
        return analyzer.analyze_morphism(f)
    
    def analyze_category(self) -> CategoryAnalysis:
        analyzer = CategoryAnalyzer(self)
        return analyzer.analyze_category()
    
    def has_products(self) -> bool:
        analyzer = CategoryAnalyzer(self)
        return analyzer._test_has_products()
    
    def has_coproducts(self) -> bool:
        analyzer = CategoryAnalyzer(self)
        return analyzer._test_has_coproducts()
    
    def is_groupoid(self) -> bool:
        analyzer = CategoryAnalyzer(self)
        return analyzer._is_groupoid()
    
    def is_preorder(self) -> bool:
        analyzer = CategoryAnalyzer(self)
        return analyzer._is_preorder()
    
    def generate_analysis_report(self) -> str:
        analyzer = CategoryAnalyzer(self)
        category_analysis = analyzer.analyze_category()
        morphism_report = analyzer.generate_morphism_report()
        
        report = [f"=== Complete Analysis of {self.name} ===\n"]
        report.append(category_analysis.analysis_summary)
        report.append("\n" + morphism_report)
        
        return "\n".join(report)
    
    # Add to Category class
    Category.is_monomorphism = is_monomorphism
    Category.is_epimorphism = is_epimorphism
    Category.is_isomorphism = is_isomorphism
    Category.find_all_isomorphisms = find_all_isomorphisms
    Category.analyze_morphism = analyze_morphism
    Category.analyze_category = analyze_category
    Category.has_products = has_products
    Category.has_coproducts = has_coproducts
    Category.is_groupoid = is_groupoid
    Category.is_preorder = is_preorder
    Category.generate_analysis_report = generate_analysis_report


# DEMONSTRATION

def demonstrate_analysis_tools():
    """Show off the analysis tools"""
    
    print("🔍 Analysis Tools Demo")
    print("=" * 50)
    
    # Add analysis methods
    add_analysis_to_category()
    
    # 1. Analyze FinSet
    print("\n1. 📦 FinSet Analysis")
    finset = StandardCategories.finite_sets(3)
    
    # Get some morphisms to analyze
    morphisms = list(finset.morphisms)[:5]
    
    for morph in morphisms:
        analysis = finset.analyze_morphism(morph)
        print(f"{morph.name}: {', '.join(analysis.analysis_notes) if analysis.analysis_notes else 'Basic morphism'}")
    
    # Category analysis
    cat_analysis = finset.analyze_category()
    print(f"\nFinSet Summary: {cat_analysis.analysis_summary}")
    
    # 2. Analyze Poset
    print("\n\n2. 📊 Poset Analysis")
    diamond = StandardCategories.diamond_poset()
    
    print(f"Is preorder: {diamond.is_preorder()}")
    print(f"Is groupoid: {diamond.is_groupoid()}")
    
    isomorphisms = diamond.find_all_isomorphisms()
    print(f"Isomorphisms: {[iso.name for iso in isomorphisms]}")
    
    # 3. Analyze Group Category  
    print("\n\n3. 🔄 Group Category Analysis")
    z3 = StandardCategories.cyclic_group(3)
    
    print(f"Is groupoid: {z3.is_groupoid()}")  # Should be True
    print(f"All morphisms are isomorphisms: {len(z3.find_all_isomorphisms()) == len(z3.morphisms)}")
    
    # 4. Generate complete reports
    print("\n\n4. 📋 Complete Analysis Reports")
    
    print("\n--- Diamond Poset Report ---")
    print(diamond.generate_analysis_report())
    
    print("\n--- Z/3Z Group Report ---")
    print(z3.generate_analysis_report())
    
    print("\n✅ Analysis tools demonstration complete!")
    print("\nNow you can analyze ANY category and its morphisms!")


if __name__ == "__main__":
    demonstrate_analysis_tools()

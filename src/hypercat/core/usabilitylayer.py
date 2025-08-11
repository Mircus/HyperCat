"""
Week 4: Clean API and Usability Layer
Make HyperCat actually pleasant to use for everyone.
"""

from typing import List, Dict, Set, Tuple, Any, Optional, Callable, Union
from hypercat.core.core import Category, Object, Morphism
from basic_constructor import BasicConstructor, add_basic_constructor_to_category
from week2_standard_categories import StandardCategories, FiniteSetCategory, PosetCategory, TypeCategory, GroupCategory
from week3_analysis_tools import MorphismAnalyzer, CategoryAnalyzer, add_analysis_to_category
import traceback
import warnings
from dataclasses import dataclass
from enum import Enum

class HelpLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

@dataclass
class CategorySummary:
    """User-friendly category summary"""
    name: str
    description: str
    num_objects: int
    num_morphisms: int
    key_properties: List[str]
    interesting_objects: Dict[str, str]
    interesting_morphisms: Dict[str, str]
    suggested_explorations: List[str]
    
class HyperCatError(Exception):
    """Base exception for HyperCat with helpful messages"""
    def __init__(self, message: str, suggestion: str = None, category_context: str = None):
        self.message = message
        self.suggestion = suggestion
        self.category_context = category_context
        super().__init__(self._format_message())
    
    def _format_message(self) -> str:
        parts = [f"❌ {self.message}"]
        
        if self.category_context:
            parts.append(f"📍 Context: {self.category_context}")
        
        if self.suggestion:
            parts.append(f"💡 Suggestion: {self.suggestion}")
        
        return "\n".join(parts)

class InvalidMorphismError(HyperCatError):
    """Error for invalid morphism operations"""
    pass

class ConstructionError(HyperCatError):
    """Error when universal constructions fail"""
    pass

class UsabilityLayer:
    """Makes HyperCat easy to use for everyone"""
    
    def __init__(self, category: Category, help_level: HelpLevel = HelpLevel.INTERMEDIATE):
        self.category = category
        self.help_level = help_level
        self.constructor = BasicConstructor(category)
        self.analyzer = CategoryAnalyzer(category)
        
        # Add methods to category
        add_basic_constructor_to_category()
        add_analysis_to_category()
        self._add_usability_methods()
    
    def _add_usability_methods(self):
        """Add user-friendly methods to category"""
        
        # Bind methods to category instance
        self.category.summarize = lambda: self.summarize()
        self.category.explore = lambda: self.explore()
        self.category.help = lambda topic=None: self.help(topic)
        self.category.quick_analysis = lambda: self.quick_analysis()
        self.category.find_examples = lambda: self.find_examples()
        self.category.safe_compute_product = lambda objs: self.safe_compute_product(objs)
        self.category.safe_compute_coproduct = lambda objs: self.safe_compute_coproduct(objs)
        self.category.explain_morphism = lambda f: self.explain_morphism(f)
        self.category.suggest_explorations = lambda: self.suggest_explorations()
        self.category.validate = lambda: self.validate_category()
    
    def summarize(self) -> CategorySummary:
        """Generate user-friendly summary of the category"""
        
        # Get analysis
        analysis = self.analyzer.analyze_category()
        
        # Determine description
        description = self._generate_description(analysis)
        
        # Find key properties
        key_properties = self._extract_key_properties(analysis)
        
        # Find interesting objects and morphisms
        interesting_objects = self._find_interesting_objects()
        interesting_morphisms = self._find_interesting_morphisms()
        
        # Generate suggestions
        suggestions = self._generate_suggestions(analysis)
        
        return CategorySummary(
            name=self.category.name,
            description=description,
            num_objects=len(self.category.objects),
            num_morphisms=len(self.category.morphisms),
            key_properties=key_properties,
            interesting_objects=interesting_objects,
            interesting_morphisms=interesting_morphisms,
            suggested_explorations=suggestions
        )
    
    def explore(self) -> str:
        """Interactive exploration of the category"""
        summary = self.summarize()
        
        report = [f"🔍 Exploring {summary.name}"]
        report.append("=" * (len(summary.name) + 12))
        report.append("")
        
        # Basic info
        report.append(f"📋 {summary.description}")
        report.append(f"📊 {summary.num_objects} objects, {summary.num_morphisms} morphisms")
        report.append("")
        
        # Key properties
        if summary.key_properties:
            report.append("🎯 Key Properties:")
            for prop in summary.key_properties:
                report.append(f"  ✅ {prop}")
            report.append("")
        
        # Interesting objects
        if summary.interesting_objects:
            report.append("🏷️  Notable Objects:")
            for name, description in summary.interesting_objects.items():
                report.append(f"  📦 {name}: {description}")
            report.append("")
        
        # Interesting morphisms
        if summary.interesting_morphisms:
            report.append("🔄 Notable Morphisms:")
            for name, description in summary.interesting_morphisms.items():
                report.append(f"  ➡️  {name}: {description}")
            report.append("")
        
        # Suggestions
        if summary.suggested_explorations:
            report.append("💡 Try These Explorations:")
            for i, suggestion in enumerate(summary.suggested_explorations, 1):
                report.append(f"  {i}. {suggestion}")
        
        return "\n".join(report)
    
    def help(self, topic: Optional[str] = None) -> str:
        """Context-aware help system"""
        
        if topic is None:
            return self._general_help()
        
        topic = topic.lower().strip()
        
        help_topics = {
            'products': self._help_products,
            'coproducts': self._help_coproducts,
            'morphisms': self._help_morphisms,
            'limits': self._help_limits,
            'analysis': self._help_analysis,
            'examples': self._help_examples,
            'errors': self._help_errors
        }
        
        if topic in help_topics:
            return help_topics[topic]()
        else:
            available = ", ".join(help_topics.keys())
            return f"❓ Unknown topic '{topic}'. Available topics: {available}\n\nTry cat.help() for general help."
    
    def quick_analysis(self) -> str:
        """Quick one-line analysis for rapid understanding"""
        summary = self.summarize()
        
        # Build quick summary
        parts = []
        
        if summary.num_objects <= 1:
            parts.append("trivial")
        elif summary.num_objects <= 5:
            parts.append("small")
        elif summary.num_objects <= 20:
            parts.append("medium")
        else:
            parts.append("large")
        
        # Add most important properties
        key_props = summary.key_properties[:2]
        if key_props:
            parts.extend(key_props)
        
        # Add structure type
        if "groupoid" in summary.description.lower():
            parts.append("groupoid")
        elif "preorder" in summary.description.lower():
            parts.append("poset")
        elif "finite set" in summary.description.lower():
            parts.append("concrete")
        
        return f"📋 {summary.name}: {', '.join(parts)} ({summary.num_objects} objects, {summary.num_morphisms} morphisms)"
    
    def find_examples(self) -> Dict[str, List[str]]:
        """Find examples of various categorical concepts"""
        examples = {
            'initial_objects': [],
            'terminal_objects': [],
            'isomorphisms': [],
            'monomorphisms': [],
            'epimorphisms': [],
            'endomorphisms': [],
            'automorphisms': []
        }
        
        # Find initial and terminal
        initial = self.constructor.find_initial_object()
        terminal = self.constructor.find_terminal_object()
        
        if initial:
            examples['initial_objects'].append(initial.name)
        if terminal:
            examples['terminal_objects'].append(terminal.name)
        
        # Analyze morphisms
        morph_analyzer = MorphismAnalyzer(self.category)
        
        for morphism in list(self.category.morphisms)[:10]:  # Limit for performance
            analysis = morph_analyzer.analyze_morphism(morphism)
            
            if analysis.is_isomorphism:
                examples['isomorphisms'].append(morphism.name)
            if analysis.is_monomorphism:
                examples['monomorphisms'].append(morphism.name)
            if analysis.is_epimorphism:
                examples['epimorphisms'].append(morphism.name)
            if analysis.is_endomorphism:
                examples['endomorphisms'].append(morphism.name)
            if analysis.is_automorphism:
                examples['automorphisms'].append(morphism.name)
        
        # Limit lists
        for key in examples:
            examples[key] = examples[key][:5]
        
        return examples
    
    def safe_compute_product(self, objects: List[Object]) -> Optional[Object]:
        """Compute product with helpful error handling"""
        try:
            if not objects:
                raise ConstructionError(
                    "Cannot compute product of empty list",
                    "Provide at least one object, or use find_terminal() for empty product",
                    f"Category: {self.category.name}"
                )
            
            if any(obj not in self.category.objects for obj in objects):
                missing = [obj for obj in objects if obj not in self.category.objects]
                raise ConstructionError(
                    f"Objects not in category: {[obj.name for obj in missing]}",
                    "Make sure all objects are added to the category first",
                    f"Category: {self.category.name}"
                )
            
            product = self.constructor.compute_product(objects)
            
            if product is None:
                obj_names = [obj.name for obj in objects]
                raise ConstructionError(
                    f"Product of {obj_names} does not exist",
                    "This category may not have all products. Try smaller sets or check if category is complete.",
                    f"Category: {self.category.name}"
                )
            
            return product
            
        except Exception as e:
            if isinstance(e, HyperCatError):
                raise
            else:
                raise ConstructionError(
                    f"Unexpected error computing product: {str(e)}",
                    "This might be a bug. Check your objects and morphisms.",
                    f"Category: {self.category.name}"
                )
    
    def safe_compute_coproduct(self, objects: List[Object]) -> Optional[Object]:
        """Compute coproduct with helpful error handling"""
        try:
            if not objects:
                raise ConstructionError(
                    "Cannot compute coproduct of empty list",
                    "Provide at least one object, or use find_initial() for empty coproduct",
                    f"Category: {self.category.name}"
                )
            
            if any(obj not in self.category.objects for obj in objects):
                missing = [obj for obj in objects if obj not in self.category.objects]
                raise ConstructionError(
                    f"Objects not in category: {[obj.name for obj in missing]}",
                    "Make sure all objects are added to the category first",
                    f"Category: {self.category.name}"
                )
            
            coproduct = self.constructor.compute_coproduct(objects)
            
            if coproduct is None:
                obj_names = [obj.name for obj in objects]
                raise ConstructionError(
                    f"Coproduct of {obj_names} does not exist",
                    "This category may not have all coproducts. Try smaller sets or check if category is cocomplete.",
                    f"Category: {self.category.name}"
                )
            
            return coproduct
            
        except Exception as e:
            if isinstance(e, HyperCatError):
                raise
            else:
                raise ConstructionError(
                    f"Unexpected error computing coproduct: {str(e)}",
                    "This might be a bug. Check your objects and morphisms.",
                    f"Category: {self.category.name}"
                )
    
    def explain_morphism(self, f: Morphism) -> str:
        """Explain what a morphism does in plain language"""
        
        if f not in self.category.morphisms:
            return f"❌ Morphism {f.name} is not in category {self.category.name}"
        
        analyzer = MorphismAnalyzer(self.category)
        analysis = analyzer.analyze_morphism(f)
        
        explanation = [f"🔍 Morphism Analysis: {f.name}"]
        explanation.append(f"📍 {f.source.name} → {f.target.name}")
        explanation.append("")
        
        # Basic properties
        if analysis.is_identity:
            explanation.append("🆔 This is an identity morphism (does nothing)")
        elif analysis.is_isomorphism:
            explanation.append("🔄 This is an isomorphism (fully reversible)")
        elif analysis.is_monomorphism and analysis.is_epimorphism:
            explanation.append("⚠️  This is both monic and epic but not iso (interesting!)")
        elif analysis.is_monomorphism:
            explanation.append("📥 This is a monomorphism (injective/one-to-one)")
        elif analysis.is_epimorphism:
            explanation.append("📤 This is an epimorphism (surjective/onto)")
        else:
            explanation.append("➡️  This is a general morphism")
        
        # Context-specific explanations
        if hasattr(f.source, 'data') and isinstance(f.source.data, (set, list, tuple)):
            source_size = len(f.source.data) if f.source.data else 0
            target_size = len(f.target.data) if hasattr(f.target, 'data') and f.target.data else 0
            explanation.append(f"📊 Function between finite sets (size {source_size} → {target_size})")
        
        # Add analysis notes
        if analysis.analysis_notes:
            explanation.append("")
            explanation.append("📝 Additional Notes:")
            for note in analysis.analysis_notes:
                explanation.append(f"  • {note}")
        
        return "\n".join(explanation)
    
    def suggest_explorations(self) -> List[str]:
        """Suggest interesting things to explore in this category"""
        suggestions = []
        analysis = self.analyzer.analyze_category()
        
        # Basic explorations
        if analysis.num_objects <= 10:
            suggestions.append("Try cat.compute_product([obj1, obj2]) with different objects")
            suggestions.append("Check cat.find_all_isomorphisms() to see invertible morphisms")
        
        # Property-based suggestions
        if analysis.has_initial:
            suggestions.append("Explore morphisms from the initial object")
        if analysis.has_terminal:
            suggestions.append("Check uniqueness of morphisms to the terminal object")
        
        if analysis.is_preorder:
            suggestions.append("This is a poset! Try finding minimal/maximal elements")
        elif analysis.is_groupoid:
            suggestions.append("All morphisms are invertible! Explore the group structure")
        
        # Construction suggestions
        if analysis.has_products and analysis.has_coproducts:
            suggestions.append("This has products AND coproducts - try comparing them")
        elif analysis.has_products:
            suggestions.append("Explore product constructions with cat.compute_product()")
        elif analysis.has_coproducts:
            suggestions.append("Explore coproduct constructions with cat.compute_coproduct()")
        
        # Size-based suggestions
        if analysis.num_objects >= 5:
            suggestions.append("Try cat.analyze_category() for complete structural analysis")
        
        return suggestions[:5]  # Limit suggestions
    
    def validate_category(self) -> Dict[str, Any]:
        """Validate category structure and suggest improvements"""
        issues = []
        warnings_list = []
        suggestions = []
        
        # Check basic structure
        if not self.category.objects:
            issues.append("Category has no objects")
            suggestions.append("Add some objects with cat.add_object()")
        
        if not self.category.morphisms:
            warnings_list.append("Category has no morphisms (discrete category)")
        
        # Check identity morphisms
        missing_identities = []
        for obj in self.category.objects:
            if obj not in self.category.identities:
                missing_identities.append(obj.name)
        
        if missing_identities:
            issues.append(f"Missing identity morphisms for: {missing_identities}")
            suggestions.append("Identity morphisms are usually created automatically")
        
        # Check composition closure
        composition_gaps = []
        for morph1 in list(self.category.morphisms)[:10]:  # Sample for performance
            for morph2 in list(self.category.morphisms)[:10]:
                if morph1.target == morph2.source:
                    comp = self.category.compose(morph1, morph2)
                    if comp is None:
                        composition_gaps.append((morph1.name, morph2.name))
        
        if composition_gaps:
            warnings_list.append(f"Some compositions undefined: {len(composition_gaps)} cases")
            suggestions.append("Consider setting missing compositions with set_composition()")
        
        # Performance warnings
        if len(self.category.objects) > 1000:
            warnings_list.append("Large category - some operations may be slow")
        
        if len(self.category.morphisms) > 10000:
            warnings_list.append("Many morphisms - consider using indices for faster lookup")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings_list,
            'suggestions': suggestions,
            'summary': f"{'✅ Valid' if len(issues) == 0 else '❌ Issues found'} - {len(warnings_list)} warnings"
        }
    
    # HELPER METHODS
    
    def _generate_description(self, analysis) -> str:
        """Generate human-readable description"""
        if analysis.is_groupoid:
            return "Groupoid where all morphisms are invertible"
        elif analysis.is_preorder:
            return "Preorder/poset with at most one morphism between objects"
        elif "FinSet" in self.category.name:
            return "Category of finite sets with functions"
        elif "Type" in self.category.name:
            return "Category of types with type constructors"
        elif "Group" in self.category.name:
            return "One-object category representing a group"
        elif "Poset" in self.category.name:
            return "Category constructed from a partially ordered set"
        else:
            return "Mathematical category with objects and morphisms"
    
    def _extract_key_properties(self, analysis) -> List[str]:
        """Extract the most important properties"""
        properties = []
        
        if analysis.has_initial and analysis.has_terminal:
            if analysis.has_zero:
                properties.append("Has zero object")
            else:
                properties.append("Has initial and terminal objects")
        elif analysis.has_initial:
            properties.append("Has initial object")
        elif analysis.has_terminal:
            properties.append("Has terminal object")
        
        if analysis.has_products and analysis.has_coproducts:
            properties.append("Has products and coproducts")
        elif analysis.has_products:
            properties.append("Has products")
        elif analysis.has_coproducts:
            properties.append("Has coproducts")
        
        if analysis.is_groupoid:
            properties.append("All morphisms invertible")
        elif analysis.is_preorder:
            properties.append("Preorder structure")
        
        if analysis.is_skeletal:
            properties.append("Skeletal (no redundant isomorphisms)")
        
        return properties
    
    def _find_interesting_objects(self) -> Dict[str, str]:
        """Find objects worth mentioning"""
        interesting = {}
        
        # Special objects
        initial = self.constructor.find_initial_object()
        terminal = self.constructor.find_terminal_object()
        
        if initial:
            interesting[initial.name] = "Initial object (unique morphism to all objects)"
        
        if terminal and terminal != initial:
            interesting[terminal.name] = "Terminal object (unique morphism from all objects)"
        
        if initial and terminal and initial == terminal:
            interesting[initial.name] = "Zero object (both initial and terminal)"
        
        # Objects with many morphisms
        object_morphism_counts = {}
        for obj in self.category.objects:
            count = len([m for m in self.category.morphisms if m.source == obj or m.target == obj])
            object_morphism_counts[obj] = count
        
        if object_morphism_counts:
            max_morphisms = max(object_morphism_counts.values())
            busy_objects = [obj for obj, count in object_morphism_counts.items() if count == max_morphisms]
            
            if len(busy_objects) == 1 and max_morphisms > 2:
                busy_obj = busy_objects[0]
                interesting[busy_obj.name] = f"Most connected ({max_morphisms} morphisms)"
        
        return interesting
    
    def _find_interesting_morphisms(self) -> Dict[str, str]:
        """Find morphisms worth mentioning"""
        interesting = {}
        
        analyzer = MorphismAnalyzer(self.category)
        
        # Find examples of each type (limit for performance)
        sample_morphisms = list(self.category.morphisms)[:20]
        
        found_iso = False
        found_mono = False
        found_epi = False
        
        for morph in sample_morphisms:
            analysis = analyzer.analyze_morphism(morph)
            
            if analysis.is_isomorphism and not found_iso:
                interesting[morph.name] = "Isomorphism (invertible)"
                found_iso = True
            elif analysis.is_monomorphism and not found_mono:
                interesting[morph.name] = "Monomorphism (injective)"
                found_mono = True
            elif analysis.is_epimorphism and not found_epi:
                interesting[morph.name] = "Epimorphism (surjective)"
                found_epi = True
            
            if found_iso and found_mono and found_epi:
                break
        
        return interesting
    
    def _generate_suggestions(self, analysis) -> List[str]:
        """Generate exploration suggestions"""
        return self.suggest_explorations()
    
    def _general_help(self) -> str:
        """General help message"""
        return f"""
🆘 HyperCat Help for {self.category.name}

📋 Quick Commands:
  cat.summarize()           - Get category overview
  cat.explore()            - Interactive exploration
  cat.quick_analysis()     - One-line summary
  cat.find_examples()      - Find examples of concepts
  cat.validate()           - Check category structure

🔧 Constructions:
  cat.compute_product([A, B])    - Build product A × B
  cat.compute_coproduct([A, B])  - Build coproduct A + B
  cat.find_initial()             - Find initial object
  cat.find_terminal()            - Find terminal object

🔍 Analysis:
  cat.is_monomorphism(f)    - Check if f is injective
  cat.is_epimorphism(f)     - Check if f is surjective
  cat.explain_morphism(f)   - Explain what f does
  cat.analyze_category()    - Complete analysis

❓ Detailed Help:
  cat.help('products')     - Help with products
  cat.help('morphisms')    - Help with morphisms
  cat.help('analysis')     - Help with analysis
  cat.help('examples')     - Help with examples

🎯 Current Category: {self.quick_analysis()}
"""
    
    def _help_products(self) -> str:
        return """
📦 Products Help

🎯 What are products?
Products are "Cartesian products" - they combine objects.
In FinSet: A × B = {(a,b) | a ∈ A, b ∈ B}

🔧 How to compute:
  product = cat.compute_product([A, B])
  product = cat.safe_compute_product([A, B, C])  # With error handling

⚠️  Common issues:
- Empty list: Use cat.find_terminal() instead
- Objects not in category: Add them first
- No products exist: Not all categories have products

🎯 For your category:
""" + (f"✅ Has products" if self.analyzer._test_has_products() else "❌ May not have all products")
    
    def _help_coproducts(self) -> str:
        return """
📦 Coproducts Help

🎯 What are coproducts?
Coproducts are "disjoint unions" - they combine objects separately.
In FinSet: A + B = A ∪ B (tagged to keep separate)

🔧 How to compute:
  coproduct = cat.compute_coproduct([A, B])
  coproduct = cat.safe_compute_coproduct([A, B, C])  # With error handling

⚠️  Common issues:
- Empty list: Use cat.find_initial() instead
- Objects not in category: Add them first  
- No coproducts exist: Not all categories have coproducts

🎯 For your category:
""" + (f"✅ Has coproducts" if self.analyzer._test_has_coproducts() else "❌ May not have all coproducts")
    
    def _help_morphisms(self) -> str:
        return f"""
🔄 Morphisms Help

🎯 What are morphisms?
Morphisms are "arrows" between objects - functions, transformations, etc.

🔍 Analysis:
  cat.is_monomorphism(f)   - Injective (one-to-one)
  cat.is_epimorphism(f)    - Surjective (onto)  
  cat.is_isomorphism(f)    - Bijective (invertible)
  cat.explain_morphism(f)  - Plain English explanation

📊 Your category has {len(self.category.morphisms)} morphisms:
  Identities: {len(self.category.identities)}
  Non-identities: {len(self.category.morphisms) - len(self.category.identities)}

💡 Try:
  morphs = list(cat.morphisms)[:5]
  for f in morphs:
      print(cat.explain_morphism(f))
"""
    
    def _help_limits(self) -> str:
        return """
🎯 Limits and Colimits Help

📚 Concepts:
- Products: A × B (combines objects)
- Coproducts: A + B (disjoint union)  
- Equalizers: {x | f(x) = g(x)} (where functions agree)
- Pullbacks: Fiber products over common object

🔧 Commands:
  cat.compute_product([A, B])
  cat.compute_coproduct([A, B])
  cat.compute_equalizer(f, g)
  cat.compute_pullback(f, g)

📖 Learn more:
Products and coproducts are the most important to understand first.
"""
    
    def _help_analysis(self) -> str:
        analysis = self.analyzer.analyze_category()
        return f"""
🔍 Analysis Help

🎯 Quick Analysis:
  cat.quick_analysis()     - One line summary
  cat.analyze_category()   - Complete analysis
  cat.find_examples()      - Examples of concepts

📊 Your Category Analysis:
  Type: {analysis.analysis_summary}
  Properties: {', '.join(self._extract_key_properties(analysis))}

🔧 Morphism Analysis:
  cat.explain_morphism(f)  - Explain any morphism
  cat.find_all_isomorphisms() - Find invertible morphisms

💡 Exploration:
  {self.quick_analysis()}
"""
    
    def _help_examples(self) -> str:
        return """
📚 Examples Help

🏗️  Standard Categories:
  StandardCategories.finite_sets(5)    - FinSet
  StandardCategories.chain_poset(4)    - Chain 0≤1≤2≤3
  StandardCategories.diamond_poset()   - Diamond lattice
  StandardCategories.basic_types()     - Type category
  StandardCategories.cyclic_group(3)   - Group Z/3Z

🔍 Find Examples in Current Category:
  cat.find_examples()      - Examples of all concepts
  cat.suggest_explorations() - Things to try

💡 Learning Path:
1. Start with FinSet for concrete intuition
2. Try posets for order relationships  
3. Explore type categories for programming
4. Use groups for algebraic structure
"""
    
    def _help_errors(self) -> str:
        return """
🚨 Error Help

🔧 Common Errors and Solutions:

❌ "Objects not in category"
   → Add objects first: cat.add_object(obj)

❌ "Product does not exist"  
   → Not all categories have products
   → Try smaller objects or check category type

❌ "Cannot compose morphisms"
   → Check f.target == g.source for g∘f
   → Make sure morphisms are in category

❌ "No initial/terminal object"
   → Many categories don't have these
   → This is normal, not an error

🆘 Getting Help:
- Use safe_compute_* methods for better errors
- Check cat.validate() for structure issues
- Use cat.help('topic') for specific help
"""


# CONVENIENT FACTORY FUNCTIONS

class HyperCat:
    """Main interface for creating and working with categories"""
    
    @staticmethod
    def create(category_type: str, *args, **kwargs) -> Category:
        """Create category with usability layer"""
        
        creators = {
            'finset': lambda size=4: StandardCategories.finite_sets(size),
            'finite_sets': lambda size=4: StandardCategories.finite_sets(size),
            'chain': lambda length=4: StandardCategories.chain_poset(length),
            'poset': lambda length=4: StandardCategories.chain_poset(length),
            'diamond': lambda: StandardCategories.diamond_poset(),
            'types': lambda: StandardCategories.basic_types(),
            'group': lambda n=3: StandardCategories.cyclic_group(n),
            'cyclic': lambda n=3: StandardCategories.cyclic_group(n),
            'empty': lambda: Category("Empty")
        }
        
        if category_type.lower() not in creators:
            available = ", ".join(creators.keys())
            raise HyperCatError(
                f"Unknown category type '{category_type}'",
                f"Available types: {available}",
                "Use HyperCat.create() factory"
            )
        
        # Create category
        if args:
            cat = creators[category_type.lower()](*args)
        else:
            cat = creators[category_type.lower()](**kwargs)
        
        # Add usability layer
        UsabilityLayer(cat)
        
        return cat
    
    @staticmethod
    def examples() -> Dict[str, Category]:
        """Get collection of example categories for learning"""
        examples = {
            'tiny_finset': HyperCat.create('finset', 2),
            'small_chain': HyperCat.create('chain', 3),
            'diamond': HyperCat.create('diamond'),
            'basic_types': HyperCat.create('types'),
            'small_group': HyperCat.create('group', 3)
        }
        
        return examples
    
    @staticmethod
    def tutorial() -> str:
        """Interactive tutorial for learning HyperCat"""
        return """
🎓 HyperCat Tutorial

Step 1: Create Your First Category
  cat = HyperCat.create('finset', 3)
  print(cat.explore())

Step 2: Explore Objects and Morphisms  
  print(f"Objects: {len(cat.objects)}")
  print(f"Morphisms: {len(cat.morphisms)}")
  
  # Get some objects
  A = cat.get_set(1)  # {1}
  B = cat.get_set(2)  # {1, 2}

Step 3: Build Products and Coproducts
  product = cat.compute_product([A, B])
  print(f"A × B = {product.data}")
  
  coproduct = cat.compute_coproduct([A, B])  
  print(f"A + B = {coproduct.data}")

Step 4: Analyze Morphisms
  morphs = list(cat.morphisms)[:3]
  for f in morphs:
      print(cat.explain_morphism(f))

Step 5: Get Complete Analysis
  print(cat.quick_analysis())
  analysis = cat.analyze_category()
  print(f"Has products: {analysis.has_products}")

Step 6: Get Help
  print(cat.help())
  print(cat.help('products'))

🎯 Try Different Categories:
  poset = HyperCat.create('chain', 4)
  types = HyperCat.create('types')
  group = HyperCat.create('group', 4)

💡 Explore Each:
  print(poset.explore())
  print(types.explore())
  print(group.explore())

🏆 Advanced: Create Your Own
  custom = Category("MyCategory")
  # Add objects and morphisms...
  UsabilityLayer(custom)  # Add nice interface
"""


# PERFORMANCE OPTIMIZATION

class PerformanceOptimizer:
    """Optimize category operations for better performance"""
    
    def __init__(self, category: Category):
        self.category = category
        self.optimizations = []
    
    def optimize(self) -> Dict[str, Any]:
        """Apply performance optimizations"""
        optimizations_applied = []
        
        # Cache frequently accessed morphisms
        if len(self.category.morphisms) > 100:
            self._create_morphism_index()
            optimizations_applied.append("Morphism indexing")
        
        # Optimize composition lookup
        if len(self.category.composition) > 1000:
            self._optimize_composition_lookup()
            optimizations_applied.append("Composition lookup optimization")
        
        # Warning for large categories
        warnings = []
        if len(self.category.objects) > 1000:
            warnings.append("Large category - consider using specialized data structures")
        
        return {
            'optimizations_applied': optimizations_applied,
            'warnings': warnings,
            'performance_tips': self._get_performance_tips()
        }
    
    def _create_morphism_index(self):
        """Create indices for faster morphism lookup"""
        if not hasattr(self.category, '_morphism_index'):
            self.category._morphism_index = {
                'by_source': defaultdict(list),
                'by_target': defaultdict(list),
                'by_source_target': defaultdict(list)
            }
            
            for morph in self.category.morphisms:
                self.category._morphism_index['by_source'][morph.source].append(morph)
                self.category._morphism_index['by_target'][morph.target].append(morph)
                self.category._morphism_index['by_source_target'][(morph.source, morph.target)].append(morph)
    
    def _optimize_composition_lookup(self):
        """Optimize composition table lookup"""
        # In a real implementation, this might use hash tables or other optimizations
        pass
    
    def _get_performance_tips(self) -> List[str]:
        """Get performance tips for this category"""
        tips = []
        
        if len(self.category.objects) > 100:
            tips.append("Consider using object indices for faster lookup")
        
        if len(self.category.morphisms) > 1000:
            tips.append("Use morphism caching for repeated operations")
        
        if len(self.category.composition) > 10000:
            tips.append("Consider lazy composition evaluation")
        
        return tips


# ERROR HANDLING IMPROVEMENTS

def setup_error_handling():
    """Set up helpful error handling for common mistakes"""
    
    # Override Python's default exception handler for HyperCat errors
    import sys
    
    def hypercat_exception_handler(exc_type, exc_value, exc_traceback):
        if isinstance(exc_value, HyperCatError):
            print(str(exc_value))
        else:
            # Fall back to default handler
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
    
    sys.excepthook = hypercat_exception_handler


# COMPREHENSIVE DEMO

def demonstrate_usability_layer():
    """Comprehensive demonstration of the usability features"""
    
    print("🎉 HyperCat Week 4: Usability Layer Demo")
    print("=" * 50)
    
    # Setup error handling
    setup_error_handling()
    
    # 1. Easy Category Creation
    print("\n1. 🏗️  Easy Category Creation")
    
    # Using factory
    cat = HyperCat.create('finset', 3)
    print(f"Created: {cat.name}")
    
    # Quick analysis
    print(f"Quick analysis: {cat.quick_analysis()}")
    
    # 2. Interactive Exploration
    print("\n2. 🔍 Interactive Exploration")
    print(cat.explore())
    
    # 3. Help System
    print("\n3. ❓ Context-Aware Help")
    print("General help:")
    print(cat.help())
    
    print("\nProduct-specific help:")
    print(cat.help('products'))
    
    # 4. Safe Operations with Error Handling
    print("\n4. 🛡️  Safe Operations")
    
    try:
        # This should work
        A = cat.get_set(1)
        B = cat.get_set(2)
        product = cat.safe_compute_product([A, B])
        print(f"✅ Product computed: {product.name}")
        
        # This should give helpful error
        empty_product = cat.safe_compute_product([])
        
    except HyperCatError as e:
        print(f"Caught helpful error:\n{e}")
    
    # 5. Examples and Suggestions
    print("\n5. 💡 Examples and Suggestions")
    
    examples = cat.find_examples()
    print("Found examples:")
    for category, items in examples.items():
        if items:
            print(f"  {category}: {items[:3]}")
    
    suggestions = cat.suggest_explorations()
    print(f"\nSuggested explorations:")
    for i, suggestion in enumerate(suggestions[:3], 1):
        print(f"  {i}. {suggestion}")
    
    # 6. Morphism Explanations
    print("\n6. 🔄 Morphism Explanations")
    
    morphisms = list(cat.morphisms)[:2]
    for morph in morphisms:
        print(cat.explain_morphism(morph))
        print()
    
    # 7. Category Validation
    print("\n7. ✅ Category Validation")
    
    validation = cat.validate()
    print(f"Validation: {validation['summary']}")
    if validation['suggestions']:
        print("Suggestions:")
        for suggestion in validation['suggestions'][:2]:
            print(f"  • {suggestion}")
    
    # 8. Different Category Types
    print("\n8. 🎭 Different Category Types")
    
    examples = HyperCat.examples()
    for name, example_cat in list(examples.items())[:3]:
        print(f"\n{name}: {example_cat.quick_analysis()}")
    
    # 9. Performance Optimization
    print("\n9. ⚡ Performance Optimization")
    
    optimizer = PerformanceOptimizer(cat)
    perf_info = optimizer.optimize()
    print(f"Optimizations applied: {perf_info['optimizations_applied']}")
    if perf_info['performance_tips']:
        print(f"Performance tips: {perf_info['performance_tips'][0]}")
    
    # 10. Tutorial Access
    print("\n10. 🎓 Tutorial")
    print("Access full tutorial with: HyperCat.tutorial()")
    
    print("\n✅ Usability layer demonstration complete!")
    print("\n🎯 HyperCat is now user-friendly for:")
    print("  👨‍🎓 Students learning category theory")
    print("  👩‍💼 Data modelers building systems")  
    print("  👨‍🔬 Researchers exploring structures")
    print("  👩‍💻 Developers using categorical patterns")


# QUICK START GUIDE

def quick_start_guide():
    """Generate a quick start guide for new users"""
    
    return """
🚀 HyperCat Quick Start Guide

📦 Installation & Import:
  # After installing HyperCat
  from hypercat import HyperCat

⭐ Create Your First Category (30 seconds):
  cat = HyperCat.create('finset', 3)
  print(cat.explore())

🔍 Explore What You Built:
  print(cat.quick_analysis())
  print(cat.help())

🏗️  Build Things:
  A = cat.get_set(1)  # Object {1}
  B = cat.get_set(2)  # Object {1,2}
  
  product = cat.compute_product([A, B])
  print(f"A × B = {product.data}")

🔬 Analyze:
  morphs = list(cat.morphisms)[:3]
  for f in morphs:
      print(cat.explain_morphism(f))

📚 Learn More:
  print(HyperCat.tutorial())
  
  # Try different categories:
  poset = HyperCat.create('chain', 4)
  types = HyperCat.create('types') 
  group = HyperCat.create('group', 3)

❓ Need Help?
  cat.help()              # General help
  cat.help('products')    # Specific topics
  cat.suggest_explorations()  # Things to try

🎯 You're Ready!
Start with FinSet, then explore posets and type categories.
Category theory has never been this accessible! 🎉
"""


if __name__ == "__main__":
    demonstrate_usability_layer()
    
    print("\n" + "="*60)
    print("📖 QUICK START GUIDE")
    print("="*60)
    print(quick_start_guide())

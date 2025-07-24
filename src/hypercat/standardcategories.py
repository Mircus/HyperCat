class StandardCategories:
    """Factory for creating standard categories."""
    
    @staticmethod
    def terminal_category() -> Category:
        """Create the terminal category 1 (one object, one morphism)."""
        cat = Category("1")
        obj = Object("*")
        cat.add_object(obj)
    @staticmethod
    def monoidal_category(unit_obj_name: str = "I") -> Category:
        """Create a basic monoidal category structure."""
        cat = Category("Monoidal")
        unit = Object(unit_obj_name)
        cat.add_object(unit)
        return cat
    
    @staticmethod
    def pushout_category() -> Category:
        """Create the pushout category (span category)."""
        cat = Category("Pushout")
        
        # Objects: •←•→•
        A = Object("A")
        B = Object("B")  
        C = Object("C")
        cat.add_object(A).add_object(B).add_object(C)
        
        # Morphisms
        f = Morphism("f", A, B)
        g = Morphism("g", A, C)
        cat.add_morphism(f).add_morphism(g)
        
        return cat
    
    @staticmethod
    def pullback_category() -> Category:
        """Create the pullback category (cospan category)."""
        cat = Category("Pullback")
        
        # Objects: •→•←•
        A = Object("A")
        B = Object("B")
        C = Object("C")
        cat.add_object(A).add_object(B).add_object(C)
        
        # Morphisms
        f = Morphism("f", A, C)
        g = Morphism("g", B, C)
        cat.add_morphism(f).add_morphism(g)
        
        return cat
    
    @staticmethod
    def slice_category(base_category: Category, base_object: Object) -> Category:
        """Create the slice category C/X."""
        slice_cat = Category(f"{base_category.name}/{base_object.name}")
        
        # Objects are morphisms f: A -> X
        for morph in base_category.morphisms:
            if morph.target == base_object:
                slice_obj = Object(f"{morph.source.name}→{base_object.name}", morph)
                slice_cat.add_object(slice_obj)
        
        return slice_cat
    
    @staticmethod
    def coslice_category(base_category: Category, base_object: Object) -> Category:
        """Create the coslice category X/C."""
        coslice_cat = Category(f"{base_object.name}/{base_category.name}")
        
        # Objects are morphisms f: X -> A
        for morph in base_category.morphisms:
            if morph.source == base_object:
                coslice_obj = Object(f"{base_object.name}→{morph.target.name}", morph)
                coslice_cat.add_object(coslice_obj)
        
        return coslice_cat
    
    @staticmethod
    def empty_category() -> Category:
        """Create the empty category 0."""
        return Category("0")
    
    @staticmethod
    def discrete_category(objects: List[str]) -> Category:
        """Create a discrete category (only identity morphisms)."""
        cat = Category(f"Discrete({len(objects)})")
        for obj_name in objects:
            obj = Object(obj_name)
            cat.add_object(obj)
        return cat
    
    @staticmethod
    def simplex_category(n: int) -> Category:
        """Create the simplex category Δ^n."""
        cat = Category(f"Δ^{n}")
        
        # Objects are ordered sets [0], [0,1], [0,1,2], ..., [0,1,...,n]
        objects = []
        for i in range(n + 1):
            obj = Object(f"[{','.join(map(str, range(i+1)))}]")
            objects.append(obj)
            cat.add_object(obj)
        
        # Morphisms are order-preserving maps
        for i in range(n):
            for j in range(i + 1, n + 1):
                # Face maps (deletions)
                for k in range(i + 1):
                    face_name = f"d_{k}^{i}"
                    face_morph = Morphism(face_name, objects[j], objects[i])
                    cat.add_morphism(face_morph)
                
                # Degeneracy maps (insertions)
                for k in range(i + 1):
                    deg_name = f"s_{k}^{i}"
                    deg_morph = Morphism(deg_name, objects[i], objects[j])
                    cat.add_morphism(deg_morph)
        
        return cat
    
    @staticmethod
    def arrow_category() -> Category:
        """Create the arrow category 2 (two objects, one non-identity arrow)."""
        cat = Category("2")
        obj0 = Object("0")
        obj1 = Object("1")
        cat.add_object(obj0)
        cat.add_object(obj1)
        
        arrow = Morphism("f", obj0, obj1)
        cat.add_morphism(arrow)
        
        return cat
    
    @staticmethod
    def walking_isomorphism() -> Category:
        """Create the walking isomorphism category."""
        cat = Category("Walking_Iso")
        obj0 = Object("0")
        obj1 = Object("1")
        cat.add_object(obj0)
        cat.add_object(obj1)
        
        f = Morphism("f", obj0, obj1)
        f_inv = Morphism("f⁻¹", obj1, obj0)
        cat.add_morphism(f)
        cat.add_morphism(f_inv)
        
        # Set up composition to make f and f_inv inverses
        cat.set_composition(f, f_inv, cat.identities[obj0])
        cat.set_composition(f_inv, f, cat.identities[obj1])
        
        return cat


# Example usage and comprehensive tests
def example_usage():
    """Demonstrate the extended library with comprehensive examples."""
    print("=== Extended Category Theory Library Demo ===\n")
    
    # 1. Basic category construction with builder
    print("1. Category Construction with Builder:")
    builder = CategoryBuilder("TestCat")
    cat = (builder
           .with_objects("A", "B", "C")
           .with_morphisms_between_all("f")
           .with_free_composition()
           .build())
    
    print(f"Built category with {len(cat.objects)} objects and {len(cat.morphisms)} morphisms")
    print(f"Valid category: {cat.is_valid()}")
    
    # 2. Object and morphism construction
    print("\n2. Advanced Object Construction:")
    A = Object("A")
    B = Object("B")
    tensor_AB = ObjectConstructor.tensor_product(A, B)
    exp_BA = ObjectConstructor.exponential_object(A, B)
    susp_A = ObjectConstructor.suspension(A)
    
    print(f"A ⊗ B = {tensor_AB}")
    print(f"B^A = {exp_BA}")
    print(f"ΣA = {susp_A}")
    
    # 3. Functor categories
    print("\n3. Functor Categories:")
    arrow_cat = StandardCategories.arrow_category()
    terminal_cat = StandardCategories.terminal_category()
    
    # Create a simple functor
    F = Functor("F", arrow_cat, terminal_cat)
    for obj in arrow_cat.objects:
        terminal_obj = next(iter(terminal_cat.objects))
        F.map_object(obj, terminal_obj)
    
    # Create functor category
    functor_cat = FunctorCategory(arrow_cat, terminal_cat)
    functor_cat.add_functor_object(F)
    
    print(f"Functor category [{arrow_cat.name},{terminal_cat.name}] created")
    print(f"Objects (functors): {len(functor_cat.objects)}")
    
    # 4. Limits and colimits
    print("\n4. Limits and Colimits:")
    # Create a simple diagram
    diagram = {A: A, B: B}
    apex = Object("Limit")
    proj_A = Morphism("π_A", apex, A)
    proj_B = Morphism("π_B", apex, B)
    projections = {A: proj_A, B: proj_B}
    
    cone = Cone(apex, diagram, projections)
    limit = Limit(cone)
    print(f"Created limit with apex {limit.limit_object}")
    
    # 5. Adjunctions
    print("\n5. Adjunctions:")
    # Create categories for adjunction
    C = Category("C")
    D = Category("D")
    
    x = Object("x")
    y = Object("y")
    C.add_object(x)
    D.add_object(y)
    
    # Create adjoint functors
    left_adj = Functor("L", C, D)
    right_adj = Functor("R", D, C)
    left_adj.map_object(x, y)
    right_adj.map_object(y, x)
    
    try:
        adjunction = Adjunction(left_adj, right_adj)
        print(f"Created adjunction L ⊣ R between {C.name} and {D.name}")
    except ValueError as e:
        print(f"Adjunction creation note: {e}")
    
    # 6. Higher categories
    print("\n6. Higher Categories:")
    two_cat = TwoCategory("2Cat")
    obj1 = Object("X")
    obj2 = Object("Y")
    two_cat.add_object(obj1).add_object(obj2)
    
    f = Morphism("f", obj1, obj2)
    g = Morphism("g", obj1, obj2)
    two_cat.add_morphism(f).add_morphism(g)
    
    alpha = TwoCell("α", f, g)
    two_cat.add_two_cell(alpha)
    
    print(f"Created 2-category with 2-cell: {alpha}")
    
    # 7. Monoidal categories
    print("\n7. Monoidal Categories:")
    monoidal = MonoidalCategory("Mon")
    unit = Object("I")
    monoidal.set_unit_object(unit)
    monoidal.set_tensor_product(ObjectConstructor.tensor_product)
    
    a_obj = Object("a")
    b_obj = Object("b")
    monoidal.add_object(a_obj).add_object(b_obj).add_object(unit)
    
    tensor_result = monoidal.tensor_objects(a_obj, b_obj)
    print(f"Tensor product: a ⊗ b = {tensor_result}")
    
    # 8. Toposes
    print("\n8. Topos Theory:")
    topos = Topos("Set")
    terminal = Object("1")
    omega = Object("Ω")
    true_morph = Morphism("true", terminal, omega)
    
    topos.set_terminal_object(terminal)
    topos.set_subobject_classifier(omega, true_morph)
    
    print(f"Created topos with terminal object {terminal} and classifier {omega}")
    print(f"Has finite limits: {topos.has_finite_limits()}")
    
    # 9. Groupoids
    print("\n9. Groupoids:")
    groupoid = Groupoid("Π₁(S¹)")
    base = Object("*")
    groupoid.add_object(base)
    
    loop = Morphism("γ", base, base)
    groupoid.add_morphism(loop)
    
    print(f"Created groupoid with loop: {loop}")
    print(f"Morphisms (including inverses): {len(groupoid.morphisms)}")
    
    # 10. Slice categories
    print("\n10. Slice Categories:")
    base_cat = StandardCategories.arrow_category()
    base_obj = next(iter(base_cat.objects))
    slice_cat = StandardCategories.slice_category(base_cat, base_obj)
    
    print(f"Created slice category {slice_cat.name}")
    print(f"Objects: {len(slice_cat.objects)}")
    
    # 11. Opposite categories
    print("\n11. Opposite Categories:")
    original = StandardCategories.arrow_category()
    opposite = original.opposite()
    
    print(f"Original: {original.name}, Opposite: {opposite.name}")
    print(f"Original morphisms: {len(original.morphisms)}")
    print(f"Opposite morphisms: {len(opposite.morphisms)}")
    
    # 12. Operads and algebras
    print("\n12. Operads and Algebras:")
    operad = Operad("Assoc")
    binary_op = "μ"
    operad.add_operation(2, binary_op)
    operad.set_unit("e")
    
    monoid_obj = Object("M")
    algebra = Algebra("Monoid", operad, monoid_obj)
    mult_map = Morphism("mult", 
                       ObjectConstructor.product(monoid_obj, monoid_obj), 
                       monoid_obj)
    algebra.set_structure_map(binary_op, mult_map)
    
    print(f"Created operad {operad.name} and algebra {algebra.name}")
    
    print("\n=== Extended Demo Complete ===")


def run_comprehensive_tests():
    """Run comprehensive tests of the library."""
    print("\n=== Running Comprehensive Tests ===")
    
    # Test category validity
    print("\n1. Testing Category Axioms:")
    cat = (CategoryBuilder("Test")
           .with_objects("A", "B", "C")
           .with_morphisms_between_all()
           .build())
    print(f"Category validity: {cat.is_valid()}")
    
    # Test functor composition
    print("\n2. Testing Functor Composition:")
    cat1 = StandardCategories.terminal_category()
    cat2 = StandardCategories.arrow_category() 
    cat3 = StandardCategories.discrete_category(["x", "y", "z"])
    
    F = Functor("F", cat1, cat2)
    G = Functor("G", cat2, cat3)
    
    # Set up functor mappings (simplified)
    try:
        comp = F.compose_with(G)
        print(f"Functor composition: {comp.name}")
    except ValueError as e:
        print(f"Composition test: {e}")
    
    # Test natural transformations
    print("\n3. Testing Natural Transformations:")
    id_functor = Functor("Id", cat2, cat2)
    for obj in cat2.objects:
        id_functor.map_object(obj, obj)
    for morph in cat2.morphisms:
        id_functor.map_morphism(morph, morph)
    
    print("Created identity functor for naturality testing")
    
    print("\n=== Tests Complete ===")


if __name__ == "__main__":
    example_usage()
    run_comprehensive_tests()

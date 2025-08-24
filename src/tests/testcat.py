from hypercat import Category, Object, Morphism

def test_identity_morphism():
    """Test that identity morphisms are created automatically."""
    C = Category("C")
    A = Object("A")
    C.add_object(A)
    
    # Check that identity morphism exists
    id_morphisms = [m for m in C.morphisms if m.source == A and m.target == A and m.name.startswith("id_")]
    assert len(id_morphisms) == 1
    id_A = id_morphisms[0]
    assert id_A.source == A and id_A.target == A

def test_composition():
    """Test morphism composition."""
    C = Category("C")
    A = Object("A")
    B = Object("B")
    C_obj = Object("C")
    
    C.add_object(A)
    C.add_object(B)
    C.add_object(C_obj)
    
    f = Morphism("f", A, B)
    g = Morphism("g", B, C_obj)
    C.add_morphism(f)
    C.add_morphism(g)
    
    # Define the composition
    h = Morphism("g∘f", A, C_obj)
    C.add_morphism(h)
    C.set_composition(f, g, h)
    
    # Now test that compose returns the defined composition
    composed = C.compose(f, g)
    assert composed is not None
    assert composed.source == A
    assert composed.target == C_obj
    assert composed == h

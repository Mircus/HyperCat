def test_identity_morphism():
    C = Category("C")
    A = C.add_object("A")
    id_A = C.get_identity("A")
    assert id_A.domain == A and id_A.codomain == A

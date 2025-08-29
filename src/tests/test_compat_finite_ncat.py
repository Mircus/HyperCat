
from hypercat.higher.finite.ncat import FiniteWeakNCategory
from hypercat.higher.finite.computad import Generator, Relation as NRel

def test_finite_ncat_certificate():
    C = FiniteWeakNCategory(n=2)
    a = C.add_generator(Generator(1, "a", 0, 1))
    b = C.add_generator(Generator(1, "b", 1, 2))
    C.add_relation(NRel(1, (a,b), (b,a), "swap"))
    lhs = (a,b,a)
    rhs = (b,a,a)
    cert = C.certificate(1, lhs, rhs, budget=64)
    assert cert, "expected non-empty certificate"

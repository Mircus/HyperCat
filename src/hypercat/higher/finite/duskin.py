
"""Duskin-like nerve (n=2 demo) that works with your existing TwoCategory.
- Uses hypercat.core.core.Morphism and Category types implicitly via TwoCategory.
"""
from hypercat.higher.twocategory import TwoCell  # keep class available
from hypercat.higher.twocategory import Category as _CompatCategory  # type alias if exposed (fallback)
from hypercat.higher.twocategory import TwoCategory  # existing API
from .nsset import FiniteTruncatedSSet

def nerve2_from_two_category(B: TwoCategory) -> FiniteTruncatedSSet:
    S = FiniteTruncatedSSet(n=2)
    # 0-simplices: objects
    obj_idx = {A: S.add_simplex(0, A) for A in B.objects}
    # 1-simplices: 1-cells (morphisms of underlying Category)
    one_idx = {}
    for f in B.category.morphisms:
        i = S.add_simplex(1, f)
        one_idx[f] = i
        S.set_face(1, 0, i, obj_idx[f.target])  # d0=tgt
        S.set_face(1, 1, i, obj_idx[f.source])  # d1=src
    # 2-simplices: 2-cells
    for a in B.two_cells:
        j = S.add_simplex(2, a)
        S.set_face(2, 0, j, one_idx[a.target])
        S.set_face(2, 1, j, one_idx[a.source])
    return S

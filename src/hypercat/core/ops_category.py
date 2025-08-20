from __future__ import annotations

from types import MappingProxyType
from typing import Dict

from .category import Cat


def opposite_category(C: Cat) -> Cat:
    # create op arrow names by suffixing ^op and swapping endpoints
    op_arrows = tuple(
        (f"{a.name}^op", a.target, a.source) for a in C.arrows
    )
    # mapping original name -> op name
    to_op: Dict[str, str] = {a.name: f"{a.name}^op" for a in C.arrows}
    # composition: (g^op, f^op) = (f∘g)^op in C^op
    comp = MappingProxyType({
        (to_op[g], to_op[f]): to_op[gf] for (g, f), gf in C.composition.items()
    })
    ids = MappingProxyType({o.name: to_op[C.identities[o.name]] for o in C.objects})
    # rebuild ArrowGen list with swapped endpoints
    arrows = tuple(
        type(C.arrows[0])(to_op[a.name], a.target, a.source) for a in C.arrows
    )
    return Cat(objects=C.objects, arrows=arrows, composition=comp, identities=ids)



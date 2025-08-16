from __future__ import annotations

from types import MappingProxyType
from typing import Dict, Set, Tuple

from .presentation import Obj, ArrowGen
from .category import Cat


def terminal_category(name: str = "Terminal") -> Cat:
    obj = Obj("*")
    id_name = "id:*"
    arrows = (ArrowGen(id_name, obj.name, obj.name),)
    composition = MappingProxyType({(id_name, id_name): id_name})
    identities = MappingProxyType({obj.name: id_name})
    return Cat(objects=(obj,), arrows=arrows, composition=composition, identities=identities)


def discrete(objects: list[str], name: str = "Discrete") -> Cat:
    objs = tuple(Obj(o) for o in objects)
    ids: Dict[str, str] = {o.name: f"id:{o.name}" for o in objs}
    arrows = tuple(ArrowGen(ids[o.name], o.name, o.name) for o in objs)
    composition = MappingProxyType({(i, i): i for i in ids.values()})
    identities = MappingProxyType(ids)
    return Cat(objects=objs, arrows=arrows, composition=composition, identities=identities)


def simplex(n: int, name: str | None = None) -> Cat:
    # Δ^n with objects 0..n and unique i->j for i<=j
    objs = tuple(Obj(str(i)) for i in range(n + 1))
    ids: Dict[str, str] = {o.name: f"id:{o.name}" for o in objs}
    arr: Dict[Tuple[int, int], str] = {}
    morph_names: Set[str] = set()
    # identities
    for i, o in enumerate(objs):
        arr[(i, i)] = ids[o.name]
        morph_names.add(ids[o.name])
    # generating arrows i->j when i<j
    for i in range(n + 1):
        for j in range(i + 1, n + 1):
            name_ij = f"{i}->{j}"
            arr[(i, j)] = name_ij
            morph_names.add(name_ij)
    arrows = tuple(ArrowGen(arr[(i, j)], str(i), str(j)) for i in range(n + 1) for j in range(i, n + 1))
    # composition (g,f) where g: j->k, f: i->j yields i->k
    composition = MappingProxyType({
        (arr[(j, k)], arr[(i, j)]): arr[(i, k)]
        for i in range(n + 1) for j in range(i, n + 1) for k in range(j, n + 1)
    })
    identities = MappingProxyType(ids)
    return Cat(objects=objs, arrows=arrows, composition=composition, identities=identities)


def walking_isomorphism(name: str = "Iso") -> Cat:
    A, B = Obj("A"), Obj("B")
    idA, idB = "id:A", "id:B"
    f, g = "f", "g"
    arrows = (
        ArrowGen(idA, A.name, A.name),
        ArrowGen(idB, B.name, B.name),
        ArrowGen(f, A.name, B.name),
        ArrowGen(g, B.name, A.name),
    )
    composition = MappingProxyType({
        (idA, idA): idA,
        (idB, idB): idB,
        (f, idA): f,
        (idB, f): f,
        (g, idB): g,
        (idA, g): g,
        (g, f): idA,
        (f, g): idB,
    })
    identities = MappingProxyType({A.name: idA, B.name: idB})
    return Cat(objects=(A, B), arrows=arrows, composition=composition, identities=identities)



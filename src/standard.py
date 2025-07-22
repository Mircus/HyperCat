
from typing import List
from .core import Object, Morphism
from .category import Category

class StandardCategories:
    @staticmethod
    def terminal_category() -> Category:
        cat = Category("1")
        obj = Object("*")
        cat.add_object(obj)
        return cat

    @staticmethod
    def empty_category() -> Category:
        return Category("0")

    @staticmethod
    def discrete_category(objects: List[str]) -> Category:
        cat = Category("Discrete")
        for obj_name in objects:
            cat.add_object(Object(obj_name))
        return cat

    @staticmethod
    def arrow_category() -> Category:
        cat = Category("2")
        obj0 = Object("0")
        obj1 = Object("1")
        cat.add_object(obj0).add_object(obj1)
        cat.add_morphism(Morphism("f", obj0, obj1))
        return cat

    @staticmethod
    def walking_isomorphism() -> Category:
        cat = Category("Iso")
        obj0 = Object("0")
        obj1 = Object("1")
        cat.add_object(obj0).add_object(obj1)
        f = Morphism("f", obj0, obj1)
        f_inv = Morphism("f⁻¹", obj1, obj0)
        cat.add_morphism(f).add_morphism(f_inv)
        cat.set_composition(f, f_inv, cat.identities[obj0])
        cat.set_composition(f_inv, f, cat.identities[obj1])
        return cat

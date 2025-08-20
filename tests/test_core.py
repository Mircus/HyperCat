from hypercat.core.presentation import Obj, ArrowGen, Presentation, Formal1
from hypercat.core.builder import obj, arrow, build_presentation
from hypercat.core.functor import Functor, apply_functor
from hypercat.core.ops import compose, identity


def test_build_presentation_adds_identities():
	A = obj("A"); B = obj("B")
	f = arrow("f","A","B")
	p = build_presentation((A,B),(f,))
	assert any(g.name == "id:A" for g in p.arrows)
	assert any(g.name == "id:B" for g in p.arrows)


def test_functor_maps_formal_path():
	F = Functor("F", {"A":"A","B":"B"}, {"f":"f"})
	path = compose(Formal1(("f",)),)
	assert apply_functor(F, path).factors == ("f",)


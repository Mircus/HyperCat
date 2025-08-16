from .presentation import Obj, ArrowGen, Formal1, Presentation
from .category import Cat
from .builder import obj, arrow, build_presentation
from .ops import compose, identity, normalize
from .functor import Functor, apply_functor
from .convert import to_dict, from_dict
from .laws import Law, LawSuite, run_suite
from .laws_category import CATEGORY_SUITE

__all__ = [
	"Obj",
	"ArrowGen",
	"Formal1",
	"Presentation",
	"Cat",
	"obj",
	"arrow",
	"build_presentation",
	"compose",
	"identity",
	"normalize",
	"Functor",
	"apply_functor",
	"to_dict",
	"from_dict",
	"Law",
	"LawSuite",
	"run_suite",
	"CATEGORY_SUITE",
]


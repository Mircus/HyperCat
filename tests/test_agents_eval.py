from hypercat.agents.actions import seq
from hypercat.agents.eval import run_plan, choose_best, quick_functor_laws


def test_run_and_choose_best():
	impl = {
		'denoise': lambda s, ctx=None: s.replace('~',''),
		'edges': lambda s, ctx=None: ''.join(ch for ch in s if ch.isalpha()),
		'segment': lambda s, ctx=None: s.upper(),
		'merge': lambda s, ctx=None: f"[{s}]",
	}
	plan1 = seq('denoise','edges','segment','merge')
	plan2 = seq('denoise','segment','merge')

	report1 = run_plan(plan1, impl, "~a~b_c-1", evaluator=lambda o: -len(o))
	assert report1.output == "[ABC]" and report1.score == -5

	best_plan, best_report = choose_best([plan1, plan2], impl, "~a~b_c-1", evaluator=lambda o: -len(o))
	assert best_plan.factors == plan1.factors and best_report.output == "[ABC]"


def test_quick_functor_laws():
	impl = {
		'f': lambda x, ctx=None: x + 1,
		'g': lambda x, ctx=None: x * 2,
		'id': lambda x, ctx=None: x,
	}
	quick_functor_laws(impl, id_name='id', samples=[0,1,2])


from hypercat.agents.actions import seq
from hypercat.agents.runtime import strong_monoidal_functor


def test_agent_pipeline_runs():
	skills = {
		'denoise': lambda s: s.replace('~',''),
		'edges': lambda s: ''.join(ch for ch in s if ch.isalpha()),
		'segment': lambda s: s.upper(),
		'merge': lambda s: f"[{s}]",
	}
	plan = seq('denoise','edges','segment','merge')
	F = strong_monoidal_functor(skills)
	assert F(plan)("~a~b_c-1") == "[ABC]"


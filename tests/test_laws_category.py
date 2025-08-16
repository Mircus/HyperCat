from hypercat.core import obj, arrow, build_presentation, Cat, run_suite, CATEGORY_SUITE


def test_category_laws_trivial_ok():
	A = obj("A")
	p = build_presentation((A,), ())
	C = Cat.from_presentation(p)
	report = run_suite(C, CATEGORY_SUITE)
	assert report.ok, report.to_text()


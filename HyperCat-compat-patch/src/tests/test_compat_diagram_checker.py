
from hypercat.diagram.commutativity_checker import Diagram, Relation, CommutativityChecker

def test_subpath_certificate():
    rels = [Relation(("a","b"), ("b","a"), "swap")]
    ok, cert = CommutativityChecker(rels).check(Diagram(("x","a","b","y"), ("x","b","a","y")))
    assert ok and cert.steps and cert.steps[0][1] == 1

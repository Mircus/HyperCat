from __future__ import annotations

from typing import Dict, Any

from .presentation import Obj, ArrowGen, Formal1, Presentation


def to_dict(p: Presentation) -> Dict[str, Any]:
	return {
		"objects": [{"name": o.name, "data": o.data} for o in p.objects],
		"arrows": [
			{"name": a.name, "source": a.source, "target": a.target} for a in p.arrows
		],
		"relations": [
			{"lhs": list(lhs.factors), "rhs": list(rhs.factors)} for lhs, rhs in p.relations
		],
	}


def from_dict(d: Dict[str, Any]) -> Presentation:
	objects = tuple(Obj(x["name"], x.get("data")) for x in d["objects"])
	arrows = tuple(ArrowGen(x["name"], x["source"], x["target"]) for x in d["arrows"])
	relations = tuple(
		(Formal1(tuple(rel["lhs"])), Formal1(tuple(rel["rhs"])) )
		for rel in d.get("relations", [])
	)
	return Presentation(objects, arrows, relations)


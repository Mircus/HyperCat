from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Tuple

from .category import Cat
from .functor import CatFunctor
from .natural import Natural


@dataclass(frozen=True)
class AxReport:
	ok: bool
	detail: str = ""


def _find_arrow(C: Cat, name: str):
	for a in C.arrows:
		if a.name == name:
			return a
	raise KeyError(f"arrow not found: {name}")


def _hom(C: Cat, src: str, tgt: str) -> List[str]:
	return [a.name for a in C.arrows if a.source == src and a.target == tgt]


def check_category_axioms(C: Cat, sample_limit: int = 0) -> AxReport:
	# identities: for all f: X→Y, id_X and id_Y exist and act as units in composition table
	for a in C.arrows:
		id_src = C.identities.get(a.source)
		id_tgt = C.identities.get(a.target)
		if id_src is None or id_tgt is None:
			return AxReport(False, f"missing identity for object of morphism {a.name}")
		# right unit: (f, id_X) = f
		if (a.name, id_src) in C.composition and C.composition[(a.name, id_src)] != a.name:
			return AxReport(False, f"f∘id_src ≠ f on {a.name}")
		# left unit: (id_Y, f) = f
		if (id_tgt, a.name) in C.composition and C.composition[(id_tgt, a.name)] != a.name:
			return AxReport(False, f"id_tgt∘f ≠ f on {a.name}")

	# associativity on available triples in composition table
	pairs = list(C.composition.keys())
	count = 0
	for (g, f) in pairs:
		for (h, g2) in pairs:
			if g2 != g:
				continue
			if sample_limit and count >= sample_limit:
				return AxReport(True, "associativity sampled")
			count += 1
			left_key = (h, C.composition[(g, f)])
			right_key = (C.composition[(h, g)], f)
			if left_key in C.composition and right_key in C.composition:
				if C.composition[left_key] != C.composition[right_key]:
					return AxReport(False, f"assoc fails on (h,g,f)=({h},{g},{f})")
	return AxReport(True, "category axioms OK")


def check_functor_axioms(F: CatFunctor) -> AxReport:
	S, T = F.source, F.target
	# identities
	for obj_name, id_src in S.identities.items():
		FX = F.object_map.get(obj_name)
		if FX is None:
			return AxReport(False, f"missing object map for {obj_name}")
		if F.morphism_map.get(id_src) != T.identities.get(FX):
			return AxReport(False, f"F(id_{obj_name})≠id_{FX}")
	# composition
	for (g, f), gf in S.composition.items():
		mg = F.morphism_map.get(g)
		mf = F.morphism_map.get(f)
		mgf = F.morphism_map.get(gf)
		if mg is None or mf is None or mgf is None:
			return AxReport(False, f"F undefined on some morphism (g={g}, f={f}, gf={gf})")
		if (mg, mf) not in T.composition or T.composition[(mg, mf)] != mgf:
			return AxReport(False, f"F(g∘f) ≠ F(g)∘F(f) on (g={g}, f={f})")
	return AxReport(True, "functor laws OK")


def check_naturality(eta: Natural) -> AxReport:
	F, G = eta.source, eta.target
	if not (F.source is G.source and F.target is G.target):
		return AxReport(False, "η typed against different (F,G)")
	S, T = F.source, F.target
	# For each arrow f: X→Y in S, check η_Y ∘ F(f) == G(f) ∘ η_X in T
	for a in S.arrows:
		f = a.name
		X = a.source
		Y = a.target
		eta_X = eta.components.get(X)
		eta_Y = eta.components.get(Y)
		Ff = F.morphism_map.get(f)
		Gf = G.morphism_map.get(f)
		if None in (eta_X, eta_Y, Ff, Gf):
			return AxReport(False, f"missing data for naturality on f={f}")
		left_key = (eta_Y, Ff)
		right_key = (Gf, eta_X)
		if left_key not in T.composition or right_key not in T.composition:
			return AxReport(False, f"composition missing in target for f={f}")
		if T.composition[left_key] != T.composition[right_key]:
			return AxReport(False, f"naturality fails on f={f}")
	return AxReport(True, "naturality OK")


def is_terminal_object(C: Cat, T_obj: str) -> AxReport:
	for o in C.objects:
		hom = _hom(C, o.name, T_obj)
		if len(hom) != 1:
			return AxReport(False, f"|Hom({o.name},{T_obj})|={len(hom)}≠1")
	return AxReport(True, "terminal object OK")


def is_product(C: Cat, X: str, Y: str, P: str, pi1: str, pi2: str) -> AxReport:
	# projection typing
	try:
		p1 = _find_arrow(C, pi1)
		p2 = _find_arrow(C, pi2)
	except KeyError as e:
		return AxReport(False, str(e))
	if not (p1.source == P and p1.target == X and p2.source == P and p2.target == Y):
		return AxReport(False, "bad projections typing")
	# universal property
	for Z in C.objects:
		f_candidates = _hom(C, Z.name, X)
		g_candidates = _hom(C, Z.name, Y)
		for f in f_candidates:
			for g in g_candidates:
				mediators = [h for h in _hom(C, Z.name, P)
					if (p1.name, h) in C.composition and C.composition[(p1.name, h)] == f
					and (p2.name, h) in C.composition and C.composition[(p2.name, h)] == g]
				if len(mediators) != 1:
					return AxReport(False, f"product not unique/existing for Z={Z.name}, (f,g)=({f},{g})")
	return AxReport(True, "product universal property OK")


def is_iso(C: Cat, f: str, g: str) -> AxReport:
	try:
		f_a = _find_arrow(C, f)
		g_a = _find_arrow(C, g)
	except KeyError as e:
		return AxReport(False, str(e))
	if not (f_a.source == g_a.target and f_a.target == g_a.source):
		return AxReport(False, "bad inverse types")
	if (g, f) not in C.composition or C.composition[(g, f)] != C.identities[f_a.source]:
		return AxReport(False, "g∘f≠id")
	if (f, g) not in C.composition or C.composition[(f, g)] != C.identities[f_a.target]:
		return AxReport(False, "f∘g≠id")
	return AxReport(True, "isomorphism OK")


def check_simplex_thin(C: Cat) -> AxReport:
	for A in C.objects:
		for B in C.objects:
			hom = _hom(C, A.name, B.name)
			if len(hom) > 1:
				return AxReport(False, f"not thin at Hom({A.name},{B.name})")
	return AxReport(True, "Δ^n thinness OK")


def certificate(label: str, *reports: AxReport) -> str:
	ok = all(r.ok for r in reports)
	lines = [f"[{label}] {'OK' if ok else 'FAIL'}"]
	for r in reports:
		lines.append(f" - {'OK' if r.ok else 'FAIL'}: {r.detail}")
	return "\n".join(lines)



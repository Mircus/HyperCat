from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence


def _fence(body: str) -> str:
    return "```mermaid\n" + body.strip() + "\n```"


# ---------------------- Category / Functor / Natural ----------------------

def _iter_arrows(category: Any) -> Iterable[Any]:
    # Support our core Cat (.arrows of ArrowGen) and any foreign shape with .morphisms
    if hasattr(category, "arrows"):
        return category.arrows
    if hasattr(category, "morphisms"):
        return category.morphisms
    return ()


def _obj_name(x: Any) -> str:
    return x.name if hasattr(x, "name") else str(x)


def _src_name(arrow: Any) -> str:
    s = getattr(arrow, "source", "")
    return _obj_name(s)


def _tgt_name(arrow: Any) -> str:
    t = getattr(arrow, "target", "")
    return _obj_name(t)


def _arr_name(arrow: Any) -> str:
    return _obj_name(getattr(arrow, "name", arrow))


def category_mermaid(C: Any, *, hide_id: bool = True) -> str:
    lines: List[str] = ["graph LR"]
    arrows = sorted(_iter_arrows(C), key=lambda a: _arr_name(a))
    for a in arrows:
        name = _arr_name(a)
        if hide_id and _src_name(a) == _tgt_name(a) and (name.startswith("id:") or name.startswith("id_")):
            continue
        lines.append(f'  {_src_name(a)} -- "{name}" --> {_tgt_name(a)}')
    return _fence("\n".join(lines))


def functor_mermaid(F: Any) -> str:
    S, T = F.source, F.target
    # Prefix node ids to avoid clashes across subgraphs
    def nid(prefix: str, name: str) -> str:
        return f"{prefix}_{name}"

    src = ["subgraph Source"]
    for a in sorted(_iter_arrows(S), key=lambda x: _arr_name(x)):
        src.append(f'  {nid("S", _src_name(a))} -- "{_arr_name(a)}" --> {nid("S", _tgt_name(a))}')
    src.append("end")

    tgt = ["subgraph Target"]
    for a in sorted(_iter_arrows(T), key=lambda x: _arr_name(x)):
        tgt.append(f'  {nid("T", _src_name(a))} -- "{_arr_name(a)}" --> {nid("T", _tgt_name(a))}')
    tgt.append("end")

    # Object map: Mapping[str,str] for CatFunctor
    links: List[str] = []
    if hasattr(F, "object_map") and isinstance(F.object_map, dict):
        for s_name, t_name in sorted(F.object_map.items(), key=lambda kv: kv[0]):
            links.append(f'  {nid("S", s_name)} -.-> {nid("T", t_name)}:::map')

    body = "\n".join(["graph LR", *src, *tgt, *links, "classDef map stroke-dasharray: 3 3;"])
    return _fence(body)


def naturality_mermaid(eta: Any, f: Any) -> str:
    # Expect 'f' as an arrow-like object with .source/.target names
    X = _src_name(f)
    Y = _tgt_name(f)
    # Avoid problematic punctuation in edge labels: use 'F·f' style
    body = f"""
graph LR
  FX["F {X}"] -->|F·{_arr_name(f)}| FY["F {Y}"]
  FX -->|η {X}| GX["G {X}"]
  FY -->|η {Y}| GY["G {Y}"]
  GX -->|G·{_arr_name(f)}| GY
""".strip()
    return _fence(body)


# ------------------------------ Agents visuals ------------------------------

def plan_mermaid(plan: Any) -> str:
    factors: Sequence[str] = getattr(plan, "factors", ())
    nodes = ["in"] + [f"s{i}" for i in range(1, len(factors) + 1)] + ["out"]
    labels = ["⟦input⟧"] + list(factors) + ["⟦output⟧"]
    lines = ["graph LR"]
    for n, l in zip(nodes, labels):
        lines.append(f'  {n}["{l}"]')
    for i in range(len(nodes) - 1):
        lines.append(f"  {nodes[i]} --> {nodes[i+1]}")
    return _fence("\n".join(lines))


def exec_gantt_mermaid(report_or_trace: Any) -> str:
    # Accept RunReport with .trace (sequence of StepTrace with duration_ms), or a custom trace with .steps
    steps = None
    if hasattr(report_or_trace, "trace"):
        steps = getattr(report_or_trace, "trace")
    elif hasattr(report_or_trace, "steps"):
        steps = getattr(report_or_trace, "steps")
    else:
        return _fence("gantt\n  dateFormat X\n  axisFormat %L\n  %% (no steps)")
    durations = [getattr(s, "duration_ms", None) for s in steps]
    if any(d is None for d in durations):
        return _fence("gantt\n  dateFormat X\n  axisFormat %L\n  %% (missing durations)")
    # Build cumulative start/end (ms)
    starts: List[int] = []
    ends: List[int] = []
    t = 0
    for d in durations:
        starts.append(int(t))
        t += float(d)
        ends.append(int(t))
    lines = ["gantt", "dateFormat X", "axisFormat %L", "section steps"]
    for i, s in enumerate(steps, 0):
        flag = "done" if getattr(s, "ok", True) else "crit"
        name = getattr(s, "name", f"step{i+1}")
        lines.append(f"{name}  :{flag}, step{i+1}, {starts[i]}, {ends[i]}")
    return _fence("\n".join(lines))


# ---------------------------------- 2-cells ---------------------------------

@dataclass(frozen=True)
class TwoCellView:
    name: str
    src_name: str   # X
    tgt_name: str   # Y
    f_name: str     # f: X→Y
    g_name: str     # g: X→Y


def twocell_mermaid(alpha: TwoCellView) -> str:
    body = f"""
graph LR
  X["{alpha.src_name}"] -->|{alpha.f_name}| Y["{alpha.tgt_name}"]
  X -->|{alpha.g_name}| Y
  note["{alpha.name}: {alpha.f_name} ⇒ {alpha.g_name}"] -.-> Y
""".strip()
    return _fence(body)


def vcomp2_mermaid(alpha: TwoCellView, beta: TwoCellView) -> str:
    body = f"""
graph LR
  X["{alpha.src_name}"] -->|{alpha.f_name}| Y["{alpha.tgt_name}"]
  X -->|{alpha.g_name}| Y
  X -->|h| Y
  a["{alpha.name}: {alpha.f_name}⇒{alpha.g_name}"] -.-> Y
  b["{beta.name}: {alpha.g_name}⇒h"] -.-> Y
  comp["{beta.name} ∘₁ {alpha.name} : {alpha.f_name} ⇒ h"] -.-> Y
""".strip()
    return _fence(body)


def hcomp2_mermaid(left: TwoCellView, right: TwoCellView) -> str:
    body = f"""
flowchart LR
  subgraph L["Left 2-cell"]
    X["{left.src_name}"] -->|{left.f_name}| Y["{left.tgt_name}"]
    X -->|{left.g_name}| Y
    noteL["{left.name}: {left.f_name}⇒{left.g_name}"] -.-> Y
  end
  subgraph R["Right 2-cell"]
    Y2["Y"] -->|{right.f_name}| Z["{right.tgt_name}"]
    Y2 -->|{right.g_name}| Z
    noteR["{right.name}: {right.f_name}⇒{right.g_name}"] -.-> Z
  end
  comp["{right.name} ∘₂ {left.name} : {left.f_name}·{right.f_name} ⇒ {left.g_name}·{right.g_name}"] --> Z
""".strip()
    return _fence(body)


# --------------------------------- Orchestrator ------------------------------

def render_all(
    items: Dict[str, Any], *, out_dir: Optional[str] = None, naturality_sample_limit: Optional[int] = 24
) -> Dict[str, str]:
    """
    items: {name: object} where object can be:
      - Category-like (has .arrows or .morphisms)
      - Functor-like  (has .source, .target, .object_map)
      - Natural-like  (has .source, .target, .components)
      - Plan-like     (has .factors)
      - Report/trace  (has .trace (preferred) or .steps with name/ok/duration_ms)
      - TwoCellView   (this class)
    Returns: {filename.md: markdown_with_mermaid}
    If out_dir is provided, also writes files there.
    """
    out: Dict[str, str] = {}

    def _write(fname: str, md: str) -> None:
        out[fname] = md
        if out_dir:
            Path(out_dir).mkdir(parents=True, exist_ok=True)
            Path(out_dir, fname).write_text(md, encoding="utf-8")

    for name, obj in items.items():
        # Functor?
        if all(hasattr(obj, a) for a in ("source", "target", "object_map")):
            _write(f"{name}__functor.md", "# Functor\n\n" + functor_mermaid(obj))
            continue
        # Natural?
        if all(hasattr(obj, a) for a in ("source", "target", "components")):
            Fs = getattr(obj.source, "source", None)
            blocks: List[str] = ["# Natural Transformation"]
            if Fs is not None and hasattr(Fs, "arrows"):
                morphs = sorted(Fs.arrows, key=lambda a: _arr_name(a))
                cap = naturality_sample_limit or len(morphs)
                for i, a in enumerate(morphs):
                    if i >= cap:
                        break
                    blocks.append(f"\n## Naturality on `{_arr_name(a)}`\n\n" + naturality_mermaid(obj, a))
            _write(f"{name}__natural.md", "\n".join(blocks))
            continue
        # Category?
        if hasattr(obj, "arrows") or hasattr(obj, "morphisms"):
            _write(f"{name}__category.md", "# Category\n\n" + category_mermaid(obj))
            continue
        # Plan?
        if hasattr(obj, "factors"):
            _write(f"{name}__plan.md", "# Plan\n\n" + plan_mermaid(obj))
            continue
        # Trace/Report?
        if hasattr(obj, "trace") or hasattr(obj, "steps"):
            _write(f"{name}__trace.md", "# Execution Trace (Gantt)\n\n" + exec_gantt_mermaid(obj))
            continue
        # TwoCellView?
        if isinstance(obj, TwoCellView):
            _write(f"{name}__twocell.md", "# 2-Cell\n\n" + twocell_mermaid(obj))
            continue
        raise TypeError(f"Don’t know how to render {name} ({type(obj).__name__})")

    return out



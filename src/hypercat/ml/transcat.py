
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, Any, Iterable, Tuple

@dataclass(frozen=True)
class ArchSpec:
    name: str
    meta: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ModelHandle:
    arch: ArchSpec
    weights: Dict[str, float]

@dataclass
class MetaOp:
    name: str
    apply_fn: Callable[[ModelHandle], ModelHandle]
    def apply(self, m: ModelHandle) -> ModelHandle: return self.apply_fn(m)

@dataclass
class MetaTransformer:
    name: str
    op: MetaOp
    def __rshift__(self, other: "MetaTransformer") -> "MetaTransformer":
        def composed(m: ModelHandle) -> ModelHandle:
            return other.op.apply(self.op.apply(m))
        return MetaTransformer(name=f"{self.name}∘{other.name}", op=MetaOp(f"{self.name}∘{other.name}", composed))

@dataclass
class NaturalTransformation:
    lhs: MetaTransformer
    rhs: MetaTransformer
    eps: float
    metric: Callable[[ModelHandle, ModelHandle], float]
    def certify(self, models: Iterable[ModelHandle]) -> Tuple[bool, float]:
        worst = 0.0
        for m in models:
            a = self.lhs.op.apply(m); b = self.rhs.op.apply(m)
            d = self.metric(a,b); worst = max(worst, d)
            if worst > self.eps: return False, worst
        return True, worst

def lora_attach(scale: float = 0.1) -> MetaTransformer:
    def _apply(m: ModelHandle) -> ModelHandle:
        new = {k: v + scale for k,v in m.weights.items()}
        return ModelHandle(m.arch, new)
    return MetaTransformer("LoRA_attach", MetaOp("LoRA_attach", _apply))

def quantize(step: float = 0.5) -> MetaTransformer:
    def _apply(m: ModelHandle) -> ModelHandle:
        new = {k: round(v/step)*step for k,v in m.weights.items()}
        return ModelHandle(m.arch, new)
    return MetaTransformer("Quantize", MetaOp("Quantize", _apply))

def prune(threshold: float = 0.05) -> MetaTransformer:
    def _apply(m: ModelHandle) -> ModelHandle:
        new = {k: (0.0 if abs(v) < threshold else v) for k,v in m.weights.items()}
        return ModelHandle(m.arch, new)
    return MetaTransformer("Prune", MetaOp("Prune", _apply))

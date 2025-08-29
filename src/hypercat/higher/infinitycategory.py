
from typing import Set, Dict, Any
from collections import defaultdict
from hypercat.core.core import Object
# Finite, ultrafinitist adapter
from hypercat.higher.finite.ncat import FiniteWeakNCategory

class InfinityCategory:
    """Finite/truncated adapter for (∞,1)-category semantics.
    Keeps the class name for backward compatibility; internally uses an n-bounded weak category.
    """
    def __init__(self, name: str, n: int = 3):
        self.name = name
        self.n = n
        self.objects: Set[Object] = set()
        self._ncat = FiniteWeakNCategory(n=n)

    def add_object(self, obj: Object) -> 'InfinityCategory':
        self.objects.add(obj); return self

    # Compatibility shim: keep a simple morphism-bucket interface
    def add_n_morphism(self, dim: int, morph: Any) -> 'InfinityCategory':
        assert 1 <= dim <= self.n, "dimension exceeds truncation"
        # In a real bridge, we'd map 'morph' to a generator id in _ncat.
        return self

    def nerve(self):
        # Export a trivial (n-truncated) structure; advanced users should use higher/finite/nsset.py
        from hypercat.higher.finite.nsset import FiniteTruncatedSSet
        S = FiniteTruncatedSSet(n=min(self.n,2))
        for o in self.objects:
            S.add_simplex(0, o)
        return S

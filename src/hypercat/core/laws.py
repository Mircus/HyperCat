from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Generic, Iterable, List, Optional, Protocol, Sequence, Tuple, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class Violation(Generic[T]):
	law: str
	message: str
	witness: Dict[str, Any]
	severity: str = "error"  # "error" | "warn"


@dataclass(frozen=True)
class LawResult(Generic[T]):
	law: str
	passed: bool
	violations: Sequence[Violation[T]]


class Law(Protocol[T]):
	name: str
	tags: Sequence[str]
	def run(self, ctx: T, config: Dict[str, Any]) -> LawResult[T]: ...


@dataclass(frozen=True)
class LawSuite(Generic[T]):
	name: str
	laws: Sequence[Law[T]]


@dataclass(frozen=True)
class SuiteReport(Generic[T]):
	suite: str
	results: Sequence[LawResult[T]]

	@property
	def ok(self) -> bool:
		return all(r.passed for r in self.results)

	def to_text(self) -> str:
		lines = [f"Suite {self.suite}: {'OK' if self.ok else 'FAIL'}"]
		for r in self.results:
			lines.append(f"  - {r.law}: {'OK' if r.passed else 'FAIL'}")
			for v in r.violations:
				lines.append(f"    • {v.severity.upper()} {v.message} | witness={v.witness}")
		return "\n".join(lines)


def run_suite(ctx: T, suite: LawSuite[T], *, config: Optional[Dict[str, Any]] = None) -> SuiteReport[T]:
	cfg = config or {}
	return SuiteReport[T](suite=suite.name, results=[law.run(ctx, cfg) for law in suite.laws])



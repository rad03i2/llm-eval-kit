from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Case:
    id: str
    output: str
    expected: str | None = None
    contains: tuple[str, ...] = ()
    excludes: tuple[str, ...] = ()
    regex: tuple[str, ...] = ()
    max_length: int | None = None


@dataclass(frozen=True)
class Result:
    id: str
    passed: bool
    score: float
    checks: dict[str, bool]
    failures: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _norm(value: str) -> str:
    return " ".join(value.casefold().split())


def parse_case(raw: dict[str, Any]) -> Case:
    if not isinstance(raw, dict):
        raise ValueError("each case must be an object")
    case_id = raw.get("id")
    output = raw.get("output")
    if not isinstance(case_id, str) or not case_id.strip():
        raise ValueError("case id must be a non-empty string")
    if not isinstance(output, str):
        raise ValueError(f"case {case_id!r}: output must be a string")
    expected = raw.get("expected")
    if expected is not None and not isinstance(expected, str):
        raise ValueError(f"case {case_id!r}: expected must be a string")
    def strings(name: str) -> tuple[str, ...]:
        value = raw.get(name, [])
        if not isinstance(value, list) or not all(isinstance(x, str) and x for x in value):
            raise ValueError(f"case {case_id!r}: {name} must be a list of non-empty strings")
        return tuple(value)
    max_length = raw.get("max_length")
    if max_length is not None and (not isinstance(max_length, int) or isinstance(max_length, bool) or max_length < 0):
        raise ValueError(f"case {case_id!r}: max_length must be a non-negative integer")
    regexes = strings("regex")
    for pattern in regexes:
        try:
            re.compile(pattern)
        except re.error as exc:
            raise ValueError(f"case {case_id!r}: invalid regex {pattern!r}: {exc}") from exc
    case = Case(case_id.strip(), output, expected, strings("contains"), strings("excludes"), regexes, max_length)
    if not any((case.expected is not None, case.contains, case.excludes, case.regex, case.max_length is not None)):
        raise ValueError(f"case {case_id!r}: at least one assertion is required")
    return case


def evaluate(case: Case) -> Result:
    checks: dict[str, bool] = {}
    if case.expected is not None:
        checks["expected"] = _norm(case.output) == _norm(case.expected)
    for i, text in enumerate(case.contains, 1):
        checks[f"contains:{i}"] = _norm(text) in _norm(case.output)
    for i, text in enumerate(case.excludes, 1):
        checks[f"excludes:{i}"] = _norm(text) not in _norm(case.output)
    for i, pattern in enumerate(case.regex, 1):
        checks[f"regex:{i}"] = re.search(pattern, case.output, re.MULTILINE) is not None
    if case.max_length is not None:
        checks["max_length"] = len(case.output) <= case.max_length
    failures = tuple(name for name, ok in checks.items() if not ok)
    score = sum(checks.values()) / len(checks) if checks else 0.0
    return Result(case.id, not failures, round(score, 4), checks, failures)


def evaluate_many(cases: list[Case]) -> dict[str, Any]:
    if not cases:
        raise ValueError("evaluation set is empty")
    results = [evaluate(case) for case in cases]
    passed = sum(result.passed for result in results)
    return {"summary": {"total": len(results), "passed": passed, "failed": len(results) - passed, "pass_rate": round(passed / len(results), 4)}, "results": [r.to_dict() for r in results]}


def load_cases(path: str | Path) -> list[Case]:
    source = Path(path)
    try:
        raw = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read evaluation file: {exc}") from exc
    items = raw.get("cases") if isinstance(raw, dict) else raw
    if not isinstance(items, list):
        raise ValueError("evaluation file must be a list or an object with a 'cases' list")
    cases = [parse_case(item) for item in items]
    ids = [case.id for case in cases]
    if len(ids) != len(set(ids)):
        raise ValueError("case ids must be unique")
    return cases

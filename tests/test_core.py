import json

import pytest

from llm_eval_kit.core import Case, evaluate, evaluate_many, load_cases, parse_case


def test_all_assertion_types_pass():
    case = Case("arabic", "الإجابة: الموصل مدينة عراقية", contains=("الموصل",), excludes=("بغداد فقط",), regex=(r"مدينة\s+عراقية",), max_length=100)
    result = evaluate(case)
    assert result.passed
    assert result.score == 1.0


def test_expected_normalizes_case_and_whitespace():
    assert evaluate(Case("x", " Hello   WORLD ", expected="hello world")).passed


def test_failure_score_and_names():
    result = evaluate(Case("x", "hello", contains=("hello", "missing"), max_length=3))
    assert not result.passed
    assert result.score == pytest.approx(1 / 3, abs=0.0001)
    assert result.failures == ("contains:2", "max_length")


def test_parse_rejects_no_assertions():
    with pytest.raises(ValueError, match="assertion"):
        parse_case({"id": "x", "output": "y"})


def test_parse_rejects_bad_regex():
    with pytest.raises(ValueError, match="invalid regex"):
        parse_case({"id": "x", "output": "y", "regex": ["["]})


def test_load_and_summary(tmp_path):
    path = tmp_path / "eval.json"
    path.write_text(json.dumps({"cases": [{"id": "a", "output": "yes", "expected": "yes"}, {"id": "b", "output": "no", "contains": ["yes"]}]}), encoding="utf-8")
    cases = load_cases(path)
    report = evaluate_many(cases)
    assert report["summary"] == {"total": 2, "passed": 1, "failed": 1, "pass_rate": 0.5}


def test_duplicate_ids_rejected(tmp_path):
    path = tmp_path / "eval.json"
    path.write_text('[{"id":"x","output":"a","expected":"a"},{"id":"x","output":"b","expected":"b"}]', encoding="utf-8")
    with pytest.raises(ValueError, match="unique"):
        load_cases(path)

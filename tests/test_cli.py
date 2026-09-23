import json

from llm_eval_kit.cli import main


def _write(tmp_path, cases):
    path = tmp_path / "cases.json"
    path.write_text(json.dumps({"cases": cases}, ensure_ascii=False), encoding="utf-8")
    return path


def test_cli_passes(tmp_path, capsys):
    path = _write(tmp_path, [{"id": "ok", "output": "Mosul", "expected": "mosul"}])
    assert main(["run", str(path)]) == 0
    assert "1/1 passed" in capsys.readouterr().out


def test_cli_fails_when_assertion_fails(tmp_path):
    path = _write(tmp_path, [{"id": "bad", "output": "x", "contains": ["y"]}])
    assert main(["run", str(path)]) == 1


def test_cli_json_and_report_file(tmp_path, capsys):
    path = _write(tmp_path, [{"id": "ok", "output": "نعم", "contains": ["نعم"]}])
    report = tmp_path / "reports" / "result.json"
    assert main(["run", str(path), "--json", "--output", str(report)]) == 0
    assert json.loads(capsys.readouterr().out)["summary"]["passed"] == 1
    assert json.loads(report.read_text(encoding="utf-8"))["results"][0]["id"] == "ok"


def test_validate_bad_file_returns_two(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{}", encoding="utf-8")
    assert main(["validate", str(path)]) == 2

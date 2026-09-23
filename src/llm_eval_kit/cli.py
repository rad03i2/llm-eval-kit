from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core import evaluate_many, load_cases

VERSION = "1.0.0"
AUTHOR = "Radwan Abdulhadi Ahmed / @rad03i2"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="llm-eval", description="Deterministic local evaluation for LLM outputs.")
    parser.add_argument("--version", action="version", version=f"llm-eval-kit {VERSION} — {AUTHOR}")
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run", help="Evaluate a JSON test set")
    run.add_argument("file", type=Path)
    run.add_argument("--json", action="store_true", dest="as_json")
    run.add_argument("--output", type=Path, help="Write JSON report to a file")
    validate = sub.add_parser("validate", help="Validate a test set without evaluating it")
    validate.add_argument("file", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        cases = load_cases(args.file)
        if args.command == "validate":
            print(f"Valid: {len(cases)} case(s)")
            return 0
        report = evaluate_many(cases)
        encoded = json.dumps(report, ensure_ascii=False, indent=2)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(encoded + "\n", encoding="utf-8")
        if args.as_json:
            print(encoded)
        else:
            summary = report["summary"]
            print(f"LLM Eval Kit — {summary['passed']}/{summary['total']} passed ({summary['pass_rate']:.0%})")
            for result in report["results"]:
                mark = "PASS" if result["passed"] else "FAIL"
                detail = "" if result["passed"] else f" [{', '.join(result['failures'])}]"
                print(f"{mark:4} {result['id']} score={result['score']:.0%}{detail}")
        return 0 if report["summary"]["failed"] == 0 else 1
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

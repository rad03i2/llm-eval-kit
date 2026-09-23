# Contributing

Thanks for improving LLM Eval Kit.

1. Fork the repository and create a focused branch.
2. Use Python 3.10+ and install with `python -m pip install -e . pytest`.
3. Keep evaluators deterministic and offline by default.
4. Add tests for behavior changes and run `python -m pytest -q`.
5. Update the bilingual README when user-facing behavior changes.
6. Open a concise pull request describing the motivation and validation performed.

Please do not commit model credentials, private prompts/data, generated reports, or unrelated artifacts. By contributing, you agree that your contribution is licensed under the MIT License.

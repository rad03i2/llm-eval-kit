# Security Policy

## Supported version

The current `main` branch and latest tagged release are supported.

## Security model

LLM Eval Kit is offline and deterministic: it does not call model providers, execute evaluated text, load Python expressions from evaluation files, or transmit telemetry. Evaluation files are treated as untrusted data. Regular expressions are Python regular expressions and a pathological pattern can consume significant CPU; only use regex rules you trust in shared CI environments.

Do not place secrets, API keys, confidential prompts, or personal data in committed evaluation fixtures or reports.

## Reporting

Please report a suspected vulnerability privately through GitHub's security reporting facilities when available. Do not include real credentials or sensitive production data in a public issue.

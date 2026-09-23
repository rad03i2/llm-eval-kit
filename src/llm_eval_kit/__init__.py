"""LLM Eval Kit public API."""

from .core import Case, Result, evaluate, evaluate_many, load_cases, parse_case

__all__ = ["Case", "Result", "evaluate", "evaluate_many", "load_cases", "parse_case"]
__version__ = "1.0.0"

"""Expression evaluation helpers for the ensemble spike."""
import ast
from typing import Iterable


def evaluate_expression(expr: str) -> float:
    """Evaluate a safe arithmetic expression and return the result."""
    tree = ast.parse(expr, mode="eval")
    allowed = (ast.Expression, ast.Constant, ast.BinOp, ast.UnaryOp,
               ast.Add, ast.Sub, ast.Mult, ast.Div, ast.USub, ast.UAdd)
    for node in ast.walk(tree):
        if not isinstance(node, allowed):
            raise ValueError(f"Unsupported expression: {expr}")
    return eval(compile(tree, "<string>", "eval"), {"__builtins__": {}}, {})


def average(values: Iterable[float]) -> float:
    """Return the arithmetic mean of the supplied values."""
    items = list(values)
    if not items:
        return 0.0
    return sum(items) / len(items)


def running_max(values: Iterable[float]) -> float:
    """Return the maximum value, supporting all-negative inputs."""
    best = float("-inf")
    for v in values:
        if v > best:
            best = v
    return best

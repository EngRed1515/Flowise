"""Safe evaluator for the JSON condition DSL used by the Rules Repository.

A condition is a JSON object with a single operator key. This avoids `eval`
entirely while keeping rules fully data-driven and auditable.

Supported forms::

    {"all": [ <cond>, ... ]}              # logical AND
    {"any": [ <cond>, ... ]}              # logical OR
    {"not": <cond>}                       # negation
    {"op": "eq", "field": "x", "value": 1}
    {"op": "ne|gt|gte|lt|lte", ...}
    {"op": "in", "field": "x", "value": [..]}
    {"op": "between", "field": "x", "value": [lo, hi]}   # lo <= x < hi (hi may be null)
    {"op": "exists", "field": "x"}
    {"op": "truthy", "field": "x"}

`field` is resolved against the flat fact dictionary produced by facts.py.
"""
from typing import Any

Facts = dict[str, Any]


def _num(v: Any) -> float | None:
    try:
        return float(v) if v is not None else None
    except (TypeError, ValueError):
        return None


def _leaf(cond: dict, facts: Facts) -> bool:
    op = cond["op"]
    field = cond.get("field")
    actual = facts.get(field) if field is not None else None
    value = cond.get("value")

    if op == "exists":
        return field in facts and facts[field] is not None
    if op == "truthy":
        return bool(actual)
    if op == "eq":
        return actual == value
    if op == "ne":
        return actual != value
    if op == "in":
        return actual in (value or [])
    if op in {"gt", "gte", "lt", "lte"}:
        a, b = _num(actual), _num(value)
        if a is None or b is None:
            return False
        return {"gt": a > b, "gte": a >= b, "lt": a < b, "lte": a <= b}[op]
    if op == "between":
        a = _num(actual)
        lo, hi = (value + [None, None])[:2] if isinstance(value, list) else (None, None)
        lo, hi = _num(lo), _num(hi)
        if a is None:
            return False
        if lo is not None and a < lo:
            return False
        if hi is not None and a >= hi:
            return False
        return True
    raise ValueError(f"Unknown operator: {op}")


def evaluate(cond: dict | None, facts: Facts) -> bool:
    """Evaluate a condition tree against a fact set. None / {} == always true."""
    if not cond:
        return True
    if "all" in cond:
        return all(evaluate(c, facts) for c in cond["all"])
    if "any" in cond:
        return any(evaluate(c, facts) for c in cond["any"])
    if "not" in cond:
        return not evaluate(cond["not"], facts)
    if "op" in cond:
        return _leaf(cond, facts)
    raise ValueError(f"Malformed condition: {cond}")

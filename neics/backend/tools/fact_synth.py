"""Synthesise positive / negative fact sets that satisfy / violate a rule's JSON
condition tree. Used by the rules-verification report to auto-generate a test
case (and its inverse) for every rule in the repository."""
from typing import Any


def _leaf(cond: dict, target: bool) -> dict:
    op, field, value = cond.get("op"), cond.get("field"), cond.get("value")
    if op == "exists":
        return {field: 1} if target else {field: None}
    if op == "truthy":
        return {field: True} if target else {field: False}
    if op == "eq":
        return {field: value} if target else {field: f"__not__{value}"}
    if op == "ne":
        return {field: f"__other__{value}"} if target else {field: value}
    if op == "in":
        vals = value or []
        return {field: vals[0] if vals else None} if target else {field: "__not_in_list__"}
    if op == "gt":
        return {field: (value or 0) + 1} if target else {field: (value or 0) - 1}
    if op == "gte":
        return {field: (value or 0)} if target else {field: (value or 0) - 1}
    if op == "lt":
        return {field: (value or 0) - 1} if target else {field: (value or 0) + 1}
    if op == "lte":
        return {field: (value or 0)} if target else {field: (value or 0) + 1}
    if op == "between":
        lo, hi = (value + [None, None])[:2] if isinstance(value, list) else (None, None)
        if target:
            return {field: lo if lo is not None else ((hi or 1) - 1)}
        return {field: (hi if hi is not None else (lo or 0) + 1)}
    return {}


def synth(cond: dict | None, target: bool = True) -> dict[str, Any]:
    """Return a fact set for which `evaluate(cond, facts) == target`.

    Returns {} for an always-true rule (logic None); such rules are flagged as
    default/fallback rules by the caller.
    """
    if not cond:
        return {}
    if "all" in cond:
        if target:
            facts: dict[str, Any] = {}
            for c in cond["all"]:
                facts.update(synth(c, True))
            return facts
        # falsify the first child only
        facts = {}
        for i, c in enumerate(cond["all"]):
            facts.update(synth(c, i != 0))
        return facts
    if "any" in cond:
        if target:
            return synth(cond["any"][0], True)
        facts = {}
        for c in cond["any"]:
            facts.update(synth(c, False))
        return facts
    if "not" in cond:
        return synth(cond["not"], not target)
    if "op" in cond:
        return _leaf(cond, target)
    return {}

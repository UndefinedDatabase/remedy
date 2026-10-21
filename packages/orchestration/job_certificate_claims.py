"""The claims a job certificate states, derived from the bytes of the member that carries each (F060).

The builder and the verifier both call these functions on the bytes of a member, so a claim in a
certificate's manifest can be checked against the member it comes from and the two always compute it
alike (DECISION F060 D3). Each answers for `data is None`, the case of a member the job never had.
"""
from __future__ import annotations

import json


def _json_object(data: bytes) -> dict | None:
    """The bytes as a UTF-8 JSON object, None when they are anything else."""
    try:
        obj = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None
    return obj if isinstance(obj, dict) else None


# WHY: the cost and its basis come from the budget member alone, so the verifier can recompute them.
def cost_claims_from_member(data: bytes | None) -> tuple[str | None, list[str]]:
    from packages.orchestration.budget_guard import (
        BudgetCounterError,
        counters_from_persisted,
        decode_persisted_budget_actuals,
    )

    if data is None:
        return None, []
    obj = _json_object(data)
    if obj is None or "budget_actuals" not in obj:
        return None, []
    first = obj.get("first_running_at")
    try:
        counters = counters_from_persisted(decode_persisted_budget_actuals(
            obj["budget_actuals"], first_running_at=first if isinstance(first, str) else None))
    except BudgetCounterError:
        return None, []
    return counters.cost_description(), list(counters.actual_sources)


# WHY: the Definition of Done summary comes from the verdict member alone, never from the data folder.
def dod_summary_from_member(data: bytes | None) -> dict | None:
    from packages.orchestration.dod_runners import STATUS_PASSED

    if data is None:
        return None
    obj = _json_object(data)
    if obj is None:
        return None
    raw_checks = obj.get("checks")
    checks = raw_checks if isinstance(raw_checks, list) else []
    passed = [c for c in checks if isinstance(c, dict) and c.get("status") == STATUS_PASSED]
    return {"released": bool(obj.get("released")), "check_count": len(checks),
            "passed_count": len(passed)}


# WHY: the regression status comes from the final verifier member alone.
def regression_status_from_member(data: bytes | None):
    if data is None:
        return None
    obj = _json_object(data)
    return obj.get("test_status") if obj is not None else None

"""A call's own fields in a run's record (DECISION F058 D3).

The two helpers below moved unchanged out of `packages/orchestration/pingpong_loop.py`, which
imports them back by name.
"""

from __future__ import annotations

from typing import Any

from packages.orchestration.model_failover import FailoverDisclosure


def _add_exit_detail(block: dict[str, Any], out: Any) -> None:
    """Name a failed provider child's exit code and stderr tail in the run record (R-1016).

    Only a call whose child exited nonzero carries them, so an ordinary round's
    JSON keeps exactly the keys it always had.
    """
    code = getattr(out, "exit_code", None)
    if code is not None:
        block["exit_code"] = code
        block["stderr_tail"] = getattr(out, "stderr_tail", "")


def _session_fields(out: Any) -> dict[str, Any]:
    """R-1055: the provider session a call reported, and whether it resumed one.

    Persisted so the relaunch of an interrupted task can find its parked session
    (:func:`parked_session_refs`), and so the record shows whether it did.
    A call a failover walk served also carries the last key ``failover`` (DECISION
    F058 D3): the session reported is the serving link's own, not the primary's, so
    the record discloses which model it belongs to.
    """
    actuals = getattr(out, "usage_actuals", None) or {}
    fields = {
        "session_id": str(actuals.get("session_id") or ""),
        "resume_used": bool(getattr(out, "resume_used", False)),
        "resume_session_ref": str(getattr(out, "resume_session_ref", "") or ""),
        "resume_fallback": bool(getattr(out, "resume_fallback", False)),
    }
    disclosure = getattr(out, "failover_disclosure", None)
    if isinstance(disclosure, FailoverDisclosure):
        fields["failover"] = disclosure.to_json()
    return fields

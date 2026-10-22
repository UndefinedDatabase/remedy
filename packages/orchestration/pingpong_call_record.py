"""A call's own fields in a run's record (DECISION F058 D3).

The three helpers below moved unchanged out of `packages/orchestration/pingpong_loop.py`, which
imports them back by name.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from packages.orchestration.model_failover import FailoverDisclosure
from packages.orchestration.tier_escalation import escalated_call_of


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
    Every call the failover walk reached carries the last key ``failover`` (DECISION
    F058 D3), whether a backup served it or its chain ran out: a session a backup
    reports is that backup's own, not the primary's, so the record discloses which
    model it belongs to. Every call an escalated provider served carries ``escalation``
    before it (DECISION F296 D3): the tier it came from and ran on, the reason and the round.
    """
    actuals = getattr(out, "usage_actuals", None) or {}
    fields = {
        "session_id": str(actuals.get("session_id") or ""),
        "resume_used": bool(getattr(out, "resume_used", False)),
        "resume_session_ref": str(getattr(out, "resume_session_ref", "") or ""),
        "resume_fallback": bool(getattr(out, "resume_fallback", False)),
    }
    escalated = escalated_call_of(out)
    if escalated is not None:
        fields["escalation"] = escalated.to_json()
    disclosure = getattr(out, "failover_disclosure", None)
    if isinstance(disclosure, FailoverDisclosure):
        fields["failover"] = disclosure.to_json()
    return fields


def parked_session_refs(run_record: dict[str, Any] | None) -> dict[str, str]:
    """R-1055: the session each role last reported in a persisted run, by role.

    Reads ``result.json`` as :func:`export_pingpong_json` writes it. A record
    written before R-1055 carries no ``session_id`` and answers ``{}``, which
    resumes nothing. A round entry whose ``failover`` names a serving link
    (DECISION F058 D4) clears that role instead of setting its session: a
    session a backup model opened is never offered to the primary on relaunch.
    An entry carrying ``escalation`` clears its role the same way (DECISION F296 D3):
    a relaunch starts on the run's configured models, which never resume an escalated
    model's session.
    """
    refs: dict[str, str] = {}
    for round_data in (run_record or {}).get("rounds") or []:
        for role in ("builder", "reviewer"):
            entry = round_data.get(role) or {}
            failover = entry.get("failover")
            if (isinstance(failover, Mapping) and failover.get("used")) or isinstance(entry.get("escalation"), Mapping):
                refs.pop(role, None)
                continue
            session_id = str(entry.get("session_id") or "")
            if session_id:
                refs[role] = session_id
    return refs

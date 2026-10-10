"""F268, F269 — what a `remedy do` walk reports when it ends: the mission's contract and the
measured tokens and cost read back from the ledger;
moved out of `packages/orchestration/do_sequence.py` unchanged, as a step of that file's
boundary on `docs/system/structure-ledger-v1.md` (structure rule 2, DECISION F205 D3);
`do_sequence.py` imports every name back by name, so each import path keeps working.
"""

from __future__ import annotations

from typing import Any

from packages.orchestration.do_context import DoContext

# ---------------------------------------------------------------------------
# The measured cost of the walk, read from the F103 ledger (DECISION F268 D11).
# ---------------------------------------------------------------------------


def _add_measured(total: float | int | None, value: float | int | None) -> float | int | None:
    """Sum two ledger figures as the ledger's own SUM does: None only when both are None."""
    if value is None:
        return total
    return value if total is None else total + value


def do_mission_contract(ctx: DoContext) -> dict[str, Any] | None:
    """The walk's mission contract body as its record holds it, or None.

    None when the walk created no mission or the mission has no contract
    (DECISION F269 D4 (6)); read from the record, so it is the contract as
    the walk left it.
    """
    if not ctx.mission_id or ctx.project is None:
        return None
    from packages.orchestration.mission_state import load_mission

    body = load_mission(str(ctx.project.id), ctx.mission_id).contract
    return body if isinstance(body, dict) else None


def do_unmet_blocking_criteria(contract: dict[str, Any] | None) -> list[str]:
    """The contract's blocking criteria not met after the walk, in contract order.

    DECISION F269 D6 (4): the blockers of D4 (5), read from the body
    `do_mission_contract` returns; empty when the walk left no contract.
    """
    from packages.orchestration.mission_contract import MissionContract, contract_blockers

    return list(contract_blockers(
        None if contract is None else MissionContract.from_json(contract)))


def do_contract_summary_line(contract: dict[str, Any] | None) -> str | None:
    """The one text line naming the contract's state after the walk, or None without one.

    DECISION F269 D6 (4): the met criteria counted against all of them, and
    each blocking criterion not met named with its status, `open` or `unmet`.
    DECISION F299 D2 (4): a blocking criterion that is `unchecked` — its
    project named no test command, so nothing ran — is named separately, after
    the ones genuinely not met, with the one phrase every surface uses.
    """
    if contract is None:
        return None
    from packages.orchestration.mission_contract import (
        CRITERION_STATUS_UNCHECKED,
        MissionContract,
    )
    from packages.orchestration.project_tests import NO_CHECK_RAN_WORDS

    criteria = MissionContract.from_json(contract).criteria
    met = sum(1 for c in criteria if c.status == "met")
    not_met = [f"{c.id} ({c.status})" for c in criteria
              if c.blocking and c.status in ("open", "unmet")]
    unchecked = [c.id for c in criteria
                if c.blocking and c.status == CRITERION_STATUS_UNCHECKED]
    parts = []
    if not_met:
        parts.append(f"blocking criteria not met: {', '.join(not_met)}")
    if unchecked:
        parts.append(f"for {', '.join(unchecked)}, {NO_CHECK_RAN_WORDS}")
    tail = "; ".join(parts) if parts else "every blocking criterion is met"
    return f"Contract: {met} of {len(criteria)} criteria met; {tail}"


def do_cost_summary(ctx: DoContext) -> dict[str, Any] | None:
    """The walk's measured tokens per role and cost, or None when no job ran.

    Read through `token_ledger.query_cost(..., job_id=<id>, by="role")` for each
    job the run step mirrored, and summed over them; a figure no call reported
    stays None, never 0. A job whose mirror failed is named in
    `mirror_failed_job_ids`, with its error, and contributes nothing.
    """
    if not ctx.cost_mirrors:
        return None
    from packages.orchestration.token_ledger import query_cost

    failed = {job_id: str(mirror.get("error") or "")
              for job_id, mirror in ctx.cost_mirrors.items()
              if not mirror.get("ledger_mirrored")}
    roles: dict[str | None, dict[str, Any]] = {}
    for job_id in ctx.cost_mirrors:
        if job_id in failed:
            continue
        report = query_cost(project_id=str(ctx.project.id), job_id=job_id, by="role")
        for row in report.rows:
            role = roles.setdefault(row.bucket, {
                "role": row.bucket, "calls": 0, "tokens_in": None, "tokens_out": None,
                "cache_read": None, "cost_usd": None})
            role["calls"] += row.calls
            for key in ("tokens_in", "tokens_out", "cache_read", "cost_usd"):
                role[key] = _add_measured(role[key], getattr(row, key))
    cost_usd = None
    for role in roles.values():
        cost_usd = _add_measured(cost_usd, role["cost_usd"])
    return {
        "roles": sorted(roles.values(), key=lambda r: str(r["role"])),
        "cost_usd": cost_usd,
        "job_ids": [job_id for job_id in ctx.cost_mirrors if job_id not in failed],
        "mirror_failed_job_ids": list(failed),
        "mirror_errors": failed,
    }


def _measured(value: float | int | None) -> str:
    return "not reported" if value is None else f"{value}"


def do_cost_summary_lines(summary: dict[str, Any] | None) -> list[str]:
    """The text lines of `do_cost_summary`: one per role, one for the cost, one per failed mirror."""
    if summary is None:
        return []
    lines = [f"Tokens {role['role'] or '(role not named)'}: input {_measured(role['tokens_in'])}, "
             f"output {_measured(role['tokens_out'])}, "
             f"cache read {_measured(role['cache_read'])} ({role['calls']} call(s))"
             for role in summary["roles"]]
    cost = summary["cost_usd"]
    lines.append("Cost: not reported by the provider" if cost is None
                 else f"Cost: ${cost:.6f} (measured, from the ledger)")
    lines.extend(f"Cost NOT recorded to the ledger for job {job_id}: {error}"
                 for job_id, error in summary["mirror_errors"].items())
    return lines

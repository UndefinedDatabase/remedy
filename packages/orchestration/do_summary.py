"""F268, F269 — what a `remedy do` walk reports when it ends: the mission's contract and the
measured tokens and cost read back from the ledger;
moved out of `packages/orchestration/do_sequence.py` unchanged, as a step of that file's
boundary on `docs/system/structure-ledger-v1.md` (structure rule 2, DECISION F205 D3);
every consumer imports these names from here (operator amendment amend1014-luna-mission-fixes D.2).
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
    job the run step mirrored, from the ledger of the job's own project (DECISION
    F205 D4), and summed over them; a figure no call reported stays None, never 0. A job whose mirror failed is named in
    `mirror_failed_job_ids`, with its error, and contributes nothing.
    """
    if not ctx.cost_mirrors:
        return None
    from packages.orchestration.job_tokens import cockpit_show_cost_usd, job_token_roles

    failed = {job_id: str(mirror.get("error") or "")
              for job_id, mirror in ctx.cost_mirrors.items()
              if not mirror.get("ledger_mirrored")}
    roles: dict[str | None, dict[str, Any]] = {}
    for job_id in ctx.cost_mirrors:
        if job_id in failed:
            continue
        # amend1015: the one reader the digest and the cockpit's TOKENS tile read too.
        for row in job_token_roles(_job_ledger_project(ctx, job_id), job_id, _job_run_ids(ctx, job_id)):
            role = roles.setdefault(row["role"], {
                "role": row["role"], "harness_invocations": 0, "model_turns": None, "tokens_in": None,
                "tokens_out": None, "cache_read": None, "cost_usd": None})
            role["harness_invocations"] += row["harness_invocations"]
            for key in ("model_turns", "tokens_in", "tokens_out", "cache_read", "cost_usd"):
                role[key] = _add_measured(role[key], row[key])
    cost_usd = None
    for role in roles.values():
        cost_usd = _add_measured(cost_usd, role["cost_usd"])
    return {
        "roles": sorted(roles.values(), key=lambda r: str(r["role"])),
        "cost_usd": cost_usd,
        "job_ids": [job_id for job_id in ctx.cost_mirrors if job_id not in failed],
        "mirror_failed_job_ids": list(failed),
        "mirror_errors": failed,
        "show_cost_usd": cockpit_show_cost_usd(str(getattr(ctx, "repo_root", "") or "")),
    }


def _job_run_ids(ctx: DoContext, job_id: str) -> list[str]:
    from packages.orchestration.pingpong_job import load_job_plan

    job = load_job_plan(job_id)
    return list(job.run_refs) if job is not None else []


def _job_ledger_project(ctx: DoContext, job_id: str) -> str:
    """The project whose ledger holds a job's calls: the walk's own, or, in a walk over several
    projects, the job's own project (DECISION F205 D4)."""
    if not ctx.projects:
        return str(ctx.project.id)
    from packages.orchestration.pingpong_job import load_job_plan

    job = load_job_plan(job_id)
    return str(job.project_id) if job is not None and job.project_id else str(ctx.project.id)


def do_verification_lines(jobs: list[dict[str, Any]]) -> list[str]:
    """One text line per job naming its verification honestly (exec-1017 D2): what ran and how it
    ended, or that the order asked for tests and none ran, or that none were asked for."""
    lines = []
    for job in jobs:
        found = job.get("verification")
        if not found:
            continue
        ran = ", ".join(f"{run.get('command') or run['source']} {run['status']}" for run in found["runs"])
        asked = f" — the order asks: {found['request']}" if found["required"] else ""
        detail = {"passed": ran, "failed": ran, "pending": "the job has not ended",
                  "not_run": f"NO test ran: {found['reason']}",
                  "not_required": f"no tests ran ({found['reason'] or 'the order asks for none'})"}[found["status"]]
        lines.append(f"Verification of job {job['job_id']}: {found['status']} — {detail}{asked}")
    return lines


def do_summary_lines(contract: dict[str, Any] | None, jobs: list[dict[str, Any]],
                     cost: dict[str, Any] | None) -> list[str]:
    """The text lines a walk ends with: the contract's state, each job's verification, the cost."""
    contract_line = do_contract_summary_line(contract)
    return ([contract_line] if contract_line is not None else []) + do_verification_lines(jobs) + \
        do_cost_summary_lines(cost)


def _measured(value: float | int | None) -> str:
    return "not reported" if value is None else f"{value}"


def _turns_words(role: dict[str, Any]) -> str:
    n, turns = role["harness_invocations"], role["model_turns"]
    invocations = f"{n} harness invocation{'' if n == 1 else 's'}"
    if turns is None:
        return f"{invocations}; model turns not reported"
    return f"{invocations}, {turns} model turn{'' if turns == 1 else 's'}"


def do_cost_summary_lines(summary: dict[str, Any] | None, *, show_cost_usd: bool | None = None) -> list[str]:
    """The text lines of `do_cost_summary`: one per role, one for the cost, one per failed mirror.

    amend1015 Part 5.2: a measured dollar figure is printed only with *show_cost_usd*, which
    defaults to the summary's own reading of `[cockpit] show_cost_usd = true` in the project's
    `.remedy/config.toml`.
    """
    if summary is None:
        return []
    lines = [f"Tokens {role['role'] or '(role not named)'}: input {_measured(role['tokens_in'])}, "
             f"output {_measured(role['tokens_out'])}, "
             f"cache read {_measured(role['cache_read'])} ({_turns_words(role)})"
             for role in summary["roles"]]
    cost = summary["cost_usd"]
    if show_cost_usd is None:
        show_cost_usd = bool(summary.get("show_cost_usd"))
    if cost is None:
        lines.append("Cost: not reported by the provider")
    elif show_cost_usd:
        lines.append(f"Cost: ${cost:.6f} (measured, from the ledger)")
    else:
        lines.append("Cost: not shown — tokens only (set show_cost_usd = true under [cockpit] "
                     "in .remedy/config.toml to show it)")
    lines.extend(f"Cost NOT recorded to the ledger for job {job_id}: {error}"
                 for job_id, error in summary["mirror_errors"].items())
    return lines


def do_json_document(ctx: DoContext, *, jobs: list[dict[str, Any]], cost: dict[str, Any] | None,
                     contract: dict[str, Any] | None) -> dict[str, Any]:
    """The object the JSON answer of `remedy do` carries: the walk's ids, shape, jobs, steps, cost and order budget.

    `order_budget` is the order's one ledger (scale audit P1-4): the caps, every planner call with
    its reason and outcome, the jobs' spend and what the planning calls cost in estimated tokens.
    """
    return {
        "mission_id": ctx.mission_id or None, "order_id": ctx.order_id or None,
        "job_ids": list(ctx.job_ids),
        "waiting_job_ids": list(ctx.waiting_job_ids),
        "contract": contract,
        "unmet_blocking_criteria": do_unmet_blocking_criteria(contract),
        "stopped_before_apply": ctx.stopped_before_apply,
        "shape": ctx.shape or None,
        "shape_source": ctx.shape_source or None,
        "mission_plan_path": ctx.mission_plan_path or None,
        "jobs": jobs,
        "steps": [r.to_json() for r in ctx.results],
        "cost": cost,
        "order_budget": ctx.ledger.summary() if ctx.ledger is not None else None,
        "landed": list(ctx.landed),
        "push": ctx.push_outcome,
        "next": list(ctx.next_lines),
    }

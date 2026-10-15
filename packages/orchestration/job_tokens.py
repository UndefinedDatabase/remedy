"""amend1015 Part 1.4 and Part 5: the tokens one job used, read ONE way for every surface.

``remedy do`` prints its ``Tokens builder:`` lines from the project's call ledger
(``token_ledger.query_cost(..., by="role")``) and Pi's own turn counts
(``pi_turn_counts.pi_turns_for_job``). Before this module the cockpit's digest and TOKENS
tile read neither, so a run the terminal measured showed "not-measured" and "—". Every
surface now reads ``job_token_roles``; the digest and the dashboard read its summary.

Remedy deliberately does not show a dollar figure in the cockpit unless the project asks
for it with ``show_cost_usd = true`` in the ``[cockpit]`` table of ``.remedy/config.toml``:
the operator works on subscriptions and judges a run by its tokens (amend1015 Part 5).

The dashboard's older, event-estimated reading (``event_token_usage``) moved here from
``ui_server.py`` unchanged, so both token readings of a job live in one module.

Public API::

    job_token_roles(project_id, job_id, run_ids) -> list[dict]
    job_token_summary(job) -> dict
    job_token_line(roles) -> str
    cockpit_show_cost_usd(repo_path) -> bool
    event_token_usage(events) -> dict
    dashboard_token_usage(job, events) -> dict
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

#: The token fields a role row carries; each is None when no call of the role reported it.
TOKEN_FIELDS = ("tokens_in", "tokens_out", "cache_read", "cost_usd")


def _add_measured(total: float | int | None, value: float | int | None) -> float | int | None:
    """Sum two ledger figures as the ledger's own SUM does: None only when both are None."""
    if value is None:
        return total
    return value if total is None else total + value


# The one reader of a job's measured tokens per role: the ledger's rows plus Pi's turn counts.
def job_token_roles(project_id: str, job_id: str, run_ids: list[str]) -> list[dict[str, Any]]:
    """One dict per ledger role of *job_id*: harness_invocations, model_turns and TOKEN_FIELDS."""
    from packages.orchestration.pi_turn_counts import pi_turns_for_job
    from packages.orchestration.token_ledger import query_cost

    report = query_cost(project_id=project_id, job_id=job_id, by="role")
    turns = pi_turns_for_job(run_ids)
    roles = []
    for row in report.rows:
        pi = turns.get(str(row.bucket))
        roles.append({"role": row.bucket, "harness_invocations": row.calls,
                      "model_turns": None if pi is None else pi["model_turns"],
                      **{key: getattr(row, key) for key in TOKEN_FIELDS}})
    return roles


def _compact(value: int | float) -> str:
    """A token count a person reads at a glance: 950, 1.2k, 3.4M."""
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"{value / 1_000:.1f}k"
    return f"{int(value)}"


def job_token_line(roles: list[dict[str, Any]]) -> str:
    """``builder: 2 harness invocations, 1.2k in / 300 out; reviewer: …`` — "" with no role."""
    parts = []
    for role in roles:
        n = role["harness_invocations"]
        words = [f"{n} harness invocation{'' if n == 1 else 's'}"]
        if role["tokens_in"] is None and role["tokens_out"] is None:
            words.append("tokens not reported by the provider")
        else:
            words.append(" / ".join(f"{'?' if role[key] is None else _compact(role[key])} {label}"
                                    for key, label in (("tokens_in", "in"), ("tokens_out", "out"))))
            if role["cache_read"]:
                words.append(f"{_compact(role['cache_read'])} cache read")
        if role["model_turns"] is not None:
            words.append(f"{role['model_turns']} model turn{'' if role['model_turns'] == 1 else 's'}")
        parts.append(f"{role['role'] or '(role not named)'}: {', '.join(words)}")
    return "; ".join(parts)


def job_token_summary(job: Any) -> dict[str, Any]:
    """The job's roles from ``job_token_roles``, their totals and ``line``; never raises.

    A job with no project, or a ledger that cannot be read, reads as no role at all —
    ``harness_invocations`` 0 and every token figure None — never as a measured zero.
    """
    project_id = str(getattr(job, "project_id", "") or "")
    job_id = str(getattr(job, "job_id", "") or "")
    roles: list[dict[str, Any]] = []
    if project_id and job_id:
        try:
            roles = job_token_roles(project_id, job_id, [str(r) for r in getattr(job, "run_refs", ()) or ()])
        except (OSError, ValueError, sqlite3.Error):
            # A ledger or a turn record that cannot be read is no measurement, never a gate.
            roles = []
    totals: dict[str, Any] = {"harness_invocations": sum(r["harness_invocations"] for r in roles),
                              "model_turns": None, **{key: None for key in TOKEN_FIELDS}}
    for role in roles:
        for key in ("model_turns", *TOKEN_FIELDS):
            totals[key] = _add_measured(totals[key], role[key])
    return {"roles": roles, **totals, "line": job_token_line(roles)}


def cockpit_show_cost_usd(repo_path: str) -> bool:
    """True only when ``[cockpit] show_cost_usd = true`` in *repo_path*'s ``.remedy/config.toml``."""
    try:
        import tomllib
    except ImportError:  # Python 3.10
        import tomli as tomllib  # type: ignore[no-redef]
    if not repo_path:
        return False
    try:
        data = tomllib.loads((Path(repo_path) / ".remedy" / "config.toml").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    cockpit = data.get("cockpit")
    return isinstance(cockpit, dict) and cockpit.get("show_cost_usd") is True


def event_token_usage(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Build safe token usage summary from events. Estimated only — no exact billing."""
    by_role: dict[str, int] = {}
    total = 0
    sources_seen: set[str] = set()

    for e in events:
        meta = e.get("metadata", {})
        tokens = meta.get("estimated_tokens", 0)
        if not isinstance(tokens, (int, float)) or tokens <= 0:
            continue
        tokens = int(tokens)
        total += tokens

        ev = e.get("event", "")
        if ev == "project_memory_recalled":
            by_role["memory"] = by_role.get("memory", 0) + tokens
            sources_seen.add("memory")
        elif ev == "repair_context_created":
            by_role["repair"] = by_role.get("repair", 0) + tokens
            sources_seen.add("repair_context")
        else:
            by_role["other"] = by_role.get("other", 0) + tokens

    known = total > 0
    missing: list[str] = []
    if "memory" not in sources_seen:
        missing.append("memory")

    return {
        "total_tokens": total if known else None,
        "known": known,
        "estimated": True,
        "source": "event_metadata",
        "by_role": by_role if by_role else {},
        "missing_sources": missing,
    }


def dashboard_token_usage(job: Any, events: list[dict[str, Any]]) -> dict[str, Any]:
    """The dashboard's ``token_usage``: the event estimate, plus ``ledger`` (``job_token_summary``)
    and ``show_cost_usd`` (``cockpit_show_cost_usd`` of the job's repository)."""
    return {**event_token_usage(events), "ledger": job_token_summary(job),
            "show_cost_usd": cockpit_show_cost_usd(str(getattr(job, "repo_path", "") or ""))}

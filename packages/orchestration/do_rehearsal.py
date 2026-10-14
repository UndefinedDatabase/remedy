"""F055 — a rehearsal's stop: `remedy do`'s `--rehearse` flag plans an order and halts at the
same boundary `--plan-only` halts at, naming the approval each waiting job still needs and the
run that would follow it, without running any job (DECISION F055 D1); the rehearsal's own
record and readable summary, written beside each job it walks (DECISION F055 D2); the staleness
warning a moved repository earns and the label a waiting rehearsed job carries (DECISION F055 D3).
"""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packages.orchestration.do_context import DO_STEP_STOPPED, DoContext, _job_run_role_flags

#: Schema version of the rehearsal record `build_job_rehearsal` answers (DECISION F055 D2).
REHEARSAL_SCHEMA_V = "rehearsal_v1"


# WHY: a rehearsal stops exactly where `--plan-only` stops, but names the approval a waiting
# job still needs before its `job run` line, so the rehearsed plan is one `yes` away from a run.
def stop_walk_for_rehearsal(ctx: DoContext) -> tuple[str, str]:
    """Stop the walk before any job runs, writing each job's rehearsal record and summary."""
    from packages.orchestration.job_plan import task_plan_blocks_execution
    from packages.orchestration.pingpong_job import load_job_plan

    summary_paths: list[str] = []
    for job_id in ctx.job_ids:
        job = load_job_plan(job_id)
        if job is not None:
            summary_paths.append(str(write_job_rehearsal(job)))
            if task_plan_blocks_execution(job) is not None:
                ctx.next_lines.append(f"remedy decision resolve {job_id} plan:approval --reason approve")
        ctx.next_lines.append(f"remedy job run {job_id}{_job_run_role_flags(ctx)}")
    return DO_STEP_STOPPED, (
        f"--rehearse: no job was run and nothing was written to the repository; "
        f"{len(ctx.job_ids)} job(s) rehearsed, mission plan: {ctx.mission_plan_path}"
        f"; rehearsal summaries: {', '.join(summary_paths)}")


def _format_usd_band(low: float | None, high: float | None) -> str:
    """Four decimals, or "not available" when either bound is unmeasured (P6: never a guess)."""
    if low is None or high is None:
        return "not available"
    return f"{low:.4f}–{high:.4f}"


def _planner_cost(trace_entries: list[dict]) -> dict[str, Any]:
    """The planning calls a job's own prompt trace recorded — never a dollar figure (DECISION
    F055 D2 (2)): no planning call records the answer's tokens or a price."""
    calls = len(trace_entries)
    roles = sorted({str(e.get("role", "")) for e in trace_entries if e.get("role")})
    prompt_chars = sum(int(e.get("prompt_chars", 0) or 0) for e in trace_entries)
    prompt_tokens_estimated = sum(
        int(e.get("prompt_tokens_estimated", 0) or 0) for e in trace_entries)
    if calls == 0:
        basis = "No planning call was made for this job: its plan is deterministic."
    else:
        basis = (
            f"{calls} planning call(s) recorded in the job's prompt trace ({', '.join(roles)}): "
            f"about {prompt_tokens_estimated} prompt tokens, estimated from {prompt_chars} prompt characters. "
            + "The answers' tokens and the price of these calls are not recorded, so no cost in dollars is claimed. The study and the mission's own plan are not counted here.")
    return {
        "calls": calls, "roles": roles, "prompt_chars": prompt_chars,
        "prompt_tokens_estimated": prompt_tokens_estimated, "basis": basis,
    }


def _task_rows(job: Any, predictive_config: Any) -> list[dict[str, Any]]:
    """One row per task: its plan band, the token band it maps to, and the estimator's band —
    the same per-task reading `subtree_rerun_cost_estimate` uses (DECISION F055 D2 (3))."""
    from packages.orchestration.cost_preview import ESTIMATE_UNAVAILABLE, estimate_cost_band
    from packages.orchestration.task_injection import PLAN_BAND_TO_TOKEN_BAND

    rows: list[dict[str, Any]] = []
    for task in job.tasks:
        plan = task.inputs.get("plan") if isinstance(task.inputs, dict) else None
        plan_band = (plan or {}).get("est_tokens_band") or ""
        token_band = PLAN_BAND_TO_TOKEN_BAND.get(plan_band) if plan_band else None
        if token_band is not None:
            estimate = estimate_cost_band(token_band, token_band, config=predictive_config)
            band_usd_low, band_usd_high, basis = (
                estimate.band_usd_low, estimate.band_usd_high, estimate.basis)
        else:
            band_usd_low, band_usd_high, basis = None, None, ESTIMATE_UNAVAILABLE
        rows.append({
            "task_id": task.task_id, "title": task.title, "plan_band": plan_band,
            "token_band": token_band or "", "band_usd_low": band_usd_low,
            "band_usd_high": band_usd_high, "basis": basis,
        })
    return rows


def _estimate_total(job: Any, predictive_config: Any) -> dict[str, Any]:
    """The whole job's band, through the shared subtree estimator — untouched (DECISION F055 D2
    (3)): one unpriced task makes the whole figure unavailable, never half-guessed."""
    from packages.orchestration.subtree_rerun import subtree_rerun_cost_estimate

    subtree_ids = [t.task_id for t in job.tasks]
    estimate = subtree_rerun_cost_estimate(job, subtree_ids, config=predictive_config)
    return {
        "band_usd_low": estimate.band_usd_low, "band_usd_high": estimate.band_usd_high,
        "basis": estimate.basis,
    }


def _risks(job: Any) -> list[str] | None:
    """The task plan's risks, or `None` — distinct from an empty list — when the job has no
    task plan from the planner (a deterministic plan, DECISION F055 D2 (4))."""
    task_plan = job.task_plan if isinstance(job.task_plan, dict) else None
    if task_plan is None:
        return None
    return list(task_plan.get("risks") or [])


def _normalization(job: Any) -> list[dict[str, Any]]:
    """The task plan's normalization record, as `job.task_plan["_normalization"]` holds it."""
    task_plan = job.task_plan if isinstance(job.task_plan, dict) else None
    if task_plan is None:
        return []
    return list(task_plan.get("_normalization") or [])


def _dod_section(dod: Any) -> dict[str, Any]:
    """`present`, `compiled` (`None` without a DoD), every check, and which were not compiled
    (DECISION F055 D2 (5))."""
    if dod is None:
        return {"present": False, "compiled": None, "checks": [], "not_compiled": []}
    checks = [
        {"id": c.id, "kind": c.kind, "blocking": c.blocking, "source": c.source}
        for c in dod.checks
    ]
    not_compiled = [c["id"] for c in checks if c["source"] != "compiled"]
    return {
        "present": True, "compiled": dod.compiled, "checks": checks,
        "not_compiled": not_compiled,
    }


def _fences_section(job: Any, fence_spec: Any, fence_error: str) -> dict[str, Any]:
    """Every path of every task's `files_hint`, in first-appearance order, checked against the
    effective fence (DECISION F055 D2 (6)); a config that cannot be read is named instead."""
    from packages.orchestration.scope_fences import check_path

    if fence_error:
        return {
            "scope_undeclared": False, "would_write": [], "would_block": [], "error": fence_error,
        }

    paths: list[str] = []
    seen: set[str] = set()
    for task in job.tasks:
        for path in task.files_hint or []:
            if path not in seen:
                seen.add(path)
                paths.append(path)

    if not paths:
        return {"scope_undeclared": True, "would_write": [], "would_block": [], "error": ""}

    worktree_root = Path(job.repo_path or ".")
    would_write: list[str] = []
    would_block: list[dict[str, str]] = []
    for path in paths:
        result = check_path(path, worktree_root, fence_spec)
        if result.allowed:
            would_write.append(path)
        else:
            would_block.append({"path": path, "reason": result.reason})
    return {
        "scope_undeclared": False, "would_write": would_write, "would_block": would_block,
        "error": "",
    }


def _next_lines(job: Any) -> list[str]:
    """The approval line when the job's task plan waits for approval, then the run line —
    without role flags, which only a live walk's `DoContext` carries."""
    from packages.orchestration.job_plan import task_plan_blocks_execution

    lines: list[str] = []
    if task_plan_blocks_execution(job) is not None:
        lines.append(f"remedy decision resolve {job.job_id} plan:approval --reason approve")
    lines.append(f"remedy job run {job.job_id}")
    return lines


# WHY: the record answers exactly what a rehearsal may know without running anything — PURE,
# so a golden file can hold its rendered summary byte for byte (DECISION F055 D2).
def build_job_rehearsal(
    job: Any,
    *,
    trace_entries: list[dict],
    dod: Any,
    predictive_config: Any,
    fence_spec: Any,
    fence_error: str,
    repo_head: str,
    rehearsed_at: str,
) -> dict[str, Any]:
    """The `rehearsal_v1` record: what planning cost, what the run would cost and risk, the
    definition of done, and which files the run could write — nothing run, nothing guessed."""
    return {
        "schema_v": REHEARSAL_SCHEMA_V,
        "job_id": str(job.job_id),
        "rehearsed_at": rehearsed_at,
        "repo_path": job.repo_path,
        "repo_head": repo_head,
        "planner_cost": _planner_cost(trace_entries),
        "tasks": _task_rows(job, predictive_config),
        "estimate_total": _estimate_total(job, predictive_config),
        "risks": _risks(job),
        "normalization": _normalization(job),
        "dod": _dod_section(dod),
        "fences": _fences_section(job, fence_spec, fence_error),
        "next": _next_lines(job),
    }


# WHY: the readable twin of `build_job_rehearsal`'s record — PURE, so the golden fixture is
# exactly this function's own output, never hand-typed prose that can drift from the code.
def render_rehearsal_summary(record: dict[str, Any]) -> str:
    """The `rehearsal.md` markdown rendered from `build_job_rehearsal`'s record."""
    lines: list[str] = []
    lines.append(f"# Rehearsal of job {record['job_id']}")
    lines.append("")
    repo_head = record["repo_head"] or "unknown"
    lines.append(
        f"Rehearsed at {record['rehearsed_at']} on {record['repo_path']} at commit "
        f"{repo_head}. No job was run, no builder or reviewer was built, nothing was applied, "
        f"and nothing was written to the repository.")
    lines.append("")

    lines.append("## What planning cost")
    lines.append("")
    lines.append(record["planner_cost"]["basis"])
    lines.append("")

    lines.append("## What the run would cost")
    lines.append("")
    lines.append("| Task | Title | Plan band | Estimate in USD |")
    lines.append("|---|---|---|---|")
    for task in record["tasks"]:
        band = task["plan_band"] or "none"
        estimate = _format_usd_band(task["band_usd_low"], task["band_usd_high"])
        lines.append(f"| {task['task_id']} | {task['title']} | {band} | {estimate} |")
    lines.append("")
    total = record["estimate_total"]
    whole = _format_usd_band(total["band_usd_low"], total["band_usd_high"])
    whole_text = f"{whole} USD" if whole != "not available" else whole
    lines.append(f"Whole job: {whole_text}. Basis: {total['basis']}.")
    lines.append("")

    lines.append("## Risks")
    lines.append("")
    risks = record["risks"]
    if risks is None:
        lines.append(
            "No task plan from the planner: the plan is deterministic and names no risk.")
    elif not risks:
        lines.append("The plan names no risk.")
    else:
        for risk in risks:
            lines.append(f"- {risk}")
    lines.append("")
    normalization = record["normalization"]
    if not normalization:
        lines.append("Normalization: changed nothing.")
    else:
        lines.append("Normalization:")
        for entry in normalization:
            sources = ", ".join(entry.get("source_ids", [])) or "-"
            results = ", ".join(entry.get("result_ids", [])) or "-"
            lines.append(
                f"- {entry.get('kind', 'unknown')} {sources} → {results}: "
                f"{entry.get('reason', '')}")
    lines.append("")

    lines.append("## Definition of done")
    lines.append("")
    dod = record["dod"]
    if not dod["present"]:
        lines.append("No definition of done is recorded for this job.")
    else:
        lines.append("| Check | Kind | Blocking | Source |")
        lines.append("|---|---|---|---|")
        for check in dod["checks"]:
            blocking = "yes" if check["blocking"] else "no"
            lines.append(f"| {check['id']} | {check['kind']} | {blocking} | {check['source']} |")
        lines.append("")
        if dod["not_compiled"]:
            lines.append(f"Not compiled: {', '.join(dod['not_compiled'])}.")
        else:
            lines.append("Every check was compiled.")
    lines.append("")

    lines.append("## What the run could write")
    lines.append("")
    fences = record["fences"]
    if fences["error"]:
        lines.append(f"The fences could not be read: {fences['error']}")
    elif fences["scope_undeclared"]:
        lines.append("Scope undeclared — the whole worktree is writable under the current fences.")
    else:
        for path in fences["would_write"]:
            lines.append(f"- would write `{path}`")
        for blocked in fences["would_block"]:
            lines.append(f"- would be blocked `{blocked['path']}`: {blocked['reason']}")
    lines.append("")

    lines.append("## To run it for real")
    lines.append("")
    for line in record["next"]:
        lines.append(f"- `{line}`")

    return "\n".join(lines) + "\n"


def _rehearsal_repo_head(repo_path: str) -> str:
    """The target repository's HEAD at rehearsal time, or "" on any failure (no guess, no raise:
    round 3's reuse path compares this, and a rehearsal must never crash on it)."""
    if not repo_path:
        return ""
    try:
        proc = subprocess.run(
            ["git", "-C", repo_path, "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=10, check=True)
    except (OSError, subprocess.SubprocessError):
        return ""
    return proc.stdout.strip()


# WHY: a plan rehearsed against yesterday's repository may no longer match it — this names the
# risk, once, at the two places a stale plan could run, and never refuses: the person decides.
def rehearsal_staleness_warning(job: Any) -> str | None:
    """One sentence when the target's HEAD moved since the job's rehearsal, else `None`."""
    rehearsal = job.metadata.get("rehearsal")
    rehearsed = rehearsal.get("repo_head", "") if isinstance(rehearsal, dict) else ""
    if not rehearsed:
        return None
    now = _rehearsal_repo_head(job.repo_path)
    if not now or now == rehearsed:
        return None
    return (f"Warning: job {job.job_id} was rehearsed at commit {rehearsed[:12]}, and its "
            f"repository is now at commit {now[:12]}; the plan may be stale, so check it "
            f"before you run it.")


# WHY: `remedy status` labels a job that still waits on the approval a rehearsal left open, so an
# operator can tell a rehearsed plan from an ordinary one before answering its decision.
def job_waits_after_rehearsal(job: Any) -> bool:
    """True for a `planned` job whose metadata holds a rehearsal record."""
    from packages.core.models import RunState

    return job.state == RunState.PLANNED and "rehearsal" in job.metadata


def _read_trace_entries(path: Path) -> list[dict]:
    """The job's prompt trace: absent file = no entries; an unreadable line is skipped."""
    if not path.is_file():
        return []
    try:
        raw_lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    entries: list[dict] = []
    for raw in raw_lines:
        raw = raw.strip()
        if not raw:
            continue
        try:
            entry = json.loads(raw)
        except ValueError:
            continue
        if isinstance(entry, dict):
            entries.append(entry)
    return entries


# WHY: the one write path a rehearsal takes — everything it reads already exists from planning;
# nothing here builds a provider, applies anything or touches the target (DECISION F055 D2 (1)).
def write_job_rehearsal(job: Any) -> Path:
    """Write `rehearsal.json` and `rehearsal.md` into the job's own evidence folder, and record
    where on the job. Returns the summary's path."""
    from packages.common.secure_fs import durable_write
    from packages.orchestration.budget_resolution import resolve_predictive_budget_config
    from packages.orchestration.data_paths import job_evidence_dir, run_log_dir
    from packages.orchestration.dod_gate import load_dod
    from packages.orchestration.pingpong_job import save_job_plan
    from packages.orchestration.scope_fences import FenceConfigError, FenceSpec, resolve_fence_spec

    job_id = str(job.job_id)
    trace_entries = _read_trace_entries(run_log_dir(job_id) / "prompt_trace.jsonl")
    dod = load_dod(job_id)
    predictive_config = resolve_predictive_budget_config(project_root=job.repo_path)

    job_fences = None
    if job.fences is not None:
        job_fences = {"allow": job.fences.allow, "deny": job.fences.deny}
    fence_error = ""
    try:
        fence_spec = resolve_fence_spec(Path(job.repo_path or "."), job_fences=job_fences)
    except FenceConfigError as exc:
        fence_spec = FenceSpec()
        fence_error = str(exc)

    repo_head = _rehearsal_repo_head(job.repo_path)
    rehearsed_at = datetime.now(timezone.utc).isoformat()

    record = build_job_rehearsal(
        job, trace_entries=trace_entries, dod=dod, predictive_config=predictive_config,
        fence_spec=fence_spec, fence_error=fence_error, repo_head=repo_head,
        rehearsed_at=rehearsed_at)
    summary = render_rehearsal_summary(record)

    evidence_dir = job_evidence_dir(job_id)
    evidence_dir.mkdir(parents=True, exist_ok=True)
    json_path = evidence_dir / "rehearsal.json"
    md_path = evidence_dir / "rehearsal.md"
    durable_write(json_path, json.dumps(record, indent=2) + "\n")
    durable_write(md_path, summary)

    job.metadata["rehearsal"] = {
        "rehearsed_at": rehearsed_at, "repo_head": repo_head, "record": "rehearsal.json",
    }
    save_job_plan(job)
    return md_path

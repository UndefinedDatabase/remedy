"""The `run` command handlers: `remedy run show` and `remedy run list` (DECISION F058 D3).

The three functions below moved unchanged out of `apps/cli/commands/do_cmd.py`, whose
`COMMAND_HANDLERS` imports them back by name.
"""

from __future__ import annotations

from apps.cli.json_envelope import emit_ok, fail
from packages.orchestration.model_failover import failover_report_line
from packages.orchestration.tier_escalation import escalation_report_lines


def _cmd_run_show(
    run_id: str,
    *,
    json_output: bool = False,
) -> None:
    """Show a persisted ping-pong run report."""
    from packages.orchestration.pingpong_loop import load_run

    data = load_run(run_id)
    if data is None:
        fail("run_not_found", f"No run matches {run_id!r}. Try: remedy run list.",
             json_output=json_output)

    if json_output:
        emit_ok(**data)
    else:
        _print_text_report(run_id, data)


def _cmd_run_list(
    *,
    json_output: bool = False,
    sort: str | None = None,
    desc: bool = False,
    since: str | None = None,
    until: str | None = None,
    limit: str | None = None,
) -> None:
    """List persisted ping-pong runs.

    `list_runs()` already orders by run directory, so `default_sort_field` is None and a call
    with no list flag returns its rows untouched: the payload `do report list` printed.
    """
    from packages.orchestration.list_options import ListOptionError, apply_list_options
    from packages.orchestration.pingpong_loop import list_runs

    try:
        runs = apply_list_options(
            list_runs(),
            sort=sort, desc=desc, since=since, until=until, limit=limit,
            sort_fields={
                "run_id": lambda r: r.get("run_id", ""),
                "goal": lambda r: r.get("goal", ""),
                "status": lambda r: r.get("status", ""),
                "finished_at": lambda r: r.get("finished_at", ""),
            },
            date_getter=lambda r: r.get("finished_at") or None,
        )
    except ListOptionError as exc:
        fail("invalid_list_option", str(exc), json_output=json_output)

    if json_output:
        emit_ok(runs=runs)
        return
    if not runs:
        print("No ping-pong runs found.")
        return
    for r in runs:
        print(f"  {r['run_id']}  {r['status']:<24s}  {r['goal']}")


def _print_text_report(run_id: str, data: dict) -> None:
    """Print concise user-facing text report."""
    # Header
    print(f"Remedy Run {run_id}")
    print(f"Goal: {data.get('goal', '')}")
    print(f"Status: {data.get('final_status', '')}")
    print()

    # Task input info
    ti = data.get("task_input")
    if ti:
        kind_label = ti.get("kind", "")
        title = ti.get("title", "")
        sha = ti.get("sha256", "")[:12]
        tokens = ti.get("tokens_estimated", 0)
        print(f"Task input: {kind_label}" + (f" ({title})" if title else ""))
        print(f"Task text size: ~{tokens} tokens (an estimate of the task text, not usage)")
        print(f"Task hash: {sha}...")
        print()

    # Provider evidence
    pe = data.get("provider_evidence", {})
    if pe:
        b_kind = pe.get("builder_provider_kind", "")
        r_kind = pe.get("reviewer_provider_kind", "")
        b_wm = pe.get("builder_write_mode", "none")
        r_wm = pe.get("reviewer_write_mode", "none")
        b_label = f"{data.get('builder_provider', 'unknown')} ({b_kind}, write mode: {b_wm})" if b_kind else data.get("builder_provider", "unknown")
        r_label = f"{data.get('reviewer_provider', 'unknown')} ({r_kind}, write mode: {r_wm})" if r_kind else data.get("reviewer_provider", "unknown")
        print(f"Builder: {b_label}")
        print(f"Reviewer: {r_label}")
    else:
        print(f"Builder: {data.get('builder_provider', 'unknown')}")
        print(f"Reviewer: {data.get('reviewer_provider', 'unknown')}")

    for line in (failover_report_line(data), *escalation_report_lines(data)):
        if line is not None:
            print(line)

    # Rounds summary
    rounds = data.get("rounds", [])
    total = data.get("total_rounds", len(rounds))
    max_r = data.get("max_rounds", 0)
    print(f"Rounds: {total}/{max_r}")

    # Worker self-report vs Remedy verification (Step 4718)
    if rounds:
        last = rounds[-1]
        builder_info = last.get("builder", {})
        if builder_info:
            summary = builder_info.get("summary", "")
            if summary:
                print(f"\nWorker self-report: {summary[:200]}")

        # No test in this run is no failed test: a `remedy do` job runs them in its own verification.
        test_status = {None: "not run in this run", True: "passed"}.get(last.get("test_passed"), "failed")
        print(f"Remedy verification: tests {test_status}")
        rv = last.get("reviewer", {})
        if rv:
            print(f"Reviewer verdict: {rv.get('verdict', 'none')}")

    # Target mutation
    mutated = data.get("target_mutated", False)
    print(f"Target touched during run: {'yes' if mutated else 'no'}")

    if data.get("error"):
        print(f"Error: {data['error']}")

    # Staged files
    staged = data.get("staged_files", [])
    if staged:
        print("\nChanged in staging:")
        for f in staged:
            print(f"  - {f}")

    # Token accounting
    ta = data.get("token_accounting", {})
    if ta:
        kind = ta.get("kind", "estimated")
        print(f"\nToken accounting: {kind}")
        # exec-1017 D3: the measured usage comes first; the initial prompt's estimate is never shown
        # alone under "actual" (on 2026-10-17 this page said ~210 beside 230,803 measured).
        for role, used in sorted(((ta.get("usage_actuals") or {}).get("by_role") or {}).items()):
            print(f"  {role} used: {used.get('input_tokens')} input, {used.get('output_tokens')} output "
                  f"tokens over {used.get('provider_call_count')} call(s) (measured)")
        ctx_est = ta.get("context_tokens_estimated", 0)
        if ctx_est:
            print(f"  Initial context sent: ~{ctx_est} tokens (an estimate of the first prompt; an agent "
                  "loop resends it and its history every turn)")
        full_est = ta.get("full_repo_tokens_estimated", 0)
        if full_est:
            print(f"  Full repo estimate: ~{full_est} tokens")
        savings = ta.get("estimated_context_savings_tokens", 0)
        ratio = ta.get("estimated_context_savings_ratio", 0.0)
        if savings > 0:
            pct = int(ratio * 100)
            print(f"  Estimated saved: ~{savings} tokens (~{pct}%)")
        if ta.get("token_note"):
            print(f"  Note: {ta['token_note']}")

"""CLI handlers for ``remedy dogfood`` — open-ended dogfood run orchestrator.

All handlers are read-only or write-metadata-only. No provider execution, no
auto-apply, no git/PR automation, no subprocess, no shell.
"""

from __future__ import annotations

import json
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import argparse


def _cmd_dogfood_create(args: Any) -> None:
    """Create a new open-ended dogfood run for a job."""
    from packages.orchestration.dogfood_run import (
        DogfoodRunPolicy,
        create_dogfood_run,
    )
    policy = DogfoodRunPolicy(
        max_steps=int(getattr(args, "max_steps", None) or 100),
        max_tokens_estimated=int(getattr(args, "max_tokens", None) or 500_000),
        max_wall_minutes=int(getattr(args, "max_wall_minutes", None) or 480),
    )
    run = create_dogfood_run(args.job_id, policy=policy)
    data = run.to_dict()
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Created dogfood run: {run.run_id}")
    print(f"  job: {run.job_id[:8]}  status: {run.status}")
    print(f"  policy: {run.policy.max_steps} steps, {run.policy.max_tokens_estimated} tokens, "
          f"{run.policy.max_wall_minutes} min")


def _cmd_dogfood_show(args: Any) -> None:
    """Show details of a dogfood run."""
    from packages.orchestration.dogfood_run import load_dogfood_run
    run = load_dogfood_run(args.run_id, args.job_id)
    if run is None:
        print(f"Run not found: {args.run_id}", file=sys.stderr)
        sys.exit(1)
    data = run.to_dict()
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Dogfood run: {run.run_id}")
    print(f"  job: {run.job_id[:8]}  status: {run.status}")
    print(f"  steps: {run.step_count}/{run.policy.max_steps}  "
          f"tokens: {run.cumulative_tokens}/{run.policy.max_tokens_estimated}")
    if run.current_lane:
        print(f"  lane: {run.current_lane}")
    if run.last_action:
        print(f"  last: {run.last_action}")
    if run.next_suggested_action:
        print(f"  next: {run.next_suggested_action}")
    if run.blocking_reasons:
        print(f"  blockers: {', '.join(run.blocking_reasons)}")


def _cmd_dogfood_status(args: Any) -> None:
    """List all dogfood runs with status summary."""
    from packages.orchestration.dogfood_run import list_dogfood_runs
    job_id = getattr(args, "job_id", None) or None
    runs = list_dogfood_runs(job_id=job_id)
    if getattr(args, "json", False):
        print(json.dumps(runs, indent=2))
        return
    if not runs:
        print("No dogfood runs found.")
        return
    for r in runs:
        rid = r.get("run_id", "?")
        jid = str(r.get("job_id", ""))[:8]
        status = r.get("status", "?")
        steps = r.get("step_count", 0)
        print(f"  {rid}  job={jid}  status={status}  steps={steps}")


def _cmd_dogfood_step(args: Any) -> None:
    """Execute one step of a dogfood run."""
    from packages.orchestration.dogfood_run import load_dogfood_run, step_dogfood_run
    run = load_dogfood_run(args.run_id, args.job_id)
    if run is None:
        print(f"Run not found: {args.run_id}", file=sys.stderr)
        sys.exit(1)
    run, cp = step_dogfood_run(run)
    data = cp.to_dict()
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Step {cp.step_index}: lane={cp.lane}  action={cp.action_taken}")
    print(f"  outcome: {cp.outcome}")
    print(f"  status: {cp.run_status}")
    if cp.next_suggested_action and cp.next_suggested_action != "none":
        print(f"  next: {cp.next_suggested_action}")
    if cp.blocking_reasons:
        print(f"  blockers: {', '.join(cp.blocking_reasons)}")


def _cmd_dogfood_stop(args: Any) -> None:
    """Stop a dogfood run."""
    from packages.orchestration.dogfood_run import load_dogfood_run, stop_dogfood_run
    run = load_dogfood_run(args.run_id, args.job_id)
    if run is None:
        print(f"Run not found: {args.run_id}", file=sys.stderr)
        sys.exit(1)
    reason = getattr(args, "reason", None) or "operator_stop"
    run = stop_dogfood_run(run, reason=reason)
    if getattr(args, "json", False):
        print(json.dumps(run.to_dict(), indent=2))
        return
    print(f"Stopped run {run.run_id}: {run.stop_reason}")


def _cmd_dogfood_replay(args: Any) -> None:
    """Replay analysis of a dogfood run."""
    from packages.orchestration.dogfood_run import analyze_dogfood_run_replay
    analysis = analyze_dogfood_run_replay(args.run_id, args.job_id)
    data = analysis.to_dict()
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Replay: {analysis.run_id}  status={analysis.run_status}")
    print(f"  steps: {analysis.total_steps}  tokens: {analysis.total_tokens}  "
          f"wall: {analysis.wall_elapsed_seconds:.0f}s")
    if analysis.lane_summaries:
        print("  lanes:")
        for ls in analysis.lane_summaries:
            print(f"    {ls.lane}: {ls.step_count} steps (#{ls.first_step}-#{ls.last_step})")
    if analysis.blocking_episodes:
        print(f"  blocking episodes: {len(analysis.blocking_episodes)}")
    if analysis.anomalies:
        print(f"  anomalies: {', '.join(analysis.anomalies)}")
    if analysis.next_actions:
        print("  next actions:")
        for na in analysis.next_actions:
            print(f"    - {na.get('action', '?')} ({na.get('lane', '?')})")


def _cmd_dogfood_checkpoints(args: Any) -> None:
    """Show raw checkpoint log."""
    from packages.orchestration.dogfood_run import load_checkpoints
    cps = load_checkpoints(args.run_id, args.job_id)
    if getattr(args, "json", False):
        print(json.dumps([cp.to_dict() for cp in cps], indent=2))
        return
    if not cps:
        print("No checkpoints.")
        return
    for cp in cps:
        print(f"  #{cp.step_index} [{cp.lane}] {cp.action_taken} -> {cp.outcome} ({cp.run_status})")


def _cmd_dogfood_next(args: Any) -> None:
    """Show what the next step would do (dry-run, no mutation)."""
    from packages.orchestration.dogfood_run import evaluate_dogfood_run, load_dogfood_run
    run = load_dogfood_run(args.run_id, args.job_id)
    if run is None:
        print(f"Run not found: {args.run_id}", file=sys.stderr)
        sys.exit(1)
    ev = evaluate_dogfood_run(run)
    data = ev.to_dict()
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Next step (dry-run): {run.run_id}  status={ev.status}")
    print(f"  lane: {ev.active_lane}")
    print(f"  budget: {ev.budget_remaining_steps} steps, "
          f"{ev.budget_remaining_tokens} tokens, "
          f"{ev.budget_remaining_wall_minutes:.0f} min")
    if ev.next_actions:
        print("  would do:")
        for na in ev.next_actions:
            print(f"    - {na.get('action', '?')}: {na.get('reason', '?')}")
    if ev.blocking_reasons:
        print(f"  blockers: {', '.join(ev.blocking_reasons)}")


def _cmd_dogfood_evaluate(args: Any) -> None:
    """Evaluate run state without stepping."""
    from packages.orchestration.dogfood_run import evaluate_dogfood_run, load_dogfood_run
    run = load_dogfood_run(args.run_id, args.job_id)
    if run is None:
        print(f"Run not found: {args.run_id}", file=sys.stderr)
        sys.exit(1)
    ev = evaluate_dogfood_run(run)
    data = ev.to_dict()
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Evaluation: {run.run_id}  status={ev.status}  satisfied={ev.satisfied}")
    if ev.evidence:
        print("  evidence:")
        for k, v in ev.evidence.items():
            print(f"    {k}: {v}")


def _cmd_dogfood_brainstorm(args: Any) -> None:
    """List brainstorm ideas for a run (metadata-only)."""
    from packages.orchestration.dogfood_run import list_brainstorm_ideas
    ideas = list_brainstorm_ideas(args.run_id, args.job_id)
    if getattr(args, "json", False):
        print(json.dumps(ideas, indent=2))
        return
    if not ideas:
        print("No brainstorm ideas recorded.")
        return
    for idea in ideas:
        print(f"  [{idea.get('priority', '?')}] {idea.get('title', '?')} ({idea.get('status', '?')})")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "dogfood.create": _cmd_dogfood_create,
    "dogfood.show": _cmd_dogfood_show,
    "dogfood.status": _cmd_dogfood_status,
    "dogfood.step": _cmd_dogfood_step,
    "dogfood.stop": _cmd_dogfood_stop,
    "dogfood.replay": _cmd_dogfood_replay,
    "dogfood.checkpoints": _cmd_dogfood_checkpoints,
    "dogfood.next": _cmd_dogfood_next,
    "dogfood.evaluate": _cmd_dogfood_evaluate,
    "dogfood.brainstorm": _cmd_dogfood_brainstorm,
}

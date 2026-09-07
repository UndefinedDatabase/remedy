"""The `context.explain` and `context.optimize` handlers, split out of `context.py`.

WHY THIS FILE EXISTS. `packages.orchestration.context_optimizer` is one of the twenty-four
prototype-cluster modules F260's Design deletes. While these two handlers sat in
`apps/cli/commands/context.py` — which also hosts the SURVIVING `context.inspect` — that file
was a surviving CONSUMER of the cluster, and its import was an edge the deletion had to cut
first. This file is instead listed in `CLUSTER_COMMAND_HANDLERS` in
`tests/orchestration/test_cluster_deletion_map.py`, so it dies WITH the module rather than
blocking it.

Remedy deliberately does NOT put these two beside `context.pack` in `context_pack_cmd.py`, even
though all three left the same file in the same round: they are built on a DIFFERENT cluster
module. One file per cluster module is what lets each module be deleted on its own edge instead
of waiting for the other's consumers to be cut too.

The command ids `context.explain` and `context.optimize` are UNCHANGED. This is a move, not a
rename; renaming commands is F261's work.
"""

from __future__ import annotations

import json as _json
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING
from uuid import UUID

from packages.orchestration.storage import JobNotFoundError, load_job

if TYPE_CHECKING:
    import argparse


def _cmd_context_explain(
    job_id_str: str,
    *,
    mode: str = "compact",
    budget: int = 2000,
    json_output: bool = False,
) -> None:
    try:
        job_id = UUID(job_id_str)
    except ValueError:
        print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
        sys.exit(1)
    try:
        job = load_job(job_id)
    except JobNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    from packages.orchestration.context_optimizer import explain_context
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.timeline import load_run_events

    data_dir = resolve_data_root()
    events = load_run_events(data_dir, job.id)
    data = explain_context(job, events, mode=mode, budget=budget)

    if json_output:
        print(_json.dumps(data, sort_keys=True))
    else:
        print(f"Context Explain: {data['job_id'][:8]} (mode={data['mode']}, budget={data['budget']})")
        print(f"  Estimated tokens: {data['estimated_tokens']}")
        for s in data["sections"]:
            inc = "included" if s["included"] else "excluded"
            print(f"  {s['id']}: ~{s['estimated_tokens']}t [{inc}] — {s['reason']}")
        for s in data.get("excluded", []):
            print(f"  {s['id']}: ~{s['estimated_tokens']}t [excluded] — {s['reason']}")
        if data.get("recommendations"):
            print("  Recommendations:")
            for r in data["recommendations"]:
                print(f"    -> {r}")


def _cmd_context_optimize(
    job_id_str: str,
    *,
    budget: int = 2000,
    json_output: bool = False,
) -> None:
    try:
        job_id = UUID(job_id_str)
    except ValueError:
        print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
        sys.exit(1)
    try:
        job = load_job(job_id)
    except JobNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    from packages.orchestration.context_optimizer import optimize_context
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.run_log import RunLogWriter
    from packages.orchestration.timeline import load_run_events

    data_dir = resolve_data_root()
    events = load_run_events(data_dir, job.id)
    data = optimize_context(job, events, budget=budget)

    # Emit context_budget_optimized event
    log = RunLogWriter(job_id=job.id)
    log.log(
        "context_budget_optimized",
        mode=data["recommended_mode"],
        budget=data["budget"],
        estimated_tokens=data["estimated_tokens"],
        token_savings=data["token_savings"],
        recommended_worker=data["recommended_worker"],
        included_section_count=len(data["included_sections"]),
        excluded_section_count=len(data["excluded_sections"]),
    )

    if json_output:
        print(_json.dumps(data, sort_keys=True))
    else:
        print(f"Context Optimize: {data['job_id'][:8]} (budget={data['budget']})")
        print(f"  Recommended mode: {data['recommended_mode']}")
        print(f"  Estimated tokens: {data['estimated_tokens']}")
        print(f"  Token savings: {data['token_savings']}")
        print(f"  Worker: {data['recommended_worker']}")
        print(f"  Included: {', '.join(data['included_sections'])}")
        if data["excluded_sections"]:
            print(f"  Excluded: {', '.join(data['excluded_sections'])}")
        if data.get("recommendations"):
            for r in data["recommendations"]:
                print(f"    -> {r}")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "context.explain": lambda args: _cmd_context_explain(
        args.job_id,
        mode=getattr(args, "mode", "compact"),
        budget=int(getattr(args, "budget", "2000")),
        json_output=getattr(args, "json", False),
    ),
    "context.optimize": lambda args: _cmd_context_optimize(
        args.job_id,
        budget=int(getattr(args, "budget", "2000")),
        json_output=getattr(args, "json", False),
    ),
}

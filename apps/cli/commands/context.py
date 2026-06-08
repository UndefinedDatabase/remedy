"""Context group command handlers."""

from __future__ import annotations

import json as _json
import sys
from typing import TYPE_CHECKING, Callable
from uuid import UUID

from packages.orchestration.storage import JobNotFoundError, load_job

if TYPE_CHECKING:
    import argparse


def _cmd_context_pack(
    job_id_str: str,
    *,
    budget: int = 2000,
    mode: str = "compact",
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

    from packages.orchestration.context_pack import (
        build_context_pack, export_context_pack_json, summarize_context_pack,
    )
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.run_log import RunLogWriter
    from packages.orchestration.timeline import load_run_events

    data_dir = resolve_data_root()
    events = load_run_events(data_dir, job.id)
    pack = build_context_pack(job, events, budget=budget, mode=mode)

    if json_output:
        print(_json.dumps(export_context_pack_json(pack), sort_keys=True))
    else:
        print(summarize_context_pack(pack))

    log = RunLogWriter(job_id=job.id)
    log.log(
        "context_pack_created",
        budget=pack.budget,
        estimated_tokens=pack.estimated_tokens,
        mode=pack.mode,
        truncated=pack.truncated,
        section_count=len(pack.sections),
    )


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
            print(f"  Recommendations:")
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


def _cmd_context_inspect(
    job_id_str: str,
    *,
    task_id: str | None = None,
    budget: int = 4000,
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

    if task_id is not None:
        try:
            UUID(task_id)
        except ValueError:
            print(f"Error: invalid task ID: {task_id!r}", file=sys.stderr)
            sys.exit(1)

    from packages.orchestration.context_inspector import (
        export_context_inspection_json,
        inspect_context,
        summarize_context_inspection,
    )
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.timeline import load_run_events

    data_dir = resolve_data_root()
    events = load_run_events(data_dir, job.id)
    inspection = inspect_context(
        job, events,
        task_id=task_id,
        budget_tokens=budget,
    )

    if json_output:
        print(_json.dumps(export_context_inspection_json(inspection), sort_keys=True))
    else:
        print(summarize_context_inspection(inspection))


COMMAND_HANDLERS: dict[str, Callable[["argparse.Namespace"], None]] = {
    "context.inspect": lambda args: _cmd_context_inspect(
        args.job_id,
        task_id=getattr(args, "task_id", None),
        budget=int(getattr(args, "budget", "4000")),
        json_output=getattr(args, "json", False),
    ),
    "context.pack": lambda args: _cmd_context_pack(
        args.job_id,
        budget=int(getattr(args, "budget", "2000")),
        mode=getattr(args, "mode", "compact"),
        json_output=args.json,
    ),
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

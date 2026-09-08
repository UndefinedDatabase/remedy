"""The `worker.recommend` and `worker.explain` handlers, split out of `worker.py`.

WHY THIS FILE EXISTS. `packages.orchestration.worker_recommend` is one of the twenty-four
prototype-cluster modules F260's Design deletes. While these two handlers sat in
`apps/cli/commands/worker.py` — which also hosts the SURVIVING `worker.list`, `worker.show`,
`worker.resources`, `worker.unload`, `worker.run` and `worker.status` — that file was a
surviving CONSUMER of the cluster, and its import was an edge the deletion had to cut first.
This file is instead listed in `CLUSTER_COMMAND_HANDLERS` in
`tests/orchestration/test_cluster_deletion_map.py`, so it dies WITH the module rather than
blocking it.

WHAT THIS CUT DOES NOT BUY, measured against `tests/orchestration/cluster_deletion_map.txt`
rather than assumed: it does NOT make `worker_recommend` deletable. Three
`packages/orchestration/` consumers still reach it — `agent_loop.py`, `autonomy_loop.py` and
`dashboard.py` — and the map keeps their three edges. One edge of four is gone, not the module.

The command ids `worker.recommend` and `worker.explain` are UNCHANGED. This is a move, not a
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


def _cmd_worker_recommend(job_id_str: str, *, json_output: bool = False) -> None:
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

    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.timeline import load_run_events
    from packages.orchestration.worker_recommend import (
        export_worker_recommendation_json,
        recommend_worker,
        summarize_worker_recommendation,
    )

    data_dir = resolve_data_root()
    events = load_run_events(data_dir, job_id)
    rec = recommend_worker(job, events)

    if json_output:
        print(_json.dumps(export_worker_recommendation_json(rec), sort_keys=True))
    else:
        print(summarize_worker_recommendation(rec))


def _cmd_worker_explain(job_id_str: str, *, json_output: bool = False) -> None:
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

    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.timeline import load_run_events
    from packages.orchestration.worker_recommend import (
        export_worker_recommendation_json,
        recommend_worker,
    )

    data_dir = resolve_data_root()
    events = load_run_events(data_dir, job_id)
    rec = recommend_worker(job, events)

    if json_output:
        out = export_worker_recommendation_json(rec)
        out["explanation"] = [
            f"{c.provider_id}: score={c.score} ({c.reason})"
            for c in rec.candidates
        ]
        print(_json.dumps(out, sort_keys=True))
    else:
        print(f"Worker Recommendation Explanation for {rec.job_id[:8]}")
        print(f"  Selected: {rec.recommended_worker}")
        print(f"  Token mode: {rec.token_mode}")
        print(f"  Requires approval: {rec.requires_approval}")
        print("\n  Scoring breakdown:")
        for c in rec.candidates:
            marker = ">>>" if c.provider_id == rec.recommended_worker else "   "
            print(f"  {marker} {c.provider_id}: score={c.score} ({c.reason})")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "worker.recommend": lambda args: _cmd_worker_recommend(args.job_id, json_output=args.json),
    "worker.explain": lambda args: _cmd_worker_explain(args.job_id, json_output=args.json),
}

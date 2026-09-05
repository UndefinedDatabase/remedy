"""Worker group command handlers."""

from __future__ import annotations

import json as _json
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING
from uuid import UUID

from packages.orchestration.storage import JobNotFoundError, load_job

if TYPE_CHECKING:
    import argparse


def _cmd_workers(
    *,
    json_output: bool = False,
    sort: str | None = None,
    desc: bool = False,
    since: str | None = None,
    until: str | None = None,
    limit: str | None = None,
) -> None:
    from packages.orchestration.list_options import ListOptionError, apply_list_options
    from packages.orchestration.worker_adapters import (
        export_worker_specs_json,
        list_worker_specs,
        summarize_worker_specs,
    )

    specs = list_worker_specs()
    try:
        specs = apply_list_options(
            specs,
            sort=sort, desc=desc, since=since, until=until, limit=limit,
            sort_fields={
                "provider_id": lambda s: s.provider_id,
                "display_name": lambda s: s.display_name,
                "status": lambda s: s.status,
            },
            default_sort_field=None,
            date_getter=None,
        )
    except ListOptionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if json_output:
        print(_json.dumps(export_worker_specs_json(specs), sort_keys=True))
    else:
        print(summarize_worker_specs(specs))


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


def _cmd_worker_show(provider_id: str, *, json_output: bool = False) -> None:
    from packages.orchestration.worker_adapters import (
        export_worker_specs_json,
        list_worker_specs,
    )

    specs = list_worker_specs()
    match = next((s for s in specs if s.provider_id == provider_id), None)
    if match is None:
        print(f"Error: unknown provider: {provider_id}", file=sys.stderr)
        sys.exit(1)
    if json_output:
        print(_json.dumps(export_worker_specs_json((match,)), sort_keys=True))
    else:
        print(f"Worker: {match.display_name} ({match.provider_id})")
        print(f"  Roles: {', '.join(match.supported_roles)}")
        print(f"  Mode:  {match.execution_mode}")
        print(f"  Status: {match.status}")
        if match.notes:
            print(f"  Notes: {match.notes}")


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


def _cmd_worker_resources(*, json_output: bool = False) -> None:
    """Best-effort GPU/VRAM and loaded model report."""
    import shutil
    import subprocess

    result: dict = {"version": 1, "ollama": None, "gpu": None}

    # Ollama loaded models
    if shutil.which("ollama"):
        try:
            proc = subprocess.run(
                ["ollama", "ps"],
                capture_output=True, text=True, timeout=10,
            )
            lines = proc.stdout.strip().splitlines()
            models = []
            for line in lines[1:]:  # skip header
                parts = line.split()
                if parts:
                    models.append({"name": parts[0], "raw": line.strip()})
            result["ollama"] = {"available": True, "loaded_models": models}
        except (subprocess.TimeoutExpired, OSError):
            result["ollama"] = {"available": True, "error": "ollama ps failed"}
    else:
        result["ollama"] = {"available": False}

    # GPU memory via nvidia-smi
    if shutil.which("nvidia-smi"):
        try:
            proc = subprocess.run(
                ["nvidia-smi", "--query-gpu=memory.used,memory.total,name", "--format=csv,noheader,nounits"],
                capture_output=True, text=True, timeout=10,
            )
            gpus = []
            for line in proc.stdout.strip().splitlines():
                parts = [p.strip() for p in line.split(",")]
                if len(parts) >= 3:
                    gpus.append({"used_mb": int(parts[0]), "total_mb": int(parts[1]), "name": parts[2]})
            result["gpu"] = {"available": True, "devices": gpus}
        except (subprocess.TimeoutExpired, OSError, ValueError):
            result["gpu"] = {"available": True, "error": "nvidia-smi failed"}
    else:
        result["gpu"] = {"available": False}

    if json_output:
        print(_json.dumps(result, sort_keys=True))
    else:
        print("Worker Resources")
        ol = result["ollama"]
        if ol and ol.get("available"):
            models = ol.get("loaded_models", [])
            if models:
                print(f"  Ollama: {len(models)} model(s) loaded")
                for m in models:
                    print(f"    - {m['name']}")
            else:
                print("  Ollama: no models loaded")
        else:
            print("  Ollama: not available")
        gpu = result["gpu"]
        if gpu and gpu.get("available"):
            for g in gpu.get("devices", []):
                print(f"  GPU: {g['name']} ({g['used_mb']}/{g['total_mb']} MB)")
        else:
            print("  GPU: nvidia-smi not available")


def _cmd_worker_unload(
    *,
    provider: str = "ollama",
    model: str | None = None,
    unload_all: bool = False,
    json_output: bool = False,
) -> None:
    """Unload models from VRAM. No shell=True."""
    import shutil
    import subprocess

    if provider != "ollama":
        print(f"Error: unsupported provider for unload: {provider}", file=sys.stderr)
        sys.exit(1)

    if not shutil.which("ollama"):
        msg = "ollama not found — no models to unload"
        if json_output:
            print(_json.dumps({
                "version": 1, "provider": provider,
                "attempted": 0, "stopped": [], "skipped": [],
                "errors": [], "unavailable": True,
            }))
        else:
            print(msg)
        return

    targets: list[str] = []
    if model:
        targets = [model]
    elif unload_all:
        # Get loaded models from ollama ps
        try:
            proc = subprocess.run(
                ["ollama", "ps"],
                capture_output=True, text=True, timeout=10,
            )
            for line in proc.stdout.strip().splitlines()[1:]:
                parts = line.split()
                if parts:
                    targets.append(parts[0])
        except (subprocess.TimeoutExpired, OSError):
            pass
    else:
        print("Error: specify --model NAME or --all", file=sys.stderr)
        sys.exit(1)

    results: list[dict] = []
    for t in targets:
        try:
            proc = subprocess.run(
                ["ollama", "stop", t],
                capture_output=True, text=True, timeout=30,
            )
            results.append({"model": t, "stopped": proc.returncode == 0, "error": proc.stderr.strip() or None})
        except (subprocess.TimeoutExpired, OSError) as e:
            results.append({"model": t, "stopped": False, "error": str(e)})

    stopped = [r["model"] for r in results if r["stopped"]]
    errors = [r["model"] for r in results if not r["stopped"]]
    skipped: list[str] = []  # targets already unloaded (future: detect from ollama ps)
    out = {
        "version": 1, "provider": provider,
        "attempted": len(targets),
        "stopped": stopped, "skipped": skipped,
        "errors": errors, "unavailable": False,
    }
    if json_output:
        print(_json.dumps(out, sort_keys=True))
    else:
        for r in results:
            status = "stopped" if r["stopped"] else f"failed ({r['error']})"
            print(f"  {r['model']}: {status}")
        if not results:
            print("  No models to unload.")


def _cmd_worker_run(*, once: bool = False, max_jobs: int = 1, max_seconds: int = 60,
                    max_steps: int = 1, max_tokens: int = 0, max_runtime_seconds: int = 60,
                    provider: str = "none", job_id: str = "", json_output: bool = False) -> None:
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.worker_queue import (
        export_worker_result_json,
        run_worker_loop,
        run_worker_once,
    )
    data_dir = resolve_data_root()
    if once:
        result = run_worker_once(
            data_dir, provider=provider, job_id=job_id,
            max_steps=max_steps, max_tokens=max_tokens, max_runtime_seconds=max_runtime_seconds,
        )
    else:
        result = run_worker_loop(data_dir, provider=provider, max_jobs=max_jobs, max_seconds=max_seconds)
    if json_output:
        print(_json.dumps(export_worker_result_json(result), sort_keys=True))
    else:
        print(f"Worker: {result.worker_id}")
        print(f"Action: {result.action_taken}")
        print(f"Jobs processed: {result.jobs_processed}")
        if result.last_job_id:
            print(f"Last job: {result.last_job_id[:8]}")
        print(f"Why stopped: {result.why_it_stopped}")
        if result.next_command:
            print(f"Next: {result.next_command}")


def _cmd_worker_status_live(*, json_output: bool = False) -> None:
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.worker_queue import export_worker_status_json, get_worker_status
    data_dir = resolve_data_root()
    status = get_worker_status(data_dir)
    if json_output:
        print(_json.dumps(export_worker_status_json(status), sort_keys=True))
    else:
        print(f"Worker: {status.worker_id or '(none)'}")
        print(f"State: {status.lifecycle_state}")
        if status.current_job_id:
            print(f"Job: {status.current_job_id[:8]}")
        if status.last_action:
            print(f"Last action: {status.last_action}")
        if status.why_it_stopped:
            print(f"Why stopped: {status.why_it_stopped}")
        print(f"Processed: {status.processed_job_count}")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "worker.list": lambda args: _cmd_workers(
        json_output=args.json,
        sort=getattr(args, "sort", None),
        desc=getattr(args, "desc", False),
        since=getattr(args, "since", None),
        until=getattr(args, "until", None),
        limit=getattr(args, "limit", None),
    ),
    "worker.recommend": lambda args: _cmd_worker_recommend(args.job_id, json_output=args.json),
    "worker.show": lambda args: _cmd_worker_show(args.provider_id, json_output=args.json),
    "worker.explain": lambda args: _cmd_worker_explain(args.job_id, json_output=args.json),
    "worker.resources": lambda args: _cmd_worker_resources(json_output=args.json),
    "worker.unload": lambda args: _cmd_worker_unload(
        provider=getattr(args, "provider", None) or "ollama",
        model=getattr(args, "model", None),
        unload_all=getattr(args, "all", False),
        json_output=args.json,
    ),
    "worker.run": lambda args: _cmd_worker_run(
        once=getattr(args, "once", False),
        max_jobs=int(getattr(args, "max_jobs", 1) or 1),
        max_seconds=int(getattr(args, "max_seconds", 60) or 60),
        max_steps=int(getattr(args, "max_steps", 1) or 1),
        max_tokens=int(getattr(args, "max_tokens", 0) or 0),
        max_runtime_seconds=int(getattr(args, "max_runtime_seconds", 60) or 60),
        provider=getattr(args, "provider", None) or "none",
        job_id=getattr(args, "job", "") or getattr(args, "job_id", "") or "",
        json_output=getattr(args, "json", False),
    ),
    "worker.status": lambda args: _cmd_worker_status_live(json_output=args.json),
}

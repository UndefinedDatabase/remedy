"""Worker group command handlers."""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from apps.cli.json_envelope import emit_ok, fail

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
        fail("invalid_list_option", str(exc), json_output=json_output)

    if json_output:
        emit_ok(**export_worker_specs_json(specs))
    else:
        print(summarize_worker_specs(specs))


def _cmd_worker_show(provider_id: str, *, json_output: bool = False) -> None:
    from packages.orchestration.worker_adapters import (
        export_worker_specs_json,
        list_worker_specs,
    )

    specs = list_worker_specs()
    match = next((s for s in specs if s.provider_id == provider_id), None)
    if match is None:
        fail("unknown_provider", f"unknown provider: {provider_id}",
             json_output=json_output)
    if json_output:
        emit_ok(**export_worker_specs_json((match,)))
    else:
        print(f"Worker: {match.display_name} ({match.provider_id})")
        print(f"  Roles: {', '.join(match.supported_roles)}")
        print(f"  Mode:  {match.execution_mode}")
        print(f"  Status: {match.status}")
        if match.notes:
            print(f"  Notes: {match.notes}")


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
        emit_ok(**result)
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
        fail("unsupported_provider", f"unsupported provider for unload: {provider}",
             json_output=json_output)

    if not model and not unload_all:
        fail("missing_argument", "specify --model NAME or --all",
             json_output=json_output)

    if not shutil.which("ollama"):
        msg = "ollama not found — no models to unload"
        if json_output:
            emit_ok(
                version=1, provider=provider,
                attempted=0, stopped=[], skipped=[],
                errors=[], unavailable=True,
            )
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
        emit_ok(**out)
    else:
        for r in results:
            status = "stopped" if r["stopped"] else f"failed ({r['error']})"
            print(f"  {r['model']}: {status}")
        if not results:
            print("  No models to unload.")


def _cmd_worker_doctor(*, json_output: bool = False) -> None:
    """Read-only: does each `available` worker spec's own tooling actually exist?

    `list_worker_specs()` is data-only by design (worker_adapters.py's own
    docstring: "no network calls, no secrets, no shell execution"), so a spec
    marked `available` is a claim nothing in that module ever tests. This is
    the one check that does: for the spec(s) currently `available`, confirm
    the executable `worker resources`/`worker unload` already assume is
    reachable really is, the same `shutil.which` probe those two use.
    """
    import shutil

    from packages.orchestration.worker_adapters import list_worker_specs

    checks: list[dict[str, str | bool]] = []

    def _check(name: str, ok: bool, detail: str = "") -> None:
        checks.append({"check": name, "ok": ok, "detail": detail})

    specs = list_worker_specs()
    _check("worker_specs", True, f"{len(specs)} provider specs loaded")

    for spec in specs:
        if spec.status != "available":
            continue
        if spec.provider_id == "ollama":
            found = shutil.which("ollama") is not None
            _check("provider_ollama", found,
                   "ollama on PATH" if found else "ollama not found on PATH")
        else:
            # An `available` spec this doctor has no probe for: say so rather
            # than silently reporting it as though it had passed one.
            _check(f"provider_{spec.provider_id}", False,
                   f"no doctor probe defined for {spec.provider_id}")

    blockers: list[str] = [str(c["check"]) for c in checks if not c["ok"]]
    ready = len(blockers) == 0

    result: dict = {
        "version": 1,
        "ready": ready,
        "checks": checks,
        "blockers": blockers,
    }

    if json_output:
        emit_ok(**result)
        return
    print(f"Worker Doctor: {'READY' if ready else 'NOT READY'}")
    for c in checks:
        ok = "OK" if c["ok"] else "FAIL"
        print(f"  [{ok}] {c['check']}: {c['detail']}")
    if blockers:
        print(f"  blockers: {', '.join(blockers)}")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "worker.list": lambda args: _cmd_workers(
        json_output=args.json,
        sort=getattr(args, "sort", None),
        desc=getattr(args, "desc", False),
        since=getattr(args, "since", None),
        until=getattr(args, "until", None),
        limit=getattr(args, "limit", None),
    ),
    "worker.show": lambda args: _cmd_worker_show(args.provider_id, json_output=args.json),
    "worker.resources": lambda args: _cmd_worker_resources(json_output=args.json),
    "worker.unload": lambda args: _cmd_worker_unload(
        provider=getattr(args, "provider", None) or "ollama",
        model=getattr(args, "model", None),
        unload_all=getattr(args, "all", False),
        json_output=args.json,
    ),
    "worker.doctor": lambda args: _cmd_worker_doctor(json_output=args.json),
}

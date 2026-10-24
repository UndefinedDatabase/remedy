"""The worker isolation evidence and its pure helpers (F152 T001, DECISION F152 D3 (3) to (5)).

Builds the child environment a `WorkerIsolation` declaration lets through, the stable digest and
evidence record that describe it without ever printing a value, and the per-build evidence
writer, shaped like `capability_routes.record_capability_decisions`. The throwaway-home pair is
built here too, though no call path uses it yet (D3 (5)).
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from packages.contracts.adapter_contract import WorkerIsolation
from packages.orchestration.job_input_definition import is_secret_key

#: The one file name every claude-cli build's isolation line is written to, beside the run's
#: capability_decisions.jsonl (DECISION F152 D3 (4)).
WORKER_ISOLATION_FILENAME = "worker_isolation.jsonl"


# WHY: the one place that decides what a worker's child process actually sees, so a route never
# hand-filters an environment itself (DECISION F152 D3 (3)).
def isolated_child_env(
    isolation: WorkerIsolation, source: Mapping[str, str],
) -> dict[str, str] | None:
    """SOURCE's allowlisted names, present and unchanged; `None` (inherit) while ISOLATION does
    not apply or names nothing to keep."""
    if not isolation.applies or not isolation.env_allowlist:
        return None
    return {name: source[name] for name in isolation.env_allowlist if name in source}


# WHY: the one digest every worker_isolation.jsonl line carries, stable at equal configuration
# and never derived from, or printing, a secret's own value (DECISION F152 D3 (3)).
def worker_env_digest(env: Mapping[str, str] | None) -> str | None:
    """SHA256 over ENV's sorted name/value pairs, a value whose name `is_secret_key` reads as
    secret replaced by `[REDACTED]` first. `None` while ENV is `None` (the environment is
    inherited)."""
    if env is None:
        return None
    pairs = [
        f"{name}={'[REDACTED]' if is_secret_key(name) else env[name]}"
        for name in sorted(env)
    ]
    return hashlib.sha256("\n".join(pairs).encode("utf-8")).hexdigest()


# WHY: the typed shape `record_worker_isolation` writes, built once so a test and the factory
# read the same fields back (DECISION F152 D3 (4)).
def worker_isolation_record(
    isolation: WorkerIsolation, env: Mapping[str, str] | None,
) -> dict[str, Any]:
    """D3 (4)'s evidence fields, except `role`, `provider` and `model`, which the caller already
    knows and `record_worker_isolation` adds."""
    return {
        "method": isolation.method,
        "applied": isolation.applies,
        "home": "throwaway" if isolation.throwaway_home else "operator",
        "env_digest": worker_env_digest(env),
        "names": sorted(env) if env else [],
        "tool_args": list(isolation.tool_args),
        "adr_ref": isolation.adr_ref,
    }


# WHY: the run's isolation evidence lives beside its capability decisions, one line per provider
# build, never per call (DECISION F152 D3 (4)); shaped like `record_capability_decisions`.
def record_worker_isolation(
    evidence_dir: str | None, *, role: str, provider: str, model: str,
    record: dict[str, Any] | None,
) -> None:
    """Append one `worker_isolation.jsonl` line; nothing written for a falsy EVIDENCE_DIR or a
    falsy RECORD (an installed adapter that declares no isolation at all, e.g. a test double)."""
    if not evidence_dir or not record:
        return
    directory = Path(evidence_dir)
    directory.mkdir(parents=True, exist_ok=True)
    line = json.dumps(
        {"role": role, "provider": provider, "model": model, **record}, sort_keys=True)
    with open(directory / WORKER_ISOLATION_FILENAME, "a", encoding="utf-8") as handle:
        handle.write(line + "\n")


# WHY: D3 (5)'s create half; no call path provides a throwaway home yet, so this is proven only
# by its own unit tests until T002's A/B proof utility becomes its first caller.
def create_throwaway_home(parent: str) -> str:
    """A private directory named `worker-home-<random>` under PARENT, mode 0o700."""
    path = tempfile.mkdtemp(prefix="worker-home-", dir=parent)
    os.chmod(path, 0o700)
    return path


# WHY: the paired teardown; refuses anything `create_throwaway_home` did not name, so this
# function can never be handed an unrelated path to delete.
def remove_throwaway_home(path: str) -> None:
    """Delete PATH; raise ValueError for a directory not named `worker-home-*`."""
    name = os.path.basename(os.path.normpath(path))
    if not name.startswith("worker-home-"):
        raise ValueError(f"refusing to remove a directory not named worker-home-*: {path!r}")
    shutil.rmtree(path)

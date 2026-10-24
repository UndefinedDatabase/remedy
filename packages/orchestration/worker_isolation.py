"""The worker isolation evidence and its pure helpers (F152 T001, DECISION F152 D3 (3) to (5);
T002, DECISION F152 D4).

Builds the child environment a `WorkerIsolation` declaration lets through, the stable digest and
evidence record that describe it without ever printing a value, and the per-build evidence
writer, shaped like `capability_routes.record_capability_decisions`. `declared_isolation` is the
one place an adapter with no declaration becomes a loud bug rather than a silent neutral fallback
(D4 (1)). The throwaway-home pair is built here too; `run_isolation_ab`'s A/B proof is its first
caller (D4 (2)).
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from packages.contracts.adapter_contract import (
    CliInvocation,
    InvocationOptions,
    WorkerAdapter,
    WorkerIsolation,
)
from packages.orchestration.exec_guard import ExecGuardPolicy, ExecGuardResult, run_guarded
from packages.orchestration.job_input_definition import is_secret_key

#: The one file name every claude-cli build's isolation line is written to, beside the run's
#: capability_decisions.jsonl (DECISION F152 D3 (4)).
WORKER_ISOLATION_FILENAME = "worker_isolation.jsonl"

#: D4 (2)'s poison channel: an un-isolated run exports it with the marker so the A/B proof can
#: show whether an isolated run still sees it.
ISOLATION_POISON_ENV = "REMEDY_ISOLATION_POISON"


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


# WHY: the one place "no declaration" becomes a loud bug instead of a silent neutral fallback,
# so every reader of an adapter's isolation goes through the same check (DECISION F152 D4 (1)).
def declared_isolation(adapter: object) -> WorkerIsolation:
    """ADAPTER's own `isolation()` answer. Raises `TypeError` naming ADAPTER's `adapter_id` and
    either that it has no `isolation` member, or the value `isolation()` answered, when that
    value is not a `WorkerIsolation`."""
    adapter_id = getattr(adapter, "adapter_id", repr(adapter))
    isolation = getattr(adapter, "isolation", None)
    if isolation is None:
        raise TypeError(f"adapter {adapter_id!r} declares no isolation(): no such member")
    declaration = isolation()
    if not isinstance(declaration, WorkerIsolation):
        raise TypeError(
            f"adapter {adapter_id!r} declares no isolation(): isolation() answered {declaration!r}")
    return declaration


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
    record: dict[str, Any],
) -> None:
    """Append one `worker_isolation.jsonl` line; nothing written for a falsy EVIDENCE_DIR."""
    if not evidence_dir:
        return
    directory = Path(evidence_dir)
    directory.mkdir(parents=True, exist_ok=True)
    line = json.dumps(
        {"role": role, "provider": provider, "model": model, **record}, sort_keys=True)
    with open(directory / WORKER_ISOLATION_FILENAME, "a", encoding="utf-8") as handle:
        handle.write(line + "\n")


# WHY: D3 (5)'s create half; proven by its own unit tests and, since this round, by
# `run_isolation_ab` below, the throwaway home's first real caller (D4 (2)).
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


# WHY: the one check both runs of `run_isolation_ab` share, so the A/B comparison and its red
# controls all read the marker the same way (DECISION F152 D4 (2)).
def _marker_seen(result: ExecGuardResult, marker: str) -> bool:
    """True when MARKER occurs in RESULT's standard output or standard error."""
    needle = marker.encode("utf-8")
    return needle in result.stdout or needle in result.stderr


@dataclass(frozen=True)
class IsolationAbResult:
    """One A/B run's two outcomes: whether the marker reached stdout/stderr un-isolated and
    isolated. `proves_isolation` is the property the utility exists to show."""

    marker_unisolated: bool
    marker_isolated: bool

    @property
    def proves_isolation(self) -> bool:
        """MARKER_UNISOLATED true and MARKER_ISOLATED false: the poison leaked un-isolated and
        the declared isolation hid it."""
        return self.marker_unisolated and not self.marker_isolated


# WHY: the one utility every adapter's certification re-runs, so proving isolation is never
# re-derived per adapter (DECISION F152 D4 (2)).
def run_isolation_ab(
    adapter: WorkerAdapter, *, marker: str,
    poison_home: Callable[[str, str], None], parent: str, timeout_seconds: float = 30.0,
) -> IsolationAbResult:
    """Run ADAPTER's own declared command line twice against one throwaway home POISON_HOME
    wrote MARKER into: un-isolated, with ADAPTER's whole environment, no declared flags and the
    throwaway home as `HOME`; isolated, with the command line as built and the environment
    `isolated_child_env` makes of that same environment. Raises `ValueError` for a declaration
    that does not apply or a command line not ending with the declared `tool_args`, before any
    home is created. The home is removed in every case, including when POISON_HOME raises."""
    declaration = declared_isolation(adapter)
    if not declaration.applies:
        raise ValueError(f"adapter {adapter.adapter_id!r} declares isolation that does not apply")
    invocation = adapter.build_invocation("builder", ("ab-proof",), InvocationOptions(model=""))
    if not isinstance(invocation, CliInvocation):
        raise ValueError(
            f"adapter {adapter.adapter_id!r} built {type(invocation).__name__}, not a command line")
    argv = list(invocation.argv)
    tool_args = list(declaration.tool_args)
    if tool_args and argv[-len(tool_args):] != tool_args:
        raise ValueError(
            f"adapter {adapter.adapter_id!r} command line does not end with its declared tool_args")
    unisolated_argv = argv[: len(argv) - len(tool_args)]

    home = create_throwaway_home(parent)
    try:
        poison_home(home, marker)
        work = os.path.join(home, "work")
        os.makedirs(work, exist_ok=True)
        base_env = dict(os.environ)
        base_env["HOME"] = home
        base_env[ISOLATION_POISON_ENV] = marker

        unisolated = run_guarded(unisolated_argv, ExecGuardPolicy(
            wall_timeout_seconds=timeout_seconds, cwd=work, env=base_env, core_file_bytes=0))
        isolated = run_guarded(argv, ExecGuardPolicy(
            wall_timeout_seconds=timeout_seconds, cwd=work,
            env=isolated_child_env(declaration, base_env), core_file_bytes=0))
    finally:
        remove_throwaway_home(home)

    return IsolationAbResult(
        marker_unisolated=_marker_seen(unisolated, marker),
        marker_isolated=_marker_seen(isolated, marker),
    )

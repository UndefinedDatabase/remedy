"""F061 T002 — execute DoD checks and record what actually happened.

One check in, one :class:`CheckEvidence` out: the command as argv, the working
directory, the exit code, how long it took, and a tail of the real output. A
check is green only when its process exited 0. Every other outcome — a missing
tool, a refused executable, a bad working directory, a timeout — is RED with a
named reason. Nothing here can produce a silent pass.

Subprocess discipline is the one already used by
``test_runner.run_tests_local``, reused rather than reinvented:

  * never ``shell=True``; ``subprocess.run`` receives an argv LIST;
  * ``cwd`` is the resolved worktree (or a validated subdirectory of it);
  * the environment is inherited as-is — no extra vars, no ``.env`` reading;
  * a timeout always applies;
  * output is captured, decoded leniently, and truncated to a tail.

Two guards are specific to this module, because a DoD check can originate from
an LLM rather than from repository discovery:

  * ``lint`` / ``build`` / ``custom_cmd`` name their own executable, so that
    executable must appear in an allowlist — by default the same closed list
    ``test_runner`` is willing to invoke. A refused executable is red with
    reason ``executable_not_allowed`` and NOTHING is run.
  * a check's ``cwd`` must resolve inside the worktree. The schema already
    refuses ``..`` and absolute paths at compile time; this is the second
    check, after symlink resolution, immediately before exec (F017).

``runtime_flow`` is a valid schema kind from R1 on, but it has NO runner here.
:func:`runner_for` raises :class:`UnsupportedCheckKindError` for it — the
registry fails loud rather than skipping the check or calling it green. The
runner lands in T003.
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from packages.orchestration.dod_schema import DoD, DoDCheck
from packages.orchestration.test_runner import _EXECUTION_SAFE_EXECUTABLES

#: Default per-check wall clock. A check that cannot finish in five minutes is
#: reported as a timeout, never left to hang a job.
CHECK_TIMEOUT_DEFAULT_SEC = 300

#: How much of the process output survives into the evidence record.
MAX_OUTPUT_TAIL_CHARS = 4000

#: Statuses a check can end in. There is no third, softer option.
STATUS_PASSED = "passed"
STATUS_FAILED = "failed"

#: Named reasons for a red check. Empty on a green one.
REASON_NONE = ""
REASON_NONZERO_EXIT = "nonzero_exit"
REASON_TOOL_UNAVAILABLE = "tool_unavailable"
REASON_TIMEOUT = "timeout"
REASON_EXECUTABLE_NOT_ALLOWED = "executable_not_allowed"
REASON_CWD_OUTSIDE_WORKTREE = "cwd_outside_worktree"
REASON_CWD_MISSING = "cwd_missing"

#: The interpreter that runs ``pytest`` checks. Resolved rather than assumed:
#: inside a virtualenv the ``python3`` on PATH is not necessarily this one.
PYTEST_PYTHON = sys.executable or "python3"

#: Executables a check may name for itself. The closed list test_runner is
#: willing to invoke — deliberately shared, so widening it stays a single,
#: reviewable decision. Callers may pass a different set explicitly.
DEFAULT_ALLOWED_EXECUTABLES = _EXECUTION_SAFE_EXECUTABLES


class UnsupportedCheckKindError(Exception):
    """No runner is registered for this check kind."""


@dataclass(frozen=True)
class CheckEvidence:
    """What one check did, in enough detail to argue about it later."""

    check_id: str
    kind: str
    source: str
    blocking: bool
    status: str
    #: Empty when green; a named reason when red.
    reason: str
    #: The argv, joined for display. Empty when nothing was executed.
    command: str
    argv: tuple[str, ...]
    #: Working directory the process ran in, relative to the worktree.
    cwd: str
    #: None when no process ran (refused, missing tool) or on timeout.
    exit_code: int | None
    duration_ms: int
    output_tail: str
    output_truncated: bool = False

    @property
    def green(self) -> bool:
        return self.status == STATUS_PASSED


# ---------------------------------------------------------------------------
# Argv construction — one builder per runnable kind
# ---------------------------------------------------------------------------

def _pytest_argv(check: DoDCheck) -> list[str]:
    spec = check.spec
    return [PYTEST_PYTHON, "-m", "pytest", str(spec["selector"]),
            *[str(a) for a in spec.get("args", [])], "-q"]


def _tool_argv(check: DoDCheck) -> list[str]:
    """lint and build share a shape: a tool, its args, then its paths."""
    spec = check.spec
    return [str(spec["tool"]),
            *[str(a) for a in spec.get("args", [])],
            *[str(p) for p in spec.get("paths", [])]]


def _custom_argv(check: DoDCheck) -> list[str]:
    return [str(a) for a in check.spec["argv"]]


#: kind -> argv builder. ``runtime_flow`` is ABSENT on purpose: its runner
#: arrives in T003, and until then asking for it must fail loudly.
RUNNER_REGISTRY: dict[str, Callable[[DoDCheck], list[str]]] = {
    "pytest": _pytest_argv,
    "lint": _tool_argv,
    "build": _tool_argv,
    "custom_cmd": _custom_argv,
}

#: Kinds whose executable comes from the check itself and is therefore
#: allowlisted. ``pytest`` is exempt: its argv is built from a fixed template
#: and only the pytest SELECTOR comes from the check.
_ALLOWLISTED_KINDS = frozenset({"lint", "build", "custom_cmd"})


def runner_for(kind: str) -> Callable[[DoDCheck], list[str]]:
    """Return the argv builder for ``kind``, or fail loud.

    A kind the schema accepts but this round cannot execute raises rather than
    returning a no-op. A check that cannot run must never look like one that
    ran and passed.
    """
    builder = RUNNER_REGISTRY.get(kind)
    if builder is None:
        raise UnsupportedCheckKindError(
            f"no runner registered for check kind {kind!r} "
            f"(available: {', '.join(sorted(RUNNER_REGISTRY))})")
    return builder


def build_argv(check: DoDCheck) -> list[str]:
    """The exact argv a check will be executed as."""
    return runner_for(check.kind)(check)


# ---------------------------------------------------------------------------
# Execution
# ---------------------------------------------------------------------------

def _resolve_cwd(check: DoDCheck, worktree_root: Path) -> tuple[Path | None, str]:
    """Resolve the check's working directory, or say why it is refused.

    Returns ``(path, "")`` when usable, ``(None, reason)`` otherwise. The
    worktree root itself is resolved first, so a symlinked worktree is compared
    against its real location rather than its alias.
    """
    root = worktree_root.resolve()
    relative = str(check.spec.get("cwd", "") or "").strip()
    candidate = (root / relative).resolve() if relative else root

    if candidate != root and root not in candidate.parents:
        return None, REASON_CWD_OUTSIDE_WORKTREE
    if not candidate.is_dir():
        return None, REASON_CWD_MISSING
    return candidate, ""


def _tail(raw: bytes) -> tuple[str, bool]:
    text = raw.decode("utf-8", errors="replace")
    if len(text) <= MAX_OUTPUT_TAIL_CHARS:
        return text, False
    return text[-MAX_OUTPUT_TAIL_CHARS:], True


def _refused(check: DoDCheck, reason: str, argv: list[str], cwd: str,
             detail: str) -> CheckEvidence:
    """A red result for a check that never reached exec."""
    return CheckEvidence(
        check_id=check.id,
        kind=check.kind,
        source=check.source,
        blocking=check.blocking,
        status=STATUS_FAILED,
        reason=reason,
        command=" ".join(argv),
        argv=tuple(argv),
        cwd=cwd,
        exit_code=None,
        duration_ms=0,
        output_tail=detail,
    )


def run_check(
    check: DoDCheck,
    worktree_root: Path | str,
    *,
    timeout_sec: int = CHECK_TIMEOUT_DEFAULT_SEC,
    allowed_executables: frozenset[str] | set[str] | None = None,
) -> CheckEvidence:
    """Run one check inside the worktree and return its evidence.

    Raises :class:`UnsupportedCheckKindError` for a kind with no runner — that
    is a wiring bug or an unimplemented round, and it is not something to paper
    over with a red result.
    """
    root = Path(worktree_root)
    argv = build_argv(check)
    allowed = DEFAULT_ALLOWED_EXECUTABLES if allowed_executables is None \
        else frozenset(allowed_executables)
    declared_cwd = str(check.spec.get("cwd", "") or "")

    if check.kind in _ALLOWLISTED_KINDS and argv[0] not in allowed:
        return _refused(
            check, REASON_EXECUTABLE_NOT_ALLOWED, argv, declared_cwd,
            f"executable {argv[0]!r} is not in the allowed set; nothing was run")

    cwd, cwd_reason = _resolve_cwd(check, root)
    if cwd is None:
        return _refused(
            check, cwd_reason, argv, declared_cwd,
            f"working directory {declared_cwd or '.'!r} is unusable "
            f"under {root}; nothing was run")

    start = time.monotonic()
    try:
        proc = subprocess.run(
            argv,
            cwd=str(cwd),
            capture_output=True,
            timeout=timeout_sec,
            env=os.environ.copy(),
        )
    except FileNotFoundError:
        # The tool is not installed. A missing linter is a RED check with a
        # named reason — never an absent one, and never a pass.
        return _refused(
            check, REASON_TOOL_UNAVAILABLE, argv, declared_cwd,
            f"{argv[0]!r} was not found on PATH")
    except subprocess.TimeoutExpired as exc:
        duration_ms = int((time.monotonic() - start) * 1000)
        raw = (exc.stdout or b"") + (exc.stderr or b"") + b"\n[timeout expired]\n"
        tail, truncated = _tail(raw)
        return CheckEvidence(
            check_id=check.id, kind=check.kind, source=check.source,
            blocking=check.blocking, status=STATUS_FAILED, reason=REASON_TIMEOUT,
            command=" ".join(argv), argv=tuple(argv), cwd=declared_cwd,
            exit_code=None, duration_ms=duration_ms, output_tail=tail,
            output_truncated=truncated,
        )

    duration_ms = int((time.monotonic() - start) * 1000)
    tail, truncated = _tail(proc.stdout + proc.stderr)
    passed = proc.returncode == 0
    return CheckEvidence(
        check_id=check.id,
        kind=check.kind,
        source=check.source,
        blocking=check.blocking,
        status=STATUS_PASSED if passed else STATUS_FAILED,
        reason=REASON_NONE if passed else REASON_NONZERO_EXIT,
        command=" ".join(argv),
        argv=tuple(argv),
        cwd=declared_cwd,
        exit_code=proc.returncode,
        duration_ms=duration_ms,
        output_tail=tail,
        output_truncated=truncated,
    )


def run_checks(
    dod: DoD,
    worktree_root: Path | str,
    *,
    timeout_sec: int = CHECK_TIMEOUT_DEFAULT_SEC,
    allowed_executables: frozenset[str] | set[str] | None = None,
) -> list[CheckEvidence]:
    """Run every check in a DoD, in order, and return the evidence.

    Deliberately returns evidence and nothing else: deciding what a red
    blocking check MEANS for a job is the job-end gate's business (T004), not
    the runner's.
    """
    return [
        run_check(check, worktree_root, timeout_sec=timeout_sec,
                  allowed_executables=allowed_executables)
        for check in dod.checks
    ]

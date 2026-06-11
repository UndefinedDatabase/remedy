"""Central contract-gated Test Execution Service — Steps 1088-1097.

Design invariants:
  - No shell=True anywhere.
  - No capture_output=True — stdout/stderr written directly to bounded files.
  - No raw output in returned models, events, Job metadata, or failure artifacts.
  - No .env loading.
  - No secret-bearing environment inheritance (secrets filtered before exec).
  - No repository mutation.
  - No kill of unrelated processes.
  - Blocked-before-start consumes zero usage slots.
  - Process isolation: start_new_session=True, stdin=DEVNULL, close_fds=True.
  - Timeout: SIGTERM + bounded wait + SIGKILL, then proc.wait().
  - Concurrent same-job run blocked by file lease.
  - Lease always released (try/finally).

Gate order for execute_test_run():
  1. load job safely
  2. validate target repository
  3. verify repo_test_run permission
  4. load persisted RunContract + validate
  5. load RunUsage
  6. evaluate run_test action (contract + budget)
  7. acquire test execution lease
  8. discover safe test command
  9. execute with process isolation
  10. persist usage and record
  11. emit lifecycle events
  12. create failure artifact if needed
  13. release lease

Public API::

    execute_test_run(request: TestExecutionRequest) -> TestExecutionResult
"""

from __future__ import annotations

import fcntl
import os
import signal
import subprocess
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any
from uuid import UUID, uuid4

from packages.orchestration.command_discovery import (
    discover_commands,
    select_best_test_candidate,
)
from packages.orchestration.data_paths import resolve_data_root
from packages.orchestration.permissions import Capability, is_allowed
from packages.orchestration.run_contract import (
    ContractAction,
    ensure_contract,
    evaluate_run_action,
    export_usage_json,
    load_usage,
    save_usage,
    validate_run_contract,
    RunUsage,
)
from packages.orchestration.storage import JobNotFoundError, load_job, save_job
from packages.orchestration.test_runner import _EXECUTION_SAFE_EXECUTABLES


# ---------------------------------------------------------------------------
# Request / Result / Lease models (Step 1088)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TestExecutionRequest:
    """Input to execute_test_run."""

    __test__ = False

    job_id: str
    source: str = "cli_v1"
    task_id: str = ""
    intent_id: str = ""
    apply_id: str = ""
    requested_timeout_seconds: float | None = None


@dataclass
class TestExecutionResult:
    """Output of execute_test_run. No raw output fields."""

    __test__ = False

    job_id: str
    contract_id: str = ""
    test_run_id: str = ""
    status: str = "blocked"           # blocked | passed | failed | timeout | environment_failure
    safe_summary: str = ""
    command_safe: str = ""
    exit_code: int | None = None
    duration_ms: int = 0
    output_ref: str = ""              # relative basename of workspace output file
    failure_artifact_id: str = ""
    linked_task_id: str = ""
    linked_intent_id: str = ""
    linked_apply_id: str = ""
    usage_before: dict[str, Any] = field(default_factory=dict)
    usage_after: dict[str, Any] = field(default_factory=dict)
    stop_reason: str = ""
    next_safe_action: str = ""
    contract_guidance: str = ""


@dataclass
class TestExecutionDecision:
    """Internal gate pass/fail record."""

    __test__ = False

    allowed: bool
    gate: str
    reason: str
    next_safe_action: str = ""
    guidance: str = ""


@dataclass
class TestExecutionLease:
    """File-backed exclusive lease for a single job's test run."""

    __test__ = False

    job_id: str
    lease_path: Path
    _fh: Any = field(default=None, repr=False, compare=False)

    def acquire(self, *, timeout_seconds: float = 5.0) -> bool:
        """Try to acquire the lease. Returns True on success."""
        self._fh = open(self.lease_path, "w")  # noqa: SIM115 — must stay open
        deadline = time.monotonic() + timeout_seconds
        while True:
            try:
                fcntl.flock(self._fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
                self._fh.write(f"{os.getpid()}\n{datetime.now(timezone.utc).isoformat()}\n")
                self._fh.flush()
                return True
            except OSError:
                if time.monotonic() >= deadline:
                    self._fh.close()
                    self._fh = None
                    return False
                time.sleep(0.05)

    def release(self) -> None:
        if self._fh is not None:
            try:
                fcntl.flock(self._fh, fcntl.LOCK_UN)
                self._fh.close()
            except OSError:
                pass
            finally:
                self._fh = None
            try:
                self.lease_path.unlink(missing_ok=True)
            except OSError:
                pass


# ---------------------------------------------------------------------------
# Environment policy (Step 1091)
# ---------------------------------------------------------------------------

_SECRET_KEY_PATTERNS: tuple[str, ...] = (
    "token", "secret", "password", "passwd", "credential", "api_key", "apikey",
    "private_key", "privatekey", "auth_key", "authkey", "access_key", "accesskey",
    "aws_secret", "aws_access", "openai_api", "anthropic_api",
)

_SAFE_ENV_PREFIXES: tuple[str, ...] = (
    "path", "home", "user", "shell", "term", "lang", "lc_",
    "tmpdir", "tmp", "temp", "virtual_env", "venv", "conda_",
    "pyenv_", "nvm_", "gopath", "goroot", "cargo_home",
    "npm_config_cache", "xdg_",
)

_ALWAYS_KEEP: frozenset[str] = frozenset({
    "PATH", "HOME", "USER", "SHELL", "TERM", "LANG", "TMPDIR", "TMP", "TEMP",
    "VIRTUAL_ENV", "VENV", "CONDA_PREFIX",
    "GOPATH", "GOROOT", "CARGO_HOME", "CARGO",
    "LC_ALL", "LC_CTYPE", "LC_MESSAGES",
    "XDG_RUNTIME_DIR", "XDG_CONFIG_HOME", "XDG_DATA_HOME", "XDG_CACHE_HOME",
    "NPM_CONFIG_CACHE",
})


def _build_safe_env(base_env: dict[str, str] | None = None) -> dict[str, str]:
    """Build a filtered environment dict safe to pass to a child test process.

    Strips any key whose lowercase form contains a secret-indicator pattern.
    Preserves only known-safe runtime variables.

    OS-level network isolation is NOT implemented — no_cloud=True in the
    contract is a policy statement, not a network sandbox.
    """
    src = base_env if base_env is not None else dict(os.environ)
    result: dict[str, str] = {}
    for key, value in src.items():
        key_lower = key.lower()
        # Always strip secret-bearing keys
        if any(pat in key_lower for pat in _SECRET_KEY_PATTERNS):
            continue
        # Keep always-allowed names
        if key in _ALWAYS_KEEP:
            result[key] = value
            continue
        # Keep keys with safe prefixes
        if any(key_lower.startswith(pfx) for pfx in _SAFE_ENV_PREFIXES):
            result[key] = value
            continue
    return result


# ---------------------------------------------------------------------------
# Process isolation (Step 1090)
# ---------------------------------------------------------------------------

_MAX_SYSTEM_TIMEOUT_SECONDS: float = 600.0
_MIN_PRACTICAL_TIMEOUT_SECONDS: float = 5.0
_SIGTERM_WAIT_SECONDS: float = 3.0


def _run_isolated_process(
    argv: list[str],
    *,
    cwd: str,
    env: dict[str, str],
    output_file: Path,
    timeout_seconds: float,
) -> tuple[str, int | None, int]:
    """Run argv in an isolated process group. Returns (status, exit_code, duration_ms).

    Output written to output_file. No capture_output=True.
    SIGTERM then SIGKILL on timeout. Process group killed.
    """
    start = time.monotonic()
    status: str
    exit_code: int | None = None

    with open(output_file, "wb") as out_fh:
        try:
            proc = subprocess.Popen(
                argv,
                cwd=cwd,
                env=env,
                stdin=subprocess.DEVNULL,
                stdout=out_fh,
                stderr=out_fh,
                start_new_session=True,
                close_fds=True,
            )
        except FileNotFoundError:
            duration_ms = int((time.monotonic() - start) * 1000)
            out_fh.write(b"[remedy: command not found]\n")
            return "environment_failure", None, duration_ms
        except OSError as exc:
            duration_ms = int((time.monotonic() - start) * 1000)
            out_fh.write(f"[remedy: OS error launching process: {exc}]\n".encode())
            return "environment_failure", None, duration_ms

        try:
            proc.wait(timeout=timeout_seconds)
            exit_code = proc.returncode
            status = "passed" if exit_code == 0 else "failed"
        except subprocess.TimeoutExpired:
            status = "timeout"
            _kill_process_group(proc)
        except Exception:
            status = "environment_failure"
            _kill_process_group(proc)

    duration_ms = int((time.monotonic() - start) * 1000)
    if status == "timeout":
        with open(output_file, "ab") as out_fh:
            out_fh.write(b"\n[remedy: test run timed out]\n")
    return status, exit_code, duration_ms


def _kill_process_group(proc: subprocess.Popen) -> None:  # type: ignore[type-arg]
    """SIGTERM the process group, wait briefly, then SIGKILL."""
    try:
        pgid = os.getpgid(proc.pid)
    except OSError:
        # Process already gone
        try:
            proc.wait(timeout=1.0)
        except Exception:
            pass
        return
    # SIGTERM
    try:
        os.killpg(pgid, signal.SIGTERM)
    except OSError:
        pass
    # Wait briefly for graceful exit
    try:
        proc.wait(timeout=_SIGTERM_WAIT_SECONDS)
    except subprocess.TimeoutExpired:
        pass
    # SIGKILL
    try:
        os.killpg(pgid, signal.SIGKILL)
    except OSError:
        pass
    # Final wait to reap
    try:
        proc.wait(timeout=2.0)
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Output handling
# ---------------------------------------------------------------------------

_MAX_OUTPUT_BYTES: int = 1_048_576  # 1 MiB


def _truncate_output_file(output_file: Path) -> tuple[int, bool, int]:
    """Truncate output file to max size. Returns (original_bytes, truncated, final_bytes)."""
    try:
        original = output_file.stat().st_size
    except OSError:
        return 0, False, 0

    if original <= _MAX_OUTPUT_BYTES:
        return original, False, original

    # Read first MAX_OUTPUT_BYTES and append truncation marker
    with open(output_file, "rb") as f:
        data = f.read(_MAX_OUTPUT_BYTES)
    data += b"\n[remedy output truncated]\n"
    output_file.write_bytes(data)
    return original, True, len(data)


# ---------------------------------------------------------------------------
# Timeout derivation (Step 1093)
# ---------------------------------------------------------------------------


def _derive_timeout(
    contract_max_runtime: float,
    runtime_used: float,
    requested_timeout: float | None,
) -> float | None:
    """Derive safe timeout. Returns None if no runtime remains (block before exec)."""
    remaining = contract_max_runtime - runtime_used if contract_max_runtime > 0 else None
    if remaining is not None and remaining <= 0:
        return None  # no runtime left — block

    candidates = [_MAX_SYSTEM_TIMEOUT_SECONDS]
    if remaining is not None:
        candidates.append(remaining)
    if requested_timeout is not None and requested_timeout > 0:
        candidates.append(requested_timeout)

    timeout = min(candidates)
    return max(timeout, _MIN_PRACTICAL_TIMEOUT_SECONDS)


# ---------------------------------------------------------------------------
# Linkage validation (Step 1098)
# ---------------------------------------------------------------------------


def _validate_linkage(
    job: Any,
    task_id: str,
    intent_id: str,
    apply_id: str,
) -> TestExecutionDecision | None:
    """Validate supplied linkage IDs against the job. Returns error decision or None."""
    if task_id:
        task_ids = {str(t.id) for t in (job.tasks or [])}
        if task_id not in task_ids:
            return TestExecutionDecision(
                allowed=False,
                gate="linkage",
                reason=f"task_id {task_id!r} not found in job",
                next_safe_action=f"remedy job show {job.id} --json",
            )
    if intent_id:
        # Intent IDs live in artifacts / metadata — check metadata
        known_intents: set[str] = set()
        for art in (job.artifacts or []):
            pi = art.metadata.get("patch_intents") or {}
            known_intents.update(pi.keys())
        if intent_id not in known_intents:
            return TestExecutionDecision(
                allowed=False,
                gate="linkage",
                reason=f"intent_id {intent_id!r} not found in job",
                next_safe_action=f"remedy job show {job.id} --json",
            )
    if apply_id:
        known_applies: set[str] = set()
        for art in (job.artifacts or []):
            ar = art.metadata.get("patch_intent_apply_records") or {}
            known_applies.update(ar.keys())
        if apply_id not in known_applies:
            return TestExecutionDecision(
                allowed=False,
                gate="linkage",
                reason=f"apply_id {apply_id!r} not found in job",
                next_safe_action=f"remedy job show {job.id} --json",
            )
    return None


# ---------------------------------------------------------------------------
# Event emission helpers (Step 1096)
# ---------------------------------------------------------------------------


def _emit(data_dir: Path, job_id: UUID, event: str, metadata: dict[str, Any]) -> None:
    from packages.orchestration.timeline import append_run_event
    try:
        append_run_event(data_dir, job_id, event=event, metadata=metadata)
    except Exception:
        pass  # non-fatal


def _safe_event_meta(
    result: TestExecutionResult,
    *,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build safe event metadata. No raw output."""
    meta: dict[str, Any] = {
        "test_run_id": result.test_run_id,
        "contract_id": result.contract_id,
        "status": result.status,
        "exit_code": result.exit_code,
        "duration_ms": result.duration_ms,
        "command_safe": result.command_safe,
        "source": "test_execution_service_v1",
    }
    if result.linked_task_id:
        meta["task_id"] = result.linked_task_id
    if result.linked_intent_id:
        meta["intent_id"] = result.linked_intent_id
    if result.linked_apply_id:
        meta["apply_id"] = result.linked_apply_id
    if result.usage_after:
        meta["usage"] = {
            "test_runs_used": result.usage_after.get("test_runs_used", 0),
            "runtime_seconds_used": result.usage_after.get("runtime_seconds_used", 0.0),
        }
    if extra:
        meta.update(extra)
    return meta


# ---------------------------------------------------------------------------
# Central execute function (Steps 1089-1097)
# ---------------------------------------------------------------------------


def execute_test_run(request: TestExecutionRequest) -> TestExecutionResult:
    """Run a test for a job. Enforces all gates. Returns a safe result.

    This is the single entry point. CLI, repair_loop, and future flows all
    call here. No raw output returned.
    """
    data_dir = resolve_data_root()
    test_run_id = uuid4().hex[:16]
    created_at = datetime.now(timezone.utc).isoformat()

    result = TestExecutionResult(
        job_id=request.job_id,
        test_run_id=test_run_id,
        linked_task_id=request.task_id,
        linked_intent_id=request.intent_id,
        linked_apply_id=request.apply_id,
    )

    # ── Gate 1: Load job ────────────────────────────────────────────────────
    try:
        job_id_parsed = UUID(request.job_id)
    except ValueError:
        result.status = "blocked"
        result.stop_reason = "invalid_job_id"
        result.safe_summary = "Job ID format invalid."
        result.next_safe_action = "remedy job list"
        return result

    try:
        job = load_job(job_id_parsed)
    except JobNotFoundError:
        result.status = "blocked"
        result.stop_reason = "job_not_found"
        result.safe_summary = "Job not found."
        result.next_safe_action = "remedy job list"
        return result

    # ── Gate 2: Validate target repository ──────────────────────────────────
    target_repo_str: str | None = job.metadata.get("target_repo")
    if not target_repo_str:
        result.status = "blocked"
        result.stop_reason = "no_target_repo"
        result.safe_summary = "No target repository attached to job."
        result.next_safe_action = f"remedy job attach-repo {job.id} <repo_path>"
        return result

    repo_root = Path(target_repo_str).resolve()
    if not repo_root.is_dir():
        result.status = "blocked"
        result.stop_reason = "target_repo_not_a_directory"
        result.safe_summary = "Target repository path does not exist."
        result.next_safe_action = f"remedy job attach-repo {job.id} <repo_path>"
        return result

    # ── Gate 3: repo_test_run permission ────────────────────────────────────
    if not is_allowed(job, Capability.repo_test_run):
        result.status = "blocked"
        result.stop_reason = "permission_denied"
        result.safe_summary = "Permission repo_test_run not granted."
        result.next_safe_action = f"remedy job permit {job.id} repo_test_run allow"
        result.contract_guidance = f"remedy job permit {job.id} repo_test_run allow"
        _emit(data_dir, job_id_parsed, "test_run_blocked", {
            "test_run_id": test_run_id,
            "reason": "permission_denied",
            "next_safe_action": result.next_safe_action,
        })
        return result

    # ── Gate 4: Load and validate contract ──────────────────────────────────
    contract = ensure_contract(job)
    result.contract_id = contract.contract_id
    contract_errors = validate_run_contract(contract)
    if contract_errors:
        result.status = "blocked"
        result.stop_reason = "contract_invalid"
        result.safe_summary = "Run contract failed validation."
        result.next_safe_action = f"remedy contract inspect {job.id} --json"
        return result

    # ── Gate 5: Load usage ───────────────────────────────────────────────────
    usage = load_usage(job)
    result.usage_before = export_usage_json(usage)

    # ── Gate 6: Evaluate run_test ────────────────────────────────────────────
    decision = evaluate_run_action(contract, ContractAction.RUN_TEST, usage=usage)
    if not decision.allowed:
        result.status = "blocked"
        result.stop_reason = f"contract_{decision.status}"
        result.safe_summary = decision.reason
        result.next_safe_action = decision.next_safe_action
        if decision.status == "exhausted" and "max_test_runs" in decision.reason:
            result.contract_guidance = (
                f"remedy contract set {job.id} max_test_runs <n>"
            )
        _emit(data_dir, job_id_parsed, "test_run_blocked", {
            "test_run_id": test_run_id,
            "contract_id": contract.contract_id,
            "reason": result.stop_reason,
            "next_safe_action": result.next_safe_action,
        })
        _emit(data_dir, job_id_parsed, "contract_decision", {
            "action": ContractAction.RUN_TEST,
            "allowed": False,
            "status": decision.status,
            "reason": decision.reason,
            "contract_id": contract.contract_id,
        })
        return result

    # ── Validate linkage IDs ─────────────────────────────────────────────────
    linkage_error = _validate_linkage(
        job, request.task_id, request.intent_id, request.apply_id
    )
    if linkage_error is not None:
        result.status = "blocked"
        result.stop_reason = "invalid_linkage"
        result.safe_summary = linkage_error.reason
        result.next_safe_action = linkage_error.next_safe_action
        return result

    # ── Gate 7: Acquire lease ────────────────────────────────────────────────
    workspace_root = data_dir / "workspaces" / str(job_id_parsed)
    workspace_root.mkdir(parents=True, exist_ok=True)
    lease_path = workspace_root / "test_execution.lock"
    lease = TestExecutionLease(job_id=str(job_id_parsed), lease_path=lease_path)

    if not lease.acquire(timeout_seconds=2.0):
        result.status = "blocked"
        result.stop_reason = "test_run_already_active"
        result.safe_summary = "Another test run is already active for this job."
        result.next_safe_action = f"remedy test status {job.id}"
        _emit(data_dir, job_id_parsed, "test_run_blocked", {
            "test_run_id": test_run_id,
            "reason": "test_run_already_active",
        })
        return result

    try:
        # ── Gate 8: Discover safe test command ──────────────────────────────
        candidates = discover_commands(job, repo_root)
        candidate = select_best_test_candidate(candidates)

        if candidate is None:
            result.status = "blocked"
            result.stop_reason = "no_test_command_discovered"
            result.safe_summary = "No safe test command discovered for this repository."
            result.next_safe_action = f"remedy test discover {job.id} --json"
            _emit(data_dir, job_id_parsed, "test_run_blocked", {
                "test_run_id": test_run_id,
                "reason": "no_test_command_discovered",
            })
            return result

        if candidate.risk == "high":
            result.status = "blocked"
            result.stop_reason = "high_risk_command"
            result.safe_summary = "Discovered command has high risk rating — blocked."
            result.next_safe_action = f"remedy test discover {job.id} --json"
            return result

        if candidate.argv[0] not in _EXECUTION_SAFE_EXECUTABLES:
            result.status = "blocked"
            result.stop_reason = "executable_not_in_safe_list"
            result.safe_summary = "Discovered executable not in safety allowlist."
            result.next_safe_action = f"remedy test discover {job.id} --json"
            return result

        result.command_safe = candidate.display

        # ── Derive timeout ───────────────────────────────────────────────────
        timeout = _derive_timeout(
            contract.max_runtime_seconds,
            usage.runtime_seconds_used,
            request.requested_timeout_seconds,
        )
        if timeout is None:
            result.status = "blocked"
            result.stop_reason = "no_runtime_remaining"
            result.safe_summary = "No runtime budget remaining in contract."
            result.next_safe_action = f"remedy contract set {job.id} max_runtime_seconds <n>"
            return result

        # ── Gate 9: Execute ──────────────────────────────────────────────────
        test_runs_dir = workspace_root / "test_runs"
        test_runs_dir.mkdir(parents=True, exist_ok=True)
        output_file = test_runs_dir / f"{test_run_id}.txt"

        safe_env = _build_safe_env()
        argv = candidate.argv_list()

        _emit(data_dir, job_id_parsed, "test_run_requested", {
            "test_run_id": test_run_id,
            "contract_id": contract.contract_id,
            "command_source_type": candidate.source_type,
            "source": request.source,
        })

        status, exit_code, duration_ms = _run_isolated_process(
            argv,
            cwd=str(repo_root),
            env=safe_env,
            output_file=output_file,
            timeout_seconds=timeout,
        )

        result.status = status
        result.exit_code = exit_code
        result.duration_ms = duration_ms
        result.output_ref = output_file.name

        # ── Gate 10: Persist usage ───────────────────────────────────────────
        # Reload job to avoid stale state, then update usage
        job = load_job(job_id_parsed)
        usage = load_usage(job)
        usage.test_runs_used += 1
        usage.runtime_seconds_used += duration_ms / 1000.0
        save_usage(job, usage)
        save_job(job)
        result.usage_after = export_usage_json(usage)

        # ── Gate 11: Persist safe test record ───────────────────────────────
        _truncate_output_file(output_file)
        _persist_test_record(job_id_parsed, result, candidate, test_run_id, created_at)

        # ── Gate 12: Emit lifecycle events ───────────────────────────────────
        if status in ("passed", "failed", "timeout"):
            event_name = "test_run_timed_out" if status == "timeout" else "test_run_completed"
            _emit(data_dir, job_id_parsed, event_name, _safe_event_meta(result))
            _emit(data_dir, job_id_parsed, "run_usage_recorded", result.usage_after)
            _emit(data_dir, job_id_parsed, "contract_decision", {
                "action": ContractAction.RUN_TEST,
                "allowed": True,
                "status": "allowed",
                "contract_id": contract.contract_id,
                "test_run_id": test_run_id,
            })
        else:
            _emit(data_dir, job_id_parsed, "test_run_blocked", {
                "test_run_id": test_run_id,
                "reason": "environment_failure",
            })

        # ── Gate 13: Create failure artifact ────────────────────────────────
        if status in ("failed", "timeout", "environment_failure"):
            _create_failure_artifact(
                job_id_parsed, result, data_dir,
                intent_id=request.intent_id,
                apply_id=request.apply_id,
            )

        # ── Guidance ─────────────────────────────────────────────────────────
        if status in ("failed", "timeout"):
            result.next_safe_action = (
                f"remedy repair start {job.id} {result.failure_artifact_id} --json"
                if result.failure_artifact_id
                else f"remedy job show {job.id} --json"
            )
        elif status == "passed":
            result.next_safe_action = f"remedy job show {job.id} --json"

        return result

    finally:
        lease.release()


# ---------------------------------------------------------------------------
# Persistence helpers
# ---------------------------------------------------------------------------


def _persist_test_record(
    job_id: UUID,
    result: TestExecutionResult,
    candidate: Any,
    test_run_id: str,
    created_at: str,
) -> None:
    """Store a safe test record in job metadata. No raw output."""
    try:
        job = load_job(job_id)
        if "test_runs" not in job.metadata:
            job.metadata["test_runs"] = []
        job.metadata["test_runs"].append({
            "test_run_id": test_run_id,
            "contract_id": result.contract_id,
            "command_safe": result.command_safe,
            "status": result.status,
            "exit_code": result.exit_code,
            "duration_ms": result.duration_ms,
            "output_ref": result.output_ref,
            "command_source_type": candidate.source_type if candidate else "",
            "command_source_path": candidate.source_path if candidate else "",
            "command_confidence": candidate.confidence if candidate else "",
            "linked_task_id": result.linked_task_id,
            "linked_intent_id": result.linked_intent_id,
            "linked_apply_id": result.linked_apply_id,
            "created_at": created_at,
        })
        save_job(job)
    except Exception:
        pass  # non-fatal — events are primary record


def _create_failure_artifact(
    job_id: UUID,
    result: TestExecutionResult,
    data_dir: Path,
    *,
    intent_id: str = "",
    apply_id: str = "",
) -> None:
    """Create and persist a TestFailureArtifact. Sets result.failure_artifact_id."""
    try:
        from packages.orchestration.test_failure_artifact import (
            build_test_failure_artifact,
            persist_failure_artifact,
        )
        from packages.orchestration.test_runner import TestRunRecord
        job = load_job(job_id)

        # Build a minimal TestRunRecord for the artifact builder
        record = TestRunRecord(
            test_run_id=result.test_run_id,
            command=result.command_safe,
            status=result.status,
            exit_code=result.exit_code,
            duration_ms=result.duration_ms,
            output_path=result.output_ref,
            output_line_count=0,
            output_bytes=0,
            created_at=datetime.now(timezone.utc).isoformat(),
            blocked_reason="",
            command_source_type="",
            command_source_path="",
            command_purpose="test",
            command_confidence="",
        )

        artifact = build_test_failure_artifact(
            job, record,
            related_intent_id=intent_id,
            related_apply_id=apply_id,
        )
        artifact_obj = persist_failure_artifact(job, artifact)
        save_job(job)

        result.failure_artifact_id = artifact.artifact_id
        _emit(data_dir, job_id, "test_failure_artifact_created", {
            "test_run_id": result.test_run_id,
            "failure_artifact_id": artifact.artifact_id,
            "status": result.status,
        })
    except Exception:
        pass  # non-fatal — result still returned

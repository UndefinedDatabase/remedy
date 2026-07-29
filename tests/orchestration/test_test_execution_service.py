"""Tests for test_execution_service.py — Steps 1088-1097.

Coverage:
  - Models (TestExecutionRequest, TestExecutionResult, TestExecutionLease)
  - Environment policy (_build_safe_env)
  - Timeout derivation (_derive_timeout)
  - Process isolation (_run_isolated_process)
  - Gate order in execute_test_run
  - Usage accounting
  - Failure artifact creation
  - Event emission (smoke)
  - Redaction invariants
  - Concurrency lease
"""

from __future__ import annotations

import os
import sys
from dataclasses import asdict
from pathlib import Path
from unittest.mock import MagicMock, patch
from uuid import uuid4

from packages.orchestration.test_execution_service import (
    TestExecutionLease,
    TestExecutionRequest,
    TestExecutionResult,
    _build_safe_env,
    _derive_timeout,
    _run_isolated_process,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_job(*, permitted: bool = True, target_repo: str | None = None, max_test_runs: int = 1):
    """A REAL Job.

    ``MagicMock(spec=Job)`` only pins the attribute NAMES: every field the test
    does not set answers with a MagicMock, so product code that compares a
    budget or a counter hits `'>' not supported between MagicMock and int`.
    A real model costs nothing here and carries the real defaults.
    """
    from packages.core.models import Job
    metadata = {"target_repo": target_repo} if target_repo else {}
    return Job(name="test-job", metadata=metadata)


def _make_contract(max_test_runs: int = 1, max_runtime_seconds: float = 300.0):
    from packages.core.models import Job
    from packages.orchestration.run_contract import build_default_run_contract
    c = build_default_run_contract(Job(name="test-job"))
    from dataclasses import replace as dc_replace
    return dc_replace(c, max_test_runs=max_test_runs, max_runtime_seconds=max_runtime_seconds)


# ---------------------------------------------------------------------------
# TestExecutionRequest model
# ---------------------------------------------------------------------------


class TestRequestModel:
    def test_defaults(self):
        req = TestExecutionRequest(job_id="abc")
        assert req.job_id == "abc"
        assert req.source == "cli_v1"
        assert req.task_id == ""
        assert req.intent_id == ""
        assert req.apply_id == ""
        assert req.requested_timeout_seconds is None

    def test_with_linkage(self):
        req = TestExecutionRequest(
            job_id="abc",
            task_id="t1",
            intent_id="i1",
            apply_id="a1",
            requested_timeout_seconds=30.0,
        )
        assert req.task_id == "t1"
        assert req.requested_timeout_seconds == 30.0


# ---------------------------------------------------------------------------
# TestExecutionResult model
# ---------------------------------------------------------------------------


class TestResultModel:
    def test_defaults(self):
        r = TestExecutionResult(job_id="abc")
        assert r.status == "blocked"
        assert r.contract_id == ""
        assert r.failure_artifact_id == ""
        assert r.exit_code is None

    def test_no_raw_output_fields(self):
        r = TestExecutionResult(job_id="abc")
        d = asdict(r)
        assert "stdout" not in d
        assert "stderr" not in d
        assert "raw_output" not in d


# ---------------------------------------------------------------------------
# Environment policy
# ---------------------------------------------------------------------------


class TestBuildSafeEnv:
    def test_path_preserved(self):
        env = _build_safe_env({"PATH": "/usr/bin:/bin"})
        assert "PATH" in env
        assert env["PATH"] == "/usr/bin:/bin"

    def test_home_preserved(self):
        env = _build_safe_env({"HOME": "/home/user", "PATH": "/usr/bin"})
        assert "HOME" in env

    def test_api_key_stripped(self):
        env = _build_safe_env({"OPENAI_API_KEY": "sk-secret", "PATH": "/usr/bin"})
        assert "OPENAI_API_KEY" not in env

    def test_token_stripped(self):
        env = _build_safe_env({"GITHUB_TOKEN": "ghp_xxx", "PATH": "/usr/bin"})
        assert "GITHUB_TOKEN" not in env

    def test_secret_stripped(self):
        env = _build_safe_env({"AWS_SECRET_ACCESS_KEY": "secret", "PATH": "/usr/bin"})
        assert "AWS_SECRET_ACCESS_KEY" not in env

    def test_password_stripped(self):
        env = _build_safe_env({"DB_PASSWORD": "hunter2", "PATH": "/usr/bin"})
        assert "DB_PASSWORD" not in env

    def test_credential_stripped(self):
        env = _build_safe_env({"GCP_CREDENTIAL_FILE": "/secrets/key.json", "PATH": "/usr/bin"})
        assert "GCP_CREDENTIAL_FILE" not in env

    def test_virtual_env_preserved(self):
        env = _build_safe_env({"VIRTUAL_ENV": "/home/user/.venv", "PATH": "/usr/bin"})
        assert "VIRTUAL_ENV" in env

    def test_locale_preserved(self):
        env = _build_safe_env({"LANG": "en_US.UTF-8", "LC_ALL": "en_US.UTF-8", "PATH": "/usr/bin"})
        assert "LANG" in env
        assert "LC_ALL" in env

    def test_empty_base(self):
        env = _build_safe_env({})
        assert isinstance(env, dict)
        # No secrets injected
        for key in env:
            assert "token" not in key.lower()
            assert "secret" not in key.lower()
            assert "password" not in key.lower()

    def test_uses_os_environ_when_no_base(self):
        with patch.dict(os.environ, {"PATH": "/usr/bin", "MY_SECRET_TOKEN": "leaked"}, clear=True):
            env = _build_safe_env()
        assert "PATH" in env
        assert "MY_SECRET_TOKEN" not in env


# ---------------------------------------------------------------------------
# Timeout derivation
# ---------------------------------------------------------------------------


class TestDeriveTimeout:
    def test_no_contract_limit_uses_system_max(self):
        t = _derive_timeout(0.0, 0.0, None)  # 0 means unlimited
        from packages.orchestration.test_execution_service import _MAX_SYSTEM_TIMEOUT_SECONDS
        assert t == _MAX_SYSTEM_TIMEOUT_SECONDS

    def test_requested_timeout_limits(self):
        t = _derive_timeout(600.0, 0.0, 30.0)
        assert t == 30.0

    def test_remaining_runtime_limits(self):
        t = _derive_timeout(100.0, 70.0, None)  # 30s remaining
        assert t == 30.0

    def test_no_remaining_runtime_blocks(self):
        t = _derive_timeout(100.0, 100.0, None)
        assert t is None

    def test_minimum_timeout_enforced(self):
        t = _derive_timeout(10.0, 9.0, 0.5)  # 1s remaining, min enforced
        from packages.orchestration.test_execution_service import _MIN_PRACTICAL_TIMEOUT_SECONDS
        assert t >= _MIN_PRACTICAL_TIMEOUT_SECONDS

    def test_uses_min_of_all_limits(self):
        t = _derive_timeout(600.0, 0.0, 45.0)
        assert t == 45.0


# ---------------------------------------------------------------------------
# Process isolation
# ---------------------------------------------------------------------------


class TestRunIsolatedProcess:
    def test_passing_process(self, tmp_path):
        output = tmp_path / "out.txt"
        status, exit_code, dur, _started = _run_isolated_process(
            [sys.executable, "-c", "import sys; sys.exit(0)"],
            cwd=str(tmp_path),
            env=_build_safe_env({"PATH": os.environ.get("PATH", "/usr/bin")}),
            output_file=output,
            timeout_seconds=10.0,
        )
        assert status == "passed"
        assert exit_code == 0
        assert dur >= 0

    def test_failing_process(self, tmp_path):
        output = tmp_path / "out.txt"
        status, exit_code, dur, _started = _run_isolated_process(
            [sys.executable, "-c", "import sys; sys.exit(1)"],
            cwd=str(tmp_path),
            env=_build_safe_env({"PATH": os.environ.get("PATH", "/usr/bin")}),
            output_file=output,
            timeout_seconds=10.0,
        )
        assert status == "failed"
        assert exit_code == 1

    def test_timeout_kills_process(self, tmp_path):
        output = tmp_path / "out.txt"
        status, exit_code, dur, _started = _run_isolated_process(
            [sys.executable, "-c", "import time; time.sleep(60)"],
            cwd=str(tmp_path),
            env=_build_safe_env({"PATH": os.environ.get("PATH", "/usr/bin")}),
            output_file=output,
            timeout_seconds=0.5,
        )
        assert status == "timeout"
        assert exit_code is None

    def test_missing_executable(self, tmp_path):
        output = tmp_path / "out.txt"
        status, exit_code, dur, _started = _run_isolated_process(
            ["/nonexistent/executable_xyz", "--test"],
            cwd=str(tmp_path),
            env=_build_safe_env({"PATH": os.environ.get("PATH", "/usr/bin")}),
            output_file=output,
            timeout_seconds=5.0,
        )
        assert status == "environment_failure"
        assert exit_code is None

    def test_output_written_to_file_not_returned(self, tmp_path):
        output = tmp_path / "out.txt"
        _run_isolated_process(
            [sys.executable, "-c", "print('hello raw output')"],
            cwd=str(tmp_path),
            env=_build_safe_env({"PATH": os.environ.get("PATH", "/usr/bin")}),
            output_file=output,
            timeout_seconds=10.0,
        )
        # Output must be in file, not returned
        assert output.read_bytes() != b""

    def test_no_shell_true(self):
        # Verify _run_isolated_process cannot be called with shell=True
        # by checking the source doesn't contain shell=True in production path
        import inspect

        from packages.orchestration import test_execution_service as svc
        src = inspect.getsource(svc._run_isolated_process)
        assert "shell=True" not in src

    def test_uses_popen_not_subprocess_run(self):
        import inspect

        from packages.orchestration import test_execution_service as svc
        src = inspect.getsource(svc._run_isolated_process)
        assert "subprocess.Popen(" in src
        assert "subprocess.run(" not in src

    def test_start_new_session_used(self):
        import inspect

        from packages.orchestration import test_execution_service as svc
        src = inspect.getsource(svc._run_isolated_process)
        assert "start_new_session=True" in src

    def test_stdin_devnull(self):
        import inspect

        from packages.orchestration import test_execution_service as svc
        src = inspect.getsource(svc._run_isolated_process)
        assert "DEVNULL" in src

    def test_secret_not_in_child_env(self, tmp_path):
        output = tmp_path / "out.txt"
        safe_env = _build_safe_env({
            "PATH": os.environ.get("PATH", "/usr/bin"),
            "MY_SECRET_TOKEN": "leaked_value",
        })
        assert "MY_SECRET_TOKEN" not in safe_env
        # Further: even if someone injected it, process would not see it
        status, _, _, _ = _run_isolated_process(
            [sys.executable, "-c",
             "import os, sys; "
             "val = os.environ.get('MY_SECRET_TOKEN', ''); "
             "sys.exit(0 if not val else 1)"],
            cwd=str(tmp_path),
            env=safe_env,
            output_file=output,
            timeout_seconds=10.0,
        )
        assert status == "passed"


# ---------------------------------------------------------------------------
# Lease
# ---------------------------------------------------------------------------


class TestExecutionLeaseTests:
    def test_acquire_and_release(self, tmp_path):
        lease = TestExecutionLease(
            job_id="test-job",
            lease_path=tmp_path / "test.lock",
        )
        assert lease.acquire(timeout_seconds=2.0)
        lease.release()
        assert not (tmp_path / "test.lock").exists()

    def test_second_acquire_fails(self, tmp_path):
        lock_path = tmp_path / "test.lock"
        lease1 = TestExecutionLease(job_id="test-job", lease_path=lock_path)
        lease2 = TestExecutionLease(job_id="test-job", lease_path=lock_path)
        assert lease1.acquire(timeout_seconds=0.2)
        try:
            # Second lease should fail quickly
            result = lease2.acquire(timeout_seconds=0.1)
            assert not result
        finally:
            lease1.release()

    def test_release_idempotent(self, tmp_path):
        lease = TestExecutionLease(
            job_id="test-job",
            lease_path=tmp_path / "test.lock",
        )
        lease.acquire(timeout_seconds=2.0)
        lease.release()
        lease.release()  # should not raise


class TestDualLeaseTests:
    """Step 1112 — repository-scoped dual lease tests."""

    def test_same_job_blocked(self, tmp_path):
        from packages.orchestration.test_execution_service import DualTestExecutionLease
        job_path = tmp_path / "job.lock"
        repo_path = tmp_path / "repo.lock"
        l1 = DualTestExecutionLease(
            job_lease=TestExecutionLease("j1", job_path),
            repo_lease=TestExecutionLease("r1", repo_path),
        )
        l2 = DualTestExecutionLease(
            job_lease=TestExecutionLease("j1", job_path),
            repo_lease=TestExecutionLease("r1", repo_path),
        )
        ok, reason = l1.acquire(timeout_seconds=0.2)
        assert ok
        try:
            ok2, reason2 = l2.acquire(timeout_seconds=0.1)
            assert not ok2
            assert reason2 == "test_run_already_active"
        finally:
            l1.release()

    def test_different_jobs_same_repo_blocked(self, tmp_path):
        from packages.orchestration.test_execution_service import DualTestExecutionLease
        job1_path = tmp_path / "job1.lock"
        job2_path = tmp_path / "job2.lock"
        repo_path = tmp_path / "repo.lock"  # same repo lease
        l1 = DualTestExecutionLease(
            job_lease=TestExecutionLease("j1", job1_path),
            repo_lease=TestExecutionLease("r1", repo_path),
        )
        l2 = DualTestExecutionLease(
            job_lease=TestExecutionLease("j2", job2_path),
            repo_lease=TestExecutionLease("r1", repo_path),
        )
        ok, reason = l1.acquire(timeout_seconds=0.2)
        assert ok
        try:
            ok2, reason2 = l2.acquire(timeout_seconds=0.1)
            assert not ok2
            assert reason2 == "test_run_already_active_same_repo"
        finally:
            l1.release()

    def test_different_repos_allowed(self, tmp_path):
        from packages.orchestration.test_execution_service import DualTestExecutionLease
        l1 = DualTestExecutionLease(
            job_lease=TestExecutionLease("j1", tmp_path / "job1.lock"),
            repo_lease=TestExecutionLease("r1", tmp_path / "repo1.lock"),
        )
        l2 = DualTestExecutionLease(
            job_lease=TestExecutionLease("j2", tmp_path / "job2.lock"),
            repo_lease=TestExecutionLease("r2", tmp_path / "repo2.lock"),
        )
        ok1, _ = l1.acquire(timeout_seconds=0.2)
        ok2, _ = l2.acquire(timeout_seconds=0.2)
        assert ok1
        assert ok2
        l1.release()
        l2.release()

    def test_release_on_pass_fail_timeout(self, tmp_path):
        from packages.orchestration.test_execution_service import DualTestExecutionLease
        job_path = tmp_path / "job.lock"
        repo_path = tmp_path / "repo.lock"
        lease = DualTestExecutionLease(
            job_lease=TestExecutionLease("j1", job_path),
            repo_lease=TestExecutionLease("r1", repo_path),
        )
        ok, _ = lease.acquire(timeout_seconds=0.2)
        assert ok
        lease.release()
        # After release, both lock files gone
        assert not job_path.exists()
        assert not repo_path.exists()

    def test_stale_lock_recoverable(self, tmp_path):
        """A stale lock file without an active flock is acquirable."""
        from packages.orchestration.test_execution_service import DualTestExecutionLease
        job_path = tmp_path / "job.lock"
        repo_path = tmp_path / "repo.lock"
        # Write stale lock files without holding the flock
        job_path.write_text("stale\n")
        repo_path.write_text("stale\n")
        lease = DualTestExecutionLease(
            job_lease=TestExecutionLease("j1", job_path),
            repo_lease=TestExecutionLease("r1", repo_path),
        )
        ok, _ = lease.acquire(timeout_seconds=0.5)
        assert ok, "Stale lock files should be acquirable"
        lease.release()

    def test_repo_lease_name_stable(self, tmp_path):
        from packages.orchestration.test_execution_service import _repo_lease_name
        repo = tmp_path / "myrepo"
        name1 = _repo_lease_name(repo)
        name2 = _repo_lease_name(repo)
        assert name1 == name2
        assert len(name1) == 32
        assert name1.isalnum()

    def test_repo_lease_name_different_paths(self, tmp_path):
        from packages.orchestration.test_execution_service import _repo_lease_name
        repo_a = tmp_path / "repo_a"
        repo_b = tmp_path / "repo_b"
        assert _repo_lease_name(repo_a) != _repo_lease_name(repo_b)


# ---------------------------------------------------------------------------
# execute_test_run gate order
# ---------------------------------------------------------------------------


class TestExecuteTestRunGates:
    """Tests for all gate checks in execute_test_run."""

    def _make_job_with_repo(self, tmp_path):
        from packages.core.models import Job
        return Job(name="test-job", metadata={"target_repo": str(tmp_path)})

    def test_invalid_job_id_blocked(self):
        from packages.orchestration.test_execution_service import execute_test_run
        req = TestExecutionRequest(job_id="not-a-uuid")
        result = execute_test_run(req)
        assert result.status == "blocked"
        assert result.stop_reason == "invalid_job_id"

    def test_job_not_found_blocked(self):
        from packages.orchestration.test_execution_service import execute_test_run
        req = TestExecutionRequest(job_id=str(uuid4()))
        result = execute_test_run(req)
        assert result.status == "blocked"
        assert result.stop_reason == "job_not_found"

    def test_no_target_repo_blocked(self, tmp_path):
        from packages.orchestration.test_execution_service import execute_test_run

        with patch("packages.orchestration.test_execution_service.resolve_data_root",
                   return_value=tmp_path):
            with patch("packages.orchestration.test_execution_service.load_job") as mock_load:
                job = self._make_job_with_repo(tmp_path)
                job.metadata = {"permissions": {"repo_test_run": "allow"}}  # no target_repo
                mock_load.return_value = job
                req = TestExecutionRequest(job_id=str(job.id))
                result = execute_test_run(req)
        assert result.status == "blocked"
        assert result.stop_reason == "no_target_repo"

    def test_permission_denied_blocked(self, tmp_path):
        from packages.orchestration.test_execution_service import execute_test_run

        with patch("packages.orchestration.test_execution_service.resolve_data_root",
                   return_value=tmp_path):
            with patch("packages.orchestration.test_execution_service.load_job") as mock_load:
                job = self._make_job_with_repo(tmp_path)
                mock_load.return_value = job
                with patch("packages.orchestration.test_execution_service.is_allowed",
                           return_value=False):
                    req = TestExecutionRequest(job_id=str(job.id))
                    result = execute_test_run(req)
        assert result.status == "blocked"
        assert result.stop_reason == "permission_denied"
        assert "repo_test_run" in result.next_safe_action

    def test_contract_budget_zero_blocked(self, tmp_path):
        from packages.orchestration.run_contract import RunUsage
        from packages.orchestration.test_execution_service import execute_test_run

        with patch("packages.orchestration.test_execution_service.resolve_data_root",
                   return_value=tmp_path):
            with patch("packages.orchestration.test_execution_service.load_job") as mock_load:
                job = self._make_job_with_repo(tmp_path)
                mock_load.return_value = job
                with patch("packages.orchestration.test_execution_service.is_allowed",
                           return_value=True):
                    with patch("packages.orchestration.test_execution_service.ensure_contract",
                               return_value=_make_contract(max_test_runs=0)):
                        with patch("packages.orchestration.test_execution_service.load_usage",
                                   return_value=RunUsage()):
                            req = TestExecutionRequest(job_id=str(job.id))
                            result = execute_test_run(req)
        assert result.status == "blocked"
        assert "max_test_runs" in result.safe_summary.lower() or "exhausted" in result.stop_reason

    def test_concurrent_run_blocked(self, tmp_path):
        from packages.orchestration.run_contract import RunUsage
        from packages.orchestration.test_execution_service import execute_test_run

        # Pre-place a lock file to simulate an active run
        ws = tmp_path / "workspaces" / "test-job-id"
        ws.mkdir(parents=True)
        lock_file = ws / "test_execution.lock"

        job = self._make_job_with_repo(tmp_path)
        job_id = uuid4()
        job.id = job_id
        ws2 = tmp_path / "workspaces" / str(job_id)
        ws2.mkdir(parents=True)
        lock2 = ws2 / "test_execution.lock"

        # Acquire a lock in another "process" using the same mechanism
        import fcntl
        fh = open(lock2, "w")
        fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)

        try:
            with patch("packages.orchestration.test_execution_service.resolve_data_root",
                       return_value=tmp_path):
                with patch("packages.orchestration.test_execution_service.load_job",
                           return_value=job):
                    with patch("packages.orchestration.test_execution_service.is_allowed",
                               return_value=True):
                        with patch("packages.orchestration.test_execution_service.ensure_contract",
                                   return_value=_make_contract(max_test_runs=5)):
                            with patch("packages.orchestration.test_execution_service.validate_run_contract",
                                       return_value=[]):
                                with patch("packages.orchestration.test_execution_service.load_usage",
                                           return_value=RunUsage()):
                                    req = TestExecutionRequest(job_id=str(job_id))
                                    result = execute_test_run(req)
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)
            fh.close()
            lock2.unlink(missing_ok=True)

        assert result.status == "blocked"
        assert result.stop_reason == "test_run_already_active"

    def test_no_test_command_blocked(self, tmp_path):
        from packages.orchestration.run_contract import RunUsage
        from packages.orchestration.test_execution_service import execute_test_run

        with patch("packages.orchestration.test_execution_service.resolve_data_root",
                   return_value=tmp_path):
            with patch("packages.orchestration.test_execution_service.load_job") as mock_load:
                job = self._make_job_with_repo(tmp_path)
                mock_load.return_value = job
                with patch("packages.orchestration.test_execution_service.is_allowed",
                           return_value=True):
                    with patch("packages.orchestration.test_execution_service.ensure_contract",
                               return_value=_make_contract(max_test_runs=5)):
                        with patch("packages.orchestration.test_execution_service.validate_run_contract",
                                   return_value=[]):
                            with patch("packages.orchestration.test_execution_service.load_usage",
                                       return_value=RunUsage()):
                                with patch("packages.orchestration.test_execution_service.discover_commands",
                                           return_value=[]):
                                    with patch("packages.orchestration.test_execution_service.select_best_test_candidate",
                                               return_value=None):
                                        req = TestExecutionRequest(job_id=str(job.id))
                                        result = execute_test_run(req)
        assert result.status == "blocked"
        assert result.stop_reason == "no_test_command_discovered"

    def _two_test_candidates(self):
        from packages.orchestration.command_discovery import CommandCandidate
        a = CommandCandidate(
            id="test:makefile:test", purpose="test", argv=("make", "test"),
            display="make test", source_type="makefile", source_path="Makefile",
            confidence="medium", risk="low", reason="", requires_permission="repo_test_run")
        b = CommandCandidate(
            id="test:makefile:check", purpose="test", argv=("make", "check"),
            display="make check", source_type="makefile", source_path="Makefile",
            confidence="medium", risk="low", reason="", requires_permission="repo_test_run")
        return [a, b]

    def _run_with_candidates(self, tmp_path, candidates, command_id, captured):
        """Drive execute_test_run with discovery stubbed to `candidates` and the real
        process replaced by a capture. Returns the TestExecutionResult."""
        from packages.orchestration.run_contract import RunUsage
        from packages.orchestration.test_execution_service import execute_test_run

        def fake_run(argv, *, cwd, env, output_file, timeout_seconds):
            captured["argv"] = list(argv)
            Path(output_file).write_bytes(b"ok\n")
            return "passed", 0, 5, True

        with patch("packages.orchestration.test_execution_service.resolve_data_root",
                   return_value=tmp_path):
            with patch("packages.orchestration.test_execution_service.load_job") as mock_load:
                job = self._make_job_with_repo(tmp_path)
                mock_load.return_value = job
                with patch("packages.orchestration.test_execution_service.is_allowed",
                           return_value=True), \
                     patch("packages.orchestration.test_execution_service.ensure_contract",
                           return_value=_make_contract(max_test_runs=5)), \
                     patch("packages.orchestration.test_execution_service.validate_run_contract",
                           return_value=[]), \
                     patch("packages.orchestration.test_execution_service.load_usage",
                           return_value=RunUsage()), \
                     patch("packages.orchestration.test_execution_service.save_usage"), \
                     patch("packages.orchestration.test_execution_service.save_job"), \
                     patch("packages.orchestration.test_execution_service.discover_commands",
                           return_value=candidates), \
                     patch("packages.orchestration.test_execution_service._run_isolated_process",
                           side_effect=fake_run):
                    req = TestExecutionRequest(job_id=str(job.id), command_id=command_id)
                    return execute_test_run(req)

    def test_explicit_command_id_executes_that_command(self, tmp_path):
        """R-0104: an explicit command_id runs and reports exactly that command."""
        captured: dict = {}
        result = self._run_with_candidates(
            tmp_path, self._two_test_candidates(), "test:makefile:test", captured)
        assert result.status == "passed"
        assert result.command_id == "test:makefile:test"
        assert captured["argv"] == ["make", "test"]

    def test_command_id_not_silently_swapped(self, tmp_path):
        """R-0104: requesting the non-best candidate must NOT fall back to select_best."""
        # select_best would pick "check" (lexicographically smaller id); we request "test".
        captured: dict = {}
        result = self._run_with_candidates(
            tmp_path, self._two_test_candidates(), "test:makefile:check", captured)
        assert result.command_id == "test:makefile:check"
        assert captured["argv"] == ["make", "check"]

    def test_unknown_command_id_blocked_at_runner(self, tmp_path):
        captured: dict = {}
        result = self._run_with_candidates(
            tmp_path, self._two_test_candidates(), "test:makefile:nope", captured)
        assert result.status == "blocked"
        assert result.stop_reason == "requested_command_not_found"
        assert "argv" not in captured  # never executed

    def test_non_test_command_id_blocked_at_runner(self, tmp_path):
        from packages.orchestration.command_discovery import CommandCandidate
        lint = CommandCandidate(
            id="lint:makefile:lint", purpose="lint", argv=("make", "lint"),
            display="make lint", source_type="makefile", source_path="Makefile",
            confidence="medium", risk="low", reason="", requires_permission="repo_lint_run")
        captured: dict = {}
        result = self._run_with_candidates(tmp_path, [lint], "lint:makefile:lint", captured)
        assert result.status == "blocked"
        assert result.stop_reason == "requested_command_not_test"
        assert "argv" not in captured

    def test_blocked_does_not_consume_usage(self, tmp_path):
        from packages.orchestration.test_execution_service import execute_test_run

        save_usage_calls = []
        with patch("packages.orchestration.test_execution_service.resolve_data_root",
                   return_value=tmp_path):
            with patch("packages.orchestration.test_execution_service.load_job") as mock_load:
                job = self._make_job_with_repo(tmp_path)
                mock_load.return_value = job
                with patch("packages.orchestration.test_execution_service.is_allowed",
                           return_value=False):
                    with patch("packages.orchestration.test_execution_service.save_usage",
                               side_effect=lambda j, u: save_usage_calls.append(u)):
                        req = TestExecutionRequest(job_id=str(job.id))
                        execute_test_run(req)
        # Permission denied before process start — save_usage should NOT be called
        assert len(save_usage_calls) == 0


# ---------------------------------------------------------------------------
# Usage accounting
# ---------------------------------------------------------------------------


class TestUsageAccounting:
    def test_usage_incremented_on_process_start(self, tmp_path):
        """Integration: a passing mini-repo increments test_runs_used by 1."""
        from packages.orchestration.run_contract import RunUsage
        from packages.orchestration.test_execution_service import execute_test_run

        # Create a minimal passing repo
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "test_pass.py").write_text("def test_it(): pass\n")
        (repo / "pyproject.toml").write_text(
            '[tool.pytest.ini_options]\ntestpaths = ["."]\n'
        )

        initial_usage = RunUsage(test_runs_used=0, runtime_seconds_used=0.0)
        captured_usage: list[RunUsage] = []

        def mock_save_usage(job, usage):
            captured_usage.append(RunUsage(
                loops_used=usage.loops_used,
                test_runs_used=usage.test_runs_used,
                runtime_seconds_used=usage.runtime_seconds_used,
            ))

        contract = _make_contract(max_test_runs=5, max_runtime_seconds=60.0)

        with patch("packages.orchestration.test_execution_service.resolve_data_root",
                   return_value=tmp_path):
            with patch("packages.orchestration.test_execution_service.load_job") as mock_load:
                job = MagicMock()
                job.id = uuid4()
                job.metadata = {"target_repo": str(repo)}
                job.tasks = []
                job.artifacts = []
                mock_load.return_value = job
                with patch("packages.orchestration.test_execution_service.is_allowed",
                           return_value=True):
                    with patch("packages.orchestration.test_execution_service.ensure_contract",
                               return_value=contract):
                        with patch("packages.orchestration.test_execution_service.validate_run_contract",
                                   return_value=[]):
                            with patch("packages.orchestration.test_execution_service.load_usage",
                                       return_value=initial_usage):
                                with patch("packages.orchestration.test_execution_service.save_usage",
                                           side_effect=mock_save_usage):
                                    with patch("packages.orchestration.test_execution_service.save_job"):
                                        req = TestExecutionRequest(
                                            job_id=str(job.id),
                                            requested_timeout_seconds=30.0,
                                        )
                                        result = execute_test_run(req)

        # Usage must have been incremented exactly once
        assert len(captured_usage) == 1
        assert captured_usage[0].test_runs_used == 1
        assert captured_usage[0].runtime_seconds_used > 0


# ---------------------------------------------------------------------------
# Architecture guards (Step 1106)
# ---------------------------------------------------------------------------


class TestArchitectureGuards:
    def test_no_shell_true_in_service(self):
        import inspect

        from packages.orchestration import test_execution_service as svc
        # Check the execution functions specifically (not docstrings/comments)
        src = inspect.getsource(svc._run_isolated_process)
        assert "shell=True" not in src
        src2 = inspect.getsource(svc.execute_test_run)
        assert "shell=True" not in src2

    def test_no_subprocess_run_in_execute_path(self):
        import inspect

        from packages.orchestration import test_execution_service as svc
        # The isolation function must use Popen, not subprocess.run
        src = inspect.getsource(svc._run_isolated_process)
        assert "subprocess.Popen(" in src
        assert "subprocess.run(" not in src

    def test_no_env_loading_in_service(self):
        import inspect

        from packages.orchestration import test_execution_service as svc
        # Check that production execution path never loads .env files
        exec_src = inspect.getsource(svc.execute_test_run)
        assert "load_dotenv" not in exec_src
        iso_src = inspect.getsource(svc._run_isolated_process)
        assert "load_dotenv" not in iso_src

    def test_service_has_no_provider_dependency(self):
        import importlib
        svc = importlib.import_module("packages.orchestration.test_execution_service")
        # Must not import any LLM/provider modules at module level
        assert "anthropic" not in dir(svc)
        assert "openai" not in dir(svc)

    def test_service_has_no_source_apply_import(self):
        import inspect

        from packages.orchestration import test_execution_service as svc
        src = inspect.getsource(svc)
        # source_apply should not be imported (no automatic repair)
        assert "from packages.orchestration.source_apply" not in src
        assert "import source_apply" not in src

    def test_result_has_no_raw_output_field(self):
        r = TestExecutionResult(job_id="x")
        field_names = {f.name for f in r.__dataclass_fields__.values()}
        assert "stdout" not in field_names
        assert "stderr" not in field_names
        assert "raw_output" not in field_names
        assert "output_content" not in field_names

    def test_service_calls_isolated_process_not_subprocess_run(self):
        import inspect

        from packages.orchestration import test_execution_service as svc
        src = inspect.getsource(svc.execute_test_run)
        assert "subprocess.run(" not in src
        assert "_run_isolated_process(" in src


class TestCatalogValidation:
    """All next_safe_action strings emitted by execute_test_run must be catalog-backed."""

    def _all_catalog_command_ids(self) -> frozenset[str]:
        from apps.cli.command_catalog import CATALOG as COMMAND_CATALOG
        return frozenset(e.command_id for e in COMMAND_CATALOG)

    def test_test_status_in_catalog(self):
        """test.status must exist since execute_test_run emits it as next_safe_action."""
        ids = self._all_catalog_command_ids()
        assert "test.status" in ids, "test.status missing from command catalog (R-0041)"

    def test_lease_blocked_next_action_references_catalog_command(self, tmp_path):
        """When lease is active, next_safe_action must point to a catalog-backed command."""
        from unittest.mock import patch
        from uuid import uuid4

        from packages.orchestration.run_contract import RunUsage
        from packages.orchestration.test_execution_service import (
            TestExecutionRequest,
            execute_test_run,
        )

        def _make_contract(max_test_runs=5):
            from packages.orchestration.run_contract import ContractAction, RunContract
            return RunContract(
                contract_id="test-contract",
                job_id="test",
                allowed_actions=[ContractAction.RUN_TEST],
                max_test_runs=max_test_runs,
            )

        from packages.core.models import Job
        job = Job(name="catalog-test", user_prompt="")
        job.metadata = {
            "target_repo": str(tmp_path),
            "permissions": {"repo_test_run": "allow"},
        }
        job_id = uuid4()
        job.id = job_id

        ws = tmp_path / "workspaces" / str(job_id)
        ws.mkdir(parents=True)
        lock_path = ws / "test_execution.lock"

        import fcntl
        fh = open(lock_path, "w")
        fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            with patch("packages.orchestration.test_execution_service.resolve_data_root",
                       return_value=tmp_path), \
                 patch("packages.orchestration.test_execution_service.load_job",
                       return_value=job), \
                 patch("packages.orchestration.test_execution_service.is_allowed",
                       return_value=True), \
                 patch("packages.orchestration.test_execution_service.ensure_contract",
                       return_value=_make_contract()), \
                 patch("packages.orchestration.test_execution_service.validate_run_contract",
                       return_value=[]), \
                 patch("packages.orchestration.test_execution_service.load_usage",
                       return_value=RunUsage()):
                result = execute_test_run(TestExecutionRequest(job_id=str(job_id)))
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)
            fh.close()
            lock_path.unlink(missing_ok=True)

        assert result.stop_reason == "test_run_already_active"
        # next_safe_action must be a valid catalog command
        action = result.next_safe_action
        catalog_ids = self._all_catalog_command_ids()
        # Extract first word sequence that looks like a command (e.g. "remedy test status <job_id>")
        parts = action.split()
        if len(parts) >= 3:
            cmd_group = parts[1]  # "test"
            cmd_sub = parts[2]    # "status"
            cmd_id = f"{cmd_group}.{cmd_sub}"
            assert cmd_id in catalog_ids, (
                f"next_safe_action {action!r} references non-catalog command {cmd_id!r}"
            )

    def test_test_status_command_has_handler(self):
        """test.status must have a registered handler."""
        from apps.cli.commands import collect_all_handlers
        handlers = collect_all_handlers()
        assert "test.status" in handlers, "test.status has no handler registered"

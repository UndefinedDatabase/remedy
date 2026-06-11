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
import subprocess
import sys
import tempfile
import time
from dataclasses import asdict
from pathlib import Path
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

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
    from packages.core.models import Job, RunState
    job = MagicMock(spec=Job)
    job.id = uuid4()
    job.name = "test-job"
    job.metadata = {}
    job.tasks = []
    job.artifacts = []
    if target_repo:
        job.metadata["target_repo"] = target_repo
    return job


def _make_contract(max_test_runs: int = 1, max_runtime_seconds: float = 300.0):
    from packages.orchestration.run_contract import build_default_run_contract
    from packages.core.models import Job
    job = MagicMock()
    job.id = uuid4()
    job.metadata = {}
    job.tasks = []
    job.artifacts = []
    c = build_default_run_contract(job)
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
        status, exit_code, dur = _run_isolated_process(
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
        status, exit_code, dur = _run_isolated_process(
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
        status, exit_code, dur = _run_isolated_process(
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
        status, exit_code, dur = _run_isolated_process(
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
        status, _, _ = _run_isolated_process(
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


# ---------------------------------------------------------------------------
# execute_test_run gate order
# ---------------------------------------------------------------------------


class TestExecuteTestRunGates:
    """Tests for all gate checks in execute_test_run."""

    def _make_job_with_repo(self, tmp_path):
        from packages.core.models import Job, RunState
        job = MagicMock(spec=Job)
        job.id = uuid4()
        job.name = "test-job"
        job.tasks = []
        job.artifacts = []
        job.metadata = {"target_repo": str(tmp_path)}
        return job

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
        from packages.orchestration.storage import load_job, save_job
        from packages.core.models import Job, RunState

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
        from packages.orchestration.test_execution_service import execute_test_run
        from packages.orchestration.run_contract import RunUsage

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
        from packages.orchestration.test_execution_service import execute_test_run
        from packages.orchestration.run_contract import RunUsage

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
        from packages.orchestration.test_execution_service import execute_test_run
        from packages.orchestration.run_contract import RunUsage

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

    def test_blocked_does_not_consume_usage(self, tmp_path):
        from packages.orchestration.test_execution_service import execute_test_run
        from packages.orchestration.run_contract import RunUsage

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
        import os
        from packages.orchestration.test_execution_service import execute_test_run
        from packages.orchestration.run_contract import RunUsage, export_usage_json

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

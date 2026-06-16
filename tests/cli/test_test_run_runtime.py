"""Runtime subprocess tests: ``remedy test run`` — Step 1104.

Each test:
  - Creates a tiny temporary repository (no flock, direct JSON writes)
  - Runs ``python -m apps.cli.grouped test run <job_id>`` as a real subprocess
  - Verifies gate behavior, output shape, and resource safety

Rules enforced here:
  - No shell=True
  - No background pytest
  - No in-process handler calls
  - Tiny temp repos only
"""

from __future__ import annotations

import fcntl
import json
from pathlib import Path
from uuid import uuid4

from tests.cli.runtime_helpers import create_test_env, run_grouped_cli

# ---------------------------------------------------------------------------
# Tiny repo factory
# ---------------------------------------------------------------------------

def _make_tiny_repo(parent: Path, *, test_content: str) -> Path:
    """Create a minimal Python repo that command_discovery can discover."""
    repo = parent / f"tiny_repo_{uuid4().hex[:8]}"
    repo.mkdir(parents=True)
    (repo / "pyproject.toml").write_text(
        '[tool.pytest.ini_options]\ntestpaths = ["tests"]\n'
    )
    tests_dir = repo / "tests"
    tests_dir.mkdir()
    (tests_dir / "__init__.py").write_text("")
    (tests_dir / "test_main.py").write_text(test_content)
    return repo


# ---------------------------------------------------------------------------
# Job setup helpers (direct JSON writes — no flock imports)
# ---------------------------------------------------------------------------

_CONTRACT_TEMPLATE: dict = {
    "version": 1,
    "scope": "full",
    "autonomy_level": "supervised",
    # Use canonical ContractAction values from run_contract.py
    "allowed_actions": [
        "plan", "context", "build_artifact", "create_patch_intent",
        "create_fix_task", "discover_commands", "write_metadata", "run_test",
    ],
    "denied_actions": [],
    "max_loops": 10,
    "max_test_runs": 3,
    "max_runtime_seconds": 3600.0,
    "max_tokens": 0,
    "max_cost_cents": 0,
    "allowed_paths": [],
    "denied_paths": [],
    "stop_before_apply": True,
    "stop_on_unknown_risk": True,
    "stop_on_medium_risk": False,
    "prefer_local": True,
    "no_cloud": False,
    "model_policy": "",
    "command_policy": "",
    "stop_conditions": [],
    "requires_approval_for": [
        "patch_apply", "apply", "source_apply", "arbitrary_shell",
        "cloud_provider", "network_fetch", "install_packages",
    ],
    "source": "test_v1",
    "notes": "",
}


def _make_job_with_repo(
    data_root: Path,
    job_id: str,
    repo_path: Path,
    *,
    allow_test: bool = True,
    max_test_runs: int = 3,
) -> None:
    """Patch a job JSON to add target_repo, permissions, and run_contract."""
    job_file = data_root / "jobs" / f"{job_id}.json"
    job_data = json.loads(job_file.read_text())

    job_data["metadata"]["target_repo"] = str(repo_path)

    if allow_test:
        job_data["metadata"].setdefault("permissions", {})
        job_data["metadata"]["permissions"]["repo_test_run"] = "allow"

    contract = dict(_CONTRACT_TEMPLATE)
    contract["contract_id"] = uuid4().hex
    contract["job_id"] = job_id
    contract["max_test_runs"] = max_test_runs
    from datetime import datetime, timezone
    contract["created_at"] = datetime.now(timezone.utc).isoformat()
    job_data["metadata"]["run_contract"] = contract

    job_file.write_text(json.dumps(job_data, indent=2))


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestMissingJobSafe:
    """Missing/invalid job IDs must not traceback."""

    def test_missing_job_blocked(self, tmp_path: Path):
        data_root, _ = create_test_env(tmp_path)
        missing_id = "00000000-0000-0000-0000-000000000000"
        r = run_grouped_cli(["test", "run", missing_id], data_root, timeout=15)
        assert r.returncode != 0
        assert "Traceback" not in r.stderr
        assert "Traceback" not in r.stdout

    def test_invalid_uuid_safe(self, tmp_path: Path):
        data_root, _ = create_test_env(tmp_path)
        r = run_grouped_cli(["test", "run", "not-a-valid-uuid"], data_root, timeout=15)
        assert r.returncode != 0
        assert "Traceback" not in r.stderr


class TestPermissionGate:
    """Permission denied blocks run before any subprocess is launched."""

    def test_permission_denied_blocks(self, tmp_path: Path):
        data_root, job_id = create_test_env(tmp_path)
        repo = _make_tiny_repo(tmp_path, test_content="def test_ok(): pass")
        # Do NOT grant repo_test_run permission
        _make_job_with_repo(data_root, job_id, repo, allow_test=False, max_test_runs=3)

        r = run_grouped_cli(["test", "run", job_id], data_root, timeout=15)
        assert r.returncode != 0
        assert "Traceback" not in r.stderr
        # Guidance should suggest the permit command
        combined = r.stdout + r.stderr
        assert "repo_test_run" in combined

    def test_permission_denied_json(self, tmp_path: Path):
        data_root, job_id = create_test_env(tmp_path)
        repo = _make_tiny_repo(tmp_path, test_content="def test_ok(): pass")
        _make_job_with_repo(data_root, job_id, repo, allow_test=False, max_test_runs=3)

        r = run_grouped_cli(["test", "run", job_id, "--json"], data_root, timeout=15)
        assert r.returncode != 0
        out = json.loads(r.stdout)
        assert out["status"] == "blocked"
        assert out["stop_reason"] == "permission_denied"


class TestZeroBudgetGate:
    """max_test_runs=0 blocks run before any subprocess is launched."""

    def test_zero_budget_blocks(self, tmp_path: Path):
        data_root, job_id = create_test_env(tmp_path)
        repo = _make_tiny_repo(tmp_path, test_content="def test_ok(): pass")
        _make_job_with_repo(data_root, job_id, repo, allow_test=True, max_test_runs=0)

        r = run_grouped_cli(["test", "run", job_id], data_root, timeout=15)
        assert r.returncode != 0
        combined = r.stdout + r.stderr
        assert "max_test_runs" in combined

    def test_zero_budget_json(self, tmp_path: Path):
        data_root, job_id = create_test_env(tmp_path)
        repo = _make_tiny_repo(tmp_path, test_content="def test_ok(): pass")
        _make_job_with_repo(data_root, job_id, repo, allow_test=True, max_test_runs=0)

        r = run_grouped_cli(["test", "run", job_id, "--json"], data_root, timeout=15)
        assert r.returncode != 0
        out = json.loads(r.stdout)
        assert out["status"] == "blocked"
        assert "exhausted" in out["stop_reason"] or "zero" in out["stop_reason"].lower() or "max_test_runs" in out.get("safe_summary", "")


class TestSuccessfulRun:
    """A one-test passing repository returns rc=0 with PASSED status."""

    def test_passing_repo_rc_zero(self, tmp_path: Path):
        data_root, job_id = create_test_env(tmp_path)
        repo = _make_tiny_repo(tmp_path, test_content="def test_ok(): pass\n")
        _make_job_with_repo(data_root, job_id, repo)

        r = run_grouped_cli(["test", "run", job_id], data_root, timeout=30)
        assert r.returncode == 0, f"Expected rc=0, got {r.returncode}. stderr={r.stderr[:200]}"
        assert "PASSED" in r.stdout

    def test_passing_repo_json(self, tmp_path: Path):
        data_root, job_id = create_test_env(tmp_path)
        repo = _make_tiny_repo(tmp_path, test_content="def test_ok(): pass\n")
        _make_job_with_repo(data_root, job_id, repo)

        r = run_grouped_cli(["test", "run", job_id, "--json"], data_root, timeout=30)
        assert r.returncode == 0, f"Expected rc=0. stderr={r.stderr[:200]}"
        out = json.loads(r.stdout)
        assert out["status"] == "passed"
        assert out["job_id"] == job_id
        assert out["test_run_id"]
        assert out["exit_code"] == 0

    def test_passing_run_no_raw_output_in_json(self, tmp_path: Path):
        """JSON result must not include raw stdout/stderr from the test process."""
        data_root, job_id = create_test_env(tmp_path)
        # Embed a distinctive string in test output
        repo = _make_tiny_repo(
            tmp_path,
            test_content='def test_ok():\n    print("REMEDY_SECRET_CANARY_12345")\n',
        )
        _make_job_with_repo(data_root, job_id, repo)

        r = run_grouped_cli(["test", "run", job_id, "--json"], data_root, timeout=30)
        assert r.returncode == 0
        out = json.loads(r.stdout)
        # Raw output must not appear in the result
        assert "REMEDY_SECRET_CANARY_12345" not in r.stdout
        assert "REMEDY_SECRET_CANARY_12345" not in r.stderr
        # output_ref is a filename, not content
        assert out.get("output_ref", "").endswith(".txt") or out.get("output_ref") == ""


class TestFailingRun:
    """A one-test failing repository returns rc!=0 with FAILED status."""

    def test_failing_repo_rc_nonzero(self, tmp_path: Path):
        data_root, job_id = create_test_env(tmp_path)
        repo = _make_tiny_repo(
            tmp_path, test_content="def test_fail(): assert False, 'intentional'\n"
        )
        _make_job_with_repo(data_root, job_id, repo)

        r = run_grouped_cli(["test", "run", job_id], data_root, timeout=30)
        assert r.returncode != 0
        assert "FAILED" in r.stderr

    def test_failing_repo_json(self, tmp_path: Path):
        data_root, job_id = create_test_env(tmp_path)
        repo = _make_tiny_repo(
            tmp_path, test_content="def test_fail(): assert False\n"
        )
        _make_job_with_repo(data_root, job_id, repo)

        r = run_grouped_cli(["test", "run", job_id, "--json"], data_root, timeout=30)
        assert r.returncode != 0
        out = json.loads(r.stdout)
        assert out["status"] == "failed"
        assert out["exit_code"] != 0

    def test_failing_repo_creates_failure_artifact(self, tmp_path: Path):
        data_root, job_id = create_test_env(tmp_path)
        repo = _make_tiny_repo(
            tmp_path, test_content="def test_fail(): assert False\n"
        )
        _make_job_with_repo(data_root, job_id, repo)

        r = run_grouped_cli(["test", "run", job_id, "--json"], data_root, timeout=30)
        assert r.returncode != 0
        out = json.loads(r.stdout)
        assert out.get("failure_artifact_id"), "failing run must create a failure artifact"


class TestTimeoutRun:
    """Test that sleeps beyond the contract limit is killed and reported as timeout."""

    def test_timeout_status(self, tmp_path: Path):
        data_root, job_id = create_test_env(tmp_path)
        repo = _make_tiny_repo(
            tmp_path,
            test_content="import time\ndef test_sleep(): time.sleep(30)\n",
        )
        _make_job_with_repo(data_root, job_id, repo)

        r = run_grouped_cli(
            ["test", "run", job_id, "--timeout-seconds", "2"],
            data_root,
            timeout=30,
        )
        assert r.returncode != 0
        out_text = r.stdout + r.stderr
        assert "TIMEOUT" in out_text

    def test_timeout_json(self, tmp_path: Path):
        data_root, job_id = create_test_env(tmp_path)
        repo = _make_tiny_repo(
            tmp_path,
            test_content="import time\ndef test_sleep(): time.sleep(30)\n",
        )
        _make_job_with_repo(data_root, job_id, repo)

        r = run_grouped_cli(
            ["test", "run", job_id, "--timeout-seconds", "2", "--json"],
            data_root,
            timeout=30,
        )
        assert r.returncode != 0
        out = json.loads(r.stdout)
        assert out["status"] == "timeout"
        assert out.get("failure_artifact_id"), "timeout must create failure artifact"


class TestConcurrentRunBlocked:
    """Second run while a lease is held returns test_run_already_active."""

    def test_lease_held_blocks(self, tmp_path: Path):
        data_root, job_id = create_test_env(tmp_path)
        repo = _make_tiny_repo(tmp_path, test_content="def test_ok(): pass\n")
        _make_job_with_repo(data_root, job_id, repo)

        # Acquire the lease file directly to simulate an in-progress run
        workspace_dir = data_root / "workspaces" / job_id
        workspace_dir.mkdir(parents=True, exist_ok=True)
        lease_path = workspace_dir / "test_execution.lock"

        with open(lease_path, "w") as lf:
            fcntl.flock(lf, fcntl.LOCK_EX | fcntl.LOCK_NB)
            try:
                r = run_grouped_cli(["test", "run", job_id, "--json"], data_root, timeout=20)
                assert r.returncode != 0
                out = json.loads(r.stdout)
                assert out["status"] == "blocked"
                assert out["stop_reason"] == "test_run_already_active"
            finally:
                fcntl.flock(lf, fcntl.LOCK_UN)


class TestJsonOutput:
    """--json flag produces parseable JSON with required keys."""

    def test_json_has_required_keys(self, tmp_path: Path):
        data_root, job_id = create_test_env(tmp_path)
        repo = _make_tiny_repo(tmp_path, test_content="def test_ok(): pass\n")
        _make_job_with_repo(data_root, job_id, repo)

        r = run_grouped_cli(["test", "run", job_id, "--json"], data_root, timeout=30)
        out = json.loads(r.stdout)
        required = {"job_id", "test_run_id", "status", "contract_id"}
        missing = required - out.keys()
        assert not missing, f"JSON missing keys: {missing}"

    def test_json_blocked_has_next_safe_action(self, tmp_path: Path):
        data_root, job_id = create_test_env(tmp_path)
        repo = _make_tiny_repo(tmp_path, test_content="def test_ok(): pass\n")
        _make_job_with_repo(data_root, job_id, repo, allow_test=False)

        r = run_grouped_cli(["test", "run", job_id, "--json"], data_root, timeout=15)
        out = json.loads(r.stdout)
        assert out.get("next_safe_action"), "blocked result must include next_safe_action"

    def test_json_passed_has_usage(self, tmp_path: Path):
        data_root, job_id = create_test_env(tmp_path)
        repo = _make_tiny_repo(tmp_path, test_content="def test_ok(): pass\n")
        _make_job_with_repo(data_root, job_id, repo)

        r = run_grouped_cli(["test", "run", job_id, "--json"], data_root, timeout=30)
        assert r.returncode == 0
        out = json.loads(r.stdout)
        usage = out.get("usage_after", {})
        assert usage.get("test_runs_used", 0) >= 1


class TestExplicitTimeout:
    """--timeout-seconds propagates correctly to the service."""

    def test_explicit_timeout_passes_fast_test(self, tmp_path: Path):
        data_root, job_id = create_test_env(tmp_path)
        repo = _make_tiny_repo(tmp_path, test_content="def test_ok(): pass\n")
        _make_job_with_repo(data_root, job_id, repo)

        r = run_grouped_cli(
            ["test", "run", job_id, "--timeout-seconds", "30"],
            data_root,
            timeout=45,
        )
        assert r.returncode == 0


class TestArchitectureGuards:
    """Source-level safety invariants for the test execution path."""

    def test_no_shell_true_in_test_execution_service(self):
        from pathlib import Path as _Path
        src = (_Path(__file__).parent.parent.parent
               / "packages" / "orchestration" / "test_execution_service.py"
               ).read_text()
        # Match shell=True not inside comments or docstrings (check Popen calls)
        popen_lines = [
            ln for ln in src.splitlines()
            if "subprocess.Popen(" in ln or "subprocess.run(" in ln
        ]
        for line in popen_lines:
            assert "shell=True" not in line, f"shell=True found in: {line.strip()}"

    def test_no_shell_true_in_test_cmds(self):
        from pathlib import Path as _Path
        src = (_Path(__file__).parent.parent.parent
               / "apps" / "cli" / "commands" / "test_cmds.py"
               ).read_text()
        assert "shell=True" not in src

    def test_no_capture_output_in_run_isolated_process(self):
        import inspect

        from packages.orchestration.test_execution_service import _run_isolated_process
        src = inspect.getsource(_run_isolated_process)
        # Must use Popen, not subprocess.run
        assert "subprocess.run(" not in src, "must use Popen, not subprocess.run"
        # subprocess call lines must not use capture_output
        subprocess_lines = [ln for ln in src.splitlines() if "subprocess.Popen(" in ln or "subprocess.run(" in ln]
        for ln in subprocess_lines:
            assert "capture_output" not in ln, f"capture_output in: {ln.strip()}"

    def test_no_traceback_on_missing_repo_dir(self, tmp_path: Path):
        """Missing target_repo directory must be handled gracefully."""
        data_root, job_id = create_test_env(tmp_path)
        # Set target_repo to a path that doesn't exist
        job_file = data_root / "jobs" / f"{job_id}.json"
        job_data = json.loads(job_file.read_text())
        job_data["metadata"]["target_repo"] = str(tmp_path / "nonexistent_repo")
        job_data["metadata"].setdefault("permissions", {})
        job_data["metadata"]["permissions"]["repo_test_run"] = "allow"
        job_file.write_text(json.dumps(job_data, indent=2))

        r = run_grouped_cli(["test", "run", job_id], data_root, timeout=15)
        assert r.returncode != 0
        assert "Traceback" not in r.stderr

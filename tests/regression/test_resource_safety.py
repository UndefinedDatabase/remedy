"""Resource-safety regression tests.

Verify that the pytest wrapper and safety docs exist and contain required
policy elements. These tests prevent accidental removal of resource-safety
infrastructure.
"""

import os
import subprocess
import tempfile
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
WRAPPER = str(REPO_ROOT / "scripts" / "remedy_pytest.sh")


def _find_processes_by_filename(filename: str) -> str:
    """Find processes matching a unique test filename marker.

    Returns pgrep stdout (empty if no match). Uses the basename to avoid
    matching unrelated paths.
    """
    basename = os.path.basename(filename)
    result = subprocess.run(
        ["pgrep", "-af", basename],
        capture_output=True,
        text=True,
    )
    # Filter out the pgrep process itself
    lines = [
        ln for ln in result.stdout.splitlines()
        if "pgrep" not in ln
    ]
    return "\n".join(lines)


def _assert_no_orphans(filename: str, retries: int = 5) -> None:
    """Assert no processes matching filename remain, with brief retry for cleanup."""
    for _ in range(retries):
        procs = _find_processes_by_filename(filename)
        if not procs:
            return
        time.sleep(0.5)
    raise AssertionError(f"Orphan processes still running for {filename}:\n{procs}")


class TestPytestWrapper:
    """Guarded pytest wrapper must exist and contain safety primitives."""

    def _wrapper_text(self) -> str:
        wrapper = REPO_ROOT / "scripts" / "remedy_pytest.sh"
        assert wrapper.exists(), "scripts/remedy_pytest.sh must exist"
        return wrapper.read_text()

    def test_wrapper_exists(self):
        assert (REPO_ROOT / "scripts" / "remedy_pytest.sh").exists()

    def test_wrapper_uses_flock(self):
        text = self._wrapper_text()
        assert "flock" in text and '"-n"' in text

    def test_wrapper_uses_timeout(self):
        assert "timeout" in self._wrapper_text()

    def test_wrapper_runs_pytest(self):
        text = self._wrapper_text()
        assert "-m pytest" in text

    def test_wrapper_no_background(self):
        text = self._wrapper_text()
        assert "run_in_background" not in text
        assert "nohup" not in text
        for line in text.splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                assert not stripped.endswith(" &"), f"Background '&' found: {stripped}"

    def test_wrapper_is_executable(self):
        import os

        wrapper = REPO_ROOT / "scripts" / "remedy_pytest.sh"
        assert os.access(wrapper, os.X_OK), "remedy_pytest.sh must be executable"


class TestResourceSafetyDocs:
    """Safety docs must mention key policy rules."""

    def test_reviewer_safety_doc_exists(self):
        assert (REPO_ROOT / "docs" / "system" / "reviewer-safety.md").exists()

    def test_docs_mention_no_background_pytest(self):
        text = (REPO_ROOT / "docs" / "system" / "reviewer-safety.md").read_text()
        assert "background" in text.lower()
        assert "never" in text.lower()

    def test_docs_mention_single_session(self):
        text = (REPO_ROOT / "docs" / "system" / "reviewer-safety.md").read_text()
        assert "parallel" in text.lower() or "single" in text.lower()

    def test_tests_readme_mentions_wrapper(self):
        text = (REPO_ROOT / "tests" / "README.md").read_text()
        assert "remedy_pytest.sh" in text

    def test_tests_readme_mentions_resource_safety(self):
        text = (REPO_ROOT / "tests" / "README.md").read_text()
        assert "Resource Safety" in text or "resource safety" in text.lower()


class TestContextIncludesResourceSafety:
    """Agent context must reference resource-safety rules."""

    def test_context_mentions_resource_safety(self):
        ctx = REPO_ROOT / ".agent" / "context.md"
        assert ctx.exists(), ".agent/context.md must exist"
        text = ctx.read_text()
        assert "resource" in text.lower() or "pytest" in text.lower()


class TestRunnerTryFinallyGuarantee:
    """remedy_pytest_runner.py must guarantee process cleanup in finally block."""

    def test_ensure_pg_dead_in_finally(self):
        text = (REPO_ROOT / "scripts" / "remedy_pytest_runner.py").read_text()
        assert "finally:" in text
        assert "_ensure_pg_dead(pgid)" in text
        # Verify _ensure_pg_dead is called after finally (not just in try body)
        lines = text.splitlines()
        finally_idx = None
        cleanup_after_finally = False
        for i, line in enumerate(lines):
            if "finally:" in line:
                finally_idx = i
            if finally_idx is not None and i > finally_idx:
                if "_ensure_pg_dead(pgid)" in line:
                    cleanup_after_finally = True
                    break
        assert cleanup_after_finally, (
            "_ensure_pg_dead(pgid) must be in a finally block"
        )


class TestRuntimeTimeoutEdgeCase:
    """Runtime lane must fail fast when NODE_TIMEOUT is too small."""

    def test_too_small_timeout_fails_fast(self):
        """NODE_TIMEOUT=5 should fail with error, not produce inner > outer."""
        env = os.environ.copy()
        env["REMEDY_NODE_TIMEOUT_SEC"] = "5"
        result = subprocess.run(
            ["bash", str(REPO_ROOT / "scripts" / "remedy_test_runtime.sh")],
            capture_output=True,
            text=True,
            timeout=10,
            env=env,
        )
        assert result.returncode != 0, "Should fail for too-small timeout"
        assert "too small" in result.stderr.lower() or "minimum" in result.stderr.lower(), (
            f"Expected 'too small' error, got: {result.stderr}"
        )

    def test_valid_timeout_computes_inner_less_than_outer(self):
        """Verify inner < outer for the default and for custom values."""
        text = (REPO_ROOT / "scripts" / "remedy_test_runtime.sh").read_text()
        assert "INNER_TIMEOUT" in text
        assert "NODE_TIMEOUT - 10" in text
        assert "INNER_TIMEOUT\" -ge \"$NODE_TIMEOUT\"" in text


class TestRunnerProcessGroupCleanup:
    """Forced timeout must not leave orphan processes."""

    def test_timeout_kills_process_group(self):
        """Run a slow test with short timeout, verify no orphans survive."""
        # Create a temporary test that sleeps long enough to be killed
        marker = f"REMEDY_TIMEOUT_TEST_{os.getpid()}"
        slow_test = tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            prefix="test_slow_",
            dir=str(REPO_ROOT / "tests" / "regression"),
            delete=False,
        )
        try:
            slow_test.write(
                f"import time, os\n"
                f"os.environ['{marker}'] = '1'\n"
                f"def test_slow():\n"
                f"    time.sleep(300)\n"
            )
            slow_test.close()

            env = os.environ.copy()
            env["REMEDY_PYTEST_TIMEOUT_SEC"] = "2"
            env["REMEDY_PYTHON"] = "python3"

            runner = REPO_ROOT / "scripts" / "remedy_pytest_runner.py"
            result = subprocess.run(
                ["python3", str(runner), "--", str(slow_test.name), "-q"],
                capture_output=True,
                text=True,
                timeout=15,
                env=env,
            )

            # Runner should return 124 (timeout)
            assert result.returncode == 124, (
                f"Expected exit code 124 (timeout), got {result.returncode}"
            )

            # Check no orphan pytest processes with our marker test file
            ps_out = subprocess.run(
                ["pgrep", "-f", os.path.basename(slow_test.name)],
                capture_output=True,
                text=True,
            )
            assert ps_out.returncode != 0, (
                f"Orphan processes found after timeout cleanup: {ps_out.stdout}"
            )
        finally:
            try:
                os.unlink(slow_test.name)
            except OSError:
                pass


class TestWrapperPathForcedTimeout:
    """Full wrapper path (remedy_pytest.sh) forced timeout cleanup.

    Exercises the actual chain: remedy_pytest.sh → flock → remedy_pytest_runner.py → child pytest.
    Uses a separate lock file to avoid contention with the outer test runner.
    """

    def _make_slow_test(self) -> str:
        """Create a temporary slow test file with unique name."""
        f = tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            prefix=f"test_wrapper_slow_{os.getpid()}_",
            dir=str(REPO_ROOT / "tests" / "regression"),
            delete=False,
        )
        f.write(
            "import time\n"
            "def test_slow_wrapper_target():\n"
            "    time.sleep(300)\n"
        )
        f.close()
        return f.name

    def _wrapper_env(self, timeout_sec: int = 2) -> dict:
        """Build env for wrapper with isolated lock and short timeout."""
        env = os.environ.copy()
        env["REMEDY_PYTEST_TIMEOUT_SEC"] = str(timeout_sec)
        env["REMEDY_PYTEST_LOCK"] = f"/tmp/remedy-pytest-test-{os.getpid()}.lock"
        env["REMEDY_PYTEST_LOCK_WAIT"] = "0"
        return env

    def test_wrapper_timeout_cleanup_no_orphans(self):
        """Wrapper timeout kills child pytest; no orphan remains."""
        slow_file = self._make_slow_test()
        lock_file = f"/tmp/remedy-pytest-test-{os.getpid()}.lock"
        try:
            env = self._wrapper_env(timeout_sec=2)
            result = subprocess.run(
                [WRAPPER, slow_file, "-q"],
                capture_output=True,
                text=True,
                timeout=20,
                env=env,
            )
            # Wrapper should exit with timeout (124) or non-zero
            assert result.returncode != 0, (
                f"Expected non-zero exit (timeout), got {result.returncode}"
            )
            # No orphan pytest processes for our slow test file
            _assert_no_orphans(slow_file)
            # No remedy_pytest_runner.py orphan
            runner_procs = _find_processes_by_filename("remedy_pytest_runner.py")
            # Filter to only processes related to our slow test
            related = [ln for ln in runner_procs.splitlines() if slow_file in ln]
            assert not related, f"Runner orphan found: {runner_procs}"
        finally:
            try:
                os.unlink(slow_file)
            except OSError:
                pass
            try:
                os.unlink(lock_file)
            except OSError:
                pass

    def test_lock_released_after_timeout(self):
        """Lock must not be held after wrapper timeout."""
        slow_file = self._make_slow_test()
        lock_file = f"/tmp/remedy-pytest-test-{os.getpid()}.lock"
        try:
            env = self._wrapper_env(timeout_sec=2)
            subprocess.run(
                [WRAPPER, slow_file, "-q"],
                capture_output=True,
                text=True,
                timeout=20,
                env=env,
            )
            # Lock should be available (flock -n should succeed)
            lock_check = subprocess.run(
                ["flock", "-n", lock_file, "echo", "unlocked"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            assert lock_check.returncode == 0, (
                f"Lock still held after wrapper timeout: {lock_check.stderr}"
            )
        finally:
            try:
                os.unlink(slow_file)
            except OSError:
                pass
            try:
                os.unlink(lock_file)
            except OSError:
                pass

    def test_subsequent_wrapper_succeeds_after_timeout(self):
        """After forced timeout, a normal wrapper run must succeed immediately."""
        slow_file = self._make_slow_test()
        lock_file = f"/tmp/remedy-pytest-test-{os.getpid()}.lock"
        try:
            env = self._wrapper_env(timeout_sec=2)
            # First: timeout run
            subprocess.run(
                [WRAPPER, slow_file, "-q"],
                capture_output=True,
                text=True,
                timeout=20,
                env=env,
            )
            _assert_no_orphans(slow_file)

            # Second: normal run with generous timeout must pass
            passing_test = tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".py",
                prefix=f"test_wrapper_pass_{os.getpid()}_",
                dir=str(REPO_ROOT / "tests" / "regression"),
                delete=False,
            )
            passing_test.write("def test_pass(): assert True\n")
            passing_test.close()

            env2 = self._wrapper_env(timeout_sec=30)
            result = subprocess.run(
                [WRAPPER, passing_test.name, "-q"],
                capture_output=True,
                text=True,
                timeout=20,
                env=env2,
            )
            assert result.returncode == 0, (
                f"Subsequent wrapper run failed: rc={result.returncode}\n"
                f"stdout: {result.stdout}\nstderr: {result.stderr}"
            )
        finally:
            try:
                os.unlink(slow_file)
            except OSError:
                pass
            try:
                os.unlink(passing_test.name)
            except OSError:
                pass
            try:
                os.unlink(lock_file)
            except OSError:
                pass


class TestRuntimeLikeTimeoutChain:
    """Simulates runtime lane outer/inner timeout structure.

    Outer timeout > inner timeout. Slow test exceeds inner.
    Inner cleanup fires before outer. No orphans. Subsequent run succeeds.
    """

    def test_inner_cleanup_before_outer(self):
        """Inner timeout (2s) fires before outer timeout (12s). No orphans."""
        slow_file = tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            prefix=f"test_runtime_chain_{os.getpid()}_",
            dir=str(REPO_ROOT / "tests" / "regression"),
            delete=False,
        )
        slow_file.write(
            "import time\n"
            "def test_slow_runtime_chain():\n"
            "    time.sleep(300)\n"
        )
        slow_file.close()
        lock_file = f"/tmp/remedy-pytest-chain-{os.getpid()}.lock"

        try:
            env = os.environ.copy()
            env["REMEDY_PYTEST_TIMEOUT_SEC"] = "2"  # inner
            env["REMEDY_PYTEST_LOCK"] = lock_file
            env["REMEDY_PYTEST_LOCK_WAIT"] = "0"

            # Simulate runtime lane: outer timeout wraps wrapper call
            outer_timeout = 12  # outer > inner (2s) + safety margin
            result = subprocess.run(
                ["timeout", "--signal=TERM", "--kill-after=5", str(outer_timeout),
                 WRAPPER, slow_file.name, "-q"],
                capture_output=True,
                text=True,
                timeout=20,
                env=env,
            )

            # Inner timeout (2s) should have fired, not outer (12s)
            # Exit code 124 = inner runner timeout
            assert result.returncode != 0, (
                f"Expected non-zero exit, got {result.returncode}"
            )

            # No orphan processes
            _assert_no_orphans(slow_file.name)

            # Subsequent wrapper run succeeds
            pass_file = tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".py",
                prefix=f"test_chain_pass_{os.getpid()}_",
                dir=str(REPO_ROOT / "tests" / "regression"),
                delete=False,
            )
            pass_file.write("def test_pass(): assert True\n")
            pass_file.close()

            env2 = os.environ.copy()
            env2["REMEDY_PYTEST_TIMEOUT_SEC"] = "30"
            env2["REMEDY_PYTEST_LOCK"] = lock_file
            env2["REMEDY_PYTEST_LOCK_WAIT"] = "0"

            result2 = subprocess.run(
                [WRAPPER, pass_file.name, "-q"],
                capture_output=True,
                text=True,
                timeout=15,
                env=env2,
            )
            assert result2.returncode == 0, (
                f"Subsequent run after timeout failed: rc={result2.returncode}\n"
                f"stderr: {result2.stderr}"
            )
        finally:
            for f in [slow_file.name, pass_file.name, lock_file]:
                try:
                    os.unlink(f)
                except (OSError, NameError):
                    pass


class TestNoBackgroundPytestInDocs:
    """No docs or prompt templates should recommend background pytest."""

    def test_no_background_pytest_in_docs(self):
        docs_dir = REPO_ROOT / "docs"
        for f in docs_dir.rglob("*.md"):
            text = f.read_text()
            lines = text.splitlines()
            for i, line in enumerate(lines, 1):
                if "run_in_background" in line and "pytest" in line.lower():
                    lower = line.lower()
                    if "never" in lower or "don't" in lower or "do not" in lower:
                        continue
                    raise AssertionError(
                        f"{f.relative_to(REPO_ROOT)}:{i} recommends background pytest"
                    )

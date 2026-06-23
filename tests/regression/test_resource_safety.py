"""Resource-safety regression tests.

Verify that the pytest wrapper and safety docs exist and contain required
policy elements. These tests prevent accidental removal of resource-safety
infrastructure.
"""

import os
import subprocess
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


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
        assert (REPO_ROOT / "docs" / "reviewer-safety.md").exists()

    def test_docs_mention_no_background_pytest(self):
        text = (REPO_ROOT / "docs" / "reviewer-safety.md").read_text()
        assert "background" in text.lower()
        assert "never" in text.lower()

    def test_docs_mention_single_session(self):
        text = (REPO_ROOT / "docs" / "reviewer-safety.md").read_text()
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

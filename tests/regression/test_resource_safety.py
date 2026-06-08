"""Resource-safety regression tests.

Verify that the pytest wrapper and safety docs exist and contain required
policy elements. These tests prevent accidental removal of resource-safety
infrastructure.
"""

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
        assert "flock -n" in self._wrapper_text()

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

"""Main Orchestrator Brain v0 architecture guards (Step 1490).

The module keeps only the decision-trace reader the cockpit calls; these guards keep it free of
execution, provider, network and git imports.
"""
from __future__ import annotations

from pathlib import Path


class TestArchitectureGuards:
    SRC = Path("packages/orchestration/orchestrator_brain.py").read_text()

    def _imports(self):
        return [ln for ln in self.SRC.splitlines()
                if ln.strip().startswith(("import ", "from "))]

    def test_no_network_subprocess(self):
        for ln in self._imports():
            for bad in ("subprocess", "socket", "requests", "httpx", "urllib", "selenium", "playwright"):
                assert bad not in ln
        assert "import subprocess" not in self.SRC
        assert "shell=True" not in self.SRC

    def test_no_provider_or_ollama(self):
        for ln in self._imports():
            low = ln.lower()
            for bad in ("ollama", "anthropic", "openai", "litellm"):
                assert bad not in low

    def test_no_apply_or_execution_imports(self):
        for ln in self._imports():
            assert "patch_apply" not in ln
            assert "source_apply" not in ln
            assert "test_execution_service" not in ln
            assert "do_continue" not in ln

    def test_no_git_pr_jobtasks(self):
        assert "os.system" not in self.SRC
        assert ".tasks.append" not in self.SRC
        for ln in self._imports():
            assert "import git" not in ln and "from git" not in ln
        assert "gh pr" not in self.SRC.lower()

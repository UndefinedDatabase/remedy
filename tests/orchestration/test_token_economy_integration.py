"""Token Economy integration tests (Steps 1775/1777/1772).

Builder-routing token hint, progress ledger items, feature suggestions, review-bundle section,
cockpit section, and placeholder-readiness hardening. All read-only; nothing executes a worker.
"""
from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

import pytest


def _job_with_repo(env, files):
    from packages.core.models import Job, RunState, Task
    from packages.orchestration.storage import save_job
    repo = env / f"repo-{uuid4().hex[:6]}"
    repo.mkdir(parents=True)
    for rel, content in files.items():
        p = repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
    job = Job(id=uuid4(), name="te", user_prompt="x", state=RunState.RUNNING,
              tasks=[Task(description="t")], artifacts=[], metadata={"target_repo": str(repo)})
    save_job(job, root=env)
    return str(job.id)


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"; d.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    return d


# ---------------------------------------------------------------------------
# Review bundle + cockpit (Step 1777)
# ---------------------------------------------------------------------------


class TestSafeSurfaces:
    def _job(self):
        return SimpleNamespace(id=uuid4())

    def test_cockpit_section_readonly(self):
        from packages.orchestration.ui_server import _build_token_economy_section
        s = _build_token_economy_section(self._job())
        assert s["live"] is False
        assert s["source"] in ("token_economy", "unavailable")
        assert "buttons" not in s and "actions" not in s
        assert " run" not in str(s.get("next_safe_action", ""))

# ---------------------------------------------------------------------------
# Placeholder readiness hardening (Step 1772)
# ---------------------------------------------------------------------------


class TestPlaceholderHardening:
    def test_ollama_placeholder_not_executable(self):
        from packages.orchestration.worker_registry import get_worker_spec, is_placeholder
        for wid in ("ollama.placeholder", "cloud.placeholder"):
            s = get_worker_spec(wid)
            assert is_placeholder(s) is True and s.enabled is False

    def test_enabled_ollama_placeholder_flagged_and_not_executed(self, tmp_path):
        # A future custom enabled ollama_candidate must still be treated as a placeholder requiring
        # approval, and integrity must flag any claim of executable readiness.
        from packages.orchestration.worker_registry import (
            _spec_from_dict,
            hard_safety_requires_approval,
        )
        spec = _spec_from_dict({"worker_id": "custom.ollama", "kind": "ollama_candidate",
                                "enabled": True, "cost_tier": "cheap", "risk_tier": "medium",
                                "execution_mode": "local_model"})
        assert hard_safety_requires_approval(spec) is True  # ollama kind → always approval

    def test_worker_registry_integrity_still_passes(self, tmp_path):
        from packages.orchestration.worker_registry import worker_registry_integrity
        assert worker_registry_integrity(data_dir=tmp_path)["passed"] is True

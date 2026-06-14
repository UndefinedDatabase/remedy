"""Self-Dogfood Planner v0 tests (Steps 1420/1421/1422).

Inspection/plan/propose, idempotency, redaction, and architecture guards. Read-only
inspection + metadata-only ProposedTasks; never edits code/applies/approves/inserts
Job.tasks/creates PRs.
"""
from __future__ import annotations

import dataclasses
import json
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from packages.core.models import Artifact, ArtifactKind, Job, Task
from packages.orchestration.storage import save_job, load_job
from packages.orchestration import self_dogfood as SD


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"; d.mkdir()
    ad = tmp_path / "agent"; ad.mkdir()
    (ad / "live_review.md").write_text("## Verdict\nPASS\n")
    (ad / "plan.md").write_text("# Plan\n## Current Step\n1400 — work\n")
    (ad / "context.md").write_text("# Context\n")
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    monkeypatch.setenv("REMEDY_AGENT_DIR", str(ad))
    return d, ad


def _job(data_dir, *, failure=True):
    t = Task(description="t")
    arts = []
    if failure:
        fa = Artifact(name="tf", content="x", kind=ArtifactKind.VERIFICATION, task_id=t.id,
                      metadata={"test_failure": True, "failure_kind": "test_failed",
                                "related_task_id": str(t.id), "safe_summary": "boom"})
        arts.append(fa)
    job = Job(id=uuid4(), name="ov", tasks=[t], artifacts=arts, metadata={"target_repo": "."})
    save_job(job, root=data_dir)
    return job


# ---------------------------------------------------------------------------
# Inspection + detectors
# ---------------------------------------------------------------------------


class TestInspection:
    def test_jobless_inspect(self, env):
        d, _ = env
        insp = SD.build_self_dogfood_inspection(data_dir=d)
        assert insp.repository_identity
        assert any(s.name == ".agent/live_review.md" for s in insp.sources_checked)

    def test_pending_review_is_blocker(self, env):
        d, ad = env
        (ad / "live_review.md").write_text("## Verdict\nPENDING\n")
        insp = SD.build_self_dogfood_inspection(data_dir=d)
        assert "review_verdict_not_pass" in insp.blockers
        assert any(i.item_type == SD.ItemType.SAFETY_GAP and i.priority == SD.Priority.BLOCKER
                   for i in insp.items)

    def test_open_blocker_finding(self, env):
        d, ad = env
        (ad / "live_review.md").write_text(
            "## Verdict\nPASS\n\n### R-1: x\n- **Status**: Open\n- **Severity**: High\n")
        insp = SD.build_self_dogfood_inspection(data_dir=d)
        assert "open_blocker_or_high_findings" in insp.blockers

    def test_evidence_gap_failure_without_repair(self, env):
        d, _ = env
        job = _job(d, failure=True)
        insp = SD.build_self_dogfood_inspection(str(job.id), d)
        assert any("Unresolved failure has no repair attempt" == i.title for i in insp.items)

    def test_roadmap_items_cite_evidence(self, env):
        d, _ = env
        insp = SD.build_self_dogfood_inspection(data_dir=d)
        roadmap = [i for i in insp.items if i.item_type == SD.ItemType.ROADMAP_NEXT]
        assert roadmap
        assert all(i.evidence for i in roadmap)  # each cites a module

    def test_stale_plan_detected(self, env):
        d, ad = env
        (ad / "plan.md").write_text("# Plan\n## Current Step\nDONE merge-ready\n- [ ] 1: open\n")
        insp = SD.build_self_dogfood_inspection(data_dir=d)
        assert any(i.fingerprint == SD._fingerprint(SD.ItemType.CLEANUP, "plan_done_open_steps")
                   for i in insp.items)


# ---------------------------------------------------------------------------
# Plan + propose + idempotency (Steps 1408/1411/1420)
# ---------------------------------------------------------------------------


class TestPlanAndPropose:
    def test_plan_groups_and_top3(self, env):
        d, _ = env
        job = _job(d)
        plan = SD.build_self_improvement_plan(str(job.id), d)
        assert plan.item_count >= 1
        assert len(plan.recommended) <= 3

    def test_propose_ambiguous_requires_selection(self, env):
        d, ad = env
        (ad / "live_review.md").write_text("## Verdict\nPENDING\n\n### R-1: x\n- **Status**: Open\n- **Severity**: High\n")
        job = _job(d)
        r = SD.propose_self_improvement(str(job.id), data_dir=d)
        assert r.stop_reason == "ambiguous_selection"
        assert not r.proposed_task_ids

    def test_propose_top_creates_tasks(self, env):
        d, _ = env
        job = _job(d)
        r = SD.propose_self_improvement(str(job.id), top=2, data_dir=d)
        assert r.stop_reason == "ok"
        assert len(r.proposed_task_ids) == 2

    def test_propose_idempotent(self, env):
        d, _ = env
        job = _job(d)
        SD.propose_self_improvement(str(job.id), top=2, data_dir=d)
        r2 = SD.propose_self_improvement(str(job.id), top=2, data_dir=d)
        assert not r2.proposed_task_ids and len(r2.skipped_existing) == 2
        from packages.orchestration.proposed_tasks import load_proposed_tasks
        assert len(load_proposed_tasks(str(job.id), d)) == 2

    def test_proposed_task_origin_and_type(self, env):
        d, _ = env
        job = _job(d)
        SD.propose_self_improvement(str(job.id), top=1, data_dir=d)
        from packages.orchestration.proposed_tasks import load_proposed_tasks
        t = load_proposed_tasks(str(job.id), d)[0]
        assert t.task_type == "self_dogfood"
        assert t.origin_recommendation_id.startswith("self_dogfood:")
        assert t.materialized_task_id == ""  # not materialized into Job.tasks

    def test_propose_missing_job(self, env):
        d, _ = env
        r = SD.propose_self_improvement(str(uuid4()), top=1, data_dir=d)
        assert r.stop_reason == "job_not_found"

    def test_propose_contract_blocked(self, env):
        d, _ = env
        from packages.orchestration.run_contract import (
            build_default_run_contract, save_contract, ContractAction,
        )
        job = _job(d)
        c = build_default_run_contract(job)
        c = dataclasses.replace(c, allowed_actions=tuple(
            a for a in c.allowed_actions if a != ContractAction.SELF_PROPOSE_TASK))
        save_contract(job, c); save_job(job, root=d)
        r = SD.propose_self_improvement(str(job.id), top=1, data_dir=d)
        assert r.stop_reason == "contract_blocked"
        assert not r.proposed_task_ids


# ---------------------------------------------------------------------------
# Redaction (Step 1421)
# ---------------------------------------------------------------------------


class TestRedaction:
    def test_no_raw_leak(self, env):
        d, ad = env
        (ad / "live_review.md").write_text(
            "## Verdict\nPASS\nleak token sk-abcdef0123456789abcd at /home/u/.ssh/id_rsa\n"
            "Traceback (most recent call last)\n")
        job = _job(d)
        SD.propose_self_improvement(str(job.id), top=2, data_dir=d)
        reloaded = load_job(UUID(str(job.id)), d)
        from packages.orchestration.review_bundle import _build_self_dogfood_summary
        from packages.orchestration.ui_server import _build_self_dogfood_section
        from packages.orchestration.proposed_tasks import load_proposed_tasks
        blobs = [
            json.dumps(SD.export_inspection_json(SD.build_self_dogfood_inspection(str(job.id), d))),
            json.dumps(SD.export_plan_json(SD.build_self_improvement_plan(str(job.id), d))),
            SD.render_report_markdown(SD.build_self_dogfood_report(str(job.id), d)),
            json.dumps(_build_self_dogfood_summary(reloaded)),
            json.dumps(_build_self_dogfood_section(reloaded)),
            json.dumps([t.model_dump(mode="json") for t in load_proposed_tasks(str(job.id), d)], default=str),
        ]
        for b in blobs:
            assert "sk-abcdef0123456789abcd" not in b
            assert "/home/" not in b
            assert "id_rsa" not in b
            assert "Traceback" not in b


# ---------------------------------------------------------------------------
# Architecture guards (Step 1422)
# ---------------------------------------------------------------------------


class TestArchitectureGuards:
    SRC = Path("packages/orchestration/self_dogfood.py").read_text()

    def _imports(self):
        return [ln for ln in self.SRC.splitlines()
                if ln.strip().startswith(("import ", "from "))]

    def test_no_network_or_subprocess(self):
        for ln in self._imports():
            for bad in ("subprocess", "socket", "requests", "httpx", "urllib", "selenium", "playwright"):
                assert bad not in ln
        assert "import subprocess" not in self.SRC
        assert "shell=True" not in self.SRC

    def test_no_provider_sdk(self):
        for ln in self._imports():
            low = ln.lower()
            for bad in ("ollama", "anthropic", "openai", "litellm"):
                assert bad not in low

    def test_no_apply_test_materialize_imports(self):
        for ln in self._imports():
            assert "patch_apply" not in ln
            assert "test_execution_service" not in ln
            assert "provider_patch_material" not in ln
            assert "do_continue" not in ln

    def test_no_job_tasks_insertion_or_git(self):
        # No direct Job.tasks mutation, no git/PR/command execution (the words
        # "git"/"commit" may appear only in roadmap label strings).
        assert ".tasks.append" not in self.SRC
        assert "os.system" not in self.SRC
        for ln in self._imports():
            assert "import git" not in ln and "from git" not in ln
        assert "gh pr" not in self.SRC.lower()

    def test_next_action_catalog_backed(self, env):
        from packages.orchestration.do_run import validate_next_safe_action_command
        d, _ = env
        job = _job(d)
        insp = SD.build_self_dogfood_inspection(str(job.id), d)
        assert insp.next_safe_action is not None
        assert validate_next_safe_action_command(insp.next_safe_action.command)

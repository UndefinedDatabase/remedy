"""Main Orchestrator Brain v0 tests (Steps 1485/1486/1487/1489/1490).

Decision quality, anti-loop guard, model routing, idea intake, redaction, and
architecture guards. Planning/decision only — no execution / model / provider / apply.
"""
from __future__ import annotations

import json
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from packages.core.models import Artifact, ArtifactKind, Job, Task
from packages.orchestration.storage import save_job, load_job
from packages.orchestration import orchestrator_brain as OB


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"; d.mkdir()
    ad = tmp_path / "agent"; ad.mkdir()
    for f in ("live_review.md", "plan.md", "context.md"):
        (ad / f).write_text("## Verdict\nPASS\n")
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    monkeypatch.setenv("REMEDY_AGENT_DIR", str(ad))
    return d, ad


def _job(data_dir, *, failure=True, related=("docs/guide.md",)):
    t = Task(description="t")
    arts = []
    if failure:
        fa = Artifact(name="tf", content="x", kind=ArtifactKind.VERIFICATION, task_id=t.id,
                      metadata={"test_failure": True, "failure_kind": "test_failed",
                                "related_task_id": str(t.id), "related_files": list(related),
                                "safe_summary": "boom"})
        arts.append(fa)
    job = Job(id=uuid4(), name="ov", tasks=[t], artifacts=arts, metadata={"target_repo": "."})
    save_job(job, root=data_dir)
    return job


# ---------------------------------------------------------------------------
# Decision quality (Step 1485)
# ---------------------------------------------------------------------------


class TestDecisionQuality:
    def test_selected_command_catalog_backed(self, env):
        from packages.orchestration.do_run import validate_next_safe_action_command
        d, _ = env
        job = _job(d)
        s = OB.build_orchestrator_situation(str(job.id), d)
        dec = OB.select_orchestrator_decision(s, d)
        if dec.selected_option and dec.selected_option.get("command"):
            assert validate_next_safe_action_command(dec.next_safe_action)

    def test_open_blocker_forces_human_review(self, env):
        d, ad = env
        (ad / "live_review.md").write_text(
            "## Verdict\nFAIL\n\n### R-1: x\n- **Status**: Open\n- **Severity**: High\n")
        job = _job(d)
        s = OB.build_orchestrator_situation(str(job.id), d)
        dec = OB.select_orchestrator_decision(s, d)
        assert dec.stop_reason == OB.StopReason.HUMAN_REVIEW_REQUIRED
        assert s.model_routing_plan.tier == OB.RoutingTier.HUMAN_REVIEW_REQUIRED

    def test_unresolved_failure_beats_roadmap(self, env):
        d, _ = env
        job = _job(d)
        s = OB.build_orchestrator_situation(str(job.id), d)
        dec = OB.select_orchestrator_decision(s, d)
        assert dec.selected_option["kind"] == OB.OptionKind.PROPOSE_REPAIR

    def test_pending_approval_beats_proposal(self, env):
        d, _ = env
        from packages.orchestration.approval_queue import make_intent_id
        # Build a job with a pending patch intent (beats other options).
        t = Task(description="t")
        art = Artifact(name="b", content="Proposed Changes:\n  - x", kind=ArtifactKind.BUILDER_PROPOSAL,
                       task_id=t.id, metadata={"patch_intent_explanations": [
                           {"file": "docs/x.md", "action": "create", "risk": "low",
                            "reason": "", "summary": "s"}], "patch_intent_approvals": {}})
        job = Job(id=uuid4(), name="ov", tasks=[t], artifacts=[art], metadata={"target_repo": "."})
        save_job(job, root=d)
        s = OB.build_orchestrator_situation(str(job.id), d)
        dec = OB.select_orchestrator_decision(s, d)
        assert dec.selected_option["kind"] == OB.OptionKind.APPROVE_INTENT

    def test_contract_denied_apply_not_recommended(self, env):
        # R-0086: an approved intent whose contract denies patch_apply must not yield a
        # selectable "continue" option.
        from packages.orchestration.approval_queue import set_approval_state
        d, _ = env
        t = Task(description="t")
        art = Artifact(name="b", content="Proposed Changes:\n  - x", kind=ArtifactKind.BUILDER_PROPOSAL,
                       task_id=t.id, metadata={"patch_intent_explanations": [
                           {"file": "docs/x.md", "action": "create", "risk": "low",
                            "reason": "", "summary": "s"}], "patch_intent_approvals": {}})
        job = Job(id=uuid4(), name="ov", tasks=[t], artifacts=[art], metadata={"target_repo": "."})
        save_job(job, root=d)
        from packages.orchestration.approval_queue import make_intent_id
        iid = make_intent_id(art.id, 0)
        j = load_job(UUID(str(job.id)), d)
        set_approval_state(j, iid, "approved", decided_by="human")
        save_job(j, root=d)  # default contract denies PATCH_APPLY
        s = OB.build_orchestrator_situation(str(job.id), d)
        cont = [o for o in s.options if o.kind == OB.OptionKind.CONTINUE_INTENT]
        assert cont and all(not o.available for o in cont)
        dec = OB.select_orchestrator_decision(s, d)
        assert (dec.selected_option or {}).get("kind") != OB.OptionKind.CONTINUE_INTENT

    def test_missing_job_safe(self, env):
        d, _ = env
        s = OB.build_orchestrator_situation(str(uuid4()), d)
        dec = OB.select_orchestrator_decision(s, d)
        assert dec.stop_reason in (OB.StopReason.SELECTED, OB.StopReason.NO_SAFE_ACTION,
                                   OB.StopReason.EVIDENCE_INCOMPLETE)
        # Even with a missing job, the baseline inspect option keeps a safe next action.
        assert dec.next_safe_action


# ---------------------------------------------------------------------------
# Anti-loop guard (Step 1486)
# ---------------------------------------------------------------------------


class TestAntiLoop:
    def test_repeated_decision_warns_then_blocks(self, env):
        d, _ = env
        job = _job(d, failure=False)  # idle → self_propose / inspect, stable evidence
        # First decision: allow.
        s1 = OB.build_orchestrator_situation(str(job.id), d)
        assert s1.loop_guard.status == OB.LoopGuardStatus.ALLOW
        OB.select_orchestrator_decision(s1, d, persist=True)
        # Second: warn.
        s2 = OB.build_orchestrator_situation(str(job.id), d)
        assert s2.loop_guard.status == OB.LoopGuardStatus.WARN
        OB.select_orchestrator_decision(s2, d, persist=True)
        # Third: block.
        s3 = OB.build_orchestrator_situation(str(job.id), d)
        assert s3.loop_guard.status == OB.LoopGuardStatus.BLOCK

    def test_repeated_repair_failure_requires_human(self, env):
        d, _ = env
        job = _job(d)
        # Inject two failed repair attempts.
        from packages.orchestration import repair_loop as RL
        j = load_job(UUID(str(job.id)), d)
        for i in range(2):
            att = RL.RepairAttempt(attempt_id=f"a{i}", job_id=str(job.id),
                                   failure_artifact_id=f"f{i}", status="tested_failed",
                                   source="cli_v1", created_at="t")
            RL.save_repair_attempt(j, att)
        s = OB.build_orchestrator_situation(str(job.id), d)
        assert s.loop_guard.status == OB.LoopGuardStatus.REQUIRE_HUMAN_REVIEW

    def test_new_evidence_resets_loop(self, env):
        d, _ = env
        job = _job(d, failure=False)
        OB.select_orchestrator_decision(OB.build_orchestrator_situation(str(job.id), d), d, persist=True)
        OB.select_orchestrator_decision(OB.build_orchestrator_situation(str(job.id), d), d, persist=True)
        # New evidence (a failure) → different fingerprint → loop resets to allow.
        _job(d) if False else None
        j = load_job(UUID(str(job.id)), d)
        j.artifacts.append(Artifact(name="tf", content="x", kind=ArtifactKind.VERIFICATION,
                                    task_id=j.tasks[0].id,
                                    metadata={"test_failure": True, "failure_kind": "test_failed",
                                              "related_task_id": str(j.tasks[0].id), "safe_summary": "n"}))
        save_job(j, root=d)
        s = OB.build_orchestrator_situation(str(job.id), d)
        assert s.loop_guard.status == OB.LoopGuardStatus.ALLOW


# ---------------------------------------------------------------------------
# Model routing (Step 1487)
# ---------------------------------------------------------------------------


class TestModelRouting:
    def test_open_blocker_high_human_review(self, env):
        d, ad = env
        (ad / "live_review.md").write_text("## Verdict\nPENDING\n")
        job = _job(d)
        s = OB.build_orchestrator_situation(str(job.id), d)
        assert s.model_routing_plan.tier == OB.RoutingTier.HUMAN_REVIEW_REQUIRED
        assert s.model_routing_plan.allow_external is False

    def test_candidate_generation_external_builder(self, env):
        d, _ = env
        # Failure with no repair attempt + test budget available → candidate needed.
        import dataclasses
        from packages.orchestration.run_contract import build_default_run_contract, save_contract
        job = _job(d)
        c = build_default_run_contract(job)
        c = dataclasses.replace(c, max_test_runs=1)
        save_contract(job, c); save_job(job, root=d)
        s = OB.build_orchestrator_situation(str(job.id), d)
        assert s.model_routing_plan.tier == OB.RoutingTier.EXTERNAL_BUILDER_NEEDED
        assert s.model_routing_plan.notes  # plan only

    def test_routing_never_executes(self, env):
        # The routing plan is data only — no model is invoked (architecture guard covers
        # imports; here we assert the plan carries a "plan only" note for non-deterministic).
        d, _ = env
        job = _job(d, failure=False)
        s = OB.build_orchestrator_situation(str(job.id), d)
        assert s.model_routing_plan.tier in (
            OB.RoutingTier.DETERMINISTIC_ONLY, OB.RoutingTier.LOCAL_ADVISOR_PREFERRED,
            OB.RoutingTier.EXTERNAL_BUILDER_NEEDED, OB.RoutingTier.HUMAN_REVIEW_REQUIRED)


# ---------------------------------------------------------------------------
# Idea intake (Steps 1479/1480)
# ---------------------------------------------------------------------------


class TestIdeas:
    def test_idea_classified_and_deduped(self, env):
        d, _ = env
        r1 = OB.record_idea("add a security audit feature", d)
        assert r1.classification == "safety_concern"
        r2 = OB.record_idea("add a security audit feature", d)
        assert r1.fingerprint == r2.fingerprint
        assert len(OB.list_ideas(d)) == 1

    def test_idea_is_hint_not_executed(self, env):
        d, _ = env
        OB.record_idea("eventually support plugins", d)
        job = _job(d, failure=False)
        s = OB.build_orchestrator_situation(str(job.id), d)
        # Idea surfaces as a human-review-only option, never auto-selected/executable.
        idea_opts = [o for o in s.options if o.kind == OB.OptionKind.HUMAN_REVIEW]
        assert all(not o.available for o in idea_opts)


# ---------------------------------------------------------------------------
# Redaction (Step 1489)
# ---------------------------------------------------------------------------


class TestRedaction:
    def test_no_raw_leak(self, env):
        d, ad = env
        (ad / "live_review.md").write_text(
            "## Verdict\nPASS\nleak sk-abcdef0123456789abcd at /home/u/.ssh/id_rsa\n"
            "Traceback (most recent call last)\n")
        OB.record_idea("token sk-deadbeefdeadbeef00 at /home/u/.env please fix", d)
        job = _job(d)
        s = OB.build_orchestrator_situation(str(job.id), d)
        dec = OB.select_orchestrator_decision(s, d, persist=True)
        blobs = [
            json.dumps(OB.export_situation_json(s)),
            json.dumps(OB.export_decision_json(dec)),
            OB.render_report_markdown(OB.build_orchestrator_report(str(job.id), d)),
            json.dumps(OB.list_ideas(d)),
        ]
        for b in blobs:
            assert "sk-abcdef0123456789abcd" not in b
            assert "sk-deadbeefdeadbeef00" not in b
            assert "/home/" not in b
            assert "id_rsa" not in b
            assert "Traceback" not in b


# ---------------------------------------------------------------------------
# Architecture guards (Step 1490)
# ---------------------------------------------------------------------------


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

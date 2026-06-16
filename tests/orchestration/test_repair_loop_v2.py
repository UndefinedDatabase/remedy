"""Token-Aware Repair Loop v1/v2 tests (Steps 1919-1938).

Unit coverage: models/serialization, storage (atomic/corruption/idempotent), failure→item,
review→item (Done≠Resolved), token-aware context pack (minimal/oversized/unknown), route recommendation
(local/external/expensive), gates (review/retest), state machine, integrity, mission signal, redaction,
and architecture guards. No model/provider/worker execution; no apply.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from uuid import uuid4

import pytest

from packages.orchestration import repair_loop_v2 as v2


def _job(env: Path, *, with_failure: bool = False, repo: bool = True) -> tuple[str, str]:
    from packages.core.models import Job, RunState, Task, Artifact, ArtifactKind
    from packages.orchestration.storage import save_job
    meta: dict = {}
    if repo:
        rp = env / f"repo-{uuid4().hex[:6]}"
        rp.mkdir(parents=True)
        (rp / "a.py").write_text("x = 1\n")
        meta["target_repo"] = str(rp)
    arts = []
    fa_id = ""
    if with_failure:
        art = Artifact(name="fail", content="x", kind=ArtifactKind.BUILDER_PROPOSAL, metadata={
            "test_failure": True, "failure_kind": "test_failed", "safe_summary": "2 tests failed",
            "related_test_run_id": "tr1", "related_files": ["/home/u/pkg/mod.py", "b.py"],
            "exit_code": 1})
        arts.append(art)
        fa_id = str(art.id)
    job = Job(id=uuid4(), name="m", user_prompt="x", state=RunState.RUNNING,
              tasks=[Task(description="t")], artifacts=arts, metadata=meta)
    save_job(job, root=env)
    return str(job.id), fa_id


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"; d.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    return d


def _review_file(env: Path, monkeypatch, body: str) -> Path:
    rf = env.parent / "lr.md"
    rf.write_text(body)
    monkeypatch.setenv("REMEDY_REVIEW_FILE", str(rf))
    return rf


# ---------------------------------------------------------------------------
# Models + storage
# ---------------------------------------------------------------------------


class TestModels:
    def test_policy_roundtrip(self):
        p = v2.default_repair_loop_policy("j")
        d = p.to_dict()
        assert d["schema_version"] == v2.SCHEMA_VERSION and d["max_attempts"] == 3
        assert v2.RepairLoopPolicy.from_dict(d).max_attempts == 3

    def test_work_item_scrubs(self):
        i = v2.RepairWorkItem(repair_id="r", job_id="j", safe_summary="oops /home/u/.env sk-ant-x",
                              suspected_files=["mod.py"])
        d = i.to_dict()
        assert "/home/u" not in d["safe_summary"]

    def test_attempt_roundtrip(self):
        a = v2.RepairAttempt(attempt_id="a1", repair_id="r", attempt_index=2, route_id="local")
        assert v2.RepairAttempt.from_dict(a.to_dict()).attempt_index == 2


class TestStorage:
    def test_policy_save_load_default(self, env):
        assert v2.load_repair_loop_policy("nojob", env).max_attempts == 3  # default, no raise
        p = v2.default_repair_loop_policy("j"); p.max_attempts = 7
        assert v2.save_repair_loop_policy(p, env)
        assert v2.load_repair_loop_policy("j", env).max_attempts == 7

    def test_work_item_save_list_load(self, env):
        it = v2.RepairWorkItem(repair_id="r1", job_id="j", source_type=v2.SOURCE_FAILURE,
                               created_at=v2._now())
        assert v2.save_repair_work_item(it, env)
        assert len(v2.list_repair_work_items(job_id="j", data_dir=env)) == 1
        assert v2.load_repair_work_item("r1", env) is not None

    def test_corrupt_policy_falls_back(self, env):
        path = v2._rl_root("j", env) / "policy.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{not json")
        assert v2.load_repair_loop_policy("j", env).max_attempts == 3  # safe default

    def test_attempts_save_list(self, env):
        a = v2.RepairAttempt(repair_id="r1", attempt_index=0)
        assert v2.save_repair_attempt(a, "j", env)
        assert len(v2.list_repair_attempts("r1", "j", env)) == 1

    def test_evaluation_save_load(self, env):
        ev = v2.RepairLoopEvaluation(repair_id="r1", job_id="j", status=v2.RepairLoopStatus.NEW,
                                     created_at=v2._now())
        assert v2.save_repair_evaluation(ev, env)
        assert v2.load_latest_repair_evaluation("r1", env)["repair_id"] == "r1"


# ---------------------------------------------------------------------------
# Failure artifact → work item
# ---------------------------------------------------------------------------


class TestFromFailure:
    def test_creates_item_no_raw_leak(self, env):
        jid, fa = _job(env, with_failure=True)
        item = v2.create_repair_item_from_failure_artifact(jid, fa, data_dir=env)
        assert item is not None and item.source_type == v2.SOURCE_FAILURE
        assert "mod.py" in item.suspected_files and "/home/u" not in json.dumps(item.to_dict())

    def test_idempotent(self, env):
        jid, fa = _job(env, with_failure=True)
        a = v2.create_repair_item_from_failure_artifact(jid, fa, data_dir=env)
        b = v2.create_repair_item_from_failure_artifact(jid, fa, data_dir=env)
        assert a.repair_id == b.repair_id
        assert len(v2.list_repair_work_items(job_id=jid, data_dir=env)) == 1

    def test_missing_artifact_safe_none(self, env):
        jid, _ = _job(env, with_failure=False)
        assert v2.create_repair_item_from_failure_artifact(jid, "nope", data_dir=env) is None


# ---------------------------------------------------------------------------
# Review finding → work item (Done ≠ Resolved)
# ---------------------------------------------------------------------------


_OPEN_HIGH = ("## Verdict\nFAIL\n\n### R-0105\n- **Severity**: High\n- **Status**: Open\n")
_RESOLVED = ("## Verdict\nPASS\n\n### R-0105\n- **Severity**: High\n- **Status**: Resolved\n")
_DONE_NOT_RESOLVED = ("## Verdict\nPENDING\n\n### R-0105\n- **Severity**: High\n- **Status**: Open\n"
                      "Done: R-0105 - builder fixed it\n")
_LOW = ("## Verdict\nPASS WITH RISKS\n\n### R-0105\n- **Severity**: Low\n- **Status**: Open\n")


class TestFromReview:
    def test_open_high_creates_item(self, env, monkeypatch):
        _review_file(env, monkeypatch, _OPEN_HIGH)
        jid, _ = _job(env)
        item = v2.create_repair_item_from_review_finding(jid, "R-0105", data_dir=env)
        assert item is not None and item.review_finding_id == "R-0105"

    def test_resolved_creates_nothing(self, env, monkeypatch):
        _review_file(env, monkeypatch, _RESOLVED)
        jid, _ = _job(env)
        assert v2.create_repair_item_from_review_finding(jid, "R-0105", data_dir=env) is None

    def test_done_marker_still_creates_item(self, env, monkeypatch):
        # Done ≠ Resolved: status is still Open, so a required item is created.
        _review_file(env, monkeypatch, _DONE_NOT_RESOLVED)
        jid, _ = _job(env)
        assert v2.create_repair_item_from_review_finding(jid, "R-0105", data_dir=env) is not None

    def test_low_severity_creates_nothing(self, env, monkeypatch):
        _review_file(env, monkeypatch, _LOW)
        jid, _ = _job(env)
        assert v2.create_repair_item_from_review_finding(jid, "R-0105", data_dir=env) is None


# ---------------------------------------------------------------------------
# Context pack — token aware
# ---------------------------------------------------------------------------


class TestContextPack:
    def test_minimal_no_raw(self, env):
        jid, fa = _job(env, with_failure=True)
        item = v2.create_repair_item_from_failure_artifact(jid, fa, data_dir=env)
        pack = v2.build_repair_context_pack(item.repair_id, data_dir=env)
        blob = json.dumps(pack).lower()
        for bad in ("/home/", "traceback", "sk-ant", "diff --git"):
            assert bad not in blob
        assert pack["status"] in ("ready", "needs_decision", "needs_compression")

    def test_unknown_context_needs_decision(self, env, monkeypatch):
        jid, fa = _job(env, with_failure=True)
        item = v2.create_repair_item_from_failure_artifact(jid, fa, data_dir=env)
        monkeypatch.setattr(v2, "routing_token_hint", None, raising=False)
        import packages.orchestration.token_economy as te
        monkeypatch.setattr(te, "routing_token_hint", lambda *a, **k: {
            "estimated_token_band": "unknown", "budget_status": "unknown",
            "requires_human_approval": True, "local_first_recommended": False})
        pack = v2.build_repair_context_pack(item.repair_id, data_dir=env)
        assert pack["status"] == "needs_decision" and pack["blocker"] == "unknown_context"

    def test_missing_item_blocked(self, env):
        assert v2.build_repair_context_pack("nope", data_dir=env)["status"] == "blocked"


# ---------------------------------------------------------------------------
# Route recommendation
# ---------------------------------------------------------------------------


class TestRoute:
    def test_unknown_requires_human(self, env, monkeypatch):
        jid, fa = _job(env, with_failure=True)
        item = v2.create_repair_item_from_failure_artifact(jid, fa, data_dir=env)
        import packages.orchestration.token_economy as te
        monkeypatch.setattr(te, "routing_token_hint", lambda *a, **k: {
            "estimated_token_band": "unknown", "budget_status": "unknown",
            "requires_human_approval": True, "local_first_recommended": False})
        rec = v2.recommend_repair_route(item.repair_id, data_dir=env)
        assert rec["recommended_route_kind"] == "human_review" and rec["requires_human_approval"]

    def test_expensive_requires_human(self, env, monkeypatch):
        jid, fa = _job(env, with_failure=True)
        item = v2.create_repair_item_from_failure_artifact(jid, fa, data_dir=env)
        import packages.orchestration.token_economy as te
        monkeypatch.setattr(te, "routing_token_hint", lambda *a, **k: {
            "estimated_token_band": "high", "budget_status": "ok",
            "requires_human_approval": True, "local_first_recommended": False})
        rec = v2.recommend_repair_route(item.repair_id, data_dir=env)
        assert rec["requires_human_approval"] is True

    def test_cheap_no_local_falls_to_external_package(self, env, monkeypatch):
        jid, fa = _job(env, with_failure=True)
        item = v2.create_repair_item_from_failure_artifact(jid, fa, data_dir=env)
        import packages.orchestration.token_economy as te
        monkeypatch.setattr(te, "routing_token_hint", lambda *a, **k: {
            "estimated_token_band": "low", "budget_status": "ok",
            "requires_human_approval": False, "local_first_recommended": False})
        rec = v2.recommend_repair_route(item.repair_id, data_dir=env)
        assert rec["recommended_route_kind"] == "external_builder_package"
        assert "external-builder package-create" in rec["next_safe_action"]

    def test_persist_attempt(self, env, monkeypatch):
        jid, fa = _job(env, with_failure=True)
        item = v2.create_repair_item_from_failure_artifact(jid, fa, data_dir=env)
        import packages.orchestration.token_economy as te
        monkeypatch.setattr(te, "routing_token_hint", lambda *a, **k: {
            "estimated_token_band": "low", "budget_status": "ok",
            "requires_human_approval": False, "local_first_recommended": False})
        v2.recommend_repair_route(item.repair_id, persist_attempt=True, data_dir=env)
        assert len(v2.list_repair_attempts(item.repair_id, jid, env)) == 1


# ---------------------------------------------------------------------------
# State machine + gates
# ---------------------------------------------------------------------------


class TestStateMachine:
    def test_new_item_context_needed(self, env):
        jid, fa = _job(env, with_failure=True)
        item = v2.create_repair_item_from_failure_artifact(jid, fa, data_dir=env)
        ev = v2.evaluate_repair_loop(item.repair_id, data_dir=env)
        assert ev.status == v2.RepairLoopStatus.CONTEXT_NEEDED
        assert ev.required_next_actions and not ev.satisfied

    def test_missing_item_blocked(self, env):
        ev = v2.evaluate_repair_loop("nope", data_dir=env)
        assert ev.status == v2.RepairLoopStatus.BLOCKED

    def test_max_attempts_blocks(self, env):
        jid, fa = _job(env, with_failure=True)
        item = v2.create_repair_item_from_failure_artifact(jid, fa, data_dir=env)
        pol = v2.load_repair_loop_policy(jid, env); pol.max_attempts = 1
        v2.save_repair_loop_policy(pol, env)
        for i in range(3):
            v2.save_repair_attempt(v2.RepairAttempt(repair_id=item.repair_id, attempt_index=i), jid, env)
        ev = v2.evaluate_repair_loop(item.repair_id, data_dir=env)
        assert ev.status == v2.RepairLoopStatus.BLOCKED
        assert any("max_attempts" in r for r in ev.blocked_reasons)

    def test_abandoned_requires_user(self, env):
        jid, fa = _job(env, with_failure=True)
        item = v2.create_repair_item_from_failure_artifact(jid, fa, data_dir=env)
        item.status = v2.RepairLoopStatus.ABANDONED
        v2.save_repair_work_item(item, env)
        ev = v2.evaluate_repair_loop(item.repair_id, data_dir=env)
        assert ev.status == v2.RepairLoopStatus.ABANDONED

    def test_every_state_has_next_action(self, env):
        jid, fa = _job(env, with_failure=True)
        item = v2.create_repair_item_from_failure_artifact(jid, fa, data_dir=env)
        ev = v2.evaluate_repair_loop(item.repair_id, data_dir=env)
        assert all(a.startswith("remedy ") for a in ev.required_next_actions)


# ---------------------------------------------------------------------------
# Integrity + mission signal
# ---------------------------------------------------------------------------


class TestIntegrity:
    def test_clean_passes(self, env):
        jid, fa = _job(env, with_failure=True)
        v2.create_repair_item_from_failure_artifact(jid, fa, data_dir=env)
        assert v2.repair_loop_integrity(data_dir=env)["passed"] is True

    def test_audit_repaired_with_open_review(self):
        ev = {"repair_id": "r", "status": "repaired", "satisfied": True}
        codes = {c["code"] for c in v2.audit_evaluation_safety(
            ev, None, review_open=True, retest_failing=False, apply_present=True,
            policy={"require_reviewer_pass": True})}
        assert "repaired_with_open_review_finding" in codes

    def test_audit_repaired_with_failing_retest(self):
        ev = {"repair_id": "r", "status": "repaired", "satisfied": True}
        codes = {c["code"] for c in v2.audit_evaluation_safety(
            ev, None, review_open=False, retest_failing=True, apply_present=True,
            policy={"require_tests_green": True})}
        assert "repaired_with_failing_retest" in codes

    def test_audit_work_item_raw_leak(self):
        bad = {"repair_id": "r", "status": "new", "safe_summary": "x", "extra": "sk-ant-secret"}
        codes = {c["code"] for c in v2.audit_work_item_safety(bad)}
        assert "raw_or_secret_in_public" in codes

    def test_audit_unknown_status(self):
        codes = {c["code"] for c in v2.audit_work_item_safety({"repair_id": "r", "status": "weird"})}
        assert "unknown_status" in codes

    def test_mission_signal_counts_open(self, env):
        jid, fa = _job(env, with_failure=True)
        v2.create_repair_item_from_failure_artifact(jid, fa, data_dir=env)
        sig = v2.repair_loop_mission_signal(jid, env)
        assert sig["open_repair_count"] == 1 and sig["repair_needed"] is True

    # -- R-0105: attempts_exceeded_without_blocked --

    def test_audit_attempts_exceeded_without_blocked_fires(self):
        """Positive: attempts > max but status not BLOCKED → violation."""
        ev = {"repair_id": "r", "status": "waiting_for_candidate", "attempts_count": 5,
              "satisfied": False, "required_next_actions": [], "optional_next_ideas": []}
        codes = {c["code"] for c in v2.audit_evaluation_safety(
            ev, None, review_open=False, retest_failing=False, apply_present=True,
            policy={"max_attempts": 3})}
        assert "attempts_exceeded_without_blocked" in codes

    def test_audit_attempts_exceeded_blocked_no_fire(self):
        """Negative: attempts > max but status IS BLOCKED → no violation."""
        ev = {"repair_id": "r", "status": "blocked", "attempts_count": 5,
              "satisfied": False, "required_next_actions": [], "optional_next_ideas": []}
        codes = {c["code"] for c in v2.audit_evaluation_safety(
            ev, None, review_open=False, retest_failing=False, apply_present=True,
            policy={"max_attempts": 3})}
        assert "attempts_exceeded_without_blocked" not in codes

    def test_audit_attempts_within_bounds_no_fire(self):
        """Negative: attempts within bounds → no violation regardless of status."""
        ev = {"repair_id": "r", "status": "waiting_for_candidate", "attempts_count": 2,
              "satisfied": False, "required_next_actions": [], "optional_next_ideas": []}
        codes = {c["code"] for c in v2.audit_evaluation_safety(
            ev, None, review_open=False, retest_failing=False, apply_present=True,
            policy={"max_attempts": 3})}
        assert "attempts_exceeded_without_blocked" not in codes

    # -- R-0105: retests_exceeded_without_blocked --

    def test_audit_retests_exceeded_without_blocked_fires(self):
        """Positive: failing retests > max but status not BLOCKED → violation."""
        ev = {"repair_id": "r", "status": "retest_failed", "attempts_count": 1,
              "satisfied": False, "required_next_actions": [], "optional_next_ideas": []}
        codes = {c["code"] for c in v2.audit_evaluation_safety(
            ev, None, review_open=False, retest_failing=False, apply_present=True,
            policy={"max_retests": 2}, failing_retest_count=4)}
        assert "retests_exceeded_without_blocked" in codes

    def test_audit_retests_exceeded_blocked_no_fire(self):
        """Negative: failing retests > max but status IS BLOCKED → no violation."""
        ev = {"repair_id": "r", "status": "blocked", "attempts_count": 1,
              "satisfied": False, "required_next_actions": [], "optional_next_ideas": []}
        codes = {c["code"] for c in v2.audit_evaluation_safety(
            ev, None, review_open=False, retest_failing=False, apply_present=True,
            policy={"max_retests": 2}, failing_retest_count=4)}
        assert "retests_exceeded_without_blocked" not in codes

    def test_audit_retests_within_bounds_no_fire(self):
        """Negative: failing retests within bounds → no violation."""
        ev = {"repair_id": "r", "status": "retest_failed", "attempts_count": 1,
              "satisfied": False, "required_next_actions": [], "optional_next_ideas": []}
        codes = {c["code"] for c in v2.audit_evaluation_safety(
            ev, None, review_open=False, retest_failing=False, apply_present=True,
            policy={"max_retests": 3}, failing_retest_count=2)}
        assert "retests_exceeded_without_blocked" not in codes

    # -- R-0105: optional_idea_marked_required --

    def test_audit_optional_idea_in_required_fires(self):
        """Positive: same string in both required and optional → violation."""
        idea = "Configure Ollama for cheap small repairs (future, disabled by default)."
        ev = {"repair_id": "r", "status": "waiting_for_candidate", "attempts_count": 0,
              "satisfied": False, "required_next_actions": [idea],
              "optional_next_ideas": [idea]}
        codes = {c["code"] for c in v2.audit_evaluation_safety(
            ev, None, review_open=False, retest_failing=False, apply_present=True,
            policy={})}
        assert "optional_idea_marked_required" in codes

    def test_audit_optional_idea_not_in_required_no_fire(self):
        """Negative: no overlap between required and optional → no violation."""
        ev = {"repair_id": "r", "status": "waiting_for_candidate", "attempts_count": 0,
              "satisfied": False,
              "required_next_actions": ["remedy repair context-pack r --json"],
              "optional_next_ideas": ["Configure Ollama (future)."]}
        codes = {c["code"] for c in v2.audit_evaluation_safety(
            ev, None, review_open=False, retest_failing=False, apply_present=True,
            policy={})}
        assert "optional_idea_marked_required" not in codes


# ---------------------------------------------------------------------------
# Architecture guards
# ---------------------------------------------------------------------------


class TestArchitectureGuards:
    def _src(self) -> str:
        p = Path(__file__).resolve().parents[2] / "packages" / "orchestration" / "repair_loop_v2.py"
        src = p.read_text(encoding="utf-8")
        src = re.sub(r'"""[\s\S]*?"""', "", src)
        src = re.sub(r"'''[\s\S]*?'''", "", src)
        src = re.sub(r'"(?:\\.|[^"\\])*"', '""', src)
        src = re.sub(r"'(?:\\.|[^'\\])*'", "''", src)
        return src

    def test_no_forbidden_imports(self):
        src = self._src()
        for bad in ("import subprocess", "subprocess.", "shell=True", "os.system", "Popen",
                    "import requests", "import socket", "import ollama", "import openai",
                    "import anthropic", "faiss", "chromadb", "import numpy"):
            assert bad not in src, bad

    def test_no_execution_or_apply(self):
        src = self._src()
        for bad in ("do_continue(", "apply_patch(", ".approve(", "eval(", "exec(", "os.fork",
                    "execute_test_run("):
            assert bad not in src, bad

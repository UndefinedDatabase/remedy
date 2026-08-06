"""F079 T001 — the handoff artifact: composition, idempotence, gaps, purity.

What the order requires proof of:

  * the same mission state yields BYTE-IDENTICAL bytes, and a repeat build on
    unchanged state accumulates no duplicate — a boundary reached twice
    without progress leaves one account, not two;
  * changed state accumulates the NEXT version, and the newest is resolvable
    by the accumulation scheme alone;
  * every missing source renders as a NAMED gap — never invented content;
  * a zero-progress mission is a valid handoff (goal plus gaps);
  * building mutates nothing: a snapshot of mission, dossier and job state is
    equal before and after;
  * the manifest redaction denylist reaches every value the handoff quotes;
  * ``schema_version`` is present in the body and in the rendered block.

No provider is contacted and no real data root is touched: every test writes
under ``tmp_path`` with the mission root passed explicitly via ``root=`` and
``REMEDY_DATA_DIR`` pointed at the same place for the job-side sources.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from packages.orchestration.checkpoints import Checkpoint, write_checkpoint
from packages.orchestration.handoff import (
    GAP_CHECKPOINT,
    GAP_DOSSIER,
    GAP_JOBS,
    GAP_NEXT_INTENT,
    HANDOFF_SCHEMA_VERSION,
    HANDOFF_SECTIONS,
    HandoffError,
    MissionForHandoffNotFoundError,
    build_handoff,
    compose_handoff_body,
    find_mission_record,
    handoff_versions,
    latest_handoff_version,
    redact_handoff_value,
    render_handoff,
)
from packages.orchestration.mission_dossier import (
    DossierItem,
    IterationFacts,
    save_dossier_state,
    start_dossier,
    update,
    write_dossier_version,
)
from packages.orchestration.mission_state import (
    create_mission,
    link_job_to_mission,
    load_mission,
)

PROJECT = "proj-handoff"


@pytest.fixture()
def data_root(tmp_path, monkeypatch):
    """A private data root for BOTH sides: mission files and job evidence."""
    from packages.orchestration.config import reset_config

    root = tmp_path / "data"
    root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    reset_config()
    yield root
    reset_config()


def _mission(root, goal: str = "ship the ledger rewrite"):
    return create_mission(PROJECT, goal, root=root)


def _seed_dossier(root, mission, *, next_step: str = "run the migration"):
    """A stored dossier version + live state, through the dossier's own writers."""
    dossier = start_dossier(mission.goal)
    result = update(dossier, IterationFacts(
        milestones=[DossierItem(id="M001", text="the rewrite is released")],
        risks=[DossierItem(id="R001", text="the migration is not reversible")],
        decisions=[DossierItem(id="D001", text="reuse the existing writer",
                               resolved=True, outcome="reused")],
        next_step=next_step))
    write_dossier_version(PROJECT, mission.id, result.dossier, root)
    save_dossier_state(PROJECT, mission.id, result.dossier, root)
    return result.dossier


def _advance_dossier(root, mission, *, next_step: str):
    """One more dossier iteration — a NEW version, the way a real run moves."""
    from packages.orchestration.mission_dossier import load_dossier_state

    dossier = load_dossier_state(PROJECT, mission.id, root)
    result = update(dossier, IterationFacts(next_step=next_step))
    write_dossier_version(PROJECT, mission.id, result.dossier, root)
    save_dossier_state(PROJECT, mission.id, result.dossier, root)
    return result.dossier


def _seed_job_checkpoint(root, mission, job_id: str, *,
                         next_intent: dict | None = None,
                         cycle_index: int = 1):
    """A linked job with one verifying checkpoint, written by the real writer."""
    link_job_to_mission(PROJECT, mission.id, job_id, "initial", root=root)
    checkpoint = Checkpoint(
        cycle_index=cycle_index,
        job_id=job_id,
        job_snapshot_path=f"jobs/{job_id}.json",
        job_snapshot_sha256="sha256:" + "a" * 64,
        worktree_head="c0ffee" + "0" * 34,
        budget_spent_tokens=1234,
        verify_result="passed",
        verify_digest="sha256:" + "b" * 64,
        next_intent=next_intent if next_intent is not None
        else {"task": "apply the migration"},
        created_at="2026-08-06T10:00:00+00:00",
    )
    write_checkpoint(job_id, checkpoint)
    return load_mission(PROJECT, mission.id, root)


def _seed_readable_job(root, mission,
                       job_id: str = "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"):
    """A persisted job linked to the mission, so the decision queue can read it."""
    from uuid import UUID

    from packages.core.models import Job
    from packages.orchestration.storage import save_job

    save_job(Job(id=UUID(job_id), name="the linked job"))
    _seed_job_checkpoint(root, mission, job_id)
    return job_id


def _state_snapshot(root):
    """Every file under the data root except the handoff artifacts themselves."""
    snapshot = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name.startswith("handoff_v"):
            continue
        snapshot[str(path.relative_to(root))] = hashlib.sha256(
            path.read_bytes()).hexdigest()
    return snapshot


class TestComposition:
    def test_the_body_carries_the_schema_version_and_the_mission(self, data_root):
        mission = _mission(data_root)
        _seed_dossier(data_root, mission)
        body = json.loads(build_handoff(mission.id, data_root)
                          .read_text(encoding="utf-8"))
        assert body["schema_version"] == HANDOFF_SCHEMA_VERSION
        assert body["mission_id"] == mission.id
        assert body["project_id"] == PROJECT
        assert body["goal"] == mission.goal

    def test_the_dossier_text_comes_from_the_dossiers_own_renderer(self, data_root):
        from packages.orchestration.mission_dossier import (
            latest_dossier_version,
            newest_dossier_text,
        )

        mission = _mission(data_root)
        _seed_dossier(data_root, mission)
        body = json.loads(build_handoff(mission.id, data_root)
                          .read_text(encoding="utf-8"))
        assert body["dossier"]["text"] == newest_dossier_text(
            PROJECT, mission.id, data_root)
        assert body["dossier"]["version"] == latest_dossier_version(
            PROJECT, mission.id, data_root)
        assert body["dossier"]["version"] > 0

    def test_the_checkpoint_reference_and_worktree_head_are_carried(self, data_root):
        mission = _mission(data_root)
        _seed_dossier(data_root, mission)
        job_id = "11111111-1111-4111-8111-111111111111"
        _seed_job_checkpoint(data_root, mission, job_id)
        body = json.loads(build_handoff(mission.id, data_root)
                          .read_text(encoding="utf-8"))
        assert body["checkpoint"]["job_id"] == job_id
        assert body["checkpoint"]["cycle_index"] == 1
        assert body["checkpoint"]["worktree_head"].startswith("c0ffee")
        assert body["checkpoint"]["content_hash"].startswith("sha256:")
        assert body["provenance"]["checkpoint_created_at"] == \
            "2026-08-06T10:00:00+00:00"

    def test_the_next_intent_prefers_the_checkpoint_over_the_dossier(self, data_root):
        mission = _mission(data_root)
        _seed_dossier(data_root, mission, next_step="narrated step")
        job_id = "22222222-2222-4222-8222-222222222222"
        _seed_job_checkpoint(data_root, mission, job_id,
                             next_intent={"task": "recorded step"})
        body = json.loads(build_handoff(mission.id, data_root)
                          .read_text(encoding="utf-8"))
        assert body["next_intent"]["source"] == "checkpoint"
        assert body["next_intent"]["intent"] == {"task": "recorded step"}

    def test_the_next_intent_falls_back_to_the_narrated_step(self, data_root):
        mission = _mission(data_root)
        _seed_dossier(data_root, mission, next_step="narrated step")
        body = json.loads(build_handoff(mission.id, data_root)
                          .read_text(encoding="utf-8"))
        assert body["next_intent"] == {
            "source": "dossier", "intent": {"next_step": "narrated step"}}

    def test_an_unknown_mission_is_refused_rather_than_invented(self, data_root):
        with pytest.raises(MissionForHandoffNotFoundError) as exc:
            build_handoff("no-such-mission", data_root)
        assert isinstance(exc.value, HandoffError)
        assert find_mission_record("no-such-mission", data_root) is None


class TestGaps:
    def test_a_missing_dossier_is_a_named_gap(self, data_root):
        mission = _mission(data_root)
        body = json.loads(build_handoff(mission.id, data_root)
                          .read_text(encoding="utf-8"))
        sources = {gap["source"] for gap in body["gaps"]}
        assert GAP_DOSSIER in sources
        assert body["dossier"] == {}
        detail = next(g["detail"] for g in body["gaps"]
                      if g["source"] == GAP_DOSSIER)
        assert "no dossier" in detail

    def test_a_mission_without_jobs_names_the_jobs_and_checkpoint_gap(self, data_root):
        mission = _mission(data_root)
        _seed_dossier(data_root, mission)
        body = json.loads(build_handoff(mission.id, data_root)
                          .read_text(encoding="utf-8"))
        sources = {gap["source"] for gap in body["gaps"]}
        assert GAP_JOBS in sources
        assert body["checkpoint"] == {}

    def test_a_job_without_checkpoints_names_the_checkpoint_gap(self, data_root):
        mission = _mission(data_root)
        _seed_dossier(data_root, mission)
        job_id = "33333333-3333-4333-8333-333333333333"
        link_job_to_mission(PROJECT, mission.id, job_id, "initial", root=data_root)
        body = json.loads(build_handoff(mission.id, data_root)
                          .read_text(encoding="utf-8"))
        gap = next(g for g in body["gaps"] if g["source"] == GAP_CHECKPOINT)
        assert "never checkpointed" in gap["detail"]
        assert job_id in gap["detail"]

    def test_a_job_whose_record_cannot_be_read_names_the_decisions_gap(
            self, data_root):
        from packages.orchestration.handoff import GAP_OPEN_DECISIONS

        mission = _mission(data_root)
        _seed_dossier(data_root, mission)
        job_id = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
        _seed_job_checkpoint(data_root, mission, job_id)  # checkpoint, no job file
        body = json.loads(build_handoff(mission.id, data_root)
                          .read_text(encoding="utf-8"))
        gap = next(g for g in body["gaps"]
                   if g["source"] == GAP_OPEN_DECISIONS)
        assert job_id in gap["detail"]
        assert body["open_decisions"] == []

    def test_a_readable_jobs_open_decisions_are_carried_with_their_ids(
            self, data_root):
        from packages.orchestration.handoff import GAP_OPEN_DECISIONS

        mission = _mission(data_root)
        _seed_dossier(data_root, mission)
        job_id = _seed_readable_job(data_root, mission)
        body = json.loads(build_handoff(mission.id, data_root)
                          .read_text(encoding="utf-8"))
        assert GAP_OPEN_DECISIONS not in {g["source"] for g in body["gaps"]}
        assert body["open_decisions"], "the queue derives at least one open item"
        for row in body["open_decisions"]:
            assert row["id"] and row["job_id"] == job_id
            # A derived decision's timestamp is minted at derivation time and
            # would differ on every build; the answer command is what matters.
            assert "created_at" not in row
            assert set(row) == {"id", "job_id", "type", "severity", "summary",
                                "next_actions"}

    def test_a_zero_progress_mission_is_a_valid_handoff(self, data_root):
        mission = _mission(data_root, goal="a goal and nothing else yet")
        path = build_handoff(mission.id, data_root)
        body = json.loads(path.read_text(encoding="utf-8"))
        assert body["goal"] == "a goal and nothing else yet"
        assert body["open_decisions"] == []
        assert body["next_intent"] == {}
        sources = {gap["source"] for gap in body["gaps"]}
        assert {GAP_DOSSIER, GAP_JOBS, GAP_NEXT_INTENT} <= sources
        # Every empty section is explained by a gap rather than left silent.
        rendered = path.with_suffix(".md").read_text(encoding="utf-8")
        assert "(gap: no dossier stored)" in rendered
        assert "(gap: no next intent recorded)" in rendered


class TestIdempotence:
    def test_the_same_state_builds_byte_identical_bytes(self, data_root):
        mission = _mission(data_root)
        _seed_dossier(data_root, mission)
        _seed_job_checkpoint(
            data_root, mission, "44444444-4444-4444-8444-444444444444")
        first = build_handoff(mission.id, data_root)
        first_hash = hashlib.sha256(first.read_bytes()).hexdigest()
        second = build_handoff(mission.id, data_root)
        assert second == first
        assert hashlib.sha256(second.read_bytes()).hexdigest() == first_hash

    def test_derived_open_decisions_do_not_break_byte_identity(self, data_root):
        """The queue DERIVES decisions per call; the handoff must still settle."""
        mission = _mission(data_root)
        _seed_dossier(data_root, mission)
        _seed_readable_job(data_root, mission)
        first = build_handoff(mission.id, data_root)
        first_bytes = first.read_bytes()
        assert json.loads(first_bytes)["open_decisions"]
        assert build_handoff(mission.id, data_root) == first
        assert first.read_bytes() == first_bytes
        assert handoff_versions(PROJECT, mission.id, data_root) == [1]

    def test_a_repeat_build_creates_no_duplicate(self, data_root):
        mission = _mission(data_root)
        _seed_dossier(data_root, mission)
        for _ in range(3):
            build_handoff(mission.id, data_root)
        assert handoff_versions(PROJECT, mission.id, data_root) == [1]

    def test_changed_state_accumulates_the_next_version(self, data_root):
        mission = _mission(data_root)
        _seed_dossier(data_root, mission, next_step="first step")
        first = build_handoff(mission.id, data_root)
        _seed_job_checkpoint(
            data_root, mission, "55555555-5555-4555-8555-555555555555")
        second = build_handoff(mission.id, data_root)
        assert second != first
        assert handoff_versions(PROJECT, mission.id, data_root) == [1, 2]
        assert latest_handoff_version(PROJECT, mission.id, data_root) == 2
        assert json.loads(second.read_text(encoding="utf-8"))["checkpoint"]
        # The older account is left exactly as it was written.
        assert not json.loads(first.read_text(encoding="utf-8"))["checkpoint"]

    def test_no_wall_clock_value_reaches_the_body(self, data_root):
        """Provenance is the SOURCE artifacts' own timestamps, nothing else."""
        mission = _mission(data_root)
        _seed_dossier(data_root, mission)
        _seed_job_checkpoint(
            data_root, mission, "66666666-6666-4666-8666-666666666666")
        body = compose_handoff_body(
            load_mission(PROJECT, mission.id, data_root), data_root)
        provenance = body["provenance"]
        assert provenance["mission_created_at"] == \
            load_mission(PROJECT, mission.id, data_root).created_at
        assert provenance["checkpoint_created_at"] == \
            "2026-08-06T10:00:00+00:00"
        assert compose_handoff_body(
            load_mission(PROJECT, mission.id, data_root), data_root) == body


class TestPurity:
    def test_building_mutates_no_mission_job_or_queue_state(self, data_root):
        mission = _mission(data_root)
        _seed_dossier(data_root, mission)
        _seed_job_checkpoint(
            data_root, mission, "77777777-7777-4777-8777-777777777777")
        before = _state_snapshot(data_root)
        build_handoff(mission.id, data_root)
        build_handoff(mission.id, data_root)
        assert _state_snapshot(data_root) == before

    def test_the_only_new_files_are_the_two_handoff_artifacts(self, data_root):
        mission = _mission(data_root)
        _seed_dossier(data_root, mission)
        before = {p for p in data_root.rglob("*") if p.is_file()}
        build_handoff(mission.id, data_root)
        created = {p.name for p in data_root.rglob("*")
                   if p.is_file()} - {p.name for p in before}
        assert created == {"handoff_v1.json", "handoff_v1.md"}


class TestRedaction:
    def test_a_secret_key_in_the_next_intent_is_redacted(self, data_root):
        mission = _mission(data_root)
        _seed_dossier(data_root, mission)
        _seed_job_checkpoint(
            data_root, mission, "88888888-8888-4888-8888-888888888888",
            next_intent={"task": "call the API",
                         "api_token": "sk-live-must-never-be-written"})
        path = build_handoff(mission.id, data_root)
        text = path.read_text(encoding="utf-8")
        assert "sk-live-must-never-be-written" not in text
        assert "[REDACTED]" in text
        body = json.loads(text)
        assert body["next_intent"]["intent"]["api_token"] == "[REDACTED]"
        assert body["next_intent"]["intent"]["task"] == "call the API"

    def test_the_manifest_denylist_is_the_one_that_applies(self):
        """The denylist reused is run_manifest's — same terms, no second list."""
        from packages.orchestration.run_manifest import is_secret_key

        for key in ("password", "aws_secret", "credential_file", "api_key"):
            assert is_secret_key(key)
            assert redact_handoff_value({key: "raw"})[key] == "[REDACTED]"
        assert redact_handoff_value({"cycle_index": 3})["cycle_index"] == 3


class TestRenderedBlock:
    def test_the_sections_render_in_one_fixed_order_dossier_first(self, data_root):
        mission = _mission(data_root)
        _seed_dossier(data_root, mission)
        _seed_job_checkpoint(
            data_root, mission, "99999999-9999-4999-8999-999999999999")
        path = build_handoff(mission.id, data_root)
        rendered = path.with_suffix(".md").read_text(encoding="utf-8")
        positions = [rendered.index(f"## {name}") for name in HANDOFF_SECTIONS]
        assert positions == sorted(positions)
        assert HANDOFF_SECTIONS[0] == "Dossier"
        assert f"Schema version: {HANDOFF_SCHEMA_VERSION}" in rendered

    def test_the_rendered_block_is_derived_from_the_body_alone(self, data_root):
        mission = _mission(data_root)
        _seed_dossier(data_root, mission)
        path = build_handoff(mission.id, data_root)
        body = json.loads(path.read_text(encoding="utf-8"))
        assert render_handoff(body) == \
            path.with_suffix(".md").read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# T002 — triggers, consumption, reference verification
# ---------------------------------------------------------------------------

def _plan_for(mission_id: str, data_root, *, milestone: str = "M001"):
    """A compiled one-milestone plan, so the loop has something to dispatch."""
    from packages.orchestration.mission_plan_schema import (
        MISSION_PLAN_SCHEMA_V,
        Milestone,
        MissionPlan,
    )
    from packages.orchestration.mission_state import set_mission_plan

    plan = MissionPlan(
        schema_v=MISSION_PLAN_SCHEMA_V,
        milestones=[Milestone(
            id=milestone, goal=f"The outcome of {milestone} holds",
            rationale=f"{milestone} exists", depends_on=[],
            jobs_draft=[{"title": "work", "goal": "do it", "est_band": "M"}])],
        compiled=True, origin="provider")
    set_mission_plan(PROJECT, mission_id, plan.model_dump(), data_root)


class _LoopJob:
    """The smallest thing the dispatch seam must return: an id and no plan."""

    def __init__(self, job_id: str = "job-0001"):
        self.id = job_id
        self.flight_plan = None


def _dispatch_double(project_id, mission_id, step, *, root=None, now=None):
    return _LoopJob()


def _execute_double(job):
    from packages.orchestration.orchestrator_loop import MilestoneEvidence  # noqa: F401

    class _Run:
        stopped = False
        stop_reason = ""
        cycles = 1
    return _Run()


def _dispatching_provider():
    """A provider that keeps asking for the same dispatch — never terminal."""
    import json as _json

    from packages.orchestration.orchestrator_move_schema import (
        ORCHESTRATOR_MOVE_SCHEMA_V,
    )

    move = _json.dumps({"schema_v": ORCHESTRATOR_MOVE_SCHEMA_V,
                        "kind": "dispatch_job",
                        "payload": {"milestone_id": "M001", "step": "keep going"}})
    return lambda prompt, attempt: move


def _run_to_limit(mission, data_root, *, iterations: int = 1):
    from packages.orchestration.orchestrator_loop import LoopLimits, run_mission

    return run_mission(
        mission.id, LoopLimits(max_iterations=iterations), project_id=PROJECT,
        call_fn=_dispatching_provider(), root=data_root,
        dispatch=_dispatch_double, execute=_execute_double,
        control_root_path=data_root / "control")


class TestLoopTrigger:
    def test_the_iteration_limit_builds_a_handoff(self, data_root):
        from packages.orchestration.orchestrator_loop import (
            TERMINAL_ITERATION_LIMIT,
        )

        mission = _mission(data_root)
        _plan_for(mission.id, data_root)
        result = _run_to_limit(mission, data_root)
        assert result.terminal == TERMINAL_ITERATION_LIMIT
        assert result.handoff_error == ""
        assert Path(result.handoff_path).is_file()
        assert Path(result.handoff_path).name == "handoff_v1.json"

    def test_a_stop_builds_a_handoff(self, data_root):
        from packages.orchestration.orchestrator_loop import TERMINAL_STOPPED
        from packages.orchestration.safe_points import request_stop

        mission = _mission(data_root)
        _plan_for(mission.id, data_root)
        control = data_root / "control"
        request_stop(mission.id, reason="operator says stop",
                     control_root_path=control)
        result = _run_to_limit(mission, data_root, iterations=2)
        assert result.terminal == TERMINAL_STOPPED
        assert Path(result.handoff_path).is_file()

    def test_a_build_failure_does_not_mask_the_terminal(self, data_root,
                                                        monkeypatch):
        from packages.orchestration import handoff as handoff_module
        from packages.orchestration.orchestrator_loop import (
            TERMINAL_ITERATION_LIMIT,
        )

        def _boom(*args, **kwargs):
            raise OSError("the evidence area is gone")

        monkeypatch.setattr(handoff_module, "build_handoff", _boom)
        mission = _mission(data_root)
        _plan_for(mission.id, data_root)
        result = _run_to_limit(mission, data_root)
        assert result.terminal == TERMINAL_ITERATION_LIMIT
        assert result.handoff_path == ""
        assert "the evidence area is gone" in result.handoff_error


class TestConsumption:
    def test_the_newest_valid_handoff_is_the_one_resumed_from(self, data_root):
        from packages.orchestration.handoff import handoff_resume_seed

        mission = _mission(data_root)
        _seed_dossier(data_root, mission, next_step="first step")
        build_handoff(mission.id, data_root)
        _advance_dossier(data_root, mission, next_step="second step")
        newest = build_handoff(mission.id, data_root)
        seed = handoff_resume_seed(mission.id, data_root)
        assert seed is not None
        assert seed.path == newest
        assert seed.path.name == "handoff_v2.json"
        assert "second step" in seed.text

    def test_an_unknown_schema_version_is_refused_not_guessed(self, data_root):
        from packages.orchestration.handoff import (
            HandoffSchemaVersionError,
            handoff_resume_seed,
        )

        mission = _mission(data_root)
        _seed_dossier(data_root, mission)
        path = build_handoff(mission.id, data_root)
        body = json.loads(path.read_text(encoding="utf-8"))
        body["schema_version"] = HANDOFF_SCHEMA_VERSION + 1
        path.write_text(json.dumps(body, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8")
        with pytest.raises(HandoffSchemaVersionError) as exc:
            handoff_resume_seed(mission.id, data_root)
        assert str(HANDOFF_SCHEMA_VERSION + 1) in str(exc.value)

    def test_a_stale_worktree_head_refuses_with_the_checkpoint_message(
            self, data_root, monkeypatch):
        from packages.orchestration import checkpoints as checkpoints_module
        from packages.orchestration.handoff import (
            HandoffReferenceStaleError,
            handoff_resume_seed,
        )

        mission = _mission(data_root)
        _seed_dossier(data_root, mission)
        job_id = "cccccccc-cccc-4ccc-8ccc-cccccccccccc"
        _seed_job_checkpoint(data_root, mission, job_id)
        build_handoff(mission.id, data_root)
        monkeypatch.setattr(checkpoints_module, "resolve_live_worktree_head",
                            lambda _job_id: "deadbeef" + "0" * 32)
        with pytest.raises(HandoffReferenceStaleError) as exc:
            handoff_resume_seed(mission.id, data_root)
        expected = checkpoints_module.worktree_drift_message(
            "c0ffee" + "0" * 34, "deadbeef" + "0" * 32)
        assert str(exc.value) == expected

    def test_a_vanished_checkpoint_refuses(self, data_root):
        from packages.orchestration.checkpoints import checkpoint_dir
        from packages.orchestration.handoff import (
            HandoffReferenceStaleError,
            handoff_resume_seed,
        )

        mission = _mission(data_root)
        _seed_dossier(data_root, mission)
        job_id = "dddddddd-dddd-4ddd-8ddd-dddddddddddd"
        _seed_job_checkpoint(data_root, mission, job_id)
        build_handoff(mission.id, data_root)
        for path in checkpoint_dir(job_id).glob("checkpoint_*.json"):
            path.unlink()
        with pytest.raises(HandoffReferenceStaleError) as exc:
            handoff_resume_seed(mission.id, data_root)
        assert "no verifying checkpoint" in str(exc.value)

    def test_a_gap_only_handoff_has_nothing_to_verify(self, data_root):
        from packages.orchestration.handoff import handoff_resume_seed

        mission = _mission(data_root)
        build_handoff(mission.id, data_root)  # zero progress: all gaps
        seed = handoff_resume_seed(mission.id, data_root)
        assert seed is not None
        assert seed.body["checkpoint"] == {}

    def test_the_seed_reaches_the_first_iterations_context_only(self, data_root):
        from packages.orchestration.orchestrator_loop import SECTION_HANDOFF

        mission = _mission(data_root)
        _plan_for(mission.id, data_root)
        first = _run_to_limit(mission, data_root)          # writes handoff_v1
        assert first.resumed_from == ""                     # nothing to resume
        provider = _dispatching_provider()
        prompts: list[str] = []

        def recording(prompt, attempt):
            prompts.append(prompt)
            return provider(prompt, attempt)

        from packages.orchestration.orchestrator_loop import (
            LoopLimits,
            run_mission,
        )

        second = run_mission(
            mission.id, LoopLimits(max_iterations=2), project_id=PROJECT,
            call_fn=recording, root=data_root, dispatch=_dispatch_double,
            execute=_execute_double, control_root_path=data_root / "control")
        assert second.resumed_from == "handoff_v1.json"
        assert SECTION_HANDOFF in prompts[0]
        assert SECTION_HANDOFF not in prompts[1]

    def test_the_root_conflict_is_named_rather_than_silent(self, data_root,
                                                           tmp_path):
        from packages.orchestration.handoff import handoff_root_conflict

        assert handoff_root_conflict(None) == ""
        assert handoff_root_conflict(data_root) == ""
        message = handoff_root_conflict(tmp_path / "elsewhere")
        assert "R-0203" in message
        assert "REMEDY_DATA_DIR" in message

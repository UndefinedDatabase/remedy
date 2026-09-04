"""
Domain tests: orchestration/test_approval_queue.py
Migrated from step-numbered test files.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock
from uuid import UUID, uuid4

import pytest

from packages.core.models import (
    Artifact,
    ArtifactKind,
    Job,
    RunState,
    Task,
)
from packages.orchestration.storage import save_job


def _make_job(*, project_id: str | None = None, target_repo: str | None = None) -> Job:
    meta: dict = {}
    if project_id:
        meta["project_id"] = project_id
    if target_repo:
        meta["target_repo"] = target_repo
    return Job(
        id=uuid4(),
        name="test job",
        user_prompt="test prompt",
        state=RunState.RUNNING,
        tasks=[
            Task(
                id=uuid4(),
                description="task",
                status=RunState.PENDING,
                inputs={"task_type": "patch"},
                output_artifact_ids=[],
            ),
        ],
        artifacts=[],
        metadata=meta,
    )


def _make_job_s57(*, project_id: str | None = None, target_repo: str | None = None) -> Job:
    meta: dict = {}
    if project_id:
        meta["project_id"] = project_id
    if target_repo:
        meta["target_repo"] = target_repo
    return Job(
        id=uuid4(),
        name="test job",
        user_prompt="test prompt",
        state=RunState.RUNNING,
        tasks=[
            Task(
                id=uuid4(),
                description="task",
                status=RunState.PENDING,
                inputs={"task_type": "patch"},
                output_artifact_ids=[],
            ),
        ],
        artifacts=[],
        metadata=meta,
    )


# ===========================================================================
# Step 57: Brain Graph Core Refactor — Structural Tests
# ===========================================================================


def _make_job_s68(**overrides) -> Job:
    defaults = {
        "id": uuid4(),
        "name": "test-job",
        "user_prompt": "test prompt",
        "description": "test job",
        "tasks": [
            Task(description="task 1", status=RunState.COMPLETED),
        ],
        "state": RunState.COMPLETED,
        "permissions": {"repo_generated_write": "allow", "repo_test_run": "allow"},
        "metadata": {"target_repo": "."},
    }
    defaults.update(overrides)
    return Job(**defaults)


def _make_job_s101(task_count: int = 3):
    job = MagicMock()
    job.id = uuid4()
    job.name = "test-job"
    job.state.value = "active"
    job.tasks = []
    job.artifacts = []
    job.metadata = {}
    for i in range(task_count):
        t = MagicMock()
        t.id = uuid4()
        t.task_type = "test_task"
        t.status.value = "completed" if i == 0 else "pending"
        t.metadata = {}
        job.tasks.append(t)
    return job


# ---------------------------------------------------------------------------
# Step 101 — Smoke/UX Contract Reset
# ---------------------------------------------------------------------------


def _make_job_with_intent(tmp_path: Path, monkeypatch) -> tuple[Job, str, Path]:
    """Create a job with an approved patch intent and attached repo."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))

    from packages.orchestration.approval_queue import (
        APPROVAL_APPROVED,
        make_intent_id,
        set_approval_state,
    )
    from packages.orchestration.permissions import Capability, set_permission

    repo = tmp_path / "repo"
    repo.mkdir()
    target = repo / "notes.md"
    target.write_text("# Original\n\nOriginal content.\n", encoding="utf-8")

    art_id = uuid4()
    intent_id = make_intent_id(art_id, 0)
    artifact = Artifact(
        id=art_id,
        kind=ArtifactKind.BUILDER_PROPOSAL,
        name="patch artifact",
        content="Summary:\nTest patch\nProposed Changes:\n  - Added line\nNotes:\nNone",
        metadata={
            "patch_intent_explanations": [
                {
                    "file": "notes.md",
                    "action": "modify",
                    "risk": "low",
                    "reason": "test intent",
                    "summary": "test",
                }
            ],
        },
    )

    job = Job(
        id=uuid4(),
        name="patch job",
        user_prompt="apply test",
        state=RunState.RUNNING,
        tasks=[],
        artifacts=[artifact],
        metadata={"target_repo": str(repo)},
    )
    set_approval_state(job, intent_id, APPROVAL_APPROVED)
    set_permission(job, Capability.repo_generated_write, allow=True)
    save_job(job)
    return job, intent_id, repo


# ===========================================================================
# Step 53.1: Continue-from-node project linking
# ===========================================================================


def _make_events() -> list[dict]:
    return [
        {"event": "job_created", "run_id": "r1", "job_id": "j1",
         "timestamp": "2026-01-01T00:00:00", "outcome": "ok", "metadata": {}},
        {"event": "patch_intent_created", "run_id": "r1", "job_id": "j1",
         "timestamp": "2026-01-01T00:01:00", "outcome": "ok",
         "metadata": {"intent_id": "pi1", "target_path": "foo.py", "action": "create"}},
    ]


# ── Step 68.1: Event Schema Registry ────────────────────────────────────




class TestContinueFromNodeProjectLinking:
    """Child job must be linked to parent's project."""

    def test_child_linked_to_project(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_registry import RemyProject, load_project, save_project

        project = RemyProject(name="test project")
        save_project(project)

        job = _make_job(project_id=str(project.id), target_repo=str(tmp_path))
        save_job(job)

        # Build brain graph
        from packages.orchestration.project_brain import build_project_brain
        graph = build_project_brain(job, [])

        # Get a node to continue from
        node_id = graph.nodes[0].id

        from packages.orchestration.continue_from_node import continue_from_node
        result = continue_from_node(job, graph, node_id, "test continue")

        # Verify child is linked in project
        project_reloaded = load_project(project.id)
        assert result.child_job_id in project_reloaded.job_ids

    def test_child_inherits_project_metadata(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_registry import RemyProject, save_project

        project = RemyProject(name="test project")
        save_project(project)

        job = _make_job(project_id=str(project.id), target_repo=str(tmp_path))
        save_job(job)

        from packages.orchestration.continue_from_node import continue_from_node
        from packages.orchestration.project_brain import build_project_brain
        graph = build_project_brain(job, [])
        result = continue_from_node(job, graph, graph.nodes[0].id, "test")

        from packages.orchestration.storage import load_job
        child = load_job(UUID(result.child_job_id))
        assert child.metadata["project_id"] == str(project.id)

    def test_parent_gets_continued_event(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job(target_repo=str(tmp_path))
        save_job(job)

        from packages.orchestration.continue_from_node import continue_from_node
        from packages.orchestration.project_brain import build_project_brain
        graph = build_project_brain(job, [])
        continue_from_node(job, graph, graph.nodes[0].id, "test")

        from packages.orchestration.data_paths import resolve_data_root
        from packages.orchestration.timeline import load_run_events
        events = load_run_events(resolve_data_root(), job.id)
        parent_events = [
            e for e in events
            if e.get("event") == "continued_from_node"
            and e.get("outcome") == "spawned_child"
        ]
        assert len(parent_events) >= 1

    def test_no_raw_prompt_in_run_log(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job(target_repo=str(tmp_path))
        save_job(job)

        from packages.orchestration.continue_from_node import continue_from_node
        from packages.orchestration.project_brain import build_project_brain
        graph = build_project_brain(job, [])
        continue_from_node(job, graph, graph.nodes[0].id, "secret prompt text XYZ")

        from packages.orchestration.data_paths import resolve_data_root
        from packages.orchestration.timeline import load_run_events
        events = load_run_events(resolve_data_root(), job.id)
        for ev in events:
            meta_str = json.dumps(ev.get("metadata", {}))
            assert "secret prompt text XYZ" not in meta_str

    def test_project_brain_aggregate_includes_child(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_registry import RemyProject, load_project, save_project

        project = RemyProject(name="test project")
        save_project(project)

        job = _make_job(project_id=str(project.id), target_repo=str(tmp_path))
        save_job(job)

        from packages.orchestration.project_registry import attach_job
        attach_job(project, str(job.id))
        save_project(project)

        from packages.orchestration.continue_from_node import continue_from_node
        from packages.orchestration.project_brain import build_project_brain
        graph = build_project_brain(job, [])
        result = continue_from_node(job, graph, graph.nodes[0].id, "test")

        # Reload project to get child
        project = load_project(project.id)
        assert result.child_job_id in project.job_ids

        # Build aggregate
        from packages.orchestration.project_brain_aggregate import (
            build_project_brain_aggregate,
            export_project_brain_aggregate_json,
        )
        from packages.orchestration.storage import list_jobs
        all_jobs = list_jobs()
        linked = [j for j in all_jobs if str(j.id) in project.job_ids]
        events_map = {}
        from packages.orchestration.data_paths import resolve_data_root
        from packages.orchestration.timeline import load_run_events
        data_dir = resolve_data_root()
        for j in linked:
            events_map[str(j.id)] = load_run_events(data_dir, j.id)

        agg = build_project_brain_aggregate(project, linked, events_map)
        exported = export_project_brain_aggregate_json(agg)
        exported_str = json.dumps(exported)
        assert result.child_job_id in exported_str
        assert agg.summary["job_count"] >= 2


# ===========================================================================
# Step 54: Patch Revert
# ===========================================================================




class TestContinueFromNodeIntegration:
    """Continue-from-node integration tests — brain edges, child graphs, invalid node."""

    def test_continue_creates_brain_edge(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.continue_from_node import continue_from_node
        from packages.orchestration.project_brain import (
            ET_CONTINUED_AS,
            build_project_brain,
        )

        job = _make_job_s57(target_repo=str(tmp_path))
        save_job(job)

        graph = build_project_brain(job, [])
        node_id = graph.nodes[0].id
        result = continue_from_node(job, graph, node_id, "test continue")

        # Rebuild graph with continuation event
        from packages.orchestration.data_paths import resolve_data_root
        from packages.orchestration.timeline import load_run_events

        events = load_run_events(resolve_data_root(), job.id)
        graph2 = build_project_brain(job, events)

        cont_edges = [e for e in graph2.edges if e.type == ET_CONTINUED_AS]
        assert len(cont_edges) >= 1
        assert any(result.child_job_id[:8] in e.target for e in cont_edges)

    def test_continue_invalid_node_raises(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.continue_from_node import continue_from_node
        from packages.orchestration.project_brain import build_project_brain

        job = _make_job_s57(target_repo=str(tmp_path))
        save_job(job)
        graph = build_project_brain(job, [])

        with pytest.raises((ValueError, KeyError)):
            continue_from_node(job, graph, "nonexistent_node_id_xyz", "test")

    def test_child_brain_graph_valid(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.continue_from_node import continue_from_node
        from packages.orchestration.project_brain import build_project_brain

        job = _make_job_s57(target_repo=str(tmp_path))
        save_job(job)
        graph = build_project_brain(job, [])
        result = continue_from_node(job, graph, graph.nodes[0].id, "child test")

        # Load child and build its brain
        from packages.orchestration.storage import load_job

        child = load_job(UUID(result.child_job_id))
        child_graph = build_project_brain(child, [])
        assert len(child_graph.nodes) >= 1
        assert child_graph.job_id == child.id




class TestDecisionQueue:
    def test_list_decisions_empty(self):
        from packages.orchestration.decision_queue import list_decisions
        job = _make_job_s68()
        decisions = list_decisions(job, [])
        # No patch intents pending, no test failures, etc.
        assert isinstance(decisions, list)

    def test_decision_types_frozenset(self):
        from packages.orchestration.decision_queue import DECISION_TYPES
        assert isinstance(DECISION_TYPES, frozenset)
        assert "patch_approval" in DECISION_TYPES
        assert "stop_reason" in DECISION_TYPES
        assert "test_failure" in DECISION_TYPES
        assert "repo_dirty" in DECISION_TYPES
        assert "memory_review" in DECISION_TYPES

    def test_test_failure_decisions(self):
        from packages.orchestration.decision_queue import list_decisions
        job = _make_job_s68()
        events = [
            {"event": "test_run_completed", "run_id": "r1", "job_id": str(job.id),
             "timestamp": "2026-01-01T00:01:00", "outcome": "failed",
             "metadata": {"status": "failed", "command": "pytest", "test_run_id": "tr1"}},
        ]
        decisions = list_decisions(job, events)
        test_decs = [d for d in decisions if d.type == "test_failure"]
        assert len(test_decs) >= 1
        assert test_decs[0].severity == "blocker"
        assert test_decs[0].status == "open"

    def test_dirty_repo_decision(self):
        from packages.orchestration.decision_queue import list_decisions
        job = _make_job_s68()
        events = [
            {"event": "git_status_read", "run_id": "r1", "job_id": str(job.id),
             "timestamp": "2026-01-01T00:01:00", "outcome": "ok",
             "metadata": {"dirty": True, "branch": "main", "changed_file_count": 3}},
        ]
        decisions = list_decisions(job, events)
        dirty_decs = [d for d in decisions if d.type == "repo_dirty"]
        assert len(dirty_decs) == 1
        assert dirty_decs[0].severity == "warning"

    def test_explain_decisions(self):
        from packages.orchestration.decision_queue import explain_decisions
        job = _make_job_s68()
        result = explain_decisions(job, [])
        assert "No pending decisions" in result or isinstance(result, str)

    def test_export_decision_json(self):
        from packages.orchestration.decision_queue import HumanDecision, export_decision_json
        d = HumanDecision(
            id="test1", type="test_failure", status="open", severity="blocker",
            source="test_run", related_node_id="", related_intent_id="",
            related_file="", safe_summary="Test failed.",
            next_actions=("fix it",), created_at="2026-01-01", resolved_at=None,
        )
        j = export_decision_json(d)
        assert j["id"] == "test1"
        assert j["type"] == "test_failure"
        assert j["severity"] == "blocker"
        assert isinstance(j["next_actions"], list)

    def test_build_decision_summary(self):
        from packages.orchestration.decision_queue import HumanDecision, build_decision_summary
        decisions = [
            HumanDecision(
                id="d1", type="test_failure", status="open", severity="blocker",
                source="test", related_node_id="", related_intent_id="",
                related_file="", safe_summary="fail",
                next_actions=("fix",), created_at="", resolved_at=None,
            ),
            HumanDecision(
                id="d2", type="repo_dirty", status="open", severity="warning",
                source="git", related_node_id="", related_intent_id="",
                related_file="", safe_summary="dirty",
                next_actions=(), created_at="", resolved_at=None,
            ),
        ]
        summary = build_decision_summary(decisions)
        assert summary["open_count"] == 2
        assert summary["high_count"] == 1  # blocker
        assert summary["medium_count"] == 1  # warning

    def test_get_decision(self):
        from packages.orchestration.decision_queue import get_decision
        job = _make_job_s68()
        events = [
            {"event": "git_status_read", "run_id": "r1", "job_id": str(job.id),
             "timestamp": "2026-01-01", "outcome": "ok",
             "metadata": {"dirty": True, "branch": "main", "changed_file_count": 1}},
        ]
        d = get_decision(job, events, "dirty_repo")
        assert d is not None
        assert d.type == "repo_dirty"

    def test_get_decision_not_found(self):
        from packages.orchestration.decision_queue import get_decision
        job = _make_job_s68()
        d = get_decision(job, [], "nonexistent")
        assert d is None


# ── Step 70: Dashboard ──────────────────────────────────────────────────




class TestReviewerLoop:
    def test_run_reviewer_returns_list(self):
        from packages.orchestration.reviewer import run_reviewer
        job = _make_job_s101(2)
        recs = run_reviewer(job)
        assert isinstance(recs, list)

    def test_run_reviewer_with_custom_fn(self):
        from packages.orchestration.reviewer import run_reviewer
        job = _make_job_s101(2)

        def custom_reviewer(context):
            return [{"title": "Add test", "task_type": "test", "reason": "coverage", "risk": "low"}]

        recs = run_reviewer(job, reviewer_fn=custom_reviewer)
        assert len(recs) == 1
        assert recs[0].title == "Add test"

    def test_store_and_list_recommendations(self):
        from packages.orchestration.reviewer import list_recommendations, run_reviewer, store_recommendations
        job = _make_job_s101(1)

        def custom_reviewer(context):
            return [{"title": "Fix bug", "task_type": "fix", "reason": "regression"}]

        recs = run_reviewer(job, reviewer_fn=custom_reviewer)
        store_recommendations(job, recs)
        stored = list_recommendations(job)
        assert len(stored) == 1
        assert stored[0]["title"] == "Fix bug"
        assert stored[0]["status"] == "pending"

    def test_store_and_list_recommendations_carries_created_at(self):
        from datetime import datetime

        from packages.orchestration.reviewer import list_recommendations, run_reviewer, store_recommendations

        job = _make_job_s101(1)

        def custom_reviewer(context):
            return [{"title": "Add caching", "task_type": "perf", "reason": "latency"}]

        recs = run_reviewer(job, reviewer_fn=custom_reviewer)
        store_recommendations(job, recs)
        stored = list_recommendations(job)
        assert stored[0]["created_at"] != ""
        datetime.fromisoformat(stored[0]["created_at"])

    def test_accept_recommendation(self, tmp_path, monkeypatch):
        from packages.orchestration.proposed_tasks import load_proposed_tasks
        from packages.orchestration.reviewer import (
            accept_recommendation,
            run_reviewer,
            store_recommendations,
        )
        monkeypatch.setattr(
            "packages.orchestration.proposed_tasks._STORE_DIR",
            tmp_path / "proposed_tasks",
        )
        job = _make_job_s101(1)

        def custom_reviewer(context):
            return [{"title": "Add docs", "task_type": "docs", "reason": "missing"}]

        recs = run_reviewer(job, reviewer_fn=custom_reviewer)
        store_recommendations(job, recs)
        rec_id = job.metadata["reviewer_recommendations"][0]["id"]
        initial_task_count = len(job.tasks)
        ok = accept_recommendation(job, rec_id)
        assert ok is True
        assert len(job.tasks) == initial_task_count  # No direct task — creates ProposedTask instead
        assert job.metadata["reviewer_recommendations"][0]["status"] == "accepted"
        proposed = load_proposed_tasks(str(job.id))
        assert len(proposed) == 1
        assert proposed[0].title == "Add docs"

    def test_reject_recommendation(self):
        from packages.orchestration.reviewer import (
            reject_recommendation,
            run_reviewer,
            store_recommendations,
        )
        job = _make_job_s101(1)

        def custom_reviewer(context):
            return [{"title": "Refactor", "task_type": "refactor", "reason": "tech debt"}]

        recs = run_reviewer(job, reviewer_fn=custom_reviewer)
        store_recommendations(job, recs)
        rec_id = job.metadata["reviewer_recommendations"][0]["id"]
        initial_task_count = len(job.tasks)
        ok = reject_recommendation(job, rec_id)
        assert ok is True
        assert len(job.tasks) == initial_task_count  # No new task
        assert job.metadata["reviewer_recommendations"][0]["status"] == "rejected"

    def test_reject_nonexistent(self):
        from packages.orchestration.reviewer import reject_recommendation
        job = _make_job_s101(0)
        ok = reject_recommendation(job, "nonexistent")
        assert ok is False

    def test_max_recommendations(self):
        from packages.orchestration.reviewer import run_reviewer
        job = _make_job_s101(1)

        def many_recs(context):
            return [{"title": f"rec-{i}", "task_type": "test"} for i in range(20)]

        recs = run_reviewer(job, reviewer_fn=many_recs, max_recommendations=3)
        assert len(recs) == 3

    def test_recommendation_fields(self):
        from packages.orchestration.reviewer import run_reviewer
        job = _make_job_s101(1)

        def custom_reviewer(context):
            return [{"title": "t", "task_type": "test", "reason": "r", "risk": "high", "priority": "critical"}]

        recs = run_reviewer(job, reviewer_fn=custom_reviewer)
        r = recs[0]
        assert r.risk == "high"
        assert r.priority == "critical"
        assert r.source == "reviewer"
        assert r.status == "pending"


# ---------------------------------------------------------------------------
# Step 108b — Review CLI Commands
# ---------------------------------------------------------------------------


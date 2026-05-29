"""Tests for Steps 53.1, 54, 55, 56."""

from __future__ import annotations

import json
from pathlib import Path
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


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


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

        from packages.orchestration.project_brain import build_project_brain
        from packages.orchestration.continue_from_node import continue_from_node
        graph = build_project_brain(job, [])
        result = continue_from_node(job, graph, graph.nodes[0].id, "test")

        from packages.orchestration.storage import load_job
        child = load_job(UUID(result.child_job_id))
        assert child.metadata["project_id"] == str(project.id)

    def test_parent_gets_continued_event(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job(target_repo=str(tmp_path))
        save_job(job)

        from packages.orchestration.project_brain import build_project_brain
        from packages.orchestration.continue_from_node import continue_from_node
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

        from packages.orchestration.project_brain import build_project_brain
        from packages.orchestration.continue_from_node import continue_from_node
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

        from packages.orchestration.project_brain import build_project_brain
        from packages.orchestration.continue_from_node import continue_from_node
        graph = build_project_brain(job, [])
        result = continue_from_node(job, graph, graph.nodes[0].id, "test")

        # Reload project to get child
        project = load_project(project.id)
        assert result.child_job_id in project.job_ids

        # Build aggregate
        from packages.orchestration.storage import list_jobs
        from packages.orchestration.project_brain_aggregate import (
            build_project_brain_aggregate,
            export_project_brain_aggregate_json,
        )
        all_jobs = list_jobs()
        linked = [j for j in all_jobs if str(j.id) in project.job_ids]
        events_map = {}
        from packages.orchestration.timeline import load_run_events
        from packages.orchestration.data_paths import resolve_data_root
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


class TestPatchRevert:
    """Snapshot-backed revert for applied patch intents."""

    def test_apply_stores_snapshot(self, tmp_path, monkeypatch):
        job, intent_id, repo = _make_job_with_intent(tmp_path, monkeypatch)
        from packages.orchestration.patch_apply import apply_patch_intent
        result = apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.state == "applied", f"blocked: {result.blocked_reason}"

        snap_dir = tmp_path / "workspaces" / str(job.id) / "patch_snapshots" / intent_id
        assert (snap_dir / "metadata.json").exists()

    def test_revert_restores_modified_file(self, tmp_path, monkeypatch):
        job, intent_id, repo = _make_job_with_intent(tmp_path, monkeypatch)
        target = repo / "notes.md"
        original = target.read_text()

        from packages.orchestration.patch_apply import apply_patch_intent
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert target.read_text() != original

        from packages.orchestration.patch_revert import revert_patch_intent
        # Reload job since apply_patch_intent saved it
        from packages.orchestration.storage import load_job
        job = load_job(job.id)
        result = revert_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.state == "reverted"
        assert target.read_text() == original

    def test_revert_deletes_created_file(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.approval_queue import APPROVAL_APPROVED, make_intent_id, set_approval_state
        from packages.orchestration.permissions import Capability, set_permission

        repo = tmp_path / "repo"
        repo.mkdir()

        art_id = uuid4()
        intent_id = make_intent_id(art_id, 0)
        artifact = Artifact(
            id=art_id, kind=ArtifactKind.BUILDER_PROPOSAL, name="create patch",
            content="Summary:\nCreate file\nProposed Changes:\n  - New content\nNotes:\nNone",
            metadata={
                "patch_intent_explanations": [{
                    "file": "new_file.md", "action": "create",
                    "risk": "low", "reason": "test", "summary": "test",
                }],
            },
        )
        job = Job(
            id=uuid4(), name="create job", user_prompt="create",
            state=RunState.RUNNING, tasks=[], artifacts=[artifact],
            metadata={"target_repo": str(repo)},
        )
        set_approval_state(job, intent_id, APPROVAL_APPROVED)
        set_permission(job, Capability.repo_generated_write, allow=True)
        save_job(job)

        from packages.orchestration.patch_apply import apply_patch_intent
        apply_patch_intent(job, intent_id, data_dir=tmp_path)
        assert (repo / "new_file.md").exists()

        from packages.orchestration.patch_revert import revert_patch_intent
        from packages.orchestration.storage import load_job
        job = load_job(job.id)
        result = revert_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.state == "reverted"
        assert not (repo / "new_file.md").exists()

    def test_second_revert_noop(self, tmp_path, monkeypatch):
        job, intent_id, repo = _make_job_with_intent(tmp_path, monkeypatch)

        from packages.orchestration.patch_apply import apply_patch_intent
        apply_patch_intent(job, intent_id, data_dir=tmp_path)

        from packages.orchestration.patch_revert import revert_patch_intent
        from packages.orchestration.storage import load_job
        job = load_job(job.id)
        revert_patch_intent(job, intent_id, data_dir=tmp_path)

        job = load_job(job.id)
        result2 = revert_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result2.state == "noop"
        assert result2.outcome == "already_reverted"

    def test_blocked_if_snapshot_missing(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job, intent_id, repo = _make_job_with_intent(tmp_path, monkeypatch)
        # Don't apply — no snapshot exists
        from packages.orchestration.patch_revert import revert_patch_intent
        result = revert_patch_intent(job, intent_id, data_dir=tmp_path)
        assert result.state == "blocked"
        assert result.blocked_reason == "snapshot_missing"

    def test_run_log_exact_schema(self, tmp_path, monkeypatch):
        job, intent_id, repo = _make_job_with_intent(tmp_path, monkeypatch)

        from packages.orchestration.patch_apply import apply_patch_intent
        apply_patch_intent(job, intent_id, data_dir=tmp_path)

        from packages.orchestration.patch_revert import revert_patch_intent
        from packages.orchestration.storage import load_job
        job = load_job(job.id)
        revert_patch_intent(job, intent_id, data_dir=tmp_path)

        from packages.orchestration.timeline import load_run_events
        events = load_run_events(tmp_path, job.id)
        revert_events = [e for e in events if e.get("event") == "patch_intent_reverted"]
        assert len(revert_events) >= 1
        meta = revert_events[0]["metadata"]
        required_keys = {
            "intent_id", "target_path", "action", "outcome",
            "existed_before", "bytes_written", "line_count",
            "before_sha256", "after_sha256",
        }
        assert required_keys <= set(meta.keys())

    def test_brain_has_patch_revert_node(self, tmp_path, monkeypatch):
        job, intent_id, repo = _make_job_with_intent(tmp_path, monkeypatch)

        from packages.orchestration.patch_apply import apply_patch_intent
        apply_patch_intent(job, intent_id, data_dir=tmp_path)

        from packages.orchestration.patch_revert import revert_patch_intent
        from packages.orchestration.storage import load_job
        job = load_job(job.id)
        revert_patch_intent(job, intent_id, data_dir=tmp_path)

        from packages.orchestration.timeline import load_run_events
        events = load_run_events(tmp_path, job.id)

        from packages.orchestration.project_brain import NT_PATCH_REVERT, build_project_brain
        graph = build_project_brain(job, events)
        types = {n.type for n in graph.nodes}
        assert NT_PATCH_REVERT in types

    def test_no_raw_content_in_revert_event(self, tmp_path, monkeypatch):
        job, intent_id, repo = _make_job_with_intent(tmp_path, monkeypatch)

        from packages.orchestration.patch_apply import apply_patch_intent
        apply_patch_intent(job, intent_id, data_dir=tmp_path)

        from packages.orchestration.patch_revert import revert_patch_intent
        from packages.orchestration.storage import load_job
        job = load_job(job.id)
        revert_patch_intent(job, intent_id, data_dir=tmp_path)

        from packages.orchestration.timeline import load_run_events
        events = load_run_events(tmp_path, job.id)
        for ev in events:
            if ev.get("event") == "patch_intent_reverted":
                meta_str = json.dumps(ev["metadata"])
                assert "Original content" not in meta_str


# ===========================================================================
# Step 55: Change Set
# ===========================================================================


class TestChangeSet:
    """Change Set / Review Board v0."""

    def test_derive_change_set(self, tmp_path, monkeypatch):
        job, intent_id, repo = _make_job_with_intent(tmp_path, monkeypatch)

        from packages.orchestration.change_set import derive_change_set
        changes = derive_change_set(job, [])
        assert len(changes) == 1
        assert changes[0].intent_id == intent_id
        assert changes[0].target_path == "notes.md"
        assert changes[0].status == "approved"

    def test_change_list_json_schema(self, tmp_path, monkeypatch):
        job, intent_id, repo = _make_job_with_intent(tmp_path, monkeypatch)

        from packages.orchestration.change_set import derive_change_set, export_change_list_json
        changes = derive_change_set(job, [])
        exported = export_change_list_json(str(job.id), changes)
        assert exported["version"] == 1
        assert "job_id" in exported
        assert "changes" in exported
        assert len(exported["changes"]) == 1

    def test_change_show_json_schema(self, tmp_path, monkeypatch):
        job, intent_id, repo = _make_job_with_intent(tmp_path, monkeypatch)

        from packages.orchestration.change_set import derive_change_set, export_change_show_json
        changes = derive_change_set(job, [])
        exported = export_change_show_json(str(job.id), changes[0])
        required = {"version", "job_id", "intent_id", "status", "target_path",
                     "risk", "approval", "apply", "proof", "test", "revert", "memory"}
        assert required <= set(exported.keys())

    def test_change_text_safe(self, tmp_path, monkeypatch):
        job, intent_id, repo = _make_job_with_intent(tmp_path, monkeypatch)

        from packages.orchestration.change_set import derive_change_set, summarize_change_list
        changes = derive_change_set(job, [])
        text = summarize_change_list(changes)
        assert intent_id in text
        assert "notes.md" in text

    def test_brain_has_change_set_node(self, tmp_path, monkeypatch):
        job, intent_id, repo = _make_job_with_intent(tmp_path, monkeypatch)

        from packages.orchestration.project_brain import NT_CHANGE_SET, build_project_brain
        graph = build_project_brain(job, [])
        types = {n.type for n in graph.nodes}
        assert NT_CHANGE_SET in types

    def test_no_raw_content_in_change_set(self, tmp_path, monkeypatch):
        job, intent_id, repo = _make_job_with_intent(tmp_path, monkeypatch)

        from packages.orchestration.change_set import derive_change_set, export_change_show_json
        changes = derive_change_set(job, [])
        exported = export_change_show_json(str(job.id), changes[0])
        exported_str = json.dumps(exported)
        assert "Original content" not in exported_str
        assert "Added line" not in exported_str


# ===========================================================================
# Step 56: Token Economy
# ===========================================================================


class TestTokenEconomy:
    """Token Economy v1 — context pack modes, worker recommend."""

    def test_context_pack_caveman_smaller_than_compact(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)

        from packages.orchestration.context_pack import build_context_pack
        caveman = build_context_pack(job, [], budget=10000, mode="caveman")
        compact = build_context_pack(job, [], budget=10000, mode="compact")
        standard = build_context_pack(job, [], budget=10000, mode="standard")
        assert caveman.estimated_tokens <= compact.estimated_tokens
        assert compact.estimated_tokens <= standard.estimated_tokens

    def test_context_pack_standard_mode(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)

        from packages.orchestration.context_pack import build_context_pack
        pack = build_context_pack(job, [], budget=10000, mode="standard")
        assert pack.mode == "standard"

    def test_caveman_no_long_prose(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)

        from packages.orchestration.context_pack import build_context_pack
        pack = build_context_pack(job, [], budget=10000, mode="caveman")
        for s in pack.sections:
            # Caveman sections should be short fragments
            lines = s.content.split("\n")
            for line in lines:
                assert len(line) < 200, f"Caveman line too long: {line[:50]}..."

    def test_worker_recommend_json_schema(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)

        from packages.orchestration.worker_recommend import (
            export_worker_recommendation_json,
            recommend_worker,
        )
        rec = recommend_worker(job, [])
        exported = export_worker_recommendation_json(rec)
        required = {
            "version", "job_id", "recommended_worker", "reason",
            "token_mode", "estimated_context_tokens",
            "requires_approval", "candidates",
        }
        assert required <= set(exported.keys())
        assert exported["version"] == 1

    def test_worker_recommend_local_first(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)

        from packages.orchestration.worker_recommend import recommend_worker
        rec = recommend_worker(job, [])
        assert rec.recommended_worker == "ollama"  # local-first
        assert not rec.requires_approval

    def test_token_policy_json_has_all_fields(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)

        from packages.orchestration.token_policy import (
            build_default_token_policy,
            export_token_policy_json,
        )
        policy = build_default_token_policy(job)
        exported = export_token_policy_json(policy)
        required = {
            "version", "job_id", "scope", "zero_token_steps",
            "local_first_steps", "expensive_model_steps",
            "forbidden_context", "compaction_rules", "budget",
        }
        assert required <= set(exported.keys())

    def test_all_modes_obey_redaction(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)

        from packages.orchestration.context_pack import build_context_pack, export_context_pack_json
        for mode in ("caveman", "compact", "standard"):
            pack = build_context_pack(job, [], budget=10000, mode=mode)
            exported = export_context_pack_json(pack)
            exported_str = json.dumps(exported)
            for forbidden in ("api_key", "password", "secret", "credential"):
                assert forbidden not in exported_str.lower() or mode in exported_str

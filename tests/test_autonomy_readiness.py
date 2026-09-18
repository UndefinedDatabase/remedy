"""Tests for autonomy readiness v0 (Step 48)."""

from __future__ import annotations

import json

from packages.core.models import RunState
from packages.orchestration.autonomy_readiness import (
    LEVELS,
    assess_job_readiness,
    assess_project_readiness,
    export_readiness_json,
    summarize_readiness,
)
from packages.orchestration.data_paths import mint_job_id
from packages.orchestration.pingpong_job import JobPlan, TaskEntry


def _make_job(**extra_meta) -> JobPlan:
    return JobPlan(
        job_id=mint_job_id(),
        job_title="readiness-test",
        user_prompt="test readiness",
        tasks=[TaskEntry(title="t", status=RunState.PENDING)],
        metadata=extra_meta,
    )


class TestReadinessBasic:
    def test_empty_events_returns_report(self):
        job = _make_job()
        report = assess_job_readiness(job, [])
        assert report.version == 2
        assert report.scope == "job"
        assert len(report.levels) == len(LEVELS)

    def test_level_0_always_eligible(self):
        job = _make_job()
        report = assess_job_readiness(job, [])
        assert report.levels[0].eligible is True

    def test_level_1_eligible_with_repo_and_tasks(self):
        job = _make_job(target_repo="/tmp/test")
        report = assess_job_readiness(job, [])
        assert report.levels[1].eligible is True

    def test_level_1_not_eligible_without_repo(self):
        job = JobPlan(
            job_id=mint_job_id(), job_title="no-repo", user_prompt="test",
            tasks=[TaskEntry(title="t", status=RunState.PENDING)],
        )
        report = assess_job_readiness(job, [])
        assert report.levels[1].eligible is False
        assert "attached_repo" in report.levels[1].missing_signals

    def test_level_5_missing_signals(self):
        job = _make_job()
        report = assess_job_readiness(job, [])
        assert report.levels[5].eligible is False
        assert "verified_snapshot" in report.levels[5].missing_signals

    def test_level_6_blocked(self):
        job = _make_job()
        report = assess_job_readiness(job, [])
        assert report.levels[6].eligible is False
        assert "mcp_not_connected" in report.levels[6].blockers

    def test_highest_eligible_level(self):
        job = _make_job(target_repo="/tmp/test")
        report = assess_job_readiness(job, [])
        assert report.highest_eligible_level >= 1

    def test_next_actions_populated(self):
        job = _make_job()
        report = assess_job_readiness(job, [])
        # Should have next_actions for first non-eligible level
        assert report.next_actions is not None


class TestReadinessJSON:
    def test_json_schema(self):
        job = _make_job()
        report = assess_job_readiness(job, [])
        data = export_readiness_json(report)
        assert data["version"] == 2
        assert data["scope"] == "job"
        assert "highest_eligible_level" in data
        assert "levels" in data
        assert "next_actions" in data
        assert "eligible_levels" in data
        assert "blocked_levels" in data
        assert "signals" in data
        assert len(data["levels"]) == len(LEVELS)

    def test_json_level_fields(self):
        job = _make_job()
        report = assess_job_readiness(job, [])
        data = export_readiness_json(report)
        for level_data in data["levels"]:
            assert "level" in level_data
            assert "name" in level_data
            assert "eligible" in level_data
            assert "present_signals" in level_data
            assert "missing_signals" in level_data
            assert "blockers" in level_data
            assert "next_actions" in level_data

    def test_no_raw_leak(self):
        job = _make_job()
        report = assess_job_readiness(job, [])
        full = json.dumps(export_readiness_json(report))
        for forbidden in ("stdout", "stderr", "raw_output", "command_output",
                          "Traceback", "diff_preview", "approval_reason"):
            assert forbidden not in full

    def test_json_is_pure_json(self):
        job = _make_job()
        report = assess_job_readiness(job, [])
        raw = json.dumps(export_readiness_json(report))
        json.loads(raw)  # must not raise


class TestReadinessText:
    def test_summarize_mentions_level(self):
        job = _make_job()
        report = assess_job_readiness(job, [])
        text = summarize_readiness(report)
        assert "Level 0" in text
        assert "observe" in text

    def test_summarize_mentions_missing(self):
        job = _make_job()
        report = assess_job_readiness(job, [])
        text = summarize_readiness(report)
        assert "missing" in text or "blockers" in text


class TestProjectReadiness:
    def test_empty_project(self):
        report = assess_project_readiness("proj1", [], {})
        assert report.scope == "project"
        assert report.highest_eligible_level == 0

    def test_project_aggregates_jobs(self):
        j1 = _make_job(target_repo="/tmp/r1")
        j2 = _make_job()
        report = assess_project_readiness("proj2", [j1, j2], {})
        # Level 1 should be eligible because j1 has repo+tasks
        assert report.levels[1].eligible is True


class TestReadinessBrainNode:
    def test_brain_has_readiness_node(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.pingpong_job import save_job_plan
        from packages.orchestration.project_brain import build_project_brain
        job = JobPlan(
            job_id=mint_job_id(), job_title="brain-test", user_prompt="test",
            tasks=[TaskEntry(title="t", status=RunState.PENDING)],
        )
        save_job_plan(job)
        graph = build_project_brain(job, [])
        types = {n.type for n in graph.nodes}
        assert "autonomy_readiness" in types

    def test_readiness_node_safe_metadata(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.pingpong_job import save_job_plan
        from packages.orchestration.project_brain import build_project_brain
        job = JobPlan(
            job_id=mint_job_id(), job_title="brain-test", user_prompt="test",
            tasks=[TaskEntry(title="t", status=RunState.PENDING)],
        )
        save_job_plan(job)
        graph = build_project_brain(job, [])
        ar_nodes = [n for n in graph.nodes if n.type == "autonomy_readiness"]
        assert ar_nodes
        meta = ar_nodes[0].metadata
        assert "highest_eligible_level" in meta
        assert "missing_count" in meta
        for forbidden in ("stdout", "stderr", "raw_output", "value"):
            assert forbidden not in meta


class TestVerifiedSnapshotSignal:
    """_has_verified_snapshot requires durable snapshot truth — no event/metadata
    fallback (Step 1159). A generic event or artifact metadata alone is not proof.
    """

    @staticmethod
    def _durable_verified(data_dir, repo_root, job_id, *, state="applied"):
        from packages.orchestration.repository_snapshot import (
            DurableApplyRecord,
            create_snapshot,
            save_durable_apply_record,
            verify_snapshot,
        )
        (repo_root / "f.py").write_text("before\n")
        snap = create_snapshot(job_id, "intent-x", ["f.py"], repo_root, data_dir)
        verify_snapshot(snap.snapshot_id, job_id, data_dir)
        rec = DurableApplyRecord(
            apply_id="apply-x", job_id=job_id, intent_id="intent-x",
            snapshot_id=snap.snapshot_id, state=state, target_paths=["f.py"],
            applied_at="2026-06-12T10:00:00+00:00",
            before_proof={}, after_proof={}, snapshot_verified=True,
        )
        save_durable_apply_record(rec, job_id, data_dir)
        return snap.snapshot_id

    def test_event_only_not_ready(self, tmp_path):
        from packages.orchestration.autonomy_readiness import _has_verified_snapshot
        job = _make_job()
        # A generic snapshot_create_completed event is NOT proof.
        assert _has_verified_snapshot(job, tmp_path) is False

    def test_artifact_metadata_only_not_ready(self, tmp_path):
        from packages.core.models import Artifact, ArtifactKind
        from packages.orchestration.approval_queue import make_intent_id
        from packages.orchestration.autonomy_readiness import _has_verified_snapshot
        art = Artifact(name="p", content="", kind=ArtifactKind.PATCH_INTENT)
        iid = make_intent_id(art.id, 0)
        art.metadata["patch_intent_apply_records"] = {iid: {"snapshot_verified": True}}
        job = _make_job()
        job.artifacts.append(art)
        # Metadata claims verified, but no durable record/snapshot exists.
        assert _has_verified_snapshot(job, tmp_path) is False

    def test_verified_durable_snapshot_true(self, tmp_path):
        from packages.orchestration.autonomy_readiness import _has_verified_snapshot
        data_dir = tmp_path / "data"; data_dir.mkdir()
        repo = tmp_path / "repo"; repo.mkdir()
        job = _make_job()
        self._durable_verified(data_dir, repo, str(job.job_id))
        assert _has_verified_snapshot(job, data_dir) is True

    def test_missing_blob_false(self, tmp_path):
        from packages.orchestration.autonomy_readiness import _has_verified_snapshot
        from packages.orchestration.repository_snapshot import _snapshot_dir
        data_dir = tmp_path / "data"; data_dir.mkdir()
        repo = tmp_path / "repo"; repo.mkdir()
        job = _make_job()
        sid = self._durable_verified(data_dir, repo, str(job.job_id))
        for b in _snapshot_dir(str(job.job_id), sid, data_dir).glob("blob_*.bin"):
            b.unlink()
        assert _has_verified_snapshot(job, data_dir) is False

    def test_tampered_manifest_false(self, tmp_path):
        from packages.orchestration.autonomy_readiness import _has_verified_snapshot
        from packages.orchestration.repository_snapshot import _snapshot_dir
        data_dir = tmp_path / "data"; data_dir.mkdir()
        repo = tmp_path / "repo"; repo.mkdir()
        job = _make_job()
        sid = self._durable_verified(data_dir, repo, str(job.job_id))
        manifest = _snapshot_dir(str(job.job_id), sid, data_dir) / "manifest.json"
        d = json.loads(manifest.read_text()); d["path_count"] = 999
        manifest.write_text(json.dumps(d, indent=2, sort_keys=True))
        assert _has_verified_snapshot(job, data_dir) is False

    def test_reverted_apply_not_ready(self, tmp_path):
        from packages.orchestration.autonomy_readiness import _has_verified_snapshot
        data_dir = tmp_path / "data"; data_dir.mkdir()
        repo = tmp_path / "repo"; repo.mkdir()
        job = _make_job()
        self._durable_verified(data_dir, repo, str(job.job_id), state="reverted")
        # Reverted apply is not "currently applied" → not revert-capable readiness.
        assert _has_verified_snapshot(job, data_dir) is False

    def test_level5_eligible_with_durable_verified_snapshot(self, tmp_path):
        """Level 5 (revert_capable) eligible only with durable verified snapshot."""
        data_dir = tmp_path / "data"; data_dir.mkdir()
        repo = tmp_path / "repo"; repo.mkdir()
        job = _make_job(
            target_repo="/tmp/test",
            permissions={"repo_generated_write": "allow", "repo_test_run": "allow"},
        )
        self._durable_verified(data_dir, repo, str(job.job_id))
        events = [
            {"event": "patch_apply_proof_recorded", "metadata": {}},
            {"event": "test_run_completed", "metadata": {}},
        ]
        report = assess_job_readiness(job, events, data_dir=data_dir)
        assert "verified_snapshot" in report.levels[5].present_signals


class TestAttachRepoTip:
    """R-0811: the readiness tip names the real job and a real path, never a placeholder."""

    @staticmethod
    def _rendered_tip(job) -> str:
        text = summarize_readiness(assess_job_readiness(job, []))
        [line] = [ln for ln in text.splitlines() if "attach-repo" in ln]
        return line

    def test_the_tip_names_the_job_and_its_projects_repository(self, tmp_path, monkeypatch):
        import re

        from packages.orchestration.project_registry import RemyProject, save_project

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        repo = tmp_path / "the-repo"
        repo.mkdir()
        project = RemyProject(name="the-repo", canonical_repo_path=str(repo))
        save_project(project)
        job = _make_job(project_id=str(project.id))

        line = self._rendered_tip(job)

        assert line.endswith(f"remedy job attach-repo {job.job_id} {repo}")
        assert not re.search(r"<[a-z_]+>", line)

    def test_the_tip_without_a_project_says_what_to_pass(self, tmp_path, monkeypatch):
        import re

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        job = _make_job()

        line = self._rendered_tip(job)

        assert f"remedy job attach-repo {job.job_id} " in line
        assert "path of the repository" in line
        assert not re.search(r"<[a-z_]+>", line)

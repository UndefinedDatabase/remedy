"""Tests for Step 61 — Brain Correctness Lock.

Multi-proof causal edges, file why chain, continue roundtrip,
project aggregate integrity, no raw content leaks.
"""

from __future__ import annotations

import json
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from packages.core.models import Artifact, ArtifactKind, Job, RunState, Task
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
        name="step61-test",
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


def _proof_event(intent_id: str, target_path: str) -> dict:
    return {
        "event": "patch_apply_proof_recorded",
        "outcome": "proof_stored",
        "metadata": {
            "intent_id": intent_id,
            "target_path": target_path,
            "sha256": f"sha_{intent_id}",
            "bytes_written": 100,
            "line_count": 10,
        },
    }


def _test_event(status: str = "passed", exit_code: int = 0) -> dict:
    return {
        "event": "test_run_completed",
        "outcome": status,
        "metadata": {
            "command": "pytest",
            "status": status,
            "exit_code": exit_code,
        },
    }


FORBIDDEN_KEYS = (
    "stdout", "stderr", "raw_output", "command_output",
    "Traceback", "diff_preview", "approval_reason",
)


# ===========================================================================
# Multi-proof causal edge correctness
# ===========================================================================


class TestMultiProofCausalEdges:
    """Proof[i] → test[i] chronological pairing, not last→last."""

    def test_three_proof_three_test_pairing(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain import (
            ET_PROOF_VERIFIED_BY,
            build_project_brain,
        )

        job = _make_job()
        save_job(job)

        events = [
            _proof_event("i1", "a.py"),
            _test_event(),
            _proof_event("i2", "b.py"),
            _test_event(),
            _proof_event("i3", "c.py"),
            _test_event(),
        ]

        graph = build_project_brain(job, events)
        pv_edges = [e for e in graph.edges if e.type == ET_PROOF_VERIFIED_BY]
        assert len(pv_edges) == 3

        # Each proof should connect to its own test, not all to last
        sources = [e.source for e in pv_edges]
        targets = [e.target for e in pv_edges]
        assert len(set(sources)) == 3, "Each proof should have unique source"
        assert len(set(targets)) == 3, "Each test should have unique target"

    def test_more_proofs_than_tests(self, tmp_path, monkeypatch):
        """Extra proofs beyond test count have no test edge."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain import (
            ET_PROOF_VERIFIED_BY,
            build_project_brain,
        )

        job = _make_job()
        save_job(job)

        events = [
            _proof_event("i1", "a.py"),
            _proof_event("i2", "b.py"),
            _test_event(),
        ]

        graph = build_project_brain(job, events)
        pv_edges = [e for e in graph.edges if e.type == ET_PROOF_VERIFIED_BY]
        # At most 1 edge (first proof → first test)
        assert len(pv_edges) == 1

    def test_proof_recorded_edge_exists(self, tmp_path, monkeypatch):
        """patch_apply → proof has recorded_proof edge."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain import (
            ET_RECORDED_PROOF,
            build_project_brain,
        )

        job = _make_job()
        # Need an artifact with apply records to get apply nodes
        art = Artifact(
            id=uuid4(), name="test-art", kind=ArtifactKind.PATCH_INTENT,
            content="",
            metadata={
                "patch_intent_apply_records": {
                    "i1": {"state": "applied", "bytes_written": 50, "line_count": 5}
                }
            },
        )
        job.artifacts.append(art)
        save_job(job)

        events = [_proof_event("i1", "a.py")]
        graph = build_project_brain(job, events)
        rp_edges = [e for e in graph.edges if e.type == ET_RECORDED_PROOF]
        assert len(rp_edges) >= 1
        assert any("apply:i1" in e.source for e in rp_edges)


# ===========================================================================
# File provenance (file why) chain correctness
# ===========================================================================


class TestFileProvenanceChain:
    """file_provenance builds correct causal chain."""

    def test_full_chain_order(self, tmp_path, monkeypatch):
        """Chain follows: patch_intent → approval → apply → proof → test_run."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.approval_queue import make_intent_id
        from packages.orchestration.file_provenance import build_file_provenance

        job = _make_job()
        art_id = uuid4()
        intent_id = make_intent_id(art_id, 0)

        art = Artifact(
            id=art_id, name="test-art", kind=ArtifactKind.PATCH_INTENT,
            content="",
            metadata={
                "patch_intent_explanations": [
                    {
                        "file": "src/foo.py",
                        "action": "modify",
                        "risk": "low",
                        "reason": "test",
                        "summary": "test intent",
                    }
                ],
                "patch_intent_approvals": {
                    intent_id: {
                        "state": "approved",
                        "decided_at": "2026-01-01",
                        "decided_by": "user",
                    }
                },
                "patch_intent_apply_records": {
                    intent_id: {"state": "applied", "bytes_written": 100, "line_count": 10}
                },
            },
        )
        job.artifacts.append(art)
        save_job(job)

        events = [
            _proof_event(intent_id, "src/foo.py"),
            _test_event(),
        ]

        prov = build_file_provenance(job, events, "src/foo.py")
        assert prov.found is True
        steps = [link.step for link in prov.chain]
        assert steps == [
            "patch_intent", "approval_decision", "patch_apply",
            "patch_apply_proof", "test_run",
        ]

    def test_no_match_returns_not_found(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.file_provenance import build_file_provenance

        job = _make_job()
        save_job(job)
        prov = build_file_provenance(job, [], "nonexistent.py")
        assert prov.found is False
        assert len(prov.chain) == 0

    def test_provenance_json_no_raw_leaks(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.approval_queue import make_intent_id
        from packages.orchestration.file_provenance import (
            build_file_provenance,
            export_file_provenance_json,
        )

        job = _make_job()
        art_id = uuid4()
        intent_id = make_intent_id(art_id, 0)
        art = Artifact(
            id=art_id, name="test-art", kind=ArtifactKind.PATCH_INTENT,
            content="",
            metadata={
                "patch_intent_explanations": [
                    {
                        "file": "x.py",
                        "action": "modify",
                        "risk": "low",
                        "reason": "test",
                        "summary": "test",
                    }
                ],
                "patch_intent_approvals": {
                    intent_id: {"state": "approved"}
                },
            },
        )
        job.artifacts.append(art)
        save_job(job)

        prov = build_file_provenance(job, [_proof_event(intent_id, "x.py")], "x.py")
        raw = json.dumps(export_file_provenance_json(prov))
        for forbidden in FORBIDDEN_KEYS:
            assert forbidden not in raw, f"Raw leak: {forbidden}"


# ===========================================================================
# Continue roundtrip + project aggregate integrity
# ===========================================================================


class TestContinueRoundtripAggregate:
    """Parent → child continue-from-node, aggregate includes both."""

    def test_aggregate_includes_parent_and_child(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.continue_from_node import continue_from_node
        from packages.orchestration.data_paths import resolve_data_root
        from packages.orchestration.project_brain import build_project_brain
        from packages.orchestration.project_brain_aggregate import (
            build_project_brain_aggregate,
        )
        from packages.orchestration.project_registry import (
            RemyProject,
            save_project,
        )
        from packages.orchestration.storage import load_job
        from packages.orchestration.timeline import load_run_events

        pid = str(uuid4())
        project = RemyProject(id=UUID(pid), name="test-project", repo_paths=[str(tmp_path)])
        save_project(project)

        parent = _make_job(project_id=pid, target_repo=str(tmp_path))
        save_job(parent)

        # Build parent brain, continue from first node
        parent_graph = build_project_brain(parent, [])
        result = continue_from_node(parent, parent_graph, parent_graph.nodes[0].id, "child task")

        child = load_job(UUID(result.child_job_id))

        # Load events for both jobs
        data_root = resolve_data_root()
        parent_events = load_run_events(data_root, parent.id)
        child_events = load_run_events(data_root, child.id)

        all_events = {
            str(parent.id): parent_events,
            str(child.id): child_events,
        }

        # Attach child to project
        project.job_ids.append(str(child.id))
        if str(parent.id) not in project.job_ids:
            project.job_ids.append(str(parent.id))

        agg = build_project_brain_aggregate(
            project, [parent, child], all_events,
        )

        # Aggregate must include nodes from both jobs
        job_node_ids = [n.id for n in agg.nodes if n.type == "job"]
        assert str(parent.id) in job_node_ids
        assert str(child.id) in job_node_ids

        # Must have continuation edge
        cont_edges = [e for e in agg.edges if e.type == "continued_as"]
        assert len(cont_edges) >= 1

        # Must have exactly 2 job subgraphs
        assert len(agg.job_graphs) == 2

    def test_aggregate_summary_counts(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain_aggregate import (
            build_project_brain_aggregate,
        )
        from packages.orchestration.project_registry import (
            RemyProject,
            save_project,
        )

        pid = str(uuid4())
        project = RemyProject(id=UUID(pid), name="count-test", repo_paths=[])
        save_project(project)

        j1 = _make_job(project_id=pid)
        j2 = _make_job(project_id=pid)
        save_job(j1)
        save_job(j2)

        agg = build_project_brain_aggregate(project, [j1, j2], {})
        assert agg.summary["job_count"] == 2
        assert agg.summary["node_count"] > 0
        assert agg.summary["edge_count"] > 0


# ===========================================================================
# No raw content leaks in brain/aggregate outputs
# ===========================================================================


class TestNoRawLeaks:
    """No raw content surfaces in brain graph, aggregate, or provenance."""

    def test_brain_json_no_raw_leaks(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain import (
            build_project_brain,
            export_project_brain_json,
        )

        job = _make_job()
        save_job(job)
        events = [_proof_event("i1", "a.py"), _test_event()]
        graph = build_project_brain(job, events)
        raw = json.dumps(export_project_brain_json(graph))
        for forbidden in FORBIDDEN_KEYS:
            assert forbidden not in raw, f"Brain JSON leak: {forbidden}"

    def test_brain_summary_no_raw_leaks(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain import (
            build_project_brain,
            summarize_project_brain,
        )

        job = _make_job()
        save_job(job)
        graph = build_project_brain(job, [])
        text = summarize_project_brain(graph)
        for forbidden in FORBIDDEN_KEYS:
            assert forbidden not in text, f"Brain summary leak: {forbidden}"

    def test_aggregate_json_no_raw_leaks(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain_aggregate import (
            build_project_brain_aggregate,
            export_project_brain_aggregate_json,
        )
        from packages.orchestration.project_registry import (
            RemyProject,
            save_project,
        )

        pid = str(uuid4())
        project = RemyProject(id=UUID(pid), name="leak-test", repo_paths=[])
        save_project(project)

        job = _make_job(project_id=pid)
        save_job(job)

        agg = build_project_brain_aggregate(project, [job], {})
        raw = json.dumps(export_project_brain_aggregate_json(agg))
        for forbidden in FORBIDDEN_KEYS:
            assert forbidden not in raw, f"Aggregate JSON leak: {forbidden}"

    def test_readiness_brain_node_no_raw_leaks(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain import build_project_brain

        job = _make_job()
        save_job(job)
        graph = build_project_brain(job, [])
        ar_nodes = [n for n in graph.nodes if n.type == "autonomy_readiness"]
        assert ar_nodes
        meta = ar_nodes[0].metadata
        for forbidden in ("stdout", "stderr", "raw_output", "value"):
            assert forbidden not in meta, f"Readiness node leak: {forbidden}"

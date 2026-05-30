"""Tests for Step 63 — Evidence Memory v1.

Memory card model, card management, learn with evidence, brain nodes safe,
no raw leaks.
"""

from __future__ import annotations

import json
from uuid import uuid4

import pytest

from packages.memory.models import MemoryEntry


class TestMemoryCardModel:
    def test_new_fields_exist(self):
        e = MemoryEntry(key="k", value="v")
        assert e.summary == ""
        assert e.scope == "job"
        assert e.validity == "active"
        assert e.review_status == "proposed"
        assert e.updated_at is None
        assert e.supersedes is None
        assert e.contradicts is None
        assert e.evidence_refs == []

    def test_roundtrip(self):
        e = MemoryEntry(
            key="k", value="v", summary="test summary",
            scope="project", validity="stale", review_status="approved",
            evidence_refs=["ref1", "ref2"],
        )
        d = json.loads(e.to_json_line())
        e2 = MemoryEntry.from_dict(d)
        assert e2.summary == "test summary"
        assert e2.scope == "project"
        assert e2.validity == "stale"
        assert e2.review_status == "approved"
        assert e2.evidence_refs == ["ref1", "ref2"]

    def test_backward_compat_from_dict(self):
        """Old entries without new fields still deserialize."""
        d = {"id": str(uuid4()), "key": "old", "value": "v1"}
        e = MemoryEntry.from_dict(d)
        assert e.summary == ""
        assert e.validity == "active"
        assert e.evidence_refs == []


class TestCardManagement:
    def test_approve(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import (
            approve_memory_card,
            store_memory,
        )

        entry = store_memory("k1", "v1", job_id="j1")
        assert entry.approved is False
        result = approve_memory_card(str(entry.id), job_id="j1")
        assert result is not None
        assert result.approved is True
        assert result.review_status == "approved"

    def test_reject(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import (
            reject_memory_card,
            store_memory,
        )

        entry = store_memory("k2", "v2", job_id="j2")
        result = reject_memory_card(str(entry.id), job_id="j2")
        assert result is not None
        assert result.approved is False
        assert result.review_status == "rejected"

    def test_mark_stale(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import mark_stale, store_memory

        entry = store_memory("k3", "v3", job_id="j3")
        result = mark_stale(str(entry.id), job_id="j3")
        assert result is not None
        assert result.validity == "stale"

    def test_supersede(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import (
            store_memory,
            supersede_memory_card,
        )

        e1 = store_memory("k4", "old", job_id="j4")
        e2 = store_memory("k4", "new", job_id="j4")
        old, new = supersede_memory_card(str(e1.id), str(e2.id), job_id="j4")
        assert old is not None
        assert old.validity == "superseded"
        assert new is not None
        assert new.supersedes == str(e1.id)

    def test_contradict(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import (
            contradict_memory_card,
            store_memory,
        )

        e1 = store_memory("k5", "claim_a", job_id="j5")
        e2 = store_memory("k5", "claim_b", job_id="j5")
        contradicted, by = contradict_memory_card(str(e1.id), str(e2.id), job_id="j5")
        assert contradicted is not None
        assert contradicted.validity == "contradicted"
        assert contradicted.contradicts == str(e2.id)

    def test_get_card(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import get_memory_card, store_memory

        entry = store_memory("k6", "v6", job_id="j6")
        card = get_memory_card(str(entry.id), job_id="j6")
        assert card is not None
        assert card.key == "k6"

    def test_get_card_not_found(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import get_memory_card

        card = get_memory_card(str(uuid4()), job_id="nonexistent")
        assert card is None


class TestLearnEvidence:
    def test_learn_creates_entries(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.core.models import Job, RunState, Task
        from packages.orchestration.memory_learn import learn_from_job
        from packages.orchestration.storage import save_job

        job = Job(
            id=uuid4(), name="learn-test", user_prompt="test",
            tasks=[Task(description="t", status=RunState.COMPLETED)],
            metadata={"target_repo": "/tmp/test"},
        )
        save_job(job)
        events = [
            {"event": "test_run_completed", "metadata": {"command": "pytest", "status": "passed", "exit_code": 0}},
            {"event": "patch_apply_proof_recorded", "metadata": {"intent_id": "i1", "target_path": "a.py", "sha256": "aaa", "bytes_written": 10, "line_count": 5}},
        ]
        result = learn_from_job(job, events, approved=True)
        assert result.learned_count > 0


class TestBrainMemoryNodeSafe:
    def test_memory_node_has_evidence_fields(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.core.models import Job, RunState, Task
        from packages.memory.local_gateway import store_memory
        from packages.orchestration.project_brain import build_project_brain
        from packages.orchestration.storage import save_job

        job = Job(
            id=uuid4(), name="brain-mem", user_prompt="test",
            tasks=[Task(description="t", status=RunState.PENDING)],
        )
        save_job(job)
        store_memory("test.key", "test value", job_id=str(job.id), approved=True)
        graph = build_project_brain(job, [])

        mem_nodes = [n for n in graph.nodes if n.type == "memory"]
        assert len(mem_nodes) >= 1
        meta = mem_nodes[0].metadata
        assert "key" in meta
        assert "summary" in meta
        assert "validity" in meta
        assert "review_status" in meta
        assert "scope" in meta
        assert "evidence_refs_count" in meta
        # No raw leaks
        for forbidden in ("stdout", "stderr", "raw_output", "value"):
            assert forbidden not in meta


class TestMemoryCardCLI:
    def test_card_show_help(self):
        import subprocess
        import sys
        result = subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped", "memory", "card-show", "--help"],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0
        assert "memory_id" in result.stdout.lower()

    def test_card_approve_help(self):
        import subprocess
        import sys
        result = subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped", "memory", "card-approve", "--help"],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0

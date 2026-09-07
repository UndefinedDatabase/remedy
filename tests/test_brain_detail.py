"""
Tests for packages/orchestration/brain_detail.py and the `remedy brain node` CLI command.

Coverage:
  - BrainNodeDetail frozen model construction
  - build_brain_node_detail: job node
  - build_brain_node_detail: task node
  - build_brain_node_detail: artifact node (no content)
  - build_brain_node_detail: patch_intent node (pending)
  - build_brain_node_detail: patch_intent node (after approval)
  - build_brain_node_detail: approval_decision node (no approval_reason)
  - build_brain_node_detail: verification node
  - build_brain_node_detail: permission_blocker node
  - build_brain_node_detail: run_event node
  - build_brain_node_detail: agent_loop node
  - build_brain_node_detail: constitution node
  - build_brain_node_detail: memory_placeholder node
  - build_brain_node_detail: mcp_placeholder node
  - unknown node_id raises ValueError with safe message
  - connections: incoming and outgoing edges rendered
  - affected_files: target_path present for patch_intent
  - affected_files: repo_applied_files present for artifact
  - summarize output: header, node id, type, sections
  - export_brain_node_detail_json: correct top-level keys
  - export_brain_node_detail_json: JSON serialisable
  - run-log schema exact: node_id, node_type, connected_count, evidence_count
  - redaction: ARTIFACT_CONTENT_MUST_NOT_RENDER absent from summary
  - redaction: DIFF_PREVIEW_MUST_NOT_RENDER absent from summary
  - redaction: APPROVAL_REASON_MUST_NOT_RENDER absent from summary
  - redaction: EVENT_MESSAGE_MUST_NOT_RENDER absent from summary
  - redaction: RAW_COMMAND_OUTPUT_MUST_NOT_RENDER absent from summary
  - redaction: all sentinels absent from JSON export
  - redaction: all sentinels absent from run log
  - CLI: invalid UUID exits 1
  - CLI: unknown job exits 1
  - CLI: unknown node exits 1
  - CLI: valid job+node prints text detail
  - CLI: --json returns parseable JSON
  - CLI: --json top-level keys correct
  - CLI: exactly one run log file created
  - CLI: run-log event schema exact
"""

from __future__ import annotations

import json
from uuid import uuid4

import pytest

from packages.core.models import Artifact, ArtifactKind, Job, RunState, Task
from packages.orchestration.approval_queue import (
    APPROVAL_APPROVED,
    APPROVAL_REJECTED,
    make_intent_id,
    set_approval_state,
)
from packages.orchestration.brain_detail import (
    BrainNodeDetail,
    build_brain_node_detail,
    export_brain_node_detail_json,
    summarize_brain_node_detail,
)
from packages.orchestration.patch_intent import RISK_HIGH, RISK_LOW, RISK_MEDIUM
from packages.orchestration.project_brain import (
    NT_AGENT_LOOP,
    NT_APPROVAL,
    NT_ARTIFACT,
    NT_BLOCKER,
    NT_CONSTITUTION,
    NT_JOB,
    NT_MCP,
    NT_MEMORY,
    NT_MEMORY_ENTRY,
    NT_PATCH_INTENT,
    NT_RUN_EVENT,
    NT_TASK,
    NT_VERIFICATION,
    build_project_brain,
)
from packages.orchestration.storage import save_job

# ---------------------------------------------------------------------------
# Sentinels
# ---------------------------------------------------------------------------

ARTIFACT_CONTENT_MUST_NOT_RENDER   = "ARTIFACT_CONTENT_MUST_NOT_RENDER"
DIFF_PREVIEW_MUST_NOT_RENDER       = "DIFF_PREVIEW_MUST_NOT_RENDER"
APPROVAL_REASON_MUST_NOT_RENDER    = "APPROVAL_REASON_MUST_NOT_RENDER"
EVENT_MESSAGE_MUST_NOT_RENDER      = "EVENT_MESSAGE_MUST_NOT_RENDER"
RAW_COMMAND_OUTPUT_MUST_NOT_RENDER = "RAW_COMMAND_OUTPUT_MUST_NOT_RENDER"

_ALL_SENTINELS = [
    ARTIFACT_CONTENT_MUST_NOT_RENDER,
    DIFF_PREVIEW_MUST_NOT_RENDER,
    APPROVAL_REASON_MUST_NOT_RENDER,
    EVENT_MESSAGE_MUST_NOT_RENDER,
    RAW_COMMAND_OUTPUT_MUST_NOT_RENDER,
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_job(**kwargs) -> Job:
    defaults: dict = {"name": "Test detail job", "state": RunState.PENDING}
    defaults.update(kwargs)
    return Job(**defaults)


def _pending_task(**kwargs) -> Task:
    return Task(description="write docs", inputs={"task_type": "write_readme"}, **kwargs)


def _completed_task(**kwargs) -> Task:
    t = Task(description="task done", inputs={"task_type": "write_readme"}, **kwargs)
    t.status = RunState.COMPLETED
    return t


def _add_patch_artifact(
    job: Job,
    *,
    risk: str = RISK_MEDIUM,
    task_id=None,
    content: str = "some content",
) -> tuple[Artifact, str]:
    """Add a single patch-intent artifact to job. Returns (artifact, intent_id)."""
    task_id = task_id or uuid4()
    artifact = Artifact(
        name="builder proposal",
        content=content,
        kind=ArtifactKind.BUILDER_PROPOSAL,
        task_id=task_id,
        metadata={
            "patch_intent_explanations": [
                {
                    "file": "docs/README.md",
                    "action": "modify",
                    "risk": risk,
                    "reason": "task type 'write_readme'",
                    "summary": "Update README heading",
                }
            ]
        },
    )
    job.artifacts.append(artifact)
    return artifact, make_intent_id(artifact.id, 0)


def _build(job: Job, events=None, *, constitution=None) -> object:
    return build_project_brain(job, events or [], constitution=constitution)


def _task_completed_event(job_id: str, task_id: str) -> dict:
    return {
        "event": "task_run_completed",
        "job_id": job_id,
        "run_id": "r1",
        "timestamp": "2026-05-06T10:01:00+00:00",
        "task_id": task_id,
        "outcome": "pass",
        "metadata": {},
    }


def _perm_denied_event(job_id: str, task_id: str) -> dict:
    return {
        "event": "task_run_failed",
        "job_id": job_id,
        "run_id": "r1",
        "timestamp": "2026-05-06T10:00:00+00:00",
        "task_id": task_id,
        "outcome": "permission_denied",
        "metadata": {"capability": "workspace_write"},
    }


def _agent_loop_event(job_id: str) -> dict:
    return {
        "event": "agent_loop_inspected",
        "job_id": job_id,
        "run_id": "r1",
        "timestamp": "2026-05-06T10:02:00+00:00",
        "outcome": "inspected",
        "metadata": {
            "stage": "build",
            "decision": "continue",
            "cycle": 1,
            "max_cycles": 3,
            "pending_finding_count": 0,
        },
    }


# ---------------------------------------------------------------------------
# TestBrainNodeDetailModel
# ---------------------------------------------------------------------------


class TestBrainNodeDetailModel:
    def test_construction(self):
        d = BrainNodeDetail(
            job_id="abc",
            node_id="x",
            node_type=NT_JOB,
            title="Job",
            status="pending",
            risk=None,
            explanation="test",
            why_it_exists=("reason",),
            connected_to=({"direction": "outgoing", "edge_type": "has_task", "node_id": "y", "node_type": NT_TASK, "node_label": "task"},),
            evidence=("evidence",),
            affected_files=(),
            next_actions=(),
            redaction_notes=(),
        )
        assert d.job_id == "abc"
        assert d.node_type == NT_JOB
        assert d.connected_to[0]["direction"] == "outgoing"

    def test_frozen(self):
        d = BrainNodeDetail(
            job_id="abc", node_id="x", node_type=NT_JOB, title="Job",
            status="pending", risk=None, explanation="test",
            why_it_exists=(), connected_to=(), evidence=(),
            affected_files=(), next_actions=(), redaction_notes=(),
        )
        with pytest.raises((AttributeError, TypeError)):
            d.title = "other"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# TestBuildBrainNodeDetail
# ---------------------------------------------------------------------------


class TestBuildBrainNodeDetail:
    def test_unknown_node_raises(self):
        job = _make_job()
        graph = _build(job)
        with pytest.raises(ValueError, match="node not found"):
            build_brain_node_detail(job, graph, "nonexistent-node-id", [])

    def test_unknown_node_message_is_safe(self):
        job = _make_job()
        graph = _build(job)
        # Large/weird node_id should not crash, message should be truncated
        with pytest.raises(ValueError):
            build_brain_node_detail(job, graph, "x" * 200, [])

    # ── job node ─────────────────────────────────────────────────────────────

    def test_job_node_detail(self):
        job = _make_job(name="Fix the README")
        job.tasks.append(_pending_task())
        graph = _build(job)
        job_node = next(n for n in graph.nodes if n.type == NT_JOB)
        detail = build_brain_node_detail(job, graph, job_node.id, [])
        assert detail.node_type == NT_JOB
        assert detail.job_id == str(job.id)
        assert "Fix the README" in detail.explanation
        assert detail.status == "pending"

    def test_job_node_has_why_it_exists(self):
        job = _make_job()
        graph = _build(job)
        job_node = next(n for n in graph.nodes if n.type == NT_JOB)
        detail = build_brain_node_detail(job, graph, job_node.id, [])
        assert len(detail.why_it_exists) > 0

    def test_job_node_next_action_includes_trust_report(self):
        job = _make_job()
        graph = _build(job)
        job_node = next(n for n in graph.nodes if n.type == NT_JOB)
        detail = build_brain_node_detail(job, graph, job_node.id, [])
        assert any("brain trust" in a for a in detail.next_actions)

    # ── task node ────────────────────────────────────────────────────────────

    def test_task_node_detail(self):
        job = _make_job()
        task = _pending_task()
        job.tasks.append(task)
        graph = _build(job)
        task_node = next(n for n in graph.nodes if n.type == NT_TASK)
        detail = build_brain_node_detail(job, graph, task_node.id, [])
        assert detail.node_type == NT_TASK
        assert "write_readme" in detail.explanation
        assert detail.status == "pending"

    def test_task_node_affected_files_from_repo_applied(self):
        job = _make_job()
        task = _pending_task()
        job.tasks.append(task)
        artifact = Artifact(
            name="a",
            content="x",
            kind=ArtifactKind.BUILDER_PROPOSAL,
            task_id=task.id,
            metadata={"repo_applied_files": ["docs/README.md", "docs/API.md"]},
        )
        job.artifacts.append(artifact)
        graph = _build(job)
        task_node = next(n for n in graph.nodes if n.type == NT_TASK)
        detail = build_brain_node_detail(job, graph, task_node.id, [])
        assert "docs/README.md" in detail.affected_files
        assert "docs/API.md" in detail.affected_files

    # ── artifact node ────────────────────────────────────────────────────────

    def test_artifact_node_detail_no_content(self):
        job = _make_job()
        artifact = Artifact(
            name="planning output",
            content=ARTIFACT_CONTENT_MUST_NOT_RENDER,
            kind=ArtifactKind.PLANNING,
        )
        job.artifacts.append(artifact)
        graph = _build(job)
        art_node = next(n for n in graph.nodes if n.type == NT_ARTIFACT)
        detail = build_brain_node_detail(job, graph, art_node.id, [])
        assert detail.node_type == NT_ARTIFACT
        assert ARTIFACT_CONTENT_MUST_NOT_RENDER not in detail.explanation
        assert "planning" in detail.explanation

    def test_artifact_node_affected_files_from_metadata(self):
        job = _make_job()
        artifact = Artifact(
            name="a",
            content="x",
            kind=ArtifactKind.BUILDER_PROPOSAL,
            metadata={"repo_applied_files": ["src/main.py"]},
        )
        job.artifacts.append(artifact)
        graph = _build(job)
        art_node = next(n for n in graph.nodes if n.type == NT_ARTIFACT)
        detail = build_brain_node_detail(job, graph, art_node.id, [])
        assert "src/main.py" in detail.affected_files

    # ── patch_intent node ────────────────────────────────────────────────────

    def test_patch_intent_pending_detail(self):
        job = _make_job()
        _, intent_id = _add_patch_artifact(job, risk=RISK_MEDIUM)
        graph = _build(job)
        pi_node = next(n for n in graph.nodes if n.type == NT_PATCH_INTENT)
        detail = build_brain_node_detail(job, graph, pi_node.id, [])
        assert detail.node_type == NT_PATCH_INTENT
        assert "docs/README.md" in detail.explanation
        assert "modify" in detail.explanation
        assert RISK_MEDIUM in detail.explanation
        assert detail.status == "pending"
        assert "docs/README.md" in detail.affected_files

    def test_patch_intent_approved_detail(self):
        job = _make_job()
        _, intent_id = _add_patch_artifact(job, risk=RISK_HIGH)
        set_approval_state(job, intent_id, APPROVAL_APPROVED)
        graph = _build(job)
        pi_node = next(n for n in graph.nodes if n.type == NT_PATCH_INTENT)
        detail = build_brain_node_detail(job, graph, pi_node.id, [])
        assert detail.status == "approved"
        # approve/reject actions no longer offered
        assert not any("approve" in a for a in detail.next_actions)

    def test_patch_intent_pending_has_approval_action(self):
        job = _make_job()
        _, intent_id = _add_patch_artifact(job)
        graph = _build(job)
        pi_node = next(n for n in graph.nodes if n.type == NT_PATCH_INTENT)
        detail = build_brain_node_detail(job, graph, pi_node.id, [])
        assert any("patch approve" in a for a in detail.next_actions)

    # ── approval_decision node ───────────────────────────────────────────────

    def test_approval_decision_no_reason(self):
        job = _make_job()
        _, intent_id = _add_patch_artifact(job, risk=RISK_LOW)
        set_approval_state(job, intent_id, APPROVAL_APPROVED, reason=APPROVAL_REASON_MUST_NOT_RENDER)
        graph = _build(job)
        dec_node = next(n for n in graph.nodes if n.type == NT_APPROVAL)
        detail = build_brain_node_detail(job, graph, dec_node.id, [])
        assert detail.node_type == NT_APPROVAL
        assert APPROVAL_REASON_MUST_NOT_RENDER not in detail.explanation
        assert "approved" in detail.explanation

    def test_approval_decision_rejected(self):
        job = _make_job()
        _, intent_id = _add_patch_artifact(job, risk=RISK_MEDIUM)
        set_approval_state(job, intent_id, APPROVAL_REJECTED)
        graph = _build(job)
        dec_node = next(n for n in graph.nodes if n.type == NT_APPROVAL)
        detail = build_brain_node_detail(job, graph, dec_node.id, [])
        assert detail.status == "rejected"

    # ── verification node ────────────────────────────────────────────────────

    def test_verification_node_detail(self):
        job = _make_job()
        task = _completed_task()
        job.tasks.append(task)
        events = [_task_completed_event(str(job.id), str(task.id))]
        graph = _build(job, events)
        ver_node = next(n for n in graph.nodes if n.type == NT_VERIFICATION)
        detail = build_brain_node_detail(job, graph, ver_node.id, events)
        assert detail.node_type == NT_VERIFICATION
        assert detail.status == "passed"
        assert "passed" in detail.explanation

    # ── permission_blocker node ──────────────────────────────────────────────

    def test_blocker_node_detail(self):
        job = _make_job()
        task = _pending_task()
        job.tasks.append(task)
        events = [_perm_denied_event(str(job.id), str(task.id))]
        graph = _build(job, events)
        blk_node = next(n for n in graph.nodes if n.type == NT_BLOCKER)
        detail = build_brain_node_detail(job, graph, blk_node.id, events)
        assert detail.node_type == NT_BLOCKER
        assert "workspace_write" in detail.explanation
        assert any("job permit" in a for a in detail.next_actions)

    def test_blocker_next_action_has_capability(self):
        job = _make_job()
        task = _pending_task()
        job.tasks.append(task)
        events = [_perm_denied_event(str(job.id), str(task.id))]
        graph = _build(job, events)
        blk_node = next(n for n in graph.nodes if n.type == NT_BLOCKER)
        detail = build_brain_node_detail(job, graph, blk_node.id, events)
        assert any("workspace_write" in a for a in detail.next_actions)

    # ── run_event node ───────────────────────────────────────────────────────

    def test_run_event_node_detail(self):
        job = _make_job()
        events = [{
            "event": "job_created",
            "job_id": str(job.id),
            "run_id": "r0",
            "timestamp": "2026-05-06T09:59:00+00:00",
            "outcome": "created",
            "message": EVENT_MESSAGE_MUST_NOT_RENDER,
            "metadata": {"output": RAW_COMMAND_OUTPUT_MUST_NOT_RENDER},
        }]
        graph = _build(job, events)
        re_node = next(n for n in graph.nodes if n.type == NT_RUN_EVENT)
        detail = build_brain_node_detail(job, graph, re_node.id, events)
        assert detail.node_type == NT_RUN_EVENT
        assert EVENT_MESSAGE_MUST_NOT_RENDER not in detail.explanation
        assert RAW_COMMAND_OUTPUT_MUST_NOT_RENDER not in detail.explanation
        assert any("timeline" in a for a in detail.next_actions)

    # ── agent_loop node ──────────────────────────────────────────────────────

    def test_agent_loop_node_detail(self):
        job = _make_job()
        events = [_agent_loop_event(str(job.id))]
        graph = _build(job, events)
        al_node = next(n for n in graph.nodes if n.type == NT_AGENT_LOOP)
        detail = build_brain_node_detail(job, graph, al_node.id, events)
        assert detail.node_type == NT_AGENT_LOOP
        assert "build" in detail.explanation
        assert "continue" in detail.explanation
        assert any("agent-loop" in a for a in detail.next_actions)

    # ── constitution node ────────────────────────────────────────────────────

    def test_constitution_node_detail(self):
        class _FakeConstitution:
            source_files = ["pyproject.toml", "tox.ini"]
            test_commands = ["pytest"]

        job = _make_job()
        graph = _build(job, constitution=_FakeConstitution())
        con_node = next(n for n in graph.nodes if n.type == NT_CONSTITUTION)
        detail = build_brain_node_detail(job, graph, con_node.id, [])
        assert detail.node_type == NT_CONSTITUTION
        assert "2" in detail.explanation  # source_count = 2
        assert any("constitution" in a for a in detail.next_actions)

    # ── placeholder nodes ────────────────────────────────────────────────────

    def test_memory_placeholder_detail(self):
        job = _make_job()
        graph = _build(job)
        mem_node = next(n for n in graph.nodes if n.type == NT_MEMORY)
        detail = build_brain_node_detail(job, graph, mem_node.id, [])
        assert detail.node_type == NT_MEMORY
        assert detail.status == "informational"
        assert "MemPalace" in detail.explanation
        assert any("Step 24+" in a for a in detail.next_actions)

    def test_mcp_placeholder_detail(self):
        job = _make_job()
        graph = _build(job)
        mcp_node = next(n for n in graph.nodes if n.type == NT_MCP)
        detail = build_brain_node_detail(job, graph, mcp_node.id, [])
        assert detail.node_type == NT_MCP
        assert detail.status == "informational"
        assert "MCP" in detail.explanation

    # ── connections ──────────────────────────────────────────────────────────

    def test_connections_include_incoming_and_outgoing(self):
        job = _make_job()
        task = _pending_task()
        job.tasks.append(task)
        graph = _build(job)
        # Job node has outgoing has_task edges
        job_node = next(n for n in graph.nodes if n.type == NT_JOB)
        detail = build_brain_node_detail(job, graph, job_node.id, [])
        outgoing = [c for c in detail.connected_to if c["direction"] == "outgoing"]
        assert len(outgoing) >= 1
        task_conn = next((c for c in outgoing if c["node_type"] == NT_TASK), None)
        assert task_conn is not None
        assert task_conn["edge_type"] == "has_task"

    def test_task_node_has_incoming_has_task(self):
        job = _make_job()
        task = _pending_task()
        job.tasks.append(task)
        graph = _build(job)
        task_node = next(n for n in graph.nodes if n.type == NT_TASK)
        detail = build_brain_node_detail(job, graph, task_node.id, [])
        incoming = [c for c in detail.connected_to if c["direction"] == "incoming"]
        assert any(c["edge_type"] == "has_task" for c in incoming)


# ---------------------------------------------------------------------------
# TestSummarizeBrainNodeDetail
# ---------------------------------------------------------------------------


class TestSummarizeBrainNodeDetail:
    def test_header_present(self):
        job = _make_job()
        graph = _build(job)
        node = next(n for n in graph.nodes if n.type == NT_JOB)
        detail = build_brain_node_detail(job, graph, node.id, [])
        out = summarize_brain_node_detail(detail)
        assert "Remedy Brain Node Detail" in out

    def test_node_id_present(self):
        job = _make_job()
        graph = _build(job)
        node = next(n for n in graph.nodes if n.type == NT_JOB)
        detail = build_brain_node_detail(job, graph, node.id, [])
        out = summarize_brain_node_detail(detail)
        assert node.id[:16] in out

    def test_sections_present(self):
        job = _make_job()
        graph = _build(job)
        node = next(n for n in graph.nodes if n.type == NT_JOB)
        detail = build_brain_node_detail(job, graph, node.id, [])
        out = summarize_brain_node_detail(detail)
        assert "Explanation" in out
        assert "Why it exists" in out
        assert "Connections" in out

    def test_evidence_section_present_when_non_empty(self):
        job = _make_job()
        graph = _build(job)
        node = next(n for n in graph.nodes if n.type == NT_JOB)
        detail = build_brain_node_detail(job, graph, node.id, [])
        out = summarize_brain_node_detail(detail)
        assert "Evidence" in out

    def test_affected_files_section_present_for_patch_intent(self):
        job = _make_job()
        _add_patch_artifact(job)
        graph = _build(job)
        pi_node = next(n for n in graph.nodes if n.type == NT_PATCH_INTENT)
        detail = build_brain_node_detail(job, graph, pi_node.id, [])
        out = summarize_brain_node_detail(detail)
        assert "Affected files" in out
        assert "docs/README.md" in out

    def test_next_actions_section_present(self):
        job = _make_job()
        task = _pending_task()
        job.tasks.append(task)
        events = [_perm_denied_event(str(job.id), str(task.id))]
        graph = _build(job, events)
        blk_node = next(n for n in graph.nodes if n.type == NT_BLOCKER)
        detail = build_brain_node_detail(job, graph, blk_node.id, events)
        out = summarize_brain_node_detail(detail)
        assert "Next actions" in out
        assert "job permit" in out


# ---------------------------------------------------------------------------
# TestExportBrainNodeDetailJson
# ---------------------------------------------------------------------------


class TestExportBrainNodeDetailJson:
    def test_top_level_keys(self):
        job = _make_job()
        graph = _build(job)
        node = next(n for n in graph.nodes if n.type == NT_JOB)
        detail = build_brain_node_detail(job, graph, node.id, [])
        export = export_brain_node_detail_json(detail)
        expected = {
            "job_id", "node_id", "node_type", "title", "status", "risk",
            "explanation", "why_it_exists", "connected_to", "evidence",
            "affected_files", "next_actions", "redaction_notes",
        }
        assert set(export.keys()) == expected

    def test_json_serialisable(self):
        job = _make_job()
        task = _pending_task()
        job.tasks.append(task)
        _, intent_id = _add_patch_artifact(job, task_id=task.id)
        set_approval_state(job, intent_id, APPROVAL_APPROVED)
        events = [_task_completed_event(str(job.id), str(task.id))]
        graph = _build(job, events)
        node = next(n for n in graph.nodes if n.type == NT_JOB)
        detail = build_brain_node_detail(job, graph, node.id, events)
        export = export_brain_node_detail_json(detail)
        serialised = json.dumps(export)
        assert len(serialised) > 0

    def test_connected_to_is_list(self):
        job = _make_job()
        job.tasks.append(_pending_task())
        graph = _build(job)
        node = next(n for n in graph.nodes if n.type == NT_JOB)
        detail = build_brain_node_detail(job, graph, node.id, [])
        export = export_brain_node_detail_json(detail)
        assert isinstance(export["connected_to"], list)

    def test_why_it_exists_is_list(self):
        job = _make_job()
        graph = _build(job)
        node = next(n for n in graph.nodes if n.type == NT_JOB)
        detail = build_brain_node_detail(job, graph, node.id, [])
        export = export_brain_node_detail_json(detail)
        assert isinstance(export["why_it_exists"], list)


# ---------------------------------------------------------------------------
# TestRedactionHardening
# ---------------------------------------------------------------------------


class TestRedactionHardening:
    def _poisoned_setup(self):
        job = _make_job()
        task = _pending_task()
        job.tasks.append(task)

        artifact = Artifact(
            name="proposal",
            content=ARTIFACT_CONTENT_MUST_NOT_RENDER,
            kind=ArtifactKind.BUILDER_PROPOSAL,
            task_id=task.id,
            metadata={
                "patch_intent_explanations": [
                    {
                        "file": "docs/x.md",
                        "action": "modify",
                        "risk": RISK_MEDIUM,
                        "reason": "task type",
                        "summary": "update x",
                        "diff_preview": DIFF_PREVIEW_MUST_NOT_RENDER,
                    }
                ]
            },
        )
        job.artifacts.append(artifact)
        intent_id = make_intent_id(artifact.id, 0)
        set_approval_state(job, intent_id, APPROVAL_APPROVED, reason=APPROVAL_REASON_MUST_NOT_RENDER)

        events = [
            {
                "event": "task_run_completed",
                "job_id": str(job.id),
                "run_id": "r1",
                "timestamp": "2026-05-06T10:01:00+00:00",
                "task_id": str(task.id),
                "outcome": "pass",
                "message": EVENT_MESSAGE_MUST_NOT_RENDER,
                "metadata": {"output": RAW_COMMAND_OUTPUT_MUST_NOT_RENDER},
            }
        ]
        return job, events

    def _check_all_sentinels(self, text: str) -> None:
        for sentinel in _ALL_SENTINELS:
            assert sentinel not in text, f"sentinel leaked: {sentinel}"

    def test_artifact_node_no_content_in_summary(self):
        job, events = self._poisoned_setup()
        graph = _build(job, events)
        art_node = next(n for n in graph.nodes if n.type == NT_ARTIFACT)
        detail = build_brain_node_detail(job, graph, art_node.id, events)
        out = summarize_brain_node_detail(detail)
        assert ARTIFACT_CONTENT_MUST_NOT_RENDER not in out

    def test_patch_intent_no_diff_in_summary(self):
        job, events = self._poisoned_setup()
        graph = _build(job, events)
        pi_node = next(n for n in graph.nodes if n.type == NT_PATCH_INTENT)
        detail = build_brain_node_detail(job, graph, pi_node.id, events)
        out = summarize_brain_node_detail(detail)
        assert DIFF_PREVIEW_MUST_NOT_RENDER not in out

    def test_approval_no_reason_in_summary(self):
        job, events = self._poisoned_setup()
        graph = _build(job, events)
        dec_node = next(n for n in graph.nodes if n.type == NT_APPROVAL)
        detail = build_brain_node_detail(job, graph, dec_node.id, events)
        out = summarize_brain_node_detail(detail)
        assert APPROVAL_REASON_MUST_NOT_RENDER not in out

    def test_verification_no_event_message_in_summary(self):
        job, events = self._poisoned_setup()
        graph = _build(job, events)
        ver_node = next(n for n in graph.nodes if n.type == NT_VERIFICATION)
        detail = build_brain_node_detail(job, graph, ver_node.id, events)
        out = summarize_brain_node_detail(detail)
        assert EVENT_MESSAGE_MUST_NOT_RENDER not in out
        assert RAW_COMMAND_OUTPUT_MUST_NOT_RENDER not in out

    def test_all_sentinels_absent_from_export_json(self):
        job, events = self._poisoned_setup()
        graph = _build(job, events)
        job_node = next(n for n in graph.nodes if n.type == NT_JOB)
        detail = build_brain_node_detail(job, graph, job_node.id, events)
        self._check_all_sentinels(json.dumps(export_brain_node_detail_json(detail)))

    def test_all_sentinels_absent_from_pi_export(self):
        job, events = self._poisoned_setup()
        graph = _build(job, events)
        pi_node = next(n for n in graph.nodes if n.type == NT_PATCH_INTENT)
        detail = build_brain_node_detail(job, graph, pi_node.id, events)
        self._check_all_sentinels(json.dumps(export_brain_node_detail_json(detail)))


# ---------------------------------------------------------------------------
# TestCLIBrainNode
# ---------------------------------------------------------------------------


class TestCLIBrainNode:
    def _job_node_id(self, job: Job) -> str:
        return str(job.id)

    def test_invalid_uuid_exits_1(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        import sys

        from apps.cli.main import main
        with pytest.raises(SystemExit) as exc:
            monkeypatch.setattr(sys, "argv", ["remedy", "brain", "node", "bad-uuid", "some-node"])
            main()
        assert exc.value.code == 1

    def test_unknown_job_exits_1(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        import sys

        from apps.cli.main import main
        with pytest.raises(SystemExit) as exc:
            monkeypatch.setattr(sys, "argv", ["remedy", "brain", "node", str(uuid4()), "some-node"])
            main()
        assert exc.value.code == 1

    def test_unknown_node_exits_1(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        import sys

        from apps.cli.main import main
        with pytest.raises(SystemExit) as exc:
            monkeypatch.setattr(sys, "argv", ["remedy", "brain", "node", str(job.id), "does-not-exist"])
            main()
        assert exc.value.code == 1

    def test_valid_job_and_node_prints_detail(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        import sys

        from apps.cli.main import main
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "node", str(job.id), self._job_node_id(job)])
        main()
        out = capsys.readouterr().out
        assert "Remedy Brain Node Detail" in out
        assert str(job.id)[:8] in out

    def test_json_flag_returns_parseable_json(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        import sys

        from apps.cli.main import main
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "node", str(job.id), self._job_node_id(job), "--json"])
        main()
        out = capsys.readouterr().out
        data = json.loads(out)
        assert data["node_id"] == str(job.id)
        assert data["node_type"] == NT_JOB

    def test_json_flag_top_level_keys(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        import sys

        from apps.cli.main import main
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "node", str(job.id), self._job_node_id(job), "--json"])
        main()
        data = json.loads(capsys.readouterr().out)
        expected = {
            "job_id", "node_id", "node_type", "title", "status", "risk",
            "explanation", "why_it_exists", "connected_to", "evidence",
            "affected_files", "next_actions", "redaction_notes",
        }
        assert set(data.keys()) == expected

    def test_exactly_one_run_log_file_created(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        import sys

        from apps.cli.main import main
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "node", str(job.id), self._job_node_id(job)])
        main()
        runs_dir = tmp_path / "job_logs" / str(job.id)
        assert len(list(runs_dir.glob("*.jsonl"))) == 1

    def test_run_log_metadata_exact_keys(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        import sys

        from apps.cli.main import main
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "node", str(job.id), self._job_node_id(job)])
        main()
        runs_dir = tmp_path / "job_logs" / str(job.id)
        events = [
            json.loads(line)
            for line in next(runs_dir.glob("*.jsonl")).read_text().splitlines()
            if line.strip()
        ]
        inspected = next(e for e in events if e.get("event") == "brain_node_inspected")
        meta = inspected.get("metadata", {})
        assert set(meta.keys()) == {
            "node_id", "node_type", "connected_count", "evidence_count"
        }

    def test_run_log_no_raw_artifact_content(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        artifact = Artifact(
            name="a",
            content=ARTIFACT_CONTENT_MUST_NOT_RENDER,
            kind=ArtifactKind.PLANNING,
        )
        job.artifacts.append(artifact)
        save_job(job)
        import sys

        from apps.cli.main import main
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "node", str(job.id), self._job_node_id(job)])
        main()
        runs_dir = tmp_path / "job_logs" / str(job.id)
        raw = next(runs_dir.glob("*.jsonl")).read_text()
        assert ARTIFACT_CONTENT_MUST_NOT_RENDER not in raw

    def test_json_flag_no_sentinels(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        _, intent_id = _add_patch_artifact(job, content=ARTIFACT_CONTENT_MUST_NOT_RENDER)
        set_approval_state(job, intent_id, APPROVAL_APPROVED, reason=APPROVAL_REASON_MUST_NOT_RENDER)
        save_job(job)
        import sys

        from apps.cli.main import main
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "node", str(job.id), self._job_node_id(job), "--json"])
        main()
        out = capsys.readouterr().out
        for sentinel in _ALL_SENTINELS:
            assert sentinel not in out, f"sentinel leaked in --json: {sentinel}"


# ---------------------------------------------------------------------------
# Memory entry detail
# ---------------------------------------------------------------------------


class TestMemoryEntryDetail:
    def test_memory_entry_detail(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import store_memory
        job = _make_job()
        save_job(job)
        entry = store_memory(key="test_k", value="secret_v", job_id=str(job.id),
                             tags=["t1"], approved=True)
        graph = build_project_brain(job, [])
        mem_node_id = f"memory:{entry.id}"
        detail = build_brain_node_detail(job, graph, mem_node_id, [])
        assert detail.node_type == NT_MEMORY_ENTRY
        assert "test_k" in detail.title
        assert "secret_v" not in summarize_brain_node_detail(detail)

    def test_memory_entry_detail_no_forbidden_sentinels(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import store_memory
        job = _make_job()
        save_job(job)
        entry = store_memory(key="k", value="MUST_NOT_RENDER_VALUE", job_id=str(job.id),
                             approved=True)
        graph = build_project_brain(job, [])
        mem_node_id = f"memory:{entry.id}"
        detail = build_brain_node_detail(job, graph, mem_node_id, [])
        text = summarize_brain_node_detail(detail)
        for sentinel in _ALL_SENTINELS:
            assert sentinel not in text
        assert "MUST_NOT_RENDER_VALUE" not in text

"""
Tests for packages/orchestration/project_brain.py and the `remedy brain` CLI command.

Coverage:
  - BrainNode / BrainEdge / ProjectBrainGraph frozen model construction
  - frozen models reject mutation
  - empty job: job node + memory_placeholder + mcp_placeholder always present
  - task nodes and has_task edges
  - artifact nodes with correct owner edge (task or job)
  - patch intent nodes (pending and decided) + approval_decision nodes
  - verification nodes from task_run_completed events
  - permission_blocker nodes from task_run_failed outcome=permission_denied
  - agent_loop nodes from agent_loop_inspected events
  - run_event nodes for key events (job_created, builder_started, etc.)
  - constitution node from constitution object
  - constitution node from project_constitution_loaded event (no object)
  - project_constitution_loaded event does NOT also create a run_event node
  - memory_placeholder and mcp_placeholder always present, status=informational
  - deterministic node sort: type-priority then id
  - deterministic edge sort: source, target, type
  - summarize output: header, short id, node/edge counts, sections
  - summarize visual status legend: grey/pulsing/white/red/amber/violet/orange
  - summarize includes all node types present
  - export_project_brain_json: version=1, job_id, nodes list, edges list
  - export schema keys: id, type, label, status, risk, ref_id, metadata per node
  - export schema keys: source, target, type, metadata per edge
  - safe cycle parsing: "2"->2, "not-a-number"->0, None->0, malformed event no crash
  - redaction: ARTIFACT_CONTENT_MUST_NOT_RENDER
  - redaction: DIFF_PREVIEW_MUST_NOT_RENDER
  - redaction: APPROVAL_REASON_MUST_NOT_RENDER
  - redaction: EVENT_MESSAGE_MUST_NOT_RENDER
  - redaction: RAW_COMMAND_OUTPUT_MUST_NOT_RENDER
  - CLI: invalid UUID exits 1
  - CLI: unknown job exits 1
  - CLI: valid job prints brain report
  - CLI: --json returns parseable JSON with version=1, job_id, nodes, edges
  - CLI: --json does not leak redaction sentinels
  - CLI: logs project_brain_inspected with exactly the required metadata keys
  - CLI: --json still logs project_brain_inspected with exact metadata keys
  - CLI: run log event contains no raw artifact content
  - CLI: exactly one run log file created
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
from packages.orchestration.patch_intent import RISK_HIGH, RISK_LOW, RISK_MEDIUM
from packages.orchestration.project_brain import (
    ET_BELONGS_TO_PROJECT,
    ET_BLOCKED,
    ET_CREATED,
    ET_DECIDED,
    ET_EMITTED,
    ET_FUTURE_MCP,
    ET_FUTURE_MEMORY,
    ET_GOVERNED,
    ET_HAS_MEMORY,
    ET_HAS_TASK,
    ET_INSPECTED,
    ET_PRODUCED_PI,
    ET_VERIFIED,
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
    NT_PROJECT_PLACEHOLDER,
    NT_RUN_EVENT,
    NT_TASK,
    NT_VERIFICATION,
    BrainEdge,
    BrainNode,
    build_project_brain,
    export_project_brain_json,
    summarize_project_brain,
)
from packages.orchestration.storage import save_job

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_job(**kwargs) -> Job:
    defaults: dict = {"name": "Test brain job", "state": RunState.PENDING}
    defaults.update(kwargs)
    return Job(**defaults)


def _pending_task(**kwargs) -> Task:
    return Task(description="write docs", inputs={"task_type": "write_readme"}, **kwargs)


def _completed_task(**kwargs) -> Task:
    t = Task(description="task done", inputs={"task_type": "write_readme"}, **kwargs)
    t.status = RunState.COMPLETED
    return t


def _add_patch_artifact(job: Job, *, risk: str = RISK_MEDIUM, task_id=None) -> str:
    """Add a single patch-intent artifact to job. Returns intent_id."""
    task_id = task_id or uuid4()
    explanations = [
        {
            "file": "docs/README.md",
            "action": "modify",
            "risk": risk,
            "reason": "task type 'write_readme'",
            "summary": "Update README heading",
        }
    ]
    artifact = Artifact(
        name="builder proposal",
        content="ARTIFACT_CONTENT_MUST_NOT_RENDER",
        kind=ArtifactKind.BUILDER_PROPOSAL,
        task_id=task_id,
        metadata={"patch_intent_explanations": explanations},
    )
    job.artifacts.append(artifact)
    return make_intent_id(artifact.id, 0)


def _task_run_completed_event(job_id: str, task_id: str) -> dict:
    return {
        "event": "task_run_completed",
        "job_id": job_id,
        "run_id": "r1",
        "timestamp": "2026-05-06T10:01:00+00:00",
        "task_id": task_id,
        "outcome": "pass",
        "metadata": {},
    }


def _perm_denied_event(job_id: str, task_id: str | None = None) -> dict:
    ev: dict = {
        "event": "task_run_failed",
        "job_id": job_id,
        "run_id": "r1",
        "timestamp": "2026-05-06T10:00:00+00:00",
        "outcome": "permission_denied",
        "metadata": {"capability": "workspace_write"},
    }
    if task_id is not None:
        ev["task_id"] = task_id
    return ev


def _agent_loop_event(job_id: str, *, stage: str = "build", decision: str = "continue") -> dict:
    return {
        "event": "agent_loop_inspected",
        "job_id": job_id,
        "run_id": "r1",
        "timestamp": "2026-05-06T10:02:00+00:00",
        "outcome": "inspected",
        "metadata": {
            "stage": stage,
            "decision": decision,
            "cycle": 0,
            "max_cycles": 3,
            "pending_finding_count": 0,
        },
    }


def _job_created_event(job_id: str) -> dict:
    return {
        "event": "job_created",
        "job_id": job_id,
        "run_id": "r0",
        "timestamp": "2026-05-06T09:59:00+00:00",
        "outcome": "created",
        "metadata": {},
    }


# ---------------------------------------------------------------------------
# TestBrainNodeEdge
# ---------------------------------------------------------------------------


class TestBrainNodeEdge:
    def test_brain_node_construction(self):
        node = BrainNode(id="abc", type=NT_JOB, label="My Job", status="pending")
        assert node.id == "abc"
        assert node.type == NT_JOB
        assert node.label == "My Job"
        assert node.status == "pending"
        assert node.risk is None
        assert node.ref_id is None
        assert node.metadata == {}

    def test_brain_node_with_metadata(self):
        node = BrainNode(
            id="x",
            type=NT_TASK,
            label="Task",
            metadata={"task_type": "write_readme", "count": 3, "flag": True},
        )
        assert node.metadata["task_type"] == "write_readme"
        assert node.metadata["count"] == 3
        assert node.metadata["flag"] is True

    def test_brain_node_frozen(self):
        node = BrainNode(id="abc", type=NT_JOB, label="Job")
        with pytest.raises((AttributeError, TypeError)):
            node.label = "other"  # type: ignore[misc]

    def test_brain_edge_construction(self):
        edge = BrainEdge(source="a", target="b", type=ET_HAS_TASK)
        assert edge.source == "a"
        assert edge.target == "b"
        assert edge.type == ET_HAS_TASK
        assert edge.metadata == {}

    def test_brain_edge_frozen(self):
        edge = BrainEdge(source="a", target="b", type=ET_HAS_TASK)
        with pytest.raises((AttributeError, TypeError)):
            edge.type = "other"  # type: ignore[misc]

    def test_project_brain_graph_construction(self):
        job = _make_job()
        graph = build_project_brain(job, [])
        assert graph.job_id == job.id
        assert isinstance(graph.nodes, tuple)
        assert isinstance(graph.edges, tuple)

    def test_project_brain_graph_frozen(self):
        job = _make_job()
        graph = build_project_brain(job, [])
        with pytest.raises((AttributeError, TypeError)):
            graph.job_id = uuid4()  # type: ignore[misc]


# ---------------------------------------------------------------------------
# TestBuildProjectBrain
# ---------------------------------------------------------------------------


class TestBuildProjectBrain:
    def test_empty_job_has_job_node(self):
        job = _make_job()
        graph = build_project_brain(job, [])
        job_nodes = [n for n in graph.nodes if n.type == NT_JOB]
        assert len(job_nodes) == 1
        assert job_nodes[0].id == str(job.id)
        assert job_nodes[0].status == "pending"

    def test_empty_job_always_has_placeholders(self):
        job = _make_job()
        graph = build_project_brain(job, [])
        mem_nodes = [n for n in graph.nodes if n.type == NT_MEMORY]
        mcp_nodes = [n for n in graph.nodes if n.type == NT_MCP]
        assert len(mem_nodes) == 1
        assert len(mcp_nodes) == 1
        assert mem_nodes[0].id == "memory_placeholder"
        assert mcp_nodes[0].id == "mcp_placeholder"
        assert mem_nodes[0].status == "informational"
        assert mcp_nodes[0].status == "informational"

    def test_empty_job_has_placeholder_edges(self):
        job = _make_job()
        graph = build_project_brain(job, [])
        job_id = str(job.id)
        mem_edges = [e for e in graph.edges if e.type == ET_FUTURE_MEMORY]
        mcp_edges = [e for e in graph.edges if e.type == ET_FUTURE_MCP]
        assert len(mem_edges) == 1
        assert mem_edges[0].source == job_id
        assert mem_edges[0].target == "memory_placeholder"
        assert len(mcp_edges) == 1
        assert mcp_edges[0].source == job_id
        assert mcp_edges[0].target == "mcp_placeholder"

    def test_task_nodes_and_edges(self):
        job = _make_job()
        task = _pending_task()
        job.tasks.append(task)
        graph = build_project_brain(job, [])
        task_nodes = [n for n in graph.nodes if n.type == NT_TASK]
        assert len(task_nodes) == 1
        assert task_nodes[0].id == str(task.id)
        assert task_nodes[0].status == "pending"
        has_task_edges = [e for e in graph.edges if e.type == ET_HAS_TASK]
        assert len(has_task_edges) == 1
        assert has_task_edges[0].source == str(job.id)
        assert has_task_edges[0].target == str(task.id)

    def test_artifact_node_owned_by_task(self):
        job = _make_job()
        task = _pending_task()
        job.tasks.append(task)
        artifact = Artifact(
            name="proposal",
            content="x",
            kind=ArtifactKind.BUILDER_PROPOSAL,
            task_id=task.id,
        )
        job.artifacts.append(artifact)
        graph = build_project_brain(job, [])
        art_nodes = [n for n in graph.nodes if n.type == NT_ARTIFACT]
        assert len(art_nodes) == 1
        assert art_nodes[0].id == str(artifact.id)
        assert art_nodes[0].status == "available"
        art_edges = [e for e in graph.edges if e.type == ET_CREATED]
        assert len(art_edges) == 1
        assert art_edges[0].source == str(task.id)
        assert art_edges[0].target == str(artifact.id)

    def test_artifact_node_owned_by_job_when_no_task_id(self):
        job = _make_job()
        artifact = Artifact(name="plan", content="x", kind=ArtifactKind.PLANNING, task_id=None)
        job.artifacts.append(artifact)
        graph = build_project_brain(job, [])
        art_edges = [e for e in graph.edges if e.type == ET_CREATED]
        assert art_edges[0].source == str(job.id)

    def test_patch_intent_nodes_pending(self):
        job = _make_job()
        _add_patch_artifact(job, risk=RISK_MEDIUM)
        graph = build_project_brain(job, [])
        pi_nodes = [n for n in graph.nodes if n.type == NT_PATCH_INTENT]
        assert len(pi_nodes) == 1
        assert pi_nodes[0].status == "pending"
        assert pi_nodes[0].risk == RISK_MEDIUM
        # No approval_decision node for pending
        dec_nodes = [n for n in graph.nodes if n.type == NT_APPROVAL]
        assert len(dec_nodes) == 0

    def test_patch_intent_approved_creates_approval_node(self):
        job = _make_job()
        intent_id = _add_patch_artifact(job, risk=RISK_HIGH)
        set_approval_state(job, intent_id, APPROVAL_APPROVED)
        graph = build_project_brain(job, [])
        dec_nodes = [n for n in graph.nodes if n.type == NT_APPROVAL]
        assert len(dec_nodes) == 1
        assert dec_nodes[0].status == APPROVAL_APPROVED
        decided_edges = [e for e in graph.edges if e.type == ET_DECIDED]
        assert len(decided_edges) == 1

    def test_patch_intent_rejected_creates_approval_node(self):
        job = _make_job()
        intent_id = _add_patch_artifact(job, risk=RISK_LOW)
        set_approval_state(job, intent_id, APPROVAL_REJECTED)
        graph = build_project_brain(job, [])
        dec_nodes = [n for n in graph.nodes if n.type == NT_APPROVAL]
        assert len(dec_nodes) == 1
        assert dec_nodes[0].status == APPROVAL_REJECTED

    def test_patch_intent_edge_from_artifact(self):
        job = _make_job()
        _add_patch_artifact(job)
        graph = build_project_brain(job, [])
        pi_edges = [e for e in graph.edges if e.type == ET_PRODUCED_PI]
        assert len(pi_edges) == 1
        # source must be the artifact node
        art_ids = {n.id for n in graph.nodes if n.type == NT_ARTIFACT}
        assert pi_edges[0].source in art_ids

    def test_verification_node_from_task_run_completed(self):
        job = _make_job()
        task = _completed_task()
        job.tasks.append(task)
        events = [_task_run_completed_event(str(job.id), str(task.id))]
        graph = build_project_brain(job, events)
        ver_nodes = [n for n in graph.nodes if n.type == NT_VERIFICATION]
        assert len(ver_nodes) == 1
        assert ver_nodes[0].status == "passed"
        ver_edges = [e for e in graph.edges if e.type == ET_VERIFIED]
        assert len(ver_edges) == 1
        assert ver_edges[0].source == str(task.id)

    def test_permission_blocker_node_from_perm_denied(self):
        job = _make_job()
        task = _pending_task()
        job.tasks.append(task)
        events = [_perm_denied_event(str(job.id), task_id=str(task.id))]
        graph = build_project_brain(job, events)
        blk_nodes = [n for n in graph.nodes if n.type == NT_BLOCKER]
        assert len(blk_nodes) == 1
        assert blk_nodes[0].status == "blocked"
        assert blk_nodes[0].metadata["capability"] == "workspace_write"
        blk_edges = [e for e in graph.edges if e.type == ET_BLOCKED]
        assert len(blk_edges) == 1
        assert blk_edges[0].source == str(task.id)

    def test_permission_blocker_no_task_id(self):
        job = _make_job()
        events = [_perm_denied_event(str(job.id), task_id=None)]
        graph = build_project_brain(job, events)
        blk_nodes = [n for n in graph.nodes if n.type == NT_BLOCKER]
        assert len(blk_nodes) == 1
        # No edge if no task_id
        blk_edges = [e for e in graph.edges if e.type == ET_BLOCKED]
        assert len(blk_edges) == 0

    def test_agent_loop_node(self):
        job = _make_job()
        events = [_agent_loop_event(str(job.id), stage="build", decision="continue")]
        graph = build_project_brain(job, events)
        al_nodes = [n for n in graph.nodes if n.type == NT_AGENT_LOOP]
        assert len(al_nodes) == 1
        assert al_nodes[0].metadata["stage"] == "build"
        assert al_nodes[0].metadata["decision"] == "continue"
        al_edges = [e for e in graph.edges if e.type == ET_INSPECTED]
        assert len(al_edges) == 1
        assert al_edges[0].target == str(job.id)

    def test_run_event_node_for_key_events(self):
        job = _make_job()
        events = [_job_created_event(str(job.id))]
        graph = build_project_brain(job, events)
        re_nodes = [n for n in graph.nodes if n.type == NT_RUN_EVENT]
        assert len(re_nodes) == 1
        assert re_nodes[0].metadata["event_type"] == "job_created"
        re_edges = [e for e in graph.edges if e.type == ET_EMITTED]
        assert len(re_edges) == 1

    def test_non_key_event_not_promoted_to_run_event(self):
        job = _make_job()
        events = [{"event": "task_run_started", "job_id": str(job.id), "metadata": {}}]
        graph = build_project_brain(job, events)
        re_nodes = [n for n in graph.nodes if n.type == NT_RUN_EVENT]
        assert len(re_nodes) == 0

    def test_constitution_node_from_object(self):
        class _FakeConstitution:
            source_files = ["pyproject.toml"]
            test_commands = ["pytest"]

        job = _make_job()
        graph = build_project_brain(job, [], constitution=_FakeConstitution())
        con_nodes = [n for n in graph.nodes if n.type == NT_CONSTITUTION]
        assert len(con_nodes) == 1
        assert con_nodes[0].status == "loaded"
        assert con_nodes[0].metadata["source_count"] == 1
        assert con_nodes[0].metadata["has_test_commands"] is True
        gov_edges = [e for e in graph.edges if e.type == ET_GOVERNED]
        assert len(gov_edges) == 1

    def test_constitution_node_from_event_only(self):
        job = _make_job()
        events = [
            {
                "event": "project_constitution_loaded",
                "job_id": str(job.id),
                "run_id": "r0",
                "timestamp": "2026-05-06T10:00:00+00:00",
                "outcome": "loaded",
                "metadata": {},
            }
        ]
        graph = build_project_brain(job, events)
        con_nodes = [n for n in graph.nodes if n.type == NT_CONSTITUTION]
        assert len(con_nodes) == 1
        assert con_nodes[0].status == "from_event"

    def test_constitution_event_does_not_create_run_event_node(self):
        job = _make_job()
        events = [
            {
                "event": "project_constitution_loaded",
                "job_id": str(job.id),
                "run_id": "r0",
                "timestamp": "2026-05-06T10:00:00+00:00",
                "outcome": "loaded",
                "metadata": {},
            }
        ]
        graph = build_project_brain(job, events)
        re_nodes = [n for n in graph.nodes if n.type == NT_RUN_EVENT]
        assert len(re_nodes) == 0, (
            "project_constitution_loaded must not create a run_event node — "
            "it is already represented by the dedicated constitution node"
        )

    def test_no_constitution_node_when_absent(self):
        job = _make_job()
        graph = build_project_brain(job, [])
        con_nodes = [n for n in graph.nodes if n.type == NT_CONSTITUTION]
        assert len(con_nodes) == 0

    def test_nodes_sorted_by_type_priority_then_id(self):
        job = _make_job()
        task = _pending_task()
        job.tasks.append(task)
        artifact = Artifact(
            name="plan", content="x", kind=ArtifactKind.PLANNING, task_id=task.id
        )
        job.artifacts.append(artifact)
        graph = build_project_brain(job, [])
        types = [n.type for n in graph.nodes]
        # Job must come before task, task before artifact
        assert types.index(NT_JOB) < types.index(NT_TASK)
        assert types.index(NT_TASK) < types.index(NT_ARTIFACT)
        # Placeholders must be at the end
        assert types.index(NT_MEMORY) > types.index(NT_ARTIFACT)
        assert types.index(NT_MCP) > types.index(NT_MEMORY)

    def test_edges_sorted_by_source_target_type(self):
        job = _make_job()
        t1 = _pending_task()
        t2 = _pending_task()
        job.tasks.extend([t1, t2])
        graph = build_project_brain(job, [])
        edge_keys = [(e.source, e.target, e.type) for e in graph.edges]
        assert edge_keys == sorted(edge_keys)

    def test_deterministic_repeated_calls(self):
        job = _make_job()
        task = _pending_task()
        job.tasks.append(task)
        _add_patch_artifact(job, task_id=task.id)
        events = [
            _job_created_event(str(job.id)),
            _task_run_completed_event(str(job.id), str(task.id)),
        ]
        g1 = build_project_brain(job, events)
        g2 = build_project_brain(job, events)
        assert [n.id for n in g1.nodes] == [n.id for n in g2.nodes]
        assert [(e.source, e.target, e.type) for e in g1.edges] == [
            (e.source, e.target, e.type) for e in g2.edges
        ]

    def test_multiple_tasks_and_artifacts(self):
        job = _make_job()
        for _ in range(3):
            job.tasks.append(_pending_task())
        for task in job.tasks:
            job.artifacts.append(
                Artifact(name="a", content="x", kind=ArtifactKind.BUILDER_PROPOSAL, task_id=task.id)
            )
        graph = build_project_brain(job, [])
        assert sum(1 for n in graph.nodes if n.type == NT_TASK) == 3
        assert sum(1 for n in graph.nodes if n.type == NT_ARTIFACT) == 3
        assert sum(1 for e in graph.edges if e.type == ET_HAS_TASK) == 3
        assert sum(1 for e in graph.edges if e.type == ET_CREATED) == 3

    def test_job_node_metadata_counts(self):
        job = _make_job()
        job.tasks.append(_pending_task())
        job.artifacts.append(Artifact(name="a", content="x", kind=ArtifactKind.PLANNING))
        graph = build_project_brain(job, [])
        job_node = next(n for n in graph.nodes if n.type == NT_JOB)
        assert job_node.metadata["task_count"] == 1
        assert job_node.metadata["artifact_count"] == 1


# ---------------------------------------------------------------------------
# TestSummarizeProjectBrain
# ---------------------------------------------------------------------------


class TestSummarizeProjectBrain:
    def test_header_present(self):
        job = _make_job()
        graph = build_project_brain(job, [])
        out = summarize_project_brain(graph)
        assert "Remedy Project Brain" in out

    def test_short_job_id_present(self):
        job = _make_job()
        graph = build_project_brain(job, [])
        out = summarize_project_brain(graph)
        assert str(job.id)[:8] in out

    def test_node_and_edge_counts_present(self):
        job = _make_job()
        graph = build_project_brain(job, [])
        out = summarize_project_brain(graph)
        assert f"Nodes: {len(graph.nodes)}" in out
        assert f"Edges: {len(graph.edges)}" in out

    def test_sections_present(self):
        job = _make_job()
        graph = build_project_brain(job, [])
        out = summarize_project_brain(graph)
        assert "Node summary" in out
        assert "Graph nodes" in out
        assert "Graph edges" in out
        assert "Future layers" in out

    def test_node_types_listed_in_summary(self):
        job = _make_job()
        task = _completed_task()
        job.tasks.append(task)
        events = [_task_run_completed_event(str(job.id), str(task.id))]
        graph = build_project_brain(job, events)
        out = summarize_project_brain(graph)
        assert NT_JOB in out
        assert NT_TASK in out
        assert NT_VERIFICATION in out
        assert NT_MEMORY in out
        assert NT_MCP in out

    def test_future_layers_note(self):
        job = _make_job()
        graph = build_project_brain(job, [])
        out = summarize_project_brain(graph)
        assert "memory_placeholder" in out
        assert "mcp_placeholder" in out


# ---------------------------------------------------------------------------
# TestExportProjectBrainJson
# ---------------------------------------------------------------------------


class TestExportProjectBrainJson:
    def test_version_is_1(self):
        job = _make_job()
        graph = build_project_brain(job, [])
        export = export_project_brain_json(graph)
        assert export["version"] == 1

    def test_job_id_string(self):
        job = _make_job()
        graph = build_project_brain(job, [])
        export = export_project_brain_json(graph)
        assert export["job_id"] == str(job.id)

    def test_nodes_is_list(self):
        job = _make_job()
        graph = build_project_brain(job, [])
        export = export_project_brain_json(graph)
        assert isinstance(export["nodes"], list)
        assert len(export["nodes"]) == len(graph.nodes)

    def test_edges_is_list(self):
        job = _make_job()
        graph = build_project_brain(job, [])
        export = export_project_brain_json(graph)
        assert isinstance(export["edges"], list)
        assert len(export["edges"]) == len(graph.edges)

    def test_node_schema_keys(self):
        job = _make_job()
        graph = build_project_brain(job, [])
        export = export_project_brain_json(graph)
        for node_dict in export["nodes"]:
            assert set(node_dict.keys()) == {"id", "type", "label", "status", "risk", "ref_id", "metadata"}

    def test_edge_schema_keys(self):
        job = _make_job()
        graph = build_project_brain(job, [])
        export = export_project_brain_json(graph)
        for edge_dict in export["edges"]:
            assert set(edge_dict.keys()) == {"source", "target", "type", "metadata"}

    def test_json_serialisable(self):
        job = _make_job()
        task = _pending_task()
        job.tasks.append(task)
        _add_patch_artifact(job, task_id=task.id)
        events = [_job_created_event(str(job.id))]
        graph = build_project_brain(job, events)
        export = export_project_brain_json(graph)
        # Must not raise
        serialised = json.dumps(export)
        assert len(serialised) > 0

    def test_node_order_preserved_from_graph(self):
        job = _make_job()
        graph = build_project_brain(job, [])
        export = export_project_brain_json(graph)
        exported_ids = [n["id"] for n in export["nodes"]]
        graph_ids = [n.id for n in graph.nodes]
        assert exported_ids == graph_ids

    def test_top_level_keys(self):
        job = _make_job()
        graph = build_project_brain(job, [])
        export = export_project_brain_json(graph)
        assert set(export.keys()) == {"version", "job_id", "nodes", "edges", "degraded"}


# ---------------------------------------------------------------------------
# TestRedactionHardening
# ---------------------------------------------------------------------------

ARTIFACT_CONTENT_MUST_NOT_RENDER    = "ARTIFACT_CONTENT_MUST_NOT_RENDER"
DIFF_PREVIEW_MUST_NOT_RENDER        = "DIFF_PREVIEW_MUST_NOT_RENDER"
APPROVAL_REASON_MUST_NOT_RENDER     = "APPROVAL_REASON_MUST_NOT_RENDER"
EVENT_MESSAGE_MUST_NOT_RENDER       = "EVENT_MESSAGE_MUST_NOT_RENDER"
RAW_COMMAND_OUTPUT_MUST_NOT_RENDER  = "RAW_COMMAND_OUTPUT_MUST_NOT_RENDER"


class TestRedactionHardening:
    def _build_poisoned_graph(self) -> tuple[Job, list[dict]]:
        job = _make_job()
        task = _pending_task()
        job.tasks.append(task)

        # Artifact with sentinel content
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
                ],
            },
        )
        job.artifacts.append(artifact)

        # Approval with sentinel reason
        intent_id = make_intent_id(artifact.id, 0)
        set_approval_state(job, intent_id, APPROVAL_APPROVED, reason=APPROVAL_REASON_MUST_NOT_RENDER)

        # Event with sentinel message
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

    def test_artifact_content_not_in_summary(self):
        job, events = self._build_poisoned_graph()
        graph = build_project_brain(job, events)
        out = summarize_project_brain(graph)
        assert ARTIFACT_CONTENT_MUST_NOT_RENDER not in out

    def test_diff_preview_not_in_summary(self):
        job, events = self._build_poisoned_graph()
        graph = build_project_brain(job, events)
        out = summarize_project_brain(graph)
        assert DIFF_PREVIEW_MUST_NOT_RENDER not in out

    def test_approval_reason_not_in_summary(self):
        job, events = self._build_poisoned_graph()
        graph = build_project_brain(job, events)
        out = summarize_project_brain(graph)
        assert APPROVAL_REASON_MUST_NOT_RENDER not in out

    def test_event_message_not_in_summary(self):
        job, events = self._build_poisoned_graph()
        graph = build_project_brain(job, events)
        out = summarize_project_brain(graph)
        assert EVENT_MESSAGE_MUST_NOT_RENDER not in out

    def test_raw_command_output_not_in_summary(self):
        job, events = self._build_poisoned_graph()
        graph = build_project_brain(job, events)
        out = summarize_project_brain(graph)
        assert RAW_COMMAND_OUTPUT_MUST_NOT_RENDER not in out

    def test_sentinels_not_in_export_json(self):
        job, events = self._build_poisoned_graph()
        graph = build_project_brain(job, events)
        export = export_project_brain_json(graph)
        serialised = json.dumps(export)
        for sentinel in [
            ARTIFACT_CONTENT_MUST_NOT_RENDER,
            DIFF_PREVIEW_MUST_NOT_RENDER,
            APPROVAL_REASON_MUST_NOT_RENDER,
            EVENT_MESSAGE_MUST_NOT_RENDER,
            RAW_COMMAND_OUTPUT_MUST_NOT_RENDER,
        ]:
            assert sentinel not in serialised, f"sentinel leaked: {sentinel}"

    def test_artifact_content_not_in_node_metadata(self):
        job, events = self._build_poisoned_graph()
        graph = build_project_brain(job, events)
        for node in graph.nodes:
            for v in node.metadata.values():
                assert ARTIFACT_CONTENT_MUST_NOT_RENDER not in str(v)


# ---------------------------------------------------------------------------
# TestCLIBrain
# ---------------------------------------------------------------------------


class TestCLIBrain:
    def test_invalid_uuid_exits_1(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from apps.cli.main import main
        with pytest.raises(SystemExit) as exc:
            import sys
            monkeypatch.setattr(sys, "argv", ["remedy", "brain", "graph", "not-a-uuid"])
            main()
        assert exc.value.code == 1

    def test_unknown_job_exits_1(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from apps.cli.main import main
        with pytest.raises(SystemExit) as exc:
            import sys
            monkeypatch.setattr(sys, "argv", ["remedy", "brain", "graph", str(uuid4())])
            main()
        assert exc.value.code == 1

    def test_valid_job_prints_report(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        import sys

        from apps.cli.main import main
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "graph", str(job.id)])
        main()
        out = capsys.readouterr().out
        assert "Remedy Project Brain" in out
        assert str(job.id)[:8] in out

    def test_cli_logs_project_brain_inspected(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        import sys

        from apps.cli.main import main
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "graph", str(job.id)])
        main()
        runs_dir = tmp_path / "job_logs" / str(job.id)
        jsonl_files = list(runs_dir.glob("*.jsonl"))
        assert len(jsonl_files) == 1
        events = [
            json.loads(line)
            for line in jsonl_files[0].read_text().splitlines()
            if line.strip()
        ]
        inspected = [e for e in events if e.get("event") == "project_brain_inspected"]
        assert len(inspected) == 1

    def test_run_log_metadata_has_exactly_required_fields(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        import sys

        from apps.cli.main import main
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "graph", str(job.id)])
        main()
        runs_dir = tmp_path / "job_logs" / str(job.id)
        events = [
            json.loads(line)
            for line in next(runs_dir.glob("*.jsonl")).read_text().splitlines()
            if line.strip()
        ]
        inspected = next(e for e in events if e.get("event") == "project_brain_inspected")
        meta = inspected.get("metadata", {})
        assert set(meta.keys()) == {
            "node_count", "edge_count", "task_count", "patch_intent_count"
        }

    def test_run_log_no_raw_artifact_content(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        task = _pending_task()
        job.tasks.append(task)
        artifact = Artifact(
            name="proposal",
            content=ARTIFACT_CONTENT_MUST_NOT_RENDER,
            kind=ArtifactKind.BUILDER_PROPOSAL,
            task_id=task.id,
        )
        job.artifacts.append(artifact)
        save_job(job)
        import sys

        from apps.cli.main import main
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "graph", str(job.id)])
        main()
        runs_dir = tmp_path / "job_logs" / str(job.id)
        raw = next(runs_dir.glob("*.jsonl")).read_text()
        assert ARTIFACT_CONTENT_MUST_NOT_RENDER not in raw

    def test_exactly_one_run_log_file_created(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        import sys

        from apps.cli.main import main
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "graph", str(job.id)])
        main()
        runs_dir = tmp_path / "job_logs" / str(job.id)
        assert len(list(runs_dir.glob("*.jsonl"))) == 1

    def test_json_flag_returns_parseable_json(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        import sys

        from apps.cli.main import main
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "graph", str(job.id), "--json"])
        main()
        out = capsys.readouterr().out
        data = json.loads(out)
        assert data["version"] == 1
        assert data["job_id"] == str(job.id)
        assert isinstance(data["nodes"], list)
        assert isinstance(data["edges"], list)

    def test_json_flag_output_has_correct_top_level_keys(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        import sys

        from apps.cli.main import main
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "graph", str(job.id), "--json"])
        main()
        out = capsys.readouterr().out
        data = json.loads(out)
        assert set(data.keys()) == {"version", "job_id", "nodes", "edges", "degraded"}

    def test_json_flag_does_not_leak_sentinels(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
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
                        "reason": "task",
                        "summary": "update x",
                        "diff_preview": DIFF_PREVIEW_MUST_NOT_RENDER,
                    }
                ]
            },
        )
        job.artifacts.append(artifact)
        intent_id = make_intent_id(artifact.id, 0)
        set_approval_state(job, intent_id, APPROVAL_APPROVED, reason=APPROVAL_REASON_MUST_NOT_RENDER)
        save_job(job)
        import sys

        from apps.cli.main import main
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "graph", str(job.id), "--json"])
        main()
        out = capsys.readouterr().out
        for sentinel in [
            ARTIFACT_CONTENT_MUST_NOT_RENDER,
            DIFF_PREVIEW_MUST_NOT_RENDER,
            APPROVAL_REASON_MUST_NOT_RENDER,
        ]:
            assert sentinel not in out, f"sentinel leaked in --json output: {sentinel}"

    def test_json_flag_still_logs_exact_metadata_keys(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        import sys

        from apps.cli.main import main
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "graph", str(job.id), "--json"])
        main()
        runs_dir = tmp_path / "job_logs" / str(job.id)
        events = [
            json.loads(line)
            for line in next(runs_dir.glob("*.jsonl")).read_text().splitlines()
            if line.strip()
        ]
        inspected = next(e for e in events if e.get("event") == "project_brain_inspected")
        meta = inspected.get("metadata", {})
        assert set(meta.keys()) == {
            "node_count", "edge_count", "task_count", "patch_intent_count"
        }


# ---------------------------------------------------------------------------
# TestVisualLegend
# ---------------------------------------------------------------------------


class TestVisualLegend:
    def test_legend_section_present(self):
        job = _make_job()
        graph = build_project_brain(job, [])
        out = summarize_project_brain(graph)
        assert "Visual status legend" in out

    def test_legend_pending_grey(self):
        job = _make_job()
        graph = build_project_brain(job, [])
        out = summarize_project_brain(graph)
        assert "pending nodes: grey" in out

    def test_legend_running_pulsing(self):
        job = _make_job()
        graph = build_project_brain(job, [])
        out = summarize_project_brain(graph)
        assert "running nodes: pulsing" in out

    def test_legend_completed_white(self):
        job = _make_job()
        graph = build_project_brain(job, [])
        out = summarize_project_brain(graph)
        assert "completed nodes: white" in out

    def test_legend_blocked_red(self):
        job = _make_job()
        graph = build_project_brain(job, [])
        out = summarize_project_brain(graph)
        assert "blocked nodes: red" in out

    def test_legend_needs_approval_amber(self):
        job = _make_job()
        graph = build_project_brain(job, [])
        out = summarize_project_brain(graph)
        assert "needs approval: amber" in out

    def test_legend_memory_layer_violet(self):
        job = _make_job()
        graph = build_project_brain(job, [])
        out = summarize_project_brain(graph)
        assert "memory layer: violet" in out

    def test_legend_mcp_quarantine_orange(self):
        job = _make_job()
        graph = build_project_brain(job, [])
        out = summarize_project_brain(graph)
        assert "mcp quarantine: orange" in out


# ---------------------------------------------------------------------------
# TestSafeCycleParsing
# ---------------------------------------------------------------------------


class TestSafeCycleParsing:
    def _al_event_with_cycle(self, job_id: str, cycle_val: object) -> dict:
        ev: dict = {
            "event": "agent_loop_inspected",
            "job_id": job_id,
            "run_id": "r1",
            "timestamp": "2026-05-06T10:02:00+00:00",
            "outcome": "inspected",
            "metadata": {
                "stage": "build",
                "decision": "continue",
                "max_cycles": 3,
                "pending_finding_count": 0,
            },
        }
        if cycle_val is not None:
            ev["metadata"]["cycle"] = cycle_val
        return ev

    def test_cycle_int_string_parsed(self):
        job = _make_job()
        events = [self._al_event_with_cycle(str(job.id), "2")]
        graph = build_project_brain(job, events)
        al = next(n for n in graph.nodes if n.type == NT_AGENT_LOOP)
        assert al.metadata["cycle"] == 2

    def test_cycle_int_value_parsed(self):
        job = _make_job()
        events = [self._al_event_with_cycle(str(job.id), 3)]
        graph = build_project_brain(job, events)
        al = next(n for n in graph.nodes if n.type == NT_AGENT_LOOP)
        assert al.metadata["cycle"] == 3

    def test_cycle_non_numeric_string_defaults_zero(self):
        job = _make_job()
        events = [self._al_event_with_cycle(str(job.id), "not-a-number")]
        graph = build_project_brain(job, events)
        al = next(n for n in graph.nodes if n.type == NT_AGENT_LOOP)
        assert al.metadata["cycle"] == 0

    def test_cycle_none_defaults_zero(self):
        job = _make_job()
        ev = self._al_event_with_cycle(str(job.id), None)
        # Explicitly set cycle to None in metadata
        ev["metadata"]["cycle"] = None
        graph = build_project_brain(job, [ev])
        al = next(n for n in graph.nodes if n.type == NT_AGENT_LOOP)
        assert al.metadata["cycle"] == 0

    def test_cycle_missing_defaults_zero(self):
        job = _make_job()
        ev: dict = {
            "event": "agent_loop_inspected",
            "job_id": str(job.id),
            "run_id": "r1",
            "timestamp": "2026-05-06T10:02:00+00:00",
            "outcome": "inspected",
            "metadata": {"stage": "build", "decision": "continue"},
            # no cycle key at all
        }
        graph = build_project_brain(job, [ev])
        al = next(n for n in graph.nodes if n.type == NT_AGENT_LOOP)
        assert al.metadata["cycle"] == 0

    def test_malformed_event_no_crash_summarize(self):
        job = _make_job()
        malformed = {
            "event": "agent_loop_inspected",
            "job_id": str(job.id),
            "metadata": {"cycle": "bad", "stage": None, "decision": None},
        }
        graph = build_project_brain(job, [malformed])
        # Must not raise
        out = summarize_project_brain(graph)
        assert "Remedy Project Brain" in out

    def test_malformed_event_no_crash_export(self):
        job = _make_job()
        malformed = {
            "event": "agent_loop_inspected",
            "job_id": str(job.id),
            "metadata": {"cycle": [], "stage": 42, "decision": {}},
        }
        graph = build_project_brain(job, [malformed])
        # Must not raise
        exported = export_project_brain_json(graph)
        assert exported["version"] == 1


# ---------------------------------------------------------------------------
# Project placeholder node (Step 28)
# ---------------------------------------------------------------------------


class TestProjectPlaceholderNode:
    def test_absent_without_project_id(self):
        job = _make_job()
        graph = build_project_brain(job, [])
        types = {n.type for n in graph.nodes}
        assert NT_PROJECT_PLACEHOLDER not in types

    def test_present_when_project_id_set(self):
        from uuid import uuid4
        job = _make_job()
        pid = str(uuid4())
        job.metadata["project_id"] = pid
        graph = build_project_brain(job, [])
        types = {n.type for n in graph.nodes}
        assert NT_PROJECT_PLACEHOLDER in types

    def test_node_id_format(self):
        from uuid import uuid4
        job = _make_job()
        pid = str(uuid4())
        job.metadata["project_id"] = pid
        graph = build_project_brain(job, [])
        pp = next(n for n in graph.nodes if n.type == NT_PROJECT_PLACEHOLDER)
        assert pp.id == f"project:{pid}"

    def test_node_status_linked(self):
        from uuid import uuid4
        job = _make_job()
        pid = str(uuid4())
        job.metadata["project_id"] = pid
        graph = build_project_brain(job, [])
        pp = next(n for n in graph.nodes if n.type == NT_PROJECT_PLACEHOLDER)
        assert pp.status == "linked"

    def test_node_metadata_contains_project_id(self):
        from uuid import uuid4
        job = _make_job()
        pid = str(uuid4())
        job.metadata["project_id"] = pid
        graph = build_project_brain(job, [])
        pp = next(n for n in graph.nodes if n.type == NT_PROJECT_PLACEHOLDER)
        assert pp.metadata["project_id"] == pid

    def test_node_label_contains_short_id(self):
        from uuid import uuid4
        job = _make_job()
        pid = str(uuid4())
        job.metadata["project_id"] = pid
        graph = build_project_brain(job, [])
        pp = next(n for n in graph.nodes if n.type == NT_PROJECT_PLACEHOLDER)
        assert pid[:8] in pp.label

    def test_belongs_to_project_edge_present(self):
        from uuid import uuid4
        job = _make_job()
        pid = str(uuid4())
        job.metadata["project_id"] = pid
        graph = build_project_brain(job, [])
        proj_node_id = f"project:{pid}"
        edge = next(
            (e for e in graph.edges if e.type == ET_BELONGS_TO_PROJECT),
            None,
        )
        assert edge is not None
        assert edge.source == str(job.id)
        assert edge.target == proj_node_id

    def test_no_edge_without_project_id(self):
        job = _make_job()
        graph = build_project_brain(job, [])
        edge = next(
            (e for e in graph.edges if e.type == ET_BELONGS_TO_PROJECT),
            None,
        )
        assert edge is None

    def test_node_sort_order(self):
        from uuid import uuid4
        job = _make_job()
        pid = str(uuid4())
        job.metadata["project_id"] = pid
        graph = build_project_brain(job, [])
        types_ordered = [n.type for n in graph.nodes]
        job_idx = types_ordered.index(NT_JOB)
        pp_idx = types_ordered.index(NT_PROJECT_PLACEHOLDER)
        assert pp_idx > job_idx

    def test_summarize_includes_project_placeholder(self):
        from uuid import uuid4
        job = _make_job()
        pid = str(uuid4())
        job.metadata["project_id"] = pid
        graph = build_project_brain(job, [])
        text = summarize_project_brain(graph)
        assert "project_placeholder" in text

    def test_export_includes_project_placeholder_node(self):
        from uuid import uuid4
        job = _make_job()
        pid = str(uuid4())
        job.metadata["project_id"] = pid
        graph = build_project_brain(job, [])
        d = export_project_brain_json(graph)
        types = {n["type"] for n in d["nodes"]}
        assert "project_placeholder" in types


# ---------------------------------------------------------------------------
# Real memory nodes in Brain
# ---------------------------------------------------------------------------


class TestRealMemoryNodesInBrain:
    """Approved local memory entries appear as real 'memory' nodes."""

    def test_approved_memory_creates_memory_node(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import store_memory
        job = _make_job()
        save_job(job)
        store_memory(key="test_k", value="test_v", job_id=str(job.id), approved=True)
        graph = build_project_brain(job, [])
        types = {n.type for n in graph.nodes}
        assert NT_MEMORY_ENTRY in types

    def test_unapproved_memory_not_in_brain(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import store_memory
        job = _make_job()
        save_job(job)
        store_memory(key="test_k", value="test_v", job_id=str(job.id), approved=False)
        graph = build_project_brain(job, [])
        types = {n.type for n in graph.nodes}
        assert NT_MEMORY_ENTRY not in types

    def test_memory_node_has_correct_metadata(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import store_memory
        job = _make_job()
        save_job(job)
        store_memory(key="my_key", value="secret_val", job_id=str(job.id),
                     tags=["t1"], approved=True)
        graph = build_project_brain(job, [])
        mem_nodes = [n for n in graph.nodes if n.type == NT_MEMORY_ENTRY]
        assert len(mem_nodes) == 1
        meta = mem_nodes[0].metadata
        assert meta["key"] == "my_key"
        assert "value" not in meta, "memory.value must not leak into brain metadata"
        assert meta["approved"] is True
        assert meta["tags"] == ["t1"]

    def test_memory_node_has_edge(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import store_memory
        job = _make_job()
        save_job(job)
        store_memory(key="k", value="v", job_id=str(job.id), approved=True)
        graph = build_project_brain(job, [])
        edge_types = {e.type for e in graph.edges}
        assert ET_HAS_MEMORY in edge_types

    def test_memory_placeholder_still_present(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import store_memory
        job = _make_job()
        save_job(job)
        store_memory(key="k", value="v", job_id=str(job.id), approved=True)
        graph = build_project_brain(job, [])
        types = {n.type for n in graph.nodes}
        assert NT_MEMORY in types, "memory_placeholder still present for future MemPalace"

    def test_memory_node_export_no_value_leak(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import store_memory
        job = _make_job()
        save_job(job)
        store_memory(key="k", value="SECRET_VALUE_42", job_id=str(job.id), approved=True)
        graph = build_project_brain(job, [])
        exported = export_project_brain_json(graph)
        import json
        exported_str = json.dumps(exported)
        assert "SECRET_VALUE_42" not in exported_str

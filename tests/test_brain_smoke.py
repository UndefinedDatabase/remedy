"""
Brain CLI JSON + Detail Smoke Hardening tests (Steps 24.1 / 24.2 / 24.3).

These are the final pre-frontend smoke tests that lock the machine-readable JSON
contract for `remedy brain --json` and `remedy brain node --json`.  Future
frontend code must consume only these --json outputs and must never parse the
human-readable text mode.

Coverage:
  Lifecycle (before planning / after planning / after run / after approval):
    - brain --json produces valid JSON with correct node types at each phase
    - brain-node --json for the primary node of each phase produces valid JSON
      with the correct top-level key set
  Brain node JSON for all 12 node types:
    - job, task, artifact, patch_intent, approval_decision, verification,
      permission_blocker, run_event, agent_loop, constitution,
      memory_placeholder, mcp_placeholder
  Regression:
    - brain --json stdout is pure JSON (no "Remedy Project Brain" human header)
    - brain --json stderr is empty on success
    - brain-node --json stdout is pure JSON (no "Remedy Brain Node Detail" header)
    - brain-node --json stderr is empty on success
    - no traceback in stdout for either command on success
  Run-log schema exact keys:
    - project_brain_inspected: exactly {node_count, edge_count, task_count, patch_intent_count}
    - brain_node_inspected: exactly {node_id, node_type, connected_count, evidence_count}
    - both verified in plain and --json mode
  Redaction hardening (all JSON/log paths):
    - ARTIFACT_CONTENT_MUST_NOT_RENDER
    - DIFF_PREVIEW_MUST_NOT_RENDER
    - APPROVAL_REASON_MUST_NOT_RENDER
    - EVENT_MESSAGE_MUST_NOT_RENDER
    - RAW_COMMAND_OUTPUT_MUST_NOT_RENDER
    absent from raw brain --json stdout, raw brain-node --json stdout,
    project_brain_inspected run log, brain_node_inspected run log;
    brain-node redaction check targets patch_intent (fallback: artifact) —
    nodes directly adjacent to poisoned content, not the job root node
  Unknown-node error path (TestBrainNodeUnknownNode):
    - exits 1, stdout empty, safe "node not found" in stderr, no traceback,
      overlong node_id safely truncated (not echoed verbatim)
"""

from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

import pytest

from packages.core.models import Artifact, ArtifactKind, Job, RunState, Task
from packages.orchestration.approval_queue import (
    APPROVAL_APPROVED,
    make_intent_id,
    set_approval_state,
)
from packages.orchestration.patch_intent import RISK_MEDIUM
from packages.orchestration.storage import save_job

# ---------------------------------------------------------------------------
# Redaction sentinels
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

_DETAIL_KEYS = frozenset({
    "job_id", "node_id", "node_type", "title", "status", "risk",
    "explanation", "why_it_exists", "connected_to", "evidence",
    "affected_files", "next_actions", "redaction_notes",
})


# ---------------------------------------------------------------------------
# Model factories
# ---------------------------------------------------------------------------


def _make_job(**kwargs) -> Job:
    defaults: dict = {"name": "Smoke test job", "state": RunState.PENDING}
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
    content: str = "some content",
    task_id=None,
) -> tuple[Artifact, str]:
    """Add a single patch-intent artifact. Returns (artifact, intent_id)."""
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
                    "reason": "task type",
                    "summary": "Update README heading",
                }
            ]
        },
    )
    job.artifacts.append(artifact)
    return artifact, make_intent_id(artifact.id, 0)


# ---------------------------------------------------------------------------
# Run log helpers
# ---------------------------------------------------------------------------


def _write_run_events(tmp_path: Path, job_id, events: list[dict]) -> None:
    """Write events to the job_logs directory so the CLI can load them."""
    runs_dir = tmp_path / "job_logs" / str(job_id)
    runs_dir.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(e) for e in events]
    (runs_dir / "smoke_test_events.jsonl").write_text("\n".join(lines) + "\n")


def _read_run_log(tmp_path: Path, job_id) -> list[dict]:
    """Read all JSONL run-log events for a job."""
    runs_dir = tmp_path / "job_logs" / str(job_id)
    if not runs_dir.exists():
        return []
    events: list[dict] = []
    for f in sorted(runs_dir.glob("*.jsonl")):
        for line in f.read_text().splitlines():
            line = line.strip()
            if line:
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return events


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


def _job_created_event(job_id: str) -> dict:
    return {
        "event": "job_created",
        "job_id": job_id,
        "run_id": "r0",
        "timestamp": "2026-05-06T09:59:00+00:00",
        "outcome": "created",
        "metadata": {},
    }


def _constitution_loaded_event(job_id: str) -> dict:
    return {
        "event": "project_constitution_loaded",
        "job_id": job_id,
        "run_id": "r0",
        "timestamp": "2026-05-06T10:00:00+00:00",
        "outcome": "loaded",
        "metadata": {},
    }


# ---------------------------------------------------------------------------
# CLI call wrappers (REMEDY_DATA_DIR must be set before calling)
# ---------------------------------------------------------------------------


def _call_brain_json(job_id_str: str, monkeypatch, capsys) -> dict:
    """Run `remedy brain <job_id> --json` and return parsed JSON.

    Consumes both stdout and stderr via capsys.readouterr(). Tests that need
    to inspect stderr directly must call main() and capsys.readouterr() themselves
    rather than using this helper.
    """
    import sys

    from apps.cli.main import main
    monkeypatch.setattr(sys, "argv", ["remedy", "brain", "graph", job_id_str, "--json"])
    main()
    return json.loads(capsys.readouterr().out)


def _call_brain_node_json(job_id_str: str, node_id: str, monkeypatch, capsys) -> dict:
    """Run `remedy brain node <job_id> <node_id> --json` and return parsed JSON.

    Consumes both stdout and stderr via capsys.readouterr(). Tests that need
    to inspect stderr directly must call main() and capsys.readouterr() themselves
    rather than using this helper.
    """
    import sys

    from apps.cli.main import main
    monkeypatch.setattr(sys, "argv", ["remedy", "brain", "node", job_id_str, node_id, "--json"])
    main()
    return json.loads(capsys.readouterr().out)


def _assert_detail_keys(data: dict) -> None:
    actual = set(data.keys())
    extra = actual - _DETAIL_KEYS
    missing = _DETAIL_KEYS - actual
    assert actual == _DETAIL_KEYS, f"extra={extra!r}  missing={missing!r}"


# ---------------------------------------------------------------------------
# TestBrainLifecycle
# ---------------------------------------------------------------------------


class TestBrainLifecycle:
    """End-to-end lifecycle smoke: parse JSON, extract node IDs, inspect nodes."""

    def test_before_planning_brain_json_valid(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        data = _call_brain_json(str(job.id), monkeypatch, capsys)
        assert data["version"] == 1
        assert data["job_id"] == str(job.id)
        assert isinstance(data["nodes"], list)
        assert isinstance(data["edges"], list)
        node_types = {n["type"] for n in data["nodes"]}
        assert {"job", "memory_placeholder", "mcp_placeholder"} <= node_types

    def test_before_planning_brain_node_job_json(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        brain = _call_brain_json(str(job.id), monkeypatch, capsys)
        job_node = next(n for n in brain["nodes"] if n["type"] == "job")
        detail = _call_brain_node_json(str(job.id), job_node["id"], monkeypatch, capsys)
        assert detail["node_type"] == "job"
        assert detail["node_id"] == job_node["id"]
        _assert_detail_keys(detail)

    def test_after_planning_tasks_in_graph_json(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        job.tasks.append(_pending_task())
        job.tasks.append(_pending_task())
        save_job(job)
        data = _call_brain_json(str(job.id), monkeypatch, capsys)
        task_nodes = [n for n in data["nodes"] if n["type"] == "task"]
        assert len(task_nodes) == 2

    def test_after_planning_brain_node_task_json(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        job.tasks.append(_pending_task())
        save_job(job)
        brain = _call_brain_json(str(job.id), monkeypatch, capsys)
        task_node = next(n for n in brain["nodes"] if n["type"] == "task")
        detail = _call_brain_node_json(str(job.id), task_node["id"], monkeypatch, capsys)
        assert detail["node_type"] == "task"
        assert detail["node_id"] == task_node["id"]
        _assert_detail_keys(detail)

    def test_after_run_verification_in_graph(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        task = _completed_task()
        job.tasks.append(task)
        save_job(job)
        _write_run_events(tmp_path, job.id, [_task_completed_event(str(job.id), str(task.id))])
        data = _call_brain_json(str(job.id), monkeypatch, capsys)
        ver_nodes = [n for n in data["nodes"] if n["type"] == "verification"]
        assert len(ver_nodes) == 1

    def test_after_run_brain_node_verification_json(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        task = _completed_task()
        job.tasks.append(task)
        save_job(job)
        _write_run_events(tmp_path, job.id, [_task_completed_event(str(job.id), str(task.id))])
        brain = _call_brain_json(str(job.id), monkeypatch, capsys)
        ver_node = next(n for n in brain["nodes"] if n["type"] == "verification")
        detail = _call_brain_node_json(str(job.id), ver_node["id"], monkeypatch, capsys)
        assert detail["node_type"] == "verification"
        assert detail["node_id"] == ver_node["id"]
        _assert_detail_keys(detail)

    def test_after_approval_decision_in_graph(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        _, intent_id = _add_patch_artifact(job)
        set_approval_state(job, intent_id, APPROVAL_APPROVED)
        save_job(job)
        data = _call_brain_json(str(job.id), monkeypatch, capsys)
        dec_nodes = [n for n in data["nodes"] if n["type"] == "approval_decision"]
        assert len(dec_nodes) == 1

    def test_after_approval_brain_node_approval_json(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        _, intent_id = _add_patch_artifact(job)
        set_approval_state(job, intent_id, APPROVAL_APPROVED)
        save_job(job)
        brain = _call_brain_json(str(job.id), monkeypatch, capsys)
        dec_node = next(n for n in brain["nodes"] if n["type"] == "approval_decision")
        detail = _call_brain_node_json(str(job.id), dec_node["id"], monkeypatch, capsys)
        assert detail["node_type"] == "approval_decision"
        _assert_detail_keys(detail)


# ---------------------------------------------------------------------------
# TestBrainNodeJsonAllTypes
# ---------------------------------------------------------------------------


class TestBrainNodeJsonAllTypes:
    """brain-node --json returns valid JSON with the correct key set for every node type."""

    def _get_detail(
        self,
        job: Job,
        node_type: str,
        tmp_path,
        monkeypatch,
        capsys,
        *,
        events: list[dict] | None = None,
    ) -> dict:
        import sys

        from apps.cli.main import main

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        save_job(job)
        if events:
            _write_run_events(tmp_path, job.id, events)

        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "graph", str(job.id), "--json"])
        main()
        brain = json.loads(capsys.readouterr().out)
        node = next(n for n in brain["nodes"] if n["type"] == node_type)

        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "node", str(job.id), node["id"], "--json"])
        main()
        return json.loads(capsys.readouterr().out)

    def test_job_node(self, tmp_path, monkeypatch, capsys):
        detail = self._get_detail(_make_job(), "job", tmp_path, monkeypatch, capsys)
        assert detail["node_type"] == "job"
        _assert_detail_keys(detail)

    def test_task_node(self, tmp_path, monkeypatch, capsys):
        job = _make_job()
        job.tasks.append(_pending_task())
        detail = self._get_detail(job, "task", tmp_path, monkeypatch, capsys)
        assert detail["node_type"] == "task"
        _assert_detail_keys(detail)

    def test_artifact_node(self, tmp_path, monkeypatch, capsys):
        job = _make_job()
        job.artifacts.append(
            Artifact(name="planning output", content="x", kind=ArtifactKind.PLANNING)
        )
        detail = self._get_detail(job, "artifact", tmp_path, monkeypatch, capsys)
        assert detail["node_type"] == "artifact"
        _assert_detail_keys(detail)

    def test_patch_intent_node(self, tmp_path, monkeypatch, capsys):
        job = _make_job()
        _add_patch_artifact(job)
        detail = self._get_detail(job, "patch_intent", tmp_path, monkeypatch, capsys)
        assert detail["node_type"] == "patch_intent"
        _assert_detail_keys(detail)

    def test_approval_decision_node(self, tmp_path, monkeypatch, capsys):
        job = _make_job()
        _, intent_id = _add_patch_artifact(job)
        set_approval_state(job, intent_id, APPROVAL_APPROVED)
        detail = self._get_detail(job, "approval_decision", tmp_path, monkeypatch, capsys)
        assert detail["node_type"] == "approval_decision"
        _assert_detail_keys(detail)

    def test_verification_node(self, tmp_path, monkeypatch, capsys):
        job = _make_job()
        task = _completed_task()
        job.tasks.append(task)
        events = [_task_completed_event(str(job.id), str(task.id))]
        detail = self._get_detail(job, "verification", tmp_path, monkeypatch, capsys, events=events)
        assert detail["node_type"] == "verification"
        _assert_detail_keys(detail)

    def test_permission_blocker_node(self, tmp_path, monkeypatch, capsys):
        job = _make_job()
        task = _pending_task()
        job.tasks.append(task)
        events = [_perm_denied_event(str(job.id), str(task.id))]
        detail = self._get_detail(job, "permission_blocker", tmp_path, monkeypatch, capsys, events=events)
        assert detail["node_type"] == "permission_blocker"
        _assert_detail_keys(detail)

    def test_run_event_node(self, tmp_path, monkeypatch, capsys):
        job = _make_job()
        events = [_job_created_event(str(job.id))]
        detail = self._get_detail(job, "run_event", tmp_path, monkeypatch, capsys, events=events)
        assert detail["node_type"] == "run_event"
        _assert_detail_keys(detail)

    def test_agent_loop_node(self, tmp_path, monkeypatch, capsys):
        job = _make_job()
        events = [_agent_loop_event(str(job.id))]
        detail = self._get_detail(job, "agent_loop", tmp_path, monkeypatch, capsys, events=events)
        assert detail["node_type"] == "agent_loop"
        _assert_detail_keys(detail)

    def test_constitution_node(self, tmp_path, monkeypatch, capsys):
        job = _make_job()
        events = [_constitution_loaded_event(str(job.id))]
        detail = self._get_detail(job, "constitution", tmp_path, monkeypatch, capsys, events=events)
        assert detail["node_type"] == "constitution"
        _assert_detail_keys(detail)

    def test_memory_placeholder_node(self, tmp_path, monkeypatch, capsys):
        detail = self._get_detail(_make_job(), "memory_placeholder", tmp_path, monkeypatch, capsys)
        assert detail["node_type"] == "memory_placeholder"
        _assert_detail_keys(detail)

    def test_mcp_placeholder_node(self, tmp_path, monkeypatch, capsys):
        detail = self._get_detail(_make_job(), "mcp_placeholder", tmp_path, monkeypatch, capsys)
        assert detail["node_type"] == "mcp_placeholder"
        _assert_detail_keys(detail)


# ---------------------------------------------------------------------------
# TestBrainJsonRegression
# ---------------------------------------------------------------------------


class TestBrainJsonRegression:
    """JSON mode must produce pure JSON; human-readable text must not appear in --json stdout."""

    def test_brain_json_no_human_header(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        data = _call_brain_json(str(job.id), monkeypatch, capsys)
        assert "Remedy Project Brain" not in json.dumps(data)
        assert data["version"] == 1

    def test_brain_json_stderr_empty_on_success(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        import sys

        from apps.cli.main import main
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "graph", str(job.id), "--json"])
        main()
        captured = capsys.readouterr()
        assert captured.err == ""

    def test_brain_json_no_traceback_in_stdout(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        data = _call_brain_json(str(job.id), monkeypatch, capsys)
        assert "Traceback" not in json.dumps(data)

    def test_brain_node_json_no_human_header(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        detail = _call_brain_node_json(str(job.id), str(job.id), monkeypatch, capsys)
        assert "Remedy Brain Node Detail" not in json.dumps(detail)
        assert detail["node_type"] == "job"

    def test_brain_node_json_stderr_empty_on_success(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        import sys

        from apps.cli.main import main
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "node", str(job.id), str(job.id), "--json"])
        main()
        captured = capsys.readouterr()
        assert captured.err == ""

    def test_brain_node_json_no_traceback_in_stdout(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        detail = _call_brain_node_json(str(job.id), str(job.id), monkeypatch, capsys)
        assert "Traceback" not in json.dumps(detail)


# ---------------------------------------------------------------------------
# TestBrainRunLogSchema
# ---------------------------------------------------------------------------


class TestBrainRunLogSchema:
    """Run-log events must have exactly the documented metadata key sets."""

    def _find(self, events: list[dict], event_type: str) -> dict:
        return next(e for e in events if e.get("event") == event_type)

    def test_project_brain_inspected_exact_keys(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        import sys

        from apps.cli.main import main
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "graph", str(job.id)])
        main()
        capsys.readouterr()
        ev = self._find(_read_run_log(tmp_path, job.id), "project_brain_inspected")
        assert set(ev.get("metadata", {}).keys()) == {
            "node_count", "edge_count", "task_count", "patch_intent_count"
        }

    def test_project_brain_inspected_json_mode_exact_keys(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        import sys

        from apps.cli.main import main
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "graph", str(job.id), "--json"])
        main()
        capsys.readouterr()
        ev = self._find(_read_run_log(tmp_path, job.id), "project_brain_inspected")
        assert set(ev.get("metadata", {}).keys()) == {
            "node_count", "edge_count", "task_count", "patch_intent_count"
        }

    def test_brain_node_inspected_exact_keys(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        import sys

        from apps.cli.main import main
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "node", str(job.id), str(job.id)])
        main()
        capsys.readouterr()
        ev = self._find(_read_run_log(tmp_path, job.id), "brain_node_inspected")
        assert set(ev.get("metadata", {}).keys()) == {
            "node_id", "node_type", "connected_count", "evidence_count"
        }

    def test_brain_node_inspected_json_mode_exact_keys(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        import sys

        from apps.cli.main import main
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "node", str(job.id), str(job.id), "--json"])
        main()
        capsys.readouterr()
        ev = self._find(_read_run_log(tmp_path, job.id), "brain_node_inspected")
        assert set(ev.get("metadata", {}).keys()) == {
            "node_id", "node_type", "connected_count", "evidence_count"
        }


# ---------------------------------------------------------------------------
# TestBrainRedactionHardening
# ---------------------------------------------------------------------------


class TestBrainRedactionHardening:
    """All 5 redaction sentinels must be absent from every JSON and log output path."""

    def _poisoned_setup(self, tmp_path: Path) -> Job:
        """Build and save a job with every redaction sentinel embedded."""
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
        save_job(job)
        _write_run_events(tmp_path, job.id, events)
        return job

    def _no_sentinels(self, text: str) -> None:
        for sentinel in _ALL_SENTINELS:
            assert sentinel not in text, f"sentinel leaked: {sentinel!r}"

    def test_brain_json_no_sentinels(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = self._poisoned_setup(tmp_path)
        data = _call_brain_json(str(job.id), monkeypatch, capsys)
        self._no_sentinels(json.dumps(data))

    def test_brain_node_json_no_sentinels(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = self._poisoned_setup(tmp_path)
        brain = _call_brain_json(str(job.id), monkeypatch, capsys)
        # Target a node adjacent to poisoned data (patch_intent preferred, artifact fallback).
        # The job node is intentionally avoided: it holds no direct content fields.
        target_node = (
            next((n for n in brain["nodes"] if n["type"] == "patch_intent"), None)
            or next(n for n in brain["nodes"] if n["type"] == "artifact")
        )
        # Check raw stdout bytes before any json.loads / json.dumps roundtrip — a roundtrip
        # could mask a leak by re-encoding sentinel bytes differently.
        import sys

        from apps.cli.main import main
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "node", str(job.id), target_node["id"], "--json"])
        main()
        raw = capsys.readouterr().out
        self._no_sentinels(raw)
        json.loads(raw)  # must still be valid JSON after the sentinel check

    def test_brain_run_log_no_sentinels(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = self._poisoned_setup(tmp_path)
        import sys

        from apps.cli.main import main
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "graph", str(job.id), "--json"])
        main()
        capsys.readouterr()
        events = _read_run_log(tmp_path, job.id)
        ev = next(e for e in events if e.get("event") == "project_brain_inspected")
        self._no_sentinels(json.dumps(ev))

    def test_brain_node_run_log_no_sentinels(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = self._poisoned_setup(tmp_path)
        brain = _call_brain_json(str(job.id), monkeypatch, capsys)
        # Mirror test_brain_node_json_no_sentinels: patch_intent → artifact → job fallback
        target_node = (
            next((n for n in brain["nodes"] if n["type"] == "patch_intent"), None)
            or next((n for n in brain["nodes"] if n["type"] == "artifact"), None)
            or next(n for n in brain["nodes"] if n["type"] == "job")
        )
        import sys

        from apps.cli.main import main
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "node", str(job.id), target_node["id"]])
        main()
        capsys.readouterr()
        events = _read_run_log(tmp_path, job.id)
        ev = next(e for e in events if e.get("event") == "brain_node_inspected")
        self._no_sentinels(json.dumps(ev))


# ---------------------------------------------------------------------------
# TestBrainNodeUnknownNode
# ---------------------------------------------------------------------------


class TestBrainNodeUnknownNode:
    """brain-node with an unknown node_id must exit 1 with a safe, truncated error."""

    def test_unknown_node_exits_1(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        import sys

        from apps.cli.main import main
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "node", str(job.id), "does-not-exist", "--json"])
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 1

    def test_unknown_node_stdout_empty(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        import sys

        from apps.cli.main import main
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "node", str(job.id), "does-not-exist", "--json"])
        with pytest.raises(SystemExit):
            main()
        assert capsys.readouterr().out == ""

    def test_unknown_node_stderr_safe_message(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        import sys

        from apps.cli.main import main
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "node", str(job.id), "does-not-exist", "--json"])
        with pytest.raises(SystemExit):
            main()
        err = capsys.readouterr().err
        assert "node not found" in err.lower()

    def test_unknown_node_stderr_no_traceback(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        import sys

        from apps.cli.main import main
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "node", str(job.id), "does-not-exist", "--json"])
        with pytest.raises(SystemExit):
            main()
        assert "Traceback" not in capsys.readouterr().err

    def test_long_node_id_safely_truncated_in_stderr(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        long_id = "x" * 200
        import sys

        from apps.cli.main import main
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "node", str(job.id), long_id, "--json"])
        with pytest.raises(SystemExit):
            main()
        err = capsys.readouterr().err
        # The full 200-char id must not appear verbatim; the truncated version is present
        assert long_id not in err
        assert len(err) > 0

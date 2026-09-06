"""
Brain Viewer v0 + v0.1 robustness tests (Steps 25 / 25.1).

Verifies:
  - BrainViewerData is a frozen dataclass with the expected fields.
  - build_brain_viewer_data produces a valid BrainViewerData bundle.
  - export_brain_viewer_json returns the correct top-level schema.
  - write_brain_viewer_files writes only under out_dir (no repo writes).
  - detail_fallback_count is 0 on happy path; increments on forced failure.
  - export JSON and run-log event include detail_fallback_count.
  - Redaction: none of the 5 sentinel strings appear in any generated file,
    including sentinels injected via synthetic run-log events.
  - _compute_positions: job node at centre, layer 1 farther out than layer 0.
  - CLI: invalid UUID exits 1; missing job exits 1; happy-path creates files.
  - CLI: stale/missing target_repo prints safe warning and still generates viewer.
  - brain_viewer_prepared run-log event has exactly
    {node_count, edge_count, detail_count, detail_fallback_count, mode}.
"""

from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

import pytest

from packages.core.models import Artifact, ArtifactKind, Job, RunState
from packages.orchestration.brain_viewer import (
    BrainViewerData,
    _compute_positions,
    _render_static_fallback,
    build_brain_viewer_data,
    export_brain_viewer_json,
    write_brain_viewer_files,
)
from packages.orchestration.project_brain import build_project_brain
from packages.orchestration.storage import save_job

# ---------------------------------------------------------------------------
# Redaction sentinels
# ---------------------------------------------------------------------------

_ALL_SENTINELS = [
    "ARTIFACT_CONTENT_MUST_NOT_RENDER",
    "DIFF_PREVIEW_MUST_NOT_RENDER",
    "APPROVAL_REASON_MUST_NOT_RENDER",
    "EVENT_MESSAGE_MUST_NOT_RENDER",
    "RAW_COMMAND_OUTPUT_MUST_NOT_RENDER",
]

_VIEWER_JSON_KEYS = frozenset(
    {
        "version",
        "job_id",
        "generated_at",
        "graph",
        "node_details",
        "positions",
        "detail_fallback_count",
    }
)

_BRAIN_VIEWER_PREPARED_METADATA_KEYS = frozenset(
    {"node_count", "edge_count", "detail_count", "detail_fallback_count", "mode"}
)


# ---------------------------------------------------------------------------
# Factories
# ---------------------------------------------------------------------------


def _make_job(**kwargs) -> Job:
    defaults: dict = {"name": "Viewer test job", "state": RunState.PENDING}
    defaults.update(kwargs)
    return Job(**defaults)


def _write_run_events(tmp_path: Path, job_id, events: list[dict]) -> None:
    runs_dir = tmp_path / "job_logs" / str(job_id)
    runs_dir.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(e) for e in events]
    (runs_dir / "viewer_test_events.jsonl").write_text("\n".join(lines) + "\n")


def _read_run_log(tmp_path: Path, job_id) -> list[dict]:
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


def _poisoned_job() -> Job:
    """Job with artifact containing all 5 redaction sentinels."""
    job = _make_job()
    content = " ".join(_ALL_SENTINELS)
    artifact = Artifact(
        name="poisoned",
        content=content,
        kind=ArtifactKind.BUILDER_PROPOSAL,
        task_id=uuid4(),
        metadata={
            "patch_intent_diff_preview": "DIFF_PREVIEW_MUST_NOT_RENDER",
            "approval_reason": "APPROVAL_REASON_MUST_NOT_RENDER",
            "command_output": "RAW_COMMAND_OUTPUT_MUST_NOT_RENDER",
        },
    )
    job.artifacts.append(artifact)
    return job


def _poisoned_events(job_id: str) -> list[dict]:
    """Synthetic run events containing event.message and command_output sentinels."""
    return [
        {
            "event": "task_run_failed",
            "job_id": job_id,
            "run_id": "r1",
            "timestamp": "2026-05-07T10:00:00+00:00",
            "outcome": "error",
            "message": "EVENT_MESSAGE_MUST_NOT_RENDER",
            "metadata": {
                "output": "RAW_COMMAND_OUTPUT_MUST_NOT_RENDER",
                "command_output": "RAW_COMMAND_OUTPUT_MUST_NOT_RENDER",
            },
        }
    ]


# ---------------------------------------------------------------------------
# TestBrainViewerDataModel
# ---------------------------------------------------------------------------


class TestBrainViewerDataModel:
    def test_frozen_raises_on_setattr(self):
        data = BrainViewerData(
            job_id="abc",
            generated_at="2026-01-01T00:00:00Z",
            graph={},
            node_details={},
            positions={},
        )
        with pytest.raises((AttributeError, TypeError)):
            data.job_id = "changed"  # type: ignore[misc]

    def test_fields_present(self):
        data = BrainViewerData(
            job_id="abc",
            generated_at="2026-01-01T00:00:00Z",
            graph={"nodes": [], "edges": []},
            node_details={},
            positions={},
        )
        assert data.job_id == "abc"
        assert data.generated_at == "2026-01-01T00:00:00Z"
        assert "nodes" in data.graph
        assert isinstance(data.node_details, dict)
        assert isinstance(data.positions, dict)

    def test_detail_fallback_count_defaults_to_zero(self):
        data = BrainViewerData(
            job_id="abc",
            generated_at="2026-01-01T00:00:00Z",
            graph={},
            node_details={},
            positions={},
        )
        assert data.detail_fallback_count == 0


# ---------------------------------------------------------------------------
# TestBuildBrainViewerData
# ---------------------------------------------------------------------------


class TestBuildBrainViewerData:
    def _data(self) -> BrainViewerData:
        job = _make_job()
        graph = build_project_brain(job, [], constitution=None)
        return build_brain_viewer_data(job, graph, [])

    def test_returns_brain_viewer_data(self):
        assert isinstance(self._data(), BrainViewerData)

    def test_job_id_matches(self):
        job = _make_job()
        graph = build_project_brain(job, [], constitution=None)
        data = build_brain_viewer_data(job, graph, [])
        assert data.job_id == str(job.id)

    def test_positions_cover_all_nodes(self):
        job = _make_job()
        graph = build_project_brain(job, [], constitution=None)
        data = build_brain_viewer_data(job, graph, [])
        node_ids = {n.id for n in graph.nodes}
        assert set(data.positions.keys()) == node_ids

    def test_positions_are_xy_pairs(self):
        data = self._data()
        for node_id, pos in data.positions.items():
            assert len(pos) == 2, f"node {node_id!r} position should be [x, y]"
            assert all(isinstance(v, float) for v in pos), (
                f"node {node_id!r} position values should be float"
            )

    def test_node_details_covers_all_nodes(self):
        job = _make_job()
        graph = build_project_brain(job, [], constitution=None)
        data = build_brain_viewer_data(job, graph, [])
        node_ids = {n.id for n in graph.nodes}
        assert set(data.node_details.keys()) == node_ids

    def test_generated_at_is_iso_utc(self):
        data = self._data()
        assert data.generated_at.endswith("Z")
        assert "T" in data.generated_at


# ---------------------------------------------------------------------------
# TestDetailFallbackCount
# ---------------------------------------------------------------------------


class TestDetailFallbackCount:
    def test_happy_path_fallback_count_zero(self):
        job = _make_job()
        graph = build_project_brain(job, [], constitution=None)
        data = build_brain_viewer_data(job, graph, [])
        assert data.detail_fallback_count == 0

    def test_forced_failure_increments_count(self, monkeypatch):
        import packages.orchestration.brain_viewer as _bv
        original = _bv.build_brain_node_detail
        calls = [0]

        def _explode(job, graph, node_id, events):
            calls[0] += 1
            if calls[0] == 1:
                raise RuntimeError("forced test failure")
            return original(job, graph, node_id, events)

        monkeypatch.setattr(_bv, "build_brain_node_detail", _explode)
        job = _make_job()
        graph = build_project_brain(job, [], constitution=None)
        data = build_brain_viewer_data(job, graph, [])
        assert data.detail_fallback_count == 1

    def test_forced_failure_still_has_all_node_details(self, monkeypatch):
        import packages.orchestration.brain_viewer as _bv
        original = _bv.build_brain_node_detail
        calls = [0]

        def _explode(job, graph, node_id, events):
            calls[0] += 1
            if calls[0] == 1:
                raise RuntimeError("forced test failure")
            return original(job, graph, node_id, events)

        monkeypatch.setattr(_bv, "build_brain_node_detail", _explode)
        job = _make_job()
        graph = build_project_brain(job, [], constitution=None)
        data = build_brain_viewer_data(job, graph, [])
        node_ids = {n.id for n in graph.nodes}
        assert set(data.node_details.keys()) == node_ids

    def test_export_json_includes_detail_fallback_count(self):
        job = _make_job()
        graph = build_project_brain(job, [], constitution=None)
        data = build_brain_viewer_data(job, graph, [])
        exported = export_brain_viewer_json(data)
        assert "detail_fallback_count" in exported
        assert exported["detail_fallback_count"] == 0


# ---------------------------------------------------------------------------
# TestExportBrainViewerJson
# ---------------------------------------------------------------------------


class TestExportBrainViewerJson:
    def test_top_level_keys(self):
        job = _make_job()
        graph = build_project_brain(job, [], constitution=None)
        data = build_brain_viewer_data(job, graph, [])
        exported = export_brain_viewer_json(data)
        assert set(exported.keys()) == _VIEWER_JSON_KEYS

    def test_version_is_1(self):
        job = _make_job()
        graph = build_project_brain(job, [], constitution=None)
        data = build_brain_viewer_data(job, graph, [])
        assert export_brain_viewer_json(data)["version"] == 1

    def test_json_serialisable(self):
        job = _make_job()
        graph = build_project_brain(job, [], constitution=None)
        data = build_brain_viewer_data(job, graph, [])
        exported = export_brain_viewer_json(data)
        serialised = json.dumps(exported)
        assert json.loads(serialised)["version"] == 1


# ---------------------------------------------------------------------------
# TestWriteBrainViewerFiles
# ---------------------------------------------------------------------------


class TestWriteBrainViewerFiles:
    def _write(self, tmp_path: Path) -> tuple[Path, BrainViewerData]:
        job = _make_job()
        graph = build_project_brain(job, [], constitution=None)
        data = build_brain_viewer_data(job, graph, [])
        out_dir = tmp_path / "viewers" / str(job.id)
        index_path = write_brain_viewer_files(data, out_dir)
        return index_path, data

    def test_returns_index_html_path(self, tmp_path):
        index_path, _ = self._write(tmp_path)
        assert index_path.name == "index.html"

    def test_index_html_exists(self, tmp_path):
        index_path, _ = self._write(tmp_path)
        assert index_path.exists()

    def test_viewer_data_json_exists(self, tmp_path):
        index_path, _ = self._write(tmp_path)
        assert (index_path.parent / "viewer_data.json").exists()

    def test_viewer_data_json_valid(self, tmp_path):
        index_path, _ = self._write(tmp_path)
        raw = (index_path.parent / "viewer_data.json").read_text()
        parsed = json.loads(raw)
        assert parsed["version"] == 1

    def test_viewer_data_json_includes_fallback_count(self, tmp_path):
        index_path, _ = self._write(tmp_path)
        parsed = json.loads((index_path.parent / "viewer_data.json").read_text())
        assert "detail_fallback_count" in parsed

    def test_no_writes_outside_out_dir(self, tmp_path):
        """Files are written only under out_dir (or its ancestors), not cwd or repo root."""
        out_dir = tmp_path / "viewers" / str(uuid4())
        job = _make_job()
        graph = build_project_brain(job, [], constitution=None)
        data = build_brain_viewer_data(job, graph, [])
        before = set(tmp_path.rglob("*"))
        write_brain_viewer_files(data, out_dir)
        after = set(tmp_path.rglob("*"))
        for p in after - before:
            is_under_out = p == out_dir or str(p).startswith(str(out_dir) + "/")
            is_ancestor_of_out = str(out_dir).startswith(str(p) + "/")
            assert is_under_out or is_ancestor_of_out, (
                f"file written outside out_dir or its ancestors: {p}"
            )

    def test_html_contains_job_short_id(self, tmp_path):
        index_path, data = self._write(tmp_path)
        html = index_path.read_text()
        assert data.job_id[:8] in html


# ---------------------------------------------------------------------------
# TestBrainViewerRedaction
# ---------------------------------------------------------------------------


class TestBrainViewerRedaction:
    def _build_poisoned_data(self) -> BrainViewerData:
        job = _poisoned_job()
        events = _poisoned_events(str(job.id))
        graph = build_project_brain(job, events, constitution=None)
        return build_brain_viewer_data(job, graph, events)

    def _no_sentinels(self, text: str, label: str) -> None:
        for s in _ALL_SENTINELS:
            assert s not in text, f"sentinel {s!r} found in {label}"

    def test_viewer_data_json_no_sentinels(self, tmp_path):
        data = self._build_poisoned_data()
        out_dir = tmp_path / "viewers" / data.job_id
        write_brain_viewer_files(data, out_dir)
        raw = (out_dir / "viewer_data.json").read_text()
        self._no_sentinels(raw, "viewer_data.json")

    def test_index_html_no_sentinels(self, tmp_path):
        data = self._build_poisoned_data()
        out_dir = tmp_path / "viewers" / data.job_id
        write_brain_viewer_files(data, out_dir)
        html = (out_dir / "index.html").read_text()
        self._no_sentinels(html, "index.html")

    def test_event_message_sentinel_absent_from_viewer_data(self, tmp_path):
        """EVENT_MESSAGE_MUST_NOT_RENDER from synthetic event must not appear in viewer_data.json."""
        job = _make_job()
        events = _poisoned_events(str(job.id))
        graph = build_project_brain(job, events, constitution=None)
        data = build_brain_viewer_data(job, graph, events)
        out_dir = tmp_path / "viewers" / str(job.id)
        write_brain_viewer_files(data, out_dir)
        raw = (out_dir / "viewer_data.json").read_text()
        assert "EVENT_MESSAGE_MUST_NOT_RENDER" not in raw
        assert "RAW_COMMAND_OUTPUT_MUST_NOT_RENDER" not in raw

    def test_event_message_sentinel_absent_from_index_html(self, tmp_path):
        """Event sentinels must not appear in the embedded HTML."""
        job = _make_job()
        events = _poisoned_events(str(job.id))
        graph = build_project_brain(job, events, constitution=None)
        data = build_brain_viewer_data(job, graph, events)
        out_dir = tmp_path / "viewers" / str(job.id)
        write_brain_viewer_files(data, out_dir)
        html = (out_dir / "index.html").read_text()
        assert "EVENT_MESSAGE_MUST_NOT_RENDER" not in html
        assert "RAW_COMMAND_OUTPUT_MUST_NOT_RENDER" not in html

    def test_cli_viewer_files_no_sentinels(self, tmp_path, monkeypatch, capsys):
        """brain-view CLI: viewer files must be free of all sentinels when job has poisoned events."""
        import sys

        from apps.cli.main import main

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _poisoned_job()
        save_job(job)
        _write_run_events(tmp_path, job.id, _poisoned_events(str(job.id)))
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "view", str(job.id)])
        main()
        capsys.readouterr()

        out_dir = tmp_path / "viewers" / str(job.id)
        for fname in ("viewer_data.json", "index.html"):
            text = (out_dir / fname).read_text()
            self._no_sentinels(text, fname)

    def test_brain_viewer_prepared_run_log_no_sentinels(
        self, tmp_path, monkeypatch, capsys
    ):
        """brain_viewer_prepared run-log event must not contain any sentinel string."""
        import sys

        from apps.cli.main import main

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _poisoned_job()
        save_job(job)
        _write_run_events(tmp_path, job.id, _poisoned_events(str(job.id)))
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "view", str(job.id)])
        main()
        capsys.readouterr()

        events = _read_run_log(tmp_path, job.id)
        prepared = next(e for e in events if e.get("event") == "brain_viewer_prepared")
        serialised = json.dumps(prepared)
        self._no_sentinels(serialised, "brain_viewer_prepared run-log event")


# ---------------------------------------------------------------------------
# TestConstitutionGuard
# ---------------------------------------------------------------------------


class TestConstitutionGuard:
    def test_stale_repo_no_crash(self, tmp_path, monkeypatch, capsys):
        """brain-view succeeds when target_repo points to a non-existent path."""
        import sys

        from apps.cli.main import main

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        job.metadata["target_repo"] = str(tmp_path / "nonexistent" / "repo")
        save_job(job)
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "view", str(job.id)])
        # Must not raise or exit with non-zero
        main()
        capsys.readouterr()

    def test_stale_repo_generates_index_html(self, tmp_path, monkeypatch, capsys):
        """brain-view still creates index.html when target_repo is stale."""
        import sys

        from apps.cli.main import main

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        job.metadata["target_repo"] = str(tmp_path / "nonexistent" / "repo")
        save_job(job)
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "view", str(job.id)])
        main()
        capsys.readouterr()
        assert (tmp_path / "viewers" / str(job.id) / "index.html").exists()

    def test_stale_repo_stderr_safe_warning(self, tmp_path, monkeypatch, capsys):
        """stderr contains only the safe warning text, not raw exception messages."""
        import sys

        from apps.cli.main import main

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        job.metadata["target_repo"] = str(tmp_path / "nonexistent" / "repo")
        save_job(job)
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "view", str(job.id)])
        main()
        err = capsys.readouterr().err
        assert "Warning: project constitution unavailable for viewer." in err

    def test_stale_repo_stderr_no_traceback(self, tmp_path, monkeypatch, capsys):
        """No raw exception text or traceback in stderr for stale repos."""
        import sys

        from apps.cli.main import main

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        job.metadata["target_repo"] = str(tmp_path / "nonexistent" / "repo")
        save_job(job)
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "view", str(job.id)])
        main()
        err = capsys.readouterr().err
        assert "Traceback" not in err
        assert "Exception" not in err
        assert "Error" not in err.replace(
            "Warning: project constitution unavailable for viewer.", ""
        )

    def test_no_attached_repo_still_works(self, tmp_path, monkeypatch, capsys):
        """brain-view works for a job with no target_repo metadata."""
        import sys

        from apps.cli.main import main

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()  # no target_repo
        save_job(job)
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "view", str(job.id)])
        main()
        capsys.readouterr()
        assert (tmp_path / "viewers" / str(job.id) / "index.html").exists()


# ---------------------------------------------------------------------------
# TestComputePositions
# ---------------------------------------------------------------------------


class TestComputePositions:
    def test_job_at_centre(self):
        from packages.orchestration.brain_viewer import _CX, _CY

        nodes = [{"id": "j1", "type": "job"}]
        positions = _compute_positions(nodes)
        assert positions["j1"] == [_CX, _CY]

    def test_layer_1_farther_than_layer_0(self):
        from packages.orchestration.brain_viewer import _CX, _CY

        nodes = [
            {"id": "j1", "type": "job"},
            {"id": "t1", "type": "task"},
        ]
        positions = _compute_positions(nodes)
        dist_job = (
            (positions["j1"][0] - _CX) ** 2 + (positions["j1"][1] - _CY) ** 2
        ) ** 0.5
        dist_task = (
            (positions["t1"][0] - _CX) ** 2 + (positions["t1"][1] - _CY) ** 2
        ) ** 0.5
        assert dist_task > dist_job

    def test_unknown_type_gets_layer_3_radius(self):
        from packages.orchestration.brain_viewer import _CX, _CY, _LAYER_RADIUS

        nodes = [{"id": "x1", "type": "totally_unknown"}]
        positions = _compute_positions(nodes)
        x, y = positions["x1"]
        dist = ((x - _CX) ** 2 + (y - _CY) ** 2) ** 0.5
        assert abs(dist - _LAYER_RADIUS[3]) < 1.0


# ---------------------------------------------------------------------------
# TestBrainViewCli
# ---------------------------------------------------------------------------


class TestBrainViewCli:
    def test_invalid_uuid_exits_1(self, tmp_path, monkeypatch, capsys):
        import sys

        from apps.cli.main import main

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "view", "not-a-uuid"])
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1
        err = capsys.readouterr().err
        assert "invalid job ID" in err

    def test_job_not_found_exits_1(self, tmp_path, monkeypatch, capsys):
        import sys

        from apps.cli.main import main

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        fake_id = str(uuid4())
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "view", fake_id])
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1

    def test_happy_path_creates_index_html(self, tmp_path, monkeypatch, capsys):
        import sys

        from apps.cli.main import main

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "view", str(job.id)])
        main()
        index_path = tmp_path / "viewers" / str(job.id) / "index.html"
        assert index_path.exists()

    def test_happy_path_prints_path(self, tmp_path, monkeypatch, capsys):
        import sys

        from apps.cli.main import main

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "view", str(job.id)])
        main()
        out = capsys.readouterr().out
        assert "Brain Viewer:" in out
        assert "index.html" in out

    def test_happy_path_logs_brain_viewer_prepared(self, tmp_path, monkeypatch, capsys):
        import sys

        from apps.cli.main import main

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "view", str(job.id)])
        main()
        capsys.readouterr()
        events = _read_run_log(tmp_path, job.id)
        prepared = [e for e in events if e.get("event") == "brain_viewer_prepared"]
        assert len(prepared) == 1

    def test_brain_viewer_prepared_schema(self, tmp_path, monkeypatch, capsys):
        """brain_viewer_prepared metadata keys must be exactly the contract set."""
        import sys

        from apps.cli.main import main

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "view", str(job.id)])
        main()
        capsys.readouterr()
        events = _read_run_log(tmp_path, job.id)
        prepared = next(e for e in events if e.get("event") == "brain_viewer_prepared")
        meta = prepared["metadata"]
        actual = set(meta.keys())
        extra = actual - _BRAIN_VIEWER_PREPARED_METADATA_KEYS
        missing = _BRAIN_VIEWER_PREPARED_METADATA_KEYS - actual
        assert actual == _BRAIN_VIEWER_PREPARED_METADATA_KEYS, (
            f"extra={extra!r}  missing={missing!r}"
        )

    def test_brain_viewer_prepared_mode_is_static(self, tmp_path, monkeypatch, capsys):
        import sys

        from apps.cli.main import main

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "view", str(job.id)])
        main()
        capsys.readouterr()
        events = _read_run_log(tmp_path, job.id)
        prepared = next(e for e in events if e.get("event") == "brain_viewer_prepared")
        assert prepared["metadata"]["mode"] == "static"

    def test_brain_viewer_prepared_fallback_count_zero_on_clean_job(
        self, tmp_path, monkeypatch, capsys
    ):
        """brain_viewer_prepared detail_fallback_count is 0 for a normal job."""
        import sys

        from apps.cli.main import main

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "view", str(job.id)])
        main()
        capsys.readouterr()
        events = _read_run_log(tmp_path, job.id)
        prepared = next(e for e in events if e.get("event") == "brain_viewer_prepared")
        assert prepared["metadata"]["detail_fallback_count"] == 0

    def test_no_writes_to_cwd(self, tmp_path, monkeypatch, capsys):
        """brain-view must not write files outside REMEDY_DATA_DIR."""
        import sys

        from apps.cli.main import main

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        cwd = Path.cwd()
        before = set(cwd.glob("*.html")) | set(cwd.glob("*.json"))
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "view", str(job.id)])
        main()
        capsys.readouterr()
        after = set(cwd.glob("*.html")) | set(cwd.glob("*.json"))
        assert after == before, "brain-view must not write files to cwd"


# ---------------------------------------------------------------------------
# TestBrainViewerDiagnostics — Step 26.5
# ---------------------------------------------------------------------------


class TestBrainViewerDiagnostics:
    """Brain Viewer must fail visibly — no infinite spinner allowed."""

    def _html(self, tmp_path: Path) -> str:
        job = _make_job()
        graph = build_project_brain(job, [], constitution=None)
        data = build_brain_viewer_data(job, graph, [])
        out_dir = tmp_path / "viewers" / str(job.id)
        index_path = write_brain_viewer_files(data, out_dir)
        return index_path.read_text()

    # -- Status element tests --

    def test_body_has_render_status_static_fallback_initial(self, tmp_path):
        html = self._html(tmp_path)
        assert 'data-render-status="static-fallback"' in html

    def test_has_render_badge_element(self, tmp_path):
        html = self._html(tmp_path)
        assert 'id="render-badge"' in html

    def test_render_badge_initial_status_static_fallback(self, tmp_path):
        html = self._html(tmp_path)
        assert 'data-status="static-fallback"' in html

    # -- Error panel tests --

    def test_has_error_panel_element(self, tmp_path):
        html = self._html(tmp_path)
        assert 'id="err-panel"' in html

    def test_error_panel_hidden_by_default(self, tmp_path):
        html = self._html(tmp_path)
        assert 'id="err-panel"' in html
        # error panel must start hidden
        idx = html.index('id="err-panel"')
        nearby = html[max(0, idx - 100):idx + 100]
        assert 'display:none' in nearby or 'display: none' in nearby

    def test_has_err_msg_element(self, tmp_path):
        html = self._html(tmp_path)
        assert 'id="err-msg"' in html

    # -- Diagnostics panel tests --

    def test_has_diag_nodes(self, tmp_path):
        html = self._html(tmp_path)
        assert 'id="diag-nodes"' in html

    def test_has_diag_edges(self, tmp_path):
        html = self._html(tmp_path)
        assert 'id="diag-edges"' in html

    def test_has_diag_details(self, tmp_path):
        html = self._html(tmp_path)
        assert 'id="diag-details"' in html

    def test_has_diag_fallbacks(self, tmp_path):
        html = self._html(tmp_path)
        assert 'id="diag-fallbacks"' in html

    def test_has_diag_sel(self, tmp_path):
        html = self._html(tmp_path)
        assert 'id="diag-sel"' in html

    def test_has_diag_status(self, tmp_path):
        html = self._html(tmp_path)
        assert 'id="diag-status"' in html

    # -- JS error handling tests --

    def test_has_js_try_catch(self, tmp_path):
        html = self._html(tmp_path)
        assert 'try{' in html or 'try {' in html

    def test_has_js_catch_clause(self, tmp_path):
        html = self._html(tmp_path)
        assert '}catch(' in html or '} catch(' in html

    def test_has_js_error_function(self, tmp_path):
        html = self._html(tmp_path)
        assert '_vErr' in html

    def test_has_window_onerror(self, tmp_path):
        html = self._html(tmp_path)
        assert 'window.onerror' in html

    def test_has_set_render_status_function(self, tmp_path):
        html = self._html(tmp_path)
        assert 'setRenderStatus' in html

    # -- Regression: viewer_data.json still valid --

    def test_viewer_data_json_remains_valid(self, tmp_path):
        job = _make_job()
        graph = build_project_brain(job, [], constitution=None)
        data = build_brain_viewer_data(job, graph, [])
        out_dir = tmp_path / "viewers" / str(job.id)
        write_brain_viewer_files(data, out_dir)
        raw = (out_dir / "viewer_data.json").read_text()
        parsed = json.loads(raw)
        assert parsed["version"] == 1
        assert "graph" in parsed
        assert "node_details" in parsed

    # -- Regression: redaction sentinels absent --

    def test_redaction_sentinels_absent_from_index_html(self, tmp_path):
        job = _poisoned_job()
        events = _poisoned_events(str(job.id))
        graph = build_project_brain(job, events, constitution=None)
        data = build_brain_viewer_data(job, graph, events)
        out_dir = tmp_path / "viewers" / str(job.id)
        write_brain_viewer_files(data, out_dir)
        html = (out_dir / "index.html").read_text()
        for s in _ALL_SENTINELS:
            assert s not in html, f"sentinel {s!r} found in index.html"

    # -- Regression: brain_viewer_prepared schema unchanged --

    def test_brain_viewer_prepared_schema_unchanged(
        self, tmp_path, monkeypatch, capsys
    ):
        import sys

        from apps.cli.main import main

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "view", str(job.id)])
        main()
        capsys.readouterr()
        events = _read_run_log(tmp_path, job.id)
        prepared = next(e for e in events if e.get("event") == "brain_viewer_prepared")
        assert set(prepared["metadata"].keys()) == _BRAIN_VIEWER_PREPARED_METADATA_KEYS

    # -- Timeout guard --

    def test_has_timeout_guard(self, tmp_path):
        html = self._html(tmp_path)
        assert "setTimeout" in html

    def test_timeout_guard_threshold_2000ms(self, tmp_path):
        html = self._html(tmp_path)
        assert "2000" in html

    def test_timeout_guard_message(self, tmp_path):
        html = self._html(tmp_path)
        assert "render did not complete" in html

    # -- window.onerror --

    def test_window_onerror_has_console_error(self, tmp_path):
        html = self._html(tmp_path)
        assert "console.error" in html

    def test_window_onerror_does_not_return_true(self, tmp_path):
        html = self._html(tmp_path)
        idx = html.index("window.onerror=function(msg)")
        snippet = html[idx : idx + 120]
        assert "return true" not in snippet

    # -- Regression: detail_fallback_count propagates --

    def test_detail_fallback_count_in_viewer_data_json(self, tmp_path, monkeypatch):
        import packages.orchestration.brain_viewer as _bv
        original = _bv.build_brain_node_detail
        calls = [0]

        def _explode(job, graph, node_id, events):
            calls[0] += 1
            if calls[0] == 1:
                raise RuntimeError("forced diagnostic test failure")
            return original(job, graph, node_id, events)

        monkeypatch.setattr(_bv, "build_brain_node_detail", _explode)
        job = _make_job()
        graph = build_project_brain(job, [], constitution=None)
        data = build_brain_viewer_data(job, graph, [])
        out_dir = tmp_path / "viewers" / str(job.id)
        write_brain_viewer_files(data, out_dir)
        parsed = json.loads((out_dir / "viewer_data.json").read_text())
        assert parsed["detail_fallback_count"] == 1


# ---------------------------------------------------------------------------
# TestBrainViewerDataIsland — Step 27
# ---------------------------------------------------------------------------


class TestBrainViewerDataIsland:
    """Data island architecture: viewer data as non-executable JSON, with server-rendered fallback."""

    def _html(self, tmp_path: Path) -> str:
        job = _make_job()
        graph = build_project_brain(job, [], constitution=None)
        data = build_brain_viewer_data(job, graph, [])
        out_dir = tmp_path / "viewers" / str(job.id)
        index_path = write_brain_viewer_files(data, out_dir)
        return index_path.read_text()

    def _island_data(self, html: str) -> dict:
        import re
        m = re.search(
            r'<script[^>]*id="viewer-data"[^>]*>(.*?)</script>',
            html,
            re.DOTALL,
        )
        assert m is not None, "viewer-data island not found in HTML"
        return json.loads(m.group(1))

    # -- No executable data literal --

    def test_no_var_vd_literal_assignment(self, tmp_path):
        html = self._html(tmp_path)
        assert "var VD=__VIEWER_DATA_JSON__" not in html

    def test_no_unresolved_viewer_data_placeholder(self, tmp_path):
        html = self._html(tmp_path)
        assert "__VIEWER_DATA_JSON__" not in html

    # -- Data island element present --

    def test_data_island_type_application_json(self, tmp_path):
        html = self._html(tmp_path)
        assert 'type="application/json"' in html

    def test_data_island_id_viewer_data(self, tmp_path):
        html = self._html(tmp_path)
        assert 'id="viewer-data"' in html

    def test_data_island_parses_as_json(self, tmp_path):
        html = self._html(tmp_path)
        data = self._island_data(html)
        assert isinstance(data, dict)

    def test_data_island_version_1(self, tmp_path):
        html = self._html(tmp_path)
        data = self._island_data(html)
        assert data["version"] == 1

    def test_data_island_has_graph(self, tmp_path):
        html = self._html(tmp_path)
        data = self._island_data(html)
        assert "graph" in data

    def test_data_island_node_count_matches_viewer_data_json(self, tmp_path):
        job = _make_job()
        graph = build_project_brain(job, [], constitution=None)
        viewer_data = build_brain_viewer_data(job, graph, [])
        out_dir = tmp_path / "viewers" / str(job.id)
        index_path = write_brain_viewer_files(viewer_data, out_dir)
        html = index_path.read_text()
        island = self._island_data(html)
        json_file = json.loads((out_dir / "viewer_data.json").read_text())
        assert len(island["graph"]["nodes"]) == len(json_file["graph"]["nodes"])

    # -- Static fallback section --

    def test_static_fallback_section_exists(self, tmp_path):
        html = self._html(tmp_path)
        assert 'id="static-fallback"' in html

    def test_static_fallback_has_sf_sum(self, tmp_path):
        html = self._html(tmp_path)
        assert 'class="sf-sum"' in html

    def test_static_fallback_has_sf_tbl(self, tmp_path):
        html = self._html(tmp_path)
        assert 'class="sf-tbl"' in html

    def test_static_fallback_job_node_type_appears(self, tmp_path):
        html = self._html(tmp_path)
        assert ">job<" in html

    def test_static_fallback_node_count_present(self, tmp_path):
        html = self._html(tmp_path)
        assert "nodes <b>" in html

    def test_static_fallback_edge_count_present(self, tmp_path):
        html = self._html(tmp_path)
        assert "edges <b>" in html

    def test_static_fallback_detail_count_present(self, tmp_path):
        html = self._html(tmp_path)
        assert "details <b>" in html

    def test_static_fallback_fallback_count_present(self, tmp_path):
        html = self._html(tmp_path)
        assert "fallbacks <b>" in html

    def test_no_unresolved_static_fallback_placeholder(self, tmp_path):
        html = self._html(tmp_path)
        assert "__STATIC_FALLBACK__" not in html

    # -- Initial status --

    def test_initial_status_static_fallback(self, tmp_path):
        html = self._html(tmp_path)
        assert 'data-render-status="static-fallback"' in html

    # -- JS reads data island --

    def test_js_reads_data_island(self, tmp_path):
        html = self._html(tmp_path)
        assert "getElementById('viewer-data')" in html

    # -- Regression: sentinels absent --

    def test_sentinels_absent_from_index_html(self, tmp_path):
        job = _poisoned_job()
        events = _poisoned_events(str(job.id))
        graph = build_project_brain(job, events, constitution=None)
        data = build_brain_viewer_data(job, graph, events)
        out_dir = tmp_path / "viewers" / str(job.id)
        write_brain_viewer_files(data, out_dir)
        html = (out_dir / "index.html").read_text()
        for s in _ALL_SENTINELS:
            assert s not in html, f"sentinel {s!r} found in index.html"

    # -- Regression: viewer_data.json schema unchanged --

    def test_viewer_data_json_schema_unchanged(self, tmp_path):
        job = _make_job()
        graph = build_project_brain(job, [], constitution=None)
        data = build_brain_viewer_data(job, graph, [])
        out_dir = tmp_path / "viewers" / str(job.id)
        write_brain_viewer_files(data, out_dir)
        parsed = json.loads((out_dir / "viewer_data.json").read_text())
        assert set(parsed.keys()) == _VIEWER_JSON_KEYS


# ---------------------------------------------------------------------------
# TestBrainViewerFallbackTruncation — Step 27.1
# ---------------------------------------------------------------------------


class TestBrainViewerFallbackTruncation:
    """Static fallback shows a notice when the node list is truncated at 50."""

    def _fallback(self, node_count: int) -> str:
        nodes = [
            {"id": f"n{i}", "type": "task", "label": f"task {i}", "status": "pending", "risk": None}
            for i in range(node_count)
        ]
        viewer_dict = {
            "graph": {"nodes": nodes, "edges": []},
            "node_details": {},
            "detail_fallback_count": 0,
        }
        return _render_static_fallback(viewer_dict)

    def test_no_truncation_notice_zero_nodes(self):
        html = self._fallback(0)
        assert "showing 50 of" not in html
        assert "sf-trunc" not in html

    def test_no_truncation_notice_few_nodes(self):
        html = self._fallback(5)
        assert "showing 50 of" not in html
        assert "sf-trunc" not in html

    def test_no_truncation_notice_exactly_50(self):
        html = self._fallback(50)
        assert "showing 50 of" not in html
        assert "sf-trunc" not in html

    def test_truncation_notice_at_51(self):
        html = self._fallback(51)
        assert "sf-trunc" in html
        assert "showing 50 of 51 nodes" in html

    def test_truncation_notice_at_large_count(self):
        html = self._fallback(200)
        assert "sf-trunc" in html
        assert "showing 50 of 200 nodes" in html

    def test_truncation_table_still_has_50_rows(self):
        html = self._fallback(100)
        # 50 data rows + 1 header row = 51 <tr> elements
        import re
        rows = re.findall(r"<tr>", html)
        assert len(rows) == 51  # header + 50 data rows

    def test_truncation_notice_no_raw_html_injection(self):
        # The count is an integer — verify escape path is used
        html = self._fallback(55)
        assert "<script" not in html
        assert "sf-trunc" in html

    def test_full_write_path_no_truncation_normal_job(self, tmp_path):
        """A normal minimal job has far fewer than 50 nodes — no truncation notice."""
        job = _make_job()
        graph = build_project_brain(job, [], constitution=None)
        data = build_brain_viewer_data(job, graph, [])
        out_dir = tmp_path / "viewers" / str(job.id)
        index_path = write_brain_viewer_files(data, out_dir)
        html = index_path.read_text()
        assert "showing 50 of" not in html


# ---------------------------------------------------------------------------
# TestBrainViewerPlaceholderOrder — Step 27.1
# ---------------------------------------------------------------------------


class TestBrainViewerPlaceholderOrder:
    """__VIEWER_DATA_JSON__ must be replaced before __STATIC_FALLBACK__ to prevent
    a node label of '__VIEWER_DATA_JSON__' from being expanded to the full JSON blob
    inside the static fallback table."""

    def test_viewer_data_json_label_stays_literal_in_fallback(self, tmp_path):
        """A node label that is literally '__VIEWER_DATA_JSON__' must appear as
        text in the fallback table cell, not as the injected JSON blob."""
        job = _make_job(name="__VIEWER_DATA_JSON__")
        graph = build_project_brain(job, [], constitution=None)
        data = build_brain_viewer_data(job, graph, [])
        out_dir = tmp_path / "viewers" / str(job.id)
        index_path = write_brain_viewer_files(data, out_dir)
        html = index_path.read_text()
        # The label must appear as a literal <td> value, not trigger JSON injection
        assert "<td>__VIEWER_DATA_JSON__</td>" in html
        # Confirm the full JSON blob was NOT injected into a table cell
        # (the JSON blob would contain '"version"' — proof of injection)
        fallback_start = html.index('id="static-fallback"')
        fallback_end = html.index('id="main"', fallback_start)
        fallback_section = html[fallback_start:fallback_end]
        assert '"version"' not in fallback_section

    def test_static_fallback_placeholder_absent_from_output(self, tmp_path):
        job = _make_job()
        graph = build_project_brain(job, [], constitution=None)
        data = build_brain_viewer_data(job, graph, [])
        out_dir = tmp_path / "viewers" / str(job.id)
        index_path = write_brain_viewer_files(data, out_dir)
        html = index_path.read_text()
        assert "__STATIC_FALLBACK__" not in html
        assert "__VIEWER_DATA_JSON__" not in html

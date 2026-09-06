"""
Unit tests for packages/orchestration/run_log.py.

Tests cover:
  - RunLogWriter creates directory and JSONL file
  - Appends valid JSON lines
  - Preserves append order
  - Does not overwrite existing events on subsequent appends
  - new_run_id() returns unique IDs
  - Events include timestamp, job_id, run_id
  - metadata default is not shared between events
  - read_run_events returns empty list for missing file
  - read_run_events returns all events in order
  - RunEvent.to_json_line() drops None fields, always includes metadata
  - RunLogWriter.log() convenience method writes correct fields
"""

from __future__ import annotations

from uuid import uuid4

from packages.orchestration.run_log import (
    RunEvent,
    RunLogWriter,
    new_run_id,
    read_run_events,
)

# ---------------------------------------------------------------------------
# new_run_id
# ---------------------------------------------------------------------------


class TestNewRunId:
    def test_returns_string(self):
        assert isinstance(new_run_id(), str)

    def test_run_ids_are_unique(self):
        ids = {new_run_id() for _ in range(100)}
        assert len(ids) == 100

    def test_run_id_is_nonempty(self):
        assert len(new_run_id()) > 0


# ---------------------------------------------------------------------------
# RunEvent.to_json_line
# ---------------------------------------------------------------------------


class TestRunEventToJsonLine:
    def _make_event(self, **overrides) -> RunEvent:
        defaults = dict(
            event="test_event",
            job_id="job-123",
            run_id="run-abc",
            timestamp="2026-01-01T00:00:00+00:00",
        )
        defaults.update(overrides)
        return RunEvent(**defaults)

    def test_output_is_valid_json(self):
        import json

        evt = self._make_event()
        parsed = json.loads(evt.to_json_line())
        assert isinstance(parsed, dict)

    def test_required_fields_present(self):
        import json

        evt = self._make_event()
        parsed = json.loads(evt.to_json_line())
        assert parsed["event"] == "test_event"
        assert parsed["job_id"] == "job-123"
        assert parsed["run_id"] == "run-abc"
        assert parsed["timestamp"] == "2026-01-01T00:00:00+00:00"

    def test_none_fields_are_dropped(self):
        import json

        evt = self._make_event(task_id=None, artifact_id=None, provider=None)
        parsed = json.loads(evt.to_json_line())
        assert "task_id" not in parsed
        assert "artifact_id" not in parsed
        assert "provider" not in parsed

    def test_set_optional_fields_are_included(self):
        import json

        evt = self._make_event(task_id="t-1", provider="ollama", outcome="pass")
        parsed = json.loads(evt.to_json_line())
        assert parsed["task_id"] == "t-1"
        assert parsed["provider"] == "ollama"
        assert parsed["outcome"] == "pass"

    def test_metadata_always_included_even_when_empty(self):
        import json

        evt = self._make_event()
        parsed = json.loads(evt.to_json_line())
        assert "metadata" in parsed
        assert parsed["metadata"] == {}

    def test_metadata_content_preserved(self):
        import json

        evt = self._make_event(metadata={"elapsed_ms": 500, "task_type": "write_readme"})
        parsed = json.loads(evt.to_json_line())
        assert parsed["metadata"]["elapsed_ms"] == 500
        assert parsed["metadata"]["task_type"] == "write_readme"

    def test_no_trailing_newline(self):
        evt = self._make_event()
        line = evt.to_json_line()
        assert not line.endswith("\n")


# ---------------------------------------------------------------------------
# RunLogWriter construction
# ---------------------------------------------------------------------------


class TestRunLogWriterConstruction:
    def test_creates_job_directory(self, tmp_path):
        job_id = uuid4()
        writer = RunLogWriter(job_id=job_id, data_root=tmp_path)
        job_dir = tmp_path / "runs" / str(job_id)
        assert job_dir.is_dir()

    def test_path_is_inside_job_directory(self, tmp_path):
        job_id = uuid4()
        writer = RunLogWriter(job_id=job_id, data_root=tmp_path)
        assert writer.path.parent == tmp_path / "runs" / str(job_id)

    def test_path_has_jsonl_extension(self, tmp_path):
        job_id = uuid4()
        writer = RunLogWriter(job_id=job_id, data_root=tmp_path)
        assert writer.path.suffix == ".jsonl"

    def test_path_filename_is_run_id(self, tmp_path):
        job_id = uuid4()
        writer = RunLogWriter(job_id=job_id, data_root=tmp_path)
        assert writer.path.stem == writer.run_id

    def test_explicit_run_id_is_used(self, tmp_path):
        job_id = uuid4()
        writer = RunLogWriter(job_id=job_id, run_id="fixed-run-id", data_root=tmp_path)
        assert writer.run_id == "fixed-run-id"
        assert writer.path.name == "fixed-run-id.jsonl"

    def test_auto_generated_run_id_is_nonempty(self, tmp_path):
        job_id = uuid4()
        writer = RunLogWriter(job_id=job_id, data_root=tmp_path)
        assert len(writer.run_id) > 0

    def test_two_writers_for_same_job_get_different_run_ids(self, tmp_path):
        job_id = uuid4()
        w1 = RunLogWriter(job_id=job_id, data_root=tmp_path)
        w2 = RunLogWriter(job_id=job_id, data_root=tmp_path)
        assert w1.run_id != w2.run_id

    def test_file_does_not_exist_until_first_append(self, tmp_path):
        job_id = uuid4()
        writer = RunLogWriter(job_id=job_id, data_root=tmp_path)
        # File should not exist yet (created lazily on first write)
        # Note: directory is created eagerly; file is created on first write.
        assert not writer.path.exists()

    def test_default_data_root_is_the_process_data_dir(self, tmp_path, monkeypatch):
        # Pins the default path the deleted `_runs_dir_default` alias used to carry.
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job_id = uuid4()
        writer = RunLogWriter(job_id=job_id)
        assert writer.path.parent == tmp_path / "runs" / str(job_id)


# ---------------------------------------------------------------------------
# RunLogWriter.append
# ---------------------------------------------------------------------------


class TestRunLogWriterAppend:
    def _writer(self, tmp_path) -> RunLogWriter:
        return RunLogWriter(job_id=uuid4(), data_root=tmp_path)

    def _make_event(self, writer: RunLogWriter, event: str = "test") -> RunEvent:
        return RunEvent(
            event=event,
            job_id=writer._job_id,
            run_id=writer.run_id,
            timestamp="2026-01-01T00:00:00+00:00",
        )

    def test_creates_file_on_first_append(self, tmp_path):
        writer = self._writer(tmp_path)
        writer.append(self._make_event(writer))
        assert writer.path.exists()

    def test_appended_line_is_valid_json(self, tmp_path):
        import json

        writer = self._writer(tmp_path)
        writer.append(self._make_event(writer, "e1"))
        lines = writer.path.read_text().splitlines()
        assert len(lines) == 1
        parsed = json.loads(lines[0])
        assert parsed["event"] == "e1"

    def test_preserves_append_order(self, tmp_path):
        import json

        writer = self._writer(tmp_path)
        for name in ("first", "second", "third"):
            writer.append(self._make_event(writer, name))

        events = [json.loads(l) for l in writer.path.read_text().splitlines()]
        assert [e["event"] for e in events] == ["first", "second", "third"]

    def test_does_not_overwrite_existing_events(self, tmp_path):
        import json

        writer = self._writer(tmp_path)
        writer.append(self._make_event(writer, "existing"))
        writer.append(self._make_event(writer, "new"))

        events = [json.loads(l) for l in writer.path.read_text().splitlines()]
        assert events[0]["event"] == "existing"
        assert events[1]["event"] == "new"

    def test_each_line_ends_with_newline(self, tmp_path):
        writer = self._writer(tmp_path)
        writer.append(self._make_event(writer))
        raw = writer.path.read_text()
        assert raw.endswith("\n")

    def test_multiple_events_each_on_own_line(self, tmp_path):
        writer = self._writer(tmp_path)
        for _ in range(5):
            writer.append(self._make_event(writer))
        lines = [l for l in writer.path.read_text().splitlines() if l.strip()]
        assert len(lines) == 5


# ---------------------------------------------------------------------------
# RunLogWriter.log convenience method
# ---------------------------------------------------------------------------


class TestRunLogWriterLog:
    def test_log_writes_event_name(self, tmp_path):

        writer = RunLogWriter(job_id=uuid4(), data_root=tmp_path)
        writer.log("my_event")
        events = read_run_events(writer.path)
        assert len(events) == 1
        assert events[0]["event"] == "my_event"

    def test_log_includes_job_id_and_run_id(self, tmp_path):
        job_id = uuid4()
        writer = RunLogWriter(job_id=job_id, data_root=tmp_path)
        writer.log("e")
        events = read_run_events(writer.path)
        assert events[0]["job_id"] == str(job_id)
        assert events[0]["run_id"] == writer.run_id

    def test_log_includes_timestamp(self, tmp_path):
        writer = RunLogWriter(job_id=uuid4(), data_root=tmp_path)
        writer.log("e")
        events = read_run_events(writer.path)
        assert "timestamp" in events[0]
        assert len(events[0]["timestamp"]) > 0

    def test_timestamp_is_utc_isoformat(self, tmp_path):
        from datetime import datetime

        writer = RunLogWriter(job_id=uuid4(), data_root=tmp_path)
        writer.log("e")
        events = read_run_events(writer.path)
        ts = events[0]["timestamp"]
        # Should parse as a valid ISO datetime
        dt = datetime.fromisoformat(ts)
        assert dt.tzinfo is not None

    def test_log_top_level_fields(self, tmp_path):
        writer = RunLogWriter(job_id=uuid4(), data_root=tmp_path)
        writer.log(
            "builder_started",
            task_id="t-1",
            artifact_id="a-1",
            provider="ollama",
            role="builder",
            model="qwen3",
            outcome="running",
            message="ok",
        )
        events = read_run_events(writer.path)
        e = events[0]
        assert e["task_id"] == "t-1"
        assert e["artifact_id"] == "a-1"
        assert e["provider"] == "ollama"
        assert e["role"] == "builder"
        assert e["model"] == "qwen3"
        assert e["outcome"] == "running"
        assert e["message"] == "ok"

    def test_extra_kwargs_go_into_metadata(self, tmp_path):
        writer = RunLogWriter(job_id=uuid4(), data_root=tmp_path)
        writer.log("e", elapsed_ms=500, task_count=3)
        events = read_run_events(writer.path)
        assert events[0]["metadata"]["elapsed_ms"] == 500
        assert events[0]["metadata"]["task_count"] == 3

    def test_metadata_default_not_shared_between_events(self, tmp_path):
        """Each event must have its own independent metadata dict."""
        writer = RunLogWriter(job_id=uuid4(), data_root=tmp_path)
        writer.log("e1", x=1)
        writer.log("e2", y=2)
        events = read_run_events(writer.path)
        assert "y" not in events[0]["metadata"]
        assert "x" not in events[1]["metadata"]

    def test_none_optional_fields_not_in_output(self, tmp_path):
        writer = RunLogWriter(job_id=uuid4(), data_root=tmp_path)
        writer.log("e")  # no optional fields
        events = read_run_events(writer.path)
        e = events[0]
        assert "task_id" not in e
        assert "artifact_id" not in e
        assert "provider" not in e


# ---------------------------------------------------------------------------
# read_run_events
# ---------------------------------------------------------------------------


class TestReadRunEvents:
    def test_returns_empty_list_for_missing_file(self, tmp_path):
        result = read_run_events(tmp_path / "nonexistent.jsonl")
        assert result == []

    def test_returns_all_events_in_order(self, tmp_path):
        writer = RunLogWriter(job_id=uuid4(), data_root=tmp_path)
        for name in ("alpha", "beta", "gamma"):
            writer.log(name)
        events = read_run_events(writer.path)
        assert [e["event"] for e in events] == ["alpha", "beta", "gamma"]

    def test_returns_list_of_dicts(self, tmp_path):
        writer = RunLogWriter(job_id=uuid4(), data_root=tmp_path)
        writer.log("e")
        events = read_run_events(writer.path)
        assert isinstance(events, list)
        assert isinstance(events[0], dict)

    def test_empty_file_returns_empty_list(self, tmp_path):
        path = tmp_path / "empty.jsonl"
        path.write_text("")
        assert read_run_events(path) == []

    def test_metadata_is_preserved(self, tmp_path):
        writer = RunLogWriter(job_id=uuid4(), data_root=tmp_path)
        writer.log("e", task_type="write_readme", count=7)
        events = read_run_events(writer.path)
        assert events[0]["metadata"]["task_type"] == "write_readme"
        assert events[0]["metadata"]["count"] == 7

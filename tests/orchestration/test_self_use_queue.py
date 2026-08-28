"""F257 — tests for the self-use queue and its read-only loader.

The load-bearing test here is
:meth:`TestShippedQueueParsesAsJobs.test_every_item_parses_as_a_job_file`: it is
what keeps the queue and the job parser from drifting apart, and it is why the
queue stores job TEXT rather than a second task format (DECISION F257 D2).
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.orchestration.pingpong_job import parse_job_file
from packages.orchestration.self_use_queue import (
    SELF_USE_QUEUE_SCHEMA_VERSION,
    SelfUseQueueError,
    default_self_use_queue_path,
    load_self_use_queue,
    next_self_use_item,
    pending_self_use_items,
)

_ONE_ITEM = {
    "id": "SU-001",
    "title": "A curated item",
    "why": "Because a reader would look here and find nothing.",
    "job_markdown": "# Job: Demo\n\n## Task 1\nDo the thing.\n\nAcceptance:\n- it is done\n",
    "consumed_by": "",
}


def _queue_body(items: list[dict], schema_version: int = 1) -> dict:
    return {
        "schema_version": schema_version,
        "description": "fixture queue",
        "items": items,
    }


def _write_queue(tmp_path: Path, body, name: str = "self_use_queue.json") -> Path:
    """Write a fixture queue and answer its path. Bad JSON is passed as a str."""
    path = tmp_path / name
    if isinstance(body, str):
        path.write_text(body, encoding="utf-8")
    else:
        path.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
    return path


def _item(**overrides) -> dict:
    item = dict(_ONE_ITEM)
    item.update(overrides)
    return item


@pytest.fixture
def isolate_data_root(tmp_path: Path, monkeypatch) -> Path:
    """Keep ``parse_job_file``'s job persistence inside this test's own root."""
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


class TestShippedQueueLoads:
    """The file Remedy actually ships is valid against its own loader."""

    def test_shipped_queue_loads_with_at_least_one_item(self):
        entries = load_self_use_queue()
        assert len(entries) >= 1

    def test_shipped_queue_declares_schema_version_one(self):
        body = json.loads(default_self_use_queue_path().read_text(encoding="utf-8"))
        assert body["schema_version"] == SELF_USE_QUEUE_SCHEMA_VERSION == 1

    def test_shipped_ids_are_unique_and_match_the_pattern(self):
        import re

        ids = [entry.id for entry in load_self_use_queue()]
        assert len(set(ids)) == len(ids), f"duplicate ids: {sorted(ids)}"
        for item_id in ids:
            assert re.match(r"^SU-\d{3}$", item_id), item_id


class TestShippedQueueParsesAsJobs:
    """Every shipped item is really a job file, not merely a string."""

    def test_every_item_parses_as_a_job_file(self, tmp_path: Path, isolate_data_root):
        repo = tmp_path / "repo"
        repo.mkdir()
        for entry in load_self_use_queue():
            job = parse_job_file(entry.job_markdown, str(repo))
            assert job.tasks, f"{entry.id}: job_markdown yielded no tasks"
            assert job.tasks[0].title.strip(), f"{entry.id}: first task has no title"


class TestLoaderRaisesRatherThanReturningEmpty:
    """"The queue is empty" and "I could not read it" must never look alike."""

    def test_missing_file_raises(self, tmp_path: Path):
        with pytest.raises(SelfUseQueueError):
            load_self_use_queue(tmp_path / "absent.json")

    def test_unparseable_json_raises(self, tmp_path: Path):
        path = _write_queue(tmp_path, "{ not json at all")
        with pytest.raises(SelfUseQueueError):
            load_self_use_queue(path)

    def test_wrong_schema_version_raises(self, tmp_path: Path):
        path = _write_queue(tmp_path, _queue_body([_item()], schema_version=2))
        with pytest.raises(SelfUseQueueError):
            load_self_use_queue(path)

    def test_missing_key_raises(self, tmp_path: Path):
        broken = _item()
        del broken["why"]
        path = _write_queue(tmp_path, _queue_body([broken]))
        with pytest.raises(SelfUseQueueError):
            load_self_use_queue(path)

    def test_wrongly_typed_key_raises(self, tmp_path: Path):
        path = _write_queue(tmp_path, _queue_body([_item(title=17)]))
        with pytest.raises(SelfUseQueueError):
            load_self_use_queue(path)

    def test_wrongly_typed_items_value_raises(self, tmp_path: Path):
        path = _write_queue(tmp_path, _queue_body("not a list"))
        with pytest.raises(SelfUseQueueError):
            load_self_use_queue(path)

    def test_duplicate_id_raises(self, tmp_path: Path):
        path = _write_queue(tmp_path, _queue_body([_item(), _item(title="second")]))
        with pytest.raises(SelfUseQueueError):
            load_self_use_queue(path)

    def test_id_not_matching_the_pattern_raises(self, tmp_path: Path):
        path = _write_queue(tmp_path, _queue_body([_item(id="SU-1")]))
        with pytest.raises(SelfUseQueueError):
            load_self_use_queue(path)

    def test_empty_queue_is_not_an_error(self, tmp_path: Path):
        path = _write_queue(tmp_path, _queue_body([]))
        assert load_self_use_queue(path) == ()


class TestNextSelfUseItem:
    """The next item is the first PENDING one, in file order."""

    def test_returns_the_first_pending_item(self, tmp_path: Path):
        path = _write_queue(tmp_path, _queue_body([
            _item(id="SU-001"),
            _item(id="SU-002", title="second"),
        ]))
        entry = next_self_use_item(path)
        assert entry is not None
        assert entry.id == "SU-001"

    def test_skips_a_consumed_item(self, tmp_path: Path):
        path = _write_queue(tmp_path, _queue_body([
            _item(id="SU-001", consumed_by="F257"),
            _item(id="SU-002", title="second"),
        ]))
        entry = next_self_use_item(path)
        assert entry is not None
        assert entry.id == "SU-002"
        assert [e.id for e in pending_self_use_items(path)] == ["SU-002"]

    def test_all_consumed_answers_none(self, tmp_path: Path):
        path = _write_queue(tmp_path, _queue_body([
            _item(id="SU-001", consumed_by="F257"),
            _item(id="SU-002", title="second", consumed_by="F258"),
        ]))
        assert next_self_use_item(path) is None
        assert pending_self_use_items(path) == ()


class TestLoaderOwnsNoWriter:
    """The module is read-only: loading must not touch the file it reads."""

    def test_loading_leaves_the_shipped_bytes_unchanged(self):
        path = default_self_use_queue_path()
        before = path.read_bytes()
        load_self_use_queue()
        after = path.read_bytes()
        assert after == before

    def test_loading_leaves_a_fixture_queue_unchanged(self, tmp_path: Path):
        path = _write_queue(tmp_path, _queue_body([_item()]))
        before = path.read_bytes()
        next_self_use_item(path)
        assert path.read_bytes() == before

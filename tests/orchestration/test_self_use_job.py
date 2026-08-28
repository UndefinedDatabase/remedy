"""F257 — tests for rendering a self-use queue item onto the real job path.

The load-bearing tests here are
:meth:`TestWriteSelfUseJobFile.test_rendered_bytes_equal_the_curated_bytes`,
which pins that the renderer edits nothing on the way out (S4), and
:meth:`TestPlanNextSelfUseItem.test_exhausted_queue_raises_rather_than_answering_none`,
which pins that exhaustion is raised rather than flowed onward (S6).
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.orchestration.self_use_job import (
    SelfUseJobError,
    plan_next_self_use_item,
    plan_self_use_item,
    write_self_use_job_file,
)
from packages.orchestration.self_use_queue import (
    SelfUseQueueEntry,
    next_self_use_item,
)


@pytest.fixture
def isolate_data_root(tmp_path: Path, monkeypatch) -> Path:
    """Keep ``plan_job_from_file``'s job persistence inside this test's own root."""
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


def _entry(**overrides) -> SelfUseQueueEntry:
    fields = {
        "id": "SU-042",
        "title": "A curated item",
        "why": "Because the track must run on something.",
        "job_markdown": "# Job: Demo\n\n## Task 1\nDo the thing.\n\nAcceptance:\n- it is done\n",
        "consumed_by": "",
    }
    fields.update(overrides)
    return SelfUseQueueEntry(**fields)


def _write_queue(tmp_path: Path, items: list[dict]) -> Path:
    path = tmp_path / "self_use_queue.json"
    body = {
        "schema_version": 1,
        "description": "fixture queue",
        "items": items,
    }
    path.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
    return path


class TestWriteSelfUseJobFile:
    """The renderer writes the curated text and nothing else."""

    def test_rendered_bytes_equal_the_curated_bytes(self, tmp_path: Path):
        entry = _entry()
        path = write_self_use_job_file(entry, tmp_path / "jobs")
        assert path.read_text(encoding="utf-8") == entry.job_markdown

    def test_it_returns_the_id_dot_md_path(self, tmp_path: Path):
        entry = _entry(id="SU-042")
        path = write_self_use_job_file(entry, tmp_path / "jobs")
        assert path.name == "SU-042.md"
        assert path.parent == tmp_path / "jobs"

    def test_it_creates_a_missing_dest_dir(self, tmp_path: Path):
        dest = tmp_path / "not" / "there" / "yet"
        assert not dest.exists()
        path = write_self_use_job_file(_entry(), dest)
        assert dest.is_dir()
        assert path.exists()


class TestPlanSelfUseItem:
    """A curated item reaches the EXISTING job parser, not a second one."""

    def test_the_shipped_item_plans_with_its_title_and_tasks(
        self, tmp_path: Path, isolate_data_root
    ):
        entry = next_self_use_item()
        assert entry is not None, "the shipped queue has no pending item"
        path, plan = plan_self_use_item(entry, tmp_path / "jobs", str(tmp_path))
        assert path.exists()
        assert plan.error == ""
        assert plan.job_title == "Document the Markdown job-file format"
        assert plan.tasks, "a planned self-use job must carry at least one task"

    def test_the_shipped_item_plans_to_exactly_one_task_with_acceptance(
        self, tmp_path: Path, isolate_data_root
    ):
        entry = next_self_use_item()
        _path, plan = plan_self_use_item(entry, tmp_path / "jobs", str(tmp_path))
        assert len(plan.tasks) == 1
        assert plan.tasks[0].task_id == "T001"
        assert plan.tasks[0].acceptance.strip()


class TestPlanNextSelfUseItem:
    """The whole track in one call, and its one deliberate failure."""

    def test_it_returns_the_shipped_pending_item(self, tmp_path: Path, isolate_data_root):
        entry, path, plan = plan_next_self_use_item(tmp_path / "jobs", str(tmp_path))
        assert entry.id == next_self_use_item().id
        assert entry.is_pending
        assert path.name == f"{entry.id}.md"
        assert plan.error == ""

    def test_exhausted_queue_raises_rather_than_answering_none(
        self, tmp_path: Path, isolate_data_root
    ):
        consumed = dict(
            id="SU-001",
            title="Already done",
            why="Every item here carries a consumer.",
            job_markdown="# Job: Demo\n\n## Task 1\nDo it.\n\nAcceptance:\n- done\n",
            consumed_by="F256",
        )
        queue_path = _write_queue(tmp_path, [consumed])
        with pytest.raises(SelfUseJobError) as excinfo:
            plan_next_self_use_item(
                tmp_path / "jobs", str(tmp_path), queue_path=queue_path
            )
        assert str(queue_path) in str(excinfo.value)

"""F258 T001 — tests for the self-use queue's generator.

The load-bearing tests are
:meth:`TestGenerateAndAppendIfEmpty.test_generates_and_appends_when_the_queue_is_empty`,
which proves the one full generate-to-write cycle end to end, and
:meth:`TestLedgerTierSafety.test_a_paragraph_shaped_like_a_heading_raises_rather_than_generating`,
which pins that an unsafe ledger paragraph is refused rather than silently
corrupting the rendered job file's task boundary.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.orchestration.self_use_generator import (
    SelfUseGenerationError,
    append_generated_item,
    default_ledger_path,
    generate_and_append_if_empty,
    generate_self_use_item,
)
from packages.orchestration.self_use_queue import load_self_use_queue, next_self_use_item

_QUEUE_ITEM = {
    "id": "SU-001",
    "title": "A curated item",
    "why": "Because the track must run on something.",
    "job_markdown": "# Job: Demo\n\n## Task 1\nDo the thing.\n\nAcceptance:\n- it is done\n",
    "consumed_by": "",
    "provenance": "operator-curated (fixture)",
}


def _write_queue(tmp_path: Path, items: list[dict], name: str = "self_use_queue.json") -> Path:
    path = tmp_path / name
    body = {"schema_version": 2, "description": "fixture queue", "items": items}
    path.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
    return path


def _queue_item(**overrides) -> dict:
    item = dict(_QUEUE_ITEM)
    item.update(overrides)
    return item


def _write_ledger(tmp_path: Path, paragraphs: list[str], name: str = "live_review.md") -> Path:
    path = tmp_path / name
    path.write_text("\n\n".join(paragraphs) + "\n", encoding="utf-8")
    return path


def _finding(r_id: str, severity: str, body: str = "Some prose describing the defect.") -> str:
    return f"- {r_id} — {severity}, {body}"


@pytest.fixture
def isolate_data_root(tmp_path: Path, monkeypatch) -> Path:
    """Keep job persistence inside this test's own root, for tests that parse a job."""
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


class TestLedgerTierPicksTheOldestEligibleFinding:
    """Tier 1: lowest id, Low or Medium, not already `Done:`."""

    def test_picks_the_lowest_id_among_several_eligible(self, tmp_path: Path):
        ledger = _write_ledger(tmp_path, [
            _finding("R-0100", "Low", "First defect."),
            _finding("R-0050", "Medium", "Second defect, lower id."),
            _finding("R-0200", "Low", "Third defect, higher id."),
        ])
        entry = generate_self_use_item(
            queue_path=_write_queue(tmp_path, [_queue_item(consumed_by="F001")]),
            ledger_path=ledger,
        )
        assert entry is not None
        assert "R-0050" in entry.title
        assert entry.why.startswith("- R-0050 — Medium,")

    def test_high_and_critical_are_never_picked(self, tmp_path: Path):
        ledger = _write_ledger(tmp_path, [
            _finding("R-0010", "Critical", "Would be oldest by id."),
            _finding("R-0020", "High", "Also ineligible."),
            _finding("R-0030", "Low", "The only eligible one."),
        ])
        entry = generate_self_use_item(
            queue_path=_write_queue(tmp_path, [_queue_item(consumed_by="F001")]),
            ledger_path=ledger,
        )
        assert entry is not None
        assert "R-0030" in entry.title

    def test_done_findings_are_skipped(self, tmp_path: Path):
        ledger_path = tmp_path / "live_review.md"
        ledger_path.write_text(
            _finding("R-0010", "Low", "Resolved already.") + "\n\n"
            "Done: R-0010 — repaired.\n\n"
            + _finding("R-0020", "Low", "Still open.") + "\n",
            encoding="utf-8",
        )
        entry = generate_self_use_item(
            queue_path=_write_queue(tmp_path, [_queue_item(consumed_by="F001")]),
            ledger_path=ledger_path,
        )
        assert entry is not None
        assert "R-0020" in entry.title

    def test_no_eligible_finding_answers_none(self, tmp_path: Path):
        ledger = _write_ledger(tmp_path, [_finding("R-0010", "Critical", "Ineligible only.")])
        entry = generate_self_use_item(
            queue_path=_write_queue(tmp_path, [_queue_item(consumed_by="F001")]),
            ledger_path=ledger,
        )
        assert entry is None

    def test_an_empty_ledger_answers_none(self, tmp_path: Path):
        ledger = tmp_path / "live_review.md"
        ledger.write_text("# Ledger\n\nNothing registered yet.\n", encoding="utf-8")
        entry = generate_self_use_item(
            queue_path=_write_queue(tmp_path, [_queue_item(consumed_by="F001")]),
            ledger_path=ledger,
        )
        assert entry is None

    def test_an_unreadable_ledger_raises_rather_than_answering_none(self, tmp_path: Path):
        with pytest.raises(SelfUseGenerationError):
            generate_self_use_item(
                queue_path=_write_queue(tmp_path, [_queue_item(consumed_by="F001")]),
                ledger_path=tmp_path / "absent.md",
            )


class TestLedgerTierSafety:
    """A paragraph that could corrupt the rendered job file is refused, not guessed around."""

    def test_a_paragraph_shaped_like_a_heading_raises_rather_than_generating(self, tmp_path: Path):
        ledger = _write_ledger(tmp_path, [
            "- R-0010 — Low, a defect whose prose happens to include\n"
            "## Task 2\n"
            "a line that looks like a second task heading."
        ])
        with pytest.raises(SelfUseGenerationError):
            generate_self_use_item(
                queue_path=_write_queue(tmp_path, [_queue_item(consumed_by="F001")]),
                ledger_path=ledger,
            )

    def test_a_paragraph_containing_an_acceptance_marker_raises(self, tmp_path: Path):
        ledger = _write_ledger(tmp_path, [
            "- R-0010 — Low, a defect whose prose happens to include\n"
            "Acceptance: something that looks like a real acceptance marker."
        ])
        with pytest.raises(SelfUseGenerationError):
            generate_self_use_item(
                queue_path=_write_queue(tmp_path, [_queue_item(consumed_by="F001")]),
                ledger_path=ledger,
            )

    def test_an_ordinary_paragraph_never_raises(self, tmp_path: Path):
        ledger = _write_ledger(tmp_path, [
            _finding("R-0010", "Low", "Ordinary prose, no heading or acceptance marker.")
        ])
        entry = generate_self_use_item(
            queue_path=_write_queue(tmp_path, [_queue_item(consumed_by="F001")]),
            ledger_path=ledger,
        )
        assert entry is not None


class TestGeneratedIdSequencing:
    """A generated item's id continues the queue's own sequence, never collides."""

    def test_the_generated_id_is_one_past_the_highest_existing(self, tmp_path: Path):
        queue_path = _write_queue(tmp_path, [
            _queue_item(id="SU-001", consumed_by="F001"),
            _queue_item(id="SU-007", consumed_by="F002"),
        ])
        ledger = _write_ledger(tmp_path, [_finding("R-0010", "Low")])
        entry = generate_self_use_item(queue_path=queue_path, ledger_path=ledger)
        assert entry is not None
        assert entry.id == "SU-008"

    def test_the_generated_id_is_su_dash_one_when_the_queue_is_empty(self, tmp_path: Path):
        queue_path = _write_queue(tmp_path, [])
        ledger = _write_ledger(tmp_path, [_finding("R-0010", "Low")])
        entry = generate_self_use_item(queue_path=queue_path, ledger_path=ledger)
        assert entry is not None
        assert entry.id == "SU-001"


class TestGeneratedEntryNeverStartsConsumed:
    def test_consumed_by_is_always_blank(self, tmp_path: Path):
        queue_path = _write_queue(tmp_path, [_queue_item(consumed_by="F001")])
        ledger = _write_ledger(tmp_path, [_finding("R-0010", "Low")])
        entry = generate_self_use_item(queue_path=queue_path, ledger_path=ledger)
        assert entry is not None
        assert entry.consumed_by == ""
        assert entry.is_pending


class TestAppendGeneratedItem:
    """The one writer this feature adds, and only this feature adds."""

    def test_the_item_is_appended_and_loadable(self, tmp_path: Path):
        queue_path = _write_queue(tmp_path, [_queue_item(consumed_by="F001")])
        ledger = _write_ledger(tmp_path, [_finding("R-0010", "Low")])
        entry = generate_self_use_item(queue_path=queue_path, ledger_path=ledger)
        assert entry is not None
        append_generated_item(entry, queue_path)
        loaded = load_self_use_queue(queue_path)
        assert loaded[-1].id == entry.id
        assert loaded[-1].job_markdown == entry.job_markdown
        assert loaded[-1].provenance == entry.provenance

    def test_appending_does_not_touch_earlier_items(self, tmp_path: Path):
        queue_path = _write_queue(tmp_path, [_queue_item(id="SU-001", consumed_by="F001")])
        ledger = _write_ledger(tmp_path, [_finding("R-0010", "Low")])
        entry = generate_self_use_item(queue_path=queue_path, ledger_path=ledger)
        append_generated_item(entry, queue_path)
        loaded = load_self_use_queue(queue_path)
        assert len(loaded) == 2
        assert loaded[0].id == "SU-001"
        assert loaded[0].consumed_by == "F001"

    def test_the_appended_jobmarkdown_parses_as_a_single_task_job(
        self, tmp_path: Path, isolate_data_root
    ):
        from packages.orchestration.pingpong_job import parse_job_file

        queue_path = _write_queue(tmp_path, [_queue_item(consumed_by="F001")])
        ledger = _write_ledger(tmp_path, [_finding("R-0010", "Low", "Ordinary prose.")])
        entry = generate_self_use_item(queue_path=queue_path, ledger_path=ledger)
        job = parse_job_file(entry.job_markdown, str(tmp_path))
        assert job.error == ""
        assert len(job.tasks) == 1
        assert job.tasks[0].task_id == "T001"
        assert job.tasks[0].acceptance.strip()


class TestGenerateAndAppendIfEmpty:
    """The seam a closure round calls: generate AND write, but only when empty."""

    def test_generates_and_appends_when_the_queue_is_empty(self, tmp_path: Path):
        queue_path = _write_queue(tmp_path, [_queue_item(consumed_by="F256")])
        ledger = _write_ledger(tmp_path, [_finding("R-0010", "Low")])
        before = json.loads(queue_path.read_text(encoding="utf-8"))
        assert len(before["items"]) == 1

        result = generate_and_append_if_empty(queue_path, ledger)

        assert result is not None
        after = json.loads(queue_path.read_text(encoding="utf-8"))
        assert len(after["items"]) == 2
        assert after["items"][-1]["id"] == result.id
        assert next_self_use_item(queue_path).id == result.id

    def test_writes_nothing_when_a_pending_item_already_exists(self, tmp_path: Path):
        queue_path = _write_queue(tmp_path, [_queue_item(consumed_by="")])
        ledger = _write_ledger(tmp_path, [_finding("R-0010", "Low")])
        before = queue_path.read_bytes()

        result = generate_and_append_if_empty(queue_path, ledger)

        assert result is None
        assert queue_path.read_bytes() == before

    def test_writes_nothing_when_no_tier_has_a_source(self, tmp_path: Path):
        queue_path = _write_queue(tmp_path, [_queue_item(consumed_by="F256")])
        ledger = tmp_path / "live_review.md"
        ledger.write_text("Nothing registered.\n", encoding="utf-8")
        before = queue_path.read_bytes()

        result = generate_and_append_if_empty(queue_path, ledger)

        assert result is None
        assert queue_path.read_bytes() == before

    def test_calling_twice_in_a_row_generates_only_once(self, tmp_path: Path):
        queue_path = _write_queue(tmp_path, [_queue_item(consumed_by="F256")])
        ledger = _write_ledger(tmp_path, [_finding("R-0010", "Low")])

        first = generate_and_append_if_empty(queue_path, ledger)
        second = generate_and_append_if_empty(queue_path, ledger)

        assert first is not None
        assert second is None
        after = json.loads(queue_path.read_text(encoding="utf-8"))
        assert len(after["items"]) == 2


class TestAgainstTheRealShippedLedger:
    """A minimal check against the real ledger, without pinning WHICH id it names.

    The ledger changes every round, so no test here may assert a specific
    `R-` id — only that the shipped ledger and queue combination behaves
    consistently with the rules above.
    """

    def test_the_real_ledger_does_not_raise(self, tmp_path: Path):
        queue_path = _write_queue(tmp_path, [_queue_item(consumed_by="F001")])
        entry = generate_self_use_item(queue_path=queue_path, ledger_path=default_ledger_path())
        if entry is not None:
            assert entry.id == "SU-002"
            assert entry.title.startswith("Address ledger finding R-")
            assert entry.consumed_by == ""

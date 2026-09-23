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


@pytest.fixture(autouse=True)
def _no_standing_order(monkeypatch, tmp_path):
    """The order tier reads the repository's real order file by default (DECISION F279 D7).

    These tests exercise the other tiers against a fixture queue, so the order is pointed at
    a file that does not exist; a test of the order tier names its own order file.
    """
    from packages.orchestration import self_use_generator

    monkeypatch.setattr(self_use_generator, "default_order_path", lambda: tmp_path / "no-order.md")

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


#: The repair sentence every fixture finding carries unless it is testing the
#: absence of one. Tier 1 only offers a finding whose paragraph NAMES a repair
#: (amend0920-selfuse-real D2), so a fixture without this is a fixture about
#: ineligibility — which is what `fix=""` says out loud.
_FIX_SENTENCE = "FIX: repair it and pin the repair with a test."


def _finding(
    r_id: str,
    severity: str,
    body: str = "Some prose describing the defect.",
    *,
    fix: str = _FIX_SENTENCE,
) -> str:
    tail = f" {fix}" if fix else ""
    return f"- {r_id} — {severity}, {body}{tail}"


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

    def test_a_paragraph_quoting_a_retired_word_is_walked_past(self, tmp_path: Path):
        """R-1015: the paragraph lands in a tracked file the retired-word guard reads.

        The word is built from two literals because this file is held to that guard too.
        """
        retired = "pro" "motion"
        ledger = _write_ledger(tmp_path, [
            _finding("R-0050", "Medium", f"It lists a {retired} result among the types."),
            _finding("R-0100", "Low", "A clean defect."),
        ])
        entry = generate_self_use_item(
            queue_path=_write_queue(tmp_path, [_queue_item(consumed_by="F001")]),
            ledger_path=ledger,
        )
        assert entry is not None
        assert "R-0100" in entry.title
        assert retired not in entry.why and retired not in entry.job_markdown

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

    def test_a_finding_a_consumed_entry_targeted_is_skipped_for_the_next(self, tmp_path: Path):
        """R-0838: the oldest open finding already has a consumed item, so the next one is picked."""
        ledger = _write_ledger(tmp_path, [
            _finding("R-0010", "Low", "Oldest, and already run once."),
            _finding("R-0020", "Low", "Next oldest, never run."),
        ])
        queue_path = _write_queue(tmp_path, [_queue_item(
            consumed_by="F001",
            title="Address ledger finding R-0010",
            provenance="generated (self-use-generator tier 1, ledger scan, R-0010)",
        )])
        entry = generate_self_use_item(queue_path=queue_path, ledger_path=ledger)
        assert entry is not None
        assert entry.title == "Address ledger finding R-0020"
        assert entry.provenance == "generated (self-use-generator tier 1, ledger scan, R-0020)"

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
            # The FIX: sentence is load-bearing here too: see the sibling test.
            "- R-0010 — Low, a defect whose prose happens to include\n"
            "## Task 2\n"
            "a line that looks like a second task heading.\n"
            f"{_FIX_SENTENCE}"
        ])
        with pytest.raises(SelfUseGenerationError):
            generate_self_use_item(
                queue_path=_write_queue(tmp_path, [_queue_item(consumed_by="F001")]),
                ledger_path=ledger,
            )

    def test_a_paragraph_containing_an_acceptance_marker_raises(self, tmp_path: Path):
        ledger = _write_ledger(tmp_path, [
            # Carries a FIX: sentence on purpose — without one the finding is
            # not eligible at all (amend0920-selfuse-real D2) and the safety
            # check this test exists for would never be reached.
            "- R-0010 — Low, a defect whose prose happens to include\n"
            "Acceptance: something that looks like a real acceptance marker.\n"
            f"{_FIX_SENTENCE}"
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

    def test_non_ascii_it_did_not_author_keeps_its_bytes(self, tmp_path: Path):
        """R-0785: an append leaves every byte before the new item as it was."""
        queue_path = tmp_path / "self_use_queue.json"
        body = {
            "schema_version": 2,
            "description": "curated — by hand, § 3 → here",
            "items": [_queue_item(consumed_by="F001", why="An em dash — kept.")],
        }
        queue_path.write_text(json.dumps(body, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        before = queue_path.read_bytes()
        untouched = before[: -len(b"\n  ]\n}\n")]
        ledger = _write_ledger(tmp_path, [_finding("R-0010", "Low")])
        entry = generate_self_use_item(queue_path=queue_path, ledger_path=ledger)
        assert entry is not None
        append_generated_item(entry, queue_path)
        after = queue_path.read_bytes()
        assert after.startswith(untouched)
        assert b"\\u" not in after

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


# ---------------------------------------------------------------------------
# amend0920-selfuse-real Part B.1 — only a finding a builder can actually repair
# ---------------------------------------------------------------------------


class TestOnlyARepairableFindingIsOffered:
    """DECISION amend0920-selfuse-real D2, the evidence: SU-019 to SU-023.

    Five consecutive closures generated an item, ran it, and landed nothing.
    Each was handed a finding whose paragraph named no repair it could make.
    Tier 1 now reads the paragraph for one.
    """

    def test_the_repairable_one_is_picked_over_a_flaky_and_an_already_queued_one(
        self, tmp_path
    ):
        """The amendment's own fixture: three findings, exactly one eligible."""
        ledger = _write_ledger(tmp_path, [
            # Oldest, and already the source of a queue entry — excluded by the
            # dedupe that was already here (R-0838).
            _finding("R-0010", "Low", "An already-queued defect."),
            # Next oldest, and unrepairable: its own text says the failing node
            # was never captured and that it is flaky.
            _finding(
                "R-0020", "Low",
                "THE SWEEP GOES RED ABOUT ONCE IN TWENTY RUNS AND THE FAILING "
                "NODE ID HAS NEVER BEEN CAPTURED. It is flaky.",
                fix="",
            ),
            # The one a builder can finish.
            _finding("R-0030", "Low", "A reader looks for a key that moved."),
        ])
        queue = _write_queue(tmp_path, [_queue_item(
            id="SU-001",
            provenance="generated (self-use-generator tier 1, ledger scan, R-0010)",
            consumed_by="F999",
        )])

        entry = generate_self_use_item(queue_path=queue, ledger_path=ledger)

        assert entry is not None, "one of the three findings is repairable"
        assert "R-0030" in entry.title, (
            f"picked {entry.title!r}; R-0010 is already queued and R-0020 names "
            "no repair it could make"
        )
        assert "R-0020" not in entry.job_markdown
        assert "R-0010" not in entry.job_markdown

    def test_a_paragraph_that_names_no_repair_is_not_offered_at_all(self, tmp_path):
        ledger = _write_ledger(tmp_path, [
            _finding("R-0010", "Low", "A defect nobody said how to repair.", fix=""),
        ])
        queue = _write_queue(tmp_path, [])
        assert generate_self_use_item(queue_path=queue, ledger_path=ledger) is None

    @pytest.mark.parametrize("phrase", [
        "it is flaky under load",
        "the failing node was never captured",
        "the node was never been captured",
        "it reddens once in twenty runs",
        "this waits on the next feature",
        "only the operator can apply it",
    ])
    def test_each_held_phrase_withdraws_a_finding_that_otherwise_qualifies(
        self, tmp_path, phrase
    ):
        """Same paragraph, same FIX sentence — only the held phrase differs."""
        control = _write_ledger(
            tmp_path, [_finding("R-0010", "Low", "A plain defect.")], name="control.md",
        )
        held = _write_ledger(
            tmp_path, [_finding("R-0010", "Low", f"A plain defect, but {phrase}.")],
            name="held.md",
        )
        queue = _write_queue(tmp_path, [])

        assert generate_self_use_item(queue_path=queue, ledger_path=control) is not None, (
            "the control must qualify, or this test proves nothing"
        )
        assert generate_self_use_item(queue_path=queue, ledger_path=held) is None, (
            f"{phrase!r} must withdraw the finding"
        )

    def test_the_headline_case_of_the_ledger_does_not_hide_a_held_phrase(self, tmp_path):
        """This ledger writes headlines in capitals; the filter reads them anyway."""
        ledger = _write_ledger(tmp_path, [
            _finding("R-0010", "Low", "THE NODE ID HAS NEVER BEEN CAPTURED."),
        ])
        queue = _write_queue(tmp_path, [])
        assert generate_self_use_item(queue_path=queue, ledger_path=ledger) is None

    def test_the_dedupe_reads_every_queue_entry_consumed_or_not(self, tmp_path):
        """R-0838's rule, restated as a test: a CONSUMED entry still excludes its finding."""
        ledger = _write_ledger(tmp_path, [
            _finding("R-0010", "Low", "Targeted by a consumed entry."),
            _finding("R-0020", "Low", "Targeted by a pending entry."),
            _finding("R-0030", "Low", "Targeted by nothing."),
        ])
        queue = _write_queue(tmp_path, [
            _queue_item(
                id="SU-001", consumed_by="F900",
                provenance="generated (self-use-generator tier 1, ledger scan, R-0010)",
            ),
            _queue_item(
                id="SU-002", consumed_by="",
                provenance="generated (self-use-generator tier 1, ledger scan, R-0020)",
            ),
        ])
        entry = generate_self_use_item(queue_path=queue, ledger_path=ledger)
        assert entry is not None
        assert "R-0030" in entry.title


class TestOrderTier:
    """T2_F279 T004: the toolchain refresh order, queued verbatim, once every fourteen days."""

    DAY = __import__("datetime").date(2026, 9, 23)

    def _order(self, tmp_path: Path) -> Path:
        from packages.orchestration.self_use_generator import default_order_path

        order = tmp_path / "order.md"
        order.write_text(
            "# Job: Refresh the pinned toolchain\n\nWhy it runs.\n\n## Task 1 — Look\nLook.\n\n"
            "Acceptance:\n- looked\n", encoding="utf-8")
        assert default_order_path() != order
        return order

    def _order_item(self, day: str) -> dict:
        return _queue_item(id="SU-001", consumed_by="F999", provenance=(
            f"generated (self-use-generator order tier, docs/orders/toolchain-refresh.md, {day})"))

    def test_the_real_order_file_is_a_job_the_tier_accepts(self, tmp_path):
        from packages.orchestration.self_use_generator import ORDER_RELATIVE_PATH

        real = Path(__file__).resolve().parents[2] / ORDER_RELATIVE_PATH
        queue_path = _write_queue(tmp_path, [])
        entry = generate_self_use_item(queue_path=queue_path, ledger_path=tmp_path / "none.md",
                                       order_path=real, today=self.DAY)
        assert entry is not None and entry.job_markdown == real.read_text(encoding="utf-8")
        assert entry.title == "Refresh the pinned toolchain"

    def test_an_order_never_queued_comes_before_the_ledger(self, tmp_path):
        queue_path = _write_queue(tmp_path, [])
        ledger = _write_ledger(tmp_path, [f"- R-0001 — Low, a finding. {_FIX_SENTENCE}"])
        order = self._order(tmp_path)
        entry = generate_self_use_item(queue_path=queue_path, ledger_path=ledger, order_path=order,
                                       today=self.DAY)
        assert entry.job_markdown == order.read_text(encoding="utf-8")
        assert entry.why == "Why it runs."
        assert entry.provenance == ("generated (self-use-generator order tier, "
                                    "docs/orders/toolchain-refresh.md, 2026-09-23)")

    def test_within_fourteen_days_the_ledger_tier_answers_instead(self, tmp_path):
        queue_path = _write_queue(tmp_path, [self._order_item("2026-09-10")])
        ledger = _write_ledger(tmp_path, [f"- R-0001 — Low, a finding. {_FIX_SENTENCE}"])
        entry = generate_self_use_item(queue_path=queue_path, ledger_path=ledger,
                                       order_path=self._order(tmp_path), today=self.DAY)
        assert entry.provenance.startswith("generated (self-use-generator tier 1")

    def test_after_fourteen_days_the_order_is_due_again(self, tmp_path):
        queue_path = _write_queue(tmp_path, [self._order_item("2026-09-09")])
        ledger = _write_ledger(tmp_path, [f"- R-0001 — Low, a finding. {_FIX_SENTENCE}"])
        entry = generate_self_use_item(queue_path=queue_path, ledger_path=ledger,
                                       order_path=self._order(tmp_path), today=self.DAY)
        assert entry.id == "SU-002" and "order tier" in entry.provenance

    def test_an_absent_order_file_leaves_the_ledger_tier_in_charge(self, tmp_path):
        queue_path = _write_queue(tmp_path, [])
        ledger = _write_ledger(tmp_path, [f"- R-0001 — Low, a finding. {_FIX_SENTENCE}"])
        entry = generate_self_use_item(queue_path=queue_path, ledger_path=ledger,
                                       order_path=tmp_path / "absent.md", today=self.DAY)
        assert entry.provenance.startswith("generated (self-use-generator tier 1")

    def test_an_order_file_that_is_not_a_job_is_refused(self, tmp_path):
        order = tmp_path / "order.md"
        order.write_text("Just prose, no job title.\n", encoding="utf-8")
        with pytest.raises(SelfUseGenerationError, match="not a job file"):
            generate_self_use_item(queue_path=_write_queue(tmp_path, []), ledger_path=tmp_path / "none.md",
                                   order_path=order, today=self.DAY)

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

from apps.cli.commands.worker_facade_cmd import (
    DoctorCoreReport,
    DoctorWarning,
)
from apps.cli.commands.worker_facade_cmd import (
    doctor_core_report as _real_doctor_core_report,
)
from packages.orchestration.doc_staleness import StaleClaim
from packages.orchestration.doc_staleness import (
    run_staleness_checks as _real_run_staleness_checks,
)
from packages.orchestration.self_use_generator import (
    SelfUseGenerationError,
    append_generated_item,
    default_ledger_path,
    generate_and_append_if_empty,
    generate_self_use_item,
)
from packages.orchestration.self_use_queue import load_self_use_queue, next_self_use_item

#: An empty report, so Tier 3 answers `None` by default and no existing test —
#: none of which is about the doctor — reads the machine's real configuration.
_EMPTY_DOCTOR_REPORT = DoctorCoreReport(
    ready=True, checks=[], blockers=[], warnings=(), dead_commands=[], disk={},
)


@pytest.fixture(autouse=True)
def _no_standing_order(monkeypatch, tmp_path):
    """The order tier reads the repository's real order file by default (DECISION F279 D7).

    These tests exercise the other tiers against a fixture queue, so the order is pointed at
    a file that does not exist; a test of the order tier names its own order file. Tier 2 is
    pointed at an empty claim tuple and Tier 3 at an empty report for the same reason:
    `run_staleness_checks()` and `doctor_core_report()` each read the machine's real repository
    tree and configuration, and a test not ABOUT that tier must not depend on either
    (DECISION F289 D1, D2). Tiers 4 and 5 read source and test files under a root, so the
    root is pointed at a folder that does not exist; a test of either tier names its own
    (DECISION F291 D1).
    """
    from apps.cli.commands import worker_facade_cmd
    from packages.orchestration import doc_staleness, self_use_generator

    monkeypatch.setattr(self_use_generator, "default_order_path", lambda: tmp_path / "no-order.md")
    monkeypatch.setattr(doc_staleness, "run_staleness_checks", lambda *a, **k: ())
    monkeypatch.setattr(worker_facade_cmd, "doctor_core_report", lambda: _EMPTY_DOCTOR_REPORT)
    monkeypatch.setattr(self_use_generator, "default_source_root", lambda: tmp_path / "no-source")

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


class TestTheAcceptanceAsksForTheRepairAlone:
    """R-1058: SU-030's builder met the old Acceptance with a ledger note.

    That Acceptance also accepted "the reviewer records in `.agent/live_review.md`
    why it cannot be — either way the ledger gains a `Done:` line", and the
    builder wrote exactly that paragraph and nothing else. The generated job now
    asks for the repair its finding names, with a red-to-green test, and tells
    the builder to leave `.agent/` alone.
    """

    def _job_markdown(self, tmp_path: Path) -> str:
        ledger = _write_ledger(tmp_path, [_finding("R-0010", "Low", "A clean defect.")])
        entry = generate_self_use_item(
            queue_path=_write_queue(tmp_path, [_queue_item(consumed_by="F001")]),
            ledger_path=ledger,
        )
        assert entry is not None
        return entry.job_markdown

    def test_no_outcome_other_than_the_repair_is_offered(self, tmp_path: Path):
        text = self._job_markdown(tmp_path)
        assert "either way" not in text
        assert "why it cannot be" not in text
        assert "`Done:" not in text

    def test_the_acceptance_asks_for_the_named_repair_with_a_red_to_green_test(
        self, tmp_path: Path
    ):
        acceptance = self._job_markdown(tmp_path).split("\nAcceptance:\n", 1)[1]
        # DECISION amend0926-decisions-selfuse D4 moved this pin to the operator's
        # two sentences; test_the_acceptance_is_the_operators_two_sentences reads them.
        assert acceptance == (
            "- R-0010 is repaired in product code or tests, with a test that fails "
            "without the repair and passes with it.\n"
            "- No file under `.agent/` is changed by this task; if the repair cannot "
            "be finished inside this task, the builder stops and states in its output "
            "what it read and why the repair is out of reach, which the reviewer then "
            "records as a failed run, and the finding's Done line is written only by "
            "a human reviewer, never by this task.\n"
        )

    def test_the_builder_is_told_to_leave_the_record_alone(self, tmp_path: Path):
        body = self._job_markdown(tmp_path).split("\nAcceptance:\n", 1)[0]
        assert "Do not edit any file under `.agent/`" in body
        assert "`.agent/live_review.md` is the reviewer's record" in body

    def test_the_acceptance_is_the_operators_two_sentences(self, tmp_path: Path):
        """Operator amendment amend0926-decisions-selfuse, Part B.3, red proof (4)."""
        text = self._job_markdown(tmp_path)
        acceptance = text.split("\nAcceptance:\n", 1)[1]
        assert "is repaired in product code or tests, with a test that fails without " \
            "the repair and passes with it." in acceptance
        assert "No file under `.agent/` is changed by this task" in acceptance
        assert "the builder stops and states in its output what it read and why the " \
            "repair is out of reach" in acceptance
        assert "records as a failed run" in acceptance
        assert "written only by a human reviewer, never by this task." in acceptance
        assert "either way the ledger gains" not in text


# ---------------------------------------------------------------------------
# F289 T001 — Tier 2: the documentation-staleness catalog (DECISION F289 D2).
# ---------------------------------------------------------------------------


def _write_doc(tmp_path: Path, relpath: str, text: str) -> Path:
    path = tmp_path / relpath
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _stub_doc_claims(monkeypatch, claims=()) -> None:
    """Point Tier 2 at exactly `claims`, in order — never the real repository tree."""
    from packages.orchestration import doc_staleness

    monkeypatch.setattr(doc_staleness, "run_staleness_checks", lambda *a, **k: tuple(claims))


#: One claim, shaped like C01's real stale finding.
_CLAIM_A = StaleClaim(
    "docs_index_guide_registration", "docs/README.md",
    "the Quick-Find Table has no link to `guides/alpha.md`",
    "`docs/guides/alpha.md` ships",
)

#: A second, distinct claim — different check, different document.
_CLAIM_B = StaleClaim(
    "config_cli_table_complete", "docs/guides/remedy-toml-user-guide.md",
    "the CLI commands table never documents `remedy config wipe`",
    "`remedy config wipe` ships",
)


class TestDocStalenessTier:
    """Tier 2, against a STUBBED claim list — DECISION F289 D2, T5_F289.md T001."""

    def test_a_single_claim_becomes_a_tier_2_item(
        self, tmp_path: Path, monkeypatch, isolate_data_root
    ):
        from packages.orchestration.pingpong_job import parse_job_file

        _stub_doc_claims(monkeypatch, [_CLAIM_A])
        ledger = _write_ledger(tmp_path, [])
        queue_path = _write_queue(tmp_path, [])

        entry = generate_self_use_item(queue_path=queue_path, ledger_path=ledger)

        assert entry is not None
        assert entry.id == "SU-001"
        assert entry.title == "Fix stale documentation: docs_index_guide_registration in docs/README.md"
        assert entry.provenance == f"generated (self-use-generator tier 2, doc staleness, {_CLAIM_A.key})"
        assert entry.why == _CLAIM_A.claim
        assert entry.consumed_by == ""
        assert f"Claim: {_CLAIM_A.claim}\n" in entry.job_markdown
        assert f"Shipped truth: {_CLAIM_A.truth}\n" in entry.job_markdown
        assert "do not edit any file under `.agent/`." in entry.job_markdown
        assert (
            "- The staleness check `docs_index_guide_registration` no longer reports "
            "this claim for `docs/README.md`.\n"
        ) in entry.job_markdown
        assert "- No file under `.agent/` is changed by this task.\n" in entry.job_markdown
        assert entry.job_markdown.endswith("- No file under `.agent/` is changed by this task.\n")

        job = parse_job_file(entry.job_markdown, str(tmp_path))
        assert job.error == ""
        assert len(job.tasks) == 1
        assert job.tasks[0].task_id == "T001"
        assert job.tasks[0].acceptance.strip()

    def test_of_two_claims_the_first_is_offered_then_the_second(
        self, tmp_path: Path, monkeypatch
    ):
        _stub_doc_claims(monkeypatch, [_CLAIM_A, _CLAIM_B])
        ledger = _write_ledger(tmp_path, [])
        queue_path = _write_queue(tmp_path, [])

        first = generate_self_use_item(queue_path=queue_path, ledger_path=ledger)
        assert first is not None
        assert _CLAIM_A.document in first.title
        append_generated_item(first, queue_path)

        second = generate_self_use_item(queue_path=queue_path, ledger_path=ledger)
        assert second is not None
        assert _CLAIM_B.document in second.title
        assert "wipe" in second.job_markdown

    def test_a_consumed_entry_targeting_a_key_still_withdraws_it(
        self, tmp_path: Path, monkeypatch
    ):
        """Mirrors R-0838 for Tier 1 and the doctor key for Tier 3."""
        _stub_doc_claims(monkeypatch, [_CLAIM_A, _CLAIM_B])
        ledger = _write_ledger(tmp_path, [])
        queue_path = _write_queue(tmp_path, [_queue_item(
            id="SU-001", consumed_by="F999",
            provenance=f"generated (self-use-generator tier 2, doc staleness, {_CLAIM_A.key})",
        )])

        entry = generate_self_use_item(queue_path=queue_path, ledger_path=ledger)

        assert entry is not None
        assert _CLAIM_B.document in entry.title

    def test_an_eligible_ledger_finding_wins_over_tier_2(self, tmp_path: Path, monkeypatch):
        _stub_doc_claims(monkeypatch, [_CLAIM_A])
        ledger = _write_ledger(tmp_path, [_finding("R-0010", "Low")])
        queue_path = _write_queue(tmp_path, [])

        entry = generate_self_use_item(queue_path=queue_path, ledger_path=ledger)

        assert entry is not None
        assert entry.provenance.startswith("generated (self-use-generator tier 1")

    def test_tier_2_wins_over_a_stubbed_actionable_tier_3_warning(
        self, tmp_path: Path, monkeypatch
    ):
        _stub_doc_claims(monkeypatch, [_CLAIM_A])
        _stub_doctor_report(monkeypatch, [_ACTIONABLE_A])
        ledger = _write_ledger(tmp_path, [])
        queue_path = _write_queue(tmp_path, [])

        entry = generate_self_use_item(queue_path=queue_path, ledger_path=ledger)

        assert entry is not None
        assert entry.provenance.startswith("generated (self-use-generator tier 2")

    def test_a_claim_holding_a_line_break_raises(self, tmp_path: Path, monkeypatch):
        unsafe = StaleClaim(
            "docs_index_guide_registration", "docs/README.md",
            "a claim whose prose happens to include\na line break", "a truth",
        )
        _stub_doc_claims(monkeypatch, [unsafe])
        ledger = _write_ledger(tmp_path, [])
        queue_path = _write_queue(tmp_path, [])

        with pytest.raises(SelfUseGenerationError):
            generate_self_use_item(queue_path=queue_path, ledger_path=ledger)

    def test_a_truth_holding_a_line_break_raises(self, tmp_path: Path, monkeypatch):
        unsafe = StaleClaim(
            "docs_index_guide_registration", "docs/README.md",
            "a claim", "a truth whose prose happens to include\na line break",
        )
        _stub_doc_claims(monkeypatch, [unsafe])
        ledger = _write_ledger(tmp_path, [])
        queue_path = _write_queue(tmp_path, [])

        with pytest.raises(SelfUseGenerationError):
            generate_self_use_item(queue_path=queue_path, ledger_path=ledger)

    def test_an_oserror_from_the_checks_becomes_a_generation_error(
        self, tmp_path: Path, monkeypatch
    ):
        from packages.orchestration import doc_staleness

        def _raise(*args, **kwargs):
            raise OSError("the docs tree could not be read")

        monkeypatch.setattr(doc_staleness, "run_staleness_checks", _raise)
        ledger = _write_ledger(tmp_path, [])
        queue_path = _write_queue(tmp_path, [])

        with pytest.raises(SelfUseGenerationError):
            generate_self_use_item(queue_path=queue_path, ledger_path=ledger)


class TestDocStalenessTierRealChain:
    """No stub: the REAL `run_staleness_checks()`, over a built fixture tree."""

    def test_a_real_missing_quick_find_entry_becomes_a_tier_2_item(
        self, tmp_path: Path, monkeypatch
    ):
        from packages.orchestration import doc_staleness, self_use_generator

        # Undo the autouse fixture's empty-tuple stub: this test is ABOUT the
        # real chain, so it restores the real function before pointing it at a
        # fixture root instead of the repository's own tree.
        monkeypatch.setattr(doc_staleness, "run_staleness_checks", _real_run_staleness_checks)

        _write_doc(tmp_path, "docs/guides/alpha.md", "# Alpha\n")
        _write_doc(tmp_path, "docs/README.md", (
            "# Index\n\n"
            "## Quick-Find Table\n\n"
            "| Keyword | File | Category |\n"
            "|---|---|---|\n\n"
            "## Guides\n\n"
            "| File | Description |\n"
            "|---|---|\n"
            "| [alpha.md](guides/alpha.md) | Alpha guide |\n"
        ))
        monkeypatch.setattr(self_use_generator, "default_docs_root", lambda: tmp_path)
        ledger = _write_ledger(tmp_path, [])
        queue_path = _write_queue(tmp_path, [])

        entry = generate_self_use_item(queue_path=queue_path, ledger_path=ledger)

        assert entry is not None
        assert entry.provenance.startswith(
            "generated (self-use-generator tier 2, doc staleness, docs_index_guide_registration:"
        )
        assert "docs/README.md" in entry.title
        assert "guides/alpha.md" in entry.why


# ---------------------------------------------------------------------------
# F289 T002 — Tier 3: an actionable `remedy doctor core` warning.
# ---------------------------------------------------------------------------


def _stub_doctor_report(monkeypatch, warnings=()) -> DoctorCoreReport:
    """Point Tier 3 at a report holding exactly `warnings`, in order."""
    from apps.cli.commands import worker_facade_cmd

    report = DoctorCoreReport(
        ready=True, checks=[], blockers=[], warnings=tuple(warnings),
        dead_commands=[], disk={},
    )
    monkeypatch.setattr(worker_facade_cmd, "doctor_core_report", lambda: report)
    return report


#: One actionable warning, shaped like the real `dead_builtin_model` kind.
_ACTIONABLE_A = DoctorWarning(
    warning="dead_builtin_model",
    summary="model-a — built-in default; fix: repoint alias",
    detail="model-a is a BUILT-IN default. Fix: repoint the alias that reaches it.",
    subject="model-a",
    repair_path="packages/orchestration/model_aliases.py",
)

#: A second, distinct actionable warning — same kind, different subject.
_ACTIONABLE_B = DoctorWarning(
    warning="dead_builtin_model",
    summary="model-b — built-in default; fix: repoint alias",
    detail="model-b is a BUILT-IN default. Fix: repoint the alias that reaches it.",
    subject="model-b",
    repair_path="packages/orchestration/model_aliases.py",
)

#: A non-actionable warning: no `repair_path`, as `dead_configured_model` carries none.
_NON_ACTIONABLE = DoctorWarning(
    warning="dead_configured_model",
    summary="dead-id — from config key orchestrator.model",
    detail="dead-id is the resolved value of config key orchestrator.model.",
    subject="dead-id",
)


class TestDoctorWarningTier:
    """Tier 3, against a STUBBED report — DECISION F289 D1, T5_F289.md T002."""

    def test_a_single_actionable_warning_becomes_a_tier_3_item(
        self, tmp_path: Path, monkeypatch, isolate_data_root
    ):
        from packages.orchestration.pingpong_job import parse_job_file

        _stub_doctor_report(monkeypatch, [_ACTIONABLE_A])
        ledger = _write_ledger(tmp_path, [])
        queue_path = _write_queue(tmp_path, [])

        entry = generate_self_use_item(queue_path=queue_path, ledger_path=ledger)

        assert entry is not None
        assert entry.id == "SU-001"
        assert entry.title == "Clear doctor warning dead_builtin_model for model-a"
        assert entry.provenance == (
            "generated (self-use-generator tier 3, doctor core, "
            "dead_builtin_model:model-a)"
        )
        assert entry.why == _ACTIONABLE_A.detail
        assert entry.consumed_by == ""
        assert _ACTIONABLE_A.detail in entry.job_markdown
        assert "`packages/orchestration/model_aliases.py`" in entry.job_markdown
        assert "Do not edit any file under `.agent/`." in entry.job_markdown
        assert (
            "- `remedy doctor core --json` no longer lists warning "
            "`dead_builtin_model` for `model-a`.\n"
        ) in entry.job_markdown
        assert "- No file under `.agent/` is changed by this task.\n" in entry.job_markdown
        assert entry.job_markdown.endswith(
            "- No file under `.agent/` is changed by this task.\n"
        )

        job = parse_job_file(entry.job_markdown, str(tmp_path))
        assert job.error == ""
        assert len(job.tasks) == 1
        assert job.tasks[0].task_id == "T001"
        assert job.tasks[0].acceptance.strip()

    def test_only_non_actionable_warnings_answer_none(self, tmp_path: Path, monkeypatch):
        _stub_doctor_report(monkeypatch, [_NON_ACTIONABLE])
        ledger = _write_ledger(tmp_path, [])
        queue_path = _write_queue(tmp_path, [])

        assert generate_self_use_item(queue_path=queue_path, ledger_path=ledger) is None

    def test_of_two_actionable_warnings_the_first_is_offered_then_the_second(
        self, tmp_path: Path, monkeypatch
    ):
        _stub_doctor_report(monkeypatch, [_ACTIONABLE_A, _ACTIONABLE_B])
        ledger = _write_ledger(tmp_path, [])
        queue_path = _write_queue(tmp_path, [])

        first = generate_self_use_item(queue_path=queue_path, ledger_path=ledger)
        assert first is not None
        assert "model-a" in first.title
        append_generated_item(first, queue_path)

        second = generate_self_use_item(queue_path=queue_path, ledger_path=ledger)
        assert second is not None
        assert "model-b" in second.title

    def test_a_consumed_entry_targeting_a_key_still_withdraws_it(
        self, tmp_path: Path, monkeypatch
    ):
        """Mirrors R-0838 for Tier 1: consumed or not, the key is still targeted."""
        _stub_doctor_report(monkeypatch, [_ACTIONABLE_A, _ACTIONABLE_B])
        ledger = _write_ledger(tmp_path, [])
        queue_path = _write_queue(tmp_path, [_queue_item(
            id="SU-001", consumed_by="F999",
            provenance=("generated (self-use-generator tier 3, doctor core, "
                        "dead_builtin_model:model-a)"),
        )])

        entry = generate_self_use_item(queue_path=queue_path, ledger_path=ledger)

        assert entry is not None
        assert "model-b" in entry.title

    def test_an_eligible_ledger_finding_wins_over_tier_3(self, tmp_path: Path, monkeypatch):
        _stub_doctor_report(monkeypatch, [_ACTIONABLE_A])
        ledger = _write_ledger(tmp_path, [_finding("R-0010", "Low")])
        queue_path = _write_queue(tmp_path, [])

        entry = generate_self_use_item(queue_path=queue_path, ledger_path=ledger)

        assert entry is not None
        assert entry.provenance.startswith("generated (self-use-generator tier 1")

    def test_a_detail_shaped_like_a_heading_raises(self, tmp_path: Path, monkeypatch):
        unsafe = DoctorWarning(
            warning="dead_builtin_model", summary="s",
            detail="a defect whose prose happens to include\n## Task 2\na heading line.",
            subject="model-a", repair_path="packages/orchestration/model_aliases.py",
        )
        _stub_doctor_report(monkeypatch, [unsafe])
        ledger = _write_ledger(tmp_path, [])
        queue_path = _write_queue(tmp_path, [])

        with pytest.raises(SelfUseGenerationError):
            generate_self_use_item(queue_path=queue_path, ledger_path=ledger)

    def test_a_detail_containing_an_acceptance_marker_raises(self, tmp_path: Path, monkeypatch):
        unsafe = DoctorWarning(
            warning="dead_builtin_model", summary="s",
            detail="a defect whose prose happens to include\nAcceptance: a marker line.",
            subject="model-a", repair_path="packages/orchestration/model_aliases.py",
        )
        _stub_doctor_report(monkeypatch, [unsafe])
        ledger = _write_ledger(tmp_path, [])
        queue_path = _write_queue(tmp_path, [])

        with pytest.raises(SelfUseGenerationError):
            generate_self_use_item(queue_path=queue_path, ledger_path=ledger)

    def test_a_report_that_raises_propagates_its_own_exception(
        self, tmp_path: Path, monkeypatch
    ):
        from apps.cli.commands import worker_facade_cmd

        class _ReportBoom(RuntimeError):
            pass

        def _raise() -> DoctorCoreReport:
            raise _ReportBoom("the report could not be built")

        monkeypatch.setattr(worker_facade_cmd, "doctor_core_report", _raise)
        ledger = _write_ledger(tmp_path, [])
        queue_path = _write_queue(tmp_path, [])

        with pytest.raises(_ReportBoom):
            generate_self_use_item(queue_path=queue_path, ledger_path=ledger)


class TestDoctorWarningTierRealChain:
    """No stub: the REAL `doctor_core_report()`, only the dead-model loaders patched."""

    def test_a_real_dead_builtin_default_becomes_a_tier_3_item(
        self, tmp_path: Path, monkeypatch
    ):
        import packages.orchestration.dead_model_list as dml
        from apps.cli.commands import worker_facade_cmd
        from packages.orchestration.dead_model_list import DeadModelEntry
        from packages.orchestration.model_aliases import resolve_model_alias

        # Undo the autouse fixture's empty-report stub: this test is ABOUT the
        # real chain, so it restores the real function before patching only
        # the dead-model loaders underneath it.
        monkeypatch.setattr(worker_facade_cmd, "doctor_core_report", _real_doctor_core_report)

        model_id = resolve_model_alias("claude-flagship")
        entries = (DeadModelEntry(id=model_id, reason="retired by the provider", superseded_by=""),)
        monkeypatch.setattr(dml, "load_dead_models", lambda path=None: entries)
        monkeypatch.setattr(dml, "dead_model_ids", lambda path=None: frozenset({model_id}))

        ledger = _write_ledger(tmp_path, [])
        queue_path = _write_queue(tmp_path, [])

        entry = generate_self_use_item(queue_path=queue_path, ledger_path=ledger)

        assert entry is not None
        assert model_id in entry.title
        assert "packages/orchestration/model_aliases.py" in entry.job_markdown
        assert entry.provenance == (
            f"generated (self-use-generator tier 3, doctor core, "
            f"dead_builtin_model:{model_id})"
        )


# ---------------------------------------------------------------------------
# F291 T001 — Tier 4: the excused blind handlers (DECISION F291 D1).
# ---------------------------------------------------------------------------


def _write_source(root: Path, relpath: str, text: str | bytes) -> Path:
    path = root / relpath
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(text, bytes):
        path.write_bytes(text)
    else:
        path.write_text(text, encoding="utf-8")
    return path


def _handler_module(*reasons: str, lead: int = 0) -> str:
    """One `try` block per reason, each ending in an excused handler, after `lead` blank lines.

    With no lead the first handler sits on line 3 and each next one four lines further down.
    """
    body = "\n" * lead
    for reason in reasons:
        body += f"try:\n    pass\nexcept Exception:  # noqa: BLE001 — {reason}\n    pass\n"
    return body


def _mark(reason: str) -> str:
    return f"except Exception:  # noqa: BLE001 — {reason}"


def _consume(queue_path: Path, entry) -> None:
    """The closure round's own edit (DECISION F257 D2): mark `entry` consumed."""
    body = json.loads(queue_path.read_text(encoding="utf-8"))
    for item in body["items"]:
        if item["id"] == entry.id:
            item["consumed_by"] = "F291-test"
    queue_path.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")


def _drain(tmp_path: Path, source_root: Path, limit: int = 10) -> list:
    """Generate, append and consume until the generator answers None; every entry, in order."""
    ledger = _write_ledger(tmp_path, [])
    queue_path = _write_queue(tmp_path, [])
    entries = []
    for _ in range(limit):
        entry = generate_and_append_if_empty(
            queue_path=queue_path, ledger_path=ledger, source_root=source_root,
        )
        if entry is None:
            return entries
        entries.append(entry)
        _consume(queue_path, entry)
    raise AssertionError(f"the generator was still answering after {limit} requests")


class TestExcusedHandlerTier:
    """Tier 4, against a FIXTURE source tree — T5_F291.md T001, DECISION F291 D1."""

    def _tree(self, tmp_path: Path) -> Path:
        root = tmp_path / "src"
        _write_source(root, "packages/zeta.py", _handler_module("z"))
        _write_source(root, "apps/alpha.py", _handler_module("a1", "a2"))
        _write_source(root, "scripts/beta.py", _handler_module("b"))
        return root

    def test_the_first_mark_in_path_then_line_order_is_offered(self, tmp_path: Path):
        root = self._tree(tmp_path)
        entry = generate_self_use_item(
            queue_path=_write_queue(tmp_path, []), ledger_path=_write_ledger(tmp_path, []),
            source_root=root,
        )
        assert entry is not None
        assert entry.id == "SU-001"
        assert entry.consumed_by == ""
        assert entry.title == "Narrow the excused handler at apps/alpha.py:3"
        assert entry.why == _mark("a1")
        assert entry.provenance == (
            "generated (self-use-generator tier 4, excused handler, "
            f"apps/alpha.py:1:{_mark('a1')})"
        )

    def test_the_job_asks_for_the_narrowing_and_the_ratchet_in_one_change(self, tmp_path: Path):
        root = self._tree(tmp_path)
        entry = generate_self_use_item(
            queue_path=_write_queue(tmp_path, []), ledger_path=_write_ledger(tmp_path, []),
            source_root=root,
        )
        text = entry.job_markdown
        assert text.startswith("# Job: Narrow the excused handler at apps/alpha.py:3\n\n## Task 1\n")
        assert text.count("## Task 1") == 1 and text.count("## ") == 1
        assert text.count("Acceptance:") == 1
        task, acceptance = text.split("Acceptance:\n")
        assert "Line 3 of `apps/alpha.py`" in task
        assert f"\n    {_mark('a1')}\n" in task
        assert "lower `MAX_EXCUSED` in `tests/test_ble001_ratchet.py` by one" in task
        assert "do not edit any file under `.agent/`" in task
        assert "`python3 -m ruff check apps/alpha.py` reports nothing" in acceptance
        assert "`python3 -m pytest -q tests/test_ble001_ratchet.py` passes" in acceptance
        assert "- No file under `.agent/` is changed by this task.\n" in acceptance

    def test_a_targeted_mark_is_never_offered_again(self, tmp_path: Path):
        entries = _drain(tmp_path, self._tree(tmp_path))
        assert [e.title for e in entries] == [
            "Narrow the excused handler at apps/alpha.py:3",
            "Narrow the excused handler at apps/alpha.py:7",
            "Narrow the excused handler at packages/zeta.py:3",
            "Narrow the excused handler at scripts/beta.py:3",
        ]
        assert [e.id for e in entries] == ["SU-001", "SU-002", "SU-003", "SU-004"]
        assert len({e.provenance for e in entries}) == 4

    def test_a_moved_mark_keeps_its_key(self, tmp_path: Path):
        root = self._tree(tmp_path)
        ledger = _write_ledger(tmp_path, [])
        queue_path = _write_queue(tmp_path, [])
        first = generate_and_append_if_empty(queue_path=queue_path, ledger_path=ledger, source_root=root)
        _consume(queue_path, first)

        # An unrelated edit moves both handlers of the file five lines down.
        _write_source(root, "apps/alpha.py", _handler_module("a1", "a2", lead=5))
        second = generate_self_use_item(queue_path=queue_path, ledger_path=ledger, source_root=root)

        assert first.why == _mark("a1")
        assert second.why == _mark("a2")
        assert second.title == "Narrow the excused handler at apps/alpha.py:12"

    def test_identical_handlers_in_one_file_are_offered_one_by_one(self, tmp_path: Path):
        root = tmp_path / "src"
        _write_source(root, "packages/twin.py", _handler_module("same", "same"))
        entries = _drain(tmp_path, root)
        assert [e.title for e in entries] == [
            "Narrow the excused handler at packages/twin.py:3",
            "Narrow the excused handler at packages/twin.py:7",
        ]
        assert [e.provenance for e in entries] == [
            f"generated (self-use-generator tier 4, excused handler, packages/twin.py:1:{_mark('same')})",
            f"generated (self-use-generator tier 4, excused handler, packages/twin.py:2:{_mark('same')})",
        ]

    def test_only_the_ratchets_roots_are_read(self, tmp_path: Path):
        root = tmp_path / "src"
        for relpath in ("tests/test_x.py", "docs/y.py", "tools/z.py", "packages/notes.txt"):
            _write_source(root, relpath, _handler_module("outside"))
        assert _drain(tmp_path, root) == []

    def test_a_mark_quoting_a_retired_word_is_walked_past(self, tmp_path: Path):
        """R-1015: the mark's line lands in a tracked file the retired-word guard reads."""
        retired = "pro" "motion"
        root = tmp_path / "src"
        _write_source(root, "apps/alpha.py", _handler_module(f"a {retired} fallback"))
        _write_source(root, "packages/zeta.py", _handler_module("z"))
        entries = _drain(tmp_path, root)
        assert [e.title for e in entries] == ["Narrow the excused handler at packages/zeta.py:3"]

    def test_an_undecodable_source_file_raises(self, tmp_path: Path):
        root = tmp_path / "src"
        _write_source(root, "packages/bad.py", b"x = '\xff\xfe'\n")
        with pytest.raises(SelfUseGenerationError):
            generate_self_use_item(
                queue_path=_write_queue(tmp_path, []), ledger_path=_write_ledger(tmp_path, []),
                source_root=root,
            )

    def test_tier_3_wins_over_tier_4(self, tmp_path: Path, monkeypatch):
        _stub_doctor_report(monkeypatch, [_ACTIONABLE_A])
        entry = generate_self_use_item(
            queue_path=_write_queue(tmp_path, []), ledger_path=_write_ledger(tmp_path, []),
            source_root=self._tree(tmp_path),
        )
        assert entry.provenance.startswith("generated (self-use-generator tier 3")

    def test_tier_4_wins_over_tier_5(self, tmp_path: Path):
        root = self._tree(tmp_path)
        _write_source(root, "packages/lonely.py", "def run():\n    return 1\n")
        entry = generate_self_use_item(
            queue_path=_write_queue(tmp_path, []), ledger_path=_write_ledger(tmp_path, []),
            source_root=root,
        )
        assert entry.provenance.startswith("generated (self-use-generator tier 4")


class TestExcusedHandlerTierReadsWhatTheRatchetCounts:
    """The item a tier 4 job clears is always one `MAX_EXCUSED` counted (DECISION F291 D1)."""

    def test_the_roots_and_the_mark_are_the_ratchets(self):
        from packages.orchestration.self_use_generator import (
            EXCUSED_HANDLER_MARK,
            EXCUSED_HANDLER_ROOTS,
            RATCHET_TEST_PATH,
        )
        from tests.test_ble001_ratchet import MARK, SCANNED_ROOTS

        assert EXCUSED_HANDLER_ROOTS == SCANNED_ROOTS
        assert (EXCUSED_HANDLER_MARK.pattern, EXCUSED_HANDLER_MARK.flags) == (MARK.pattern, MARK.flags)
        assert (Path(__file__).resolve().parents[2] / RATCHET_TEST_PATH).is_file()

    def test_the_generator_spells_no_mark_of_its_own(self):
        from packages.orchestration import self_use_generator
        from packages.orchestration.self_use_generator import EXCUSE_MARK_WORDS
        from tests.test_ble001_ratchet import MARK

        source = Path(self_use_generator.__file__).read_text(encoding="utf-8")
        assert [line for line in source.splitlines() if MARK.search(line)] == []
        assert MARK.search(f"# {EXCUSE_MARK_WORDS} — a reason")

    def test_the_real_tree_offers_the_ratchets_first_mark(self, tmp_path: Path, monkeypatch):
        from packages.orchestration import self_use_generator
        from tests.test_ble001_ratchet import _marks

        # Undo the autouse fixture's missing root: this test is ABOUT the real tree.
        real_root = Path(self_use_generator.__file__).resolve().parents[2]
        monkeypatch.setattr(self_use_generator, "default_source_root", lambda: real_root)

        entry = generate_self_use_item(
            queue_path=_write_queue(tmp_path, []), ledger_path=_write_ledger(tmp_path, []),
        )
        path, number, _rest = min(_marks(), key=lambda mark: (mark[0], mark[1]))
        assert entry is not None
        assert entry.title == f"Narrow the excused handler at {path}:{number}"


# ---------------------------------------------------------------------------
# F291 T002 — Tier 5: the test-less modules (DECISION F291 D1).
# ---------------------------------------------------------------------------


class TestUntestedModuleTier:
    """Tier 5, against a FIXTURE tree — T5_F291.md T002, DECISION F291 D1."""

    def _tree(self, tmp_path: Path) -> Path:
        root = tmp_path / "src"
        _write_source(root, "packages/pkg/__init__.py", "def helper():\n    return 0\n")
        _write_source(root, "packages/pkg/alpha.py",
                      "def run():\n    return 1\n\n\ndef _inner():\n    return 2\n\n\nclass Shape:\n    pass\n")
        _write_source(root, "packages/pkg/beta.py", "def go():\n    return 3\n")
        _write_source(root, "packages/pkg/empty.py", "VALUE = 1\n")
        _write_source(root, "apps/cli/commands/gamma_cmd.py", "def _cmd_gamma(args):\n    return None\n")
        _write_source(root, "apps/ui/delta.py", "def shown():\n    return 4\n")
        _write_source(root, "tests/test_beta.py", "from packages.pkg import beta\n")
        return root

    def test_the_first_untested_module_is_offered(self, tmp_path: Path):
        entry = generate_self_use_item(
            queue_path=_write_queue(tmp_path, []), ledger_path=_write_ledger(tmp_path, []),
            source_root=self._tree(tmp_path),
        )
        assert entry is not None
        assert entry.id == "SU-001"
        assert entry.consumed_by == ""
        assert entry.title == "Write the first tests for packages/pkg/alpha.py"
        assert entry.why == "No file under `tests/` imports `packages.pkg.alpha`."
        assert entry.provenance == (
            "generated (self-use-generator tier 5, untested module, packages/pkg/alpha.py)"
        )

    def test_the_job_names_the_module_its_test_file_and_its_names(self, tmp_path: Path):
        entry = generate_self_use_item(
            queue_path=_write_queue(tmp_path, []), ledger_path=_write_ledger(tmp_path, []),
            source_root=self._tree(tmp_path),
        )
        text = entry.job_markdown
        assert text.startswith("# Job: Write the first tests for packages/pkg/alpha.py\n\n## Task 1\n")
        assert text.count("## ") == 1 and text.count("Acceptance:") == 1
        task, acceptance = text.split("Acceptance:\n")
        assert "No file under `tests/` imports `packages.pkg.alpha`" in task
        assert "The names to test are `run`, `Shape`.\n" in task
        assert "`_inner`" not in text
        assert "`test_alpha.py`" in task
        assert "Change no production code" in task
        assert "do not edit any file under `.agent/`" in task
        assert "- A test file under `tests/` imports `packages.pkg.alpha`, and pytest passes on it.\n" in acceptance
        assert "- Each of `run`, `Shape` is exercised by at least one of the new tests.\n" in acceptance
        assert "- No file under `.agent/` is changed by this task.\n" in acceptance

    @pytest.mark.parametrize("relpath, text", [
        ("tests/test_a.py", "import packages.pkg.alpha\n"),
        ("tests/test_a.py", "import packages.pkg.alpha as alpha_module\n"),
        ("tests/test_a.py", "from packages.pkg import alpha\n"),
        ("tests/test_a.py", "from packages.pkg.alpha import run\n"),
        ("tests/deep/er/test_a.py", "def test_it():\n    from packages.pkg import alpha\n"),
    ], ids=["import", "import-as", "from-package", "from-module", "nested-and-local"])
    def test_every_import_form_counts(self, tmp_path: Path, relpath: str, text: str):
        root = self._tree(tmp_path)
        _write_source(root, relpath, text)
        entry = generate_self_use_item(
            queue_path=_write_queue(tmp_path, []), ledger_path=_write_ledger(tmp_path, []),
            source_root=root,
        )
        assert entry.title == "Write the first tests for apps/cli/commands/gamma_cmd.py"

    def test_a_module_with_only_private_names_offers_them(self, tmp_path: Path):
        entries = _drain(tmp_path, self._tree(tmp_path))
        gamma = entries[1]
        assert gamma.title == "Write the first tests for apps/cli/commands/gamma_cmd.py"
        assert "The names to test are `_cmd_gamma`.\n" in gamma.job_markdown
        assert "`test_gamma_cmd.py`" in gamma.job_markdown

    def test_never_an_init_a_nameless_module_or_one_outside_the_roots(self, tmp_path: Path):
        entries = _drain(tmp_path, self._tree(tmp_path))
        assert [e.provenance for e in entries] == [
            "generated (self-use-generator tier 5, untested module, packages/pkg/alpha.py)",
            "generated (self-use-generator tier 5, untested module, apps/cli/commands/gamma_cmd.py)",
        ]

    def test_an_unparseable_test_file_raises(self, tmp_path: Path):
        root = self._tree(tmp_path)
        _write_source(root, "tests/test_broken.py", "def (\n")
        with pytest.raises(SelfUseGenerationError):
            generate_self_use_item(
                queue_path=_write_queue(tmp_path, []), ledger_path=_write_ledger(tmp_path, []),
                source_root=root,
            )

    def test_a_test_file_that_vanished_is_skipped(self, tmp_path: Path):
        """R-1114, DECISION F291 D4: a file gone between the listing and the read is skipped."""
        root = self._tree(tmp_path)
        (root / "tests" / "test_gone.py").symlink_to(tmp_path / "missing.py")
        entry = generate_self_use_item(
            queue_path=_write_queue(tmp_path, []), ledger_path=_write_ledger(tmp_path, []),
            source_root=root,
        )
        assert entry.title == "Write the first tests for packages/pkg/alpha.py"

    def test_any_other_unreadable_test_file_still_raises(self, tmp_path: Path):
        """DECISION F291 D4: only a vanished file is skipped; a directory named like one is not."""
        root = self._tree(tmp_path)
        (root / "tests" / "test_folder.py").mkdir()
        with pytest.raises(SelfUseGenerationError):
            generate_self_use_item(
                queue_path=_write_queue(tmp_path, []), ledger_path=_write_ledger(tmp_path, []),
                source_root=root,
            )


class TestUntestedModuleTierRealChain:
    """Tier 5 against the real tree, read back by a second, independent reader."""

    def test_the_real_tree_offers_a_module_no_test_imports(self, tmp_path: Path, monkeypatch):
        import re

        from packages.orchestration import self_use_generator

        real_root = Path(self_use_generator.__file__).resolve().parents[2]
        monkeypatch.setattr(self_use_generator, "default_source_root", lambda: real_root)
        # Tier 4 always has an item on the real tree; with no root to read it answers None.
        monkeypatch.setattr(self_use_generator, "EXCUSED_HANDLER_ROOTS", ())

        entry = generate_self_use_item(
            queue_path=_write_queue(tmp_path, []), ledger_path=_write_ledger(tmp_path, []),
        )
        assert entry is not None
        assert entry.provenance.startswith("generated (self-use-generator tier 5, untested module, ")
        relpath = entry.provenance.rsplit(", ", 1)[1].rstrip(")")
        assert relpath.startswith(("packages/", "apps/cli/")) and relpath.endswith(".py")
        assert (real_root / relpath).is_file() and not relpath.endswith("__init__.py")

        dotted = relpath[:-3].replace("/", ".")
        parent, stem = dotted.rsplit(".", 1)
        importer = re.compile(
            rf"^\s*(?:import\s+{re.escape(dotted)}\b|from\s+{re.escape(dotted)}\s+import\b"
            rf"|from\s+{re.escape(parent)}\s+import\s+.*\b{re.escape(stem)}\b)",
            re.M,
        )
        def _source(path: Path) -> str:
            # R-1114: a temporary module another test removed while this ran is gone.
            try:
                return path.read_text(encoding="utf-8")
            except FileNotFoundError:
                return ""

        hits = [
            path.relative_to(real_root).as_posix()
            for path in sorted((real_root / "tests").rglob("*.py"))
            if importer.search(_source(path))
        ]
        assert hits == []


# ---------------------------------------------------------------------------
# F291 T003 — the requirement, at the generator: three requests, three items.
# ---------------------------------------------------------------------------


class TestThreeRequestsOnAQueueExhaustedForTiersZeroToThree:
    """T5_F291.md T003: with tiers 0 to 3 dry, three requests give three different items."""

    def test_three_requests_three_items_then_none(self, tmp_path: Path):
        root = tmp_path / "src"
        _write_source(root, "packages/alpha.py", _handler_module("a1", "a2") + "\n\ndef run():\n    return 1\n")
        entries = _drain(tmp_path, root)
        assert [e.id for e in entries] == ["SU-001", "SU-002", "SU-003"]
        assert [e.provenance.split(",")[0] for e in entries] == [
            "generated (self-use-generator tier 4",
            "generated (self-use-generator tier 4",
            "generated (self-use-generator tier 5",
        ]
        assert len({e.provenance for e in entries}) == 3

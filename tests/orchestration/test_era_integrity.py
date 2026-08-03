"""F070 T002 — the era fixture corpus and its detectors.

The external-orchestration era (docs/agents/split_workflow.md, in production
since 2026-07-23) produced a catalogue of ways a handback can be wrong while
looking right. Each class below is a MINIMAL REPRODUCTION extracted from a real
finding in this repository's history; every fixture cites the commit it came
from, so a reader can go check that the reproduction is faithful:

  * R-0141 / R-0143 / R-0145 — incomplete handback accounting (2db44f95, add00a21)
  * R-0144 — a verdict the reviewer never authored (a00445af)
  * R-0146 — an advertised flag silently dropped (269195fe)
  * R-0147 — a proof of its own premise passed off as verification (15c7ebe0)
  * R-0148 — authored text corrupted in transport and applied verbatim (d3f929ce)

Each class gets a detector test here and a loop test in
``test_orchestrator_loop.py``: this file proves the defect is FLAGGED, that one
proves the loop REFUSES TO ADVANCE on it.

A clean handback must stay clean — a detector that fires on everything is a
detector nobody keeps — so every class also has its repaired twin.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.orchestration.era_integrity import (
    DEFECT_CORRUPTED_AUTHORED_TEXT,
    DEFECT_DROPPED_FLAG,
    DEFECT_FINDING_CLASSES,
    DEFECT_INCOMPLETE_ACCOUNTING,
    DEFECT_SELF_AUTHORED_VERDICT,
    DEFECT_SELF_CONSISTENCY_PROOF,
    AuthoredText,
    Handback,
    ProofClaim,
    authored_text_digest,
    detect_era_defects,
    render_defects,
)

FIXTURES = Path(__file__).parent / "fixtures" / "era"

#: fixture file -> the defect kind it must produce.
CORPUS: dict[str, str] = {
    "r0141_r0143_r0145_incomplete_accounting.json": DEFECT_INCOMPLETE_ACCOUNTING,
    "r0144_self_authored_verdict.json": DEFECT_SELF_AUTHORED_VERDICT,
    "r0146_dropped_flag.json": DEFECT_DROPPED_FLAG,
    "r0147_self_consistency_proof.json": DEFECT_SELF_CONSISTENCY_PROOF,
    "r0148_corrupted_authored_text.json": DEFECT_CORRUPTED_AUTHORED_TEXT,
}


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def fixture_handback(name: str) -> Handback:
    return Handback.from_json(load_fixture(name)["handback"])


# ---------------------------------------------------------------------------
# the corpus itself
# ---------------------------------------------------------------------------


class TestTheCorpus:
    def test_every_finding_class_has_a_fixture(self):
        kinds = {CORPUS[name] for name in CORPUS}
        assert kinds == set(DEFECT_FINDING_CLASSES)

    @pytest.mark.parametrize("name", sorted(CORPUS))
    def test_every_fixture_cites_the_commit_it_was_extracted_from(self, name):
        body = load_fixture(name)
        assert body["source"], f"{name} does not say where it came from"
        assert body["finding_class"]
        assert body["why"]

    @pytest.mark.parametrize("name", sorted(CORPUS))
    def test_every_fixture_parses_as_a_handback(self, name):
        assert isinstance(fixture_handback(name), Handback)


# ---------------------------------------------------------------------------
# one detector test per class
# ---------------------------------------------------------------------------


class TestOneDetectorPerFindingClass:
    @pytest.mark.parametrize("name,kind", sorted(CORPUS.items()))
    def test_the_fixture_is_flagged_with_its_own_class(self, name, kind):
        defects = detect_era_defects(fixture_handback(name))
        assert defects, f"{name} was not flagged at all"
        kinds = {d.kind for d in defects}
        assert kind in kinds, f"{name} flagged as {kinds}, expected {kind}"

    @pytest.mark.parametrize("name,kind", sorted(CORPUS.items()))
    def test_the_flag_names_the_precedent(self, name, kind):
        defect = next(d for d in detect_era_defects(fixture_handback(name))
                      if d.kind == kind)
        assert defect.to_json()["finding_class"] == DEFECT_FINDING_CLASSES[kind]
        assert defect.detail

    def test_a_clean_handback_is_not_flagged(self):
        assert detect_era_defects(Handback(
            commits=("abc1234",),
            reported_commits=("abc1234",),
            changed_files_tables={"abc1234": ("packages/x.py",)},
            external_actions=("created PR #1",),
            reported_actions=("created PR #1",),
            verdict_text="PASS", verdict_author="reviewer",
            advertised_flags=("--dry-run",), passed_flags=("--dry-run",),
        )) == []

    def test_an_empty_handback_is_not_flagged(self):
        assert detect_era_defects(Handback()) == []


# ---------------------------------------------------------------------------
# the detectors, per class, including the repaired twin
# ---------------------------------------------------------------------------


class TestIncompleteAccounting:
    """R-0141 / R-0143 / R-0145."""

    def test_a_commit_inside_the_range_missing_from_the_tables(self):
        defects = detect_era_defects(Handback(
            commits=("aaa", "bbb"), reported_commits=("aaa",),
            changed_files_tables={"aaa": ("x.py",)}))
        assert [d.kind for d in defects] == [DEFECT_INCOMPLETE_ACCOUNTING]
        assert "bbb" in defects[0].detail

    def test_a_reported_commit_with_no_changed_files_table(self):
        defects = detect_era_defects(Handback(
            commits=("aaa",), reported_commits=("aaa",),
            changed_files_tables={"aaa": ()}))
        assert defects and "no changed-files table" in defects[0].detail

    def test_an_external_action_taken_but_never_reported(self):
        defects = detect_era_defects(Handback(
            external_actions=("created PR #152",)))
        assert defects and "never" in defects[0].detail

    def test_the_repaired_handback_is_clean(self):
        assert detect_era_defects(Handback(
            commits=("aaa", "bbb"), reported_commits=("aaa", "bbb"),
            changed_files_tables={"aaa": ("x.py",), "bbb": ("y.py",)},
            external_actions=("created PR #152",),
            reported_actions=("created PR #152",))) == []


class TestSelfAuthoredVerdict:
    """R-0144 — the same class as the builder-self-merge rule."""

    def test_a_verdict_the_worker_wrote_is_flagged(self):
        defects = detect_era_defects(Handback(
            verdict_text="Integration gate: PASS.", verdict_author="worker"))
        assert any(d.kind == DEFECT_SELF_AUTHORED_VERDICT for d in defects)

    def test_a_verdict_while_the_review_is_pending_is_flagged(self):
        defects = detect_era_defects(Handback(
            verdict_text="PASS", verdict_author="reviewer",
            review_pending=True))
        assert any("still pending" in d.detail for d in defects)

    def test_no_verdict_at_all_is_not_a_defect(self):
        assert detect_era_defects(Handback(verdict_author="worker")) == []

    def test_a_reviewer_authored_verdict_is_clean(self):
        assert detect_era_defects(Handback(
            verdict_text="PASS", verdict_author="reviewer")) == []


class TestDroppedFlag:
    """R-0146 — a preview request that silently executes for real."""

    def test_an_advertised_flag_that_is_never_passed_through(self):
        defects = detect_era_defects(Handback(
            advertised_flags=("--dry-run", "--checkpoint"),
            passed_flags=("--checkpoint",)))
        assert [d.kind for d in defects] == [DEFECT_DROPPED_FLAG]
        assert "--dry-run" in defects[0].detail

    def test_passing_every_advertised_flag_is_clean(self):
        assert detect_era_defects(Handback(
            advertised_flags=("--dry-run",),
            passed_flags=("--dry-run", "--json"))) == []


class TestSelfConsistencyProof:
    """R-0147 — a proof asserting byte-identity over a missing sentence."""

    def test_an_assertion_that_does_not_survive_re_checking(self):
        defects = detect_era_defects(Handback(proofs=(
            ProofClaim(name="PROOF 1", needle="the full sentence.",
                       authoritative="the full", asserted=True),)))
        assert [d.kind for d in defects] == [DEFECT_SELF_CONSISTENCY_PROOF]
        assert "PROOF 1" in defects[0].detail

    def test_a_proof_checked_against_a_different_text_is_named_as_such(self):
        defects = detect_era_defects(Handback(proofs=(
            ProofClaim(name="PROOF 1", needle="sentence",
                       authoritative="no match here",
                       compared_against="a sentence", asserted=True),)))
        assert "compared against a different text" in defects[0].detail

    def test_an_honest_negative_assertion_is_clean(self):
        assert detect_era_defects(Handback(proofs=(
            ProofClaim(name="PROOF 1", needle="absent",
                       authoritative="present", asserted=False),))) == []

    def test_an_honest_positive_assertion_is_clean(self):
        assert detect_era_defects(Handback(proofs=(
            ProofClaim(name="PROOF 1", needle="present",
                       authoritative="it is present here",
                       asserted=True),))) == []


class TestCorruptedAuthoredText:
    """R-0148 — hash on write, verify on read."""

    def test_text_that_does_not_match_its_declared_digest(self):
        authored = "| a | b |"
        defects = detect_era_defects(Handback(authored_texts=(
            AuthoredText(name="phv1-r1-10",
                         declared_sha256=authored_text_digest(authored),
                         applied_text="| a |\nb |"),)))
        assert [d.kind for d in defects] == [DEFECT_CORRUPTED_AUTHORED_TEXT]
        assert "phv1-r1-10" in defects[0].detail

    def test_text_with_no_declared_digest_cannot_be_verified(self):
        defects = detect_era_defects(Handback(authored_texts=(
            AuthoredText(name="x", declared_sha256="", applied_text="y"),)))
        assert defects and "no declared digest" in defects[0].detail

    def test_intact_text_is_clean(self):
        authored = "| a | b |"
        assert detect_era_defects(Handback(authored_texts=(
            AuthoredText(name="x",
                         declared_sha256=authored_text_digest(authored),
                         applied_text=authored),))) == []

    def test_the_digest_is_the_mechanism_not_a_wrap_guard(self):
        """The 2026-07-27 note: the wrap-guard rationale is obsolete internally.

        A text that gained an innocuous trailing newline is flagged just the
        same, because the mechanism is byte identity and not a shape heuristic
        that would have to guess which differences are innocuous.
        """
        authored = "| a | b |"
        defects = detect_era_defects(Handback(authored_texts=(
            AuthoredText(name="x",
                         declared_sha256=authored_text_digest(authored),
                         applied_text=authored + "\n"),)))
        assert [d.kind for d in defects] == [DEFECT_CORRUPTED_AUTHORED_TEXT]


class TestRendering:
    def test_the_reason_names_every_class_it_found(self):
        text = render_defects(detect_era_defects(
            fixture_handback("r0141_r0143_r0145_incomplete_accounting.json")))
        assert "R-0141/R-0143/R-0145" in text
        assert "cd13645" in text

    def test_nothing_found_renders_empty(self):
        assert render_defects([]) == ""

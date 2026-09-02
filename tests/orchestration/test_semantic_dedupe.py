"""Tests for the per-session sent-hash index (F109 T001a).

The scope rule of the feature binds every case below: RESUMED SESSION ONLY,
PROVEN SENDS ONLY. So the tests are mostly about what the index REFUSES to
remember — an unsuccessful call, a call with no session id — because a hash the
index holds without proof is a segment the composition hook would later replace
with a marker the model never received.

Hermetic throughout: no network and no sleep anywhere. The unit tests are also
PURE — no tmp_path, no provider — while the final class deliberately drives the
real ping-pong loop against ``FakeProvider`` in a tmp_path (F109 T001b-ii). The
manifest in the first case is built through the REAL producer in
``prompt_segments`` so
the index is pinned against the manifest shape that actually ships rather than
against a hand-made dictionary.
"""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from packages.orchestration.pingpong_loop import run_pingpong
from packages.orchestration.pingpong_provider import FakeProvider
from packages.orchestration.prompt_segments import (
    PromptSegmentRegistry,
    SegmentStabilityRank,
    compose_prompt_segments,
)
from packages.orchestration.session_sent_index import (
    DEDUPE_MIN_SEGMENT_CHARS,
    SessionSentIndex,
    SessionSentIndexError,
    dedupe_marker_for_segment,
    invalidate_on_resume_fallback,
    record_finalized_call,
    session_id_of_finalized_call,
    session_sent_index_from_evidence,
    should_dedupe_segment,
)


def _real_manifest_rows(
    *specs: tuple[str, SegmentStabilityRank, str],
) -> list[dict[str, str | int]]:
    """Manifest rows from the REAL producer, not a hand-made dictionary."""
    registry = PromptSegmentRegistry()
    for name, rank, text in specs:
        registry.register(name, rank, text)
    composed = compose_prompt_segments(registry.registered_segments())
    return composed.manifest_as_dicts()


def _sample_rows() -> list[dict[str, str | int]]:
    return _real_manifest_rows(
        ("system", SegmentStabilityRank.SYSTEM, "you are a builder"),
        ("dossier", SegmentStabilityRank.DOSSIER, "the repo is remedy"),
        ("task", SegmentStabilityRank.TASK, "implement the index"),
    )


def _digests(rows: list[dict[str, str | int]]) -> list[str]:
    return [str(row["sha256"]) for row in rows]


# ---------------------------------------------------------------------------
# 1, 7: what a proven send records


class TestProvenSendsAreRecorded:
    def test_a_successful_call_records_every_hash_in_its_manifest(self):
        rows = _sample_rows()
        index = SessionSentIndex()

        added = index.record_call("session-a", rows, ok=True)

        assert added == len(rows)
        assert index.sent_hashes("session-a") == frozenset(_digests(rows))
        for digest in _digests(rows):
            assert index.was_sent("session-a", digest) is True

    def test_the_recorded_hashes_come_from_the_real_manifest_shape(self):
        rows = _sample_rows()
        assert [set(row) for row in rows] == [
            {"name", "rank", "sha256", "chars", "tokens_estimated"}
        ] * len(rows)

        index = SessionSentIndex()
        index.record_call("session-a", rows, ok=True)

        assert index.sent_hashes("session-a") == frozenset(_digests(rows))

    def test_recording_the_same_manifest_twice_is_idempotent(self):
        rows = _sample_rows()
        index = SessionSentIndex()

        first = index.record_call("session-a", rows, ok=True)
        after_first = index.sent_hashes("session-a")
        second = index.record_call("session-a", rows, ok=True)

        assert first == len(rows)
        assert second == 0
        assert index.sent_hashes("session-a") == after_first

    def test_record_call_returns_only_the_count_of_newly_added_hashes(self):
        first_rows = _real_manifest_rows(
            ("system", SegmentStabilityRank.SYSTEM, "shared prefix"),
        )
        second_rows = _real_manifest_rows(
            ("system", SegmentStabilityRank.SYSTEM, "shared prefix"),
            ("task", SegmentStabilityRank.TASK, "a brand new task"),
        )
        index = SessionSentIndex()

        index.record_call("session-a", first_rows, ok=True)
        added = index.record_call("session-a", second_rows, ok=True)

        assert added == 1


# ---------------------------------------------------------------------------
# 2, 3: what an UNPROVEN send does not record


class TestUnprovenSendsAreNotRecorded:
    def test_a_failed_call_records_nothing_and_leaves_the_session_empty(self):
        rows = _sample_rows()
        index = SessionSentIndex()

        added = index.record_call("session-a", rows, ok=False)

        assert added == 0
        assert index.sent_hashes("session-a") == frozenset()
        assert index.session_ids() == ()
        for digest in _digests(rows):
            assert index.was_sent("session-a", digest) is False

    def test_a_call_with_an_empty_session_id_records_nothing(self):
        rows = _sample_rows()
        index = SessionSentIndex()

        added = index.record_call("", rows, ok=True)

        assert added == 0
        assert index.sent_hashes("") == frozenset()
        assert index.session_ids() == ()
        for digest in _digests(rows):
            assert index.was_sent("", digest) is False

    def test_a_call_with_a_whitespace_only_session_id_records_nothing(self):
        rows = _sample_rows()
        index = SessionSentIndex()

        added = index.record_call("   ", rows, ok=True)

        assert added == 0
        assert index.sent_hashes("   ") == frozenset()
        assert index.session_ids() == ()
        for digest in _digests(rows):
            assert index.was_sent("   ", digest) is False


# ---------------------------------------------------------------------------
# 4, 12: sessions never read each other's sends


class TestSessionsStayDisjoint:
    def test_identical_segment_text_does_not_cross_from_one_session_to_another(self):
        rows = _sample_rows()
        index = SessionSentIndex()

        index.record_call("session-a", rows, ok=True)

        assert index.sent_hashes("session-b") == frozenset()
        for digest in _digests(rows):
            assert index.was_sent("session-a", digest) is True
            assert index.was_sent("session-b", digest) is False

    def test_two_sessions_keep_their_own_sets_after_both_record(self):
        shared_rows = _sample_rows()
        extra_rows = _real_manifest_rows(
            ("task", SegmentStabilityRank.TASK, "only session b saw this"),
        )
        index = SessionSentIndex()

        index.record_call("session-a", shared_rows, ok=True)
        index.record_call("session-b", shared_rows, ok=True)
        index.record_call("session-b", extra_rows, ok=True)

        extra_digest = _digests(extra_rows)[0]
        assert index.was_sent("session-b", extra_digest) is True
        assert index.was_sent("session-a", extra_digest) is False
        assert index.sent_hashes("session-a") == frozenset(_digests(shared_rows))

    def test_was_sent_is_false_for_a_session_the_index_has_never_seen(self):
        index = SessionSentIndex()

        assert index.was_sent("never-seen", "a" * 64) is False
        assert index.sent_hashes("never-seen") == frozenset()


# ---------------------------------------------------------------------------
# 5, 6: the resume-fallback safety valve


class TestInvalidateSession:
    def test_invalidate_clears_exactly_the_named_session(self):
        rows = _sample_rows()
        index = SessionSentIndex()
        index.record_call("session-a", rows, ok=True)
        index.record_call("session-b", rows, ok=True)

        index.invalidate_session("session-a")

        assert index.sent_hashes("session-a") == frozenset()
        assert index.sent_hashes("session-b") == frozenset(_digests(rows))
        assert index.session_ids() == ("session-b",)

    def test_invalidate_on_an_unknown_session_id_is_a_silent_no_op(self):
        rows = _sample_rows()
        index = SessionSentIndex()
        index.record_call("session-a", rows, ok=True)

        assert index.invalidate_session("never-seen") is None

        assert index.sent_hashes("session-a") == frozenset(_digests(rows))
        assert index.session_ids() == ("session-a",)


# ---------------------------------------------------------------------------
# 8, 9: the evidence seam


class TestEvidenceRoundTrip:
    def test_a_round_trip_preserves_every_session_and_every_hash(self):
        rows_a = _sample_rows()
        rows_b = _real_manifest_rows(
            ("system", SegmentStabilityRank.SYSTEM, "b only"),
        )
        index = SessionSentIndex()
        index.record_call("session-a", rows_a, ok=True)
        index.record_call("session-b", rows_b, ok=True)

        rebuilt = session_sent_index_from_evidence(index.as_evidence_dicts())

        assert rebuilt.session_ids() == index.session_ids()
        for session_id in index.session_ids():
            assert rebuilt.sent_hashes(session_id) == index.sent_hashes(session_id)
        assert rebuilt.as_evidence_dicts() == index.as_evidence_dicts()

    def test_evidence_rows_are_sorted_at_both_levels(self):
        index = SessionSentIndex()
        index.record_call("session-b", _sample_rows(), ok=True)
        index.record_call("session-a", _sample_rows(), ok=True)

        evidence = index.as_evidence_dicts()

        assert [row["session_id"] for row in evidence] == ["session-a", "session-b"]
        for row in evidence:
            assert row["sent_sha256"] == sorted(row["sent_sha256"])

    def test_two_indexes_built_in_opposite_order_produce_equal_evidence(self):
        rows_a = _sample_rows()
        rows_b = _real_manifest_rows(
            ("system", SegmentStabilityRank.SYSTEM, "b only"),
        )

        forward = SessionSentIndex()
        forward.record_call("session-a", rows_a, ok=True)
        forward.record_call("session-b", rows_b, ok=True)

        backward = SessionSentIndex()
        backward.record_call("session-b", rows_b, ok=True)
        backward.record_call("session-a", rows_a, ok=True)

        assert forward.as_evidence_dicts() == backward.as_evidence_dicts()


# ---------------------------------------------------------------------------
# 10, 11: a malformed input is a programming error, never a smaller index


class TestMalformedInputRaises:
    def test_record_call_raises_for_a_manifest_row_with_no_sha256_key(self):
        index = SessionSentIndex()

        with pytest.raises(SessionSentIndexError):
            index.record_call("session-a", [{"name": "system", "rank": 0}], ok=True)

    def test_record_call_raises_for_an_empty_sha256(self):
        index = SessionSentIndex()

        with pytest.raises(SessionSentIndexError):
            index.record_call("session-a", [{"sha256": ""}], ok=True)

    def test_record_call_raises_for_a_row_that_is_not_a_mapping(self):
        index = SessionSentIndex()

        with pytest.raises(SessionSentIndexError):
            index.record_call("session-a", ["not-a-mapping"], ok=True)

    def test_a_malformed_row_leaves_the_index_unchanged(self):
        rows = _sample_rows()
        index = SessionSentIndex()
        index.record_call("session-a", rows, ok=True)

        with pytest.raises(SessionSentIndexError):
            index.record_call("session-a", rows + [{"name": "bad"}], ok=True)

        assert index.sent_hashes("session-a") == frozenset(_digests(rows))

    def test_from_evidence_raises_for_a_row_with_no_session_id(self):
        with pytest.raises(SessionSentIndexError):
            session_sent_index_from_evidence([{"sent_sha256": ["a" * 64]}])

    def test_from_evidence_raises_for_an_empty_session_id(self):
        with pytest.raises(SessionSentIndexError):
            session_sent_index_from_evidence(
                [{"session_id": "  ", "sent_sha256": ["a" * 64]}]
            )

    def test_from_evidence_raises_when_sent_sha256_is_not_a_sequence(self):
        with pytest.raises(SessionSentIndexError):
            session_sent_index_from_evidence(
                [{"session_id": "session-a", "sent_sha256": 7}]
            )

    def test_from_evidence_raises_when_sent_sha256_is_a_bare_string(self):
        with pytest.raises(SessionSentIndexError):
            session_sent_index_from_evidence(
                [{"session_id": "session-a", "sent_sha256": "abc"}]
            )

    def test_from_evidence_raises_for_an_empty_hash_entry(self):
        with pytest.raises(SessionSentIndexError):
            session_sent_index_from_evidence(
                [{"session_id": "session-a", "sent_sha256": ["a" * 64, ""]}]
            )

    def test_from_evidence_raises_for_a_row_that_is_not_a_mapping(self):
        with pytest.raises(SessionSentIndexError):
            session_sent_index_from_evidence(["not-a-mapping"])


# ---------------------------------------------------------------------------
# T001b-i: the finalized-call adapters


def _finalized_output(
    *,
    error: str = "",
    usage_actuals: object = None,
    resume_used: bool = False,
    resume_session_ref: str = "",
    resume_fallback: bool = False,
) -> SimpleNamespace:
    """A stand-in for a finalized provider call, over the fields adapters read.

    DUCK-TYPED ON PURPOSE, mirroring the adapters themselves: they reach these
    attributes with ``getattr`` and import nothing from ``pingpong_provider``, so
    these tests import nothing from it either. A test that constructed a real
    ``BuilderOutput`` would quietly re-introduce the provider-layer dependency the
    index exists to stay free of, and the test suite would stop being able to
    detect its return.
    """
    return SimpleNamespace(
        error=error,
        usage_actuals=usage_actuals,
        resume_used=resume_used,
        resume_session_ref=resume_session_ref,
        resume_fallback=resume_fallback,
    )


class TestSessionIdOfFinalizedCall:
    def test_it_returns_the_session_id_the_provider_reported(self):
        output = _finalized_output(usage_actuals={"session_id": "session-a"})

        assert session_id_of_finalized_call(output) == "session-a"

    @pytest.mark.parametrize(
        "usage_actuals",
        [
            None,
            {},
            {"cost_usd": 0.01},
            {"session_id": None},
            {"session_id": ""},
            {"session_id": 0},
        ],
    )
    def test_it_returns_empty_when_no_session_id_was_reported(self, usage_actuals):
        output = _finalized_output(usage_actuals=usage_actuals)

        assert session_id_of_finalized_call(output) == ""

    @pytest.mark.parametrize("usage_actuals", [["session-a"], 7])
    def test_a_non_mapping_usage_actuals_reads_as_no_session_and_never_raises(
        self, usage_actuals
    ):
        output = _finalized_output(usage_actuals=usage_actuals)

        assert session_id_of_finalized_call(output) == ""


class TestRecordFinalizedCall:
    def test_a_proven_call_records_every_hash_and_returns_record_calls_count(self):
        rows = _sample_rows()
        output = _finalized_output(usage_actuals={"session_id": "session-a"})
        index = SessionSentIndex()

        added = record_finalized_call(index, output, rows)

        reference = SessionSentIndex()
        assert added == reference.record_call("session-a", rows, ok=True)
        assert added == len(rows)
        assert index.sent_hashes("session-a") == frozenset(_digests(rows))

    def test_an_errored_call_records_nothing_and_leaves_the_session_empty(self):
        rows = _sample_rows()
        output = _finalized_output(
            error="provider_error: TimeoutError",
            usage_actuals={"session_id": "session-a"},
        )
        index = SessionSentIndex()

        added = record_finalized_call(index, output, rows)

        assert added == 0
        assert index.sent_hashes("session-a") == frozenset()
        assert index.session_ids() == ()

    def test_a_call_with_no_session_id_records_nothing_though_it_succeeded(self):
        rows = _sample_rows()
        output = _finalized_output(usage_actuals=None)
        index = SessionSentIndex()

        added = record_finalized_call(index, output, rows)

        assert added == 0
        assert index.session_ids() == ()


class TestInvalidateOnResumeFallback:
    def test_no_fallback_flag_means_no_invalidation_even_with_a_resumed_ref(self):
        rows = _sample_rows()
        index = SessionSentIndex()
        index.record_call("session-a", rows, ok=True)
        output = _finalized_output(resume_used=True, resume_session_ref="session-a")

        assert invalidate_on_resume_fallback(index, output, "session-a") is False

        assert index.sent_hashes("session-a") == frozenset(_digests(rows))
        assert index.session_ids() == ("session-a",)

    def test_a_fallback_empties_exactly_the_resumed_session(self):
        rows = _sample_rows()
        index = SessionSentIndex()
        index.record_call("session-a", rows, ok=True)
        index.record_call("session-b", rows, ok=True)
        output = _finalized_output(resume_fallback=True)

        assert invalidate_on_resume_fallback(index, output, "session-a") is True

        assert index.sent_hashes("session-a") == frozenset()
        assert index.sent_hashes("session-b") == frozenset(_digests(rows))
        assert index.session_ids() == ("session-b",)

    def test_the_loops_replaced_output_invalidates_when_resumed_ref_is_passed(self):
        # THE LOOP'S REAL SHAPE: on the fallback path pingpong_loop.py calls the
        # provider again with resume=None and sets resume_fallback on the NEW
        # output, so that output's own resume_session_ref is "".
        rows = _sample_rows()
        index = SessionSentIndex()
        index.record_call("session-a", rows, ok=True)
        replaced = _finalized_output(
            resume_fallback=True, resume_used=False, resume_session_ref=""
        )

        assert invalidate_on_resume_fallback(index, replaced, "session-a") is True

        assert index.sent_hashes("session-a") == frozenset()

    def test_the_loops_replaced_output_alone_invalidates_nothing(self):
        # THIS IS THE FAILURE THE THIRD ARGUMENT PREVENTS. Reading only the
        # output object, the adapter has no id to act on and the stale session
        # survives a fallback — silently, on exactly the path invalidation
        # exists for.
        rows = _sample_rows()
        index = SessionSentIndex()
        index.record_call("session-a", rows, ok=True)
        replaced = _finalized_output(
            resume_fallback=True, resume_used=False, resume_session_ref=""
        )

        assert invalidate_on_resume_fallback(index, replaced) is False

        assert index.sent_hashes("session-a") == frozenset(_digests(rows))

    def test_the_output_ref_is_used_when_the_caller_holds_no_variable(self):
        rows = _sample_rows()
        index = SessionSentIndex()
        index.record_call("session-a", rows, ok=True)
        output = _finalized_output(
            resume_fallback=True, resume_used=True, resume_session_ref="session-a"
        )

        assert invalidate_on_resume_fallback(index, output) is True

        assert index.sent_hashes("session-a") == frozenset()

    @pytest.mark.parametrize("resumed_ref", ["   ", "\t"])
    def test_a_whitespace_only_ref_invalidates_nothing(self, resumed_ref):
        rows = _sample_rows()
        index = SessionSentIndex()
        index.record_call("session-a", rows, ok=True)
        output = _finalized_output(resume_fallback=True)

        assert invalidate_on_resume_fallback(index, output, resumed_ref) is False

        assert index.sent_hashes("session-a") == frozenset(_digests(rows))


class TestAdapterLifecycle:
    def test_record_then_fallback_then_record_again(self):
        rows = _sample_rows()
        index = SessionSentIndex()
        success = _finalized_output(usage_actuals={"session_id": "s1"})

        assert record_finalized_call(index, success, rows) == len(rows)
        assert index.sent_hashes("s1") == frozenset(_digests(rows))

        fallback = _finalized_output(resume_fallback=True, resume_session_ref="")
        assert invalidate_on_resume_fallback(index, fallback, "s1") is True
        assert index.sent_hashes("s1") == frozenset()
        assert index.session_ids() == ()

        assert record_finalized_call(index, success, rows) == len(rows)
        assert index.sent_hashes("s1") == frozenset(_digests(rows))


class TestChainAgainstTheRealLoop:
    """F109 T001b-ii: THESE CASES RUN THE REAL LOOP, WITH ONE PROVIDER PER ROLE.

    Every test above is a pure unit test of the index. Every test here drives
    ``run_pingpong`` end to end against ``FakeProvider`` and then reads
    ``PingPongResult.session_sent_evidence`` — they are the first cases in this
    feature proving the index is fed by ACTUAL provider calls rather than by a
    hand-built manifest. Both fixtures are declared inside this class on
    purpose, so the pure tests above keep touching no tmp_path and no provider.

    WHY THE TWO PROVIDERS CARRY DISTINCT SESSION IDS — read this before changing
    anything here (finding R-0770, repaired in F109 round 4). These cases used to
    pass ONE ``FakeProvider`` instance as both ``builder_provider`` and
    ``reviewer_provider``. A ``FakeProvider`` reports a single
    ``fake_session_id``, so the Builder and Reviewer seams recorded into the SAME
    evidence row and the loop's four call sites collapsed into a single
    observable: deleting either ``record_finalized_call`` left the row populated
    by the other seam, so no mutation of an individual seam could be caught and
    the suite stayed green on a broken loop. Two subjects sharing one observable
    cannot fail on either. Giving the roles DISTINCT ids — ``sess-builder`` and
    ``sess-reviewer`` — gives each seam a row of its own, so a case can name the
    seam it pins. Never collapse the two ids back into one.
    """

    BUILDER_SESSION = "sess-builder"
    REVIEWER_SESSION = "sess-reviewer"

    @staticmethod
    def _make_repo(base: Path) -> Path:
        """Minimal demo repo, matching tests/orchestration/test_session_resume.py."""
        base.mkdir(parents=True)
        (base / "README.md").write_text("# Demo\nA demo project.\n")
        (base / "docs").mkdir()
        (base / "docs" / "README.md").write_text("# Docs\nDocumentation here.\n")
        (base / "src").mkdir()
        (base / "src" / "main.py").write_text("def hello():\n    return 'hello'\n")
        (base / ".env").write_text("API_KEY=secret123\n")
        (base / ".env.local").write_text("DB_PASSWORD=hunter2\n")
        return base

    @staticmethod
    def _provider_pair(
        *,
        with_session_ids: bool = True,
        supports_resume: bool = True,
        builder_resume_fails: bool = False,
    ) -> tuple[FakeProvider, FakeProvider]:
        """THE PAIR EVERY CASE HERE DRIVES: one provider per role, distinct ids.

        Built in exactly one place so no case restates it and no case can quietly
        go back to sharing a single instance between the two roles — which is the
        collapse the class docstring describes. ``FakeProvider`` counts builds and
        reviews on separate counters, so splitting one instance into two changes
        no round outcome; it only splits the observable.
        """
        builder_id = TestChainAgainstTheRealLoop.BUILDER_SESSION if with_session_ids else ""
        reviewer_id = TestChainAgainstTheRealLoop.REVIEWER_SESSION if with_session_ids else ""
        builder = FakeProvider(
            fail_on_round=1, pass_on_round=2, supports_resume=supports_resume,
            fake_session_id=builder_id, resume_fails=builder_resume_fails,
        )
        reviewer = FakeProvider(
            fail_on_round=1, pass_on_round=2, supports_resume=supports_resume,
            fake_session_id=reviewer_id,
        )
        return builder, reviewer

    @staticmethod
    def _run(repo: Path, providers: tuple[FakeProvider, FakeProvider], **kwargs):
        builder_provider, reviewer_provider = providers
        return run_pingpong(
            "Fix README", str(repo),
            builder_provider=builder_provider, reviewer_provider=reviewer_provider,
            **kwargs,
        )

    @staticmethod
    def _rows_by_session(result) -> dict[str, list[str]]:
        """The evidence keyed by session id, so a case can name the seam it reads."""
        return {
            str(row["session_id"]): list(row["sent_sha256"])
            for row in result.session_sent_evidence
        }

    @pytest.fixture(autouse=True)
    def isolate_data_root(self, tmp_path: Path, monkeypatch):
        """Redirect REMEDY_DATA_DIR to tmp so no case here writes the real data root."""
        data_dir = tmp_path / "remedy_data"
        data_dir.mkdir()
        monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
        return data_dir

    @pytest.fixture
    def demo_repo(self, tmp_path: Path) -> Path:
        return self._make_repo(tmp_path / "demo_repo")

    def test_the_builder_seam_records_a_row_of_its_own(self, demo_repo: Path):
        # THE BUILDER SEAM, PINNED ALONE. Deleting the Builder
        # record_finalized_call from pingpong_loop.py makes this row disappear
        # entirely, so this case is the one that mutation breaks. No exact hash
        # COUNT is asserted: the count follows from prompt composition and would
        # pin this test to unrelated prompt changes.
        result = self._run(demo_repo, self._provider_pair(), repair_rounds=2)

        rows = self._rows_by_session(result)
        assert self.BUILDER_SESSION in rows, sorted(rows)
        assert rows[self.BUILDER_SESSION] != []

    def test_the_reviewer_seam_records_a_row_of_its_own(self, demo_repo: Path):
        # The mirror of the case above, for the Reviewer seam: deleting the
        # Reviewer record_finalized_call removes exactly this row.
        result = self._run(demo_repo, self._provider_pair(), repair_rounds=2)

        rows = self._rows_by_session(result)
        assert self.REVIEWER_SESSION in rows, sorted(rows)
        assert rows[self.REVIEWER_SESSION] != []

    def test_both_seams_appear_exactly_once_and_the_rows_are_sorted(self, demo_repo: Path):
        result = self._run(demo_repo, self._provider_pair(), repair_rounds=2)

        session_ids = [str(row["session_id"]) for row in result.session_sent_evidence]
        assert set(session_ids) == {self.BUILDER_SESSION, self.REVIEWER_SESSION}
        assert len(session_ids) == 2
        # The determinism as_evidence_dicts promises: rows sorted by session id.
        assert session_ids == sorted(session_ids)

    def test_every_recorded_hash_is_a_real_segment_hash(self, demo_repo: Path):
        result = self._run(demo_repo, self._provider_pair(), repair_rounds=2)

        assert result.session_sent_evidence != []
        for row in result.session_sent_evidence:
            hashes = row["sent_sha256"]
            assert hashes
            assert hashes == sorted(hashes)
            for digest in hashes:
                assert len(digest) == 64, digest
                assert set(digest) <= set("0123456789abcdef"), digest

    def test_a_provider_pair_that_reports_no_session_id_records_nothing(self, demo_repo: Path):
        # The proven-sends-only rule surviving contact with the loop: with no
        # session named by either role, there is no session to remember against.
        result = self._run(
            demo_repo, self._provider_pair(with_session_ids=False), repair_rounds=2,
        )

        assert result.session_sent_evidence == []

    def test_the_two_seams_do_not_share_one_observable(self, demo_repo: Path):
        # THE COUNTER-MEASURE TO R-0770, ASSERTED RATHER THAN ONLY DOCUMENTED.
        # Builder and Reviewer compose different prompts, so their recorded hash
        # sets differ. This assertion fails the moment the two seams are wired to
        # one index key again — which is exactly the collapse the repair prevents.
        result = self._run(demo_repo, self._provider_pair(), repair_rounds=2)

        rows = self._rows_by_session(result)
        assert set(rows[self.BUILDER_SESSION]) != set(rows[self.REVIEWER_SESSION])

    def test_a_single_round_run_records_the_sessions_it_proved(
        self, demo_repo: Path, tmp_path: Path,
    ):
        # PINNED FROM REAL RUNS, not from expectation. Recording is keyed on a
        # PROVEN send that names a session, and a first round proves exactly
        # that; "resumed session only" governs the composition hook (T002), not
        # what the index is permitted to remember.
        sessionless = self._run(
            demo_repo, self._provider_pair(with_session_ids=False, supports_resume=False),
        )
        assert len(sessionless.rounds) == 1
        assert sessionless.session_sent_evidence == []

        named = self._run(self._make_repo(tmp_path / "repo_named"), self._provider_pair())
        assert len(named.rounds) == 1
        assert [str(row["session_id"]) for row in named.session_sent_evidence] == [
            self.BUILDER_SESSION,
            self.REVIEWER_SESSION,
        ]
        for row in named.session_sent_evidence:
            assert row["sent_sha256"]

    def test_a_failed_builder_resume_falls_back_within_the_same_round(self, demo_repo: Path):
        # THIS CASE PINS THE FALLBACK PATH AND NOTHING MORE. It asserts the run
        # completes and that round 2's builder really did fall back. A SINGLE run
        # cannot discriminate the Builder invalidate_on_resume_fallback call,
        # because the record_finalized_call that follows it refills the very
        # session just cleared. The case below discriminates it, by comparing two
        # runs; R-0770 records that a within-run discriminator waits for T002.
        result = self._run(
            demo_repo, self._provider_pair(builder_resume_fails=True), repair_rounds=2,
        )

        assert result.final_status == "staged_review_passed"
        assert result.rounds[1].builder_output.resume_fallback is True
        assert [str(row["session_id"]) for row in result.session_sent_evidence] == [
            self.BUILDER_SESSION,
            self.REVIEWER_SESSION,
        ]

    def test_the_fallback_invalidation_shrinks_exactly_the_builder_row(
        self, demo_repo: Path, tmp_path: Path,
    ):
        # ROUND 3'S DISCRIMINATOR, KEPT AND NARROWED TO THE SEAM THAT FELL BACK.
        # Only the builder's resume fails here, so only the builder's row may
        # move; naming the row is what the two distinct session ids buy.
        fallback = self._run(
            demo_repo, self._provider_pair(builder_resume_fails=True), repair_rounds=2,
        )
        assert fallback.final_status == "staged_review_passed"
        assert fallback.rounds[1].builder_output.resume_fallback is True

        clean = self._run(
            self._make_repo(tmp_path / "repo_clean"), self._provider_pair(), repair_rounds=2,
        )
        assert clean.rounds[1].builder_output.resume_fallback is False

        fallback_rows = self._rows_by_session(fallback)
        clean_rows = self._rows_by_session(clean)
        # THE DISCRIMINATOR. The fallback dropped what the failed resume made
        # unprovable, so the surviving BUILDER set is strictly SMALLER than the
        # same chain that never fell back. Without the invalidation the fallback
        # run would ACCUMULATE round 1's hashes and the two rows would be equal.
        assert len(fallback_rows[self.BUILDER_SESSION]) < len(clean_rows[self.BUILDER_SESSION]), (
            len(fallback_rows[self.BUILDER_SESSION]),
            len(clean_rows[self.BUILDER_SESSION]),
        )
        # The Reviewer never fell back, so its row is untouched by the fallback.
        assert len(fallback_rows[self.REVIEWER_SESSION]) == len(clean_rows[self.REVIEWER_SESSION])

    def test_the_loop_is_otherwise_unchanged_for_a_non_resuming_provider_pair(self, demo_repo: Path):
        # Both expected values were MEASURED on a real run at this round's base
        # commit before the wiring landed, and again after it — not recalled.
        result = self._run(
            demo_repo, self._provider_pair(supports_resume=False), repair_rounds=2,
        )

        assert result.final_status == "staged_review_passed"
        assert len(result.rounds) == 2


# ---------------------------------------------------------------------------
# T002a: the pure dedupe DECISION and the MARKER TEXT
#
# PURE AGAIN, deliberately: no tmp_path, no provider and no loop below this
# line. These cases pin every rule about WHEN a segment may be replaced before
# any of it can reach a prompt, so the composition hook that follows (T002b) is
# mechanical and carries no decision of its own.


SENT_HASH = "a" * 64
LONG_ENOUGH = "x" * DEDUPE_MIN_SEGMENT_CHARS


class TestShouldDedupeSegment:
    def test_a_long_already_sent_segment_is_deduped(self):
        assert should_dedupe_segment(LONG_ENOUGH, SENT_HASH, frozenset({SENT_HASH})) is True

    def test_the_kill_switch_refuses_though_every_other_condition_holds(self):
        # THE CASE THAT MUST NEVER ROT. Disabling dedupe has to be total, not
        # mostly: this is the only assertion that says so.
        assert (
            should_dedupe_segment(
                LONG_ENOUGH, SENT_HASH, frozenset({SENT_HASH}), enabled=False
            )
            is False
        )

    def test_a_hash_the_session_never_received_is_not_deduped(self):
        assert should_dedupe_segment(LONG_ENOUGH, "b" * 64, frozenset({SENT_HASH})) is False

    def test_an_empty_sent_set_dedupes_nothing(self):
        assert should_dedupe_segment(LONG_ENOUGH, SENT_HASH, frozenset()) is False

    def test_a_segment_of_exactly_the_minimum_length_is_deduped(self):
        # THE BOUNDARY, INCLUSIVE SIDE. The comparison is >=, so exactly the
        # minimum qualifies.
        text = "x" * DEDUPE_MIN_SEGMENT_CHARS
        assert len(text) == DEDUPE_MIN_SEGMENT_CHARS

        assert should_dedupe_segment(text, SENT_HASH, frozenset({SENT_HASH})) is True

    def test_a_segment_one_character_below_the_minimum_is_not_deduped(self):
        # THE BOUNDARY, EXCLUSIVE SIDE. One character fewer is refused, which is
        # what makes the >= above a decision rather than an accident.
        text = "x" * (DEDUPE_MIN_SEGMENT_CHARS - 1)
        assert len(text) == DEDUPE_MIN_SEGMENT_CHARS - 1

        assert should_dedupe_segment(text, SENT_HASH, frozenset({SENT_HASH})) is False

    def test_a_custom_min_chars_override_is_honoured(self):
        short = "x" * 12
        sent = frozenset({SENT_HASH})

        assert should_dedupe_segment(short, SENT_HASH, sent) is False
        assert should_dedupe_segment(short, SENT_HASH, sent, min_chars=10) is True

    @pytest.mark.parametrize("text", [None, 7, b"x" * 300, ["x" * 300], object()])
    def test_a_non_string_text_returns_false_and_raises_nothing(self, text):
        assert should_dedupe_segment(text, SENT_HASH, frozenset({SENT_HASH})) is False

    @pytest.mark.parametrize("sha256", [None, 7, "", "   ", b"a" * 64, ["a" * 64]])
    def test_a_malformed_sha256_returns_false_and_raises_nothing(self, sha256):
        assert should_dedupe_segment(LONG_ENOUGH, sha256, frozenset({SENT_HASH})) is False


class TestDedupeMarkerForSegment:
    def test_the_marker_is_exactly_the_expected_string(self):
        # THE WHOLE STRING, not a substring: the marker is what the model reads,
        # so its exact wording is the contract.
        assert dedupe_marker_for_segment("dossier") == "[unchanged: dossier, previously provided]"

    @pytest.mark.parametrize("name", ["", "   ", "\t\n"])
    def test_a_nameless_marker_raises(self, name):
        # A marker naming nothing would tell the model that something it cannot
        # identify was withheld — worse than sending the segment again.
        with pytest.raises(SessionSentIndexError):
            dedupe_marker_for_segment(name)

    def test_the_marker_is_shorter_than_the_threshold_that_justifies_it(self):
        # THE THRESHOLD ACTUALLY GUARANTEES A SAVING. This pins the constant
        # against the marker it exists to justify: change either so that the
        # replacement stops saving anything and this case fails.
        marker = dedupe_marker_for_segment("dossier")

        assert len(marker) < DEDUPE_MIN_SEGMENT_CHARS


class TestTheDecisionAgainstARecordedIndex:
    """The decision read against a REAL index built from a REAL manifest.

    No loop and no provider — just the two halves of the feature meeting: what
    ``record_call`` remembered, and what ``should_dedupe_segment`` will do with
    it. The hashes are genuine segment hashes from the shipped producer, never
    hand-made, so a change to the hashing scheme cannot leave this passing.
    """

    LONG_TEXT = "the dossier body, repeated to earn its replacement. " * 8
    SHORT_TEXT = "implement the index"

    def _recorded(self) -> tuple[frozenset[str], dict[str, str]]:
        rows = _real_manifest_rows(
            ("dossier", SegmentStabilityRank.DOSSIER, self.LONG_TEXT),
            ("task", SegmentStabilityRank.TASK, self.SHORT_TEXT),
        )
        index = SessionSentIndex()
        index.record_call("session-a", rows, ok=True)
        by_name = {str(row["name"]): str(row["sha256"]) for row in rows}
        return index.sent_hashes("session-a"), by_name

    def test_a_long_recorded_segment_is_deduped_and_a_short_one_is_not(self):
        sent, by_name = self._recorded()
        assert len(self.LONG_TEXT) >= DEDUPE_MIN_SEGMENT_CHARS
        assert len(self.SHORT_TEXT) < DEDUPE_MIN_SEGMENT_CHARS
        assert set(by_name) == {"dossier", "task"}

        assert should_dedupe_segment(self.LONG_TEXT, by_name["dossier"], sent) is True
        # SAME SESSION, SAME MANIFEST, PROVEN SENT — and still refused, purely
        # because replacing it would not pay for the marker.
        assert by_name["task"] in sent
        assert should_dedupe_segment(self.SHORT_TEXT, by_name["task"], sent) is False

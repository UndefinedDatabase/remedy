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

from packages.orchestration.pingpong_loop import (
    ReviewFinding,
    _dedupe_resumed_segments,
    compose_builder_prompt,
    compose_reviewer_prompt,
    run_pingpong,
)
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
        reviewer_resume_fails: bool = False,
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
            fake_session_id=reviewer_id, resume_fails=reviewer_resume_fails,
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


# ---------------------------------------------------------------------------
# T002b, first half: the composition TRANSFORM that applies that decision
#
# PURE like the T002a block above — no tmp_path, no provider and no loop below
# this line. Segments are built through the REAL PromptSegmentRegistry rather
# than as PromptSegment literals, so every case runs against the shape that
# actually ships, and the last cases pin the transform's hash source against
# the index's own.


TRANSFORM_LONG_TEXT = "the dossier body, long enough to earn its replacement. " * 8
TRANSFORM_SHORT_TEXT = "implement the transform"


def _registered_segments(*specs: tuple[str, SegmentStabilityRank, str]) -> tuple:
    """Segments from the REAL registry, in registration order."""
    registry = PromptSegmentRegistry()
    for name, rank, text in specs:
        registry.register(name, rank, text)
    return registry.registered_segments()


def _sha256_by_name(*specs: tuple[str, SegmentStabilityRank, str]) -> dict[str, str]:
    """Segment name -> sha256, taken from the shipped manifest producer."""
    return {str(row["name"]): str(row["sha256"]) for row in _real_manifest_rows(*specs)}


class TestDedupeResumedSegments:
    """The transform rewrites TEXT and nothing else, and says what it rewrote."""

    def test_a_long_already_sent_segment_becomes_its_marker_with_name_and_rank_kept(self):
        specs = (("dossier", SegmentStabilityRank.DOSSIER, TRANSFORM_LONG_TEXT),)
        segments = _registered_segments(*specs)
        sent = frozenset(_sha256_by_name(*specs).values())

        kept, replaced = _dedupe_resumed_segments(segments, sent)

        # THE TEXT IS EXACTLY THE MARKER, not merely something shorter.
        assert kept[0].text == dedupe_marker_for_segment("dossier")
        # AND EVERYTHING ELSE ABOUT THE SEGMENT SURVIVES — this is what keeps
        # composition order and the cacheable prefix untouched.
        assert kept[0].name == segments[0].name == "dossier"
        assert kept[0].rank == segments[0].rank == SegmentStabilityRank.DOSSIER
        assert replaced == ("dossier",)

    def test_the_replaced_names_are_exactly_the_replaced_segments_in_order(self):
        specs = (
            ("system", SegmentStabilityRank.SYSTEM, TRANSFORM_LONG_TEXT + " one"),
            ("dossier", SegmentStabilityRank.DOSSIER, TRANSFORM_LONG_TEXT + " two"),
            ("task", SegmentStabilityRank.TASK, TRANSFORM_LONG_TEXT + " three"),
        )
        by_name = _sha256_by_name(*specs)
        sent = frozenset({by_name["system"], by_name["task"]})

        kept, replaced = _dedupe_resumed_segments(_registered_segments(*specs), sent)

        assert replaced == ("system", "task")
        # The one segment this session never received still carries its body.
        assert kept[1].text == TRANSFORM_LONG_TEXT + " two"

    def test_the_returned_order_is_input_order_and_never_rank_order(self):
        # Ranks 5, 0, 2 in REGISTRATION order, so a rank sort inside the
        # transform would visibly reorder them and fail this case.
        specs = (
            ("steering", SegmentStabilityRank.STEERING, TRANSFORM_LONG_TEXT + " a"),
            ("system", SegmentStabilityRank.SYSTEM, TRANSFORM_LONG_TEXT + " b"),
            ("dossier", SegmentStabilityRank.DOSSIER, TRANSFORM_LONG_TEXT + " c"),
        )
        segments = _registered_segments(*specs)
        sent = frozenset(_sha256_by_name(*specs).values())

        kept, replaced = _dedupe_resumed_segments(segments, sent)

        assert [segment.name for segment in kept] == [segment.name for segment in segments]
        assert [segment.name for segment in kept] == ["steering", "system", "dossier"]
        assert replaced == ("steering", "system", "dossier")

    def test_the_kill_switch_returns_every_segment_unchanged_and_no_names(self):
        # THE CASE THAT MUST NEVER ROT. Disabling has to be TOTAL, so the same
        # input is deduped with the default first: nothing but the flag differs.
        specs = (("dossier", SegmentStabilityRank.DOSSIER, TRANSFORM_LONG_TEXT),)
        segments = _registered_segments(*specs)
        sent = frozenset(_sha256_by_name(*specs).values())
        assert _dedupe_resumed_segments(segments, sent)[1] == ("dossier",)

        kept, replaced = _dedupe_resumed_segments(segments, sent, enabled=False)

        assert kept == tuple(segments)
        assert replaced == ()

    def test_an_empty_sent_set_replaces_nothing(self):
        specs = (
            ("dossier", SegmentStabilityRank.DOSSIER, TRANSFORM_LONG_TEXT),
            ("task", SegmentStabilityRank.TASK, TRANSFORM_SHORT_TEXT),
        )
        segments = _registered_segments(*specs)

        kept, replaced = _dedupe_resumed_segments(segments, frozenset())

        assert replaced == ()
        # UNCHANGED means the SAME OBJECTS, not equal copies.
        assert all(kept[index] is segments[index] for index in range(len(segments)))

    def test_a_long_segment_whose_hash_was_never_sent_is_not_replaced(self):
        specs = (("dossier", SegmentStabilityRank.DOSSIER, TRANSFORM_LONG_TEXT),)
        segments = _registered_segments(*specs)
        stranger = _sha256_by_name(("other", SegmentStabilityRank.TASK, "a different body"))

        kept, replaced = _dedupe_resumed_segments(segments, frozenset(stranger.values()))

        assert replaced == ()
        assert kept[0].text == TRANSFORM_LONG_TEXT

    def test_a_short_already_sent_segment_is_refused_for_its_length_alone(self):
        specs = (("task", SegmentStabilityRank.TASK, TRANSFORM_SHORT_TEXT),)
        segments = _registered_segments(*specs)
        digest = _sha256_by_name(*specs)["task"]
        sent = frozenset({digest})
        # THE HASH IS IN THE SET FIRST, so the refusal below is demonstrably
        # about LENGTH and not about a hash the session never received.
        assert digest in sent
        assert len(TRANSFORM_SHORT_TEXT) < DEDUPE_MIN_SEGMENT_CHARS

        kept, replaced = _dedupe_resumed_segments(segments, sent)

        assert replaced == ()
        assert kept[0].text == TRANSFORM_SHORT_TEXT

    def test_a_smaller_min_chars_replaces_what_the_default_refuses(self):
        specs = (("task", SegmentStabilityRank.TASK, TRANSFORM_SHORT_TEXT),)
        segments = _registered_segments(*specs)
        sent = frozenset(_sha256_by_name(*specs).values())

        assert _dedupe_resumed_segments(segments, sent)[1] == ()

        kept, replaced = _dedupe_resumed_segments(
            segments, sent, min_chars=len(TRANSFORM_SHORT_TEXT)
        )

        assert replaced == ("task",)
        assert kept[0].text == dedupe_marker_for_segment("task")

    def test_the_transform_reads_the_same_hashes_a_real_index_recorded(self):
        # THE ANTI-DRIFT PIN, end to end. The sent set is not hand-made: the
        # REAL manifest rows are recorded into a REAL SessionSentIndex and read
        # back, so a change to either hash source that broke dedupe could not
        # land green here.
        specs = (
            ("dossier", SegmentStabilityRank.DOSSIER, TRANSFORM_LONG_TEXT),
            ("task", SegmentStabilityRank.TASK, TRANSFORM_SHORT_TEXT),
        )
        index = SessionSentIndex()
        index.record_call("session-a", _real_manifest_rows(*specs), ok=True)
        sent = index.sent_hashes("session-a")

        kept, replaced = _dedupe_resumed_segments(_registered_segments(*specs), sent)

        assert replaced == ("dossier",)
        assert kept[0].text == dedupe_marker_for_segment("dossier")
        assert kept[1].text == TRANSFORM_SHORT_TEXT

    def test_the_input_segments_are_not_mutated(self):
        specs = (("dossier", SegmentStabilityRank.DOSSIER, TRANSFORM_LONG_TEXT),)
        segments = _registered_segments(*specs)
        sent = frozenset(_sha256_by_name(*specs).values())

        kept, replaced = _dedupe_resumed_segments(segments, sent)

        assert replaced == ("dossier",)
        assert kept[0].text != segments[0].text
        assert segments[0].text == TRANSFORM_LONG_TEXT

    def test_composing_the_returned_segments_carries_the_marker_not_the_body(self):
        specs = (
            ("dossier", SegmentStabilityRank.DOSSIER, TRANSFORM_LONG_TEXT),
            ("task", SegmentStabilityRank.TASK, TRANSFORM_SHORT_TEXT),
        )
        index = SessionSentIndex()
        index.record_call("session-a", _real_manifest_rows(*specs), ok=True)
        kept, _ = _dedupe_resumed_segments(
            _registered_segments(*specs), index.sent_hashes("session-a")
        )

        composed = compose_prompt_segments(kept)

        assert dedupe_marker_for_segment("dossier") in composed.text
        assert TRANSFORM_LONG_TEXT not in composed.text
        assert TRANSFORM_SHORT_TEXT in composed.text


# ---------------------------------------------------------------------------
# T002b, second half: THE COMPOSITION SEAM — the two compose functions and the
# two loop call sites.
#
# THE "no tmp_path, no provider and no loop below this line" NOTE ABOVE STOPS
# HERE, and deliberately so. The golden cases in the class below are still pure,
# but the last two drive the REAL loop against ``FakeProvider`` in a tmp_path,
# because the scope rule this whole feature turns on — "resumed session only" —
# lives at the CALL SITE, and no re-composition can observe a call site. A
# re-composition asserts what the test itself passed in; only the loop's own
# recorded prompts say what the loop actually composed.
#
# THE FIRST THREE CASES ARE THE FEATURE FILE'S FIRST ACCEPTANCE ITEM: with no
# dedupe argument, or with ``None``, or with an EMPTY sent set, the composed
# bytes are exactly what this repository composed before the parameter existed.
# That is why the default is ``None`` rather than an empty frozenset: ``None``
# does not call the transform at all, so the bypass is provable and not merely
# likely.


GOLDEN_FINDING = ReviewFinding(
    id="R-9001",
    severity="high",
    file="src/main.py",
    summary="the greeting has no test",
    required_fix="add a test for hello()",
)

GOLDEN_DIFF = (
    "--- a/src/main.py\n+++ b/src/main.py\n@@ -1,2 +1,2 @@\n"
    "-def hello():\n+def hello(name):\n"
)

# THREE SHAPES THAT REALLY DIFFER — findings, safe_diff and round_number all
# vary, and ``test_the_three_builder_shapes_are_not_the_same_prompt`` below
# PROVES they differ rather than asserting the goldens over three copies of one
# prompt, which would pass while proving nothing.
BUILDER_SHAPES: tuple[dict, ...] = (
    {"round_number": 1},
    {"round_number": 2, "findings": [GOLDEN_FINDING], "safe_diff": GOLDEN_DIFF},
    {
        "round_number": 7,
        "findings": [GOLDEN_FINDING],
        "safe_diff": GOLDEN_DIFF + "@@ -9,1 +9,1 @@\n-old\n+new\n",
        "test_result": "1 failed, 3 passed",
        "task_body": "rewrite the greeting so it takes a name",
        "scope_contract": "Touch only src/main.py.",
    },
)

REVIEWER_SHAPES: tuple[dict, ...] = (
    {},
    {
        "safe_diff": GOLDEN_DIFF,
        "test_result": "1 failed, 3 passed",
        "prior_findings": [GOLDEN_FINDING],
        "repair_round": 2,
        "scope_contract": "Touch only src/main.py.",
    },
)

BUILDER_ARGS = ("Fix the greeting", "The repository is remedy.")
REVIEWER_ARGS = ("Fix the greeting", "I renamed the parameter.")


def _sha256_of_marker(name: str) -> str:
    """The SHIPPED producer's sha256 of ``name``'s marker text.

    Rank is irrelevant to a manifest sha256 — it is taken over the segment TEXT
    alone — so any rank answers here. Taking the digest from the same producer
    the index recorded keeps this file free of a second hashing expression that
    could drift away from the one the feature actually decides on.
    """
    spec = (name, SegmentStabilityRank.SYSTEM, dedupe_marker_for_segment(name))
    return _sha256_by_name(spec)[name]


def _names_replaced_by_their_marker(composed) -> list[str]:
    """Every manifest name whose segment text is EXACTLY that name's marker."""
    return [
        str(row["name"])
        for row in composed.manifest_as_dicts()
        if str(row["sha256"]) == _sha256_of_marker(str(row["name"]))
    ]


class TestTheComposeSeamBypassesUntilAResumedSessionSaysOtherwise:
    """The two compose functions, their default, and the loop's own call sites."""

    @pytest.fixture
    def loop_repo(self, tmp_path: Path, monkeypatch) -> Path:
        """A demo repo with ``REMEDY_DATA_DIR`` redirected — for the loop cases only.

        Deliberately NOT autouse, so the golden cases above it keep touching no
        tmp_path and no environment. The repo itself comes from
        ``TestChainAgainstTheRealLoop._make_repo`` rather than from a second copy
        of it, and the providers below come from that class's ``_provider_pair``
        for the same reason: one construction, one place to keep honest.
        """
        data_dir = tmp_path / "remedy_data"
        data_dir.mkdir()
        monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
        return TestChainAgainstTheRealLoop._make_repo(tmp_path / "demo_repo")

    # -- SPEC L case 1: the builder golden, over three shapes ----------------

    def test_the_three_builder_shapes_are_not_the_same_prompt(self):
        # THE DISCRIMINATOR FOR THE GOLDEN BELOW. Three shapes that composed the
        # same bytes would make the byte-equality cases vacuous.
        texts = [compose_builder_prompt(*BUILDER_ARGS, **shape).text for shape in BUILDER_SHAPES]
        assert len(set(texts)) == len(BUILDER_SHAPES), [len(text) for text in texts]

    @pytest.mark.parametrize("shape_index", range(len(BUILDER_SHAPES)))
    def test_the_builder_default_and_an_explicit_none_compose_the_same_bytes(self, shape_index: int):
        shape = BUILDER_SHAPES[shape_index]

        omitted = compose_builder_prompt(*BUILDER_ARGS, **shape)
        explicit = compose_builder_prompt(*BUILDER_ARGS, dedupe_sent_hashes=None, **shape)

        assert explicit.text == omitted.text
        # THE MANIFEST TOO, not only the text: a transform that rewrote names or
        # ranks while leaving the bytes alone would pass a text-only assertion.
        assert explicit.manifest == omitted.manifest

    # -- SPEC L case 2: the reviewer golden, over two shapes -----------------

    def test_the_two_reviewer_shapes_are_not_the_same_prompt(self):
        texts = [compose_reviewer_prompt(*REVIEWER_ARGS, **shape).text for shape in REVIEWER_SHAPES]
        assert len(set(texts)) == len(REVIEWER_SHAPES), [len(text) for text in texts]

    @pytest.mark.parametrize("shape_index", range(len(REVIEWER_SHAPES)))
    def test_the_reviewer_default_and_an_explicit_none_compose_the_same_bytes(self, shape_index: int):
        shape = REVIEWER_SHAPES[shape_index]

        omitted = compose_reviewer_prompt(*REVIEWER_ARGS, **shape)
        explicit = compose_reviewer_prompt(*REVIEWER_ARGS, dedupe_sent_hashes=None, **shape)

        assert explicit.text == omitted.text
        assert explicit.manifest == omitted.manifest

    # -- SPEC L case 3: an EMPTY set is not None, so the transform really runs -

    @pytest.mark.parametrize("shape_index", range(len(BUILDER_SHAPES)))
    def test_an_empty_sent_set_runs_the_transform_and_still_composes_the_same_bytes(
        self, shape_index: int,
    ):
        # THIS IS THE CASE THAT PROVES THE BYPASS IS ABOUT THE DATA. ``None``
        # skips the transform entirely; ``frozenset()`` walks every segment
        # through it and must still produce the identical bytes, because nothing
        # in an empty set can match a hash.
        shape = BUILDER_SHAPES[shape_index]

        omitted = compose_builder_prompt(*BUILDER_ARGS, **shape)
        empty_set = compose_builder_prompt(*BUILDER_ARGS, dedupe_sent_hashes=frozenset(), **shape)

        assert empty_set.text == omitted.text
        assert empty_set.manifest == omitted.manifest

    def test_an_empty_sent_set_composes_the_same_reviewer_bytes_too(self):
        omitted = compose_reviewer_prompt(*REVIEWER_ARGS, **REVIEWER_SHAPES[1])
        empty_set = compose_reviewer_prompt(
            *REVIEWER_ARGS, dedupe_sent_hashes=frozenset(), **REVIEWER_SHAPES[1]
        )

        assert empty_set.text == omitted.text
        assert empty_set.manifest == omitted.manifest

    # -- SPEC L case 4: the dedupe actually firing ---------------------------

    def test_a_second_composition_against_its_own_recorded_manifest_carries_markers(self):
        # END TO END THROUGH THE REAL INDEX: the sent set is not hand-made. The
        # FIRST composition's own manifest rows are recorded through a real
        # ``SessionSentIndex.record_call(..., ok=True)`` and read back with
        # ``sent_hashes``, so a drift between the composer's hashes and the
        # index's could not land green here.
        shape = BUILDER_SHAPES[2]
        first = compose_builder_prompt(*BUILDER_ARGS, **shape)
        index = SessionSentIndex()
        index.record_call("sess-compose", first.manifest_as_dicts(), ok=True)

        second = compose_builder_prompt(
            *BUILDER_ARGS, dedupe_sent_hashes=index.sent_hashes("sess-compose"), **shape
        )

        replaced = _names_replaced_by_their_marker(second)
        assert replaced, [str(row["name"]) for row in second.manifest_as_dicts()]
        # STRICTLY SHORTER — the whole point of the feature, measured rather
        # than assumed.
        assert len(second.text) < len(first.text)
        # NAMES AND RANKS SURVIVE. The manifest shape is what evidence and the
        # cacheable prefix are keyed on; only text may move.
        first_rows = first.manifest_as_dicts()
        second_rows = second.manifest_as_dicts()
        assert [str(row["name"]) for row in second_rows] == [str(row["name"]) for row in first_rows]
        assert [int(row["rank"]) for row in second_rows] == [int(row["rank"]) for row in first_rows]

    # -- SPEC L case 5: the kill switch, now at the composition seam ---------

    def test_the_kill_switch_composes_the_no_dedupe_bytes_from_the_same_full_set(self):
        # THE POSITIVE CONTROL COMES FIRST, so nothing but the flag differs
        # between the two calls compared below.
        shape = BUILDER_SHAPES[2]
        plain = compose_builder_prompt(*BUILDER_ARGS, **shape)
        index = SessionSentIndex()
        index.record_call("sess-compose", plain.manifest_as_dicts(), ok=True)
        sent = index.sent_hashes("sess-compose")
        assert _names_replaced_by_their_marker(
            compose_builder_prompt(*BUILDER_ARGS, dedupe_sent_hashes=sent, **shape)
        )

        disabled = compose_builder_prompt(
            *BUILDER_ARGS, dedupe_sent_hashes=sent, dedupe_enabled=False, **shape
        )

        assert disabled.text == plain.text
        assert disabled.manifest == plain.manifest

    # -- SPEC L case 6: the scope rule at the call site, negative side -------

    def test_a_chain_that_never_resumes_composes_no_marker_anywhere(self, loop_repo: Path):
        # THE SAFETY PROPERTY OF THIS ROUND, READ OFF THE RUN'S OWN PROMPTS.
        # Providers that do not advertise resume support leave
        # ``builder_resume_ref`` and ``reviewer_resume_ref`` None for every
        # round, so both call sites pass None and no marker can exist.
        providers = TestChainAgainstTheRealLoop._provider_pair(supports_resume=False)

        result = TestChainAgainstTheRealLoop._run(loop_repo, providers, repair_rounds=2)

        assert result.final_status == "staged_review_passed"
        assert len(result.rounds) == 2
        assert result.prompt_traces
        for trace in result.prompt_traces:
            # THE ABSENCE IS ONLY AS WIDE AS THE RECORDED TEXT, so the trace is
            # asserted un-truncated before it is asserted marker-free.
            assert trace.prompt_text_truncated is False, (trace.role, trace.round)
            assert "[unchanged: " not in trace.prompt_text_redacted, (trace.role, trace.round)

    # -- SPEC L case 7: the scope rule at the call site, positive side -------

    def test_a_resumed_repair_chain_composes_a_marker_and_still_completes(self, loop_repo: Path):
        # THE MIRROR OF THE CASE ABOVE, and the one that shows the wiring is
        # live rather than merely harmless. The pair here advertises resume and
        # reports session ids, so round 2 resumes and its composition may skip
        # what round 1 provably delivered to that same session.
        providers = TestChainAgainstTheRealLoop._provider_pair()

        result = TestChainAgainstTheRealLoop._run(loop_repo, providers, repair_rounds=2)

        assert result.final_status == "staged_review_passed"
        marked = [
            (trace.role, trace.round)
            for trace in result.prompt_traces
            if "[unchanged: " in trace.prompt_text_redacted
        ]
        assert marked, [(trace.role, trace.round) for trace in result.prompt_traces]
        # RESUMED SESSION ONLY: round 1 can never carry a marker, because there
        # is nothing proven sent to a session that did not exist yet.
        assert all(round_number > 1 for _, round_number in marked), marked


# ---------------------------------------------------------------------------
# R-0771: A RESUME FALLBACK IS NOT A RESUMED SESSION.
#
# Every case above either composes a prompt directly or drives a chain whose
# resumes SUCCEED. The cases below drive the one path where the loop composes for
# a session it then abandons: a resume attempt that errors, whose retry opens a
# BRAND-NEW session. That new session has been told nothing, so a marker in its
# prompt names content it has never seen — and the segment this feature replaces
# first is ``builder_system``, the one carrying the safety rules about working
# only in staging. These cases exist so that property cannot rot.
#
# THEY READ THE CALLS, NOT THE TRACES. The prompt TRACE for a round is written
# before the provider call, so on the Builder side it describes the composition
# the fallback abandoned rather than the one that was sent; only the arguments
# the provider was really invoked with say what left the loop.


DEDUPE_MARKER_PREFIX = "[unchanged: "


def _capture_role_calls(provider: FakeProvider, method_name: str) -> list[tuple[str | None, str]]:
    """Wrap ONE provider method so every real call is recorded and still happens.

    The wrapper delegates to the bound original and returns its result unchanged,
    so the run stays the real one: nothing here stubs a provider or short-circuits
    a round. Each entry is ``(resume, prompt)``, which is exactly the pair a marker
    claim is about — what was sent, and whether the session it went to had ever
    received the originals.
    """
    calls: list[tuple[str | None, str]] = []
    original = getattr(provider, method_name)

    def wrapper(prompt: str, **kwargs):
        calls.append((kwargs.get("resume"), prompt))
        return original(prompt, **kwargs)

    setattr(provider, method_name, wrapper)
    return calls


@pytest.fixture
def fallback_repo(tmp_path: Path, monkeypatch) -> Path:
    """The demo repo with ``REMEDY_DATA_DIR`` redirected, for the fallback cases.

    Module level, NOT autouse, and under a name no class above uses, so nothing
    already in this file changes behaviour. The repo itself still comes from
    ``TestChainAgainstTheRealLoop._make_repo`` and the providers from that class's
    ``_provider_pair`` — one construction, one place to keep honest, exactly as
    the class above does it.
    """
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return TestChainAgainstTheRealLoop._make_repo(tmp_path / "demo_repo")


class TestAResumeFallbackSendsFullContent:
    """R-0771, pinned against the real loop on both roles."""

    @staticmethod
    def _split(calls: list[tuple[str | None, str]]) -> tuple[list[str], list[str]]:
        """The prompts sent to a FRESH session, and the prompts sent to a resumed one."""
        fresh = [prompt for resume, prompt in calls if resume is None]
        resumed = [prompt for resume, prompt in calls if resume is not None]
        return fresh, resumed

    # -- SPEC O case 1: the builder fallback, the case that must never rot ----

    def test_a_builder_resume_fallback_sends_full_content(self, fallback_repo: Path):
        # THE DISCRIMINATOR FOR THE WHOLE REPAIR. Deleting the two recomposition
        # statements from the Builder fallback branch of ``pingpong_loop.py``
        # restores the defect exactly and fails assertion (b) below.
        builder, reviewer = TestChainAgainstTheRealLoop._provider_pair(
            builder_resume_fails=True,
        )
        calls = _capture_role_calls(builder, "build")

        result = TestChainAgainstTheRealLoop._run(
            fallback_repo, (builder, reviewer), repair_rounds=2,
        )

        # (a) THE FALLBACK REALLY HAPPENED, so this case cannot pass vacuously
        # on a run that never took the branch it is about.
        assert result.final_status == "staged_review_passed"
        assert result.rounds[1].builder_output.resume_fallback is True

        fresh, resumed = self._split(calls)
        # (b) THE PROPERTY R-0771 NAMES: a session that has been told nothing is
        # never told that content it has never seen was previously provided.
        assert fresh
        assert [p for p in fresh if DEDUPE_MARKER_PREFIX in p] == [], [len(p) for p in fresh]
        # (c) AND DEDUPE WAS ON FOR THIS RUN. Without this, (b) would be
        # satisfied by the feature never firing at all and would prove nothing
        # about the fallback.
        assert [p for p in resumed if DEDUPE_MARKER_PREFIX in p] != [], [len(p) for p in resumed]

    # -- SPEC O case 2: the same three assertions on the reviewer side --------

    def test_a_reviewer_resume_fallback_sends_full_content(self, fallback_repo: Path):
        # THE MIRROR, and it needs its own assertions rather than a parametrize:
        # the Reviewer sends ``reviewer_effective`` — the base prompt plus any
        # schema instruction — not ``reviewer_prompt``, so the two roles do not
        # rebind the same names inside their fallback branches.
        builder, reviewer = TestChainAgainstTheRealLoop._provider_pair(
            reviewer_resume_fails=True,
        )
        calls = _capture_role_calls(reviewer, "review")

        result = TestChainAgainstTheRealLoop._run(
            fallback_repo, (builder, reviewer), repair_rounds=2,
        )

        assert result.final_status == "staged_review_passed"
        assert result.rounds[1].reviewer_output.resume_fallback is True

        fresh, resumed = self._split(calls)
        assert fresh
        assert [p for p in fresh if DEDUPE_MARKER_PREFIX in p] == [], [len(p) for p in fresh]
        assert [p for p in resumed if DEDUPE_MARKER_PREFIX in p] != [], [len(p) for p in resumed]

    # -- SPEC O case 3: the evidence agrees with the bytes --------------------

    def test_the_recorded_builder_row_describes_the_bytes_that_were_sent(
        self, fallback_repo: Path,
    ):
        # HOW THE CORRESPONDENCE IS ESTABLISHED, AND WHERE IT STOPS SHORT — read
        # this before strengthening or weakening the assertions. The evidence row
        # carries sha256 values ALONE: no names, no text. A hash cannot be
        # inverted back into a substring of the prompt, so "every recorded hash
        # is a segment of the bytes that were sent" is not decidable from outside
        # the loop, and this case does not claim it.
        #
        # What IS decidable is the thing the defect got wrong. A MARKER's text
        # follows from its name alone, so its hash is computable here via
        # ``_sha256_of_marker``; the round 2 Builder trace records the manifest of
        # the composition the fallback ABANDONED, so the names that composition
        # replaced are readable; and the round 1 trace records those same names at
        # FULL content. This case therefore asserts, for every name the abandoned
        # composition replaced, that the recorded row holds the FULL-content hash
        # and NOT the marker hash — a statement about the segments the defect
        # touched, which is narrower than the sentence above and is written that
        # way on purpose.
        builder, reviewer = TestChainAgainstTheRealLoop._provider_pair(
            builder_resume_fails=True,
        )
        calls = _capture_role_calls(builder, "build")

        result = TestChainAgainstTheRealLoop._run(
            fallback_repo, (builder, reviewer), repair_rounds=2,
        )
        assert result.rounds[1].builder_output.resume_fallback is True

        traces = {
            trace.round: {str(row["name"]): str(row["sha256"]) for row in trace.segment_manifest}
            for trace in result.prompt_traces
            if trace.role == "builder"
        }
        replaced = [name for name, sha in traces[2].items() if sha == _sha256_of_marker(name)]
        # THE POSITIVE CONTROL: the abandoned composition really did replace
        # something, so the loop below is not quantified over nothing.
        assert replaced, sorted(traces[2])

        recorded = set(
            TestChainAgainstTheRealLoop._rows_by_session(result)[
                TestChainAgainstTheRealLoop.BUILDER_SESSION
            ]
        )
        for name in replaced:
            assert name in traces[1], (name, sorted(traces[1]))
            assert _sha256_of_marker(name) not in recorded, name
            assert traces[1][name] in recorded, name
        # AND THE BYTES AGREE WITH THE ROW: the last thing this session was
        # actually sent opened a fresh session and carried no marker at all.
        assert calls[-1][0] is None
        assert DEDUPE_MARKER_PREFIX not in calls[-1][1]

    # -- SPEC O case 4: the round 7 property survives the repair --------------

    def test_a_resumed_chain_that_never_falls_back_still_dedupes(self, fallback_repo: Path):
        # ROUND 7'S PROPERTY, RE-READ OFF THE CALLS RATHER THAN THE TRACES. No
        # role falls back here, so every role must still carry a marker on its
        # resumed call and none may carry one on a call that opened a session.
        builder, reviewer = TestChainAgainstTheRealLoop._provider_pair()
        builder_calls = _capture_role_calls(builder, "build")
        reviewer_calls = _capture_role_calls(reviewer, "review")

        result = TestChainAgainstTheRealLoop._run(
            fallback_repo, (builder, reviewer), repair_rounds=2,
        )

        assert result.final_status == "staged_review_passed"
        assert result.rounds[1].builder_output.resume_fallback is False
        assert result.rounds[1].reviewer_output.resume_fallback is False
        for role, calls in (("builder", builder_calls), ("reviewer", reviewer_calls)):
            fresh, resumed = self._split(calls)
            assert [p for p in resumed if DEDUPE_MARKER_PREFIX in p] != [], role
            assert [p for p in fresh if DEDUPE_MARKER_PREFIX in p] == [], role

"""Tests for F109 semantic dedupe — the per-session sent-hash index
(T001a), the composition hook and its markers (T002), the config kill
switch (T002c) and the trace's record of what was not resent (T003c).

The scope rule of the feature binds every case below: RESUMED SESSION ONLY,
PROVEN SENDS ONLY. So the tests are mostly about what the index REFUSES to
remember — an unsuccessful call, a call with no session id — because a hash the
index holds without proof is a segment the composition hook would later replace
with a marker the model never received.

Hermetic throughout: no network and no sleep anywhere. The unit tests are also
PURE — no tmp_path, no provider — while the later classes deliberately drive
the real ping-pong loop against ``FakeProvider`` in a tmp_path, beginning at
F109 T001b-ii and continuing through every slice that followed it. The
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
from packages.orchestration.prompt_trace import measure_dedupe_savings_from_traces
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
        # ``_sha256_of_marker``; round 2 now records TWO Builder traces — the
        # abandoned resumed composition FIRST, then the full-content call that
        # actually reached the provider, appended by F109 ``R-0774`` — and this
        # case reads the FIRST of them, because the names that abandoned
        # composition replaced are what the assertion is about; and the round 1
        # trace records those same names at FULL content. The selection below
        # therefore collects each round's Builder traces IN ORDER and takes
        # index 0 explicitly, rather than leaning on a dict comprehension's
        # last-wins overwrite: that reliance is finding ``R-0775``, and a third
        # trace would have moved it again in silence. This case therefore
        # asserts, for every name the abandoned composition replaced, that the
        # recorded row holds the FULL-content hash and NOT the marker hash — a
        # statement about the segments the defect touched, which is narrower
        # than the sentence above and is written that way on purpose.
        builder, reviewer = TestChainAgainstTheRealLoop._provider_pair(
            builder_resume_fails=True,
        )
        calls = _capture_role_calls(builder, "build")

        result = TestChainAgainstTheRealLoop._run(
            fallback_repo, (builder, reviewer), repair_rounds=2,
        )
        assert result.rounds[1].builder_output.resume_fallback is True

        builder_traces_by_round: dict[int, list] = {}
        for trace in result.prompt_traces:
            if trace.role == "builder":
                builder_traces_by_round.setdefault(trace.round, []).append(trace)
        traces = {
            round_num: {
                str(row["name"]): str(row["sha256"])
                for row in entries[0].segment_manifest
            }
            for round_num, entries in builder_traces_by_round.items()
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


# ---------------------------------------------------------------------------
# T002c: A COMPOSED PROMPT REPORTS THE SEGMENTS IT REPLACED.
#
# ``_dedupe_resumed_segments`` has always returned the replaced NAMES, and both
# compose functions used to throw them away. They now ride back on
# ``ComposedPrompt.deduped_names``, so a later reader can see what the model was
# NOT sent again instead of re-deriving it from hashes.
#
# EVERY POSITIVE CASE BELOW IS PAIRED WITH A MEASUREMENT OF THE SEGMENT IT
# NAMES. A report is only worth having if it names the segments that actually
# shrank; a name a caller had simply invented would satisfy "the report is
# non-empty" and prove nothing, so cases 3 and 4 tie each reported name to a
# manifest row of exactly marker length and each unreported name to its
# unchanged hash.


class TestTheComposedPromptReportsTheNamesItReplaced:
    """SPEC T: ``deduped_names`` on both roles, pure and through the real loop."""

    BUILDER_SHAPE = BUILDER_SHAPES[2]
    REVIEWER_SHAPE = REVIEWER_SHAPES[1]
    SESSION = "sess-report"

    @classmethod
    def _builder_pair(cls) -> tuple:
        """A builder composition, and a second one against its OWN recorded manifest.

        The sent set is built the way round 7's cases build it — through a real
        ``SessionSentIndex.record_call(..., ok=True)`` over the first
        composition's manifest rows — never from a hand-made hash, so a drift
        between the composer's digests and the index's could not land green here.
        """
        first = compose_builder_prompt(*BUILDER_ARGS, **cls.BUILDER_SHAPE)
        index = SessionSentIndex()
        index.record_call(cls.SESSION, first.manifest_as_dicts(), ok=True)
        second = compose_builder_prompt(
            *BUILDER_ARGS,
            dedupe_sent_hashes=index.sent_hashes(cls.SESSION),
            **cls.BUILDER_SHAPE,
        )
        return first, second

    @classmethod
    def _reviewer_pair(cls) -> tuple:
        """The reviewer half of ``_builder_pair``, built the same way."""
        first = compose_reviewer_prompt(*REVIEWER_ARGS, **cls.REVIEWER_SHAPE)
        index = SessionSentIndex()
        index.record_call(cls.SESSION, first.manifest_as_dicts(), ok=True)
        second = compose_reviewer_prompt(
            *REVIEWER_ARGS,
            dedupe_sent_hashes=index.sent_hashes(cls.SESSION),
            **cls.REVIEWER_SHAPE,
        )
        return first, second

    # -- SPEC T case 1: a composition that deduped nothing reports nothing ----

    @pytest.mark.parametrize("explicit_none", [False, True])
    def test_a_composition_that_dedupes_nothing_reports_no_names(self, explicit_none: bool):
        # BOTH ROLES, AND BOTH SHAPES OF "no dedupe": the argument omitted, and
        # the argument passed explicitly as ``None``. This is also the case that
        # would go red if the keyword were passed only on the branch that really
        # replaced something, because then the empty case would take a different
        # code path from the full one.
        extra = {"dedupe_sent_hashes": None} if explicit_none else {}

        builder = compose_builder_prompt(*BUILDER_ARGS, **extra, **self.BUILDER_SHAPE)
        reviewer = compose_reviewer_prompt(*REVIEWER_ARGS, **extra, **self.REVIEWER_SHAPE)

        assert builder.deduped_names == ()
        assert reviewer.deduped_names == ()

    # -- SPEC T case 2: what really deduped is exactly what is reported -------

    def test_a_composition_that_dedupes_reports_exactly_the_names_it_replaced(self):
        # THE SECOND READER IS INDEPENDENT OF THE REPORT:
        # ``_names_replaced_by_their_marker`` decides membership from the
        # manifest's own sha256 against the marker text a name produces, so it
        # neither reads ``deduped_names`` nor can be read from it.
        _, builder = self._builder_pair()
        _, reviewer = self._reviewer_pair()

        assert list(builder.deduped_names) == _names_replaced_by_their_marker(builder)
        assert list(reviewer.deduped_names) == _names_replaced_by_their_marker(reviewer)
        # NOT VACUOUS: both roles really replaced something here, so the equality
        # above is not two empty lists agreeing with each other.
        assert builder.deduped_names != ()
        assert reviewer.deduped_names != ()

    # -- SPEC T case 3: each reported name shrank to exactly its own marker ---

    def test_every_reported_name_names_a_segment_that_shrank_to_its_marker(self):
        _, builder = self._builder_pair()

        rows = {str(row["name"]): int(row["chars"]) for row in builder.manifest_as_dicts()}
        assert builder.deduped_names != ()
        for name in builder.deduped_names:
            # IN THE MANIFEST AT ALL — a reported name the manifest never held
            # would be an invented one.
            assert name in rows, (name, sorted(rows))
            assert rows[name] == len(dedupe_marker_for_segment(name)), name

    # -- SPEC T case 4: the negative half, which is what makes case 3 mean it -

    def test_a_segment_the_report_omits_kept_its_original_hash(self):
        first, second = self._builder_pair()

        before = {str(row["name"]): str(row["sha256"]) for row in first.manifest_as_dicts()}
        after = {str(row["name"]): str(row["sha256"]) for row in second.manifest_as_dicts()}
        untouched = [name for name in after if name not in second.deduped_names]
        assert untouched, sorted(after)
        for name in untouched:
            assert after[name] == before[name], name

    # -- SPEC T case 5: the report as the REAL loop produces it ---------------

    @staticmethod
    def _capture_compositions(monkeypatch) -> list:
        """Record every ``ComposedPrompt`` the loop's own compose calls return.

        The wrappers delegate to the originals and return their results
        unchanged — exactly what ``_capture_role_calls`` does for a provider —
        so the run below stays the real one. The composed object itself never
        reaches ``PingPongResult`` (a prompt trace carries the manifest, not the
        report), so wrapping the two functions in the loop's own module namespace
        is how the LOOP's compositions are read without widening production code
        that has no consumer for the report yet.
        """
        import packages.orchestration.pingpong_loop as loop

        composed: list = []

        def wrap(function_name: str) -> None:
            original = getattr(loop, function_name)

            def wrapper(*args, **kwargs):
                result = original(*args, **kwargs)
                composed.append(result)
                return result

            monkeypatch.setattr(loop, function_name, wrapper)

        wrap("compose_builder_prompt")
        wrap("compose_reviewer_prompt")
        return composed

    def test_a_resumed_chain_reports_the_names_it_replaced(
        self, fallback_repo: Path, monkeypatch,
    ):
        composed = self._capture_compositions(monkeypatch)
        providers = TestChainAgainstTheRealLoop._provider_pair()

        result = TestChainAgainstTheRealLoop._run(fallback_repo, providers, repair_rounds=2)

        assert result.final_status == "staged_review_passed"
        assert composed
        assert [prompt.deduped_names for prompt in composed if prompt.deduped_names] != []

    def test_a_chain_that_never_resumes_reports_nothing_anywhere(
        self, fallback_repo: Path, monkeypatch,
    ):
        # THE MIRROR, and the reason the case above is about the scope rule
        # rather than about the field existing: providers that do not advertise
        # resume leave both resume refs None, so no composition can dedupe and
        # none may report a name.
        composed = self._capture_compositions(monkeypatch)
        providers = TestChainAgainstTheRealLoop._provider_pair(supports_resume=False)

        result = TestChainAgainstTheRealLoop._run(fallback_repo, providers, repair_rounds=2)

        assert result.final_status == "staged_review_passed"
        assert composed
        assert [prompt.deduped_names for prompt in composed if prompt.deduped_names] == []


# ---------------------------------------------------------------------------
# T002c, the config KILL SWITCH.
#
# ``run_pingpong`` carries ``semantic_dedupe_enabled``, forwarded to both
# PRIMARY compositions as ``dedupe_enabled``. The flag is tested in exactly one
# place — ``should_dedupe_segment`` consults ``enabled`` first and alone, and
# ``_dedupe_resumed_segments`` returns the segments untouched on False — so the
# loop only has to hand it down, and these cases are about the handing down.
#
# THEY DRIVE THE REAL LOOP because a parameter that is accepted and then ignored
# at a call site is invisible to any re-composition: a re-composition asserts
# what the test itself passed in, and only the run's own prompts and calls say
# what the loop composed.
#
# THE RESUME FALLBACK IS OUTSIDE THE SWITCH BY CONSTRUCTION: the fallback
# recompositions pass no dedupe argument at all, so they send full content at
# either value. Case 4 pins that, because "R-0771 still holds" is exactly the
# property a new parameter threaded through this call site is most likely to
# have broken.


class TestTheSemanticDedupeKillSwitch:
    """SPEC W: ``semantic_dedupe_enabled`` through the real loop, on and off."""

    @staticmethod
    def _marked_traces(result) -> list[tuple[str, int]]:
        """Every recorded prompt carrying a marker, as ``(role, round)`` pairs.

        An absence is only as wide as the text it was searched in, so every
        trace is asserted UN-TRUNCATED before it is read — the same guard
        ``test_a_chain_that_never_resumes_composes_no_marker_anywhere`` applies,
        for the same reason.
        """
        for trace in result.prompt_traces:
            assert trace.prompt_text_truncated is False, (trace.role, trace.round)
        return [
            (trace.role, trace.round)
            for trace in result.prompt_traces
            if DEDUPE_MARKER_PREFIX in trace.prompt_text_redacted
        ]

    # -- SPEC W case 1: the switch works, and only the switch differs ---------

    def test_the_switch_alone_decides_whether_a_resumed_chain_carries_a_marker(
        self, fallback_repo: Path,
    ):
        # ONE CASE, TWO RUNS, ONE FIXTURE, ON PURPOSE. The claim is a
        # DIFFERENCE — the disabled run composes no marker where the otherwise
        # identical default run does — and a difference split across two cases is
        # two claims that could both hold while the runs differed in something
        # else as well. Same repo, same provider construction, same repair
        # budget; ``semantic_dedupe_enabled`` is the only argument that moves,
        # and the second run does not even name it.
        disabled = TestChainAgainstTheRealLoop._run(
            fallback_repo,
            TestChainAgainstTheRealLoop._provider_pair(),
            repair_rounds=2,
            semantic_dedupe_enabled=False,
        )
        default = TestChainAgainstTheRealLoop._run(
            fallback_repo,
            TestChainAgainstTheRealLoop._provider_pair(),
            repair_rounds=2,
        )

        # BOTH RUNS STILL COMPLETE. A switch that changed the outcome would not
        # be a kill switch, it would be a second code path.
        assert disabled.final_status == "staged_review_passed"
        assert default.final_status == "staged_review_passed"
        assert disabled.prompt_traces
        assert default.prompt_traces
        # THE POSITIVE CONTROL FIRST, so the emptiness below is about the flag
        # rather than about a chain that never resumed.
        assert self._marked_traces(default) != []
        assert self._marked_traces(disabled) == []

    # -- SPEC W case 2: the deduped-name report agrees with the switch --------

    def test_a_disabled_run_reports_no_deduped_names_on_any_composition(
        self, fallback_repo: Path, monkeypatch,
    ):
        # THE COMPOSED OBJECTS ARE READ THE WAY SPEC T CASE 5 READS THEM, through
        # that class's own capture helper, because the report never reaches
        # ``PingPongResult``. The positive half already lives there:
        # ``test_a_resumed_chain_reports_the_names_it_replaced`` runs this very
        # chain at the default flag and finds names, so this case mirrors a
        # measured run rather than an assumption.
        composed = TestTheComposedPromptReportsTheNamesItReplaced._capture_compositions(
            monkeypatch,
        )
        providers = TestChainAgainstTheRealLoop._provider_pair()

        result = TestChainAgainstTheRealLoop._run(
            fallback_repo, providers, repair_rounds=2, semantic_dedupe_enabled=False,
        )

        assert result.final_status == "staged_review_passed"
        assert composed
        # THE CHAIN REALLY RESUMED: two rounds ran and both seams recorded proven
        # sends, so round 2 composed against a POPULATED index and would have
        # deduped had the flag not said otherwise.
        assert len(result.rounds) == 2
        assert sorted(TestChainAgainstTheRealLoop._rows_by_session(result)) == [
            TestChainAgainstTheRealLoop.BUILDER_SESSION,
            TestChainAgainstTheRealLoop.REVIEWER_SESSION,
        ]
        assert [prompt.deduped_names for prompt in composed if prompt.deduped_names] == []

    # -- SPEC W case 3: the resume condition, not the flag, gates the marker --

    @pytest.mark.parametrize("enabled", [True, False])
    def test_a_chain_that_never_resumes_composes_no_marker_at_either_flag_value(
        self, fallback_repo: Path, enabled: bool,
    ):
        # THE FLAG MUST NOT BECOME THE ONLY THING STANDING BETWEEN A FRESH CALL
        # AND A MARKER — the resume condition is, and it holds at BOTH values.
        # Without this case a switch wired permanently to False would satisfy
        # every absence claim in this class and prove nothing about the scope
        # rule the feature actually turns on.
        providers = TestChainAgainstTheRealLoop._provider_pair(supports_resume=False)

        result = TestChainAgainstTheRealLoop._run(
            fallback_repo, providers, repair_rounds=2, semantic_dedupe_enabled=enabled,
        )

        assert result.final_status == "staged_review_passed"
        assert result.prompt_traces
        assert self._marked_traces(result) == []

    # -- SPEC W case 4: the fallback stays outside the switch -----------------

    @pytest.mark.parametrize("enabled", [True, False])
    def test_a_builder_resume_fallback_sends_full_content_at_either_flag_value(
        self, fallback_repo: Path, enabled: bool,
    ):
        # R-0771'S PROPERTY, RE-ASSERTED UNDER THE NEW PARAMETER and read off the
        # CALLS rather than the traces. Since R-0774 the fallback round records
        # TWO Builder traces — the composition the fallback ABANDONED first, then
        # the full-content call that actually left the loop — so a trace-based
        # reading would have to choose between them, while the calls say which
        # bytes left the loop without choosing. R-0777 corrected this comment,
        # which described a single trace.
        builder, reviewer = TestChainAgainstTheRealLoop._provider_pair(
            builder_resume_fails=True,
        )
        calls = _capture_role_calls(builder, "build")

        result = TestChainAgainstTheRealLoop._run(
            fallback_repo, (builder, reviewer), repair_rounds=2,
            semantic_dedupe_enabled=enabled,
        )

        assert result.final_status == "staged_review_passed"
        assert result.rounds[1].builder_output.resume_fallback is True

        fresh, resumed = TestAResumeFallbackSendsFullContent._split(calls)
        # THE FALLBACK OPENED A FRESH SESSION AND CARRIED NO MARKER, at either
        # value, because that recomposition passes no dedupe argument at all.
        assert fresh
        assert [p for p in fresh if DEDUPE_MARKER_PREFIX in p] == [], [len(p) for p in fresh]
        # AND THE FLAG STILL GOVERNED THE CALLS IT DOES GOVERN, so neither half
        # of this case can pass because dedupe was simply off everywhere.
        assert resumed
        marked_resumed = [p for p in resumed if DEDUPE_MARKER_PREFIX in p]
        assert (marked_resumed != []) is enabled, (enabled, len(resumed), len(marked_resumed))
# ---------------------------------------------------------------------------
# R-0774: ONE PROMPT TRACE PER ACTUAL PROVIDER INVOCATION, ON A RESUME FALLBACK.
#
# A resume fallback makes a SECOND provider call in the same round, with a
# prompt RECOMPOSED AT FULL CONTENT. Until this round the Builder wrote its
# trace two statements BEFORE that recomposition and never wrote another, so the
# only Builder trace of a fallback round described the composition the loop had
# just ABANDONED: ``prompt_sha256``, ``prompt_chars``, ``segment_manifest`` and
# ``prompt_text_redacted`` all reported bytes the provider never received. That
# is a FALSE live indicator in the evidence rather than a missing one.
#
# WHY THESE CASES READ THE TRACES AND SPEC O'S READ THE CALLS. SPEC O asserts
# what LEFT the loop and deliberately refuses to trust the traces, because at
# that time the traces were the broken artefact. These cases assert that the
# traces now AGREE with those same calls, so the two sets are complementary and
# neither replaces the other. Every length compared below is taken from
# ``_split(calls)`` rather than written down, so a fixture change moves both
# sides together instead of pinning today's byte count.


class TestATraceIsRecordedForEveryProviderInvocation:
    """SPEC Z: R-0774, pinned against the real loop on both roles."""

    @staticmethod
    def _role_traces(result, role: str, round_number: int) -> list:
        """Every trace of one ROLE in one ROUND, in the order it was recorded.

        Each trace is asserted UN-TRUNCATED before any caller reads it: a marker
        ABSENCE is only as wide as the recorded text, so a truncated entry could
        satisfy "carries no marker" by having dropped the marker. This is the
        guard ``TestTheSemanticDedupeKillSwitch._marked_traces`` applies, for the
        same reason.
        """
        for trace in result.prompt_traces:
            assert trace.prompt_text_truncated is False, (trace.role, trace.round)
        return [
            trace for trace in result.prompt_traces
            if trace.role == role and trace.round == round_number
        ]

    # -- SPEC Z case 1: the builder fallback ---------------------------------

    def test_a_builder_resume_fallback_records_the_bytes_it_actually_sent(
        self, fallback_repo: Path,
    ):
        # THE DISCRIMINATOR FOR THE BUILDER HALF OF THE REPAIR. Deleting the
        # second ``result.prompt_traces.append`` from the Builder fallback branch
        # of ``pingpong_loop.py`` restores the defect exactly and fails
        # assertion (b) below on its very first line.
        builder, reviewer = TestChainAgainstTheRealLoop._provider_pair(
            builder_resume_fails=True,
        )
        calls = _capture_role_calls(builder, "build")

        result = TestChainAgainstTheRealLoop._run(
            fallback_repo, (builder, reviewer), repair_rounds=2,
        )

        # (a) THE FALLBACK REALLY FIRED, so this case cannot pass vacuously on a
        # run that never took the branch it is about.
        assert result.final_status == "staged_review_passed"
        fallback_round = result.rounds[1]
        assert fallback_round.builder_output.resume_fallback is True

        # (b) TWO INVOCATIONS, TWO TRACES — the abandoned resumed attempt keeps
        # its own honest record, and the call that actually reached the provider
        # finally gets one.
        traces = self._role_traces(result, "builder", fallback_round.round_number)
        assert len(traces) == 2, [t.prompt_chars for t in traces]
        assert DEDUPE_MARKER_PREFIX in traces[0].prompt_text_redacted
        assert DEDUPE_MARKER_PREFIX not in traces[1].prompt_text_redacted

        # (c) AND THE SECOND TRACE DESCRIBES THE BYTES THAT LEFT THE LOOP. The
        # length comes from the fresh-session call itself, so this pins the
        # correspondence rather than today's prompt size.
        fresh, resumed = TestAResumeFallbackSendsFullContent._split(calls)
        assert fresh
        assert traces[1].prompt_chars == len(fresh[-1]), (
            traces[1].prompt_chars, [len(p) for p in fresh],
        )
        # AND DEDUPE WAS ON, so (b)'s marker assertions are about the fallback
        # rather than about a run in which the feature never fired.
        assert [p for p in resumed if DEDUPE_MARKER_PREFIX in p] != []

    # -- SPEC Z case 2: the reviewer fallback, the same claim ----------------

    def test_a_reviewer_resume_fallback_records_the_bytes_it_actually_sent(
        self, fallback_repo: Path,
    ):
        # THE MIRROR, AND IT NEEDS ITS OWN CASE RATHER THAN A PARAMETRIZE. This
        # role reaches the property by a different route: its traces are written
        # by the ``on_call=_rev_trace(...)`` callback, which ``_call_with_retry``
        # fires once per ACTUAL invocation and which reads ``reviewer_composed``
        # at call time, so it picks up the fallback rebinding on its own. The
        # DISCRIMINATOR is therefore that callback: dropping ``on_call`` from the
        # Reviewer fallback's ``_call_with_retry`` fails assertion (b) here.
        # Pinning it matters precisely because nothing in the Reviewer branch
        # looks like the Builder's explicit append.
        builder, reviewer = TestChainAgainstTheRealLoop._provider_pair(
            reviewer_resume_fails=True,
        )
        calls = _capture_role_calls(reviewer, "review")

        result = TestChainAgainstTheRealLoop._run(
            fallback_repo, (builder, reviewer), repair_rounds=2,
        )

        assert result.final_status == "staged_review_passed"
        fallback_round = result.rounds[1]
        assert fallback_round.reviewer_output.resume_fallback is True

        traces = self._role_traces(result, "reviewer", fallback_round.round_number)
        assert len(traces) == 2, [t.prompt_chars for t in traces]
        assert DEDUPE_MARKER_PREFIX in traces[0].prompt_text_redacted
        assert DEDUPE_MARKER_PREFIX not in traces[1].prompt_text_redacted

        fresh, resumed = TestAResumeFallbackSendsFullContent._split(calls)
        assert fresh
        assert traces[1].prompt_chars == len(fresh[-1]), (
            traces[1].prompt_chars, [len(p) for p in fresh],
        )
        assert [p for p in resumed if DEDUPE_MARKER_PREFIX in p] != []

    # -- SPEC Z case 3: the discriminator against an unconditional append ----

    def test_a_chain_that_never_falls_back_records_one_trace_per_role_per_round(
        self, fallback_repo: Path,
    ):
        # WITHOUT THIS CASE, CASES 1 AND 2 WOULD BOTH PASS ON A LOOP THAT HAD
        # SIMPLY BEGUN APPENDING A SECOND TRACE UNCONDITIONALLY — a different
        # defect wearing the same green, and a worse one, because it would
        # double-count every call in ``call_segments`` rather than mis-describe
        # the rare one. No role falls back here, so every role must record
        # EXACTLY ONE trace in EVERY round.
        providers = TestChainAgainstTheRealLoop._provider_pair()

        result = TestChainAgainstTheRealLoop._run(
            fallback_repo, providers, repair_rounds=2,
        )

        assert result.final_status == "staged_review_passed"
        # THE POSITIVE CONTROL: more than one round ran, and neither role fell
        # back, so "one trace per role per round" is a claim about a chain that
        # really had the opportunity to record a second one.
        assert len(result.rounds) == 2
        for round_data in result.rounds:
            assert round_data.builder_output.resume_fallback is False
            assert round_data.reviewer_output.resume_fallback is False
            for role in ("builder", "reviewer"):
                traces = self._role_traces(result, role, round_data.round_number)
                assert len(traces) == 1, (
                    role, round_data.round_number, [t.prompt_chars for t in traces],
                )


# ---------------------------------------------------------------------------
# T003c: THE TRACE RECORDS WHAT THE MODEL DID NOT RECEIVE AGAIN.
#
# `PromptTraceEntry.deduped_segment_names` carries the names whose TEXT the
# composition behind that trace replaced with a marker. It is derived from
# `composed_prompt` at the same seam `segment_manifest` already uses, so a trace
# can never describe one prompt's bytes with another prompt's withholdings.
#
# THESE CASES DRIVE THE REAL LOOP. The unit-level claims about the derivation
# live in tests/orchestration/test_prompt_trace.py; what is only decidable here
# is that the loop's OWN compositions reach the field — a derivation that is
# correct in isolation proves nothing about a call site that never passes the
# composed object down.


class TestTheTraceNamesWhatWasNotResent:
    """SPEC E: `deduped_segment_names` through the real loop, on both flag values."""

    @staticmethod
    def _untruncated(result) -> list:
        """Every trace of the run, each asserted UN-TRUNCATED before it is read.

        The same guard `TestTheSemanticDedupeKillSwitch._marked_traces` and
        `TestATraceIsRecordedForEveryProviderInvocation._role_traces` apply, and
        it is applied here for the neighbouring reads rather than for the new
        field itself: `prompt_text_redacted` and the marker searches below are
        only as wide as the bytes that survived the cap. `deduped_segment_names`
        is a list the cap never touches, so this guard is honest about covering
        the readings around it and keeps one convention across the file.
        """
        for trace in result.prompt_traces:
            assert trace.prompt_text_truncated is False, (trace.role, trace.round)
        return list(result.prompt_traces)

    # -- SPEC E case 4: a resumed chain records the names it did not resend ----

    def test_a_resumed_chain_records_the_names_it_did_not_resend(self, fallback_repo: Path):
        # NEITHER ROLE FALLS BACK HERE, so every role records exactly one trace
        # per round and the round 2 Builder trace IS the composition that left
        # the loop — no choosing between two.
        providers = TestChainAgainstTheRealLoop._provider_pair()

        result = TestChainAgainstTheRealLoop._run(fallback_repo, providers, repair_rounds=2)

        assert result.final_status == "staged_review_passed"
        self._untruncated(result)
        # (a) NON-VACUITY FIRST: the chain really resumed. Two rounds ran, the
        # Builder did not fall back, and both seams recorded a proven send — so
        # round 2 composed against a POPULATED index and had something to
        # withhold. Without this the emptiness assertions below would be
        # satisfied by a chain that never got the chance to dedupe.
        assert len(result.rounds) == 2
        assert result.rounds[1].builder_output.resume_fallback is False
        assert sorted(TestChainAgainstTheRealLoop._rows_by_session(result)) == [
            TestChainAgainstTheRealLoop.BUILDER_SESSION,
            TestChainAgainstTheRealLoop.REVIEWER_SESSION,
        ]

        first = TestATraceIsRecordedForEveryProviderInvocation._role_traces(
            result, "builder", 1,
        )
        second = TestATraceIsRecordedForEveryProviderInvocation._role_traces(
            result, "builder", result.rounds[1].round_number,
        )
        assert len(first) == 1, [t.prompt_chars for t in first]
        assert len(second) == 1, [t.prompt_chars for t in second]
        # (b) ROUND 1 OPENED THE SESSION, so it withheld nothing and names nothing.
        assert first[0].deduped_segment_names == []
        # (c) ROUND 2 RESUMED IT, and says what it withheld.
        assert second[0].deduped_segment_names != []
        # (d) THE TWO READINGS OF ONE TRACE AGREE. A marker row is still a
        # manifest row, so every withheld name is still named by that same
        # trace's manifest; a name in one and not the other would mean the two
        # fields describe different compositions.
        manifest_names = {str(row["name"]) for row in second[0].segment_manifest}
        for name in second[0].deduped_segment_names:
            assert name in manifest_names, (name, sorted(manifest_names))

    # -- SPEC E case 5: the fallback's two traces disagree, and that is the point

    def test_the_fallbacks_two_builder_traces_disagree_about_what_was_withheld(
        self, fallback_repo: Path,
    ):
        # WHAT TIES THIS FIELD TO `R-0774`'S REPAIR. The fallback round makes TWO
        # Builder calls: the resumed composition that withheld segments, then the
        # full-content recomposition that actually reached the provider. With
        # only the first traced — the state before `R-0774` — the round's single
        # trace would have reported withheld names for a call that re-sent every
        # byte in full, which is a FALSE live indicator rather than a missing one.
        builder, reviewer = TestChainAgainstTheRealLoop._provider_pair(
            builder_resume_fails=True,
        )

        result = TestChainAgainstTheRealLoop._run(
            fallback_repo, (builder, reviewer), repair_rounds=2,
        )

        assert result.final_status == "staged_review_passed"
        fallback_round = result.rounds[1]
        assert fallback_round.builder_output.resume_fallback is True
        self._untruncated(result)

        traces = TestATraceIsRecordedForEveryProviderInvocation._role_traces(
            result, "builder", fallback_round.round_number,
        )
        assert len(traces) == 2, [t.prompt_chars for t in traces]
        # THE ABANDONED COMPOSITION WITHHELD SEGMENTS, and its own bytes carry
        # the markers that withholding produced.
        assert traces[0].deduped_segment_names != []
        assert DEDUPE_MARKER_PREFIX in traces[0].prompt_text_redacted
        # THE CALL THAT REACHED THE PROVIDER WITHHELD NOTHING, and its bytes
        # agree: a fresh session was told nothing was previously provided.
        assert traces[1].deduped_segment_names == []
        assert DEDUPE_MARKER_PREFIX not in traces[1].prompt_text_redacted

    # -- SPEC E case 6: the field is wired to the dedupe decision, not to a role

    def test_a_disabled_run_names_nothing_on_any_trace(self, fallback_repo: Path):
        # THE DISCRIMINATOR AGAINST THE FIELD BEING WIRED TO SOMETHING OTHER THAN
        # THE DEDUPE DECISION. This is the very chain case 4 finds names on, with
        # `semantic_dedupe_enabled` the only argument that moves, so an empty
        # report here is about the flag rather than about a chain that never
        # resumed.
        providers = TestChainAgainstTheRealLoop._provider_pair()

        result = TestChainAgainstTheRealLoop._run(
            fallback_repo, providers, repair_rounds=2, semantic_dedupe_enabled=False,
        )

        assert result.final_status == "staged_review_passed"
        # NON-VACUITY, the same two readings case 4 makes: two rounds ran and
        # both seams recorded a proven send, so round 2 composed against a
        # populated index and would have withheld had the flag not said no.
        assert len(result.rounds) == 2
        assert sorted(TestChainAgainstTheRealLoop._rows_by_session(result)) == [
            TestChainAgainstTheRealLoop.BUILDER_SESSION,
            TestChainAgainstTheRealLoop.REVIEWER_SESSION,
        ]

        traces = self._untruncated(result)
        assert traces
        assert [t.deduped_segment_names for t in traces if t.deduped_segment_names] == []


# ---------------------------------------------------------------------------
# SPEC H cases 6-7: THE SAVING, MEASURED FROM THE RUN'S OWN RECORD.
# The exact arithmetic of `measure_dedupe_savings_from_traces` is pinned in
# `tests/orchestration/test_prompt_trace.py` on hand-built entries, where the
# numbers can be chosen and cannot drift. What only the real loop can show is
# that a genuine resumed chain produces a trace record the function can measure
# at all — and that switching the feature off collapses that reading to nothing
# without inventing an unmeasured name to explain it.
# ---------------------------------------------------------------------------


class TestTheRunsOwnTraceMeasuresWhatItWithheld:
    """SPEC H: `measure_dedupe_savings_from_traces` driven by the real loop."""

    @staticmethod
    def _reported_names(result) -> list[str]:
        """Every name any trace of the run reported as withheld, in trace order."""
        return [
            name
            for trace in result.prompt_traces
            for name in trace.deduped_segment_names
        ]

    # -- SPEC H case 6: a resumed chain saved something, and it is measurable --

    def test_a_resumed_chain_reports_a_positive_net_saving(self, fallback_repo: Path):
        providers = TestChainAgainstTheRealLoop._provider_pair()

        result = TestChainAgainstTheRealLoop._run(
            fallback_repo, providers, repair_rounds=2,
        )

        # (a) NON-VACUITY FIRST: the chain really resumed. Two rounds ran, the
        # Builder did not fall back, both seams recorded a proven send, and some
        # trace does report a withheld name — without which every assertion
        # below would be satisfied by a run that never deduped anything.
        assert result.final_status == "staged_review_passed"
        assert len(result.rounds) == 2
        assert result.rounds[1].builder_output.resume_fallback is False
        assert sorted(TestChainAgainstTheRealLoop._rows_by_session(result)) == [
            TestChainAgainstTheRealLoop.BUILDER_SESSION,
            TestChainAgainstTheRealLoop.REVIEWER_SESSION,
        ]
        reported = self._reported_names(result)
        assert reported != []

        measured = measure_dedupe_savings_from_traces(list(result.prompt_traces))

        # (b) EVERY REPORTED OCCURRENCE WAS MEASURABLE from this run's own
        # record. The run opened both sessions itself, so nothing here was
        # withheld against a full send that happened before the trace begins.
        assert measured.unmeasured_segment_names == ()
        assert measured.deduped_occurrences_counted == len(reported)
        # (c) AND THE SAVING IS NET, not gross: a marker costs characters of its
        # own, this run paid them, and what is left over is still positive.
        assert measured.chars_spent_on_markers > 0
        assert measured.chars_avoided > measured.chars_spent_on_markers
        assert measured.net_chars_saved == (
            measured.chars_avoided - measured.chars_spent_on_markers
        )
        assert measured.net_chars_saved > 0

    # -- SPEC H case 7: the discriminator, on the same chain with the flag off -

    def test_a_disabled_run_reports_zero_and_names_nothing_unmeasured(
        self, fallback_repo: Path,
    ):
        # THE DISCRIMINATOR THAT STOPS CASE 6 PASSING on a function that reports
        # activity whatever the run did. This is case 6's chain with
        # `semantic_dedupe_enabled` the only argument that moves, so a zero here
        # is about the flag rather than about a chain that never resumed. THE
        # EMPTY UNMEASURED FIELD IS THE SECOND HALF: a run that withheld nothing
        # has nothing it failed to measure, and a function that named a segment
        # here would be inventing an excuse for its own zero.
        providers = TestChainAgainstTheRealLoop._provider_pair()

        result = TestChainAgainstTheRealLoop._run(
            fallback_repo, providers, repair_rounds=2, semantic_dedupe_enabled=False,
        )

        assert result.final_status == "staged_review_passed"
        assert len(result.rounds) == 2
        assert sorted(TestChainAgainstTheRealLoop._rows_by_session(result)) == [
            TestChainAgainstTheRealLoop.BUILDER_SESSION,
            TestChainAgainstTheRealLoop.REVIEWER_SESSION,
        ]
        assert self._reported_names(result) == []

        measured = measure_dedupe_savings_from_traces(list(result.prompt_traces))

        assert measured.chars_avoided == 0
        assert measured.chars_spent_on_markers == 0
        assert measured.net_chars_saved == 0
        assert measured.deduped_occurrences_counted == 0
        assert measured.unmeasured_segment_names == ()

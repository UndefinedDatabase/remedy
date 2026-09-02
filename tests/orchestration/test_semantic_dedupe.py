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
    SessionSentIndex,
    SessionSentIndexError,
    invalidate_on_resume_fallback,
    record_finalized_call,
    session_id_of_finalized_call,
    session_sent_index_from_evidence,
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
    """F109 T001b-ii: THESE CASES RUN THE REAL LOOP.

    Every test above is a pure unit test of the index. Every test here drives
    ``run_pingpong`` end to end against ``FakeProvider`` and then reads
    ``PingPongResult.session_sent_evidence`` — they are the first cases in this
    feature proving the index is fed by ACTUAL provider calls rather than by a
    hand-built manifest. Both fixtures are declared inside this class on
    purpose, so the pure tests above keep touching no tmp_path and no provider.
    """

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
    def _run(repo: Path, provider: FakeProvider, **kwargs):
        return run_pingpong(
            "Fix README", str(repo),
            builder_provider=provider, reviewer_provider=provider,
            **kwargs,
        )

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

    def test_a_resumed_two_round_chain_populates_the_evidence(self, demo_repo: Path):
        provider = FakeProvider(
            fail_on_round=1, pass_on_round=2,
            supports_resume=True, fake_session_id="sess-1",
        )
        result = self._run(demo_repo, provider, repair_rounds=2)

        assert result.session_sent_evidence != []
        assert len(result.session_sent_evidence) == 1
        row = result.session_sent_evidence[0]
        assert row["session_id"] == "sess-1"
        assert row["sent_sha256"] != []
        assert row["sent_sha256"] == sorted(row["sent_sha256"])

    def test_every_recorded_hash_is_a_real_segment_hash(self, demo_repo: Path):
        provider = FakeProvider(
            fail_on_round=1, pass_on_round=2,
            supports_resume=True, fake_session_id="sess-1",
        )
        result = self._run(demo_repo, provider, repair_rounds=2)

        hashes = result.session_sent_evidence[0]["sent_sha256"]
        assert hashes
        for digest in hashes:
            assert len(digest) == 64, digest
            assert set(digest) <= set("0123456789abcdef"), digest

    def test_a_provider_that_reports_no_session_id_records_nothing(self, demo_repo: Path):
        # The proven-sends-only rule surviving contact with the loop: with no
        # session named, there is no session to remember anything against.
        provider = FakeProvider(fail_on_round=1, pass_on_round=2, supports_resume=True)
        result = self._run(demo_repo, provider, repair_rounds=2)

        assert result.session_sent_evidence == []

    def test_a_single_round_run_records_its_session_even_though_it_never_resumed(
        self, demo_repo: Path, tmp_path: Path,
    ):
        # PINNED FROM REAL RUNS, not from expectation. Recording is keyed on a
        # PROVEN send that names a session, and a first round proves exactly
        # that; "resumed session only" governs the composition hook (T002), not
        # what the index is permitted to remember.
        sessionless = self._run(demo_repo, FakeProvider())
        assert len(sessionless.rounds) == 1
        assert sessionless.session_sent_evidence == []

        named = self._run(
            self._make_repo(tmp_path / "repo_named"),
            FakeProvider(supports_resume=True, fake_session_id="sess-1"),
        )
        assert len(named.rounds) == 1
        assert [row["session_id"] for row in named.session_sent_evidence] == ["sess-1"]
        assert named.session_sent_evidence[0]["sent_sha256"]

    def test_a_fallen_back_resume_leaves_post_fallback_evidence_not_a_stale_set(
        self, demo_repo: Path, tmp_path: Path,
    ):
        fallback = self._run(
            demo_repo,
            FakeProvider(
                fail_on_round=1, pass_on_round=2, supports_resume=True,
                fake_session_id="sess-1", resume_fails=True,
            ),
            repair_rounds=2,
        )
        assert fallback.final_status == "staged_review_passed"
        assert fallback.rounds[1].builder_output.resume_fallback is True

        clean = self._run(
            self._make_repo(tmp_path / "repo_clean"),
            FakeProvider(
                fail_on_round=1, pass_on_round=2, supports_resume=True,
                fake_session_id="sess-1",
            ),
            repair_rounds=2,
        )
        assert clean.rounds[1].builder_output.resume_fallback is False

        assert [row["session_id"] for row in fallback.session_sent_evidence] == ["sess-1"]
        fallback_hashes = fallback.session_sent_evidence[0]["sent_sha256"]
        clean_hashes = clean.session_sent_evidence[0]["sent_sha256"]
        # THE DISCRIMINATOR. The fallback dropped what the failed resume made
        # unprovable, so the surviving set is strictly SMALLER than the same
        # chain that never fell back. Without the invalidation the fallback run
        # would ACCUMULATE round 1's hashes and this comparison would not hold.
        assert len(fallback_hashes) < len(clean_hashes), (
            len(fallback_hashes), len(clean_hashes),
        )

    def test_the_loop_is_otherwise_unchanged_for_a_non_resuming_provider(self, demo_repo: Path):
        # Both expected values were MEASURED on a real run at this round's base
        # commit before the wiring landed, and again after it — not recalled.
        provider = FakeProvider(
            fail_on_round=1, pass_on_round=2,
            supports_resume=False, fake_session_id="sess-1",
        )
        result = self._run(demo_repo, provider, repair_rounds=2)

        assert result.final_status == "staged_review_passed"
        assert len(result.rounds) == 2

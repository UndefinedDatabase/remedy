"""F010 — the classifier, the record and the writer.

The classifier is the part everything else trusts, so it is tested as a table: every class
in the enum, the precedence between contradictory signals, and the promise that an unknown
combination is *returned*, never raised.
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

from packages.orchestration import failure_postmortem as FP
from packages.orchestration.failure_postmortem import (
    MAX_RAW_REASON_CHARS,
    POSTMORTEM_FILENAME,
    POSTMORTEM_VERSION,
    Classification,
    FailureClass,
    FailureSignals,
    PostmortemConflictError,
    PostmortemError,
    PostmortemV1,
    classify,
    read_postmortem,
    truncate_reason,
    write_postmortem,
)
from packages.orchestration.provider_timeouts import (
    is_nonzero_exit_error,
    is_timeout_error,
)
from packages.orchestration.worktrees import WorktreeConflictError, WorktreeLockError


def _record(**kw) -> PostmortemV1:
    base = dict(
        failure_class=FailureClass.PROVIDER_TIMEOUT,
        signal_source=FP.SIGNAL_ERROR_TEXT,
        job_id="J1", task_id="T001", run_id="r1", call_id="calls/builder/round-01/attempt",
        role="builder", provider="fake", raw_reason="provider_error: TimeoutExpired",
    )
    base.update(kw)
    return PostmortemV1(**base)


# ---------------------------------------------------------------------------
# The classifier: every class, and the precedence between them
# ---------------------------------------------------------------------------

class TestClassifyEveryClass:
    @pytest.mark.parametrize("signals,expected,source", [
        # typed exceptions
        (FailureSignals(exception=WorktreeConflictError("both changed x.py")),
         FailureClass.WORKTREE_CONFLICT, FP.SIGNAL_TYPED_EXCEPTION),
        (FailureSignals(exception=WorktreeLockError("held by run r9")),
         FailureClass.WORKTREE_LOCK, FP.SIGNAL_TYPED_EXCEPTION),
        (FailureSignals(exception=FileNotFoundError("claude")),
         FailureClass.PROVIDER_UNAVAILABLE, FP.SIGNAL_TYPED_EXCEPTION),
        (FailureSignals(exception=subprocess.TimeoutExpired("claude", 60)),
         FailureClass.PROVIDER_TIMEOUT, FP.SIGNAL_TYPED_EXCEPTION),
        (FailureSignals(exception=subprocess.CalledProcessError(1, "claude")),
         FailureClass.PROVIDER_NONZERO_EXIT, FP.SIGNAL_TYPED_EXCEPTION),
        # terminal statuses
        (FailureSignals(terminal_status="test_failed"),
         FailureClass.TEST_FAILED, FP.SIGNAL_TERMINAL_STATUS),
        (FailureSignals(terminal_status="review_failed"),
         FailureClass.REVIEW_FAILED, FP.SIGNAL_TERMINAL_STATUS),
        (FailureSignals(terminal_status="provider_unavailable"),
         FailureClass.PROVIDER_UNAVAILABLE, FP.SIGNAL_TERMINAL_STATUS),
        (FailureSignals(runtime_probe_failed=True, error_text="supervisor_missing"),
         FailureClass.RUNTIME_PROBE_FAILED, FP.SIGNAL_TERMINAL_STATUS),
        # reserved classes: classifiable, wired to nothing (F011 / F018)
        (FailureSignals(terminal_status="stopped"),
         FailureClass.STOPPED, FP.SIGNAL_TERMINAL_STATUS),
        (FailureSignals(terminal_status="budget_exhausted"),
         FailureClass.BUDGET_EXHAUSTED, FP.SIGNAL_TERMINAL_STATUS),
        # structured error_class
        (FailureSignals(error_class="parse", error_text="malformed_output: not json"),
         FailureClass.PARSE, FP.SIGNAL_ERROR_CLASS),
        (FailureSignals(error_class="config", error_text="missing model"),
         FailureClass.CONFIG, FP.SIGNAL_ERROR_CLASS),
        # error text, through the shared retry predicates
        (FailureSignals(error_text="provider_error: TimeoutExpired: after 600s"),
         FailureClass.PROVIDER_TIMEOUT, FP.SIGNAL_ERROR_TEXT),
        (FailureSignals(error_text="claude CLI exited 1: internal error"),
         FailureClass.PROVIDER_NONZERO_EXIT, FP.SIGNAL_ERROR_TEXT),
        (FailureSignals(error_text="claude: command not found"),
         FailureClass.PROVIDER_UNAVAILABLE, FP.SIGNAL_ERROR_TEXT),
        # retry evidence, when nothing better exists
        (FailureSignals(retry_reasons=("builder:attempt1:provider_error: TimeoutExpired",)),
         FailureClass.PROVIDER_TIMEOUT, FP.SIGNAL_RETRY_REASONS),
        # nothing known
        (FailureSignals(), FailureClass.UNKNOWN, FP.SIGNAL_NONE),
        (FailureSignals(error_text="something nobody has ever seen"),
         FailureClass.UNKNOWN, FP.SIGNAL_NONE),
    ])
    def test_the_class_and_the_signal_that_produced_it(self, signals, expected, source):
        verdict = classify(signals)
        assert verdict.failure_class is expected
        assert verdict.signal_source == source

    def test_every_enum_member_is_reachable(self):
        """No class exists that nothing can ever produce."""
        from packages.orchestration.scope_fences import (
            ChangeSetFenceResult,
            FenceViolation,
            FenceViolationError,
        )

        _fence_err = FenceViolationError(ChangeSetFenceResult(
            allowed=False,
            violations=(FenceViolation(
                path=".git/x", normalized=".git/x",
                operation="modify", role="target",
                reason="denied:builtin:git directory",
            ),),
            touched_count=1,
        ))
        produced = set()
        for signals in (
            FailureSignals(exception=WorktreeConflictError("x")),
            FailureSignals(exception=WorktreeLockError("x")),
            FailureSignals(exception=subprocess.TimeoutExpired("c", 1)),
            FailureSignals(exception=subprocess.CalledProcessError(1, "c")),
            FailureSignals(exception=FileNotFoundError("c")),
            # R-0185: a new enum member needs a producer, or the class exists
            # and nothing can ever reach it.
            FailureSignals(exception=OSError("killed while writing")),
            FailureSignals(exception=_fence_err),
            FailureSignals(terminal_status="test_failed"),
            FailureSignals(terminal_status="review_failed"),
            FailureSignals(terminal_status="stopped"),
            FailureSignals(terminal_status="budget_exhausted"),
            FailureSignals(runtime_probe_failed=True),
            FailureSignals(error_class="parse"),
            FailureSignals(error_class="config"),
            FailureSignals(),
        ):
            produced.add(classify(signals).failure_class)
        assert produced == set(FailureClass)


class TestPrecedence:
    def test_a_typed_exception_beats_a_terminal_status(self):
        verdict = classify(FailureSignals(
            exception=WorktreeLockError("held"),
            terminal_status="test_failed",
            error_class="parse",
            error_text="provider_error: TimeoutExpired",
        ))
        assert verdict.failure_class is FailureClass.WORKTREE_LOCK
        assert verdict.signal_source == FP.SIGNAL_TYPED_EXCEPTION

    def test_a_terminal_status_beats_an_error_class(self):
        verdict = classify(FailureSignals(
            terminal_status="test_failed", error_class="parse"))
        assert verdict.failure_class is FailureClass.TEST_FAILED
        assert verdict.signal_source == FP.SIGNAL_TERMINAL_STATUS

    def test_an_error_class_beats_the_retry_reasons(self):
        verdict = classify(FailureSignals(
            error_class="parse",
            retry_reasons=("reviewer:attempt1:provider_error: TimeoutExpired",),
        ))
        assert verdict.failure_class is FailureClass.PARSE
        assert verdict.signal_source == FP.SIGNAL_ERROR_CLASS

    def test_a_reviewer_rejection_is_not_a_transport_failure(self):
        """`needs_repair` is a normal verdict. It is not a provider crash."""
        verdict = classify(FailureSignals(reviewer_verdict="needs_repair"))
        assert verdict.failure_class is FailureClass.UNKNOWN

    def test_an_untyped_exception_falls_through_to_the_weaker_signals(self):
        verdict = classify(FailureSignals(
            exception=RuntimeError("boom"), terminal_status="review_failed"))
        assert verdict.failure_class is FailureClass.REVIEW_FAILED

    def test_classification_is_deterministic(self):
        signals = FailureSignals(
            error_class="config", error_text="x", retry_reasons=("a", "b"))
        assert [classify(signals) for _ in range(5)] == [
            Classification(FailureClass.CONFIG, FP.SIGNAL_ERROR_CLASS, "config")] * 5

    def test_the_classifier_never_raises_and_never_mutates(self):
        signals = FailureSignals(error_text="\x00\xff nonsense", retry_reasons=("z",))
        before = signals
        assert classify(signals).failure_class is FailureClass.UNKNOWN
        assert signals == before


class TestSharedTimeoutPredicate:
    """The classifier uses THE retry predicate — not a copy of the string match."""

    def test_the_timeout_predicate_is_the_retry_one(self):
        assert FP.is_timeout_error is is_timeout_error
        assert FP.is_nonzero_exit_error is is_nonzero_exit_error

    @pytest.mark.parametrize("error", [
        "provider_error: TimeoutExpired",
        "provider_error: RuntimeError: timeout after 600s",
        "TIMEOUT while waiting",
    ])
    def test_case_and_message_variants_the_retry_path_already_accepts(self, error):
        assert is_timeout_error(error)
        assert classify(FailureSignals(error_text=error)).failure_class is (
            FailureClass.PROVIDER_TIMEOUT)

    @pytest.mark.parametrize("error", ["exited 1: fail", "NONZERO exit status"])
    def test_nonzero_variants(self, error):
        assert is_nonzero_exit_error(error)
        assert classify(FailureSignals(error_text=error)).failure_class is (
            FailureClass.PROVIDER_NONZERO_EXIT)


# ---------------------------------------------------------------------------
# The record
# ---------------------------------------------------------------------------

class TestRecord:
    def test_the_raw_reason_is_bounded_deterministically(self):
        long = "x" * (MAX_RAW_REASON_CHARS + 500)
        once = truncate_reason(long)
        assert once == truncate_reason(long)
        assert len(once) == MAX_RAW_REASON_CHARS + len(FP.TRUNCATION_SUFFIX)
        assert once.endswith(FP.TRUNCATION_SUFFIX)
        assert _record(raw_reason=long).to_json()["raw_reason"] == once

    def test_relative_evidence_refs_survive(self):
        payload = _record(evidence_refs=("raw_stream.jsonl", "./run_events.jsonl")).to_json()
        assert payload["evidence_refs"] == ["raw_stream.jsonl", "run_events.jsonl"]

    @pytest.mark.parametrize("ref", [
        "/home/someone/.data/raw_stream.jsonl",
        "../../etc/passwd",
        "calls/../../escape.json",
        "C:\\Users\\dev\\raw.jsonl",
    ])
    def test_absolute_and_traversing_refs_are_rejected(self, ref):
        with pytest.raises(ValueError):
            _record(evidence_refs=(ref,)).to_json()

    def test_the_record_carries_its_version_and_the_retry_evidence(self):
        payload = _record(
            retry_reasons=("builder:attempt1:provider_error: TimeoutExpired",),
            retries_used=2,
        ).to_json()
        assert payload["postmortem_v"] == POSTMORTEM_VERSION
        assert payload["retries_used"] == 2
        assert payload["retry_reasons"][0].startswith("builder:attempt1:")
        assert payload["scope"] == "call"


# ---------------------------------------------------------------------------
# The writer: atomic, exactly-once, contained
# ---------------------------------------------------------------------------

class TestWriter:
    def test_an_atomic_write_leaves_one_readable_record(self, tmp_path):
        path = write_postmortem(tmp_path, _record(), root=tmp_path)
        assert path == tmp_path / POSTMORTEM_FILENAME
        data = read_postmortem(path)
        assert data["failure_class"] == "provider_timeout"
        assert not list(tmp_path.glob(".*tmp")), "a temporary file was left behind"

    def test_writing_the_identical_record_again_is_idempotent(self, tmp_path):
        write_postmortem(tmp_path, _record(), root=tmp_path)
        write_postmortem(tmp_path, _record(), root=tmp_path)   # same failure, later clock
        assert len(list(tmp_path.glob("postmortem*.json"))) == 1

    def test_a_conflicting_record_is_never_silently_overwritten(self, tmp_path):
        write_postmortem(tmp_path, _record(), root=tmp_path)
        with pytest.raises(PostmortemConflictError):
            write_postmortem(tmp_path, _record(failure_class=FailureClass.PARSE),
                             root=tmp_path)
        assert read_postmortem(tmp_path / POSTMORTEM_FILENAME)["failure_class"] == (
            "provider_timeout")

    def test_a_read_only_evidence_directory_raises_clearly(self, tmp_path):
        """Deterministic under root too.

        `os.access` lies to root: it calls a 0o500 directory writable, so the reviewed
        writer happily wrote into it on the review host and this test's `DID NOT RAISE` was
        the honest complaint. The writer now reads the DECLARED mode bits, which do not
        care who is asking.
        """
        target = tmp_path / "ro"
        target.mkdir()
        os.chmod(target, 0o500)
        try:
            with pytest.raises(PostmortemError, match="read-only"):
                write_postmortem(target, _record(), root=tmp_path)
            assert not list(target.iterdir()), "no temporary file survived the failure"
        finally:
            os.chmod(target, 0o700)

    def test_an_io_failure_during_the_write_leaves_no_partial_record(self, tmp_path, monkeypatch):
        """A short/failing write is not a written record."""
        real_write = os.write

        def broken(fd, data):
            raise OSError(28, "No space left on device")

        monkeypatch.setattr(os, "write", broken)
        with pytest.raises(PostmortemError):
            write_postmortem(tmp_path, _record(), root=tmp_path)
        monkeypatch.setattr(os, "write", real_write)

        assert not (tmp_path / POSTMORTEM_FILENAME).exists()
        assert not list(tmp_path.glob(".*tmp")), "a partial temp file survived"

    def test_a_symlinked_destination_directory_is_refused(self, tmp_path):
        """The reviewer's reproduction: a symlinked directory handed to the writer."""
        outside = tmp_path / "outside"
        outside.mkdir()
        root = tmp_path / "evidence"
        root.mkdir()
        (root / "call").symlink_to(outside, target_is_directory=True)

        with pytest.raises(PostmortemError):
            write_postmortem(root / "call", _record(), root=root)
        assert not (outside / POSTMORTEM_FILENAME).exists(), "the record escaped the tree"

    def test_a_symlinked_parent_component_is_refused(self, tmp_path):
        outside = tmp_path / "outside"
        (outside / "deep").mkdir(parents=True)
        root = tmp_path / "evidence"
        root.mkdir()
        (root / "mid").symlink_to(outside, target_is_directory=True)

        with pytest.raises(PostmortemError):
            write_postmortem(root / "mid" / "deep", _record(), root=root)
        assert not (outside / "deep" / POSTMORTEM_FILENAME).exists()

    def test_a_destination_outside_the_trusted_root_is_refused(self, tmp_path):
        root = tmp_path / "evidence"
        root.mkdir()
        with pytest.raises(PostmortemError, match="escapes"):
            write_postmortem(tmp_path / "elsewhere", _record(), root=root)

    def test_a_predictable_temp_file_cannot_be_hijacked(self, tmp_path):
        """The temp name is unpredictable AND exclusively created, so a pre-planted file
        of the old predictable name changes nothing."""
        planted = tmp_path / f".{POSTMORTEM_FILENAME}.{os.getpid()}.tmp"
        planted.symlink_to(tmp_path / "victim.json")

        write_postmortem(tmp_path, _record(), root=tmp_path)

        assert not (tmp_path / "victim.json").exists(), "the planted symlink was written"
        assert read_postmortem(tmp_path / POSTMORTEM_FILENAME)["failure_class"] == (
            "provider_timeout")

    def test_a_concurrently_published_different_record_conflicts(self, tmp_path):
        """Publication is create-only: last-writer-wins would silently lose a failure."""
        write_postmortem(tmp_path, _record(), root=tmp_path)
        with pytest.raises(PostmortemConflictError):
            write_postmortem(tmp_path, _record(failure_class=FailureClass.PARSE),
                             root=tmp_path)
        assert read_postmortem(tmp_path / POSTMORTEM_FILENAME)["failure_class"] == (
            "provider_timeout")

    def test_a_concurrently_published_identical_record_is_idempotent(self, tmp_path):
        write_postmortem(tmp_path, _record(), root=tmp_path)
        write_postmortem(tmp_path, _record(), root=tmp_path)
        assert len(list(tmp_path.glob("postmortem*.json"))) == 1
        assert not list(tmp_path.glob(".*tmp"))

    def test_a_symlinked_target_is_refused_not_followed(self, tmp_path):
        outside = tmp_path / "outside.json"
        outside.write_text("{}\n")
        target = tmp_path / "call"
        target.mkdir()
        (target / POSTMORTEM_FILENAME).symlink_to(outside)

        with pytest.raises(PostmortemError):
            write_postmortem(target, _record(), root=tmp_path)
        assert outside.read_text() == "{}\n", "the symlink was followed out of the dir"

    def test_an_unsupported_version_is_rejected_on_read(self, tmp_path):
        (tmp_path / POSTMORTEM_FILENAME).write_text(
            json.dumps({"postmortem_v": 99, "failure_class": "parse"}) + "\n")
        with pytest.raises(ValueError):
            read_postmortem(tmp_path / POSTMORTEM_FILENAME)


class TestCallDirectory:
    def test_a_provider_call_directory_is_used_when_it_exists(self, tmp_path):
        stream = tmp_path / "streams" / "builder" / "round-01" / "attempt-01"
        stream.mkdir(parents=True)
        chosen = FP.call_evidence_dir(tmp_path, "builder", 1, "attempt",
                                      provider_call_dir=str(stream))
        assert chosen == stream

    def test_otherwise_the_run_gets_a_stable_call_directory(self, tmp_path):
        chosen = FP.call_evidence_dir(tmp_path, "reviewer", 2, "parse-retry")
        assert chosen == tmp_path / "calls" / "reviewer" / "round-02" / "parse-retry"
        assert chosen == FP.call_evidence_dir(tmp_path, "reviewer", 2, "parse-retry")

    def test_only_artifacts_that_exist_are_referenced(self, tmp_path):
        (tmp_path / "raw_stream.jsonl").write_text("{}\n")
        assert FP.existing_evidence_refs(tmp_path) == ("raw_stream.jsonl",)


class TestCanonicalCollector:
    """Both real source layouts, collected once each."""

    def test_run_and_stream_layouts_are_both_collected(self, tmp_path):
        run = tmp_path / "runs" / "r1"
        (run / "calls" / "builder" / "round-01" / "attempt").mkdir(parents=True)
        write_postmortem(run / "calls" / "builder" / "round-01" / "attempt", _record(),
                         root=run)

        streams = tmp_path / "streams"
        streamed = streams / "builder" / "round-01" / "attempt-01"
        streamed.mkdir(parents=True)
        write_postmortem(streamed, _record(failure_class=FailureClass.PARSE,
                                           signal_source=FP.SIGNAL_ERROR_CLASS),
                         root=streams)

        found = FP.collect_task_call_postmortems(run_dir=run, task_stream_dir=streams)
        layouts = [layout for layout, _ in found]
        assert layouts == [
            "runs/calls/builder/round-01/attempt",
            "streams/builder/round-01/attempt-01",
        ]

    def test_a_missing_layout_is_simply_empty(self, tmp_path):
        assert FP.collect_task_call_postmortems(
            run_dir=tmp_path / "nope", task_stream_dir=None) == []


class TestJobRollup:
    def test_a_typed_worktree_lock_becomes_a_job_scope_record(self):
        from packages.orchestration.worktrees import WorktreeLockError

        record = FP.build_job_rollup(
            job_id="J1",
            signals=FailureSignals(exception=WorktreeLockError("held by run r9")),
        )
        payload = record.to_json()
        assert payload["scope"] == "job"
        assert payload["failure_class"] == "worktree_lock"
        assert payload["signal_source"] == "typed_exception"
        assert payload["task_id"] == "", "a job failure is not a pending task's fault"


# ---------------------------------------------------------------------------
# Finding 1 — validate BEFORE mutating, and see the symlink the caller asked for
# ---------------------------------------------------------------------------

class TestWriterValidatesBeforeItCreates:
    def _rec(self):
        return _record()

    def test_a_destination_symlink_INSIDE_the_root_is_refused(self, tmp_path):
        """`resolve()` answers "where does it point", not "did you ask me through a link".

        The reviewed writer resolved first, so `root/link -> root/real` looked like an
        ordinary directory and the record silently landed somewhere the caller never named.
        """
        root = tmp_path / "evidence"
        (root / "real").mkdir(parents=True)
        (root / "link").symlink_to(root / "real", target_is_directory=True)

        with pytest.raises(PostmortemError, match="symlink"):
            write_postmortem(root / "link", self._rec(), root=root)
        assert not (root / "real" / POSTMORTEM_FILENAME).exists()

    def test_a_parent_symlink_INSIDE_the_root_is_refused(self, tmp_path):
        root = tmp_path / "evidence"
        (root / "real" / "deep").mkdir(parents=True)
        (root / "mid").symlink_to(root / "real", target_is_directory=True)

        with pytest.raises(PostmortemError, match="symlink"):
            write_postmortem(root / "mid" / "deep", self._rec(), root=root)
        assert not (root / "real" / "deep" / POSTMORTEM_FILENAME).exists()

    def test_a_rejected_request_creates_nothing_outside_the_root(self, tmp_path):
        """The reviewed writer mkdir'd first: `outside/newdir` existed before it said no."""
        outside = tmp_path / "outside"
        outside.mkdir()
        root = tmp_path / "evidence"
        root.mkdir()
        (root / "link").symlink_to(outside, target_is_directory=True)

        with pytest.raises(PostmortemError):
            write_postmortem(root / "link" / "newdir", self._rec(), root=root)

        assert list(outside.iterdir()) == [], "a directory was created outside the root"
        assert not (outside / "newdir").exists()

    def test_a_symlinked_trusted_root_is_refused(self, tmp_path):
        real = tmp_path / "real_root"
        real.mkdir()
        link_root = tmp_path / "root_link"
        link_root.symlink_to(real, target_is_directory=True)

        with pytest.raises(PostmortemError, match="symlink"):
            write_postmortem(link_root / "call", self._rec(), root=link_root)
        assert not (real / "call").exists()

    def test_a_missing_trusted_root_is_refused_rather_than_created(self, tmp_path):
        with pytest.raises(PostmortemError, match="does not exist"):
            write_postmortem(tmp_path / "gone" / "call", self._rec(),
                             root=tmp_path / "gone")
        assert not (tmp_path / "gone").exists()

    def test_a_symlink_substituted_right_after_mkdir_is_caught(self, tmp_path, monkeypatch):
        """The narrow window the second round closed: swap the directory we just created."""
        root = tmp_path / "evidence"
        root.mkdir()
        outside = tmp_path / "outside"
        outside.mkdir()

        real_mkdir = os.mkdir

        def racing_mkdir(name, mode=0o777, *, dir_fd=None):
            real_mkdir(name, mode, dir_fd=dir_fd)
            if name == "call":                     # swap it for a symlink, right now
                os.rmdir(name, dir_fd=dir_fd)
                os.symlink(str(outside), name, dir_fd=dir_fd)

        monkeypatch.setattr(os, "mkdir", racing_mkdir)
        with pytest.raises(PostmortemError, match="symlink"):
            write_postmortem(root / "call", self._rec(), root=root)
        monkeypatch.undo()

        assert list(outside.iterdir()) == []

    def test_a_symlink_swapped_in_after_validation_cannot_redirect_the_write(
        self, tmp_path, monkeypatch,
    ):
        """The window the reviewer demonstrated: the destination is VALID when it is
        checked, and becomes a symlink to `outside` immediately before the temp file is
        created. Names are never re-resolved — the write goes through the fd we already
        hold — so the swap changes nothing.
        """
        root = tmp_path / "evidence"
        (root / "call").mkdir(parents=True)
        outside = tmp_path / "outside"
        outside.mkdir()

        real_open = os.open
        swapped = {"done": False}

        def swapping_open(path, flags, mode=0o777, *, dir_fd=None):
            if (not swapped["done"] and isinstance(path, str)
                    and path.startswith(f".{POSTMORTEM_FILENAME}")):
                swapped["done"] = True             # right before the temp file is created
                (root / "call").rmdir()
                (root / "call").symlink_to(outside, target_is_directory=True)
            return real_open(path, flags, mode, dir_fd=dir_fd)

        monkeypatch.setattr(os, "open", swapping_open)
        with pytest.raises(PostmortemError):
            write_postmortem(root / "call", self._rec(), root=root)
        monkeypatch.undo()

        assert swapped["done"], "the seam never fired"
        # The fd we hold still points at the directory the caller NAMED — which has just
        # been unlinked — so the write fails loudly. It does not follow the attacker's
        # symlink, which is the whole point.
        assert list(outside.iterdir()) == [], "the record was redirected outside the root"

    def test_a_symlink_swapped_in_before_publication_cannot_redirect_it(
        self, tmp_path, monkeypatch,
    ):
        root = tmp_path / "evidence"
        (root / "call").mkdir(parents=True)
        outside = tmp_path / "outside"
        outside.mkdir()

        real_link = os.link
        swapped = {"done": False}

        def swapping_link(src, dst, *, src_dir_fd=None, dst_dir_fd=None,
                          follow_symlinks=True):
            swapped["done"] = True                 # right before the record is published
            (root / "call").rmdir()
            (root / "call").symlink_to(outside, target_is_directory=True)
            return real_link(src, dst, src_dir_fd=src_dir_fd, dst_dir_fd=dst_dir_fd)

        monkeypatch.setattr(os, "link", swapping_link)
        with pytest.raises(PostmortemError):
            write_postmortem(root / "call", self._rec(), root=root)
        monkeypatch.undo()

        assert swapped["done"]
        assert list(outside.iterdir()) == [], "publication followed the swapped symlink"

    def test_no_file_descriptor_leaks_on_success_or_failure(self, tmp_path):

        def open_fds() -> int:
            return len(os.listdir("/proc/self/fd"))

        before = open_fds()
        write_postmortem(tmp_path / "ok", self._rec(), root=tmp_path)
        assert open_fds() == before, "a descriptor leaked on the success path"

        (tmp_path / "outside").mkdir()
        (tmp_path / "bad").symlink_to(tmp_path / "outside", target_is_directory=True)
        with pytest.raises(PostmortemError):
            write_postmortem(tmp_path / "bad", self._rec(), root=tmp_path)
        assert open_fds() == before, "a descriptor leaked on the failure path"

    def test_an_existing_record_reached_through_a_symlink_is_refused(self, tmp_path):
        root = tmp_path / "evidence"
        (root / "call").mkdir(parents=True)
        outside = tmp_path / "outside.json"
        outside.write_text('{"postmortem_v": 1}\n')
        os.symlink(str(outside), str(root / "call" / POSTMORTEM_FILENAME))

        with pytest.raises(PostmortemError):
            write_postmortem(root / "call", self._rec(), root=root)
        assert outside.read_text() == '{"postmortem_v": 1}\n'

    def test_the_platform_must_support_containment(self, tmp_path, monkeypatch):
        """No primitives, no guarantee — and no silent fallback to the racy algorithm."""
        monkeypatch.setattr(FP, "_DIR_FD_SUPPORTED", False)
        with pytest.raises(PostmortemError, match="cannot guarantee"):
            write_postmortem(tmp_path, self._rec(), root=tmp_path)

    def test_a_zero_byte_write_fails_instead_of_looping(self, tmp_path, monkeypatch):
        monkeypatch.setattr(os, "write", lambda fd, data: 0)
        with pytest.raises(PostmortemError, match="no progress"):
            write_postmortem(tmp_path, self._rec(), root=tmp_path)
        monkeypatch.undo()

        assert not (tmp_path / POSTMORTEM_FILENAME).exists()
        assert not list(tmp_path.glob(".*tmp")), "a temp file survived the failure"

    def test_partial_positive_writes_still_produce_a_whole_record(self, tmp_path, monkeypatch):
        real_write = os.write
        monkeypatch.setattr(os, "write", lambda fd, data: real_write(fd, data[:7]))

        write_postmortem(tmp_path, self._rec(), root=tmp_path)
        monkeypatch.undo()

        assert read_postmortem(tmp_path / POSTMORTEM_FILENAME)["failure_class"] == (
            "provider_timeout")
        assert not list(tmp_path.glob(".*tmp"))


# ---------------------------------------------------------------------------
# Finding 5 — nothing secret, and no local path, ever reaches a record
# ---------------------------------------------------------------------------

class TestRedaction:
    @pytest.mark.parametrize("secret,needle", [
        ("API_KEY=supersecret", "supersecret"),
        ("ANTHROPIC_API_KEY=sk-ant-0123456789", "sk-ant-0123456789"),
        ("Authorization: Bearer abcdef0123456789abcdef", "abcdef0123456789abcdef"),
        ("PASSWORD=hunter2", "hunter2"),
        ('{"api_key": "leakme"}', "leakme"),
    ])
    def test_a_secret_never_reaches_the_record(self, tmp_path, secret, needle):
        record = _record(raw_reason=f"provider failed: {secret}",
                         retry_reasons=(f"builder:attempt1:{secret}",))
        write_postmortem(tmp_path, record, root=tmp_path)
        payload = (tmp_path / POSTMORTEM_FILENAME).read_text()

        assert needle not in payload, payload
        assert "REDACTED" in payload

    @pytest.mark.parametrize("path", [
        "/home/user/.data/pingpong_runs/r1/postmortem.json",
        "/tmp/pytest-of-root/x/postmortem.json",
        r"C:\\Users\\dev\\.data\\postmortem.json",
    ])
    def test_an_absolute_path_never_reaches_the_record(self, tmp_path, path):
        record = _record(raw_reason=f"PostmortemError: read-only: {path}")
        write_postmortem(tmp_path, record, root=tmp_path)
        payload = json.loads((tmp_path / POSTMORTEM_FILENAME).read_text())

        assert "/home/user" not in payload["raw_reason"]
        assert "/tmp/pytest" not in payload["raw_reason"]
        assert "C:" not in payload["raw_reason"]
        # ...and the words that CLASSIFY the failure survive.
        assert "read-only" in payload["raw_reason"]
        assert "postmortem.json" in payload["raw_reason"]

    def test_the_runtime_data_root_keeps_its_meaning(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        (tmp_path / "data" / "pingpong_runs" / "r1").mkdir(parents=True)
        text = FP.safe_text(f"could not write {tmp_path}/data/pingpong_runs/r1/postmortem.json")
        assert text.endswith("[runtime-data]/pingpong_runs/r1/postmortem.json"), text

    def test_classification_still_works_on_a_redacted_reason(self):
        reason = FP.safe_text("claude CLI timed out after 600s (API_KEY=abc123)")
        assert "abc123" not in reason
        assert classify(FailureSignals(error_text=reason)).failure_class is (
            FailureClass.PROVIDER_TIMEOUT)


class TestFileUriAndLabelledPathRedaction:
    """F007's accepted scrubber, shared — plus the label-prefixed form F010 needed."""

    @pytest.mark.parametrize("text,gone", [
        ("file:///home/bernardo/private/project/secret.py", "/home/bernardo"),
        ("file://localhost/home/bernardo/private/secret.py", "/home/bernardo"),
        ("file:///C:/Users/Bernardo/private/secret.py", "C:/Users"),
        ("file://server/share/private.txt", "server/share"),
        ("file:///home/alice/private%20folder/secret.txt", "/home/alice"),
        ("cwd:/tmp/secret-repo", "/tmp/secret-repo"),
        ("path:/home/user/private.txt", "/home/user"),
        ('working directory "/home/user/private dir" is gone', "/home/user"),
        ("see /home/user/x.txt", "/home/user"),
        (r"C:\Users\dev\private.txt", r"C:\Users"),
    ])
    def test_a_private_path_never_survives(self, text, gone):
        assert gone not in FP.safe_text(text)

    @pytest.mark.parametrize("text", [
        "profile:///home/alice/test.txt",
        "myfile://server/share/x.txt",
        "notafile:///home/alice/test.txt",
        "some.file:///home/alice/test.txt",
        "x-file:///home/alice/test.txt",
    ])
    def test_a_string_that_is_not_a_file_uri_is_left_alone(self, text):
        assert FP.safe_text(text) == text

    def test_the_shared_module_is_the_one_f007_uses(self):
        from packages.common import path_redaction
        from packages.runtimes import dev_server

        # Every redaction name dev_server holds IS the shared object — the
        # anti-drift point of this test. (`_FILE_URI_RE` is no longer among
        # them: dev_server hands file URIs to scrub_paths and never touches
        # the regex itself.)
        assert dev_server._scrub_paths is path_redaction.scrub_paths
        assert dev_server._basename is path_redaction.basename
        assert dev_server._ABS_PREFIX_RE is path_redaction.ABS_PREFIX_RE
        assert "file:///home/alice/x.py" not in dev_server._redact(
            "see file:///home/alice/x.py")

    def test_a_record_carries_no_private_path(self, tmp_path):
        record = _record(raw_reason=(
            "failed at file:///home/bernardo/private/project/secret.py "
            "and cwd:/tmp/secret-repo"))
        write_postmortem(tmp_path, record, root=tmp_path)
        payload = (tmp_path / POSTMORTEM_FILENAME).read_text()

        for private in ("/home/bernardo", "file:///", "/tmp/secret-repo"):
            assert private not in payload
        assert "secret.py" in payload


# ---------------------------------------------------------------------------
# The reviewer's platform: O_NOFOLLOW accepted, and ignored
# ---------------------------------------------------------------------------

@pytest.fixture
def nofollow_is_a_lie(monkeypatch):
    """Simulate the external Linux 4.4 host: the flag is accepted and does nothing.

    The constant exists, `supports_dir_fd` advertises everything, and a directory symlink
    opened with `O_RDONLY|O_DIRECTORY|O_NOFOLLOW` is followed anyway. The writer must refuse
    every symlink ANYWAY — from its own stat/fstat identity comparison, not from an ELOOP
    the kernel was never going to raise.
    """
    real_open = os.open
    nofollow = getattr(os, "O_NOFOLLOW", 0)

    def open_without_nofollow(path, flags, mode=0o777, *, dir_fd=None):
        return real_open(path, flags & ~nofollow, mode, dir_fd=dir_fd)

    monkeypatch.setattr(os, "open", open_without_nofollow)
    return open_without_nofollow


class TestAPlatformWhereNoFollowIsIgnored:
    def _rec(self):
        return _record()

    def test_the_simulation_really_defeats_o_nofollow(self, tmp_path, nofollow_is_a_lie):
        """Prove the seam: without the writer's own checks, the symlink WOULD be followed."""
        outside = tmp_path / "outside"
        outside.mkdir()
        (tmp_path / "link").symlink_to(outside, target_is_directory=True)

        root_fd = os.open(str(tmp_path), os.O_RDONLY | os.O_DIRECTORY)
        try:
            fd = os.open("link", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                         dir_fd=root_fd)
            try:
                assert os.fstat(fd).st_ino == outside.stat().st_ino, (
                    "the seam did not reproduce the external platform")
            finally:
                os.close(fd)
        finally:
            os.close(root_fd)

    def test_a_destination_symlink_to_outside_is_still_refused(
        self, tmp_path, nofollow_is_a_lie,
    ):
        root = tmp_path / "evidence"
        root.mkdir()
        outside = tmp_path / "outside"
        outside.mkdir()
        (root / "call").symlink_to(outside, target_is_directory=True)

        with pytest.raises(PostmortemError, match="symlink"):
            write_postmortem(root / "call", self._rec(), root=root)
        assert list(outside.iterdir()) == [], "the record escaped the evidence tree"

    def test_a_destination_symlink_INSIDE_the_root_is_still_refused(
        self, tmp_path, nofollow_is_a_lie,
    ):
        root = tmp_path / "evidence"
        (root / "real").mkdir(parents=True)
        (root / "link").symlink_to(root / "real", target_is_directory=True)

        with pytest.raises(PostmortemError, match="symlink"):
            write_postmortem(root / "link", self._rec(), root=root)
        assert not (root / "real" / POSTMORTEM_FILENAME).exists()

    def test_a_symlinked_parent_component_is_still_refused(
        self, tmp_path, nofollow_is_a_lie,
    ):
        root = tmp_path / "evidence"
        root.mkdir()
        outside = tmp_path / "outside"
        (outside / "deep").mkdir(parents=True)
        (root / "mid").symlink_to(outside, target_is_directory=True)

        with pytest.raises(PostmortemError, match="symlink"):
            write_postmortem(root / "mid" / "deep", self._rec(), root=root)
        assert list((outside / "deep").iterdir()) == []

    def test_a_symlinked_trusted_root_is_still_refused(self, tmp_path, nofollow_is_a_lie):
        real = tmp_path / "real_root"
        real.mkdir()
        link_root = tmp_path / "root_link"
        link_root.symlink_to(real, target_is_directory=True)

        with pytest.raises(PostmortemError, match="symlink"):
            write_postmortem(link_root / "call", self._rec(), root=link_root)
        assert list(real.iterdir()) == []

    def test_a_symlinked_existing_record_is_still_refused(self, tmp_path, nofollow_is_a_lie):
        root = tmp_path / "evidence"
        (root / "call").mkdir(parents=True)
        outside = tmp_path / "outside.json"
        outside.write_text('{"postmortem_v": 1, "failure_class": "parse"}\n')
        os.symlink(str(outside), str(root / "call" / POSTMORTEM_FILENAME))

        with pytest.raises(PostmortemError, match="symlink"):
            write_postmortem(root / "call", self._rec(), root=root)
        assert outside.read_text().startswith('{"postmortem_v": 1')

    def test_a_missing_component_is_still_created_normally(
        self, tmp_path, nofollow_is_a_lie,
    ):
        root = tmp_path / "evidence"
        root.mkdir()
        write_postmortem(root / "calls" / "builder" / "round-01", self._rec(), root=root)
        assert (root / "calls" / "builder" / "round-01" / POSTMORTEM_FILENAME).is_file()


class TestIdentityMismatchIsRefused:
    def test_a_component_swapped_between_the_stat_and_the_open_is_caught(
        self, tmp_path, monkeypatch,
    ):
        """Not a symlink at check time; a different inode at open time. Refused."""
        root = tmp_path / "evidence"
        (root / "call").mkdir(parents=True)
        other = tmp_path / "other"
        other.mkdir()

        real_open = os.open
        swapped = {"done": False}

        def swapping_open(path, flags, mode=0o777, *, dir_fd=None):
            if path == "call" and not swapped["done"]:
                swapped["done"] = True
                (root / "call").rmdir()
                (root / "call").symlink_to(other, target_is_directory=True)
                return real_open(str(other), flags & ~getattr(os, "O_NOFOLLOW", 0), mode)
            return real_open(path, flags, mode, dir_fd=dir_fd)

        monkeypatch.setattr(os, "open", swapping_open)
        with pytest.raises(PostmortemError, match="not the directory it claimed"):
            write_postmortem(root / "call", _record(), root=root)
        monkeypatch.undo()

        assert swapped["done"], "the seam never fired"
        assert list(other.iterdir()) == []


class TestATrustedRootIsMandatory:
    def test_root_none_fails_before_any_mutation(self, tmp_path):
        """The old optional mode mkdir'd through an untrusted symlink first."""
        outside = tmp_path / "outside"
        outside.mkdir()
        parent = tmp_path / "parent"
        parent.mkdir()
        (parent / "link").symlink_to(outside, target_is_directory=True)

        with pytest.raises(PostmortemError, match="explicit trusted evidence root"):
            write_postmortem(parent / "link" / "newdir", _record(), root=None)

        assert list(outside.iterdir()) == [], "a directory was created outside the root"

    def test_every_production_call_site_passes_a_root(self):
        import inspect

        from packages.orchestration import job_evidence, pingpong_job, pingpong_loop

        for module in (job_evidence, pingpong_job, pingpong_loop):
            src = inspect.getsource(module)
            for line in src.splitlines():
                if "write_postmortem(" in line and "def " not in line and "import" not in line:
                    following = src[src.index(line):src.index(line) + 300]
                    assert "root=" in following, f"{module.__name__}: {line.strip()}"


class TestTheParentOfTheEvidenceRootIsVerifiedToo:
    """F010 shares the anchored primitives with F011, so F011's parent-of-root hole was
    F010's too: with `real/link -> outside`, `write_postmortem(root=real/link/root)` wrote
    the record into `outside`."""

    def _rec(self):
        return PostmortemV1(failure_class=FailureClass.PROVIDER_TIMEOUT,
                            signal_source="error_text", job_id="j1")

    def test_a_symlinked_parent_of_the_root_is_refused(self, tmp_path):
        outside = tmp_path / "outside"
        (outside / "root").mkdir(parents=True)
        (tmp_path / "real").mkdir()
        (tmp_path / "real" / "link").symlink_to(outside)
        root = tmp_path / "real" / "link" / "root"

        with pytest.raises(PostmortemError, match="symlink"):
            write_postmortem(root / "dir", self._rec(), root=root)

        assert list((outside / "root").iterdir()) == []

    def test_a_safe_absolute_root_still_writes(self, tmp_path):
        root = tmp_path / "evidence"
        root.mkdir()
        path = write_postmortem(root / "call", self._rec(), root=root)
        assert Path(path).is_file()

    def test_a_relative_root_still_writes(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        Path("evidence").mkdir()
        path = write_postmortem(Path("evidence/call"), self._rec(), root=Path("evidence"))
        assert Path(path).is_file()


# ---------------------------------------------------------------------------
# F075 R-0185 — transport and machine failures the classifier used to call unknown
# ---------------------------------------------------------------------------
#
# Campaign attempt 1 injected two realistic shapes at the orchestrator loop's
# seams and F010 read both as `unknown`, which cost three runs the
# no-unknown-postmortems criterion while Remedy in fact knew exactly what had
# happened. The classes below are the EXISTING taxonomy plus one honest new
# member for the machine-under-us case; nothing here is a second spelling of a
# provider class.


class TestTransportAndMachineFailures:

    def _classify(self, exc):
        return classify(FailureSignals(exception=exc,
                                       error_text=f"{type(exc).__name__}: {exc}"))

    def test_a_connection_error_is_the_provider_not_answering(self):
        verdict = self._classify(ConnectionError("connection refused"))
        assert verdict.failure_class is FailureClass.PROVIDER_UNAVAILABLE
        assert verdict.signal_source == FP.SIGNAL_TYPED_EXCEPTION

    @pytest.mark.parametrize("exc", [
        ConnectionRefusedError("connection refused"),
        ConnectionResetError("connection reset by peer"),
        BrokenPipeError("broken pipe"),
    ])
    def test_every_connection_error_subclass_lands_on_the_same_class(self, exc):
        assert self._classify(exc).failure_class is FailureClass.PROVIDER_UNAVAILABLE

    def test_a_bare_os_error_is_the_machine_not_the_provider(self):
        verdict = self._classify(OSError("killed while writing"))
        assert verdict.failure_class is FailureClass.IO_FAILURE
        assert verdict.signal_source == FP.SIGNAL_TYPED_EXCEPTION

    def test_the_os_error_family_keeps_its_more_specific_members(self):
        """TimeoutError, ConnectionError and FileNotFoundError are all OSError
        subclasses in 3.10; a bare-OSError rule ordered above them would eat
        every one of them."""
        assert self._classify(TimeoutError("x")).failure_class is \
            FailureClass.PROVIDER_TIMEOUT
        assert self._classify(FileNotFoundError("x")).failure_class is \
            FailureClass.PROVIDER_UNAVAILABLE
        assert self._classify(ConnectionError("x")).failure_class is \
            FailureClass.PROVIDER_UNAVAILABLE

    def test_a_connection_failure_read_from_text_alone_is_classified(self):
        verdict = classify(FailureSignals(error_text="the model host returned HTTP 503"))
        assert verdict.failure_class is FailureClass.PROVIDER_UNAVAILABLE
        assert verdict.signal_source == FP.SIGNAL_ERROR_TEXT

    def test_a_machine_failure_read_from_text_alone_is_classified(self):
        verdict = classify(FailureSignals(error_text="no space left on device"))
        assert verdict.failure_class is FailureClass.IO_FAILURE

    def test_a_provider_reading_wins_over_a_machine_reading(self):
        """A provider error that also mentions a pipe is still a provider error."""
        verdict = classify(FailureSignals(
            error_text="connection reset by peer; broken pipe"))
        assert verdict.failure_class is FailureClass.PROVIDER_UNAVAILABLE

    @pytest.mark.parametrize("exc", [
        ValueError("something nobody can classify"),
        RuntimeError("the vibes were off"),
        KeyError("k"),
    ])
    def test_a_genuinely_unrecognizable_failure_stays_unknown(self, exc):
        """The falsification: the new classes must not make `unknown` unreachable."""
        assert self._classify(exc).failure_class is FailureClass.UNKNOWN

    def test_an_unrecognizable_message_stays_unknown(self):
        assert classify(FailureSignals(
            error_text="the flurb did not glorp")).failure_class is FailureClass.UNKNOWN

    def test_the_io_predicate_is_narrow_enough_to_be_worth_having(self):
        assert FP.is_io_failure_error("killed while writing the dossier") is True
        assert FP.is_io_failure_error("everything was completely fine") is False
        assert FP.is_io_failure_error("") is False

    def test_the_connection_predicate_is_narrow_enough_to_be_worth_having(self):
        assert FP.is_provider_connection_error("HTTP 503 from the host") is True
        assert FP.is_provider_connection_error("a perfectly good answer") is False
        assert FP.is_provider_connection_error(None) is False


class TestABareSlashIsNotAPath:
    """R-0206: a space-delimited slash is prose, not a filesystem path.

    ABS_PATH_RE used to accept a zero-length tail, so the delimiter in
    "plan status / plan next" scrubbed to "[path]/path" and every commit
    subject containing " / " was rejected by the evidence-packaging
    metadata scan — a false positive that blocked a closure. The tail is
    now mandatory. What must NOT change is the detection of real paths,
    which is what the second half of this class pins.
    """

    @pytest.mark.parametrize("text", [
        "a / b",
        "feat(f080): remedy plan status / plan next (T001)",
        "read / write mode",
        "/",
    ])
    def test_prose_with_a_lone_slash_survives_untouched(self, text):
        assert FP.safe_text(text) == text

    def test_the_packaging_metadata_scan_accepts_such_a_subject(self):
        from packages.orchestration.run_manifest import _contains_local_path

        assert _contains_local_path(
            "feat(f080): remedy plan status / plan next (T001)") is False

    @pytest.mark.parametrize("text,gone", [
        ("could not read /etc/passwd", "/etc"),
        ("wrote /home/user/private/notes.md", "/home/user"),
        ("cwd:/tmp/secret-repo failed", "/tmp/secret-repo"),
        ("see file:///home/alice/private/secret.txt", "/home/alice"),
    ])
    def test_a_real_path_is_still_redacted(self, text, gone):
        assert gone not in FP.safe_text(text)

    def test_the_packaging_metadata_scan_still_rejects_a_real_path(self):
        from packages.orchestration.run_manifest import _contains_local_path

        assert _contains_local_path("fix: read /home/user/secret.txt") is True

    @pytest.mark.parametrize("text", [
        "F112 R18 C5-fix: correct Range placeholder and changed-files +/- counts in handback",
        "changed-files +/- counts",
        "a+/-b",
    ])
    def test_a_punctuation_only_tail_is_not_a_path(self, text):
        # R-0790: a ONE-CHARACTER punctuation tail like the "-" in "+/-"
        # satisfied R-0206's own "tail is now mandatory" fix without being
        # any part of a real filesystem path, and blocked a real closure's
        # review zip on this exact ordinary commit subject.
        assert FP.safe_text(text) == text

    def test_the_packaging_metadata_scan_accepts_a_punctuation_only_tail(self):
        from packages.orchestration.run_manifest import _contains_local_path

        assert _contains_local_path(
            "F112 R18 C5-fix: correct Range placeholder and changed-files "
            "+/- counts in handback") is False

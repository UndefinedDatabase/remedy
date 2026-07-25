"""F011 T001 — the stop-control protocol.

A stop request is a small private file. These tests hold it to the promises the runner
depends on: it is durable, atomic, idempotent, cheap to check, impossible to point out of
the control area, and unreadable-but-present is still a stop rather than a crash.
"""
from __future__ import annotations

import json
import os
import stat as _stat
from pathlib import Path

import pytest

from packages.orchestration.safe_points import (
    CONTROL_DIR_MODE,
    CONTROL_FILE_MODE,
    STOP_SIGNAL_VERSION,
    UNKNOWN_REASON,
    StopArchiveConflictError,
    StopControlError,
    StopSignal,
    clear_stop,
    consume_stop,
    request_stop,
    stop_archive_dir,
    stop_request_path,
    stop_requested,
    stop_status,
    validate_job_id,
)

JOB = "a1b2c3d4e5f60718"


@pytest.fixture
def control(tmp_path) -> Path:
    """A control root of our own. Nothing here touches the developer's real data dir."""
    return tmp_path / "control"


class TestTheRequestRoundTrips:
    def test_a_request_is_durable_readable_and_carries_the_operator_reason(self, control):
        signal = request_stop(JOB, "operator requested stop", "cli",
                              control_root_path=control)
        assert signal.stop_signal_v == STOP_SIGNAL_VERSION
        assert signal.job_id == JOB and signal.request_id
        assert signal.reason == "operator requested stop" and signal.source == "cli"
        assert signal.requested_at

        read_back = stop_requested(JOB, control_root_path=control)
        assert read_back == signal

    def test_no_request_means_no_signal(self, control):
        assert stop_requested(JOB, control_root_path=control) is None

    def test_the_file_and_its_directory_are_private(self, control):
        request_stop(JOB, "x", "cli", control_root_path=control)
        path = stop_request_path(JOB, control)
        assert _stat.S_IMODE(path.stat().st_mode) == CONTROL_FILE_MODE
        assert _stat.S_IMODE(path.parent.stat().st_mode) == CONTROL_DIR_MODE

    def test_the_written_json_has_no_absolute_path_and_no_secret(self, control):
        request_stop(JOB, f"stopping run in {control}/secret token=sk-live-abcdef123456",
                     "cli", control_root_path=control)
        raw = stop_request_path(JOB, control).read_text()
        assert str(control) not in raw
        assert "sk-live-abcdef123456" not in raw
        assert "/" not in json.loads(raw)["reason"] or "[path]" in json.loads(raw)["reason"]


class TestDoubleRequestsAreOneEpisode:
    def test_a_second_request_returns_the_first_signal(self, control):
        first = request_stop(JOB, "first", "cli", control_root_path=control)
        second = request_stop(JOB, "second", "ui", control_root_path=control)
        assert second.request_id == first.request_id
        assert second.reason == "first"          # the pending request stands, unchanged

    def test_two_requests_leave_exactly_one_pending_file(self, control):
        request_stop(JOB, "a", "cli", control_root_path=control)
        request_stop(JOB, "b", "cli", control_root_path=control)
        job_dir = stop_request_path(JOB, control).parent
        assert sorted(p.name for p in job_dir.iterdir()) == ["stop.json"]

    def test_a_stop_after_a_consume_is_a_NEW_episode(self, control):
        first = request_stop(JOB, "first", "cli", control_root_path=control)
        consume_stop(JOB, control_root_path=control)
        second = request_stop(JOB, "second", "cli", control_root_path=control)
        assert second.request_id != first.request_id


class TestAnUnreadableRequestIsStillAStop:
    def test_malformed_json_becomes_reason_unknown_and_never_raises(self, control):
        request_stop(JOB, "real", "cli", control_root_path=control)
        stop_request_path(JOB, control).write_text("{not json at all")

        signal = stop_requested(JOB, control_root_path=control)
        assert signal is not None
        assert signal.reason == UNKNOWN_REASON and signal.degraded
        assert signal.request_id.startswith("malformed-")

    def test_a_version_we_do_not_understand_is_not_guessed_at(self, control):
        stop_request_path(JOB, control).parent.mkdir(parents=True, exist_ok=True)
        stop_request_path(JOB, control).write_text(json.dumps({
            "stop_signal_v": 99, "job_id": JOB, "request_id": "abc123",
            "reason": "from the future", "source": "cli",
        }))
        signal = stop_requested(JOB, control_root_path=control)
        assert signal is not None and signal.degraded
        assert signal.reason == UNKNOWN_REASON

    def test_a_malformed_request_is_honoured_not_silently_replaced(self, control):
        """It is still an operator asking us to stop. Overwriting it would discard the very
        request we are supposed to honour — so the degraded episode stands."""
        stop_request_path(JOB, control).parent.mkdir(parents=True, exist_ok=True)
        stop_request_path(JOB, control).write_text("garbage")

        signal = request_stop(JOB, "operator", "cli", control_root_path=control)
        assert signal.degraded and signal.reason == UNKNOWN_REASON
        assert signal.request_id.startswith("malformed-")
        assert stop_requested(JOB, control_root_path=control) == signal


class TestThePathCannotEscapeTheControlArea:
    @pytest.mark.parametrize("job_id", [
        "../../etc", "..", ".", "a/b", "a\\b", "", "  ", "x" * 65, "/abs", "a;rm -rf /",
    ])
    def test_a_traversal_like_job_id_is_refused_before_it_is_a_path(self, job_id, control):
        with pytest.raises(StopControlError):
            request_stop(job_id, "x", "cli", control_root_path=control)
        with pytest.raises(StopControlError):
            stop_requested(job_id, control_root_path=control)

    def test_validate_job_id_accepts_what_remedy_actually_produces(self):
        assert validate_job_id("a1b2c3d4e5f60718")
        assert validate_job_id("866e6aef9b6c4990")
        assert validate_job_id("job-1_2")

    def test_a_symlinked_control_directory_is_refused_not_followed(self, control, tmp_path):
        outside = tmp_path / "outside"
        outside.mkdir()
        (control / "jobs").mkdir(parents=True)
        (control / "jobs" / JOB).symlink_to(outside)

        with pytest.raises(StopControlError, match="symlink"):
            request_stop(JOB, "x", "cli", control_root_path=control)
        assert list(outside.iterdir()) == []          # nothing was written through it

    def test_a_symlinked_request_file_is_refused_not_read(self, control, tmp_path):
        secret = tmp_path / "secret.json"
        secret.write_text(json.dumps({"stop_signal_v": 1, "request_id": "deadbeef",
                                      "reason": "planted", "source": "attacker"}))
        path = stop_request_path(JOB, control)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.symlink_to(secret)

        with pytest.raises(StopControlError, match="symlink"):
            stop_requested(JOB, control_root_path=control)


class TestAnUnwritableControlAreaIsLoud:
    def test_a_read_only_control_root_raises_instead_of_silently_doing_nothing(
            self, control):
        control.mkdir(parents=True)
        os.chmod(control, 0o500)
        try:
            with pytest.raises(StopControlError):
                request_stop(JOB, "x", "cli", control_root_path=control)
        finally:
            os.chmod(control, 0o700)

    def test_a_read_only_job_control_dir_raises(self, control):
        request_stop(JOB, "x", "cli", control_root_path=control)
        clear_stop(JOB, control_root_path=control)
        job_dir = stop_request_path(JOB, control).parent
        os.chmod(job_dir, 0o500)
        try:
            with pytest.raises(StopControlError):
                request_stop(JOB, "y", "cli", control_root_path=control)
        finally:
            os.chmod(job_dir, 0o700)


class TestConsumingArchivesHistory:
    def test_consume_returns_the_exact_signal_and_archives_it(self, control):
        signal = request_stop(JOB, "operator requested stop", "cli",
                              control_root_path=control)
        consumed = consume_stop(JOB, control_root_path=control)

        assert consumed == signal
        assert stop_requested(JOB, control_root_path=control) is None   # no longer pending

        archived = stop_archive_dir(JOB, control) / f"{signal.request_id}.json"
        assert archived.is_file()
        assert json.loads(archived.read_text()) == signal.to_json()
        assert _stat.S_IMODE(archived.stat().st_mode) == CONTROL_FILE_MODE

    def test_consuming_nothing_is_not_an_error(self, control):
        assert consume_stop(JOB, control_root_path=control) is None

    def test_a_re_consumed_identical_archive_completes_instead_of_conflicting(self, control):
        signal = request_stop(JOB, "x", "cli", control_root_path=control)
        # Simulate a consume that archived and then died before unlinking the request.
        archived = stop_archive_dir(JOB, control) / f"{signal.request_id}.json"
        archived.parent.mkdir(parents=True, exist_ok=True)
        archived.write_text(json.dumps(signal.to_json(), indent=2, sort_keys=True) + "\n")

        assert consume_stop(JOB, control_root_path=control) == signal
        assert stop_requested(JOB, control_root_path=control) is None

    def test_a_conflicting_archive_is_never_overwritten(self, control):
        signal = request_stop(JOB, "x", "cli", control_root_path=control)
        archived = stop_archive_dir(JOB, control) / f"{signal.request_id}.json"
        archived.parent.mkdir(parents=True, exist_ok=True)
        archived.write_text(json.dumps({"stop_signal_v": 1, "job_id": JOB,
                                        "request_id": signal.request_id,
                                        "reason": "something else", "source": "cli",
                                        "requested_at": ""}, indent=2, sort_keys=True) + "\n")

        with pytest.raises(StopArchiveConflictError):
            consume_stop(JOB, control_root_path=control)
        # The stop is NOT reported as consumed: the request is still pending.
        assert stop_requested(JOB, control_root_path=control) == signal

    def test_a_failed_archive_leaves_the_request_pending(self, control):
        signal = request_stop(JOB, "x", "cli", control_root_path=control)
        adir = stop_archive_dir(JOB, control)
        adir.mkdir(parents=True, exist_ok=True)
        os.chmod(adir, 0o500)
        try:
            with pytest.raises(StopControlError):
                consume_stop(JOB, control_root_path=control)
            assert stop_requested(JOB, control_root_path=control) == signal
        finally:
            os.chmod(adir, 0o700)


class TestClearAndStatus:
    def test_clear_drops_a_pending_request_without_creating_an_episode(self, control):
        request_stop(JOB, "x", "cli", control_root_path=control)
        assert clear_stop(JOB, control_root_path=control) is True
        assert stop_requested(JOB, control_root_path=control) is None
        assert not stop_archive_dir(JOB, control).exists()
        assert clear_stop(JOB, control_root_path=control) is False

    def test_status_distinguishes_nothing_pending_and_consumed(self, control):
        empty = stop_status(JOB, control_root_path=control)
        assert empty.pending is None and empty.consumed_count == 0

        request_stop(JOB, "first", "cli", control_root_path=control)
        pending = stop_status(JOB, control_root_path=control)
        assert pending.pending is not None and pending.consumed_count == 0

        consume_stop(JOB, control_root_path=control)
        consumed = stop_status(JOB, control_root_path=control)
        assert consumed.pending is None and consumed.consumed_count == 1

        request_stop(JOB, "second", "cli", control_root_path=control)
        both = stop_status(JOB, control_root_path=control)
        assert both.pending is not None and both.consumed_count == 1

    def test_status_json_has_no_absolute_paths(self, control):
        request_stop(JOB, "x", "cli", control_root_path=control)
        consume_stop(JOB, control_root_path=control)
        raw = json.dumps(stop_status(JOB, control_root_path=control).to_json())
        assert str(control) not in raw


class TestTheSafePointCheckIsCheap:
    def test_it_loads_no_config(self, control, monkeypatch):
        request_stop(JOB, "x", "cli", control_root_path=control)

        import packages.orchestration.config as cfg

        def _explode(*a, **k):                    # a safe point must never do this
            raise AssertionError("stop_requested() loaded the config system")

        monkeypatch.setattr(cfg, "get_config", _explode)
        assert stop_requested(JOB, control_root_path=control) is not None

    def test_it_touches_only_the_one_file(self, control, monkeypatch):
        request_stop(JOB, "x", "cli", control_root_path=control)

        scanned: list[str] = []
        real_iterdir = Path.iterdir

        def _watch(self):                         # no directory scan on the hot path
            scanned.append(str(self))
            return real_iterdir(self)

        monkeypatch.setattr(Path, "iterdir", _watch)
        assert stop_requested(JOB, control_root_path=control) is not None
        assert scanned == []


class TestTheSignalIsBounded:
    def test_a_huge_reason_is_truncated(self, control):
        signal = request_stop(JOB, "x" * 5000, "y" * 5000, control_root_path=control)
        assert len(signal.reason) <= 500
        assert len(signal.source) <= 120

    def test_a_multiline_reason_becomes_one_line(self, control):
        signal = request_stop(JOB, "stop\nnow\r\nplease", "cli", control_root_path=control)
        assert "\n" not in signal.reason and "\r" not in signal.reason

    def test_an_empty_reason_is_unknown_not_blank(self, control):
        signal = request_stop(JOB, "", "", control_root_path=control)
        assert signal.reason == UNKNOWN_REASON and signal.source == "unknown"

    def test_the_signal_is_immutable(self):
        signal = StopSignal(job_id=JOB, request_id="abc")
        with pytest.raises(Exception):
            signal.reason = "changed"        # type: ignore[misc]


# ---------------------------------------------------------------------------
# Hardening round 1 — what the external review found
# ---------------------------------------------------------------------------

from packages.orchestration.safe_points import (  # noqa: E402
    acknowledge_stop,
    archive_stop,
    archived_signals,
    is_safe_id,
    normalize_timestamp,
)


def _write_raw(control: Path, job_id: str, text: str) -> Path:
    path = control / "jobs" / job_id / "stop.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path


class TestNoParentComponentMayBeASymlink:
    """The reviewed build validated only the FINAL path. `control -> outside` therefore
    wrote `outside/jobs/<job>/stop.json` — precisely the class of bug F010 had already
    fixed. The control area now uses the same directory-FD-anchored primitives."""

    def test_a_symlinked_control_root_writes_nothing_outside(self, control, tmp_path):
        outside = tmp_path / "outside"
        outside.mkdir()
        control.symlink_to(outside)

        with pytest.raises(StopControlError, match="symlink"):
            request_stop(JOB, "x", "cli", control_root_path=control)
        assert list(outside.iterdir()) == []

    def test_a_symlinked_jobs_directory_writes_nothing_outside(self, control, tmp_path):
        outside = tmp_path / "outside"
        outside.mkdir()
        control.mkdir(parents=True)
        (control / "jobs").symlink_to(outside)

        with pytest.raises(StopControlError, match="symlink"):
            request_stop(JOB, "x", "cli", control_root_path=control)
        assert list(outside.iterdir()) == []

    def test_a_symlinked_archive_directory_writes_nothing_outside(self, control, tmp_path):
        outside = tmp_path / "outside"
        outside.mkdir()
        signal = request_stop(JOB, "x", "cli", control_root_path=control)
        (control / "jobs" / JOB / "archive").symlink_to(outside)

        with pytest.raises(StopControlError, match="symlink"):
            archive_stop(JOB, signal, control_root_path=control)
        assert list(outside.iterdir()) == []
        assert stop_requested(JOB, control_root_path=control) == signal   # still pending

    def test_an_internal_symlink_inside_the_control_root_is_refused(self, control,
                                                                    tmp_path):
        inside_target = control / "elsewhere"
        inside_target.mkdir(parents=True)
        (control / "jobs").mkdir()
        (control / "jobs" / JOB).symlink_to(inside_target)

        with pytest.raises(StopControlError, match="symlink"):
            request_stop(JOB, "x", "cli", control_root_path=control)
        assert list(inside_target.iterdir()) == []

    def test_an_ineffective_O_NOFOLLOW_is_still_caught(self, control, tmp_path,
                                                       monkeypatch):
        """The review host that broke F010 accepts `O_NOFOLLOW` and follows the link anyway.
        The refusal must come from OUR identity check, not from the kernel's goodwill."""
        outside = tmp_path / "outside"
        outside.mkdir()
        control.mkdir(parents=True)
        (control / "jobs").symlink_to(outside)

        real_open = os.open

        def _open_without_nofollow(path, flags, *a, **kw):
            return real_open(path, flags & ~getattr(os, "O_NOFOLLOW", 0), *a, **kw)

        monkeypatch.setattr(os, "open", _open_without_nofollow)

        with pytest.raises(StopControlError):
            request_stop(JOB, "x", "cli", control_root_path=control)
        assert list(outside.iterdir()) == []

    def test_no_temp_file_and_no_fd_leak_survive_a_refusal(self, control, tmp_path):
        outside = tmp_path / "outside"
        outside.mkdir()
        control.mkdir(parents=True)
        (control / "jobs").mkdir()
        (control / "jobs" / JOB).symlink_to(outside)

        before = len(os.listdir("/proc/self/fd"))
        for _ in range(20):
            with pytest.raises(StopControlError):
                request_stop(JOB, "x", "cli", control_root_path=control)
        after = len(os.listdir("/proc/self/fd"))

        assert after <= before + 1, "the refusal path leaks file descriptors"
        assert list(outside.iterdir()) == []


class TestAMaliciousRequestIdCannotTraverse:
    """`request_id: "../../../../escaped"` used to survive degraded parsing and then became
    `escaped.json` OUTSIDE the archive directory."""

    @pytest.mark.parametrize("evil", [
        "../escaped", "../../../../escaped", "a/b", "a\\b", "/etc/passwd",
        "C:\\windows\\system32", "", "x" * 200, ".", "..",
    ])
    def test_an_unsafe_id_never_becomes_a_path(self, control, tmp_path, evil):
        _write_raw(control, JOB, json.dumps(
            {"stop_signal_v": 1, "request_id": evil, "reason": "r", "source": "s"}))

        signal = stop_requested(JOB, control_root_path=control)
        assert signal is not None and signal.degraded
        assert signal.request_id.startswith("malformed-")
        assert is_safe_id(signal.request_id)

        consume_stop(JOB, control_root_path=control)
        archives = list((control / "jobs" / JOB / "archive").glob("*.json"))
        assert len(archives) == 1
        assert archives[0].name == f"{signal.request_id}.json"
        # ...and nothing was created anywhere else under the temporary root.
        assert not (tmp_path / "escaped.json").exists()
        assert not (control / "jobs" / JOB / "escaped.json").exists()

    def test_an_unknown_version_with_a_malicious_id_is_also_degraded(self, control):
        _write_raw(control, JOB, json.dumps(
            {"stop_signal_v": 99, "request_id": "../../../escaped"}))
        signal = stop_requested(JOB, control_root_path=control)
        assert signal.degraded and signal.request_id.startswith("malformed-")

    def test_the_archive_boundary_refuses_an_unsafe_id_even_if_handed_one(self, control):
        request_stop(JOB, "x", "cli", control_root_path=control)
        evil = StopSignal(job_id=JOB, request_id="../../escaped")
        with pytest.raises(StopControlError, match="unsafe request id"):
            archive_stop(JOB, evil, control_root_path=control)

    def test_the_degraded_id_is_deterministic(self, control):
        _write_raw(control, JOB, "garbage bytes")
        first = stop_requested(JOB, control_root_path=control)
        second = stop_requested(JOB, control_root_path=control)
        assert first.request_id == second.request_id     # the same corrupt file is ONE stop


class TestRequestedAtIsNotFreeText:
    """`requested_at` was copied verbatim out of the control file into the ledger, the
    post-mortem and the Evidence bundle."""

    @pytest.mark.parametrize("evil", [
        "API_KEY=supersecret /home/alice/private",
        "/home/alice/secrets/token.txt",
        "sk-live-abcdef123456",
        "x" * 500,
        "not a timestamp",
    ])
    def test_a_malicious_timestamp_is_dropped(self, control, evil):
        _write_raw(control, JOB, json.dumps(
            {"stop_signal_v": 1, "request_id": "abc123def456", "reason": "r",
             "source": "s", "requested_at": evil}))

        signal = stop_requested(JOB, control_root_path=control)
        assert signal.requested_at == ""
        raw = json.dumps(signal.to_json())
        assert "supersecret" not in raw and "/home/alice" not in raw
        assert "sk-live" not in raw

    def test_a_real_timestamp_survives(self, control):
        stamp = "2026-07-14T10:00:00+00:00"
        _write_raw(control, JOB, json.dumps(
            {"stop_signal_v": 1, "request_id": "abc123def456", "reason": "r",
             "source": "s", "requested_at": stamp}))
        assert stop_requested(JOB, control_root_path=control).requested_at == stamp

    def test_normalize_timestamp_is_total(self):
        assert normalize_timestamp(None) == ""
        assert normalize_timestamp(12345) == ""
        assert normalize_timestamp("2026-07-14") == "2026-07-14"


class TestConcurrentRequestsConvergeOnOneId:
    def test_two_threads_return_the_same_request_id(self, control):
        import threading

        results: list[StopSignal] = []
        barrier = threading.Barrier(2)

        def _ask(reason: str) -> None:
            barrier.wait()
            results.append(request_stop(JOB, reason, "cli", control_root_path=control))

        threads = [threading.Thread(target=_ask, args=(f"caller {i}",)) for i in range(2)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len({s.request_id for s in results}) == 1, "two callers, two episodes"
        on_disk = stop_requested(JOB, control_root_path=control)
        assert on_disk.request_id == results[0].request_id

    def test_a_publication_race_returns_the_winners_signal(self, control, monkeypatch):
        """Force the exact interleaving: our caller reads "nothing pending", another caller
        publishes, and only THEN does our caller try to link. The reviewed build used
        `os.replace` and silently destroyed the winner's request."""
        import packages.common.secure_fs as fs

        winner: dict[str, StopSignal] = {}
        real_write = fs.write_file_atomically

        def _slip_in_first(dir_fd, name, data, **kw):
            if name == "stop.json" and "winner" not in winner:
                winner["winner"] = None                    # re-entry guard
                monkeypatch.undo()
                winner["winner"] = request_stop(JOB, "the other terminal", "cli",
                                                control_root_path=control)
            return real_write(dir_fd, name, data, **kw)

        monkeypatch.setattr(
            "packages.orchestration.safe_points._fs.write_file_atomically", _slip_in_first)

        got = request_stop(JOB, "our terminal", "cli", control_root_path=control)
        assert got.request_id == winner["winner"].request_id
        assert got.reason == "the other terminal"      # the winner's request stands


class TestTheTwoStepConsume:
    def test_archiving_does_not_remove_the_pending_request(self, control):
        signal = request_stop(JOB, "x", "cli", control_root_path=control)
        ref = archive_stop(JOB, signal, control_root_path=control)

        assert ref == f"jobs/{JOB}/archive/{signal.request_id}.json"
        assert stop_requested(JOB, control_root_path=control) == signal   # STILL pending
        assert len(archived_signals(JOB, control_root_path=control)) == 1

    def test_archiving_twice_is_idempotent(self, control):
        signal = request_stop(JOB, "x", "cli", control_root_path=control)
        archive_stop(JOB, signal, control_root_path=control)
        archive_stop(JOB, signal, control_root_path=control)
        assert len(archived_signals(JOB, control_root_path=control)) == 1

    def test_acknowledge_removes_only_our_own_request(self, control):
        first = request_stop(JOB, "first", "cli", control_root_path=control)
        archive_stop(JOB, first, control_root_path=control)
        acknowledge_stop(JOB, first, control_root_path=control)
        assert stop_requested(JOB, control_root_path=control) is None

        second = request_stop(JOB, "second", "cli", control_root_path=control)
        # A stale finalization must not delete the NEXT episode's request.
        assert acknowledge_stop(JOB, first, control_root_path=control) is False
        assert stop_requested(JOB, control_root_path=control) == second


# ---------------------------------------------------------------------------
# Hardening round 2 — the PARENT of the trusted root
# ---------------------------------------------------------------------------

class TestTheParentOfTheControlRootIsVerifiedToo:
    """`anchor_root()` used to verify the root's final component and then open its PARENT by
    raw name. With `real/link -> outside`, a control root of `real/link/control` was
    "verified" and the whole control area landed in `outside`. Every component from the
    filesystem root down is now walked and identity-checked."""

    def test_anchor_root_rejects_a_symlinked_parent(self, tmp_path):
        from packages.common import secure_fs as fs

        outside = tmp_path / "outside"
        (outside / "control").mkdir(parents=True)
        (tmp_path / "real").mkdir()
        (tmp_path / "real" / "link").symlink_to(outside)

        with pytest.raises(fs.SecureFsError, match="symlink"):
            fs.anchor_root(tmp_path / "real" / "link" / "control")

    def test_request_stop_through_a_symlinked_parent_writes_nothing_outside(self, tmp_path):
        outside = tmp_path / "outside"
        (outside / "control").mkdir(parents=True)
        (tmp_path / "real").mkdir()
        (tmp_path / "real" / "link").symlink_to(outside)
        control = tmp_path / "real" / "link" / "control"

        with pytest.raises(StopControlError, match="symlink"):
            request_stop(JOB, "x", "cli", control_root_path=control)

        assert list((outside / "control").iterdir()) == []
        assert not (outside / "control" / "jobs").exists()

    def test_a_missing_root_under_a_symlinked_parent_creates_nothing_outside(self, tmp_path):
        outside = tmp_path / "outside"
        outside.mkdir()
        (tmp_path / "real").mkdir()
        (tmp_path / "real" / "link").symlink_to(outside)
        control = tmp_path / "real" / "link" / "control"

        with pytest.raises(StopControlError, match="symlink"):
            request_stop(JOB, "x", "cli", control_root_path=control)

        assert list(outside.iterdir()) == []      # `control` was never created out there

    def test_reading_through_a_symlinked_parent_is_refused_too(self, tmp_path):
        outside = tmp_path / "outside"
        (outside / "control").mkdir(parents=True)
        (tmp_path / "real").mkdir()
        (tmp_path / "real" / "link").symlink_to(outside)

        with pytest.raises(StopControlError, match="symlink"):
            stop_requested(JOB, control_root_path=tmp_path / "real" / "link" / "control")

    def test_a_safe_missing_control_root_is_still_created(self, tmp_path):
        control = tmp_path / "data" / "control"          # neither component exists yet
        signal = request_stop(JOB, "x", "cli", control_root_path=control)

        assert control.is_dir()
        assert _stat.S_IMODE(control.stat().st_mode) == CONTROL_DIR_MODE
        assert stop_requested(JOB, control_root_path=control) == signal

    def test_a_relative_control_root_still_works(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        signal = request_stop(JOB, "x", "cli", control_root_path=Path("rel/control"))

        assert (tmp_path / "rel" / "control" / "jobs" / JOB / "stop.json").is_file()
        assert stop_requested(JOB, control_root_path=Path("rel/control")) == signal

    def test_an_absolute_control_root_still_works(self, tmp_path):
        control = tmp_path / "abs" / "control"
        signal = request_stop(JOB, "x", "cli", control_root_path=control.absolute())
        assert stop_requested(JOB, control_root_path=control) == signal

    def test_no_fd_leak_on_the_parent_symlink_refusal(self, tmp_path):
        outside = tmp_path / "outside"
        (outside / "control").mkdir(parents=True)
        (tmp_path / "real").mkdir()
        (tmp_path / "real" / "link").symlink_to(outside)
        control = tmp_path / "real" / "link" / "control"

        before = len(os.listdir("/proc/self/fd"))
        for _ in range(30):
            with pytest.raises(StopControlError):
                request_stop(JOB, "x", "cli", control_root_path=control)
        assert len(os.listdir("/proc/self/fd")) <= before + 1

"""F199 T002 — the local crash report: what it holds, what it leaves out, and who writes it."""

from __future__ import annotations

import os
import pathlib
import threading
from datetime import datetime, timedelta, timezone

from packages.orchestration import crash_report
from packages.orchestration.crash_report import (
    CRASH_NOTICE,
    config_digest,
    crash_reports_dir,
    install_thread_crash_hook,
    recent_crash_reports,
    render_crash_report,
    write_crash_report,
)

FIXED_TIME = datetime(2026, 10, 13, 12, 30, 45, 123456, tzinfo=timezone.utc)

PLANTED = (
    "AbCdEfGhIjKl",
    "hunter2secret",
    "plain-value-123",
    "abcdefghijklmnopqrstuvwxyz012345",
    "ghp_ABCDEF",
    "abcdef0123456789abcdef",
)


def _crash_with_secrets() -> RuntimeError:
    message = (
        "failed with sk-ant-api03-AbCdEfGhIjKlMnOpQrStUvWxYz0123456789 "
        "password=hunter2secret "
        '{"api_key": "plain-value-123"} '
        "Authorization: Bearer abcdefghijklmnopqrstuvwxyz012345 "
        "ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "
        "token=abcdef0123456789abcdef "
        "at " + str(pathlib.Path.home()) + "/project"
    )
    try:
        raise RuntimeError(message)
    except RuntimeError as caught:
        return caught


def _plain_crash() -> ValueError:
    try:
        raise ValueError("plain failure")
    except ValueError as caught:
        return caught


def test_a_crash_with_planted_secrets_is_written_without_them():
    path = write_crash_report(_crash_with_secrets(), command="job.list", now=FIXED_TIME)
    assert path is not None and path.is_file()
    assert path.parent == crash_reports_dir()
    assert path.name.startswith("20261013T123045123456Z-")
    assert (path.stat().st_mode & 0o777) == 0o600
    text = path.read_text(encoding="utf-8")
    for secret in (*PLANTED, str(pathlib.Path.home())):
        assert secret not in text
    for expected in (
        "[REDACTED]", "- command: job.list", "- version: ",
        "- configuration digest: sha256:", "## Traceback", "RuntimeError", CRASH_NOTICE,
    ):
        assert expected in text


def test_the_header_lines_of_a_fixed_input_are_exact():
    text = render_crash_report(
        _plain_crash(), command="job.list", when=FIXED_TIME, version="1.2.3", digest="sha256:abc")
    assert text.splitlines()[:7] == [
        "# Remedy crash report",
        "",
        "- time: 2026-10-13T12:30:45Z",
        "- version: 1.2.3",
        "- command: job.list",
        "- error: ValueError: plain failure",
        "- configuration digest: sha256:abc",
    ]
    assert text.endswith(CRASH_NOTICE + "\n")


def test_a_folder_that_cannot_be_made_gives_none_and_raises_nothing(tmp_path):
    blocker = tmp_path / "a-file"
    blocker.write_text("not a folder")
    assert write_crash_report(_plain_crash(), command="job.list", root=blocker) is None


def test_the_configuration_digest_is_unavailable_when_the_snapshot_fails(monkeypatch):
    from packages.orchestration import run_manifest

    def explode():
        raise ValueError("no configuration")

    monkeypatch.setattr(run_manifest, "_config_snapshot", explode)
    assert config_digest() == "unavailable"


def test_a_thread_that_raises_writes_one_report_and_calls_the_previous_hook(
    tmp_path, monkeypatch,
):
    seen: list[threading.ExceptHookArgs] = []
    monkeypatch.setattr(threading, "excepthook", seen.append)
    previous = threading.excepthook
    restore = install_thread_crash_hook("serve.start", root=tmp_path)
    assert threading.excepthook is not previous

    def boom() -> None:
        raise RuntimeError("thread failure")

    worker = threading.Thread(target=boom, name="probe-thread")
    worker.start()
    worker.join()
    restore()
    assert threading.excepthook is previous
    assert len(seen) == 1
    reports = list(crash_reports_dir(tmp_path).glob("*.md"))
    assert len(reports) == 1
    text = reports[0].read_text(encoding="utf-8")
    assert "- command: serve.start (thread probe-thread)" in text
    assert "RuntimeError: thread failure" in text


def test_a_thread_that_ends_on_system_exit_writes_no_report(tmp_path, monkeypatch):
    monkeypatch.setattr(threading, "excepthook", lambda _args: None)
    restore = install_thread_crash_hook("serve.start", root=tmp_path)

    def leave() -> None:
        raise SystemExit(0)

    worker = threading.Thread(target=leave, name="leaver")
    worker.start()
    worker.join()
    restore()
    assert not crash_reports_dir(tmp_path).exists() or not list(
        crash_reports_dir(tmp_path).glob("*.md"))


def test_recent_reports_leave_out_an_eight_day_old_one_and_come_newest_first(tmp_path):
    now = datetime.now(timezone.utc)
    folder = crash_reports_dir(tmp_path)
    folder.mkdir(parents=True)
    ages = {"old.md": timedelta(days=8), "mid.md": timedelta(days=2), "new.md": timedelta(hours=1)}
    for name, age in ages.items():
        path = folder / name
        path.write_text("report")
        stamp = (now - age).timestamp()
        os.utime(path, (stamp, stamp))
    found = recent_crash_reports(tmp_path, now=now)
    assert [path.name for path in found] == ["new.md", "mid.md"]


def test_recent_reports_of_a_missing_folder_is_empty(tmp_path):
    assert recent_crash_reports(tmp_path) == []


def test_the_notice_says_remedy_never_sends_the_report():
    assert "never sends" in crash_report.CRASH_NOTICE


# A private key written so that no source line of this file names it whole (R-1280).
PEM = "-----BEGIN RSA " + "PRIVATE KEY-----\nMIIEabcdef\n-----END RSA " + "PRIVATE KEY-----"


def test_a_private_key_in_the_error_hides_only_the_error_and_its_traceback_entry():
    """R-1280, DECISION F307 D5: each part is redacted on its own, so the rest of the report stays."""
    try:
        raise RuntimeError("bad key " + PEM)
    except RuntimeError as caught:
        error = caught
    text = render_crash_report(error, command="job.list", when=FIXED_TIME, version="1.2.3", digest="sha256:abc")
    assert text.splitlines()[2:7] == [
        "- time: 2026-10-13T12:30:45Z",
        "- version: 1.2.3",
        "- command: job.list",
        "- error: [PRIVATE_KEY_REDACTED]",
        "- configuration digest: sha256:abc",
    ]
    assert "Traceback (most recent call last):" in text
    assert "in test_a_private_key_in_the_error_hides_only_the_error_and_its_traceback_entry" in text
    assert "MIIEabcdef" not in text and "BEGIN RSA" not in text
    assert text.endswith(CRASH_NOTICE + "\n")


def test_a_secret_in_the_command_is_redacted_on_its_own_line():
    text = render_crash_report(
        _plain_crash(), command="job.list --token=abcdef0123456789abcdef", when=FIXED_TIME,
        version="1.2.3", digest="sha256:abc")
    assert "abcdef0123456789abcdef" not in text
    assert "- error: ValueError: plain failure" in text

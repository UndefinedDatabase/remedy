"""F278 T001 — `secure_fs.durable_write`, the one path-based durable write.

Every later slice of F278 migrates a private atomic-write helper onto this one and deletes the
copy, so these tests pin what the migration is allowed to rely on: both fsyncs happen, in the
order that makes the publication survive a crash; concurrent writers of one record never share
a temporary path; a failure leaves neither residue nor a half-written target; and the file gets
exactly the mode asked for.
"""
from __future__ import annotations

import json
import os
import stat as _stat
import threading
from pathlib import Path

import pytest

from packages.common import secure_fs
from packages.common.secure_fs import durable_write, durable_write_json


def _record_fsyncs(monkeypatch: pytest.MonkeyPatch) -> list[tuple[str, int]]:
    """Wrap the real ``os.fsync`` and record (kind, inode) of every descriptor it is handed."""
    calls: list[tuple[str, int]] = []
    real_fsync = os.fsync

    def recording_fsync(fd: int) -> None:
        st = os.fstat(fd)
        kind = "dir" if _stat.S_ISDIR(st.st_mode) else "file" if _stat.S_ISREG(st.st_mode) else "other"
        calls.append((kind, st.st_ino))
        real_fsync(fd)

    monkeypatch.setattr(secure_fs.os, "fsync", recording_fsync)
    return calls


class TestBothFsyncsHappen:
    def test_the_file_and_then_its_parent_directory_are_fsynced(
            self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        calls = _record_fsyncs(monkeypatch)
        target = tmp_path / "record.json"

        durable_write(target, b"payload\n")

        assert calls == [("file", target.stat().st_ino), ("dir", tmp_path.stat().st_ino)], (
            "durable_write must fsync the file it publishes, then the directory holding it")

    def test_fsync_dir_false_skips_only_the_directory(
            self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        calls = _record_fsyncs(monkeypatch)
        target = tmp_path / "record.json"

        durable_write(target, b"payload\n", fsync_dir=False)

        assert calls == [("file", target.stat().st_ino)]


class TestConcurrentWritersOfOnePath:
    def test_eight_writers_leave_exactly_one_intact_payload_and_no_residue(
            self, tmp_path: Path) -> None:
        target = tmp_path / "shared.json"
        # Distinct sizes, so a torn or interleaved file cannot equal any one payload by accident.
        payloads = [bytes([65 + i]) * (200_000 + i * 997) for i in range(8)]
        for _ in range(10):
            barrier = threading.Barrier(len(payloads))
            errors: list[OSError] = []

            def writer(data: bytes) -> None:
                barrier.wait()
                try:
                    durable_write(target, data)
                except OSError as exc:  # collected and asserted below, never swallowed
                    errors.append(exc)

            threads = [threading.Thread(target=writer, args=(p,)) for p in payloads]
            for t in threads:
                t.start()
            for t in threads:
                t.join()

            assert errors == [], f"a concurrent writer failed: {errors!r}"
            assert target.read_bytes() in payloads, "the published file is no writer's payload"
            assert sorted(p.name for p in tmp_path.iterdir()) == ["shared.json"], (
                "a temporary file was left beside the target")


class TestTheTemporaryFile:
    def test_a_multi_suffix_name_keeps_its_temporary_file_a_sibling_under_its_whole_name(
            self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        seen: list[str] = []
        real_replace = os.replace

        def recording_replace(src, dst) -> None:
            seen.append(os.fspath(src))
            real_replace(src, dst)

        monkeypatch.setattr(secure_fs.os, "replace", recording_replace)
        target = tmp_path / "a.b.json"

        durable_write(target, b"{}\n")

        assert len(seen) == 1
        tmp = Path(seen[0])
        assert tmp.parent == tmp_path, "the temporary file must live in the destination directory"
        assert tmp.name.startswith(".a.b.json."), (
            f"the temporary name {tmp.name!r} must carry the whole destination name")
        assert target.read_bytes() == b"{}\n"

    def test_a_failed_publish_leaves_no_residue_and_the_old_file_untouched(
            self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        target = tmp_path / "record.json"
        target.write_bytes(b"old\n")

        def failing_replace(src, dst) -> None:
            raise OSError("simulated rename failure")

        monkeypatch.setattr(secure_fs.os, "replace", failing_replace)

        with pytest.raises(OSError, match="simulated rename failure"):
            durable_write(target, b"new\n")

        assert target.read_bytes() == b"old\n"
        assert sorted(p.name for p in tmp_path.iterdir()) == ["record.json"]

    def test_a_failed_write_leaves_no_residue(
            self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        def failing_write(fd: int, data) -> int:
            raise OSError("simulated disk full")

        monkeypatch.setattr(secure_fs.os, "write", failing_write)

        with pytest.raises(OSError, match="simulated disk full"):
            durable_write(tmp_path / "record.json", b"data\n")

        assert list(tmp_path.iterdir()) == []


class TestModeAndShape:
    def test_the_default_mode_is_private_whatever_the_umask(self, tmp_path: Path) -> None:
        old = os.umask(0)
        try:
            durable_write(tmp_path / "private.json", "text\n")
        finally:
            os.umask(old)

        assert _stat.S_IMODE((tmp_path / "private.json").stat().st_mode) == 0o600

    def test_an_explicit_mode_is_applied_exactly(self, tmp_path: Path) -> None:
        durable_write(tmp_path / "shared.txt", b"x", mode=0o644)

        assert _stat.S_IMODE((tmp_path / "shared.txt").stat().st_mode) == 0o644

    def test_a_str_is_written_as_utf8(self, tmp_path: Path) -> None:
        durable_write(tmp_path / "text.txt", "grüße\n")

        assert (tmp_path / "text.txt").read_bytes() == "grüße\n".encode()

    def test_durable_write_json_writes_standard_sorted_json(self, tmp_path: Path) -> None:
        target = tmp_path / "doc.json"

        durable_write_json(target, {"b": 1, "a": [True, None]})

        text = target.read_text(encoding="utf-8")
        assert text.endswith("\n")
        assert json.loads(text) == {"a": [True, None], "b": 1}
        assert text.index('"a"') < text.index('"b"')

    def test_durable_write_json_refuses_a_non_finite_float(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError):
            durable_write_json(tmp_path / "doc.json", {"x": float("nan")})

        assert list(tmp_path.iterdir()) == []

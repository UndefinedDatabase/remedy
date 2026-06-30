"""Tests for scratch_file_guard.py — root scan + allow logic + writer."""

from __future__ import annotations

import json
from pathlib import Path

from packages.orchestration.scratch_file_guard import (
    FORBIDDEN_PATTERNS,
    build_scratch_file_guard,
    write_scratch_file_guard,
)


def _touch(path: Path) -> None:
    path.write_text("# scratch\n", encoding="utf-8")


def test_clean_workspace_passes(tmp_path: Path) -> None:
    _touch(tmp_path / "main.py")
    (tmp_path / "packages").mkdir()

    guard = build_scratch_file_guard(str(tmp_path))

    assert guard["guard_status"] == "PASS"
    assert guard["schema_version"] == "1.0.0"
    assert guard["checked_patterns"] == list(FORBIDDEN_PATTERNS)
    assert guard["files_found"] == []
    assert guard["forbidden_files"] == []
    assert guard["suggested_cleanup"] == []


def test_forbidden_files_block(tmp_path: Path) -> None:
    _touch(tmp_path / "_run_thing.py")
    _touch(tmp_path / "_pt_check.py")
    _touch(tmp_path / "_cleanup_tmp.py")
    _touch(tmp_path / "keep.py")

    guard = build_scratch_file_guard(str(tmp_path))

    assert guard["guard_status"] == "BLOCKED"
    assert set(guard["forbidden_files"]) == {
        "_run_thing.py",
        "_pt_check.py",
        "_cleanup_tmp.py",
    }
    assert set(guard["files_found"]) == set(guard["forbidden_files"])
    assert guard["suggested_cleanup"] == [f"rm {p}" for p in guard["forbidden_files"]]


def test_dunder_modules_not_flagged(tmp_path: Path) -> None:
    _touch(tmp_path / "__init__.py")
    _touch(tmp_path / "__main__.py")

    guard = build_scratch_file_guard(str(tmp_path))

    assert guard["guard_status"] == "PASS"
    assert guard["files_found"] == []


def test_allowed_file_not_flagged(tmp_path: Path) -> None:
    _touch(tmp_path / "_run_thing.py")

    guard = build_scratch_file_guard(str(tmp_path), allowed_files=["_run_thing.py"])

    assert guard["guard_status"] == "PASS"
    assert guard["forbidden_files"] == []
    assert guard["allowed_files_found"] == ["_run_thing.py"]
    assert guard["files_found"] == ["_run_thing.py"]


def test_nested_files_ignored(tmp_path: Path) -> None:
    sub = tmp_path / "packages"
    sub.mkdir()
    _touch(sub / "_run_nested.py")

    guard = build_scratch_file_guard(str(tmp_path))

    assert guard["guard_status"] == "PASS"
    assert guard["files_found"] == []


def test_missing_workspace_passes() -> None:
    guard = build_scratch_file_guard("/nonexistent/workspace/path")

    assert guard["guard_status"] == "PASS"
    assert guard["files_found"] == []


def test_writer_job_level(tmp_path: Path) -> None:
    ws = tmp_path / "ws"
    ws.mkdir()
    _touch(ws / "_run_thing.py")
    ev = tmp_path / "evidence"
    ev.mkdir()
    written: dict[str, str] = {}

    write_scratch_file_guard(str(ws), str(ev), "", None, written)

    assert "scratch_file_guard.json" in written
    data = json.loads((ev / "scratch_file_guard.json").read_text())
    assert data["guard_status"] == "BLOCKED"
    assert data["task_id"] == ""
    assert data["forbidden_files"] == ["_run_thing.py"]


def test_writer_task_level(tmp_path: Path) -> None:
    ws = tmp_path / "ws"
    ws.mkdir()
    _touch(ws / "_run_scratch.py")
    ev = tmp_path / "evidence"
    ev.mkdir()
    written: dict[str, str] = {}

    write_scratch_file_guard(str(ws), str(ev), "T001", None, written)

    rel = "task_runs/T001/scratch_file_guard.json"
    assert rel in written
    data = json.loads((ev / "task_runs" / "T001" / "scratch_file_guard.json").read_text())
    assert data["task_id"] == "T001"
    assert data["guard_status"] == "BLOCKED"


def test_writer_merges_review_scope_changed_files(tmp_path: Path) -> None:
    ws = tmp_path / "ws"
    ws.mkdir()
    _touch(ws / "_run_thing.py")
    ev = tmp_path / "evidence"
    packet_dir = ev / "task_runs" / "T001"
    packet_dir.mkdir(parents=True)
    (packet_dir / "review_scope_packet.json").write_text(
        json.dumps({"changed_files": ["_run_thing.py"]}), encoding="utf-8"
    )
    written: dict[str, str] = {}

    write_scratch_file_guard(str(ws), str(ev), "", None, written)

    data = json.loads((ev / "scratch_file_guard.json").read_text())
    assert data["guard_status"] == "PASS"
    assert data["allowed_files_found"] == ["_run_thing.py"]


def test_writer_noop_without_evidence_dir(tmp_path: Path) -> None:
    written: dict[str, str] = {}
    write_scratch_file_guard(str(tmp_path), "", "", None, written)
    assert written == {}


def test_root_underscore_python_file_is_blocked(tmp_path: Path) -> None:
    _touch(tmp_path / "_scratch.py")

    guard = build_scratch_file_guard(str(tmp_path))

    assert guard["guard_status"] == "BLOCKED"
    assert "_scratch.py" in guard["forbidden_files"]


def test_root_underscore_python_file_allowed_when_explicitly_scoped(tmp_path: Path) -> None:
    _touch(tmp_path / "_scratch.py")

    guard = build_scratch_file_guard(str(tmp_path), allowed_files=["_scratch.py"])

    assert guard["guard_status"] == "PASS"
    assert "_scratch.py" in guard["allowed_files_found"]
    assert guard["forbidden_files"] == []

"""footprint(): one read-only walk of the data root, per child and per class (F276 T001)."""
from __future__ import annotations

import os

from packages.orchestration.data_footprint import export_footprint_json, footprint


def _write(path, size: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"x" * size)


def _tree(root):
    _write(root / "job_workspaces" / "staging_a" / "big.bin", 3000)
    _write(root / "job_workspaces" / "staging_a" / "src" / "a.py", 100)
    _write(root / "jobs" / "j1" / "job.json", 40)
    _write(root / "task_jobs" / "old.json", 11)
    _write(root / "stray.txt", 5)


def test_bytes_and_files_per_child_and_per_class(tmp_path):
    _tree(tmp_path)
    body = export_footprint_json(footprint(tmp_path))
    assert body["exists"] is True
    assert body["children"] == [
        {"name": "job_workspaces", "class": "ephemeral", "bytes": 3100, "files": 2},
        {"name": "jobs", "class": "durable", "bytes": 40, "files": 1},
        {"name": "stray.txt", "class": "unclassified", "bytes": 5, "files": 1},
        {"name": "task_jobs", "class": "unclassified", "bytes": 11, "files": 1},
    ]
    assert body["classes"] == {
        "ephemeral": {"bytes": 3100, "files": 2},
        "durable": {"bytes": 40, "files": 1},
        "unclassified": {"bytes": 16, "files": 2},
    }
    assert body["total"] == {"bytes": 3156, "files": 5}


def test_a_symlink_is_counted_by_its_own_size_and_never_followed(tmp_path):
    outside = tmp_path / "outside"
    _write(outside / "huge.bin", 50_000)
    root = tmp_path / "data"
    _write(root / "jobs" / "j1" / "job.json", 40)
    os.symlink(outside, root / "jobs" / "link_dir")
    os.symlink(outside / "huge.bin", root / "runs")
    fp = footprint(root)
    by_name = {c.name: c for c in fp.children}
    link_dir_size = os.lstat(root / "jobs" / "link_dir").st_size
    assert (by_name["jobs"].bytes, by_name["jobs"].files) == (40 + link_dir_size, 2)
    assert by_name["runs"].bytes == os.lstat(root / "runs").st_size < 50_000
    assert fp.total_bytes < 50_000


def test_a_missing_root_is_reported_not_raised(tmp_path):
    body = export_footprint_json(footprint(tmp_path / "absent"))
    assert body["exists"] is False
    assert body["children"] == []
    assert body["total"] == {"bytes": 0, "files": 0}


def test_the_walk_shells_out_to_nothing(tmp_path, monkeypatch):
    import subprocess

    def refuse(*_a, **_k):
        raise AssertionError("footprint started a process")

    monkeypatch.setattr(subprocess, "Popen", refuse)
    monkeypatch.setattr(os, "system", refuse)
    _tree(tmp_path)
    assert footprint(tmp_path).total_files == 5


def test_the_walk_writes_nothing(tmp_path):
    _tree(tmp_path)
    before = sorted((p.relative_to(tmp_path), p.stat().st_mtime_ns) for p in tmp_path.rglob("*"))
    footprint(tmp_path)
    after = sorted((p.relative_to(tmp_path), p.stat().st_mtime_ns) for p in tmp_path.rglob("*"))
    assert before == after

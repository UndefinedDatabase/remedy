"""`scripts/stage_review_reports.py` and its place in `make_review_zip.sh` (exec-1017 D5).

The review ZIP carries the newest ten review reports, newest first, failed runs included, with an
index, on the ordinary `make_review_zip.sh` call: no argument and no job id.
"""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import zipfile
from pathlib import Path

import pytest

from packages.orchestration.review_reports import REVIEW_REPORT_SCHEMA, write_review_report

REPO_ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location("stage_review_reports", REPO_ROOT / "scripts" / "stage_review_reports.py")
SRR = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(SRR)

SECRET = "sk-ant-api03-" + "Z" * 40


def _report(n: int, status: str = "completed") -> dict:
    report_id = f"rr-202610{n:02d}T120000Z-{n:08x}"
    return {"schema": REVIEW_REPORT_SCHEMA, "report_id": report_id,
            "started_at": f"2026-10-{n:02d}T12:00:00+00:00", "ended_at": f"2026-10-{n:02d}T12:05:00+00:00",
            "duration_s": 300.0, "outcome": {"status": status, "reason": f"run {n}"},
            "order": {"text": f"Order number {n}. token={SECRET}"},
            "configuration": {"lane": "bounded"}, "job_ids": [f"{n:016x}"]}


@pytest.fixture()
def data_root(tmp_path, monkeypatch) -> Path:
    root = tmp_path / "data"
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    for n in range(1, 12):                                  # eleven reports, the 3rd one failed
        write_review_report(_report(n, "failed" if n == 3 else "completed"))
    return root


def test_the_ten_newest_are_staged_newest_first_and_the_eleventh_is_left_out(data_root, tmp_path):
    dest = tmp_path / "staged"

    assert SRR.stage(dest) == 10

    index = json.loads((dest / "index.json").read_text())
    assert [entry["report_id"] for entry in index["reports"]] == [_report(n)["report_id"] for n in range(11, 1, -1)]
    assert not (dest / f"{_report(1)['report_id']}.json").exists()                 # the oldest
    assert next(e for e in index["reports"] if e["report_id"] == _report(3)["report_id"])["status"] == "failed"
    assert "| failed |" in (dest / "INDEX.md").read_text()


def test_staged_copies_hold_no_secret_and_staging_is_byte_for_byte_repeatable(data_root, tmp_path):
    first, second = tmp_path / "a", tmp_path / "b"
    SRR.stage(first)
    SRR.stage(second)

    for path in sorted(first.iterdir()):
        assert SECRET not in path.read_text()
        assert path.read_bytes() == (second / path.name).read_bytes()


def test_with_no_report_the_index_says_so_and_lists_none(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "empty"))

    assert SRR.stage(tmp_path / "staged") == 0
    index = json.loads((tmp_path / "staged" / "index.json").read_text())
    assert index["reports"] == [] and index["note"].startswith("no review report exists")


@pytest.mark.skipif(shutil.which("git") is None or shutil.which("zip") is None, reason="git and zip required")
def test_the_ordinary_review_zip_carries_the_ten_newest_reports_without_any_argument(data_root, tmp_path):
    from tests.orchestration.test_review_zip_hygiene import _make_git_repo_with_scripts

    repo = _make_git_repo_with_scripts(tmp_path)
    env = {**os.environ, "REMEDY_DATA_DIR": str(data_root), "REMEDY_REVIEW_DIR": "."}
    proc = subprocess.run(["bash", "scripts/make_review_zip.sh"], cwd=repo, env=env,
                          capture_output=True, text=True, timeout=120)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "Review reports packaged: 10" in proc.stdout
    [package] = list(repo.glob("remedy-review-*.zip"))
    with zipfile.ZipFile(package) as archive:
        names = set(archive.namelist())
        reports = sorted(name for name in names if name.startswith("review_reports/rr-"))
        assert len(reports) == 10 and f"review_reports/{_report(1)['report_id']}.json" not in names
        assert {"review_reports/index.json", "review_reports/INDEX.md"} <= names
        assert all(SECRET not in archive.read(name).decode() for name in reports)

"""Tests for `packages.orchestration.client_digest` (T002, DECISION F295 D4).

Each test sets `REMEDY_DATA_DIR` to a short directory from
`tmp_path_factory.mktemp`, as `tests/cli/test_serve_cmd.py` does.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from packages.orchestration.client_digest import build_client_digest
from packages.orchestration.job_apply import job_apply_landed

NOW = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)


@pytest.fixture
def root(tmp_path_factory, monkeypatch) -> Path:
    base = tmp_path_factory.mktemp("cd")
    monkeypatch.setenv("REMEDY_DATA_DIR", str(base))
    return base


def _apply_record(root: Path, job_id: str, name: str, body: str) -> None:
    record_dir = root / "job_apply_records" / job_id
    record_dir.mkdir(parents=True, exist_ok=True)
    (record_dir / name).write_text(body)


# ── job_apply_landed ──────────────────────────────────────────────────────


def test_job_apply_landed_is_false_with_no_records_directory(root):
    assert job_apply_landed("no-such-job") is False


@pytest.mark.parametrize("status", ["dry_run", "blocked"])
def test_job_apply_landed_is_false_for_a_status_that_is_not_applied(root, status):
    _apply_record(root, "job-1", "a.json", json.dumps({"status": status}))

    assert job_apply_landed("job-1") is False


def test_job_apply_landed_is_true_when_one_record_reads_applied(root):
    _apply_record(root, "job-2", "a.json", json.dumps({"status": "blocked"}))
    _apply_record(root, "job-2", "b.json", json.dumps({"status": "applied"}))

    assert job_apply_landed("job-2") is True


def test_job_apply_landed_skips_a_file_of_invalid_json_beside_an_applied_record(root):
    _apply_record(root, "job-3", "bad.json", "{not json")
    _apply_record(root, "job-3", "good.json", json.dumps({"status": "applied"}))

    assert job_apply_landed("job-3") is True


# ── build_client_digest ───────────────────────────────────────────────────


def test_build_client_digest_on_an_empty_data_root_equals_the_version_1_frame(root):
    digest = build_client_digest(now=NOW)

    assert digest == {
        "version": 1,
        "read_at": NOW.isoformat(),
        "supervisor": {"answers": False},
        "projects": [],
        "jobs": [],
        "awaiting_apply": [],
        "degraded": False,
        "skipped_files": [],
    }


def test_build_client_digest_names_a_job_file_that_is_not_valid_json_as_degraded(root):
    from packages.orchestration.data_paths import jobs_dir

    bad_dir = jobs_dir(root) / "bad-job-id"
    bad_dir.mkdir(parents=True)
    (bad_dir / "job.json").write_text("not json")

    digest = build_client_digest(now=NOW)

    assert digest["degraded"] is True
    assert "bad-job-id" in digest["skipped_files"]

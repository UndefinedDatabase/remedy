"""Tests for `packages.orchestration.client_changes` (F253, DECISION F253 D4 (2)).

Each test sets `REMEDY_DATA_DIR` to a short directory from `tmp_path_factory.mktemp`, as
`tests/orchestration/test_client_digest.py` does.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from packages.orchestration.client_changes import (
    CLIENT_CHANGES_OVERLAP_SECONDS,
    build_client_changes,
    parse_client_cursor,
)
from packages.orchestration.client_digest import build_client_digest
from packages.orchestration.data_paths import job_record_path
from packages.orchestration.pingpong_job import JobPlan, save_job_plan

NOW = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

REPO_ROOT = Path(__file__).resolve().parents[2]

#: Git identity for the scratch repository the seed below commits into.
_SEED_GIT_IDENTITY = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
                      "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
#: A deadline already in the past: the run's budget stops it before any task runs, raising the
#: one decision a fake run raises on its own (as tests/ui_server/test_public_api.py's
#: `_seed_project_job_and_decision` does; copied below rather than imported from that test module).
_SEED_PAST_DEADLINE = "2000-01-01T00:00:00+00:00"


@pytest.fixture
def root(tmp_path_factory, monkeypatch) -> Path:
    base = tmp_path_factory.mktemp("cc")
    monkeypatch.setenv("REMEDY_DATA_DIR", str(base))
    return base


def _seed_project_job_and_decision(tmp_path: Path) -> str:
    """Put one project, one job and one open decision on the current data root; the job id.

    Copied from `tests/ui_server/test_public_api.py`'s `_seed_project_job_and_decision`: an order
    file whose deadline has already passed stops the run before any task runs and raises the
    budget decision, so `remedy do` exits 1 and leaves one job with one open decision behind.
    """
    repo = tmp_path / "seed-repo"
    repo.mkdir()
    env = {**os.environ, **_SEED_GIT_IDENTITY}
    subprocess.run(["git", "init", "-q", str(repo)], check=True, env=env)
    (repo / "README.md").write_text("# Scratch\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "README.md"], check=True, env=env)
    subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", "init"], check=True, env=env)
    order_file = tmp_path / "seed-order.md"
    order_file.write_text(
        "---\nmax-cost-usd: 1\n---\nAdd a line saying hello to README.md\n", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "-m", "apps.cli.main", "do", str(order_file), "--json",
         "--no-ui", "--yes", "--no-llm", "--builder-provider", "fake",
         "--reviewer-provider", "fake", "--deadline", _SEED_PAST_DEADLINE],
        cwd=str(repo), capture_output=True, text=True, env=env, timeout=120)
    assert result.returncode == 1, result.stdout + result.stderr
    return json.loads(result.stdout)["job_ids"][0]


def _resolve_decision(job_id: str, decision_id: str, *, reason: str) -> dict:
    """`remedy decision resolve <job> <decision> --reason <reason> --json`'s parsed answer."""
    result = subprocess.run(
        [sys.executable, "-m", "apps.cli.main", "decision", "resolve", job_id, decision_id,
         "--reason", reason, "--json"],
        cwd=str(REPO_ROOT), capture_output=True, text=True,
        env={**os.environ}, timeout=30)
    return json.loads(result.stdout)


def _without_age(decisions: list[dict]) -> list[dict]:
    return [{k: v for k, v in d.items() if k != "age_seconds"} for d in decisions]


# ── parse_client_cursor ───────────────────────────────────────────────────


@pytest.mark.parametrize("text", [
    "2026-01-01T00:00:00Z", "2026-01-01T00:00:00+00:00", "2026-01-01T00:00:00+02:00",
])
def test_parse_client_cursor_reads_an_offset_or_a_trailing_z(text):
    parsed = parse_client_cursor(text)
    assert parsed.tzinfo is not None


@pytest.mark.parametrize("text", ["2026-01-01T00:00:00", "", "yesterday"])
def test_parse_client_cursor_refuses_a_naive_time_empty_string_and_nonsense(text):
    with pytest.raises(ValueError):
        parse_client_cursor(text)


# ── build_client_changes without `since` ──────────────────────────────────


def test_without_since_every_list_is_empty_and_cursor_equals_read_at(root):
    changes = build_client_changes(None, now=NOW)

    assert changes == {
        "read_at": NOW.isoformat(),
        "cursor": NOW.isoformat(),
        "since": None,
        "overlap_seconds": CLIENT_CHANGES_OVERLAP_SECONDS,
        "jobs": [],
        "decisions": [],
        "closed_decisions": [],
        "missions": [],
        "applies": [],
        "degraded": False,
        "skipped_files": [],
    }


# ── build_client_changes with `since`, against a seeded job ──────────────


def test_a_seeded_job_is_listed_with_its_decision_and_mission(root, tmp_path):
    before = datetime.now(timezone.utc) - timedelta(seconds=1)
    job_id = _seed_project_job_and_decision(tmp_path)

    changes = build_client_changes(before)
    digest = build_client_digest(job_ids=[job_id])

    [job_entry] = [j for j in changes["jobs"] if j["job_id"] == job_id]
    [reference_entry] = [j for j in digest["jobs"] if j["job_id"] == job_id]
    assert job_entry == reference_entry
    assert _without_age([d for d in changes["decisions"] if d["job_id"] == job_id]) == _without_age(
        [d for d in digest["decisions"] if d["job_id"] == job_id])
    [mission] = [m for m in changes["missions"] if job_id in m["job_ids"]]
    assert mission["project_id"]


def test_ten_seconds_after_the_seed_nothing_is_listed(root, tmp_path):
    _seed_project_job_and_decision(tmp_path)
    since = datetime.now(timezone.utc) + timedelta(seconds=10)

    changes = build_client_changes(since)

    assert changes["jobs"] == []
    assert changes["decisions"] == []
    assert changes["missions"] == []
    assert changes["applies"] == []


# ── the overlap boundary, by file modification time ───────────────────────


def test_the_overlap_boundary_by_file_modification_time(root):
    since = NOW
    inside, outside = (
        JobPlan(job_title=title, project_id="proj-1") for title in ("inside", "outside"))
    save_job_plan(inside)
    save_job_plan(outside)
    inside_mtime = (since - timedelta(seconds=3)).timestamp()
    outside_mtime = (since - timedelta(seconds=10)).timestamp()
    os.utime(job_record_path(str(inside.job_id)), (inside_mtime, inside_mtime))
    os.utime(job_record_path(str(outside.job_id)), (outside_mtime, outside_mtime))

    changes = build_client_changes(since, now=NOW)

    listed = {j["job_id"] for j in changes["jobs"]}
    assert str(inside.job_id) in listed
    assert str(outside.job_id) not in listed


# ── closed_decisions: a budget decision answered `abandon` ───────────────


def test_an_abandoned_decision_is_named_under_closed_decisions_with_its_resolved_at(root, tmp_path):
    before = datetime.now(timezone.utc) - timedelta(seconds=1)
    job_id = _seed_project_job_and_decision(tmp_path)
    digest = build_client_digest(job_ids=[job_id])
    [decision] = [d for d in digest["decisions"] if d["type"] == "token_budget"]

    answered = _resolve_decision(job_id, decision["decision_id"], reason="abandon")
    assert answered["ok"] is True

    changes = build_client_changes(before)

    [closed] = [c for c in changes["closed_decisions"] if c["job_id"] == job_id]
    assert closed["decision_id"] == decision["decision_id"]
    assert closed["resolved_at"]


# ── applies: a changed apply record, and one that is not JSON ────────────


def _apply_record(root: Path, job_id: str, name: str, body: str) -> None:
    record_dir = root / "job_apply_records" / job_id
    record_dir.mkdir(parents=True, exist_ok=True)
    (record_dir / name).write_text(body, encoding="utf-8")


def test_a_changed_apply_record_is_listed_and_a_non_json_one_is_skipped(root):
    since = NOW
    _apply_record(root, "job-a", "a1.json", json.dumps(
        {"job_apply_id": "a1", "status": "applied", "finished_at": "2026-01-01T11:59:58+00:00"}))
    _apply_record(root, "job-a", "bad.json", "{not json")
    changed_mtime = (since - timedelta(seconds=2)).timestamp()
    for name in ("a1.json", "bad.json"):
        path = root / "job_apply_records" / "job-a" / name
        os.utime(path, (changed_mtime, changed_mtime))

    changes = build_client_changes(since, now=NOW)

    [applied] = [a for a in changes["applies"] if a["job_apply_id"] == "a1"]
    assert applied == {
        "job_id": "job-a", "job_apply_id": "a1", "status": "applied",
        "finished_at": "2026-01-01T11:59:58+00:00",
    }
    assert changes["degraded"] is True
    assert any("bad.json" in skipped for skipped in changes["skipped_files"])

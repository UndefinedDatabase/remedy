"""F253 S3a — `remedy client changes [--since <cursor>] [--json]` (DECISION F253 D4 (3)).

Through the command line as a subprocess, on the scratch data root `tests/conftest.py`'s autouse
fixture sets (inherited by the child process through its copy of `os.environ`), the way
`tests/ui_server/test_public_api.py`'s `_seed_project_job_and_decision` seeds one. Every
subprocess's `cwd` is outside this repository, so, as every other CLI subprocess test in this
suite does (`tests/cli/test_golden_path.py`, `tests/cli/runtime_helpers.py` and others), its
`PYTHONPATH` is pinned to this repository's own root — never an unrelated `apps` package another
sys.path entry might resolve first.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

#: Git identity for the scratch repository the seed below commits into.
_SEED_GIT_IDENTITY = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
                      "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
#: A deadline already in the past: the run's budget stops it before any task runs.
_SEED_PAST_DEADLINE = "2000-01-01T00:00:00+00:00"


def _subprocess_env() -> dict[str, str]:
    """A fresh copy of `os.environ`, read at call time — never a module-level snapshot, which
    would freeze at import (collection), before `tests/conftest.py`'s autouse fixture has set
    `REMEDY_DATA_DIR` for the test in hand, and send every subprocess at this repository's own
    real `.data` (R-0803) — with `PYTHONPATH` pinned to this repository's own root, ahead of
    whatever else another sys.path entry might resolve `apps` from first.
    """
    return {**os.environ, "PYTHONPATH": str(REPO_ROOT)}


def _remedy(args: list[str], cwd: Path) -> tuple[int, str]:
    result = subprocess.run(
        [sys.executable, "-m", "apps.cli.main", *args],
        cwd=str(cwd), capture_output=True, text=True, env=_subprocess_env(), timeout=60)
    return result.returncode, result.stdout


def _seed_project_job_and_decision(tmp_path: Path) -> str:
    """Put one project, one job and one open decision on the current data root; the job id.

    Copied from `tests/ui_server/test_public_api.py`'s `_seed_project_job_and_decision`.
    """
    repo = tmp_path / "seed-repo"
    repo.mkdir()
    env = {**_subprocess_env(), **_SEED_GIT_IDENTITY}
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


def test_remedy_client_changes_json_exits_0_with_every_key_and_empty_lists(tmp_path):
    code, out = _remedy(["client", "changes", "--json"], tmp_path)

    assert code == 0, out
    body = json.loads(out)
    assert body["ok"] is True
    assert {"read_at", "cursor", "since", "overlap_seconds", "jobs", "decisions",
            "closed_decisions", "missions", "applies", "degraded", "skipped_files"} <= set(body)
    assert body["since"] is None
    assert body["jobs"] == body["decisions"] == body["closed_decisions"] == []
    assert body["missions"] == body["applies"] == []


def test_since_well_before_a_seeded_run_lists_the_seeded_job(tmp_path):
    job_id = _seed_project_job_and_decision(tmp_path)

    code, out = _remedy(
        ["client", "changes", "--since", "2000-01-01T00:00:00Z", "--json"], tmp_path)

    assert code == 0, out
    body = json.loads(out)
    assert body["ok"] is True
    assert any(job["job_id"] == job_id for job in body["jobs"])


def test_since_yesterday_exits_2_with_invalid_cursor(tmp_path):
    code, out = _remedy(["client", "changes", "--since", "yesterday", "--json"], tmp_path)

    assert code == 2, out
    body = json.loads(out)
    assert body["ok"] is False
    assert body["error"] == "invalid_cursor"


def test_without_json_it_prints_the_next_cursor_line(tmp_path):
    code, out = _remedy(["client", "changes"], tmp_path)

    assert code == 0, out
    assert any(line.startswith("Next cursor: ") for line in out.splitlines())

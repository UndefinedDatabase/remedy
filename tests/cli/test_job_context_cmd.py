"""Runtime CLI tests for `remedy job context <id> --task <tid>` (F107 T004 part 2a).

Every case runs against a REAL fixture repo on disk and a REAL persisted Job,
through the same grouped-CLI entry point a user types. Assertions are on real
values — tier numbers, renderings, token counts, exit codes — never on
truthiness, because a truthy assertion cannot tell a correct tier from any
other tier.
"""

from __future__ import annotations

import json
from uuid import uuid4

import pytest

from apps.cli.commands.job_context_cmd import list_repo_candidate_paths
from packages.orchestration.token_economy import estimate_text_tokens
from tests.cli.runtime_helpers import run_grouped_cli

#: The fenced file: it imports its direct neighbor, which imports one file
#: further out, and a fourth file nothing imports at all. That shape is exactly
#: the four F107 tiers on four files.
ALPHA_PY = '''"""The fenced module — the task's declared write scope."""
import beta


def run_alpha(value: int) -> int:
    return beta.double(value)
'''

BETA_PY = '''"""Direct import neighbor of alpha (tier 2)."""
import gamma


def double(value: int) -> int:
    return gamma.scale(value, 2)
'''

GAMMA_PY = '''"""One hop past the neighbor (tier 3)."""


def scale(value: int, factor: int) -> int:
    return value * factor
'''

UNRELATED_PY = '''"""Nothing imports this file (tier 4)."""


def unrelated_helper() -> str:
    return "unrelated"
'''


@pytest.fixture()
def env(tmp_path, monkeypatch):
    """Isolated data root plus a git ceiling.

    The fixture repo is deliberately NOT a git checkout, so the candidate
    listing must come from the documented rglob fallback. The ceiling pins
    that: without it, a tmp_path that happened to live inside some checkout
    would silently take the `git ls-files` branch and list other files.
    """
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))
    return data_dir


def _make_repo(tmp_path):
    """A four-file fixture repo carrying a `.git` directory that is not a checkout."""
    repo = tmp_path / "repo"
    (repo / ".git").mkdir(parents=True)
    (repo / ".git" / "config").write_text("[core]\n")
    (repo / "alpha.py").write_text(ALPHA_PY)
    (repo / "beta.py").write_text(BETA_PY)
    (repo / "gamma.py").write_text(GAMMA_PY)
    (repo / "unrelated.py").write_text(UNRELATED_PY)
    return repo


def _make_job(data_dir, repo, *, files_hint=("alpha.py",), attach_repo=True):
    """Persist a real Job whose single task carries a real flight-plan block."""
    from packages.core.models import Job, Task
    from packages.orchestration.storage import save_job

    task = Task(
        description="edit alpha",
        inputs={"flight": {"planned_id": "T001", "files_hint": list(files_hint)}},
    )
    metadata = {"target_repo": str(repo)} if attach_repo else {}
    job = Job(id=uuid4(), name="f107-context", tasks=[task], metadata=metadata)
    save_job(job, root=data_dir)
    return job, task


def _entry(entries, path):
    """The single entry for `path`, asserting it appears exactly once."""
    hits = [e for e in entries if e["path"] == path]
    assert len(hits) == 1, f"expected exactly 1 entry for {path}, got {hits}"
    return hits[0]


def _run_json(env, job_id, *extra):
    r = run_grouped_cli(["job", "context", job_id, *extra, "--json"], env)
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


def test_fenced_file_is_tier_one_and_rendered_full(tmp_path, env):
    repo = _make_repo(tmp_path)
    job, _task = _make_job(env, repo)
    data = _run_json(env, str(job.id), "--task", "T001")

    alpha = _entry(data["included"], "alpha.py")
    assert alpha["tier"] == 1
    assert alpha["rendering"] == "full"
    assert alpha["estimated_tokens"] == estimate_text_tokens(ALPHA_PY)
    assert data["fenced_paths"] == ["alpha.py"]
    assert data["candidate_count"] == 4
    assert data["candidate_source"] == "filesystem walk"


def test_direct_import_neighbor_appears_at_tier_two(tmp_path, env):
    repo = _make_repo(tmp_path)
    job, _task = _make_job(env, repo)
    data = _run_json(env, str(job.id), "--task", "T001")

    beta = _entry(data["included"], "beta.py")
    assert beta["tier"] == 2
    assert beta["rendering"] == "full"
    assert beta["estimated_tokens"] == estimate_text_tokens(BETA_PY)
    # Tier 3 is present too, and by its own rendering rather than a demotion.
    gamma = _entry(data["included"], "gamma.py")
    assert gamma["tier"] == 3
    assert gamma["rendering"] == "signatures"


def test_unrelated_module_is_omitted_for_distance(tmp_path, env):
    repo = _make_repo(tmp_path)
    job, _task = _make_job(env, repo)
    data = _run_json(env, str(job.id), "--task", "T001")

    omitted = _entry(data["omissions"], "unrelated.py")
    assert omitted["reason"] == "distance"
    assert omitted["tier"] == 4
    assert omitted["outcome"] == "omitted"
    assert [e["path"] for e in data["omissions"]] == ["unrelated.py"]


def test_json_view_carries_the_same_paths_as_the_text_view(tmp_path, env):
    repo = _make_repo(tmp_path)
    job, _task = _make_job(env, repo)
    data = _run_json(env, str(job.id), "--task", "T001")

    text = run_grouped_cli(["job", "context", str(job.id), "--task", "T001"], env)
    assert text.returncode == 0, text.stderr
    text_paths = {
        token
        for line in text.stdout.splitlines()
        for token in line.split()
        if token.endswith(".py")
    }
    json_paths = {e["path"] for e in data["included"]}
    json_paths |= {e["path"] for e in data["omissions"]}
    assert text_paths == json_paths
    assert text_paths == {"alpha.py", "beta.py", "gamma.py", "unrelated.py"}


def test_planned_id_and_task_uuid_prefix_reach_the_same_task(tmp_path, env):
    repo = _make_repo(tmp_path)
    job, task = _make_job(env, repo)

    by_planned = _run_json(env, str(job.id), "--task", "T001")
    by_prefix = _run_json(env, str(job.id), "--task", str(task.id)[:8])
    assert by_planned["task_id"] == str(task.id)
    assert by_prefix["task_id"] == str(task.id)
    assert by_prefix["included"] == by_planned["included"]
    assert by_prefix["omissions"] == by_planned["omissions"]


def test_unknown_task_exits_three_and_names_nothing_it_did_not_find(tmp_path, env):
    repo = _make_repo(tmp_path)
    job, task = _make_job(env, repo)

    r = run_grouped_cli(["job", "context", str(job.id), "--task", "T999"], env)
    assert r.returncode == 3
    assert "T999" in r.stderr
    assert "T001" not in r.stderr
    assert str(task.id) not in r.stderr
    assert "Traceback" not in r.stderr


def test_job_without_target_repo_exits_two(tmp_path, env):
    repo = _make_repo(tmp_path)
    job, _task = _make_job(env, repo, attach_repo=False)

    r = run_grouped_cli(["job", "context", str(job.id), "--task", "T001"], env)
    assert r.returncode == 2
    assert "target_repo" in r.stderr
    assert "Traceback" not in r.stderr


def test_candidate_listing_excludes_dot_git_and_is_sorted(tmp_path, env):
    repo = _make_repo(tmp_path)
    assert list_repo_candidate_paths(repo) == [
        "alpha.py",
        "beta.py",
        "gamma.py",
        "unrelated.py",
    ]


def test_empty_files_hint_is_rendered_rather_than_treated_as_an_error(tmp_path, env):
    repo = _make_repo(tmp_path)
    job, _task = _make_job(env, repo, files_hint=())

    r = run_grouped_cli(["job", "context", str(job.id), "--task", "T001"], env)
    assert r.returncode == 0, r.stderr
    assert "Fenced paths (0)" in r.stdout
    data = _run_json(env, str(job.id), "--task", "T001")
    assert data["fenced_paths"] == []
    assert data["included"] == []
    assert data["estimated_tokens"] == 0
    assert sorted(e["path"] for e in data["omissions"]) == [
        "alpha.py",
        "beta.py",
        "gamma.py",
        "unrelated.py",
    ]

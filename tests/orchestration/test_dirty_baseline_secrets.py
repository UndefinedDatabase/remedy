"""A dirty sensitive or unrelated file never enters the job workspace or a Git object (amend1014c, R1).

Real git repositories and the real `run_job` with a fake builder. The dummy marker is fixed and
only booleans are asserted, so a failure message never prints it.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from packages.orchestration import dirty_baseline as DB
from packages.orchestration import worktrees as W
from packages.orchestration.dirty_baseline import job_start_baseline
from packages.orchestration.job_apply import apply_job, summarize_job_apply
from packages.orchestration.pingpong_job import JOB_COMPLETED
from tests.orchestration.test_dirty_baseline import _DIRTY, _run, dirty_repo  # noqa: F401 (fixture)
from tests.orchestration.test_job_apply_history import _state, data_root  # noqa: F401 (autouse)
from tests.orchestration.test_job_worktree_integration import _git, repo  # noqa: F401 (fixture)

MARKER = b"DUMMY-MARKER-0f3a9c-not-a-real-secret"


def _marker_in_any_git_object(repo: Path) -> bool:
    """True when any object in the repository's database, reachable or not, holds the marker."""
    listing = subprocess.run(["git", "cat-file", "--batch-all-objects", "--batch"], cwd=repo,
                             capture_output=True, check=True).stdout
    return MARKER in listing


def _bytes_of(path: Path) -> bytes:
    return path.read_bytes()


@pytest.mark.parametrize("name", [".env", ".env.local", "deploy.pem", "id.key", "credentials.json"])
def test_an_untracked_sensitive_file_never_reaches_the_workspace_or_a_git_object(dirty_repo, monkeypatch, name):
    secret = dirty_repo / name
    secret.write_bytes(MARKER + b"\n")
    before = (_bytes_of(secret), _git(dirty_repo, "status", "--porcelain", "--", name))
    seen: dict = {}

    job = _run(dirty_repo, monkeypatch, seen)

    assert job.state == JOB_COMPLETED, job.error
    assert name not in seen["tree"]                                       # not in the workspace
    assert not _marker_in_any_git_object(dirty_repo)                      # not in any object, any branch
    assert (_bytes_of(secret), _git(dirty_repo, "status", "--porcelain", "--", name)) == before
    start = job_start_baseline(job)
    assert name not in [e["path"] for e in start["entries"]]
    assert {"path": name, "category": DB.sensitive_path_category(name)} in start["preserved"]
    assert MARKER.decode() not in str(start)


def test_a_dirty_unrelated_file_is_not_copied_stays_uncommitted_and_is_named_without_content(dirty_repo, monkeypatch):
    seen: dict = {}
    job = _run(dirty_repo, monkeypatch, seen)
    assert seen["saw_notes"] == "notes\n"                                  # HEAD's bytes, not the dirty ones
    assert "edited by hand" not in str(job_start_baseline(job))

    result = apply_job(job.job_id, str(dirty_repo), approve=True, commit_auto=True)

    assert result.status == "applied" and result.commit_sha, result.blocked_reason
    assert (dirty_repo / "notes.txt").read_text() == "notes, edited by hand\n"
    assert _git(dirty_repo, "status", "--porcelain").split() == ["M", "notes.txt"]
    assert _git(dirty_repo, "show", "--name-only", "--format=", "HEAD").split() == ["README.md"]
    assert result.preserved_dirty_paths == ["notes.txt"]
    assert "notes.txt" in summarize_job_apply(result) and "edited by hand" not in summarize_job_apply(result)


def test_an_untracked_unrelated_file_is_absent_from_the_workspace(dirty_repo, monkeypatch):
    (dirty_repo / "scratch.txt").write_text("a private note\n")
    seen: dict = {}
    job = _run(dirty_repo, monkeypatch, seen)
    assert "scratch.txt" not in seen["tree"]
    assert (dirty_repo / "scratch.txt").read_text() == "a private note\n"
    assert any(p["path"] == "scratch.txt" for p in job_start_baseline(job)["preserved"])


def test_a_dirty_deliverable_is_seeded_byte_exactly_and_the_diff_is_only_the_builders_delta(dirty_repo, monkeypatch):
    from packages.orchestration.job_evidence import job_result_diff_source

    seen: dict = {}
    job = _run(dirty_repo, monkeypatch, seen)
    assert seen["saw"] == _DIRTY
    diff = job_result_diff_source(job)[0].read_text()
    added = [ln for ln in diff.splitlines() if ln.startswith("+") and not ln.startswith("+++")]
    assert added == ["+The job's reviewed paragraph."]


@pytest.mark.parametrize("target", [".env", "keys/server.pem"])
def test_an_order_targeting_a_sensitive_path_is_refused_before_a_worktree_or_a_provider_call(repo, monkeypatch, target):
    from packages.orchestration.pingpong_job import parse_job_file, run_job

    (repo / "README.md").write_text("# Base\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "readme")
    calls: list[str] = []
    created: list[str] = []
    monkeypatch.setattr(W, "create", lambda *a, **k: created.append("worktree"))

    class _Builder:
        def build(self, *a, **k):
            calls.append("build")

        review = build

    job = parse_job_file(f"# Edit\n\n## Task 1 — change {target}\n\nFiles:\n- {target}\n", str(repo))
    done = run_job(job.job_id, builder_provider=_Builder(), reviewer_provider=_Builder(),
                   builder_name="fake", reviewer_name="fake", max_rounds=1)

    assert not calls and not created
    assert done.state != JOB_COMPLETED and target in done.error
    assert MARKER.decode() not in done.error


def test_the_order_guard_refuses_a_sensitive_target_by_name_alone():
    from packages.orchestration.do_role_guards import sensitive_order_refusal

    assert "an environment file" in sensitive_order_refusal("Add a variable to .env")
    assert "private key" in sensitive_order_refusal("Rotate certs/server.pem")
    assert sensitive_order_refusal("Add a paragraph to README.md") == ""


def test_a_git_ignored_sensitive_file_stays_ignored_and_untouched_and_the_guard_does_not_need_ignore(dirty_repo, monkeypatch):
    (dirty_repo / ".gitignore").write_text("*.local\n")
    _git(dirty_repo, "add", ".gitignore")
    _git(dirty_repo, "commit", "-qm", "ignore")
    ignored = dirty_repo / "ignored.local"
    ignored.write_bytes(MARKER)
    seen: dict = {}
    job = _run(dirty_repo, monkeypatch, seen)
    assert job.state == JOB_COMPLETED and "ignored.local" not in seen["tree"]
    assert _bytes_of(ignored) == MARKER and not _marker_in_any_git_object(dirty_repo)
    # the classifier is by name: an UNignored copy of the same shape is refused too, with no .gitignore help
    assert DB.sensitive_path_category(".env") and DB.sensitive_path_category("a/b/.env.production")
    assert not DB.sensitive_path_category("README.md")


def test_representability_refusals_stay_by_path_and_never_open_a_sensitive_file(repo, monkeypatch):
    (repo / "base.txt").write_text("x\n")
    (repo / ".env").write_bytes(MARKER)
    opened: list[str] = []
    real = Path.read_bytes
    monkeypatch.setattr(Path, "read_bytes", lambda self: (opened.append(self.name), real(self))[1])

    baseline = DB.capture_dirty_baseline(repo, ["base.txt", ".env"])

    assert ".env" not in opened and [e.path for e in baseline.entries] == ["base.txt"]
    assert (".env", "an environment file") in baseline.preserved
    with pytest.raises(DB.DirtyBaselineUnsupported, match="not a path|outside"):
        DB.seed_workspace_from_baseline(DB.DirtyBaseline("h", "b", (DB.BaselineEntry("../x", "file", "s"),), "d"), repo)


def test_an_http_route_in_an_order_is_no_host_path_but_a_host_path_still_is():
    from packages.orchestration.do_role_guards import sensitive_order_refusal

    assert sensitive_order_refusal("Add a GET /health endpoint to src/api.py") == ""
    assert sensitive_order_refusal("Serve /api/v2/users from src/routes.py") == ""
    assert "outside the repository" in sensitive_order_refusal("Copy /etc/passwd into docs")
    assert "outside the repository" in sensitive_order_refusal("Read /home/someone/notes")
    assert "outside the repository" in sensitive_order_refusal("Write to /tmp/out.txt")
    assert "outside the repository" in sensitive_order_refusal("Open ../secrets/notes")

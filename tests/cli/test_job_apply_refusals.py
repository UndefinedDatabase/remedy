"""F304 T003 — an approved apply that did not land is refused with one token per cause.

`remedy job apply <job> --approve --json` answers `"ok": false` with a fixed `error` token whenever
the apply did not land, still carries every key of the apply's answer, and exits 1, or 3 when the
job is absent or not ready to apply; flags that clash exit 2 before the job is read. A preview,
without `--approve` or with `--dry-run`, answers `"ok": true` and exits 0 (DECISION F304 D4).

In-process through `apps.cli.grouped.main`, with the real `run_job` and fake providers, the way
`tests/orchestration/test_job_apply_commit.py` drives them, and the data root under `tmp_path`.
"""
from __future__ import annotations

import json

import pytest

from apps.cli.client_interface import OPERATION_REFUSAL_TOKENS
from apps.cli.grouped import main
from packages.orchestration.job_apply import (
    APPLY_REFUSAL_TOKENS,
    COMMIT_REFUSED,
    CONTRACT_UNMET_OPENING,
    CONTRACT_UNREADABLE_OPENING,
    DETACHED_HEAD_OPENING,
    DIRTY_TREE_OPENING,
    HISTORY_REFUSED,
    LOCAL_UPSTREAM_WORDS,
    NO_UPSTREAM_WORDS,
    PUSH_REFUSED,
    JobApplyResult,
    apply_refusal,
)
from tests.orchestration.test_job_apply import _make_partially_blocked_job
from tests.orchestration.test_job_apply_commit import _bare_upstream, _mission
from tests.orchestration.test_job_apply_history import (  # noqa: F401  (autouse fixture)
    _completed,
    _one_task_job,
    _operator_commit,
    _state,
    data_root,
)
from tests.orchestration.test_job_worktree_integration import (  # noqa: F401  (fixture)
    _git,
    repo,
)


def _refused(capsys, *argv: str, code: int = 1) -> dict:
    """The answer of `remedy job apply <argv> --json`, which must exit `code` with a declared token."""
    with pytest.raises(SystemExit) as exc:
        main(["job", "apply", *argv, "--json"])
    assert exc.value.code == code
    data = json.loads(capsys.readouterr().out)
    assert data["ok"] is False and data["error"] in OPERATION_REFUSAL_TOKENS["job.apply"], data
    return data


def _approve(job, repo, *flags: str) -> tuple[str, ...]:
    return (job.job_id, "--repo", str(repo), "--approve", *flags)


# The six causes T003 names, each through the command line.

def test_a_dirty_tree_is_target_dirty_and_changes_nothing(repo, monkeypatch, capsys):
    job = _completed(repo, monkeypatch)
    (repo / "scratch.txt").write_text("wip\n")
    before = _state(repo)

    data = _refused(capsys, *_approve(job, repo, "--commit", "Add the page"))

    assert data["error"] == "target_dirty"
    assert "uncommitted changes in scratch.txt" in data["message"]
    assert (data["status"], data["files_applied"], data["commit_sha"]) == ("blocked", [], "")
    assert _state(repo) == before


def test_a_detached_head_is_target_detached_head(repo, monkeypatch, capsys):
    job = _completed(repo, monkeypatch)
    _git(repo, "checkout", "-q", "--detach")

    data = _refused(capsys, *_approve(job, repo, "--commit-auto"))

    assert data["error"] == "target_detached_head"
    assert not (repo / "one.txt").exists()


def test_a_branch_without_an_upstream_is_push_no_upstream(repo, monkeypatch, capsys):
    job = _completed(repo, monkeypatch)

    data = _refused(capsys, *_approve(job, repo, "--commit", "Add the page", "--push"))

    assert data["error"] == "push_no_upstream"
    assert data["pushed"] is False and not (repo / "one.txt").exists()


def test_an_unmet_blocking_criterion_is_push_refused_by_contract(repo, monkeypatch, capsys,
                                                                 tmp_path):
    _bare_upstream(repo, tmp_path)
    job = _completed(repo, monkeypatch)
    _mission(monkeypatch, statuses={"C001": ("unmet", True)})

    data = _refused(capsys, *_approve(job, repo, "--commit-auto", "--push"))

    assert data["error"] == "push_refused_by_contract"
    assert "C001" in data["message"]
    assert data["pushed"] is False and not (repo / "one.txt").exists()


def test_a_merge_that_conflicts_is_merge_conflict(repo, monkeypatch, capsys):
    job = _one_task_job(repo, monkeypatch, "pkg/mod.txt")
    _operator_commit(repo, "pkg", "a file where the job makes a directory\n", "Add pkg as a file")
    before = _state(repo)

    data = _refused(capsys, *_approve(job, repo, "--commit-with-history"))

    assert data["error"] == "merge_conflict"
    assert data["merge_conflicts"] and data["merge_commit"] == ""
    assert _state(repo) == before


def test_a_protected_path_is_blocked_paths(tmp_path, capsys):
    job, _workspace, target = _make_partially_blocked_job(tmp_path)

    data = _refused(capsys, *_approve(job, target))

    assert data["error"] == "blocked_paths"
    assert data["files_blocked"] and data["files_applied"] == []


# The rest of the rule.

def test_a_job_that_does_not_exist_exits_3(tmp_path, capsys):
    data = _refused(capsys, "0123456789abcdef", "--repo", str(tmp_path), "--approve", code=3)

    assert data["error"] == "job_not_found"


def test_flags_that_clash_exit_2_before_the_job_is_read(capsys):
    data = _refused(capsys, "0123456789abcdef", "--approve", "--commit", "Add the page",
                    "--commit-auto", code=2)

    assert data["error"] == "invalid_argument"
    assert "only one of them may be given" in data["message"]


@pytest.mark.parametrize("preview", [(), ("--approve", "--dry-run")])
def test_a_preview_that_meets_a_refusal_still_exits_0(repo, monkeypatch, capsys, preview):
    job = _completed(repo, monkeypatch)
    (repo / "scratch.txt").write_text("wip\n")

    main(["job", "apply", job.job_id, "--repo", str(repo), *preview, "--commit", "Add the page",
          "--json"])

    data = json.loads(capsys.readouterr().out)
    assert (data["ok"], data["status"]) == (True, "dry_run")
    assert any("uncommitted changes in scratch.txt" in reason for reason in data["blocked_reasons"])


def test_the_text_answer_prints_the_summary_and_exits_1(repo, monkeypatch, capsys):
    job = _completed(repo, monkeypatch)
    (repo / "scratch.txt").write_text("wip\n")

    with pytest.raises(SystemExit) as exc:
        main(["job", "apply", *_approve(job, repo, "--commit", "Add the page")])

    assert exc.value.code == 1
    out, err = capsys.readouterr()
    assert f"BLOCKED: {COMMIT_REFUSED}: {DIRTY_TREE_OPENING} in scratch.txt" in out
    assert err.startswith(f"Error: {COMMIT_REFUSED}: {DIRTY_TREE_OPENING}")


# Every token the rule declares, read from the result an apply returns.

_CAUSES = [
    ("job_not_found", {"blocked_reason": "job_not_found: 0123456789abcdef"}),
    ("job_not_ready", {"blocked_reason": "job_not_completed: status=stopped"}),
    ("job_not_ready", {"blocked_reason": "reviewer_not_pass: T001 verdict=fail"}),
    ("job_not_ready", {"blocked_reason": "no_files_in_apply_manifests"}),
    ("blocked_paths", {"blocked_reason": "blocked_paths: ['.env: secret_file']",
                       "files_blocked": [".env: secret_file"]}),
    ("blocked_paths", {"blocked_reason": "no_files_to_apply",
                       "files_blocked": [".env: secret_file"]}),
    ("apply_failed", {"blocked_reason": "no_files_to_apply"}),
    ("target_changed", {"blocked_reason": "baseline_check_failed: ['a.txt: target_changed_since_job']"}),
    ("target_changed", {"blocked_reason": "baseline_check_before_apply_failed: ['a.txt']"}),
    ("target_dirty", {"blocked_reason": f"{COMMIT_REFUSED}: {DIRTY_TREE_OPENING} in a.txt; "
                                        f"commit or stash them and re-run."}),
    ("target_detached_head", {"blocked_reason": f"{HISTORY_REFUSED}: {DETACHED_HEAD_OPENING}; "
                                                f"check out the branch and re-run."}),
    ("merge_conflict", {"blocked_reason": f"{HISTORY_REFUSED}: Merging the job branch conflicts "
                                          f"in pkg, so the merge was aborted.",
                        "merge_conflicts": ["pkg"]}),
    ("push_no_upstream", {"blocked_reason": f"{PUSH_REFUSED}: The branch main {NO_UPSTREAM_WORDS}; "
                                            f"set one."}),
    ("push_no_upstream", {"blocked_reason": f"{PUSH_REFUSED}: The upstream of main is the local "
                                            f"branch refs/heads/b, and {LOCAL_UPSTREAM_WORDS}."}),
    ("push_refused_by_contract", {"blocked_reason": f"{PUSH_REFUSED}: {CONTRACT_UNMET_OPENING} "
                                                    f"C001 are unmet, so nothing is pushed."}),
    ("push_refused_by_contract", {"blocked_reason": f"{PUSH_REFUSED}: {CONTRACT_UNREADABLE_OPENING} "
                                                    f"(OSError: gone), so no push can be shown safe."}),
    ("commit_refused", {"blocked_reason": f"{COMMIT_REFUSED}: The target's .gitignore matches "
                                          f"two.txt, so a commit cannot hold it."}),
    ("history_merge_refused", {"blocked_reason": f"{HISTORY_REFUSED}: Job j ran in a staging "
                                                 f"copy, not on a git branch."}),
    ("push_refused", {"blocked_reason": f"{PUSH_REFUSED}: --push pushes what a commit flag lands, "
                                        f"so it is refused alone."}),
    ("apply_failed", {"blocked_reason": "write_failed: a.txt: No space left on device"}),
    ("post_test_failed", {"status": "applied_test_failed", "post_test_summary": "exit=1"}),
    ("push_failed", {"status": "applied_push_failed",
                     "blocked_reasons": ["The push of abc failed (frozen)."]}),
    ("apply_failed", {"status": "applied_cleanup_failed"}),
]


@pytest.mark.parametrize(("token", "fields"), _CAUSES)
def test_each_cause_reads_as_its_token(token, fields):
    result = JobApplyResult(approved=True, **{"status": "blocked", **fields})

    error, message = apply_refusal(result)

    assert (error, bool(message)) == (token, True)


def test_the_causes_reach_every_declared_token_and_no_other():
    assert sorted({token for token, _fields in _CAUSES}) == list(APPLY_REFUSAL_TOKENS)


@pytest.mark.parametrize("fields", [{"approved": False, "status": "blocked"},
                                    {"approved": True, "dry_run": True, "status": "blocked"},
                                    {"approved": True, "status": "applied"}])
def test_a_preview_and_a_landed_apply_are_no_refusal(fields):
    assert apply_refusal(JobApplyResult(blocked_reason="blocked_paths: x", **fields)) is None

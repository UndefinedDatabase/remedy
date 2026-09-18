"""F270 T004, the `do` half — `remedy do` takes `--commit "<message>"`, `--commit-auto`,
`--commit-with-history` and `--push`, chains its jobs under a commit flag and pushes
once per mission (DECISION F270 D4).

In-process through `apps.cli.grouped.main`, on test_do_sequence_cli.py's own `repo`
fixture, fake builder and reviewer and model-call tripwire. Every remote is a bare
repository under `tmp_path` whose update hook logs each ref update, so a push is
counted, never guessed; no test reaches a network or a real provider.
"""
from __future__ import annotations

import dataclasses
import json
import subprocess
from pathlib import Path

import pytest

from apps.cli.grouped import main
from tests.cli.test_do_sequence_cli import (  # noqa: F401 — fixtures used by name
    ORDER,
    _git,
    _step,
    no_model_call,
    repo,
)

MESSAGE = "Add the contact page"


def _run(capsys, *extra: str) -> tuple[int, dict | None, str]:
    """``(exit code, the --json object or None, stderr)`` of one `remedy do`."""
    code = 0
    try:
        main(["do", ORDER, "--no-llm", "--no-ui", "--json",
              "--builder-provider", "fake", "--reviewer-provider", "fake", *extra])
    except SystemExit as exc:
        code = exc.code
    captured = capsys.readouterr()
    return code, (json.loads(captured.out) if captured.out.strip() else None), captured.err


def _head(repo: Path) -> str:
    return _git(repo, "rev-parse", "HEAD").strip()


def _branch(repo: Path) -> str:
    return _git(repo, "symbolic-ref", "--short", "HEAD").strip()


def _clean(repo: Path) -> bool:
    return _git(repo, "status", "--porcelain", "--untracked-files=all") == ""


def _bare_upstream(repo: Path) -> Path:
    """A bare remote under tmp_path, the branch's upstream; its update hook logs each ref update."""
    remote = repo.parent / "remote.git"
    subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True,
                   capture_output=True, timeout=60)
    _git(remote, "config", "receive.denyNonFastForwards", "true")
    log = repo.parent / "pushes.log"
    hook = remote / "hooks" / "update"
    hook.write_text(f'#!/bin/sh\necho "$1 $2 $3" >> {log}\n')
    hook.chmod(0o755)
    _git(repo, "remote", "add", "origin", str(remote))
    _git(repo, "push", "-q", "-u", "origin", _branch(repo))
    log.unlink()
    return remote


def _pushes(repo: Path) -> list[str]:
    log = repo.parent / "pushes.log"
    return log.read_text().splitlines() if log.exists() else []


def _nothing_ran(repo: Path) -> bool:
    """No data file, no project and no job: the walk's first step never ran."""
    from packages.orchestration.pingpong_job import list_job_plans
    from packages.orchestration.project_registry import resolve_project

    data_root = repo.parent / "data"
    return ([p for p in data_root.rglob("*") if p.is_file()] == []
            and resolve_project(repo) is None and list_job_plans() == [])


def _before_the_apply_step_mark(monkeypatch, status: str) -> list[str]:
    """Right before the apply step, set the mission's FIRST blocking criterion to ``status``.

    Through the contract's own writer. Returns the list the marked id is put in.
    """
    from packages.orchestration import do_sequence
    from packages.orchestration.mission_contract import (
        read_mission_contract,
        write_mission_contract,
    )
    from packages.orchestration.mission_state import load_mission

    real_apply = do_sequence.DO_STEP_TABLE["apply"]
    marked: list[str] = []

    def apply_after_marking(ctx):
        project_id = str(ctx.project.id)
        contract = read_mission_contract(load_mission(project_id, ctx.mission_id))
        first = next(c for c in contract.criteria if c.blocking)
        marked.append(first.id)
        write_mission_contract(project_id, ctx.mission_id, dataclasses.replace(
            contract, criteria=tuple(dataclasses.replace(c, status=status) if c is first else c
                                     for c in contract.criteria)))
        return real_apply(ctx)

    monkeypatch.setitem(do_sequence.DO_STEP_TABLE, "apply", apply_after_marking)
    return marked


# ── The commit flags: one commit, or one merge, on the operator's branch ──


def test_commit_lands_one_commit_with_that_first_line_and_the_trailers(repo, capsys):
    head, branch = _head(repo), _branch(repo)

    code, data, _err = _run(capsys, "--commit", MESSAGE)

    assert code == 0, data and _step(data, "apply")
    [job_id] = data["job_ids"]
    landed = _head(repo)
    assert _git(repo, "rev-list", f"{head}..{landed}").split() == [landed]
    assert _git(repo, "rev-parse", f"{landed}^").strip() == head
    assert _git(repo, "log", "-1", "--format=%s").strip() == MESSAGE
    trailers = _git(repo, "log", "-1", "--format=%(trailers:only,unfold)").splitlines()
    assert f"Remedy-Job: {job_id}" in trailers
    assert "Co-authored-by: Remedy <remedy@local>" in trailers
    assert _git(repo, "log", "-1", "--format=%an <%ae>").strip() == "T <t@e.com>"
    assert data["landed"] == [{"job_id": job_id, "sha": landed, "branch": branch}]
    assert data["stopped_before_apply"] is False and data["push"] is None
    assert _clean(repo)


def test_commit_auto_lands_one_commit_whose_first_line_passes_the_rule(repo, capsys):
    from packages.orchestration.job_apply import commit_subject_problem

    head = _head(repo)

    code, data, _err = _run(capsys, "--commit-auto")

    assert code == 0, data and _step(data, "apply")
    assert _git(repo, "rev-list", "--count", f"{head}..HEAD").strip() == "1"
    subject = _git(repo, "log", "-1", "--format=%s").strip()
    assert commit_subject_problem(subject) == "", subject
    assert [entry["sha"] for entry in data["landed"]] == [_head(repo)]


def test_commit_with_history_lands_a_merge_commit(repo, capsys):
    head = _head(repo)

    code, data, _err = _run(capsys, "--commit-with-history")

    assert code == 0, data and _step(data, "apply")
    merge = _head(repo)
    parents = _git(repo, "rev-list", "--parents", "-n", "1", merge).split()[1:]
    assert len(parents) == 2 and parents[0] == head
    assert _git(repo, "log", "-1", "--format=%s").startswith("Merge the ")
    assert [entry["sha"] for entry in data["landed"]] == [merge]


# ── Refused before any step: exit 2, "Nothing was run.", nothing written ──


@pytest.mark.parametrize(("flags", "sentence"), [
    (("--push",), "--push pushes what --commit, --commit-auto or --commit-with-history "
                  "lands, so it is refused alone"),
    (("--commit", MESSAGE, "--commit-auto"), "only one of them may be given"),
    (("--commit-auto", "--commit-with-history"), "only one of them may be given"),
    (("--commit", MESSAGE, "--plan-only"), "--plan-only runs no job, so --commit would"),
    (("--commit-auto", "--push", "--plan-only"),
     "--plan-only runs no job, so --commit-auto and --push would"),
    (("--commit", "Add the page\nand more"), "--commit takes one line"),
], ids=["lone-push", "commit-and-auto", "auto-and-history", "commit-plan-only",
        "auto-push-plan-only", "two-line-message"])
def test_a_flag_rule_is_refused_before_any_step(repo, capsys, flags, sentence):
    head = _head(repo)

    code, data, err = _run(capsys, *flags)

    assert code == 2 and data is None
    assert sentence in err and "Nothing was run." in err
    assert _nothing_ran(repo) and _head(repo) == head and _clean(repo)


def test_a_dirty_tree_is_refused_before_any_step(repo, capsys):
    (repo / "notes.txt").write_text("the operator's own work\n")

    code, data, err = _run(capsys, "--commit", MESSAGE)

    assert code == 2 and data is None
    assert "uncommitted changes in notes.txt" in err and "Nothing was run." in err
    assert _nothing_ran(repo)
    assert (repo / "notes.txt").read_text() == "the operator's own work\n"


def test_push_with_no_upstream_is_refused_before_any_step(repo, capsys):
    remote = repo.parent / "remote.git"
    subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True,
                   capture_output=True, timeout=60)
    _git(repo, "remote", "add", "origin", str(remote))
    head = _head(repo)

    code, data, err = _run(capsys, "--commit", MESSAGE, "--push")

    assert code == 2 and data is None
    assert (f"has no upstream to push to; `git push --set-upstream origin {_branch(repo)}` "
            f"sets one.") in err
    assert _nothing_ran(repo) and _head(repo) == head
    assert _git(remote, "for-each-ref") == ""


# ── One push per mission ──


def test_push_sends_exactly_one_fast_forward_push_to_the_upstream(repo, capsys):
    remote = _bare_upstream(repo)
    branch = _branch(repo)
    before = _git(remote, "rev-parse", branch).strip()

    code, data, _err = _run(capsys, "--commit", MESSAGE, "--push")

    assert code == 0, data and _step(data, "apply")
    landed = _head(repo)
    assert _pushes(repo) == [f"refs/heads/{branch} {before} {landed}"]
    assert _git(repo, "rev-parse", f"{landed}^").strip() == before       # a fast-forward
    assert _git(remote, "rev-parse", branch).strip() == landed
    push = data["push"]
    assert (push["pushed"], push["sha"], push["remote"], push["ref"], push["error"],
            push["source"]) == (True, landed, "origin", f"refs/heads/{branch}", "", "--push")
    assert str(remote) not in json.dumps(push)
    assert "once, never forced (--push)" in _step(data, "apply")["detail"]


def test_the_key_with_a_commit_flag_pushes_once_without_push(repo, capsys, monkeypatch):
    _bare_upstream(repo)
    monkeypatch.setenv("REMEDY_APPLY_PUSH_AFTER_MISSION", "true")

    code, data, err = _run(capsys, "--commit", MESSAGE)

    assert code == 0, data and _step(data, "apply")
    assert len(_pushes(repo)) == 1 and _pushes(repo)[0].endswith(_head(repo))
    assert data["push"]["pushed"] is True
    assert data["push"]["source"] == "apply.push_after_mission"
    from apps.cli.commands.do_cmd import DO_PUSH_KEY_WITHOUT_COMMIT
    assert DO_PUSH_KEY_WITHOUT_COMMIT not in err


def test_the_key_without_a_commit_flag_commits_and_pushes_nothing_and_says_so(
        repo, capsys, monkeypatch):
    from apps.cli.commands.do_cmd import DO_PUSH_KEY_WITHOUT_COMMIT

    _bare_upstream(repo)
    monkeypatch.setenv("REMEDY_APPLY_PUSH_AFTER_MISSION", "true")
    head = _head(repo)

    code, data, err = _run(capsys, "--apply")

    assert code == 0, data and _step(data, "apply")
    assert DO_PUSH_KEY_WITHOUT_COMMIT in err
    assert DO_PUSH_KEY_WITHOUT_COMMIT.count(". ") == 0 and DO_PUSH_KEY_WITHOUT_COMMIT.endswith(".")
    assert _head(repo) == head and _pushes(repo) == []
    assert data["landed"] == [] and data["push"] is None


@pytest.mark.parametrize("extra", [(), ("--apply",)], ids=["plain", "apply"])
@pytest.mark.parametrize("key_set", [False, True], ids=["key-unset", "key-set"])
def test_remedy_never_commits_on_the_operator_branch_without_a_commit_flag(
        repo, capsys, monkeypatch, extra, key_set):
    _bare_upstream(repo)
    if key_set:
        monkeypatch.setenv("REMEDY_APPLY_PUSH_AFTER_MISSION", "true")
    else:
        monkeypatch.delenv("REMEDY_APPLY_PUSH_AFTER_MISSION", raising=False)
    head = _head(repo)

    code, data, _err = _run(capsys, *extra)

    assert code == 0, data and data["steps"][-1]
    assert _head(repo) == head and _pushes(repo) == []
    assert data["landed"] == [] and data["push"] is None


# ── The contract: only an unmet blocking criterion holds a push (DECISION F270 D4 (6)) ──


def test_an_unmet_blocking_criterion_is_refused_before_anything_is_applied(
        repo, capsys, monkeypatch):
    _bare_upstream(repo)
    marked = _before_the_apply_step_mark(monkeypatch, "unmet")
    head = _head(repo)

    code, data, _err = _run(capsys, "--commit", MESSAGE, "--push")

    assert code == 1
    detail = _step(data, "apply")["detail"]
    assert detail.startswith("--push was refused, so nothing was applied, committed or pushed")
    assert f"criteria {marked[0]} are unmet, so nothing is pushed" in detail
    assert _head(repo) == head and _clean(repo) and _pushes(repo) == []
    assert data["landed"] == [] and data["push"]["pushed"] is False


def test_an_open_blocking_criterion_is_pushed_and_named_in_the_json(repo, capsys):
    """A `do` job serves no milestone, so the planner's criteria stay `open` (R-0977)."""
    _bare_upstream(repo)

    code, data, _err = _run(capsys, "--commit", MESSAGE, "--push")

    assert code == 0, data and _step(data, "apply")
    still_open = [c["id"] for c in data["contract"]["criteria"]
                  if c["blocking"] and c["status"] == "open"]
    assert still_open, "the fixture's mission has no open blocking criterion"
    assert data["push"]["pushed"] is True and len(_pushes(repo)) == 1
    assert data["push"]["open_blocking_criteria"] == still_open
    assert f"criteria {', '.join(still_open)} are still open" in _step(data, "apply")["detail"]


def test_a_push_the_remote_refuses_leaves_the_commit_and_fails_the_walk(repo, capsys):
    remote = _bare_upstream(repo)
    (remote / "hooks" / "update").write_text(
        "#!/bin/sh\necho the remote is frozen >&2\nexit 1\n")
    before = _git(remote, "rev-parse", _branch(repo)).strip()

    code, data, err = _run(capsys, "--commit", MESSAGE, "--push")

    assert code == 1
    detail = _step(data, "apply")["detail"]
    assert "the remote is frozen" in detail and "push it by hand" in detail
    assert _git(remote, "rev-parse", _branch(repo)).strip() == before
    assert data["landed"][0]["sha"] == _head(repo) != before
    assert data["push"]["pushed"] is False and "the remote is frozen" in data["push"]["error"]
    assert "Error: apply failed" in err


# ── A walk of several jobs chains under a commit flag ──


def test_a_two_job_walk_under_commit_lands_two_linear_commits_and_one_push(repo, capsys):
    from packages.orchestration.pingpong_job import load_job_plan

    _bare_upstream(repo)
    head = _head(repo)

    code, data, _err = _run(capsys, "--force-mission", "--commit", MESSAGE, "--push")

    assert code == 0, data and [s for s in data["steps"] if s["status"] != "done"]
    job_ids = data["job_ids"]
    assert len(job_ids) == 2 and data["waiting_job_ids"] == []
    shas = _git(repo, "rev-list", "--reverse", f"{head}..HEAD").split()
    assert len(shas) == 2 and _git(repo, "rev-list", "--merges", f"{head}..HEAD") == ""
    assert [entry["sha"] for entry in data["landed"]] == shas
    assert [entry["job_id"] for entry in data["landed"]] == job_ids
    assert [_git(repo, "log", "-1", "--format=%s", sha).strip() for sha in shas] == [
        f"{MESSAGE} (job 1 of 2)", f"{MESSAGE} (job 2 of 2)"]
    assert load_job_plan(job_ids[1]).worktree_base_commit == shas[0]
    assert len(_pushes(repo)) == 1 and _pushes(repo)[0].endswith(shas[1])


def test_a_chained_walk_under_an_unmet_criterion_lands_its_commits_and_refuses_the_push(
        repo, capsys, monkeypatch):
    _bare_upstream(repo)
    marked = _before_the_apply_step_mark(monkeypatch, "unmet")
    head = _head(repo)

    code, data, _err = _run(capsys, "--force-mission", "--commit-auto", "--push")

    assert code == 1
    detail = _step(data, "apply")["detail"]
    assert "--push was refused after the commits landed" in detail
    assert f"criteria {marked[0]} are unmet" in detail
    shas = _git(repo, "rev-list", "--reverse", f"{head}..HEAD").split()
    assert shas == [entry["sha"] for entry in data["landed"]] and len(shas) == 2
    from packages.orchestration.job_apply import commit_subject_problem
    assert [commit_subject_problem(_git(repo, "log", "-1", "--format=%s", sha).strip())
            for sha in shas] == ["", ""]
    assert _pushes(repo) == [] and data["push"]["pushed"] is False


def test_a_walk_that_stops_keeps_its_commit_and_pushes_nothing(repo, capsys, monkeypatch):
    from packages.orchestration import pingpong_job

    _bare_upstream(repo)
    real_run_job = pingpong_job.run_job
    calls: list[str] = []

    def second_job_does_not_complete(job_id, **kwargs):
        calls.append(job_id)
        if len(calls) == 2:
            return pingpong_job.load_job_plan(job_id)        # still planned: not completed
        return real_run_job(job_id, **kwargs)

    monkeypatch.setattr(pingpong_job, "run_job", second_job_does_not_complete)
    head = _head(repo)

    code, data, _err = _run(capsys, "--force-mission", "--commit", MESSAGE, "--push")

    assert code == 1
    run = _step(data, "run")
    assert run["status"] == "failed"
    [landed] = data["landed"]
    assert run["detail"].endswith(
        f"the 1 commit(s) that landed ({landed['sha'][:12]}) stay on {landed['branch']}, "
        f"and nothing was pushed")
    assert _git(repo, "rev-list", f"{head}..HEAD").split() == [landed["sha"]]
    assert _pushes(repo) == [] and data["push"] is None
    assert [s["name"] for s in data["steps"]][-1] == "run"


def test_the_apply_step_never_passes_push_to_a_job(repo, capsys, monkeypatch):
    from packages.orchestration import job_apply

    _bare_upstream(repo)
    real = job_apply.apply_job
    seen: list[dict] = []

    def recording(job_id, target_repo, **kwargs):
        seen.append(kwargs)
        return real(job_id, target_repo, **kwargs)

    monkeypatch.setattr(job_apply, "apply_job", recording)

    code, data, _err = _run(capsys, "--force-mission", "--commit", MESSAGE, "--push")

    assert code == 0, data and _step(data, "apply")
    assert len(seen) == 2 and [kwargs.get("push", False) for kwargs in seen] == [False, False]
    assert len(_pushes(repo)) == 1

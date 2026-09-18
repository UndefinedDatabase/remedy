"""F270 T004 — `remedy job apply --approve --commit "<message>" | --commit-auto [--push]`.

DECISION F270 D3. `--commit` and `--commit-auto` copy as a plain apply does,
then land ONE commit of exactly the copied files on the operator's current
branch, as the operator, with the contract line and the two trailers. `--push`
pushes what landed to the branch's configured upstream, a bare repository under
`tmp_path`, never forced. Every refusal comes before anything is written. Drives
the real `run_job` with fake providers; no provider and no network is used.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from packages.orchestration import mission_contract as MC
from packages.orchestration import mission_state as MS
from packages.orchestration.config import get_key_spec, load_config, push_after_mission_enabled
from packages.orchestration.job_apply import (
    COMMIT_REFUSED,
    PUSH_REFUSED,
    apply_job,
    commit_subject_problem,
    load_job_apply_record,
    summarize_job_apply,
)
from tests.orchestration.test_job_apply_history import (  # noqa: F401  (autouse fixture)
    _completed,
    _hook,
    _operator_commit,
    _state,
    data_root,
)
from tests.orchestration.test_job_worktree_integration import (  # noqa: F401  (fixture)
    _git,
    repo,
)

COMMIT_KEYS = ("commit_message_mode", "commit_sha", "push", "pushed", "push_remote",
               "push_ref", "push_error", "push_open_criteria")


def _branch(repo: Path) -> str:
    return _git(repo, "symbolic-ref", "--short", "HEAD").strip()


def _head(repo: Path) -> str:
    return _git(repo, "rev-parse", "HEAD").strip()


def _paragraphs(repo: Path, sha: str = "HEAD") -> list[str]:
    return _git(repo, "log", "-1", "--format=%B", sha).strip().split("\n\n")


def _trailers(repo: Path, sha: str = "HEAD") -> list[str]:
    return _git(repo, "log", "-1", "--format=%(trailers:only,unfold)", sha).split("\n")


def _touched(repo: Path, sha: str = "HEAD") -> list[str]:
    return sorted(_git(repo, "show", "--name-only", "--format=", sha).split())


def _refused(result, prefix: str, before: dict, repo: Path) -> str:
    """The refusal's one sentence, after proving nothing was written or landed."""
    assert result.status == "blocked", (result.status, result.blocked_reason)
    assert result.blocked_reason.startswith(f"{prefix}: "), result.blocked_reason
    sentence = result.blocked_reason[len(prefix) + 2:]
    assert sentence.endswith("."), sentence
    assert result.commit_sha == "" and result.files_applied == [] and not result.pushed
    assert _state(repo) == before
    return sentence


def _bare_upstream(repo: Path, tmp_path: Path) -> Path:
    """A bare remote under tmp_path, the branch's upstream; its update hook logs every ref update."""
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True,
                   capture_output=True, timeout=60)
    _git(remote, "config", "receive.denyNonFastForwards", "true")
    log = tmp_path / "pushes.log"
    hook = remote / "hooks" / "update"
    hook.write_text(f'#!/bin/sh\necho "$1 $2 $3" >> {log}\n')
    hook.chmod(0o755)
    _git(repo, "remote", "add", "origin", str(remote))
    _git(repo, "push", "-q", "-u", "origin", _branch(repo))
    log.unlink()
    return remote


def _pushes(tmp_path: Path) -> list[str]:
    log = tmp_path / "pushes.log"
    return log.read_text().splitlines() if log.exists() else []


def _mission(monkeypatch, goal: str = "", statuses: dict | None = None) -> None:
    """Put the job under a mission with this goal and, when given, a contract."""
    contract = None
    if statuses is not None:
        contract = MC.MissionContract(criteria=tuple(
            MC.ContractCriterion(id=cid, text=f"criterion {cid}", origin="planner",
                                 blocking=blocking, status=status)
            for cid, (status, blocking) in statuses.items())).to_json()
    mission = SimpleNamespace(goal=goal, contract=contract)
    monkeypatch.setattr(MS, "mission_for_job", lambda job_id, root=None: mission)


class TestCommitWithAMessage:
    def test_c1_one_commit_of_exactly_the_copied_files_as_the_operator(self, repo, monkeypatch):
        job = _completed(repo, monkeypatch)
        before = _head(repo)
        hook_log = repo / ".git" / "commit-msg-ran"
        _hook(repo, "commit-msg", f"#!/bin/sh\necho ran >> {hook_log}\n")

        result = apply_job(job.job_id, str(repo), approve=True,
                           commit_message="Add the contact page")

        assert result.status == "applied", result.blocked_reason
        head = _head(repo)
        assert result.commit_sha == head
        assert _git(repo, "rev-list", f"{before}..{head}").split() == [head]
        assert _git(repo, "log", "-1", "--format=%P", head).split() == [before]
        assert _touched(repo, head) == sorted(result.files_applied) == ["one.txt", "two.txt"]
        assert _git(repo, "status", "--porcelain", "--untracked-files=all") == ""
        assert _git(repo, "log", "-1", "--format=%an <%ae>|%cn <%ce>", head).strip() == (
            "T <t@e.com>|T <t@e.com>")
        assert hook_log.read_text() == "ran\n"          # the operator's hooks ran
        paragraphs = _paragraphs(repo, head)
        assert paragraphs[0] == "Add the contact page"
        assert job.job_id in paragraphs[1]
        assert paragraphs[-2] == "contract: none"         # the last body line
        trailers = _trailers(repo, head)
        assert f"Remedy-Job: {job.job_id}" in trailers
        assert "Co-authored-by: Remedy <remedy@local>" in trailers
        record = load_job_apply_record(job.job_id, result.job_apply_id)
        assert all(key in record for key in COMMIT_KEYS)
        assert record["commit_message_mode"] == "message" and record["commit_sha"] == head
        assert record["push"] is False and record["pushed"] is False
        summary = summarize_job_apply(result)
        assert head in summary and "Nothing was pushed." in summary
        assert "No commits or pushes were made" not in summary

    def test_c2_the_contract_line_counts_the_criteria(self, repo, monkeypatch):
        job = _completed(repo, monkeypatch)
        _mission(monkeypatch, statuses={"C001": ("met", True), "C002": ("open", False)})
        result = apply_job(job.job_id, str(repo), approve=True,
                           commit_message="Add the contact page")
        assert result.status == "applied", result.blocked_reason
        assert _paragraphs(repo)[-2] == "contract: 1 of 2 criteria green"

    def test_c3_a_refusing_hook_leaves_the_files_copied_and_out_of_the_index(
        self, repo, monkeypatch,
    ):
        job = _completed(repo, monkeypatch)
        head = _head(repo)
        _hook(repo, "pre-commit", "#!/bin/sh\necho not on this branch >&2\nexit 1\n")
        result = apply_job(job.job_id, str(repo), approve=True, commit_message="Add the page")
        assert result.status == "blocked" and result.commit_sha == ""
        assert result.blocked_reason.startswith("commit_failed: ")
        assert '"not on this branch"' in result.blocked_reason
        assert _head(repo) == head
        assert _git(repo, "diff", "--cached", "--name-only") == ""
        assert sorted(_git(repo, "status", "--porcelain").splitlines()) == [
            "?? one.txt", "?? two.txt"]

    def test_c4_a_commit_touching_a_path_remedy_did_not_copy_is_reported(
        self, repo, monkeypatch,
    ):
        job = _completed(repo, monkeypatch)
        before = _head(repo)
        _hook(repo, "pre-commit", "#!/bin/sh\necho x > extra.txt\ngit add extra.txt\n")
        result = apply_job(job.job_id, str(repo), approve=True, commit_message="Add the page")
        assert result.status == "blocked", result.blocked_reason
        assert result.blocked_reason.startswith("commit_failed: git commit reported success")
        assert "extra.txt" in result.blocked_reason
        assert result.commit_sha == _head(repo) != before     # recorded, never reset
        assert f"git reset --keep {before}" in summarize_job_apply(result)

    def test_c5_a_failed_post_test_leaves_the_files_copied_and_uncommitted(
        self, repo, monkeypatch,
    ):
        job = _completed(repo, monkeypatch)
        head = _head(repo)
        result = apply_job(job.job_id, str(repo), approve=True,
                           commit_message="Add the page", test_command="false")
        assert result.status == "applied_test_failed" and result.commit_sha == ""
        assert _head(repo) == head
        assert (repo / "one.txt").exists() and (repo / "two.txt").exists()
        assert any("made no commit" in r for r in result.blocked_reasons)
        record = load_job_apply_record(job.job_id, result.job_apply_id)
        assert record["commit_sha"] == "" and sorted(record["files_applied"]) == [
            "one.txt", "two.txt"]

    def test_c6_a_staging_job_is_committed_onto_a_git_target(self, tmp_path):
        from tests.orchestration.test_job_apply import _make_baselined_job

        job, _ws, target, rel = _make_baselined_job(tmp_path)
        for args in (("init", "-q"), ("config", "user.email", "t@e.com"),
                     ("config", "user.name", "T"), ("config", "commit.gpgsign", "false"),
                     ("add", "-A"), ("commit", "-qm", "init")):
            _git(target, *args)
        before = _head(target)
        result = apply_job(job.job_id, str(target), approve=True,
                           commit_message="Change the tracked file")
        assert result.status == "applied", result.blocked_reason
        assert _git(target, "log", "-1", "--format=%P").split() == [before]
        assert _touched(target) == [rel]
        assert _paragraphs(target)[0] == "Change the tracked file"


class TestCommitAuto:
    def test_a1_one_commit_whose_first_line_passes_the_rule(self, repo, monkeypatch):
        job = _completed(repo, monkeypatch)
        before = _head(repo)
        result = apply_job(job.job_id, str(repo), approve=True, commit_auto=True)
        assert result.status == "applied", result.blocked_reason
        head = _head(repo)
        assert _git(repo, "rev-list", f"{before}..{head}").split() == [head]
        assert _touched(repo, head) == ["one.txt", "two.txt"]
        paragraphs = _paragraphs(repo, head)
        assert commit_subject_problem(paragraphs[0]) == ""
        assert paragraphs[0] == f"Apply the 2 tasks of Remedy job {job.job_id[:8]}"
        assert f"- {job.tasks[0].title}\n- {job.tasks[1].title}" in paragraphs
        assert paragraphs[-2] == "contract: none"
        assert f"Remedy-Job: {job.job_id}" in _trailers(repo, head)
        assert result.commit_message_mode == "auto"

    def test_a2_the_missions_goal_is_the_first_line_when_it_passes_the_rule(
        self, repo, monkeypatch,
    ):
        job = _completed(repo, monkeypatch)
        _mission(monkeypatch, goal="add the contact page to the site")
        result = apply_job(job.job_id, str(repo), approve=True, commit_auto=True)
        assert result.status == "applied", result.blocked_reason
        assert _paragraphs(repo)[0] == "Add the contact page to the site"

    @pytest.mark.parametrize("line", [
        "T002",                                   # an id alone
        "task 2: T002",
        "The contact page for the site",          # no verb
        "Add " + "the contact page " * 5,         # 89 characters
        "Add " + "x" * 76,                        # 80 characters
        "Add it",                                 # two words
        "",
        "Add the\ncontact page",
    ])
    def test_a3_the_rule_rejects_an_id_a_verbless_line_and_a_long_line(self, line):
        assert commit_subject_problem(line) != ""

    def test_a5_title_first_asks_the_jobs_title_before_the_missions_goal(self, monkeypatch):
        """DECISION F270 D4 (3): `remedy do`'s walk of several jobs asks each job's title first."""
        from packages.orchestration.job_apply import build_auto_commit_subject

        _mission(monkeypatch, goal="add the contact page to the site")
        job = SimpleNamespace(job_id="0123456789abcdef", job_title="write the footer links",
                              tasks=[])
        assert build_auto_commit_subject(job) == "Add the contact page to the site"
        assert build_auto_commit_subject(job, title_first=True) == "Write the footer links"

    def test_a4_the_rule_accepts_a_short_sentence(self):
        assert commit_subject_problem("Add the contact page") == ""
        assert commit_subject_problem("Fix the " + "a" * 64) == ""    # exactly 72
        assert commit_subject_problem("Fix the " + "a" * 65) != ""    # 73


class TestFlagRefusals:
    @pytest.mark.parametrize("flags", [
        {"commit_message": "Add the page", "commit_auto": True},
        {"commit_message": "Add the page", "commit_with_history": True},
        {"commit_auto": True, "commit_with_history": True},
        {"commit_message": "Add the page", "commit_auto": True, "push": True},
    ])
    @pytest.mark.parametrize("approve", [True, False])
    def test_f1_the_commit_flags_clash(self, repo, monkeypatch, flags, approve):
        job = _completed(repo, monkeypatch)
        before = _state(repo)
        sentence = _refused(apply_job(job.job_id, str(repo), approve=approve, **flags),
                            COMMIT_REFUSED, before, repo)
        assert "only one of them may be given" in sentence

    @pytest.mark.parametrize("message", ["", "   ", "Add the page\nand more"])
    def test_f2_an_empty_or_two_line_message_is_refused(self, repo, monkeypatch, message):
        job = _completed(repo, monkeypatch)
        before = _state(repo)
        sentence = _refused(apply_job(job.job_id, str(repo), approve=True,
                                      commit_message=message), COMMIT_REFUSED, before, repo)
        assert sentence.startswith("--commit ")

    @pytest.mark.parametrize("approve", [True, False])
    def test_f3_a_lone_push_is_refused(self, repo, monkeypatch, approve):
        job = _completed(repo, monkeypatch)
        before = _state(repo)
        sentence = _refused(apply_job(job.job_id, str(repo), approve=approve, push=True),
                            PUSH_REFUSED, before, repo)
        assert "refused alone" in sentence

    @pytest.mark.parametrize("mode", [{"commit_message": "Add the page"},
                                      {"commit_auto": True}])
    def test_f4_a_dirty_tree_is_refused_naming_the_path(self, repo, monkeypatch, mode):
        job = _completed(repo, monkeypatch)
        (repo / "scratch.txt").write_text("wip\n")
        before = _state(repo)
        sentence = _refused(apply_job(job.job_id, str(repo), approve=True, **mode),
                            COMMIT_REFUSED, before, repo)
        assert "uncommitted changes in scratch.txt" in sentence
        assert not (repo / "one.txt").exists()

    def test_f5_a_detached_head_is_refused(self, repo, monkeypatch):
        job = _completed(repo, monkeypatch)
        _git(repo, "checkout", "-q", "--detach")
        before = _state(repo)
        assert "detached HEAD" in _refused(
            apply_job(job.job_id, str(repo), approve=True, commit_message="Add the page"),
            COMMIT_REFUSED, before, repo)
        assert not (repo / "one.txt").exists()

    def test_f6_a_rebase_in_progress_is_refused_and_left_alone(self, repo, monkeypatch):
        job = _completed(repo, monkeypatch)
        branch = _branch(repo)
        _git(repo, "checkout", "-q", "-b", "side")
        _operator_commit(repo, "base.txt", "side\n", "Edit base on the side")
        _git(repo, "checkout", "-q", branch)
        _operator_commit(repo, "base.txt", "main\n", "Edit base on the branch")
        _git(repo, "checkout", "-q", "side")
        rebase = subprocess.run(["git", "rebase", branch], cwd=str(repo),
                                capture_output=True, text=True, timeout=60)
        assert rebase.returncode != 0 and (repo / ".git" / "rebase-merge").is_dir()
        before = _state(repo)
        result = apply_job(job.job_id, str(repo), approve=True, commit_message="Add the page")
        _refused(result, COMMIT_REFUSED, before, repo)
        assert any("in the middle of a rebase of its own" in r
                   for r in result.blocked_reasons), result.blocked_reasons
        assert (repo / ".git" / "rebase-merge").is_dir() and not (repo / "one.txt").exists()

    def test_f7_a_copied_path_the_gitignore_matches_is_refused(self, repo, monkeypatch):
        job = _completed(repo, monkeypatch)
        _operator_commit(repo, ".gitignore", "two.txt\n", "Ignore two")
        before = _state(repo)
        sentence = _refused(apply_job(job.job_id, str(repo), approve=True,
                                      commit_message="Add the page"),
                            COMMIT_REFUSED, before, repo)
        assert ".gitignore matches two.txt" in sentence
        assert not (repo / "one.txt").exists()

    def test_f8_the_preview_names_every_refusal_and_the_command(self, repo, monkeypatch):
        job = _completed(repo, monkeypatch)
        (repo / "scratch.txt").write_text("wip\n")
        before = _state(repo)
        preview = apply_job(job.job_id, str(repo), commit_message="Add the page", push=True)
        assert preview.status == "dry_run" and _state(repo) == before
        summary = summarize_job_apply(preview)
        assert "With --approve, --commit --push would be refused:" in summary
        assert "uncommitted changes in scratch.txt" in summary and "no upstream" in summary
        assert "--approve --commit 'Add the page' --push" in summary


class TestPush:
    def test_p1_exactly_one_push_to_the_upstream_never_forced(
        self, repo, monkeypatch, tmp_path,
    ):
        remote = _bare_upstream(repo, tmp_path)
        assert _git(remote, "config", "receive.denyNonFastForwards").strip() == "true"
        job = _completed(repo, monkeypatch)
        branch, before = _branch(repo), _head(repo)
        result = apply_job(job.job_id, str(repo), approve=True,
                           commit_message="Add the contact page", push=True)
        assert result.status == "applied", (result.blocked_reason, result.push_error)
        head = _head(repo)
        assert _pushes(tmp_path) == [f"refs/heads/{branch} {before} {head}"]
        assert _git(remote, "rev-parse", f"refs/heads/{branch}").strip() == head
        assert result.pushed and result.push_remote == "origin"
        assert result.push_ref == f"refs/heads/{branch}" and result.push_error == ""
        record = load_job_apply_record(job.job_id, result.job_apply_id)
        assert record["pushed"] is True and record["push_remote"] == "origin"
        assert str(remote) not in json.dumps(record)            # the name, never the URL
        assert "never forced" in summarize_job_apply(result)

    def test_p2_the_push_argv_names_the_upstream_and_no_force(
        self, repo, monkeypatch, tmp_path,
    ):
        from packages.orchestration import job_apply as JA

        _bare_upstream(repo, tmp_path)
        job = _completed(repo, monkeypatch)
        seen: list[tuple[str, ...]] = []
        real = JA._history_git

        def spy(target, *args, **kw):
            if "push" in args:
                seen.append(args)
            return real(target, *args, **kw)

        monkeypatch.setattr(JA, "_history_git", spy)
        result = apply_job(job.job_id, str(repo), approve=True,
                           commit_message="Add the page", push=True)
        assert result.pushed, result.push_error
        assert seen == [("push", "--porcelain", "origin",
                         f"{result.commit_sha}:refs/heads/{_branch(repo)}")]

    def test_p3_the_history_merge_is_pushed_once(self, repo, monkeypatch, tmp_path):
        remote = _bare_upstream(repo, tmp_path)
        job = _completed(repo, monkeypatch)
        result = apply_job(job.job_id, str(repo), approve=True, commit_with_history=True,
                           push=True)
        assert result.status == "applied", (result.blocked_reason, result.push_error)
        assert result.commit_sha == result.merge_commit != ""
        assert len(_pushes(tmp_path)) == 1
        assert _git(remote, "rev-parse", _branch(repo)).strip() == result.merge_commit

    def test_p4_no_upstream_is_refused_naming_the_command(self, repo, monkeypatch, tmp_path):
        remote = tmp_path / "remote.git"
        subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True, timeout=60)
        _git(repo, "remote", "add", "origin", str(remote))
        job = _completed(repo, monkeypatch)
        before = _state(repo)
        sentence = _refused(apply_job(job.job_id, str(repo), approve=True,
                                      commit_message="Add the page", push=True),
                            PUSH_REFUSED, before, repo)
        assert f"`git push --set-upstream origin {_branch(repo)}`" in sentence
        assert _git(remote, "for-each-ref") == "" and not (repo / "one.txt").exists()

    def test_p5_an_unmet_blocking_criterion_is_refused_before_anything(
        self, repo, monkeypatch, tmp_path,
    ):
        """DECISION F270 D4 (6): an `unmet` blocking criterion is red and holds the push."""
        _bare_upstream(repo, tmp_path)
        job = _completed(repo, monkeypatch)
        _mission(monkeypatch, statuses={"C001": ("met", True), "C002": ("unmet", True),
                                        "C003": ("unmet", False), "C004": ("open", True)})
        before = _state(repo)
        sentence = _refused(apply_job(job.job_id, str(repo), approve=True,
                                      commit_auto=True, push=True),
                            PUSH_REFUSED, before, repo)
        assert "criteria C002 are unmet, so nothing is pushed" in sentence
        assert "C003" not in sentence and "C004" not in sentence
        assert _pushes(tmp_path) == [] and not (repo / "one.txt").exists()

    def test_p7_an_open_blocking_criterion_is_pushed_and_named(
        self, repo, monkeypatch, tmp_path,
    ):
        """DECISION F270 D4 (6): an `open` blocking criterion, which no gate has evaluated,
        does not hold the push; it is named in the output and the record."""
        remote = _bare_upstream(repo, tmp_path)
        job = _completed(repo, monkeypatch)
        _mission(monkeypatch, statuses={"C001": ("met", True), "C002": ("open", True),
                                        "C003": ("open", False)})
        result = apply_job(job.job_id, str(repo), approve=True, commit_auto=True, push=True)
        assert result.status == "applied", (result.blocked_reason, result.push_error)
        assert result.pushed and len(_pushes(tmp_path)) == 1
        assert _git(remote, "rev-parse", _branch(repo)).strip() == result.commit_sha
        assert result.push_open_criteria == ["C002"]
        record = load_job_apply_record(job.job_id, result.job_apply_id)
        assert record["push_open_criteria"] == ["C002"]
        summary = summarize_job_apply(result)
        assert "criteria C002 are still open, not yet evaluated" in summary
        assert "C003" not in summary

    def test_p6_a_push_that_fails_leaves_the_commit_and_says_so(
        self, repo, monkeypatch, tmp_path,
    ):
        remote = _bare_upstream(repo, tmp_path)
        hook = remote / "hooks" / "pre-receive"
        hook.write_text("#!/bin/sh\necho the remote is frozen >&2\nexit 1\n")
        hook.chmod(0o755)
        job = _completed(repo, monkeypatch)
        remote_tip = _git(remote, "rev-parse", _branch(repo)).strip()
        result = apply_job(job.job_id, str(repo), approve=True,
                           commit_message="Add the page", push=True)
        assert result.status == "applied_push_failed"
        assert result.pushed is False and "the remote is frozen" in result.push_error
        assert result.commit_sha == _head(repo) != remote_tip
        assert _git(remote, "rev-parse", _branch(repo)).strip() == remote_tip
        assert "stays where it landed" in summarize_job_apply(result)
        record = load_job_apply_record(job.job_id, result.job_apply_id)
        assert record["status"] == "applied_push_failed" and record["push_error"]


class TestNoCommitWithoutAFlag:
    @pytest.mark.parametrize("key_set", [False, True])
    def test_n1_plain_approve_commits_and_pushes_nothing(
        self, repo, monkeypatch, tmp_path, key_set,
    ):
        _bare_upstream(repo, tmp_path)
        if key_set:
            monkeypatch.setenv("REMEDY_APPLY_PUSH_AFTER_MISSION", "true")
        job = _completed(repo, monkeypatch)
        head = _head(repo)
        result = apply_job(job.job_id, str(repo), approve=True)
        assert result.status == "applied", result.blocked_reason
        assert result.commit_sha == "" and result.commit_message_mode == "" and not result.pushed
        assert _head(repo) == head and _pushes(tmp_path) == []
        assert sorted(_git(repo, "status", "--porcelain").splitlines()) == [
            "?? one.txt", "?? two.txt"]
        assert "No commits or pushes were made" in summarize_job_apply(result)


class TestTheConfigKey:
    def test_k1_registered_as_a_bool_defaulting_to_false(self):
        spec = get_key_spec("apply.push_after_mission")
        assert spec is not None and spec.value_type is bool and spec.default is False
        assert spec.env_var == "REMEDY_APPLY_PUSH_AFTER_MISSION"
        assert spec.description.endswith(".") and ". " not in spec.description

    @pytest.mark.parametrize("raw, expected", [
        (None, False), ("true", True), ("1", True), ("yes", True),
        ("false", False), ("0", False), ("maybe", False),
    ])
    def test_k2_the_helper_reads_only_a_true_env_value_as_true(
        self, monkeypatch, tmp_path, raw, expected,
    ):
        if raw is None:
            monkeypatch.delenv("REMEDY_APPLY_PUSH_AFTER_MISSION", raising=False)
        else:
            monkeypatch.setenv("REMEDY_APPLY_PUSH_AFTER_MISSION", raw)
        config = load_config(tmp_path / "none.toml", tmp_path / "none-user.toml")
        assert push_after_mission_enabled(config) is expected

    @pytest.mark.parametrize("toml_value, expected", [
        ("true", True), ("false", False), ('"false"', False), ('"true"', True)])
    def test_k3_the_toml_string_false_is_false(self, monkeypatch, tmp_path,
                                               toml_value, expected):
        monkeypatch.delenv("REMEDY_APPLY_PUSH_AFTER_MISSION", raising=False)
        project = tmp_path / "remedy.toml"
        project.write_text(f"[remedy.apply]\npush_after_mission = {toml_value}\n")
        config = load_config(project, tmp_path / "none-user.toml")
        assert push_after_mission_enabled(config) is expected


class TestThroughTheCli:
    def test_a_clash_is_a_blocked_apply_and_a_commit_lands(self, repo, monkeypatch, data_root):
        from tests.cli.runtime_helpers import run_grouped_cli

        job = _completed(repo, monkeypatch)
        base = ["job", "apply", job.job_id, "--repo", str(repo), "--approve", "--json"]
        clash = run_grouped_cli(base + ["--commit", "Add the page", "--commit-auto"],
                                data_root, timeout=120)
        assert clash.returncode == 0, clash.stderr          # a blocked apply exits 0
        assert json.loads(clash.stdout)["blocked_reason"].startswith(f"{COMMIT_REFUSED}: ")
        alone = run_grouped_cli(base + ["--push"], data_root, timeout=120)
        assert json.loads(alone.stdout)["blocked_reason"].startswith(f"{PUSH_REFUSED}: ")

        landed = run_grouped_cli(base + ["--commit", "Add the contact page"],
                                 data_root, timeout=120)
        assert landed.returncode == 0, landed.stderr
        data = json.loads(landed.stdout)
        assert data["status"] == "applied", data["blocked_reason"]
        assert all(key in data for key in COMMIT_KEYS)
        assert data["commit_sha"] == _head(repo)
        assert _paragraphs(repo)[0] == "Add the contact page"

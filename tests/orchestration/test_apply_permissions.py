"""The apply's `write_worktree` / `commit` / `push` seams and `remedy do`'s mission-level push
ask the permission matrix through `apply_permissions.py` (DECISION F141 D3). `dependency_change`
and `destructive` ask the same matrix through a decision on the job instead of a flag
(DECISION F141 D4).

(a)-(f) drive the module's three public functions directly, on stand-in objects carrying only
``job_id``, ``commit_message_mode``, ``push`` and ``status``, with a data root under ``tmp_path``.
(g)-(i) drive the real paths — `apply_job` and `do_mission_push_refusals` — mirroring the fixtures
of `tests/orchestration/test_job_apply_commit.py`. A test that needs the push switch off gives
`get_config` a config loaded with `load_config` from a project file under `tmp_path`; never the
environment (autonomy.allow_push is refused from the environment by the matrix itself).

(j)-(r) drive `dependency_change` and `destructive`'s predicates and their decision path, on the
same kind of stand-in objects, now also carrying ``worktree_branch`` and an empty ``metadata``
dict (the escalation store). (s) drives the real `_flag_refusals` directly against a real git
branch that deletes a tracked file (see its docstring for why not the full `apply_job`).
(t)-(u) are R-1398: `do_push_mission`'s own `push` seam.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from types import SimpleNamespace

from packages.orchestration import config as config_module
from packages.orchestration import job_apply as job_apply_module
from packages.orchestration import pingpong_job as pingpong_job_module
from packages.orchestration.apply_permissions import (
    DEPENDENCY_MANIFEST_NAMES,
    PERMISSION_APPROVE,
    PERMISSION_DECISION_TASK_ID,
    PERMISSION_DECLINE,
    WRITE_PERMISSION_REFUSED,
    apply_permission_refusals,
    grant_push_permission,
    is_dependency_manifest,
    is_migration_path,
    push_permission_refusals,
)
from packages.orchestration.config import load_config
from packages.orchestration.data_paths import data_class_dir, job_dir
from packages.orchestration.do_apply import do_mission_push_refusals, do_push_mission
from packages.orchestration.do_context import DO_STEP_DONE, DO_STEP_FAILED, DoContext
from packages.orchestration.escalation import answer_task_decision, escalation_records
from packages.orchestration.job_apply import (
    COMMIT_REFUSED,
    HISTORY_REFUSED,
    PUSH_REFUSED,
    PushOutcome,
    apply_job,
    apply_refusal,
)
from packages.orchestration.permission_matrix import (
    JOB_LEVEL_FILENAME,
    PERMISSION_DENY,
    PERMISSION_GRANTS_FILENAME,
    PERMISSION_MATRIX,
)
from tests.orchestration.test_job_apply_commit import _bare_upstream
from tests.orchestration.test_job_apply_history import (  # noqa: F401  (autouse fixture)
    _completed,
    _one_task_job,
    _state,
    data_root,
)
from tests.orchestration.test_job_worktree_integration import (  # noqa: F401  (fixture)
    _git,
    repo,
)


def _result(**overrides) -> SimpleNamespace:
    base = {"commit_message_mode": "", "push": False, "status": ""}
    base.update(overrides)
    return SimpleNamespace(**base)


def _pin(job_id: str, level: str) -> None:
    folder = job_dir(job_id)
    folder.mkdir(parents=True, exist_ok=True)
    (folder / JOB_LEVEL_FILENAME).write_text(json.dumps({"level": level}), encoding="utf-8")


def _grants() -> list[dict]:
    path = data_class_dir("autonomy") / PERMISSION_GRANTS_FILENAME
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()]


def _switch_off(tmp_path):
    project = tmp_path / "remedy.toml"
    project.write_text("[remedy]\nautonomy.allow_push = false\n", encoding="utf-8")
    return load_config(project_path=project, user_path=tmp_path / "none-user.toml")


def _switch_on(tmp_path):
    return load_config(project_path=tmp_path / "none.toml", user_path=tmp_path / "none-user.toml")


# ---------------------------------------------------------------------------
# (a)-(f): the module's own functions, on stand-in objects
# ---------------------------------------------------------------------------


def test_a_plain_apply_previews_clean_then_grants_write_worktree_at_the_late_call():
    job = SimpleNamespace(job_id="job-a")
    result = _result()

    assert apply_permission_refusals(job, result, [], []) == []
    assert _grants() == []

    result.status = "approved_apply_started"
    assert apply_permission_refusals(job, result, [], []) == []
    grants = _grants()
    assert len(grants) == 1
    assert grants[0]["action"] == "write_worktree"
    assert grants[0]["approval_kind"] == "flag" and grants[0]["approval_ref"] == "--approve"
    assert grants[0]["job_id"] == "job-a"


def test_b_a_message_commit_with_push_grants_all_three_in_order():
    job = SimpleNamespace(job_id="job-b")
    result = _result(commit_message_mode="message", push=True, status="approved_apply_started")

    assert apply_permission_refusals(job, result, [], []) == []
    grants = _grants()
    assert [g["action"] for g in grants] == ["write_worktree", "commit", "push"]
    assert [g["approval_ref"] for g in grants] == ["--approve", "--commit", "--push"]


def test_c_a_pinned_l5_job_with_auto_and_push_grants_only_push():
    _pin("job-c", "L5")
    job = SimpleNamespace(job_id="job-c")
    result = _result(commit_message_mode="auto", push=True, status="approved_apply_started")

    assert apply_permission_refusals(job, result, [], []) == []
    grants = _grants()
    assert [g["action"] for g in grants] == ["push"]
    assert grants[0]["approval_ref"] == "--push"


def test_d_switch_off_refuses_push_and_writes_no_grant_even_at_the_late_call(tmp_path, monkeypatch):
    monkeypatch.setattr(config_module, "get_config", lambda: _switch_off(tmp_path))
    job = SimpleNamespace(job_id="job-d")
    result = _result(commit_message_mode="message", push=True, status="approved_apply_started")

    refusals = apply_permission_refusals(job, result, [], [])
    assert len(refusals) == 1
    assert refusals[0].startswith(f"{PUSH_REFUSED}: Remedy may not push")
    assert "(push, L2) = deny" in refusals[0]
    assert _grants() == []


def test_e1_a_denied_commit_cell_answers_history_merge_refused_in_history_mode(monkeypatch):
    monkeypatch.setitem(PERMISSION_MATRIX, ("commit", "L2"), PERMISSION_DENY)
    job = SimpleNamespace(job_id="job-e1")
    result = _result(commit_message_mode="history", status="approved_apply_started")

    refusals = apply_permission_refusals(job, result, [], [])
    assert refusals and refusals[0].startswith(f"{HISTORY_REFUSED}: ")


def test_e2_a_denied_commit_cell_answers_commit_refused_in_auto_mode(monkeypatch):
    monkeypatch.setitem(PERMISSION_MATRIX, ("commit", "L2"), PERMISSION_DENY)
    job = SimpleNamespace(job_id="job-e2")
    result = _result(commit_message_mode="auto", status="approved_apply_started")

    refusals = apply_permission_refusals(job, result, [], [])
    assert refusals and refusals[0].startswith(f"{COMMIT_REFUSED}: ")


def test_e3_a_denied_write_worktree_cell_answers_permission_refused(monkeypatch):
    monkeypatch.setitem(PERMISSION_MATRIX, ("write_worktree", "L2"), PERMISSION_DENY)
    job = SimpleNamespace(job_id="job-e3")
    result = _result(status="approved_apply_started")

    refusals = apply_permission_refusals(job, result, [], [])
    assert refusals and refusals[0].startswith(f"{WRITE_PERMISSION_REFUSED}: ")


def test_f1_push_permission_refusals_and_grant_with_switch_off_write_nothing(tmp_path, monkeypatch):
    monkeypatch.setattr(config_module, "get_config", lambda: _switch_off(tmp_path))

    refusals = push_permission_refusals("job-f1")
    assert refusals and refusals[0].startswith("Remedy may not push")

    denied = grant_push_permission("job-f1", "--push")
    assert denied.startswith("Remedy may not push")
    assert _grants() == []


def test_f2_grant_push_permission_with_switch_on_writes_one_grant(tmp_path, monkeypatch):
    monkeypatch.setattr(config_module, "get_config", lambda: _switch_on(tmp_path))

    assert grant_push_permission("job-f2", "apply.push_after_mission") == ""
    grants = _grants()
    assert len(grants) == 1
    assert grants[0]["action"] == "push"
    assert grants[0]["approval_ref"] == "apply.push_after_mission"


# ---------------------------------------------------------------------------
# (g)-(i): the real paths, mirroring test_job_apply_commit.py's own fixtures
# ---------------------------------------------------------------------------


def test_g_switch_off_blocks_an_approved_apply_with_a_commit_and_push(repo, monkeypatch, tmp_path):
    _bare_upstream(repo, tmp_path)
    job = _completed(repo, monkeypatch)
    before = _state(repo)
    monkeypatch.setattr(config_module, "get_config", lambda: _switch_off(tmp_path))

    result = apply_job(job.job_id, str(repo), approve=True,
                       commit_message="Add the page", push=True)

    assert result.status == "blocked", result.blocked_reason
    token, sentence = apply_refusal(result)
    assert token == "push_refused"
    assert "autonomy.allow_push is false" in sentence
    assert _state(repo) == before


def test_h_a_plain_approved_apply_copies_and_leaves_one_write_worktree_grant(repo, monkeypatch):
    job = _completed(repo, monkeypatch)

    result = apply_job(job.job_id, str(repo), approve=True)

    assert result.status == "applied", result.blocked_reason
    assert (repo / "one.txt").exists() and (repo / "two.txt").exists()
    grants = _grants()
    assert len(grants) == 1
    assert grants[0]["action"] == "write_worktree"
    assert grants[0]["approval_ref"] == "--approve"
    assert grants[0]["job_id"] == job.job_id


def test_i_do_mission_push_refusals_with_switch_off_answers_the_switch_sentence(
    tmp_path, monkeypatch,
):
    monkeypatch.setattr(config_module, "get_config", lambda: _switch_off(tmp_path))
    ctx = DoContext(order="goal", repo_root=str(tmp_path))

    refusals, still_open, unchecked = do_mission_push_refusals(ctx)

    assert any(r.startswith("Remedy may not push") for r in refusals)
    assert still_open == [] and unchecked == []


# ---------------------------------------------------------------------------
# (j)-(k): the two predicates (DECISION F141 D4 (1))
# ---------------------------------------------------------------------------


def test_j_is_dependency_manifest_matches_every_manifest_name_and_requirements_txt():
    for name in DEPENDENCY_MANIFEST_NAMES:
        assert is_dependency_manifest(name)
        assert is_dependency_manifest(f"sub/dir/{name}")
    assert is_dependency_manifest("requirements-dev.txt")
    for not_manifest in ("src/app.py", "Makefile", "tsconfig.json", "docs/requirements.md"):
        assert not is_dependency_manifest(not_manifest)


def test_k_is_migration_path_matches_a_migrations_folder_only():
    for migration in ("app/migrations/0001_init.py", "migrations/env.py"):
        assert is_migration_path(migration)
    for not_migration in ("migrations.py", "src/migrationsfoo/x.py"):
        assert not is_migration_path(not_migration)


# ---------------------------------------------------------------------------
# (l)-(r): `dependency_change` and `destructive` ask through a decision on the job
# (DECISION F141 D4 (2)), on stand-in objects carrying `worktree_branch` and an empty
# escalation store.
# ---------------------------------------------------------------------------


def _job(job_id: str) -> SimpleNamespace:
    return SimpleNamespace(job_id=job_id, worktree_branch=f"remedy/{job_id}", metadata={})


def test_l_a_dependency_change_raises_one_decision_naming_it_and_its_command(monkeypatch):
    calls = []
    monkeypatch.setattr(pingpong_job_module, "save_job_plan", lambda job: calls.append(job))
    job = _job("job-l")
    result = _result(approved=True, dry_run=False)

    refusals = apply_permission_refusals(job, result, ["pyproject.toml"], [])

    assert len(calls) == 1
    records = escalation_records(job)
    assert len(records) == 1
    record = records[0]
    assert record["task_id"] == PERMISSION_DECISION_TASK_ID
    assert record["options"] == [PERMISSION_APPROVE, PERMISSION_DECLINE]
    assert record["safe_default"] == PERMISSION_DECLINE
    assert "(dependency_change, L2) = ask" in record["question"]
    assert "pyproject.toml" in record["question"]
    assert len(refusals) == 1
    assert refusals[0].startswith(f"{WRITE_PERMISSION_REFUSED}: ")
    decision_id = record["decision_id"]
    assert decision_id in refusals[0] and record["question"] in refusals[0]

    second = apply_permission_refusals(job, result, ["pyproject.toml"], [])
    assert len(calls) == 1
    assert escalation_records(job) == records
    assert second == refusals


def test_m_a_preview_answers_the_preview_sentence_and_raises_nothing(monkeypatch):
    calls = []
    monkeypatch.setattr(pingpong_job_module, "save_job_plan", lambda job: calls.append(job))
    job = _job("job-m")
    result = _result(approved=False, dry_run=False)

    refusals = apply_permission_refusals(job, result, ["pyproject.toml"], [])

    assert calls == []
    assert escalation_records(job) == []
    assert len(refusals) == 1
    assert refusals[0].startswith(f"{WRITE_PERMISSION_REFUSED}: ")
    assert refusals[0].endswith("An approved apply asks you through a decision.")


def test_n_an_approved_decision_grants_at_the_late_call_only(monkeypatch):
    monkeypatch.setattr(pingpong_job_module, "save_job_plan", lambda job: None)
    job = _job("job-n")
    result = _result(approved=True, dry_run=False)
    apply_permission_refusals(job, result, ["pyproject.toml"], [])
    decision_id = escalation_records(job)[0]["decision_id"]
    answer_task_decision(job, decision_id, answer=PERMISSION_APPROVE,
                         now=datetime.now(timezone.utc))

    first = apply_permission_refusals(job, result, ["pyproject.toml"], [])
    assert first == []
    assert _grants() == []

    result.status = "approved_apply_started"
    late = apply_permission_refusals(job, result, ["pyproject.toml"], [])
    assert late == []
    decision_grants = [g for g in _grants() if g["action"] == "dependency_change"]
    assert len(decision_grants) == 1
    assert decision_grants[0]["approval_kind"] == "decision"
    assert decision_grants[0]["approval_ref"] == decision_id


def test_o_a_declined_decision_refuses_naming_the_answer(monkeypatch):
    monkeypatch.setattr(pingpong_job_module, "save_job_plan", lambda job: None)
    job = _job("job-o")
    result = _result(approved=True, dry_run=False)
    apply_permission_refusals(job, result, ["pyproject.toml"], [])
    decision_id = escalation_records(job)[0]["decision_id"]
    answer_task_decision(job, decision_id, answer=PERMISSION_DECLINE,
                         now=datetime.now(timezone.utc))

    refusals = apply_permission_refusals(job, result, ["pyproject.toml"], [])

    assert len(refusals) == 1
    assert refusals[0].startswith(f"{WRITE_PERMISSION_REFUSED}: ")
    assert f"You answered decision {decision_id} with {PERMISSION_DECLINE}" in refusals[0]
    assert refusals[0].endswith("so this apply stays refused.")


def test_p_a_pinned_l4_job_needs_no_decision_and_grants_nothing_for_it(monkeypatch):
    _pin("job-p", "L4")

    def _no_decision(job):
        raise AssertionError("no decision should be enqueued at L4")

    monkeypatch.setattr(pingpong_job_module, "save_job_plan", _no_decision)
    job = _job("job-p")
    result = _result(approved=True, dry_run=False, status="approved_apply_started")

    refusals = apply_permission_refusals(job, result, ["pyproject.toml"], [])

    assert refusals == []
    assert escalation_records(job) == []
    assert all(g["action"] != "dependency_change" for g in _grants())


def test_q_a_migration_path_asks_the_same_way_as_a_dependency_change(monkeypatch):
    monkeypatch.setattr(pingpong_job_module, "save_job_plan", lambda job: None)
    job = _job("job-q")
    result = _result(approved=True, dry_run=False)

    refusals = apply_permission_refusals(job, result, ["app/migrations/0001_init.py"], [])

    assert len(refusals) == 1
    assert refusals[0].startswith(f"{WRITE_PERMISSION_REFUSED}: ")
    assert "(destructive, L2) = ask" in refusals[0]
    assert "app/migrations/0001_init.py" in refusals[0]
    record = escalation_records(job)[0]
    assert record["decision_id"] in refusals[0]


def test_r_r1397_a_nonempty_refused_records_no_grant_while_empty_does(monkeypatch):
    monkeypatch.setattr(pingpong_job_module, "save_job_plan", lambda job: None)
    job1 = _job("job-r1")
    result1 = _result(approved=True, dry_run=False, status="approved_apply_started")

    held = apply_permission_refusals(job1, result1, [], ["commit_refused: a prior refusal."])
    assert held == []
    assert _grants() == []

    job2 = _job("job-r2")
    result2 = _result(approved=True, dry_run=False, status="approved_apply_started")
    clear = apply_permission_refusals(job2, result2, [], [])
    assert clear == []
    assert len(_grants()) == 1


# ---------------------------------------------------------------------------
# (s): a real history apply whose job branch deletes a tracked file
# ---------------------------------------------------------------------------


def _tree_without(repo_path, tree: str, rel: str) -> str:
    """The sha of TREE with REL removed, a top-level path of a flat tree (plumbing only,
    the working tree and the index are never touched)."""
    listing = subprocess.run(["git", "ls-tree", tree], cwd=str(repo_path),
                             capture_output=True, text=True, check=True).stdout
    kept = "\n".join(line for line in listing.splitlines() if not line.endswith(f"\t{rel}"))
    return subprocess.run(["git", "mktree"], cwd=str(repo_path),
                          input=(kept + "\n") if kept else "",
                          capture_output=True, text=True, check=True).stdout.strip()


def test_s_a_history_apply_whose_branch_deletes_a_tracked_file_is_blocked_by_a_decision(
    repo, monkeypatch,
):
    """DECISION F141 D4 (2)'s history-mode destructive check, on the real `_flag_refusals`
    and a real git branch that deletes `base.txt` (tracked in `repo`'s own initial commit).

    Deviation from the block's literal "through the real `apply_job`": `apply_job`'s
    pre-existing, unrelated fidelity gates (`_check_source_coverage`'s "unexpected"
    check and the `blocked_paths`/"would skip" checks of `_apply_from_workspace`) answer
    FIRST for any job branch that deletes a file no task's apply manifest declares, and
    a task's apply manifest can never declare a deleted file applied
    (`_verify_in_place_apply`'s own `missing_files` gate) — confirmed empirically, not
    merely reasoned. Reaching this case through `apply_job` itself would need another
    change to `job_apply.py`, which stays at 2541 lines this round. `_flag_refusals` is
    the real, unmodified function those fidelity gates sit in FRONT of; calling it
    directly, against the real target and a real job branch, still exercises the new
    destructive-via-history-diff code end to end, just without the unrelated gates this
    round does not touch.
    """
    monkeypatch.setattr(pingpong_job_module, "save_job_plan", lambda job: None)
    head = _git(repo, "rev-parse", "HEAD").strip()
    initial_tree = _git(repo, "rev-parse", f"{head}^{{tree}}").strip()
    new_tree = _tree_without(repo, initial_tree, "base.txt")
    branch = "remedy/job-s"
    new_tip = _git(repo, "commit-tree", new_tree, "-p", head, "-m", "delete base.txt").strip()
    _git(repo, "branch", branch, new_tip)
    diff_text = subprocess.run(
        ["git", "diff", "--no-color", "--no-ext-diff", "--src-prefix=a/", "--dst-prefix=b/",
         initial_tree, f"{new_tip}^{{tree}}"],
        cwd=str(repo), capture_output=True, text=True, check=True).stdout
    before = _state(repo)

    job = SimpleNamespace(job_id="job-s", worktree_branch=branch, worktree_head=new_tip,
                         job_initial_tree=initial_tree, metadata={}, isolation_mode="worktree",
                         result_diff_sha256=hashlib.sha256(diff_text.encode("utf-8")).hexdigest())
    result = _result(commit_message_mode="history", status="", approved=True, dry_run=False,
                     target_repo=str(repo))

    refusals = job_apply_module._flag_refusals(job, result, repo, [],
                                               skip_blocked=False, skipped=[])

    assert len(refusals) == 1
    assert refusals[0].startswith(f"{WRITE_PERMISSION_REFUSED}: ")
    assert "(destructive, L2) = ask" in refusals[0]
    assert "base.txt" in refusals[0]
    record = escalation_records(job)[-1]
    assert record["decision_id"] in refusals[0]
    assert _state(repo) == before


# ---------------------------------------------------------------------------
# (t)-(u): R-1398, `do_push_mission`'s own `push` seam
# ---------------------------------------------------------------------------


def test_t_r1398_do_push_mission_grants_the_configured_push_and_calls_it_once(
    tmp_path, monkeypatch,
):
    monkeypatch.setattr(config_module, "get_config", lambda: _switch_on(tmp_path))
    push_calls: list[tuple] = []

    def fake_push(target, sha, branch):
        push_calls.append((target, sha, branch))
        return PushOutcome(True, "origin", "refs/heads/main", "")

    monkeypatch.setattr(job_apply_module, "push_to_upstream", fake_push)
    ctx = DoContext(order="goal", repo_root=str(tmp_path), push=True,
                    push_source="apply.push_after_mission",
                    landed=[{"job_id": "job-t", "sha": "deadbeef", "branch": "main"}])

    status, sentence = do_push_mission(ctx)

    assert status == DO_STEP_DONE
    assert "apply.push_after_mission" in sentence
    assert len(push_calls) == 1
    grants = [g for g in _grants() if g["action"] == "push"]
    assert len(grants) == 1
    assert grants[0]["approval_ref"] == "apply.push_after_mission"
    assert grants[0]["job_id"] == "job-t"


def test_u_r1398_a_switch_turned_off_after_the_preflight_fails_naming_the_sentence(
    tmp_path, monkeypatch,
):
    on = _switch_on(tmp_path)
    off = _switch_off(tmp_path)
    calls = {"n": 0}

    def fake_get_config():
        calls["n"] += 1
        return on if calls["n"] == 1 else off

    monkeypatch.setattr(config_module, "get_config", fake_get_config)
    push_calls: list[tuple] = []
    monkeypatch.setattr(job_apply_module, "push_to_upstream",
                        lambda *a: push_calls.append(a) or PushOutcome(True, "origin", "x", ""))
    ctx = DoContext(order="goal", repo_root=str(tmp_path), push=True,
                    push_source="apply.push_after_mission",
                    landed=[{"job_id": "job-u", "sha": "deadbeef", "branch": "main"}])

    status, sentence = do_push_mission(ctx)

    assert status == DO_STEP_FAILED
    assert "autonomy.allow_push is false" in sentence
    assert ctx.push_outcome is not None
    assert "autonomy.allow_push is false" in ctx.push_outcome["error"]
    assert push_calls == []


# ---------------------------------------------------------------------------
# (v)-(x): R-1399 — `_flag_refusals` hands the apply's planned paths and its own
# refusals to the matrix, through the real paths (`apply_job`, `_flag_refusals`).
# ---------------------------------------------------------------------------


def test_v_r1399_a_plain_approved_apply_of_a_dependency_change_blocks_apply_failed(
    repo, monkeypatch,
):
    job = _one_task_job(repo, monkeypatch, "pyproject.toml")
    before = _state(repo)

    result = apply_job(job.job_id, str(repo), approve=True)

    assert result.status == "blocked", result.blocked_reason
    token, sentence = apply_refusal(result)
    assert token == "apply_failed"
    assert "(dependency_change, L2) = ask" in sentence
    reloaded = pingpong_job_module.load_job_plan(job.job_id)
    record = escalation_records(reloaded)[-1]
    assert record["decision_id"] in sentence
    assert _state(repo) == before


def test_w_r1399_the_same_with_a_commit_message_also_blocks_apply_failed(repo, monkeypatch):
    job = _one_task_job(repo, monkeypatch, "pyproject.toml")
    before = _state(repo)

    result = apply_job(job.job_id, str(repo), approve=True, commit_message="Add a dependency")

    assert result.status == "blocked", result.blocked_reason
    token, sentence = apply_refusal(result)
    assert token == "apply_failed"
    assert "(dependency_change, L2) = ask" in sentence
    reloaded = pingpong_job_module.load_job_plan(job.job_id)
    record = escalation_records(reloaded)[-1]
    assert record["decision_id"] in sentence
    assert _state(repo) == before


def test_x_r1399_the_late_call_over_a_dirty_tracked_target_refuses_and_grants_nothing(
    repo, monkeypatch,
):
    """`_flag_refusals` at the late call (`status == "approved_apply_started"`), directly,
    over a target whose own tracked file (`base.txt`) is dirty: history mode's checkout
    refusal fires, and `apply_permission_refusals` grants nothing while it stands
    (DECISION F141 D4 (3))."""
    job = _completed(repo, monkeypatch)
    (repo / "base.txt").write_text("dirtied by hand\n")

    refusals = job_apply_module._flag_refusals(
        job, _result(commit_message_mode="history", status="approved_apply_started"),
        repo, ["one.txt", "two.txt"], skip_blocked=False, skipped=[])

    assert len(refusals) == 1
    assert refusals[0].startswith(f"{HISTORY_REFUSED}: ")
    assert "uncommitted changes in base.txt" in refusals[0]
    assert _grants() == []

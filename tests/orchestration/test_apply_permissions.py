"""The apply's `write_worktree` / `commit` / `push` seams and `remedy do`'s mission-level push
ask the permission matrix through `apply_permissions.py` (DECISION F141 D3).

(a)-(f) drive the module's three public functions directly, on stand-in objects carrying only
``job_id``, ``commit_message_mode``, ``push`` and ``status``, with a data root under ``tmp_path``.
(g)-(i) drive the real paths — `apply_job` and `do_mission_push_refusals` — mirroring the fixtures
of `tests/orchestration/test_job_apply_commit.py`. A test that needs the push switch off gives
`get_config` a config loaded with `load_config` from a project file under `tmp_path`; never the
environment (autonomy.allow_push is refused from the environment by the matrix itself).
"""
from __future__ import annotations

import json
from types import SimpleNamespace

from packages.orchestration import config as config_module
from packages.orchestration.apply_permissions import (
    WRITE_PERMISSION_REFUSED,
    apply_permission_refusals,
    grant_push_permission,
    push_permission_refusals,
)
from packages.orchestration.config import load_config
from packages.orchestration.data_paths import data_class_dir, job_dir
from packages.orchestration.do_apply import do_mission_push_refusals
from packages.orchestration.do_context import DoContext
from packages.orchestration.job_apply import (
    COMMIT_REFUSED,
    HISTORY_REFUSED,
    PUSH_REFUSED,
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

    assert apply_permission_refusals(job, result) == []
    assert _grants() == []

    result.status = "approved_apply_started"
    assert apply_permission_refusals(job, result) == []
    grants = _grants()
    assert len(grants) == 1
    assert grants[0]["action"] == "write_worktree"
    assert grants[0]["approval_kind"] == "flag" and grants[0]["approval_ref"] == "--approve"
    assert grants[0]["job_id"] == "job-a"


def test_b_a_message_commit_with_push_grants_all_three_in_order():
    job = SimpleNamespace(job_id="job-b")
    result = _result(commit_message_mode="message", push=True, status="approved_apply_started")

    assert apply_permission_refusals(job, result) == []
    grants = _grants()
    assert [g["action"] for g in grants] == ["write_worktree", "commit", "push"]
    assert [g["approval_ref"] for g in grants] == ["--approve", "--commit", "--push"]


def test_c_a_pinned_l5_job_with_auto_and_push_grants_only_push():
    _pin("job-c", "L5")
    job = SimpleNamespace(job_id="job-c")
    result = _result(commit_message_mode="auto", push=True, status="approved_apply_started")

    assert apply_permission_refusals(job, result) == []
    grants = _grants()
    assert [g["action"] for g in grants] == ["push"]
    assert grants[0]["approval_ref"] == "--push"


def test_d_switch_off_refuses_push_and_writes_no_grant_even_at_the_late_call(tmp_path, monkeypatch):
    monkeypatch.setattr(config_module, "get_config", lambda: _switch_off(tmp_path))
    job = SimpleNamespace(job_id="job-d")
    result = _result(commit_message_mode="message", push=True, status="approved_apply_started")

    refusals = apply_permission_refusals(job, result)
    assert len(refusals) == 1
    assert refusals[0].startswith(f"{PUSH_REFUSED}: Remedy may not push")
    assert "(push, L2) = deny" in refusals[0]
    assert _grants() == []


def test_e1_a_denied_commit_cell_answers_history_merge_refused_in_history_mode(monkeypatch):
    monkeypatch.setitem(PERMISSION_MATRIX, ("commit", "L2"), PERMISSION_DENY)
    job = SimpleNamespace(job_id="job-e1")
    result = _result(commit_message_mode="history", status="approved_apply_started")

    refusals = apply_permission_refusals(job, result)
    assert refusals and refusals[0].startswith(f"{HISTORY_REFUSED}: ")


def test_e2_a_denied_commit_cell_answers_commit_refused_in_auto_mode(monkeypatch):
    monkeypatch.setitem(PERMISSION_MATRIX, ("commit", "L2"), PERMISSION_DENY)
    job = SimpleNamespace(job_id="job-e2")
    result = _result(commit_message_mode="auto", status="approved_apply_started")

    refusals = apply_permission_refusals(job, result)
    assert refusals and refusals[0].startswith(f"{COMMIT_REFUSED}: ")


def test_e3_a_denied_write_worktree_cell_answers_permission_refused(monkeypatch):
    monkeypatch.setitem(PERMISSION_MATRIX, ("write_worktree", "L2"), PERMISSION_DENY)
    job = SimpleNamespace(job_id="job-e3")
    result = _result(status="approved_apply_started")

    refusals = apply_permission_refusals(job, result)
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

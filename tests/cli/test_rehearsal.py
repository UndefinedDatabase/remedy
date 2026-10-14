"""F055 T001 — `remedy do --rehearse`'s guarantees: it stops where `--plan-only` stops, it
refuses together with a flag that would answer, apply, commit or push, and a real run moves
the counters a rehearsal must leave at zero (DECISION F055 D1).

In-process through `apps.cli.grouped.main`, against a temporary git repository holding one
committed file, with the data root under `tmp_path`, the fake builder and reviewer, and
`--no-ui`, as `tests/cli/test_do_sequence_cli.py` drives `remedy do`. A tripwire fails the test
if any model-call factory is reached, except for the one test that deliberately mocks it.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from apps.cli.grouped import main
from tests.run_side_effect_counters import (
    count_applicator_calls,
    count_role_provider_builds,
    count_worktree_creations,
    snapshot_repository_state,
)

ORDER = "Write a CONTRIBUTING.md"
FAKE_ROLES = ("--builder-provider", "fake", "--reviewer-provider", "fake")


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=str(repo), capture_output=True,
                          text=True, check=True).stdout


@pytest.fixture
def repo(tmp_path, monkeypatch) -> Path:
    """An UNREGISTERED git repository with one committed file, as the working directory."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    target = tmp_path / "target"
    target.mkdir()
    _git(target, "init", "-q")
    _git(target, "config", "user.email", "t@e.com")
    _git(target, "config", "user.name", "T")
    _git(target, "config", "commit.gpgsign", "false")
    (target / "README.md").write_text("# target\n")
    _git(target, "add", "-A")
    _git(target, "commit", "-qm", "init")
    monkeypatch.chdir(target)
    return target.resolve()


@pytest.fixture(autouse=True)
def no_model_call(monkeypatch):
    """Every factory that could reach a model fails the test when called.

    The one test that deliberately drives the LLM-mocked plan branch (DECISION F055 D1's
    guarantees scenario (c)) replaces these same two names again, after this fixture, with its
    own fakes — the last `monkeypatch.setattr` of a name wins, as `test_plan_approval.py` relies
    on throughout.
    """
    def tripwire(*args, **kwargs):
        raise AssertionError("remedy do reached a model-call factory under --no-llm")

    import packages.orchestration.study  # noqa: F401
    monkeypatch.setattr("packages.orchestration.intake.make_provider_call_fn", tripwire)
    monkeypatch.setattr("packages.orchestration.intake.make_structured_call_fn", tripwire)
    monkeypatch.setattr("packages.orchestration.study.make_structured_call_fn", tripwire)
    monkeypatch.setattr("packages.orchestration.study.study_call_fn", tripwire)


def _do(capsys, *extra: str, order: str = ORDER) -> str:
    main(["do", order, "--no-llm", "--no-ui", *FAKE_ROLES, *extra])
    return capsys.readouterr().out


def _do_json(capsys, *extra: str, order: str = ORDER) -> dict:
    return json.loads(_do(capsys, "--json", *extra, order=order))


def _step(data: dict, name: str) -> dict:
    return next(s for s in data["steps"] if s["name"] == name)


# ── (a) a rehearsal moves nothing ────────────────────────────────────────────


def test_rehearsal_runs_no_job_and_moves_no_counter(repo, capsys, monkeypatch):
    from packages.core.models import RunState
    from packages.orchestration.pingpong_job import load_job_plan

    role_builds = count_role_provider_builds(monkeypatch)
    applicator_calls = count_applicator_calls(monkeypatch)
    worktrees_created = count_worktree_creations(monkeypatch)
    before = snapshot_repository_state(repo)

    data = _do_json(capsys, "--rehearse")

    after = snapshot_repository_state(repo)
    run = _step(data, "run")
    assert run["status"] == "stopped"
    assert run["detail"].startswith(
        "--rehearse: no job was run and nothing was written to the repository; ")
    assert not role_builds
    assert not applicator_calls
    assert not worktrees_created
    assert after == before
    [job_id] = data["job_ids"]
    assert load_job_plan(job_id).state == RunState.PLANNED


# ── (b) the same order, for real, moves them ─────────────────────────────────


def test_the_same_order_without_rehearse_moves_the_provider_and_worktree_counters(
        repo, capsys, monkeypatch):
    from packages.orchestration.pingpong_job import JOB_COMPLETED, load_job_plan

    role_builds = count_role_provider_builds(monkeypatch)
    # `count_applicator_calls` is not asserted here: a bare `remedy do "<order>"` (no `--apply`)
    # never reaches the apply step, `apply_patch_intent` is only `remedy patch apply`'s path, and
    # `_strict_apply_to_workspace` is the non-worktree copy-mode fallback, not the git-worktree
    # path this fixture's job takes (named in the handback, not a blind counter).
    worktrees_created = count_worktree_creations(monkeypatch)
    before = snapshot_repository_state(repo)

    data = _do_json(capsys)

    after = snapshot_repository_state(repo)
    assert load_job_plan(data["job_ids"][0]).state == JOB_COMPLETED
    assert role_builds["builder"] > 0
    assert role_builds["reviewer"] > 0
    assert worktrees_created
    assert after != before


# ── (c) a rehearsal with a pending plan names the approval before the run line ──


def test_rehearsal_of_a_pending_task_plan_names_the_approval_before_the_run_line(
        repo, capsys, monkeypatch):
    from packages.orchestration import do_sequence
    from packages.orchestration.pingpong_job import load_job_plan
    from tests.cli.test_plan_approval import _setup_llm_mocks

    real_plan_order_job = do_sequence.plan_order_job

    def planned_on_the_llm_branch(order, **kwargs):
        _setup_llm_mocks(monkeypatch, plan_succeeds=True)
        return real_plan_order_job(order, **{**kwargs, "no_llm": False})

    monkeypatch.setattr(do_sequence, "plan_order_job", planned_on_the_llm_branch)

    role_builds = count_role_provider_builds(monkeypatch)
    applicator_calls = count_applicator_calls(monkeypatch)
    worktrees_created = count_worktree_creations(monkeypatch)

    data = _do_json(capsys, "--rehearse", "--force-job")

    [job_id] = data["job_ids"]
    task_plan = load_job_plan(job_id).task_plan
    assert task_plan["_approval"] == "pending"
    from packages.core.models import RunState
    assert load_job_plan(job_id).state == RunState.PLANNED
    approve = f"remedy decision resolve {job_id} plan:approval --reason approve"
    run_line = f"remedy job run {job_id}"
    assert approve in data["next"]
    index = data["next"].index(approve)
    assert data["next"][index + 1].startswith(run_line)
    assert not role_builds
    assert not applicator_calls
    assert not worktrees_created


# ── (d) --rehearse refuses together with --yes or a commit/apply/push flag ──────


@pytest.mark.parametrize(("flag", "message_tail"), [
    (("--yes",),
     "--rehearse leaves the plan's approval open for you to answer, and --yes would approve "
     "it unattended. Nothing was run."),
    (("--apply",),
     "--rehearse runs no job, so --apply would have nothing to apply, commit or push. "
     "Nothing was run."),
    (("--commit", "m"),
     "--rehearse runs no job, so --commit would have nothing to apply, commit or push. "
     "Nothing was run."),
    (("--commit-auto",),
     "--rehearse runs no job, so --commit-auto would have nothing to apply, commit or push. "
     "Nothing was run."),
    (("--commit-with-history",),
     "--rehearse runs no job, so --commit-with-history would have nothing to apply, commit or "
     "push. Nothing was run."),
    (("--push",),
     "--rehearse runs no job, so --push would have nothing to apply, commit or push. "
     "Nothing was run."),
])
def test_rehearse_refuses_with_a_conflicting_flag(repo, capsys, monkeypatch, flag, message_tail):
    from packages.orchestration.pingpong_job import list_job_plans

    role_builds = count_role_provider_builds(monkeypatch)
    applicator_calls = count_applicator_calls(monkeypatch)
    worktrees_created = count_worktree_creations(monkeypatch)

    with pytest.raises(SystemExit) as exc:
        _do(capsys, "--rehearse", "--json", *flag)

    assert exc.value.code == 2
    out = json.loads(capsys.readouterr().out)
    assert out["ok"] is False
    assert out["error"] == "invalid_argument"
    assert out["message"] == message_tail
    assert list_job_plans() == []
    assert not role_builds
    assert not applicator_calls
    assert not worktrees_created


# ── (e) --rehearse --json: the run step, stopped, with its prefix ───────────────


def test_rehearse_json_run_step_is_stopped_with_its_prefix(repo, capsys):
    data = _do_json(capsys, "--rehearse")

    run = _step(data, "run")
    assert run["status"] == "stopped"
    assert run["detail"].startswith(
        "--rehearse: no job was run and nothing was written to the repository; ")

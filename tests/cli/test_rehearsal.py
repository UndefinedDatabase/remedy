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
    count_planning_calls,
    count_role_provider_builds,
    count_worktree_creations,
    snapshot_repository_state,
)

ORDER = "Write a CONTRIBUTING.md"
#: An order naming two files walks the full lane, where a generated plan keeps its approval open.
TWO_FILE_ORDER = "Write CONTRIBUTING.md and CHANGELOG.md"
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


def _plan_with_mocked_llm(monkeypatch) -> None:
    """Route the shape step's planning through the (mocked) LLM task-plan branch, as scenario
    (c) does, so a rehearsed job's task plan waits for a person's approval (DECISION F055 D3)."""
    from packages.orchestration import do_sequence
    from tests.cli.test_plan_approval import _setup_llm_mocks

    real_plan_order_job = do_sequence.plan_order_job

    def planned_on_the_llm_branch(order, **kwargs):
        _setup_llm_mocks(monkeypatch, plan_succeeds=True)
        return real_plan_order_job(order, **{**kwargs, "no_llm": False})

    monkeypatch.setattr(do_sequence, "plan_order_job", planned_on_the_llm_branch)


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

    data = _do_json(capsys, "--rehearse", order=TWO_FILE_ORDER)

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


# ── (d) --rehearse refuses together with --run-unattended or a commit/apply/push flag ──────


@pytest.mark.parametrize(("flag", "message_tail"), [
    (("--run-unattended",),
     "--rehearse leaves the plan's approval open for you to answer, and --run-unattended would approve "
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


# ── (k) --rehearse writes rehearsal.json and rehearsal.md beside the job ────────


def test_rehearse_writes_the_rehearsal_record_and_names_it_in_the_run_step(repo, capsys):
    from packages.orchestration.data_paths import job_evidence_dir

    before = snapshot_repository_state(repo)
    real_head = _git(repo, "rev-parse", "HEAD").strip()

    data = _do_json(capsys, "--rehearse")

    after = snapshot_repository_state(repo)
    assert after == before
    [job_id] = data["job_ids"]
    evidence_dir = job_evidence_dir(job_id)
    json_path = evidence_dir / "rehearsal.json"
    md_path = evidence_dir / "rehearsal.md"
    assert json_path.is_file()
    assert md_path.is_file()
    record = json.loads(json_path.read_text(encoding="utf-8"))
    assert record["schema_v"] == "rehearsal_v1"
    assert record["repo_head"] == real_head

    run = _step(data, "run")
    assert str(md_path) in run["detail"]


# ── (l) R-1316: the applicator counter, proven to count ─────────────────────────


def test_a_real_apply_run_moves_the_applicator_counter(repo, capsys, monkeypatch):
    applicator_calls = count_applicator_calls(monkeypatch)

    _do_json(capsys, "--apply")

    assert applicator_calls["apply_job"] > 0


# ── (m) rehearse, approve, run: no second planning call (R-1317, DECISION F055 D3) ──


def test_approve_then_run_a_rehearsed_job_completes_with_no_further_planning_call(
        repo, capsys, monkeypatch):
    from packages.orchestration.pingpong_job import JOB_COMPLETED, load_job_plan

    _plan_with_mocked_llm(monkeypatch)

    data = _do_json(capsys, "--rehearse", "--force-job", order="Write m.md")
    [job_id] = data["job_ids"]
    assert load_job_plan(job_id).task_plan["_approval"] == "pending"

    planning_calls = count_planning_calls(monkeypatch)

    main(["decision", "resolve", job_id, "plan:approval", "--reason", "approve"])
    capsys.readouterr()
    main(["job", "run", job_id, *FAKE_ROLES, "--json"])
    capsys.readouterr()

    assert load_job_plan(job_id).state == JOB_COMPLETED
    assert not planning_calls


# ── (n) --rehearse --force-mission on two deliverables: two jobs, neither run ──


def test_rehearse_force_mission_on_two_deliverables_yields_two_planned_jobs(
        repo, capsys, monkeypatch):
    from packages.core.models import RunState
    from packages.orchestration.data_paths import job_evidence_dir
    from packages.orchestration.pingpong_job import load_job_plan

    role_builds = count_role_provider_builds(monkeypatch)
    applicator_calls = count_applicator_calls(monkeypatch)
    worktrees_created = count_worktree_creations(monkeypatch)
    before = snapshot_repository_state(repo)

    data = _do_json(capsys, "--rehearse", "--force-mission",
                    order="Write docs/alpha.md and docs/beta.md")

    after = snapshot_repository_state(repo)
    assert (data["shape"], data["shape_source"]) == ("milestones", "--force-mission")
    job_ids = data["job_ids"]
    assert len(job_ids) == 2
    jobs = [load_job_plan(j) for j in job_ids]
    assert [job.state for job in jobs] == [RunState.PLANNED, RunState.PLANNED]
    for job_id in job_ids:
        evidence_dir = job_evidence_dir(job_id)
        assert (evidence_dir / "rehearsal.json").is_file()
        assert (evidence_dir / "rehearsal.md").is_file()
    assert not role_builds
    assert not applicator_calls
    assert not worktrees_created
    assert after == before


# ── (o) a moved repository warns at approval and at run; an unmoved one does not ──


def test_a_moved_repository_warns_at_approval_and_run_an_unmoved_one_does_not(
        repo, capsys, monkeypatch):
    _plan_with_mocked_llm(monkeypatch)

    # Job A: rehearsed, then the repository moves — both the approval and the run warn.
    data_a = _do_json(capsys, "--rehearse", order="Write oa.md and oa2.md")
    [job_a] = data_a["job_ids"]
    (repo / "extra.txt").write_text("more\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "moved")

    main(["decision", "resolve", job_a, "plan:approval", "--reason", "approve"])
    assert "the plan may be stale" in capsys.readouterr().err

    main(["job", "run", job_a, *FAKE_ROLES, "--json"])
    assert "the plan may be stale" in capsys.readouterr().err

    # Job B: rehearsed AFTER the move, with no further commit — neither warns.
    data_b = _do_json(capsys, "--rehearse", order="Write ob.md and ob2.md")
    [job_b] = data_b["job_ids"]

    main(["decision", "resolve", job_b, "plan:approval", "--reason", "approve"])
    assert "the plan may be stale" not in capsys.readouterr().err

    main(["job", "run", job_b, *FAKE_ROLES, "--json"])
    assert "the plan may be stale" not in capsys.readouterr().err


# ── (p) R-1317: job run refuses a rehearsed job whose plan is not approved ──────


def test_job_run_refuses_a_rehearsed_jobs_plan_pending_then_rejected(
        repo, capsys, monkeypatch):
    from packages.core.models import RunState
    from packages.orchestration.pingpong_job import load_job_plan

    _plan_with_mocked_llm(monkeypatch)
    role_builds = count_role_provider_builds(monkeypatch)

    data = _do_json(capsys, "--rehearse", "--force-job", order="Write p.md")
    [job_id] = data["job_ids"]

    with pytest.raises(SystemExit) as exc:
        main(["job", "run", job_id, *FAKE_ROLES, "--json"])
    assert exc.value.code == 3
    out = json.loads(capsys.readouterr().out)
    assert out["ok"] is False
    assert out["error"] == "plan_awaiting_approval"
    assert load_job_plan(job_id).state == RunState.PLANNED
    assert not role_builds

    main(["decision", "resolve", job_id, "plan:approval", "--reason", "reject"])
    capsys.readouterr()

    with pytest.raises(SystemExit) as exc2:
        main(["job", "run", job_id, *FAKE_ROLES, "--json"])
    assert exc2.value.code == 3
    out2 = json.loads(capsys.readouterr().out)
    assert out2["ok"] is False
    assert out2["error"] == "plan_rejected"
    assert load_job_plan(job_id).state == RunState.PLANNED
    assert not role_builds


# ── (q) remedy status labels a waiting rehearsed job, and drops it once it runs ──


def test_status_labels_a_waiting_rehearsed_job_and_drops_the_label_once_it_runs(
        repo, capsys, monkeypatch):
    from packages.orchestration.pingpong_job import JOB_COMPLETED, load_job_plan

    _plan_with_mocked_llm(monkeypatch)

    data = _do_json(capsys, "--rehearse", "--force-job", order="Write q.md")
    [job_id] = data["job_ids"]

    main(["status", "--json"])
    before = json.loads(capsys.readouterr().out)
    entry = next(e for e in before["jobs"]["planned"] if e["job_id"] == job_id)
    assert entry["rehearsed"] is True

    main(["status"])
    text = capsys.readouterr().out
    short = job_id[:8]
    line = next(l for l in text.splitlines() if short in l)
    assert line.rstrip().endswith("(rehearsed)")

    main(["decision", "resolve", job_id, "plan:approval", "--reason", "approve"])
    capsys.readouterr()
    main(["job", "run", job_id, *FAKE_ROLES, "--json"])
    capsys.readouterr()
    assert load_job_plan(job_id).state == JOB_COMPLETED

    main(["status", "--json"])
    after = json.loads(capsys.readouterr().out)
    entry2 = next(e for e in after["jobs"]["completed"] if e["job_id"] == job_id)
    assert entry2["rehearsed"] is False


# ── (r) R-1318: the planning counter, proven to count ───────────────────────


def test_planning_counter_counts_a_real_planning_call(repo, capsys, monkeypatch):
    """`_setup_llm_mocks` replaces `job_plan.plan_job_llm` with its own stub lambda via
    `monkeypatch.setattr` — the same attribute `count_planning_calls` wraps. When the mocks
    install AFTER the counter (as `_plan_with_mocked_llm` does, lazily, inside
    `plan_order_job`), that later setattr wins and overwrites the counting wrapper, so the
    counter never fires and `assert not planning_calls` elsewhere passes for the wrong
    reason. Install the mocks first here, so the counter wraps the already-mocked attribute
    last and nothing re-patches it afterward, and prove it actually counts."""
    from packages.orchestration import do_sequence
    from tests.cli.test_plan_approval import _setup_llm_mocks

    _setup_llm_mocks(monkeypatch, plan_succeeds=True)

    counts = count_planning_calls(monkeypatch)

    real_plan_order_job = do_sequence.plan_order_job
    monkeypatch.setattr(
        do_sequence, "plan_order_job",
        lambda order, **kwargs: real_plan_order_job(order, **{**kwargs, "no_llm": False}))

    _do_json(capsys, "--rehearse", order="Write r1318.md and r1318b.md")

    assert counts["plan_job_llm"] > 0

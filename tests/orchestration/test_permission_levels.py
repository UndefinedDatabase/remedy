"""A fixture per autonomy level, through the real seams, proving the matrix's per-level
differences end to end rather than against its own constant (F141, DECISION F141 D7 (3)).

Each case pins one job at one of `L2` to `L5` under a data root of its own, under `tmp_path`,
then drives the real seam `require_permission`/`require_permissions` is called from —
`apply_permission_refusals`, `confirm_cost_preview`, `build_builder_context` and
`plan_child_spawn` — and asserts the test's OWN literal table of what each level grants, asks
or refuses, never read back from `PERMISSION_MATRIX` itself.
"""
from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from apps.cli.cost_preview_confirm import confirm_cost_preview
from packages.orchestration import config as config_module
from packages.orchestration import pingpong_job as pingpong_job_module
from packages.orchestration.apply_permissions import WRITE_PERMISSION_REFUSED, apply_permission_refusals
from packages.orchestration.autonomy_gate import AUTONOMY_LEVELS
from packages.orchestration.builder_context import build_builder_context
from packages.orchestration.config import load_config
from packages.orchestration.cost_preview import CostBandEstimate
from packages.orchestration.data_paths import job_dir
from packages.orchestration.escalation import escalation_records
from packages.orchestration.exec_guard import ExecGuardPolicy, plan_child_spawn
from packages.orchestration.job_apply import PUSH_REFUSED
from packages.orchestration.permission_matrix import JOB_LEVEL_FILENAME, PERMISSION_GRANTS_FILENAME
from tests.orchestration.test_builder_context import repo  # noqa: F401  (fixture)

UNAVAILABLE = CostBandEstimate(None, None, "estimate_unavailable", {})


def _pin(job_id: str, level: str, root) -> None:
    folder = job_dir(job_id, root)
    folder.mkdir(parents=True, exist_ok=True)
    (folder / JOB_LEVEL_FILENAME).write_text(json.dumps({"level": level}), encoding="utf-8")


def _job(job_id: str) -> SimpleNamespace:
    return SimpleNamespace(job_id=job_id, worktree_branch=f"remedy/{job_id}", metadata={})


def _result(**overrides) -> SimpleNamespace:
    base = {"commit_message_mode": "", "push": False, "status": ""}
    base.update(overrides)
    return SimpleNamespace(**base)


def _grants(root) -> list[dict]:
    path = root / "autonomy" / PERMISSION_GRANTS_FILENAME
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _switch_off(tmp_path):
    project = tmp_path / "remedy.toml"
    project.write_text("[remedy]\nautonomy.allow_push = false\n", encoding="utf-8")
    return load_config(project_path=project, user_path=tmp_path / "none-user.toml")


@pytest.fixture(autouse=True)
def _data_root(tmp_path, monkeypatch):
    """Every case's own data root under `tmp_path`, never the real one."""
    root = tmp_path / "data"
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    return root


# ---------------------------------------------------------------------------
# (a) apply_permission_refusals, late call, a commit message and push
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("level", AUTONOMY_LEVELS, ids=AUTONOMY_LEVELS)
def test_a_apply_grant_lines_differ_by_level(level, _data_root):
    job_id = f"job-a-{level}"
    _pin(job_id, level, _data_root)
    job = SimpleNamespace(job_id=job_id)
    result = _result(commit_message_mode="message", push=True, status="approved_apply_started")

    refusals = apply_permission_refusals(job, result, ["src/app.py"], [])

    assert refusals == []
    actions = [grant["action"] for grant in _grants(_data_root)]
    expected = {
        "L2": ["write_worktree", "commit", "push"],
        "L3": ["write_worktree", "commit", "push"],
        "L4": ["commit", "push"],
        "L5": ["push"],
    }[level]
    assert actions == expected


# ---------------------------------------------------------------------------
# (b) a dependency_change asks a decision below L4, nothing at L4 and L5
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("level", AUTONOMY_LEVELS, ids=AUTONOMY_LEVELS)
def test_b_dependency_change_asks_a_decision_only_below_l4(level, _data_root, monkeypatch):
    monkeypatch.setattr(pingpong_job_module, "save_job_plan", lambda job: None)
    job_id = f"job-b-{level}"
    _pin(job_id, level, _data_root)
    job = _job(job_id)
    result = _result(approved=True, dry_run=False)

    refusals = apply_permission_refusals(job, result, ["pyproject.toml"], [])

    if level in ("L2", "L3"):
        assert len(refusals) == 1
        assert refusals[0].startswith(f"{WRITE_PERMISSION_REFUSED}: ")
        assert len(escalation_records(job)) == 1
    else:
        assert refusals == []
        assert escalation_records(job) == []


# ---------------------------------------------------------------------------
# (c) a destructive migration path asks a decision at every level
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("level", AUTONOMY_LEVELS, ids=AUTONOMY_LEVELS)
def test_c_destructive_migration_asks_a_decision_at_every_level(level, _data_root, monkeypatch):
    monkeypatch.setattr(pingpong_job_module, "save_job_plan", lambda job: None)
    job_id = f"job-c-{level}"
    _pin(job_id, level, _data_root)
    job = _job(job_id)
    result = _result(approved=True, dry_run=False)

    refusals = apply_permission_refusals(job, result, ["app/migrations/0001_init.py"], [])

    assert len(refusals) == 1
    assert refusals[0].startswith(f"{WRITE_PERMISSION_REFUSED}: ")
    assert len(escalation_records(job)) == 1


# ---------------------------------------------------------------------------
# (d) confirm_cost_preview grants expensive below L5, none at L5
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("level", AUTONOMY_LEVELS, ids=AUTONOMY_LEVELS)
def test_d_confirm_cost_preview_grants_expensive_below_l5(level, _data_root):
    job_id = f"job-d-{level}"
    _pin(job_id, level, _data_root)

    proceed = confirm_cost_preview(
        UNAVAILABLE, confirm_above_usd=5.0, yes=True, command_name="job.resume", job_id=job_id,
    )

    assert proceed is True
    grants = [g for g in _grants(_data_root) if g["action"] == "expensive"]
    if level == "L5":
        assert grants == []
    else:
        assert len(grants) == 1
        assert grants[0]["job_id"] == job_id


# ---------------------------------------------------------------------------
# (e) build_builder_context and a networked child grant nothing at any level
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("level", AUTONOMY_LEVELS, ids=AUTONOMY_LEVELS)
def test_e_builder_context_and_networked_child_grant_nothing(level, _data_root, repo):
    job_id = f"job-e-{level}"
    _pin(job_id, level, _data_root)

    build_builder_context(
        repo_path=str(repo), goal="goal", mentioned_files=None,
        compiled_context_paths=None, compiled_context_candidates=None,
        compiled_context_token_budget=None, context_record_dir=None, job_id=job_id,
    )
    plan_child_spawn(ExecGuardPolicy())

    assert _grants(_data_root) == []


# ---------------------------------------------------------------------------
# (f) with the push switch off, (a)'s apply at the first call refuses push at every level
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("level", AUTONOMY_LEVELS, ids=AUTONOMY_LEVELS)
def test_f_push_switch_off_refuses_at_the_first_call_at_every_level(
    level, _data_root, tmp_path, monkeypatch,
):
    monkeypatch.setattr(config_module, "get_config", lambda: _switch_off(tmp_path))
    job_id = f"job-f-{level}"
    _pin(job_id, level, _data_root)
    job = SimpleNamespace(job_id=job_id)
    result = _result(commit_message_mode="message", push=True, status="")

    refusals = apply_permission_refusals(job, result, ["src/app.py"], [])

    assert len(refusals) == 1
    assert refusals[0].startswith(f"{PUSH_REFUSED}: ")
    assert f"(push, {level}) = deny" in refusals[0]
    assert _grants(_data_root) == []

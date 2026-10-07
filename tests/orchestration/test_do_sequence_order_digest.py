"""F295 R11 — a job `remedy do` plans records its order text digest (R-1148, DECISION F295 D10).

`plan_order_job` computes, once, the lowercase hex sha256 of its `mission`
argument's UTF-8 bytes and passes it to each of its three `JobPlan`
constructions as `job_file_sha256` — the LLM plan, the failed LLM plan, and
the deterministic plan. Every digest here is compared with
`hashlib.sha256(<order>.encode("utf-8")).hexdigest()` computed in the test.
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys
from pathlib import Path

import pytest

_CLI = [sys.executable, "-m", "apps.cli.grouped"]


def _git_repo(tmp_path: Path) -> Path:
    """A git repository with one commit, as `tests/cli/test_plan_approval.py` builds it."""
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(repo), "commit", "--allow-empty", "-m", "init", "-q"],
        check=True, capture_output=True,
        env={**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
             "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"},
    )
    return repo


def _env(tmp_path: Path) -> dict:
    return {
        **os.environ,
        "PYTHONPATH": os.getcwd(),
        "REMEDY_DATA_DIR": str(tmp_path / "data"),
    }


def _registered_repo(tmp_path: Path, monkeypatch) -> Path:
    """A git repository registered with `init`, exactly as `test_plan_approval.py` does it."""
    repo = _git_repo(tmp_path)
    env = _env(tmp_path)
    subprocess.run(
        [*_CLI, "init"], capture_output=True, text=True, timeout=30,
        cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
    )
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.chdir(str(repo))
    return repo


def _shape_order(repo: Path, order: str, **kwargs):
    """`plan_order_job` called as `test_plan_approval.py`'s `_shape_order` calls it."""
    from packages.orchestration.do_sequence import plan_order_job
    from packages.orchestration.project_registry import resolve_project

    return plan_order_job(order, project=resolve_project(repo), repo_path=str(repo), **kwargs)


_FAKE_INTAKE_JSON = """{"schema_v": "ji1", "goal": "Test goal.", "context_refs": [], \
"constraints": [], "acceptance_hints": [], "truncated_input": false, "clarifications": []}"""

_FAKE_PLAN_JSON = """{"schema_v": "task_plan_v1", "tasks": [{"id": "T001", \
"title": "Do thing", "goal": "A goal", "acceptance": ["Done"], "depends_on": [], \
"est_tokens_band": "M", "files_hint": []}], "risks": []}"""


def _setup_llm_mocks(monkeypatch, *, plan_succeeds=True):
    """Mock the intake and task-plan LLM branches, copied from `test_plan_approval.py`."""
    def _fake_call(prompt: str, attempt: int) -> str:
        return _FAKE_INTAKE_JSON

    monkeypatch.setattr(
        "packages.orchestration.intake.make_provider_call_fn",
        lambda: _fake_call,
    )

    def _fake_plan_call(prompt: str, attempt: int) -> str:
        return _FAKE_PLAN_JSON

    monkeypatch.setattr(
        "packages.orchestration.intake.make_structured_call_fn",
        lambda model_cls, **kw: _fake_plan_call,
    )

    from packages.orchestration.job_plan import TaskPlanResult
    from packages.orchestration.schemas.models import TaskPlan

    if plan_succeeds:
        _fp = TaskPlan(
            schema_v="task_plan_v1",
            tasks=[{
                "id": "T001", "title": "Do thing", "goal": "A goal",
                "acceptance": ["Done"], "depends_on": [],
                "est_tokens_band": "M", "files_hint": [],
            }],
            risks=[],
        )
        monkeypatch.setattr(
            "packages.orchestration.job_plan.plan_job_llm",
            lambda intake, call_fn, **kw: TaskPlanResult(
                plan=_fp, source="llm", calls=1, transformations=[]),
        )
    else:
        monkeypatch.setattr(
            "packages.orchestration.job_plan.plan_job_llm",
            lambda intake, call_fn, **kw: TaskPlanResult(
                plan=None, source="llm", error_hint="parse failure"),
        )


def test_a_deterministic_plan_records_the_digest_of_its_order_text(tmp_path, monkeypatch):
    from packages.orchestration.pingpong_job import load_job_plan

    repo = _registered_repo(tmp_path, monkeypatch)
    order = "Write a CONTRIBUTING.md"
    expected = hashlib.sha256(order.encode("utf-8")).hexdigest()

    shaped = _shape_order(repo, order, no_llm=True)

    assert shaped.job.job_file_sha256 == expected
    assert load_job_plan(shaped.job.job_id).job_file_sha256 == expected


def test_deterministic_tasks_record_the_digest_of_their_order_text(tmp_path, monkeypatch):
    from packages.orchestration.pingpong_job import load_job_plan
    from packages.orchestration.task_deliverables import deterministic_job_plans

    repo = _registered_repo(tmp_path, monkeypatch)
    order = "Write a CONTRIBUTING.md"
    expected = hashlib.sha256(order.encode("utf-8")).hexdigest()
    [first_plan, *_] = deterministic_job_plans(order)

    shaped = _shape_order(repo, order, no_llm=True, deterministic_tasks=first_plan)

    assert shaped.job.job_file_sha256 == expected
    assert load_job_plan(shaped.job.job_id).job_file_sha256 == expected


def test_an_llm_task_plan_records_the_digest_of_its_order_text(tmp_path, monkeypatch):
    from packages.orchestration.pingpong_job import load_job_plan

    repo = _registered_repo(tmp_path, monkeypatch)
    order = "Write a CONTRIBUTING.md"
    expected = hashlib.sha256(order.encode("utf-8")).hexdigest()
    _setup_llm_mocks(monkeypatch, plan_succeeds=True)

    shaped = _shape_order(repo, order)

    assert shaped.job.job_file_sha256 == expected
    assert load_job_plan(shaped.job.job_id).job_file_sha256 == expected


def test_a_failed_llm_task_plan_leaves_its_job_with_the_digest(tmp_path, monkeypatch):
    import json

    from packages.orchestration.data_paths import job_record_paths
    from packages.orchestration.do_sequence import OrderJobPlanError

    repo = _registered_repo(tmp_path, monkeypatch)
    order = "Write a CONTRIBUTING.md"
    expected = hashlib.sha256(order.encode("utf-8")).hexdigest()
    _setup_llm_mocks(monkeypatch, plan_succeeds=False)

    with pytest.raises(OrderJobPlanError, match="task plan generation failed"):
        _shape_order(repo, order)

    [record_path] = job_record_paths()
    record = json.loads(record_path.read_text(encoding="utf-8"))
    assert record["job_file_sha256"] == expected


def test_the_digest_is_taken_over_the_utf8_bytes_of_the_order(tmp_path, monkeypatch):
    from packages.orchestration.pingpong_job import load_job_plan

    repo = _registered_repo(tmp_path, monkeypatch)
    order = "Schreibe eine ÜBERSICHT.md"
    expected = hashlib.sha256(order.encode("utf-8")).hexdigest()

    shaped = _shape_order(repo, order, no_llm=True)

    assert shaped.job.job_file_sha256 == expected
    assert load_job_plan(shaped.job.job_id).job_file_sha256 == expected

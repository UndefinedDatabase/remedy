"""F2/F3/F13 — the RECORDED invocation controls are the ones the runner actually EXECUTES.

The reviewed build resolved the invocation controls into the persisted ExecutionConfig but then
dispatched the run with the product defaults — so the manifest and the runtime disagreed. These
tests drive the REAL ``run_job()`` and prove, for every invocation control, that three values
agree: the value actually handed to the runtime (``run_pingpong`` / the task limiter), the value
persisted on the JobPlan's ExecutionConfig, and the value recorded in the RunManifest input
definition. They also prove the omission-sentinel resolution (F3): an explicit value overrides a
persisted one even when it equals the product default.
"""
from __future__ import annotations

import pytest

from packages.orchestration import pingpong_loop as PL
from packages.orchestration.pingpong_job import (
    JOB_COMPLETED,
    ExecutionConfig,
    job_evidence_dir,
    load_job_plan,
    parse_job_file,
    run_job,
)
from packages.orchestration.run_manifest import load_latest_manifest_verified

_TWO_TASK_JOB = (
    "# Job: runtime truth\n\n"
    "## Task 1\nDo thing one.\n\nAcceptance:\n- done\n\n"
    "## Task 2\nDo thing two.\n\nAcceptance:\n- done\n"
)


@pytest.fixture
def data_root(tmp_path, monkeypatch):
    root = tmp_path / "remedy_data"
    root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    return root


@pytest.fixture
def repo(tmp_path):
    import subprocess
    r = tmp_path / "repo"
    r.mkdir()
    subprocess.run("git init -q && git config user.email t@t && git config user.name t "
                   "&& echo '# demo' > README.md && git add -A && git commit -qm init",
                   shell=True, cwd=r, check=True)
    return r


def _prov():
    from packages.orchestration.pingpong_provider import FakeProvider
    return FakeProvider(pass_on_round=1, fail_on_round=99)


@pytest.fixture
def spy_run_pingpong(monkeypatch):
    """Record the kwargs each ``run_pingpong`` dispatch actually receives, while delegating to
    the real implementation so the run completes and writes its manifest."""
    calls: list[dict] = []
    real = PL.run_pingpong

    def _spy(*args, **kwargs):
        calls.append(dict(kwargs))
        return real(*args, **kwargs)

    monkeypatch.setattr(PL, "run_pingpong", _spy)
    return calls


def _persist_execution_config(job, **controls):
    job.execution_config = ExecutionConfig(**controls)
    from packages.orchestration.pingpong_job import _persist_job
    _persist_job(job)


def test_persisted_invocation_controls_are_executed_and_recorded(
        data_root, repo, spy_run_pingpong):
    job = parse_job_file(_TWO_TASK_JOB, str(repo))
    # max_tasks=5 (>= the 2 tasks) lets the job COMPLETE and write its manifest; the other
    # controls are the material values whose runtime==config==manifest equality we assert.
    _persist_execution_config(
        job,
        timeout_sec=777, timeout_sec_source="persisted",
        timeout_profile="", timeout_profile_source="persisted",
        max_output_chars=1234, max_output_chars_source="persisted",
        stream_evidence=True, stream_evidence_source="persisted",
        max_tasks=5, max_tasks_source="persisted")

    # No explicit invocation controls on the call → everything resolves from the persisted config.
    done = run_job(job.job_id, builder_provider=_prov(), reviewer_provider=_prov(),
                   repair_rounds=0)
    assert done.status == JOB_COMPLETED

    # --- the runtime dispatch received exactly the persisted values (every task) ---
    assert spy_run_pingpong, "run_pingpong was never dispatched"
    for kw in spy_run_pingpong:
        assert kw["timeout_sec"] == 777
        assert kw["max_output_chars"] == 1234
        assert kw["stream_evidence"] is True
        assert kw["stream_evidence_dir"] is not None      # stream mode is actually on

    # --- the persisted JobPlan config agrees ---
    reloaded = load_job_plan(job.job_id)
    ec = reloaded.execution_config
    assert (ec.timeout_sec, ec.max_output_chars, ec.stream_evidence, ec.max_tasks) == \
           (777, 1234, True, 5)

    # --- the RunManifest input definition agrees ---
    ref = load_latest_manifest_verified(job_evidence_dir(job.job_id), job_id=job.job_id)
    ex = ref.snapshot.job_input["execution"]
    assert ex["timeout_sec"] == 777 and ex["timeout_sec_source"] == "persisted"
    assert ex["max_output_chars"] == 1234
    assert ex["stream_evidence"] is True
    assert ex["max_tasks"] == 5


def test_persisted_max_tasks_actually_caps_the_run(data_root, repo, spy_run_pingpong):
    # F2: persisted max_tasks=1 must limit a 2-task job to a single dispatched task.
    job = parse_job_file(_TWO_TASK_JOB, str(repo))
    _persist_execution_config(job, max_tasks=1, max_tasks_source="persisted")
    run_job(job.job_id, builder_provider=_prov(), reviewer_provider=_prov(), repair_rounds=0)
    assert len(spy_run_pingpong) == 1, "persisted max_tasks=1 did not cap the run"


def test_explicit_default_overrides_persisted_nondefault(data_root, repo, spy_run_pingpong):
    # F3: persisted max_tasks=1, but the caller EXPLICITLY passes max_tasks=0 (the product
    # default). The explicit value must win — both tasks run — proving omission != explicit.
    job = parse_job_file(_TWO_TASK_JOB, str(repo))
    _persist_execution_config(
        job, max_tasks=1, max_tasks_source="persisted",
        stream_evidence=True, stream_evidence_source="persisted")

    run_job(job.job_id, builder_provider=_prov(), reviewer_provider=_prov(),
            repair_rounds=0, max_tasks=0, stream_evidence=False)

    assert len(spy_run_pingpong) == 2, "explicit max_tasks=0 did not override persisted 1"
    assert spy_run_pingpong[0]["stream_evidence"] is False, \
        "explicit stream_evidence=False did not override persisted True"
    reloaded = load_job_plan(job.job_id)
    assert reloaded.execution_config.max_tasks == 0
    assert reloaded.execution_config.max_tasks_source == "invocation"
    assert reloaded.execution_config.stream_evidence_source == "invocation"


def test_explicit_value_equal_to_default_still_counts_as_explicit(
        data_root, repo, spy_run_pingpong):
    # F3: an explicit timeout equal to the product default (120) still resolves as "invocation".
    job = parse_job_file(_TWO_TASK_JOB, str(repo))
    _persist_execution_config(
        job, timeout_sec=777, timeout_sec_source="persisted", max_tasks=1,
        max_tasks_source="persisted")

    run_job(job.job_id, builder_provider=_prov(), reviewer_provider=_prov(),
            repair_rounds=0, timeout_sec=120)

    assert spy_run_pingpong[0]["timeout_sec"] == 120     # explicit default beat persisted 777
    reloaded = load_job_plan(job.job_id)
    assert reloaded.execution_config.timeout_sec == 120
    assert reloaded.execution_config.timeout_sec_source == "invocation"

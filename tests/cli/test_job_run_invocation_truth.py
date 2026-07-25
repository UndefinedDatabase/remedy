"""F1/F2 — the PUBLIC CLI preserves the omission sentinel end to end.

These drive the ACTUAL grouped parser and the ``do job-run`` / ``do job-resume`` command
handlers (not ``run_job()`` directly), and prove that an omitted invocation flag stays ``None``
so a persisted value survives, while an explicit flag — even one equal to the product default —
overrides it. ``run_pingpong`` is spied to capture exactly what the runtime received.
"""
from __future__ import annotations

import subprocess

import pytest

from apps.cli.commands.do_cmd import COMMAND_HANDLERS
from apps.cli.grouped import build_parser
from packages.orchestration import pingpong_loop as PL
from packages.orchestration.pingpong_job import (
    ExecutionConfig,
    _persist_job,
    load_job_plan,
    parse_job_file,
)

_TWO_TASK_JOB = (
    "# Job: cli truth\n\n"
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
    r = tmp_path / "repo"
    r.mkdir()
    subprocess.run("git init -q && git config user.email t@t && git config user.name t "
                   "&& echo '# demo' > README.md && git add -A && git commit -qm init",
                   shell=True, cwd=r, check=True)
    return r


@pytest.fixture
def spy(monkeypatch):
    calls: list[dict] = []
    real = PL.run_pingpong

    def _spy(*args, **kwargs):
        calls.append(dict(kwargs))
        return real(*args, **kwargs)

    monkeypatch.setattr(PL, "run_pingpong", _spy)
    return calls


def _plan(repo, **controls):
    job = parse_job_file(_TWO_TASK_JOB, str(repo))
    job.execution_config = ExecutionConfig(**controls)
    _persist_job(job)
    return job


def _run(argv):
    args = build_parser().parse_args(argv)
    COMMAND_HANDLERS[f"do.{args._subcmd}"](args)


# --------------------------------------------------------------------------- F1


def test_no_flag_job_run_preserves_persisted_controls(data_root, repo, spy):
    job = _plan(repo, timeout_sec=777, timeout_sec_source="persisted",
                max_output_chars=1234, max_output_chars_source="persisted",
                stream_evidence=True, stream_evidence_source="persisted",
                max_tasks=1, max_tasks_source="persisted",
                timeout_profile="patient", timeout_profile_source="persisted")
    _run(["do", "job-run", job.job_id])              # NO invocation flags at all
    # persisted max_tasks=1 → exactly one dispatched task
    assert len(spy) == 1
    kw = spy[0]
    assert kw["timeout_sec"] == 777
    assert kw["max_output_chars"] == 1234
    assert kw["stream_evidence"] is True
    assert kw["timeout_profile"] == "patient"
    ec = load_job_plan(job.job_id).execution_config
    assert (ec.timeout_sec, ec.max_output_chars, ec.stream_evidence, ec.max_tasks) == \
           (777, 1234, True, 1)
    assert ec.max_tasks_source == "persisted"


def test_explicit_max_tasks_zero_overrides_persisted(data_root, repo, spy):
    job = _plan(repo, max_tasks=1, max_tasks_source="persisted")
    _run(["do", "job-run", job.job_id, "--max-tasks", "0"])
    assert len(spy) == 2                              # both tasks ran
    ec = load_job_plan(job.job_id).execution_config
    assert ec.max_tasks == 0 and ec.max_tasks_source == "invocation"


def test_explicit_no_stream_evidence_overrides_persisted_true(data_root, repo, spy):
    job = _plan(repo, stream_evidence=True, stream_evidence_source="persisted",
                max_tasks=1, max_tasks_source="persisted")
    _run(["do", "job-run", job.job_id, "--no-stream-evidence"])
    assert spy[0]["stream_evidence"] is False
    ec = load_job_plan(job.job_id).execution_config
    assert ec.stream_evidence is False and ec.stream_evidence_source == "invocation"


def test_explicit_default_timeout_still_records_invocation(data_root, repo, spy):
    job = _plan(repo, timeout_sec=777, timeout_sec_source="persisted",
                max_tasks=1, max_tasks_source="persisted")
    _run(["do", "job-run", job.job_id, "--timeout-sec", "120"])
    assert spy[0]["timeout_sec"] == 120
    ec = load_job_plan(job.job_id).execution_config
    assert ec.timeout_sec == 120 and ec.timeout_sec_source == "invocation"


def test_persisted_profile_survives_no_flag(data_root, repo, spy):
    job = _plan(repo, timeout_profile="patient", timeout_profile_source="persisted",
                max_tasks=1, max_tasks_source="persisted")
    _run(["do", "job-run", job.job_id])
    assert spy[0]["timeout_profile"] == "patient"
    ec = load_job_plan(job.job_id).execution_config
    assert ec.timeout_profile == "patient"


def test_explicit_normal_profile_overrides_persisted_patient(data_root, repo, spy):
    job = _plan(repo, timeout_profile="patient", timeout_profile_source="persisted",
                max_tasks=1, max_tasks_source="persisted")
    _run(["do", "job-run", job.job_id, "--timeout-profile", "normal"])
    assert spy[0]["timeout_profile"] == "normal"
    ec = load_job_plan(job.job_id).execution_config
    assert ec.timeout_profile == "normal" and ec.timeout_profile_source == "invocation"


# --------------------------------------------------------------------------- F1 resume


def test_job_resume_preserves_omission(data_root, repo, spy):
    # A stopped/resumable job: resume with NO flags must keep the persisted max_tasks cap.
    job = _plan(repo, max_tasks=1, max_tasks_source="persisted")
    _run(["do", "job-run", job.job_id])              # runs task 1, second stays pending
    spy.clear()
    _run(["do", "job-resume", job.job_id])           # no flags
    ec = load_job_plan(job.job_id).execution_config
    assert ec.max_tasks == 1 and ec.max_tasks_source == "persisted"

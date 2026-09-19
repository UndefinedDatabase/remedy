"""The export's explicit verification runs, over one job exported once per module.

This module was the end-to-end regression for the manual-only completion path: a job whose
tasks carried operator-attested evidence was exported, and the export overlaid that evidence.
F273 finding R-0914: an operator repair is attested no longer, and the export's attestation
overlay is deleted with the writer, so the manual-completion assertions went with them. What
stays are the export's verification-run properties, which never depended on the attestation.

Efficiency (finding 7): the job is exported exactly ONCE per module (module-scoped fixture).
A guard test asserts the single export/root-verification execution.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from packages.orchestration.job_evidence import export_job_evidence
from packages.orchestration.pingpong_job import _persist_job, parse_job_file

_REPO_ROOT = Path(__file__).resolve().parents[2]

_THREE_TASK_JOB = """\
# Job: F003 Manual Completion Regression

## Task 1
Core token pipeline.

## Task 2
Final verifier and evidence export.

## Task 3
Packaging and provenance.
"""

_T001_FILES = [
    "packages/orchestration/pingpong_loop.py",
    "packages/orchestration/pingpong_provider.py",
    "packages/orchestration/token_actuals.py",
    "packages/orchestration/token_truth.py",
    "packages/orchestration/f_core_a.py",
    "packages/orchestration/f_core_b.py",
    "tests/orchestration/test_token_actuals.py",
    "tests/orchestration/test_token_truth.py",
    "tests/orchestration/test_pingpong_cli.py",
]  # 9
_T002_FILES = [
    "packages/orchestration/final_verifier.py",
    "tests/orchestration/test_final_verifier.py",
]  # 2
_T003_FILES = [
    "scripts/build_review_manifest.py",
    "scripts/make_review_zip.sh",
    "tests/orchestration/test_change_provenance_gate.py",
]  # 3
_ALL_FILES = _T001_FILES + _T002_FILES + _T003_FILES  # 14

# Module-level instrumentation proving a single export/root-verification run.
_EXPORT_COUNT = {"n": 0}
_RUNNER_CALLS: list[str] = []


def _STUB_RUNNER(command: str) -> dict:
    """Deterministic verification runner — never spawns pytest (finding 3).

    Reports the .py test files named in the command as passed. Fails loudly if
    asked to run this very module (would be recursion in the real runner).
    """
    _RUNNER_CALLS.append(command)
    import shlex
    if "test_manual_completion_bundle" in command:
        raise AssertionError("recursive verification of the running test module")
    files = [t for t in shlex.split(command) if t.endswith(".py")]
    _n_passed = len(files) or 1
    _nids = [f"{f}::test_stub_{i}" for i, f in enumerate(files)] if files else ["stub::test_0"]
    return {
        "exit_code": 0,
        "passed": _n_passed,
        "failed": 0,
        "test_files": files,
        "stdout_summary": "stub-run",
        "node_ids": _nids,
    }


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=str(repo), check=True,
                   capture_output=True, text=True)


def _init_repo(path: Path, seed_pipeline: bool = False) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    (path / "README.md").write_text("base\n")
    if seed_pipeline:
        je = _REPO_ROOT / "packages/orchestration/job_evidence.py"
        dst = path / "packages/orchestration/job_evidence.py"
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(je.read_text(encoding="utf-8"), encoding="utf-8")
    _git(path, "init", "-q")
    _git(path, "config", "user.email", "t@example.com")
    _git(path, "config", "user.name", "Test")
    _git(path, "add", "-A")
    _git(path, "commit", "-q", "-m", "base")
    return path


def _write_files(repo: Path, files: list[str]) -> None:
    for rel in files:
        p = repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if Path(rel).name.startswith("test_"):
            # A trivially passing test so the export's root verification (which
            # runs matching test files from the repo) yields >=1 passed, 0 failed.
            p.write_text("def test_ok():\n    assert True\n")
        else:
            p.write_text(f"# generated content for {rel}\nVALUE = 1\n")


@pytest.fixture(scope="module")
def bundle(tmp_path_factory):
    """Build the job and export it ONCE for the module."""
    tmp_path = tmp_path_factory.mktemp("mc_bundle")
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    import os
    prev = os.environ.get("REMEDY_DATA_DIR")
    os.environ["REMEDY_DATA_DIR"] = str(data_dir)
    try:
        combined = _init_repo(tmp_path / "combined", seed_pipeline=True)
        _write_files(combined, _ALL_FILES)

        job = parse_job_file(_THREE_TASK_JOB, str(combined))
        _persist_job(job)
        per_task = {"T001": _T001_FILES, "T002": _T002_FILES, "T003": _T003_FILES}

        out_dir = tmp_path / "evidence_out"
        _EXPORT_COUNT["n"] += 1
        # Explicit verification commands covering every changed test file, run
        # through an injected deterministic runner (finding 3: no recursive
        # pytest; finding 2: real per-task coverage).
        vcmds = [
            "python3 -m pytest -q " + " ".join(f for f in _T001_FILES if "test_" in f),
            "python3 -m pytest -q " + " ".join(f for f in _T002_FILES if "test_" in f),
            "python3 -m pytest -q " + " ".join(f for f in _T003_FILES if "test_" in f),
        ]
        export_job_evidence(
            job.job_id, str(out_dir),
            verification_commands=vcmds,
            verification_runner=_STUB_RUNNER,
        )
        yield {
            "job_id": job.job_id,
            "out_dir": out_dir,
            "per_task": per_task,
            "verification_commands": vcmds,
        }
    finally:
        if prev is None:
            os.environ.pop("REMEDY_DATA_DIR", None)
        else:
            os.environ["REMEDY_DATA_DIR"] = prev


def _read(out_dir: Path, rel: str) -> dict:
    return json.loads((out_dir / rel).read_text())


# ---------------------------------------------------------------------------
# Efficiency (Finding 7)
# ---------------------------------------------------------------------------

def test_single_export_per_module(bundle):
    assert _EXPORT_COUNT["n"] == 1


# ---------------------------------------------------------------------------
# Finding 3 — no recursion; Finding 4 — dedup
# ---------------------------------------------------------------------------

def test_verification_runs_recorded_with_ids(bundle):
    vt = _read(bundle["out_dir"], "verification_tests.json")
    assert vt["verification_type"] == "explicit_commands"
    run_ids = [r["run_id"] for r in vt["runs"]]
    assert run_ids == ["vr-0001", "vr-0002", "vr-0003"]
    # Top-level totals derived from runs.
    assert vt["passed"] == sum(r["passed"] for r in vt["runs"])
    assert vt["exit_code"] == 0


def test_no_recursive_pytest_invocation(bundle):
    # The injected runner saw exactly our commands; none targeted this module.
    assert bundle["verification_commands"] == _RUNNER_CALLS[:3]
    assert not any("test_manual_completion_bundle" in c for c in _RUNNER_CALLS)


def test_export_without_commands_runs_no_verification(bundle, tmp_path):
    """Finding 3: with no commands and no runner, export must not spawn pytest
    (no verification_tests.json, no recursion)."""
    # Re-export the SAME job with no verification requested.
    out2 = tmp_path / "no_verify"
    export_job_evidence(bundle["job_id"], str(out2))
    assert not (out2 / "verification_tests.json").exists()


def test_shared_root_run_counted_once_not_per_task(bundle):
    """Finding 4: the deduplicated test total equals the sum of unique runs,
    never multiplied by the number of tasks."""
    vt = _read(bundle["out_dir"], "verification_tests.json")
    fv = _read(bundle["out_dir"], "final_verifier_report.json")
    unique_total = sum(r["passed"] for r in vt["runs"])
    assert fv["test_status"]["passed"] == unique_total
    # Not multiplied across the 3 tasks + root.
    assert fv["test_status"]["passed"] != unique_total * len(bundle["per_task"])

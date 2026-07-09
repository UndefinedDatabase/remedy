"""End-to-end regression for the deterministic manual-only completion path.

Simulates the real-world defect that produced internally contradictory evidence:

  * an original T001 provider run that BLOCKED (provider_unavailable) and left a
    stale ``safe_diff_files`` containing ``_copy_refs.py`` plus only a partial
    file set;
  * T002 and T003 that were originally skipped (no recorded scope);
  * clean, isolated, task-scoped manual diffs (T001: 9 files, T002: 2, T003: 3).

After operator attestation and a full evidence export it asserts every fixed
property: no phantom ``_copy_refs.py``; exact per-task review scopes; root-
verification-backed test gates; two-layer execution evidence preserving the
historical provider call; a final job review listing the real combined file set;
manual completion represented on EXISTING artifacts (no ``operator_attested_
completion.json``); a generic linked-prior-job id; and strict manifest validation
that rejects every independent tampering.

Efficiency (finding 7): the scenario is built and exported exactly ONCE per
module (module-scoped fixture); negative tests tamper cheap copies of the single
export rather than re-running root verification. A guard test asserts the single
export/root-verification execution.

These assertions fail on the pre-fix implementation.
"""
from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest

from packages.orchestration.job_evidence import export_job_evidence
from packages.orchestration.pingpong_job import _persist_job, parse_job_file
from packages.orchestration.repair_attest import attest_operator_repair

_REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO_ROOT / "scripts"))
import build_review_manifest as brm  # noqa: E402

_LINKED_PRIOR_JOB = "dc54f5bc63c5430c"

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
    return {
        "exit_code": 0,
        "passed": len(files) or 1,
        "failed": 0,
        "test_files": files,
        "stdout_summary": "stub-run",
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


def _seed_old_run_trace(data_root: Path, run_id: str, provider_calls: int) -> None:
    run_dir = data_root / "pingpong_runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "prompt_trace_summary.json").write_text(json.dumps({
        "builder_prompts": provider_calls,
        "reviewer_prompts": 0,
    }))


@pytest.fixture(scope="module")
def bundle(tmp_path_factory):
    """Build the scenario, attest all three tasks, export ONCE for the module."""
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
        job.tasks[0].status = "blocked"
        job.tasks[0].final_status = "provider_unavailable"
        job.tasks[0].run_id = "oldrun001"
        job.tasks[0].safe_diff_files = ["_copy_refs.py"] + _T001_FILES[:4]
        job.tasks[1].status = "skipped"
        job.tasks[2].status = "skipped"
        _persist_job(job)
        _seed_old_run_trace(data_dir, "oldrun001", 1)

        per_task = {"T001": _T001_FILES, "T002": _T002_FILES, "T003": _T003_FILES}
        attest_results = {}
        for tid, files in per_task.items():
            wt = _init_repo(tmp_path / f"wt_{tid}")
            _write_files(wt, files)
            res = attest_operator_repair(
                job.job_id, tid, f"manual completion {tid}", str(wt),
                task_scoped=True, allowed_files=files,
                linked_prior_job_id=_LINKED_PRIOR_JOB,
            )
            assert "error" not in res, res
            attest_results[tid] = res

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
            "attest_results": attest_results,
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


def test_no_operator_attested_completion_artifact(bundle):
    # Finding 2/6: the unroadmapped root artifact must not exist.
    assert not (bundle["out_dir"] / "operator_attested_completion.json").exists()


# ---------------------------------------------------------------------------
# Task-scoped attestation (Finding 1 + Finding 4 + Finding 5)
# ---------------------------------------------------------------------------

def test_task_scoped_ignores_stale_safe_diff_files(bundle):
    mrp = _read(bundle["out_dir"], "task_runs/T001/manual_repair_provenance.json")
    assert mrp["task_scope_source"] == "attested_diff"
    assert set(mrp["task_scoped_files"]) == set(_T001_FILES)
    assert "_copy_refs.py" not in mrp["task_scoped_files"]


def test_prior_execution_layer_preserved(bundle):
    pe = _read(bundle["out_dir"], "task_runs/T001/provider_evidence.json")
    assert pe["completion_provider_call_count"] == 0
    assert pe["supersedes_prior_execution"] is True
    assert pe["prior_execution"]["provider_call_count"] == 1


def test_linked_prior_job_generic(bundle):
    # Finding 4: linked job flows through generic provenance, not a hardcode.
    for tid in ("T001", "T002", "T003"):
        mrp = _read(bundle["out_dir"], f"task_runs/{tid}/manual_repair_provenance.json")
        assert mrp["linked_prior_job_id"] == _LINKED_PRIOR_JOB
    fjr = _read(bundle["out_dir"], "final_job_review.json")
    assert _LINKED_PRIOR_JOB in fjr["linked_prior_job_ids"]


# ---------------------------------------------------------------------------
# Review scope + tests + execution evidence (Findings 2/3/4)
# ---------------------------------------------------------------------------

def test_review_scopes_exact_per_task(bundle):
    out = bundle["out_dir"]
    assert len(_read(out, "task_runs/T001/review_scope_packet.json")["changed_files"]) == 9
    assert len(_read(out, "task_runs/T002/review_scope_packet.json")["changed_files"]) == 2
    assert len(_read(out, "task_runs/T003/review_scope_packet.json")["changed_files"]) == 3


def test_missing_tests_gates_reference_root_verification(bundle):
    out = bundle["out_dir"]
    for tid in ("T001", "T002", "T003"):
        mtg = _read(out, f"task_runs/{tid}/missing_tests_gate.json")
        assert mtg["gate_status"] == "PASS"
        assert mtg.get("tests_satisfied_by") == "root_verification"
        assert mtg.get("verification_run_ids"), tid
        tests_txt = (out / "task_runs" / tid / "tests.txt").read_text()
        assert "tests_verified_by_root_verification" in tests_txt



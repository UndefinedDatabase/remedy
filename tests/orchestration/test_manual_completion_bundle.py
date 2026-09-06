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

import json
import subprocess
import sys
from pathlib import Path

import pytest

from packages.orchestration import data_paths
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


def _seed_old_run_trace(data_root: Path, run_id: str, provider_calls: int) -> None:
    run_dir = data_paths.run_dir(run_id, data_root)
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


# ---------------------------------------------------------------------------
# Finding 2 — per-task coverage; Finding 3 — no recursion; Finding 4 — dedup
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
    # Re-export the SAME already-attested job with no verification requested.
    out2 = tmp_path / "no_verify"
    export_job_evidence(bundle["job_id"], str(out2))
    assert not (out2 / "verification_tests.json").exists()


def test_task_without_coverage_gets_needs_tests(bundle, tmp_path):
    """Finding 2: a task whose changed tests are not covered by a successful run
    must receive missing_tests_gate = NEEDS_TESTS (no false 'satisfied')."""
    out3 = tmp_path / "partial_cov"
    # Only cover T002/T003; omit T001's tests entirely.
    vcmds = [
        "python3 -m pytest -q " + " ".join(f for f in _T002_FILES if "test_" in f),
        "python3 -m pytest -q " + " ".join(f for f in _T003_FILES if "test_" in f),
    ]
    export_job_evidence(
        bundle["job_id"], str(out3),
        verification_commands=vcmds, verification_runner=_STUB_RUNNER,
    )
    mtg = _read(out3, "task_runs/T001/missing_tests_gate.json")
    assert mtg["gate_status"] == "NEEDS_TESTS"
    assert mtg["uncovered_tests"]
    # And the whole bundle is therefore not authoritative.
    val = brm.validate_evidence_candidate(str(out3))
    fv = _read(out3, "final_verifier_report.json")
    assert fv["verdict"] != "PASS_WITH_RISKS" or val["is_valid_current_run"] is True
    # missing-tests NEEDS_TESTS blocks final verifier from a clean pass:
    assert fv["missing_tests_gate"] == "NEEDS_TESTS"


def test_shared_root_run_counted_once_not_per_task(bundle):
    """Finding 4: the deduplicated test total equals the sum of unique runs,
    never multiplied by the number of tasks."""
    vt = _read(bundle["out_dir"], "verification_tests.json")
    fv = _read(bundle["out_dir"], "final_verifier_report.json")
    unique_total = sum(r["passed"] for r in vt["runs"])
    assert fv["test_status"]["passed"] == unique_total
    # Not multiplied across the 3 tasks + root.
    assert fv["test_status"]["passed"] != unique_total * len(bundle["per_task"])


def test_execution_evidence_two_layers(bundle):
    ev = _read(bundle["out_dir"], "task_runs/T001/task_execution_evidence.json")
    assert ev["completion_provider_call_count"] == 0
    assert ev["prior_execution"]["provider_call_count"] == 1


def test_final_job_review_lists_combined_files(bundle):
    fjr = _read(bundle["out_dir"], "final_job_review.json")
    assert set(fjr["actual_changed_files"]) == set(_ALL_FILES)
    assert set(fjr["expected_changed_files"]) == set(_ALL_FILES)
    assert fjr["completion_mode"] == "manual_operator_repair"
    assert fjr["human_final_reviewer_required"] is True
    assert "_copy_refs.py" not in fjr["actual_changed_files"]


# ---------------------------------------------------------------------------
# Final verifier + manifest authoritative (all findings together)
# ---------------------------------------------------------------------------

def test_final_verifier_pass_with_risks_no_phantom(bundle):
    fv = _read(bundle["out_dir"], "final_verifier_report.json")
    assert fv["verdict"] == "PASS_WITH_RISKS"
    assert fv["human_final_reviewer_required"] is True
    assert set(fv["operator_attested_tasks"]) == {"T001", "T002", "T003"}
    assert "_copy_refs.py" not in fv["authoritative_changed_files"]
    assert fv["review_subject_uncovered_files"] == []
    assert fv["content_hash_mismatches"] == []
    assert fv["file_set_alignment_status"] == "PASS"
    assert set(fv["authoritative_changed_files"]) == set(_ALL_FILES)
    assert fv["token_status"]["actual_available"] is False


def test_manifest_accepts_manual_completion(bundle):
    out = str(bundle["out_dir"])
    assert brm._is_manual_completion(out) is True
    assert brm.validate_manual_completion(out) == []
    validation = brm.validate_evidence_candidate(out)
    assert validation["manual_completion"] is True
    assert validation["is_valid_current_run"] is True, validation["validation_errors"]
    assert validation["manual_completion_errors"] == []
    for art in ("job_flow.json", "agent_run_trace.jsonl",
                "agent_run_trace_summary.json", "command_transcript.json"):
        assert validation["required_root_artifacts"][art] == "not_applicable_manual_completion"
    assert validation["job_id"] == bundle["job_id"]


def test_completion_provider_call_total_zero(bundle):
    truth = _read(bundle["out_dir"], "token_truth.json")
    assert truth["provider_call_count"] == 0
    assert truth["actual_available"] is False


def test_effective_status_on_manifests(bundle):
    # Finding 5: root + task manifests + tasks.json show effective completion.
    out = bundle["out_dir"]
    root = _read(out, "manifest.json")
    assert root["effective_status"] == "operator_attested_complete"
    assert root["evidence_available"] is True
    # Root persisted_status is the persisted JOB status (never mutated).
    assert root["persisted_status"] in ("planned", "blocked", "pending")
    tasks = json.loads((out / "tasks.json").read_text())
    for t in tasks:
        assert t["effective_status"] == "operator_attested_complete"
        assert t["evidence_available"] is True
        assert "persisted_status" in t
    for tid in ("T001", "T002", "T003"):
        tm = _read(out, f"task_runs/{tid}/manifest.json")
        assert tm["evidence_available"] is True
        assert tm["effective_status"] == "operator_attested_complete"
        summary = (out / "task_runs" / tid / "summary.md").read_text()
        assert "Evidence unavailable" not in summary
        assert "operator-attested" in summary.lower()


def test_task_manifest_unavailable_without_effective_rejected(bundle, tmp_path):
    # Finding 5: revert a task manifest to "unavailable" -> bundle rejected.
    def mut(d):
        p = d / "task_runs" / "T001" / "manifest.json"
        j = json.loads(p.read_text())
        j["evidence_available"] = False
        j.pop("effective_status", None)
        p.write_text(json.dumps(j))
    tampered = _tampered_dir(bundle, tmp_path, mut)
    assert brm.validate_manual_completion(tampered)
    assert brm.validate_evidence_candidate(tampered)["is_valid_current_run"] is False


def test_linked_prior_job_summary_present(bundle):
    # Finding 7: summary present, ids match, unknown count is null not 0.
    fjr = _read(bundle["out_dir"], "final_job_review.json")
    summaries = fjr["linked_prior_job_summaries"]
    assert [s["job_id"] for s in summaries] == [_LINKED_PRIOR_JOB]
    s = summaries[0]
    # In the isolated test data root the linked job is not loadable -> honest
    # unknown, NEVER silently zero.
    assert s["status"] == "unknown"
    assert s["provider_call_count"] is None
    assert s["source"] == "unavailable"


def test_observability_index_manual_completion(bundle):
    # Finding 6: index derives from manual artifacts (no job_flow.json).
    import build_observability_index as boi
    idx = boi.build_observability_index(str(bundle["out_dir"]))
    assert idx["job_id"] == bundle["job_id"]
    assert sorted(idx["tasks_generated"]) == ["T001", "T002", "T003"]
    assert set(idx["changed_artifacts"]) == set(_ALL_FILES)
    assert "passed" in idx["tests"]["summary"]
    assert idx["audit"]["status"] == "PASS_WITH_RISKS"
    assert idx["audit"]["human_decision_required"] is True
    assert idx["audit"]["completion_provider_call_count"] == 0
    # No invented provider/prompt traces.
    assert idx["tokens"]["actual_tokens_available"] is False


def test_tampered_linked_summary_rejected(bundle, tmp_path):
    def mut(d):
        _patch_json(d, "final_job_review.json",
                    lambda j: j.update(linked_prior_job_summaries=[
                        {"job_id": "wrongjob", "status": "blocked", "provider_call_count": 1}]))
    tampered = _tampered_dir(bundle, tmp_path, mut)
    assert brm.validate_manual_completion(tampered)
    assert brm.validate_evidence_candidate(tampered)["is_valid_current_run"] is False


# ---------------------------------------------------------------------------
# Finding 3 — strict validation rejects every independent tampering.
# ---------------------------------------------------------------------------

def _tampered_dir(bundle, tmp_path, mutate) -> str:
    """Copy the single exported bundle, apply one mutation, return the path."""
    import shutil
    dst = tmp_path / "tampered"
    shutil.copytree(bundle["out_dir"], dst)
    mutate(dst)
    return str(dst)


def _patch_json(base: Path, rel: str, mutate) -> None:
    p = base / rel
    data = json.loads(p.read_text())
    mutate(data)
    p.write_text(json.dumps(data, indent=2) + "\n")


@pytest.mark.parametrize("name,mutate", [
    ("human_review_flag", lambda d: _patch_json(
        d, "task_runs/T001/review.json", lambda j: j.update(human_final_reviewer_required=False))),
    ("provider_call_count", lambda d: _patch_json(
        d, "task_runs/T001/provider_evidence.json", lambda j: j.update(provider_call_count=1))),
    ("task_id", lambda d: _patch_json(
        d, "task_runs/T001/manual_repair_provenance.json", lambda j: j.update(task_id="T099"))),
    ("task_changed_files", lambda d: _patch_json(
        d, "task_runs/T001/manual_repair_provenance.json",
        lambda j: j.update(changed_files=j["changed_files"][:-1]))),
    ("final_job_union", lambda d: _patch_json(
        d, "final_job_review.json",
        lambda j: j.update(actual_changed_files=j["actual_changed_files"][:-1]))),
    ("root_exit_code", lambda d: _patch_json(
        d, "verification_tests.json", lambda j: j.update(exit_code=1))),
    ("root_failed_count", lambda d: _patch_json(
        d, "verification_tests.json", lambda j: j.update(failed=3))),
    ("content_proof_hash", lambda d: _patch_json(
        d, "current_change_content_proof.json",
        lambda j: j["file_hashes"].pop(next(iter(j["file_hashes"]))))),
    ("job_id", lambda d: _patch_json(
        d, "final_job_review.json", lambda j: j.update(job_id="deadbeefdeadbeef"))),
    ("provenance_hash", lambda d: _patch_json(
        d, "task_runs/T001/manual_repair_provenance.json",
        lambda j: j.update(provenance_sha256="notavalidhash"))),
    ("task_overlap", lambda d: _patch_json(
        d, "task_runs/T002/manual_repair_provenance.json",
        lambda j: j.update(changed_files=j["changed_files"] + _T001_FILES[:1]))),
])
def test_tampered_manual_completion_rejected(bundle, tmp_path, name, mutate):
    tampered = _tampered_dir(bundle, tmp_path, mutate)
    errors = brm.validate_manual_completion(tampered)
    assert errors, f"tampering {name!r} was not rejected"
    validation = brm.validate_evidence_candidate(tampered)
    assert validation["is_valid_current_run"] is False, name


def _rewrite_safe_diff(base: Path, tid: str, transform) -> None:
    p = base / "task_runs" / tid / "safe.diff"
    p.write_text(transform(p.read_text()))


@pytest.mark.parametrize("name,mutate", [
    # Valid-looking but WRONG hashes (not merely malformed strings).
    ("wrong_provenance_sha", lambda d: _patch_json(
        d, "task_runs/T001/manual_repair_provenance.json",
        lambda j: j.update(provenance_sha256="a" * 64))),
    ("wrong_diff_sha", lambda d: _patch_json(
        d, "task_runs/T001/manual_repair_provenance.json",
        lambda j: j.update(diff_sha256="1" * 64))),
    ("wrong_tracked_diff_sha", lambda d: _patch_json(
        d, "task_runs/T001/manual_repair_provenance.json",
        lambda j: j.update(tracked_diff_sha256="b" * 64))),
    ("wrong_safe_diff_sha", lambda d: _patch_json(
        d, "task_runs/T001/manual_repair_provenance.json",
        lambda j: j.update(safe_diff_sha256="c" * 64))),
    # safe.diff content tampering.
    ("safe_diff_one_byte", lambda d: _rewrite_safe_diff(
        d, "T001", lambda s: s + "X")),
    ("safe_diff_empty", lambda d: _rewrite_safe_diff(
        d, "T001", lambda s: "")),
    ("safe_diff_removed_header", lambda d: _rewrite_safe_diff(
        d, "T001", lambda s: "\n".join(
            l for l in s.splitlines() if "token_actuals.py" not in l) + "\n")),
    ("safe_diff_added_header", lambda d: _rewrite_safe_diff(
        d, "T001", lambda s: s + "--- /dev/null\n+++ b/packages/orchestration/sneaky.py\n# x\n")),
    # untracked entry tampering.
    ("untracked_hash", lambda d: _patch_json(
        d, "task_runs/T001/manual_repair_provenance.json",
        lambda j: j["untracked_file_hashes"][0].update(sha256="d" * 64))),
    ("untracked_size", lambda d: _patch_json(
        d, "task_runs/T001/manual_repair_provenance.json",
        lambda j: j["untracked_file_hashes"][0].update(size_bytes=-5))),
    ("task_scoped_list", lambda d: _patch_json(
        d, "task_runs/T001/manual_repair_provenance.json",
        lambda j: j.update(task_scoped_files=j["task_scoped_files"][:-1]))),
])
def test_provenance_hash_tampering_rejected(bundle, tmp_path, name, mutate):
    """Finding 1: recomputed provenance/safe.diff hashes reject valid-looking
    but wrong values and any safe.diff/untracked mutation."""
    tampered = _tampered_dir(bundle, tmp_path, mutate)
    errors = brm.validate_manual_completion(tampered)
    assert errors, f"hash tampering {name!r} was not rejected"
    assert brm.validate_evidence_candidate(tampered)["is_valid_current_run"] is False, name

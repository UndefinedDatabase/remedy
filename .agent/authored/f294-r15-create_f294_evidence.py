#!/usr/bin/env python3
"""Create the evidence job for F294 round 15, the closure sequence's evidence round.

Adapted from F293's `create_f293_evidence.py` (`.agent/authored/f293-r23-create_f293_evidence.py`),
which packaged READY on its first build. The evidence directory, base commit, job id, job title,
step range, feature id, run_id and TEST_FILES are F294's: every python test file the feature added
or edited (the in-process golden path and scoped listings, the run manifest's identity tests, the
data-root isolation test, the acceptance guard, the self-use item's tests and the BLE001 ratchet),
the test files nearest its two production modules (`packages/orchestration/run_manifest.py` and
`apps/cli/commands/dev.py`), the test load governor's test for its `tests/conftest.py` change, plus
the standard closure set this repository's every prior feature packages against (the docs
consistency/source-path/vocabulary guards, the block lint, the two reachability guards of closure
precondition 7, the integrity gate, the ledger rotation guard, the closure cost script, the review
metadata guard and the test runner's own node). Only the standing D3 quarantine is deselected.
Everything else is F293's and load-bearing: node ids from --collect-only, the collected-count
assert, len(node_ids) == selected, sorted test_files, the output_hash over the real pytest output,
the two ancestry counts (closure-protocol pitfall (e)), the unsafe-text red control, and
`validate_verification_tests` over the written document (pitfall (f)).
Run from the repository root at the accepted head: `python3 <this file> [<evidence dir>]`; the
optional argument overrides the evidence directory for a reviewer's dry run.
"""
import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = "020bc9a168783d5a56f2f5aaa9ece76ff359c7aa"
EVIDENCE_DIR = sys.argv[1] if len(sys.argv) > 1 else ".remedy-wt/f294-r15-evidence"
TEST_FILES = sorted([
    "tests/cli/test_golden_path.py",
    "tests/cli/test_scoped_listings.py",
    "tests/docs/test_docs_consistency.py",
    "tests/docs/test_named_source_paths.py",
    "tests/docs/test_vocabulary.py",
    "tests/orchestration/test_autonomy.py",
    "tests/orchestration/test_block_lint.py",
    "tests/orchestration/test_closure_suite_cost.py",
    "tests/orchestration/test_import_reachability.py",
    "tests/orchestration/test_integrity_gate.py",
    "tests/orchestration/test_live_review_rotation.py",
    "tests/orchestration/test_review_gate_sensitive_metadata.py",
    "tests/orchestration/test_run_manifest_integrity.py",
    "tests/orchestration/test_run_manifest_security.py",
    "tests/orchestration/test_test_runner.py",
    "tests/regression/test_f294_acceptance.py",
    "tests/regression/test_named_bugs.py",
    "tests/regression/test_test_load_governor.py",
    "tests/test_ble001_ratchet.py",
    "tests/test_cli_execution_loop_closure.py",
    "tests/test_data_root_isolation.py",
    "tests/test_no_orphan_modules.py",
    "tests/test_repair_context_reviewer_memory.py",
])
#: `not legacy` deselects the standing D3 quarantine; no F294 test needs a deselection by name.
DESELECT = "not legacy"


def git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout.strip()


def main() -> int:
    repo_root = Path(".").resolve()
    sys.path.insert(0, str(repo_root / "scripts"))
    from build_review_manifest import _unsafe_text, validate_evidence_candidate, validate_verification_tests

    head_commit = git("rev-parse", "HEAD")
    ancestry = git("rev-list", "--count", "--ancestry-path", f"{BASE}..{head_commit}")
    plain = git("rev-list", "--count", f"{BASE}..{head_commit}")
    print(f"head {head_commit}\nancestry-path count {ancestry}\nplain count {plain}")
    if ancestry != plain:
        print("ERROR: the two counts differ, so the base is wrong (pitfall (e)); stopping")
        return 1

    collect = subprocess.run(["python3", "-m", "pytest", "--collect-only", "-q", "-k", DESELECT, *TEST_FILES],
                             cwd=repo_root, capture_output=True, text=True, check=False)
    node_ids = [ln.strip() for ln in collect.stdout.split("\n") if ln.startswith("tests/") and "::" in ln]
    collected = re.search(r"(\d+)/(\d+) tests? collected \((\d+) deselected\)", collect.stdout)
    if collected:
        selected, total, deselected = (int(collected.group(i)) for i in (1, 2, 3))
    else:
        plain_count = re.search(r"(\d+) tests? collected", collect.stdout)
        selected = total = int(plain_count.group(1)) if plain_count else -1
        deselected = 0
    if selected != len(node_ids) or not node_ids or selected + deselected != total:
        print(f"ERROR: collect-only count mismatch: {selected}/{total} ({deselected}) vs {len(node_ids)}")
        return 1
    print(f"collected node ids {len(node_ids)}, deselected {deselected}")

    unsafe = [(nid, _unsafe_text(nid)) for nid in node_ids if _unsafe_text(nid) is not None]
    print(f"red control: unsafe among the real ids {len(unsafe)} {unsafe[:3]}")
    print(f"red control: planted id -> {_unsafe_text('tests/x.py::test_a[/home/someone/secret]')}")
    if unsafe:
        return 1

    run = subprocess.run(["python3", "-m", "pytest", "-v", "-k", DESELECT, *TEST_FILES], cwd=repo_root,
                         capture_output=True, text=True, check=False)
    test_output = run.stdout
    counts = {"passed": 0, "failed": 0, "skipped": 0}
    for line in test_output.split("\n")[-15:]:
        for word in counts:
            found = re.search(rf"(\d+) {word}", line)
            if found:
                counts[word] = int(found.group(1))
    output_hash = hashlib.sha256(test_output.encode()).hexdigest()
    print(f"pytest exit {run.returncode}, {counts}, output_hash {output_hash}")

    verification_runs = [{
        "run_id": "vr-1215",
        "command": f"python3 -m pytest -v -k '{DESELECT}' {' '.join(TEST_FILES)}",
        "exit_code": run.returncode,
        "passed": counts["passed"],
        "failed": counts["failed"],
        "skipped": counts["skipped"],
        "selected": len(node_ids),
        "deselected": deselected,
        "test_files": TEST_FILES,
        "node_ids": node_ids,
        "output_hash": output_hash,
        "duration_seconds": 0.0,
        "stdout_summary": f"{counts['passed']} passed",
        "head_sha": head_commit,
    }]

    from packages.orchestration.job_evidence import create_manual_completion_bundle

    evidence_dir = Path(EVIDENCE_DIR).resolve()
    if evidence_dir.exists():
        shutil.rmtree(evidence_dir)
    evidence_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    summary = create_manual_completion_bundle(
        str(evidence_dir),
        repo_root=".",
        base_commit=BASE,
        head_commit=head_commit,
        job_id="f294r15e1001",
        job_title="F294 round 15 evidence job",
        step_range="T002",
        prior_job_ids=[],
        verification_runs=verification_runs,
        timestamp=now.isoformat(timespec="seconds"),
        generated_at=now.isoformat(timespec="microseconds"),
        review_feature_id="f294",
    )

    vt_path = evidence_dir / "verification_tests.json"
    problems, vt_passed = validate_verification_tests(json.loads(vt_path.read_text(encoding="utf-8")))
    print(f"validate_verification_tests problems {problems} passed {vt_passed}")
    validation = validate_evidence_candidate(str(evidence_dir))
    print(f"is_valid_current_run {validation['is_valid_current_run']}")
    print(f"validation_errors {validation['validation_errors']}")
    print("gates written:", sorted(p.name for p in evidence_dir.glob("*_gate.json"))
          + sorted(p.name for p in evidence_dir.glob("final_verifier_report.json")))
    print(json.dumps(summary, indent=2))
    return 0 if not problems and validation["is_valid_current_run"] and run.returncode == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

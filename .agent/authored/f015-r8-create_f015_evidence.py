#!/usr/bin/env python3
"""Create the evidence job for F015 round 8, the closure sequence's evidence half.

Adapted from F267's `create_f267_evidence.py`, which packaged READY on its first build. The
evidence directory, base commit, job id, job title, step range, feature id, run_id and TEST_FILES
are F015's: the tests the feature added, the approval, catalog, exit-code, door and plan tests its
rounds reached, the two files its closure-suite repairs touched, the docs pins its vocabulary and
roadmap edits reach, the two reachability guards of closure precondition 7, and the golden path.
Everything else is F267's and load-bearing: node ids from --collect-only, the collected-count
assert, len(node_ids) == selected, sorted test_files, the output_hash over the real pytest output,
the two ancestry counts (closure-protocol pitfall (e)), the unsafe-text red control, and
`validate_verification_tests` over the written document (pitfall (f)).
SCOPED per pitfall (d): `tests/runtimes/test_supervisor_portability.py` is left out because its
file-URI redaction cases embed local paths by design, and `-k` deselects the parametrized
refusal table of `tests/orchestration/test_plan_editing.py`, whose ids the secret detector reads
as an `sk-` key (`plan_edit_ta` + `sk-args0-...`); both ran green in the committed closure suite,
`.agent/authored/f015-closure-suite.txt`, which the bundle does not replace.
Run from the repository root at the accepted HEAD: `python3 <this file>`.
"""
import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = "fce49ce0789eec07148673ec4e356d28f1eb5fe3"
EVIDENCE_DIR = ".remedy-wt/f015-r8-evidence"
TEST_FILES = sorted([
    "tests/cli/test_exit_codes.py",
    "tests/cli/test_golden_path.py",
    "tests/cli/test_job_plan_cmd.py",
    "tests/cli/test_plan_approval.py",
    "tests/cli/test_real_test_execution_cli.py",
    "tests/docs/test_docs_consistency.py",
    "tests/docs/test_vocabulary.py",
    "tests/orchestration/test_import_reachability.py",
    "tests/orchestration/test_job_plan.py",
    "tests/orchestration/test_plan_edit_execution.py",
    "tests/orchestration/test_plan_editing.py",
    "tests/orchestration/test_roadmap_index.py",
    "tests/test_command_catalog.py",
    "tests/test_no_orphan_modules.py",
    "tests/ui_server/test_command_dispatch.py",
])
DESELECT = "not test_refused_edit_names_the_violation_and_writes_nothing"


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
    if (not collected or int(collected.group(1)) != len(node_ids) or not node_ids
            or int(collected.group(1)) + int(collected.group(3)) != int(collected.group(2))):
        print(f"ERROR: collect-only count mismatch: {collected and collected.group(0)} vs {len(node_ids)}")
        return 1
    deselected = int(collected.group(3))
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
        "run_id": "vr-1048",
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
        job_id="f015r8e1001",
        job_title="F015 round 8 evidence job",
        step_range="T001-T003",
        prior_job_ids=[],
        verification_runs=verification_runs,
        timestamp=now.isoformat(timespec="seconds"),
        generated_at=now.isoformat(timespec="microseconds"),
        review_feature_id="f015",
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
    return 0 if not problems and validation["is_valid_current_run"] else 1


if __name__ == "__main__":
    sys.exit(main())

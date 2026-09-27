#!/usr/bin/env python3
"""Create the evidence job for F028 round 11, the closure sequence's evidence round.

Adapted from F288's `create_f288_evidence.py` (`.agent/authored/f288-r9-create_f288_evidence.py`),
which packaged READY on its first build. The evidence directory, base commit, job id, job title,
step range, feature id, run_id and TEST_FILES are F028's: the python tests the feature added or
edited (the draft pass, the confirmation, the fold, the shortfall answers, the plan edit kind, the
report's origin clause, the command line, the write door, the dashboard's origin, the injection
controls' contracts and the live end-to-end proof) and the guards its modules reach (the event
vocabulary and its humanized catalog, the command catalog and its help, the exit-code guide, the
raw-colour ratchet, the development-artifact boundary, the blind-exception ratchet, the docs pins,
the two reachability guards of closure precondition 7) and the golden path. Everything else is
F288's and load-bearing: node ids from --collect-only, the collected-count assert,
len(node_ids) == selected, sorted test_files, the output_hash over the real pytest output, the two
ancestry counts (closure-protocol pitfall (e)), the unsafe-text red control, and
`validate_verification_tests` over the written document (pitfall (f)). The committed closure suite,
`.agent/authored/f028-closure-suite.txt`, carries the full-suite proof; the bundle does not replace
it. Run from the repository root at the accepted head: `python3 <this file> [<evidence dir>]`; the
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

BASE = "ceb90b8a8304e8ef95490b8f41a5860d061ad5c7"
EVIDENCE_DIR = sys.argv[1] if len(sys.argv) > 1 else ".remedy-wt/f028-r11-evidence"
TEST_FILES = sorted([
    "tests/cli/test_exit_codes.py",
    "tests/cli/test_golden_path.py",
    "tests/cli/test_job_inject.py",
    "tests/docs/test_docs_consistency.py",
    "tests/orchestration/test_development_artifact_boundary.py",
    "tests/orchestration/test_event_names.py",
    "tests/orchestration/test_import_reachability.py",
    "tests/orchestration/test_plan_editing.py",
    "tests/orchestration/test_run_report.py",
    "tests/orchestration/test_task_injection.py",
    "tests/orchestration/test_task_injection_runner.py",
    "tests/test_ble001_ratchet.py",
    "tests/test_command_catalog.py",
    "tests/test_help_renderer.py",
    "tests/test_no_orphan_modules.py",
    "tests/ui_contracts/test_humanize_catalog.py",
    "tests/ui_contracts/test_inject_controls_contract.py",
    "tests/ui_contracts/test_raw_colour_ratchet.py",
    "tests/ui_contracts/test_responsive.py",
    "tests/ui_server/test_command_channel.py",
    "tests/ui_server/test_command_dispatch.py",
    "tests/ui_server/test_dashboard_task_origin.py",
    "tests/ui_server/test_task_injection_e2e_live.py",
])
#: `not legacy` deselects the standing D3 quarantine. Each parenthesised term deselects ONE
#: parametrized case whose own id reads to `_unsafe_text` as a local path or a secret, by design —
#: each proves such a value is refused:
#: `test_a_nonce_that_cannot_be_a_filename_is_400_on_its_own_field`'s `../escape` case and
#: `test_a_bad_reason_is_a_400_on_reason_before_the_job_is_read`'s fake `sk-ant-` key case, the two
#: the reviewer's dry run at `9023b29b` found unsafe and no other, as F027's tool deselected them.
#: Both run, green, in the committed closure suite.
DESELECT = ("not legacy"
            " and not (cannot_be_a_filename_is_400_on_its_own_field and escape)"
            " and not (bad_reason_is_a_400_on_reason and aaaaaaaa)")


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
        "run_id": "vr-0281",
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
        job_id="f028r11e1001",
        job_title="F028 round 11 evidence job",
        step_range="T001-T003",
        prior_job_ids=[],
        verification_runs=verification_runs,
        timestamp=now.isoformat(timespec="seconds"),
        generated_at=now.isoformat(timespec="microseconds"),
        review_feature_id="f028",
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

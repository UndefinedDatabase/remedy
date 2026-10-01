#!/usr/bin/env python3
"""Create the evidence job for F292 round 13, the closure sequence's evidence round.

Adapted from F294's `create_f294_evidence.py` (`.agent/authored/f294-r15-create_f294_evidence.py`),
which packaged READY on its first build. The evidence directory, base commit, job id, job title,
step range, feature id, run_id and TEST_FILES are F292's: every python test file the feature added
or edited (the two UI contracts, the command channel, the dashboard's plan section, the hunk
decisions route and the live end-to-end test in headless Chrome), the test files nearest its
production modules (`apps/cli/commands/job_plan_cmd.py`, `packages/orchestration/plan_editing.py`,
`packages/orchestration/hunk_decision_record.py` and `packages/orchestration/ui_server.py`, with the
palette's contract and the patch command that records hunk decisions), plus the standard closure
set this repository's every prior feature packages against (the docs consistency/source-path/
vocabulary guards, the block lint, the two reachability guards of closure precondition 7, the
integrity gate, the ledger rotation guard, the closure cost script, the review metadata guard and
the test runner's own node). The standing D3 quarantine and one unsafe-named case are deselected.
Everything else is F293's and F294's and load-bearing: node ids from --collect-only, the
collected-count assert, len(node_ids) == selected, sorted test_files, the output_hash over the real
pytest output, the two ancestry counts (closure-protocol pitfall (e)), the unsafe-text red control,
and `validate_verification_tests` over the written document (pitfall (f)).
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

BASE = "2d138e90fe17dfb89e18f9f4cf4a96cf08d417b7"
EVIDENCE_DIR = sys.argv[1] if len(sys.argv) > 1 else ".remedy-wt/f292-r13-evidence"
TEST_FILES = sorted([
    "tests/cli/test_golden_path.py",
    "tests/cli/test_job_plan_cmd.py",
    "tests/cli/test_patch_cmd.py",
    "tests/docs/test_docs_consistency.py",
    "tests/docs/test_named_source_paths.py",
    "tests/docs/test_vocabulary.py",
    "tests/orchestration/test_block_lint.py",
    "tests/orchestration/test_closure_suite_cost.py",
    "tests/orchestration/test_hunk_decision_record.py",
    "tests/orchestration/test_import_reachability.py",
    "tests/orchestration/test_integrity_gate.py",
    "tests/orchestration/test_live_review_rotation.py",
    "tests/orchestration/test_plan_editing.py",
    "tests/orchestration/test_review_gate_sensitive_metadata.py",
    "tests/orchestration/test_test_runner.py",
    "tests/test_no_orphan_modules.py",
    "tests/ui_contracts/test_hunk_decision_contract.py",
    "tests/ui_contracts/test_palette_contract.py",
    "tests/ui_contracts/test_plan_view_contract.py",
    "tests/ui_server/test_command_channel.py",
    "tests/ui_server/test_dashboard_contract.py",
    "tests/ui_server/test_dashboard_plan.py",
    "tests/ui_server/test_hunk_decisions_route.py",
    "tests/ui_server/test_plan_view_live.py",
])
#: `not legacy` deselects the standing D3 quarantine. The parenthesised term deselects ONE
#: parametrized case whose own id reads to `_unsafe_text` as a local path, by design — it proves
#: such a value is refused: `test_a_nonce_that_cannot_be_a_filename_is_400_on_its_own_field`'s
#: `../escape` case, the one the reviewer's dry run at `afa8ebad3` found unsafe and no other, as
#: F029's and F030's tools deselected it. It runs, green, in the committed closure suite.
DESELECT = ("not legacy"
            " and not (cannot_be_a_filename_is_400_on_its_own_field and escape)")


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
        "run_id": "vr-1216",
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
        job_id="f292r13e1001",
        job_title="F292 round 13 evidence job",
        step_range="T001-T003",
        prior_job_ids=[],
        verification_runs=verification_runs,
        timestamp=now.isoformat(timespec="seconds"),
        generated_at=now.isoformat(timespec="microseconds"),
        review_feature_id="f292",
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

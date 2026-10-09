#!/usr/bin/env python3
"""Create the evidence job for F253 round 37, the closure's evidence round on the copied branch.

Adapted from F304's `create_f304_evidence.py` (`.agent/authored/f304-r23-create_f304_evidence.py`),
which packaged READY, by way of F253 round 35's copy, whose bundle was refused only for five
commit subjects (R-1226); this copy differs from F304's in its base commit, round, evidence
directory, job id, job title, step range, feature id, run_id and TEST_FILES.
TEST_FILES are F253's: every python test file the feature added or edited, the guards nearest its
production modules and the ones its closure suite found red, the self-use tests, every file under
`tests/docs/`, plus the standard closure set this repository's every prior feature packages
against. The standing D3 quarantine is deselected, and so are nine test functions whose
parameter ids the packaging scan reads as a local path or a secret (closure-protocol
pitfall (d)); the closure's one full suite, `.agent/authored/f253-closure-suite.txt`, ran
them green.
Everything else is F304's and load-bearing: node ids from --collect-only, the collected-count
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

BASE = "1474a65ea6ed9f8063ce57f5294f9afaf95deee4"
EVIDENCE_DIR = sys.argv[1] if len(sys.argv) > 1 else ".remedy-wt/f253-r37-evidence"
TEST_FILES = sorted([
    "tests/cli/test_advertised_commands.py",
    "tests/cli/test_client_changes_cmd.py",
    "tests/cli/test_client_interface.py",
    "tests/cli/test_client_order_cmd.py",
    "tests/cli/test_client_run_cmd.py",
    "tests/cli/test_command_catalog.py",
    "tests/cli/test_do_flags.py",
    "tests/cli/test_do_order_file.py",
    "tests/cli/test_exit_codes.py",
    "tests/cli/test_golden_path.py",
    "tests/cli/test_job_decline.py",
    "tests/cli/test_job_refusal_envelope.py",
    "tests/cli/test_machine_client_contract.py",
    "tests/cli/test_machine_client_paths.py",
    "tests/cli/test_serve_cmd.py",
    "tests/docs/test_bootstrap_reads_decisions_by_part.py",
    "tests/docs/test_docs_consistency.py",
    "tests/docs/test_environment_guide.py",
    "tests/docs/test_named_source_paths.py",
    "tests/docs/test_operator_questions_shape.py",
    "tests/docs/test_retired_promote_word.py",
    "tests/docs/test_toolchain_refresh_order.py",
    "tests/docs/test_vocabulary.py",
    "tests/orchestration/test_api_clients.py",
    "tests/orchestration/test_block_lint.py",
    "tests/orchestration/test_client_changes.py",
    "tests/orchestration/test_client_digest.py",
    "tests/orchestration/test_closure_suite_cost.py",
    "tests/orchestration/test_decision_queue.py",
    "tests/orchestration/test_durable_write_guard.py",
    "tests/orchestration/test_import_reachability.py",
    "tests/orchestration/test_integrity_gate.py",
    "tests/orchestration/test_live_review_rotation.py",
    "tests/orchestration/test_public_api_gate_paths.py",
    "tests/orchestration/test_review_gate_sensitive_metadata.py",
    "tests/orchestration/test_self_use_findings.py",
    "tests/orchestration/test_self_use_queue.py",
    "tests/orchestration/test_self_use_runner.py",
    "tests/orchestration/test_serve_daemon.py",
    "tests/orchestration/test_serve_paths.py",
    "tests/orchestration/test_serve_runs.py",
    "tests/orchestration/test_test_runner.py",
    "tests/regression/test_named_bugs.py",
    "tests/test_ble001_ratchet.py",
    "tests/test_command_catalog.py",
    "tests/test_data_paths.py",
    "tests/test_data_root_isolation.py",
    "tests/test_no_orphan_modules.py",
    "tests/test_parametrize_ids_stable.py",
    "tests/test_remedy_smoke_script.py",
    "tests/test_reserved_namespaces.py",
    "tests/ui_server/test_command_channel.py",
    "tests/ui_server/test_public_api.py",
])
#: `not legacy` deselects the standing D3 quarantine; the names after it deselect the test
#: functions whose parameter ids the packaging scan reads as a local path or a secret.
_UNSAFE_ID_FUNCTIONS = (
    "test_a_budget_answer_above_a_ceiling_is_refused_naming_its_limit",
    "test_a_budget_answer_inside_the_ceilings_or_outside_the_policy_is_passed_on",
    "test_a_nonce_that_cannot_be_a_filename_is_400_on_its_own_field",
    "test_a_path_value_that_begins_with_a_dash_is_400_and_runs_nothing",
    "test_an_undeclared_key_a_repeated_key_or_a_bad_value_is_400",
    "test_an_unknown_full_id_or_a_value_that_is_no_id_is_run_not_found",
    "test_an_unknown_or_path_shaped_id_is_order_not_found",
    "test_read_order_record_refuses_a_malformed_or_unknown_id",
    "test_the_api_port_answers_every_cockpit_only_path_404",
)
DESELECT = " and ".join(["not legacy", *(f"not {n}" for n in _UNSAFE_ID_FUNCTIONS)])


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
        "run_id": "vr-1254",
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
        job_id="f253r37e1001",
        job_title="F253 round 37 evidence job",
        step_range="T001-T002",
        prior_job_ids=[],
        verification_runs=verification_runs,
        timestamp=now.isoformat(timespec="seconds"),
        generated_at=now.isoformat(timespec="microseconds"),
        review_feature_id="f253",
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

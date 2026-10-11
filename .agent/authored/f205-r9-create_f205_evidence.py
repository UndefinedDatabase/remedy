#!/usr/bin/env python3
"""Create the evidence job for F205 round 9, the closure's evidence round.

Adapted from F302's `.agent/authored/f302-r7-create_f302_evidence.py`, which packaged READY;
this copy differs from it in its base commit, round, evidence directory, job id, job title, step
range, feature id, run_id, TEST_FILES and the deselected functions, taken from F253's evidence.
TEST_FILES are F205's: every python test file the feature added or edited, the guards nearest its
production modules (the mission record and store, the order file, `remedy do` and its project
repository, the loop's dispatch, the upkeep, the client digest and changes, the public API), the
self-use tests, every file under `tests/docs/`, plus the
standard closure set this repository's every prior feature packages against. The standing D3
quarantine is deselected, and so are the three test functions whose parameter ids the packaging
scan reads as a local path. The closure's one full suite, `.agent/authored/f205-closure-suite.txt`,
ran green on the tree that ships.
Everything else is F301's and load-bearing: node ids from --collect-only, the collected-count
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

BASE = "c72d2a7ec7f3784a82e6d61b9cd828dae6714d96"
EVIDENCE_DIR = sys.argv[1] if len(sys.argv) > 1 else ".remedy-wt/f205-r9-evidence"
TEST_FILES = sorted([
    "tests/cli/test_advertised_commands.py",
    "tests/cli/test_client_interface.py",
    "tests/cli/test_command_catalog.py",
    "tests/cli/test_do_commit_flags.py",
    "tests/cli/test_do_order_file.py",
    "tests/cli/test_do_project_repo.py",
    "tests/cli/test_do_sequence_cli.py",
    "tests/cli/test_do_several_projects.py",
    "tests/cli/test_exit_codes.py",
    "tests/cli/test_golden_path.py",
    "tests/cli/test_json_contract.py",
    "tests/cli/test_json_envelope.py",
    "tests/cli/test_machine_client_contract.py",
    "tests/cli/test_mission_cmd.py",
    "tests/cli/test_plan_approval.py",
    "tests/docs/test_bootstrap_reads_decisions_by_part.py",
    "tests/docs/test_docs_consistency.py",
    "tests/docs/test_environment_guide.py",
    "tests/docs/test_named_source_paths.py",
    "tests/docs/test_operator_questions_shape.py",
    "tests/docs/test_retired_promote_word.py",
    "tests/docs/test_toolchain_refresh_order.py",
    "tests/docs/test_vocabulary.py",
    "tests/orchestration/test_block_lint.py",
    "tests/orchestration/test_client_changes.py",
    "tests/orchestration/test_client_digest.py",
    "tests/orchestration/test_closure_suite_cost.py",
    "tests/orchestration/test_dead_command_check.py",
    "tests/orchestration/test_do_sequence.py",
    "tests/orchestration/test_durable_write_guard.py",
    "tests/orchestration/test_import_reachability.py",
    "tests/orchestration/test_integrity_gate.py",
    "tests/orchestration/test_lessons.py",
    "tests/orchestration/test_live_review_rotation.py",
    "tests/orchestration/test_mission_contract.py",
    "tests/orchestration/test_mission_projects.py",
    "tests/orchestration/test_mission_state.py",
    "tests/orchestration/test_mission_upkeep.py",
    "tests/orchestration/test_orchestrator_dispatch.py",
    "tests/orchestration/test_order_file.py",
    "tests/orchestration/test_product_smoke.py",
    "tests/orchestration/test_review_gate_sensitive_metadata.py",
    "tests/orchestration/test_self_use_findings.py",
    "tests/orchestration/test_self_use_queue.py",
    "tests/orchestration/test_self_use_runner.py",
    "tests/orchestration/test_serve_daemon.py",
    "tests/orchestration/test_stream_evidence_integration.py",
    "tests/orchestration/test_structure_measure.py",
    "tests/regression/test_named_bugs.py",
    "tests/test_agent_tooling.py",
    "tests/test_ble001_ratchet.py",
    "tests/test_command_catalog.py",
    "tests/test_data_root_isolation.py",
    "tests/test_grouped_cli.py",
    "tests/test_no_orphan_modules.py",
    "tests/test_parametrize_ids_stable.py",
    "tests/test_remedy_smoke_script.py",
    "tests/test_reserved_namespaces.py",
    "tests/test_structure_ratchet.py",
    "tests/test_subprocess_timeouts.py",
    "tests/ui_server/test_public_api.py",
])
#: `not legacy` deselects the standing D3 quarantine; the names after it deselect the test
#: functions whose parameter ids the packaging scan reads as a local path or a secret, the ones the
#: reviewer's precheck at `801dd494b` found among these files, as F253's evidence did.
_UNSAFE_ID_FUNCTIONS = (
    "test_a_path_value_that_begins_with_a_dash_is_400_and_runs_nothing",
    "test_an_undeclared_key_a_repeated_key_or_a_bad_value_is_400",
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
        "run_id": "vr-1205",
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
        job_id="f205r9e1001",
        job_title="F205 round 9 evidence job",
        step_range="T001-T002",
        prior_job_ids=[],
        verification_runs=verification_runs,
        timestamp=now.isoformat(timespec="seconds"),
        generated_at=now.isoformat(timespec="microseconds"),
        review_feature_id="f205",
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

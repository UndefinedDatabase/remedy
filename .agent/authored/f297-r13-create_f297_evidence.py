#!/usr/bin/env python3
"""Create the evidence job for F297 round 13, the closure's evidence round.

Adapted from F205's `.agent/authored/f205-r9-create_f205_evidence.py`, which packaged READY;
this copy differs from it in its base commit, round, evidence directory, job id, job title, step
range, feature id, run_id, TEST_FILES and the deselected functions. TEST_FILES are F297's: every
python test file the feature added or edited since its fork point, every file under `tests/docs/`,
plus F205's set, the standard closure set this repository's every prior feature packages against.
The base is the fork point `9dab4d7f0`, not a merge base, because the branch merged `main` in at
F297 R12 C2 (closure-protocol pitfall (e)). The standing D3 quarantine is deselected, and so are
the test functions whose parameter ids the packaging scan reads as a local path, which the
reviewer's precheck at `6ff218bd2` found. The closure's one full suite,
`.agent/authored/f297-closure-suite.txt`, ran green on the tree that ships.
Everything else is F205's and load-bearing: node ids from --collect-only, the collected-count
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

BASE = "9dab4d7f01f9574f23cf637861f74222107fcb21"
EVIDENCE_DIR = sys.argv[1] if len(sys.argv) > 1 else ".remedy-wt/f297-r13-evidence"
TEST_FILES = sorted([
    "tests/cli/test_advertised_commands.py",
    "tests/cli/test_client_interface.py",
    "tests/cli/test_command_catalog.py",
    "tests/cli/test_decision_cmd.py",
    "tests/cli/test_do_commit_flags.py",
    "tests/cli/test_do_flags.py",
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
    "tests/cli/test_quick_start.py",
    "tests/cli/test_status_cmd.py",
    "tests/docs/test_bootstrap_reads_decisions_by_part.py",
    "tests/docs/test_docs_consistency.py",
    "tests/docs/test_environment_guide.py",
    "tests/docs/test_named_source_paths.py",
    "tests/docs/test_operator_questions_shape.py",
    "tests/docs/test_retired_promote_word.py",
    "tests/docs/test_toolchain_refresh_order.py",
    "tests/docs/test_vocabulary.py",
    "tests/orchestration/test_block_lint.py",
    "tests/orchestration/test_ci_workflow.py",
    "tests/orchestration/test_claude_cli_resume.py",
    "tests/orchestration/test_client_changes.py",
    "tests/orchestration/test_client_digest.py",
    "tests/orchestration/test_closure_suite_cost.py",
    "tests/orchestration/test_dead_command_check.py",
    "tests/orchestration/test_do_sequence.py",
    "tests/orchestration/test_do_sequence_order_digest.py",
    "tests/orchestration/test_dod_runners.py",
    "tests/orchestration/test_durable_write_guard.py",
    "tests/orchestration/test_evidence_bundle.py",
    "tests/orchestration/test_import_reachability.py",
    "tests/orchestration/test_integrity_gate.py",
    "tests/orchestration/test_job_burn.py",
    "tests/orchestration/test_job_stop_integration.py",
    "tests/orchestration/test_lessons.py",
    "tests/orchestration/test_live_review_rotation.py",
    "tests/orchestration/test_mission_contract.py",
    "tests/orchestration/test_mission_projects.py",
    "tests/orchestration/test_mission_state.py",
    "tests/orchestration/test_mission_upkeep.py",
    "tests/orchestration/test_orchestrator_dispatch.py",
    "tests/orchestration/test_order_file.py",
    "tests/orchestration/test_order_shape_repair.py",
    "tests/orchestration/test_pingpong_cli.py",
    "tests/orchestration/test_product_smoke.py",
    "tests/orchestration/test_project_brain.py",
    "tests/orchestration/test_project_tests.py",
    "tests/orchestration/test_repo_mission.py",
    "tests/orchestration/test_resume_cli.py",
    "tests/orchestration/test_review_gate_sensitive_metadata.py",
    "tests/orchestration/test_self_use_findings.py",
    "tests/orchestration/test_self_use_generator.py",
    "tests/orchestration/test_self_use_queue.py",
    "tests/orchestration/test_self_use_runner.py",
    "tests/orchestration/test_serve_daemon.py",
    "tests/orchestration/test_serve_runs.py",
    "tests/orchestration/test_stream_evidence_integration.py",
    "tests/orchestration/test_structure_measure.py",
    "tests/orchestration/test_veto_proposal.py",
    "tests/regression/test_named_bugs.py",
    "tests/regression/test_test_load_governor.py",
    "tests/test_agent_tooling.py",
    "tests/test_ble001_ratchet.py",
    "tests/test_cli_main.py",
    "tests/test_command_catalog.py",
    "tests/test_data_root_isolation.py",
    "tests/test_grouped_cli.py",
    "tests/test_no_orphan_modules.py",
    "tests/test_parametrize_ids_stable.py",
    "tests/test_project_constitution.py",
    "tests/test_remedy_smoke_script.py",
    "tests/test_reserved_namespaces.py",
    "tests/test_structure_ratchet.py",
    "tests/test_subprocess_timeouts.py",
    "tests/test_timeline.py",
    "tests/ui_server/test_public_api.py",
])
#: `not legacy` deselects the standing D3 quarantine; the names after it deselect the test
#: functions whose parameter ids the packaging scan reads as a local path or a secret, the ones the
#: reviewer's precheck at `6ff218bd2` found among these files, as F205's evidence did.
_UNSAFE_ID_FUNCTIONS = (
    "test_a_path_value_that_begins_with_a_dash_is_400_and_runs_nothing",
    "test_an_undeclared_key_a_repeated_key_or_a_bad_value_is_400",
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
        "run_id": "vr-1297",
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
        job_id="f297r13e1001",
        job_title="F297 round 13 evidence job",
        step_range="T001-T025",
        prior_job_ids=[],
        verification_runs=verification_runs,
        timestamp=now.isoformat(timespec="seconds"),
        generated_at=now.isoformat(timespec="microseconds"),
        review_feature_id="f297",
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

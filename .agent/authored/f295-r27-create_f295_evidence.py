#!/usr/bin/env python3
"""Create the evidence job for F295 round 27, the closure sequence's evidence round.

Adapted from F294's `create_f294_evidence.py` (`.agent/authored/f294-r15-create_f294_evidence.py`),
which packaged READY on its first build. The evidence directory, base commit, job id, job title,
step range, feature id, run_id and TEST_FILES are F295's: every python test file the feature added
or edited (the order file, the client digest, the budget decision, the gate test and the contract
page's test, and the commands they reach), the test files nearest its production modules (the
checkpoints, `remedy do`'s sequence, the job apply and digest, the ping-pong job, the project
cockpit, the proof chain, the stream evidence and the decision and job commands), every file under
`tests/docs/`, the self-use queue's own tests, plus the standard closure set this repository's
every prior feature packages against (the block lint, the two reachability guards of closure
precondition 7, the integrity gate, the ledger rotation guard, the closure cost script, the review
metadata guard, the named-bugs regression file and the test runner's own node). The standing D3
quarantine and the redaction cases whose ids carry secret shapes are deselected.
Everything else is F294's, F293's and F290's and load-bearing: node ids from --collect-only, the
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

BASE = "9a8431ea9c8f930d56e42671e4599c7cd94cb78b"
EVIDENCE_DIR = sys.argv[1] if len(sys.argv) > 1 else ".remedy-wt/f295-r27-evidence"
TEST_FILES = sorted([
    "tests/cli/test_change_proof_cli.py",
    "tests/cli/test_command_catalog.py",
    "tests/cli/test_cost_preview_confirm.py",
    "tests/cli/test_decision_answers.py",
    "tests/cli/test_decision_cmd.py",
    "tests/cli/test_do_cmd_summary.py",
    "tests/cli/test_do_flags.py",
    "tests/cli/test_do_order_file.py",
    "tests/cli/test_do_sequence_cli.py",
    "tests/cli/test_exit_codes.py",
    "tests/cli/test_golden_path.py",
    "tests/cli/test_job_commands.py",
    "tests/cli/test_job_refusal_envelope.py",
    "tests/cli/test_machine_client_contract.py",
    "tests/cli/test_patch_cmd.py",
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
    "tests/orchestration/test_budget_decision.py",
    "tests/orchestration/test_checkpoints.py",
    "tests/orchestration/test_client_digest.py",
    "tests/orchestration/test_closure_suite_cost.py",
    "tests/orchestration/test_decision_inbox.py",
    "tests/orchestration/test_do_sequence.py",
    "tests/orchestration/test_do_sequence_order_digest.py",
    "tests/orchestration/test_exec_guard.py",
    "tests/orchestration/test_import_reachability.py",
    "tests/orchestration/test_integrity_gate.py",
    "tests/orchestration/test_job_apply.py",
    "tests/orchestration/test_job_digest.py",
    "tests/orchestration/test_live_review_rotation.py",
    "tests/orchestration/test_mission_contract.py",
    "tests/orchestration/test_order_file.py",
    "tests/orchestration/test_pingpong_job_dod_gate.py",
    "tests/orchestration/test_pingpong_job_hunk_ledger.py",
    "tests/orchestration/test_pingpong_job_ownership.py",
    "tests/orchestration/test_project_cockpit.py",
    "tests/orchestration/test_proof_chain.py",
    "tests/orchestration/test_resume_cli.py",
    "tests/orchestration/test_review_gate_sensitive_metadata.py",
    "tests/orchestration/test_self_use_queue.py",
    "tests/orchestration/test_stream_evidence.py",
    "tests/orchestration/test_stream_evidence_integration.py",
    "tests/orchestration/test_test_runner.py",
    "tests/regression/test_named_bugs.py",
    "tests/test_ble001_ratchet.py",
    "tests/test_command_catalog.py",
    "tests/test_no_orphan_modules.py",
])
#: `not legacy` deselects the standing D3 quarantine. The two further terms deselect the
#: parametrized redaction cases of `tests/orchestration/test_stream_evidence.py` whose own ids
#: carry secret-shaped strings that `_unsafe_text` reads as a secret, by design — each proves such a
#: value is redacted (closure-protocol pitfall (d)).
DESELECT = ("not legacy"
            " and not test_secret_shapes_redacted"
            " and not test_sk_key_at_token_boundary_redacted")


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
        "run_id": "vr-1295",
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
        job_id="f295r27e1001",
        job_title="F295 round 27 evidence job",
        step_range="T001-T004",
        prior_job_ids=[],
        verification_runs=verification_runs,
        timestamp=now.isoformat(timespec="seconds"),
        generated_at=now.isoformat(timespec="microseconds"),
        review_feature_id="f295",
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

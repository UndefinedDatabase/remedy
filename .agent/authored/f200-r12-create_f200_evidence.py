#!/usr/bin/env python3
"""Create the evidence job for F200 round 12, the closure sequence's evidence round.

Adapted from F292's `create_f292_evidence.py` (`.agent/authored/f292-r13-create_f292_evidence.py`),
which packaged READY on its first build. The evidence directory, base commit, job id, job title,
step range, feature id, run_id and TEST_FILES are F200's: every python test file the feature added
or edited (the serve command, the client's parity and scope, the supervisor, its paths, its runs,
its restart under SIGKILL, its STOP file and its artifacts, the command-line help and exit codes),
the test files nearest its production modules (`apps/cli/command_catalog.py`,
`apps/cli/commands/do_cmd.py`, `apps/cli/commands/job_pause_cmd.py`,
`apps/cli/commands/job_stop_cmd.py`, `packages/orchestration/config.py`,
`packages/orchestration/data_paths.py`, `packages/orchestration/pause_control.py` and
`packages/orchestration/ui_server.py`, with the environment registry), every file under
`tests/docs/`, plus the standard closure set this repository's every prior feature packages against
(the block lint, the two reachability guards of closure precondition 7, the integrity gate, the
ledger rotation guard, the closure cost script, the review metadata guard and the test runner's own
node). The standing D3 quarantine and one unsafe-named case are deselected.
Everything else is F293's, F294's and F292's and load-bearing: node ids from --collect-only, the
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

BASE = "959b88a8577a218435e9d775d81446c83b5835f5"
EVIDENCE_DIR = sys.argv[1] if len(sys.argv) > 1 else ".remedy-wt/f200-r12-evidence"
TEST_FILES = sorted([
    "tests/cli/test_cli_ux.py",
    "tests/cli/test_command_catalog.py",
    "tests/cli/test_exit_codes.py",
    "tests/cli/test_golden_path.py",
    "tests/cli/test_job_pause.py",
    "tests/cli/test_job_run_invocation_truth.py",
    "tests/cli/test_job_stop.py",
    "tests/cli/test_serve_client_parity.py",
    "tests/cli/test_serve_client_scope.py",
    "tests/cli/test_serve_cmd.py",
    "tests/docs/test_bootstrap_reads_decisions_by_part.py",
    "tests/docs/test_docs_consistency.py",
    "tests/docs/test_environment_guide.py",
    "tests/docs/test_named_source_paths.py",
    "tests/docs/test_operator_questions_shape.py",
    "tests/docs/test_retired_promote_word.py",
    "tests/docs/test_toolchain_refresh_order.py",
    "tests/docs/test_vocabulary.py",
    "tests/orchestration/test_block_lint.py",
    "tests/orchestration/test_closure_suite_cost.py",
    "tests/orchestration/test_config.py",
    "tests/orchestration/test_env_registry.py",
    "tests/orchestration/test_import_reachability.py",
    "tests/orchestration/test_integrity_gate.py",
    "tests/orchestration/test_job_stop_integration.py",
    "tests/orchestration/test_live_review_rotation.py",
    "tests/orchestration/test_pause_control.py",
    "tests/orchestration/test_review_gate_sensitive_metadata.py",
    "tests/orchestration/test_serve_artifacts.py",
    "tests/orchestration/test_serve_daemon.py",
    "tests/orchestration/test_serve_paths.py",
    "tests/orchestration/test_serve_restart_kill.py",
    "tests/orchestration/test_serve_runs.py",
    "tests/orchestration/test_serve_stop_file.py",
    "tests/orchestration/test_test_runner.py",
    "tests/test_command_catalog.py",
    "tests/test_data_paths.py",
    "tests/test_no_orphan_modules.py",
    "tests/ui_server/test_command_channel.py",
])
#: `not legacy` deselects the standing D3 quarantine. The two parenthesised terms deselect the
#: parametrized cases whose own ids read to `_unsafe_text` as a local path, by design — each proves
#: such a value is refused: `test_a_nonce_that_cannot_be_a_filename_is_400_on_its_own_field`'s
#: `../escape` case, as F029's, F030's and F292's tools deselected it, and the `../etc` case of
#: `test_a_malformed_job_id_is_a_usage_error` in `tests/cli/test_job_pause.py` and
#: `tests/cli/test_job_stop.py`, the cases the reviewer's dry run on base `2ebf3e3b4` found unsafe
#: and no other. Each runs, green, in the committed closure suite.
DESELECT = ("not legacy"
            " and not (cannot_be_a_filename_is_400_on_its_own_field and escape)"
            " and not (a_malformed_job_id_is_a_usage_error and etc)")


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
        "run_id": "vr-1217",
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
        job_id="f200r12e1001",
        job_title="F200 round 12 evidence job",
        step_range="T001-T002",
        prior_job_ids=[],
        verification_runs=verification_runs,
        timestamp=now.isoformat(timespec="seconds"),
        generated_at=now.isoformat(timespec="microseconds"),
        review_feature_id="f200",
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

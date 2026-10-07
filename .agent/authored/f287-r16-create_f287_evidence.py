#!/usr/bin/env python3
"""Create the evidence job for F287 round 16, the closure sequence's evidence round, run again.

Adapted from F295's `create_f295_evidence.py` (`.agent/authored/f295-r27-create_f295_evidence.py`),
which packaged READY on its first build, as did F287's own round 14 copy
(`.agent/authored/f287-r14-create_f287_evidence.py`), whose package round 15's docs repair
outdated; this copy differs from that one only in its round, evidence directory, job id,
job title and run_id. The evidence directory, base commit, job id, job title,
step range, feature id, run_id, TEST_FILES and the deselection are F287's: every python test file
the feature added or edited (the `claude-cli` resume, the relaunch through `run_job`, the persisted
session fields and the command-line relaunch), the test files nearest its two production modules
(`pingpong_provider.py` and `pingpong_loop.py`: the provider tests, the ping-pong loop, the
pause, stop and resume paths, the repair loop and the prompt dedupe that a resumed session turns
on, and the job commands), the self-use queue, findings and runner tests, every file under
`tests/docs/`, plus the standard closure set this repository's every prior feature packages
against (the block lint, the two reachability guards of closure precondition 7, the integrity
gate, the ledger rotation guard, the closure cost script, the review metadata guard, the
named-bugs regression file and the test runner's own node). The standing D3 quarantine and the
provider test whose ids carry a secret-shaped API key are deselected.
Everything else is F295's, F294's and F290's and load-bearing: node ids from --collect-only, the
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

BASE = "7c91c3b6984510370d9b0d909039781df1c17aeb"
EVIDENCE_DIR = sys.argv[1] if len(sys.argv) > 1 else ".remedy-wt/f287-r16-evidence"
TEST_FILES = sorted([
    "tests/cli/test_command_catalog.py",
    "tests/cli/test_exit_codes.py",
    "tests/cli/test_golden_path.py",
    "tests/cli/test_job_commands.py",
    "tests/cli/test_job_run_session_resume.py",
    "tests/cli/test_job_show.py",
    "tests/docs/test_bootstrap_reads_decisions_by_part.py",
    "tests/docs/test_docs_consistency.py",
    "tests/docs/test_environment_guide.py",
    "tests/docs/test_named_source_paths.py",
    "tests/docs/test_operator_questions_shape.py",
    "tests/docs/test_retired_promote_word.py",
    "tests/docs/test_toolchain_refresh_order.py",
    "tests/docs/test_vocabulary.py",
    "tests/orchestration/test_block_lint.py",
    "tests/orchestration/test_builder_prompt_golden.py",
    "tests/orchestration/test_claude_cli_exec_guard.py",
    "tests/orchestration/test_claude_cli_failure_detail.py",
    "tests/orchestration/test_claude_cli_resume.py",
    "tests/orchestration/test_closure_suite_cost.py",
    "tests/orchestration/test_import_reachability.py",
    "tests/orchestration/test_integrity_gate.py",
    "tests/orchestration/test_job_stop_integration.py",
    "tests/orchestration/test_live_review_rotation.py",
    "tests/orchestration/test_pause_resume.py",
    "tests/orchestration/test_pingpong.py",
    "tests/orchestration/test_pingpong_integration.py",
    "tests/orchestration/test_pingpong_provider_claude_api.py",
    "tests/orchestration/test_pingpong_provider_ollama.py",
    "tests/orchestration/test_provider_evidence_integration.py",
    "tests/orchestration/test_provider_retry.py",
    "tests/orchestration/test_relaunch_session_resume.py",
    "tests/orchestration/test_repair_loop.py",
    "tests/orchestration/test_resume_cli.py",
    "tests/orchestration/test_review_gate_sensitive_metadata.py",
    "tests/orchestration/test_reviewer_prompt_golden.py",
    "tests/orchestration/test_self_use_findings.py",
    "tests/orchestration/test_self_use_queue.py",
    "tests/orchestration/test_self_use_runner.py",
    "tests/orchestration/test_semantic_dedupe.py",
    "tests/orchestration/test_session_resume.py",
    "tests/orchestration/test_test_runner.py",
    "tests/orchestration/test_worktree_resume_cli.py",
    "tests/regression/test_named_bugs.py",
    "tests/test_ble001_ratchet.py",
    "tests/test_command_catalog.py",
    "tests/test_no_orphan_modules.py",
])
#: `not legacy` deselects the standing D3 quarantine. The further term deselects the parametrized
#: case of `tests/orchestration/test_pingpong_provider_claude_api.py` whose own id carries a
#: secret-shaped API key that `_unsafe_text` reads as a secret, by design — it proves such a key
#: never reaches the error text (closure-protocol pitfall (d)).
DESELECT = ("not legacy"
            " and not test_no_key_reaches_the_error_text")


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
        "run_id": "vr-1288",
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
        job_id="f287r16e1001",
        job_title="F287 round 16 evidence job",
        step_range="T001-T003",
        prior_job_ids=[],
        verification_runs=verification_runs,
        timestamp=now.isoformat(timespec="seconds"),
        generated_at=now.isoformat(timespec="microseconds"),
        review_feature_id="f287",
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

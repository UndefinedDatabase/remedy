#!/usr/bin/env python3
"""Create the evidence job for F027 round 13, the closure sequence's evidence round.

Adapted from F026's `create_f026_evidence.py` (`.agent/authored/f026-r7-create_f026_evidence.py`),
which packaged READY on its first build. The evidence directory, base commit, job id, job title,
step range, feature id, run_id and TEST_FILES are F027's: the python tests the feature added (the
veto control protocol, the linear runner's and the cycle executor's folds, the replan proposal, the
CLI verb, the dashboard's `vetoes` section, the page's contract guard, the live end-to-end) and those
it edited or reached (the decision CLI, inbox and evidence, the event names, the manifest's
expectation tables, the worktree restore, the door's dispatch and channel, the pause door's live
test, the catalog, the exit codes, the semantic zoom wiring, the event catalog), the UI toolchain
nodes that run eslint, tsc and the whole vitest suite (`test_ui_lint.py`,
`test_dashboard_contract.py`, `test_test_runner.py`), where every one of F027's TypeScript tests
runs, the drift, colour and glyph guards its page edits reach, the docs pins and the vocabulary
guard, the two reachability guards of closure precondition 7, and the golden path. `-k` deselects
the standing D3 quarantine and the parametrized cases named beside DESELECT. Everything else is
F019's and load-bearing: node ids from --collect-only, the collected-count assert,
len(node_ids) == selected, sorted test_files, the output_hash over the real pytest output, the two
ancestry counts (closure-protocol pitfall (e)), the unsafe-text red control, and
`validate_verification_tests` over the written document (pitfall (f)). The committed closure suite,
`.agent/authored/f027-closure-suite.txt`, carries the full-suite proof; the bundle does not replace it.
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

BASE = "557cbbcc5f5f0a46bf6d9c90b971b2723657d651"
EVIDENCE_DIR = sys.argv[1] if len(sys.argv) > 1 else ".remedy-wt/f027-r13-evidence"
TEST_FILES = sorted([
    "tests/cli/test_decision_cmd.py",
    "tests/cli/test_exit_codes.py",
    "tests/cli/test_golden_path.py",
    "tests/cli/test_job_veto.py",
    "tests/docs/test_docs_consistency.py",
    "tests/docs/test_vocabulary.py",
    "tests/orchestration/test_decision_evidence.py",
    "tests/orchestration/test_decision_inbox.py",
    "tests/orchestration/test_event_names.py",
    "tests/orchestration/test_import_reachability.py",
    "tests/orchestration/test_task_expectation_episode_context.py",
    "tests/orchestration/test_task_expectation_status_truth.py",
    "tests/orchestration/test_task_veto.py",
    "tests/orchestration/test_task_veto_cycles.py",
    "tests/orchestration/test_task_veto_runner.py",
    "tests/orchestration/test_test_runner.py",
    "tests/orchestration/test_veto_proposal.py",
    "tests/orchestration/test_worktrees.py",
    "tests/test_command_catalog.py",
    "tests/test_no_orphan_modules.py",
    "tests/ui_contracts/test_design_drift.py",
    "tests/ui_contracts/test_humanize_catalog.py",
    "tests/ui_contracts/test_node_glyph_tokens.py",
    "tests/ui_contracts/test_raw_colour_ratchet.py",
    "tests/ui_contracts/test_semantic_zoom_wiring.py",
    "tests/ui_contracts/test_ui_lint.py",
    "tests/ui_contracts/test_veto_controls_contract.py",
    "tests/ui_server/test_command_channel.py",
    "tests/ui_server/test_command_dispatch.py",
    "tests/ui_server/test_dashboard_contract.py",
    "tests/ui_server/test_dashboard_vetoes.py",
    "tests/ui_server/test_pause_door_live.py",
    "tests/ui_server/test_task_veto_e2e_live.py",
])
#: `not legacy` deselects the standing D3 quarantine. Each parenthesised term deselects ONE
#: parametrized case whose own id reads to `_unsafe_text` as a local path or a secret, by design —
#: each proves such a value is refused: `test_an_unsupported_status_blocks`'s `../evil` case,
#: `test_unsafe_job_ids_are_rejected`'s `../escape` case,
#: `test_a_nonce_that_cannot_be_a_filename_is_400_on_its_own_field`'s `../escape` case, and
#: `test_a_bad_reason_is_a_400_on_reason_before_the_job_is_read`'s fake `sk-ant-` key case. The
#: reviewer's dry run at `07c78cd8` found the first, second and fourth unsafe and no other. All
#: of them run, green, in the committed closure suite.
DESELECT = ("not legacy and not (unsupported_status_blocks and evil)"
            " and not (unsafe_job_ids_are_rejected and escape)"
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
        "run_id": "vr-1072",
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
        job_id="f027r13e1001",
        job_title="F027 round 13 evidence job",
        step_range="T001-T003",
        prior_job_ids=[],
        verification_runs=verification_runs,
        timestamp=now.isoformat(timespec="seconds"),
        generated_at=now.isoformat(timespec="microseconds"),
        review_feature_id="f027",
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

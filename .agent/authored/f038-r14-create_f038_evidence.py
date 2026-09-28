#!/usr/bin/env python3
"""Create the evidence job for F038 round 14, the closure sequence's evidence round.

Adapted from F036's `create_f036_evidence.py` (`.agent/authored/f036-r8-create_f036_evidence.py`),
which packaged READY on its first build. The evidence directory, base commit, job id, job title,
step range, feature id, run_id and TEST_FILES are F038's: the python tests the feature added or
edited (the evidence, the checked answer, the request parse with and without the model, the door,
the chat turn, `remedy chat ask`, the route, the contracts and the live end-to-end proof, and the
task-run readers R-1091 repaired), and the guards its modules reach (the command catalog, its help
and exit codes, the advertised commands, the vocabulary, the switch's config key and its guide, the
model routing inventory, the decision inbox, the raw-colour ratchet, the handler walk, the
development-artifact boundary, the durable-write guard, the blind-exception ratchet, the docs pins,
the dashboard contract and the two reachability guards of closure precondition 7) and the golden
path. `tests/ui_server/test_command_channel.py`, which the branch edited by one walked path, stays
out of the bundle: one of its parametrized node ids carries `../escape` on purpose, which the
unsafe-text scan rightly refuses; the committed closure suite, `.agent/authored/f038-closure-suite.txt`,
carries it with the full-suite proof. Everything else is F036's and load-bearing: node ids from
--collect-only, the collected-count assert, len(node_ids) == selected, sorted test_files, the
output_hash over the real pytest output, the two ancestry counts (closure-protocol pitfall (e)), the
unsafe-text red control, and `validate_verification_tests` over the written document (pitfall (f)).
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

BASE = "fec08a5b9a9742eb070cd97d0d96ddc272e3a33f"
EVIDENCE_DIR = sys.argv[1] if len(sys.argv) > 1 else ".remedy-wt/f038-r14-evidence"
TEST_FILES = sorted([
    "tests/cli/test_advertised_commands.py",
    "tests/cli/test_chat_ask.py",
    "tests/cli/test_chat_cmd.py",
    "tests/cli/test_command_catalog.py",
    "tests/cli/test_exit_codes.py",
    "tests/cli/test_golden_path.py",
    "tests/docs/test_docs_consistency.py",
    "tests/docs/test_environment_guide.py",
    "tests/docs/test_vocabulary.py",
    "tests/orchestration/test_chat_answer.py",
    "tests/orchestration/test_chat_door.py",
    "tests/orchestration/test_chat_evidence.py",
    "tests/orchestration/test_chat_intent.py",
    "tests/orchestration/test_chat_intent_model.py",
    "tests/orchestration/test_chat_turn.py",
    "tests/orchestration/test_config.py",
    "tests/orchestration/test_decision_inbox.py",
    "tests/orchestration/test_development_artifact_boundary.py",
    "tests/orchestration/test_diff_view_source.py",
    "tests/orchestration/test_durable_write_guard.py",
    "tests/orchestration/test_env_registry.py",
    "tests/orchestration/test_final_verifier.py",
    "tests/orchestration/test_import_reachability.py",
    "tests/orchestration/test_model_routing.py",
    "tests/test_ble001_ratchet.py",
    "tests/test_command_catalog.py",
    "tests/test_help_renderer.py",
    "tests/test_no_orphan_modules.py",
    "tests/ui_contracts/test_chat_citations.py",
    "tests/ui_contracts/test_evidence_panel_contract.py",
    "tests/ui_contracts/test_raw_colour_ratchet.py",
    "tests/ui_server/test_chat_e2e_live.py",
    "tests/ui_server/test_chat_route.py",
    "tests/ui_server/test_dashboard_contract.py",
    "tests/ui_server/test_handler_table_walk.py",
])
#: `not legacy` deselects the standing D3 quarantine.
DESELECT = "not legacy"


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
        "run_id": "vr-0381",
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
        job_id="f038r14e1001",
        job_title="F038 round 14 evidence job",
        step_range="T001-T003",
        prior_job_ids=[],
        verification_runs=verification_runs,
        timestamp=now.isoformat(timespec="seconds"),
        generated_at=now.isoformat(timespec="microseconds"),
        review_feature_id="f038",
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

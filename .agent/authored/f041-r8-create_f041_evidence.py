#!/usr/bin/env python3
"""Create the evidence job for F041 round 8, the closure sequence's evidence round.

Adapted from F286's `create_f286_evidence.py` (`.agent/authored/f286-r3-create_f286_evidence.py`),
which packaged READY on its first build. The evidence directory, base commit, job id, job title,
step range, feature id, run_id and TEST_FILES are F041's: every python test file the feature added or
edited (the attack corpus and the roots, the file route, the preview record, runner and worker, the
command line, the door, the results panel's contract, the tour and the end-to-end run) and the guards
the closure reads (the ledger rotation, the integrity gate, the block lint, the docs pins and
vocabulary, and the two reachability guards of closure precondition 7) and the golden path.
Everything else is F286's and load-bearing: node ids from --collect-only, the collected-count
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

BASE = "45c584e6ea896a0e16675b2ff2241d1e010a42be"
EVIDENCE_DIR = sys.argv[1] if len(sys.argv) > 1 else ".remedy-wt/f041-r8-evidence"
TEST_FILES = sorted([
    "tests/cli/test_golden_path.py",
    "tests/cli/test_job_preview.py",
    "tests/docs/test_docs_consistency.py",
    "tests/docs/test_named_source_paths.py",
    "tests/docs/test_vocabulary.py",
    "tests/orchestration/test_artifact_markdown.py",
    "tests/orchestration/test_artifact_preview.py",
    "tests/orchestration/test_block_lint.py",
    "tests/orchestration/test_import_reachability.py",
    "tests/orchestration/test_integrity_gate.py",
    "tests/orchestration/test_live_review_rotation.py",
    "tests/orchestration/test_preview_control.py",
    "tests/orchestration/test_preview_runner.py",
    "tests/orchestration/test_preview_worker.py",
    "tests/orchestration/test_result_tour.py",
    "tests/test_no_orphan_modules.py",
    "tests/ui_contracts/test_artifact_preview.py",
    "tests/ui_server/test_artifacts_route.py",
    "tests/ui_server/test_command_channel.py",
    "tests/ui_server/test_preview_commands.py",
    "tests/ui_server/test_preview_end_to_end.py",
])
#: `not legacy` deselects the standing D3 quarantine. The five tests named after it are
#: parametrized with the traversal and scheme vectors F041 refuses (`/etc/passwd`, `../outside.md`,
#: `//evil.example` and their kin), so their node ids spell exactly the local paths the packaging
#: scan rejects (closure-protocol pitfall (d)); they are deselected BY NAME, so no such string
#: reaches a node id or this command, and their proof rides in the closure suite transcript
#: `.agent/authored/f041-closure-suite.txt`, which ran them green.
UNSAFE_ID_TESTS = (
    "test_a_nonce_that_cannot_be_a_filename_is_400_on_its_own_field",
    "test_a_refused_or_absent_name_resolves_to_none",
    "test_a_refused_request_answers_json_and_no_bytes",
    "test_any_other_request_is_refused_before_the_disk_is_read",
    "test_safe_url_keeps_only_the_schemes_it_names",
)
DESELECT = " and ".join(["not legacy", *(f"not {name}" for name in UNSAFE_ID_TESTS)])


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
        "run_id": "vr-0384",
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
        job_id="f041r8e1001",
        job_title="F041 round 8 evidence job",
        step_range="T001-T003",
        prior_job_ids=[],
        verification_runs=verification_runs,
        timestamp=now.isoformat(timespec="seconds"),
        generated_at=now.isoformat(timespec="microseconds"),
        review_feature_id="f041",
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

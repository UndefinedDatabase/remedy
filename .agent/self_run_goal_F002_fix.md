# Job: F002 Fix — Reviewer Findings for Operator Repair

## Task 1 — Strengthen operator attestation validation

In `packages/orchestration/final_verifier.py`, modify `_operator_attested_tasks()`:

* Validate all four required attestation artifacts, not just review.json verdict
* Required for valid operator_attested:
  - review.json: verdict=operator_attested, reviewer identity present
  - provider_evidence.json: execution_mode=manual_operator_repair, provider_call_count=0
  - token_accounting.json: actual_available=false
  - manual_repair_provenance.json: job_id, task_id, diff_sha256, changed_files, note, timestamp
* If any artifact missing or inconsistent: report invalid_operator_attestation finding, do not PASS
* Return type changes to tuple[list[str], list[dict]] for (attested, findings)
* Merge attestation_findings into unresolved_findings in report output

Add tests in `tests/orchestration/test_final_verifier.py`:
* Spoofed review.json without manual_repair_provenance => not PASS
* Missing provider_evidence.json => not PASS
* Wrong execution_mode => not PASS
* actual_available=true => not PASS
* Complete valid attestation => PASS with badge

Acceptance:
* `python3 -m pytest tests/orchestration/test_final_verifier.py -q`

## Task 2 — Untracked files in provenance + CLI confirmation

In `packages/orchestration/repair_attest.py`:

* Modify `_collect_workspace_diff()` to return a dataclass with:
  - tracked_diff, tracked_diff_sha256
  - untracked_file_hashes (path, sha256, size_bytes per untracked file)
  - provenance_sha256 covering both tracked diff and untracked hashes
* `manual_repair_provenance.json` includes tracked_diff_sha256, untracked_file_hashes, provenance_sha256
* Add `collect_diff_stat()` function for CLI display

In CLI (`do_cmd.py`, `command_catalog.py`, `grouped.py`):
* Add `--yes` flag to repair-attest command
* Without `--yes`: show diff stat and exit 2
* With `--yes`: proceed with attestation, show diff stat in text output

Add tests in `tests/orchestration/test_repair_attest.py`:
* Tracked file in provenance
* Untracked file in changed_files and hashes
* Changing untracked content changes provenance hash
* No git repo gives empty provenance
* CLI without --yes exits 2
* CLI with --yes writes attestation
* Text output shows diff stat

Acceptance:
* `python3 -m pytest tests/orchestration/test_repair_attest.py -q`

## Task 3 — builder_no_changes evidence + completion gate fix

In `packages/orchestration/pingpong_evidence.py`:
* `_build_tests_txt()`: produce "builder_no_changes" message when no rounds
* `_build_review_json()`: produce synthetic "no_changes_verified" review when no rounds
* `write_evidence_bundle()`: always write tests.txt and review.json

In `packages/orchestration/pingpong_job.py`:
* `validate_job_task_result()`: treat builder_no_changes as valid (return True)
* This ensures later tasks are not skipped silently

Add tests:
* builder_no_changes produces review.json in `tests/orchestration/test_evidence_bundle.py`
* builder_no_changes produces tests.txt
* builder_no_changes does not skip evidence
* builder_no_changes passes completion gate in `tests/orchestration/test_job_task_runner.py`

Acceptance:
* `python3 -m pytest tests/orchestration/test_evidence_bundle.py tests/orchestration/test_job_task_runner.py -q`

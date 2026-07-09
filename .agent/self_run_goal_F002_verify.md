# Job: F002 Verify — Operator repair evidence path verification

## Task 1 — Verify operator attestation validation logic

Verify the operator attestation validation in `packages/orchestration/final_verifier.py`:

* `_operator_attested_tasks()` requires all mandatory fields
* Missing task_id in any artifact blocks attestation
* Missing manual_operator_repair/no_provider_calls blocks attestation
* Invalid SHA256 hashes block attestation
* Empty note blocks attestation
* All-attested status does NOT bypass fresh_evidence_gate, change_provenance_gate, or file alignment checks

Acceptance:
- `python3 -m pytest tests/orchestration/test_final_verifier.py -q`

## Task 2 — Verify repair_attest writer correctness

Verify `packages/orchestration/repair_attest.py`:

* Empty note produces safe default
* manual_operator_repair and no_provider_calls always written
* Provenance hash includes untracked path, sha256, and size_bytes
* tracked_diff_truncated recorded when applicable
* prompt_trace_status = not_applicable_manual_repair in provider_evidence

Acceptance:
- `python3 -m pytest tests/orchestration/test_repair_attest.py -q`

## Task 3 — Verify builder_no_changes path and evidence pipeline

Verify `packages/orchestration/pingpong_loop.py` and `packages/orchestration/pingpong_job.py`:

* builder_no_changes continues through test/reviewer phases
* builder_no_changes + reviewer pass => task pass
* builder_no_changes without reviewer => blocked
* Later tasks still run after no-change verified task

Acceptance:
- `python3 -m pytest tests/orchestration/test_job_task_runner.py tests/orchestration/test_evidence_bundle.py -q`

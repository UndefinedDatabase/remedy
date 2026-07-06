# Job: F002 — Operator Repair as a Valid Evidence Path

## Task 1 — Create repair_attest module with artifact writers

Create `packages/orchestration/repair_attest.py` with:

* `attest_operator_repair(job_id, task_id, note, repo_path)` function
* Collects workspace diff since last valid state (git diff or file comparison)
* Hashes the diff (SHA256)
* Writes these artifacts into the task's evidence directory:
  * `provider_evidence.json` with `execution_mode = "manual_operator_repair"`
  * `review.json` with `verdict = "operator_attested"`, `reviewer = "operator"`, note, timestamp
  * `token_accounting.json` with `actual_available = false`, `reason = "manual"`
  * `manual_repair_provenance.json` with diff_sha256, changed_files list, note, timestamp
* All JSONs must be schema-valid for their respective consumers
* Attest applies per task, never per job

Create `tests/orchestration/test_repair_attest.py` with tests:

* Artifact writer produces all 4 JSON files
* provider_evidence.json has execution_mode = manual_operator_repair
* review.json has verdict = operator_attested
* token_accounting.json has actual_available = false, reason = manual
* manual_repair_provenance.json has diff_sha256, files, note, timestamp
* Attest on non-existent job/task returns error

Acceptance:

* All 4 artifact files are written correctly
* Tests pass: `python3 -m pytest tests/orchestration/test_repair_attest.py -q`

## Task 2 — CLI command + final verifier acceptance + report badge

Add CLI command `remedy do repair-attest <job_id> <task_id> [--note "..."]` to:
* `apps/cli/command_catalog.py` — add command entry in do group
* `apps/cli/grouped.py` — ensure arg parsing works
* `apps/cli/commands/do_cmd.py` — add handler that calls `attest_operator_repair()`

Modify `packages/orchestration/final_verifier.py`:
* Accept `operator_attested` as PASS-equivalent verdict
* Add visible badge/label `[OPERATOR ATTESTED]` in report output when operator_attested is used
* Without attest: task remains BLOCKED (existing behavior)

Modify `packages/orchestration/token_truth.py`:
* For tasks with execution_mode = manual_operator_repair, set actual_available = false
* Do not label manual repair as actual provider usage

Add/update tests:
* Without attest => verifier/gate BLOCKED (existing behavior verified)
* With attest => verifier accepts operator_attested as PASS-equivalent
* Report contains visible [OPERATOR ATTESTED] badge
* Token truth does not label manual repair as actual provider usage

Acceptance:

* CLI `remedy do repair-attest` works
* Final verifier accepts operator_attested
* Tests pass: `python3 -m pytest tests/orchestration/test_repair_attest.py tests/orchestration/test_final_verifier.py tests/orchestration/test_token_truth.py -q`

## Task 3 — End-to-end: blocked job -> attest -> verifier PASS

Create an end-to-end test that:
1. Creates a fake blocked job with a failed/blocked task
2. Runs `attest_operator_repair()` on that task with a note
3. Runs final verifier on the job
4. Verifies verifier PASS with operator_attested badge
5. Verifies token_truth actual_available = false for attested task
6. Verifies all 4 artifact files are present and valid

Add to `tests/orchestration/test_repair_attest.py` or a new integration test.

Acceptance:

* Full pipeline works: blocked -> attest -> verifier PASS
* All tests pass: `python3 -m pytest tests/orchestration/test_repair_attest.py tests/orchestration/test_final_verifier.py tests/orchestration/test_job_evidence.py tests/orchestration/test_token_truth.py tests/test_do_job_flow.py -q`

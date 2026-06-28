# Job: Self-Run Observability Index v1

Steps 5271-5300

## Task 1: Create self_run_observability_index.json builder

Add a function to `scripts/build_review_manifest.py` (or a new module at `scripts/build_observability_index.py`) that generates `self_run_observability_index.json` from an evidence directory.

The index must answer in one place:

- Which tasks were generated? (from job_flow.json)
- Which worker prompt was sent for each task? (from task_runs/*/prompt_trace.jsonl — summary only, not raw)
- Which reviewer prompt was sent for each task? (from task_runs/*/prompt_trace.jsonl — summary only)
- Which findings were opened? (from task_runs/*/review.json)
- Which repair prompt followed each finding? (from task_runs/*/repair_loop.json)
- Which findings were rechecked?
- Which artifacts changed? (from agent_run_trace_summary.json or command_transcript.json)
- Which tests ran? (from command_transcript.json)
- How many estimated/actual tokens were used? (from task_runs/*/token_accounting.json)
- Where are the relevant evidence files? (relative paths only)
- What was the final audit status? (from job_flow.json)
- What is the next safe human action?

Requirements:
- Use safe relative artifact refs, not absolute local paths
- Do not expose raw secrets, raw full prompts, raw stdout/stderr, or full diffs
- One section per task
- Link task IDs to prompt trace entries, review results, repair loop records, token accounting, and changed files
- Clearly mark missing data as "absent" or similar instead of pretending it exists
- Work even when evidence is incomplete (partial artifacts)
- Output: `self_run_observability_index.json` written to the evidence directory

Acceptance:
- Function exists and is callable from CLI or from do_cmd.py
- Output is valid JSON
- All required sections present (tasks, findings, tokens, audit, next_action)
- Missing data clearly marked
- No absolute paths in output
- No raw prompts or secrets in output

## Task 2: Integrate index generation into do job-flow

After evidence is written, call the index builder to produce `self_run_observability_index.json` in the evidence directory.

Requirements:
- Index is generated automatically at the end of `do job-flow`
- Index generation must not fail the job flow — if generation fails, log a warning and continue
- Index appears alongside other evidence artifacts

Acceptance:
- Running `do job-flow` produces `self_run_observability_index.json` in the evidence dir
- If evidence is incomplete, the index still generates with "absent" markers
- The job flow still succeeds even if index generation raises an exception

## Task 3: Ensure index is included in review zip

The `make_review_zip.sh` script already includes all files from the evidence directory under `evidence/current/`. Verify that `self_run_observability_index.json` is included automatically.

Requirements:
- No changes to make_review_zip.sh needed (it already copies the full evidence dir)
- Add a test that verifies the index file appears in the zip under `evidence/current/self_run_observability_index.json`

Acceptance:
- Test proves the index is in the review zip
- make_review_zip.sh is NOT made stricter
- Zip filename pattern unchanged

## Task 4: Add focused tests

Add tests for the observability index builder:
- Test with complete evidence directory
- Test with incomplete evidence (missing artifacts)
- Test that no absolute paths appear in output
- Test that no raw prompts appear in output
- Test that output is valid JSON
- Test that missing data is marked as "absent" not hidden

Acceptance:
- At least 6 focused tests
- All pass
- No flaky tests

# Job: Self-Run Repair + Observability Index Completion v1

Steps 5301-5330

Previous run (job a42ed4f1eac349fa) proved Remedy can develop itself but ended BLOCKED. This run completes the work and fixes system weaknesses.

Reference diffs from previous run (use as source material, do NOT copy blindly):
- remedy-job-evidence-selfrun-5271-5300/task_runs/T001/safe.diff
- remedy-job-evidence-selfrun-5271-5300/task_runs/T002/safe.diff
- remedy-job-evidence-selfrun-5271-5300/task_runs/T003/safe.diff

## Task 1: Implement Self-Run Observability Index

Create `scripts/build_observability_index.py` that generates `self_run_observability_index.json` from an evidence directory.

The index must answer in one place:
- Which tasks were generated? (from job_flow.json)
- Which worker prompt was sent for each task? (summary only — kind, round, sha256, token estimate — NOT raw prompt text)
- Which reviewer prompt was sent for each task? (summary only)
- Which findings were opened? (from task_runs/*/review.json)
- Which repair prompt followed each finding? (from task_runs/*/repair_loop.json)
- Which findings were rechecked?
- Which artifacts changed? (from job_flow.json final_audit.changed_files or agent_run_trace_summary.json)
- Which tests ran? (from command_transcript.json or job_flow.json final_audit.test_summary)
- How many estimated/actual tokens were used? (from task_runs/*/token_accounting.json)
- Where are the relevant evidence files? (relative paths only)
- What was the final audit status? (from job_flow.json)
- What is the next safe human action?

Requirements:
- Use safe relative artifact refs, not absolute local paths
- Do not expose raw secrets, raw full prompts, raw stdout/stderr, or full diffs
- One section per task
- Link task IDs to prompt trace entries, review results, repair loop records, token accounting, and changed files
- Mark missing data explicitly as "absent" (not hidden or faked)
- Work on incomplete evidence including skipped tasks
- Include agent-run timeline summary
- If repair prompts exist, map them to findings
- CLI callable: `python3 scripts/build_observability_index.py --evidence-dir <path>`

Use the prior evidence diff (remedy-job-evidence-selfrun-5271-5300/task_runs/T001/safe.diff) as reference for the implementation approach. It contains a working 431-line module that was reviewer-approved. Adapt and harden it, do not blindly copy.

Acceptance:
- File exists at scripts/build_observability_index.py
- Output is valid JSON
- All required sections present (tasks, findings, tokens, audit, next_action)
- Missing data clearly marked as "absent"
- No absolute paths in output
- No raw prompts or secrets in output
- Works on incomplete evidence dirs

## Task 2: Integrate index generation into do job-flow

Add best-effort integration so `do job-flow` writes `self_run_observability_index.json` into the evidence directory after evidence export.

Requirements:
- Call happens after evidence and command transcript are written
- Failure must NOT crash the job flow
- Failure must be recorded structurally: add `observability_index_status` field to the final JSON output (value: "generated", "failed", or "skipped")
- If generation fails, include `observability_index_error` with the error message
- Do not change review zip filename behavior
- Do not make make_review_zip.sh stricter

Use the prior evidence diff (remedy-job-evidence-selfrun-5271-5300/task_runs/T002/safe.diff) as reference. It shows a working integration using importlib. Adapt and harden it.

Acceptance:
- Running `do job-flow` produces self_run_observability_index.json in evidence dir
- If evidence is incomplete, index generates with "absent" markers
- Job flow succeeds even if index generation raises an exception
- Final JSON output includes observability_index_status field

## Task 3: Fix reviewer verdict normalization

The previous self-run exposed: reviewer returned `verdict=pass` with `finding_count=1`, which Remedy treated as `review_inconsistent` and blocked without attempting repair.

Fix the reviewer output normalization so `pass + findings > 0` is handled productively.

Required behavior:
- If reviewer output contains `verdict=pass` AND `finding_count > 0`, normalize verdict to `needs_review` (not plain `pass`)
- This triggers the existing repair loop instead of blocking as `review_inconsistent`
- Do NOT allow `pass + findings` to silently pass without review
- Unresolved findings must not be hidden
- The final_audit and repair_loop must clearly explain what happened

Find the reviewer output normalization code (likely in packages/orchestration/pingpong_loop.py or pingpong_provider.py where ReviewerOutput is parsed) and add the normalization there.

Acceptance:
- Reviewer `pass` with findings is normalized to `needs_review`
- Repair loop is triggered for the findings
- Final audit explains the normalization
- No silent pass-through of findings

## Task 4: Fix command transcript vs target guard contradiction

The previous run had inconsistent safety metadata:
- target_guard.json: target_mutated=false
- command_transcript.json: target_repo_mutated=true

Cause: transcript compares repo hashes before/after, but cache/noise files (.mypy_cache, .pytest_cache, .ruff_cache) change the hash even though target_guard correctly ignores them.

Fix so the command transcript uses the same noise exclusion policy.

Find the command transcript target mutation detection in apps/cli/commands/do_cmd.py (look for target_repo_hash_before, target_repo_hash_after, target_repo_mutated).

Required behavior:
- Transcript must not claim target mutation when only ignored cache/noise files changed
- Add explicit fields: target_content_mutated (true only for real source changes), target_noise_changed (true if only cache files changed), ignored_noise_files (list)
- Keep real target source mutation detection strict

Acceptance:
- Command transcript and target guard agree when only cache/noise changes
- New fields present in command_transcript.json
- Real source mutations still detected

## Task 5: Add focused tests

Add focused tests for the observability index and the fixes above.

Tests needed:
- Observability index with complete evidence dir → valid JSON, all sections present
- Observability index with incomplete evidence (missing artifacts) → "absent" markers, still valid JSON
- No absolute local paths in index output
- No raw full prompts in index output (only summaries with sha256/token count)
- Missing data marked as "absent" not hidden as empty/zero
- Index included in review zip under evidence/current/self_run_observability_index.json
- Reviewer pass with findings → normalized to needs_review
- Command transcript target mutation consistent with target guard for cache-only changes

Acceptance:
- At least 8 focused tests
- All pass
- No flaky tests
- Tests cover the fixes from Tasks 3 and 4

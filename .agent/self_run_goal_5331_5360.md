# Job: Operational Artifact Guard + Promote-Ready Observability Index v1

Steps 5331-5360

Previous run (job da737770b0a04aff) proved Remedy can develop itself but ended BLOCKED because target guard classified a review zip as target mutation. This run carries forward the accepted code, fixes operational artifact classification, and ensures the observability index is persistently visible.

Reference diffs from previous run (use as source material, do NOT copy blindly):
- remedy-job-evidence-selfrun-5301-5330/task_runs/T001/safe.diff
- remedy-job-evidence-selfrun-5301-5330/task_runs/T002/safe.diff
- remedy-job-evidence-selfrun-5301-5330/task_runs/T003/safe.diff
- remedy-job-evidence-selfrun-5301-5330/task_runs/T004/safe.diff
- remedy-job-evidence-selfrun-5301-5330/task_runs/T005/safe.diff

## Task 1: Carry forward Observability Index + fixes from prior run

The previous run (da737770b0a04aff) produced reviewer-approved code that was staged but never applied to the target repo. Re-create these accepted changes cleanly in the new staging workspace.

Files to carry forward:
- `scripts/build_observability_index.py` — full observability index builder (from T001 diff)
- `apps/cli/commands/do_cmd.py` — `_persist_observability_index()` integration (from T002 diff) AND command transcript noise-aware mutation fields (from T004 diff)
- `packages/orchestration/pingpong_provider.py` — `normalize_reviewer_verdict()` function, `original_verdict`/`verdict_normalized` fields on ReviewerOutput (from T003 diff)
- `packages/orchestration/pingpong_loop.py` — `normalization_note` on RepairDecision, verdict normalization audit trail fields in `_build_repair_loop_summary()` and `_build_job_flow_summary()` (from T003 diff)
- `tests/test_do_job_flow.py` — `test_command_transcript_noise_fields_agree_with_guard` (from T004 diff)
- `tests/test_observability_index.py` — focused tests for index, verdict normalization, transcript consistency (from T005 diff)

Do NOT blindly copy. Read each diff, understand what it does, and apply the changes cleanly to the current codebase. If any context has shifted, adapt.

Acceptance:
- All files listed above exist with the carried-forward changes
- Changes are consistent with each other (no stale imports, no missing functions)
- No syntax errors
- Code compiles (python3 -c "import scripts.build_observability_index")

## Task 2: Fix operational artifact classification

Target guard and command transcript must not classify Remedy review/evidence transport artifacts as target source mutation.

The previous run was BLOCKED because `remedy-review-20260629-113227.zip` appeared in the repo root during the run and was classified as target mutation.

Add a shared operational-artifact policy that recognizes these root-level patterns as Remedy operational artifacts, not source code:
- `remedy-review-YYYYMMDD-HHMMSS.zip` (review zip transport files)
- `run_transcript.txt` (self-run transcript)
- `remedy-job-evidence-*` directories and their contents (evidence bundles)

Required behavior:
- Source-code changes still count as target mutation (strict)
- Operational review/evidence artifacts do NOT count as target source mutation
- Cache/noise artifacts (.mypy_cache, .pytest_cache, .ruff_cache, __pycache__, *.pyc) still do NOT count as source mutation
- Target guard and command transcript must agree

Add the classification function near the existing `_is_target_noise()` function in `packages/orchestration/pingpong_loop.py`. Add a new function `_is_operational_artifact(rel_path: str) -> bool` that matches the patterns above.

Update target guard to use three-way classification:
- content (real source) — counts as mutation
- operational artifacts — does NOT count as mutation
- noise (cache files) — does NOT count as mutation

Add explicit fields to both target_guard.json and command_transcript.json:
- `target_content_mutated`: bool — true only for real source changes
- `target_operational_artifacts_changed`: bool — true if operational artifacts appeared/changed
- `target_noise_changed`: bool — true if only cache files changed
- `ignored_operational_artifacts`: list — which operational files were ignored
- `ignored_noise_files`: list — which cache/noise files were ignored

The headline `target_mutated` field must track `target_content_mutated` (real source), not the aggregate.

Do not hide arbitrary files. Only ignore exact Remedy operational patterns.

Acceptance:
- `_is_operational_artifact()` function exists in pingpong_loop.py
- Target guard uses three-way classification
- Command transcript uses same classification
- Both agree on operational artifacts
- Real source mutations still detected
- New fields present in both target_guard.json and command_transcript.json

## Task 3: Make observability index status persistently visible

The prior T002 integration calls `_persist_observability_index()` and updates `flow_result`, but this happens AFTER `job_flow.json` is already written. The index status is only visible in stdout, not in any persisted evidence artifact.

Fix this so index status is visible in a persisted file.

Recommended approach: re-persist `job_flow.json` after index generation, or append the status to `command_transcript.json`.

Required fields in the persisted artifact:
- `observability_index_status`: "generated", "failed", or "skipped"
- `observability_index_error`: error message string (only when not "generated")
- `observability_index_ref`: "self_run_observability_index.json" (only when generated)

Acceptance:
- After `do job-flow` completes, at least one persisted evidence file contains `observability_index_status`
- The field is readable by downstream tools without parsing stdout
- Generated/failed/skipped all produce the correct status
- Error message is captured on failure

## Task 4: Ensure index is actually generated and included in review zip

After a successful `do job-flow`, the evidence directory must contain `self_run_observability_index.json`.

The review zip must include this file under `evidence/current/self_run_observability_index.json`.

The index must:
- Contain one section per task
- Summarize worker/reviewer prompts without raw full prompt bodies (only sha256, token estimate, kind, round)
- Show findings, repair loops, token accounting, changed files, tests, audit status, next safe action
- Handle incomplete evidence gracefully (mark missing data as "absent", not hidden or fabricated)
- Use safe relative artifact refs (never absolute local paths)
- Contain no raw diffs, stdout/stderr, or secrets

If the index builder script (`scripts/build_observability_index.py`) already exists from Task 1, verify it meets all these requirements. If any are missing, add them.

Acceptance:
- `self_run_observability_index.json` exists in evidence dir after `do job-flow`
- File is valid JSON
- All required sections present (tasks, findings, tokens, audit, next_action)
- No absolute paths
- No raw prompts or secrets
- Missing data marked "absent"
- Works on incomplete evidence dirs
- Included in review zip under evidence/current/

## Task 5: Focused tests

Add focused tests covering the observability index and the operational artifact / transcript fixes.

Tests needed:
- Observability index with complete evidence dir → valid JSON, all sections present
- Observability index with incomplete evidence (missing artifacts) → "absent" markers, still valid JSON
- No raw prompt body in index output (only summaries with sha256/token count)
- No absolute local paths in index output
- Reviewer `pass` with findings → normalized to `needs_repair`
- Original reviewer verdict is preserved after normalization
- Command transcript and target guard agree when only cache/noise files change
- Command transcript and target guard agree when only Remedy operational artifacts change (e.g. remedy-review-*.zip)
- Real source file mutation still blocks (not classified as noise or operational)
- `self_run_observability_index.json` is included in review zip under evidence/current/

Acceptance:
- At least 10 focused tests
- All pass
- No flaky tests
- Tests cover operational artifact classification (Task 2)
- Tests cover index persistence (Task 3)
- Tests cover verdict normalization (from prior T003)
- Tests cover transcript/guard consistency (from prior T004 + Task 2)

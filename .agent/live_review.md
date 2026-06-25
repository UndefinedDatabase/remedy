# Live Review — Steps 4832-4844: Job Runner Correctness + Token Context Policy v1

Reviewer: parallel reviewer (independent; owns verdict).
Builder must NOT write reviewer verdicts. Builder must NOT self-merge.
Builder must NOT mark findings as resolved.
Timestamp: 2026-06-25

## Verdict (reviewer-owned)
PENDING

## Commit reviewed
(pending commit)

## PR reviewed
No open PR. Builder on `feature/steps-3276-3355-job-fulfillment-spine-v0`.

## Builder handoff

### What changed
Correctness closure for Job Task Runner v0: fixed CLI command truth, made task IDs deterministic by parse order, added strict workspace apply with safety manifest, added job-level target repo snapshot guard, strengthened task completion gate, added per-task proof summaries, added explicit token context policy, and comprehensive tests.

### Files changed
- `packages/orchestration/pingpong_job.py` — Substantial rewrite (~600 lines): added ApplyManifest, TaskProofSummary, TargetGuard dataclasses; deterministic task IDs; strict workspace apply with path safety; target repo snapshot guard; token context policy; fixed next_command truth
- `apps/cli/commands/do_cmd.py` L686, L694 — Fixed stale `remedy do job run` → `remedy do job-run`
- `tests/orchestration/test_job_task_runner.py` — Rewritten (~530 lines): 65 tests across 14 classes
- `.agent/plan.md` — updated
- `.agent/context.md` — updated

### Step-by-step results

**Step 4832 — Fix job CLI command truth**
`_suggest_next_command()` now uses `job-run`, `job-report` (hyphenated). Fixed 2 stale `remedy do job run` in `_cmd_do_job_plan()`. All next_command strings are copy-pasteable.

**Step 4833 — CLI E2E tests**
TestCliE2E: 5 tests — catalog entries, handler existence, next_command includes job_id and uses hyphens.

**Step 4834 — Deterministic task IDs**
Task IDs assigned by parse order: first parsed = T001, second = T002. `source_heading_number` stores original heading. `## Task 7` + `## Task 9` → T001, T002. Duplicate headings → T001, T002. Tests: TestDeterministicTaskIds (5 tests).

**Step 4835 — Strict workspace apply manifest**
`_strict_apply_to_workspace()` returns `ApplyManifest` with applied/missing/unsupported/unexpected/duplicate lists. Missing staged files block. Duplicate paths block. Path traversal blocks. Absolute paths block. `.env*`, `.git`, cache dirs, private key files block. No silent skipping. Tests: TestStrictWorkspaceApply (8 tests).

**Step 4836 — Reuse promotion safety logic**
`_is_unsafe_path()` validates all paths with traversal, env, git, unsafe dir, and private key checks. Same safety level as existing staging_workspace filtering. Tests: TestPromotionSafetyReuse (3 tests).

**Step 4837 — Job-level target repo snapshot guard**
`_snapshot_target_repo()` + `_check_target_repo_guard()` reuse `_snapshot_target` and `_check_target_mutation` from pingpong_loop.py. Checked after each task. Mutation → task blocked, job blocked. `TargetGuard` persisted in job JSON. Tests: TestTargetRepoGuard (2 tests).

**Step 4838 — Strengthen task completion gate**
Task reaches APPLIED only if: final_status == "staged_review_passed" AND strict apply succeeded AND target guard passed. Any failure → TASK_BLOCKED/FAILED + JOB_BLOCKED + remaining SKIPPED. Tests: TestTaskCompletionGate (3 tests).

**Step 4839 — Per-task proof summaries**
`TaskProofSummary` dataclass with task_id, title, run_id, final_status, applied_files, test_passed, reviewer_verdict, repair info, tokens_estimated. Persisted in job JSON. Tests: TestProofSummaries (3 tests).

**Step 4840 — Token context policy**
`_build_task_prompt()` passes only: job title, current task body/acceptance, last 5 proof summaries with applied file lists. No full previous prompts, no full diffs, no full repo. Report includes `context_strategy` dict. Tests: TestTokenContextPolicy (1 test).

**Step 4841 — Token-bounded prompt tests**
TestTokenBoundedPrompt (5 tests): body truncation, bounded summary in prompt, no full Task 1 body in Task 2, only last 5 summaries, prompt length bounded.

**Step 4842 — Blocking-path E2E tests**
TestBlockingPathE2E (5 tests): missing file blocks, .env blocks, traversal blocks, duplicate blocks, task stays PASSED (not APPLIED) when blocked.

**Step 4843 — Existing flows preserved**
TestExistingFlowsPreserved (9 tests) + 305 adjacent tests pass. Full suite: 7807 passed.

**Step 4844 — Architecture guard**
All clean:
- No stale `remedy do job run`/`plan`/`report` in production code
- No `shell=True`
- No provider calls during plan
- No target repo mutation (snapshot guard)
- No git ops
- No `os.environ`/`getenv` in job module
- No `live_review.md` dependency
- No unbounded history (last 5 summaries)
- No full repo in prompt
- No auto-promote
- Task IDs by parse order, not heading number
- Strict apply: no silent skips
- Path safety: traversal, .env, .git, keys all blocked
- Task done only after review + strict apply + guard

### Test results
- Job task runner: 65/65 pass
- Evidence bundle: 65/65 pass
- Repair loop: 131/131 pass
- Job fulfillment: 109/109 pass
- Fast lane: 571/571 pass
- Runtime lane: 57/57 pass (4/4 suites)
- Lint: ruff clean, mypy clean (200 source files)
- Full suite: 7807 passed, 8 skipped, 1 deselected, 0 failed (239s)

### What this proves
- All job CLI next commands are copy-pasteable
- Task IDs are unique and deterministic by parse order
- Job workspace apply is strict — cannot silently skip
- Unsafe paths (traversal, .env, .git, keys) block apply
- Job-level target repo mutation guard exists and works
- Task completion requires review pass + strict apply + guard
- Task 2 never starts before task 1 is applied
- Token context is bounded (last 5 summaries, 2000-char body limit)
- Job report shows context strategy and proof summaries
- Existing single-task, repair, evidence, promotion flows preserved
- Remedy can run ordered jobs safely and token-efficiently

### What this does not prove
- Real Claude CLI dogfood
- DAG/parallel scheduling
- Final target-repo job promotion
- Delete-file handling in workspace apply (blocked by design)

### Carry-forward
No open findings. All prior reviewer verdicts: PASS.

### Review quiet-window
- Final review file check: 2026-06-25 ~18:55 UTC
- live_review.md last modified: overwritten for this handoff
- No reviewer activity detected
- No findings requiring Builder action

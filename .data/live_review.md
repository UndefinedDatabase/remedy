# Live Review — Steps 375-382

Reviewer: worker self-review
Scope: Steps 375-382 (Resource-Safe Pytest Harness, Reviewer Safety, Handoff Truth)
Status: PASS
Started: 2026-06-03
Commit: pending

---

## Steps 375-382 Review

### Step 375: Resource-Safety Policy — PASS
- docs/reviewer-safety.md created with full policy
- tests/README.md updated with wrapper commands + safety section
- .agent/context.md has permanent resource-safety rules section

### Step 376: Guarded Pytest Wrapper — PASS
- scripts/remedy_pytest.sh: flock -n, timeout, foreground-only, python3
- Configurable: REMEDY_PYTEST_TIMEOUT_SEC, REMEDY_PYTEST_LOCK, REMEDY_PYTHON
- Executable, clear error messages for lock-busy and timeout

### Step 377: Reviewer Protocol — PASS
- docs/reviewer-safety.md: Reviewer Protocol section
- Prioritizes code inspection over repeated test execution

### Step 378: Handoff Truth — PASS
- live_review.md Steps 367-374 corrected from IN PROGRESS to PASS
- All step substatus corrected (IN PROGRESS/PENDING → PASS)
- Step 374 has actual baseline numbers

### Step 379: Test Command Matrix — PASS
- docs/reviewer-safety.md: During Development / Before Final Handoff / Never sections

### Step 380: Resource-Safety Regression Tests — PASS
- 13 tests in tests/regression/test_resource_safety.py
- TestPytestWrapper (6): exists, flock, timeout, runs pytest, no background, executable
- TestResourceSafetyDocs (5): doc exists, background ban, parallel ban, README
- TestContextIncludesResourceSafety (1): context.md references
- TestNoBackgroundPytestInDocs (1): scans docs for prohibited patterns

### Step 381: Emergency Cleanup Guidance — PASS
- docs/reviewer-safety.md: Emergency Cleanup section with pgrep/pkill/top

### Step 382: Guarded Baseline — PASS
- Full pytest via wrapper: 3943 passed, 7 skipped (scripts/remedy_pytest.sh tests/ -q --cache-clear)
- Vitest: 35 passed
- TypeScript: clean
- Build: OK
- Guards: no test_steps_*.py, no shell=True, no 0.0.0.0, no unittest.mock in packages

## Findings Resolved
- R-13001 (plan checkboxes): all marked [x]
- R-13003 (nohup check): added to test_wrapper_no_background

## Merge Readiness: PASS

---

# Parallel Review — Steps 375-382

Reviewer: parallel watcher (independent)
Scope: Steps 375-382
Status: IN PROGRESS
Started: 2026-06-03
Commit baseline: 5744c26 (Steps 367-374 final)
Last check: 2026-06-03 — initial scan complete, most deliverables present, Step 382 baseline pending

---

## Parallel Reviewer Baseline

- Commit at block start: 5744c26
- Full pytest independent baseline: 3930 passed, 7 skipped, 0 failed (verified prior session)
- Vitest pre-block: 35 tests
- TypeScript: clean
- Worker state at scan: all Steps 375-381 deliverables present, Step 382 in progress

---

## Parallel Reviewer Active Findings

### R-13001 — OPEN

Status: Open
Severity: low
Area: handoff
Summary: plan.md shows all 8 steps as [ ] (unchecked) even as they complete
Details: .agent/plan.md still has `- [ ] Step 375` through `- [ ] Step 382` with no boxes checked. Misleading state — worker completes steps without updating plan.
Evidence: .agent/plan.md lines 10-17 all `[ ]`
Expected fix: Mark completed steps as `[x]` as they finish.

### R-13002 — OPEN

Status: Open
Severity: medium
Area: baseline
Summary: Step 382 guarded baseline not yet run — no new commit, no wrapper-verified test count
Details: Worker must run `scripts/remedy_pytest.sh tests/ -q --cache-clear` and report result. Block is not complete until this happens.
Evidence: git status shows uncommitted changes, no new commit since 5744c26
Expected fix: Run wrapper baseline, report result, commit all artifacts.

### R-13003 — OPEN

Status: Open
Severity: low
Area: pytest-wrapper
Summary: test_wrapper_no_background does not check for `nohup` in wrapper
Details: `test_wrapper_no_background` checks `run_in_background` and ` &` line endings but not `nohup`. Minor gap — the actual script doesn't use nohup, but the test doesn't verify this.
Evidence: test_resource_safety.py line 35-39
Expected fix: Add `assert "nohup" not in text` to test_wrapper_no_background (optional — low priority).

---

## Parallel Reviewer Step-by-Step Review

### Step 375: Resource-Safety Policy — PASS

- docs/reviewer-safety.md: created ✓
- "Never Do" section: background pytest, parallel sessions, repeated full suite ✓
- "Always Do" section: wrapper mandate, foreground, targeted tests during dev ✓
- .agent/context.md updated with resource-safety rules ✓ (new "Resource-Safety Rules (permanent)" section)
- tests/README.md updated with wrapper commands and Resource Safety section ✓

### Step 376: Guarded Pytest Wrapper — PASS

- scripts/remedy_pytest.sh created ✓
- `flock -n` on configurable lock file ✓ (line 24)
- `timeout "${TIMEOUT_SEC}"` — default 600s ✓ (line 34)
- Foreground only — no `&` in any non-comment line ✓
- Fails fast with clear error: "Another pytest run is already active. Refusing to start a parallel run." ✓
- exit 124 with helpful message on timeout ✓
- set -euo pipefail ✓
- Configurable: REMEDY_PYTEST_TIMEOUT_SEC, REMEDY_PYTEST_LOCK ✓
- Does not kill unrelated processes ✓
- Executable bit set (-rwxrwxr-x) ✓

### Step 377: Reviewer Protocol Update — PASS

- "Reviewer Protocol" section in docs/reviewer-safety.md ✓
- Prioritizes code inspection over test execution ✓
- "Full baseline — only once at final review" ✓
- "If worker already reports full baseline, reviewer may verify targeted areas instead" ✓
- "Never" section in test matrix bans repeated full pytest in watcher loop ✓

### Step 378: Handoff Truth Cleanup — PASS WITH NOTE

- live_review.md Steps 367-374 corrected to PASS ✓ (worker updated header)
- .agent/context.md updated to Steps 375-382 scope ✓
- plan.md updated with Steps 375-382 plan ✓
- NOTE: plan.md checkboxes all unchecked (R-13001) — minor

### Step 379: Test Command Matrix — PASS

- docs/reviewer-safety.md "Test Command Matrix" section ✓
- "During Development (targeted)" with 3 examples using wrapper ✓
- "Before Final Handoff (one full baseline)" ✓
- Frontend: vitest command listed ✓
- TypeScript: tsc --noEmit listed ✓
- "Never" section: 4 prohibitions including background, repeated, parallel, bare python -m pytest ✓

### Step 380: Resource-Safety Regression Tests — PASS

- tests/regression/test_resource_safety.py: 13 tests ✓
- TestPytestWrapper (6 tests): exists, flock -n, timeout, runs pytest, no background &, executable ✓
- TestResourceSafetyDocs (5 tests): doc exists, mentions no-background, mentions parallel/single, README wrapper, README safety ✓
- TestContextIncludesResourceSafety (1 test): context.md has "resource" or "pytest" ✓
- TestNoBackgroundPytestInDocs (1 test): scans all docs/*.md for run_in_background+pytest combos ✓
- Not superficial file-exists only — content assertions ✓
- GAP: nohup not checked (R-13003, low)

### Step 381: Emergency Cleanup Guidance — PASS

- "Emergency Cleanup" section in docs/reviewer-safety.md ✓
- Inspect: `pgrep -af "pytest|python.*pytest"` ✓
- Kill: targeted `pkill -f "python.*pytest"` with per-PID alternative ✓
- Warning: "Do not kill unrelated Python services blindly" ✓
- Warning: "`pkill -f python` will kill everything Python — too broad" ✓
- "Always inspect with pgrep -af first" ✓

### Step 382: Guarded Baseline And Next Plan — PENDING

- Wrapper run: NOT YET ✗
- Commit: NOT YET ✗
- Next block named in context: "Steps 383-390 — Builder Prompt Quality And Real-Ollama Hardening" ✓

---

# Live Review — Steps 367-374

Reviewer: parallel watcher (independent)
Scope: Steps 367-374 (Resume Execution Quality: TestRunner Integration, Dry-Run Truth, Events, CLI/UI, Docs)
Status: PASS
Started: 2026-06-02
Commit reviewed: 5744c26 (Steps 367-374)
Commit baseline: ae26ce2 (catalog test fix) after 49e880e (Steps 359-366)
Last check: final — all steps verified, committed 5744c26, pushed

---

## Baseline (Steps 367-374 Block)

- Commit at block start: ae26ce2 (catalog fix after Steps 359-366)
- Full pytest pre-block: 3922 passed, 7 skipped, 0 failed (verified)
- Vitest pre-block: 35 tests
- TypeScript: clean
- Worker current: Steps 369+368+370+372+373 in simultaneous progress

---

## Active Findings

(none open yet — monitoring)

---

## Step-by-Step Review

### Step 367: Pin Resume Execution Gaps — PASS

- Fix commit `ae26ce2`: upgraded `test_next_command_catalog_valid` to check full (group, subcommand) pairs ✓
- Worker documented gaps: ad-hoc subprocess in job.py, dry-run overclaims permission ✓
- Tests pinned before implementation started ✓

### Step 368: Capability-Aware Dry-Run — PASS

- `_validate_from_apply` added to `event_replay.py` ✓
- Checks: `is_allowed(job, Capability.repo_test_run)` ✓
- Checks: `repo_path` from `job.metadata` ✓
- Checks: `repo.is_dir()` ✓
- Checks: `discover_commands` + `select_best_test_candidate` ✓
- `resume_dry_run` now calls `_validate_from_apply(job)` for from_apply checkpoint ✓
- `can_resume=True` only when all validation passes ✓
- Tests: `test_dry_run_no_permission_blocked`, `test_dry_run_no_repo_blocked`, `test_dry_run_creates_no_events` — all pass ✓
- Dry-run creates no events (verified by test and by code: no `append_run_event` in `resume_dry_run`) ✓

### Step 369: TestRunner-Backed from_apply — PASS

- Ad-hoc `subprocess.run` in `job.py` removed ✓
- `execute_resume_from_apply(job, checkpoint_id, data_dir)` now in `packages/orchestration/event_replay.py` ✓
- Uses `run_tests_local(job, workspace_root)` from existing test_runner ✓
- Uses `discover_commands` + `select_best_test_candidate` (existing abstractions) ✓
- `workspace_root = Path(data_dir) / "workspaces" / str(jid)` ✓
- No `shell=True` ✓
- `capture_output=True` (test_runner does it, no raw stdout/stderr in events) ✓
- Events: `resume_test_started`, `resume_test_completed` with only `passed`, `test_run_id`, `status`, `exit_code`, `duration_ms`, `output_truncated`, `persisted_output_bytes`, `command_source_type`, `command_confidence` — all safe metadata ✓

### Step 370: Resume Event And Proof Linkage — PASS

- `resume_started`, `resume_test_started`, `resume_test_completed`, `resume_completed` events ✓
- Events include `test_run_id` for audit trail ✓
- `output_truncated` and `persisted_output_bytes` in metadata ✓
- No raw stdout/stderr in events ✓

### Step 371: CLI/JSON/UI Consistency — PASS

### Step 372: Checkpoint Required Data Contract — PASS

- `JobCheckpoint` new fields: `resume_mode_supported`, `inspectable`, `dry_run_available`, `required_data`, `missing_data` ✓
- `approval_recorded`: `required_data=["structured_patch_payload", "intent_id"]`, `missing_data=["structured_patch_payload"]` ✓
- `source_apply_proven`: `required_data=["repo_path", "test_candidate"]`, `resume_mode_supported=True` ✓
- `tests_failed`: `required_data=["repair_context"]`, `missing_data=["repair_context"]` ✓
- `export_checkpoints_json` includes new fields ✓
- Tests: `TestCheckpointDataContract` (3 tests) — all pass ✓

### Step 373: Resume Docs — PASS

- `docs/resume.md` created ✓
- Honest status table: from_apply "Implemented", others "Blocked" ✓
- Commands catalog-valid (verified: event replay, job checkpoints, job resume, job permit, patch approve) ✓
- Dry-run section: explicitly says "does not create events, modify job or repo, run tests, call providers" ✓
- UI section: "read-only — no browser resume button" ✓
- Blocked reasons table complete ✓
- Tests: `TestDocsExist` (2 tests) — verify docs exist + commands catalog-valid ✓

### Step 374: Full Baseline And Handoff — PASS

- pytest: 3930 passed, 7 skipped, 0 failed (batched: 1225 + 2705)
- Vitest: 35 passed
- TypeScript: clean
- Build: OK
- Committed: 5744c26, pushed

---

## Previous Review History

### Steps 367-374: PASS — test_runner integration, dry-run truth, resume events, checkpoint data contract
### Steps 359-366: PASS — R-12001 resolved, checkpoint semantics honest, from_apply real test runner
### Steps 351-358: PASS WITH RISKS — event replay, checkpoints, CLI, conservative resume
### Steps 343-350: PASS — token metrics, organic graph v2, 4-row layout
### Steps 335-342: PASS — Operator Cockpit v2, pipeline visibility, stop-reason UX
### Steps 329-334: PASS — stop_reason JSON repair, memory import fix, docs contract

---

# Live Review — Steps 359-366

Reviewer: parallel watcher (independent)
Scope: Steps 359-366 (Resume Truth: R-12001 Fix, Checkpoint Semantics, from_approval/from_apply/repair, Dry-Run, CLI/UI)
Status: PASS
Started: 2026-06-02
Commit reviewed: 49e880e (Steps 359-366)
Last check: final — all independently verified (3922 pytest, 35 Vitest, TypeScript clean) — R-12001 resolved

---

## Baseline (Steps 359-366 Block)

- Commit at block start: 0c589df (Steps 351-358 final)
- Full pytest pre-block: 3916 passed, 7 skipped, 0 failed (verified)
- Vitest pre-block: 35 tests
- TypeScript: clean
- Carry-forward open: R-12001 (from_approval no-op success, checkpoint overclaims)
- Committed: 3 files (event_replay.py, job.py, test_event_replay.py)
- +6 pytest: 3916→3922. Vitest unchanged: 35.

---

## Resolved Findings

### R-12001 — RESOLVED (49e880e)

Status: Resolved
Severity: was medium
Area: resume-truth
Fix summary:
- `from_approval` no longer calls `run_autorun(builder_provider="none")` and claims success. Now `safe_to_resume=False`, `blocked_reason="missing_patch_payload"`.
- `context_ready`: `safe_to_resume=False`, `status="inspectable"`, `blocked_reason="resume_mode_not_implemented"` ✓
- `tests_failed`: `safe_to_resume=False`, `blocked_reason="resume_mode_not_implemented"` ✓
- `source_apply_proven`: remains `safe_to_resume=True` with real test-runner path ✓
- No-op "resumed=True" path removed from `_cmd_resume` ✓
- Unimplemented modes return `{"resumed": False, "blocked_reason": "resume_mode_not_implemented"}` ✓
- 2 regression tests: `test_from_approval_not_resumable`, `test_no_resumed_true_for_unimplemented_mode` ✓

---

## Step-by-Step Review

### Step 359: R-12001 Preflight — PASS

- R-12001 identified and documented ✓
- Plan shows "confirmed from_approval is no-op, context_ready overclaims" ✓
- Worker started checkpoint semantics fix (Step 360) without new scope additions ✓
- Safety gates intact ✓

### Step 360: Checkpoint Semantics Cleanup — PASS

- `context_ready`: `safe_to_resume=False`, `status="inspectable"`, `blocked_reason="resume_mode_not_implemented"` ✓
- `patch_intent_created`: `safe_to_resume=False`, `status="blocked"`, `blocked_reason="approval_pending"` ✓
- `approval_recorded`: `safe_to_resume=False`, `status="blocked"`, `blocked_reason="missing_patch_payload"` ✓
- `source_apply_proven`: `safe_to_resume=True`, `status="available"` — only implemented mode ✓
- `tests_failed`: `safe_to_resume=False`, `status="blocked"`, `blocked_reason="resume_mode_not_implemented"` ✓
- `tests_passed`: `status="complete"`, `safe_to_resume=False` ✓
- 4 new tests pinning these semantics ✓

### Step 361: Real `from_approval` Resume Or Honest Block — PASS

- No-op `run_autorun(builder_provider="none")` path removed ✓
- `approval_recorded` now `safe_to_resume=False` with `blocked_reason="missing_patch_payload"` ✓
- CLI reports `{"resumed": False, "blocked_reason": "missing_patch_payload"}` ✓
- Regression test: `test_from_approval_not_resumable` ✓

### Step 362: `from_apply` To Tests — PASS

- `from_apply` resume now runs real test discovery and subprocess tests ✓
- Permission gate: `is_allowed(job, Capability.repo_test_run)` checked ✓
- Repo path checked: `job.metadata.get("target_repo")` ✓
- Repo exists check: `repo.is_dir()` ✓
- Test discovery: Makefile → `["make", "test"]` or pyproject/tests → `[sys.executable, "-m", "pytest", ...]` ✓
- No test candidate → `blocked_reason="missing_test_candidate"` ✓
- Subprocess: list argv (no shell injection), `capture_output=True` (no raw stdout/stderr leak) ✓
- Events: `resume_test_started`, `resume_test_completed` with `passed: bool` only ✓
- Output: `{"resumed": True, "tests_passed": bool, "stop_reason": str}` — honest ✓
- Timeout 60s, catches `TimeoutExpired` and `OSError` ✓

### Step 363: `from_test_failure` Repair Resume — PASS

- `tests_failed` checkpoint: `safe_to_resume=False`, `blocked_reason="resume_mode_not_implemented"` ✓
- No repair resume path exists — blocked cleanly ✓
- `_cmd_resume` falls through to unimplemented mode → `{"resumed": False, "blocked_reason": "resume_mode_not_implemented"}` ✓
- Test: `test_tests_failed_checkpoint_blocked` ✓

### Step 364: Dry-Run Accuracy — PASS

- `resume_dry_run` creates no events (no `append_run_event` in event_replay.py) ✓
- No calls to provider/source_apply/test_runner ✓
- `from_approval`: now returns `can_resume=False` (was True) ✓
- `from_apply`: returns `can_resume=True`, `would_run_stage="test_run"` ✓
- Blocked checkpoints: `can_resume=False` with precise `blocked_reason` ✓
- Updated tests: `test_dry_run_from_approved_blocked`, `test_dry_run_from_apply_resumable` ✓

### Step 365: CLI And UI Resume Truth — PASS

- `_cmd_resume` with unimplemented mode: `{"resumed": False, "blocked_reason": "resume_mode_not_implemented"}` ✓
- No `resumed=True` for blocked modes ✓
- `_cmd_checkpoints` text output: `[safe]`/`[blocked]` labels reflect new semantics ✓
- Dashboard `_build_resume_section`: dynamically uses updated `find_checkpoints()` — no UI code change needed ✓
- UI `ResumeCard`: `can_resume=True` only after patch applied (`source_apply_proven`) ✓
- No browser mutation buttons ✓

### Step 366: Full Baseline And Handoff — PASS

- pytest: 3922 passed, 7 skipped, 0 failed (independently re-run from repo root) ✓
- Vitest: 35 passed (independently re-run) ✓
- TypeScript: clean (independently re-run) ✓
- Build: OK ✓
- No `test_steps_*.py` ✓
- No `shell=True` in new code ✓
- source_apply gate intact ✓
- Resume cannot bypass gates ✓
- Dry-run creates no mutations/events ✓

---

## Final Verdict

**PASS**

R-12001 status: RESOLVED — `from_approval` no longer no-ops to success; blocked with `missing_patch_payload`
Checkpoint semantics status: PASS — only `source_apply_proven` is `safe_to_resume=True`; all others blocked with precise reasons; 4 pinning tests
from_approval status: PASS — blocked honestly, `missing_patch_payload`, no fake `resumed=True`
from_apply status: PASS — real test runner, permission gate, repo check, list argv, no raw output, honest pass/fail
from_test_failure status: PASS — blocked `resume_mode_not_implemented`, no fake repair claim
Dry-run mutation proof: PASS — no `append_run_event`, no subprocess calls in event_replay.py `resume_dry_run`
CLI/UI truth status: PASS — unimplemented → `resumed=False`; UI `can_resume` only after patch applied
Raw leak status: PASS — `capture_output=True` swallows test output; events only contain `passed: bool`
Full pytest verified: YES — 3922 passed, 7 skipped (independently re-run from repo root)
UI unit tests verified: YES — 35 Vitest passed (independently re-run)
TypeScript/build verified: YES — clean (independently re-run)

**Top 3 Risks:**
1. `from_apply` test discovery is limited (Makefile or pyproject.toml/tests dir). Edge case: project with neither marker gets `missing_test_candidate`. Correct behavior (blocked), but resume looks broken for unconventional projects.
2. `from_approval` is now blocked because "StructuredPatch is not persisted on job artifacts." If patch persistence is added later, checkpoint semantics need updating to re-enable this mode. Current behavior is safe and honest.
3. `test_next_command_catalog_valid` (from previous block) still checks only command GROUP level. For the new `remedy event replay {jid}` and `remedy job summary {jid}` commands in blocked checkpoints, the group "event" and "job" are in catalog_groups, so the test passes. Full subcommand validation not yet added.

**Top 3 Strengths:**
1. R-12001 fully resolved: no no-op success anywhere. The unimplemented mode fallback `{"resumed": False, "blocked_reason": "resume_mode_not_implemented"}` is a catch-all that makes adding new modes safe.
2. `from_apply` real implementation: permission gate, repo check, test discovery, subprocess with no shell, `capture_output=True`, honest pass/fail output. This is the only safe mode and it's properly gated.
3. Regression tests: `TestR12001Regression` class with 2 pinning tests ensures the fix stays. New dry-run tests update the contract accurately.

**Concrete Improvements:**
- When patch persistence is implemented, re-enable `from_approval` → `source_apply` path and add a test.
- Upgrade `test_next_command_catalog_valid` to check full subcommand (group + sub) against catalog.
- Document which resume modes are planned for future blocks in `.agent/context.md`.

**Merge readiness:** PASS. R-12001 fully resolved. All safety gates intact. Full baseline green. No open findings. Commit 49e880e ready.

**Watcher stopped because:** Commit 49e880e completes Steps 359-366. All claims independently verified. R-12001 resolved. No open findings. Stopping watcher.

---

## Previous Review History

### Steps 359-366: PASS — R-12001 resolved, checkpoint semantics honest, from_apply real test runner, all modes blocked or implemented correctly
### Steps 351-358: PASS WITH RISKS — event replay, checkpoints, CLI, dry-run, conservative resume (R-12001 open)
### Steps 343-350: PASS — token metrics, organic graph v2, 4-row layout
### Steps 335-342: PASS — Operator Cockpit v2, pipeline visibility, stop-reason UX
### Steps 329-334: PASS — stop_reason JSON repair, memory import fix, docs contract
### Steps 321-328: PASS WITH RISKS — Ollama wired into autorun, provider mode, stop-reason truth
### Steps 313-320: PASS — real-repo hardening, Ollama reliability, stop reasons, CLI docs
### Steps 305-312: PASS — structured patch pipeline, repair loop, operator visibility

---

# Live Review — Steps 351-358

Reviewer: parallel watcher (independent)
Scope: Steps 351-358 (Event Replay, Checkpoint Detection, CLI, Dry-Run, Safe Resume, UI Visibility)
Status: PASS WITH RISKS
Started: 2026-06-02
Commit reviewed: 0c589df (Steps 351-358)
Last check: final — all independently verified (3916 pytest, 35 Vitest, TypeScript clean) — R-12001 open

---

## Baseline (Steps 351-358 Block)

- Commit at block start: 8bb2e84 (Steps 343-350 final)
- Full pytest pre-block: 3898 passed, 7 skipped, 0 failed (verified)
- Vitest pre-block: 35 tests
- TypeScript: clean
- Committed: 14 files (5 Python + 4 TypeScript + 2 CSS + 3 test)
- +18 pytest: 3898→3916. Vitest unchanged: 35.

---

## Active Findings

### Finding R-12001

Status: Open
Severity: medium
Area: resume
Summary: `from_approval` resume claims to run source_apply but does nothing
Details: `_cmd_resume` with `from_approval` calls `run_autorun(..., builder_provider="none", autonomy_level=3)`. With `builder_provider="none"`, `result.stage = "builder_skipped_no_worker"`, not `"builder_complete"`. The approval gate condition is `if autonomy_level >= 3 and result.stage == "builder_complete"` — never fires. Source_apply never runs.
The operator sees "Resumed from approval_recorded. Stage: builder_skipped_no_worker" — looks like nothing happened, which is correct but misleading.
Dry-run says `would_run_stage: "source_apply"` — accurate intent — but actual resume doesn't deliver it.
Evidence:
- `apps/cli/commands/job.py`: `run_autorun(..., builder_provider="none", ...)` returns `stage="builder_skipped_no_worker"`
- `packages/orchestration/autorun.py:222`: approval gate requires `result.stage == "builder_complete"`
- Commit message says "from_approval mode fully wired (continue to source_apply)" — incorrect
Expected fix: Either (a) implement `from_approval` resume via a direct source_apply call with the existing approved intent, or (b) clearly document/output that V1 does not actually execute the apply step and update dry-run to say `would_run_stage: "not_implemented_v1"`.

---

## Resolved Findings

(none — R-12001 is the sole finding)

---

## Step-by-Step Review

### Step 351: Preflight + UI Layout Regression Guard — PASS

- Git clean at start ✓
- `.claude/` in `.gitignore` (from 8fc6bef) ✓
- No `test_steps_*.py` files ✓
- Layout guard added: `tests/ui_contracts/test_main_layout_guard.py` (5 tests) ✓
- Tests verify: exactly 4 main column children, expected components, no PipelinePanel in main, 4 CSS rows, PipelinePanel in right panel ✓
- All 5 tests pass (independently verified) ✓
- Not brittle pixel tests — uses regex structural analysis ✓

### Step 352: Event Replay Model — PASS

- `event_replay.py` created: `replay_job()`, `find_checkpoints()`, `resume_dry_run()` ✓
- `JobReplayState` reconstructed from real event ledger ✓
- All fields from safe event metadata (no raw prompts/output/diffs/source) ✓
- `degraded=True, degraded_reason="no_events"` for empty jobs ✓
- `redaction: "safe_metadata_only"` documented in all exports ✓
- `export_replay_json()`, `export_checkpoints_json()`, `export_dry_run_json()` — safe ✓
- 6 replay model tests: empty, fixture success, approval pending, parse failed, repair loop, no raw ✓

### Step 353: Safe Checkpoint Detection — PASS

- Checkpoints: context_ready, patch_intent_created, approval_recorded, source_apply_proven, tests_failed, tests_passed, stopped ✓
- `safe_to_resume=False` for: approval_pending, tests_passed (complete), stopped ✓
- `safe_to_resume=True` for: context_ready, approval_recorded, source_apply_proven, tests_failed (when repair budget remains) ✓
- `required_capabilities` and `required_approvals` populated on checkpoints ✓
- `next_command` in checkpoints is catalog-valid (`job`, `patch`, `event` groups) ✓
- 3 checkpoint tests ✓
- GAP: `test_next_command_catalog_valid` checks command group only, not full subcommand

### Step 354: CLI: Inspect Replay And Checkpoints — PASS

- `event replay <job_id> --json` in catalog as `event.replay`, `action_class="read_only"` ✓
- `job checkpoints <job_id> --json` in catalog as `job.checkpoints`, `action_class="read_only"` ✓
- `job resume <job_id> --checkpoint <id> --dry-run --json` in catalog as `job.resume` ✓
- Text output: only canonical stage IDs, stop reasons, checkpoint kinds — no raw content ✓
- Missing job → `sys.exit(1)` with simple error message (no traceback) ✓
- `export_replay_json` verified safe at export level ✓

### Step 355: Resume Dry-Run — PASS

- `--dry-run` flag calls `resume_dry_run()` which reads events but makes no writes ✓
- `can_resume: bool`, `would_run_stage: str`, `blocked_reason: str` output ✓
- Blocked checkpoints returned with `can_resume: False` ✓
- Missing checkpoint → `checkpoint_not_found` blocked ✓
- 3 dry-run tests pass ✓

### Step 356: Safe Resume v1 — PASS WITH RISKS

- `cp.safe_to_resume` check before any resume action ✓
- `resume_blocked` event emitted when not safe ✓
- `resume_started` event emitted before action ✓
- `from_approval` mode: calls `run_autorun` with `builder_provider="none"` ✓
- No raw content in resume events ✓
- Permission check via `requires_permission=True` in catalog ✓
- R-12001 (MEDIUM): `from_approval` claims source_apply but actually does nothing — builder skipped, approval gate never fires. Safe (no mutation), but functionally ineffective and commit message overclaimsrs.

### Step 357: Dashboard/UI Read-Only Replay And Resume Visibility — PASS

- `_build_resume_section` in dashboard: derived from `replay_job()` + `find_checkpoints()` ✓
- Returns: `replay_available`, `can_resume`, `latest_checkpoint` (safe metadata), `blocked_reason` ✓
- `except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError)` — specific, not broad ✓
- No raw content in resume section ✓
- `ResumeCard` in PipelinePanel: shows "Resume available" / "Resume blocked" ✓
- `next_command` clipboard-only (no navigation, no mutation) ✓
- `RemedyResume` + `RemedyResumeCheckpoint` TypeScript types added ✓
- `resume: dashboard.resume ?? null` in normalizeDashboardPayload ✓

### Step 358: Full Baseline And Handoff — PASS

- pytest: 3916 passed, 7 skipped, 0 failed (independently re-run from repo root) ✓
- Vitest: 35 passed (independently re-run) ✓
- TypeScript: clean (independently re-run) ✓
- Build: OK ✓
- No `test_steps_*.py` ✓
- No `shell=True` in new files ✓
- No broad `except Exception` (narrowed to specific types) ✓
- source_apply gate intact (approval gate condition unchanged) ✓
- Dry-run does not write ✓
- `.agent/plan.md` and `.agent/context.md` updated ✓

---

## Final Verdict

**PASS WITH RISKS**

Replay model status: PASS — events → safe metadata, degraded for empty, redaction documented, 6 tests
Checkpoint status: PASS — conservative boundaries, approval_pending blocked, tests_passed blocked, 3 tests
CLI status: PASS — all 3 commands in catalog, no raw output, missing job handled
Dry-run status: PASS — reads only, no mutations, blocked/can_resume output, 3 tests
Safe resume status: PASS WITH RISKS — gate enforced, resume_blocked event, R-12001: from_approval claims source_apply but delivers nothing
UI visibility status: PASS — read-only ResumeCard, clipboard command, no mutation
Raw leak status: PASS — safe metadata only throughout, specific exception handlers, `redaction` field in all exports
Full pytest verified: YES — 3916 passed, 7 skipped (independently re-run)
UI unit tests verified: YES — 35 Vitest passed (independently re-run)
TypeScript/build verified: YES — `tsc --noEmit` clean (independently re-run)

**Top 3 Risks:**
1. R-12001 (MEDIUM): `from_approval` resume reports success ("Resumed from approval_recorded") but silently does nothing — `run_autorun(builder_provider="none")` returns `builder_skipped_no_worker`. Operator expects patch apply; gets no-op. Misleading output. Dry-run also overclaims `would_run_stage: "source_apply"`.
2. `test_next_command_catalog_valid` only checks command group ("job", "patch"), not full subcommand. A checkpoint with `remedy job nonexistent_command` would pass. Low risk since all next_commands are hardcoded strings in event_replay.py and currently catalog-valid.
3. `job.resume` without `--dry-run` is in the catalog with `may_mutate_repo=True` but V1 only implements no-op behavior for most resume modes. Gap between documentation and implementation.

**Top 3 Strengths:**
1. Conservative checkpoint safety — `safe_to_resume=False` for approval_pending, tests_passed, stopped states. No arbitrary event becomes resumable.
2. End-to-end redaction: `redaction: "safe_metadata_only"` on all export objects, `output_hash[:16]` truncation, no raw prompt/provider output anywhere in the pipeline.
3. Broad except narrowed: `except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError)` catches expected failures without swallowing programming errors — passes the `test_no_broad_except_exception_in_dashboard` quality gate.

**Concrete Improvements:**
- Fix R-12001: either (a) implement direct source_apply with existing approved intent in `from_approval` resume, or (b) update dry-run `would_run_stage` to `"not_implemented_v1"` and output "Resume registered (V1: apply not yet automated)".
- Add `test_next_command_fully_valid` that validates checkpoint `next_command` against full catalog subcommands (group + sub), not just group.
- Add a test verifying that real `job.resume` (non-dry-run) emits `resume_started` and `resume_completed` events without writing to the repo.

**Merge readiness:** PASS WITH RISKS. R-12001 is the sole finding (medium, not a safety blocker). All safety gates intact. Full baseline green. Acceptable to merge; R-12001 should be addressed in next block.

**Watcher stopped because:** Commit 0c589df completes Steps 351-358. All claims independently verified. R-12001 noted but not a safety blocker. Stopping watcher.

---

## Previous Review History

### Steps 351-358: PASS WITH RISKS — event replay, safe checkpoints, checkpoint CLI, dry-run, conservative resume v1 (R-12001: from_approval resume does nothing, misleads operator)
### Steps 343-350: PASS — token metrics (honest), organic graph v2, 4-row layout, compact UI
### Steps 335-342: PASS — Operator Cockpit v2, pipeline visibility, stop-reason UX
### Steps 329-334: PASS — stop_reason JSON repair, memory import fix, docs contract closure
### Steps 321-328: PASS WITH RISKS — Ollama wired into autorun, provider mode, stop-reason truth
### Steps 313-320: PASS — real-repo hardening, Ollama reliability, stop reasons, CLI docs
### Steps 305-312: PASS — structured patch pipeline, repair loop, operator visibility
### Steps 297-304: PASS — test polish, rollback cleanup, project memory integration
### Steps 289-296: PASS — test re-architecture, transactionality, dashboard truth
### Steps 283-288: PASS — full baseline green, all findings resolved

---

# Live Review — Steps 343-350

Reviewer: parallel watcher (independent)
Scope: Steps 343-350 (Visual Target Alignment, Token Metrics, Layout, Organic Graph v2, Baseline)
Status: PASS
Started: 2026-06-02
Commit reviewed: 8bb2e84 (Steps 343-350)
Last check: final — all claims independently verified (3898 pytest, 35 Vitest, TypeScript clean)

---

## Baseline (Steps 343-350 Block)

- Commit at block start: 8fc6bef (Steps 335-342 final)
- Full pytest pre-block: 3895 passed, 7 skipped, 0 failed (verified)
- Vitest pre-block: 31 tests
- TypeScript: clean
- Committed: 15 files (7 TypeScript + 3 CSS + 1 Python + 3 test + 1 gitignore-related)
- +3 pytest: 3895→3898. +4 Vitest: 31→35.

---

## Active Findings

(none open)

---

## Step-by-Step Review

### Step 343: Visual Target Audit And Preflight — PASS

- Git clean at start (only `.data/live_review.md` modified) ✓
- `.claude/` now in `.gitignore` (fixed in 8fc6bef) ✓
- Tests green at block start: 3895 passed ✓
- Worker identified layout issues (PipelinePanel as 5th row, oversized grid) ✓
- Backend truth contracts intact (stop_reason string, source_apply gate) ✓
- Plan updated: Steps 343-350 with layout issues documented ✓

### Step 344: Token Usage Metric Contract — IN PROGRESS

Backend (`packages/orchestration/ui_server.py`):
- `_build_token_usage(events)` reads `estimated_tokens` from event metadata ✓
- `total_tokens: None` when no data (not 0) ✓
- `known: bool` distinguishes zero vs unknown ✓
- `estimated: True` always — no false precision claim ✓
- `by_role` breakdown: context/memory/repair/planner/other ✓
- `missing_sources` list for incomplete data ✓
- No raw prompts/provider output — only metadata token counts ✓

Frontend (`TopMetricsBar.tsx`):
- Fifth metric: key="tokens", label="Tokens" ✓
- Shows "—" when value is 0 (unknown) ✓
- "estimated" label shown when tokens > 0 ✓
- Tooltip shows by_role breakdown on hover/focus ✓
- `tabIndex={m.tooltip ? 0 : undefined}` — keyboard accessible ✓
- `onFocus/onBlur` — focus accessible ✓
- `aria-label` on article element ✓
- `role="tooltip"` on tooltip div ✓
- `formatTokens()`: 1.5k / 1.5M formatting ✓
- CSS: `repeat(5, 1fr)` grid updated ✓

Tests added: 3 Python (`test_empty_job_unknown_tokens`, `test_context_tokens_counted`, `test_no_raw_content_in_token_usage`) + 4 Vitest (fifth metric, dash suffix, known tooltip, no raw prompt) ✓

### Step 345: Main Layout Proportions — IN PROGRESS

- PipelinePanel removed from main column ✓
- `RemedyShell.tsx`: only 4 rows remain (metrics, command, graph, timeline) ✓
- Row sizes reduced: metrics 78→56px, command 52→40px, timeline 118→80px ✓
- Gap reduced: 14→10px ✓
- `data-testid="main-column"` added ✓
- PipelinePanel moved to RightLivePanel ✓
- AddTaskButton removed (mutation button gone) ✓

### Step 346: Organic Brain Graph v2 — PASS

- `CLUSTER_DEFS` (radial starburst anchors) removed ✓
- Replaced with organic branching: `branchCount = Math.max(3, Math.min(6, realNodes.length/4))` ✓
- Branch nodes: `sourceKind: "layout_only"`, `clickable: false`, `state: "planned"` (not fake done) ✓
- Real nodes: `sourceKind: "real_brain"`, `clickable: true` ✓
- Particles reduced: 12/28/48 → 4/8/14 (ambient only) ✓
- Deterministic from seeded RNG ✓
- No fake completed nodes ✓

### Step 347: Bottom Phase Timeline v2 — PASS

- Padding reduced: 16→8px ✓
- Border-radius: 16→12px ✓
- Icons: 32-40px → 24px ✓
- Labels: 9px ✓
- Main line: 2→1px, margins 48→36px ✓
- `align-items: center` corrected ✓
- No fake/demo events ✓

### Step 348: Right Panel Compact Operator Stack — PASS

- PipelinePanel added to right panel ✓
- `AddTaskButton` removed (mutation button gone) ✓
- Status pill reduced: 38→32px ✓
- Gap reduced: 10→8px ✓
- `overflow-y: auto; scrollbar-width: thin` for overflow ✓
- No mutation calls ✓

### Step 349: Visual Scale, Accessibility, And Screenshot-Target Tests — PASS

- 4 Vitest token metric tests (5th metric, dash suffix, known tooltip, no raw) ✓
- 3 Python token tests (unknown, counted, no raw) ✓
- `tabIndex`, `onFocus/onBlur`, `aria-label` on TopMetricsBar metric items ✓
- `role="tooltip"` on tooltip div ✓
- `prefers-reduced-motion` in existing `test_reduced_motion_disables` ✓
- TypeScript type check clean ✓
- GAP: No dedicated test for "main layout not 5 rows" — verified by code inspection only

### Step 350: Full Baseline And Handoff — PASS

- pytest: 3898 passed, 7 skipped, 0 failed (independently re-run from repo root) ✓
- Vitest: 35 passed (independently re-run) ✓
- TypeScript: clean (independently re-run) ✓
- Build: OK ✓
- No `test_steps_*.py` ✓
- No `shell=True` in new files ✓
- No `0.0.0.0` in packages/apps ✓
- UI remains read-only (AddTaskButton removed, clipboard-only commands) ✓
- Token presented as estimated (not exact) ✓
- Graph does not fake completed work ✓
- `.agent/plan.md` and `.agent/context.md` updated ✓

---

## Final Verdict

**PASS**

Token metric status: PASS — estimated, honest unknown state, by_role breakdown, hover/focus tooltip, 7 tests
Layout proportions status: PASS — 4-row main grid, PipelinePanel in right panel, compact sizes
Organic graph status: PASS — branching tree, CLUSTER_DEFS removed, no fake done nodes, deterministic
Phase timeline status: PASS — compact rail, 24px icons, 9px labels, 1px line
Right panel status: PASS — compact stack, mutation button removed, scrollable overflow
Raw leak status: PASS — token totals only, no raw prompts/provider output in tooltip
Full pytest verified: YES — 3898 passed, 7 skipped (independently re-run from repo root)
UI unit tests verified: YES — 35 Vitest tests passed (independently re-run)
TypeScript/build verified: YES — `tsc --noEmit` clean (independently re-run)

**Top 3 Risks:**
1. No regression test for "main layout is exactly 4 rows." PipelinePanel removal from main is verified by code inspection only. If a future commit re-adds a component to main, no test will catch it.
2. `branchCount` minimum is 3 even for empty dashboards (no real nodes). This creates 3 decorative branches from nothing, which is aesthetic but could be confusing on truly empty jobs. Low probability of user confusion.
3. Token tooltip only tests data correctness, not hover/focus keyboard accessibility in a DOM environment. The `tabIndex`/`onFocus` attributes are correct but untested at runtime level.

**Top 3 Strengths:**
1. Token usage is honest end-to-end: `known: False`/`total_tokens: null` for empty jobs, `estimated: True` always, "estimated" label in UI. No synthetic token counts anywhere.
2. Graph CLUSTER_DEFS removal eliminates the starburst problem at the model layer. The real data drives branch count, branch nodes are `layout_only/clickable:false`, so no layout node can be mistaken for real work.
3. AddTaskButton (mutation risk) removed in same commit as right panel restructuring. No mutation buttons remain in the UI.

**Concrete Improvements:**
- Add a Vitest test: `normalizeDashboardPayload` result has metrics of length 5 and contains no `PipelinePanel` in main-column structure (or check `data-testid="main-column"` children count if DOM testing is added).
- Add Python test: `_build_force_brain_model` with empty nodes yields branch nodes with `clickable=false` and no `state="done"` branch nodes.
- Consider adding `aria-describedby` pointing to tooltip id on the metric article for proper ARIA tooltip association.

**Merge readiness:** PASS. All scope blockers clear. Full baseline green. No open findings. Token usage honest. Graph starburst removed. Commit 8bb2e84 ready.

**Watcher stopped because:** Commit 8bb2e84 completes Steps 343-350. All claims independently verified. No open findings. Stopping watcher.

---

## Security Checklist (Steps 343-350)

| Check | Status |
|-------|--------|
| No mutation buttons added | ✓ AddTaskButton removed |
| No mutation endpoints | ✓ |
| Token tooltip no raw prompts | ✓ by_role counts only |
| Token presented as estimated | ✓ "estimated" label |
| Token total null when unknown | ✓ not fake zero |
| No external fonts/CDNs | ✓ CSS local only |
| No shell=True | ✓ |
| PipelinePanel out of main | ✓ Step 345 |

---

## Previous Review History

### Steps 343-350: PASS — token metrics (honest), organic graph v2, 4-row layout, compact UI, full baseline green
### Steps 335-342: PASS — Operator Cockpit v2, pipeline visibility, stop-reason UX, read-only decision queue, full baseline green
### Steps 329-334: PASS — stop_reason JSON repair, memory import fix, docs contract closure, full baseline green
### Steps 321-328: PASS WITH RISKS — Ollama wired into autorun, provider mode, stop-reason truth, docs updated
### Steps 313-320: PASS — real-repo hardening, Ollama reliability, stop reasons, CLI docs
### Steps 305-312: PASS — structured patch pipeline, repair loop, operator visibility
### Steps 297-304: PASS — test polish, rollback cleanup, project memory integration
### Steps 289-296: PASS — test re-architecture, transactionality, dashboard truth
### Steps 283-288: PASS — full baseline green, all findings resolved
### Steps 277-282: PASS — R-4001/R-4002/R-4003 resolved
### Steps 269-276: PASS — R-3011/R-3012/R-3013 resolved, approval gate added
### Steps 261-268: PASS — dashboard-first UI, permission boundary, frontend tests
### Steps 253-260: PASS — contract repair, safety quick wins
### Steps 247-252: PASS — data-honest mission control
### Steps 227-246: PASS — Canvas Force Brain Graph

---

# Live Review — Steps 335-342

Reviewer: parallel watcher (independent)
Scope: Steps 335-342 (Operator Cockpit v2: Pipeline Visibility, Stop Reason UX, Decision Queue, Baseline)
Status: PASS
Started: 2026-06-02
Commit reviewed: 8fc6bef (Steps 335-342)
Last check: final — all steps complete, independently verified (3895 pytest, 31 Vitest, TypeScript clean)

---

## Baseline (Steps 335-342 Block)

- Commit at block start: cd1359c (Steps 329-334 final)
- Full pytest pre-block: 3886 passed, 7 skipped, 0 failed
- Vitest pre-block: 21 tests
- TypeScript: clean
- Worker current step: Step 336 (pipeline contract in dashboard v4)
- Committed: ui_server.py, 5 UI files, 5 new pipeline component files, 1 new Python test file, .gitignore

---

## Resolved Findings

### R-11001 — RESOLVED (8fc6bef)

Status: Resolved
Severity: was low
Area: preflight
Fix: `.claude/` added to `.gitignore` at line 216. ✓

---

## Step-by-Step Review

### Step 335: Repo And Dashboard Preflight — PASS

- Tests green at block start: 3886 passed, 7 skipped ✓
- Docs exist (`docs/autocoder-usage.md`) ✓
- `.data/` in `.gitignore` ✓
- `.claude/` NOT in `.gitignore` ✗ (R-11001, LOW, not a blocker)
- stop_reason JSON stays string (verified from Step 334) ✓
- source_apply gate intact (bridge unchanged) ✓
- Dashboard empty state honest (stale=true, all null) — verified in pipeline tests ✓
- Worker updated plan.md to Steps 335-342 ✓

### Step 336: Pipeline Status Contract — IN PROGRESS

- `_build_pipeline_section` wired into `_build_dashboard` ✓
- All fields derived from real job events via `_load_events(job)` ✓
- Unknown = null (parse_success: None, provider: None when no events) ✓
- `next_command` catalog-valid — verified all 7 generated commands ✓
- No raw content: only file_count/token_count/hash metadata ✓
- 9 Python tests in `tests/ui_server/test_pipeline_contract.py` — all pass ✓
- TypeScript types: `RemedyPipeline` added to `RemedyDashboard` as `pipeline: RemedyPipeline | null` ✓
- Existing v3/v4 dashboard fields unchanged — additive ✓
- `normalizePipeline` handles null/missing → returns `null` ✓

### Step 337: Pipeline Timeline Component — IN PROGRESS

- `PipelineTimeline.tsx`: renders 7-9 stages, correct states ✓
- States: done/current/blocked/failed/skipped/unknown/waiting (all `PipelineStepState`) ✓
- Empty: "No pipeline run yet" ✓
- No click handlers — read-only ✓
- Stop reason informs step state (parse failed → patch step "failed") ✓
- 10 Vitest tests: empty, fixture success, approval, parse fail, repair loop, no raw output, dashboard integration ✓
- 31 Vitest total passing ✓

### Step 338: Stop Reason Card + Next Safe Command — IN PROGRESS

- `StopReasonCard.tsx`: machine value in `<code>` + human label ✓
- STOP_LABELS covers 14 canonical stop reasons ✓
- Graceful fallback for unknown stop_reason ✓
- `next_command`: clipboard-only (`navigator.clipboard.writeText`) — no navigation, no mutation ✓
- No raw output leaks in component ✓

### Step 339: Read-Only Decision Queue — PASS

- `approval_required`, `approval_status`, `intent_id`, `intent_status` in pipeline data ✓
- Approval step in timeline shows blocked/approved state ✓
- `next_command` shows "remedy patch approve/show" commands ✓
- No browser mutation buttons ✓
- No mutation endpoints ✓
- No raw diff/approval reason/patch content ✓
- GAP: No dedicated decision queue component — intent path_count/op_count not shown (noted in improvements)

### Step 340: Repair Loop Visibility — IN PROGRESS

- `repair_loop.used`, `cycle_count`, `max_cycles` in pipeline section ✓
- Repair step shown in timeline only when `repairUsed=true` ✓
- Detail: "Cycle X/Y" (safe metadata, no raw test output) ✓
- Stop reason visible when budget exhausted ✓
- Empty jobs never show repair activity ✓

### Step 341: Memory And Source Context Visibility — IN PROGRESS

- `ContextCard.tsx`: file_count, test_file_count, estimated_tokens, truncated shown ✓
- Memory: item_count, truncated shown ✓
- "No context or memory injected" honest empty state ✓
- No raw file content, no raw memory content ✓
- No raw prompt/provider input ✓
- selection_hash/context_hash in data but NOT displayed in UI (good, reduces noise) ✓

### Step 342: Full Baseline And Handoff — PASS

- pytest: 3895 passed, 7 skipped, 0 failed (independently verified from repo root) ✓
- Vitest: 31 passed (independently verified) ✓
- TypeScript: clean — `tsc --noEmit` exits 0 (independently verified) ✓
- Build: OK ✓
- No `tests/test_steps_*.py` ✓
- No `shell=True` in new files ✓
- No `0.0.0.0` in packages/apps (ui_server docs: "127.0.0.1 only") ✓
- source_apply gate intact (ui_server reads apply status, doesn't invoke apply) ✓
- `.claude/` in `.gitignore` (R-11001 resolved) ✓
- `.agent/context.md` and `.agent/plan.md` updated ✓
- `.data/live_review.md` has Steps 335-342 section ✓

---

## Final Verdict

**PASS**

Dashboard pipeline contract status: PASS — 30+ fields from real event ledger, null when unknown, 9 Python tests
UI pipeline timeline status: PASS — PipelineTimeline with 8-10 steps, 7 states, honest empty state, 10 Vitest tests
Stop reason card status: PASS — machine value + human label + 14 canonical reasons + clipboard-only next_command
Decision queue status: PASS — approval_required/status/intent_id in pipeline; approval step shows blocked state; next_command shows patch approve command. No explicit path_count/op_count display.
Repair loop visibility status: PASS — repair step in timeline when used, cycle X/Y detail, no raw test output
Memory/context visibility status: PASS — ContextCard shows file_count/tokens/item_count; honest "No context" empty state
Raw leak status: PASS — no raw_stdout/stderr/command_output/diff_preview in new components
Full pytest verified: YES — 3895 passed, 7 skipped (independently re-run from repo root)
UI unit tests verified: YES — 31 Vitest tests passed (independently re-run)
TypeScript/build verified: YES — `tsc --noEmit` clean (independently re-run)

**Top 3 Risks:**
1. `buildPipelineSteps` client-side step state logic is complex (9 steps, conditional booleans). Covered by 10 Vitest tests for key scenarios. Risk: edge-case state combinations (e.g., intent approved but apply_status "failed") may show misleading states. No safety impact — display only.
2. Decision queue shows no path_count or op_count for patch intents. An operator approving a multi-file patch has no count metadata in the UI to preview impact. Must use CLI (`remedy patch show`) to inspect.
3. `next_command` in StopReasonCard contains real job_id and intent_id from pipeline data. These are safe (UUIDs, no raw content), but the field is shown verbatim in UI code. If intent_id is empty but approval_required, the command becomes "remedy patch approve <job_id> " with trailing space — cosmetic issue only.

**Top 3 Strengths:**
1. Full data contract — backend `_build_pipeline_section()` derives every field from real job events, with `null`/empty for unknowns, `stale=True` for empty jobs. No fake pipeline data ever appears.
2. Defense-in-depth on raw content: `scrubUiText()` scrubs forbidden strings from task labels; pipeline components only display metadata (counts, hashes, canonical IDs); test `test_no_raw_content_in_pipeline` verifies end-to-end.
3. R-11001 fixed in same commit — `.claude/` in `.gitignore` prevents accidental tooling state commits.

**Concrete Improvements:**
- Add intent path_count and op_count to decision queue display (from `builder_patch_parsed` event `target_path_count` metadata) for operator pre-approval awareness.
- Guard `next_command` for empty intent_id: if `stop_reason == "approval_required"` but `intent_id == ""`, show "remedy patch list {job_id}" instead of "remedy patch approve {job_id} ".
- Add `test_approval_required_no_intent_id` to pipeline contract tests to pin this edge case.

**Merge readiness:** PASS. All scope blockers clear. Full baseline green. No open findings. Read-only UI confirmed. Commit 8fc6bef ready.

**Watcher stopped because:** Commit 8fc6bef completes Steps 335-342. All steps independently verified. No open findings. 10-minute no-change window would apply from now; stopping early since commit signals block completion.

---

## Security Checklist (Steps 335-342)

| Check | Status |
|-------|--------|
| No 0.0.0.0 in ui_server | ✓ documented "127.0.0.1 only" |
| No mutation endpoints | ✓ "No POST/PUT/DELETE" |
| No browser mutation buttons | ✓ clipboard copy only |
| No raw provider output in pipeline | ✓ |
| No raw source/diff/memory in pipeline | ✓ |
| No raw test output | ✓ |
| No approval reason displayed | ✓ |
| No fake/demo pipeline data | ✓ event-ledger driven |
| No shell=True | ✓ |
| No external fonts/CDNs | ✓ CSS local only |
| Empty pipeline honest (stale=True) | ✓ |
| .claude/ gitignored | ✗ R-11001 |

---

## Previous Review History

### Steps 335-342: PASS — Operator Cockpit v2, pipeline visibility, stop-reason UX, read-only decision queue, full baseline green
### Steps 329-334: PASS — stop_reason JSON repair, memory import fix, docs contract closure, full baseline green
### Steps 321-328: PASS WITH RISKS — Ollama wired into autorun, provider mode, stop-reason truth, docs updated (R-10001 open)
### Steps 313-320: PASS — real-repo hardening, Ollama reliability, stop reasons, CLI docs (all resolved)
### Steps 305-312: PASS — structured patch pipeline, repair loop, operator visibility
### Steps 297-304: PASS — test polish, rollback cleanup, project memory integration
### Steps 289-296: PASS — test re-architecture, transactionality, dashboard truth
### Steps 283-288: PASS — full baseline green, all findings resolved
### Steps 277-282: PASS — R-4001/R-4002/R-4003 resolved
### Steps 269-276: PASS — R-3011/R-3012/R-3013 resolved, approval gate added
### Steps 261-268: PASS — dashboard-first UI, permission boundary, frontend tests
### Steps 253-260: PASS — contract repair, safety quick wins
### Steps 247-252: PASS — data-honest mission control
### Steps 227-246: PASS — Canvas Force Brain Graph

---

# Live Review — Steps 329-334

Reviewer: parallel watcher (independent) — overrides worker self-review
Scope: Steps 329-334 (Docs Update, Stop Reason JSON Repair, Memory Injection Fix, CLI Path Tests, Command Contract, Baseline)
Status: PASS
Started: 2026-06-02
Commit baseline: 639e5ed (Steps 321-328)
Last check: final — all claims independently verified (memory module, R-10001 reproduction, Vitest, TypeScript, full pytest)

---

## Baseline (Steps 329-334 Block)

- Commit at block start: 639e5ed (Steps 321-328 final)
- Full pytest pre-block: 3869 passed, 7 skipped, 0 failed
- Full pytest post-block: 3886 passed, 7 skipped, 0 failed (+17 tests net)
- Vitest: 21 passed
- TypeScript: clean (no errors)
- Build: OK
- Carry-forward resolved: R-10001, N-10001, N-10002

---

## Resolved Findings

Done: R-10001 - stop_reason no longer clobbered with boolean False in JSON output. Removed "stop_reason" from events key tuple in autorun.py. do_cmd.py now uses _BOOL_EVENTS whitelist — only known boolean events get `val == "True"` conversion, others stay as strings. Events already in `out` (like stop_reason from result fields) skip. 5 tests prove stop_reason stays string for prose/unavailable/approval/false-check.

Done: N-10001 - `unsafe_path` and `path_traversal` restored as separate rows in docs/autocoder-usage.md stop reasons table.

Done: N-10002 - Memory import fixed. `from packages.memory.format_memory import format_memory_section` → `from packages.memory.context_summary import build_memory_context, format_memory_section`. Now calls `build_memory_context()` first, then `format_memory_section(summary)`. Degradation metadata explicit: `memory_context_attached`, `memory_error_kind`, `memory_item_count`, `memory_context_hash`, `memory_truncated`. No broad `except Exception: pass`.

---

## Step-by-Step Review

### Step 329: Autocoder Usage Docs — PASS

- Pipeline overview section added (Builder → Parse → Intent → Approval → Apply → Test → Proof) ✓
- VRAM free: `remedy worker unload --provider ollama --all` (catalog-valid) ✓
- Warning: "Real Ollama is local, model-quality-dependent, and not guaranteed" ✓
- "Normal CI does not require Ollama" ✓
- Patch inspect: `remedy patch list/show/approve/reject/apply` ✓
- Test: `remedy test run` ✓
- `unsafe_path` and `path_traversal` in stop reasons table ✓
- All tests pass including docs contract tests ✓

### Step 330: Stop Reason JSON Repair — PASS

- Removed `"stop_reason"` from events key tuple at autorun.py Ollama path ✓
- `do_cmd.py`: `_BOOL_EVENTS` whitelist replaces blanket `val == "True"` ✓
- Events already in `out` dict skip (no clobber) ✓
- Non-boolean events pass through as strings ✓
- 5 tests: prose stays string, unavailable stays string, approval stays string, never boolean false, booleans stay booleans ✓

### Step 331: Memory Injection Import And Degradation — PASS

- Import fixed: `packages.memory.context_summary` (correct module) ✓
- Calls `build_memory_context()` → `format_memory_section(summary)` ✓
- `memory_metadata` populated: `memory_context_attached`, `memory_item_count`, `memory_context_hash`, `memory_truncated` ✓
- Specific exception handling: ImportError, OSError, Exception with distinct `memory_error_kind` ✓
- No broad `except Exception: pass` ✓
- When no memory: `memory_context_attached=False`, `memory_error_kind` recorded ✓

### Step 332: Real CLI Path Regression Tests — PASS

- `tests/cli/test_do_cmd_cli_path.py` created (9 tests) ✓
- `TestStopReasonJsonIntegrity`: prose, unavailable, approval, never-false, booleans ✓
- `TestFixtureCliPath`: deterministic, source_apply gated at autonomy 2 ✓
- `TestDefaultProviderSafe`: default doesn't call Ollama ✓
- `TestNoRawLeakInJson`: SECRET_API_KEY not in JSON output ✓
- All use `_capture_json_output()` matching actual do_cmd.py logic ✓

### Step 333: Docs Command Contract And Operator Hints — PASS

- `TestDocsCommandContract`: extracts `remedy ...` commands, validates group+sub against CATALOG ✓
- `TestDocsCommandContract::test_docs_do_commands_valid`: validates --flags against do.run args ✓
- Additional docs tests: pipeline overview, stop reasons complete, VRAM free, model warning, patch commands, test run ✓
- All 26 new+modified tests pass ✓

### Step 334: Full Baseline And Handoff — PASS

- pytest: 3886 passed, 7 skipped, 0 failed (batched) ✓
- Vitest: 21 passed ✓
- TypeScript: clean ✓
- Build: OK ✓
- No shell=True in packages/apps ✓
- No 0.0.0.0 in packages/apps ✓
- No unittest.mock in packages/ ✓
- No test_steps_*.py ✓
- source_apply gate intact ✓
- stop_reason stays string in JSON ✓
- Memory import valid, no swallowed error ✓
- Docs exist with accurate commands ✓

---

## Final Verdict

**PASS**

All carry-forward findings resolved. Full baseline green. No new risks.

---

## Previous Review History

### Steps 329-334: PASS — stop_reason JSON repair, memory import fix, docs contract closure, full baseline green
### Steps 321-328: PASS WITH RISKS — Ollama wired into autorun, provider mode, stop-reason truth, docs updated (R-10001 open)
### Steps 313-320: PASS — real-repo hardening, Ollama reliability, stop reasons, CLI docs (all resolved)
### Steps 305-312: PASS — structured patch pipeline, repair loop, operator visibility
### Steps 297-304: PASS — test polish, rollback cleanup, project memory integration
### Steps 289-296: PASS — test re-architecture, transactionality, dashboard truth
### Steps 283-288: PASS — full baseline green, all findings resolved
### Steps 277-282: PASS — R-4001/R-4002/R-4003 resolved
### Steps 269-276: PASS — R-3011/R-3012/R-3013 resolved, approval gate added
### Steps 261-268: PASS — dashboard-first UI, permission boundary, frontend tests
### Steps 253-260: PASS — contract repair, safety quick wins
### Steps 247-252: PASS — data-honest mission control
### Steps 227-246: PASS — Canvas Force Brain Graph

---

# Live Review — Steps 321-328

Reviewer: parallel watcher (independent)
Scope: Steps 321-328 (Provider Mode, OllamaBuilder Autorun, Stop Reasons, Real CLI Smoke, Prompt Quality, Docs, Baseline)
Status: PASS WITH RISKS
Started: 2026-06-02
Commit reviewed: 639e5ed (Steps 321-328: Wire Ollama into remedy do, stop-reason truth, provider-mode)
Last check: final — R-10001 unresolved in commit, all else verified

---

## Baseline

- Commit at block start: b042618 (Steps 313-320 final)
- Full pytest pre-block: 3838 passed, 5 skipped, 0 failed
- Full pytest post-commit (639e5ed): 3869 passed, 7 skipped, 0 failed (+31 tests net)
- Vitest: not re-run (no UI changes this block)
- TypeScript/build: not re-run (no UI changes this block)

---

## Active Findings

### Finding R-10001

Status: Open (committed unfixed in 639e5ed)
Severity: medium
Area: stop-reasons
Summary: JSON output (`--json`) clobbers `stop_reason` string with boolean `False`
Details: `run_autorun` appends `{"event": "stop_reason", "value": "provider_output_prose_only"}` to `result.events` (autorun.py:216). `do_cmd.py` JSON output path applies `val == "True"` to every event including stop_reason, overwriting the string with `False`. An operator using `remedy do --builder-provider ollama --json` with a failing model gets `"stop_reason": false` instead of `"stop_reason": "provider_output_prose_only"` — specific failure reason lost.

Reproduction confirmed:
```
result.stop_reason: 'provider_output_prose_only'
out["stop_reason"] after events loop: False
```

Evidence:
- `packages/orchestration/autorun.py:213-218`: "stop_reason" in events key list for Ollama path
- `apps/cli/commands/do_cmd.py:85-89`: events loop `out[key] = val == "True"` for all events
- Test `test_json_output_has_stop_reason_and_provider` constructs dict directly — doesn't catch this

Expected fix: Remove "stop_reason" from the key tuple at autorun.py:216. `result.stop_reason` already carries the value. Add an integration test that runs through the events loop (mirrors the actual `do_cmd.py` JSON path).

---

## Resolved Findings

### R-10002 — RESOLVED (639e5ed)

Status: Resolved
Severity: high (was)
Area: cli-docs
Fix: `docs/autocoder-usage.md` updated:
- `--builder-provider fixture/ollama` Quick Start commands added ✓
- Builder Providers table (none/fixture/ollama) added ✓
- "future step / not yet wired" note removed ✓
- Test `test_docs_mention_builder_provider` + `test_docs_commands_use_builder_provider` added ✓

---

## Minor Notes (not blockers)

### N-10001 (LOW)
Docs stop reasons table dropped `unsafe_path` and `path_traversal` as distinct entries, merged into `validation_failed`. Both remain valid STOP_REASONS in builder_bridge.py. Operators seeing these in JSON output won't find them in the table.

### N-10002 (LOW)
`autorun.py:649`: `from packages.memory.format_memory import format_memory_section` — module path wrong, caught by `except Exception`, memory context silently never injected into Ollama prompt. Functional gap only, no safety impact.

---

## Step-by-Step Review

### Step 321: Close Review Truth Gaps — PASS

All 313-320 findings resolved in b042618. R-10002 addressed in this block. No stale claims. ✓

### Step 322: Explicit Builder Provider Mode — PASS

- `--builder-provider none|fixture|ollama` in CLI and catalog ✓
- Default `none` (no implicit Ollama) ✓
- Invalid value → SystemExit(2) ✓
- Catalog entry matches `_VALID_PROVIDERS` ✓
- 4 parser tests + catalog test pass ✓

### Step 323: OllamaBuilder Wired Into Autorun — PASS

- `_run_ollama_builder` calls `OllamaBuilder().build()` ✓
- Output through `run_builder_bridge` (parse → intent → approve → source_apply → test) ✓
- Approval gate at autonomy < 3 ✓
- Unavailable provider → `provider_unavailable` stop_reason ✓
- `autorun_builder_completed` emits only `provider` + `has_structured_patch` (bool, no raw) ✓
- `test_ollama_valid_patch_creates_intent`: proof_collected on mock success ✓
- `test_no_raw_output_in_events`: SECRET_KEY not in events ✓

### Step 324: Stop Reason Propagation — PASS WITH RISKS

- `AutorunResult.stop_reason` populated correctly ✓
- CLI text output: correct (`Stop reason: provider_output_prose_only`) ✓
- JSON output: BUG — specific stop_reason string overwritten with `False` ✗ (R-10001)
- Dashboard canonical stop_reason: unchanged, still correct ✓
- Tests: `test_json_output_has_stop_reason_and_provider` doesn't cover CLI JSON path ✗

### Step 325: Real `remedy do` Ollama Smoke — PASS

- `tests/orchestration/test_real_do_ollama_smoke.py` added ✓
- `TestFixtureDoSmoke` (2 tests): always run, CI-safe, tests actual `run_autorun` path ✓
- `TestRealDoOllamaSmoke` (2 tests): gated by `REMEDY_REAL_OLLAMA_SMOKE=1`, skips cleanly ✓
- Real smoke path: uses `builder_provider="ollama"` not pytest-only Ollama ✓
- Assertions cover pipeline behavior not guaranteed model success ✓
- Raw leak check: `assert "def hello" not in meta_str` ✓
- Result: 2 passed, 2 skipped ✓

### Step 326: Builder Prompt Quality — PASS

- Prompt strengthened: relative paths only, no shell commands, no secret files, full content not diff, no wrapper text ✓
- `format=schema` JSON enforcement ✓
- `_extract_first_json_object`: handles trailing text, escape-aware implementation ✓
- `test_trailing_explanation_after_json` passes ✓
- 18 mocked Ollama failure cases in test_ollama_patch_reliability.py ✓
- 14 prompt quality tests in test_builder_prompt_quality.py all pass ✓
- Memory context silently fails (N-10002, LOW) ✗

### Step 327: Operator Docs And Command Contract — PASS

- Docs updated: `--builder-provider` documented with table ✓
- All Quick Start commands catalog-valid ✓
- `remedy dev status --json` hint valid (`dev.status` has `--json` arg) ✓
- "future step" note removed ✓
- Stop reasons table: minor inaccuracy (N-10001, LOW) ✓
- No git commit/browser mutation/network ops added ✓

### Step 328: Baseline — PASS WITH RISKS

- pytest: 3869 passed, 7 skipped, 0 failed ✓
- +31 net new tests ✓
- No `tests/test_steps_*.py` files ✓
- source_apply gate intact ✓
- structured patch requires intent (bridge unchanged) ✓
- Real Ollama CLI status: honest in docs ✓
- fixture smoke passes ✓
- `.data/live_review.md`: updated ✓
- `.agent/plan.md`: updated ✓
- R-10001 in committed code: JSON stop_reason clobbered ✗

---

## Final Verdict

**PASS WITH RISKS**

Provider mode status: PASS — `--builder-provider none|fixture|ollama` wired correctly, catalog matches, default safe
Ollama autorun status: PASS — `_run_ollama_builder` calls OllamaBuilder through full bridge pipeline
Real `remedy do` Ollama smoke status: PASS — gated by env, 2 CI-safe fixture tests always run
Stop reason propagation status: PASS WITH RISKS — text output correct; JSON output loses stop_reason string (R-10001)
Docs/command validity status: PASS — `--builder-provider` documented, commands catalog-valid
Raw leak status: PASS — no raw provider/source/secret content in events
Full pytest verified: YES — 3869 passed, 7 skipped
UI unit tests verified: NOT RE-RUN (no UI changes this block)
TypeScript/build verified: NOT RE-RUN (no UI changes this block)

**Top 3 Risks:**
1. R-10001 (MEDIUM): `remedy do --builder-provider ollama --json` outputs `"stop_reason": false` instead of the specific reason string — specific failure lost in machine-readable output. Consumer scripts or operators using `--json` get no useful signal on why the pipeline stopped.
2. N-10002 (LOW): Memory context never injected into OllamaBuilder prompt (wrong import path, silently fails). Model has no project memory — prompts less effective but no safety impact.
3. N-10001 (LOW): `unsafe_path` and `path_traversal` stop reasons removed from docs table. Still fire in production; operators won't find them in the docs.

**Top 3 Strengths:**
1. Full pipeline wiring — OllamaBuilder output flows through parse → intent → auto-approve → source_apply → test with no bypass. Approval gate enforced at autonomy < 3 and tested.
2. Prompt hardening — explicit rules forbid shell commands, secret files, path traversal, non-relative paths, and prose. `format=schema` enforces JSON output. Parser handles trailing text via `_extract_first_json_object`.
3. Honest CI smoke — `TestFixtureDoSmoke` (always-run) uses real `run_autorun` path with `builder_provider="fixture"`, not a synthetic mock. Real Ollama path gated and clearly labeled opt-in.

**Concrete Improvements:**
- Fix R-10001: remove "stop_reason" from events key tuple at autorun.py:216. Add test verifying `out["stop_reason"]` is a string after the events loop.
- Fix N-10002: change `from packages.memory.format_memory import format_memory_section` → `from packages.memory.context_summary import format_memory_section` (and handle its required argument, or use a no-arg wrapper).
- Fix N-10001: restore `unsafe_path` and `path_traversal` rows to the stop reasons table.

**Merge readiness:** PASS WITH RISKS. R-10001 is the sole unfixed finding. All safety gates intact. Full baseline green. Acceptable to merge; R-10001 can be a follow-up fix.

**Watcher stopped because:** Worker committed 639e5ed completing Steps 321-328. R-10001 remains open but is not a safety blocker. 10-minute no-change window would now apply; stopping early since commit signals block completion.

---

## Security Checklist

| Check | Status |
|-------|--------|
| No shell=True in new files | ✓ |
| No raw provider output in events | ✓ |
| No raw source/diff/prompt in events | ✓ |
| Approval gate intact (autonomy < 3) | ✓ |
| Source_apply gate intact (intent required) | ✓ |
| Provider unavailable handled safely | ✓ |
| Ollama gated behind explicit --builder-provider | ✓ |
| No implicit Ollama calls (default=none) | ✓ |
| No 0.0.0.0 bindings | ✓ |
| No external network deps in CI tests | ✓ |
| Real Ollama smoke skips cleanly when env unset | ✓ |
| JSON stop_reason string preserved | ✗ R-10001 |
| Docs honest about CLI Ollama support | ✓ R-10002 resolved |
| OllamaBuilder prompt discourages prose | ✓ |
| Parser handles trailing text safely | ✓ |
| No secrets in prompt or events | ✓ |

---

## Previous Review History

### Steps 321-328: PASS WITH RISKS — Ollama wired into autorun, provider mode, stop-reason truth, docs updated (R-10001 open)
### Steps 313-320: PASS — real-repo hardening, Ollama reliability, stop reasons, CLI docs (all resolved)
### Steps 305-312: PASS — structured patch pipeline, repair loop, operator visibility
### Steps 297-304: PASS — test polish, rollback cleanup, project memory integration
### Steps 289-296: PASS — test re-architecture, transactionality, dashboard truth
### Steps 283-288: PASS — full baseline green, all findings resolved
### Steps 277-282: PASS — R-4001/R-4002/R-4003 resolved
### Steps 269-276: PASS — R-3011/R-3012/R-3013 resolved, approval gate added
### Steps 261-268: PASS — dashboard-first UI, permission boundary, frontend tests
### Steps 253-260: PASS — contract repair, safety quick wins
### Steps 247-252: PASS — data-honest mission control
### Steps 227-246: PASS — Canvas Force Brain Graph

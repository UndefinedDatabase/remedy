# Live Review — Steps 4917-4926: Job Evidence Nested Path Containment Closure v1

## Verdict (reviewer-owned)
**PASS** @ ca897c0
All 6 findings (R-3501 through R-3506) resolved. 53 tests. 7976 full suite.

---

# Live Review — Steps 4927-4936: Job Evidence Symlink Containment Closure v2

## Verdict (reviewer-owned)
**PASS** @ de8c6f1
All 6 findings (R-3601 through R-3606) resolved. 53 tests. 7976 full suite.

---

# Live Review — Steps 4937-4944: Real Job Evidence Export Dogfood Audit

## Verdict (reviewer-owned)
**BLOCKED** — No export artifacts at `/tmp/remedy-job-evidence-5b7cb31539f947ba/`.

---

# Live Review — Steps 4945-4960: Job Final Review + Human-Approved Job Promote v0

## Verdict (reviewer-owned)
**PASS** @ 2684ae7 (assessed at e5715c5 with v1 safety closure applied)

v0 delivers core promotion with correct gates, CLI, dry-run, post-test, and persistence.
46 promote tests pass. 8020 full suite (3 pre-existing/environmental failures only).

### Verified
- Dry-run does not mutate target (4 tests)
- `--approve` required; CLI defaults to dry_run=True (1 test)
- No git commit/push/reset/checkout in code (grep verified — only in docstrings)
- Readiness gates: job completed, tasks applied, run_id, reviewer pass, tests pass, target guard (7 gate tests)
- Unsafe files blocked: traversal, .env, private keys, absolute paths (2 tests + approve-path tests)
- Post-apply content verification
- Promotion record persisted (2 tests)
- CLI catalog entry (`may_mutate_repo=True`, `may_execute_commands=True`, `supports_json=True`)
- CLI handler JSON + text output (5 tests)
- Post-test command: `shlex.split`, no `shell=True`, timeout 120s, output capped 10K (2 tests)
- `subprocess.run` only in `_run_post_test` for user-provided test command — no git subprocess calls

All 10 findings (R-3501 through R-3510) resolved — v0 core logic sound, safety hardened by v1.

---

# Live Review — Steps 4961-4974: Job Promote Safety Closure v1

Reviewer: parallel reviewer (independent; owns verdict).
Builder must NOT write reviewer verdicts. Builder must NOT self-merge.
Builder must NOT mark findings as resolved.
Timestamp: 2026-06-26

## Verdict (reviewer-owned)
**PASS** @ e5715c5
All 8 findings resolved. 46 promote tests. 8020 full suite (3 pre-existing/environmental).

## Findings

### R-3601 Blocker — Approved promote overwrites dirty target paths
**Resolved.** `_check_target_cleanliness()` at L250 compares target files against workspace. Dirty files block with `dirty_planned_target_paths`. Test `test_dirty_target_path_blocks_promote` passes. `test_clean_target_allows_promote` confirms clean path succeeds with `target_clean=True`.

### R-3602 Blocker — Workspace symlink leaks external contents
**Resolved.** `_validate_source_containment()` at L88: checks `is_symlink()`, `.resolve()` for escape, `is_file()` for regular, parent symlink walk. Three tests pass: `test_workspace_source_symlink_blocks`, `test_workspace_parent_symlink_blocks`, `test_target_dest_symlink_escape_blocks`. `_validate_dest_containment()` at L133 blocks destination symlink escapes.

### R-3603 Blocker — Promotion uses broad workspace fallback
**Resolved.** `_collect_workspace_files()` removed entirely. L370: explicit apply manifest required for every task (`missing_apply_manifest` block). L393: files collected from manifests only. L396: `no_files_in_apply_manifests` if empty. Three tests pass: `test_no_apply_manifest_blocks`, `test_empty_apply_manifest_blocks`, `test_pending_apply_manifest_blocks`.

### R-3604 High — Target cleanliness check is not immediate
**Resolved.** Two checks: first at L457 (before dry-run exit), second at L480 immediately before apply loop (`target_changed_before_apply` block). TOCTOU window minimized to validation + writability preflight between checks.

### R-3605 High — Promotion record failure is silently swallowed
**Resolved.** `_persist_job_promotion()` at L560 no longer wraps in `try/except OSError: pass` — raises on failure. Preflight writability check at L469 tests write/unlink before apply. Test `test_unwritable_promo_dir_blocks_approved` (monkeypatched `_promotions_dir` to `/nonexistent/readonly/path`) passes.

### R-3606 High — Tests do not exercise real CLI path
**Resolved.** `TestCLICommandPaths` at L1032: `test_cli_approve_applies` (full approve through CLI handler, verifies `promoted` + files), `test_cli_blocked_json` (nonexistent job → blocked JSON), `test_cli_text_blocked` (nonexistent job → blocked text). All pass.

### R-3607 Medium — Promotion output leaks secrets
**Resolved.** JSON export at L613: `_redact_json_value(raw)` on entire dict. Paths: `_sanitize_path()` for `target_repo` and `job_workspace_path`. `post_test_command_present` (bool) replaces raw command string. Text summary: `_redact_secrets()` wraps full output at L694. `_sanitize_path()` for target in text. Post-test summary removed from text output. Three redaction tests pass.

### R-3608 Medium — Existing safety regresses
**Resolved.** All 30 original v0 tests still pass. 16 new v1 tests added. 46 total. Full suite 8020 passed. No regressions. Pre-existing failures: `test_full_chain_order` (provenance chain, unrelated) + 2 lock contention tests (environment-dependent).

## Notes
v1 diff: +645 lines across `job_promote.py` (241 changed) + `test_job_promote.py` (453 added) + `plan.md`. Clean safety closure — no workspace fallback, source/dest containment, target cleanliness with immediate recheck, persistence raised not swallowed, full redaction pipeline.

---

# Live Review — Steps 4975-4990: Job Promote Baseline-Aware Safety Closure v2

Reviewer: parallel reviewer (independent; owns verdict).
Builder must NOT write reviewer verdicts. Builder must NOT self-merge.
Builder must NOT mark findings as resolved.
Timestamp: 2026-06-26

## Verdict (reviewer-owned)
**PASS** @ 6d55071
Baseline-aware promotion replaces naive target-vs-workspace comparison.
`AppliedFileProof` records pre-job hash. `_check_baseline_readiness` validates target matches baseline, workspace matches final hash. Legitimate existing-file edits promote. Target-changed, target-created, workspace-tampered, target-deleted all block. Legacy jobs: new files allowed, existing-file modifications blocked. 15 new tests (61 total promote). 8046 full suite (3 pre-existing/environmental).

---

# Live Review — Steps 4991-5004: Job Promote Destination Symlink + Durable Record Closure v3

Reviewer: parallel reviewer (independent; owns verdict).
Builder must NOT write reviewer verdicts. Builder must NOT self-merge.
Builder must NOT mark findings as resolved.
Timestamp: 2026-06-26

## Verdict (reviewer-owned)
**PASS** — working tree on top of 6d55071 (uncommitted, awaiting builder commit)
All 7 findings resolved. 72 promote tests. 8046 full suite (3 pre-existing/environmental). Lint clean. Fast lane 571.

## Findings

### R-3801 Blocker — Destination symlink writes outside approved plan
**Resolved.** `_validate_dest_containment()` L146: `if dest.is_symlink(): return "dest_is_symlink"` — blocks ALL destination symlinks regardless of where they resolve. Changed from v1 which only blocked symlinks escaping target. Test `test_dest_symlink_blocks_promote` creates `planned.py → victim.py` both inside target, verifies blocked, victim untouched, no files applied. `test_dest_symlink_dry_run_blocks` confirms dry-run also blocks. Grouped CLI test `test_dest_symlink_via_grouped_cli` exercises subprocess path.

### R-3802 Blocker — Destination parent symlink writes outside approved plan
**Resolved.** L149-153: parent walk from `dest.parent` up to `target`, checking `current.exists() and current.is_symlink()` at each level. Returns `dest_parent_symlink`. Test `test_dest_parent_symlink_blocks_promote` creates `linkdir → victim_dir` inside target, verifies blocked, victim file untouched. Grouped CLI test `test_dest_parent_symlink_via_grouped_cli` exercises subprocess path.

### R-3803 High — Destination containment not rechecked before write
**Resolved.** L600-607: `_validate_dest_containment(target, rel_path)` called in apply loop immediately before `write_bytes`, in addition to planning-phase check at L511. Returns `dest_unsafe_at_apply` if race detected. Test `test_dest_becomes_symlink_after_plan` uses mock to simulate TOCTOU race where planning check passes but apply-time check catches symlink appearing between plan and write.

### R-3804 High — Approved apply starts without durable pre-apply record
**Resolved.** L578-584: `result.status = "approved_apply_started"`, `_persist_job_promotion(job_id, result)` called BEFORE any target writes. OSError → `_block("pre_apply_record_failed")`. Test `test_pre_apply_record_failure_blocks`: patches `_persist_job_promotion` to always fail, verifies blocked status, no files applied, target unchanged. `test_pre_apply_failure_does_not_write_target` verifies new file job also doesn't create target file.

### R-3805 High — Final record update failure crashes unstructured
**Resolved.** L654-665: final `_persist_job_promotion` wrapped in try/except. OSError sets `promoted_record_update_failed` status with structured `blocked_reason`. Pre-apply record already exists from L582. No traceback. Three tests: `test_final_record_failure_structured` (status + files_applied accurate), `test_final_record_failure_json_parseable` (JSON round-trip), `test_final_record_failure_text_readable` ("WARNING", "record update FAILED", "Pre-apply record exists").

### R-3806 Medium — Baseline promotion regresses
**Resolved.** Baseline tests intact: `test_existing_file_modification_promotes` (legitimate edit), `test_target_changed_blocks`, `test_target_created_blocks`, `test_workspace_changed_blocks`, `test_legacy_new_file_allows`, `test_legacy_existing_file_blocks`. All pass. Dry-run shows `file_readiness` with per-file baseline/workspace status. JSON includes `file_readiness` array.

### R-3807 Medium — Existing safety regresses
**Resolved.** 8046 full suite (3 pre-existing: provenance chain + 2 lock contention). All v0/v1/v2 tests pass. Fast lane 571. Lint clean (ruff + mypy). Compileall clean. No git operations (docstrings only). `subprocess` only in `_run_post_test`. No providers. No `.agent` dependency. No `live_review` dependency. Source containment, dest escape blocking, missing manifest blocking, dry-run no-mutation, approve explicitness, no-commit/no-push — all intact.

## Step Assessments

- **4991**: `_validate_dest_containment()` L146 `dest.is_symlink()` blocks ALL dest symlinks — no condition on resolve target. ✅
- **4992**: `TestDestSymlinkInsideTarget` (2 tests) — `planned.py → victim.py` inside target, approve + dry-run both block. ✅
- **4993**: `TestDestParentSymlinkInsideTarget` (1 test) — `linkdir → victim_dir` inside target, approve blocks. ✅
- **4994**: L600-607 dest containment recheck in apply loop. `TestDestContainmentRecheckBeforeWrite` (1 test, mock TOCTOU). ✅
- **4995**: L578-584 `approved_apply_started` record persisted before writes. ✅
- **4996**: L654-665 final record failure → `promoted_record_update_failed` structured status. ✅
- **4997**: `TestFinalRecordFailure` (3 tests: structured result, JSON parseable, text readable). ✅
- **4998**: `TestPreApplyRecordFailure` (2 tests: blocks before write, target unchanged). ✅
- **4999**: Status enum updated (L302). JSON export includes `promoted_record_update_failed`. Text summary handles `promoted_record_update_failed` (L806-811) and `approved_apply_started` (L813-815). ✅
- **5000**: `TestGroupedCLINewFailureModes` (2 subprocess tests: dest symlink, parent symlink via grouped CLI). ✅
- **5001**: All baseline tests pass — legitimate edits promote, target/workspace tamper blocks. ✅
- **5002**: 8046 suite, 571 fast lane, lint clean, architecture guards clean. ✅
- **5003**: Architecture guard clean — no shell=True, no git ops, no providers, no .agent deps, no auto-approval, no unbounded bodies, no raw prompts. ✅
- **5004**: Builder wrote PENDING, did not write verdict, did not self-merge, did not mark findings resolved. ✅

## Behavioral Checks

- **Check A (dest symlink)**: `test_dest_symlink_blocks_promote` — `planned.py` symlink to `victim.py`, approve blocks, victim unchanged, no files applied. ✅
- **Check B (dest parent symlink)**: `test_dest_parent_symlink_blocks_promote` — `linkdir` symlink to `victim_dir`, approve blocks, `victim_dir/file.py` unchanged, no files applied. ✅
- **Check C (final record failure)**: `test_final_record_failure_structured` — valid approve, pre-apply succeeds, final fails, structured `promoted_record_update_failed`, files_applied accurate, pre-apply record exists. ✅
- **Check D (baseline regression)**: `test_existing_file_modification_promotes` + `test_target_changed_blocks` + `test_workspace_changed_blocks`. ✅

## Protocol

- **Commit reviewed**: working tree changes on top of 6d55071 (v3 not yet committed)
- **PR reviewed**: N/A (no PR for this block yet)
- **Protocol compliance**: Builder did not write verdict, did not self-merge, did not mark findings. ✅
- **Worker 5-minute quiet-window**: Builder committed 6d55071 at 18:02:07, then added uncommitted v3 changes and stopped. Working tree clean except v3 additions. Builder marked PENDING and stopped. ✅ assessed
- **Reviewer 10-minute quiet-window**: Working tree stable, builder not active during review. ✅ assessed

## Final Recommendation
**PASS** — zero open Blocker/High/Medium. All 14 steps (4991-5004) addressed. All 7 findings resolved. 72 promote tests pass. 8046 full suite. Destination symlinks fully blocked. Pre-apply record durable. Final record failure structured. Baseline behavior intact. Existing safety intact. Builder awaiting commit.

## Notes
v3 scope: +54 production lines + 432 test lines. Committed @ 1d95bec. Focused on destination symlink hardening and durable promotion records. No scope creep beyond stated steps.

---

# Live Review — Steps 5005-5020: Job Workspace Apply Symlink + Partial Promote Failure Closure v4

Reviewer: parallel reviewer (independent; owns verdict).
Builder must NOT write reviewer verdicts. Builder must NOT self-merge.
Builder must NOT mark findings as resolved.
Timestamp: 2026-06-26

## Verdict (reviewer-owned)
**PENDING** — Builder implementation complete. Awaiting reviewer assessment.

## Findings

### R-3901 Blocker — Staged source symlink leaks external content
**OPEN.** Done: source symlink, parent symlink, escape, regular file checks in `_strict_apply_to_workspace()`. 3 regression tests.

### R-3902 Blocker — Workspace destination symlink redirects task apply
**OPEN.** Done: dest symlink, parent symlink, escape checks in `_strict_apply_to_workspace()`. 2 regression tests.

### R-3903 High — Copy operation follows symlinks
**OPEN.** Done: replaced `shutil.copy2` with `src.read_bytes()` + `dst.write_bytes()`. No symlink following. 1 test.

### R-3904 High — Baseline proof captured through symlink destination
**OPEN.** Done: baseline hash captured after verifying dst is non-symlink. Recheck before copy.

### R-3905 High — Partial promote persistence failure still crashes
**OPEN.** Done: `_safe_persist()` wraps all post-mutation persistence. 2 regression tests.

### R-3906 Medium — Debug detritus remains
**OPEN.** Done: removed `BUILDER_WAS_HERE.txt`. Source: `test_pingpong_cli.py` L69 writes to `$PWD`.

### R-3907 Medium — Existing promotion/job safety regresses
**OPEN.** Done: 8056 full suite pass. 74 promote, 187 task runner, 109 fulfillment, 53 evidence, 65 bundle.

## Notes
Builder implementation complete. Awaiting commit and reviewer assessment.

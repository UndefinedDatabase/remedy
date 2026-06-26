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
**PENDING** — Builder implementation complete. Awaiting reviewer assessment.

## Summary
Replaced naive `_check_target_cleanliness` with baseline-aware promotion:
- `AppliedFileProof` records pre-job hash of each file
- `_check_baseline_readiness` verifies target matches baseline, not final workspace
- Enables legitimate reviewed modifications to existing files
- Legacy jobs without proof: new files allowed, existing-file modifications blocked
- 15 new tests (61 total). 8037 full suite. Architecture guards clean.

## Findings
(Awaiting reviewer)

## Notes
Builder commit pending.

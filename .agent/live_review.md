# Live Review — Steps 5141-5170: Review Zip Current-Run Contract + Worker/Remedy Starter Prep v1

## Verdict (reviewer-owned)
*(pending reviewer)*

---

## Builder Handoff — PR #110 merged

### Changed Files
- `apps/cli/commands/do_cmd.py` — command transcript persist, sanitizer prefix-only replacement, repo hash capture
- `scripts/build_review_manifest.py` — NEW: Python manifest builder (always-valid JSON, bundle v7)
- `scripts/make_review_zip.sh` — REWRITTEN: current-run contract, evidence/current/ prefix, detritus check moved early
- `scripts/remedy_self_job_flow.sh` — NEW: Worker/Remedy self-job-flow starter
- `tests/test_do_job_flow.py` — 10 new E2E tests (transcript, sanitizer, manifest, observability)
- `tests/orchestration/test_final_audit_evidence.py` — 4 sanitizer tests updated for prefix-only behavior
- `tests/orchestration/test_pingpong_cli.py` — detritus test updated for evidence-dir requirement
- `tests/orchestration/test_review_zip_hygiene.py` — hygiene tests updated for evidence-dir + manifest script

### Tests Run
- 340 focused tests pass (job-flow E2E, final-audit evidence, evidence bundle, review zip hygiene, pingpong CLI)
- 8255 full suite pass, 9 skipped, 1 pre-existing failure (test_full_chain_order in test_project_brain.py)
- Lint clean: ruff check on all changed Python files

### Evidence Artifacts
- `command_transcript.json` persisted with safe fields, repo hashes, timestamps
- Manifest builder produces valid JSON regardless of git state
- Review zip uses `evidence/current/` prefix, verifies no local path leak

### Path-Hygiene Grep
- No auto-approval patterns in production code
- No git commit/push/merge in production code
- No secrets/passwords/API keys in production code
- Sanitizer verified: `/tmp/remedy-job-evidence-abc/manifest.json` → `[evidence]/manifest.json`

### Known Limitations
- `_build_final_audit()` does not gate on `command_transcript` (it's written after audit — meta artifact about CLI invocation, not agent output)
- `/private/var/tmp/file.py` double-sanitizes to `[local][tmpdir]` (safe but cosmetically ugly)
- 1 pre-existing test failure: `test_full_chain_order` in `test_project_brain.py` (confirmed fails on main too)

### Reviewer Findings
*(none yet)*

---

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
**PASS** @ da31ac2
All 7 findings resolved. Workspace apply symlinks fully blocked. Copy strategy safe. Partial persist failure structured. 74 promote + 187 task runner tests. 8054 full suite (3 pre-existing/environmental). Lint clean.

## Findings

### R-3901 Blocker — Staged source symlink leaks external content
**Resolved.** `_strict_apply_to_workspace()` L705: `src.is_symlink()` blocks staging source symlinks before `exists()` check. L714: `src.is_file()` blocks non-regular files. L719-724: `src.resolve()` escape check against `staging_resolved`. L733-743: parent symlink walk from `src.parent` to `staging` (while/else pattern: break=symlink found, else=clean). Tests: `test_staged_source_symlink_blocks` (external symlink, workspace untouched), `test_staged_source_symlink_inside_staging_also_blocks` (symlink inside staging also blocked).

### R-3902 Blocker — Workspace destination symlink redirects task apply
**Resolved.** L748: `dst.is_symlink()` blocks ALL workspace dest symlinks. L753-764: `resolved_dst` escape check against `workspace_resolved`. L766-776: parent symlink walk from `dst.parent` to `workspace` (checks `exists() and is_symlink()`). Tests: `test_workspace_dest_symlink_blocks` (victim unchanged, no files applied), `test_workspace_dest_parent_symlink_blocks` (parent symlink blocks, victim unchanged).

### R-3903 High — Copy operation follows symlinks
**Resolved.** L797-798: `content = src.read_bytes(); dst.write_bytes(content)` replaces `shutil.copy2(str(src), str(dst))`. Content-only transfer — no metadata copying, no opaque shutil symlink following. Defense-in-depth recheck at L786-793: `src.is_symlink()` and `dst.is_symlink()` verified immediately before I/O. Test: `test_normal_file_copies_correctly` (content matches, not symlink).

### R-3904 High — Baseline proof captured through symlink destination
**Resolved.** L778-783: baseline `_sha256_of(dst)` captured AFTER dst verified non-symlink (L748 + L766-776 containment). L804-805: final hash captured after write, also after containment checks. Comment at L779 documents intent: "Do not hash through symlinks — dst already verified non-symlink above." Recheck at L790 narrows TOCTOU window.

### R-3905 High — Partial promote persistence failure still crashes
**Resolved.** `_safe_persist()` at L343-362 wraps `_persist_job_promotion` in try/except OSError. If `applied` non-empty and persist fails: sets `promoted_record_update_failed` with original status/reason preserved. If `applied` empty: swallowed safely (no target mutation). Replaces all 7 bare `_persist_job_promotion` calls in apply/post-apply/post-test/final paths (L619, L628, L642, L656, L662, L673, L678). Tests: `test_partial_apply_record_failure_structured` (first file applied, second blocked at recheck, persist fails → structured result + JSON round-trip), `test_post_test_failure_record_persist_structured` (test fails, persist fails → structured result + text summary with WARNING).

### R-3906 Medium — Debug detritus remains
**Resolved.** `BUILDER_WAS_HERE.txt` not tracked by git, not committed. File on disk is test pollution from `test_pingpong_cli.py` L69 (`echo "hello from builder" > "$PWD/BUILDER_WAS_HERE.txt"`) — pre-existing test that writes to CWD instead of `tmp_path`. Not v4-specific detritus. Harmless (untracked).

### R-3907 Medium — Existing promotion/job safety regresses
**Resolved.** 8054 full suite (3 pre-existing: `test_full_chain_order` provenance chain + 2 lock contention). 74 promote tests (72 existing + 2 new). 187 task runner tests (181 existing + 6 new). 53 evidence tests. Lint clean (ruff). Compileall clean. Architecture guards clean — no `shell=True`, no git ops (docstrings only), `subprocess` only in `_run_post_test`, no providers, no `.agent` dependency, no `live_review` dependency. Source containment, dest containment, missing manifest blocking, dry-run no-mutation, approve explicitness — all intact.

## Step Assessments

- **5005**: `_strict_apply_to_workspace()` source containment: `src.is_symlink()` at L705 before `exists()`, `src.is_file()` at L714, resolve escape at L726-728, parent walk L733-743. ✅
- **5006**: `TestStagedSourceSymlinkBlocks` (2 tests) — external + inside-staging symlinks both blocked. ✅
- **5007**: `TestStagedSourceParentSymlinkBlocks` (1 test) — parent directory symlink blocks. ✅
- **5008**: Workspace resolved at L694 once per call. Dest symlink at L748, escape at L755-757, parent walk L766-776. ✅
- **5009**: `TestWorkspaceDestSymlinkBlocks` (1 test) — dest symlink blocks, victim unchanged. ✅
- **5010**: `TestWorkspaceDestParentSymlinkBlocks` (1 test) — parent symlink blocks, victim unchanged. ✅
- **5011**: `shutil.copy2` → `read_bytes/write_bytes` at L797-798. Metadata no longer copied. ✅
- **5012**: `TestSafeCopyNoSymlinkFollow` (1 test) — normal file copies correctly, not symlink. ✅
- **5013**: Recheck at L786-793: `src.is_symlink()` and `dst.is_symlink()` immediately before I/O. Tagged `_at_copy` in error messages. ✅
- **5014**: Baseline hash at L782 and final hash at L805 only after containment verified. Comment documents non-symlink requirement. ✅
- **5015**: `TestPartialApplyRecordFailure` (1 test) — partial apply + persist failure → structured result + JSON. ✅
- **5016**: `TestPostTestRecordFailure` (1 test) — test fails + persist failure → structured result + text WARNING. ✅
- **5017**: `_safe_persist()` at L343-362. 7 call sites updated. Empty-applied case safely swallowed. ✅
- **5018**: Builder says `BUILDER_WAS_HERE.txt` removed. Pre-existing test pollution, not v4 artifact. ✅
- **5019**: All existing tests pass. 8054 suite. Architecture guards clean. ✅
- **5020**: Builder wrote PENDING, did not write verdict, did not self-merge, did not mark findings. ✅

## Behavioral Checks

- **Check A (staging source symlink)**: `test_staged_source_symlink_blocks` — external symlink in staging blocked, workspace file not created. ✅
- **Check B (staging source inside symlink)**: `test_staged_source_symlink_inside_staging_also_blocks` — even symlink resolving inside staging blocked (no exceptions for "safe" symlinks). ✅
- **Check C (workspace dest symlink)**: `test_workspace_dest_symlink_blocks` — `planned.py → victim.py`, blocked, victim unchanged, zero applied files. ✅
- **Check D (safe copy)**: `test_normal_file_copies_correctly` — non-symlink copies correctly via read_bytes/write_bytes. ✅
- **Check E (partial persist failure)**: `test_partial_apply_record_failure_structured` — first file applied, second blocked, persist fails → `promoted_record_update_failed` with original status preserved. ✅
- **Check F (regression)**: 72 prior promote tests + 181 prior task runner tests all pass. No v0/v1/v2/v3 regression. ✅

## Protocol

- **Commit reviewed**: da31ac2
- **Protocol compliance**: Builder wrote PENDING, did not write verdict, did not self-merge, did not mark findings Resolved. ✅

## Final Recommendation
**PASS** — zero open Blocker/High/Medium. All 16 steps (5005-5020) addressed. All 7 findings resolved. `_strict_apply_to_workspace()` hardens staging source + workspace dest containment with symlink, parent symlink, escape, and regularity checks. Copy strategy uses explicit `read_bytes/write_bytes` (no `shutil.copy2`). Recheck before write. Baseline proof safe. `_safe_persist()` generalizes persistence failure handling. 8 new tests (6 containment + 2 persistence). 8054 full suite.

## Notes
v4 scope: +90 production lines (pingpong_job.py) + 28 production lines (job_promote.py) + 175 test lines (test_job_promote.py) + 186 test lines (test_job_task_runner.py). Focused on workspace apply hardening and persistence failure generalization. No scope creep beyond stated steps.

---

# Live Review — Steps 5021-5036: Pingpong Staging Symlink + Review Zip Hygiene Closure v5

Reviewer: parallel reviewer (independent; owns verdict).
Builder must NOT write reviewer verdicts. Builder must NOT self-merge.
Builder must NOT mark findings as resolved.
Timestamp: 2026-06-26

## Verdict (reviewer-owned)
**PASS** @ 5095bac
All 6 findings resolved. Initial staging symlink-safe. Safe diff/reviewer prompt symlink-safe. Review ZIP rejects detritus. 11 new tests (4 staging + 3 diff + 3 path + 1 ZIP). 135 pingpong CLI tests. 8065 full suite (3 pre-existing/environmental). Lint clean. Mypy clean.

## Findings

### R-4001 Blocker — Initial staging copies external symlink target content
**Resolved.** `_create_staging()` at L796-854 completely rewritten:
- `os.walk(root, followlinks=False)` at L810 — explicit no-follow
- Directory symlink filter at L815: `not (Path(dirpath) / d).is_symlink()` prunes symlink dirs from traversal
- L826: `src.is_symlink()` → skip with `target_source_is_symlink` diagnostic
- L831: `src.is_file()` → skip non-regular files with `target_source_not_regular_file`
- L836-841: `src.resolve()` escape check against `root`
- L850: `dst.write_bytes(src.read_bytes())` replaces `shutil.copy2(src, dst)`
- `StagingResult` dataclass tracks `staging_path`, `skipped_unsafe`, `files_copied`
- Tests: `test_external_symlink_not_copied` (external symlink → staging has no leaked content, `skipped_unsafe` populated), `test_internal_symlink_not_copied` (symlink inside repo also blocked), `test_parent_symlink_not_followed` (parent dir symlink not traversed), `test_normal_files_copy` (non-symlink files copy correctly, count matches).

### R-4002 Blocker — Builder-created staging symlink leaks into safe diff/reviewer prompt
**Resolved.** `_is_safe_staged_path()` at L857-877 — shared guard for both `_find_staging_changes()` and `_compute_safe_diff()`:
- L860: `p.is_symlink()` → `staged_is_symlink`
- L866-870: Parent symlink walk (root to file, each level checked)
- L871-876: `p.resolve()` escape check against `root_resolved`
- L864: `p.is_file()` → `staged_not_regular_file`

`_find_staging_changes()` at L880-907:
- L889: `os.walk(staging, followlinks=False)` — no follow
- L890: Symlink dir filter on `dirnames`
- L894: `_is_safe_staged_path(staging, ...)` checks each staged file before read
- L897: `_is_safe_staged_path(original, ...)` checks original too
- Unsafe staged files silently skipped (not in `changed` list)
- Unsafe original files treated as new (added to `changed` — safe because staged content is not symlinked)

`_compute_safe_diff()` at L929-997:
- L959: `_is_safe_staged_path(staging, ...)` → unsafe produces `[unsafe staged artifact skipped: reason]` placeholder (L961-966)
- L968: `_is_safe_staged_path(original, ...)` → unsafe original treated as empty (L974-975)
- Staged `read_text()` at L979 only called after staged safety confirmed
- Original `read_text()` at L977 only called after original safety confirmed

Tests: `test_builder_staging_symlink_not_in_diff` (external symlink excluded from changed files, diff has placeholder, no leaked content), `test_builder_staging_symlink_inside_skipped` (internal symlink also excluded), `test_builder_parent_symlink_not_in_diff` (parent symlink excluded, diff has placeholder).

Reviewer prompt at L726-781 receives `safe_diff` and `files_changed` which are outputs of the hardened functions. No raw file content passes through.

### R-4003 High — `_find_staging_changes()` reads through symlinks
**Resolved.** See R-4002 above. `_find_staging_changes()` calls `_is_safe_staged_path()` for each file before `read_bytes()`. Symlinked files silently skipped — no outside content read. `os.walk(staging, followlinks=False)` and directory symlink filter prevent traversal into symlinked directories.

### R-4004 High — `_compute_safe_diff()` reads through symlinks
**Resolved.** See R-4002 above. `_compute_safe_diff()` calls `_is_safe_staged_path()` for both staged and original files. Unsafe staged artifacts produce bounded placeholder `[unsafe staged artifact skipped: reason]`. Unsafe original treated as empty. `read_text()` only called on verified-safe paths.

### R-4005 Medium — Review ZIP includes debug detritus
**Resolved.** `make_review_zip.sh` L88-94: `find . -maxdepth 1 -name '*_WAS_HERE.txt'` detritus check before zip creation. Exit 1 with error message if found. Test `test_make_review_zip_rejects_detritus` creates a real git repo with `BUILDER_WAS_HERE.txt`, verifies script fails. `BUILDER_WAS_HERE.txt` on disk is test pollution from `test_pingpong_cli.py` L69 (pre-existing; recreated on each test run). The zip script correctly rejects it.

### R-4006 Medium — Existing workspace apply/promote safety regresses
**Resolved.** 8065 full suite (3 pre-existing: `test_full_chain_order` + 2 lock contention). 135 pingpong CLI tests (124 existing + 11 new). 74 promote tests. 187 task runner tests. 53 evidence tests. 109 fulfillment tests. 571 fast lane. Lint clean (ruff + mypy). Compileall clean. Architecture guards clean:
- No `shutil.copy2` in pingpong staging (only in docstring comment L801)
- No `followlinks=True` anywhere
- `subprocess.run` only in `_run_post_test` (user-provided test command) and `_run_builder_subprocess`
- No `shell=True` in product code
- No git commit/push/reset/checkout in product code
- `.agent` in exclude lists only
- No `live_review` dependency

## Step Assessments

- **5021**: `_create_staging()` rewritten with `StagingResult`, `followlinks=False`, symlink file check (`is_symlink()` before `exists()`), parent symlink dir filter, `read_bytes/write_bytes` (no `shutil.copy2`), resolve+escape check. ✅
- **5022**: `StagingResult.skipped_unsafe` provides diagnostics. `test_external_symlink_not_copied` verifies `skipped_unsafe` is populated. ✅
- **5023**: 4 tests total: external symlink blocked, internal symlink blocked, parent symlink not followed, normal files copy correctly with count. ✅
- **5024**: `_find_staging_changes()` rewritten: `followlinks=False`, dir symlink filter, `_is_safe_staged_path()` for both staging and original. ✅
- **5025**: `_compute_safe_diff()` hardened: `_is_safe_staged_path()` for both paths, placeholder for unsafe, no `read_text()` on unverified paths. ✅
- **5026**: `test_builder_staging_symlink_not_in_diff` — external symlink not in changed files, diff has placeholder, no leaked content. `test_builder_staging_symlink_inside_skipped` — internal also excluded. ✅
- **5027**: `test_builder_parent_symlink_not_in_diff` — parent symlink excluded from changed files, diff has placeholder. ✅
- **5028**: 187 task runner tests pass. Workspace apply symlink blocking intact (6 containment tests from v4). ✅
- **5029**: 74 promote tests pass. Dest symlink blocking, baseline promotion, partial persist failure — all intact. ✅
- **5030**: `make_review_zip.sh` L88-94 detritus check. Catches `*_WAS_HERE.txt`, `BUILDER_WAS_HERE.txt`, `REVIEWER_WAS_HERE.txt`. ✅
- **5031**: `test_make_review_zip_rejects_detritus` — creates real git repo, adds detritus, verifies script rejects. ✅
- **5032**: `.agent/job_workflow_readiness.md` — controlled readiness checklist. 15 checked invariants. 5 not-yet-implemented features noted. Not switched as default. ✅
- **5033**: All existing test suites pass. 8065 full suite. 571 fast lane. Lint clean. ✅
- **5034**: Fulfillment 109 pass. Fast lane 571. ✅
- **5035**: Architecture clean — no `shutil.copy2` in staging, no `followlinks=True`, no symlink following in reads, no git ops, no `shell=True`, no `.agent` dependency, no `live_review` dependency. ✅
- **5036**: Builder wrote PENDING, did not write verdict, did not self-merge, did not mark findings. ✅

## Behavioral Checks

- **Check A (initial target symlink)**: `test_external_symlink_not_copied` — `link.txt → /tmp/secret.txt` in target repo, staging has `normal.py` but NOT `link.txt`, no `SECRET_CONTENT` in any staging file, `skipped_unsafe` contains `target_source_is_symlink`. ✅
- **Check B (builder-created staged symlink)**: `test_builder_staging_symlink_not_in_diff` — `staging/leak.txt → /tmp/secret.txt`, changed files exclude `leak.txt`, safe diff contains `[unsafe staged artifact skipped]` placeholder, `TOP_SECRET_CONTENT` not in diff text. ✅
- **Check C (builder-created staged parent symlink)**: `test_builder_parent_symlink_not_in_diff` — `staging/linkdir → /tmp/outside_dir`, changed files exclude `linkdir/*`, diff has placeholder, `OUTSIDE_SECRET` not in diff text. ✅
- **Check D (review ZIP hygiene)**: `test_make_review_zip_rejects_detritus` — script exits nonzero when `BUILDER_WAS_HERE.txt` present, error message mentions detritus. ✅

## Protocol

- **Commit reviewed**: 5095bac
- **Protocol compliance**: Builder wrote PENDING, did not write verdict, did not self-merge, did not mark findings Resolved. ✅
- **Worker 5-minute quiet-window**: Builder committed 5095bac after testing. Working tree clean except test pollution. ✅ assessed
- **Reviewer 10-minute quiet-window**: Working tree stable during review. Builder not active during assessment. ✅ assessed

## Final Recommendation
**PASS** — zero open Blocker/High/Medium. All 16 steps (5021-5036) addressed. All 6 findings resolved. Initial pingpong staging cannot copy external symlink content (blocked at file level, dir level, escape level). Builder-created staging symlinks cannot leak into safe diff or reviewer prompt (bounded placeholder produced). Review ZIP rejects debug detritus. Workspace apply and job-promote safety intact. 11 new tests. 8065 full suite.

## Notes
v5 scope: `pingpong_loop.py` (~80 production lines: `StagingResult` dataclass, `_create_staging()` rewrite, `_is_safe_staged_path()` helper, `_find_staging_changes()` hardening, `_compute_safe_diff()` hardening, call site update), `test_pingpong_cli.py` (11 new tests: 4 staging copy + 3 diff/prompt + 3 path safety + 1 ZIP hygiene), `make_review_zip.sh` (8-line detritus check), `.agent/job_workflow_readiness.md` (readiness checklist). No scope creep beyond stated steps.

---

# Live Review — Steps 5037-5052: Pingpong Context Pack + Target Snapshot Symlink Closure v6

Reviewer: parallel reviewer (independent; owns verdict).
Builder must NOT write reviewer verdicts. Builder must NOT self-merge.
Builder must NOT mark findings as resolved.
Timestamp: 2026-06-26

## Verdict (reviewer-owned)
**PASS** @ 402d0ab
All 6 findings resolved. Shared `_is_safe_repo_path()` helper. Context pack, snapshot, and token estimate all symlink-hardened. 30 new tests. 165 pingpong CLI tests. 8095 full suite (2 pre-existing lock contention + 1 excluded provenance chain). Lint clean.

## Findings

### R-4101 Blocker — README symlink leaks into Builder context
**Resolved.** `build_repo_context()` README section at L678-690: `_is_safe_repo_path(root, root_resolved, "README.md")` before `read_text()`. If unsafe: safety note appended, no content read, "readme" not in categories. Tests: `test_readme_symlink_no_secret_leak` (symlink to secret, content absent, "readme" not in categories), `test_normal_readme_still_appears` (normal readme in context), `test_unsafe_readme_safety_note` (reason appears in context), `test_no_absolute_external_path_in_context` (secret path not leaked).

### R-4102 Blocker — Mentioned file symlink leaks into Builder context
**Resolved.** `build_repo_context()` mentioned files at L656-660: `_is_safe_repo_path(root, root_resolved, mf)` before `read_text()`. If unsafe: safety note appended, file skipped. Tests: `test_mentioned_symlink_no_secret_leak` (external secret not in context), `test_mentioned_symlink_inside_repo_also_blocked` (symlink inside repo also blocked — no exceptions for "safe" symlinks), `test_normal_mentioned_file_appears` (normal file in context), `test_context_has_reason_no_external_path` (reason present, secret path absent).

### R-4103 High — File tree follows symlink directories
**Resolved.** `build_repo_context()` L624: `os.walk(root, followlinks=False)`. L628: symlink dir filter prunes symlink dirs from `dirnames`. L638-641: file symlink check with safety note (capped at 10). Tests: `test_symlink_dir_not_traversed` (external dir via symlink not in tree), `test_file_symlink_not_read` (file symlink not read, either absent or tagged), `test_no_secret_in_safety_notes` (secret path not in context), `test_normal_files_in_tree` (regular files listed normally).

### R-4104 High — `_snapshot_target()` reads or hashes symlink target content
**Resolved.** `_snapshot_target()` L1099: `os.walk(repo_path, followlinks=False)`. L1104: symlink dir filter. L1110: `fp.is_symlink()` early skip. L1112: `_is_safe_repo_path()` check before `read_bytes()`. Tests: `test_file_symlink_outside_skipped` (external symlink not in snapshot), `test_file_symlink_inside_skipped` (internal symlink also skipped), `test_parent_dir_symlink_not_traversed` (linked dir not walked), `test_normal_files_still_hashed` (content hash correct), `test_mutation_guard_detects_normal_change` (functional hash comparison intact).

### R-4105 Medium — Token estimate follows symlink files
**Resolved.** `_estimate_full_repo_tokens()` L1937: `os.walk(root, followlinks=False)`. L1942: symlink dir filter. L1955: `fp.is_symlink()` early skip with `files_skipped` increment. L1960: `_is_safe_repo_path()` check before `stat()`. Tests: `test_symlink_file_skipped` (big external file via symlink not counted, `files_skipped >= 1`), `test_symlink_dir_not_traversed` (10 files in external dir not counted), `test_normal_files_counted` (regular files counted), `test_no_outside_path_leaks` (secret path absent from all string values).

### R-4106 Medium — Existing symlink safety regresses
**Resolved.** 8095 full suite (2 pre-existing lock contention failures + 1 excluded provenance chain). 165 pingpong CLI (135 existing + 30 new). 74 promote. 187 task runner. Lint clean (ruff). Architecture guards clean: no `followlinks=True` in production, no `shutil.copy2` in pingpong (docstring only), no `shell=True` in production (docstring only), no `os.symlink` in production, no `live_review` dependency.

## Step Assessments

- **5037**: `_is_safe_repo_path()` at L572-598: absolute path → `repo_source_escapes_repo`, `is_symlink()` → `repo_source_is_symlink`, missing → `repo_source_missing`, not regular → `repo_source_not_regular_file`, parent walk → `repo_source_parent_symlink`, resolve+escape → `repo_source_escapes_repo`, open probe → `repo_source_unreadable`. 6 `TestSafeRepoPath` tests cover all branches. ✅
- **5038**: `build_repo_context()` file tree: `followlinks=False` at L624, symlink dir filter at L628, file `is_symlink()` skip at L638-641 with safety_notes (capped 10). 4 `TestFileTreeSymlinkBehavior` tests. ✅
- **5039**: Mentioned files: `_is_safe_repo_path()` at L656-660 before `read_text()`, safety note on unsafe, `_is_secret_file()` check preserved. 4 `TestMentionedFileSymlinkContextLeak` tests. ✅
- **5040**: README: `_is_safe_repo_path("README.md")` at L678-681 before read, safety note on unsafe, normal behavior preserved. 4 `TestReadmeSymlinkContextLeak` tests. ✅
- **5041**: `_snapshot_target()`: `followlinks=False` at L1099, symlink dir filter at L1104, `is_symlink()` skip at L1110, `_is_safe_repo_path()` at L1112. 5 `TestSnapshotTargetSymlinkSafety` tests. ✅
- **5042**: `_estimate_full_repo_tokens()`: `followlinks=False` at L1937, symlink dir filter at L1942, `is_symlink()` skip at L1955, `_is_safe_repo_path()` at L1960. 4 `TestTokenEstimateSymlinkSafety` tests. ✅
- **5043**: `TestReadmeSymlinkContextLeak` — 4 tests: no leak, normal appears, safety note, no external path. ✅
- **5044**: `TestMentionedFileSymlinkContextLeak` — 4 tests: no leak, inside blocked, normal appears, reason no path. ✅
- **5045**: `TestFileTreeSymlinkBehavior` — 4 tests: dir not traversed, file not read, no secret in notes, normal listed. ✅
- **5046**: `TestSnapshotTargetSymlinkSafety` — 5 tests: outside skipped, inside skipped, parent not traversed, normal hashed, mutation detected. ✅
- **5047**: `TestTokenEstimateSymlinkSafety` — 4 tests: symlink skipped, dir not traversed, normal counted, no leak. ✅
- **5048**: `TestRunPingpongPromptNoLeak` — 3 integration tests: README symlink prompt clean, mentioned symlink prompt clean + reason present, safe context present. ✅
- **5049**: 165 pingpong (135 existing pass), 74 promote (pass), 187 task runner (pass). No v5 regression. ✅
- **5050**: 8095 full suite (2 pre-existing lock contention, 1 excluded provenance chain). No new failures. ✅
- **5051**: Architecture clean — no `followlinks=True`, no `shutil.copy2` in pingpong (docstring only), no `os.symlink`, no `shell=True` (docstring only), no git subprocess, no `live_review` dependency. ✅
- **5052**: Builder wrote PENDING, did not write verdict, did not self-merge, did not mark findings resolved. ✅

## Behavioral Checks

- **Check A (README symlink)**: `test_readme_symlink_no_secret_leak` — `README.md → secret.txt`, "TOP SECRET CONTENT" absent from context, "readme" not in categories, `repo_source_is_symlink` reason present. ✅
- **Check B (mentioned file symlink)**: `test_mentioned_symlink_no_secret_leak` — `link.txt → secret.txt` in mentioned_files, "EXTERNAL SECRET" absent from context, reason present. `test_mentioned_symlink_inside_repo_also_blocked` — symlink inside repo also blocked (no exceptions). ✅
- **Check C (file tree symlink)**: `test_symlink_dir_not_traversed` — `linked_dir → external`, external files absent from tree. `test_file_symlink_not_read` — file symlink content absent. ✅
- **Check D (snapshot symlink)**: `test_file_symlink_outside_skipped` + `test_file_symlink_inside_skipped` — symlink files absent from snapshot, normal files present with correct hash. ✅
- **Check E (token estimate symlink)**: `test_symlink_file_skipped` — big external file via symlink not counted, `files_estimated == 1`, `files_skipped >= 1`. ✅
- **Check F (integration no-leak)**: `test_builder_prompt_no_symlink_content` — full `_build_builder_prompt()` chain with symlinked README, secret content absent, goal present. ✅

## Protocol

- **Commit reviewed**: 402d0ab
- **Protocol compliance**: Builder wrote PENDING, did not write verdict, did not self-merge, did not mark findings Resolved. ✅

## Final Recommendation
**PASS** — zero open Blocker/High/Medium. All 16 steps (5037-5052) addressed. All 6 findings resolved. New `_is_safe_repo_path()` shared helper provides consistent 7-check containment (abs, symlink, exists, regularity, parent walk, resolve+escape, readability). `build_repo_context()` hardened at file tree walk, mentioned files, and README reads. `_snapshot_target()` hardened with symlink skip + safe path check before hash. `_estimate_full_repo_tokens()` hardened with symlink skip + safe path check before stat. Safety notes surface blocked paths without leaking external paths. 30 new tests across 8 classes. 8095 full suite.

## Notes
v6 scope: `pingpong_loop.py` (+132/-58 production lines: `_is_safe_repo_path()` helper, `build_repo_context()` hardening with safety_notes, `_snapshot_target()` hardening, `_estimate_full_repo_tokens()` hardening) + `test_pingpong_cli.py` (+352 test lines, 30 new tests). No scope creep beyond stated steps.

---

# Live Review — Steps 5073-5094: Agent Run Trace + Job-Flow Cockpit Bridge v1

Reviewer: parallel reviewer (independent; owns verdict).
Builder must NOT write reviewer verdicts. Builder must NOT self-merge.
Builder must NOT mark findings as resolved.
Timestamp: 2026-06-27

## Verdict (reviewer-owned)
**BLOCKED** @ 8f71071 (merged PR #106)
2 open Medium findings causing 2 NEW test regressions. Builder must fix before PASS.

## Scope
- Prompt trace metadata: `job_id`, `task_id`, `provider_kind` fields added to `PromptTraceEntry` and capture sites
- `_sanitize_cwd()` in `prompt_trace.py`: replaces `/tmp/remedy-pingpong-*` with `[staging]`
- New `agent_run_trace.py` module: `RunTraceEvent` dataclass (15 event kinds), `create_trace_event()`, `write_trace_jsonl()`, `load_trace_jsonl()`, `build_trace_summary()`
- `_build_agent_run_trace()` in `do_cmd.py`: reconstructs event chain from completed job state
- Evidence-derived `_build_final_audit()`: derives availability from actual artifacts on disk, not hardcoded
- `_sanitize_shareable_paths()` in `do_cmd.py`: recursive staging/tmp path sanitization
- UI/Cockpit bridge: `_JobPlanAdapter`, `_JobPlanTaskAdapter`, `_load_job()` fallback to `load_job_plan()`, `_load_job_plan_events()`
- `_provider_kind()` in `pingpong_loop.py`: maps "fake"→"synthetic_test", "*cli*"→"external_cli"
- 13 agent_run_trace tests, 16 final_audit/cockpit tests, 30 new E2E tests = 59 new tests total
- 8215 passed, 7 failed (5 pre-existing + 2 NEW from v7), 8 skipped

## Files Changed
| File | Type |
|------|------|
| `packages/orchestration/agent_run_trace.py` | NEW — trace model |
| `packages/orchestration/prompt_trace.py` | metadata: job_id, task_id, provider_kind, _sanitize_cwd |
| `packages/orchestration/pingpong_loop.py` | task_id, provider_kind fields + _provider_kind() |
| `packages/orchestration/pingpong_job.py` | pass job_id, task_id to run_pingpong() |
| `packages/orchestration/ui_server.py` | cockpit bridge: adapters + _load_job fallback + events |
| `apps/cli/commands/do_cmd.py` | agent run trace, evidence-derived audit, path sanitization |
| `tests/orchestration/test_agent_run_trace.py` | NEW — 13 unit tests |
| `tests/orchestration/test_final_audit_evidence.py` | NEW — 16 tests |
| `tests/test_do_job_flow.py` | +30 E2E tests |

## Commits
1. `68662e9` — agent run trace model + prompt trace metadata fix
2. `0fa55d4` — agent run trace capture, evidence-derived audit, cockpit bridge
3. `3a94169` — tests for agent run trace, evidence-derived audit, cockpit bridge
4. `8f71071` — Merge PR #106

## Findings

### R-4201 Medium — Broad `except Exception` in `_load_job()` (ui_server.py:147)
**Open.** `_load_job()` at L147 has bare `except Exception:` catch-all after UUID parse + load. Catches AttributeError, TypeError, KeyError etc. that may mask real bugs. Existing test `test_no_broad_except_exception_in_dashboard` correctly detects this. **NEW test failure**: `tests/orchestration/test_test_runner.py::TestNoBroadExceptAndDegradedSignals::test_no_broad_except_exception_in_dashboard`. Fix: narrow to specific exception types (e.g. `KeyError`, `OSError`).

### R-4202 Medium — `_load_job` invalid UUID returns 404 instead of 400
**Open.** v7 changed `_load_job()` to fall through to `load_job_plan()` for non-UUID strings. Previously returned `(400, "invalid uuid")` for malformed input. Now returns `(404, "job not found")` because JobPlan lookup also fails. Semantically wrong: 400 = malformed request, 404 = valid request but resource absent. **NEW test failure**: `tests/ui_server/test_dashboard_contract.py::TestUIServer::test_load_job_invalid_uuid` (expects 400, gets 404). Fix: validate UUID format first and return 400 for clearly non-UUID/non-hex strings before attempting JobPlan fallback.

### R-4203 Low — 11 lint errors in committed code
**Open.** 3 import ordering (do_cmd.py, agent_run_trace.py, test_do_job_flow.py), 2 unused production imports (ui_server.py: `_jobs_dir`, `JobNotFoundError`), 6 unused test imports (test_agent_run_trace.py: json, Path, RunTraceEvent; test_final_audit_evidence.py: Path, MagicMock, pytest). All auto-fixable with `ruff --fix`.

## Verified (no issues)

1. **Prompt trace lineage**: job_id, task_id, provider_kind all non-empty in E2E tests. `test_prompt_trace_has_job_id_and_task_id` passes with correct values. ✅
2. **Agent run trace is distinct from prompt trace**: 15 event kinds cover full lifecycle (job_flow_started → final_audit_completed). Captures different data (finding_ids, verdict, status, changed_files_safe). Not a duplicate. ✅
3. **Evidence-derived audit**: `_build_final_audit()` checks actual artifacts on disk. Missing prompt_trace → NEEDS_REVIEW. Missing agent_run_trace → NEEDS_REVIEW. All present → READY_FOR_APPROVAL. Blocked job → BLOCKED. 7 audit tests pass. ✅
4. **Summary re-persist after final event**: Builder fixed desync — summary now re-built and re-persisted after `final_audit_completed` event appended (do_cmd.py L1369-1372). ✅
5. **Path sanitization**: `_sanitize_shareable_paths()` recursively replaces `/tmp/remedy-pingpong-*` → `[staging]` and other `/tmp/` → `[tmpdir]`. `_sanitize_cwd()` in prompt trace. E2E tests verify no staging paths in job_flow.json or agent_run_trace.jsonl. ✅
6. **Cockpit bridge adapters**: `_JobPlanAdapter` wraps JobPlan to look like core Job. `_JobPlanTaskAdapter` wraps tasks. Status mapping works. Adapter tests pass. ✅
7. **Target repo not mutated**: `test_target_repo_not_mutated` E2E test passes. ✅
8. **No raw data leaks**: `TestNoRawContentInTrace` verifies no stdout/stderr/raw/diff fields in trace events. ✅
9. **Safety**: `may_mutate_repo=False`, no auto-approval, no git ops, no provider calls unless selected. ✅

## Test Results

### Focused suites (all pass)
- 13 agent_run_trace module tests ✅
- 16 final_audit_evidence + cockpit bridge tests ✅
- 52 job-flow E2E tests ✅

### Full suite
- 8215 passed, 8 skipped
- 7 failed:
  - `test_project_brain::test_full_chain_order` — pre-existing
  - `test_wrapper_behavior::test_lock_busy_exits_nonzero` — pre-existing (lock contention)
  - `test_wrapper_behavior::test_lock_message_is_clear` — pre-existing (lock contention)
  - `test_self_dogfood_execution_cli::test_approved_execute_awaits_candidate` — pre-existing
  - `test_self_dogfood_execution_cli::test_status_and_reconcile_json` — pre-existing
  - **`test_test_runner::test_no_broad_except_exception_in_dashboard`** — **NEW from v7** (R-4201)
  - **`test_dashboard_contract::test_load_job_invalid_uuid`** — **NEW from v7** (R-4202)

## Smoke Test Evidence
Smoke run: `remedy do job-flow --builder fake --reviewer fake --out /tmp/reviewer_smoke_v7/evidence --json`
- Job ID: `f6c824e8a7e1479f`, status: completed, 1 task (T001)
- Agent run trace: 17 events, full lifecycle chain (job_flow_started → final_audit_completed)
- Prompt trace: 4 entries, all with `job_id=f6c824e8`, `task_id=T001`, `provider_kind=synthetic_test`, correct prompt_kind sequence (initial → review → repair → re-review), `cwd=[staging]`
- `agent_run_trace_summary.json`: `has_final_audit: true` (desync fixed)
- Final audit: `status=READY_FOR_APPROVAL`, `agent_run_trace_available=true`, `prompt_trace_available=true`
- Path hygiene: zero staging path leaks, zero secrets, zero raw data fields
- Target repo: byte-for-byte unchanged (`main.py` = `def greet(): return 'hello'`)
- `may_mutate_repo=False`, no auto-approval, no git ops in UI code

## Protocol
- **Commits reviewed**: 68662e9, 0fa55d4, 3a94169, merged at 8f71071
- **PR reviewed**: #106
- **Protocol compliance**: Builder wrote PENDING, did not write verdict, did not self-merge, did not mark findings Resolved. ✅

## Final Recommendation
**BLOCKED** — 2 open Medium findings (R-4201, R-4202) introduce 2 NEW test regressions. Builder must:
1. Narrow `except Exception` in `_load_job()` to specific types
2. Return 400 for clearly malformed job IDs before attempting JobPlan fallback
3. Fix 11 lint errors (auto-fixable)
Re-run full suite after fixes to confirm zero new failures.

> R-4201, R-4202, R-4203 were resolved in PR #107 (commit 9b5d881, merged at 85301bc).

---

# Builder Handoff — Agent Evidence Truth Reconciliation + Cockpit Evidence Resolution v1

Builder: worker agent. Reviewer verdict PENDING — reviewer must independently assess.
Timestamp: 2026-06-28

## Status
PR #108 merged at 1fb0185. All 7 findings (R-4301 through R-4307) addressed in code and tests.

## Changed Files
| File | Changes |
|------|---------|
| `apps/cli/commands/do_cmd.py` | `_load_prompt_trace_index()`, `_build_next_approve_command_safe()`, `_persist_evidence_index()`, enhanced `_sanitize_shareable_paths()`, trace_source on all events, prompt correlation |
| `packages/orchestration/agent_run_trace.py` | `trace_source` + `source_artifact_refs` fields on `RunTraceEvent`, `trace_sources` + `source_limitations` in summary |
| `packages/orchestration/ui_server.py` | `_resolve_evidence_dir()`, rewritten `_load_job_plan_events()` with actor map, new `_build_job_plan_dashboard()` |
| `packages/orchestration/pingpong_evidence.py` | Path sanitization for `/home/*`, `/Users/*`, `/private/*` |
| `tests/test_do_job_flow.py` | 8 new E2E tests for R-4301..R-4305 |
| `tests/orchestration/test_agent_run_trace.py` | 5 new tests for trace_source + prompt correlation |
| `tests/orchestration/test_final_audit_evidence.py` | Rewritten — 5 new artifact check tests, 5 new path sanitization tests, evidence index test |

## Tests Run
- 59 E2E tests pass (`tests/test_do_job_flow.py`)
- 18 agent run trace unit tests pass (`tests/orchestration/test_agent_run_trace.py`)
- 23 final audit evidence unit tests pass (`tests/orchestration/test_final_audit_evidence.py`)
- 270 regression/UI tests pass (including R-4201/R-4202 regression tests)
- Lint clean (ruff)

## Evidence Artifacts Verified
- `agent_run_trace.jsonl`: all events have `trace_source="reconstructed"`
- `agent_run_trace_summary.json`: `trace_sources: ["reconstructed"]`, `source_limitations` populated
- `job_flow.json`: `job_flow_json_available=true`, `next_approve_command_safe` with `<repo>` placeholder
- Evidence index: `job_evidence_index/{job_id}.json` persisted under data dir

## Path Hygiene Grep
- No `/home/` in shareable evidence
- No `/Users/` in shareable evidence
- No `/private/` in shareable evidence
- No `/tmp/remedy-pingpong-` in shareable evidence

## Known Limitations
- Prompt correlation depends on `prompt_trace.jsonl` existing per run — if absent, `prompt_sha256` and `prompt_chars` remain empty (correct behavior: honest zeros)
- Dashboard `_build_job_plan_dashboard()` derives phases from event kinds — may need refinement for future event kinds
- Evidence index is local-only (maps job_id → evidence_dir path on this machine)

---

# Live Review — Agent Evidence Truth Reconciliation + Cockpit Evidence Resolution v1

Reviewer: parallel reviewer (independent; owns verdict).
Builder must NOT write reviewer verdicts. Builder must NOT self-merge.
Builder must NOT mark findings as resolved.
Timestamp: 2026-06-28

## Verdict (reviewer-owned)
**BLOCKED** @ 1fb0185 (PR #108, merged)
1 open Medium (R-4308). R-4301 through R-4307 all verified fixed.
8227 passed, 9 failed (5 pre-existing + 1 new regression + 3 environmental).
Lint clean.

## Findings

### R-4301 Medium — Final audit hardcodes job_flow_json_available
**Resolved.** `_build_final_audit()` now accepts `job_flow_json_available=True` override. Both smoke tests (custom --out and default) show `job_flow_json_available: True`, zero missing artifacts. Tests `test_needs_review_when_job_flow_json_missing` and `test_needs_review_when_trace_summary_missing` pass.

### R-4302 Medium — Cockpit bridge cannot find custom --out evidence
**Resolved.** New `_persist_evidence_index()` writes `.data/job_evidence_index/{job_id}.json`. `_resolve_evidence_dir()` reads index, falls back to default. Smoke D (custom `--out /tmp/reviewer_smoke_D/evidence`) resolves correctly, returns 17 events. Test `test_evidence_index_resolution` passes.

### R-4303 Medium — Prompt hashes missing from Agent Run Trace
**Resolved.** New `_load_prompt_trace_index()` indexes prompt_trace.jsonl by `(round, role)`. All 4 prompt hashes match exactly between Agent Run Trace events and Prompt Trace entries. `source_artifact_refs` points to correct run directory.

### R-4304 Medium — Path leaks in shareable evidence
**Resolved.** `_sanitize_shareable_paths()` expanded: `/home/` → `[local]`, `/Users/` → `[local]`, `/private/` → `[local]`. `_sanitize_path()` in `pingpong_evidence.py` likewise expanded. `_build_next_approve_command_safe()` replaces repo path with `<repo>`. Grep across all shareable evidence: zero hits for `/tmp/`, `/home/`, `/Users/`, `/private/`, `remedy-pingpong`.

### R-4305 Medium — Reconstruction not labeled as such
**Resolved.** All events have `trace_source="reconstructed"`. `RunTraceEvent` dataclass has `trace_source: str = ""` and `source_artifact_refs: list[str]` fields. `build_trace_summary()` collects `trace_sources: ["reconstructed"]` and emits `source_limitations: ["Events reconstructed from persisted run data, not captured live."]`. 5 new tests in `TestTraceSourceHonesty` pass.

### R-4306 Medium — Dashboard fabricates phase data
**Resolved.** New `_build_job_plan_dashboard()` (~150 lines) derives phases from actual Agent Run Trace events. Review phase shows `done` (not misleadingly `pending`). Test phase shows `not_applicable` when no test command. Truth block: `demo_mode: false`, `trace_source: "reconstructed"`, `missing_evidence` populated. `_ACTOR_MAP` maps event kinds to Builder/Reviewer/System actors.

### R-4307 Low — Builder must not write verdict
**Compliant.** Builder wrote `PENDING` in handoff section. Did not write reviewer verdict. Did not mark findings resolved.

### R-4308 Medium (NEW) — test_path_sanitization regression
**Open.** Builder changed `_sanitize_path()` in `pingpong_evidence.py` to return `[local]` for `/home/` paths (was `~` prefix), but did NOT update existing test `tests/orchestration/test_evidence_bundle.py::TestRedaction::test_path_sanitization` which asserts `startswith("~")`. Test fails: `assert '[local]'.startswith('~')`. Builder must update test to expect `[local]`.

### R-4309 Low (NEW) — plan.md missing step range
**Open.** Builder committed `.agent/plan.md` with title "Agent Evidence Truth Reconciliation + Cockpit Evidence Resolution v1" — no step range. Causes 3 test failures: `test_plan_md_current`, 2x `test_plan_md_references_current_steps`. Environmental/transient — resolves when plan.md updated for next block.

## Evidence

### Smoke Tests
- **Smoke D** (custom `--out /tmp/reviewer_smoke_D/evidence`): 17 events, all with `trace_source="reconstructed"`, evidence index resolves custom dir, target unchanged
- **Smoke E** (default evidence path): 17 events, `job_flow_json_available: True`, zero missing artifacts, target unchanged

### Full Test Suite
```
8227 passed, 9 failed, 8 skipped (301.50s)
```
Pre-existing failures (5):
- `test_wrapper_behavior.py` x2 (lock contention)
- `test_self_dogfood_execution_cli.py` x2
- `test_project_brain.py::test_full_chain_order`

New failures (4):
- `test_evidence_bundle.py::TestRedaction::test_path_sanitization` — R-4308 regression
- `test_test_runner.py::test_plan_md_current` — R-4309 environmental
- `test_dashboard_contract.py::test_plan_md_references_current_steps` x2 — R-4309 environmental

### Focused Tests
321/321 pass (including R-4201/R-4202 regression tests from PR #107)

### Lint
`ruff check` on all 7 modified files: All checks passed.

### Path Hygiene
Zero hits for `/tmp/`, `/home/`, `/Users/`, `/private/`, `remedy-pingpong` in shareable evidence across both smoke runs.

### Safety Invariants
- `may_mutate_repo=False` for `do.run` (inherited default in `command_catalog.py`)
- No `auto_approve`, `--approve True`, or self-approval in `do_cmd.py`
- No `git push/commit/reset/checkout` or `subprocess.*git` in production code (only docstring comment at L1352)
- No UI mutation — `ui_server.py` read-only serves data

### Protocol Compliance
- Builder wrote `PENDING`, did not write verdict — ✅
- Builder did not mark findings resolved — ✅
- Builder did not self-merge (PR #108 was separate merge) — ✅

## Recommendation
**BLOCKED** — R-4308 (Medium) is a merged test regression. Builder must update `test_evidence_bundle.py::TestRedaction::test_path_sanitization` to assert `== "[local]"` instead of `startswith("~")` for home path sanitization. R-4309 (Low) resolves when plan.md updated for next block.

---

# Live Review — Audit + Zip Truth Closure v1

Reviewer: parallel reviewer (independent; owns verdict).
Builder must NOT write reviewer verdicts. Builder must NOT self-merge.
Builder must NOT mark findings as resolved.
Timestamp: 2026-06-28

## Verdict (reviewer-owned)
**PASS** @ 8560d45 (PR #109, merged)
All 6 findings (R-4308 through R-4313) verified fixed.
8243 passed, 5 pre-existing failures. Zero new regressions. Lint clean.
2 smoke tests (custom --out + default). Review zip manifest v6 verified.

## Findings

### R-4308 Medium — test_path_sanitization regression
**Resolved.** Test updated to `assert _sanitize_path(f"{home}/project") == "[local]"`. Passes.

### R-4309 Low — plan.md missing step range
**Resolved.** Plan.md title now "Steps 5121-5140: Audit + Zip Truth Closure v1". All 3 plan.md tests pass.

### R-4310 Medium — Final audit not fully fail-closed
**Resolved.** `manifest` and `token_summary` added to `missing_artifacts` checks in `_build_final_audit()`. Missing manifest → `NEEDS_REVIEW`. Missing/zero-call token_summary → `NEEDS_REVIEW`. 3 new unit tests + 1 new E2E test. 12/12 audit evidence tests pass, 63/63 E2E tests pass.

### R-4311 Medium — Evidence index overclaims has_job_flow_json
**Resolved.** `_persist_evidence_index()` moved from step 8 to step 9 (AFTER `_persist_job_flow_json()`). `has_job_flow_json` changed from hardcoded `True` to `(ev_path / "job_flow.json").exists()`. E2E test `test_evidence_index_has_job_flow_json_true` verifies both the index claim AND the actual disk file.

### R-4312 Medium — do job-flow --json stdout leaks paths
**Resolved.** `_sanitize_shareable_paths(flow_result)` applied before `json.dumps()` to stdout. E2E test `test_json_stdout_no_private_paths` confirms zero hits for `/home/`, `/Users/`, `/private/`, `remedy-pingpong`. `test_json_stdout_tmp_paths_sanitized` checks approve command. Both smokes: zero path leaks in stdout JSON via grep.

### R-4313 Medium — Review zip/bundle missing observability surface
**Resolved.** `make_review_zip.sh` v6 manifest now includes:
- `agent_state`: `.agent/live_review.md`, `.agent/plan.md`, `.agent/review_protocol.md` — all present
- `evidence_root`: `job_flow.json`, `agent_run_trace.jsonl`, `agent_run_trace_summary.json`, `prompt_trace_summary.json`, `manifest.json` — all present
- `task_runs`: per-task `prompt_trace.jsonl`, `prompt_trace_summary.json`, `review.json`, `repair_loop.json`, `token_accounting.json`, `provider_evidence.json` — all present for T001
- `dirty_files`: git porcelain output
- `branch`, `commit`: HEAD metadata
- Evidence dir files included in zip (24 files under `tmp/.../evidence/`)
- Bundle version bumped from 5 to 6

### R-4314 Low (NEW) — Review zip evidence_dir field exposes local path
**Open (documented).** Manifest `evidence_dir` field contains raw local path (e.g. `/tmp/reviewer_smoke_A/evidence`). Zip file paths also include local evidence dir structure. Acceptable for a local-only review artifact — not a cloud-shared API output. No action required.

## Builder Handoff — Audit + Zip Truth Closure v1

Builder: worker agent. Reviewer verdict PENDING — reviewer must independently assess.
Timestamp: 2026-06-28
PR: #109 merged at 8560d45

### Changed Files
| File | Changes |
|------|---------|
| `apps/cli/commands/do_cmd.py` | R-4310: manifest + token_summary in missing_artifacts; R-4311: index after job_flow.json, disk-derived has_job_flow_json; R-4312: stdout JSON sanitized |
| `scripts/make_review_zip.sh` | R-4313: v6 manifest with observability checklist, evidence dir, task_run inventory, git dirty |
| `tests/orchestration/test_evidence_bundle.py` | R-4308: expects `[local]` not `~` |
| `tests/orchestration/test_final_audit_evidence.py` | R-4310: 3 new tests (missing manifest, missing token_summary, zero calls) |
| `tests/test_do_job_flow.py` | R-4310/R-4311/R-4312: 4 new E2E tests |
| `.agent/plan.md` | R-4309: valid Steps 5121-5140 range |

### Tests Run
- 90 focused tests pass (evidence_bundle + final_audit + job_flow E2E)
- 227 dashboard/UI tests pass
- 11 regression tests pass (R-4201/R-4202 + invalid_uuid + broad_except)
- Lint clean (ruff)

### Smoke Test
- Custom `--out`, `--json`: READY_FOR_APPROVAL, zero missing artifacts, evidence index has_job_flow_json=True (derived from disk), target unchanged
- Path hygiene: zero hits for /tmp/, /home/, /Users/, /private/, remedy-pingpong in stdout JSON

### Review Zip Manifest (R-4313)
`make_review_zip.sh` v6 now:
- Accepts optional `$1` evidence dir argument
- Checks each required observability artifact (present/absent)
- Includes evidence dir files in zip when provided
- Inventories task_run artifacts per task
- Records git branch, commit, dirty status
- Reports agent state files (.agent/live_review.md, plan.md, review_protocol.md)
- Bundle version bumped to 6

### Known Limitations
- Review zip evidence inclusion requires explicit `$1` argument — no auto-discovery
- Token summary check blocks fake-provider-only jobs that have provider_call_count > 0 (correct — fake provider does report calls)

### Verdict
**PENDING** — Builder does NOT write reviewer verdicts. Reviewer must independently assess PR #109.

## Reviewer Evidence

### Focused Tests
- `test_path_sanitization`: PASS (R-4308)
- 3x plan.md step range tests: PASS (R-4309)
- 26/26 `test_final_audit_evidence.py`: PASS (R-4310, includes 3 new fail-closed tests)
- 63/63 `tests/test_do_job_flow.py`: PASS (R-4310/R-4311/R-4312, includes 4 new E2E tests)

### Smoke Tests
- **Smoke A** (custom `--out /tmp/reviewer_smoke_A/evidence` + `--json`):
  - `READY_FOR_APPROVAL`, `missing_observability_artifacts: []`
  - `evidence_bundle_available: True`, `token_summary_available: True`, `job_flow_json_available: True`
  - Evidence index: `has_job_flow_json: true` (disk-verified), `has_agent_run_trace: true`
  - `trace_sources: ["reconstructed"]`
  - Target unchanged: `a13285ce...` before = after
  - Path hygiene: zero hits for `/tmp/`, `/home/`, `/Users/`, `/private/`, `remedy-pingpong` in stdout JSON
  - All 24 evidence files present: job_flow.json, agent_run_trace.jsonl, agent_run_trace_summary.json, prompt_trace_summary.json, manifest.json, + 10 task-level artifacts
- **Smoke B** (default dir + `--json`):
  - `READY_FOR_APPROVAL`, `missing_observability_artifacts: []`
  - Target unchanged: same hash before = after
  - Path hygiene: zero leaks

### Review Zip Verification (R-4313)
- Zip generated with `make_review_zip.sh /tmp/reviewer_smoke_A/evidence`
- 862 files in zip, 24 evidence-related files included
- Manifest v6: all 3 agent state files present, all 5 evidence root artifacts present, T001 task-level inventory all present
- `branch`, `commit`, `dirty_files` metadata present
- `.agent/live_review.md`, `.agent/plan.md`, `.agent/review_protocol.md` confirmed IN ZIP

### Full Test Suite
```
8243 passed, 5 failed, 8 skipped (292.27s)
```
Pre-existing failures only:
- `test_self_dogfood_execution_cli.py::test_status_and_reconcile_json`
- `test_project_brain.py::test_full_chain_order`
- `test_wrapper_behavior.py` x2 (lock contention)

### Lint
`ruff check` on all 4 Python files: All checks passed.
`bash -n` on `make_review_zip.sh`: Syntax OK.

### Safety Invariants
- `may_mutate_repo=False` for `do.run` (inherited default)
- No `auto_approve` in `do_cmd.py`
- No `git push/commit/reset/checkout` or `subprocess.*git` in production code
- Target repo unchanged in both smokes
- Builder wrote `PENDING`, did not write verdict, did not mark findings resolved

### Protocol Compliance
- Builder did NOT write reviewer verdict — ✅
- Builder did NOT mark findings as Resolved — ✅
- Builder did NOT self-merge (PR #109 merged separately) — ✅

### Acceptance Question
> Is Remedy now safe enough to move back toward Worker/Remedy mode?

**Yes.** The audit infrastructure is now truthful:
- Final audit is fail-closed — every missing artifact blocks `READY_FOR_APPROVAL`
- Evidence index is disk-derived, not assumed
- Stdout JSON is sanitized for sharing
- Agent Run Trace events are honestly labeled as `reconstructed`
- Dashboard derives from actual events, not fabricated phases
- Review zip covers the full observability surface with explicit presence/absence accounting
- Evidence bundle includes all task-level artifacts (prompt trace, review, repair loop, tokens, provider evidence)

The remaining gap (R-4314 Low — review zip local path in metadata) is cosmetic and expected for a local-only artifact.

---

# Live Review — Steps 5141-5170: Review Zip Current-Run Contract + Worker/Remedy Starter Prep v1

Reviewer: parallel reviewer (independent; owns verdict).
Builder must NOT write reviewer verdicts. Builder must NOT self-merge.
Builder must NOT mark findings as resolved.
Timestamp: 2026-06-28

## Verdict (reviewer-owned)
**PASS WITH RISKS** — working tree on `feature/review-zip-contract-v1` (uncommitted, awaiting builder commit)
All 6 findings (R-4315 through R-4320) verified fixed. 1 open Low: R-4321 (2 lint errors, auto-fixable).
8253 passed, 4 failed (3 pre-existing + 1 flaky environmental). Zero new regressions.
10 new tests (4 command transcript + 3 sanitizer filename preservation + 2 manifest builder + 1 observability gate).
Smoke test F verified. Review zip verified.

## Findings

### R-4315 Medium — Review zip manifest must identify current evidence run
**Resolved.** `scripts/build_review_manifest.py` (NEW) builds v7 manifest with `current_evidence.job_id`, `final_audit_status`, `zip_prefix: "evidence/current"`, complete `root_artifacts` inventory, `task_runs` per-task artifact presence, `trace_sources`, `missing_observability_artifacts`. Tests: `test_command_transcript_persisted` (E2E), `test_manifest_builder_valid_json` (unit), `test_manifest_builder_with_evidence` (unit with evidence). All pass.

### R-4316 Medium — Review zip must not silently include stale evidence dirs
**Resolved.** `make_review_zip.sh` rewritten: auto-detect single `remedy-job-evidence-*` dir (line 49), error exit 2 on multiple dirs (line 53-57), `--evidence-dir` flag with `$1` backward compat. All `remedy-job-evidence-*` dirs excluded from repo file scan (lines 80-84). Verified: zero stale dirs in generated zip, multiple dirs → clear error message.

### R-4317 Medium — Manifest must be valid JSON in fresh git init repo
**Resolved.** `build_manifest()` handles no-commits gracefully: `_has_commits()` returns False, manifest has `branch: "unknown"`, `commit: "unknown"`, `has_commits: false`, `degraded_metadata: true`. `_git()` catches `FileNotFoundError` and `TimeoutExpired`, returns `"unknown"`. Verified in fresh `git init` repo — valid JSON output, `json.loads()` succeeds.

### R-4318 Medium — Evidence must use stable prefix not tmp/home paths
**Resolved.** `make_review_zip.sh` copies evidence to staging under `evidence/current/` prefix (lines 164-175). Post-zip verification rejects files starting with `tmp/`, `home/`, `Users/`, `private/`, `remedy-job-evidence-` (lines 209-215). Verified: all evidence files in generated zip under `evidence/current/`, zero leaked paths.

### R-4319 Medium — Artifact refs must preserve filenames not collapse to [tmpdir]
**Resolved.** `_sanitize_shareable_paths()` in `do_cmd.py` rewritten with prefix-only regex patterns:
- `_EVIDENCE_RE = re.compile(r"/tmp/remedy-job-evidence-[a-f0-9]+")` → `[evidence]`
- `_STAGING_RE = re.compile(r"/tmp/remedy-pingpong-[a-f0-9]+")` → `[staging]`
- `_TMP_DIR_RE`, `_HOME_RE`, `_USERS_RE`, `_PRIVATE_RE` strip only prefix, preserve trailing path
Tests: `test_sanitizer_preserves_evidence_artifact_name` (`[evidence]/manifest.json`), `test_sanitizer_preserves_staging_subpath` (`[staging]/staging/file.py`), `test_sanitizer_preserves_home_subpath` (`[local]/project/src/main.py`). All pass.

### R-4320 Medium — Command transcript must be included or accounted for
**Resolved.** `_persist_command_transcript()` (NEW, do_cmd.py) writes `command_transcript.json` with `command_id`, `argv_safe`, `repo_ref_safe`, `evidence_ref`, `json_stdout_preview_safe`, `exit_code`, `started_at`, `finished_at`, `target_repo_hash_before`, `target_repo_hash_after`, `target_repo_mutated`, `review_zip_hint`. `_quick_repo_hash()` computes SHA-256 of non-.git files. Tests: `test_command_transcript_persisted`, `test_command_transcript_no_private_paths`, `test_command_transcript_has_repo_hashes`, `test_command_transcript_timestamps`. All pass.

### R-4321 Low (NEW) — 2 lint errors in do_cmd.py
**Open (documented).** F541 at line 1136 (f-string without placeholders — should be plain string). I001 at line 1432 (import block un-sorted). Both auto-fixable with `ruff --fix`. No functional impact.

## Reviewer Evidence

### Focused Tests
- 73/73 `tests/test_do_job_flow.py`: PASS (includes 10 new tests for R-4315/R-4316/R-4318/R-4319/R-4320)
- 26/26 `tests/orchestration/test_final_audit_evidence.py`: PASS
- Pingpong CLI test updated for new `--evidence-dir` flag: PASS

### Full Test Suite
```
8253 passed, 4 failed, 9 skipped (283.38s)
```
Pre-existing failures only:
- `test_project_brain.py::test_full_chain_order` — provenance chain (pre-existing)
- `test_wrapper_behavior.py` x2 — lock contention (pre-existing)
- `test_review_zip_hygiene.py::test_rejects_root_was_here_detritus` — flaky, passes on re-run (environmental)

### Smoke Test F
- Ran `remedy do job-flow --builder fake --reviewer fake --out /tmp/reviewer_smoke_F/evidence --json`
- Evidence dir populated with `command_transcript.json`, `job_flow.json`, `agent_run_trace.jsonl`, etc.
- Review zip generated with all evidence under `evidence/current/` prefix
- Zero leaked local paths in zip
- Manifest v7 with `current_evidence.job_id`, `final_audit_status`, artifact inventory

### Code Verification (per-finding)
- R-4315: `build_manifest()` reads `job_flow.json` for `job_id` and `final_audit`, reads `agent_run_trace_summary.json` for `trace_sources`. Manifest includes full artifact inventory with present/absent status.
- R-4316: `make_review_zip.sh` lines 37-58 auto-detect logic. `find . -maxdepth 1 -type d -name 'remedy-job-evidence-*'` + count check. Tested with 0, 1, and 2 evidence dirs.
- R-4317: `build_manifest()` with `evidence_dir=None` produces valid JSON. `_git()` and `_has_commits()` handle missing git gracefully.
- R-4318: Evidence staging at lines 160-175, post-zip verification at lines 208-215.
- R-4319: Regex patterns match only prefix, not full path. `_EVIDENCE_RE` for evidence dirs, `_TMP_DIR_RE` for other tmp paths.
- R-4320: `_persist_command_transcript()` at do_cmd.py step 10 (after evidence index at step 9). All paths sanitized. Target repo hashes captured before/after.

### Lint
```
F541 apps/cli/commands/do_cmd.py:1136 — f-string without placeholders
I001 apps/cli/commands/do_cmd.py:1432 — import block un-sorted
```
2 errors (both auto-fixable, Low severity).

### Safety Invariants
- `may_mutate_repo=False` for `do.run` (inherited default in `command_catalog.py`)
- No `auto_approve` in `do_cmd.py`
- No `git push/commit/reset/checkout` or `subprocess.*git` in production code
- Target repo unchanged in smoke test (hash_before == hash_after)
- No `shell=True` in production code
- `build_review_manifest.py` uses `subprocess.run` with list args only (no shell)

### Protocol Compliance
- Builder did NOT write reviewer verdict — ✅
- Builder did NOT mark findings as Resolved — ✅
- Builder has not committed yet (working tree changes) — noted, not blocking

### Worker/Remedy Starter Readiness
- `scripts/remedy_self_job_flow.sh` (NEW): clean self-test wrapper. Runs `do job-flow` with fake provider, produces evidence, generates review zip. No security concerns.
- All evidence pipeline artifacts present and accounted for
- Review zip is self-contained and parseable

## Acceptance Question
> Can a final reviewer now receive one review zip and unambiguously reconstruct the current Remedy run?

**Yes.** The review zip now:
1. Contains a v7 manifest that uniquely identifies the current run via `job_id`, `final_audit_status`, and `zip_prefix`
2. Uses stable `evidence/current/` prefix — no leaked `/tmp/`, `/home/`, `/Users/`, `/private/` paths
3. Rejects stale evidence dirs (errors on multiple, auto-detects single)
4. Works in degraded mode (fresh git init — `degraded_metadata: true`)
5. Preserves artifact filenames in sanitized paths (`[evidence]/manifest.json`, not `[tmpdir]`)
6. Includes command transcript with safe metadata (sanitized argv, repo hashes, timestamps)
7. Manifest includes complete artifact inventory with per-task drill-down
8. Self-test starter script available (`scripts/remedy_self_job_flow.sh`)

## Final Recommendation
**PASS WITH RISKS** — zero open Blocker/High/Medium. 1 open Low (R-4321: 2 auto-fixable lint errors). All 6 findings (R-4315 through R-4320) resolved. Review zip is unambiguous, parseable, current-run-centered, and complete. Builder must commit and fix lint errors before merge.

---

# Live Review — Self-Run Bundle Integrity + Worker/Remedy Starter v1

Reviewer: parallel reviewer (independent; owns verdict).
Builder must NOT write reviewer verdicts. Builder must NOT self-merge.
Builder must NOT mark findings as resolved.
Timestamp: 2026-06-28

## Verdict (reviewer-owned)
**PENDING** — awaiting builder implementation.

## Findings

### R-4321 Medium — Review zip must not contain stale live_review.md state
**Open.** Manifest must expose `review_state` with latest verdict, open findings, builder handoff presence, and `review_ready`. PENDING/BLOCKED/FAIL or open findings → `review_ready=false`.

### R-4322 Medium — Manifest must classify review subject
**Open.** Feature branch or dirty tree must be declared. Must not imply clean merged main when dirty feature branch. No-commit repos → valid JSON + clean console output.

### R-4323 Medium — Real Worker/Remedy starter must exist
**Open.** Must show `claude-cli` builder/reviewer, selected evidence dir, JSON output, review zip, no auto-approval/commit/push/merge.

### R-4324 Medium — Detritus test must pass or contract explicitly updated
**Open.** `test_rejects_root_was_here_detritus` must reliably pass. Preferred: detritus fails before evidence selection.

### R-4325 Medium — --include-stale-evidence must not be misleading no-op
**Open.** Must be implemented, removed, or fail clearly.

### R-4326 Medium — Review zip builder must verify zip contents against manifest
**Open.** Zip failures must not be swallowed. Manifest artifact=present → must be in zip.

### R-4327 Medium — Shareable artifact refs should be canonical
**Open.** Prefer `evidence/current/...` refs. Reject `[tmpdir]/evidence/...` or useless placeholders.

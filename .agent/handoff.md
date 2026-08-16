# Handback — F085 R13 (record the R12 PASS, register R-0504, give `exec_guard` its first caller)

Feature T2_F085 Sandbox hardening (stage 1) · Round R13 · Branch feature/f085-sandbox-hardening
Fortschritt: ~45 % (Amendment F085 D1 angewandt · T001 gebaut · R12 PASS · T002a Scrubbing-Hälfte gebaut · die ERSTE der fünf Builder-Sites migriert · vier Sites, T002b-d, T003 offen) — Schätzung
Open findings: 119 registered, 3 resolved, 0 `Landed:` → 116 open. Max R-0504, next free R-0505. The open count RISES by exactly one this round (115 → 116), as the block declares: one registration, no resolution.

## Range

Review of 91f85510..HEAD

## Commits

### 6a916fc6 docs(f085): save the R13 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r13.md | +400 -0 | C0a — the reviewer's `.remedy-wt/f085-r13.md` copied byte-for-byte with `shutil.copyfile`, digest verified before the commit |

### 598444bd docs(f085): mirror the R13 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +391 -255 | C0b — the COMMITTED C0a blob (`git cat-file blob HEAD:.agent/authored/f085-r13.md`) copied whole, never the scratch file |

### f10b3630 docs(review): record the R12 PASS and register a vacuous-test finding
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +42 -0 | C1 — pure APPEND of REVIEW1 (the R12 PASS) then REVIEW2 (R-0504), each preceded by exactly one blank line |

### 0c94feb1 feat(f085): route the managed builder spawn through the exec guard
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/managed_builder_execution.py | +53 -9 | C2 — MBE1/MBE2 imports, MBE3 adds `_builder_exec_policy` and `_guarded_exit_code`, MBE4 replaces the `subprocess.run` spawn with `run_guarded` + a `CompletedProcess` shim |
| tests/orchestration/test_managed_builder_execution.py | +71 -7 | C2 — TEST replaces the vacuous source-text test with an AST assertion and adds three behaviour-equality tests (wall timeout, signal exit code, policy/env floor) |

### 9bcd2a45 docs(f085): advance the plan to the R13 migration round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +8 -7 | C3 — the PLAN pair over `## Current Step` and `## Next Steps`; `## Goal` and `## Risks` byte-identical to 91f85510 |

### (this commit) docs(f085): rewrite the handback for R13
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | see note | C4 — a handback cannot table the commit that writes it (R-0149); G11 orders its own count nowhere and the reviewer measures it at the next gate |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | this commit |

## External actions

`git push -u origin feature/f085-sandbox-hardening` after C3 → `91f85510..9bcd2a45`, success, upstream tracking set. A second push follows C4, then `gh pr list --state open --json number,headRefName,baseRefName,isDraft`; both are post-C4, so their outputs live in the round report (R-0494). No PR created, none merged. NO `git worktree` was added, removed or pruned — see deviation 2.

## Verification

Every exit code below is the real `subprocess.returncode` of the gate's exact argv with `cwd=/home/decodeux/Repos/remedy`; this session's Bash tool rejects `$?`, loops and `$( )` by FORM, so no code was read with `echo $?`.
G1 `git status --porcelain` EMPTY (no output) before C0a, C0b, C1, C2 and C3, and again before C4 with only `.agent/handoff.md` in flight; `.agent/STOP` re-read from disk before the FIRST and again before the LAST commit — absent both times; `git worktree list` → ONE line, `/home/decodeux/Repos/remedy  9bcd2a45 [feature/f085-sandbox-hardening]`.
G2 TRANSPORT: `.remedy-wt/f085-r13.md`, `git cat-file blob HEAD:.agent/authored/f085-r13.md` and `.agent/last_block.md` are all byte-EQUAL at sha256 e7f57d218a3bb2418b744753b46e667cfa8cf6e2ab22f43342e672c2eb865808, 23370 B, 400 lines — one digest across all three, disk-to-disk, no fallback.
G3 C1 SHAPE: the pre-C1 blob (262529 B) is a byte-exact PREFIX of the post-C1 file (266306 B) → True; the HEAD blob equals the file on disk → True; the 3777-byte remainder is byte-equal to one blank line + REVIEW1 + one blank line + REVIEW2 → True; REVIEW1 occurs 1× and REVIEW2 1× in the WHOLE file at HEAD. READING, not a prediction: `git show --numstat --format= f10b3630` → `42	0	.agent/live_review.md`; the deletion column is 0 because C1 only appends.
G4 ARITHMETIC over `.agent/live_review.md`, regexes `^- R-\d+ — `, `^Done: R-\d+ — `, `^Landed: R-\d+` (all `re.M`). Base 91f85510: 118 / 3 / 0 → 115 open, reproducing the reviewer's reading. HEAD: 119 / 3 / 0 → 116 open. REGISTERED symmetric difference `['R-0504']`; RESOLUTION symmetric difference `[]`. Duplicate registered ids `[]`; resolutions naming an unregistered id `[]`. Max R-0504, next free R-0505. A rise of exactly one, as ordered.
G5 PAIR SHAPES over the WHOLE of each target file at HEAD: MBE1 FROM 0 / TO 1, MBE4 0 / 1, TEST 0 / 1, PLAN 0 / 1 (rewrites); MBE2 FROM 1 / TO 1 and MBE3 1 / 1 (appends whose TO contains its own FROM) — all six match the shapes the block measured in its dry run. `.agent/plan.md` at HEAD: sha256 8dae6b41813aff162aeb1c5a877ab667be909c723c30bbb4dc5b3fce42f65f6d, 2437 B, 42 lines (< 50); `## Goal` and `## Risks` byte-IDENTICAL to base → True, `## Current Step` and `## Next Steps` → False, i.e. changed. R-0503 counter-measure: 124 lines added to the two SOURCE files, 16 blank/bare-docstring lines excluded, 108 considered, 3 repeat — see deviation 3.
G6 CALLER `git grep -l -E 'from packages.orchestration.exec_guard import|from packages.orchestration import exec_guard|import exec_guard' -- packages tests` → exit 0 at both ends. Base: ONE path, `tests/orchestration/test_exec_guard.py`. HEAD: THREE — `packages/orchestration/managed_builder_execution.py`, `tests/orchestration/test_exec_guard.py`, `tests/orchestration/test_managed_builder_execution.py`. The guard has a real caller in the running system for the first time.
G7 IMPORT PATH first, from the primary checkout: `managed_builder_execution.__file__` = `/home/decodeux/Repos/remedy/./packages/orchestration/managed_builder_execution.py`, `exec_guard.__file__` = `/home/decodeux/Repos/remedy/./packages/orchestration/exec_guard.py`, `_builder_exec_policy` present True, `_guarded_exit_code` present True. Then BEHAVIOUR: `python3 -m pytest tests/orchestration/test_managed_builder_execution.py -q` → exit 0, `132 passed in 1.67s` at HEAD and exit 0, `129 passed in 0.50s` at base; `python3 -m pytest tests/orchestration/test_exec_guard.py -q` → exit 0, `12 passed` at base AND at HEAD, unchanged.
G8 RED CONTROLS in a disposable `git archive HEAD` extraction at `.remedy-wt/r13_red` (deviation 2), imports proven to resolve inside the copy, baseline exit 0 `132 passed`, the file restored from a pristine copy between each mutation. Each mutation reddened EXACTLY the named test, every other test staying green: (a) a direct `subprocess.run` inserted into `run_managed_builder` → exit 1, red = `[test_spawn_goes_through_the_guard_and_never_through_a_shell]`; (b) the `wall_timeout` re-raise disabled → exit 1, red = `[test_wall_timeout_is_translated_into_the_timeout_status]`; (c) `_guarded_exit_code` returning `guarded.returncode` unconditionally → exit 1, red = `[test_a_signal_death_keeps_the_negative_exit_code_contract]`; (d) the `env_allowlist` field deleted → exit 1, red = `[test_builder_policy_reproduces_the_sanitized_env_and_floors_it]`. Restored → exit 0, `132 passed`, red NONE. `git status --porcelain` in the PRIMARY checkout was empty at every step and the copy was deleted afterwards.
G9 RUFF `python3 -m ruff check packages/orchestration/managed_builder_execution.py tests/orchestration/test_managed_builder_execution.py` → exit 0, `All checks passed!` at base AND exit 0, `All checks passed!` at HEAD, so no pre-existing error is read as new.
G10 STATE READERS `python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -q` → exit 0, `157 passed` at base and at HEAD, which also proves `test_no_shell_true_in_orchestration` still runs. CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, `42 passed` at base and at HEAD.
G11 COMMIT HYGIENE, three readings. `git diff --name-only 91f85510..HEAD` measured BEFORE C4 → exit 0, six paths: `.agent/authored/f085-r13.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `packages/orchestration/managed_builder_execution.py`, `tests/orchestration/test_managed_builder_execution.py`. Equals the seven declared paths minus `.agent/handoff.md` → True; 0 paths outside it. INSERTIONS (`+` column of `git show --numstat`): C0a 400, C0b 391, C1 42, C2 53 + 71 = 124, C3 8 — none exceeds 500; C4's own count is ordered nowhere. `git log --format=%h %p 91f85510..HEAD` → ONE parent per commit, linear 91f85510 ← 6a916fc6 ← 598444bd ← f10b3630 ← 0c94feb1 ← 9bcd2a45. `git reflog` → HEAD@{0}..HEAD@{4} are this round's five commits, every entry prefixed `commit:`, HEAD@{5} is 91f85510 the R12 handback; no amend, rebase, reset, branch switch or force-push.
G12 STALENESS, MEASURED and deliberately NOT fixed here. (1) `packages/orchestration/exec_guard.py` still says "NO CALLER. Nothing in this repository imports this module yet." — G6 now names three importers, so the sentence is FALSE at this commit; the same block's "CHOOSING an allowlist per command class is T002a's migration half and is not done here" is outdated for the same reason. (2) `packages/orchestration/managed_builder_execution.py`'s module docstring ("This module is the ONLY place in the codebase that may invoke subprocess for builder execution", "shell=False ALWAYS") and `run_managed_builder`'s own docstring ("This is the ONLY function that executes a subprocess for builder adapters. shell=False ALWAYS.") are outdated: the spawn is now `exec_guard.run_guarded`'s `subprocess.Popen`, which passes no `shell` keyword at all. Both edits belong with the four remaining sites in R14, as the block orders.

## Authored-text proofs

All twelve slices — REVIEW1, REVIEW2, MBE1F/T, MBE2F/T, MBE3F/T, MBE4F/T, TESTF/T, PLANF/T — were extracted from the COMMITTED `.agent/last_block.md` (byte-equal to `.agent/authored/f085-r13.md` and to the reviewer's `.remedy-wt/f085-r13.md` by G2, so this is a disk-to-disk proof and not a digest fallback) by their one-line `<<<SLICE …>>>` / `<<<END …>>>` markers programmatically, never retyped, never split by substring, and applied byte-verbatim. Each applier verified its FROM occurred EXACTLY once immediately before replacing it — MBE1 1, MBE2 1, MBE3 1, MBE4 1, TEST 1, PLAN 1 — and G5 measured every pair again over the whole file after the commit. No marker LINE reached any target file: `<<<SLICE` and `<<<END` occur 0 times in the C1 remainder, in `.agent/plan.md` and in the two source files at HEAD. No slice was corrected, reformatted or interpreted: the regex-looking text and backticks inside REVIEW1 and REVIEW2 landed as prose.

## Deviations & assumptions

1. The ordered sequence C0a, C0b, C1, C2, C3, C4 was followed EXACTLY — six commits, none added, none dropped, no reordering, and no commit outside it. The change set is the seven declared paths and nothing else; `.agent/context.md` and `.agent/decisions.md` were deliberately not touched, as the block orders.
2. G8 says "disposable worktree" while constraint 3 says "No worktree is added, removed or pruned" and G1 orders `git worktree list` to print ONE line. Reconciled in favour of the two hard constraints: the disposable tree is a `git archive HEAD` extraction into the gitignored `.remedy-wt/r13_red`, not a `git worktree add`. It is isolated from the primary checkout exactly as G5 of the self-drive protocol requires, its `__file__` probes prove the mutated copy is what pytest imported, and `git worktree list` stayed at one line throughout.
3. G5's R-0503 once-check reports three added SOURCE lines occurring more than once among the added lines: `import tempfile`, `with tempfile.TemporaryDirectory() as td:` and `save_command_template(t, data_dir=Path(td))`. Measured, not repaired: each occurs exactly twice inside the reviewer's own TESTT slice (the two new integration tests share that fixture boilerplate), and TESTT itself occurs exactly ONCE in the committed test file, so nothing was applied twice. The check's purpose — catching a doubled application — is met.
4. `cp` and the `remedy` CLI are denied in this session, so C0a and C0b used `shutil.copyfile` and `git cat-file blob`, which constraint 1 explicitly permits; G2 proves the BYTE property the gate names rather than the tool. Gate scratch — the slice extractors, the pre-C1 and remainder blobs, the pristine source copy and this draft — lives under the gitignored `.remedy-wt/`; nothing there entered the change set and `git status --porcelain` was empty at every commit.
5. Commit Gate at C0a–C2: `.agent/plan.md` still described R12, because C3 is the bundle's fifth commit — the known R-0491 shape, which this bundle carries unchanged.
6. Stated-cause overage (DECISION D15): this file is 95 lines, within the ≤100 allowance the >5-commit case grants and over the 60-line base cap. Cause is mandated content only — six per-commit tables, the item-status table, and a TWELVE-gate verification block in which G3 carries the prefix/remainder proof, G4 the full symmetric-difference arithmetic, G5 six pair tallies plus the plan digest, G8 four named red controls and G12 two quoted staleness findings. No section was dropped and no transcript was padded.

7. The dispatching message announced "fourteen gates"; the block on disk numbers TWELVE, G1 through G12. The block is authoritative and all twelve were run, including every sub-part — G7's import-path probe, G8's four red controls, G10's canary and G11's three readings, which is plausibly where the higher count came from. Reported as a discrepancy in the brief, not a gate failure: no gate contradicted the block.

## Next

- FIRST, per Phase 1 rule 1 of docs/agents/self_drive_protocol.md, re-read `.agent/STOP` from disk: Phase 0 is one-shot while G6 binds at any point. It was absent when this round read it before its first and last commits, which says nothing about the next session;
- THEN the Open PR Gate (Phase 1 rule 2): the `gh pr list` output for this round is in the round report, post-C4 (R-0494); no PR was created and none merged;
- then T002a's four REMAINING builder sites of amendment F085 D1 — `pingpong_provider.py`:952, 1075, 1208 and `stream_evidence.py`:595 — move to `run_guarded` the same way `managed_builder_execution.py` did here, each with its own behaviour-equality goldens, and G12's two stale texts are corrected in that same round;
- the R13 verdict is written by the NEXT round's record commit.

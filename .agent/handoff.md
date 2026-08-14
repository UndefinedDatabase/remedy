# Handback — F077 Autonomy watchdog · R10 (T002 wiring)

Branch `feature/f077-autonomy-watchdog`. Base `24600478`.
Fortschritt: `~70 % (T001 ✅ · T002 Aktion ✅ unverdrahtet · Verdrahtung R10 · T003 offen) — Schätzung`

## Range
Review of `24600478..HEAD`.

## Commits

### 02362a1b chore(f077): save the R10 block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f077-r10.md | +293/-0 | C0a, byte for byte |

### ca791c52 chore(f077): mirror the R10 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +293/-99 | C0b, `cp` disk-to-disk |

### 4f771e3c docs(f077): record the R9 verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C1, authored GATE-R9 slice appended |

### c84aecac docs(f077): register decision D9 on the e2e guard probe
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +40/-0 | C2, authored DECISION-D9 slice appended |

### 908d0df5 feat(f077): call the autonomy watchdog from run_mission
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/watchdog.py | +50/-8 | C3a `watchdog_pass`; the module's "no caller" clause repaired with it |
| packages/orchestration/orchestrator_loop.py | +15/-0 | C3b the call site |
| packages/orchestration/mission_state.py | +5/-0 | C3c pair MS-DOCSTRING |
| apps/cli/commands/mission_cmd.py | +4/-0 | C3d pair CMD-DOCSTRING |
| tests/orchestration/test_watchdog.py | +196/-4 | C3e three loop tests; stale "no call site" comment repaired |

### b7ee075c chore(f077): mirror the R10 wiring round into plan and context
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +33/-29 | C4, R10 current, R11/R12 ahead, blocker + resume re-trip risk |
| .agent/context.md | +16/-11 | C4, watchdog now described as WIRED; `## Steps` extended |

### (this commit) chore(f077): handback R10
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C5; a handoff cannot table its own commit (R-0149) |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | wiring, both pairs and three tests landed; see Deviation 1 for the guard it broke |
| C4 | done | |
| C5 | done | this file |

## External actions
`git worktree add .remedy-wt/redproof-r10 HEAD --detach` → created at `908d0df5`; `git worktree remove --force`
+ `git worktree prune` → list back to 1 line. `git push -u origin feature/f077-autonomy-watchdog` → gate 16. No PR.

## Verification
1. `git status --porcelain` EMPTY; `git worktree list` 1 line.
2. `cmp .agent/authored/f077-r10.md .agent/last_block.md` exit 0; shared sha256
   `da0b9f66dbdc642b17adba8c2ee26fb3e6442055850bdf194d910dfb9fc7e031`; 293 lines each.
3. `^Gate: R9 — PASS` in live_review → 1; `^## Steps` in live_review → 1; `^## DECISION F077 D9 ` in decisions → 1.
4. Open set recomputed mechanically: 21 registered, 2 resolved (R-0383, R-0384), no duplicate id → NINETEEN open:
   R-0361/0362/0363/0364/0367/0368/0369/0371/0374/0375/0376/0377/0378/0379/0380/0381/0382/0385/0386.
5. `import packages.orchestration.orchestrator_loop` exit 0; `import packages.orchestration.watchdog` exit 0.
6. `test_watchdog.py` base `25 passed` → HEAD `28 passed`; `grep -c "def test_"` 28 (nothing skipped/double-collected).
   `test_orchestrator_loop.py` base `196 passed` → HEAD **`1 failed, 195 passed`** (Deviation 1).
   C3b anchor: `grep -c` of `_record(iteration, context.digest, move.model_dump(), outcome, cost)` → **2**; only one
   is followed by the `if outcome.terminal:` three-liner, and that unique one is where the call went.
7. `tests/cli/test_mission_cmd.py` → `83 passed`.
8. PROBE `tests/orchestration/test_mission_e2e.py`: base `24 passed` → HEAD `24 passed`. GREEN; file untouched.
   All three tripwires stayed inert, as D9 read them: `no_progress` is cleared by each `declare_milestone_done`
   (longest run 2 vs threshold 3); `burn_anomaly` sees 0 measured entries (that scenario writes `usage: None`)
   against `burn_min_samples + burn_window` = 8; `goal_drift` sees only M001 and M002, both in the plan.
9. `ruff check` over the five changed files under packages/apps/tests → `All checks passed!`.
10. Canary `tests/cli/test_golden_path.py` → `42 passed`.
11. `pytest tests/ -q -k "dashboard_contract or resource_safety or test_runner"` → `216 passed, 16648 deselected`,
    re-run AFTER the C4 edits; both drafts validated against every assertion that reads them first (R-0162).
12. `integrity check --json` → `passed: true`, `fail_count: 0`, `check_count: 5`, `high_blockers_open`:
    "no open blocker/high findings".
13. RED-PROOF in `.remedy-wt/redproof-r10` at `908d0df5` with the C3b call deleted → `2 failed, 26 passed`:
    `test_three_dispatches_in_a_row_trip_no_progress_through_the_loop` and
    `test_the_paused_mission_dispatches_nothing_on_the_next_run` (`assert 'iteration_failed' == 'mission_not_active'`).
    The new tests do reach the call site. The third is the NEGATIVE control and passes without the call by
    construction — it asserts zero watchdog entries — which is what a negative control is, not a gap.
14. Insertions per commit (C0a…C5): 293, 293, 2, 40, 270, 49, 100. None over 500.
15. `test -e .agent/STOP` → ABSENT before the round, ABSENT at handback.
16. `git push -u origin feature/f077-autonomy-watchdog` run at handback; branch in sync with origin.
17. Trailing-whitespace scan over all twelve touched files → none; all newline-terminated.

## Authored-text proofs
`cmp` exit 0 (gate 2). GATE-R9 re-extracted from the committed authored file, present in `.agent/live_review.md`
exactly 1x, 2919 bytes / 2904 chars. DECISION-D9 present in `.agent/decisions.md` exactly 1x, 2559 bytes /
2547 chars. Both pairs APPEND-shaped and proved as such: FROM exactly 1x in each target file, TO literally
contains FROM, every TO-only line exactly 1x among that commit's ADDED lines. Zero marker lines reached any file.

## Deviations & assumptions
1. **BLOCKER, declared, NOT repaired.**
   `test_orchestrator_loop.py::TestTheLedgerCoversEveryIteration::test_one_entry_per_iteration_numbered_from_one`
   is RED at HEAD. It scripts three identical dispatches on M001 under `max_iterations=3` — exactly the
   `no_progress` pattern — so its ledger reads `[1, 2, 3, 3]` against `== [1, 2, 3]`, and its second assertion
   `all(kind == "dispatch_job")` breaks too. The extra entry carries the loop's own iteration number, i.e.
   DECISION F077 D6 working as designed: a stale whole-ledger guard of exactly the class D8 predicted, in a file
   D8 and D9 never examined. The block names twelve files, says "nothing beyond them", and makes gate 8 the SOLE
   authority for a thirteenth (`test_mission_e2e.py`, which measured green), so no gate authorises repairing this
   one; per the block's closing STOP clause it is reported, not repaired, and the round ends here. C3 was still
   committed: without it gates 6, 8 and 13 are not reproducible, and AGENTS.md "If Blocked" directs committing
   the valid completed portion and recording the exact blocker in `.agent/plan.md`, which C4 does.
2. Two docstring repairs beyond the two authored pairs, both inside already-declared files and both made false by
   C3 itself: `watchdog.py`'s "It has NO caller in `orchestrator_loop` at this commit", and the `test_watchdog.py`
   section comment asserting the same. Leaving either would re-create the R-0384 defect in the commit causing it.
3. **Deviations, declared** (DECISION D15): this handback is 126 lines against the ≤100 a >5-commit round allows.
   Cause is mandated content — six per-commit tables plus the self-referential seventh, the item-status table, the
   seventeen-gate verification table, the authored-text proofs, and Deviation 1, which is the one thing the next
   round cannot start without. No section was dropped to meet the cap.

## Next
R11 repairs that single stale guard — the only red on the branch — then starts T003.

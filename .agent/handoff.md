# Handback — F077 Autonomy watchdog · R14 (T003, first half: CLI + resume)

Branch `feature/f077-autonomy-watchdog`. Base `15a075c3`. Last work commit
`824684bb`; the handback commit follows it and touches only this file.
Fortschritt: `~85 % (T001 ✅ · T002 ✅ · T003 halb: CLI + resume gebaut, Report offen) — Schätzung`

## Range
Review of `15a075c3..HEAD`. Twelve files, exactly the ordered change set;
`apps/cli/commands/worker_facade_cmd.py` was NOT touched.

## Commits
| SHA | Subject | Paths | +/- |
|---|---|---|---|
| 62d8a327 | save the R14 block verbatim | .agent/authored/f077-r14.md | +364/-0 |
| a9b5bed0 | mirror the R14 block into last_block | .agent/last_block.md | +316/-189 |
| 3985bda9 | record the R13 verdict | .agent/live_review.md | +2/-0 |
| 66cbd558 | extract the read-only evaluate_mission | packages/orchestration/watchdog.py; tests/orchestration/test_watchdog.py | +36/-14; +89/-3 |
| c472d7ac | add the mission watchdog command | apps/cli/command_catalog.py; apps/cli/commands/mission_cmd.py; tests/cli/test_mission_cmd.py | +14/-0; +38/-0; +70/-0 |
| 2fc976f6 | add the mission resume verb | the same three files | +14/-0; +12/-3; +57/-0 |
| 824684bb | DECISION D12 + state mirror | .agent/decisions.md; .agent/context.md; .agent/plan.md | +34/-0; +14/-5; +16/-17 |

The handback commit rewrites `.agent/handoff.md` alone and cannot table itself.

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | own commit — the shared stage measured 680 insertions (Deviation 1) |
| C1 | done | GATE-R13 appended verbatim; it is the only slice for that file |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | this file |

## External actions
`git worktree add --detach .remedy-wt/f077-r14-redproof HEAD` → created at
`2fc976f6`; `git worktree remove` + `git worktree prune` → `git worktree list`
back to 1 line, tree clean. `git push -u origin feature/f077-autonomy-watchdog`.
No `gh`, no PR.

## Verification — every value measured in this run, none copied
| # | Gate | Measured |
|---|---|---|
| 1 | `git status --porcelain` / `git worktree list` | EMPTY / 1 line |
| 2 | `cmp` authored vs last_block | exit 0; shared sha256 `32e1a40869ac0cd89c68bf411ac29c37b4e8052df8744c5fcebdf6867955d4d4`; 364 lines; both equal the source under `.remedy-wt/` |
| 3 | `^Gate: R13 — ` / `^Landed: ` | 1 / **1** (the residual `Landed: R-0384` is R-0380's live evidence and was left) |
| 4 | open set, recomputed | 27 registered − 4 `Done:` (R-0383, R-0384, R-0388, R-0390) = **23 open**; no duplicate id; next free **R-0393** |
| 5 | `^## DECISION F077 D12 ` | 1 |
| 6 | `test_watchdog.py` + `test_mission_e2e.py` | **56 passed** (52 at base; C2 adds 4) |
| 7 | `tests/cli/test_mission_cmd.py` | **92 passed** (83 at base; C3 adds 5, C4 adds 4) |
| 8 | catalog + grouped-cli + worker-facade | **576 passed** — unchanged, no fall |
| 9 | `test_orchestrator_loop.py` | **196 passed** — unchanged |
| 10 | canary `test_golden_path.py` | **42 passed** |
| 11 | `-k "dashboard_contract or resource_safety or test_runner"` | **216 passed, 16661 deselected** (deselected +13 = the 13 tests added; Deviation 2). Run after drafting both state files, before committing C5; every test reading `.agent/plan.md` or `.agent/context.md` was grepped first and the drafts validated against `test_test_runner.py` (Goal/Next Steps/F-id; Active Branch/`feature/`/F-id) and `test_resource_safety.py` (`resource` or `pytest`) |
| 12 | scoped `ruff check` (5 files) | `All checks passed!` |
| 13 | `integrity check --json` | passed=true, fail_count=0, check_count=5, `high_blockers_open` pass; `handler_import` now reads `handlers=336` (Deviation 3) |
| 14 | RED-PROOF, disposable worktree at `2fc976f6` | See below — both mutations bite |
| 15 | `wc -l .agent/plan.md` | **43** |
| 16 | insertions per commit | 364, 316, 2, 125, 122, 83, 64 — none over 500 |
| 17 | `.agent/STOP` | ABSENT before the round and ABSENT at handback |
| 18 | `git diff --check 15a075c3..HEAD` | no output |
| 19 | `git diff --name-only 15a075c3..HEAD` | the twelve ordered files and nothing else |
| 20 | push | `git push -u origin feature/f077-autonomy-watchdog` |

Gate 4's names, in record order: R-0380, R-0381, R-0361, R-0362, R-0363,
R-0364, R-0367, R-0368, R-0369, R-0371, R-0374, R-0375, R-0376, R-0377,
R-0378, R-0379, R-0382, R-0385, R-0386, R-0387, R-0389, R-0391, R-0392.

Gate 14, colour observed, never predicted. The worktree was proven green first
(`-k "Resume or Watchdog"` → `9 passed, 83 deselected`), and its tests import
from the worktree because `_run` spawns `apps.cli.grouped` with `cwd` set to
`Path(__file__).resolve().parents[2]` (R-0337).
(a) `"resume": MISSION_STATUS_PAUSED` → `1 failed, 3 passed, 88 deselected`;
`TestMissionResume::test_pause_then_resume_leaves_the_mission_active` fails on
`AssertionError: assert 'Status: active' in '…\n  Status: paused\n'`. Reported
honestly: `test_the_json_shape_matches_show` stays green under this mutation by
construction — it compares `resume`'s JSON to `show`'s, and both read `paused`.
(b) `milestone_ids=()` in `evaluate_mission` → `7 failed, 25 passed, 24 errors`.
All four new tests fail; `test_evaluate_mission_reports_no_trip_for_a_quiet_ledger`
fails on `Left contains one more item: Trip(kind='goal_drift', …
"not one of the mission plan's 0 milestones"…)` and the other three on
`assert 2 == 1`. Both mutations reverted; `git status --porcelain` in the
worktree was empty before removal.

## Authored-text proofs — disk to disk, against the COMMITTED authored file
- GATE-R13: `sed -n '279p' .agent/authored/f077-r14.md` and `tail -n 1
  .agent/live_review.md` both sha256 `3655993b572915dce3c0b1e22bdb2fe173cae746c1a61bffe79afe303d5227b7`.
- DECISION-D12: `sed -n '286,318p'` of the authored file and `tail -n 33
  .agent/decisions.md` both sha256 `54c23a5165534890983ebbe1fcee69f998c113d1659af2f32bc4f956778c4a7e`.
- DOCSTRING pair: FROM is 0x in `mission_cmd.py` (both its lines grep to 0);
  TO is 1x — `sed -n '331,334p'` of the authored file and `sed -n '8,11p'
  apps/cli/commands/mission_cmd.py` both sha256
  `f2971a729cc1691296f742dee7ccd381a21a49266bd43266927fc84dd77cd09f`.

## Deviations, declared
1. **C0a and C0b are two commits, not one.** The block permits them to share
   one; staged together `git diff --cached --stat` measured **680 insertions**
   against the 500 cap, and two distinct files are not AGENTS.md's SINGLE
   state-file exemption. Split: +364 then +316.
2. **Gate 11's deselected number is 16661, not the ordered-expectation 16648.**
   The delta is exactly +13, the 13 tests this round adds (4 in
   `test_watchdog.py`, 9 in `test_mission_cmd.py`). Unadjusted, as ordered.
3. **`integrity check` reports `handlers=336`, not the inventory's 334.** The
   two new catalog entries and their two handlers. Not an ordered value;
   recorded because it is a measured number that moved.
4. **Three truth repairs inside ordered files, beyond the ordered slices.**
   Each fixes a sentence the ordered change itself made false: (i)
   `test_watchdog.py`'s module docstring gains a bullet for `evaluate_mission`
   and no longer calls the `run_mission` block "the last section", because the
   new section is now last; (ii) `_cmd_mission_set_status`'s own docstring now
   names `resume` (inventory Q3 lists it as a prose copy to extend); (iii)
   `watchdog_pass`'s inline comment no longer says "the two reads above", since
   those reads moved into `evaluate_mission`. No `Gate:`, `Done:`, `- R-NNNN`
   or `Landed:` line was authored anywhere this round.
5. **This handoff is 134 lines.** Cause per DECISION D15: the 20-row
   verification table, the per-commit table, the item-status table over eight
   items, the three authored-text proofs, the two red-proof transcripts, the 23
   finding names and the mandated 5-part Next section. No section dropped.

## Next
1. Phase 1 rule 1 of `docs/agents/self_drive_protocol.md` — re-read
   `.agent/STOP` FROM DISK before rule 2's Open PR Gate.
2. Rule 2, the Open PR Gate. There is NO open PR for this branch, and one is
   created at closure, not before.
3. R15 builds the report surface under DECISION F077 D12 — the trip lead block
   in `_cmd_mission_show` and its tests — and owes R14's own `Gate: R14 — `
   paragraph as its FIRST commit, before any code. If that commit is missing,
   the record has lost a round.
4. R16 is the integration gate, then closure.
5. Open findings: **23** — R-0380, R-0381, R-0361, R-0362, R-0363, R-0364,
   R-0367, R-0368, R-0369, R-0371, R-0374, R-0375, R-0376, R-0377, R-0378,
   R-0379, R-0382, R-0385, R-0386, R-0387, R-0389, R-0391, R-0392. Next free
   id: **R-0393**.

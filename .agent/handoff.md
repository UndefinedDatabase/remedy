# Handback — F077 Autonomy watchdog · R15 (T003 complete: the trip leads `mission show`)

Branch `feature/f077-autonomy-watchdog`. Base `9ef5c62b`. Last work commit
`7c5749a7`; the handback commit follows it and touches only this file.
Fortschritt: `~92 % (T001 ✅ · T002 ✅ · T003 ✅ CLI, resume und Report) — Schätzung`

## Range
Review of `9ef5c62b..HEAD`. Ten files, exactly the ordered change set;
`worker_facade_cmd.py`, `command_catalog.py` and `mission_state.py` untouched.

## Commits
| SHA | Subject | Paths | +/- |
|---|---|---|---|
| 261bf016 | save the R15 block verbatim | .agent/authored/f077-r15.md | +277/-0 |
| 053408ab | mirror the R15 block into last_block | .agent/last_block.md | +221/-308 |
| f4f0254f | record the R14 verdict and register R-0393 | .agent/live_review.md | +4/-0 |
| 05941d40 | read the recorded trips back out of a ledger | packages/orchestration/watchdog.py; tests/orchestration/test_watchdog.py | +47/-0; +89/-0 |
| 826fb5a3 | lead a paused mission's show with the trip | apps/cli/commands/mission_cmd.py; tests/cli/test_mission_cmd.py | +43/-2; +130/-0 |
| 7c5749a7 | mirror R15 into plan and context | .agent/context.md; .agent/plan.md | +17/-5; +22/-20 |

The handback commit rewrites `.agent/handoff.md` alone and cannot table itself.

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | own commit (Deviation 1) |
| C1 | done | GATE-R14 then FINDING-R393, verbatim, before any code |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | this file |

## External actions
`git worktree add --detach .remedy-wt/f077-r15-redproof HEAD` → created at
`826fb5a3`; both mutations reverted, `git worktree remove` + `git worktree
prune` → `git worktree list` back to 1 line. `git push -u origin
feature/f077-autonomy-watchdog`. No `gh`, no PR.

## Verification — every value measured in this run, none copied
| # | Gate | Measured |
|---|---|---|
| 1 | `git status --porcelain` / `git worktree list` | EMPTY / 1 line |
| 2 | `cmp` authored vs last_block | exit 0; shared sha256 `d38d23f676fc6d7ae65b3dc4959cf83cddfa20a6ce1a20219dd1a07dfdc284ae`; **277 lines** each; both equal the source under `.remedy-wt/` |
| 3 | `^Gate: R14 — ` / `^- R-0393 — ` / `^Landed: ` | 1 / 1 / **1** (the residual `Landed: R-0384` is R-0380's live evidence and was left) |
| 4 | open set, recomputed | 28 registered − 4 `Done:` (R-0383, R-0384, R-0388, R-0390) = **24 open**; no duplicate id; next free **R-0394** |
| 5 | `test_watchdog.py` + `test_mission_e2e.py` | **61 passed** (56 at base; C2 adds 5) |
| 6 | `tests/cli/test_mission_cmd.py` | **97 passed** (92 at base; C3 adds 5) |
| 7 | catalog + grouped-cli + worker-facade | **576 passed** — unmoved, as ordered |
| 8 | `test_orchestrator_loop.py` | **196 passed** — unmoved |
| 9 | canary `test_golden_path.py` | **42 passed** |
| 10 | `-k "dashboard_contract or resource_safety or test_runner"` | **216 passed, 16671 deselected** (deselected +10 = the 10 tests added; Deviation 2). Run after drafting both state files, before committing C4; every test reading `.agent/plan.md` or `.agent/context.md` was grepped first (8 files) and the drafts validated against `test_test_runner.py` (Goal/Next Steps/F-id; Active Branch/`feature/`/F-id), `test_dashboard_contract.py` (`Steps` in both) and `test_resource_safety.py` (`resource` or `pytest`) |
| 11 | scoped `ruff check` (4 files) | `All checks passed!` |
| 12 | `integrity check --json` | passed=true, fail_count=0, check_count=5, `high_blockers_open` pass; `handler_import` reads `handlers=336`, unmoved, as ordered |
| 13 | RED-PROOF, disposable worktree at `826fb5a3` | See below — both mutations bite |
| 14 | `wc -l .agent/plan.md` | **45** |
| 15 | insertions per commit | 277, 221, 4, 136, 173, 39 — none over 500 |
| 16 | `.agent/STOP` | ABSENT before the round and ABSENT at handback |
| 17 | `git diff --check 9ef5c62b..HEAD` | no output; all 9 range files newline-terminated (checked byte-wise) |
| 18 | `git diff --name-only 9ef5c62b..HEAD` | the nine files above; this commit makes the tenth, `.agent/handoff.md` |
| 19 | push | `git push -u origin feature/f077-autonomy-watchdog` |

Gate 4's names, in record order: R-0380, R-0381, R-0361, R-0362, R-0363,
R-0364, R-0367, R-0368, R-0369, R-0371, R-0374, R-0375, R-0376, R-0377,
R-0378, R-0379, R-0382, R-0385, R-0386, R-0387, R-0389, R-0391, R-0392, R-0393.

Gate 13, colour observed, never predicted. ONE selection string, used unchanged
for the baseline and for BOTH mutations (finding R-0393): over
`tests/orchestration/test_watchdog.py tests/cli/test_mission_cmd.py`,
`-k "ShowLeadsWithTheTrip or reports_no_trip or round_trip_through_the_ledger
or later_one or fixed_kind_order or torn_trip_entry"` → 12 selected, 122
deselected at every run. The 12 are the round's 10 new tests plus
`test_evaluate_mission_reports_no_trip_for_a_quiet_ledger` and
`TestMissionWatchdog::test_an_unrun_mission_reports_no_tripwires`, which the
`reports_no_trip` term also matches. The CLI tests import from the worktree
because `_run` spawns `apps.cli.grouped` with `cwd=Path(__file__).parents[2]`
(R-0337). Baseline `12 passed, 122 deselected`.
(a) first-per-kind instead of last in `latest_trips_from_ledger` →
`1 failed, 11 passed, 122 deselected`;
`test_two_entries_of_one_kind_report_only_the_later_one` fails on
`AssertionError: assert 'the first reading' == 'the later reading'`.
(b) `if True or mission.status == MISSION_STATUS_PAUSED` in `_cmd_mission_show`
→ `1 failed, 11 passed, 122 deselected`;
`TestShowLeadsWithTheTrip::test_an_active_mission_with_an_old_trip_gets_no_lead`
fails on `AssertionError: assert 'STOPPED' not in 'STOPPED: th...inked yet)\n'`.
Both mutations reverted and each mutated file verified byte-identical to HEAD's
with `cmp` before the worktree was removed.

## Authored-text proofs — disk to disk, against the COMMITTED authored file
Both slices are one physical line, extracted from `.agent/authored/f077-r15.md`
by line index and never retyped.
- GATE-R14: authored line 244 and `.agent/live_review.md` line 116 both sha256
  `7d045e07041bf746c6e593f5a8909d751ab6651740067ab2687e07638718c48c`.
- FINDING-R393: authored line 248 and `.agent/live_review.md` line 118 both
  sha256 `3bb62290030b72dc5c74646bff797cda6b379ae4c23a20a9d20bfdf5d326b56c`.

## Deviations, declared
1. **C0a and C0b are two commits, not one.** Unlike R14 this was NOT forced:
   staged together they measure 277 + 221 = **498 insertions**, inside the 500
   cap. Split anyway, because two unrelated whole-file rewrites in one commit
   is the mixed diff AGENTS.md Commit Discipline warns about, and the R14
   precedent already reads as two commits. Declared because the block's split
   clause was conditional and its condition did not fire.
2. **Gate 10's deselected number is 16671, not the base 16661.** The delta is
   exactly +10, the 10 tests this round adds (5 in `test_watchdog.py`, 5 in
   `test_mission_cmd.py`). Unadjusted, as ordered.
3. **One docstring line beyond the ordered slices**, in
   `tests/orchestration/test_watchdog.py`: its module docstring enumerates what
   each test in the file pins, and the ordered change adds a section that
   enumeration would otherwise silently omit, so it gains one bullet for
   `latest_trips_from_ledger`. Same class of repair as R14's Deviation 4. No
   `Gate:`, `Done:`, `- R-NNNN` or `Landed:` line was authored anywhere.
4. **This handoff is 133 lines.** Cause per DECISION D15: the 19-row
   verification table, the per-commit table, the item-status table over seven
   items, the two authored-text proofs, the gate-13 pair transcript with its
   stated selection string, the 24 finding names and the mandated 5-part Next
   section. No section dropped.

## Next
1. Phase 1 rule 1 of `docs/agents/self_drive_protocol.md` — re-read
   `.agent/STOP` FROM DISK before rule 2's Open PR Gate.
2. Rule 2, the Open PR Gate. There is NO open PR for this branch, and one is
   created at closure, not before.
3. R16 is the INTEGRATION GATE per `docs/agents/integration_gate.md`. It owes
   no gate paragraph: R15 was reviewed before this session ended, and its
   `Gate: R15 — PASS` is already on the record — R16 starts fully gated.
4. Closure follows R16 per `docs/roadmap/STATUS_closure_protocol.md`, and it
   still owes an ist-doc for the watchdog under `docs/`, registered in
   `docs/README.md`. No round has written it yet.
5. Open findings: **24** — R-0380, R-0381, R-0361, R-0362, R-0363, R-0364,
   R-0367, R-0368, R-0369, R-0371, R-0374, R-0375, R-0376, R-0377, R-0378,
   R-0379, R-0382, R-0385, R-0386, R-0387, R-0389, R-0391, R-0392, R-0393.
   Next free id: **R-0394**.

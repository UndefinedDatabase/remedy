# Handback — F031 Decision inbox, round R48 (repair)

Branch: `feature/f031-decision-inbox`. Range: Review of `20eabead`..`f42970ad`
plus this commit, which no range ending at C8 can table. THE TIP WAS RED AND IS
GREEN: `python3 -m pytest tests/ui_server/ -q` exited 1 at `20eabead`, 1 failed /
479 passed, on
`TestCommandDoorImportGuard::test_the_door_imports_exactly_the_allowed_set`; at
C8 it exits 0, 486 passed — 480 after C5's two ruled imports, plus C6's six.

## Commits

### 5b311096 docs(agent): save the F031 R48 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f031-r48.md | +389 −0 | C0a: the block saved byte for byte |

### 39c3607a docs(agent): mirror the F031 R48 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +314 −360 | C0b: same git blob as C0a |

### b0b4b499 docs(agent): advance the plan to the F031 R48 repair round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +20 −22 | C1: PLANF031R48 applied whole |

### 41a5a3e3 docs(agent): register the three findings the F031 R47 gate raised
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +6 −0 | C2: R-0697, R-0698, R-0699 |

### 28fcc704 docs(agent): record the F031 R47 verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2 −0 | C3: the `F031 R47` gate entry |

### c01d32b4 docs(agent): land DECISION F031 D25 on the blocked-round plan append
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +35 −0 | C4: DECISION F031 D25 |

### 891d06f5 test(ui-server): rule the two flight plan imports DECISION F031 D24 adds to the door
| Path | +/- | Reason |
|---|---|---|
| tests/ui_server/test_command_channel.py | +4 −0 | C5/S1: two `ALLOWED_IMPORTS` entries |

### 7286e161 test(ui-server): pin what the door answers and does for an fp decision
| Path | +/- | Reason |
|---|---|---|
| tests/ui_server/test_command_channel.py | +96 −0 | C6/S3: four tests of the answer |
| tests/ui_server/test_command_dispatch.py | +92 −0 | C6/S4: two tests of the effect |

### e2e85ce1 feat(decision-inbox): mirror the door fp branch in the answerability key
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/decision_inbox.py | +33 −17 | C7/S5,S6: `fp:` mirror + docstring |
| tests/orchestration/test_decision_inbox.py | +30 −4 | C7/S7,S8: tuple, comment, resolved test |

### f42970ad test(ui): pin the browser answers a pending flight plan card offers
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/decisionCard.test.ts | +17 −0 | C8/S9: the only browser-side evidence |

### C9 (this commit) docs(agent): write the F031 R48 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | per numstat | a handoff cannot table its own commit (R-0149) |

## External actions

`git worktree add .remedy-wt/r48gate HEAD` — created for G6/G7 at `f42970ad`.
`git worktree remove .remedy-wt/r48gate` — removed before C9.
`git push origin feature/f031-decision-inbox` is ordered after this commit.
No PR created, merged or commented on; no `gh` command run.

## Verification

Every gate RUN; one entry each, real exit codes; transcripts in the round report.

- G1 exit 0 — branch correct; porcelain 0 lines after each of C0a…C8; `.agent/STOP`
  ABSENT before C0a and before C9; block sha256 `a36a7280…5606e` / 35632 B /
  389 lines at C0a, C0b and off disk at C8, all EQUAL; C0a and C0b are one blob.
- G2 exit 0 — 4 slices extracted from the COMMITTED C0a blob; CONTENT 85,
  TOTAL 389, PROSE 389 − 85 = 304 ≤ 400, TOTAL ≤ 490.
- G3 exit 0 — plan.md at C1 byte-equal to PLANF031R48; minus-newline control
  FALSE; `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 45 (< 50).
- G4 exit 0 — 868456+1+5671=874128, 874128+1+4006=878135, 611101+1+2175=613277,
  both base blobs as the block measured them; reader (b) N=3/1/6, units 355→358,
  358→359, 1472→1478, last N equal in order; all 3 paragraph-1 flips REJECTED.
- G5 exit 0 — `^- R-\d+ — ` 257→260→260→260, ADDED at C2 exactly {R-0697,
  R-0698, R-0699}, none removed anywhere; `^Done: R-\d+ — ` 6, `^Landed: R-` 0,
  `^Gate: R\d+ — ` 19 at all four points; `^Gate: F\d+ R\d+ — ` 28→28→29→29,
  ADDED at C3 exactly {F031 R47}; ids DISTINCT, max R-0699; open 251→254;
  `^## DECISION F031 D\d+ ` 24→25.
- G6 exit 1 then 0 — the RED/GREEN line above; then, in the worktree, removing
  EITHER new `flight_plan` entry turned that same guard RED at exit 1.
- G7 exit 1, 1, 1 — all three mutations RED, each restored before the next:
  (a) the `approve`/`reject` refusal → 1 failure; (b) the
  `resolve_flight_plan_approval` call and its return → 4 failures; (c) the `fp:`
  branch of `_answerable_by_decision_resolve` → 1 failure. Names in the round
  report; no mutation left a suite green.
- G8 exit 0 on every command, serial — 42 / 486 (480 + C6's SIX) / 52 / 21 / 16
  / 561+4 skipped UNCHANGED / 35 (34 + S8's one) / 38 / 29 / 27, the last three
  UNCHANGED; `npx tsc --noEmit` 0; `npx vitest run` 0 at 30 files, 455 tests
  (454 + S9's one). Markers 0/0 in all three targets vs a live CONTROL of 4/4;
  path set 10, both residues EMPTY; every commit single-parent; insertions 389,
  314, 20, 6, 2, 35, 4, 188, 63, 17, all < 500; `git ls-files .remedy-wt` 0;
  `git worktree list` 1 line; reflog for these ten: `commit` throughout, amend/rebase/cherry 0.

## Authored-text proofs

Four slices, extracted from the committed C0a blob by marker line and applied
byte for byte: PLANF031R48 → plan.md (C1), FINDINGS48 → live_review.md (C2),
LEDGER48 → live_review.md (C3), DECISION25 → decisions.md (C4). Each proved by
whole-file equality AND by an independent paragraph reader, negative control on
the FIRST appended paragraph. All readings TRUE, all controls REJECTED (G3, G4).

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | S1; suite run on the working tree FIRST, per constraint 3 |
| C6 | done | S2–S4, six tests |
| C7 | done | S5–S8 |
| C8 | done | S9 |
| C9 | done | this commit |
| push | done | runs on exit; a commit cannot carry the reading of a push that follows it, and the block excludes that reading here |

## Deviations & assumptions

- No departure from the ordered commit sequence: C0a, C0b, C1…C9 exactly as
  constraint 2 fixes it — ten commits before this one, none extra, none dropped.
- Constraint 10 names "S1 and S6" as the two items that widen a ruled set, but
  S6 is the docstring sentence and S7 is the tuple; read as S1 and S7, the only
  reading the SPEC supports. No assertion was weakened: both widenings are the
  mechanism those guards document, and every neighbouring suite re-ran UNCHANGED.
- C6's effect tests live in a NEW class `TestFlightPlanApprovalDispatchEffects`
  with its own fixture and server helper, not inside `TestJobStopDispatchEffects`
  whose name is `job.stop`'s: sharing the helper would have mixed a refactor into
  a test commit, which AGENTS.md forbids. The ~30 duplicated lines are deliberate.
- Nothing under `docs/`, no production file outside `decision_inbox.py`.
- 11 commits, so the >10-commit handback tier applies; this file is within it.

## Open findings

254 open (`^- R-\d+ — ` 260 minus `^Done: R-\d+ — ` 6). R-0697, R-0698 and
R-0699 were registered THIS round and deliberately carry no `Done:` line: the
next round's reviewer verifies the repair before recording it.

## Next

The reviewer gates R48 off disk over `20eabead`..the C9 SHA and issues the
verdict. A new session runs Phase 1 rule 1 (`.agent/STOP`) before the Open PR
Gate. Next build round: R49, the clarification form.

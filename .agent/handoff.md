# Handback — F022 Live cost ticker · Runde 7 (T002a)

Fortschritt: ~40 % (T001 fertig · T002 zur Haelfte nach dieser Runde · T003
             offen; ab hier rechnet der Client die Fuellung und sonst nichts)
             — Schaetzung

Branch `feature/f022-live-cost-ticker`, round base `d97cdbb2`. Open set after C2: 231 records, maximum `R-0670`, two High carried forward (R-0495, R-0574), both inherited from closed features.

## Range
Review of d97cdbb2..HEAD — seven commits, C0a C0b C1 C2 C3 C4 C5, in the block's order.

## Commits
### 1be0fff5 docs(state): save the F022 R7 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f022-r7.md | +362/-0 | C0a — the block verbatim, 36027 bytes / 362 lines |

### 77e3a0ad docs(state): mirror the F022 R7 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +240/-166 | C0b — written from the committed C0a blob `bc1a9f5b` |

### a6ec63ab docs(state): point the F022 plan at R7
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +18/-14 | C1 — slice PLANF022R7, whole-text replacement |

### fd530b7c docs(state): record the F022 R6 verdict and register R-0670
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | C2 — slice LEDGER7, finding and gate paragraph in ONE commit |

### c6b026bf docs(state): rule the client cost reading as DECISION F022 D4
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +18/-0 | C3 — slice DEC4, appended |

### 8e34539b feat(ui): read one budget tick into the COST metric's render decisions
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/costMetric.ts | +210/-0 | C4 — the pure module: unit, denominator, fill, level, marker, tooltip |
| apps/ui/src/api/costMetric.test.ts | +212/-0 | C4 — U1–U7, 17 tests |
| apps/ui/src/api/types.ts | +10/-1 | C4 — `RemedyMetricKey` gains `cost`, `RemedyMetric.cost?` added |

### C5 docs(state): hand back the F022 R7 cost-module round
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C5 — this file; a handoff cannot table its own commit (R-0149) |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a block save | done | |
| C0b last_block mirror | done | |
| C1 the plan | done | |
| C2 R6 verdict + R-0670 | done | |
| C3 DECISION F022 D4 | done | |
| C4 types + module + tests | done | |
| C5 the handback | done | |

## External actions
- `git worktree add .remedy-wt/g5 HEAD --detach` then `git worktree remove` — G5 mutation controls; removed, `git worktree list` back to one line.
- `git worktree add .remedy-wt/g9 HEAD --detach` then `git worktree remove` — G9 red proofs; removed, `git worktree list` back to one line.
- `gh pr list --state open --json number,headRefName` → `[]`. No PR created, nothing merged.
- `git push` on `feature/f022-live-cost-ticker` after C5 — the only remote write this round.

## Verification
- G1 EXIT 0 — `.agent/STOP` absent, read from disk before C0a and again before C5; branch `feature/f022-live-cost-ticker`; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3 and C4.
- G2 EXIT 0 — five readings (`.remedy-wt/f022-r7.md`, C0a blob `bc1a9f5b`, C0b blob `bc1a9f5b`, `.agent/last_block.md` on disk, `.agent/authored/f022-r7.md` on disk) are ALL sha256 `2ca2930d614185ef4b32f1db7c1885cc5f8793340cafac51be75c2d84377d831` over 36027 bytes and 362 lines; the digest the delegation names agrees.
- G3 EXIT 0 — the extractor over the committed C0a blob printed 3 slices over 64 CONTENT lines; TOTAL re-measures at 362 and PROSE at 298, so constraint 11's numerals reproduce exactly.
- G4 EXIT 0 — `.agent/plan.md` at `a6ec63ab` is byte-equal to PLANF022R7 plus exactly one newline, 2418 bytes against the bare slice's 2417; the bare-slice control is FALSE; `^## Goal$` 1, `^## Next Steps$` 1, 44 lines against the cap of 50.
- G5 EXIT 0 — C2: round-base blob is a byte-exact PREFIX, remainder 8875 = 1 + 8873 + 1, independent splitter 256→258 with BOTH LEDGER7 paragraphs equal IN ORDER. C3: prefix holds, remainder 5128 = 1 + 5126 + 1, splitter 1278→1287 with all 9 DEC4 paragraphs equal in order, `^## DECISION F022 D4 ` counts 1. Controls in `.remedy-wt/g5`: bytes 504784 `R`→`r` and 506988 `t`→`T` (C2), 529223 `N`→`n` and 533968 SPACE→NUL (C3) — both readers rejected all four mutants and accepted the true file.
- G6 EXIT 0 — base `d97cdbb2`: 230 records, all DISTINCT, maximum `R-0669`, `^Done: R-` 0, `^Landed: ` 0, `^Gate: R` 6 over 6 distinct keys. C2: 231 records, all DISTINCT, maximum `R-0670`, 0, 0, 7 over 7 distinct keys. ids ADDED {R-0670}, ids REMOVED {} — exactly the expected pair; `^## Steps$` 1; the map paragraph is byte-identical at base and at C2 (1065 bytes).
- G7 EXIT 0 — `npm run typecheck` from `apps/ui` at C4, no output, agreeing with the reviewer's base reading.
- G8 EXIT 0 — `npm run test:unit` from `apps/ui` at C4: 17 test files and 235 tests passed, against the base's 16 and 218 — a difference of +1 file and +17 tests, all in `costMetric.test.ts`. Node names: U1 "shows usd and divides by the usd limit", "enumerates BOTH limits with their own fills, usd line first"; U2 "takes the unit and the denominator from the token limit", "pins all three levels and both boundaries"; U3 "spend with no limit renders the spent-only variant", "never borrows the other unit's limit as a denominator"; U4 "only an actual basis of the shown unit clears the marker", "a tokens view reads the TOKENS basis and ignores the cost basis"; U5 "states a zero and pins singular against plural", "an absent count adds no line"; U6 "every shape yields a view and throws nothing", "a limit of zero is limitless rather than a division by zero", "a non-object basis marks the figure estimated"; U7 "the comment stripper actually removes something", "the code names no price, rate or tariff", "every numeric literal is one DECISION F022 D4 clause 5 permits"; and "formats dollars to two decimals and tokens on the 1k/1M rule".
- G9 EXIT 1 on every mutant, all three inside `.remedy-wt/g9` driven from the primary install by constraint 8's route; the unmutated worktree ran 17 passed first. (a) denominator falls back to the OTHER unit's limit → 3 failed / 14 passed: both U2 cases and U3 "spend with no limit renders the spent-only variant"; U3's serialised-view case stayed GREEN — said plainly under Deviations. (b) warn threshold 0.85 → 0.95 → 2 failed / 15 passed: U2 "pins all three levels and both boundaries" as ordered, plus U7's literal guard catching the unpermitted 0.95. (c) `estimated` driven from `basis.cost` for every unit → 1 failed / 16 passed: exactly U4's tokens-unit discriminator. Before (b), before (c) and after (c) the worktree file was BYTE-EQUAL to blob `8e34539b:apps/ui/src/api/costMetric.ts`, sha256 prefix `476474f0de48b184`.
- G10 EXIT 0 ×4, serially in the primary checkout at C4: `tests/ui_server/` 455 passed, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21, `tests/orchestration/test_integrity_gate.py` 16 — 544 in total, equal to the reviewer's base reading.
- G11 EXIT 0 — `python3 -m pytest tests/ui_contracts/ -q`: 495 passed, 4 skipped, equal to the base reading; the two repo-wide sweeps take the new module in and stay green.
- G12 EXIT 0 — `python3 -m pytest tests/cli/test_golden_path.py -q`: 42 passed, equal to the base reading.
- G13 EXIT 0 — six commits before C5, every one single-parent; insertions 362, 240, 18, 4, 18 and 432, each under the 500 cap; the range path set equals the block's Change set minus `.agent/handoff.md`, the difference EMPTY in BOTH directions; `git show --numstat` agrees cell by cell with the tables above; lines BEGINNING `<<<SLICE ` or `<<<END ` count 0 in all three slice targets (6 each in the two block carriers, by construction); `git ls-files .remedy-wt` 0; one worktree; the six round reflog rows all carry operation `commit`, so amend 0, rebase 0, cherry 0.
- G14 EXIT 0 — `gh pr list --state open --json number,headRefName` printed verbatim: `[]`.
- G15 CHECKED, re-measured at C4 — branch point `c34ef32b` is the merge commit of PR #211; the vitest config still reads `environment: "node"` with `include: ["src/**/*.test.ts"]`; no `warn` token in `apps/ui/src/styles/tokens.css` or `globals.css`; R-0495 and R-0574 are both still on record; the `BUDGET_TICK_EVENT` comment R-0670 describes is unchanged in `packages/orchestration/ui_server.py`; `RemedyMetric.value` is still `number | "—"`; `costMetric.ts` carries NO import statement at all; `TopMetricsBar.tsx` still holds its private `formatTokens`; there is no `@types/node` in this workspace. Two residuals and one carried sentence are named under Deviations; no slice was edited.

## Authored-text proofs
All three slices were extracted PROGRAMMATICALLY by marker line out of the committed C0a blob `bc1a9f5b`; none was retyped, rewrapped or reflowed.
- PLANF022R7 → `.agent/plan.md` at `a6ec63ab`: byte-equal to the slice plus one newline, 2418 against the bare slice's 2417; the bare-slice control is FALSE.
- LEDGER7 → `.agent/live_review.md` at `fd530b7c`: the round-base blob is a byte-exact prefix, remainder 8875 = 1 + 8873 + 1; the independent paragraph reader goes 256→258 with both slice paragraphs equal in order.
- DEC4 → `.agent/decisions.md` at `c6b026bf`: prefix holds, remainder 5128 = 1 + 5126 + 1; the paragraph reader goes 1278→1287 with all 9 slice paragraphs equal in order.

## Deviations & assumptions
- COMMIT SEQUENCE: no departure. C0a, C0b, C1, C2, C3, C4 and C5 landed in the block's order — seven commits, none added, none dropped, none reordered.
- DECLARED CONTRADICTION (constraint 1): DEC4's REVERSE clause names deleting `costMetric.ts` with its test file and narrowing `RemedyMetricKey` back to seven strings, but does not name removing `RemedyMetric.cost`, which C4 also adds. The slice was applied byte for byte and not repaired.
- DECLARED CONTRADICTION (constraint 1): DEC4's CONTEXT calls `RemedyMetricKey` a closed union of seven strings at `types.ts:3`; at C4 it holds eight members and sits at line 8. DEC4 scopes that sentence to `d97cdbb2` in its own opening words, so it reads as a base measurement rather than a stale claim; either way the slice was not edited.
- G9(a) PARTIAL, said plainly: the mutation reddened U3's fill/level/limitless case as ordered, but U3's SECOND case — the serialised-view assertion — stayed GREEN under it, because the borrowed denominator leaks into `fill` while both tooltip lines stay separately guarded and empty. The ordered shape (ii) is red and the file is red; the serialised-view case simply does not reach that leak. Reported rather than repaired — strengthening it would need a second C4.
- G15 RESIDUAL: PLANF022R7 states that `npm run lint` is red at base. The block's NOT A GATE paragraph forbids running it, so that sentence is CARRIED from the reviewer's base measurement rather than re-measured here.
- ASSUMPTION, U7's reader: `costMetric.test.ts` reaches `node:fs` and `node:url` through `await import(<variable>)` rather than a static specifier. There is no `@types/node` in this workspace and the static form fails `npm run typecheck` with TS2307 on both modules — measured — while G7 gates that command at exit 0. Same modules, same file read off disk, with the two function shapes declared locally.

## Next
R8 — T002's RENDER half: the COST metric in `TopMetricsBar.tsx`, its CSS tokens, the `remedyApi.ts` wiring and the shell seam that feeds it the live tick, plus the `tests/ui_contracts/` source guard. Before authoring it, Phase 1 rule 1: re-read `.agent/STOP` from disk, then the Open PR Gate.

# Handback — F022 Live cost ticker, Runde 10 (T003a, the live wiring)

Fortschritt: ~70 % (T001 fertig · T002 fertig · T003a diese Runde · T003b offen;
             diese Runde verdrahtet den Ticker zum ersten Mal live und schreibt
             das R9-Urteil auf Platte) — Schaetzung

Branch `feature/f022-live-cost-ticker`. Round base `a8952614`.

## Range
Review of a8952614..bcd4dd07 (C0a–C9) plus this handoff commit (C10).

## Commits
### d4fe3bf8 docs(state): save the F022 R10 step block as authored text
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f022-r10.md | +482/-0 | C0a, the block saved byte-for-byte |

### 793cd8d5 docs(state): mirror the F022 R10 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +402/-148 | C0b, same bytes, same git blob a763f93d |

### 63119805 docs(state): point the F022 plan at R10, the live wiring round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +22/-16 | C1, slice PLANF022R10 whole-file |

### 593c26c6 docs(state): repair the F022 round map to the built round sequence
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +10/-4 | C2, the one MAPFROM→MAPTO pair |

### 44063bf0 docs(state): record the F022 R9 PASS and the R-0644 recurrence
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | C3, LEDGER10's two paragraphs, appended |

### d8ca0f11 docs(state): rule DECISION F022 D6 on the live tick path
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +55/-0 | C4, slice DEC6, appended |

### 15e77d66 feat(ui): read the latest budget tick out of one stream frame
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/budgetTick.ts | +41/-0 | C5, `budgetTickFiguresOf`, type-only imports |
| apps/ui/src/api/budgetTick.test.ts | +51/-0 | C5, 6 tests incl. every malformed envelope |

### ec1d0785 feat(ui): hold the latest budget tick on the stream state and its view
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/brainStream.ts | +17/-3 | C6, `budget` field, fold behind the replay guard |
| apps/ui/src/api/brainStream.test.ts | +52/-0 | C6, 6 cases incl. carry-forward by reference |
| apps/ui/src/api/brainStreamRunner.ts | +11/-1 | C6, `budget` on the view, seeded and `===`-compared |
| apps/ui/src/api/brainStreamRunner.test.ts | +71/-0 | C6, 6 cases incl. the replay publishing nothing |

### aa052495 feat(ui): compose the bar's cost tile from the latest tick
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/costTicker.ts | +35/-0 | C7, `metricsWithCostTicker`, calls `costMetricOf` |
| apps/ui/src/api/costTicker.test.ts | +64/-0 | C7, 6 cases incl. both by-reference returns |
| apps/ui/src/api/remedyApi.ts | +11/-0 | C7, eighth `cost` entry + the degraded-path absence |
| apps/ui/src/api/remedyApi.test.ts | +18/-3 | C7, the order guard's name and assertions moved together |

### 48f63b1e feat(ui): wire the live cost tile through the shell and pin the path
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/shell/RemedyShell.tsx | +2/-1 | C8, the bar's only prop change |
| tests/ui_contracts/test_cost_metric_render.py | +69/-0 | C8, `TestTheLiveTickReachesTheBar`, 4 tests |

### bcd4dd07 test(ui): pin a negative spend as the limitless cost view
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/costMetric.test.ts | +12/-0 | C9, R-0671's one missing assertion |

### C10 (this commit) — `.agent/handoff.md`, rewritten whole. A handoff cannot table the commit that writes it (R-0149).

## External actions
- `git worktree add .remedy-wt/r10-ctl bcd4dd07 --detach` → G6 negative control; `git worktree remove --force` → removed.
- `git worktree add .remedy-wt/r10-red bcd4dd07 --detach` → red control for C8's new contract; removed the same way.
- `gh pr list --state open --json number,headRefName` → `[]` verbatim.
- `git push` → see Next. No PR created, nothing merged (G15).

## Verification
Every gate run by me; every exit code real. Transcripts are in the round report, not here (R-0582).
- G1 exit 0 — `.agent/STOP` absent before C0a and before C10; branch `feature/f022-live-cost-ticker`; `git status --porcelain` 0 lines after each of C0a..C9.
- G2 exit 0 — one sha256 `49f733db…b566c23`, 38270 bytes, 482 lines across all FIVE readings (reviewer file, C0a blob, C0b blob, `last_block.md` on disk, `authored/f022-r10.md` on disk); C0a and C0b resolve to the same blob `a763f93d`; the delegation's digest agrees.
- G3 exit 0 — the extractor over the committed C0a blob printed 5 slices over 121 CONTENT lines, TOTAL 482, PROSE 361. Constraint 10's three numerals reproduce exactly.
- G4 exit 0 — `.agent/plan.md` at C1 is 2727 bytes = PLANF022R10's 2726 + one newline; NEGATIVE CONTROL against the bare slice is False; `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 48 ≤ 50.
- G5 exit 0 — containment printed `TO contains FROM: false`, matching the convention block. In `.agent/live_review.md`: MAPFROM 1 at base → 0 at C2; MAPTO 0 → 1; bytes 535681 → 536120, delta 439 = len(MAPTO) 810 − len(MAPFROM) 371; `^## Steps$` 1 at C2.
- G6 exit 0 — C3: prefix exact, remainder 6606 = 1 + LEDGER10's 6604 + 1; reader (b) counted N=2 paragraphs, 265→267 units, last 2 equal in order. C4: prefix exact, remainder 3564 = 1 + DEC6's 3562 + 1; N=6, 1297→1303 units, last 6 equal in order. NEGATIVE CONTROL in `.remedy-wt/r10-ctl`: one byte flipped at BYTE offset 536161 in LEDGER10's first paragraph (`WER-AUTHORED SLICE S` → `WER-AUTHOReD SLICE S`) and at BYTE offset 541142 in DEC6's first (`the live tick is hel` → `the live tIck is hel`) — both readers rejected both mutants and accepted both true files. Worktree removed; `git worktree list` 1 line.
- G7 exit 0 — `.agent/live_review.md`, base vs C3: lines matching `^- R-\d+ — ` 234 → 234, all DISTINCT at both, max id `R-0673` at both, ids ADDED the EMPTY SET and ids REMOVED the EMPTY SET, so NO ID WAS MINTED. `^Done: R-` 1 → 1 over the single id `R-0653`; `^Landed: ` 0 → 0; `^Recurrence: R-` 3 → 4, gaining `R-0644` over ids {R-0445, R-0645, R-0672} → {R-0445, R-0644, R-0645, R-0672}; `^Gate: R` 9 → 10 over 9 → 10 distinct keys, gaining `R9`. `^- R-0644 — ` is exactly 1 at both, so the recurrence APPENDED and rewrote nothing. Every base numeral the block quoted reproduced.
- G8 exit 0 — `^## DECISION F022 D6 ` in `.agent/decisions.md`: 1 at C4, 0 at the round base.
- G9 exit 0 — `npm run typecheck` in `apps/ui`, no output, matching the base reference.
- G10 exit 0 — `npm run test:unit` in `apps/ui`: 19 files, 268 tests. Base reference 17 files / 241 tests, so +2 files and +27 tests, accounted for in full: `budgetTick.test.ts` NEW +6 (C5); `costTicker.test.ts` NEW +6 (C7); `brainStream.test.ts` 25→31 (+6, C6); `brainStreamRunner.test.ts` 20→26 (+6, C6); `remedyApi.test.ts` 46→48 (+2, C7 — one renamed guard plus two new); `costMetric.test.ts` 23→24 (+1, C9). 6+6+6+6+2+1 = 27.
- G11 exit 0 — `python3 -m pytest tests/ui_contracts/ -q` run FROM THE REPOSITORY ROOT `/home/decodeux/Repos/remedy`: 518 passed, 4 skipped. Base reference 514 passed / 4 skipped; the +4 are C8's `TestTheLiveTickReachesTheBar`.
- G12 exit 0 — the "single arithmetic home" clause run at the BASE FIRST: over 58 non-test `.ts`/`.tsx` under `apps/ui/src` with comments stripped, the files naming any of `spent_usd`, `spent_tokens`, `limit_usd`, `limit_tokens` are exactly `apps/ui/src/api/costMetric.ts` — SATISFIED at the base, so nothing was removed to meet it. At C8 `48f63b1e`, over 60 such files, the answer is the same single file. Both readings agree with the reviewer's. Red control in `.remedy-wt/r10-red`: adding one `f.spent_usd / f.limit_usd` line to `costTicker.ts` and reverting the shell prop took 3 of the 4 new tests red while the other 20 stayed green.
- G13 exit 0 — all 11 commits before C10 single-parent; insertions 482, 402, 22, 10, 4, 55, 92, 151, 128, 71, 12 (total 1429), each under the 500 cap; the range path set matches the Change set with the difference EMPTY in BOTH directions (`.agent/handoff.md` excluded, it is C10's); `git show --numstat` agrees cell by cell with every `## Commits` row above; `^<<<SLICE ` and `^<<<END ` count 0 in `.agent/plan.md`, `.agent/live_review.md` and `.agent/decisions.md`; `git ls-files .remedy-wt` 0; one worktree; the round's 11 reflog rows carry amend 0, rebase 0, cherry 0.
- G14 exit 0 — serially in the primary checkout at C9: `tests/ui_server/` 455, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21, `tests/orchestration/test_integrity_gate.py` 16 — 544 across the four; canary `tests/cli/test_golden_path.py` 42. Both match the base reference. No two pytest processes ran at once.
- G15 exit 0 — `gh pr list --state open --json number,headRefName` printed `[]`. No PR created, nothing merged.
- G16 exit 0 — checked, and NO RESIDUAL. Re-measured at C4: merge base with `main` is `c34ef32b`, whose subject is the PR #211 merge; `ui_server.py` holds 0 endpoint literals containing `stats`; `R-0644`, `R-0665`, `R-0670`, `R-0671`, `R-0672`, `R-0673` each occur exactly once as a `^- R-\d+ — ` record; `R-0673` first appears as a record at `5f8cb0cc` and 0 times at its parent; `TopMetricsBar.tsx` lines 27–31 at `142af5e4` are the whole of `formatTokens` and hold exactly 2 `/` characters, so LEDGER10's correction is right; `.agent/authored/f022-r9.md` is sha256 `6ffeb77f…6dc6ac` over 24266 bytes and 228 lines as claimed; `e5c86774..a8952614` is 5 commits with insertions 228, 124, 11, 6, 42; the `.agent/last_block.md` numstat row at `761bf4b1` is `+124/-278`; R9's handback is 73 lines. Every file-fact those slices state re-measures TRUE.
- NOT A GATE, measured only because C1's risk sentence states it: `npm run lint` in `apps/ui` is RED at HEAD with 78 problems (76 errors, 2 warnings), all of them `Parsing error` from a config that cannot parse TypeScript at all. The block states 72 at the base. Both readings are reported and NOTHING is reconciled (constraint 9); the sentence's claim — that lint is red and routes to a paydown branch as R-0622 — holds under my measurement.

## Authored-text proofs
Five slices, all extracted PROGRAMMATICALLY by marker line from the committed C0a blob `d4fe3bf8`, none retyped:
- PLANF022R10 2726 bytes / 48 content lines → `.agent/plan.md` at C1, byte-equal plus one newline (G4).
- MAPFROM 371 / 5 and MAPTO 810 / 11 → the one pair at C2, applied whole (G5).
- LEDGER10 6604 / 3 → appended at C3, both readers (G6).
- DEC6 3562 / 54 → appended at C4, both readers (G6).
`.agent/authored/f022-r10.md`, `.agent/last_block.md` and the reviewer's `.remedy-wt/f022-r10.md` are byte-identical (G2), so the disk-to-disk comparison the fidelity protocol asks for held in its strongest form.

## Deviations & assumptions
- DECISION D15 stated cause: this handback is 136 lines, over the 100 the block sets for this commit count. The overage is mandated content — 12 per-commit changed-files tables for a 12-commit bundle, 16 one-line gate results several of which must carry base-vs-measured pairs, the item-status table's 12 rows, and the authored-text proof list. No section was dropped and no transcript is included.
- NO DEPARTURE from the block's ordered commit sequence: C0a, C0b, C1, C2, C3, C4, C5, C6, C7, C8, C9, C10 were committed in exactly that order, none added, none dropped, none merged.
- NO SLICE WAS EDITED, and I found NO contradiction between a slice and anything I measured — LEDGER10's corrected division count of TWO is what I re-measure at `142af5e4` (G16), and every base numeral the block quoted for G7, G10, G11, G14 reproduced.
- Two deliberate absences, both licensed by the block: `packages/orchestration/ui_server.py` was not touched, so R-0670 is NOT repaired here (constraint 7); no `.module.css` was touched and no visual token was added (constraint 5).
- Assumption, declared: the degraded path (`normalizeApiFailure`) gains no cost tile, per the block's own reading. `metricsWithCostTicker` returns a metrics array with no `cost` entry unchanged AND by reference, and a comment in `normalizeApiFailure` records the absence where a reader would search for it.

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a save this block | done | |
| C0b mirror into last_block | done | |
| C1 the plan | done | |
| C2 repair the round map | done | |
| C3 the R9 verdict and the R-0644 recurrence | done | |
| C4 DECISION F022 D6 | done | |
| C5 the tick reader | done | |
| C6 the stream state and the runner view | done | |
| C7 the metric composition and the dashboard's cost tile | done | |
| C8 the shell wiring and its source contract | done | |
| C9 the R-0671 assertion | done | |
| C10 the handback | done | this commit |

## Next
R11 — T003b, the terminal reconciliation and the delta labelling. It must open by ruling a DECISION on the SOURCE of the ledger's final figure: the feature file names "the stats endpoint" and no such endpoint exists among the job endpoints `packages/orchestration/ui_server.py` dispatches (0 endpoint literals containing `stats`, measured at C4), so R11 cannot build against that name until it rules one. Before anything else that round, re-read `.agent/STOP` from disk (Phase 1 rule 1) and only then the Open PR Gate (rule 2).

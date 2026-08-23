# Handback — F022 Live cost ticker · Runde 8 (T002b)

Fortschritt: ~55 % (T001 fertig · T002 fertig nach dieser Runde · T003 offen;
             der COST-Wert wird ab hier wirklich gezeichnet, mit Fuellung,
             Schwelle und Schaetzmarke) — Schaetzung

## Range
Review of 142af5e4..HEAD — eight commits, C0a C0b C1 C2 C3 C4 C5 C6, in the block's order. Branch `feature/f022-live-cost-ticker`, round base `142af5e4`. Open set after C2: 233 records, maximum `R-0672`, two High carried forward (R-0495, R-0574), both inherited from closed features.

## Commits
### b88f3553 docs(state): save the F022 R8 step block as authored text
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f022-r8.md | +382/-0 | C0a — the block verbatim, 42013 bytes / 382 lines |

### d92cdf92 docs(state): mirror the F022 R8 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +245/-225 | C0b — written from the committed C0a blob `9d573bbd` |

### 8051fd56 docs(state): point the F022 plan at R8
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +17/-18 | C1 — slice PLANF022R8, whole-text replacement |

### 6034b603 docs(state): record the F022 R7 verdict, resolve R-0653 and register two findings
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +8/-0 | C2 — slice LEDGER8: `Done: R-0653`, R-0671, R-0672 and `Gate: R7` in ONE commit |

### 4d2681c4 docs(state): rule the F022 cost render as DECISION F022 D5
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +20/-0 | C3 — slice DEC5, appended |

### 4d728bf2 test(ui): pin the cost view with fixture-stream goldens
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/costMetric.test.ts | +91/-0 | C4 — GO1 tick stream, GO2 four hand-written goldens, GO3 coverage; no production byte |

### 68cf3c16 feat(ui): draw the COST metric with its coin, marker, track and threshold
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/icons/RemedyGlyphs.tsx | +13/-0 | C5 — `CoinGlyph`, the coin `assets_spec.md` line 179 already specifies |
| apps/ui/src/components/metrics/TopMetricsBar.module.css | +45/-0 | C5 — the cost track, its two banded patterns, the marker and the tooltip rows |
| apps/ui/src/components/metrics/TopMetricsBar.tsx | +57/-13 | C5 — cost arm, estimate marker, fill track, tooltip, accessible name |
| tests/ui_contracts/test_cost_metric_render.py | +270/-0 | C5 — P1–P8, 19 tests over comment-stripped source |

### C6 docs(state): hand back the F022 R8 render round
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C6 — this file; a handoff cannot table its own commit (R-0149) |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a save this block | done | |
| C0b mirror it into last_block | done | |
| C1 the plan | done | |
| C2 the R7 verdict, one resolution and two findings | done | |
| C3 DECISION F022 D5 | done | |
| C4 the fixture-stream goldens | done | |
| C5 the render and its source contract | deviated | `formatTokens` also removed from the component — P6 cannot pass while it stands; see Deviations |
| C6 the handback | done | |

## External actions
- `git worktree add .remedy-wt/r8g5 68cf3c16` then `git worktree remove` (G5 controls), and `git worktree add .remedy-wt/r8g9 68cf3c16` then `git worktree remove` (G9 red proofs) — both removed, `git worktree list` back to one line.
- `gh pr list --state open --json number,headRefName` → `[]`. No PR created, nothing merged.
- `git push` on `feature/f022-live-cost-ticker` after C6 — the only remote write this round.

## Verification
- G1 EXIT 0 — `.agent/STOP` absent, read from disk before C0a and again before C6; branch `feature/f022-live-cost-ticker`; `git status --porcelain` 0 lines after every one of C0a, C0b, C1, C2, C3, C4 and C5.
- G2 EXIT 0 — `.remedy-wt/f022-r8.md`, the committed C0a blob, the committed C0b blob and `.agent/last_block.md` on disk are ALL sha256 `a077de71476f731f7d7c857916269e002d2e66dcc3e29bfe7f9850fdefdb278d` over 42013 bytes and 382 lines, and the digest the delegation names is the fifth reading and agrees; C0a and C0b are the SAME git blob `9d573bbd`.
- G3 EXIT 0 — the extractor over the committed C0a blob printed 3 slices (PLANF022R8, LEDGER8, DEC5) over 69 CONTENT lines; TOTAL re-measures at 382 and PROSE at 313 as TOTAL − CONTENT, so constraint 10's three numerals reproduce exactly.
- G4 EXIT 0 — `.agent/plan.md` at `8051fd56` is byte-equal to PLANF022R8 plus exactly one newline, 2297 bytes against the bare slice's 2296; the bare-slice control is FALSE; `^## Goal$` 1, `^## Next Steps$` 1, 43 lines against the cap of 50.
- G5 EXIT 0 — C2: the round-base blob is a byte-exact PREFIX, remainder 12211 = 1 + 12209 + 1, independent blank-line splitter 258→262 with ALL FOUR LEDGER8 paragraphs equal IN ORDER. C3: prefix holds, remainder 6761 = 1 + 6759 + 1, splitter 1287→1297 with all ten DEC5 paragraphs equal in order, `^## DECISION F022 D5 ` counts 1. Controls in `.remedy-wt/r8g5`: byte 513657 `D`→`E` and byte 525865 `.`→`/` (C2), byte 534341 `#`→`$` and byte 541099 `.`→`/` (C3) — both readers rejected all four mutants and accepted the true file.
- G6 EXIT 0 — base `142af5e4`: 231 records, all DISTINCT, maximum `R-0670`, `^Done: R-` 0, `^Landed: ` 0, `^Gate: R` 7 over 7 distinct keys. C2: 233 records, all DISTINCT, maximum `R-0672`, `^Done: R-` 1 with distinct ids {R-0653}, `^Landed: ` 0, `^Gate: R` 8 over 8 distinct keys. ids ADDED {R-0671, R-0672}, ids REMOVED the EMPTY SET; `^- R-0653 — ` still occurs exactly once; `^## Steps$` 1; the map paragraph is byte-identical at base and at C2 (1074 bytes).
- G7 EXIT 0 — `npm run typecheck` from `apps/ui` at C5, no output, agreeing with the reviewer's base reading.
- G8 EXIT 0 — `npm run test:unit` from `apps/ui` at C5: 17 test files and 241 tests passed against the base's 17 and 235, so the file count holds and the test count rises by 6, every one of them C4's in `costMetric.test.ts` (17→23 tests in that file).
- G9 EXIT 1 on every mutant, all three in `.remedy-wt/r8g9`; the unmutated worktree ran 19 passed and the unmutated scoped vitest 23 passed first. (a) the fill track rendered unconditionally with the `m.cost.fill !== null` guard dropped → 1 failed / 18 passed, `TestNoFakeDenominatorAtTheRenderLayer::test_the_track_is_guarded_on_a_real_fill`, which is P4. (b) the marker driven from `level === "warn"` instead of `estimated` → 2 failed / 17 passed, `TestTheMarkerIsTheBasisNotTheThreshold::test_the_marker_is_named_once_and_rendered_off_estimated` and `::test_no_expression_joins_the_marker_to_a_level`, which is P3 entire. (c) one figure in one golden, the warn entry's `fill: 0.85`→`0.84`, run as `npx vitest run src/api/costMetric.test.ts --root <wt>/apps/ui --config <primary>/apps/ui/vitest.config.ts` from the primary `apps/ui` → 1 failed / 22 passed, naming the entry `tick 1 renders $3.40 at level warn`, which is GO2. No mutation left the suite green; before each next mutation the worktree file was BYTE-EQUAL to its committed blob at `68cf3c16`.
- G10 EXIT 0 ×4, serially in the primary checkout at C5: `tests/ui_server/` 455 passed, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21, `tests/orchestration/test_integrity_gate.py` 16 — 544 in total, equal to the reviewer's base reading.
- G11 EXIT 0 — `python3 -m pytest tests/ui_contracts/ -q`: 514 passed and 4 skipped against the base's 495 and 4, a difference of exactly +19, which is C5's new file entire; both repo-wide sweeps read the edited component and stay green.
- G12 EXIT 0 — `python3 -m pytest tests/cli/test_golden_path.py -q`: 42 passed, equal to the base reading.
- G13 EXIT 0 — seven commits before C6, every one single-parent; insertions 382, 245, 17, 8, 20, 91 and 385, each under the 500 cap; the range path set is the block's Change set minus `.agent/handoff.md`, the difference EMPTY in both directions otherwise; `git show --numstat` agrees cell by cell with the tables above; lines BEGINNING `<<<SLICE ` or `<<<END ` count 0 in all three slice targets; `git ls-files .remedy-wt` 0; one worktree; `git status --porcelain` 0; the seven round reflog rows all carry operation `commit`, so 0 amend, 0 rebase and 0 cherry.
- G14 EXIT 0 — `gh pr list --state open --json number,headRefName` printed verbatim: `[]`. No PR created, nothing merged.
- G15 CHECKED, re-measured at C5 — branch point `c34ef32b` is still the merge base with `main`; the vitest config still reads `include: ["src/**/*.test.ts"]`; no tracked path contains `assumption` and `assumption_log` is still named by 76 docs; `usableFigure`'s quoted clause, U6's `{ spent_usd: -1, limit_usd: 4 }` case, `types.ts`'s type-only import and its optional `cost` field all read exactly as C2 states, and `costMetric.ts` is untouched by this round; each of the seven tokens constraint 9 names is defined exactly once in BOTH sheets; `assets_spec.md` line 179 is still the coin row; `ux_spec.md` §10 still carries both the 4-segment opening and the 6px/radius-3/`--remedy-blue-100`/350ms track; `.progressTrack` is still 5px over `rgba(76, 131, 255, 0.16)` at 600ms; `remedyApi.ts` is untouched and still builds seven metrics. One residual and one carried sentence are named below; no slice was edited.

## Authored-text proofs
- PLANF022R8 → `.agent/plan.md` at `8051fd56`: extracted PROGRAMMATICALLY by marker line out of the committed C0a blob `9d573bbd`, never retyped, rewrapped or reflowed; byte-equal to the slice plus one newline, 2297 against the bare slice's 2296, with the bare-slice control FALSE.
- LEDGER8 → `.agent/live_review.md` at `6034b603`: same extraction; the round-base blob is a byte-exact prefix and the remainder is 12211 = 1 + 12209 + 1; the independent paragraph reader goes 258→262 with all four slice paragraphs equal in order.
- DEC5 → `.agent/decisions.md` at `4d2681c4`: same extraction; prefix holds and the remainder is 6761 = 1 + 6759 + 1; the paragraph reader goes 1287→1297 with all ten slice paragraphs equal in order.

## Deviations & assumptions
- COMMIT SEQUENCE: no departure. C0a, C0b, C1, C2, C3, C4, C5 and C6 landed in the block's order — eight commits, none added, none dropped, none reordered.
- DEVIATION FROM C5's "gains, and nothing more" LIST, AND THE CONTRADICTION IT EXPOSES (constraint 1): `TopMetricsBar.tsx` also LOST its private `formatTokens` and now imports `formatTokenCount` from `costMetric.ts` — P6 forbids any `/` outside a JSX tag or a string over the comment-stripped `.tsx`, `formatTokens` divides three times, so the ordered guard cannot pass while it stands, and `costMetric.ts`'s own comment already names R8 as the round that removes it; the two are the same algorithm, so the tokens metric's rendered output is unchanged, which is what constraint 6 asks for. DEC5's REVERSE clause then calls its four-item list "the whole of this round's production surface" WITHOUT naming that removal, so a reversal performed exactly as written leaves the component importing a formatter from a module D4's own reversal deletes, with no local replacement — the R-0672 shape recurring inside the clause R-0672 was raised about. The slice was applied byte for byte and NOT repaired.
- G15 CARRIED SENTENCE: PLANF022R8 states that `npm run lint` is RED at base. The block's NOT A GATE paragraph forbids running it, so that one sentence is carried from the reviewer's base measurement rather than re-measured here. Every other file fact C1 through C5 land was re-measured at C5 and holds.
- AS THE BLOCK ORDERS IT SAID: `.costTrack` and `.progressTrack` now DIFFER on disk — 6px, radius 3, `--remedy-blue-100`, 350ms against 5px, `rgba(76, 131, 255, 0.16)`, 600ms. `ux_spec.md` §10 specifies the first; `.progressTrack` predates that sentence and MetricsBar's other metrics are on this feature's Do-not-touch list, so the older rule was left exactly as it was (DECISION F022 D5 clause 5).

## Next
R9 — T003: the terminal reconciliation with its delta label, the live wiring through `remedyApi.ts` and `RemedyShell.tsx`, and the fake-job end-to-end. Before authoring it, Phase 1 rule 1: re-read `.agent/STOP` from disk, then the Open PR Gate.

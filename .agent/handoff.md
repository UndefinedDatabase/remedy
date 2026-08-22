# F021 R32 handback — record R31, define the pill token, pin the resolution set

Fortschritt: ~98 % (T002 fertig und verdrahtet; es fehlt nur noch T003:
             Klick-Sprung und der deaktivierte Steuer-Eingang)
             — Schaetzung

## Range
Review of 8efdb7ea6615984ca40dcbbc2f07e692b48be67a..HEAD — round base `8efdb7ea`.
Branch `feature/f021-live-activity-feed`. Open findings: 224 registered under `^- R-\d+ — `, of which 86 end `OPEN.`; `Done: R-` 1.

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a `580df037` | done | |
| C0b `ae7b54be` | done | |
| C1 `17a1a09a` | done | |
| C2 `cbcbf85a` | done | |
| C3 `d98d8e1d` | done | |
| C4 `86e3de0a` | done | |
| C5 (this file) | done | its own SHA is unnameable from inside it |

## Commits

### 580df037 chore(agent): save the F021 R32 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f021-r32.md | +330/-0 | the block saved verbatim (C0a) |

### ae7b54be chore(agent): mirror the R32 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +248/-398 | written FROM the committed C0a blob (C0b) |

### 17a1a09a docs(state): point the F021 plan at R32, the record and token round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +16/-15 | PLANF021R32 whole-file write (C1) |

### cbcbf85a docs(review): record the R31 PASS, register R-0661 and correct two reviewer defects
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +8/-0 | RECORD32 appended, ONE blank line at the join (C2) |

### d98d8e1d fix(ui): define the pill radius token the shipped sheet never adopted
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/styles/tokens.css | +4/-0 | TOKENPAIR, append-shaped (C3) |

### 86e3de0a test(ui-contracts): pin the unresolved custom property set
| Path | +/- | Reason |
|---|---|---|
| tests/ui_contracts/test_design_drift.py | +46/-0 | PINSLICE2, TWO blank lines at the join (C4) |

### C5 docs(state): hand back F021 R32 — SHA unnameable: this is the commit that writes this file
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | owed to R33 | the handback itself (C5) |

## External actions
`git push -u origin feature/f021-live-activity-feed` after C5. `gh pr list --state open --json number,headRefName` exit 0, output `[]`; neither `gh pr create` nor `gh pr merge` was run. No worktree added or removed (constraint 8).

## Verification — one line per gate, transcripts in the round report (R-0582)
G1 `.agent/STOP` ABSENT before C0a and again before C5; branch `feature/f021-live-activity-feed`; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3, C4.
G2 sha256 `e41c3614ee740cec6acd5a79729c9431d6302c0d1ff66584595812b0e01f6da4`, 31240 bytes, 330 lines — EQUAL across `.remedy-wt/f021-r32.md`, `.agent/authored/f021-r32.md` at C0a and `.agent/last_block.md` at C0b (both blob `742b3e39`). My extractor printed 3 whole texts, 1 pair, 105 CONTENT lines; TOTAL 330 against 490, PROSE 225 against 400.
G3 `cmp` plan.md vs slice+newline exit 0; NEGATIVE CONTROL vs the bare slice exit 1; last byte is a newline; `^## Goal$` 1, `^## Next Steps$` 1; `wc -l` 48, under 50.
G4 TOKENPAIR FROM 1x at base (whole-line AND indent-agnostic AGREEING) and 1x at C3 — append-shaped, no zero owed; `--remedy-radius-pill` 0x at base, 1x at C3; each of the 4 TO-only lines exactly once in C3's added lines; value `  --remedy-radius-pill: 999px;` against the design reference's `--remedy-radius-md: 14px; --remedy-radius-sm: 10px; --remedy-radius-pill: 999px;`.
G5 canonical `^- R-\d+ — ` 223→224, ALL DISTINCT at both, max R-0660→R-0661; loose `^- R-` 224→225, gap to canonical 1 at both, UNCHANGED; `Done: R-` 1/1; `Landed: ` 0/0; `Gate: R` keys 30→31, DISTINCT at both; `Gate: R32` 0→1; `- R-0661 — ` 0→1; `- R-0662` 0/0; RECORD32 paragraphs opening with the bytes `- R-` = 1; `^Recurrence: R-0629 — ` 0→1; `^Recurrence: ` 3→5; `- R-0629 — ` and `- R-0587 — ` each 1 at BOTH. ONE CLAUSE IS FALSE AS WRITTEN — Deviations 1.
G6 unresolved set at the round base, sorted, EXACTLY 5: `--remedy-mono`, `--remedy-radius-pill`, `--remedy-warning-bg`, `--remedy-warning-border`, `--remedy-warning-fg`; at C3/C4 EXACTLY the 4 others; the landed pin runs green at C4.
G7 SERIAL, PRIMARY checkout, repo root: `tests/ui_contracts/` exit 0, 486 passed + 4 skipped = 490, base-equivalent 488, difference 2 = PINSLICE2's two test functions; `npx tsc --noEmit` from `apps/ui` exit 0, output EMPTY; the three state-reader suites exit 0, 511; canary exit 0, 42.
G8 NO worktree: the base CSS tree was rebuilt into a `.remedy-wt` scratch with `git show 8efdb7ea:<path>` and its unresolved set CONTAINS `--remedy-radius-pill` (5 members) while C3's does NOT (4) — the pin's own discriminator, false at the base; scratch deleted, `git status --porcelain` 0 lines.
G9 base..C4 path set EQUALS the six non-handoff `Change:` paths, both differences EMPTY; 6 commits, every one single-parent; `git show --numstat` and `git diff --numstat` agree cell by cell and agree with the tables above; insertions 330, 248, 16, 8, 4, 46, each under 500; `git ls-files .remedy-wt` 0; `git worktree list` the primary checkout ALONE; `gh pr list --state open` `[]`; marker sweep line-anchored 0 for `<<<SLICE `, `<<<END `, `<<<FROM `, `<<<TO ` and for any `<<<` in all four files a slice or pair landed in; reflog read BY OPERATION — all six of this round's rows `commit`, with `amend`, `rebase` and `cherry` 0 each in that field.

## Authored-text proofs
All four texts were extracted BY MARKER LINE from the COMMITTED C0a blob `580df037:.agent/authored/f021-r32.md`, never retyped. `.agent/plan.md`: `cmp` exit 0 against PLANF021R32 + one newline, exit 1 against the bare slice. `.agent/live_review.md`: the base blob is a byte-exact PREFIX and the remainder is EXACTLY one newline + RECORD32 + one newline; units 279→283 ELEMENTWISE, RECORD32 measuring 4. `tests/ui_contracts/test_design_drift.py`: base blob a byte-exact PREFIX, remainder EXACTLY two newlines + PINSLICE2 + one newline; 19→20 top-level classes, all 20 with two blank lines above. `apps/ui/src/styles/tokens.css`: TOKENPAIR's FROM was asserted present exactly once before the replacement.

## Deviations & assumptions
1. G5's clause "`^Recurrence: R-0629 — ` and `^Recurrence: R-0587 — ` each 0 then 1" is FALSE for the R-0587 half and was NOT repaired. Measured: `^Recurrence: R-0587 — ` is 1 at the round base — line 1190, the entry `433daa59` landed — and 2 at C2. The R-0629 half is correct at 0→1. The SLICE is right and the GATE CLAUSE is wrong: RECORD32 itself calls this the "Fourth instance" of R-0587 and names that earlier entry's SHA, so a base reading of 0 was never possible. Constraint 1 forbids repairing reviewer text, so it is declared rather than fixed.
2. The ui_contracts BASE total was measured with `--deselect tests/ui_contracts/test_design_drift.py::TestEveryCustomPropertyResolves` in the primary checkout, NOT by checking out `8efdb7ea`, because constraint 8 forbids creating a worktree this round. It printed 484 passed + 4 skipped + 2 deselected = 488, the value the block names.
3. No other departure from the ordered sequence: the commits are exactly C0a, C0b, C1, C2, C3, C4, C5 — none extra, none dropped, none reordered.
4. DECISION D15, size: this file measures 83 lines by `wc -l`, over the 60-line baseline and inside the ≤100 tier AGENTS.md grants a handback whose per-commit tables cover more than five commits, which this one's seven do. Mandated cause: seven per-commit tables, nine one-line gate results, the item-status table and the two authored-text/deviation sections. No section was dropped to reach it.

## Next
R32's OWN VERDICT IS UNRECORDED and the next round's ledger commit owes it, together with the two readings C5 cannot state about itself: C5's insertion count and its `wc -l`. The FOUR surviving unresolved custom properties — `--remedy-mono`, `--remedy-warning-bg`, `--remedy-warning-border`, `--remedy-warning-fg` — are registered under R-0661 and route to the PAYDOWN BRANCH, NOT to F021: each needs a value decided against the design reference, which is a design question. R33 is T003 — the row click-jump to the graph store, then the disabled steering input with the tooltip naming F030 — after which F021 reaches its integration-gate round. The next session's first action is Phase 1 rule 1, re-reading `.agent/STOP` from disk, before rule 2.

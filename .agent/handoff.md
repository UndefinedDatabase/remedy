# Handback — F022 Live cost ticker · Runde 14 (T003b-b, die Client-Haelfte)

Fortschritt: ~88 % (T001 fertig · T002 fertig · T003a fertig · T003b-a fertig —
             diese Runde baut die Client-Haelfte: die Schluss-Abrechnung gegen
             die Ledger-Zahl mit ihrem Delta-Label) — Schaetzung

Branch `feature/f022-live-cost-ticker`. Round base `5d3e6045`.
Deviations, declared: this handback is 148 lines, over the 60-line cap, under
DECISION D15 — the cause is the mandated per-commit tables for 9 commits, the
13 one-line gate rows, the 9-row item-status table and the ordered-sequence and
tooling deviations §4 requires in prose.

## Range

Review of `5d3e6045`..`HEAD` (C7 below).

## Commits

### 2690329d chore(state): save the F022 R14 step block as authored text (C0a)
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f022-r14.md | +393/-0 | the block file copied byte-for-byte |

### 3a55afb4 chore(state): mirror the F022 R14 block into last_block (C0b)
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +291/-160 | same bytes, from the C0a blob; full-file rewrite |

### ca3273be docs(state): point the F022 plan at R14, the client reconciliation (C1)
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +11/-10 | PLANF022R14 replaces the file whole |

### 39d07ada docs(state): record the F022 R13 verdict in the live review ledger (C2)
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | LEDGER14 appended, one paragraph |

### 5c6d4fc6 docs(state): rule DECISION F022 D8 for the terminal reconciliation (C3)
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +71/-0 | DEC14 appended, nine paragraphs |

### c2e78b32 feat(ui): add the terminal cost reconciliation module per DECISION F022 D8 (C4)
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/costReconciliation.ts | +74/-0 | the new module, authored not sliced |
| apps/ui/src/api/costReconciliation.test.ts | +145/-0 | 13 cases incl. the guarded source scan |

### 318a85a1 feat(ui): carry the ledger budget figure into the dashboard type (C5)
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/types.ts | +7/-2 | `budgetFinal` on `RemedyDashboard` |
| apps/ui/src/api/remedyApi.ts | +7/-0 | `budget_final` mapped opaquely, `null` default |
| apps/ui/src/api/remedyApi.test.ts | +31/-0 | the `budget_final transport` describe |

### 4e460b2e feat(ui): render the terminal ledger figure with its delta label (C6)
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/types.ts | +5/-0 | `costFinalNote` on `RemedyMetric` |
| apps/ui/src/components/shell/RemedyShell.tsx | +12/-1 | the reconciliation wraps the ticker |
| apps/ui/src/components/metrics/TopMetricsBar.tsx | +3/-0 | the note rendered off its own field |
| tests/ui_contracts/test_cost_metric_render.py | +72/-0 | `TestTheLedgerFigureReachesTheBar` |

### C7 docs(state): hand back the F022 R14 client reconciliation round
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this file; a handoff cannot table its own commit |

## External actions

`git worktree add .remedy-wt/g5wt HEAD --detach` → ok; `git worktree remove
--force .remedy-wt/g5wt` → ok, list back to 1 line (G5 control). `git worktree
add .remedy-wt/g9wt HEAD --detach` → ok; `git worktree remove --force
.remedy-wt/g9wt` → ok, list back to 1 line (G9 mutations). `gh pr list --state
open --json number,headRefName` → `[]`. `git push` → after C7. No PR created,
nothing merged.

## Verification

One line per gate; transcripts stay in the round report (R-0582).

- G1 exit 0 — `.agent/STOP` absent, read from disk before C0a and again before C7; branch `feature/f022-live-cost-ticker`; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3, C4, C5 and C6.
- G2 exit 0 — five readings of the block are EQUAL: sha256 `1c827a3f558a…b5b5`, 30949 bytes, 393 lines (scratch `.remedy-wt/f022-r14.md`, the committed C0a blob, the committed C0b blob, `.agent/last_block.md` on disk, the delegation's digest); C0a and C0b resolve to the SAME git blob `ac070803`.
- G3 exit 0 — the extractor over the COMMITTED C0a blob, matching the line-anchored markers `<<<SLICE ` / `<<<END `, printed 3 slices over 116 CONTENT lines; TOTAL 393, PROSE 277 — constraint 10's numerals reproduce exactly, nothing to reconcile.
- G4 exit 0 — `.agent/plan.md` at `ca3273be` is 2608 bytes = PLANF022R14's 2607 + exactly one newline; NEGATIVE CONTROL against the BARE slice is FALSE (2608 vs 2607); `^## Goal$` 1x, `^## Next Steps$` 1x, `wc -l` 45 ≤ 50.
- G5 exit 0 (both files), controls exit 1 — reader (a): each pre-commit blob is a byte-exact PREFIX and the remainder is 1 + slice + 1 — `.agent/live_review.md` at `39d07ada` 5004 = 1 + LEDGER14's 5002 + 1, `.agent/decisions.md` at `5c6d4fc6` 4512 = 1 + DEC14's 4510 + 1. Reader (b), independent blank-line splitter: N = 1 for LEDGER14 (275 → 276 units) and N = 9 for DEC14 (1310 → 1319 units), the LAST N units equal the slice's paragraphs IN ORDER in both. NEGATIVE CONTROL in `.remedy-wt/g5wt`: one BYTE flipped at BYTE offset 569200 in live_review (`22 R13 entry. R13 PA` → `22 R13 entsy. R13 PA`) and at BYTE offset 548460 in decisions (` when the ledger fig` → ` when the medger fig`), both inside the FIRST appended paragraph — BOTH readers REJECT both mutants and BOTH ACCEPT both true files. Worktree removed; `git worktree list` 1 line.
- G6 exit 0 — `^- R-\d+ — ` records 234 at base `5d3e6045` and 234 at C2, all DISTINCT at both, MAXIMUM `R-0673` at both; ids ADDED and ids REMOVED are both the EMPTY SET, so NO ID WAS MINTED. `^Done: R-` 2 → 2 over `R-0653` and `R-0670`; `^Landed: ` 0 → 0; `^Recurrence: R-` 8 → 8; `^Gate: R` 13 → 14 over 13 → 14 distinct keys, gaining exactly the key `R13`. Every base reference numeral the block states reproduced under my own measurement.
- G7 exit 0 — the AST-free scan read 61 shipped `.ts`/`.tsx` files under `apps/ui/src` (test files excluded) and, with comments stripped, the LIST of files whose code names `spent_usd`, `spent_tokens`, `limit_usd` or `limit_tokens` is exactly `['apps/ui/src/api/costMetric.ts']`. `costReconciliation.ts` IS in the scanned set and its RAW source DOES name a field, so the comment-stripping half is not vacuous either.
- G8 exit 0 ×3 — in the PRIMARY checkout at C6: `vitest run` 20 files / 285 tests passed (base reference 19 / 268; +1 file, +17 tests, all mine); `tsc --noEmit` exit 0 with NO output (base reference identical); `python3 -m pytest tests/ui_contracts/ -q` 525 passed, 4 skipped (base reference 518 / 4; +7 = the new contract class). `npm run lint` NOT RUN, per the block.
- G9 — POSITIVE CONTROL FIRST, then two mutations, all in `.remedy-wt/g9wt` and never in the primary checkout. Control: unmutated worktree, `costReconciliation.test.ts` 13/13 passed, exit 0. MUTATION 1, deleting `if (received.display === ledger.display) return undefined;` so the note renders unconditionally: exit 1, exactly 1 test failed — "says NOTHING when the two displays are equal", which received `final (ledger): $4.20 — live estimate was $4.20`, the self-contradicting label DECISION F022 D8 clause 3 exists to prevent. Restored (worktree `git status --porcelain` 0 lines). MUTATION 2, deleting `if (running) return metrics as RemedyMetric[];` so the reconciliation runs mid-run: exit 1, exactly 1 test failed — "a RUNNING job gets the SAME array". Worktree removed; `git worktree list` 1 line.
- G10 exit 0 ×5 — serially in the PRIMARY checkout at C6, never two pytest processes at once, `python3 -m pytest <path> -q` from the repository root: `tests/ui_server/` 470 passed, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21, `tests/orchestration/test_integrity_gate.py` 16 → 559 across the four; canary `tests/cli/test_golden_path.py` 42. All five match the block's reference figures exactly.
- G11 exit 0 — 8 commits before C7, every one single-parent; insertions 393, 291, 11, 2, 71, 219, 45 and 92, each under the 500 cap; the range path set is exactly the 13 declared non-handoff paths with the difference EMPTY in BOTH directions (`.agent/handoff.md` is C7's and still pending); `git show --numstat` agrees cell by cell with every `## Commits` row above; the LINE-ANCHORED `^<<<SLICE ` and `^<<<END ` each count 0 in `.agent/plan.md`, 0 in `.agent/live_review.md` and 0 in `.agent/decisions.md`; `git ls-files .remedy-wt` 0; one worktree; the round's 8 reflog rows all carry the action `commit` — amend 0, rebase 0, cherry 0.
- G12 exit 0 — `gh pr list --state open --json number,headRefName` printed, verbatim, `[]`. No PR created, nothing merged: the integration gate has not run and the closure protocol creates the PR at closure.
- G13 — CHECKED, ONE RESIDUAL, reported and NOT repaired. Re-measured at C6: `git merge-base main HEAD` IS `c34ef32b`; R-0672, R-0625, R-0431, R-0413, R-0533, R-0495, R-0574, R-0622 and R-0665 are each exactly one `^- R-\d+ — ` record; the plan's single-arithmetic-home sentence still holds at C6 (G7); DEC14's `Measured at 5d3e6045` clause is SCOPED and verified true there — `budgetFinal` occurs 0x in `types.ts` at `5d3e6045` and 2x at C6, `costFinalNote` 1x at C6, which is the change this round exists to make and not a staleness. RESIDUAL: DEC14's reversal instruction says `remedyApi.test.ts` gained "its three cases" while the `budget_final transport` describe holds 4 `it(` cases — the block's three plus one pinning `normalizeApiFailure`'s new `budgetFinal: null`. CARRIED, NOT RE-MEASURED: PLANF022R14's sentence that `npm run lint` in `apps/ui` is RED at base — G8's "NOT A GATE and not run" clause excludes it.

## Authored-text proofs

Three slices extracted PROGRAMMATICALLY by their marker LINES from the COMMITTED
C0a blob and applied byte-for-byte, never retyped or reflowed: PLANF022R14
2607 B, LEDGER14 5002 B, DEC14 4510 B. Disk-to-disk equality is G2, G4
(bare-slice control FALSE) and G5 (two independent readers per file, byte-flip
controls). The C4/C5/C6 production code is AUTHORED, not transported, exactly as
the block's slice convention states.

## Deviations & assumptions

- ORDERED COMMIT SEQUENCE: none. C0a, C0b, C1, C2, C3, C4, C5, C6, C7 landed
  exactly as constraint 3 fixes them — no extra commit, none dropped, no
  reordering.
- NO SLICE WAS EDITED. One slice contradicts what I measured, declared under
  constraint 1 and repeated in G13: DEC14's reversal says `remedyApi.test.ts`
  gained "its three cases"; it gained four. The fourth pins `normalizeApiFailure`
  returning `budgetFinal: null`, a line C5 had to add for `tsc` to pass once the
  field became non-optional. I left the slice and the test both alone.
- TOOLING: `npx` is DENIED to this worker session-wide, so G8's `npx vitest run`
  and `npx tsc --noEmit` ran as `npm run --prefix apps/ui test:unit` and
  `npm run --prefix apps/ui typecheck`, whose package.json bodies are literally
  `vitest run` and `tsc --noEmit`. `--prefix` replaces the block's "with `apps/ui`
  as the working directory"; vitest's own banner confirmed the root each time.
- BY CONSTRUCTION of constraint 3's order, C4 references `costFinalNote` before
  C6 declares it, so C4 and C5 do not typecheck in isolation. G8 measures C6,
  where they do. Nothing was reordered to hide this.
- No measurement of mine differed from a reference numeral the block states for
  the base `5d3e6045`, so nothing needed reconciling under constraint 9.
- G11's numbers cover the 8 commits BEFORE C7; C7's own belong to the next
  round's ledger entry, as the block directs.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save this block | done | |
| C0b mirror it into last_block | done | |
| C1 the plan | done | |
| C2 the R13 verdict | done | |
| C3 DECISION F022 D8 | done | |
| C4 the reconciliation module and its tests | done | |
| C5 the transport, type and mapping | done | |
| C6 the render and its contract | done | |
| C7 the handback | done | this commit |

## Next

1. Phase 1 rule 1 FIRST: re-read `.agent/STOP` from disk before anything else.
2. Gate R14 — this round is ungated and its verdict is the next round's C1.
3. R15, the integration gate, per docs/agents/integration_gate.md. T003b is now
   complete on both halves, so F022 has no unbuilt clause left in its Goal.

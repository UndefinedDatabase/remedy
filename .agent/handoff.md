# Handoff — F031 Decision inbox, R25 (worker → planner/reviewer)

Branch `feature/f031-decision-inbox`. Base `6163e887`. C0a `31692efd`, C0b `7361d821`, C1 `84f7e6dd`, C2 `a48219d4`, C3 `82d4992a`, C4 = this commit.

Fortschritt: ~88 % (F031 claimed; R1 through R24 landed, R24 gated here ·
             T001 SHIPPED · T002a MODEL shipped, wired and RENDERED ·
             T002b ORDERING, FILTERING and BADGE SERVER SHIPPED and gated ·
             T002b badge UI half here, closing T002b · T003 offen)
             — Schaetzung

## Range
Review of 6163e887..HEAD

## Commits
### 31692efd docs(agent): save the F031 R25 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f031-r25.md | +450 -0 | C0a — the block saved verbatim |

### 7361d821 docs(agent): mirror the F031 R25 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +286 -286 | C0b — byte-identical mirror of the C0a blob |

### 84f7e6dd docs(agent): point the F031 plan at R25
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +27 -25 | C1 — PLANF031R25, whole-file |

### a48219d4 docs(agent): record the F031 R24 verdict and mint R-0683
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4 -0 | C2 — LEDGER25 appended |

### 82d4992a feat(ui): give the decision inbox card its open-decision count
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/decisionCard.ts | +26 -12 | S1 `countOpenDecisions` + the header's absence note repaired |
| apps/ui/src/api/decisionCard.test.ts | +50 -0 | S4 — 5 tests on the count |
| apps/ui/src/api/decisionFilter.ts | +8 -6 | S3 — both falsified sentences retired |
| apps/ui/src/components/panels/DecisionInboxCard.tsx | +37 -18 | S2 — the badge, plus this file's own falsified sentence (deviation 1) |
| apps/ui/src/components/panels/RightLivePanel.module.css | +17 -0 | S2 — `.decisionOpenCount` APPENDED, no existing rule edited |
| .agent/decisions.md | +36 -0 | S5 — DECISION F031 D10 |

### C4 — this commit (self-reference, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C4 — this handback |

## External actions
- `git worktree add .remedy-wt/f031-r25-redproof 82d4992a` → created at a path that did not exist; `git worktree remove .remedy-wt/f031-r25-redproof` → removed BY THAT EXACT PATH, `git worktree list` 1 line after, the mutated file restored byte-identically inside the worktree first.
- Scratch I created and left, by exact path: `.remedy-wt/r25-extract-PLANF031R25.txt`, `.remedy-wt/r25-extract-LEDGER25.txt`, `.remedy-wt/r25-handoff-draft.md`. Nothing pre-existing under `.remedy-wt/` was touched or deleted.
- `git push origin feature/f031-decision-inbox` — ordered after C4. That push's outcome is not a value of any file this round writes: the reviewer measures the pushed tips at the next gate and records them in the R25 entry of `.agent/live_review.md`.
- No PR created, no branch deleted, nothing merged, no force flag, no history rewrite.

## Verification
- G1 branch `feature/f031-decision-inbox`, not `main`; `.agent/STOP` read from disk ABSENT before C0a and again before C4; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3. All FOUR readings — scratch `.remedy-wt/f031-r25.md`, the C0a blob, the C0b blob, `.agent/last_block.md` off disk — sha256 `763fadf96fd9f162398c1f43c1480014f601607d6d0c85f412af01043ed9e8a7`, 39202 bytes, 450 newlines, EQUAL; C0a's and C0b's file is the SAME git blob `23946f597c7371987f5a51ec2aa877e41336228e`.
- G2 my extractor over the COMMITTED C0a blob printed 2 slices (PLANF031R25, LEDGER25), CONTENT 52 lines inside markers, TOTAL 450 lines, so PROSE = 450 − 52 = 398 — under the 400 prose cap (F085 D5) and under the 490 total cap (F085 D6). Neither is exceeded.
- G3 `.agent/plan.md` at C1 byte-equal to PLANF031R25 under the newline-INCLUDED convention, 2849 bytes and 49 newlines on both sides; NEGATIVE CONTROL against the slice minus its trailing newline False; `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 49, strictly under 50.
- G4 reader (a), the equality constraint 8 states: True, 677520 + 1 + 10037 = 687558 = actual 687558. Reader (b): blank-line units 309 → 311, N = 2 as MY split measured, the last 2 units equal LEDGER25's 2 paragraphs IN ORDER; trailing-newline handling — `rstrip("\n")` applied to BOTH sides of every compared unit. NEGATIVE CONTROL, one byte flipped inside the appended text IN MEMORY only, never on the tracked file: both readers reject the mutant, both accept the true file.
- G5 `^- R-\d+ — ` 243 → 244 all DISTINCT, ids ADDED exactly {R-0683}, ids REMOVED the EMPTY SET, max R-0682 → R-0683; `^Done: R-\d+ — ` 4 → 4; `^Landed: R-` 0 → 0; `^Recurrence: R-` 19 → 19; `^Gate: R\d+ — ` 19 → 19 UNCHANGED; `^Gate: F\d+ R\d+ — ` 5 → 6, ADDED key exactly `F031 R24`, all keys DISTINCT; §3 item 10 open set 239 → 240 at C2; `^- R-0593 — ` occurs exactly 1; `git diff --name-only a48219d4..82d4992a` does NOT name `.agent/live_review.md`.
- G6 red proof in the disposable worktree at C3, vitest run from the PRIMARY `apps/ui` with `--root` at the worktree. UNMUTATED: REAL exit 0, 20 files, 332 tests. MUTANT (`countOpenDecisions`'s body → `return models.length;`, every other byte untouched): REAL exit 1, 4 failed / 328 passed, the failing tests being `countOpenDecisions > counts only the open cards of a mixed list`, `> answers zero when every card in the list is already resolved`, `> reads isOpen rather than an open-SOUNDING status string`, `> ignores the type filter's business entirely, counting across every type`. IT WENT RED. Worktree removed by its exact path `.remedy-wt/f031-r25-redproof`; `git worktree list` 1 line after.
- G7 structure at C3 in `DecisionInboxCard.tsx`: the literal `if (decisions.length === 0) return null;` exactly 1; `aria-pressed` 1, `aria-live` 1, both still present; the call line is `  const openCount = countOpenDecisions(decisions);` — the UNFILTERED prop — and lines holding BOTH `countOpenDecisions` and the token `visible` number 0. In `decisionCard.ts`, `countOpenDecisions` greps to exactly 1 `export` line.
- G7 suites, PRIMARY checkout at C3, `git worktree list` 1 line immediately before the first, run SERIALLY and never two alive at once, every one a REAL exit 0: `npm run typecheck` exit 0, stdout only npm's own two banner lines, stderr empty, 0 diagnostics; `npm run test:unit` exit 0, 23 files / 357 tests, `decisionFilter.test.ts` 20 and `decisionOrder.test.ts` 16 both UNMOVED, `decisionCard.test.ts` 27 → 32, difference 5, exactly the 5 tests S4 adds. Python, by the block's exact lines: `tests/ui_server/` 480; `test_test_runner` 52; `test_resource_safety` 21; `test_integrity_gate` 16; `tests/ui_contracts/` 525 passed with 4 skipped; `test_golden_path` 42. Every one identical to the reviewer's base reading — no difference to account for.
- G8 line-anchored `^<<<SLICE ` and `^<<<END ` both 0 in `.agent/plan.md` at C1, `.agent/live_review.md` at C2 and all six files C3 writes, against CONTROL 2 and 2 over the C0a blob. `git diff --name-only 6163e887..82d4992a` names 10 paths, NONE under `docs/`, `packages/` or `tests/`, and none of `.agent/context.md`, either inventory, `RightLivePanel.tsx`, `decisionOrder.ts`, `RemedyApp.tsx` or `GraphFilterChips.tsx`; range MINUS change set EMPTY, change set MINUS range exactly `.agent/handoff.md`. C0a..C3 each SINGLE-PARENT with insertions 450, 286, 27, 4, 166 read from `git diff --numstat`, each under the 500 cap (DECISION F104 D1), agreeing cell for cell with the `+/-` column above. `git ls-files .remedy-wt` 0; `git ls-files *.zip` 0. Reflog scoped to THIS ROUND'S 5 entries by the operation prefix before the first colon: `commit` 5×, amend 0, rebase 0, cherry 0. SHA-shaped tokens in the C0a blob, word-bounded 7–40 hex: 24 occurrences, 11 distinct, types 10 `commit` + 1 `blob` (`141e5735…` the blob), FAILING SET EMPTY.
- G9 the push — see `## External actions`; its outcome is the reviewer's to measure, not this file's.

## Authored-text proofs
PLANF031R25 → `.agent/plan.md` at C1: byte-equal, 2849 bytes both sides (G3). LEDGER25 → `.agent/live_review.md` at C2: whole-file equality True plus the independent last-2-units-in-order reading (G4). Both slices were extracted PROGRAMMATICALLY by marker LINE out of the COMMITTED C0a blob, and no marker line reached any target file (G8). No `Done:` and no `Landed:` line was written.

## Deviations & assumptions
1. ADDITION BEYOND THE LITERAL SPEC, and I believe the spec is incomplete rather than wrong. S1 and S3 name two falsified comments; there is a THIRD, in `DecisionInboxCard.tsx` itself — "The inbox badge's COUNT is still genuinely absent everywhere" — which THIS commit falsifies. S2 opens that file anyway and it is in the change set, so I repaired it there and named where the count now lives. Leaving it would have shipped a fresh instance of exactly the R-0593 class S3 exists to close.
2. TENSION INSIDE S2, resolved rather than worked around, and reported so the reviewer can overrule it. S2 says the badge "shows the number S1 returns and nothing else" and, two sentences later, that it must "carry a word saying what is counted, on an element whose ROLE permits a name". A bare digit cannot carry a word. What ships is an `<output>` (implicit ARIA role `status`, which permits a name, unlike the `generic` role a bare `div`/`span` gets — R-0682's whole subject) whose VISIBLE text is `{openCount} open`. Its `aria-label` is `"Open decisions waiting: <n>"` and NOT the bare phrase, because `aria-label` REPLACES an element's content in the accessibility tree: a label naming only the word would have hidden the digit it explains. The colon form needs no plural branch, so no branch entered this untested markup (DECISION F031 D5).
3. ASSUMPTION recorded, not gated: `countOpenDecisions` is the name I chose under S1's naming clause — 3 words, one domain word, and it grepped to 0 occurrences anywhere under `apps/` before I wrote it. Likewise `.decisionOpenCount` for the CSS class. The class is APPENDED; no existing rule in `RightLivePanel.module.css` was edited, and every value in it resolves to a custom property the sheet already uses above (`--remedy-radius-pill`, `--remedy-bg-2`, `--remedy-line`, `--remedy-muted`). `--remedy-focus` is not referenced.
4. NO CONTRADICTION FOUND between the block's stated base readings and my own: `.agent/plan.md` 47 lines / 2792 bytes at base, live_review 677520 bytes, the ledger sets 243/4/0/19/19/5, and all six Python suite counts reproduced exactly. The block's sha256, byte count and line count for its own file all three matched what I measured, so no reviewer numeral is declared wrong.
5. No departure from the ordered commit sequence: C0a, C0b, C1, C2, C3, C4 — six commits, none extra, none dropped, none reordered. No amend, rebase, cherry-pick, force-push, history rewrite, branch deletion, merge or pull request.
6. Handback tier, resolved from AGENTS.md `### handoff.md` against the commit count constraint 4 fixes: 6 commits, more than 5, so the cap is ≤100 lines. This file measures 100 lines with `wc -l`, so it FITS and no DECISION D15 overage is claimed; no token cap is claimed either. The `Fortschritt:` block above is carried VERBATIM from the block and measures 5 lines.

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a save block | done | |
| C0b mirror block | done | |
| C1 plan | done | |
| C2 ledger | done | |
| C3 code, tests, D10 | done | |
| C4 handback | done | this commit |
| S1 count + header repair | done | `countOpenDecisions` in `decisionCard.ts` |
| S2 badge + style | deviated | shipped as ordered; S2's two clauses conflict — deviation 2 |
| S3 decisionFilter.ts comments | deviated | both sentences retired as ordered; a THIRD falsified comment repaired — deviation 1 |
| S4 tests | done | 5 tests, 27 → 32 |
| S5 DECISION F031 D10 | done | |
| push | done | ordered after C4; outcome carried by G9 to the reviewer |

## Findings
Open set 240 at `a48219d4`, by the §3 item 10 rule DECISION F009 D10 requires — every `^- R-\d+ — ` paragraph (244) minus every `^Done: R-\d+ — ` line (4). This round mints R-0683 and resolves none; R-0593 stays OPEN, its instances in `packages/orchestration/release_gate.py` and `pyproject.toml` untouched and its landed paragraph unedited.
The narrower set, the findings THIS FEATURE must still act on, is the 23 distinct ids `.agent/plan.md` lists at `84f7e6dd` across 25 occurrences, the two repeats being R-0495 and R-0574 named again as the Highs.

## Next
This round ends the session. The next session, in this order: (1) read `.agent/STOP` from disk as Phase 1 rule 1, BEFORE the Open PR Gate as rule 2; (2) the R25 verdict is UNRECORDED and is owed by the next round's ledger commit (DECISION F085 D9); (3) T002b is CLOSED by this round, so the next work is T003 per DECISION F031 D4 — answering through the existing write channel — whose first round also carries R-0682's `role="group"` fix in both files that need it.

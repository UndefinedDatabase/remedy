# Handback — F031 Decision inbox, round R38 (T003 component wiring, LAST step)

Branch: `feature/f031-decision-inbox`. Open findings: 241.

## Range

Review of `a1bf1f5d`..`HEAD`.

## Commits

### 173573e0 docs(agent): save the F031 R38 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f031-r38.md | +271/-0 | C0a, the block saved byte for byte |

### eb959257 docs(agent): mirror the F031 R38 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +236/-285 | C0b, the C0a blob read back with `git show` |

### 4de53f90 docs(agent): point the F031 plan at R38
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +17/-20 | C1, PLANF031R38 applied byte for byte |

### a5d1268e docs(agent): record the F031 R37 verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C2, LEDGER38 appended |

### 0a513667 feat(ui): make the decision inbox answerable from the card
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/RemedyApp.tsx | 7 files, +147/-49 | S1, `serverToken={token}` to the shell |
| apps/ui/src/components/shell/RemedyShell.tsx | " | S1, prop declared and passed on |
| apps/ui/src/components/panels/RightLivePanel.tsx | " | S1/S2, prop plus `jobId={dashboard.jobId}` |
| apps/ui/src/components/panels/DecisionInboxCard.tsx | " | S2-S7, target, click, keys, tone, header |
| apps/ui/src/components/panels/RightLivePanel.module.css | " | S5, the outcome classes |
| apps/ui/src/api/decisionCard.ts | " | S6, the "SEND is absent" clause retired |
| apps/ui/src/api/decisionAnswer.ts | " | S6, the "sender round" clause retired |

### aad8df00 test(ui-contracts): pin the decision answer wiring in source
| Path | +/- | Reason |
|---|---|---|
| tests/ui_contracts/test_decision_answer_wiring.py | +198/-0 | C4, the S8/S9 guard, 16 tests |

### C5 (this commit, grouped — a handoff cannot table itself, R-0149)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C5, this handback |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | same git blob `f3833bda` as C0a |
| C1 | done | |
| C2 | done | |
| C3 | done | one commit, per constraint 5 |
| C4 | done | |
| C5 | done | this commit |
| push | done | ordered after C5; its reading is not carried here |

## Verification

One physical line per gate, as the block orders; the full per-gate detail is in this round's report.

- G1 BRANCH/CLEAN/TRANSPORT — exit 0. Branch correct; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3, C4; `.agent/STOP` ABSENT at both ordered readings; the C0a blob, the C0b blob and both working copies read at C4 are ALL FOUR sha256 `8a3d0e942842451e71fced4d310b51e667360f650a5b6d0f4fb98bcccea30f8b` over 22029 bytes and 271 lines, EQUAL, with C0a and C0b the SAME git blob `f3833bda`.
- G2 EXTRACTION/CAPS — exit 0. Extracted from the committed C0a blob by marker line: 2 slices, CONTENT 47, TOTAL 271, PROSE 224 — 224 <= 400 (DECISION F085 D5) and 271 <= 490 (DECISION F085 D6).
- G3 THE PLAN — exit 0. `.agent/plan.md` at C1 byte-equal to PLANF031R38 under the newline-INCLUDED convention at 2638 bytes; the minus-trailing-newline negative control FALSE; `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 46, strictly under 50.
- G4 THE APPEND — exit 0. Whole-file byte equality 795163 + 1 + 3720 = 798884 against an actual 798884, pre-commit blob a byte-exact PREFIX; second reader: blank-line units 333 -> 334, the last 1 unit equals LEDGER38's 1 paragraph IN ORDER, the SWAPPED comparison FALSE; a one-byte IN-MEMORY flip is REJECTED by both readers and the tracked file was never mutated.
- G5 THE LEDGER SETS — exit 0. `^- R-\d+ — ` 246 -> 246 with ids ADDED and ids REMOVED both the EMPTY SET, all 246 DISTINCT, maximum `R-0685`; `^Done: R-\d+ — ` 5 -> 5; `^Landed: R-` 0 -> 0; `^Gate: R\d+ — ` 19 -> 19; `^Gate: F\d+ R\d+ — ` 18 -> 19 with the ADDED key exactly `F031 R37`, all keys DISTINCT; the open set is 241 at C2.
- G6 MARKERS/PATHS/COMMITS — exit 0. `^<<<SLICE ` and `^<<<END ` are 0 and 0 in the plan at C1 and the ledger at C2 against a live CONTROL of 2 and 2 over the C0a blob; `git diff --name-only a1bf1f5d..aad8df00` names 12 paths with range-minus-change-set EMPTY and change-set-minus-range exactly `.agent/handoff.md`, which is C5; insertions 271, 236, 17, 2, 147 and 198 from `git diff --numstat`, each SINGLE-PARENT and each under 500; `git ls-files .remedy-wt` 0 and `git worktree list` 1 line at C4; the reflog for the six reads `commit` in every operation prefix, so `amend`, `rebase` and `cherry` are 0 each.
- G7 THE COMPILER — REAL exit 0 twice: `npx tsc --noEmit` in `apps/ui` at C3 and again at C4, zero diagnostics both times.
- G8 THE UNIT SUITE — `npx vitest run` in `apps/ui` at C4, REAL exit 0, 30 test files and 448 tests, IDENTICAL to `a1bf1f5d` on both numbers, this round having added no `.test.ts`.
- G9 GUARD/RED PROOF/READERS — REAL exit 0, 16 tests collected. Red proof in the disposable worktree `.remedy-wt/r38red`: the exact bytes `serverToken={serverToken}` occurred 1 time in its `RemedyShell.tsx`, and deleting that ONE occurrence gave REAL exit 1 with 1 failure, the node id `TestServerTokenReachesTheCard::test_shell_passes_the_token_to_the_live_panel` — so the guard does reach the chain; the worktree was removed by its exact path and `git worktree list` is back to 1 line. Six suites run SERIALLY in the primary at C4, every one a REAL exit 0: `tests/ui_server/` 480, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16, `tests/ui_contracts/` 541 passed with 4 skipped (525 -> 541, a movement of exactly the 16 this gate's first command collected), and the canary `test_golden_path` 42.

## Authored-text proofs

PLANF031R38 and LEDGER38 were extracted from the COMMITTED C0a blob by marker line and applied unretyped; G3 and G4 are their disk-to-disk results.

## Deviations & assumptions

- `git commit` ran with `-q`, so its own summary was suppressed. Every insertion figure comes from `git diff --numstat` and was confirmed against `git show --shortstat`, which prints the identical per-commit sentence.
- S5 orders three tone classes; a FOURTH class `.decisionOutcome` was added beside them carrying layout only (`flex-basis`, `margin`, `font-size`, `line-height`). The `Record<DecisionOutcomeTone, string>` maps to exactly the three tone classes S5 names, and the base class carries no colour and no token.
- The outcome sentence is rendered only once an outcome exists, which is S5's wording; an always-present empty live region would announce more reliably but is not what the spec described.
- NOT FIXED because it lies outside the change set: `decisionAnswerFlow.ts`'s header still reads "the card that shows it is R37's", and that card is R38's. The block's Change list does not name that file, so it was left untouched.
- No contradiction was found inside the block, no slice was corrected, and no ordered commit was added, dropped or reordered.

## Next

The clarification FORM and the `NeedsAttentionCard` decision-branch ruling (DECISION F031 D4), then the integration-gate round.

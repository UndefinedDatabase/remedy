# Handback — F031 Decision inbox, round R39 (answer-control repair)

Branch: `feature/f031-decision-inbox`. Base `279cd819`, tip at C4 `f93e1008`.
Open findings: 244.

## Range

Review of `279cd819`..`HEAD`.

## Commits

### 569f2c11 docs(agent): save the F031 R39 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f031-r39.md | +234/-0 | C0a, the block saved byte for byte |

### a218cd86 docs(agent): mirror the F031 R39 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +153/-190 | C0b, the C0a blob read back with `git show` |

### 403ff14f docs(agent): point the F031 plan at R39
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +12/-10 | C1, PLANF031R39 applied byte for byte |

### 5d073e9b docs(agent): register the three findings the F031 R38 gate raised
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +6/-0 | C2, FINDINGS39 appended BEFORE any fix |

### f71893d8 docs(agent): record the F031 R38 verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C3, LEDGER39 appended |

### f93e1008 fix(ui): announce the answer outcome and disable a button by its own key
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/decisionAnswerFlow.ts | +1/-1 | S4, the header names the card |
| apps/ui/src/components/panels/DecisionInboxCard.tsx | +52/-20 | S1/S2/S3 |
| apps/ui/src/components/panels/RightLivePanel.module.css | +13/-0 | S2, the quiet class and its WHY |
| tests/ui_contracts/test_decision_answer_wiring.py | +104/-2 | S5, 9 new tests, 1 rewritten |

### C5 (this commit, grouped — a handoff cannot table itself, R-0149)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C5, this handback |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | same git blob `5754c75c` as C0a |
| C1 | done | landed while the plan still described R38, as ordered |
| C2 | done | the findings land before any fix |
| C3 | done | |
| C4 | done | |
| C5 | done | this commit |
| push | done | ordered after C5; its reading is not carried here |

## The three findings

- R-0686 — the outcome paragraph carrying `aria-live="polite"` is now rendered from a decision row's FIRST render with an empty sentence, and only its TEXT is conditional; its empty state is collapsed by `.decisionOutcomeQuiet { position: absolute; }`, out of flow, with a CSS WHY comment naming `display: none`, `visibility: hidden` and the `hidden` attribute as the three mechanisms excluded because each removes the node from the accessibility tree.
- R-0687 — `sendingKey: string | null` became `sendingKeys: ReadonlySet<string>`; a press adds ONLY its own key through `withAnswerKey` and its settle removes ONLY its own through `withoutAnswerKey`, `disabled={sendingKeys.has(answerKey)}` reads its own key alone, and there are exactly TWO writers of that state, so no second press can enable or clear another answer's button. The comment above the state now states the stronger guarantee and names the weaker one it replaced.
- R-0688 — `decisionAnswerFlow.ts`'s header sentence now reads "the card that shows it is `DecisionInboxCard.tsx`"; nothing else in that file changed (+1/-1).

## Verification

One physical line per gate; per-gate detail is in this round's report.

- G1 BRANCH/CLEAN/TRANSPORT — exit 0. Branch `feature/f031-decision-inbox`; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3 and C4; `.agent/STOP` ABSENT at both ordered readings; the C0a blob, the C0b blob and both working copies read at C4 are ALL FOUR sha256 `0fa1108a24dffcaea736a42474feaafba2d74871f910b0b8e1ecb5a94b99cad9` over 25411 bytes and 234 lines, EQUAL, C0a and C0b resolving to the SAME git blob `5754c75c`.
- G2 EXTRACTION/CAPS — exit 0. Extracted from the COMMITTED C0a blob by marker line: 3 slices printed, CONTENT 54, TOTAL 234, PROSE 180 — 180 <= 400 (DECISION F085 D5) and 234 <= 490 (DECISION F085 D6).
- G3 THE PLAN — exit 0. `.agent/plan.md` at C1 byte-equal to PLANF031R39 under the newline-INCLUDED convention at 2807 bytes; the minus-trailing-newline negative control FALSE; `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 48, strictly under 50.
- G4 THE TWO APPENDS — exit 0. C2: 798884 + 1 + 5435 = 804320 against an actual 804320; C3: 804320 + 1 + 4819 = 809140 against an actual 809140; each pre-commit blob a byte-exact PREFIX. Second reader, blank-line units: 334 -> 337 with the last 3 units equal to FINDINGS39's 3 paragraphs IN ORDER and the SWAPPED comparison FALSE; 337 -> 338 with the last unit equal to LEDGER39's single paragraph — a one-paragraph slice makes its own reversal IDENTICAL, so the swap was run cross-slice instead and is FALSE both ways. A one-byte IN-MEMORY flip is REJECTED by both readers for both appends; the tracked file was never mutated.
- G5 THE LEDGER SETS — exit 0. `^- R-\d+ — ` 246 -> 249 -> 249, ids ADDED across C2 exactly {`R-0686`, `R-0687`, `R-0688`} and across C3 the EMPTY SET, ids REMOVED the EMPTY SET at both steps, all 249 DISTINCT, maximum `R-0688`; `^Done: R-\d+ — ` 5 -> 5 -> 5; `^Landed: R-` 0 -> 0 -> 0; `^Gate: R\d+ — ` 19 -> 19 -> 19; `^Gate: F\d+ R\d+ — ` 19 -> 19 -> 20 with the ADDED key exactly `F031 R38`; open set 241 before C2 and 244 after C3.
- G6 MARKERS/PATHS/COMMITS — exit 0. `^<<<SLICE ` and `^<<<END ` are 0 and 0 in the plan at C1 and in the ledger at C3, against a live CONTROL of 3 and 3 over the C0a blob; `git diff --name-only 279cd819..f93e1008` names 8 paths, range-minus-change-set EMPTY and change-set-minus-range exactly `.agent/handoff.md`, which is C5, with nothing under `docs/`, `packages/` or `apps/cli/`, one path under `tests/` and one under `apps/ui/src/api/`; insertions 234, 153, 12, 6, 2 and 170 from `git diff --numstat`, each SINGLE-PARENT and each under 500; `git ls-files .remedy-wt` 0 lines and `git worktree list` 1 line at C4; the reflog for the six reads `commit` in every operation prefix, so `amend`, `rebase` and `cherry` are 0 each.
- G7 THE FIXES ARE PROVED — REAL exit 0 three times at C4: `npx tsc --noEmit` in `apps/ui` with zero diagnostics, `npx vitest run` in `apps/ui` at 30 files and 448 tests (IDENTICAL to `279cd819`, no `.test.ts` added), and the guard file at 25 collected, up from 16. All 10 new or rewritten assertions were proved capable of failing in the disposable worktree `.remedy-wt/r39red`, never in the primary: 7 reverts, each of a string occurring EXACTLY 1 time in the file it was removed from, each REAL exit 1 — R1 (the region created with its sentence again) failed `TestTheOutcomeRegionExistsBeforeItSpeaks::test_the_region_is_rendered_empty_rather_than_created_with_its_sentence` and `::test_the_region_is_never_conditionally_created`, 2; R2 (`display: none`) failed `::test_the_empty_region_is_collapsed_out_of_flow` and `::test_the_outcome_rules_never_use_a_mechanism_that_removes_the_node`, 2; R3 (`hidden` attribute) failed `::test_the_card_never_hides_the_region_with_the_hidden_attribute`, 1; R4 (`disabled` reads the whole set) failed `TestTheRetiredAndDeliberateAbsences::test_the_buttons_are_not_unconditionally_disabled`, 1; R5 (a settle clears every key) failed `TestOnePressTouchesOnlyItsOwnButton::test_a_press_removes_only_its_own_key_when_it_settles`, 1; R6 (a third writer) failed `::test_no_third_writer_can_clear_the_in_flight_set`, 1; R7 (the header back to a round number) failed `TestTheFlowHeaderNamesItsCard::test_the_header_names_the_component_that_shows_the_sentence` and `::test_the_header_routes_no_reader_to_a_round_number`, 2. Each revert was restored, the worktree read 25 passed again, it was removed BY ITS EXACT PATH and `git worktree list` is back to 1 line.
- G8 THE READERS AND THE CANARY — REAL exit 0 for all six, run SERIALLY in the primary checkout at C4, never two pytest processes alive at once: `tests/ui_server/` 480, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16, `tests/ui_contracts/` 550 passed with 4 skipped, and the canary `test_golden_path` 42. Every count is base-identical except `tests/ui_contracts/`, which moved 541 -> 550: exactly the 9 TEST FUNCTIONS G7's guard file gained, 16 -> 25.

## Authored-text proofs

PLANF031R39, FINDINGS39 and LEDGER39 were extracted from the COMMITTED C0a blob by their marker lines and applied unretyped; G3 and G4 are their disk-to-disk results. No slice was corrected or reflowed.

## Deviations & assumptions

- ONE EXISTING ASSERTION WAS REWRITTEN, WHICH S5's "keep every assertion the file already carries" forbids as written. `test_the_buttons_are_not_unconditionally_disabled` quoted the literal `disabled={sendingKey === answerKey}` — the very expression S3 orders replaced — so S5 and S3 cannot both be met on that line. The assertion's PROPERTY was kept and restated over the new shape (`disabled={sendingKeys.has(answerKey)}`), no assertion was deleted, and the file grew from 16 to 25 tests. Flagged rather than silently resolved.
- The push status above says `done` in the R38 sense: it is ordered after C5, and no reading of it is carried here.
- `git commit` ran with `-q`; every `+/-` cell comes from `git diff --numstat` itself.
- LEDGER39 is a SINGLE paragraph, so G4's ordered-swap control is degenerate for it (a one-element reversal is the identity). It is reported as such and the cross-slice swap was run in its place, FALSE both ways, rather than reported as a passing control it cannot be.
- No other contradiction was found inside the block, no slice was corrected, and no ordered commit was added, dropped or reordered.

## Next

The clarification FORM and the `NeedsAttentionCard` decision-branch ruling (DECISION F031 D4), then the integration-gate round.

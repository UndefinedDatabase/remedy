# Handback — F031 Decision inbox, round R40 (guard-reach repair)

Branch: `feature/f031-decision-inbox`. Base `14fde389`, tip at C4 `05bdeae1`.
Open findings: 246.

## Range

Review of `14fde389`..`HEAD`.

## Commits

### c02c35d4 docs(agent): save the F031 R40 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f031-r40.md | +241/-0 | C0a — the block saved byte for byte |

### a175b7e1 docs(agent): mirror the F031 R40 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +139/-132 | C0b — mirrored by `git show`, same blob `662d158d` |

### ef3bd0d3 docs(agent): point the F031 plan at R40
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +13/-13 | C1 — PLANF031R40 applied byte for byte |

### c600827b docs(agent): register the two findings the F031 R39 gate raised
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | C2 — FINDINGS40 appended: R-0689, R-0690 |

### cbb021d6 docs(agent): record the F031 R39 verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C3 — LEDGER40 appended: `Gate: F031 R39` |

### 05bdeae1 test(ui): pin the helper bodies and forbid every conditional live region
| Path | +/- | Reason |
|---|---|---|
| tests/ui_contracts/test_decision_answer_wiring.py | +103/-1 | C4 — S1, S2, S3; the single deletion is the S2 rename |

### C5 (this commit — a handoff cannot table itself, R-0149)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | self-reference | C5 — this rewrite |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | this commit |
| push | done | ordered after C5; its reading belongs to the next gate |

## The two findings

- R-0689 — FIXED at C4. New class `TestTheInFlightHelpersTouchOnlyTheirOwnKey` reads the EXTRACTED BODY of `withAnswerKey` and of `withoutAnswerKey` through the new brace-matching reader `ts_function_body`, never a whole-file sweep, and pins per body: copy before change (`new Set(sending)`), only the passed key (`next.add(answerKey)` / `next.delete(answerKey)`), no bulk operation (`.clear(` and `new Set()` both excluded), plus a cross-check that each body is not the other's. The reviewer's surviving mutation now fails 2 tests.
- R-0690 — FIXED at C4. New reader `jsx_between_answer_button_and_live_paragraph` takes the comment-stripped source between the answer button's `</button>` and the `<p` carrying the LAST `aria-live="polite"`; `test_the_region_is_created_under_no_conditional_operator_at_all` forbids `?`, `&&` and `||` there. The old literal check is kept verbatim and only RENAMED to `test_the_null_ternary_shape_r0686_was_registered_against_is_absent`. The reviewer's surviving mutation now fails.

## External actions

`git worktree add .remedy-wt/r40red 05bdeae1 --detach` — created; `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/r40red` by exact path — done, list back to 1 line. Push of `feature/f031-decision-inbox` after C5; the block leaves its reading to the next gate. No PR or `gh` action this round.

## Verification

- G1 exit 0 — branch `feature/f031-decision-inbox`; `git status --porcelain` 0 lines after each of C0a/C0b/C1/C2/C3/C4; `.agent/STOP` read from disk ABSENT before C0a and again before C5; block sha256 `236f665d12e4dc7d9dda32a512b531dc9b982f3038fd698ce42027bc1a8e8f7a`, 24444 bytes, 241 lines — EQUAL as saved at C0a, as mirrored at C0b and as read off disk at C4; C0a and C0b are the SAME git blob `662d158d`.
- G2 exit 0 — 3 slices printed from the COMMITTED C0a blob by marker line; TOTAL 241, CONTENT 52, PROSE 189. My extractor counts `<<<SLICE`/`<<<END` as PROSE. 189 <= 400, 241 <= 490.
- G3 exit 0 — `.agent/plan.md` at `ef3bd0d3` BYTE-EQUAL to PLANF031R40 newline-included, 2771 bytes; minus-trailing-newline control FALSE; `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 48 (< 50).
- G4 exit 0 — C2: 809140 + 1 + 3246 = 812387 against actual 812387; reader B units 338 -> 340, last 2 units equal FINDINGS40's paragraphs IN ORDER, SWAPPED FALSE. C3: 812387 + 1 + 5281 = 817669 against actual 817669; units 340 -> 341, last unit equals LEDGER40 IN ORDER. LEDGER40 is ONE paragraph, so its self-reversal is the identity (TRUE) — declared degenerate, not reported as a passing control; the CROSS-SLICE swap against FINDINGS40's paragraphs is FALSE both ways. One in-memory byte flip per append: BOTH readers REJECT. The tracked file was never mutated.
- G5 exit 0 — `^- R-\d+ — ` 249 -> 251 -> 251; ADDED {`R-0689`, `R-0690`} across C2, ADDED EMPTY across C3, REMOVED EMPTY at both, all DISTINCT at all three points, maximum `R-0690`. `^Done: R-\d+ — ` 5, `^Landed: R-` 0, `^Gate: R\d+ — ` 19 at all three. `^Gate: F\d+ R\d+ — ` 20 -> 20 -> 21, ADDED key exactly `F031 R39`. Open set 244 before C2, 246 after C3.
- G6 exit 0 — `^<<<SLICE ` and `^<<<END ` are 0 and 0 in the plan at `ef3bd0d3` and in the ledger at `cbb021d6`, against a live CONTROL of 3 and 3 over the C0a blob. `git diff --name-only 14fde389..05bdeae1` = 5 paths; range-minus-declared EMPTY, declared-minus-range = {`.agent/handoff.md`} alone, which C5 writes. Insertions 241, 139, 13, 4, 2, 103 — each single-parent, each under 500. `git ls-files .remedy-wt` 0; `git worktree list` 1 line. Reflog: all six prefixes read `commit`; `amend` 0, `rebase` 0, `cherry` 0.
- G7 exit 0 — in `apps/ui`: `npx tsc --noEmit` REAL 0 with no diagnostic; `npx vitest run` REAL 0 at 30 files and 448 tests, identical to `14fde389`. Guard file REAL 0 at 31 collected (> 25). Six mutations in the disposable worktree `.remedy-wt/r40red` at C4, each target counted at exactly 1 occurrence in `DecisionInboxCard.tsx` before mutating, each restored byte-identical afterwards: (1) `new Set(sending)` -> `sending as Set<string>` in the adder — REAL 1, 1 failed, `TestTheInFlightHelpersTouchOnlyTheirOwnKey::test_the_add_helper_copies_the_set_before_it_changes_it`; (2) `next.add(answerKey)` -> `next.add(answerKey.trim())` — REAL 1, 1 failed, `::test_the_add_helper_adds_the_passed_key_and_nothing_else`; (3) the same copy mutation in the remover — REAL 1, 1 failed, `::test_the_remove_helper_copies_the_set_before_it_changes_it`; (4) `next.delete(answerKey)` -> `next.delete(String(answerKey))` — REAL 1, 1 failed, `::test_the_remove_helper_deletes_the_passed_key_and_nothing_else`; (a) the block's own `next.delete(answerKey);` -> `next.clear();` — REAL 1, 2 failed, that same test AND `::test_neither_helper_carries_a_bulk_operation`; (b) the block's own `{outcome === null ? undefined : ( ... )}` wrap with the inner ternary left in place — REAL 1, 1 failed, `TestTheOutcomeRegionExistsBeforeItSpeaks::test_the_region_is_created_under_no_conditional_operator_at_all`. No new assertion stayed green under its own mutation. Worktree removed by its exact path; `git worktree list` back to 1 line.
- G8 exit 0 for each, run SERIALLY in the primary checkout at C4 — `tests/ui_server/` 480 passed; `tests/orchestration/test_test_runner.py` 52; `tests/regression/test_resource_safety.py` 21; `tests/orchestration/test_integrity_gate.py` 16; `tests/ui_contracts/` 556 passed with 4 skipped; canary `tests/cli/test_golden_path.py` 42. `tests/ui_contracts/` moved 550 -> 556, exactly the guard file's 25 -> 31 in TEST FUNCTIONS. No other suite moved.

## Authored-text proofs

All three slices were extracted from the COMMITTED C0a blob by their marker LINES and applied byte for byte — PLANF031R40 by `shutil.copyfile`, FINDINGS40 and LEDGER40 by a byte append of one `\n` plus the slice. Disk-to-disk equality against the committed `.agent/authored/f031-r40.md` is proved under G3 and G4. Nothing was retyped, reflowed or corrected.

## Deviations & assumptions

- The ordered sequence C0a, C0b, C1, C2, C3, C4, C5 was followed exactly: no extra commit, none dropped, none reordered.
- S2 states the region between the button and the paragraph "is whitespace once comments are stripped". On disk it is whitespace PLUS the bare `{}` the stripper leaves where the JSX comment `{/* ... */}` stood. Reported rather than corrected: the assertion shipped is the ordered one — no `?`, `&&` or `||` in that region — and `{}` holds none of the three, so it is tight, not lucky.
- No file under `apps/`, `docs/`, `packages/` or `apps/cli/` was touched; the one `tests/` path is the guard file. The component was not edited to suit a guard.

## Next

Push `feature/f031-decision-inbox`, then the planner/reviewer re-runs G1 through G8 off disk and issues the R40 verdict.

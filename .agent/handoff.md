# Handback — F031 Decision inbox, Round R53 (the MODEL and COMMAND halves of the FORM)

Branch `feature/f031-decision-inbox`; base `e62726c7` → C3 `fd6e70a9`, then C4. THE BRANCH TIP IS GREEN: every gate this block ordered ran and passed.
NO FILE OUTSIDE `apps/ui/src/api/` AND `.agent/` CHANGED THIS ROUND — `packages/`, `docs/` and `tests/` are each EMPTY in `e62726c7..fd6e70a9`. Open findings: 255, unmoved.
BOTH G7 PROBES RETURNED NON-ZERO: the model probe 6 failing tests, the builder probe 5, against 0 failing at an unmutated control. Read G7 — the raw exit code alone is NOT the discriminator here.

## Range

Review of e62726c7..HEAD — C0a `8bb58a2d`, C0b `821254bd`, C1 `e0648abd`, C2 `a9c5d197`, C3 `fd6e70a9`, C4 this commit. Every `+/-` is `git diff --numstat` itself and agrees cell for cell with G8.

## Commits

### 8bb58a2d docs(agent): save the F031 R53 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f031-r53.md | +294/-0 | C0a: the block, verbatim |

### 821254bd docs(agent): mirror the F031 R53 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +194/-219 | C0b: the same bytes as C0a |

### e0648abd docs(agent): advance the plan to the F031 R53 form round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +16/-17 | C1: PLANF031R53 |

### a9c5d197 docs(agent): record the F031 R52 verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C2: LEDGER53 appended |

### fd6e70a9 feat(ui): carry the plan's open questions into the card model and the answer command
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/decisionCard.ts | +74/-0 | C3: S1 `DecisionClarification`, S2 the reader and the model field |
| apps/ui/src/api/decisionCard.test.ts | +121/-0 | C3: S5 model tests; both whole-model `toEqual`s updated |
| apps/ui/src/api/decisionAnswer.ts | +43/-5 | C3: S3 the optional fourth parameter, S4 the false header sentence |
| apps/ui/src/api/decisionAnswer.test.ts | +113/-0 | C3: S5 builder tests, 0 deleted lines |

### C4 (this commit) — the handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C4: a handoff cannot table its own commit |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | this commit |
| push | done | ordered after C4; run right after it, its reading not quoted here |

## External actions

- `git worktree add --detach .remedy-wt/r53-probe-c fd6e70a9`, the same for `r53-probe-d` and `r53-probe-c2` — each exit 0, each removed by its EXACT path with `git worktree remove --force`, list back to 1 line each time. Three, not two: see Deviations 3.
- `git push origin feature/f031-decision-inbox` — ordered after C4. No `gh` command, no PR action.

## Verification

- G1 exit 0 — branch correct; `git status --porcelain` 0 lines after C0a, C0b, C1, C2 and C3; `.agent/STOP` ABSENT read from disk before C0a and again before C4; the block is sha256 `d6cdc987…679e2cc4`, 24310 bytes, 294 lines at C0a, at C0b and read off disk at C3 — all three EQUAL — and C0a and C0b are the SAME git blob `3ab1efc9a25d`.
- G2 exit 0 — 2 slices printed from the COMMITTED C0a blob by their marker lines; CONTENT 46, TOTAL 294, PROSE 248. PROSE 248 ≤ 400, TOTAL 294 ≤ 490.
- G3 exit 0 — plan at C1 byte-equal to PLANF031R53; the minus-trailing-newline control is FALSE; `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 45, under 50.
- G4 exit 0 — reader 1: 903306 + 1 + 4077 = 907384 and the committed blob is 907384; the pre-C2 blob read exactly the 903306 the block named. Reader 2: N counted by my own script is 1, so paragraph 1 IS also the last; units 368 → 369; the last N units match the slice in order. The one-byte flip inside paragraph 1 is REJECTED by BOTH readers. The tracked file was never mutated — every past revision was read with `git show`.
- G5 exit 0 — before C2 / after C2 / after C3: `^- R-\d+ — ` 263/263/263, `^Done: R-\d+ — ` 8/8/8, `^Landed: R-` 0/0/0, `^Gate: R\d+ — ` 19/19/19, `^Gate: F\d+ R\d+ — ` 33/34/34. Only C2 moved a set: gate key ADDED exactly `F031 R52`, none removed; no id added or removed at either step; ids DISTINCT, maximum `R-0702`; open set 255 before C2 and 255 after C3.
- G6 exit 0 — 25 calls to `buildDecisionResolveCommand(` in `decisionAnswer.test.ts`: 16 pass THREE arguments (the 14 that existed at `e62726c7`, all unmoved, plus 2 new) and 9 pass four. The new parameter is declared `  clarificationAnswers?: Record<string, string>,` — OPTIONAL. `git diff e62726c7..fd6e70a9 -- apps/ui/src/api/decisionAnswer.ts` has 5 deleted lines, NONE matching `decision_id` and NONE matching `answer: trimmedAnswer`; `decisionAnswer.test.ts` has 0 deleted lines, so no test was deleted and none weakened.
- G7 (a) exit 0 — `npx tsc --noEmit`, cwd `apps/ui`, at C3.
- G7 (b) exit 0 — `npx vitest run --root .`, cwd `apps/ui`, at C3: 30 test FILES and 475 TESTS. Files UNCHANGED from the 30 measured at `e62726c7`; tests UP 20 from 455, exactly what S5 adds (11 in `decisionCard.test.ts`, 9 in `decisionAnswer.test.ts`).
- G7 (c) exit 1, NON-ZERO — the model probe in `.remedy-wt/r53-probe-c`: filling `clarifications` with an empty array unconditionally turns 6 tests RED (5 in `decisionCard.test.ts`, 1 in `decisionAnswer.test.ts`), so S5's model tests really do guard S2. Repeated narrowed in `.remedy-wt/r53-probe-c2`: exit 1, 6 failed / 444 passed, against an unmutated control of exit 0, 0 failed / 450 passed. Both worktrees removed by exact path; `git worktree list` back to 1 line.
- G7 (d) exit 1, NON-ZERO — the builder probe in a FRESH `.remedy-wt/r53-probe-d`: dropping the spread so the fourth parameter is ignored turns 5 tests RED, all in `decisionAnswer.test.ts` (carries / keys / drops-blank / trims / trims-edges). Narrowed: exit 1, 5 failed / 445 passed, against the same control of exit 0, 0 failed / 450 passed measured in THAT worktree before it was mutated. Removed by exact path; list back to 1 line.
- G8 exit 0 — both path residues EMPTY against the expected eight paths; `packages/`, `docs/` and `tests/` each EMPTY in `--stat`; `^<<<SLICE ` and `^<<<END ` are 0 and 0 in the plan at C1, live_review at C2 and each of the four `apps/ui` files at C3, against a CONTROL of 2 and 2 over the C0a blob; insertions 294, 194, 16, 2, 351, each commit single-parent and under 500; `git ls-files .remedy-wt` 0 lines; `git worktree list` 1 line at C3; the reflog entries for this round's own five commits all read prefix `commit`, with `amend`, `rebase` and `cherry` 0 each among them.
  THE SUITES, run SERIALLY in the primary checkout at C3, every one a REAL exit 0 and every one EQUAL to the base reading the block quoted: canary 42; `tests/ui_contracts/` 561 passed with 4 skipped — UNMOVED, so no scope drift; `tests/ui_server/` 489; `test_test_runner.py` 52; `test_resource_safety.py` 21; `test_integrity_gate.py` 16.

## Authored-text proofs

Both slices were extracted from the COMMITTED C0a blob by their marker lines, never from the prompt, and applied byte for byte. Disk to disk: `.agent/authored/f031-r53.md` on disk at C3 is byte-identical to the C0a blob and to the C0b blob (sha256 `d6cdc987…679e2cc4`, 24310 bytes, 294 lines). `.agent/plan.md` at C1 equals PLANF031R53 exactly; `.agent/live_review.md` at C2 equals its pre-commit blob plus one newline plus LEDGER53 exactly. The `apps/ui` change is DESCRIBED, not sliced (constraint 1), so no authored text applies to C3.

## Deviations & assumptions

The ordered sequence C0a, C0b, C1, C2, C3, C4 was followed with no extra commit, no dropped commit and no reordering. No finding was registered or resolved, no decision ruled, no `Done:` paragraph written, no slice corrected or reflowed. Three deviations, all inside G7's probes:
1. The ordered command `npx vitest run --root <worktree>/apps/ui` CANNOT RUN as written: a fresh worktree has no `node_modules`, so vitest fails to load the worktree's OWN `vitest.config.ts` with `ERR_MODULE_NOT_FOUND: vitest` and exits 1 having run ZERO tests. I added `--config <primary>/apps/ui/vitest.config.ts` — the identical config file — and the run then reaches the tests.
2. EVEN THEN THE RAW EXIT CODE DOES NOT DISCRIMINATE: at an UNMUTATED worktree that command is STILL exit 1, because `src/components/prompt/promptTraceLens.test.ts` fails to LOAD there for the same missing-`node_modules` reason. I therefore also ran each probe narrowed to `src/api/`, where the unmutated control is a REAL exit 0 over 27 files and 450 tests. Both readings are above; the failing-TEST sets, not the exit codes, are the evidence, and each probe is red only on tests S5 adds.
3. THREE worktrees were created and removed, not two: the narrowed control that makes reading 2 meaningful was first measured in `r53-probe-d` before its mutation, after `r53-probe-c` had already been removed, so probe (c) was repeated in a third worktree `r53-probe-c2`. All three were removed by their exact paths, none was ever in the primary checkout.

## Next

Re-read `.agent/STOP` from disk first; then the Open PR Gate; then review this round's handback; then R54, the COMPONENT half of the FORM.

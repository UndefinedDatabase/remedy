# Handback — F031 Decision inbox, R47 — HANDED BACK EARLY

Branch `feature/f031-decision-inbox`. The round stopped after C7: two EXISTING
tests the block did not order changed turn RED, which constraint 9 and self-drive
G8 make a finding and a hand-back rather than a test to edit.

## Range
Review of a73c137e..c4bad853

## Commits
### d003c4f1 docs(agent): save the F031 R47 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f031-r47.md | +435/-0 | C0a, the block as transported |

### f309c241 docs(agent): mirror the R47 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +389/-180 | C0b, same git blob 2de7c199 as C0a |

### 68e568b4 docs(agent): advance the plan to the F031 R47 door round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +26/-27 | C1, PLANF031R47 applied byte for byte |

### e477457a docs(agent): record the F031 R46 verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C2, LEDGER47 appended |

### 08630a42 docs(agent): land DECISION F031 D24 opening the write door to fp approvals
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +35/-0 | C3, DECISION24 appended |

### 8037f052 test(ui-contracts): retire the duplicate live-region guard R-0696 names
| Path | +/- | Reason |
|---|---|---|
| tests/ui_contracts/test_decision_answer_wiring.py | +0/-11 | C4, S15's single deletion |

### 6728d510 docs(agent): record R-0696 fixed by retiring the duplicate guard
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C5, DONE696 appended |

### d69a1bfb feat(ui-server): dispatch an fp-prefixed decision to the flight plan approval
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ui_server.py | +46/-1 | C6, S1 through S6 |

### c4bad853 feat(decision-queue): offer approve and reject as pending flight plan options
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/decision_queue.py | +9/-0 | C7, S7 and S8 |
| tests/orchestration/test_bundled_clarification.py | +2/-2 | C7, S9's two updates |

C10 rewrites `.agent/handoff.md` alone, at the `+/-` numstat reports: a handoff
cannot table the commit that writes it.

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | R-0696 FIXED here |
| C5 | done | R-0696 recorded here |
| C6 | done | leaves tests/ui_server/ RED — F-A |
| C7 | done | |
| C8 | skipped | S10 turns an existing test RED (F-B); constraint 9 forbids editing it |
| C9 | skipped | S12/S13/S14 all sit behind C8 |
| C10 | done | this handback |
| push | done | `git push origin feature/f031-decision-inbox` |

## Findings raised
- F-A `test_command_channel.py::TestCommandDoorImportGuard::test_the_door_imports_exactly_the_allowed_set`
  FAILS at C6: the two ruled imports `flight_plan.open_clarification_questions`
  and `flight_plan.resolve_flight_plan_approval` are absent from
  `ALLOWED_IMPORTS`. That guard's own comment says an entry "belongs in the same
  commit as the decision that widens it", so C6 owed them and the block did not
  order them.
- F-B `test_decision_inbox.py::test_answerable_key_matches_what_the_write_door_accepts[flight_plan_approval]`
  FAILS as soon as S10 lands: `ANSWERABLE_DECISION_TYPES` is `("task_decision",)`
  while the pending fp card now reads True. A per-TYPE tuple cannot express this
  at all — the RESOLVED `fp:approval` card carries the same type and is NOT
  answerable — so the fix is a spec decision, not a tuple entry.
- Both are the R-0694/0695/0696 root cause the plan's step 2 names: a block
  ordering a change against files it had not read.

## Verification — one line per gate, real exit codes
- G1 exit 0. Branch correct; `git status --porcelain` 0 lines after every commit
  C0a..C7; `.agent/STOP` ABSENT before C0a and before C10. sha256 77cfe894…65c2d8,
  34685 bytes, 435 lines EQUAL across the C0a blob, the C0b blob, both disk copies
  and the reviewer's scratch; C0a and C0b are the same blob 2de7c199.
- G2 exit 0. 4 slices extracted from the C0a blob; CONTENT 83, TOTAL 435, PROSE
  352 (≤400), TOTAL 435 (≤490).
- G3 exit 0. plan.md at C1 byte-equal to PLANF031R47 (2725 bytes); minus-newline
  control FALSE; `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 47 (<50).
- G4 exit 0. C2 863212+1+4361=867574, C3 608934+1+2166=611101, C5
  867574+1+881=868456 — all three identities TRUE. Reader (b): N=1 units 353→354,
  N=6 units 1466→1472, N=1 units 354→355; for both N=1 slices paragraph 1 is also
  the last. The flip inside paragraph 1 was REJECTED by BOTH readers on all three.
  Past blobs read with `git show`; no tracked file was ever mutated.
- G5 exit 0. Before C2 / after C2 / after C3 / after C5 — findings 257/257/257/257,
  Done 5/5/5/6, Landed 0 and `Gate: R` 19 throughout, `Gate: F R` 27/28/28/28.
  ADDED across C2 exactly {`F031 R46`}, across C5 exactly {`R-0696`}; nothing
  REMOVED anywhere. Ids DISTINCT, max R-0696. Open 252 before C2, 251 after C5.
  `^## DECISION F031 D\d+ ` 23 before C3, 24 after.
- G6 exit 0. `^    def test_` 37→36; REMOVED exactly
  {`test_the_region_after_the_button_still_carries_no_conditional_operator`},
  ADDED empty; `jsx_between_answer_button_and_live_paragraph` reads 2 (definition
  plus the keeper's one call); `pytest tests/ui_contracts/ -q` exit 0, 561 passed
  4 skipped — exactly the ordered reading.
- G7 NOT RUN: both mutations are controls over code C8/C9 never wrote. No worktree
  was created; `git worktree list` is 1 line.
- G8 PARTIAL, serial at c4bad853, one pytest process at a time: golden_path 42
  exit 0; **tests/ui_server/ 479 passed 1 FAILED, exit 1** (F-A); test_runner 52
  exit 0; resource_safety 21 exit 0; integrity_gate 16 exit 0; test_decision_inbox
  34 exit 0; test_bundled_clarification 38 exit 0, UNCHANGED as ordered;
  test_decision_answers 29 and test_plan_approval 27, both exit 0 and UNCHANGED —
  S7 changed no CLI semantics. `npx tsc --noEmit` exit 0; `npx vitest run` exit 0,
  30 files 454 tests, unchanged because S14 was skipped.
- G9 exit 0 over what it could cover. Markers 0/0 in plan.md, live_review.md and
  decisions.md against a live CONTROL of 4/4 over the C0a blob. `a73c137e..c4bad853`
  is 9 paths: residue actual-minus-expected EMPTY; residue expected-minus-actual is
  the five paths C8/C9 never reached (decision_inbox.py, test_decision_inbox.py,
  both tests/ui_server/ files, decisionCard.test.ts). Insertions 435, 389, 26, 2,
  35, 0, 2, 46, 11 — each single-parent and under 500. `git ls-files .remedy-wt` 0.
  Reflog SCOPED to these nine commits: every prefix `commit`; amend/rebase/cherry
  0 each.

## Authored-text proofs
All four slices were extracted from the COMMITTED C0a blob by marker line and
applied as bytes, never retyped. PLANF031R47 proved byte-equal at C1; LEDGER47,
DECISION24 and DONE696 each proved twice under G4 with a first-paragraph negative
control. No slice was edited or reflowed.

## R-0696
FIXED at C4 by deleting the NEWER of the duplicate pair; recorded at C5 by
DONE696. Open findings after C5: 251, before the reviewer registers F-A and F-B.

## S12's split, as the block asked it be stated
Not written — C8 and C9 were skipped. The intended split stands for the repair
round: `test_command_channel.py` takes what the door ANSWERS (200 approve, 200
reject, 409 non-pending, 409 on the full CLI line R-0693 measured the browser
posting); `test_command_dispatch.py` takes the EFFECT behind it (the plan really
reads `approved` on disk, and `save_job` ran EXACTLY ONCE — the only guard on S3's
deliberate omission). The two files' own docstrings draw that boundary.

## Deviations & assumptions
- ORDERED SEQUENCE DEPARTED FROM: C8 and C9 were NOT made. C0a..C7 landed in the
  ordered order with no extra, dropped or reordered commit among them.
- C6 is committed and leaves `tests/ui_server/` RED (F-A). I neither reverted it
  nor added the two `ALLOWED_IMPORTS` entries: constraint 9 forbids editing an
  existing test, and reverting an ordered commit is a repair nobody ordered.
- S1 said nothing else in `_dispatch_decision_resolve` changes. Its docstring
  SUMMARY moved from "Answer one task decision and PERSIST it." to "Answer one
  decision and PERSIST it.", because the method now answers two kinds and the old
  sentence would be false on disk. S4 and S6 grew that docstring anyway.
- S3's comment reads "the task-decision path just below" rather than the block's
  "three lines away": `save_job` is nine lines below, so the block's figure would
  have shipped as a false sentence.
- AGENTS.md "If Blocked" item 2 wants the blocker in `.agent/plan.md`. plan.md was
  left exactly as PLANF031R47 wrote it and the blocker is here instead, because
  constraint 4 reserves that file's text to the reviewer this round.
- Process lesson I own: C6 was committed before `tests/ui_server/` was run.
  Running the affected suite first would have caught F-A one commit earlier.
- No worktree created; nothing under `.remedy-wt/` committed; the reviewer's
  scratch original untouched.

## Deviations, declared
This handback measures 185 lines with `wc -l`, against the 100-line tier its nine
tabled commits earn — a DECISION D15 stated-cause overage. The cause is mandated
content: nine per-commit tables, a thirteen-row item-status table, nine gate lines
carrying real exit codes, the two findings this hand-back exists to raise, and the
S12 statement the block ordered by name. No section was dropped to meet the cap.

## Next
Review a73c137e..c4bad853 off disk, then author R48 as a REPAIR round ruling F-A
and F-B — the two `ALLOWED_IMPORTS` entries in that guard's own terms, and how
answerability for `fp:` is expressed once a per-TYPE tuple cannot say it — before
re-ordering C8 and C9. The next session starts at self-drive Phase 1 rule 1
(`.agent/STOP`, ABSENT at this writing) and only then the Open PR Gate.

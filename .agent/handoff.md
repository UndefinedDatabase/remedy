# Handback — F031 Decision inbox, ROUND R43

Branch: `feature/f031-decision-inbox` (never left; no branch created, no force-push,
no amend/rebase/cherry-pick). Deviations, declared: 117 lines against the 100-line
tier — cause is the mandated content itself (8 per-commit tables, an 18-row
item-status table and nine one-line gate rows), per AGENTS.md DECISION D15.

## Range

Review of `5b810e33`..`HEAD` — C0a `02e8563b` through C6, the commit that writes
this file and therefore cannot name its own SHA.

## Commits

### 02e8563b docs(agent): save the F031 R43 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f031-r43.md | +293/-0 | C0a, `shutil.copyfile` of the block |

### 558c7484 docs(agent): mirror the F031 R43 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +224/-232 | C0b, same git blob `2b7bd186` as C0a |

### dfce9f74 docs(agent): point the F031 plan at R43
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +22/-22 | C1, PLANF031R43 byte for byte |

### 758e0344 docs(agent): register the finding the F031 R42 gate raised
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C2, FINDINGS43 appended (R-0694) |

### a9b0d29f docs(agent): record the F031 R42 verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C3, LEDGER43 appended (`Gate: F031 R42`) |

### 7cbff830 docs(agent): land DECISION F031 D20 splitting the D19 programme
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +22/-0 | C4, DECISION20 appended |

### f86c0b8f feat(orchestration): derive whether the write door can answer a decision card
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/decision_inbox.py | +34/-4 | C5, S1–S5 |
| tests/orchestration/test_decision_inbox.py | +31/-3 | C5, S6–S8 |

### C6 (this commit) docs(agent): write the F031 R43 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | whole-file rewrite | C6 cannot table itself (R-0149 pattern) |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | this file |
| S1 | done | decision_inbox.py:29 `find_task_decision` import; acyclic, verified |
| S2 | done | decision_inbox.py:75-96, body is the `is not None` expression alone |
| S3 | done | decision_inbox.py:88-94, the deliberate absence in as many words |
| S4 | done | decision_inbox.py:122-124, third key, existing two unchanged |
| S5 | done | 2 stale sentences found in that file: line 6 module docstring, line 106 `build_decision_inbox` docstring; both corrected. Post-C5 sweep for `two`/standalone `2` in decision_inbox.py returns 0 lines |
| S6 | done | test file:281 comment, 285 rename to `..._plus_exactly_three`, 288-292 expected set |
| S7 | done | test file:39-43 `ANSWERABLE_DECISION_TYPES`, 310-318 the parametrized test over the existing `PRODUCING_FIXTURES`; no new fixture |
| S8 | done | test file:179-180 presence + `isinstance(..., bool)` |
| S9 | done | diff shows no other change; no test deleted, no assertion weakened |
| push | done | `git push origin feature/f031-decision-inbox` after C6 |

## External actions

- `git worktree add .remedy-wt/r43-mut f86c0b8f` — created for G7 only.
- `git worktree remove .remedy-wt/r43-mut` — removed by exact path; `git worktree list` 1 line.
- `git push origin feature/f031-decision-inbox` after C6. No PR create/edit/merge, no `gh`.

## Verification

- G1 exit 0 — branch correct; `git status --porcelain` 0 lines after C0a/C0b/C1/C2/C3/C4/C5; `.agent/STOP` ABSENT before C0a and before C6. Block at C0a, at C0b and off disk at C5 all sha256 `e75fd033eea7922a3d4c222c906a9ce3f84b7f0697aefaf314a54d566a3d4c70`, 26648 bytes, 293 lines — all three EQUAL; C0a and C0b are the SAME git blob `2b7bd186`.
- G2 exit 0 — extractor printed 4 slices from the committed C0a blob. TOTAL 293, CONTENT 72, PROSE 221 (markers counted as prose). 221 ≤ 400, 293 ≤ 490.
- G3 exit 0 — `.agent/plan.md` at C1 byte-equal to PLANF031R43 TRUE (newline-included); minus-trailing-newline control FALSE; `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 49 (< 50).
- G4 exit 0 — C2: 834598 + 1 + 2735 = 837334, reader A TRUE, N=1, units 346→347, reader B TRUE. C3: 837334 + 1 + 4159 = 841494, reader A TRUE, N=1, units 347→348, reader B TRUE. C4: 602495 + 1 + 1427 = 603923, reader A TRUE, N=4, units 1446→1450, reader B TRUE. N counted by my script, never read from the block. Negative control (one byte flipped in memory in appended paragraph 1) REJECTED by BOTH readers on all three. For FINDINGS43 and LEDGER43 N is 1, so paragraph 1 is also the last. No tracked file mutated.
- G5 exit 0 — `^- R-\d+ — ` 254 → 255 → 255, ADDED across C2 exactly {R-0694}, REMOVED empty, none added/removed at C3; all ids DISTINCT, max `R-0694`. `^Done: R-\d+ — ` 5, `^Landed: R-` 0, `^Gate: R\d+ — ` 19 at all three points. `^Gate: F\d+ R\d+ — ` 23 → 23 → 24, ADDED key exactly `F031 R42`. Open set 249 before C2, 250 after C3. `^## DECISION F031 D\d+ ` 19 before C4, 20 after.
- G6 exit 0 — S1–S9 all DONE with file:line above. Sweep of decision_inbox.py at C5 for `two` or standalone `2`: 0 lines. `python3 -m ruff check` on both changed files REAL exit 0, "All checks passed!". `assert` statements in the test file (AST count) 18 before, 21 after.
- G7 exit 0 primary / 1 + 1 mutated — primary at C5: `pytest tests/orchestration/test_decision_inbox.py -q` REAL exit 0, 33 passed (25 at `5b810e33`). Mutation (a) helper returns True unconditionally: REAL exit 1, 7 failed / 26 passed, FAILED `test_answerable_key_matches_what_the_write_door_accepts[{patch_approval,stop_reason,test_failure,repo_dirty,token_budget,memory_review,flight_plan_approval}]`. Mutation (b) S4 assignment deleted: REAL exit 1, 17 failed / 16 passed, FAILED all 8 `test_card_appears_for_each_producing_type[...]`, `test_card_keys_are_the_export_keys_plus_exactly_three`, and all 8 `test_answerable_key_matches_what_the_write_door_accepts[...]`. Both ran only in `.remedy-wt/r43-mut`, restored between them (byte-equality re-checked TRUE both times).
- G8 exit 0 — `^<<<SLICE `/`^<<<END ` are 0/0 in plan.md@C1, live_review.md@C3, decisions.md@C4 and BOTH files C5 touches, against a live CONTROL of 4/4 over the C0a blob. `git diff --name-only 59521bf5..f86c0b8f` is 10 paths; range MINUS expected union = [], union MINUS range = [] — exact both ways. Insertions 293, 224, 22, 2, 2, 22, 65 — each single-parent and under 500. `git ls-files .remedy-wt` 0; `git worktree list` 1 line at C5 after removal. Every reflog entry for the 7 commits reads `commit:`; `amend` 0, `rebase` 0, `cherry` 0.
- G9 exit 0 — serially in the primary checkout at C5, one pytest process at a time: `tests/ui_server/` 480 passed; `tests/orchestration/test_test_runner.py` 52 passed; `tests/regression/test_resource_safety.py` 21 passed; `tests/orchestration/test_integrity_gate.py` 16 passed; canary `tests/cli/test_golden_path.py` 42 passed; `tests/ui_contracts/` 556 passed, 4 skipped. Every one REAL exit 0 and identical to the `5b810e33` baseline. NO RED — the unreproduced `test_test_runner.py` red the reviewer saw in dry runs did not recur, so no five-times re-run was triggered.

## Authored-text proofs

Disk-to-disk against the COMMITTED `.agent/authored/f031-r43.md` blob (`2b7bd186`), never the prompt:
- PLANF031R43 → `.agent/plan.md` at C1: byte-equal TRUE, negative control FALSE.
- FINDINGS43 → `.agent/live_review.md` at C2: appended exactly, both readers TRUE, flip REJECTED.
- LEDGER43 → `.agent/live_review.md` at C3: appended exactly, both readers TRUE, flip REJECTED.
- DECISION20 → `.agent/decisions.md` at C4: appended exactly, both readers TRUE, flip REJECTED.
- The C5 Python is authored to section S's SPEC, not sliced. No slice was retyped, reflowed or corrected.

## Deviations & assumptions

- No departure from the ordered commit sequence: C0a, C0b, C1, C2, C3, C4, C5, C6 landed in that order, no extra commit, none dropped, none reordered.
- BLOCK TEXT DISCREPANCY, reported not corrected: constraint 2 says "the five marked SLICES", but the block carries FOUR (PLANF031R43, FINDINGS43, LEDGER43, DECISION20) and my extractor printed 4 against a CONTROL of 4/4 markers. The bundle line and the `Change:` list are consistent with four; I applied four and changed nothing.
- R-0694: REGISTERED at C2 as Low — a fix clause saying "binding on the next block" that lives only in ledger prose, so R42's block did not apply R-0631's clause. It is deliberately NOT FIXED here: the repair is a new item in `docs/agents/planner_reviewer_prompt.md` §3, which is the reviewer's own file and is not in this round's change set. R43's G4 applied R-0631's clause by hand instead.
- Open findings after C3: 250 (255 `^- R-\d+ — ` minus 5 `^Done: R-\d+ — `).

## Next

Re-read `.agent/STOP` from disk FIRST; then the Open PR Gate; then review this
round's handback; then R44 — the browser half of DECISION F031 D19: the model
field and the card that renders no button the door refuses.

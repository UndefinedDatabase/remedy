# Handback — F031 Decision inbox, ROUND R44

Branch: `feature/f031-decision-inbox`. Range: Review of `46ae059f`..HEAD (C6).
Block `.agent/authored/f031-r44.md`: sha256 `87e21495a88fef3c7aed52b8a6ec42f5a96e49859d4cda083cf04177d481275f`, 28458 bytes, 300 lines.

## Commits

### 3f308748 docs(agent): save the F031 R44 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f031-r44.md | +300/-0 | C0a — the reviewer's block, byte for byte |

### 0206d71a docs(agent): mirror the F031 R44 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +194/-187 | C0b — same bytes, same git blob as C0a |

### 0cbf4911 docs(agent): make the plan current for F031 R44
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +20/-22 | C1 — PLANF031R44 replaces the file whole |

### d886c49e docs(agent): register the F031 R44 finding R-0695
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C2 — FINDINGS44 appended |

### cfef2a48 docs(agent): record the F031 R43 verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C3 — LEDGER44 appended |

### 862bdea2 docs(agent): land DECISION F031 D21
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +28/-0 | C4 — DECISION21 appended |

### 50e97f81 fix(orchestration): answerability key mirrors the door OPEN refusal
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/decision_inbox.py | +28/-16 | C5 — S1–S5, the OPEN condition |
| tests/orchestration/test_decision_inbox.py | +31/-1 | C5 — S6, the discriminating test |

### C6 docs(agent): write the F031 R44 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | self-referential (R-0149 pattern) | C6 — this file; its numstat cannot exist before it is written, and G1–G9 all ran strictly earlier |

## External actions
`git worktree add --detach .remedy-wt/f031-r44-g7 50e97f81` — created for G7; `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/f031-r44-g7` — removed by exact path, `git worktree list` back to 1 line. `git push origin feature/f031-decision-inbox` after C6 (its reading is not written here, per the block).

## Verification — one line per gate, REAL exit codes
- G1 exit 0 — `git status --porcelain` 0 lines after C0a, C0b, C1, C2, C3, C4, C5; `.agent/STOP` ABSENT before C0a and before C6; C0a blob = C0b blob = disk@C5 = sha256 `87e21495…d481275f`, 28458 bytes, 300 lines, SAME git blob `d84e4272`.
- G2 exit 0 — extractor over the COMMITTED C0a blob printed 4 slices; CONTENT 76, TOTAL 300, PROSE 224 (≤400), TOTAL ≤490.
- G3 exit 0 — plan@C1 byte-equal to PLANF031R44 (newline-included) TRUE; minus-trailing-newline control FALSE; `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 47 (<50).
- G4 exit 0 — 841494+1+3235=844730, 844730+1+4888=849619, 603923+1+1809=605733, all three identities TRUE; reader 2 N=1, 1, 5 (script-counted), units 348→349→350 and 1450→1455, last-N in order equal; N=1 for both ledger slices so paragraph 1 is also the last; byte flip in paragraph 1 REJECTED by BOTH readers on all three; no tracked file mutated.
- G5 exit 0 — `^- R-\d+ — ` 255→256→256, ADDED {R-0695} at C2 and none REMOVED; `^Gate: F\d+ R\d+ — ` 24→24→25, ADDED {F031 R43} at C3; `^Done: R-\d+ — ` 5, `^Landed: R-` 0, `^Gate: R\d+ — ` 19 throughout; ids DISTINCT, max R-0695; open set 250 before C2, 251 after C3; `^## DECISION F031 D\d+ ` 20→21.
- G6 exit 0 — S1 DONE decision_inbox.py:29-32; S2 DONE :107-108; S3 DONE :80-93; S4 DONE :95-105; S5 DONE — C5's diff on that file holds exactly TWO hunks, `@@ -26,7 +26,10 @@` and `@@ -75,25 +78,34 @@`, and an AST comparison of C4 vs C5 shows module docstring UNCHANGED and `build_decision_inbox` source UNCHANGED; S6 DONE test file :24-27 and :324-348; S7 DONE — no function removed, `ANSWERABLE_DECISION_TYPES` unchanged. `python3 -m ruff check` on both files REAL exit 0 ("All checks passed!"). AST `assert` count 21 → 27.
- G7 primary exit 0 — `pytest tests/orchestration/test_decision_inbox.py -q` 34 collected, 34 passed (33 at 46ae059f). In the disposable worktree: (a) red control, existence-only return, REAL exit 1, "1 failed, 33 passed", FAILED `tests/orchestration/test_decision_inbox.py::test_answerable_key_goes_false_once_the_decision_has_been_answered`; (b) return True unconditionally, REAL exit 1, "8 failed, 26 passed", FAILED the 7 non-`task_decision` params of `test_answerable_key_matches_what_the_write_door_accepts` plus the new test; (c) return False unconditionally, REAL exit 1, "2 failed, 32 passed", FAILED `…test_answerable_key_matches_what_the_write_door_accepts[task_decision]` and the new test. Tree restored byte-equal after each; worktree porcelain 0.
- G8 exit 0 — `^<<<SLICE `/`^<<<END ` 0/0 in plan@C1, live_review@C3, decisions@C4 and BOTH files C5 touches, against a live CONTROL of 4/4 over the C0a blob; `git diff --name-only 46ae059f..50e97f81` equals the expected 7-path set BOTH WAYS; insertions 300, 194, 20, 2, 2, 28, 59 — each single-parent and under 500; `git ls-files .remedy-wt` 0; `git worktree list` 1 line; all 7 reflog entries for THIS round read `commit:`, with `amend`/`rebase`/`cherry` 0 each among them.
- G9 exit 0 (all six, run SERIALLY in the primary checkout) — `tests/ui_server/` 480 passed; `tests/orchestration/test_test_runner.py` 52 passed; `tests/regression/test_resource_safety.py` 21 passed; `tests/orchestration/test_integrity_gate.py` 16 passed; canary `tests/cli/test_golden_path.py` 42 passed; `tests/ui_contracts/` 556 passed, 4 skipped — every reading identical to the `46ae059f` baseline, no red, no FAILED node id.

## Authored-text proofs
Four slices, extracted from the COMMITTED C0a blob by marker line and applied BYTE FOR BYTE: PLANF031R44 (whole-file replace), FINDINGS44, LEDGER44, DECISION21 (appends of existing bytes + exactly one newline + slice). Every identity proved in G3/G4. C0a and C0b are the same git blob as the reviewer's `.remedy-wt/f031-r44-block.md`, which was left in place.

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
| C6 | done | this commit |
| S1 | done | |
| S2 | done | |
| S3 | done | |
| S4 | done | |
| S5 | done | proved by AST equality, not by the word |
| S6 | done | |
| S7 | done | |
| push | done | ordered after C6; its reading is not recorded here |

## R-0695
Registered at C2 as Medium: `answerable_by_decision_resolve` reported True for an already-answered task decision, which `_dispatch_decision_resolve` refuses 409 `rejected_state`. Its CODE half LANDED at C5 — the helper now tests EXISTENCE and `ESCALATION_STATUS_OPEN`, and the new test pins the True→False transition. Its PROCESS half — the `docs/agents/planner_reviewer_prompt.md` §3 item it shares with R-0694 — is NOT in this round's change set and stays OPEN.

Open findings: 251 (`^- R-\d+ — ` 256 minus `^Done: R-\d+ — ` 5).

## Deviations & assumptions
Commit sequence executed exactly as ordered: C0a, C0b, C1, C2, C3, C4, C5, C6 — no extra commit, none dropped, none reordered. No slice was corrected; nothing in the block read as wrong to me. No file under `apps/` or `docs/` was touched. Nothing under `.remedy-wt/` is committed and the reviewer's block copy was not deleted.

No DECISION D15 overage is declared: 8 commits earn the 100-line cap and this file measures under it with every mandated section present.

## Next
1. Re-read `.agent/STOP` from disk (Phase 1 rule 1). 2. The Open PR Gate. 3. Review this round's handback and the `46ae059f`..HEAD diff. 4. Then R45 — the browser half of D19: `DecisionCardModel` gains the field and `DecisionInboxCard` renders no button for a card the door refuses.

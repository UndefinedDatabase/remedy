# Handback — F031 Decision inbox, round R41 (record and hand off)

Branch: `feature/f031-decision-inbox`. Base `3afdb209`, tip at C3 `51a1b735`.
Open findings: 247.

## Range

Review of `3afdb209`..`HEAD`.

## Commits

### 0cdbda3a docs(agent): save the F031 R41 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f031-r41.md | +184/-0 | C0a — the block saved byte for byte |

### 818efadf docs(agent): mirror the F031 R41 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +112/-169 | C0b — mirrored by `git show`, same blob `491e5cd3` |

### 813aa914 docs(agent): point the F031 plan at R41
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +17/-14 | C1 — PLANF031R41 applied byte for byte |

### 0296a02f docs(agent): register the finding the F031 R40 gate raised
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C2 — FINDINGS41 appended: R-0691 |

### 51a1b735 docs(agent): record the F031 R40 verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C3 — LEDGER41 appended: `Gate: F031 R40` |

### C4 (this commit — a handoff cannot table itself, R-0149)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | self-reference | C4 — this rewrite |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | applied byte for byte; the slice is 51 lines — see Deviations |
| C2 | done | |
| C3 | done | |
| C4 | done | this commit |
| push | done | ordered after C4; its reading belongs to the next gate |

## The finding

- R-0691 — REGISTERED at C2, deliberately NOT FIXED this round. Low: `test_the_add_helper_adds_the_passed_key_and_nothing_else` and its remover twin name a completeness claim while the predicate underneath is a containment claim — a presence check plus an exclusion list cannot see a second, foreign `add`. No code and no test file was touched here. Constraint 4 and the PLANF031R41 slice route the repair — a rename of both assertions plus a residual note in the class docstring — to the integration-gate round.

## External actions

No worktree was created this round, so none was removed; `git worktree list` reads 1 line throughout. Push of `feature/f031-decision-inbox` after C4 — the block leaves its reading to the next gate. No PR and no `gh` action this round.

## Verification

- G1 exit 0 — branch `feature/f031-decision-inbox`; `git status --porcelain` 0 lines after each of C0a/C0b/C1/C2/C3; `.agent/STOP` read from disk ABSENT before C0a and again before C4; block sha256 `0a70adced995e7ed78d9d14cdd91ea660f13192ea77413918ca50dab8fe4fe38`, 20004 bytes, 184 lines — EQUAL as saved at C0a, as mirrored at C0b and as read off disk at C3; C0a and C0b are the SAME git blob `491e5cd3`.
- G2 exit 0 — 3 slices printed from the COMMITTED C0a blob by marker line (PLANF031R41 51, FINDINGS41 1, LEDGER41 1); TOTAL 184, CONTENT 53, PROSE 131. My extractor counts `<<<SLICE`/`<<<END` as PROSE, the convention R40's two readers agreed on. 131 <= 400, 184 <= 490.
- G3 exit 0 on every byte check, FAILED on its line sub-check — `.agent/plan.md` at `813aa914` is BYTE-EQUAL to PLANF031R41 newline-included at 3002 bytes; minus-trailing-newline control FALSE; `^## Goal$` 1, `^## Next Steps$` 1; `wc -l` 51, which is NOT strictly under 50. The slice as authored is 51 lines, so that sub-check is unmeetable without editing the slice. Constraint 1 forbids that. Declared below, not corrected.
- G4 exit 0 — C2: 817669 + 1 + 2338 = 820008 against actual 820008, pre-commit blob a byte-exact prefix, whole-file byte identity TRUE; reader B units 341 -> 342, last unit equals FINDINGS41's paragraph. C3: 820008 + 1 + 5653 = 825662 against actual 825662, prefix TRUE, identity TRUE; units 342 -> 343, last unit equals LEDGER41's paragraph. BOTH slices are ONE paragraph, so an in-slice ordered swap is the identity for each and is declared degenerate, not reported as a passing control; the CROSS-SLICE swap is FALSE both ways — FINDINGS41's paragraph is not the last unit at C3 and LEDGER41's is not the last unit at C2. One in-memory byte flip per append: BOTH readers REJECT, for each. The tracked file was never mutated.
- G5 exit 0 — `^- R-\d+ — ` 251 -> 252 -> 252; ADDED across C2 exactly {`R-0691`}, ADDED across C3 EMPTY, REMOVED EMPTY at both, all ids DISTINCT at all three points, maximum `R-0690` before C2 and `R-0691` after. `^Done: R-\d+ — ` 5, `^Landed: R-` 0, `^Gate: R\d+ — ` 19 at all three. `^Gate: F\d+ R\d+ — ` 21 -> 21 -> 22, ADDED key exactly `F031 R40`. Open set 246 before C2, 247 after C3.
- G6 exit 0 — `^<<<SLICE ` and `^<<<END ` are 0 and 0 in the plan at `813aa914` and in the ledger at `51a1b735`, against a live CONTROL of 3 and 3 over the C0a blob. `git diff --name-only 3afdb209..51a1b735` = 4 paths, ALL under `.agent/`; range-minus-declared EMPTY, declared-minus-range = {`.agent/handoff.md`} alone, which C4 writes. Insertions 184, 112, 17, 2, 2 — each single-parent, each under 500. `git ls-files .remedy-wt` 0 lines; `git worktree list` 1 line. Reflog: all five prefixes read `commit`; `amend` 0, `rebase` 0, `cherry` 0.
- G7 exit 0 for each, run SERIALLY in the PRIMARY checkout at C3, one pytest process alive at a time — `tests/ui_server/` 480 passed; `tests/orchestration/test_test_runner.py` 52; `tests/regression/test_resource_safety.py` 21; `tests/orchestration/test_integrity_gate.py` 16; canary `tests/cli/test_golden_path.py` 42; `tests/ui_contracts/` 556 passed with 4 skipped. Every reading is IDENTICAL to the `3afdb209` baseline the block states. Nothing moved, as a round that adds no test must show.

## Authored-text proofs

All three slices were extracted from the COMMITTED C0a blob `491e5cd3` by their marker LINES, never from the prompt, and applied byte for byte — PLANF031R41 written whole, FINDINGS41 and LEDGER41 by a byte append of one `\n` plus the slice. `.agent/last_block.md` was produced by `git show HEAD:.agent/authored/f031-r41.md` and never retyped. Disk-to-disk equality against the committed `.agent/authored/f031-r41.md` is proved under G1, G3 and G4. Nothing was retyped, reflowed or corrected.

## Deviations & assumptions

- The ordered sequence C0a, C0b, C1, C2, C3, C4 was followed exactly: no extra commit, none dropped, none reordered.
- THE PLAN SLICE AND ITS OWN GATE CONFLICT, and the conflict is reported rather than resolved. PLANF031R41 as authored is 51 content lines; G3 requires `.agent/plan.md` at C1 to be BOTH byte-equal to that slice AND strictly under 50 lines by `wc -l`, and those two cannot both hold. AGENTS.md's `.agent/plan.md` rule ("keep it short (<50 lines)") is also at 51. Constraint 1 says a slice that looks wrong is reported, never corrected, because a corrected slice destroys the transport proof — so the slice shipped byte for byte and `.agent/plan.md` is 51 lines. The growth over PLANF031R40's 48 is +1 in `## Current Step`, +1 in `## Next Steps` item 2 and +2 in the first `## Risks` bullet. Trimming any one of those four lines would bring the file to 50 and still not be under 50; the smallest correction that satisfies both is -2 lines, and it is the author's to make.
- No file outside `.agent/` was touched. The change set is 4 paths over `3afdb209`..`51a1b735`, all under `.agent/`, and the fifth declared path `.agent/handoff.md` is this commit.
- No worktree was created, so no removal was performed; `.remedy-wt/` holds nothing from this round and `git ls-files .remedy-wt` is 0.

## Next

Re-read `.agent/STOP` from disk FIRST — it was ABSENT at both readings this round, but Phase 0 is one-shot while G6 of the protocol binds at any point. Then run the Open PR Gate (`gh pr list --state open ...`). Then review this round's handback and re-run G1 through G7 off disk to issue the R41 verdict, ruling on the G3 plan-length conflict declared above. Then the clarification FORM round. That order is Phase 1 of docs/agents/self_drive_protocol.md.

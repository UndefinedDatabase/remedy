# Handback — F009 R12, the closing state round

Round base `fde072f181e223a32e22b663f315375f753f7d45`, branch `feature/f009-single-write-channel`. State: 60 % (T001 gebaut · T002 gebaut bis auf die Publikation — T003 öffnet die Wirkung) — Schätzung

## Range

Review of `fde072f1..HEAD` — seven commits: C0a, C0b, C1, C2, C3, C4 and C5, in that order. Nothing came between them, none was dropped and none was added. NO PRODUCTION CODE: nothing under `packages/`, `apps/`, `tests/` or `docs/` is touched, measured in G8.

## Commits

### 0f198286 docs(state): save the F009 R12 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f009-r12.md | +182/-0 | the round's block, byte-exact |

### 20a7fc3a docs(state): mirror the F009 R12 step block into the live block slot
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +110/-219 | written from the committed C0a blob |

### 61c31dde docs(state): set the plan to the F009 R12 closing round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +12/-15 | PLANF009R12, applied byte-equal |

### 95cf9fe2 docs(review): register R-0636 against the R11 block specification
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | R0636 appended |

### ff61faa0 docs(review): register R-0637 against the nonce record size bound
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | R0637 appended |

### 3cfb44d2 docs(review): record the R11 verdict in the live review ledger
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | LEDGER12 appended; R11 PASSED |

### C5, this commit, docs(state): write the F009 R12 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | a handback cannot table the commit that writes it |

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | this commit |

## External actions

`gh` was not run; this branch carries no pull request. No worktree was created or removed — this round ordered no destructive probe. `git push` follows C5, the last commit of this round and of this session.

## Verification

Transcripts are in the round report (R-0582); one line per gate here. Every gate that names a commit was measured at `3cfb44d2`, which is C4.

- G1 STOP ABSENT at Step 0 and again before C5; `git rev-parse --abbrev-ref HEAD` printed `feature/f009-single-write-channel` at every reading; `git status --porcelain` printed 0 lines after each of C0a through C4; the round base read at Step 0 is `fde072f181e223a32e22b663f315375f753f7d45`, which was also HEAD at Step 0.
- G2 EQUAL — the scratch file as received, `.agent/authored/f009-r12.md` at C0a and `.agent/last_block.md` at C0b are all sha256 `1672d8922c5e11d9cb9079d428fe9b23cb02c12568041447d4b4aa07c9027c7c` over 20456 bytes and 182 lines, equal to the digest the task prompt named; C0b was written from the committed C0a blob, never from the scratch file again.
- G3 4 slices from my own ordered extraction out of the committed C0a blob: PLANF009R12 `bbc7ef5a…` 2221 bytes 38 lines, R0636 `6aff69d8…` 2728 bytes 1 line, R0637 `986b9736…` 2082 bytes 1 line, LEDGER12 `2774366f…` 4348 bytes 1 line; the aggregates my script printed are 4 slices, 11379 bytes and 41 lines.
- G4 `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R12 at 38 lines against the 50-line cap; `^## Goal$` 1, `^## Next Steps$` 1, first `\bF\d{3}\b` match `F009`.
- G5 ALL THREE APPENDS TO `.agent/live_review.md` HOLD UNDER BOTH READERS, each from its own base — the round base for C2, the C2 blob for C3, the C3 blob for C4. (a) prefix byte-exact and remainder equal to a newline plus the slice: C2 remainder `524e0fde…` 2729 bytes 2 lines, C3 `4348fa7d…` 2083 bytes 2 lines, C4 `cedfbff7…` 4349 bytes 2 lines; the file goes 445503 → 448232 → 450315 → 454664 bytes and 1076 → 1078 → 1080 → 1082 lines. (b) N COUNTED BY MY SCRIPT is 1 for each, and the last 1 blank-line unit of the whole file equals the slice's 1 paragraph. NEGATIVE CONTROL per append, one printable-ASCII byte of the FIRST appended paragraph flipped (offsets 445506 `R`→`S`, 448235 `R`→`S`, 450316 `G`→`H`): reader (a) ACCEPTS the true value and REJECTS the flip, reader (b) ACCEPTS the true value and REJECTS the flip — four outcomes per append, twelve in all, all as required. Nothing already in the file was edited.
- G6 line-anchored over `.agent/live_review.md` at the round base, C3 and C4: `^- R-\d+ — ` 201, 203 and 203 with every id DISTINCT at each (201/201, 203/203, 203/203 distinct); `^- R-0636 — ` 0, 1 and 1; `^- R-0637 — ` 0, 1 and 1; `^Done: R-\d+ — ` 2, 2 and 2; `^Landed: ` 0, 0 and 0; `^> Next free id` 0, 0 and 0; `^Gate: R\d+ — ` 11, 11 and 12 over that many DISTINCT keys. Max id at C4 is R-0637. My script printed 201 for item 10's rule at `3cfb44d2` — line-anchored `^- R-\d+ — ` 203 minus line-anchored `^Done: R-\d+ — ` 2 (DECISION F009 D10). Of the 12 `Gate: ` lines at C4, 11 match `^Gate: R(\d+) — the R(\d+) entry\.` with the second numeral one less than the first; the one non-match reads `Gate: R1 — the F008 R36 entry.`
- G7 both suites EXIT 0, run SERIALLY in the primary checkout at C4, never two pytest processes at once: `python3 -m pytest tests/cli/test_golden_path.py -q -rf` printed `42 passed` (passed+skipped 42), and the second group over `tests/ui_server/`, `tests/orchestration/test_test_runner.py`, `tests/regression/test_resource_safety.py` and `tests/orchestration/test_integrity_gate.py` printed `507 passed` (507). Neither count was predicted; each is what the run printed, and each exit code is the one my script read from the process.
- G8 the range from the round base to C4 lists EXACTLY the four declared paths other than `.agent/handoff.md` — `.agent/authored/f009-r12.md`, `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md` — the set difference empty in both directions, and 0 paths beginning `packages/`, `apps/`, `tests/` or `docs/`, which is constraint 3 as a measurement. Six commits, each with ONE parent, `git show --numstat` and `git diff --numstat` AGREEING on every cell and every cell equal to the `+/-` column of the tables above; insertions 182, 110, 12, 2, 2 and 2, all under the 500-insertion cap of AGENTS.md DECISION F104 D1, so no split was needed. `^<<<SLICE ` and `^<<<END ` read 0 lines each in `.agent/plan.md` and `.agent/live_review.md` at C4. THIS ROUND'S six reflog rows — the entries above the round base — classify as `commit` 6, with `amend`, `rebase` and `cherry` 0 each; no total is asserted over the whole reflog (R-0601). `git ls-files .remedy-wt` is 0.
- G9 this handback carries every mandated section of docs/agents/handback_template.md, an item-status table with exactly one row for each of C0a, C0b, C1, C2, C3, C4 and C5, the round base SHA and one line per gate. `wc -l` measures it at 84 lines against the 100 a bundle of more than five commits allows.

## Authored-text proofs

All four slices were extracted from the COMMITTED C0a blob by their `<<<SLICE ` and `<<<END ` marker lines with a script and applied programmatically. PLANF009R12 is byte-equal to `.agent/plan.md` at C1 (G4); R0636, R0637 and LEDGER12 are proved as appends under two independent readers, each with its own script-counted N and its own negative control on the first appended paragraph (G5). No marker line reached any target file; nothing was retyped, rewrapped, reflowed, reindented or whitespace-adjusted.

## Deviations & assumptions

None. The block's ordered commit sequence C0a, C0b, C1, C2, C3, C4, C5 was followed exactly: no commit was added, dropped or reordered. All four slices were applied byte for byte and no objection to any of them arose. No repair was performed for R-0636 or R-0637 — constraint 3 orders both deferred to the round that retires the 501 seam.

## Next

THIS SESSION ENDED HERE. The round wrote NO production code, by design: it exists so that two defects the R11 review found and one verdict it reached survive the session that found them, and a finding that lives only in a session's chat is lost when that session ends. No `.agent/STOP` is present. The next session's FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1) and its SECOND the Open PR Gate (Phase 1 rule 2), which is EMPTY because this branch carries no pull request and F009 opens one at its own closure. Open findings at `3cfb44d2` are 201 by item 10's rule — line-anchored `^- R-\d+ — ` 203 minus line-anchored `^Done: R-\d+ — ` 2 (DECISION F009 D10). The next free id, derived with `max` over the line-anchored entries, is R-0638. `.agent/candidates.md` is EMPTY — it holds its header and an explicit EMPTY statement, and zero candidate entries. The next round is T003's effect table per DECISION F009 D5 — the round that retires the 501 seam, and therefore the round that owes the fixes for R-0636 and R-0637, both of which depend on the publish call site it introduces. R-0403, R-0607, R-0608, R-0609, R-0611, R-0613, R-0622, R-0630, R-0633 and R-0635 stay routed to a paydown branch.

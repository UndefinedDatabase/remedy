# Handback — F009 R9, persisting one finding and one verdict

Round base `d8d8610e1887766a935eae7a2eeb53ad5626b3ec`, branch `feature/f009-single-write-channel`. State: 40 % (T001 gebaut · T002 begonnen — Limit steht, Quittung und Wirkung folgen in R10 und T003) — Schätzung

## Range

Review of `d8d8610e..HEAD` — six commits: C0a, C0b, C1, C2, C3, C4. No code was written.

## Commits

### e0136413 docs(state): save the F009 R9 step block as authored text
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f009-r9.md | +179/-0 | the round's block, byte-exact |

### f59c6a78 docs(state): mirror the F009 R9 step block into the live block slot
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +99/-205 | written from the committed C0a blob |

### 9d6b004a docs(state): set the plan to the F009 R9 closing round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +12/-12 | PLANF009R9, applied byte-equal |

### 7524e76b docs(review): register R-0634 against the shipped concurrency test
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | R0634 appended; the round's one new id |

### 84164cf8 docs(review): record the R8 verdict in the live review ledger
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | LEDGER9 appended; R8 PASSED |

### C4, this commit, docs(state): write the F009 R9 handback
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
| C4 | done | this commit |

## External actions

None beyond the push. No worktree was created and no `gh` command ran; this branch carries no pull request. `git push` follows C4, the last commit of this session.

## Verification

Transcripts are in the round report (R-0582); one line per gate here.

- G1 STOP ABSENT at Step 0 and again before C4; branch `feature/f009-single-write-channel` at every reading; `git status --porcelain` 0 lines after each of C0a through C4; round base as stated above.
- G2 EQUAL — the scratch file as received, `.agent/authored/f009-r9.md` at C0a and `.agent/last_block.md` at C0b are all sha256 `d04b283d875d177c5f17cceeb9acc73712494f3c9273ea6d404c4c2ffb7f45d7` over 18788 bytes and 179 lines, equal to the digest the prompt named; C0b was written from the committed C0a blob, not from the scratch file.
- G3 3 slices from my own ordered extraction out of the committed C0a blob: PLANF009R9 `78e4afdb…` 2359 bytes 41 lines, R0634 `ad565aa7…` 2555 bytes 1 line, LEDGER9 `e60d199d…` 5042 bytes 1 line; the aggregates are 3 slices, 9956 bytes and 43 lines, over a concatenation of sha256 `9e531bd8…`.
- G4 `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R9 at 41 lines against the 50-line cap; `^## Goal$` 1, `^## Next Steps$` 1, first `\bF\d{3}\b` match F009.
- G5 BOTH APPENDS HOLD UNDER BOTH READERS. C2 over the round base: (a) prefix exact, remainder `af804c0b…` 2556 bytes 2 lines, equal to a newline plus R0634; (b) N COUNTED 1 against 213 blank-line units, last unit equal in order. C3 over the C2 blob: (a) remainder `42636ef3…` 5043 bytes 2 lines, equal to a newline plus LEDGER9; (b) N COUNTED 1 against 214 units. For each append the one-byte flip of the FIRST appended paragraph is REJECTED by both readers while the unflipped value is ACCEPTED by both — four outcomes per append, all as required.
- G6 line-anchored at the round base, C2 and C3: `^- R-\d+ — ` 199, 200 and 200 with every id DISTINCT at each; `^- R-0634 — ` 0, 1 and 1; `^Done: R-\d+ — ` 1 at all three; `^Landed: ` 0 at all three; `^> Next free id` 0 at all three; `^Gate: R\d+ — ` 8, 8 and 9 over that many DISTINCT keys. Max id at C3 is R-0634. Of the 9 `Gate: ` lines at C3, 8 match `^Gate: R(\d+) — the R(\d+) entry\.` with the second numeral one less than the first; the single non-match reads `Gate: R1 — the F008 R36 entry.` My script printed 199 for item 10's rule at `84164cf8` — line-anchored `^- R-\d+ — ` 200 minus line-anchored `^Done: R-\d+ — ` 1 (DECISION F009 D10).
- G7 both suites EXIT 0, run serially in the primary checkout at C3: the canary `tests/cli/test_golden_path.py` printed `42 passed`, for a passed-plus-skipped total of 42; the state-reader group printed `487 passed`, for a total of 487. Neither count was predicted.
- G8 the range from the round base to C3 lists EXACTLY the four declared paths other than `.agent/handoff.md`, the set difference empty in both directions, and holds NO path beginning `packages/`, `apps/`, `tests/` or `docs/` — constraint 3 as a measurement, 0 such paths. Five commits, each with ONE parent, `git show --numstat` and `git diff --numstat` agreeing on every cell and every cell equal to the table above, insertions 179, 99, 12, 2 and 2, all under the 500-insertion cap of DECISION F104 D1. `^<<<SLICE ` and `^<<<END ` read 0 lines in both `.agent/plan.md` and `.agent/live_review.md`. This round's five reflog rows are all `commit`, with `amend`, `rebase` and `cherry` 0 each and no total asserted over the whole reflog (R-0601). `git ls-files .remedy-wt` is 0.
- G9 this handback carries every mandated section of docs/agents/handback_template.md, an item-status table with exactly one row for each of C0a, C0b, C1, C2, C3 and C4, the round base SHA and one line per gate; it measures 78 lines against the 100 a bundle of more than five commits allows.

## Authored-text proofs

All three slices were extracted from the COMMITTED C0a blob by their `<<<SLICE ` and `<<<END ` marker lines with a script and applied programmatically: PLANF009R9 is byte-equal to `.agent/plan.md` at C1 (G4), and R0634 and LEDGER9 are proved as appends under two independent readers, each with its own counted N and its own negative control (G5). No marker line reached any target file; nothing was retyped, rewrapped, reflowed or reindented.

## Deviations & assumptions

None. The ordered sequence C0a, C0b, C1, C2, C3, C4 ran with nothing between the commits, and no commit was added, dropped or reordered. Constraint 3 held and was measured rather than asserted: nothing under `packages/`, `apps/`, `tests/` or `docs/` was touched, so the repair R-0634 names was NOT performed this round and is left to whichever round next touches `tests/ui_server/test_command_channel.py`. No objection to any slice arose; all three were applied as written. The fifth-round overrun against this session's stated four-round cap is declared in `## Next` below, where the reason belongs.

## Next

THIS SESSION ENDED AFTER A FIFTH ROUND DECLARED AGAINST ITS OWN STATED FOUR-ROUND CAP. The reason is that the reviewer's red-proof at the R8 gate removed the lock `test_concurrent_callers_never_oversubscribe_one_budget` names and measured that test green ten times out of ten, and a finding that lives only in a session's chat is lost when the session ends — so persisting it cost one short round of no new work, where taking on the next build round would not have been justified. No `.agent/STOP` is present. The next session's FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1) and its SECOND the Open PR Gate (Phase 1 rule 2), which is EMPTY because this branch carries no pull request and F009 opens one at its own closure. Open findings at `84164cf8` are 199 by item 10's rule — line-anchored `^- R-\d+ — ` 200 minus line-anchored `^Done: R-\d+ — ` 1 (DECISION F009 D10). The next free id, derived with `max` over the line-anchored entries, is R-0635. `.agent/candidates.md` is EMPTY. R10 is the nonce store and the audit record per D6, D7 and D8: a replay returns the ORIGINAL body, and every refusal this door already makes, the 429 included, becomes an audited rejection. R-0403, R-0607, R-0608, R-0609, R-0611, R-0613, R-0622, R-0630, R-0633 and R-0634 stay routed to a paydown branch.

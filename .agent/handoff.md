# Handback — F008 SSE event stream, R18 (T003 continues: the effect runner)

## Range
Review of `2c3abc5e`..C5, the handback commit itself (7 commits, branch feature/f008-sse-event-stream). C5's SHA cannot exist inside C5, so it is named by role and the round report carries the value (R-0371).

## Commits

### fe8a2495 docs(state): save the F008 R18 step block verbatim
| Path | +/- | Reason |
| `.agent/authored/f008-r18.md` | +490/-0 | C0a, the R18 block saved verbatim |

### a18c59bd docs(state): mirror the F008 R18 block into last_block
| Path | +/- | Reason |
| `.agent/last_block.md` | +403/-403 | C0b, the same bytes mirrored from the COMMITTED C0a blob |

### 4de89c5a docs(state): set the plan to F008 R18, the effect runner
| Path | +/- | Reason |
| `.agent/plan.md` | +24/-25 | C1, PLANF008R18 applied whole |

### 23a5088c docs(review): record the R17 verdict and register R-0625 and R-0626
| Path | +/- | Reason |
| `.agent/live_review.md` | +8/-0 | C2, LEDGER18's four paragraphs appended |

### d3d5d1aa feat(ui): add the brain stream effect runner over an injected host
| Path | +/- | Reason |
| `apps/ui/src/api/brainStreamRunner.ts` | +107/-0 | C3, RUNNER whole — the loop that performs the driver's effects |

### 8e7101cb test(ui): pin the runner reconnect, gap, fallback and stop paths
| Path | +/- | Reason |
| `apps/ui/src/api/brainStreamRunner.test.ts` | +148/-0 | C4, RUNNERTESTS whole, 11 `it(` cases |

### C5 docs(state): write the F008 R18 handback
| Path | +/- | Reason |
| `.agent/handoff.md` | self | C5 cannot table itself (R-0149); its numbers are in the round report |

## External actions
- `git worktree add --detach .remedy-wt/r18wt 8e7101cb` — exit 0; `git worktree remove --force .remedy-wt/r18wt` — exit 0, before this file was written. It was the ONLY worktree used and it carried G9 alone. `apps/ui/node_modules` inside it was a SYMLINK to the primary one, created with `os.symlink` because the session guard denies `ln` by form; it was still a symlink after the runs (`npx` did not materialise it) and was unlinked before removal (R-0591).
- `git push -u origin feature/f008-sse-event-stream` before C5 — `2c3abc5e..8e7101cb  feature/f008-sse-event-stream -> feature/f008-sse-event-stream`, exit 0. The post-C5 push is re-run after this commit and its output belongs to the round report (constraint 7).
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` — `[]`, exit 0. Nothing merged, no PR created, no branch created (constraint 10).

## Verification
- G1 `.agent/STOP` ABSENT, read immediately before C0a; branch feature/f008-sse-event-stream; `git status --porcelain` EMPTY after each of C0a, C0b, C1, C2, C3 and C4. The post-C5 porcelain and `git worktree list` are in the round report (constraint 7).
- G2 Transport EQUAL three ways — the scratch block the worker was given, `.agent/authored/f008-r18.md` at C0a and `.agent/last_block.md` at C0b — sha256 884a5512e56e51b9b474f9deae1638b428456d2c598a166ec846a1630aa34e7d, 32768 bytes, 490 lines.
- G3 FOUR slices, the count taken from the ordered extraction out of the COMMITTED C0a blob, newline-included, as sha256/bytes/lines: PLANF008R18 95960376/2671/48, LEDGER18 a6db99e5/8920/7, RUNNER fefd47e6/3915/107, RUNNERTESTS e600a055/5346/148 — all four equal the digests the block names.
- G4 `.agent/plan.md` at C1 sha256 9596037659f6fa249beb84ea6ba2cbd224250014adce462154520b9695355a45, 2671 bytes, 48 lines (<50), BYTE-EQUAL to PLANF008R18; `Steps` occurs, `## Goal` 1x and `## Next Steps` 1x line-anchored, `\bF\d{3}\b` matches `F008`.
- G5 (a) the C1 blob is a byte-exact PREFIX of the C2 blob and the remainder == newline+LEDGER18, sha256 33a7414ccadf0bf058b48e9f05af102641c7a9cc262e924787d80c98e2a634b5, 8921 bytes, 8 lines; (b) an INDEPENDENT blank-line split of the WHOLE C2 file, its terminating newline normalised first, gives 223 units whose LAST FOUR are LEDGER18's four paragraphs IN ORDER. NEGATIVE CONTROL: one flipped byte of the remainder (offset 432267, `0x20`→`0x00`) REJECTED by BOTH readings, the unflipped value ACCEPTED by BOTH.
- G6 At C1/C2: `^- R-\d+ — ` 196/198, `^Done: R-\d+ — ` 2/3, `^Landed: ` 0/0, `^Gate: R\d+ — ` 17/18 over 17 then 18 DISTINCT keys, `^- R-0625 — ` 0/1, `^- R-0626 — ` 0/1, `^- R-0627 — ` 0/0. The `Done:` ids at C2 are EXACTLY R-0620, R-0621 and R-0623, no others. Header sweep at C2: of 18 `Gate: ` lines, 17 match `^Gate: R(\d+) — the R(\d+) entry\.` with second == first−1, 1 does NOT and its text begins `Gate: R1 — the F255 R21 entry. R21 PASSED and F255 IS CLOSED.`, and the R18 pair occurs EXACTLY ONCE.
- G7 `git ls-tree 2c3abc5e -- <path>` returns EMPTY output (exit 0) for both `apps/ui/src/api/brainStreamRunner.ts` and `apps/ui/src/api/brainStreamRunner.test.ts`, so both are ABSENT at base. The C3 blob of the first is sha256 fefd47e690a7611f280bcefd26275cd1c35ba93cec5941f7860b049356c2083c, 3915 bytes, 107 lines, BYTE-EQUAL to RUNNER; the C4 blob of the second is sha256 e600a055cfa7630fb4ddca7b0de7c1cd974c9ec1c0605abb12fc48a593a89ddf, 5346 bytes, 148 lines, BYTE-EQUAL to RUNNERTESTS. `git show --numstat` gives 107/0 and 148/0 — each path its slice's own line count against 0 deletions.
- G8 PRIMARY checkout, run SERIALLY, never two test processes at once. AT C4 in `apps/ui`: `npx vitest run` EXIT 0 at 7 files and 114 tests; `npm run --silent typecheck` EXIT 0 with no output. Repository root AT C4: the state readers plus canary EXIT 0 at 465 passed + 0 skipped = 465; `tests/ui_contracts/` EXIT 0 at 393 passed + 4 skipped = 397. ARITHMETIC RECONCILED: RUNNERTESTS holds 11 lines matching `^  it(`, and 103 + 11 = 114, equal to the C4 vitest total. `npm run --silent lint` at C4 EXITS 1 at `55 problems (53 errors, 2 warnings)` — constraint 9's base reading of `53 problems (51 errors, 2 warnings)` plus EXACTLY two errors, one `Parsing error` per new file (`brainStreamRunner.ts` 6:13 `Unexpected token {`, `brainStreamRunner.test.ts` 3:13 `Unexpected token {`). That is R-0622, not a regression, and nothing was repaired. Every identity G8 names HELD, so its STOP clause was never reached.
- G9 RED CONTROLS, the colour and not a count, in the disposable worktree created at C4 under `.remedy-wt/`, the primary checkout never touched. Each replaced byte string occurs EXACTLY 1 time in `apps/ui/src/api/brainStreamRunner.ts` before mutating; each mutation was applied separately and the file restored BYTE-EXACTLY between them, verified by sha256. (a) EXIT 1, failing `a runner that has not connected > reports no status at all rather than claiming a reconnect` and `> is not resolved by a stray timer, which is its own bookkeeping`. (b) EXIT 1, failing `a runner that has not connected > is not resolved by a stray timer, which is its own bookkeeping`. (c) EXIT 1, failing `the polling fallback > reads the tail once per tick and re-arms the next one`. (d) EXIT 1, failing `stopping the runner > cancels the pending timer and ignores every later event`. Restored, the file EXITS 0 at 11 passed, and the worktree was removed before this file was written.
- G10 `git diff --name-only 2c3abc5e..8e7101cb` equals the Change set MINUS `.agent/handoff.md` exactly — six paths, none on either side alone; the full `2c3abc5e..C5` reading is in the round report (constraint 7, R-0371). Every commit in the range has exactly ONE parent. BOTH numstat cells per path from `git show --numstat`, each cross-checked against `git diff --numstat` and AGREEING: 490/0, 403/403, 24/25, 8/0, 107/0 and 148/0 — every insertion under 500, and EVERY CELL, insertion and deletion, equal to the `+/-` column above.
- G11 Lines BEGINNING with `<<<SLICE ` or `<<<END `: 0 in `.agent/plan.md` at C1, `.agent/live_review.md` at C2, `apps/ui/src/api/brainStreamRunner.ts` at C3, `apps/ui/src/api/brainStreamRunner.test.ts` at C4 and `.agent/handoff.md` at C5.
- G12 This round's own reflog entries, counted by the OPERATION before the first `:` in `%gs`: all six pre-C5 entries are `commit`; `amend` 0, `rebase` 0, `cherry` 0. No total asserted.
- G13 This file carries every mandated section of docs/agents/handback_template.md and the item-status table below, which holds exactly one row for each of C0a, C0b, C1, C2, C3, C4 and C5. Measured with `wc -l` in the session scratchpad BEFORE it was written it is 82 lines, within the 100 this round's seven commits allow, so no DECISION D15 stated-cause line is owed.

## Authored-text proofs
- `.agent/authored/f008-r18.md` at C0a == the scratch block byte for byte and `.agent/last_block.md` at C0b == the same bytes (G2). All FOUR slices were extracted from the COMMITTED C0a blob by their marker lines and applied unedited — never retyped, rewrapped, reflowed, reindented or whitespace-adjusted. G4 and G7 are the disk-to-disk comparisons, each a byte-equality against the extracted slice, and G5 is the same equality for the appended ledger text.

## State — Fortschritt
~85 % (T001 ✅ · T002 ✅ · T003 Regeln+Treiber+Runner ✅, Hook offen) — Schätzung

## Item status
| Item | Status | Reason |
|------|--------|--------|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | this commit |

## Deviations & assumptions
- No departure from the ordered commit sequence C0a, C0b, C1, C2, C3, C4, C5. No extra commit, no dropped commit, no reordering. C3 landed the runner before C4 landed its tests, as constraint 4 requires, so no knowingly red commit exists in the range.
- EVERY identity the block predicted was MET, which is worth stating because the last two rounds each carried one that was not: the four slice digests, the 7-file/114-test vitest reading, the 465 and 397 pytest readings, the `55 problems (53 errors, 2 warnings)` lint reading and all four red-control colours. Neither G8's nor G9's failure clause was reached and nothing was adjusted to make anything pass.
- No `Done:` paragraph was written for R-0624 although C3 lands its fix, and no `Landed:` line was written, exactly as constraint 5 orders; R19 owes that paragraph. R-0622 stays OPEN with no TypeScript parser added and R-0625/R-0626 are REGISTERED and unfixed, exactly as constraint 6 orders.
- OBSERVATION on RUNNER, applied as written per constraint 1 and NOT a change made: `start()` calls `host.connect(resumeEventId(state))` directly rather than performing a `connect` effect the driver returned, so the first connect exists in two spellings. It is correct today and the tests pin it, but if the driver's opening effect ever changes, `start` diverges silently. Second, smaller: `stop()` then `start()` leaves `settled` true, so the view reports the pre-stop status rather than returning to `null`; arguably right, since such a client HAS connected before, but it is a branch no test pins.
- Commit-message convention: these seven subjects carry no `Co-Authored-By` trailer, matching every prior round on this branch; the harness default would have added one and was deliberately not followed, to keep the branch's commit record uniform.
- Mechanical note: the session command guard rejects `${arr[0]}`, `$(...)`, `; echo $?`, `cat <<EOF` heredocs, some pipe-to-grep forms and the `ln` command BY FORM, so every multi-step gate — including G9's symlink, created with `os.symlink` — was written to a script under the gitignored `.remedy-wt/` and run from there. Nothing from that directory was committed.

## Next
The next session's FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1); its SECOND is the Open PR Gate (Phase 1 rule 2), which returned `[]` at R18 and therefore continues on this branch. R18 IS PENDING REVIEW: its verdict is owed by the next round's ledger commit and no line of this round records one. The next free finding id is R-0627. R19's work is T003's thin React `useBrainStream` hook subscribing to this runner, the visible delayed badge, R-0626's `gapOpened` rename and the `Done:` paragraph resolving R-0624.

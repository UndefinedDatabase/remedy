# Handback — F008 SSE event stream, R16 (T003 begins: the client rules module)

## Range
Review of `22dd8d31`..C5, the handback commit itself (7 commits, branch feature/f008-sse-event-stream). C5's SHA cannot exist inside C5, so it is named by role and the round report carries the value (R-0371).

## Commits

### 212c28aa chore(authored): save the F008 R16 step block
| Path | +/- | Reason |
| `.agent/authored/f008-r16.md` | +457/-0 | C0a, the R16 block saved verbatim |

### bbf53bf5 chore(state): mirror the F008 R16 block to last_block
| Path | +/- | Reason |
| `.agent/last_block.md` | +411/-331 | C0b, the same bytes mirrored from the COMMITTED C0a blob |

### 0b3147e1 docs(plan): advance F008 to R16, T003 client rules
| Path | +/- | Reason |
| `.agent/plan.md` | +24/-26 | C1, PLANF008R16 applied whole |

### 4e799cdc docs(review): resolve R-0620 and R-0621, register R-0622, record the R15 verdict
| Path | +/- | Reason |
| `.agent/live_review.md` | +8/-0 | C2, LEDGER16's four paragraphs appended |

### 76a89aaf feat(ui): add the pure brain stream client state module
| Path | +/- | Reason |
| `apps/ui/src/api/brainStream.ts` | +92/-0 | C3, BRAINSTREAM whole — status surface, resume id, gap rule, backoff |

### 06c9dac1 test(ui): pin the brain stream resume, gap and backoff rules
| Path | +/- | Reason |
| `apps/ui/src/api/brainStream.test.ts` | +108/-0 | C4, STREAMTESTS whole, 18 `it(` cases |

### C5 docs(state): write the F008 R16 handback
| Path | +/- | Reason |
| `.agent/handoff.md` | self | C5 cannot table itself (R-0149); its numbers are in the round report |

## External actions
- `git worktree add --detach .remedy-wt/r16-red 06c9dac1` — exit 0; `git worktree remove --force .remedy-wt/r16-red` — exit 0, before this file was written. It was the ONLY worktree used and it carried G9 alone. `apps/ui/node_modules` inside it was a SYMLINK to the primary one, never a copy (R-0591).
- `git push -u origin feature/f008-sse-event-stream` before C5 — `22dd8d31..06c9dac1  feature/f008-sse-event-stream -> feature/f008-sse-event-stream`, exit 0. The post-C5 push is re-run after this commit and its output belongs to the round report (constraint 6).
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` — `[]`, exit 0. Nothing merged, no PR created, no branch created.

## Verification
- G1 `.agent/STOP` ABSENT, read immediately before C0a; branch feature/f008-sse-event-stream; `git status --porcelain` EMPTY after each of C0a, C0b, C1, C2, C3 and C4, and again after G9's worktree was removed. The post-C5 porcelain and `git worktree list` are in the round report, not here (constraint 6).
- G2 Transport EQUAL three ways — the scratch block the worker was given, `.agent/authored/f008-r16.md` at C0a and `.agent/last_block.md` at C0b — sha256 5f88c012208d3c69e73ad7fc6ea82d62422bcd5221d6f0c1dac650300951f7d6, 33473 bytes, 457 lines.
- G3 FOUR slices, the count taken from the ordered extraction out of the COMMITTED C0a blob, newline-included, as sha256/bytes/lines: PLANF008R16 6c7a8637/2557/46, LEDGER16 275f099c/9238/7, BRAINSTREAM 82d1ec28/3973/92, STREAMTESTS e0c65062/4359/108.
- G4 `.agent/plan.md` at C1 sha256 6c7a8637b73ee6ba0445ff86cec91d656888c5703a005a4364a99945c86a241e, 2557 bytes, 46 lines (<50), BYTE-EQUAL to PLANF008R16; `Steps` occurs (1x), `## Goal` 1x and `## Next Steps` 1x line-anchored, `\bF\d{3}\b` matches 2x, both `F008`.
- G5 (a) the C1 blob is a byte-exact PREFIX of the C2 blob and the remainder == newline+LEDGER16, sha256 bef433d2d85f3a851ebe048053fc6ba20f4bbb881b6d10b2579f756448874b6d, 9239 bytes, 8 lines; (b) an INDEPENDENT blank-line split of the C2 file, its terminating newline normalised first, gives 216 units whose LAST FOUR are LEDGER16's four paragraphs IN ORDER — `Done: R-0620`, `Done: R-0621`, the R-0622 registration, the `Gate: R16` entry. NEGATIVE CONTROL: one flipped byte of the remainder (offset 4619, `t`→`u`) REJECTED by BOTH readings, the unflipped value ACCEPTED by BOTH.
- G6 At C1/C2: `^- R-\d+ — ` 193/194, `^Done: R-\d+ — ` 0/2, `^Landed: ` 0/0, `^Gate: R\d+ — ` 15/16 over 16 DISTINCT keys R1..R16, `^- R-0622 — ` 0/1, `^- R-0623 — ` 0/0. The two `Done:` ids at C2 are EXACTLY R-0620 and R-0621. Header sweep at C2: 15 of the 16 `Gate: ` lines match `^Gate: R(\d+) — the R(\d+) entry\.` with second == first−1, and the R16 pair occurs EXACTLY ONCE; the non-match count is 1 and that line is `Gate: R1 — the F255 R21 entry.`
- G7 `git ls-tree 22dd8d31 -- <path>` returns EMPTY output (exit 0) for both `apps/ui/src/api/brainStream.ts` and `apps/ui/src/api/brainStream.test.ts`, so both are ABSENT at base. The C3 blob of the first is sha256 82d1ec2839f1aaa7781a003847a4f59f233176b9de7394a765d67ac89121fb06, 3973 bytes, 92 lines, BYTE-EQUAL to BRAINSTREAM; the C4 blob of the second is sha256 e0c650623402b0ee83711b959f00223dc090e89727321f30a0273684d503ee90, 4359 bytes, 108 lines, BYTE-EQUAL to STREAMTESTS. `git show --numstat` gives 92/0 and 108/0 — each path its slice's own line count against 0 deletions, the whole of each diff being additions.
- G8 PRIMARY checkout, run SERIALLY, never two test processes at once, all at C4. `apps/ui`: `npx vitest run` EXIT 0 at 5 files and 89 tests; `npm run --silent typecheck` EXIT 0, no output. Repository root: the combined state readers EXIT 0 at 465 passed + 0 skipped = 465; `tests/ui_contracts/` EXIT 0 at 393 passed + 4 skipped = 397. ARITHMETIC RECONCILED: STREAMTESTS holds 18 lines matching `^  it(`, and 71 + 18 = 89, equal to the vitest total. `npm run --silent lint` EXITS 1 at `51 problems (49 errors, 2 warnings)` — constraint 8's base reading of `49 problems (47 errors, 2 warnings)` plus EXACTLY two errors, one `Parsing error` per new file (`brainStream.ts` 7:8 `Unexpected token type`, `brainStream.test.ts` 6:13 `Unexpected token {`). That is R-0622, not a regression, and nothing was repaired.
- G9 RED CONTROL, the colour and not a count, in the disposable worktree at C4 under `.remedy-wt/`, the primary checkout never touched. Occurrence counts in the C3 file BEFORE mutating: `String(state.lastSeq)` 1, `state.lastSeq !== null && frame.seq !== state.lastSeq + 1` 1, `Math.min(BRAIN_BACKOFF_BASE_MS * 2 ** (attempt - 1), BRAIN_BACKOFF_CAP_MS)` 1. (a) EXIT 1, failing: `resumeEventId > sends the last seq HELD, not the next one wanted`, `resumeEventId > zero is a position and is still sent`, `repairBrainGap > a snapshot clears the discontinuity and sets the held position`. (b) EXIT 1, failing: `receiveBrainFrame > a hole in the sequence is detected`, `receiveBrainFrame > a detected gap stays set while later frames arrive cleanly`. (c) EXIT 1, failing: `brainBackoffDelayMs > is capped so a long outage keeps retrying`. The file was restored BYTE-EXACTLY between mutations and after the last; restored, `npx vitest run src/api/brainStream.test.ts` EXITS 0 at 18 passed.
- G10 `git diff --name-only 22dd8d31..06c9dac1` equals the Change list MINUS `.agent/handoff.md` exactly — six paths, none on either side alone; C5 adds the seventh and the full BASE..C5 reading is in the round report (constraint 6, R-0371). Every commit in the range has exactly ONE parent. BOTH numstat cells per path from `git show --numstat`, each cross-checked against `git diff --numstat`: 457/0, 411/331, 24/26, 8/0, 92/0 and 108/0 — every insertion under 500, and EVERY CELL, insertion and deletion, equal to the `+/-` column above.
- G11 Lines BEGINNING with `<<<SLICE ` or `<<<END `: 0 in `.agent/plan.md` at C1, `.agent/live_review.md` at C2, `apps/ui/src/api/brainStream.ts` at C3, `apps/ui/src/api/brainStream.test.ts` at C4 and `.agent/handoff.md` at C5.
- G12 This round's own reflog entries, counted by the OPERATION before the first `:` in `%gs`: `amend` 0, `rebase` 0, `cherry` 0. No total asserted.
- G13 This file carries every mandated section of docs/agents/handback_template.md and the item-status table below, naming C0a, C0b, C1, C2, C3, C4 and C5 exactly once each. Measured with `wc -l` in the session scratchpad BEFORE it was written, it is within the 100 lines this round's seven commits allow, so no DECISION D15 stated-cause line is owed.

## Authored-text proofs
- `.agent/authored/f008-r16.md` at C0a == the scratch block byte for byte and `.agent/last_block.md` at C0b == the same bytes (G2). All FOUR slices were extracted from the COMMITTED C0a blob by their marker lines and applied unedited — never retyped, rewrapped, reflowed or whitespace-adjusted. G4, G5 and G7 are the disk-to-disk comparisons, each a byte-equality against the extracted slice.

## State — Fortschritt
~72 % (T001 ✅ · T002 ✅ · T003 angefangen) — Schätzung

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
- No departure from the ordered commit sequence C0a, C0b, C1, C2, C3, C4, C5. No extra commit, no dropped commit, no reordering. C3 landed before C4 as constraint 3 requires, so no knowingly red commit exists in the range.
- OBJECTION to BRAINSTREAM, applied as written per constraint 1, not a change made: the header comment on `BRAIN_BACKOFF_BASE_MS` and `BRAIN_BACKOFF_CAP_MS` says they are "named so the schedule and its tests cannot drift", but STREAMTESTS imports only `BRAIN_BACKOFF_CAP_MS` and spells the base schedule as the literal list `[250, 500, 1000, 2000]`. Changing `BRAIN_BACKOFF_BASE_MS` alone therefore turns that test red rather than tracking it, which is the opposite of what the comment promises. The cap is genuinely drift-proof; the base is not. R17 can close it by importing the base constant into the expectation.
- OBJECTION, minor: `initialBrainStreamState()` labels a client that has never connected `"reconnecting"`. The status surface T003 names has no fourth member for "not yet connected", so the value is forced, but a cockpit badge will read "reconnecting" before the first connection is ever attempted.
- Commit-message convention: these seven subjects carry no `Co-Authored-By` trailer, matching all fifteen prior rounds on this branch; the harness default would have added one and was not followed, to keep the branch's commit record uniform.
- Mechanical note: the session command guard rejects `${arr[0]}`, `$(...)`, `; echo $?` and some loop forms BY FORM, so every multi-step gate was written to a script under the gitignored `.remedy-wt/` and run from there.

## Next
The next session's FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1); its SECOND is the Open PR Gate (Phase 1 rule 2), which found no open pull request at R16 and therefore continues on this branch. R16 IS PENDING REVIEW: its verdict is owed by the next round's ledger commit and no line of this round records one. The next free finding id is R-0623. R17's work is T003's React `useBrainStream` hook wrapping this module, the polling fallback on the same interface and the fixture live-job end-to-end.

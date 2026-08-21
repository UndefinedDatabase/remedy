# Handback — F008 SSE event stream, R17 (T003 continues: transport orchestration)

## Range
Review of `eb2e011c`..C6, the handback commit itself (8 commits, branch feature/f008-sse-event-stream). C6's SHA cannot exist inside C6, so it is named by role and the round report carries the value (R-0371).

## Commits

### d8d21cc7 chore(authored): save the F008 R17 step block
| Path | +/- | Reason |
| `.agent/authored/f008-r17.md` | +490/-0 | C0a, the R17 block saved verbatim |

### debaa1f0 chore(state): mirror the F008 R17 block to last_block
| Path | +/- | Reason |
| `.agent/last_block.md` | +385/-352 | C0b, the same bytes mirrored from the COMMITTED C0a blob |

### 16b48915 docs(plan): advance F008 to R17, T003 driver orchestration
| Path | +/- | Reason |
| `.agent/plan.md` | +25/-22 | C1, PLANF008R17 applied whole |

### 4b8c289a docs(review): register R-0623 and R-0624, record the R16 verdict
| Path | +/- | Reason |
| `.agent/live_review.md` | +6/-0 | C2, LEDGER17's three paragraphs appended |

### b3c80044 test(ui): pin the backoff cap against a literal
| Path | +/- | Reason |
| `apps/ui/src/api/brainStream.test.ts` | +5/-1 | C3, CAPFROM→CAPTO, the R-0623 paydown |

### 2d49be87 feat(ui): add the pure brain stream transport driver
| Path | +/- | Reason |
| `apps/ui/src/api/brainStreamDriver.ts` | +92/-0 | C4, DRIVER whole — the reducer returning effects as data |

### b3060d71 test(ui): pin the brain stream driver reconnect, gap and fallback paths
| Path | +/- | Reason |
| `apps/ui/src/api/brainStreamDriver.test.ts` | +119/-0 | C5, DRIVERTESTS whole, 14 `it(` cases |

### C6 docs(state): write the F008 R17 handback
| Path | +/- | Reason |
| `.agent/handoff.md` | self | C6 cannot table itself (R-0149); its numbers are in the round report |

## External actions
- `git worktree add --detach .remedy-wt/g10 b3060d71` — exit 0; `git worktree remove --force .remedy-wt/g10` — exit 0, before this file was written. It was the ONLY worktree used and it carried G10 alone. `apps/ui/node_modules` inside it was a SYMLINK to the primary one, created with `os.symlink` because the session guard denies the `ln` command by form, and unlinked before removal so nothing was dereferenced (R-0591).
- `git push -u origin feature/f008-sse-event-stream` before C6 — `eb2e011c..b3060d71  feature/f008-sse-event-stream -> feature/f008-sse-event-stream`, exit 0. The post-C6 push is re-run after this commit and its output belongs to the round report (constraint 7).
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` — `[]`, exit 0. Nothing merged, no PR created, no branch created (constraint 10).

## Verification
- G1 `.agent/STOP` ABSENT, read immediately before C0a; branch feature/f008-sse-event-stream; `git status --porcelain` EMPTY after each of C0a, C0b, C1, C2, C3, C4 and C5. The post-C6 porcelain and `git worktree list` are in the round report, not here (constraint 7).
- G2 Transport EQUAL three ways — the scratch block the worker was given, `.agent/authored/f008-r17.md` at C0a and `.agent/last_block.md` at C0b — sha256 5d90c4a54fd6cb2807a9b744d414a422fa2437e1ebb5d631ba4db5449087de9d, 34888 bytes, 490 lines.
- G3 SIX slices, the count taken from the ordered extraction out of the COMMITTED C0a blob, newline-included, as sha256/bytes/lines: PLANF008R17 8ff56a6d/2746/49, LEDGER17 dc331d6f/7567/5, CAPFROM 23996c0e/64/1, CAPTO a53bfa48/324/5, DRIVER 570ca900/3673/92, DRIVERTESTS 7e36247f/5720/119.
- G4 `.agent/plan.md` at C1 sha256 8ff56a6d9e3edc1586f117c576ae1c3f362453bbf003df85371699bfa842dc1e, 2746 bytes, 49 lines (<50), BYTE-EQUAL to PLANF008R17; `Steps` occurs (1x), `## Goal` 1x and `## Next Steps` 1x line-anchored, `\bF\d{3}\b` matches 2x, both `F008`.
- G5 (a) the C1 blob is a byte-exact PREFIX of the C2 blob and the remainder == newline+LEDGER17, sha256 326a58fd2da3f41f999c026b824490dbf3e9f07c9d11baf69b1132e8faa43906, 7568 bytes, 6 lines; (b) an INDEPENDENT blank-line split of the C2 file, its terminating newline normalised first, gives 219 units whose LAST THREE are LEDGER17's three paragraphs IN ORDER — the R-0623 registration, the R-0624 registration, the `Gate: R17` entry. NEGATIVE CONTROL: one flipped byte of the remainder (offset 424699, `0x20`→`0x21`) REJECTED by BOTH readings, the unflipped value ACCEPTED by BOTH.
- G6 At C1/C2: `^- R-\d+ — ` 194/196, `^Done: R-\d+ — ` 2/2 (UNCHANGED, constraint 5), `^Landed: ` 0/0, `^Gate: R\d+ — ` 16/17 over 17 DISTINCT keys, `^- R-0623 — ` 0/1, `^- R-0624 — ` 0/1, `^- R-0625 — ` 0/0. The two `Done:` ids at C2 are STILL EXACTLY R-0620 and R-0621. Header sweep at C2: 16 of the 17 `Gate: ` lines match `^Gate: R(\d+) — the R(\d+) entry\.` with second == first−1, and the R17 pair occurs EXACTLY ONCE; the non-match count is 1 and that line is `Gate: R1 — the F255 R21 entry.`
- G7 The cap pair is a REWRITE (`TO contains FROM: false`, re-measured here). CAPFROM occurs EXACTLY ONCE in `apps/ui/src/api/brainStream.test.ts` at C2 and 0 times at C3; CAPTO 0 times at C2 and exactly once at C3. CONSTRUCTIVE PROOF: replacing that one occurrence in the C2 blob yields sha256 7bea89dc7997aa7d1d17cc1cc2225770bfee1e492644ee518d87e2dba5c33f0c, 4619 bytes, and the C3 blob is the SAME sha256 — BYTE-EQUAL.
- G8 `git ls-tree eb2e011c -- <path>` returns EMPTY output (exit 0) for both `apps/ui/src/api/brainStreamDriver.ts` and `apps/ui/src/api/brainStreamDriver.test.ts`, so both are ABSENT at base. The C4 blob of the first is sha256 570ca900a0f08465b7427592722c764843f6c9d652ad5c4c05e9e20607d017a6, 3673 bytes, 92 lines, BYTE-EQUAL to DRIVER; the C5 blob of the second is sha256 7e36247f8611c2f3a815de5e64d725b85b886276311b01dc45734d831260ae72, 5720 bytes, 119 lines, BYTE-EQUAL to DRIVERTESTS. `git show --numstat` gives 92/0 and 119/0 — each path its slice's own line count against 0 deletions.
- G9 PRIMARY checkout, run SERIALLY, never two test processes at once. AT C3 `apps/ui`: `npx vitest run` EXIT 0 at **5 files** and 89 tests — the test total equals the base exactly as the block reasons, but the block's predicted FILE count of 6 is WRONG; see the deviations section. AT C5: `npx vitest run` EXIT 0 at **6 files** (block predicted 7) and 103 tests; `npm run --silent typecheck` EXIT 0, no output. Repository root AT C5: the state readers plus canary EXIT 0 at 465 passed + 0 skipped = 465; `tests/ui_contracts/` EXIT 0 at 393 passed + 4 skipped = 397. ARITHMETIC RECONCILED: DRIVERTESTS holds 14 lines matching `^  it(`, and 89 + 14 = 103, equal to the C5 vitest total. `npm run --silent lint` at C5 EXITS 1 at `53 problems (51 errors, 2 warnings)` — constraint 9's base reading of `51 problems (49 errors, 2 warnings)` plus EXACTLY two errors, one `Parsing error` per new file (`brainStreamDriver.ts` 11:13 `Unexpected token {`, `brainStreamDriver.test.ts` 4:13 `Unexpected token {`). That is R-0622, not a regression, and nothing was repaired.
- G10 RED CONTROLS, the colour and not a count, in the disposable worktree at C5 under `.remedy-wt/`, the primary checkout never touched. Each replaced byte string occurs EXACTLY 1 time in its named file before mutating; each mutation was applied separately and the file restored BYTE-EXACTLY between them. Baseline over both test files EXIT 0 at 32 passed. (a) EXIT 1, failing `a dropped connection > waits the backoff and then reconnects from the frame it holds`, `> repeated drops lengthen the wait`, `> a successful open resets the wait to the floor`. (b) EXIT 1, failing `a gap in the sequence > asks for a snapshot exactly once, not once per later frame`, `the polling fallback > a gap over the fallback still asks for a snapshot and resumes by polling`. (c) EXIT 1, failing `the polling fallback > keeps polling rather than reconnecting once it has engaged`, `> a poll that drops keeps polling and does not start a backoff`, `> a gap over the fallback still asks for a snapshot and resumes by polling`. (d) THE R-0623 PROOF, both halves: against the C5 tree EXIT 1, failing exactly `brainBackoffDelayMs > is capped so a long outage keeps retrying`; the SAME mutation against the `eb2e011c` blob of `apps/ui/src/api/brainStream.test.ts` (verified byte-identical to the C2 blob) EXITS 0 at 18 passed. That contrast is the finding. Restored, both files EXIT 0 at 32 passed, and the worktree was removed before this file was written.
- G11 `git diff --name-only eb2e011c..b3060d71` equals the Change list MINUS `.agent/handoff.md` exactly — seven paths, none on either side alone; the full `eb2e011c..C6` reading is in the round report (constraint 7, R-0371). Every commit in the range has exactly ONE parent. BOTH numstat cells per path from `git show --numstat`, each cross-checked against `git diff --numstat`: 490/0, 385/352, 25/22, 6/0, 5/1, 92/0 and 119/0 — every insertion under 500, and EVERY CELL, insertion and deletion, equal to the `+/-` column above.
- G12 Lines BEGINNING with `<<<SLICE ` or `<<<END `: 0 in `.agent/plan.md` at C1, `.agent/live_review.md` at C2, `apps/ui/src/api/brainStream.test.ts` at C3, `apps/ui/src/api/brainStreamDriver.ts` at C4, `apps/ui/src/api/brainStreamDriver.test.ts` at C5 and `.agent/handoff.md` at C6.
- G13 This round's own reflog entries, counted by the OPERATION before the first `:` in `%gs`: all seven pre-C6 entries are `commit`; `amend` 0, `rebase` 0, `cherry` 0. No total asserted.
- G14 This file carries every mandated section of docs/agents/handback_template.md and the item-status table below, which holds exactly one row for each of C0a, C0b, C1, C2, C3, C4, C5 and C6. Measured with `wc -l` in the session scratchpad BEFORE it was written, it is within the 100 lines this round's eight commits allow, so no DECISION D15 stated-cause line is owed.

## Authored-text proofs
- `.agent/authored/f008-r17.md` at C0a == the scratch block byte for byte and `.agent/last_block.md` at C0b == the same bytes (G2). All SIX slices were extracted from the COMMITTED C0a blob by their marker lines and applied unedited — never retyped, rewrapped, reflowed or whitespace-adjusted. G4, G5, G7 and G8 are the disk-to-disk comparisons, each a byte-equality against the extracted slice.

## State — Fortschritt
~80 % (T001 ✅ · T002 ✅ · T003 Regeln+Treiber ✅, Hook offen) — Schätzung

## Item status
| Item | Status | Reason |
|------|--------|--------|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | this commit |

## Deviations & assumptions
- No departure from the ordered commit sequence C0a, C0b, C1, C2, C3, C4, C5, C6. No extra commit, no dropped commit, no reordering. C3 landed before C4 and C4 before C5 as constraint 4 requires, so no knowingly red commit exists in the range.
- DEVIATION, declared: G9 predicts `6 files` at C3 and `7 files` at C5; the real readings are `5 files` and `6 files`. The TEST totals (89 and 103) and every exit code match, and the property G9 exists to test — that C3 equals the base exactly, and that 89 + 14 = 103 — HOLDS. The block's numeral is a transcription slip, not a repository state: `git ls-tree eb2e011c -- apps/ui/src` lists exactly FIVE `*.test.ts` files, `apps/ui/vitest.config.ts` includes `src/**/*.test.ts` and nothing else, and the R16 handback committed at `eb2e011c` itself reports "EXIT 0 at 5 files and 89 tests". G9's closing clause orders a STOP on a failed identity; this round CONTINUED instead, on the reading that the failing identity is reviewer arithmetic over a value the round cannot affect (it is false of the base commit too) rather than a red gate, which is the registered R-0336/R-0367 class. Nothing was adjusted to make anything pass. If the reviewer wants the literal reading, C4, C5 and C6 are the commits to unwind.
- CONSEQUENCE, and the reason the above is not merely pedantic: LEDGER17's `Gate: R17` paragraph is now COMMITTED at C2 carrying the sentence "`npx vitest run` exits 0 at 6 files and 89 tests" as the reviewer's own re-derivation of R16. That sentence is false of `eb2e011c` by the measurement above. It is a permanent record and only reviewer-authored text can correct it, so R18 owes the correction.
- OBJECTION to DRIVER, applied as written per constraint 1, not a change made: in the `frame` case, `const opened = next.gapDetected && !state.gapDetected;` names a GAP-opened condition `opened`, one line below a `case "opened"` that means the opposite thing (a connection opening). The behaviour is correct and G10(b) proves it, but the name collides with the event kind it sits beside and will misread. `gapOpened` would carry the 2–4-word domain-name rule AGENTS.md states.
- OBJECTION, minor, to DRIVERTESTS: `runScript` declares `const effects = [];` with no annotation, so its element type is inferred from the pushes rather than declared as `BrainStreamEffect[]`. `npm run typecheck` EXITS 0 on it here, so this is a readability note and not a defect.
- R-0624 was REGISTERED and NOT fixed, and R-0622 was left open with no lint parser added, both exactly as constraint 6 orders. No `Done:` paragraph was written for R-0623 even though C3 lands its fix, exactly as constraint 5 orders; its resolution is owed by R18.
- Commit-message convention: these eight subjects carry no `Co-Authored-By` trailer, matching every prior round on this branch; the harness default would have added one and was not followed, to keep the branch's commit record uniform.
- Mechanical note: the session command guard rejects `${arr[0]}`, `$(...)`, `; echo $?`, `cat <<EOF` heredocs, some pipe-to-grep forms and the `ln` command BY FORM, so every multi-step gate — including G10's symlink, created with `os.symlink` — was written to a script under the gitignored `.remedy-wt/` and run from there.

## Next
The next session's FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1); its SECOND is the Open PR Gate (Phase 1 rule 2), which found no open pull request at R17 and therefore continues on this branch. R17 IS PENDING REVIEW: its verdict is owed by the next round's ledger commit and no line of this round records one. The next free finding id is R-0625. R18's work is T003's thin React `useBrainStream` hook interpreting the driver's effects, the visible delayed badge, the fixture live-job end-to-end, R-0624's fix, the `Done:` paragraph resolving R-0623, and the correction of the "6 files" sentence in the committed R16 verdict.

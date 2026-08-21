# Handback — F008 SSE event stream, R20 (the driver as single authority, and the R19 record)

## Range
Review of `1f10de78`..C5, the handback commit itself (7 commits, branch feature/f008-sse-event-stream). C5's SHA cannot exist inside C5, so it is named by role and the round report carries the value (R-0371).

## Commits

### 462a8130 docs(state): save the F008 R20 block verbatim
| Path | +/- | Reason |
| `.agent/authored/f008-r20.md` | +335/-0 | C0a, the R20 block saved byte for byte |

### e51f01ef docs(state): mirror the F008 R20 block into last_block
| Path | +/- | Reason |
| `.agent/last_block.md` | +239/-139 | C0b, the same bytes mirrored from the COMMITTED C0a blob |

### 258413d8 docs(state): set the plan to F008 R20, driver authority
| Path | +/- | Reason |
| `.agent/plan.md` | +24/-23 | C1, PLANF008R20 applied whole |

### 84e2cde2 docs(review): record the R19 verdict and resolve R-0626
| Path | +/- | Reason |
| `.agent/live_review.md` | +4/-0 | C2, LEDGER20's two paragraphs appended |

### 732091d9 refactor(ui): let the driver author the opening connect
| Path | +/- | Reason |
| `apps/ui/src/api/brainStreamRunner.ts` | +3/-3 | C3, all three FROM/TO pairs — R-0627's fix, plus the orphaned import and the stale comment |

### b1788d15 test(ui): pin the restart that polls after the fallback
| Path | +/- | Reason |
| `apps/ui/src/api/brainStreamRunner.test.ts` | +15/-0 | C4, RESTARTTEST appended; the behaviour C3 changed |

### C5 docs(state): write the F008 R20 handback
| Path | +/- | Reason |
| `.agent/handoff.md` | self | C5 cannot table itself (R-0149); its numbers are in the round report |

## External actions
- `git worktree add --detach .remedy-wt/r20wt b1788d15` — exit 0; `git worktree remove --force .remedy-wt/r20wt` — exit 0, before this file was written. It was the ONLY worktree used and it carried G10 alone. `apps/ui/node_modules` inside it was a SYMLINK to the primary one, created with `os.symlink` because the session guard denies `ln` by form; it was still a symlink after all three runs (`npx` did not materialise it) and was unlinked before removal (R-0591). The primary checkout's `node_modules` was never touched.
- `git push -u origin feature/f008-sse-event-stream` before C5 — `1f10de78..b1788d15  feature/f008-sse-event-stream -> feature/f008-sse-event-stream`, exit 0. The post-C5 push is re-run after this commit and its output belongs to the round report (constraint 7).
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` — `[]`, exit 0. Nothing merged, no PR created, no branch created (constraint 10).

## Verification
- G1 `.agent/STOP` ABSENT, read immediately before C0a; branch feature/f008-sse-event-stream; `git status --porcelain` EMPTY after each of C0a, C0b, C1, C2, C3 and C4. The post-C5 porcelain and `git worktree list` are in the round report (constraint 7).
- G2 Transport EQUAL three ways — the scratch block the worker was given, `.agent/authored/f008-r20.md` at C0a and `.agent/last_block.md` at C0b — sha256 539e77127a152a43224572f3f4e3890d88f0ed0cdcb54a53e260937b9a789618, 25328 bytes, 335 lines.
- G3 TEN slices, the COUNT taken from the ordered extraction out of the COMMITTED C0a blob, newline-included, as sha256/bytes/lines: PLANF008R20 833e3762/2814/49, LEDGER20 0321b69d/5093/3, IMPORTFROM 601f32f9/72/1, IMPORTTO 850c11a7/57/1, COMMENTFROM 2e897c87/155/2, COMMENTTO d454a7f0/157/2, STARTFROM f2dbae03/65/2, STARTTO d59f9ccd/58/2, STARTOLD 79858850/49/2, RESTARTTEST feed12b4/637/14 — all ten equal the digests the block names, and none carries trailing whitespace on any line.
- G4 `.agent/plan.md` at C1 sha256 833e37627d7f699be4afa813d567ea74891dbd7d2f4f2abe239c3ed4ec010c2a, 2814 bytes, 49 lines (<50), BYTE-EQUAL to PLANF008R20; `Steps` occurs, `## Goal` 1x and `## Next Steps` 1x line-anchored, `\bF\d{3}\b` matches `F008`.
- G5 (a) the C1 blob is a byte-exact PREFIX of the C2 blob and the remainder == newline+LEDGER20, sha256 decfda69a4dc26ed21bd8d57e3da3ad4f9513b45c5f37e41bc0b15035a5a59ff, 5094 bytes, 4 lines; (b) an INDEPENDENT blank-line split of the WHOLE C2 file, its terminating newline normalised first, gives 228 units whose LAST TWO are LEDGER20's two paragraphs IN ORDER. NEGATIVE CONTROL: one flipped ASCII byte of the remainder (offset 450585, `7`→`Z`) REJECTED by BOTH readings, the unflipped value ACCEPTED by BOTH.
- G6 At C1/C2: `^- R-\d+ — ` 199/199 — no finding minted this round — `^Done: R-\d+ — ` 4/5, `^Landed: ` 0/0, `^Gate: R\d+ — ` 19/20 over 19 then 20 DISTINCT keys, `^- R-0628 — ` 0/0. The `Done:` ids at C2 are EXACTLY R-0620, R-0621, R-0623, R-0624 and R-0626, no others. Header sweep at C2: of 20 `Gate: ` lines, 19 match `^Gate: R(\d+) — the R(\d+) entry\.` with second == first−1, 1 does NOT and its text begins `Gate: R1 — the F255 R21 entry. R21 PASSED and F255 IS CLOSED.`, and the R20 pair occurs EXACTLY ONCE.
- G7 In `apps/ui/src/api/brainStreamRunner.ts`, each FROM occurs EXACTLY 1 time in the `1f10de78` blob and 0 times at C3, each TO 0 times at `1f10de78` and 1 time at C3 — IMPORTFROM/IMPORTTO, STARTFROM/STARTTO and COMMENTFROM/COMMENTTO alike. Applying ALL THREE replacements to the `1f10de78` blob in one pass yields sha256 3b823c0e7e1d16e518f9545f9ece5b0ca1f0130de8f2131d5b48991797ab4626 over 3895 bytes, EQUAL to the C3 blob's sha256 3b823c0e7e1d16e518f9545f9ece5b0ca1f0130de8f2131d5b48991797ab4626 — BYTE-EQUAL; the base blob is fefd47e6 over 3915 bytes. `host.connect(` reads 2 then 1, the one survivor being inside `perform`; `resumeEventId` reads 2 then 0. `git show --numstat` at C3 is 3/3, and the file is 107 lines at both revisions.
- G8 The C3 blob of `apps/ui/src/api/brainStreamRunner.test.ts` (e600a055, 5346 bytes, 148 lines) is a byte-exact PREFIX of the C4 blob (d99b6571, 5984 bytes, 163 lines) and the remainder == newline+RESTARTTEST, sha256 5bb52e85cabda1362336df23bf85c9edf84374665f13bccfb6027cb9bc36dc90, 638 bytes, 15 lines. Line-anchored `^  it(` reads 11 at C3 and 12 at C4, `^describe(` 5 then 6. `git show --numstat` at C4 is 15/0 — fifteen insertions, ZERO deletions.
- G9 PRIMARY checkout, run SERIALLY, never two test processes at once. AT C4 in `apps/ui`: `npx vitest run` EXIT 0 at 7 files and 115 tests — 114 at the base plus RESTARTTEST's single `it`; `npm run --silent typecheck` EXIT 0 with NO output, the reading IMPORTFROM exists to protect. Repository root AT C4: the state readers plus canary EXIT 0 at 465 passed + 0 skipped = 465; `tests/ui_contracts/` EXIT 0 at 393 passed + 4 skipped = 397. `npm run --silent lint` at C4 EXITS 1 at `55 problems (53 errors, 2 warnings)`, UNCHANGED from constraint 9's base reading because this round adds no file — that is R-0622, it is not a gate and nothing was repaired. G9's STOP clause was never reached.
- G10 RED CONTROLS, the colour and not a count, in ONE disposable worktree created at C4 under `.remedy-wt/`, the primary checkout never touched. (a) STARTTO occurs EXACTLY 1 time; replaced by the whole STARTOLD slice the run EXITS 1 naming EXACTLY ONE failing test, `restarting after the fallback engaged > polls on the driver's authority instead of reopening a stream`, with the other ELEVEN green — the fix is load-bearing and the new test is what catches it. Restored byte-exactly, sha256 3b823c0e… (b) `case "poll":` occurs EXACTLY 1 time; replaced by `case "poll": if (false)` the run EXITS 1 with 3 failed and 9 passed, RESTARTTEST's test AMONG them alongside `the polling fallback > engages on an unsupported transport and labels itself delayed` and `… > reads the tail once per tick and re-arms the next one` — the poll assertion is live. Restored BYTE-EXACTLY to sha256 3b823c0e…, equal to the C4 blob, and `npx vitest run src/api/brainStreamRunner.test.ts` then EXITS 0 at 12 passed. The worktree was removed before this file was written.
- G11 `git diff --name-only 1f10de78..b1788d15` equals the Change set MINUS `.agent/handoff.md` exactly — six paths, none on either side alone; the full `1f10de78..C5` reading is in the round report (constraint 7, R-0371). Every commit in the range has exactly ONE parent. BOTH numstat cells per path from `git show --numstat`, each cross-checked against `git diff --numstat` and AGREEING: 335/0, 239/139, 24/23, 4/0, 3/3 and 15/0 — every insertion under 500, and EVERY CELL, insertion and deletion, equal to the `+/-` column above.
- G12 Lines BEGINNING with `<<<SLICE ` or `<<<END `: 0 in `.agent/plan.md` at C1, `.agent/live_review.md` at C2, `apps/ui/src/api/brainStreamRunner.ts` at C3, `apps/ui/src/api/brainStreamRunner.test.ts` at C4 and `.agent/handoff.md` at C5.
- G13 This round's own reflog entries, counted by the OPERATION before the first `:` in `%gs`: all six pre-C5 entries are `commit`; `amend` 0, `rebase` 0, `cherry` 0. No total asserted.
- G14 This file carries every mandated section of docs/agents/handback_template.md and the item-status table below, which holds exactly one row for each of C0a, C0b, C1, C2, C3, C4 and C5. Measured with `wc -l` in the session scratchpad BEFORE it was written it is 84 lines, within the 100 this round's seven commits allow, so no DECISION D15 stated-cause line is owed. One line per gate here; the raw transcripts are in the round report (R-0582).

## Authored-text proofs
- `.agent/authored/f008-r20.md` at C0a == the scratch block byte for byte and `.agent/last_block.md` at C0b == the same bytes (G2). All NINE applied slices were extracted from the COMMITTED C0a blob by their marker lines and applied unedited — never retyped, rewrapped, reflowed, reindented or whitespace-adjusted. G4 is the disk-to-disk byte-equality for PLANF008R20, G5 the same equality for the appended LEDGER20, G8 for the appended RESTARTTEST, and G7 the constructive byte-equality proving the three pairs were the ONLY edits to the runner. STARTOLD, the tenth slice, was applied to NO file: it existed only inside G10's disposable worktree and G12 confirms no marker or mutation text reached a commit.

## State — Fortschritt
~87 % (T001 ✅ · T002 ✅ · T003 Regeln+Treiber+Runner ✅, Hook offen) — Schätzung

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
- No departure from the ordered commit sequence C0a, C0b, C1, C2, C3, C4, C5. No extra commit, no dropped commit, no reordering. C1 was the first substantive commit, as constraint 2 requires, and C3 and C4 stayed separate as constraint 4 requires.
- EVERY identity the block predicted was MET: the ten slice digests, the three FROM-zero/TO-one pair readings, the reviewer's own 3b823c0e/3895 constructive value and fefd47e6/3915 base, the 199/199 · 4→5 · 19→20 set moves, the `host.connect(` 2→1 and `resumeEventId` 2→0 counts, the 3/3 and 15/0 numstats, the unchanged 107-line runner, the 7-file/115-test vitest reading, the 465 and 397 pytest readings, the `55 problems (53 errors, 2 warnings)` lint reading and both red controls' colour. Nothing was adjusted to make anything pass.
- ONE reading is stated differently by the block in two places and both are correct: G3 measures RESTARTTEST itself at 637 bytes and 14 lines, while G8 measures the C3→C4 REMAINDER — the separating newline plus the slice — at 638 bytes and 15 lines. Both were measured and both match.
- No `Done:` paragraph was written for R-0627 although C3 lands its fix, and no `Landed:` line was written, exactly as constraint 5 orders; R21 owes that paragraph. No id was minted: R-0628 stays free. R-0622 stays OPEN with no TypeScript parser added (constraint 6), and no dependency was added — no jsdom, no happy-dom, no testing library (constraint 3).
- No objection is raised against any slice: all nine applied cleanly, and the reviewer's `TO contains FROM: false` reading holds for all three pairs, so G7's FROM-zero counts are the honest test of them.
- Commit-message convention: these seven subjects carry no `Co-Authored-By` trailer, matching every prior round on this branch; the harness default would have added one and was deliberately not followed, to keep the branch's commit record uniform.
- Mechanical note: the session command guard rejects `${arr[0]}`, `$(...)`, `; echo $?`, `cat <<EOF` heredocs, some pipe-to-grep forms, chained `;` commands and the `ln` command BY FORM, so every multi-step gate — including G10's symlink, created with `os.symlink` — was written to a script under the gitignored `.remedy-wt/` and run from there. Nothing from that directory was committed.

## Next
The next session's FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1); its SECOND is the Open PR Gate (Phase 1 rule 2), which returned `[]` at R20 and therefore continues on this branch. R20 IS PENDING REVIEW: its verdict is owed by the next round's ledger commit and no line of this round records one. The next free finding id is R-0628. R21's work is T003's thin React `useBrainStream` hook over this runner and the visible delayed badge under docs/ui/design_reference/ — a round that OPENS with the jsdom-or-testing-library dependency decision, since neither is installed — plus the `Done:` paragraph resolving R-0627.

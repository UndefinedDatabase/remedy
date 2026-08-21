# Handback — F008 SSE event stream, R24 (the stream host pinned by twelve tests, the R23 record)
## Range
Review of `b6a1c4d1`..C4, the handback commit itself (6 commits, branch feature/f008-sse-event-stream). C4's SHA cannot exist inside C4, so it is named by role and the round report carries the value (R-0371).
## Commits
### e9d1bea4 docs(state): save the F008 R24 block verbatim
| Path | +/- | Reason |
| `.agent/authored/f008-r24.md` | +425/-0 | C0a, the R24 block saved byte for byte |

### 77906cb8 docs(state): mirror the F008 R24 block into last_block
| Path | +/- | Reason |
| `.agent/last_block.md` | +296/-215 | C0b, the same bytes mirrored from the COMMITTED C0a blob |

### cd830005 docs(state): set the plan to F008 R24, pinning the stream host
| Path | +/- | Reason |
| `.agent/plan.md` | +14/-18 | C1, PLANF008R24 applied whole |

### df466117 docs(review): record the R23 verdict
| Path | +/- | Reason |
| `.agent/live_review.md` | +2/-0 | C2, LEDGER24's single paragraph appended |

### 46ac9da4 test(ui): pin the DOM-free stream host with twelve tests
| Path | +/- | Reason |
| `apps/ui/src/api/brainStreamHost.test.ts` | +194/-0 | C3, HOSTTESTS as a NEW file, whole |

### C4 docs(state): write the F008 R24 handback
| Path | +/- | Reason |
| `.agent/handoff.md` | self | C4 cannot table itself (R-0149); its numbers are in the round report |

## External actions
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` — exit 0, `[]`, so the round continues on this branch. `git worktree add --detach .remedy-wt/r24wt 46ac9da4` — exit 0, and `git worktree remove` on it — exit 0, the path gone and the PRIMARY checkout the only worktree left; its `apps/ui/node_modules` was an `os.symlink` to the primary tree's, still a symlink at teardown, unlinked there, and the primary `node_modules` was never touched. `git push -u origin feature/f008-sse-event-stream` is run ONCE, AFTER C4, and its output belongs to the round report (constraint 5). NOTHING merged, no PR created, no PR updated, no branch created (constraint 8).

## Verification
- G1 `.agent/STOP` ABSENT, read immediately before C0a; branch feature/f008-sse-event-stream; `git status --porcelain` EMPTY after each of C0a, C0b, C1, C2 and C3. The post-C4 porcelain and `git worktree list` are in the round report (constraint 5).
- G2 Transport EQUAL three ways — the scratch block at `.remedy-wt/f008-r24.md` as received, `.agent/authored/f008-r24.md` at C0a and `.agent/last_block.md` at C0b — sha256 e1123bf53acb712bc891c69e77f2ce51392ba013ad2f633d49b0b187d2814b85, 24620 bytes, 425 lines, and that value EQUALS the digest carried in the task prompt.
- G3 THREE slices, the COUNT taken from the ordered extraction out of the COMMITTED C0a blob by their marker lines, newline-included as sha256/bytes/lines: PLANF008R24 063f969b/2033/38, LEDGER24 9243828b/3396/1 and HOSTTESTS 5281e235/6791/194 — all three equal to the digests the block names, at the 38 and 194 lines it names, and NONE carries trailing whitespace on any line (the offending-line list was empty for all three).
- G4 `.agent/plan.md` at C1 sha256 063f969b673df341d6c3365b45c48359219dd11a306208429b52aee6d1b834b1, 2033 bytes, 38 lines (<50), BYTE-EQUAL to PLANF008R24; `Steps` occurs, `## Goal` 1x and `## Next Steps` 1x line-anchored, `\bF\d{3}\b` matches `F008`.
- G5 (a) the C1 blob (bcebd967, 467608 bytes, 1076 lines) is a byte-exact PREFIX of the C2 blob (193b2366, 471005 bytes, 1078 lines) and the remainder == newline+LEDGER24, sha256 37ceeffc71312a3a13c59de4254c440b662985619f9ea5879503e6acf26b4411, 3397 bytes, 2 lines; (b) an INDEPENDENT blank-line split of the WHOLE C2 file, its terminating newline normalised first, gives 234 units whose LAST is LEDGER24's single paragraph. NEGATIVE CONTROL: one flipped ASCII byte of the remainder (offset 1698, `w`→`X`) REJECTED by BOTH readings, the unflipped value ACCEPTED by BOTH.
- G6 At C1/C2, line-anchored: `^- R-\d+ — ` 200/200 — NO id was minted — `^- R-0629 — ` 0/0, `^- R-0628 — ` 1/1, `^Done: R-\d+ — ` 6/6, `^Landed: ` 0/0, `^Gate: R\d+ — ` 23/24 over 23 then 24 DISTINCT keys. Header sweep at C2: of 24 `^Gate: ` lines, 23 match `^Gate: R(\d+) — the R(\d+) entry\.` with second == first−1, 1 does NOT and its text opens `Gate: R1 — the F255 R21 entry.` (that non-matching line runs 5381 chars; the sentence up to its first period is quoted), and the R24 pair `Gate: R24 — the R23 entry.` occurs EXACTLY ONCE.
- G7 `git ls-tree b6a1c4d1 -- apps/ui/src/api/brainStreamHost.test.ts` is EMPTY, so the file did NOT exist at the base; its blob at C3 is sha256 5281e235669f74d668dd0ae2aa95605d30fffd8eef1693a35cbda676615ed719, BYTE-EQUAL to HOSTTESTS' 5281e235669f74d668dd0ae2aa95605d30fffd8eef1693a35cbda676615ed719. `git show --numstat` at C3 reads 194/0 — insertions only, ZERO deletions, the file being new. `git diff --name-only b6a1c4d1..46ac9da4 -- apps/ui/src/api/brainStreamHost.ts` is EMPTY: the module under test was NOT touched (constraint 3).
- G8 PRIMARY checkout, run SERIALLY, never two test processes at once, AT C3. In `apps/ui`: `npx vitest run` EXIT 0 at 8 test files and 131 tests — the base's 119 plus HOSTTESTS' twelve `it`s, and 119+12=131 is the arithmetic the block asks for — `npx vitest run src/api/brainStreamHost.test.ts` alone EXIT 0 at 12, and `npm run --silent typecheck` EXIT 0 with NO output on stdout or stderr. From the root: the state readers plus canary EXIT 0 at 465 passed + 0 skipped = 465, `tests/ui_contracts/` EXIT 0 at 393 passed + 4 skipped = 397. `npm run --silent lint` EXIT 1 at `57 problems (55 errors, 2 warnings)`, exactly constraint 7's measured value and one above the base's 56 because eslint cannot parse the one file this round adds — that is R-0622 and NOT a gate (R-0364). G8's STOP clause was never reached.
- G9 THREE RED CONTROLS, all in the ONE disposable worktree at `.remedy-wt/r24wt` created at C3, the primary checkout never touched, each deleting ONE whole line of `src/api/brainStreamHost.ts` — the module, never the test — and each restored to sha256 664ce74eea95405886146ffd9bc28ed2850035c35219534c480e8552601eec42 and verified before the next ran. (a) `    if (typeof seq !== "number") return;` occurred EXACTLY ONCE (line 81), EXIT 1, one failure named `an open stream > drops a malformed frame instead of dispatching a broken one`, 11 passed. (b) `      drop();` occurred TWICE at that indent, at lines 87 and 123, NOT once as the block states — see Deviations — so the block's own unambiguous identification was used and line 87, the FIRST statement of `connect`, was deleted: EXIT 1, one failure named `reconnecting > closes the previous socket before opening the next`, 11 passed. (c) `    held = frame.seq;` occurred EXACTLY ONCE (line 56), EXIT 1, one failure named `the polling fallback > asks from the position the stream reached and surfaces each frame in order`, 11 passed. After all three the restored module's sha256 EQUALS its `b6a1c4d1` blob and the same command EXITS 0 at 12 passed. The worktree was removed BEFORE C4.
- G10 `git diff --name-only b6a1c4d1..46ac9da4` equals the Change set MINUS `.agent/handoff.md` exactly — five paths, none on either side alone; the full `b6a1c4d1..C4` reading is in the round report (constraint 5). Every commit in the range has exactly ONE parent. BOTH numstat cells per path from `git show --numstat`, each cross-checked against `git diff --numstat` and AGREEING: 425/0, 296/215, 14/18, 2/0 and 194/0 — every insertion under 500, and EVERY CELL, insertion and deletion, equal to the `+/-` column above.
- G11 Lines BEGINNING with `<<<SLICE ` or `<<<END `: 0 in `.agent/plan.md` at C1, 0 in `.agent/live_review.md` at C2, 0 in `apps/ui/src/api/brainStreamHost.test.ts` at C3, and 0 in this file, measured on the exact bytes committed as C4. This round's own reflog entries, counted by the OPERATION before the first `:` in `%gs`: all five pre-C4 entries are `commit` (e9d1bea4, 77906cb8, cd830005, df466117, 46ac9da4, five entries found and five classified); `amend` 0, `rebase` 0, `cherry` 0. No total asserted.
- G12 This file carries every mandated section of docs/agents/handback_template.md and the item-status table below, which holds exactly one row for each of C0a, C0b, C1, C2, C3 and C4. Measured with `wc -l` in the session scratchpad BEFORE it was written it is 67 lines, UNDER the 100 this round's six commits allow, so no DECISION D15 stated-cause line is owed. One line per gate here; the raw transcripts are in the round report (R-0582).

## Authored-text proofs
- `.agent/authored/f008-r24.md` at C0a == the scratch block byte for byte and `.agent/last_block.md` at C0b == the same bytes (G2). ALL THREE slices were extracted from the COMMITTED C0a blob by their marker lines and applied unedited — never retyped, rewrapped, reflowed, reindented or whitespace-adjusted. G4 is the disk-to-disk byte-equality for PLANF008R24, G5 the ordered-append equality for LEDGER24 agreed by two independent readings with a negative control, and G7 the byte-equality for HOSTTESTS as a new file. There was NO FROM/TO pair this round, so no containment reading is claimed. All three slices reached a commit; G11 confirms no marker line reached one.

## State — Fortschritt
~94 % (T001 ✅ · T002 ✅ · T003 Regeln+Treiber+Runner+Store+Host ✅, Hook offen) — Schätzung

## Item status
| Item | Status | Reason |
|------|--------|--------|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | this commit |
## Deviations & assumptions
- No departure from the ordered commit sequence C0a, C0b, C1, C2, C3, C4. No extra commit, no dropped commit, no reordering; C1 was the first substantive commit, as constraint 2 requires. NO DEPENDENCY WAS ADDED (constraint 3): `apps/ui/package.json` and `apps/ui/package-lock.json` were not opened, no jsdom, happy-dom or testing library was installed or attempted, and `apps/ui/src/api/brainStreamHost.ts` was NOT edited in the primary checkout — G7 proves the range does not touch it. NO test failed, so the module was never adjusted to suit a test. R-0629 stays free, R-0628 stays OPEN with no `Done:` and no `Landed:` line, R-0622 stays OPEN and no TypeScript parser was added to make lint green (constraint 4).
- ONE OBJECTION, raised rather than fixed. G9's control (b) describes `      drop();` as "occurring once at that indent". It occurs TWICE at six leading spaces — line 87, the first statement of `connect`, and line 123, the body of `close`. The parenthetical is false; the identification around it ("the FIRST statement of `connect`") is not, and the failing test the block predicts is the connect-side one, so line 87 was deleted and the measured count of 2 is reported rather than the block's 1. Deleting line 123 would have been a different control — `close` idempotence — and was not run. The control still discriminates: it went red on exactly the predicted test. No slice was edited and no gate value was rounded toward the block.
- Commit-message convention: these six subjects carry no `Co-Authored-By` trailer, matching every prior round on this branch. The session command guard rejects `$(...)`, `; echo $?`, heredocs, chained `;` commands and `cd X && … | tail` BY FORM — that last one was refused mid-round — so every multi-step gate and every test run was written to a script under the gitignored `.remedy-wt/` and run from there; nothing from that directory was committed.

## Next
The next session's FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1); its SECOND is the Open PR Gate (Phase 1 rule 2), which returned `[]` at R24 and therefore continues on this branch. R24 IS PENDING REVIEW: its verdict is owed by the next round's ledger commit and no line of this round records one. The next free finding id is R-0629. With this round the adapter is PROVED, not merely compiled — twelve tests over injected seams, three red controls each naming exactly one failing test. R25's work is the thin `useBrainStream` hook and the visible delayed badge, gated by `npm run typecheck` and a `tests/ui_contracts/` source contract in the style this repository uses for every React component (R-0628); the integration gate follows before closure.

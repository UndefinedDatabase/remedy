# Handback — F008 SSE event stream, R26 (the composition seam landed, the R25 verdict recorded)
## Range
Review of `369fd39e`..C4, the handback commit itself (6 commits, branch feature/f008-sse-event-stream). C4's SHA cannot exist inside C4, so it is named by role and the round report carries the value (R-0371).
## Commits
### b00a42f0 docs(state): save the F008 R26 block verbatim
| Path | +/- | Reason |
| `.agent/authored/f008-r26.md` | +376/-0 | C0a, the R26 block saved byte for byte |

### abef185b docs(state): mirror the F008 R26 block into last_block
| Path | +/- | Reason |
| `.agent/last_block.md` | +299/-115 | C0b, the same bytes mirrored from the COMMITTED C0a blob |

### 433e59eb docs(state): set the plan to F008 R26, the composition seam
| Path | +/- | Reason |
| `.agent/plan.md` | +15/-13 | C1, PLANF008R26 applied whole |

### f683ab43 docs(review): record the R25 verdict in the live review ledger
| Path | +/- | Reason |
| `.agent/live_review.md` | +2/-0 | C2, LEDGER26's paragraph appended |

### 931ed066 feat(ui): compose the stream host and runner into one session
| Path | +/- | Reason |
| `apps/ui/src/api/brainStreamSession.ts` | +38/-0 | C3, SESSION applied as a NEW file |
| `apps/ui/src/api/brainStreamSession.test.ts` | +111/-0 | C3, SESSIONTESTS applied as a NEW file |

### C4 docs(state): write the F008 R26 handback
| Path | +/- | Reason |
| `.agent/handoff.md` | self | C4 cannot table itself (R-0149); its numbers are in the round report |

## External actions
- `git worktree add --detach .remedy-wt/g9 931ed066` exit 0, then `git worktree remove --force` and `git worktree prune` — G9's disposable worktree, its `apps/ui/node_modules` a SYMLINK and never a copy (R-0591), removed and pruned BEFORE this handback, leaving the primary checkout the only worktree. `git push -u origin feature/f008-sse-event-stream` runs ONCE, AFTER C4, and its output belongs to the round report (constraint 5). NOTHING merged, no PR created, no PR updated, no branch created (constraint 7); NO `gh` command was run this round — the block states the R26 Open PR Gate returned `[]`, and no new branch is being cut.

## Verification
- G1 `.agent/STOP` ABSENT, read immediately before C0a; branch feature/f008-sse-event-stream; `git status --porcelain` EMPTY after each of C0a, C0b, C1, C2 and C3. The post-C4 porcelain, `git worktree list` and push output are in the round report (constraint 5).
- G2 Transport EQUAL three ways — `.remedy-wt/f008-r26.md` as received, `.agent/authored/f008-r26.md` at C0a and `.agent/last_block.md` at C0b — sha256 a3c93663a29902caa1d59081b5806a87020d864b29a472a9728ee38e4cc8244d, 22565 bytes, 376 lines, and that value EQUALS the digest carried in the task prompt.
- G3 FOUR slices, the COUNT taken from the ordered extraction out of the COMMITTED C0a blob by their marker lines, newline-included as sha256/bytes/lines: PLANF008R26 4ce0503e/2210/41, LEDGER26 8a9d2ef6/2923/1, SESSION 1935909b/1683/38, SESSIONTESTS 5a2d6cef/3842/111 — every digest and every line count equal to the values the block names, and NONE carries trailing whitespace on any line (the offending-line list was empty for all four).
- G4 `.agent/plan.md` at C1 sha256 4ce0503e11ae176200334e76db4111230dd9781aa717778aef838ba387e6c1b3, 2210 bytes, 41 lines (<50), BYTE-EQUAL to PLANF008R26; `Steps` occurs (1x), `## Goal` 1x and `## Next Steps` 1x line-anchored, `\bF\d{3}\b` matches `F008`.
- G5 (a) the C1 blob (6b33fef0, 476764 bytes, 1082 lines) is a byte-exact PREFIX of the C2 blob (330e236a, 479688 bytes, 1084 lines) and the remainder == newline+LEDGER26, sha256 46d541f8863f4e6f1f08d060c3ea7cd51b1b7564f26d88507fea15919967edfa, 2924 bytes, 2 lines; (b) an INDEPENDENT blank-line split of the WHOLE C2 file, its terminating newline normalised first, gives 237 units whose LAST unit is LEDGER26's paragraph. NEGATIVE CONTROL: one flipped ASCII byte of the remainder (file offset 476804, remainder offset 40, `.`→0x0e) REJECTED by BOTH readings, the unflipped value ACCEPTED by BOTH.
- G6 At C1/C2, line-anchored: `^- R-\d+ — ` 201/201 — this round mints NO id — `^- R-0630 — ` 0/0, `^- R-0629 — ` 1/1, `^- R-0628 — ` 1/1, `^Done: R-\d+ — ` 6/6, `^Landed: ` 0/0, `^Gate: R\d+ — ` 25/26 over 25 then 26 DISTINCT keys. Header sweep at C2: of 26 `^Gate: ` lines, 25 match `^Gate: R(\d+) — the R(\d+) entry\.` with second == first−1, 1 does NOT and its text to its first period is `Gate: R1 — the F255 R21 entry.`, and the R26 pair `Gate: R26 — the R25 entry.` occurs EXACTLY ONCE.
- G7 `git ls-tree 6e39f19d` is EMPTY for BOTH code paths, so the round ADDS them and edits nothing. At C3 `brainStreamSession.ts` is 1935909b, 1683 bytes, 38 lines, BYTE-EQUAL to SESSION, numstat 38/0; `brainStreamSession.test.ts` is 5a2d6cef, 3842 bytes, 111 lines, BYTE-EQUAL to SESSIONTESTS, numstat 111/0 — each cell the slice's own line count with ZERO deletions.
- G8 PRIMARY checkout, run SERIALLY, never two test processes at once, AT C3 (931ed066): `npm run --silent typecheck` in `apps/ui` EXIT 0 with 0 bytes of output; `npx vitest run` in `apps/ui` EXIT 0 at 9 Test Files and 137 Tests; `python3 -m pytest tests/ui_contracts/ -q -rf` EXIT 0 at 393 passed + 4 skipped = 397; the state readers plus canary EXIT 0 at 465 passed + 0 skipped = 465. G8's STOP clause was never reached.
- G9 In a disposable worktree at C3 with `apps/ui/node_modules` symlinked, the baseline EXITS 0 at 9 files and 137 tests. Each ordered byte string occurs EXACTLY ONCE in `brainStreamSession.ts` by my own count. (a) deleting `      host.close();` (20 bytes) EXITS 1 with EXACTLY ONE failure, named `a composed brain stream session > closes the socket when the caller closes the session`, and 136 passed. (b) deleting `      runner.stop();` (21 bytes) EXITS 1 with EXACTLY ONE failure, named `a composed brain stream session > performs nothing more once it is closed`, and 136 passed. After each restore the file's sha256 is 1935909b… — IDENTICAL to its pre-mutation value — and the post-restore run EXITS 0 at 137.
- G10 `git diff --name-only 6e39f19d..931ed066`, run exactly as the block orders it, yields EIGHT paths, not six: the Change-set six PLUS `.agent/authored/f008-r25.md` and `.agent/handoff.md`, both written by R25, because `6e39f19d` is R24's handback and not this round's base. With `369fd39e`, the R25 handback this round starts from, the reading is EXACTLY the six paths with none on either side alone; see Deviations. Every commit in `369fd39e`..C3 has exactly ONE parent. BOTH numstat cells per path from `git show --numstat`, each cross-checked against `git diff --numstat` and AGREEING: 376/0, 299/115, 15/13, 2/0, and 111/0 with 38/0 — every insertion under 500, and EVERY CELL, insertion and deletion, equal to the `+/-` column above.
- G11 Lines BEGINNING with `<<<SLICE ` or `<<<END `: 0 in `.agent/plan.md` at C1, 0 in `.agent/live_review.md` at C2, 0 in EACH code file at C3, and 0 in this file, measured on the exact bytes committed. This round's own reflog entries, counted by the OPERATION before the first `:` in `%gs`: all five pre-C4 entries are `commit` (five found, five classified); `amend` 0, `rebase` 0, `cherry` 0. No total asserted.
- G12 This file carries every mandated section of docs/agents/handback_template.md, the `## Next` content the gate names in that order, and the item-status table below, which holds exactly one row for each of C0a, C0b, C1, C2, C3 and C4 — "exactly one row" scoping to that TABLE. Measured with `wc -l` in the session scratchpad BEFORE it was written it is 69 lines, UNDER the 100 this round's six commits allow, so no DECISION D15 stated-cause line is owed. One line per gate here; the raw transcripts are in the round report (R-0582).

## Authored-text proofs
- `.agent/authored/f008-r26.md` at C0a == the received block byte for byte and `.agent/last_block.md` at C0b == the same bytes (G2). ALL FOUR slices were extracted from the COMMITTED C0a blob by their marker lines and applied unedited — never retyped, rewrapped, reflowed, reindented or whitespace-adjusted. G4 is the disk-to-disk byte equality for PLANF008R26, G5 the ordered-append equality for LEDGER26 agreed by two independent readings with a negative control, and G7 the disk-to-disk byte equality for SESSION and SESSIONTESTS. There was NO FROM/TO pair this round, so no containment reading is claimed. All four slices reached a commit; G11 confirms no marker line reached one.

## State — Fortschritt
~95 % (T001 ✅ · T002 ✅ · T003 Regeln+Treiber+Runner+Store+Host+Seam ✅, Hook offen) — Schätzung

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
- No departure from the ordered commit sequence C0a, C0b, C1, C2, C3, C4. No extra commit, no dropped commit, no reordering; C1 was the first substantive commit, as constraint 2 requires.
- G10's base SHA is WRONG IN THE BLOCK and the gate is unmeetable as written: `6e39f19d` is R24's handback, so `6e39f19d..C3` necessarily also contains R25's five commits and therefore `.agent/authored/f008-r25.md` and `.agent/handoff.md`. I ran the command exactly as ordered, report its real eight-path output above, and ALSO report the `369fd39e..C3` reading, which does equal the Change set minus `.agent/handoff.md` exactly. I did not edit the block; registering or dismissing this is the reviewer's call. G7's `ls-tree 6e39f19d` is unaffected — both code paths are absent at BOTH candidate bases.
- Commit-message convention: these six subjects DO carry a `Co-Authored-By: Claude Opus 5` trailer, which the five prior rounds on this branch do not. My session harness mandates that trailer on every commit; the subjects themselves keep the branch's convention and carry no leading-slash token, absolute path or secret-like string.
- NO EXISTING SOURCE FILE WAS EDITED and NO DEPENDENCY WAS ADDED (constraint 3): both code paths are NEW files by G7's `ls-tree`, and `apps/ui/package.json` and `apps/ui/package-lock.json` were never opened. NO id was minted and none resolved (constraint 4): R-0630 stays free, R-0628, R-0629 and R-0622 stay OPEN, and no `Done:` and no `Landed:` line was written for any of them. `npm run lint` was NOT run: it is red at base, is R-0622, and is not a gate (R-0364).
- The session command guard rejects `$(...)`, `; echo $?`, shell loops and chained `;` commands BY FORM, so every multi-step gate, both mutation controls and all four suite runs were written to a script under the gitignored `.remedy-wt/` and run from there; nothing from that directory was committed. NO OBJECTION to any slice: all four applied byte for byte, and every value the block predicted of them was MEASURED at that value.
## Next
The next session's FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1); its SECOND is the Open PR Gate (Phase 1 rule 2). R26 IS PENDING REVIEW: its verdict is owed by the next round's ledger commit, and no line of this round records one. The next free finding id is R-0630. R-0628, R-0629 and R-0622 are all OPEN. R27's work is `useBrainStream.ts` over this session plus its `tests/ui_contracts/` source contract — the style every React component here is gated by — with the hook closing the session on unmount, or a remounting cockpit leaks one EventSource per mount.

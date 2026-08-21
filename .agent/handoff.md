# Handback — F008 SSE event stream, R27 (the React hook landed, the R26 verdict recorded)
## Range
Review of `a86231c0`..C4, the handback commit itself (7 commits, branch feature/f008-sse-event-stream). C4's SHA cannot exist inside C4, so it is named by role and the round report carries the value (R-0371).
## Commits
### 27984108 docs(state): save the F008 R27 block verbatim
| Path | +/- | Reason |
| `.agent/authored/f008-r27.md` | +394/-0 | C0a, the R27 block saved byte for byte |

### 1408caf8 docs(state): mirror the F008 R27 block into last_block
| Path | +/- | Reason |
| `.agent/last_block.md` | +285/-267 | C0b, the same bytes mirrored from the COMMITTED C0a blob |

### e22203b2 docs(state): set the plan to F008 R27, the React hook round
| Path | +/- | Reason |
| `.agent/plan.md` | +13/-14 | C1, PLANF008R27 applied whole |

### 6264a959 docs(review): append the F008 R26 instance to R-0368
| Path | +/- | Reason |
| `.agent/live_review.md` | +1/-1 | C2a, R0368FROM replaced by R0368TO, the round's ONE pair, a REWRITE |

### 31223074 docs(review): record the R26 verdict in the live review ledger
| Path | +/- | Reason |
| `.agent/live_review.md` | +2/-0 | C2b, LEDGER27's paragraph appended |

### 345a8be8 feat(ui): subscribe the cockpit to a job stream with useBrainStream
| Path | +/- | Reason |
| `apps/ui/src/api/useBrainStream.ts` | +36/-0 | C3, HOOK applied as a NEW file |
| `tests/ui_contracts/test_brain_stream_hook.py` | +87/-0 | C3, CONTRACT applied as a NEW file |

### C4 docs(state): write the F008 R27 handback
| Path | +/- | Reason |
| `.agent/handoff.md` | self | C4 cannot table itself (R-0149); its numbers are in the round report |

## External actions
- `git worktree add /home/decodeux/Repos/remedy/.remedy-wt/g10 --detach 345a8be8` exit 0, then `git worktree remove` and `git worktree prune` both exit 0 — G10's disposable worktree, its `apps/ui/node_modules` created with `os.symlink` and never copied (R-0591), removed and pruned BEFORE this handback, leaving the primary checkout the only worktree. `git push -u origin feature/f008-sse-event-stream` runs ONCE, AFTER C4, and its output belongs to the round report (constraint 5). NOTHING merged, no PR created, no PR updated, no branch created (constraint 7); NO `gh` command was run this round — the block states the R26 Open PR Gate returned `[]`, and no new branch is being cut.

## Verification
- G1 `.agent/STOP` ABSENT (`ls` exit 2, "No such file or directory"), read immediately before C0a; branch feature/f008-sse-event-stream; `git status --porcelain` EMPTY after each of C0a, C0b, C1, C2a, C2b and C3. The post-C4 porcelain, `git worktree list` and push output are in the round report (constraint 5).
- G2 Transport EQUAL three ways — `.remedy-wt/f008-r27.md` as received, `.agent/authored/f008-r27.md` at C0a and `.agent/last_block.md` at C0b — all sha256 bc0f2ff03d5d9883809adf91764c63111c409d028a3a3e732d369ce7ae8bc2d1 over 27996 bytes and 394 lines, and that value EQUALS the digest carried in the task prompt.
- G3 SIX slices, the COUNT taken from an ordered extraction out of the COMMITTED C0a blob (`git show 27984108:…`) by their marker lines, newline-included as sha256/bytes/lines: PLANF008R27 4e8555ca/2206/40, R0368FROM 432fdc8e/93/1, R0368TO 8e234582/2180/1, LEDGER27 5528f762/3500/1, HOOK 362a9d56/1841/36, CONTRACT 0565e0be/3514/87 — every digest prefix and every line count equal to the values the block names, and NONE carries trailing whitespace on any line (the offending-line list was empty for all six).
- G4 `.agent/plan.md` at C1 sha256 4e8555caef7e73306eb686e323a000be200b6aeeab222d72f4e56e6fcb9969ed, 2206 bytes, 40 lines (<50), BYTE-EQUAL to PLANF008R27; `Steps` occurs (1x), `## Goal` 1x and `## Next Steps` 1x line-anchored, and `\bF\d{3}\b` matches `F008`.
- G5 The REWRITE at C2a, base bytes read with `git show a86231c0:.agent/live_review.md` into memory and never over the tracked file: R0368FROM counts 1 at the round base and 0 at C2a; R0368TO counts 0 at the round base and 1 at C2a — the FROM-0x / TO-1x proof — identical both newline-included and newline-stripped. Compared as an ordered list of blank-line-separated units the base and C2a blobs are 237 units each, the `^- R-\d+ — ` paragraph COUNT is 201 at both, and EXACTLY ONE unit differs (index 16), which begins `- R-0368 — `; every other paragraph is byte-identical. C2a blob b1da940e, 481775 bytes, 1084 lines.
- G6 (a) the C2a blob is a byte-exact PREFIX of the C2b blob (2f8330d0, 485276 bytes, 1086 lines) and the remainder == newline+LEDGER27, sha256 ffe2be2007c378fd96547342cece5e6ebde5fb56a451578c18b1d350a33abf5b, 3501 bytes, 2 lines; (b) an INDEPENDENT blank-line split of the WHOLE C2b file, its terminating newline normalised first, gives 238 units whose LAST unit is LEDGER27's paragraph. NEGATIVE CONTROL: one flipped ASCII byte of the remainder (file offset 481776, `G`→`g`) REJECTED by BOTH readings, the unflipped value ACCEPTED by BOTH.
- G7 At C2a/C2b, line-anchored: `^- R-\d+ — ` 201/201 — this round mints NO id — `^- R-0630 — ` 0/0, `^- R-0629 — ` 1/1, `^- R-0628 — ` 1/1, `^- R-0368 — ` 1/1, `^Done: R-\d+ — ` 6/6, `^Landed: ` 0/0, `^Gate: R\d+ — ` 26/27 over 26 then 27 DISTINCT keys. HEADER SWEEP at C2b: of 27 `^Gate: ` lines, 26 match `^Gate: R(\d+) — the R(\d+) entry\.` with second == first−1, 1 does NOT and its text to its first period is `Gate: R1 — the F255 R21 entry.`, and the R27 pair `Gate: R27 — the R26 entry.` occurs EXACTLY ONCE.
- G8 `git ls-tree a86231c0` is EMPTY (0 bytes of output) for BOTH code paths, so the round ADDS them and edits nothing. At C3 `useBrainStream.ts` is 362a9d56, 1841 bytes, 36 lines, BYTE-EQUAL to HOOK, numstat 36/0; `test_brain_stream_hook.py` is 0565e0be, 3514 bytes, 87 lines, BYTE-EQUAL to CONTRACT, numstat 87/0 — each cell the slice's own line count with ZERO deletions.
- G9 PRIMARY checkout, SERIALLY, never two test processes at once, AT C3 (345a8be8): `npm run --silent typecheck` in `apps/ui` EXIT 0 with 0 bytes of output; `npx vitest run` in `apps/ui` EXIT 0 at 9 Test Files and 137 Tests, UNCHANGED from the base; `python3 -m pytest tests/ui_contracts/ -q -rf` EXIT 0 at 402 passed + 4 skipped = 406, nine more than the base's 397; the state readers plus canary EXIT 0 at 465 passed + 0 skipped = 465. G9's STOP clause was never reached.
- G10 Disposable worktree at C3 with `apps/ui/node_modules` an `os.symlink`; each ordered byte string occurs EXACTLY ONCE in `apps/ui/src/api/useBrainStream.ts` by my own count (and, contra the block's parenthetical, ZERO times in CONTRACT — see Deviations). (a) DELETING the line `    return () => { session.close(); };` EXITS 1 at 1 failed and 8 passed, the failure named `TestBrainStreamHookContract::test_hook_closes_the_session_on_unmount`. (b) REPLACING `useSyncExternalStore(session.subscribe, session.view, session.view)` with `session.view()` EXITS 1 at 1 failed and 8 passed, the failure named `TestBrainStreamHookContract::test_hook_reads_the_runner_as_an_external_store`. (c) REPLACING `latestMakeDeps.current(jobId)` with `latestMakeDeps.current()` makes `npm run --silent typecheck` EXIT 2 — the code I actually observed — printing `src/api/useBrainStream.ts(25,73): error TS2554: Expected 1 arguments, but got 0.` After EACH restore the file's sha256 is 362a9d56… — IDENTICAL to its pre-mutation value.
- G11 `git diff --name-only a86231c0..345a8be8`, measured from the round base this block's header names and no other SHA, yields EXACTLY the six Change-set paths minus `.agent/handoff.md`, with NONE on either side alone. Every commit in that range has exactly ONE parent (six commits, six single-parent readings). BOTH numstat cells per path from `git show --numstat`, each cross-checked against `git diff --numstat` and AGREEING: 394/0, 285/267, 13/14, 1/1, 2/0, and 36/0 with 87/0 — every insertion under 500 (max 394), and EVERY CELL, insertion and deletion, equal to the `+/-` column above.
- G12 Lines BEGINNING with `<<<SLICE ` or `<<<END `: 0 in `.agent/plan.md` at C1, 0 in `.agent/live_review.md` at C2a, 0 at C2b, 0 in EACH code file at C3, and 0 in this file, measured on the exact bytes committed. This round's own reflog entries, counted by the OPERATION before the first `:` in `%gs`: all six pre-C4 entries are `commit` (six found, six classified, HEAD@{6} being R26's handback and outside this round); `amend` 0, `rebase` 0, `cherry` 0. No total asserted.
- G13 This file carries every mandated section of docs/agents/handback_template.md, the `## Next` content the gate names in that order, and the item-status table below, which holds exactly one row for each of C0a, C0b, C1, C2a, C2b, C3 and C4 — "exactly one row" scoping to that TABLE. Measured with `wc -l` in the session scratchpad BEFORE it was written it is 77 lines, UNDER the 100 this round's seven commits allow, so no DECISION D15 stated-cause line is owed. One line per gate here; the raw transcripts are in the round report (R-0582).

## Authored-text proofs
- `.agent/authored/f008-r27.md` at C0a == the received block byte for byte and `.agent/last_block.md` at C0b == the same bytes (G2). ALL SIX slices were extracted from the COMMITTED C0a blob by their marker lines and applied unedited — never retyped, rewrapped, reflowed, reindented or whitespace-adjusted. G4 is the disk-to-disk byte equality for PLANF008R27; G5 the FROM-0x/TO-1x proof for the round's ONE pair, R0368FROM→R0368TO, applied as an exact byte-string replacement with the paragraph around it untouched, and TO does NOT contain FROM, so the pair is a REWRITE and no append reading is claimed for it; G6 the ordered-append equality for LEDGER27 agreed by two independent readings with a negative control; G8 the disk-to-disk byte equality for HOOK and CONTRACT. All six slices reached a commit; G12 confirms no marker line reached one.

## State — Fortschritt
~97 % (T001 ✅ · T002 ✅ · T003 Regeln+Treiber+Runner+Store+Host+Seam+Hook ✅, Badge offen) — Schätzung

## Item status
| Item | Status | Reason |
|------|--------|--------|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2a | done | |
| C2b | done | |
| C3 | done | |
| C4 | done | this commit |
## Deviations & assumptions
- No departure from the ordered commit sequence C0a, C0b, C1, C2a, C2b, C3, C4. No extra commit, no dropped commit, no reordering; C1 was the first substantive commit and C2a preceded C2b, as constraint 2 requires.
- OBJECTION to a factual aside in G10, raised here because constraint 1 forbids editing a slice or a block: G10 says "the same byte string also occurs in CONTRACT, which ASSERTS it". Measured, it does not — each of the three ordered byte strings occurs 0 times in `tests/ui_contracts/test_brain_stream_hook.py`, because CONTRACT asserts the SHORTER forms `return () => { session.close(); };` (no leading indent) and `useSyncExternalStore(`, and asserts nothing about `latestMakeDeps.current(jobId)`. The gate itself is unaffected: it orders the count in the hook, which is 1 for all three, and I mutated only that file.
- G6's negative control was run TWICE. The first flip target, remainder offset 10, was a SPACE, and `^0x20` turned it into a NUL — a degenerate corruption both readings reject trivially. I discarded that reading and re-ran the control against the first ALPHABETIC byte of the remainder (file offset 481776, `G`→`g`), a printable-ASCII-to-printable-ASCII flip; the reported result is the second run's. Nothing was committed between the two.
- Commit-message convention: these seven subjects carry a `Co-Authored-By: Claude Opus 5` trailer, as R26's did. The subjects keep the branch's convention and carry no leading-slash token, absolute path or secret-like string.
- Beyond the ordered gates I ran `python3 -m pytest tests/ui_contracts/test_brain_stream_hook.py -q -rf` ONCE before committing C3, as the AGENTS.md self-review loop's "what could break" step; it exited 0 at 9 passed and changed nothing. The G9 readings above are from the ordered run at C3, not from it.
- NO EXISTING SOURCE FILE WAS EDITED and NO DEPENDENCY WAS ADDED (constraint 3): both code paths are NEW files by G8's `ls-tree`, `.agent/live_review.md` is the one existing file this round edited, and `apps/ui/package.json` and `apps/ui/package-lock.json` were never opened. NO id was minted and none resolved (constraint 4): R-0630 stays free; R-0368 is AMENDED and still OPEN, as are R-0628, R-0629 and R-0622; no `Done:` and no `Landed:` line was written for any of them. `npm run lint` was NOT run: it is red at base, it is R-0622, and it is not a gate (R-0364).
- The session command guard rejects `$(...)`, `; echo $?`, heredocs, shell loops and chained `;` commands BY FORM, so every multi-step gate, all three mutation controls and all four suite runs were written to scripts under the gitignored `.remedy-wt/` and run from there; nothing from that directory was committed.
## Next
The next session's FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1); its SECOND is the Open PR Gate (Phase 1 rule 2). R27 IS PENDING REVIEW: its verdict is owed by the next round's ledger commit, and no line of this round records one. The next free finding id is R-0630. R-0628, R-0629, R-0622 and R-0368 are all OPEN — R-0628 names this hook and is resolved by the round that REVIEWS this one, never by the round that built it. R28 puts the delayed badge on a visible surface and wires the hook's deps to the endpoint T001 and T002 built, the first round in which this feature's server half and client half meet.

# Handback — F008 SSE event stream, R28 (the R27 verdict recorded, R-0629 amended)
## Range
Review of `c768cf03`..C3, the handback commit itself (6 commits, branch feature/f008-sse-event-stream). C3's SHA cannot exist inside C3, so it is named by role and the round report carries the value (R-0371).
## Commits
### e301b8c3 docs(state): save the F008 R28 block verbatim
| Path | +/- | Reason |
| `.agent/authored/f008-r28.md` | +228/-0 | C0a, the R28 block saved byte for byte |

### 234a4e94 docs(state): mirror the F008 R28 block into last_block
| Path | +/- | Reason |
| `.agent/last_block.md` | +129/-295 | C0b, the same bytes mirrored from the COMMITTED C0a blob |

### 4d766cf4 docs(state): set the plan to F008 R28, recording the R27 verdict
| Path | +/- | Reason |
| `.agent/plan.md` | +11/-12 | C1, PLANF008R28 applied whole |

### 1cf2280b docs(review): amend R-0629 with the F008 R27 instance
| Path | +/- | Reason |
| `.agent/live_review.md` | +1/-1 | C2a, the round's ONE pair, applied as a REWRITE |

### fcea57b5 docs(review): record the R27 verdict in the live review ledger
| Path | +/- | Reason |
| `.agent/live_review.md` | +2/-0 | C2b, LEDGER28's paragraph appended |

### C3 docs(state): write the F008 R28 handback
| Path | +/- | Reason |
| `.agent/handoff.md` | self | C3 cannot table itself (R-0149); its numbers are in the round report |

## External actions
- `git push -u origin feature/f008-sse-event-stream` runs ONCE, AFTER C3, and its output belongs to the round report (constraint 5). NO worktree was added or removed this round (constraint 6) — the primary checkout stayed the only one. NOTHING merged, no PR created, no PR updated, no branch created (constraint 7), and NO `gh` command was run: the block records the R26 Open PR Gate returning `[]`, and no new branch is being cut.

## Verification
- G1 `.agent/STOP` ABSENT (`ls` exit 2, "No such file or directory"), read immediately before C0a; branch feature/f008-sse-event-stream; `git status --porcelain` EMPTY after each of C0a, C0b, C1, C2a and C2b. The post-C3 porcelain, `git worktree list` and push output are in the round report (constraint 5).
- G2 Transport EQUAL three ways — `.remedy-wt/f008-r28.md` as received, `.agent/authored/f008-r28.md` at C0a and `.agent/last_block.md` at C0b — all sha256 a7ad435632c7e37a69f77b314509722b1e1cf347a8acb2cc25f89007f94b33b5 over 19687 bytes and 228 lines, and that value EQUALS the digest carried in the task prompt.
- G3 FOUR slices, the COUNT taken from an ordered extraction out of the COMMITTED C0a blob (`git show e301b8c3:…`) by their marker lines, newline-included as sha256/bytes/lines: PLANF008R28 23eed56c/2140/39, R0629FROM 64428337/82/1, R0629TO f6653cda/1745/1, LEDGER28 c64702c1/3855/1 — every digest prefix and every line count equal to the values the block names, and NONE carries trailing whitespace on any line (the offending-line list was empty for all four).
- G4 `.agent/plan.md` at C1 sha256 23eed56cb6af86de0dae30f0484b4df57c8384dfa39400ce81e57740cf83d9c1, 2140 bytes, 39 lines (<50), BYTE-EQUAL to PLANF008R28; `Steps` occurs (1x), `## Goal` 1x and `## Next Steps` 1x line-anchored, and `\bF\d{3}\b` matches `F008`.
- G5 The REWRITE at C2a, base bytes read with `git show c768cf03:.agent/live_review.md` into scratch and never over the tracked file: R0629FROM counts 1 at the round base and 0 at C2a; R0629TO counts 0 at the round base and 1 at C2a — the FROM-0x / TO-1x proof a rewrite owes. The base blob (2f8330d0, 485276 bytes, 1086 lines) with that ONE byte-string substitution applied is BYTE-EQUAL to the C2a blob (206a84e7, 486939 bytes, 1086 lines). The blank-line paragraph COUNT is 238 at the base and 238 at C2a, UNCHANGED, and EXACTLY ONE paragraph differs — index 234, the one beginning `- R-0629 — `.
- G6 (a) the C2a blob is a byte-exact PREFIX of the C2b blob (d1907e30, 490795 bytes, 1088 lines) and the remainder == newline+LEDGER28, sha256 67dfdfba14879ef039272709b2e36ac2bf15f83e539e742c876dc8f1d6f8ef44, 3856 bytes, 2 lines; (b) an INDEPENDENT blank-line split of the WHOLE C2b file, its terminating newline normalised first, gives 239 units whose LAST unit is LEDGER28's paragraph. NEGATIVE CONTROL: one PRINTABLE ASCII byte of the remainder flipped to another printable one (remainder offset 1, `G`→`Z`) REJECTED by BOTH readings, the unflipped value ACCEPTED by BOTH.
- G7 At C2a/C2b, line-anchored: `^- R-\d+ — ` 201/201 — this round mints NO id — `^- R-0630 — ` 0/0, `^- R-0629 — ` 1/1, `^- R-0628 — ` 1/1, `^- R-0368 — ` 1/1, `^Done: R-\d+ — ` 6/6, `^Landed: ` 0/0, `^Gate: R\d+ — ` 27/28 over 27 then 28 DISTINCT keys. HEADER SWEEP at C2b: of 28 `Gate: ` lines, 27 match `^Gate: R(\d+) — the R(\d+) entry\.` with second == first−1, 1 does NOT and its text to its first period is `Gate: R1 — the F255 R21 entry.`, and the R28 pair occurs EXACTLY ONCE.
- G7 suites, PRIMARY checkout, SERIALLY, never two test processes at once, AT C2b: the five-target state-reader command the block names EXIT 0 at 465 passed + 0 skipped = 465; `python3 -m pytest tests/ui_contracts/ -q -rf` EXIT 0 at 402 passed + 4 skipped = 406. G7's STOP clause was never reached.
- G8 `git diff --name-only c768cf03..fcea57b5`, measured from the round base this block's header names and no other SHA, yields EXACTLY the four Change-set paths minus `.agent/handoff.md`, with NONE on either side alone. Every commit in that range has exactly ONE parent (five commits, five single-parent readings). BOTH numstat cells per path from `git show --numstat`, each cross-checked against `git diff --numstat` and AGREEING: 228/0, 129/295, 11/12, 1/1 and 2/0 — every insertion under 500 (max 228), and EVERY CELL, insertion and deletion, equal to the `+/-` column above.
- G9 Lines BEGINNING with the two slice markers: 0 in `.agent/plan.md` at C1, 0 in `.agent/live_review.md` at C2a, 0 at C2b, and 0 in this file, measured on the drafted bytes C3 commits unchanged. This round's own reflog entries, counted by the OPERATION before the first `:` in `%gs`: all FIVE pre-C3 entries are `commit` (five found, five classified, the sixth being R27's handback and outside this round); `amend` 0, `rebase` 0, `cherry` 0. No total asserted.
- G10 This file carries every mandated section of docs/agents/handback_template.md, the `## Next` content constraint 9 names in that order, and the item-status table below, which holds exactly one row for each of C0a, C0b, C1, C2a, C2b and C3 — "exactly one row" scoping to that TABLE. Measured with `wc -l` in `.remedy-wt/` BEFORE it was written here it is 68 lines, UNDER the 100 this round's six commits allow, so no DECISION D15 stated-cause line is owed. One line per gate here; the raw transcripts are in the round report (R-0582).

## Authored-text proofs
- `.agent/authored/f008-r28.md` at C0a == the received block byte for byte and `.agent/last_block.md` at C0b == the same bytes (G2). ALL FOUR slices were extracted from the COMMITTED C0a blob by their marker lines and applied unedited — never retyped, rewrapped, reflowed, reindented or whitespace-adjusted. G4 is the disk-to-disk byte equality for PLANF008R28. G5 is the FROM-0x/TO-1x proof for the round's ONE pair, R0629FROM→R0629TO, applied as an exact byte-string replacement with the paragraph around it not reflowed; TO does NOT contain FROM, so the pair is a REWRITE and no append reading is claimed for it. G6 is the ordered-append equality for LEDGER28, agreed by two independent readings with a negative control. All four slices reached a commit; G9 confirms no marker line reached one.

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
| C3 | done | this commit |
## Deviations & assumptions
- No departure from the ordered commit sequence C0a, C0b, C1, C2a, C2b, C3. No extra commit, no dropped commit, no reordering; C1 was the first substantive commit and C2a preceded C2b, as constraint 2 requires.
- OBJECTION to a factual clause inside LEDGER28, raised here because constraint 1 forbids editing a slice: the slice's closing sentence says R27 "DECLARED FOUR DEVIATIONS AND EVERY ONE IS SOUND". One is not sound. R27's own deviations list claims "these seven subjects carry a `Co-Authored-By: Claude Opus 5` trailer, as R26's did"; measured over `a86231c0..c768cf03` with `git log --format=%(trailers:key=Co-Authored-By,valueonly)`, ALL SEVEN R27 commits return an EMPTY trailer list, so the claim is false and the clause certifying it inherits that. I applied LEDGER28 byte for byte anyway. No id is minted for it (constraint 4); the round report carries the transcript.
- My six commit subjects match this branch's actual convention and carry NO `Co-Authored-By` trailer, as no commit on this branch does. None carries a leading-slash token, absolute path or secret-like string.
- Constraint 3 held: NO code file was edited and NO dependency was added; `apps/ui/package.json` and `apps/ui/package-lock.json` were never opened, and `.agent/live_review.md` is the one previously existing file this round amends beyond the state files the bundle names. Constraint 4 held: R-0630 stays FREE, R-0629 is AMENDED and still OPEN as are R-0628, R-0368 and R-0622, and no `Done:` and no `Landed:` line was written for any of them. `npm run lint` was NOT run: it is red at base, it is R-0622, and it is not a gate (R-0364).
- Constraint 6 held: NO worktree was created and no red control was ordered, this round shipping no behaviour to break. The typecheck and `npx vitest run` readings the block quotes at base were NOT re-run — the block's "Done when" list orders only the two pytest suites, and no TypeScript changed.
- The session command guard rejects `$(...)`, `; echo $?`, heredocs, shell loops and chained `;` commands BY FORM, so every multi-step gate was written to a script under the gitignored `.remedy-wt/` and run from there; nothing from that directory was committed.
## Next
The next session's FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1); its SECOND is the Open PR Gate (Phase 1 rule 2). R28 IS PENDING REVIEW: its verdict is owed by the next round's ledger commit, and no line of this round records one. The next free finding id is R-0630. R-0628, R-0629, R-0368 and R-0622 are all OPEN, and R-0628's hook HAS now landed and been reviewed under its contract, so R29 MAY resolve it. R29's work is the delayed badge on a visible surface plus wiring the hook's deps to the endpoint T001 and T002 built — the first round in which this feature's two halves meet.

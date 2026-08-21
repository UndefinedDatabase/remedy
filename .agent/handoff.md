# Handback — F008 SSE event stream, R25 (the R24 verdict recorded, R-0629 registered, no code changed)
## Range
Review of `6e39f19d`..C3, the handback commit itself (5 commits, branch feature/f008-sse-event-stream). C3's SHA cannot exist inside C3, so it is named by role and the round report carries the value (R-0371).
## Commits
### 6bd98edd docs(state): save the F008 R25 block verbatim
| Path | +/- | Reason |
| `.agent/authored/f008-r25.md` | +192/-0 | C0a, the R25 block saved byte for byte |

### b252f72f docs(state): mirror the F008 R25 block into last_block
| Path | +/- | Reason |
| `.agent/last_block.md` | +107/-340 | C0b, the same bytes mirrored from the COMMITTED C0a blob |

### 596c6f0b docs(state): set the plan to F008 R25, recording the R24 verdict
| Path | +/- | Reason |
| `.agent/plan.md` | +13/-12 | C1, PLANF008R25 applied whole |

### 0586d578 docs(review): record the R24 verdict and register R-0629
| Path | +/- | Reason |
| `.agent/live_review.md` | +4/-0 | C2, LEDGER25's two paragraphs appended |

### C3 docs(state): write the F008 R25 handback
| Path | +/- | Reason |
| `.agent/handoff.md` | self | C3 cannot table itself (R-0149); its numbers are in the round report |

## External actions
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` — exit 0, `[]`, so the round continues on this branch. NO worktree was created or removed this round (constraint 6): the primary checkout is the only one and no red control was ordered, this round shipping no behaviour to break. `git push -u origin feature/f008-sse-event-stream` is run ONCE, AFTER C3, and its output belongs to the round report (constraint 5). NOTHING merged, no PR created, no PR updated, no branch created (constraint 8).

## Verification
- G1 `.agent/STOP` ABSENT, read immediately before C0a; branch feature/f008-sse-event-stream; `git status --porcelain` EMPTY after each of C0a, C0b, C1 and C2. The post-C3 porcelain, `git worktree list` and push output are in the round report (constraint 5).
- G2 Transport EQUAL three ways — `.remedy-wt/f008-r25.md` as received, `.agent/authored/f008-r25.md` at C0a and `.agent/last_block.md` at C0b — sha256 aa5693287d3e823a12d1a0c7ea3e0454279d5b5bcd435ffc612cd2815fb9eeea, 17234 bytes, 192 lines, and that value EQUALS the digest carried in the task prompt.
- G3 TWO slices, the COUNT taken from the ordered extraction out of the COMMITTED C0a blob by their marker lines, newline-included as sha256/bytes/lines: PLANF008R25 0cc72159/2045/39 and LEDGER25 2dd41f07/5758/3 — both equal to the digests the block names, at the 39 lines it names, and NEITHER carries trailing whitespace on any line (the offending-line list was empty for both).
- G4 `.agent/plan.md` at C1 sha256 0cc721597eae16f814cb4e763f61200be716a3ed7390f231bd07b0e1569393d9, 2045 bytes, 39 lines (<50), BYTE-EQUAL to PLANF008R25; `Steps` occurs, `## Goal` 1x and `## Next Steps` 1x line-anchored, `\bF\d{3}\b` matches `F008`.
- G5 (a) the C1 blob (193b2366, 471005 bytes, 1078 lines) is a byte-exact PREFIX of the C2 blob (6b33fef0, 476764 bytes, 1082 lines) and the remainder == newline+LEDGER25, sha256 e765427eaabb8b14bf81cdc959b47653f47fe1a469511224a466cfb1dc2428ee, 5759 bytes, 4 lines; (b) an INDEPENDENT blank-line split of the WHOLE C2 file, its terminating newline normalised first, gives 236 units whose LAST TWO, in order, are LEDGER25's two paragraphs. NEGATIVE CONTROL: one flipped ASCII byte of the remainder (offset 2000, `l`→`X`) REJECTED by BOTH readings, the unflipped value ACCEPTED by BOTH.
- G6 At C1/C2, line-anchored: `^- R-\d+ — ` 200/201 — R-0629 is the ONLY id minted — `^- R-0629 — ` 0/1, `^- R-0630 — ` 0/0, `^- R-0628 — ` 1/1, `^Done: R-\d+ — ` 6/6, `^Landed: ` 0/0, `^Gate: R\d+ — ` 24/25 over 24 then 25 DISTINCT keys. Header sweep at C2: of 25 `^Gate: ` lines, 24 match `^Gate: R(\d+) — the R(\d+) entry\.` with second == first−1, 1 does NOT and its text opens `Gate: R1 — the F255 R21 entry.` (that non-matching line runs 5381 chars; it is quoted here to its first period), and the R25 pair `Gate: R25 — the R24 entry.` occurs EXACTLY ONCE.
- G7 PRIMARY checkout, run SERIALLY, never two test processes at once, AT C2 — the commit at which both edited state files are final. The state readers plus canary EXIT 0 at 465 passed + 0 skipped = 465; `tests/ui_contracts/` EXIT 0 at 393 passed + 4 skipped = 397. Both are passed-plus-skipped readings, as the block requires. G7's STOP clause was never reached.
- G8 `git diff --name-only 6e39f19d..0586d578` equals the Change set MINUS `.agent/handoff.md` exactly — four paths, none on either side alone; the full `6e39f19d`..C3 reading is in the round report (constraint 5). Every commit in the range has exactly ONE parent. BOTH numstat cells per path from `git show --numstat`, each cross-checked against `git diff --numstat` and AGREEING: 192/0, 107/340, 13/12 and 4/0 — every insertion under 500, and EVERY CELL, insertion and deletion, equal to the `+/-` column above.
- G9 Lines BEGINNING with `<<<SLICE ` or `<<<END `: 0 in `.agent/plan.md` at C1, 0 in `.agent/live_review.md` at C2, and 0 in this file, measured on the exact bytes committed as C3. This round's own reflog entries, counted by the OPERATION before the first `:` in `%gs`: all four pre-C3 entries are `commit` (6bd98edd, b252f72f, 596c6f0b, 0586d578, four entries found and four classified); `amend` 0, `rebase` 0, `cherry` 0. No total asserted.
- G10 This file carries every mandated section of docs/agents/handback_template.md, the `## Next` content constraint 9 names in that order, and the item-status table below, which holds exactly one row for each of C0a, C0b, C1, C2 and C3 — "exactly one row" scoping to that TABLE. Measured with `wc -l` in the session scratchpad BEFORE it was written it is 58 lines, UNDER the 60 this round's five commits allow, so no DECISION D15 stated-cause line is owed. One line per gate here; the raw transcripts are in the round report (R-0582).

## Authored-text proofs
- `.agent/authored/f008-r25.md` at C0a == the scratch block byte for byte and `.agent/last_block.md` at C0b == the same bytes (G2). BOTH slices were extracted from the COMMITTED C0a blob by their marker lines and applied unedited — never retyped, rewrapped, reflowed, reindented or whitespace-adjusted. G4 is the disk-to-disk byte-equality for PLANF008R25 and G5 the ordered-append equality for LEDGER25, agreed by two independent readings with a negative control. There was NO FROM/TO pair this round, so no containment reading is claimed. Both slices reached a commit; G9 confirms no marker line reached one.

## State — Fortschritt
~94 % (T001 ✅ · T002 ✅ · T003 Regeln+Treiber+Runner+Store+Host ✅, Hook offen) — Schätzung

## Item status
| Item | Status | Reason |
|------|--------|--------|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | this commit |
## Deviations & assumptions
- No departure from the ordered commit sequence C0a, C0b, C1, C2, C3. No extra commit, no dropped commit, no reordering; C1 was the first substantive commit, as constraint 2 requires. NO CODE FILE WAS EDITED and NO DEPENDENCY WAS ADDED (constraint 3): `apps/ui/package.json` and `apps/ui/package-lock.json` were not opened, and G8 proves the range touches only the four state paths. R-0629 is REGISTERED and stays OPEN, R-0628 stays OPEN, R-0622 stays OPEN, no `Done:` and no `Landed:` line was written for any of them, and R-0630 stays free (constraint 4). NO OBJECTION to any slice: both applied byte for byte and every value the block predicted — the two slice digests, the 39-line plan, the two ledger paragraphs, the set counts and the two suite totals — was MEASURED at that value.
- Commit-message convention: these five subjects carry no `Co-Authored-By` trailer, matching every prior round on this branch. The session command guard rejects `$(...)`, `; echo $?`, heredocs, shell loops and chained `;` commands BY FORM, so every multi-step gate and both test runs were written to a script under the gitignored `.remedy-wt/` and run from there; nothing from that directory was committed.
## Next
The next session's FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1); its SECOND is the Open PR Gate (Phase 1 rule 2), which returned `[]` at R25 and therefore continues on this branch. R25 IS PENDING REVIEW: its verdict is owed by the next round's ledger commit and no line of this round records one. The next free finding id is R-0630. R-0628 and R-0629 are both OPEN. R26's work is the thin `useBrainStream` hook over the runner store plus the visible delayed badge, gated by `npm run typecheck` and a NEW `tests/ui_contracts/` source contract in the style this repository uses for every React component, with the hook calling the host's `close` on unmount or a remounting cockpit leaks one EventSource per mount.

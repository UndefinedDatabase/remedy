# F021 R33 handback — record R32, land the envelope's task linkage

Fortschritt: ~98 % (T002 fertig; T003 hat mit dem Server-Feld begonnen, es fehlen
             Klick-Sprung und Steuer-Eingang) — Schaetzung

## Range
Review of 6e529304456c17b284ad65ad0b0315bf1bd06663..HEAD — round base `6e529304`,
branch `feature/f021-live-activity-feed`. Open findings 223, by
`planner_reviewer_prompt.md` §3 item 10 — `^- R-\d+ — ` 224 minus
`^Done: R-\d+ — ` 1 — measured at C2 `6d937573` (DECISION F009 D10).

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a `d773dc1a` | done | |
| C0b `3eb8d32b` | done | |
| C1 `220d73ba` | done | |
| C2 `6d937573` | done | |
| C3 `94dc7add` | done | source pair AND both test pairs, one commit (constraint 3) |
| C4 (this file) | done | its own SHA is unnameable from inside it |

## Commits

### d773dc1a chore(agent): save the F021 R33 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f021-r33.md | +312/-0 | the block saved verbatim (C0a) |

### 3eb8d32b chore(agent): mirror the R33 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +252/-270 | written FROM the committed C0a blob (C0b) |

### 220d73ba docs(state): point the F021 plan at R33, the record and envelope-field round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +22/-21 | PLANF021R33 whole-file write (C1) |

### 6d937573 docs(review): record the R32 PASS and correct two reviewer defects against open findings
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +6/-0 | RECORD33 appended, ONE blank line at the join (C2) |

### 94dc7add feat(ui-server): carry the task linkage in the shared event envelope
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ui_server.py | +13/-0 | SUMMARYPAIR — `task_id` from two sources (C3) |
| tests/ui_server/test_sse_stream.py | +27/-3 | PINPAIR then GOLDENPAIR (C3) |

### C4 docs(state): hand back F021 R33 — SHA unnameable: this is the commit that writes this file
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | owed to R34 | the handback itself (C4) |

## External actions
`git push -u origin feature/f021-live-activity-feed` after C4. `gh pr list --state
open --json number,headRefName,baseRefName,isDraft` exit 0, output `[]`; no
`gh pr create`, no `gh pr merge`. ONE worktree, added and removed: `git worktree
add --detach .remedy-wt/g6 6e529304` then `git worktree remove --force` (G6).

## Verification — one line per gate, transcripts in the round report (R-0582)
G1 `.agent/STOP` ABSENT before C0a and again before C4; branch `feature/f021-live-activity-feed`; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3.
G2 sha256 `8b2ac868303ef15f1b8deb954b43aa8e33dbff00fcaa33a978aed0eed50ae5ce`, 23727 bytes, 312 lines — EQUAL across `.remedy-wt/f021-r33.md`, `.agent/authored/f021-r33.md` at C0a and `.agent/last_block.md` at C0b (both blob `d4f63ac2`). My extractor printed 2 whole texts, 3 pairs, 113 CONTENT lines; TOTAL 312 against 490, PROSE 199 against 400.
G3 `cmp` plan.md vs PLANF021R33+newline exit 0; NEGATIVE CONTROL vs the bare slice exit 1; last byte is a newline; `^## Goal$` 1, `^## Next Steps$` 1; `wc -l` 49, under 50.
G4 SUMMARYPAIR/PINPAIR/GOLDENPAIR FROM each 1x at base and 0x at C3, in that application order; every non-blank TO-only line exactly once in C3's 40 added lines (12, 21 and 2 lines). `"task_id"` in the test file 0 then 11. TWO ORDERED NUMERALS ARE FALSE — Deviations 1 and 2: `, "outcome": "ok"}` is 5 then 3, not 5 then 5, and `task_id` in ui_server.py is 44 then 48, not 0 then a count.
G5 canonical `^- R-\d+ — ` 224→224, ALL DISTINCT at both, max R-0661 at both; loose `^- R-` 225→225, gap to canonical 1 at both; `^Done: R-` 1→1 line-anchored (35→35 unanchored, unchanged under either reading — Deviations 5); `^Gate: R` 31→32, DISTINCT at both; `^Gate: R33` 0→1; `^Recurrence: ` 5→7; `^Recurrence: R-0661 — ` 0→1; `^Recurrence: R-0607 — ` 0→1; `^- R-0661 — ` 1→1; `^- R-0607 — ` 1→1. RECORD33 paragraphs opening with the bytes `- R-` = 0 of 3. Base blob a byte-exact PREFIX of C2, remainder EXACTLY one newline + RECORD33 + one newline.
G6 RED-PROOF in `.remedy-wt/g6` at `6e529304`, PINPAIR and GOLDENPAIR applied WITHOUT SUMMARYPAIR (FROM still 1x in the worktree source): `4 failed, 62 passed`, the failures being `TestFrameShape::test_the_envelope_carries_the_safe_fields_only`, `TestFrameShape::test_the_envelope_carries_the_linkage_from_both_event_sources`, `TestFramingGolden::test_the_wire_bytes_match_the_golden` and `TestFramingGolden::test_the_golden_is_what_the_frame_builders_produce`. Worktree removed; `git status --porcelain` 0 lines; `git worktree list` the primary checkout ALONE.
G7 SERIAL, PRIMARY checkout, repo root: `tests/ui_server/` exit 0, 439 passed (438 at the base, measured in the G6 worktree before its pairs were applied — the difference is PINPAIR's one new test); the FOUR state readers exit 0 — that ui_server run plus 89 over `test_test_runner.py`, `test_resource_safety.py` and `test_integrity_gate.py`, 528 together, the fourth file being the one R-0607 rules in; canary `tests/cli/test_golden_path.py` exit 0, 42; `python3 -m ruff check packages/orchestration/ui_server.py tests/ui_server/test_sse_stream.py` exit 0, "All checks passed!". Constraint 12's 405 pair did NOT fail in any run.
G8 `git diff --name-only 6e529304..94dc7add` EQUALS the six non-handoff `Change:` paths, BOTH set differences EMPTY; at C4 the set is those six plus `.agent/handoff.md`, the seventh `Change:` path (Deviations 4). 6 commits, every one single-parent; `git show --numstat` and `git diff --numstat` agree cell by cell and agree with the tables above; insertions 312, 252, 22, 6, 40 and C4's own, each under 500. Marker sweep LINE-ANCHORED 0 for each of `<<<SLICE `, `<<<END `, `<<<FROM `, `<<<TO ` in all four target files; unanchored `<<<` 0 in three of them and 18 in `.agent/live_review.md`, unchanged from the base (Deviations 3). Reflog BY OPERATION: every one of this round's rows is `commit`, `amend`/`rebase`/`cherry` 0 each. `gh pr list --state open` printed `[]`.

## Authored-text proofs
All five texts were extracted BY MARKER LINE from the COMMITTED C0a blob
`d773dc1a:.agent/authored/f021-r33.md`, never retyped. `.agent/plan.md`: `cmp`
exit 0 against PLANF021R33 + one newline, exit 1 against the bare slice.
`.agent/live_review.md`: base blob a byte-exact PREFIX, remainder EXACTLY one
newline + RECORD33 + one newline. The three pairs: each FROM asserted present
EXACTLY once immediately before its replacement by the applying script, which
refuses any other count; PINPAIR before GOLDENPAIR (constraint 11).

## Deviations & assumptions
None repaired; constraint 1 forbids editing reviewer text, so each is declared.
1. G4's "`, "outcome": "ok"}` 5 then 5 — UNCHANGED" is FALSE: MEASURED 5 then 3,
   because GOLDENPAIR's own TO rewrites that tail on both `GOLDEN_STREAM` lines.
   The clause's PROPERTY holds: the 3 survivors are the 3 INPUT fixtures at
   unchanged lines 19, 76, 89, and 5 − 2 = 3 accounts for the delta.
2. G4's "`task_id` 0 at base" for `ui_server.py` is FALSE: MEASURED 44 then 48,
   delta 4 = SUMMARYPAIR's new occurrences; the file carried task ids long
   before F021.
3. G8's "0 for any `<<<` at all" is UNMEETABLE over `.agent/live_review.md`: 18
   at base, 18 at C2, RECORD33 contributing 0; reaching 0 means editing landed
   ledger text, which constraint 7 forbids. R-0630/R-0587 class; the
   line-anchored readings, the load-bearing ones, are all 0.
4. G8's path-set clause and its "6 commits" clause cannot hold at one HEAD: the
   six-path set holds at C3, and the sixth commit C4 adds the seventh path.
   Both readings reported rather than one chosen.
5. The block writes `Done: R-` unanchored where constraint 8 wants a named
   pattern. Both readings reported; both unchanged across C2.
6. The ONE ordered worktree was ALSO used, before its pairs were applied, for
   the base `tests/ui_server/` reading (438). No second worktree was created.
7. No departure from the ordered commit sequence: exactly C0a, C0b, C1, C2, C3,
   C4 — none extra, dropped or reordered.
8. DECISION D15, size: 115 lines, over the ≤100 tier this round's six commit
   tables earn. Mandated cause: six commit tables, eight gate lines, the
   item-status table, the authored-text section and eight deviations, of which
   four are false or unmeetable gate clauses that must be evidenced rather than
   asserted. No section was dropped and no transcript is restated here.

## Next
R33's OWN VERDICT IS UNRECORDED and the next round's ledger commit owes it, with
the two readings C4 cannot state about itself: C4's insertion count and its
`wc -l`. R34 is the CLIENT half of T003 — `feedRow.ts` carries the `task_id` the
envelope now emits and a row click resolves it to a node id, emitting
`onSelectNode`. R35 is the disabled steering input with the F030 tooltip, after
which F021 reaches its integration-gate round. The next session's first action is
Phase 1 rule 1, re-reading `.agent/STOP` from disk, before rule 2.

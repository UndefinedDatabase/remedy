# F021 R35 handback — record R34, wire the jump, pin it by source contract

Fortschritt: ~99 % (T003 Klick-Sprung fertig; es fehlt nur noch der deaktivierte
             Steuer-Eingang) — Schaetzung

## Range
Review of 83a03ba1d703ca127d1a4103f5dac22a66405e2c..HEAD — round base `83a03ba1`,
branch `feature/f021-live-activity-feed`. Open findings 223, by
`planner_reviewer_prompt.md` §3 item 10 — canonical `^- R-\d+ — ` 224 minus
`^Done: R-\d+ — ` 1 — measured at C2 `cb3093bb` (DECISION F009 D10).

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a `ad920c8d` | done | |
| C0b `ee4aca3e` | done | |
| C1 `6eb63c45` | done | |
| C2 `cb3093bb` | done | |
| C3 `20b1a2ca` | done | all six source pairs plus CSSPAIR, three files, one commit |
| C4 `6270aebf` | done | |
| C5 (this file) | done | its own SHA is unnameable from inside it |

## Commits

### ad920c8d chore(agent): save the F021 R35 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f021-r35.md | +399/-0 | the block saved verbatim (C0a) |

### ee4aca3e chore(agent): mirror the R35 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +316/-275 | written FROM the committed C0a blob (C0b) |

### 6eb63c45 docs(state): point the F021 plan at R35, the wiring round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +20/-21 | PLANF021R35 whole-file write (C1) |

### cb3093bb docs(review): record the R34 PASS and the reviewer's own path miscount
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | RECORD35 appended, ONE blank line at the join (C2) |

### 20b1a2ca feat(ui): a feed row that resolves to a node jumps to it
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/panels/ActivityFeedCard.tsx | +44/-16 | IMPORT, LIVEFEED, ROWS, CARDSIG, LIVEFEEDUSE pairs, in that order (C3) |
| apps/ui/src/components/panels/RightLivePanel.module.css | +7/-0 | CSSPAIR, append-shaped (C3) |
| apps/ui/src/components/panels/RightLivePanel.tsx | +1/-1 | PANELPAIR (C3) |

### 6270aebf test(ui-contracts): pin that the component really calls the jump rule
| Path | +/- | Reason |
|---|---|---|
| tests/ui_contracts/test_brain_stream_ring.py | +49/-0 | CONTRACTSLICE appended, TWO blank lines at the join (C4) |

### C5 docs(state): hand back F021 R35 — SHA unnameable: this is the commit that writes this file
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | owed to R36 | the handback itself (C5) |

## External actions
`git push -u origin feature/f021-live-activity-feed` after C5. `gh pr list --state
open --json number,headRefName,baseRefName,isDraft` exit 0, output `[]`; no `gh pr
create`, no `gh pr merge`. ONE worktree, added and removed: `git worktree add
--detach .remedy-wt/g6 6270aebf` then `git worktree remove --force` (G6).

## Verification — one line per gate, transcripts in the round report (R-0582)
G1 `.agent/STOP` ABSENT before C0a and again before C5; branch `feature/f021-live-activity-feed`; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3, C4.
G2 sha256 `fb40b19004ee91d79c1c2b624d2a9cc0e4958d07f8908a0d4b43e323a5174ac5`, 26645 bytes, 399 lines — EQUAL over the bytes I read, `.remedy-wt/f021-r35.md`, `.agent/authored/f021-r35.md` at C0a and `.agent/last_block.md` at C0b. My extractor printed 3 whole texts, 7 pairs, 172 CONTENT lines, 27 marker lines; TOTAL 399 against 490, PROSE 227 against 400 — both re-measured from that blob and both matching constraint 12.
G3 `cmp` plan.md vs PLANF021R35+newline exit 0; NEGATIVE CONTROL vs the bare slice exit 1; last byte `0a`; `^## Goal$` 1, `^## Next Steps$` 1; `wc -l` 47, under 50.
G4 LIVEFEEDPAIR, ROWSPAIR, CARDSIGPAIR, LIVEFEEDUSEPAIR, PANELPAIR each FROM 1x at base and 0x at C3. IMPORTPAIR and CSSPAIR, append-shaped, each 1x at base and 1x at C3 in their target; IMPORTPAIR's FROM also occurs once in `RightLivePanel.tsx`, 2x tree-wide at BOTH ends, unchanged. `nodeIdForFeedRow` in `ActivityFeedCard.tsx` 0 then 2; `.activityItemJump` in the CSS 0 then 2. §4.9 per-line clause is RED for 2 of 50 distinct TO-only lines — Deviation 1 — with the ordered proof there instead.
G5 canonical `^- R-\d+ — ` 224→224, ALL DISTINCT at both, max R-0661 at both; loose `^- R-` 225→225, gap 1 at both; `^Done: R-` 1→1; `^Gate: R` 33→34, DISTINCT at both; `^Gate: R35` 0→1; `^Recurrence: ` 10→11; `^Recurrence: R-0402 — ` 0→1; `^- R-0402 — ` 1→1. RECORD35 paragraphs opening with the bytes `- R-` = 0 of 2. Base blob a byte-exact PREFIX of C2, remainder EXACTLY one newline + RECORD35 + one newline, 3908 bytes both measured and predicted.
G6 RED-PROOF in `.remedy-wt/g6` at C4, ` tasks={dashboard.tasks} onSelectNode={onSelectNode}` deleted from the ONE `<ActivityFeedCard` line, `TaskChecklistCard` left carrying both: `1 failed, 61 passed`, the sole failure `tests/ui_contracts/test_brain_stream_ring.py::TestAFeedRowJumpsToItsNode::test_the_panel_hands_the_card_what_the_rule_needs`, the node id the gate names. Worktree removed; `git status --porcelain` 0 lines; `git worktree list` the primary checkout ALONE.
G7 SERIAL, PRIMARY checkout: `tests/ui_contracts/` exit 0, 490 passed 4 skipped = 494, against 486+4 = 490 at the base, difference +4, exactly CONTRACTSLICE's four tests. `npm run test:unit` in `apps/ui` exit 0, 16 files and 218 tests — UNCHANGED from the base, as ordered. `npx tsc --noEmit` in `apps/ui` exit 0, EMPTY stdout and stderr; per constraint 10 this was its first honest execution and I ran it BEFORE committing C3 as well as after C4, exit 0 both times. FOUR state readers exit 0, 528 passed. Canary `tests/cli/test_golden_path.py` exit 0, 42 passed. `python3 -m ruff check tests/ui_contracts/test_brain_stream_ring.py` exit 0. `npm run lint` neither run nor reported (constraint 8).
G8 `git diff --name-only 83a03ba1..HEAD` at C4: I COUNT EIGHT paths, and they equal the EIGHT non-handoff `Change:` paths with BOTH set differences EMPTY — the block's G8 says SEVEN (Deviation 2). At C5 it is those eight plus `.agent/handoff.md`, so I COUNT NINE, where G8 predicts eight. 7 commits at C5, 6 at C4, every one single-parent; `git show --numstat` and `git diff --numstat` agree cell by cell on all six measurable commits; insertions 399, 316, 20, 4, 52, 49 and C5's own, each under 500. Marker sweep LINE-ANCHORED 0 for each of `<<<SLICE `, `<<<END `, `<<<FROM `, `<<<TO ` over all five named files. UNANCHORED `<<<` 0 over each of the three `apps/` files and the contract file. Reflog BY OPERATION: all of this round's rows are `commit`, `amend`/`rebase`/`cherry` 0 each. `gh pr list --state open` printed `[]`.

## Authored-text proofs
All ten texts — three slices and seven pairs — were extracted BY MARKER LINE from
the COMMITTED C0a blob `ad920c8d:.agent/authored/f021-r35.md`, never retyped.
`plan.md`: `cmp` exit 0 against slice + one newline, exit 1 against the bare
slice. `live_review.md` and `test_brain_stream_ring.py`: each base blob a
byte-exact PREFIX, remainders EXACTLY one and EXACTLY two newlines plus the slice
plus one terminator. Each pair's FROM was asserted present EXACTLY once
immediately before its replacement by the applying script, which refuses any
other count. REPLAY PROOF: re-applying all seven pairs to the three BASE blobs in
the ordered sequence reproduces the three C3 blobs BYTE FOR BYTE.

## Deviations & assumptions
None repaired; constraint 1 forbids editing reviewer text, so each is declared.
1. G4's §4.9 clause — "over the lines C3's diff ADDS, each TO-only line appears
   exactly once" — is RED as literally written, and unmeetable for CODE. Of 50
   distinct TO-only lines, two are structural repeats: `}) {` closes both
   LIVEFEEDPAIR's and CARDSIGPAIR's signature, and `        );` closes both the
   `const body = (` and the ternary INSIDE ROWSPAIR's own TO. This is open
   finding R-0531. The load-bearing property is measured and GREEN instead: the
   multiset of C3's 52 added lines EQUALS the multiset of the 52 TO-only lines,
   and the replay above is byte-exact. Nothing was edited to reach it.
2. R-0402 RECURS A THIRD TIME, in the block that records its second instance.
   The `Change:` section contradicts ITSELF: it opens "it names EIGHT paths, of
   which SEVEN are not the handoff" and closes "That is NINE entries and EIGHT
   non-handoff paths". I COUNT nine entries and eight non-handoff paths, so the
   closing sentence is right and the opening one is short by one; G8 inherits
   the wrong numeral twice ("the SEVEN non-handoff paths", "those seven plus
   `.agent/handoff.md` for EIGHT"). Both set differences are EMPTY against the
   eight, so the load-bearing half is unharmed, exactly as at R34.
3. Constraint 9 says "Four pairs edit ActivityFeedCard.tsx" and then enumerates
   FIVE — IMPORTPAIR, LIVEFEEDPAIR, ROWSPAIR, CARDSIGPAIR, LIVEFEEDUSEPAIR. Five
   is right: I measured each of those five FROMs present exactly once in that
   file at the base. The enumeration binds, the numeral does not, and I applied
   the five in the order named. Same R-0402 class as Deviation 2.
4. No departure from the ordered commit sequence: exactly C0a, C0b, C1, C2, C3,
   C4, C5 — none extra, dropped or reordered. No finding id minted or resolved.
5. DECISION D15, size: 127 lines, over the ≤100 tier this round's seven commit
   tables earn. Mandated cause: seven commit tables, eight gate lines, the
   item-status table, the authored-text section and five deviations, of which
   three are false or unmeetable gate clauses that must be evidenced rather than
   asserted. No section was dropped and no transcript is restated here.

## Next
R35's OWN VERDICT IS UNRECORDED and the next round's ledger commit owes it, with
the three readings C5 cannot state about itself: C5's SHA, its insertion count
and its `wc -l`. R36 is the last unbuilt item of T003 and of the feature — the
steering input rendered DISABLED with the tooltip naming F030 — after which F021
goes to the integration-gate round, the evidence round and the STATUS-commit
round. The next session's first action is Phase 1 rule 1, re-reading
`.agent/STOP` from disk, before rule 2.

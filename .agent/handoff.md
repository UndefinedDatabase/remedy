# F021 R34 handback — record R33, land the row's task linkage and its resolver

Fortschritt: ~98 % (T003 zur Haelfte: Server-Feld und Aufloeser stehen, es fehlen
             die Verdrahtung und der Steuer-Eingang) — Schaetzung

## Range
Review of a14f02947d262a1b38a3b7e87f6735efc6cbcd9c..HEAD — round base `a14f0294`,
branch `feature/f021-live-activity-feed`. Open findings 223, by
`planner_reviewer_prompt.md` §3 item 10 — `^- R-\d+ — ` 224 minus
`^Done: R-\d+ — ` 1 — measured at C2 `55353f79` (DECISION F009 D10).

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a `6c5151bf` | done | |
| C0b `093e84a2` | done | |
| C1 `8e9a396d` | done | |
| C2 `55353f79` | done | |
| C3 `8b68dcaf` | done | both source pairs, the test pair and both new files, one commit (constraint 3) |
| C4 (this file) | done | its own SHA is unnameable from inside it |

## Commits

### 6c5151bf chore(agent): save the F021 R34 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f021-r34.md | +358/-0 | the block saved verbatim (C0a) |

### 093e84a2 chore(agent): mirror the R34 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +268/-222 | written FROM the committed C0a blob `cdc59f80` (C0b) |

### 8e9a396d docs(state): point the F021 plan at R34, the record and resolver round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +23/-24 | PLANF021R34 whole-file write (C1) |

### 55353f79 docs(review): record the R33 PASS and three reviewer defects against open findings
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +8/-0 | RECORD34 appended, ONE blank line at the join (C2) |

### 8b68dcaf feat(ui): resolve a feed row to the graph node its task owns
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/feedRow.ts | +5/-0 | ROWFIELD then ROWPROJECT (C3) |
| apps/ui/src/api/feedFocus.ts | +36/-0 | FEEDFOCUS, new module, no caller yet (C3) |
| apps/ui/src/api/feedFocus.test.ts | +42/-0 | FEEDFOCUSTEST, 6 tests (C3) |
| apps/ui/src/api/actionClass.test.ts | +1/-1 | ACTIONROW, the typechecking repair (C3) |

### C4 docs(state): hand back F021 R34 — SHA unnameable: this is the commit that writes this file
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | owed to R35 | the handback itself (C4) |

## External actions
`git push -u origin feature/f021-live-activity-feed` after C4. `gh pr list --state
open --json number,headRefName,baseRefName,isDraft` exit 0, output `[]`; no `gh pr
create`, no `gh pr merge`. ONE worktree, added and removed: `git worktree add
--detach .remedy-wt/g6 8b68dcaf` then `git worktree remove --force` (G6).

## Verification — one line per gate, transcripts in the round report (R-0582)
G1 `.agent/STOP` ABSENT before C0a and again before C4; branch `feature/f021-live-activity-feed`; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3.
G2 sha256 `d75dbec5f6eb8c3d5e564af5f6a1c9fcf272edb272d1d41bbde9ca5701da8e04`, 25519 bytes, 358 lines — EQUAL over the bytes I read, `.remedy-wt/f021-r34.md`, `.agent/authored/f021-r34.md` at C0a and `.agent/last_block.md` at C0b (both blob `cdc59f80`). My extractor printed 4 whole texts, 3 pairs, 152 CONTENT lines, 17 marker lines; TOTAL 358 against 490, PROSE 206 against 400 — both re-measured from that blob and both matching constraint 12.
G3 `cmp` plan.md vs PLANF021R34+newline exit 0; NEGATIVE CONTROL vs the bare slice exit 1; last byte `0a`; `^## Goal$` 1, `^## Next Steps$` 1; `wc -l` 48, under 50.
G4 ROWFIELD/ROWPROJECT/ACTIONROW FROM each 1x at base and 0x at C3, applied in that order; `TO contains FROM` False for all three. Neither new path existed at base (`git cat-file -e` exit 128 for both); `cmp` vs slice+newline exit 0 and vs bare slice exit 1 for both; `wc -l` 36 and 42. Over C3's 84 added lines every non-blank TO-only line appears exactly once (4+1+1 lines). `taskId` reported as a DELTA only, never as a gate: 0→2 in feedRow.ts, 0→1 in actionClass.test.ts.
G5 canonical `^- R-\d+ — ` 224→224, ALL DISTINCT at both, max R-0661 at both; loose `^- R-` 225→225, gap 1 at both; `^Done: R-` 1→1 line-anchored (34→34 unanchored — Deviation 4); `^Gate: R` 32→33, labels DISTINCT at both; `^Gate: R34` 0→1; `^Recurrence: ` 7→10; `^Recurrence: R-0369 — ` 0→1; `^Recurrence: R-0419 — ` 0→1; `^Recurrence: R-0630 — ` 1→2 as ordered; `^- R-0369 — `, `^- R-0419 — `, `^- R-0630 — ` 1→1 each. RECORD34 paragraphs opening with the bytes `- R-` = 0 of 4. Base blob a byte-exact PREFIX of C2, remainder EXACTLY one newline + RECORD34 + one newline, 5781 bytes both measured and predicted.
G6 RED-PROOF in `.remedy-wt/g6` at C3, `owner.nodeId`→`owner.id` in `feedFocus.ts` (1 occurrence before, 0 after): `2 failed | 4 passed`, the failures being `nodeIdForFeedRow > resolves a row to the node of the task that owns it` and `nodeIdForFeedRow > reads the task's nodeId and never assumes it equals the task id` — the second is the test the gate names. Worktree removed; `git status --porcelain` 0 lines; `git worktree list` the primary checkout ALONE.
G7 SERIAL, PRIMARY checkout: `npm run test:unit` in `apps/ui` exit 0, 16 files and 218 tests, against 15 and 212 which I measured MYSELF in the same checkout at C2 before C3 — difference one file and six tests, exactly FEEDFOCUSTEST. `npx tsc --noEmit` in `apps/ui` exit 0 with EMPTY stdout and stderr, and exit 0 with empty output at C2 too, so the green is the change's and not a pre-existing pass being reported. FOUR state readers exit 0, 528 passed. `tests/ui_contracts/` exit 0, 486 passed 4 skipped. Canary `tests/cli/test_golden_path.py` exit 0, 42 passed. No ruff gate ordered; `npm run lint` neither run nor reported (constraint 9).
G8 `git diff --name-only a14f0294..HEAD` at C3 EQUALS the non-handoff `Change:` paths, BOTH set differences EMPTY — but that set has EIGHT members, not the seven G8 names (Deviation 1); at C4 it is those eight plus `.agent/handoff.md` (Deviation 2). 6 commits, every one single-parent; `git show --numstat` and `git diff --numstat` agree cell by cell on all five measurable commits; insertions 358, 268, 23, 8, 84 and C4's own, each under 500 (Deviation 3). Marker sweep LINE-ANCHORED 0 for each of `<<<SLICE `, `<<<END `, `<<<FROM `, `<<<TO ` over all five named files; UNANCHORED `<<<` 0 over each of the three `apps/` files. Reflog BY OPERATION: all five of this round's rows are `commit`, `amend`/`rebase`/`cherry` 0 each. `gh pr list --state open` printed `[]`.

## Authored-text proofs
All seven texts — four slices, three pairs — were extracted BY MARKER LINE from
the COMMITTED C0a blob `6c5151bf:.agent/authored/f021-r34.md`, never retyped.
`plan.md`, `feedFocus.ts`, `feedFocus.test.ts`: `cmp` exit 0 against slice + one
newline, exit 1 against the bare slice. `live_review.md`: base blob a byte-exact
PREFIX, remainder EXACTLY one newline + RECORD34 + one newline. Each pair's FROM
was asserted present EXACTLY once immediately before its replacement by the
applying script, which refuses any other count; ROWFIELD before ROWPROJECT.

## Deviations & assumptions
None repaired; constraint 1 forbids editing reviewer text, so each is declared.
1. G8's "the seven non-handoff `Change:` paths" is FALSE: the `Change:` list
   enumerates EIGHT of them, nine with `.agent/handoff.md`. The load-bearing
   property holds — both set differences over those eight are EMPTY at C3.
2. G8's path-set clause and its "6 commits" clause cannot hold at one HEAD: the
   eight-path set holds at C3, where the range has 5 commits; the sixth commit
   C4 adds the ninth path. Both readings reported rather than one chosen.
3. C0b's insertions are 268 under `git show --numstat` and `git diff --numstat`,
   which agree, while that commit's own `--stat` summary printed 358/312 under
   rewrite detection (`rewrite .agent/last_block.md (79%)`). Both readings are
   under 500; the numstat pair is the one G8 orders.
4. G5 writes `Done: R-` where constraint 8 wants a named pattern. Both readings
   reported: line-anchored 1→1, unanchored 34→34, unchanged under either.
5. `.agent/live_review.md` carries 18 unanchored `<<<` occurrences at base and
   24 at C2, RECORD34 contributing 6 as it quotes the marker names. G8 rightly
   does NOT order that count — it is the R-0630 class C2 records.
6. No departure from the ordered commit sequence: exactly C0a, C0b, C1, C2, C3,
   C4 — none extra, dropped or reordered. No finding id minted or resolved.
7. DECISION D15, size: 115 lines, over the ≤100 tier this round's six commit
   tables earn. Mandated cause: six commit tables, eight gate lines, the
   item-status table, the authored-text section and seven deviations, of which
   four are false or unmeetable gate clauses that must be evidenced rather than
   asserted. No section was dropped and no transcript is restated here.

## Next
R34's OWN VERDICT IS UNRECORDED and the next round's ledger commit owes it, with
the three readings C4 cannot state about itself: C4's SHA, its insertion count
and its `wc -l`. R35 is the WIRING — `ActivityFeedCard` renders a resolvable row
as a button emitting `onSelectNode`, `RightLivePanel` passes the task list down,
and a `tests/ui_contracts/` contract pins that the component really calls
`nodeIdForFeedRow`, which lands this round with no caller. R36 is the disabled
steering input with the F030 tooltip. The next session's first action is Phase 1
rule 1, re-reading `.agent/STOP` from disk, before rule 2.

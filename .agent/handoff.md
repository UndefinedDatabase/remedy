# Handback — F021 R22 (the injected transport clock)

Feature F021 Live activity feed + now-card · round R22 · branch `feature/f021-live-activity-feed`
Round base: `bf0c50bfa61991f80925c4e48b33b5e5663a4029` (the R21 handback commit).
Fortschritt: ~88 % (T002 — die vier reinen Regeln stehen; die Verdrahtung ist in
             vier kleine Runden zerlegt, R22 legt die Uhr als Abhaengigkeit)
             — Schaetzung

## Range
Review of `bf0c50bf`..`329a1727` (C0a–C4); C5 below is the commit that writes this file.

## Commits

### 1580fded docs(state): save the F021 R22 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f021-r22.md | +417/-0 | C0a — the R22 block, NEW |

### 75a439ea docs(state): mirror the F021 R22 step block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +358/-168 | C0b — written FROM the committed C0a blob |

### 0f100c6c docs(state): point the F021 plan at R22, the clock round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +19/-16 | C1 — PLANF021R22 plus one terminating newline |

### 33b44b4a docs(review): record the R21 verdict and DECISION F021 D6
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | C2 — RECORD22 appended; no older entry opened |

### 8aca4145 feat(ui): inject the client clock into the brain-stream transport
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/brainStreamHost.ts | +4/-0 | C3 — HOSTDEPSNOW: `now()` on BrainStreamHostDeps |
| apps/ui/src/api/brainStreamDeps.ts | +15/-0 | C3 — ENVNOW, DEPSRETURNNOW, GLOBALSDATE, BROWSERNOW |
| apps/ui/src/api/brainStreamHost.test.ts | +3/-0 | C3 — HOSTFAKENOW |
| apps/ui/src/api/brainStreamSession.test.ts | +3/-0 | C3 — SESSIONFAKENOW, the pair `tsc` forced |
| apps/ui/src/api/brainStreamDeps.test.ts | +13/-0 | C3 — RECORDERNOW, DEPSFORWARDCASE, GLOBALSFAKEDATE, BROWSERNOWCASE |

### 329a1727 test(ui-contracts): pin the injected transport clock
| Path | +/- | Reason |
|---|---|---|
| tests/ui_contracts/test_brain_stream_ring.py | +37/-0 | C4 — CONTRACTHOSTPATH pair + CONTRACTCLOCK append |

### C5 docs(state): hand back F021 R22 — the handback commit, which cannot name its own SHA (R-0494)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C5 — this file |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | eleven pairs, all APPEND-shaped |
| C4 | done | the twelfth pair plus the contract append |
| C5 | done | this commit |

## External actions
`git push -u origin feature/f021-live-activity-feed` runs immediately after C5; a handoff cannot table its own push, so the outcome is in the round report. No PR created, no PR merged, no worktree added or removed. `gh pr list --state open --json number,headRefName` → `[]`.

## Verification — one line per gate; transcripts kept in the round report (R-0582)
G1 PASS — `.agent/STOP` ABSENT before C0a and again before C5; branch `feature/f021-live-activity-feed`; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3 and C4. Owed reading: `bf0c50bf` is single-parent and touches `.agent/handoff.md` alone at +41/-57, under the 500-insertion cap.
G2 PASS — sha256 `d36c446a31dd7b1dafda420f97ee58511bc1c96f01601da4c730e8315449f136`, 26881 bytes, 417 lines, EQUAL across all four copies (bytes read, `.remedy-wt/f021-r22.md`, the C0a blob, the C0b blob); C0b was written FROM the committed C0a blob.
G3 PASS with a reported discrepancy — the marker-line extractor over the committed C0a blob read 12 PAIRS and 3 whole-text slices (PLANF021R22, RECORD22, CONTRACTCLOCK) over 162 CONTENT lines; TOTAL 417 against D6's 490 and PROSE 255 against D5's 400, both EQUAL to constraint 8. G3's prose says "the two whole texts"; the MEASURED count is 3 and constraint 8's arithmetic counts all 3 — see Deviations.
G4 PASS — all twelve pairs: ANCHOR count at the round base EXACTLY 1, and ANCHOR-plus-newline-plus-ADD EXACTLY 1 at the commit that applied it (eleven at `8aca4145`, CONTRACTHOSTPATH at `329a1727`). The twelve-row table is in the round report. No FROM-zero count was ordered or taken (constraint 4).
G5 PASS on the append, with a reported discrepancy on the prefix clause — remainder EXACTLY one newline + CONTRACTCLOCK + one newline, sha256 `18c9ab17288e29a09be4b78ceed2f8ba9a4c83d43dbf1b00f66bdb0996aea203`, 1713 bytes, 36 lines; the file is 14374 B / 326 L at C3, 14412 B / 327 L after CONTRACTHOSTPATH and 16125 B / 363 L at C4. ORDERED EQUALITY: C4's 37 added lines are CONTRACTHOSTPATH's single ADD line, then the convention's one newline, then CONTRACTCLOCK's 35 lines IN ORDER. The C3 blob is NOT a byte-prefix of the C4 file, because the same commit's pair inserts mid-file — see Deviations.
G6 PASS — `cmp` of `.agent/plan.md` against PLANF021R22 plus one terminator exit 0; NEGATIVE CONTROL against the bare slice exit 1; last byte is a newline; `wc -l` reads EXACTLY 46, the ordered and measured value; `^## Goal$` 1 and `^## Next Steps$` 1.
G7 PASS — reader (a): the base blob is a byte-exact PREFIX, remainder exactly one newline + RECORD22 + one newline, sha256 `43408753c14e405b6159deb4c69fb43575f75b9bf55271175e8865d3ae6c6e82`, 5163 bytes, 4 lines; file 529237 B / 1136 L before, 534400 B / 1140 L after. reader (b): units 249 → 251 ELEMENTWISE over the whole list, RECORD22 exactly 2 units. NEGATIVE CONTROL at offset 5, inside the FIRST paragraph, `e` → `X` at equal length: BOTH readers REJECT it and BOTH accept the true file. The base blob was read with `git show` into `.remedy-wt/`; no tracked file was overwritten.
G8 PASS — round base → C2: `- R-` 218 → 218, all DISTINCT at both points; maximum `R-0655` at both; `Done: R-` 0 and `Landed: ` 0 at both; `Gate: R` keys 20 → 21, both DISTINCT; `Gate: R22` 0 → 1. No id minted, none resolved.
G9 PASS — run SERIALLY, never two at once, counting by passed plus skipped. cwd `/home/decodeux/Repos/remedy/apps/ui`: `npx tsc --noEmit` exit 0 with output EMPTY (0 bytes on stdout and stderr) — the load-bearing gate; `npm run test:unit` exit 0 at 15 files / 209 tests. cwd `/home/decodeux/Repos/remedy`: `tests/ui_contracts/` exit 0 at 465 passed + 4 skipped = 469; the three state-reading suites exit 0 at 511; the golden-path canary exit 0 at 42. Every total equals the ordered value. No docs gate is owed.
G10 PASS — base..C4: 6 commits, every one single-parent; the path set EQUALS the ten non-handoff `Change:` paths with both differences EMPTY; `git show --numstat` and `git diff --numstat` agree cell by cell with the tables above; insertions 417, 358, 19, 4, 38 and 37, each under the 500 cap; `git ls-files .remedy-wt` 0; `git worktree list` the primary checkout alone, no worktree created; `gh pr list --state open` `[]`, and neither `gh pr create` nor `gh pr merge` was run; the LINE-ANCHORED marker sweep reads 0 for all four marker prefixes in each of the eight files a slice landed in; the reflog read BY OPERATION shows this round's six rows all `commit`, with `amend`, `rebase` and `cherry` each 0 in that field.

## Authored-text proofs
`.agent/authored/f021-r22.md` at C0a and `.agent/last_block.md` at C0b are byte-identical to the block as read, at the G2 digest. PLANF021R22 → `.agent/plan.md` by `cmp` exit 0 with the bare-slice control at exit 1 (G6). RECORD22 → `.agent/live_review.md` under two independent readers with a rejected mutant (G7). CONTRACTCLOCK → `tests/ui_contracts/test_brain_stream_ring.py` by remainder equality and ordered line equality (G5). All three slices and all twelve pairs were extracted MECHANICALLY from the committed C0a blob by their marker LINES; nothing was hand-copied, retyped or reflowed.

## Deviations & assumptions
No departure from the ordered commit sequence: C0a, C0b, C1, C2, C3, C4, C5 exactly — no extra commit, none dropped, no reordering. No slice was altered and no path outside `Change:` was written.
Reported discrepancy 1 (block text, NOT repaired): G3 calls the `<<<SLICE `/`<<<END ` texts "the two whole texts"; the extractor read THREE — PLANF021R22, RECORD22 and CONTRACTCLOCK. Constraint 8's own arithmetic counts all three (162 CONTENT lines, PROSE 255), so the numeral "two" in G3 is the outlier. Nothing was adjusted to close the gap.
Reported discrepancy 2 (gate text, NOT repaired): G5 asks that the PRE-COMMIT blob of the contract file be a byte-exact PREFIX of the post-commit file. C4 also applies pair CONTRACTHOSTPATH, which inserts a line MID-FILE, so that clause is unmeetable as literally written; measured, the C3 blob is not a prefix (reported False). The append itself was gated against the post-pair blob, where the prefix holds and the remainder is exactly one newline + CONTRACTCLOCK + one newline, and the ordered-equality clause was met over C4's whole added-line list.
DECISION D15 — this handback is 90 lines against the 60-line base cap, within the ≤100 the template allows when per-commit tables of more than five commits require it. Cause, mandated content only: seven per-commit changed-files tables, the item-status table, and one line for each of ten gates whose readings ARE the evidence. No section was dropped and no transcript was inlined.

## Next
The next round is R23: the frame event carries `receivedAtMs` — `brainStreamDriver.ts`'s event union and `brainStreamHost.ts`'s `tell`, stamped from the clock THIS round installed, with their vitest cases and a contract line. DECISION F021 D6, written into `.agent/live_review.md` at C2, holds the four-round decomposition (R22 the clock, R23 the frame stamp, R24 the ring's row, R25 the NowCard's badge and dot, R26 the scroll container and pill) and the two rejected alternatives. R22's own verdict is UNRECORDED and R23's C2 owes it. A new session begins at docs/agents/self_drive_protocol.md Phase 1 rule 1 — the `.agent/STOP` check — BEFORE rule 2's Open PR Gate (R-0347); rule 2 will find no open pull request, so F021 continues on this branch.
Open findings: 218 open, maximum R-0655, next free R-0656 — none registered this round, none resolved.

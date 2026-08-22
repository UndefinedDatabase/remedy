# Handoff — F021 Live activity feed · R14 · make the feed live from the published ring

Round base 9fcce96de76740dc21953d68214ec7a171a40b5f · branch feature/f021-live-activity-feed · open findings 213, max R-0650, next free R-0651; this round mints and resolves none.

Fortschritt: ~70 % (T002 fertig — der Stream erreicht jetzt wirklich die
             Oberflaeche: Ring, View, Props und Feed haengen zusammen; es
             fehlen NowCard-Verfeinerung, Scroll-Disziplin und T003)
             — Schaetzung

## Range
Review of 9fcce96de76740dc21953d68214ec7a171a40b5f..HEAD.

## Commits
### b71b15dc docs(state): save the F021 R14 live-feed block as authored text
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f021-r14.md | 440/0 | C0a — the received block saved byte for byte |

### 9f8f8f75 docs(state): mirror the F021 R14 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | 318/293 | C0b — written FROM the committed C0a blob |

### 8c6a1225 docs(state): point the F021 plan at R14 and the live feed
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | 18/17 | C1 — PLANF021R14 plus one terminating newline |

### a7641178 docs(review): record the R13 verdict as PASS with no new finding
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | C2 — RECORD13 appended; no id minted, none resolved |

### e50e8fbe feat(ui): render the live brain-stream ring in the activity feed
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/panels/ActivityFeedCard.tsx | 50/1 | C3 — AFC1, AFC2: LIVE_ROWS_SHOWN, LiveFeed newest-first, the dropped-rows notice |
| apps/ui/src/components/panels/RightLivePanel.tsx | 3/2 | C3 — RLP0, RLP1, RLP2: the ring passes through the panel |
| apps/ui/src/components/shell/RemedyShell.tsx | 1/1 | C3 — SHELL1: the one useBrainStream call hands the ring down |
| tests/ui_contracts/test_brain_stream_ring.py | 47/0 | C3 — CONTRACTPATHS pair, then CONTRACTFEED's 4 cases |

### C4 docs(state): hand back F021 R14 — SHA UNNAMEABLE HERE because this is the commit that writes this file, the R-0149 self-reference exception
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | this file | C4 — the handback |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | this commit |

## External actions
- `git worktree add --detach .remedy-wt/wt-f021-r14-redctl e50e8fbe` — created for G12 only; `git worktree remove --force` + `git worktree prune`; list is the primary checkout alone.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` — exit 0, `[]`. Neither `gh pr create` nor `gh pr merge` was run; F021 is mid-feature.
- `git push -u origin feature/f021-live-activity-feed` — after C4, per constraint 8.

## Verification
One line per gate; the transcripts stay in the round report (R-0582). All fourteen executed with real exit codes.
- G1 PASS — `.agent/STOP` absent before C0a and again before C4; branch `feature/f021-live-activity-feed`; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3. Owed reading: 9fcce96d is single-parent, touches `.agent/handoff.md` alone, 47 insertions / 65 deletions, under the 500 cap.
- G2 PASS — sha256 `c7010621d32bd48e2d90cff21665e4f96549302d9bee3071021ec56c75361ab5`, 30876 bytes, 440 lines, EQUAL over the received bytes, `.remedy-wt/f021-r14.md`, C0a and C0b; C0b written from the committed C0a blob.
- G3 PASS — extractor over the committed C0a blob by marker LINES: 17 slices, 161 CONTENT lines. TOTAL 440 vs D6's 490; PROSE 440−161 = 279 vs D5's 400. Both equal constraint 9.
- G4 PASS — `cmp .agent/plan.md` against PLANF021R14+NL exit 0; negative control against the bare slice exit 1 (EOF after byte 2517). Last byte is a newline; `^## Goal$` 1; `^## Next Steps$` 1; `wc -l` 44 ≤ 50.
- G5 PASS — reader (a): base blob (481235 B, 1102 L, sha `8039ef00…`) read via `git show <base>:<path>` into `.remedy-wt/`, a byte-exact PREFIX of C2 (486845 B, 1104 L); remainder 5610 B, 2 L, sha `5f1e83064ed6159319376ee06bfc63a6265766b4c508d8b8510d0b55b36fec96` == NL+RECORD13+NL. Reader (b) set-wise: units 232 → 233, RECORD13 = 1 unit, ELEMENTWISE equal over the whole list. Negative control at offset 2 of the FIRST paragraph, `L`→`Q` at equal length: both readers REJECT it and ACCEPT the true file.
- G6 PASS — base then C2: `- R-` 213 → 213, DISTINCT 213 → 213; maximum R-0650 → R-0650; `Done: R-` 0 → 0; `Landed: ` 0 → 0; `Gate: R` keys 13 → 14, both DISTINCT; `Gate: R14` 0 → 1. Every value as ordered.
- G7 PASS — whole-string over raw bytes, twenty-one numbers. At the ROUND BASE every FROM is 1 (AFC1, AFC2, RLP0, RLP1, RLP2, SHELL1, CONTRACTPATHS). At C3, by shape: APPEND-SHAPED AFC1 FROM 1 TO 1, RLP0 FROM 1 TO 1, CONTRACTPATHS FROM 1 TO 1; REPLACING AFC2 FROM 0 TO 1, RLP1 FROM 0 TO 1, RLP2 FROM 0 TO 1, SHELL1 FROM 0 TO 1.
- G8 PASS — prefix plus remainder, never a per-line count. The prefix side is the CONTRACTPATHS-SUBSTITUTED base blob of `test_brain_stream_ring.py` (5863 B), a byte-exact prefix of that file at C3; remainder 1874 B, 42 L, sha `e2c220f8385021ceba156ac14a11284830bc575ef70919bd765fa7cf38791cb1`, == NL+CONTRACTFEED+NL.
- G9 PASS — blank lines immediately before CONTRACTFEED's `class TestTheFeedIsFedFromTheStream:` line in the C3 file: 2. Counted, not delegated to ruff (R-0558). CONTRACTFEED's leading blank was not trimmed.
- G10 PASS — `npx tsc --noEmit`, cwd `/home/decodeux/Repos/remedy/apps/ui`, exit 0, stdout and stderr both EMPTY.
- G11 PASS — `npx vitest run`, cwd `/home/decodeux/Repos/remedy/apps/ui`, PRIMARY checkout, exit 0: 12 files, 177 tests. UNCHANGED from the round base, as ordered; this round adds no vitest case.
- G12 PASS — worktree `.remedy-wt/wt-f021-r14-redctl` at e50e8fbe, a name no directory already used. GREEN FIRST: exit 0, 17 passed. The mutation target occurs EXACTLY ONCE in that worktree's `RemedyShell.tsx`; the two new props were removed from it. Re-run: exit 1, EXACTLY 1 failed / 16 passed, the failure `TestTheFeedIsFedFromTheStream::test_the_shell_hands_the_ring_to_the_panel`, assertion "the ring is published on the view but never handed to the panel". Worktree removed and pruned.
- G13 PASS — PRIMARY checkout, SERIALLY, cwd `/home/decodeux/Repos/remedy` (the repository root) for all three. `tests/ui_contracts/` exit 0, 443 passed + 4 skipped = 447. `tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py` exit 0, 511. `tests/cli/test_golden_path.py` exit 0, 42 (canary). No docs gate owed.
- G14 PASS with ONE clause declared unmeetable, below — base..C3: path set is the eight non-handoff `Change:` paths, BOTH differences EMPTY; all 5 commits single-parent; `git show --numstat` and `git diff --numstat` agree cell by cell with `## Commits` above; insertions 440, 318, 18, 2, 101 — every one under 500; `git ls-files .remedy-wt` 0; `git worktree list` the primary checkout alone; `gh pr list --state open` EMPTY and neither `gh pr create` nor `gh pr merge` was run. Reflog by OPERATION — the text before the first `:` in `git reflog --format=%gs`, scoped to this round's 5 rows — every operation is `commit`, and `amend`, `rebase`, `cherry` are each 0 in that field.

## Authored-text proofs
- `.agent/authored/f021-r14.md` at C0a, `.agent/last_block.md` at C0b, the received bytes and the reviewer's emitted `.remedy-wt/f021-r14.md` are all sha256 `c7010621…1ab5` over 30876 bytes / 440 lines (G2).
- Every applied slice was extracted MECHANICALLY from the committed C0a blob by its marker lines and never retyped: PLANF021R14 by `cmp` exit 0 with a red control at exit 1 (G4); RECORD13 by two independent readers with a negative control (G5); the seven pairs by whole-string byte counts (G7); CONTRACTFEED by prefix-plus-remainder digest (G8).

## Deviations & assumptions
- No departure from the ordered commit sequence: C0a, C0b, C1, C2, C3, C4 were committed in exactly that order, six commits, none added, none dropped, none reordered.
- G14's marker clause is UNMEETABLE AS WRITTEN on one path and is reported rather than reconciled. `<<<SLICE `/`<<<END ` LINES at C3 read 0 in `.agent/plan.md`, `ActivityFeedCard.tsx`, `RightLivePanel.tsx`, `RemedyShell.tsx` and `test_brain_stream_ring.py`, but 1 in `.agent/live_review.md`. That single line is line 1078, the pre-existing `Gate: R5` entry whose PROSE quotes the marker text; it reads 1 at the ROUND BASE too, so the clause is already red at base and cannot fail honestly (R-0364). This round's delta is 0: the bytes C2 appended carry no marker line. The ledger was NOT edited to make the clause green. This is the R-0563 / "a gate quotes its own wording" class; the counter-measure a future block owes is to scope the clause to the round's ADDED bytes, or to exclude `.agent/live_review.md` by name.
- Constraint 5 (pairs before appends) was applied PER TARGET FILE as constraint 5 itself now states: in `test_brain_stream_ring.py` the CONTRACTPATHS pair was applied first and CONTRACTFEED appended second; no pair touches `.agent/live_review.md`, so C2's append disturbs nothing.
- G14's reflog clause was measured by OPERATION, never by substring over whole rows. For contrast only, a substring count over whole reflog rows repo-wide reads amend 82 / rebase 26 / cherry 60, because this repository's commit SUBJECTS discuss amends by design; that count is not this gate.
- `npm run lint` in `apps/ui` is RED at base (R-0622); it is not a gate here and was not run. No formatter or linter that rewrites files was run. No CSS, asset or icon was added; `@mui` and `POST` were not introduced and the word `Activity` was not removed.
- `.remedy-wt/` holds this round's scratch and is gitignored — `git ls-files .remedy-wt` is 0. That directory's presence in a review zip stays R-0403, routed to a paydown branch.
- DECISION D15 declared overage: this file is 93 lines against the 60-line cap, within the ≤100 the template allows when per-commit tables of more than five commits require it. Cause is mandated content only — six per-commit changed-files tables, the item-status table, fourteen one-line gate readings carrying the numerals G1-G14 order, and the four-line `Fortschritt:` block. No section was dropped and no prose padding was added.

## Next
THIS SESSION ENDS WITH C4. The next session's FIRST action is docs/agents/self_drive_protocol.md Phase 1 rule 1 — re-read `.agent/STOP` from disk — BEFORE rule 2's Open PR Gate (R-0347). Rule 2 will find NO open pull request, so rule 5 applies and F021 continues on this branch. R14's OWN VERDICT IS UNRECORDED: the next round's C2 owes it. R15 is the scroll discipline that never yanks a reader who has scrolled up, plus the NowCard over the ACTION-class subset with its recency dot.

# F021 R31 handback — T002, the feed-scroll wiring

Fortschritt: ~98 % (T002 — Feed-Scroll verdrahtet; es fehlt nur noch T003:
             Klick-Sprung und der deaktivierte Steuer-Eingang)
             — Schaetzung

Branch `feature/f021-live-activity-feed`. ROUND BASE `d63d29e89c783ee973fdac10a608f76b2f3898e7`.

## Range
Review of d63d29e8..b9c7d726 (C0a-C6). C7 is the commit that writes this file.

## Items
| Item | Commit | Status | Reason |
|---|---|---|---|
| C0a | bd732c0b | done | block copied verbatim, sha256 verified |
| C0b | 834f53f5 | done | written FROM the committed C0a blob |
| C1 | ff4c687f | done | |
| C2 | 433daa59 | done | |
| C3 | c70a6e87 | done | |
| C4 | a23990a2 | done | |
| C5 | d1951b00 | done | |
| C6 | b9c7d726 | done | |
| C7 | this commit | done | rewrites `.agent/handoff.md`; cannot name its own SHA |

## Commits
### bd732c0b chore(agent): save the F021 R31 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f021-r31.md | +480/-0 | the block, verbatim (C0a) |
### 834f53f5 chore(agent): mirror the R31 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +409/-174 | mirror written from the C0a blob (C0b) |
### ff4c687f docs(state): point the F021 plan at R31, the feed-scroll wiring round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +19/-20 | PLANF021R31 plus one terminator (C1) |
### 433daa59 docs(review): record the R30 PASS and correct its hand-read count
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | RECORD31 appended (C2) |
### c70a6e87 docs(state): rule the feed axis and window size as F021 D10
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +4/-0 | DECISION10 appended (C3) |
### a23990a2 feat(ui): give the live feed a 52vh scroll box and a jump-to-live pill
| Path | +/- | Reason |
|---|---|---|
| ...panels/RightLivePanel.module.css | +16/-1 | CSSPAIR (C4) |
### d1951b00 feat(ui): wire the feed scroll rule and jump-to-live into the activity card
| Path | +/- | Reason |
|---|---|---|
| ...panels/ActivityFeedCard.tsx | +58/-5 | CARDIMPORT and CARDFEED (C5) |
### b9c7d726 test(ui-contracts): pin the feed scroll wiring and the scrollable box
| Path | +/- | Reason |
|---|---|---|
| tests/ui_contracts/test_brain_stream_ring.py | +54/-0 | PINSLICE appended (C6) |
### C7 docs(state): hand back F021 R31 — the handoff commit, which cannot table itself
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | see `## Next` | this file; its own numbers are owed to R32 |

## External actions
`git worktree add .remedy-wt/r31-red b9c7d726 --detach` — created, used for G10 only.
`git worktree remove --force` + `git worktree prune` — removed; list is the primary checkout alone.
`gh pr list --state open --json number,headRefName` — `[]`. No `gh pr create`, no `gh pr merge`.
`git push -u origin feature/f021-live-activity-feed` after C7 — outcome in `## Next`.

## Verification
G1 `.agent/STOP` ABSENT before C0a and again before C7; branch correct; `git status --porcelain` 0 lines after each of C0a-C6.
G2 TRANSPORT sha256 517a68fabc2a291a6ceaf75deab36b032e0e2c98d20da974f94293c9fcba4abd, 37455 bytes, 480 lines, EQUAL across all four copies.
G3 SLICES extracted from the C0a blob by marker line: 4 whole texts, 3 pairs, 210 CONTENT lines, 17 marker lines, 0 stray `<<<`; TOTAL 480 (cap 490), PROSE 270 (cap 400).
G4 `cmp` plan vs slice+NL exit 0; NEGATIVE CONTROL vs bare slice exit 1; last byte is a newline; `^## Goal$` 1; `^## Next Steps$` 1; `wc -l` 47, under 50.
G5a live_review remainder sha256 e41e95369fe0a41e6248fcec4120fb88deb2ccb152a345c6887b5113a555b9ab 6542 B/4 L; 604034 B/1192 L to 610576 B/1196 L; units 277 to 279 ELEMENTWISE, RECORD31 2 units; join 1 blank line; control offset 2 `L`->`Z` REJECTED by both readers, true file ACCEPTED by both; numstat 4/0, no deletion.
G5b decisions remainder sha256 9c67c28d5528137d8964369a29d81f15951484597c9b050aea00af80f4d82f32 2803 B/4 L; 502967 B/7020 L to 505770 B/7024 L; units 1240 to 1242 ELEMENTWISE, DECISION10 2 units; join 1 blank line; control offset 2 `D`->`Z` REJECTED by both, true file ACCEPTED by both; numstat 4/0, no deletion.
G6 CSSPAIR FROM 1x->0x and TO 0x->1x; CARDIMPORT 1x->0x, 0x->1x; CARDFEED 1x->0x, 0x->1x; at C4 `max-height: 52vh` 1, `overflow: auto` 1, `.jumpToLivePill` 1 at line start.
G7 canonical `^- R-\d+ — ` 223, all DISTINCT, max R-0660 at BOTH commits; loose `- R-` 224 at both, UNMOVED; `Done: R-` 1/1; `Landed: ` 0/0; `Gate: R` keys 29 then 30, DISTINCT at both; `Gate: R31` 0 then 1; `- R-0661` 0/0; RECORD31 lines starting `- R-` 0; `^Recurrence: R-0644 — ` 0 then 1; `^Recurrence: ` 2 then 3; `- R-0644 — ` 1 at both. C3: `^## DECISION F021 D10 ` 1, LAST such heading, 1 blank line above.
G8 comment-stripped card: `recent.slice(-LIVE_ROWS_SHOWN).reverse()` 1, `recentDropped > 0` 1, `shouldFollowNewest` 2, `shouldShowNewRowsPill` 2, `nextFeedScroll` 3, `FEED_SCROLL_START` 3, `scrollTop` 3, `from "../../api/feedScroll"` 1; raw: `emptyState` 2, `No activity yet` 1, `Activity` 7, `@mui` 0, `POST` 0.
G9 `npx tsc --noEmit` (apps/ui) exit 0, output EMPTY; `npm run test:unit` (apps/ui) exit 0, 15 files / 212 tests, UNCHANGED; from the repo root, serially: `tests/ui_contracts/` exit 0, base 478+4=482 to 484+4=488, difference 6 = PINSLICE's 6 test functions counted from the committed slice; state readers exit 0, 511+0; canary exit 0, 42+0.
G10 in `.remedy-wt/r31-red` at b9c7d726: GREEN 58 passed; after deleting the 3 lines RED, exit 1, 1 failed / 57 passed, FAILED `tests/ui_contracts/test_brain_stream_ring.py::TestTheFeedScrollRuleIsWiredToTheCard::test_the_card_never_scrolls_without_asking_the_rule`; worktree removed and pruned, `git worktree list` the primary checkout ALONE.
G11 path set 8 EQUAL to the eight non-handoff `Change:` paths, both differences EMPTY; 8 commits, every one single-parent; `git show --numstat` and `git diff --numstat` agree cell by cell with the tables above; insertions 480, 409, 19, 4, 4, 16, 58, 54, each under 500; `git ls-files .remedy-wt` 0; marker sweep line-anchored 0 for all 4 prefixes AND 0 lines starting `<<<` in each of the 6 files a slice or pair landed in; reflog OPERATION field every row `commit`, `amend`/`rebase`/`cherry` 0 each; `gh pr list --state open` EMPTY.

## Authored-text proofs
`.agent/plan.md` vs PLANF021R31+NL: `cmp` exit 0; vs the bare slice: exit 1. RECORD31, DECISION10, PINSLICE and all three pair halves were extracted MECHANICALLY from the committed C0a blob by marker line and applied by byte replacement; no slice was retyped.

## Deviations & assumptions
No departure from the ordered commit sequence C0a, C0b, C1, C2, C3, C4, C5, C6, C7: nine commits, in that order, nothing extra, nothing dropped.
DECLARED 1, applied not fixed (constraint 1). Constraint 5 fixes the PINSLICE join at ONE blank line; all 14 pre-existing top-level classes in `tests/ui_contracts/test_brain_stream_ring.py` sit behind TWO, which is PEP 8 E302. I applied the block's convention literally. `python3 -m ruff check` on that file is exit 0 (E301-E306 are preview-only), so no ordered gate sees it, but the file is now inconsistent with itself.
DECLARED 2, a measurement in G10 that does not hold. The block states the mutation target occurs once "whole-line and indent-agnostic counts agreeing". At C5/C6 the whole-line count is 0 and the indent-agnostic count is 1 — the line is indented four spaces, so whole-line equality is 0 by construction and the two readings DISAGREE. The target is still unique under two independent readings (substring 1, indent-agnostic 1), so the red control was run and is reported above.
DECLARED 3, applied not fixed (constraint 1). CSSPAIR's TO writes `border-radius: var(--remedy-radius-pill)`, and `--remedy-radius-pill` is defined NOWHERE: `apps/ui/src/styles/tokens.css` defines only `--remedy-radius-xl/lg/md/sm`. The pill therefore renders with square corners (the undefined var falls back to the initial value). The other three custom properties in that block resolve. No gate of this round covers CSS variable resolution.
DECISION D15, handback size: this file measures 96 lines by `wc -l`, over the 60-line baseline and WITHIN the 100-line tier AGENTS.md grants a handback whose per-commit tables cover more than five commits, which this one's nine do. The mandated content causing the overage is the nine per-commit tables, the item-status table, the eleven per-gate lines and the three declared deviations.

## Next
R31's OWN VERDICT IS UNRECORDED. The next round's ledger commit owes it, together with the readings C7 cannot state about itself: C7's insertion count and this file's line count, both measured from `git show --numstat` at C7.
R32 is T003 — the row click-jump to the graph store, then the disabled steering input with the tooltip naming F030.
First action of the next session is Phase 1 rule 1, `.agent/STOP`, before Phase 1 rule 2, the Open PR Gate.

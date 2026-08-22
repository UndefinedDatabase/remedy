# Handback — F021 R2 (measurement round)

Feature F021 Live activity feed + now-card, round R2, branch
feature/f021-live-activity-feed, round base `5179725f5680eea91a9ce627c188cab94dde144b`.
Fortschritt: ~5 % (T001 offen · T002 offen · T003 offen; R1 hat das Feature
             beansprucht, diese Runde vermisst den Boden — Humanize-Katalog,
             Feed und NowCard werden ab R4 gebaut) — Schätzung

## Range
Review of `5179725f5680eea91a9ce627c188cab94dde144b..HEAD` (5 commits).

## Commits
### 78afebcc chore(agent): save the F021 R2 measurement block as authored text
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f021-r2.md | 226/0 | C0a, the R2 block saved verbatim, NEW |
### 2a5e6611 chore(agent): mirror the F021 R2 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | 172/296 | C0b, written from the committed C0a blob |
### 41bb3bf2 docs(state): point the F021 plan at the R2 measurement round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | 17/16 | C1, PLANF021R2 applied in full |
### 2488ff1d docs(review): record the R1 verdict as PASS
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | C2, RECORD1 appended after the base blob |
### C3 (SHA ABSENT BY CONSTRUCTION — C3 is the final commit and it writes this very file, so it cannot carry its own identifier, the R-0149 pattern; its SHA is in the round report) docs(state): record the F021 R2 source inventory and hand back R2
| Path | +/- | Reason |
|---|---|---|
| .agent/f021_inventory.md | 320/0 | C3, the measured inventory, NEW |
| .agent/handoff.md | 63/66 | C3, this handback, measured on staged content |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |

## External actions
`git worktree add --detach .remedy-wt/f021r2-wt 2488ff1d` for G5's destructive
half, then `git worktree remove --force` and `git worktree prune` — `git worktree
list` afterwards shows the primary checkout only. `git push -u origin
feature/f021-live-activity-feed` runs after C3 as the block's last step; its
outcome is in the round report. No PR created, none merged, no `gh pr create` and
no `gh pr merge` run.

## Verification
- G1 STOP absent immediately before C0a and again immediately before C3; branch feature/f021-live-activity-feed; `git status --porcelain` 0 lines after each of C0a, C0b, C1 and C2; C3's own reading is in the round report (checklist item 14).
- G2 TRANSPORT: `.agent/authored/f021-r2.md` at C0a, `.agent/last_block.md` at C0b and the received bytes are all sha256 9e0b791a263135fd11d1502b45d5c4c87722ed31988145375d8f114f0214e4da over 19837 bytes and 226 lines; C0b was written FROM the committed C0a blob.
- G3 SLICES: the marker-line extractor over the committed C0a blob printed 2 slices over 45 CONTENT lines; constraint 9 re-measures from that same blob as TOTAL 226 against DECISION F085 D6's 490 and PROSE 181 against D5's 400.
- G4 PLAN: `cmp .agent/plan.md <PLANF021R2>` exit 0, negative control `cmp` against RECORD1 exit 1; `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 44 under the 50 cap.
- G5 APPEND, reader (a): base blob is a byte-exact PREFIX of the C2 file, remainder sha256 cae9be9ff6c179e9a11b2184a15f2d5321259a42e2b013a27078a56a8360bc95 over 4991 bytes and 2 lines, equal to one newline plus RECORD1; file 421786 bytes / 1070 lines before and 426777 bytes / 1072 lines after.
- G5 APPEND, reader (b): blank-line units N 216 at the base and 217 at C2, every carried unit elementwise equal, LAST unit at C2 equals RECORD1 while the base's last unit does not; NEGATIVE CONTROL, one printable byte of the FIRST paragraph replaced at equal length, is REJECTED by BOTH readers while BOTH ACCEPT the true file — run in the disposable worktree named above, since removed and pruned.
- G6 LEDGER SETS, line-anchored, base then C2: `- R-` entries 211 then 211, DISTINCT 211 then 211; `Done: R-` 0 then 0; `Landed: ` 0 then 0; `Gate: R` keys 1 then 2, DISTINCT 1 then 2; `Gate: R2` 0 then 1; MAXIMUM registered id R-0648 at BOTH points, as constraint 3 requires.
- G7 INVENTORY, a SHAPE check that cannot judge whether a reading is TRUE: `wc -l` 320, five sections `## (a)`..`## (e)` present and in order, distinct cited source paths that resolve under `git ls-files` — (a) 7, (b) 3, (c) 7, (d) 8, (e) 10.
- G8 CONTRACT SUITES, primary checkout, serial, on the tree C3 commits: `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py -q -rf` exit 0, 511 passed plus skipped (511 passed, 0 skipped), 40.75s.
- G9 CANARY, run after G8 finished: `python3 -m pytest tests/cli/test_golden_path.py -q -rf` exit 0, 42 passed, 20.51s.
- G10 NO PRODUCTION FILE CHANGED: 0 paths beginning `apps/`, `packages/` or `tests/` in the range; `git ls-files .remedy-wt` reads 0 with every scratch script of this round under `.remedy-wt/f021r2/`; the post-C3 `git status --porcelain` reading is in the round report.
- G11 RANGE, measured base-to-tree with C3 fully staged and re-run after C3: the path set EQUALS the block's six-path `Change:` list, both set differences EMPTY; every commit single-parent; `git show --numstat` and `git diff --numstat` agree cell by cell with the table above; maximum insertions 320 under the 500 cap; leading `<<<SLICE `/`<<<END ` 0 LINES in both `.agent/plan.md` and `.agent/live_review.md`; reflog `amend` 0, `rebase` 0, `cherry` 0.
- G12 NO PULL REQUEST: `gh pr list --state open --json number,headRefName` printed `[]`; this round ran neither `gh pr create` nor `gh pr merge`.
- G13 THIS HANDBACK carries every mandated section of docs/agents/handback_template.md, an item-status row for each of C0a, C0b, C1, C2 and C3, the round base SHA, ONE LINE PER GATE with transcripts kept in the round report (R-0582), and the block's `Fortschritt:` line verbatim across all three of its lines.

## Authored-text proofs
PLANF021R2 to `.agent/plan.md` at C1 — `cmp` exit 0 against the slice extracted
from the committed C0a blob by its marker LINES, with a negative control against
RECORD1 at exit 1 (G4). RECORD1 to `.agent/live_review.md` at C2 — appended, not
replaced, and proved under two independent readers plus a first-paragraph mutant
both readers reject (G5). Both slices were extracted programmatically from the
committed C0a blob and never retyped. There was NO FROM/TO pair this round, so no
containment reading is owed and none is stated (constraint 4).

## Deviations & assumptions
No commit was added, dropped or reordered: C0a, C0b, C1, C2, C3 exactly as the
block ordered them. Constraint 3 held — this round minted no finding id, wrote no
`- R-` entry, no `Done:` and no `Landed:` line; R-0648 stays the maximum and
R-0649 is the next free id. `.agent/f021_inventory.md` is the worker's own
measurement and no claim in it was copied from the feature file, from the block
or from any `.agent/` document. One reading in it contradicts a convenient
assumption and is reported rather than smoothed: the stream envelope
`_safe_event_summary` carries NO task id, so a feed row cannot resolve to a graph
node without a change under `packages/` — that is a design question for R3, not a
defect of this round. DECISION D15 OVERAGE DECLARED: this file is 97 lines
against the 60-line cap a five-commit round allows. The cause is mandated content
only — the per-commit tables for five commits, the item-status table, the
authored-text proofs, and G13's ONE LINE PER GATE over thirteen gates, two of
which (G5's two readers) need a line each. No section was dropped to reach the
cap, and no transcript was moved into this file.

## Next
Reviewer gates this handback against the source and, on PASS, authors R3: rule
the feed's shape as a DECISION on the measured ground, per `.agent/plan.md` Next
Steps item 1.

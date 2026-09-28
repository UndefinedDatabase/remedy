# Handoff — F036, round 7 (the closure sequence's first round: book round 6, register and repair
R-1090, write the Built State, consolidate the checklist, and take the feature's one full suite)

## Session

SESSION 2 of feature F036 · round 7 · rounds so far 7. Context remaining at handback: a large
majority of the context budget is left — this round read AGENTS.md, the block, `STATUS_closure_
protocol.md` preconditions 2/3/7, `integration_gate.md`, R-1090 in the booking diff,
`TourOverlay.module.css`, the actions row of `TourOverlay.tsx`,
`test_tour_overlay_contract.py`, the six `f036-r6-render_*` files, `f036-r6-render.txt` and
`f036-r6-mutations.py` in full before writing anything; wrote the CSS repair and its test (S1/S2),
the round 7 render harness (four byte-copies plus a rewritten `drive.mjs` adding C-k), the round 7
mutation tool, the Built State and the checklist consolidation, and ran every gate (G1–G5,
including the feature's one full-suite run) for real before writing this handback.

## Range

Review of `032c1ce20..HEAD` (`HEAD` is this handback's own commit, `F036 R7 C7`, on
`feature/f036-guided-result-tour`).

## Commits

### 3034d14ef F036 R7 C1: copy round 7 block and payloads
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f036-r7-block.md | 215/0 | copy of the block, verified line count and sha256 |
| .agent/authored/f036-r7-booking.diff | 26/0 | copy of the reviewer's booking.diff payload |
| .agent/authored/f036-r7-closure_docs.diff | 122/0 | copy of the reviewer's closure_docs.diff payload |
| .agent/authored/f036-r7-plan.md | 30/0 | copy of the reviewer's plan.md payload |

393 insertions total, exactly the block's own C1 note (215-line block + 178).

### 34830656f F036 R7 C2: book round 6, resolve R-1088 and R-1089, register R-1090
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 8/0 | round 6's `Gate:` entry, the `Done:` resolutions of R-1089 and R-1088, and the registration of R-1090, appended by booking.diff |
| .agent/plan.md | 9/6 | rewritten to the reviewer's plan.md payload |
| .agent/prose_slips.md | 2/0 | F036's two prose-slip lines (round 5, round 6) appended by booking.diff |

Measured exactly the block's own C2 expected numstat: 8/0, 9/6, 2/0.

### 6659b7df4 F036 R7 C3: keep the tour's action labels on one line in the docked card
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | `Landed: R-1090 —` line appended, preceded by a blank line |
| apps/ui/src/components/tour/TourOverlay.module.css | 4/0 | S1 (a) `white-space: nowrap;` as the `.actions button` rule's last declaration, (b) the R-1090 comment and `.card[data-shown="true"] .actions { flex-wrap: wrap; }` |
| tests/ui_contracts/test_tour_overlay_contract.py | 10/0 | S2 the new test, directly after `test_the_card_carries_data_shown_and_docks_over_the_left_rail_while_shown` |

16 insertions (no expected number stated by the block for C3; measured). Test file ran green:
`10 passed in 0.19s`.

### 258004d42 F036 R7 C4: render the docked card's actions again (1/2)
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f036-r7-render_index.html | 11/0 | S3 byte-copy of round 6's scratch page |
| .agent/authored/f036-r7-render_main.tsx | 130/0 | S3 byte-copy of round 6's harness module |
| .agent/authored/f036-r7-render_measure.py | 191/0 | S3 byte-copy of round 6's runner |
| .agent/authored/f036-r7-render_vite.config.mjs | 28/0 | S3 byte-copy of round 6's scratch build config |

360 insertions (the block's single C4, part 1 of 2 — see Deviations).

### 916b0fbc6 F036 R7 C4: render the docked card's actions again (2/2)
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f036-r7-render.txt | 36/0 | S3 the harness's whole recorded output, `RENDER: 11 of 11 checks pass` |
| .agent/authored/f036-r7-render_drive.mjs | 412/0 | S3 round 6's driver, screenshot paths renamed to `f036-r7-worker`, plus the new C-k check (R-1090) |

448 insertions (the block's single C4, part 2 of 2 — see Deviations).

### f249b148f F036 R7 C5: add the round 7 mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f036-r7-mutations.py | 111/0 | the G4 red-proof tool: m1–m2 through the CONTRACT test, modelled on round 6's CONTRACT route |

### 3b92631a2 F036 R7 C6: write the Built State and consolidate the checklist
| Path | +/- | Reason |
|---|---|---|
| docs/agents/planner_reviewer_prompt.md | 8/0 | the consolidation paragraph, inserted directly before "The next consolidation measures against 34." |
| docs/roadmap/features/T5_F036.md | 95/0 | the Built State section, applied via closure_docs.diff |

Measured exactly the block's own C6 expected numstat: 8/0, 95/0.

### <this commit> F036 R7 C7: record the closure suite transcript and rewrite handoff for round 7
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, per docs/agents/handback_template.md |
| .agent/authored/f036-closure-suite.txt | new | the full-suite command, exit code, wall time, summary line, bad-node-id list (NONE) and the tree it ran on |

## External actions

- `git worktree add .remedy-wt/f036-r7-mut HEAD` (HEAD = `f249b148f`, C5) — the official G4
  worktree. Outcome: worktree created, detached at `f249b148f`.
- `python3 .agent/authored/f036-r7-mutations.py .remedy-wt/f036-r7-mut` inside that worktree —
  outcome: both mutations caught, both controls green, both restorations byte-identical, primary
  checkout clean; `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`.
- `git worktree remove .remedy-wt/f036-r7-mut --force` then `git worktree prune` — the official
  G4 worktree's own cleanup (constraint 6). Outcome: removed; `git worktree list | wc -l` read 61,
  matching the round's step-4 reading.
- `npm --prefix apps/ui run build` (C7a) — outcome: built in 2.15s, REAL_EXIT=0.
- `git push origin feature/f036-guided-result-tour` — run immediately after this commit per the
  bundle order. Its real outcome is reported in the round's reply (G6), not here, because this
  file is written before the push happens.
- No `gh pr create`, no `gh pr merge`, no checkout of `main`, no branch deletion, no force-push,
  no `git stash` — none of these were run, per constraint 5.

## Verification

**G1 TRANSPORT AND RECORDS** — PAYLOADS table readings (before use), all MATCH:
```
booking.diff:      26 lines,  8386 bytes, sha256 37c1472d39f853dd18c48c54620e50a47a16c18e1ea400483fdb02d83ee552dd
closure_docs.diff: 122 lines, 9739 bytes, sha256 98c5969890cc1113f49a7919b3c5c501f753183a0452307af53faf7cf47faaa1
plan.md:            30 lines, 1109 bytes, sha256 4bae9ddf5bfc2f8993f881062877519dcce4239dddc210532fbfe8d6465d88bf
```
Block self-check: 215 lines, sha256
`7792083bb11e6173b9cb6ab8eb0c2d2ab42e83436c104e629778d185ba885e17` — MATCH on both readings given
in the delegation message. `.agent/authored/f036-r7-*` copies vs. sources, read back via
`git show 3034d14ef:<path>`, all byte-identical (also sha256-verified):
```
f036-r7-block.md          vs .remedy-wt/f036-r7/block.md                    MATCH
f036-r7-booking.diff      vs .remedy-wt/f036-r7-payloads/booking.diff       MATCH
f036-r7-closure_docs.diff vs .remedy-wt/f036-r7-payloads/closure_docs.diff  MATCH
f036-r7-plan.md           vs .remedy-wt/f036-r7-payloads/plan.md            MATCH
```
`open_finding_ids` over `.agent/live_review.md` at C2 (`scripts.rotate_live_review`) read
`['R-1090']`, matching. `latest_gate_verdict` read `PASS`, matching. Bytes/sha256 at C2
(`.agent/live_review.md` 338454 bytes, `.agent/prose_slips.md` 376317 bytes, `.agent/plan.md` 1109
bytes) all MATCH the reviewer's table, sha256 included. Bytes/sha256 at C6
(`docs/roadmap/features/T5_F036.md` 12363 bytes, `docs/agents/planner_reviewer_prompt.md` 109446
bytes) both MATCH, sha256 included. `live_checklist_items` over the planner prompt
(`packages.orchestration.block_lint`) read 34 items both at `032c1ce2` and at C6 — the
consolidation joined nothing, as the block specifies.

**G2 THE CODE AND THE TESTS** — at C6 (`3b92631a2`), serially:
```
python3 -m ruff check tests/ui_contracts/test_tour_overlay_contract.py \
  .agent/authored/f036-r7-render_measure.py .agent/authored/f036-r7-mutations.py
All checks passed!
REAL_EXIT=0
```
```
python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/docs \
  tests/cli/test_golden_path.py tests/orchestration/test_block_lint.py \
  tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py
1450 passed, 4 skipped in 44.78s
REAL_EXIT=0
```
SKIPPED lines (all 4, the F252 quarantines in `tests/ui_contracts/`):
```
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252) ...
```
```
python3 -m apps.cli.main integrity check --json
```
Six checks, all `pass`, `fail_count` 0, `ok` true (`handler_import`, `live_review_verdict`,
`plan_consistency`, `relevant_untracked`, `repo_root_hygiene`, `high_blockers_open`).
```
python3 -m apps.cli.main integrity block .remedy-wt/f036-r7/block.md
All 7 checkable items pass.
REAL_EXIT=0
```
`git status --porcelain` empty, no untracked file.

The CSS diff of C3 (`6659b7df4`), quoted whole:
```diff
diff --git a/apps/ui/src/components/tour/TourOverlay.module.css b/apps/ui/src/components/tour/TourOverlay.module.css
index acc5d721a..b20da3ee6 100644
--- a/apps/ui/src/components/tour/TourOverlay.module.css
+++ b/apps/ui/src/components/tour/TourOverlay.module.css
@@ -43,6 +43,9 @@
   width: calc(var(--remedy-left-width) - 32px);
   max-height: 60vh;
 }
+/* The docked card is the left rail's width, too narrow for Previous, Next and "Show me" in
+   one row, so the row wraps instead of a label (R-1090). */
+.card[data-shown="true"] .actions { flex-wrap: wrap; }
 
 .header { display: flex; align-items: center; justify-content: space-between; }
 .header h2 {
@@ -102,6 +105,7 @@
   color: var(--remedy-blue-strong);
   font-size: 12px;
   font-weight: 600;
+  white-space: nowrap;
 }
 /* ux_spec.md §14: disabled is 45% opacity with the state carried in `disabled` itself, the same
    reading LessonsOverlay.module.css's own `.pager button:disabled` gives it. */
```

**G3 THE RENDER** — the draft run at C3 (`python3 .remedy-wt/f036-r7-worker/f036-r7-render_
measure.py /home/decodeux/Repos/remedy`) printed `RENDER: 11 of 11 checks pass`, `drive.mjs exit
code: 0`, and removed `.remedy-wt/f036-render-run`; that exact run's output is what C4 committed
as `f036-r7-render.txt`. After C4, run once more
(`python3 .agent/authored/f036-r7-render_measure.py /home/decodeux/Repos/remedy`), last three
lines:
```
server pid 424956 stopped (SIGTERM)
removed work dir: /home/decodeux/Repos/remedy/.remedy-wt/f036-render-run
drive.mjs exit code: 0
```
C-k's printed counts:
```
C-k before=[{"label":"Previous","lines":1,"inside":true},{"label":"Next","lines":1,"inside":true},{"label":"Show me","lines":1,"inside":true}] after=[{"label":"Previous","lines":1,"inside":true},{"label":"Next","lines":1,"inside":true},{"label":"Show me","lines":2,"inside":true}]
```
Screenshots: `.remedy-wt/f036-r7-worker/render-tour.png` (199290 bytes),
`.remedy-wt/f036-r7-worker/render-tour-shown.png` (369057 bytes). `git status --porcelain` empty.

**G4 THE RED PROOFS** — `git worktree add .remedy-wt/f036-r7-mut HEAD` (`f249b148f`) then
`python3 .agent/authored/f036-r7-mutations.py .remedy-wt/f036-r7-mut`, whole output:
```
control (start) CONTRACT: exit=0 failed=0 tests=[]
m1 the white-space: nowrap; line is removed: runner=CONTRACT exit=1 failed=1 tests=['tests/ui_contracts/test_tour_overlay_contract.py::test_an_action_label_stays_on_one_line_and_the_docked_row_wraps'] caught=True restored=True
m2 the .card[data-shown="true"] .actions rule line is removed: runner=CONTRACT exit=1 failed=1 tests=['tests/ui_contracts/test_tour_overlay_contract.py::test_an_action_label_stays_on_one_line_and_the_docked_row_wraps'] caught=True restored=True
control (end) CONTRACT: exit=0 failed=0 tests=[]
restored byte-identical: True (m1 the white-space: nowrap; line is removed (apps/ui/src/components/tour/TourOverlay.module.css))
restored byte-identical: True (m2 the .card[data-shown="true"] .actions rule line is removed (apps/ui/src/components/tour/TourOverlay.module.css))
PRIMARY checkout git status --porcelain:
(empty)
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
REAL_EXIT=0. No mutation stayed green; no extra test was needed. `git worktree remove
.remedy-wt/f036-r7-mut --force`, `git worktree prune`, `git worktree list | wc -l` = 61 (matches
step 4). `git status --porcelain` empty.

**G5 THE INTEGRATION GATE** —
```
npm --prefix apps/ui run build
✓ built in 2.15s
REAL_EXIT=0
```
`git status --porcelain` empty after it.
```
python3 -m pytest -n auto -q
20375 passed, 20 skipped, 1 warning in 198.59s (0:03:18)
REAL_EXIT=0
```
Bad node ids (failed plus errors): NONE. `tests/orchestration/test_import_reachability.py` and
`tests/test_no_orphan_modules.py` hold no bad node (the whole run's FAILED/ERROR list is empty, so
neither file contributed one) — closure precondition 7 holds. Transcript written to
`.agent/authored/f036-closure-suite.txt`; raw log at
`.remedy-wt/f036-r7-worker/full-suite.log`. Tree it ran on: `3b92631a2` (C6).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | deviated | split into two parts under constraint 2 — declared below |
| C5 | done | |
| C6 | done | |
| C7 | done | this handback |
| G1 | done | |
| G2 | done | |
| G3 | done | |
| G4 | done | every mutation caught first run; no extra test needed |
| G5 | done | full suite green, 20375 passed / 20 skipped, NONE bad |

## Authored-text proofs

`booking.diff` and `closure_docs.diff` were each applied via `git apply --check` (exit 0) then
`git apply` (exit 0) — never edited, never retyped. All three payloads (`booking.diff`,
`closure_docs.diff`, `plan.md`) were verified line count/byte count/sha256 against the PAYLOADS
table before use, and the committed `.agent/authored/f036-r7-*` copies read back byte-identical to
their sources via `git show` (G1, above). `.agent/plan.md` was REWRITTEN to the payload file by
`shutil.copyfile`, never hand-edited; its post-write bytes/sha256 equal the payload table's own row
and C2's resulting file hashes matched the reviewer's G1 table exactly for all three files (see
Verification, G1). The CSS repair, its test, the `drive.mjs` C-k check, and the mutation tool are
worker-authored against the block's specification, not transcribed from a payload; the other four
render files (`index.html`, `main.tsx`, `vite.config.mjs`, `measure.py`) are byte-copies of round
6's own committed files by `shutil.copyfile`, per S3's "byte-copies of round 6's" — verified by
re-reading each after the copy and by a direct byte-comparison script (all four MATCH).

## Deviations & assumptions

- **C4 split into two commits (constraint 2).** The block's single C4 — five render files plus
  `f036-r7-render.txt` — numstats to 808 insertions together, over the 500-line cap. Split into
  part 1/2 (the four byte-copies — `index.html`, `main.tsx`, `vite.config.mjs`, `measure.py`, 360
  insertions) and part 2/2 (`drive.mjs` and `f036-r7-render.txt`, 448 insertions), each its own
  subject with `(1/2)`/`(2/2)`, exactly as constraint 2 orders.
- **C-k's red control targets the actual DOM classes, not literal `.actions`/button selectors.**
  The block's S3 describes the red control as restoring round 6's rules via an injected `<style>`
  element; because `TourOverlay.module.css` is a CSS Module, the rendered classes are hashed at
  build time (e.g. `_actions_yfva1_48`), so the injected style reads those hashed classes off the
  live DOM (`actionsEl.className`, `card.className`) rather than the literal source-level class
  names `.actions`/`.card`, reproducing the identical selectors and specificity the real rules use
  (`<actionsClass> button` for the button rule, `<cardClass>[data-shown="true"] <actionsClass>`
  for the wrap rule, both `!important`, appended last so they win the cascade). Verified: the
  first attempt used the buttons' own `className` (empty — the buttons carry no class of their
  own, only `.actions button`'s descendant selector reaches them) and the red control's "after"
  measurement showed no wrapped label; switching to the actions/card classes reproduced the
  original defect exactly (`Show me` at `lines: 2` after the control), so C-k's before/after halves
  both hold for the real reason R-1090 describes, not by an unrelated accident.
- No other deviation. Every mutation in G4 was caught on the first (and only) official run; no
  additional test was needed. No red gate was hit against a payload or against committed code.
  The full suite ran exactly once, in C7, and nowhere else this round.

## Next

Per the block's `## Next` order: (1) Phase 1 rule 1 — read `.agent/STOP` from disk at session
start. (2) The review of round 7, including the repair of R-1090. (3) The closure's evidence
round — the booking of round 7 with R-1090's resolution, the self-use item, any repair the suite
requires, the evidence bundle and the review package. (4) The closing round. Open-findings count:
1 (R-1090, landed and awaiting review). Operator questions open: 1.

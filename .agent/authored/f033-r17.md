STEP T003b — F033 Hunk-level diff approval — ROUND 17 — SESSION 5

Goal: give the tasks-card row the partial apply truth, so a task whose changes
disagree stops reading "Done" on the surface an operator actually watches, and
book the round 16 verdict and its two prose slips in this round's first commits.

WHY THIS ROUND EXISTS. Finding R-0738 names THREE surfaces — the viewer badge,
the node glyph and the report line. Round 16 landed the first: `_task_truth_maps`
in `packages/orchestration/ui_server.py` now folds a task's changes by AGREEMENT
and emits a distinct `partial`, and
`apps/ui/src/components/detail/DetailPopover.tsx` labels it. This round lands the
SECOND. The report line is the NEXT round's and is not touched here, so R-0738
STAYS OPEN and no `Done:` line for it is written.

DECISION F033 D5 is authored below and lands in the ledger with the verdict. It
rules that the "node glyph" R-0738 names is the TASKS-CARD state tile, not a
widened `RemedyState`. Read RECORD17's second paragraph before writing any code:
it is the reasoning, and it is what a later reader will search for.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f033-r17.md`
  C0b  mirror the same bytes into `.agent/last_block.md`
  C1   `.agent/plan.md` <- PLAN17 (whole-file replacement)
  C2   `.agent/live_review.md` <- append RECORD17
  C3   `.agent/prose_slips.md` <- append SLIPS17
  C4   the tasks-card partial tile and status text (SPEC A and SPEC B)
  C5   the contract test that pins the new seam (SPEC C)
  C6   `.agent/handoff.md` <- the handback
  C7   `.agent/handoff.md` <- the PUSH OUTCOME, recorded after the push

C7 exists because it must, and this block names it rather than leaving the
worker to invent it. Round 16's worker had to add such a commit on its own
initiative and declared the deviation; that is one of the two slips SLIPS17
carries. The push outcome cannot exist before the push: run `git push` after C6,
then write the REAL outcome into `.agent/handoff.md` and commit it as C7. Never
commit a promise.

C1 is the FIRST substantive commit because this round touches the finding
ledger, and docs/agents/planner_reviewer_prompt.md section 3 checklist item 23
requires the plan to be advanced first when a round does.

Change set — exactly these paths, nothing else, in either direction:
  `.agent/authored/f033-r17.md`
  `.agent/last_block.md`
  `.agent/plan.md`
  `.agent/live_review.md`
  `.agent/prose_slips.md`
  `apps/ui/src/components/panels/TaskChecklistCard.tsx`
  `apps/ui/src/components/panels/RightLivePanel.module.css`
  `tests/ui_contracts/test_apply_state_partial.py`
  `.agent/handoff.md`

Constraints:
 1. Apply every authored slice BYTE FOR BYTE. If a slice is wrong, apply it as
    given and declare the disagreement in the handback. Never edit a slice.
 2. The authored slices are WHOLE TEXTS, not FROM/TO pairs. PLAN17 REPLACES
    `.agent/plan.md` entirely. RECORD17 and SLIPS17 are APPENDS: each target
    file ends in exactly one newline today, so the applied form is the old
    bytes, then ONE newline, then the slice. No pair in this block is FROM/TO,
    so no containment test and no FROM-zero count is owed anywhere in it.
 3. `packages/orchestration/ui_server.py` is NOT in the change set. The apply
    fold is finished and correct; this round CONSUMES it and changes nothing in
    it. G6 mutation (iii) edits it ONLY inside a disposable worktree.
 4. No new glyph, no new design token, no `assets_spec.md` amendment. The tile
    reuses the existing `TaskDoneGlyph` and the existing `--remedy-blue-strong`
    token. This is DECISION F033 D5's load-bearing claim; breaking it would need
    the feature file's ASSET REFERENCE banner to be excepted, and this round has
    no such exception.
 5. `RemedyState` in `apps/ui/src/api/types.ts` is NOT widened, and that file is
    not edited at all. `RemedyTaskItem.applyStatus` already exists and already
    carries the value: measured by the reviewer at `5f0273d8`,
    `selectChecklistRows` in `apps/ui/src/cockpitLogic.ts` slices the task array
    and copies no fields, so the card already receives it. No plumbing is
    needed, and none may be added.
 6. Destructive verification runs ONLY inside a disposable `git worktree`
    (docs/agents/self_drive_protocol.md G5). The primary checkout satisfies
    `git status --porcelain` empty at the handback.
 7. Every gate command is EXECUTED and its REAL exit code recorded. The word
    "green" is not a result.
 8. This round registers NO finding and resolves NONE. It writes no `Done:` and
    no `Landed:` line. The only growth of the record is RECORD17.

SPEC A — `apps/ui/src/components/panels/TaskChecklistCard.tsx`

Read the whole file first. It has two helpers that today take a bare `state`
string: `iconFor` and `stateText`. Both must instead take the ROW, so both can
read `applyStatus` beside the lifecycle state. Change their signatures, their
call sites inside the component, and nothing else in the file.

 A1. `iconFor` gains a FIRST branch, ahead of the `done` branch: when the task's
     `applyStatus` is exactly `"partial"`, return the blue filled check tile —
     the same `TaskDoneGlyph` the done branch renders, wrapped in a span whose
     class is a NEW `styles.checkPartial`. Ahead of `done` on purpose: a task
     may be finished AND only partly applied, and that is precisely the case
     R-0738 exists for, so the partial answer must win.
 A2. `stateText` gains the same first branch, returning a label DISTINCT from
     "Done", "In Progress", "Blocked" and "Planned". Use exactly
     `Partially applied`, which is the string
     `apps/ui/src/components/detail/DetailPopover.tsx` already returns for this
     value — one spelling per concept, per the Code Discoverability Conventions
     of AGENTS.md. Measured by the reviewer at `5f0273d8`: that exact string
     occurs 0 times in `TaskChecklistCard.tsx` today.
 A3. Above `iconFor`, one WHY comment naming finding R-0738 and citing
     `docs/ui/design_reference/ux_spec.md` section 11 item 4 as the rule the
     blue filled check tile comes from. Keep it short. Do NOT quote the string
     `Partially applied` inside it: SPEC C reads that label off comment-stripped
     source, so a comment quoting it would be stripped correctly, but the file
     is better off without the trap.
 A4. `outcomeHint` is NOT changed. The apply truth belongs in the tile and the
     status text, which is where `ux_spec.md` puts it; the hint is where an
     outcome summary goes, and the two must not compete for one line.

SPEC B — `apps/ui/src/components/panels/RightLivePanel.module.css`

Add ONE rule, `.checkPartial`, directly beneath the existing `.checkDone svg`
line. It is `.checkDone` with a blue fill: same 16px box, same 5px radius, same
grid centring, same white glyph colour, `background: var(--remedy-blue-strong)`.
Add the matching `.checkPartial svg { width: 10px; height: 10px; }` beside it,
because the glyph inside is the same one. No other rule in the file changes, and
no raw hex colour is introduced — measured by the reviewer at `5f0273d8`, the
token `--remedy-blue-strong` already occurs 19 times in this file.

SPEC C — `tests/ui_contracts/test_apply_state_partial.py`

This file already pins the fold against the POPOVER. EXTEND it — do not replace
it, and do not weaken anything already in it — so it pins the fold against the
CARD as well. Add a paragraph to the module docstring naming the card, so the
docstring stays true.

 C1. Add a `CARD` path constant for
     `apps/ui/src/components/panels/TaskChecklistCard.tsx`, beside `POPOVER`.
 C2. Reuse `strip_ts_comments` and the `helper_body` brace-walker. `helper_body`
     is written against one fixed helper name; generalise it to take the
     function name as an argument and update the popover call sites so their
     behaviour is unchanged. This is the ONLY edit permitted to existing test
     code in this file.
 C3. A new class asserting the CARD readers are not vacuous, in the shape this
     file already uses: the card really loses text to the stripper; the scoper
     for each card helper returns strictly less than the whole module and does
     not reach the neighbouring helper.
 C4. A new class asserting the seam. Derive the emitted set with the EXISTING
     `fold_apply_labels()`, which walks the shipped fold's AST — do NOT restate
     the labels. Then assert: the card's `stateText` returns a label for
     `partial`; that label is distinct from every other label `stateText` can
     return; and the card's `iconFor` has a branch on `partial` returning a tile
     class distinct from the one the `done` branch returns. Read every one of
     these off COMMENT-STRIPPED source.
 C5. One assertion tying the two components together: the label the CARD returns
     for `partial` and the label the POPOVER returns for `partial` are the SAME
     string. That is one-spelling-per-concept made mechanical, and it is what
     stops the two surfaces drifting apart in a later round.
 C6. Do not assert a COUNT of tests, of branches, or of labels anywhere in the
     new text.

Done when — G1 through G8, the maximum operator amendment amend0827-process-diet
rule 5 allows. Run every one of them. Report ONE LINE PER GATE in the handback,
each carrying the command's REAL exit code and the numbers it printed. Every
gate below runs at a commit STRICTLY EARLIER than C6, which is what lets the
handback quote it; C6's and C7's own structural numbers are measured by the
REVIEWER at the next gate and belong in no gate here.

 G1 HYGIENE AND THE STOP FILE. Before C0a, confirm `.agent/STOP` does not exist
    and report the exact message the check printed. Run `git status --porcelain`
    before C0a and again after C5; both must print nothing.

 G2 TRANSPORT. For each slice below, extract its applied region from its target
    file and compare that region's sha256 to the digest in that slice's own
    BEGIN marker. These are the reviewer's measurements of the slices it ships:
      PLAN17   2660 bytes  0171904031cd5176d01880c956399dfc22cea4d33a18960d3590641dac566c0a
      RECORD17 6982 bytes  31cbb3f3a1270180fafceead40b63aa90d41ad231ac698c43c149a072419e30c
      SLIPS17   959 bytes  a0a8aefa37aa93283d920b8e8ab6e27bdd5c9cdfbf374b3459b6fe52b401d429
    For PLAN17 the region is the WHOLE file. For the two appends it is the LAST
    N bytes, N being that slice's byte length above. Report one digest and one
    verdict per slice. This proves the saved copy, its mirror and the working
    copy agree; it is NOT a claim about the bytes that were emitted, and the
    handback says so in those words.

 G3 THE RECORD APPEND at C2 — full byte forensics, because `.agent/live_review.md`
    is the record. Three readings, all required:
    (a) BYTES. The pre-commit blob is 1542724 bytes and must be a byte PREFIX of
        the post-commit file; the post-commit file must be exactly 1549707 bytes
        (1542724 + 1 + 6982); RECORD17 must be an exact SUFFIX of it.
    (b) STRUCTURE, an independent reader. Split the post-commit file on blank
        lines, COUNT the slice's paragraphs into N — your script counts N, this
        block does not assert it — and require the LAST N blank-line units to
        equal the slice's N paragraphs IN ORDER.
    (c) NEGATIVE CONTROL. Flip one byte at offset 1544671 of the post-commit
        file. That offset lies inside the FIRST appended paragraph, which spans
        1542725 to 1546617; ASSERT that containment in the script before
        flipping, so the control is proved to sit where it must. BOTH readings
        (a) and (b) must REJECT the flipped copy. Flip in memory or on a copy;
        never write it to the tracked file.

 G4 THE LEDGER after C2. Report every count as a before and an after:
      `^- R-\d+ — `        306, UNMOVED  (this round registers nothing)
      `^Done: R-\d+ — `    50 lines over 48 distinct, UNMOVED
      `^Landed: R-\d+ — `  17, UNMOVED
      `^Gate: F033 R16 — ` 0 before, exactly 1 after
      distinct `DECISION F033 D<n>` ids: 4 before, 5 after, the ADDED one D5
      the open set, registered minus resolved: 258, UNMOVED
      `^- R-0738 — ` still exactly 1, with NO `^Done: R-0738 — ` line

 G5 THE PROSE FILES. `.agent/plan.md` after C1 is byte-EQUAL to PLAN17 at 2660
    bytes over 47 lines — under the 50-line cap AGENTS.md sets — and still holds
    `## Goal` and `## Next Steps`, which the four state readers require.
    `.agent/prose_slips.md` after C3 is exactly 25942 bytes (24982 + 1 + 959),
    the old bytes a PREFIX and SLIPS17 an exact SUFFIX.

 G6 THE MUTATIONS, at the commit C5 creates, inside a disposable `git worktree`,
    restoring every mutated file byte-identically afterwards and PROVING the
    restoration. Report the UNMUTATED CONTROL first, with its real exit code and
    counts: a colour with no baseline is not evidence. Before each mutation,
    assert its anchor occurs EXACTLY ONCE in the file named, and report that
    count.
    (i)   In `apps/ui/src/components/panels/TaskChecklistCard.tsx`, delete the
          `iconFor` branch returning the `styles.checkPartial` tile. Anchor:
          `styles.checkPartial`. The card TILE assertions of SPEC C go RED.
    (ii)  In the same file, delete the `stateText` branch returning
          `Partially applied`. Anchor: `Partially applied`. The card LABEL
          assertions and the cross-component assertion C5 go RED.
    (iii) In `packages/orchestration/ui_server.py`, replace
          `apply_by_task[tid] = "partial"` with `apply_by_task[tid] = "applied"`.
          The card SEAM assertions go RED — which is what proves SPEC C derives
          the emitted set from the shipped fold's AST rather than restating it.
          The reviewer ran exactly this mutation at `5f0273d8` in its own
          disposable worktree, having first asserted the anchor unique: the
          unmutated control was 13 passed at REAL exit 0, and the mutated run
          exit 1 at 2 failed. Your run adds the card's own failures to those, so
          expect MORE than 2; report the number you measured.

 G7 THE SUITES, run SERIALLY in the PRIMARY checkout at the commit C5 creates,
    each with its real exit code. The reviewer measured every base reading below
    at `5f0273d8`, so a number that moves is a result rather than a surprise:
      `python3 -m pytest tests/ui_contracts/test_apply_state_partial.py -q`
          base 13 passed; after this round it MUST be higher — report it
      `python3 -m pytest tests/ui_contracts/ -q`   base 677 passed, 4 skipped
      `python3 -m pytest tests/ui_server/test_dashboard_contract.py -q`
          base 74 passed
      `python3 -m pytest tests/regression/test_named_bugs.py -q`
          base 64 passed, 6 skipped
      `python3 -m pytest tests/cli/test_golden_path.py -q`
          base 42 passed — the canary every handback runs
      `ruff check tests/ui_contracts/test_apply_state_partial.py`  must exit 0

 G8 THE STRUCTURE over `5f0273d8`..C5. Every commit single-parent. Report each
    commit's insertion count — the `+` column of `git diff --numstat`, which is
    what AGENTS.md DECISION F104 D1 caps at 500 — and confirm each is under 500.
    The path set over that range must EQUAL the change set above MINUS
    `.agent/handoff.md`, in BOTH directions: the handback is written at C6 and
    C7, which this range deliberately does not reach, and that is the whole of
    the difference. Read each path below at `5f0273d8` and at C5 with
    `git rev-parse <commit>:<path>` — a read that writes nothing — and require
    the two blob ids EQUAL:
      `packages/orchestration/ui_server.py`
      `packages/orchestration/run_report.py`
      `packages/orchestration/diff_parser.py`
      `packages/orchestration/hunk_identity.py`
      `packages/orchestration/hunk_apply.py`
      `packages/orchestration/source_apply.py`
      `packages/orchestration/diff_repair.py`
      `apps/cli/commands/patch.py`
      `apps/ui/src/api/types.ts`
      `apps/ui/src/api/remedyApi.ts`
      `apps/ui/src/cockpitLogic.ts`
      `apps/ui/src/components/detail/DetailPopover.tsx`
      `apps/ui/src/components/timeline/PhaseTimeline.tsx`
      `docs/roadmap/STATUS.md`
      `docs/roadmap/ROADMAP.md`
      `docs/ui/design_reference/assets_spec.md`

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It
carries the SESSION NUMBER 5, the round number 17, the Fortschritt line, the
changed-files table, ONE LINE PER GATE with real exit codes, the open-findings
count, every deviation with its reason, and the next expected action. It has NO
length cap. The `## Commits` table the template mandates takes its `+/-` cells
from the SAME `git diff --numstat` run G8 reports — compare them cell by cell
and say you did; never fill that column from a file's line counts, which is how
a full-file rewrite makes the table and the gate disagree. Then push, then
record the real push outcome in C7.

The authored slices follow. Each marker line opens with three '<' and closes
with three '>'. A slice begins on the line after its BEGIN marker and ends on
the line before its END marker; the marker lines are never part of the slice.

<<<BEGIN PLAN17 target=.agent/plan.md mode=replace bytes=2660 sha256=0171904031cd5176d01880c956399dfc22cea4d33a18960d3590641dac566c0a>>>
# Plan — F033 Hunk-level diff approval

Branch: feature/f033-hunk-approval-v2, cut from `main` at `bd8d9529`, the merge
commit of pull request 221. SESSION 5 of this feature.

## Goal
Surgical consent over changes: hunks carry STABLE content-hash ids, an
`approve_hunks` command applies the approved set to the branch all-or-nothing,
and rejected hunks become precise repair feedback quoted verbatim in the next
round — every partial state rendered truthfully in viewer, node and report.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| T001 stable ids, viewer v2, consolidation | done | round 5 |
| decision core · subset diff · all-or-nothing apply | done | rounds 6, 7, 8 |
| failed-rollback truth · ledger · the door's effect | done | rounds 9-11, D4 |
| the recorder takes the viewer's envelope | done | round 12 |
| one evidence-directory resolver for viewer and doors | done | round 13 |
| the CLI command and its handler | done | rounds 14, 15 |
| the write door's exposure and dispatch | done | round 15 |
| T003 the apply fold's partial truth, and the popover label | done | round 16 |
| T003 the task row's partial tile and status text | open | this round, R-0738 |
| T003 the report line | open | next |
| T003 rejection reasons quoted into the repair prompt | open | after that |
| R-0745, the door's transitive import closure | open | with the next door work |
| the operator docs for `patch approve-hunks` | open | closure sequence |

## Next Steps
1. R-0738's second surface: `apps/ui/src/components/panels/TaskChecklistCard.tsx`
   reads `applyStatus` beside the lifecycle state, so a partially applied task
   shows the blue filled check tile and a distinct status text instead of
   reading "Done". DECISION F033 D5 rules this the task node's partial
   treatment and `RemedyState` is NOT widened. R-0738 STAYS OPEN: one of the
   three surfaces its resolution names is still untouched.
2. Then the report line. `packages/orchestration/run_report.py` holds no apply
   state at all, so its `TaskOutcome` gains one and the fold moves to a home
   both readers may import. Only after that is R-0738 resolvable.
3. Then rejection reasons quoted VERBATIM into the next repair prompt, with the
   trace proof `docs/roadmap/features/T5_F033.md` calls acceptance material.
4. Then the closure sequence, which owes `docs/` an operator-facing description
   of `remedy patch approve-hunks` — no round has been allowed a `docs/` path yet.

## Risks
- The apply fold has one consumer but three downstream surfaces; a value added on
  one side only renders as "Unknown", which is why the contract test pins both ends.
<<<END PLAN17>>>

<<<BEGIN RECORD17 target=.agent/live_review.md mode=append bytes=6982 sha256=31cbb3f3a1270180fafceead40b63aa90d41ad231ac698c43c149a072419e30c>>>
Gate: F033 R16 — THE PARTIAL APPLY STATE BECOMES TELLABLE. THE ROUND PASSED. This entry books, under operator amendment amend0827 rule 1, the verdict the reviewer committed and pushed in `.agent/handoff.md` at `5f0273d8`; it is written by the first substantive commit of round 17 and buys no round of its own. All eight gates were re-executed by the reviewer at `c7dc3cc0` and every ordered reading reproduced. TRANSPORT: the C0a blob is 30868 bytes at sha256 `8fcdfcd2…df874d`, EQUAL to the reviewer's own scratchpad original, with ONE blob id at C0b — a chain walking the saved copy, its mirror and the working copy, which is what this workflow can measure and is not a claim about the emitted bytes. THE RECORD APPEND at `807f6f25` reconstructs 1535259 plus one newline plus 7464 to 1542724, the committed blob exactly, base a byte PREFIX, N COUNTED at 3, the last three blank-line units equal to the slice's paragraphs IN ORDER, and a negative control at byte 1537103 — proved to lie inside the FIRST appended paragraph, spanning 1535260 to 1538947 — rejected by BOTH readers. THE LEDGER: registered 305 to 306 with the ADDED id exactly `R-0745`; `Done:` 49 lines over 47 distinct to 50 over 48 with the ADDED resolved id exactly `R-0744` and the `Landed: R-0744` line still standing beside its new `Done:` paragraph; `Landed:` 17 UNMOVED, that round writing none; `^Gate: F033 R15 — ` exactly 1; four distinct `DECISION F033 D` ids UNMOVED; the open set 258 at both ends of the round; and `- R-0738` still registered with no `Done:` line, which is correct — that round ADVANCED the finding and did not resolve it. THE PROSE FILES: `.agent/plan.md` byte-EQUAL to its slice at 2453 bytes over 44 lines, under the 50-line cap; `.agent/prose_slips.md` reconstructs 24266 plus one newline plus 715 to 24982. THE FOLD: the shipped apply fold agrees or says `partial`, and the reviewer traced every branch by hand, including the two the SPEC did not name — a task whose every change carries the `getattr` default reads `not_applied` exactly as before, and a task mixing `reverted` with that default now reads `partial` where the old membership test said `reverted`, which is the same defect and the same repair. The PROOF fold three lines above it is byte-identical. THE MUTATIONS were re-run by the reviewer in its own disposable worktree at `c924eb41` with its OWN anchors, each asserted UNIQUE, the import proved to resolve inside the worktree and every file restored byte-identically: controls 39 and 13 at REAL exit 0; restoring the membership test is exit 1 at 4 failed; making the mixed arm return `applied` is exit 1 at 5 failed; and deleting the TSX `partial` branch is exit 1 at 4 failed, which proves the PYTHON contract test really reads the TypeScript, with no vitest anywhere. THE REVIEWER ALSO RAN A MUTATION THE BLOCK NEVER ORDERED, to test the contract test's own headline claim rather than take it on trust: adding a FIFTH backend label the popover cannot render reddens `test_the_two_sets_agree_in_both_directions`, so the seam guard really is derived from the fold's AST and not restated. THE SUITES were re-run SERIALLY in the primary checkout, every REAL exit 0: the cockpit 39, the new contract 13, `tests/ui_contracts/` 677 passed and 4 skipped, `test_command_channel.py` 106, `test_patch_cmd.py` 13 and the canary 42, with `ruff` exiting 0. THE STRUCTURE: seven single-parent commits over the range ending at C5, of 400, 272, 17, 6, 2, 21 and 396 insertions, every one under 500; the path set EQUALS the declared change set in BOTH directions; and the do-not-touch paths byte-identical by blob id. SIX DEVIATIONS were declared and all six are honest; two of them are defects in the reviewer's own block and are recorded in `.agent/prose_slips.md` as that round's two slips, with no id and no round of their own, under operator amendment amend0827 rule 2.

DECISION F033 D5 — THE TASK NODE'S PARTIAL TREATMENT IS THE TASKS-CARD STATE TILE, AND `RemedyState` IS NOT WIDENED. Raised by the reviewer while planning round 17 under docs/agents/planner_reviewer_prompt.md §4 item 7, because the round-16 handback committed at `5f0273d8` measured a different route for this surface and a silent re-plan is forbidden. CONTEXT, measured by the reviewer at `5f0273d8`: finding R-0738 names three surfaces and the second of them is "the node glyph"; `docs/roadmap/features/T5_F033.md`'s Design says "the task node shows the partial glyph treatment per reference"; and the graph node's state is `RemedyState` in `apps/ui/src/api/types.ts`, a CLOSED union of `done`, `current`, `pending`, `blocked` and `suggested` with no partial member, read by `RemedyJourneyItem`, `RemedyTaskItem`, `RemedyGraphNode`, `RemedyGraphEdge`, `RemedyPhase` and by `apps/ui/src/components/timeline/PhaseTimeline.tsx`, so widening it hands a value to five readers that have no meaning for it. CHOSEN: the partial treatment lands on the TASKS-card row in `apps/ui/src/components/panels/TaskChecklistCard.tsx` — a row that already RECEIVES `RemedyTaskItem.applyStatus` at `5f0273d8`, because `selectChecklistRows` in `apps/ui/src/cockpitLogic.ts` slices the task array and copies no fields — and the round that this decision governs makes that row read the value beside the lifecycle state, as `apps/ui/src/components/detail/DetailPopover.tsx` already does at `5f0273d8`, rendering the blue filled check tile and a distinct status text, which is what `docs/ui/design_reference/ux_spec.md` section 11 item 4 binds: "done=green filled check tile, in_progress=blue filled check tile only when partially applied else doc glyph". THAT CLAUSE IS THE ONLY PARTIAL-APPLY TREATMENT THE CANONICAL DESIGN REFERENCE SPECIFIES — measured by the reviewer at `5f0273d8` by reading every case-insensitive occurrence of "partial" under `docs/ui/design_reference/`, of which `graph_spec.md` and `assets_spec.md` hold none — so the tile needs no new glyph, no new token and no `assets_spec.md` amendment, and this feature file's ASSET REFERENCE banner is satisfied rather than excepted. The row is the node's own affordance in any case: its click handler calls `onSelectNode(row.nodeId)`. ALTERNATIVES CONSIDERED: (a) widen `RemedyState` with a `partial` member — rejected because apply state and lifecycle state are different axes, so a union carrying both makes every reader answer a question it was not asked, and because a graph glyph for it is a treatment `assets_spec.md` does not specify and would have to be amended for; (b) add `applyStatus` to `RemedyGraphNode` and paint the canvas node — rejected as larger than the reference asks for and freely deferrable, since nothing about the tile prevents a later round from adding it. HOW TO REVERSE: any later relay may order (a) or (b); this decision binds the surface round 17 builds and no round after it. R-0738 STAYS OPEN either way — the third surface its resolution names, the report line, is untouched by this decision.
<<<END RECORD17>>>

<<<BEGIN SLIPS17 target=.agent/prose_slips.md mode=append bytes=959 sha256=a0a8aefa37aa93283d920b8e8ab6e27bdd5c9cdfbf374b3459b6fe52b401d429>>>
2026-08-29 · F033 R16 · The block's `ui_server.py` SPEC ordered the fold's WHY comment to QUOTE the membership test `if "applied" in apply_states` while its contract-test SPEC ordered an assertion that no membership test remains, so a text search would have been answered by the reviewer's own ordered comment — pre-emission checklist item 2's shape reaching a TEST rather than a done-when; the worker resolved it with an AST predicate that is strictly stronger, declared the disagreement, and the reviewer's mutation confirms the predicate discriminates.

2026-08-29 · F033 R16 · The block's bundle ended at C6, the handback commit, and said nothing about where the PUSH outcome is recorded, so the worker added a C7 to carry the real outcome instead of committing a promise; nothing on disk is wrong and the change set was not exceeded, and a future block should name the commit the push outcome lands in rather than leaving the worker to invent one.
<<<END SLIPS17>>>

STEP T003c — F033 Hunk-level diff approval — ROUND 18 — SESSION 5

Goal: give the apply fold a home both readers may import and the APPLIED/TOTAL
counts R-0738's fix asks for, without changing a single answer the cockpit gives
today; and book the round 17 verdict and its two prose slips in the first
commits.

WHY THIS ROUND EXISTS. R-0738's third surface is the report line, and
`packages/orchestration/run_report.py` cannot reach the fold today: the fold's
body sits inside `_task_truth_maps` in `packages/orchestration/ui_server.py`, a
private function in the HTTP server module. A report that imported the HTTP
server to learn a task's apply state would be the wrong dependency in the wrong
direction. So this round MOVES the decision logic to
`packages/orchestration/proof_chain.py` — the module that DEFINES `ProofChange`
and its `apply_state` field, and whose module-level imports are only
`dataclasses`, `datetime`, `pathlib`, `typing` and `packages.core.models`,
measured by the reviewer at `2a938b5e` — and gives it the counts. The report
line itself is the NEXT round. R-0738 STAYS OPEN and no `Done:` line is written.

THE TRAP THIS ROUND IS BUILT AROUND, and the reason the move and a test edit
must land together. `tests/ui_contracts/test_apply_state_partial.py` learns the
fold's four labels by WALKING THE AST of the function named in its own
`FOLD_FUNCTION` constant, inside the file named in its `SERVER` constant, and
collecting every string literal assigned to its `FOLD_MAP` subscript. Move the
literals to another file and that walk finds NOTHING. Its
`test_the_ast_derivation_finds_labels_at_all` would then fail — loudly, which is
the good case — while every seam assertion beneath it would have been measuring
the popover and the card against an EMPTY expected set. The guard must follow
the code in the same round, and SPEC C is that move.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f033-r18.md`
  C0b  mirror the same bytes into `.agent/last_block.md`
  C1   `.agent/plan.md` <- PLAN18 (whole-file replacement)
  C2   `.agent/live_review.md` <- append RECORD18
  C3   `.agent/prose_slips.md` <- append SLIPS18
  C4   the fold's new home and its counts (SPEC A), and the delegation (SPEC B)
  C5   the fold's own unit tests (SPEC D)
  C6   the re-pointed seam guard (SPEC C)
  C7   `.agent/handoff.md` <- the handback
  C8   `.agent/handoff.md` <- the PUSH OUTCOME, recorded after the push

WHERE THE PUSHES GO, stated in full because round 17 spent a declared deviation
discovering that this block's predecessor left it open. Push after C7. Then
write the REAL outcome of that push into `.agent/handoff.md` and commit it as
C8. Then push AGAIN, so C8 itself reaches the remote. That LAST push is the
round's final action and is recorded in NO commit, deliberately: a commit
recording it would need a commit recording that one. The regress is cut here,
and the REVIEWER verifies the final pushed state itself with `git rev-parse`
against the remote. Do not write a sentence predicting what a later push will
do; C7 and C8 describe only what has already happened.

C1 is the FIRST substantive commit because this round touches the finding
ledger, per docs/agents/planner_reviewer_prompt.md section 3 checklist item 23.

Change set — exactly these paths, nothing else, in either direction:
  `.agent/authored/f033-r18.md`
  `.agent/last_block.md`
  `.agent/plan.md`
  `.agent/live_review.md`
  `.agent/prose_slips.md`
  `packages/orchestration/proof_chain.py`
  `packages/orchestration/ui_server.py`
  `tests/orchestration/test_proof_chain.py`
  `tests/ui_contracts/test_apply_state_partial.py`
  `.agent/handoff.md`

Constraints:
 1. Apply every authored slice BYTE FOR BYTE. If a slice is wrong, apply it as
    given and declare the disagreement. Never edit a slice.
 2. The authored slices are WHOLE TEXTS, not FROM/TO pairs. PLAN18 REPLACES
    `.agent/plan.md`. RECORD18 and SLIPS18 are APPENDS: each target ends in
    exactly one newline today, so the applied form is the old bytes, then ONE
    newline, then the slice. No pair here is FROM/TO, so no containment test and
    no FROM-zero count is owed anywhere in this block.
 3. NO ANSWER CHANGES THIS ROUND. For every input, the label
    `_task_truth_maps` returns must be exactly what it returns at `2a938b5e`.
    This is a move plus an addition, never a re-decision. The counts are NEW
    information beside the label, not a new label.
 4. `tests/ui_server/test_dashboard_cockpit_truth.py` is NOT in the change set
    and must not be edited. It imports `_task_truth_maps` from
    `packages.orchestration.ui_server` and asserts its answers directly;
    leaving it untouched and GREEN is this round's proof that the delegation
    preserved the contract. If you believe it must change, stop and declare it
    rather than editing it.
 5. `packages/orchestration/run_report.py` is NOT touched. The report line is
    the next round; landing half of it here would leave a mechanism no test
    reaches.
 6. Destructive verification runs ONLY inside a disposable `git worktree`
    (docs/agents/self_drive_protocol.md G5). The primary checkout satisfies
    `git status --porcelain` empty at the handback.
 7. Every gate command is EXECUTED and its REAL exit code recorded. The word
    "green" is not a result.
 8. This round registers NO finding and resolves NONE. No `Done:` line, no
    `Landed:` line. The only growth of the record is RECORD18.
 9. The bare `ruff` executable is denied to this session's shell; round 17
    measured that. Run `python3 -m ruff check ...`, which is the same tool with
    the repository's own configuration, and say which form you used.

SPEC A — `packages/orchestration/proof_chain.py`

Read the file first, at least `ProofChange`, `ProofChain` and the module's
imports. Add, near the other truth rules and BELOW the dataclasses:

 A1. A frozen dataclass — name it `TaskApplyState` — carrying three fields: the
     `state` string, the `applied` count and the `total` count. Give it the
     one-line WHY comment the Code Discoverability Conventions of AGENTS.md ask
     for, directly above the definition.
 A2. A public function `fold_task_apply_states(chain)` returning
     `dict[str, TaskApplyState]`, keyed by the FULL task id. It groups
     `chain.changes` by `task_id`, skipping changes whose task id is empty,
     exactly as `_task_truth_maps` does today, and folds each group by
     AGREEMENT with the SAME four answers and in the SAME order the shipped
     fold uses at `2a938b5e`: all `applied` -> `applied`; else all `reverted` ->
     `reverted`; else none of them in `("applied", "reverted")` -> `not_applied`;
     else `partial`. Read each change's state with
     `getattr(c, "apply_state", "")`, so a change with no such attribute keeps
     behaving exactly as it does now.
 A3. `applied` is the number of changes in that task's group whose state is
     `applied`; `total` is the size of the group. These are the numbers R-0738's
     fix calls "the count of applied changes against the total available", and
     the report line consumes them next round.
 A4. `chain` may be None: return an empty dict, as the shipped fold does.
     Guard the same exception classes the shipped fold guards
     (`ImportError`, `AttributeError`, `TypeError`) and return an empty dict on
     any of them, so a malformed chain degrades exactly as it does today.
 A5. Carry the WHY comment that currently sits above the apply fold in
     `ui_server.py` — the paragraph naming finding R-0738 and the membership
     test it replaced — over to the new function, adapting only what the move
     makes untrue. That comment is why the fold looks the way it does, and it
     must not be left behind in a file that no longer holds the fold.

SPEC B — `packages/orchestration/ui_server.py`

 B1. `_task_truth_maps` KEEPS its name, its signature, its docstring's promise
     and its return type `tuple[dict[str, str], dict[str, str]]`. Its PROOF half
     is untouched, byte for byte.
 B2. Its APPLY half becomes a delegation: call
     `fold_task_apply_states` and map each entry to its `state` string. Import it
     inside the function, beside the existing local import of the proof
     constants — the module's import surface is guarded elsewhere and this round
     does not widen it.
 B3. Delete the apply fold's decision logic from this file. After this commit
     the four apply labels are literals in `proof_chain.py` and in no other
     production module — SPEC C's guard depends on exactly that.

SPEC C — `tests/ui_contracts/test_apply_state_partial.py`

Re-point the AST reader at the fold's new home, changing NOTHING else about what
this file asserts. Every existing assertion must still run and still mean what
it meant.

 C1. Point the constant that names the searched FILE at
     `packages/orchestration/proof_chain.py`, and the constant that names the
     searched FUNCTION at `fold_task_apply_states`. If the subscript name the
     walk collects from also changes, change it with them.
 C2. `fold_apply_labels()` must return the same four strings after this round as
     before it. `test_the_ast_derivation_finds_labels_at_all` is the guard that
     this re-pointing worked at all; keep it and let it do its job.
 C3. The membership-test reader is written against the local list name the old
     fold used. Keep an equivalent AST predicate over whatever the new fold
     names that list, so the "no longer answers by membership" assertion still
     discriminates rather than passing vacuously on a name that no longer exists.
 C4. Update the module docstring where it names `ui_server.py` as the fold's
     home, so the file's own prose stays true.
 C5. Do not weaken, delete or skip any existing assertion, and do not assert a
     COUNT of tests, branches or labels anywhere.

SPEC D — `tests/orchestration/test_proof_chain.py`

The fold has never had a direct unit test: today it is reachable only through
the cockpit. Add a class that tests it AS A FUNCTION.

 D1. Build `ProofChange` values directly and assert all four states from
     explicit inputs: every change applied; every change reverted; none applied
     or reverted; and a MIXED group. Build the mixed case explicitly, which is
     what R-0738's resolution clause asks for — never observe whatever a fixture
     happens to produce.
 D2. Assert the COUNTS on each of those cases, including that `total` is the
     group size and `applied` counts only the applied changes. Cover a mixed
     group where the two numbers differ, since equal numbers would let a fold
     that returned the same value twice pass.
 D3. Assert the None chain gives an empty dict, that a change with an empty task
     id is skipped, and that two tasks in one chain are folded independently.
 D4. Do not assert a COUNT of tests anywhere.

Done when — G1 through G8, the maximum operator amendment amend0827-process-diet
rule 5 allows. Run every one. Report ONE LINE PER GATE in the handback with the
command's REAL exit code and the numbers it printed. Every gate runs at a commit
STRICTLY EARLIER than C7, which is what lets the handback quote it.

 G1 HYGIENE AND THE STOP FILE. Before C0a, confirm `.agent/STOP` does not exist
    and report the exact message printed. Run `git status --porcelain` before
    C0a and again after C6; both must print nothing.

 G2 TRANSPORT. For each slice below, extract its applied region from its target
    and compare that region's sha256 to the digest in that slice's BEGIN marker:
      PLAN18   2765 bytes  5214755bf41d758a22903a62b8d60b6df4c2ab4af7929f2c6d7779ad0b6a273a
      RECORD18 5764 bytes  40df3d80c337ebf480b5638f14b8adb861d31df74436c6a067d1c7b047cb48bf
      SLIPS18  1049 bytes  6372f2bbee6a23f437a09c342aa515ca7d81903e11b7da6311410826b77e4956
    For PLAN18 the region is the WHOLE file; for the appends it is the LAST N
    bytes, N being that slice's byte length above. Report one digest and one
    verdict per slice. This proves the saved copy, its mirror and the working
    copy agree; it is not a claim about the emitted bytes, and the handback says
    so in those words.

 G3 THE RECORD APPEND at C2 — full byte forensics, `.agent/live_review.md` being
    the record. Three readings, all required:
    (a) BYTES. The pre-commit blob is 1549707 bytes and must be a byte PREFIX of
        the post-commit file; the post-commit file must be exactly 1555472 bytes
        (1549707 + 1 + 5764); RECORD18 must be an exact SUFFIX of it.
    (b) STRUCTURE, an independent reader. Split the post-commit file on blank
        lines, COUNT the slice's paragraphs into N — your script counts N, this
        block does not assert it — and require the LAST N blank-line units to
        equal the slice's N paragraphs IN ORDER.
    (c) NEGATIVE CONTROL. Flip one byte at offset 1552589 of the post-commit
        file. That offset lies inside the FIRST appended paragraph, which spans
        1549708 to 1555470; ASSERT that containment before flipping. Run readers
        (a) and (b) INDEPENDENTLY and require EACH to reject the flipped copy
        and to accept the unflipped one — a reader that rejects everything
        proves nothing. Flip in memory or on a copy, never on the tracked file.

 G4 THE LEDGER after C2, every count as a before and an after:
      `^- R-\d+ — `        306, UNMOVED  (this round registers nothing)
      `^Done: R-\d+ — `    50 lines over 48 distinct, UNMOVED
      `^Landed: R-\d+ — `  17, UNMOVED
      `^Gate: F033 R17 — ` 0 before, exactly 1 after
      distinct `DECISION F033 D<n>` ids: 5, UNMOVED — this round rules none
      the open set, registered minus resolved: 258, UNMOVED
      `^- R-0738 — ` still exactly 1, with NO `^Done: R-0738 — ` line

 G5 THE PROSE FILES. `.agent/plan.md` after C1 is byte-EQUAL to PLAN18 at 2765
    bytes over 49 lines — under the 50-line cap AGENTS.md sets — and still holds
    `## Goal` and `## Next Steps`. `.agent/prose_slips.md` after C3 is exactly
    26992 bytes (25942 + 1 + 1049), old bytes a PREFIX, SLIPS18 an exact SUFFIX.

 G6 THE MUTATIONS, at the commit C6 creates, inside a disposable `git worktree`,
    restoring every mutated file byte-identically and PROVING it against the
    committed blob. Report the UNMUTATED CONTROL first with its real exit code
    and counts. Before each mutation assert its anchor occurs EXACTLY ONCE in
    the file named, and report that count. Run all three suites named in G7's
    first three lines for each mutation, because these mutations are meant to
    reach different files:
    (i)   In `packages/orchestration/proof_chain.py`, change the fold's
          `partial` answer to `applied`. The seam assertions in
          `tests/ui_contracts/test_apply_state_partial.py` AND the mixed-case
          unit test in `tests/orchestration/test_proof_chain.py` must go RED.
          This is the single most important reading of the round: it proves the
          re-pointed guard reads the fold's REAL new home.
    (ii)  In the same file, make the fold report `total` where it should report
          `applied`. The COUNT assertions of SPEC D must go RED. If they do not,
          the counts are pinned by nothing and say so plainly.
    (iii) In `packages/orchestration/ui_server.py`, make `_task_truth_maps`
          return an empty apply map instead of the delegated one.
          `tests/ui_server/test_dashboard_cockpit_truth.py` — which this round
          does NOT edit — must go RED. That is the proof the adapter is still
          wired to the cockpit.

 G7 THE SUITES, SERIALLY, in the PRIMARY checkout at the commit C6 creates, each
    with its real exit code. Base readings measured by the reviewer at
    `2a938b5e`, so a number that moves is a result rather than a surprise:
      `python3 -m pytest tests/orchestration/test_proof_chain.py -q`
          base 90 passed; MUST be higher after SPEC D — report it
      `python3 -m pytest tests/ui_contracts/test_apply_state_partial.py -q`
          base 20 passed; SPEC C adds no test, so 20 is the expected reading
      `python3 -m pytest tests/ui_server/test_dashboard_cockpit_truth.py -q`
          base 39 passed; this file is not edited, so 39 is expected
      `python3 -m pytest tests/ui_contracts/ -q`  base 684 passed, 4 skipped
      `python3 -m pytest tests/orchestration/test_run_report.py -q`  base 71 passed
      `python3 -m pytest tests/cli/test_golden_path.py -q`  base 42 — the canary
      `python3 -m ruff check packages/orchestration/proof_chain.py packages/orchestration/ui_server.py tests/orchestration/test_proof_chain.py tests/ui_contracts/test_apply_state_partial.py`
          must exit 0

 G8 THE STRUCTURE over `2a938b5e`..C6. Every commit single-parent. Report each
    commit's insertion count — the `+` column of `git diff --numstat`, which
    AGENTS.md DECISION F104 D1 caps at 500 — and confirm each is under 500. The
    path set over that range must EQUAL the change set above MINUS
    `.agent/handoff.md`, in BOTH directions; the handback is written at C7 and
    C8, which this range deliberately does not reach, and that is the whole of
    the difference. Read each path below at `2a938b5e` and at C6 with
    `git rev-parse <commit>:<path>` — a read that writes nothing — and require
    the two blob ids EQUAL:
      `packages/orchestration/run_report.py`
      `packages/orchestration/evidence_index.py`
      `packages/orchestration/diff_parser.py`
      `packages/orchestration/hunk_identity.py`
      `packages/orchestration/hunk_apply.py`
      `packages/orchestration/source_apply.py`
      `packages/orchestration/diff_repair.py`
      `apps/cli/commands/patch.py`
      `apps/ui/src/api/types.ts`
      `apps/ui/src/cockpitLogic.ts`
      `apps/ui/src/components/detail/DetailPopover.tsx`
      `apps/ui/src/components/panels/TaskChecklistCard.tsx`
      `apps/ui/src/components/panels/RightLivePanel.module.css`
      `tests/ui_server/test_dashboard_cockpit_truth.py`
      `docs/roadmap/STATUS.md`
      `docs/roadmap/ROADMAP.md`

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It
carries the SESSION NUMBER 5, the round number 18, the Fortschritt line, the
changed-files table, ONE LINE PER GATE with real exit codes, the open-findings
count, every deviation with its reason, and the next expected action. It has NO
length cap. The `## Commits` table takes its `+/-` cells from the SAME
`git diff --numstat` run G8 reports — compare them cell by cell and say you did;
never fill that column from a file's line counts. Then the two pushes and C8, in
the order stated above.

The authored slices follow. Each marker line opens with three '<' and closes
with three '>'. A slice begins on the line after its BEGIN marker and ends on
the line before its END marker; the marker lines are never part of the slice.

<<<BEGIN PLAN18 target=.agent/plan.md mode=replace bytes=2765 sha256=5214755bf41d758a22903a62b8d60b6df4c2ab4af7929f2c6d7779ad0b6a273a>>>
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
| one evidence-directory resolver, the CLI door, the write door | done | 13-15 |
| T003 the fold's partial truth, the popover label | done | round 16 |
| T003 the tasks-card partial tile and status text | done | round 17, D5 |
| T003 the fold gets a shared home and counts | open | this round |
| T003 the report line | open | next |
| T003 rejection reasons quoted into the repair prompt | open | after that |
| R-0738, resolvable once the report line lands | open | R-0738 |
| R-0745, the door's transitive import closure | open | next door work |
| the operator docs for `patch approve-hunks` | open | closure sequence |

## Next Steps
1. The apply fold moves out of `packages/orchestration/ui_server.py` into
   `packages/orchestration/proof_chain.py`, where `ProofChange` and its
   `apply_state` are defined, and gains the APPLIED and TOTAL counts R-0738's
   fix asks for. `_task_truth_maps` keeps its name and signature and delegates,
   so the cockpit's own tests stay untouched. The seam guard in
   `tests/ui_contracts/test_apply_state_partial.py` follows the literals to
   their new file: it walks them by AST, so leaving it behind would EMPTY its
   expected set rather than redden it.
2. Then the report line. `packages/orchestration/run_report.py` holds no apply
   state at all, so `TaskOutcome` gains one and `_task_lines` renders the mixed
   case with its counts. Only then is R-0738 resolvable on all three surfaces.
3. Then rejection reasons quoted VERBATIM into the next repair prompt, with the
   trace proof `docs/roadmap/features/T5_F033.md` calls acceptance material.
4. Then the closure sequence, which owes `docs/` an operator-facing description
   of `remedy patch approve-hunks` — no round has had a `docs/` path yet.

## Risks
- The fold's labels are read by an AST walk in a test that names the file they
  live in; the move and that test's re-pointing must land in one round.
<<<END PLAN18>>>

<<<BEGIN RECORD18 target=.agent/live_review.md mode=append bytes=5764 sha256=40df3d80c337ebf480b5638f14b8adb861d31df74436c6a067d1c7b047cb48bf>>>
Gate: F033 R17 — THE TASKS-CARD ROW LEARNS THE PARTIAL APPLY STATE. THE ROUND PASSED. This entry books, under operator amendment amend0827 rule 1, the verdict the reviewer committed and pushed in `.agent/handoff.md` at `2a938b5e`; it is written by the first substantive commit of round 18 and buys no round of its own. Every gate was re-executed by the reviewer at `2a938b5e` from scripts of its own, and every ordered reading reproduced. TRANSPORT, and it is stronger this round than the shape docs/agents/planner_reviewer_prompt.md §3 item 37 describes as this workflow's limit: `cmp` of the committed `.agent/authored/f033-r17.md` against the reviewer's OWN scratchpad original, and `cmp` of `.agent/last_block.md` against that same original, both SILENT — one end of each comparison is the reviewer's file rather than the worker's, so this is a real receipt and not only a self-consistency chain; the three applied slice regions are byte-EQUAL to their originals at 2660, 6982 and 959 bytes. THE RECORD APPEND at `49052cf5` reconstructs 1542724 plus one newline plus 6982 to 1549707, the committed blob exactly, base a byte PREFIX, slice an exact SUFFIX, N COUNTED at 2 over 706 blank-line units, the last two units equal to the slice's paragraphs IN ORDER, and a negative control at byte 1544671 — proved to lie inside the FIRST appended paragraph, spanning 1542725 to 1546617, exactly the span the block stated — REJECTED by both readers run independently, each of which accepted the unflipped file. THE LEDGER: registered 306 UNMOVED, this round registering nothing; `Done:` 50 lines over 48 distinct UNMOVED; `Landed:` 17 UNMOVED; `^Gate: F033 R16 — ` 0 before and exactly 1 after; distinct `DECISION F033 D` ids 4 before and 5 after with the ADDED one exactly D5; the open set 258 at both ends; and `- R-0738` still registered with no `Done:` line, which is correct — this round advanced it to its SECOND surface and did not resolve it. THE PROSE FILES: `.agent/plan.md` byte-EQUAL to its slice at 2660 bytes over 47 lines, under the 50-line cap, carrying `## Goal` and `## Next Steps`; `.agent/prose_slips.md` reconstructs 24982 plus one newline plus 959 to 25942, prefix and suffix both proved. THE CODE is exactly what the SPEC ordered and nothing more: `iconFor` and `stateText` in `apps/ui/src/components/panels/TaskChecklistCard.tsx` now take the ROW and read `applyStatus` BEFORE the lifecycle state, so a finished task whose changes only half landed no longer reads "Done"; `.checkPartial` in `apps/ui/src/components/panels/RightLivePanel.module.css` is `.checkDone` with `background: var(--remedy-blue-strong)`, reusing the existing `TaskDoneGlyph`, and the reviewer measured that the file's DISTINCT hex colour values are unchanged by the round, so no new colour entered it. THE MUTATIONS were re-run by the reviewer in its own disposable worktree at `2a938b5e` with its OWN anchors, each asserted UNIQUE before mutating, every file restored and PROVED byte-identical against the committed blob afterwards: unmutated control 20 passed at REAL exit 0; deleting the `styles.checkPartial` tile branch is exit 1 at 1 failed, the tile assertion alone; deleting the `Partially applied` label branch is exit 1 at 3 failed, the two label assertions and the cross-component one; and replacing the fold's `partial` with `applied` in `packages/orchestration/ui_server.py` is exit 1 at 6 failed — the two popover assertions plus ALL FOUR card seam assertions — which proves the card guard derives its expected set from the SHIPPED fold's AST rather than restating it. THE REVIEWER ALSO RAN A MUTATION THE BLOCK NEVER ORDERED, to test the round's newest claim rather than take it on trust: changing the POPOVER's label so the two surfaces spell the state differently reddens EXACTLY ONE test, `test_the_card_and_the_popover_use_one_spelling`, so the one-spelling guard is an independent discriminator and not a side effect of its neighbours. The post-restore control is 20 passed at REAL exit 0 and the worktree was removed by exact path. THE SUITES were re-run SERIALLY in the primary checkout, every REAL exit 0: the contract file 20 passed against a base of 13, `tests/ui_contracts/` 684 passed and 4 skipped against 677 and 4, the dashboard contract 74, the named-bug regressions 64 passed and 6 skipped, and the canary 42, with `ruff` exiting 0 over the changed test file. THE STRUCTURE: ten single-parent commits over `5f0273d8`..`2a938b5e` of 345, 345, 14, 4, 4, 23, 204, 262, 16 and 19 insertions, every one under 500; the path set over the WHOLE range EQUALS the declared change set in BOTH directions; and all sixteen do-not-touch paths blob-identical at both ends. SEVEN DEVIATIONS were declared and all seven are honest. Two are defects in the reviewer's own block and are recorded in `.agent/prose_slips.md` as this round's two slips, with no id and no round of their own, under operator amendment amend0827 rule 2: the block's SPEC B set "same white glyph colour" against "no raw hex colour is introduced" when the neighbour it ordered copied carries `color: #fff`, and the block named C7 as the push-outcome commit while saying nothing about whether C7 is itself pushed, which is round 16's slip reproduced one level down. The other five need no action: the sandbox denies the bare `ruff` executable so the identical check ran through `python3 -m ruff`; the block's stated paragraph span was CORRECT and the worker's first script used a different index convention, which it re-measured and declared; an `-x` run's partial count was withdrawn rather than reported as a measurement; the three ordered card-vacuity readings were written as three; and no `Done:` or `Landed:` line was written, which is what constraint 8 ordered.
<<<END RECORD18>>>

<<<BEGIN SLIPS18 target=.agent/prose_slips.md mode=append bytes=1049 sha256=6372f2bbee6a23f437a09c342aa515ca7d81903e11b7da6311410826b77e4956>>>
2026-08-29 · F033 R17 · The block's SPEC B ordered `.checkPartial` to keep "the same white glyph colour" as `.checkDone` AND said "no raw hex colour is introduced", while the rule it ordered copied carries `color: #fff`, so the two clauses could not both be met literally; the worker applied the first, declared the disagreement, and the reviewer measured that the file's DISTINCT hex colour values are unchanged by the round, so the intended property held and only the wording was wrong — a clause about a VALUE SET should say so instead of saying "no raw hex".

2026-08-29 · F033 R17 · The block named C7 as the commit the push outcome lands in, which repaired round 16's slip, and then said nothing about whether C7 is ITSELF pushed, so C7's text predicted it would stay local and AGENTS.md Push Discipline falsified that prediction the moment the worker obeyed it; the worker spent a declared C8 correcting one sentence, and a block that names a post-push commit must also say what happens to that commit — the same slip one level down.
<<<END SLIPS18>>>

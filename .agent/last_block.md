STEP T003d — F033 Hunk-level diff approval — ROUND 19 — SESSION 5

Goal: give the run report R-0738's THIRD surface — a task line that tells a
mixed apply state from a complete one, with the counts behind it — fix R-0746 in
the same round that gives the shared fold its second importer, and book the
round 18 verdict and its two prose slips in the first commits.

WHY THIS ROUND EXISTS. R-0738 names three surfaces and two are built. The third
is `packages/orchestration/run_report.py`, which holds NO reference to apply
state at all, measured by the reviewer at `41b83021`: `TaskOutcome` carries a
task id, a description, a status and an evidence ref, and `_task_lines` renders
exactly those. Round 18 put the fold where this module may import it. This round
is the consumer. After it, R-0738 is RESOLVABLE — but this block does NOT
resolve it: the reviewer writes that resolution at the next gate, after gating
this round's evidence, and this round writes no `Done:` line for it.

THE CONSTRAINT THIS ROUND IS BUILT AROUND. `tests/orchestration/test_run_report.py`
holds GOLDEN FULL-TEXT REPORTS — `GOLDEN_GREEN` and its neighbours are complete
expected documents, and their `## Tasks` sections contain lines such as
"- `aaaaaaaa` — Write the renderer — **completed** — [evidence](tasks/aaaaaaaa/output.md)"
byte for byte. A task with NO recorded apply state must therefore render EXACTLY
as it does today. That is not only a test-compatibility trick: it is this
module's own P6 rule that an absent source renders "not recorded" and never an
invented value. Build the new clause so the golden reports pass UNCHANGED and do
not edit them; if you find you must, stop and declare it.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f033-r19.md`
  C0b  mirror the same bytes into `.agent/last_block.md`
  C1   `.agent/plan.md` <- PLAN19 (whole-file replacement)
  C2   `.agent/live_review.md` <- append RECORD19
  C3   `.agent/prose_slips.md` <- append SLIPS19
  C4   the report's apply state, its attach and its line (SPEC A)
  C5   the report's tests (SPEC B)
  C6   R-0746: the public API list, and the guard that keeps it true (SPEC C)
  C7   `.agent/handoff.md` <- the handback
  C8   `.agent/handoff.md` <- the PUSH OUTCOME, recorded after the push

WHERE THE PUSHES GO. Push after C7. Then write the REAL outcome of that push
into `.agent/handoff.md` and commit it as C8. Then push AGAIN so C8 reaches the
remote. That last push is the round's final action and is recorded in NO commit,
deliberately — a commit recording it would need a commit recording that one, and
the regress is cut here. The REVIEWER verifies the final pushed state itself.
Never write a sentence predicting what a later push will do.

C1 is the FIRST substantive commit because this round touches the finding
ledger, per docs/agents/planner_reviewer_prompt.md section 3 checklist item 23.

Change set — exactly these paths, nothing else, in either direction:
  `.agent/authored/f033-r19.md`
  `.agent/last_block.md`
  `.agent/plan.md`
  `.agent/live_review.md`
  `.agent/prose_slips.md`
  `packages/orchestration/run_report.py`
  `packages/orchestration/proof_chain.py`
  `tests/orchestration/test_run_report.py`
  `.agent/handoff.md`

Constraints:
 1. Apply every authored slice BYTE FOR BYTE. If a slice is wrong, apply it as
    given and declare the disagreement. Never edit a slice.
 2. The authored slices are WHOLE TEXTS, not FROM/TO pairs. PLAN19 REPLACES
    `.agent/plan.md`. RECORD19 and SLIPS19 are APPENDS: each target ends in
    exactly one newline today, so the applied form is the old bytes, then ONE
    newline, then the slice. No pair here is FROM/TO, so no containment test and
    no FROM-zero count is owed anywhere in this block.
 3. RECORD19 registers finding R-0746 and this round FIXES it, at C6. Because a
    resolution is the reviewer's text and never the worker's, write
    `Landed: R-0746 — <one line: what changed, which commit>` into
    `.agent/live_review.md` at C6 and NOTHING else about it. Do not write a
    `Done:` line for R-0746 or for any other finding.
 4. R-0738 is NOT resolved here and no `Done:` or `Landed:` line is written for
    it. This round builds its third surface; the reviewer gates that evidence
    and writes the resolution at the next gate.
 5. `packages/orchestration/ui_server.py` is NOT touched. Its adapter already
    consumes the fold and this round changes no cockpit answer.
 6. Destructive verification runs ONLY inside a disposable `git worktree`
    (docs/agents/self_drive_protocol.md G5). The primary checkout satisfies
    `git status --porcelain` empty at the handback.
 7. Every gate command is EXECUTED and its REAL exit code recorded. The word
    "green" is not a result.
 8. The bare `ruff` executable is denied to this session's shell. Run
    `python3 -m ruff check ...` and say which form you used.

SPEC A — `packages/orchestration/run_report.py`

Read the module first, at least `TaskOutcome`, `_task_lines`,
`collect_report_sources`, `_evidence_sources` and `build_report_sources`, and
note how every evidence-area read is guarded on its own so one unreadable source
never costs the report the others.

 A1. `TaskOutcome` gains three fields, all defaulted so every existing
     construction site keeps working unchanged: the folded apply state as a
     string defaulting to the EMPTY string, and the applied and total counts as
     integers defaulting to 0. Empty means NOT RECORDED, which is this module's
     standing rule for an absent source, and it is what keeps the golden reports
     byte-identical.
 A2. `build_report_sources` attaches the state. It already has the job and the
     base sources, so it is the only place that can. Import
     `fold_task_apply_states` from `packages/orchestration/proof_chain.py`,
     build the chain the same way the rest of this module reaches evidence —
     guarded on its own, any failure leaving the tasks exactly as they were —
     and rewrite the `tasks` tuple with the state and counts attached.
 A3. MATCH ON THE FULL TASK ID, NEVER ON `TaskOutcome.task_id`. Measured by the
     reviewer at `41b83021`: `collect_report_sources` sets that field to
     `str(getattr(t, "id", ""))[:8]`, a TRUNCATION, while the fold keys on the
     full id. Two tasks whose ids share their first eight characters would
     otherwise take each other's apply state. Re-read `job.tasks` — the same
     iteration `collect_report_sources` used — and pair each full id with its
     `TaskOutcome`, so the truncated value is never a lookup key. State that
     reason in a WHY comment above the attach; it is the trap this round names
     in its own plan.
 A4. `_task_lines` renders the clause ONLY when the apply state is non-empty,
     appended after the status and before the evidence link, so an unrecorded
     state produces the line this module produces today, byte for byte. Use
     these words, with the counts as applied-over-total:
       partial      -> partially applied (5/8 changes)
       applied      -> applied (8/8 changes)
       reverted     -> reverted (0/8 changes)
       not_applied  -> not applied (0/8 changes)
     "partially applied" is the spelling the other two surfaces already use;
     keep it. An apply state this table does not know renders NOTHING rather
     than an invented phrase — the same fail-quiet rule as an absent source.
 A5. Do not change the task-line cap, the evidence link, or any other section.

SPEC B — `tests/orchestration/test_run_report.py`

Add a class for the new behaviour. Do not edit the golden reports, and do not
weaken any existing assertion.

 B1. Render a task with each of the four states and assert the exact clause,
     including the counts. Build the mixed case EXPLICITLY — R-0738's resolution
     asks for a test that constructs the mixed state rather than one that
     observes whatever a fixture produced.
 B2. Assert that a `TaskOutcome` with no apply state renders the line UNCHANGED:
     compare against the same line rendered by a source built without the new
     fields, so the assertion measures the property rather than restating the
     string.
 B3. Assert that an apply state the table does not know renders no clause.
 B4. THE TRUNCATION TEST, which is the one that pins A3. Build a job with TWO
     tasks whose ids agree in their first eight characters and differ after
     them, give them DIFFERENT apply states, drive `build_report_sources`, and
     assert each task line carries ITS OWN state. A lookup on the truncated id
     passes every other test in this file and fails this one.
 B5. Assert the counts survive the attach: a task whose applied and total differ
     reports both, and they are the fold's numbers rather than recomputed here.
 B6. Do not assert a COUNT of tests anywhere.

SPEC C — R-0746, in `packages/orchestration/proof_chain.py` and its test

 C1. Add `fold_task_apply_states(chain) -> dict[str, TaskApplyState]` to the
     `Public API::` block of the module docstring, in the same shape the four
     entries already there use. That is the whole fix.
 C2. Add ONE test — put it in `tests/orchestration/test_run_report.py` with the
     rest of this round's tests, since that file is already in the change set —
     that reads the two against each other rather than restating either: collect
     every module-level function in `proof_chain.py` whose name does not begin
     with an underscore, by walking the AST, and assert every one of them is
     named in the `Public API::` block. A list that is checked only by being
     re-typed is the defect R-0746 already is.
 C3. At C6 write the `Landed: R-0746` line described in constraint 3.

Done when — G1 through G8, the maximum operator amendment amend0827-process-diet
rule 5 allows. Run every one. Report ONE LINE PER GATE in the handback with the
command's REAL exit code and the numbers it printed. Every gate runs at a commit
STRICTLY EARLIER than C7, which is what lets the handback quote it.

 G1 HYGIENE AND THE STOP FILE. Before C0a, confirm `.agent/STOP` does not exist
    and report the exact message printed. Run `git status --porcelain` before
    C0a and again after C6; both must print nothing.

 G2 TRANSPORT. For each slice below, extract its applied region from its target
    and compare that region's sha256 to the digest in that slice's BEGIN marker:
      PLAN19   2740 bytes  8e33f449d67de9ab27f6d8f79f797fc4038b8ad176966aee40143abf2ad3baf4
      RECORD19 8021 bytes  7f6d3ccb1526a4a731ac9ba4fdce26709327d6f0c55bbdfc0706cd2b8ac2ecc2
      SLIPS19  1047 bytes  44aa61fab7ee3c5bbca05327fcb81d8609024922fc8a0e4254d0326d9a1e8601
    For PLAN19 the region is the WHOLE file; for the appends it is the LAST N
    bytes, N being that slice's byte length above. Report one digest and one
    verdict per slice. This proves the saved copy, its mirror and the working
    copy agree; it is not a claim about the emitted bytes, and the handback says
    so in those words.

 G3 THE RECORD APPEND at C2 — full byte forensics, `.agent/live_review.md` being
    the record. Three readings, all required:
    (a) BYTES. The pre-commit blob is 1555472 bytes and must be a byte PREFIX of
        the post-commit file; the post-commit file must be exactly 1563494 bytes
        (1555472 + 1 + 8021); RECORD19 must be an exact SUFFIX of it.
    (b) STRUCTURE, an independent reader. Split the post-commit file on blank
        lines, COUNT the slice's paragraphs into N — your script counts N, this
        block does not assert it — and require the LAST N blank-line units to
        equal the slice's N paragraphs IN ORDER.
    (c) NEGATIVE CONTROL. Flip one byte at offset 1558370 of the post-commit
        file. That offset lies inside the FIRST appended paragraph, which spans
        1555473 to 1561267; ASSERT that containment before flipping. Run readers
        (a) and (b) INDEPENDENTLY and require EACH to reject the flipped copy
        AND to accept the unflipped one — a reader that rejects everything
        proves nothing. Flip in memory or on a copy, never on the tracked file.

 G4 THE LEDGER after C2 and again after C6, every count as a before and an
    after. This round is the first in a while to move the ledger, so read
    carefully:
      `^- R-\d+ — `        306 before, 307 after C2, the ADDED id exactly R-0746
      `^Done: R-\d+ — `    50 lines over 48 distinct, UNMOVED at both
      `^Landed: R-\d+ — `  17 before, 18 after C6, the ADDED id exactly R-0746
      `^Gate: F033 R18 — ` 0 before, exactly 1 after C2
      distinct `DECISION F033 D<n>` ids: 5, UNMOVED — this round rules none
      the open set, registered minus distinct resolved: 258 before, 259 after
      `^- R-0738 — ` still exactly 1, with NO `^Done: R-0738 — ` line

 G5 THE PROSE FILES. `.agent/plan.md` after C1 is byte-EQUAL to PLAN19 at 2740
    bytes over 48 lines — under the 50-line cap AGENTS.md sets — and still holds
    `## Goal` and `## Next Steps`. `.agent/prose_slips.md` after C3 is exactly
    28040 bytes (26992 + 1 + 1047), old bytes a PREFIX, SLIPS19 an exact SUFFIX.

 G6 THE MUTATIONS, at the commit C6 creates, inside a disposable `git worktree`,
    restoring every mutated file byte-identically and PROVING it against the
    committed blob. Report the UNMUTATED CONTROL first with its real exit code
    and counts. Before each mutation assert its anchor occurs EXACTLY ONCE in
    the file named, and report that count. Run
    `tests/orchestration/test_run_report.py` for each:
    (i)   In `packages/orchestration/run_report.py`, make `_task_lines` drop the
          apply clause entirely. SPEC B1's four state assertions must go RED,
          and B2's unchanged-line assertion must STAY GREEN — report both, since
          a mutation that reddens everything would not distinguish the two.
    (ii)  In the same file, make the attach look the apply state up by the
          TRUNCATED `TaskOutcome.task_id` instead of the full id. ONLY SPEC B4's
          truncation test may go red. If others go red as well, say so; if B4
          stays GREEN, the truncation test is pinning nothing and you must say
          that plainly.
    (iii) In `packages/orchestration/proof_chain.py`, delete the
          `fold_task_apply_states` line from the `Public API::` block. SPEC C2's
          guard must go RED — that is the proof R-0746's fix is held by a test
          rather than by having been typed once.

 G7 THE SUITES, SERIALLY, in the PRIMARY checkout at the commit C6 creates, each
    with its real exit code. Base readings measured by the reviewer at
    `41b83021`, so a number that moves is a result rather than a surprise:
      `python3 -m pytest tests/orchestration/test_run_report.py -q`
          base 71 passed; MUST be higher — report it
      `python3 -m pytest tests/orchestration/test_proof_chain.py -q`
          base 104 passed; SPEC C adds no test here, so 104 is expected
      `python3 -m pytest tests/ui_contracts/test_apply_state_partial.py -q`
          base 20 passed; not edited, so 20 is expected
      `python3 -m pytest tests/ui_server/test_dashboard_cockpit_truth.py -q`
          base 39 passed; not edited, so 39 is expected
      `python3 -m pytest tests/cli/test_job_report.py -q`
          the CLI reader of this report; report the number you measure
      `python3 -m pytest tests/cli/test_golden_path.py -q`  base 42 — the canary
      `python3 -m ruff check packages/orchestration/run_report.py packages/orchestration/proof_chain.py tests/orchestration/test_run_report.py`
          must exit 0

 G8 THE STRUCTURE over `41b83021`..C6. Every commit single-parent. Report each
    commit's insertion count — the `+` column of `git diff --numstat`, which
    AGENTS.md DECISION F104 D1 caps at 500 — and confirm each is under 500. The
    path set over that range must EQUAL the change set above MINUS
    `.agent/handoff.md`, in BOTH directions; the handback is written at C7 and
    C8, which this range deliberately does not reach. Read each path below at
    `41b83021` and at C6 with `git rev-parse <commit>:<path>` — a read that
    writes nothing — and require the two blob ids EQUAL:
      `packages/orchestration/ui_server.py`
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
      `tests/ui_server/test_dashboard_cockpit_truth.py`
      `tests/ui_contracts/test_apply_state_partial.py`
      `docs/roadmap/STATUS.md`
      `docs/roadmap/ROADMAP.md`

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It
carries the SESSION NUMBER 5, the round number 19, the Fortschritt line, the
changed-files table, ONE LINE PER GATE with real exit codes, the open-findings
count, every deviation with its reason, and the next expected action. It has NO
length cap. The `## Commits` table takes its `+/-` cells from the SAME
`git diff --numstat` run G8 reports — compare them cell by cell and say you did.
Then the two pushes and C8, in the order stated above.

The authored slices follow. Each marker line opens with three '<' and closes
with three '>'. A slice begins on the line after its BEGIN marker and ends on
the line before its END marker; the marker lines are never part of the slice.

<<<BEGIN PLAN19 target=.agent/plan.md mode=replace bytes=2740 sha256=8e33f449d67de9ab27f6d8f79f797fc4038b8ad176966aee40143abf2ad3baf4>>>
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
| T003 the fold's shared home and its counts | done | round 18 |
| T003 the report line, R-0738's third surface | open | this round |
| R-0746, the module's stale public API list | open | this round |
| T003 rejection reasons quoted into the repair prompt | open | next |
| R-0738, resolvable once the report line is gated | open | after that |
| R-0745, the door's transitive import closure | open | next door work |
| the operator docs for `patch approve-hunks` | open | closure sequence |

## Next Steps
1. The report line. `packages/orchestration/run_report.py` holds no apply state
   at all, so `TaskOutcome` gains one with its counts, `build_report_sources`
   attaches it from `fold_task_apply_states`, and `_task_lines` renders the
   mixed case. A task with NO recorded apply state renders exactly as it does
   today — the golden reports in `tests/orchestration/test_run_report.py` are
   full-text fixtures and are the guard for that. R-0746 is fixed in the same
   round, because this is the round that gives the fold its second importer.
2. Then rejection reasons quoted VERBATIM into the next repair prompt, with the
   trace proof `docs/roadmap/features/T5_F033.md` calls acceptance material.
3. Then R-0738 is resolvable: viewer badge, tasks-card row and report line all
   tell a mixed apply state apart from a complete one.
4. Then the closure sequence, which owes `docs/` an operator-facing description
   of `remedy patch approve-hunks` — no round has had a `docs/` path yet.

## Risks
- The report's task ids are truncated to eight characters while the fold keys on
  the full id, so the attach must not match on the truncated value.
<<<END PLAN19>>>

<<<BEGIN RECORD19 target=.agent/live_review.md mode=append bytes=8021 sha256=7f6d3ccb1526a4a731ac9ba4fdce26709327d6f0c55bbdfc0706cd2b8ac2ecc2>>>
Gate: F033 R18 — THE APPLY FOLD GETS A SHARED HOME AND ITS COUNTS. THE ROUND PASSED. This entry books, under operator amendment amend0827 rule 1, the verdict the reviewer committed and pushed in `.agent/handoff.md` at `41b83021`; it is written by the first substantive commit of round 19 and buys no round of its own. Every gate was re-executed by the reviewer at `41b83021` from scripts of its own, and every ordered reading reproduced. TRANSPORT: `cmp` of the committed `.agent/authored/f033-r18.md` against the reviewer's OWN scratchpad original, and of `.agent/last_block.md` against that same original, both SILENT — one end of each comparison is the reviewer's file rather than the worker's — and the three applied slice regions are byte-EQUAL to their originals at 2765, 5764 and 1049 bytes. THE RECORD APPEND at `440de7ea` reconstructs 1549707 plus one newline plus 5764 to 1555472, the committed blob exactly, base a byte PREFIX, slice an exact SUFFIX, N COUNTED at 1 over 707 blank-line units, and a negative control at byte 1552589 — proved to lie inside the FIRST appended paragraph, spanning 1549708 to 1555470, exactly the span the block stated — REJECTED by both readers run INDEPENDENTLY, each of which accepted the unflipped file. THE LEDGER: registered 306 UNMOVED; `Done:` 50 lines over 48 distinct UNMOVED; `Landed:` 17 UNMOVED; `^Gate: F033 R17 — ` 0 before and exactly 1 after; distinct `DECISION F033 D` ids 5 at both ends, this round ruling none; the open set 258 at both ends; and `- R-0738` still registered with no `Done:` line. THE PROSE FILES: `.agent/plan.md` byte-EQUAL to its slice at 2765 bytes over 49 lines, under the 50-line cap; `.agent/prose_slips.md` reconstructs 25942 plus one newline plus 1049 to 26992. THE MOVE IS A MOVE: the fold's four branches sit in `packages/orchestration/proof_chain.py` in the same order and with the same comparisons they had in `packages/orchestration/ui_server.py`, the counts are added beside the answer rather than folded into it, and `_task_truth_maps` keeps its name, signature and return type and drops to an adapter over the folded entries' `state`. THE SEAM GUARD REALLY FOLLOWED THE CODE, which was this round's whole risk: `tests/ui_contracts/test_apply_state_partial.py` now names `packages/orchestration/proof_chain.py`, the function `fold_task_apply_states` and the subscript `state_by_task`, and its own non-vacuity assertion is what would catch a re-pointing that had silently emptied the expected set. THE MUTATIONS were re-run by the reviewer in its own disposable worktree at `41b83021` with its OWN anchors, each asserted UNIQUE before mutating, every file restored and PROVED byte-identical against the committed blob: unmutated control 163 passed at REAL exit 0; collapsing the fold's `partial` into `applied` is exit 1 at 12 failed ACROSS THREE FILES, including the cockpit file this round never edited; making the applied count report the group size is exit 1 at 4 failed, exactly the count assertions; and emptying the adapter is exit 1 at 8 failed, every one of them in that same unedited cockpit file, which is the proof the delegation is still wired. THE REVIEWER ALSO RAN A CHECK THE BLOCK NEVER ORDERED, and it is the one that actually settles this round's central claim. The block's constraint 3 required that NO ANSWER CHANGE, and the ordered gates only showed that the cockpit's tests stayed green, which is weaker. So the reviewer built the SAME synthetic chains in a worktree at `2a938b5e` and in one at `41b83021`, drove the SHIPPED `_task_truth_maps` in each, and compared: 157 task shapes — every combination of `applied`, `reverted`, `not_applied`, the empty string and an unrecognised value up to length three, plus the empty-task-id case and the None chain — with EQUAL key sets and ZERO differing answers. The move changed nothing, measured rather than argued. THE SUITES were re-run SERIALLY in the primary checkout, every REAL exit 0: `test_proof_chain.py` 104 passed against a base of 90, the contract file 20, the cockpit truth 39, `tests/ui_contracts/` 684 passed and 4 skipped, `test_run_report.py` 71 and the canary 42, with `ruff` exiting 0 over all four changed files. THE STRUCTURE: ten single-parent commits over `2a938b5e`..`41b83021` of 373, 273, 19, 2, 4, 81, 170, 34, 269 and 14 insertions, every one under 500; the path set over the WHOLE range EQUALS the declared change set in BOTH directions; and all sixteen do-not-touch paths blob-identical at both ends, `packages/orchestration/run_report.py` and `tests/ui_server/test_dashboard_cockpit_truth.py` among them. NINE DEVIATIONS were declared and all nine are honest. One is promoted to the finding R-0746 registered below. Two are defects in the reviewer's own block and are recorded in `.agent/prose_slips.md` as this round's two slips: the block ordered an `ImportError` guard on a function that performs no import, and its SPEC B3 stated the sweep "the four apply labels are literals in `proof_chain.py` and in no other production module" widely enough to invite a literal string search that finds the unrelated proof-metrics `"partial"` still standing in `ui_server.py`. The remaining six need no action: the sandbox denies the bare `ruff` executable so the identical check ran through `python3 -m ruff`; the constant naming the searched file was renamed from a name that would have been false after the move, an identifier change that altered no assertion; the membership predicate's premise held already and was made explicit rather than rewritten; the restores went through a checkout of the exact path when a textual revert became ambiguous, with byte-identity proved against the committed blob; no `Done:` or `Landed:` line was written; and the ordered commit sequence was followed exactly.

- R-0746 — Low, `packages/orchestration/proof_chain.py` DOCUMENTS A PUBLIC API LIST THAT NO LONGER NAMES ALL OF ITS PUBLIC API. Raised by the reviewer at the F033 R18 gate, from the worker's own declared deviation, and promoted to a finding rather than a prose slip because the wrong state is on disk under `packages/` and a reader meets it. The module docstring carries a `Public API::` block listing `build_proof_chain`, `export_proof_chain_json`, `summarize_proof_chain` and `derive_next_safe_action`. Round 18 added a fifth public function to the module, `fold_task_apply_states`, whose entire reason for existing is that MORE THAN ONE module must import it — the cockpit does today and the run report does next round — and the list does not name it. Measured by the reviewer at `41b83021`: the function is defined at module level, has no leading underscore, is imported by `packages/orchestration/ui_server.py`, and appears nowhere in the docstring. WHY THIS IS NOT A PROSE SLIP: the AGENTS.md Code Discoverability Conventions rule that this repository is navigated by text search and that "deliberate absences are documented where a reader would search for them"; an export list is exactly such a reader's landing point, and one that is silently incomplete is worse than none, because it reads as exhaustive. A later reader looking for the shared fold's public entry point finds a curated list that excludes it and concludes it is private. WHY LOW: no behaviour is wrong, no gate is blind, every test passes, and the function is reachable and correct — the defect is confined to a navigational aid. It is the reviewer's own omission that produced it: the R18 SPEC named the WHY comment the new function must carry and never named the docstring list, so the worker left it alone deliberately and said so, which was the correct thing to do. FIX: add `fold_task_apply_states(chain) -> dict[str, TaskApplyState]` to the `Public API::` block in the same round that gives the function its second importer, so the list and the fact become true together. Resolved when the module docstring names every public function the module defines, checked by reading the two against each other rather than by trusting the list.
<<<END RECORD19>>>

<<<BEGIN SLIPS19 target=.agent/prose_slips.md mode=append bytes=1047 sha256=44aa61fab7ee3c5bbca05327fcb81d8609024922fc8a0e4254d0326d9a1e8601>>>
2026-08-29 · F033 R18 · The block's SPEC A4 ordered the moved fold to guard `ImportError` beside `AttributeError` and `TypeError` "so a malformed chain degrades exactly as it does today", but the new function performs no import — the old one did, which is why the guard was there — so one member of the ordered tuple is unreachable by construction; the worker applied it as written and declared it, and a spec that carries a guard across a move should re-derive which of its clauses the move keeps alive.

2026-08-29 · F033 R18 · The block's SPEC B3 claimed that after the move "the four apply labels are literals in `proof_chain.py` and in no other production module", which is true of the APPLY labels and false of a literal search for the string, because `_metrics_proof_from_chain` in `ui_server.py` sets a proof-metrics `state = "partial"` that has nothing to do with the fold; no gate ordered that count so nothing was unmeetable, and the lesson is the standing one that a sweep claim is only as wide as the search that measured it.
<<<END SLIPS19>>>

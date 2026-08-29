STEP T003e — F033 Hunk-level diff approval — ROUND 20 — SESSION 5

Goal: ship the function that turns rejected hunks into repair findings with the
operator's reasons quoted VERBATIM, with the trace proof this feature's
Acceptance calls acceptance material; and book the round 19 verdict together
with the resolutions of R-0738 and R-0746.

WHY THIS ROUND EXISTS. `docs/roadmap/features/T5_F033.md` requires that
"rejected hunks' reasons appear verbatim in the following repair prompt", and
its Design says rejections "enqueue as repair findings for the next round,
quoted with their reasons". The store already exists and already promises this:
`packages/orchestration/hunk_ledger.py` holds `HunkLedgerEntry.reason` as, in
its own docstring's words, "the operator's own words held VERBATIM, surrounding
whitespace included — T003 quotes it into the next repair prompt and this is not
the layer that reformats an operator's words". Nothing performs that quoting.
This round writes it, as a PURE function with no caller yet, and the round after
wires it into the builder's prompt. Shipping the renderer and its wiring in one
block does not fit, and a block that does not fit is not delivered.

THIS ROUND IS NOT BOOKKEEPING. It books a verdict and two resolutions in its
first commits, which operator amendment amend0827 rule 1 requires to ride on a
round that is happening anyway, and the round happening anyway is the new module.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f033-r20.md`
  C0b  mirror the same bytes into `.agent/last_block.md`
  C1   `.agent/plan.md` <- PLAN20 (whole-file replacement)
  C2   `.agent/live_review.md` <- append RECORD20
  C3   `.agent/prose_slips.md` <- append SLIPS20
  C4   the rejection-findings renderer (SPEC A)
  C5   its tests, including the verbatim trace proof (SPEC B)
  C6   `.agent/handoff.md` <- the handback
  C7   `.agent/handoff.md` <- the PUSH OUTCOME, recorded after the push

WHERE THE PUSHES GO. Push after C6. Then write the REAL outcome of that push
into `.agent/handoff.md` and commit it as C7. Then push AGAIN so C7 reaches the
remote. That last push is the round's final action and is recorded in NO commit,
deliberately — a commit recording it would need a commit recording that one, and
the regress is cut here. The REVIEWER verifies the final pushed state itself.
Never write a sentence predicting what a later push will do.

C1 is the FIRST substantive commit because this round touches the finding
ledger, per docs/agents/planner_reviewer_prompt.md section 3 checklist item 23.

Change set — exactly these paths, nothing else, in either direction:
  `.agent/authored/f033-r20.md`
  `.agent/last_block.md`
  `.agent/plan.md`
  `.agent/live_review.md`
  `.agent/prose_slips.md`
  `packages/orchestration/hunk_repair_findings.py`
  `tests/orchestration/test_hunk_repair_findings.py`
  `.agent/handoff.md`

Constraints:
 1. Apply every authored slice BYTE FOR BYTE. If a slice is wrong, apply it as
    given and declare the disagreement. Never edit a slice.
 2. The authored slices are WHOLE TEXTS, not FROM/TO pairs. PLAN20 REPLACES
    `.agent/plan.md`. RECORD20 and SLIPS20 are APPENDS: each target ends in
    exactly one newline today, so the applied form is the old bytes, then ONE
    newline, then the slice. No pair here is FROM/TO, so no containment test and
    no FROM-zero count is owed anywhere in this block.
 3. RECORD20 carries the round 19 verdict AND the `Done:` paragraphs for R-0738
    and R-0746. Those are the reviewer's authored resolutions. The existing
    `Landed: R-0746` line STAYS where it is: this record is append-only, and
    the precedent on this branch is that a `Landed:` line stands beside the
    `Done:` paragraph that supersedes it rather than being deleted. Write no
    `Done:` and no `Landed:` line of your own this round.
 4. `packages/orchestration/hunk_ledger.py` and
    `packages/orchestration/hunk_approval.py` are NOT touched. This round READS
    the shapes they define and adds nothing to them.
 5. The new module is PURE: text and data in, text out. No filesystem, no
    subprocess, no network, no environment read, no import of any module that
    performs those at import time. Its only project import is the ledger's
    types, and it must work when handed duck-typed objects rather than the real
    dataclasses.
 6. A new module under `packages/orchestration/` is swept by repo-wide guards
    that name no path — `.agent/context.md` records this as a standing project
    constraint. G7 therefore gates `tests/regression/test_named_bugs.py` and
    `tests/regression/test_resource_safety.py` beside this round's own tests.
 7. Destructive verification runs ONLY inside a disposable `git worktree`
    (docs/agents/self_drive_protocol.md G5). The primary checkout satisfies
    `git status --porcelain` empty at the handback.
 8. Every gate command is EXECUTED and its REAL exit code recorded. The word
    "green" is not a result. The bare `ruff` executable is denied to this
    session's shell; run `python3 -m ruff check ...` and say which form you used.

SPEC A — `packages/orchestration/hunk_repair_findings.py`, a NEW module

Read `packages/orchestration/hunk_ledger.py` first — at least its module
docstring, `HunkLedgerEntry`, `HunkDecisionLedger`, the three `HUNK_STATE_*`
constants and its `_total_text` guard. This module is its sibling and follows
its rules.

 A1. A module docstring in the shape this package uses, with a `Public API::`
     block naming every public name the module defines. Round 19's R-0746 is
     exactly the defect of a list that does not; write it complete and let
     SPEC B's guard hold it that way.
 A2. `render_rejection_findings(ledger) -> str`, the module's one public
     function. It returns the repair-prompt text for the REJECTED hunks of one
     attempt, and the EMPTY STRING when there are none — an empty findings block
     is not a heading with nothing under it.
 A3. THE VERBATIM RULE, which is the whole point of the function. Each rejected
     entry's `reason` is emitted EXACTLY as stored: no strip, no rewrap, no
     escaping, no truncation, no case change, no collapsing of internal
     whitespace. A reason containing newlines, backticks, markdown, leading or
     trailing spaces reaches the output unchanged. Put the reason on its OWN
     lines rather than inside a bullet, so a multi-line reason stays readable
     without being reformatted, and say in a WHY comment that this layer does
     not reformat an operator's words — `hunk_ledger.py`'s docstring is where
     that rule comes from.
 A4. Order is the LEDGER's own entry order, which is the order the attempt's
     diff carries its hunks. Do not sort, and do not deduplicate.
 A5. Only entries whose state is the rejected one appear. Approved and pending
     entries produce nothing at all — a repair prompt that lists what was
     accepted is a different feature.
 A6. TOTALITY, the rule every sibling in this family states: this function NEVER
     raises, on any input at all — `None`, a non-iterable, an object with no
     `entries`, an entry with no `reason`, an id whose `__str__` is broken.
     Re-state the coercion guard the way `hunk_ledger.py` does rather than
     importing its private one, and say why in a comment. On anything
     unreadable, return the empty string rather than a partial block.
 A7. Name the heading and any fixed literal as module-level constants so a
     caller and a test match on a NAME and never on a spelling — the convention
     `hunk_ledger.py` states for its own vocabularies.

SPEC B — `tests/orchestration/test_hunk_repair_findings.py`, a NEW file

Name it after the module it covers, which is this repository's pattern.

 B1. THE TRACE PROOF, and it is the acceptance material: build a ledger holding
     a rejected hunk whose reason contains AWKWARD BYTES — at minimum a newline,
     a backtick, leading and trailing whitespace, and a markdown-significant
     character — render it, and assert the reason appears in the output as an
     EXACT SUBSTRING, byte for byte. Assert the property, not a hand-typed copy
     of the expected document.
 B2. Two rejected hunks with different reasons both appear, each with its own
     id, and in the LEDGER's order rather than sorted.
 B3. Approved and pending entries contribute nothing: a ledger of only those
     renders the empty string, and a mixed ledger renders only its rejections.
 B4. An empty ledger renders the empty string, and so does a ledger whose
     entries are all approved — the two are different inputs and both are
     legitimate, per this feature's own edge-case note that a full-approval
     round is valid.
 B5. TOTALITY, driven rather than asserted: call the function with `None`, with
     an object having no `entries`, with a non-iterable `entries`, with an entry
     missing `reason`, and with an entry whose `__str__` raises, and assert each
     call RETURNS rather than raises. Build the raising object explicitly; a
     totality claim tested only on well-formed input is not tested.
 B6. THE GUARD FOR A1: walk the new module's AST for every public module-level
     function and assert each is named in its `Public API::` block. This is
     round 19's R-0746 fix applied to the module being born, so the list starts
     true and stays true. Put it in this file.
 B7. Do not assert a COUNT of tests anywhere.

Done when — G1 through G8, the maximum operator amendment amend0827-process-diet
rule 5 allows. Run every one. Report ONE LINE PER GATE in the handback with the
command's REAL exit code and the numbers it printed. Every gate runs at a commit
STRICTLY EARLIER than C6, which is what lets the handback quote it.

 G1 HYGIENE AND THE STOP FILE. Before C0a, confirm `.agent/STOP` does not exist
    and report the exact message printed. Run `git status --porcelain` before
    C0a and again after C5; both must print nothing.

 G2 TRANSPORT. For each slice below, extract its applied region from its target
    file AT THE COMMIT THAT APPLIED IT — C1 for PLAN20, C2 for RECORD20, C3 for
    SLIPS20 — and compare that region's sha256 to the digest in that slice's
    BEGIN marker. Naming the commit is round 19's second prose slip repaired:
    a later commit of the same round may legitimately append to the same file.
      PLAN20   2570 bytes  11f614e84b0eac586273872dd7938c11fb1ec83b10601f9861172907c089e91a
      RECORD20 10101 bytes 8cfd110e40c78fd9f2f173f633d3b166d0672106c763c3e693a6fb7f01d5d352
      SLIPS20  1622 bytes  0d0130886ab67db31061a36ae4f4b7ad7808c87467e58bf4f6da82c33ddfffa4
    For PLAN20 the region is the WHOLE file; for the appends it is the LAST N
    bytes at that commit, N being the slice's byte length above. Report one
    digest and one verdict per slice. This proves the saved copy, its mirror and
    the working copy agree; it is not a claim about the emitted bytes, and the
    handback says so in those words.

 G3 THE RECORD APPEND at C2 — full byte forensics, `.agent/live_review.md` being
    the record. Three readings, all required:
    (a) BYTES. The pre-commit blob is 1565456 bytes and must be a byte PREFIX of
        the post-commit file; the post-commit file must be exactly 1575558 bytes
        (1565456 + 1 + 10101); RECORD20 must be an exact SUFFIX of it AT C2.
    (b) STRUCTURE, an independent reader. Split the post-commit file on blank
        lines, COUNT the slice's paragraphs into N — your script counts N, this
        block does not assert it — and require the LAST N blank-line units to
        equal the slice's N paragraphs IN ORDER.
    (c) NEGATIVE CONTROL. Flip one byte at offset 1568181 of the post-commit
        file. That offset lies inside the FIRST appended paragraph, which spans
        1565457 to 1570905; ASSERT that containment before flipping. Run readers
        (a) and (b) INDEPENDENTLY and require EACH to reject the flipped copy
        AND to accept the unflipped one. Flip in memory or on a copy, never on
        the tracked file.

 G4 THE LEDGER after C2, every count as a before and an after. This round
    RESOLVES two findings, so read carefully:
      `^- R-\d+ — `        307, UNMOVED — this round registers nothing
      `^Done: R-\d+ — `    50 lines over 48 distinct before, 52 over 50 after,
                           the ADDED ids exactly R-0738 and R-0746
      `^Landed: R-\d+ — `  18, UNMOVED — the `Landed: R-0746` line STAYS
      `^Gate: F033 R19 — ` 0 before, exactly 1 after
      distinct `DECISION F033 D<n>` ids: 5, UNMOVED
      the open set, registered minus distinct resolved: 259 before, 257 after
      `^Done: R-0738 — ` and `^Done: R-0746 — ` each exactly 1 after

 G5 THE PROSE FILES. `.agent/plan.md` after C1 is byte-EQUAL to PLAN20 at 2570
    bytes over 46 lines — under the 50-line cap AGENTS.md sets — and still holds
    `## Goal` and `## Next Steps`. `.agent/prose_slips.md` after C3 is exactly
    29663 bytes (28040 + 1 + 1622), old bytes a PREFIX, SLIPS20 an exact SUFFIX.

 G6 THE MUTATIONS, at the commit C5 creates, inside a disposable `git worktree`,
    restoring the mutated file byte-identically and PROVING it against the
    committed blob. Report the UNMUTATED CONTROL first with its real exit code
    and counts. Before each mutation assert its anchor occurs EXACTLY ONCE in
    the file, and report that count. Run
    `tests/orchestration/test_hunk_repair_findings.py` for each:
    (i)   Make the renderer emit each rejected hunk's ID but not its REASON.
          SPEC B1's trace proof must go RED. This is the round's central
          reading: it is the only one that proves the verbatim property is
          measured rather than described.
    (ii)  Make the renderer emit APPROVED entries as well as rejected ones.
          SPEC B3's assertions must go RED.
    (iii) Remove the totality guard so a broken input raises. SPEC B5's driven
          totality assertions must go RED. If B5 stays green, the totality claim
          is pinned by nothing and you must say so plainly.

 G7 THE SUITES, SERIALLY, in the PRIMARY checkout at the commit C5 creates, each
    with its real exit code. Base readings measured by the reviewer at
    `d4a21259`, so a number that moves is a result rather than a surprise:
      `python3 -m pytest tests/orchestration/test_hunk_repair_findings.py -q`
          NEW this round; report the number you measure
      `python3 -m pytest tests/orchestration/test_hunk_ledger.py -q`
          base 29 passed; not edited, so 29 is expected
      `python3 -m pytest tests/orchestration/test_hunk_approval.py -q`
          base 30 passed; not edited, so 30 is expected
      `python3 -m pytest tests/regression/test_named_bugs.py -q`
          base 64 passed, 6 skipped — a repo-wide sweep, per constraint 6
      `python3 -m pytest tests/regression/test_resource_safety.py -q`
          base 21 passed — the other repo-wide sweep
      `python3 -m pytest tests/cli/test_golden_path.py -q`  base 42 — the canary
      `python3 -m ruff check packages/orchestration/hunk_repair_findings.py tests/orchestration/test_hunk_repair_findings.py`
          must exit 0

 G8 THE STRUCTURE over `d4a21259`..C5. Every commit single-parent. Report each
    commit's insertion count — the `+` column of `git diff --numstat`, which
    AGENTS.md DECISION F104 D1 caps at 500 — and confirm each is under 500. The
    path set over that range must EQUAL the change set above MINUS
    `.agent/handoff.md`, in BOTH directions; the handback is written at C6 and
    C7, which this range deliberately does not reach. Read each path below at
    `d4a21259` and at C5 with `git rev-parse <commit>:<path>` — a read that
    writes nothing — and require the two blob ids EQUAL:
      `packages/orchestration/hunk_ledger.py`
      `packages/orchestration/hunk_approval.py`
      `packages/orchestration/hunk_identity.py`
      `packages/orchestration/hunk_subset_diff.py`
      `packages/orchestration/hunk_apply.py`
      `packages/orchestration/proof_chain.py`
      `packages/orchestration/run_report.py`
      `packages/orchestration/ui_server.py`
      `packages/orchestration/diff_parser.py`
      `apps/cli/commands/patch.py`
      `apps/ui/src/api/types.ts`
      `apps/ui/src/components/detail/DetailPopover.tsx`
      `apps/ui/src/components/panels/TaskChecklistCard.tsx`
      `tests/ui_contracts/test_apply_state_partial.py`
      `docs/roadmap/STATUS.md`
      `docs/roadmap/ROADMAP.md`

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It
carries the SESSION NUMBER 5, the round number 20, the Fortschritt line, the
changed-files table, ONE LINE PER GATE with real exit codes, the open-findings
count, every deviation with its reason, and the next expected action. It has NO
length cap. The `## Commits` table takes its `+/-` cells from the SAME
`git diff --numstat` run G8 reports — compare them cell by cell and say you did.
Then the two pushes and C7, in the order stated above.

The authored slices follow. Each marker line opens with three '<' and closes
with three '>'. A slice begins on the line after its BEGIN marker and ends on
the line before its END marker; the marker lines are never part of the slice.

<<<BEGIN PLAN20 target=.agent/plan.md mode=replace bytes=2570 sha256=11f614e84b0eac586273872dd7938c11fb1ec83b10601f9861172907c089e91a>>>
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
| T003 partial truth on all three surfaces, R-0738 | done | rounds 16-19 |
| R-0746, the module's public API list | done | round 19 |
| T003 rejection reasons rendered verbatim as repair findings | open | this round |
| T003 that renderer wired into the next builder round | open | next |
| R-0745, the door's transitive import closure | open | next door work |
| the operator docs for `patch approve-hunks` | open | closure sequence |
| the integration gate round, then closure | open | after the above |

## Next Steps
1. The rejection half of T003's loop, as a PURE renderer with no caller yet:
   `packages/orchestration/hunk_ledger.py` already holds each rejected hunk's
   reason VERBATIM and says in its own docstring that T003 quotes it into the
   next repair prompt. This round ships the function that does the quoting and
   the trace proof the feature file calls acceptance material — a reason with
   awkward bytes in it survives into the rendered text unchanged.
2. Then wiring: the renderer's output reaches the next builder round's prompt,
   and the two-round end-to-end the feature's Acceptance asks for.
3. Then R-0745, whose fix clause recommends a transitive-closure test over the
   write door's imports.
4. Then the closure sequence: `docs/` still owes an operator-facing description
   of `remedy patch approve-hunks`, and no round has had a `docs/` path yet. The
   integration gate runs before closure, per docs/agents/integration_gate.md.

## Risks
- A new module under `packages/orchestration/` is swept by repo-wide guards that
  name no path, so this round gates the two sweeps as well as its own tests.
<<<END PLAN20>>>

<<<BEGIN RECORD20 target=.agent/live_review.md mode=append bytes=10101 sha256=8cfd110e40c78fd9f2f173f633d3b166d0672106c763c3e693a6fb7f01d5d352>>>
Gate: F033 R19 — THE REPORT LINE, R-0738's THIRD SURFACE. THE ROUND PASSED. This entry books, under operator amendment amend0827 rule 1, the verdict the reviewer committed and pushed in `.agent/handoff.md` at `d4a21259`; it is written by the first substantive commit of round 20 and buys no round of its own. Every gate was re-executed by the reviewer at `d4a21259` from scripts of its own, and every ordered reading reproduced. TRANSPORT: `cmp` of the committed `.agent/authored/f033-r19.md` and of `.agent/last_block.md` against the reviewer's OWN scratchpad original, both SILENT; `.agent/plan.md` byte-EQUAL to PLAN19 at 2740 bytes over 48 lines and `.agent/prose_slips.md` suffix-EQUAL to SLIPS19. RECORD19 is the exact SUFFIX of `.agent/live_review.md` AT `e057697d`, the commit that appended it, and is no longer the suffix at the branch tip because C6 legitimately appended the `Landed:` line after it — the worker read every append region at the commit that applied it and declared that the block's wording had not named those commits. THE RECORD APPEND at `e057697d` reconstructs 1555472 plus one newline plus 8021 to 1563494, base a byte PREFIX, slice an exact SUFFIX, N COUNTED at 2 over 709 blank-line units, and a negative control at byte 1558370 — proved to lie inside the FIRST appended paragraph, spanning 1555473 to 1561267, exactly the span the block stated — REJECTED by both readers run INDEPENDENTLY, each of which accepted the unflipped file. THE LEDGER, read at four commits: registered 306 to 307 with the ADDED id exactly `R-0746`; `Done:` 50 lines over 48 distinct UNMOVED throughout, this round resolving nothing; `Landed:` 17 to 18 with the ADDED id exactly `R-0746` and no `Done:` line beside it, which is correct because a resolution is the reviewer's text; `^Gate: F033 R18 — ` 0 before and exactly 1 after; distinct `DECISION F033 D` ids 5 UNMOVED; the open set 258 to 259; and `- R-0738` still registered with no `Done:` line at every one of the four readings. THE CODE IS BETTER THAN THE SPEC ORDERED IT. `_task_lines` in `packages/orchestration/run_report.py` appends the clause only when `APPLY_STATE_LABELS` knows the state, so an unrecorded state renders the line byte for byte as before; the attach re-reads `job.tasks` for FULL ids and pairs them positionally, never keying on the truncated `TaskOutcome.task_id`; and the worker added a length-agreement guard the SPEC never ordered — when the two iterations disagree it attaches NOTHING rather than guessing an alignment, which is the honest answer and the one a positional pairing needs. THE MUTATIONS were re-run by the reviewer in its own disposable worktree at `d4a21259` with its OWN anchors, each asserted UNIQUE, both files restored and PROVED byte-identical against the committed blob: unmutated control 81 passed at REAL exit 0; dropping the clause from the task line is exit 1 at 6 failed, the four state assertions plus the two that also read the rendered clause, with the unchanged-line assertion STILL GREEN; keying the attach on the TRUNCATED id is exit 1 at EXACTLY 1 failed, and that one is the truncation test, so the design risk the block named is pinned by one test and by nothing else; and deleting the new entry from the `Public API::` block is exit 1 at 1 failed, the guard that holds R-0746's fix. THE REVIEWER ALSO RAN A CHECK THE BLOCK NEVER ORDERED, aimed at the round's central constraint rather than at its code: making an UNRECORDED apply state render a clause reddens all THREE golden full-text report fixtures, plus the unchanged-line and unknown-state assertions — so the claim that a job with no proof chain still gets its old report byte for byte is enforced by real documents and not merely asserted in the block. THE SUITES were re-run SERIALLY in the primary checkout, every REAL exit 0: `test_run_report.py` 81 passed against a base of 71, `test_proof_chain.py` 104, the contract file 20, the cockpit truth 39, `tests/cli/test_job_report.py` 30 and the canary 42, with `ruff` exiting 0 over the three changed files. THE STRUCTURE: ten single-parent commits over `41b83021`..`d4a21259` of 351, 215, 17, 4, 4, 112, 154, 51, 299 and 14 insertions, every one under 500; the path set over the WHOLE range EQUALS the declared change set in BOTH directions; and all sixteen do-not-touch paths blob-identical at both ends. TEN DEVIATIONS were declared and all ten are honest. THE FIRST OF THEM IS A REAL DEFECT IN THE REVIEWER'S BLOCK AND THE WORKER WAS RIGHT TO REFUSE IT AS WRITTEN: SPEC C1 ordered one docstring line and called it "the whole fix" while SPEC C2 ordered a guard asserting that EVERY public module-level function is named, and those two cannot both hold, because `packages/orchestration/proof_chain.py` had SIX public functions and not five. The worker wrote the guard first, ran it against C1 applied literally, got a REAL exit 1 naming both missing entries, and added the second line rather than ship a red gate or weaken the guard. The reviewer confirms by its own AST walk at three commits: at `2a938b5e` the module had five public functions with `derive_next_safe_action_from_changes` ALREADY unlisted, at `41b83021` six with two unlisted, and at `d4a21259` six with none unlisted. R-0746's own resolution clause asked for exactly what the worker did, so the block's narrower FIX clause was the half that was wrong. Recorded as a prose slip, and corrected in that finding's resolution below.

Done: R-0738 — RESOLVED. A task whose changes disagree now renders as PARTIAL on all three surfaces the finding names, and each surface is pinned by a test that BUILDS the mixed case explicitly rather than observing whatever a fixture produced, which is what this finding's own resolution clause required. THE FOLD, at `eb4c697d`: `_task_truth_maps` stopped answering by membership and now agrees or says `partial`, so a task holding eight changes of which one applied is no longer indistinguishable from a task all eight of which applied — the defect this finding was raised for. THE VIEWER BADGE, at `eb4c697d`: `applyStatus` in `apps/ui/src/components/detail/DetailPopover.tsx` labels that value "Partially applied", and `tests/ui_contracts/test_apply_state_partial.py` derives the backend's emittable set from the SHIPPED fold's AST and requires the popover to branch on every member, so a fifth state added on one side alone reddens a test instead of reaching an operator as "Unknown". THE NODE, at `81817cb8`: DECISION F033 D5 ruled the treatment onto the tasks-card row rather than onto a widened `RemedyState`, because `docs/ui/design_reference/ux_spec.md` section 11 item 4 is the only partial-apply treatment the canonical design reference specifies; `iconFor` and `stateText` in `apps/ui/src/components/panels/TaskChecklistCard.tsx` read `applyStatus` BEFORE the lifecycle state, so a finished task whose changes half landed shows the blue filled check tile and reads "Partially applied" instead of "Done". THE REPORT LINE, at `cd7cd9c0`: `packages/orchestration/run_report.py` held no reference to apply state at all before this feature; `TaskOutcome` now carries the folded state with the APPLIED and TOTAL counts, and `_task_lines` renders "partially applied (5/8 changes)" — the wording the feature file's Design named — while an UNRECORDED state still renders the line byte for byte as before, which three golden full-text fixtures enforce. THE THREE SURFACES CANNOT DRIFT APART, which is the property that makes this resolvable rather than merely done: the shared fold moved to `packages/orchestration/proof_chain.py` at `ed10b57a` so the cockpit and the report read ONE implementation, and the reviewer proved the move changed nothing by driving the shipped function over 157 task shapes at the commit before and the commit after, with zero differing answers; one test asserts the card and the popover spell the state with the SAME string; and the seam guard derives its expected set from the fold's AST rather than restating it. EVERY READING IN THIS PARAGRAPH WAS RE-RUN BY THE REVIEWER at the gate of the round that produced it, each in its own disposable worktree with its own anchors, and each mutation's colour was ordered before its count.

Done: R-0746 — RESOLVED, at `191da989`, and this resolution CARRIES A CORRECTION OF THE FINDING'S OWN TEXT rather than rewriting it, because that record is append-only. THE FIX: the `Public API::` block of `packages/orchestration/proof_chain.py` now names `fold_task_apply_states`, and a guard in `tests/orchestration/test_run_report.py` walks the module's AST for every public module-level function and asserts each is named there, so the list is now checked by reading it against the module rather than by having been typed once. The reviewer proved the guard discriminates: deleting the new entry reddens exactly that test. THE CORRECTION: the finding above says "Round 18 added a FIFTH public function to the module", and that numeral is WRONG. Measured by the reviewer by walking the AST at three commits: `packages/orchestration/proof_chain.py` held FIVE public module-level functions at `2a938b5e`, before round 18 touched it, and `derive_next_safe_action_from_changes` was ALREADY absent from the list at that commit; round 18 added a SIXTH, not a fifth, and left TWO unlisted rather than one. The defect was therefore OLDER and WIDER than the finding that reported it, and the reviewer produced that error by counting the module's public functions from the docstring list it was accusing of being incomplete — reading the accused list as the census of the thing it was failing to describe. The consequence reached the block: its FIX clause ordered one line and called it the whole fix while its guard clause required all of them, and those two could not both hold. The worker measured the contradiction, wrote the guard first, and added both lines; the finding's Resolved clause — "names every public function the module defines, checked by reading the two against each other" — is what it satisfied, and that clause was right where the FIX clause was wrong.
<<<END RECORD20>>>

<<<BEGIN SLIPS20 target=.agent/prose_slips.md mode=append bytes=1622 sha256=0d0130886ab67db31061a36ae4f4b7ad7808c87467e58bf4f6da82c33ddfffa4>>>
2026-08-29 · F033 R19 · The block's SPEC C1 ordered one docstring line and called it "the whole fix" while its SPEC C2 ordered a guard asserting that EVERY public module-level function is named in that list, and the two could not both hold, because `packages/orchestration/proof_chain.py` had six public functions and not five; the root cause is that the reviewer counted the module's public functions from the very docstring list it was accusing of being incomplete, instead of walking the module — a census taken from the accused, which is how finding R-0746 also landed with a wrong numeral, corrected in its resolution rather than by a rewrite.

2026-08-29 · F033 R19 · The block's G2 said to "extract its applied region from its target file" without naming the COMMIT the region is read at, and this round legitimately appended a `Landed:` line to `.agent/live_review.md` after the slice, so the slice stopped being the file's suffix at the branch tip while remaining exactly the suffix at the commit that applied it; the worker read each region at its own commit and declared the ambiguity, and an append gate should name the commit it is measured at whenever the same round writes to that file twice.

2026-08-29 · F033 R19 · The block's SPEC A2 told the worker to "build the chain the same way the rest of this module reaches evidence" without naming the two imports that takes — `resolve_data_root` and `load_run_events` — so the worker had to find them and declared the gap; a SPEC that points at a pattern rather than naming the calls leaves the worker to rediscover what the reviewer already read.
<<<END SLIPS20>>>

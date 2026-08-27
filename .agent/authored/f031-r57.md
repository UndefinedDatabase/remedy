── STEP RESOLUTION SWEEP / F031 — ROUND R57 ───────────────────────────
Goal:        Resolve R-0695, R-0697, R-0698 and R-0699, whose code halves landed
             at R44 and R48 and whose shared process half landed at R56, on
             evidence the reviewer measured itself at this gate. Record the R56
             verdict, which PASSED on every gate. Widen §3 item 35 from a MISSING
             list item to a WRONG round label, because the R56 block reproduced
             R-0704's class inside the very slice that landed that item. NO
             PRODUCTION CODE CHANGES. NO ID IS MINTED THIS ROUND.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the plan
             · C2 the R56 gate entry and the four resolutions · C3 the item 35
             widening · C4 handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f031-r57.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `docs/agents/planner_reviewer_prompt.md`, `.agent/handoff.md`.
             NOTHING UNDER `apps/`, `packages/` OR `tests/`, and no file under
             `docs/` other than the one named — in particular nothing under
             `docs/roadmap/`, which AGENTS.md puts behind an explicit operator
             request. `.agent/decisions.md` is not in it either: no decision is
             ruled this round.

Constraints:
 1. EVERY SLICE IS APPLIED BYTE FOR BYTE. Never retype one, never reflow one,
    never fix one. A slice's text is its content lines joined with a newline
    plus ONE trailing newline. If a slice looks wrong, say so in the handback
    and finish the round anyway — a corrected slice destroys the transport
    proof.
 2. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4. No pair may be
    reordered and none may be merged.
 3. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES R56. That is
    ordered: the plan becomes current at C1.
 4. EVERY SLICE IS THE REVIEWER'S TEXT. You never write a `Done:` paragraph of
    your own and never mint a finding id. LEDGER57 carries the R56 gate entry
    and the four resolutions this round lands, and you add nothing to it.
 5. THE LEDGER SETS MOVE ONCE, AND THIS ROUND RESOLVES FOUR FINDINGS AND MINTS
    NO ID. Across C2 `^- R-\d+ — ` stays 265 with the ADDED id set EMPTY;
    `^Done: R-\d+ — ` moves 8 to 12 with the ADDED set exactly R-0695, R-0697,
    R-0698 and R-0699; `^Gate: F\d+ R\d+ — ` moves 37 to 38 with the ADDED key
    exactly `F031 R56`; `^Landed: R-` stays 0 and `^Gate: R\d+ — ` stays 19. The
    open set is 257 before C2 and 253 after C2.
 6. RE-READ `.agent/STOP` FROM DISK before C0a and again before C4. If it exists
    at either reading, finish the commit in hand, write the handback and STOP.
    Never create it, never delete it.
 7. NOTHING DESTRUCTIVE IS ORDERED THIS ROUND. Create no worktree; the primary
    checkout reads `git status --porcelain` 0 lines at every commit. The red
    controls this round's resolutions quote were run by the REVIEWER, in a
    disposable worktree that is already removed; you re-run none of them.
 8. THE S1 PAIR IS AN APPEND, MEASURED AND NOT ASSERTED. The reviewer ran the
    containment test before emission and its output is `TO contains FROM: true`,
    so the §4.9 APPEND obligation governs it and a FROM-zero count is
    unattainable by construction. Never report one for this pair.
 9. YOUR HANDBACK'S CAP. AGENTS.md gives 60 lines at most, or 100 at most when
    per-commit tables of MORE THAN FIVE commits require it. Count the commits
    the Bundle above orders and derive your cap from that count yourself. If the
    MANDATED content genuinely does not fit, write the DECISION D15 "Deviations,
    declared" line naming your actual line count and the specific mandated
    content that caused the overage. Do not invent a tier.
10. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `cp`, brace literals containing a quote character, `cd x && y`,
    and every form of environment assignment. Route anything that counts, hashes
    or compares through a quoted python heredoc, read real exit codes from
    `subprocess.run(...).returncode`, and pass `cwd=` rather than `cd`. Run
    pytest SERIALLY — never two pytest processes alive at once. `--timeout` IS
    NOT AVAILABLE to pytest here: passing it exits 4 and reports no failure.

Spec — the one edit to `docs/agents/planner_reviewer_prompt.md`, at C3:
 S1. REPLACE the single occurrence of S4NEW's own FIRST LINE with the WHOLE of
     S4NEW. That first line is the last line of §3 item 35's body, and the
     reviewer measured it as occurring exactly 1x in that file at `941b8966`.
     S4NEW begins with that line verbatim and continues item 35's body at the
     same six-space indent, so the result is one longer item 35 and no new
     numbered item: renumber nothing, add nothing of your own, and do not insert
     a blank line anywhere in what you apply.

Done when — run every gate yourself and record its REAL exit code. G1 through G8
run at commits STRICTLY EARLIER than C4, so the handback can quote them; the
push is ordered after C4 and its reading is NOT written into the handback. Read
every non-current revision with `git show <rev>:<path>` into memory; never write
a past blob over a tracked file to read it.
 G1. BRANCH, CLEANLINESS, TRANSPORT. Branch is `feature/f031-decision-inbox`.
     `git status --porcelain` prints 0 lines after each of C0a, C0b, C1, C2 and
     C3. `.agent/STOP` read from disk before C0a and before C4, both ABSENT.
     Report the sha256, byte count and line count of this block as saved at C0a,
     as mirrored at C0b, and as read off disk at C3 — all three must be EQUAL —
     and say whether C0a and C0b are the same git blob.
 G2. EXTRACTION AND CAPS. Extract the slices from the COMMITTED C0a blob by
     their marker LINES, never from the prompt. Report how many slices your
     extractor printed, the CONTENT line total, the TOTAL line count, and PROSE
     as TOTAL minus CONTENT. MARKERS ARE PROSE. PROSE must be at most 400 and
     TOTAL at most 490.
 G3. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF031R57 under the
     newline-INCLUDED convention. Run the negative control against the slice
     MINUS its trailing newline and report it FALSE. Report `^## Goal$` 1,
     `^## Next Steps$` 1, and `wc -l` STRICTLY UNDER 50.
 G4. THE APPEND, PROVED TWICE, THE SECOND READER COVERING THE WHOLE APPENDED
     REGION. `.agent/live_review.md` at C2 equals its pre-commit blob plus ONE
     newline plus LEDGER57. The reviewer measured the base blob at `941b8966`
     itself: `.agent/live_review.md` is 923830 bytes. If it reads differently
     before C2, something moved that this round did not order — stop and hand
     back. Report both byte counts and the sum. Then confirm with a SECOND,
     independent reader: split the whole file on blank lines, let N be the number
     of paragraphs YOUR SCRIPT COUNTS in that slice — never a number this block
     asserts — and compare the LAST N units of the file against the slice's N
     paragraphs IN ORDER. Report N and the unit count before and after. THE
     NEGATIVE CONTROL GOES ON THE FIRST APPENDED PARAGRAPH, which is the
     position a tail-only reading cannot see: flip ONE byte IN MEMORY inside
     paragraph 1 and report that BOTH readers REJECT it. Never mutate the
     tracked file.
 G5. THE LEDGER SETS. Report at two points — before C2 and after C2 — the
     line-anchored counts of `^- R-\d+ — `, `^Done: R-\d+ — `, `^Landed: R-`,
     `^Gate: R\d+ — ` and `^Gate: F\d+ R\d+ — `, plus the finding ids, the
     RESOLVED ids and the gate keys ADDED and REMOVED as SETS, whether all ids
     are DISTINCT, and the maximum id. Every movement constraint 5 names is
     checked here, INCLUDING the ones that must NOT move. Report the open set at
     both points, and report that every id in the ADDED resolved set also occurs
     as a `^- R-\d+ — ` paragraph in the same file — a resolution of a finding
     the record does not hold would be worse than no resolution at all.
 G6. THE PAIR. At the base `941b8966` report the count of S4NEW's own FIRST LINE
     in `docs/agents/planner_reviewer_prompt.md`, which must be 1, and the count
     of `^  36\. \*\*`, which must be 0. Report the containment test's own output
     for this pair, which constraint 8 fixes as `TO contains FROM: true`, and
     order NO FROM-zero count. At C3: S4NEW occurs 1x, its first line still
     occurs 1x, `^  36\. \*\*` occurs 0x, and each TO-ONLY line of S4NEW — every
     line of it except that shared first line — occurs exactly 1x AMONG THE LINES
     THAT COMMIT'S DIFF ADDS. Report the file's line count at the base and at C3
     and confirm the difference is exactly S4NEW's own line count MINUS ONE,
     which you measure from the slice rather than from this block. Report that
     `git diff --name-only C2..C3` is that one path and nothing else, and that
     the diff for that path has ZERO deleted lines.
 G7. NOTHING ELSE MOVED, MARKERS, PATHS, COMMITS. Compare the path set of
     `git diff --name-only 941b8966..C3` BOTH WAYS against this round's expected
     set — the Change line's list MINUS `.agent/handoff.md`, excluded because
     the handback is written at C4, outside a range ending at C3 — and report
     both residues EMPTY. Report `git diff --stat 941b8966..C3` restricted to
     `apps/`, `packages/`, `tests/` and `docs/roadmap/` and confirm each is
     EMPTY. Line-anchored `^<<<SLICE ` and `^<<<END ` are 0 and 0 in
     `.agent/plan.md` at C1, `.agent/live_review.md` at C2 and
     `docs/agents/planner_reviewer_prompt.md` at C3, against a CONTROL count
     over the C0a blob, which is not 0. Report each commit's insertions from
     `git diff --numstat` for C0a through C3, confirm each is single-parent and
     under 500. Report `git ls-files .remedy-wt` as 0 lines, `git worktree list`
     as 1 line, and `git ls-files --others --exclude-standard` as 0 lines at C3.
 G8. THE DOCS READERS, THE CANARY AND THE STATE READERS. In the PRIMARY checkout
     at C3, run SERIALLY — never two pytest processes alive at once — reporting
     each REAL exit code and count: `python3 -m pytest tests/docs/ -q`,
     `tests/test_agent_tooling.py`, `tests/orchestration/test_role_conventions.py`,
     `tests/cli/test_golden_path.py` (the canary), `tests/ui_server/`,
     `tests/orchestration/test_test_runner.py`,
     `tests/regression/test_resource_safety.py` and
     `tests/orchestration/test_integrity_gate.py`. At `941b8966` the reviewer
     measured these itself at 295, 10 passed with 1 skipped, 35, 42, 489, 52, 21
     and 16, every one at exit 0. THE FIRST THREE ARE THE ONES THAT READ
     `docs/agents/`, so they are the ones this round could actually move; any
     movement in them is unexplained and you stop and hand back.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C4: feature and round, branch, the per-commit changed-files table
             with the `+/-` column taken from `git diff --numstat` ITSELF and
             agreeing cell for cell with G7's readings, the item-status table
             covering C0a, C0b, C1, C2, C3, C4 and the push, ONE LINE PER GATE
             for G1 through G8 with its real exit code, the open-findings count
             AFTER this round, and the next expected action. SAY PLAINLY THAT NO
             PRODUCTION CODE CHANGED, THAT THE ONLY `docs/` FILE TOUCHED IS THE
             REVIEWER PROMPT, WHICH FINDING IDS THIS ROUND RESOLVED, AND THAT NO
             ID WAS MINTED. THE NEXT ACTION SECTION NAMES, IN THIS ORDER: re-read
             `.agent/STOP` from disk first, then the Open PR Gate, then review
             this round's handback, then the round that measures the widened §3
             item 35 on disk and resolves R-0704 while landing the item R-0694's
             fix clause asks for, and only then the COMPONENT half of the markup.
             Name no round number for those two: this workflow has twice had a
             pre-assigned label go stale, and item 35 as widened by this round
             forbids it. Obey constraint 9's cap. Then push with
             `git push origin feature/f031-decision-inbox`.
──────────────────────────────────────────────────────────────────────

<<<SLICE PLANF031R57
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1-D26.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R57 is the resolution sweep. R-0695, R-0697, R-0698 and R-0699 carry code halves
that landed at R44 and R48 and process halves that landed at R56, and every one
of the four is measured on disk at this gate — each with an unmutated control
and a mutation that names the guard the fix created — and resolved. The round
also widens §3 item 35 from a MISSING list item to a WRONG round label, because
the R56 block reproduced R-0704's class inside the very slice that landed that
item's first half.

## Next Steps
1. R-0704 stays OPEN until its widened counter-measure has been measured on
   disk at a later gate, rather than being resolved by the round that writes it.
   That round also carries the item R-0694's own fix clause asks for, which
   states R-0631's append-reader rule.
2. The COMPONENT half: the pending card renders a field per open clarification
   and the flow carries the map R53 built.
   `tests/ui_contracts/test_decision_answer_wiring.py` pins the card's call
   string and its two-writer count, so that round moves those guards with it.
3. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- SIX OF THE EIGHT PRODUCING TYPES STILL CANNOT BE ANSWERED THROUGH THE DOOR.
  R-0693 measures the gap; the rest are outside F031's scope, and the inbox
  tells the truth about every one of them rather than offering a refused button.
- THIS FILE NAMES NO ROUND NUMBER IT HAS NOT BEGUN. Twice a pre-assigned label
  went stale the moment a round was inserted ahead of it; a step is named by
  what it does, and its number is knowable only when it starts.
- THE FORM IS REACHABLE ONLY BY A NON-BROWSER CLIENT until the component half
  lands. R53 moved the seam to the edge of the markup and no further.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 257 at `941b8966`
  and the four resolutions this round lands take it to 253.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R57

<<<SLICE LEDGER57
Gate: F031 R56 — the F031 R56 entry. R56 PASSED ON EVERY GATE ITS BLOCK ORDERED, G1 THROUGH G8, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk. THIS WAS THE SECOND CHECKLIST HALF: no production file changed, and the only `docs/` path it touched is `docs/agents/planner_reviewer_prompt.md`, which gained §3 items 34 and 35. TRANSPORT HELD: the C0a and C0b blobs are byte-identical at sha256 `e7ad33b5…0264a2bc` over 24076 bytes and 293 lines, resolve to the SAME git blob `af0b07059b4b`, and the working copy at `941b8966` matches both; the extraction printed 4 slices with CONTENT 113 and TOTAL 293, so PROSE 180 against 400 and TOTAL 293 against 490. THE PLAN at `0799371f` is byte-equal to PLANF031R56 with the minus-newline control FALSE, `^## Goal$` 1, `^## Next Steps$` 1 and `wc -l` 48. THE APPEND IS EXACT: 920032 + 1 + 3797 = 923830 and the committed blob is 923830; N counted by the reviewer's own script is 1, units 373 to 374, the last unit matches the slice's paragraph, and a byte flipped IN MEMORY inside it is REJECTED by BOTH readers — with N at 1 the whole appended region IS the first paragraph, so the two readers agree by construction rather than by independent reach, which the worker declared and this entry records. THE SETS MOVED EXACTLY WHERE CONSTRAINT 5 ALLOWED AND NO ID WAS MINTED: `^- R-\d+ — ` 265 to 265 with the ADDED id set EMPTY, `^Gate: F\d+ R\d+ — ` 36 to 37 with the ADDED key exactly `F031 R55`, `^Done: R-\d+ — ` 8, `^Landed: R-` 0 and `^Gate: R\d+ — ` 19 all unmoved, ids DISTINCT with the maximum still `R-0704`, and the open set 257 at both points. THE CHECKLIST EDIT IS AN INSERTION AND NOTHING ELSE: at `58de811a` the anchor line occurs 1x and `  34. **` and `  35. **` 0x over 993 lines; at `c49ba739` S2NEW and S3NEW occur 1x each, the anchor still 1x, `^  34\. \*\*` and `^  35\. \*\*` 1x each and `^  36\. \*\*` 0x over 1057 lines, S2NEW ends exactly where S3NEW begins and S3NEW exactly where the anchor begins, the delta 64 equals 36 plus 28 measured from the slices, and that commit's numstat reads 64 and 0. NOTHING ELSE MOVED: both path residues EMPTY over the expected path set, `apps/`, `packages/`, `tests/` and `docs/roadmap/` each EMPTY in the range, markers 0 and 0 in the plan, the ledger and the reviewer prompt against a CONTROL of 4 and 4, insertions 293, 162, 20, 2 and 64 with each commit single-parent and under 500, `git ls-files .remedy-wt` 0 lines, `git worktree list` 1 line and no untracked path at all. THE READERS THE REVIEWER RE-RAN SERIALLY, every one at a REAL exit 0 and every one EQUAL to the base reading: `tests/docs/` 295, `tests/test_agent_tooling.py` 10 passed with 1 skipped, `tests/orchestration/test_role_conventions.py` 35, the canary 42, `tests/ui_server/` 489, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21 and `tests/orchestration/test_integrity_gate.py` 16. ONE CORRECTION TO THE REVIEWER'S OWN PRE-EMISSION MEASUREMENT, dated rather than hidden: the R56 block was measured before emission at 291 lines by summing separately-counted chunks, and the committed block is 293 with a frame of 168 where that sum read 166, so the reviewer's own arithmetic was two low. No cap was breached — 293 against 490 and 180 against 400 — but a summed count is not a measured one, and the block that lands a checklist item about reading before ordering is the wrong place to learn it. THE SECOND OBSERVATION IS A DEFECT IN THE R56 BLOCK'S OWN PLAN SLICE, FOUND BY THE REVIEWER AT THIS GATE, AND IT REPRODUCES R-0704'S CLASS FOR THE THIRD TIME: PLANF031R56's `## Next Steps` gave item 1 to an unnumbered resolution sweep and labelled item 2 `R57`, while the sweep IS a round and takes R57, so the markup is R58. NO NEW ID IS MINTED, per §3 item 30 — R-0704 is OPEN and describes exactly this class — and R-0704 STAYS OPEN, because the counter-measure it names has now failed once under itself: item 35 as landed catches an item the list does not hold and not a label the list holds in the wrong position. This round widens item 35 to reach it, and the finding closes only when that widening has been measured on disk at a later gate. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing table, no unverified completion claim and no silent scope change.

Done: R-0695 — RESOLVED AT F031 R57 BY MEASUREMENT AT THIS GATE, the fix itself having landed at R44. `_answerable_by_decision_resolve` no longer tests existence alone: `packages/orchestration/decision_inbox.py` at `941b8966` returns `record is not None and record.get("status") == ESCALATION_STATUS_OPEN` for every non-`fp:` id, which is exactly the pair of conditions `escalation.answer_task_decision` enforces, and the helper's docstring names R-0693 for the first reading and R-0695 for the second. THE FIX IS PROVED REACHED RATHER THAN MERELY PRESENT, which a passing suite cannot show: in a disposable worktree at `941b8966` the UNMUTATED control is a REAL exit 0 at 35 passed, and with the OPEN condition removed — the exact state this finding recorded — `tests/orchestration/test_decision_inbox.py` exits 1 at 1 failed and 34 passed, the single failure being `test_answerable_key_goes_false_once_the_decision_has_been_answered`, the test written to catch it. THE PROCESS HALF LANDED SEPARATELY, at R56 C3, as §3 item 34: a block that computes a value from another module's predicate reads that predicate's OWN refusal conditions and not merely its route to the data. Both halves are on disk, so this closes.

Done: R-0697 — RESOLVED AT F031 R57 BY MEASUREMENT AT THIS GATE, the fix having landed at R48. `TestCommandDoorImportGuard.ALLOWED_IMPORTS` in `tests/ui_server/test_command_channel.py` at `941b8966` holds `("packages.orchestration.flight_plan", "open_clarification_questions")` and `("packages.orchestration.flight_plan", "resolve_flight_plan_approval")`, each annotated `# F031 D24` — the mechanism the guard's own comment documents, which is that an entry is there because a ruled DECISION puts it there, rather than an exception to it. THE RED TIP IS GONE AND THE REVIEWER RE-RAN IT ITSELF: `python3 -m pytest tests/ui_server/ -q` is exit 0 at 489 passed in the primary checkout, where this finding recorded exit 1 at 1 failed and 479 passed. THE GUARD IS PROVED STILL LOAD-BEARING rather than merely satisfied: with the `resolve_flight_plan_approval` entry deleted inside a disposable worktree at `941b8966` the file exits 1 at 1 failed and 105 passed against an unmutated control of a REAL exit 0 at 106 passed, and the failure is `test_the_door_imports_exactly_the_allowed_set` itself — so the allowed set really is compared against the door's real imports and did not merely grow to fit them. THE PROCESS HALF IS §3 item 34, landed at R56 C3.

Done: R-0698 — RESOLVED AT F031 R57 BY MEASUREMENT AT THIS GATE, the fix having landed at R48. `ANSWERABLE_DECISION_TYPES` in `tests/orchestration/test_decision_inbox.py` at `941b8966` reads `("flight_plan_approval", "task_decision")`, and the resolved case this finding says a type check cannot express has its own sibling test rather than a tuple entry — which is the correction this finding made to the worker's analysis, now on disk rather than only in the record. THE CONSTANT IS PROVED COMPARED rather than decorative: reverted to `("task_decision",)` inside a disposable worktree at `941b8966` the file exits 1 at 1 failed and 34 passed against an unmutated control of a REAL exit 0 at 35 passed, and the failure is exactly `test_answerable_key_matches_what_the_write_door_accepts[flight_plan_approval]`, the parameter this finding predicted would go red. THE PROCESS HALF IS §3 item 34, landed at R56 C3: a block reads the CONSTANT a parametrized test compares its changed behaviour against.

Done: R-0699 — RESOLVED AT F031 R57 BY MEASUREMENT AT THIS GATE, the tests having landed at R48. The door's `fp:` dispatch is no longer untested: `tests/ui_server/test_command_channel.py` at `941b8966` names it in `test_an_fp_approval_answered_approve_is_accepted`, `test_an_fp_approval_answered_reject_is_accepted`, `test_an_fp_approval_on_a_plan_that_is_not_pending_is_409`, `test_an_fp_approval_answering_an_unknown_question_id_is_409`, `test_an_fp_approval_whose_answers_are_not_a_map_is_409` and `test_an_fp_approval_answered_with_a_next_action_string_is_409`, while the EFFECTS sit in `tests/ui_server/test_command_dispatch.py` as `test_an_accepted_fp_approval_really_resolved_the_plan` and `test_the_accepted_fp_approval_saves_the_job_exactly_once` — split by the boundary their own docstrings draw, which is what this finding's fix clause ordered. THE RED CONTROL R47 COULD NOT RUN HAS NOW BEEN RUN, and that is what makes this a resolution rather than a claim: with the door's refusal clause `if not isinstance(fp, dict) or fp.get("_approval") != "pending":` replaced by `if False:` inside a disposable worktree at `941b8966`, `tests/ui_server/` exits 1 at 1 failed and 488 passed against an unmutated control of a REAL exit 0 at 489 passed, and the failure is `test_an_fp_approval_on_a_plan_that_is_not_pending_is_409` — the guard that clause exists for. THE PROCESS HALF IS §3 item 35, landed at R56 C3.
<<<END LEDGER57

<<<SLICE S4NEW
      missing the thing the paragraph beside it promised.
      The recurrence at R56 widens this item from a MISSING item to a WRONG LABEL, and
      it is why the item is not yet a habit: the R56 block landed this very
      counter-measure while its own PLANF031R56 slice reproduced the class inside the
      same commit range. That slice's `## Next Steps` gave item 1 to an unnumbered
      resolution sweep and labelled item 2 `R57`, while the sweep IS a round and takes
      R57, so the markup is R58 and the label was wrong the moment it was written —
      the same arithmetic as the R55 instance, one round later, under the rule written
      to stop it. A state slice therefore assigns a round NUMBER to the round it is
      written FOR and to no other: a step not yet begun is named by what it DOES, and
      the number it will carry is not knowable while any step ahead of it can still be
      inserted, split or dropped. The prose-versus-list reading above catches an item
      the list does not hold; only this one catches a label the list holds in the
      WRONG POSITION, because there the list is complete, correctly ordered, and every
      sentence about it is true except the numeral — which is the half no reader
      re-derives, since deriving it means counting the rounds that have not happened.
<<<END S4NEW

STEP CHECKLIST ROUND / F031 — ROUND R59
Goal:        Land the two §3 checklist items the open set is waiting on: the
             append-reader rule R-0631 wrote as finding prose and R-0694 asks
             for as an item of its own, and R-0705's two-part transport rule.
             Record the R58 verdict, which PASSED on every gate the reviewer
             re-ran. NO PRODUCTION CODE, no `docs/roadmap/` file, no decision.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the plan
             · C2 the R58 gate entry · C3 the two new §3 items · C4 handback ·
             then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f031-r59.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `docs/agents/planner_reviewer_prompt.md`, `.agent/handoff.md`.
             NOTHING UNDER `apps/`, `packages/` or `tests/`, and nothing under
             `docs/roadmap/`. `.agent/decisions.md` is not in it either.

Constraints:
 1. EVERY SLICE IS APPLIED BYTE FOR BYTE. Never retype one, never reflow one,
    never fix one. A slice's text is its content lines joined with a newline
    plus ONE trailing newline. If a slice looks wrong, say so in the handback
    and finish the round anyway — a corrected slice destroys the transport
    proof.
 2. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4. No pair may be
    reordered and none may be merged.
 3. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES R58. That is
    ordered: the plan becomes current at C1.
 4. EVERY SLICE IS THE REVIEWER'S TEXT. You never write a `Done:` paragraph of
    your own and never mint a finding id. LEDGER59 carries the R58 gate entry
    and nothing else. NO FINDING IS RESOLVED THIS ROUND: the items C3 lands are
    the fixes R-0631, R-0694 and R-0705 are waiting for, and a resolution is
    written by the round that can name the commit holding them.
 5. THE LEDGER SETS MOVE ONCE. Across C2 `^Gate: F\d+ R\d+ — ` moves 39 to 40
    with the ADDED key exactly `F031 R58`. `^- R-\d+ — ` stays 266,
    `^Done: R-\d+ — ` stays 13, `^Landed: R-` stays 0 and `^Gate: R\d+ — `
    stays 19. The open set is 253 before C2 and 253 after C2.
 6. THE S1 PAIR IS AN APPEND, MEASURED AND NOT ASSERTED. The reviewer ran the
    containment test before emission and its output is `TO contains FROM: true`,
    so the §4.9 APPEND obligation governs it and a FROM-zero count is
    unattainable by construction. Never report one for this pair. The added
    lines are NOT all distinct — two of them are blank — so the obligation is
    ORDERED EQUALITY and never a per-line count.
 7. RE-READ `.agent/STOP` FROM DISK before C0a and again before C4. If it exists
    at either reading, finish the commit in hand, write the handback and STOP.
    Never create it, never delete it.
 8. NOTHING DESTRUCTIVE IS ORDERED THIS ROUND. Create no worktree; the primary
    checkout reads `git status --porcelain` 0 lines at every commit.
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
 S1. REPLACE the single occurrence of S36NEW's own FIRST LINE with the WHOLE of
     S36NEW. That first line is the last line of §3 item 35's body, and the
     reviewer measured it as occurring exactly 1x in that file at `97b79145`.
     S36NEW begins with that line verbatim, then a blank line, then two new
     numbered items at the same two-space label indent and six-space body indent
     the neighbouring items use. The line that FOLLOWS the anchor in the file is
     blank and the one after it opens the paragraph beginning "Why this is on
     disk and not a habit", and both stay exactly where they are: renumber
     nothing, add nothing of your own, and delete nothing.

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
     and say whether C0a and C0b are the same git blob. Report also whether any
     line of the block as saved is a run of a single repeated character, which
     must come back as none. THEN STATE IN ONE SENTENCE WHAT THIS PROOF COVERS:
     the saved copy, its mirror and the working copy, all three your own output,
     and NOT the bytes that were emitted to you. That sentence is the second
     half of the rule S36NEW lands, obeyed by the block that lands it.
 G2. EXTRACTION AND CAPS. Extract the slices from the COMMITTED C0a blob by
     their marker LINES, never from the prompt. Report how many slices your
     extractor printed, each slice's own line count, the CONTENT line total, the
     TOTAL line count, and PROSE as TOTAL minus CONTENT. MARKERS ARE PROSE.
     PROSE must be at most 400 and TOTAL at most 490.
 G3. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF031R59 under the
     newline-INCLUDED convention. Run the negative control against the slice
     MINUS its trailing newline and report it FALSE. Report `^## Goal$` 1,
     `^## Next Steps$` 1, and `wc -l` STRICTLY UNDER 50.
 G4. THE APPEND, PROVED TWICE, THE SECOND READER COVERING THE WHOLE APPENDED
     REGION. `.agent/live_review.md` at C2 equals its pre-commit blob plus ONE
     newline plus LEDGER59. The reviewer measured the base blob at `97b79145`
     itself: `.agent/live_review.md` is 941584 bytes. If it reads differently
     before C2, something moved that this round did not order — stop and hand
     back. Report both byte counts and the sum. Then confirm with a SECOND,
     independent reader: split the whole file on blank lines, let N be the number
     of paragraphs YOUR SCRIPT COUNTS in that slice — never a number this block
     asserts — and compare the LAST N units of the file against the slice's N
     paragraphs IN ORDER. Report N and the unit count before and after. THE
     NEGATIVE CONTROL GOES ON THE FIRST APPENDED PARAGRAPH: flip ONE byte IN
     MEMORY inside paragraph 1 and report that BOTH readers REJECT it. Never
     mutate the tracked file.
 G5. THE LEDGER SETS. Report at two points — before C2 and after C2 — the
     line-anchored counts of `^- R-\d+ — `, `^Done: R-\d+ — `, `^Landed: R-`,
     `^Gate: R\d+ — ` and `^Gate: F\d+ R\d+ — `, plus the finding ids, the
     RESOLVED ids and the gate keys ADDED and REMOVED as SETS, whether all ids
     are DISTINCT, and the maximum id. Every movement constraint 5 names is
     checked here, INCLUDING the ones that must NOT move. Report the open set at
     both points.
 G6. THE PAIR. At `97b79145` the reviewer measured
     `docs/agents/planner_reviewer_prompt.md` at 1072 lines, with S36NEW's own
     FIRST LINE occurring 1x and line-anchored `^  36\. \*\*` and `^  37\. \*\*`
     both 0x. Take those four readings at the base yourself and report them.
     Then at C3 report: S36NEW occurs 1x, its first line still occurs 1x,
     `^  36\. \*\*` is 1, `^  37\. \*\*` is 1, and the file's line count, whose
     difference from the base must equal S36NEW's own line count MINUS ONE.
     Because constraint 6 fixes the pair as an APPEND, the obligation is ORDERED
     EQUALITY: report that the lines C3's diff ADDS are EXACTLY the lines of
     S36NEW after its first, IN ORDER, and report `git diff --numstat` for that
     commit beside it. Order and report NO FROM-zero count.
 G7. NOTHING ELSE MOVED, MARKERS, PATHS, COMMITS. Compare the path set of
     `git diff --name-only 97b79145..C3` BOTH WAYS against this round's expected
     set — the Change line's list MINUS `.agent/handoff.md`, excluded because
     the handback is written at C4, outside a range ending at C3 — and report
     both residues EMPTY. Report `git diff --stat 97b79145..C3` restricted to
     `apps/`, `packages/`, `tests/` and `docs/roadmap/` and confirm each is
     EMPTY. Line-anchored `^<<<SLICE ` and `^<<<END ` are 0 and 0 in
     `.agent/plan.md` at C1, in `.agent/live_review.md` at C2 and in
     `docs/agents/planner_reviewer_prompt.md` at C3, against a CONTROL count
     over the C0a blob, which is not 0. Report each commit's insertions from
     `git diff --numstat` for C0a through C3, confirm each is single-parent and
     under 500. Report `git ls-files .remedy-wt` as 0 lines, `git worktree list`
     as 1 line, and `git ls-files --others --exclude-standard` as 0 lines at C3.
 G8. THE CANARY, THE STATE READERS AND THE DOCS READERS. In the PRIMARY checkout
     at C3, run SERIALLY — never two pytest processes alive at once — reporting
     each REAL exit code and count: `tests/cli/test_golden_path.py` (the canary),
     `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
     `tests/regression/test_resource_safety.py`,
     `tests/orchestration/test_integrity_gate.py`, `tests/docs/`,
     `tests/test_agent_tooling.py` and
     `tests/orchestration/test_role_conventions.py`. At `97b79145` the reviewer
     measured these itself at 42, 489, 52, 21, 16, 295, 10 passed with 1 skipped,
     and 35, every one at exit 0. These are the readers a round rewriting
     `.agent/` state and `docs/agents/` can actually move, so any movement is
     unexplained and you stop and hand back.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C4: feature and round, branch, the per-commit changed-files table
             with the `+/-` column taken from `git diff --numstat` ITSELF and
             agreeing cell for cell with G7's readings, the item-status table
             covering C0a, C0b, C1, C2, C3, C4 and the push, ONE LINE PER GATE
             for G1 through G8 with its real exit code, the open-findings count
             AFTER this round, and the next expected action. SAY PLAINLY THAT NO
             FILE UNDER `apps/`, `packages/`, `tests/` OR `docs/roadmap/`
             CHANGED, THAT NO FINDING WAS RESOLVED THIS ROUND, AND THAT THE OPEN
             COUNT IS THEREFORE UNCHANGED AT THE NUMBER G5 MEASURED. THE NEXT
             ACTION NAMES, IN THIS ORDER: re-read `.agent/STOP` from disk first,
             then the Open PR Gate, then review THIS round's handback and record
             its verdict together with the resolutions the items C3 lands now
             make provable, and only then the COMPONENT half of the markup. Name
             no round number for those: §3 item 35 forbids numbering a round that
             has not begun. Obey constraint 9's cap. Then push with
             `git push origin feature/f031-decision-inbox`.

<<<SLICE PLANF031R59
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
R59 is a checklist round. It records the R58 verdict and lands two items in the
§3 pre-emission checklist of `docs/agents/planner_reviewer_prompt.md`: the
append-reader rule R-0631 wrote as finding prose and R-0694 asks for as an item
of its own, and R-0705's two-part transport rule — no unstated run of repeated
characters in a block's frame, and a verdict that states what its transport
proof covers. NO FINDING IS RESOLVED THIS ROUND: the round that can name the
commit holding the fix writes the resolutions.

## Next Steps
1. The resolutions of R-0631, R-0694 and R-0705, written against the commit that
   lands their fix, recorded beside this round's verdict.
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
- NO GATE IN THIS WORKFLOW COMPARES THE EMITTED BLOCK TO THE COMMITTED ONE.
  R-0705 states the limit; every transport claim is the saved copy to its mirror
  to disk, and the appliable bytes are proved separately against their targets.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 253 at `97b79145`
  and this round moves it by nothing.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R59

<<<SLICE LEDGER59
Gate: F031 R58 — the F031 R58 entry. R58 PASSED ON EVERY GATE ITS BLOCK ORDERED, G1 THROUGH G7, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk. THIS WAS A RECORD ROUND: no file outside `.agent/` changed, R-0704 closed and R-0705 opened in the same commit, and the open set reads 253 at both points. THE TRANSPORT CHAIN THIS WORKFLOW CAN ACTUALLY WALK HELD, AND THAT CHAIN IS THE SAVED COPY, ITS MIRROR AND THE WORKING COPY — NOT THE EMITTED BYTES, which R-0705 records as unmeasurable here: the C0a and C0b blobs are byte-identical at sha256 `9aaf4726…37632c48` over 21646 bytes and 201 lines and resolve to the SAME git blob `8e170e184964`, the working copy matches both, and NO LINE OF THE BLOCK IS A RUN OF ONE REPEATED CHARACTER — the first block written to R-0705's own counter-measure, by the reviewer that registered it. THE EXTRACTION printed 2 slices at 47 and 5 content lines with CONTENT 52 and TOTAL 201, so PROSE 149 against 400 and TOTAL 201 against 490. THE PLAN at `d2f1d3e0` is byte-equal to PLANF031R58 with the minus-newline control FALSE, `^## Goal$` 1, `^## Next Steps$` 1 and `wc -l` 47. THE APPEND IS EXACT AND ITS SECOND READER COVERED THE WHOLE APPENDED REGION: 933063 + 1 + 8520 = 941584 and the committed blob is 941584; N counted by the reviewer's own script is 3, units 379 to 382, the last three units match the slice's three paragraphs IN ORDER, and a byte flipped IN MEMORY inside the FIRST appended paragraph is REJECTED by BOTH readers. THE SETS MOVED EXACTLY WHERE CONSTRAINT 5 ALLOWED: `^- R-\d+ — ` 265 to 266 with the ADDED id exactly `R-0705`, `^Done: R-\d+ — ` 12 to 13 with the ADDED id exactly `R-0704`, `^Gate: F\d+ R\d+ — ` 38 to 39 with the ADDED key exactly `F031 R57`, `^Landed: R-` 0 and `^Gate: R\d+ — ` 19 unmoved, every id DISTINCT with `R-0705` the maximum, `R-0704` also present as a `^- R-\d+ — ` paragraph and `R-0705` absent from every `^Done:` line, and the open set 253 before C2 and 253 after it. NOTHING ELSE MOVED: both path residues EMPTY over the expected path set, `apps/`, `packages/`, `tests/` and `docs/` WHOLE each EMPTY in the range, markers 0 and 0 in the plan and in the ledger against a CONTROL of 2 and 2, and `git ls-files .remedy-wt` 0 lines, `git worktree list` 1 line and `git ls-files --others --exclude-standard` 0 lines. THE READERS THE REVIEWER RE-RAN SERIALLY, every one at a REAL exit 0 and every one EQUAL to the base reading: the canary 42, `tests/ui_server/` 489, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21 and `tests/orchestration/test_integrity_gate.py` 16. THE PER-COMMIT INSERTIONS OVER THE WHOLE RANGE, INCLUDING THE HANDBACK COMMIT ITS OWN GATES COULD NOT REACH, are 201, 104, 13, 6 and 29, each single-parent and under 500, and the handback at `97b79145` is 60 lines against the 60 constraint 8 made it derive from a five-commit bundle; §3 item 31 is why those last two numbers are recorded here rather than in a round report that ends with the session. THE HANDBACK'S `+/-` COLUMN AGREES CELL FOR CELL WITH `git diff --numstat`. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.
<<<END LEDGER59

<<<SLICE S36NEW
      re-derives, since deriving it means counting the rounds that have not happened.

  36. **A multi-paragraph append is proved by a second reader that covers the WHOLE
      appended region, and its negative control sits on the FIRST appended
      paragraph.** Findings R-0631 and R-0694. When a block orders an append to a
      record file, reading (b) — the independent structural reader that exists
      because a byte reader and a structural reader fail differently — compares the
      LAST N blank-line units of the whole file against the slice's N paragraphs IN
      ORDER, where N is a value the worker's script COUNTS and never a number the
      block asserts, and the negative control flips a byte inside the FIRST appended
      paragraph rather than the last. A single-paragraph append is the N=1 case of
      that same sentence, so one wording covers both shapes and no block has to
      decide which it is holding. A reader worded "the last unit equals the slice's
      final paragraph" is a TOTAL check only at N=1, and against a longer slice it
      degenerates to a check of one paragraph: R-0631 records a fifty-one-paragraph
      append, measured at `f19abdfb`, in which a byte flipped in the FIRST appended
      paragraph was REJECTED by reading (a) and ACCEPTED by reading (b) as worded,
      so the independence the gate claimed covered one paragraph in fifty-one. A
      control placed on the LAST paragraph hides the same gap from the other side,
      because the byte reader rejects it alone and reading (b) is then never
      exercised while the gate still reports a pass. Item 22 governs a sentence
      quantifying across COMMITS and item 28 a value the handback template also
      carries; neither reaches this one, because here every number is measured and
      every range is right, and only the REGION the second reader covers is too
      small. This is an item rather than a habit for the reason the list itself
      exists: R-0631 stated exactly this counter-measure in a finding BODY and
      labelled it binding on the next block that orders a multi-paragraph append,
      and R-0694 is the record of the next such block ordering three of them with
      both gates worded tail-only and no control on a first paragraph — because a
      rule living in ledger prose binds nobody.

  37. **A verdict states what its transport proof COVERS, and a block's frame carries
      no run of repeated characters whose length is not stated.** Finding R-0705.
      Under docs/agents/self_drive_protocol.md there is no paste relay: the block
      travels inside the worker's prompt and the worker TYPES it into
      `.agent/authored/`, so every transport gate this workflow can run compares the
      saved copy to its mirror to the working copy — three artefacts that are all
      the worker's own output. Such a chain proves the worker was SELF-CONSISTENT
      and says nothing about whether it received what was sent. Two obligations
      follow and neither is a new gate. FIRST, no line of a block is a run of a
      single repeated character unless its length is stated beside it: a run has no
      length a reader recovers by eye, so it is the one part of a block that fails
      to survive retyping without leaving a trace, and a fixed short rule or a
      stated count makes the bytes recoverable. SECOND, a verdict names the chain
      its proof actually walked — the saved copy, its mirror, the working copy — and
      never claims the EMITTED bytes, because that claim is unmeasurable in this
      workflow and an unmeasurable claim in a verdict is the thing this record
      exists to prevent. Item 12 governs the reviewer's own pre-emission runs and
      item 33 whether an ordered command can produce a reading at all; neither
      reaches this one, because here every ordered command runs and returns a true
      reading, and the defect is that the property the reading is reported as
      establishing is strictly larger than the property it establishes. LOW and
      structural rather than lucky: nothing appliable travels in a block's frame —
      the appliable bytes are the slices, each proved against its TARGET by its own
      gate — so a frame line that drifts cannot reach any file this repository
      keeps.
<<<END S36NEW

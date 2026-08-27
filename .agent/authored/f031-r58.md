STEP RECORD ROUND / F031 — ROUND R58
Goal:        Write the R57 verdict, which PASSED on every gate. Resolve R-0704
             now that the widened §3 item 35 is on disk and the reviewer has
             measured it there. Register R-0705, the transport gap the R57
             worker declared before review. NOTHING OUTSIDE `.agent/` IS
             TOUCHED: no production code, no `docs/` file, no decision.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the plan
             · C2 the R57 gate entry, the R-0704 resolution and R-0705 · C3
             handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f031-r58.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `.agent/handoff.md`. NOTHING UNDER `apps/`, `packages/`, `tests/`
             or `docs/` — in particular nothing under `docs/agents/` and nothing
             under `docs/roadmap/`. `.agent/decisions.md` is not in it either.

Constraints:
 1. EVERY SLICE IS APPLIED BYTE FOR BYTE. Never retype one, never reflow one,
    never fix one. A slice's text is its content lines joined with a newline
    plus ONE trailing newline. If a slice looks wrong, say so in the handback
    and finish the round anyway — a corrected slice destroys the transport
    proof.
 2. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3. No pair may be reordered
    and none may be merged.
 3. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES R57. That is
    ordered: the plan becomes current at C1.
 4. EVERY SLICE IS THE REVIEWER'S TEXT. You never write a `Done:` paragraph of
    your own and never mint a finding id. LEDGER58 carries the gate entry, the
    one resolution and the one registration this round lands, and you add
    nothing to it.
 5. THE LEDGER SETS MOVE ONCE. Across C2 `^- R-\d+ — ` moves 265 to 266 with the
    ADDED id exactly `R-0705`; `^Done: R-\d+ — ` moves 12 to 13 with the ADDED
    id exactly `R-0704`; `^Gate: F\d+ R\d+ — ` moves 38 to 39 with the ADDED key
    exactly `F031 R57`; `^Landed: R-` stays 0 and `^Gate: R\d+ — ` stays 19. The
    open set is 253 before C2 and 253 after C2 — one finding closes and one
    opens, so the count is unchanged and that is not an error.
 6. RE-READ `.agent/STOP` FROM DISK before C0a and again before C3. If it exists
    at either reading, finish the commit in hand, write the handback and STOP.
    Never create it, never delete it.
 7. NOTHING DESTRUCTIVE IS ORDERED THIS ROUND. Create no worktree; the primary
    checkout reads `git status --porcelain` 0 lines at every commit.
 8. YOUR HANDBACK'S CAP. AGENTS.md gives 60 lines at most, or 100 at most when
    per-commit tables of MORE THAN FIVE commits require it. Count the commits
    the Bundle above orders and derive your cap from that count yourself. If the
    MANDATED content genuinely does not fit, write the DECISION D15 "Deviations,
    declared" line naming your actual line count and the specific mandated
    content that caused the overage. Do not invent a tier.
 9. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `cp`, brace literals containing a quote character, `cd x && y`,
    and every form of environment assignment. Route anything that counts, hashes
    or compares through a quoted python heredoc, read real exit codes from
    `subprocess.run(...).returncode`, and pass `cwd=` rather than `cd`. Run
    pytest SERIALLY — never two pytest processes alive at once. `--timeout` IS
    NOT AVAILABLE to pytest here: passing it exits 4 and reports no failure.

Done when — run every gate yourself and record its REAL exit code. G1 through G7
run at commits STRICTLY EARLIER than C3, so the handback can quote them; the
push is ordered after C3 and its reading is NOT written into the handback. Read
every non-current revision with `git show <rev>:<path>` into memory; never write
a past blob over a tracked file to read it.
 G1. BRANCH, CLEANLINESS, TRANSPORT. Branch is `feature/f031-decision-inbox`.
     `git status --porcelain` prints 0 lines after each of C0a, C0b, C1 and C2.
     `.agent/STOP` read from disk before C0a and before C3, both ABSENT. Report
     the sha256, byte count and line count of this block as saved at C0a, as
     mirrored at C0b, and as read off disk at C2 — all three must be EQUAL — and
     say whether C0a and C0b are the same git blob. Report also whether any line
     of the block as saved is a run of a single repeated character, which must
     come back as none: that reading is what makes this block's own transport
     recoverable, and R-0705 is why it is ordered.
 G2. EXTRACTION AND CAPS. Extract the slices from the COMMITTED C0a blob by
     their marker LINES, never from the prompt. Report how many slices your
     extractor printed, each slice's own line count, the CONTENT line total, the
     TOTAL line count, and PROSE as TOTAL minus CONTENT. MARKERS ARE PROSE.
     PROSE must be at most 400 and TOTAL at most 490.
 G3. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF031R58 under the
     newline-INCLUDED convention. Run the negative control against the slice
     MINUS its trailing newline and report it FALSE. Report `^## Goal$` 1,
     `^## Next Steps$` 1, and `wc -l` STRICTLY UNDER 50.
 G4. THE APPEND, PROVED TWICE, THE SECOND READER COVERING THE WHOLE APPENDED
     REGION. `.agent/live_review.md` at C2 equals its pre-commit blob plus ONE
     newline plus LEDGER58. The reviewer measured the base blob at `75bd8210`
     itself: `.agent/live_review.md` is 933063 bytes. If it reads differently
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
     both points, and report that the ADDED resolved id also occurs as a
     `^- R-\d+ — ` paragraph in the same file, and that the ADDED finding id
     does NOT occur as a `^Done: R-\d+ — ` line.
 G6. NOTHING ELSE MOVED, MARKERS, PATHS, COMMITS. Compare the path set of
     `git diff --name-only 75bd8210..C2` BOTH WAYS against this round's expected
     set — the Change line's list MINUS `.agent/handoff.md`, excluded because
     the handback is written at C3, outside a range ending at C2 — and report
     both residues EMPTY. Report `git diff --stat 75bd8210..C2` restricted to
     `apps/`, `packages/`, `tests/` and `docs/` and confirm each is EMPTY —
     `docs/` WHOLE, not only its subtrees, because this round touches no
     documentation at all. Line-anchored `^<<<SLICE ` and `^<<<END ` are 0 and 0
     in `.agent/plan.md` at C1 and `.agent/live_review.md` at C2, against a
     CONTROL count over the C0a blob, which is not 0. Report each commit's
     insertions from `git diff --numstat` for C0a through C2, confirm each is
     single-parent and under 500. Report `git ls-files .remedy-wt` as 0 lines,
     `git worktree list` as 1 line, and `git ls-files --others
     --exclude-standard` as 0 lines at C2.
 G7. THE CANARY AND THE STATE READERS. In the PRIMARY checkout at C2, run
     SERIALLY — never two pytest processes alive at once — reporting each REAL
     exit code and count: `python3 -m pytest tests/cli/test_golden_path.py -q`
     (the canary), `tests/ui_server/`,
     `tests/orchestration/test_test_runner.py`,
     `tests/regression/test_resource_safety.py` and
     `tests/orchestration/test_integrity_gate.py`. At `75bd8210` the reviewer
     measured these itself at 42, 489, 52, 21 and 16, every one at exit 0. These
     are the readers a round rewriting `.agent/` state can actually move, so any
     movement is unexplained and you stop and hand back.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C3: feature and round, branch, the per-commit changed-files table
             with the `+/-` column taken from `git diff --numstat` ITSELF and
             agreeing cell for cell with G6's readings, the item-status table
             covering C0a, C0b, C1, C2, C3 and the push, ONE LINE PER GATE for
             G1 through G7 with its real exit code, the open-findings count
             AFTER this round, and the next expected action. SAY PLAINLY THAT NO
             FILE OUTSIDE `.agent/` CHANGED, THAT R-0704 IS NOW RESOLVED AND
             R-0705 IS NOW OPEN, AND THAT THE OPEN COUNT IS UNCHANGED BECAUSE
             ONE CLOSED AND ONE OPENED. THIS IS THE LAST ROUND OF ITS SESSION,
             SO THE NEXT ACTION SECTION IS WHAT THE NEXT SESSION RESUMES FROM
             AND IT NAMES, IN THIS ORDER: re-read `.agent/STOP` from disk first,
             then the Open PR Gate, then review THIS round's handback and record
             its verdict, then the round landing both the §3 item R-0694's fix
             clause asks for and R-0705's two-part counter-measure, and only
             then the COMPONENT half of the markup. Name no round number for
             those: §3 item 35 as widened at R57 forbids numbering a round that
             has not begun. Obey constraint 8's cap. Then push with
             `git push origin feature/f031-decision-inbox`.

<<<SLICE PLANF031R58
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
R58 is a record round and touches no file outside `.agent/`. It writes the R57
verdict, resolves R-0704 now that the widened §3 item 35 is on disk and the
reviewer has measured it there, and registers R-0705, the transport gap the R57
worker declared before review: a run of repeated characters in a block's frame
has no length a reader can recover, so the committed block is not provably the
emitted one. No production code, no `docs/` file and no decision this round.

## Next Steps
1. The §3 item R-0694's own fix clause asks for, which states R-0631's
   append-reader rule, landed together with R-0705's counter-measure.
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
  R-0705 states the limit; every transport claim is C0a to C0b to disk, and the
  appliable bytes are proved separately, slice by slice, against their targets.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 253 at `75bd8210`,
  and R-0704 closing beside R-0705 opening leaves it at 253.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R58

<<<SLICE LEDGER58
Gate: F031 R57 — the F031 R57 entry. R57 PASSED ON EVERY GATE ITS BLOCK ORDERED, G1 THROUGH G8, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk. THIS WAS THE RESOLUTION SWEEP: no production file changed, no `docs/` file but the reviewer prompt, and four findings closed on evidence the reviewer measured itself rather than on a green suite. TRANSPORT HELD WITHIN THE PROOF THIS WORKFLOW CAN ACTUALLY TAKE: the C0a and C0b blobs are byte-identical at sha256 `6da46cc9…4b044bf` over 26103 bytes and 253 lines and resolve to the SAME git blob `10d6732f37f4`, the working copy at `75bd8210` matches both, and the extraction printed 3 slices at 47, 9 and 16 content lines with CONTENT 72 and TOTAL 253, so PROSE 181 against 400 and TOTAL 253 against 490. THE PLAN at `97fd96ec` is byte-equal to PLANF031R57 with the minus-newline control FALSE, `^## Goal$` 1, `^## Next Steps$` 1 and `wc -l` 47. THE APPEND IS EXACT AND ITS SECOND READER REALLY REACHED PAST THE TAIL THIS TIME: 923830 + 1 + 9232 = 933063 and the committed blob is 933063; N counted by the reviewer's own script is 5, units 374 to 379, the last five units match the slice's five paragraphs IN ORDER, and a byte flipped IN MEMORY inside the FIRST appended paragraph is REJECTED by BOTH readers — a discrimination the R56 entry could not make, because N was 1 there. THE SETS MOVED EXACTLY WHERE CONSTRAINT 5 ALLOWED: `^- R-\d+ — ` 265 to 265 with the ADDED id set EMPTY, `^Done: R-\d+ — ` 8 to 12 with the ADDED set exactly `R-0695`, `R-0697`, `R-0698` and `R-0699`, `^Gate: F\d+ R\d+ — ` 37 to 38 with the ADDED key exactly `F031 R56`, `^Landed: R-` 0 and `^Gate: R\d+ — ` 19 unmoved, every resolved id also present as a `^- R-\d+ — ` paragraph, and the open set 257 before C2 and 253 after it. THE PAIR IS AN APPEND AND ITS OBLIGATION WAS THE APPEND ONE: at `941b8966` S4NEW's first line occurs 1x and `^  36\. \*\*` 0x over 1057 lines; the containment test reads `TO contains FROM: true`, so no FROM-zero count was ordered or reported; at `e7ce5f1e` S4NEW occurs 1x, its first line still 1x, `^  36\. \*\*` still 0x over 1072 lines, the delta 15 equals the slice's 16 lines minus the shared one, and the reviewer's own reading of that commit's added lines is ORDERED EQUALITY — 15 added lines, each a TO-only line of S4NEW, in the slice's order, with numstat 15 and 0. NOTHING ELSE MOVED: both path residues EMPTY over the expected path set, `apps/`, `packages/`, `tests/` and `docs/roadmap/` each EMPTY in the range, markers 0 and 0 in the plan, the ledger and the reviewer prompt against a CONTROL of 3 and 3, insertions 253, 130, 20, 10 and 15 with each commit single-parent and under 500, and `git ls-files .remedy-wt` 0 lines, `git worktree list` 1 line and `git ls-files --others --exclude-standard` 0 lines. THE READERS THE REVIEWER RE-RAN SERIALLY, every one at a REAL exit 0 and every one EQUAL to the base reading: `tests/docs/` 295, `tests/test_agent_tooling.py` 10 passed with 1 skipped, `tests/orchestration/test_role_conventions.py` 35, the canary 42, `tests/ui_server/` 489, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21 and `tests/orchestration/test_integrity_gate.py` 16. THE ROUND'S ONE DECLARED DEPARTURE IS ACCEPTED AND REGISTERED RATHER THAN CHARGED TO IT: the worker could not recover the length of the block's two box-rule lines from the prompt and reconstructed them to this emitter's own on-disk convention, said so before review, and left every other line character-for-character — which is R-0705 below, a defect of the transport and of the reviewer's claim about it, not of the round. AND ONE PIECE OF EVIDENCE JOINS AN OPEN FINDING RATHER THAN MINTING AN ID: the R56 block's pre-emission size was SUMMED from separately-counted chunks at 291 while the committed block is 293, which is exactly `R-0470`, "A BLOCK DECLARED A SIZE IT HAD NOT MEASURED", still OPEN — so that entry gains this instance and no second id is created, per §3 item 30. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing table, no unverified completion claim and no silent scope change.

Done: R-0704 — RESOLVED AT F031 R58 BY MEASUREMENT OF THE WIDENED COUNTER-MEASURE ON DISK. R-0704 recorded a plan slice whose prose forward-referenced a round its own numbered list no longer held, and it was kept OPEN through two further instances precisely because the first counter-measure did not reach them: §3 item 35 as landed at R56 C3 catches an item the list does NOT hold, and both recurrences were a label the list DID hold, in the wrong position. THE WIDENING IS NOW ON DISK AND THE REVIEWER READ IT THERE: `docs/agents/planner_reviewer_prompt.md` at `e7ce5f1e` carries item 35 at 1072 lines with the R56 recurrence named in its own body and the rule stated as a prohibition rather than a caution — a state slice assigns a round NUMBER to the round it is written FOR and to no other, because a step not yet begun is named by what it does and its number is not knowable while any step ahead of it can still be inserted, split or dropped. THE FIX IS PROVED APPLIED RATHER THAN ASSERTED: the slice occurs 1x, its shared first line still occurs 1x, the added lines of that commit are exactly the slice's other lines IN ORDER, and no numbered item was created — `^  36\. \*\*` is 0 at that commit as it was at the base. THE PLAN THAT LANDS WITH THIS PARAGRAPH IS THE FIRST TO OBEY THE NEW RULE, naming its later steps by what they do and giving no round number to any of them, so the record and the file it governs agree for the first time since this finding was raised. Nothing about the two landed instances is rewritten: §3 item 20 forbids it, and a dated correction is how this record stays honest.

- R-0705 — Low, NOTHING IN THIS WORKFLOW COMPARES THE BLOCK THAT WAS EMITTED TO THE BLOCK THAT WAS COMMITTED, AND A RUN OF REPEATED CHARACTERS IS WHERE THAT GAP BECOMES VISIBLE. DECLARED BY THE R57 WORKER BEFORE REVIEW, which is the only reason it is knowable at all. Under self-drive there is no paste relay: docs/agents/self_drive_protocol.md replaces the hash-stamp ritual, the block travels inside the worker's prompt, and the worker TYPES it into `.agent/authored/`. Every transport gate this branch has run — including the one in the block that produced this finding — compares C0a to C0b to the working copy, and all three are the worker's own output, so a faithful chain proves the worker was self-consistent and says nothing about whether it received what was sent. THE INSTANCE: the R57 block's frame carries two lines that are runs of one box-drawing character, and a run has no length a reader recovers by eye. The worker reconstructed them to the lengths it measured across `f031-r50.md` through `f031-r56.md`, 71 characters for the header and 70 for the closing rule, and reported the reconstruction; the committed block is therefore not byte-identical to the emitted one, and no gate could have detected it. LOW, AND THE REASON IS STRUCTURAL RATHER THAN LUCKY: nothing appliable travels in a block's frame. The appliable bytes are the slices, and each is proved against its TARGET by its own gate — byte-equality for a whole-file replacement, pre-blob plus newline plus slice for an append, ordered equality of the added lines for a pair — so a frame line that drifts cannot reach any file this repository keeps. THE FIX HAS TWO HALVES AND NEITHER IS A NEW GATE. First, a block's frame carries no run of repeated characters whose length is not stated beside it; a fixed short rule, or a stated count, makes the bytes recoverable, and the block registering this finding is written that way as its own demonstration. Second, and more important, every verdict states what its transport proof COVERS — C0a to C0b to disk — and never claims the emitted bytes, because that claim is unmeasurable here and an unmeasurable claim in a verdict is the thing this record exists to prevent. Both halves belong in docs/agents/planner_reviewer_prompt.md §3, which is the reviewer's own file and is in no round's change set by default, so this stays OPEN until a round puts them there. NOT A DUPLICATE, and the open set was searched for the DEFECT before this id was minted, as §3 item 30 requires: `R-0470` is a block declaring a size it had not measured, `R-0403` is the review zip packaging scratch, and `R-0408` is a block naming a TOOL where it means a PROPERTY, while this is the transport CHAIN having an unmeasured first link. OPEN.
<<<END LEDGER58

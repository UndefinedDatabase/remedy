STEP RECORD ROUND / F031 — ROUND R60
Goal:        Write the R59 verdict, which PASSED on every gate the reviewer
             re-ran. Resolve R-0631, R-0694 and R-0705 against the §3 items
             that landed at `513bb9e0`. Register the two reviewer defects the
             R59 worker declared before review. NOTHING OUTSIDE `.agent/` IS
             TOUCHED: no production code, no `docs/` file, no decision.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the plan
             · C2 the R59 gate entry, three resolutions and two registrations
             · C3 handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f031-r60.md`,
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
 3. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES R59. That is
    ordered: the plan becomes current at C1.
 4. EVERY SLICE IS THE REVIEWER'S TEXT. You never write a `Done:` paragraph of
    your own and never mint a finding id. LEDGER60 carries the gate entry, the
    three resolutions and the two registrations this round lands, and you add
    nothing to it and remove nothing from it.
 5. THE LEDGER SETS MOVE ONCE. Across C2 `^- R-\d+ — ` moves 266 to 268 with the
    ADDED ids exactly `R-0706` and `R-0707`; `^Done: R-\d+ — ` moves 13 to 16
    with the ADDED ids exactly `R-0631`, `R-0694` and `R-0705`;
    `^Gate: F\d+ R\d+ — ` moves 40 to 41 with the ADDED key exactly `F031 R59`;
    `^Landed: R-` stays 0 and `^Gate: R\d+ — ` stays 19. The open set is 253
    before C2 and 252 after C2 — three findings close and two open.
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
     come back as none. THEN STATE IN ONE SENTENCE WHAT THIS PROOF COVERS: the
     saved copy, its mirror and the working copy, all three your own output, and
     NOT the bytes that were emitted to you. §3 item 37 is why both readings are
     ordered.
 G2. EXTRACTION AND CAPS. Extract the slices from the COMMITTED C0a blob by
     their marker LINES, never from the prompt. Report how many slices your
     extractor printed, each slice's own line count, the CONTENT line total, the
     TOTAL line count, and PROSE as TOTAL minus CONTENT. MARKERS ARE PROSE.
     PROSE must be at most 400 and TOTAL at most 490.
 G3. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF031R60 under the
     newline-INCLUDED convention. Run the negative control against the slice
     MINUS its trailing newline and report it FALSE. Report `^## Goal$` 1,
     `^## Next Steps$` 1, and `wc -l` STRICTLY UNDER 50.
 G4. THE APPEND, PROVED TWICE, THE SECOND READER COVERING THE WHOLE APPENDED
     REGION. `.agent/live_review.md` at C2 equals its pre-commit blob plus ONE
     newline plus LEDGER60. The reviewer measured the base blob at `84f362e5`
     itself: `.agent/live_review.md` is 944832 bytes over 383 blank-line units.
     If it reads differently before C2, something moved that this round did not
     order — stop and hand back. Report both byte counts and the sum. Then
     confirm with a SECOND, independent reader, exactly as §3 item 36 now
     requires: split the whole file on blank lines, let N be the number of
     paragraphs YOUR SCRIPT COUNTS in that slice — never a number this block
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
     both points, and report that EVERY ADDED resolved id also occurs as a
     `^- R-\d+ — ` paragraph in the same file, and that NEITHER ADDED finding id
     occurs as a `^Done: R-\d+ — ` line.
 G6. NOTHING ELSE MOVED, MARKERS, PATHS, COMMITS. Compare the path set of
     `git diff --name-only 84f362e5..C2` BOTH WAYS against this round's expected
     set — the Change line's list MINUS `.agent/handoff.md`, excluded because
     the handback is written at C3, outside a range ending at C2 — and report
     both residues EMPTY. Report `git diff --stat 84f362e5..C2` restricted to
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
     exit code and count: `tests/cli/test_golden_path.py` (the canary),
     `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
     `tests/regression/test_resource_safety.py` and
     `tests/orchestration/test_integrity_gate.py`. At `84f362e5` the reviewer
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
             FILE OUTSIDE `.agent/` CHANGED, THAT R-0631, R-0694 AND R-0705 ARE
             NOW RESOLVED, THAT R-0706 AND R-0707 ARE NOW OPEN, AND THAT THE
             OPEN COUNT FELL BY ONE BECAUSE THREE CLOSED AND TWO OPENED. THE
             NEXT ACTION NAMES, IN THIS ORDER: re-read `.agent/STOP` from disk
             first, then the Open PR Gate, then review THIS round's handback and
             record its verdict, then the COMPONENT half of the markup — the
             pending card rendering a field per open clarification, with
             `tests/ui_contracts/test_decision_answer_wiring.py` moving with it.
             Name no round number for those: §3 item 35 forbids numbering a
             round that has not begun. Obey constraint 8's cap. Then push with
             `git push origin feature/f031-decision-inbox`.

<<<SLICE PLANF031R60
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
R60 is a record round and touches no file outside `.agent/`. It writes the R59
verdict, resolves R-0631, R-0694 and R-0705 against the §3 items that landed at
`513bb9e0`, and registers the two reviewer defects the R59 worker declared
before review: an ordered-equality gate defeated by git's hunk anchoring, and a
delegation wrapper that described the block's own last line wrongly. No
production code, no `docs/` file and no decision this round.

## Next Steps
1. The COMPONENT half: the pending card renders a field per open clarification
   and the flow carries the map R53 built.
   `tests/ui_contracts/test_decision_answer_wiring.py` pins the card's call
   string and its two-writer count, so that round moves those guards with it.
2. The integration-gate round per `docs/agents/integration_gate.md`, then
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
- NO GATE COMPARES THE EMITTED BLOCK TO THE COMMITTED ONE AND NONE CAN. §3 item
  37 closes the reviewer's obligation to SAY so; the gap itself stands, and
  every transport claim is the saved copy to its mirror to disk.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 253 at `84f362e5`,
  and three closing beside two opening leaves it at 252.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R60

<<<SLICE LEDGER60
Gate: F031 R59 — the F031 R59 entry. R59 PASSED ON EVERY GATE ITS BLOCK ORDERED, G1 THROUGH G8, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk. THIS WAS THE CHECKLIST ROUND: the only file outside `.agent/` that changed is `docs/agents/planner_reviewer_prompt.md`, which gained §3 items 36 and 37 at `513bb9e0`, and no finding was resolved in it. THE TRANSPORT PROOF COVERS THE SAVED COPY, ITS MIRROR AND THE WORKING COPY — ALL THREE THE WORKER'S OWN OUTPUT — AND NOT THE EMITTED BYTES, which is §3 item 37 binding on the first verdict written after it landed: the C0a and C0b blobs are byte-identical at sha256 `397b9d24…471c751b` over 22612 bytes and 282 lines and resolve to the SAME git blob `3b4442cca8bf`, the working copy matches both, and no line of the block is a run of one repeated character. THE EXTRACTION printed 3 slices at 48, 1 and 56 content lines with CONTENT 105 and TOTAL 282, so PROSE 177 against 400 and TOTAL 282 against 490. THE PLAN at `91e83527` is byte-equal to PLANF031R59 with the minus-newline control FALSE, `^## Goal$` 1, `^## Next Steps$` 1 and `wc -l` 48. THE APPEND IS EXACT: 941584 + 1 + 3247 = 944832 and the committed blob is 944832; N counted by the reviewer's own script is 1, units 382 to 383, the last unit matches the slice's one paragraph, and a byte flipped IN MEMORY inside the FIRST appended paragraph is REJECTED by BOTH readers — the N=1 case §3 item 36 covers in the same sentence as every longer slice. THE SETS MOVED EXACTLY WHERE CONSTRAINT 5 ALLOWED: `^Gate: F\d+ R\d+ — ` 39 to 40 with the ADDED key exactly `F031 R58`, and `^- R-\d+ — ` 266, `^Done: R-\d+ — ` 13, `^Landed: R-` 0 and `^Gate: R\d+ — ` 19 every one UNMOVED, all ids DISTINCT with `R-0705` the maximum, and the open set 253 at both points. THE PAIR LANDED EXACTLY: at `97b79145` the prompt is 1072 lines with S36NEW's first line 1x and `^  36\. \*\*` and `^  37\. \*\*` both 0; at `513bb9e0` it is 1127 lines, S36NEW occurs 1x, its first line still 1x, both item counts 1, the delta 55 equals the slice's 56 lines minus the shared one, and `git diff --numstat` reads 55 and 0. THE STRONGEST READING IS THE ONE THE REVIEWER TOOK ITSELF: the C3 blob equals the base blob with the anchor line replaced ONCE by the slice, the 56 lines occupying the replaced region equal the slice IN ORDER, and the tail below them is byte-identical to the base tail. NOTHING ELSE MOVED: both path residues EMPTY, `apps/`, `packages/`, `tests/` and `docs/roadmap/` each EMPTY in the range, markers 0 and 0 in the plan, the ledger and the prompt against a CONTROL of 3 and 3, insertions 282, 186, 13, 2, 55 and 60 with each commit single-parent and under 500, and `git ls-files .remedy-wt` 0 lines, `git worktree list` 1 line and `git ls-files --others --exclude-standard` 0 lines. THE READERS THE REVIEWER RE-RAN SERIALLY, every one at a REAL exit 0 and every one EQUAL to the base reading: the canary 42, `tests/ui_server/` 489, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21, `tests/orchestration/test_integrity_gate.py` 16, `tests/docs/` 295, `tests/test_agent_tooling.py` 10 passed with 1 skipped and `tests/orchestration/test_role_conventions.py` 35. THE HANDBACK COMMIT'S OWN NUMBERS, WHICH §3 ITEM 31 ROUTES HERE: `84f362e5` adds 60 lines and removes 31 in `.agent/handoff.md`, and that handoff is 89 lines against the 100 a six-commit bundle made the worker derive. THE ROUND'S TWO DECLARED DEPARTURES ARE BOTH THE REVIEWER'S AND BOTH BECOME FINDINGS BELOW rather than being charged to the round: the delegation prose mis-described the block's own last line, and G6's ordered-equality wording does not survive git's hunk anchoring. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.

Done: R-0631 — RESOLVED AT F031 R60 BY THE §3 ITEM LANDED AT `513bb9e0`. R-0631 recorded a two-reader append gate whose second reader compared only the LAST unit, so against a fifty-one-paragraph slice its negative control could probe one paragraph in fifty-one, and its counter-measure was written as finding prose labelled binding on the next block. THAT WORDING IS NOW §3 ITEM 36 AND THE REVIEWER READ IT ON DISK: `docs/agents/planner_reviewer_prompt.md` at `513bb9e0` is 1127 lines and carries `^  36\. \*\*` exactly once, stating that reading (b) compares the LAST N blank-line units of the whole file against the slice's N paragraphs IN ORDER with N counted by the worker's script rather than asserted by the block, and that the negative control flips a byte inside the FIRST appended paragraph. THE ITEM ALSO CARRIES THE N=1 SENTENCE, so a single-paragraph append is the same rule rather than an exception a block has to recognise, and it names the control placed on the LAST paragraph as the mirror-image defect — rejected by the byte reader alone, leaving the structural reader unexercised while the gate reports a pass. THE FIX IS PROVED APPLIED RATHER THAN ASSERTED: the slice occurs 1x, the C3 blob equals the base blob with its anchor line replaced ONCE, and the tail below the replaced region is byte-identical to the base tail.

Done: R-0694 — RESOLVED AT F031 R60 BY THAT SAME ITEM, WHICH IS WHAT THIS FINDING ASKED FOR BY NAME. R-0694 recorded that R-0631's fix clause lived only in ledger prose and that the next block to order a multi-paragraph append did not apply it — three appends, both gates worded tail-only, no control on a first paragraph — and its own fix names the remedy exactly: a new §3 checklist item stating R-0631's clause, landing with the reviewer rather than with that round's worker. §3 ITEM 34, LANDED EARLIER AT R56, EXPLICITLY DID NOT DISCHARGE THIS HALF and says so in its own body; item 36 at `513bb9e0` is that half, and the reviewer measured it there at 1127 lines with `^  36\. \*\*` occurring exactly once. THE ITEM NAMES BOTH FINDINGS IN ITS OWN TEXT and closes on why it is an item rather than a habit — a rule living in ledger prose binds nobody — so the sentence that failed to bind now sits where blocks are actually checked.

Done: R-0705 — RESOLVED AT F031 R60 BY §3 ITEM 37, BOTH HALVES, AND DEMONSTRATED BY THE TWO BLOCKS THAT OBEYED IT BEFORE IT LANDED. R-0705 recorded that nothing in this workflow compares the block that was emitted to the block that was committed, and that a run of repeated characters is where that gap becomes visible. `docs/agents/planner_reviewer_prompt.md` at `513bb9e0` carries `^  37\. \*\*` exactly once, holding both halves the finding named: no line of a block is a run of a single repeated character unless its length is stated beside it, and a verdict names the chain its proof actually walked — the saved copy, its mirror, the working copy — and never claims the EMITTED bytes. THE RULE WAS DEMONSTRATED BEFORE IT WAS WRITTEN: the R58 and R59 blocks each carry no such run, both measured by the reviewer off the committed blobs at `480e6ef3` and `270971e4`, and the F031 R59 entry above is the first verdict to state what its transport proof covers. WHAT IS CLOSED AND WHAT IS NOT, SAID PLAINLY: the underlying gap stands, because under self-drive there is no emitted artefact to compare against and no gate can be written for one. What this resolves is the reviewer's obligation to SAY so, which is the only part of that gap a rule can reach, and the finding's own fix asked for exactly that and nothing more.

- R-0706 — Low, AN ORDERED-EQUALITY GATE READ AGAINST `git diff`'s ADDED LINES IS DEFEATED BY HUNK ANCHORING WHENEVER THE APPENDED REGION BEGINS WITH A LINE THE TARGET ALREADY HAS BELOW THE ANCHOR. The defect is the reviewer's, in the R59 block, and it was FOUND AND DECLARED BY THE WORKER as deviation 2 of that round rather than by any gate. G6 ordered that the lines C3's diff ADDS be exactly the lines of S36NEW after its first, IN ORDER. S36NEW's second line is BLANK and the line already following the anchor in the target is also blank, so `git diff --unified=0` anchored its hunk one line earlier and printed 55 added lines beginning with item 36's first line and ending with a blank — the slice's tail rotated by one position. MEASURED BY THE REVIEWER AT `513bb9e0`: the added multiset is EQUAL, the rotation-by-one is TRUE, `--numstat` reads 55 and 0, and the whole-file identity — the C3 blob equals the base blob with the anchor line replaced ONCE by the slice — is TRUE, so the applied bytes are exactly right and only the gate's wording is wrong. WHY LOW: nothing false landed, the worker declared the mismatch rather than choosing whichever reading produced a green, and the stronger property was available and held. THE OPEN SET WAS SEARCHED FOR THE DEFECT BEFORE THIS ID WAS MINTED, per §3 item 30, and `R-0503` is the nearest neighbour and a different fix: it governs an "exactly once among the added lines" COUNT over structural lines, which docs/agents/planner_reviewer_prompt.md §4.9 already replaced with ordered equality; this is that replacement itself failing, through the DIFF's choice of hunk boundary rather than through multiplicity. THE FIX: a gate proving an insertion states the WHOLE-FILE IDENTITY as its primary reading — the post blob equals the pre blob with the FROM replaced exactly once by the TO — and orders a diff-derived reading only beside it, never as the proof, because a diff reports one of several equally correct hunk boundaries and the block cannot know in advance which. Where a line-by-line reading is genuinely wanted, the block orders the lines OCCUPYING the replaced region, which the target's own text fixes, rather than the lines the diff calls added. OPEN.

- R-0707 — Low, THE PROSE WRAPPING A DELEGATED BLOCK MADE A FALSE CLAIM ABOUT THE BLOCK'S OWN BYTES, AND NO GATE READS THAT PROSE. The defect is the reviewer's, in the R59 delegation, and it was FOUND AND DECLARED BY THE WORKER as deviation 1 of that round. Under docs/agents/self_drive_protocol.md the block travels inside a worker prompt, so a wrapper exists that never lands on disk: it named the delimiters correctly and then described the block's last line as ending with the branch name, which is the `Handback:` line rather than the final `<<<END` marker the delimited text actually ends with. THE WORKER RESOLVED THE CONTRADICTION CORRECTLY — it saved the delimited bytes verbatim per the primary instruction and constraint 1, corrected nothing, and declared the mismatch — and the committed block is 282 lines and 22612 bytes, which the reviewer re-measured off the C0a blob at `270971e4`. WHY LOW AND WHY IT STILL MATTERS: nothing false landed, but a wrapper sentence that contradicts the block is exactly the instruction a less careful worker resolves the other way, by trimming the block to fit the description — and the wrapper is the one artefact of a self-drive round that no gate, no reviewer and no later session ever reads again. THE OPEN SET WAS SEARCHED FOR THE DEFECT BEFORE THIS ID WAS MINTED, per §3 item 30: the reviewer-block-defect family `R-0418`, `R-0420`, `R-0428` and `R-0642` all concern the block's OWN text, which §3 item 11 already binds by requiring every claim about it to be measured, and `R-0705` concerns the block's transport rather than the prose around it. This is the surface none of them reaches. THE FIX: a delegation wrapper states the delimiters and NOTHING ELSE about the block's contents — no first line, no last line, no length, no slice count — and where a receipt check is wanted it is ordered as a MEASUREMENT the worker takes and reports, never as a description the reviewer recalls. OPEN.
<<<END LEDGER60

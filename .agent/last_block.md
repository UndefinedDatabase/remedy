── STEP CHECKLIST / F031 — ROUND R56 ──────────────────────────────────
Goal:        Land the remaining §3 pre-emission checklist items this branch owes:
             the one R-0694, R-0695, R-0697 and R-0698 share — a block reads the
             file it orders a change against, for what that file already holds —
             and the one R-0699 and R-0704 share, that a description and the
             enumeration it points at are read against each other. Record the
             R55 verdict, which PASSED on every gate, and advance
             `.agent/plan.md`. NO PRODUCTION CODE CHANGES. NO FINDING IS
             RESOLVED AND NO ID IS MINTED THIS ROUND.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the plan
             · C2 the R55 gate entry · C3 the checklist items · C4 handback ·
             then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f031-r56.md`,
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
    plus ONE trailing newline; a slice that ends in a blank content line carries
    that blank line on purpose and it is part of it. If a slice looks wrong, say
    so in the handback and finish the round anyway — a corrected slice destroys
    the transport proof.
 2. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4. No pair may be
    reordered and none may be merged.
 3. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES R55. That is
    ordered: the plan becomes current at C1.
 4. EVERY SLICE IS THE REVIEWER'S TEXT. You never write a `Done:` paragraph and
    never mint a finding id of your own. LEDGER56 carries everything this round
    records and you add nothing to it. NO FINDING IS RESOLVED THIS ROUND.
 5. THE LEDGER SETS MOVE ONCE, AND THIS ROUND ADDS NO ID. Across C2
    `^- R-\d+ — ` stays 265 with the ADDED id set EMPTY, and
    `^Gate: F\d+ R\d+ — ` moves 36 to 37 with the ADDED key exactly `F031 R55`.
    `^Done: R-\d+ — ` stays 8, `^Landed: R-` stays 0 and `^Gate: R\d+ — ` stays
    19. The open set is 257 before C2 and 257 after C2.
 6. RE-READ `.agent/STOP` FROM DISK before C0a and again before C4. If it exists
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

Spec — the edits to `docs/agents/planner_reviewer_prompt.md`, at C3:
 S1. INSERT S2NEW immediately BEFORE the line
     `  Why this is on disk and not a habit: item 2 has recurred six times across`,
     which the reviewer measured as occurring exactly 1x in that file at
     `58de811a`. That line opens the closing paragraph of the §3 pre-emission
     checklist and item 33 is the last numbered item before it, so S2NEW becomes
     item 34 at the END of the numbered list. The blank line that already
     follows item 33 is what separates item 33 from S2NEW.
 S2. THEN INSERT S3NEW immediately BEFORE that SAME anchor line, so it lands
     AFTER the S2NEW that S1 just applied and becomes item 35. S2NEW's own
     trailing blank line is what separates item 34 from S3NEW, and S3NEW's own
     trailing blank line is what separates item 35 from the closing paragraph.
     ADD NOTHING OF YOUR OWN, and renumber nothing: no item is removed, so no
     existing label moves.

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
 G3. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF031R56 under the
     newline-INCLUDED convention. Run the negative control against the slice
     MINUS its trailing newline and report it FALSE. Report `^## Goal$` 1,
     `^## Next Steps$` 1, and `wc -l` STRICTLY UNDER 50.
 G4. THE APPEND, PROVED TWICE, THE SECOND READER COVERING THE WHOLE APPENDED
     REGION. `.agent/live_review.md` at C2 equals its pre-commit blob plus ONE
     newline plus LEDGER56. The reviewer measured the base blob at `58de811a`
     itself: `.agent/live_review.md` is 920032 bytes. If it reads differently
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
     `^Gate: R\d+ — ` and `^Gate: F\d+ R\d+ — `, plus the ids and gate keys
     ADDED and REMOVED as SETS, whether all ids are DISTINCT, and the maximum
     id. Every movement constraint 5 names is checked here, INCLUDING the ones
     that must NOT move, and the ADDED id set must come back EMPTY. Report the
     open set at both points.
 G6. THE CHECKLIST EDIT. At the base `58de811a`, report the count of the S1
     anchor line, which must be 1, and the counts of the lines `  34. **` and
     `  35. **`, which must both be 0. At C3 in
     `docs/agents/planner_reviewer_prompt.md`: S2NEW occurs 1x, S3NEW occurs 1x,
     the anchor line still occurs 1x, line-anchored `^  34\. \*\*` and
     `^  35\. \*\*` each occur 1x while `^  36\. \*\*` occurs 0x, and S2NEW ends
     exactly where S3NEW begins while S3NEW ends exactly where the anchor line
     begins. Report the file's line count at the base and at C3 and confirm the
     difference is exactly the SUM of the line counts of the slices S1 and S2
     order inserted, which you measure from the slices themselves rather than
     from this block. Report that `git diff --name-only C2..C3` is that one path
     and nothing else, and that the diff for that path has ZERO deleted lines —
     an insertion removes nothing.
 G7. NOTHING ELSE MOVED, MARKERS, PATHS, COMMITS. Compare the path set of
     `git diff --name-only 58de811a..C3` BOTH WAYS against this round's expected
     set — the Change line's list MINUS `.agent/handoff.md`, excluded because
     the handback is written at C4, outside a range ending at C3 — and report
     both residues EMPTY. Report `git diff --stat 58de811a..C3` restricted to
     `apps/`, `packages/`, `tests/` and `docs/roadmap/` and confirm each is
     EMPTY. Line-anchored `^<<<SLICE ` and `^<<<END ` are 0 and 0 in
     `.agent/plan.md` at C1, `.agent/live_review.md` at C2 and
     `docs/agents/planner_reviewer_prompt.md` at C3, against a CONTROL count
     over the C0a blob, which is not 0. Report each commit's insertions from
     `git diff --numstat` for C0a through C3, confirm each is single-parent and
     under 500. Report `git ls-files .remedy-wt` as 0 and `git worktree list` as
     1 line at C3.
 G8. THE DOCS READERS, THE CANARY AND THE STATE READERS. In the PRIMARY checkout
     at C3, run SERIALLY — never two pytest processes alive at once — reporting
     each REAL exit code and count: `python3 -m pytest tests/docs/ -q`,
     `tests/test_agent_tooling.py`, `tests/orchestration/test_role_conventions.py`,
     `tests/cli/test_golden_path.py` (the canary), `tests/ui_server/`,
     `tests/orchestration/test_test_runner.py`,
     `tests/regression/test_resource_safety.py` and
     `tests/orchestration/test_integrity_gate.py`. At `58de811a` the reviewer
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
             REVIEWER PROMPT, AND THAT NO FINDING WAS RESOLVED AND NO ID MINTED.
             THE NEXT ACTION SECTION NAMES, IN THIS ORDER: re-read `.agent/STOP`
             from disk first, then the Open PR Gate, then review this round's
             handback, then the resolution sweep that re-measures the landed
             code halves of R-0695, R-0697, R-0698 and R-0699 and resolves them,
             and only then R57, the markup. Obey constraint 8's cap. Then push
             with `git push origin feature/f031-decision-inbox`.
──────────────────────────────────────────────────────────────────────

<<<SLICE PLANF031R56
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
R56 lands the remaining §3 checklist items: the one R-0694, R-0695, R-0697 and
R-0698 share — a block reads the file it orders a change against, for what that
file already holds — and the one R-0699 and R-0704 share, that a description and
the enumeration it points at are read against each other. R-0696 is already
`Done:` and its resolution routes its root cause here. R-0694's fix clause asks
for a further item stating R-0631's append-reader rule; this round does not land
it. NO FINDING IS RESOLVED THIS ROUND.

## Next Steps
1. The resolution sweep: R-0695, R-0697, R-0698 and R-0699 carry code halves
   that landed at R44 and R48 with no `Done:` paragraph, so each is re-measured
   on disk and resolved, with the process halves item 34 discharges.
2. R57, the COMPONENT half: the pending card renders a field per open
   clarification and the flow carries the map R53 built.
   `tests/ui_contracts/test_decision_answer_wiring.py` pins the card's call
   string and its two-writer count, so that round moves those guards with it.
3. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- SIX OF THE EIGHT PRODUCING TYPES STILL CANNOT BE ANSWERED THROUGH THE DOOR.
  R-0693 measures the gap; the rest are outside F031's scope, and the inbox
  tells the truth about every one of them rather than offering a refused button.
- THE MARKUP IS R57, NOT R56, and the form stays reachable only by a non-browser
  client until it lands; the R55 plan numbered it R56 over an unnumbered round.
- THE REVIEWER'S OWN BLOCK KEEPS CARRYING THE DEFECT: R54 and R55 were each
  caught by the worker, and the R55 plan's round numbering by the reviewer at
  the R55 gate. That is the split working, and why checklist rounds come first.
- FINDINGS WHOSE CODE HALF HAS LANDED ARE STILL COUNTED OPEN, because only
  reviewer-authored text sets Resolved. Step 1 above is that debt.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 257 at `58de811a`
  and this round mints no id.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R56

<<<SLICE LEDGER56
Gate: F031 R55 — the F031 R55 entry. R55 PASSED ON EVERY GATE ITS BLOCK ORDERED, G1 THROUGH G8, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk. THIS WAS THE CHECKLIST HALF: no production file changed, and the only `docs/` path it touched is `docs/agents/planner_reviewer_prompt.md`, which gained §3 item 33, the counter-measure R-0703 names. TRANSPORT HELD: the C0a and C0b blobs are byte-identical at sha256 `bff31a47…d0c4c41b` over 22145 bytes and 247 lines, resolve to the SAME git blob `6e018b05b1d0`, and the working copy at `58de811a` matches both; the extraction printed 3 slices with CONTENT 78 and TOTAL 247, so PROSE 169 against 400 and TOTAL 247 against 490. THE PLAN at `770b1a99` is byte-equal to PLANF031R55 with the minus-newline control FALSE, `^## Goal$` 1, `^## Next Steps$` 1 and `wc -l` 48. THE APPEND IS EXACT AND ITS SECOND READER COVERED THE WHOLE APPENDED REGION: 914510 + 1 + 5521 = 920032 and the committed blob is 920032; N counted by the reviewer's own script is 2, units 371 to 373, the last two units match the slice's two paragraphs IN ORDER, and a byte flipped IN MEMORY inside the FIRST appended paragraph is REJECTED by BOTH readers. THE SETS MOVED EXACTLY WHERE CONSTRAINT 5 ALLOWED: `^- R-\d+ — ` 264 to 265 with the ADDED id exactly `R-0704`, `^Gate: F\d+ R\d+ — ` 35 to 36 with the ADDED key exactly `F031 R54`, `^Done: R-\d+ — ` 8, `^Landed: R-` 0 and `^Gate: R\d+ — ` 19 all unmoved, ids DISTINCT with the maximum now `R-0704`, and the open set 256 before C2 and 257 after it. THE CHECKLIST EDIT IS AN INSERTION AND NOTHING ELSE: at `84551691` the anchor line occurs 1x and `  33. **` 0x over 966 lines; at `b76aca50` S1NEW occurs 1x, the anchor still 1x, `^  33\. \*\*` 1x and `^  34\. \*\*` 0x over 993 lines, the delta 27 equals the slice's own line count, S1NEW ends exactly where the anchor begins, and that commit's numstat reads 27 and 0. NOTHING ELSE MOVED: both path residues EMPTY over the expected path set, `apps/`, `packages/`, `tests/` and `docs/roadmap/` each EMPTY in the range, markers 0 and 0 in the plan, the ledger and the reviewer prompt against a CONTROL of 3 and 3, insertions 247, 152, 20, 4 and 27 with each commit single-parent and under 500, `git ls-files .remedy-wt` 0 lines and `git worktree list` 1 line. THE `+/-` COLUMN OF THE HANDBACK'S `## Commits` TABLE AGREES CELL FOR CELL WITH `git diff --numstat`, which §3 item 28 exists to check, and the handback carries every section docs/agents/handback_template.md mandates, in order, at 100 lines against the 100-line cap the worker DERIVED ITSELF from a six-commit bundle. THE READERS THE REVIEWER RE-RAN SERIALLY, every one at a REAL exit 0 and every one EQUAL to the base reading: `tests/docs/` 295, `tests/test_agent_tooling.py` 10 passed with 1 skipped, `tests/orchestration/test_role_conventions.py` 35, the canary 42, `tests/ui_server/` 489, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21 and `tests/orchestration/test_integrity_gate.py` 16. ONE FURTHER INSTANCE OF R-0704'S OWN CLASS WAS FOUND AT THIS GATE, IN THE REVIEWER'S PLANF031R55 SLICE, AND NO NEW ID IS MINTED FOR IT, because §3 item 30 rules that fresh evidence for an OPEN finding joins that finding rather than a second id: that slice's `## Next Steps` holds an unnumbered checklist round as item 1 and calls the markup `R56` as item 2, while the checklist round IS a round and takes R56, so the markup is R57 — a forward reference disagreeing with the list it points at, which is exactly the counter-measure R-0704 names. THE R56 PLAN REPAIRS IT and the §3 items this round lands are the standing fix. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing table, no unverified completion claim and no silent scope change.
<<<END LEDGER56

<<<SLICE S2NEW
  34. **Every file a block orders a change against is READ at emission, for what it
      already holds.** Findings R-0694, R-0695, R-0697 and R-0698, with R-0696 as the
      resolved instance whose own `Done:` paragraph routes its root cause here. Before
      a block orders an addition, a call, an import or a computed value into a file,
      the reviewer reads that file and the guards that bind it, and writes what it
      found beside the order. The kinds of target that have each cost this branch a
      round are the ones to read. The TESTS that already guard the path, because a
      guard may already assert what the order asks for: R45's item S10 ordered a
      contract guard `tests/ui_contracts/test_decision_answer_wiring.py` already
      carried, and the suite gained a second test calling the same reader over the
      same source for the same property (R-0696). The EQUALITY GUARD that pins a
      closed set the order widens: R47's items S1 and S3 ordered two imports into the
      write door without naming `TestCommandDoorImportGuard` in
      `tests/ui_server/test_command_channel.py`, so the branch tip shipped RED at 1
      failed and 479 passed (R-0697). The CONSTANT a parametrized test compares the
      changed behaviour against: `ANSWERABLE_DECISION_TYPES` in
      `tests/orchestration/test_decision_inbox.py`, which the ordered predicate change
      would have turned red for the `flight_plan_approval` parameter (R-0698). The
      REFUSAL CONDITIONS of a predicate whose value the order computes, and not merely
      its route to the data: `_answerable_by_decision_resolve` in
      `packages/orchestration/decision_inbox.py` tested existence alone while
      `escalation.answer_task_decision` returns None for any record not OPEN, so the
      key read True in exactly the state the write door refuses (R-0695). And the OPEN
      SET itself, which is a target of the same kind: a fix clause labelled binding on
      the next block binds nothing unless the next block greps for it, so the open set
      is read for such clauses before emission and each one is applied or named as
      declined (R-0694 — whose own fix clause asks in addition for R-0631's
      append-reader rule as an item of its own, which this item is not and does not
      discharge). Items 6, 7 and 8 are the neighbours and none of them reaches this
      one: item 6 binds a ZERO-GATE to the target's existing content, item 7 an
      addition an existing count guard makes UNSATISFIABLE, and item 8 a gate whose
      expected VALUE the code contradicts — each of those describes an order that
      FAILS, while every instance here is an order that SUCCEEDS against a file the
      block never read. Nothing is unsatisfiable when the target already satisfies the
      order, and nothing goes red until a guard the block never named finally runs.

<<<END S2NEW

<<<SLICE S3NEW
  35. **A description and the enumeration it points at are read against each other,
      and the enumeration is the half that gets executed.** Findings R-0699 and
      R-0704. Where a block or a state slice both DESCRIBES work in prose and LISTS
      it — a Bundle beside a SPEC, a Current Step beside a Next Steps list, a heading
      beside its own body — the prose is resolved against the list before emission,
      item by item, and anything the prose names that the list does not hold is added
      to the list or struck from the prose. The list is the half that is executed: a
      worker commits by the Bundle, and a resuming session reads `.agent/plan.md` by
      its numbered steps, so a promise living only in the prose is a promise nothing
      performs. R-0699 is that shape inside a block: R47's Bundle described C6 as the
      door's `fp:` dispatch and gave no commit to the tests its own item S12
      described, the worker followed the Bundle because the enumeration is what tells
      it when to commit, and the dispatch landed with no test naming it — which also
      left that round's ordered red control with nothing to bite on. R-0704 is the
      same shape inside a state file: the PLANF031R54 slice's Current Step promised a
      checklist round while its own Next Steps held neither, so the file AGENTS.md's
      Session Resume tells the next session to read SECOND routed that session past
      the round it had been re-sequenced to put first. A further instance was found at
      the R55 gate in the reviewer's PLANF031R55 slice and recorded in that round's
      ledger entry without a new id, per item 30: the list held an unnumbered
      checklist round ahead of an item labelled R56, so that label was already wrong
      by one before the round it named had begun. Items 16 and 17 are the neighbours.
      Item 16 resolves a COUNT to the list it names, and item 17 makes a pair that
      changes a structure's ARITY span the whole structure; neither reaches a prose
      sentence naming an ITEM the list does not hold, because no numeral is stated and
      no arity changes — the list is well-formed, correctly numbered, and simply
      missing the thing the paragraph beside it promised.

<<<END S3NEW

── STEP CHECKLIST / F031 — ROUND R55 ──────────────────────────────────
Goal:        Land the §3 pre-emission checklist item that finding R-0703 calls
             for, and repair `.agent/plan.md`, whose R54 revision named a
             checklist round its own Next Steps list no longer held. ONE
             checklist item lands this round; the R-0694 through R-0699 item is
             deliberately NOT in it, because those findings have not been
             re-read from the record and an item written from memory is the
             trap this list exists to close. NO PRODUCTION CODE CHANGES.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the plan
             · C2 the R54 gate entry and R-0704 · C3 the checklist item · C4
             handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f031-r55.md`,
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
 3. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES R54. That is
    ordered: the plan becomes current at C1.
 4. EVERY SLICE IS THE REVIEWER'S TEXT. You never write a `Done:` paragraph and
    never mint a finding id of your own. LEDGER55 carries BOTH units this round
    registers and you add nothing to it. NO FINDING IS RESOLVED THIS ROUND.
 5. THE LEDGER SETS MOVE ONCE, AND THIS ROUND REALLY DOES ADD AN ID. Across C2
    `^- R-\d+ — ` moves 264 to 265 with the ADDED id exactly `R-0704`, and
    `^Gate: F\d+ R\d+ — ` moves 35 to 36 with the ADDED key exactly `F031 R54`.
    `^Done: R-\d+ — ` stays 8, `^Landed: R-` stays 0 and `^Gate: R\d+ — ` stays
    19. The open set is 256 before C2 and 257 after C2.
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

Spec — the one edit to `docs/agents/planner_reviewer_prompt.md`, at C3:
 S1. INSERT S1NEW immediately BEFORE the line
     `  Why this is on disk and not a habit: item 2 has recurred six times across`,
     which the reviewer measured as occurring exactly 1x in that file at
     `84551691`. That line opens the closing paragraph of the §3 pre-emission
     checklist, and item 32 is the last numbered item before it, so S1NEW
     becomes item 33 at the END of the numbered list. S1NEW's own trailing blank
     line is what separates it from that closing paragraph; the blank line that
     already follows item 32 is what separates item 32 from S1NEW. ADD NOTHING
     OF YOUR OWN, and renumber nothing: no item is removed, so no label moves.

Done when — run every gate yourself and record its REAL exit code. G1 through G8
run at commits STRICTLY EARLIER than C4, so the handback can quote them; the
push is ordered after C4 and its reading is NOT written into the handback.
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
 G3. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF031R55 under the
     newline-INCLUDED convention. Run the negative control against the slice
     MINUS its trailing newline and report it FALSE. Report `^## Goal$` 1,
     `^## Next Steps$` 1, and `wc -l` STRICTLY UNDER 50.
 G4. THE APPEND, PROVED TWICE, THE SECOND READER COVERING THE WHOLE APPENDED
     REGION. Read every non-current revision with `git show <rev>:<path>` into
     memory; never write a past blob over a tracked file to read it.
     `.agent/live_review.md` at C2 equals its pre-commit blob plus ONE newline
     plus LEDGER55. The reviewer measured the base blob at `84551691` itself:
     `.agent/live_review.md` is 914510 bytes. If it reads differently before C2,
     something moved that this round did not order — stop and hand back. Report
     both byte counts and the sum. Then confirm with a SECOND, independent
     reader: split the whole file on blank lines, let N be the number of
     paragraphs YOUR SCRIPT COUNTS in that slice — never a number this block
     asserts — and compare the LAST N units of the file against the slice's N
     paragraphs IN ORDER. Report N and the unit count before and after. THE
     NEGATIVE CONTROL GOES ON THE FIRST APPENDED PARAGRAPH, which is the
     position a tail-only reading cannot see: flip ONE byte IN MEMORY inside
     paragraph 1 and report that BOTH readers REJECT it. Never mutate the
     tracked file.
 G5. THE LEDGER SETS. Report at two points — before C2 and after C2 — the
     line-anchored counts of `^- R-\d+ — `, `^Done: R-\d+ — `, `^Landed: R-`,
     `^Gate: R\d+ — ` and `^Gate: F\d+ R\d+ — `, plus the ids and gate keys
     ADDED and REMOVED as SETS, whether all ids are DISTINCT, and the maximum
     id. Every movement constraint 5 names is checked here, INCLUDING the ones
     that must NOT move. Report the open set at both points.
 G6. THE CHECKLIST EDIT. At the base `84551691`, report the count of the S1
     anchor line, which must be 1, and the count of the line `  33. **` , which
     must be 0. At C3 in `docs/agents/planner_reviewer_prompt.md`: S1NEW occurs
     1x, the anchor line still occurs 1x, and a line-anchored `^  33\. \*\*`
     occurs 1x while `^  34\. \*\*` occurs 0x. Report the file's line count at
     the base and at C3 and confirm the difference is exactly S1NEW's own line
     count, which you measure from the slice rather than from this block. Report
     that `git diff --name-only C2..C3` is that one path and nothing else, and
     that the diff for that path has ZERO deleted lines — an insertion removes
     nothing.
 G7. NOTHING ELSE MOVED, MARKERS, PATHS, COMMITS. Compare the path set of
     `git diff --name-only 84551691..C3` BOTH WAYS against this round's expected
     set — the Change line's list MINUS `.agent/handoff.md`, excluded because
     the handback is written at C4, outside a range ending at C3 — and report
     both residues EMPTY. Report `git diff --stat 84551691..C3` restricted to
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
     `tests/orchestration/test_integrity_gate.py`. At `84551691` the reviewer
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
             REVIEWER PROMPT, AND THAT R-0704 IS NOW ON DISK AND OPEN. THE NEXT
             ACTION SECTION NAMES, IN THIS ORDER: re-read `.agent/STOP` from
             disk first, then the Open PR Gate, then review this round's
             handback, then the remaining §3 checklist round that lands the
             R-0694 through R-0699 item together with the counter-measure R-0704
             names, and only then R56, the markup. Obey constraint 8's cap. Then
             push with `git push origin feature/f031-decision-inbox`.
──────────────────────────────────────────────────────────────────────

<<<SLICE PLANF031R55
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
R55 lands the §3 checklist item R-0703 calls for — a vitest colour ordered
inside a worktree must name its config, scope its selection and report the
unmutated control first — and repairs this file, whose R54 revision named a
checklist round its own Next Steps list no longer held (R-0704). The markup is
renumbered to R56, and that renumbering is stated here rather than performed
silently. The R-0694 through R-0699 item is NOT in this round: those six
findings have not been re-read from the record, and an item written from memory
is the trap this list exists to close.

## Next Steps
1. The second §3 checklist item: the R-0694 through R-0699 share — a block reads
   the TARGET before ordering anything against it — landed together with the
   counter-measure R-0704 names, in a round that re-reads all seven findings
   from `.agent/live_review.md` first.
2. R56: the COMPONENT half — the pending card renders a field per open
   clarification and the flow carries the map R53 built.
   `tests/ui_contracts/test_decision_answer_wiring.py` pins the card's call
   string and its two-writer count, so that round moves those guards with it.
3. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- SIX OF THE EIGHT PRODUCING TYPES STILL CANNOT BE ANSWERED THROUGH THE DOOR.
  R-0693 measures the gap; the rest are outside F031's scope, and the inbox
  tells the truth about every one of them rather than offering a refused button.
- THE FORM IS REACHABLE ONLY BY A NON-BROWSER CLIENT UNTIL R56. R53 moved the
  seam to the edge of the markup and no further.
- TWO CONSECUTIVE ROUNDS RAISED A DEFECT IN THE REVIEWER'S OWN BLOCK, both found
  by the worker before the reviewer read the diff. That is the split working,
  but it is also why the checklist rounds outrank the markup.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 256 at `84551691`
  and R-0704 takes it to 257.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R55

<<<SLICE LEDGER55
Gate: F031 R54 — the F031 R54 entry. R54 PASSED ON EVERY GATE ITS BLOCK ORDERED, G1 THROUGH G7, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk. THIS WAS THE RECORD HALF: no production file changed, and its whole purpose was to put R53's verdict and R-0703 on disk before any further work, which docs/agents/planner_reviewer_prompt.md §4 item 4 requires. TRANSPORT HELD: the C0a and C0b blobs are byte-identical at sha256 `fafd25bc…a1e1cb7f` over 19170 bytes and 183 lines and resolve to the SAME git blob `b092f9adff03`; the extraction printed 2 slices with CONTENT 45 and TOTAL 183, so PROSE 138 against 400 and TOTAL 183 against 490. THE PLAN at `8e1d8f89` is byte-equal to PLANF031R54 with the minus-newline control FALSE, `^## Goal$` 1, `^## Next Steps$` 1 and `wc -l` 42. THE APPEND IS EXACT AND ITS SECOND READER COVERED BOTH UNITS: 907384 + 1 + 7125 = 914510 and the committed blob is 914510; N counted by the reviewer's own script is 2, units 369 to 371, the last two units match the slice's two paragraphs IN ORDER, and the byte flip placed on the FIRST appended paragraph — the gate entry, which a tail-only reading cannot see — is REJECTED by BOTH readers. THE SETS MOVED EXACTLY WHERE CONSTRAINT 5 ALLOWED AND THIS ROUND REALLY DID MINT AN ID: `^- R-\d+ — ` 263 to 264 with the ADDED id exactly `R-0703`, `^Gate: F\d+ R\d+ — ` 34 to 35 with the ADDED key exactly `F031 R53`, `^Done: R-\d+ — ` 8, `^Landed: R-` 0 and `^Gate: R\d+ — ` 19 all unmoved, ids DISTINCT with the maximum now `R-0703`, and the open set 255 before C2 and 256 after it. NOTHING ELSE MOVED: both path residues EMPTY over the four expected paths, `apps/`, `docs/`, `packages/` and `tests/` each EMPTY in the range, markers 0 and 0 in the plan and the ledger against a CONTROL of 2 and 2, insertions 183, 113, 16 and 4 with each commit single-parent and under 500, `git ls-files .remedy-wt` 0 lines and `git worktree list` 1 line. THE STATE READERS THE REVIEWER RE-RAN SERIALLY, every one at a REAL exit 0 and every one EQUAL to the base reading, as a round changing no test must leave them: canary 42, `tests/ui_server/` 489, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21 and `tests/orchestration/test_integrity_gate.py` 16. THE HANDBACK IS 59 LINES against the 60-line cap the worker DERIVED ITSELF from a five-commit bundle rather than quoting a tier, which is what constraint 8 asked for. THE ROUND'S ONE OBSERVATION IS A REAL DEFECT IN THE REVIEWER'S OWN SLICE, reported and not corrected exactly as constraint 1 requires, and it is registered as R-0704 below rather than charged to this round. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing table, no unverified completion claim and no silent scope change.

- R-0704 — Low, A PLAN SLICE'S PROSE FORWARD-REFERENCED A ROUND ITS OWN NUMBERED LIST NO LONGER HELD, SO THE FILE `AGENTS.md` SESSION RESUME READS SECOND ROUTES THE NEXT SESSION PAST THE ROUND IT WAS RE-SEQUENCED TO PUT FIRST. The defect is the reviewer's, in the PLANF031R54 slice of the F031 R54 block saved at `2d04fa7f`. FOUND AND DECLARED BY THE WORKER as its single observation, which applied the slice unchanged as constraint 1 required rather than repairing it — the correct behaviour, and the reason the defect is visible at all. MEASURED at `84551691`: `.agent/plan.md`'s Current Step ends "the checklist edit follows, and the markup becomes R55", while its Next Steps holds exactly two items, `1.` R55 the COMPONENT half and `2.` the integration-gate round, so the checklist round the same paragraph promises appears NOWHERE in the list that is supposed to carry it. `.agent/handoff.md` at that same commit names it correctly — "then the §3 checklist round that lands the R-0694 through R-0699 item AND the R-0703 item; and only then R55" — so the two resume artifacts DISAGREE, and the one that disagrees is the one AGENTS.md tells the next session to read before the review record. THE CAUSE IS AN ARITY EDIT: the previous plan carried the reviewer-file round as its item 2, the R54 slice deleted that item because the Current Step now described it, and the Current Step described only the RECORD half — so the prose kept a forward reference whose target the list had lost. Low because `.agent/plan.md` is rewritten every round and this round's own slice repairs it, and because the handoff carried the correct ordering throughout, so no session could have been misled without also ignoring the handback; but it is a real disagreement between the two artifacts a resuming session reads, and it was found by the worker rather than by any gate the block ordered. NOT A DUPLICATE, and the open set was searched for the DEFECT before this id was minted, as §3 item 30 requires: `R-0548` is about a round omitting `.agent/plan.md` from its change set entirely and `R-0447` about a second copy of the round map falling out of step with the first, while this is a single copy disagreeing with ITSELF. THE COUNTER-MEASURE IS A §3 CHECKLIST ITEM AND THIS BLOCK DOES NOT LAND IT: item 16's widening resolves a COUNT to the list it names, and item 17 governs a PAIR that changes a structure's arity, so neither reaches a whole-file slice whose prose names an item the list no longer holds. The item — before emission, read every forward reference in a state slice against the list it points at — lands in the round this round's plan names as its first next step, together with the R-0694 through R-0699 item. OPEN.
<<<END LEDGER55

<<<SLICE S1NEW
  33. **A colour ordered inside a worktree names the runner's configuration, SCOPES
      its selection, and reports the UNMUTATED control beside the mutated one.**
      Finding R-0703. A block may order a vitest red-proof in the disposable
      worktree §4 item 10 and docs/agents/self_drive_protocol.md G5 require, only
      when it ALSO names `--config <primary>/apps/ui/vitest.config.ts` and narrows
      the run to the sources under proof. `apps/ui/node_modules` is gitignored, so
      a fresh worktree carries neither the runner nor a config that can import it;
      and an UNSCOPED run additionally collects
      `src/components/prompt/promptTraceLens.test.ts`, which fails to resolve under
      `--root` and is a worktree artifact rather than a result. Both halves were
      already on disk, in R-0653's own RESOLUTION, and neither had been promoted
      here — which is how a block came to reproduce a defect a RESOLVED finding had
      already solved, the rule-in-a-finding-body class of R-0548 reaching a
      resolution instead of a fix clause. Order the control in the SAME worktree
      BEFORE the mutation and require its exit code beside the mutated one: a
      colour with no baseline is not evidence. Item 5 decides WHETHER a colour may
      be ordered and item 12 pairs the reviewer's own dry run with a red control;
      this one governs whether the ordered command can produce a reading AT ALL in
      the one environment the guardrails permit it to run in, which neither
      reaches, because the recipe is sound and only the ENVIRONMENT defeats it.
      Measured at `fd6e70a9`: as ordered the run exits 1 having loaded nothing;
      with the config but the whole root the UNMUTATED control is still exit 1 at
      466 passed, so red was the answer either way; scoped to `src/api/` the
      unmutated control is a REAL exit 0 at 450 passed and the two mutations are
      exit 1 at 6 and 5 failures. The gate that cannot fail and the gate that
      cannot pass are the same defect wearing two faces.

<<<END S1NEW

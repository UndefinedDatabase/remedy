── STEP RECORD / F031 — ROUND R54 (record half) ───────────────────────
Goal:        Put R53's verdict and the finding R53 exposed onto disk BEFORE any
             further work. R53's probes showed that the reviewer's own block
             ordered a vitest red-proof by a route that cannot run in a worktree
             and whose whole-root form is red unmutated. Findings persist first
             (docs/agents/planner_reviewer_prompt.md §4 item 4), so this round
             registers R-0703 and re-sequences the plan. NO PRODUCTION FILE
             CHANGES, and the §3 checklist edit this finding calls for is NOT in
             this round — it is the next one.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the plan
             · C2 the R53 gate entry and R-0703 · C3 handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f031-r54.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `.agent/handoff.md`. NOTHING UNDER `apps/`, `docs/`, `packages/`
             or `tests/`. `.agent/decisions.md` is not in it either: the
             re-sequencing is a step-size judgement under §3, not a ruling.

Constraints:
 1. EVERY SLICE IS APPLIED BYTE FOR BYTE. Never retype one, never reflow one,
    never fix one. A slice's text is its content lines joined with a newline
    plus ONE trailing newline. If a slice looks wrong, say so in the handback
    and finish the round anyway — a corrected slice destroys the transport
    proof.
 2. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3. No pair may be reordered
    and none may be merged.
 3. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES R53. That is
    ordered: the plan becomes current at C1.
 4. EVERY SLICE IS THE REVIEWER'S TEXT. You never write a `Done:` paragraph and
    never mint a finding id of your own. LEDGER54 carries BOTH units this round
    registers and you add nothing to it.
 5. THE LEDGER SETS MOVE ONCE, AND THIS ROUND REALLY DOES ADD AN ID. Across C2
    `^- R-\d+ — ` moves 263 to 264 with the ADDED id exactly `R-0703`, and
    `^Gate: F\d+ R\d+ — ` moves 34 to 35 with the ADDED key exactly `F031 R53`.
    `^Done: R-\d+ — ` stays 8, `^Landed: R-` stays 0 and `^Gate: R\d+ — ` stays
    19. The open set is 255 before C2 and 256 after C2.
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
push is ordered after C3 and its reading is NOT written into the handback.
 G1. BRANCH, CLEANLINESS, TRANSPORT. Branch is `feature/f031-decision-inbox`.
     `git status --porcelain` prints 0 lines after each of C0a, C0b, C1 and C2.
     `.agent/STOP` read from disk before C0a and before C3, both ABSENT. Report
     the sha256, byte count and line count of this block as saved at C0a, as
     mirrored at C0b, and as read off disk at C2 — all three must be EQUAL — and
     say whether C0a and C0b are the same git blob.
 G2. EXTRACTION AND CAPS. Extract the slices from the COMMITTED C0a blob by
     their marker LINES, never from the prompt. Report how many slices your
     extractor printed, the CONTENT line total, the TOTAL line count, and PROSE
     as TOTAL minus CONTENT. MARKERS ARE PROSE. PROSE must be at most 400 and
     TOTAL at most 490.
 G3. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF031R54 under the
     newline-INCLUDED convention. Run the negative control against the slice
     MINUS its trailing newline and report it FALSE. Report `^## Goal$` 1,
     `^## Next Steps$` 1, and `wc -l` STRICTLY UNDER 50.
 G4. THE APPEND, PROVED TWICE, THE SECOND READER COVERING THE WHOLE APPENDED
     REGION. Read every non-current revision with `git show <rev>:<path>` into
     memory; never write a past blob over a tracked file to read it.
     `.agent/live_review.md` at C2 equals its pre-commit blob plus ONE newline
     plus LEDGER54. The reviewer measured the base blob at `1bff8736` itself:
     `.agent/live_review.md` is 907384 bytes. If it reads differently before C2,
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
     that must NOT move. Report the open set as `^- R-\d+ — ` minus
     `^Done: R-\d+ — ` at both points.
 G6. NOTHING ELSE MOVED, MARKERS, PATHS, COMMITS. Compare the path set of
     `git diff --name-only 1bff8736..C2` BOTH WAYS against this round's expected
     set — the Change line's list MINUS `.agent/handoff.md`, excluded because
     the handback is written at C3, outside a range ending at C2 — and report
     both residues EMPTY. Report `git diff --stat 1bff8736..C2` restricted to
     `apps/`, `docs/`, `packages/` and `tests/` and confirm each is EMPTY.
     Line-anchored `^<<<SLICE ` and `^<<<END ` are 0 and 0 in `.agent/plan.md`
     at C1 and `.agent/live_review.md` at C2, against a CONTROL count over the
     C0a blob, which is not 0. Report each commit's insertions from
     `git diff --numstat` for C0a through C2, confirm each is single-parent and
     under 500. Report `git ls-files .remedy-wt` as 0 and `git worktree list` as
     1 line at C2.
 G7. THE CANARY AND THE STATE READERS. In the PRIMARY checkout at C2, run
     SERIALLY — never two pytest processes alive at once — reporting each REAL
     exit code and count: `python3 -m pytest tests/cli/test_golden_path.py -q`
     (the canary), `tests/ui_server/`,
     `tests/orchestration/test_test_runner.py`,
     `tests/regression/test_resource_safety.py` and
     `tests/orchestration/test_integrity_gate.py`. At `1bff8736` the reviewer
     measured these itself at 42, 489, 52, 21 and 16, every one at exit 0. This
     round changes no test and no production file, so every one must still read
     exactly that; any movement is unexplained and you stop and hand back.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C3: feature and round, branch, the per-commit changed-files table
             with the `+/-` column taken from `git diff --numstat` ITSELF and
             agreeing cell for cell with G6's readings, the item-status table
             covering C0a, C0b, C1, C2, C3 and the push, ONE LINE PER GATE for
             G1 through G7 with its real exit code, the open-findings count
             AFTER this round, and the next expected action. SAY PLAINLY THAT NO
             PRODUCTION FILE CHANGED AND THAT R-0703 IS NOW ON DISK AND OPEN.
             THE NEXT ACTION SECTION NAMES, IN THIS ORDER: re-read `.agent/STOP`
             from disk first, then the Open PR Gate, then review this round's
             handback, then the §3 checklist round that lands the R-0694 through
             R-0699 item AND the R-0703 item, and only then R55, the markup.
             Obey constraint 8's cap. Then push with
             `git push origin feature/f031-decision-inbox`.
──────────────────────────────────────────────────────────────────────

<<<SLICE PLANF031R54
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
R54 is the REVIEWER-FILE round, and it now runs BEFORE the markup rather than
after it. R53's probes exposed a second checklist gap — a block ordered a vitest
red-proof inside a worktree by a route that cannot run there, and whose
whole-root control is red UNMUTATED — so the markup round, which needs exactly
such probes, would walk into the same trap. This half registers R-0703 and
re-sequences; the checklist edit follows, and the markup becomes R55.

## Next Steps
1. R55: the COMPONENT half — the pending card renders a field per open
   clarification and the flow carries the map R53 built.
   `tests/ui_contracts/test_decision_answer_wiring.py` pins the card's call
   string and its two-writer count, so that round moves those guards with it.
2. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- SIX OF THE EIGHT PRODUCING TYPES STILL CANNOT BE ANSWERED THROUGH THE DOOR.
  R-0693 measures the gap; the rest are outside F031's scope, and the inbox
  tells the truth about every one of them rather than offering a refused button.
- THE FORM IS REACHABLE ONLY BY A NON-BROWSER CLIENT UNTIL R55. R53 moved the
  seam to the edge of the markup and no further.
- A VITEST RED-PROOF IN A WORKTREE NEEDS BOTH `--config <primary>` AND A SCOPED
  SELECTION. R-0653's own resolution recorded this at F022 R7 and nothing
  promoted it into the checklist, which is why R53's block repeated it.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 255 at `1bff8736`
  and R-0703 takes it to 256.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R54

<<<SLICE LEDGER54
Gate: F031 R53 — the F031 R53 entry. R53 PASSED ON EVERY GATE ITS BLOCK ORDERED, G1 THROUGH G8, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk; every value the handback states reproduced. TRANSPORT HELD: the C0a and C0b blobs are byte-identical at sha256 `d6cdc987…679e2cc4` over 24310 bytes and 294 lines, the SAME git blob `3ab1efc9a25d`, and the extraction printed 2 slices with CONTENT 46 and TOTAL 294, so PROSE 248 against 400 and TOTAL 294 against 490 — equal to the reviewer's own pre-emission measurement of the same bytes. THE PLAN at `e0648abd` is byte-equal to PLANF031R53 with the minus-newline control FALSE, `^## Goal$` 1, `^## Next Steps$` 1 and `wc -l` 45. THE APPEND IS EXACT: 903306 + 1 + 4077 = 907384 and the committed blob is 907384; N counted by the reviewer's own script is 1, units 368 to 369, the last N units match in order, and the byte flip on the FIRST appended paragraph is REJECTED by BOTH readers. THE SETS MOVED ONLY WHERE CONSTRAINT 6 ALLOWED: `^Gate: F\d+ R\d+ — ` 33 to 34 with the ADDED key exactly `F031 R52`; `^- R-\d+ — ` 263, `^Done: R-\d+ — ` 8, `^Landed: R-` 0 and `^Gate: R\d+ — ` 19 unmoved at all three points; ids DISTINCT, maximum `R-0702`, open set 255 before C2 and 255 after C3. THE PRODUCTION CHANGE WAS READ LINE BY LINE AND IS FAITHFUL TO ITS SPEC: `fd6e70a9` adds `DecisionClarification` and a total `cardClarifications` reader that drops a blank-id entry, projects `payload.clarifications` onto the model, gives `DecisionResolveArgs` an OPTIONAL `answers` and `buildDecisionResolveCommand` an OPTIONAL fourth parameter spread in through `clarificationAnswersArg`, which OMITS the key rather than sending it empty. THE ARGS KEY IS THE ONE THE DOOR READS: the reviewer parsed `_dispatch_decision_resolve` at `1bff8736` and it reads exactly `decision_id` and `answer`, plus `answers` inside `_validated_clarification_answers`, so S4's rewritten header sentence naming those three is TRUE rather than merely different. THE TWO WHOLE-MODEL `toEqual` ASSERTIONS WERE UPDATED BY PURE INSERTION of `clarifications: [],` — `decisionCard.test.ts` and `decisionAnswer.test.ts` are each +121/-0 and +113/-0, so no assertion was deleted or weakened to make a red go away. THE SUITES THE REVIEWER RE-RAN ITSELF: `npx tsc --noEmit` REAL exit 0; `npx vitest run --root .` REAL exit 0 at 30 files and 475 tests against 30 and 455 at the base, the 20 new tests being this round's; and serially in the primary checkout canary 42, `tests/ui_contracts/` 561 passed with 4 skipped, `tests/ui_server/` 489, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21 and `tests/orchestration/test_integrity_gate.py` 16, every one at exit 0 and every one EQUAL to the base reading — `tests/ui_contracts/` unmoved is what proves this round left the markup and its guards alone. NOTHING ELSE MOVED: both path residues EMPTY over the eight expected paths, `packages/`, `docs/` and `tests/` each EMPTY in the range, markers 0 and 0 in all six targets against a CONTROL of 2 and 2, insertions 294, 194, 16, 2 and 351 with each commit single-parent and under 500, `git ls-files .remedy-wt` 0 lines, `git worktree list` 1 line, reflog prefixes all `commit` with `amend`, `rebase` and `cherry` 0 each. THE HANDBACK IS 91 LINES inside its cap, and the push landed with the remote ref equal to the local tip. THE ROUND'S THREE DECLARED DEVIATIONS ARE ALL ABOUT THE REVIEWER'S OWN PROBE RECIPE AND ARE ALL CORRECT — the reviewer reproduced each in its own worktree — and they are registered as R-0703 rather than charged to this round. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing table, no unverified completion claim and no silent scope change.

- R-0703 — Medium, A BLOCK ORDERED A VITEST RED-PROOF INSIDE A WORKTREE BY A ROUTE THAT CANNOT RUN THERE, AND WHOSE REPAIRED WHOLE-ROOT FORM IS RED WITH NO MUTATION AT ALL, SO THE PROBE PROVED NOTHING IN EITHER SHAPE. The defect is the reviewer's, in the F031 R53 block saved at `8bb58a2d`, whose G7(c) and G7(d) ordered `npx vitest run --root <worktree>/apps/ui` from the primary `apps/ui`. FOUND AND DECLARED BY THE WORKER, which repaired it on its own initiative and reported all three deviations before the reviewer read the diff. MEASURED BY THE REVIEWER ITSELF at `fd6e70a9` in its own disposable worktree, not inferred: as ordered, the run exits 1 having loaded nothing, because a fresh worktree carries no `apps/ui/node_modules` and the worktree's own `vitest.config.ts` cannot import `vitest`; adding `--config <primary>/apps/ui/vitest.config.ts` makes it run, and the UNMUTATED control is then STILL exit 1 — 1 failed file, 29 passed, 466 tests passed — because `src/components/prompt/promptTraceLens.test.ts` fails to resolve under `--root` and is a worktree artifact rather than a result. So the ordered colour was unreachable and the obvious repair is VACUOUS: red is the answer whether or not the code under proof is mutated, which is the R-0438 class arriving through the harness instead of through a path. SCOPED to `src/api/` the same command discriminates properly: the unmutated control is a REAL exit 0 at 27 files and 450 tests, reverting `clarifications` to an unconditional empty array gives exit 1 with 6 failures, and making the builder ignore its fourth parameter gives exit 1 with 5 failures — the two readings the worker reported, reproduced independently. NOT A DUPLICATE, and the open set was searched for the DEFECT before this id was minted, as §3 item 30 requires: `R-0518` is the closest OPEN neighbour and is about a pytest node needing a gitignored build directory, `R-0591` is about `copytree`'s symlink default and `R-0577` about a probe recipe that can only fail — none of them names the vitest route. `R-0653` DOES name it, exactly and correctly, in its RESOLUTION at F022 R7: that text records the working form `npx vitest run <file> --root <worktree>/apps/ui --config <primary>/apps/ui/vitest.config.ts`, and records as "part of the resolution, not a residual" that an unscoped worktree run also collects `promptTraceLens.test.ts` and must therefore be scoped. R-0653 is Done, so this evidence cannot be added to it. THAT IS THE ROOT CAUSE AND IT IS THE ONE THE CHECKLIST EXISTS FOR: both halves of the correct recipe were already on disk, in a resolution the reviewer wrote, and nothing promoted either into §3 — so the next block needing them did not read them, which is the rule-in-a-finding-body class R-0548 already recorded. Medium because a vacuous red-proof certifies a guard nobody has shown to fire, and the next round is the markup round, which needs exactly these probes. THE FIX IS A §3 CHECKLIST ITEM, landing in R54 beside the R-0694 through R-0699 item: a block that orders a vitest colour inside a worktree names `--config <primary>/apps/ui/vitest.config.ts`, SCOPES the selection to the sources under proof, and orders the UNMUTATED control in that same worktree FIRST, reporting its exit code beside the mutated one — a colour ordered without its control is a reading with no baseline. OPEN.
<<<END LEDGER54

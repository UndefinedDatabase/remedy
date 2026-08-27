── STEP FORM / F031 — ROUND R53 ───────────────────────────────────────
Goal:        Build the MODEL and COMMAND halves of the FORM. The card model
             gains the plan's open questions from `payload.clarifications`, and
             the answer builder learns to carry the `answers` map R51's door
             already validates. NO MARKUP CHANGES: the component is R54, because
             DECISION F031 D5 rules branching into the layer vitest reaches and
             this repository ships no DOM harness.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the plan
             · C2 the R52 gate entry · C3 the model, the builder and their tests
             · C4 handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f031-r53.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `apps/ui/src/api/decisionCard.ts`,
             `apps/ui/src/api/decisionCard.test.ts`,
             `apps/ui/src/api/decisionAnswer.ts`,
             `apps/ui/src/api/decisionAnswer.test.ts`, `.agent/handoff.md`.
             NOTHING UNDER `packages/`, `docs/` OR `tests/`, and no file under
             `apps/` other than those named. In particular
             `apps/ui/src/components/panels/DecisionInboxCard.tsx`,
             `apps/ui/src/api/decisionAnswerFlow.ts` and
             `tests/ui_contracts/test_decision_answer_wiring.py` ARE NOT IN THIS
             CHANGE SET: they are R54's, and G8 proves this round left them put.
             `.agent/decisions.md` is not in it either — D26 already rules the
             contract this round builds against, so no decision is ruled here.

Constraints:
 1. THE PRODUCTION CHANGE IS DESCRIBED, NOT SLICED. The Spec below fixes
    behaviour, public surface and honesty rules; you write the code under
    AGENTS.md's self-review loop and its file-editing safety rules. Only the
    `.agent/` state texts are byte-verbatim slices.
 2. EVERY SLICE IS APPLIED BYTE FOR BYTE. Never retype one, never reflow one,
    never fix one. A slice's text is its content lines joined with a newline
    plus ONE trailing newline. If a slice looks wrong, say so in the handback
    and finish the round anyway — a corrected slice destroys the transport
    proof.
 3. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4. No pair may be
    reordered and none may be merged.
 4. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES R52. That is
    ordered: the plan becomes current at C1.
 5. EVERY SLICE IS THE REVIEWER'S TEXT. You never write a `Done:` paragraph and
    never mint a finding id. NO FINDING IS REGISTERED OR RESOLVED THIS ROUND.
 6. THE LEDGER SETS MOVE ONCE. Across C2 the gate-key pattern
    `^Gate: F\d+ R\d+ — ` moves 33 to 34 with the ADDED key exactly `F031 R52`.
    Across the whole round `^- R-\d+ — ` stays 263, `^Done: R-\d+ — ` stays 8,
    `^Landed: R-` stays 0 and `^Gate: R\d+ — ` stays 19. The open set is 255
    before C2 and 255 after C3.
 7. RE-READ `.agent/STOP` FROM DISK before C0a and again before C4. If it exists
    at either reading, finish the commit in hand, write the handback and STOP.
    Never create it, never delete it.
 8. DESTRUCTIVE VERIFICATION IS ISOLATED. G7's probe runs ONLY inside a
    disposable `git worktree` you create under `.remedy-wt/` and remove again BY
    ITS EXACT PATH before C4 — never by glob, and never in the primary checkout,
    which reads `git status --porcelain` 0 lines at every commit. Earlier
    rounds' scratch under `.remedy-wt/` is left alone; nothing there is ever
    committed. A FRESH WORKTREE HAS NO `node_modules`, so run vitest against it
    with `npx vitest run --root <worktree>/apps/ui` FROM THE PRIMARY CHECKOUT's
    `apps/ui` directory, which is where the installed dependencies live.
 9. YOUR HANDBACK'S CAP. AGENTS.md gives 60 lines at most, or 100 at most when
    per-commit tables of more than five commits require it. THERE IS NO TIER
    ABOVE 100. Derive your cap from the commits the Bundle above orders and stay
    inside it; if the MANDATED content genuinely does not fit, write the
    DECISION D15 "Deviations, declared" line naming your actual line count and
    the specific mandated content that caused the overage. Do not invent a tier.
10. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `cp`, brace literals containing a quote character, `cd x && y`,
    and every form of environment assignment. Route anything that counts, hashes
    or compares through a quoted python heredoc, read real exit codes from
    `subprocess.run(...).returncode`, pass `cwd=` rather than `cd`, and copy
    with `shutil.copyfile`. Run pytest SERIALLY — never two pytest processes
    alive at once. `--timeout` IS NOT AVAILABLE to pytest here: passing it exits
    4 and reports no failure at all.

Spec — the `apps/ui` files of the change set, at C3. Write the code; the
numbered items fix what it must do, and every WHY comment named below is one
sentence directly above its definition (AGENTS.md, Code Discoverability
Conventions).
 S1. `apps/ui/src/api/decisionCard.ts` gains an exported interface
     `DecisionClarification` with exactly the string fields `id`, `question`,
     `defaultAnswer` and `impact`. The endpoint sends `id`, `question`,
     `default_answer` and `impact` — `packages/orchestration/flight_plan.py`
     `open_clarification_questions` builds every record with those keys and
     `str()`-coerces each — so the two spellings differ ONLY in case convention,
     exactly as `taskId` already differs from `task_id` on this model.
 S2. The same module gains a module-level reader for `payload.clarifications`,
     in the shape `payloadOptions` and `payloadTaskId` already have: a payload
     that is not an object, or is null, yields no clarifications rather than
     throwing. `DecisionCardModel` gains `clarifications: DecisionClarification[]`
     and `buildDecisionCardModel` fills it. THE READING IS TOTAL: a non-array
     value, a non-object entry and a non-string field each fall back rather than
     raise, so no payload makes the model throw — the property
     `decisionCard.test.ts` already asserts for the whole model.
     AN ENTRY WHOSE `id` IS BLANK AFTER TRIMMING IS DROPPED, and its WHY comment
     carries this fact: R51's `_validated_clarification_answers` refuses the
     WHOLE request when any answered id is unknown to the plan, so a field the
     operator can fill but never submit would cost them every OTHER answer in
     the same post. Dropping is not losing the question — `decision_queue.py`
     writes the open-question COUNT into the card's own `safe_summary`.
 S3. `apps/ui/src/api/decisionAnswer.ts`: `DecisionResolveArgs` gains an
     OPTIONAL `answers?: Record<string, string>`, and
     `buildDecisionResolveCommand` gains a fourth parameter, OPTIONAL, of that
     type. Every existing call site passes nothing and the body it builds stays
     byte-identical to today's — that is the property G6 and G7(b) measure.
     THE KEY IS OMITTED, NEVER SENT EMPTY, whenever nothing survives the
     filtering below: R51's validator reads an ABSENT `answers` as "accept every
     default" and that is DECISION F031 D24's original contract, so omission is
     the one spelling that keeps a client written before this form valid.
     AN ENTRY WHOSE VALUE IS BLANK AFTER TRIMMING IS DROPPED rather than
     refused, and the WHY comment says why: per question, absent already MEANS
     the default, so an untouched field posts as the default the operator saw
     beside it. The values that ARE sent are TRIMMED, for the reason this
     function already trims `answer` — the record is durable.
 S4. THE HEADER COMMENT OF `decisionAnswer.ts` IS NOW FALSE AND THIS ROUND FIXES
     IT. Read at `e62726c7`, the `DecisionResolveArgs` doc comment says
     `_dispatch_decision_resolve` "reads exactly these two and nothing else",
     which R51 falsified when it taught the door `args.answers`. Rewrite that
     sentence so it names the third key and stays true. Change no other sentence
     of that header. Leaving a false sentence in shipped code beside a correct
     change is the defect R51's own round was credited with catching.
 S5. THE TESTS, in the two `.test.ts` files named in the change set. Cover at
     least: the fields S1 names, projected from a real endpoint-shaped payload;
     a missing, null and non-object payload each giving no clarifications; a
     non-array `clarifications`; a blank-id entry dropped; a builder call with
     no fourth argument producing a body with NO `answers` key; a call whose map
     survives filtering carrying it; an all-blank map omitting it; and values
     arriving trimmed. `decisionCard.test.ts` CARRIES WHOLE-MODEL `toEqual`
     ASSERTIONS THAT PIN EVERY KEY OF THE MODEL — the reviewer counted two at
     `e62726c7` — and they go red the moment S2 lands. Update every one of them
     in the SAME commit. Add tests; delete none, and weaken no assertion to make
     a red go away.

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
 G3. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF031R53 under the
     newline-INCLUDED convention. Run the negative control against the slice
     MINUS its trailing newline and report it FALSE. Report `^## Goal$` 1,
     `^## Next Steps$` 1, and `wc -l` STRICTLY UNDER 50.
 G4. THE APPEND, PROVED TWICE, THE SECOND READER COVERING THE WHOLE APPENDED
     REGION. Read every non-current revision with `git show <rev>:<path>` into
     memory; never write a past blob over a tracked file to read it.
     `.agent/live_review.md` at C2 equals its pre-commit blob plus ONE newline
     plus LEDGER53. The reviewer measured the base blob at `e62726c7` itself:
     `.agent/live_review.md` is 903306 bytes. If it reads differently before C2,
     something moved that this round did not order — stop and hand back. Report
     both byte counts and the sum. Then confirm with a SECOND, independent
     reader: split the whole file on blank lines, let N be the number of
     paragraphs YOUR SCRIPT COUNTS in that slice — never a number this block
     asserts — and compare the LAST N units of the file against the slice's N
     paragraphs IN ORDER. Report N and the unit count before and after. THE
     NEGATIVE CONTROL GOES ON THE FIRST APPENDED PARAGRAPH: flip ONE byte IN
     MEMORY inside paragraph 1 and report that BOTH readers REJECT it. If N is
     1, say so and note that paragraph 1 is also the last. Never mutate the
     tracked file.
 G5. THE LEDGER SETS. Report at three points — before C2, after C2, after C3 —
     the line-anchored counts of `^- R-\d+ — `, `^Done: R-\d+ — `,
     `^Landed: R-`, `^Gate: R\d+ — ` and `^Gate: F\d+ R\d+ — `, plus the ids and
     gate keys ADDED and REMOVED as SETS at each step, whether all ids are
     DISTINCT, and the maximum id. Every movement constraint 6 names is checked
     here, INCLUDING the ones that must NOT move. Report the open set as
     `^- R-\d+ — ` minus `^Done: R-\d+ — ` before C2 and after C3.
 G6. THE BUILDER'S OLD CALLERS ARE UNTOUCHED. At C3, in a python heredoc, report
     how many calls to `buildDecisionResolveCommand(` in
     `apps/ui/src/api/decisionAnswer.test.ts` pass THREE arguments, and quote
     the declaration line of S3's new parameter to show it is OPTIONAL. Then
     report that `git diff e62726c7..C3 -- apps/ui/src/api/decisionAnswer.ts`
     contains NO deleted line matching `decision_id` and none matching
     `answer: trimmedAnswer` — the keys the old body sends, which a rewrite
     rather than an addition would have moved.
 G7. THE SUITES, AND THAT THE NEW TESTS REALLY GUARD.
     (a) `npx tsc --noEmit` with `cwd` `apps/ui` at C3, REAL exit 0. The
         reviewer ran that exact command line at `e62726c7` and it exits 0
         there, so a red here is this round's own doing.
     (b) `npx vitest run --root .` with `cwd` `apps/ui` at C3, REAL exit 0.
         Report the test-FILE count and the TEST count. At `e62726c7` the
         reviewer measured 30 files and 455 tests. DO NOT PREDICT the new
         numbers: report what you measure and say how each compares.
     (c) THE FIRST PROBE, in a disposable worktree at C3 under `.remedy-wt/`,
         never in the primary checkout, run per constraint 8. In THAT
         WORKTREE's copy of `apps/ui/src/api/decisionCard.ts`, make
         `buildDecisionCardModel` fill `clarifications` with an empty array
         unconditionally — the one-line revert of S2's behaviour — and run
         vitest against that worktree. REPORT THE REAL EXIT CODE, WHICH MUST BE
         NON-ZERO. Then remove that worktree by its exact path and report
         `git worktree list` back to 1 line. A green here would mean S5's model
         tests guard nothing.
     (d) THE SECOND PROBE, the same way, in a FRESH worktree: make
         `buildDecisionResolveCommand` ignore its fourth parameter entirely and
         run vitest against that worktree. REPORT THE REAL EXIT CODE, WHICH
         MUST BE NON-ZERO, then remove that worktree by its exact path. The
         probes are separate because one green would otherwise hide behind the
         other's red.
 G8. NOTHING ELSE MOVED, MARKERS, PATHS, COMMITS, AND THE UNTOUCHED GUARDS.
     Compare the path set of `git diff --name-only e62726c7..C3` BOTH WAYS
     against this round's expected set — the Change line's list MINUS
     `.agent/handoff.md`, excluded because the handback is written at C4,
     outside a range ending at C3 — and report both residues EMPTY. Report
     `git diff --stat e62726c7..C3` restricted to `packages/`, `docs/` and
     `tests/` and confirm each is EMPTY. Line-anchored `^<<<SLICE ` and
     `^<<<END ` are 0 and 0 in `.agent/plan.md` at C1, `.agent/live_review.md`
     at C2 and each of the four `apps/ui` files at C3, against a CONTROL count
     over the C0a blob, which is not 0. Report each commit's insertions from
     `git diff --numstat` for C0a through C3, confirm each is single-parent and
     under 500. Report `git ls-files .remedy-wt` as 0 and `git worktree list` as
     1 line at C3. Report the reflog FOR THIS ROUND'S OWN COMMITS ONLY: every
     operation prefix must read `commit`, and among those entries `amend`,
     `rebase` and `cherry` must be 0 each. Do not count those words over the
     whole reflog. THEN, IN THE PRIMARY CHECKOUT AT C3, RUN SERIALLY — never
     two pytest processes alive at once — reporting each REAL exit code and
     count: `python3 -m pytest tests/cli/test_golden_path.py -q` (the canary),
     `tests/ui_contracts/`, `tests/ui_server/`,
     `tests/orchestration/test_test_runner.py`,
     `tests/regression/test_resource_safety.py` and
     `tests/orchestration/test_integrity_gate.py`. At `e62726c7` the reviewer
     measured these itself at 42, 561 passed with 4 skipped, 489, 52, 21 and 16,
     every one at exit 0. `tests/ui_contracts/` IS THE ONE THAT MUST NOT MOVE:
     it reads the card, the flow and the stylesheet this round does not touch,
     so any movement there is scope drift — stop and hand back.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C4: feature and round, branch, the per-commit changed-files table
             with the `+/-` column taken from `git diff --numstat` ITSELF and
             agreeing cell for cell with G8's readings, the item-status table
             covering C0a, C0b, C1, C2, C3, C4 and the push, ONE LINE PER GATE
             for G1 through G8 with its real exit code, the open-findings count,
             and the next expected action. SAY PLAINLY WHETHER THE BRANCH TIP IS
             GREEN, WHAT BOTH OF G7's PROBES RETURNED, AND THAT NO FILE OUTSIDE
             `apps/ui/src/api/` AND `.agent/` CHANGED THIS ROUND. THE NEXT
             ACTION SECTION NAMES, IN THIS ORDER: re-read `.agent/STOP` from
             disk first, then the Open PR Gate, then review this round's
             handback, then R54. Obey constraint 9's cap. Then push with
             `git push origin feature/f031-decision-inbox`.
──────────────────────────────────────────────────────────────────────

<<<SLICE PLANF031R53
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
R53 builds the MODEL and COMMAND halves of the FORM and stops there. The card
model gains the plan's open questions from `payload.clarifications`, and the
answer builder learns to carry the `answers` map R51's door already validates.
Both halves are pure and the shipped vitest config reaches both, which is why
the markup is R54: DECISION F031 D5 rules branching into this layer.

## Next Steps
1. R54: the COMPONENT half — the pending card renders a field per open
   clarification and the flow carries the map this round builds.
   `tests/ui_contracts/test_decision_answer_wiring.py` pins the card's call
   string and its two-writer count, so that round moves those guards with it.
2. A reviewer-file round landing the §3 checklist item R-0694 through R-0699
   share: a block reads the TARGET before ordering anything against it — every
   guard whose ruled set the change widens, every constant a test compares
   against, and every fixture whose state decides an outcome.
3. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- SIX OF THE EIGHT PRODUCING TYPES STILL CANNOT BE ANSWERED THROUGH THE DOOR.
  R-0693 measures the gap; the rest are outside F031's scope, and the inbox
  tells the truth about every one of them rather than offering a refused button.
- THE FORM IS REACHABLE ONLY BY A NON-BROWSER CLIENT UNTIL R54. This round moves
  the seam to the edge of the markup and no further.
- TWO WHOLE-MODEL `toEqual` ASSERTIONS IN `decisionCard.test.ts`, counted at
  `e62726c7`, PIN EVERY KEY OF `DecisionCardModel`, so a new field turns them
  red in the commit that adds it. That is the guard working, not a regression.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 255 at `e62726c7`
  and this round leaves it at 255.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R53

<<<SLICE LEDGER53
Gate: F031 R52 — the F031 R52 entry. R52 PASSED ON EVERY GATE ITS BLOCK ORDERED, G1 THROUGH G8, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk rather than reading the handback back; every value that handback states reproduced. THE STRONGEST CHECK IS AGAIN ONE THE BLOCK DID NOT ORDER: the reviewer applied S1, S2 and S3 to the base blob of `tests/ui_server/test_command_channel.py` independently, in memory, and the landed file at `e745f93d` is BYTE-IDENTICAL to that simulation, so the worker applied exactly what was specified and nothing else. TRANSPORT HELD: the C0a blob and the C0b blob are byte-identical at sha256 `2ce15158…2829d1d7` over 24953 bytes and 319 lines, and both resolve to the SAME git blob `f929a5e26850`. THE EXTRACTION printed 7 slices, CONTENT 109 and TOTAL 319, so PROSE was 210 against 400 and TOTAL 319 against 490. THE BASE ASSERTIONS REPRODUCED: S1FROM and S2FROM each 1x at `743a8f7b`, the S3 anchor 1x, and `TO contains FROM` FALSE on both pairs, so each really was the REWRITE the spec declared; at C3 S1FROM and S2FROM are 0x, S1TO, S2TO and S3NEW 1x each, and `git diff --name-only` across C2..C3 is that one path alone. THE PLAN at `cdc8ab16` is byte-equal to PLANF031R52 with the minus-newline control FALSE, `^## Goal$` 1, `^## Next Steps$` 1 and `wc -l` 46. THE APPEND IS EXACT: 898056 + 1 + 5249 = 903306 and the committed blob is 903306; N counted by the reviewer's own script is 1, units 367 to 368, the last N units match the slice in order, and the byte flip placed on the FIRST appended paragraph is REJECTED by BOTH readers. THE SETS MOVED ONLY WHERE CONSTRAINT 6 ALLOWED: `^Gate: F\d+ R\d+ — ` 32 to 33 with the ADDED key exactly `F031 R51` and none removed; `^- R-\d+ — ` 263, `^Done: R-\d+ — ` 8, `^Landed: R-` 0 and `^Gate: R\d+ — ` 19 all unmoved at all three points; no id added or removed; ids DISTINCT with the maximum `R-0702`; open set 255 before C2 and 255 after C3. THE PROBE DISCRIMINATES AND THE REVIEWER RE-RAN IT ITSELF in its own disposable worktree rather than accepting the report: the three-line validation sequence counts exactly 1, and replacing it with `answers = {}` turns `tests/ui_server/test_command_channel.py` RED at a REAL exit code of 1 with exactly two failures — the two tests this round adds and no others — so they really do guard R51's third refusal rather than nothing; the worktree was removed by its exact path and `git worktree list` returned to 1 line. RUFF over the edited test file is REAL exit 0 at C3 and was also 0 at the base read through `--stdin-filename`, so the gate was not vacuous and no past blob was ever written over a tracked file. THE SUITES THE REVIEWER RE-RAN SERIALLY IN THE PRIMARY CHECKOUT, every one at a REAL exit 0: canary 42, `tests/ui_server/` 489 against 487 at the base — exactly the two tests S3 adds — `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21 and `tests/orchestration/test_integrity_gate.py` 16. NOTHING ELSE MOVED: both path residues are EMPTY over the five expected paths, `apps/`, `docs/` and `packages/` are each EMPTY in the range, the marker sweep reads 0 and 0 in all three targets against a CONTROL of 7 and 7 over the C0a blob, the insertions are 319, 212, 13, 2, 45 and 54 with each commit single-parent and under 500, `git ls-files .remedy-wt` is 0 lines, `git worktree list` is 1 line, and the reflog entries for this round's own six commits all read prefix `commit` with `amend`, `rebase` and `cherry` 0 each among them. THE HANDBACK IS EXACTLY 100 LINES, the ceiling AGENTS.md gives when per-commit tables of more than five commits require it, so no DECISION D15 line was owed, and its per-commit `+/-` column agrees cell for cell with `git diff --numstat` — the R-0592 class, checked rather than assumed. THE PUSH LANDED: the remote branch ref equals the local tip `e62726c7`, so the item-status row claiming it is true on disk. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing table, no unverified completion claim and no silent scope change.
<<<END LEDGER53

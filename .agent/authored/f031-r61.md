STEP SEAM ROUND / F031 — ROUND R61
Goal:        Write the R60 verdict. Then land the SEAM half of the clarification
             form: `buildDecisionSendRequest` and `answerDecisionCard` forward
             the answers map `buildDecisionResolveCommand` has accepted since
             R51, with vitest tests for both hops. NO COMPONENT AND NO
             STYLESHEET IS TOUCHED, and no `docs/` file and no decision.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the plan
             · C2 the R60 gate entry · C3 the send hop and its tests · C4 the
             flow hop and its tests · C5 handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f031-r61.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `apps/ui/src/api/decisionSend.ts`,
             `apps/ui/src/api/decisionSend.test.ts`,
             `apps/ui/src/api/decisionAnswerFlow.ts`,
             `apps/ui/src/api/decisionAnswerFlow.test.ts`, `.agent/handoff.md`.
             NOTHING under `apps/ui/src/components/`, nothing under `packages/`,
             nothing under `tests/`, nothing under `docs/`. In particular
             `apps/ui/src/components/panels/DecisionInboxCard.tsx`,
             `apps/ui/src/components/panels/RightLivePanel.module.css` and
             `tests/ui_contracts/test_decision_answer_wiring.py` are NOT in the
             change set: the markup half is a later round.

Constraints:
 1. THE TWO STATE SLICES ARE APPLIED BYTE FOR BYTE. Never retype one, never
    reflow one, never fix one. A slice's text is its content lines joined with a
    newline plus ONE trailing newline. If a slice looks wrong, say so in the
    handback and finish the round anyway — a corrected slice destroys the
    transport proof. THE CODE IS NOT SLICED: S1 through S4 below DESCRIBE the
    edits and you write the TypeScript yourself, in the surrounding files' own
    idiom.
 2. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4, C5. No pair may be
    reordered and none may be merged.
 3. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES R60. That is
    ordered: the plan becomes current at C1.
 4. EVERY LEDGER SLICE IS THE REVIEWER'S TEXT. You never write a `Done:`
    paragraph of your own and never mint a finding id. LEDGER61 carries the R60
    gate entry and nothing else. NO FINDING IS RESOLVED THIS ROUND.
 5. THE LEDGER SETS MOVE ONCE. Across C2 `^Gate: F\d+ R\d+ — ` moves 41 to 42
    with the ADDED key exactly `F031 R60`. `^- R-\d+ — ` stays 268,
    `^Done: R-\d+ — ` stays 16, `^Landed: R-` stays 0 and `^Gate: R\d+ — `
    stays 19. The open set is 252 before C2 and 252 after C2.
 6. TWO GUARDS BIND THE FLOW FILE AND NEITHER IS IN YOUR CHANGE SET.
    `tests/ui_contracts/test_decision_answer_wiring.py` reads the RAW text of
    `apps/ui/src/api/decisionAnswerFlow.ts` and requires the string
    `DecisionInboxCard.tsx` to be PRESENT and the string `R37` to be ABSENT.
    Whatever you add to that file's header keeps the first and introduces no
    round number at all — name DECISION ids and file paths, never a round.
 7. THE CARD IS NOT TOUCHED, SO ITS PINNED CALL STRING MUST NOT MOVE. That same
    test asserts `answerDecisionCard(target, decision, answer.value)` occurs in
    the card. Your signature change is source-compatible with a three-argument
    call by construction — the new parameter is OPTIONAL — and G6 re-runs that
    suite to prove it.
 8. RE-READ `.agent/STOP` FROM DISK before C0a and again before C5. If it exists
    at either reading, finish the commit in hand, write the handback and STOP.
    Never create it, never delete it.
 9. THE ONLY DESTRUCTIVE VERIFICATION IS G7's, AND IT RUNS IN A DISPOSABLE
    WORKTREE UNDER `.remedy-wt/`, NEVER IN THE PRIMARY CHECKOUT. The primary
    reads `git status --porcelain` 0 lines at every commit, and the worktree is
    removed and pruned before C5.
10. YOUR HANDBACK'S CAP. AGENTS.md gives 60 lines at most, or 100 at most when
    per-commit tables of MORE THAN FIVE commits require it. Count the commits
    the Bundle above orders and derive your cap from that count yourself. Write
    the DECISION D15 "Deviations, declared" line ONLY if the MANDATED content
    genuinely does not fit, and if you write it, name what actually caused the
    overage — blank separator lines are not mandated content, and R-0582 records
    that this declaration has become automatic.
11. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `cp`, brace literals containing a quote character, `cd x && y`,
    and every form of environment assignment. Route anything that counts, hashes
    or compares through a quoted python heredoc, read real exit codes from
    `subprocess.run(...).returncode`, and pass `cwd=` rather than `cd`. Run
    pytest SERIALLY — never two pytest processes alive at once. `--timeout` IS
    NOT AVAILABLE to pytest here: passing it exits 4 and reports no failure.

Spec — the code, DESCRIBED. Write it yourself in each file's own idiom.
 S1. `apps/ui/src/api/decisionSend.ts`, at C3. Give
     `buildDecisionSendRequest` a FIFTH parameter,
     `clarificationAnswers?: Record<string, string>`, after `clientNonce`, and
     pass it as the FOURTH argument of `buildDecisionResolveCommand`. Change
     nothing else: the two refusals, the header map, the path and the
     serialisation stay exactly as they are. Extend the header's "IT COMPOSES,
     IT DOES NOT RE-DERIVE" paragraph with the fact that the map is FORWARDED
     rather than read here, that every refusal it can earn is still
     `decisionAnswer.ts`'s, and that omitting the argument builds the
     byte-identical request every existing call site already builds.
 S2. `apps/ui/src/api/decisionSend.test.ts`, at C3. Add cases, in the file's
     existing style, for: omitting the map builds a body whose `args` carries NO
     `answers` key; a map with one filled value builds `args.answers` holding
     that question id with its value TRIMMED; a map whose every value is blank
     after trimming builds a body with NO `answers` key; and the map reaches
     NEITHER the path NOR the headers. The last one is the transposition guard
     R-0684 earned, one layer up.
 S3. `apps/ui/src/api/decisionAnswerFlow.ts`, at C4. Give `answerDecisionCard` a
     FOURTH parameter, `clarificationAnswers?: Record<string, string>`, and move
     `deps` to FIFTH. Widen `DecisionAnswerFlowDeps.buildRequest` with the same
     fifth optional parameter S1 gave the real builder, and pass the map through
     at the one call site. The map is DATA and `deps` are SEAMS, so the data
     goes before the seams — the shape `buildDecisionResolveCommand` already
     uses. Add to the header, under the deliberate absences, that this module
     neither reads nor validates the map: it forwards it, and every refusal it
     can earn belongs to `decisionAnswer.ts`. Constraint 6 binds what that
     header may say.
 S4. `apps/ui/src/api/decisionAnswerFlow.test.ts`, at C4. Every existing call
     that passes `deps` as the FOURTH argument now passes `undefined` in the new
     fourth position and `deps` fifth; calls passing three arguments are
     unchanged. Then add cases for: the map reaching the builder as its fifth
     argument, unchanged and by identity; and omitting the map handing the
     builder `undefined` there. Extend the existing case titled "hands the
     builder the target, the card, the answer and the minted nonce, unchanged"
     so its title and its assertion both cover the fifth argument — it reads a
     four-element array today and would otherwise describe a call that no longer
     exists.

Done when — run every gate yourself and record its REAL exit code. G1 through G8
run at commits STRICTLY EARLIER than C5, so the handback can quote them; the
push is ordered after C5 and its reading is NOT written into the handback. Read
every non-current revision with `git show <rev>:<path>` into memory; never write
a past blob over a tracked file to read it.
 G1. BRANCH, CLEANLINESS, TRANSPORT. Branch is `feature/f031-decision-inbox`.
     `git status --porcelain` prints 0 lines after each of C0a, C0b, C1, C2, C3
     and C4. `.agent/STOP` read from disk before C0a and before C5, both ABSENT.
     Report the sha256, byte count and line count of this block as saved at C0a,
     as mirrored at C0b, and as read off disk at C4 — all three must be EQUAL —
     and say whether C0a and C0b are the same git blob. Report also whether any
     line of the block as saved is a run of a single repeated character, which
     must come back as none. THEN STATE IN ONE SENTENCE WHAT THIS PROOF COVERS:
     the saved copy, its mirror and the working copy, all three your own output,
     and NOT the bytes that were emitted to you. §3 item 37 is why.
 G2. EXTRACTION AND CAPS. Extract the slices from the COMMITTED C0a blob by
     their marker LINES, never from the prompt. Report how many slices your
     extractor printed, each slice's own line count, the CONTENT line total, the
     TOTAL line count, and PROSE as TOTAL minus CONTENT. MARKERS ARE PROSE.
     PROSE must be at most 400 and TOTAL at most 490.
 G3. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF031R61 under the
     newline-INCLUDED convention. Run the negative control against the slice
     MINUS its trailing newline and report it FALSE. Report `^## Goal$` 1,
     `^## Next Steps$` 1, and `wc -l` STRICTLY UNDER 50.
 G4. THE APPEND, PROVED TWICE, THE SECOND READER COVERING THE WHOLE APPENDED
     REGION. `.agent/live_review.md` at C2 equals its pre-commit blob plus ONE
     newline plus LEDGER61. The reviewer measured the base blob at `486b3ef8`
     itself: `.agent/live_review.md` is 956513 bytes over 389 blank-line units.
     If it reads differently before C2, something moved that this round did not
     order — stop and hand back. Report both byte counts and the sum. Then
     confirm with a SECOND, independent reader, as §3 item 36 requires: split
     the whole file on blank lines, let N be the number of paragraphs YOUR
     SCRIPT COUNTS in that slice — never a number this block asserts — and
     compare the LAST N units of the file against the slice's N paragraphs IN
     ORDER. Report N and the unit count before and after. THE NEGATIVE CONTROL
     GOES ON THE FIRST APPENDED PARAGRAPH: flip ONE byte IN MEMORY inside
     paragraph 1 and report that BOTH readers REJECT it. Never mutate the
     tracked file.
 G5. THE LEDGER SETS. Report at two points — before C2 and after C2 — the
     line-anchored counts of `^- R-\d+ — `, `^Done: R-\d+ — `, `^Landed: R-`,
     `^Gate: R\d+ — ` and `^Gate: F\d+ R\d+ — `, plus the finding ids, the
     RESOLVED ids and the gate keys ADDED and REMOVED as SETS, whether all ids
     are DISTINCT, and the maximum id. Every movement constraint 5 names is
     checked here, INCLUDING the ones that must NOT move. Report the open set at
     both points.
 G6. THE TYPE GATE, THE UNIT SUITE AND THE UNTOUCHED CONTRACT SUITE. In the
     PRIMARY checkout at C4, run each and report its REAL exit code: `npx tsc
     --noEmit` from `apps/ui`; `npx vitest run` from `apps/ui`; and
     `python3 -m pytest tests/ui_contracts/ -q` from the repository root. At
     `486b3ef8` the reviewer measured these itself at exit 0; exit 0 with 30
     files and 475 tests; and exit 0 with 561 passed and 4 skipped. THE CONTRACT
     SUITE MUST READ EXACTLY 561 AND 4 AGAIN — it reads the card, this round
     does not touch the card, and any movement there means the change reached a
     file the Change line forbids. THE VITEST TOTAL MUST RISE, by exactly the
     number of cases YOU added; report that number as YOUR OWN count and report
     the file count beside it.
 G7. THE RED CONTROL, IN A DISPOSABLE WORKTREE. Add a worktree at C4 under
     `.remedy-wt/`. Run there, with the config named because a fresh worktree
     carries no `node_modules` of its own and the run must find the primary's:
     `npx vitest run src/api/ --root <worktree>/apps/ui --config
     <primary>/apps/ui/vitest.config.ts`. Report the UNMUTATED control FIRST and
     require a REAL exit 0 with its test count. Then, in the WORKTREE only,
     delete the `clarificationAnswers` argument from the
     `buildDecisionResolveCommand` call inside `buildDecisionSendRequest` in
     `apps/ui/src/api/decisionSend.ts` — the reviewer measured that call as
     occurring exactly 1x in that file at `486b3ef8` — and re-run the SAME
     command. Report the exit code, the failure count and the NAMES of the
     failing tests, which must include the cases S2 added. A colour with no
     baseline is not evidence, which is why the control is ordered first. Then
     `git worktree remove` it and `git worktree prune`, and report `git worktree
     list` as 1 line and `git ls-files .remedy-wt` as 0 lines.
 G8. NOTHING ELSE MOVED, MARKERS, PATHS, COMMITS, AND THE STATE READERS. Compare
     the path set of `git diff --name-only 486b3ef8..C4` BOTH WAYS against this
     round's expected set — the Change line's list MINUS `.agent/handoff.md`,
     excluded because the handback is written at C5 — and report both residues
     EMPTY. Report `git diff --stat 486b3ef8..C4` restricted to `packages/`,
     `tests/`, `docs/` and `apps/ui/src/components/` and confirm each is EMPTY.
     Line-anchored `^<<<SLICE ` and `^<<<END ` are 0 and 0 in `.agent/plan.md`
     at C1 and `.agent/live_review.md` at C2, against a CONTROL count over the
     C0a blob, which is not 0. Report each commit's insertions from `git diff
     --numstat` for C0a through C4, confirm each is single-parent and under 500.
     Then, in the PRIMARY checkout at C4, run SERIALLY — never two pytest
     processes alive at once — reporting each REAL exit code and count:
     `tests/cli/test_golden_path.py` (the canary), `tests/ui_server/`,
     `tests/orchestration/test_test_runner.py`,
     `tests/regression/test_resource_safety.py` and
     `tests/orchestration/test_integrity_gate.py`. At `486b3ef8` the reviewer
     measured these itself at 42, 489, 52, 21 and 16, every one at exit 0. Any
     movement is unexplained: stop and hand back.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C5: feature and round, branch, the per-commit changed-files table
             with the `+/-` column taken from `git diff --numstat` ITSELF and
             agreeing cell for cell with G8's readings, the item-status table
             covering C0a, C0b, C1, C2, C3, C4, C5 and the push, ONE LINE PER
             GATE for G1 through G8 with its real exit code, the open-findings
             count AFTER this round, and the next expected action. SAY PLAINLY
             THAT NO COMPONENT, NO STYLESHEET AND NO FILE UNDER `tests/`,
             `packages/` OR `docs/` CHANGED, THAT NO FINDING WAS RESOLVED, AND
             THAT THE OPEN COUNT IS UNCHANGED AT THE NUMBER G5 MEASURED. THE
             NEXT ACTION NAMES, IN THIS ORDER: re-read `.agent/STOP` from disk
             first, then the Open PR Gate, then review THIS round's handback and
             record its verdict, then the MARKUP half — the card rendering a
             field per open clarification and passing the map to the widened
             flow, with `tests/ui_contracts/test_decision_answer_wiring.py`
             moving with the call string it pins. Name no round number for
             those: §3 item 35 forbids numbering a round that has not begun.
             Obey constraint 10's cap. Then push with `git push origin
             feature/f031-decision-inbox`.

<<<SLICE PLANF031R61
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
R61 writes the R60 verdict and lands the SEAM half of the clarification form.
`buildDecisionResolveCommand` has taken the answers map since R51; neither
`buildDecisionSendRequest` nor `answerDecisionCard` forwards it, so the map R53
built cannot reach the door from any caller. This round widens both hops and
tests them under the shipped vitest config. IT TOUCHES NO COMPONENT: the card,
its stylesheet and `tests/ui_contracts/test_decision_answer_wiring.py` are all
untouched, which is why the pinned call string stays green.

## Next Steps
1. The MARKUP half: the card renders a field per open clarification, collects
   them into the map, and passes it to the widened flow.
   `tests/ui_contracts/test_decision_answer_wiring.py` pins the card's call
   string at `answerDecisionCard(target, decision, answer.value)`, so that
   round moves the guard with the call it pins.
2. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- THE FORM WAS ONE STEP AND IS NOW TWO. Seven files in one round crossed the
  block cap and put a seam change beside a markup change; the seam is reachable
  by vitest and the markup is not, so they gate differently and are split.
- SIX OF THE EIGHT PRODUCING TYPES STILL CANNOT BE ANSWERED THROUGH THE DOOR.
  R-0693 measures the gap; the rest are outside F031's scope, and the inbox
  tells the truth about every one of them rather than offering a refused button.
- THIS FILE NAMES NO ROUND NUMBER IT HAS NOT BEGUN. Twice a pre-assigned label
  went stale the moment a round was inserted ahead of it; a step is named by
  what it does, and its number is knowable only when it starts.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 252 at `486b3ef8`
  and this round moves it by nothing.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R61

<<<SLICE LEDGER61
Gate: F031 R60 — the F031 R60 entry. R60 PASSED ON EVERY GATE ITS BLOCK ORDERED, G1 THROUGH G7, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk. THIS WAS THE RECORD ROUND: no file outside `.agent/` changed, R-0631, R-0694 and R-0705 closed against the §3 items landed at `513bb9e0`, R-0706 and R-0707 opened, and the open set fell 253 to 252. THE TRANSPORT PROOF COVERS THE SAVED COPY, ITS MIRROR AND THE WORKING COPY AND NOT THE EMITTED BYTES, per §3 item 37: the C0a and C0b blobs are byte-identical at sha256 `a0bfa359…f298e36` over 24744 bytes and 206 lines and resolve to the SAME git blob `d48e5b030b70`, the working copy matches both, and no line of the block is a run of one repeated character. THE EXTRACTION printed 2 slices at 45 and 11 content lines with CONTENT 56 and TOTAL 206, so PROSE 150 against 400 and TOTAL 206 against 490. THE PLAN at `3b213213` is byte-equal to PLANF031R60 with the minus-newline control FALSE, `^## Goal$` 1, `^## Next Steps$` 1 and `wc -l` 45. THE APPEND IS EXACT AND ITS SECOND READER REALLY REACHED PAST THE TAIL: 944832 + 1 + 11680 = 956513 and the committed blob is 956513; N counted by the reviewer's own script is 6, units 383 to 389, the last six units match the slice's six paragraphs IN ORDER, and a byte flipped IN MEMORY inside the FIRST appended paragraph is REJECTED by BOTH readers — the first multi-paragraph append this branch has gated under §3 item 36 since that item landed. THE SETS MOVED EXACTLY WHERE CONSTRAINT 5 ALLOWED: `^- R-\d+ — ` 266 to 268 with the ADDED ids exactly `R-0706` and `R-0707`, `^Done: R-\d+ — ` 13 to 16 with the ADDED ids exactly `R-0631`, `R-0694` and `R-0705`, `^Gate: F\d+ R\d+ — ` 40 to 41 with the ADDED key exactly `F031 R59`, `^Landed: R-` 0 and `^Gate: R\d+ — ` 19 unmoved, nothing REMOVED from any set, all ids DISTINCT with `R-0707` the maximum, every resolved id also present as a `^- R-\d+ — ` paragraph, neither new id present as a `^Done:` line, and the open set 253 before C2 and 252 after it. NOTHING ELSE MOVED: both path residues EMPTY, `apps/`, `packages/`, `tests/` and `docs/` WHOLE each EMPTY in the range, markers 0 and 0 in the plan and the ledger against a CONTROL of 2 and 2, insertions 206, 116, 13, 12 and 29 with each commit single-parent and under 500, and `git ls-files .remedy-wt` 0 lines, `git worktree list` 1 line and `git ls-files --others --exclude-standard` 0 lines. THE READERS THE REVIEWER RE-RAN SERIALLY, every one at a REAL exit 0 and every one EQUAL to the base reading: the canary 42, `tests/ui_server/` 489, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21 and `tests/orchestration/test_integrity_gate.py` 16. THE HANDBACK COMMIT'S OWN NUMBERS, WHICH §3 ITEM 31 ROUTES HERE: `486b3ef8` adds 29 lines and removes 37 in `.agent/handoff.md`. AND ONE PIECE OF EVIDENCE JOINS AN OPEN FINDING RATHER THAN MINTING AN ID, per §3 item 30: that handback is 81 lines against the 60 a five-commit bundle earns, declared under AGENTS.md DECISION D15 with the cause given as mandated content — and the R58 handback at `97b79145` carried the SAME mandated sections for the SAME five commits and the same seven gate lines in exactly 60. Re-measured by the reviewer: R58 holds 9 blank lines and 51 non-blank against R60's 24 and 57, so 15 of the 21 excess lines are optional separators rather than content, and the stated cause is therefore not the whole cause. `R-0470` and `R-0700` are neighbours and neither is this; `R-0582` IS — it records that the declared overage has become every round and names leaving the cap in place and declaring against it forever as the drift nobody proposed — so that entry gains this instance and no second id is created. ITS CHEAPER REPAIR IS NOW CLOSED OFF, AND THE RECORD SHOULD SAY SO: R-0582 offered routing the transcript to the ROUND REPORT, and §3 item 31 has since ruled that under self-drive no such channel exists, so only two routes remain live — an AGENTS.md cap the mandated content can meet, or a block that orders less into the handback. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.
<<<END LEDGER61

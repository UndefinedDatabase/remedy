── STEP T003 component wiring / F031 — ROUND R38 ──────────────────────
Goal:        Make the decision inbox ANSWERABLE: the server token reaches the
             card, an answer click calls `answerDecisionCard`, the sentence it
             answers is rendered by its tone, the buttons ship enabled, and the
             three sentences saying nothing posts yet are retired. This is the
             LAST step of T003. The round also records R37's PASS.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the plan
             · C2 the R37 gate entry · C3 the wiring (one commit, see
             constraint 5) · C4 the contract test · C5 handback · then the push.
Change:      Exactly these paths, nothing else. `.agent/authored/f031-r38.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `apps/ui/src/RemedyApp.tsx`,
             `apps/ui/src/components/shell/RemedyShell.tsx`,
             `apps/ui/src/components/panels/RightLivePanel.tsx`,
             `apps/ui/src/components/panels/DecisionInboxCard.tsx`,
             `apps/ui/src/components/panels/RightLivePanel.module.css`,
             `apps/ui/src/api/decisionCard.ts`,
             `apps/ui/src/api/decisionAnswer.ts`,
             `tests/ui_contracts/test_decision_answer_wiring.py`,
             `.agent/handoff.md`. No file under `docs/`, `packages/` or
             `apps/cli/` is touched, and no other file under `tests/`.

Constraints:
 1. EVERY SLICE IS APPLIED BYTE FOR BYTE. Never retype one, never reflow one,
    never fix one. If a slice looks wrong, STOP and say so in the handback
    instead of correcting it — a corrected slice destroys the transport proof.
 2. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4, C5. One path per
    commit except C3, which carries the wiring's files together.
 3. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES R37. That is
    ordered, not an oversight: the plan becomes current at C1, which is the
    FIRST substantive commit of the round (§3 item 23).
 4. THE PRODUCTION CHANGE IS DESCRIBED, NOT SLICED. S1 through S9 below fix
    behaviour, seam and public surface; you write the code under AGENTS.md's
    self-review loop and you may name things better than the spec does.
 5. THE WIRING IS ONE COMMIT BECAUSE THE COMPILER SAYS SO. `apps/ui/tsconfig.json`
    sets `noUnusedLocals` and `noUnusedParameters` true and `strict` true, so a
    component that declares a prop no child accepts, or accepts one it does not
    pass on, fails `tsc --noEmit`. Landing the chain in pieces would put a red
    compiler between two green commits. Measured at `a1bf1f5d`, not assumed.
 6. NO NEW BRANCH ENTERS THE MARKUP. DECISION F031 D5 keeps every real rule in
    a module the shipped vitest config reaches, and it reaches
    `src/**/*.test.ts` only. A `Record` lookup and a null check are projections
    and are allowed; a `switch`, an `if` chain over a tone, or any comparison
    against a decision's `type` or `status` is not.
 7. NO INVENTED DESIGN TOKEN. The three tone colours are
    `--remedy-green-500`, `--remedy-orange-400` and `--remedy-red-500`, each
    already DEFINED in `apps/ui/src/styles/tokens.css` — verified there at
    `a1bf1f5d`. Do not add a token, and do not write a raw hex.
 8. THE STALENESS SWEEP IS STANDING. Every sentence this round writes or leaves
    behind in a file it edits must be true of that file at C4. A comment that
    says a thing is absent, arrives later, or is owed by a future round is
    exactly what S6 exists to retire — sweep the WHOLE header of each file you
    touch, not only the sentence the spec quotes.
 9. THE LEDGER SETS MOVE ONLY HERE. Across C2, `^- R-\d+ — ` stays 246 with the
    ids ADDED and the ids REMOVED both EMPTY, `^Done: R-\d+ — ` stays 5,
    `^Landed: R-` stays 0, `^Gate: R\d+ — ` stays 19, and
    `^Gate: F\d+ R\d+ — ` moves 18 to 19 with the ADDED key exactly `F031 R37`.
    This round mints no finding id and resolves none.
10. RE-READ `.agent/STOP` FROM DISK before C0a and again before C5. If it
    exists at either reading, finish the commit in hand, write the handback and
    STOP. Never create it, never delete it.
11. SCRATCH LIVES UNDER `.remedy-wt/` and is removed BY ITS EXACT PATH, never
    by a glob. Nothing under `.remedy-wt/` is ever committed.
12. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `cp`, and every form of environment assignment (`VAR=x cmd`,
    `env VAR=x cmd`, `export VAR=x; cmd`). Route anything that counts, hashes
    or compares through `python3 - <<'PY'`, read real exit codes from
    `subprocess.run(...).returncode`, and copy with `shutil.copyfile`.

Spec — the wiring:
 S1. THREAD THE TOKEN, WHOLE CHAIN. `RemedyApp` already holds `token` from
     `readUrlState`. Pass it down as a REQUIRED prop named `serverToken`
     through `RemedyShell` and `RightLivePanel` to `DecisionInboxCard`. Every
     hop declares it in its own props type, and the name is `serverToken` at
     every hop — one spelling per concept, AGENTS.md's discoverability rule.
 S2. THE JOB ID COMES FROM THE DASHBOARD, NOT THE URL. `DecisionInboxCard`
     builds its `DecisionSendTarget` as `{ jobId, serverToken }` with `jobId`
     taken from `dashboard.jobId` — the value `RemedyShell` already trusts for
     the stream (DECISION F008 D3) — threaded to the card the same way. Named
     fields make the transposition finding R-0684 forbade inexpressible; keep
     them named, and never spread a bare pair of strings into that type.
 S3. ONE CLICK, ONE FLOW. An answer button's `onClick` calls
     `answerDecisionCard(target, decision, answer.value)` from
     `../../api/decisionAnswerFlow` and awaits the `DecisionOutcomeMessage` it
     answers. Nothing else in this component reaches the network, mints a
     nonce, builds a request or names a status.
 S4. STATE IS KEYED BY THE ROW KEY THE CARD ALREADY COMPUTES. The outcome
     message and the in-flight marker are stored per ANSWER under a key built
     from the same `${decisionIndex}-${decision.id}` pair the `article` key
     uses, extended by the answer's own index. Two cards carrying one id must
     not share a sentence. Keep the key expression in ONE place.
 S5. WHAT THE OPERATOR SEES. While a send is in flight that answer's button is
     `disabled` and no other button is. When the flow answers, render
     `message.sentence` in that row, its class chosen from a
     `Record<DecisionOutcomeTone, string>` constant — `ok`, `warn` and `error`
     mapping to three classes you add to `RightLivePanel.module.css` under
     constraint 7. The sentence region carries `aria-live="polite"`, because it
     appears under a control the operator just pressed. No sentence text is
     invented here: every word an operator reads comes from `decisionOutcome.ts`.
 S6. RETIRE THE THREE SENTENCES, each true only while no component calls the
     flow. In `apps/ui/src/api/decisionCard.ts` the clause beginning "What is
     still genuinely absent is the SEND"; in `apps/ui/src/api/decisionAnswer.ts`
     the clause saying the sender round owns the request call; in
     `DecisionInboxCard.tsx` the clause beginning "What is still absent is the
     SEND", together with the `ANSWER_PENDING_TITLE` constant and its
     `title`/`disabled` use. Replace each with what is now TRUE, naming where
     the send lives. All three were read at `a1bf1f5d`.
 S7. THE NEW WHY COMMENTS carry one fact each, directly above the definition:
     on the tone map, that colour and placement are the component's and the
     sentence never is; on the key expression, that two cards may carry one id;
     on the `serverToken` prop, that it is a credential and never reaches a URL
     path. Say plainly in `DecisionInboxCard.tsx` that no DOM test reaches this
     markup, and name the contract test that guards it instead.

Spec — the guard:
 S8. ADD `tests/ui_contracts/test_decision_answer_wiring.py`, modelled on
     `tests/ui_contracts/test_remedy_shell_stream.py`, the precedent for this
     whole shape. Copy its `strip_ts_comments` helper and run EVERY assertion
     over COMMENT-STRIPPED source — these files carry long prose headers naming
     the very symbols being asserted, so an unstripped guard would be satisfied
     by the comment describing the code rather than by the code (finding
     R-0584). Include its self-test shape too: assert that some comment really
     present in the raw source is GONE after stripping, so a stripper that
     silently did nothing cannot make every other assertion vacuous.
 S9. WHAT IT MUST PIN, over stripped source: that `RemedyApp` passes
     `serverToken` to `RemedyShell`; that `RemedyShell` passes it to
     `RightLivePanel`; that `RightLivePanel` passes it to `DecisionInboxCard`;
     that `DecisionInboxCard` imports `answerDecisionCard` from
     `../../api/decisionAnswerFlow` AND calls it; that the three tone keys and
     their classes are present; and that `ANSWER_PENDING_TITLE` occurs ZERO
     times in that component's stripped source. Pin the ABSENCE the component's
     own header promises as well: no comparison against `decision.type` or
     `decision.status` anywhere in its stripped source.

Done when — run every gate yourself and record its REAL exit code. G1 through
G9 run at commits STRICTLY EARLIER than C5, so the handback can quote them
(§3 item 31); the push is ordered after C5 and its reading is NOT written into
the handback — the reviewer takes that reading at the next gate.
 G1. BRANCH, CLEANLINESS, TRANSPORT. Branch is `feature/f031-decision-inbox`.
     `git status --porcelain` prints 0 lines after each of C0a, C0b, C1, C2, C3
     and C4. `.agent/STOP` read from disk before C0a and before C5, both
     ABSENT. Report the sha256, byte count and line count of this block as
     saved at C0a, as mirrored at C0b, and as read off disk at C4 — all three
     readings must be EQUAL — and say whether C0a and C0b are the same git blob.
 G2. EXTRACTION AND CAPS. Extract the slices from the COMMITTED C0a blob by
     their marker LINES, never from the prompt. Report how many slices your
     extractor printed, the CONTENT line total, the TOTAL line count of the
     block, and PROSE as TOTAL minus CONTENT. PROSE must be at most 400
     (DECISION F085 D5) and TOTAL at most 490 (DECISION F085 D6).
 G3. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF031R38 under the
     newline-INCLUDED convention. Run the negative control: compare against the
     slice MINUS its trailing newline and report that FALSE. Report `^## Goal$`
     1, `^## Next Steps$` 1, and `wc -l` strictly under 50.
 G4. THE APPEND. `.agent/live_review.md` at C2 equals its pre-commit blob plus
     ONE newline plus LEDGER38, as one whole-file byte equality — report both
     byte counts and the sum. Confirm with a SECOND, independent reader: split
     the file on blank lines, report how the unit count moves, and check that
     the last units equal LEDGER38's paragraphs IN ORDER; then run the SWAPPED
     comparison and report it FALSE. Run a negative control by flipping ONE
     byte IN MEMORY and report that both readers REJECT it. Never mutate the
     tracked file.
 G5. THE LEDGER SETS. Report every count constraint 9 names, before and after
     C2, plus the ids ADDED and the ids REMOVED as sets, whether all ids are
     DISTINCT, and the maximum id. Report the open set at C2 as
     `^- R-\d+ — ` minus `^Done: R-\d+ — `.
 G6. MARKERS, PATHS, COMMITS. Line-anchored `^<<<SLICE ` and `^<<<END ` are 0
     and 0 in `.agent/plan.md` at C1 and in `.agent/live_review.md` at C2,
     against a CONTROL count over the C0a blob, which is not 0. Report
     `git diff --name-only a1bf1f5d..C4` and compare it BOTH WAYS against the
     change set above. Report each commit's insertions from
     `git diff --numstat`, confirm each is single-parent and each under 500,
     and confirm the numbers agree with `git commit`'s own summary. Report
     `git ls-files .remedy-wt` as 0 and `git worktree list` as 1 line at C4.
     Report the reflog for this round's commits: every operation prefix must
     read `commit`, and `amend`, `rebase` and `cherry` must be 0 each.
 G7. THE COMPILER. `npx tsc --noEmit` in `apps/ui`, run at C3 and again at C4,
     REAL exit 0 both times. This gate is why constraint 5 exists. It reads
     exit 0 at the base `a1bf1f5d`, measured before this block was written, so
     a red here belongs to this round.
 G8. THE UNIT SUITE. `npx vitest run` in `apps/ui` at C4, REAL exit 0. Report
     the test-file count and the test count. At `a1bf1f5d` they are 30 and 448;
     this round adds no `.test.ts`, so both must be IDENTICAL. If either moved,
     report the numbers and which files changed rather than explaining it away.
 G9. THE GUARD, ITS RED PROOF, AND THE READERS. Run
     `python3 -m pytest tests/ui_contracts/test_decision_answer_wiring.py -q`
     at C4: REAL exit 0, and report how many tests it collected. Then PROVE IT
     CAN FAIL, in a DISPOSABLE WORKTREE and never in the primary checkout: add
     one at C4 under `.remedy-wt/r38red`; there count the exact bytes
     `serverToken={serverToken}` in
     `apps/ui/src/components/shell/RemedyShell.tsx` and report the count, which
     must be 1; then delete that ONE occurrence IN THE WORKTREE and re-run the
     same test file against the worktree's copy. Report WHICH node ids failed
     and HOW MANY. A GREEN result there is the honest thing to declare, not
     something to paper over: it would mean the guard does not reach the chain
     and the round needs a repair, so say so plainly. Remove the worktree by
     its exact path and report `git worktree list` back to 1 line. Then, in the
     PRIMARY checkout at C4 and SERIALLY — never two pytest processes alive at
     once, which produces false reds — run and report the real exit code and
     count of each: `tests/ui_server/`,
     `tests/orchestration/test_test_runner.py`,
     `tests/regression/test_resource_safety.py`,
     `tests/orchestration/test_integrity_gate.py`, `tests/ui_contracts/`, and
     the canary `tests/cli/test_golden_path.py`. At `a1bf1f5d` these read 480,
     52, 21, 16, 525 passed with 4 skipped, and 42; `tests/ui_contracts/` MUST
     grow by exactly the number G9's first command collected, and any other
     movement is reported as a number, never explained away.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C5: feature and round, branch, the per-commit changed-files table
             with the `+/-` column taken from `git diff --numstat` itself and
             agreeing cell for cell with G6, the item-status table covering
             C0a, C0b, C1, C2, C3, C4, C5 and the push, ONE LINE PER GATE for
             G1 through G9 with its real exit code, the open-findings count,
             and the next expected action. Derive your line cap from AGENTS.md
             yourself, from the commit count you actually made; if the mandated
             content genuinely does not fit, declare the DECISION D15 overage
             with its stated cause. Then push with
             `git push origin feature/f031-decision-inbox`.
──────────────────────────────────────────────────────────────────────

<<<SLICE PLANF031R38
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1–D18.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R38 is the COMPONENT round and the LAST step of T003: the server token reaches
the card, an answer click calls `answerDecisionCard`, the sentence it answers is
rendered by its tone, the buttons ship enabled, and the three sentences saying
nothing posts yet are retired. The round also records R37's PASS.

## Next Steps
1. The clarification FORM, and the ruling on `NeedsAttentionCard`'s decision
   branch (DECISION F031 D4).
2. The integration-gate round per `docs/agents/integration_gate.md`, whose block
   also carries the checklist items R-0683, R-0377, R-0419, R-0429, R-0560,
   R-0582, R-0583 and R-0633 route there, then closure per
   `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- THE DEFAULT DEADLINE CREATES A TIMER IT CANNOT CANCEL, as
  `decisionAnswerFlow.ts`'s own header records: the seam DECISION F031 D18 chose
  carries no handle, so when the submit wins the 20-second timer still fires.
  This round is the one that wires it to a real click.
- THE SERVER STILL ACCEPTS A BLANK ANSWER AND WRITES IT ONCE. R29 stopped it in
  the browser only; DECISION F031 D14 routes that check to F009, not fixed here.
- NO DOM HARNESS REACHES THIS ROUND'S MARKUP. The shipped vitest config collects
  `src/**/*.test.ts`, so the wiring is gated by comment-stripped SOURCE reading
  in `tests/ui_contracts/` and by `tsc --noEmit`, never by a rendered click.
- Open findings, by the rule and commit DECISION F009 D10 requires — every
  `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the set is 241 at
  `a1bf1f5d` and this round leaves it there.
- The findings THIS FEATURE MUST STILL ACT ON are R-0377, R-0403, R-0413,
  R-0419, R-0429, R-0431, R-0441, R-0445, R-0471, R-0495, R-0533, R-0560,
  R-0574, R-0582, R-0583, R-0593, R-0601, R-0622, R-0625, R-0632, R-0633,
  R-0672, R-0674, R-0675, R-0676, R-0677, R-0678, R-0679, R-0683, R-0684 and
  R-0685; R-0495 and R-0574 are the two Highs.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R38

<<<SLICE LEDGER38
Gate: F031 R37 — the F031 R37 entry. R37 PASSED ON EVERY ONE OF ITS EIGHT GATES, AND THE REVIEWER RE-RAN EVERY ONE ITSELF at a later session off disk rather than reading the handback back; every value that handback states reproduced exactly. THE VERDICT ARRIVES ONE ROUND LATE BY CONSTRUCTION (§4 item 13 and the record-round rule), not by omission. TRANSPORT HELD IN ITS STRONGEST FORM for the ninth round running: the C0a blob at `e05eb4be`, the C0b blob at `1b163954`, `.agent/authored/f031-r37.md` at `a1bf1f5d` and both working copies read off disk are ALL FIVE byte-identical at sha256 `dd86faeeababbedbe55716c95fe5137c51c5365551d65e23a5dbc2d66e6a09e3` over 32499 bytes and 320 lines, C0a and C0b resolving to the SAME git blob `50671be5`. THE EXTRACTION printed 2 slices, 52 content lines and 320 total, so PROSE was 268 against the 400 DECISION F085 D5 sets and TOTAL 320 against the 490 DECISION F085 D6 sets. THE PLAN at `f2aac4d8` equals PLANF031R37 exactly at 2831 bytes and 49 lines, with the trailing-newline-removed control FALSE, `^## Goal$` 1, `^## Next Steps$` 1, and 49 strictly under the 50 AGENTS.md sets. THE APPEND at `0d399389` satisfied whole-file equality in the shape that block's constraint 7 states, at 783847 + 1 + 11315 = 795163 against an actual 795163, with the pre-commit blob a byte-exact PREFIX. THE SETS MOVED EXACTLY WHERE THAT BLOCK'S CONSTRAINT 9 ALLOWED AND NOWHERE ELSE: `^- R-\d+ — ` 246 to 246 with the ids ADDED and the ids REMOVED BOTH the EMPTY SET and all 246 DISTINCT, maximum `R-0685` unmoved; `^Done: R-\d+ — ` 5 to 5; `^Landed: R-` 0 to 0; `^Recurrence: R-` 25 to 26 and `^Recurrence: R-0582` 0 to 1; `^Gate: R\d+ — ` 19 to 19; `^Gate: F\d+ R\d+ — ` 17 to 18 with the ADDED key exactly `F031 R36`, all keys DISTINCT. The open set is 241 at `0d399389`. MARKERS STAYED OUT OF THE TARGETS: line-anchored `^<<<SLICE ` and `^<<<END ` are 0 and 0 in the plan at `f2aac4d8` and in the ledger at `0d399389`, against a live CONTROL of 2 and 2 over the C0a blob. THE FIVE COMMITS ARE EACH SINGLE-PARENT at insertions 320, 193, 19, 4 and 39 read from `git diff --numstat`, each under the 500 AGENTS.md DECISION F104 D1 counts, each touching exactly one path, and the range names exactly the five paths of that block's change set. The reflog scoped to those five reads `commit` in every operation prefix, so `amend`, `rebase` and `cherry` are 0 each; `git ls-files .remedy-wt` is 0 and `git worktree list` is 1 line. THE SIX SUITES WERE RE-RUN SERIALLY IN THE PRIMARY CHECKOUT at `a1bf1f5d` and every count is IDENTICAL to that handback's: `tests/ui_server/` 480, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16, `tests/ui_contracts/` 525 passed with 4 skipped, and the canary `test_golden_path` 42, every one a REAL exit 0. THE TWO READINGS THAT HANDBACK COULD NOT CARRY ARE RECORDED HERE, which is where §3 item 31 rules they belong: its own commit `a1bf1f5d` inserts 39 lines against 176 deleted, and the push landed, `git rev-parse` reading the local tip and `origin/feature/f031-decision-inbox` as the same `a1bf1f5d`. THE HANDBACK MET ITS CAP AT EXACTLY 60 LINES with no DECISION D15 overage declared, which is R-0582's own cheaper repair working as intended — the per-gate detail moved out of the handback and the round still proved every claim. ONE CAUTION IS REGISTERED WITHOUT A NEW ID, because R-0582 is OPEN and already carries this fix: the channel that detail moved INTO is a round report, and §3 item 31 rules that under self-drive such a report ends with the session. Nothing was lost this time only because the next session re-measured everything from disk. The durable half of that repair is THIS entry, not the report.
<<<END LEDGER38

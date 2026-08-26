── STEP T003 answer-control repair / F031 — ROUND R39 ─────────────────
Goal:        Register the three findings the R38 gate raised and fix all three:
             the outcome sentence must really be announced, a button must stay
             disabled until ITS OWN send settles, and a module header must stop
             routing the card it now has to a round number.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the plan
             · C2 the three findings, in their own commit · C3 the R38 gate
             entry · C4 the fixes and their guards · C5 handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f031-r39.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `apps/ui/src/components/panels/DecisionInboxCard.tsx`,
             `apps/ui/src/components/panels/RightLivePanel.module.css`,
             `apps/ui/src/api/decisionAnswerFlow.ts`,
             `tests/ui_contracts/test_decision_answer_wiring.py`,
             `.agent/handoff.md`. No file under `docs/`, `packages/` or
             `apps/cli/`, and no other file under `tests/` or under
             `apps/ui/src/api/`.

Constraints:
 1. EVERY SLICE IS APPLIED BYTE FOR BYTE. Never retype one, never reflow one,
    never fix one. If a slice looks wrong, STOP and say so in the handback
    instead of correcting it — a corrected slice destroys the transport proof.
 2. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4, C5. The findings land
    at C2 BEFORE any fix, so a session that dies mid-round still leaves the
    record complete (§4 item 4). C3 and C4 may not be reordered around it.
 3. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES R38. That is
    ordered: the plan becomes current at C1, the FIRST substantive commit.
 4. THE PRODUCTION CHANGE IS DESCRIBED, NOT SLICED. S1 through S5 fix the
    properties; you write the code under AGENTS.md's self-review loop.
 5. THE THREE FINDINGS ARE THE REVIEWER'S TEXT. You never write a `Done:`
    paragraph and never edit a finding's wording. When a fix lands, the record
    of it is this round's handback and the NEXT gate's entry, not a resolution
    you author (§4 item 4).
 6. NO NEW BRANCH ENTERS THE MARKUP, unchanged from R38: DECISION F031 D5
    keeps every real rule in a module the shipped vitest config reaches. A
    `Record` lookup, a set-membership test and a null check are projections; a
    `switch` or a comparison against a decision's `type` or `status` is not.
 7. NO INVENTED DESIGN TOKEN, unchanged from R38. Any colour resolves to a
    custom property `apps/ui/src/styles/tokens.css` already defines.
 8. THE LEDGER SETS MOVE TWICE, AND ONLY AS STATED. Across C2 `^- R-\d+ — `
    moves 246 to 249, the ids ADDED are exactly `R-0686`, `R-0687` and
    `R-0688`, the ids REMOVED are EMPTY, and all ids stay DISTINCT. Across C3
    `^Gate: F\d+ R\d+ — ` moves 19 to 20 with the ADDED key exactly `F031 R38`.
    Across BOTH, `^Done: R-\d+ — ` stays 5, `^Landed: R-` stays 0 and
    `^Gate: R\d+ — ` stays 19. The open set is 241 before C2 and 244 after.
 9. RE-READ `.agent/STOP` FROM DISK before C0a and again before C5. If it
    exists at either reading, finish the commit in hand, write the handback and
    STOP. Never create it, never delete it.
10. SCRATCH LIVES UNDER `.remedy-wt/` and is removed BY ITS EXACT PATH, never
    by a glob. Nothing under `.remedy-wt/` is ever committed.
11. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `cp`, and every form of environment assignment. Route anything
    that counts, hashes or compares through `python3 - <<'PY'`, read real exit
    codes from `subprocess.run(...).returncode`, and copy with
    `shutil.copyfile`.

Spec — the fixes:
 S1. THE LIVE REGION EXISTS BEFORE IT HAS ANYTHING TO SAY (R-0686). The element
     carrying `aria-live="polite"` is rendered from the FIRST render of a
     decision row, not created together with its first sentence. Assistive
     technology registers a live region when it ENTERS the accessibility tree
     and announces later MUTATIONS of it, so a region inserted already
     populated announces nothing.
 S2. AND ITS EMPTY STATE STAYS IN THE ACCESSIBILITY TREE. Do NOT reach for
     `display: none`, `visibility: hidden` or the `hidden` attribute to hide
     the empty region: each removes the node from that tree and reinstates
     R-0686 in a form that looks fixed. Collapse it by other means — no
     content, no margin, no forced flex line — and say in a WHY comment which
     three mechanisms are excluded and why, so the next reader does not
     "tidy it up" with one of them.
 S3. A BUTTON STAYS DISABLED UNTIL ITS OWN FLOW SETTLES (R-0687). Replace the
     single `sendingKey` with per-ANSWER-KEY in-flight tracking, so pressing a
     second answer never changes the first's disabled state, and each button's
     disabled state depends on ITS OWN key alone. Both properties must hold at
     once: exactly the pressed answer is disabled while it is in flight, AND no
     other press can clear it. Correct the comment above that state — the one
     now claiming a single key makes the guarantee — to say what the new shape
     really guarantees.
 S4. NAME THE COMPONENT, NOT THE ROUND (R-0688). In
     `apps/ui/src/api/decisionAnswerFlow.ts`, the header sentence "It answers a
     value; the card that shows it is R37's" is replaced by one naming
     `DecisionInboxCard.tsx`, which exists and shows it. Change nothing else in
     that file: no code, no seam, no other sentence.
 S5. THE GUARDS GROW WITH THE FIXES. Extend
     `tests/ui_contracts/test_decision_answer_wiring.py` — never replace it —
     so each of S1, S2 and S3 is pinned by at least one assertion over
     COMMENT-STRIPPED source, and so is S4 over that module's raw text, since
     the sentence being fixed IS a comment and stripping would delete the
     evidence. Keep every assertion the file already carries. You choose the
     exact strings; G7 requires you to PROVE each new assertion can fail.

Done when — run every gate yourself and record its REAL exit code. G1 through
G8 run at commits STRICTLY EARLIER than C5, so the handback can quote them
(§3 item 31); the push is ordered after C5 and its reading is NOT written into
the handback — the reviewer takes that reading at the next gate.
 G1. BRANCH, CLEANLINESS, TRANSPORT. Branch is `feature/f031-decision-inbox`.
     `git status --porcelain` prints 0 lines after each of C0a, C0b, C1, C2, C3
     and C4. `.agent/STOP` read from disk before C0a and before C5, both
     ABSENT. Report the sha256, byte count and line count of this block as
     saved at C0a, as mirrored at C0b, and as read off disk at C4 — all three
     must be EQUAL — and say whether C0a and C0b are the same git blob.
 G2. EXTRACTION AND CAPS. Extract the slices from the COMMITTED C0a blob by
     their marker LINES, never from the prompt. Report how many slices your
     extractor printed, the CONTENT line total, the TOTAL line count, and PROSE
     as TOTAL minus CONTENT. PROSE must be at most 400 (DECISION F085 D5) and
     TOTAL at most 490 (DECISION F085 D6).
 G3. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF031R39 under the
     newline-INCLUDED convention. Run the negative control against the slice
     MINUS its trailing newline and report it FALSE. Report `^## Goal$` 1,
     `^## Next Steps$` 1, and `wc -l` strictly under 50.
 G4. THE TWO APPENDS, EACH PROVED SEPARATELY. `.agent/live_review.md` at C2
     equals its pre-commit blob plus ONE newline plus FINDINGS39, and at C3
     equals ITS pre-commit blob plus ONE newline plus LEDGER39 — report both
     byte counts and the sum for EACH. For EACH, confirm with a SECOND,
     independent reader: split on blank lines, report how the unit count moves,
     check the last units equal that slice's paragraphs IN ORDER, and report
     the SWAPPED comparison FALSE. For EACH, flip ONE byte IN MEMORY and report
     that both readers REJECT it. Never mutate the tracked file.
 G5. THE LEDGER SETS. Report every count constraint 8 names at three points —
     before C2, after C2, after C3 — plus the ids ADDED and REMOVED as sets at
     each step, whether all ids are DISTINCT, and the maximum id. Report the
     open set as `^- R-\d+ — ` minus `^Done: R-\d+ — ` before C2 and after C3.
 G6. MARKERS, PATHS, COMMITS. Line-anchored `^<<<SLICE ` and `^<<<END ` are 0
     and 0 in `.agent/plan.md` at C1 and in `.agent/live_review.md` at C3,
     against a CONTROL count over the C0a blob, which is not 0. Report
     `git diff --name-only 279cd819..C4` and compare it BOTH WAYS against the
     change set above. Report each commit's insertions from
     `git diff --numstat`, confirm each is single-parent and under 500. Report
     `git ls-files .remedy-wt` as 0 and `git worktree list` as 1 line at C4.
     Report the reflog for this round's commits: every operation prefix must
     read `commit`, and `amend`, `rebase` and `cherry` must be 0 each.
 G7. THE FIXES ARE PROVED, NOT ASSERTED. At C4 run `npx tsc --noEmit` in
     `apps/ui` (REAL exit 0), `npx vitest run` in `apps/ui` (REAL exit 0,
     report the file and test counts — at `279cd819` they are 30 and 448 and
     this round adds no `.test.ts`), and
     `python3 -m pytest tests/ui_contracts/test_decision_answer_wiring.py -q`
     (REAL exit 0, report the collected count, which must EXCEED the 16 that
     file collects at `279cd819`). Then, in a DISPOSABLE WORKTREE at C4 under
     `.remedy-wt/r39red` and never in the primary checkout, prove EACH NEW
     assertion can fail: for each, revert in the worktree the ONE specific
     change that assertion pins, re-run that test file, and report WHICH node
     ids failed and HOW MANY. Before each revert, count the exact bytes you are
     about to remove IN THE FILE you remove them from and report the count,
     which must be 1; if it is not 1, choose a longer unique string and report
     that instead. A new assertion that stays GREEN under its own revert is a
     guard that pins nothing — declare it plainly rather than adjusting it.
     Remove the worktree by its exact path and report `git worktree list` back
     to 1 line.
 G8. THE READERS AND THE CANARY, in the PRIMARY checkout at C4 and SERIALLY —
     never two pytest processes alive at once, which produces false reds. Run
     and report the real exit code and count of each: `tests/ui_server/`,
     `tests/orchestration/test_test_runner.py`,
     `tests/regression/test_resource_safety.py`,
     `tests/orchestration/test_integrity_gate.py`, `tests/ui_contracts/`, and
     the canary `tests/cli/test_golden_path.py`. At `279cd819` these read 480,
     52, 21, 16, 541 passed with 4 skipped, and 42; `tests/ui_contracts/` MUST
     grow by exactly the increase in G7's collected count for that one file —
     TEST FUNCTIONS, not assertions — and any other movement is a reported number.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C5: feature and round, branch, the per-commit changed-files table
             with the `+/-` column taken from `git diff --numstat` itself and
             agreeing cell for cell with G6, the item-status table covering
             C0a, C0b, C1, C2, C3, C4, C5 and the push, ONE LINE PER GATE for
             G1 through G8 with its real exit code, an explicit line for each
             of R-0686, R-0687 and R-0688 saying what changed, the open-findings
             count, and the next expected action. Derive your line cap from
             AGENTS.md yourself, from the commit count you actually made; if the
             mandated content genuinely does not fit, declare the DECISION D15
             overage with its stated cause. Then push with
             `git push origin feature/f031-decision-inbox`.
──────────────────────────────────────────────────────────────────────

<<<SLICE PLANF031R39
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
R39 registers the three findings the R38 gate raised and fixes all three: the
outcome sentence is really announced, a button stays disabled until ITS OWN send
settles, and a module header names the component it has instead of a round
number. The round also records R38's PASS.

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
  R38 wired it to a real click, so it now fires behind a live button.
- THE SERVER STILL ACCEPTS A BLANK ANSWER AND WRITES IT ONCE. R29 stopped it in
  the browser only; DECISION F031 D14 routes that check to F009, not fixed here.
- NO DOM HARNESS REACHES THE INBOX MARKUP. The shipped vitest config collects
  `src/**/*.test.ts`, so the wiring is gated by comment-stripped SOURCE reading
  in `tests/ui_contracts/test_decision_answer_wiring.py` and by `tsc --noEmit`,
  never by a rendered click. Both R-0686 and R-0687 got past R38's gates for
  exactly that reason: a source guard cannot see an accessibility-tree property.
- Open findings, by the rule and commit DECISION F009 D10 requires — every
  `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the set is 241 at
  `279cd819` and this round takes it to 244.
- The findings THIS FEATURE MUST STILL ACT ON are R-0377, R-0403, R-0413,
  R-0419, R-0429, R-0431, R-0441, R-0445, R-0471, R-0495, R-0533, R-0560,
  R-0574, R-0582, R-0583, R-0593, R-0601, R-0622, R-0625, R-0632, R-0633,
  R-0672, R-0674, R-0675, R-0676, R-0677, R-0678, R-0679, R-0683, R-0684,
  R-0685, R-0686, R-0687 and R-0688; R-0495 and R-0574 are the two Highs.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R39

<<<SLICE FINDINGS39
- R-0686 — Medium, A LIVE REGION CREATED TOGETHER WITH ITS FIRST SENTENCE ANNOUNCES NOTHING. Raised by the reviewer at the R38 gate against `apps/ui/src/components/panels/DecisionInboxCard.tsx` as committed at `0a513667`. THE MEASUREMENT: the outcome paragraph is rendered as `outcome === null ? null : (<p className={...} aria-live="polite">{outcome.sentence}</p>)`, so the element carrying the live-region attribute does not exist in the accessibility tree until the very render that also gives it its text. Assistive technology registers a live region when the node ENTERS that tree and announces subsequent MUTATIONS of it; a region inserted already populated is not announced by the major screen readers. The consequence lands on the one sentence an operator most needs after pressing a button — whether the answer was recorded, refused, or never reached the run — and it is delivered silently. THE COMMENT DIRECTLY ABOVE IT ASSERTS THE OPPOSITE, which is what hid this from review: "It ANNOUNCES itself: this sentence appears under a control the operator just pressed, so a silent insertion would leave a screen reader on the button with nothing said" describes exactly the outcome the code produces. THE WORKER IS NOT AT FAULT: S5 of the R38 block ordered "When the flow answers, render `message.sentence` in that row ... The sentence region carries `aria-live="polite"`", which reads as a conditional render, the worker implemented it literally, and it RAISED the concern in its own handback rather than letting it pass — the §4 item 7 wrong-spec class, caught by the round that shipped it. WHY NO GATE SAW IT: every guard on this file reads comment-stripped SOURCE, and no source predicate can distinguish a node that is in the accessibility tree at first render from one that is not. THE FIX: render the element carrying `aria-live` from the FIRST render of a decision row, before it has anything to say, and collapse its empty state WITHOUT `display: none`, `visibility: hidden` or the `hidden` attribute — each of those removes the node from the accessibility tree and reinstates this defect in a form that looks fixed.

- R-0687 — Medium, ONE IN-FLIGHT KEY FOR THE WHOLE CARD RE-ENABLES A BUTTON WHILE ITS OWN ANSWER IS STILL ON THE WIRE. Raised by the reviewer at the R38 gate against `apps/ui/src/components/panels/DecisionInboxCard.tsx` as committed at `0a513667`. THE MEASUREMENT: `sendingKey` is a single `string | null` for the entire card, set to the pressed answer's key before the await and back to `null` after it, while `disabled={sendingKey === answerKey}` leaves every other answer in every row live by design. Press answer A, then press answer B while A is still in flight: the second press overwrites `sendingKey`, so A's button is ENABLED although A's request has not settled; when A then settles it writes `null`, so B's button is enabled while B is still on the wire. Both presses are reachable by construction, and no third state is needed to get there. THE CONSEQUENCE IS A DUPLICATE SEND, NOT A LOST ONE: `decisionAnswer.ts` records that the server writes an answer ONCE, so a second request for the same decision earns 409 and the operator reads "This decision is no longer open. It may already have been answered." about the decision they just answered — an honest sentence arriving as a confusing one. `decisionAnswerFlow.ts`'s uncancellable 20-second deadline widens that window rather than closing it. THE COMMENT ABOVE THE STATE IS HALF TRUE, which is why it read as sufficient: "a single key is what makes 'no other button is disabled' true by construction" does hold, while the property that actually protects a send — that a button stays disabled until ITS OWN flow settles — does not, and only the second one is a guarantee. THE WORKER IS NOT AT FAULT: S5 of the R38 block ordered the weaker of the two properties verbatim, and the code implements what was ordered. THE FIX: track the in-flight set per ANSWER KEY so a press never changes another answer's disabled state, and pin BOTH properties in `tests/ui_contracts/test_decision_answer_wiring.py`.

- R-0688 — Low, A MODULE HEADER STILL ROUTES THE CARD IT NOW HAS TO A ROUND NUMBER. Raised by the reviewer at the R38 gate against `apps/ui/src/api/decisionAnswerFlow.ts`, whose header reads "IT RENDERS NOTHING AND KNOWS NO COMPONENT. It answers a value; the card that shows it is R37's" — as committed at `a1bf1f5d` and unchanged at `279cd819`. The card that shows it is `DecisionInboxCard.tsx`, it was wired at `0a513667`, and the round it names was never the component round: R37 was the record round and R38 did the wiring, so the reference was already pointing at the wrong round when it was written. THE WORKER IS NOT AT FAULT AND DID THE RIGHT THING: the R38 block's change set does not name that file, its constraint 8 scopes the staleness sweep to files the round edits, and editing it anyway would have been the silent scope change §4.5 makes a block condition — so it was declared in the handback instead, which is the shape this workflow wants from a worker who finds a true sentence outside its own change set. THE REVIEWER IS AT FAULT for writing a forward reference as a ROUND NUMBER rather than as a PATH: a round number resolves to nothing a reader can open, and it goes stale on a schedule nobody tracks. THE FIX: name the component, not the round, here and wherever else this branch left one.
<<<END FINDINGS39

<<<SLICE LEDGER39
Gate: F031 R38 — the F031 R38 entry. R38 PASSED ON EVERY ONE OF ITS NINE GATES, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk rather than reading the handback back; every value that handback states reproduced exactly, including all seven per-commit insertion counts and every cell of its `## Commits` table. THIS IS THE ROUND THAT MADE THE INBOX ANSWERABLE, the last step of T003: the token now travels `RemedyApp` to `RemedyShell` to `RightLivePanel` to `DecisionInboxCard` as a REQUIRED prop under one spelling at every hop, the card builds `{ jobId, serverToken }` with NAMED fields from `dashboard.jobId`, a click calls `answerDecisionCard`, and the sentence comes back coloured by its tone. TRANSPORT HELD for the tenth round running: the C0a blob at `173573e0`, the C0b blob at `eb959257` and both working copies read off disk at `279cd819` are ALL FOUR byte-identical at sha256 `8a3d0e942842451e71fced4d310b51e667360f650a5b6d0f4fb98bcccea30f8b` over 22029 bytes and 271 lines, C0a and C0b resolving to the SAME git blob `f3833bda`. THE BLOCK MEASURED THE SAME ON DISK AS IT DID BEFORE EMISSION — 271 TOTAL, 47 CONTENT, 224 PROSE, against caps of 490 and 400 — which is what stands in for the hash-stamp ritual when a block travels by prompt and no scratchpad original exists (docs/agents/self_drive_protocol.md). THE PLAN at `4de53f90` equals PLANF031R38 exactly at 2638 bytes and 46 lines, minus-newline control FALSE, `^## Goal$` 1, `^## Next Steps$` 1. THE APPEND at `a5d1268e` is 795163 + 1 + 3720 = 798884 against an actual 798884, prefix preserved. THE SETS MOVED ONLY WHERE CONSTRAINT 9 ALLOWED: `^- R-\d+ — ` 246 to 246 with ADDED and REMOVED both EMPTY and all DISTINCT, `^Done: R-\d+ — ` 5 to 5, `^Landed: R-` 0 to 0, `^Gate: R\d+ — ` 19 to 19, `^Gate: F\d+ R\d+ — ` 18 to 19 with the ADDED key exactly `F031 R37`; open set 241. MARKERS 0 and 0 in the plan at `4de53f90` and the ledger at `a5d1268e` against a live CONTROL of 2 and 2. THE CHANGE SET IS EXACT IN BOTH DIRECTIONS: 13 paths, range-minus-declared EMPTY and declared-minus-range EMPTY, nothing under `docs/`, `packages/` or `apps/cli/`, and one path under `tests/`. THE SEVEN COMMITS ARE EACH SINGLE-PARENT at insertions 271, 236, 17, 2, 147, 198 and 72, each under the 500 DECISION F104 D1 counts; the reflog reads `commit` in every prefix, so `amend`, `rebase` and `cherry` are 0 each. THE GATES THE REVIEWER RE-RAN: `tsc --noEmit` REAL exit 0 with no diagnostic, `vitest run` REAL exit 0 at 30 files and 448 tests IDENTICAL to base, and the six Python suites SERIALLY at 480, 52, 21, 16, 541 passed with 4 skipped, and canary 42 — `tests/ui_contracts/` moving 525 to 541, which is EXACTLY the 16 the new guard collects. THE RED PROOF DISCRIMINATES, AND THE REVIEWER PROVED IT ON A SECOND, INDEPENDENT MUTATION THE BLOCK NEVER ORDERED: in a disposable worktree at `279cd819`, deleting the single occurrence of `serverToken={serverToken}` in `RemedyShell.tsx` failed exactly `TestServerTokenReachesTheCard::test_shell_passes_the_token_to_the_live_panel` at exit 1, and replacing the single occurrence of the `answerDecisionCard(target, decision, answer.value)` call failed exactly `TestAnswerClickCallsTheFlow::test_card_calls_the_flow_with_the_target_the_decision_and_the_answer` at exit 1, each restoring to 16 passed; the worktree was removed by its exact path and `git worktree list` returned to 1 line. THE PUSH LANDED: local tip, `origin/feature/f031-decision-inbox` and `git ls-remote` all read `279cd819`. THE HANDBACK IS 93 LINES against the 100-line tier its seven commits earn, no DECISION D15 overage declared. THREE THINGS THE WORKER ROUTED TO THE REVIEWER, ALL THREE ADJUDICATED HERE. FIRST, the fourth CSS class `.decisionOutcome` beside the three tone classes is ACCEPTED and is not a deviation: constraint 7 forbade inventing a design token and writing a raw hex, that class carries layout alone, and the three tones resolve to `--remedy-green-500`, `--remedy-orange-400` and `--remedy-red-500`, each already defined in the shipped sheet. SECOND, leaving the stale sentence in `decisionAnswerFlow.ts` was CORRECT — it sits outside the block's change set, and editing it would have been the silent scope change §4.5 makes a block condition — and it is now registered as R-0688 rather than being repaired out of scope. THIRD, the worker's doubt about the live region was RIGHT and the reviewer's S5 was WRONG; it is registered as R-0686. R-0687 the reviewer raised on its own reading of the same commit. ALL THREE ARE THE SPECIFICATION'S DEFECTS AND NONE IS A BLOCK CONDITION: no fabricated value, no false live indicator, no missing table, no unverified claim, no silent scope change. A round that ships what it was told and flags what it doubts is the workflow working, and R39 repairs all three.
<<<END LEDGER39

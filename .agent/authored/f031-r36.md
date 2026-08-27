── STEP R36 — F031 Decision inbox ────────────────────────────
Goal:        Record R35's PASS, then ship T003's two remaining PURE modules:
             the outcome sentence an operator reads and the flow that sequences
             mint, build, send and outcome behind injected seams. This is the
             work R34 was to do and never began, returning under its own number
             because R34 landed a commit and earned its key (§3 item 26). NO
             COMPONENT IS WIRED THIS ROUND — the token threading, the click
             handler and the enabled buttons are R37's.

Fortschritt: ~97 % (F031 claimed; R1 through R35 landed, R35 gated here ·
             T001 SHIPPED · T002 COMPLETE · T003 answer command, request,
             deep-link, submit and nonce seams shipped; outcome sentence and
             flow land here, component wiring open) — Schaetzung

Bundle:      C0a save this block · C0b mirror it into last_block · C1 the plan
             and DECISION F031 D18 together · C2 the R35 gate entry · C3 the
             outcome module and its tests · C4 the flow module and its tests ·
             C5 handback.

Change set:  exactly these paths, nothing else —
             .agent/authored/f031-r36.md                             (C0a)
             .agent/last_block.md                                    (C0b)
             .agent/plan.md, .agent/decisions.md                     (C1)
             .agent/live_review.md                                   (C2)
             apps/ui/src/api/decisionOutcome.ts                      (C3)
             apps/ui/src/api/decisionOutcome.test.ts                 (C3)
             apps/ui/src/api/decisionAnswerFlow.ts                   (C4)
             apps/ui/src/api/decisionAnswerFlow.test.ts              (C4)
             .agent/handoff.md                                       (C5)
             This list bounds the round's WRITES, not its ACTIONS: the push
             named in G11 is ordered explicitly and is not a file (R-0674).

── Base ──────────────────────────────────────────────────────
The round base is `ce4da4a1bdcf5837b751767aa4d3cba107a0532a`, the R35 handback
commit and the tip of `feature/f031-decision-inbox`; the reviewer read the local
tip, the remote-tracking ref and `git ls-remote origin` at the R35 gate and all
three agreed. Stay on that branch; never commit to `main`. Every SHA-shaped
token here resolved under `git cat-file -t`.

Readings the reviewer MEASURED at that base, re-checkable there:
- `.agent/live_review.md` 778079 bytes and 1287 lines; `^- R-\d+ — ` 246 all
  DISTINCT, maximum `R-0685`; `^Done: R-\d+ — ` 5, so the §3 item 10 open set
  is 241; `^Recurrence: R-` 25; `^Landed: R-` 0. THE GATE SERIES IS SPLIT by
  DECISION F031 D7: `^Gate: R\d+ — ` 19, frozen, and `^Gate: F\d+ R\d+ — ` 16.
  `^Gate: F031 R35 — ` occurs 0 times, so LEDGER36's header is the first of its
  key, and the three headers above it read `Gate: F031 R32 — the F031 R32
  entry.`, `Gate: F031 R33 — the F031 R33 entry.` and `Gate: F031 R34 — the
  F031 R34 entry.`, which is the shape its own header matches (§3 item 26).
- `.agent/plan.md` 2823 bytes and 49 lines. `.agent/decisions.md` 597218 bytes
  and 8013 lines, its last entry `## DECISION F031 D17 (2026-08-26)`, and the
  file's final two bytes are a newline preceded by `.` — DECISIOND18 is a pure
  EOF append.
- `docs/roadmap/**` is UNTOUCHED: the §3 docs-round gate is not earned.
- The six Python suites at that base, run SERIALLY by the reviewer, every one a
  REAL exit 0: `tests/ui_server/` 480, `test_test_runner` 52,
  `test_resource_safety` 21, `test_integrity_gate` 16, `tests/ui_contracts/`
  525 passed with 4 skipped, and the canary `test_golden_path` 42.
- THE UI GATES ARE EARNED THIS ROUND, because the change set holds files under
  `apps/`. At the base, run by the reviewer in the PRIMARY `apps/ui`:
  `npm run typecheck` REAL exit 0 with zero diagnostics, and `npm run test:unit`
  REAL exit 0 at 28 files and 419 tests. The eight decision test files carried
  `decisionAnswer` 20, `decisionCard` 36, `decisionFilter` 20, `decisionFocus`
  7, `decisionNonce` 9, `decisionOrder` 16, `decisionSend` 12 and
  `decisionSubmit` 10. Neither `decisionOutcome.ts` nor `decisionAnswerFlow.ts`
  exists yet; the four modules they build on all do.
- THE PROBE RECIPE G9 ORDERS WAS RUN BY THE REVIEWER AT THIS BASE, both green
  and red, so you need not invent one. A fresh worktree has no
  `apps/ui/node_modules` (R-0518) and symlinking one is denied, so vitest is
  launched FROM the primary `apps/ui` with the worktree as its root and the
  PRIMARY config, resolving vitest from the primary's dependencies while
  collecting the worktree's sources. Unmutated over two existing decision test
  files: 2 files, 19 tests, REAL exit 0. With `.filter(isCommandNonceCharacter)`
  — 1 occurrence — deleted from the WORKTREE copy of `decisionNonce.ts`: REAL
  exit 1, 1 failed, 18 passed, the primary's `git status --porcelain` 0 lines
  after, and the worktree removed BY ITS EXACT PATH leaving `git worktree list`
  at 1 line. That red proves the run reads the worktree and not the primary.
- THIS BLOCK'S OWN TWO CAPS, measured on its final bytes before emission and
  stated so your re-measurement can disagree with the reviewer's, are 490 lines
  TOTAL (DECISION F085 D6) and 400 lines PROSE (DECISION F085 D5). G2 orders
  you to report both from the COMMITTED blob.

── Constraints ───────────────────────────────────────────────
1. Apply every authored SLICE BYTE FOR BYTE. Never retype, rewrap or "fix" one.
   If a slice looks wrong, apply it verbatim and DECLARE the disagreement: a
   contradiction in this block is the reviewer's defect, not yours to repair.
2. Slice transport. The reviewer's original is on disk at
   `.remedy-wt/f031-r36.md`. COPY that file to `.agent/authored/f031-r36.md` at
   C0a — never retype it — and mirror it byte-identically into
   `.agent/last_block.md` at C0b. THIS BLOCK STATES NO DIGEST OF ITSELF: a file
   cannot carry its own sha256, so the proof is G1's disk-to-disk comparison
   over four readings, which docs/agents/self_drive_protocol.md substitutes for
   the hash-stamp ritual when there is no transport. Report the digest YOU
   measure. Extract every slice PROGRAMMATICALLY out of the COMMITTED C0a blob
   by its marker LINES — `<<<SLICE <NAME>` opens, `<<<END <NAME>` closes.
   Markers never reach a target file.
3. Commit sequence, exactly: C0a, C0b, C1, C2, C3, C4, C5 — none extra, none
   dropped, none reordered. C1 is FIRST substantive because this round writes
   the finding ledger (§3 item 23), and carries the plan AND DECISION F031 D18
   TOGETHER so the plan's reference to D18 is true at the commit that makes it
   (§3 item 20, R-0524). To correct a landed commit do NOT add one outside this
   sequence — declare it, with its own `## Commits` and item-status rows.
4. Never amend, rebase, cherry-pick, force-push or rewrite history; never delete
   a branch; never merge; create no pull request.
5. `git status --porcelain` prints 0 lines after every commit. Read
   `.agent/STOP` from disk before C0a and again before C5, and REPORT WHAT YOU
   READ rather than the value this block expects; if it is present, finish the
   commit in hand, write the handback and stop. NEVER delete that sentinel
   (R-0347).
6. The slices this block carries are the whole text PLANF031R36, the appended
   text DECISIOND18 and the appended text LEDGER36. This paragraph names them
   and states no count; G2 orders you to report the count YOUR extractor
   measured.
7. THE TWO APPENDS' SHAPE, STATED ONCE HERE, WITH EVERY GATE NAMING THIS
   PARAGRAPH RATHER THAN RESTATING IT. Under the newline-INCLUDED convention
   each slice already ends in a newline, so a target after its append is
   EXACTLY its blob before that commit, then one newline, then the slice —
   `.agent/decisions.md` with DECISIOND18 at C1, `.agent/live_review.md` with
   LEDGER36 at C2. Each receives NOTHING ELSE in that commit and nothing in any
   other commit of this round (R-0657). Paragraph counts are yours to measure.
8. THIS BLOCK CARRIES NO FROM/TO PAIR, so no containment test is reported and
   no FROM-zero count is ordered (§3 item 15). The plan is a WHOLE-FILE
   replacement; DECISIOND18 and LEDGER36 are appends.
9. THIS ROUND MINTS NO FINDING ID AND RESOLVES NONE. LEDGER36 carries no `- R-`
   paragraph, no `Done:` line and no `Recurrence:` line, so `^- R-\d+ — ` stays
   246 with the maximum still `R-0685`, `^Done: R-\d+ — ` stays 5, leaving the
   §3 item 10 open set UNCHANGED at 241, and `^Recurrence: R-` stays 25. It
   carries ONE `Gate: F\d+ R\d+ — ` header, so that count moves 16 → 17 with the
   added key exactly `F031 R35`. `^Landed: R-` stays 0: WRITE NO `Landed:` LINE.
   No landed finding paragraph is edited (§3 item 20).
10. THE PRODUCTION CHANGE IS DESCRIBED, NOT SLICED. S1 through S6 below fix
    behaviour, seam, public surface and honesty rules; you write the code under
    the AGENTS.md self-review loop and the repo's own conventions, and you are
    expected to catch what the spec got wrong and declare it. Touch nothing
    under `docs/`, `packages/` or `tests/`, and no file under `apps/` other
    than the four the change set names. The "nothing posts yet" header
    sentences in `decisionCard.ts` and `DecisionInboxCard.tsx` stay UNTOUCHED
    and stay TRUE: no component calls the flow, so R37 retires them.
11. Destructive verification runs ONLY inside a disposable `git worktree` under
    `.remedy-wt/`, removed BY ITS EXACT PATH (R-0662). Everything already there
    is pre-existing scratch belonging to no commit, this block's own file
    included: create no worktree at an existing path, and delete nothing you did
    not create. NEVER `cd` for a mutation — address the worktree file by ABSOLUTE
    path, run the tests with an explicit working directory, and read the PRIMARY
    checkout's `git status --porcelain` immediately after.

── Specification ─────────────────────────────────────────────
S1  `apps/ui/src/api/decisionOutcome.ts` — EVERY SENTENCE AN OPERATOR READS
    ABOUT A SENT ANSWER, and nothing else. It is pure: no clock, no socket, no
    storage, no randomness, and no input makes it throw. It exports a tone
    union whose members are `ok`, `warn` and `error`; a message interface
    carrying that tone and one `sentence` string; a function mapping one
    `DecisionSubmitResult` to a message; and a second function answering the
    message for an answer that was never sendable at all. The second exists
    because an unsendable answer has no `DecisionSubmitResult` to map, and
    adding a fourth member to `decisionSubmit.ts`'s closed outcome union would
    change a shipped vocabulary for a case that never reaches the wire.
    RETURN A FRESH OBJECT from both, never a shared constant, so no caller can
    mutate the vocabulary for every other caller.

S2  THE TONE RULE, which is what makes `tone` carry something the outcome alone
    does not: `ok` when the door accepted; `warn` when trying again could
    plausibly help; `error` when it could not. `accepted` is `ok`.
    `unreachable` is `warn`: nothing was heard back and the request may simply
    not have arrived. A `refused` maps by STATUS, over the statuses
    `packages/orchestration/ui_server.py` really answers, named in
    `decisionSubmit.ts`'s own header: 429 over the rate budget is `warn`, while
    403 for a bad token or double-submit header, 400 for a malformed body, 409
    for a decision absent or no longer open, and 501 for an id the server does
    not dispatch are each `error`. Any OTHER status is `error` with a sentence
    that does not pretend to know which refusal it was. DERIVE NOTHING FROM THE
    NUMBER ITSELF — no range arithmetic, no `>= 500` branch — so a status that
    door never sends cannot acquire a confident sentence by accident.

S3  THE SENTENCES ARE THE OPERATOR'S, not the protocol's. Each says what
    happened to THEIR answer and, where true, what they can do next. No
    sentence contains a status number, a header name, a URL or the word
    `fetch`: the number rides in the result the caller already holds, and a
    sentence that leaks it turns a card into a console. Every sentence is a
    module-scope `const` rather than an inline literal, so the vocabulary is
    readable in one place — the convention `DecisionInboxCard.tsx` follows.

S4  `apps/ui/src/api/decisionAnswerFlow.ts` — ONE ANSWER, END TO END, as the
    only place the four T003 modules are sequenced. It exports a deps interface
    and one async function taking the send target, the card model, the answer
    text and those deps, and answering a message from S1. EVERY DEPENDENCY IS
    AN INJECTED SEAM WITH A DEFAULT: the nonce minter, the request builder, the
    submit, and the deadline. The defaults are the shipped functions, so a
    caller passes nothing and a test passes everything. IT NEVER THROWS and it
    always answers a message. Order of work: mint; if that answers `null`,
    return the unsendable message WITHOUT touching the network. Build; if that
    answers `null`, the same. Otherwise submit, and map what comes back.

S5  THE DEADLINE, WHICH IS THE ONLY CLOCK IN THIS CHAIN. `submitDecisionSendRequest`
    sets no timeout by design (DECISION F031 D16) and every other module in
    this chain states in its own header that it reads no clock, so the flow
    races the submit against a `deadline` seam — a function answering a promise
    that settles when the wait is over — whose default is the one place a timer
    is created. WHEN THE DEADLINE WINS the flow answers the message for an
    `unreachable` result at status 0, reusing the closed vocabulary rather than
    adding a fourth outcome: from the operator's seat "we never heard back" and
    "we could not reach it" are one sentence, and `decisionSubmit.ts` fixes
    status 0 as the number no door answers. THE SEND IS NOT CANCELLED and never
    retried — the flow stops WAITING, and the WHY comment above the race says
    exactly that so no reader believes the request was withdrawn. DECISIOND18
    records this as DECISION F031 D18.

S6  TESTS: one `.test.ts` beside each new module, which is what the shipped
    `apps/ui/vitest.config.ts` collects — it sets the environment to `node` and
    includes `src/**/*.test.ts` only, so a `.tsx` test would not be collected
    and no DOM harness exists (DECISION F031 D5). Assert the tone AND the
    sentence identity for every branch S2 names, including the unknown-status
    fallback; assert both `null` paths of S4 reach no submit, by passing a
    submit seam that records whether it was called; assert that a submit which
    never settles still answers, by passing a deadline that settles at once;
    and assert that a submit which settles first wins the race. PATCH NO
    GLOBAL: no test under `apps/ui/src` patches one today, and a leaked global
    fails in an unrelated file. Give every test a name that reads as a sentence
    about behaviour, as the neighbouring decision tests do.

<<<SLICE PLANF031R36
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
R36 records R35's PASS, then ships T003's two remaining PURE modules:
`decisionOutcome.ts`, the sentence and tone an operator reads for one send's
result, and `decisionAnswerFlow.ts`, which sequences mint, build, send and
outcome behind injected seams. This is R34's unstarted work under a new number.
No component is wired this round.

## Next Steps
1. R37, the COMPONENT round: thread the server token from `RemedyApp`'s
   `readUrlState` through `RemedyShell` and `RightLivePanel`, call the flow on
   a click, render its sentence and enable the buttons.
2. The clarification FORM, and the ruling on `NeedsAttentionCard`'s decision
   branch (DECISION F031 D4).
3. The integration-gate round per `docs/agents/integration_gate.md`, whose
   block also carries the §3 checklist items R-0683, R-0377, R-0419, R-0429,
   R-0560, R-0583 and R-0633 route there, then closure per
   `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- THE ONLY CLOCK IN THE ANSWER CHAIN IS THE FLOW'S DEADLINE SEAM.
  `submitDecisionSendRequest` sets no timeout by design (DECISION F031 D16), so
  DECISION F031 D18 puts the timer behind one injected seam and maps a deadline
  win onto the existing `unreachable` outcome. The send is not cancelled; the
  flow stops waiting.
- THE SERVER STILL ACCEPTS A BLANK ANSWER AND WRITES IT ONCE. R29 stopped it in
  the browser only; DECISION F031 D14 routes that check to F009, not fixed here.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 241 at `ce4da4a1` and this round leaves it there.
- The findings THIS FEATURE MUST STILL ACT ON are R-0377, R-0403, R-0413,
  R-0419, R-0429, R-0431, R-0441, R-0445, R-0471, R-0495, R-0533, R-0560,
  R-0574, R-0583, R-0593, R-0601, R-0622, R-0625, R-0632, R-0633, R-0672,
  R-0674, R-0675, R-0676, R-0677, R-0678, R-0679, R-0683, R-0684 and R-0685;
  R-0495 and R-0574 are the two Highs.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R36

<<<SLICE DECISIOND18
## DECISION F031 D18 (2026-08-26) — the answer flow owns the only clock in the chain, and a deadline win reuses the `unreachable` outcome

CHOSEN, THE FLOW BOUNDS THE SEND AND THE SUBMIT STILL DOES NOT. DECISION F031
D16 rules that `submitDecisionSendRequest` sets no timeout, reads no clock and
never retries, and `decisionAnswer.ts`, `decisionSend.ts` and `decisionNonce.ts`
each state in their own headers that they read no clock either. A send that
never settles therefore had no deadline anywhere, which would leave a button
disabled forever the moment R37 wires one. The deadline lands in
`apps/ui/src/api/decisionAnswerFlow.ts` as an INJECTED SEAM with a default, so
exactly one module in this chain creates a timer and every other module's
no-clock claim stays true.

CHOSEN, A DEADLINE WIN IS `unreachable` AT STATUS 0 RATHER THAN A FOURTH
OUTCOME. `decisionSubmit.ts` declares its outcome union closed at three and
fixes status 0 as the one number no door answers. From the operator's seat a
request that was never answered and a request that never arrived are the same
sentence, so a fourth member would add a branch every future caller must handle
to say something nobody reads differently.

CHOSEN, THE SEND IS NOT CANCELLED. The flow stops WAITING; the request may still
arrive and be written. Judging when a write may be abandoned belongs to whoever
knows what the write meant, which is not this layer, and an `AbortController`
here would promise a withdrawal the server never agreed to.

SUPERSEDING A ROUND ATTRIBUTION IN DECISION F031 D17: that entry says the
outcome sentence and the wiring both land in R33. R33 and R35 became record
rounds and R34 stopped on the `.agent/STOP` sentinel without starting, so the
outcome sentence and the flow land in R36 and the component wiring is R37. The
split D17 chose is unchanged; only the round numbers moved.

REVERSE IT by deleting the deadline seam and awaiting the submit directly. The
outcome vocabulary needs no change, because nothing was added to it.
<<<END DECISIOND18

<<<SLICE LEDGER36
Gate: F031 R35 — the F031 R35 entry. R35 PASSED ON EVERY ONE OF ITS EIGHT GATES, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk rather than reading the handback back; every value that handback states reproduced cell for cell. THE ROUND RECORDED TWO VERDICTS AT ONCE, WHICH IS WHY IT EXISTED: R33 and R34 both reached this session ungated — R33 because its own block wrongly claimed the §4.13 terminator carve-out, R34 because it stopped on the `.agent/STOP` sentinel after a single commit — and Phase 1 rule 4 of docs/agents/self_drive_protocol.md forbids planning new work over an ungated round. TRANSPORT HELD IN ITS STRONGEST FORM for the seventh round running: the reviewer's own scratchpad original `.remedy-wt/f031-r35.md`, the C0a blob committed at `6f018cd2`, the C0b blob committed at `5a609009` and `.agent/last_block.md` read off disk at `ce4da4a1` are ALL FOUR byte-identical at sha256 `5ef05e5da2ed9d78c7743984eeca256fdfcddc364de8f5e398dd6f0c53838b30` over 33595 bytes and 312 lines, C0a and C0b resolving to the SAME git blob `f20be294bce30965c80a5b5b7864dfdc7324fd71`. THE EXTRACTION printed 2 slices, 54 content lines and 312 total, so PROSE was 258 against the 400-line cap DECISION F085 D5 sets and TOTAL 312 against the 490 DECISION F085 D6 sets. THE PLAN at `7b642dff` equals PLANF031R35 exactly at 2823 bytes and 49 lines, with the trailing-newline-removed control FALSE, `^## Goal$` 1 and `^## Next Steps$` 1, and 49 strictly under the 50 AGENTS.md sets — a bound the reviewer's OWN DRY RUN caught at 52 lines and trimmed to 49 BEFORE emission, which is the R-0654 clause-versus-clause trap defeated by measurement rather than by luck. THE C2 APPEND SATISFIED WHOLE-FILE EQUALITY: `.agent/live_review.md` at `08c0d06b` is its C1 blob plus one newline plus LEDGER35, at 764867 + 1 + 13211 = 778079 against an actual 778079, and the SECOND, INDEPENDENT READER AGREED — a blank-line split moves the unit count 327 to 330, N is 3 by that split, and the last three units equal LEDGER35's three paragraphs IN ORDER with trailing newlines rstripped on BOTH sides, while the same three SWAPPED are rejected. THE NEGATIVE CONTROL WAS RUN IN MEMORY, never on the tracked file: one byte flipped inside the appended text, and both readers REJECT the mutant while both ACCEPT the true file. THE SETS MOVED EXACTLY WHERE THAT BLOCK'S CONSTRAINT 9 ALLOWED AND NOWHERE ELSE: `^- R-\d+ — ` 246 to 246 with the ids ADDED and the ids REMOVED BOTH the EMPTY SET and all 246 DISTINCT, maximum `R-0685` unmoved; `^Done: R-\d+ — ` 5 to 5 with the ids ADDED the EMPTY SET; `^Landed: R-` 0 to 0; `^Gate: R\d+ — ` 19 to 19 frozen and `^Gate: F\d+ R\d+ — ` 14 to 16, the added keys exactly `F031 R33` and `F031 R34`, all keys DISTINCT; `^Recurrence: R-` 24 to 25 and `^Recurrence: R-0583` 0 to 1. The §3 item 10 open set is 241 at `08c0d06b`, and `- R-0583 — ` still occurs exactly ONCE line-anchored, so its landed paragraph was not edited. HYGIENE HELD: line-anchored `^<<<SLICE ` and `^<<<END ` are 0 in `.agent/plan.md` at `7b642dff` and `.agent/live_review.md` at `08c0d06b`, against a CONTROL of 2 and 2 over the C0a blob; the range `cae07944`..`08c0d06b` names 4 paths, all under `.agent/`, none under `docs/`, `packages/`, `tests/` or `apps/` and neither `.agent/context.md` nor `.agent/decisions.md` nor either inventory file, with range-minus-change-set EMPTY and change-set-minus-range exactly `.agent/handoff.md`; the five commits `6f018cd2` through `ce4da4a1` are each SINGLE-PARENT with insertions 312, 217, 23, 6 and 71 read from `git diff --numstat`, each under the 500 cap AGENTS.md DECISION F104 D1 sets, and the first four agree cell for cell with the `+/-` column of that handback's `## Commits` table; `git ls-files .remedy-wt` 0, the zip glob 0, `git worktree list` 1 line and `git status --porcelain` 0. THE BLOCK'S OWN OBJECT IDS RESOLVE: 26 SHA-shaped occurrences, 11 distinct, 10 `commit` and 1 `blob`, failing set EMPTY. THE REFLOG, scoped to this round's entries, reads `commit` throughout, so `amend`, `rebase` and `cherry` are 0 each. THE SUITES ARE THE REVIEWER'S OWN, run SERIALLY in the primary checkout, never two alive at once, every one a REAL exit 0: `tests/ui_server/` 480, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16, `tests/ui_contracts/` 525 passed with 4 skipped, and the canary `test_golden_path` 42, every count identical to the base reading, and NO `apps/ui` command was ordered or reported because the change set held no file under `apps/`. THE PUSH DISCHARGED: the local tip, the remote-tracking ref and `git ls-remote origin` all read `ce4da4a1bdcf5837b751767aa4d3cba107a0532a`, no pull request was created, no branch deleted and nothing merged. THE FIVE DECLARED ITEMS ARE ADJUDICATED AND NONE IS A DEFECT. The declared handback overage at 90 lines against the 60-line tier its 5 commits earn — 5 not being MORE THAN 5, which is what the 100-line tier requires — is accepted under the AGENTS.md stated-cause ruling DECISION D15, with no section dropped. Reading exit codes through `subprocess.run(...).returncode` because this session's guard refuses `$?` is a method difference over verbatim argv. Committing C0a and C0b while the plan still described R33 is what constraint 3 ordered, and the declaration is correct. Item 4 declares that no contradiction was found and nothing was applied other than verbatim, which the reviewer's own four-way transport reading confirms. Item 5's assumption, that a paragraph is a blank-line-delimited unit, is the reading G4 intends and the one that makes N measure 3. ITS `## Next` STATES NO VERDICT, NO COLOUR AND NO PASS FOR ITSELF, so R-0583's defect did not recur in the very round that recorded it. THE VERDICT IS PASS.
<<<END LEDGER36

── Done when ─────────────────────────────────────────────────
Run every gate yourself, record its REAL exit code and REAL output, and report
ONE ENTRY PER GATE in the handback, as briefly as the ordered values allow and
with transcripts kept out (R-0582). "Green" as a word is a finding. Every gate
runs at a commit STRICTLY EARLIER than C5 (§3 item 31); G11's push follows it.

G1  Branch, cleanliness, transport. `git branch --show-current` prints
    `feature/f031-decision-inbox` and NOT `main`; report what `.agent/STOP` read
    from disk actually was before C0a and again before C5, per constraint 5;
    `git status --porcelain` line count after each commit through C4 is 0. Then
    report sha256, byte count and line count for FOUR readings —
    `.remedy-wt/f031-r36.md` before C0a, the committed C0a blob, the committed
    C0b blob, and `.agent/last_block.md` off disk after C0b — ALL FOUR EQUAL,
    and the git blob id of C0a's and C0b's file, the SAME id.

G2  Extraction and the block's own two caps. Run your extractor over the
    COMMITTED C0a blob and report the slice count, the CONTENT lines inside
    markers, and the TOTAL — the numbers YOUR extractor printed — then PROSE as
    TOTAL minus CONTENT, against the two caps the Base names. If either is
    exceeded say so plainly and continue; it is the reviewer's to fix.

G3  The plan. `.agent/plan.md` at C1 is byte-equal to PLANF031R36 under your
    stated newline convention; report slice length, file length and convention.
    NEGATIVE CONTROL: NOT byte-equal to that slice MINUS its trailing newline.
    `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` STRICTLY under 50.

G4  The two appends, EACH as ONE equality over the whole file, in the shape
    constraint 7 states — name that paragraph, do not restate its formula.
    Report the boolean and the byte arithmetic for `.agent/decisions.md` at C1
    and for `.agent/live_review.md` at C2, against the pre-commit lengths you
    measure yourself. For the DECISIOND18 append report a SECOND, INDEPENDENT
    reading: split the committed file on blank lines, take the LAST N units,
    and confirm they equal DECISIOND18's paragraphs IN ORDER, where N is the
    number YOUR split measured; give the unit count before and after, and STATE
    YOUR TRAILING-NEWLINE HANDLING, because a naive split reports FALSE on a
    byte-perfect file. That slice carries MORE THAN ONE paragraph, so ORDER is
    load-bearing: report the SWAPPED comparison too, and it must be false.
    LEDGER36 is a SINGLE paragraph, so no order reading is ordered for it.
    NEGATIVE CONTROL, for each append: flip ONE byte inside the appended text;
    the reader must reject the mutant and accept the true file, IN MEMORY only.

G5  The ledger sets, base versus C2 in `.agent/live_review.md`, in the shape
    constraint 9 states — report each side of every movement it names, that the
    `- R-` ids ADDED and REMOVED are BOTH the EMPTY SET, that all
    `^- R-\d+ — ` ids are DISTINCT, that the maximum is still `R-0685`, and
    that the `^Done: R-\d+ — ` ids ADDED are ALSO the EMPTY SET.
    `^Gate: R\d+ — ` 19 → 19 UNCHANGED, and `^Gate: F\d+ R\d+ — ` 16 → 17, the
    ADDED key being exactly `F031 R35`, all keys DISTINCT (§3 item 26). Report
    `^Recurrence: R-` 25 → 25 and `^Landed: R-` 0 → 0. Report the §3 item 10
    open set at C2.

G6  Markers, paths, commit shapes and object ids. Line-anchored `^<<<SLICE `
    and `^<<<END ` are all 0 in `.agent/plan.md` and `.agent/decisions.md` at
    C1, in `.agent/live_review.md` at C2, and in every file C3 and C4 write,
    against the same counts over the COMMITTED C0a blob as a CONTROL, where
    they are NOT 0. ONLY the line-anchored reading is ordered — this block
    quotes both markers inside backticks mid-line, so a raw SUBSTRING count is
    unmeetable and is NOT ordered. `git diff --name-only <base>..C4` names NO
    path under `docs/`, `packages/` or `tests/`, and neither
    `.agent/context.md` nor either inventory file; the range path set MINUS the
    change set is EMPTY and the change set MINUS the range is exactly
    `.agent/handoff.md`, which C5 writes. Over C0a..C4 report per commit that
    it is single-parent and its INSERTION count — the `+` column only, per
    AGENTS.md DECISION F104 D1 — each under 500; those same numbers fill the
    `+/-` column of the `## Commits` table, derived from `git diff --numstat`
    and NOT from `git commit`'s own summary, and you report that the two agree
    cell for cell (§3 item 28). Report `git ls-files .remedy-wt` as 0, the zip
    glob as 0, and `git worktree list` as 1 line at C4. FOR THE REFLOG state
    SCOPE and FIELD: over THIS ROUND'S entries only, by the OPERATION PREFIX
    before the first colon of `git reflog --format=%gs`, report `amend`,
    `rebase` and `cherry` each 0 and how many you scoped to. Finally extract
    every SHA-shaped token from the COMMITTED C0a blob with the word-bounded
    pattern matching 7 to 40 hex characters — whose boundaries do NOT match the
    64-char sha256 digest this block also carries — pass each to
    `git cat-file -t`, and report the token count YOUR extractor measured, the
    type per token, and the FAILING SET, which MUST BE EMPTY.

G7  The new modules' own shape, read off the COMMITTED files at C4 and reported
    as counts you measured. In `decisionOutcome.ts`: `fetch`, `setTimeout`,
    `Date.now` and `localStorage` are each 0, and no sentence constant contains
    a digit. In `decisionAnswerFlow.ts`: `fetch` and `localStorage` are 0 — it
    reaches the network only through the injected submit — and every dependency
    it names has a default, shown by the exported function being callable with
    the deps argument omitted. In BOTH new test files `vi.` and `globalThis`
    are 0, so no global was patched. Report that `decisionSubmit.ts`'s outcome
    union is UNEDITED at the three members it had at the base.

G8  The UI gates, in the PRIMARY `apps/ui` at the C4 tree, both a REAL exit 0,
    by these exact command lines with no extra flag:
      npm run typecheck
      npm run test:unit
    Report typecheck's diagnostic count and, for the unit run, the FILE count
    and the TEST total, the per-file count of each of the two NEW test files,
    and that the eight decision test files the Base names are UNMOVED at the
    counts it gives. Account for any difference. Do NOT run `npm run lint`: its
    eslint parses no TypeScript in this repo and is red at the base, so it
    would measure nothing (R-0622).

G9  MUTATION PROBES, one per new module, in a disposable worktree created at a
    path that does not yet exist under `.remedy-wt/` and removed BY THAT EXACT
    PATH afterwards. Use the recipe the Base reports: launch vitest FROM the
    primary `apps/ui`, with the worktree's `apps/ui` as the root, the PRIMARY
    `apps/ui/vitest.config.ts` as the config, and the two new test files named
    as arguments — a fresh worktree has no `node_modules`, and this is the form
    the reviewer proved both green and red at the base. Take an UNMUTATED
    reading first, then one at a time, each mutation applied to the WORKTREE
    copy only and restored before the next:
      (a) in `decisionOutcome.ts`, change the tone the 429 branch answers to
          the tone an unrecoverable refusal answers;
      (b) in `decisionAnswerFlow.ts`, defeat the race so the submit is awaited
          directly and the deadline is never consulted.
    FOR EACH, name the exact byte string you changed, report its occurrence
    count IN THAT FILE — which must be 1, and if it is not, choose a longer
    string that is unique and say which you used (§3 item 25) — then report the
    REAL exit code, the passed and failed counts, and the FAILING NODE IDS.
    THIS BLOCK NAMES NO TEST AND ORDERS NO COLOUR: report what happened. A
    GREEN MUTATION IS THE HONEST ANSWER TO DECLARE, not to paper over, and it
    tells the reviewer its own spec left a branch unreached (R-0633). Report
    the primary checkout's `git status --porcelain` as 0 lines immediately
    after the last restore, and `git worktree list` as 1 line after removal.

G10 The state readers and the canary, in the PRIMARY checkout at the C4 tree,
    all REAL exit 0, run SERIALLY and never two alive at once, by these exact
    command lines with no extra flag:
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/ui_contracts/ -q
      python3 -m pytest tests/cli/test_golden_path.py -q
    These are the four state readers a round rewriting `.agent/` state gates,
    plus `tests/ui_contracts/`, which scans every shipped source under
    `apps/ui/src`, plus the canary. Account for any difference from the Base's
    counts. Report `git worktree list` as 1 line immediately BEFORE the first
    of them.

G11 The push. AFTER C5, run `git push origin feature/f031-decision-inbox`, then
    report that the local tip, the remote-tracking ref and `git ls-remote
    origin` for this branch all read the SAME sha. No `--force`, no
    `--force-with-lease`, no history rewrite, no branch deletion, no pull
    request, nothing merged.

── Handback ──────────────────────────────────────────────────
Rewrite `.agent/handoff.md` at C5 per docs/agents/handback_template.md: feature
and round, branch, base and commit SHAs, a changed-files table per commit, the
item-status table covering every commit and the push, one entry per gate with
its real result, the finding counts, and the next expected action. Carry the
`Fortschritt:` block above VERBATIM — count its lines yourself; no numeral is
stated here — and if any clause of it is false of the round that actually
happened, carry the ordered bytes UNCHANGED and write the correction BESIDE
them. Give the item-status table and the finding counts their own headings,
named as the template names them. EVERY NUMERAL YOUR HANDBACK STATES ABOUT A
LIST IS COUNTED MECHANICALLY BEFORE YOU COMMIT IT, or the list is named and NO
numeral is given (R-0441). Any finding count carries the RULE and the COMMIT it
was measured at (F009 D10).

THE HANDBACK LINE CAP: this block states no cap and no tier. Resolve it from
AGENTS.md under `### handoff.md` against the commit count constraint 3 fixes,
and report BOTH that count and the tier.

YOUR `## Next` SECTION STATES NO VERDICT, NO COLOUR AND NO PASS for this round:
the reviewer has not read the diff when you write it, and a handback that
predicts its own gate is finding R-0583's second instance, which R35 recorded.
Name instead, in order: that the next session reads `.agent/STOP` from disk as
Phase 1 rule 1 BEFORE the Open PR Gate as rule 2; that R36's verdict is NOT YET
on disk and the next reviewed round records it as the `Gate: F031 R36` entry;
and that R37 is the component round — the token threaded from `RemedyApp`'s
`readUrlState` through `RemedyShell` and `RightLivePanel`, the flow called on a
click, its sentence rendered and the buttons enabled.

Declare every deviation, contradiction and assumption.
──────────────────────────────────────────────────────────────

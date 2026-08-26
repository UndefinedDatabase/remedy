── STEP R29 — F031 Decision inbox ────────────────────────────
Goal:        Record R28's PASS, then close the two defects the R28 gate found
             in the seam R28 itself shipped: a whitespace-only answer is
             built, sent and PERSISTED, since the server validates nothing and
             writes answers ONCE; and the job id sits beside the credential as
             a bare string, so a swap puts the TOKEN IN THE URL PATH.

Fortschritt: ~94 % (F031 claimed; R1 through R28 landed, R28 gated here ·
             T001 SHIPPED · T002 COMPLETE · T003 answer command, deep-link
             and request seams shipped and now hardened, wiring open)
             — Schaetzung

Bundle:      C0a save this block · C0b mirror it into last_block · C1 the
             plan · C2 the R28 gate entry and the registrations of R-0684 and
             R-0685 · C3 the trim refusal, the credential pair, their tests,
             the two stale sentences and DECISION F031 D14 · C4 handback.

Change set:  exactly these paths, nothing else —
             .agent/authored/f031-r29.md                             (C0a)
             .agent/last_block.md                                    (C0b)
             .agent/plan.md                                          (C1)
             .agent/live_review.md                                   (C2)
             apps/ui/src/api/decisionAnswer.ts                       (C3)
             apps/ui/src/api/decisionAnswer.test.ts                  (C3)
             apps/ui/src/api/decisionSend.ts                         (C3)
             apps/ui/src/api/decisionSend.test.ts                    (C3)
             .agent/decisions.md                               (C3, D14)
             .agent/handoff.md                                       (C4)
             This list bounds the round's WRITES, not its ACTIONS: the push
             named in G9 is ordered explicitly and is not a file (R-0674).

── Base ──────────────────────────────────────────────────────
The round base is `26327a43fcbe2400203c44f750c3e2ffa43fcfd6`, the R28 handback
commit and the tip of `feature/f031-decision-inbox`, local and remote EQUAL —
the reviewer measured both at the R28 gate. Stay on that branch; never commit
to `main`. Every SHA-shaped token here resolved under `git cat-file -t`.

Readings the reviewer MEASURED at that base, re-checkable there:
- `.agent/live_review.md` 717469 bytes and 1263 lines; `^- R-\d+ — ` 244 all
  DISTINCT, maximum `R-0683`; `^Done: R-\d+ — ` 5, so the §3 item 10 open set
  is 239; `^Recurrence: R-` 22; `^Landed: R-` 0. THE GATE SERIES IS SPLIT by
  DECISION F031 D7: `^Gate: R\d+ — ` 19, frozen, and `^Gate: F\d+ R\d+ — ` 9,
  those nine being `F031 R19` through `F031 R27`. THIS ROUND MINTS TWO IDS,
  which is why constraint 10 differs from the last three rounds'.
- `.agent/plan.md` 46 lines, 2799 bytes. `docs/roadmap/**` is UNTOUCHED, so
  the §3 docs-round gate is not earned and is not ordered.
- `apps/ui`: `npm run typecheck` exit 0, zero diagnostics on stdout and
  stderr; `npm run test:unit` exit 0 at 26 files and 395 tests, of which
  `decisionCard.test.ts` is 36, `decisionAnswer.test.ts` 17,
  `decisionFilter.test.ts` 20, `decisionOrder.test.ts` 16,
  `decisionFocus.test.ts` 7 and `decisionSend.test.ts` 10.
- The six Python suites all exit 0; their counts are stated ONCE, in G7.
- WHY THE TRIM IS A REAL DEFECT AND NOT A TIDY-UP: the reviewer traced the
  whole path at `26327a43`, and that three-step measurement is stated ONCE,
  in LEDGER29's `- R-0685` paragraph, which this Base deliberately does not
  restate. READ IT BEFORE WRITING S1 — it is why the refusal is ordered.
- THE SERVER IS NOT THE AUTHORITY HERE, WHICH MAKES TWO SENTENCES STALE.
  `decisionAnswer.ts` at that base calls each refusal "a SECOND copy of a
  rule `packages/orchestration/ui_server.py` already enforces" and returns
  null "for the four bodies that door would refuse anyway" — but the
  empty-answer refusal has NO server counterpart, and S1 adds a second that
  is the browser's ALONE. S3 repairs both AT THEIR SOURCE.
- `decisionSend.ts` carries the same staleness by reference — "the four
  bodies `buildDecisionResolveCommand` already refuses" — and it is in this
  change set for S2 anyway. S3 repairs it too.
- THE OTHER ADJACENT PAIR NEEDS NO FIX, stated so you do not widen the
  change. Swapping `answerText` with `clientNonce` already fails LOUDLY: a
  prose answer cannot match `COMMAND_NONCE_PATTERN`, so the builder answers
  null. Only the job id and the credential swap silently — S2 fixes that pair
  and nothing else.
- THE ABSENCE SWEEP, run per R-0377's recurrence, over files OUTSIDE this
  change set: `decisionCard.ts` says "nothing in this browser posts that
  body", and this round still adds no `fetch`, so it stays TRUE. `docs/`
  mentions `decision.resolve` only as the SERVER's command id, which this
  round does not touch.
- THIS BLOCK'S OWN TWO CAPS, measured on its final bytes before emission and
  stated so your re-measurement can disagree with the reviewer's, are 490
  lines TOTAL (DECISION F085 D6) and 400 lines PROSE (DECISION F085 D5). G2
  orders you to report both from the COMMITTED blob.

── Constraints ───────────────────────────────────────────────
1. Apply every authored SLICE BYTE FOR BYTE. Never retype, rewrap or "fix"
   one. If a slice looks wrong, apply it verbatim and DECLARE the
   disagreement: a contradiction in this block is the reviewer's defect.
2. THE PRODUCTION CHANGE, ITS TESTS AND DECISION D14 ARE DESCRIBED, NOT
   SLICED. The numbered specification S1 through S4 fixes behaviour,
   structure and copy; YOU write that code, those tests and that decision
   entry under AGENTS.md's Mandatory Self-Review Loop and its File Editing
   Safety Rules. Where the spec is silent, prefer the idiom the neighbouring
   module already uses. Where the spec is WRONG, say so in the handback and
   do the right thing.
3. Slice transport. The reviewer's original is on disk at
   `.remedy-wt/f031-r29.md`. COPY that file to `.agent/authored/f031-r29.md`
   at C0a — never retype it — and mirror it byte-identically into
   `.agent/last_block.md` at C0b. THIS BLOCK STATES NO DIGEST OF ITSELF: a
   file cannot carry its own sha256, so the proof is the disk-to-disk
   comparison G1 orders over four readings, which is what
   docs/agents/self_drive_protocol.md substitutes for the hash-stamp ritual
   when there is no transport. Report the digest YOU measure. Extract every
   slice PROGRAMMATICALLY out of the COMMITTED C0a blob by its marker LINES —
   `<<<SLICE <NAME>` opens, `<<<END <NAME>` closes. Marker lines never reach a
   target file.
4. Commit sequence, exactly: C0a, C0b, C1, C2, C3, C4. No extra commit, none
   dropped, no reordering. C1 is FIRST substantive because this round writes
   the finding ledger (§3 item 23). To correct a landed commit, do NOT add one
   outside this sequence — declare it, and give it its own `## Commits` and
   item-status rows (R-0675).
5. Never amend, rebase, cherry-pick, force-push or rewrite history; never
   delete a branch; never merge; create no pull request.
6. `git status --porcelain` prints 0 lines after every commit. Read
   `.agent/STOP` from disk before C0a and again before C4; if present, finish
   the commit in hand, write the handback and stop. NEVER delete that
   sentinel (R-0347).
7. The slices this block carries are the whole text PLANF031R29 and the
   appended text LEDGER29. This paragraph names them and states no count; G2
   orders you to report the count YOUR extractor measured.
8. THE ONE APPEND'S SHAPE, STATED ONCE HERE, WITH EVERY GATE NAMING THIS
   PARAGRAPH RATHER THAN RESTATING IT. Under the newline-INCLUDED convention
   each slice already ends in a newline, so `.agent/live_review.md` after C2
   is EXACTLY: its blob at C1, then one newline, then LEDGER29 — and it
   receives NOTHING ELSE in that commit, and nothing at all in any other
   commit of this round (R-0657). LEDGER29's own paragraph count is yours to
   measure; this paragraph states no number. `.agent/decisions.md` also GROWS
   at C3, by text YOU author under S4, so no equality gate is ordered over it
   and none may be reported.
9. THIS BLOCK CARRIES NO FROM/TO PAIR, so no containment test is reported and
   no FROM-zero count is ordered (§3 item 15). The plan is a WHOLE-FILE
   replacement and LEDGER29 is an append.
10. THIS ROUND MINTS TWO FINDING IDS AND RESOLVES NONE — the first minting
    round in four, so read this constraint rather than reusing the last
    block's. LEDGER29 carries the two `- R-` registration paragraphs
    `R-0684` and `R-0685` and NO `Done:` line, so `^- R-\d+ — ` moves
    244 → 246 with the ids ADDED being EXACTLY that pair and the maximum
    becoming `R-0685`, while `^Done: R-\d+ — ` stays 5 and the §3 item 10
    open set moves 239 → 241. `^Recurrence: R-` stays 22 and `^Landed: R-`
    stays 0: WRITE NO `Landed:` LINE and no `Done:` line. No landed finding
    paragraph is edited (§3 item 20); the two stale SOURCE sentences S3
    repairs are not ledger text and are a different thing entirely.
11. TOUCH NO DOCUMENT AND NO OTHER CODE. Nothing under `docs/`, `packages/`
    or `tests/`, and neither `.agent/context.md` nor either
    `f031_*_inventory.md`. Inside `apps/` ONLY the four paths the change set
    names are written — NOT `decisionCard.ts`, `decisionFocus.ts`,
    `feedFocus.ts`, `remedyApi.ts`, `RemedyApp.tsx`, `RightLivePanel.tsx`,
    `DecisionInboxCard.tsx` or any other test file. THIS ROUND STILL WIRES
    NOTHING AND SENDS NOTHING: write no `fetch`, and edit no component.
12. Destructive verification runs ONLY in a disposable `git worktree` under
    `.remedy-wt/`, removed BY ITS EXACT PATH (R-0662) and before the G7
    suites. Everything already there is pre-existing scratch belonging to no
    commit, this block's own file included: create no worktree at an existing
    path, and delete nothing you did not create.

── Specification (S1–S4) — the production change ─────────────
S1  THE TRIM REFUSAL, in `apps/ui/src/api/decisionAnswer.ts`.
    `buildDecisionResolveCommand` TRIMS the answer text once, refuses when
    the TRIMMED text is empty — replacing the exact `=== ""` comparison, so
    `"   "` now answers `null` where it previously built a body — and sends
    the TRIMMED text as `args.answer`, never the raw one. Trim by the
    language's own `String.prototype.trim`; invent no character class.
    WHY BOTH HALVES: the refusal exists because the record is written ONCE
    and a blank answer cannot be corrected through this door, and the
    trimming exists because leading and trailing space in a durable,
    write-once record is noise no reader asked for. Put the one-line WHY
    comment directly above the refusal. Change NO other refusal, and change
    nothing about the nonce, the command id or the key spellings.

S2  THE CREDENTIAL PAIR, in `apps/ui/src/api/decisionSend.ts`.
    `buildDecisionSendRequest` currently takes `jobId` and `serverToken` as
    two ADJACENT bare `string` parameters, so transposing them at a call site
    type-checks and builds `/api/jobs/<the token>/commands` — the credential
    in the request PATH, which is the one thing this module's own comment
    says must never happen, and which its "token is not in the path" test
    cannot catch because that test passes the arguments in the right order.
    REPLACE THE TWO PARAMETERS WITH ONE OBJECT carrying both as named
    fields, so the transposition is not expressible; keep the remaining
    parameters and the return type as they are. Name the object for what it
    is — the addressed job and the credential that opens its door — and keep
    both empty-string refusals, now reading the object's fields.
    THIS IS AGENTS.md's Code Discoverability rule "use distinct ID/value
    types where an argument swap is plausible" applied at the cheapest
    moment: before the call site exists.

S3  THE TWO STALE SENTENCES, at their source, in the same two modules.
    In `decisionAnswer.ts`: the header's claim that every refusal is a second
    copy of a server-enforced rule is FALSE of the empty-answer refusal and
    now of S1's trim refusal too. Rewrite it to say which refusals MIRROR the
    server and that the blank-answer refusal is the browser's ALONE, naming
    WHY — the server validates nothing and writes once — while keeping the
    point that the server stays the authority for those that DO mirror it.
    Also retire "the four bodies that door would refuse anyway" from that
    module's opening comment: NAME the refused set instead of counting it, so
    it cannot go stale again the next time one is added (§3 item 16). In
    `decisionSend.ts` the same count reappears as "the four bodies
    `buildDecisionResolveCommand` already refuses" — treat it the same way.
    State no numeral for either set.

S4  DECISION F031 D14, appended to `.agent/decisions.md` in the shape D1
    through D13 already use there. CHOSEN: the browser refuses a
    whitespace-only answer although the server accepts one, which is a
    DELIBERATE divergence rather than a mirror, because
    `answer_task_decision` validates nothing and answers are written once —
    so the only place a blank answer can still be stopped is before it is
    sent. CHOSEN: the answer is trimmed before it is sent, so the durable
    record carries no incidental whitespace. CHOSEN: the send builder takes
    the job id and the server token as ONE named object, because two
    adjacent bare strings make a swap type-check and put the credential in
    the URL path. ALTERNATIVE: adding the validation to the server instead,
    rejected for THIS round because F031's change set is the browser and the
    write door is F009's — record it as the better long-term home and route
    it to that feature rather than doing it here. ALTERNATIVE: branded string
    types for every id in this seam, rejected as more machinery than one
    swappable pair earns. REVERSE the divergence by deleting the trim
    refusal, and the object by inlining its two fields.

── Authored slices ───────────────────────────────────────────

<<<SLICE PLANF031R29
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1–D14.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R29 records R28's PASS and hardens the seam R28 shipped: a whitespace-only
answer is refused rather than persisted into a write-once record, the answer is
trimmed, and the send builder's job id and credential become one named object
so a swapped call site cannot put the token in the URL path.

## Next Steps
1. T003's WIRING round, which needs no ruling: thread the job id and the token
   from `RemedyApp`'s `readUrlState` through the shell to the inbox card, mint
   the nonce, issue the request, and wire the resolver R27 shipped. That round
   owns the only `fetch` in this seam and the only component edits.
2. The clarification FORM itself, and the ruling on `NeedsAttentionCard`'s
   decision branch (DECISION F031 D4).
3. The integration-gate round per `docs/agents/integration_gate.md`, whose
   block also carries the §3 checklist items R-0683, R-0377, R-0419 and R-0429
   route there, then closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- NOTHING CALLS THE REQUEST BUILDER OR THE RESOLVER YET. That is deliberate
  under DECISION F031 D5 — the seam ships tested, the wiring follows — but it
  means `tsc` and review, not a test, are what will catch a mis-wired call site.
- THE SERVER STILL ACCEPTS A BLANK ANSWER AND WRITES IT ONCE. R29 stops it in
  the browser only; DECISION F031 D14 routes the server-side validation to
  F009, which owns the write door, and it is NOT fixed here.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 239 at `26327a43` and this round MINTS TWO, R-0684 and R-0685, taking
  it to 241 and resolving none.
- The findings THIS FEATURE MUST STILL ACT ON are R-0377, R-0403, R-0413,
  R-0419, R-0429, R-0431, R-0441, R-0445, R-0471, R-0495, R-0533, R-0574,
  R-0593, R-0601, R-0622, R-0625, R-0632, R-0672, R-0674, R-0675, R-0676,
  R-0677, R-0678, R-0679, R-0683, R-0684 and R-0685; R-0495 and R-0574 are the
  two Highs.
- BLOCK CAPS ARE TWO, not one: 490 lines TOTAL (DECISION F085 D6) and 400 lines
  PROSE (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R29

<<<SLICE LEDGER29
Gate: F031 R28 — the F031 R28 entry. R28 PASSED ON EVERY ONE OF ITS NINE GATES, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk rather than reading the handback back; every value that handback states reproduced cell for cell. TRANSPORT HELD IN ITS STRONGEST FORM, and for this round the chain is complete end to end: the reviewer's own scratchpad original `.remedy-wt/f031-r28.md`, the C0a blob committed at `f211909b`, the C0b blob committed at `5cbe934a` and `.agent/last_block.md` read off disk at `26327a43` are ALL FOUR byte-identical at sha256 `2688e6ad3c9880d0122a4e69ae214a543be1a841894be2ebc8baae00c2d1120f` over 42098 bytes and 451 lines, C0a and C0b resolving to the SAME git blob `1b854b72175b17bf72e9cd4db6803d3d8c72db9f`, and that digest is the one the reviewer measured on its own bytes BEFORE emission — so the block that was authored and the block that was applied are provably the same artifact. THE EXTRACTION printed 2 slices, 51 content lines and 451 total, so PROSE was 400 EXACTLY, at the 400-line cap DECISION F085 D5 sets rather than over it, and TOTAL 451 against the 490 DECISION F085 D6 sets; the worker flagged the zero headroom unprompted, which is the right instinct and is why the next block was cut with margin. THE PLAN at `29b4c13c` equals PLANF031R28 exactly at 2799 bytes and 46 lines, with the trailing-newline-removed control FALSE, `^## Goal$` 1 and `^## Next Steps$` 1, and 46 strictly under the 50 AGENTS.md sets. THE C2 APPEND SATISFIED WHOLE-FILE EQUALITY: `.agent/live_review.md` at `1598aa92` is its C1 blob plus one newline plus LEDGER28, at 705142 + 1 + 12326 = 717469 against an actual 717469, and the SECOND, INDEPENDENT READER AGREED — a blank-line split moves the unit count 315 to 318 and its last 3 units equal that slice's 3 paragraphs IN ORDER, trailing newlines rstripped on BOTH sides. THE NEGATIVE CONTROL WAS RUN IN MEMORY, never on the tracked file: one byte flipped at offset 711306, inside the appended text, and both readers REJECT the mutant while both ACCEPT the true file. THE SETS MOVED EXACTLY WHERE THAT BLOCK'S CONSTRAINT 10 ALLOWED AND NOWHERE ELSE: `^- R-\d+ — ` 244 to 244 with the ids ADDED and the ids REMOVED BOTH the EMPTY SET and all 244 DISTINCT, maximum `R-0683` unmoved; `^Done: R-\d+ — ` 5 to 5 with the ids ADDED the EMPTY SET; `^Landed: R-` 0 to 0; `^Recurrence: R-` 20 to 22, with `^Recurrence: R-0419` and `^Recurrence: R-0429` each 0 to 1; `^Gate: R\d+ — ` 19 to 19 frozen and `^Gate: F\d+ R\d+ — ` 8 to 9, the added key exactly `F031 R27`, all keys DISTINCT. The §3 item 10 open set is 239 at `1598aa92`, and `- R-0419 — ` and `- R-0429 — ` each still occur exactly ONCE line-anchored, so neither landed paragraph was edited when its recurrence was appended. THE RED PROOF IS THE REVIEWER'S OWN, run in a disposable worktree at `f22c95f5` created at a path that did not exist and removed BY THAT EXACT PATH, with `git worktree list` 1 line and `git status --porcelain` 0 after: UNMUTATED the run gives REAL exit 0 at 23 files and 370 tests, and with the single line setting the `X-Remedy-CSRF` header DELETED — 36 bytes, counted exactly ONCE in that file before the deletion, per §3 item 25 — the run goes REAL exit 1 at 2 failed and 368 passed, the two being `carries the token in BOTH token headers, as ONE secret per DECISION F009 D11` and `puts the Bearer scheme on the authorization header ONLY`, which is cell for cell what that handback reports; the file was restored byte-identically inside the worktree before removal. THE SUITES ARE THE REVIEWER'S OWN, run SERIALLY, never two alive at once, every one a REAL exit 0: `npm run typecheck` with zero diagnostics on stdout and stderr, `npm run test:unit` at 26 files and 395 tests — one file and 10 tests more than the base, that file being `decisionSend.test.ts` — with `decisionAnswer.test.ts` 17, `decisionCard.test.ts` 36, `decisionFilter.test.ts` 20, `decisionOrder.test.ts` 16 and `decisionFocus.test.ts` 7 ALL UNMOVED; then `tests/ui_server/` 480, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16, `tests/ui_contracts/` 525 passed with 4 skipped and the canary `test_golden_path` 42, every count identical to the base reading. THE PRODUCTION CHANGE IS WHAT S1 THROUGH S3 ORDERED: `decisionSend.ts` composes `buildDecisionResolveCommand` and `jobCommandsPath` imported from `./decisionAnswer` and re-derives neither, carries `Authorization` once and `X-Remedy-CSRF` once with the SAME token in both per DECISION F009 D11, and holds `fetch(`, `XMLHttpRequest`, `Date.now`, `Math.random` and `useState` ZERO times each — which is what PURE means here and is what keeps the deliberate-absence sentences in `decisionCard.ts` and `decisionAnswer.ts` TRUE, both verified still present and both files untouched by this round. DECISION F031 D13 landed with its citations correct. HYGIENE HELD: line-anchored `^<<<SLICE ` and `^<<<END ` are 0 in `.agent/plan.md` at `29b4c13c`, `.agent/live_review.md` at `1598aa92` and all three files C3 writes, against a CONTROL of 2 and 2 over the C0a blob; the range `b6ae6f99`..`f22c95f5` names 7 paths, none under `docs/`, `packages/` or `tests/` and none of the forbidden set, with range-minus-change-set EMPTY and change-set-minus-range exactly `.agent/handoff.md`; the six commits `f211909b` through `26327a43` are each SINGLE-PARENT with insertions 451, 243, 19, 6, 234 and 157 read from `git diff --numstat`, each under the 500 cap AGENTS.md DECISION F104 D1 sets, and those numbers agree cell for cell with the `+/-` column of that handback's `## Commits` table; `git ls-files .remedy-wt` 0, the zip glob 0, `git worktree list` 1 line and `git status --porcelain` 0. THE BLOCK'S OWN OBJECT IDS RESOLVE: 24 SHA-shaped occurrences, 10 distinct, 9 `commit` and 1 `blob`, failing set EMPTY. THE REFLOG, scoped by the worker to the 5 entries C0a through C3 — correctly, since §3 item 31 puts every gate strictly earlier than C4 — reads `commit` throughout, so `amend`, `rebase` and `cherry` are 0 each. THE PUSH DISCHARGED: `refs/heads/feature/f031-decision-inbox` on the remote and the local tip are both `26327a43fcbe2400203c44f750c3e2ffa43fcfd6`, no pull request was created, no branch deleted and nothing merged. THE HANDBACK'S OVERAGE IS DECLARED AND PERMITTED: 198 lines against the 100-line tier its 6 commits earn, carrying the DECISION D15 stated-cause line that names that count as a numeral, with no section dropped; it is R-0582's curve again and that finding stays OPEN to carry it. THE SEVEN DECLARED ITEMS ARE ADJUDICATED AND NONE IS A DEFECT. Items 1, 6 and 7 are the block being obeyed. Item 2 is the cap rule being followed. Item 3, the reflog scoped to 5 rather than 6, is CORRECT and better than the alternative, for the §3 item 31 reason above. Item 4 is the honest reading of a gate that states no number, and the reviewer's own run reproduced both names. Item 5, checking the job id and token BEFORE calling the body builder, is behaviour-identical because all three paths answer `null`, and the spec fixed which inputs refuse rather than the order they are tested in. THE VERDICT IS PASS. TWO NEW FINDINGS ARE REGISTERED BESIDE THIS ENTRY, both raised by the reviewer against the code R28 shipped rather than against the round's conduct: R-0684 and R-0685.

- R-0684 — Medium, A CREDENTIAL AND AN ID SIT ADJACENT AS BARE STRINGS, SO THE SWAP THAT PUTS THE TOKEN IN THE URL PATH TYPE-CHECKS. Raised by the reviewer at the R28 gate against `apps/ui/src/api/decisionSend.ts` as committed at `f22c95f5`. THE MEASUREMENT: `buildDecisionSendRequest(jobId: string, serverToken: string, model, answerText: string, clientNonce: string)` takes the addressed job and the credential that opens its door as two ADJACENT parameters of the same type, both opaque identifiers with no structure to tell them apart. Transposing them at a call site is accepted by `tsc`, and the result is not a harmless 403: the first argument is spent by `jobCommandsPath`, so the request path becomes `/api/jobs/<the server token>/commands` and the per-run credential is written into the URL — the precise outcome this module's own header forbids in the sentence "never in the path and never in a query string, because a query string is the part of a URL that reaches logs". A path reaches exactly the same logs. WHY NO TEST CATCHES IT: `decisionSend.test.ts` does pin "keeps the token out of the path entirely", and that test passes its arguments in the CORRECT order, so it asserts a property of the module while the defect lives at the call site — and no call site exists yet, which is the only reason nothing is broken on disk today. THE WORKER IS NOT AT FAULT: the R28 block ordered the neighbouring module's idiom and `buildDecisionResolveCommand` is positional, so this is the reviewer's specification gap, found by reading the shipped signature against AGENTS.md's Code Discoverability rule "use distinct ID/value types where an argument swap is plausible (the branded-type/newtype pattern) so swaps become type errors" — a rule that is FORWARD-LOOKING and therefore binds this module, which is new code. WHY IT IS MEDIUM RATHER THAN LOW: the harm is a credential in a request path rather than a wrong answer, and the moment of maximum risk is the very next round, which writes the first call site. THE FIX, ordered by the block that registers this: the two parameters become ONE named object, so the transposition is not expressible. The neighbouring pair `answerText`/`clientNonce` is deliberately left alone — a swap there fails loudly against `COMMAND_NONCE_PATTERN` — because a rule applied where it buys nothing is churn.

- R-0685 — Medium, A WHITESPACE-ONLY ANSWER IS BUILT BY THE BROWSER, ACCEPTED BY THE SERVER AND WRITTEN ONCE, SO A DECISION CAN BE RESOLVED WITH NOTHING AND NEVER RE-ANSWERED. Raised by the reviewer at the R28 gate by tracing the whole path at `26327a43`, and carried as a RISK in `.agent/plan.md` for several rounds before anyone measured the far end of it. THE MEASUREMENT, in three steps. In `apps/ui/src/api/decisionAnswer.ts`, `buildDecisionResolveCommand` compares `answerText === ""` exactly, so `"   "` passes every refusal and a body is built. In `packages/orchestration/ui_server.py`, `_dispatch_decision_resolve` reads `args.get("answer")` and hands it to `answer_task_decision` with no check of its own; the door validates the command id, the nonce and the job, and nothing at all about the answer's content. In `packages/orchestration/escalation.py`, `answer_task_decision` writes `record["answer"] = str(answer)`, sets the status to answered and returns — it validates nothing — and its own docstring records that "answers are written once, so a late second answer cannot silently overwrite the one the run acted on", which is enforced by returning `None` for any record not OPEN. So a blank answer is accepted 200, persisted, and CANNOT be corrected through this door: the correction is answered 409. WHY IT IS NOT ALREADY A LIVE BUG: nothing can produce one today, because the answer affordances ship disabled and no clarification form exists — the defect is latent and the form round is exactly when it would go live, which is why it is registered now rather than after. WHY THE BROWSER IS THE RIGHT PLACE FOR THIS ROUND'S HALF: the server is F009's write door and F031's change set is the browser, so the block registering this orders the browser refusal and DECISION F031 D14 routes the server-side validation to F009 rather than reaching across a feature boundary to take it. THAT ROUTING IS THE FINDING'S OTHER HALF AND IS NOT DISCHARGED BY THE BROWSER FIX: a second client, the CLI included, would still write a blank answer. THIS ALSO FALSIFIES A SENTENCE IN THE SHIPPED MODULE, which is repaired at its source in the same round: `decisionAnswer.ts` claims every refusal it makes is "a SECOND copy of a rule `packages/orchestration/ui_server.py` already enforces", and the empty-answer refusal has no server counterpart at all.
<<<END LEDGER29

── Done when ─────────────────────────────────────────────────
Run every gate yourself, record its REAL exit code and REAL output, and report
ONE ENTRY PER GATE in the handback, as briefly as the ordered values allow and
with transcripts kept out (R-0582). "Green" as a word is a finding. Every gate
runs at a commit STRICTLY EARLIER than C4 (§3 item 31); G9's push follows it.

G1  Branch, cleanliness, transport. `git branch --show-current` prints
    `feature/f031-decision-inbox` and NOT `main`; `.agent/STOP` read from disk
    is ABSENT before C0a and again before C4; `git status --porcelain` line
    count after each of C0a, C0b, C1, C2 and C3 is 0. Then report sha256, byte
    count and line count for FOUR readings — `.remedy-wt/f031-r29.md` before
    C0a, the committed C0a blob, the committed C0b blob, and
    `.agent/last_block.md` off disk after C0b — ALL FOUR EQUAL, and the git
    blob id of C0a's and C0b's file, the SAME id.

G2  Extraction and the block's own two caps. Run your extractor over the
    COMMITTED C0a blob and report the slice count, the CONTENT lines inside
    markers, and the TOTAL — the numbers YOUR extractor printed — then PROSE
    as TOTAL minus CONTENT, against the two caps the Base names. If either is
    exceeded say so plainly and continue; it is the reviewer's to fix.

G3  The plan. `.agent/plan.md` at C1 is byte-equal to PLANF031R29 under your
    stated newline convention; report slice length, file length and
    convention. NEGATIVE CONTROL: NOT byte-equal to that slice MINUS its
    trailing newline. `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` STRICTLY
    under 50.

G4  The C2 append, as ONE equality over the whole file, in the shape
    constraint 8 states — name that paragraph, do not restate its formula.
    Report the boolean and the byte arithmetic against the C1 length you
    measure yourself. Report a SECOND, INDEPENDENT reading: split the
    committed file on blank lines, take the LAST N units, and confirm they
    equal LEDGER29's paragraphs IN ORDER, where N is the number YOUR split
    measured; give the unit count before and after, and STATE YOUR
    TRAILING-NEWLINE HANDLING, because a naive split reports FALSE on a
    byte-perfect file. This slice carries MORE THAN ONE paragraph, so ORDER is
    load-bearing and a set comparison does not discharge it. NEGATIVE CONTROL:
    flip ONE byte inside the appended text; BOTH readers must reject the
    mutant and BOTH accept the true file. Do that flip in memory or under a
    disposable worktree per constraint 12, never on the tracked file.

G5  The ledger sets, base versus C2 in `.agent/live_review.md`, in the shape
    constraint 10 states — report each side of every movement it names. THIS
    ROUND ADDS IDS, so report the ADDED set explicitly and that it is exactly
    `R-0684` and `R-0685`, that the REMOVED set is EMPTY, that all
    `^- R-\d+ — ` ids are DISTINCT, that the maximum is now `R-0685`, and that
    the `^Done: R-\d+ — ` ids ADDED are the EMPTY SET. `^Gate: R\d+ — `
    19 → 19 UNCHANGED, and `^Gate: F\d+ R\d+ — ` 9 → 10, the ADDED key being
    exactly `F031 R28`, all keys DISTINCT (§3 item 26). Report `^Recurrence:
    R-` 22 → 22 and `^Landed: R-` 0 → 0. Report the §3 item 10 open set at C2,
    and that `git diff --name-only` over C3 does NOT name
    `.agent/live_review.md` — the whole of constraint 8's "nothing at all in
    any other commit".

G6  THE RED PROOF, in a disposable worktree at C3 per constraint 12, so the
    primary checkout is never mutated, with vitest run from the PRIMARY
    checkout's `apps/ui` so the primary's `node_modules` resolves:
      npx vitest run --config <PRIMARY>/apps/ui/vitest.config.ts \
        --root <WORKTREE>/apps/ui src/api/
    Run it UNMUTATED first and report the file and test counts. Then, INSIDE
    THAT WORKTREE, in `apps/ui/src/api/decisionAnswer.ts`, REVERT S1's refusal
    to the exact-comparison form it replaced — that is, make the emptiness
    test read the answer text RAW instead of trimmed, leaving the trimming of
    the SENT value and every other byte alone, so the mutant is precisely the
    defect R-0685 describes and nothing else. FIRST count the exact bytes you
    are about to change IN THAT FILE and report the count, which MUST be 1
    (§3 item 25). Run the same line again. IT MUST GO RED. Report the REAL
    exit code, the NAMES of the failing tests, and the failure count YOUR run
    measured; this block states no number. A GREEN means S3's tests never
    distinguish a whitespace-only answer from an empty one, and is reported as
    such. Restore the file byte-identically, report that worktree's
    `git status --porcelain` as 0, remove the worktree BY ITS EXACT PATH and
    report `git worktree list` as 1 line after, naming that path.

G7  Structure, then the suites. Report, as counts YOU measured at C3: over
    `decisionAnswer.ts`, that `trim` occurs and that the literal `=== ""`
    tested against the RAW answer text is GONE — quote the refusal line — and
    that `fetch(` is still 0; over `decisionSend.ts`, that
    `buildDecisionSendRequest` takes the job id and the token as ONE object
    parameter — quote the signature — and that `fetch(`, `Date.now` and
    `useState` are each still 0. Report that the string `four bodies` occurs 0
    times across BOTH modules (§3 item 16, S3). Then in the PRIMARY checkout
    at the C3 tree, all REAL exit 0, run SERIALLY and never two alive at once,
    with `git worktree list` reported as 1 line immediately BEFORE the first
    of them. At `apps/ui`: `npm run typecheck` with ZERO diagnostics on stdout
    and stderr — this is the gate that proves S2's call-site change is
    complete, since the object parameter breaks every positional caller;
    `npm run test:unit`, reporting the file and test counts YOUR run measured
    — `decisionCard.test.ts` must still be exactly 36,
    `decisionFilter.test.ts` exactly 20, `decisionOrder.test.ts` exactly 16
    and `decisionFocus.test.ts` exactly 7, any movement in any of the four
    being a finding, while the FILE count must be exactly 26, UNCHANGED from
    the Base, because this round adds no test file; report
    `decisionAnswer.test.ts` and `decisionSend.test.ts` against the Base's 17
    and 10 and say how many each gained. Then in Python, by these exact
    command lines with no extra flag:
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/ui_contracts/ -q
      python3 -m pytest tests/cli/test_golden_path.py -q
    These are the four state readers a round rewriting `.agent/` state gates,
    plus `tests/ui_contracts/`, plus the canary. The reviewer ran all six at
    `26327a43` with these exact lines and measured in that order 480, 52, 21,
    16, 525 passed with 4 skipped, and 42, every one exit 0. Account for any
    difference.

G8  Markers, paths, commit shapes and object ids. Line-anchored `^<<<SLICE `
    and `^<<<END ` both 0 in `.agent/plan.md` at C1, `.agent/live_review.md`
    at C2 and every file C3 writes, against the same counts over the COMMITTED
    C0a blob as a CONTROL, where they are NOT 0. ONLY the line-anchored
    reading is ordered — this block quotes both markers inside backticks
    mid-line, so a raw SUBSTRING count is unmeetable and is NOT ordered.
    `git diff --name-only <base>..C3` names NO path under `docs/`, `packages/`
    or `tests/`, and none of `.agent/context.md`, either inventory file,
    `apps/ui/src/api/decisionCard.ts`, `apps/ui/src/api/decisionFocus.ts`,
    `apps/ui/src/api/feedFocus.ts`, `apps/ui/src/RemedyApp.tsx`,
    `apps/ui/src/components/panels/RightLivePanel.tsx`,
    `apps/ui/src/components/panels/DecisionInboxCard.tsx` or
    `apps/ui/src/api/remedyApi.ts`; the range path set MINUS the change set is
    EMPTY and the change set MINUS the range is exactly `.agent/handoff.md`,
    which C4 writes. Over C0a..C3 report per commit that it is single-parent
    and its INSERTION count — the `+` column only, per AGENTS.md DECISION F104
    D1 — each under 500; those same numbers fill the `+/-` column of the
    `## Commits` table, derived from `git diff --numstat` and NOT from
    `git commit`'s own summary, and you report that the two agree cell for
    cell (§3 item 28). Report `git ls-files .remedy-wt` as 0 and
    `git ls-files` over the zip glob as 0. FOR THE REFLOG state SCOPE and
    FIELD: over THIS ROUND'S entries only, by the OPERATION PREFIX before the
    first colon of `git reflog --format=%gs`, report `amend`, `rebase` and
    `cherry` each 0 and how many you scoped to. Finally extract every
    SHA-shaped token from the COMMITTED C0a blob with the word-bounded pattern
    matching 7 to 40 hex characters — whose boundaries do NOT match the
    64-char sha256 digest this block also carries — pass each to
    `git cat-file -t`, and report the token count YOUR extractor measured, the
    type per token, and the FAILING SET, which MUST BE EMPTY.

G9  The push. AFTER C4, run `git push origin feature/f031-decision-inbox`. No
    `--force`, no `--force-with-lease`, no history rewrite, no branch
    deletion, no pull request. THAT PUSH'S OUTCOME IS NOT A VALUE OF ANY FILE
    THIS ROUND WRITES: the reviewer measures the pushed tips at the next gate
    and records them in the R29 entry of `.agent/live_review.md`. In
    `## External actions` write the push COMMAND and that sentence. In the
    item-status table the push row is `done`, reason "ordered after C4;
    outcome carried by G9 to the reviewer". Report the real outcome in your
    final message.

── Handback ──────────────────────────────────────────────────
Rewrite `.agent/handoff.md` at C4 per docs/agents/handback_template.md:
feature and round, branch, base and commit SHAs, a changed-files table per
commit, the item-status table covering C0a through C4, S1 through S4 and the
push, one entry per gate with its real result, the finding counts, and the next
expected action. Carry the `Fortschritt:` block above VERBATIM — count its
lines yourself; no numeral is stated here.

EVERY NUMERAL YOUR HANDBACK STATES ABOUT A LIST IS COUNTED MECHANICALLY BEFORE
YOU COMMIT IT, or the list is named and NO numeral is given (R-0441). Any
finding count carries the RULE and the COMMIT it was measured at (F009 D10); a
narrower set is "the findings this feature must still act on".

THE HANDBACK LINE CAP: this block states no cap and no tier. Resolve it from
AGENTS.md under `### handoff.md` against the commit count constraint 4 fixes,
and report BOTH that count and the tier. If the MANDATED content does not fit,
exceed it and carry a DECISION D15 "Deviations, declared" line naming your
measured count as a NUMERAL (R-0430) and the content behind it. Never drop a
section to fit; claim no token cap. R-0582 is OPEN against the reviewer for
this pressure, so a declared overage is not a finding against you — but PREFER
BREVITY WHEREVER THE ORDERED VALUES ALLOW IT.

YOUR `## Next` SECTION names, in order: that the next session reads
`.agent/STOP` from disk as Phase 1 rule 1 BEFORE the Open PR Gate as rule 2;
that the R29 verdict is UNRECORDED and owed by the next round's ledger commit
(DECISION F085 D9); and that T003's WIRING round is next and owns the only
`fetch` and the only component edits in this seam.

Declare every deviation, contradiction and assumption.
──────────────────────────────────────────────────────────────

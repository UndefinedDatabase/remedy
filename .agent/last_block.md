── STEP R28 — F031 Decision inbox ────────────────────────────
Goal:        Record R27's PASS, RETIRE THE TOKEN BLOCKER — an unrun absence
             claim: the browser has held the server token since F008 and both
             write-door headers carry that ONE value — and ship
             `decisionSend.ts`, which turns a card plus an answer into the
             exact request that door accepts, still without issuing it.

Fortschritt: ~93 % (F031 claimed; R1 through R27 landed, R27 gated here ·
             T001 SHIPPED · T002 COMPLETE · T003 answer command and deep-link
             seam shipped, request seam here, wiring and forms open)
             — Schaetzung

Bundle:      C0a save this block · C0b mirror it into last_block · C1 the
             plan · C2 the R27 gate entry and the R-0419 and R-0429
             recurrences · C3 the request builder, its tests and DECISION
             F031 D13 · C4 handback.

Change set:  exactly these paths, nothing else —
             .agent/authored/f031-r28.md                             (C0a)
             .agent/last_block.md                                    (C0b)
             .agent/plan.md                                          (C1)
             .agent/live_review.md                                   (C2)
             apps/ui/src/api/decisionSend.ts                   (C3, NEW)
             apps/ui/src/api/decisionSend.test.ts              (C3, NEW)
             .agent/decisions.md                               (C3, D13)
             .agent/handoff.md                                       (C4)
             This list bounds the round's WRITES, not its ACTIONS: the push
             named in G9 is ordered explicitly and is not a file (R-0674).

── Base ──────────────────────────────────────────────────────
The round base is `b6ae6f9955a72cc9dd91d4b7a8742028e82f2b3a`, the R27 handback
commit and the tip of `feature/f031-decision-inbox`, local and remote EQUAL —
the reviewer measured both at the R27 gate. Stay on that branch; never commit
to `main`. Every SHA-shaped token here resolved under `git cat-file -t`.

Readings the reviewer MEASURED at that base, re-checkable there:
- `.agent/live_review.md` 705142 bytes and 1257 lines; `^- R-\d+ — ` 244 all
  DISTINCT, maximum `R-0683`; `^Done: R-\d+ — ` 5, so the §3 item 10 open set
  is 239; `^Recurrence: R-` 20; `^Landed: R-` 0. THE GATE SERIES IS SPLIT by
  DECISION F031 D7: `^Gate: R\d+ — ` 19, frozen, and `^Gate: F\d+ R\d+ — ` 8,
  those eight being `F031 R19` through `F031 R26`. `^Recurrence: R-0419` and
  `^Recurrence: R-0429` each occur 0 times: the two paragraphs LEDGER28
  appends are the first of their keys, and BOTH ids are OPEN at this base.
- `.agent/plan.md` 47 lines, 2781 bytes. `docs/roadmap/**` is UNTOUCHED, so
  the §3 docs-round gate is not earned and is not ordered.
- `apps/ui`: `npm run typecheck` exit 0, zero diagnostics on stdout and
  stderr; `npm run test:unit` exit 0 at 25 files and 385 tests, of which
  `decisionCard.test.ts` is 36, `decisionAnswer.test.ts` 17,
  `decisionFilter.test.ts` 20, `decisionOrder.test.ts` 16 and
  `decisionFocus.test.ts` 7.
- The six Python suites all exit 0; their counts are stated ONCE, in G7.
- THE TOKEN IS ALREADY IN THE BROWSER, which is why this round needs no
  operator ruling. At `b6ae6f99`: `apps/ui/src/RemedyApp.tsx` reads `token`
  out of `window.location.search` in `readUrlState` and REFUSES TO RENDER
  without it, and `apps/ui/src/api/remedyApi.ts` already spends that value on
  every read, building `token=` into `loadRemedyDashboard`'s query.
  `packages/orchestration/ui_server.py` mints it with
  `secrets.token_urlsafe(24)` and injects it into the served `index.html`.
- ONE SECRET OPENS BOTH HALVES OF THE WRITE DOOR. In that same server module
  `_bearer_token_accepted` and the `COMMAND_CSRF_HEADER` check BOTH call
  `server_token_matches(supplied, self.server_token)`, and the comment above
  `COMMAND_CSRF_HEADER` records DECISION F009 D11: the header "carries the
  server token itself", because there is no cookie to double-submit against.
  So `Authorization: Bearer <t>` and `X-Remedy-CSRF: <t>` take the SAME `<t>`.
- THE WRITE DOOR READS NO QUERY STRING AND NO CONTENT TYPE. Measured at
  `b6ae6f99`: `_handle_command_submission` authenticates from headers only,
  then reads `Content-Length` and parses JSON; every `Content-Type` in that
  module is on a RESPONSE. Send the header because the body IS JSON, ASSERT
  NOTHING about the server requiring it, and never put the token in a POST
  path — a query string is the part of a URL that lands in logs.
- THE BODY BUILDER ALREADY EXISTS and is why S1 invents no shape.
  `apps/ui/src/api/decisionAnswer.ts` exports `buildDecisionResolveCommand`,
  returning `DecisionResolveCommandBody | null` for four reasons, and
  `jobCommandsPath(jobId)`, a PATH with no host and no query. S1 composes
  those two; it re-derives neither.
- THE ABSENCE SWEEP, run because R-0377's recurrence asks for it. S1's module
  makes NO sentence false in a file outside this change set, and the reason
  is exactly S1's purity: at `b6ae6f99` `decisionCard.ts` says what is still
  absent is the SEND, "nothing in this browser posts that body", and
  `decisionAnswer.ts` says the sender round "owns that call". BOTH STAY TRUE,
  because this round still posts nothing — which is why G7's `fetch(`
  zero-count is a gate and not a nicety.
- THIS BLOCK'S OWN TWO CAPS, measured on its final bytes before emission and
  stated so your re-measurement can disagree with the reviewer's, are 490
  lines TOTAL (DECISION F085 D6) and 400 lines PROSE (DECISION F085 D5). G2
  orders you to report both from the COMMITTED blob.

── Constraints ───────────────────────────────────────────────
1. Apply every authored SLICE BYTE FOR BYTE. Never retype, rewrap or "fix"
   one. If a slice looks wrong, apply it verbatim and DECLARE the
   disagreement: a contradiction in this block is the reviewer's defect.
2. THE PRODUCTION CHANGE, ITS TESTS AND DECISION D13 ARE DESCRIBED, NOT
   SLICED. The numbered specification S1 through S3 fixes behaviour,
   structure and copy; YOU write that code, those tests and that decision
   entry under AGENTS.md's Mandatory Self-Review Loop and its File Editing
   Safety Rules. Where the spec is silent, prefer the idiom the neighbouring
   module already uses. Where the spec is WRONG, say so in the handback and
   do the right thing.
3. Slice transport. The reviewer's original is on disk at
   `.remedy-wt/f031-r28.md`. COPY that file to `.agent/authored/f031-r28.md`
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
7. The slices this block carries are the whole text PLANF031R28 and the
   appended text LEDGER28. This paragraph names them and states no count; G2
   orders you to report the count YOUR extractor measured.
8. THE ONE APPEND'S SHAPE, STATED ONCE HERE, WITH EVERY GATE NAMING THIS
   PARAGRAPH RATHER THAN RESTATING IT. Under the newline-INCLUDED convention
   each slice already ends in a newline, so `.agent/live_review.md` after C2
   is EXACTLY: its blob at C1, then one newline, then LEDGER28 — and it
   receives NOTHING ELSE in that commit, and nothing at all in any other
   commit of this round (R-0657). LEDGER28's own paragraph count is yours to
   measure; this paragraph states no number. `.agent/decisions.md` also GROWS
   at C3, by text YOU author under S3, so no equality gate is ordered over it
   and none may be reported.
9. THIS BLOCK CARRIES NO FROM/TO PAIR, so no containment test is reported and
   no FROM-zero count is ordered (§3 item 15). The plan is a WHOLE-FILE
   replacement and LEDGER28 is an append.
10. THIS ROUND MINTS NO FINDING ID AND RESOLVES NONE. LEDGER28 carries no
    `- R-` paragraph and no `Done:` line, so `^- R-\d+ — ` stays 244 with the
    maximum still `R-0683` and `^Done: R-\d+ — ` stays 5, leaving the §3 item
    10 open set UNCHANGED at 239. It carries two `Recurrence:` lines, so
    `^Recurrence: R-` moves 20 → 22. `^Landed: R-` stays 0: WRITE NO `Landed:`
    LINE, and write no `Done:` line either — R-0419 and R-0429 both stay OPEN
    on purpose, because this round widens their evidence rather than
    discharging them. No landed finding paragraph is edited (§3 item 20).
11. TOUCH NO DOCUMENT AND NO OTHER CODE. Nothing under `docs/`, `packages/`
    or `tests/`, and neither `.agent/context.md` nor either
    `f031_*_inventory.md`. Inside `apps/` ONLY the two NEW paths the change
    set names are written — NOT `decisionAnswer.ts`, `decisionCard.ts`,
    `decisionFocus.ts`, `feedFocus.ts`, `remedyApi.ts`, `RemedyApp.tsx`,
    `RightLivePanel.tsx`, `DecisionInboxCard.tsx` or any other test file.
    THIS ROUND WIRES NOTHING AND SENDS NOTHING: if you are editing a component
    to make the request reachable, or writing `fetch`, stop.
12. Destructive verification runs ONLY in a disposable `git worktree` under
    `.remedy-wt/`, removed BY ITS EXACT PATH (R-0662) and before the G7
    suites. Everything already there is pre-existing scratch belonging to no
    commit, this block's own file included: create no worktree at an existing
    path, and delete nothing you did not create.

── Specification (S1–S3) — the production change ─────────────
S1  THE REQUEST BUILDER, a NEW module `apps/ui/src/api/decisionSend.ts`,
    written as the sibling of `apps/ui/src/api/decisionAnswer.ts` and under
    the same rule: everything that can be a VALUE is one. It exports the shape
    of one HTTP request — path, method, headers and a body STRING — and ONE
    function building it from the job's identity and token, the card model,
    the answer text and a caller-supplied nonce.
    COMPOSE, DO NOT RE-DERIVE: the body is whatever
    `buildDecisionResolveCommand` returns, serialised with `JSON.stringify`,
    and the path is `jobCommandsPath(jobId)`, both imported from
    `./decisionAnswer`, so the four refusals stay defined in one place.
    THE ANSWER IS `null` WHENEVER THE REQUEST WOULD BE UNSENDABLE: when the
    body builder refuses, and additionally when the job id or the token is
    the empty string — a request with no credential is one the door answers
    403, refused here by the same "one round trip earlier" rule.
    THE HEADERS ARE THREE. `Authorization` carries `Bearer ` followed by the
    token; `X-Remedy-CSRF` carries THE SAME TOKEN, unmodified, per DECISION
    F009 D11; `Content-Type` is `application/json` because the body is JSON.
    Take the header NAMES from the server's own spelling. The token appears
    in NO other part of the request — not in the path, not in a query.
    THE WHY COMMENTS carry the deliberate absences, per AGENTS.md's Code
    Discoverability rules: this module opens no socket and calls no `fetch`,
    mints no nonce and reads no clock, and the caller owns the origin. Say
    that the two token headers are ONE secret rather than two, and name D11.

S2  THE TESTS, a NEW `apps/ui/src/api/decisionSend.test.ts`, following
    `decisionAnswer.test.ts`'s idiom. Build every model through
    `buildDecisionCardModel` so the tests pin the SEAM. Name each test for
    the property it pins, and cover at least: that a well-formed call yields
    the exact path, the `POST` method, and a body that JSON-parses back to
    the command `buildDecisionResolveCommand` builds; that BOTH token headers
    hold the token and that they hold the SAME string, which is D11's rule
    made executable; that the `Bearer ` prefix is present on the
    `Authorization` header ONLY; that the token appears NOWHERE in the path;
    that an empty token and an empty job id each answer `null`; and that a
    refusal from the body builder — use the not-open case, which
    `decisionAnswer.test.ts` already pins — propagates as `null` rather than
    a request with a `null` body.

S3  DECISION F031 D13, appended to `.agent/decisions.md` in the shape D1
    through D12 already use there. CHOSEN: the browser authenticates the
    write door with the SAME per-run server token it has held since F008 —
    `RemedyApp` reads it from the URL and will not render without it — so NO
    new secret, NO new endpoint and NO server change is required, and the
    "design ruling" the plan named as a blocker is ruled unnecessary.
    CHOSEN: `Authorization` and `X-Remedy-CSRF` carry that one value, because
    both server checks compare against `self.server_token` and DECISION F009
    D11 already rules that the CSRF header carries the server token itself.
    CHOSEN: the request is a VALUE built by a pure module and issued by its
    caller, per DECISION F031 D5. ALTERNATIVE: minting a second CSRF secret
    or adding a token endpoint, rejected because D11 already fixes the
    header's value and a second secret is a second thing to rotate for no
    gain. ALTERNATIVE: the token as a query parameter the way reads do,
    rejected because the write door reads headers only and a query string is
    the part of a URL that reaches logs. REVERSE it by changing this module's
    header map alone, should the server ever mint a distinct CSRF secret.

── Authored slices ───────────────────────────────────────────

<<<SLICE PLANF031R28
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1–D13.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R28 records R27's PASS, retires the token blocker as DECISION F031 D13 — the
browser has held the server token since F008 and both write-door headers carry
that one value — and ships `decisionSend.ts`, the pure request a sender issues.

## Next Steps
1. T003's WIRING round: thread the job id and the token from `RemedyApp`'s
   `readUrlState` through the shell to the inbox card, mint the nonce, issue
   the request R28 ships, and wire the resolver R27 ships. That round owns the
   only `fetch` in this seam, and it needs no ruling that is not already made.
2. T003's remainder: the clarification form — whose input must TRIM, since the
   builder refuses only the empty string — and the ruling on
   `NeedsAttentionCard`'s decision branch (DECISION F031 D4).
3. The integration-gate round per `docs/agents/integration_gate.md`, whose
   block also carries the §3 checklist items R-0683, R-0377, R-0419 and R-0429
   route there, then closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- NOTHING CALLS THE REQUEST BUILDER OR THE RESOLVER YET, exactly as nothing
  called `decisionInboxView` for a round. That is deliberate under DECISION
  F031 D5 — the seam ships tested, the wiring follows — but it means `tsc` and
  review, not a test, are what will catch a mis-wired call site.
- A WHITESPACE-ONLY ANSWER IS STILL BUILT, not refused: `decisionAnswer.ts`
  compares against the empty string exactly, so the form round owes the trim.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 239 at `b6ae6f99` and this round leaves it there, minting nothing and
  resolving nothing; R-0419 and R-0429 gain recurrences and stay OPEN.
- The findings THIS FEATURE MUST STILL ACT ON are R-0377, R-0403, R-0413,
  R-0419, R-0429, R-0431, R-0441, R-0445, R-0471, R-0495, R-0533, R-0574,
  R-0593, R-0601, R-0622, R-0625, R-0632, R-0672, R-0674, R-0675, R-0676,
  R-0677, R-0678, R-0679 and R-0683; R-0495 and R-0574 are the two Highs.
- BLOCK CAPS ARE TWO, not one: 490 lines TOTAL (DECISION F085 D6) and 400 lines
  PROSE (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R28

<<<SLICE LEDGER28
Gate: F031 R27 — the F031 R27 entry. R27 PASSED ON EVERY ONE OF ITS NINE GATES, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk rather than reading the handback back; every value that handback states reproduced cell for cell. TRANSPORT HELD IN ITS STRONGEST FORM, cmp-against-scratchpad rather than the digest fallback: the reviewer's own `.remedy-wt/f031-r27.md`, the C0a blob committed at `cdf40849`, the C0b blob committed at `ce374ca6` and `.agent/last_block.md` read off disk at `b6ae6f99` are ALL FOUR byte-identical at sha256 `3f31a05d2e5969ba0dfca086ef1255350fa326baad80041a623936ee10d82fda` over 38339 bytes and 449 lines, C0a and C0b resolving to the SAME git blob `b723f36ca5a27ba8b1ee76d27baf5f68d6c198d9`. THE EXTRACTION printed 2 slices, 50 content lines and 449 total, so PROSE was 399 against the 400-line cap DECISION F085 D5 sets and TOTAL 449 against the 490 DECISION F085 D6 sets. THE PLAN at `a81a04ae` equals PLANF031R27 exactly at 2781 bytes and 47 lines, with the trailing-newline-removed control FALSE, `^## Goal$` 1 and `^## Next Steps$` 1, and 47 strictly under the 50 AGENTS.md sets. THE C2 APPEND SATISFIED WHOLE-FILE EQUALITY: `.agent/live_review.md` at `7b601083` is its C1 blob plus one newline plus LEDGER27, at 696400 + 1 + 8741 = 705142 against an actual 705142, and the SECOND, INDEPENDENT READER AGREED — a blank-line split moves the unit count 313 to 315 and its last 2 units equal that slice's 2 paragraphs IN ORDER, trailing newlines rstripped on BOTH sides. THE NEGATIVE CONTROL WAS RUN IN MEMORY, never on the tracked file: one byte flipped at offset 696601, inside the appended text, and both readers REJECT the mutant while both ACCEPT the true file. THE SETS MOVED EXACTLY WHERE THAT BLOCK'S CONSTRAINT 10 ALLOWED AND NOWHERE ELSE: `^- R-\d+ — ` 244 to 244 with the ids ADDED and the ids REMOVED BOTH the EMPTY SET and all 244 DISTINCT, maximum `R-0683` unmoved; `^Done: R-\d+ — ` 5 to 5 with the ids ADDED the EMPTY SET; `^Landed: R-` 0 to 0; `^Recurrence: R-` 19 to 20 and `^Recurrence: R-0377` 0 to 1; `^Gate: R\d+ — ` 19 to 19 frozen and `^Gate: F\d+ R\d+ — ` 7 to 8, the added key exactly `F031 R26`, all keys DISTINCT. The §3 item 10 open set is 239 at `7b601083`, and `- R-0377 — ` still occurs exactly ONCE line-anchored, so its landed paragraph was not edited. THE RED PROOF IS THE REVIEWER'S OWN, run in a disposable worktree at `2e06cd62` created at a path that did not exist and removed BY THAT EXACT PATH, with `git worktree list` 1 line and `git status --porcelain` 0 after: UNMUTATED the run gives REAL exit 0 at 22 files and 360 tests, and with the resolver's single return of the matched task's `nodeId` — counted exactly ONCE in that file before the edit — changed to return the decision's own task id instead, the run goes REAL exit 1 at 3 failed and 357 passed, the three being `resolves a decision to the node of the task it is about`, `reads the task id rather than the decision's own id` and `answers the task's nodeId and never the task id it matched on`, which is cell for cell what that handback reports; the file was restored byte-identically inside the worktree before removal. THE SUITES ARE THE REVIEWER'S OWN, run SERIALLY, never two alive at once, every one a REAL exit 0: `npm run typecheck` with zero diagnostics on stdout and stderr, `npm run test:unit` at 25 files and 385 tests — one file and 11 tests more than the base, that file being `decisionFocus.test.ts` at 7 — with `decisionAnswer.test.ts` 17, `decisionFilter.test.ts` 20 and `decisionOrder.test.ts` 16 all UNMOVED and `decisionCard.test.ts` 36 against the base's 32, so S3(a) added exactly 4; then `tests/ui_server/` 480, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16, `tests/ui_contracts/` 525 passed with 4 skipped and the canary `test_golden_path` 42, every count identical to the base reading. THE PRODUCTION CHANGE IS WHAT S1 THROUGH S4 ORDERED: `decisionFocus.ts` imports `FocusableTask` from `./feedFocus` by the line `import type { FocusableTask } from "./feedFocus";` and declares no type of that name itself, with `fetch(`, `Date.now` and `useState` 0 each; `decisionCard.ts` no longer contains the string `absent everywhere is ANSWERING`, and `taskId` appears in the `DecisionCardModel` interface exactly once, projected through the total `cardText`, so a payload that is absent, is not an object, or carries a non-string `task_id` gives the empty string. HYGIENE HELD: line-anchored `^<<<SLICE ` and `^<<<END ` are 0 in `.agent/plan.md` at `a81a04ae`, `.agent/live_review.md` at `7b601083` and all five files C3 writes, against a CONTROL of 2 and 2 over the C0a blob; the range `beec7b83`..`2e06cd62` names 9 paths, none under `docs/`, `packages/` or `tests/` and none of the forbidden set, with range-minus-change-set EMPTY and change-set-minus-range exactly `.agent/handoff.md`; the six commits `cdf40849` through `b6ae6f99` are each SINGLE-PARENT with insertions 449, 245, 24, 4, 182 and 164 read from `git diff --numstat`, each under the 500 cap AGENTS.md DECISION F104 D1 sets, and those numbers agree cell for cell with the `+/-` column of that handback's `## Commits` table; `git ls-files .remedy-wt` 0, the zip glob 0, `git worktree list` 1 line and `git status --porcelain` 0. THE BLOCK'S OWN OBJECT IDS RESOLVE: 21 SHA-shaped occurrences, 10 distinct, 9 `commit` and 1 `blob`, failing set EMPTY. THE REFLOG, scoped to this round's 6 entries by the operation prefix before the first colon of `git reflog --format=%gs`, reads `commit` six times, so `amend`, `rebase` and `cherry` are 0 each. THE PUSH DISCHARGED: `refs/heads/feature/f031-decision-inbox` on the remote and the local tip are both `b6ae6f9955a72cc9dd91d4b7a8742028e82f2b3a`, no pull request was created, no branch deleted and nothing merged. THE HANDBACK'S OVERAGE IS DECLARED AND PERMITTED: 196 lines against the 100-line tier its 6 commits earn, carrying the DECISION D15 stated-cause line that names that count as a numeral and the mandated content behind it, with no section dropped — which AGENTS.md's `### handoff.md` allows explicitly and which is therefore NOT a finding against this round; it is R-0582's own growth curve, and that finding stays OPEN to carry it. THE SIX DECLARED ITEMS ARE ADJUDICATED. Items 1, 4 and 6 are the block being obeyed and the cap rule being followed, and are not deviations at all. ITEM 5 IS CORRECT: the block stated no failure number, so reporting three rather than comparing was the only honest reading, and the reviewer's own run reproduced all three names. ITEM 2 IS CORRECT AND IS AN IMPROVEMENT ON THE ORDER: giving the full-card fixture `task_id: "T-7"` makes that whole-model assertion pin a NON-EMPTY id, where minimal compliance would have made a test named "flattens a full card" assert that a full card has no task. ITEM 3 IS A REAL REVIEWER-BLOCK DEFECT, is the reviewer's own, and is the R-0429 recurrence appended beside this entry. THE VERDICT IS PASS.

Recurrence: R-0419 — SECOND INSTANCE, and the costliest so far: an unrun absence claim became a BLOCKER and stalled a round. MEASURED at `b6ae6f99`: `.agent/plan.md` rules that T003's sender round "needs a design ruling first: the browser holds NO bearer token and NO `X-Remedy-CSRF` value today, and how one reaches the page is a decision that spans the server and the shell", and `.agent/handoff.md` at that same commit repeats it as the round's closing instruction. BOTH CLAIMS ARE FALSE, and reading four files refutes them. `apps/ui/src/RemedyApp.tsx` takes `token` out of `window.location.search` in `readUrlState` and REFUSES TO RENDER without it, erroring "Missing job or token in the URL."; `apps/ui/src/api/remedyApi.ts` already spends that value on every dashboard read, building `token=` into its query; `packages/orchestration/ui_server.py` mints it with `secrets.token_urlsafe(24)` and injects it into the served `index.html`. The write door needs no OTHER secret: in that same server module `_bearer_token_accepted` and the `COMMAND_CSRF_HEADER` check BOTH call `server_token_matches(supplied, self.server_token)`, and the comment above that constant records DECISION F009 D11's ruling that the header "carries the server token itself" because there is no cookie to double-submit against. So the browser has held both header values since F008, and the ruling the plan was waiting for was a ruling about nothing. WHY THIS IS A RECURRENCE AND NOT A NEW ID, per §3 item 30: R-0419 is OPEN and its standing rule is precisely the rule broken here — "a block may state a repository-wide absence ... only after a repository-wide search, and the block names the search it ran. An absence claimed from a single file is an unrun claim." The reviewer read `decisionAnswer.ts`, whose header truthfully records that THAT module refuses to hold a token, and wrote one module's deliberate absence out as a property of the whole browser. WHAT THIS INSTANCE ADDS IS THE COST MODEL. R-0419's first instance carried a planning decision on a false reason, and the decision survived its bad reason; this one manufactured a phantom blocker that `.agent/plan.md`, `.agent/handoff.md` and a round-closing `## Next` all carried forward, and under docs/agents/self_drive_protocol.md guardrail G8 a blocker is a session-ending condition — so an unrun absence claim can now HALT the build rather than merely misexplain it, which is a different severity of harm from the same defect. The widened counter-measure owed to §3 is therefore: an absence claim that BLOCKS work is verified before it is written down, by naming the search and the files read, and no block may route a blocker to a future round on an unrun claim. THAT EDIT IS ROUTED TO THE INTEGRATION-GATE ROUND'S BLOCK, beside the items R-0683 and R-0377 already route there, so it does not become the finding body it is warning about. THE INSTANCE ITSELF IS REPAIRED BY THE ROUND THIS ENTRY'S BLOCK ORDERS: DECISION F031 D13 rules the token question, C1 removes the blocker from the plan, and S1 ships the request that spends the token — which is why R-0419 gains evidence here and is NOT resolved, the CLASS staying open until the checklist item lands.

Recurrence: R-0429 — SECOND INSTANCE, found by the WORKER while applying the R27 block and declared in its handback before the reviewer read the diff, exactly as the first instance was. MEASURED at `cdf40849`: that block's S3(a) orders the two whole-model `toEqual` assertions "at lines 164 and 188 of that file at the base commit" to be re-grepped before editing "because S1's own edit moves those line numbers (§3 item 9)", while the same block's S1 names `apps/ui/src/api/decisionCard.ts` as the file it edits and S3(a)'s own subject is `apps/ui/src/api/decisionCard.test.ts`. Those are two different files, so S1's edit could not have moved those numbers; the worker re-grepped as ordered, found both assertions still at 164 and 188, and said so. WHY THIS IS A RECURRENCE AND NOT A NEW ID, per §3 item 30: R-0429 is OPEN, is already headed CLAUSE-VS-CLAUSE, and already describes two clauses of one block, written by one reviewer in one file, that agree in TOPIC and disagree in a detail no linear read catches. WHAT THIS INSTANCE ADDS IS THE DETAIL TYPE. R-0429's standing rule reaches an ORDINAL — "a block clause that cites a numbered item of its own contract by ORDINAL is checked by counting into the contract list and reading back what that ordinal actually names" — and the detail that disagreed here is a FILE IDENTITY, which no ordinal check reads. The widened counter-measure owed to §3 is therefore: a clause giving a REASON that refers to another item of the same block resolves that reference before emission and names the file, the symbol or the item it actually points at. A false reason attached to a CORRECT instruction is invisible to every gate the block can order — the instruction is obeyed, the gate is green, and only a reader comparing two distant clauses can see it, which is why both instances were caught by the worker and neither by a gate. IT IS LOW, as the first instance was: the ordered action was right, the worker performed it, and nothing wrong reached disk. THAT EDIT IS ROUTED TO THE INTEGRATION-GATE ROUND'S BLOCK, and R-0429 stays OPEN until the checklist item lands.
<<<END LEDGER28

── Done when ─────────────────────────────────────────────────
Run every gate yourself, record its REAL exit code and REAL output, and report
ONE ENTRY PER GATE in the handback, as briefly as the ordered values allow and
with transcripts kept out (R-0582). "Green" as a word is a finding. Every gate
runs at a commit STRICTLY EARLIER than C4 (§3 item 31); G9's push follows it.

G1  Branch, cleanliness, transport. `git branch --show-current` prints
    `feature/f031-decision-inbox` and NOT `main`; `.agent/STOP` read from disk
    is ABSENT before C0a and again before C4; `git status --porcelain` line
    count after each of C0a, C0b, C1, C2 and C3 is 0. Then report sha256, byte
    count and line count for FOUR readings — `.remedy-wt/f031-r28.md` before
    C0a, the committed C0a blob, the committed C0b blob, and
    `.agent/last_block.md` off disk after C0b — ALL FOUR EQUAL, and the git
    blob id of C0a's and C0b's file, the SAME id.

G2  Extraction and the block's own two caps. Run your extractor over the
    COMMITTED C0a blob and report the slice count, the CONTENT lines inside
    markers, and the TOTAL — the numbers YOUR extractor printed — then PROSE
    as TOTAL minus CONTENT, against the two caps the Base names. If either is
    exceeded say so plainly and continue; it is the reviewer's to fix, not
    yours. The reviewer measured PROSE at 400 exactly, so a disagreement of
    even one line between your extractor and the reviewer's is worth stating.

G3  The plan. `.agent/plan.md` at C1 is byte-equal to PLANF031R28 under your
    stated newline convention; report slice length, file length and
    convention. NEGATIVE CONTROL: NOT byte-equal to that slice MINUS its
    trailing newline. `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` STRICTLY
    under 50.

G4  The C2 append, as ONE equality over the whole file, in the shape
    constraint 8 states — name that paragraph, do not restate its formula.
    Report the boolean and the byte arithmetic against the C1 length you
    measure yourself. Report a SECOND, INDEPENDENT reading: split the
    committed file on blank lines, take the LAST N units, and confirm they
    equal LEDGER28's paragraphs IN ORDER, where N is the number YOUR split
    measured; give the unit count before and after, and STATE YOUR
    TRAILING-NEWLINE HANDLING, because a naive split reports FALSE on a
    byte-perfect file. This slice carries MORE THAN ONE paragraph, so ORDER is
    load-bearing and a set comparison does not discharge it. NEGATIVE CONTROL: flip ONE byte inside
    the appended text; BOTH readers must reject the mutant and BOTH accept the
    true file. Do that flip in memory or under a disposable worktree per
    constraint 12, never on the tracked file.

G5  The ledger sets, base versus C2 in `.agent/live_review.md`, in the shape
    constraint 10 states — report each side of every movement it names, that
    the `- R-` ids ADDED and REMOVED are BOTH the EMPTY SET, that all
    `^- R-\d+ — ` ids are DISTINCT, and that the `^Done: R-\d+ — ` ids ADDED
    are ALSO the EMPTY SET. `^Gate: R\d+ — ` 19 → 19 UNCHANGED, and
    `^Gate: F\d+ R\d+ — ` 8 → 9, the ADDED key being exactly `F031 R27`, all
    keys DISTINCT (§3 item 26). Report `^Recurrence: R-` 20 → 22 and that
    `^Recurrence: R-0419` and `^Recurrence: R-0429` each move 0 → 1. Report
    the §3 item 10 open set at C2, that `- R-0419 — ` and `- R-0429 — ` each
    still occur exactly ONCE line-anchored so neither landed paragraph was
    edited, and that `git diff --name-only` over C3 does NOT name
    `.agent/live_review.md` — the whole of constraint 8's "nothing at all in
    any other commit".

G6  THE RED PROOF, in a disposable worktree at C3 per constraint 12, so the
    primary checkout is never mutated, with vitest run from the PRIMARY
    checkout's `apps/ui` so the primary's `node_modules` resolves:
      npx vitest run --config <PRIMARY>/apps/ui/vitest.config.ts \
        --root <WORKTREE>/apps/ui src/api/
    Run it UNMUTATED first and report the file and test counts. Then, INSIDE
    THAT WORKTREE, in `apps/ui/src/api/decisionSend.ts`, DELETE the single
    line that sets the `X-Remedy-CSRF` header — the omission a sender would
    most plausibly ship, since the bearer alone looks like authentication and
    `tsc` cannot tell a complete header map from an incomplete one. FIRST
    count the exact bytes you are about to delete IN THAT FILE and report the
    count, which MUST be 1 (§3 item 25); leave every other byte alone. Run the
    same line again. IT MUST GO RED. Report the REAL exit code, the NAMES of
    the failing tests, and the failure count YOUR run measured; this block
    states no number. A GREEN means S2's tests never pin the second header,
    and is reported as such. Restore the file byte-identically, report that
    worktree's `git status --porcelain` as 0, remove the worktree BY ITS EXACT
    PATH and report `git worktree list` as 1 line after, naming that path.

G7  Structure, then the suites. Report, as counts YOU measured at C3, over
    `decisionSend.ts`: that `fetch(`, `XMLHttpRequest`, `Date.now`,
    `Math.random` and `useState` each occur ZERO times — what PURE means here,
    and what keeps the deliberate-absence sentences in `decisionCard.ts` and
    `decisionAnswer.ts` TRUE per the Base's sweep; that
    `buildDecisionResolveCommand` and `jobCommandsPath` are both IMPORTED from
    `./decisionAnswer`, quoting the import line; and that the literals
    `Authorization` and `X-Remedy-CSRF` each occur exactly once.
    Then in the PRIMARY checkout at the C3 tree, all REAL exit 0, run SERIALLY
    and never two alive at once, with `git worktree list` reported as 1 line
    immediately BEFORE the first of them. At `apps/ui`: `npm run typecheck`
    with ZERO diagnostics on stdout and stderr; `npm run test:unit`, reporting
    the file and test counts YOUR run measured — `decisionAnswer.test.ts` must
    still be exactly 17, `decisionCard.test.ts` exactly 36,
    `decisionFilter.test.ts` exactly 20, `decisionOrder.test.ts` exactly 16
    and `decisionFocus.test.ts` exactly 7, any movement in any of the five
    being a finding, while the FILE count must be exactly 26, one more than
    the Base's 25, that one being `decisionSend.test.ts`; report that new
    file's own count. Then in Python, by these exact command lines with no
    extra flag:
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/ui_contracts/ -q
      python3 -m pytest tests/cli/test_golden_path.py -q
    These are the four state readers a round rewriting `.agent/` state gates,
    plus `tests/ui_contracts/`, plus the canary. The reviewer ran all six at
    `b6ae6f99` with these exact lines and measured in that order 480, 52, 21,
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
    `apps/ui/src/api/decisionAnswer.ts`, `apps/ui/src/api/decisionCard.ts`,
    `apps/ui/src/api/decisionFocus.ts`, `apps/ui/src/api/feedFocus.ts`,
    `apps/ui/src/RemedyApp.tsx`,
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
    and records them in the R28 entry of `.agent/live_review.md`. In
    `## External actions` write the push COMMAND and that sentence. In the
    item-status table the push row is `done`, reason "ordered after C4;
    outcome carried by G9 to the reviewer". Report the real outcome in your
    final message.

── Handback ──────────────────────────────────────────────────
Rewrite `.agent/handoff.md` at C4 per docs/agents/handback_template.md:
feature and round, branch, base and commit SHAs, a changed-files table per
commit, the item-status table covering C0a through C4, S1 through S3 and the
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
exactly this pressure, so a declared overage is not a finding against you, but
PREFER BREVITY WHEREVER THE ORDERED VALUES ALLOW IT.

YOUR `## Next` SECTION names, in order: that the next session reads
`.agent/STOP` from disk as Phase 1 rule 1 BEFORE the Open PR Gate as rule 2;
that the R28 verdict is UNRECORDED and owed by the next round's ledger commit
(DECISION F085 D9); and that T003's WIRING round is UNBLOCKED by DECISION D13.

Declare every deviation, contradiction and assumption.
──────────────────────────────────────────────────────────────

── STEP R31 — F031 Decision inbox ────────────────────────────
Goal:        Record R30's PASS and ship the ONE impure call this feature
             needs, as a module a test can still reach: `decisionSubmit.ts`
             posts the request `decisionSend.ts` builds and maps what comes
             back to a closed three-value result. Nothing calls it yet — the
             component wiring is R32's, exactly as the resolver and the
             request builder shipped tested before their callers.

Fortschritt: ~96 % (F031 claimed; R1 through R30 landed, R30 gated here ·
             T001 SHIPPED · T002 COMPLETE · T003 answer command, request and
             deep-link seams shipped and wired, submit seam here, click
             handler open) — Schaetzung

Bundle:      C0a save this block · C0b mirror it into last_block · C1 the
             plan · C2 the R30 gate entry and R-0560's recurrence · C3 the
             submit module, its tests and DECISION F031 D16 · C4 handback.

Change set:  exactly these paths, nothing else —
             .agent/authored/f031-r31.md                             (C0a)
             .agent/last_block.md                                    (C0b)
             .agent/plan.md                                          (C1)
             .agent/live_review.md                                   (C2)
             apps/ui/src/api/decisionSubmit.ts                 (C3, NEW)
             apps/ui/src/api/decisionSubmit.test.ts            (C3, NEW)
             .agent/decisions.md                               (C3, D16)
             .agent/handoff.md                                       (C4)
             This list bounds the round's WRITES, not its ACTIONS: the push
             named in G9 is ordered explicitly and is not a file (R-0674).

── Base ──────────────────────────────────────────────────────
The round base is `5ee3024b75af8fcb3015bd2e013510f597d545c3`, the R30 handback
commit and the tip of `feature/f031-decision-inbox`, local and remote EQUAL —
the reviewer measured both at the R30 gate. Stay on that branch; never commit
to `main`. Every SHA-shaped token here resolved under `git cat-file -t`.

Readings the reviewer MEASURED at that base, re-checkable there:
- `.agent/live_review.md` 736829 bytes and 1271 lines; `^- R-\d+ — ` 246 all
  DISTINCT, maximum `R-0685`; `^Done: R-\d+ — ` 5, so the §3 item 10 open set
  is 241; `^Recurrence: R-` 22; `^Landed: R-` 0. THE GATE SERIES IS SPLIT by
  DECISION F031 D7: `^Gate: R\d+ — ` 19, frozen, and `^Gate: F\d+ R\d+ — ` 11,
  those eleven being `F031 R19` through `F031 R29`. `^Recurrence: R-0560`
  occurs 0 times and `R-0560` is OPEN: the recurrence LEDGER31 appends is the
  first of its key. THIS ROUND MINTS NO ID.
- `.agent/plan.md` 48 lines, 2774 bytes. `docs/roadmap/**` is UNTOUCHED, so
  the §3 docs-round gate is not earned and is not ordered.
- `apps/ui`: `npm run typecheck` exit 0, zero diagnostics on stdout and
  stderr; `npm run test:unit` exit 0 at 26 files and 400 tests, of which
  `decisionSend.test.ts` is 12, `decisionAnswer.test.ts` 20,
  `decisionCard.test.ts` 36, `decisionFilter.test.ts` 20,
  `decisionOrder.test.ts` 16 and `decisionFocus.test.ts` 7.
- The six Python suites all exit 0; their counts are stated ONCE, in G7.
- THE REQUEST IS ALREADY A VALUE. `apps/ui/src/api/decisionSend.ts` exports
  `DecisionSendRequest` — `path`, `method`, `headers` and a body STRING — and
  `buildDecisionSendRequest`, which answers `null` for every unsendable case.
  S1 CONSUMES that value and re-derives none of it: it does not read a model,
  an answer or a nonce, and it never builds a path or a header.
- THE VITEST ENVIRONMENT IS `node`, collecting `src/**/*.test.ts` only, and
  the reviewer measured that NO test in `apps/ui/src` uses `vi.` or assigns
  `globalThis` — a global-patching idiom would be the first here. S1's
  injected parameter is why S2 needs none: the test passes its own function,
  so no global is touched and no two tests can leak into each other.
- WHAT THE SERVER ANSWERS, read at this base from
  `packages/orchestration/ui_server.py`, because S1's mapping must not invent
  statuses: 403 for a bad token AND for a bad CSRF header, 400 for a
  malformed body, 409 when the decision is absent or no longer open, 429 over
  the rate budget, 501 for an undispatched id, and 200 on success.
- THE ABSENCE SWEEP, run per R-0377's widened counter-measure over files
  OUTSIDE this change set. Three files say the SEND is still missing:
  `decisionCard.ts`, `decisionAnswer.ts` and `DecisionInboxCard.tsx`. All
  three STAY TRUE this round, because S1 ships a module with NO CALLER, so
  nothing posts. They become false in R32, which wires the click and edits
  all three anyway; the repair is DEFERRED to that round on purpose.
- THIS BLOCK'S OWN TWO CAPS, measured on its final bytes before emission and
  stated so your re-measurement can disagree with the reviewer's, are 490
  lines TOTAL (DECISION F085 D6) and 400 lines PROSE (DECISION F085 D5). G2
  orders you to report both from the COMMITTED blob.

── Constraints ───────────────────────────────────────────────
1. Apply every authored SLICE BYTE FOR BYTE. Never retype, rewrap or "fix"
   one. If a slice looks wrong, apply it verbatim and DECLARE the
   disagreement: a contradiction in this block is the reviewer's defect.
2. THE PRODUCTION CHANGE, ITS TESTS AND DECISION D16 ARE DESCRIBED, NOT
   SLICED. The numbered specification S1 through S3 fixes behaviour,
   structure and copy; YOU write that code, those tests and that decision
   entry under AGENTS.md's Mandatory Self-Review Loop and its File Editing
   Safety Rules. Where the spec is silent, prefer the idiom the neighbouring
   module already uses. Where the spec is WRONG, say so in the handback and
   do the right thing.
3. Slice transport. The reviewer's original is on disk at
   `.remedy-wt/f031-r31.md`. COPY that file to `.agent/authored/f031-r31.md`
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
7. The slices this block carries are the whole text PLANF031R31 and the
   appended text LEDGER31. This paragraph names them and states no count; G2
   orders you to report the count YOUR extractor measured.
8. THE ONE APPEND'S SHAPE, STATED ONCE HERE, WITH EVERY GATE NAMING THIS
   PARAGRAPH RATHER THAN RESTATING IT. Under the newline-INCLUDED convention
   each slice already ends in a newline, so `.agent/live_review.md` after C2
   is EXACTLY: its blob at C1, then one newline, then LEDGER31 — and it
   receives NOTHING ELSE in that commit, and nothing at all in any other
   commit of this round (R-0657). LEDGER31's own paragraph count is yours to
   measure; this paragraph states no number. `.agent/decisions.md` also GROWS
   at C3, by text YOU author under S3, so no equality gate is ordered over it
   and none may be reported.
9. THIS BLOCK CARRIES NO FROM/TO PAIR, so no containment test is reported and
   no FROM-zero count is ordered (§3 item 15). The plan is a WHOLE-FILE
   replacement and LEDGER31 is an append.
10. THIS ROUND MINTS NO FINDING ID AND RESOLVES NONE. LEDGER31 carries no
    `- R-` paragraph and no `Done:` line, so `^- R-\d+ — ` stays 246 with the
    maximum still `R-0685` and `^Done: R-\d+ — ` stays 5, leaving the §3 item
    10 open set UNCHANGED at 241. It carries ONE `Recurrence:` line, so
    `^Recurrence: R-` moves 22 → 23 and `^Recurrence: R-0560` moves 0 → 1.
    `^Landed: R-` stays 0: WRITE NO `Landed:` LINE, and no `Done:` line —
    R-0560 stays OPEN, because this round widens its evidence rather than
    discharging it. No landed finding paragraph is edited (§3 item 20).
11. TOUCH NO DOCUMENT AND NO OTHER CODE. Nothing under `docs/`, `packages/`
    or `tests/`, and neither `.agent/context.md` nor either
    `f031_*_inventory.md`. Inside `apps/` ONLY the two NEW paths the change
    set names are written — NOT `decisionSend.ts`, `decisionAnswer.ts`,
    `decisionCard.ts`, `decisionFocus.ts`, `remedyApi.ts`, `RemedyApp.tsx`,
    `RemedyShell.tsx`, `RightLivePanel.tsx`, `DecisionInboxCard.tsx`, any
    `.css` file, or any other test file. THIS ROUND WIRES NOTHING: if you
    find yourself editing a component to give the module a caller, or
    enabling the answer buttons, stop — that is R32's work.
12. Destructive verification runs ONLY in a disposable `git worktree` under
    `.remedy-wt/`, removed BY ITS EXACT PATH (R-0662) and before the G7
    suites. Everything already there is pre-existing scratch belonging to no
    commit, this block's own file included: create no worktree at an existing
    path, and delete nothing you did not create.

── Specification (S1–S3) — the production change ─────────────
S1  THE SUBMIT, a NEW module `apps/ui/src/api/decisionSubmit.ts`. It exports
    the RESULT type and ONE async function that sends a `DecisionSendRequest`
    — imported as a TYPE from `./decisionSend` — and answers that result. It
    is the ONLY place in this feature that touches the network.
    THE RESULT IS A CLOSED VOCABULARY, not a `Response`. Three outcomes and
    nothing else: the door ACCEPTED it, REFUSED it, or could not be REACHED.
    Carry the numeric status beside the outcome so a card can say WHICH
    refusal — 403 a credential, 409 a decision already answered or closed,
    429 the rate budget — with status 0 when unreachable, no response
    existing. Name the outcomes as a union of string literals, never
    booleans, so a fourth can be added without changing arity.
    IT NEVER THROWS AND NEVER RETRIES. A rejected send — offline, refused
    connection, aborted — becomes the unreachable result, because a promise
    that rejects inside a click handler is an unhandled rejection and a card
    that renders nothing. One attempt only: deciding when a retry is safe is
    not this module's call.
    THE SEND FUNCTION IS A PARAMETER with a default, and that is the whole
    testing seam: declare a NARROW local type naming only what this module
    reads back — a boolean for success and a numeric status — rather than
    depending on the DOM `Response`, and default it to the global `fetch`. A
    test then passes its own function and never touches a global. Pass the
    request's own `path`, `method`, `headers` and `body` through unchanged;
    add no header, no credential and no query.
    THE WHY COMMENTS carry the deliberate absences: no retry, no timeout, no
    nonce minting, no clock, and no knowledge of what a decision IS.

S2  THE TESTS, a NEW `apps/ui/src/api/decisionSubmit.test.ts`, following
    `decisionSend.test.ts`'s idiom. Build the request through
    `buildDecisionSendRequest` rather than by hand, so the tests pin the SEAM
    between the builder and the sender; a helper that returns a well-formed
    request keeps each test about one thing. Pass a stub send function and
    assert AT LEAST: that it is called exactly ONCE, and with the request's
    own path, method, headers and body unchanged; that a 200 answers
    accepted; that a 403 and a 409 each answer refused CARRYING that status,
    which is what lets a card tell a credential problem from a stale
    decision; that a rejected promise answers unreachable with status 0 and
    that the call does NOT reject; and that the failing cases still call the
    send function exactly once, which is what "no retry" means. Name each
    test for the property it pins. Touch no global.

S3  DECISION F031 D16, appended to `.agent/decisions.md` in the shape D1
    through D15 already use there. CHOSEN: the one network call in F031 lives
    in its own module and takes its send function as a defaulted parameter,
    so the impure edge is still reachable by the shipped vitest config —
    which is DECISION F031 D5's rule followed to its last step rather than
    abandoned at the wire. CHOSEN: the module answers a closed three-value
    outcome plus a numeric status instead of a `Response`, so no caller can
    read a body this feature has no use for, and a card can distinguish a
    credential refusal from a stale decision. CHOSEN: one attempt, never a
    retry, and never a throw. ALTERNATIVE: calling `fetch` directly in the
    component, rejected because nothing in the shipped test config reaches a
    component, so the mapping from status to meaning would ship untested.
    ALTERNATIVE: patching the global `fetch` in tests, rejected because no
    test in `apps/ui/src` does that today and a leaked global is a failure
    that shows up in an unrelated file. REVERSE it by inlining the module at
    its single call site.

── Authored slices ───────────────────────────────────────────

<<<SLICE PLANF031R31
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1–D16.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R31 records R30's PASS and ships `decisionSubmit.ts`, the ONE impure call this
feature needs: it posts the request `decisionSend.ts` builds and maps the answer
to a closed three-value outcome. It has no caller yet; R32 wires the click.

## Next Steps
1. R32, T003's LAST wiring round: thread the server token from `RemedyApp`'s
   `readUrlState` to the card, mint the nonce, call the submit module on an
   answer click, enable the disabled buttons, and retire the three "nothing
   posts yet" sentences in `decisionCard.ts`, `decisionAnswer.ts` and
   `DecisionInboxCard.tsx` — that round is the first to falsify them.
2. The clarification FORM, and the ruling on `NeedsAttentionCard`'s decision
   branch (DECISION F031 D4).
3. The integration-gate round per `docs/agents/integration_gate.md`, whose
   block also carries the §3 checklist items R-0683, R-0377, R-0419, R-0429
   and R-0560 route there, then closure per
   `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- NOTHING CALLS THE SUBMIT MODULE YET, as nothing called the resolver or the
  request builder for a round. Deliberate under DECISION F031 D5 — the seam
  ships tested, the wiring follows — but `tsc` and review, not a test, are
  what will catch a mis-wired call site in R32.
- THE SERVER STILL ACCEPTS A BLANK ANSWER AND WRITES IT ONCE. R29 stopped it
  in the browser only; DECISION F031 D14 routes the server-side check to F009,
  which owns the write door, and it is NOT fixed here.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 241 at `5ee3024b` and this round leaves it there, minting nothing and
  resolving nothing; R-0560 gains a recurrence and stays OPEN.
- The findings THIS FEATURE MUST STILL ACT ON are R-0377, R-0403, R-0413,
  R-0419, R-0429, R-0431, R-0441, R-0445, R-0471, R-0495, R-0533, R-0560,
  R-0574, R-0593, R-0601, R-0622, R-0625, R-0632, R-0672, R-0674, R-0675,
  R-0676, R-0677, R-0678, R-0679, R-0683, R-0684 and R-0685; R-0495 and
  R-0574 are the two Highs.
- BLOCK CAPS ARE TWO, not one: 490 lines TOTAL (DECISION F085 D6) and 400 lines
  PROSE (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R31

<<<SLICE LEDGER31
Gate: F031 R30 — the F031 R30 entry. R30 PASSED ON EVERY ONE OF ITS NINE GATES, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk rather than reading the handback back; every value that handback states reproduced cell for cell. TRANSPORT HELD IN ITS STRONGEST FORM and the chain closed end to end for the third round running: the reviewer's own scratchpad original `.remedy-wt/f031-r30.md`, the C0a blob committed at `3cdced7f`, the C0b blob committed at `a4a35350` and `.agent/last_block.md` read off disk at `5ee3024b` are ALL FOUR byte-identical at sha256 `350809178e8c5c50e14d709836d60b251aa294061816550bd2b173ee95fcb2c9` over 36722 bytes and 448 lines, C0a and C0b resolving to the SAME git blob `537c08aa7b7a7d371d381570e40dfb72555b5bb5`, and that digest is the one the reviewer measured on its own bytes BEFORE emission. THE EXTRACTION printed 2 slices, 49 content lines and 448 total, so PROSE was 399 against the 400-line cap DECISION F085 D5 sets and TOTAL 448 against the 490 DECISION F085 D6 sets. THE PLAN at `277d1f61` equals PLANF031R30 exactly at 2774 bytes and 48 lines, with the trailing-newline-removed control FALSE, `^## Goal$` 1 and `^## Next Steps$` 1, and 48 strictly under the 50 AGENTS.md sets. THE C2 APPEND SATISFIED WHOLE-FILE EQUALITY: `.agent/live_review.md` at `eaf80e31` is its C1 blob plus one newline plus LEDGER30, at 729516 + 1 + 7312 = 736829 against an actual 736829, and the SECOND, INDEPENDENT READER AGREED — a blank-line split moves the unit count 321 to 322 and its last unit equals that slice's single paragraph, trailing newlines rstripped on BOTH sides. THE NEGATIVE CONTROL WAS RUN IN MEMORY, never on the tracked file: one byte flipped at offset 729567, inside the appended text, and both readers REJECT the mutant while both ACCEPT the true file. THE SETS MOVED EXACTLY WHERE THAT BLOCK'S CONSTRAINT 10 ALLOWED AND NOWHERE ELSE: `^- R-\d+ — ` 246 to 246 with the ids ADDED and the ids REMOVED BOTH the EMPTY SET and all 246 DISTINCT, maximum `R-0685` unmoved; `^Done: R-\d+ — ` 5 to 5 with the ids ADDED the EMPTY SET; `^Landed: R-` 0 to 0; `^Recurrence: R-` 22 to 22; `^Gate: R\d+ — ` 19 to 19 frozen and `^Gate: F\d+ R\d+ — ` 10 to 11, the added key exactly `F031 R29`, all keys DISTINCT. The §3 item 10 open set is 241 at `eaf80e31`. BOTH RED CONTROLS ARE THE REVIEWER'S OWN, run in a disposable worktree at `572f7298` created at a path that did not exist and removed BY THAT EXACT PATH, with `git worktree list` 1 line and `git status --porcelain` 0 after. The TYPE control needed a route the block did not supply, and the reviewer's FIRST attempt at one was BLIND: a `paths` mapping of every specifier into the primary's `node_modules` resolved `react` to its JavaScript and produced 213 `TS7016` diagnostics on the UNMUTATED tree, so the green control caught the broken route before any red was believed — the §3 item 12 discipline paying for itself. With `node_modules/@types/*` added ahead of `node_modules/*` in that mapping the unmutated worktree gives REAL exit 0 at ZERO diagnostics, and with S1's `onSelectNode` attribute removed from the `DecisionInboxCard` element the same command gives REAL exit 2 at exactly ONE diagnostic, `TS2741: Property 'onSelectNode' is missing in type … but required`. The CSS control, with one `var(--remedy-bg-2)` inside `.decisionJumpChip` renamed to a token `tokens.css` does not define, gives REAL exit 1 at 1 failed and 50 passed, naming `TestEveryCustomPropertyResolves::test_the_unresolved_set_has_not_grown` and the undefined property — so both of this round's real gates are proven able to fail. Both files were restored byte-identically inside that worktree, whose `git status --porcelain` was 0 before removal. THE SUITES ARE THE REVIEWER'S OWN, run SERIALLY, never two alive at once, every one a REAL exit 0: `npm run typecheck` with zero diagnostics on stdout and stderr, `npm run test:unit` at 26 files and 400 tests — BOTH counts identical to the base, because this round adds no test and no test reaches its markup; then `tests/ui_server/` 480, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16, `tests/ui_contracts/` 525 passed with 4 skipped and the canary `test_golden_path` 42, every count identical to the base reading. THE PRODUCTION CHANGE IS WHAT S1 THROUGH S4 ORDERED. `RightLivePanel.tsx` moves ONE line, handing the card the same `dashboard.tasks` and `onSelectNode` the `ActivityFeedCard` line beside it already passes. `DecisionInboxCard.tsx` imports `nodeIdForDecisionCard` from `../../api/decisionFocus` ONCE and calls it ONCE per decision, imports `FocusableTask` from `../../api/feedFocus` and declares no type of that name, holds `fetch(` 0 times, keeps the answer button's `disabled` attribute, and renders the jump control ONLY when the resolver answers non-null — a null renders `null`, so a card that cannot jump does not appear to offer it. The falsified projection sentence is GONE at 0 occurrences of `never a value this file chose`, replaced by one that splits a card's CONTENT from this file's own fixed affordance labels, and the SEND sentence is untouched and still true. `.decisionJumpChip` uses six custom properties and EVERY one of them is defined in `apps/ui/src/styles/tokens.css`, with `--remedy-focus` appearing only inside a comment explaining why it is unusable and never inside a `var()`. DECISION F031 D15 landed with its citations correct. HYGIENE HELD: line-anchored `^<<<SLICE ` and `^<<<END ` are 0 in `.agent/plan.md` at `277d1f61`, `.agent/live_review.md` at `eaf80e31` and all four files C3 writes, against a CONTROL of 2 and 2 over the C0a blob; the range `def633e9`..`572f7298` names 8 paths, none under `docs/`, `packages/` or `tests/` and none of the forbidden set, with range-minus-change-set EMPTY and change-set-minus-range exactly `.agent/handoff.md`; the six commits `3cdced7f` through `5ee3024b` are each SINGLE-PARENT with insertions 448, 261, 20, 2, 140 and 53 read from `git diff --numstat`, each under the 500 cap AGENTS.md DECISION F104 D1 sets, and those numbers agree cell for cell with the `+/-` column of that handback's `## Commits` table; `git ls-files .remedy-wt` 0, the zip glob 0, `git worktree list` 1 line and `git status --porcelain` 0. THE BLOCK'S OWN OBJECT IDS RESOLVE: 19 SHA-shaped occurrences, 10 distinct, 9 `commit` and 1 `blob`, failing set EMPTY. THE REFLOG, scoped to the 5 entries C0a through C3, reads `commit` throughout, so `amend`, `rebase` and `cherry` are 0 each. THE PUSH DISCHARGED: `refs/heads/feature/f031-decision-inbox` on the remote and the local tip are both `5ee3024b75af8fcb3015bd2e013510f597d545c3`, no pull request was created, no branch deleted and nothing merged. THE HANDBACK IS INSIDE ITS CAP AGAIN: 88 lines against the 100-line tier its 6 commits earn, with 12 lines to spare and no overage line needed. ITS MANDATED CONTENT IS ALL PRESENT — the reviewer checked for the item-status table and the finding counts by NAME and found neither heading, then checked for the CONTENT and found both: an 11-row table covering C0a through C4, S1 through S4 and the push, with `deviated` correctly against S2, and the finding counts inside the G5 entry carrying the RULE and the COMMIT DECISION F009 D10 requires. Only the two HEADINGS `## Item status` and `## Findings` are absent, which is a template deviation and not a dropped section; the next block asks for the headings and no finding is minted for it. THE NINE DECLARED ITEMS ARE ADJUDICATED AND NONE IS A DEFECT OF THE ROUND. Items 4, 6, 7, 8 and 9 are the block being obeyed and its scratch accounted for. Item 1, two label constants where the spec named one, is CORRECT: S2(e) ordered a sentence asserting that the fixed affordance labels are constants at the top, and leaving the title inline would have made that ordered sentence false on landing. Item 5, typing the two new props REQUIRED rather than optional as `ActivityFeedCard` exports them, is the stronger reading and the one G6(a) needs, since an optional prop cannot go red when it is dropped. Item 3, the `tsc` route, is exactly the disclosure the block asked for and the reviewer reproduced it independently. ITEM 2 IS THE REVIEWER'S OWN DEFECT and is the R-0560 recurrence appended beside this entry. THE VERDICT IS PASS.

Recurrence: R-0560 — SECOND INSTANCE, found by the WORKER while applying the R30 block and declared before the reviewer read the diff. MEASURED at `3cdced7f`: that block's G6(a) ordered the `onSelectNode` attribute deleted from the `DecisionInboxCard` element and then ordered "count the exact bytes you delete in THAT file first and report the count, which MUST be 1 (§3 item 25)". The reviewer re-measured at `572f7298`: the bytes ` onSelectNode={onSelectNode}` occur THREE times in `apps/ui/src/components/panels/RightLivePanel.tsx`, once on each of the `DecisionInboxCard`, `ActivityFeedCard` and `TaskChecklistCard` elements, so the ordered count of 1 was unattainable for the string as described. The worker resolved it correctly and without being told how — it took the whole `<DecisionInboxCard … />` element, whose occurrences are 1, deleted the attribute inside that, and reported the count of the target it actually used. WHY THIS IS A RECURRENCE AND NOT A NEW ID, per §3 item 30: R-0560 is OPEN and already names this defect — a destructive gate quoting bytes that are not unique at the SHA the control runs at — and a second id would be two things to resolve for one rule. WHAT THIS INSTANCE ADDS. R-0560's own instance was ambiguity ACROSS FILES, the same line living in a source file and a test file, and its counter-measure reads "where the bytes recur inside the named file, the control orders a longer UNIQUE byte string instead". This instance is multiplicity WITHIN one file, and it shows that naming the enclosing ELEMENT — which the R30 block did do, and which is stricter than the enclosing FUNCTION that instance criticised — is still not sufficient, because the block went on to order a COUNT over the shorter string it had quoted. The widened counter-measure owed to §3 is therefore: a destructive gate MEASURES the bytes it prints, in the file it names, at the base commit, BEFORE emission, and where that count is not 1 the block PRINTS the longer unique string itself rather than ordering a count the worker must discover is wrong. Citing item 25 while breaking it is what makes this worth recording: the R30 block quoted the item number in the same sentence that violated it. THAT EDIT IS ROUTED TO THE INTEGRATION-GATE ROUND'S BLOCK, beside the items R-0683, R-0377, R-0419 and R-0429 already route there. R-0560 stays OPEN until the checklist item lands.
<<<END LEDGER31

── Done when ─────────────────────────────────────────────────
Run every gate yourself, record its REAL exit code and REAL output, and report
ONE ENTRY PER GATE in the handback, as briefly as the ordered values allow and
with transcripts kept out (R-0582). "Green" as a word is a finding. Every gate
runs at a commit STRICTLY EARLIER than C4 (§3 item 31); G9's push follows it.

G1  Branch, cleanliness, transport. `git branch --show-current` prints
    `feature/f031-decision-inbox` and NOT `main`; `.agent/STOP` read from disk
    is ABSENT before C0a and again before C4; `git status --porcelain` line
    count after each of C0a, C0b, C1, C2 and C3 is 0. Then report sha256, byte
    count and line count for FOUR readings — `.remedy-wt/f031-r31.md` before
    C0a, the committed C0a blob, the committed C0b blob, and
    `.agent/last_block.md` off disk after C0b — ALL FOUR EQUAL, and the git
    blob id of C0a's and C0b's file, the SAME id.

G2  Extraction and the block's own two caps. Run your extractor over the
    COMMITTED C0a blob and report the slice count, the CONTENT lines inside
    markers, and the TOTAL — the numbers YOUR extractor printed — then PROSE
    as TOTAL minus CONTENT, against the two caps the Base names. If either is
    exceeded say so plainly and continue; it is the reviewer's to fix.

G3  The plan. `.agent/plan.md` at C1 is byte-equal to PLANF031R31 under your
    stated newline convention; report slice length, file length and
    convention. NEGATIVE CONTROL: NOT byte-equal to that slice MINUS its
    trailing newline. `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` STRICTLY
    under 50.

G4  The C2 append, as ONE equality over the whole file, in the shape
    constraint 8 states — name that paragraph, do not restate its formula.
    Report the boolean and the byte arithmetic against the C1 length you
    measure yourself. Report a SECOND, INDEPENDENT reading: split the
    committed file on blank lines, take the LAST N units, and confirm they
    equal LEDGER31's paragraphs IN ORDER, where N is the number YOUR split
    measured; give the unit count before and after, and STATE YOUR
    TRAILING-NEWLINE HANDLING, because a naive split reports FALSE on a
    byte-perfect file. This slice carries MORE THAN ONE paragraph, so ORDER is
    load-bearing and a set comparison does not discharge it. NEGATIVE CONTROL:
    flip ONE byte inside the appended text; BOTH readers must reject the
    mutant and BOTH accept the true file. Do that flip in memory or under a
    disposable worktree per constraint 12, never on the tracked file.

G5  The ledger sets, base versus C2 in `.agent/live_review.md`, in the shape
    constraint 10 states — report each side of every movement it names, that
    the `- R-` ids ADDED and REMOVED are BOTH the EMPTY SET, that all
    `^- R-\d+ — ` ids are DISTINCT, that the maximum is still `R-0685`, and
    that the `^Done: R-\d+ — ` ids ADDED are ALSO the EMPTY SET.
    `^Gate: R\d+ — ` 19 → 19 UNCHANGED, and `^Gate: F\d+ R\d+ — ` 11 → 12, the
    ADDED key being exactly `F031 R30`, all keys DISTINCT (§3 item 26). Report
    `^Recurrence: R-` 22 → 23, that `^Recurrence: R-0560` moves 0 → 1, and
    `^Landed: R-` 0 → 0. Report the §3 item 10 open set at C2, that
    `- R-0560 — ` still occurs exactly ONCE line-anchored so its landed
    paragraph was not edited, and that `git diff --name-only` over C3 does NOT
    name `.agent/live_review.md` — the whole of constraint 8's "nothing at all
    in any other commit".

G6  THE RED PROOF, in a disposable worktree at C3 per constraint 12, so the
    primary checkout is never mutated, with vitest run from the PRIMARY
    checkout's `apps/ui` so the primary's `node_modules` resolves:
      npx vitest run --config <PRIMARY>/apps/ui/vitest.config.ts \
        --root <WORKTREE>/apps/ui src/api/
    Run it UNMUTATED first and report the file and test counts. Then, INSIDE
    THAT WORKTREE, in `apps/ui/src/api/decisionSubmit.ts`, MUTATE S1's
    status mapping so that EVERY answered request maps to the accepted
    outcome — the confusion a sender would most plausibly ship, since a
    refusal and a success are both answers and neither throws. THE TARGET IS
    YOURS TO NAME, because only you have written it: choose the SHORTEST byte
    string in that file that occurs EXACTLY ONCE and expresses that mapping,
    and report the string plus its measured count of 1 (§3 item 25, and R-0560's recurrence in LEDGER31 — this block
    deliberately does not quote a target it cannot measure). Leave every other
    byte alone and run the same line again. IT MUST GO RED. Report the REAL
    exit code, the NAMES of the failing tests, and the failure count YOUR run
    measured; this block states no number. A GREEN means S2's tests never
    distinguish a refusal from an acceptance, and is reported as such. Restore
    the file byte-identically, report that worktree's `git status
    --porcelain` as 0, remove the worktree BY ITS EXACT PATH and report
    `git worktree list` as 1 line after, naming that path.

G7  Structure, then the suites. Report, as counts YOU measured at C3, over
    `decisionSubmit.ts`: that `DecisionSendRequest` is imported as a TYPE from
    `./decisionSend` — quote the import line; that the send parameter carries a
    DEFAULT naming the global `fetch` — quote the signature; that
    `setTimeout`, `Date.now` and `crypto` each occur 0 times; and that it
    reaches into no decision FIELD, by reporting `answerText`, `decision_id`,
    `client_nonce`, `taskId` and `buildDecision` as 0 each — the module moves
    a request and reports what came back, which those counts make measurable
    rather than asserted. Over `decisionSubmit.test.ts`: that `vi.` and
    `globalThis` each occur 0 times, so no global was patched. Then
    in the PRIMARY checkout at the C3 tree, all REAL exit 0, run SERIALLY and
    never two alive at once, with `git worktree list` reported as 1 line
    immediately BEFORE the first of them. At `apps/ui`: `npm run typecheck`
    with ZERO diagnostics on stdout and stderr; `npm run test:unit`, reporting
    the file and test counts YOUR run measured — `decisionSend.test.ts` must
    still be exactly 12, `decisionAnswer.test.ts` exactly 20,
    `decisionCard.test.ts` exactly 36, `decisionFilter.test.ts` exactly 20,
    `decisionOrder.test.ts` exactly 16 and `decisionFocus.test.ts` exactly 7,
    any movement in any of the six being a finding, while the FILE count must
    be exactly 27, one more than the Base's 26, that one being
    `decisionSubmit.test.ts`; report that new file's own count. Then in
    Python, by these exact command lines with no extra flag:
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/ui_contracts/ -q
      python3 -m pytest tests/cli/test_golden_path.py -q
    These are the four state readers a round rewriting `.agent/` state gates,
    plus `tests/ui_contracts/`, plus the canary. The reviewer ran all six at
    `5ee3024b` with these exact lines and measured in that order 480, 52, 21,
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
    `apps/ui/src/api/decisionSend.ts`, `apps/ui/src/api/decisionAnswer.ts`,
    `apps/ui/src/api/decisionCard.ts`, `apps/ui/src/api/decisionFocus.ts`,
    `apps/ui/src/RemedyApp.tsx`,
    `apps/ui/src/components/shell/RemedyShell.tsx`,
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
    and records them in the R31 entry of `.agent/live_review.md`. In
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

GIVE THE ITEM-STATUS TABLE AND THE FINDING COUNTS THEIR OWN HEADINGS, named as
the template names them. R30's handback carried both in full but under neither
heading; that cost nothing and is not a finding, and this line is how it stops
recurring.

EVERY NUMERAL YOUR HANDBACK STATES ABOUT A LIST IS COUNTED MECHANICALLY BEFORE
YOU COMMIT IT, or the list is named and NO numeral is given (R-0441). Any
finding count carries the RULE and the COMMIT it was measured at (F009 D10); a
narrower set is "the findings this feature must still act on".

THE HANDBACK LINE CAP: this block states no cap and no tier. Resolve it from
AGENTS.md under `### handoff.md` against the commit count constraint 4 fixes,
and report BOTH that count and the tier. R29 and R30 both met that tier, so it
is reachable; if the MANDATED content still does not fit, exceed it and carry a
DECISION D15 line naming your count as a NUMERAL (R-0430) and its cause.

YOUR `## Next` SECTION names, in order: that the next session reads
`.agent/STOP` from disk as Phase 1 rule 1 BEFORE the Open PR Gate as rule 2;
that the R31 verdict is UNRECORDED and owed by the next round's ledger commit
(DECISION F085 D9); and that R32 is T003's LAST wiring round and is the first
round that falsifies the three "nothing posts yet" sentences.

Declare every deviation, contradiction and assumption.
──────────────────────────────────────────────────────────────

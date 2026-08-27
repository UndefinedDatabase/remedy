── STEP R26 — F031 Decision inbox ────────────────────────────
Goal:        T003 OPENS, at the layer a test can reach. The browser learns to
             SAY `decision.resolve`: a pure builder turns a card plus a typed
             answer into the exact body `/api/jobs/<id>/commands` already
             accepts, and refuses the four bodies that door would reject
             anyway. R-0682's `role="group"` lands in both chip rows.

Fortschritt: ~90 % (F031 claimed; R1 through R25 landed, R25 gated here ·
             T001 SHIPPED · T002a MODEL shipped, wired and RENDERED ·
             T002b ORDERING, FILTERING and BADGE COMPLETE and gated ·
             T003 answer-command model here, its sender and forms open)
             — Schaetzung

Bundle:      C0a save this block · C0b mirror it into last_block · C1 the
             plan · C2 the R25 gate entry and R-0682's resolution · C3 the
             answer-command module, its tests, the `role="group"` fix in both
             chip rows and DECISION F031 D11 · C4 handback.

Change set:  exactly these paths, nothing else —
             .agent/authored/f031-r26.md                             (C0a)
             .agent/last_block.md                                    (C0b)
             .agent/plan.md                                          (C1)
             .agent/live_review.md                                   (C2)
             apps/ui/src/api/decisionAnswer.ts                       (C3, NEW)
             apps/ui/src/api/decisionAnswer.test.ts                  (C3, NEW)
             apps/ui/src/components/panels/DecisionInboxCard.tsx     (C3)
             apps/ui/src/components/graph/GraphFilterChips.tsx       (C3)
             .agent/decisions.md                               (C3, D11)
             .agent/handoff.md                                       (C4)
             This list bounds the round's WRITES, not its ACTIONS: the push
             named in G9 is ordered explicitly and is not a file (R-0674).
             NOTHING under `packages/` is written — the door already exists.

── Base ──────────────────────────────────────────────────────
The round base is `92b323e314980ecb4eef7fd79fe619d54f55b8c6`, the R25
handback commit and the tip of `feature/f031-decision-inbox`, local and remote
EQUAL — the reviewer measured both at the R25 gate. Stay on that branch; never
commit to `main`. Every SHA-shaped token here resolved under `git cat-file -t`.

Readings the reviewer MEASURED at that base, re-checkable there:
- `.agent/live_review.md` 687558 bytes and 1249 lines; `^- R-\d+ — ` 244 all
  DISTINCT, maximum `R-0683`; `^Done: R-\d+ — ` 4, so the §3 item 10 open set
  is 240; `^Recurrence: R-` 19; `^Landed: R-` 0. THE GATE SERIES IS SPLIT by
  DECISION F031 D7: `^Gate: R\d+ — ` 19, frozen, and `^Gate: F\d+ R\d+ — ` 6,
  those six being `F031 R19` through `F031 R24`.
- `.agent/plan.md` 49 lines, 2849 bytes. `docs/roadmap/**` is UNTOUCHED, so
  the §3 docs-round gate is not earned and is not ordered.
- `apps/ui`: `npm run typecheck` exit 0, zero diagnostics on stdout and
  stderr; `npm run test:unit` exit 0 at 23 files and 357 tests, of which
  `decisionCard.test.ts` is 32, `decisionFilter.test.ts` 20 and
  `decisionOrder.test.ts` 16.
- The Python suites, every one exit 0: `tests/ui_server/` 480,
  `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16,
  `tests/ui_contracts/` 525 passed with 4 skipped, `test_golden_path` 42.
- THE DOOR THIS ROUND ADDRESSES ALREADY EXISTS, every value below read out of
  `packages/orchestration/ui_server.py` at this base rather than inferred from
  a name. `do_POST` routes exactly one shape, `/api/jobs/<job_id>/commands`;
  everything else is 405. `_read_command_payload` requires a JSON OBJECT with
  `command` a non-empty string, `client_nonce` a non-empty string that
  `command_nonce.nonce_is_valid` accepts, and an optional `args` object whose
  ABSENCE means the empty object. `DECISION_RESOLVE_COMMAND_ID` is the literal
  `decision.resolve`. `_dispatch_decision_resolve` reads exactly `decision_id`
  and `answer` out of `args`, each degrading to `""`; DECISION F009 D22 rules
  `source` deliberately NOT sent, so the answer takes the `human` default. A
  None dispatch is a 409 — an absent or already-resolved decision.
- THE NONCE'S CHARACTER CLASS IS `safe_points._ID_RE`, reached through
  `nonce_is_valid` -> `is_safe_id`, exactly `^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$`.
  It is a guard because the nonce becomes a FILENAME in the control directory.
- THE BROWSER HAS NO WRITE CLIENT AT ALL: `remedyApi.ts` issues only
  `method: "GET"`, `nonce` occurs 0 times under `apps/ui/src`, and
  `decisionAnswer.ts` does not exist — S1 creates it. The card's answer
  buttons ship DISABLED under `ANSWER_PENDING_TITLE`; this round leaves them.
- `DecisionCardModel` carries `id: string`, `isOpen: boolean` and
  `answers: DecisionAnswer[]`, each `{ kind, label, value }`. No new field.
- THE TWO CHIP ROWS R-0682 NAMES both measure `role=` 0 times at this base,
  while `aria-label` occurs 3 times in `DecisionInboxCard.tsx` — one inside a
  comment — and 1 time in `GraphFilterChips.tsx`.
- THE SUITE GUARDS OVER THE FILES C3 REWRITES were read first (§3 item 7).
  `tests/ui_contracts/test_graph_architecture.py` reads `GraphFilterChips.tsx`
  by SUBSTRING PRESENCE of four label strings only, no test reads
  `DecisionInboxCard.tsx` at all, and there is NO `count(` and no `== 1`
  assertion over either. Adding an attribute is safe.
- THIS BLOCK'S OWN TWO CAPS, measured on its final bytes before emission and
  stated so your re-measurement can disagree with the reviewer's, are 490
  lines TOTAL (DECISION F085 D6) and 400 lines PROSE (DECISION F085 D5). G2
  orders you to report both from the COMMITTED blob.

── Constraints ───────────────────────────────────────────────
1. Apply every authored SLICE BYTE FOR BYTE. Never retype, rewrap or "fix"
   one. If a slice looks wrong, apply it verbatim and DECLARE the
   disagreement: a contradiction in this block is the reviewer's defect.
2. THE PRODUCTION CHANGE, ITS TESTS AND DECISION D11 ARE DESCRIBED, NOT
   SLICED. The numbered specification S1 through S4 fixes behaviour,
   structure and copy; YOU write that code, those tests and that decision
   entry under AGENTS.md's Mandatory Self-Review Loop and its File Editing
   Safety Rules. Where the spec is silent, prefer the idiom the neighbouring
   module already uses. Where the spec is WRONG, say so in the handback and
   do the right thing.
3. Slice transport. The reviewer's original is on disk at
   `.remedy-wt/f031-r26.md`. COPY that file to `.agent/authored/f031-r26.md`
   at C0a — never retype it — and mirror it byte-identically into
   `.agent/last_block.md` at C0b. THIS BLOCK STATES NO DIGEST OF ITSELF: a
   file cannot carry its own sha256, so the proof is the disk-to-disk
   comparison G1 orders over four readings, which is what
   docs/agents/self_drive_protocol.md substitutes for the hash-stamp ritual
   when there is no transport. Report the digest YOU measure. Extract every slice
   PROGRAMMATICALLY out of the COMMITTED C0a blob by its marker LINES —
   `<<<SLICE <NAME>` opens, `<<<END <NAME>` closes. Marker lines never reach
   a target file.
4. Commit sequence, exactly: C0a, C0b, C1, C2, C3, C4. No extra commit, none
   dropped, no reordering. C1 is FIRST substantive because this round writes
   the finding ledger (§3 item 23). C3 SHIPS S1 THROUGH S4, the
   `role="group"` fix in BOTH chip rows included: the `Done: R-0682`
   paragraph C2 writes describes that change, and this clause is the commit
   order it names in place of a SHA (§3 item 20, the R-0524 carve-out). To
   correct a landed commit, do NOT add one outside this sequence — declare
   it, and give it its own `## Commits` and item-status rows (R-0675).
5. Never amend, rebase, cherry-pick, force-push or rewrite history; never
   delete a branch; never merge; create no pull request.
6. `git status --porcelain` prints 0 lines after every commit. Read
   `.agent/STOP` from disk before C0a and again before C4; if present, finish
   the commit in hand, write the handback and stop. NEVER delete that
   sentinel (R-0347).
7. The slices this block carries are the whole text PLANF031R26 and the
   appended text LEDGER26. This paragraph names them and states no count; G2
   orders you to report the count YOUR extractor measured.
8. THE ONE APPEND'S SHAPE, STATED ONCE HERE, WITH EVERY GATE NAMING THIS
   PARAGRAPH RATHER THAN RESTATING IT. Under the newline-INCLUDED convention
   each slice already ends in a newline, so `.agent/live_review.md` after C2
   is EXACTLY: its blob at C1, then one newline, then LEDGER26 — and it
   receives NOTHING ELSE in that commit, and nothing at all in any other
   commit of this round (R-0657). LEDGER26's own paragraph count is yours to
   measure; this paragraph states no number. `.agent/decisions.md` also GROWS
   at C3, by text YOU author under S4, so no equality gate is ordered over it
   and none may be reported.
9. THIS BLOCK CARRIES NO FROM/TO PAIR, so no containment test is reported and
   no FROM-zero count is ordered (§3 item 15). The plan is a WHOLE-FILE
   replacement and LEDGER26 is an append.
10. THIS ROUND MINTS NO FINDING ID AND RESOLVES EXACTLY ONE. LEDGER26 carries
    no `- R-` paragraph, so `^- R-\d+ — ` stays 244 with the maximum still
    `R-0683`; it carries one `Done:` line, so `^Done: R-\d+ — ` moves 4 → 5
    and the §3 item 10 open set moves 240 → 239. `^Landed: R-` and
    `^Recurrence: R-` are UNCHANGED at 0 and 19. WRITE NO `Landed:` LINE: the
    resolution is reviewer-authored and is already in LEDGER26. No landed
    finding paragraph is edited (§3 item 20).
11. TOUCH NO DOCUMENT AND NO OTHER CODE. Nothing under `docs/`, `packages/`
    or `tests/`, and neither `.agent/context.md` nor either
    `f031_*_inventory.md`. Inside `apps/` only the four paths the change set
    names are written — NOT `RightLivePanel.tsx`, `remedyApi.ts`,
    `RemedyApp.tsx`, `decisionCard.ts`, `decisionFilter.ts`,
    `decisionOrder.ts` or any other test file.
12. Destructive verification runs ONLY in a disposable `git worktree` under
    `.remedy-wt/`, removed BY ITS EXACT PATH (R-0662) and before the G7
    suites. Everything already there is pre-existing scratch belonging to no
    commit, this block's own file included: create no worktree at an existing
    path, and delete nothing you did not create.

── Specification (S1–S4) — the production change ─────────────
S1  THE ANSWER COMMAND, a NEW module `apps/ui/src/api/decisionAnswer.ts`.
    It is PURE: it performs no I/O, opens no socket and reads no clock, so
    every one of its answers is a value a test can assert. It exports, each
    with the one-line WHY comment directly above it:
    (a) the command id as a named constant, whose value is the literal
        `decision.resolve` the Base quotes from `ui_server.py`;
    (b) a predicate over a candidate nonce, mirroring the server's character
        class the Base states, total over `unknown`;
    (c) a function from a job id to that job's commands PATH, in the shape
        the Base quotes — no host, no query, leading slash;
    (d) THE BUILDER: it takes a `DecisionCardModel`, the answer text the
        operator chose or typed, and a nonce, and returns EITHER the exact
        request body the door accepts — `command`, `client_nonce` and an
        `args` object carrying `decision_id` and `answer`, those key
        spellings and no others — OR `null`.
    IT RETURNS `null` FOR EXACTLY FOUR REASONS, and each is a body the door
    would refuse anyway, refused one round trip earlier: the model's `id` is
    empty, so no record could match; the answer text is empty, so the
    decision would resolve with nothing; the nonce fails (b); or the model is
    NOT open, which the door answers 409. It sends NO `source` key —
    DECISION F009 D22 rules that omission and passing one would land the
    record in neither tally — and it invents no key the door does not read.
    Name each export for what it answers, carrying the domain word, so it
    greps to its own definition and its real usages only.
    THE DELIBERATE ABSENCES ARE DOCUMENTED WHERE A READER WOULD SEARCH FOR
    THEM, per AGENTS.md's Code Discoverability rules: this module neither
    SENDS the request nor MINTS the nonce — the caller supplies it, which is
    what keeps this module pure — and the sender round owns both.

S2  THE TESTS, a NEW file `apps/ui/src/api/decisionAnswer.test.ts` following
    the idiom of `decisionCard.test.ts` beside it. Build every model through
    `buildDecisionCardModel` rather than by hand, so the tests pin the SEAM
    and not a literal. Cover, at minimum: the accepted body's exact shape and
    every one of its key spellings; that no `source` key is present; each of
    S1's FOUR refusals separately, one test each; the nonce predicate saying
    yes to a plain id and no to the empty string, to a 65-character value, to
    one opening with a hyphen and to one carrying a path separator; and the
    path function's exact output. Name each test for the property it pins.

S3  R-0682, in BOTH files the finding names: add `role="group"` beside the
    existing `aria-label` on the chip row of `DecisionInboxCard.tsx` and on
    the chip row of `GraphFilterChips.tsx` — the ARIA pattern that makes a
    labelled group nameable, where a bare `div` maps to `generic` and drops
    the name. Add NOTHING else to either file: no pin under
    `tests/ui_contracts/`, no new label, no restyling, and do NOT touch the
    `<output>` the previous round added. Where a header comment states an
    absence this change falsifies, repair it and name what falsified it.

S4  DECISION F031 D11, appended to `.agent/decisions.md` in the shape D1
    through D10 already use there, ruling the SPLIT this round makes.
    CHOSEN: the answer path ships as a PURE builder now and a side-effecting
    sender later, because DECISION F031 D5 leaves the markup reached by no
    test — so everything that can be a value is made one and the untested
    remainder shrinks to the fetch call. CHOSEN: the nonce is the CALLER's to
    supply, so the builder needs no clock, no random source and no injection
    seam. CHOSEN: the builder refuses four bodies the server would also
    refuse, and that duplication exists to spare the operator a round trip,
    NEVER to replace the server's check, which stays the only authority.
    ALTERNATIVE: one function that builds and sends, rejected because it puts
    the body's shape beyond every test this repository can run. REVERSE it by
    folding the builder into the sender once a DOM harness lands.

── Authored slices ───────────────────────────────────────────

<<<SLICE PLANF031R26
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1–D11.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R26 OPENS T003 at the layer a test can reach: `decisionAnswer.ts` turns a card
plus a typed answer into the exact body `/api/jobs/<id>/commands` accepts and
refuses four the door would refuse anyway, while R-0682's `role="group"` lands
on both chip rows.

## Next Steps
1. T003's sender round wires that body to the door — the CSRF header, the
   bearer token, the nonce the browser mints, and the answer affordances the
   card currently ships DISABLED.
2. T003's remainder: the clarification form, the deep links into graph focus,
   and the ruling on `NeedsAttentionCard`'s decision branch (DECISION F031 D4).
3. The integration-gate round per `docs/agents/integration_gate.md`, whose
   block also carries the §3 checklist item R-0683 routes there, then closure
   per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- THE BUILDER IS PURE AND THE DOOR IS NOT. Every refusal it makes is a SECOND
  copy of a rule `ui_server.py` already enforces — the nonce character class
  most of all — so the two can drift. It refuses early to spare the operator a
  round trip, never to replace the server's check.
- NO TEST REACHES THE MARKUP under DECISION F031 D5, so `role="group"` is
  pinned by review alone; this round adds no `tests/ui_contracts/` pin, and
  this line records that gap rather than implying coverage.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 240 at `92b323e3`, and this round's C2 lowers it to 239 by resolving
  R-0682 and minting nothing, in the commit order the R26 block's constraint 4
  fixes.
- The findings THIS FEATURE MUST STILL ACT ON are R-0403, R-0413, R-0431,
  R-0441, R-0445, R-0471, R-0495, R-0533, R-0574, R-0593, R-0601, R-0622,
  R-0625, R-0632, R-0672, R-0674, R-0675, R-0676, R-0677, R-0678, R-0679 and
  R-0683; R-0495 and R-0574 are the two Highs.
- BLOCK CAPS ARE TWO, not one: 490 lines TOTAL (DECISION F085 D6) and 400 lines
  PROSE (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R26

<<<SLICE LEDGER26
Gate: F031 R25 — the F031 R25 entry. R25 PASSED ON EVERY ONE OF ITS NINE GATES, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk rather than reading the handback back; every value that handback states reproduced exactly, and R25 earns no finding against its execution. TRANSPORT HELD IN ITS STRONGEST FORM, cmp-against-scratchpad rather than the digest fallback: the reviewer's own `.remedy-wt/f031-r25.md`, the C0a blob committed at `31692efd`, the C0b blob committed at `7361d821` and `.agent/last_block.md` read off disk at `92b323e3` are ALL FOUR byte-identical at sha256 `763fadf96fd9f162398c1f43c1480014f601607d6d0c85f412af01043ed9e8a7` over 39202 bytes and 450 lines, C0a and C0b resolving to the SAME git blob `23946f597c7371987f5a51ec2aa877e41336228e`. THE EXTRACTION printed 2 slices, 52 content lines and 450 total, so PROSE was 398 against the 400-line cap DECISION F085 D5 sets and TOTAL 450 against the 490 DECISION F085 D6 sets. THE PLAN at `84f7e6dd` equals PLANF031R25 exactly at 2849 bytes and 49 lines, with the trailing-newline-removed control FALSE, `^## Goal$` 1 and `^## Next Steps$` 1, and 49 strictly under the 50 AGENTS.md sets; the narrow finding list it carries holds 23 DISTINCT ids across 25 occurrences, the two repeats being `R-0495` and `R-0574` named again as the Highs, so that handback's reading is exact. THE C2 APPEND SATISFIED WHOLE-FILE EQUALITY: `.agent/live_review.md` at `a48219d4` is its C1 blob plus one newline plus LEDGER25, at 677520 + 1 + 10037 = 687558 against an actual 687558, and the SECOND, INDEPENDENT READER AGREED — a blank-line split moves the unit count 309 to 311 and its last 2 units equal that slice's 2 paragraphs IN ORDER, trailing newlines rstripped on BOTH sides. THE NEGATIVE CONTROL WAS RUN IN MEMORY, never on disk: both readers REJECT the one-byte mutant and both ACCEPT the true file. THE SETS MOVED EXACTLY WHERE THAT BLOCK'S CONSTRAINT 10 ALLOWED AND NOWHERE ELSE: `^- R-\d+ — ` 243 to 244 all DISTINCT, ids ADDED exactly `R-0683`, ids REMOVED the EMPTY SET, maximum `R-0682` to `R-0683`; `^Done: R-` 4 to 4, `^Landed: R-` 0 to 0, `^Recurrence: R-` 19 to 19; `^Gate: R\d+ — ` 19 to 19 frozen and `^Gate: F\d+ R\d+ — ` 5 to 6, the added key exactly `F031 R24`, all keys DISTINCT. The §3 item 10 open set is 240 at `a48219d4`, and `- R-0593 — ` still occurs exactly ONCE line-anchored, so its landed paragraph was not edited. THE RED PROOF IS THE REVIEWER'S OWN, run in a disposable worktree at `82d4992a` created at a path that did not exist and removed BY THAT EXACT PATH, with `git worktree list` 1 line and `git status --porcelain` 0 after: the mutation target occurs EXACTLY ONCE in the file, UNMUTATED gives exit 0 at 20 files and 332 tests, and with `countOpenDecisions`'s body reduced to the every-card-counts mutant the run goes REAL exit 1 at 4 failed and 328 passed, the four being `counts only the open cards of a mixed list`, `answers zero when every card in the list is already resolved`, `reads isOpen rather than an open-SOUNDING status string` and `ignores the type filter's business entirely, counting across every type` — cell for cell what that handback reports; the file was restored byte-identically inside the worktree before removal. THE SUITES ARE THE REVIEWER'S OWN, run SERIALLY, never two alive at once, every one a REAL exit 0: `npm run typecheck` with zero diagnostics on stdout and stderr, `npm run test:unit` at 23 files and 357 tests with `decisionCard.test.ts` 27 to 32 — the difference being exactly the 5 tests S4 adds — and `decisionFilter.test.ts` 20 and `decisionOrder.test.ts` 16 both UNMOVED, then `tests/ui_server/` 480, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16, `tests/ui_contracts/` 525 passed with 4 skipped and the canary `test_golden_path` 42, every count identical to the base reading with no difference to account for. THE PRODUCTION CHANGE IS WHAT S1 THROUGH S3 ORDERED: `countOpenDecisions` greps to exactly one `export` line, it is called as `const openCount = countOpenDecisions(decisions);` — the UNFILTERED prop — no line holds both that name and the token `visible`, the guard `if (decisions.length === 0) return null;` occurs exactly once, and `aria-pressed` and `aria-live` are each still present. THE BADGE'S SURFACE WAS READ BEYOND THE GATES: every custom property `.decisionOpenCount` uses — `--remedy-radius-pill`, `--remedy-bg-2`, `--remedy-line` and `--remedy-muted` — resolves to exactly one definition in `apps/ui/src/styles/tokens.css` while `--remedy-focus` is referenced nowhere, and `build_decision_inbox` cards EVERY decision `list_decisions` yields rather than the open ones alone, so a count of `isOpen` over that list is the number the badge claims to show. HYGIENE HELD: line-anchored `^<<<SLICE ` and `^<<<END ` are 0 in `.agent/plan.md` at `84f7e6dd`, `.agent/live_review.md` at `a48219d4` and all six files C3 writes, against a CONTROL of 2 and 2 over the C0a blob; the range `6163e887`..`82d4992a` names 10 paths, none under `docs/`, `packages/` or `tests/` and none of the six that block forbids, with range-minus-change-set EMPTY and change-set-minus-range exactly `.agent/handoff.md`; the five commits `31692efd` through `82d4992a` are each SINGLE-PARENT with insertions 450, 286, 27, 4 and 166 read from `git diff --numstat`, each under the 500 cap AGENTS.md DECISION F104 D1 sets, agreeing CELL FOR CELL with the `+/-` column of that handback's `## Commits` table, which is the §3 item 28 reading; `git ls-files .remedy-wt` 0, the zip glob 0, `git worktree list` 1 line and `git status --porcelain` 0. THE BLOCK'S OWN OBJECT IDS RESOLVE: 24 SHA-shaped occurrences, 11 distinct, failing set EMPTY, 10 `commit` and 1 `blob`. THE PUSH DISCHARGED, which is the outcome that block's G9 routed to the reviewer rather than to any file R25 wrote: `refs/heads/feature/f031-decision-inbox` and the local tip are both `92b323e314980ecb4eef7fd79fe619d54f55b8c6`, no pull request was created, no branch deleted and nothing merged. THE HANDBACK FITS ITS TIER WITH NO OVERAGE: 100 lines against the 100 AGENTS.md allows for its 6 commits, every mandated section present, and the `Fortschritt:` block carried VERBATIM from the block at 5 lines. THE SIX DECLARED ITEMS ARE ADJUDICATED. Items 4 through 6 are the block being obeyed and are not deviations at all. ITEM 1, the THIRD falsified comment repaired in `DecisionInboxCard.tsx`, is CORRECT and earns no finding: that file is in the change set, S2 opens it anyway, and the sentence this very commit falsified is the exact R-0593 class S3 exists to close, so leaving it would have shipped a fresh instance while two others were retired. ITEM 2 IS NOT A CONTRADICTION, and this entry rules it so rather than leaving it standing as a reviewer defect: S2's "nothing else" is glossed by its own next sentence — "it is not a dot, not a colour and not a state" — so it bars a second SIGNAL and never a label, and the `<output>` that ships, whose implicit ARIA role `status` permits the accessible name a bare `div` would drop, meets both clauses exactly as written. ITEM 3's names are sound: `countOpenDecisions` and `.decisionOpenCount` each grepped to nothing before they were written. THE VERDICT IS PASS.

Done: R-0682 — Resolved at the F031 R26 gate by the round this entry's block orders: `role="group"` now sits beside the existing `aria-label` on BOTH chip rows the finding names — the one in `apps/ui/src/components/panels/DecisionInboxCard.tsx` and the one in `apps/ui/src/components/graph/GraphFilterChips.tsx` — which is the ARIA pattern that makes a labelled group nameable, so neither label is computed and dropped any more. The commit carrying it is fixed by constraint 4 of that block rather than named by a SHA, because the change had not landed when this text was authored (§3 item 20, the R-0524 carve-out). MEASURED at `92b323e3`, before the fix: `role=` occurs 0 times in each file while `aria-label` occurs 3 times in the first and 1 in the second, so both group labels were inert exactly as the finding says. NO PIN WAS ADDED to `tests/ui_contracts/`: the finding's fix clause offers one as a consideration rather than an order, DECISION F031 D5 leaves this markup reached by no test, and a substring pin over a `.tsx` file would guard the attribute's PRESENCE without proving it reaches the accessibility tree — so `.agent/plan.md` records the gap instead, which is honest where a green pin would not be. THE CITATION HALF of the finding needs no code change and gets none: `component_spec.md`'s FilterChips entry orders only `aria-pressed` and the polite live region, both of which ship and both of which still ship after this change, and the R23 block's misattribution stays recorded in the finding's own paragraph, which §3 item 20 forbids rewriting.
<<<END LEDGER26

── Done when ─────────────────────────────────────────────────
Run every gate yourself, record its REAL exit code and REAL output, and report
ONE LINE PER GATE in the handback, transcripts kept out (R-0582). "Green" as a
word is a finding. Every gate runs at a commit STRICTLY EARLIER than C4 (§3
item 31); G9's push runs after it and names its carrier.

G1  Branch, cleanliness, transport. `git branch --show-current` prints
    `feature/f031-decision-inbox` and NOT `main`; `.agent/STOP` read from disk
    is ABSENT before C0a and again before C4; `git status --porcelain` line
    count after each of C0a, C0b, C1, C2 and C3 is 0. Then report sha256, byte
    count and line count for FOUR readings — `.remedy-wt/f031-r26.md` before
    C0a, the committed C0a blob, the committed C0b blob, and
    `.agent/last_block.md` off disk after C0b — ALL FOUR EQUAL, and the git
    blob id of C0a's and C0b's file, the SAME id.

G2  Extraction and the block's own two caps. Run your extractor over the
    COMMITTED C0a blob and report the slice count, the CONTENT lines inside
    markers, and the TOTAL — the numbers YOUR extractor printed — then PROSE
    as TOTAL minus CONTENT, against the two caps the Base names. If either is
    exceeded say so plainly and continue; it is not yours to fix.

G3  The plan. `.agent/plan.md` at C1 is byte-equal to PLANF031R26 under your
    stated newline convention; report slice length, file length and
    convention. NEGATIVE CONTROL: NOT byte-equal to that slice MINUS its
    trailing newline. `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` STRICTLY
    under 50.

G4  The C2 append, as ONE equality over the whole file, in the shape
    constraint 8 states — name that paragraph, do not restate its formula.
    Report the boolean and the byte arithmetic against the C1 length you
    measure yourself. Report a SECOND, INDEPENDENT reading: split the
    committed file on blank lines, take the LAST N units, and confirm they
    equal LEDGER26's paragraphs IN ORDER, where N is the number YOUR split
    measured; give the unit count before and after, and STATE YOUR
    TRAILING-NEWLINE HANDLING, because the R21 through R25 entries all record
    that a naive split reports FALSE on a byte-perfect file. This slice
    carries MORE THAN ONE paragraph, so ORDER is load-bearing and a set
    comparison does not discharge it. NEGATIVE CONTROL: flip ONE byte inside
    the appended text; BOTH readers must reject the mutant and BOTH accept the
    true file. Do that flip in memory or under a disposable worktree per
    constraint 12, never on the tracked file.

G5  The ledger sets, base versus C2 in `.agent/live_review.md`, in the shape
    constraint 10 states — report each side of every movement it names, that
    the ids ADDED and the ids REMOVED are BOTH the EMPTY SET, and that all
    `^- R-\d+ — ` ids are DISTINCT. Report the `^Done: R-\d+ — ` ids ADDED as
    exactly `R-0682`. `^Gate: R\d+ — ` 19 → 19 UNCHANGED, and
    `^Gate: F\d+ R\d+ — ` 6 → 7, the ADDED key being exactly `F031 R25`, all
    keys DISTINCT (§3 item 26). Report the §3 item 10 open set at C2, that
    `- R-0682 — ` still occurs exactly ONCE line-anchored so its landed
    paragraph was not edited, and that `git diff --name-only` over C3 does NOT
    name `.agent/live_review.md` — the whole of constraint 8's "nothing at all
    in any other commit".

G6  THE RED PROOF, in a disposable worktree at C3 per constraint 12, so the
    primary checkout is never mutated, with vitest run from the PRIMARY
    checkout's `apps/ui` so the primary's `node_modules` resolves:
      npx vitest run --config <PRIMARY>/apps/ui/vitest.config.ts \
        --root <WORKTREE>/apps/ui src/api/
    Run it UNMUTATED first and report the file and test counts. Then, in
    `apps/ui/src/api/decisionAnswer.ts` INSIDE THAT WORKTREE, change S1's
    builder so that it returns its request body for a model that is NOT open
    instead of `null` — the one refusal whose absence a server answers 409 and
    a hurried reader never sees — leaving every other byte alone, and run the
    same line again. IT MUST GO RED. Report the REAL exit code, the NAMES of
    the failing tests, and the failure count YOUR run measured; this block
    states no number. A GREEN means S2's tests do not discriminate an open
    decision from a resolved one, and is reported as such. Remove the worktree
    BY ITS EXACT PATH and report `git worktree list` as 1 line after, naming
    that path.

G7  Structure, then the suites. Report, as counts YOU measured at C3: over
    BOTH chip files, `role="group"` exactly ONCE each and the existing
    `aria-label` still present on the SAME element — quote the element's line
    from each file; over `DecisionInboxCard.tsx`, that the `<output>` the
    previous round added is UNCHANGED and that `aria-pressed` and `aria-live`
    are each still present; over `decisionAnswer.ts`, that the literal
    `decision.resolve` occurs exactly once and the strings `fetch(`,
    `XMLHttpRequest`, `Math.random` and `Date.now` each occur ZERO times,
    which is what "pure" means here and is measurable. Then in the PRIMARY
    checkout at the C3 tree, all REAL exit 0, run SERIALLY and never two alive
    at once, with `git worktree list` reported as 1 line immediately BEFORE
    the first of them. At `apps/ui`: `npm run typecheck` with ZERO diagnostics
    on stdout and stderr; `npm run test:unit`, reporting the file and test
    counts YOUR run measured — `decisionCard.test.ts` must still be exactly
    32, `decisionFilter.test.ts` exactly 20 and `decisionOrder.test.ts`
    exactly 16, any movement in any of the three being a finding, while the
    FILE count must be exactly 24, one more than the Base's 23, that one being
    `decisionAnswer.test.ts`: report the file count, the total test count, and
    how many tests S2 added. Then in Python, by these exact command lines with
    no extra flag:
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/ui_contracts/ -q
      python3 -m pytest tests/cli/test_golden_path.py -q
    These are the four state readers a round rewriting `.agent/` state gates,
    plus `tests/ui_contracts/` — which READS `GraphFilterChips.tsx`, the file
    S3 edits — plus the canary. The reviewer ran all six at `92b323e3` with
    these exact lines and measured in that order 480, 52, 21, 16, 525 passed
    with 4 skipped, and 42, every one exit 0. Account for any difference.

G8  Markers, paths, commit shapes and object ids. Line-anchored `^<<<SLICE `
    and `^<<<END ` both 0 in `.agent/plan.md` at C1, `.agent/live_review.md`
    at C2 and every file C3 writes, against the same counts over the COMMITTED
    C0a blob as a CONTROL, where they are NOT 0. ONLY the line-anchored
    reading is ordered — this block quotes both markers inside backticks
    mid-line, so a raw SUBSTRING count is unmeetable and is NOT ordered.
    `git diff --name-only <base>..C3` names NO path under `docs/`, `packages/`
    or `tests/`, and none of `.agent/context.md`, either inventory file,
    `apps/ui/src/components/panels/RightLivePanel.tsx`,
    `apps/ui/src/api/decisionCard.ts`, `apps/ui/src/api/decisionFilter.ts`,
    `apps/ui/src/api/decisionOrder.ts` or `apps/ui/src/RemedyApp.tsx`; the
    range path set MINUS the change set is EMPTY and the change set MINUS the
    range is exactly `.agent/handoff.md`, which C4 writes. Over C0a..C3 report
    per commit that it is single-parent and its INSERTION count — the `+`
    column only, per AGENTS.md DECISION F104 D1 — each under 500; those same
    numbers fill the `+/-` column of the `## Commits` table, derived from
    `git diff --numstat` and NOT from `git commit`'s own summary, and you
    report that the two agree cell for cell (§3 item 28). Report
    `git ls-files .remedy-wt` as 0 and `git ls-files` over `*.zip` as 0. FOR
    THE REFLOG state SCOPE and FIELD: over THIS ROUND'S entries only, by the
    OPERATION PREFIX before the first colon of `git reflog --format=%gs`,
    report `amend`, `rebase` and `cherry` each 0 and how many you scoped to.
    Finally extract every SHA-shaped token from the COMMITTED C0a blob with
    the word-bounded pattern matching 7 to 40 hex characters — whose
    boundaries do NOT match the 64-char sha256 digest this block also carries
    — pass each to `git cat-file -t`, and report the token count YOUR
    extractor measured, the type per token, and the FAILING SET, which MUST BE
    EMPTY.

G9  The push. AFTER C4, run `git push origin feature/f031-decision-inbox`. No
    `--force`, no `--force-with-lease`, no history rewrite, no branch
    deletion, no pull request. THAT PUSH'S OUTCOME IS NOT A VALUE OF ANY FILE
    THIS ROUND WRITES: the reviewer measures the pushed tips at the next gate
    and records them in the R26 entry of `.agent/live_review.md`. In
    `## External actions` write the push COMMAND and that sentence. In the
    item-status table the push row is `done`, reason "ordered after C4;
    outcome carried by G9 to the reviewer". Report the real outcome in your
    final message.

── Handback ──────────────────────────────────────────────────
Rewrite `.agent/handoff.md` at C4 per docs/agents/handback_template.md:
feature and round, branch, base and commit SHAs, a changed-files table per
commit, the item-status table covering C0a through C4, S1 through S4 and the
push, ONE LINE PER GATE with its real result, the finding counts, and the next
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
section to fit; claim no token cap.

YOUR `## Next` SECTION names, in order: that the next session reads
`.agent/STOP` from disk as Phase 1 rule 1 BEFORE the Open PR Gate as rule 2;
that the R26 verdict is UNRECORDED and owed by the next round's ledger commit
(DECISION F085 D9); and that T003 continues with the sender round the plan's
Next Steps names first.

Declare every deviation, contradiction and assumption.
──────────────────────────────────────────────────────────────

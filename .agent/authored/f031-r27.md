── STEP R27 — F031 Decision inbox ────────────────────────────
Goal:        T003's DEEP LINK, at the pure layer, plus the repair R26 owed.
             A decision learns which task it is about, a resolver turns that
             into the graph node the card will jump to — following the
             resolver F021 already shipped rather than inventing a second
             mapping — and the sentence R26 falsified and could not reach is
             retired at its source.

Fortschritt: ~92 % (F031 claimed; R1 through R26 landed, R26 gated here ·
             T001 SHIPPED · T002 COMPLETE · T003 answer-command model
             shipped, deep-link seam here, sender and forms open)
             — Schaetzung

Bundle:      C0a save this block · C0b mirror it into last_block · C1 the
             plan · C2 the R26 gate entry and R-0377's recurrence · C3 the
             task linkage, the focus resolver, their tests, the falsified
             comment and DECISION F031 D12 · C4 handback.

Change set:  exactly these paths, nothing else —
             .agent/authored/f031-r27.md                             (C0a)
             .agent/last_block.md                                    (C0b)
             .agent/plan.md                                          (C1)
             .agent/live_review.md                                   (C2)
             apps/ui/src/api/decisionCard.ts                         (C3)
             apps/ui/src/api/decisionCard.test.ts                    (C3)
             apps/ui/src/api/decisionFocus.ts                        (C3, NEW)
             apps/ui/src/api/decisionFocus.test.ts                   (C3, NEW)
             .agent/decisions.md                               (C3, D12)
             .agent/handoff.md                                       (C4)
             This list bounds the round's WRITES, not its ACTIONS: the push
             named in G9 is ordered explicitly and is not a file (R-0674).
             `decisionCard.ts` IS in this list on purpose — see S1 and the
             R-0377 recurrence C2 writes.

── Base ──────────────────────────────────────────────────────
The round base is `beec7b83cb51bf4a34db82f3bb029623e14433f6`, the R26
handback commit and the tip of `feature/f031-decision-inbox`, local and remote
EQUAL — the reviewer measured both at the R26 gate. Stay on that branch; never
commit to `main`. Every SHA-shaped token here resolved under `git cat-file -t`.

Readings the reviewer MEASURED at that base, re-checkable there:
- `.agent/live_review.md` 696400 bytes and 1253 lines; `^- R-\d+ — ` 244 all
  DISTINCT, maximum `R-0683`; `^Done: R-\d+ — ` 5, so the §3 item 10 open set
  is 239; `^Recurrence: R-` 19; `^Landed: R-` 0. THE GATE SERIES IS SPLIT by
  DECISION F031 D7: `^Gate: R\d+ — ` 19, frozen, and `^Gate: F\d+ R\d+ — ` 7,
  those seven being `F031 R19` through `F031 R25`. `^Recurrence: R-0377`
  occurs 0 times: the paragraph LEDGER27 appends is the first of its key.
- `.agent/plan.md` 47 lines, 2653 bytes. `docs/roadmap/**` is UNTOUCHED, so
  the §3 docs-round gate is not earned and is not ordered.
- `apps/ui`: `npm run typecheck` exit 0, zero diagnostics on stdout and
  stderr; `npm run test:unit` exit 0 at 24 files and 374 tests, of which
  `decisionCard.test.ts` is 32, `decisionAnswer.test.ts` 17,
  `decisionFilter.test.ts` 20 and `decisionOrder.test.ts` 16.
- The Python suites, every one exit 0: `tests/ui_server/` 480,
  `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16,
  `tests/ui_contracts/` 525 passed with 4 skipped, `test_golden_path` 42.
- THE RESOLVER THIS ROUND COPIES ALREADY EXISTS and is the reason S2 invents
  nothing. `apps/ui/src/api/feedFocus.ts` exports `nodeIdForFeedRow(row, tasks)`
  returning `string | null`, and the type `FocusableTask` — exactly
  `{ id: string; nodeId: string }` — narrowed on purpose so an unrelated task
  field cannot churn it. Its own comment records that DECISION F021 D2
  REJECTED inventing a second client-side mapping for this, and that a null is
  not a failure but a row that must not OFFER the jump.
- THE DASHBOARD ALREADY CARRIES THE TASK LIST where the inbox is rendered:
  `RightLivePanel` reads `dashboard.tasks` and passes it to `ActivityFeedCard`
  and `TaskChecklistCard` beside `onSelectNode`. This round does NOT wire the
  card — it ships the resolver the wiring will call, as `decisionFilter.ts`
  shipped a view before its caller.
- THE DECISION'S TASK LINKAGE IS IN THE PAYLOAD AND NOT YET IN THE MODEL.
  `DecisionInboxEntry` types `payload?: unknown`, and the server reads that
  payload's `task_id` in `decision_inbox._blocked_subtree_size` to compute the
  blocked subtree — so the field exists on the wire and `DecisionCardModel`
  simply does not project it yet. S1 projects it.
- TWO WHOLE-MODEL EQUALITY ASSERTIONS GUARD THAT MODEL'S KEY SET (§3 item 7),
  at `apps/ui/src/api/decisionCard.test.ts` lines 164 and 188, each a
  `expect(buildDecisionCardModel(...)).toEqual({ ... })` over EVERY key. A new
  field breaks BOTH unless both gain it. That file is in the change set and S3
  orders the update; this is named here because a block that adds a field
  without naming its shape guards makes the worker discover a red suite.
- THIS BLOCK'S OWN TWO CAPS, measured on its final bytes before emission and
  stated so your re-measurement can disagree with the reviewer's, are 490
  lines TOTAL (DECISION F085 D6) and 400 lines PROSE (DECISION F085 D5). G2
  orders you to report both from the COMMITTED blob.

── Constraints ───────────────────────────────────────────────
1. Apply every authored SLICE BYTE FOR BYTE. Never retype, rewrap or "fix"
   one. If a slice looks wrong, apply it verbatim and DECLARE the
   disagreement: a contradiction in this block is the reviewer's defect.
2. THE PRODUCTION CHANGE, ITS TESTS AND DECISION D12 ARE DESCRIBED, NOT
   SLICED. The numbered specification S1 through S4 fixes behaviour,
   structure and copy; YOU write that code, those tests and that decision
   entry under AGENTS.md's Mandatory Self-Review Loop and its File Editing
   Safety Rules. Where the spec is silent, prefer the idiom the neighbouring
   module already uses. Where the spec is WRONG, say so in the handback and
   do the right thing.
3. Slice transport. The reviewer's original is on disk at
   `.remedy-wt/f031-r27.md`. COPY that file to `.agent/authored/f031-r27.md`
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
7. The slices this block carries are the whole text PLANF031R27 and the
   appended text LEDGER27. This paragraph names them and states no count; G2
   orders you to report the count YOUR extractor measured.
8. THE ONE APPEND'S SHAPE, STATED ONCE HERE, WITH EVERY GATE NAMING THIS
   PARAGRAPH RATHER THAN RESTATING IT. Under the newline-INCLUDED convention
   each slice already ends in a newline, so `.agent/live_review.md` after C2
   is EXACTLY: its blob at C1, then one newline, then LEDGER27 — and it
   receives NOTHING ELSE in that commit, and nothing at all in any other
   commit of this round (R-0657). LEDGER27's own paragraph count is yours to
   measure; this paragraph states no number. `.agent/decisions.md` also GROWS
   at C3, by text YOU author under S4, so no equality gate is ordered over it
   and none may be reported.
9. THIS BLOCK CARRIES NO FROM/TO PAIR, so no containment test is reported and
   no FROM-zero count is ordered (§3 item 15). The plan is a WHOLE-FILE
   replacement and LEDGER27 is an append.
10. THIS ROUND MINTS NO FINDING ID AND RESOLVES NONE. LEDGER27 carries no
    `- R-` paragraph and no `Done:` line, so `^- R-\d+ — ` stays 244 with the
    maximum still `R-0683` and `^Done: R-\d+ — ` stays 5, leaving the §3 item
    10 open set UNCHANGED at 239. It carries one `Recurrence:` line, so
    `^Recurrence: R-` moves 19 → 20. `^Landed: R-` stays 0: WRITE NO `Landed:`
    LINE, and write no `Done:` line either — R-0377 stays OPEN on purpose,
    because this round widens its evidence rather than discharging it. No
    landed finding paragraph is edited (§3 item 20).
11. TOUCH NO DOCUMENT AND NO OTHER CODE. Nothing under `docs/`, `packages/`
    or `tests/`, and neither `.agent/context.md` nor either
    `f031_*_inventory.md`. Inside `apps/` only the four paths the change set
    names are written — NOT `decisionAnswer.ts`, `decisionFilter.ts`,
    `decisionOrder.ts`, `feedFocus.ts`, `remedyApi.ts`, `RightLivePanel.tsx`,
    `DecisionInboxCard.tsx` or any other test file. THIS ROUND WIRES NOTHING:
    if you find yourself editing a component to make the resolver reachable,
    stop — that is the sender round's work and the plan says so.
12. Destructive verification runs ONLY in a disposable `git worktree` under
    `.remedy-wt/`, removed BY ITS EXACT PATH (R-0662) and before the G7
    suites. Everything already there is pre-existing scratch belonging to no
    commit, this block's own file included: create no worktree at an existing
    path, and delete nothing you did not create.

── Specification (S1–S4) — the production change ─────────────
S1  THE TASK LINKAGE, in `apps/ui/src/api/decisionCard.ts`. `DecisionCardModel`
    gains ONE field: the id of the task the decision is about, a `string`,
    projected by `buildDecisionCardModel` out of the entry's `payload` under
    the payload's OWN key spelling `task_id` — the spelling
    `decision_inbox._blocked_subtree_size` reads on the server, and DECISION
    F031 D1 rules that the browser and the CLI describe one thing one way.
    Total by construction, like every other field of that model: a payload
    that is absent, is not an object, or carries a non-string `task_id` gives
    the EMPTY STRING, never `undefined` and never a throw. Name the field for
    what it holds in this module's existing camelCase idiom, put the one-line
    WHY comment directly above the projection, and change NO other field.
    THEN REPAIR THAT FILE'S FALSIFIED SENTENCE, which R26 could not reach.
    Its header still reads "What is still genuinely absent everywhere is
    ANSWERING, which is T003's." R26 landed `./decisionAnswer.ts`, which
    builds the answer command, so "everywhere" is false. Rewrite the sentence
    for what is true at this commit: the answer COMMAND is built in
    `./decisionAnswer.ts`, and what is still absent is the SEND — nothing in
    this browser posts that body yet. Keep the sentence's shape as a
    deliberate-absence note naming where the thing now IS, per AGENTS.md's
    Code Discoverability rules.

S2  THE FOCUS RESOLVER, a NEW module `apps/ui/src/api/decisionFocus.ts`,
    written to be the sibling of `apps/ui/src/api/feedFocus.ts` and not a
    second design. It exports ONE function: given a decision — take only the
    field S1 adds, in the `Pick<...>` idiom `nodeIdForFeedRow` already uses,
    so an unrelated model field cannot churn it — and the readonly task list
    the dashboard carries, it returns the graph node id that decision jumps
    to, or `null`. IMPORT `FocusableTask` FROM `./feedFocus` rather than
    declaring a second type of that shape: one spelling per concept is
    AGENTS.md's rule and a duplicate would be the exact second mapping
    DECISION F021 D2 rejected. A decision with an empty task id answers
    `null`; a task id matching no task in the list answers `null`; a match
    answers that task's `nodeId`. Say in the WHY comment that a null is NOT a
    failure — it is a card that must not OFFER the jump rather than one that
    jumps somewhere arbitrary — and that no clock, no fetch and no component
    belong in this module.

S3  THE TESTS, in two places.
    (a) `apps/ui/src/api/decisionCard.test.ts` gains coverage for S1's field:
        that a well-formed payload projects the id; that an absent payload, a
        non-object payload and a non-string `task_id` each give the empty
        string. THE TWO WHOLE-MODEL `toEqual` ASSERTIONS the Base names, at
        lines 164 and 188 of that file at the base commit, MUST gain the new
        key — re-grep both before editing, because S1's own edit moves those
        line numbers (§3 item 9). Change nothing else in that file.
    (b) `apps/ui/src/api/decisionFocus.test.ts`, NEW, following
        `feedFocus.test.ts`'s idiom if one exists and `decisionCard.test.ts`'s
        otherwise: the three answers S2 names — matched, unmatched, empty id —
        plus that the resolver reads the task id rather than the decision's
        own `id`, pinned by a case where the two DIFFER and only the task id
        matches a task. Build models through `buildDecisionCardModel` so the
        tests pin the SEAM. Name each test for the property it pins.

S4  DECISION F031 D12, appended to `.agent/decisions.md` in the shape D1
    through D11 already use there. CHOSEN: the decision's deep link resolves
    through the dashboard's OWN task list by task id, reusing `feedFocus.ts`'s
    `FocusableTask` and its null-means-no-jump contract, because DECISION
    F021 D2 already rejected a second client-side mapping for the activity
    feed and the same reasoning binds here. CHOSEN: the model projects
    `task_id` as a plain string field rather than the whole payload, so the
    card never reads an untyped blob and the resolver stays narrow.
    ALTERNATIVE: matching a decision's own id against the graph, rejected
    because a decision id is not a node id and nothing on the wire relates
    them. REVERSE it by projecting the payload wholesale once a card needs
    more of it than the task id.

── Authored slices ───────────────────────────────────────────

<<<SLICE PLANF031R27
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1–D12.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R27 ships T003's DEEP-LINK seam at the pure layer: the model learns the task a
decision is about, `decisionFocus.ts` turns that into the graph node the card
will jump to — the resolver `feedFocus.ts` already proved — and the sentence R26
falsified in `decisionCard.ts` is retired at its source.

## Next Steps
1. T003's SENDER round, which needs a design ruling first: the browser holds
   NO bearer token and NO `X-Remedy-CSRF` value today, and how one reaches the
   page is a decision that spans the server and the shell. Rule it, then wire
   the body `decisionAnswer.ts` builds, and wire the resolver R27 ships.
2. T003's remainder: the clarification form — whose input must TRIM, since the
   builder refuses only the empty string — and the ruling on
   `NeedsAttentionCard`'s decision branch (DECISION F031 D4).
3. The integration-gate round per `docs/agents/integration_gate.md`, whose
   block also carries the §3 checklist item R-0683 routes there, then closure
   per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- NOTHING CALLS THE RESOLVER YET, exactly as nothing called `decisionInboxView`
  for a round. That is deliberate under DECISION F031 D5 — the seam ships
  tested, the wiring follows — but it means `tsc` and review, not a test, are
  what will catch a mis-wired call site.
- A WHITESPACE-ONLY ANSWER IS STILL BUILT, not refused: `decisionAnswer.ts`
  compares against the empty string exactly, so the form round owes the trim.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 239 at `beec7b83` and this round leaves it there, minting nothing and
  resolving nothing; R-0377 gains a recurrence and stays OPEN.
- The findings THIS FEATURE MUST STILL ACT ON are R-0377, R-0403, R-0413,
  R-0431, R-0441, R-0445, R-0471, R-0495, R-0533, R-0574, R-0593, R-0601,
  R-0622, R-0625, R-0632, R-0672, R-0674, R-0675, R-0676, R-0677, R-0678,
  R-0679 and R-0683; R-0495 and R-0574 are the two Highs.
- BLOCK CAPS ARE TWO, not one: 490 lines TOTAL (DECISION F085 D6) and 400 lines
  PROSE (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R27

<<<SLICE LEDGER27
Gate: F031 R26 — the F031 R26 entry. R26 PASSED ON EVERY ONE OF ITS NINE GATES, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk rather than reading the handback back; every value that handback states reproduced exactly. TRANSPORT HELD IN ITS STRONGEST FORM, cmp-against-scratchpad rather than the digest fallback: the reviewer's own `.remedy-wt/f031-r26.md`, the C0a blob committed at `9ea82d68`, the C0b blob committed at `40df4b16` and `.agent/last_block.md` read off disk at `beec7b83` are ALL FOUR byte-identical at sha256 `dbf5fbe2f657a7191d197a4be5767664604a86103ca22d4c48e165ec70290bde` over 38200 bytes and 448 lines, C0a and C0b resolving to the SAME git blob `970f470292593aa1ad6f097b081c9d9a990c3e65`. THE EXTRACTION printed 2 slices, 50 content lines and 448 total, so PROSE was 398 against the 400-line cap DECISION F085 D5 sets and TOTAL 448 against the 490 DECISION F085 D6 sets. THE PLAN at `7019185f` equals PLANF031R26 exactly at 2653 bytes and 47 lines, with the trailing-newline-removed control FALSE, `^## Goal$` 1 and `^## Next Steps$` 1, and 47 strictly under the 50 AGENTS.md sets. THE C2 APPEND SATISFIED WHOLE-FILE EQUALITY: `.agent/live_review.md` at `b313d680` is its C1 blob plus one newline plus LEDGER26, at 687558 + 1 + 8841 = 696400 against an actual 696400, and the SECOND, INDEPENDENT READER AGREED — a blank-line split moves the unit count 311 to 313 and its last 2 units equal that slice's 2 paragraphs IN ORDER, trailing newlines rstripped on BOTH sides. THE NEGATIVE CONTROL WAS RUN IN MEMORY, never on disk: both readers REJECT the one-byte mutant and both ACCEPT the true file. THE SETS MOVED EXACTLY WHERE THAT BLOCK'S CONSTRAINT 10 ALLOWED AND NOWHERE ELSE: `^- R-\d+ — ` 244 to 244 with the ids ADDED and the ids REMOVED BOTH the EMPTY SET and all DISTINCT, maximum `R-0683` unmoved; `^Done: R-\d+ — ` 4 to 5 with the id added exactly `R-0682`; `^Landed: R-` 0 to 0, `^Recurrence: R-` 19 to 19; `^Gate: R\d+ — ` 19 to 19 frozen and `^Gate: F\d+ R\d+ — ` 6 to 7, the added key exactly `F031 R25`, all keys DISTINCT. The §3 item 10 open set is 239 at `b313d680`, and `- R-0682 — ` still occurs exactly ONCE line-anchored, so its landed paragraph was not edited when it was resolved. THE RED PROOF IS THE REVIEWER'S OWN, run in a disposable worktree at `069f744c` created at a path that did not exist and removed BY THAT EXACT PATH, with `git worktree list` 1 line and `git status --porcelain` 0 after: the not-open refusal occurs EXACTLY ONCE in the module, UNMUTATED gives exit 0 at 21 files and 349 tests, and with that refusal DELETED the run goes REAL exit 1 at 2 failed and 347 passed, the two being `refuses a decision that is NOT open, which the server answers 409` and `reads isOpen rather than an open-SOUNDING status string` — cell for cell what that handback reports; the file was restored byte-identically inside the worktree before removal. THE SUITES ARE THE REVIEWER'S OWN, run SERIALLY, never two alive at once, every one a REAL exit 0: `npm run typecheck` with zero diagnostics on stdout and stderr, `npm run test:unit` at 24 files and 374 tests — one file and 17 tests more than the base, that file being `decisionAnswer.test.ts` — with `decisionCard.test.ts` 32, `decisionFilter.test.ts` 20 and `decisionOrder.test.ts` 16 all UNMOVED, then `tests/ui_server/` 480, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16, `tests/ui_contracts/` 525 passed with 4 skipped and the canary `test_golden_path` 42, every count identical to the base reading. THE PRODUCTION CHANGE IS WHAT S1 THROUGH S3 ORDERED: `decisionAnswer.ts` carries the literal `decision.resolve` exactly once and the strings `fetch(`, `XMLHttpRequest`, `Math.random`, `Date.now` and `await ` ZERO times each, which is what PURE means here and is measurable rather than asserted; the builder's four refusals are the four S1 named, in that order; no `source` key is sent, per DECISION F009 D22; and `role="group"` occurs exactly ONCE in each chip file, on the SAME element as the existing `aria-label`, with the `<output>` R25 added byte-identical to its previous form and `aria-pressed` and `aria-live` each still present. HYGIENE HELD: line-anchored `^<<<SLICE ` and `^<<<END ` are 0 in `.agent/plan.md` at `7019185f`, `.agent/live_review.md` at `b313d680` and all five files C3 writes, against a CONTROL of 2 and 2 over the C0a blob; the range `92b323e3`..`069f744c` names 9 paths, none under `docs/`, `packages/` or `tests/` and none of the forbidden set, with range-minus-change-set EMPTY and change-set-minus-range exactly `.agent/handoff.md`; the five commits `9ea82d68` through `069f744c` are each SINGLE-PARENT with insertions 448, 347, 23, 4 and 277 read from `git diff --numstat`, each under the 500 cap AGENTS.md DECISION F104 D1 sets; `git ls-files .remedy-wt` 0, the zip glob 0, `git worktree list` 1 line and `git status --porcelain` 0. THE BLOCK'S OWN OBJECT IDS RESOLVE: 20 SHA-shaped occurrences, 10 distinct, failing set EMPTY, 9 `commit` and 1 `blob`. THE PUSH DISCHARGED: `refs/heads/feature/f031-decision-inbox` and the local tip are both `beec7b83cb51bf4a34db82f3bb029623e14433f6`, no pull request was created, no branch deleted and nothing merged. THE HANDBACK'S OVERAGE IS DECLARED AND PERMITTED: 136 lines against the 100-line tier its 6 commits earn, carrying the DECISION D15 stated-cause line that names the count and the mandated content behind it, with no section dropped — which AGENTS.md's `### handoff.md` allows explicitly and which is therefore NOT a finding. THE FIVE DECLARED ITEMS ARE ADJUDICATED. Items 4 and 5 are the block being obeyed and the cap rule being followed, and are not deviations at all. ITEM 2 IS CORRECT: the falsified header sentence in `DecisionInboxCard.tsx` was falsified by S1's new module rather than by S3's attribute, the file was already in the change set, and repairing it there is the R-0593 class being closed rather than widened. ITEM 3 IS A REAL GAP AND IS ROUTED, NOT DISMISSED: the builder compares against the empty string exactly, so a whitespace-only answer is built rather than refused; nothing can produce one today, because the answer buttons ship DISABLED and no form exists, so the obligation lands on T003's form round and `.agent/plan.md` carries it as a risk from this round's C1. ITEM 1 IS THE REVIEWER'S OWN DEFECT and is the recurrence appended beside this entry. THE VERDICT IS PASS.

Recurrence: R-0377 — SECOND INSTANCE, and the first outside `.agent/plan.md`: the R26 block's constraint 11 excluded `apps/ui/src/api/decisionCard.ts` from a change set enforced as exhaustive, while that same block's S1 ordered a new module whose EXISTENCE falsified a sentence in that excluded file. MEASURED at `beec7b83`: `decisionCard.ts` still reads "What is still genuinely absent everywhere is ANSWERING, which is T003's", and `apps/ui/src/api/decisionAnswer.ts` — which builds the decision-answer command body — landed at `069f744c` in that very round, so "everywhere" was false the moment the round ended. The worker measured it, declared it, and correctly did NOT widen its change set to fix it, which is exactly what R-0377 says an honest worker can only do. WHY THIS IS A RECURRENCE AND NOT A NEW ID, per §3 item 30: R-0377 is OPEN and already names this cause in general terms — "change-set gates are written by listing the files the round's ITEMS touch, and the files a round's CONSEQUENCES touch are then absent from a list that is enforced as exhaustive" — and this instance is that sentence with a source file in place of a state file, so a second id would be two things to resolve for one defect. WHAT THIS INSTANCE ADDS. R-0377's counter-measure was narrowed to `.agent/plan.md` and promoted to §3 checklist item 23 in that form, which reaches the finding ledger and nothing else; it does not reach a DELIBERATE-ABSENCE COMMENT in a source file, which is the R-0593 class arriving through a change set rather than through neglect. The widened counter-measure owed to §3 is therefore: before emitting a block, read every ABSENCE claim in every file the block's own new code makes false — not only the files the block WRITES — and either add that file to the change set or state in the block why the repair is deferred and to which round. THAT EDIT IS ROUTED TO THE INTEGRATION-GATE ROUND'S BLOCK, beside the item R-0683 already routes there, so it does not become the finding body it is warning about. THE INSTANCE ITSELF IS REPAIRED BY THE ROUND THIS ENTRY'S BLOCK ORDERS: S1 names `decisionCard.ts` in the change set and retires the sentence, which is why R-0377 gains evidence here and is not resolved — the CLASS is still open until the checklist item lands.
<<<END LEDGER27

── Done when ─────────────────────────────────────────────────
Run every gate yourself, record its REAL exit code and REAL output, and report
ONE LINE PER GATE in the handback, transcripts kept out (R-0582). "Green" as a
word is a finding. Every gate runs at a commit STRICTLY EARLIER than C4 (§3
item 31); G9's push runs after it and names its carrier.

G1  Branch, cleanliness, transport. `git branch --show-current` prints
    `feature/f031-decision-inbox` and NOT `main`; `.agent/STOP` read from disk
    is ABSENT before C0a and again before C4; `git status --porcelain` line
    count after each of C0a, C0b, C1, C2 and C3 is 0. Then report sha256, byte
    count and line count for FOUR readings — `.remedy-wt/f031-r27.md` before
    C0a, the committed C0a blob, the committed C0b blob, and
    `.agent/last_block.md` off disk after C0b — ALL FOUR EQUAL, and the git
    blob id of C0a's and C0b's file, the SAME id.

G2  Extraction and the block's own two caps. Run your extractor over the
    COMMITTED C0a blob and report the slice count, the CONTENT lines inside
    markers, and the TOTAL — the numbers YOUR extractor printed — then PROSE
    as TOTAL minus CONTENT, against the two caps the Base names. If either is
    exceeded say so plainly and continue; it is not yours to fix.

G3  The plan. `.agent/plan.md` at C1 is byte-equal to PLANF031R27 under your
    stated newline convention; report slice length, file length and
    convention. NEGATIVE CONTROL: NOT byte-equal to that slice MINUS its
    trailing newline. `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` STRICTLY
    under 50.

G4  The C2 append, as ONE equality over the whole file, in the shape
    constraint 8 states — name that paragraph, do not restate its formula.
    Report the boolean and the byte arithmetic against the C1 length you
    measure yourself. Report a SECOND, INDEPENDENT reading: split the
    committed file on blank lines, take the LAST N units, and confirm they
    equal LEDGER27's paragraphs IN ORDER, where N is the number YOUR split
    measured; give the unit count before and after, and STATE YOUR
    TRAILING-NEWLINE HANDLING, because the R21 through R26 entries all record
    that a naive split reports FALSE on a byte-perfect file. This slice
    carries MORE THAN ONE paragraph, so ORDER is load-bearing and a set
    comparison does not discharge it. NEGATIVE CONTROL: flip ONE byte inside
    the appended text; BOTH readers must reject the mutant and BOTH accept the
    true file. Do that flip in memory or under a disposable worktree per
    constraint 12, never on the tracked file.

G5  The ledger sets, base versus C2 in `.agent/live_review.md`, in the shape
    constraint 10 states — report each side of every movement it names, that
    the `- R-` ids ADDED and REMOVED are BOTH the EMPTY SET, that all
    `^- R-\d+ — ` ids are DISTINCT, and that the `^Done: R-\d+ — ` ids ADDED
    are ALSO the EMPTY SET. `^Gate: R\d+ — ` 19 → 19 UNCHANGED, and
    `^Gate: F\d+ R\d+ — ` 7 → 8, the ADDED key being exactly `F031 R26`, all
    keys DISTINCT (§3 item 26). Report `^Recurrence: R-` 19 → 20 and that
    `^Recurrence: R-0377` moves 0 → 1. Report the §3 item 10 open set at C2,
    that `- R-0377 — ` still occurs exactly ONCE line-anchored so its landed
    paragraph was not edited, and that `git diff --name-only` over C3 does NOT
    name `.agent/live_review.md` — the whole of constraint 8's "nothing at all
    in any other commit".

G6  THE RED PROOF, in a disposable worktree at C3 per constraint 12, so the
    primary checkout is never mutated, with vitest run from the PRIMARY
    checkout's `apps/ui` so the primary's `node_modules` resolves:
      npx vitest run --config <PRIMARY>/apps/ui/vitest.config.ts \
        --root <WORKTREE>/apps/ui src/api/
    Run it UNMUTATED first and report the file and test counts. Then, in
    `apps/ui/src/api/decisionFocus.ts` INSIDE THAT WORKTREE, change S2's
    resolver so that it returns the decision's task id itself instead of the
    matched task's `nodeId` — the confusion a deep link would most plausibly
    ship, since the two are both non-empty strings and `tsc` cannot tell them
    apart — leaving every other byte alone, and run the same line again. IT
    MUST GO RED. Report the REAL exit code, the NAMES of the failing tests,
    and the failure count YOUR run measured; this block states no number. A
    GREEN means S3(b)'s tests never distinguish a task id from a node id, and
    is reported as such. Remove the worktree BY ITS EXACT PATH and report
    `git worktree list` as 1 line after, naming that path.

G7  Structure, then the suites. Report, as counts YOU measured at C3: over
    `decisionFocus.ts`, that `FocusableTask` is IMPORTED from `./feedFocus`
    and that the file declares no type of its own by that name — quote the
    import line — and that `fetch(`, `Date.now` and `useState` each occur ZERO
    times; over `decisionCard.ts`, that the falsified sentence S1 names is
    GONE, by reporting that the exact string `absent everywhere is ANSWERING`
    occurs 0 times, and that the new field's key appears in the model
    interface exactly once. Then in the PRIMARY checkout at the C3 tree, all
    REAL exit 0, run SERIALLY and never two alive at once, with
    `git worktree list` reported as 1 line immediately BEFORE the first of
    them. At `apps/ui`: `npm run typecheck` with ZERO diagnostics on stdout
    and stderr; `npm run test:unit`, reporting the file and test counts YOUR
    run measured — `decisionAnswer.test.ts` must still be exactly 17,
    `decisionFilter.test.ts` exactly 20 and `decisionOrder.test.ts` exactly
    16, any movement in any of the three being a finding, while the FILE count
    must be exactly 25, one more than the Base's 24, that one being
    `decisionFocus.test.ts`; report `decisionCard.test.ts`'s count against the
    Base's 32 and how many tests S3(a) added, and the new file's own count.
    Then in Python, by these exact command lines with no extra flag:
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/ui_contracts/ -q
      python3 -m pytest tests/cli/test_golden_path.py -q
    These are the four state readers a round rewriting `.agent/` state gates,
    plus `tests/ui_contracts/`, plus the canary. The reviewer ran all six at
    `beec7b83` with these exact lines and measured in that order 480, 52, 21,
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
    `apps/ui/src/api/decisionAnswer.ts`, `apps/ui/src/api/feedFocus.ts`,
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
    `git ls-files` over `*.zip` as 0. FOR THE REFLOG state SCOPE and FIELD:
    over THIS ROUND'S entries only, by the OPERATION PREFIX before the first
    colon of `git reflog --format=%gs`, report `amend`, `rebase` and `cherry`
    each 0 and how many you scoped to. Finally extract every SHA-shaped token
    from the COMMITTED C0a blob with the word-bounded pattern matching 7 to 40
    hex characters — whose boundaries do NOT match the 64-char sha256 digest
    this block also carries — pass each to `git cat-file -t`, and report the
    token count YOUR extractor measured, the type per token, and the FAILING
    SET, which MUST BE EMPTY.

G9  The push. AFTER C4, run `git push origin feature/f031-decision-inbox`. No
    `--force`, no `--force-with-lease`, no history rewrite, no branch
    deletion, no pull request. THAT PUSH'S OUTCOME IS NOT A VALUE OF ANY FILE
    THIS ROUND WRITES: the reviewer measures the pushed tips at the next gate
    and records them in the R27 entry of `.agent/live_review.md`. In
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
that the R27 verdict is UNRECORDED and owed by the next round's ledger commit
(DECISION F085 D9); and that T003's sender round needs the token-delivery
ruling the plan's Next Steps names before any wiring is written.

Declare every deviation, contradiction and assumption.
──────────────────────────────────────────────────────────────

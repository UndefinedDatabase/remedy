── STEP R30 — F031 Decision inbox ────────────────────────────
Goal:        Record R29's PASS and give the deep-link resolver R27 shipped its
             FIRST CALLER. A decision card that names a task the dashboard
             carries gains a control that jumps to that task's graph node;
             one that names no task, or names a task this dashboard lacks,
             gains nothing at all — the affordance never lies.

Fortschritt: ~95 % (F031 claimed; R1 through R29 landed, R29 gated here ·
             T001 SHIPPED · T002 COMPLETE · T003 answer command, request and
             deep-link seams shipped, deep link WIRED here, send open)
             — Schaetzung

Bundle:      C0a save this block · C0b mirror it into last_block · C1 the
             plan · C2 the R29 gate entry · C3 the panel hand-down, the card's
             jump control, its style and DECISION F031 D15 · C4 handback.

Change set:  exactly these paths, nothing else —
             .agent/authored/f031-r30.md                             (C0a)
             .agent/last_block.md                                    (C0b)
             .agent/plan.md                                          (C1)
             .agent/live_review.md                                   (C2)
             apps/ui/src/components/panels/RightLivePanel.tsx        (C3)
             apps/ui/src/components/panels/DecisionInboxCard.tsx     (C3)
             apps/ui/src/components/panels/RightLivePanel.module.css (C3)
             .agent/decisions.md                               (C3, D15)
             .agent/handoff.md                                       (C4)
             This list bounds the round's WRITES, not its ACTIONS: the push
             named in G9 is ordered explicitly and is not a file (R-0674).

── Base ──────────────────────────────────────────────────────
The round base is `def633e988f638efb2db2d816c720f419400b9bb`, the R29 handback
commit and the tip of `feature/f031-decision-inbox`, local and remote EQUAL —
the reviewer measured both at the R29 gate. Stay on that branch; never commit
to `main`. Every SHA-shaped token here resolved under `git cat-file -t`.

Readings the reviewer MEASURED at that base, re-checkable there:
- `.agent/live_review.md` 729516 bytes and 1269 lines; `^- R-\d+ — ` 246 all
  DISTINCT, maximum `R-0685`; `^Done: R-\d+ — ` 5, so the §3 item 10 open set
  is 241; `^Recurrence: R-` 22; `^Landed: R-` 0. THE GATE SERIES IS SPLIT by
  DECISION F031 D7: `^Gate: R\d+ — ` 19, frozen, and `^Gate: F\d+ R\d+ — ` 10,
  those ten being `F031 R19` through `F031 R28`. THIS ROUND MINTS NO ID.
- `.agent/plan.md` 47 lines, 2734 bytes. `docs/roadmap/**` is UNTOUCHED, so
  the §3 docs-round gate is not earned and is not ordered.
- `apps/ui`: `npm run typecheck` exit 0, zero diagnostics on stdout and
  stderr; `npm run test:unit` exit 0 at 26 files and 400 tests, of which
  `decisionCard.test.ts` is 36, `decisionAnswer.test.ts` 20,
  `decisionFilter.test.ts` 20, `decisionOrder.test.ts` 16,
  `decisionFocus.test.ts` 7 and `decisionSend.test.ts` 12.
- The six Python suites all exit 0; their counts are stated ONCE, in G7.
- THE PANEL ALREADY HOLDS BOTH VALUES S1 HANDS DOWN, which is why S1 is one
  line. `RightLivePanel` destructures `dashboard` and `onSelectNode`, and
  already passes `dashboard.tasks` and `onSelectNode` to `ActivityFeedCard`
  and `TaskChecklistCard` on the two lines beneath the `DecisionInboxCard`
  line. Nothing new is threaded from `RemedyApp`, which this round leaves
  untouched.
- THE RESOLVER IS READY AND UNCALLED. `apps/ui/src/api/decisionFocus.ts`
  exports `nodeIdForDecisionCard(decision, tasks)`, taking
  `Pick<DecisionCardModel, "taskId">` and a readonly `FocusableTask[]` and
  answering `string | null`. Its own comment fixes the contract S2 must
  honour: a null is NOT a failure, it is a card that must not OFFER the jump.
- THE FEED'S IDIOM CANNOT BE COPIED WHOLE. `ActivityFeedCard` makes the
  ENTIRE row a `<button>` when its row resolves, under the comment "Only a
  row that can really jump becomes a button, so the affordance never lies". A
  decision row already CONTAINS the answer buttons, so wrapping it would nest
  interactive controls — invalid HTML, unreachable by keyboard. The RULE is
  copied; the SHAPE is not, and DECISION F031 D15 records that.
- THE CSS RULE THAT GOVERNS S3, and why no new token is minted. Finding
  R-0661 and `tests/ui_contracts/test_design_drift.py`'s
  `TestEveryCustomPropertyResolves` scan every `.css` under `apps/ui/src` and
  fail when a `var(--remedy-…)` resolves to nothing outside a four-name
  allowlist. The reviewer verified at this base that `--remedy-radius-pill`,
  `--remedy-bg-2`, `--remedy-line`, `--remedy-line-strong`, `--remedy-muted`,
  `--remedy-ink` and `--remedy-blue-strong` are ALL defined in
  `apps/ui/src/styles/tokens.css`, so S3 needs none. Do NOT name
  `--remedy-focus`: the neighbouring `.decisionFilterChip:focus-visible`
  block records that the sheet never adopted it and that naming it would drop
  the declaration.
- THIS BLOCK'S OWN TWO CAPS, measured on its final bytes before emission and
  stated so your re-measurement can disagree with the reviewer's, are 490
  lines TOTAL (DECISION F085 D6) and 400 lines PROSE (DECISION F085 D5). G2
  orders you to report both from the COMMITTED blob.

── Constraints ───────────────────────────────────────────────
1. Apply every authored SLICE BYTE FOR BYTE. Never retype, rewrap or "fix"
   one. If a slice looks wrong, apply it verbatim and DECLARE the
   disagreement: a contradiction in this block is the reviewer's defect.
2. THE PRODUCTION CHANGE AND DECISION D15 ARE DESCRIBED, NOT SLICED. The
   numbered specification S1 through S4 fixes behaviour, structure and copy;
   YOU write that code and that decision entry under AGENTS.md's Mandatory
   Self-Review Loop and its File Editing Safety Rules. Where the spec is
   silent, prefer the idiom the neighbouring module already uses. Where the
   spec is WRONG, say so in the handback and do the right thing.
3. Slice transport. The reviewer's original is on disk at
   `.remedy-wt/f031-r30.md`. COPY that file to `.agent/authored/f031-r30.md`
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
7. The slices this block carries are the whole text PLANF031R30 and the
   appended text LEDGER30. This paragraph names them and states no count; G2
   orders you to report the count YOUR extractor measured.
8. THE ONE APPEND'S SHAPE, STATED ONCE HERE, WITH EVERY GATE NAMING THIS
   PARAGRAPH RATHER THAN RESTATING IT. Under the newline-INCLUDED convention
   each slice already ends in a newline, so `.agent/live_review.md` after C2
   is EXACTLY: its blob at C1, then one newline, then LEDGER30 — and it
   receives NOTHING ELSE in that commit, and nothing at all in any other
   commit of this round (R-0657). LEDGER30's own paragraph count is yours to
   measure; this paragraph states no number. `.agent/decisions.md` also GROWS
   at C3, by text YOU author under S4, so no equality gate is ordered over it
   and none may be reported.
9. THIS BLOCK CARRIES NO FROM/TO PAIR, so no containment test is reported and
   no FROM-zero count is ordered (§3 item 15). The plan is a WHOLE-FILE
   replacement and LEDGER30 is an append.
10. THIS ROUND MINTS NO FINDING ID AND RESOLVES NONE. LEDGER30 carries no
    `- R-` paragraph, no `Done:` line and no `Recurrence:` line, so
    `^- R-\d+ — ` stays 246 with the maximum still `R-0685`,
    `^Done: R-\d+ — ` stays 5, `^Recurrence: R-` stays 22 and `^Landed: R-`
    stays 0 — WRITE NO `Landed:` LINE — leaving the §3 item 10 open set
    UNCHANGED at 241. No landed finding paragraph is edited (§3 item 20).
11. TOUCH NO DOCUMENT AND NO OTHER CODE. Nothing under `docs/`, `packages/`
    or `tests/`, and neither `.agent/context.md` nor either
    `f031_*_inventory.md`. Inside `apps/` ONLY the three paths the change set
    names are written — NOT `RemedyApp.tsx`, `ActivityFeedCard.tsx`,
    `TaskChecklistCard.tsx`, `decisionCard.ts`, `decisionFocus.ts`,
    `decisionAnswer.ts`, `decisionSend.ts`, `feedFocus.ts`, `remedyApi.ts`,
    `tokens.css` or ANY test file. THIS ROUND STILL SENDS NOTHING: write no
    `fetch`, mint no nonce, and do not enable the answer buttons.
12. Destructive verification runs ONLY in a disposable `git worktree` under
    `.remedy-wt/`, removed BY ITS EXACT PATH (R-0662) and before the G7
    suites. Everything already there is pre-existing scratch belonging to no
    commit, this block's own file included: create no worktree at an existing
    path, and delete nothing you did not create.

── Specification (S1–S4) — the production change ─────────────
S1  THE HAND-DOWN, in `RightLivePanel.tsx`. The `DecisionInboxCard` element
    gains `tasks` and `onSelectNode`, taking the SAME two expressions the
    `ActivityFeedCard` element on the next line already passes — read them
    off that line rather than inventing them. Change nothing else in the
    file: no new prop on the panel itself, no import, no reordering.

S2  THE JUMP CONTROL, in `DecisionInboxCard.tsx`.
    (a) The component's props gain the task list and the node-selecting
        callback, typed as `ActivityFeedCard` types its own — import the
        `FocusableTask` TYPE from `../../api/feedFocus` rather than declaring
        a second shape, per AGENTS.md's one-spelling-per-concept rule.
    (b) For each rendered decision, resolve its node with
        `nodeIdForDecisionCard` imported from `../../api/decisionFocus`.
        Resolve it ONCE per decision, beside the existing per-decision work.
    (c) A NON-NULL node renders ONE button inside the existing
        `.decisionChips` row, after the three chips already there, whose
        click calls the callback with that node id. A NULL node renders
        NOTHING — no disabled control, no placeholder. That is the resolver's
        own contract and the feed's rule both; a card that cannot jump must
        not appear to offer it.
    (d) THE BUTTON'S LABEL IS THIS FILE'S OWN, so name it as a `const` beside
        `ANSWER_PENDING_TITLE`, `FILTER_CHIPS_LABEL` and `OPEN_COUNT_LABEL`,
        in that idiom, with an `aria-label` or `title` saying where it goes
        rather than repeating the visible word. Keep it chip-row short.
    (e) REPAIR THE HEADER'S PROJECTION SENTENCE, which this control falsifies.
        It currently claims the component "adds nothing of its own: every
        string it displays is a FIELD — of a model, or of a chip
        `decisionFilter.ts` derived — never a value this file chose." Rewrite
        it to state what is true and already was: the displayed CONTENT of a
        card comes from models, while the FIXED AFFORDANCE LABELS are this
        file's own and are declared as constants at the top — the three that
        exist plus the one (d) adds. Do not weaken the architecture paragraph
        below it: this round dispatches on whether a node RESOLVED, never on
        a decision's `type` or `status`, so that paragraph stays true as
        written and is not edited.
    (f) The SEND is still absent, so the sentence saying so — and the
        disabled answer buttons it explains — are left EXACTLY as they are.

S3  THE STYLE, in `RightLivePanel.module.css`, added beside the existing
    `.decisionChip` rule rather than at the end of the file. It is the CARD's
    chip scale, interactive: take `.decisionFilterChip` as the model, since
    that is this card's existing interactive chip, and give the new rule a
    pointer cursor and a `:focus-visible` outline of 2px offset 2px, which
    `ux_spec.md` §14 requires of every interactive control. EVERY value
    resolves to a custom property `apps/ui/src/styles/tokens.css` ALREADY
    defines — the Base names the seven that are available and forbids
    `--remedy-focus`. Add NO token, and edit no other rule. Carry a short
    comment saying which rule it takes its scale from and why the ring names
    `--remedy-blue-strong`.

S4  DECISION F031 D15, appended to `.agent/decisions.md` in the shape D1
    through D14 already use there. CHOSEN: a decision card's deep link is its
    OWN control inside the chip row, not the whole row as `ActivityFeedCard`
    makes it, because a decision row already contains the answer buttons and
    nesting interactive controls is invalid HTML and unreachable by keyboard
    — the feed's RULE is copied, its SHAPE is not. CHOSEN: a card whose
    resolver answers null renders no control at all rather than a disabled
    one, so the affordance never lies; the disabled ANSWER buttons are a
    different case and stay, because there the action exists and is merely
    not built yet. ALTERNATIVE: making the card TITLE the button, rejected
    because the title is content, and a reader would lose the line between
    reading a decision and navigating away from it.
    REVERSE it by deleting the control and its style; nothing else depends
    on either.

── Authored slices ───────────────────────────────────────────

<<<SLICE PLANF031R30
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1–D15.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R30 records R29's PASS and gives the deep-link resolver its first caller: a
decision card that names a task the dashboard carries now offers a control that
jumps to that task's graph node, and a card that names none offers nothing.

## Next Steps
1. T003's SEND round, the last of the seam: thread the job id and the server
   token from `RemedyApp`'s `readUrlState` down to the card, mint the nonce,
   issue the request `decisionSend.ts` builds, and enable the answer buttons
   that ship disabled today. It owns the only `fetch` in this feature.
2. The clarification FORM, and the ruling on `NeedsAttentionCard`'s decision
   branch (DECISION F031 D4).
3. The integration-gate round per `docs/agents/integration_gate.md`, whose
   block also carries the §3 checklist items R-0683, R-0377, R-0419 and R-0429
   route there, then closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- NO TEST REACHES THIS MARKUP. The shipped vitest config collects
  `src/**/*.test.ts` and no DOM harness exists (DECISION F031 D5), so R30's
  wiring is gated by `tsc`, by `tests/ui_contracts/` for the style, and by
  review — not by a unit test. That is the known cost of D5, not a gap opened
  here, and it is why the resolver itself was shipped tested first.
- THE SERVER STILL ACCEPTS A BLANK ANSWER AND WRITES IT ONCE. R29 stopped it
  in the browser only; DECISION F031 D14 routes the server-side check to F009,
  which owns the write door, and it is NOT fixed here.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 241 at `def633e9` and this round leaves it there, minting nothing and
  resolving nothing.
- The findings THIS FEATURE MUST STILL ACT ON are R-0377, R-0403, R-0413,
  R-0419, R-0429, R-0431, R-0441, R-0445, R-0471, R-0495, R-0533, R-0574,
  R-0593, R-0601, R-0622, R-0625, R-0632, R-0672, R-0674, R-0675, R-0676,
  R-0677, R-0678, R-0679, R-0683, R-0684 and R-0685; R-0495 and R-0574 are the
  two Highs.
- BLOCK CAPS ARE TWO, not one: 490 lines TOTAL (DECISION F085 D6) and 400 lines
  PROSE (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R30

<<<SLICE LEDGER30
Gate: F031 R29 — the F031 R29 entry. R29 PASSED ON EVERY ONE OF ITS NINE GATES, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk rather than reading the handback back; every value that handback states reproduced cell for cell. TRANSPORT HELD IN ITS STRONGEST FORM and the chain closed end to end for the second round running: the reviewer's own scratchpad original `.remedy-wt/f031-r29.md`, the C0a blob committed at `ef3fbfb1`, the C0b blob committed at `9d05c933` and `.agent/last_block.md` read off disk at `def633e9` are ALL FOUR byte-identical at sha256 `6e361d0c24739e00b5cfcb29cdf8be47c4077c65357cc095542d3124be038609` over 41552 bytes and 451 lines, C0a and C0b resolving to the SAME git blob `3e9206dd10a3a0445df9b7ca0581469cb890d984`, and that digest is the one the reviewer measured on its own bytes BEFORE emission. THE EXTRACTION printed 2 slices, 52 content lines and 451 total, so PROSE was 399 against the 400-line cap DECISION F085 D5 sets and TOTAL 451 against the 490 DECISION F085 D6 sets. THE PLAN at `41f4e3dd` equals PLANF031R29 exactly at 2734 bytes and 47 lines, with the trailing-newline-removed control FALSE, `^## Goal$` 1 and `^## Next Steps$` 1, and 47 strictly under the 50 AGENTS.md sets. THE C2 APPEND SATISFIED WHOLE-FILE EQUALITY: `.agent/live_review.md` at `16d0240e` is its C1 blob plus one newline plus LEDGER29, at 717469 + 1 + 12046 = 729516 against an actual 729516, and the SECOND, INDEPENDENT READER AGREED — a blank-line split moves the unit count 318 to 321 and its last 3 units equal that slice's 3 paragraphs IN ORDER, trailing newlines rstripped on BOTH sides. THE NEGATIVE CONTROL WAS RUN IN MEMORY, never on the tracked file: one byte flipped at offset 723493, inside the appended text, and both readers REJECT the mutant while both ACCEPT the true file. THE SETS MOVED EXACTLY WHERE THAT BLOCK'S CONSTRAINT 10 ALLOWED AND NOWHERE ELSE, and this was a MINTING round, the first in four: `^- R-\d+ — ` 244 to 246 with the ids ADDED being EXACTLY `R-0684` and `R-0685`, the ids REMOVED the EMPTY SET, all 246 DISTINCT and the maximum moving to `R-0685`; `^Done: R-\d+ — ` 5 to 5 with the ids ADDED the EMPTY SET; `^Landed: R-` 0 to 0; `^Recurrence: R-` 22 to 22; `^Gate: R\d+ — ` 19 to 19 frozen and `^Gate: F\d+ R\d+ — ` 9 to 10, the added key exactly `F031 R28`, all keys DISTINCT. The §3 item 10 open set is 241 at `16d0240e`. THE RED PROOF IS THE REVIEWER'S OWN, run in a disposable worktree at `10c3b40c` created at a path that did not exist and removed BY THAT EXACT PATH, with `git worktree list` 1 line and `git status --porcelain` 0 after: UNMUTATED the run gives REAL exit 0 at 23 files and 375 tests, and with the refusal line reverted from the trimmed reading to the raw one — the exact bytes counted exactly ONCE in that file before the change, per §3 item 25 — the run goes REAL exit 1 at 2 failed and 373 passed, the two being `refuses a whitespace-only answer, which the server accepts and writes ONCE` and `propagates the blank-answer refusal, so no whitespace answer is sendable`, which is cell for cell what that handback reports; the file was restored byte-identically inside the worktree before removal. THE SUITES ARE THE REVIEWER'S OWN, run SERIALLY, never two alive at once, every one a REAL exit 0: `npm run typecheck` with zero diagnostics on stdout and stderr, `npm run test:unit` at 26 files and 400 tests — the FILE count UNCHANGED, since this round added no test file, and the test count 5 higher, `decisionAnswer.test.ts` 17 to 20 and `decisionSend.test.ts` 10 to 12 — with `decisionCard.test.ts` 36, `decisionFilter.test.ts` 20, `decisionOrder.test.ts` 16 and `decisionFocus.test.ts` 7 ALL UNMOVED; then `tests/ui_server/` 480, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16, `tests/ui_contracts/` 525 passed with 4 skipped and the canary `test_golden_path` 42, every count identical to the base reading. THE PRODUCTION CHANGE IS WHAT S1 THROUGH S4 ORDERED. `decisionAnswer.ts` trims once and refuses the TRIMMED text: `.trim()` occurs once, the refusal reads `if (trimmedAnswer === "") {`, the raw `answerText === ""` comparison is GONE at 0 occurrences, and the body sends the trimmed value — so a whitespace-only answer can no longer reach a record the server writes once and never revises. `decisionSend.ts` takes `target: DecisionSendTarget` with NAMED `jobId` and `serverToken` fields, so the transposition R-0684 describes is no longer expressible, and `fetch(`, `Date.now` and `useState` remain 0 in both modules. The string `four bodies` is 0 across BOTH modules, the stale count retired at its source in favour of a NAMED set. DECISION F031 D14 landed with its citations correct. HYGIENE HELD: line-anchored `^<<<SLICE ` and `^<<<END ` are 0 in `.agent/plan.md` at `41f4e3dd`, `.agent/live_review.md` at `16d0240e` and all five files C3 writes, against a CONTROL of 2 and 2 over the C0a blob; the range `26327a43`..`10c3b40c` names 9 paths, none under `docs/`, `packages/` or `tests/` and none of the forbidden set, with range-minus-change-set EMPTY and change-set-minus-range exactly `.agent/handoff.md`; the six commits `ef3fbfb1` through `def633e9` are each SINGLE-PARENT with insertions 451, 228, 21, 6, 164 and 59 read from `git diff --numstat`, each under the 500 cap AGENTS.md DECISION F104 D1 sets, and those numbers agree cell for cell with the `+/-` column of that handback's `## Commits` table; `git ls-files .remedy-wt` 0, the zip glob 0, `git worktree list` 1 line and `git status --porcelain` 0. THE BLOCK'S OWN OBJECT IDS RESOLVE: 22 SHA-shaped occurrences, 10 distinct, 9 `commit` and 1 `blob`, failing set EMPTY. THE REFLOG, scoped to the 5 entries C0a through C3, reads `commit` throughout, so `amend`, `rebase` and `cherry` are 0 each. THE PUSH DISCHARGED: `refs/heads/feature/f031-decision-inbox` on the remote and the local tip are both `def633e988f638efb2db2d816c720f419400b9bb`, no pull request was created, no branch deleted and nothing merged. THE HANDBACK IS INSIDE ITS CAP FOR THE FIRST TIME IN THIS BRANCH'S RECENT HISTORY: 100 lines against the 100-line tier its 6 commits earn, no DECISION D15 overage line needed and no section dropped — which is R-0582's pressure easing rather than that finding being resolved, and it stays OPEN. THE SEVEN DECLARED ITEMS ARE ADJUDICATED AND NONE IS A DEFECT. Items 1, 3, 5 and 7 are the block being obeyed, the naming rule being applied, a completeness check the reviewer reproduced independently, and a tooling note forced by the sandbox's command guard. Item 6 is the honest reading of a gate that states no number. ITEM 4 IS CORRECT AND WELL ROUTED: `docs/` genuinely describes none of this behaviour — the reviewer grepped `docs/ui`, `docs/system` and `docs/guides` and the only hit is a layout rule about unbalanced whitespace — so nothing on disk is falsified, and constraint 11 rightly forbade the edit. ITEM 2 IS AN IMPROVEMENT ON THE ORDER, not a deviation from it: S3 named the OPENING comments, the worker found the same stale count in the two builder DOCSTRINGS of those same files, and repaired both rather than leaving a known-false numeral standing one screen below a corrected one — which is the R-0417 "fix the instance, not the class" shape being avoided. THE VERDICT IS PASS.
<<<END LEDGER30

── Done when ─────────────────────────────────────────────────
Run every gate yourself, record its REAL exit code and REAL output, and report
ONE ENTRY PER GATE in the handback, as briefly as the ordered values allow and
with transcripts kept out (R-0582). "Green" as a word is a finding. Every gate
runs at a commit STRICTLY EARLIER than C4 (§3 item 31); G9's push follows it.

G1  Branch, cleanliness, transport. `git branch --show-current` prints
    `feature/f031-decision-inbox` and NOT `main`; `.agent/STOP` read from disk
    is ABSENT before C0a and again before C4; `git status --porcelain` line
    count after each of C0a, C0b, C1, C2 and C3 is 0. Then report sha256, byte
    count and line count for FOUR readings — `.remedy-wt/f031-r30.md` before
    C0a, the committed C0a blob, the committed C0b blob, and
    `.agent/last_block.md` off disk after C0b — ALL FOUR EQUAL, and the git
    blob id of C0a's and C0b's file, the SAME id.

G2  Extraction and the block's own two caps. Run your extractor over the
    COMMITTED C0a blob and report the slice count, the CONTENT lines inside
    markers, and the TOTAL — the numbers YOUR extractor printed — then PROSE
    as TOTAL minus CONTENT, against the two caps the Base names. If either is
    exceeded say so plainly and continue; it is the reviewer's to fix.

G3  The plan. `.agent/plan.md` at C1 is byte-equal to PLANF031R30 under your
    stated newline convention; report slice length, file length and
    convention. NEGATIVE CONTROL: NOT byte-equal to that slice MINUS its
    trailing newline. `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` STRICTLY
    under 50.

G4  The C2 append, as ONE equality over the whole file, in the shape
    constraint 8 states — name that paragraph, do not restate its formula.
    Report the boolean and the byte arithmetic against the C1 length you
    measure yourself. Report a SECOND, INDEPENDENT reading: split the
    committed file on blank lines, take the LAST N units, and confirm they
    equal LEDGER30's paragraphs IN ORDER, where N is the number YOUR split
    measured; give the unit count before and after, and STATE YOUR
    TRAILING-NEWLINE HANDLING, because a naive split reports FALSE on a
    byte-perfect file. NEGATIVE CONTROL: flip ONE byte inside the appended
    text; BOTH readers must reject the mutant and BOTH accept the true file.
    Do that flip in memory or under a disposable worktree per constraint 12,
    never on the tracked file.

G5  The ledger sets, base versus C2 in `.agent/live_review.md`, in the shape
    constraint 10 states — report each side of every movement it names, that
    the `- R-` ids ADDED and REMOVED are BOTH the EMPTY SET, that all
    `^- R-\d+ — ` ids are DISTINCT, that the maximum is still `R-0685`, and
    that the `^Done: R-\d+ — ` ids ADDED are ALSO the EMPTY SET.
    `^Gate: R\d+ — ` 19 → 19 UNCHANGED, and `^Gate: F\d+ R\d+ — ` 10 → 11, the
    ADDED key being exactly `F031 R29`, all keys DISTINCT (§3 item 26). Report
    `^Recurrence: R-` 22 → 22 and `^Landed: R-` 0 → 0, the §3 item 10 open set
    at C2, and that `git diff --name-only` over C3 does NOT name
    `.agent/live_review.md` — the whole of constraint 8's "nothing at all in
    any other commit".

G6  TWO RED CONTROLS, because this round's real gates are `tsc` and the CSS
    contract rather than a unit test, and a gate that cannot fail proves
    nothing when it passes. Both run in ONE disposable worktree at C3 per
    constraint 12. Run each mutation, record the REAL exit code, RESTORE the
    file byte-identically, and confirm that worktree's `git status
    --porcelain` is 0 before the next.
    (a) TYPE WIRING. In `RightLivePanel.tsx` inside that worktree, DELETE the
        `onSelectNode` attribute S1 adds to the `DecisionInboxCard` element —
        count the exact bytes you delete in THAT file first and report the
        count, which MUST be 1 (§3 item 25) — then run `npm run typecheck`
        from the PRIMARY checkout's `apps/ui` with `--project` pointed at that
        worktree, or by whatever route runs `tsc` over the worktree's sources
        using the primary's installed compiler. IT MUST GO RED, and you report
        the REAL exit code and the diagnostic naming the missing prop. If you
        cannot run `tsc` against the worktree at all, say so plainly and run
        this control by a route you CAN run, naming it — do not report a
        colour you did not observe.
    (b) CSS CONTRACT. In `RightLivePanel.module.css` inside that worktree,
        change ONE `var(--remedy-…)` inside S3's new rule to a name
        `apps/ui/src/styles/tokens.css` does not define, then run
        `python3 -m pytest tests/ui_contracts/test_design_drift.py -q` from
        that worktree. IT MUST GO RED and name
        `TestEveryCustomPropertyResolves`. Report the REAL exit code and the
        failing test id; this block states no failure count.
    Then remove the worktree BY ITS EXACT PATH and report `git worktree list`
    as 1 line after, naming that path.

G7  Structure, then the suites. Report, as counts YOU measured at C3: that
    `nodeIdForDecisionCard` is IMPORTED from `../../api/decisionFocus` in
    `DecisionInboxCard.tsx` and CALLED there exactly once — quote both lines;
    that `FocusableTask` is imported from `../../api/feedFocus` and the file
    declares no type of that name; that `fetch(` is 0 there and the answer
    button still carries `disabled`; that `never a value this file chose` is
    0, S2(e)'s sentence retired; and that every `--remedy-` name S3's new rule
    uses appears as a DEFINITION in `apps/ui/src/styles/tokens.css`, listing
    the names you checked. Then in
    the PRIMARY checkout at the C3 tree, all REAL exit 0, run SERIALLY and
    never two alive at once, with `git worktree list` reported as 1 line
    immediately BEFORE the first of them. At `apps/ui`: `npm run typecheck`
    with ZERO diagnostics on stdout and stderr; `npm run test:unit`, reporting
    the file and test counts YOUR run measured, which must be EXACTLY 26 and
    400 — UNCHANGED from the Base, because this round adds no test and no test
    reaches this markup, and any movement is a finding. Then in Python, by
    these exact command lines with no extra flag:
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/ui_contracts/ -q
      python3 -m pytest tests/cli/test_golden_path.py -q
    These are the four state readers a round rewriting `.agent/` state gates,
    plus `tests/ui_contracts/` — which is this round's REAL style gate, not a
    formality — plus the canary. The reviewer ran all six at `def633e9` with
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
    `apps/ui/src/RemedyApp.tsx`, `apps/ui/src/styles/tokens.css`,
    `apps/ui/src/components/panels/ActivityFeedCard.tsx`,
    `apps/ui/src/components/panels/TaskChecklistCard.tsx`,
    `apps/ui/src/api/decisionFocus.ts`, `apps/ui/src/api/decisionAnswer.ts`,
    `apps/ui/src/api/decisionSend.ts` or `apps/ui/src/api/remedyApi.ts`; the
    range path set MINUS the change set is EMPTY and the change set MINUS the
    range is exactly `.agent/handoff.md`, which C4 writes. Over C0a..C3 report
    per commit that it is single-parent and its INSERTION count — the `+`
    column only, per AGENTS.md DECISION F104 D1 — each under 500; those same
    numbers fill the `+/-` column of the `## Commits` table, derived from
    `git diff --numstat` and NOT from `git commit`'s own summary, and you
    report that the two agree cell for cell (§3 item 28). Report
    `git ls-files .remedy-wt` as 0 and `git ls-files` over the zip glob as 0.
    FOR THE REFLOG state SCOPE and FIELD: over THIS ROUND'S entries only, by
    the OPERATION PREFIX before the first colon of `git reflog --format=%gs`,
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
    and records them in the R30 entry of `.agent/live_review.md`. In
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
and report BOTH that count and the tier. R29 met that tier exactly, so it is
reachable; if the MANDATED content still does not fit, exceed it and carry a
DECISION D15 line naming your count as a NUMERAL (R-0430) and its cause.

YOUR `## Next` SECTION names, in order: that the next session reads
`.agent/STOP` from disk as Phase 1 rule 1 BEFORE the Open PR Gate as rule 2;
that the R30 verdict is UNRECORDED and owed by the next round's ledger commit
(DECISION F085 D9); and that T003's SEND round is next and is the last of the
seam, owning the only `fetch` in this feature.

Declare every deviation, contradiction and assumption.
──────────────────────────────────────────────────────────────

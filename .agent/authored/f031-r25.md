── STEP R25 — F031 Decision inbox ────────────────────────────
Goal:        T002b BADGE, THE HALF THAT SHOWS, and the sweep R23 owed. The
             inbox card carries its own OPEN count, derived in
             `decisionCard.ts` where the model's `isOpen` already lives, and
             the two comments that call counting and wiring absent are
             retired at their source, each naming what falsified it.

Fortschritt: ~88 % (F031 claimed; R1 through R24 landed, R24 gated here ·
             T001 SHIPPED · T002a MODEL shipped, wired and RENDERED ·
             T002b ORDERING, FILTERING and BADGE SERVER SHIPPED and gated ·
             T002b badge UI half here, closing T002b · T003 offen)
             — Schaetzung

Bundle:      C0a save this block · C0b mirror it into last_block · C1 the
             plan · C2 the R24 gate entry and one new finding · C3 the count,
             the badge, its style, the two comment repairs, the tests and
             DECISION F031 D10 · C4 handback.

Change set:  exactly these paths, nothing else —
             .agent/authored/f031-r25.md                             (C0a)
             .agent/last_block.md                                    (C0b)
             .agent/plan.md                                          (C1)
             .agent/live_review.md                                   (C2)
             apps/ui/src/api/decisionCard.ts                         (C3)
             apps/ui/src/api/decisionCard.test.ts                    (C3)
             apps/ui/src/api/decisionFilter.ts                       (C3)
             apps/ui/src/components/panels/DecisionInboxCard.tsx     (C3)
             apps/ui/src/components/panels/RightLivePanel.module.css (C3)
             .agent/decisions.md                               (C3, D10)
             .agent/handoff.md                                       (C4)
             This list bounds the round's WRITES, not its ACTIONS: the push
             named in G9 is ordered explicitly and is not a file (R-0674).
             R-0682's `role="group"` fix is NOT here: it spans a second file
             this round has no reason to open, and its `Landed:` line would
             give `.agent/live_review.md` a second write. The plan routes it
             to T003's first round.

── Base ──────────────────────────────────────────────────────
The round base is `6163e88774699c0265dd6d2613d190737acb91ad`, the R24
handback commit and the tip of `feature/f031-decision-inbox`, local and
remote EQUAL — the reviewer measured both with `git ls-remote` at the R24
gate. Stay on that branch; create none, never commit to `main`. Every
SHA-shaped token here resolved under `git cat-file -t` before emission,
and the types are NOT all `commit`.

Readings the reviewer MEASURED at that base, re-checkable there:
- `.agent/live_review.md` 677520 bytes; `^- R-\d+ — ` 243 all DISTINCT,
  maximum `R-0682`; `^Done: R-\d+ — ` 4, so the §3 item 10 open set is
  239; `^Recurrence: R-` 19; `^Landed: R-` 0. THE GATE SERIES IS SPLIT by
  DECISION F031 D7: `^Gate: R\d+ — ` 19, frozen, and
  `^Gate: F\d+ R\d+ — ` 5, those five being `F031 R19` through `F031 R23`.
- `.agent/plan.md` 47 lines, 2792 bytes. `docs/roadmap/**` is UNTOUCHED,
  so the §3 docs-round gate is not earned and is not ordered.
- `apps/ui`: `npm run typecheck` exit 0, zero diagnostics on stdout and
  stderr; `npm run test:unit` exit 0 at 23 files and 352 tests, of which
  `decisionCard.test.ts` is 27, `decisionFilter.test.ts` 20 and
  `decisionOrder.test.ts` 16.
- The Python suites, every one exit 0: `tests/ui_server/` 480,
  `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate`
  16, `tests/ui_contracts/` 525 passed with 4 skipped, `test_golden_path` 42.
- THE COUNT IS ALREADY IN THE MODEL, which is why S1 adds a reader and not
  a derivation. `DecisionCardModel` carries `isOpen: boolean`, set by
  `buildDecisionCardModel` as `card.status === "open"`. No new field is
  needed and no status string is compared outside `decisionCard.ts`.
- THE BADGE'S LIVENESS ALREADY EXISTS AND IS NOT AN SSE REFETCH.
  `apps/ui/src/RemedyApp.tsx` reloads the WHOLE dashboard on
  `window.setInterval(load, 5000)`, so `decisionInbox` refreshes every five
  seconds with no new wiring, where DECISION F031 D2 rules the badge
  refetched on an SSE signal. S5 records that departure.
- THE SUITE GUARDS OVER THE FILES C3 REWRITES were read first (§3 item 7).
  Under `tests/` there is NO `count(` and no `== 1` assertion over any of
  them; `tests/ui_contracts/test_ux_quality.py` reads
  `RightLivePanel.module.css` by SUBSTRING PRESENCE only. Appending a class
  is safe; editing an existing rule is not, which S2 forbids.
- THIS BLOCK'S OWN TWO CAPS, measured on its final bytes before emission
  and stated so your re-measurement can disagree with the reviewer's, are
  490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE (DECISION F085
  D5). G2 orders you to report both from the COMMITTED blob.

── Constraints ───────────────────────────────────────────────
1. Apply every authored SLICE BYTE FOR BYTE. Never retype, rewrap or
   "fix" one. If a slice looks wrong, apply it verbatim and DECLARE the
   disagreement: a contradiction in this block is the reviewer's defect.
2. THE PRODUCTION CHANGE, ITS TESTS AND DECISION D10 ARE DESCRIBED, NOT
   SLICED. The numbered specification S1 through S5 fixes behaviour,
   structure, style and copy; YOU write that code, those tests and that
   decision entry under AGENTS.md's Mandatory Self-Review Loop and its File
   Editing Safety Rules. Where the spec is silent, prefer the idiom the
   neighbouring module already uses. Where the spec is WRONG, say so in the
   handback and do the right thing.
3. Slice transport. This block is saved verbatim as
   `.agent/authored/f031-r25.md` at C0a and mirrored byte-identically into
   `.agent/last_block.md` at C0b. Extract every slice PROGRAMMATICALLY out
   of the COMMITTED C0a blob by its marker LINES — `<<<SLICE <NAME>` opens,
   `<<<END <NAME>` closes. Marker lines never reach a target file.
4. Commit sequence, exactly: C0a, C0b, C1, C2, C3, C4. No extra commit,
   none dropped, no reordering. C1 is FIRST substantive because this round
   writes the finding ledger (§3 item 23). To correct a landed commit, do
   NOT add one outside this sequence — declare it, and give it its own
   `## Commits` and item-status rows (R-0675).
5. Never amend, rebase, cherry-pick, force-push or rewrite history; never
   delete a branch; never merge; create no pull request.
6. `git status --porcelain` prints 0 lines after every commit. Read
   `.agent/STOP` from disk before C0a and again before C4; if present,
   finish the commit in hand, write the handback and stop. NEVER delete
   that sentinel (R-0347).
7. The slices this block carries are the whole text PLANF031R25 and the
   appended text LEDGER25. This paragraph names them and states no count;
   G2 orders you to report the count YOUR extractor measured.
8. THE ONE APPEND'S SHAPE, STATED ONCE HERE, WITH EVERY GATE NAMING THIS
   PARAGRAPH RATHER THAN RESTATING IT. Under the newline-INCLUDED
   convention each slice already ends in a newline, so `.agent/live_review.md`
   after C2 is EXACTLY: its blob at C1, then one newline, then LEDGER25 —
   and it receives NOTHING ELSE in that commit, and nothing at all in any
   other commit of this round (R-0657). LEDGER25's own paragraph count is
   yours to measure; this paragraph states no number. `.agent/decisions.md`
   also GROWS at C3, by text YOU author under S5, so no equality gate is
   ordered over it and none may be reported.
9. THIS BLOCK CARRIES NO FROM/TO PAIR, so no containment test is reported
   and no FROM-zero count is ordered (§3 item 15). The plan is a WHOLE-FILE
   replacement and LEDGER25 is an append.
10. THIS ROUND MINTS EXACTLY ONE FINDING ID AND RESOLVES NONE. LEDGER25
    carries `R-0683`, so `^- R-\d+ — ` moves 243 → 244 with the maximum
    moving `R-0682` → `R-0683`. `^Done: R-`, `^Landed: R-` and
    `^Recurrence: R-` are ALL UNCHANGED at 4, 0 and 19, so the §3 item 10
    open set moves 239 → 240. WRITE NO `Done:` LINE — only reviewer-authored
    text sets Resolved — and WRITE NO `Landed:` LINE: R-0682's fix is not in
    this round's change set, and R-0593 stays OPEN because its instances in
    `packages/orchestration/release_gate.py` and `pyproject.toml` are
    outside F031 and untouched, even though S3 repairs its last instance in
    this feature's reach. No landed finding paragraph is edited (§3 item 20).
11. TOUCH NO DOCUMENT AND NO OTHER CODE. Nothing under `docs/`,
    `packages/` or `tests/`, and neither `.agent/context.md` nor either
    `f031_*_inventory.md`. Inside `apps/` only the five paths the change set
    names are written — NOT `RightLivePanel.tsx`, `decisionOrder.ts`,
    `remedyApi.ts`, `RemedyApp.tsx`, `TopMetricsBar.tsx` or
    `components/graph/GraphFilterChips.tsx`, and no other test file.
12. Destructive verification runs ONLY in a disposable `git worktree`
    under `.remedy-wt/`, removed BY ITS EXACT PATH (R-0662) and before the
    G7 suites. Everything already there is pre-existing scratch belonging
    to no commit, this block's own file included: create no worktree at an
    existing path, and delete nothing you did not create.

── Specification (S1–S5) — the production change ─────────────
S1  THE COUNT, in `apps/ui/src/api/decisionCard.ts`, exported beside
    `decisionCardModels`. It takes a readonly array of `DecisionCardModel`
    and returns how many carry `isOpen`, as a `number`. Total by
    construction: no input makes it throw and an empty array answers 0.
    Name it for what it answers, carrying the domain word, so it greps to
    its own definition and its real usages only. It compares NO status
    string of its own — `isOpen` is already that comparison, made once in
    `buildDecisionCardModel` — and it must not filter, sort or re-derive
    anything else. Put the one-line WHY comment directly above it.
    THEN REPAIR THAT FILE'S OWN HEADER, which still says that what "is
    still genuinely absent everywhere is COUNTING". It is not, after this
    commit. Rewrite it for what is true: the count lives here, the badge
    showing it is in `../components/panels/DecisionInboxCard`, and the
    remaining absence is T003's answering. Keep the sentence's shape — a
    deliberate-absence note naming where the thing now IS, per AGENTS.md's
    Code Discoverability rules.

S2  THE BADGE, in `apps/ui/src/components/panels/DecisionInboxCard.tsx`,
    rendered inside the existing `cardHeader` beside `<h2>Decision inbox</h2>`
    and computed ONCE per render from the UNFILTERED `decisions` prop —
    never from `view.visible`, or the badge would count what the chosen chip
    left rather than what the job is waiting on. It shows the number S1
    returns and nothing else; it is not a dot, not a colour and not a state,
    so `ux_spec.md` §14's colour-only rule has nothing to bite on. Give the
    number an accessible reading: a bare digit beside a heading is ambiguous
    to a screen reader, so carry a word saying what is counted, on an
    element whose ROLE permits a name — R-0682 is open in this record
    precisely because an `aria-label` on a bare `<div>` does not.
    A STYLE for it is APPENDED to
    `apps/ui/src/components/panels/RightLivePanel.module.css` — a new class
    name only, EDITING NO EXISTING RULE — on the card's own chip scale, every
    value resolving to a custom property `apps/ui/src/styles/tokens.css`
    ALREADY DEFINES. `--remedy-focus` is still not one; R23 spent a
    correction commit on exactly that.

S3  THE LAST `R-0593` INSTANCE IN THIS FEATURE'S REACH, in
    `apps/ui/src/api/decisionFilter.ts`, whose header carries TWO sentences
    this branch has already falsified. FIRST: "THE SEAM IS NOT WIRED YET —
    `RightLivePanel.tsx` still hands `orderDecisionInbox(...)` straight to
    the card — and `decisionInboxView` is the shape that wiring will call,
    which is why it exists a round before its caller does."
    `DecisionInboxCard.tsx` has imported and called `decisionInboxView`
    since `6147efc4`. The middle clause is still TRUE and stays true; the
    two around it are not. Rewrite the sentence to name `6147efc4` as the
    commit that gave the module its caller and to say WHERE that caller is,
    so the pointer runs both ways. SECOND: "the inbox badge's count is the
    piece of T002b still genuinely absent everywhere" — S1 lands it in
    `./decisionCard.ts`, so name that module instead of the absence.

S4  THE TESTS, appended to `apps/ui/src/api/decisionCard.test.ts` beside the
    existing `decisionCardModels` block and following that file's idiom.
    Cover, at minimum: an empty array answers 0; a mixed list answers only
    the `isOpen` ones; a list whose every card is resolved answers 0; and
    the count reads `isOpen` rather than a status string, pinned by a model
    whose `status` is some OTHER open-sounding word and whose `isOpen` is
    therefore false. Build every model through `buildDecisionCardModel`
    rather than by hand, so the tests pin the SEAM and not a literal. Name
    each test for the property it pins.

S5  DECISION F031 D10, appended to `.agent/decisions.md` in the shape D1
    through D9 already use there, ruling the badge's SURFACE and its
    LIVENESS, both of which depart from the feature file as written.
    CHOSEN, surface: the badge is the inbox CARD's own header count, not
    "the shell's inbox icon" the Design section names — measured at this
    round's base, the shell has no inbox icon and `component_spec.md`
    specifies none, so there is no icon to hang a count on while the card
    showing the decisions is right there. CHOSEN, liveness: D2 rules the
    badge refetched on an SSE signal; what ships is `RemedyApp.tsx`'s
    existing five-second `setInterval` reload, which already refreshes
    `decisionInbox`. D2's INTENT is met — no new event kind, re-derivation
    rather than emission — and only its MECHANISM differs, so record the
    measurement rather than add a second refetch path beside a working one.
    ALTERNATIVE: a stream-driven refetch, rejected as a second path to the
    same data whose only gain is latency under five seconds on a panel that
    is read, not raced. REVERSE the surface by moving the count into a shell
    affordance once one exists; the liveness by subscribing to the stream.

── Authored slices ───────────────────────────────────────────

<<<SLICE PLANF031R25
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1–D10.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R25 CLOSES T002b: the inbox card carries its own OPEN count, derived in
`decisionCard.ts` from the `isOpen` the model already sets, and the last two
comments in this feature that call counting and wiring absent are retired at
their source, each naming what falsified it.

## Next Steps
1. T003 wires answering through the existing write channel, adds the
   clarification form and the deep links, rules `NeedsAttentionCard` (DECISION
   F031 D4), and carries R-0682's `role="group"` fix in both files.
2. The integration-gate round per `docs/agents/integration_gate.md`, whose
   block also carries the §3 checklist item R-0683 routes there, then closure
   per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- THE BADGE MUST COUNT THE PROP, NOT THE VIEW. `DecisionInboxCard` holds both
  the unfiltered `decisions` prop and the filtered `view.visible`; a count taken
  from the second would drop every time a chip narrowed the list and would tell
  the operator the queue had shrunk when only their filter had.
- STILL NO TEST REACHES THE MARKUP under DECISION F031 D5, so the badge's
  RENDERING is pinned by `tsc`, structure and review, while its NUMBER is
  pinned by `decisionCard.test.ts`. Keeping the count a pure function is what
  makes that split possible.
- TWO NUMBERS NOW ANSWER ONE QUESTION from opposite sides of the wire:
  `metrics.open`, re-derived on the server at R24, and this badge, derived in
  the browser. They agree today because both read one queue through one
  endpoint, and nothing pins that agreement.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 239 at `9ec7b2de`, and this round's C2 raises it to 240 by minting
  R-0683, in the commit order the R25 block's constraint 4 fixes.
- The findings THIS FEATURE MUST STILL ACT ON are R-0403, R-0413, R-0431,
  R-0441, R-0445, R-0471, R-0495, R-0533, R-0574, R-0593, R-0601, R-0622,
  R-0625, R-0632, R-0672, R-0674, R-0675, R-0676, R-0677, R-0678, R-0679,
  R-0682 and R-0683; R-0495 and R-0574 are the two Highs.
- BLOCK CAPS ARE TWO, not one: 490 lines TOTAL (DECISION F085 D6) and 400 lines
  PROSE (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R25

<<<SLICE LEDGER25
Gate: F031 R24 — the F031 R24 entry. R24 PASSED ON EVERY ONE OF ITS NINE GATES, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk rather than reading the handback back; every value that handback states reproduced exactly, and R24 earns no finding against its execution. TRANSPORT HELD IN ITS STRONGEST FORM, cmp-against-scratchpad rather than the digest fallback: the reviewer's own emitted `.remedy-wt/f031-r24.md`, the C0a blob committed at `0f5ef322`, the C0b blob committed at `4adb26ef`, and `.agent/last_block.md` read off disk at `6163e887` are ALL FOUR byte-identical at sha256 `a56ced36452288e42457aedc34f113c0f94f2944c2f17c946b49605a2dc6345c` over 40561 bytes and 450 lines, C0a and C0b resolving to the SAME git blob `141e5735d7f3f9610334f80bc0bf34add3702fa7`. THE EXTRACTION printed 2 slices, 52 content lines and 450 total, so PROSE was 450 − 52 = 398 against the 400-line cap DECISION F085 D5 sets and TOTAL 450 against the 490 DECISION F085 D6 sets. THE PLAN at `d6822bfd` equals PLANF031R24 exactly at 2792 bytes and 47 lines, with the trailing-newline-removed control FALSE, `^## Goal$` 1 and `^## Next Steps$` 1, and 47 strictly under the 50 AGENTS.md sets; its narrow finding list holds 22 DISTINCT ids across 24 occurrences, the two repeats being `R-0495` and `R-0574` named again as the Highs, so the handback's "22 distinct" is exact. THE C2 APPEND SATISFIED WHOLE-FILE EQUALITY: `.agent/live_review.md` at `9ec7b2de` is its C1 blob plus one newline plus that round's slice, at 665858 + 1 + 11661 = 677520 against an actual 677520, and the SECOND, INDEPENDENT READER AGREED — a blank-line split moves the unit count 306 to 309 and its last 3 units equal that slice's 3 paragraphs IN ORDER, trailing newlines rstripped on BOTH sides. A THREE-PARAGRAPH SLICE MAKES ORDER LOAD-BEARING, and the ordered comparison is what was run. THE NEGATIVE CONTROL WAS RUN IN MEMORY, never on disk: both readers REJECT the one-byte mutant and both ACCEPT the true file. THE SETS MOVED EXACTLY WHERE CONSTRAINT 10 ALLOWED AND NOWHERE ELSE: `^- R-\d+ — ` 242 to 243 all DISTINCT, ids ADDED exactly `R-0682`, ids REMOVED the EMPTY SET, maximum `R-0681` to `R-0682`; `^Done: R-` 4 to 4, `^Landed: R-` 0 to 0, `^Recurrence: R-` 18 to 19; `^Gate: R\d+ — ` 19 to 19 frozen and `^Gate: F\d+ R\d+ — ` 4 to 5, the added key exactly `F031 R23`, all keys DISTINCT. The §3 item 10 open set is 239 at `9ec7b2de`; `- R-0593 — ` still occurs exactly ONCE line-anchored, so its landed paragraph was not edited, while `^Recurrence: R-0593` moved 1 to 2, the new paragraph joining the old rather than replacing it. THE RED PROOF IS THE REVIEWER'S OWN, run in a disposable worktree at `6b68718e` and removed by exact path with `git worktree list` 1 line and `git status --porcelain` 0 after: the mutation target — the helper's whole `try`/`except` body — occurs EXACTLY ONCE in the file, UNMUTATED gives exit 0 at 45 and 74 tests, and with the body reduced to the literal `0` BOTH suites go REAL exit 1 with exactly 1 failure each, both named `test_repo_less_job_reports_its_open_decisions`, which is cell for cell what the handback reports; the file was restored byte-identically inside the worktree before removal. THE SUITES ARE THE REVIEWER'S OWN, run SERIALLY, never two alive at once, every one a REAL exit 0: `ruff check` over the three Python paths printed "All checks passed!", and `tests/ui_server/` 480, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16, `test_autonomy` 81 and `test_golden_path` 42 — the 480 being 474 plus exactly the 6 tests S3 added, with every other count identical to the base readings. THE PRODUCTION CHANGE IS WHAT S1 AND S2 ORDERED, read by AST rather than by grep so that SCOPE was measured and not guessed: `def _count_open_decisions` occurs once, the name occurs once inside `_build_dashboard` and once inside `_build_live_state_json`, `blocker_count` occurs 0 times in either body, the helper aliases the queue's `list_decisions` as `list_queue_decisions` so the `orchestrator_brain` spelling in `_build_orchestrator_section` is untouched, and its `except` tuple is the SAME six exception types that neighbour catches. Both payload keys keep their name, their `int` type and their position. HYGIENE HELD: line-anchored `^<<<SLICE ` and `^<<<END ` are 0 in `.agent/plan.md` at `d6822bfd`, `.agent/live_review.md` at `9ec7b2de` and all four files C3 writes, against a CONTROL of 2 and 2 over the C0a blob; the range `030a43d1`..`6b68718e` names 8 paths, none under `docs/` or `apps/` and none of `.agent/context.md`, either inventory, `decision_queue.py` or `decision_inbox.py`, with range-minus-change-set EMPTY and change-set-minus-range exactly `.agent/handoff.md`; the six commits of `030a43d1`..`6163e887` are each SINGLE-PARENT with insertions 450, 263, 21, 6, 150 and 73 read from `git diff --numstat`, each under the 500 cap AGENTS.md DECISION F104 D1 sets, and the first five agree CELL FOR CELL with the `+/-` column of that handback's `## Commits` table, which is the §3 item 28 reading; `git ls-files .remedy-wt` 0, the zip glob 0, `git worktree list` 1 line and `git status --porcelain` 0; the reflog read by OPERATION PREFIX shows `commit` for every entry of this round with amend 0, rebase 0 and cherry 0. THE BLOCK'S OWN OBJECT IDS RESOLVE: 23 SHA-shaped occurrences, 11 distinct, failing set EMPTY, 10 `commit` and 1 `blob`. THE PUSH DISCHARGED, which is the outcome G9 routed to the reviewer rather than to any file R24 wrote: measured with `git ls-remote`, `refs/heads/feature/f031-decision-inbox` and the local tip are both `6163e88774699c0265dd6d2613d190737acb91ad`, and no pull request was created, no branch deleted and nothing merged. THE HANDBACK FITS ITS TIER WITH NO OVERAGE: 96 lines against the 100 AGENTS.md allows for its 6 commits, every mandated section present. THE SIX DECLARED ITEMS ARE ADJUDICATED. Items 3 through 6 are the block being obeyed and are not deviations at all. ITEMS 1 AND 2 ARE BOTH THE REVIEWER'S OWN DEFECT, correctly declared and correctly NOT worked around, and together they are R-0683, appended beside this entry. THE VERDICT IS PASS.

- R-0683 — Medium, A GATE COUNTED AN IDENTIFIER OVER A WHOLE FILE WHILE THE THING THE BLOCK RETIRED WAS A LOCAL, AND ITS CARVE-OUT PUT A SURVIVING USE IN A PLACE THE CODE CONTRADICTS — TWICE IN ONE GATE. Raised by the reviewer at the F031 R24 gate, out of two deviations the WORKER declared, and confirmed by the reviewer at `6b68718e` by parsing the module with `ast`, so every reading below is scope-resolved rather than grepped. FIRST INSTANCE: R24's G7 ordered `blocker_count` to occur ZERO times in the whole of `packages/orchestration/ui_server.py`. It occurs TWICE, at lines 857 and 874, and both are payload KEYS of `_build_overnight_section` — `"blocker_count": "unknown"` and `"blocker_count": len(d.get("blockers", []))` — an unrelated readiness section with a `blockers` list of its own. What S2 actually retired was the LOCAL of that name inside `_build_dashboard`, and that local really is gone: `blocker_count` occurs 0 times inside either builder body. The ordered zero was therefore unmeetable by any correct round, and the only way to meet it was to break a contract the block never mentioned. SECOND INSTANCE, in the same gate: G7 ordered `human_decision_requested` absent from BOTH builder bodies while carving out "the humanize maps elsewhere in the module, which legitimately keep that string". That map is NOT elsewhere — `_event_actors` sits at line 1847, INSIDE `_build_dashboard`, which spans 1687 to 2020, and it labels the activity feed's actor rather than counting anything. So the carve-out named a location the code does not have: the ordered zero holds in `_build_live_state_json`, which measures 0, and cannot hold in `_build_dashboard`, which measures 1. WHY MEDIUM AND NOT LOW: neither error cost the round anything — the worker measured both, reported the real numbers, changed nothing it was not ordered to change and declared both as contradictions, which is exactly right — but a gate that cannot be met is indistinguishable on the page from one that binds, and the next worker to meet one by editing the code is the failure this finding exists to prevent. That is not hypothetical here: meeting instance one required deleting two keys of an unrelated public payload. WHAT THE CLASS IS. §3 item 24 makes the reviewer resolve every PATH a gate names, and §3 item 21 every path a baseline COMMAND runs over, because a path that does not resolve makes a gate vacuous. NOTHING in that checklist makes the reviewer resolve the SCOPE of an IDENTIFIER a gate counts, and both halves of this finding are that gap: the first counts a name over a file when the block's own change is scoped to a function, the second asserts where a name lives without reading where it lives. COUNTER-MEASURE, and it is owed to §3 rather than to this paragraph, because a rule that lives only in a finding body binds nothing — R-0377, R-0491 and R-0656 each proved that by recurring: a new checklist item requiring that a gate counting an identifier over a file first resolve that identifier's every occurrence to its enclosing scope, and STATE the scope it means, so "0 in the whole file" is written only when the whole file is what the block changes. Where the block's change is scoped to a function, the gate is scoped to that function too, by AST and not by grep. THAT EDIT IS ROUTED TO THE INTEGRATION-GATE ROUND'S OWN BLOCK, named in `.agent/plan.md` at this round's C1, so it does not become the finding body it is warning about. SEARCHED BEFORE MINTING per §3 item 30: `.agent/live_review.md` at `9ec7b2de` holds no open finding about an identifier's scope — R-0559, the nearest neighbour, governs the PATHS a gate names and its fix clause reaches paths only, while the R-0441 family governs NUMERALS a block states about lists it owns; neither describes a count whose every individual reading is correct and whose SCOPE is wrong.
<<<END LEDGER25

── Done when ─────────────────────────────────────────────────
Run every gate yourself, record its REAL exit code and REAL output, and
report ONE LINE PER GATE in the handback, transcripts kept out (R-0582).
"Green" as a word is a finding. Every gate runs at a commit STRICTLY
EARLIER than C4 (§3 item 31); G9's push runs after it and names its carrier.

G1  Branch, cleanliness, transport. `git branch --show-current` prints
    `feature/f031-decision-inbox` and NOT `main`; `.agent/STOP` read from
    disk is ABSENT before C0a and again before C4; `git status --porcelain`
    line count after each of C0a, C0b, C1, C2 and C3 is 0. Then report
    sha256, byte count and line count for FOUR readings —
    `.remedy-wt/f031-r25.md` before C0a, the committed C0a blob, the
    committed C0b blob, and `.agent/last_block.md` off disk after C0b — all
    four EQUAL, and the git blob id of C0a's and C0b's file, the SAME id.

G2  Extraction and the block's own two caps. Run your extractor over the
    COMMITTED C0a blob and report the slice count, the CONTENT lines inside
    markers, and the TOTAL — the numbers YOUR extractor printed — then
    PROSE as TOTAL minus CONTENT, against the two caps the Base names. If
    either is exceeded say so plainly and continue; it is not yours to fix.

G3  The plan. `.agent/plan.md` at C1 is byte-equal to PLANF031R25 under
    your stated newline convention; report slice length, file length and
    convention. NEGATIVE CONTROL: NOT byte-equal to that slice MINUS its
    trailing newline. `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` STRICTLY
    under 50.

G4  The C2 append, as ONE equality over the whole file, in the shape
    constraint 8 states — name that paragraph, do not restate its formula.
    Report the boolean and the byte arithmetic against the C1 length you
    measure yourself. Report a SECOND, INDEPENDENT reading: split the
    committed file on blank lines, take the LAST N units, and confirm they
    equal LEDGER25's paragraphs IN ORDER, where N is the number YOUR split
    measured; give the unit count before and after, and STATE YOUR
    TRAILING-NEWLINE HANDLING, because the R21 through R24 entries all
    record that a naive split reports FALSE on a byte-perfect file. This
    slice carries MORE THAN ONE paragraph, so ORDER is load-bearing and a
    set comparison does not discharge it. NEGATIVE CONTROL: flip ONE byte
    inside the appended text; BOTH readers must reject the mutant and BOTH
    accept the true file. Do that flip in memory or under a disposable
    worktree per constraint 12, never on the tracked file.

G5  The ledger sets, base versus C2 in `.agent/live_review.md`, in the
    shape constraint 10 states — report each side of every movement it
    names, plus that the ids ADDED are exactly `R-0683`, that the ids
    REMOVED are the EMPTY SET, and that all `^- R-\d+ — ` ids are DISTINCT.
    `^Gate: R\d+ — ` 19 → 19 UNCHANGED, and `^Gate: F\d+ R\d+ — ` 5 → 6,
    the ADDED key being exactly `F031 R24`, all keys DISTINCT (§3 item 26).
    Report the §3 item 10 open set at C2, that `- R-0593 — ` still occurs
    exactly ONCE line-anchored, and that `git diff --name-only` over C3 does
    NOT name `.agent/live_review.md` — the whole of constraint 8's "nothing
    at all in any other commit".

G6  THE RED PROOF, in a disposable worktree at C3 per constraint 12, so the
    primary checkout is never mutated, with vitest run from the PRIMARY
    checkout's `apps/ui` so the primary's `node_modules` resolves:
      npx vitest run --config <PRIMARY>/apps/ui/vitest.config.ts \
        --root <WORKTREE>/apps/ui src/api/
    Run it UNMUTATED first and report the file and test counts. Then, in
    `apps/ui/src/api/decisionCard.ts` INSIDE THAT WORKTREE, change the body
    of S1's counting function so it returns `models.length` — the
    every-card-counts mutant, the wrong answer a badge would most plausibly
    ship — leaving every other byte alone, and run the same line again. IT
    MUST GO RED. Report the REAL exit code, the NAMES of the failing tests,
    and the failure count YOUR run measured; this block states no number. A
    GREEN means S4's tests do not discriminate open from resolved, and is
    reported as such. Remove the worktree BY ITS EXACT PATH and report
    `git worktree list` as 1 line after, naming that path.

G7  Structure, then the suites. Report, as counts YOU measured at C3, over
    `apps/ui/src/components/panels/DecisionInboxCard.tsx`: the literal guard
    `if (decisions.length === 0) return null;` exactly ONCE, `aria-pressed`
    and `aria-live` each still present, and S1's counting function CALLED
    WITH THE UNFILTERED PROP — quote the call line, and report that no line
    holds both that function's name and the token `visible`. Over
    `decisionCard.ts`, that name greps to exactly one `export`. Then in the
    PRIMARY checkout at the C3 tree,
    all REAL exit 0, run SERIALLY and never two alive at once, with
    `git worktree list` reported as 1 line immediately BEFORE the first of
    them. At `apps/ui`: `npm run typecheck` with ZERO diagnostics on stdout
    and stderr; `npm run test:unit`, reporting the file and test counts YOUR
    run measured — `decisionFilter.test.ts` must still be exactly 20 and
    `decisionOrder.test.ts` exactly 16, any movement in either being a
    finding, while `decisionCard.test.ts` MUST EXCEED 27 by exactly the
    number of tests S4 adds: report BOTH numbers and their difference. Then
    in Python, by these exact command lines with no extra flag:
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/ui_contracts/ -q
      python3 -m pytest tests/cli/test_golden_path.py -q
    These are the four state readers a round rewriting `.agent/` state
    gates, plus `tests/ui_contracts/` — which READS the CSS S2 appends to —
    plus the canary. The reviewer ran all six at `6163e887` with these exact
    lines and measured in that order 480, 52, 21, 16, 525 passed with 4
    skipped, and 42, every one exit 0. Account for any difference.

G8  Markers, paths, commit shapes and object ids. Line-anchored
    `^<<<SLICE ` and `^<<<END ` both 0 in `.agent/plan.md` at C1,
    `.agent/live_review.md` at C2 and every file C3 writes, against the
    same counts over the COMMITTED C0a blob as a CONTROL, where they are
    NOT 0. ONLY the line-anchored reading is ordered — LEDGER25 quotes both
    markers inside backticks mid-line, so a raw SUBSTRING count is
    unmeetable and is NOT ordered. `git diff --name-only <base>..C3` names
    NO path under `docs/`, `packages/` or `tests/`, and none of
    `.agent/context.md`, either inventory file,
    `apps/ui/src/components/panels/RightLivePanel.tsx`,
    `apps/ui/src/api/decisionOrder.ts`, `apps/ui/src/RemedyApp.tsx` or
    `apps/ui/src/components/graph/GraphFilterChips.tsx`; the range path set
    MINUS the change set is EMPTY and the change set MINUS the range is
    exactly `.agent/handoff.md`, which C4 writes. Over C0a..C3 report per
    commit that it is single-parent and its INSERTION count — the `+` column
    only, per AGENTS.md DECISION F104 D1 — each under 500; those same
    numbers fill the `+/-` column of the `## Commits` table, derived from
    `git diff --numstat` and NOT from `git commit`'s own summary, and you
    report that the two agree cell for cell (§3 item 28). Report
    `git ls-files .remedy-wt` as 0 and `git ls-files` over `*.zip` as 0.
    FOR THE REFLOG state SCOPE and FIELD: over THIS ROUND'S entries only, by
    the OPERATION PREFIX before the first colon of `git reflog --format=%gs`,
    report `amend`, `rebase` and `cherry` each 0 and how many you scoped to. Finally extract every SHA-shaped
    token from the COMMITTED C0a blob with the word-bounded pattern
    matching 7 to 40 hex characters — whose boundaries do NOT match the
    64-char sha256 digest this block also carries — pass each to
    `git cat-file -t`, and report the token count YOUR extractor measured,
    the type per token, and the FAILING SET, which MUST BE EMPTY. THE TYPES
    ARE NOT ALL `commit`: LEDGER25 quotes the git BLOB id
    `141e5735d7f3f9610334f80bc0bf34add3702fa7`, resolved before emission.

G9  The push. AFTER C4, run `git push origin feature/f031-decision-inbox`.
    No `--force`, no `--force-with-lease`, no history rewrite, no branch
    deletion, no pull request. THAT PUSH'S OUTCOME IS NOT A VALUE OF ANY
    FILE THIS ROUND WRITES: the reviewer measures the pushed tips at the
    next gate and records them in the R25 entry of `.agent/live_review.md`.
    In `## External actions` write the push COMMAND and that sentence. In
    the item-status table the push row is `done`, reason "ordered after C4;
    outcome carried by G9 to the reviewer". Report the real outcome in your
    final message.

── Handback ──────────────────────────────────────────────────
Rewrite `.agent/handoff.md` at C4 per docs/agents/handback_template.md:
feature and round, branch, base and commit SHAs, a changed-files table per
commit, the item-status table covering C0a through C4, S1 through S5 and
the push, ONE LINE PER GATE with its real result, the finding counts, and
the next expected action. Carry the `Fortschritt:` block above VERBATIM —
count its lines yourself; no numeral is stated here.

EVERY NUMERAL YOUR HANDBACK STATES ABOUT A LIST IS COUNTED MECHANICALLY
BEFORE YOU COMMIT IT, or the list is named and NO numeral is given (R-0441).
Any finding count carries the RULE and the COMMIT it was measured at
(F009 D10); a narrower set is "the findings this feature must still act on".

THE HANDBACK LINE CAP: this block states no cap and no tier. Resolve it
from AGENTS.md under `### handoff.md` against the commit count constraint 4
fixes, and report BOTH that count and the tier. If the MANDATED content
does not fit, exceed it and carry a DECISION D15 "Deviations, declared"
line naming your measured count as a NUMERAL (R-0430) and the content
behind it. Never drop a section to fit; claim no token cap.

THIS ROUND ENDS THE SESSION, so your `## Next` section is the next
session's first instruction and names, in order: that it reads
`.agent/STOP` from disk as Phase 1 rule 1 BEFORE the Open PR Gate as rule
2; that the R25 verdict is UNRECORDED and owed by the next round's ledger
commit (DECISION F085 D9); and that T002b is CLOSED by this round, so the
next work is T003 per DECISION F031 D4, whose first round also carries
R-0682's `role="group"` fix in both files that need it.

Declare every deviation, contradiction and assumption.
──────────────────────────────────────────────────────────────

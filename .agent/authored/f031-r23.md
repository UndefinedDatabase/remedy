── STEP R23 — F031 Decision inbox ────────────────────────────
Goal:        T002b FILTERING, THE HALF THAT SHOWS. `DecisionInboxCard` owns
             the chosen type in its own state, draws the chips
             `decisionTypeChoices` derives and shows the quiet line
             `decisionInboxView` returns when none survive — the seam R22
             built the view shape for. The two remaining `R-0593` comments in
             this feature's reach are repaired, and the R22 verdict written.

Fortschritt: ~78 % (F031 claimed; R1 through R22 landed, R22 gated here ·
             T001 SHIPPED · T002a MODEL shipped, wired and RENDERED ·
             T002b ORDERING SHIPPED and gated · T002b FILTER shipped whole
             here, model at R22 and control now · T002b badge und T003 offen)
             — Schaetzung

Bundle:      C0a save this block · C0b mirror it into last_block · C1 the
             plan · C2 the R22 gate entry · C3 the control, its styles, the
             two comment repairs and DECISION F031 D8 · C4 handback.

Change set:  exactly these paths, nothing else —
             .agent/authored/f031-r23.md                       (C0a)
             .agent/last_block.md                              (C0b)
             .agent/plan.md                                    (C1)
             .agent/live_review.md                             (C2)
             apps/ui/src/components/panels/DecisionInboxCard.tsx     (C3)
             apps/ui/src/components/panels/RightLivePanel.module.css (C3)
             apps/ui/src/api/decisionCard.ts                   (C3, comment)
             .agent/decisions.md                               (C3, D8)
             .agent/handoff.md                                 (C4)
             This list bounds the round's WRITES, not its ACTIONS: the push
             named in G9 is ordered explicitly and is not a file (R-0674).
             `RightLivePanel.tsx` is NOT here: it keeps handing
             `orderDecisionInbox(dashboard.decisionInbox)` to the card, and
             the state lives in the card — the shape `component_spec.md`
             fixes for `GraphFilterChips` ("state stays in BrainGraphStage").

── Base ──────────────────────────────────────────────────────
The round base is `879bd137a008c982c6f54ffc9e7caf13d45a3dc0`, the R22
handback commit and the tip of `feature/f031-decision-inbox`, local and
remote EQUAL — the reviewer measured both with `git ls-remote` at the R22
gate. Stay on that branch; create none, never commit to `main`. Every
SHA-shaped token here resolved under `git cat-file -t` before emission;
the types are NOT all `commit`, and G8 does not ask them to be.

Readings the reviewer MEASURED at that base, re-checkable there:
- `.agent/live_review.md` 657516 bytes; `^- R-\d+ — ` 242 all DISTINCT,
  maximum `R-0681`; `^Done: R-\d+ — ` 4, so the §3 item 10 open set is
  238; `^Recurrence: R-` 18; `^Landed: R-` 0. THE GATE SERIES IS SPLIT by
  DECISION F031 D7: `^Gate: R\d+ — ` 19, frozen, and
  `^Gate: F\d+ R\d+ — ` 3, those three being `F031 R19`, `F031 R20` and
  `F031 R21`.
- `.agent/plan.md` 48 lines, 2811 bytes. `docs/roadmap/**` is UNTOUCHED,
  so the §3 docs-round gate is not earned and is not ordered.
- `apps/ui`: `npm run typecheck` exit 0, zero diagnostics; `npm run
  test:unit` exit 0 at 23 files and 352 tests, of which `decisionCard.test.ts`
  is 27, `decisionOrder.test.ts` 16 and `decisionFilter.test.ts` 20.
- The Python suites, every one exit 0: `tests/ui_server/` 474,
  `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16,
  `tests/ui_contracts/` 525 passed with 4 skipped, `test_golden_path` 42.
- THE SUITE GUARDS OVER THE FILES C3 REWRITES were read first (§3 item 7):
  `tests/ui_contracts/test_ux_quality.py` reads `RightLivePanel.module.css`
  by SUBSTRING PRESENCE only, and NO `count(` or `== 1` assertion over
  either `apps/` file exists under `tests/`, so appending classes is safe.
- THIS BLOCK'S OWN TWO CAPS, measured on its final bytes before emission
  and stated so your re-measurement can disagree with the reviewer's, are
  490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE (DECISION F085
  D5). G2 orders you to report both from the COMMITTED blob.

── Constraints ───────────────────────────────────────────────
1. Apply every authored SLICE BYTE FOR BYTE. Never retype, rewrap or
   "fix" one. If a slice looks wrong, apply it verbatim and DECLARE the
   disagreement: a contradiction in this block is the reviewer's defect.
2. THE PRODUCTION CHANGE AND DECISION D8 ARE DESCRIBED, NOT SLICED. The
   numbered specification S1 through S4 fixes behaviour, structure, style
   and copy; YOU write that code and that decision entry under AGENTS.md's
   Mandatory Self-Review Loop and its File Editing Safety Rules. Where the
   spec is silent, prefer the idiom the neighbouring module already uses.
   Where the spec is WRONG, say so in the handback and do the right thing.
3. Slice transport. This block is saved verbatim as
   `.agent/authored/f031-r23.md` at C0a and mirrored byte-identically into
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
7. The slices this block carries are the whole text PLANF031R23 and the
   appended text LEDGER23. This paragraph names them and states no count;
   G2 orders you to report the count YOUR extractor measured.
8. THE ONE APPEND'S SHAPE, STATED ONCE HERE, WITH EVERY GATE NAMING THIS
   PARAGRAPH RATHER THAN RESTATING IT. Under the newline-INCLUDED
   convention each slice already ends in a newline, so `.agent/live_review.md`
   after C2 is EXACTLY: its blob at C1, then one newline, then LEDGER23 —
   and it receives NOTHING ELSE in that commit (R-0657). LEDGER23's own
   paragraph count is yours to measure; this paragraph states no number.
   `.agent/decisions.md` also GROWS at C3, but by text YOU author under S4,
   so no equality gate is ordered over it and none may be reported.
9. THIS BLOCK CARRIES NO FROM/TO PAIR, so no containment test is reported
   and no FROM-zero count is ordered (§3 item 15). The plan is a WHOLE-FILE
   replacement and LEDGER23 is an append.
10. THIS ROUND MINTS NO FINDING ID AND RESOLVES NONE. `^- R-\d+ — ` must
    be 242 before and after, maximum staying `R-0681`, and `^Done: R-` and
    `^Landed: R-` UNCHANGED at 4 and 0, so the §3 item 10 open set stays
    238. `^Recurrence: R-` stays 18. WRITE NO `Landed:` LINE FOR R-0593
    even though S3 repairs its last two instances inside this feature: the
    instances in `packages/orchestration/release_gate.py` and
    `pyproject.toml` are OUTSIDE F031 and untouched, so R-0593 stays OPEN,
    and only reviewer-authored text may record what a repair settled
    (§4.4). R-0593's landed paragraph and its `Recurrence:` paragraph are
    NOT edited (§3 item 20).
11. TOUCH NO DOCUMENT AND NO OTHER CODE. Nothing under `docs/`,
    `packages/` or `tests/` is edited, and neither `.agent/context.md` nor
    either `f031_*_inventory.md`. Inside `apps/` only the three paths the
    change set names are written — NOT `RightLivePanel.tsx`, NOT
    `decisionFilter.ts`, NOT `decisionOrder.ts`, no test file. THIS ROUND
    ADDS NO TEST: D5 rules no test reaches this markup, and G6 MEASURES it.
12. Destructive verification runs ONLY in a disposable `git worktree`
    under `.remedy-wt/`, removed BY ITS EXACT PATH (R-0662) and before the
    G7 suites. Everything already there is pre-existing scratch belonging
    to no commit, this block's own file included: create no worktree at an
    existing path, and delete nothing you did not create.

── Specification (S1–S4) — the production change ─────────────
S1  THE CONTROL, in `apps/ui/src/components/panels/DecisionInboxCard.tsx`.
    Import `useState` from `react` — the idiom
    `components/graph/BrainGraphStage.tsx` uses — and `DECISION_FILTER_ALL`
    plus `decisionInboxView` from `../../api/decisionFilter`. Hold the
    chosen type as `useState<string>(DECISION_FILTER_ALL)`.
    THE GUARD IS THE LOAD-BEARING LINE: the existing
    `if (decisions.length === 0) return null;` keeps reading the UNFILTERED
    prop and is NOT rewritten to read the filtered list, or the card would
    unmount with its own control inside it and strand the operator.
    Then compute the view ONCE per render from the prop and the state, draw
    one `<button>` per `choices` entry, list `visible` through the existing
    `decisionRow` markup UNCHANGED, and where `emptyMessage` is non-null
    render that single line INSTEAD of the list. Every string still comes
    from a field, so this file chooses no copy of its own, and NO NEW
    BRANCH ON A DECISION'S `type` OR `status` enters it: adding a filter
    leaves the header's architecture line true, because the filter
    dispatches on nothing.
    A11y, per `component_spec.md`'s FilterChips entry: each chip is a
    `<button type="button">` carrying `aria-pressed` for whether it is the
    chosen value, the chip row carries an `aria-label`, and the region
    holding the list carries `aria-live="polite"` so a filter change
    announces instead of silently reflowing.

S2  THE STYLES, appended to
    `apps/ui/src/components/panels/RightLivePanel.module.css` — new class
    names only; EDIT NO EXISTING RULE, since `test_ux_quality.py` reads
    this file for `taskRow`, `done`, `current`, `suggested`, `overflow` and
    `.panel`. A row class for the chip strip and a chip class on the CARD's
    own chip scale that `.decisionChip` sets — pill radius via
    `var(--remedy-radius-pill)`, the `--remedy-line` border, small type —
    plus a selected state under DECISION F031 D8, with colour from
    `--remedy-*` tokens wherever one exists. The selected chip is NEVER
    distinguished by colour alone (`ux_spec.md` §14: "never color-only
    state changes"): it also carries weight or a border change. Give it a
    `:focus-visible` ring, since §14 rules focus a 2px `--remedy-focus`
    outer ring and these are the panel's first interactive chips.

S3  THE LAST TWO `R-0593` REPAIRS IN THIS FEATURE'S REACH, at C3.
    (a) `DecisionInboxCard.tsx`'s header still reads that Remedy
    "deliberately does NOT sort, filter, count or answer here: ordering
    over age and blocked size and the inbox badge are T002b's subject".
    FILTERING IS HERE as of this round, so that sentence is about to be
    false as well as undiscoverable. Rewrite it for what is true after S1:
    the chosen type lives in this component's state while the RULES live in
    `../../api/decisionFilter`, ordering in `../../api/decisionOrder`, the
    badge's COUNT is still absent everywhere, answering still T003's.
    (b) `apps/ui/src/api/decisionCard.ts`'s `decisionCardModels` docstring
    still reads "the rule over age and blocked size is T002b's subject" —
    the same one-directional gap the R22 handback registered as its
    deviation 5 and left here. Rewrite that sentence to NAME
    `./decisionOrder.ts` as the module holding the rule, keeping the point
    it already makes: that a model which quietly re-sorted would make the
    rule impossible to see. CHANGE NOTHING ELSE IN THAT FILE — no export,
    no signature, no behaviour — which is why `decisionCard.test.ts` must
    still measure exactly 27 at G7.

S4  DECISION F031 D8, appended to `.agent/decisions.md` in the shape D1
    through D7 already use there, ruling the ONE visual deviation this round
    takes — `.agent/context.md` binds `docs/ui/design_reference/` and wants a
    technical reason for any departure. CHOSEN: the chips take the CARD's
    chip scale, not the glass dock of `ux_spec.md` §13, keeping §13's
    selected-chip treatment and `component_spec.md`'s `aria-pressed`. WHY:
    §13 specifies that dock for the GRAPH STAGE — a floating overlay on the
    dark canvas, radius 999, backdrop blur, 30px chips — and the inbox is a
    card inside the right panel, which already supplies the glass, so a dock
    there would outweigh the 13px titles above it and double the glass.
    ALTERNATIVE: reusing `GraphFilterChips` verbatim, rejected because its
    `GraphFilter` union is a FIXED four-value list while the inbox's choices
    are DERIVED, so adopting it would reintroduce the hardcoded type list
    `decisionFilter.ts` refuses to have. REVERSE by giving the chip class
    the `GraphFilterChips.module.css` dock values.

── Authored slices ───────────────────────────────────────────

<<<SLICE PLANF031R23
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `f031_*_inventory.md` the inventories, `.agent/decisions.md` D1–D8.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R23 CLOSES T002b's filtering half: `DecisionInboxCard` holds the chosen type in
its own state, draws the chips `decisionTypeChoices` derives and shows the quiet
line `decisionInboxView` returns when none survive. It also repairs the last two
`R-0593` comments inside this feature and writes the R22 verdict.

## Next Steps
1. T002b BADGE under DECISION F031 D2: it re-derives on refetch over the
   existing SSE stream, no new event kind, D2's two constant-zero counters
   replaced.
2. T003 wires answering through the existing write channel and rules
   `NeedsAttentionCard` (DECISION F031 D4).
3. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- THE EMPTY-STATE TRAP IS LIVE THIS ROUND: `DecisionInboxCard` opens with
  `if (decisions.length === 0) return null;`, and that guard must keep reading
  the UNFILTERED prop. Filtering to zero would otherwise unmount the card AND
  its own control and strand the operator with no way back, which is the whole
  reason `decisionInboxView` returns a quiet line instead.
- NO TEST REACHES THE MARKUP under DECISION F031 D5, so this round's `.tsx` is
  pinned by `tsc`, by structure and by review alone. Every branch that could
  live in `apps/ui/src/api/` already does, and R23 adds no test by design.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 238 at `aa48d967`, unchanged by this round.
- The findings THIS FEATURE MUST STILL ACT ON are R-0403, R-0413, R-0431,
  R-0441, R-0445, R-0471, R-0495, R-0533, R-0574, R-0593, R-0601, R-0622,
  R-0625, R-0632, R-0672, R-0674, R-0675, R-0676, R-0677, R-0678 and R-0679;
  R-0495 and R-0574 are the two Highs.
- BLOCK CAPS ARE TWO, not one: 490 lines TOTAL (DECISION F085 D6) and 400 lines
  PROSE (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R23

<<<SLICE LEDGER23
Gate: F031 R22 — the F031 R22 entry. R22 PASSED ON EVERY ONE OF ITS NINE GATES, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk rather than reading the handback back; every value that handback states reproduced exactly, and R22 earns no finding. TRANSPORT HELD IN ITS STRONGEST FORM, cmp-against-scratchpad rather than the digest fallback: the reviewer's own emitted `.remedy-wt/f031-r22.md`, the C0a blob committed at `7de87810`, the C0b blob committed at `296ea957`, and `.agent/last_block.md` read off disk at `879bd137` are ALL FOUR byte-identical at sha256 `1c305462638d726b6bf15a3321e04022d4d6a3914f4663637a0c317aa7e95298` over 34109 bytes and 446 lines, C0a and C0b resolving to the SAME git blob `52f6a0ca81202278eeb67aee5ffaa7f7fa501f9e`. THE EXTRACTION printed 2 slices, 49 content lines and 446 total, so PROSE was 446 − 49 = 397 against the 400-line cap DECISION F085 D5 sets and TOTAL 446 against the 490 DECISION F085 D6 sets — inside both, and the reviewer notes that 397 against 400 is three lines of margin, which is why R23's design was measured against the caps before its spec was written rather than after. THE PLAN at `b5eb6cd0` equals PLANF031R22 exactly at 2811 bytes and 48 lines, with the trailing-newline-removed control FALSE, `^## Goal$` 1 and `^## Next Steps$` 1, and 48 strictly under the 50 AGENTS.md sets. THE C2 APPEND SATISFIED WHOLE-FILE EQUALITY: `.agent/live_review.md` at `aa48d967` is its C1 blob plus one newline plus LEDGER22, at 651806 + 1 + 5709 = 657516 against an actual 657516, and the SECOND, INDEPENDENT READER AGREED — a blank-line split moves the unit count 304 to 305 and its last 1 unit equals LEDGER22's paragraph once trailing newlines are rstripped on BOTH sides, the handling the R21 entry already recorded as necessary. THE NEGATIVE CONTROL WAS RUN IN MEMORY, never on disk, flipping one byte inside the appended region: both readers REJECT the mutant and both ACCEPT the true file, so neither reading is vacuous. THE SETS MOVED ONLY WHERE CONSTRAINT 10 ALLOWED: `^- R-\d+ — ` 242 to 242 all DISTINCT, ids ADDED and ids REMOVED both the EMPTY SET, maximum `R-0681` unchanged, `^Done: R-` 4 to 4, `^Landed: R-` 0 to 0 and `^Recurrence: R-` 18 to 18. THE SPLIT SERIES BEHAVED AS DECISION F031 D7 RULES for a third round running: `^Gate: R\d+ — ` 19 to 19, frozen, and `^Gate: F\d+ R\d+ — ` 2 to 3, the added key exactly `F031 R21`, all keys DISTINCT, so the §3 item 26 header collision this series exists to prevent did not occur. The §3 item 10 open set is 238 at `aa48d967`, and `- R-0593 — ` occurs exactly ONCE line-anchored and `^Recurrence: R-0593` exactly ONCE, so its paragraphs were not edited. THE PROBES ARE THE REVIEWER'S OWN MUTANTS, written in a disposable worktree at `22fc6193` and removed by exact path, `git worktree list` 1 line and `git status --porcelain` 0 after: UNMUTATED exit 0 at 1 file and 20 tests; PROBE B, the `DECISION_FILTER_ALL` special case removed from `filterDecisionsByType`, REAL exit 1 with 2 failed, exactly the two the handback names — `filterDecisionsByType > yields every model under the all value` and `decisionInboxView > reports no empty message while something is visible`. PROBE A DIVERGED FROM THE HANDBACK AND THE DIVERGENCE IS THE MUTANT, NOT THE RECORD: the reviewer's fixed choice list kept the All chip's `count: models.length`, so it went REAL exit 1 with 7 failed where the handback reports 9, its 7 being 6 `decisionTypeChoices` tests plus `decisionInboxView > never throws, however broken the models it is handed`. The two the reviewer's weaker mutant spared are precisely the two that read the All chip's count — `puts the all choice first and counts every model on it` and `still offers the all choice when the filter emptied the list, so the operator can get back` — so the handback's 9 is the honest reading of a more aggressive fixed list, both mutants kill the extensibility test first, and the derivation is pinned under either. THE SUITES ARE THE REVIEWER'S OWN, run SERIALLY, never two alive at once, every one a REAL exit 0: `npm run typecheck` with ZERO diagnostics, its stdout holding only npm's two script-echo lines and its stderr empty; `npm run test:unit` at 23 files and 352 tests with `decisionCard.test.ts` 27 and `decisionOrder.test.ts` 16 both UNMOVED and the new `decisionFilter.test.ts` at 20, which is the whole of the 22-to-23 and 332-to-352 movement; and in Python `tests/ui_server/` 474, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16, `tests/ui_contracts/` 525 passed with 4 skipped and `test_golden_path` 42 — every count identical to the base readings. THE MODULE'S SURFACE IS WHAT S1 ORDERED: `decisionFilter.ts` at `22fc6193` carries exactly ONE import line, `import type { DecisionCardModel } from "./decisionCard";`, its `switch` count is 0 raw AND comment-stripped beside `brainStreamDriver.ts` at 1, and each of the six S1 names grep to exactly one `export` there. THE UNTYPED-CHIP CLAIM WAS CHECKED AGAINST THE CODE IT DESCRIBES rather than taken on trust: `cardText` in `decisionCard.ts` returns `typeof value === "string" ? value : ""`, so `buildDecisionCardModel` really does default a missing `type` to the empty string, and `modelType` mirrors that same coercion — the comment is true and the empty-type chip reaches real cards. HYGIENE HELD: line-anchored `^<<<SLICE ` and `^<<<END ` are 0 in `.agent/plan.md` at `b5eb6cd0`, `.agent/live_review.md` at `aa48d967` and all three `apps/` files at `22fc6193`, against a CONTROL of 2 and 2 over the C0a blob; the range names 7 paths, none under `docs/`, `packages/` or `tests/` and none of `.agent/decisions.md`, `.agent/context.md`, either inventory or `DecisionInboxCard.tsx`, with range-minus-change-set EMPTY and change-set-minus-range exactly `.agent/handoff.md`; the six commits of `f13b92c0`..`879bd137` are each SINGLE-PARENT with insertions 446, 323, 20, 2, 314 and 66 read from `git diff --numstat`, each under the 500 cap AGENTS.md DECISION F104 D1 sets, and the first five agree CELL FOR CELL with the `+/-` column of that handback's `## Commits` table, which is the §3 item 28 reading; `git ls-files .remedy-wt` 0 and the zip glob 0. THE BLOCK'S OWN OBJECT IDS RESOLVE: 19 SHA-shaped occurrences, 9 distinct, failing set EMPTY, 8 `commit` and one `blob`, that blob being `599e6675d9e5aa79fb038ca357f7b20e1498daf2`. THE PUSH DISCHARGED, which is the outcome G9 routed to the reviewer rather than to any file R22 wrote: measured with `git ls-remote`, `refs/heads/feature/f031-decision-inbox` and the local tip are both `879bd137a008c982c6f54ffc9e7caf13d45a3dc0`, and no pull request was created, no branch deleted and nothing merged. THE HANDBACK FITS ITS TIER WITH NO OVERAGE: 97 lines against the 100 AGENTS.md allows for its 6 commits, every mandated section present. THE FIVE DECLARED DEVIATIONS ARE ADJUDICATED AND NONE IS A FINDING. Deviation 1, routing the two `apps/ui` lines and the six pytest lines through `subprocess.run`, changed HOW and not WHAT and preserved REAL exit codes a pipe would have swallowed. Deviation 2 IS THE REVIEWER'S OWN DEFECT, correctly declared: the delegating message stated 34097 bytes for a block that is 34109, and since the sha256 in that same message matched the real bytes the worker was right to authenticate by digest and proceed — the wrong numeral never reached disk, it has no carrier left to repair, and it is recorded here rather than minted as an id because the class already sits OPEN as the R-0441 family. Deviation 3 is the gate quoting its own marker, a known shape: `- R-0593 — ` is line-anchored once as constraint 10 ordered, and its second raw-substring occurrence is LEDGER22's own sentence quoting the pattern. Deviation 4 IS A REAL DESIGN CATCH BY THE WORKER, not a deviation to forgive: `DECISION_FILTER_ALL` is the ordinary string `"all"`, so a decision typed literally `"all"` would have produced a second chip with a duplicate `value`, and excluding the sentinel from the concrete choices while the All chip keeps counting and showing those cards is the right resolution, pinned by its own named test, which the reviewer's PROBE A killed. Deviation 5 registers the `decisionCardModels` docstring left unrepaired under S4's CHANGE-NOTHING-ELSE clause, and R23's S3(b) carries it. THE VERDICT IS PASS.
<<<END LEDGER23

── Done when ─────────────────────────────────────────────────
Run every gate yourself, record its REAL exit code and REAL output, and
report ONE LINE PER GATE in the handback, transcripts kept out of it
(R-0582). "Green" as a word is a finding. Every gate runs at a commit
STRICTLY EARLIER than C4 (§3 item 31); G9's push runs after it and names
its own carrier.

G1  Branch, cleanliness, transport. `git branch --show-current` prints
    `feature/f031-decision-inbox` and NOT `main`; `.agent/STOP` read from
    disk is ABSENT before C0a and again before C4; `git status --porcelain`
    line count after each of C0a, C0b, C1, C2 and C3 is 0. Then report
    sha256, byte count and line count for FOUR readings —
    `.remedy-wt/f031-r23.md` before C0a, the committed C0a blob, the
    committed C0b blob, and `.agent/last_block.md` off disk after C0b — all
    four EQUAL, and the git blob id of C0a's and C0b's file, the SAME id.

G2  Extraction and the block's own two caps. Run your extractor over the
    COMMITTED C0a blob and report the slice count, the CONTENT lines inside
    markers, and the TOTAL line count — the numbers YOUR extractor printed.
    Then report PROSE, computed as TOTAL minus CONTENT, against the two
    caps the Base section names. If either is exceeded, say so plainly and
    continue: an oversize block is the reviewer's defect to record, not
    yours to fix.

G3  The plan. `.agent/plan.md` at C1 is byte-equal to PLANF031R23 under
    your stated newline convention; report slice length, file length and
    convention. NEGATIVE CONTROL: NOT byte-equal to that slice with its
    trailing newline REMOVED. `^## Goal$` 1, `^## Next Steps$` 1, `wc -l`
    STRICTLY under 50.

G4  The C2 append, as ONE equality over the whole file, in the shape
    constraint 8 states — name that paragraph, do not restate its formula.
    Report the boolean and the byte arithmetic against the C1 length you
    measure yourself. Report a SECOND, INDEPENDENT reading: split the
    committed file on blank lines, take the LAST N units, and confirm they
    equal LEDGER23's paragraphs IN ORDER, where N is the number YOUR split
    measured; give the unit count before and after, and STATE YOUR
    TRAILING-NEWLINE HANDLING, because the R21 and R22 entries both record
    that a naive split reports FALSE on a byte-perfect file. NEGATIVE
    CONTROL: flip ONE byte inside the appended text; BOTH readers must
    reject the mutant and BOTH accept the true file. Do that flip in memory
    or under a disposable worktree per constraint 12, never on the tracked
    file.

G5  The ledger sets, base versus C2 in `.agent/live_review.md`:
    `^- R-\d+ — ` 242 → 242 all DISTINCT, ids ADDED and REMOVED both the
    EMPTY SET, maximum `R-0681` → `R-0681`; `^Done: R-` 4 → 4,
    `^Landed: R-` 0 → 0 and `^Recurrence: R-` 18 → 18, all UNCHANGED.
    `^Gate: R\d+ — ` 19 → 19 UNCHANGED, and `^Gate: F\d+ R\d+ — ` 3 → 4,
    the ADDED key being exactly `F031 R22`, all keys DISTINCT (§3 item 26).
    Report the §3 item 10 open set at C2 — paragraphs minus `Done:` lines —
    which must be 238. Report that `- R-0593 — ` still occurs exactly ONCE
    line-anchored and that `^Recurrence: R-0593` still occurs exactly ONCE,
    since constraint 10 forbids editing either paragraph.

G6  THE COVERAGE GAP, MEASURED RATHER THAN ASSUMED, in a disposable
    worktree at C3 per constraint 12, with vitest run from the PRIMARY
    checkout's `apps/ui` so the primary's `node_modules` resolves:
      npx vitest run --config <PRIMARY>/apps/ui/vitest.config.ts \
        --root <WORKTREE>/apps/ui src/api/
    (a) THE TYPECHECK'S REACH, PROVED WITHOUT A MUTATION: tsc cannot run in
    a fresh worktree at all — the reviewer tried, and got 797 diagnostics at
    the base because a worktree has no `node_modules` and every `react`
    import fails to resolve (the R-0518 class). Instead, in the PRIMARY at
    `apps/ui`, run `npx tsc --noEmit --listFiles`, report its REAL exit code
    and the file count YOUR run printed, and report that the list holds
    `DecisionInboxCard.tsx` exactly ONCE — the evidence G7's typecheck is
    not blind to this markup. The reviewer measured exit 0 and 996 files at
    `879bd137`; account for any difference.
    (b) THE MARKUP PROBE, ordered as a PROBE and NOT as a colour because
    §3 item 5 forbids ordering a red whose branch no test reaches: change
    the guard so it reads the FILTERED list — the empty-state trap S1 names
    — then run the vitest line above and REPORT WHETHER ANY TEST FAILS AT
    ALL. The reviewer EXPECTS GREEN, and green is the honest answer to
    record: it MEASURES the gap DECISION F031 D5 accepts, and is the
    evidence this `.tsx` is pinned by `tsc`, structure and review rather
    than by the suite. A RED means a test does reach the markup, which is
    better news and is reported as such. Restore the file. Report
    `git worktree list` as 1 line after the removals, naming exact paths.

G7  The card's structure, then the suites. Over
    `apps/ui/src/components/panels/DecisionInboxCard.tsx` at C3 report, as
    counts YOU measured: that `aria-pressed` occurs at least once, that
    `aria-live` occurs at least once, that `useState` occurs, that the
    literal guard `if (decisions.length === 0) return null;` occurs exactly
    ONCE and that the token `decisions.length` does NOT appear inside any
    line also containing `visible` — the empty-state trap, checked as text
    because no test reaches it. Report the `switch` count over that file,
    which must be 0 both raw and comment-stripped, beside the count over
    `apps/ui/src/api/brainStreamDriver.ts`, which the reviewer measured as
    exactly 1 at `879bd137`, so a zero here is a measurement and not a blind
    command. Then in the PRIMARY checkout at the C3 tree, all REAL exit 0,
    run SERIALLY and never two alive at once, with `git worktree list`
    reported as 1 line immediately BEFORE the first of them. At `apps/ui`:
    `npm run typecheck` with ZERO diagnostics on stdout and stderr;
    `npm run test:unit`, reporting the file and test counts YOUR run
    measured — `decisionCard.test.ts` must still be exactly 27,
    `decisionOrder.test.ts` exactly 16 and `decisionFilter.test.ts` exactly
    20, any movement in any of the three being a finding, and since this
    round adds no test the totals must stay at the 23 files and 352 tests
    the Base section records. Then in Python, by these exact command lines
    with no extra flag:
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/ui_contracts/ -q
      python3 -m pytest tests/cli/test_golden_path.py -q
    These are the four state readers a round rewriting `.agent/` state
    gates, plus `tests/ui_contracts/` — which READS
    `RightLivePanel.module.css`, so it is the gate S2's appended classes
    must not disturb — plus the canary. The reviewer ran all six at
    `879bd137` with these exact lines and measured in that order 474, 52,
    21, 16, 525 passed with 4 skipped, and 42, every one exit 0. Account
    for any difference.

G8  Markers, paths, commit shapes and object ids. Line-anchored
    `^<<<SLICE ` and `^<<<END ` both 0 in `.agent/plan.md` at C1,
    `.agent/live_review.md` at C2 and every file C3 writes, against the
    same counts over the COMMITTED C0a blob as a CONTROL, where they are
    NOT 0. ONLY the line-anchored reading is ordered — LEDGER23 quotes both
    markers inside backticks mid-line, so a raw SUBSTRING count is
    unmeetable and is NOT ordered (the R22 deviation 3 shape, pre-empted). `git diff --name-only <base>..C3` names NO path under `docs/`,
    `packages/` or `tests/`, and neither `.agent/context.md` nor either
    inventory file nor `apps/ui/src/components/panels/RightLivePanel.tsx`
    nor `apps/ui/src/api/decisionFilter.ts`; the range path set MINUS the
    change set is EMPTY and the change set MINUS the range is exactly
    `.agent/handoff.md`, which C4 writes. Over C0a..C3 report per commit
    that it is single-parent and its INSERTION count — the `+` column only,
    per AGENTS.md DECISION F104 D1 — each under 500; those same numbers
    fill the `+/-` column of the `## Commits` table, derived from
    `git diff --numstat` and NOT from `git commit`'s own summary, and you
    report that the two agree cell for cell (§3 item 28). Report
    `git ls-files .remedy-wt` as 0 and `git ls-files` over `*.zip` as 0.
    FOR THE REFLOG state SCOPE and FIELD: over THIS ROUND'S entries only,
    by the OPERATION PREFIX before the first colon of
    `git reflog --format=%gs`, report `amend`, `rebase` and `cherry` each 0
    and how many entries you scoped to. Finally extract every SHA-shaped
    token from the COMMITTED C0a blob with the word-bounded pattern
    matching 7 to 40 hex characters — whose boundaries do NOT match the
    64-char sha256 digests this block also carries — pass each to
    `git cat-file -t`, and report the token count YOUR extractor measured,
    the type per token, and the FAILING SET, which MUST BE EMPTY. THE TYPES
    ARE NOT ALL `commit`: LEDGER23 quotes the git BLOB ids
    `599e6675d9e5aa79fb038ca357f7b20e1498daf2` and
    `52f6a0ca81202278eeb67aee5ffaa7f7fa501f9e`, both resolved before emission.

G9  The push. AFTER C4, run `git push origin feature/f031-decision-inbox`.
    No `--force`, no `--force-with-lease`, no history rewrite, no branch
    deletion, no pull request. THAT PUSH'S OUTCOME IS NOT A VALUE OF ANY
    FILE THIS ROUND WRITES: the reviewer measures the pushed tips at the
    next gate and records them in the R23 entry of `.agent/live_review.md`.
    In `## External actions` write the push COMMAND and that sentence. In
    the item-status table the push row is `done`, reason "ordered after C4;
    outcome carried by G9 to the reviewer". Report the real outcome in your
    final message.

── Handback ──────────────────────────────────────────────────
Rewrite `.agent/handoff.md` at C4 per docs/agents/handback_template.md:
feature and round, branch, base and commit SHAs, a changed-files table per
commit, the item-status table covering C0a through C4, S1 through S4 and
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
genuinely does not fit, exceed it and carry a DECISION D15 "Deviations,
declared" line naming your measured count as a NUMERAL (R-0430) and the
content behind it. Never drop a section to fit; claim no token cap.

THIS ROUND ENDS THE SESSION, so your `## Next` section is the next
session's first instruction and names, in order: that it reads
`.agent/STOP` from disk as Phase 1 rule 1 BEFORE the Open PR Gate as rule
2; that the R23 verdict is UNRECORDED and owed by the next round's ledger
commit (DECISION F085 D9); and that R24 is the T002b BADGE under DECISION
F031 D2, which re-derives on refetch over the existing SSE stream with no
new event kind and replaces D2's two constant-zero counters.

Declare every deviation, contradiction and assumption.
──────────────────────────────────────────────────────────────

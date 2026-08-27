── STEP R22 — F031 Decision inbox ────────────────────────────
Goal:        T002b FILTERING, the PURE HALF. A new `decisionFilter.ts`
             derives the offered types FROM the models present, applies the
             chosen one and says what an empty result means, with its tests
             beside it; `decisionCard.ts`'s stale absence note is repaired.
             The round also writes the R21 verdict, which by DECISION F085
             D9 no R21 artefact could carry. THE CONTROL AND ITS STYLES ARE
             R23's, and the reason is stated below rather than inferred.

Fortschritt: ~70 % (F031 claimed; R1 through R21 landed, R21 gated here ·
             T001 SHIPPED · T002a MODEL shipped, wired and RENDERED ·
             T002b ORDERING SHIPPED and gated · T002b filter MODEL ships
             here, its control R23 · T002b badge und T003 offen)
             — Schaetzung

Bundle:      C0a save this block · C0b mirror it into last_block · C1 the
             plan · C2 the R21 gate entry · C3 the pure filter module, its
             tests and the `decisionCard.ts` comment · C4 handback.

Change set:  exactly these paths, nothing else —
             .agent/authored/f031-r22.md                       (C0a)
             .agent/last_block.md                              (C0b)
             .agent/plan.md                                    (C1)
             .agent/live_review.md                             (C2)
             apps/ui/src/api/decisionFilter.ts                 (C3, NEW)
             apps/ui/src/api/decisionFilter.test.ts            (C3, NEW)
             apps/ui/src/api/decisionCard.ts                   (C3, comment)
             .agent/handoff.md                                 (C4)
             This list bounds the round's WRITES, not its ACTIONS: the push
             named in G9 is ordered explicitly and is not a file (R-0674).

WHY THE CONTROL IS NOT HERE, stated rather than left to be inferred: this
block sits under two caps, 490 lines TOTAL (DECISION F085 D6) and 400 lines
PROSE (DECISION F085 D5), and the reviewer measured a version carrying the
control's specification at 482 TOTAL and 436 PROSE — inside one cap and
over the other. The design was cut rather than the wording, exactly as D5
intends. `DecisionInboxCard.tsx` is therefore NOT in the change set and its
own absence note stays TRUE for this round, since nothing here makes that
component filter. R23 adds the control, repairs that second note, and is
where `docs/ui/design_reference/`'s FilterChips rules bind.

── Base ──────────────────────────────────────────────────────
The round base is `f13b92c0a8a978f631a961786b0870b7594e7cbe`, the R21
handback commit and the tip of `feature/f031-decision-inbox`, local and
remote EQUAL — the reviewer measured both with `git ls-remote` at the R21
gate. Stay on that branch; create none, never commit to `main`. Every
SHA-shaped token here resolved under `git cat-file -t` before emission;
the types are NOT all `commit` and G8 does not ask them to be.

Readings the reviewer MEASURED at that base, re-checkable there:
- `.agent/live_review.md` 651806 bytes; `^- R-\d+ — ` 242 all DISTINCT,
  maximum `R-0681`; `^Done: R-\d+ — ` 4, so the §3 item 10 open set is
  238; `^Recurrence: R-` 18; `^Landed: R-` 0. THE GATE SERIES IS SPLIT by
  DECISION F031 D7: `^Gate: R\d+ — ` 19, frozen, and
  `^Gate: F\d+ R\d+ — ` 2, those two being `F031 R19` and `F031 R20`.
- `.agent/plan.md` 48 lines, 2832 bytes. `docs/roadmap/**` is UNTOUCHED,
  so the §3 docs-round gate is not earned and is not ordered.
- `apps/ui`: `npm run typecheck` exit 0 with zero diagnostics;
  `npm run test:unit` exit 0 at 22 files and 332 tests, of which
  `decisionCard.test.ts` is 27 and `decisionOrder.test.ts` is 16.
- The Python suites, every one exit 0: `tests/ui_server/` 474,
  `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate`
  16, `test_golden_path` 42, and `tests/ui_contracts/` 525 passed with 4
  skipped. `tests/ui_contracts/` IS earned this round because the change
  set holds `apps/` paths; at R21 it was not.
- `apps/ui/src/api/brainStreamDriver.ts` contains exactly one `switch`,
  which is what makes G7's zero-count over the new module a measurement.
- THIS BLOCK'S OWN TWO CAPS, measured on its final bytes before emission
  and stated so your re-measurement can disagree with the reviewer's, are
  the two the paragraph above names. G2 orders you to report both from the
  COMMITTED blob.

── Constraints ───────────────────────────────────────────────
1. Apply every authored SLICE BYTE FOR BYTE. Never retype, rewrap or
   "fix" one. If a slice looks wrong, apply it verbatim and DECLARE the
   disagreement: a contradiction in this block is the reviewer's defect.
2. THE PRODUCTION CHANGE IS DESCRIBED, NOT SLICED. The numbered
   specification S1 through S4 fixes behaviour, seam, public surface and
   honesty rules; YOU write that code under AGENTS.md's Mandatory
   Self-Review Loop and its File Editing Safety Rules. Where the spec is
   silent, prefer the idiom the neighbouring module already uses. Where
   the spec is WRONG, say so in the handback and do the right thing.
3. Slice transport. This block is saved verbatim as
   `.agent/authored/f031-r22.md` at C0a and mirrored byte-identically into
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
7. The slices this block carries are the whole text PLANF031R22 and the
   appended text LEDGER22. This paragraph names them and states no count;
   G2 orders you to report the count YOUR extractor measured.
8. THE ONE APPEND'S SHAPE, STATED ONCE HERE, WITH EVERY GATE NAMING THIS
   PARAGRAPH RATHER THAN RESTATING IT. Under the newline-INCLUDED
   convention each slice already ends in a newline, so `.agent/live_review.md`
   after C2 is EXACTLY: its blob at C1, then one newline, then LEDGER22 —
   and it receives NOTHING ELSE in that commit (R-0657). LEDGER22's own
   paragraph count is yours to measure; this paragraph states no number.
9. THIS BLOCK CARRIES NO FROM/TO PAIR, so no containment test is reported
   and no FROM-zero count is ordered (§3 item 15). The plan is a WHOLE-FILE
   replacement and LEDGER22 is an append.
10. THIS ROUND MINTS NO FINDING ID AND RESOLVES NONE. `^- R-\d+ — ` must
    be 242 before and after, maximum staying `R-0681`, and `^Done: R-` and
    `^Landed: R-` UNCHANGED at 4 and 0, so the §3 item 10 open set stays
    238. `^Recurrence: R-` stays 18. WRITE NO `Landed:` LINE FOR R-0593
    even though S4 repairs one of its instances: its original instances in
    `packages/orchestration/release_gate.py` and `pyproject.toml` are
    untouched and the `DecisionInboxCard.tsx` one is R23's, so R-0593 stays
    OPEN, and only reviewer-authored text may record what a repair settled
    (§4.4). R-0593's landed paragraph and its `Recurrence:` paragraph are
    NOT edited (§3 item 20).
11. TOUCH NO DOCUMENT AND NO OTHER CODE. Nothing under `docs/`,
    `packages/` or `tests/` is edited, and neither `.agent/decisions.md`,
    `.agent/context.md` nor either `f031_*_inventory.md`. Inside `apps/`
    only the three paths the change set names are written — in particular
    NOT `DecisionInboxCard.tsx`, `RightLivePanel.tsx` or any `.module.css`.
    This round rules no DECISION.
12. Destructive verification runs ONLY in a disposable `git worktree`
    under `.remedy-wt/`, removed BY ITS EXACT PATH (R-0662) and before the
    G7 suites. Everything already there is pre-existing scratch belonging
    to no commit, this block's own file included: create no worktree at an
    existing path, and delete nothing you did not create.

── Specification (S1–S4) — the production change ─────────────
S1  NEW MODULE `apps/ui/src/api/decisionFilter.ts`, pure, importing only
    the model TYPE from `./decisionCard`. DECISION F031 D5 puts it here
    because the shipped `apps/ui/vitest.config.ts` includes
    `src/**/*.test.ts` and reaches no markup. Public surface:
      - `DECISION_FILTER_ALL`, the string constant `"all"`.
      - `DecisionTypeChoice`: `value: string`, `label: string`,
        `count: number`.
      - `decisionTypeChoices(models)` → `DecisionTypeChoice[]`.
      - `filterDecisionsByType(models, filter)` → `DecisionCardModel[]`.
      - `DecisionInboxView`: `choices: DecisionTypeChoice[]`,
        `visible: DecisionCardModel[]`, `emptyMessage: string | null`.
      - `decisionInboxView(models, filter)` → `DecisionInboxView`.
    Every list parameter is `readonly DecisionCardModel[]`. TOTAL BY
    CONSTRUCTION: no input makes any of these throw. THE SEAM IS NOT WIRED
    THIS ROUND — `RightLivePanel.tsx` keeps passing
    `orderDecisionInbox(dashboard.decisionInbox)` untouched, and neither
    `decisionCardModels` nor the `remedyApi.ts` projection nor
    `decisionOrder.ts` learns about filtering. R23 calls
    `decisionInboxView` from `DecisionInboxCard`, which is why the view
    shape exists now rather than later.

S2  (a) `decisionTypeChoices` DERIVES the offered types from the models it
    is given and from NOTHING ELSE — no hardcoded list, no `switch`, no
    type-to-widget map, no producer enum import. That is the architecture
    line `decisionCard.ts` already states, and a type this repository has
    never produced must appear as a choice the day some producer emits it.
    The result begins with the `DECISION_FILTER_ALL` choice labelled
    `"All"`, counting EVERY model; the concrete choices follow, one per
    DISTINCT `type` present, sorted ASCENDING by `value` under the default
    string comparison so the control is stable across refetches. A model
    whose `type` is the empty string — `buildDecisionCardModel` defaults it
    there — gets the choice `value: ""` with a label naming it untyped,
    because a card the control cannot reach is a card the operator loses.
    With no models the result is the `DECISION_FILTER_ALL` choice alone,
    counting 0.
    (b) `filterDecisionsByType` returns a NEW array and never mutates or
    reorders its input: `orderDecisionInbox` fixes the order upstream and
    `Array.prototype.filter` preserves it. `DECISION_FILTER_ALL` yields
    every model. Any other value yields the models whose `type` EQUALS it —
    including `""`, and including a value no model carries, which yields
    none.
    (c) `decisionInboxView` composes the two and adds `emptyMessage`, which
    is `null` whenever `visible` is non-empty, and otherwise a QUIET ONE
    LINE per `docs/ui/design_reference/ux_spec.md` §14 ("panels show quiet
    one-line empties, never illustrations") — distinct wording for the
    empty-under-`DECISION_FILTER_ALL` case and the empty-under-a-concrete-
    filter case, the second naming the filtered type so the operator reads
    why the list is empty rather than guessing. The wording is yours; it is
    the only copy this round invents.

S3  TESTS: `apps/ui/src/api/decisionFilter.test.ts`, built the way
    `decisionOrder.test.ts` builds models — through `buildDecisionCardModel`
    from a payload shaped like the endpoint's, never a hand-made lookalike.
    Cover at least: choices derived from the models present, with a type
    this repository has never produced appearing as a choice, NAMED as the
    extensibility property so a reader greps to it; the
    `DECISION_FILTER_ALL` choice first, counting every model; concrete
    choices sorted and DISTINCT; the empty-`type` choice; the per-choice
    counts; `DECISION_FILTER_ALL` yielding every model; a concrete filter
    yielding only its type; an unknown filter yielding none; ORDER
    PRESERVED through the filter; the input array NEITHER mutated NOR
    reordered; `emptyMessage` null when `visible` is non-empty and a string
    in both empty cases; and the no-models case. Report the count YOUR run
    measured; this block states no number for it.

S4  THE R-0593 REPAIR IN `apps/ui/src/api/decisionCard.ts`, at C3. Its
    header still reads that Remedy "deliberately does NOT sort, filter or
    count here: ordering over age and blocked size is T002b's subject". The
    claim is literally true and the DISCOVERABILITY is what is broken:
    AGENTS.md's Code Discoverability Conventions require a deliberate
    absence to be documented "where a reader would search for it", and a
    reader searching this file for the comparator is told only that it
    belongs to some future slice. Rewrite that sentence so it NAMES
    `./decisionOrder.ts` as the module holding the ordering and
    `./decisionFilter.ts` as the one holding the filtering, and narrows the
    remaining absence to what is genuinely still absent here — counting,
    which is the badge and is still T002b's. CHANGE NOTHING ELSE IN THAT
    FILE: no export, no signature, no behaviour, which is why
    `decisionCard.test.ts` must still measure exactly 27 at G7. The repair
    does NOT edit `.agent/live_review.md`; R-0593 stays OPEN under
    constraint 10 and the reviewer records what it settled at the next
    gate.

── Authored slices ───────────────────────────────────────────

<<<SLICE PLANF031R22
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `f031_*_inventory.md` the inventories, `.agent/decisions.md` D1–D7.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R22 ships the PURE HALF of T002b filtering: `decisionFilter.ts` derives the
offered types from the models present, applies the chosen one and says what an
empty result means, with its tests beside it, plus the `decisionCard.ts` comment
repair. It also writes the R21 verdict, which no R21 artefact could carry.

## Next Steps
1. R23 wires the control into `DecisionInboxCard` and repairs that file's own
   `Recurrence: R-0593` note. `docs/ui/design_reference/` is binding under
   `.agent/context.md`: the FilterChips section of `component_spec.md` rules the
   interaction, and a control authored without reading it is a §4.5 block
   condition, not a finding.
2. T002b BADGE under DECISION F031 D2: it re-derives on refetch over the
   existing SSE stream, no new event kind, D2's two constant-zero counters
   replaced.
3. T003 wires answering through the existing write channel and rules
   `NeedsAttentionCard` (DECISION F031 D4); then the integration-gate round and
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- THE EMPTY-STATE TRAP, waiting for R23: `DecisionInboxCard` opens with
  `if (decisions.length === 0) return null;`, and that guard must keep reading
  the UNFILTERED list. Filtering to zero matches would otherwise unmount the
  card AND its own control and strand the operator with no way back.
- NO TEST REACHES THE MARKUP under DECISION F031 D5, so every branch that can
  live in `apps/ui/src/api/` is placed there, where the shipped vitest config
  reaches it, and R23's markup stays a projection pinned by review alone.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 238 at `f13b92c0`, unchanged by this round.
- The findings THIS FEATURE MUST STILL ACT ON are R-0403, R-0413, R-0431,
  R-0441, R-0445, R-0471, R-0495, R-0533, R-0574, R-0593, R-0601, R-0622,
  R-0625, R-0632, R-0672, R-0674, R-0675, R-0676, R-0677, R-0678 and R-0679;
  R-0495 and R-0574 are the two Highs.
- BLOCK CAPS ARE TWO, not one: 490 lines TOTAL (DECISION F085 D6) and 400 lines
  PROSE (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R22

<<<SLICE LEDGER22
Gate: F031 R21 — the F031 R21 entry. R21 PASSED ON EVERY ONE OF ITS NINE GATES, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk rather than reading the handback back; every value that handback states reproduced exactly, and R21 earns no finding. TRANSPORT HELD IN ITS STRONGEST FORM, cmp-against-scratchpad rather than the digest fallback: the reviewer's own emitted `.remedy-wt/f031-r21.md`, the C0a blob committed at `540ff83b`, the C0b blob committed at `b7b345a4`, and `.agent/last_block.md` read off disk at `f13b92c0` are ALL FOUR byte-identical at sha256 `0fcea101e1f37782cf9565142a8269d23a8a497c2577d58f056d236cad862d75` over 29854 bytes and 340 lines, C0a and C0b resolving to the SAME git blob `599e6675d9e5aa79fb038ca357f7b20e1498daf2`. THE EXTRACTION printed 3 slices, 50 content lines and 340 total, so PROSE was 340 − 50 = 290 against the 400-line cap DECISION F085 D5 sets and TOTAL 340 against the 490 DECISION F085 D6 sets — comfortably inside both, which the block the R20 entry reports on was not. THE PLAN at `b2c00ebc` equals PLANF031R21 exactly at 2832 bytes and 48 lines, with the trailing-newline-removed control FALSE, `^## Goal$` 1 and `^## Next Steps$` 1, and 48 strictly under the 50 AGENTS.md sets. THE ONE COMMIT CARRYING TWO APPENDS SATISFIED WHOLE-FILE EQUALITY: `.agent/live_review.md` at `259e4fd9` is its C1 blob plus one newline plus LEDGER21 plus one newline plus EVIDENCE0593, at 642904 + 1 + 6827 + 1 + 2073 = 651806 against an actual 651806. THE SECOND, INDEPENDENT READER AGREED, and the reviewer records HOW because its own first attempt did not: a blank-line split moves the unit count 302 to 304 and its last two units equal LEDGER21's paragraph then EVIDENCE0593's IN ORDER only once trailing newlines are normalised on both sides, since the file's final unit keeps the newline the slice's rstripped paragraph has lost. The naive comparison reports FALSE on a byte-perfect file, and a worker who reported that reading as red would have been wrong about a correct commit — which is why this entry states the handling rather than the verdict alone. THE SETS MOVED ONLY WHERE CONSTRAINT 9 ALLOWED: `^- R-\d+ — ` 242 to 242 all DISTINCT, ids ADDED and ids REMOVED both the EMPTY SET, maximum `R-0681` unchanged, `^Done: R-` 4 to 4 and `^Landed: R-` 0 to 0, and `^Recurrence: R-` 17 to 18 gaining exactly `R-0593` by multiset difference. THE SPLIT SERIES BEHAVED AS DECISION F031 D7 RULES for a second round running: `^Gate: R\d+ — ` 19 to 19, frozen, and `^Gate: F\d+ R\d+ — ` 1 to 2, the added key exactly `F031 R20`, both keys DISTINCT, so the §3 item 26 header collision this series exists to prevent did not occur. The §3 item 10 open set is 238 at `259e4fd9`, and `- R-0593 — ` still occurs exactly ONCE both line-anchored and as a substring, so EVIDENCE0593 joined that finding rather than replacing it and its landed paragraph was not edited. HYGIENE HELD: line-anchored `^<<<SLICE ` and `^<<<END ` are 0 in `.agent/plan.md` at `b2c00ebc` and in `.agent/live_review.md` at `259e4fd9`, against a CONTROL of 3 and 3 over the C0a blob, so the reading is not vacuous; the range `a462932f`..`259e4fd9` names 4 paths, none under `apps/`, `packages/`, `tests/` or `docs/` and none of `.agent/decisions.md`, `.agent/context.md` or either inventory, range-minus-change-set EMPTY and change-set-minus-range exactly `.agent/handoff.md`; the five commits of `a462932f`..`f13b92c0` are each SINGLE-PARENT with insertions 340, 192, 21, 4 and 44 read from `git diff --numstat`, each under the 500 cap AGENTS.md DECISION F104 D1 sets, and the first four agree CELL FOR CELL with the `+/-` column of that handback's `## Commits` table, which is the §3 item 28 reading; `git ls-files .remedy-wt` 0, the zip glob 0, `git worktree list` 1 line and `git status --porcelain` 0; the reflog read by OPERATION PREFIX over that round's entries shows amend 0, rebase 0 and cherry 0. THE BLOCK'S OWN OBJECT IDS RESOLVE: 19 SHA-shaped occurrences, 11 distinct, failing set EMPTY, one `blob` and ten `commit`. THE SUITES ARE THE REVIEWER'S OWN, run SERIALLY, never two alive at once, every one a REAL exit 0: `npm run typecheck` with ZERO diagnostics on stdout and stderr, `npm run test:unit` at 22 files and 332 tests with `decisionCard.test.ts` 27 and `decisionOrder.test.ts` 16, and in Python `tests/ui_server/` 474, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16 and `test_golden_path` 42 — every count identical to the reviewer's base readings, the expected reading for a round whose path set holds no `apps/` file. THE PUSH DISCHARGED, which is the outcome G9 of that round routed here rather than to any file R21 wrote: measured with `git ls-remote`, `refs/heads/feature/f031-decision-inbox` and the local tip are both `f13b92c0a8a978f631a961786b0870b7594e7cbe`, and no pull request was created, no branch deleted and nothing merged. THE HANDBACK'S DECLARED OVERAGE IS ACCEPTED: 81 lines against the 60-line tier its 5 commits fix, the numeral stated as AGENTS.md DECISION D15 requires, no section dropped, and the content behind it — five per-commit tables, the nine-gate list, the item-status table and the authored-text proofs — is mandated rather than verbose. THE THREE DECLARED TOOLING AND ORDERING ITEMS ARE SOUND AND NONE IS A FINDING: routing the two `apps/ui` command lines through `subprocess.run` with a working directory of `apps/ui` changed HOW not WHAT, running the five pytest lines the same way preserved REAL exit codes a pipe would have swallowed, and applying PLANF031R21 byte for byte while it read ahead of C2 is the constraint-1 behaviour the R20 entry already adjudicated as correct. THE VERDICT IS PASS.
<<<END LEDGER22

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
    `.remedy-wt/f031-r22.md` before C0a, the committed C0a blob, the
    committed C0b blob, and `.agent/last_block.md` off disk after C0b — all
    four EQUAL, and the git blob id of C0a's and C0b's file, the SAME id.

G2  Extraction and the block's own two caps. Run your extractor over the
    COMMITTED C0a blob and report the slice count, the CONTENT lines inside
    markers, and the TOTAL line count — the numbers YOUR extractor printed.
    Then report PROSE, computed as TOTAL minus CONTENT, against the two
    caps the Base section names. If either is exceeded, say so plainly and
    continue: an oversize block is the reviewer's defect to record, not
    yours to fix.

G3  The plan. `.agent/plan.md` at C1 is byte-equal to PLANF031R22 under
    your stated newline convention; report slice length, file length and
    convention. NEGATIVE CONTROL: NOT byte-equal to that slice with its
    trailing newline REMOVED. `^## Goal$` 1, `^## Next Steps$` 1, `wc -l`
    STRICTLY under 50.

G4  The C2 append, as ONE equality over the whole file, in the shape
    constraint 8 states — name that paragraph, do not restate its formula.
    Report the boolean and the byte arithmetic against the C1 length you
    measure yourself. Report a SECOND, INDEPENDENT reading: split the
    committed file on blank lines, take the LAST N units, and confirm they
    equal LEDGER22's paragraphs IN ORDER, where N is the number YOUR split
    measured; give the unit count before and after, and STATE YOUR
    TRAILING-NEWLINE HANDLING, because the R21 entry records that a naive
    split reports FALSE on a byte-perfect file. NEGATIVE CONTROL: flip ONE
    byte inside the appended text; BOTH readers must reject the mutant and
    BOTH accept the true file, and the mutant is written only under a
    disposable worktree per constraint 12.

G5  The ledger sets, base versus C2 in `.agent/live_review.md`:
    `^- R-\d+ — ` 242 → 242 all DISTINCT, ids ADDED and REMOVED both the
    EMPTY SET, maximum `R-0681` → `R-0681`; `^Done: R-` 4 → 4,
    `^Landed: R-` 0 → 0 and `^Recurrence: R-` 18 → 18, all UNCHANGED.
    `^Gate: R\d+ — ` 19 → 19 UNCHANGED, and `^Gate: F\d+ R\d+ — ` 2 → 3,
    the ADDED key being exactly `F031 R21`, all keys DISTINCT (§3 item 26).
    Report the §3 item 10 open set at C2 — paragraphs minus `Done:` lines —
    which must be 238. Report that `- R-0593 — ` still occurs exactly ONCE
    and that `^Recurrence: R-0593` still occurs exactly ONCE, since
    constraint 10 forbids editing either paragraph.

G6  The probes, in a disposable worktree per constraint 12, run from the
    PRIMARY checkout's `apps/ui` directory so the primary's `node_modules`
    resolves — a fresh worktree has none, and the reviewer verified this
    exact invocation with a red control before ordering it:
      npx vitest run --config <PRIMARY>/apps/ui/vitest.config.ts \
        --root <WORKTREE>/apps/ui src/api/decisionFilter.test.ts
    Run it UNMUTATED first and report exit 0 and the counts. Then PROBE A,
    making `decisionTypeChoices` return a FIXED list of type choices
    instead of deriving them, which is the architecture line S2(a) states;
    then PROBE B, removing the `DECISION_FILTER_ALL` special case from
    `filterDecisionsByType` so that value is compared against `type` like
    any other, which is S2(b). For EACH report the REAL exit code, HOW MANY
    tests failed and WHICH test names failed — never a predicted number. A
    probe that comes back GREEN is the honest answer to DECLARE, not to
    paper over: it means the property is unpinned, and saying so is worth
    more to this feature than a red would be. Report `git worktree list` as
    1 line after the removals and name the exact paths you removed.

G7  The new module's surface, then the suites. Over
    `apps/ui/src/api/decisionFilter.ts` at C3 report: that it imports
    nothing but a TYPE from `./decisionCard`; its `switch` count, which
    must be 0, beside the `switch` count over
    `apps/ui/src/api/brainStreamDriver.ts`, which the Base section says is
    exactly 1, so a zero here is a measurement and not a blind command; and
    each name S1 lists, grepped in that file. Then in the PRIMARY checkout at C3
    tree, all REAL exit 0, run SERIALLY and never two alive at once, with
    `git worktree list` reported as 1 line immediately BEFORE the first of
    them. At `apps/ui`: `npm run typecheck` with ZERO diagnostics on stdout
    and stderr; `npm run test:unit`, reporting the file and test counts
    YOUR run measured — `decisionCard.test.ts` must still be exactly 27 and
    `decisionOrder.test.ts` exactly 16, any movement in either being a
    finding, while the totals move by your new file, whose count you report
    rather than predict. Then in Python, by these exact command lines with
    no extra flag:
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/ui_contracts/ -q
      python3 -m pytest tests/cli/test_golden_path.py -q
    These are the four state readers a round rewriting `.agent/` state
    gates, plus `tests/ui_contracts/` which this round's `apps/` paths
    earn, plus the canary. The reviewer executed all six at the base
    `f13b92c0` with these exact lines and measured in that order 474, 52,
    21, 16, 525 passed with 4 skipped, and 42, every one exit 0. Account
    for any difference.

G8  Markers, paths, commit shapes and object ids. Line-anchored
    `^<<<SLICE ` and `^<<<END ` both 0 in `.agent/plan.md` at C1,
    `.agent/live_review.md` at C2 and every `apps/` file C3 writes, against
    the same counts over the COMMITTED C0a blob as a CONTROL, where they
    are NOT 0. `git diff --name-only <base>..C3` names NO path under
    `docs/`, `packages/` or `tests/`, and neither `.agent/decisions.md` nor
    `.agent/context.md` nor either inventory file nor
    `apps/ui/src/components/panels/DecisionInboxCard.tsx`; the range path
    set MINUS the change set is EMPTY and the change set MINUS the range is
    exactly `.agent/handoff.md`, which C4 writes. Over C0a..C3 report per
    commit that it is single-parent and its INSERTION count — the `+`
    column only, per AGENTS.md DECISION F104 D1 — each under 500; those
    same numbers fill the `+/-` column of the `## Commits` table, derived
    from `git diff --numstat` and NOT from `git commit`'s own summary, and
    you report that the two agree cell for cell (§3 item 28). Report
    `git ls-files .remedy-wt` as 0 and `git ls-files` over `*.zip` as 0.
    FOR THE REFLOG state SCOPE and FIELD: over THIS ROUND'S entries only,
    by the OPERATION PREFIX before the first colon of
    `git reflog --format=%gs`, report `amend`, `rebase` and `cherry` each 0
    and how many entries you scoped to. Finally extract every SHA-shaped
    token from the COMMITTED C0a blob with the word-bounded pattern
    `[0-9a-f]{7,40}` — whose boundaries do NOT match the 64-char sha256
    digests this block also carries — pass each to `git cat-file -t`, and
    report the token count YOUR extractor measured, the type per token, and
    the FAILING SET, which MUST BE EMPTY. THE TYPES ARE NOT ALL `commit`:
    LEDGER22 quotes the git BLOB id
    `599e6675d9e5aa79fb038ca357f7b20e1498daf2`, resolved to type `blob`
    before emission.

G9  The push. AFTER C4, run `git push origin feature/f031-decision-inbox`.
    No `--force`, no `--force-with-lease`, no history rewrite, no branch
    deletion, no pull request. THAT PUSH'S OUTCOME IS NOT A VALUE OF ANY
    FILE THIS ROUND WRITES: the reviewer measures the pushed tips at the
    next gate and records them in the R22 entry of `.agent/live_review.md`.
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
BEFORE YOU COMMIT IT, or the list is named and NO numeral is given
(R-0441). Any finding count carries the RULE that produced it and the
COMMIT it was measured at, per DECISION F009 D10; a narrower set is named
"the findings this feature must still act on", never "open" unqualified.

THE HANDBACK LINE CAP: this block states no cap and no tier. Resolve it
from AGENTS.md under `### handoff.md` against the commit count constraint
4 fixes, and report BOTH that count and the tier. If the MANDATED content
genuinely does not fit, exceed it and carry a DECISION D15 "Deviations,
declared" line naming your measured count as a NUMERAL (R-0430) and the
mandated content behind it. Never drop a section to fit, and claim no
token cap: that cap was withdrawn.

THIS ROUND ENDS THE SESSION, so your `## Next` section is the next
session's first instruction and names, in order: that it reads
`.agent/STOP` from disk as Phase 1 rule 1 BEFORE the Open PR Gate as rule
2; that the R22 verdict is UNRECORDED and owed by the next round's ledger
commit (DECISION F085 D9); and that R23 wires the filter control into
`DecisionInboxCard`, repairs that file's own `Recurrence: R-0593` note, and
MUST read `docs/ui/design_reference/` before authoring the control, per
`.agent/context.md`.

Declare every deviation, contradiction and assumption.
──────────────────────────────────────────────────────────────

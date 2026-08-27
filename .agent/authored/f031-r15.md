── STEP R15 — F031 Decision inbox ────────────────────────────
Goal:        Record the R14 verdict, register the R-0441 recurrence,
             and PROJECT the wired model into markup per DECISION F031
             D4: a decision-inbox card built from the shipped
             `RightLivePanel.module.css` shell, mounted in
             `RightLivePanel`, reading `dashboard.decisionInbox` and
             branching on nothing of its own.

Fortschritt: ~55 % (F031 claimed; R1 through R14 landed and gated ·
             T001 SHIPPED · T002a MODEL shipped, red-proofed and wired
             · this round renders it · T002b ordering/filtering/badge
             und T003 offen) — Schaetzung

Bundle:      C0a save this block · C0b mirror it into last_block · C1
             the plan · C2 the R14 gate entry and the R-0441
             recurrence · C3 the card, its mount and its styles · C4
             handback.

Change set:  exactly these paths, nothing else —
             .agent/authored/f031-r15.md                        (C0a)
             .agent/last_block.md                               (C0b)
             .agent/plan.md                                     (C1)
             .agent/live_review.md                              (C2)
             apps/ui/src/components/panels/DecisionInboxCard.tsx (C3, NEW)
             apps/ui/src/components/panels/RightLivePanel.tsx    (C3)
             apps/ui/src/components/panels/RightLivePanel.module.css (C3)
             .agent/handoff.md                                  (C4)
             This list bounds the round's WRITES, not its ACTIONS:
             the push named in G11 is ordered explicitly and is not a
             file (R-0674).

── Base ──────────────────────────────────────────────────────
The round base is `e12a4d46989ec1780771b94fee0fbb44c528a8d0`, the R14
handback commit and the tip of `feature/f031-decision-inbox`, local
and remote equal — the reviewer measured both with `git ls-remote`.
Stay on that branch; create none, never commit to `main`. Every
SHA-shaped token here was passed to `git cat-file -t` before emission
and every one RESOLVES; the types are NOT all `commit` and G10 does
not ask them to be.

Readings the reviewer MEASURED at that base, re-checkable there:
- `.agent/live_review.md`: 604055 bytes, 1211 lines, 292 blank-line
  units; `^- R-\d+ — ` 241 all DISTINCT, maximum `R-0680`;
  `^Done: R-\d+ — ` 3, so the §3 item 10 open set — the first
  pattern's paragraphs minus the second's lines — is 238;
  `^Recurrence: R-` 15; `^Gate: R\d+ — ` 14, the keys `R19` and `R1`
  through `R14` minus `R14` itself, which this round adds.
- `.agent/plan.md` 49 lines, 2925 bytes. `.agent/handoff.md` 97
  lines. `.agent/decisions.md` UNTOUCHED this round.
- `apps/ui`: `npm run test:unit` exit 0 at 21 files and 316 tests;
  `npm run typecheck` exit 0 with zero diagnostics.
- `apps/ui/src/styles/` defines 58 `--remedy-*` custom properties, and
  the set of `--remedy-*` properties `RightLivePanel.module.css` USES
  but that directory does not DEFINE is EMPTY. Finding R-0661 is that
  set being non-empty in another stylesheet; keeping it empty here is
  what G8 gates.
- `RightLivePanel.module.css` already carries `.card`, `.cardHeader`,
  `.attentionTitle` and `.emptyState` among others — read it first.

── Why this round exists ─────────────────────────────────────
R14 wired the decision-card model into the dashboard payload and its
verdict is owed by THIS round's ledger commit, which by DECISION F085
D9 no artefact of R14 could carry. `dashboard.decisionInbox` now
arrives on every dashboard and NOTHING RENDERS IT, so this round
closes that gap in the direction DECISION F031 D4 already fixed.

C2 ALSO REGISTERS A RECURRENCE, NOT A NEW ID. The R14 handback wrote
"the findings THIS FEATURE MUST STILL ACT ON are the eighteen named in
`.agent/plan.md` at 597c20ce" while that bullet names NINETEEN. Before
considering an id the reviewer searched the open set for the DEFECT as
§3 item 30 requires, and R-0441 — a numeral contradicting the
enumeration it claims to be counted from — already holds this family
and is OPEN, so LEDGER15 adds a `Recurrence:` line instead.

WHAT THIS ROUND CANNOT PROVE, STATED UP FRONT RATHER THAN DISCOVERED.
DECISION F031 D5 rules that the shipped vitest config collects
`src/**/*.test.ts` in a `node` environment and reaches no markup, so NO
TEST REACHES THE COMPONENT THIS ROUND SHIPS, and `typecheck` is the only
static reader that works here (finding R-0622). G9 therefore orders a
PROBE rather than a colour: removing the mount is expected to turn
NOTHING red, and putting that on the record is how the round's evidence
limit gets stated instead of a green gate implying coverage.

── Constraints ───────────────────────────────────────────────
1. Apply every authored slice BYTE FOR BYTE. Never retype, rewrap or
   "fix" one. If a slice looks wrong, apply it verbatim and DECLARE
   the disagreement in the handback: a contradiction inside this block
   is the reviewer's defect, not yours.
2. Slice transport. This block is saved verbatim as
   `.agent/authored/f031-r15.md` at C0a and mirrored byte-identically
   into `.agent/last_block.md` at C0b. Extract every slice
   PROGRAMMATICALLY out of the COMMITTED C0a blob by its marker LINES
   — `<<<SLICE <NAME>` opens, `<<<END <NAME>` closes. Marker lines
   never reach a target file.
3. Commit sequence, exactly: C0a, C0b, C1, C2, C3, C4. No extra
   commit, none dropped, no reordering. C1 is the FIRST substantive
   commit because this round writes to the finding ledger (§3 item
   23). C3 is the ONLY commit touching `apps/`. To correct a landed
   commit, do NOT add one outside this sequence — declare it, and give
   any such commit its own `## Commits` row and its own item-status
   row (R-0675).
4. Never amend, rebase, cherry-pick, force-push or rewrite history;
   never delete a branch; never merge; create no pull request.
5. `git status --porcelain` prints 0 lines after every commit. Read
   `.agent/STOP` from disk before C0a and again before C4; if present,
   finish the commit in hand, write the handback and stop. NEVER
   delete that sentinel (R-0347).
6. The slices this block carries are the whole text PLANF031R15 and
   the appended text LEDGER15. This paragraph names them and states no
   count; G3 orders you to report the count YOUR extractor measured.
   THE PRODUCTION CODE IS NOT A SLICE: section 5 is a numbered SPEC
   and you author the TypeScript and CSS that meet it.
7. THE ONE APPEND'S SHAPE IS STATED ONCE, HERE, WITH EVERY GATE NAMING
   THIS PARAGRAPH RATHER THAN RESTATING IT. Under the newline-INCLUDED
   convention the slice already ends in a newline, so the target is
   EXACTLY: its base blob, then one newline, then the slice. LEDGER15
   goes to `.agent/live_review.md` at C2, which receives NOTHING ELSE
   in that commit (R-0657). Nothing follows it, and the file ends in
   exactly one newline because the slice carries it. THIS BLOCK
   CARRIES NO FROM/TO PAIR, so no containment reading is owed.
8. THIS ROUND MINTS NO FINDING ID AND WRITES NO `Done:` LINE. It
   writes exactly ONE `Recurrence:` line, for `R-0441`, inside
   LEDGER15. `^- R-\d+ — ` must be 241 before and 241 after with the
   maximum `R-0680` unchanged; `^Done: R-` 3 before and 3 after;
   `^Recurrence: R-` 15 before and 16 after. A recurrence resolves
   nothing, so the §3 item 10 open set stays 238.
9. Touch nothing under `packages/`, `tests/` or `docs/`, and nothing
   under `apps/` except the files section 5 names. Do not touch
   `.agent/decisions.md`, `.agent/context.md`,
   `.agent/f031_inventory.md` or `.agent/f031_ui_inventory.md` —
   landed evidence is corrected by dating in a later round, never by
   editing (§3 item 20).
10. `docs/roadmap/ROADMAP.md` and `docs/roadmap/STATUS.md` are NOT
    touched: AGENTS.md forbids the first absent an explicit operator
    request, and this round claims and closes nothing. Because no
    `docs/roadmap/**` path is in the change set, the §3 docs-round
    gate is not earned and is not ordered.
11. Destructive verification runs ONLY in a disposable `git worktree`
    under `.remedy-wt/`, removed BY ITS EXACT PATH (R-0662) and before
    the G10 suites. Everything already under `.remedy-wt/` is
    pre-existing scratch belonging to no commit, this block's own file
    included: create no worktree at an existing path there, and delete
    nothing you did not create.
12. NO EXISTING BEHAVIOUR CHANGES. No existing component, prop, CSS
    class or test is renamed, reordered, weakened or removed, and
    `NeedsAttentionCard` stays exactly as it is — DECISION F031 D4
    keeps it DISTINCT from the inbox and leaves its retirement to
    T003. Every edit section 5 orders is ADDITIVE. `npm run lint` is
    NOT ordered and is not run: finding R-0622 records that eslint
    parses no TypeScript here. No test is added either, because
    DECISION F031 D5 rules the markup out of the tested layer.

── 5. The production code, as a SPEC ─────────────────────────
Author the TypeScript and CSS yourself. Follow the surrounding idiom:
the one-line WHY comment sits directly above a definition, and a
deliberate absence is written down where a reader would search for it
(AGENTS.md, Code Discoverability Conventions). Read each file you edit
in full before editing it.

S1 NEW `apps/ui/src/components/panels/DecisionInboxCard.tsx`. One
   exported component, `DecisionInboxCard`, taking the models to
   render as its only prop, typed with an `import type` of
   `DecisionCardModel` from `../../api/decisionCard` — a TYPE import,
   because this component borrows no logic from that module.
   THE ARCHITECTURE LINE, and the property G8 measures: it branches on
   NOTHING about a decision. No `switch`, and no comparison whatsoever
   against a decision's `type` or `status` — those are DATA here and
   never control flow, which is what lets a decision type nobody has
   produced yet render on the day some producer first emits it. Every
   string it displays is read from a model FIELD; none is chosen by a
   conditional. Write that refusal down as a deliberate absence in the
   file's header comment.
   Its ONE guard is emptiness: with no models it returns `null`,
   exactly as `NeedsAttentionCard` does with no item. Otherwise it
   renders a `section` using the shipped `.card` class with a
   `.cardHeader` holding an `h2` reading `Decision inbox`, then one
   row per model carrying, from the model and only the model: the
   `title`, then the `ageLabel`, `blockedLabel` and `type` as chips,
   then one `button` per entry of `answers` labelled `answer.label`.
   Those buttons are `type="button"` and DISABLED, with a `title`
   saying answering arrives with T003 — this round wires no write
   path, and a live-looking control that does nothing is exactly the
   false live indicator §4.5 makes a block condition.
   Give each row a stable React key that cannot collide when two cards
   carry the same id, and use no comparison operator to build it.

S2 `apps/ui/src/components/panels/RightLivePanel.tsx`. Import the new
   component and mount it, passing `dashboard.decisionInbox`. Place it
   directly AFTER `NeedsAttentionCard` and BEFORE `ActivityFeedCard`,
   so the two attention surfaces sit together. Nothing else in this
   file changes: no prop is added to `RightLivePanel` itself, because
   the data already arrives inside `dashboard`.

S3 `apps/ui/src/components/panels/RightLivePanel.module.css`. APPEND
   the classes S1 needs — the rows, the chip strip and the answer
   buttons — reusing the existing card shell rather than restyling it.
   EVERY colour, radius, font and shadow comes from a `--remedy-*`
   custom property that `apps/ui/src/styles/` ALREADY DEFINES; add no
   new token and hard-code no hex value, which is what keeps the set
   G8 measures empty. Follow the file's existing formatting.

── Authored slices ───────────────────────────────────────────

<<<SLICE PLANF031R15
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the merge
commit of pull request #213 which closed F022. `.agent/live_review.md` is the
record and the finding-id ceiling; the two `f031_*_inventory.md` files are the
inventories; `.agent/decisions.md` carries DECISION F031 D1 through D5.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R15 records the R14 verdict, registers the R-0441 recurrence, and renders what
R14 wired: `DecisionInboxCard` projects `dashboard.decisionInbox` into markup
built from the shipped `RightLivePanel.module.css` shell and mounted in
`RightLivePanel`, branching on nothing of its own.

## Next Steps
1. T002b adds ordering over age and blocked size, filtering, and the badge,
   where DECISION F031 D2 binds: the badge re-derives on refetch over the
   existing SSE stream, no new event kind ships, and D2's two constant-zero
   counters get replaced. The ordering rule is documented on the sort control.
2. T003 wires answering through the write channel — the card's answer buttons
   ship DISABLED until it lands — and rules there whether
   `NeedsAttentionCard`'s decision branch is retired, which D4 leaves open.
3. The DOM harness that would test the markup is its own feature per DECISION
   F031 D5, and nothing in F031 waits on it.

## Risks
- THE SEED-KEY COLLISION, carried forward and never to be dropped while it
  stands: `.agent/live_review.md` holds `Gate: R19` as a seed entry inherited
  from F022, so if F031 reaches its own R19 that key collides — the §3 item 26
  defect. A round before then renames the seed or the scheme. F031 is at R15,
  so five rounds remain.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 238 at `e12a4d46`, and a recurrence resolves nothing, so C2 leaves it
  at 238.
- The findings THIS FEATURE MUST STILL ACT ON are R-0403, R-0413, R-0431,
  R-0441, R-0445, R-0471, R-0495, R-0533, R-0574, R-0601, R-0622, R-0625,
  R-0632, R-0672, R-0674, R-0675, R-0676, R-0677, R-0678 and R-0679; R-0495 and
  R-0574 are the two Highs. This bullet states no count of that list.
- R-0622 is live ground: eslint parses no TypeScript here and `npm run lint`
  exits 1 at 80 problems, so `typecheck` is the only static reader that works.
- THE MARKUP THIS ROUND SHIPS IS REACHED BY NO TEST, which DECISION F031 D5
  rules its own feature. Every branch therefore stays in `decisionCard.ts`; one
  migrating into the `.tsx` leaves the tested region silently.
<<<END PLANF031R15

<<<SLICE LEDGER15
Gate: R14 — the F031 R14 entry. R14 PASSED ON EVERY ONE OF ITS ELEVEN GATES, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk rather than reading the handback back; every value that handback states reproduced exactly. TRANSPORT HELD IN ITS STRONGEST FORM, cmp-against-scratchpad rather than the digest fallback: the reviewer's own emitted `.remedy-wt/f031-r14.md`, the committed C0a blob, the committed C0b blob and `.agent/last_block.md` off disk are ALL FOUR byte-identical at sha256 `1a6e1b0f6058637e59e8cc84122a414d46729a97f551b4bbcea0e205665b9827` over 32941 bytes and 444 lines, C0a and C0b resolving to the SAME git blob `cb5e9ea8188e9ec89b9419238a53bfa4813e0ebe`. THE EXTRACTION printed 2 slices, 52 content lines inside markers and 444 total. THE SLICES APPLIED BYTE FOR BYTE: `.agent/plan.md` at `597c20ce` equals PLANF031R14 exactly at 2925 bytes and 49 lines with the trailing-newline-removed control FALSE, `^## Goal$` 1, `^## Next Steps$` 1; and the ledger append equals its base blob plus one newline plus LEDGER14 EXACTLY, 597681 + 1 + 6373 = 604055 against an actual 604055, corroborated by an independent blank-line split going 290 to 292 units whose last 2 units equal the slice's 2 paragraphs IN ORDER. THE SETS MOVED ONLY WHERE CONSTRAINT 8 ALLOWED: `^- R-\d+ — ` 241 to 241 all DISTINCT, ids ADDED and ids REMOVED both the EMPTY SET, maximum `R-0680` unchanged, `^Done: R-` 2 to 3 gaining EXACTLY `R-0680`, `^Recurrence: R-` 15 to 15, and `^Gate: R\d+ — ` 13 to 14 gaining EXACTLY the key `R13`, all 14 DISTINCT. THIS IS THE FEATURE'S SECOND PRODUCTION-CODE ROUND UNDER THE SPEC FORM, SO THE REVIEWER READ THE SHIPPED CODE rather than resting on the gates. Every clause of S1 through S4 is met and nothing beyond them moved: `RemedyDashboard` gains `decisionInbox` as a NON-OPTIONAL `DecisionCardModel[]`, imported `import type` from `./decisionCard`, which imports nothing back, so the direction stays acyclic; `normalizeDashboardPayload` gains an optional FOURTH parameter and sets the field from `decisionCardModels(decisionsDocument ?? {})`; `normalizeApiFailure` sets it to the empty array; and `loadRemedyDashboard` reads `/api/jobs/<job_id>/decisions` in a `try`/`catch` that MIRRORS the `brain-view-model` read line for line, pushing `decisions` onto `failedEndpoints` and degrading identically. THE ENDPOINT IS REAL, not assumed: `packages/orchestration/ui_server.py` maps the key `decisions` to `_build_decisions_json`, which returns `build_decision_inbox`'s document. THE GAP R13's ENTRY RECORDED IS CLOSED — `decisionCard.ts` had no production caller at `d63a146f` and has one at `475f0f36`. THE RED PROOF IS THE REVIEWER'S OWN, RE-RUN INDEPENDENTLY in a disposable worktree it then removed by exact path, by the route finding R-0653's resolution records: an unmutated control at the worktree root exits 0 at 56 passed, and with `decisionInbox` mutated to the empty array for every input the SAME command exits 1 with EXACTLY ONE failing test, `decisionInbox projection > projects every card of the document, in the endpoint's order`. The tests therefore reach the projection rather than asserting near it. THE TOOLCHAIN AND SUITE READINGS ARE THE REVIEWER'S OWN, taken in the primary checkout: `npm run typecheck` exit 0 with ZERO diagnostics, so the non-optional field named no third construction site; `npm run test:unit` exit 0 at 21 files UNCHANGED and 316 tests against the base's 312, a difference of exactly the four cases S4 orders, with 0 deleted lines in `remedyApi.test.ts`; and the five Python suites run SERIALLY, never two alive at once, every one a REAL exit 0 at `tests/ui_server/` 474, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16 and `test_golden_path` 42, identical to the base readings. HYGIENE HELD: markers line-anchored 0 in all five targets, the range `e12a4d46`..`475f0f36` names no path under `packages/`, `tests/` or `docs/`, no `apps/` path beyond the three the block names, and neither `.agent/decisions.md` nor `.agent/context.md` nor either inventory; `git ls-files .remedy-wt` 0, the zip glob 0, `git worktree list` 1 line, `git status --porcelain` 0, and the reflog read by OPERATION PREFIX shows amend 0, rebase 0 and cherry 0. THE RANGE HELD: `d63a146f`..`e12a4d46` is SIX commits, every one single-parent, with per-commit insertions of 444, 266, 18, 4 and 83 for C0a through C3, each under the 500 cap and each equal cell for cell to the `## Commits` table the handback carries. THE BLOCK'S OWN OBJECT IDS RESOLVE: 22 SHA-shaped tokens, 9 distinct, failing set EMPTY, one of type `blob` and eight of type `commit`, exactly as the block predicted. THE NUMBERS §3 ITEM 31 RULES NO ARTEFACT OF R14 COULD CARRY: the handback commit `e12a4d46` is 61 insertions and 82 deletions and single-parent, the file it writes is 97 lines against the ≤100 tier its six commits earn, and THE PUSH DISCHARGED — measured with `git ls-remote`, the local tip and `refs/heads/feature/f031-decision-inbox` are both `e12a4d46989ec1780771b94fee0fbb44c528a8d0`, `gh pr list --state open` is EMPTY, and nothing was created or merged. THE ONE DECLARED ASSUMPTION IS SOUND: section 5 left the fourth parameter's TYPE unstated and the worker used `any`, matching `dashboard: any` and `brainDetail?: any` in the same signature inside that file's existing `no-explicit-any` disable region, which is the narrowest reading available and changes nothing. R14 EARNS ONE FINDING, and it is a RECURRENCE rather than a new id — registered immediately below against R-0441. THE VERDICT IS PASS.

Recurrence: R-0441 — A NUMERAL THAT CONTRADICTS THE ENUMERATION IT CLAIMS TO HAVE BEEN COUNTED FROM. SECOND INSTANCE, at F031 R14, and it is the WORKER'S, in the handback rather than in a block. NO NEW ID IS MINTED: R-0441 already holds this family, and the open set was searched for the DEFECT before any id was considered (§3 item 30) — the search that F086 R28 failed and that R-0602 repeated one feature later. THE INSTANCE, measured by the reviewer at `e12a4d46`: `.agent/handoff.md` reads "the findings THIS FEATURE MUST STILL ACT ON are the eighteen named in `.agent/plan.md` at 597c20ce", and that bullet of `.agent/plan.md` at `597c20ce` names NINETEEN ids — R-0403, R-0413, R-0431, R-0445, R-0471, R-0495, R-0533, R-0574, R-0601, R-0622, R-0625, R-0632, R-0672, R-0674, R-0675, R-0676, R-0677, R-0678 and R-0679 — before its closing clause naming the two Highs and the resolved R-0680. Low, as R-0441 is: no gate consumed the numeral, the LIST is correct, and the handback is rewritten every round so the wrong word does not persist the way an append-only entry would. It is registered because of WHERE it landed. R-0441's standing rule says a numeral is produced by counting the emitted bytes mechanically in the same pre-emission pass that measures the block's line count, and every instance so far has been a REVIEWER writing a block; this one is a WORKER writing the handback, which no pre-emission pass covers because the handback is written after the block is gone. THE RULE IS THEREFORE WIDENED HERE, binding both roles: any sentence in a BLOCK or a HANDBACK that states a count of a list it names resolves that count by counting the list mechanically before the text is committed, or states the list and NO numeral — which is what the plan bullet itself correctly does, and why the plan was right while the report describing it was wrong. The reviewer's own counter-measure from this round forward is to re-derive every numeral a handback states about a file this workflow writes, at the commit the handback names, as part of the gate rather than as a courtesy.
<<<END LEDGER15

── Done when ─────────────────────────────────────────────────
Run every gate yourself, record its REAL exit code and REAL output,
and report ONE LINE PER GATE in the handback, transcripts kept out of
it (R-0582). "Green" as a word is a finding. Every gate below runs at
a commit STRICTLY EARLIER than C4 (§3 item 31); G11 runs after it and
names its own carrier.

G1  Branch and cleanliness. `git branch --show-current` prints
    `feature/f031-decision-inbox` and NOT `main`. `.agent/STOP` read
    from disk is ABSENT before C0a and again before C4. Report
    `git status --porcelain` line count after each of C0a, C0b, C1, C2
    and C3; each must be 0.

G2  Transport. Report sha256, byte count and line count for FOUR
    readings: `.remedy-wt/f031-r15.md` before C0a, the committed C0a
    blob, the committed C0b blob, and `.agent/last_block.md` off disk
    after C0b. All four must be EQUAL. Report the git blob id of C0a's
    and C0b's file; they must be the SAME id.

G3  Extraction. Run your extractor over the COMMITTED C0a blob and
    report the slice count, the CONTENT lines inside markers, and the
    TOTAL line count. Report the numbers YOUR extractor printed.

G4  The plan. `.agent/plan.md` at C1 is byte-equal to PLANF031R15
    under your stated newline convention; report slice length, file
    length and convention. NEGATIVE CONTROL: NOT byte-equal to that
    slice with its trailing newline REMOVED. `^## Goal$` 1,
    `^## Next Steps$` 1, `wc -l` STRICTLY under 50.

G5  The append, as ONE equality over the whole file, in the shape
    constraint 7 states — name that paragraph, do not restate its
    formula. Report the boolean and the byte arithmetic against the
    base's 604055. Report a SECOND, INDEPENDENT reading: split the
    committed file on blank lines, take the LAST N units, and confirm
    they equal LEDGER15's N paragraphs IN ORDER, where N is the number
    YOUR split measured and not one stated here (R-0631). Give the
    unit count before and after. NEGATIVE CONTROL: flip ONE byte
    inside the FIRST paragraph the append added; BOTH readers must
    reject the mutant and BOTH accept the true file. Write any mutant
    only under a disposable worktree per constraint 11.

G6  The sets, base versus C2 in `.agent/live_review.md`:
    `^- R-\d+ — ` 241 → 241, all DISTINCT, the ids ADDED and the ids
    REMOVED both the EMPTY SET, maximum `R-0680` UNCHANGED.
    `^Done: R-` 3 → 3, UNCHANGED. `^Recurrence: R-` 15 → 16, the ids
    ADDED being exactly `R-0441`. `^Gate: R\d+ — ` 14 → 15, gaining
    exactly the key `R14`, with `R19` and `R1` through `R13` still
    present, and all 15 keys DISTINCT (§3 item 26). Report the §3 item
    10 open set at C2 — paragraphs minus `Done:` lines — which must
    still be 238.

G7  Markers, paths, structure and hygiene. Line-anchored `^<<<SLICE `
    and `^<<<END ` both count 0 in `.agent/plan.md` at C1,
    `.agent/live_review.md` at C2, and each of the `apps/` files
    section 5 names, at C3. Report that `git diff --name-only
    <base>..C3` names NO path under `packages/`, `tests/` or `docs/`,
    no path under `apps/` other than those section 5 names, and
    neither `.agent/decisions.md` nor `.agent/context.md` nor either
    inventory file. Over C0a..C3 report per commit that it is
    single-parent and its INSERTION count — the `+` column only, per
    AGENTS.md DECISION F104 D1 — each under 500. Those same numbers
    fill the `+/-` column of the `## Commits` table the handback
    template mandates: derive that column from `git diff --numstat`
    and NOT from the files' before/after line counts, and report that
    the table and this gate agree cell for cell (§3 item 28). Report
    the range path set MINUS the change set (EMPTY) and the change set
    MINUS the range (exactly `.agent/handoff.md`, which C4 writes).
    Report `git ls-files .remedy-wt` as 0 and `git ls-files` over
    `*.zip` as 0. FOR THE REFLOG, state the SCOPE and the FIELD in the
    reading itself: over THIS ROUND'S entries only, read by the
    OPERATION PREFIX before the first colon of
    `git reflog --format=%gs`, report `amend`, `rebase` and `cherry`
    each 0, and how many entries you scoped to.

G8  THE CODE COMPILES, THE SUITE IS UNMOVED, AND THE ARCHITECTURE LINE
    HOLDS. In `apps/ui` at C3 report `npm run typecheck` with its REAL
    exit code, which must be 0 with ZERO diagnostics. Report
    `npm run test:unit` with its REAL exit code, file count and test
    count: both must be UNCHANGED at the base's 21 and 316, because
    constraint 12 adds no test and the markup is outside the collected
    set — any movement is a finding. THEN, over the NEW
    `DecisionInboxCard.tsx` at C3 and reporting the number YOU
    measured for each: `switch` must be 0; the number of comparison
    operators applied to a decision's `type` or `status` — search for
    `type` or `status` followed by `===`, `!==`, `==` or `!=` — must
    be 0; and the import of `decisionCard` must be an `import type`,
    which you report by quoting the import line. FINALLY the token
    gate: compute the set of `--remedy-*` custom properties that
    `RightLivePanel.module.css` at C3 USES via `var(...)` minus those
    `apps/ui/src/styles/` DEFINES, and report it — it must be EMPTY,
    as it is at the base, and report the count of `#` hex literals
    among the lines C3 ADDS to that file, which must be 0 (finding
    R-0661).

G9  THE MOUNT, AND THE HONEST LIMIT OF THIS ROUND'S EVIDENCE. First
    report that the component is really mounted: at C3,
    `RightLivePanel.tsx` names `DecisionInboxCard` and passes
    `dashboard.decisionInbox` to it, and the new file exists at the
    path section 5 gives — quote the mounting line. THEN, in a
    disposable worktree per constraint 11, DELETE that mounting line
    and run `npm run typecheck` and `npm run test:unit` by the route
    finding R-0653's resolution records for a worktree run. THIS IS A
    PROBE, NOT A COLOUR: report what actually happened, and if NOTHING
    goes red, say so plainly — that is the expected reading and it is
    the point of the gate, because DECISION F031 D5 puts the markup
    outside the collected set and this records exactly how far the
    round's evidence reaches. Do not report a colour you did not see.
    Remove the worktree BY ITS EXACT PATH afterwards and report
    `git worktree list` as 1 line and `git status --porcelain` as 0 in
    the primary checkout.

G10 The block's own object ids, and the Python suites. Extract every
    SHA-shaped token from the COMMITTED C0a blob with the word-bounded
    pattern `[0-9a-f]{7,40}` — whose boundaries do NOT match the
    64-char sha256 digests this block also carries — and pass each to
    `git cat-file -t`. FAILING means the token does NOT RESOLVE, and
    THE FAILING SET MUST BE EMPTY: this block quotes no non-existent
    id, so it has no positive control. THE TYPES ARE NOT ALL `commit`
    AND THE GATE DOES NOT ASK THEM TO BE — LEDGER15 quotes the git
    BLOB id `cb5e9ea8188e9ec89b9419238a53bfa4813e0ebe`, which the
    reviewer resolved to type `blob` before emission, and every other
    token resolves to type `commit`. Report the token count YOUR
    extractor measured, the failing set, and the type per token. Then,
    with `git worktree list` reported as 1 line immediately BEFORE the
    first pytest command, run these SERIALLY in the PRIMARY checkout
    at the C3 tree, never two at once, all exit 0:
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/cli/test_golden_path.py -q
    These are the four state readers a round rewriting `.agent/` state
    gates, plus the canary. The reviewer executed all five at the base
    `e12a4d46` with these exact command lines and no extra flag, and
    measured in that order 474, 52, 21, 16 and 42, every one exit 0.
    Account for any difference.

G11 The push. AFTER C4, run
    `git push origin feature/f031-decision-inbox`. No `--force`, no
    `--force-with-lease`, no history rewrite, no branch deletion, no
    pull request. THIS GATE'S OUTCOME IS NOT A VALUE OF ANY FILE THIS
    ROUND WRITES, and its carrier is named here so you inherit ONE
    instruction rather than two: the reviewer measures the pushed tips
    at the next gate and records them in the R15 entry of
    `.agent/live_review.md`. In `## External actions` write the push
    COMMAND and that sentence. In the item-status table the push row's
    status is `done` with the reason "ordered after C4; outcome
    carried by G11 to the reviewer" — it is NOT `deviated`, because
    the step is performed exactly as ordered and only its OUTCOME
    lands elsewhere. Report the real outcome in your final message.

── Handback ──────────────────────────────────────────────────
Rewrite `.agent/handoff.md` at C4 per docs/agents/handback_template.md:
feature and round, branch, base and commit SHAs, a changed-files table
per commit, the item-status table covering C0a, C0b, C1, C2, C3, C4
and the push, ONE LINE PER GATE with its real result, the finding
counts, and the next expected action. Carry the `Fortschritt:` block
above VERBATIM — count its lines yourself; no numeral is stated here.

EVERY NUMERAL YOUR HANDBACK STATES ABOUT A LIST IS COUNTED
MECHANICALLY BEFORE YOU COMMIT IT, or the list is named and NO numeral
is given. This is the widened R-0441 rule LEDGER15 registers, and it
binds this handback: the instance it records is a handback sentence
that counted a plan bullet by eye and got it wrong.

THE HANDBACK LINE CAP: this block states no cap and no tier. Resolve
it from AGENTS.md under `### handoff.md` against the commit count
constraint 3 fixes, and report BOTH that count and the tier. If the
MANDATED content genuinely does not fit, exceed it and carry a
DECISION D15 "Deviations, declared" line naming your measured count as
a NUMERAL (R-0430) and the mandated content behind it. Never drop a
section to fit, and claim no token cap: that cap was withdrawn.

Any finding count you state carries the RULE that produced it and the
COMMIT it was measured at, in the same sentence, per DECISION F009
D10. A narrower set is named "the findings this feature must still act
on" and is never called "open" unqualified.

THIS IS THE LAST ROUND OF ITS SESSION, so your `## Next` section is
the next session's first instruction and names, in order: Phase 1 rule
1 (re-read `.agent/STOP` from disk), THEN Phase 1 rule 2 (the Open PR
Gate — report what `gh pr list --state open` printed and whether any
pull request exists for this branch); that the R15 verdict is
UNRECORDED and is owed by the next round's ledger commit, which by
DECISION F085 D9 no artefact of this round can carry; and that the
next build step is T002b — ordering over age and blocked size,
filtering, and the badge — under DECISION F031 D2.

Declare every deviation, contradiction and assumption.
──────────────────────────────────────────────────────────────

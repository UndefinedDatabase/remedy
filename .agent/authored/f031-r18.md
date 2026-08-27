── STEP R18 — F031 Decision inbox ────────────────────────────
Goal:        Record the R17 verdict, and RULE the ordering formula
             T002b needs before any code is written for it —
             DECISION F031 D6, into `.agent/decisions.md` and into
             the feature file's amendment series. This round ships NO
             code: §4.7 of docs/agents/planner_reviewer_prompt.md
             puts a spec amendment into the record BEFORE the round
             that builds under it.

Fortschritt: ~58 % (F031 claimed; R1 through R17 landed and gated ·
             T001 SHIPPED · T002a MODEL shipped, wired and RENDERED ·
             R-0681 repaired at R17, resolution owed · T002b
             ordering/filtering/badge und T003 offen) — Schaetzung

Bundle:      C0a save this block · C0b mirror it into last_block · C1
             the plan · C2 the R17 gate entry · C3 DECISION F031 D6 ·
             C4 the feature-file amendment · C5 handback.

Change set:  exactly these paths, nothing else —
             .agent/authored/f031-r18.md                       (C0a)
             .agent/last_block.md                              (C0b)
             .agent/plan.md                                    (C1)
             .agent/live_review.md                             (C2)
             .agent/decisions.md                               (C3)
             docs/roadmap/features/T5_F031.md                  (C4)
             .agent/handoff.md                                 (C5)
             This list bounds the round's WRITES, not its ACTIONS:
             the push named in G12 is ordered explicitly and is not a
             file (R-0674).

── Base ──────────────────────────────────────────────────────
The round base is `48124293e77c4fc2d9de558b0ab0f1d76fd421b0`, the R17
handback commit and the tip of `feature/f031-decision-inbox`, local
and remote equal — the reviewer measured both with `git ls-remote`.
Stay on that branch; create none, never commit to `main`. Every
SHA-shaped token here was passed to `git cat-file -t` before emission
and every one RESOLVES; the types are NOT all `commit` and G11 does
not ask them to be.

Readings the reviewer MEASURED at that base, re-checkable there:
- `.agent/live_review.md`: 624137 bytes; `^- R-\d+ — ` 242 all
  DISTINCT, maximum `R-0681`; `^Done: R-\d+ — ` 3, so the §3 item 10
  open set — the first pattern's paragraphs minus the second's lines
  — is 239; `^Recurrence: R-` 16; `^Landed: R-` 1, that one line
  being R-0681's; `^Gate: R\d+ — ` 17, the keys `R19` and `R1`
  through `R16`, `R17` being what this round adds.
- `.agent/plan.md` 49 lines, 2892 bytes. `.agent/handoff.md` 95
  lines. `.agent/decisions.md` 566658 bytes, 7534 lines, ending in
  exactly one newline after the D5 REVERSE IT paragraph;
  `^## DECISION F031 D\d+` 5, the numbers D1 through D5.
- `docs/roadmap/features/T5_F031.md` 150 lines, ending in exactly one
  newline; `^## Design amendments ` 2, naming R5 and R11.
- The reviewer RAN both docs gates at this base with the exact
  command lines G10 orders: `tests/docs/` exit 0 at 295 passed, and
  `tests/orchestration/test_roadmap_index.py` exit 0 at 30 passed.
- `apps/ui`: `npm run test:unit` exit 0 at 21 files and 316 tests;
  `npm run typecheck` exit 0 with zero diagnostics.
- THE ORDERING GROUND, measured at that base. `DecisionCardModel`
  (`apps/ui/src/api/decisionCard.ts` line 39) carries a NUMERIC
  `blockedCount` but only a FORMATTED `ageLabel`, so D6's rule needs
  a numeric age the model does not yet carry. `decisionCardModels`
  (line 189) preserves the endpoint's order, which
  `decisionCard.test.ts` line 202 and `remedyApi.test.ts` line 544
  both PIN by name; both stay TRUE under D6, which rules a SEPARATE
  comparator rather than a sort inside either. `DecisionInboxEntry`
  carries no job field, so no job filter is buildable here.

── Why this round exists ─────────────────────────────────────
R17's verdict is owed by THIS round's ledger commit, which by
DECISION F085 D9 no artefact of R17 could carry. R17 PASSED: the
reviewer re-ran all twelve of its gates itself and every value it
states reproduced exactly. The full reading is the LEDGER18 slice.

R-0681 IS NOT RESOLVED HERE, DELIBERATELY. R17 marked the landed
rename `Landed:`, which §4.4 reserves for a fix whose review has not
yet happened, and the reviewer has now gated it — so the authored
`Done:` text is owed. It is deferred to R19 because this block is
budgeted at 490 lines TOTAL by DECISION F085 D6 and carrying the
resolution as well would exceed that, and §4.4 says in terms that a
surviving `Landed:` line is what an unreviewed-looking fix should
look like on disk. LEDGER18 carries the full measurement of that fix
regardless, so the RECORD is complete this round and only the marker
lags. R19 replaces the line.

THE ORDERING RULE IS RULED BEFORE IT IS BUILT. The feature file
writes T002b's whole subject as a literal product — "age × blocked
size" — under which every decision blocking nothing scores 0 whatever
its age, so those cards tie and their order is the endpoint's
accident; DECISION F031 D3 makes that the common case, not an edge.
§4.7 routes a wrong spec to planning with the amendment authored INTO
the block, recorded as an operator-visible DECISION and proceeded
under, never as a question. D6 is that amendment, ruled a round ahead
of the code so R19's gates measure a comparator against a rule
already on disk when they run.

── Constraints ───────────────────────────────────────────────
1. Apply every authored slice BYTE FOR BYTE. Never retype, rewrap or
   "fix" one. If a slice looks wrong, apply it verbatim and DECLARE
   the disagreement in the handback: a contradiction inside this block
   is the reviewer's defect, not yours.
2. Slice transport. This block is saved verbatim as
   `.agent/authored/f031-r18.md` at C0a and mirrored byte-identically
   into `.agent/last_block.md` at C0b. Extract every slice
   PROGRAMMATICALLY out of the COMMITTED C0a blob by its marker LINES
   — `<<<SLICE <NAME>` opens, `<<<END <NAME>` closes. Marker lines
   never reach a target file.
3. Commit sequence, exactly: C0a, C0b, C1, C2, C3, C4, C5. No extra
   commit, none dropped, no reordering. C1 is the FIRST substantive
   commit because this round writes the finding ledger (§3 item 23).
   To correct a landed commit, do NOT add one outside this sequence —
   declare it, and give any such commit its own `## Commits` row and
   its own item-status row (R-0675).
4. Never amend, rebase, cherry-pick, force-push or rewrite history;
   never delete a branch; never merge; create no pull request.
5. `git status --porcelain` prints 0 lines after every commit. Read
   `.agent/STOP` from disk before C0a and again before C5; if present,
   finish the commit in hand, write the handback and stop. NEVER
   delete that sentinel (R-0347).
6. The slices this block carries are the whole text PLANF031R18 and
   the appended texts LEDGER18, DECISIOND6 and AMEND18. This
   paragraph names them and states no count; G3 orders you to report
   the count YOUR extractor measured.
7. THE APPENDED SLICES SHARE ONE SHAPE, STATED ONCE HERE, WITH EVERY
   GATE NAMING THIS PARAGRAPH RATHER THAN RESTATING IT. Under the
   newline-INCLUDED convention each slice already ends in a newline,
   so the target after the commit is EXACTLY: its blob at the
   commit's PARENT, then one newline, then the slice. LEDGER18 goes
   to `.agent/live_review.md` at C2, DECISIOND6 to
   `.agent/decisions.md` at C3 and AMEND18 to
   `docs/roadmap/features/T5_F031.md` at C4, and each of those
   commits receives NOTHING ELSE (R-0657). THIS BLOCK CARRIES NO
   FROM/TO PAIR, so no containment reading is owed.
8. THIS ROUND MINTS NO FINDING ID and writes no `Done:`, `Landed:` or
   `Recurrence:` line. In `.agent/live_review.md`, `^- R-\d+ — ` must
   be 242 before and 242 after with the maximum staying `R-0681`;
   `^Done: R-` 3 before and 3 after; `^Landed: R-` 1 before and 1
   after; `^Recurrence: R-` 16 before and 16 after. The §3 item 10
   open set therefore stays 239.
9. TOUCH NO CODE. Nothing under `packages/`, `apps/` or `tests/` is
   edited. `docs/roadmap/features/T5_F031.md` IS edited, by C4 and by
   nothing else; `docs/roadmap/ROADMAP.md` and `STATUS.md` are NOT —
   AGENTS.md forbids the first absent an explicit operator request,
   and this round claims and closes nothing. Do not touch
   `.agent/context.md` or either `f031_*_inventory.md`.
10. BECAUSE C4 PUTS A `docs/roadmap/**` PATH IN THE CHANGE SET, the §3
    docs-round gate IS earned and G10 orders it, together with
    `tests/orchestration/test_roadmap_index.py`, which
    `.agent/context.md` binds to any round touching that tree.
11. Destructive verification runs ONLY in a disposable `git worktree`
    under `.remedy-wt/`, removed BY ITS EXACT PATH (R-0662) and before
    the G11 suites. Everything already there is pre-existing scratch
    belonging to no commit, this block's own file included: create no
    worktree at an existing path, and delete nothing you did not
    create.
12. `npm run lint` is NOT ordered: finding R-0622 records that eslint
    parses no TypeScript here. `npm run typecheck` and
    `npm run test:unit` ARE ordered (G9) though no code moves,
    because their counts are what make "no code moved" measurable.

── Authored slices ───────────────────────────────────────────

<<<SLICE PLANF031R18
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `f031_*_inventory.md` the inventories, `.agent/decisions.md` D1–D6.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R18 records the R17 verdict and rules DECISION F031 D6 — the urgency formula
T002b orders by — into `.agent/decisions.md` and the feature file's amendment
series. No code ships, and R-0681's `Done:` text is owed by R19.

## Next Steps
1. RESOLVE R-0681 FIRST: replace its `Landed:` line in `.agent/live_review.md`
   with authored `Done:` text. The fix itself landed at `6ede183c` and the
   reviewer gated it at R18; only the marker lags.
2. T002b ORDERING, under D6: add a numeric age to `DecisionCardModel`, ship the
   comparator as its own pure function beside `decisionCard.ts`, wire it where
   the inbox is handed to the card, and update the two `toEqual` blocks in
   `decisionCard.test.ts` that pin the model's exact shape.
3. T002b FILTERING by type, then the badge under DECISION F031 D2: it
   re-derives on refetch over the existing SSE stream, no new event kind ships,
   and D2's two constant-zero counters get replaced. T003 then wires answering
   and rules whether `NeedsAttentionCard`'s decision branch is retired (D4).

## Risks
- THE SEED-KEY COLLISION, carried forward while it stands:
  `.agent/live_review.md` holds `Gate: R19` as a seed entry inherited from
  F022, so an F031 entry under that key duplicates it — the §3 item 26 defect.
  A verdict is recorded by the NEXT round, so the colliding write is R20's. The
  seed is NOT rewritten (§3 item 20); that entry takes a feature-qualified key,
  ruled as a DECISION before R20 rather than left as this bullet.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 239 at `48124293` and R18 does not move it.
- The findings THIS FEATURE MUST STILL ACT ON are R-0403, R-0413, R-0431,
  R-0441, R-0445, R-0471, R-0495, R-0533, R-0574, R-0601, R-0622, R-0625,
  R-0632, R-0672, R-0674, R-0675, R-0676, R-0677, R-0678, R-0679 and R-0681,
  the last awaiting only its resolution text; R-0495 and R-0574 are the Highs.
- R-0622 is live ground: eslint parses no TypeScript here and `npm run lint`
  exits 1 at 80 problems, so `typecheck` is the only static reader that works.
- THE SHIPPED MARKUP IS REACHED BY NO TEST, which DECISION F031 D5 rules its own
  feature, and R15's own probe measured it: deleting the mount turns nothing
  red. Every branch therefore stays in the pure layer under `apps/ui/src/api/`.
<<<END PLANF031R18

<<<SLICE LEDGER18
Gate: R17 — the F031 R17 entry. R17 PASSED ON EVERY ONE OF ITS TWELVE GATES, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk rather than reading the handback back; every value that handback states reproduced exactly. TRANSPORT HELD IN ITS STRONGEST FORM, cmp-against-scratchpad rather than the digest fallback: the reviewer's own emitted `.remedy-wt/f031-r17.md`, the committed C0a blob, the committed C0b blob and `.agent/last_block.md` off disk are ALL FOUR byte-identical at sha256 `8323814916eb60f8bf506bacd32cbc571fb5090a455a2ae0818ae0c5832e0673` over 31846 bytes and 460 lines, C0a and C0b resolving to the SAME git blob `87dbf588669fe871237e703f21b0fc5bd175d7f1`. THE EXTRACTION printed 3 slices, 51 content lines and 460 total. THE SLICES APPLIED BYTE FOR BYTE: `.agent/plan.md` at `0faf773c` equals PLANF031R17 exactly at 2892 bytes and 49 lines with the trailing-newline-removed control FALSE, `^## Goal$` 1 and `^## Next Steps$` 1; the C2 append equals its parent blob plus one newline plus LEDGER17 EXACTLY, 619591 + 1 + 4171 = 623763 against an actual 623763; and the C4 append equals its parent blob plus one newline plus LANDED17 EXACTLY, 623763 + 1 + 373 = 624137 against an actual 624137, both corroborated by an independent blank-line reader going 296 to 297 to 298 units. THE SETS MOVED ONLY WHERE CONSTRAINT 8 ALLOWED: `^- R-\d+ — ` 242 to 242 all DISTINCT, ids ADDED and ids REMOVED both the EMPTY SET, maximum `R-0681` unchanged, `^Done: R-` 3 to 3, `^Recurrence: R-` 16 to 16, `^Landed: R-` 0 to 1 gaining exactly `R-0681`, and `^Gate: R\d+ — ` 16 to 17 gaining EXACTLY the key `R16`, all 17 DISTINCT and the new header matching the shape of the series it joins (§3 item 26). The §3 item 10 open set is 239 at `c7a0b099`. THE RENAME IS THE PART THAT MATTERED AND THE REVIEWER READ IT LINE BY LINE, not only through its gates: the C3 diff at `6ede183c` is 13 changed lines and nothing else — 4 in `apps/ui/src/api/decisionCard.ts` and 9 in `apps/ui/src/api/decisionCard.test.ts` — with the parameter names, the doc comments, `DecisionCardModel` and `DecisionInboxDocument` all untouched, and both files' total line counts UNCHANGED at 194 and 226. THE COMPLETENESS GATE CARRIED A RED CONTROL THAT MOVED IN BOTH DIRECTIONS, inside a disposable worktree and never in the primary checkout: restoring the old declaration took the whole-tree count 3 to 4 and the `apps/ui/src/api/` count 0 to 1, so the gate can fail and its green reading means something. THE REVIEWER'S OWN SWEEP found the old identifier 0 times under `packages/`, `tests/`, `docs/` and `apps/cli/`, so nothing outside `apps/ui/src` referenced it. THE TOOLCHAIN READINGS ARE THE REVIEWER'S OWN, taken in the primary checkout: `npm run typecheck` exit 0 with ZERO diagnostics, and `npm run test:unit` exit 0 at 21 files and 316 tests, BOTH UNCHANGED from the base, which is the expected reading for a pure rename. THE FIVE PYTHON SUITES ARE THE REVIEWER'S OWN, run SERIALLY, never two alive at once, every one a REAL exit 0 at `tests/ui_server/` 474, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16 and `test_golden_path` 42. HYGIENE HELD: line-anchored markers 0 in all three targets against a control of 3 in the block blob itself, so the reading is not vacuous; the range `a48d1234`..`c7a0b099` names six paths, none under `packages/`, `tests/` or `docs/` and no `apps/` path beyond the two the change set names; `git ls-files .remedy-wt` 0, the zip glob 0, `git worktree list` 1 line, `git status --porcelain` 0, and the reflog read by OPERATION PREFIX over this round's seven entries shows amend 0, rebase 0 and cherry 0. THE RANGE HELD: `a48d1234`..`48124293` is SEVEN commits, every one single-parent, with per-commit insertions of 460, 290, 15, 2, 13, 2 and 60, each under the 500 cap, and the `## Commits` table's `+/-` column agrees with `git diff --numstat` cell for cell (§3 item 28). THE BLOCK'S OWN OBJECT IDS RESOLVE: 17 SHA-shaped tokens, 7 distinct, failing set EMPTY, one `blob` and six `commit`. THE PUSH DISCHARGED — measured with `git ls-remote`, the local tip and `refs/heads/feature/f031-decision-inbox` are both `48124293e77c4fc2d9de558b0ab0f1d76fd421b0`, and nothing was created or merged; the branch carries R1 through R17 unmerged. THE TWO DECLARED DEVIATIONS ARE BOTH SOUND AND THE REVIEWER CHECKED EACH RATHER THAN ACCEPTING IT. The G9 timing deviation — the toolchain readings taken at `c7a0b099` rather than at `6ede183c` — is discharged by `git diff --name-only 6ede183c..c7a0b099 -- apps/ui` naming 0 paths, which the reviewer re-ran: the `apps/ui` tree at `c7a0b099` IS the tree at `6ede183c`, so the reading describes the commit it claims to. The tooling deviation — a whole-file identifier substitution in place of a line-scoped script, forced by this session's command guard — is discharged by the diff itself, which touches exactly the 4 and 9 lines the block named and no other. Both were declared before review rather than discovered in it. R17 EARNS NO FINDING. THE VERDICT IS PASS.
<<<END LEDGER18

<<<SLICE DECISIOND6
## DECISION F031 D6 (2026-08-26) — the urgency rule is `(blockedCount + 1) × ageSeconds`, ordered open-first and totalised by `id`

CHOSEN. T002b orders the inbox by a rule stated here and pinned by a test, not
by a tooltip sentence. A card's URGENCY is `(blockedCount + 1) * ageSeconds`.
The inbox is ordered by three keys in this order: OPEN cards before closed ones;
then urgency DESCENDING; then `id` ASCENDING. An `ageSeconds` of `null` — the
endpoint's own answer for an unreadable `created_at`, which `decisionAgeLabel`
already renders as "unknown age" — scores 0 and therefore sorts last within its
group, because an unreadable stamp is not evidence of urgency.

WHY THE `+ 1`, the only departure from the feature file's own words.
`docs/roadmap/features/T5_F031.md` writes the rule as "age × blocked size" and
as "urgency = f(age, blocked_count)". A literal product collapses every decision
that blocks nothing to exactly 0 whatever its age, so an unblocking question
asked a week ago and one asked a second ago TIE and their order becomes whatever
the endpoint happened to send. DECISION F031 D3 fixes the acceptance set at the
eight PRODUCING types, among which blocking nothing is ordinary rather than an
edge, so the collapse would be the common case. Adding one keeps the product the
file asks for, keeps blocked size dominant — one blocked task doubles a card's
score — and leaves age as the total order among cards that block nothing.

WHY THE OTHER TWO KEYS EXIST. Open-first is a SEPARATE key because a resolved
decision is not urgent at any age or blocked size, and folding that into the
score means picking a constant large enough to dominate every possible product,
which a boolean key needs not. `id` is the FINAL key because without a total
order the result depends on the input order, and the test pinning this rule must
feed it a shuffled document and get exactly one answer back;
`buildDecisionCardModel` defaults `id` to the empty string, so the comparator is
total by construction.

WHAT THIS DOES NOT CHANGE. `decisionCardModels` keeps the endpoint's order and
so does the projection in `remedyApi.ts`: the two tests pinning that —
`decisionCard.test.ts` "preserves the order the endpoint sent" and
`remedyApi.test.ts` "projects every card of the document, in the endpoint's
order" — stay true and keep meaning what their names say. The rule ships as its
own comparator, applied where the inbox is handed to the card.

WHAT IT COSTS, declared so the round paying it is not read as scope drift.
`DecisionCardModel` gains a numeric age field, the model having a formatted
`ageLabel` and no number to sort by; that is additive, and the two `toEqual`
blocks in `decisionCard.test.ts` asserting the model's EXACT shape gain one line
each. WHAT IS NOT BUILDABLE IS NOT RULED: the file asks for "filters by
type/job", `DecisionInboxEntry` carries no job field at this commit, so T002b
filters by TYPE only and the job filter waits on T003's deep links.

ALTERNATIVES CONSIDERED. The literal product with no `+ 1`: rejected for the
collapse above. A lexicographic rule ranking blocked size first and age second:
rejected because it is not the multiplicative rule the file asks for and it puts
an ancient unblocking decision permanently behind any card blocking one task. A
tunable weighted sum: rejected because the weight is a number nobody can defend
and every later reviewer would relitigate it.

REVERSE IT by deleting this DECISION and its bullet in the `## Design
amendments` section of `docs/roadmap/features/T5_F031.md` that names R18, and by
restoring the literal product in the comparator this rule names.
<<<END DECISIOND6

<<<SLICE AMEND18
## Design amendments (F031 R18, 2026-08-26)

> This ruling SUPERSEDES the sentences it names above, on the same terms as the
> R5 and R11 sections: the originals stay so this file records what was planned
> and then what was ruled. Rationale, alternatives and the reversal path are in
> `.agent/decisions.md` under DECISION F031 D6.

- **D6 — urgency is `(blockedCount + 1) × ageSeconds`, open-first, `id`-total.**
  "Goal & Done" says sorting follows "a documented rule (age × blocked size)"
  and "Design (suggested shape)" says "urgency = f(age, blocked_count)". Taken
  literally, that product scores every decision blocking nothing at 0 whatever
  its age, so those cards tie and their order is the endpoint's accident, and
  DECISION F031 D3 makes them ordinary rather than rare. The rule is therefore
  `(blockedCount + 1) * ageSeconds`, ordered open cards first, then urgency
  descending, then `id` ascending so the comparator is total; a null age scores
  0 and sorts last in its group. It ships as its own comparator, so
  `decisionCardModels` and the `remedyApi.ts` projection keep the endpoint's
  order and the two tests pinning that stay true. "filters by type/job" narrows
  to TYPE alone: `DecisionInboxEntry` carries no job field, so no job filter is
  buildable until T003's deep links add one.
<<<END AMEND18

── Done when ─────────────────────────────────────────────────
Run every gate yourself, record its REAL exit code and REAL output,
and report ONE LINE PER GATE in the handback, transcripts kept out of
it (R-0582). "Green" as a word is a finding. Every gate below runs at
a commit STRICTLY EARLIER than C5 (§3 item 31); G12 runs after it and
names its own carrier.

G1  Branch and cleanliness. `git branch --show-current` prints
    `feature/f031-decision-inbox` and NOT `main`. `.agent/STOP` read
    from disk is ABSENT before C0a and again before C5. Report
    `git status --porcelain` line count after each of C0a, C0b, C1,
    C2, C3 and C4; each must be 0.

G2  Transport. Report sha256, byte count and line count for FOUR
    readings: `.remedy-wt/f031-r18.md` before C0a, the committed C0a
    blob, the committed C0b blob, and `.agent/last_block.md` off disk
    after C0b. All four must be EQUAL. Report the git blob id of C0a's
    and C0b's file; they must be the SAME id.

G3  Extraction. Run your extractor over the COMMITTED C0a blob and
    report the slice count, the CONTENT lines inside markers, and the
    TOTAL line count. Report the numbers YOUR extractor printed.

G4  The plan. `.agent/plan.md` at C1 is byte-equal to PLANF031R18
    under your stated newline convention; report slice length, file
    length and convention. NEGATIVE CONTROL: NOT byte-equal to that
    slice with its trailing newline REMOVED. `^## Goal$` 1,
    `^## Next Steps$` 1, `wc -l` STRICTLY under 50.

G5  The append at C2, as ONE equality over the whole file, in the
    shape constraint 7 states — name that paragraph, do not restate
    its formula. Report the boolean and the byte arithmetic against
    the base's 624137. Report a SECOND, INDEPENDENT reading: split the
    committed file on blank lines, take the LAST N units, and confirm
    they equal LEDGER18's N paragraphs IN ORDER, where N is the number
    YOUR split measured and not one stated here (R-0631). Give the
    unit count before and after. NEGATIVE CONTROL: flip ONE byte
    inside the paragraph the append added; BOTH readers must reject
    the mutant and BOTH accept the true file. Write any mutant only
    under a disposable worktree per constraint 11.

G6  The appends at C3 and C4, each in the same shape constraint 7
    states, each against the byte length YOU measure at that commit's
    parent. For `.agent/decisions.md` at C3 also report
    `^## DECISION F031 D\d+` moving 5 → 6, gaining exactly the
    heading numbered D6, with D1 through D5 still present. For
    `docs/roadmap/features/T5_F031.md` at C4 also report
    `^## Design amendments ` moving 2 → 3, gaining exactly the heading
    naming R18, with the R5 and R11 headings still present and all
    three DISTINCT (§3 item 26). Report each file's line count before
    and after.

G7  The ledger sets, base versus C2 in `.agent/live_review.md`:
    `^- R-\d+ — ` 242 → 242, all DISTINCT, ids ADDED and ids REMOVED
    both the EMPTY SET, maximum `R-0681` → `R-0681`. `^Done: R-`
    3 → 3, `^Landed: R-` 1 → 1 and `^Recurrence: R-` 16 → 16, all
    THREE UNCHANGED. `^Gate: R\d+ — ` 17 → 18, gaining exactly the
    key `R17`, with `R19` and `R1` through `R16` still present, and
    all 18 keys DISTINCT (§3 item 26). Report the §3 item 10 open set
    at C2 — paragraphs minus `Done:` lines — which must be 239.

G8  Markers, paths, structure and hygiene. Line-anchored `^<<<SLICE `
    and `^<<<END ` both count 0 in each target at the commit that
    writes it — `.agent/plan.md` at C1, `.agent/live_review.md` at
    C2, `.agent/decisions.md` at C3,
    `docs/roadmap/features/T5_F031.md` at C4 — against the same two
    counts over the COMMITTED C0a blob as a CONTROL, where they are
    NOT 0, so the reading is not vacuous. Report that
    `git diff --name-only <base>..C4` names NO path under `packages/`,
    `apps/` or `tests/`, no `docs/` path other than the one above, and
    neither `.agent/context.md` nor either inventory file; that the
    range path set MINUS the change set is EMPTY and the change set
    MINUS the range is exactly `.agent/handoff.md`, which C5 writes.
    Over C0a..C4 report per commit that it is single-parent and its
    INSERTION count — the `+` column only, per AGENTS.md DECISION
    F104 D1 — each under 500; those same numbers fill the `+/-`
    column of the `## Commits` table the handback template mandates,
    derived from `git diff --numstat` and NOT from `git commit`'s own
    summary, and you report that the table and this gate agree cell
    for cell (§3 item 28). Report `git ls-files .remedy-wt` as 0 and
    `git ls-files` over `*.zip` as 0. FOR THE REFLOG, state the SCOPE
    and the FIELD in the reading itself: over THIS ROUND'S entries
    only, read by the OPERATION PREFIX before the first colon of
    `git reflog --format=%gs`, report `amend`, `rebase` and `cherry`
    each 0, and how many entries you scoped to.

G9  THE CODE THIS ROUND DOES NOT TOUCH IS STILL GREEN. In the PRIMARY
    checkout, report `npm run typecheck` in `apps/ui` with its REAL
    exit code, which must be 0 with ZERO diagnostics on stdout and
    stderr, and `npm run test:unit` with its REAL exit code, file
    count and test count: both counts must be UNCHANGED at the base's
    21 and 316, because constraint 9 forbids this round any code and
    any movement is a finding. What makes those counts meaningful is
    G8's reading that the range holds no `apps/` path.

G10 THE DOCS GATES CONSTRAINT 10 EARNS. Run both in the PRIMARY
    checkout at the C4 tree, SERIALLY, with these exact command lines
    and no extra flag, both exit 0:
      python3 -m pytest tests/docs/ -q
      python3 -m pytest tests/orchestration/test_roadmap_index.py -q
    The reviewer executed both at the base `48124293` and measured
    295 passed and 30 passed, each exit 0. Report YOUR counts and
    account for any difference. A count that MOVES is not by itself a
    failure — `tests/docs/` reads feature FILENAMES and index rows,
    and this round adds neither — but an unexplained movement is.

G11 The block's own object ids, and the Python suites. Extract every
    SHA-shaped token from the COMMITTED C0a blob with the word-bounded
    pattern `[0-9a-f]{7,40}` — whose boundaries do NOT match the
    64-char sha256 digests this block also carries — and pass each to
    `git cat-file -t`. FAILING means the token does NOT RESOLVE, and
    THE FAILING SET MUST BE EMPTY: this block quotes no non-existent
    id, so it has no positive control. THE TYPES ARE NOT ALL `commit`
    AND THE GATE DOES NOT ASK THEM TO BE — LEDGER18 quotes the git
    BLOB id `87dbf588669fe871237e703f21b0fc5bd175d7f1`, resolved to
    type `blob` before emission, and every other token resolves to
    type `commit`. Report the token count YOUR extractor measured,
    the failing set, and the type per token. Then, with
    `git worktree list` reported as 1 line immediately BEFORE the
    first pytest command, run these SERIALLY in the PRIMARY checkout
    at the C4 tree, never two at once, all exit 0:
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/cli/test_golden_path.py -q
    These are the four state readers a round rewriting `.agent/` state
    gates, plus the canary. The reviewer executed all five at the base
    `48124293` with these exact command lines and no extra flag, and
    measured in that order 474, 52, 21, 16 and 42, every one exit 0.
    Account for any difference.

G12 The push. AFTER C5, run
    `git push origin feature/f031-decision-inbox`. No `--force`, no
    `--force-with-lease`, no history rewrite, no branch deletion, no
    pull request. THIS GATE'S OUTCOME IS NOT A VALUE OF ANY FILE THIS
    ROUND WRITES, and its carrier is named here so you inherit ONE
    instruction rather than two: the reviewer measures the pushed tips
    at the next gate and records them in the R18 entry of
    `.agent/live_review.md`. In `## External actions` write the push
    COMMAND and that sentence. In the item-status table the push row's
    status is `done` with the reason "ordered after C5; outcome
    carried by G12 to the reviewer" — it is NOT `deviated`, because
    the step is performed exactly as ordered and only its OUTCOME
    lands elsewhere. Report the real outcome in your final message.

── Handback ──────────────────────────────────────────────────
Rewrite `.agent/handoff.md` at C5 per docs/agents/handback_template.md:
feature and round, branch, base and commit SHAs, a changed-files table
per commit, the item-status table covering C0a, C0b, C1, C2, C3, C4,
C5 and the push, ONE LINE PER GATE with its real result, the finding
counts, and the next expected action. Carry the `Fortschritt:` block
above VERBATIM — count its lines yourself; no numeral is stated here.

EVERY NUMERAL YOUR HANDBACK STATES ABOUT A LIST IS COUNTED
MECHANICALLY BEFORE YOU COMMIT IT, or the list is named and NO numeral
is given — the widened R-0441 rule the R15 ledger entry registers.
Any finding count carries the RULE that produced it and the COMMIT it
was measured at, in the same sentence, per DECISION F009 D10; a
narrower set is named "the findings this feature must still act on"
and is never called "open" unqualified.

THE HANDBACK LINE CAP: this block states no cap and no tier. Resolve
it from AGENTS.md under `### handoff.md` against the commit count
constraint 3 fixes, and report BOTH that count and the tier. If the
MANDATED content genuinely does not fit, exceed it and carry a
DECISION D15 "Deviations, declared" line naming your measured count as
a NUMERAL (R-0430) and the mandated content behind it. Never drop a
section to fit, and claim no token cap: that cap was withdrawn.

Your `## Next` section names, in order: that the R18 verdict is
UNRECORDED and is owed by the next round's ledger commit, which by
DECISION F085 D9 no artefact of this round can carry; and that R19
resolves R-0681 and then builds T002b's ordering under DECISION F031
D6, whose obligations `## Next Steps` items 1 and 2 of the plan name.

Declare every deviation, contradiction and assumption.
──────────────────────────────────────────────────────────────

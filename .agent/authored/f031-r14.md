── STEP R14 — F031 Decision inbox ────────────────────────────
Goal:        Record the R13 verdict, RESOLVE R-0680, and give the
             shipped decision-card model its FIRST production caller:
             the dashboard payload gains a `decisionInbox` field
             projected through `decisionCardModels`, and
             `loadRemedyDashboard` gains the optional `/decisions`
             fetch that `brain-view-model` already models.

Fortschritt: ~45 % (F031 claimed; R1 through R13 landed and gated ·
             T001 SHIPPED · T002a's MODEL shipped, red-proofed and now
             WIRED · the `.tsx` projection, T002b ordering/filtering/
             badge and T003 offen) — Schaetzung

Bundle:      C0a save this block · C0b mirror it into last_block · C1
             the plan · C2 the R13 gate entry and the R-0680
             resolution · C3 the wiring with its tests · C4 handback.

Change set:  exactly these paths, nothing else —
             .agent/authored/f031-r14.md                       (C0a)
             .agent/last_block.md                              (C0b)
             .agent/plan.md                                    (C1)
             .agent/live_review.md                             (C2)
             apps/ui/src/api/types.ts                          (C3)
             apps/ui/src/api/remedyApi.ts                      (C3)
             apps/ui/src/api/remedyApi.test.ts                 (C3)
             .agent/handoff.md                                 (C4)
             This list bounds the round's WRITES, not its ACTIONS:
             the push named in G11 is ordered explicitly and is not a
             file (R-0674).

── Base ──────────────────────────────────────────────────────
The round base is `d63a146fb9c7f0a782887dd768ec7c5bb6f7dcf6`, the R13
handback commit and the tip of `feature/f031-decision-inbox`, local
and remote equal — the reviewer measured both with `git ls-remote`.
Stay on that branch; create none, never commit to `main`. Every
SHA-shaped token here was passed to `git cat-file -t` before emission
and every one resolves, so G10 orders that sweep with an EMPTY failure
set and no positive control.

Readings the reviewer MEASURED at that base, re-checkable there:
- `.agent/live_review.md`: 597681 bytes, 1207 lines, 290 blank-line
  units; `^- R-\d+ — ` 241 all DISTINCT, maximum `R-0680`;
  `^Done: R-\d+ — ` 2, so the §3 item 10 open set — the first
  pattern's paragraphs minus the second's lines — is 239;
  `^Recurrence: R-` 15; `^Gate: R\d+ — ` 13, the keys `R19` and `R1`
  through `R13` minus `R13` itself, which this round adds.
- `.agent/plan.md` 49 lines, 2910 bytes. `.agent/handoff.md` 118
  lines. `.agent/decisions.md` 566658 bytes, UNTOUCHED this round.
- `apps/ui`: `npm run test:unit` exit 0 at 21 files and 312 tests;
  `npm run typecheck` exit 0 with zero diagnostics.
- `apps/ui/src/api/remedyApi.test.ts` 535 lines, `types.ts` 221 lines.
- THE GAP THIS ROUND CLOSES, measured: `apps/ui/src/api/decisionCard.ts`
  is imported by `decisionCard.test.ts` and by NOTHING ELSE under
  `apps/ui/src`. The model ships, is red-proofed, and no production
  path calls it.

── Why this round exists ─────────────────────────────────────
R13 shipped no code and its verdict is owed by THIS round's ledger
commit, which by DECISION F085 D9 no artefact of R13 could carry. R13
also applied the fix for R-0680 at its C1; the reviewer has now
verified that fix on disk, so C2 additionally writes the `Done:`
paragraph only reviewer-authored text at a LATER gate may add.

THE BUILD STEP IS REORDERED, AND THIS SAYS SO RATHER THAN DOING IT
QUIETLY. The R13 handback named the `.tsx` projection as the next
step. This round does the DATA WIRING first and the `.tsx` next, for
one measured reason: `decisionCard.ts` has no production caller, so a
`.tsx` reading a prop nobody supplies would render nothing in the real
product and, under DECISION F031 D5, no test would reach it either —
a round that is green and inert. Wiring first gives the model a caller
inside `normalizeDashboardPayload`, which `remedyApi.test.ts` already
exercises with no fetch mocking, so the projection is PROVEN this
round and the `.tsx` gets a live source on the day it lands.

NO DECISION IS RULED AND `.agent/decisions.md` IS NOT TOUCHED. DECISION
F031 D4 says the card is built from the shipped shell and mounted in
`RightLivePanel`, and that is unchanged and still next; only the order
of two steps inside T002 moves, which is the reviewer's ordinary
planning call and not a spec amendment.

── Constraints ───────────────────────────────────────────────
1. Apply every authored slice BYTE FOR BYTE. Never retype, rewrap or
   "fix" one. If a slice looks wrong, apply it verbatim and DECLARE
   the disagreement in the handback: a contradiction inside this block
   is the reviewer's defect, not yours.
2. Slice transport. This block is saved verbatim as
   `.agent/authored/f031-r14.md` at C0a and mirrored byte-identically
   into `.agent/last_block.md` at C0b. Extract every slice
   PROGRAMMATICALLY out of the COMMITTED C0a blob by its marker LINES
   — `<<<SLICE <NAME>` opens, `<<<END <NAME>` closes. Marker lines
   never reach a target file.
3. Commit sequence, exactly: C0a, C0b, C1, C2, C3, C4. No extra
   commit, none dropped, no reordering. C1 is the FIRST substantive
   commit because this round resolves a finding (§3 item 23). C3 is
   the ONLY commit touching `apps/`, and it carries the code and its
   tests together. To correct a landed commit, do NOT add one outside
   this sequence — declare it, and give any such commit its own
   `## Commits` row and its own item-status row (R-0675).
4. Never amend, rebase, cherry-pick, force-push or rewrite history;
   never delete a branch; never merge; create no pull request.
5. `git status --porcelain` prints 0 lines after every commit. Read
   `.agent/STOP` from disk before C0a and again before C4; if present,
   finish the commit in hand, write the handback and stop. NEVER
   delete that sentinel (R-0347).
6. The slices this block carries are the whole text PLANF031R14 and
   the appended text LEDGER14. This paragraph names them and states no
   count; G3 orders you to report the count YOUR extractor measured.
   THE PRODUCTION CODE IS NOT A SLICE: section 5 below is a numbered
   SPEC and you author the TypeScript that meets it, in this
   repository's own idiom.
7. THE ONE APPEND'S SHAPE IS STATED ONCE, HERE, WITH EVERY GATE NAMING
   THIS PARAGRAPH RATHER THAN RESTATING IT. Under the newline-INCLUDED
   convention the slice already ends in a newline, so the target is
   EXACTLY: its base blob, then one newline, then the slice. LEDGER14
   goes to `.agent/live_review.md` at C2, which receives NOTHING ELSE
   in that commit (R-0657). Nothing follows it, and the file ends in
   exactly one newline because the slice carries it. THIS BLOCK
   CARRIES NO FROM/TO PAIR, so no containment reading is owed.
8. THIS ROUND MINTS NO FINDING ID AND WRITES NO `Recurrence:` LINE. It
   writes exactly ONE `Done:` line, for `R-0680`, inside LEDGER14.
   `^- R-\d+ — ` must be 241 before and 241 after with the maximum
   `R-0680` unchanged; `^Done: R-` must be 2 before and 3 after;
   `^Recurrence: R-` 15 before and 15 after. The §3 item 10 open set
   therefore moves 239 to 238.
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
12. NO EXISTING BEHAVIOUR CHANGES. No field of `RemedyDashboard` is
    renamed, reordered or removed, no existing test is edited, deleted
    or weakened, and no existing assertion moves. Every edit section 5
    orders is ADDITIVE. `npm run lint` is NOT ordered and is not run:
    finding R-0622 records that eslint parses no TypeScript here.

── 5. The production code, as a SPEC ─────────────────────────
Author the TypeScript yourself. Follow the surrounding idiom: the
one-line WHY comment sits directly above a definition, and a
deliberate absence is written down where a reader would search for it
(AGENTS.md, Code Discoverability Conventions).

S1 `apps/ui/src/api/types.ts`. `RemedyDashboard` gains exactly ONE
   field, `decisionInbox`, typed `DecisionCardModel[]` and NOT
   optional, imported from `./decisionCard`. Non-optional is the
   point: `tsc` then NAMES every construction site rather than letting
   one be silently absent. Measured at `d63a146f` there are exactly
   two such sites, both in `remedyApi.ts` and both covered by S2, and
   the one fixture that builds a dashboard — `baseDashboard` in
   `apps/ui/src/cockpitLogic.test.ts` — spreads `normalizeApiFailure`
   and therefore needs no edit. If `tsc` names a third site, STOP and
   declare it rather than widening the change set.

S2 `apps/ui/src/api/remedyApi.ts`, the projection. Import
   `decisionCardModels` from `./decisionCard`.
   `normalizeDashboardPayload` gains a FOURTH parameter, optional,
   after `brainDetail`, carrying the raw `/decisions` document. Its
   return literal gains `decisionInbox`, set to that document projected
   through `decisionCardModels`, with an absent argument treated as an
   empty document so the field is always an array.
   `normalizeApiFailure`'s literal gains `decisionInbox` as the empty
   array. Nothing else in either function changes.

S3 `apps/ui/src/api/remedyApi.ts`, the fetch. `loadRemedyDashboard`
   gains a THIRD, OPTIONAL endpoint read that MIRRORS the existing
   `brain-view-model` one in shape: same `fetchJson` helper, same
   `${base}/api/jobs/${o.jobId}/…?${q}` URL form with the endpoint
   `decisions`, same `try`/`catch`, and on failure
   `failedEndpoints.push("decisions")` and nothing else. It sits after
   the brain read and before the `normalizeDashboardPayload` call,
   whose new fourth argument is what it produced. A failure therefore
   degrades exactly as `brain-view-model` already does: the name joins
   `apiHealth.failedEndpoints` and the dashboard still renders.
   The route is real — `packages/orchestration/ui_server.py` maps the
   endpoint key `decisions` to `_build_decisions_json`, which returns
   `build_decision_inbox`'s document with its `decisions` array.

S4 `apps/ui/src/api/remedyApi.test.ts`, APPENDED at the end of the
   file — no existing test is touched. A new `describe` covering AT
   LEAST these properties, each as its own `it`:
   (a) a document with two cards projects to two models IN THE
       ENDPOINT'S ORDER, asserting the `ageLabel` and `blockedLabel`
       that `decisionCard.ts` computes for the inputs you choose;
   (b) an ABSENT fourth argument yields the empty array;
   (c) a document whose `decisions` is not an array yields the empty
       array;
   (d) `normalizeApiFailure` carries the empty array.
   Nothing is mocked and no fetch is called: that is precisely why the
   projection lives in `normalizeDashboardPayload`. You may add more
   cases; you may not add fewer properties.

── Authored slices ───────────────────────────────────────────

<<<SLICE PLANF031R14
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
R14 records the R13 verdict, resolves R-0680, and gives the shipped model its
FIRST production caller: `RemedyDashboard` gains `decisionInbox`,
`normalizeDashboardPayload` projects the `/decisions` document through
`decisionCardModels`, and `loadRemedyDashboard` reads that endpoint optionally.

## Next Steps
1. The `.tsx` projection per DECISION F031 D4: a card from the shipped
   `RightLivePanel.module.css` shell, mounted in `RightLivePanel`, reading
   `dashboard.decisionInbox` and carrying no branching of its own — every
   decision it makes must first exist in `decisionCard.ts`.
2. T002b adds ordering over age and blocked size, filtering, and the badge,
   where DECISION F031 D2 binds: the badge re-derives on refetch over the
   existing SSE stream, no new event kind ships, and D2's two constant-zero
   counters get replaced.
3. T003 wires answering through the write channel, and rules there whether
   `NeedsAttentionCard`'s decision branch is retired, which D4 leaves open.

## Risks
- THE SEED-KEY COLLISION, carried forward and never to be dropped while it
  stands: `.agent/live_review.md` holds `Gate: R19` as a seed entry inherited
  from F022, so if F031 reaches its own R19 that key collides — the §3 item 26
  defect. A round before then renames the seed or the scheme. F031 is at R14,
  so six rounds remain.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 238 once C2 lands, from 239 at `d63a146f`.
- The findings THIS FEATURE MUST STILL ACT ON are R-0403, R-0413, R-0431,
  R-0445, R-0471, R-0495, R-0533, R-0574, R-0601, R-0622, R-0625, R-0632,
  R-0672, R-0674, R-0675, R-0676, R-0677, R-0678 and R-0679; R-0495 and R-0574
  are the two Highs. R-0680 is resolved by this round's C2.
- R-0622 is live ground: eslint parses no TypeScript here and `npm run lint`
  exits 1 at 80 problems, so `typecheck` is the only static reader that works.
- The rendered markup is reached by NO test until a DOM harness lands, which
  DECISION F031 D5 rules its own feature, and `loadRemedyDashboard` is reached by
  none either — which is why the projection lands in `normalizeDashboardPayload`.
<<<END PLANF031R14

<<<SLICE LEDGER14
Gate: R13 — the F031 R13 entry. R13 PASSED ON EVERY ONE OF ITS TEN GATES, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk rather than reading the handback back; every value that handback states reproduced exactly, and no value it states was left unmeasured. TRANSPORT HELD IN ITS STRONGEST FORM, cmp-against-scratchpad rather than the digest fallback: the reviewer's own emitted `.remedy-wt/f031-r13.md`, the committed C0a blob, the committed C0b blob and `.agent/last_block.md` off disk are ALL FOUR byte-identical at sha256 `77ed31a73bb85778af3de70bcf3eb29eec311c639d692b03f117d80e27add5c8` over 29728 bytes and 345 lines, C0a and C0b resolving to the SAME git blob `15e71b0dbeabdd80100b08cb9c236d1a013258d7`. THE EXTRACTION over that committed blob printed 2 slices, 52 content lines inside markers and 345 total. THE SLICES APPLIED BYTE FOR BYTE: `.agent/plan.md` at `a48e0144` equals PLANF031R13 exactly at 2910 bytes and 49 lines, with the trailing-newline-removed control FALSE, `^## Goal$` 1, `^## Next Steps$` 1 and 49 strictly under 50; and the ledger append equals its base blob plus one newline plus LEDGER13 EXACTLY, 588533 + 1 + 9147 = 597681 against an actual 597681, corroborated by an independent blank-line split going 288 to 290 units whose last 2 units equal the slice's 2 paragraphs IN ORDER. THE REPAIR IS MEASURED, NOT ASSUMED, and it is the substance of the round: the string `R19` occurs 0 times in `.agent/plan.md` at the base `13306809` and 2 times at `a48e0144`, so the seed-key warning R-0680 records as lost is back on disk in the file AGENTS.md's Session Resume tells the next session to read SECOND. THE SETS MOVED ONLY WHERE CONSTRAINT 8 ALLOWED: `^- R-\d+ — ` 240 to 241 all DISTINCT at both ends, ids ADDED exactly `R-0680` and ids REMOVED the EMPTY SET, maximum `R-0679` to `R-0680`, `^Done: R-` 2 to 2, `^Recurrence: R-` 15 to 15, and `^Gate: R\d+ — ` 12 to 13 gaining EXACTLY the key `R12`, all 13 DISTINCT. HYGIENE HELD: markers line-anchored 0 in both targets, the range `13306809`..`bae304bc` names no path under `packages/`, `apps/`, `tests/` or `docs/` and neither `.agent/decisions.md` nor `.agent/context.md` nor either inventory, `git ls-files .remedy-wt` 0, the zip glob 0, `git worktree list` 1 line, `git status --porcelain` 0, and the reflog read by OPERATION PREFIX over this round's 5 entries shows amend 0, rebase 0 and cherry 0. THE RANGE HELD: `13306809`..`d63a146f` is FIVE commits, every one single-parent, with per-commit insertions from `git diff --numstat` of 345, 203, 31, 4 and 90 — each under the 500 cap, and the first four equal cell for cell to the `## Commits` table the handback carries. THE TOOLCHAIN AND SUITE READINGS ARE THE REVIEWER'S OWN, taken in the primary checkout: `npm run test:unit` exit 0 at 21 files and 312 tests, unchanged from the base as a round adding no test should be; `npm run typecheck` exit 0 with ZERO diagnostics; and the five Python suites run SERIALLY, never two alive at once, every one a REAL exit 0 at `tests/ui_server/` 474, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16 and `test_golden_path` 42. THE BLOCK'S OWN OBJECT IDS RESOLVE: 12 SHA-shaped tokens, 6 distinct, every one type `commit` under `git cat-file -t`, failing set EMPTY. THE HANDBACK'S SELF-CLAIMS ARE TRUE: it is 118 lines as its own DECISION D15 line declares, and the 4-line `Fortschritt:` block is carried into it VERBATIM. THE R-0586 SCAN, run by the reviewer over LEDGER13 with backtick-quoted spans deleted first, finds 0 unquoted occurrences of the forbidden label. THE NUMBERS §3 ITEM 31 RULES NO ARTEFACT OF R13 COULD CARRY: the handback commit `d63a146f` is 90 insertions and 72 deletions and single-parent; and THE PUSH DISCHARGED — measured with `git ls-remote`, the local tip and `refs/heads/feature/f031-decision-inbox` are both `d63a146fb9c7f0a782887dd768ec7c5bb6f7dcf6`, `gh pr list --state open` is EMPTY, and nothing was created or merged. THE REVIEWER ALSO SPOT-CHECKED THE FACTS LEDGER13 ASSERTS ABOUT R12 RATHER THAN TRUSTING THEM, because a shape gate never fails on a false sentence: `decisionCard.ts` and its test are 194 and 226 lines at `8df27c6e`, `git ls-tree` prints nothing for either at `8b4e2295`, and the R12 range is SIX single-parent commits whose insertions are exactly 450, 331, 17, 2, 420 and 81 over a path set of exactly seven — every one reproduced. R13 EARNS NO FINDING. ONE FACT IS RECORDED HERE FOR THE ROUND THAT FOLLOWS, not as a defect of R13, which was ordered to ship no code: measured at `d63a146f`, `apps/ui/src/api/decisionCard.ts` is imported by `decisionCard.test.ts` and by NOTHING ELSE under `apps/ui/src`, so the model that R12 shipped and red-proofed still has no production caller — which is why R14 wires it before projecting it into markup. THE VERDICT IS PASS.

Done: R-0680 — RESOLVED AT F031 R13 BY RESTORING THE WARNING AND MEASURING THE RESTORATION. R-0680 recorded that PLANF031R12, a WHOLE-FILE replacement of `.agent/plan.md`, silently dropped the R11 risk bullet warning that `.agent/live_review.md` carries `Gate: R19` as an F022 seed entry, and that the warning survived nowhere else — the string `R19` occurring 0 times in the plan at `13306809` and no paragraph of `.agent/live_review.md` or `.agent/decisions.md` recording the collision. R13's C1 applied PLANF031R13, which restores it as the FIRST bullet of `## Risks`, names the round count remaining, and marks it as never to be dropped again while it stands. THE FIX IS VERIFIED BY THE REVIEWER'S OWN READING, not by the handback: `R19` occurs 0 times in `.agent/plan.md` at `13306809` and 2 times at `a48e0144`, and the plan there is byte-equal to the authored slice at 2910 bytes and 49 lines. The STANDING RULE the finding states is unchanged and binds from here: before emitting any WHOLE-FILE replacement of a `.agent/` state file, diff the authored slice against the file it replaces and account for every bullet, constraint and warning the base carries and the slice does not — carry it forward, or state in the block WHY it is being retired and where it now lives. The R14 block that carries this resolution applied that rule to itself and says so: the base plan's `## Risks` section carries five bullets and PLANF031R14 carries the same five, head for head, which the reviewer compared mechanically before emission.
<<<END LEDGER14

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
    readings: `.remedy-wt/f031-r14.md` before C0a, the committed C0a
    blob, the committed C0b blob, and `.agent/last_block.md` off disk
    after C0b. All four must be EQUAL. Report the git blob id of C0a's
    and C0b's file; they must be the SAME id.

G3  Extraction. Run your extractor over the COMMITTED C0a blob and
    report the slice count, the CONTENT lines inside markers, and the
    TOTAL line count. Report the numbers YOUR extractor printed.

G4  The plan. `.agent/plan.md` at C1 is byte-equal to PLANF031R14
    under your stated newline convention; report slice length, file
    length and convention. NEGATIVE CONTROL: NOT byte-equal to that
    slice with its trailing newline REMOVED. `^## Goal$` 1,
    `^## Next Steps$` 1, `wc -l` STRICTLY under 50.

G5  The append, as ONE equality over the whole file, in the shape
    constraint 7 states — name that paragraph, do not restate its
    formula. Report the boolean and the byte arithmetic against the
    base's 597681. Report a SECOND, INDEPENDENT reading: split the
    committed file on blank lines, take the LAST N units, and confirm
    they equal LEDGER14's N paragraphs IN ORDER, where N is the number
    YOUR split measured and not one stated here (R-0631). Give the
    unit count before and after. NEGATIVE CONTROL: flip ONE byte
    inside the FIRST paragraph the append added; BOTH readers must
    reject the mutant and BOTH accept the true file. Write any mutant
    only under a disposable worktree per constraint 11.

G6  The sets, base versus C2 in `.agent/live_review.md`:
    `^- R-\d+ — ` 241 → 241, all DISTINCT, the ids ADDED and the ids
    REMOVED both the EMPTY SET, maximum `R-0680` UNCHANGED.
    `^Done: R-` 2 → 3, the ids ADDED being exactly `R-0680`.
    `^Recurrence: R-` 15 → 15, UNCHANGED. `^Gate: R\d+ — ` 13 → 14,
    gaining exactly the key `R13`, with `R19` and `R1` through `R12`
    still present, and all 14 keys DISTINCT (§3 item 26). Report the
    §3 item 10 open set at C2 — paragraphs minus `Done:` lines — which
    must be 238.

G7  Markers, paths, structure and hygiene. Line-anchored `^<<<SLICE `
    and `^<<<END ` both count 0 in `.agent/plan.md` at C1,
    `.agent/live_review.md` at C2, and each of the `apps/` files
    section 5 names, at C3. Report that `git diff --name-only
    <base>..C3` names NO path under `packages/`, `tests/` or `docs/`,
    no path under `apps/` other than those section 5 names, and neither
    `.agent/decisions.md` nor `.agent/context.md` nor either inventory
    file. Over C0a..C3 report per commit that it is single-parent and
    its INSERTION count — the `+` column only, per AGENTS.md DECISION
    F104 D1 — each under 500. Those same numbers fill the `+/-` column
    of the `## Commits` table the handback template mandates: derive
    that column from `git diff --numstat` and NOT from the files'
    before/after line counts, and report that the table and this gate
    agree cell for cell (§3 item 28). Report the range path set MINUS
    the change set (EMPTY) and the change set MINUS the range (exactly
    `.agent/handoff.md`, which C4 writes). Report
    `git ls-files .remedy-wt` as 0 and `git ls-files` over `*.zip` as
    0. FOR THE REFLOG, state the SCOPE and the FIELD in the reading
    itself: over THIS ROUND'S entries only, read by the OPERATION
    PREFIX before the first colon of `git reflog --format=%gs`, report
    `amend`, `rebase` and `cherry` each 0, and how many entries you
    scoped to.

G8  THE CODE COMPILES AND THE SUITE GREW. In `apps/ui` at C3 report
    `npm run typecheck` with its REAL exit code, which must be 0 with
    ZERO diagnostics — under finding R-0622 it is the only static
    reader that works here, and S1's non-optional field means a missed
    construction site shows up HERE. Report `npm run test:unit` with
    its REAL exit code, its file count and its test count. The file
    count must be UNCHANGED at 21, because S4 appends to an existing
    file and adds none. The test count must be STRICTLY GREATER than
    the base's 312; report the number YOU measured and the difference,
    and do NOT expect a number this block states, because this block
    states none. Report also that `git diff <base>..C3 -- apps/ui` has
    NO deleted line in `remedyApi.test.ts` (constraint 12: no existing
    test is edited or weakened).

G9  THE RED PROOF, that the new tests reach the projection rather than
    assert near it. In a disposable worktree per constraint 11, using
    the route finding R-0653's resolution records — `npx vitest run
    src/api/remedyApi.test.ts --root <worktree>/apps/ui --config
    <primary>/apps/ui/vitest.config.ts`, run with the working
    directory inside the PRIMARY `apps/ui` so npx and the config
    resolve against the primary install and nothing is written to the
    primary checkout — FIRST run an UNMUTATED control at that SAME
    root and report its colour and counts, because only a control at
    the same root makes a mutant's effect attributable. THEN mutate
    `normalizeDashboardPayload` in the WORKTREE ONLY so that
    `decisionInbox` is the empty array for every input, ignoring the
    document it was given, and re-run the SAME command. Report the
    exit code, whether the run is RED, and the NAME of every test that
    failed. Do not report a count as the property: the property is
    that the run goes RED and that the failures are S4's cases.
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
    AND THE GATE DOES NOT ASK THEM TO BE — LEDGER14 quotes the git
    BLOB id `15e71b0dbeabdd80100b08cb9c236d1a013258d7`, which the
    reviewer resolved to type `blob` before emission, and every other
    token resolves to type `commit`. Report the token count YOUR
    extractor measured, the failing set, and the type per token. Then, with `git worktree list` reported as 1 line
    immediately BEFORE the first pytest command, run these SERIALLY in
    the PRIMARY checkout at the C3 tree, never two at once, all
    exit 0:
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/cli/test_golden_path.py -q
    These are the four state readers a round rewriting `.agent/` state
    gates, plus the canary. The reviewer executed all five at the base
    `d63a146f` with these exact command lines and no extra flag, and
    measured in that order 474, 52, 21, 16 and 42, every one exit 0.
    Account for any difference.

G11 The push. AFTER C4, run
    `git push origin feature/f031-decision-inbox`. No `--force`, no
    `--force-with-lease`, no history rewrite, no branch deletion, no
    pull request. THIS GATE'S OUTCOME IS NOT A VALUE OF ANY FILE THIS
    ROUND WRITES, and its carrier is named here so you inherit ONE
    instruction rather than two: the reviewer measures the pushed tips
    at the next gate and records them in the R14 entry of
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
pull request exists for this branch); that the R14 verdict is
UNRECORDED and is owed by the next round's ledger commit, which by
DECISION F085 D9 no artefact of this round can carry; and that the
next build step is the `.tsx` projection per DECISION F031 D4, reading
`dashboard.decisionInbox`, mounted in `RightLivePanel`, with no
branching of its own.

Declare every deviation, contradiction and assumption.
──────────────────────────────────────────────────────────────

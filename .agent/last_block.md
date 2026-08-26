── STEP R17 — F031 Decision inbox ────────────────────────────
Goal:        Record the R16 verdict and REPAIR R-0681. The interface
             `apps/ui/src/api/decisionCard.ts` exports as
             `DecisionInboxCard` is renamed `DecisionInboxEntry`,
             carrying every occurrence of that identifier in its own
             file and in `decisionCard.test.ts`. The React component
             `DecisionInboxCard.tsx` and its mount keep their names.
             This is a SPLIT round: it ships production code, and no
             round of that kind may be self-certified.

Fortschritt: ~57 % (F031 claimed; R1 through R16 landed and gated ·
             T001 SHIPPED · T002a MODEL shipped, wired and RENDERED ·
             R-0681 repaired here · T002b ordering/filtering/badge
             und T003 offen) — Schaetzung

Bundle:      C0a save this block · C0b mirror it into last_block · C1
             the plan · C2 the R16 gate entry · C3 the rename · C4 the
             `Landed:` line for R-0681 · C5 handback.

Change set:  exactly these paths, nothing else —
             .agent/authored/f031-r17.md                       (C0a)
             .agent/last_block.md                              (C0b)
             .agent/plan.md                                    (C1)
             .agent/live_review.md                        (C2 and C4)
             apps/ui/src/api/decisionCard.ts                   (C3)
             apps/ui/src/api/decisionCard.test.ts              (C3)
             .agent/handoff.md                                 (C5)
             This list bounds the round's WRITES, not its ACTIONS:
             the push named in G12 is ordered explicitly and is not a
             file (R-0674).

── Base ──────────────────────────────────────────────────────
The round base is `a48d1234a5c82797a7760adadf1fa00140b92019`, the R16
handback commit and the tip of `feature/f031-decision-inbox`, local
and remote equal — the reviewer measured both with `git ls-remote`.
Stay on that branch; create none, never commit to `main`. Every
SHA-shaped token here was passed to `git cat-file -t` before emission
and every one RESOLVES; the types are NOT all `commit` and G11 does
not ask them to be.

Readings the reviewer MEASURED at that base, re-checkable there:
- `.agent/live_review.md`: 619591 bytes, 1219 lines, 296 blank-line
  units; `^- R-\d+ — ` 242 all DISTINCT, maximum `R-0681`;
  `^Done: R-\d+ — ` 3, so the §3 item 10 open set — the first
  pattern's paragraphs minus the second's lines — is 239;
  `^Recurrence: R-` 16; `^Landed: R-` 0; `^Gate: R\d+ — ` 16, the
  keys `R19` and `R1` through `R15`, `R16` being what this round adds.
- `.agent/plan.md` 49 lines, 2985 bytes. `.agent/handoff.md` 84
  lines. `.agent/decisions.md` UNTOUCHED this round.
- `apps/ui`: `npm run test:unit` exit 0 at 21 files and 316 tests;
  `npm run typecheck` exit 0 with zero diagnostics.
- THE RENAME'S GROUND, measured by `git grep -n` over `apps/ui/src`
  at that base. The identifier `DecisionInboxCard` occurs on 16
  lines across four files. THIRTEEN of them are the INTERFACE and
  are what C3 renames: `apps/ui/src/api/decisionCard.ts` lines 58,
  145, 165 and 193, and `apps/ui/src/api/decisionCard.test.ts` lines
  9, 73, 84, 101, 119, 130, 143, 144 and 152. THREE of them are the
  COMPONENT and C3 leaves them alone:
  `apps/ui/src/components/panels/DecisionInboxCard.tsx` line 30, and
  `apps/ui/src/components/panels/RightLivePanel.tsx` lines 7 and 22
  — line 7 carries the identifier AND the module path, and a line is
  counted once. `DecisionInboxEntry` occurs 0 times anywhere in this
  repository, which the reviewer measured with `git grep` over the
  whole tree before choosing it.
- `apps/ui/src/api/decisionCard.ts` is 194 lines and
  `apps/ui/src/api/decisionCard.test.ts` is 226 lines.

── Why this round exists ─────────────────────────────────────
R16's verdict is owed by THIS round's ledger commit, which by
DECISION F085 D9 no artefact of R16 could carry. R16 PASSED: the
reviewer re-ran all ten of its gates itself and every value it states
reproduced exactly. The full reading is the LEDGER17 slice below.

THE ROUND THEN REPAIRS R-0681, which R16 registered and deliberately
did not fix, being the last round of its session. The interface and
the component share one identifier for two unrelated concepts with
INVERTED cardinality — the singular-sounding `DecisionInboxCard`
interface is ONE endpoint entry, while the component of that name
renders the WHOLE inbox. AGENTS.md's Code Discoverability
Conventions require a name to grep to its own definition and real
usages only, and one spelling to serve one concept repo-wide.

THE INTERFACE IS THE HALF THAT RENAMES, not the component. `Card` is
the idiom every sibling in `apps/ui/src/components/panels/` uses, so
the component's name is right; the interface's is not, and its own
doc comment at `apps/ui/src/api/decisionCard.ts` line 52 already
calls it "One entry of the endpoint's `decisions` array". Its
sibling in the same file is `DecisionInboxDocument`, so
`DecisionInboxEntry` joins an existing naming series rather than
inventing one.

A CORRECTION THIS ROUND OWES THE RECORD: R-0681's FIX clause, landed
at `7d031ab1`, orders the rename to carry "its three use sites and
the test import". The three use sites in `decisionCard.ts` are
right, and "the test import" undercounts — `decisionCard.test.ts`
carries the identifier on nine lines, of which one is the import and
eight are type annotations. The landed finding is NOT rewritten (§3
item 20); the correction is dated into LEDGER17 and the true list is
the one this block's Base section measures.

── Constraints ───────────────────────────────────────────────
1. Apply every authored slice BYTE FOR BYTE. Never retype, rewrap or
   "fix" one. If a slice looks wrong, apply it verbatim and DECLARE
   the disagreement in the handback: a contradiction inside this block
   is the reviewer's defect, not yours.
2. Slice transport. This block is saved verbatim as
   `.agent/authored/f031-r17.md` at C0a and mirrored byte-identically
   into `.agent/last_block.md` at C0b. Extract every slice
   PROGRAMMATICALLY out of the COMMITTED C0a blob by its marker LINES
   — `<<<SLICE <NAME>` opens, `<<<END <NAME>` closes. Marker lines
   never reach a target file.
3. Commit sequence, exactly: C0a, C0b, C1, C2, C3, C4, C5. No extra
   commit, none dropped, no reordering. C1 is the FIRST substantive
   commit because this round writes the finding ledger (§3 item 23).
   C3 lands the rename and C4 follows it, so the `Landed:` line C4
   applies is true when it lands — this is the ordering constraint
   §3 item 20's R-0524 carve-out requires, since no SHA for C3 can
   exist while LANDED17 is authored. To correct a landed commit, do
   NOT add one outside this sequence — declare it, and give any such
   commit its own `## Commits` row and its own item-status row
   (R-0675).
4. Never amend, rebase, cherry-pick, force-push or rewrite history;
   never delete a branch; never merge; create no pull request.
5. `git status --porcelain` prints 0 lines after every commit. Read
   `.agent/STOP` from disk before C0a and again before C5; if present,
   finish the commit in hand, write the handback and stop. NEVER
   delete that sentinel (R-0347).
6. The slices this block carries are the whole text PLANF031R17, the
   appended text LEDGER17 and the appended text LANDED17. This
   paragraph names them and states no count; G3 orders you to report
   the count YOUR extractor measured.
7. THE APPENDED SLICES SHARE ONE SHAPE, STATED ONCE HERE, WITH EVERY
   GATE NAMING THIS PARAGRAPH RATHER THAN RESTATING IT. Under the
   newline-INCLUDED convention each slice already ends in a newline,
   so the target after the commit is EXACTLY: its blob at the
   commit's PARENT, then one newline, then the slice. LEDGER17 goes
   to `.agent/live_review.md` at C2 and LANDED17 goes to the same
   file at C4, and each of those commits receives NOTHING ELSE
   (R-0657). Nothing follows either slice, and the file ends in
   exactly one newline because the slice carries it. THIS BLOCK
   CARRIES NO FROM/TO PAIR, so no containment reading is owed, and
   C3 is described by the SPEC in the next section rather than
   sliced.
8. THIS ROUND MINTS NO FINDING ID and writes no `Done:` line and no
   `Recurrence:` line. `^- R-\d+ — ` must be 242 before and 242
   after, the maximum must stay `R-0681`, `^Done: R-` 3 before and 3
   after, `^Recurrence: R-` 16 before and 16 after. The §3 item 10
   open set therefore stays 239. `^Landed: R-` moves 0 to 1, gaining
   exactly `R-0681`: §4.4 of docs/agents/planner_reviewer_prompt.md
   reserves `Done:` for reviewer text written AFTER the fix is
   gated, so a fix landing inside its own round is marked `Landed:`
   and the reviewer replaces that line at the next gate. Do NOT
   write a `Done:` paragraph of your own, however honestly hedged.
9. THE CODE CHANGE IS EXACTLY THE RENAME. Nothing under `packages/`,
   `tests/` or `docs/` is edited, and no `apps/` path outside the two
   named in the change set. Do not touch `.agent/decisions.md`,
   `.agent/context.md`, `.agent/f031_inventory.md` or
   `.agent/f031_ui_inventory.md` — landed evidence is corrected by
   dating in a later round, never by editing (§3 item 20). This round
   rules no DECISION.
10. `docs/roadmap/ROADMAP.md` and `docs/roadmap/STATUS.md` are NOT
    touched: AGENTS.md forbids the first absent an explicit operator
    request, and this round claims and closes nothing. Because no
    `docs/roadmap/**` path is in the change set, the §3 docs-round
    gate is not earned and is not ordered.
11. Destructive verification runs ONLY in a disposable `git worktree`
    under `.remedy-wt/`, removed BY ITS EXACT PATH (R-0662) and before
    the G11 suites. Everything already under `.remedy-wt/` is
    pre-existing scratch belonging to no commit, this block's own file
    included: create no worktree at an existing path there, and delete
    nothing you did not create.
12. `npm run lint` is NOT ordered and is not run: finding R-0622
    records that eslint parses no TypeScript here.
13. A FRESH WORKTREE CANNOT TYPECHECK, and the reviewer measured this
    at emission rather than leaving you to discover it: a worktree
    under `.remedy-wt/` has no `apps/ui/node_modules`, and running
    `tsc --noEmit --project <worktree>/apps/ui/tsconfig.json` from the
    primary checkout exits 2 with `TS2307 Cannot find module 'react'`
    and a wall of `TS7026`, because node resolution walks from the
    worktree path. So `npm run typecheck` is ordered ONLY in the
    PRIMARY checkout (G9) and NO typecheck red control is ordered —
    G10 carries this round's red control instead, over the grep gate,
    which needs no dependencies. State this limit in the handback
    rather than claiming a sensitivity nothing measured.

── C3, the rename: SPEC, not a slice ─────────────────────────
Production code is DESCRIBED and you author the bytes; nothing below
is a slice and nothing below is hash-stamped.

S1. In `apps/ui/src/api/decisionCard.ts`, replace the identifier
    `DecisionInboxCard` with `DecisionInboxEntry` at each of the four
    lines the Base section names — the `export interface` declaration
    and the three type positions. Change nothing else in that file:
    not the `card` PARAMETER names, not the doc comments, not the
    prose word "card" wherever it appears, not `DecisionCardModel`,
    not `DecisionInboxDocument`, not the module's own filename.
S2. In `apps/ui/src/api/decisionCard.test.ts`, replace the same
    identifier with `DecisionInboxEntry` at each of the nine lines the
    Base section names — the `import type` on line 9 and the eight
    type annotations. Change nothing else: no test name, no fixture
    value, no assertion, no variable named `card`.
S3. Touch NOTHING under `apps/ui/src/components/`. The component
    `DecisionInboxCard`, its file name, its import in
    `RightLivePanel.tsx` and its mount all keep the name they have.
S4. The rename is a pure identifier substitution over a CLOSED set:
    after S1 and S2 the old identifier must not occur anywhere under
    `apps/ui/src/api/`. G10 measures that; do not assume it.

── Authored slices ───────────────────────────────────────────

<<<SLICE PLANF031R17
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
R17 records the R16 verdict and REPAIRS R-0681: the interface
`apps/ui/src/api/decisionCard.ts` exports as `DecisionInboxCard` becomes
`DecisionInboxEntry`, carrying every occurrence of that identifier in its own
file and in `decisionCard.test.ts`. The React component keeps its name.

## Next Steps
1. T002b adds ordering over age and blocked size, filtering, and the badge,
   where DECISION F031 D2 binds: the badge re-derives on refetch over the
   existing SSE stream, no new event kind ships, and D2's two constant-zero
   counters get replaced.
2. T003 wires answering through the write channel — the card's answer buttons
   ship DISABLED until it lands — and rules there whether
   `NeedsAttentionCard`'s decision branch is retired, which D4 leaves open.
3. Settle the seed-key collision the first risk below names.

## Risks
- THE SEED-KEY COLLISION, carried forward and never to be dropped while it
  stands: `.agent/live_review.md` holds `Gate: R19` as a seed entry inherited
  from F022, so an F031 entry under that same key would duplicate it — the §3
  item 26 defect. A round's verdict is recorded by the NEXT round's ledger
  commit, so the colliding write is R20's. The landed seed is NOT rewritten,
  which §3 item 20 forbids; the entry that would collide takes a
  feature-qualified key instead.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 239 at `a48d1234`, and R17 mints no id.
- The findings THIS FEATURE MUST STILL ACT ON are R-0403, R-0413, R-0431,
  R-0441, R-0445, R-0471, R-0495, R-0533, R-0574, R-0601, R-0622, R-0625,
  R-0632, R-0672, R-0674, R-0675, R-0676, R-0677, R-0678, R-0679 and R-0681,
  the last of which this round repairs; R-0495 and R-0574 are the two Highs.
- R-0622 is live ground: eslint parses no TypeScript here and `npm run lint`
  exits 1 at 80 problems, so `typecheck` is the only static reader that works.
- THE SHIPPED MARKUP IS REACHED BY NO TEST, which DECISION F031 D5 rules its own
  feature, and R15's own probe measured it: deleting the mount turns nothing
  red. Every branch therefore stays in `decisionCard.ts`.
<<<END PLANF031R17

<<<SLICE LEDGER17
Gate: R16 — the F031 R16 entry. R16 PASSED ON EVERY ONE OF ITS TEN GATES, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk rather than reading the handback back; every value that handback states reproduced exactly. TRANSPORT HELD IN ITS STRONGEST FORM: the committed C0a blob, the committed C0b blob and `.agent/last_block.md` off disk are byte-identical at sha256 `1a101776247772758a13c23238ac5415757dbf02074abbf141d6183434edd603` over 29626 bytes and 365 lines, C0a and C0b resolving to the SAME git blob `5845552a2f9f2164a774bce6aa12edffb95737cd`. THE EXTRACTION printed 2 slices, 52 content lines and 365 total. THE SLICES APPLIED BYTE FOR BYTE: `.agent/plan.md` at `877fc883` equals PLANF031R16 exactly at 2985 bytes and 49 lines with the trailing-newline-removed control FALSE, `^## Goal$` 1 and `^## Next Steps$` 1; and the ledger append at `7d031ab1` equals its base blob plus one newline plus LEDGER16 EXACTLY, 611720 + 1 + 7870 = 619591 against an actual 619591. THE SETS MOVED ONLY WHERE CONSTRAINT 8 ALLOWED: `^- R-\d+ — ` 241 to 242 all DISTINCT, ids ADDED exactly `R-0681` and ids REMOVED the EMPTY SET, maximum `R-0680` to `R-0681`, `^Done: R-` 3 to 3, `^Recurrence: R-` 16 to 16, and `^Gate: R\d+ — ` 15 to 16 gaining EXACTLY the key `R15`, all 16 DISTINCT, whose header shape matches the series it joins (§3 item 26). The §3 item 10 open set is 239 at `7d031ab1`. THE R-0586 SCAN OVER THE APPENDED SLICE, backtick spans deleted first, counts 0 unquoted occurrences of the bare word this checklist forbids. HYGIENE HELD: line-anchored markers 0 in both targets, the range `4fc7dc77`..`7d031ab1` names four paths and none under `packages/`, `apps/`, `tests/` or `docs/`, `git ls-files .remedy-wt` 0, `git worktree list` 1 line, `git status --porcelain` 0, and the reflog read by OPERATION PREFIX over this round's five entries shows amend 0, rebase 0 and cherry 0. THE RANGE HELD: `4fc7dc77`..`a48d1234` is FIVE commits, every one single-parent, with per-commit insertions of 365, 174, 18, 4 and 44 for C0a through C3 and the handback, each under the 500 cap, and the `## Commits` table's `+/-` column agrees with `git diff --numstat` cell for cell (§3 item 28). THE BLOCK'S OWN OBJECT IDS RESOLVE: 14 SHA-shaped tokens, 7 distinct, failing set EMPTY, one `blob` and six `commit`. THE TOOLCHAIN READINGS ARE THE REVIEWER'S OWN, taken in the primary checkout: `npm run typecheck` exit 0 with ZERO diagnostics, and `npm run test:unit` exit 0 at 21 files and 316 tests, BOTH UNCHANGED from the base, which is the expected reading for a round that touched no code. THE FIVE PYTHON SUITES ARE THE REVIEWER'S OWN, run SERIALLY, never two alive at once, every one a REAL exit 0 at `tests/ui_server/` 474, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16 and `test_golden_path` 42. THE PUSH DISCHARGED — measured with `git ls-remote`, the local tip and `refs/heads/feature/f031-decision-inbox` are both `a48d1234a5c82797a7760adadf1fa00140b92019`, `gh pr list --state open` printed `[]`, and nothing was created or merged; the branch carries R1 through R16 unmerged. THE HANDBACK'S DECLARED OVERAGE IS HONEST: it measures 84 newlines against a base tier of 60, and every line the reviewer counted belongs to content AGENTS.md or the handback template mandates. R16 SHIPPED NO CODE, exactly as its constraint 9 ordered, and the reviewer confirms the range names no path under `apps/`. ONE CORRECTION IS OWED TO THE RECORD AND IS DATED HERE RATHER THAN EDITED IN: the FIX clause of R-0681, landed at `7d031ab1`, orders the rename to carry "its three use sites and the test import", and measured at `a48d1234` the test file `apps/ui/src/api/decisionCard.test.ts` carries the identifier on NINE lines — the `import type` on line 9 plus eight type annotations on lines 73, 84, 101, 119, 130, 143, 144 and 152 — so the clause's "the test import" undercounts the work by eight lines. The three use sites in `apps/ui/src/api/decisionCard.ts` — lines 145, 165 and 193, beside the declaration at line 58 — are correct as stated. R-0681's finding body is otherwise sound and its diagnosis reproduced in full. THE VERDICT IS PASS.
<<<END LEDGER17

<<<SLICE LANDED17
Landed: R-0681 — the interface `DecisionInboxCard` in `apps/ui/src/api/decisionCard.ts` is now `DecisionInboxEntry`, renamed across four lines of that file and nine of `apps/ui/src/api/decisionCard.test.ts`; the React component `DecisionInboxCard` and its mount are untouched. Landed at the C3 commit of F031 R17, whose position constraint 3 of that round's block fixes.
<<<END LANDED17

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
    readings: `.remedy-wt/f031-r17.md` before C0a, the committed C0a
    blob, the committed C0b blob, and `.agent/last_block.md` off disk
    after C0b. All four must be EQUAL. Report the git blob id of C0a's
    and C0b's file; they must be the SAME id.

G3  Extraction. Run your extractor over the COMMITTED C0a blob and
    report the slice count, the CONTENT lines inside markers, and the
    TOTAL line count. Report the numbers YOUR extractor printed.

G4  The plan. `.agent/plan.md` at C1 is byte-equal to PLANF031R17
    under your stated newline convention; report slice length, file
    length and convention. NEGATIVE CONTROL: NOT byte-equal to that
    slice with its trailing newline REMOVED. `^## Goal$` 1,
    `^## Next Steps$` 1, `wc -l` STRICTLY under 50.

G5  The appends, each as ONE equality over the whole file, in the
    shape constraint 7 states — name that paragraph, do not restate
    its formula. For C2 report the boolean and the byte arithmetic
    against the base's 619591; for C4 report the boolean and the byte
    arithmetic against whatever C2 left, which you measure rather
    than take from here. Report a SECOND, INDEPENDENT reading for
    EACH: split the committed file on blank lines, take the LAST N
    units, and confirm they equal that slice's N paragraphs IN ORDER,
    where N is the number YOUR split measured and not one stated here
    (R-0631). Give the unit count before and after each commit.
    NEGATIVE CONTROL, for C2 only: flip ONE byte inside the paragraph
    the append added; BOTH readers must reject the mutant and BOTH
    accept the true file. Write any mutant only under a disposable
    worktree per constraint 11.

G6  The sets, base versus C4 in `.agent/live_review.md`:
    `^- R-\d+ — ` 242 → 242, all DISTINCT, the ids ADDED and the ids
    REMOVED both the EMPTY SET, maximum `R-0681` → `R-0681`.
    `^Done: R-` 3 → 3 and `^Recurrence: R-` 16 → 16, both UNCHANGED.
    `^Landed: R-` 0 → 1, gaining exactly `R-0681`. `^Gate: R\d+ — `
    16 → 17, gaining exactly the key `R16`, with `R19` and `R1`
    through `R15` still present, and all 17 keys DISTINCT (§3 item
    26). Report the §3 item 10 open set at C4 — paragraphs minus
    `Done:` lines — which must be 239.

G7  Markers, paths and structure. Line-anchored `^<<<SLICE ` and
    `^<<<END ` both count 0 in `.agent/plan.md` at C1 and in
    `.agent/live_review.md` at C2 and at C4. Report that
    `git diff --name-only <base>..C4` names NO path under `packages/`,
    `tests/` or `docs/`, no `apps/` path other than the two the change
    set names, and neither `.agent/decisions.md` nor
    `.agent/context.md` nor either inventory file. Over C0a..C4 report
    per commit that it is single-parent and its INSERTION count — the
    `+` column only, per AGENTS.md DECISION F104 D1 — each under 500.
    Those same numbers fill the `+/-` column of the `## Commits` table
    the handback template mandates: derive that column from
    `git diff --numstat` and NOT from `git commit`'s own summary,
    which applies rewrite detection and reports different figures for
    a full-file rewrite, and report that the table and this gate agree
    cell for cell (§3 item 28). Report the range path set MINUS the
    change set (EMPTY) and the change set MINUS the range (exactly
    `.agent/handoff.md`, which C5 writes).

G8  Hygiene. Report `git ls-files .remedy-wt` as 0 and `git ls-files`
    over `*.zip` as 0. FOR THE REFLOG, state the SCOPE and the FIELD
    in the reading itself: over THIS ROUND'S entries only, read by the
    OPERATION PREFIX before the first colon of
    `git reflog --format=%gs`, report `amend`, `rebase` and `cherry`
    each 0, and how many entries you scoped to. Report
    `git worktree list` as 1 line immediately BEFORE the first pytest
    command of G11.

G9  THE RENAME TYPE-CHECKS AND THE SUITE IS UNMOVED. In the PRIMARY
    checkout at the C3 tree, and never in a worktree — constraint 13
    measured why — report `npm run typecheck` in `apps/ui` with its
    REAL exit code, which must be 0 with ZERO diagnostics on stdout
    and stderr, and `npm run test:unit` with its REAL exit code, file
    count and test count: both counts must be UNCHANGED at the base's
    21 and 316, because a rename adds and removes no test and any
    movement is a finding. In the same handback line state the LIMIT
    constraint 13 names: no red control was run against typecheck,
    so this reading proves consistency and not sensitivity.

G10 THE RENAME IS COMPLETE AND BOUNDED, and this gate carries the
    round's red control. At the C3 tree report, with `git grep -n`
    over `apps/ui/src`: the identifier `DecisionInboxCard` occurs on
    exactly 3 lines, in exactly the two files
    `apps/ui/src/components/panels/DecisionInboxCard.tsx` and
    `apps/ui/src/components/panels/RightLivePanel.tsx`, and 0 times
    anywhere under `apps/ui/src/api/`; and `DecisionInboxEntry`
    occurs on exactly 13 lines, in exactly the two files
    `apps/ui/src/api/decisionCard.ts` and
    `apps/ui/src/api/decisionCard.test.ts`. Report also that
    `git diff --numstat <base>..C3` names exactly those two api files
    with 4 insertions and 4 deletions for `decisionCard.ts` and 9 and
    9 for `decisionCard.test.ts`, and that the total line counts are
    UNCHANGED at 194 and 226 — a pure substitution adds no line.
    RED CONTROL, inside a disposable worktree at C3 per constraint 11
    and never in the primary checkout: in that worktree's
    `apps/ui/src/api/decisionCard.ts` replace the byte string
    `export interface DecisionInboxEntry {`, which occurs EXACTLY
    ONCE in that file at C3 — report that count before replacing —
    with `export interface DecisionInboxCard {`, then re-run the two
    grep readings above and report that the first now counts 4 lines
    rather than 3 and that the `apps/ui/src/api/` reading is now 1
    rather than 0. BOTH must move, or this gate cannot fail and
    proves nothing. Remove the worktree BY ITS EXACT PATH afterwards.

G11 The block's own object ids, and the Python suites. Extract every
    SHA-shaped token from the COMMITTED C0a blob with the word-bounded
    pattern `[0-9a-f]{7,40}` — whose boundaries do NOT match the
    64-char sha256 digests this block also carries — and pass each to
    `git cat-file -t`. FAILING means the token does NOT RESOLVE, and
    THE FAILING SET MUST BE EMPTY: this block quotes no non-existent
    id, so it has no positive control. THE TYPES ARE NOT ALL `commit`
    AND THE GATE DOES NOT ASK THEM TO BE — LEDGER17 quotes the git
    BLOB id `5845552a2f9f2164a774bce6aa12edffb95737cd`, which the
    reviewer resolved to type `blob` before emission, and every other
    token resolves to type `commit`. Report the token count YOUR
    extractor measured, the failing set, and the type per token. Then
    run these SERIALLY in the PRIMARY checkout at the C4 tree, never
    two at once, all exit 0:
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/cli/test_golden_path.py -q
    These are the four state readers a round rewriting `.agent/` state
    gates, plus the canary. The reviewer executed all five at the base
    `a48d1234` with these exact command lines and no extra flag, and
    measured in that order 474, 52, 21, 16 and 42, every one exit 0.
    Account for any difference.

G12 The push. AFTER C5, run
    `git push origin feature/f031-decision-inbox`. No `--force`, no
    `--force-with-lease`, no history rewrite, no branch deletion, no
    pull request. THIS GATE'S OUTCOME IS NOT A VALUE OF ANY FILE THIS
    ROUND WRITES, and its carrier is named here so you inherit ONE
    instruction rather than two: the reviewer measures the pushed tips
    at the next gate and records them in the R17 entry of
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

Your `## Next` section names, in order: that the R17 verdict is
UNRECORDED and is owed by the next round's ledger commit, which by
DECISION F085 D9 no artefact of this round can carry; that the
`Landed: R-0681` line is an UNREVIEWED fix until the reviewer replaces
it with authored `Done:` text at that gate; and that T002b is the next
build step under DECISION F031 D2.

Declare every deviation, contradiction and assumption.
──────────────────────────────────────────────────────────────

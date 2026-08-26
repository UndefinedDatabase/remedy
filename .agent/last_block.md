── STEP R19 — F031 Decision inbox ────────────────────────────
Goal:        Record the R18 verdict, RESOLVE R-0681 by replacing its
             `Landed:` line with authored `Done:` text, and register
             a RECURRENCE of R-0385 against the reviewer's own R17
             block. This round ships NO code: T002b's ordering is
             R20's, under the rule DECISION F031 D6 already fixed.

Fortschritt: ~59 % (F031 claimed; R1 through R18 landed and gated ·
             T001 SHIPPED · T002a MODEL shipped, wired and RENDERED ·
             R-0681 resolved here · T002b ordering/filtering/badge
             und T003 offen) — Schaetzung

Bundle:      C0a save this block · C0b mirror it into last_block · C1
             the plan · C2 the R-0681 resolution · C3 the R18 gate
             entry and the R-0385 recurrence · C4 handback.

Change set:  exactly these paths, nothing else —
             .agent/authored/f031-r19.md                       (C0a)
             .agent/last_block.md                              (C0b)
             .agent/plan.md                                    (C1)
             .agent/live_review.md                        (C2 and C3)
             .agent/handoff.md                                 (C4)
             This list bounds the round's WRITES, not its ACTIONS:
             the push named in G10 is ordered explicitly and is not a
             file (R-0674).

── Base ──────────────────────────────────────────────────────
The round base is `6c758fc84316cacc0162fb6fdf290b8d3034fe09`, the R18
handback commit and the tip of `feature/f031-decision-inbox`, local
and remote equal — the reviewer measured both with `git ls-remote`.
Stay on that branch; create none, never commit to `main`. Every
SHA-shaped token here resolved under `git cat-file -t` before
emission; the types are NOT all `commit` and G9 does not ask them to
be.

Readings the reviewer MEASURED at that base, re-checkable there:
- `.agent/live_review.md` 629198 bytes; `^- R-\d+ — ` 242 all
  DISTINCT, maximum `R-0681`; `^Done: R-\d+ — ` 3, so the §3 item 10
  open set — the first pattern's paragraphs minus the second's lines
  — is 239; `^Recurrence: R-` 16; `^Landed: R-` 1, that line being
  R-0681's and occurring EXACTLY ONCE in the file; `^Gate: R\d+ — `
  18, the keys `R19` and `R1` through `R17`.
- `.agent/plan.md` 49 lines, 3024 bytes. `.agent/handoff.md` 93
  lines. `.agent/decisions.md` and `docs/roadmap/**` UNTOUCHED this
  round, so the §3 docs-round gate is not earned and is not ordered.
- `apps/ui`: `npm run typecheck` exit 0 with zero diagnostics;
  `npm run test:unit` exit 0 at 21 files and 316 tests.
- THIS BLOCK'S OWN TWO CAPS, measured on its final bytes before
  emission and stated here so your re-measurement can disagree with
  the reviewer's: DECISION F085 D6 budgets a block at 490 lines TOTAL
  and DECISION F085 D5 caps its PROSE — TOTAL minus the slice CONTENT
  inside the markers — at 400. G3 orders you to report both from the
  COMMITTED blob.

── Why this round exists ─────────────────────────────────────
R18's verdict is owed by THIS round's ledger commit, which by
DECISION F085 D9 no artefact of R18 could carry. R18 PASSED on all
twelve of its gates, every one re-run by the reviewer; LEDGER19 is
the full reading.

R-0681 IS RESOLVED HERE, as R18's own plan ordered. The fix landed at
`6ede183c` and was gated at R18; only the `Landed:` marker lagged,
R18's block having no line budget left for the resolution. §4.4
orders the reviewer to replace that placeholder at the next gate.

THE REVIEWER REGISTERS A RECURRENCE AGAINST ITSELF. Measured at
`8e4e55d6`, the R17 block ran 409 prose lines against the 400-line
cap DECISION F085 D5 sets, because the reviewer checked every block
against a single remembered budget of 490 TOTAL and never evaluated
the prose cap at all. That is the defect R-0385 already records, so
§3 item 30 forbids a second id and LEDGER19 carries a `Recurrence:`
line instead. The counter-measure is in this block's own Base
section: both caps measured, both stated, both re-measured by you.

T002b'S ORDERING IS DELIBERATELY NOT IN THIS ROUND. It was drafted
into it and the block came out over both caps three times running,
which is the condition DECISION F085 D6 answers by changing the
design rather than squeezing the prose. The rule it builds under —
DECISION F031 D6, landed at `24b47b3b` and mirrored in the feature
file at `75d4b532` — is already on disk, so R20 can be a pure code
round with no ruling left to make.

── Constraints ───────────────────────────────────────────────
1. Apply every authored slice BYTE FOR BYTE. Never retype, rewrap or
   "fix" one. If a slice looks wrong, apply it verbatim and DECLARE
   the disagreement: a contradiction inside this block is the
   reviewer's defect, not yours.
2. Slice transport. This block is saved verbatim as
   `.agent/authored/f031-r19.md` at C0a and mirrored byte-identically
   into `.agent/last_block.md` at C0b. Extract every slice
   PROGRAMMATICALLY out of the COMMITTED C0a blob by its marker LINES
   — `<<<SLICE <NAME>` opens, `<<<END <NAME>` closes. Marker lines
   never reach a target file.
3. Commit sequence, exactly: C0a, C0b, C1, C2, C3, C4. No extra
   commit, none dropped, no reordering. C1 is FIRST substantive
   because this round writes the finding ledger (§3 item 23); C2
   precedes C3 so the replacement happens where the line already sits
   and C3's append stays a true append at the tail. To correct a
   landed commit, do NOT add one outside this sequence — declare it,
   and give it its own `## Commits` and item-status rows (R-0675).
4. Never amend, rebase, cherry-pick, force-push or rewrite history;
   never delete a branch; never merge; create no pull request.
5. `git status --porcelain` prints 0 lines after every commit. Read
   `.agent/STOP` from disk before C0a and again before C4; if
   present, finish the commit in hand, write the handback and stop.
   NEVER delete that sentinel (R-0347).
6. The slices this block carries are the whole text PLANF031R19, the
   pair's FROM text LANDEDFROM, that pair's TO text DONE0681, and the
   appended text LEDGER19. This paragraph names them and states no
   count; G3 orders you to report the count YOUR extractor measured.
7. THE ONE APPEND'S SHAPE, STATED ONCE HERE, WITH EVERY GATE NAMING
   THIS PARAGRAPH RATHER THAN RESTATING IT. Under the newline-INCLUDED
   convention the slice already ends in a newline, so the target after
   the commit is EXACTLY: its blob at the commit's PARENT, then one
   newline, then the slice. LEDGER19 goes to `.agent/live_review.md`
   at C3, which receives NOTHING ELSE in that commit (R-0657).
   LEDGER19 carries more than one paragraph; G6 orders you to report
   how many YOUR split measured, and this paragraph states no number.
8. THE ONE PAIR'S SHAPE, MEASURED NOT ASSERTED (§3 item 15). The
   containment test printed `TO contains FROM: false` before
   emission, so LANDEDFROM → DONE0681 is a REWRITE and the §4.9
   rewrite obligation applies: after C2 the FROM text occurs 0 times
   in `.agent/live_review.md` and the TO text exactly 1. The FROM
   occurs EXACTLY ONCE in that file at the base, so the target is
   unique (§3 item 25). Replace in place; do not append.
9. THIS ROUND MINTS NO FINDING ID. `^- R-\d+ — ` must be 242 before
   and after, maximum staying `R-0681`. `^Landed: R-` moves 1 to 0
   and `^Done: R-` moves 3 to 4 gaining exactly `R-0681` — ONE edit,
   C2, and a round where only one happened is a failed round — so the
   §3 item 10 open set moves 239 to 238. `^Recurrence: R-` moves 16
   to 17 at C3, gaining exactly `R-0385`.
10. TOUCH NO CODE and no document. Nothing under `packages/`,
    `apps/`, `tests/` or `docs/` is edited, and neither
    `.agent/decisions.md`, `.agent/context.md` nor either
    `f031_*_inventory.md` — landed evidence is corrected by dating in
    a later round, never by editing (§3 item 20). This round rules no
    DECISION.
11. Destructive verification runs ONLY in a disposable `git worktree`
    under `.remedy-wt/`, removed BY ITS EXACT PATH (R-0662) and
    before the G9 suites. Everything already there is pre-existing
    scratch belonging to no commit, this block's own file included:
    create no worktree at an existing path, and delete nothing you
    did not create.
12. `npm run lint` is NOT ordered: R-0622 records that eslint parses
    no TypeScript here. `typecheck` and `test:unit` ARE ordered (G8)
    though no code moves, because their counts are what make "no code
    moved" measurable.

── Authored slices ───────────────────────────────────────────

<<<SLICE PLANF031R19
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
R19 records the R18 verdict, resolves R-0681 with authored `Done:` text, and
registers a recurrence of R-0385 against the reviewer's own R17 block, which ran
409 prose lines against a 400-line cap. No code ships.

## Next Steps
1. R20 ships T002b ORDERING under DECISION F031 D6, already on disk: add
   `ageSeconds` to `DecisionCardModel` — `buildDecisionCardModel` computes that
   local already and only omits it from the returned object — ship the
   comparator as `apps/ui/src/api/decisionOrder.ts` with its own `.test.ts`,
   wire it in `RightLivePanel`, and update the two `toEqual` blocks in
   `decisionCard.test.ts` that pin the model's exact shape. R20 must ALSO rule
   the seed-key collision the first risk below names.
2. T002b FILTERING by type — D6 narrows the feature file's "filters by
   type/job" to TYPE alone, `DecisionInboxEntry` carrying no job field.
3. T002b BADGE under DECISION F031 D2: it re-derives on refetch over the
   existing SSE stream, no new event kind, D2's two constant-zero counters
   replaced. T003 then wires answering and rules `NeedsAttentionCard` (D4).

## Risks
- THE SEED-KEY COLLISION, now the nearest deadline: `.agent/live_review.md`
  holds `Gate: R19` as a seed entry inherited from F022, and a verdict is
  recorded by the NEXT round, so R20's ledger entry is the first that would
  duplicate that key — the §3 item 26 defect. The seed is NOT rewritten (§3
  item 20); R20 rules a feature-qualified key as a DECISION before writing it.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 238 once C2 lands, from 239 at `6c758fc8`.
- The findings THIS FEATURE MUST STILL ACT ON are R-0403, R-0413, R-0431,
  R-0441, R-0445, R-0471, R-0495, R-0533, R-0574, R-0601, R-0622, R-0625,
  R-0632, R-0672, R-0674, R-0675, R-0676, R-0677, R-0678 and R-0679; R-0495 and
  R-0574 are the two Highs. R-0681 leaves this list at C2.
- BLOCK CAPS ARE TWO, not one: 490 lines TOTAL (DECISION F085 D6) and 400 lines
  PROSE (DECISION F085 D5). R-0385's recurrence is what happens when only the
  first is checked; every block from here states and re-measures both.
- THE SHIPPED MARKUP IS REACHED BY NO TEST, which DECISION F031 D5 rules its own
  feature, so T002b's logic lives in the pure layer under `apps/ui/src/api/`.
<<<END PLANF031R19

<<<SLICE LANDEDFROM
Landed: R-0681 — the interface `DecisionInboxCard` in `apps/ui/src/api/decisionCard.ts` is now `DecisionInboxEntry`, renamed across four lines of that file and nine of `apps/ui/src/api/decisionCard.test.ts`; the React component `DecisionInboxCard` and its mount are untouched. Landed at the C3 commit of F031 R17, whose position constraint 3 of that round's block fixes.
<<<END LANDEDFROM

<<<SLICE DONE0681
Done: R-0681 — RESOLVED at F031 R17, commit `6ede183c`, and gated by the reviewer at R18. The interface `apps/ui/src/api/decisionCard.ts` exported as `DecisionInboxCard` is now `DecisionInboxEntry`, joining the `DecisionInboxDocument` series already in that file and matching its own doc comment, which called it "One entry of the endpoint's `decisions` array" before the rename and still does. THE REVIEWER MEASURED THE FIX ITSELF at `6ede183c`: `git grep -n` over `apps/ui/src` counts `DecisionInboxCard` on exactly 3 lines, all of them the COMPONENT — `apps/ui/src/components/panels/DecisionInboxCard.tsx` line 30 and `apps/ui/src/components/panels/RightLivePanel.tsx` lines 7 and 22 — and 0 lines anywhere under `apps/ui/src/api/`; `DecisionInboxEntry` counts exactly 13 lines in exactly `apps/ui/src/api/decisionCard.ts` and `apps/ui/src/api/decisionCard.test.ts`; `git diff --numstat` for that commit reads 4 and 4 for the first and 9 and 9 for the second, with both files' total line counts UNCHANGED at 194 and 226, which is what makes it a pure substitution rather than an edit. The reviewer also read the whole diff: the parameter names `card`, the doc comments, `DecisionCardModel` and `DecisionInboxDocument` are all untouched, and a sweep over `packages/`, `tests/`, `docs/` and `apps/cli/` found the old identifier 0 times, so nothing outside `apps/ui/src` referenced it. `npm run typecheck` exit 0 with zero diagnostics and `npm run test:unit` exit 0 at 21 files and 316 tests, both re-run by the reviewer in the primary checkout. THE LIMIT OF THAT EVIDENCE, stated because a green reading is not a sensitive one: no red control was run against `typecheck`, because a fresh worktree under `.remedy-wt/` has no `apps/ui/node_modules` and `tsc` there exits 2 on `TS2307 Cannot find module 'react'` before it reads any of this repository's own types. The grep gate carried the round's red control instead and it MOVED in both directions, taking the whole-tree count 3 to 4 and the `apps/ui/src/api/` count 0 to 1 when the old declaration was restored inside a disposable worktree, so the completeness half of this resolution rests on measurement rather than on the compiler's silence. ONE CORRECTION TO THIS FINDING'S OWN FIX CLAUSE, dated rather than edited in: that clause ordered the rename to carry "its three use sites and the test import", and the test file carried the identifier on NINE lines, so the clause undercounted the work by eight; the R16 gate entry records that correction and R17 performed the full thirteen. THE STANDING RULE R-0681 ESTABLISHED IS UNCHANGED and binds the reviewer from here: before a spec names any new exported symbol, grep the repository for that identifier and report the result in the block.
<<<END DONE0681

<<<SLICE LEDGER19
Gate: R18 — the F031 R18 entry. R18 PASSED ON EVERY ONE OF ITS TWELVE GATES, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk rather than reading the handback back; every value that handback states reproduced exactly. TRANSPORT HELD IN ITS STRONGEST FORM, cmp-against-scratchpad rather than the digest fallback: the reviewer's own emitted `.remedy-wt/f031-r18.md`, the committed C0a blob, the committed C0b blob and `.agent/last_block.md` off disk are ALL FOUR byte-identical at sha256 `32b2664d1827403c438ab4bd54327956a64f29779ddc82ed2da6f3a58fe31364` over 33873 bytes and 476 lines, C0a and C0b resolving to the SAME git blob `c732ebf49afd964f5d2ccdc19a4f6da0482c548f`. THE EXTRACTION printed 4 slices, 125 content lines and 476 total. THE THREE APPENDS APPLIED BYTE FOR BYTE, each equal to its parent blob plus one newline plus its slice: `.agent/live_review.md` at `7107a563` at 624137 + 1 + 5060 = 629198 against an actual 629198; `.agent/decisions.md` at `24b47b3b` at 566658 + 1 + 3653 = 570312 against an actual 570312; and `docs/roadmap/features/T5_F031.md` at `75d4b532` at 8485 + 1 + 1318 = 9804 against an actual 9804. `.agent/plan.md` at `a0565593` equals PLANF031R18 exactly at 3024 bytes and 49 lines with the trailing-newline-removed control FALSE, `^## Goal$` 1 and `^## Next Steps$` 1. THE SETS MOVED ONLY WHERE CONSTRAINT 8 ALLOWED: `^- R-\d+ — ` 242 to 242 all DISTINCT, ids ADDED and ids REMOVED both the EMPTY SET, maximum `R-0681` unchanged, and `^Done: R-` 3 to 3, `^Landed: R-` 1 to 1 and `^Recurrence: R-` 16 to 16, all three UNCHANGED as a round writing none of them requires. `^Gate: R\d+ — ` 17 to 18 gaining EXACTLY the key `R17`, all 18 DISTINCT and the new header matching the shape of the series it joins (§3 item 26). The §3 item 10 open set is 239 at `7107a563`. THE TWO NEW DOCUMENT HEADINGS ALSO JOIN THEIR SERIES CORRECTLY, which is the same item-26 reading applied to two more files: `^## DECISION F031 D\d+` 5 to 6 gaining exactly the D6 heading with D1 through D5 still present, and `^## Design amendments ` 2 to 3 gaining exactly the R18 heading with the R5 and R11 headings still present and all three DISTINCT. THE RULING ITSELF IS THE POINT OF THIS ROUND and the reviewer read both landed texts rather than only their byte counts: DECISION F031 D6 fixes the urgency rule at `(blockedCount + 1) * ageSeconds` ordered open-first, urgency descending and `id` ascending, states the `+ 1` as its only departure from the feature file's literal product and gives the reason — a literal product ties every card that blocks nothing, which DECISION F031 D3 makes the common case — declares the cost to `DecisionCardModel` and to the two exact-shape assertions before the round that pays it, narrows "filters by type/job" to TYPE alone because `DecisionInboxEntry` carries no job field, and carries a REVERSE IT clause naming both the decision and its feature-file bullet. The feature-file amendment mirrors it and supersedes nothing silently. HYGIENE HELD: line-anchored markers 0 in all four targets against a control of 4 in the block blob itself, so the reading is not vacuous; the range `6c758fc8`'s predecessor `48124293`..`75d4b532` names six paths, none under `packages/`, `apps/` or `tests/` and exactly one under `docs/`; `git ls-files .remedy-wt` 0, the zip glob 0, `git worktree list` 1 line, `git status --porcelain` 0, and the reflog read by OPERATION PREFIX over this round's seven entries shows amend 0, rebase 0 and cherry 0. THE RANGE HELD: `48124293`..`6c758fc8` is SEVEN commits, every one single-parent, with per-commit insertions of 476, 310, 26, 2, 56, 21 and 45, each under the 500 cap, and the `## Commits` table's `+/-` column agrees with `git diff --numstat` cell for cell (§3 item 28). THE BLOCK'S OWN OBJECT IDS RESOLVE: 22 SHA-shaped tokens, 8 distinct, failing set EMPTY, one `blob` and seven `commit`. THE CODE THIS ROUND DID NOT TOUCH IS STILL GREEN, measured by the reviewer in the primary checkout: `npm run typecheck` exit 0 with ZERO diagnostics and `npm run test:unit` exit 0 at 21 files and 316 tests, both UNCHANGED, which is the expected reading for a round whose range holds no `apps/` path. THE SEVEN PYTHON SUITES ARE THE REVIEWER'S OWN, run SERIALLY, never two alive at once, every one a REAL exit 0: the docs-round gate this round EARNED by touching `docs/roadmap/**` at `tests/docs/` 295 and `test_roadmap_index` 30, plus the four state readers and the canary at `tests/ui_server/` 474, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16 and `test_golden_path` 42. THE PUSH DISCHARGED — measured with `git ls-remote`, the local tip and `refs/heads/feature/f031-decision-inbox` are both `6c758fc84316cacc0162fb6fdf290b8d3034fe09`, and nothing was created or merged; the branch carries R1 through R18 unmerged. THE DECLARED DEVIATIONS ARE SOUND: the command guard rejected two measurement-only shell forms, each re-run in an accepted form with no committed byte affected, and the scratch this round created — one worktree and one slice directory — was removed by exact path, never by glob. R18 EARNS NO FINDING. THE VERDICT IS PASS.

Recurrence: R-0385 — THE REVIEWER'S OWN R17 BLOCK WAS EMITTED OVER THE 400-LINE PROSE CAP, which is exactly the defect R-0385 registered and which no gate of R16, R17 or R18 measured. Measured at `8e4e55d6`, `.agent/authored/f031-r17.md` is 460 lines TOTAL holding 51 lines of slice CONTENT inside 3 marker pairs, so its PROSE is 409 lines counting the marker lines and 403 without them; DECISION F085 D5 caps a block's prose at 400 and DECISION F085 D6 caps its TOTAL at 490, and the R17 block met the second while breaking the first. THE CAUSE IS THE REVIEWER'S, not the worker's: the reviewer carried a single remembered budget of 490 lines and checked every block against that alone, so the prose cap was never evaluated at emission for three consecutive rounds. R16 at 313 prose lines and R18 at 351 were inside it by luck of length rather than by measurement. THE LANDED BLOCK IS NOT REWRITTEN (§3 item 20) and no round is reopened: R17's content was correct and its gates all passed. NO NEW ID IS MINTED, because §3 item 30 forbids a second id for a defect the open set already holds and R-0385 is that record — the same class, R-0363 being its earlier instance. THE COUNTER-MEASURE, binding the reviewer from here: every block is measured against BOTH caps before emission, prose computed as TOTAL minus slice CONTENT, and both numbers are stated in the block's own constraints so the worker's re-measurement can disagree with the reviewer's. This round's block is the first to carry that reading.
<<<END LEDGER19

── Done when ─────────────────────────────────────────────────
Run every gate yourself, record its REAL exit code and REAL output,
and report ONE LINE PER GATE in the handback, transcripts kept out of
it (R-0582). "Green" as a word is a finding. Every gate runs at a
commit STRICTLY EARLIER than C4 (§3 item 31); G10 runs after it and
names its own carrier.

G1  Branch and cleanliness. `git branch --show-current` prints
    `feature/f031-decision-inbox` and NOT `main`. `.agent/STOP` read
    from disk is ABSENT before C0a and again before C4. Report
    `git status --porcelain` line count after each of C0a, C0b, C1,
    C2 and C3; each must be 0.

G2  Transport. Report sha256, byte count and line count for FOUR
    readings: `.remedy-wt/f031-r19.md` before C0a, the committed C0a
    blob, the committed C0b blob, and `.agent/last_block.md` off disk
    after C0b. All four must be EQUAL. Report the git blob id of
    C0a's and C0b's file; they must be the SAME id.

G3  Extraction and the block's own two caps. Run your extractor over
    the COMMITTED C0a blob and report the slice count, the CONTENT
    lines inside markers, and the TOTAL line count — the numbers YOUR
    extractor printed. Then report PROSE, computed as TOTAL minus
    CONTENT, against the two caps the Base section names: TOTAL at
    most 490 and PROSE at most 400. If either is exceeded, say so
    plainly and continue — an oversize block is the reviewer's defect
    to record, not yours to fix.

G4  The plan. `.agent/plan.md` at C1 is byte-equal to PLANF031R19
    under your stated newline convention; report slice length, file
    length and convention. NEGATIVE CONTROL: NOT byte-equal to that
    slice with its trailing newline REMOVED. `^## Goal$` 1,
    `^## Next Steps$` 1, `wc -l` STRICTLY under 50.

G5  THE PAIR, in the REWRITE shape constraint 8 measured — name that
    paragraph, do not restate its reading. Before C2 report
    LANDEDFROM's count in `.agent/live_review.md`, which must be
    exactly 1; after C2 report LANDEDFROM's count, which must be 0,
    and DONE0681's, which must be exactly 1. Report that
    `git diff --numstat` for C2 names `.agent/live_review.md` alone,
    and that the file's byte length moved by exactly the two slices'
    difference in length, computed from the extracted slices rather
    than taken from here.

G6  The append at C3, as ONE equality over the whole file, in the
    shape constraint 7 states — name that paragraph, do not restate
    its formula. Report the boolean and the byte arithmetic against
    whatever C2 left, which you measure rather than take from here.
    Report a SECOND, INDEPENDENT reading: split the committed file on
    blank lines, take the LAST N units, and confirm they equal
    LEDGER19's N paragraphs IN ORDER, where N is the number YOUR
    split measured (R-0631); give the unit count before and after.
    NEGATIVE CONTROL: flip ONE byte inside the FIRST paragraph the
    append added; BOTH readers must reject the mutant and BOTH accept
    the true file. Write any mutant only under a disposable worktree
    per constraint 11.

G7  The ledger sets, base versus C3 in `.agent/live_review.md`:
    `^- R-\d+ — ` 242 → 242 all DISTINCT, ids ADDED and REMOVED both
    the EMPTY SET, maximum `R-0681` → `R-0681`. `^Landed: R-` 1 → 0
    and `^Done: R-` 3 → 4, the ADDED `Done:` id being exactly
    `R-0681`. `^Recurrence: R-` 16 → 17, gaining exactly `R-0385`.
    `^Gate: R\d+ — ` 18 → 19, gaining exactly the key `R18`, with
    `R19` and `R1` through `R17` still present and all 19 DISTINCT
    (§3 item 26). Report the §3 item 10 open set at C3 — paragraphs
    minus `Done:` lines — which must be 238.

G8  Markers, paths, hygiene, and the code this round does not touch.
    Line-anchored `^<<<SLICE ` and `^<<<END ` both 0 in
    `.agent/plan.md` at C1 and `.agent/live_review.md` at C3, against
    the same counts over the COMMITTED C0a blob as a CONTROL, where
    they are NOT 0. Report that `git diff --name-only <base>..C3`
    names NO path under `packages/`, `apps/`, `tests/` or `docs/`,
    and neither `.agent/decisions.md` nor `.agent/context.md` nor
    either inventory file; that the range path set MINUS the change
    set is EMPTY and the change set MINUS the range is exactly
    `.agent/handoff.md`, which C4 writes. Over C0a..C3 report per
    commit that it is single-parent and its INSERTION count — the `+`
    column only, per AGENTS.md DECISION F104 D1 — each under 500;
    those same numbers fill the `+/-` column of the `## Commits`
    table, derived from `git diff --numstat` and NOT from
    `git commit`'s own summary, and you report that the two agree
    cell for cell (§3 item 28). Report `git ls-files .remedy-wt` as 0
    and `git ls-files` over `*.zip` as 0. FOR THE REFLOG, state SCOPE
    and FIELD in the reading: over THIS ROUND'S entries only, by the
    OPERATION PREFIX before the first colon of
    `git reflog --format=%gs`, report `amend`, `rebase` and `cherry`
    each 0 and how many entries you scoped to. Finally, in the
    PRIMARY checkout: `npm run typecheck` in `apps/ui` REAL exit 0
    with ZERO diagnostics on stdout and stderr, and `npm run
    test:unit` REAL exit 0 with both counts UNCHANGED at the base's
    21 files and 316 tests — any movement is a finding, and what
    makes them meaningful is the path reading above.

G9  The block's own object ids, and the Python suites. Extract every
    SHA-shaped token from the COMMITTED C0a blob with the word-bounded
    pattern `[0-9a-f]{7,40}` — whose boundaries do NOT match the
    64-char sha256 digests this block also carries — and pass each to
    `git cat-file -t`. FAILING means the token does NOT RESOLVE, and
    THE FAILING SET MUST BE EMPTY: this block quotes no non-existent
    id, so it has no positive control. THE TYPES ARE NOT ALL `commit`
    AND THE GATE DOES NOT ASK THEM TO BE — LEDGER19 quotes the git
    BLOB id `c732ebf49afd964f5d2ccdc19a4f6da0482c548f`, resolved to
    type `blob` before emission, every other token resolving to
    `commit`. Report the token count YOUR extractor measured, the
    failing set, and the type per token. Then, with
    `git worktree list` reported as 1 line immediately BEFORE the
    first pytest command, run these SERIALLY in the PRIMARY checkout
    at the C3 tree, never two at once, all exit 0:
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/cli/test_golden_path.py -q
    These are the four state readers a round rewriting `.agent/` state
    gates, plus the canary. The reviewer executed all five at the base
    `6c758fc8` with these exact command lines and no extra flag, and
    measured in that order 474, 52, 21, 16 and 42, every one exit 0.
    Account for any difference.

G10 The push. AFTER C4, run
    `git push origin feature/f031-decision-inbox`. No `--force`, no
    `--force-with-lease`, no history rewrite, no branch deletion, no
    pull request. THIS GATE'S OUTCOME IS NOT A VALUE OF ANY FILE THIS
    ROUND WRITES, and its carrier is named here so you inherit ONE
    instruction rather than two: the reviewer measures the pushed tips
    at the next gate and records them in the R19 entry of
    `.agent/live_review.md`. In `## External actions` write the push
    COMMAND and that sentence. In the item-status table the push row
    is `done`, reason "ordered after C4; outcome carried by G10 to
    the reviewer" — NOT `deviated`, the step being performed exactly
    as ordered with only its OUTCOME landing elsewhere. Report the
    real outcome in your final message.

── Handback ──────────────────────────────────────────────────
Rewrite `.agent/handoff.md` at C4 per docs/agents/handback_template.md:
feature and round, branch, base and commit SHAs, a changed-files table
per commit, the item-status table covering C0a through C4 and the
push, ONE LINE PER GATE with its real result, the finding counts, and
the next expected action. Carry the `Fortschritt:` block above
VERBATIM — count its lines yourself; no numeral is stated here.

EVERY NUMERAL YOUR HANDBACK STATES ABOUT A LIST IS COUNTED
MECHANICALLY BEFORE YOU COMMIT IT, or the list is named and NO numeral
is given (R-0441). Any finding count carries the RULE that produced it
and the COMMIT it was measured at, in one sentence, per DECISION F009
D10; a narrower set is named "the findings this feature must still act
on", never "open" unqualified.

THE HANDBACK LINE CAP: this block states no cap and no tier. Resolve
it from AGENTS.md under `### handoff.md` against the commit count
constraint 3 fixes, and report BOTH that count and the tier. If the
MANDATED content genuinely does not fit, exceed it and carry a
DECISION D15 "Deviations, declared" line naming your measured count as
a NUMERAL (R-0430) and the mandated content behind it. Never drop a
section to fit, and claim no token cap: that cap was withdrawn.

Your `## Next` section names, in order: that the R19 verdict is
UNRECORDED and is owed by the next round's ledger commit (DECISION
F085 D9); that R20 is the T002b ORDERING round under DECISION F031
D6, which is already on disk and needs no further ruling; and that
R20's ledger entry is the FIRST that would collide with the inherited
`Gate: R19` seed key, so R20's block must rule the feature-qualified
key before writing it.

Declare every deviation, contradiction and assumption.
──────────────────────────────────────────────────────────────

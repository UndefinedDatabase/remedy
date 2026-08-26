── STEP R13 — F031 Decision inbox ────────────────────────────
Goal:        Record the R12 verdict, REGISTER the reviewer's own
             defect — a whole-file plan rewrite silently dropped the
             only carrier of a standing forward-looking warning — and
             REPAIR it in the same round by restoring that warning to
             the plan. No production code.

Fortschritt: ~40 % (F031 claimed; R1 through R12 landed and gated ·
             T001 SHIPPED · T002a's MODEL shipped and red-proofed ·
             the `.tsx` projection, T002b ordering/filtering/badge and
             T003 offen) — Schaetzung

Bundle:      C0a save this block · C0b mirror it into last_block · C1
             the plan, carrying the repair · C2 the R12 gate entry and
             the new finding · C3 handback.

Change set:  exactly these paths, nothing else —
             .agent/authored/f031-r13.md                       (C0a)
             .agent/last_block.md                              (C0b)
             .agent/plan.md                                    (C1)
             .agent/live_review.md                             (C2)
             .agent/handoff.md                                 (C3)
             This list bounds the round's WRITES, not its ACTIONS:
             the push named in G10 is ordered explicitly and is not a
             file (R-0674).

── Base ──────────────────────────────────────────────────────
The round base is `13306809da092eef995061b5809dd70e5a93f505`, the R12
handback commit and the tip of `feature/f031-decision-inbox`, local
and remote equal. Stay on that branch; create none, never commit to
`main`. Every SHA-shaped token here was passed to `git cat-file -t`
before emission and every one resolves, so G9 orders that sweep with
an EMPTY failure set and no positive control.

Readings the reviewer MEASURED at that base, re-checkable there:
- `.agent/live_review.md`: 588533 bytes, 1203 lines, 288 blank-line
  units; `^- R-\d+ — ` 240 all DISTINCT, maximum `R-0679`;
  `^Done: R-\d+ — ` 2, so the §3 item 10 open set — the first
  pattern's paragraphs minus the second's lines — is 238;
  `^Recurrence: R-` 15; `^Gate: R\d+ — ` 12, the keys `R19` and `R1`
  through `R12` minus `R12` itself, which this round adds.
- `.agent/plan.md` 49 lines, 2918 bytes. `.agent/handoff.md` 100
  lines. `.agent/decisions.md` 566658 bytes, UNTOUCHED this round.
- The string `R19` occurs 0 times in `.agent/plan.md`, and no
  paragraph of `.agent/live_review.md` or `.agent/decisions.md`
  records the seed-key collision the R11 plan warned of. The reviewer
  searched both files for it before minting the finding below.

── Why this round exists ─────────────────────────────────────
R12 shipped the decision-card model and its 27 tests, and its own
verdict is owed by THIS round's ledger commit, which by DECISION F085
D9 no artefact of R12 could carry.

THE ROUND ALSO REPAIRS A DEFECT OF THE REVIEWER'S OWN. The R11 plan
carried a risk bullet warning that `.agent/live_review.md` holds
`Gate: R19` as a seed entry inherited from F022, so if F031 ever
reaches its own R19 that key collides — the §3 item 26 defect. The R12
plan slice, authored by the reviewer as a WHOLE-FILE replacement,
simply did not carry that bullet forward, and the warning existed
nowhere else: measured at the base, `R19` appears 0 times in
`.agent/plan.md` and no ledger or decisions paragraph records the
risk. A whole-file rewrite is a delete of everything it does not
repeat, and the plan is the file AGENTS.md's Session Resume tells the
next session to read SECOND.

The R12 WORKER found this, said so in its report, and deliberately did
NOT repair it — substituting its own text for an authored slice is the
worse defect, and the call was the reviewer's to make. That is the
workflow behaving exactly as designed, and it is why C2 registers the
finding against the reviewer rather than against the round.

── Constraints ───────────────────────────────────────────────
1. Apply every authored slice BYTE FOR BYTE. Never retype, rewrap or
   "fix" one. If a slice looks wrong, apply it verbatim and DECLARE
   the disagreement in the handback: a contradiction inside this block
   is the reviewer's defect, not yours.
2. Slice transport. This block is saved verbatim as
   `.agent/authored/f031-r13.md` at C0a and mirrored byte-identically
   into `.agent/last_block.md` at C0b. Extract every slice
   PROGRAMMATICALLY out of the COMMITTED C0a blob by its marker LINES
   — `<<<SLICE <NAME>` opens, `<<<END <NAME>` closes. Marker lines
   never reach a target file.
3. Commit sequence, exactly: C0a, C0b, C1, C2, C3. No extra commit,
   none dropped, no reordering. C1 is the FIRST substantive commit
   because this round registers a finding (§3 item 23), and C1 is also
   where the repair lands, so the plan is correct on disk before the
   finding describing its defect is written. The push runs after C3.
   To correct a landed commit, do NOT add one outside this sequence —
   declare it, and give any such commit its own `## Commits` row and
   its own item-status row (R-0675).
4. Never amend, rebase, cherry-pick, force-push or rewrite history;
   never delete a branch; never merge; create no pull request.
5. `git status --porcelain` prints 0 lines after every commit. Read
   `.agent/STOP` from disk before C0a and again before C3; if present,
   finish the commit in hand, write the handback and stop. NEVER
   delete that sentinel (R-0347).
6. The slices this block carries are the whole text PLANF031R13 and
   the appended text LEDGER13. This paragraph names them and states no
   count; G3 orders you to report the count YOUR extractor measured.
7. THE ONE APPEND'S SHAPE IS STATED ONCE, HERE, WITH EVERY GATE NAMING
   THIS PARAGRAPH RATHER THAN RESTATING IT. Under the newline-INCLUDED
   convention the slice already ends in a newline, so the target is
   EXACTLY: its base blob, then one newline, then the slice. LEDGER13
   goes to `.agent/live_review.md` at C2, which receives NOTHING ELSE
   in that commit (R-0657). Nothing follows it, and the file ends in
   exactly one newline because the slice carries it. THIS BLOCK
   CARRIES NO FROM/TO PAIR, so no containment reading is owed.
8. THIS ROUND MINTS EXACTLY ONE FINDING ID, `R-0680`, and writes no
   `Recurrence:` line and no `Done:` line. `^- R-\d+ — ` must be 240
   before and 241 after, the maximum must move from `R-0679` to
   `R-0680`, `^Done: R-` must be 2 before and 2 after, and
   `^Recurrence: R-` 15 before and 15 after. The §3 item 10 open set
   therefore moves 238 to 239: R-0680's fix lands at C1 of this same
   round, and this ledger's convention records an applied fix in the
   finding's own FIX paragraph rather than by a `Done:` line, which
   only reviewer-authored text at a LATER gate may add.
9. Touch nothing under `packages/`, `apps/`, `tests/` or `docs/`. Do
   not touch `.agent/decisions.md`, `.agent/context.md`,
   `.agent/f031_inventory.md` or `.agent/f031_ui_inventory.md` —
   landed evidence is corrected by dating in a later round, never by
   editing (§3 item 20). This round rules no DECISION.
10. `docs/roadmap/ROADMAP.md` and `docs/roadmap/STATUS.md` are NOT
    touched: AGENTS.md forbids the first absent an explicit operator
    request, and this round claims and closes nothing. Because no
    `docs/roadmap/**` path is in the change set, the §3 docs-round
    gate is not earned and is not ordered.
11. Destructive verification runs ONLY in a disposable `git worktree`
    under `.remedy-wt/`, removed BY ITS EXACT PATH (R-0662) and before
    the G9 suites. Everything already under `.remedy-wt/` is
    pre-existing scratch belonging to no commit, this block's own file
    included: create no worktree at an existing path there, and delete
    nothing you did not create.

── Authored slices ───────────────────────────────────────────

<<<SLICE PLANF031R13
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
R13 records the R12 verdict and registers R-0680, a reviewer defect this round
repairs: the R12 plan rewrite dropped the seed-key warning below and it survived
nowhere else. T002a's tested layer is SHIPPED — `decisionCard.ts` with 27 cases
beside it, red-proofed against a mutation making it branch on a decision's type.

## Next Steps
1. Project the model into a `.tsx` card built from the shipped
   `RightLivePanel.module.css` shell per DECISION F031 D4, mounted in
   `RightLivePanel`, carrying no branching of its own — every decision it makes
   must first exist in `decisionCard.ts`.
2. T002b adds ordering over age and blocked size, filtering, and the badge,
   where DECISION F031 D2 binds: the badge re-derives on refetch over the
   existing SSE stream, no new event kind ships, and D2's two constant-zero
   counters get replaced.
3. T003 wires answering through the write channel, and rules there whether
   `NeedsAttentionCard`'s decision branch is retired, which D4 leaves open.

## Risks
- THE SEED-KEY COLLISION, restored here as the repair R-0680 names and never to
  be dropped again while it stands: `.agent/live_review.md` holds `Gate: R19` as
  a seed entry inherited from F022, so if F031 reaches its own R19 that key
  collides — the §3 item 26 defect. A round before then renames the seed or the
  scheme. F031 is at R13, so seven rounds remain.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 239 once C2 lands, from 238 at `13306809`.
- The findings THIS FEATURE MUST STILL ACT ON are R-0403, R-0413, R-0431,
  R-0445, R-0471, R-0495, R-0533, R-0574, R-0601, R-0622, R-0625, R-0632,
  R-0672, R-0674, R-0675, R-0676, R-0677, R-0678, R-0679 and R-0680; R-0495 and
  R-0574 are the two Highs.
- R-0622 is live ground: eslint parses no TypeScript here and `npm run lint`
  exits 1 at 80 problems, so `typecheck` is the only static reader that works.
- The rendered markup is reached by NO test until a DOM harness lands, which
  DECISION F031 D5 rules its own feature. Every branch therefore stays in the
  pure model; one migrating into a `.tsx` leaves the tested region.
<<<END PLANF031R13

<<<SLICE LEDGER13
Gate: R12 — the F031 R12 entry. R12 PASSED ON EVERY ONE OF ITS TWELVE GATES, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk rather than reading the handback back; every value that handback states reproduced exactly. THIS IS THE FEATURE'S FIRST PRODUCTION-CODE ROUND UNDER THE SPEC FORM, so the reviewer READ THE SHIPPED CODE rather than resting on the gates, because a green gate is not a working feature. `apps/ui/src/api/decisionCard.ts` is 194 lines and implements every clause of the block's S1 through S9: `decisionAgeLabel` returns `unknown age` for a null or non-finite age and otherwise the largest whole unit with the boundaries at 60, 3600 and 86400 and a negative clamped to 0; `decisionBlockedLabel` carries the singular; `decisionAnswers` tries `payload.options`, then `next_actions`, then a single `free_text` affordance, narrowing each at runtime so a missing, null or non-array value falls through rather than throwing; `buildDecisionCardModel` is total by construction with a fallback on every field; and `decisionCardModels` imposes NO ordering, which is the property that keeps T002b's rule visible. The module's header documents its own deliberate absences in this repository's idiom — no per-type form registry, no type-to-widget map, no `switch` over a decision type — which is what AGENTS.md's discoverability conventions ask of code a reader will search for and not find. THE RED PROOF IS THE REVIEWER'S OWN, RE-RUN INDEPENDENTLY IN A DISPOSABLE WORKTREE IT THEN REMOVED BY EXACT PATH: with `decisionAnswers` mutated to return the empty array when the type equals `warp_core_alignment` — a branch on `card.type`, which is precisely what the architecture line forbids — the suite exits 1 with EXACTLY TWO failing tests, `decisionAnswers > renders a NOVEL decision type generically, from its payload alone` and `decisionAnswers > gives two cards that differ ONLY in type identical answers`, against an unmutated control at the SAME root of 303 passed and 0 failed. The tests therefore reach the property rather than merely asserting near it. THE RANGE HELD: `8b4e2295`..`13306809` is SIX commits, every one single-parent and correctly chained, the path set EQUAL to the block's seven-path change set with both differences EMPTY, and per-commit insertions from `git diff --numstat` of 450, 331, 17, 2, 420 and 81 — each under the 500 cap and each equal cell for cell to the `## Commits` table the handback carries. TRANSPORT HELD IN ITS STRONGEST FORM: the reviewer's own emitted `.remedy-wt/f031-r12.md`, the committed C0a blob, the committed C0b blob and `.agent/last_block.md` off disk are ALL FOUR byte-identical at sha256 `31c83344a8fab82fa57a8a34cbd2deacd57fa8447a9cb97d22b75b0b77ec1071` over 32697 bytes and 450 lines, C0a and C0b resolving to the SAME git blob. THE SLICES APPLIED BYTE FOR BYTE: `.agent/plan.md` at `f94ca4f5` equals PLANF031R12 exactly at 2918 bytes and 49 lines with the trailing-newline-removed control FALSE; and the ledger append equals its base blob plus one newline plus LEDGER12 EXACTLY, 582367 + 1 + 6165 = 588533, with an independent blank-line split going 287 to 288 units at N=1 and the last unit equal to the slice's paragraph — nine numbers the reviewer had PREDICTED from its own dry run before delegating, every one reproduced. THE SETS MOVED ONLY WHERE CONSTRAINT 9 ALLOWED: `^- R-\d+ — ` 240 to 240 all DISTINCT with ids ADDED and REMOVED both EMPTY, maximum `R-0679` unchanged, `^Done: R-` 2 to 2, `^Recurrence: R-` 15 to 15, and `^Gate: R\d+ — ` 11 to 12 gaining EXACTLY the key `R11`, all twelve DISTINCT. THE TWO FILES ARE GENUINELY NEW: `git ls-tree` at the base prints NOTHING for either, both are present at `8df27c6e` at 194 and 226 lines, and the range names no other path under `apps/`. THE TOOLCHAIN READINGS ARE THE REVIEWER'S OWN, taken in the primary checkout: `npm run test:unit` exit 0 at 21 files and 312 tests against the base's 20 and 285, so this round contributes one file and 27 cases; `npm run typecheck` exit 0 with ZERO diagnostics. NO LINT GATE WAS ORDERED OR RUN, and that was correct: measured at this round's base, `npm run lint` exits 1 with 80 problems and `npx eslint` fails on the UNTOUCHED `src/api/recency.ts` with `Parsing error: Unexpected token type`, so eslint parses no TypeScript in this repository at all — the defect finding R-0622 already records and which this round's base measurement confirms as live ground rather than history. THE FIVE PYTHON SUITES ARE THE REVIEWER'S OWN, run SERIALLY with never two pytest processes alive, every one a REAL exit 0 at `tests/ui_server/` 474, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16 and `test_golden_path` 42 — identical to the base readings. HYGIENE HELD: markers line-anchored 0 in all four targets, `git ls-files .remedy-wt` 0, the zip glob 0, `git worktree list` 1 line, `git status --porcelain` 0, and the reflog read by OPERATION PREFIX shows amend 0, rebase 0 and cherry 0. THE PUSH DISCHARGED: measured against `git ls-remote`, the local and remote tips are both `13306809da092eef995061b5809dd70e5a93f505`; `gh pr list --state open` is EMPTY and nothing was merged. THE NUMBERS §3 ITEM 31 RULES NO ARTEFACT OF R12 COULD CARRY: the handback commit `13306809` is 81 insertions and 74 deletions and single-parent, and the file it writes is 100 lines, exactly the tier its constraint 4 earns. THE NINE DECLARED ITEMS WERE EACH INSPECTED AND EACH IS SOUND, and two deserve naming. FIRST, the worktree the red proof ran in has no `node_modules`, so `promptTraceLens.test.ts` cannot COLLECT there and the worktree total is 303 rather than the primary's 312; the worker isolated that by running an unmutated control at the SAME root before the mutant, which is the only method that makes the mutant's effect attributable, and the reviewer reproduced both halves. SECOND, the item-status `push` row reads `done` with the outcome routed to this entry, which is the correction this reviewer owed after R11's row read `deviated` for a step that had in fact discharged. R12 EARNS NO FINDING. The one defect this round surfaces belongs to the REVIEWER and is registered immediately below as R-0680; the R12 worker found it, declared it, and correctly declined to repair it. THE VERDICT IS PASS.

- R-0680 — Medium, REVIEWER-SLICE DEFECT, A WHOLE-FILE PLAN REWRITE SILENTLY DROPPED THE ONLY CARRIER OF A STANDING FORWARD-LOOKING WARNING. Found by the R12 WORKER while applying the reviewer's own PLANF031R12 slice, declared in its report, and confirmed by the reviewer by searching the repository before minting this id. THE INSTANCE: the R11 plan, at `8b4e2295`, closes its `## Risks` section with a bullet reading that the record holds `Gate: R19` from F022 as its seed entry, that if F031 reaches its own R19 that key collides — the §3 item 26 defect — and that a round before then renames the seed or the scheme. PLANF031R12 replaced `.agent/plan.md` as a WHOLE FILE and did not carry that bullet, substituting two new risk bullets in its place. MEASURED AT `13306809`, and this is what makes it Medium rather than Low: the string `R19` occurs 0 times in `.agent/plan.md`, and no paragraph of `.agent/live_review.md` or `.agent/decisions.md` records the collision risk — the reviewer searched both files for `R19` in context and for the words `collide` and `collision` and found no carrier — so the warning did not move, it ended. A whole-file replacement is a delete of everything it does not repeat, and the file it deleted from is the one AGENTS.md's Session Resume tells the next session to read SECOND, ahead of the review record. The cost is not hypothetical: F031 is at R13, seven rounds from the collision, and the next reviewer to write `Gate: R19` would duplicate a key this ledger already holds, which is the §3 item 26 defect R-0587 registers and which R11 was renumbered specifically to avoid. This is the class `.agent/context.md` already names as standing — a rewrite deletes rules that bind the next round — arriving in `.agent/plan.md`, where nothing had written it down. It is a REVIEWER defect end to end: the worker applied the slice byte for byte exactly as constraint 1 requires, surfaced the loss in its report, and correctly did not substitute text of its own for an authored slice. FIX, APPLIED BY THIS ROUND'S C1: PLANF031R13 restores the warning as the FIRST bullet of `## Risks`, states the round count remaining, and marks it as never to be dropped again while it stands. STANDING RULE FROM HERE, BINDING THE REVIEWER: before emitting any WHOLE-FILE replacement of a `.agent/` state file, diff the authored slice against the file it replaces and account for every bullet, constraint and warning the base carries and the slice does not — carry it forward, or state in the block WHY it is being retired and where it now lives. Item 20 of the §3 checklist governs a slice that states a fact about a file the same block edits; nothing in that list governs what a replacement OMITS, which is why this recurs and why the check is written as an omission diff rather than as a reading of the new text.
<<<END LEDGER13

── Done when ─────────────────────────────────────────────────
Run every gate yourself, record its REAL exit code and REAL output,
and report ONE LINE PER GATE in the handback, transcripts kept out of
it (R-0582). "Green" as a word is a finding. Every gate below runs at
a commit STRICTLY EARLIER than C3 (§3 item 31); G10 runs after it and
names its own carrier.

G1  Branch and cleanliness. `git branch --show-current` prints
    `feature/f031-decision-inbox` and NOT `main`. `.agent/STOP` read
    from disk is ABSENT before C0a and again before C3. Report
    `git status --porcelain` line count after each of C0a, C0b, C1 and
    C2; each must be 0.

G2  Transport. Report sha256, byte count and line count for FOUR
    readings: `.remedy-wt/f031-r13.md` before C0a, the committed C0a
    blob, the committed C0b blob, and `.agent/last_block.md` off disk
    after C0b. All four must be EQUAL. Report the git blob id of C0a's
    and C0b's file; they must be the SAME id.

G3  Extraction. Run your extractor over the COMMITTED C0a blob and
    report the slice count, the CONTENT lines inside markers, and the
    TOTAL line count. Report the numbers YOUR extractor printed.

G4  The plan, and THE REPAIR. `.agent/plan.md` at C1 is byte-equal to
    PLANF031R13 under your stated newline convention; report slice
    length, file length and convention. NEGATIVE CONTROL: NOT
    byte-equal to that slice with its trailing newline REMOVED.
    `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` STRICTLY under 50.
    THE REPAIR IS MEASURED, NOT ASSUMED: report that the string `R19`
    occurs 0 times in `.agent/plan.md` at the BASE and more than 0
    times at C1, and quote the count at C1 that YOU measured.

G5  The append, as ONE equality over the whole file, in the shape
    constraint 7 states — name that paragraph, do not restate its
    formula. Report the boolean and the byte arithmetic against the
    base's 588533. Report a SECOND, INDEPENDENT reading: split the
    committed file on blank lines, take the LAST N units, and confirm
    they equal LEDGER13's N paragraphs IN ORDER, where N is the number
    YOUR split measured and not one stated here (R-0631). Give the
    unit count before and after. NEGATIVE CONTROL: flip ONE byte
    inside the FIRST paragraph the append added; BOTH readers must
    reject the mutant and BOTH accept the true file. Write any mutant
    only under a disposable worktree per constraint 11.

G6  The sets, base versus C2 in `.agent/live_review.md`:
    `^- R-\d+ — ` 240 → 241, all DISTINCT, the ids ADDED being exactly
    `R-0680` and the ids REMOVED the EMPTY SET, maximum `R-0679` →
    `R-0680`. `^Done: R-` 2 → 2 and `^Recurrence: R-` 15 → 15, both
    UNCHANGED. `^Gate: R\d+ — ` 12 → 13, gaining exactly the key
    `R12`, with `R19` and `R1` through `R11` still present, and all 13
    keys DISTINCT (§3 item 26). Report the §3 item 10 open set at C2 —
    paragraphs minus `Done:` lines — which must be 239.

G7  Markers, paths, structure and hygiene. Line-anchored `^<<<SLICE `
    and `^<<<END ` both count 0 in `.agent/plan.md` at C1 and
    `.agent/live_review.md` at C2. Report that
    `git diff --name-only <base>..C2` names NO path under `packages/`,
    `apps/`, `tests/` or `docs/`, and neither `.agent/decisions.md`
    nor `.agent/context.md` nor either inventory file. Over C0a..C2
    report per commit that it is single-parent and its INSERTION count
    — the `+` column only, per AGENTS.md DECISION F104 D1 — each under
    500. Those same numbers fill the `+/-` column of the `## Commits`
    table the handback template mandates: derive that column from
    `git diff --numstat` and NOT from the files' before/after line
    counts, and report that the table and this gate agree cell for
    cell (§3 item 28). Report the range path set MINUS the change set
    (EMPTY) and the change set MINUS the range (exactly
    `.agent/handoff.md`, which C3 writes). Report
    `git ls-files .remedy-wt` as 0 and `git ls-files` over `*.zip` as
    0. FOR THE REFLOG, state the SCOPE and the FIELD in the reading
    itself: over THIS ROUND'S entries only, read by the OPERATION
    PREFIX before the first colon of `git reflog --format=%gs`, report
    `amend`, `rebase` and `cherry` each 0, and how many entries you
    scoped to.

G8  THE CODE THIS ROUND DOES NOT TOUCH IS STILL GREEN. Report
    `npm run test:unit` in `apps/ui` with its REAL exit code, file
    count and test count; the base is 21 files and 312 tests and this
    round adds no test, so an unchanged reading is the expected one and
    any change is a finding. Report `npm run typecheck` in `apps/ui`,
    which must be exit 0. NO LINT GATE IS ORDERED; do not run one.

G9  The block's own object ids, and the Python suites. Extract every
    SHA-shaped token from the COMMITTED C0a blob with the word-bounded
    pattern `[0-9a-f]{7,40}` — whose boundaries do NOT match the
    64-char sha256 digests this block also carries — and pass each to
    `git cat-file -t`. THE FAILING SET MUST BE EMPTY: this block
    quotes no non-existent id, so it has no positive control. Report
    the token count YOUR extractor measured, the failing set, and the
    type per token. Then, with `git worktree list` reported as 1 line
    immediately BEFORE the first pytest command, run these SERIALLY in
    the PRIMARY checkout at the C2 tree, never two at once, all
    exit 0:
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/cli/test_golden_path.py -q
    These are the four state readers a round rewriting `.agent/` state
    gates, plus the canary. The reviewer executed all five at the base
    `13306809` with these exact command lines and no extra flag, and
    measured in that order 474, 52, 21, 16 and 42, every one exit 0.
    Account for any difference.

G10 The push. AFTER C3, run
    `git push origin feature/f031-decision-inbox`. No `--force`, no
    `--force-with-lease`, no history rewrite, no branch deletion, no
    pull request. THIS GATE'S OUTCOME IS NOT A VALUE OF ANY FILE THIS
    ROUND WRITES, and its carrier is named here so you inherit ONE
    instruction rather than two: the reviewer measures the pushed tips
    at the next gate and records them in the R13 entry of
    `.agent/live_review.md`. In `## External actions` write the push
    COMMAND and that sentence. In the item-status table the push row's
    status is `done` with the reason "ordered after C3; outcome
    carried by G10 to the reviewer" — it is NOT `deviated`, because
    the step is performed exactly as ordered and only its OUTCOME
    lands elsewhere. Report the real outcome in your final message.

── Handback ──────────────────────────────────────────────────
Rewrite `.agent/handoff.md` at C3 per docs/agents/handback_template.md:
feature and round, branch, base and commit SHAs, a changed-files table
per commit, the item-status table covering C0a, C0b, C1, C2, C3 and
the push, ONE LINE PER GATE with its real result, the finding counts,
and the next expected action. Carry the `Fortschritt:` block above
VERBATIM — count its lines yourself; no numeral is stated here.

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
Gate — report that `gh pr list --state open` is EMPTY and that no pull
request exists for this branch, so none is merged and none is created
yet); that the R13 verdict is UNRECORDED and is owed by the next
round's ledger commit, which by DECISION F085 D9 no artefact of this
round can carry; and that the next build step projects the shipped
`decisionCard.ts` model into a `.tsx` card per DECISION F031 D4,
mounted in `RightLivePanel`, with no branching of its own.

Declare every deviation, contradiction and assumption.
──────────────────────────────────────────────────────────────

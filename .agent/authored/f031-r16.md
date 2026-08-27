── STEP R16 — F031 Decision inbox ────────────────────────────
Goal:        Record the R15 verdict and REGISTER a reviewer defect the
             R15 gate found: the spec named the new component with an
             identifier `decisionCard.ts` already exports for a
             different concept. This is the SESSION'S LAST ROUND and
             it ships NO code — the fix is ordered as the next
             session's first build step, and the finding persists here
             so a session boundary cannot lose it.

Fortschritt: ~55 % (F031 claimed; R1 through R15 landed and gated ·
             T001 SHIPPED · T002a MODEL shipped, wired and RENDERED ·
             T002b ordering/filtering/badge und T003 offen)
             — Schaetzung

Bundle:      C0a save this block · C0b mirror it into last_block · C1
             the plan · C2 the R15 gate entry and the new finding ·
             C3 handback.

Change set:  exactly these paths, nothing else —
             .agent/authored/f031-r16.md                       (C0a)
             .agent/last_block.md                              (C0b)
             .agent/plan.md                                    (C1)
             .agent/live_review.md                             (C2)
             .agent/handoff.md                                 (C3)
             This list bounds the round's WRITES, not its ACTIONS:
             the push named in G10 is ordered explicitly and is not a
             file (R-0674).

── Base ──────────────────────────────────────────────────────
The round base is `4fc7dc77c37bc0a8ef158cdd34b02009a52fbc0f`, the R15
handback commit and the tip of `feature/f031-decision-inbox`, local
and remote equal — the reviewer measured both with `git ls-remote`.
Stay on that branch; create none, never commit to `main`. Every
SHA-shaped token here was passed to `git cat-file -t` before emission
and every one RESOLVES; the types are NOT all `commit` and G9 does not
ask them to be.

Readings the reviewer MEASURED at that base, re-checkable there:
- `.agent/live_review.md`: 611720 bytes, 1215 lines, 294 blank-line
  units; `^- R-\d+ — ` 241 all DISTINCT, maximum `R-0680`;
  `^Done: R-\d+ — ` 3, so the §3 item 10 open set — the first
  pattern's paragraphs minus the second's lines — is 238;
  `^Recurrence: R-` 16; `^Gate: R\d+ — ` 15, the keys `R19` and `R1`
  through `R15` minus `R15` itself, which this round adds.
- `.agent/plan.md` 49 lines, 2894 bytes. `.agent/handoff.md` 94
  lines. `.agent/decisions.md` UNTOUCHED this round.
- `apps/ui`: `npm run test:unit` exit 0 at 21 files and 316 tests;
  `npm run typecheck` exit 0 with zero diagnostics.
- THE DEFECT, measured at that base: the identifier
  `DecisionInboxCard` is exported TWICE in this repository — as an
  `interface` at `apps/ui/src/api/decisionCard.ts` line 58, and as the
  React component at
  `apps/ui/src/components/panels/DecisionInboxCard.tsx`. The interface
  has 3 further use sites in `decisionCard.ts` and is imported by
  `decisionCard.test.ts`.

── Why this round exists ─────────────────────────────────────
R15 rendered the decision inbox and its verdict is owed by THIS
round's ledger commit, which by DECISION F085 D9 no artefact of R15
could carry.

THE ROUND ALSO REGISTERS A DEFECT OF THE REVIEWER'S OWN, found while
gating R15. Section 5 of the R15 block ordered the component be called
`DecisionInboxCard`, and `apps/ui/src/api/decisionCard.ts` already
exported an interface of that exact name — for ONE raw endpoint entry,
where the component renders the WHOLE inbox. The worker applied the
spec exactly as constraint 1 requires. AGENTS.md's Code
Discoverability Conventions state that a name must grep to its own
definition and real usages only, and one spelling serves one concept
repo-wide; this breaks both, in code that section is explicitly
forward-looking about.

THIS IS THE LAST ROUND OF THE SESSION AND IT SHIPS NO CODE. §4.4 of
docs/agents/planner_reviewer_prompt.md puts the finding's persistence
FIRST precisely so a session that ends cannot lose it, and the rename
is ordered as the next session's first build step instead of being
rushed against a session boundary. A rename touching a red-proofed
module with 27 tests beside it deserves its own gated round.

── Constraints ───────────────────────────────────────────────
1. Apply every authored slice BYTE FOR BYTE. Never retype, rewrap or
   "fix" one. If a slice looks wrong, apply it verbatim and DECLARE
   the disagreement in the handback: a contradiction inside this block
   is the reviewer's defect, not yours.
2. Slice transport. This block is saved verbatim as
   `.agent/authored/f031-r16.md` at C0a and mirrored byte-identically
   into `.agent/last_block.md` at C0b. Extract every slice
   PROGRAMMATICALLY out of the COMMITTED C0a blob by its marker LINES
   — `<<<SLICE <NAME>` opens, `<<<END <NAME>` closes. Marker lines
   never reach a target file.
3. Commit sequence, exactly: C0a, C0b, C1, C2, C3. No extra commit,
   none dropped, no reordering. C1 is the FIRST substantive commit
   because this round registers a finding (§3 item 23). To correct a
   landed commit, do NOT add one outside this sequence — declare it,
   and give any such commit its own `## Commits` row and its own
   item-status row (R-0675).
4. Never amend, rebase, cherry-pick, force-push or rewrite history;
   never delete a branch; never merge; create no pull request.
5. `git status --porcelain` prints 0 lines after every commit. Read
   `.agent/STOP` from disk before C0a and again before C3; if present,
   finish the commit in hand, write the handback and stop. NEVER
   delete that sentinel (R-0347).
6. The slices this block carries are the whole text PLANF031R16 and
   the appended text LEDGER16. This paragraph names them and states no
   count; G3 orders you to report the count YOUR extractor measured.
7. THE ONE APPEND'S SHAPE IS STATED ONCE, HERE, WITH EVERY GATE NAMING
   THIS PARAGRAPH RATHER THAN RESTATING IT. Under the newline-INCLUDED
   convention the slice already ends in a newline, so the target is
   EXACTLY: its base blob, then one newline, then the slice. LEDGER16
   goes to `.agent/live_review.md` at C2, which receives NOTHING ELSE
   in that commit (R-0657). Nothing follows it, and the file ends in
   exactly one newline because the slice carries it. THIS BLOCK
   CARRIES NO FROM/TO PAIR, so no containment reading is owed.
8. THIS ROUND MINTS EXACTLY ONE FINDING ID, `R-0681`, and writes no
   `Done:` line and no `Recurrence:` line. `^- R-\d+ — ` must be 241
   before and 242 after, the maximum must move from `R-0680` to
   `R-0681`, `^Done: R-` must be 3 before and 3 after, and
   `^Recurrence: R-` 16 before and 16 after. The §3 item 10 open set
   therefore moves 238 to 239. The reviewer searched the open set for
   the DEFECT before minting the id (§3 item 30) — for a name that
   greps to two definitions, for the discoverability convention, and
   for the words collide and shadow — and no open finding holds it.
9. TOUCH NO CODE. Nothing under `packages/`, `apps/`, `tests/` or
   `docs/` is edited, and that includes the rename this round's
   finding orders — it belongs to the next session's first build
   round. Do not touch `.agent/decisions.md`, `.agent/context.md`,
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
12. `npm run lint` is NOT ordered and is not run: finding R-0622
    records that eslint parses no TypeScript here.

── Authored slices ───────────────────────────────────────────

<<<SLICE PLANF031R16
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
R16 records the R15 verdict and registers R-0681, a reviewer defect found at the
R15 gate: the spec named the component `DecisionInboxCard`, which
`apps/ui/src/api/decisionCard.ts` already exports as an interface. No code ships.

## Next Steps
1. REPAIR R-0681 FIRST, before new feature work: rename the INTERFACE in
   `apps/ui/src/api/decisionCard.ts` to name one endpoint ENTRY, carrying its
   three use sites and its `decisionCard.test.ts` import, and leave the
   component alone. Gate on `typecheck` and the unchanged 21 files, 316 tests.
2. T002b adds ordering over age and blocked size, filtering, and the badge,
   where DECISION F031 D2 binds: the badge re-derives on refetch over the
   existing SSE stream, no new event kind ships, and D2's two constant-zero
   counters get replaced.
3. T003 wires answering through the write channel — the card's answer buttons
   ship DISABLED until it lands — and rules there whether
   `NeedsAttentionCard`'s decision branch is retired, which D4 leaves open.

## Risks
- THE SEED-KEY COLLISION, carried forward and never to be dropped while it
  stands: `.agent/live_review.md` holds `Gate: R19` as a seed entry inherited
  from F022, so if F031 reaches its own R19 that key collides — the §3 item 26
  defect. A round before then renames the seed or the scheme. F031 is at R16,
  so four rounds remain, and this is now the nearer deadline of the two.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 239 once C2 lands, from 238 at `4fc7dc77`.
- The findings THIS FEATURE MUST STILL ACT ON are R-0403, R-0413, R-0431,
  R-0441, R-0445, R-0471, R-0495, R-0533, R-0574, R-0601, R-0622, R-0625,
  R-0632, R-0672, R-0674, R-0675, R-0676, R-0677, R-0678, R-0679 and R-0681;
  R-0495 and R-0574 are the two Highs. This bullet states no count of that list.
- R-0622 is live ground: eslint parses no TypeScript here and `npm run lint`
  exits 1 at 80 problems, so `typecheck` is the only static reader that works.
- THE SHIPPED MARKUP IS REACHED BY NO TEST, which DECISION F031 D5 rules its own
  feature, and R15's own probe measured it: deleting the mount turns nothing
  red. Every branch therefore stays in `decisionCard.ts`.
<<<END PLANF031R16

<<<SLICE LEDGER16
Gate: R15 — the F031 R15 entry. R15 PASSED ON EVERY ONE OF ITS ELEVEN GATES, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk rather than reading the handback back; every value that handback states reproduced exactly. TRANSPORT HELD IN ITS STRONGEST FORM, cmp-against-scratchpad rather than the digest fallback: the reviewer's own emitted `.remedy-wt/f031-r15.md`, the committed C0a blob, the committed C0b blob and `.agent/last_block.md` off disk are ALL FOUR byte-identical at sha256 `a54c7a0ba757764d1eae510dfdc1680ba8ba8b568609045c7021a463c0ea541f` over 34734 bytes and 451 lines, C0a and C0b resolving to the SAME git blob `dc1cc6863a19439c9a6b3983d87cac7a7a11fd64`. THE EXTRACTION printed 2 slices, 52 content lines and 451 total. THE SLICES APPLIED BYTE FOR BYTE: `.agent/plan.md` at `7add6592` equals PLANF031R16's predecessor PLANF031R15 exactly at 2894 bytes and 49 lines with the trailing-newline-removed control FALSE, `^## Goal$` 1 and `^## Next Steps$` 1; and the ledger append equals its base blob plus one newline plus LEDGER15 EXACTLY, 604055 + 1 + 7664 = 611720 against an actual 611720, corroborated by an independent blank-line split going 292 to 294 units whose last 2 units equal the slice's 2 paragraphs IN ORDER. THE SETS MOVED ONLY WHERE CONSTRAINT 8 ALLOWED: `^- R-\d+ — ` 241 to 241 all DISTINCT, ids ADDED and REMOVED both EMPTY, maximum `R-0680` unchanged, `^Done: R-` 3 to 3, `^Recurrence: R-` 15 to 16 gaining EXACTLY `R-0441`, and `^Gate: R\d+ — ` 14 to 15 gaining EXACTLY the key `R14`, all 15 DISTINCT. THE REVIEWER READ THE SHIPPED CODE rather than resting on the gates. `DecisionInboxCard.tsx` is 64 lines and meets every clause of S1: its ONE guard is emptiness, every string it displays is a FIELD of a model, the answer buttons are `type="button"` and DISABLED with a title naming T003, and the React key pairs position with id so two cards sharing an id still differ. THE ARCHITECTURE LINE HOLDS BY MEASUREMENT, not by assertion: `switch` occurs 0 times and a comparison operator applied to `type` or `status` occurs 0 times, and the module import is `import type`, so the component borrows no logic from the layer it projects. S2 mounts it between `NeedsAttentionCard` and `ActivityFeedCard` exactly as ordered, in a two-line diff that changes nothing else. S3 APPENDS 32 CSS lines carrying 0 hex literals, and the set of `--remedy-*` properties `RightLivePanel.module.css` USES minus those `apps/ui/src/styles/` DEFINES is EMPTY at 24 used against 58 defined — the R-0661 class held open rather than joined. THE TOOLCHAIN READINGS ARE THE REVIEWER'S OWN, taken in the primary checkout: `npm run typecheck` exit 0 with ZERO diagnostics, and `npm run test:unit` exit 0 at 21 files and 316 tests, BOTH UNCHANGED from the base, which is the expected reading for a round DECISION F031 D5 puts outside the collected set. THE FIVE PYTHON SUITES ARE THE REVIEWER'S OWN, run SERIALLY, never two alive at once, every one a REAL exit 0 at `tests/ui_server/` 474, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16 and `test_golden_path` 42. HYGIENE HELD: markers line-anchored 0 in all five targets, the range `4fc7dc77`'s predecessor `e12a4d46`..`58506912` names no path under `packages/`, `tests/` or `docs/` and no `apps/` path beyond the three the block names, `git ls-files .remedy-wt` 0, the zip glob 0, `git worktree list` 1 line, `git status --porcelain` 0, and the reflog read by OPERATION PREFIX over this round's entries shows amend 0, rebase 0 and cherry 0. THE RANGE HELD: `e12a4d46`..`4fc7dc77` is SIX commits, every one single-parent, with per-commit insertions of 451, 238, 20, 4 and 98 for C0a through C3, each under the 500 cap. THE BLOCK'S OWN OBJECT IDS RESOLVE: 19 SHA-shaped tokens, 7 distinct, failing set EMPTY, one `blob` and six `commit`. THE PUSH DISCHARGED — measured with `git ls-remote`, the local tip and `refs/heads/feature/f031-decision-inbox` are both `4fc7dc77c37bc0a8ef158cdd34b02009a52fbc0f`, `gh pr list --state open` is EMPTY, and nothing was created or merged. THE HONEST PROBE IS THE PART WORTH KEEPING. G9 ordered the mount deleted and the result REPORTED rather than a colour predicted, and the worker reported that NOTHING went red: the unmutated control in the same worktree produced the identical single failure, which finding R-0653's resolution names as a worktree artifact. That is the correct and expected reading — DECISION F031 D5 puts this markup outside the collected set — and the round is stronger for recording the limit of its own evidence instead of letting a green gate imply coverage. THE THREE DECLARED ITEMS ARE EACH SOUND: the prop name the spec never fixed, the `## Commits` column taken from `git diff --numstat` at 238/231 rather than from `git commit`'s rewrite-detected 451/444 — which the gate ordered and which the reviewer reproduced — and the typecheck half of G9 declared a LIMIT rather than a colour, because a fresh worktree has no `node_modules` and its control already emits diagnostics. R15 EARNS ONE FINDING, and it belongs to the REVIEWER, not to the round: it is registered immediately below as R-0681. THE VERDICT IS PASS.

- R-0681 — Medium, A REVIEWER SPEC NAMED A NEW COMPONENT WITH AN IDENTIFIER THE MODULE IT PROJECTS ALREADY EXPORTS, SO ONE NAME NOW GREPS TO TWO UNRELATED DEFINITIONS WITH INVERTED CARDINALITY. Raised by the reviewer against its own R15 block while gating that round, and confirmed by grep before minting: the open set was searched for the DEFECT first (§3 item 30) — for a name resolving to two definitions, for the discoverability convention, and for the words collide and shadow — and no open finding holds this class. THE INSTANCE, measured at `4fc7dc77`: `apps/ui/src/api/decisionCard.ts` exports `interface DecisionInboxCard` at line 58, describing ONE entry of the endpoint's `decisions` array, with three further use sites in that file and an `import type` of it in `decisionCard.test.ts`; and `apps/ui/src/components/panels/DecisionInboxCard.tsx` exports `function DecisionInboxCard`, the component rendering the WHOLE inbox. The two are unrelated, and their cardinality is inverted — the singular-sounding interface is the single entry while the same word names the collection. AGENTS.md's Code Discoverability Conventions require that a name grep to its own definition and real usages only and that one spelling serve one concept repo-wide, and that section is explicitly forward-looking, so it binds this code most of all. It is a REVIEWER defect end to end: section 5 of the R15 block ORDERED the component's name, the worker applied the spec exactly as constraint 1 requires, and nothing in the block or its gates could have caught it, because every gate measured the component's own bytes and the name is correct in isolation. Medium rather than Low because nothing fails today and the cost is deferred: `typecheck` is silent, all 316 tests pass, and the collision surfaces when T003 needs both symbols in one module and a reader imports the wrong one. FIX, ORDERED FOR THE NEXT SESSION'S FIRST BUILD ROUND rather than rushed against this session's boundary: rename the INTERFACE to name one endpoint ENTRY, carrying its three use sites and the test import with it, and leave the component alone — `Card` is the idiom every sibling in that panel folder uses, and the interface is the symbol whose name is actually inaccurate. STANDING RULE FROM HERE, BINDING THE REVIEWER: before a spec names any new exported symbol, grep the repository for that identifier and report the result in the block, exactly as §3 item 7 already requires for a string a change ADDS to a file. Item 7 reads the tests that guard a file; nothing in that checklist reads the NAMESPACE a new name lands in, which is why this arrived through a spec that was otherwise measured line by line.
<<<END LEDGER16

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
    readings: `.remedy-wt/f031-r16.md` before C0a, the committed C0a
    blob, the committed C0b blob, and `.agent/last_block.md` off disk
    after C0b. All four must be EQUAL. Report the git blob id of C0a's
    and C0b's file; they must be the SAME id.

G3  Extraction. Run your extractor over the COMMITTED C0a blob and
    report the slice count, the CONTENT lines inside markers, and the
    TOTAL line count. Report the numbers YOUR extractor printed.

G4  The plan. `.agent/plan.md` at C1 is byte-equal to PLANF031R16
    under your stated newline convention; report slice length, file
    length and convention. NEGATIVE CONTROL: NOT byte-equal to that
    slice with its trailing newline REMOVED. `^## Goal$` 1,
    `^## Next Steps$` 1, `wc -l` STRICTLY under 50.

G5  The append, as ONE equality over the whole file, in the shape
    constraint 7 states — name that paragraph, do not restate its
    formula. Report the boolean and the byte arithmetic against the
    base's 611720. Report a SECOND, INDEPENDENT reading: split the
    committed file on blank lines, take the LAST N units, and confirm
    they equal LEDGER16's N paragraphs IN ORDER, where N is the number
    YOUR split measured and not one stated here (R-0631). Give the
    unit count before and after. NEGATIVE CONTROL: flip ONE byte
    inside the FIRST paragraph the append added; BOTH readers must
    reject the mutant and BOTH accept the true file. Write any mutant
    only under a disposable worktree per constraint 11.

G6  The sets, base versus C2 in `.agent/live_review.md`:
    `^- R-\d+ — ` 241 → 242, all DISTINCT, the ids ADDED being exactly
    `R-0681` and the ids REMOVED the EMPTY SET, maximum `R-0680` →
    `R-0681`. `^Done: R-` 3 → 3 and `^Recurrence: R-` 16 → 16, both
    UNCHANGED. `^Gate: R\d+ — ` 15 → 16, gaining exactly the key
    `R15`, with `R19` and `R1` through `R14` still present, and all 16
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
    `git diff --numstat` and NOT from `git commit`'s own summary,
    which applies rewrite detection and reports different figures for
    a full-file rewrite (the R15 declaration), and report that the
    table and this gate agree cell for cell (§3 item 28). Report the
    range path set MINUS the change set (EMPTY) and the change set
    MINUS the range (exactly `.agent/handoff.md`, which C3 writes).
    Report `git ls-files .remedy-wt` as 0 and `git ls-files` over
    `*.zip` as 0. FOR THE REFLOG, state the SCOPE and the FIELD in the
    reading itself: over THIS ROUND'S entries only, read by the
    OPERATION PREFIX before the first colon of
    `git reflog --format=%gs`, report `amend`, `rebase` and `cherry`
    each 0, and how many entries you scoped to.

G8  THE CODE THIS ROUND DOES NOT TOUCH IS STILL GREEN. Report
    `npm run typecheck` in `apps/ui` with its REAL exit code, which
    must be 0 with ZERO diagnostics, and `npm run test:unit` with its
    REAL exit code, file count and test count: both counts must be
    UNCHANGED at the base's 21 and 316, because constraint 9 forbids
    this round any code at all and any movement is a finding. Report
    also that `git diff --name-only <base>..C2` contains no path
    beginning `apps/`, which is the same reading G7 takes and is
    stated here because it is what makes these two counts meaningful.

G9  The block's own object ids, and the Python suites. Extract every
    SHA-shaped token from the COMMITTED C0a blob with the word-bounded
    pattern `[0-9a-f]{7,40}` — whose boundaries do NOT match the
    64-char sha256 digests this block also carries — and pass each to
    `git cat-file -t`. FAILING means the token does NOT RESOLVE, and
    THE FAILING SET MUST BE EMPTY: this block quotes no non-existent
    id, so it has no positive control. THE TYPES ARE NOT ALL `commit`
    AND THE GATE DOES NOT ASK THEM TO BE — LEDGER16 quotes the git
    BLOB id `dc1cc6863a19439c9a6b3983d87cac7a7a11fd64`, which the
    reviewer resolved to type `blob` before emission, and every other
    token resolves to type `commit`. Report the token count YOUR
    extractor measured, the failing set, and the type per token. Then,
    with `git worktree list` reported as 1 line immediately BEFORE the
    first pytest command, run these SERIALLY in the PRIMARY checkout
    at the C2 tree, never two at once, all exit 0:
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/cli/test_golden_path.py -q
    These are the four state readers a round rewriting `.agent/` state
    gates, plus the canary. The reviewer executed all five at the base
    `4fc7dc77` with these exact command lines and no extra flag, and
    measured in that order 474, 52, 21, 16 and 42, every one exit 0.
    Account for any difference.

G10 The push. AFTER C3, run
    `git push origin feature/f031-decision-inbox`. No `--force`, no
    `--force-with-lease`, no history rewrite, no branch deletion, no
    pull request. THIS GATE'S OUTCOME IS NOT A VALUE OF ANY FILE THIS
    ROUND WRITES, and its carrier is named here so you inherit ONE
    instruction rather than two: the reviewer measures the pushed tips
    at the next gate and records them in the R16 entry of
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

THIS IS THE LAST ROUND OF THE WHOLE SESSION, so your `## Next` section
is the next session's first instruction and names, in order: Phase 1
rule 1 (re-read `.agent/STOP` from disk), THEN Phase 1 rule 2 (the
Open PR Gate — report what `gh pr list --state open` printed and
whether any pull request exists for this branch, and note that NO pull
request has ever been opened for it, so the branch carries R1 through
R16 unmerged); that the R16 verdict is UNRECORDED and is owed by the
next round's ledger commit, which by DECISION F085 D9 no artefact of
this round can carry; that the next BUILD round repairs R-0681 by the
rename `## Next Steps` item 1 of the plan describes; and that T002b
follows it under DECISION F031 D2.

Declare every deviation, contradiction and assumption.
──────────────────────────────────────────────────────────────

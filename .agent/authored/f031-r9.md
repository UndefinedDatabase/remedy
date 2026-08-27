── STEP R9 — F031 Decision inbox ─────────────────────────────
Goal:        Record the R8 verdict and carry the pushed tips the R8
             gate deliberately left uncarried, then MEASURE the UI
             ground T002 needs into a new inventory file. State and
             measurement only; no production path is touched and no
             design question is ruled.

Fortschritt: ~27 % (F031 claimed; R1 through R8 landed and gated ·
             T001 SHIPPED — the derivation module, the read endpoint
             and 29 tests are on disk and green · T002 blocked on two
             MEASURED gaps R10 must rule · T003 offen) — Schaetzung

Bundle:      C0a save this block · C0b mirror it into last_block ·
             C1 the plan · C2 the R8 gate entry · C3 the UI
             inventory · C4 the handback.

Change set:  exactly these paths, nothing else —
             .agent/authored/f031-r9.md                        (C0a)
             .agent/last_block.md                              (C0b)
             .agent/plan.md                                    (C1)
             .agent/live_review.md                             (C2)
             .agent/f031_ui_inventory.md                       (C3)
             .agent/handoff.md                                 (C4)
             This list bounds the round's WRITES, not its ACTIONS:
             the push named in G10 is ordered explicitly and is not a
             file (R-0674).

── Base ──────────────────────────────────────────────────────
The round base is `1ec7a33009f15da0f20b95f1baae3f814b4f0c0b`, the R8
handback commit and the current tip of `feature/f031-decision-inbox`.
Every SHA-shaped token in this block was passed to `git cat-file -t`
before emission and every one resolves, so G9 orders that sweep with
an EMPTY failure set and this block declares no positive control.
Stay on that branch; create none, never commit to `main`.

Readings the reviewer MEASURED at that base, re-checkable there:
- `.agent/live_review.md`: 566277 bytes, 1195 lines, 284 blank-line
  units; `^- R-\d+ — ` 240 all DISTINCT, maximum `R-0679`;
  `^Done: R-\d+ — ` 2; `^Recurrence: R-` 15; `^Gate: R\d+ — ` 8,
  the keys `R19`, `R1`, `R2`, `R3`, `R4`, `R5`, `R6` and `R7`.
- The §3 item 10 open set — every `^- R-\d+ — ` paragraph minus
  every `^Done: R-\d+ — ` line — is 240 − 2 = 238 at that commit.
- `.agent/plan.md` 49 lines, 3017 bytes. `.agent/handoff.md` 75
  lines. `.agent/f031_ui_inventory.md` does NOT exist there.

── Why this round exists ─────────────────────────────────────
R8 passed on every one of its nine gates under the reviewer's own
execution. C2 records that verdict and carries the pushed tips,
which by finding R-0679's fix clause have no other carrier: R8's own
G9 ruled that its push outcome is a value of no file R8 writes.

C3 is the round's substance. The plan's Risks name a design gap, and
the reviewer measured a SECOND one while preparing this block: the
shipped UI toolchain collects no component test at all. T002 cannot
be planned against either gap until both are measured per file and
symbol, and a ruling authored over an unmeasured gap is exactly the
improvisation the feature file's CANONICAL DESIGN REFERENCE banner
forbids. This round measures; R10 rules.

── Constraints ───────────────────────────────────────────────
1. Apply every authored slice BYTE FOR BYTE. Never retype, rewrap,
   reflow or "fix" one. If a slice looks wrong, apply it verbatim
   and DECLARE the disagreement in the handback: a contradiction
   inside this block is the reviewer's defect, not yours.
2. Slice transport. This block is saved verbatim as
   `.agent/authored/f031-r9.md` at C0a and mirrored byte-identically
   into `.agent/last_block.md` at C0b. Extract every slice
   PROGRAMMATICALLY out of the COMMITTED C0a blob by its marker
   LINES — `<<<SLICE <NAME>` opens, `<<<END <NAME>` closes. Marker
   lines never reach a target file.
3. Commit sequence, exactly: C0a, C0b, C1, C2, C3, C4. No extra
   commit, none dropped, no reordering. C1 is the FIRST substantive
   commit because this round touches the finding ledger (§3 item
   23). The push runs after C4. To correct a landed commit, do NOT
   add one outside this sequence — declare it (R-0675).
4. Never amend, rebase, cherry-pick, force-push or rewrite history;
   never delete a branch; never merge; create no pull request.
5. `git status --porcelain` prints 0 lines after every commit. Read
   `.agent/STOP` from disk before C0a and again before C4; if
   present, finish the commit in hand, write the handback and stop.
6. The slices this block carries are the whole text PLANF031R9 and
   the ledger paragraph GATE8. This paragraph names them and states
   no count; G3 orders you to report the count YOUR extractor
   measured.
7. C2 appends GATE8 to `.agent/live_review.md`. THE APPEND SHAPE IS
   STATED ONCE, HERE, AND EVERY GATE NAMES THIS PARAGRAPH RATHER
   THAN RESTATING IT. Under the newline-INCLUDED convention the
   slice already ends in a newline, so the file at C2 is EXACTLY:
   the base blob, then one newline, then GATE8. Nothing follows, and
   the file ends in exactly one newline because GATE8 carries it.
   THIS BLOCK CARRIES NO FROM/TO PAIR, so no containment reading is
   owed and none is stated.
8. THIS ROUND MINTS NO FINDING ID and writes no `Recurrence:` line.
   `^- R-\d+ — ` must be 240 before and 240 after, the maximum must
   stay `R-0679`, and `^Recurrence: R-` must be 15 before and 15
   after. R8 earned no finding: every gate reproduced under the
   reviewer's own execution.
9. Touch nothing under `packages/`, `apps/`, `tests/` or `docs/`,
   and not `.agent/decisions.md` or `.agent/f031_inventory.md` —
   landed evidence is corrected by dating in a later round, never by
   editing (§3 item 20). Consequently `tests/docs/` and
   `test_roadmap_index.py` are NOT gated. C3 creates a NEW file and
   never edits the existing inventory.
10. C3 is a MEASUREMENT, not an authored text: no slice carries its
    content, and every value in it is one YOUR command printed. Where
    this block states a reading of its own beside a question, report
    yours and ACCOUNT FOR ANY DIFFERENCE rather than restating the
    reviewer's number.
11. Destructive verification, if any, runs ONLY in a disposable
    `git worktree` under `.remedy-wt/`, removed BY ITS EXACT PATH
    (R-0662) and before the G9 suites. `.remedy-wt/dry`,
    `.remedy-wt/rev-r7` and `.remedy-wt/f031-r8.md` are PRE-EXISTING
    scratch belonging to no round of this feature: do not create a
    worktree at either path, read from them or delete them.

── Authored slices ───────────────────────────────────────────

<<<SLICE PLANF031R9
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the merge
commit of pull request #213 which closed F022. `.agent/live_review.md` is the
record and the finding-id ceiling; `.agent/f031_inventory.md` is the measured
source inventory; `.agent/decisions.md` carries DECISION F031 D1, D2 and D3.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact. DONE when the inbox lists fixture
decisions of every PRODUCING type with correct blocked-size math, answering from
a card round-trips through the write channel into the same effects the CLI
produces, the badge tracks live, and ordering follows a documented rule over age
and blocked size rather than vibes.

## Current Step
R9 records the R8 verdict and MEASURES the UI ground T002 needs into
`.agent/f031_ui_inventory.md`. T001 is SHIPPED: the derivation module, the
`/api/jobs/<job_id>/decisions` route and 29 tests are on disk and green.

## Next Steps
1. R10 rules the two gaps Risks names below, each as a DECISION with
   alternatives and a reversal path, before any card ships.
2. T002a then builds the cards and the GENERIC options renderer — producers own
   the semantics, so no per-type form is hardcoded — with the tests whose shape
   R10's second ruling settles.
3. T002b adds ordering, filtering and the badge, where DECISION F031 D2 binds:
   the badge re-derives on refetch over the existing SSE stream, no new event
   kind ships, and the two constant-zero counters D2 names get replaced.

## Risks
- Open findings, stated with the rule and the commit DECISION F009 D10 requires:
  by §3 item 10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — `
  line — the open set is 238, measured at `1ec7a330`.
- The findings THIS FEATURE MUST STILL ACT ON — a narrower set, named as what it
  is and not called "open" — are R-0403, R-0413, R-0431, R-0445, R-0471, R-0495,
  R-0533, R-0574, R-0601, R-0625, R-0632, R-0672, R-0674, R-0675, R-0676, R-0677,
  R-0678 and R-0679; R-0495 and R-0574 are the two Highs, from F085 and F086.
- THE CANONICAL DESIGN REFERENCE HAS NO INBOX AND NO DECISION COMPONENT, so T002
  has no visual authority and may not improvise one: measured at `1ec7a330`,
  `component_spec.md` names no such component.
- THE SHIPPED UI TOOLCHAIN COLLECTS NO COMPONENT TEST. Measured at `1ec7a330`:
  `apps/ui/vitest.config.ts` sets `environment` to `node` and includes only
  `src/**/*.test.ts`, and `apps/ui/package.json` names no DOM harness — so T002's
  "component tests" is a spec claim R10 rules on, not a plan a round executes.
- The record holds `Gate: R19` from F022 as its seed entry. If F031 reaches its
  own R19 that key collides — the §3 item 26 defect. A round before then renames
  the seed or the scheme; this bullet is the reminder.
<<<END PLANF031R9

<<<SLICE GATE8
Gate: R8 — the F031 R8 entry. R8 PASSED ON EVERY ONE OF ITS NINE GATES, AND THE REVIEWER RE-RAN EVERY EXECUTABLE ONE ITSELF rather than reading the handback's word for any of them; every value that handback states reproduced exactly. THE ROUND WAS STATE ONLY, and its change set held. TRANSPORT HELD: the committed C0a blob, the committed C0b blob and `.agent/last_block.md` as read from disk are ALL sha256 `f3b569635c4e158e8569622372b0c1192799c7e17a5fa0901c59ca64c15728fc` over 22462 bytes and 293 lines, and C0a and C0b resolve to the SAME git blob `ba2a3a9e16f127a3042f6edea319df7558268d12`; the reviewer's own extractor over that blob printed 2 slices, 50 CONTENT lines inside markers and 293 TOTAL lines over 4 marker lines, reproducing the block's own reading. THE PLAN IS BYTE-EXACT: `.agent/plan.md` at `23522837` is 3017 bytes equal to PLANF031R8 under the newline-INCLUDED convention, the trailing-newline-removed control is FALSE, `^## Goal$` and `^## Next Steps$` occur once each, and `wc -l` is 49, strictly under the cap of 50. THE LEDGER APPEND HELD AS ONE EQUALITY OVER THE WHOLE FILE: at `3dbc1ba8` it is EXACTLY the base blob plus one newline plus GATE7, 561117 bytes becoming 566277 with the delta 5160 equal to 1 plus 5159; an independent blank-line split went 283 units to 284 with the LAST equal to GATE7; and the reviewer flipped one byte at offset 561218, inside the appended paragraph, whereupon BOTH readers rejected the mutant and BOTH accepted the true file. THE REVIEWER RAN THAT CONTROL IN MEMORY RATHER THAN IN A DISPOSABLE WORKTREE — a deliberate deviation from the recipe G5 ordered, in the stricter direction, because a mutant that is never written to disk cannot escape into the primary checkout at all. THE SETS MOVED ONLY WHERE CONSTRAINT 8 ALLOWED: `^- R-\d+ — ` 240 to 240 all DISTINCT, ids ADDED and ids REMOVED both the EMPTY SET, maximum `R-0679` unchanged, `^Done: R-` 2 to 2, `^Recurrence: R-` 15 to 15, and `^Gate: R\d+ — ` 7 to 8 gaining exactly the key `R7` with `R19`, `R1`, `R2`, `R3`, `R4`, `R5` and `R6` still present. MARKERS WERE LINE-ANCHORED 0 in both applied targets at their own commits; the four-path range holds nothing under `packages/`, `apps/`, `tests/` or `docs/` and neither `.agent/decisions.md` nor `.agent/f031_inventory.md`; the range path set MINUS the change set is EMPTY and the change set MINUS the range is exactly `.agent/handoff.md`; `git ls-files .remedy-wt` is 0, the zip glob is 0, `git worktree list` is one line and `git status --porcelain` is 0. THE REFLOG READING STATES ITS OWN SCOPE AND FIELD: over this round's five entries, read by the OPERATION PREFIX before the first colon of `git reflog --format=%gs`, every prefix is `commit`, so amend 0, rebase 0 and cherry 0. THE BLOCK'S OWN OBJECT IDS WERE SWEPT: 9 occurrences over 6 distinct word-bounded hex tokens, every one resolving under `git cat-file -t` as five commits and one blob, so the failing set is EMPTY as that block predicted. THE FIVE SUITES ARE THE REVIEWER'S OWN, run SERIALLY in the primary checkout with never two pytest processes alive, every one REAL exit code 0 at `tests/ui_server/` 474, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16 and `test_golden_path` 42 — cell for cell the readings the block ordered, so there is no difference to account for. THE PER-COMMIT INSERTIONS ARE 293, 157, 21 and 2 for C0a through C2, each single-parent and each under the 500 cap, AND THE HANDBACK COMMIT `1ec7a330` IS ITSELF 38 INSERTIONS AND SINGLE-PARENT — the number §3 item 31 rules no artefact of that round could carry, recorded here because this entry is the first place that can hold it. THE PUSH DISCHARGED, AND THIS SENTENCE IS THE CARRIER FINDING R-0679'S FIX CLAUSE NAMES: measured by the reviewer against `git ls-remote`, the local and remote tips of `feature/f031-decision-inbox` are both `1ec7a33009f15da0f20b95f1baae3f814b4f0c0b`; no pull request exists on that branch, and nothing was merged. THE HANDBACK DERIVED ITS OWN CAP rather than quoting one, reading the tier as 60 from the five commits its constraint 3 fixes, landing at 75 lines, and declaring the overage as DECISION D15 requires with the mandated content behind it named — the five per-commit tables, the six-row item-status table and the one-line-per-gate block. THE ONE DECLARED DEVIATION IS SOUND: the `push` row is marked `deviated` because that round's own G9 ruled its outcome a value of no file the round writes, so the row records what the block ORDERED and this entry records what the push DID. THE VERDICT IS PASS.
<<<END GATE8

── The inventory C3 writes ───────────────────────────────────
Create `.agent/f031_ui_inventory.md`, headed
`# F031 UI Inventory — the ground T002 builds on`, then one `## Q<n>`
section per question below, in this order, each answering PER FILE
AND SYMBOL with the command you ran. Answer what you MEASURE; where
this block states the reviewer's own reading, report yours beside it
and account for any difference. Close with `## Observations`.

Q1 — the design authority. Which files under
`docs/ui/design_reference/` name a decision, inbox or queue
component? Report the search you ran over that folder and every hit
with its file and line. The reviewer measured: `component_spec.md`
names no such component, and the only `inbox` string in the folder is
one `ux_spec.md` line placing mobile status/digest/inbox surfaces out
of scope.

Q2 — the shipped tokens. Which `--remedy-*` custom properties are
DEFINED (not merely used) under `apps/ui/src/styles/`? Report the
count and the list. Definitions only: the design reference's own
`tokens.css` is NOT the shipped sheet and is out of this answer.

Q3 — the card shell. Read
`apps/ui/src/components/panels/NeedsAttentionCard.tsx` completely and
report the CSS module it imports, every class name it uses from it,
its root element and the exact `data-ui` attribute value it carries.
Then report which OTHER components import that same module.

Q4 — the test toolchain. Quote VERBATIM from
`apps/ui/vitest.config.ts` the `environment` value and every entry of
`include`. Then report, by the config's own glob, how many test files
exist under `apps/ui/src`, and separately how many files match
`src/**/*.test.tsx`. Then report the number of lines in
`apps/ui/package.json` matching `jsdom`, `happy-dom` or
`testing-library`. The reviewer measured the environment as `node`,
one include glob, 20 files matching it, 0 matching the tsx glob and 0
dependency lines naming a DOM harness.

Q5 — what the shipped tests actually test. Name three of the test
files Q4 counted and, for each, the SYMBOL it imports and asserts on.
State in one sentence what that makes the repository's UI test
strategy — a claim your three examples support.

Q6 — the mount point. Which component composes the cards of the right
panel, in which file, and in what ORDER are its card children
rendered? Name the element and `data-ui` value that wraps them, and
name the component that renders that composer.

Q7 — the overlap. Report every occurrence of the string
`Needs your decision` under `apps/ui/src` with file and line. Then
report whether any file under `apps/ui/src/api/` references the T001
route path `/api/jobs/<job_id>/decisions` in any form. State in one
sentence what the two answers together mean for T002 — that a surface
answering to the inbox's name already ships while its data path does
not.

── Done when ─────────────────────────────────────────────────
Run every gate yourself, record its REAL exit code and REAL output,
and report ONE LINE PER GATE in the handback, transcripts kept out
of it (R-0582). "Green" as a word is a finding. Every gate below runs
at a commit STRICTLY EARLIER than C4, which writes the handback (§3
item 31); G10 runs after it and its carrier is named in G10 itself.

G1  Branch and cleanliness. `git branch --show-current` prints
    `feature/f031-decision-inbox` and NOT `main`. `.agent/STOP` read
    from disk is ABSENT before C0a and again before C4. Report
    `git status --porcelain` line count after each of C0a, C0b, C1,
    C2 and C3; each must be 0.

G2  Transport. Report sha256, byte count and line count for FOUR
    readings: `.remedy-wt/f031-r9.md` before C0a, the committed C0a
    blob, the committed C0b blob, and `.agent/last_block.md` off
    disk after C0b. All four must be EQUAL. Report the git blob id
    of C0a's and C0b's file; they must be the SAME id.

G3  Extraction. Run your extractor over the COMMITTED C0a blob and
    report the slice count, the CONTENT lines inside markers, and
    the TOTAL line count. Report the numbers YOUR extractor printed.

G4  The plan. `.agent/plan.md` at C1 is byte-equal to PLANF031R9
    under your stated newline convention; report slice length, file
    length and convention. NEGATIVE CONTROL: NOT byte-equal to that
    slice with its trailing newline REMOVED. `^## Goal$` 1,
    `^## Next Steps$` 1, `wc -l` STRICTLY under 50.

G5  The ledger append, as ONE equality over the whole file, in the
    shape constraint 7 states — name that paragraph, do not restate
    its formula. Report the boolean and the byte arithmetic against
    the base's 566277. Report a SECOND, INDEPENDENT reading: split
    the C2 file on blank lines and confirm the LAST unit equals
    GATE8, with the unit count before and after. NEGATIVE CONTROL:
    flip ONE byte inside the appended paragraph; BOTH readers must
    reject the mutant and BOTH accept the true file. If you write
    that mutant anywhere, write it only under a disposable worktree
    per constraint 11.

G6  The sets, base versus C2 in `.agent/live_review.md`:
    `^- R-\d+ — ` 240 → 240 all DISTINCT, ids ADDED and ids REMOVED
    both the EMPTY SET, maximum `R-0679` → `R-0679`, `^Done: R-`
    2 → 2, `^Recurrence: R-` 15 → 15 UNCHANGED. `^Gate: R\d+ — `
    8 → 9, gaining exactly the key `R8`, with `R19`, `R1`, `R2`,
    `R3`, `R4`, `R5`, `R6` and `R7` still present.

G7  The inventory. `.agent/f031_ui_inventory.md` exists at C3, and at
    the base it does not — read the base with
    `git ls-tree 1ec7a330 -- .agent/f031_ui_inventory.md`, which must
    print nothing; never write over the tracked file to compare.
    Report its line count, that it carries one `^## Q<n>` heading for
    each question of the section above IN THAT ORDER, and that it
    carries `^## Observations`. Report, for Q4 specifically, every
    quoted value and every count that question asks for, and state
    for each whether it MATCHES the reviewer's reading stated there
    or DIFFERS, with the difference accounted for. A Q section whose
    answer you could not measure says so and names the reason; it
    never guesses.

G8  Markers, paths, structure and hygiene. Line-anchored `^<<<SLICE `
    and `^<<<END ` both count 0 in `.agent/plan.md` at C1, in
    `.agent/live_review.md` at C2 and in `.agent/f031_ui_inventory.md`
    at C3. Report that `git diff --name-only <base>..C3` names NO
    path under `packages/`, `apps/`, `tests/` or `docs/`, and NEITHER
    `.agent/decisions.md` NOR `.agent/f031_inventory.md`. Over
    C0a..C3 report per commit that it is single-parent and its
    INSERTION count — the `+` column only, per AGENTS.md DECISION
    F104 D1 — each under 500. Those same per-commit numbers also fill
    the `+/-` column of the `## Commits` table the handback template
    mandates: derive that column from `git diff --numstat` and NOT
    from the files' before/after line counts, and report that the
    table and this gate agree cell for cell (§3 item 28). Report the
    range path set MINUS the
    change set (EMPTY) and the change set MINUS the range (exactly
    `.agent/handoff.md`, which C4 writes). Report
    `git ls-files .remedy-wt` as 0, `git ls-files` over `*.zip` as
    0, and `git worktree list` as 1 line. FOR THE REFLOG, state the
    SCOPE and the FIELD in the reading itself: over THIS ROUND'S
    entries only, read by the OPERATION PREFIX before the first
    colon of `git reflog --format=%gs`, report `amend`, `rebase` and
    `cherry` each 0, and how many entries you scoped to.

G9  The block's own object ids, and the suites. Extract every
    SHA-shaped token from the COMMITTED C0a blob with the
    word-bounded pattern `[0-9a-f]{7,40}` — whose boundaries do NOT
    match the 64-char sha256 digests this block also carries — and
    pass each to `git cat-file -t`. THE FAILING SET MUST BE EMPTY:
    this block quotes no non-existent id, so it has no positive
    control. Report the token count YOUR extractor measured, the
    failing set, and the type printed for each token. Then, with
    `git worktree list` reported as 1 line immediately BEFORE the
    first pytest command, run these SERIALLY in the PRIMARY checkout
    at the C3 tree, never two pytest processes at once, all exit 0:
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/cli/test_golden_path.py -q
    The reviewer executed all five at `1ec7a330` and measured, in
    that order, 474, 52, 21, 16 and 42, every one exit 0. Report
    yours against those and account for any difference.

G10 The push. AFTER C4, run
    `git push origin feature/f031-decision-inbox`. No `--force`, no
    `--force-with-lease`, no history rewrite, no branch deletion, no
    pull request. THIS GATE'S OUTCOME IS NOT A VALUE OF ANY FILE
    THIS ROUND WRITES, and its carrier is named here so you inherit
    ONE instruction rather than two: the reviewer measures the
    pushed tips at the next gate and records them in the R9 entry of
    `.agent/live_review.md`. In `## External actions` write the push
    COMMAND and that sentence — which is how this block satisfies
    `docs/agents/handback_template.md` and R-0679's fix clause
    together. Report the real outcome in your final message.

── Handback ──────────────────────────────────────────────────
Rewrite `.agent/handoff.md` at C4 per docs/agents/handback_template.md:
feature and round, branch, base and commit SHAs, a changed-files
table per commit, the item-status table covering C0a, C0b, C1, C2,
C3, C4 and the push, ONE LINE PER GATE with its real result, the
finding counts, and the next expected action. Carry the
`Fortschritt:` block above VERBATIM — count its lines yourself and
carry exactly those; this block states no numeral for them.

THE HANDBACK LINE CAP: this block states no cap and no tier. Resolve
it from AGENTS.md under `### handoff.md` against the commit count
constraint 3 fixes, and report BOTH that count and the tier. If the
MANDATED content genuinely does not fit, exceed it and carry a
DECISION D15 "Deviations, declared" line naming your measured count
and the mandated content behind it. Never drop a section to fit. Do
NOT claim compliance with any token cap: that cap was withdrawn.

Any finding count you state carries the RULE that produced it and
the COMMIT it was measured at, in the same sentence, per DECISION
F009 D10. A narrower set is named "the findings this feature must
still act on" and is never called "open" unqualified.

Your `## Next` section names, in order: Phase 1 rule 1 (re-read
`.agent/STOP` from disk), then that NO pull request exists for this
branch and none should be created yet, then that R10 rules the two
measured gaps as DECISIONs with alternatives and a reversal path
before any card ships, and then that R10's first commit also records
the R9 verdict, which by DECISION F085 D9 no artefact of this round
can carry.

Declare every deviation, contradiction and assumption.
──────────────────────────────────────────────────────────────

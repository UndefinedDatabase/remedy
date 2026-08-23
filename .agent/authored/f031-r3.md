── STEP R3 — F031 Decision inbox ─────────────────────────────
Goal:        Record the R2 verdict, then take the decision-inbox
             inventory: what exists in the source today for the queue,
             its CLI, the producers, the blocked-subtree computation,
             the decision event kinds and the write channel — each
             MEASURED by you in the source, never recalled. No
             production code changes.

Fortschritt: ~2 % (F031 claimed; R1 and R2 landed and gated · the
             inventory is this round · no T-slice started) —
             Schaetzung

Bundle:      C0a save this block · C0b mirror it into last_block ·
             C1 the plan · C2 the R2 gate entry · C3 the inventory
             file · C4 the handback.

Change set:  exactly these paths, nothing else —
             .agent/authored/f031-r3.md
             .agent/last_block.md
             .agent/plan.md
             .agent/live_review.md
             .agent/f031_inventory.md
             .agent/handoff.md
             This list bounds the round's WRITES, not its ACTIONS: the
             push named in gate G9 is ordered explicitly and is not a
             file (finding R-0674).

── Base ──────────────────────────────────────────────────────
The round base is `9e773d4afd0da714c5d7423fd8bd4c9c6039bee6`, the C3 of
F031 R2 and the tip of `feature/f031-decision-inbox`, which is also the
remote tip. Stay on that branch; create none, never commit to `main`.

Readings the reviewer MEASURED at `9e773d4a`, re-checkable there:
- `.agent/live_review.md`: `^- R-\d+ — ` 238 all DISTINCT, maximum
  `R-0677`; `^Done: R-\d+ — ` 2; `^Recurrence: R-` 13;
  `^Gate: R\d+ — ` 2, the keys `R19` and `R1`.
- The §3 item 10 open set — every `^- R-\d+ — ` paragraph minus every
  `^Done: R-\d+ — ` line — is 238 − 2 = 236 at that commit.
- `.agent/plan.md` 43 lines. `.agent/f031_inventory.md` does NOT exist.
- These paths all resolve at the base:
  `packages/orchestration/decision_queue.py`,
  `apps/cli/commands/decision.py`,
  `packages/orchestration/dag_schedule.py`,
  `packages/orchestration/ui_server.py`,
  `apps/ui/src/api/humanizeCatalog.ts`,
  `docs/roadmap/features/T5_F031.md`.

── Constraints ───────────────────────────────────────────────
1. Apply every authored slice BYTE FOR BYTE. Never retype, rewrap,
   reflow or "fix" a slice. If a slice looks wrong, apply it verbatim
   and DECLARE the disagreement in the handback. A contradiction inside
   this block is the reviewer's defect, not yours: state it, reconcile
   nothing.
2. Slice transport. This block is saved verbatim as
   `.agent/authored/f031-r3.md` at C0a and mirrored byte-identically
   into `.agent/last_block.md` at C0b. Extract every slice
   PROGRAMMATICALLY out of the COMMITTED C0a blob by its marker LINES —
   a line equal to `<<<SLICE <NAME>` opens it, a line equal to
   `<<<END <NAME>` closes it. Marker lines never reach a target file.
3. Commit sequence, exactly: C0a, C0b, C1, C2, C3, C4. No extra commit,
   none dropped, no reordering. If you must correct a landed commit, do
   NOT add a commit outside this sequence — declare it (R-0675). The
   push runs after C4.
4. Never amend, rebase, cherry-pick, force-push or rewrite history;
   never delete a branch; never merge; create no pull request.
5. `git status --porcelain` prints 0 lines after every commit. Read
   `.agent/STOP` from disk before C0a and again before C4; if present,
   finish the commit in hand, write the handback and stop (G6).
6. The slices this block carries are the whole text PLANF031R3, the
   appended paragraph GATE2, and the inventory scaffold INVENTORY.
   This paragraph names them and states no count of them; G3 orders you
   to report the count YOUR extractor measured.
7. C2 appends GATE2 to `.agent/live_review.md`, separated from the
   preceding text by exactly one blank line, the file ending in exactly
   one newline. This block carries no FROM/TO pair, so no containment
   reading is owed and none is stated.
8. THIS ROUND MINTS NO FINDING ID and changes no finding record.
   `^- R-\d+ — ` must be 238 before and after and the maximum must stay
   `R-0677`. If your inventory uncovers a DEFECT, do NOT mint an id for
   it: record it in the inventory's `## Observations` section as an
   observation with its measurement, and the reviewer rules it next
   round. An inventory round that mints ids is a scope breach.
9. THE INVENTORY IS YOURS TO MEASURE, NOT TO COPY, AND IT IS THE ONE
   SLICE CONSTRAINT 1 DOES NOT BIND WHOLE. The INVENTORY slice is a
   SCAFFOLD: headings and question text, with each answer line left as
   the literal `ANSWER: TO BE MEASURED`. Its STRUCTURE LINES — every
   line that is not an `ANSWER: ` line — are covered by constraint 1
   and land verbatim, in order, unedited. Its ANSWER lines are yours:
   replace each with what YOUR OWN commands printed against the source
   at the base commit. So `.agent/f031_inventory.md` as COMMITTED at C3
   contains no `TO BE MEASURED` token, and G7 proves both halves —
   the structure verbatim, the answers replaced. Committing the
   scaffold unreplaced and fixing it in a later commit would breach
   constraint 3; do the replacement before C3.
   Every answer names the file and the symbol it was read from, and
   every citation is `path` plus a SYMBOL name — never a bare line
   number, which the next edit invalidates (§3 item 9). Where a
   question asks whether something exists and it does not, the answer
   says so explicitly and names the command whose empty output proves
   it; "deliberately does not exist" is a finding-grade fact in this
   repository and is written as one (AGENTS.md, Code Discoverability).
   The reviewer has measured every one of these answers independently
   and will compare; a disagreement is a real signal, so report what
   you measured even where it surprises you.
10. Do not touch any path under `packages/`, `apps/`, `tests/`,
    `docs/` or `README.md`. This round reads production code and writes
    only `.agent/` state. No production behaviour changes.

── Authored slices ───────────────────────────────────────────

<<<SLICE PLANF031R3
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the merge
commit of pull request #213 which closed F022. `.agent/live_review.md` is the
source of truth for the record, the round map and the finding-id ceiling.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the file-based decision queue, live via
decision.requested and decision.resolved events driving the badge, with
branch-only blocking semantics intact. DONE when the inbox lists fixture
decisions of every producing type with correct blocked-size math, answering from
a card round-trips through the write channel into the same effects the CLI
produces, the badge tracks live, and ordering follows a documented rule over age
and blocked size rather than vibes.

## Current Step
R3 records the R2 verdict and takes the decision-inbox inventory into
`.agent/f031_inventory.md`: the queue store and its types, the CLI surface, the
producers, the blocked-subtree computation, the decision event kinds on both
sides, the write-channel command, and what the UI has today — each measured in
the source, no T-slice planned until it is on disk.

## Next Steps
1. R4 records the R3 verdict and rules the tick-shaped questions the inventory
   leaves open — chiefly the event-kind envelope, since the feature file says
   "envelope coordination if not yet present" and the inventory settles which.
2. T001 follows the feature file's Task slicing: the read endpoint, the
   blocked-size computation, scoping, and contract tests per producer type.

## Risks
- Open findings, stated with the rule and the commit DECISION F009 D10 requires:
  by §3 item 10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — `
  line — the open set is 236 measured at `9e773d4a`.
- The findings THIS FEATURE MUST STILL ACT ON — a narrower set, named as what it
  is and not called "open" — are R-0403, R-0413, R-0431, R-0445, R-0495, R-0533,
  R-0574, R-0625, R-0632, R-0672, R-0674, R-0675, R-0676 and R-0677. R-0495 and
  R-0574 are the two Highs, both inherited from the closed F085 and F086.
- F031 depends on F009, F050 and F051. All three are marked `[x]` in
  `docs/roadmap/STATUS.md`, measured at `9e773d4a`; R3's inventory confirms what
  each actually left behind in the source rather than trusting the mark.
- The record holds `Gate: R19` from F022 as its seed entry. If F031 reaches its
  own R19 that key collides — the §3 item 26 defect. A round before then renames
  the seed or the scheme; this bullet is the reminder.
<<<END PLANF031R3

<<<SLICE GATE2
Gate: R2 — the F031 R2 entry. R2 PASSED ON EVERY ONE OF ITS TEN GATES, AND THE REVIEWER RE-RAN EVERY ONE OF THEM ITSELF RATHER THAN READING THE HANDBACK'S WORD FOR ANY OF THEM. THE ROUND'S SUBSTANCE IS THE R1 VERDICT AND TWO RECURRENCES, AND BOTH RECURRENCES ARE THE REVIEWER'S OWN DEFECTS IN TEXT THE REVIEWER AUTHORED — which is the workflow behaving as designed, because the worker caught the first while applying it and the reviewer caught the second while gating it. TRANSPORT HELD IN ITS STRONGEST FORM: the reviewer's own scratch original at `.remedy-wt/f031-r2.md`, the committed C0a blob, the committed C0b blob and `.agent/last_block.md` read off disk are ALL sha256 `aa3ec89faf1e94bced71de1ca99db00e2ce5adf8bf527918c02ff372cf0ff188` over 26090 bytes and 290 lines, and C0a and C0b resolve to the SAME git blob `bdec9eb4`. THE EXTRACTION over the committed C0a blob printed 4 slices across 46 content lines against 290 total, reproducing the worker's own reading. `.agent/plan.md` at `696e18a9` is 2567 bytes and 43 lines, byte-equal to PLANF031R2 with the trailing-newline-removed control FALSE, `^## Goal$` and `^## Next Steps$` once each, strictly under the cap of 50. THE THREE APPENDS LANDED REGION-EXACT UNDER TWO INDEPENDENT READERS AND A CONTROL: the base blob is a byte-exact PREFIX of the C2 file, the byte delta is 9696 against slice lengths 4749, 2517 and 2427 plus three separator newlines, an independent blank-line split went 271 units to 274 with the LAST THREE equal to GATE1, RECUR632 and RECUR676 IN ORDER, and the worker's byte-flip control inside the FIRST appended paragraph was rejected by both readers while both accepted the true file — the reviewer ran its OWN mutant beside it and got the same answer. THE SETS MOVED ONLY WHERE CONSTRAINT 8 ALLOWED, which is the reading this round existed to protect: `^- R-\d+ — ` 238 to 238 with ids ADDED the EMPTY SET and ids REMOVED the EMPTY SET, maximum `R-0677` UNCHANGED, `^Done: R-` 2 to 2, `^Recurrence: R-` 11 to 13 gaining exactly one `R-0632` line and one `R-0676` line, and `^Gate: R\d+ — ` 1 to 2 gaining exactly the key `R1` with `R19` still present. A ROUND THAT REGISTERS TWO DEFECTS WITHOUT MINTING AN ID IS THE POINT OF §3 ITEM 30, and this is the first round in this record to do it deliberately. STRUCTURE HELD: five commits, each single-parent, insertions 290, 218, 19, 6 and 44, each far under the 500 cap and each agreeing cell for cell with the handback's `## Commits` tables under the reviewer's own `git diff --numstat`; the range path set MINUS the change set is EMPTY and the change set MINUS the range is EMPTY once the handback commit is counted; the anchored markers are 0 in both edited files; `git ls-files .remedy-wt` 0 and the zip glob 0; one worktree; `git status --porcelain` 0; amend, rebase and cherry each 0 in the reflog OPERATION field. THE FIVE SUITES ARE THE REVIEWER'S OWN, run serially with never two pytest processes alive, every one exit 0: 470, 52, 21, 16 and 42, cell for cell the base readings. THE PUSH DISCHARGED to `9e773d4a` and the remote tip equals the local tip; no pull request, nothing merged. THE TIER COUNTER-MEASURE WORKED THE FIRST TIME IT WAS TRIED, which is the round's quiet result: the block deliberately stated NO handback cap and NO tier and ordered the worker to derive both from AGENTS.md against the commit count constraint 3 fixes, and the worker derived five commits, resolved the condition ">5 per-commit tables" to FALSE, named the 60-line tier, measured its own file at 79 lines and declared a DECISION D15 stated-cause overage itemising the mandated content that caused it. That is the R-0676 recurrence's replacement counter-measure discharging correctly one round after it was written, by the actor that can count the commits after they exist. THE VERDICT IS PASS: every gate reproduced under the reviewer's own execution, no id was minted, no finding record moved, and the two defects this round records are both against text the reviewer wrote.
<<<END GATE2

<<<SLICE INVENTORY
# F031 Inventory — the decision inbox as the source has it today

> MEASURED, not recalled. Every answer below was produced by a command run
> against the working tree at the round base named in `.agent/handoff.md`, and
> every answer names the file and the SYMBOL it was read from rather than a bare
> line number. Where a thing does not exist, the answer says so and names the
> command whose empty output proves it. This file is state, not documentation:
> it is superseded by the T-slices it exists to plan.

## Q1 — the queue store
Which module owns the decision queue, is it file-based, and what is its public
read surface?
ANSWER: TO BE MEASURED

## Q2 — the decision types
What is the exact set of decision types the queue recognises, where is it
defined, and how many members does it have?
ANSWER: TO BE MEASURED

## Q3 — the producers
Which call sites actually WRITE a decision into the queue, and which of the Q2
types does each produce?
ANSWER: TO BE MEASURED

## Q4 — the CLI surface
What decision commands exist, what are their command ids, and which module
implements them?
ANSWER: TO BE MEASURED

## Q5 — the blocked-subtree computation
Which symbol computes what a waiting task blocks downstream, in which module,
and what does it take and return?
ANSWER: TO BE MEASURED

## Q6 — the decision event kinds
Does the event stream carry a decision-requested or decision-resolved event kind
today, on the Python side and in the TypeScript humanize catalog? Name the
search you ran and its result on each side.
ANSWER: TO BE MEASURED

## Q7 — the write channel
Is there already a write-channel command that resolves a decision? Name the
command id, the constant that holds it, and the dispatch symbol.
ANSWER: TO BE MEASURED

## Q8 — the UI today
Does any inbox or decision component exist under `apps/ui/src`? Name the search
and its result.
ANSWER: TO BE MEASURED

## Q9 — the dependencies
F031 depends on F009, F050 and F051. For each, give the STATUS mark and the one
thing it left behind that F031 will build on.
ANSWER: TO BE MEASURED

## Observations
Defects or surprises found while measuring, each with its measurement. No
finding id is minted here (block constraint 8); the reviewer rules these.
ANSWER: TO BE MEASURED
<<<END INVENTORY

── Done when ─────────────────────────────────────────────────
Run every gate yourself, record its REAL exit code and REAL output, and
report ONE LINE PER GATE in the handback with transcripts kept out of it
(finding R-0582). "Green" as a word is a finding. Every gate runs at a
commit STRICTLY EARLIER than C4, which writes the handback (§3 item 31).

G1  Branch and cleanliness. `git branch --show-current` prints
    `feature/f031-decision-inbox` and NOT `main`. `.agent/STOP` read
    from disk is ABSENT before C0a and again before C4. Report
    `git status --porcelain` line count after each of C0a, C0b, C1, C2
    and C3; each must be 0.

G2  Transport. Report sha256, byte count and line count for FOUR
    readings: `.remedy-wt/f031-r3.md` before C0a, the committed C0a
    blob, the committed C0b blob, and `.agent/last_block.md` off disk
    after C0b. All four must be EQUAL. Report the git blob id of C0a's
    and C0b's file; they must be the SAME id.

G3  Extraction. Run your extractor over the COMMITTED C0a blob and
    report the slice count, the CONTENT lines inside markers, and the
    TOTAL line count. Report the numbers YOUR extractor printed.

G4  The plan. `.agent/plan.md` at C1 is byte-equal to PLANF031R3 under
    your stated newline convention; report the slice length, the file
    length and the convention. NEGATIVE CONTROL: the file is NOT
    byte-equal to the same slice with its trailing newline REMOVED.
    `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` STRICTLY under 50.

G5  The append. Report that the region of `.agent/live_review.md` at C2
    equals the extracted GATE2 bytes, that the base blob is a byte-exact
    PREFIX of the C2 file, and the byte arithmetic. Report a SECOND,
    INDEPENDENT reading: split the C2 file on blank lines and confirm
    the LAST unit equals GATE2; report the unit count before and after.
    NEGATIVE CONTROL: flip ONE byte inside the appended paragraph in a
    disposable worktree and report that BOTH readers reject the mutant
    while BOTH accept the true file.

G6  The sets moved only where constraint 8 allows. In
    `.agent/live_review.md`, base `9e773d4a` versus C2: `^- R-\d+ — `
    238 → 238, ids ADDED the EMPTY SET, ids REMOVED the EMPTY SET,
    maximum `R-0677` → `R-0677` UNCHANGED, `^Done: R-` 2 → 2,
    `^Recurrence: R-` 13 → 13. `^Gate: R\d+ — ` 2 → 3, gaining exactly
    the key `R2`, with `R19` and `R1` still present.

G7  The inventory is answered and its citations resolve. At C3, in
    `.agent/f031_inventory.md`:
    (a) STRUCTURE VERBATIM: take the INVENTORY slice, drop every line
        beginning `ANSWER: `, and confirm the remaining lines appear in
        the committed file verbatim, in the same order, with nothing
        between them but the replaced answer lines. Report the number
        of structure lines compared and the number that matched, and
        they must be EQUAL. Report `^## Q\d+ — ` measured on the slice
        and on the file, and they must be EQUAL;
    (b) the literal token `TO BE MEASURED` occurs 0 times — every
        placeholder was replaced. Report also that it occurs a NONZERO
        number of times in the INVENTORY slice itself, so this reading
        distinguishes a replaced file from an unreplaced one rather
        than passing on a string that was never there;
    (c) `^ANSWER: ` occurs once under every `## ` heading of the file —
        report the heading count and the ANSWER count and that they
        are EQUAL;
    (d) EVERY repository path the file names — extract them
        mechanically, do not list them by hand — resolves at the base
        with `git ls-tree 9e773d4a -- <path>`; report the number of
        paths extracted and the number that resolved, and they must be
        EQUAL. Report the extracted list in the ROUND's scratch, not in
        the handback;
    (e) EVERY symbol the file names as a definition site is grepped
        back in the file it is attributed to and found; report the
        number checked and the number found, and they must be EQUAL.
        This is the gate that makes the inventory a measurement rather
        than an essay (finding R-0338's class: never attribute a name
        to a file without resolving it there).

G8  Structure and hygiene, over C0a..C3. Report per commit: that it is
    single-parent, and its INSERTION count — the `+` column only, per
    AGENTS.md DECISION F104 D1 — each under 500. Report the range path
    set MINUS the change set (must be EMPTY) and the change set MINUS
    the range (must be exactly `.agent/handoff.md`, which C4 writes).
    Report `git ls-files .remedy-wt` as 0, `git ls-files` over the
    pattern `*.zip` as 0, `git worktree list` as 1 line, and the reflog
    OPERATION field with amend, rebase and cherry each 0. Report that
    `git diff --name-only 9e773d4a..C3` names NO path under
    `packages/`, `apps/`, `tests/` or `docs/` (constraint 10).

G9  Suites, run SERIALLY, never two pytest processes at once, in the
    PRIMARY checkout at the C3 tree, with `git worktree list` reported
    as 1 line immediately BEFORE the first pytest command. All must
    exit 0; report the real exit code and the counts:
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/cli/test_decision_answers.py -q
      python3 -m pytest tests/cli/test_open_decisions_view.py -q
      python3 -m pytest tests/cli/test_golden_path.py -q
    The reviewer executed the first four and the last at `6325ac2f`
    with no worktree present and measured 470, 52, 21, 16 and 42, every
    one exit 0. The two decision suites are ordered here because this
    round reads their subject; the reviewer has NOT measured their
    counts, so report whatever YOUR run prints and do not reconcile it
    against any number. `tests/docs/` is NOT ordered: no `docs/` path
    is in the change set.

G10 The push. AFTER C4, run `git push origin feature/f031-decision-inbox`.
    No `--force`, no `--force-with-lease`, no history rewrite, no branch
    deletion, no pull request. This gate's outcome is REPORTED TO THE
    REVIEWER and is NOT a value of any file this round writes (finding
    R-0371's extended counter-measure).

── Handback ──────────────────────────────────────────────────
Rewrite `.agent/handoff.md` at C4 per docs/agents/handback_template.md:
feature and round, branch, base and commit SHAs, a changed-files table
per commit, the item-status table covering C0a, C0b, C1, C2, C3, C4 and
the push, ONE LINE PER GATE with its real result, the finding counts,
and the next expected action. Carry the `Fortschritt:` block above
VERBATIM across the lines it occupies — count them yourself and carry
exactly those; this block states no numeral for them.

THE HANDBACK LINE CAP: this block states no cap and no tier. Resolve it
yourself from AGENTS.md under `### handoff.md` against the number of
commits constraint 3 fixes, and report BOTH the commit count you derived
and the tier that follows. If the MANDATED content genuinely does not
fit, exceed it and carry a DECISION D15 "Deviations, declared" line
naming your measured line count and the specific mandated content that
caused it. Never drop a mandated section to fit. Do NOT claim compliance
with any token cap: that cap was withdrawn.

Any finding count you state carries the RULE that produced it and the
COMMIT it was measured at, in the same sentence, per DECISION F009 D10.
A narrower set is named "the findings this feature must still act on"
and is never called "open" unqualified.

Do NOT restate the inventory's answers in the handback — it is a
committed file the reviewer reads directly, and copying it in would
duplicate a record that can then drift (R-0417). Report only that G7's
readings passed and what they measured.

Declare every deviation, contradiction and assumption.
──────────────────────────────────────────────────────────────

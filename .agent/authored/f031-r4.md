── STEP R4 — F031 Decision inbox ─────────────────────────────
Goal:        Record the R3 verdict and the one recurrence its review
             surfaced, and carry the inventory's consequences into the
             plan so the next session can rule the design and plan
             T001 without re-measuring anything. State only.

Fortschritt: ~3 % (F031 claimed; R1, R2 and R3 landed and gated · the
             source inventory is on disk · the design rulings and T001
             are next · no T-slice started) — Schaetzung

Bundle:      C0a save this block · C0b mirror it into last_block ·
             C1 the plan · C2 the R3 gate entry and the recurrence ·
             C3 the handback.

Change set:  exactly these paths, nothing else —
             .agent/authored/f031-r4.md
             .agent/last_block.md
             .agent/plan.md
             .agent/live_review.md
             .agent/handoff.md
             This list bounds the round's WRITES, not its ACTIONS: the
             push named in gate G9 is ordered explicitly and is not a
             file (finding R-0674).

── Base ──────────────────────────────────────────────────────
The round base is `f26c5da5e5b60e8b7a3b2ba1a4b1a0e5c0ff5a0d`'s branch —
resolve the base as the current tip of `feature/f031-decision-inbox`,
which is the C4 of F031 R3 and equals the remote tip. Stay on that
branch; create none, never commit to `main`.

Readings the reviewer MEASURED at that tip, re-checkable there:
- `.agent/live_review.md`: `^- R-\d+ — ` 238 all DISTINCT, maximum
  `R-0677`; `^Done: R-\d+ — ` 2; `^Recurrence: R-` 13;
  `^Gate: R\d+ — ` 3, the keys `R19`, `R1` and `R2`.
- The §3 item 10 open set — every `^- R-\d+ — ` paragraph minus every
  `^Done: R-\d+ — ` line — is 238 − 2 = 236 at that commit.
- `.agent/plan.md` 44 lines. `.agent/f031_inventory.md` exists, 225
  lines, with `TO BE MEASURED` occurring 0 times in it.

── Why this round exists ─────────────────────────────────────
R3 passed on every one of its ten gates under the reviewer's own
execution, and the reviewer additionally re-measured all six of the
inventory's `## Observations` against the source and found every one
true. C2 records that verdict.

The review also found ONE defect, and it is the reviewer's own: G8 of
the R3 block ordered "the reflog OPERATION field with amend, rebase and
cherry each 0" and named NO SCOPE, where the R1 and R2 blocks had both
written "over this round's rows". Read literally the clause is
repository-wide and unmeetable — the worker measured 17 amend, 26
rebase-family and 60 cherry-pick entries in the repo-wide reflog, all
predating this branch — while over the branch's own 18 entries all
three are 0. The worker reported BOTH scopes and declared the
ambiguity, which is the correct response and the only reason nothing
false reached the record. NO NEW ID IS MINTED: the open set was
searched for the defect (§3 item 30) and R-0601 already holds this
exact family — a reflog gate whose SCOPE makes it unmeetable — so C2
records a `Recurrence:` paragraph against it.

C1 carries the inventory's consequences into the plan. This round rules
NOTHING about the design: the contradictions the inventory found are
real and deserve a decision written with room to think, so the plan
names them as R5's work rather than settling them in a record round.

── Constraints ───────────────────────────────────────────────
1. Apply every authored slice BYTE FOR BYTE. Never retype, rewrap,
   reflow or "fix" a slice. If a slice looks wrong, apply it verbatim
   and DECLARE the disagreement in the handback. A contradiction inside
   this block is the reviewer's defect, not yours: state it, reconcile
   nothing.
2. Slice transport. This block is saved verbatim as
   `.agent/authored/f031-r4.md` at C0a and mirrored byte-identically
   into `.agent/last_block.md` at C0b. Extract every slice
   PROGRAMMATICALLY out of the COMMITTED C0a blob by its marker LINES —
   a line equal to `<<<SLICE <NAME>` opens it, a line equal to
   `<<<END <NAME>` closes it. Marker lines never reach a target file.
3. Commit sequence, exactly: C0a, C0b, C1, C2, C3. No extra commit,
   none dropped, no reordering. If you must correct a landed commit, do
   NOT add a commit outside this sequence — declare it (R-0675). The
   push runs after C3.
4. Never amend, rebase, cherry-pick, force-push or rewrite history;
   never delete a branch; never merge; create no pull request.
5. `git status --porcelain` prints 0 lines after every commit. Read
   `.agent/STOP` from disk before C0a and again before C3; if present,
   finish the commit in hand, write the handback and stop (G6).
6. The slices this block carries are the whole text PLANF031R4 and the
   two appended paragraphs GATE3 and RECUR601. This paragraph names
   them and states no count of them; G3 orders you to report the count
   YOUR extractor measured.
7. C2 appends GATE3 then RECUR601 to `.agent/live_review.md` in that
   order, each separated from the preceding text and from each other by
   exactly one blank line, the file ending in exactly one newline. This
   block carries no FROM/TO pair, so no containment reading is owed and
   none is stated.
8. THIS ROUND MINTS NO FINDING ID and changes no finding record.
   `^- R-\d+ — ` must be 238 before and after and the maximum must stay
   `R-0677`.
9. Do not touch any path under `packages/`, `apps/`, `tests/`, `docs/`
   or `README.md`, and do not touch `.agent/f031_inventory.md` — the
   inventory is landed evidence and is corrected by dating in a later
   round, never by editing (§3 item 20, findings R-0417 and R-0525).
10. Destructive verification, if any, runs ONLY in a disposable
    `git worktree` under `.remedy-wt/`, removed BY ITS EXACT PATH
    (R-0662) and BEFORE the G8 suites — a worktree present makes
    `tests/orchestration/test_test_runner.py::`
    `TestVitestFrontendTestFoundation::test_vitest_passes` fail on a
    missing `node_modules` (the R-0518 shape), which is an artefact of
    the measurement and not a regression.

── Authored slices ───────────────────────────────────────────

<<<SLICE PLANF031R4
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the merge
commit of pull request #213 which closed F022. `.agent/live_review.md` is the
source of truth for the record, the round map and the finding-id ceiling;
`.agent/f031_inventory.md` is the measured source inventory R3 landed.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via decision events
driving the badge, with branch-only blocking semantics intact. DONE when the
inbox lists fixture decisions of every producing type with correct blocked-size
math, answering from a card round-trips through the write channel into the same
effects the CLI produces, the badge tracks live, and ordering follows a
documented rule over age and blocked size rather than vibes.

## Current Step
R4 records the R3 verdict and the R-0601 recurrence, and carries the inventory's
consequences into this plan. It rules nothing: the design questions below are
R5's, written with room to think rather than settled in a record round.

## Next Steps
1. R5 rules three things the inventory forces, each as a DECISION in
   `.agent/decisions.md`: (a) what "the decision queue" IS, since
   `decision_queue.py` performs no I/O and re-derives decisions from the job's
   events, so the feature file's "FILE-BASED (the established store with its
   CLI)" describes the event log rather than the module; (b) whether the badge
   is fed by EMITTING the decision event kinds that do not exist today or by
   re-deriving on snapshot refetch; (c) whether the two declared-but-unproduced
   types stay in the set, since a fixture per producing type is the acceptance
   criterion and two types have no producer to fixture.
2. R6 records the R5 verdict and plans T001 against whatever R5 ruled.

## Risks
- Open findings, stated with the rule and the commit DECISION F009 D10 requires:
  by §3 item 10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — `
  line — the open set is 236, measured at R3's C4.
- The findings THIS FEATURE MUST STILL ACT ON — a narrower set, named as what it
  is and not called "open" — are R-0403, R-0413, R-0431, R-0445, R-0495, R-0533,
  R-0574, R-0601, R-0625, R-0632, R-0672, R-0674, R-0675, R-0676 and R-0677, of
  which R-0495 and R-0574 are the two Highs, inherited from F085 and F086.
- THE BADGE F031 IS ASKED TO DRIVE IS A CONSTANT ZERO TODAY. `decision_count`
  and the `open_decisions` sum both count `human_decision_requested`, which no
  producer emits and which `event_schemas.py` does not declare. This is the
  largest gap between the feature file and the source, and no T-slice estimate
  is sound until R5 rules item 1(b).
- The record holds `Gate: R19` from F022 as its seed entry. If F031 reaches its
  own R19 that key collides — the §3 item 26 defect. A round before then renames
  the seed or the scheme; this bullet is the reminder.
<<<END PLANF031R4

<<<SLICE GATE3
Gate: R3 — the F031 R3 entry. R3 PASSED ON EVERY ONE OF ITS TEN GATES, AND THE REVIEWER RE-RAN EVERY ONE OF THEM ITSELF RATHER THAN READING THE HANDBACK'S WORD FOR ANY OF THEM. THE ROUND'S SUBSTANCE IS THE SOURCE INVENTORY, and it is the first round of this feature to read production code rather than state. TRANSPORT HELD IN ITS STRONGEST FORM: the reviewer's own scratch original at `.remedy-wt/f031-r3.md`, the committed C0a blob, the committed C0b blob and `.agent/last_block.md` off disk are ALL sha256 `ec113810c7d85451dbd56e8bc45ee79e5b4a41a441006310dc5b5cdca0e08966` over 24005 bytes and 363 lines, and C0a and C0b resolve to the SAME git blob. THE EXTRACTION printed 3 slices across 104 content lines against 363 total. `.agent/plan.md` at C1 is 2617 bytes and 44 lines, byte-equal to its slice with the trailing-newline-removed control FALSE, `^## Goal$` and `^## Next Steps$` once each, strictly under the cap of 50. THE APPEND HELD UNDER BOTH READERS AND A CONTROL: the base blob is a byte-exact PREFIX, the delta is 4014 bytes against a 4013-byte slice plus one separator, an independent blank-line split went 274 units to 275 with the LAST equal to GATE2, and a byte-flip mutant was rejected by both readers while both accepted the true file — the reviewer ran its own mutant beside the worker's and agreed. THE SETS MOVED ONLY WHERE CONSTRAINT 8 ALLOWED: `^- R-\d+ — ` 238 to 238, ids ADDED and ids REMOVED both the EMPTY SET, maximum `R-0677` UNCHANGED, `^Done: R-` 2 to 2, `^Recurrence: R-` 13 to 13, and `^Gate: R\d+ — ` 2 to 3 gaining exactly the key `R2`. THE INVENTORY GATE IS THE ONE THAT MATTERED AND IT HELD IN EVERY LIMB: the scaffold's structure lines landed verbatim in strict lockstep, the Q-headings agree on both sides, the literal `TO BE MEASURED` occurs 0 times in the committed file while occurring a nonzero number of times in the slice — so the reading distinguishes a replaced file from an unreplaced one rather than passing on a string that was never there — every `## ` heading carries exactly one `ANSWER: `, every repository path the file names resolves at the base, and every symbol it attributes to a file is found in that file. THE REVIEWER DID NOT STOP AT THE GATE. All six of the inventory's `## Observations` were re-measured independently against the source and ALL SIX ARE TRUE: `packages/orchestration/decision_queue.py` imports only `dataclasses`, `typing` and `Job` and performs NO I/O, so it re-derives decisions rather than storing them and the feature file's "FILE-BASED" describes the event log rather than the module; `human_decision_requested` has seven occurrences of which every one is a reader, a label-map key, a count or a test fixture and NONE is an emission, and it is absent from `event_schemas.py`, so `decision_count` and the `open_decisions` sum are both always 0 in production and the badge F031 must drive is a constant zero; `human_decision_resolved` has zero occurrences anywhere; `worker_approval` and `revert_missing` occur ONLY inside the `DECISION_TYPES` frozenset while `patch_approval` and `token_budget` each have a real producer beside their declaration, so two declared types are produced by nobody; `HumanDecision.type` is annotated plain `str` and `DECISION_TYPES` is imported only under `tests/`, so the set constrains nothing at runtime; and `ui_server.py` contains no `fp:` handling at all while `_dispatch_decision_resolve` reaches only `answer_task_decision`. AN INVENTORY THAT CONTRADICTS ITS OWN FEATURE FILE IN ITS FIRST ROUND IS THE INVENTORY WORKING, and the worker declared the contradiction against the block's own Goal rather than quietly writing the answer the block expected — which is what constraint 1 exists to produce. STRUCTURE HELD: six commits, each single-parent, insertions 363, 252, 18, 2, 225 and 126, each far under the 500 cap; the range path set MINUS the change set is EMPTY and the change set MINUS the range is EMPTY once the handback commit is counted; NO path under `packages/`, `apps/`, `tests/` or `docs/` appears in the range, so the round read production code and changed none of it; `git ls-files .remedy-wt` 0 and the zip glob 0; one worktree; `git status --porcelain` 0. THE SEVEN SUITES ARE THE REVIEWER'S OWN, run serially with never two pytest processes alive, every one exit 0: 470, 52, 21, 16, 29, 26 and 42, the five previously measured reproducing cell for cell and the two decision suites measured here for the first time. THE PUSH DISCHARGED and the remote tip equals the local tip; no pull request, nothing merged. THE VERDICT IS PASS, and the round's one declared imprecision is the reviewer's own reflog clause, recorded in the paragraph below.
<<<END GATE3

<<<SLICE RECUR601
Recurrence: R-0601 — A REFLOG GATE WAS ORDERED WITH NO SCOPE AT ALL, SO ITS LITERAL READING IS REPOSITORY-WIDE AND UNMEETABLE. SECOND INSTANCE, at F031 R3, and it is the reviewer's own. NO NEW ID IS MINTED: R-0601 already holds this family — a reflog gate whose SCOPE is wrong makes the ordered universal impossible for the round to satisfy — and its counter-measure already replaces the unmeetable universal with claims measured over the round's own entries. THE MEASUREMENT, taken by the worker and confirmed by the reviewer: G8 of the R3 block orders "the reflog OPERATION field with amend, rebase and cherry each 0" and names no scope, where G11 of the R1 block and G8 of the R2 block had both written "over this round's rows". Over the branch's own 18 reflog entries the three counts are 0, 0 and 0 and the gate is met; over the repository-wide reflog of 5928 entries they are 17 `commit (amend)`, 26 rebase-family and 60 `cherry-pick`, the most recent dated 2026-08-19, 2026-07-24 and 2026-08-03 and ALL of them predating this branch, so under the literal reading the gate can never pass and never could have. WHAT MAKES IT A RECURRENCE RATHER THAN A NEW CLASS: R-0601's instance was a reflog universal that the round's own navigation made unmeetable, and this is the same gate family losing the same qualifier from the other direction — there the scope was stated and too wide for the round, here it was not stated at all and defaults to the widest scope there is. THE WORKER RESOLVED IT THE RIGHT WAY ROUND: it reported BOTH readings, named the operation counts under each, dated the repo-wide hits to show they precede the branch, and declared the ambiguity rather than picking the reading that suited it — so nothing false reached the record and the property the gate protects, the ABSENCE of history rewriting by THIS round, is affirmatively measured. WHY IT RECURRED IS WORTH THE PARAGRAPH: the scope qualifier survived two blocks by being copied forward and was lost the one time the gate was re-typed rather than copied, which is the failure mode of every rule that lives in a sentence rather than in a check. THE COUNTER-MEASURE IS EXTENDED, binding on every block from here: a gate that counts anything in the reflog states the SCOPE and the FIELD in the same clause — the entries of THIS round, read by the operation prefix before the first colon of `git reflog --format=%gs` — and a block that omits either is defective even when the round happens to satisfy it. The scope half is this recurrence; the field half is finding R-0613, and the two are one clause, so a block writes them together or writes neither correctly.
<<<END RECUR601

── Done when ─────────────────────────────────────────────────
Run every gate yourself, record its REAL exit code and REAL output, and
report ONE LINE PER GATE in the handback with transcripts kept out of it
(finding R-0582). "Green" as a word is a finding. Every gate runs at a
commit STRICTLY EARLIER than C3, which writes the handback (§3 item 31).

G1  Branch and cleanliness. `git branch --show-current` prints
    `feature/f031-decision-inbox` and NOT `main`. `.agent/STOP` read
    from disk is ABSENT before C0a and again before C3. Report
    `git status --porcelain` line count after each of C0a, C0b, C1 and
    C2; each must be 0.

G2  Transport. Report sha256, byte count and line count for FOUR
    readings: `.remedy-wt/f031-r4.md` before C0a, the committed C0a
    blob, the committed C0b blob, and `.agent/last_block.md` off disk
    after C0b. All four must be EQUAL. Report the git blob id of C0a's
    and C0b's file; they must be the SAME id.

G3  Extraction. Run your extractor over the COMMITTED C0a blob and
    report the slice count, the CONTENT lines inside markers, and the
    TOTAL line count. Report the numbers YOUR extractor printed.

G4  The plan. `.agent/plan.md` at C1 is byte-equal to PLANF031R4 under
    your stated newline convention; report the slice length, the file
    length and the convention. NEGATIVE CONTROL: the file is NOT
    byte-equal to the same slice with its trailing newline REMOVED.
    `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` STRICTLY under 50.

G5  The two appends. For GATE3 and RECUR601 separately, report that the
    corresponding region of `.agent/live_review.md` at C2 equals the
    extracted slice bytes, that the base blob is a byte-exact PREFIX of
    the C2 file, and the byte arithmetic. Report a SECOND, INDEPENDENT
    reading: split the C2 file on blank lines and confirm the LAST TWO
    units equal the two slices IN ORDER; report the unit count before
    and after. NEGATIVE CONTROL: flip ONE byte inside the FIRST
    appended paragraph in a disposable worktree and report that BOTH
    readers reject the mutant while BOTH accept the true file.

G6  The sets moved only where constraint 8 allows. In
    `.agent/live_review.md`, the round base versus C2: `^- R-\d+ — `
    238 → 238, ids ADDED the EMPTY SET, ids REMOVED the EMPTY SET,
    maximum `R-0677` → `R-0677` UNCHANGED, `^Done: R-` 2 → 2.
    `^Recurrence: R-` 13 → 14, gaining exactly one `R-0601` line.
    `^Gate: R\d+ — ` 3 → 4, gaining exactly the key `R3`, with `R19`,
    `R1` and `R2` still present.

G7  Markers and untouched paths. Line-anchored `^<<<SLICE ` and
    `^<<<END ` both count 0 in `.agent/plan.md` and
    `.agent/live_review.md` at C2. Report that
    `git diff --name-only <base>..C2` names NO path under `packages/`,
    `apps/`, `tests/` or `docs/` and does NOT name
    `.agent/f031_inventory.md` (constraint 9).

G8  Structure and hygiene, over C0a..C2. Report per commit: that it is
    single-parent, and its INSERTION count — the `+` column only, per
    AGENTS.md DECISION F104 D1 — each under 500. Report the range path
    set MINUS the change set (must be EMPTY) and the change set MINUS
    the range (must be exactly `.agent/handoff.md`, which C3 writes).
    Report `git ls-files .remedy-wt` as 0, `git ls-files` over the
    pattern `*.zip` as 0, and `git worktree list` as 1 line. FOR THE
    REFLOG, state the SCOPE and the FIELD in the reading itself, as
    this round's own RECUR601 slice requires: over THIS ROUND'S reflog
    entries only, read by the OPERATION PREFIX before the first colon
    of `git reflog --format=%gs`, report `amend`, `rebase` and `cherry`
    each 0, and report how many entries you scoped the reading to.

G9  Suites, run SERIALLY, never two pytest processes at once, in the
    PRIMARY checkout at the C2 tree, with `git worktree list` reported
    as 1 line immediately BEFORE the first pytest command. All must
    exit 0; report the real exit code and the counts:
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/cli/test_golden_path.py -q
    The reviewer executed all five at R3's C4 with no worktree present
    and measured, in the order listed: 470, 52, 21, 16 and 42, every
    one exit 0. Report yours against those and account for any
    difference. `tests/docs/` is NOT ordered: no `docs/` path is in the
    change set.

G10 The push. AFTER C3, run `git push origin feature/f031-decision-inbox`.
    No `--force`, no `--force-with-lease`, no history rewrite, no branch
    deletion, no pull request. This gate's outcome is REPORTED TO THE
    REVIEWER and is NOT a value of any file this round writes (finding
    R-0371's extended counter-measure).

── Handback ──────────────────────────────────────────────────
Rewrite `.agent/handoff.md` at C3 per docs/agents/handback_template.md:
feature and round, branch, base and commit SHAs, a changed-files table
per commit, the item-status table covering C0a, C0b, C1, C2, C3 and the
push, ONE LINE PER GATE with its real result, the finding counts, and
the next expected action. Carry the `Fortschritt:` block above VERBATIM
across the lines it occupies — count them yourself and carry exactly
those; this block states no numeral for them.

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

THIS IS THE LAST ROUND OF THE SESSION. Your `## Next` section is the
only thing the next session reads first, so make it name, in order:
Phase 1 rule 1 (re-read `.agent/STOP` from disk), then that no pull
request exists for this branch and none should be created yet, then
that R5 rules the three design questions `.agent/plan.md` names, then
that R5's first commit also records the R4 verdict, which by DECISION
F085 D9 no artefact of this round can carry.

Declare every deviation, contradiction and assumption.
──────────────────────────────────────────────────────────────

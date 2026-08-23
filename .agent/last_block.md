── STEP R8 — F031 Decision inbox ─────────────────────────────
Goal:        Record the R7 verdict, carry the pushed tips the R7
             gate measured into the permanent record as finding
             R-0679's fix clause requires, and plan T002 against a
             design gap this session MEASURED. State only; no
             production path is touched.

Fortschritt: ~25 % (F031 claimed; R1 through R7 landed and gated ·
             T001 SHIPPED — the derivation module, the read endpoint
             and 29 tests are on disk and green · T002 planned, its
             design gap named · T003 offen) — Schaetzung

Bundle:      C0a save this block · C0b mirror it into last_block ·
             C1 the plan · C2 the R7 gate entry · C3 the handback.

Change set:  exactly these paths, nothing else —
             .agent/authored/f031-r8.md                        (C0a)
             .agent/last_block.md                              (C0b)
             .agent/plan.md                                    (C1)
             .agent/live_review.md                             (C2)
             .agent/handoff.md                                 (C3)
             This list bounds the round's WRITES, not its ACTIONS:
             the push named in G9 is ordered explicitly and is not a
             file (R-0674).

── Base ──────────────────────────────────────────────────────
The round base is `3f3d3e8f7f6032576db7ad0e5f672869b60f6dc2`, the R7
handback commit and the current tip of `feature/f031-decision-inbox`.
Every SHA-shaped token in this block was passed to `git cat-file -t`
before emission and every one resolves, so G8 orders that sweep with
an EMPTY failure set and this block declares no positive control.
Stay on that branch; create none, never commit to `main`.

Readings the reviewer MEASURED at that base, re-checkable there:
- `.agent/live_review.md`: `^- R-\d+ — ` 240 all DISTINCT, maximum
  `R-0679`; `^Done: R-\d+ — ` 2; `^Recurrence: R-` 15;
  `^Gate: R\d+ — ` 7, the keys `R19`, `R1`, `R2`, `R3`, `R4`, `R5`
  and `R6`.
- The §3 item 10 open set — every `^- R-\d+ — ` paragraph minus
  every `^Done: R-\d+ — ` line — is 240 − 2 = 238 at that commit.
- `.agent/plan.md` 49 lines. `.agent/handoff.md` 90 lines.

── Why this round exists ─────────────────────────────────────
R7 passed on every one of its eleven gates under the reviewer's own
execution, INCLUDING BOTH RED-PROOFS, which the reviewer re-ran in
its own disposable worktree rather than reading the worker's word
for them. C2 records that verdict and carries the pushed tips, which
by finding R-0679's fix clause have no other carrier.

C1 plans T002, and it plans it against something this session
measured rather than assumed: the canonical design reference has NO
inbox or decision component. That is a spec gap, not a licence to
improvise, so the plan names the ruling T002's first round owes
before any card ships.

── Constraints ───────────────────────────────────────────────
1. Apply every authored slice BYTE FOR BYTE. Never retype, rewrap,
   reflow or "fix" one. If a slice looks wrong, apply it verbatim
   and DECLARE the disagreement in the handback: a contradiction
   inside this block is the reviewer's defect, not yours.
2. Slice transport. This block is saved verbatim as
   `.agent/authored/f031-r8.md` at C0a and mirrored byte-identically
   into `.agent/last_block.md` at C0b. Extract every slice
   PROGRAMMATICALLY out of the COMMITTED C0a blob by its marker
   LINES — `<<<SLICE <NAME>` opens, `<<<END <NAME>` closes. Marker
   lines never reach a target file.
3. Commit sequence, exactly: C0a, C0b, C1, C2, C3. No extra commit,
   none dropped, no reordering. C1 is the FIRST substantive commit
   because this round touches the finding ledger (§3 item 23). The
   push runs after C3. To correct a landed commit, do NOT add one
   outside this sequence — declare it (R-0675).
4. Never amend, rebase, cherry-pick, force-push or rewrite history;
   never delete a branch; never merge; create no pull request.
5. `git status --porcelain` prints 0 lines after every commit. Read
   `.agent/STOP` from disk before C0a and again before C3; if
   present, finish the commit in hand, write the handback and stop.
6. The slices this block carries are the whole text PLANF031R8 and
   the ledger paragraph GATE7. This paragraph names them and states
   no count; G3 orders you to report the count YOUR extractor
   measured.
7. C2 appends GATE7 to `.agent/live_review.md`. THE APPEND SHAPE IS
   STATED ONCE, HERE, AND EVERY GATE NAMES THIS PARAGRAPH RATHER
   THAN RESTATING IT — the R-0471 counter-measure the previous round
   registered, applied again. Under the newline-INCLUDED convention
   the slice already ends in a newline, so the file at C2 is
   EXACTLY: the base blob, then one newline, then GATE7. Nothing
   follows, and the file ends in exactly one newline because GATE7
   carries it. THIS BLOCK CARRIES NO FROM/TO PAIR, so no containment
   reading is owed and none is stated.
8. THIS ROUND MINTS NO FINDING ID and writes no `Recurrence:` line.
   `^- R-\d+ — ` must be 240 before and 240 after, the maximum must
   stay `R-0679`, and `^Recurrence: R-` must be 15 before and 15
   after. R7 earned no finding: every gate reproduced and the two
   declared items are naming rulings the block itself ordered.
9. Touch nothing under `packages/`, `apps/`, `tests/` or `docs/`,
   and not `.agent/decisions.md` or `.agent/f031_inventory.md` —
   landed evidence is corrected by dating in a later round, never by
   editing (§3 item 20, findings R-0417 and R-0525). Consequently
   `tests/docs/` and `test_roadmap_index.py` are NOT gated.
10. Destructive verification, if any, runs ONLY in a disposable
    `git worktree` under `.remedy-wt/`, removed BY ITS EXACT PATH
    (R-0662) and before the G8 suites. `.remedy-wt/dry` and
    `.remedy-wt/rev-r7` are PRE-EXISTING scratch belonging to no
    round of this feature: do not create a worktree at either path,
    read from them or delete them.

── Authored slices ───────────────────────────────────────────

<<<SLICE PLANF031R8
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
R8 records the R7 verdict and plans T002. T001 is SHIPPED: the module, the
`/api/jobs/<job_id>/decisions` route and 29 tests are on disk and green.

## Next Steps
1. R9 measures the UI inventory the inbox needs and rules the design gap named in
   Risks: which `--remedy-*` tokens the SHIPPED `apps/ui/src` CSS defines (not
   the reference sheet's), which card shell to reuse, where the inbox mounts in
   `RemedyShell`, and how the UI is tested — measured per file and symbol.
2. T002a then builds the cards and the GENERIC options renderer — producers own
   the semantics, so no per-type form is hardcoded — with the component tests
   the extensibility test requires.
3. T002b adds ordering, filtering and the badge, where DECISION F031 D2 binds:
   the badge re-derives on refetch over the existing SSE stream, no new event
   kind ships, and the two constant-zero counters D2 names get replaced.

## Risks
- Open findings, stated with the rule and the commit DECISION F009 D10 requires:
  by §3 item 10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — `
  line — the open set is 238, measured at `3f3d3e8f`.
- The findings THIS FEATURE MUST STILL ACT ON — a narrower set, named as what it
  is and not called "open" — are R-0403, R-0413, R-0431, R-0445, R-0471, R-0495,
  R-0533, R-0574, R-0601, R-0625, R-0632, R-0672, R-0674, R-0675, R-0676, R-0677,
  R-0678 and R-0679; R-0495 and R-0574 are the two Highs, from F085 and F086.
- THE CANONICAL DESIGN REFERENCE HAS NO INBOX AND NO DECISION COMPONENT, so T002
  has no visual authority and may not improvise one. Measured at `3f3d3e8f`:
  `component_spec.md` names no such component, and the only "inbox" string in
  that folder is one `ux_spec.md` §15 line listing mobile "status/digest/inbox
  surfaces" as expressly out of scope. R9 owes that ruling as a DECISION, with
  alternatives and a reversal path, before any card ships.
- The record holds `Gate: R19` from F022 as its seed entry. If F031 reaches its
  own R19 that key collides — the §3 item 26 defect. A round before then renames
  the seed or the scheme; this bullet is the reminder.
<<<END PLANF031R8

<<<SLICE GATE7
Gate: R7 — the F031 R7 entry. R7 PASSED ON EVERY ONE OF ITS ELEVEN GATES, AND THE REVIEWER RE-RAN EVERY ONE OF THEM ITSELF — THE TWO RED-PROOFS INCLUDED, IN ITS OWN DISPOSABLE WORKTREE, rather than reading the handback's word for any of them; every value that handback states reproduced exactly. THIS IS THE FIRST ROUND OF THIS FEATURE TO SHIP PRODUCTION CODE, so the code was read bottom-up before any number was checked: `packages/orchestration/decision_inbox.py` performs no I/O, opens no path and keeps no state, exactly as DECISION F031 D1 requires; it is additive over `export_decision_json` by precisely the two keys the block specified; and its docstring records the absent project argument as a deliberate absence, which is what AGENTS.md "Code Discoverability Conventions" asks of code that does not exist. TRANSPORT HELD IN ITS STRONGEST FORM: the reviewer's own pre-emission scratch at `.remedy-wt/f031-r7.md`, the committed C0a blob, the committed C0b blob and `.agent/last_block.md` off disk are ALL sha256 `9b1a517f52d133c610e40608faa1a8c20c41a2e59588cb98aad13d3bbcff2d69` over 33656 bytes and 457 lines, with C0a and C0b resolving to the SAME git blob `98f6f251`. THE EXTRACTION printed 3 slices across 51 content lines against 457 total over 6 marker lines. `.agent/plan.md` at `8a0bdc18` is 2954 bytes and 49 lines, byte-equal to PLANF031R7 under the newline-INCLUDED convention with the trailing-newline-removed control FALSE, `^## Goal$` and `^## Next Steps$` once each, strictly under the cap of 50. THE LEDGER APPEND HELD AS AN EQUALITY OVER THE WHOLE FILE: at `85daf94d` it is EXACTLY the base blob plus one newline plus GATE6 plus one newline plus RECUR471, 553746 bytes to 561117 with the delta 7371 equal to 1 plus 4255 plus 1 plus 3114; an independent blank-line split went 281 units to 283 with the LAST TWO equal to GATE6 then RECUR471 IN ORDER; and the reviewer flipped its own byte inside the FIRST appended paragraph, which BOTH readers rejected while BOTH accepted the true file. THE SETS MOVED ONLY WHERE CONSTRAINT 9 ALLOWED: `^- R-\d+ — ` 240 to 240 all DISTINCT, ids ADDED and ids REMOVED both the EMPTY SET, maximum `R-0679` unchanged, `^Done: R-` 2 to 2, `^Recurrence: R-` 14 to 15 with the one gained line naming `R-0471`, and `^Gate: R\d+ — ` 6 to 7 gaining exactly the key `R6`. MARKERS WERE LINE-ANCHORED 0 in all six applied targets at their own commits; the eight-path range holds nothing under `docs/` or `apps/` and neither `.agent/decisions.md` nor `.agent/f031_inventory.md`; the range path set MINUS the change set is EMPTY and the change set MINUS the range is exactly `.agent/handoff.md`; six single-parent commits with insertions 457, 382, 21, 4, 391 and 120, each under the 500 cap; `git ls-files .remedy-wt` 0, the zip glob 0, one worktree, `git status --porcelain` 0. THE REFLOG READING STATES ITS OWN SCOPE AND FIELD: over this round's entries, read by the OPERATION PREFIX before the first colon of `git reflog --format=%gs`, every prefix is `commit`, so amend 0, rebase 0 and cherry 0. THE BLOCK'S OWN OBJECT IDS WERE SWEPT: 10 occurrences over 7 distinct word-bounded hex tokens, every one resolving under `git cat-file -t`, so the failing set is EMPTY as that block predicted. BOTH RED-PROOFS ARE REAL, AND THE REVIEWER PRODUCED ITS OWN: with the blocked-count seed set forced empty, `tests/orchestration/test_decision_inbox.py` went 1 failed and 24 passed on the single node id `test_blocked_count_equals_dag_blocked_downstream` reading `assert 0 == 3`; with the `handlers` key `decisions` renamed `decisionz`, `tests/ui_server/test_decisions_endpoint.py` went 2 failed and 2 passed on its two endpoint node ids, 404 where 200 is asserted. Each mutation reaches the test that is supposed to catch it, which is what makes the green run afterwards mean anything. THE SEVEN SUITES ARE THE REVIEWER'S OWN, run SERIALLY with never two pytest processes alive, every one REAL exit code 0 at 25, 4, 474, 52, 21, 16 and 42, and `ruff` over the four change-set paths under `packages/` and `tests/` exited 0 on the repository's OWN configuration. THE ARITHMETIC THE BLOCK ORDERED HELD: `tests/ui_server/` moved 470 to 474, which is exactly the four tests the route slice adds, so nothing else in that directory changed colour. THE PUSH DISCHARGED, AND THIS SENTENCE IS THE CARRIER FINDING R-0679'S FIX CLAUSE NAMES: measured by the reviewer against `git ls-remote`, the local and remote tips of `feature/f031-decision-inbox` are both `3f3d3e8f7f6032576db7ad0e5f672869b60f6dc2`; no pull request exists, and nothing was merged. THE HANDBACK DERIVED ITS OWN CAP rather than quoting one, reading the tier as 100 from the seven commits its constraint 3 fixes and landing at 90 lines, so no DECISION D15 overage was owed or claimed. THE ROUND'S TWO DECLARED ITEMS ARE BOTH SOUND: the test file sits under `tests/orchestration/` because AGENTS.md names a test after the source it covers and the block ruled that over the feature file's suggestion, and the G9 (b) probe's UI auto-build happened INSIDE the disposable worktree and left the primary checkout at `git status --porcelain` 0. THE VERDICT IS PASS.
<<<END GATE7

── Done when ─────────────────────────────────────────────────
Run every gate yourself, record its REAL exit code and REAL output,
and report ONE LINE PER GATE in the handback, transcripts kept out
of it (R-0582). "Green" as a word is a finding. Every gate runs at a
commit STRICTLY EARLIER than C3, which writes the handback (§3 item
31).

G1  Branch and cleanliness. `git branch --show-current` prints
    `feature/f031-decision-inbox` and NOT `main`. `.agent/STOP` read
    from disk is ABSENT before C0a and again before C3. Report
    `git status --porcelain` line count after each of C0a, C0b, C1
    and C2; each must be 0.

G2  Transport. Report sha256, byte count and line count for FOUR
    readings: `.remedy-wt/f031-r8.md` before C0a, the committed C0a
    blob, the committed C0b blob, and `.agent/last_block.md` off
    disk after C0b. All four must be EQUAL. Report the git blob id
    of C0a's and C0b's file; they must be the SAME id.

G3  Extraction. Run your extractor over the COMMITTED C0a blob and
    report the slice count, the CONTENT lines inside markers, and
    the TOTAL line count. Report the numbers YOUR extractor printed.

G4  The plan. `.agent/plan.md` at C1 is byte-equal to PLANF031R8
    under your stated newline convention; report slice length, file
    length and convention. NEGATIVE CONTROL: NOT byte-equal to that
    slice with its trailing newline REMOVED. `^## Goal$` 1,
    `^## Next Steps$` 1, `wc -l` STRICTLY under 50.

G5  The ledger append, as ONE equality over the whole file, in the
    shape constraint 7 states — name that paragraph, do not restate
    its formula. Report the boolean and the byte arithmetic. Report
    a SECOND, INDEPENDENT reading: split the C2 file on blank lines
    and confirm the LAST unit equals GATE7, with the unit count
    before and after. NEGATIVE CONTROL: flip ONE byte inside the
    appended paragraph in a disposable worktree; BOTH readers must
    reject the mutant and BOTH accept the true file.

G6  The sets, base versus C2 in `.agent/live_review.md`:
    `^- R-\d+ — ` 240 → 240 all DISTINCT, ids ADDED and ids REMOVED
    both the EMPTY SET, maximum `R-0679` → `R-0679`, `^Done: R-`
    2 → 2, `^Recurrence: R-` 15 → 15 UNCHANGED. `^Gate: R\d+ — `
    7 → 8, gaining exactly the key `R7`, with `R19`, `R1`, `R2`,
    `R3`, `R4`, `R5` and `R6` still present.

G7  Markers, paths, structure and hygiene. Line-anchored `^<<<SLICE `
    and `^<<<END ` both count 0 in `.agent/plan.md` at C1 and in
    `.agent/live_review.md` at C2. Report that
    `git diff --name-only <base>..C2` names NO path under
    `packages/`, `apps/`, `tests/` or `docs/`, and NEITHER
    `.agent/decisions.md` NOR `.agent/f031_inventory.md`. Over
    C0a..C2 report per commit that it is single-parent and its
    INSERTION count — the `+` column only, per AGENTS.md DECISION
    F104 D1 — each under 500. Report the range path set MINUS the
    change set (EMPTY) and the change set MINUS the range (exactly
    `.agent/handoff.md`, which C3 writes). Report
    `git ls-files .remedy-wt` as 0, `git ls-files` over `*.zip` as
    0, and `git worktree list` as 1 line. FOR THE REFLOG, state the
    SCOPE and the FIELD in the reading itself: over THIS ROUND'S
    entries only, read by the OPERATION PREFIX before the first
    colon of `git reflog --format=%gs`, report `amend`, `rebase` and
    `cherry` each 0, and how many entries you scoped to.

G8  The block's own object ids, and the suites. Extract every
    SHA-shaped token from the COMMITTED C0a blob with the
    word-bounded pattern `[0-9a-f]{7,40}` — whose boundaries do NOT
    match the 64-char sha256 digests this block also carries — and
    pass each to `git cat-file -t`. THE FAILING SET MUST BE EMPTY:
    this block quotes no non-existent id, so it has no positive
    control. Report the token count YOUR extractor measured, the
    failing set, and the type printed for each token. Then, with
    `git worktree list` reported as 1 line immediately BEFORE the
    first pytest command, run these SERIALLY in the PRIMARY checkout
    at the C2 tree, never two pytest processes at once, all exit 0:
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/cli/test_golden_path.py -q
    The reviewer executed all five at `3f3d3e8f` and measured, in
    that order, 474, 52, 21, 16 and 42, every one exit 0. Report
    yours against those and account for any difference.

G9  The push. AFTER C3, run
    `git push origin feature/f031-decision-inbox`. No `--force`, no
    `--force-with-lease`, no history rewrite, no branch deletion, no
    pull request. THIS GATE'S OUTCOME IS NOT A VALUE OF ANY FILE
    THIS ROUND WRITES, and its carrier is named here so you inherit
    ONE instruction rather than two: the reviewer measures the
    pushed tips at the next gate and records them in the R8 entry of
    `.agent/live_review.md`. In `## External actions` write the push
    COMMAND and that sentence — which is how this block satisfies
    `docs/agents/handback_template.md` and R-0679's fix clause
    together. Report the real outcome in your final message.

── Handback ──────────────────────────────────────────────────
Rewrite `.agent/handoff.md` at C3 per docs/agents/handback_template.md:
feature and round, branch, base and commit SHAs, a changed-files
table per commit, the item-status table covering C0a, C0b, C1, C2,
C3 and the push, ONE LINE PER GATE with its real result, the finding
counts, and the next expected action. Carry the `Fortschritt:` block
above VERBATIM — count its lines yourself and carry exactly those;
this block states no numeral for them.

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

THIS IS THE LAST ROUND OF THE SESSION. Your `## Next` section is the
only thing the next session reads first, so make it name, in order:
Phase 1 rule 1 (re-read `.agent/STOP` from disk), then that NO pull
request exists for this branch and none should be created yet, then
that R9 measures the UI inventory and rules the design gap the plan's
Risks names — the canonical design reference carries no inbox and no
decision component, so T002 has no visual authority until that ruling
lands — and then that R9's first commit also records the R8 verdict,
which by DECISION F085 D9 no artefact of this round can carry.

Declare every deviation, contradiction and assumption.
──────────────────────────────────────────────────────────────

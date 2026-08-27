── STEP R6 — F031 Decision inbox ─────────────────────────────
Goal:        Record the R5 verdict, register the one contradiction R5
             declared — which is the reviewer's own — and plan T001
             against the three rulings R5 landed, so the next round
             writes production code against a settled design. State
             only; no production path is touched.

Fortschritt: ~5 % (F031 claimed; R1 through R5 landed and gated · the
             source inventory and the three design rulings are on disk
             · T001 is planned and starts next · no T-slice shipped)
             — Schaetzung

Bundle:      C0a save this block · C0b mirror it into last_block ·
             C1 the plan · C2 the R5 gate entry and finding R-0679 ·
             C3 the handback.

Change set:  exactly these paths, nothing else —
             .agent/authored/f031-r6.md
             .agent/last_block.md
             .agent/plan.md
             .agent/live_review.md
             .agent/handoff.md
             This list bounds the round's WRITES, not its ACTIONS: the
             push named in gate G9 is ordered explicitly and is not a
             file (finding R-0674).

── Base ──────────────────────────────────────────────────────
The round base is `49c50d05d0b495a1534741d3fda4b6b68e2f4286`, the R5
handback commit and the current tip of `feature/f031-decision-inbox`.
Every SHA-shaped token in this block was passed to `git cat-file -t`
before emission and every one resolves — this block quotes no
non-existent id, so unlike R5's G11 it declares no positive control and
G8 orders the sweep with an EMPTY failure set. Stay on that branch;
create none, never commit to `main`.

Readings the reviewer MEASURED at that base, re-checkable there:
- `.agent/live_review.md`: `^- R-\d+ — ` 239 all DISTINCT, maximum
  `R-0678`; `^Done: R-\d+ — ` 2; `^Recurrence: R-` 14;
  `^Gate: R\d+ — ` 5, the keys `R19`, `R1`, `R2`, `R3` and `R4`.
- The §3 item 10 open set — every `^- R-\d+ — ` paragraph minus every
  `^Done: R-\d+ — ` line — is 239 − 2 = 237 at that commit.
- `.agent/plan.md` 48 lines. `.agent/handoff.md` 94 lines.

── Why this round exists ─────────────────────────────────────
R5 passed on every one of its thirteen gates under the reviewer's own
execution. Transport was proved in its STRONGEST form rather than by
the digest fallback: the reviewer's own scratch original still existed
at review time and is byte-identical to both committed blobs. C2
records that verdict.

R5 declared ONE contradiction and it is the reviewer's own. G13 of the
R5 block forbade the push's outcome from being a value of any file the
round writes, while `docs/agents/handback_template.md` requires the
`## External actions` section to carry every push as "command +
outcome". The two cannot both be satisfied, so the worker wrote the
command, withheld the result, marked the push row `deviated` for that
reason and invented nothing — which is the correct response and the
only reason nothing false reached the record. The open set was searched
for the DEFECT before the id was minted (§3 item 30); FIND679 names the
neighbouring entries and why none of them reaches it.

C1 plans T001. The three rulings R5 landed as DECISION F031 D1, D2 and
D3 settle what T001 must build, so the plan names the endpoint, the
blocked-size wiring and the fixture set rather than re-opening them.

── Constraints ───────────────────────────────────────────────
1. Apply every authored slice BYTE FOR BYTE. Never retype, rewrap,
   reflow or "fix" a slice. If a slice looks wrong, apply it verbatim
   and DECLARE the disagreement in the handback. A contradiction inside
   this block is the reviewer's defect, not yours: state it, reconcile
   nothing.
2. Slice transport. This block is saved verbatim as
   `.agent/authored/f031-r6.md` at C0a and mirrored byte-identically
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
6. The slices this block carries are the whole text PLANF031R6 and the
   two ledger paragraphs GATE5 and FIND679. This paragraph names them
   and states no count of them; G3 orders you to report the count YOUR
   extractor measured.
7. C2 appends GATE5 then FIND679 to `.agent/live_review.md` in that
   order, each separated from the preceding text and from each other by
   exactly one blank line, the file ending in exactly one newline. THIS
   BLOCK CARRIES NO FROM/TO PAIR, so no containment reading is owed and
   none is stated.
8. THIS ROUND MINTS EXACTLY ONE FINDING ID, `R-0679`, and changes no
   existing finding record. `^- R-\d+ — ` must be 239 before and 240
   after, and the maximum must move from `R-0678` to `R-0679`.
9. Do not touch any path under `packages/`, `apps/`, `tests/` or
   `docs/`, and do not touch `.agent/decisions.md` or
   `.agent/f031_inventory.md` — both are landed evidence and are
   corrected by dating in a later round, never by editing (§3 item 20,
   findings R-0417 and R-0525).
10. Destructive verification, if any, runs ONLY in a disposable
    `git worktree` under `.remedy-wt/`, removed BY ITS EXACT PATH
    (R-0662) and BEFORE the G7 suites. Note that
    `.remedy-wt/dry` is a PRE-EXISTING scratch directory belonging to
    no round of this feature: do not create a worktree at that path, do
    not read from it and do not delete it.

── Authored slices ───────────────────────────────────────────

<<<SLICE PLANF031R6
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the merge
commit of pull request #213 which closed F022. `.agent/live_review.md` is the
source of truth for the record and the finding-id ceiling;
`.agent/f031_inventory.md` is the measured source inventory; `.agent/decisions.md`
carries DECISION F031 D1, D2 and D3, which settle the design.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact. DONE when the inbox lists fixture
decisions of every PRODUCING type with correct blocked-size math, answering from
a card round-trips through the write channel into the same effects the CLI
produces, the badge tracks live, and ordering follows a documented rule over age
and blocked size rather than vibes.

## Current Step
R6 records the R5 verdict, registers finding R-0679, and plans T001. It writes no
production code: the next round is the first of this feature to do so.

## Next Steps
1. R7 builds T001 against the rulings: a read endpoint that derives its cards
   from `list_decisions` in `packages/orchestration/decision_queue.py` (D1 — the
   queue is a derived view, so no storage is added), carrying per card the type,
   the age, and a blocked count wired from `blocked_downstream` in
   `packages/orchestration/dag_schedule.py`, which no decision reads today.
2. R7 ships contract tests with a fixture per PRODUCING type — the eight types a
   branch of `list_decisions` emits (D3), NOT the ten of `DECISION_TYPES` — plus
   the scoping rule and the unreadable-entry honesty the feature file requires.
3. R8 records the R7 verdict and plans T002, where D2 binds: the badge
   re-derives on refetch over the existing stream and no new event kind ships.

## Risks
- Open findings, stated with the rule and the commit DECISION F009 D10 requires:
  by §3 item 10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — `
  line — the open set is 237, measured at `49c50d05`.
- The findings THIS FEATURE MUST STILL ACT ON — a narrower set, named as what it
  is and not called "open" — are R-0403, R-0413, R-0431, R-0445, R-0495, R-0533,
  R-0574, R-0601, R-0625, R-0632, R-0672, R-0674, R-0675, R-0676, R-0677, R-0678
  and R-0679, of which R-0495 and R-0574 are the two Highs, inherited from F085
  and F086.
- T001 IS THE FIRST ROUND OF THIS FEATURE TO TOUCH PRODUCTION CODE, so it is a
  SPLIT round by the §3 Round-types rule and its gates grow accordingly: the
  suites this feature has been running are state readers and will not exercise a
  new endpoint. R7's block must add the suite that does.
- The record holds `Gate: R19` from F022 as its seed entry. If F031 reaches its
  own R19 that key collides — the §3 item 26 defect. A round before then renames
  the seed or the scheme; this bullet is the reminder.
<<<END PLANF031R6

<<<SLICE GATE5
Gate: R5 — the F031 R5 entry. R5 PASSED ON EVERY ONE OF ITS THIRTEEN GATES, AND THE REVIEWER RE-RAN EVERY ONE OF THEM ITSELF RATHER THAN READING THE HANDBACK'S WORD FOR ANY OF THEM; every value the handback states reproduced exactly, and the round's one declared contradiction is the reviewer's own, registered below as R-0679. TRANSPORT HELD IN ITS STRONGEST FORM RATHER THAN BY THE DIGEST FALLBACK: the reviewer's own scratch original at `.remedy-wt/f031-r5.md`, the committed C0a blob at `af048031`, the committed C0b blob at `d97c1d18` and `.agent/last_block.md` off disk are ALL sha256 `be41960e388ce8d3838aa44164dae902ce103d8b1b60188f02db28d64c763154` over 35476 bytes and 488 lines, and C0a and C0b resolve to the SAME git blob `30bc5a77` — the reviewer compared its OWN pre-emission bytes to the committed ones, which is the primary proof shape §4 item 9 asks for and which most rounds cannot produce. THE EXTRACTION printed 5 slices across 200 content lines against 488 total. `.agent/plan.md` at `cefcbbb4` is 2816 bytes and 48 lines, byte-equal to PLANF031R5 under the newline-INCLUDED convention with the trailing-newline-removed control FALSE, `^## Goal$` and `^## Next Steps$` once each, strictly under the cap of 50. THE LEDGER APPEND HELD UNDER A STRICTER READING THAN THE GATE ORDERED: at `f05d00c5` the file is EXACTLY the base blob plus one newline plus GATE4 plus one newline plus FIND678, an equality that fixes position and content together, 539793 bytes to 546250 with the delta 6457 equal to 1 plus 3974 plus 1 plus 2481; an independent blank-line split went 277 units to 279 with the LAST TWO equal to GATE4 then FIND678 IN ORDER; and the reviewer flipped its own byte at offset 539994 inside the FIRST appended paragraph, which BOTH readers rejected while BOTH accepted the true file. THE SETS MOVED ONLY WHERE CONSTRAINT 8 ALLOWED: `^- R-\d+ — ` 238 to 239 all DISTINCT, ids ADDED exactly the one id `R-0678`, ids REMOVED the EMPTY SET, maximum `R-0677` to `R-0678`, `^Done: R-` 2 to 2, `^Recurrence: R-` 14 to 14 UNCHANGED, and `^Gate: R\d+ — ` 4 to 5 gaining exactly the key `R4`. THE TWO OTHER APPENDS HELD TO THE SAME EQUALITY: `.agent/decisions.md` at `b97e823e` is exactly its base blob plus one newline plus DEC031 plus one newline, with `^## DECISION F031 D` going 0 to 3 and each of the D1, D2 and D3 headers occurring exactly once — the §3 item 26 comparison against that file's existing `## DECISION <feature> D<n>` series; and `docs/roadmap/features/T5_F031.md` at `a8ec4e07` is exactly its base blob plus one newline plus FEATAMEND plus one newline, with `^## Design amendments ` going 0 to 1. MARKERS WERE LINE-ANCHORED 0 in all four targets at their own commits, and the six-path range holds nothing under `packages/`, `apps/` or `tests/`, not `README.md`, neither `docs/roadmap/ROADMAP.md` nor `docs/roadmap/STATUS.md`, and not `.agent/f031_inventory.md`. STRUCTURE HELD: seven commits from `f4311bf6` to `49c50d05`, each single-parent, insertions 488, 358, 27, 4, 121, 31 and 64, each under the 500 cap; over the full range the path set MINUS the change set and the change set MINUS the path set are BOTH EMPTY; `git ls-files .remedy-wt` 0, the zip glob 0, one worktree, `git status --porcelain` 0. THE REFLOG READING STATES ITS OWN SCOPE AND FIELD: over the 7 entries of this round's own range, read by the OPERATION PREFIX before the first colon of `git reflog --format=%gs`, every prefix is `commit`, so amend 0, rebase 0 and cherry 0. THE BLOCK'S OWN OBJECT IDS WERE SWEPT, which is the R-0678 discipline applied to the block that registered it: 23 occurrences over 11 distinct word-bounded hex tokens, every one resolving under `git cat-file -t` except exactly the id FIND678 QUOTES as its evidence — the gate's positive control, which proves the pattern matched rather than silently finding nothing. THE SEVEN SUITES ARE THE REVIEWER'S OWN, run SERIALLY with never two pytest processes alive, every one REAL exit code 0 at 470, 52, 21, 16, 42, 295 and 30 — the first five reproducing the previous readings cell for cell and the last two summing to the 325 the reviewer measured at the base before ordering them, so the feature-file append turned nothing red. THE PUSH DISCHARGED: local and remote tips are both `49c50d05d0b495a1534741d3fda4b6b68e2f4286`; no pull request, nothing merged. THE HANDBACK DERIVED ITS OWN CAP rather than quoting one, reading the tier as 100 from the seven commits constraint 3 fixes, landing at 94 lines with no DECISION D15 overage owed, no section dropped and no token cap claimed. THE VERDICT IS PASS.
<<<END GATE5

<<<SLICE FIND679
- R-0679 — Low, A BLOCK FORBADE A VALUE THAT THE HANDBACK TEMPLATE INDEPENDENTLY MANDATES, SO THE TWO TEXTS GOVERNING ONE SECTION COULD NOT BOTH BE OBEYED. Raised by the reviewer at the F031 R5 gate against the reviewer's own R5 block, after the worker declared it. THE INSTANCE: G13 of that block reads "This gate's outcome is REPORTED TO THE REVIEWER and is NOT a value of any file this round writes", while `docs/agents/handback_template.md` requires the `## External actions` section to record "Every push, PR create/edit/merge, gh command, worktree add/remove — command + outcome". The push is the last act of the round and the handback is written by the commit before it, so the outcome cannot be a value of that file; but the template mandates it, and a block may not silently overrule a document it does not amend. THE WORKER RESOLVED IT THE RIGHT WAY ROUND: it wrote the command, withheld the result, marked the push row `deviated` naming this reason rather than a failure, and invented nothing — so nothing false reached the record and the round paid one declared deviation for the reviewer's error. WHY LOW: the property the template protects is not lost, only relocated. The push outcome is measured by the reviewer at the next gate and recorded in the ledger entry for that round — this entry's own predecessor states the discharged push and the equal local and remote tips for R4, and the R5 entry above does the same — so the value survives in an append-only file rather than in a rewritten one, which is strictly the better carrier. THE OPEN SET WAS SEARCHED FOR THE DEFECT BEFORE THIS ID WAS MINTED (§3 item 30), and the three nearest entries each stop short. R-0371 and R-0449 bar ordering a value INTO an artifact that is written before the value can exist, and G13 OBEYS them — it is the counter-measure those findings prescribe, correctly applied. R-0494 governs a reading routed to a "round report" that dies with the session, and G13 does not lose the value, because the reviewer records it in the ledger. R-0592 and §3 item 28 govern a value the worker must write TWICE, where a gate reaches one copy and not the other; here the block forbids the single write the template requires, which is the inverse shape and is reached by none of them. THE FIX, binding on every block from here: where a block's gate withholds a value that a mandated handback section requires, the gate SAYS SO IN THE SAME CLAUSE and names the artifact that will carry it instead — "the outcome is not a value of this file; the reviewer records it in the next round's ledger entry" — so the worker reads one instruction rather than two contradictory ones and spends no deviation proving the reviewer's texts disagree. A bare prohibition against a standing template is a contradiction the worker inherits; a prohibition that names its replacement carrier is an instruction. OPEN.
<<<END FIND679

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
    readings: `.remedy-wt/f031-r6.md` before C0a, the committed C0a
    blob, the committed C0b blob, and `.agent/last_block.md` off disk
    after C0b. All four must be EQUAL. Report the git blob id of C0a's
    and C0b's file; they must be the SAME id.

G3  Extraction. Run your extractor over the COMMITTED C0a blob and
    report the slice count, the CONTENT lines inside markers, and the
    TOTAL line count. Report the numbers YOUR extractor printed.

G4  The plan. `.agent/plan.md` at C1 is byte-equal to PLANF031R6 under
    your stated newline convention; report the slice length, the file
    length and the convention. NEGATIVE CONTROL: the file is NOT
    byte-equal to the same slice with its trailing newline REMOVED.
    `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` STRICTLY under 50.

G5  The ledger append, as an EQUALITY rather than two region checks.
    Report that `.agent/live_review.md` at C2 is byte-for-byte the base
    blob, then one newline, then GATE5, then one newline, then FIND679,
    then one newline — one boolean over the whole file, which fixes
    position and content together. Report the byte arithmetic beside
    it. Report a SECOND, INDEPENDENT reading: split the C2 file on
    blank lines and confirm the LAST TWO units equal the two slices IN
    ORDER; report the unit count before and after. NEGATIVE CONTROL:
    flip ONE byte inside the FIRST appended paragraph in a disposable
    worktree and report that BOTH readers reject the mutant while BOTH
    accept the true file.

G6  The sets. In `.agent/live_review.md`, the round base versus C2:
    `^- R-\d+ — ` 239 → 240 all DISTINCT, ids ADDED exactly the one id
    `R-0679`, ids REMOVED the EMPTY SET, maximum `R-0678` → `R-0679`,
    `^Done: R-` 2 → 2, `^Recurrence: R-` 14 → 14 UNCHANGED.
    `^Gate: R\d+ — ` 5 → 6, gaining exactly the key `R5`, with `R19`,
    `R1`, `R2`, `R3` and `R4` still present.

G7  Markers, paths, structure and hygiene. Line-anchored `^<<<SLICE `
    and `^<<<END ` both count 0 in `.agent/plan.md` at C1 and in
    `.agent/live_review.md` at C2. Report that
    `git diff --name-only <base>..C2` names NO path under `packages/`,
    `apps/`, `tests/` or `docs/`, and names NEITHER
    `.agent/decisions.md` NOR `.agent/f031_inventory.md`
    (constraint 9). Over C0a..C2 report per commit that it is
    single-parent and its INSERTION count — the `+` column only, per
    AGENTS.md DECISION F104 D1 — each under 500. Report the range path
    set MINUS the change set (must be EMPTY) and the change set MINUS
    the range (must be exactly `.agent/handoff.md`, which C3 writes).
    Report `git ls-files .remedy-wt` as 0, `git ls-files` over the
    pattern `*.zip` as 0, and `git worktree list` as 1 line. FOR THE
    REFLOG, state the SCOPE and the FIELD in the reading itself: over
    THIS ROUND'S reflog entries only, read by the OPERATION PREFIX
    before the first colon of `git reflog --format=%gs`, report
    `amend`, `rebase` and `cherry` each 0, and report how many entries
    you scoped the reading to.

G8  The block's own object ids. Extract every SHA-shaped token from the
    COMMITTED C0a blob with the word-bounded pattern `[0-9a-f]{7,40}`,
    which by its boundaries does NOT match the 64-character sha256
    digests this block also carries, and pass each to
    `git cat-file -t`. THE SET OF TOKENS THAT FAIL MUST BE EMPTY —
    this block, unlike R5's, quotes no non-existent id, so it has no
    positive control and an empty failure set is the expected reading.
    Report the token count YOUR extractor measured, the failing set,
    and the type `git cat-file -t` printed for each token.

G9  Suites, run SERIALLY, never two pytest processes at once, in the
    PRIMARY checkout at the C2 tree, with `git worktree list` reported
    as 1 line immediately BEFORE the first pytest command. All must
    exit 0; report the real exit code and the counts:
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/cli/test_golden_path.py -q
    The reviewer executed all five at `49c50d05` with no worktree
    present and measured, in the order listed: 470, 52, 21, 16 and 42,
    every one exit 0. Report yours against those and account for any
    difference. `tests/docs/` and `tests/orchestration/test_roadmap_index.py`
    are NOT ordered: no `docs/` path is in this round's change set.

G10 The push. AFTER C3, run `git push origin feature/f031-decision-inbox`.
    No `--force`, no `--force-with-lease`, no history rewrite, no branch
    deletion, no pull request. THIS GATE'S OUTCOME IS NOT A VALUE OF ANY
    FILE THIS ROUND WRITES, and the artifact that carries it instead is
    named here so you inherit ONE instruction rather than two: the
    reviewer measures the pushed tips at the next gate and records them
    in the R6 entry of `.agent/live_review.md`. In `## External actions`
    write the push COMMAND and that sentence, which is how this block
    satisfies `docs/agents/handback_template.md` and finding R-0679's
    fix clause together. Report the real outcome to the reviewer in your
    final message.

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
Phase 1 rule 1 (re-read `.agent/STOP` from disk), then that NO pull
request exists for this branch and none should be created yet, then
that R7 builds T001 as the plan's Next Steps describe and is the first
round of this feature to touch production code — so it is a SPLIT round
whose block must add the suite that exercises the new endpoint — then
that R7's first commit also records the R6 verdict, which by DECISION
F085 D9 no artefact of this round can carry.

Declare every deviation, contradiction and assumption.
──────────────────────────────────────────────────────────────

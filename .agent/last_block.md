── STEP R2 — F031 Decision inbox ─────────────────────────────
Goal:        Record the F031 R1 verdict on disk, register the two
             RECURRENCES that round's review surfaced — both of them
             reviewer-block defects, neither a new id — and correct the
             plan's open-set wording against the DECISION that already
             rules it. State only, no production code.

Fortschritt: ~0 % (F031 claimed; R1 landed and is gated here · no
             T-slice started · the decision-inbox inventory is R3) —
             Schaetzung

Bundle:      C0a save this block · C0b mirror it into last_block ·
             C1 the corrected plan · C2 the R1 gate entry and the two
             recurrence paragraphs · C3 the handback.

Change set:  exactly these paths, nothing else —
             .agent/authored/f031-r2.md
             .agent/last_block.md
             .agent/plan.md
             .agent/live_review.md
             .agent/handoff.md
             This list bounds the round's WRITES, not its ACTIONS: the
             push named in gate G10 is ordered explicitly and is not a
             file (finding R-0674).

── Base ──────────────────────────────────────────────────────
The round base is `ae5e989de8e92b09272341e988faf98b54dfed75`, the C5 of
F031 R1 and the tip of `feature/f031-decision-inbox`, which is also the
remote tip. Stay on that branch; create none, and never commit to
`main`.

Every reading this block states about the base was MEASURED by the
reviewer at `ae5e989d`:
- `.agent/live_review.md`: `^- R-\d+ — ` 238 records all DISTINCT with
  maximum `R-0677`; `^Done: R-\d+ — ` 2, naming `R-0653` and `R-0670`;
  `^Recurrence: R-` 11; `^Gate: R\d+ — ` exactly 1, the key `R19`.
- The §3 item 10 open set — every `^- R-\d+ — ` paragraph minus every
  `^Done: R-\d+ — ` line — is 238 − 2 = 236 at that commit.
- `R-0632` is present as a record and is NOT named by any `Done:` line,
  so it is open by item 10.
- `.agent/plan.md`: 44 lines.

── Why this round exists ─────────────────────────────────────
The reviewer re-ran every one of R1's thirteen gates itself and all
thirteen reproduced, so R1's verdict is PASS and C2 records it. The
review ALSO found two defects, and both are the reviewer's own, in text
the reviewer authored into the R1 block:

(a) The R1 block's Handback paragraph resolved the two-tier handback cap
    to 60 lines "because this round has fewer than six per-commit
    tables", over a round whose own constraint 3 fixes SEVEN commits.
    That is finding R-0676's exact class, one feature after it was
    registered and one round after its counter-measure was reported
    working.
(b) The R1 block's plan slice states that the open set is "NOT
    mechanically derivable" and routes the ruling to R3. That is false
    on disk: DECISION F009 D10 in `.agent/decisions.md` already rules
    it, and finding R-0632 — which is OPEN — already registers the
    defect. The same plan slice and the R1 handback then each called a
    twelve-id set "open" without the rule and commit D10 requires.

NEITHER MINTS AN ID. The open set was searched for both defects before
this block was written (§3 item 30): R-0676 already holds (a) and
R-0632 already holds (b), so each is recorded as a `Recurrence:`
paragraph that extends its finding's counter-measure, and the record's
`^- R-\d+ — ` count does not move this round.

── Constraints ───────────────────────────────────────────────
1. Apply every authored slice BYTE FOR BYTE. Never retype, rewrap,
   reflow or "fix" a slice. If a slice looks wrong, apply it verbatim
   and DECLARE the disagreement in the handback. A contradiction inside
   this block is the reviewer's defect, not yours: state it, reconcile
   nothing.
2. Slice transport. This block is saved verbatim as
   `.agent/authored/f031-r2.md` at C0a and mirrored byte-identically
   into `.agent/last_block.md` at C0b. Extract every slice
   PROGRAMMATICALLY out of the COMMITTED C0a blob by its marker LINES —
   a line equal to `<<<SLICE <NAME>` opens it, a line equal to
   `<<<END <NAME>` closes it — never by hand and never from this
   prompt. Marker lines never reach a target file.
3. Commit sequence, exactly: C0a, C0b, C1, C2, C3. No extra commit,
   none dropped, no reordering. If you must correct a landed commit, do
   NOT add a commit outside this sequence — declare it instead (finding
   R-0675). The push runs after C3.
4. Never amend, rebase, cherry-pick, force-push or rewrite history;
   never delete a branch; never merge anything; create no pull request.
5. `git status --porcelain` prints 0 lines after every commit. Read
   `.agent/STOP` from disk before C0a and again before C3; if it exists
   at either point, finish the commit in hand, write the handback and
   stop (guardrail G6).
6. The slices this block carries are the whole text PLANF031R2 and the
   three appended paragraphs GATE1, RECUR632 and RECUR676. This
   paragraph names them and states no count of them; G3 orders you to
   report the count YOUR extractor measured.
7. C2 appends GATE1, RECUR632 and RECUR676 to `.agent/live_review.md`
   in that order, each separated from the preceding text and from each
   other by exactly one blank line, the file ending in exactly one
   newline. This block carries no FROM/TO pair, so no containment
   reading is owed and none is stated.
8. This round MINTS NO FINDING ID. `^- R-\d+ — ` must be 238 before and
   238 after, and the maximum id must be `R-0677` before and after. A
   new `- R-XXXX` record appearing in C2 is a failure of this round,
   not a bonus.
9. Destructive verification, if you run any, happens ONLY inside a
   disposable `git worktree` under `.remedy-wt/`. Remove it BY ITS
   EXACT PATH, never by a glob (finding R-0662), and remove it BEFORE
   the G9 suites run — with a worktree present,
   `tests/orchestration/test_test_runner.py::`
   `TestVitestFrontendTestFoundation::test_vitest_passes` fails because
   `npx vitest run` finds the worktree's own `apps/ui/vitest.config.ts`
   and no worktree carries `node_modules` (the R-0518 shape). The
   reviewer measured that red and then measured 52 passed with no
   worktree present, both at `6325ac2f`.
10. Do not touch `docs/`, `README.md`, `.agent/context.md`,
    `.agent/candidates.md` or `.agent/decisions.md` this round. The
    ruling this round applies is DECISION F009 D10, which is ALREADY on
    disk; nothing new is decided, so nothing is written to the decision
    log.

── Authored slices ───────────────────────────────────────────

<<<SLICE PLANF031R2
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
R2 records the F031 R1 verdict — PASS on all thirteen gates, each re-run by the
reviewer — and registers the two recurrences that review surfaced, R-0632 and
R-0676, both reviewer-block defects and neither a new id.

## Next Steps
1. R3 takes the decision-inbox inventory in the source and MEASURES each part:
   the file-based queue store and its CLI, every producer that writes a
   decision, the DAG module's blocked-subtree entry point, and the decision
   event kinds the stream carries today on the Python and the TypeScript side.
2. R3 also settles whether F050 and F051 are built, since F031 depends on both.
3. T001 follows the feature file's Task slicing once that inventory is on disk.

## Risks
- Open findings, stated with the rule and the commit DECISION F009 D10 requires:
  by §3 item 10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — `
  line — the open set is 236 measured at `ae5e989d`. R1's plan and handback each
  called a twelve-id set "open" unqualified, which D10 forbids and which the
  R-0632 recurrence this round records.
- The findings THIS FEATURE MUST STILL ACT ON — a narrower set, named as what it
  is and not called "open" — are R-0403, R-0413, R-0431, R-0445, R-0495, R-0533,
  R-0574, R-0625, R-0672, R-0674, R-0675, R-0676, R-0677 and R-0632. R-0495 and
  R-0574 are the two Highs, both inherited from the closed F085 and F086.
- The record now holds `Gate: R19` from F022 as its seed entry. If F031 reaches
  its own R19, that key collides and the ledger gains two paragraphs answering
  to one key — the §3 item 26 defect. A round before then renames the seed or
  the scheme; this bullet is the reminder, measured at `ae5e989d`.
<<<END PLANF031R2

<<<SLICE GATE1
Gate: R1 — the F031 R1 entry. R1 PASSED ON EVERY ONE OF ITS THIRTEEN GATES, AND THE REVIEWER RE-RAN EVERY ONE OF THEM ITSELF RATHER THAN READING THE HANDBACK'S WORD FOR ANY OF THEM. THE ROUND'S SUBSTANCE IS THE CLAIM OF F031 AND THE DISCHARGE OF F022'S CLOSURE: the STATUS line moved to `[~]`, the review record was reset for the new feature, the F022 R19 verdict was written into it, the one candidate F022 carried became `R-0677`, and the candidate carrier is EMPTY. TRANSPORT HELD IN ITS STRONGEST FORM: the reviewer's own scratch original at `.remedy-wt/f031-r1.md`, the committed C0a blob, the committed C0b blob and `.agent/last_block.md` read off disk are ALL sha256 `81b1ef8a490792e091c1c24857cdc6b921fbe322743e2ccf77b2a08fb51b0864` over 30543 bytes and 404 lines, and C0a and C0b resolve to the SAME git blob `fa6194d5` — four readings including the reviewer's own pre-delegation copy, which is the strongest form this workflow can produce, because it proves the bytes the reviewer authored are the bytes that landed. THE EXTRACTION over the committed C0a blob printed 9 slices across 127 content lines against 404 total, reproducing the worker's reading exactly. THE WHOLE-FILE WRITES ARE BYTE-EXACT under the worker's stated newline convention and under the reviewer's independent one: `.agent/plan.md` at `5abc41ed` is 2491 bytes with `^## Goal$` 1, `^## Next Steps$` 1 and 44 lines strictly under the cap of 50; `.agent/candidates.md` at `6dab419d` is 634 bytes carrying `^EMPTY\.` 1 and `^NON-EMPTY\.` 0 and naming `R-0677`; `.agent/context.md` at `6dab419d` is 2139 bytes with its F031 heading once — and every trailing-newline-removed control printed FALSE, so each equality distinguishes the two candidates rather than accepting both. THE ONE PAIR WAS MEASURED, NOT ASSERTED: STATUSFROM 1 at `6325ac2f` to 0 at C2 and STATUSTO 0 to 1, one application, `^- \[~\] F\d+ — ` 0 to 1 and `^- \[x\] F\d+ — ` 57 to 57 UNCHANGED, and the reviewer's own script printed TRUE for "the C2 file equals the base blob with only that one replacement applied". THE SCRIPTED RECORD REBUILD DID EXACTLY WHAT CONSTRAINT 10 ALLOWED AND NOTHING MORE, which is the round's one genuinely destructive act and therefore the one that needed the strongest proof: `^Gate: R\d+ — ` went 19 to exactly 1 and that key is `R19`; the F031 title appears once and no F022 title survives; `^## Steps$` and `^## Findings$` are 1 each; and the finding records went 237 to 238 with ids REMOVED the EMPTY SET, ids ADDED exactly `R-0677`, maximum `R-0676` to `R-0677`, `^Done: R-` 2 to 2 and `^Recurrence: R-` 11 to 11. Not one finding record was pruned by a rebuild that deleted 99128 bytes. THE TWO APPENDS LANDED REGION-EXACT and the reviewer ran its OWN mutant control beside the worker's, flipping a byte inside the first appended paragraph and confirming the equality check rejects the mutant while accepting the true file. STRUCTURE HELD: seven commits, every one single-parent, insertions 404, 385, 35, 1, 24, 24 and 62, each far under the 500 cap; the range path set MINUS the change set is EMPTY and the change set MINUS the range is EMPTY once the handback commit is counted; the anchored markers `^<<<SLICE ` and `^<<<END ` are 0 in all five edited files; `git ls-files .remedy-wt` 0 and `git ls-files` over the zip glob 0; one worktree; `git status --porcelain` 0; and the reflog OPERATION field carries amend 0, rebase 0 and cherry 0. THE SEVEN SUITES ARE THE REVIEWER'S OWN, run serially with never two pytest processes alive, every one exit 0 and every count identical to the base readings the block ordered them against: 295, 30, 470, 52, 21, 16 and 42. THE PUSH DISCHARGED and the remote tip equals the local tip at `ae5e989d`; no pull request was created and nothing was merged. THE HANDBACK'S OWN NUMBERS WERE AUDITED RATHER THAN READ: every `+/-` cell of its `## Commits` tables was re-derived with `git diff --numstat` and all eight agree cell for cell, which is §3 item 28's obligation and the half a later session actually reads. THE VERDICT IS PASS. THE ROUND'S ONE DECLARED CONTRADICTION IS THE REVIEWER'S AND IT IS CORRECT: the block resolved the handback cap to its 60-line tier over a round its own constraint 3 fixes at seven commits, the worker refused to reconcile it, wrote every mandated table, measured 95 lines against the 100-line tier that actually applies and claimed no overage — which is the R-0676 class recurring, recorded in the paragraph below. A SECOND REVIEWER DEFECT THE WORKER COULD NOT HAVE SEEN is recorded in the paragraph after it: the block's plan slice asserted that the open set is not mechanically derivable and routed the ruling forward, over a repository where DECISION F009 D10 had already ruled it.
<<<END GATE1

<<<SLICE RECUR632
Recurrence: R-0632 — AN AUTHORED TEXT CALLED A NARROW SET OF FINDINGS "OPEN" WITHOUT THE RULE AND THE COMMIT, AND A SECOND TEXT DENIED THAT ANY DERIVATION EXISTS. SECOND INSTANCE, at F031 R1, and it is the reviewer's own. NO NEW ID IS MINTED: R-0632 already registers that "N findings are open" carries at least three live meanings in this repository, and DECISION F009 D10 — committed beside it and still on disk — already rules the answer. THE MEASUREMENT, taken by the reviewer at `ae5e989d`: the §3 item 10 open set is every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line, which is 238 − 2 = 236. The R1 plan slice's Risks section instead says "The open set carried into F031 is" twelve named ids "plus R-0677", and the R1 handback says "Open findings: 13" — both naming the narrow per-feature set, both calling it "open" unqualified, and neither stating the rule or the commit, which is precisely the sentence shape D10 forbids. WHAT MAKES THIS WORSE THAN THE FIRST INSTANCE, and worth a paragraph rather than a shrug: the same plan slice also states that the set "is NOT mechanically derivable from `.agent/live_review.md`" and routes the ruling to a later round, so the reviewer did not merely restate an unqualified count — it asserted the absence of a ruling that had been on disk since 2026-08-21 and scheduled work to produce it again. R-0632's own body names item 10 as "THE ONLY WRITTEN RULE", so the record contradicted the block on the page. THE CAUSE IS THE ONE R-0632 PREDICTS: the reviewer derived the set by reading the PREVIOUS feature's plan rather than the record, which is also exactly what §3 item 10's last sentence forbids, and the record's lack of a per-paragraph resolution marker made the wrong route the easy one. NO LANDED TEXT IS REWRITTEN — R1's handback is corrected by dating, not editing (R-0417, R-0525) — but `.agent/plan.md` is rewritten every round by construction, so C1 of this round states the item 10 count with its rule and its commit and names the narrower set as "the findings this feature must still act on". THE COUNTER-MEASURE IS EXTENDED, binding on every block from here: a block that states any finding count states the RULE that produced it and the COMMIT it was measured at in the SAME sentence, and a block that proposes to RULE something first greps `.agent/decisions.md` for a DECISION already ruling it and names what it found. D10 existed, was searched for by nobody, and was contradicted by the round that most needed it.
<<<END RECUR632

<<<SLICE RECUR676
Recurrence: R-0676 — A BLOCK RESOLVED A TWO-TIER REPOSITORY CAP TO ITS STRICTER TIER BY HAND-COUNTING ITS OWN COMMITS AND GETTING THE COUNT WRONG. SECOND INSTANCE, at F031 R1, and it is the reviewer's own — one round after the R18 gate entry recorded this finding's counter-measure "working the first time it was tried". NO NEW ID IS MINTED: R-0676 already rules this class, and its first instance was also a SEVEN-commit round, so this is the same defect at the same arity rather than a new shape. THE MEASUREMENT, taken at `ae5e989d`: the R1 block's Handback paragraph reads "The 60-line cap applies (this round has fewer than six per-commit tables)", while that same block's constraint 3 fixes the sequence C0a, C0b, C1, C2, C3, C4, C5 — seven commits — and its own Handback sentence orders an item-status table covering all seven. AGENTS.md under `### handoff.md` reads "≤60 lines (≤100 when per-commit tables of >5 commits require it)", so the condition is TRUE and the applicable tier is 100. THE WORKER RESOLVED IT THE RIGHT WAY ROUND and declared it: it named both readings, said which it was writing against, wrote every mandated table, measured its handback at 95 lines and claimed NO DECISION D15 overage — so unlike the first instance, no false deviation reached the permanent record, and the only cost is a wrong rule quotation in a block. WHY IT RECURRED IS THE PART WORTH RECORDING: R-0676's counter-measure was for a block to quote the correct tier, which leaves the reviewer hand-counting its own commit sequence at the moment it is least able to — the sequence is fixed in constraint 3, fifty lines away from the Handback paragraph that counts it, which is the §3 item 16 "resolve every count to the list it NAMES" shape arriving inside the counter-measure for a different finding. A rule that requires a correct hand count has the same failure mode as the count it replaced. THE COUNTER-MEASURE IS REPLACED, not merely restated, and binds every block from here: a block states NO handback line cap and NO tier. It orders the worker to resolve the tier itself from AGENTS.md against the commit count the block's own sequence constraint fixes, and to report both the count it derived and the tier that follows. The number then comes from the actor that can count the commits after they exist, which is the same reasoning §3 item 31 already applies to every other value a handback must carry.
<<<END RECUR676

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
    readings: `.remedy-wt/f031-r2.md` as it exists before C0a, the
    committed C0a blob, the committed C0b blob, and `.agent/last_block.md`
    off disk after C0b. All four must be EQUAL. Report the git blob id
    of C0a's and C0b's file; they must be the SAME id.

G3  Extraction. Run your extractor over the COMMITTED C0a blob and
    report the number of slices it found, the CONTENT lines inside
    markers, and the file's TOTAL line count. Report the numbers YOUR
    extractor printed; this block states none of them.

G4  The plan. `.agent/plan.md` at C1 is byte-equal to PLANF031R2 under
    your stated newline convention; report the slice length, the file
    length and the convention. NEGATIVE CONTROL: the file is NOT
    byte-equal to the same slice with its trailing newline REMOVED.
    `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` STRICTLY under 50.

G5  The three appends land byte-exact. For GATE1, RECUR632 and RECUR676
    separately, report that the corresponding region of
    `.agent/live_review.md` at C2 equals the extracted slice bytes, and
    report the byte arithmetic: base length, C2 length, and the
    difference against the three slice lengths plus your separators.
    Report that the base blob is a byte-exact PREFIX of the C2 file.
    Report a SECOND, INDEPENDENT reading: split the C2 file on blank
    lines, and confirm the LAST three units equal the three slices IN
    ORDER; report the unit count before and after. NEGATIVE CONTROL:
    flip ONE byte inside the FIRST appended paragraph in a disposable
    worktree and report that BOTH readers reject the mutant while BOTH
    accept the true file.

G6  The sets moved only where constraint 8 allows. In
    `.agent/live_review.md`, base `ae5e989d` versus C2: `^- R-\d+ — `
    238 → 238 with ids ADDED the EMPTY SET and ids REMOVED the EMPTY
    SET, all DISTINCT at both, maximum `R-0677` → `R-0677` UNCHANGED.
    `^Done: R-` 2 → 2. `^Recurrence: R-` 11 → 13, gaining exactly one
    `R-0632` line and one `R-0676` line. `^Gate: R\d+ — ` 1 → 2,
    gaining exactly the key `R1`, with `R19` still present. Report each
    reading as a before/after pair.

G7  Markers never reach a target. Line-anchored `^<<<SLICE ` and
    `^<<<END ` both count 0 in `.agent/plan.md` and in
    `.agent/live_review.md` at C2.

G8  Structure and hygiene, over C0a..C2. Report per commit: that it is
    single-parent, and its INSERTION count — the `+` column only, per
    AGENTS.md DECISION F104 D1 — each under 500. Report the range path
    set MINUS the change set (must be EMPTY) and the change set MINUS
    the range (must be exactly `.agent/handoff.md`, which C3 writes).
    Report `git ls-files .remedy-wt` as 0, `git ls-files` over the
    pattern `*.zip` as 0, `git worktree list` as 1 line, and the reflog
    OPERATION field over this round's rows with amend, rebase and
    cherry each 0.

G9  Suites, run SERIALLY, never two pytest processes at once, in the
    PRIMARY checkout at the C2 tree, with `git worktree list` reported
    as 1 line immediately BEFORE the first pytest command. All must
    exit 0; report the real exit code and the counts:
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/cli/test_golden_path.py -q
    The reviewer executed all five at `6325ac2f` with no worktree
    present and measured, in the order listed: 470, 52, 21, 16 and 42,
    every one exit 0. Report yours against those and account for any
    difference. `tests/docs/` and the roadmap index are NOT ordered
    this round: no `docs/` path is in the change set.

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
and the tier that follows from it. If the MANDATED content genuinely
does not fit that tier, exceed it and carry a DECISION D15 "Deviations,
declared" line naming your measured line count and the specific mandated
content that caused the overage. Never drop a mandated section to fit.
Do NOT claim compliance with any token cap: that cap was withdrawn.

Any finding count you state carries the RULE that produced it and the
COMMIT it was measured at, in the same sentence, per DECISION F009 D10.
A narrower set is named as "the findings this feature must still act on"
and is never called "open" unqualified.

Declare every deviation, contradiction and assumption.
──────────────────────────────────────────────────────────────

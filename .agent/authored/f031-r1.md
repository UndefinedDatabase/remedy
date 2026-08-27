── STEP R1 — F031 Decision inbox ─────────────────────────────
Goal:        Claim F031, reset the review record for the new feature,
             close F022's record with its R19 gate entry, register the
             one candidate F022 carried as R-0677, and empty the
             candidate carrier — all state, no production code.

Fortschritt: ~0 % (F031 claimed; the round map's R1 is this round · no
             T-slice started · the decision-inbox inventory is R3) —
             Schaetzung

Bundle:      C0a save this block · C0b mirror it into last_block ·
             C1 the plan · C2 the STATUS claim · C3 the review-record
             reset carrying the open set forward, the F022 R19 gate
             entry and the R-0677 record · C4 the emptied candidate
             carrier and the new branch context · C5 the handback.

Change set:  exactly these paths, nothing else —
             .agent/authored/f031-r1.md
             .agent/last_block.md
             .agent/plan.md
             docs/roadmap/STATUS.md
             .agent/live_review.md
             .agent/candidates.md
             .agent/context.md
             .agent/handoff.md
             This list bounds the round's WRITES. It does not bound the
             round's ACTIONS: the branch creation and the push named in
             constraint 3 and gate G12 are ordered explicitly and are
             not files (finding R-0674).

── Base and branch ───────────────────────────────────────────
The round base is `6325ac2fad76ca94e23f7bd02c80427d28e05f1f`, the merge
commit of pull request #213 which closed F022, and it is the tip of
`main`. BEFORE C0a, create and switch to `feature/f031-decision-inbox`
from that commit. Never commit to `main` (self-drive guardrail G3).

Every reading this block states about the base was MEASURED by the
reviewer at `6325ac2f` and is re-checkable there:
- `docs/roadmap/STATUS.md`: `^- \[~\] F\d+ — ` 0 and `^- \[x\] F\d+ — ` 57.
- `.agent/live_review.md`: 1241 lines, 617860 bytes, `^- R-\d+ — ` 237
  records all DISTINCT with maximum `R-0676`, `^Gate: R\d+ — ` 19 keys
  which are `R41` followed by `R1` through `R18`, `^Done: R-` 2 naming
  `R-0653` and `R-0670`, and no occurrence of the string `R-0677`.
- `.agent/candidates.md`: 35 lines, 2298 bytes, NON-EMPTY, one candidate.
- `.agent/context.md`: 46 lines.
- `docs/roadmap/features/T5_F031.md` resolves at the base.

── Constraints ───────────────────────────────────────────────
1. Apply every authored slice BYTE FOR BYTE. Never retype, rewrap,
   reflow, reindent or "fix" a slice. If a slice looks wrong, apply it
   verbatim anyway and declare the disagreement in the handback. The
   authored text is the record; your correction of it is not.
2. Slice transport. This block is saved verbatim as
   `.agent/authored/f031-r1.md` at C0a and mirrored byte-identically
   into `.agent/last_block.md` at C0b. Extract every slice
   PROGRAMMATICALLY out of the COMMITTED C0a blob by its marker LINES —
   a line equal to `<<<SLICE <NAME>` opens it and a line equal to
   `<<<END <NAME>` closes it — never by hand and never from this prompt.
   The marker lines themselves NEVER reach a target file.
3. Commit sequence, exactly: C0a, C0b, C1, C2, C3, C4, C5. No extra
   commit, none dropped, no reordering. If you must correct a landed
   commit, do NOT add a commit outside this sequence — declare it
   instead (finding R-0675). The branch is created before C0a; the push
   runs after C5.
4. Never amend, rebase, cherry-pick, force-push or rewrite history, and
   never delete a branch. Never merge anything this round.
5. `git status --porcelain` prints 0 lines after every commit of this
   round. Read `.agent/STOP` from disk before C0a and again before C5;
   if it exists at either point, finish the commit in hand, write the
   handback and stop (guardrail G6).
6. The slices this block carries are the whole texts PLANF031R1,
   LRHEADER, LRSTEPS, GATE19, RECORD677, CANDIDATES and CONTEXT, and
   the pair halves STATUSFROM and STATUSTO. This paragraph names them
   and states no count of them; G3 orders you to REPORT the count your
   own extractor measured.
7. Pair shape, measured not asserted. The reviewer ran the containment
   test on the one pair this block carries and records its OUTPUT here:
   STATUSFROM/STATUSTO — `TO contains FROM: false`. That output makes it
   a REWRITE, so G4 orders the FROM-zero reading and NOT the §4.9 append
   obligation. Apply the pair EXACTLY ONCE, and apply it BEFORE any
   whole-file write touches the same file.
8. Destructive target uniqueness. STATUSFROM's bytes occur in
   `docs/roadmap/STATUS.md` at `6325ac2f` exactly 1 time as a whole
   anchored line, 1 time as a bare substring and 1 time indent-agnostic
   — three readings that agree — so the pair has one unambiguous target.
9. Destructive verification, if you run any, happens ONLY inside a
   disposable `git worktree` under `.remedy-wt/`, never in the primary
   checkout. Remove such a worktree BY ITS EXACT PATH and never by a
   glob (finding R-0662, which cost this machine roughly 78 archived
   review packages). Report `git worktree list` back at 1 line.
10. The review record's reset at C3 is a SCRIPTED rebuild, not a hand
    edit, and its algorithm is fixed here: take `.agent/live_review.md`
    at `6325ac2f`; replace the header block — every line from the first
    line of the file up to and including the last line of the leading
    `>` blockquote — with LRHEADER; replace the BODY of the `## Steps`
    section — every line after the `## Steps` heading up to but not
    including the `## Findings` heading — with LRSTEPS; delete every
    `Gate:` paragraph, all 19 of them, blank-line-separated units whose
    first line matches `^Gate: R\d+ — `; then append GATE19 and
    RECORD677. Carry EVERY `^- R-\d+ — ` record forward unchanged: this
    reset prunes the round map and the previous features' gate entries,
    and prunes no finding record.
11. Do not touch `docs/roadmap/ROADMAP.md`, `README.md`, or any path
    outside the change set. The README's Status line already reads
    `Next: F031 (Decision inbox)`; a claim does not change it, only a
    closure does.
12. REMOVE every disposable worktree BEFORE running the G12 suites, and
    report `git worktree list` as 1 line immediately before the first
    pytest command. This is not hygiene, it is a correctness condition
    the reviewer MEASURED at `6325ac2f`: with a worktree present under
    `.remedy-wt/`, `tests/orchestration/test_test_runner.py::`
    `TestVitestFrontendTestFoundation::test_vitest_passes` FAILS,
    because `npx vitest run` discovers the worktree's own
    `apps/ui/vitest.config.ts` and no worktree carries `node_modules`
    (the R-0518 shape); the error is
    `Cannot find package 'vitest' imported from` that config. With no
    worktree present the SAME suite is 52 passed. A red produced this
    way is an artefact of the measurement, so if you see it, remove the
    worktree, re-run, and report BOTH readings rather than either one
    alone.

── Authored slices ───────────────────────────────────────────

<<<SLICE PLANF031R1
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the merge
commit of pull request #213 which closed F022. `.agent/live_review.md` is the
source of truth for the open set, the round map and the finding-id ceiling.

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
R1 claims F031. It advances this plan, flips the STATUS line to `[~]`, resets
the review record for the new feature, writes the F022 R19 gate entry that
closes that feature's record, registers the single candidate F022 carried as
R-0677, and empties `.agent/candidates.md` in the same round.

## Next Steps
1. R2 records the R1 verdict on disk.
2. R3 takes the decision-inbox inventory in the source and MEASURES each part:
   the file-based queue store and its CLI, every producer that writes a
   decision, the DAG module's blocked-subtree entry point, and the decision
   event kinds the stream carries today on the Python and the TypeScript side.
3. T001 follows the feature file's Task slicing once that inventory is on disk.

## Risks
- The open set carried into F031 is R-0403, R-0413, R-0431, R-0445, R-0495,
  R-0533, R-0574, R-0625, R-0672, R-0674, R-0675 and R-0676, each re-read in the
  record at `6325ac2f` and carrying no resolution line there, plus R-0677 which
  R1 mints. R-0495 and R-0574 are the two Highs, both inherited from the
  already-closed F085 and F086 and neither an F031 defect.
- That set is NOT mechanically derivable from `.agent/live_review.md`. The
  record carries no machine-readable resolution marker, so the §3 item 10 rule
  yields 235 where the practice yields 12, and the plan's Risks section is the
  only carrier. R3 rules how the open set is to be derived; until it does, this
  bullet is the set.
- F031 depends on F009, F050 and F051. F009 is closed; whether F050 and F051 are
  built is UNMEASURED at this commit and R3's inventory settles it before any
  T-slice is planned.
<<<END PLANF031R1

<<<SLICE LRHEADER
# Live Review — F031 Decision inbox

> Round-by-round review record for the F031 branch, reset at the feature claim.
> The F022 record closed with pull request #213, merged into `main` at this
> feature's Open PR Gate as `6325ac2f` after CI run 32639191630 concluded
> SUCCESS on `45e4691f`. That branch's LAST round, R19, has no gate entry in its
> own record by construction, because a round's verdict is written by the NEXT
> reviewed round (DECISION F085 D9) and R19 was the last round F022 had; its
> entry is therefore the first `Gate:` paragraph below. Finding ids continue the
> monotonic R-XXXX series across the reset, and every finding record F022
> carried is carried forward unchanged.
<<<END LRHEADER

<<<SLICE LRSTEPS

R1 claim F031 in the roadmap ledger, create the branch, reset this record
carrying every finding record forward, gate F022 R19 and register the one
candidate F022 carried as R-0677, emptying the carrier in the same round → R2
record the R1 verdict on disk and rule how the open set is to be derived, the
gap R1's plan records → R3 the decision-inbox inventory: the file-based queue
store and its CLI, every producer that writes a decision, the DAG module's
blocked-subtree entry point, and the decision event kinds the stream carries
today on the Python and the TypeScript side, each MEASURED in the source, plus
whether F050 and F051 are built → the T-slices follow the feature file's Task
slicing and are planned once that inventory is on disk.

<<<END LRSTEPS

<<<SLICE GATE19
Gate: R19 — the F022 R19 entry. R19 PASSED ON EVERY ONE OF ITS TWELVE GATES, TEN OF WHICH WERE EXECUTABLE BEFORE THE HANDBACK COMMIT AND TWO OF WHICH NAMED ACTIONS RUNNING AFTER IT, AND THE REVIEWER RE-RAN EVERY EXECUTABLE ONE ITSELF RATHER THAN READING THE HANDBACK'S WORD FOR ANY OF THEM. THE ROUND'S SUBSTANCE IS THAT F022 IS CLOSED: the STATUS line flipped to `[x]` with the evidence job, package and digest R18 produced, the README capability list moved in the SAME commit, and the pull request was opened and deliberately not merged so the operator kept a review window. TRANSPORT HELD: the committed C0a blob, the committed C0b blob and `.agent/last_block.md` as read from disk are ALL sha256 `43ff9ad400bbb051bc2dff872c1aafa7619d3fc3df60861759ce671fa9d16876` over 27431 bytes and 356 lines, and C0a and C0b resolve to the SAME git blob `8ba85f9d`; the reviewer's own extractor over that blob printed 11 slices, reproducing the block's own reading. THE WHOLE-FILE WRITES ARE BYTE-EXACT: `.agent/plan.md` at `1c71b751` is 2544 bytes equal to PLANF022R19 plus exactly one newline, 44 lines strictly under the cap of 50, `^## Goal$` and `^## Next Steps$` once each; `.agent/candidates.md` at `45e4691f` is 2298 bytes equal to CANDIDATES plus exactly one newline; each bare-slice control was FALSE. THE FOUR PAIRS WERE MEASURED ONE READING PER PAIR AND NONE GENERALISED: STATUSFROM/STATUSTO, RM1FROM/RM1TO, RM2FROM/RM2TO and RM3FROM/RM3TO each printed `TO contains FROM: false`, each FROM went 1 to 0 and each TO 0 to 1, and BOTH edited files reconstruct byte-exactly from their base blob with only their own pairs applied — the strongest form of that proof, and the reviewer ran it rather than accepting the counts. THE LEDGER MOVED WHERE THE ROUND PROMISED AND NOWHERE ELSE: 237 records at the base and 237 at C2, all DISTINCT at both, maximum `R-0676` UNCHANGED, ids added and ids removed both the EMPTY SET, `^Done: R-` 2 and 2, `^Recurrence: R-` 11 and 11, and `^Gate: R` 18 becoming 19 by gaining exactly the key `R18` — this round minted no id, which is correct, because the closure protocol reserves the candidate's id for the next session's first reviewed round. THE ROADMAP READINGS REPRODUCE: `^- \[~\] F\d+ — ` 1 becoming 0 and `^- \[x\] F\d+ — ` 56 becoming 57 in `docs/roadmap/STATUS.md`, `57 of 255` present once in `README.md` with `56 of 255` absent, and the Tier 5 row reading `| 5 | Operator Cockpit | 5 | 29 |`. THE PACKAGE IS REAL AND THE REVIEWER WEIGHED IT ITSELF: `remedy-review-20260823-135731-READY_FOR_REVIEW.zip` is 68628435 bytes at sha256 `85fe27aaeefe0b885b6b2fe081187cff51a0e070ae7d9d5320e7d57d1e150f58`, recomputed over the published file rather than quoted from the build, and it is untracked and gitignore-matched so it never entered the repository. THE SUITES ARE THE REVIEWER'S OWN, run serially with never two pytest processes alive at once, every one exit 0: `tests/docs/` 295 passed, `tests/orchestration/test_roadmap_index.py` 30 passed, and the canary `tests/cli/test_golden_path.py` 42 passed, reproducing the handback cell for cell. STRUCTURE HELD: five commits, every one single-parent, insertions 356, 247, 15, 2 and 101, each far under the 500 cap and each agreeing with the handback's per-commit table; the anchored markers `^<<<SLICE ` and `^<<<END ` count 0 in all five edited files; `git ls-files .remedy-wt` is 0; one worktree; `git status --porcelain` 0 lines; and the reflog's OPERATION field carries amend 0, rebase 0 and cherry 0 over this round's rows. THE TWO INTENT GATES BOTH DISCHARGED HONESTLY, which is the point of the form R-0371's extended counter-measure requires: the push landed and the pull request was created as #213, and neither value was written into any file the round committed. THE ROUND DECLARED ONE CONTRADICTION AND IT WAS THE REVIEWER'S: the Handback paragraph ordered the `Fortschritt:` block carried "across all five of its lines" over a block whose Fortschritt occupies four, and the worker carried all four verbatim, edited nothing and reconciled nothing — the correct resolution, and the numeral was the only reading in the block that did not reproduce. IT ALSO DECLARED ITS HANDBACK AT 100 LINES against the 60-line tier, correctly resolved because five commits is not more than five per-commit tables, with the DECISION D15 stated cause naming the mandated content that caused it. THE VERDICT IS PASS. WHAT FOLLOWED IS RECORDED HERE BECAUSE NO F022 ARTEFACT CAN CARRY IT: the next session's Open PR Gate found CI run 32639191630 pending on #213, waited for it under the amend0820 ruling rather than treating it as a blocker, read it as SUCCESS, and merged the pull request with `--merge --delete-branch` as `6325ac2f`, after which `main` was clean and no pull request remained open.
<<<END GATE19

<<<SLICE RECORD677
- R-0677 — Low, FIVE REVIEW PACKAGES APPEARED IN THE WORKING TREE DURING A SESSION THAT ORDERED NO SUCH WRITE, AND THE ANSWER IS THAT THEY WERE TRACKED FILES GIT PUT BACK. Raised by the reviewer as a closure candidate during the F022 R19 review, carried on disk in `.agent/candidates.md` because the closure protocol reserves ids for the next session's first reviewed round, and REGISTERED here with its resolution already measured. THE ORIGINAL OBSERVATION, taken at `9a1e677f`: `remedy-review-20260726-001936-`, `-20260726-165629-`, `-20260726-202004-`, `-20260726-215057-` and `-20260727-101857-READY_FOR_REVIEW.zip` each carried an mtime EQUAL to their ctime at 2026-08-23 13:29:18, all five within 44 milliseconds of each other, while their filenames dated them to July. Equal mtime and ctime means the bytes were WRITTEN at that instant rather than touched, so five packages named for July were created during an August session by a step no round ordered and no handback recorded. THE CAUSE, MEASURED BY THE REVIEWER AT `45e4691f`: all five were TRACKED IN GIT. `git ls-files '*.zip'` returned exactly those five paths; `git log --diff-filter=A` names the commit that added each one — `785f4d4b` for the first and then `ecbe72fd`, `f778c6f4`, `df0db06d` and `350275b5`, the F014, F016, F034, F046 and F047 closure commits of 2026-07-26 and 2026-07-27 — and they total 41624083 bytes of binary carried in the repository. They were committed before `.gitignore` gained its `remedy-review-*` line, and a rule added later does not untrack what is already tracked. The simultaneous write is therefore ordinary Git behaviour and not a mystery: the glob that finding R-0662 records, run during the F021 R40 closure, deleted them from the working tree along with the untracked archive, and because these five were tracked a later checkout restored them byte-for-byte at one instant. The commit that fixed the packaging pipeline states this independently — `dd5e6d0e` reads "the five tracked ones were restored from Git" — so the record already held the answer the candidate asked for. NOTHING ABOUT F022'S CLOSURE RESTS ON ANY OF THIS: that feature's package is `remedy-review-20260823-135731-READY_FOR_REVIEW.zip`, which is untracked and gitignore-matched, and the reviewer recomputed its digest over the published file. THE DEFECT IS ALREADY REMEDIED AND THE REMEDY IS VERIFIED, WHICH IS WHY THIS IS REGISTERED AT LOW AND CLOSED IN THE SAME BREATH: `dd5e6d0e fix(packaging): publish review packages outside the repository` moved publication to `REMEDY_REVIEW_DIR` outside the repository and removed all five tracked archives, it is an ancestor of `main` at `6325ac2f`, and the reviewer measured `git ls-files '*.zip'` there as EMPTY. WHAT REMAINS OWED IS THE GENERALISATION, and it is what keeps this from being merely a closed ticket: no gate in this workflow reads whether a build artefact class is tracked, so the same shape — an ignore rule added after the fact, leaving tracked bytes behind it — is invisible until someone stats a file and is surprised. Fix, binding on the next block whose change set includes a packaging or evidence path: order a reading of `git ls-files` over every artefact glob `.gitignore` names for build output, require it EMPTY, and record the reading. R-0403 is a neighbour and not a duplicate — it concerns what goes INTO a package, this concerns packages tracked BY the repository — and the open set was searched for the defect before this id was minted (§3 item 30).
<<<END RECORD677

<<<SLICE CANDIDATES
# Closure Candidates — carrier of record

> Written per docs/roadmap/STATUS_closure_protocol.md ("Closure-candidate
> findings", disk-vehicle rule, operator ruling 2026-08-01). Read at Window-1
> session bootstrap (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present at
> feature-claim time is a block condition.

EMPTY. The one candidate F022 carried was registered as finding R-0677 in
`.agent/live_review.md` by F031 R1, the first reviewed round after that closure,
and this file was emptied in the same round exactly as the closure protocol
requires.
<<<END CANDIDATES

<<<SLICE CONTEXT
# Context — F031 Decision inbox

## Active Branch
feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the merge commit
of pull request #213 which closed F022.

## Scope
F031 only: the decision read endpoint and blocked-size computation, the inbox
cards with their generic options renderer, ordering, filtering and badge, and
the answer wiring through the existing write channel. The roadmap feature file
is `docs/roadmap/features/T5_F031.md` and its Task slicing fixes the order.

## Do not touch
The decision queue's storage format and its CLI semantics, and the write
channel's nonce and audit behaviour. The feature file's own Do-not-touch
section governs and is not narrowed here.

## Assumptions
- The decision queue is and stays FILE-BASED. The inbox is a READ VIEW plus
  command wiring, never a storage migration; an earlier sketch's "(SQLite)" is
  explicitly not the design.
- The card renderer is generic over the decision's options payload. No
  per-type form is hardcoded, which the extensibility test pins.
- Answering reuses the existing decision-answer command through the write
  channel rather than adding a second write path.

## Constraints
- A round touching `docs/roadmap/**` also gates
  `tests/orchestration/test_roadmap_index.py` beside `tests/docs/`.
- A round rewriting `.agent/` state gates the four state readers:
  `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
  `tests/regression/test_resource_safety.py` and
  `tests/orchestration/test_integrity_gate.py`.
- Every handback runs the canary `pytest tests/cli/test_golden_path.py`.
- Destructive verification runs only inside a disposable git worktree under
  `.remedy-wt/`, never in the primary checkout, which satisfies
  `git status --porcelain` empty at every verdict.
- This is a UI feature, so `docs/ui/design_reference/` is binding and any
  visual deviation is documented with a technical reason.

## Steps
The round map lives in the `## Steps` section of `.agent/live_review.md`, per
R-0447's remedy, and this file deliberately does not restate it: a second copy
of the map is what fell out of step and cost F022 a finding.
<<<END CONTEXT

<<<SLICE STATUSFROM
- [ ] F031 — Decision inbox
<<<END STATUSFROM

<<<SLICE STATUSTO
- [~] F031 — Decision inbox
<<<END STATUSTO

── Done when ─────────────────────────────────────────────────
Run every gate yourself, record its REAL exit code and its REAL output,
and report ONE LINE PER GATE in the handback with the transcripts kept
out of it (finding R-0582). "Green" as a word is a finding. Every gate
below runs at a commit STRICTLY EARLIER than C5, which writes the
handback (§3 item 31).

G1  Branch and cleanliness. `git branch --show-current` prints
    `feature/f031-decision-inbox` and NOT `main`. `.agent/STOP` read
    from disk is ABSENT before C0a and again before C5. Report
    `git status --porcelain` line count after each of C0a, C0b, C1, C2,
    C3 and C4; each must be 0.

G2  Transport. Report sha256, byte count and line count for FOUR
    readings: `.remedy-wt/f031-r1.md` as it exists before C0a, the
    committed C0a blob, the committed C0b blob, and `.agent/last_block.md`
    read from disk after C0b. All four must be EQUAL. Report the git
    blob id of C0a's and C0b's file; they must be the SAME id.

G3  Extraction. Run your extractor over the COMMITTED C0a blob and
    report the number of slices it found, the number of CONTENT lines
    inside markers, and the file's TOTAL line count. Report the numbers
    YOUR extractor printed; this block states none of them.

G4  The STATUS claim. In `docs/roadmap/STATUS.md`: STATUSFROM 1 at
    `6325ac2f` → 0 at C2, STATUSTO 0 → 1, applied EXACTLY ONCE.
    `^- \[~\] F\d+ — ` 0 → 1 and `^- \[x\] F\d+ — ` 57 → 57 UNCHANGED.
    The file at C2 must equal its `6325ac2f` blob with ONLY that one
    replacement applied — report that comparison as a boolean your own
    script printed.

G5  The plan. `.agent/plan.md` at C1 is byte-equal to PLANF031R1 under
    your stated newline convention; report the slice length, the file
    length and the convention. NEGATIVE CONTROL: report that the file
    is NOT byte-equal to the same slice with its trailing newline
    REMOVED, so the equality above distinguishes the two. `^## Goal$` 1,
    `^## Next Steps$` 1, and `wc -l` STRICTLY under 50.

G6  The record reset, structure. In `.agent/live_review.md`: at
    `6325ac2f` `^Gate: R\d+ — ` is 19; at C3 it must be exactly 1 and
    that one key must be `R19`. `^# Live Review — F031 Decision inbox`
    1 at C3 and `^# Live Review — F022` 0. `^## Steps$` 1 and
    `^## Findings$` 1 at C3.

G7  The record reset, findings preserved. This is the gate that proves
    the rebuild pruned only what constraint 10 allows. Extract the set
    of `^- R-\d+ — ` ids at `6325ac2f` and at C3. Report: the count at
    each (237 at the base), that all are DISTINCT at each, the ids
    REMOVED which must be the EMPTY SET, and the ids ADDED which must be
    exactly `{R-0677}`. Report the maximum id at each: `R-0676` → `R-0677`.
    Report `^Done: R-` 2 → 2. NEGATIVE CONTROL: run your id extractor
    over a deliberately corrupted copy in a disposable worktree with one
    record's `- R-` prefix broken, and report that the count drops.

G8  The two appended slices land byte-exact. For GATE19 and RECORD677
    separately, report that the appended region of `.agent/live_review.md`
    at C3 equals the extracted slice bytes, and report the byte
    arithmetic (base length, C3 length, and the difference against the
    two slice lengths plus your separators). The two appended paragraphs
    are separated from each other and from the preceding text by a blank
    line. NEGATIVE CONTROL: flip ONE byte inside the FIRST appended
    paragraph in a disposable worktree and report that your equality
    check REJECTS the mutant while ACCEPTING the true file.

G9  The carrier and the context. `.agent/candidates.md` at C4 is
    byte-equal to CANDIDATES under your stated convention, contains
    `^EMPTY\.` 1 and `^NON-EMPTY\.` 0, and names `R-0677`.
    `.agent/context.md` at C4 is byte-equal to CONTEXT and contains
    `^# Context — F031 Decision inbox$` 1. For BOTH files run the same
    negative control as G5: the landed file is NOT byte-equal to its
    slice with the trailing newline REMOVED.

G10 Markers never reach a target. Line-anchored `^<<<SLICE ` and
    `^<<<END ` both count 0 in each of `.agent/plan.md`,
    `docs/roadmap/STATUS.md`, `.agent/live_review.md`,
    `.agent/candidates.md` and `.agent/context.md` at C4.

G11 Structure and hygiene, over C0a..C4. Report per commit: that it is
    single-parent, and its INSERTION count — the `+` column only, per
    AGENTS.md DECISION F104 D1 — each under 500. Report the range path
    set MINUS the change set (must be EMPTY) and the change set MINUS
    the range (must be exactly `.agent/handoff.md`, which C5 writes).
    Report `git ls-files .remedy-wt` as 0, `git ls-files '*.zip'` as 0,
    `git worktree list` as 1 line, and the reflog OPERATION field over
    this round's rows with amend, rebase and cherry each 0.

G12 Suites, run SERIALLY, never two pytest processes at once, in the
    PRIMARY checkout at the C4 tree. All must exit 0; report the real
    exit code and the counts:
      python3 -m pytest tests/docs/ -q
      python3 -m pytest tests/orchestration/test_roadmap_index.py -q
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/cli/test_golden_path.py -q
    The reviewer executed all seven at `6325ac2f` with no worktree
    present and measured, in the order listed: 295, 30, 470, 52, 21, 16
    and 42, every one exit 0. Report yours against those and account for
    any difference. The full suite is NOT run this round.

G13 The push. AFTER C5, run `git push -u origin feature/f031-decision-inbox`.
    No `--force`, no `--force-with-lease`, no history rewrite, no branch
    deletion. Do NOT create a pull request this round. This gate's
    outcome is REPORTED TO THE REVIEWER and is NOT a value of any file
    this round writes (finding R-0371's extended counter-measure).

── Handback ──────────────────────────────────────────────────
Rewrite `.agent/handoff.md` at C5 per docs/agents/handback_template.md:
feature and round, branch, base and commit SHAs, a changed-files table
per commit, the item-status table covering C0a, C0b, C1, C2, C3, C4, C5
and the push, ONE LINE PER GATE with its real result, the open-findings
count, and the next expected action. Carry the `Fortschritt:` block
above VERBATIM across the lines it occupies — count them yourself and
carry exactly those; this block states no numeral for them.

The 60-line cap applies (this round has fewer than six per-commit
tables). If the MANDATED content genuinely does not fit, exceed it and
carry a DECISION D15 "Deviations, declared" line naming your measured
line count and the specific mandated content that caused the overage.
Never drop a mandated section to fit. Do NOT claim compliance with any
token cap: that cap was withdrawn.

Declare every deviation, contradiction and assumption. A contradiction
inside this block is the reviewer's defect, not yours: apply the slice
verbatim, state the disagreement, reconcile nothing.
──────────────────────────────────────────────────────────────

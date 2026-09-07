STEP T004/7 — F272 — round 25 — the record flip is ATOMIC, not per-caller: D14 part 2 is corrected, and the session closes

Base commit for every reading in this block: `4491ec9e`, the round 24 handback commit.
Every separator line below is exactly twenty `=` characters.

====================
Goal
====================

DECISION F272 D14, landed one round ago, ruled that T004 stages BY CALLER: a
round takes one classic-store consumer, moves it to `load_job_plan`, and adapts
the renderers it feeds. Parts 1 and 3 of that ruling stand. PART 2 IS WRONG, and
the measurement that shows it was taken after D14 was written.

WHAT WAS MEASURED, at the base commit, by RUNNING the shipped functions rather
than reading them. The classic `Job` and the unified `JobPlan` now differ in
exactly TWO fields: `id` and `name`. T002 closed every other gap, and the task
vocabularies already agree — `TaskEntry(...).status == RunState.PENDING` is True,
because both are plain strings against a `str` enum. So the whole remaining
migration is the `.id` spelling.

That single gap is what makes a per-caller flip impossible. Calling the shipped
helpers with a `JobPlan` gives:

    assess_job_readiness   FAIL -> AttributeError: 'JobPlan' object has no attribute 'id'
    recommend_worker       FAIL -> AttributeError: 'JobPlan' object has no attribute 'id'
    list_decisions         OK   -> list

`assess_job_readiness` has SEVEN call sites in seven modules and
`recommend_worker` SIX in six. Moving any ONE consumer onto the unified record
forces its shared helpers to accept a `JobPlan`, which forces THEIR other callers
to pass one, and the closure does not terminate before it has swallowed the whole
consumer graph. The only alternative is a helper that accepts both records, and
AGENTS.md's Scope Control forbids exactly that: "Replacing is deleting", no
attic, no compatibility reader.

THE FLIP IS THEREFORE ATOMIC, AND IT IS TOO LARGE FOR ONE COMMIT. An `ast` sweep
over all 1068 tracked `.py` files counts 468 `<job-ish>.id` reads in 74
production files and 1545 in 137 test files. That figure is an UPPER BOUND from a
receiver-NAME heuristic and not a probe measurement — `.id` is polymorphic here
exactly as `.status` was — but even a fraction of it exceeds the DECISION F104 D1
cap of 500 insertions for a single commit, and a half-flipped tree is red, so the
work fits neither in one commit nor in several.

That is a planning problem this feature cannot solve inside its own budget, and
it is the finding the next session's scope report needs. This round records it
and closes the session; it does not attempt the flip.

====================
Bundle
====================

C0a  save this block verbatim to `.agent/authored/f272-r25.md`
C0b  mirror the same bytes to `.agent/last_block.md`
C1   `.agent/plan.md` replaced byte for byte with PLANF272R25
C2   `.agent/live_review.md` — append RECORDR25, the round 24 PASS gate entry
     owed by amend0827 rule 1. No finding is minted this round.
C3   `.agent/prose_slips.md` — append SLIPSR25, one dated line
C4   `docs/roadmap/features/T2_F272.md` — append D15SLICE, the correction
C5   `.agent/handoff.md` rewritten, closing SESSION 11

====================
Change set — exactly these paths and nothing else
====================

    .agent/authored/f272-r25.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    docs/roadmap/features/T2_F272.md
    .agent/handoff.md

NOTHING under `packages/`, `apps/`, `tests/` or `scripts/` changes this round.
No production line moves, so no red-proof and no mutation is ordered or possible.
If a measurement forces a path outside this list, APPLY IT AND DECLARE IT.

====================
Constraints
====================

1. This block is applied verbatim. If a slice is wrong, apply it as written and
   declare the disagreement; never silently correct it.
2. Every authored slice is extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f272-r25.md`, between its `<<<BEGIN NAME>>>` and
   `<<<END NAME>>>` lines. Never retype a slice. A slice is read INCLUSIVE of
   the newline ending its last content line.
3. C0a and C0b are `shutil.copyfile` of `.remedy-wt/f272-r25-block.md`.
4. EVERY APPEND IN THIS ROUND IS `post == pre + b"\n" + slice`, and the block
   states those bytes rather than leaving them to be inferred — round 24's worker
   had to derive them and declared it. Each of the three append targets ends in
   exactly ONE newline at the base commit and contains ZERO occurrences of three
   consecutive newlines, so one blank line is the only separator any of them uses.
5. D15SLICE CORRECTS D14 BY APPENDING, NEVER BY REWRITING. §3 item 20 forbids
   overwriting landed text, and D14's parts 1 and 3 remain correct and in force.
   D14's own section is not edited.
6. THIS ROUND MINTS NO FINDING ID. Round 24 PASSED, and the one gap its worker
   declared is the reviewer's own block prose, which reached no file, so under
   amend0827 rule 2 it is a dated `.agent/prose_slips.md` line and never an id.
   `R-0826` must still be free when the round ends.
7. Read `.agent/STOP` with `os.path.exists` before C0a, before C4 and before C5,
   and report all three readings.
8. NO WORKTREE IS NEEDED OR PERMITTED THIS ROUND. The primary checkout satisfies
   `git status --porcelain` == empty at every commit boundary.
9. THE DOCS GATE APPLIES because the change set includes `docs/roadmap/**`.

====================
Done when — the gates
====================

Run every gate with `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, no pipe between the
command and the echo. Report ONE LINE PER GATE with the transcripts below it.
Every gate runs before C5, the commit that writes the handback.

G1 TRANSPORT. One digest comparison: the committed `.agent/authored/f272-r25.md`
   and `.agent/last_block.md` against the file this block was delivered from.
   Report sha256, byte length and line count for each.

G2 THE RECORD, over the single append at C2, against its own pre-image.
   (a) BYTE: report pre_len, pre_sha256, post_len, post_sha256, the terminal
       twelve bytes and trailing-newline run of each,
       `PRE_IS_BYTE_EXACT_PREFIX_OF_POST` and `POST_EQUALS_PRE_NL_SLICE`. At the
       base commit the pre-image is 1209111 bytes, 2129 lines, and its sha256
       begins `8ca58e083752f416`.
   (b) STRUCTURAL: strip the single terminal newline, split on blank lines,
       compare the LAST N units against the slice's paragraphs IN ORDER, where N
       is COUNTED BY YOUR SCRIPT from the slice and never taken from this block.
       Report N, units before, units after and `EVERYTHING_BEFORE_UNCHANGED`.
   (c) NEGATIVE CONTROL on the FIRST paragraph the append adds, in memory only,
       never on disk: flip one byte, require BOTH readers to reject it, then
       re-read the file and confirm it is byte-identical to the real post-image.
   (d) COUNTS, each measured, none adjusted to agree:
           ^- R-\d{4} distinct        309 -> 309
           ^Done: R-\d{4} distinct    252 -> 252
           open set BY DISTINCT ID     57 ->  57
           ^Gate:                      47 ->  48
           ^Gate: F272 R24              0 ->   1
           ^- R-0826                    0 ->   0
       Report OPEN FINDINGS BY DISTINCT ID with its arithmetic.

G3 THE TWO PROSE FILES. `.agent/plan.md` is byte-equal to PLANF272R25; report its
   bytes, its line count against the AGENTS.md cap of 50, and that `## Goal` and
   `## Next Steps` are both present. `.agent/prose_slips.md` gets the byte append
   check only — pre_len 148887 at the base commit, and `POST_EQUALS_PRE_NL_SLICE`
   for SLIPSR25. Report the line count it gains.

G4 THE FEATURE FILE. For C4 report pre_len, pre_sha256, post_len, post_sha256,
   `PRE_IS_BYTE_EXACT_PREFIX_OF_POST` and `POST_EQUALS_PRE_NL_SLICE`. The
   pre-image is 58026 bytes and 754 lines. Then report the count of
   `^### DECISION F272 D` headings before and after — it is 14 at the base commit
   — and confirm that each of `D1` through `D15` heads exactly one section, by
   listing the heading line of every one. A duplicated or skipped number is a
   STOP, not a note. Confirm ALSO that D14's own section is BYTE-UNCHANGED, by
   comparing the bytes between its heading and the start of D15's heading against
   the same span at the base commit.

G5 THE DOCS GATE. In the primary checkout at C4, run serially and report each
   exit code and count:
       python3 -B -m pytest tests/docs/ -q -p no:randomly
       python3 -B -m pytest tests/orchestration/test_roadmap_index.py -q -p no:randomly
       python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly
   The reviewer measured these at the base commit as 303, 30 and 42. REPORT THE
   NUMBER YOU MEASURE for each. No `.py` file changes this round, so no ruff
   reading is owed and none is ordered.

G6 THE TREE. `git status --porcelain` EMPTY at every commit boundary with the
   real output each time. `git ls-files .remedy-wt` empty. `git worktree list`
   unchanged from the base, which is the primary plus the twelve pre-existing
   `remedy/job-*` entries. Per-commit insertions from
   `git diff --numstat <parent> <commit>` for C0a through C4 — C5 excluded,
   because a commit cannot count its own insertions while it is being written —
   each under the DECISION F104 D1 cap of 500. The three `.agent/STOP` readings.

====================
Handback — this one CLOSES THE SESSION, so it carries more than usual
====================

Rewrite `.agent/handoff.md` completely: `SESSION 11 of feature F272 · round 25 ·
rounds so far 25`; the soft-limit reading under amend0906-triage-throughput,
which is 12 sessions and 40 rounds; one sentence of context self-assessment; the
range; a per-commit changed-files table whose `+/-` column comes from `git diff
--numstat` and is compared cell for cell against G6's figures; the item-status
table for C0a through C5; one line per gate with the transcripts below it; every
deviation and assumption. It has no length cap.

BECAUSE THIS HANDBACK ENDS THE SESSION IT ALSO CARRIES, in its own section:

  * SESSION 11 ran THREE delegated rounds — 23, 24 and 25 — all three PASSED,
    which is below the six-to-eight target amend0905-throughput sets, and
    amend0906 rule 3 requires the reason in one sentence: the session spent its
    measurement budget establishing that T004's remaining work is a single
    atomic record flip rather than the per-caller sequence the plan assumed, and
    that finding is what rounds 24 and 25 put on disk.
  * THE NEXT SESSION IS SESSION 12, WHICH REACHES F272'S SOFT LIMIT of 12
    sessions. Its first obligation after the Phase 0 probe is therefore NOT more
    building: it is the SCOPE REPORT, and then the amend0905-throughput
    split-and-close default, EXECUTED on the session's own authority — register
    the remaining scope as a new feature placed directly after F272 per
    amend0906-split-placement, close F272 at a self-consistent scope through the
    normal closure sequence, and record the whole move as a dated DECISION.
  * THE FIGURES THAT SCOPE REPORT NEEDS ARE ALREADY MEASURED AND MUST NOT BE
    RE-DERIVED: they are in `.agent/f272_t004_staging.md` and in DECISIONs F272
    D14 and D15.
  * THE NEXT SESSION'S FIRST ACTION: run Phase 0, the state probe; then check
    `.agent/STOP` under Phase 1 rule 1 BEFORE the Open PR Gate under rule 2, in
    that order. No PR exists for this branch and none was created.

<<<BEGIN PLANF272R25 target=.agent/plan.md>>>
# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 to 25 PASSED except round 2
(premise corrected by DECISION F272 D2) and round 21 (R-0824, repaired by round
22). T001, T002 and T003 are COMPLETE. T004 is under way.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the run
re-key, T002 the rest of the unified record, T003 the consumers, T004 the
classic runner, T005 the reachability test and the cluster deletion.

## Current Step

Record that T004's remaining work is ONE ATOMIC record flip and not the
per-caller sequence DECISION F272 D14 assumed. `Job` and `JobPlan` now differ in
only `id` and `name`; `.id` sits on helpers with six and seven callers each, so
moving one consumer closes over the whole graph, and a helper taking both records
is the compatibility reader AGENTS.md forbids. DECISION F272 D15 carries it.

## Next Steps

1. SESSION 12 REACHES THE SOFT LIMIT of 12 sessions. Its first obligation is the
   SCOPE REPORT, then the amend0905-throughput split-and-close default executed
   on the session's own authority — register the remainder as a new feature
   placed directly after F272 per amend0906-split-placement, and close F272 at a
   self-consistent scope through the normal closure sequence.
2. The figures that report needs are already measured: 60 production and 127 test
   files migrate, twelve cluster-bound consumers never do, and the `.id` flip has
   an upper bound of 468 production and 1545 test reads. See
   `.agent/f272_t004_staging.md` and DECISIONs F272 D14 and D15.
3. `job.run-next`, `job.run` and F114's cost-preview carrier all sit BEHIND that
   flip and are named in D13, D14 and this plan's predecessor; none is startable
   before the record boundary moves.
4. T005 is never split and stays last, whichever feature ends up owning it.

## Risks

- The flip exceeds the DECISION F104 D1 cap of 500 insertions for one commit and
  cannot be split without a red tree, so it needs a ruling this feature's budget
  cannot buy. That is the scope report's central question.
- A half-performed deletion is the state the Orchestrator brief forbids, so every
  deletion round ends with the full suite green in the PRIMARY checkout.
- F272's soft limit is 12 sessions and 40 rounds under amend0906. At session 11
  and round 25 the feature is inside it; session 12 reaches it.
<<<END PLANF272R25>>>

<<<BEGIN RECORDR25 target=.agent/live_review.md mode=append>>>
Gate: F272 R24 — the F272 round 24 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER RATHER THAN READ, in the primary checkout at `4491ec9e`. Range `81b2dc86`..`4491ec9e`, eight commits, every one single-parent, in exactly the ordered sequence C0a, C0b, C1, C2, C3, C4, C5, C6, with `git diff --stat` naming exactly the eight declared paths and nothing under `packages/`, `apps/`, `tests/` or `scripts/`. G1 TRANSPORT IS A REAL CHAIN: the reviewer's own scratch original `.remedy-wt/f272-r24-block.md`, written and hashed BEFORE delegation, and the committed `.agent/authored/f272-r24.md` and `.agent/last_block.md` are all 24493 bytes at 285 lines and all hash to `255fd4f05f3ee938fcbc470037428918862cbae2f347cbde0f437eece3edf5f5`; the staging artefact matches its own pre-delegation original at `25ed0b5a1fc1180e4339e28b95bec986b9f51ccdc946d5a7f56de48e4d7ff526` and 5921 bytes. Per §3 item 37 that chain covers those artefacts and is not a claim about the bytes emitted into a prompt. G2 THE RECORD reproduces: 1209111 bytes from a 1204799-byte pre-image that is a byte-exact prefix, with registrations 309 unchanged, resolutions BY DISTINCT ID 252 unchanged, open set 57 unchanged, `^Gate: ` 46 to 47, `^Gate: F272 R23 ` 0 to 1 and R-0826 still free — exactly the shape a round that mints and resolves nothing must have. G3 THE PLAN is 2525 bytes at 47 lines against the cap of 50 and byte-equal to its slice. G4 THE FEATURE FILE went 52485 to 58026 bytes and 736 to 754 lines with the pre-image a byte-exact prefix and `POST_EQUALS_PRE_NL_SLICE` true, the DECISION headings 13 to 14, and the reviewer independently confirms the heading numbers read exactly `1` through `14`, each one appearing once and in order. G5 THE DOCS GATE is EXIT 0 at 375 passed across `tests/docs/`, `tests/orchestration/test_roadmap_index.py` and the canary, which is 303 plus 30 plus 42 and matches the reviewer's own pre-measured figures cell for cell. G6 THE TREE: `git status --porcelain` empty, `git ls-files .remedy-wt` empty, per-commit insertions at a maximum of 296, under the DECISION F104 D1 cap of 500. THE RULING ITSELF WAS RE-DERIVED AND NOT ACCEPTED: the reviewer recomputed the staging artefact's central arithmetic from the stored inventory rather than reading it, confirming 72 production consumers, twelve DIES entries every one of which really is in that inventory's own PROD list, and 60 remaining — so DECISION F272 D14's first part rests on a measurement the reviewer reproduced independently. THE WORKER'S CONDUCT IS UPHELD IN FULL, AND ITS FOURTH DEVIATION IS THE ROUND'S BEST: its first draft of the handback wrote a FABRICATED SHA for the commit that had not yet been made, into four separate places; it caught this against the rule that no unmeasured SHA is ever written, checked how the previous round had solved the same problem, and rewrote all four sites so the range ends at the last commit that exists and says why. Nothing false reached disk, and the reviewer confirms `3216cd5c` occurs zero times in the committed file. Its remaining deviations are accepted: two pushes rather than one, because a handback cannot transcribe a push of itself; deriving the append separator's byte form from the files because the block named the property without spelling the bytes, which is a gap in the reviewer's block and is recorded as a dated prose-slip line beside this entry; and writing gate scripts to `.remedy-wt/` because the session's bash guard rejects a brace quantifier, with `\n\n+` used for the identical language the block spelled `\n{2,}`.
<<<END RECORDR25>>>

<<<BEGIN SLIPSR25 target=.agent/prose_slips.md mode=append>>>
2026-09-07, F272 round 24 — the block ordered `POST_EQUALS_PRE_NL_SLICE` for three separate appends without ever spelling the separator bytes, so the worker had to derive `pre + b"\n" + slice` from the files themselves and declare the assumption; it derived it correctly, and no gate was weakened, but a property named only by the identifier of its own gate is a property the block did not state. When a block orders an append proof, spell the byte relation it must satisfy in the constraints rather than leaving the gate's name to carry it.
<<<END SLIPSR25>>>

<<<BEGIN D15SLICE target=docs/roadmap/features/T2_F272.md mode=append>>>
### DECISION F272 D15 (2026-09-07, F272 round 25) — correction to D14 part 2: the classic-to-unified flip is ATOMIC over the consumer graph, not stageable by caller, because `.id` is the last gap and it sits on shared helpers

CONTEXT. DECISION F272 D14, recorded one round earlier, ruled in its second part that T004 stages BY CALLER: a round takes one classic-store consumer, moves it to `load_job_plan`, and adapts the renderers it feeds. That ruling was made from a reading of which modules OPEN the store. It was not made from a reading of what happens when a `JobPlan` is actually handed to the functions those modules call, and that reading contradicts it. D14's parts ONE and THREE are unaffected and remain in force — the twelve cluster-bound consumers are still never migrated, and `job.run-next` still dies with the rails rather than ahead of them. This decision corrects the SECOND part only, and it corrects it by APPENDING, because `docs/roadmap/features/T2_F272.md` records landed rulings and §3 item 20 forbids overwriting them; D14's own section is left byte-unchanged.

MEASURED at `4491ec9e`, by RUNNING the shipped functions rather than reading them. FIRST, the two records have almost converged: the only fields of the classic `Job` with no counterpart on `JobPlan` are `id` and `name`, T002 having closed every other gap, and the task vocabularies already agree because `TaskEntry(...).status == RunState.PENDING` evaluates True — both are plain strings against a `str` enum. So the entire remaining migration is the `.id` spelling. SECOND, that one gap does not stay local. Calling the shipped `assess_job_readiness` and `recommend_worker` with a `JobPlan` fails identically with `AttributeError: 'JobPlan' object has no attribute 'id'`, while `list_decisions` already succeeds — and `assess_job_readiness` has SEVEN call sites across seven modules with `recommend_worker` at SIX across six. Moving any ONE consumer onto the unified record therefore forces its shared helpers to accept a `JobPlan`, which forces every OTHER caller of those helpers to pass one, and that closure does not terminate before it has taken in the whole consumer graph.

CHOSEN. THE FLIP IS ATOMIC AND IS ACKNOWLEDGED TO BE TOO LARGE FOR THIS FEATURE'S REMAINING BUDGET, rather than attempted in slices that cannot be green. The only way to make a per-caller sequence work is a helper that accepts both records, and AGENTS.md's Scope Control forbids precisely that — "Replacing is deleting", with no attic, no deprecated alias and no compatibility reader. An `ast` sweep over all 1068 tracked `.py` files bounds the flip at 468 `<job-ish>.id` reads in 74 production files and 1545 in 137 test files. THAT FIGURE IS AN UPPER BOUND FROM A RECEIVER-NAME HEURISTIC AND NOT A PROBE MEASUREMENT: `.id` is polymorphic in this repository exactly as `.status` was, so the honest site set is whatever the DECISION F272 D7 raising-property method returns, and that probe has not been run. Even a fraction of the bound exceeds the DECISION F104 D1 cap of 500 insertions for a single commit, and a half-flipped tree is red, so the work fits neither in one commit nor in a sequence of them under the rules as they stand.

CONSEQUENCE, AND IT IS THE POINT OF THIS RULING. F272 cannot finish T004 within its own limit, and the next session — session 12, which reaches the soft limit of 12 sessions — owes the scope report and then the amend0905-throughput split-and-close default. This decision exists so that report is written from measurements rather than from an estimate, and so no later session re-derives the graph a third time. The question that report must put to the operator is the one this feature cannot answer on its own authority: how a change that is atomic by construction is to be landed under a per-commit insertion cap that forbids it.

ALTERNATIVES CONSIDERED. Adding an `id` property to `JobPlan` so the helpers keep working — rejected as the compatibility reader Scope Control forbids by name, and it would leave two spellings of the job identity alive, which is the exact defect F272 exists to remove. Renaming `job_id` to `id` on `JobPlan` instead — rejected: `job_id` is the spelling F260 D1 ruled and every record on disk carries, and DECISION F272 D4 already ruled it the ONE required key. Flipping the helpers first and leaving their classic callers broken for a round — rejected: it leaves the suite red at a commit boundary, which every gate in this workflow exists to prevent. Attempting the flip anyway and declaring an oversize commit — rejected: AGENTS.md permits at most one declared oversize commit per feature and this would be far beyond what that exception contemplates.

REVERSE by deleting this section, at which point D14 part 2's per-caller staging stands unamended and the next session discovers the closure for itself.
<<<END D15SLICE>>>

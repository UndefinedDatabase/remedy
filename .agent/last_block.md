STEP — F274 ROUND 20 — the R-0837 repair: guard the attestation authority set against a deleted file, so a deletion feature can be packaged at all

Goal: unblock the F274 closure. `packages.orchestration.job_evidence.create_manual_completion_bundle`
is the canonical closure evidence producer, and on this branch it REFUSES to build at all, because
the branch deletes a source file. One conjunct on one comprehension fixes it; this round lands that
conjunct, ships a regression test that goes red without it, proves the colour by mutation in a
disposable worktree, and re-runs the whole suite because the value the conjunct narrows feeds four
more artifacts in the same function. The ledger commit books round 19's PASS verdict, registers
R-0837 and R-0838, and appends the R-0784 recurrence.

Base commit for every reading in this block: `bb375019`.

WHAT THE REVIEWER MEASURED BEFORE AUTHORING, by APPLYING the change and RUNNING it, not by reading
the code. In a disposable worktree at `bb375019`, against the fork point
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, the authority set holds 57 paths and exactly one of
them, `apps/cli/commands/feature_cmd.py`, is `status='deleted'` with `current_sha256=None`. The
producer was then called TWICE, and it fails from BOTH of the only two placements that path can
have: with the deleted file IN the task partition it raises `ValueError: T001: safe-diff path set
does not match the task partition`, and with it OUT it raises `ValueError: task partition does not
exactly cover the attestable authority set`. The guard below was then applied and committed in that
same worktree, and the SAME producer call SUCCEEDS from both placements, returning `verdict
PASS_WITH_RISKS` and `commit_count 158`. THE COUNTS ARE NOT A GATE IN THIS ROUND and no done-when
below asserts one, because the round's own commits enter the authority set and move every one of
them; what is gated is the BEHAVIOUR — refusal before, success after.

ONE MEASUREMENT FROM THAT DRY RUN THAT COSTS NOTHING NOW AND WOULD COST A ROUND LATER: the
authority set is read from the WORKING TREE, so the reviewer's own untracked probe script under the
worktree root joined it and moved the count from 57 to 58 until it was moved out. Nothing in this
round depends on it. It is written into R-0837 and into the plan because closure round A runs the
evidence job for real.

WHAT THE REVIEWER READ IN THE FILES THIS BLOCK ORDERS CHANGED, per §3 item 34, with what it found.
(a) `packages/orchestration/job_evidence.py`: `authority = sorted(` occurs EXACTLY ONCE, and the
conjunct `is_attestable_source(f.path) and f.current_sha256` occurs EXACTLY ONCE — in the
`file_hashes` loop about twenty lines below the authority comprehension, which is the idiom this
fix copies rather than invents. After the fix that conjunct occurs twice and `authority = sorted(`
still occurs once. (b) THE ONLY SOURCE-TEXT GUARD over that file is
`tests/orchestration/test_job_evidence.py::TestEvidenceHygiene::test_no_hardcoded_verification_test_list`,
which reads the module source and asserts the absence of the two strings `test_role_config.py` and
`test_execution_config_evidence.py`; this change adds neither, so §3 item 7 is discharged rather
than assumed. (c) THE HOME FOR THE REGRESSION TEST IS NOT THE ONE THE HANDBACK PROPOSED, and the
reason is worth stating: `tests/orchestration/test_review_subject_deletions.py` covers
`resolve_review_subject`, which is NOT defective — it reports the deletion correctly, and a test
there would exercise the wrong module. `tests/orchestration/test_review_manual_completion_shapes.py`
already drives `create_manual_completion_bundle` end to end over a temporary git repository through
`TestManualCompletionRunsEndToEnd`, with `_init_repo`, `_commit` and `_rev` helpers at module
scope; that class's repository has no deletion in it, and no test in this repository builds a bundle
from a branch that deletes a file. That is the gap, and that file is where it closes.

THE FIX IS DESCRIBED AND NOT SLICED, because production code is never reviewer-authored bytes the
worker only transcribes. The worker writes it, the gates below measure it.

FRAME CONVENTION. Every slice is delimited by a line reading `BEGIN <NAME> sha256=<hex> bytes=<n>`
and a line reading `END <NAME>`; the slice is the bytes BETWEEN those two lines, its leading
newline and its trailing newline INCLUDED, and marker lines never reach any file. No line of this
block's FRAME is a run of a single repeated character.


## Bundle — the commits of this round, in this order

C0a  Save this block verbatim as `.agent/authored/f274-r20.md`.
C0b  Mirror the same bytes into `.agent/last_block.md`.
C1   Replace `.agent/plan.md` with the PLAN20 slice.
C2   Append the RECORD20 slice to `.agent/live_review.md` — four paragraphs: round 19's PASS
     verdict, the R-0837 registration, the R-0838 registration, and the R-0784 recurrence — and
     append the SLIP20 slice to `.agent/prose_slips.md`.
C3   THE FIX AND ITS TEST, in one commit: the guard in `packages/orchestration/job_evidence.py` and
     the regression test in `tests/orchestration/test_review_manual_completion_shapes.py`.
C4   Rewrite `.agent/handoff.md` and hand back.


## Change — the exact set; nothing outside it is touched

    .agent/authored/f274-r20.md                                   (new, C0a)
    .agent/last_block.md                                          (rewrite, C0b)
    .agent/plan.md                                                (rewrite, C1)
    .agent/live_review.md                                         (append, C2)
    .agent/prose_slips.md                                         (append, C2)
    packages/orchestration/job_evidence.py                        (C3)
    tests/orchestration/test_review_manual_completion_shapes.py   (C3)
    .agent/handoff.md                                             (rewrite, C4)

THE GUARD, at C3. In `create_manual_completion_bundle`, the statement whose first line is
`    authority = sorted({f.path for f in subject.files` — the sole occurrence of `authority =
sorted(` in that file — gains the conjunct `and f.current_sha256` to its existing
`is_attestable_source(f.path)` condition, so that a subject file with no content at the branch tip
is excluded from the attestation authority set. Wrap the comprehension across two lines if the line
would otherwise exceed the project's line length; the formatting is the worker's, the condition is
not. Nothing else in the file changes: no other statement, no import, no comment above a different
symbol. Put the one-line WHY comment directly above the statement, per AGENTS.md Code
Discoverability, naming what a deleted path cannot attest.

THE REGRESSION TEST, at C3, in `tests/orchestration/test_review_manual_completion_shapes.py`. ONE
new test class holding ONE test method, added at the END of the file, reusing the module's existing
`_init_repo`, `_commit` and `_rev` helpers rather than introducing new ones. It builds a temporary
repository whose BASE commit carries at least three attestable source files, and whose head range
MODIFIES at least two of them and DELETES exactly one (by `git rm` plus a commit, which the module
has no helper for — add the smallest one you need, or inline the two `subprocess.run` calls in the
style `_commit` already uses). It then calls `create_manual_completion_bundle` over that repository
the way `TestManualCompletionRunsEndToEnd._bundle` does — same `verification_runs` shape, a
`review_feature_id`, `num_tasks=2` — and asserts, at minimum: that the call RETURNS rather than
raising; that the returned `verdict` is `PASS_WITH_RISKS`; that the deleted path is ABSENT from the
`file_hashes` of the produced `current_change_content_proof.json`; and that every SURVIVING changed
source path IS present there. The test's docstring names R-0837 and states, in one sentence, that
without the guard this call raises `ValueError` from one of two mutually exclusive checks. Do NOT
assert an authority COUNT: that number moves with the fixture and pins nothing about the defect.


## Constraints

1.  Apply every slice BYTE FOR BYTE. If a slice looks wrong, apply it anyway and say so in the
    handback under deviations — the reviewer owns slice text, and a corrected slice is a finding
    against the reviewer, never a repair the worker performs.
2.  The change set above is exhaustive. A path outside it is not edited, created or deleted this
    round, and that includes every file under `docs/` and `scripts/`.
3.  ONE worker, this round only. Follow AGENTS.md in full: self-review loop before every commit,
    the Commit Gate, small commits, push after committing.
4.  NEVER work on `main`, never force-push, never rewrite history, and delete no branch.
5.  Every destructive check — the mutation of G5 — runs ONLY inside a disposable `git worktree`
    under the gitignored `.remedy-wt/`, never in the primary checkout. Remove that worktree and run
    `git worktree prune` before C4.
6.  The primary checkout satisfies `git status --porcelain` == EMPTY at the end of every commit.
7.  If ANY gate below comes back red, STOP: commit what is honestly finished, write the handback
    with the raw output, and hand back. Do not repair a red gate by re-scoping it, and do not edit
    a test to make a gate green.
8.  Report every gate's REAL exit code and REAL output. "Green" as a word is a finding against this
    round; the number or the transcript is the evidence.
9.  C3 is ONE commit carrying both the guard and its test, deliberately: a production behaviour
    change and the test that proves it belong together, and splitting them would land a commit
    whose behaviour no test in the tree reaches.
10. The full-suite run of G7 is NOT a claim that this feature's integration gate has re-passed —
    round 18 holds that claim and this round does not restate it. It runs because the value this
    round narrows feeds `workspace.diff`, the `expected_changed_files` and `actual_changed_files`
    pair, `write_manual_completion_evidence`'s `authority` argument, and the `source_files` and
    `evidence_covered_files` keys, so a scoped gate cannot see what it might have moved.


## Done when — eight gates, each RUN and each REPORTED with its real output

G1  TRANSPORT, at C0b. `sha256sum` of `.remedy-wt/f274-r20-FINAL.md`, of the committed
    `.agent/authored/f274-r20.md`, and of the committed `.agent/last_block.md`. Report all three
    digests and all three byte counts. The three digests must be EQUAL. This proves the chain
    scratch-original to saved copy to mirror and claims nothing about the bytes the reviewer
    emitted, per §3 item 37.

G2  THE PLAN, at C1. Report `wc -c` and `wc -l` of `.agent/plan.md`; it must be byte-identical to
    the PLAN20 slice at 2631 bytes and 43 lines, which is under the AGENTS.md cap of 50. Report
    that `## Goal` and `## Next Steps` each occur in it, which
    `tests/orchestration/test_test_runner.py` asserts.

G3  THE APPENDS, at C2, with full byte forensics for `.agent/live_review.md` because it is the
    record. (a) BYTES: report the file's size before and after; the reviewer measured 638448 before
    at `bb375019` and the RECORD20 slice at 12426 bytes, so after must be 650874. (b) EXACT APPEND:
    the pre-commit blob is a byte-exact PREFIX of the post-commit file, and the slice is an exact
    SUFFIX of it — report both booleans. (c) ORDERED EQUALITY, by a reader independent of (b): split
    the whole post-commit file on blank lines, COUNT the slice's own paragraphs into N rather than
    taking N from this block, and compare the file's LAST N units against the slice's N paragraphs
    IN ORDER; report N and the boolean. (d) NEGATIVE CONTROL on the FIRST appended paragraph: flip
    one byte inside it, in scratch and never in the tracked file, and report that BOTH the reader of
    (b) and the reader of (c) REJECT it. (e) COUNTS over the post-commit file: blank-line units
    246 to 250; `^Gate: ` 50 to 51; `^Gate: F274 R19 ` 0 to 1; `^RECURRENCE of R-0784 ` 0 to 1;
    distinct `^- R-\d+ — ` ids 70 to 72; distinct `^Done: R-\d+ — ` ids 7 to 7; and the OPEN SET
    BY DISTINCT ID 63 to 65. (f) THE SLIP: `.agent/prose_slips.md` is an exact append of SLIP20,
    164868 bytes to 165189, gaining exactly one blank-line unit. (g) Report the count of unquoted
    `\bHEAD\b` in the RECORD20 slice with every backtick-quoted span deleted first; it must be 0.

G4  THE GUARD, at C3. Report `git show --numstat C3 -- packages/orchestration/job_evidence.py` and
    the FULL `git diff` of that file for C3, verbatim. In the post-commit file report the count of
    `authority = sorted(`, which must be 1, and of `is_attestable_source(f.path) and
    f.current_sha256`, which must be 2. Report that the two strings
    `test_role_config.py` and `test_execution_config_evidence.py` are each absent from the file, so
    that the source guard named above still holds. Then `ruff check
    packages/orchestration/job_evidence.py tests/orchestration/test_review_manual_completion_shapes.py`
    and report its exit code and output.

G5  THE RED-PROOF, in a disposable worktree at C3 under `.remedy-wt/`, never in the primary
    checkout. (a) IMPORT PROOF FIRST, because an editable install of this project exists and has
    shadowed a worktree before: with the worktree as the working directory, run `python3 -B -c
    "import packages.orchestration.job_evidence as m; print(m.__file__)"` and report the path, which
    must be inside that worktree. (b) THE UNMUTATED CONTROL, in that same worktree and BEFORE any
    mutation: run the new test alone by its node id with `python3 -B -m pytest <node id> -q
    -p no:randomly` and report the exit code, which must be 0. (c) THE MUTATION: in
    `<worktree>/packages/orchestration/job_evidence.py` — the exact path, and the bytes are unique
    inside it because `authority = sorted(` occurs there exactly once — delete the conjunct `and
    f.current_sha256` from that one statement, restoring its pre-round condition and nothing else.
    (d) Re-run the SAME command as (b) and report the exit code, which must be NON-ZERO, together
    with the assertion or error text, which must name `ValueError` and one of the two messages
    quoted in R-0837. (e) Report `git worktree list | wc -l` after removing the worktree and running
    `git worktree prune`.

G6  THE SCOPED SUITE, at C3, in the primary checkout, serially:
    `python3 -B -m pytest tests/orchestration/test_review_manual_completion_shapes.py
    tests/orchestration/test_review_subject_deletions.py tests/cli/test_golden_path.py -q
    -p no:randomly`. Report the exit code and the counts line verbatim. Exit code must be 0, and the
    passed count must be STRICTLY GREATER than 78, which is what the reviewer measured for this
    exact command line at `bb375019`. This selection carries the golden-path canary, so no separate
    canary run is owed.

G7  THE FULL SUITE, at C3, in the primary checkout: `python3 -m pytest -n auto -q`. Report the exit
    code and the final counts line VERBATIM. Then LIST every failing node id — the list may be
    empty, and "empty" is itself the reading to report. For EACH id in that list, re-run that id
    alone, serially, three times, and report the three exit codes; `tests/orchestration/
    test_product_smoke.py` produced exactly this shape at round 18 from one leaked port on one
    xdist worker, and the serial re-runs are how integration_gate.md step 4 tells the two apart.

G8  THE TREE, readings taken at C3 and reported in the handback. `git status --porcelain` EMPTY;
    `git ls-files .remedy-wt` EMPTY; `git worktree list | wc -l`; the change set of
    `git diff --name-only bb375019..C3`, which must be exactly the seven paths of the Change section
    other than `.agent/handoff.md`; and the INSERTION count of each of C0a, C0b, C1, C2 and C3
    separately, each of which must be at most 500 per AGENTS.md DECISION F104 D1. C4's own numbers
    are not ordered here and belong to the next round's ledger entry.


## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It has NO length cap. It carries:
the feature and round; SESSION 8 of F274; the branch; the commit SHAs; the changed-files table with
the real `git diff --numstat` columns; ONE LINE PER GATE G1 through G8 with that gate's real
result; the open-findings count; the item-status table with every ordered item exactly once; and
the deviations, stated plainly. Its state block repeats this line verbatim:

BEGIN FORTSCHRITT sha256=78f37ae26b3287e27e49480d9f578c3424dcf22644c524c0c18ea226e969344d bytes=291
Fortschritt: F274 schließt bei ~35 % des ursprünglichen Umfangs, Closure-Blocker R-0837 behoben, Integrationsgate BESTANDEN, F275 registriert (Löschkarte ✅ · Reachability-Ratsche ✅ · D1–D8 ✅ · F275 ✅ · Gate ✅ · Self-Use ✅ · R-0837 ✅ · Closure offen) — Schätzung
END FORTSCHRITT


Then push the branch. Do NOT open a pull request this round and do NOT merge anything.

BEGIN PLAN20 sha256=6c86b31441467619677a0d9dbdd36e674e2d62665ab9b2315cbd9c20258ac6be bytes=2631
# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Close F274 at the edge work it actually built and carry the cluster deletion, the atomic record
flip and the classic runner to F275, per DECISION F274 D8. F275 is registered, the integration
gate has PASSED and the self-use precondition is met; the close is BLOCKED by R-0837 until this
round lands its fix.

## Current Step

The R-0837 repair. `create_manual_completion_bundle` builds its attestation authority set from
every attestable changed path, including one this branch DELETED, then requires both that the task
partition cover that set exactly and that each task's safe diff yield exactly its own paths — which
a deleted file's safe diff never does. The two checks are jointly unsatisfiable, so the canonical
closure evidence producer refuses every deletion feature, and F274 and F275 are both one. This
round guards the comprehension with `f.current_sha256`, the idiom the same function already uses
twenty lines below it for `file_hashes`, and ships a regression test that goes red without it. Its
ledger commit books round 19's PASS verdict, registers R-0837 and R-0838 and appends the R-0784
recurrence.

## Next Steps

1. CLOSURE ROUND A: the ledger rotation by `scripts/rotate_live_review.py` as its own commit, then
   the evidence job and the fresh review zip. The zip's `base_commit` is the FORK POINT
   `13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, whose ancestry-path and plain `rev-list` counts are
   EQUAL — never `git merge-base`, which names `origin/main`'s tip here and gives unequal counts.
2. CLOSURE ROUND B: the STATUS `[x]` flip, the README sync and the one `consumed_by` edit setting
   `SU-013` to `f274`, in ONE commit; then the pull request, which is NOT merged this session.

## Risks

- The authority set is read from the WORKING TREE and not from the commit, so an untracked `.py`
  file under the repo root joins it and shifts every count the closure round reports. The tree is
  clean before the evidence job runs, and closure round A gates that first.
- The open High findings are R-0803, R-0804, R-0806 and R-0807, all F273's rather than this
  feature's, per DECISION F272 D12. The integrity gate's `high_blockers_open` check reports "no
  open blocker/high findings" and is WRONG while those four are open — that is R-0648, and
  DECISION F272 D17 requires the close to say so and to rest on the named list instead.
END PLAN20

BEGIN RECORD20 sha256=9f7fe20802dafc9ba04dfac35f3608be8146937e9081489dc81dc8220c1486f5 bytes=12426

Gate: F274 R19 — the F274 round 19 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER ITSELF against the COMMITTED blobs, in the primary checkout, at `1052824a`. Booked by round 20's ledger commit out of `.agent/handoff.md` at `bb375019`, which operator amendment amend0827-process-diet rule 1 makes a durable carrier, so no round was spent on the booking. RANGE `ae7607e6`..`1052824a`, six commits, every one single-parent, in the ordered sequence C0a, C0b, C1, C2, C3, C4. G1 TRANSPORT covered the chain this workflow can walk per §3 item 37 — the scratch original `.remedy-wt/f274-r19-FINAL.md` and both committed copies, all 29497 bytes at `68406001c27b4bbb8fa6ea25dabb723d7dae7092eda3721264dbb5ce24f1a655` — and claimed nothing about the emitted bytes. G2 THE PLAN at `f794c678`: byte-equal to its slice at 2504 bytes and 42 lines against the cap of 50. G3 THE RECORD APPEND at `16c9d070`: 628109 to 638448 bytes, exact append, N counted as 3, ordered equality true, the control on the FIRST appended paragraph at offset 628110 rejected by BOTH readers; units 243 to 246, `^Gate: ` 49 to 50, `^Gate: F274 R18 ` 0 to 1, the R-0819 recurrence line count 0 to 2, registrations 70 to 70, distinct resolutions 7 to 7, OPEN SET 63 TO 63 BY DISTINCT ID. G4 THE GENERATION at `0d66a45e`, read back through the shipped loader rather than out of the JSON: before the call `pending_self_use_items()` was 0 and `next_self_use_item()` was `None`; the appended entry is `SU-013`, "Address ledger finding R-0445", provenance `generated (self-use-generator tier 1, ledger scan, R-0445)`, `consumed_by` the EMPTY STRING; the queue went 38745 to 43764 bytes and 12 to 13 items; after the call pending is 1, next answers `SU-013`, and `SU-013` is the ONLY entry with a blank `consumed_by`, which is what leaves exactly one item for the closure commit to consume. G5 THE RUN: job `1a5b417ef7b64fe5`, state BLOCKED, task T001 blocked, 102.36 seconds of real provider time, `execution_config` naming `ollama` for both roles with the literal `fake` ABSENT, budgets `max_provider_calls=6` and `max_cost_usd=0.5`, and NOTHING APPLIED. G6 THE EVIDENCE DIRECTORY: seven files, every one `.txt`, none `.log`, and `run_defects.txt` agreeing with the handback at tuple length 2. G7 THE SCOPE GUARD PASSED AND ITS CAP CLAUSE FAILED, which the worker reported as failing rather than re-scoping: the range names twelve paths, all under `.agent/` or the single `scripts/self_use_queue.json`, with none under `packages/`, `apps/`, `tests/` or `docs/`; per-commit insertions are 300, 205, 15, 6 and 737 for C0a through C3, and C3 IS 237 OVER THE DECISION F104 D1 CAP OF 500. THE OVERSIZE COMMIT IS ACCEPTED UNDER THE AGENTS.md EXCEPTION and the reviewer measured condition (b) itself: across all 154 non-merge commits since the fork point, `0d66a45e` at 737 insertions is the ONLY one over 500, so it is this feature's single declared-oversize commit, and it was declared before review with its inseparability reason. THE DEFECT IS THE REVIEWER'S OWN: the round 19 block ordered C3 as ONE commit and resolved G4 through G8 at C3, which forced the queue edit, the run and a 579-line machine-generated `jobplan.txt` into a single plainly splittable commit. DECISION F272 D18 reserves this feature's one allowance for the LEDGER ROTATION on the ground that a rotation cannot be split, so the reviewer MEASURED the rotation rather than assuming D18's figure: run against a throwaway worktree at `1052824a`, `scripts/rotate_live_review.py` moves 32 gate records and 5 finding pairs and produces a commit of EIGHTY-EIGHT insertions — the ledger shrinking 638448 to 471740 bytes and the archive growing 2535031 to 2701739, with the script's own open-findings count 61 before and after — so D18's premise is true in general and false here, and no second oversize commit arises. G8 THE TREE: porcelain empty, `git ls-files .remedy-wt` empty, worktrees back to 14 with the throwaway branch deleted, unquoted `\bHEAD\b` zero in the RECORD19 slice. TEN DEVIATIONS WERE DECLARED AND THE REVIEWER SUSTAINS ALL TEN; five deserve naming. The job BLOCKED, which constraint 5 permits and which is recorded, not repaired. `run_job` created a second worktree and branch the block did not anticipate, `remedy/job-1a5b417ef7b64fe5`; the worker left the branch in place because protocol guardrail G2 forbids branch deletion beyond what is authorised, and fifteen such `remedy/job-*` branches already exist from earlier features, so this is the established state rather than litter. The block's claim that the persisted `JobPlan` lands in `dest_dir` is WRONG — it goes to `.data/jobs/<id>/job.json` via `data_paths.job_record_path`, and `.data/` is gitignored so the isolation held anyway; that is a reviewer prose error and earns the dated `.agent/prose_slips.md` line this round appends, not an id. The worker's first unit reader was defective, so it reverted the uncommitted ledger, corrected the reader and re-ran, with identical bytes both times. And the ollama daemon could not be probed directly because the session guard denies loopback `curl`, so the worker substituted the run's own evidence, which the reviewer had already confirmed independently before authoring.

- R-0837 — High, THE CANONICAL CLOSURE EVIDENCE PRODUCER CANNOT PACKAGE A BRANCH THAT DELETES A SOURCE FILE, SO IT BLOCKS THE CLOSURE OF EVERY DELETION FEATURE, AND F274 AND F275 ARE BOTH ONE. Found by the reviewer of round 19 while dry-running closure algorithm step 1, and RE-MEASURED INDEPENDENTLY by the reviewer of round 20 at `bb375019` rather than carried over from the handback. §3 item 30 was performed FIRST: the open set was searched for the DEFECT — for `create_manual_completion_bundle`, `authority`, `attestable`, `safe-diff path set`, `task partition` and `job_evidence` — and none of the fourteen registrations those terms return holds this defect, so this id is not a duplicate. THE MECHANISM. `packages/orchestration/job_evidence.py` builds the attestation authority set inside `create_manual_completion_bundle` as `sorted({f.path for f in subject.files if is_attestable_source(f.path)})`, which is the sole occurrence of `authority = sorted(` in that file. For this branch against the fork point `13dfaabd93d7b6452a1d23ca698e29ed47ecf035` that set holds 57 paths, one of which is `apps/cli/commands/feature_cmd.py`, DELETED by round 7 of this feature and correctly reported by `resolve_review_subject` with `status='deleted'` and `current_sha256=None`. The producer then requires the task partition to cover the authority set EXACTLY, and requires each task's `parse_safe_diff_paths(build_safe_diff_text(...))` to equal that task's own file list EXACTLY — and a deleted file's safe diff yields NO path at all. THE TWO CHECKS ARE THEREFORE JOINTLY UNSATISFIABLE, AND THE REVIEWER PROVED IT IN BOTH DIRECTIONS rather than reasoning about it, in a disposable worktree at `bb375019`: with the deleted file IN the partition the producer raises `ValueError: T001: safe-diff path set does not match the task partition`, and with it OUT the same producer raises `ValueError: task partition does not exactly cover the attestable authority set`. Those are the only two placements a path can have, so there is no third option. WHY HIGH: docs/roadmap/STATUS_closure_protocol.md algorithm step 2 makes a failing package a closure BLOCKER, so this defect stops any feature that deletes a file from closing at all, and both F274 and its follow-up F275 are deletion features by construction. THE FIX IS ONE CONJUNCT AND IT MATCHES AN IDIOM THE SAME FUNCTION ALREADY USES twenty lines below, where `file_hashes` is built with `if is_attestable_source(f.path) and f.current_sha256`: guard the authority comprehension the same way, so a file with no content at the branch tip is not asked to attest content it does not have. VERIFIED AND NOT MERELY PROPOSED: applied and committed in a disposable worktree at `bb375019`, the same producer call that failed twice above SUCCEEDS from both placements and returns `verdict PASS_WITH_RISKS` with `commit_count 158`. A SECOND MEASUREMENT THE CLOSURE ROUND NEEDS, found while taking the first: the authority set is read from the WORKING TREE and not from the commit, so an untracked `.py` file under the repo root joins it — the reviewer's own probe script did exactly that and moved the count from 57 to 58 until it was moved out of the worktree — which is why the evidence job runs only against a checkout that `git status --porcelain` reports empty. Resolved when the guard is on the branch with a regression test that goes red without it, and one closure package builds READY_FOR_REVIEW from a branch that deletes a source file.

- R-0838 — Low, THE SELF-USE GENERATOR RE-SELECTS A FINDING THAT AN ALREADY-CONSUMED QUEUE ITEM TARGETED, SO TWO CONSECUTIVE CLOSURES SPENT THEIR ONE SELF-USE ITEM ON THE SAME FINDING. Offered unprompted by the WORKER of round 19 and confirmed by the reviewer of round 20 against `scripts/self_use_queue.json` at `bb375019`. §3 item 30 was performed FIRST: `self_use_generator`, `self-use item` and `consumed_by` return R-0785, R-0786 and R-0826 as open findings against that same module, and not one of them is this defect — R-0785 is its `ensure_ascii` whole-file rewrite, R-0786 its file header contradicting its contents, R-0826 its defect reporter being blind to a budget stop — so this id is not a duplicate. MEASURED: `packages.orchestration.self_use_generator` tier 1 picks the oldest OPEN Low-or-Medium finding in `.agent/live_review.md` and does not exclude findings that an already-consumed queue entry targets, so `SU-012`, whose `consumed_by` is `F272`, and `SU-013`, whose `consumed_by` is the empty string and which was generated for this close, both carry the title `Address ledger finding R-0445` and the provenance `generated (self-use-generator tier 1, ledger scan, R-0445)`; `R-0445` is registered, carries no `Done:` line, and therefore stayed the oldest open Low-or-Medium finding across both closes. WHY LOW AND NOT MEDIUM: nothing on disk is wrong, both queue entries are honest records of what they actually ran, and every invariant the queue file states about itself still holds — what is defeated is the track's stated purpose, that each close makes Remedy use Remedy on something NEW, and that purpose fails exactly whenever the previous target is still open. Resolved when tier 1 excludes every finding an existing queue entry already targets, with a test that seeds a consumed entry against the oldest open Low-or-Medium finding and asserts the generator selects the next one instead.

RECURRENCE of R-0784 at F274 round 19, measured by the reviewer at `1052824a` and booked here by round 20's ledger commit. NO NEW ID IS SPENT: §3 item 30 requires the open set searched for the DEFECT before an id is minted, and R-0784 is OPEN and already holds this exact class — the self-use run a closure consumes ending BLOCKED at the approval gate, with both strings `describe_self_use_run_defects` returns registered because closure precondition 6 requires it. THE INSTANCE. `SU-013`'s run is job `1a5b417ef7b64fe5`, and the tuple that `.agent/selfuse_f274/run_defects.txt` records verbatim has length 2: `job 1a5b417ef7b64fe5 (blocked): task_T001_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail` and `T001 (blocked): completion_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail`. Those are byte-identical to R-0784's own two strings apart from the job id, and they are the job-level and the task-level view of ONE gate failure, so they take one id and not two. WHAT THIS RECURRENCE ADDS TO R-0784, and the reason it is booked rather than merely noted: THE CLASS SURVIVED A WHOLE FEATURE. R-0784 was registered from F272's closure run under a different job id, F274's closure run reproduced it exactly, and in both the configured local model spent its repair rounds on a task whose fix is a rule about reviewer practice rather than a code change any builder can make — `SU-012` and `SU-013` both target `R-0445`, which is finding R-0838 above and the reason the same unsuitable task was selected a second time. R-0784's severity of Low is UNCHANGED and the reviewer restates its ground: no Remedy code behaved wrongly, no state on disk is wrong, and an approval gate that refuses an unfinished job is the gate working.
END RECORD20

BEGIN SLIP20 sha256=f6ac7daf0ad3e5543ed00c1716faef6bd45a887d723e70903d3cb443bcfb502c bytes=321

2026-09-08 · F274 R19 · The round 19 block claimed the persisted `JobPlan` lands in the run's `dest_dir`, and it lands at `.data/jobs/<id>/job.json` through `data_paths.job_record_path` instead; `.data/` is gitignored, so the isolation the claim was offered as evidence for held anyway and nothing wrong reached disk.
END SLIP20

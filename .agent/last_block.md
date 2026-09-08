STEP — F274 ROUND 21 — R-0837's SECOND SITE: the review zip refuses the branch the producer now accepts

Goal: finish unblocking the F274 closure. Round 20 guarded the evidence producer and it builds. The
reviewer then DRY-RAN THE WHOLE CLOSURE PACKAGE before authoring the closure round, and step 2 of the
closure algorithm — the MANDATORY review zip — still refuses this branch, because
`scripts/build_review_zip.py` recomputes the attestable set independently, WITHOUT the guard, and
then requires it to EQUAL the authority set the producer wrote. The same conjunct at that second
site makes the package build READY_FOR_REVIEW. This round lands it with a two-test regression
module, proves both colours by mutation in a disposable worktree, and re-runs the whole suite. Its
ledger commit books round 20's PASS verdict and appends the second site to R-0837 WITHOUT minting
an id.

Base commit for every reading in this block: `630f22b9`.

WHAT THE REVIEWER MEASURED BEFORE AUTHORING, by RUNNING THE REAL CLOSURE PIPELINE and not by
reading code. At `630f22b9`, in a disposable worktree, `create_manual_completion_bundle` SUCCEEDS —
`verdict PASS_WITH_RISKS`, `authority_count 58`, `commit_count 163`, partition 20/20/18 — so round
20's fix holds. A real evidence bundle was then built from it and `bash scripts/make_review_zip.sh
--evidence-dir <dir>` was run for real: EXIT 2, with `REVIEW_ZIP_ERROR: authority set != attestable
ReviewSubject paths (only_in_authority=[], only_in_subject=['apps/cli/commands/feature_cmd.py'])`.
The guard below was then applied and committed in that same worktree, the evidence bundle
REGENERATED at the new tip, and the zip re-run: EXIT 0, `PACKAGE_STATUS=READY_FOR_REVIEW`,
`REVIEW_SUBJECT_ALIGNMENT=PASS`, `EVIDENCE_AUTHORITATIVE=true`, 3948 members,
`authoritative_count 59`, `tombstone_count 1`. That last number is why this fix loses no coverage:
the deletion is still attested, by the tombstone `ReviewFileV1.base_sha256` exists for, whose own
docstring says recording a deleted file is the POINT rather than a reason to drop it.

THE REVIEWER RECORDS ITS OWN MISTAKE PLAINLY, because the record is where that belongs: round 20
dry-ran the PRODUCER, found it green, and called the closure unblocked — when the closure is a
TWO-STEP algorithm and only step 1 had been run. The half that caught it is R-0837's own resolution
condition, which demands a package that actually reaches READY_FOR_REVIEW, and that condition is
UNCHANGED by this round.

WHAT THE REVIEWER READ IN THE FILES THIS BLOCK ORDERS CHANGED, per §3 item 34, with what it found.
(a) `scripts/build_review_zip.py` is 607 lines; `attestable_subject = {f.path for f in
subject.files` occurs EXACTLY ONCE, `is_attestable_source(f.path)` occurs EXACTLY ONCE, and the
guarded form `is_attestable_source(f.path) and f.current_sha256` occurs ZERO times. After the fix
the guarded form occurs once and the other two counts are unchanged, the first because it is the
statement's own opening and the second because it is a substring of the guarded form. (b) NO test
in this repository calls `_assert_authority_equality` — `ArchivePlanError` is named by
`tests/orchestration/test_review_zip_fail_closed.py`, `test_review_declared_empty_subject.py` and
`test_review_acquisition_budget.py`, and each covers the decoder and content-proof paths rather
than the authority-equality assertion. That is the gap this round closes, and it is why the new
tests go in a NEW module rather than into one of those three. (c) The module name
`tests/orchestration/test_review_zip_deleted_path_authority.py` is FREE at the base.

THE FIX AND ITS TESTS ARE DESCRIBED AND NOT SLICED, because production code is never reviewer-
authored bytes the worker only transcribes. The worker writes them; the gates below measure them.

FRAME CONVENTION. Every slice is delimited by a line reading `BEGIN <NAME> sha256=<hex> bytes=<n>`
and a line reading `END <NAME>`. THE SLICE IS THE BYTES STRICTLY BETWEEN THOSE TWO LINES — the
BEGIN line's own terminating newline is part of the BEGIN line and not part of the slice, and the
slice's final byte is the newline immediately preceding the END line. Marker lines never reach any
file. No line of this block's FRAME is a run of a single repeated character.


## Bundle — the commits of this round, in this order

C0a  Save this block verbatim as `.agent/authored/f274-r21.md`.
C0b  Mirror the same bytes into `.agent/last_block.md`.
C1   Replace `.agent/plan.md` with the PLAN21 slice.
C2   Append the RECORD21 slice to `.agent/live_review.md` — two paragraphs: round 20's PASS verdict
     and R-0837's SECOND SITE — and append the SLIPS21 slice to `.agent/prose_slips.md`.
C3   THE FIX AND ITS TESTS, in one commit: the guard in `scripts/build_review_zip.py` and the new
     regression module `tests/orchestration/test_review_zip_deleted_path_authority.py`.
C4   Rewrite `.agent/handoff.md` and hand back.


## Change — the exact set; nothing outside it is touched

    .agent/authored/f274-r21.md                                       (new, C0a)
    .agent/last_block.md                                              (rewrite, C0b)
    .agent/plan.md                                                    (rewrite, C1)
    .agent/live_review.md                                             (append, C2)
    .agent/prose_slips.md                                             (append, C2)
    scripts/build_review_zip.py                                       (C3)
    tests/orchestration/test_review_zip_deleted_path_authority.py     (new, C3)
    .agent/handoff.md                                                 (rewrite, C4)

THE GUARD, at C3. In `_assert_authority_equality` in `scripts/build_review_zip.py`, the statement
whose first line is `    attestable_subject = {f.path for f in subject.files` — the sole occurrence
in that file — gains the conjunct `and f.current_sha256` to its existing `is_attestable_source(
f.path)` condition, so the set it recomputes matches the one the producer writes. Wrap the
comprehension across two lines if the line would otherwise exceed the project's line length of 120;
the formatting is the worker's, the condition is not. Nothing else in that file changes. Put the
one-line WHY comment directly above the statement, per AGENTS.md Code Discoverability, naming that
a deleted path attests through its tombstone rather than through current content, and naming
R-0837.

THE REGRESSION MODULE, at C3, new at
`tests/orchestration/test_review_zip_deleted_path_authority.py`. `scripts/` is not on the default
import path for the suite, so the module inserts the repository's `scripts/` directory on
`sys.path` — derive it from `Path(__file__).resolve().parents[2] / "scripts"`, never from a
hard-coded absolute path — and imports `build_review_zip` inside the test bodies. It builds a real
`ReviewSubjectV1` from `packages.orchestration.review_subject` holding three real `ReviewFileV1`
records: two `modified` with a `current_sha256`, and one `deleted` with `current_sha256=None` and a
`base_sha256` set, which is the tombstone shape that type documents. It then calls
`_assert_authority_equality` directly, with `content_proof=None` and a `staged` stand-in whose
`load_json` returns `None` for every name, so that ONLY the attestable-subject comparison is
exercised. TWO tests, and the second is not optional:
  1. THE REGRESSION: authority = the two live paths, and the call MUST NOT RAISE. This is the
     assertion that fails without the guard.
  2. THE DISCRIMINATOR: authority = only ONE of the two live paths, and the call MUST still raise
     `ArchivePlanError` whose message contains `authority set != attestable ReviewSubject paths`.
     Without this second test the first one is satisfied by deleting the check entirely, and a
     guard test that cannot tell a fix from a deletion proves nothing.
The module docstring names R-0837 and states in one sentence what the unguarded coordinator does.


## Constraints

1.  Apply every slice BYTE FOR BYTE. If a slice looks wrong, apply it anyway and say so in the
    handback under deviations — the reviewer owns slice text, and a corrected slice is a finding
    against the reviewer, never a repair the worker performs.
2.  The change set above is exhaustive. A path outside it is not edited, created or deleted this
    round, and that includes every file under `docs/` and every other file under `scripts/`.
3.  ONE worker, this round only. Follow AGENTS.md in full: self-review loop before every commit,
    the Commit Gate, small commits, push after committing.
4.  NEVER work on `main`, never force-push, never rewrite history, and delete no branch.
5.  Every destructive check — the mutation of G5 — runs ONLY inside a disposable `git worktree`
    under the gitignored `.remedy-wt/`, never in the primary checkout. Remove that worktree and run
    `git worktree prune` before C4. `pytest` has no `norecursedirs` in this repository, so a
    worktree left in place is COLLECTED by the full run of G7; prune before G7, not after.
6.  The primary checkout satisfies `git status --porcelain` == EMPTY at the end of every commit.
7.  If ANY gate below comes back red, STOP: commit what is honestly finished, write the handback
    with the raw output, and hand back. Do not repair a red gate by re-scoping it, and do not edit
    a test to make a gate green.
8.  Report every gate's REAL exit code and REAL output. "Green" as a word is a finding against this
    round; the number or the transcript is the evidence.
9.  Do NOT build a review zip this round and do NOT run the evidence job. Those are closure round
    A's work, they need a clean tree at a settled head, and a package built now would be stale
    before it was recorded.
10. The full-suite run of G7 is NOT a claim that this feature's integration gate has re-passed —
    round 18 holds that claim and this round does not restate it. It runs because
    `scripts/build_review_zip.py` is on the packaging path that many suites import.


## Done when — eight gates, each RUN and each REPORTED with its real output

G1  TRANSPORT, at C0b. `sha256sum` of `.remedy-wt/f274-r21-FINAL.md`, of the committed
    `.agent/authored/f274-r21.md`, and of the committed `.agent/last_block.md`. Report all three
    digests and all three byte counts. The three digests must be EQUAL. This proves the chain
    scratch-original to saved copy to mirror and claims nothing about the bytes the reviewer
    emitted, per §3 item 37.

G2  THE PLAN, at C1. Report `wc -c` and `wc -l` of `.agent/plan.md`; it must be byte-identical to
    the PLAN21 slice at 2869 bytes and 45 lines, which is under the AGENTS.md cap of 50. Report
    that `## Goal` and `## Next Steps` each occur in it.

G3  THE APPENDS, at C2, with full byte forensics for `.agent/live_review.md` because it is the
    record. (a) BYTES: report the file's size before and after; the reviewer measured 650874 before
    at `630f22b9` and the RECORD21 slice at 7688 bytes, so after must be 658562. (b) EXACT APPEND:
    the pre-commit blob is a byte-exact PREFIX of the post-commit file, and the slice is an exact
    SUFFIX of it — report both booleans. (c) ORDERED EQUALITY, by a reader independent of (b):
    split the whole post-commit file on blank lines, COUNT the slice's own paragraphs into N rather
    than taking N from this block, and compare the file's LAST N units against the slice's N
    paragraphs IN ORDER; report N and the boolean. (d) NEGATIVE CONTROL on the FIRST appended
    paragraph: flip one byte inside it, in scratch and never in the tracked file, and report that
    BOTH the reader of (b) and the reader of (c) REJECT it. (e) COUNTS over the post-commit file:
    blank-line units 250 to 252; `^Gate: ` 51 to 52; `^Gate: F274 R20 ` 0 to 1; `^SECOND SITE of
    R-0837 ` 0 to 1; distinct `^- R-\d+ — ` ids 72 to 72; distinct `^Done: R-\d+ — ` ids 7 to 7;
    and the OPEN SET BY DISTINCT ID 65 to 65 — this round registers NOTHING, deliberately, because
    §3 item 30 forbids a second id for a defect the set already holds. (f) THE SLIPS:
    `.agent/prose_slips.md` is an exact append of SLIPS21, 165189 bytes to 165972, gaining exactly
    TWO blank-line units. (g) Report the count of unquoted `\bHEAD\b` in the RECORD21 slice with
    every backtick-quoted span deleted first; it must be 0.

G4  THE GUARD, at C3. Report `git show --numstat C3 -- scripts/build_review_zip.py` and the FULL
    `git diff` of that file for C3, verbatim. In the post-commit file report the count of
    `attestable_subject = {f.path for f in subject.files`, which must be 1; of
    `is_attestable_source(f.path)`, which must be 1; and of `is_attestable_source(f.path) and
    f.current_sha256`, which must be 1 where it was 0. Then `ruff check
    scripts/build_review_zip.py tests/orchestration/test_review_zip_deleted_path_authority.py` and
    report its exit code and output.

G5  THE RED-PROOF, in a disposable worktree at C3 under `.remedy-wt/`, never in the primary
    checkout. (a) IMPORT PROOF FIRST, because an editable install of this project exists and has
    shadowed a worktree before: with the worktree as the working directory, run `python3 -B -c
    "import packages.orchestration.review_subject as m; print(m.__file__)"` and report the path,
    which must be inside that worktree. (b) THE UNMUTATED CONTROL, in that same worktree and BEFORE
    any mutation: `python3 -B -m pytest tests/orchestration/test_review_zip_deleted_path_authority.py
    -q -p no:randomly`; report the exit code, which must be 0, and the counts line, which must
    report 2 passed. (c) THE MUTATION: in `<worktree>/scripts/build_review_zip.py` — the exact
    path, and the bytes are unique inside it because `attestable_subject = {f.path for f in
    subject.files` occurs there exactly once — delete the conjunct `and f.current_sha256` from that
    one statement, restoring its pre-round condition and nothing else. (d) Re-run the SAME command
    as (b) and report the exit code, which must be NON-ZERO, and the counts line, which must report
    EXACTLY 1 failed and 1 passed. BOTH halves of that count are the gate: the failing test is the
    regression, and the PASSING one is the discriminator proving the mutation did not simply
    disable the check. Report which test id failed. (e) Report `git worktree list | wc -l` after
    removing the worktree and running `git worktree prune`.

G6  THE SCOPED SUITE, at C3, in the primary checkout, serially:
    `python3 -B -m pytest tests/orchestration/test_review_zip_deleted_path_authority.py
    tests/orchestration/test_review_zip_fail_closed.py
    tests/orchestration/test_review_declared_empty_subject.py
    tests/orchestration/test_review_authoritative_e2e.py
    tests/orchestration/test_review_packaging_dirty_disposition.py tests/cli/test_golden_path.py -q
    -p no:randomly`. Report the exit code and the counts line verbatim. Exit code must be 0, and
    the passed count must be EXACTLY 69: the reviewer measured 67 for the same selection WITHOUT
    the new module at `630f22b9`, and this round adds exactly two tests. This selection carries the
    golden-path canary, so no separate canary run is owed.

G7  THE FULL SUITE, at C3, in the primary checkout, with every disposable worktree already pruned:
    `python3 -m pytest -n auto -q`. Report the exit code and the final counts line VERBATIM. Then
    LIST every failing node id — the list may be empty, and "empty" is itself the reading to
    report. For EACH id in that list, re-run that id alone, serially, three times, and report the
    three exit codes; `tests/orchestration/test_product_smoke.py` produced exactly this shape at
    rounds 18 and 20 from one leaked port on one xdist worker, and the serial re-runs are how
    docs/agents/integration_gate.md step 4 tells a flake and a regression apart.

G8  THE TREE, readings taken at C3 and reported in the handback. `git status --porcelain` EMPTY;
    `git ls-files .remedy-wt` EMPTY; `git worktree list | wc -l`; the change set of
    `git diff --name-only 630f22b9..C3`, which must be exactly the seven paths of the Change
    section other than `.agent/handoff.md`; and the INSERTION count of each of C0a, C0b, C1, C2 and
    C3 separately, each of which must be at most 500 per AGENTS.md DECISION F104 D1. C4's own
    numbers are not ordered here and belong to the next round's ledger entry.


## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It has NO length cap. It carries:
the feature and round; SESSION 8 of F274; the branch; the commit SHAs; the changed-files table with
the real `git diff --numstat` columns; ONE LINE PER GATE G1 through G8 with that gate's real
result; the open-findings count; the item-status table with every ordered item exactly once; and
the deviations, stated plainly. Its state block repeats this line verbatim:

BEGIN FORTSCHRITT sha256=e6cde7c5462b0ab92e5ee7e46eadb9f4433bcd27bb7e79545ff966e996dbfff8 bytes=304
Fortschritt: F274 schließt bei ~35 % des ursprünglichen Umfangs, Closure-Blocker R-0837 an BEIDEN Stellen behoben, Paket als READY_FOR_REVIEW nachgewiesen (Löschkarte ✅ · Reachability-Ratsche ✅ · D1–D8 ✅ · F275 ✅ · Gate ✅ · Self-Use ✅ · R-0837 ✅ · Closure offen) — Schätzung
END FORTSCHRITT


Then push the branch. Do NOT open a pull request this round and do NOT merge anything.

BEGIN PLAN21 sha256=bf5c3c345041876f1de426e76d5a1c7790db159441930b364605f266eb66bb76 bytes=2869
# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Close F274 at the edge work it actually built and carry the cluster deletion, the atomic record
flip and the classic runner to F275, per DECISION F274 D8. F275 is registered, the integration gate
has PASSED and the self-use precondition is met; the close is BLOCKED by R-0837 until BOTH of its
sites are guarded.

## Current Step

R-0837's SECOND SITE. Round 20 guarded the evidence producer and it now builds, but the reviewer
dry-ran the whole closure package before authoring the closure round and the MANDATORY review zip
still refuses this branch: `scripts/build_review_zip.py` recomputes the attestable set
independently, without the `current_sha256` guard, and then requires it to EQUAL the authority set
the producer wrote. The two comprehensions are one rule with two spellings, so narrowing one side
alone converts a producer failure into a packager refusal. This round applies the same conjunct at
the second site and ships a two-test regression module — one test for the deleted path, one
discriminator proving a genuinely missing live path STILL blocks — and its ledger commit books
round 20's PASS verdict and appends the second site to R-0837 without minting an id.

## Next Steps

1. CLOSURE ROUND A: the ledger rotation by `scripts/rotate_live_review.py` as its own commit, then
   the evidence job and the fresh review zip, built from a CLEAN tree. The package's `base_commit`
   is the FORK POINT `13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, whose ancestry-path and plain
   `rev-list` counts the reviewer measured EQUAL at 163 — never `git merge-base`, which names
   `origin/main`'s tip `d0d8b24d` here and gives unequal counts.
2. CLOSURE ROUND B: the STATUS `[x]` flip, the README sync and the one `consumed_by` edit setting
   `SU-013` to `f274`, in ONE commit; then the pull request, which is NOT merged this session.

## Risks

- The authority set is read from the WORKING TREE and not from the commit, so an untracked `.py`
  file under the repo root joins it and shifts every count the closure round reports. `pytest` has
  no `norecursedirs` here either, so a leftover worktree under `.remedy-wt/` is collected by a full
  run. The tree is clean and the worktrees are pruned before the evidence job.
- The open High findings are R-0803, R-0804, R-0806 and R-0807, all F273's rather than this
  feature's, per DECISION F272 D12. The integrity gate's `high_blockers_open` check reports "no
  open blocker/high findings" and is WRONG while those four are open — that is R-0648, and
  DECISION F272 D17 requires the close to say so and to rest on the named list instead.
END PLAN21

BEGIN RECORD21 sha256=51c890060afcfb9966e1ec4e9073d0f518f4670f967332734fe0d40af3c3210a bytes=7688

Gate: F274 R20 — the F274 round 20 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER ITSELF against the COMMITTED blobs, in the primary checkout, at `630f22b9`. Booked by round 21's ledger commit out of `.agent/handoff.md`, which operator amendment amend0827-process-diet rule 1 makes a durable carrier, so no round was spent on the booking. RANGE `bb375019`..`630f22b9`, six commits, every one single-parent, in the ordered sequence C0a, C0b, C1, C2, C3, C4, and the branch is pushed and in sync. G1 TRANSPORT: the scratch original `.remedy-wt/f274-r20-FINAL.md` and both committed copies are all 32833 bytes at `d5fc3280b35c9b22d6639cde2e859b2e2aed03435ad6ad4a2bd6b77e57a1ffac`; the chain walked is scratch-original to saved copy to mirror, and nothing is claimed about the emitted bytes, per §3 item 37. G2 THE PLAN at `5dbaec86`: byte-equal to its slice at 2631 bytes and 43 lines against the cap of 50, with `## Goal` and `## Next Steps` once each. G3 THE APPENDS at `b6827f2a`: `.agent/live_review.md` 638448 to 650874 bytes, the pre-commit blob an exact PREFIX and the slice an exact SUFFIX, N counted as 4 from the slice itself, ordered equality true, and the negative control on the FIRST appended paragraph at offset 638449 — `G` to `g` — REJECTED by BOTH readers; units 246 to 250, `^Gate: ` 50 to 51, `^Gate: F274 R19 ` 0 to 1, `^RECURRENCE of R-0784 ` 0 to 1, registrations 70 to 72, distinct resolutions 7 to 7, OPEN SET 63 TO 65 BY DISTINCT ID; `.agent/prose_slips.md` 164868 to 165189, exact append, exactly one unit gained; and unquoted `\bHEAD\b` in the RECORD20 slice, backtick-quoted spans deleted first, 0. G4 THE GUARD at `cacd42af`: numstat 3 insertions and 1 deletion, `authority = sorted(` occurring once and `is_attestable_source(f.path) and f.current_sha256` twice, both strings the source-text hygiene guard forbids still ABSENT, and `ruff check` exit 0 over both changed files. G5 THE RED-PROOF, RE-RUN BY THE REVIEWER IN ITS OWN DISPOSABLE WORKTREE and not read from the handback: the module resolved inside that worktree rather than to the editable install, the UNMUTATED control exited 0 at 1 passed, the revert target was unique with `authority = sorted(` occurring exactly once, and with the conjunct deleted the SAME node id exited 1 with `ValueError: T002: safe-diff path set does not match the task partition` raised at `job_evidence.py:3081` — so the mutation reaches the test and the test is not decorative. G6 THE SCOPED SUITE: exit 0 at 79 passed against the 78 the reviewer measured for that exact command line before the round, the golden-path canary inside the selection. G7 THE FULL SUITE, and the two runs DISAGREED, which is recorded rather than smoothed: the worker measured exit 0 at 19768 passed with an EMPTY failing list, and the reviewer's own run measured exit 1 at 1 failed and 19767 passed, the single failure being `tests/orchestration/test_product_smoke.py::TestAppStartsGreen::test_a_clean_app_passes`. The reviewer attributed it rather than assuming it: three serial re-runs of that node id all exit 0, which is the SERIAL-PASS xdist-flake class docs/agents/integration_gate.md step 4 records rather than treats as a blocker; the same FILE produced the same shape at round 18 from one leaked port on one xdist worker; and the file imports nothing this round touched, reaching `socket` and 75 port references and no evidence module. G8 THE TREE: porcelain empty, `git ls-files .remedy-wt` empty, 14 worktrees, the range path set exactly the seven declared paths, and per-commit insertions 289, 241, 22, 10 and 61 for C0a through C3, every one under the DECISION F104 D1 cap of 500 — this round declared NO oversize commit. EIGHT DEVIATIONS WERE DECLARED AND THE REVIEWER SUSTAINS ALL EIGHT; three deserve naming. `ruff` ran as `python3 -m ruff` because the session guard denies the bare executable, which is the same tool over the same paths and the reviewer's own re-run used the same route for exit 0. Exit codes were captured through an explicit-argv `subprocess.run` wrapper because the guard rejects `$?` by form and a pipe reports the pipe's status, which is the correct workaround and not a weakening. And the mutation of G5 left C3's two-line WHY comment in place while restoring only the CONDITION, which cannot affect behaviour and which the reviewer's independent re-proof reproduced. TWO PROSE SLIPS OF THE REVIEWER'S OWN are appended to `.agent/prose_slips.md` by this same commit and neither reached disk: the block's frame convention said a slice's leading newline was INCLUDED, which read literally makes every slice one byte, and gate G5 quoted the `T001` form of a message whose task id is fixture-dependent and actually arrived as `T002`.

SECOND SITE of R-0837 at F274 round 21, found by the reviewer while DRY-RUNNING the whole closure package before authoring the closure round, and measured at `630f22b9`. NO NEW ID IS SPENT: §3 item 30 requires the open set searched for the DEFECT before an id is minted, and R-0837 is OPEN and IS this defect — a branch that deletes a source file cannot be packaged — so this is one defect at a second site, not a second defect. WHY ROUND 20 COULD NOT SEE IT: R-0837's fix makes `create_manual_completion_bundle` succeed, and it does, which the reviewer re-measured at `630f22b9` where it returns `verdict PASS_WITH_RISKS`, `authority_count 58`, `commit_count 163` and a three-way partition of 20, 20 and 18 files. But the producer is only step 1 of docs/roadmap/STATUS_closure_protocol.md's algorithm. Step 2, the MANDATORY review zip, still refuses the same branch: run for real at `630f22b9` against a real evidence bundle, `bash scripts/make_review_zip.sh --evidence-dir <dir>` exits 2 with `REVIEW_ZIP_ERROR: authority set != attestable ReviewSubject paths (only_in_authority=[], only_in_subject=['apps/cli/commands/feature_cmd.py'])`. THE MECHANISM. `scripts/build_review_zip.py`, inside `_assert_authority_equality`, recomputes the attestable set INDEPENDENTLY as `{f.path for f in subject.files if is_attestable_source(f.path)}` — the very comprehension R-0837 guards in the producer, unguarded here — and then requires it to EQUAL the authority set the producer wrote. Narrowing one side without the other converts a producer failure into a packager refusal, so the two comprehensions are ONE rule with two spellings and both must carry the guard. THE FIX IS THE SAME CONJUNCT, AND THE REVIEWER PROVED IT END TO END rather than proposing it: applied and committed in a disposable worktree at `630f22b9`, the evidence bundle regenerated at that worktree's new tip and `make_review_zip.sh` re-run, the package builds `PACKAGE_STATUS=READY_FOR_REVIEW` with `REVIEW_SUBJECT_ALIGNMENT=PASS`, `EVIDENCE_AUTHORITATIVE=true`, 3948 members, `authoritative_count 59` and `tombstone_count 1`. THAT LAST NUMBER IS THE POINT AND IT ANSWERS THE OBVIOUS OBJECTION: the deletion is still ATTESTED, through the tombstone that `ReviewFileV1.base_sha256` exists for and whose docstring says a deleted file's record is the POINT rather than a reason to drop it, so excluding a deleted path from the CURRENT-CONTENT authority set costs no coverage at all. R-0837's RESOLUTION CONDITION IS UNCHANGED AND IT IS THE HALF THAT CAUGHT THIS: it requires not only the guard and its red-proof but that ONE CLOSURE PACKAGE BUILDS READY_FOR_REVIEW FROM A BRANCH THAT DELETES A SOURCE FILE — false while only the producer was guarded, and true only with both sites guarded. The lesson the reviewer records against itself: round 20 dry-ran the PRODUCER and called the closure unblocked, when the closure is a two-step algorithm and only step 1 had been run.
END RECORD21

BEGIN SLIPS21 sha256=b126c4e5d1c5dbac857d5e3d48fcd15f8ec1bf9ef33d9702c1746dac55ac9a48 bytes=783

2026-09-08 · F274 R20 · The round 20 block's frame convention said a slice is the bytes between its markers "its leading newline and its trailing newline INCLUDED", which read literally makes every slice one byte long and matches no digest; the worker resolved it correctly as the bytes strictly between the marker lines, all four slices matched their stamped sha256 and byte count, and nothing wrong reached disk.

2026-09-08 · F274 R20 · The round 20 block's gate G5(d) required the mutated run to name one of the two messages quoted in R-0837 and quoted the `T001` form, while the task id in that message is fixture-dependent and the run correctly produced `T002`; the worker met the substance without declaring a deviation and the reviewer's own re-proof reproduced `T002`.
END SLIPS21

── STEP CLOSURE — F275 — ROUND 108 ──
Goal: CLOSURE ROUND A. Book round 107's verdict and the two recurrences; rotate the ledger as
its own commit; from a clean tree at that commit run the evidence job and build a fresh review
package that reaches READY_FOR_REVIEW; run the full suite once; hand back the five values the
STATUS line is authored from.

Base commit: `7040f192`. Round type: CLOSURE SEQUENCE, the one exception to the ban on
bookkeeping rounds. Read `docs/roadmap/STATUS_closure_protocol.md` and the amend0914-f275-sprint
paragraph of `docs/agents/self_drive_protocol.md` first.

THE FRAME RULE, per item 37 of §3, stated as the property MEASURED over the final bytes: NO LINE
of this block is a run of a single repeated character, and every box-drawing rule inside the
STEP and SLICE header lines is exactly two characters long.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f275-r108.md`, the block as received
C0b `.agent/last_block.md`, the block as received
C1 THE BOOKKEEPING COMMIT: `.agent/plan.md` gets slice PLAN108 as a full replacement;
   `.agent/live_review.md` gets slice RECORD108 appended
C2 THE ROTATION: `python3 -B scripts/rotate_live_review.py` from the primary checkout's root,
   with no arguments; its own commit, of `.agent/live_review.md` and
   `.agent/live_review_archive.md` only. C2 IS THE ACCEPTED HEAD.
   Then, committing nothing: SPEC E, the evidence job, and SPEC Z, the review package.
C3 `.agent/authored/f275-r108-suite.txt`, per SPEC S
C4 `.agent/handoff.md`, the handback

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3.

## Change — exactly these paths and no others

The Bundle's paths. The evidence directory and the package are untracked artifacts, never
committed. `docs/roadmap/STATUS.md`, `README.md` and `scripts/self_use_queue.json` are NOT
touched: they belong to closure round B's one closure commit.

## SPEC E — the evidence job, at C2, in the primary checkout

E1 THE BASE. With base `a5bf894946ab6de053a4232109d6341a63533768`, the fork point: the counts of
`git rev-list --ancestry-path <base>..<C2>` and `git rev-list <base>..<C2>` are EQUAL, the base
is an ancestor of `origin/main`, and `git status --porcelain` is empty; otherwise STOP.
E2 THE VERIFICATION RECORD, from a real run at C2 of
`python3 -B -m pytest tests/docs/ -q -p no:randomly` and a real `--collect-only` of the same
selection, with `PYTHONPATH`, `REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed. Node ids are the
collect-only lines containing `::`. One entry, these fields and no others: `run_id` `vr-0001`;
`command`; `exit_code`; `passed`; `failed`; `skipped`; `deselected`; `selected`, equal to
passed plus failed plus skipped; `node_ids`, whose length equals `selected`; `test_files`, the
node ids' file paths, sorted; `stdout_summary`, the run's stdout, its last 4000 characters;
`output_hash`, the sha256 hex of exactly that string; `head_sha`; `duration_seconds`. Pre-scan
every node id and test file with `_unsafe_text` from `scripts/build_review_manifest.py`, loaded
by file path; any flag is a STOP.
E3 THE PRODUCER. Call `packages.orchestration.job_evidence.create_manual_completion_bundle` with
`evidence_dir` a fresh directory under `.remedy-wt/r108w/`; `repo_root` the primary checkout;
`base_commit` the fork point; `head_commit` the full sha of C2; `job_id` from
`secrets.token_hex(8)`; `job_title` `F275 one world completion part three closure evidence`;
`step_range` `T001-T003`; `prior_job_ids` the empty list; `verification_runs` the one entry;
`review_feature_id` `f275`; `timestamp` and `generated_at` one ISO-8601 UTC value.

## SPEC Z — the review package, after SPEC E

With `git status --porcelain` empty and the branch pushed through C2:
`bash scripts/make_review_zip.sh --evidence-dir <SPEC E's directory>` from the primary checkout's
root. Do not move, rename or delete the package it prints.

## SPEC S — the suite, once, after SPEC Z and before C3

From the primary checkout's root, serially:
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, with `PYTHONPATH`,
`REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`, output under
`.remedy-wt/r108w/`. The transcript file holds: line 1 `EXIT=<pytest's return code>`; line 2 the
run's last output line with its leading and trailing `=` and spaces stripped; then every distinct
bad node, the text after a line-initial `FAILED ` or `ERROR ` up to the first ` - `, sorted.

## Constraints

1. NO SLICE IS EDITED. PLAN108 and RECORD108 land byte for byte.
2. READ `.agent/STOP` before C0a, before C2 and before C4, with real exit codes.
3. The rotation is run by the SCRIPT, never by hand. If it refuses, STOP and report its stderr.
4. A red gate, a refusal or a package other than READY_FOR_REVIEW is a STOP: commit what is
   honestly finished, hand back with the raw output. A failing package is a CLOSURE BLOCKER.
5. No `.py` file under `.agent/`; scratch under `.remedy-wt/r108w/`, uncommitted. The reviewer's
   `.remedy-wt/r101/` is not opened.
6. No `gh`, no `remedy`, no pull request, no merge, NEVER a force-push, no history rewrite, no
   branch created or deleted, no worktree. Push after C1, C2, C3 and C4. Nothing is deleted.
7. Do NOT flip the STATUS line, touch `README.md`, set any `consumed_by` or write a `Done:` line.
8. The package `remedy-review-20260914-230148-READY_FOR_REVIEW.zip` already in
   `/home/decodeux/Repos/remedy-history/zips/` is the reviewer's dry run from a throwaway head,
   `847335e2`, and is NOT this closure's package; leave it and name it in the handback as such.
9. THE BLOCK'S OWN SIZE, measured on its final bytes: 216 lines TOTAL and 164 lines of
   PROSE, against the caps of 490 and 400.
10. GATE ORDER. G1 runs at C1, G2 at C2, G3 and G4 after C2 and before the suite, G5 after the
    suite with its committed-transcript reading at C3, and G6 after C3. Nothing runs after C4.
11. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and
    no subject carries a leading-slash token or an absolute path.

## Done when — the gates, each run for real and its exit code recorded

G1 TRANSPORT AND BOOKKEEPING, at C1. The sha256 of `.agent/authored/f275-r108.md` at C0a equals
the block digest received, and `.agent/last_block.md` at C0b is byte-identical to it. The slices
FOUND, each against its BEGIN-marker sha256. `.agent/plan.md` at C1 is byte-identical to PLAN108,
at most 50 lines, one `## Goal` and one `## Next Steps`. The blob
`git show 7040f192:.agent/live_review.md`, whose length there is 1195998 bytes, followed by
RECORD108 equals the file at C1. Lines matching `^Gate: F\d+ R\d+ — ` read 129 at `7040f192` and
130 at C1, with `Gate: F275 R107 — ` once. The open set BY DISTINCT ID reads 89 at both with
identical membership.

G2 THE ROTATION, at C2. The script's FULL stdout: the reviewer's dry run of the same script on
the same appended ledger moved 23 gate records and 26 finding pairs, took the ledger from 1199598
to 952372 bytes and the archive from 2701739 to 2948965, and printed its own open-findings count
identical before and after. REPORT every figure; the property gated is that the script's count
and the distinct-id open set are each identical before and after, that `R-0784`, `R-0809`,
`R-0838` and `R-0880` are still registrations in the ledger, that the archive's bytes at C1 are an
exact prefix of its bytes at C2, and that `git show --numstat` of C2 names exactly the two paths
with at most 500 insertions.

G3 THE EVIDENCE JOB, per SPEC E. Report E1's two counts and booleans; the entry's `exit_code`,
`passed`, `selected`, the length of `node_ids` and `test_files`; the pre-scan's flag count; and the
producer's returned summary IN FULL with its `job_id` and `verdict`. The reviewer's dry run read
equal counts, 306 passed and selected, three test files, 0 flags, and the verdict
`PASS_WITH_RISKS`.

G4 THE PACKAGE, per SPEC Z, and the preconditions. Report the script's FULL stdout and its exit
code; `PACKAGE_STATUS`, which MUST be `READY_FOR_REVIEW`; `REVIEW_SUBJECT_ALIGNMENT`, which must
be `PASS`; `EVIDENCE_AUTHORITATIVE`, which must be `true`; the package filename; its SHA-256 as
printed and as recomputed from the file, which must agree; its absolute directory;
`member_count`, `authoritative_count` and `tombstone_count`; and the manifest's
`committed_review_subject` base and head, read OUT of the package, which must be the fork point
and C2. Then, from the primary checkout's root, `python3 -B -m pytest tests/docs/ -q` and
`python3 -B -m pytest tests/cli/test_golden_path.py -q`, both exit 0, and in Python
`packages.orchestration.integrity_gate.run_integrity_checks()`: its `.passed`, `.fail_count`, and
the `name`, `status` and `message` of the check named `high_blockers_open`, verbatim, beside the
open High findings you read from the ledger yourself.

G5 THE SUITE, per SPEC S. Report pytest's real exit code, the summary line and every bad node
with its last `E   ` line. Each bad node is re-run ALONE three times and reported FLAKY only if
all three pass. Bad nodes less FLAKY: MUST be none. At C3 the committed transcript equals the
file rebuilt from the saved stdout.

G6 TREE, PATH SET, CAP, after C3. `git status --porcelain` prints `''` and `git worktree list`
one row. The changed-path set of `7040f192`..C3 against the Bundle's paths other than
`.agent/handoff.md`: MISSING and EXTRA by name. One row per commit with insertions, deletions and
staged path count, and the commits reaching 500 insertions, named.

Handback: `.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 35 of feature F275 · round 108 · rounds so far 108`; the Commits table compared cell by
cell against G6, C4's row carrying no numbers; one Verification line per gate with its REAL exit
code; External actions; Deviations; one sentence of context self-assessment; and, in ONE clearly
headed block, the five values closure round B's STATUS line is authored from, spelled exactly as
the tools printed them:

    Evidence job   <job_id>
    package        <package filename>
    SHA-256        <hash>
    package path   <absolute directory>
    accepted HEAD  <full 40-character sha of C2>

`## Next` states `Operator questions open: 1`. NO SCOPE REPORT AND NO SESSION-LIMIT BANNER.

── SLICE PLAN108 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN108 sha256=17529c4d959189687096f4e48910542ee22fdefb64d1ba0915a94625a3ee9ef9
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. T001, T002 and T003 are DONE, the
Built State is current, the integration gate passed and the self-use precondition is met.

## Current Step

CLOSURE ROUND A. It books round 107's verdict with the recurrences of `R-0784` and `R-0838`
that the self-use run produced, then rotates the ledger by `scripts/rotate_live_review.py` as
its own commit, and from a clean tree at that commit runs the closure evidence job and builds a
fresh review package. The reviewer dry-ran this sequence at a throwaway head before authoring
it: the producer returns `PASS_WITH_RISKS` and the package builds `READY_FOR_REVIEW`. The
rotation commit is the accepted head; after it come only the suite transcript and the handback.

## Next Steps

1. CLOSURE ROUND B: book round 108's verdict, then the closure commit — the STATUS `[x]` line
   authored from round A's measured values, the README sync and `SU-014`'s `consumed_by` set to
   `F275`, in one commit — then the pull request, which is not merged in that session.

## Risks

- The package's `base_commit` is the FORK POINT `a5bf894946ab6de053a4232109d6341a63533768`,
  whose ancestry-path and plain `rev-list` counts the reviewer measured equal; never
  `git merge-base`, which names `d0aa833b` after this branch merged `main` in.
- The authority set is read from the WORKING TREE, so an untracked file or a leftover worktree
  changes what is packaged: the tree is clean and the worktrees pruned before the evidence job.
- A DRY-RUN PACKAGE IS IN THE ARCHIVE: `remedy-review-20260914-230148-READY_FOR_REVIEW.zip`
  in `/home/decodeux/Repos/remedy-history/zips/` was built from the reviewer's throwaway head
  `847335e2` and is NOT the closure package.
- The open High findings are R-0803, R-0804, R-0806 and R-0807, all F273's per DECISION F272
  D12; the integrity gate's `high_blockers_open` check does not see them, which is R-0648.
- The open set is 89 by distinct id, with `R-0784`, `R-0809`, `R-0838` and `R-0880` open.
END PLAN108

── SLICE RECORD108 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD108 sha256=260a21029dacf8e6d2ef66304c78177289a35688a657fcb3414fd7f335b6d081

Gate: F275 R107 — the F275 round 107 entry. VERDICT PASS. Written by the planner and reviewer of session 35 after reading the committed range `50171d2f`..`7040f192` and re-deriving every reading that bears on the verdict; the worker's report and its transcripts were evidence for no line below. It is booked here by the first commit of round 108 that writes the record, per operator amendment amend0827-process-diet rule 1.

WHAT THE TRANSPORT PROOF COVERS, per item 37 of §3. The committed `.agent/authored/f275-r107.md` and `.agent/last_block.md` equal the reviewer's original at 20169 bytes at `7040f192`; `.agent/plan.md` equals PLAN107; `.agent/live_review.md` at `d7b73d61` is byte-identical to the reviewer's own application of the 22 owner endings and RECORD107 to its blob at `50171d2f`, 1195998 bytes; and `.agent/prose_slips.md` and `.agent/decisions.md` there each equal their blob at `50171d2f` followed by their slice. The open set stayed 89 by distinct id with identical membership, and each of the 22 re-assigned ids carries one `Owner: F273.` ending.

THE SELF-USE PRECONDITION. At `6deab62c` `scripts/self_use_queue.json` holds its 13 earlier items unchanged and one more, `SU-014`, "Address ledger finding R-0445", with the provenance of the generator's tier 1 and an empty `consumed_by`, which the reviewer's own run of the generator against a copy had predicted. `.agent/selfuse_f275/` records the run of `run_next_self_use_item` on that item: job `c9720cf080b84cc0`, blocked, its one task `T001` blocked, an `execution_config` naming `ollama` for builder and reviewer in which `fake` does not appear, 140.1 seconds, and a defect tuple of length 2. Nothing the job proposed was applied: the round changed no path outside `.agent/` and that queue file.

THE SUITE. The committed transcript `.agent/authored/f275-r107-suite.txt` reads exit 0 with 18442 passed and 23 skipped and lists no bad node.

RECURRENCE of R-0784 at F275 round 107, measured by the reviewer at `7040f192` and booked here by round 108's ledger commit. NO NEW ID IS SPENT, per §3 item 30: R-0784 is OPEN and holds this exact class, the self-use run a closure consumes ending blocked at the approval gate with both strings `describe_self_use_run_defects` returns registered because closure precondition 6 requires it. THE INSTANCE. `SU-014`'s run is job `c9720cf080b84cc0`, and the tuple `.agent/selfuse_f275/run_defects.txt` records verbatim has length 2: `job c9720cf080b84cc0 (blocked): task_T001_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail` and `T001 (blocked): completion_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail`. They are byte-identical to R-0784's own two strings and to F274's recurrence apart from the job id, and they are the job-level and the task-level view of one gate failure, so they take one id and not two. R-0784's severity of Low is unchanged: no Remedy code behaved wrongly, and an approval gate that refuses an unfinished job is the gate working.

RECURRENCE of R-0838 at F275 round 107, measured by the reviewer at `7040f192` and booked here by round 108's ledger commit. NO NEW ID IS SPENT, per §3 item 30. The self-use generator selected `R-0445` a THIRD time: `SU-012`, consumed by F272, `SU-013`, consumed by F274, and `SU-014`, generated for this close, all carry the title `Address ledger finding R-0445`, because R-0445 is still the oldest open Low-or-Medium finding and tier 1 does not exclude a finding an existing queue entry targets. R-0838's severity of Low is unchanged, and its resolution condition stands as registered.
END RECORD108

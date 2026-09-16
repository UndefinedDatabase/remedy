── STEP CLOSURE — F261 — ROUND 27 ──
Goal: CLOSURE ROUND A. Book round 26's verdict and its recurrences; rotate the ledger as its own
commit; from a clean tree at that commit run the evidence job, build a fresh review package that
reaches READY_FOR_REVIEW and run the integrity check; hand back the five values the STATUS line
is authored from.

Base commit: `f2872a33`, on `feature/f261-cli-vocabulary-v2`. SESSION 7 of F261. Round type:
CLOSURE SEQUENCE, the one exception to the ban on bookkeeping rounds. Read AGENTS.md,
`docs/agents/self_drive_protocol.md` and `docs/roadmap/STATUS_closure_protocol.md` first.

THE FRAME RULE, per item 37 of §3, measured over the final bytes: NO LINE of this block that is
two or more characters long is a run of a single repeated character, and every box-drawing rule
inside the STEP and SLICE header lines is exactly two characters long.

ENVIRONMENT: `VAR=x cmd`, `env` and `export` are denied, so set environment in-process; `cp` is
denied, so copy with `shutil.copyfile`. Shell loops, `$(...)` and `$?` in a compound command are
refused by form, so write such checks as Python scripts under `.remedy-wt/f261r27w/`, and never
name a script after a standard-library module. Never call `run_job` or any runner.
`git branch --list 'remedy/job-*'` reads 17 lines at `f2872a33`; keep it so.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f261-r27.md`, the block file the delegating message names, by
    `shutil.copyfile`
C0b `.agent/last_block.md`, the same bytes
C1  THE RECORD, one commit: `.agent/plan.md` becomes slice PLAN27; slice RECORD27 is appended to
    `.agent/live_review.md`
C2  THE ROTATION: `python3 -B scripts/rotate_live_review.py` from the primary checkout's root,
    with no arguments; its own commit, of `.agent/live_review.md` and
    `.agent/live_review_archive.md` only. C2 IS THE ACCEPTED HEAD.
    Then, committing nothing: SPEC E, the evidence job; SPEC Z, the review package; the checks
    of G5.
C3  `.agent/handoff.md`, the handback; then `git push origin feature/f261-cli-vocabulary-v2`

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. Push after C1, C2 and C3. No pull request
is created.

## Change — exactly these paths and no others

The Bundle's paths. The evidence directory and the package are untracked artifacts, never
committed. `docs/roadmap/STATUS.md`, `README.md` and `scripts/self_use_queue.json` are NOT
touched: they belong to closure round B's one closure commit.

## The append

RECORD27 begins with an empty line, and `.agent/live_review.md` ends in a newline at `f2872a33`:
the append is the file's bytes followed by the slice's bytes, and nothing else.

## SPEC E — the evidence job, at C2, in the primary checkout

E1 THE BASE. With base `7cdde89b5d0dc8ef1fb96980105870e956699873`, the fork point: the counts of
`git rev-list --ancestry-path <base>..<C2>` and `git rev-list <base>..<C2>` are EQUAL, `git
merge-base --is-ancestor <base> origin/main` exits 0, and `git status --porcelain` is empty;
otherwise STOP.
E2 THE VERIFICATION RECORD, from a real run at C2 of
`python3 -B -m pytest tests/docs/ -q -p no:randomly` and a real `--collect-only` of the same
selection, with `PYTHONPATH`, `REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed. Node ids are the
collect-only lines containing `::`. One entry, these fields and no others: `run_id` `vr-0001`;
`command`; `exit_code`; `passed`; `failed`; `skipped`; `deselected`; `selected`, equal to passed
plus failed plus skipped; `node_ids`, whose length equals `selected`; `test_files`, the node ids'
file paths, sorted; `stdout_summary`, the run's stdout, its last 4000 characters; `output_hash`,
the sha256 hex of exactly that string; `head_sha`; `duration_seconds`. Pre-scan every node id and
test file with `_unsafe_text` from `scripts/build_review_manifest.py`, loaded by file path; any
flag is a STOP.
E3 THE PRODUCER. Call `packages.orchestration.job_evidence.create_manual_completion_bundle` with
`evidence_dir` a fresh directory under `.remedy-wt/f261r27w/`; `repo_root` the primary checkout;
`base_commit` the fork point; `head_commit` the full sha of C2; `job_id` from
`secrets.token_hex(8)`; `job_title` `F261 CLI vocabulary v2 closure evidence`; `step_range`
`T001-T003`; `prior_job_ids` the empty list; `verification_runs` the one entry;
`review_feature_id` `f261`; `timestamp` and `generated_at` one ISO-8601 UTC value.

## SPEC Z — the review package, after SPEC E

With `git status --porcelain` empty and the branch pushed through C2:
`bash scripts/make_review_zip.sh --evidence-dir <SPEC E's directory>` from the primary checkout's
root, with no `REMEDY_REVIEW_DIR` set, so the script's own default directory holds the package. Do
not move, rename or delete the package it prints.

## Constraints

1. NO SLICE IS EDITED. Extract each slice as the bytes strictly between its `BEGIN <NAME>` and
   `END <NAME>` lines and verify its sha256 before use; a discrepancy is DECLARED, never repaired.
2. READ `.agent/STOP` before C0a, before C2 and before C3, with real exit codes. If it exists:
   finish a half-written commit, write the handoff, push, stop.
3. The rotation is run by the SCRIPT, never by hand. If it refuses, STOP and hand back its stderr.
4. A red gate, a refusal, or a package other than READY_FOR_REVIEW is a STOP: commit what is
   honestly finished and hand back with the raw output. A failing package is a CLOSURE BLOCKER.
5. Scratch and scripts live under `.remedy-wt/f261r27w/`, uncommitted; no `.py` file under
   `.agent/`. Under `.remedy-wt/` open only `.remedy-wt/f261-block/` and your own directory. No
   worktree is created in this round.
6. Every commit other than C2 stays under 500 insertions, read as the first column of
   `git show --numstat --format= <commit>`. C2 is over it by construction, and the handback
   DECLARES it under AGENTS.md's declared-oversize exception with DECISION F272 D18's reason: the
   rotation cannot be split without leaving records in neither file or in both, and the script
   verifies every moved record by sha256; it is this feature's only such commit.
7. NEVER merge, open a pull request, force-push, rewrite history, create or delete a branch. No
   `remedy`, no `gh`. Do NOT flip the STATUS line, touch `README.md`, set any `consumed_by` or
   write a `Done:` line.
8. THE BLOCK'S OWN SIZE, measured on its final bytes: 235 lines TOTAL and 184 lines of PROSE,
   against the caps of 490 and 400, where PROSE is every line that is not a line of slice
   CONTENT — the `BEGIN` and `END` marker lines count as prose.
9. GATE ORDER. G1 and G2 after C1; G3 after C2; G4 after SPEC E; G5 after SPEC Z; G6 after G5 and
   before C3. No gate runs after C3; C3's own numbers are the reviewer's.
10. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and
    no subject carries a leading-slash token or an absolute path.

## Done when — every gate run for real, its exit code recorded

G1 TRANSPORT. The sha256 of `.agent/authored/f261-r27.md` at C0a equals the digest the delegating
message gives, and `.agent/last_block.md` at C0b is byte-identical to it; the slices FOUND, each
matching its BEGIN-marker sha256.

G2 THE RECORD, at C1. `.agent/plan.md` is byte-identical to PLAN27, at most 50 lines, with
`^## Goal$` once and `^## Next Steps$` once. `.agent/live_review.md` equals its `f2872a33` blob
followed by RECORD27, which the reviewer's own application reads as 1135907 bytes with sha256
`84301e032a64e0eb77caeb82c4940d21e6cb750fc94a27b05812a93feb480298`. `^Gate: F\d+ R\d+ — ` reads 135 at `f2872a33` and 136 at C1, with
`Gate: F261 R26 — ` 0 times and once; the open set by distinct id, the ids of `^- R-\d+ — ` lines
minus the ids of `^Done: R-\d+ — ` lines, reads 125 at both with identical membership.
`python3 -B -m pytest tests/docs/ -q` exits 0 at C1.

G3 THE ROTATION, at C2. Report the script's FULL stdout and exit code. The reviewer's dry run of
the same script on the same appended ledger moved 110 gate records and 7 finding pairs, took the
ledger from 1135907 to 620380 bytes and the archive from 2948965 to 3464492, printed its own
open-findings count as 123 before and after, and left `.agent/live_review.md` with sha256
`dfc4747d104149ad7a22e73c61df983bec9c7bc0ff06bf2cec697422a25d576c` and
`.agent/live_review_archive.md` with sha256
`271ee9e7a91d16dac8da56eeaa807b5d3dd010c64d934d667500843c5ff20552`; the two files at C2 MUST have those digests.
The distinct-id open set at C2 equals C1's; the archive's bytes at C1 are an exact prefix of its
bytes at C2; `git show --numstat --format=` of C2 names exactly the two paths — report its
insertions and deletions.

G4 THE EVIDENCE JOB, per SPEC E. Report E1's two counts, which must be equal, and the exit code
of the ancestry check; the entry's `exit_code`, `passed`, `selected`, the lengths of `node_ids`
and `test_files`; the pre-scan's flag count; and the producer's returned summary IN FULL with its
`job_id` and `verdict`. The reviewer's dry run, on a head without the two block-save commits, read
181 and 181, exit 0, 310 passed and selected, four test files, 0 flags, and `PASS_WITH_RISKS`.

G5 THE PACKAGE AND THE PRECONDITIONS, per SPEC Z. Report the script's exit code and every line of
its stdout of the form `NAME=value`; `PACKAGE_STATUS` MUST be `READY_FOR_REVIEW`,
`REVIEW_SUBJECT_ALIGNMENT` `PASS` and `EVIDENCE_AUTHORITATIVE` `true`. Report the package
filename; its SHA-256 as printed and as recomputed from the file, which must agree; its absolute
directory; and, read OUT of the package's `.review_zip_manifest.json`, `package_status` and
`committed_review_subject`'s `base_commit`, `head_commit` and `commit_count`, which must be the
fork point, C2 and E1's count. Then, from the primary checkout's root,
`python3 -B -m pytest tests/docs/ -q` and `python3 -B -m pytest tests/cli/test_golden_path.py -q`,
both exit 0; and in Python `packages.orchestration.integrity_gate.run_integrity_checks()`: its
`.passed`, `.fail_count`, and the `name`, `status` and `message` of the check named
`high_blockers_open`, verbatim, beside the open High findings you read from the ledger yourself.

G6 TREE, PATH SET, CAP. `git status --porcelain` prints `''`, `git worktree list` one row,
`git branch --list 'remedy/job-*'` 17 lines, and `git rev-parse HEAD` equals
`git rev-parse origin/feature/f261-cli-vocabulary-v2`. The changed-path set of `f2872a33`..C2
against the Bundle's paths other than `.agent/handoff.md`: MISSING and EXTRA by name. One row per
commit of `f2872a33`..C2 with insertions, deletions and staged path count, and the commits reaching
500 insertions, named.

## The handback, C3

`.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 7 of feature F261 · round 27 · rounds so far 27`, with one sentence of context
self-assessment. `## Commits` lists C0a to C2, each row's `+/-` cell equal to G6's reading of that
commit; C3's own numbers appear nowhere, per item 31 of §3. `## Verification` gives G1 to G6 with
real exit codes. It carries External actions, Authored-text proofs, Item-status, Deviations, and
constraint 6's declaration of C2. It carries, in ONE clearly headed block, the five values closure
round B's STATUS line is authored from, spelled exactly as the tools printed them:

    Evidence job   <job_id>
    package        <package filename>
    SHA-256        <hash>
    package path   <absolute directory>
    accepted HEAD  <full 40-character sha of C2>

It states the open findings at 125 by distinct id, with the High ids R-0803, R-0804 and R-0807,
and `Operator questions open: 1`. It carries NO new scope report and no session-limit banner, for
the reason round 26's handback gave. Its `## Next` names, in order: Phase 1 rule 1; the
reviewer's verdict on round 27; closure round B.

── SLICE PLAN27 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN27 sha256=e8fa0859261f87762db06e8865634fdd0041c8e1138a14017fc6b5a15c07c6e5
# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md` — as far as this feature reaches it; DECISION F261 D25
moves the rest to F280. The Built State is current, the integration gate passed and the
self-use precondition is met.

## Current Step

CLOSURE ROUND A. It books round 26's verdict with the recurrences of R-0645, R-0784 and R-0838
that round measured, then rotates the ledger by `scripts/rotate_live_review.py` as its own
commit, and from a clean tree at that commit runs the closure evidence job, the integrity check
and a fresh review package. The rotation commit is the accepted head; only the handback follows
it in this round.

## Next Steps

1. CLOSURE ROUND B: book round A's verdict, then the closure commit — the STATUS `[x]` line
   authored from round A's measured values, the README sync and `SU-015`'s `consumed_by` set to
   `F261`, in one commit — then the pull request, which is not merged in that session.
2. F280, which Rule A5 proposes once F261 is merged.

## Risks

- The package's `base_commit` is the FORK POINT `7cdde89b`, which is also the merge base
  because this branch has merged nothing in.
- The authority set is read from the WORKING TREE, so an untracked file or a leftover worktree
  changes what is packaged: the tree is clean and the worktrees pruned before the evidence job.
- The open High findings are R-0803, R-0804 and R-0807, none of them F261's; the integrity
  gate's `high_blockers_open` check does not see them, which is R-0648.
- The open set is 125 by distinct id; seven that F261 owned belong to F280 by DECISION F261 D25.
END PLAN27

── SLICE RECORD27 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD27 sha256=c951086e67d5bce35ea6eb28b6212820fe4e0387bae2b3e7707dc0d9ff05cc60

Gate: F261 R26 — the F261 round 26 entry. VERDICT PASS, AND THE INTEGRATION GATE OF `docs/agents/integration_gate.md` PASSES. Written by the planner and reviewer of session 42 after reading the committed range `ed3c82d1`..`f2872a33` and re-deriving every reading that bears on the verdict; the worker's report and its transcripts were evidence for no line below. It is booked here by the first commit of round 27 that writes the record, per operator amendment amend0827-process-diet rule 1. Only this entry may carry the full-suite claim, and it carries it.

WHAT THE TRANSPORT PROOF COVERS, per item 37 of §3. The committed `.agent/authored/f261-r26.md` at `8767a465` and `.agent/last_block.md` at `0c07789c` equal the reviewer's scratch original at 24460 bytes; `.agent/plan.md` at `1b03919a` equals PLAN26; `.agent/live_review.md` there equals its blob at `ed3c82d1` followed by RECORD26, 1130125 bytes, and `.agent/decisions.md` its blob followed by DEC26, 1432544 bytes. The `Gate:` count went from 134 to 135, and the open set stayed 125 by distinct id with identical membership. The range changes no path outside `.agent/` and `scripts/self_use_queue.json`.

THE GATE. The branch run, `python3 -m pytest -n auto -q -rfE` in the primary checkout at `1b03919a`, read exit 1 with 1 failed, 17652 passed and 23 skipped, and the reviewer's own run of the same command at `f2872a33` read the same summary with the same single failed id, `tests/cli/test_job_rerun_workspace_identity.py::TestNoFalseWorkspaceDrift::test_a_mutated_workspace_shows_blocking_drift`. The worker re-ran that id alone three times, each exit 0, which classes it flaky under step 4 of the gate procedure, and the reviewer's second run of the whole suite at `f2872a33`, with `-p no:randomly` added, read exit 0 with 17653 passed and 23 skipped. BRANCH-ONLY less flaky is therefore empty. The base run, in a throwaway worktree at the fork point `7cdde89b` with `apps/ui/node_modules` and `apps/ui/dist` copied at equal file and symlink counts and the build stamped newer than every source, read exit 0 with 18443 passed and 23 skipped; no dist file's mtime fell inside its window and `React UI not built` appears 0 times, so BASE-ONLY is empty. The passed counts differ by 791, of which the flaky id is 1, and `git diff --name-status 7cdde89b 1b03919a -- tests/` lists 22 test files deleted, 4 added and 4 renamed.

THE SELF-USE PRECONDITION. At `8e44bd6c` `scripts/self_use_queue.json` holds its 14 earlier items unchanged and one more, `SU-015`, "Address ledger finding R-0445", with the provenance of the generator's tier 1 and an empty `consumed_by`, which the reviewer's own run of the generator against a copy had predicted, 53810 bytes. `.agent/selfuse_f261/` records the run of `run_next_self_use_item` on that item: job `90395ff070d8486c`, blocked, its one task `T001` blocked, an `execution_config` naming `ollama` for builder and reviewer in which `fake` does not appear, 115.82 seconds, and a defect tuple of length 2. The worker's capture script raised after the call returned, and the worker read the state from the job record the run persisted rather than calling the runner again, and declared it; the reviewer loaded that record with `load_job_plan` and read the same state, tasks, providers and tuple. The run left one new branch, `remedy/job-90395ff070d8486c`, and nothing it proposed was applied.

RECURRENCE of R-0645 at F261 round 26, measured by the reviewer at `f2872a33` and booked here by round 27's ledger commit. NO NEW ID IS SPENT, per §3 item 30: R-0645 is OPEN and names this exact id as one of its instances. THE CAUSE, which R-0645 did not yet record: sampling `git status --porcelain --untracked-files=all` every 50 milliseconds during a full `-n auto` run of the primary checkout at `f2872a33` saw seven untracked files appear under `tests/regression/`, named with the prefixes `test_slow_`, `test_wrapper_slow_`, `test_wrapper_pass_`, `test_runtime_chain_` and `test_chain_pass_` that `tests/regression/test_resource_safety.py` gives the temporary test files it writes into the checkout. `worktree_identity` in `packages/orchestration/run_manifest.py` digests untracked files that are not ignored, so a test that reads the Remedy checkout's identity twice while such a file exists for one of the two readings sees `remedy_worktree_digest` drift, which is exactly the failure this id shows. Neither test file differs between `7cdde89b` and `f2872a33`, so the race is older than this branch. R-0645's severity of Low is unchanged.

RECURRENCE of R-0784 at F261 round 26, measured by the reviewer at `f2872a33` and booked here by round 27's ledger commit. NO NEW ID IS SPENT, per §3 item 30: R-0784 is OPEN and holds this exact class. THE INSTANCE. `SU-015`'s run is job `90395ff070d8486c`, and the tuple `.agent/selfuse_f261/run_defects.txt` records verbatim has length 2: `job 90395ff070d8486c (blocked): task_T001_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail` and `T001 (blocked): completion_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail`. They match R-0784's own two strings apart from the job id, and they are the job-level and the task-level view of one gate failure, so they take one id and not two. R-0784's severity of Low is unchanged.

RECURRENCE of R-0838 at F261 round 26, measured by the reviewer at `f2872a33` and booked here by round 27's ledger commit. NO NEW ID IS SPENT, per §3 item 30. The self-use generator selected `R-0445` a FOURTH time: `SU-012`, consumed by F272, `SU-013`, consumed by F274, `SU-014`, consumed by F275, and `SU-015`, generated for this close, all carry the title `Address ledger finding R-0445`. R-0838's severity of Low is unchanged, and its resolution condition stands as registered.
END RECORD27

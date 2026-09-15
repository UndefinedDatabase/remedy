── STEP T002/3 — F261 — ROUND 7 ──
Goal: Book round 6's PASS, record DECISION F261 D6, and rename the output-visible words of
`job apply` in three commits and add their guards in a fourth, each by applying a table; run the
suite once.

Base commit: `8b07c95b`, on `feature/f261-cli-vocabulary-v2`, the operator's commit after round 6.
SESSION 2 of F261. Read AGENTS.md, docs/agents/self_drive_protocol.md, and DECISIONs F261 D5 and
D6 once C1 has landed D6.

THE FRAME RULE, per item 37 of §3, measured over the final bytes: NO LINE of this block is a run
of a single repeated character, and every box-drawing rule inside the STEP and SLICE header
lines is exactly two characters long.

ENVIRONMENT: `VAR=x cmd`, `env` and `export` are denied, so set environment in-process; `cp` is
denied, so copy with `shutil.copyfile`; bare `ruff` is denied, so use `python3 -m ruff check`.
Shell loops, `$(...)` and `$?` in a compound command are refused by form, so write such checks
as Python scripts under `.remedy-wt/f261r7w/`; a pipe into `tail` hides pytest's exit code. The
editable install resolves `apps` and `packages` to the PRIMARY checkout, so a pytest run inside a
worktree goes through a runner script that changes into the worktree, puts it first on
`sys.path` and in `PYTHONPATH`, and asserts `packages.orchestration.job_apply` loaded from inside it.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f261-r7.md`, the block file the delegating message names, by
    `shutil.copyfile`
C0b `.agent/last_block.md`, the same bytes
C1  THE RECORD, one commit: `.agent/plan.md` becomes slice PLAN7; slice RECORD7 is appended to
    `.agent/live_review.md` and slice DEC6 to `.agent/decisions.md`
C2  STATUS VALUES AND REASON CODES: copy `.remedy-wt/f261-block/f261-r7-words-1.jsonl` to
    `.agent/authored/f261-r7-words-1.jsonl` and apply it per THE TABLES, in one commit
C3  THE JOB APPLY RECORD: the same with `f261-r7-words-2.jsonl`, in one commit
C4  THE TEXT: the same with `f261-r7-words-3.jsonl`, in one commit
C5  THE GUARDS: the same with `f261-r7-guard.jsonl`, in one commit
C6  `.agent/handoff.md`, the handback; then `git push origin feature/f261-cli-vocabulary-v2`

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. No pull request is created.

## Change — exactly these paths and no others

C0a to C1: `.agent/authored/f261-r7.md`, `.agent/last_block.md`, `.agent/plan.md`,
`.agent/live_review.md` and `.agent/decisions.md`. C2 to C5: each table's own carrier and the
paths G3 and G4 name. C6: `.agent/handoff.md`.

## The appends

RECORD7 and DEC6 each begin with an empty line, and both targets end in a newline at `8b07c95b`:
an append is the file's bytes followed by the slice's bytes, and nothing else.

## THE TABLES

Each carrier holds one JSON array per line. Their sha256 digests, to verify before copying:
`f261-r7-words-1.jsonl` `0e2d9ebf700c8d7417c0fb3b0c334ef71e1d0a8cf26ce6d3f3dca1ae0b43cde3`,
`f261-r7-words-2.jsonl` `3f424e7dd4ed86bf29b4badb9a7e3df5078171b818f47aaebf8885fcbf7af6e6`,
`f261-r7-words-3.jsonl` `7f5278cbd603fe074c0bbfefba3eb3dd46a68c233ad53c1ad8d53eff795a8ea5`,
`f261-r7-guard.jsonl` `06ac0b87c1ee1e8075c0ff2df271a00468ba78e29e57f072e34acc56cc7224a2`.
Apply the rows strictly
in file order, each against the tree as the previous rows left it, from the repository root:
`["edit", path, old, new, count]` opens the path with `encoding="utf-8", newline=""`, requires
the number of occurrences of `old` to equal `count` exactly, and replaces every occurrence with
`new`; `["delete", path]` removes the file; `["move", src, dst]` renames the file, whose target
must not exist; `["create", path, content]` writes `content` to a path that must not exist, with
the same encoding and newline setting. A count that differs or a target that exists is a STOP:
touch nothing further, commit nothing of that table, and hand back with the row and the reading.
Stage each commit with `git add -A` after its table and its carrier. The tables are the
reviewer's measured dry run of DECISION F261 D6, one table per CHOSEN paragraph and a last one
for its guards: words-1 the status values and reason codes, words-2 the job apply record's
key, directory, prefix and names, words-3 the text and the `--skip-blocked` help, guard the tests.

## SPEC S — the suite, once, after G5 and before C6

From the primary checkout's root, serially:
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, with `PYTHONPATH`,
`REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`, output under
`.remedy-wt/f261r7w/`. Report pytest's return code, the run's last output line, and every
distinct bad node, the text after a line-initial `FAILED ` or `ERROR ` up to the first ` - `.
Re-run each bad node alone, once, the same way, and report that return code beside it.

## Constraints

1. NO SLICE AND NO TABLE IS EDITED. Extract each slice as the bytes strictly between its
   `BEGIN <NAME>` and `END <NAME>` lines and verify its sha256 before use.
2. READ `.agent/STOP` before C0a, before C2 and before C6, with real exit codes. If it exists:
   finish a half-written commit, write the handoff, push, stop.
3. A red gate is a STOP: commit what is honestly finished, hand back with the raw output.
4. Scratch, runner scripts and your worktree live under `.remedy-wt/f261r7w/`, uncommitted; no
   `.py` file under `.agent/`. Under `.remedy-wt/` open only `.remedy-wt/f261-block/` and your
   own directory. `git worktree list` reads one row now; leave it so. Create no symlink.
5. Every commit stays under 500 insertions, read as the first column of `git show --numstat
   --format= <commit>` with git's default rename detection.
6. NEVER merge, open a pull request, force-push, rewrite history or delete a branch. No `remedy`.
   Write no `Done:` paragraph.
7. THE BLOCK'S OWN SIZE, measured on its final bytes: 237 lines TOTAL and 186 lines of PROSE,
   against the caps of 490 and 400.
8. GATE ORDER. G1 and G2 after C1; G3 after C4; G4 and G5 after C5; then SPEC S, whose result is
   G6; G7 after C6 and the push, reported in the completion message only.
9. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and
   no subject carries a leading-slash token or an absolute path.

## Done when — every gate run for real, its exit code recorded

G1 TRANSPORT. The sha256 of `.agent/authored/f261-r7.md` at C0a equals the digest the delegating
message gives, and `.agent/last_block.md` at C0b is byte-identical to it; the slices FOUND, each
matching its BEGIN-marker sha256; each committed carrier's sha256 equals its digest above.

G2 THE RECORD, at C1. `.agent/plan.md` is byte-identical to PLAN7, at most 50 lines, with
`^## Goal$` once and `^## Next Steps$` once. `.agent/live_review.md` equals its `8b07c95b` blob
followed by RECORD7, and `.agent/decisions.md` its `8b07c95b` blob followed by DEC6. Over
`.agent/live_review.md`: `^Gate: F\d+ R\d+ — ` reads 115 at `8b07c95b` and 116 at C1, with
`Gate: F261 R6 — ` once at C1; distinct `^- R-\d+ — ` ids 100 and 100; distinct
`^Done: R-\d+ — ` ids 4 and 4; the open set by distinct id 96 and 96, equal as sets.

G3 THE WORDS, at C2, C3 and C4. Let J be `packages/orchestration/job_apply.py`,
`tests/orchestration/test_job_apply.py`, `tests/orchestration/test_job_apply_consistency.py`,
`tests/orchestration/test_job_worktree_handoff.py` and
`tests/orchestration/test_job_worktree_integrity.py`. `git diff --no-renames --name-only` from
each commit's parent prints exactly that commit's carrier and J at C2 and at C3, and its carrier,
J and `apps/cli/command_catalog.py` at C4. `git rev-parse <commit>:<dir>` equals the dry run:
C2 `apps` `712eeb42e83fb80f3135dc818661dd9d551255c0`, `packages` `4cbcd9905fdecc5c55c7b4baea53d2c3a24ee70a`, `tests`
`a940c877ae81ae6dc299e9112d91b42c14a36d7b`; C3 `apps` the same as C2, `packages`
`fd54296c79da659c0db38cab9b93e1fabfb7cecc`, `tests` `7d62b6115d1ff77e7ab7a0173472adf0a11cfef9`; C4 `apps`
`5366495d1c37d66bf02d972926f12b32ce160a8a`, `packages` `c9e5203590e1501c9cc8be7b6ede8f0d158888b0`, `tests`
`93007477fb72c8eb8613c8881bf96978f488f11f`. At each of those commits, `scripts`, `docs` and `README.md` equal
their objects at `8b07c95b`. Report each commit's insertions per constraint 5.

G4 THE GUARDS, at C5. `git diff --no-renames --name-only <C4> <C5>` prints exactly
`.agent/authored/f261-r7-guard.jsonl` and `tests/orchestration/test_job_apply.py`; `git rev-parse`
gives `tests` `4fc4dc808311601a0bd720297cc365029c9da7ea` and `apps` and `packages` equal to C4. Report C5's
insertions. Then three greps, each with its exit code and raw output: GA `git grep -n -I -w -e
promotion_id -e job_promotions -e remedy-promo -e promoted_test_failed -e
promoted_record_update_failed -e promoted_cleanup_failed -e no_promotable_files -e
promotion_record_update_failed -e promotion_worktree_failed -e promotion_materialization_error -e
temporary_promotion_cleanup_failed -e promotion_source_inspect_failed -e promotion_coverage_failed
-e promotion_record_not_writable -e _apply_records_dir -e fake_apply_records_dir <C5> -- apps
packages scripts tests docs ':!docs/roadmap'` exits 1 and prints nothing; GB `git grep -n -I -i
-e promot <C5> --` followed by the paths of J prints exactly one line, the guard's own
`assert "promot" not in help_text.lower()` in `tests/orchestration/test_job_apply.py`; GC
`git grep -n -I -w -e TestApplyRecord -e TestApplyRecordPersistence -e
test_unwritable_apply_record_dir_blocks_approved <C5> -- tests/orchestration` exits 1 and prints
nothing. `python3 -m ruff check` over `apps/cli/command_catalog.py` and the paths of J exits 0.

G5 THE RED-PROOF, in `git worktree add --detach .remedy-wt/f261r7w/wt <C5's sha>`, each run
through the runner over the four test files of J with `-rf --tb=no`, each mutation replacing
bytes whose count in the named file must read 1, and each restored afterwards with
`git -C .remedy-wt/f261r7w/wt checkout -- <that file>`. (a) CONTROL: must exit 0.
(b) `packages/orchestration/job_apply.py`: `result.status = "applied"` becomes
`result.status = "promoted"`: must exit 1 with `TestApproveApplies::test_approve_applies_safe_files`
among the failed nodes. (c) The same file: `"job_apply_records"` becomes `"job_promotions"`, and
(d) `"job_apply_id"` becomes `"promotion_id"`: each must exit 1 with
`TestJobApplyRecord::test_the_record_is_stored_under_job_apply_records_by_its_job_apply_id`
among the failed nodes. (e) The same file: `Job apply record: ` with its trailing space becomes
`Promotion: `: must exit 1 with `TestJobApplyRecord::test_the_summary_names_the_job_apply_record`
among the failed nodes. (f) `apps/cli/command_catalog.py`: the help text
`"Apply the non-blocked files and deliberately leave the protected ones not applied (they are named, never written)"` becomes
`"Promote the non-blocked files and deliberately leave the protected ones unpromoted (they are named, never written)"`: must exit 1 with
`TestCLICommandShape::test_the_skip_blocked_help_speaks_of_applying` among the failed nodes.
Report each exit code, summary line and number of failed nodes; then
`git worktree remove --force .remedy-wt/f261r7w/wt`.

G6 THE SUITE, SPEC S at C5: must exit 0 with no bad node; report the last output line.

G7 THE TREE, after C6 and the push. `git status --porcelain` prints `''`; C0a to C6 are
single-parent commits in that order on `8b07c95b`; `git rev-parse HEAD` equals
`git rev-parse origin/feature/f261-cli-vocabulary-v2`; `git worktree list` prints one row.

## The handback, C6

`.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 2 of feature F261 · round 7 · rounds so far 7`, with one sentence of context
self-assessment. `## Commits` lists C0a to C5, each row's `+/-` cell equal to constraint 5's
reading of that commit and its deletions column; C6's own numbers appear nowhere, per item 31 of
§3. `## Verification` gives G1 to G6 with real exit codes. It states the open findings at 96 by
distinct id, with the High ids R-0803, R-0804, R-0806 and R-0807, and
`Operator questions open: 0`. Its `## Next` names, in order: Phase 1 rule 1; the reviewer's
verdict on round 7; `job show --full`.

── SLICE PLAN7 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN7 sha256=e266f146efd7532878f8fddf3b9288d88a90732d150f63eb8f413d5c03970d2b
# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 7 continues T002. It books round 6's PASS and records DECISION F261 D6, then renames the
output-visible words of `job apply` in three commits, its status values and reason codes, the
job apply record's key, directory and temporary prefix, and its printed text, prose and
`--skip-blocked` help, and adds guards for the record and that help in a fourth commit; each
applies a table the round saves under `.agent/authored/`.

## Next Steps

1. `job show --full` composing the read commands as sections, with the blocked-task findings
   R-0806 asks for and the fix R-0896 needs.
2. One commit per folded read command and `do job-report`, each adding its id to the guard.
3. The run-level promote words DECISION F261 D6 leaves, ruled by sense, with the kept-by-sense
   list DECISION amend0905-vocab D5 names written into the record and a test for the
   Acceptance grep of the retired word.
4. T003, the prune to D4, and T004.

## Risks

- 96 findings are open by distinct id before and after this round's record; four are High,
  R-0803, R-0804, R-0806 and R-0807.
- `job show` prints JSON that the canary, `tests/cli/test_plan_approval.py` and
  `scripts/remedy_smoke.sh` parse, so its `--full` form only adds keys to that JSON.
- Job apply records written before this round stay under `job_promotions/`, and nothing reads
  them after it.
END PLAN7

── SLICE RECORD7 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD7 sha256=fb75a6487109d811fe8f9d1855d47d7fb63c59f81a947496fd37ecb33ae6596f

Gate: F261 R6 — the F261 round 6 entry. VERDICT PASS. Written by the planner and reviewer of session 37 after reading the committed range `a1c42d72`..`1495255f` and re-deriving the readings below; the worker's report was evidence for none of them. It is booked here by the first commit of round 7 that writes the record, per operator amendment amend0827-process-diet rule 1. THE TRANSPORT: `.agent/authored/f261-r6.md` at `2e6cc882` and `.agent/last_block.md` at `c3c39002` are byte-identical to the reviewer's scratch original, sha256 `58db64d509ba6eac939675876843a0160c59b651eee94d70399317b4d68e8461`, and `.agent/authored/f261-r6-rename-1.jsonl` at `dd3e1f3e` and `.agent/authored/f261-r6-rename-2.jsonl` at `fa5a9990` are byte-identical to the reviewer's tables. THE STATE: at `7f94f581` and again at `1495255f`, `.agent/plan.md` equals PLAN6 and `.agent/live_review.md` and `.agent/decisions.md` equal their `a1c42d72` blobs followed by RECORD6 and DEC5. THE RENAMES: at `dd3e1f3e` and at `fa5a9990` the `apps`, `packages` and `tests` objects equal the reviewer's dry runs of table 1 and of tables 1 and 2, which had reproduced the research helper's trees exactly, and `scripts`, `docs` and `README.md` equal their objects at `a1c42d72`; each commit's `--no-renames` path set is the dry run's plus its own carrier, and `git show --numstat` reads 153 and 422 insertions. As line multisets, the lines table 1 changes differ from the lines they replace only by the module path and its test aliases, and the lines table 2 changes only by that table's name map. At `fa5a9990` the absence greps of the old identifiers and of `job_promote` exit 1 with no output, and ruff over the touched files that survive exits 0. In the reviewer's dry run a full suite under `-n auto` read 10 failed and 18157 passed, every failure in `tests/ui_server` or `test_vitest_passes`, classes the helper's base control also failed; reverting the CLI's import to `job_promote` failed 14 tests of `tests/orchestration/test_job_apply.py`, and reverting `def apply_job(` failed 74. THE REVIEWER'S RUN in the primary checkout at `1495255f` of `tests/orchestration/test_job_apply.py`, `tests/orchestration/test_job_apply_consistency.py`, `tests/orchestration/test_job_worktree_handoff.py`, `tests/orchestration/test_job_worktree_integrity.py`, `tests/orchestration/test_import_reachability.py`, `tests/orchestration/test_self_use_runner.py`, `tests/test_command_catalog.py`, `tests/cli/test_advertised_commands.py`, `tests/docs/`, `tests/ui_server/test_dashboard_contract.py` and `tests/cli/test_golden_path.py` read 640 passed. The open set reads 96 by distinct id at `1495255f`. Between this verdict and its booking the operator committed `8b07c95b`, DECISION amend0915-q2-close D1, which answered operator question Q2 and left `.agent/operator_questions.md` empty.
END RECORD7

── SLICE DEC6 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC6 sha256=d3aa5c753fd4778c31b350080c73e0d436f8117b236586ff10e6a79f0cb66c4d

## DECISION F261 D6 (2026-09-15, F261 round 7) — the output-visible words of `job apply`, and the job apply record's own spelling

CONTEXT. DECISION F261 D5 left the string values, the JSON key and the names on disk of `packages/orchestration/job_apply.py` to a words round. This section is that round's ruling. Measured by the reviewer's research helper at `1495255f`, whose `apps`, `packages` and `tests` objects equal those at `8b07c95b`, and re-read by the reviewer on the dry-run trees: every reader of a job apply status value, and every occurrence of the reason codes, `promotion_id`, `job_promotions` and `remedy-promo-` renamed below, sits in `job_apply.py` or in `tests/orchestration/test_job_apply.py`, `test_job_apply_consistency.py`, `test_job_worktree_handoff.py` and `test_job_worktree_integrity.py`; no script, UI source or `docs/` page reads one; and no reader compares a job apply status with a task or manifest status in the same variable.

CHOSEN, FIRST: THE STATUS VALUES AND REASON CODES. `promoted`, `promoted_test_failed`, `promoted_record_update_failed` and `promoted_cleanup_failed` become `applied`, `applied_test_failed`, `applied_record_update_failed` and `applied_cleanup_failed`. The task and manifest status `applied` is a field of a different record, and where a summary prints both, on separate lines, both are true. `no_promotable_files` becomes `no_files_to_apply`; `promotion_worktree_failed`, `promotion_materialization_error`, `promotion_source_inspect_failed`, `promotion_coverage_failed` and `temporary_promotion_cleanup_failed` become `apply_worktree_failed`, `apply_materialization_error`, `apply_source_inspect_failed`, `apply_coverage_failed` and `temporary_apply_cleanup_failed`; `promotion_record_update_failed` and `promotion_record_not_writable` become `job_apply_record_update_failed` and `job_apply_record_not_writable`.

CHOSEN, SECOND: THE JOB APPLY RECORD IS SPELLED WITH `job_apply`. At `8b07c95b` the words `apply_id` and "apply record" already name the patch apply record, `DurableApplyRecord` in `packages/orchestration/repository_snapshot.py`, stored under a job workspace's `apply_records/` and named by the `--apply-id` option. One spelling per concept, per the discoverability conventions of AGENTS.md, gives the job-level record its own: `promotion_id` becomes `job_apply_id` as the result field, the JSON key and the stored file's name; the data directory `job_promotions` becomes `job_apply_records`; the printed `Promotion: <id>` becomes `Job apply record: <id>`; the temporary prefix `remedy-promo-` becomes `remedy-job-apply-`; and round 6's names `_apply_records_dir`, `fake_apply_records_dir`, `TestApplyRecord`, `TestApplyRecordPersistence` and `test_unwritable_apply_record_dir_blocks_approved` take the same prefix. The `TestApplyRecord` of `tests/test_patch_apply.py` is the patch record's and stays.

CHOSEN, THIRD: THE TEXT AND ITS GUARDS. The printed lines, docstrings and comments of `job_apply.py` and of the four test files that use the job-result sense take apply words, and so does the `--skip-blocked` help of `job apply` in `apps/cli/command_catalog.py`, where "unpromoted" becomes "not applied". Before this round no test pinned the record's directory, its key, the summary's record line or that help, so the round adds tests that read a stored record back from `job_apply_records/<job>/<job_apply_id>.json` by its `job_apply_id` key, find `Job apply record: <id>` in the summary, and find no promote word in the help.

CONSEQUENCE. `job apply --json` prints `job_apply_id` where it printed `promotion_id`, and its statuses and reason codes read as above. Records written before this round stay under `job_promotions/` and nothing reads them, as DECISION D-A of `docs/roadmap/features/T2_F261.md` allows. The promote words outside `job_apply.py`, among them the `do` group's description, `promotion_readiness` in `do report`, the job state `promoted` in `packages/orchestration/pingpong_job.py` and the staging pipeline of `job_fulfillment.py` and `staging_workspace.py`, wait for T002's run-level step, which rules them by sense. HOW TO REVERSE: revert the round's four table commits and delete this section.
END DEC6

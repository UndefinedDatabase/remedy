── STEP T003 — F275 — ROUND 103 ──
Goal: The second BRIDGE round. Book round 102's verdict and register `R-0885` and `R-0886`;
repair in production where the flip broke a contract, per SPEC P; apply the committed test
carrier; red-prove every production change; run the full suite once and show the bad-node set
strictly shrinking with no node newly bad.

Base commit: `0fac911d`. Round type: SPLIT. Operator amendment amend0914-f275-sprint in
`docs/agents/self_drive_protocol.md` governs this round; read that paragraph first.

THE FRAME RULE, per item 37 of §3, stated as the property MEASURED over the final bytes: NO LINE
of this block is a run of a single repeated character, and every box-drawing rule inside the
STEP and SLICE header lines is exactly two characters long.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f275-r103.md`, the block as received
C0b `.agent/last_block.md`, the block as received
C0c `.agent/authored/f275-r103-tests.md`, the test carrier as received
C1 THE BOOKKEEPING COMMIT: `.agent/plan.md` gets slice PLAN103 as a full replacement;
   `.agent/live_review.md` gets slice RECORD103 appended; `.agent/prose_slips.md` gets slice
   SLIP103 appended; `.agent/decisions.md` gets slice DEC103 appended
C2 SPEC P1 to P4, the repairs of `R-0885` and `R-0886`
C3 SPEC P5 to P9, the other production repairs
C4 the test carrier's fence applied, per SPEC T
C5 `.agent/authored/f275-r103-suite.txt`, per SPEC S
C6 `.agent/handoff.md`, the handback

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. No `Landed:` or `Done:` line is
written: the handback names the commits that repair `R-0885` and `R-0886`.

## Change — exactly these paths and no others

The Bundle's `.agent/` paths; at C2 and C3 the files SPEC P names; at C4 the paths the
carrier's diff names.

## SPEC P — the production repairs, written by the worker

P1 `packages/orchestration/pingpong_job.py`, `_persist_job`: write the exported JSON, unchanged
in bytes, to a temporary file created in the record's own directory; flush it and `os.fsync`
it; then `os.replace` it over the record path. On any exception the temporary file is removed
and the exception re-raised. The function still returns the record path. One WHY comment: a
save interrupted part-way leaves the previous record or the new one, never a torn file.
P2 `apps/cli/commands/job.py`, `_scope_label`: a job whose `project_id` is empty or absent is
unscoped; the test is the value's truthiness, never `is None`.
P3 `apps/cli/commands/project.py`, `_cmd_project_adopt`: a job already belongs to a project
only when its `project_id` is non-empty.
P4 `packages/orchestration/project_scope.py`, `job_in_scope`: the legacy branch takes a job
whose `project_id` is empty or absent, and the docstring's legacy rule says "no project_id"
where it says "project_id=None".
P5 `apps/cli/commands/do_cmd.py`, `_cmd_do_mission`: the value handed to `JobPlan(budgets=...)`
is the validated `JobBudgets` model's `model_dump(mode="json")`, the dict the record declares.
P6 `apps/cli/commands/job_context_cmd.py`, `_task_files_hint`: the flight block's `files_hint`,
`inputs["flight"]["files_hint"]`, wins when it is a list; otherwise the task's own
`files_hint`; neither a list gives an empty scope. The comment above it and the module
docstring's sentence about the two sources state that order and why:
`map_flight_plan_to_tasks` writes the scope into the flight block, and `_task_planned_id` reads
the flight block first too.
P7 `packages/orchestration/job_fulfillment.py`, `run_job_fulfill`: the entry load of the job
calls `require_job_plan`, the raising loader, with the same arguments. Nothing else changes.
P8 `packages/orchestration/test_execution_service.py`: the job loads in `_persist_test_record`,
`_create_failure_artifact` and `finalize_test_outcome` call `require_job_plan`; the import of
`load_job_plan` goes once nothing uses it.
P9 `scripts/remedy_runtime_cli_smoke.py`: `create_env` mints the id as sixteen lowercase hex
characters and writes the record to `jobs/<id>/job.json` with the keys `job_id`, `job_title`,
`created_at`, `tasks`, `status`, `artifacts`, `budget` and `metadata`, still importing nothing
from `packages/`; `smoke_propose` and `smoke_worker` read the record from that path.

## SPEC T — the test carrier, at C4

Extract the one fence of `.agent/authored/f275-r103-tests.md` as COMMITTED at C0c into scratch;
from the repository root run `git apply --check` on it and then `git apply`. No other edit.

## SPEC S — the suite, once, after the red-proofs and before C5

The round's FIRST AND ONLY full-suite run, from the primary checkout's root, serially:
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, with
`PYTHONPATH`, `REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`,
stdout and stderr saved under `.remedy-wt/r103w/`. A bad node is the text after a line-initial
`FAILED ` or `ERROR ` up to the first ` - ` or the line's end. The transcript file holds: line 1
`EXIT=<pytest's return code>`; line 2 the run's last output line with its leading and trailing
`=` and spaces stripped; then every distinct bad node, sorted, one per line; nothing after the
last line's newline. With no bad node, the file is those two lines.

## Constraints

1. NO SLICE IS EDITED. PLAN103, RECORD103, SLIP103 and DEC103 land byte for byte, and the
   carrier's fence is applied unaltered; a discrepancy is DECLARED, never repaired.
2. READ `.agent/STOP` before C0a, before C2 and before C6, with real exit codes. If it appears,
   finish the commit in hand, write the handback and end.
3. No `.py` file under `.agent/`; scratch under `.remedy-wt/r103w/`, uncommitted, every scratch
   output path absolute. The reviewer's `.remedy-wt/r101/` is not opened.
4. The appends at C1 have a ZERO deletion column. Every commit stays under 500 insertions,
   counted per commit before it is made.
5. No `gh`, no `remedy`, no pull request, no branch created or deleted, no merge, NEVER a
   force-push, no history rewrite. Push after C1, C4, C5 and C6.
6. THE ONE WORKTREE is G3's, `git worktree add --detach` at C4 under `.remedy-wt/r103w/`,
   removed without `--force` and pruned before the suite runs.
7. THE BLOCK'S OWN SIZE, measured on its final bytes: 278 lines TOTAL and 200 lines of
   PROSE, against the caps of 490 and 400.
8. GATE ORDER. G1 runs at C1. G2 runs after C4. G3 and then G4 run after G2 and before the
   suite. G5 runs after the suite, with its committed-transcript reading at C5. G6 runs after C5
   and before C6. No gate runs after C6; C6's own numbers are the reviewer's.
9. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and
   no subject carries a leading-slash token or an absolute path.

## Done when — the gates, each run for real and its exit code recorded

G1 TRANSPORT AND BOOKKEEPING, at C1. The sha256 of `.agent/authored/f275-r103.md` at C0a equals
the block digest received, `.agent/last_block.md` at C0b is byte-identical to it, and the
sha256 of `.agent/authored/f275-r103-tests.md` at C0c equals the carrier digest received.
Extract the slices by their markers, report how many were FOUND, and check each against its
BEGIN-marker sha256. `.agent/plan.md` at C1 is byte-identical to PLAN103, with at most 50 lines,
one `## Goal` and one `## Next Steps`. For each append, the blob `git show 0fac911d:<path>`
followed by the slice equals the file at C1: 1171965 bytes for `.agent/live_review.md`, 305816
for `.agent/prose_slips.md` and 1321901 for `.agent/decisions.md`. Lines matching
`^Gate: F\d+ R\d+ — ` read 124 at `0fac911d` and 125 at C1, with `Gate: F275 R102 — ` once. The
open set BY DISTINCT ID, the ids of `^- R-\d{4} — ` paragraphs minus the ids of `^Done: R-\d{4}`
lines, reads 89 at `0fac911d` and 91 at C1, the ids added `R-0885` and `R-0886`.

G2 THE CODE, after C4. `git show --name-only` of C2 lists exactly P1 to P4's files, and of C3
exactly P5 to P9's. At C4, `git apply --check` and `git apply` exit 0, and `git rev-parse
C4:tests` reads the reviewer's dry-run tree 52cc576ae9c7ae9777c68f41ab32230551bfe100.
`ruff check --output-format concise` over every file C2, C3 and C4 change: exit 0.
`ruff check . --output-format concise` rows as a MULTISET with line and column dropped, at
`0fac911d` from a `git archive` tree under `.remedy-wt/r103w/` and at C4 in the primary
checkout: no row at C4 absent at `0fac911d`; the reviewer read 11 at both.

G3 THE RED-PROOFS, in G3's worktree at C4, one production file at a time: write that file's
blob at C1 over it, run the named test file from inside the worktree with SPEC S's environment
and `python3 -B -m pytest -q -p no:randomly -p no:cacheprovider`, report the bad node ids, then
restore the file and show it byte-identical to C4's. Each named node MUST be among the bad
nodes; a named node that stays green is DECLARED with its tally, never papered over. The
reviewer's dry run, file by file:
P1 over `tests/orchestration/test_unified_store_parity.py`:
`TestTheWriteReplacesTheRecordWhole::test_a_failure_before_the_rename_leaves_the_previous_record_intact`.
P2 over `tests/cli/test_scoped_listings.py`: `TestScopedListingsCLI::test_legacy_job_hidden_and_unscoped_label`.
P3 over the same file: `TestScopedListingsCLI::test_adopt_persists` and
`TestScopedListingsCLI::test_adopting_a_pingpong_job_id_exits_cleanly_instead_of_crashing`.
P4 over the same file: `TestTwoProjectIsolation::test_a_record_with_no_project_is_legacy`.
P5 over `tests/cli/test_plan_approval.py`: `TestConfigBudgetPrecedence::test_config_budget_survives_plan_suggestion`
and `TestConfigBudgetPrecedence::test_plan_fills_unset_config_field`.
P6 over `tests/cli/test_job_context_cmd.py`: `test_direct_import_neighbor_appears_at_tier_two`,
`test_fenced_file_is_tier_one_and_rendered_full` and `test_unrelated_module_is_omitted_for_distance`.
P7 over `tests/orchestration/test_job_fulfillment.py`:
`TestJobFulfillFixturePass::test_a_pingpong_job_id_reaches_the_store_instead_of_a_uuid_parse`.
P8 over `tests/orchestration/test_test_execution_service.py`:
`TestUsageAccounting::test_usage_incremented_on_process_start`.
P9 over `tests/cli/test_propose_cli_runtime.py` and `tests/cli/test_worker_cli_runtime.py`:
`TestProposeRuntimeSmoke::test_propose_flow` and `TestWorkerRuntimeSmoke::test_worker_flow`.
Then remove and prune the worktree, per constraint 6.

G4 THE TARGETED FILES, in the primary checkout, with SPEC S's environment:
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider` over the nine test files the
carrier changes and `tests/cli/test_job_context_cmd.py`, `tests/cli/test_propose_cli_runtime.py`,
`tests/cli/test_worker_cli_runtime.py`, `tests/orchestration/test_job_fulfillment.py`,
`tests/orchestration/test_test_execution_service.py`, `tests/test_data_paths.py`,
`tests/orchestration/test_project_scope.py`, `tests/orchestration/test_checkpoints.py`,
`tests/orchestration/test_job_budgets.py`, `tests/cli/test_mission_cmd.py`,
`tests/storage/test_persistence.py` and `tests/orchestration/test_job_plan_state_reads.py`:
exit 0; the reviewer's worktree read 863 passed.

G5 THE BRIDGE, per SPEC S. BASE is the set of bad nodes in `.agent/authored/f275-r102-suite.txt`
at `0fac911d`. Report pytest's real exit code, the summary line, the count of distinct bad
nodes, FIXED (in BASE and not bad now) and NEWLY BAD (bad now and not in BASE), each by node
id, and every BASE node still bad with its last `E   ` line. Each NEWLY BAD node is re-run by
its node id ALONE three times with SPEC S's environment and reported FLAKY with the three
tallies only if all three pass. NEWLY BAD less FLAKY: MUST be empty; FIXED: MUST be non-empty.
At C5 the committed transcript equals the file rebuilt from the saved stdout, and before C5
`git status --porcelain` listed only that file.

G6 TREE, CANARY, PATH SET, OPEN SET, CAP, after C5. `git status --porcelain` prints `''` and
`git worktree list` one row. The canary `python3 -B -m pytest tests/cli/test_golden_path.py -q`:
exit code and tally REPORTED. The changed-path set of `0fac911d`..C5 against the union of the
Bundle's `.agent/` paths other than `.agent/handoff.md` and the paths of C2, C3 and C4: MISSING
and EXTRA by name. The open set at C5 equals C1's. One row per commit of `0fac911d`..C5 with
insertions, deletions and staged path count, and the commits reaching 500 insertions, named.

Handback: `.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 35 of feature F275 · round 103 · rounds so far 103`; the Commits table read from
`git show --numstat` and compared cell by cell against G6, C6's row carrying no numbers and
saying why; one Verification line per gate with its REAL exit code; External actions;
Authored-text proofs; Item-status; Deviations; one sentence of context self-assessment;
`## Next` stating `Operator questions open: 1`. NO SCOPE REPORT AND NO SESSION-LIMIT BANNER,
by amendment amend0911-f275-to-scope.

── SLICE PLAN103 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN103 sha256=a31103e51f4fb81fe60beea4e3f8b94dbcd9c65cefb22ead46810cc3f2e4ead5
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001 and T002 are DONE, the classic runner's whole
command surface is gone as of round 34, and the record flip landed in round 101.

## Current Step

ROUND 103 IS THE SECOND BRIDGE ROUND, per operator amendment amend0914-f275-sprint rule 3, and
it aims at every bad node round 102's transcript lists. It registers and repairs `R-0885`, the
job save the flip left non-atomic, and `R-0886`, the three readers that treat only `None` as
no project. It repairs the rest in production where the flip broke a contract — the budgets a
mission hands its record, the flight plan's file scope in the job context command, the entry
load of job fulfilment and the three job loads of the test execution service — and in the
runtime smoke harness and the tests where they still seed a classic record. The full suite
runs once; its bad-node set must be a strict subset of round 102's.

## Next Steps

1. MORE BRIDGE ROUNDS only if round 103's transcript does not read exit 0, each strictly
   shrinking the committed bad-node set with no node newly bad.
2. THE CLASSIC STORE: the classic `Job` and `Task` models and `packages/orchestration/storage.py`
   with their remaining readers, the which-store branches of the cockpit and its unreachable
   `_JobPlanAdapter`, the classic-store search inside `resolve_job_id`, and the guard tests
   that still pin the classic models.
3. THE CLOSURE SEQUENCE, with the integration gate's full-suite runs.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20
  sessions and 60 rounds without a replacement, so this feature closes only at full scope.
- THE BRANCH IS RED until a bridge round's transcript reads exit 0, and hosted CI on the branch
  is expected to be red in that span, per amend0914 rule 3.
- THE BRIDGE IS BOUNDED at eight rounds after the flip commit: a ninth writes an operator
  question and stops, and a round that adds a bad node is FAIL.
- A SERVER-START RACE: a command-channel test read its server's info file before the server
  wrote it once in the reviewer's full run after the flip and passed ten times alone.
- ONE ROUTED LOAD IS REACHED BY NO TEST until `R-0883` is repaired.
- The open set is 89 by distinct id at this round's base and 91 once `R-0885` and `R-0886` are
  registered, with `R-0809`, `R-0880`, `R-0883` and `R-0884` open. Four are High — R-0803,
  R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END PLAN103

── SLICE RECORD103 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD103 sha256=5d90ab5234b6f06f8f6753b1c10f3706a8d9d0235345ed46dc07aeeff8d62ed2

Gate: F275 R102 — the F275 round 102 entry. VERDICT PASS. Written by the planner and reviewer of session 35 after reading the committed range `7f2991c9`..`0fac911d` and re-deriving every reading that bears on a product path; the worker's report and its transcripts were evidence for no line below. It is booked here by the first commit of round 103 that writes the record, per operator amendment amend0827-process-diet rule 1. The round is the first bridge round of operator amendment amend0914-f275-sprint rule 3.

WHAT THE TRANSPORT PROOF COVERS, per item 37 of §3. The committed `.agent/authored/f275-r102.md` and `.agent/last_block.md` equal the reviewer's original at 24741 bytes at `0fac911d`; `.agent/plan.md` equals PLAN102 from `2d907c03` through `0fac911d`; the three appends at `2d907c03` are exact, 1168612 bytes followed by RECORD102 in the review record, 305304 followed by SLIP102 in the prose slips and 1318510 followed by DEC102 in the decisions. The ledger's `Gate: F<n> R<n> — ` heads read 124 at `0fac911d` with `Gate: F275 R101 — ` once, and the open set stayed 89 with identical membership.

THE CODE IS THE TREE THE REVIEWER BUILT. `2b118122` changes 184 paths, every one a path the flip commit `ebc0182c` changed, and its changed lines are import statements. The `packages`, `apps` and `tests` trees at `0fac911d` are identical to the reviewer's own dry run at `7f2991c9` of `ruff`'s fixer followed by the eleven replacements of EDITS102, `d3a40d00`, `625e9faa` and `50b10765`; `docs` and `scripts` do not change in the range. No commit of the range reaches 500 insertions.

THE BRIDGE SHRANK. The committed transcript `.agent/authored/f275-r102-suite.txt` reads exit 1 with 22 failed, 18419 passed, 23 skipped and 7 errors, 29 distinct bad nodes, sorted; against the 40 of `.agent/authored/f275-r101-suite.txt` it has no node newly bad and the eleven ordered nodes fixed, which the reviewer re-derived from the two committed transcripts. The reviewer's own re-run in the primary checkout at `0fac911d` read the five edited test files with `tests/orchestration/test_ci_budgets.py` at 250 passed, `tests/docs/` at 306 passed, the canary at 2 failed and 40 passed with both failures in the transcript, and `ruff check .` at 11 rows, `I001` 9, `UP035` 1 and `F821` 1, each also present at `5ce0c5a2`.

ONE DEFECT OF THE BLOCK, declared by the worker. The Bundle ordered the block and its mirror as one commit while constraint 4 ordered every commit under 500 insertions, and the two files together are 504; the worker committed them as `0c449dd1` and `6489feca` and declared it. It is booked as one line in `.agent/prose_slips.md` by the commit that books this entry.

- R-0885 — Medium, THE RECORD FLIP MOVED EVERY JOB SAVE FROM AN ATOMIC REPLACE TO A PLAIN OVERWRITE OF THE RECORD, SO A SAVE INTERRUPTED PART-WAY CAN LEAVE A TORN `job.json`. Raised by the planner and reviewer of session 35 of F275 while preparing round 103. THE DEFECT: at `0fac911d` the classic writer `_atomic_write_job` in `packages/orchestration/storage.py` writes a temporary file in the record's directory, calls `os.fsync` on it and `os.replace`s it over the record, while the unified writer `_persist_job` in `packages/orchestration/pingpong_job.py`, which `save_job_plan` calls and which every job save has reached since the flip commit `ebc0182c`, calls `write_text` on the record path itself. The docstring of `TestTornCheckpoint` in `tests/orchestration/test_resume_kill.py` still names `storage._atomic_write_job` as the reason a torn record cannot be produced on demand. MEASURED by the reviewer in a worktree at `0fac911d` carrying round 103's tests: `test_a_failure_before_the_rename_leaves_the_previous_record_intact` of `tests/orchestration/test_unified_store_parity.py`, which makes `os.fsync` raise during a save of a changed record, fails with `_persist_job` in its `0fac911d` form, because that form never calls `os.fsync` and the save does not raise. WHY MEDIUM: a process killed, or a disk that fills, while a record is being written leaves bytes no loader can read, so that job can no longer be shown or resumed; nothing goes wrong while no write is interrupted. WHY F275's: its own flip commit moved every job save onto this writer. FIX: `_persist_job` writes the record to a temporary file in the same directory, fsyncs it and replaces the record with it, removing the temporary file on failure, and the test above pins that a failure before the rename leaves the previous record byte-identical.

- R-0886 — Medium, THE UNIFIED RECORD SPELLS AN ABSENT PROJECT AS `""` WHILE THREE READERS STILL TREAT ONLY `None` AS NO PROJECT, SO AN UNSCOPED JOB IS LABELLED ORPHANED, IS REFUSED BY `project adopt`, AND IS HIDDEN FROM A ONE-PROJECT LISTING. Raised by the planner and reviewer of session 35 of F275 while preparing round 103. THE DEFECT: at `0fac911d` `JobPlan.project_id` in `packages/orchestration/pingpong_job.py` defaults to `""`, the classic `Job` spelled it `None`, and `_scope_label` in `apps/cli/commands/job.py`, `_cmd_project_adopt` in `apps/cli/commands/project.py` and `job_in_scope` in `packages/orchestration/project_scope.py` each test `project_id is None` or `is not None`. MEASURED by the reviewer in a worktree at `0fac911d` carrying round 103's tests, restoring one reader at a time to its `0fac911d` form: `_scope_label` makes `test_legacy_job_hidden_and_unscoped_label` of `tests/cli/test_scoped_listings.py` fail; `_cmd_project_adopt` makes `test_adopt_persists` and `test_adopting_a_pingpong_job_id_exits_cleanly_instead_of_crashing` fail; and `job_in_scope` makes `test_a_record_with_no_project_is_legacy` fail, a test no file held at `0fac911d`, which is why the suite never saw that third reader. WHY MEDIUM: every job created without a project reaches all three, in the job listing, in `project adopt` and in project scoping, with no error to show it. WHY F275's: its own flip commit `ebc0182c` put these readers onto the unified record. FIX: each of the three reads an empty or absent `project_id` as no project, and the four tests above pin it.
END RECORD103

── SLICE SLIP103 ── target `.agent/prose_slips.md` ── APPEND ──
BEGIN SLIP103 sha256=d1dcca341871b3d77cbc28fd42e0b55fa89c864506556f20ea6f496093cb0d51

2026-09-14 · F275 R102 · The round 102 block ordered its C0 as ONE commit of `.agent/authored/f275-r102.md` and `.agent/last_block.md` while its constraint 4 ordered every commit under 500 insertions, and the two whole-file writes together were 504; the worker split C0 into two commits and declared it. THE RULE THAT FOLLOWS: a commit a block orders to hold more than one whole-file write sums those files' insertions against the cap before the block leaves.
END SLIP103

── SLICE DEC103 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC103 sha256=d28c9bf2f79e79e317f112dc467d9cee8980e35fd09373cba706c7f18ee3d0e3

## DECISION F275 D77 (2026-09-14, F275 round 103) — the second bridge round repairs where the flip broke a contract, re-seeds the tests that still write a classic record, and keeps each test's premise where the unified record can carry it

CONTEXT. Round 102's committed transcript lists 29 bad nodes. Before authoring, the reviewer had two research agents diagnose them in disposable worktrees at `0fac911d`, then applied their repairs and its own in a third worktree and ran them: the nine changed test files and twelve neighbouring test files read 863 passed, and restoring each changed production file and the runtime smoke harness to its `0fac911d` form made exactly the tests named in round 103's block fail.

CHOSEN, FIRST: WHERE THE FLIP BROKE A CONTRACT, PRODUCTION IS REPAIRED. The transform renamed a construction or a loader without the contract behind it. `do_mission` hands `JobPlan.budgets` a pydantic `JobBudgets` where the record declares a dict, so the save fails to serialize. `run_job_fulfill` and three loads of the test execution service call `load_job_plan`, which answers `None`, where the classic `load_job` raised, so a missing job travels on as `None`, and the fulfilment and usage-accounting tests fail. `job context` reads a `TaskEntry`'s own empty `files_hint` ahead of the flight plan's scope, which `map_flight_plan_to_tasks` writes into the flight block. `R-0885` and `R-0886` are the two defects the suite could not see in full. ALTERNATIVE for the job context command: have `map_flight_plan_to_tasks` also fill `TaskEntry.files_hint`, rejected here because `run_job` reads that field as the task's fence, so it would change what a flight-planned job executes, not what the command shows.

CHOSEN, SECOND: A TEST THAT SEEDS A CLASSIC RECORD IS RE-SEEDED, NOT DELETED. The plan approval tests save their `JobPlan` in-process instead of spawning a child that writes a classic `Job`; the kill-and-resume child builds, saves and reloads a unified record; the scoped listings, golden path, proposed-task and runtime smoke fixtures write `jobs/<id>/job.json` instead of `jobs/<id>.json`; the repair loop tests stop parsing a sixteen-hex id as a UUID. One premise changes and is ruled here: `test_adopting_a_pingpong_job_id_exits_cleanly_instead_of_crashing` wrote a sixteen-hex record the classic store could not find and expected "job not found"; after the flip that id names a real unified record, so the test adopts it and asserts the adoption, which keeps its guard against a `UUID(...)` parse of that id. ALTERNATIVE: deleting it, rejected because the parse guard it carries is the repair of finding `R-0882`.

CHOSEN, THIRD: WHAT THE FLIP LEFT UNREACHABLE WAITS FOR THE CLASSIC STORE ROUND. `_JobPlanAdapter` in `packages/orchestration/ui_server.py` is built by nothing in production at `0fac911d`, and `resolve_job_id` still searches the classic store; `test_job_plan_adapter_has_required_fields` reads the adapter's status `.value` again, as it did before the transform rewrote that line, and both go when the classic store goes.

CONSEQUENCE. `R-0885` and `R-0886` are registered by the commit that lands this paragraph and repaired by round 103's code commits; their `Done:` paragraphs belong to the round that reviews them. `R-0809`, `R-0880`, `R-0883` and `R-0884` stay open.

HOW TO REVERSE. Delete this paragraph block and revert round 103's code and test commits; the 29 nodes are bad again, and a save interrupted part-way can tear a record again.
END DEC103

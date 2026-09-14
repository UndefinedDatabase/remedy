── STEP T003 — F275 — ROUND 99 ──
Goal: Commit the flip's tenth OVERLAY, applied after the first nine to the flipped tree at
`844a7f21`: the checkpoint writer measures a job's snapshot at the unified record's path, the
tests touching a job's record on disk follow that path, the mission command tests build their
jobs as unified records, and the layout guard stops pinning the checkpoint module to the
classic store; measured by the full suite in fresh flipped trees.

Base commit: `e7c09077`. The chain's base stays `844a7f21`, per DECISION F275 D64. Round type:
SPLIT. No path under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/` changes; the overlay
edits production code and nine test files, carried in a diff, and G6 red-proves the production
edit twice.

THE FRAME RULE, per item 37 of §3, stated as the property MEASURED over the final bytes: NO LINE
of this block is a run of a single repeated character, and every box-drawing rule inside the
STEP and SLICE header lines is exactly two characters long.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f275-r99.md`             the block, saved verbatim
C0b `.agent/last_block.md`                    mirrored FROM THE COMMITTED C0a BLOB
C1  `.agent/plan.md`                          slice PLAN99, a full replacement
C2  `.agent/live_review.md`                   slice RECORD99 appended, the round 98 verdict
C3  `.agent/prose_slips.md`                   slice SLIPS99 appended
C4  `.agent/authored/f275-r99-overlay-<k>.md` the overlay carriers of SPEC C, ONE COMMIT EACH
C5  `.agent/decisions.md`                     slice DEC99 appended
C6  `.agent/handoff.md`                       the handback

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3.

## Change — exactly these paths and no others

The Bundle's paths, `<k>` running from 1 over the carriers SPEC C produces.

## SPEC O — the edits, made in the EDIT worktree of constraint 8 on top of the ninth overlay

SPEC O edits these paths and no others: `packages/orchestration/checkpoints.py`,
`tests/cli/test_job_report.py`, `tests/cli/test_mission_cmd.py`,
`tests/orchestration/test_checkpoints.py`, `tests/orchestration/test_handoff.py`,
`tests/orchestration/test_long_run_executor.py`, `tests/orchestration/test_mission_state.py`,
`tests/orchestration/test_resume_cli.py`, `tests/orchestration/test_resume_kill.py`,
`tests/test_data_paths.py`.
O1 THE CHECKPOINT'S SNAPSHOT. Inside the `try` of `_job_snapshot_reference` in `checkpoints.py`,
the local import reads `from packages.orchestration.data_paths import job_record_path,
resolve_data_root` on one line; `path = jobs_dir() / f"{job_id}.json"` becomes
`path = job_record_path(job_id)`; directly after `data = path.read_bytes()` comes the new
statement `relative = path.relative_to(resolve_data_root()).as_posix()`; and the `return` after
the `try` hands back `relative` where it built `f"jobs/{job_id}.json"`, its digest unchanged. The
docstring and the `except (OSError, ValueError)` clause stay as they are.
O2 THE FLAT PATH IN THE TESTS. In each function named here, ONE f-string changes, 13 in all:
`<base> / f"{E}.json"` becomes `<base> / E / "job.json"`, and `f"jobs/{E}.json"` becomes
`f"jobs/{E}/job.json"`, `E` unchanged. `_job_file` of `test_job_report.py`;
`test_a_deleted_job_renders_as_missing_and_never_crashes` and
`test_not_even_when_the_goal_smells_long_lived` of `test_mission_cmd.py`; `make_checkpoint`,
`test_build_checkpoint_records_the_persisted_snapshot` and
`test_the_checkpoint_references_the_persisted_snapshot` of `test_checkpoints.py`;
`_seed_job_checkpoint` of `test_handoff.py`; `test_default_step_runs_the_real_single_task_path`
of `test_long_run_executor.py`; `test_a_deleted_job_renders_as_missing_and_never_crashes`,
`test_an_unreadable_job_is_not_reported_as_missing` and
`test_a_gone_previous_job_refuses_rather_than_verifying_blind` of `test_mission_state.py`;
`put_checkpoint` of `test_resume_cli.py`; and
`test_the_kill_leaves_checkpoints_for_the_committed_cycles` of `test_resume_kill.py`.
O3 THE MISSION FIXTURES, in `test_mission_cmd.py`. In the subprocess script of each of
`_link_job`, `_pending_plan_job` and `TestContinue._green_job`: the script piece
`"from packages.core.models import Job, RunState;"` becomes
`"from packages.core.models import RunState;"`; the piece
`"from packages.orchestration.storage import save_job;"` becomes
`"from packages.orchestration.pingpong_job import JobPlan, save_job_plan;"`; `Job(name=` becomes
`JobPlan(job_title=` with the name's value and every other keyword kept; `save_job(job);` becomes
`save_job_plan(job);`; and `str(job.id)` and `job.id` become `job.job_id`. In
`test_the_cockpit_reads_the_carried_module_and_says_so`, the class attribute `id` of the double
`_Job` becomes `job_id`, its value kept.
O4 THE CLASSIC-STORE GUARD, in `test_data_paths.py`. `test_the_classic_store_modules_still_call_jobs_dir`
imports `storage` alone and loops `for module in (storage,):`; its name stays. Its docstring, the
docstring of `test_no_module_that_owns_job_evidence_spells_the_path_itself` and the comment
above `_JOB_EVIDENCE_OWNING_MODULES` stop naming `checkpoints.py` as a module of the classic
store: each says `storage.py` is the one that names it, and the comment and the guard's
docstring add, in one sentence each, that `checkpoints.py` called `jobs_dir` until the flip moved
its job snapshot onto `job_record_path`. Nothing else in that file changes.
The function names are the reviewer's reading of `844a7f21` flipped through nine overlays;
where one differs, the site is located by its text and the difference declared.

## SPEC C — the carriers, at C4

The VERBATIM stdout of `git diff` in EDIT, against its index as constraint 8 stages it, is cut at
`diff --git` lines into consecutive parts in its own order, each part as many whole file diffs as
fit in 440 lines, a new part starting only when the next file diff would not fit. Part `<k>` is
`.agent/authored/f275-r99-overlay-<k>.md`: at most 40 lines of prose naming its base `844a7f21`,
that the flipped tree is built as G4 of `.agent/authored/f275-r99.md` orders, that the parts form
the TENTH overlay and apply after `.agent/authored/f275-r98-overlay-1.md` in `<k>` order, and
how to apply each — extract the fence, `git apply --check`, then `git apply`; then exactly ONE
fence, a line of three backticks and `diff`, the part, and a line of three backticks; nothing
after it but one newline. Joined in `<k>` order, the fences equal the whole diff byte for byte.

## Constraints

1. NO SLICE IS EDITED. PLAN99, RECORD99, SLIPS99 and DEC99 land byte for byte; a discrepancy
   inside one is DECLARED, never repaired.
2. SPEC O and SPEC C are the worker's OWN work. The reviewer's scratch `.remedy-wt/r90/` through
   `.remedy-wt/r98/` is not opened.
3. READ `.agent/STOP` before C0a and before C6, with real exit codes. If it appears, finish the
   commit in hand, write the handoff and end.
4. Every commit stages EXACTLY ONE path and stays under 500 insertions.
5. No `.py` file under `.agent/`; scratch under `.remedy-wt/r99w/`, uncommitted; every scratch
   output path absolute.
6. No landed record is rewritten: the `.agent/live_review.md`, `.agent/prose_slips.md` and
   `.agent/decisions.md` commits are APPENDS with a ZERO deletion column.
7. No `gh`, no `remedy`, no pull request, no branch created or deleted, no merge, NEVER a
   force-push, no history rewrite. Not even a version query.
8. THREE worktrees, each `git worktree add --detach` at `844a7f21` under `.remedy-wt/r99w/`:
   EDIT, CONTROL and OVERLAY. In each: the transform as G4 orders, `git add -A`, then for each of
   `.agent/authored/f275-r90-overlay.md`, `.agent/authored/f275-r91-overlay.md`,
   `.agent/authored/f275-r92-overlay-1.md` through `-4.md`, `.agent/authored/f275-r93-overlay-1.md`
   and `-2.md`, `.agent/authored/f275-r94-overlay-1.md` and `-2.md`,
   `.agent/authored/f275-r95-overlay-1.md` through `-4.md`, `.agent/authored/f275-r96-overlay-1.md`,
   `.agent/authored/f275-r97-overlay-1.md` and `.agent/authored/f275-r98-overlay-1.md`, overlay by overlay in that order, the fences of the
   COMMITTED carriers applied with `git apply --check` then `git apply`, and `git add -A` once
   after each overlay's parts. Only EDIT receives SPEC O, and any test may run there while it is
   made; before the diff is taken its `git diff --name-only` lists exactly SPEC O's paths. Only
   OVERLAY receives the C4 carriers. All three are REMOVED AND PRUNED before C5, without
   `--force`. The generator's trees are plain directories.
9. THE BLOCK'S OWN SIZE, measured on its final bytes: 307 lines TOTAL and 239 lines of
   PROSE, against the caps of 490 and 400.
10. GATE ORDER. G4's setup — the generator, the three worktrees, the chain — runs after C3 and
    before the first C4 commit, because the carriers are cut from EDIT; G4's readings, G5 and G6
    are taken after the last C4 commit and strictly before C5, per item 31 of §3. DEC99's
    measured figures are G4(b)'s readings — 17 f-strings in CONTROL and 2 in OVERLAY, and three
    classic fixture scripts in CONTROL — and its ten paths are SPEC O's list; DEC99 quotes no G5
    or G6 reading. G1, G2, G3, G7 and G8 run at C5. No gate runs after C6; C6's own numbers
    are the reviewer's.
11. A RED G5 IS A STOP. Each node G5 finds bad only in OVERLAY is re-run by its node id alone in
    OVERLAY three times with G5's environment; unless every re-run passes, the worker commits
    nothing further after C4 except the handback, which lists every such node with its last
    `E   ` line. A node whose three re-runs all pass is reported FLAKY with the three tallies.

## Done when — the gates, each run for real and its exit code recorded

G1 TRANSPORT, BUDGET, SLICES. `.agent/authored/f275-r99.md` at C0a against the block as received,
by `cmp`; `.agent/last_block.md` at C0b byte-identical to the COMMITTED C0a blob. Extract the
slices by their markers, report how many were FOUND, check each against its BEGIN-marker
sha256, and re-measure TOTAL and PROSE against constraint 9.

G2 THE PLAN. `.agent/plan.md` at C1 byte-identical to PLAN99 from the COMMITTED C0a blob; at
most 50 lines; one `## Goal` and one `## Next Steps`.

G3 THE RECORD. For the appends at C2 into `.agent/live_review.md` and at C5 into
`.agent/decisions.md`, FULL FORENSICS: the pre-commit blob read with `git show` at the commit's
PARENT, its length printed — 1157489 and 1305147 — READER A with the arithmetic printed; READER B
over the file's LAST N blank-line units against the slice's N paragraphs IN ORDER, N counted by
the script; a letter flipped in the FIRST appended paragraph REJECTED by both readers; deletion
column 0. `.agent/prose_slips.md` at C3 equals its 304743-byte pre-commit blob followed by
exactly SLIPS99. Derive the ledger's `Gate:` header pattern from the file, report how many heads
it matches, and that RECORD99's header matches it and duplicates none.

G4 THE TREES, THE CHAIN AND THE CARRIERS, set up and read per constraint 10. The generator trees
and run exactly as G4 of `.agent/authored/f275-r90.md` orders, the pinned digests checked first,
with the readings that block states; the transform in each worktree reading 2183 resolving and 0
not, 264 files, 6097 rewrites and 0 broken; every earlier overlay applying with exit 0 in each.
Then: (a) the fences extracted from the COMMITTED C4 blobs: report the part count and each part's
line count, each at most 440; joined in `<k>` order they equal EDIT's diff; in OVERLAY each
applies with `git apply --check` and `git apply` exit 0, in order; `git diff --name-only` there,
against the index constraint 8 staged, lists exactly SPEC O's paths by name, each byte-identical
to EDIT's; report MISSING and EXTRA. (b) With `ast`, over SPEC O's ten paths, each reading given
as CONTROL then OVERLAY, names matched EXACTLY: f-strings whose LAST literal part is exactly
`.json` and that hold exactly one formatted value whose source text ends in `job_id`, 17 and 2,
listed per path, the 2 both in `tests/test_data_paths.py`; string constants, the literal parts
of f-strings included, containing `from packages.orchestration.storage import save_job;`, 3 and
0, and containing `from packages.orchestration.pingpong_job import JobPlan, save_job_plan;`, 0
and 3; `Assign` targets in the body of the class `_Job` inside
`test_the_cockpit_reads_the_carried_module_and_says_so` named `id`, 1 and 0, and named `job_id`,
0 and 1; inside `test_the_classic_store_modules_still_call_jobs_dir`, bare names plus import
aliases named `checkpoints`, 2 and 0. (c) `ruff check --output-format concise`, run from inside
each of CONTROL and OVERLAY over SPEC O's paths, rows compared as a MULTISET of
`<path>: <code> <message>` with line and column DROPPED: added 0 and removed 0. The reviewer read
16 rows in each; the exit is 1 in BOTH trees and is reported, never ordered.

G5 THE FULL SUITE IN FRESH FLIPPED TREES, per constraint 10, CONTROL first and OVERLAY second,
serially. Each is its worktree's FIRST pytest run of any kind, `apps/ui/node_modules` and
`apps/ui/dist` reported absent before it. `cwd` the worktree; `PYTHONPATH`, `REMEDY_PROJECT` and
`REMEDY_DATA_DIR` removed; `PYTHONDONTWRITEBYTECODE=1`;
`packages.orchestration.pingpong_job.__file__` printed and inside the worktree;
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`. A bad node is the
text after `FAILED ` or `ERROR ` up to the first ` - ` or the line's end. The reviewer measured
CONTROL `84 failed, 18351 passed, 29 skipped, 1 warning, 7 errors`, 91 bad nodes, and its own
dry run of SPEC O `64 failed, 18371 passed, 29 skipped, 1 warning, 7 errors`, 71; one node of
those 71 was bad only in the dry run,
`tests/ui_server/test_command_channel.py::TestCommandChannelDoor::test_post_to_non_commands_path_is_405`
with `Server did not start in time`, and passed three re-runs by its id alone. REPORT OVERLAY's
tally and bad-node count. Bad only in OVERLAY, less the nodes constraint 11 reports FLAKY: MUST
be 0. REPORT the fixed nodes' count per test file.

G6 THE PROBES, per constraint 10, in OVERLAY after G5; `__pycache__` purged before each run;
G5's environment; flags `-q -p no:randomly -p no:cacheprovider --tb=short -rfE`. For each
mutation, the bytes it replaces counted as stated first, then the selection run UNMUTATED and
MUTATED, each tally and exit code reported with the node ids bad only under the mutation, then
the file restored and its bytes confirmed. Both mutations are in
`packages/orchestration/checkpoints.py`, inside `_job_snapshot_reference` only, where the bytes
each replaces count 1 there and 1 in the file, and both run over
`tests/orchestration/test_checkpoints.py`, where
`TestWriting::test_build_checkpoint_records_the_persisted_snapshot` and
`TestCycleBoundaryWiring::test_the_checkpoint_references_the_persisted_snapshot` MUST go bad under
each. M1 replaces `relative = path.relative_to(resolve_data_root()).as_posix()` with
`relative = f"jobs/{job_id}.json"`. M2 replaces `path = job_record_path(job_id)` with
`path = job_record_path(job_id).parent.with_suffix(".json")`. The reviewer's dry run read
`37 passed` unmutated and `2 failed, 35 passed` mutated, for each.

G7 TREE, CANARY, LINT, PATH SET, OPEN SET, at C5. `git status --porcelain` prints `''`;
`git worktree list` one row; `git diff --name-only e7c09077 C5 -- packages apps tests docs
scripts` empty; the canary `python3 -B -m pytest tests/cli/test_golden_path.py -q` exit 0, 42;
`ruff check . --output-format concise` rows as a MULTISET at `e7c09077`, read from a
`git archive` tree, and at C5, difference empty, 26 at `e7c09077`. The changed-path set of
`e7c09077`..C5 against the Bundle's paths MINUS `.agent/handoff.md`, MISSING and EXTRA by name.
The open set BY DISTINCT ID at `e7c09077` and at C5: 88 at both, membership identical;
`R-0809`, `R-0880` and `R-0883` open.

G8 THE INSERTION CAP over `e7c09077`..C5: one row per commit with insertions, deletions and
staged path count, and the number of commits reaching 500 insertions.

Handback: `.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 33 of feature F275 · round 99 · rounds so far 99`; the Commits table read from
`git show --numstat` and compared cell by cell against G8, C6's row carrying no numbers and
saying why; one Verification line per gate with its REAL exit code; External actions;
Authored-text proofs; Item-status; Deviations; `## Next` stating `Operator questions open: 1`.
NO SCOPE REPORT AND NO SESSION-LIMIT BANNER, by amendment amend0911-f275-to-scope.

── SLICE PLAN99 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN99 sha256=8d6738e5e079f0b667348db670f043c8c5d3bab48f438ca4f1b1de67105ce15a
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001 and T002 are DONE, and the classic runner's whole
command surface is gone as of round 34.

## Current Step

ROUND 99 ADDS THE FLIP'S TENTH OVERLAY, on top of the first nine, under DECISION F275 D64's
method. The checkpoint writer measures a job's snapshot at the unified record's own path,
tests that touch a job's record on disk use that path, the mission command tests build their
jobs as unified records, and the layout guard stops pinning the checkpoint module to the
classic store. The diff is carried in a carrier, so no path under `packages/`, `apps/` or
`tests/` moves; the round books the round 98 verdict and its prose slip.

## Next Steps

1. MORE OVERLAYS, one residue group each, every one applied on top of those before it:
   production code that hands a `JobPlan` a `JobBudgets` model where the record holds its
   serialized dict; the self-dogfood runtimes; the classic-shaped tests of routed handlers in
   `tests/test_data_paths.py`; and what is left of the classic runner under `job resume`,
   whose kill-and-resume fixture still builds a classic job.
2. THE FLIP: the transform, then every overlay in round order, landed as a series of commits
   each under the 500-insertion cap inside one round, carrying DECISION F275 D48's obligations
   and registering the structured acceptance form DECISION F275 D22 leaves to it, unless the
   operator allows one more oversized commit.
3. Then the classic store, with the which-store branches and adapters the overlays leave
   unreached, then the closure sequence.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20
  sessions and 60 rounds without a replacement, so this feature closes only at full scope.
- THE FLIP IS NOT CLOSE: many test nodes still fail in the flipped tree, and a test that starts
  the command line from a directory outside that tree runs this checkout's code instead.
- AN OVERLAY IS A DIFF AGAINST A FIXED TREE: it holds only while the production tree stays at
  `844a7f21`, and it depends on the generator and transform staying reproducible from round
  77's two scratch JSON files.
- ONE ROUTED LOAD IS REACHED BY NO TEST until `R-0883` is repaired.
- The open set is 88 by distinct id at this round's base, with `R-0809`, `R-0880` and `R-0883`
  open. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END PLAN99

── SLICE RECORD99 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD99 sha256=9d4383d5b306329a0434bad78e59afc6211926fd3e8d1922f87bac42f25137c5

Gate: F275 R98 — the F275 round 98 entry. VERDICT PASS. Written by the planner and reviewer of session 33 after reading the committed range `ac17fd6e`..`e7c09077` and RE-DERIVING EVERY GATE AND EVERY PROBE INDEPENDENTLY; the worker's report and its transcripts were evidence for no line below. It is booked here by the FIRST SUBSTANTIVE COMMIT of round 99 that writes the record, per operator amendment amend0827-process-diet rule 1. The round moved no path under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/`; its code is the diff carried in `.agent/authored/f275-r98-overlay-1.md`.

WHAT THE TRANSPORT PROOF COVERS, per item 37 of §3. The committed `.agent/authored/f275-r98.md` blob was identical to the reviewer's own original at 24607 bytes, `.agent/last_block.md` equalled it from its own commit through `e7c09077`, and all four slices matched their BEGIN-marker digests; `.agent/plan.md` equalled PLAN98. The three appends were exact under reader A — 1154699 plus 2790 into the review record, 304316 plus 427 into the prose slips and 1302522 plus 2625 into the decisions — with reader B holding at N counted from each slice as 3, 1 and 6, and a letter flipped in each FIRST appended paragraph rejected by both readers. Every commit staged one path, the largest the carrier at 327 insertions, and its one fence reads 286 lines.

THE OVERLAY HOLDS UNDER THE REVIEWER'S OWN RE-RUN. The reviewer transformed a worktree at `844a7f21` from its own generator run, applied and staged the committed overlays of rounds 90 to 97, and applied the committed round 98 fence: `git apply --check` and `git apply` exited 0, 9 paths changed, seven of them production code, and the diff was byte-identical to the reviewer's own dry run of SPEC O. With `ast`, under SPEC O1's rule read over the statement list that holds the `try`, the `load_job_plan` sites read 0 and the `require_job_plan` sites 13, against 13 and 0 in the same worktree before the fence; in the three functions SPEC O2 names, the classic record keys, the unified keys and the flat `.json` f-strings read 0, 3 and 0, against 3, 0 and 3; the `ruff` rows over the 9 files read 10 in each as a multiset with line and column dropped, none added. The reviewer's first full run of that byte-identical diff, in a fresh flipped tree of its own, read 84 failed, 18351 passed, 29 skipped and 7 errors, 91 bad nodes, against 113 in a fresh run of the chain before it: 22 fixed and none newly bad. In the reviewer's worktree, loading with `load_job_plan` again in `_cmd_contract_inspect` made exactly `test_missing_job_safe` and `test_invalid_job_safe` of `TestContractInspectCLI` bad, and doing the same in `start_repair_loop_v0` made exactly `test_repair_loop_job_not_found` and `test_repair_start_job_not_found` bad. In the primary checkout at `e7c09077` the canary read 42 and `ruff check .` read 26 rows against 26 at `ac17fd6e`, the difference empty; the open set stayed 88 with identical membership, `R-0809`, `R-0880` and `R-0883` open. The worker declared that the rule's words, read literally, point at the `try` body, and used the reading its counts came from.
END RECORD99

── SLICE SLIPS99 ── target `.agent/prose_slips.md` ── APPEND ──
BEGIN SLIPS99 sha256=177a9f7e140e0cd765e844279395bab31d042e7154e1513682033796454b42d9

2026-09-14 · F275 R98 · THE RULE of SPEC O1 in the round 98 block said "the first later statement of the same statement list" right after naming the `try` body as the list holding the `Assign`, while the reviewer's scan read the statement list that holds the `try`; read literally the words match 10 other calls and none of the 13 named, and the worker used the scan's reading and declared it. THE RULE THAT FOLLOWS: a structural rule that names two nested statement lists says which one each clause reads, in the words of the scan that produced its figure.
END SLIPS99

── SLICE DEC99 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC99 sha256=b236320e7e6c426333c223947893c7f112684aec980e77c139cfa1b8cfca46fd

## DECISION F275 D73 (2026-09-14, F275 round 99) — the tenth overlay: a job's record on disk is read at the unified store's path, and the mission command tests build their jobs as unified records

CONTEXT. In the flipped tree at `844a7f21`, with nine overlays applied, a job's record is `job.json` inside a directory named by the job id, but the checkpoint writer measures its job snapshot at the classic flat path `jobs/<id>.json`, finds nothing there, and records neither a path nor a digest. Tests that delete, corrupt or read a job's record use the same flat path, and three job fixtures in `tests/cli/test_mission_cmd.py` build a classic `Job` and save it with the classic `save_job` inside a subprocess script, where the transform's `ast` rewrite cannot see them. Over the ten paths the overlay touches, 17 f-strings spell a `.json` file name after a job id, and `tests/test_data_paths.py` pins `checkpoints.py` as a module that must keep calling `jobs_dir`.

CHOSEN, FIRST: THE CHECKPOINT MEASURES THE UNIFIED RECORD. `_job_snapshot_reference` reads `job_record_path(job_id)` and records that path relative to the data root, so the path a checkpoint carries is whatever `data_paths` says a record's path is, per DECISION F260 D1. ALTERNATIVE: spelling `jobs/<id>/job.json` by hand in the checkpoint module, rejected because a layout spelled at a call site is how the flat path outlived the store it named.

CHOSEN, SECOND: THE TESTS FOLLOW THE RECORD. The flat paths in the tests the overlay touches name the record's own directory; the three subprocess fixtures build a `JobPlan` and call `save_job_plan`; a readiness double names its id `job_id`; and the guard that pinned `checkpoints.py` to the classic store ranges over `storage.py` alone, its comments saying why. The 2 flat paths left, both in `tests/test_data_paths.py`, write classic records for the job-id resolver's tests and stay until the classic store goes. ALTERNATIVE: dropping `checkpoints.py` from the guard without a word, rejected because the guard's comments exist to stop an exclusion nobody can explain.

CONSEQUENCE. What the overlay fixes, and that it newly breaks nothing, is measured by the gates of round 99's block and recorded in the round 99 ledger entry by the round that books its verdict. `R-0809`, `R-0880` and `R-0883` stay open, and no finding is registered or resolved.

HOW TO REVERSE. Delete the round 99 overlay carriers under `.agent/authored/` and this paragraph block; in the flipped tree a checkpoint then records no job snapshot again and the mission command tests cannot find their jobs.
END DEC99

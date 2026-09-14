── STEP T003 — F275 — ROUND 100 ──
Goal: Commit the flip's eleventh OVERLAY, applied after the first ten to the flipped tree at
`844a7f21`, editing tests only: reads of a proposed task's and a project-brain node's id read
`id` again, two classic models reached through `__import__` become unified records, and
`MagicMock` job doubles set `job_id` and `job_title`; measured by the full suite in fresh flipped
trees.

Base commit: `71dbb930`. The chain's base stays `844a7f21`, per DECISION F275 D64. Round type:
SPLIT. No path under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/` changes; the overlay
edits seventeen test files and no production code, carried in a diff, so no mutation probe is
ordered.

THE FRAME RULE, per item 37 of §3, stated as the property MEASURED over the final bytes: NO LINE
of this block is a run of a single repeated character, and every box-drawing rule inside the
STEP and SLICE header lines is exactly two characters long.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f275-r100.md`             the block, saved verbatim
C0b `.agent/last_block.md`                     mirrored FROM THE COMMITTED C0a BLOB
C1  `.agent/plan.md`                           slice PLAN100, a full replacement
C2  `.agent/live_review.md`                    slice RECORD100 appended, the round 99 verdict
C3  `.agent/authored/f275-r100-overlay-<k>.md` the overlay carriers of SPEC C, ONE COMMIT EACH
C4  `.agent/decisions.md`                      slice DEC100 appended
C5  `.agent/handoff.md`                        the handback

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. No prose slip is carried this round, so
`.agent/prose_slips.md` is not in the Bundle.

## Change — exactly these paths and no others

The Bundle's paths, `<k>` running from 1 over the carriers SPEC C produces.

## SPEC O — the edits, made in the EDIT worktree of constraint 8 on top of the tenth overlay

SPEC O edits these paths and no others: `tests/cli/test_job_commands.py`,
`tests/cli/test_self_dogfood_execution_cli.py`, `tests/orchestration/test_approval_queue.py`,
`tests/orchestration/test_autorun.py`, `tests/orchestration/test_self_dogfood_execution.py`,
`tests/orchestration/test_source_apply.py`, `tests/orchestration/test_test_execution_service.py`,
`tests/orchestration/test_test_runner.py`, `tests/regression/test_named_bugs.py`,
`tests/test_patch_apply.py`, `tests/test_project_brain.py`,
`tests/ui_contracts/test_graph_architecture.py`, `tests/ui_contracts/test_responsive.py`,
`tests/ui_contracts/test_ux_quality.py`, `tests/ui_server/test_brain_view_model.py`,
`tests/ui_server/test_dashboard_cockpit_truth.py`, `tests/ui_server/test_live_state.py`.
O1 A PROPOSED TASK'S ID. In `test_self_dogfood_execution.py`, every `pt.job_id` handed as the
FIRST argument of `SE.evaluate_self_execution_eligibility` or `SE.start_self_execution` becomes
`pt.id` — once in each of `test_approved_self_task_eligible`, `test_main_branch_blocks`,
`test_unknown_branch_blocks`, `test_contract_blocked`, `test_execute_awaits_candidate`,
`test_main_blocks_start` and `test_next_actions_catalog_backed`, and twice in
`test_execute_idempotent_resume` — and `unapproved.job_id` becomes `unapproved.id` in
`test_unapproved_blocks`. In `_approved_task` of `test_self_dogfood_execution_cli.py`, the
returned `tasks[0].job_id` becomes `tasks[0].id`. The `str(job.job_id)` beside each stays.
O2 A BRAIN NODE'S ID. In `test_project_brain.py`, `job_nodes[0].job_id` in
`test_empty_job_has_job_node` and `task_nodes[0].task_id` in `test_task_nodes_and_edges` read
`.id`; the right-hand side of each comparison stays.
O3 THE TWO CLASSIC CONSTRUCTIONS. In `test_symlink_escape_blocked` of `test_patch_apply.py`,
`__import__("packages.core.models", fromlist=["Job"]).Job(job_title="symlink test")` becomes
`JobPlan(job_title="symlink test")`, the module already importing `JobPlan`. In
`test_proof_not_verified_from_event_presence` of `test_dashboard_cockpit_truth.py`,
`__import__("packages.core.models", fromlist=["Task"]).Task(title="x")` becomes
`TaskEntry(title="x")`, and the module's `from packages.orchestration.pingpong_job import
JobPlan` reads `JobPlan, TaskEntry`.
O4 THE JOB DOUBLES. THE RULE, read with `ast` under `tests/`: in a function where the bare name
`job` is the target of an `Assign` whose value is a call of the bare name `MagicMock` or `Mock`,
each `Assign` target that is the attribute `id` or `name` of that bare name `job`. The reviewer's
reading finds 37 such targets in 19 functions of twelve files, which are SPEC O's paths other
than the five O1 to O3 name. Each target `job.id` becomes `job.job_id` and each `job.name`
becomes `job.job_title`, the assigned values unchanged. Two reads follow: in
`test_accept_recommendation` of `test_approval_queue.py`, `load_proposed_tasks(str(job.id))`
reads `str(job.job_id)`; in `test_usage_incremented_on_process_start` of
`test_test_execution_service.py`, `job_id=str(job.id),` reads `job_id=str(job.job_id),`.
The function names are the reviewer's reading of `844a7f21` flipped through ten overlays;
where one differs, the site is located by its text and the difference declared.

## SPEC C — the carriers, at C3

The VERBATIM stdout of `git diff` in EDIT, against its index as constraint 8 stages it, is cut at
`diff --git` lines into consecutive parts in its own order, each part as many whole file diffs as
fit in 440 lines, a new part starting only when the next file diff would not fit. Part `<k>` is
`.agent/authored/f275-r100-overlay-<k>.md`: at most 40 lines of prose naming its base
`844a7f21`, that the flipped tree is built as G4 of `.agent/authored/f275-r100.md` orders, that
the parts form the ELEVENTH overlay and apply after `.agent/authored/f275-r99-overlay-1.md` in
`<k>` order, and how to apply each — extract the fence, `git apply --check`, then `git apply`;
then exactly ONE fence, a line of three backticks and `diff`, the part, and a line of three
backticks; nothing after it but one newline. Joined in `<k>` order, the fences equal the whole
diff byte for byte.

## Constraints

1. NO SLICE IS EDITED. PLAN100, RECORD100 and DEC100 land byte for byte; a discrepancy inside
   one is DECLARED, never repaired.
2. SPEC O and SPEC C are the worker's OWN work. The reviewer's scratch `.remedy-wt/r90/` through
   `.remedy-wt/r98/` is not opened.
3. READ `.agent/STOP` before C0a and before C5, with real exit codes. If it appears, finish the
   commit in hand, write the handoff and end.
4. Every commit stages EXACTLY ONE path and stays under 500 insertions.
5. No `.py` file under `.agent/`; scratch under `.remedy-wt/r100w/`, uncommitted; every scratch
   output path absolute.
6. No landed record is rewritten: the `.agent/live_review.md` and `.agent/decisions.md` commits
   are APPENDS with a ZERO deletion column.
7. No `gh`, no `remedy`, no pull request, no branch created or deleted, no merge, NEVER a
   force-push, no history rewrite. Not even a version query.
8. THREE worktrees, each `git worktree add --detach` at `844a7f21` under `.remedy-wt/r100w/`:
   EDIT, CONTROL and OVERLAY. In each: the transform as G4 orders, `git add -A`, then for each of
   `.agent/authored/f275-r90-overlay.md`, `.agent/authored/f275-r91-overlay.md`,
   `.agent/authored/f275-r92-overlay-1.md` through `-4.md`, `.agent/authored/f275-r93-overlay-1.md`
   and `-2.md`, `.agent/authored/f275-r94-overlay-1.md` and `-2.md`,
   `.agent/authored/f275-r95-overlay-1.md` through `-4.md`, and then
   `.agent/authored/f275-r96-overlay-1.md`, `.agent/authored/f275-r97-overlay-1.md`,
   `.agent/authored/f275-r98-overlay-1.md` and `.agent/authored/f275-r99-overlay-1.md`, overlay
   by overlay in that order, the fences of the COMMITTED carriers applied with
   `git apply --check` then `git apply`, and `git add -A` once after each overlay's parts. Only
   EDIT receives SPEC O, and any test may run there while it is made; before the diff is taken
   its `git diff --name-only` lists exactly SPEC O's paths. Only OVERLAY receives the C3
   carriers. All three are REMOVED AND PRUNED before C4, without `--force`. The generator's
   trees are plain directories.
9. THE BLOCK'S OWN SIZE, measured on its final bytes: 276 lines TOTAL and 209 lines of
   PROSE, against the caps of 490 and 400.
10. GATE ORDER. G4's setup — the generator, the three worktrees, the chain — runs after C2 and
    before the first C3 commit, because the carriers are cut from EDIT; G4's readings and G5 are
    taken after the last C3 commit and strictly before C4, per item 31 of §3. DEC100's measured
    figures are G4(b)'s CONTROL readings, 11, 2, 2 and 37; DEC100 quotes no G5 reading. G1, G2,
    G3, G6 and G7 run at C4. No gate runs after C5; C5's own numbers are the reviewer's.
11. A RED G5 IS A STOP. Each node G5 finds bad only in OVERLAY is re-run by its node id alone in
    OVERLAY three times with G5's environment; unless every re-run passes, the worker commits
    nothing further after C3 except the handback, which lists every such node with its last
    `E   ` line. A node whose three re-runs all pass is reported FLAKY with the three tallies.

## Done when — the gates, each run for real and its exit code recorded

G1 TRANSPORT, BUDGET, SLICES. `.agent/authored/f275-r100.md` at C0a against the block as
received, by `cmp`; `.agent/last_block.md` at C0b byte-identical to the COMMITTED C0a blob.
Extract the slices by their markers, report how many were FOUND, check each against its
BEGIN-marker sha256, and re-measure TOTAL and PROSE against constraint 9.

G2 THE PLAN. `.agent/plan.md` at C1 byte-identical to PLAN100 from the COMMITTED C0a blob; at
most 50 lines; one `## Goal` and one `## Next Steps`.

G3 THE RECORD. For the appends at C2 into `.agent/live_review.md` and at C4 into
`.agent/decisions.md`, FULL FORENSICS: the pre-commit blob read with `git show` at the commit's
PARENT, its length printed — 1160621 and 1307742 — READER A with the arithmetic printed; READER B
over the file's LAST N blank-line units against the slice's N paragraphs IN ORDER, N counted by
the script; a letter flipped in the FIRST appended paragraph REJECTED by both readers; deletion
column 0. Derive the ledger's `Gate:` header pattern from the file, report how many heads it
matches, and that RECORD100's header matches it and duplicates none.

G4 THE TREES, THE CHAIN AND THE CARRIERS, set up and read per constraint 10. The generator trees
and run exactly as G4 of `.agent/authored/f275-r90.md` orders, the pinned digests checked first,
with the readings that block states; the transform in each worktree reading 2183 resolving and 0
not, 264 files, 6097 rewrites and 0 broken; every earlier overlay applying with exit 0 in each.
Then: (a) the fences extracted from the COMMITTED C3 blobs: report the part count and each part's
line count, each at most 440; joined in `<k>` order they equal EDIT's diff; in OVERLAY each
applies with `git apply --check` and `git apply` exit 0, in order; `git diff --name-only` there,
against the index constraint 8 staged, lists exactly SPEC O's paths by name, each byte-identical
to EDIT's; report MISSING and EXTRA. (b) With `ast`, over every tracked `.py` file under
`tests/`, each reading given as CONTROL then OVERLAY, names matched EXACTLY: Load-context
attributes named `job_id` whose value is the bare name `pt` or `unapproved`, or a subscript of
the bare name `tasks`, in O1's two files, 11 and 0; in `tests/test_project_brain.py`,
Load-context attributes named `job_id` off a subscript of the bare name `job_nodes` or named
`task_id` off a subscript of the bare name `task_nodes`, 2 and 0; attributes whose value is a
call of the bare name `__import__` with the first argument `"packages.core.models"`, 2 and 0;
THE RULE of O4's targets, 37 and 0; under the same rule's binding, `Assign` targets that are the
attribute `job_id` or `job_title` of `job`, 1 and 38. (c) `ruff check --output-format concise`,
run from inside each of CONTROL and OVERLAY over SPEC O's paths, rows compared as a MULTISET of
`<path>: <code> <message>` with line and column DROPPED: added 0 and removed 0. The reviewer read
34 rows in each; the exit is 1 in BOTH trees and is reported, never ordered.

G5 THE FULL SUITE IN FRESH FLIPPED TREES, per constraint 10, CONTROL first and OVERLAY second,
serially. Each is its worktree's FIRST pytest run of any kind, `apps/ui/node_modules` and
`apps/ui/dist` reported absent before it. `cwd` the worktree; `PYTHONPATH`, `REMEDY_PROJECT` and
`REMEDY_DATA_DIR` removed; `PYTHONDONTWRITEBYTECODE=1`;
`packages.orchestration.pingpong_job.__file__` printed and inside the worktree;
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`. A bad node is the
text after `FAILED ` or `ERROR ` up to the first ` - ` or the line's end. The reviewer measured
CONTROL `63 failed, 18372 passed, 29 skipped, 1 warning, 7 errors`, 70 bad nodes, and its own
dry run of SPEC O `46 failed, 18389 passed, 29 skipped, 1 warning, 7 errors`, 53. REPORT
OVERLAY's tally and bad-node count. Bad only in OVERLAY, less the nodes constraint 11 reports
FLAKY: MUST be 0. REPORT the fixed nodes' count per test file.

G6 TREE, CANARY, LINT, PATH SET, OPEN SET, at C4. `git status --porcelain` prints `''`;
`git worktree list` one row; `git diff --name-only 71dbb930 C4 -- packages apps tests docs
scripts` empty; the canary `python3 -B -m pytest tests/cli/test_golden_path.py -q` exit 0, 42;
`ruff check . --output-format concise` rows as a MULTISET at `71dbb930`, read from a
`git archive` tree, and at C4, difference empty, 26 at `71dbb930`. The changed-path set of
`71dbb930`..C4 against the Bundle's paths MINUS `.agent/handoff.md`, MISSING and EXTRA by name.
The open set BY DISTINCT ID at `71dbb930` and at C4: 88 at both, membership identical;
`R-0809`, `R-0880` and `R-0883` open.

G7 THE INSERTION CAP over `71dbb930`..C4: one row per commit with insertions, deletions and
staged path count, and the number of commits reaching 500 insertions.

Handback: `.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 33 of feature F275 · round 100 · rounds so far 100`; the Commits table read from
`git show --numstat` and compared cell by cell against G7, C5's row carrying no numbers and
saying why; one Verification line per gate with its REAL exit code; External actions;
Authored-text proofs; Item-status; Deviations; `## Next` stating `Operator questions open: 1`.
NO SCOPE REPORT AND NO SESSION-LIMIT BANNER, by amendment amend0911-f275-to-scope.

── SLICE PLAN100 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN100 sha256=b2da3289ae9c482b583677b340cc0c6726d290d0f45144bcd8ba8343c68acf4c
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

ROUND 100 ADDS THE FLIP'S ELEVENTH OVERLAY, on top of the first ten, under DECISION F275 D64's
method, and it edits tests only. Where the transform read the id of a proposed task or of a
project-brain node as a job's or a task's id, the test reads `id` again; two classic models a
test reached through `__import__` become the unified records they were already built as; and
`MagicMock` job doubles set the unified record's `job_id` and `job_title`. The diff is carried
in carriers, so no path under `packages/`, `apps/` or `tests/` moves; the round books the round
99 verdict.

## Next Steps

1. MORE OVERLAYS, one residue group each, every one applied on top of those before it:
   production code that hands a `JobPlan` a `JobBudgets` model where the record holds its
   serialized dict; the classic-shaped tests of routed handlers in `tests/test_data_paths.py`;
   what is left of the classic runner under `job resume`, whose kill-and-resume fixture still
   builds a classic job; and the job digest's stored goldens.
2. THE FLIP: the transform, then every overlay in round order, landed as a series of commits
   each under the 500-insertion cap inside one round, carrying DECISION F275 D48's obligations
   and registering the structured acceptance form DECISION F275 D22 leaves to it, unless the
   operator allows one more oversized commit.
3. Then the classic store, with the which-store branches and adapters the overlays leave
   unreached, then the closure sequence.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20
  sessions and 60 rounds without a replacement, so this feature closes only at full scope.
- THE FLIP IS NOT CLOSE: test nodes still fail in the flipped tree, and a test that starts the
  command line from a directory outside that tree runs this checkout's code instead.
- AN OVERLAY IS A DIFF AGAINST A FIXED TREE: it holds only while the production tree stays at
  `844a7f21`, and it depends on the generator and transform staying reproducible from round
  77's two scratch JSON files.
- ONE ROUTED LOAD IS REACHED BY NO TEST until `R-0883` is repaired.
- The open set is 88 by distinct id at this round's base, with `R-0809`, `R-0880` and `R-0883`
  open. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END PLAN100

── SLICE RECORD100 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD100 sha256=22d77bb4295894ee9c7aaba31a86df149702031e1c317d5f6ff9b3630415c0f6

Gate: F275 R99 — the F275 round 99 entry. VERDICT PASS. Written by the planner and reviewer of session 33 after reading the committed range `e7c09077`..`71dbb930` and RE-DERIVING EVERY GATE AND EVERY PROBE INDEPENDENTLY; the worker's report and its transcripts were evidence for no line below. It is booked here by the FIRST SUBSTANTIVE COMMIT of round 100 that writes the record, per operator amendment amend0827-process-diet rule 1. The round moved no path under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/`; its code is the diff carried in `.agent/authored/f275-r99-overlay-1.md`.

WHAT THE TRANSPORT PROOF COVERS, per item 37 of §3. The committed `.agent/authored/f275-r99.md` blob was identical to the reviewer's own original at 26552 bytes, `.agent/last_block.md` equalled it from its own commit through `71dbb930`, and all four slices matched their BEGIN-marker digests; `.agent/plan.md` equalled PLAN99. The three appends were exact under reader A — 1157489 plus 3132 into the review record, 304743 plus 561 into the prose slips and 1305147 plus 2595 into the decisions — with reader B holding at N counted from each slice as 3, 1 and 6, and a letter flipped in each FIRST appended paragraph rejected by both readers. Every commit staged one path, the largest the carrier at 343 insertions, and its one fence reads 303 lines.

THE OVERLAY HOLDS UNDER THE REVIEWER'S OWN RE-RUN. The reviewer transformed a fresh worktree at `844a7f21` from its own generator run, applied and staged the committed overlays of rounds 90 to 98, and applied the committed round 99 fence: `git apply --check` and `git apply` exited 0 and 10 paths changed, one of them production code. The diff differed from the reviewer's own dry run only in the wording of one comment and one docstring in `tests/test_data_paths.py`, which SPEC O4 left to the worker. With `ast`, the f-strings naming a `.json` file after a job id read 2 against 17 before the fence, the classic `storage` import in the subprocess fixtures 0 against 3 and the unified import 3 against 0, the double's `id` attribute 0 against 1, and the name `checkpoints` in the classic-store guard 0 against 2; the `ruff` rows over the 10 files read 16 in each as a multiset with line and column dropped, none added. That worktree's first full run read 63 failed, 18372 passed, 29 skipped and 7 errors, 70 bad nodes, against 91 in the reviewer's fresh run of the chain before it: 21 fixed and none newly bad. In the same worktree, recording the flat path again in `_job_snapshot_reference`, and separately measuring the snapshot at the flat path, each made exactly `test_build_checkpoint_records_the_persisted_snapshot` and `test_the_checkpoint_references_the_persisted_snapshot` bad. In the primary checkout at `71dbb930` the canary read 42 and `ruff check .` read 26 rows against 26 at `e7c09077`, the difference empty; the open set stayed 88 with identical membership, `R-0809`, `R-0880` and `R-0883` open.
END RECORD100

── SLICE DEC100 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC100 sha256=5f745b2773a5968d03392056f58866a2f77f44892a018f09d051c3fc9ac25cbf

## DECISION F275 D74 (2026-09-14, F275 round 100) — the eleventh overlay: tests read a proposed task's and a brain node's own id again, build unified records where they already meant to, and give their job doubles the unified record's names

CONTEXT. In the flipped tree at `844a7f21`, with ten overlays applied, the rewrite of `.id` reads reached records that are not jobs or tasks. In the two self-dogfood execution test files, 11 reads of a proposed task's `id` — off `pt`, `unapproved` and `tasks[0]` — became `job_id`, so the proposed task's job id is handed on as its own id and the eligibility checks find no such proposed task. In `tests/test_project_brain.py`, 2 reads of a brain node's `id` became `job_id` and `task_id`, which a brain node does not have. 2 constructions reach `packages.core.models` through `__import__`, which a rewrite of imported names cannot see, so they build a classic `Job` and `Task` with the unified keywords. And 37 assignments give a `MagicMock` job double the classic `id` and `name`, while the flipped code reads `job_id` and `job_title` off it.

CHOSEN, FIRST: EACH READ NAMES THE RECORD IT READS. The proposed-task and brain-node reads read `id`, and the two constructions build `JobPlan` and `TaskEntry`, the records their keywords already name. ALTERNATIVE: teaching the transform these receivers and re-running it, rejected because under DECISION F275 D64 every overlay is a diff against the transform's fixed output, and these sites are few enough to name.

CHOSEN, SECOND: A JOB DOUBLE SPELLS THE UNIFIED RECORD. The 37 assignments set `job_id` and `job_title`, and the reads of such a double's `id` in `test_accept_recommendation` and `test_usage_incremented_on_process_start` read `job_id`, as DECISION F275 D69 ruled for the job doubles it renamed. ALTERNATIVE: leaving doubles that nothing fails on, rejected because a `MagicMock` answers any attribute, so a double that sets the wrong name fails only where a value is compared, and the next such comparison would be found one full run at a time.

CONSEQUENCE. The overlay edits no production code, so no mutation probe applies; per DECISION F275 D48 the full suite is the backstop. What the overlay fixes, and that it newly breaks nothing, is measured by the gates of round 100's block and recorded in the round 100 ledger entry by the round that books its verdict. `R-0809`, `R-0880` and `R-0883` stay open, and no finding is registered or resolved.

HOW TO REVERSE. Delete the round 100 overlay carriers under `.agent/authored/` and this paragraph block; the self-dogfood eligibility tests then look for a proposed task by its job's id again.
END DEC100

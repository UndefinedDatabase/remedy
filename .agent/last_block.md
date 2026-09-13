── STEP T003 — F275 — ROUND 95 ──
Goal: Commit the flip's sixth OVERLAY, applied after the first five to the flipped tree at
`844a7f21`: production reads of a job's classic `id` and `name` read `job_id` and `job_title`,
the job doubles tests hand that code spell the same, and a handler test that doubles the job
loader also doubles the resolver; measured by the full suite in fresh flipped trees.

Base commit: `6ec72f20`. The chain's base stays `844a7f21`, per DECISION F275 D64. Round type:
SPLIT. No path under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/` changes; the overlay
edits production code and tests, carried in a diff, and G6 red-proves three of its changes.

THE FRAME RULE, per item 37 of §3, stated as the property MEASURED over the final bytes: NO LINE
of this block is a run of a single repeated character, and every box-drawing rule inside the
STEP and SLICE header lines is exactly two characters long.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f275-r95.md`             the block, saved verbatim
C0b `.agent/last_block.md`                    mirrored FROM THE COMMITTED C0a BLOB
C1  `.agent/plan.md`                          slice PLAN95, a full replacement
C2  `.agent/live_review.md`                   slice RECORD95 appended, the round 94 verdict
C3  `.agent/prose_slips.md`                   slice SLIPS95 appended
C4  `.agent/authored/f275-r95-overlay-<k>.md` the overlay carriers of SPEC C, ONE COMMIT EACH
C5  `.agent/decisions.md`                     slice DEC95 appended
C6  `.agent/handoff.md`                       the handback

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3.

## Change — exactly these paths and no others

The Bundle's paths, `<k>` running from 1 over the carriers SPEC C produces.

## SPEC O — the edits, made in the EDIT worktree of constraint 8 on top of the fifth overlay

SPEC O edits these paths and no others. Under `apps/cli/commands/`: `decision.py`, `do_cmd.py`,
`failure_stats_cmd.py`, `job.py`, `memory.py`, `mission_cmd.py`, `project.py`, `readiness.py`,
`repo.py`, `review_cmd.py`, `status_cmd.py`. Under `packages/orchestration/`: `autorun.py`,
`event_replay.py`, `orchestrator_loop.py`, `project_registry.py`, `project_summary.py`,
`provider_patch_material.py`, `self_dogfood_execution.py`, `test_execution_service.py`,
`ui_server.py`. Under `tests/`: `cli/test_change_proof_cli.py`, `cli/test_context_inspect_cli.py`,
`cli/test_project_summary_cli.py`, `cli/test_review_cmd.py`, `orchestration/test_handoff.py`,
`orchestration/test_orchestrator_loop.py`, `orchestration/test_project_summary.py`,
`test_cli_execution_loop_closure.py`, `test_project_registry.py`,
`ui_server/test_budget_tick_envelope.py`, `ui_server/test_event_seq.py`,
`ui_server/test_sse_stream.py`. No test is added or deleted, and an assertion changes only in an
attribute name O2 orders.
O1 THE CLASSIC READS. Under `packages/` and `apps/`, outside `packages/orchestration/storage.py`,
every attribute read in `ast` Load context named `id` or `name` whose value is the bare name
`job`, `j` or `plan` becomes the same read of `job_id` or `job_title`; nothing else on its line
changes. The reviewer's count 79.
O2 THE JOB DOUBLES spell the unified record. In `test_project_summary.py` the `_FakeJob`
dataclass field `id` is `job_id`, its `__post_init__` tests and sets `self.job_id`, and every
`.id` read off `job`, `j`, `j1`, `j2` or `j3` reads `.job_id`; `_FakeProject` is unchanged. The
class attribute `id` of `_FakeJob` in `test_event_seq.py`, of the nested `_Job` in
`test_budget_tick_envelope.py` and of both `_Job` classes in `test_sse_stream.py` is `job_id`,
and every `_Job.id` read in `test_sse_stream.py` reads `_Job.job_id`. In `test_review_cmd.py`
each `SimpleNamespace(id=uuid4())` is `SimpleNamespace(job_id=uuid4())` and `job_stub.id` reads
`job_stub.job_id`. In `test_project_summary_cli.py` `_make_job` sets `job.job_id`, and every `.id`
read off `job`, `j1` or `j2` reads `.job_id`; `proj.id` is unchanged. `_FakeJob.__init__` in
`test_project_registry.py` sets `self.job_id = UUID(job_id)` and `self.job_title`;
`_FakeJob.__init__` in `test_orchestrator_loop.py` sets `self.job_id = job_id`, and
`test_the_dispatched_job_is_executed_in_the_same_iteration` asserts on `str(seen[0].job_id)`;
`_LoopJob.__init__` in `test_handoff.py` sets `self.job_id = job_id`.
O3 THE RESOLVER DOUBLES. In `test_change_proof_cli.py`, `test_context_inspect_cli.py` and
`test_cli_execution_loop_closure.py`, every `with` statement whose FIRST context manager is a
`patch` of a job loader with `return_value=job` gains, as its SECOND context manager,
`patch(<resolver>, side_effect=lambda raw: raw)`: `<resolver>` is
`"apps.cli.commands.change.resolve_job_id"` beside `"apps.cli.commands.change.require_job_plan"`,
`"apps.cli.commands.file.lookup_job_id"` beside `"apps.cli.commands.file.require_job_plan"`,
`"apps.cli.commands.context.lookup_job_id"` beside `"apps.cli.commands.context.require_job_plan"`,
and beside `"packages.orchestration.pingpong_job.load_job_plan"` the `lookup_job_id` of the
module whose handler that `with` block calls, `apps.cli.commands.review_cmd` or
`apps.cli.commands.memory`. The reviewer's count 27.

## SPEC C — the carriers, at C4

The VERBATIM stdout of `git diff` in EDIT, against its index as constraint 8 stages it, is cut at
`diff --git` lines into consecutive parts in its own order, each part as many whole file diffs as
fit in 440 lines, a new part starting only when the next file diff would not fit. Part `<k>` is
`.agent/authored/f275-r95-overlay-<k>.md`: at most 40 lines of prose naming its base `844a7f21`,
that the flipped tree is built as G4 of `.agent/authored/f275-r95.md` orders, that the parts form
the SIXTH overlay and apply after `.agent/authored/f275-r94-overlay-2.md` in `<k>` order, and how
to apply each — extract the fence, `git apply --check`, then `git apply`; then exactly ONE fence,
a line of three backticks and `diff`, the part, and a line of three backticks; nothing after it
but one newline. Joined in `<k>` order, the fences equal the whole diff byte for byte.

## Constraints

1. NO SLICE IS EDITED. PLAN95, RECORD95, SLIPS95 and DEC95 land byte for byte; a discrepancy
   inside one is DECLARED, never repaired.
2. SPEC O and SPEC C are the worker's OWN work. The reviewer's scratch `.remedy-wt/r90/` through
   `.remedy-wt/r95/` is not opened.
3. READ `.agent/STOP` before C0a and before C6, with real exit codes. If it appears, finish the
   commit in hand, write the handoff and end.
4. Every commit stages EXACTLY ONE path and stays under 500 insertions.
5. No `.py` file under `.agent/`; scratch under `.remedy-wt/r95w/`, uncommitted; every scratch
   output path absolute.
6. No landed record is rewritten: the `.agent/live_review.md`, `.agent/prose_slips.md` and
   `.agent/decisions.md` commits are APPENDS with a ZERO deletion column.
7. No `gh`, no `remedy`, no pull request, no branch created or deleted, no merge, NEVER a
   force-push, no history rewrite.
8. THREE worktrees, each `git worktree add --detach` at `844a7f21` under `.remedy-wt/r95w/`:
   EDIT, CONTROL and OVERLAY. In each: the transform as G4 orders, `git add -A`, then for each of
   `.agent/authored/f275-r90-overlay.md`, `.agent/authored/f275-r91-overlay.md`,
   `.agent/authored/f275-r92-overlay-1.md` through `-4.md`, `.agent/authored/f275-r93-overlay-1.md`
   and `-2.md` and `.agent/authored/f275-r94-overlay-1.md` and `-2.md`, overlay by overlay in that
   order, the fences of the COMMITTED carriers applied with `git apply --check` then `git apply`,
   and `git add -A` once after each overlay's parts. Only EDIT receives SPEC O, and any test may
   run there while it is made; before the diff is taken its `git diff --name-only` lists exactly
   SPEC O's paths. Only OVERLAY receives the C4 carriers. All three are REMOVED AND PRUNED before
   C5, without `--force`. The generator's trees are plain directories.
9. THE BLOCK'S OWN SIZE, measured on its final bytes: 299 lines TOTAL and 225 lines of
   PROSE, against the caps of 490 and 400.
10. GATE ORDER. G4's setup — the generator, the three worktrees, the chain — runs after C3 and
    before the first C4 commit, because the carriers are cut from EDIT; G4's readings, G5 and G6
    are taken after the last C4 commit and strictly before C5, per item 31 of §3. DEC95's
    measured figures, 79 and 54, are G4(b)'s CONTROL readings, and its nine and three count the
    files O2 and O3 name; DEC95 quotes no G5 or G6 reading. G1, G2, G3, G7 and G8 run at C5. No
    gate runs after C6; C6's own numbers are the reviewer's.
11. A RED G5 IS A STOP. Each node G5 finds bad only in OVERLAY is re-run by its node id alone in
    OVERLAY three times with G5's environment; unless every re-run passes, the worker commits
    nothing further after C4 except the handback, which lists every such node with its last
    `E   ` line. A node whose three re-runs all pass is reported FLAKY with the three tallies.

## Done when — the gates, each run for real and its exit code recorded

G1 TRANSPORT, BUDGET, SLICES. `.agent/authored/f275-r95.md` at C0a against the block as received,
by `cmp`; `.agent/last_block.md` at C0b byte-identical to the COMMITTED C0a blob. Extract the
slices by their markers, report how many were FOUND, check each against its BEGIN-marker
sha256, and re-measure TOTAL and PROSE against constraint 9.

G2 THE PLAN. `.agent/plan.md` at C1 byte-identical to PLAN95 from the COMMITTED C0a blob; at
most 50 lines; one `## Goal` and one `## Next Steps`.

G3 THE RECORD. For the appends at C2 into `.agent/live_review.md` and at C5 into
`.agent/decisions.md`, FULL FORENSICS: the pre-commit blob read with `git show` at the commit's
PARENT, its length printed — 1145506 and 1294405 — READER A with the arithmetic printed; READER B
over the file's LAST N blank-line units against the slice's N paragraphs IN ORDER, N counted by
the script; a letter flipped in the FIRST appended paragraph REJECTED by both readers; deletion
column 0. `.agent/prose_slips.md` at C3 equals its 302371-byte pre-commit blob followed by
exactly SLIPS95. Derive the ledger's `Gate:` header pattern from the file, report how many heads
it matches, and that RECORD95's header matches it and duplicates none.

G4 THE TREES, THE CHAIN AND THE CARRIERS, set up and read per constraint 10. The generator trees
and run exactly as G4 of `.agent/authored/f275-r90.md` orders, the pinned digests checked first,
with the readings that block states; the transform in each worktree reading 2183 resolving and 0
not, 264 files, 6097 rewrites and 0 broken; every earlier overlay applying with exit 0 in each.
Then: (a) the fences extracted from the COMMITTED C4 blobs: report the part count and each part's
line count, each at most 440; joined in `<k>` order they equal EDIT's diff; in OVERLAY each
applies with `git apply --check` and `git apply` exit 0, in order; `git diff --name-only` there,
against the index constraint 8 staged, lists exactly SPEC O's paths by name, each byte-identical
to EDIT's; report MISSING and EXTRA. (b) With `ast`, in CONTROL and in OVERLAY, names matched
EXACTLY: O1's reads, counted over `packages/` and `apps/` outside
`packages/orchestration/storage.py` as O1 defines them, 79 and 0. O2's spellings, counted over
O2's files as the sum of: assignment and annotated-assignment targets named `id` or `name`, and
`self.id` or `self.name` targets, inside classes named `_FakeJob`, `_Job` or `_LoopJob`;
attribute nodes named `id` off the bare names `job`, `j`, `j1`, `j2`, `j3`, `job_stub` or `_Job`;
and keywords `id` of calls of the bare name `SimpleNamespace` — 54 and 0. Calls of the bare name
`patch` whose first argument is a string constant among O3's resolvers, over O3's files, 0 and
27. `def test_` counts per changed test file equal in both trees. (c) `ruff check
--output-format concise`, run from inside each of CONTROL and OVERLAY over SPEC O's paths, rows
compared as a MULTISET of `<path>: <code> <message>` with line and column DROPPED: added 0 and
removed 0. The reviewer read 23 rows in each; the exit is 1 in BOTH trees and is reported,
never ordered.

G5 THE FULL SUITE IN FRESH FLIPPED TREES, per constraint 10, CONTROL first and OVERLAY second,
serially. Each is its worktree's FIRST pytest run of any kind, `apps/ui/node_modules` and
`apps/ui/dist` reported absent before it. `cwd` the worktree; `PYTHONPATH`, `REMEDY_PROJECT` and
`REMEDY_DATA_DIR` removed; `PYTHONDONTWRITEBYTECODE=1`;
`packages.orchestration.pingpong_job.__file__` printed and inside the worktree;
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`. A bad node is the
text after `FAILED ` or `ERROR ` up to the first ` - ` or the line's end. The reviewer measured
CONTROL `225 failed, 18186 passed, 29 skipped, 1 warning, 31 errors`, 256 bad nodes, and its own
dry run of SPEC O `150 failed, 18261 passed, 29 skipped, 1 warning, 31 errors`, 181. REPORT
OVERLAY's tally and bad-node count. Bad only in OVERLAY: MUST be 0, per constraint 11. REPORT
the fixed nodes' count per test file.

G6 THE PROBES, per constraint 10, in OVERLAY after G5; `__pycache__` purged before each run;
G5's environment; flags `-q -p no:randomly -p no:cacheprovider --tb=short -rfE`. For each
mutation, the bytes it replaces counted as 1 first, in the file or in the named test's span,
then the selection run UNMUTATED and MUTATED, each tally and exit code reported with the node
ids bad only under the mutation, then the file restored and its bytes confirmed. M1 in
`packages/orchestration/project_registry.py`, the bytes `{j.job_title[:40]}")` become
`{j.name[:40]}")`, over `tests/test_project_registry.py`:
`TestSummarizeProject::test_jobs_shown_with_state` MUST go bad. M2 in
`packages/orchestration/ui_server.py`, the two lines `        "job_id": str(job.job_id),` and
`        "cursor": str(len(events)),` become the same two with `job.id`, over
`tests/ui_server/test_event_seq.py`: every node of that file MUST go bad; the reviewer's dry run
read 7. M3 in `tests/cli/test_change_proof_cli.py`, the resolver `patch` O3 added to the `with`
statement of `test_handler_text_output` is removed and nothing else, over the node
`tests/cli/test_change_proof_cli.py::test_handler_text_output`, which MUST go bad.

G7 TREE, CANARY, LINT, PATH SET, OPEN SET, at C5. `git status --porcelain` prints `''`;
`git worktree list` one row; `git diff --name-only 6ec72f20 C5 -- packages apps tests docs
scripts` empty; the canary `python3 -B -m pytest tests/cli/test_golden_path.py -q` exit 0, 42;
`ruff check . --output-format concise` rows as a MULTISET at `6ec72f20`, read from a
`git archive` tree, and at C5, difference empty, 26 at `6ec72f20`. The changed-path set of
`6ec72f20`..C5 against the Bundle's paths MINUS `.agent/handoff.md`, MISSING and EXTRA by name.
The open set BY DISTINCT ID at `6ec72f20` and at C5: 88 at both, membership identical;
`R-0809`, `R-0880` and `R-0883` open.

G8 THE INSERTION CAP over `6ec72f20`..C5: one row per commit with insertions, deletions and
staged path count, and the number of commits reaching 500 insertions.

Handback: `.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 32 of feature F275 · round 95 · rounds so far 95`; the Commits table read from
`git show --numstat` and compared cell by cell against G8, C6's row carrying no numbers and
saying why; one Verification line per gate with its REAL exit code; External actions;
Authored-text proofs; Item-status; Deviations; `## Next` stating `Operator questions open: 1`.
NO SCOPE REPORT AND NO SESSION-LIMIT BANNER, by amendment amend0911-f275-to-scope.

── SLICE PLAN95 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN95 sha256=61d719b32abb3ff33754312d9e743f498deabf21b46578f92c815aa196c2550d
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

ROUND 95 ADDS THE FLIP'S SIXTH OVERLAY, on top of the first five, under DECISION F275 D64's
method. Production code reading `.id` or `.name` off a job it loaded reads the unified
record's `job_id` and `job_title`; the job doubles tests hand that code spell the same; and a
handler test that doubles the job loader also doubles the resolver the handler's module binds.
The diff is carried in consecutive carriers, so no path under `packages/`, `apps/` or `tests/`
moves; the round books the round 94 verdict and its two prose slips.

## Next Steps

1. MORE OVERLAYS, one residue group each, every one applied on top of those before it: the
   pydantic calls tests still make on a `JobPlan`, such as `model_dump_json`, and the `job show`
   handler that prints one; tests that give a record's `created_at` a `datetime`; classic
   spellings read off job records under other local names; the mission end-to-end fixture that
   never reaches its decision job; tests that still redirect the classic store's `_DATA_DIR`;
   and what is left of the classic runner under `job resume`, which still builds a classic job.
2. THE FLIP: the transform, then every overlay in round order, landed as a series of commits
   each under the 500-insertion cap inside one round, carrying DECISION F275 D48's obligations
   and registering the structured acceptance form DECISION F275 D22 leaves to it, unless the
   operator allows one more oversized commit.
3. Then the classic store, with the which-store branches and adapters the overlays leave
   unreached, then the closure sequence.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20
  sessions and 60 rounds without a replacement, so this feature closes only at full scope.
- THE FLIP IS NOT CLOSE: many test nodes still fail in the flipped tree.
- AN OVERLAY IS A DIFF AGAINST A FIXED TREE: it holds only while the production tree stays at
  `844a7f21`, and it depends on the generator and transform staying reproducible from round
  77's two scratch JSON files.
- ONE ROUTED LOAD IS REACHED BY NO TEST until `R-0883` is repaired.
- The open set is 88 by distinct id at this round's base, with `R-0809`, `R-0880` and `R-0883`
  open. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END PLAN95

── SLICE RECORD95 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD95 sha256=26bba3f083f2c40b4169852573eaf25bdd23054a8c7a6f4e3c69367ed3d65767

Gate: F275 R94 — the F275 round 94 entry. VERDICT PASS. Written by the planner and reviewer of session 32 after reading the committed range `38b0a25a`..`6ec72f20` and RE-DERIVING EVERY GATE AND EVERY PROBE INDEPENDENTLY; the worker's report and its transcripts were evidence for no line below. It is booked here by the FIRST SUBSTANTIVE COMMIT of round 95 that writes the record, per operator amendment amend0827-process-diet rule 1. The round moved no path under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/`; its code is the diff carried in `.agent/authored/f275-r94-overlay-1.md` and `-2.md`.

WHAT THE TRANSPORT PROOF COVERS, per item 37 of §3. The committed `.agent/authored/f275-r94.md` blob was identical to the reviewer's own original at 28291 bytes, `.agent/last_block.md` equalled it from its own commit through `6ec72f20`, and all four slices matched their BEGIN-marker digests; `.agent/plan.md` equalled PLAN94. The three appends were exact under reader A — 1142023 plus 3483 into the review record, 301820 plus 551 into the prose slips and 1290732 plus 3673 into the decisions — with reader B holding at N counted from each slice as 4, 1 and 7, and a letter flipped in each FIRST appended paragraph rejected by both readers. Every commit staged one path, the largest the first carrier at 391 insertions, and the two fences read 351 and 176 lines, which is what cutting the joined diff greedily at 440 lines gives.

THE OVERLAY HOLDS UNDER THE REVIEWER'S OWN RE-RUN. The reviewer transformed a worktree at `844a7f21` from its own generator run, applied and staged the committed overlays of rounds 90 to 93, and applied the two committed round 94 fences: every `git apply --check` and `git apply` exited 0 and 15 paths changed, 11 of them production code. With `ast`, the `TaskEntry` constructions passing `acceptance_checks`, the `UUID` calls parsing a task id, the pydantic calls read off `TaskEntry`, the `model_copy` calls in `mission_state.py` and the fixtures setting the classic `_DATA_DIR` in `test_proposed_tasks.py` read 0, 0, 0, 0 and 0, against 2, 4, 1, 1 and 16 in a control tree of the chain before it. Compared as a multiset with line and column dropped, the `ruff` rows over the 15 files read 12 in each tree, none added. That worktree's first full run read 225 failed, 18186 passed, 29 skipped and 31 errors, 256 bad nodes, against 406 in the reviewer's fresh run of the chain before it: 150 fixed and none newly bad. In the same worktree, returning the empty default to `TaskEntry.task_id` made exactly the identity pin and 14 nodes of `tests/orchestration/test_dag_schedule.py` bad; dropping the membership test from `awaiting_decision_task_ids` made exactly `test_a_malformed_task_id_blocks_nothing` bad; and reading the planned id from the task's own id first made `test_planned_id_and_task_uuid_prefix_reach_the_same_task` and two more nodes of `tests/cli/test_job_context_cmd.py` bad. In the primary checkout at `6ec72f20` the canary read 42 and `ruff check .` read 26 rows, as at `38b0a25a`; the open set stayed 88 with identical membership, `R-0809`, `R-0880` and `R-0883` open.

WHAT THE WORKER NAMED AND THE NEXT OVERLAY TAKES. Five more guidance lines of `execute_test_run` read `job.id` off the plan it loaded, beside the one SPEC O ordered changed. The carrier holds them, not a path under `packages/`, so they are not a finding: round 95's overlay rewrites every such read.
END RECORD95

── SLICE SLIPS95 ── target `.agent/prose_slips.md` ── APPEND ──
BEGIN SLIPS95 sha256=1a6d68bc29631705b2d805bb42c0055641b1e937a39de14be9af28baf343ebc0

2026-09-13 · F275 R94 · SPEC O6 of the round 94 block said the body of `_task_planned_id` "begins with exactly" two ordered lines, while a function's body begins with its docstring, which the same item ordered kept; the worker read the words as the first statements after the docstring and declared it. THE RULE THAT FOLLOWS: an order placing a line at the start of a function body names what precedes it or says "the first statement".

2026-09-13 · F275 R94 · SPEC O7 of the round 94 block ordered one `job.id` read in `execute_test_run` rewritten, the one the residue showed, while five more reads of the same attribute off the same local sat in that function; the worker changed the one and named the five. THE RULE THAT FOLLOWS: an attribute fix ordered at one site is first swept over every read of that attribute off the same binding in the enclosing function.
END SLIPS95

── SLICE DEC95 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC95 sha256=4581628f3a694e2e4dc951dcb7d82c3823f04b7f68bef027b8314b989b69a3aa

## DECISION F275 D69 (2026-09-13, F275 round 95) — the sixth overlay: a job record's classic spellings the transform could not reach are read as the unified record's, the job doubles tests hand that code spell the same, and a handler test doubles the resolver beside the loader

CONTEXT. The transform rewrote the sites its owner check could decide and refused the rest, which DECISION F275 D45 ruled acceptable. In the flipped tree at `844a7f21`, with five overlays applied, 79 attribute reads under `packages/` and `apps/` outside the classic store's own module still read `.id` or `.name` off a local named `job`, `j` or `plan`; `JobPlan` has neither attribute, so each such read raises whenever the local holds one. Nine test files hand such code job doubles that spell the classic record, 54 spellings of `id` or `name` among them. And handler tests in three files double the job loader but not the resolver the handler calls first, which now reads the disk for a sixteen-hex id where a full UUID used to return unread.

CHOSEN, FIRST: THE READ SPELLS THE UNIFIED RECORD. Every such read becomes `job_id` or `job_title`. ALTERNATIVES: `id` and `name` properties on `JobPlan`, rejected as the compatibility reader AGENTS.md Scope Control forbids, on a record whose classic twin is deleted after the flip; widening the owner check, rejected because DECISION F275 D47 recorded that route ended.

CHOSEN, SECOND: A DOUBLE FOLLOWS THE RECORD, as DECISION F275 D67 ruled for doubles installed by name. The job doubles carry `job_id` and `job_title` where they carried `id` and `name`, and the tests read them back under those names.

CHOSEN, THIRD: A HANDLER TEST DOUBLES THE RESOLVER BESIDE THE LOADER. Each such test patches the resolver name the handler's module binds with an identity, so the test still reaches the handler with the id it built. ALTERNATIVES: letting a full sixteen-hex id pass the resolver unread, as a full UUID does, rejected because `tests/test_data_paths.py` pins that a sixteen-hex directory without a record does not resolve; saving real records, rejected because these tests already double every store read the handler makes.

CONSEQUENCE. The reads are chosen by the name of the local that holds the record, so a classic read off any other name is untouched and is a later overlay's subject; and a changed read that the classic runner under `job resume` hands a classic job would now raise where it read before, which that runner's remains, a later overlay's subject, decide. What the overlay fixes, and that it newly breaks nothing, is measured by the gates of round 95's block and recorded in the round 95 ledger entry by the round that books its verdict. `R-0809`, `R-0880` and `R-0883` stay open, and no finding is registered or resolved.

HOW TO REVERSE. Delete the round 95 overlay carriers under `.agent/authored/` and this paragraph block; those reads then raise in the flipped tree again.
END DEC95

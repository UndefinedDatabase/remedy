── STEP T003 — F275 — ROUND 94 ──
Goal: Commit the flip's fifth OVERLAY, applied after the first four to the flipped tree at
`844a7f21`: a task record built without an id mints one, a task id is a string wherever it is
read, the classic acceptance list becomes acceptance text, and no pydantic call is made on a
task record; measured by the full suite in fresh flipped trees.

Base commit: `38b0a25a`. The chain's base stays `844a7f21`, per DECISION F275 D64. Round type:
SPLIT. No path under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/` changes; the overlay
edits production code and tests, carried in a diff, and G6 red-proves three of its changes.

THE FRAME RULE, per item 37 of §3, stated as the property MEASURED over the final bytes: NO LINE
of this block is a run of a single repeated character, and every box-drawing rule inside the
STEP and SLICE header lines is exactly two characters long.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f275-r94.md`             the block, saved verbatim
C0b `.agent/last_block.md`                    mirrored FROM THE COMMITTED C0a BLOB
C1  `.agent/plan.md`                          slice PLAN94, a full replacement
C2  `.agent/live_review.md`                   slice RECORD94 appended, the round 93 verdict
C3  `.agent/prose_slips.md`                   slice SLIPS94 appended
C4  `.agent/authored/f275-r94-overlay-<k>.md` the overlay carriers of SPEC C, ONE COMMIT EACH
C5  `.agent/decisions.md`                     slice DEC94 appended
C6  `.agent/handoff.md`                       the handback

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3.

## Change — exactly these paths and no others

The Bundle's paths, `<k>` running from 1 over the carriers SPEC C produces.

## SPEC O — the edits, made in the EDIT worktree of constraint 8 on top of the fourth overlay

SPEC O edits these paths and no others: `apps/cli/commands/context.py`,
`apps/cli/commands/job_context_cmd.py`, `packages/orchestration/data_paths.py`,
`packages/orchestration/decision_inbox.py`, `packages/orchestration/escalation.py`,
`packages/orchestration/flight_plan.py`, `packages/orchestration/mission_state.py`,
`packages/orchestration/pingpong_job.py`, `packages/orchestration/proposed_tasks.py`,
`packages/orchestration/test_execution_service.py`,
`packages/orchestration/test_failure_artifact.py`, `tests/orchestration/test_flight_plan.py`,
`tests/orchestration/test_mint_call_sites.py`, `tests/orchestration/test_proposed_tasks.py`,
`tests/test_data_paths.py`. A line in a triple backtick span below is ordered byte for byte.
O1 THE MINTER. In `data_paths.py`, after `mint_episode_id`, `def mint_task_id() -> str:` with a
one-line docstring naming the id of a TASK no job file numbered, returning `uuid4().hex[:16]`.
The module docstring's Public API list gains a `mint_task_id() -> str` line after
`mint_episode_id`'s; the DECISION F260 D2 comment above the minters says the same sixteen hex
characters name five kinds of thing, and calls `safe_points.new_request_id` the fifth kind.
O2 THE DEFAULT. In `pingpong_job.py` the module-level import from `data_paths` also binds
`mint_task_id`, and `TaskEntry`'s field is ```    task_id: str = field(default_factory=mint_task_id)```
under a comment saying a job file's tasks are numbered `T001`, `T002` by parse order and a task
built by code mints its id, as the classic `Task` did.
O3 ACCEPTANCE TEXT. `map_flight_plan_to_tasks` in `flight_plan.py` passes
`acceptance="\n".join(pt.acceptance)` in place of `acceptance_checks=`; `build_verify_first_task`
in `mission_state.py` passes its one sentence as `acceptance=`; `AcceptanceCheck` leaves both
imports. `test_three_tasks_in_order` in `test_flight_plan.py` asserts
`task.acceptance.splitlines() == [f"Thing {i + 1} done"]`.
O4 NO PYDANTIC CALL ON A TASK RECORD. `inject_verify_first` appends `replace(task, inputs=inputs)`,
the module already importing `replace`; `do_materialize` in `proposed_tasks.py` builds
`TaskEntry(task_id=task_dict["id"], title=task_dict["description"], inputs=task_dict["inputs"],
status=task_dict["status"])`.
O5 A TASK ID IS A STRING. `persist_failure_artifact` in `test_failure_artifact.py` passes
`task_id=failure.task_id or None`, and `UUID` leaves its import. In `escalation.py`,
`awaiting_decision_task_ids` returns `set[str]`: it binds
`known = {str(task.task_id) for task in getattr(job, "tasks", ()) or ()}`, and for each open
record binds `task_id = str(record.get("task_id") or "")` and adds it under exactly
```        if task_id and task_id in known:``` with a comment that an id naming no task of
this job blocks nothing. `_blocked_subtree_size` in `decision_inbox.py` seeds
`{str(payload["task_id"])}` when the payload is a dict with a truthy `task_id`, else the empty
set; `UUID` leaves the imports, and `build_decision_inbox`'s docstring says a task id that names
no task gives 0 blocked. In `context.py` the `UUID(task_id)` refusal and its import go; the
membership check stays.
O6 THE PLANNED ID. The body of `_task_planned_id` in `job_context_cmd.py` begins with exactly the
two lines ```    planned = _task_flight_inputs(task).get("planned_id")``` and
```    if planned:```, returns `str(planned)` there, and otherwise returns
`str(getattr(task, "task_id", "") or "")`; its docstring and comment say why the flight-plan
block wins.
O7 ONE ATTRIBUTE. `execute_test_run` in `test_execution_service.py` renders its `job show`
guidance from `job.job_id` where it reads `job.id`.
O8 THE PINS AND THE ROOT. In `test_mint_call_sites.py` the module docstring's first line names the
TASK kind, "THE TWO DATACLASS DEFAULTS" reads "THE THREE", and after the RUN pin
`test_task_entry_task_id_default_is_the_mint_function_itself` asserts
`pingpong_job.TaskEntry.__dataclass_fields__["task_id"].default_factory is data_paths.mint_task_id`.
In `tests/test_data_paths.py`, `TestMintIds._minters` also returns `mint_task_id`, and
`test_the_task_minter_is_a_fourth_distinct_function` asserts it is none of the other three. In
`test_proposed_tasks.py` each `monkeypatch.setattr("packages.orchestration.storage._DATA_DIR",
tmp_path / "jobs")` line becomes `monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))`.

## SPEC C — the carriers, at C4

The VERBATIM stdout of `git diff` in EDIT, against its index as constraint 8 stages it, is cut at
`diff --git` lines into consecutive parts in its own order, each part as many whole file diffs as
fit in 440 lines, a new part starting only when the next file diff would not fit. Part `<k>` is
`.agent/authored/f275-r94-overlay-<k>.md`: prose naming its base `844a7f21`, that the flipped
tree is built as G4 of `.agent/authored/f275-r94.md` orders, that the parts form the FIFTH
overlay and apply after `.agent/authored/f275-r93-overlay-2.md` in `<k>` order, and how to apply
each — extract the fence, `git apply --check`, then `git apply`; then exactly ONE fence, a line of
three backticks and `diff`, the part, and a line of three backticks; nothing after it but one
newline. Joined in `<k>` order, the fences equal the whole diff byte for byte.

## Constraints

1. NO SLICE IS EDITED. PLAN94, RECORD94, SLIPS94 and DEC94 land byte for byte; a discrepancy
   inside one is DECLARED, never repaired.
2. SPEC O and SPEC C are the worker's OWN work. The reviewer's scratch `.remedy-wt/r90/` through
   `.remedy-wt/r94/` is not opened.
3. READ `.agent/STOP` before C0a and before C6, with real exit codes. If it appears, finish the
   commit in hand, write the handoff and end.
4. Every commit stages EXACTLY ONE path and stays under 500 insertions.
5. No `.py` file under `.agent/`; scratch under `.remedy-wt/r94w/`, uncommitted; every scratch
   output path absolute.
6. No landed record is rewritten: the `.agent/live_review.md`, `.agent/prose_slips.md` and
   `.agent/decisions.md` commits are APPENDS with a ZERO deletion column.
7. No `gh`, no `remedy`, no pull request, no branch created or deleted, no merge, NEVER a
   force-push, no history rewrite.
8. THREE worktrees, each `git worktree add --detach` at `844a7f21` under `.remedy-wt/r94w/`:
   EDIT, CONTROL and OVERLAY. In each: the transform as G4 orders, `git add -A`, then for each of
   `.agent/authored/f275-r90-overlay.md`, `.agent/authored/f275-r91-overlay.md`,
   `.agent/authored/f275-r92-overlay-1.md` through `-4.md` and
   `.agent/authored/f275-r93-overlay-1.md` and `-2.md`, overlay by overlay in that order, the
   fences of the COMMITTED carriers applied with `git apply --check` then `git apply`, and
   `git add -A` after each overlay. Only EDIT receives SPEC O, and any test may run there while
   it is made; before the diff is taken its `git diff --name-only` lists exactly SPEC O's paths.
   Only OVERLAY receives the C4 carriers. All three are REMOVED AND PRUNED before C5, without
   `--force`. The generator's trees are plain directories.
9. THE BLOCK'S OWN SIZE, measured on its final bytes: 315 lines TOTAL and 242 lines of
   PROSE, against the caps of 490 and 400.
10. GATE ORDER. G4's setup — the generator, the three worktrees, the chain — runs after C3 and
    before the first C4 commit, because the carriers are cut from EDIT; G4's readings, G5 and G6
    are taken after the last C4 commit and strictly before C5, per item 31 of §3. DEC94's
    measured figures — four, two, one, one and 16 — are G4(b)'s CONTROL readings; DEC94 quotes
    no G5 or G6 reading. G1, G2, G3, G7 and G8 run at C5. No gate runs after C6; C6's own
    numbers are the reviewer's.
11. A RED G5 IS A STOP. Each node G5 finds bad only in OVERLAY is re-run by its node id alone in
    OVERLAY three times with G5's environment; unless every re-run passes, the worker commits
    nothing further after C4 except the handback, which lists every such node with its last
    `E   ` line. A node whose three re-runs all pass is reported FLAKY with the three tallies.

## Done when — the gates, each run for real and its exit code recorded

G1 TRANSPORT, BUDGET, SLICES. `.agent/authored/f275-r94.md` at C0a against the block as received,
by `cmp`; `.agent/last_block.md` at C0b byte-identical to the COMMITTED C0a blob. Extract the
slices by their markers, report how many were FOUND, check each against its BEGIN-marker
sha256, and re-measure TOTAL and PROSE against constraint 9.

G2 THE PLAN. `.agent/plan.md` at C1 byte-identical to PLAN94 from the COMMITTED C0a blob; at
most 50 lines; one `## Goal` and one `## Next Steps`.

G3 THE RECORD. For the appends at C2 into `.agent/live_review.md` and at C5 into
`.agent/decisions.md`, FULL FORENSICS: the pre-commit blob read with `git show` at the commit's
PARENT, its length printed — 1142023 and 1290732 — READER A with the arithmetic printed; READER B
over the file's LAST N blank-line units against the slice's N paragraphs IN ORDER, N counted by
the script; a letter flipped in the FIRST appended paragraph REJECTED by both readers; deletion
column 0. `.agent/prose_slips.md` at C3 equals its 301820-byte pre-commit blob followed by
exactly SLIPS94. Derive the ledger's `Gate:` header pattern from the file, report how many heads
it matches, and that RECORD94's header matches it and duplicates none.

G4 THE TREES, THE CHAIN AND THE CARRIERS, set up and read per constraint 10. The generator trees
and run exactly as G4 of `.agent/authored/f275-r90.md` orders, the pinned digests checked first,
with the readings that block states; the transform in each worktree reading 2183 resolving and 0
not, 264 files, 6097 rewrites and 0 broken; every earlier overlay applying with exit 0 in each.
Then: (a) the fences extracted from the COMMITTED C4 blobs: report the part count and each part's
line count, each at most 440; joined in `<k>` order they equal EDIT's diff; in OVERLAY each
applies with `git apply --check` and `git apply` exit 0, in order; `git diff --name-only` there,
against the index constraint 8 staged, lists exactly SPEC O's paths by name, each
byte-identical to EDIT's; report MISSING and EXTRA. (b) With `ast`, in CONTROL and in OVERLAY,
matching NAMES EXACTLY except where containment is said: calls of the bare name `TaskEntry`
passing a keyword `acceptance_checks`, under `packages/`, `apps/` and `tests/`, 2 and 0; calls
of the bare name `UUID` with one argument whose source text CONTAINS `task_id`, under
`packages/` and `apps/`, 4 and 0; calls of an attribute whose name starts `model_` read off the
bare name `TaskEntry`, under all three, 1 and 0; calls of an attribute named `model_copy` in
`packages/orchestration/mission_state.py`, 1 and 0; calls of an attribute named `setattr` in
`tests/orchestration/test_proposed_tasks.py` whose first argument is the string constant
`packages.orchestration.storage._DATA_DIR`, 16 and 0. `def test_` counts per changed test file,
by `ast`: OVERLAY equals CONTROL, plus one in each of `tests/orchestration/test_mint_call_sites.py`
and `tests/test_data_paths.py`. (c) `ruff check --output-format concise`, run from inside each of
CONTROL and OVERLAY over SPEC O's paths, rows compared as a MULTISET of
`<path>: <code> <message>` with line and column DROPPED: added 0 and removed 0. The reviewer read
12 rows in each; the exit is 1 in BOTH trees and is reported, never ordered.

G5 THE FULL SUITE IN FRESH FLIPPED TREES, per constraint 10, CONTROL first and OVERLAY second,
serially. Each is its worktree's FIRST pytest run of any kind, `apps/ui/node_modules` and
`apps/ui/dist` reported absent before it. `cwd` the worktree; `PYTHONPATH`, `REMEDY_PROJECT` and
`REMEDY_DATA_DIR` removed; `PYTHONDONTWRITEBYTECODE=1`;
`packages.orchestration.pingpong_job.__file__` printed and inside the worktree;
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`. A bad node is the
text after `FAILED ` or `ERROR ` up to the first ` - ` or the line's end. The reviewer measured
CONTROL `375 failed, 18034 passed, 29 skipped, 1 warning, 31 errors`, 406 bad nodes, and its own
dry run of SPEC O `225 failed, 18186 passed, 29 skipped, 1 warning, 31 errors`, 256. REPORT
OVERLAY's tally and bad-node count. Bad only in OVERLAY: MUST be 0, per constraint 11. REPORT
the fixed nodes' count per test file.

G6 THE PROBES, per constraint 10, in OVERLAY after G5; `__pycache__` purged before each run;
G5's environment; flags `-q -p no:randomly -p no:cacheprovider --tb=short -rfE`. For each
mutation, the bytes it replaces counted in the file as 1 first, then the selection run
UNMUTATED and MUTATED, each tally and exit code reported with the node ids bad only under the
mutation, then the file restored and its bytes confirmed. M1 in
`packages/orchestration/pingpong_job.py`, O2's ordered field line becomes
`    task_id: str = ""`, over `tests/orchestration/test_mint_call_sites.py` and
`tests/orchestration/test_dag_schedule.py`: the pin MUST go bad; the reviewer's dry run read 15,
the pin and 14 nodes of `test_dag_schedule.py`. M2 in `packages/orchestration/escalation.py`,
O5's ordered test becomes `        if task_id:`, over `tests/orchestration/test_escalation.py`:
`TestAwaitingBranch::test_a_malformed_task_id_blocks_nothing` MUST go bad. M3 in
`apps/cli/commands/job_context_cmd.py`, O6's first ordered line becomes
`    planned = getattr(task, "task_id", "")`, over `tests/cli/test_job_context_cmd.py`, whose
unmutated run the reviewer read at 3 failed: `test_planned_id_and_task_uuid_prefix_reach_the_same_task`
MUST go bad; the reviewer's dry run read two more, `test_json_view_carries_the_same_paths_as_the_text_view`
and `test_empty_files_hint_is_rendered_rather_than_treated_as_an_error`.

G7 TREE, CANARY, LINT, PATH SET, OPEN SET, at C5. `git status --porcelain` prints `''`;
`git worktree list` one row; `git diff --name-only 38b0a25a C5 -- packages apps tests docs
scripts` empty; the canary `python3 -B -m pytest tests/cli/test_golden_path.py -q` exit 0, 42;
`ruff check . --output-format concise` rows as a MULTISET at `38b0a25a`, read from a
`git archive` tree, and at C5, difference empty, 26 at `38b0a25a`. The changed-path set of
`38b0a25a`..C5 against the Bundle's paths MINUS `.agent/handoff.md`, MISSING and EXTRA by name.
The open set BY DISTINCT ID at `38b0a25a` and at C5: 88 at both, membership identical;
`R-0809`, `R-0880` and `R-0883` open.

G8 THE INSERTION CAP over `38b0a25a`..C5: one row per commit with insertions, deletions and
staged path count, and the number of commits reaching 500 insertions.

Handback: `.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 32 of feature F275 · round 94 · rounds so far 94`; the Commits table read from
`git show --numstat` and compared cell by cell against G8, C6's row carrying no numbers and
saying why; one Verification line per gate with its REAL exit code; External actions;
Authored-text proofs; Item-status; Deviations; `## Next` stating `Operator questions open: 1`.
NO SCOPE REPORT AND NO SESSION-LIMIT BANNER, by amendment amend0911-f275-to-scope.

── SLICE PLAN94 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN94 sha256=3559a4f07543a9a91db0a99ee809eace696714f0c93912535bed21efc0d9ff4c
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

ROUND 94 ADDS THE FLIP'S FIFTH OVERLAY, on top of the first four, under DECISION F275 D64's
method. A task record built without an id mints one, as the classic `Task` did; a task id is
read as a string wherever code parsed it as a `UUID`; the classic `acceptance_checks` list
becomes acceptance text; no pydantic call is made on a task record; and the proposed-task
tests point the data root at their own directory. The diff is carried in consecutive
carriers, so no path under `packages/`, `apps/` or `tests/` moves; the round books the round
93 verdict and its slip.

## Next Steps

1. MORE OVERLAYS, one residue group each, every one applied on top of those before it: tests
   that still redirect the classic store's `_DATA_DIR`; handlers resolving a minted job id no
   store holds; the pydantic calls made on a `JobPlan`, such as `model_dump_json`; the mission
   end-to-end fixture that never reaches its decision job; what is left of the classic runner
   under `job resume`; and duck-typed test doubles, such as the `_FakeJob` behind a ruled site
   in `packages/orchestration/project_registry.py`.
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
END PLAN94

── SLICE RECORD94 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD94 sha256=9884df7c82c0df583a735dd556d635fea2e559f876945b3a1794a0dfd2d66c66

Gate: F275 R93 — the F275 round 93 entry. VERDICT PASS. Written by the planner and reviewer of session 31 after reading the committed range `dbab6b13`..`2738ac31` and RE-DERIVING EVERY GATE AND EVERY PROBE INDEPENDENTLY; the worker's report and its transcripts were evidence for no line below. It was carried in `.agent/handoff.md` at `38b0a25a` and is booked here by the FIRST SUBSTANTIVE COMMIT of round 94 that writes the record, per operator amendment amend0827-process-diet rule 1. The round moved no path under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/`; its code is the test-only diff carried in `.agent/authored/f275-r93-overlay-1.md` and `-2.md`.

WHAT THE TRANSPORT PROOF COVERS, per item 37 of §3. The committed `.agent/authored/f275-r93.md` blob was identical to the reviewer's own original at 23923 bytes, `.agent/last_block.md` equalled it from its own commit through `2738ac31`, and all four slices matched their BEGIN-marker digests; `.agent/plan.md` equalled PLAN93. The three appends were exact under reader A — 1138457 plus 3566 into the review record, 300925 plus 895 into the prose slips and 1288099 plus 2633 into the decisions — with reader B holding at N counted from each slice as 4, 2 and 6, and a letter flipped in each FIRST appended paragraph rejected by both readers. Every commit staged one path, the largest the first carrier at 426 insertions, and the two fences read 390 and 300 lines, which is what cutting the joined diff greedily at 440 lines gives.

THE OVERLAY HOLDS UNDER THE REVIEWER'S OWN RE-RUN. The reviewer transformed a worktree at `844a7f21` from its own generator run, applied and staged the committed first and second overlays and the four round 92 parts, and applied the two committed round 93 fences: every `git apply --check` and `git apply` exited 0 and 13 paths changed, all under `tests/`. With `ast` over `tests/`, the dotted targets naming a classic store function, the `setattr` calls naming one and the unified functions read off the `storage` module read 0, 0 and 0, against 53, 3 and 9 in the reviewer's own copy of the chain before it. Compared as a multiset with line and column dropped, the `ruff` rows over the 13 files read 9 before and 9 after, none added. That worktree's first full run read 375 failed, 18034 passed, 29 skipped and 31 errors, 406 bad nodes, against 449 in the reviewer's fresh run of the chain before it: 43 fixed and none newly bad. In the same worktree `tests/orchestration/test_job_plan_state_reads.py` read 4 passed; narrowing its finder to the first loader made exactly the planted case parametrized with `require_job_plan` bad, and pointing `test_handler_path_traversal_rejected` back at `apps.cli.commands.change.load_job` made that node bad. In the primary checkout at `2738ac31` the canary read 42 and `ruff check .` read 26 rows, a multiset equal to that of `844a7f21`, whose production tree it shares; the open set stayed 88 with identical membership, `R-0809`, `R-0880` and `R-0883` open.

ONE GATE OF THE BLOCK WAS WRONG, AND THE WORKER DECLARED IT. G4(c) ordered `ruff check --select F401,F811,F821` over the changed paths to exit 0 in the overlay's tree, and it exits 1 on three `F821 Undefined name mint_job_id` rows in `tests/test_data_paths.py` that the transform leaves there; the reviewer measured the same three rows before the overlay and after it. The property the gate was written for — no such row added — holds, and nothing wrong reached any path.
END RECORD94

── SLICE SLIPS94 ── target `.agent/prose_slips.md` ── APPEND ──
BEGIN SLIPS94 sha256=80503360af56105ca44d5cd4de10ee74b99aa7e552e25d977139a2f4c19168e7

2026-09-13 · F275 R93 · G4(c) of the round 93 block ordered `ruff check --select F401,F811,F821` over the changed test files to exit 0 in the overlay's tree without running it in the tree before the overlay, where three `F821` rows the transform leaves in `tests/test_data_paths.py` already make it exit 1; the worker declared the red and the rows stand identically in both trees. THE RULE THAT FOLLOWS: an exit code ordered for a flipped tree is first read in the control tree, and where the control is already red the gate compares rows instead.
END SLIPS94

── SLICE DEC94 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC94 sha256=5ed6ed9db09a2d10c99a88dc641b1935d37393553b42ffcebb5302ac27b49d90

## DECISION F275 D68 (2026-09-13, F275 round 94) — the fifth overlay: a task record built without an id mints one, a task id is a string wherever it is read, and the classic acceptance list becomes the unified record's acceptance text

CONTEXT. The classic `Task` minted a `uuid4` for its `id` whenever a caller gave none, while `TaskEntry.task_id` defaults to the empty string. In the flipped tree at `844a7f21`, with four overlays applied, every task built by code without an id therefore shares one empty id, so the task graph cannot tell those tasks apart. Four `UUID(...)` calls under `packages/` and `apps/` still parse a task id, which the unified record spells `T001` or as sixteen hex characters; two `TaskEntry` constructions still pass the classic `acceptance_checks` keyword, which the dataclass does not declare; one production call is `TaskEntry.model_validate` and `inject_verify_first` calls `model_copy` on a task record, neither of which a dataclass has; and 16 `monkeypatch.setattr` calls in `tests/orchestration/test_proposed_tasks.py` redirect the classic store's `_DATA_DIR` while the flipped code reads the data root.

CHOSEN, FIRST: A TASK BUILT WITHOUT AN ID MINTS ONE. `data_paths.mint_task_id` joins the three minters DECISION F260 D2 ruled, one function per kind of id, and it is `TaskEntry.task_id`'s default factory, pinned by object identity beside the job and run defaults. A job file's tasks keep their `T001` numbering, because the parser passes those ids explicitly. ALTERNATIVES: minting at each construction, rejected because every construction that omits the id would need its own call where the classic record needed none; keeping the empty default and teaching readers to tolerate it, rejected because tasks sharing an id collapse into one node of the graph whatever the reader does.

CHOSEN, SECOND: A TASK ID IS A STRING WHEREVER IT IS READ. The failure artifact stores the id as given; the set of tasks waiting on a decision holds the ids of the job's own tasks, so an id naming no task still blocks nothing; the decision inbox seeds its blocked count with the id as a string; `context` no longer refuses a `--task` that is not a UUID and answers with its existing not-found error instead; and `job context` reads a task's planned id from its flight-plan block before its own id, because a task built from a flight plan now carries a minted id beside it. The guidance line of `execute_test_run` reads `job.job_id`, the one attribute of that line the transform left classic.

CHOSEN, THIRD: THE ACCEPTANCE LIST BECOMES TEXT. The two constructions join their criteria with newlines into `TaskEntry.acceptance`, the mapping `planned_task_to_task_entry` already uses, and no pydantic call is made on a task record: `do_materialize` constructs the `TaskEntry` from its dict, and `inject_verify_first` uses `dataclasses.replace`. Every criterion both sites build is required, so nothing a reader could observe is lost there; DECISION F275 D22's registration of the structured form stays with the flip round.

CONSEQUENCE. `tests/orchestration/test_mint_call_sites.py` and `TestMintIds` in `tests/test_data_paths.py` pin the new minter, and the proposed-task fixtures set `REMEDY_DATA_DIR`. What the overlay fixes, and that it newly breaks nothing, is measured by the gates of round 94's block and recorded in the round 94 ledger entry by the round that books its verdict. `R-0809`, `R-0880` and `R-0883` stay open, and no finding is registered or resolved.

HOW TO REVERSE. Delete the round 94 overlay carriers under `.agent/authored/` and this paragraph block; tasks built by code then share the empty id again in the flipped tree.
END DEC94

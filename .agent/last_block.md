── STEP T003 — F275 — ROUND 98 ──
Goal: Commit the flip's ninth OVERLAY, applied after the first eight to the flipped tree at
`844a7f21`: a job load whose `except Exception` handler stands for a missing job calls the
unified store's raising loader, and the runtime test helper writes its job where and as the
unified store reads one; measured by the full suite in fresh flipped trees.

Base commit: `ac17fd6e`. The chain's base stays `844a7f21`, per DECISION F275 D64. Round type:
SPLIT. No path under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/` changes; the overlay
edits production code and two test files, carried in a diff, and G6 red-proves two of its loads.

THE FRAME RULE, per item 37 of §3, stated as the property MEASURED over the final bytes: NO LINE
of this block is a run of a single repeated character, and every box-drawing rule inside the
STEP and SLICE header lines is exactly two characters long.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f275-r98.md`             the block, saved verbatim
C0b `.agent/last_block.md`                    mirrored FROM THE COMMITTED C0a BLOB
C1  `.agent/plan.md`                          slice PLAN98, a full replacement
C2  `.agent/live_review.md`                   slice RECORD98 appended, the round 97 verdict
C3  `.agent/prose_slips.md`                   slice SLIPS98 appended
C4  `.agent/authored/f275-r98-overlay-<k>.md` the overlay carriers of SPEC C, ONE COMMIT EACH
C5  `.agent/decisions.md`                     slice DEC98 appended
C6  `.agent/handoff.md`                       the handback

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3.

## Change — exactly these paths and no others

The Bundle's paths, `<k>` running from 1 over the carriers SPEC C produces.

## SPEC O — the edits, made in the EDIT worktree of constraint 8 on top of the eighth overlay

SPEC O edits these paths and no others: `apps/cli/commands/contract_cmd.py`,
`apps/cli/commands/repo.py`, `apps/cli/commands/test_cmds.py`,
`packages/orchestration/orchestrator_loop.py`, `packages/orchestration/real_test_execution.py`,
`packages/orchestration/repair_loop.py`, `packages/orchestration/watchdog.py`,
`tests/cli/runtime_helpers.py`, `tests/cli/test_test_run_runtime.py`.
O1 THE RAISING LOADER. THE RULE, read with `ast` under `packages/`, `apps/` and `tests/`, names
matched EXACTLY: a call of the bare name `load_job_plan` that is the whole value of an `Assign`
to ONE bare name; that `Assign` is a direct statement of the body of a `try` having a handler
whose type contains the bare name `Exception`, alone or in a tuple; the first later statement
of the same statement list that mentions the bound name READS it; and the innermost enclosing
function holds no comparison whose left operand is that name and one of whose comparators is
the constant `None`. The reviewer's reading finds 13 such calls, one
in each of: `_cmd_contract_inspect`, `_cmd_contract_check` and `_cmd_contract_set` of
`contract_cmd.py`; `_cmd_commit_readiness` of `repo.py`; `_cmd_discover_commands` of
`test_cmds.py`; `open_mission_decisions`, `collect_milestone_evidence` and
`escalate_repeated_refusal` of `orchestrator_loop.py`; `resolve_allowed_command`,
`list_test_runs` and `get_test_run` of `real_test_execution.py`; `start_repair_loop_v0` of
`repair_loop.py`; and `decide` of `watchdog.py`, the innermost definition, nested inside
`act_on_trips`. Each of the 13 calls `require_job_plan` with the same arguments. In the local
`from packages.orchestration.pingpong_job import` of each of those functions — for `decide`,
the one in `act_on_trips` — `require_job_plan` stands in place of `load_job_plan`, with the
names' order otherwise kept, except in `start_repair_loop_v0`, whose second `load_job_plan`
call stays unchanged: its import reads `load_job_plan, require_job_plan, save_job_plan`.
O2 THE RUNTIME HELPER. In `create_test_env` of `runtime_helpers.py`, the local `jobs_dir` becomes
`job_dir = root / "jobs" / jid`, made with the same `mkdir` arguments; the record's keys `"id"`,
`"name"` and `"state"` become `"job_id"`, `"job_title"` and `"status"` with their values and
places kept, `"user_prompt"` holds `""` in place of `None`, and the file written is
`job_dir / "job.json"`. In `_make_job_with_repo` and `test_no_traceback_on_missing_repo_dir` of
`test_test_run_runtime.py`, `data_root / "jobs" / f"{job_id}.json"` becomes
`data_root / "jobs" / job_id / "job.json"`. Nothing else in either file changes.
The function names are the reviewer's reading of `844a7f21` flipped through eight overlays;
where one differs, the call is located by its arguments and the difference declared.

## SPEC C — the carriers, at C4

The VERBATIM stdout of `git diff` in EDIT, against its index as constraint 8 stages it, is cut at
`diff --git` lines into consecutive parts in its own order, each part as many whole file diffs as
fit in 440 lines, a new part starting only when the next file diff would not fit. Part `<k>` is
`.agent/authored/f275-r98-overlay-<k>.md`: at most 40 lines of prose naming its base `844a7f21`,
that the flipped tree is built as G4 of `.agent/authored/f275-r98.md` orders, that the parts form
the NINTH overlay and apply after `.agent/authored/f275-r97-overlay-1.md` in `<k>` order, and
how to apply each — extract the fence, `git apply --check`, then `git apply`; then exactly ONE
fence, a line of three backticks and `diff`, the part, and a line of three backticks; nothing
after it but one newline. Joined in `<k>` order, the fences equal the whole diff byte for byte.

## Constraints

1. NO SLICE IS EDITED. PLAN98, RECORD98, SLIPS98 and DEC98 land byte for byte; a discrepancy
   inside one is DECLARED, never repaired.
2. SPEC O and SPEC C are the worker's OWN work. The reviewer's scratch `.remedy-wt/r90/` through
   `.remedy-wt/r98/` is not opened.
3. READ `.agent/STOP` before C0a and before C6, with real exit codes. If it appears, finish the
   commit in hand, write the handoff and end.
4. Every commit stages EXACTLY ONE path and stays under 500 insertions.
5. No `.py` file under `.agent/`; scratch under `.remedy-wt/r98w/`, uncommitted; every scratch
   output path absolute.
6. No landed record is rewritten: the `.agent/live_review.md`, `.agent/prose_slips.md` and
   `.agent/decisions.md` commits are APPENDS with a ZERO deletion column.
7. No `gh`, no `remedy`, no pull request, no branch created or deleted, no merge, NEVER a
   force-push, no history rewrite. Not even a version query.
8. THREE worktrees, each `git worktree add --detach` at `844a7f21` under `.remedy-wt/r98w/`:
   EDIT, CONTROL and OVERLAY. In each: the transform as G4 orders, `git add -A`, then for each of
   `.agent/authored/f275-r90-overlay.md`, `.agent/authored/f275-r91-overlay.md`,
   `.agent/authored/f275-r92-overlay-1.md` through `-4.md`, `.agent/authored/f275-r93-overlay-1.md`
   and `-2.md`, `.agent/authored/f275-r94-overlay-1.md` and `-2.md`,
   `.agent/authored/f275-r95-overlay-1.md` through `-4.md`, `.agent/authored/f275-r96-overlay-1.md`
   and `.agent/authored/f275-r97-overlay-1.md`, overlay by overlay in that order, the fences of the
   COMMITTED carriers applied with `git apply --check` then `git apply`, and `git add -A` once
   after each overlay's parts. Only EDIT receives SPEC O, and any test may run there while it is
   made; before the diff is taken its `git diff --name-only` lists exactly SPEC O's paths. Only
   OVERLAY receives the C4 carriers. All three are REMOVED AND PRUNED before C5, without
   `--force`. The generator's trees are plain directories.
9. THE BLOCK'S OWN SIZE, measured on its final bytes: 287 lines TOTAL and 219 lines of
   PROSE, against the caps of 490 and 400.
10. GATE ORDER. G4's setup — the generator, the three worktrees, the chain — runs after C3 and
    before the first C4 commit, because the carriers are cut from EDIT; G4's readings, G5 and G6
    are taken after the last C4 commit and strictly before C5, per item 31 of §3. DEC98's one
    measured figure, 13, is G4(b)'s CONTROL reading; DEC98 quotes no G5 or G6 reading. G1, G2,
    G3, G7 and G8 run at C5. No gate runs after C6; C6's own numbers are the reviewer's.
11. A RED G5 IS A STOP. Each node G5 finds bad only in OVERLAY is re-run by its node id alone in
    OVERLAY three times with G5's environment; unless every re-run passes, the worker commits
    nothing further after C4 except the handback, which lists every such node with its last
    `E   ` line. A node whose three re-runs all pass is reported FLAKY with the three tallies.

## Done when — the gates, each run for real and its exit code recorded

G1 TRANSPORT, BUDGET, SLICES. `.agent/authored/f275-r98.md` at C0a against the block as received,
by `cmp`; `.agent/last_block.md` at C0b byte-identical to the COMMITTED C0a blob. Extract the
slices by their markers, report how many were FOUND, check each against its BEGIN-marker
sha256, and re-measure TOTAL and PROSE against constraint 9.

G2 THE PLAN. `.agent/plan.md` at C1 byte-identical to PLAN98 from the COMMITTED C0a blob; at
most 50 lines; one `## Goal` and one `## Next Steps`.

G3 THE RECORD. For the appends at C2 into `.agent/live_review.md` and at C5 into
`.agent/decisions.md`, FULL FORENSICS: the pre-commit blob read with `git show` at the commit's
PARENT, its length printed — 1154699 and 1302522 — READER A with the arithmetic printed; READER B
over the file's LAST N blank-line units against the slice's N paragraphs IN ORDER, N counted by
the script; a letter flipped in the FIRST appended paragraph REJECTED by both readers; deletion
column 0. `.agent/prose_slips.md` at C3 equals its 304316-byte pre-commit blob followed by
exactly SLIPS98. Derive the ledger's `Gate:` header pattern from the file, report how many heads
it matches, and that RECORD98's header matches it and duplicates none.

G4 THE TREES, THE CHAIN AND THE CARRIERS, set up and read per constraint 10. The generator trees
and run exactly as G4 of `.agent/authored/f275-r90.md` orders, the pinned digests checked first,
with the readings that block states; the transform in each worktree reading 2183 resolving and 0
not, 264 files, 6097 rewrites and 0 broken; every earlier overlay applying with exit 0 in each.
Then: (a) the fences extracted from the COMMITTED C4 blobs: report the part count and each part's
line count, each at most 440; joined in `<k>` order they equal EDIT's diff; in OVERLAY each
applies with `git apply --check` and `git apply` exit 0, in order; `git diff --name-only` there,
against the index constraint 8 staged, lists exactly SPEC O's paths by name, each byte-identical
to EDIT's; report MISSING and EXTRA. (b) With `ast`, in CONTROL and in OVERLAY: THE RULE of O1
counted over `packages/`, `apps/` and `tests/`, once with the callee `load_job_plan` and once with
the callee `require_job_plan` in its place, 13 and 0 in CONTROL, 0 and 13 in OVERLAY, each site
listed as path, innermost function and line; and inside the three functions O2 names, dict
literal keys that are the string constants `id`, `name` or `state`, 3 and 0, keys `job_id`,
`job_title` or `status`, 0 and 3, and f-strings whose last literal part ends in `.json`, 3 and 0.
(c) `ruff check --output-format concise`, run from inside each of CONTROL and OVERLAY over SPEC
O's paths, rows compared as a MULTISET of `<path>: <code> <message>` with line and column
DROPPED: added 0 and removed 0. The reviewer read 10 rows in each; the exit is 1 in BOTH trees
and is reported, never ordered.

G5 THE FULL SUITE IN FRESH FLIPPED TREES, per constraint 10, CONTROL first and OVERLAY second,
serially. Each is its worktree's FIRST pytest run of any kind, `apps/ui/node_modules` and
`apps/ui/dist` reported absent before it. `cwd` the worktree; `PYTHONPATH`, `REMEDY_PROJECT` and
`REMEDY_DATA_DIR` removed; `PYTHONDONTWRITEBYTECODE=1`;
`packages.orchestration.pingpong_job.__file__` printed and inside the worktree;
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`. A bad node is the
text after `FAILED ` or `ERROR ` up to the first ` - ` or the line's end. The reviewer measured
CONTROL `106 failed, 18329 passed, 29 skipped, 1 warning, 7 errors`, 113 bad nodes, and its own
dry run of SPEC O `84 failed, 18351 passed, 29 skipped, 1 warning, 7 errors`, 91. REPORT
OVERLAY's tally and bad-node count. Bad only in OVERLAY: MUST be 0, per constraint 11. REPORT
the fixed nodes' count per test file.

G6 THE PROBES, per constraint 10, in OVERLAY after G5; `__pycache__` purged before each run;
G5's environment; flags `-q -p no:randomly -p no:cacheprovider --tb=short -rfE`. For each
mutation, the bytes it replaces counted as stated first, then the selection run UNMUTATED and
MUTATED, each tally and exit code reported with the node ids bad only under the mutation, then
the file restored and its bytes confirmed. Both mutations replace the bytes
`require_job_plan(job_id)` with
`__import__("packages.orchestration.pingpong_job", fromlist=["load_job_plan"]).load_job_plan(job_id)`
inside ONE function only. M1 in `apps/cli/commands/contract_cmd.py`, inside
`_cmd_contract_inspect`, where the bytes count 1 there and 3 in the file, over
`tests/cli/test_contract_runtime.py`: `TestContractInspectCLI::test_missing_job_safe` and
`TestContractInspectCLI::test_invalid_job_safe` MUST go bad; the reviewer's dry run read
`6 passed` unmutated and `2 failed, 4 passed` mutated. M2 in
`packages/orchestration/repair_loop.py`, inside `start_repair_loop_v0`, where the bytes count 1
there and 1 in the file, over `tests/orchestration/test_test_failure_repair.py`:
`TestRepairLoopV0::test_repair_loop_job_not_found` and
`TestRepairCLIHandlers::test_repair_start_job_not_found` MUST go bad; the reviewer's dry run read
`58 passed` unmutated and `2 failed, 56 passed` mutated.

G7 TREE, CANARY, LINT, PATH SET, OPEN SET, at C5. `git status --porcelain` prints `''`;
`git worktree list` one row; `git diff --name-only ac17fd6e C5 -- packages apps tests docs
scripts` empty; the canary `python3 -B -m pytest tests/cli/test_golden_path.py -q` exit 0, 42;
`ruff check . --output-format concise` rows as a MULTISET at `ac17fd6e`, read from a
`git archive` tree, and at C5, difference empty, 26 at `ac17fd6e`. The changed-path set of
`ac17fd6e`..C5 against the Bundle's paths MINUS `.agent/handoff.md`, MISSING and EXTRA by name.
The open set BY DISTINCT ID at `ac17fd6e` and at C5: 88 at both, membership identical;
`R-0809`, `R-0880` and `R-0883` open.

G8 THE INSERTION CAP over `ac17fd6e`..C5: one row per commit with insertions, deletions and
staged path count, and the number of commits reaching 500 insertions.

Handback: `.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 33 of feature F275 · round 98 · rounds so far 98`; the Commits table read from
`git show --numstat` and compared cell by cell against G8, C6's row carrying no numbers and
saying why; one Verification line per gate with its REAL exit code; External actions;
Authored-text proofs; Item-status; Deviations; `## Next` stating `Operator questions open: 1`.
NO SCOPE REPORT AND NO SESSION-LIMIT BANNER, by amendment amend0911-f275-to-scope.

── SLICE PLAN98 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN98 sha256=68f437d7db73c8782b87311ab1ab924739fbfd235b0d45d7744683984bdc1042
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

ROUND 98 ADDS THE FLIP'S NINTH OVERLAY, on top of the first eight, under DECISION F275 D64's
method. A job load whose `except Exception` handler stands for a missing job, and whose result
is read after that handler, calls the unified store's raising loader, so the handler runs
again; and the runtime test helper writes its job where, and in the shape, the unified store
reads one. The diff is carried in a carrier, so no path under `packages/`, `apps/` or `tests/`
moves; the round books the round 97 verdict and its prose slip.

## Next Steps

1. MORE OVERLAYS, one residue group each, every one applied on top of those before it:
   production code that hands a `JobPlan` a `JobBudgets` model where the record holds its
   serialized dict; the `mission` and `decision resolve --as-mission` commands finding no
   previous job; the self-dogfood runtimes; the classic-shaped tests of routed handlers in
   `tests/test_data_paths.py`; and what is left of the classic runner under `job resume`, which
   still builds a classic job.
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
END PLAN98

── SLICE RECORD98 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD98 sha256=a765ca276968914d7aa88672dfc71ca08841a6a28f59850e675f70558260a99b

Gate: F275 R97 — the F275 round 97 entry. VERDICT PASS. Written by the planner and reviewer of session 32 after reading the committed range `a8f86e5c`..`a98d47c6` and RE-DERIVING EVERY GATE AND EVERY PROBE INDEPENDENTLY; the worker's report and its transcripts were evidence for no line below. It is booked here by the FIRST SUBSTANTIVE COMMIT of round 98 that writes the record, per operator amendment amend0827-process-diet rule 1. The round moved no path under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/`; its code is the diff carried in `.agent/authored/f275-r97-overlay-1.md`.

WHAT THE TRANSPORT PROOF COVERS, per item 37 of §3. The committed `.agent/authored/f275-r97.md` blob was identical to the reviewer's own original at 23039 bytes, `.agent/last_block.md` equalled it from its own commit through `a98d47c6`, and all four slices matched their BEGIN-marker digests; `.agent/plan.md` equalled PLAN97. The three appends were exact under reader A — 1151875 plus 2824 into the review record, 303802 plus 514 into the prose slips and 1300377 plus 2145 into the decisions — with reader B holding at N counted from each slice as 3, 1 and 6, and a letter flipped in each FIRST appended paragraph rejected by both readers. Every commit staged one path, the largest the carrier at 236 insertions, and its one fence reads 197 lines.

THE OVERLAY HOLDS UNDER THE REVIEWER'S OWN RE-RUN. The reviewer transformed a worktree at `844a7f21` from its own generator run, applied and staged the committed overlays of rounds 90 to 96, and applied the committed round 97 fence: every `git apply --check` and `git apply` exited 0, 6 paths changed, all production code, and the diff was byte-identical to the reviewer's own final dry run of SPEC O. With `ast`, the `_as_uuid` definition and references, the `UUID` calls in `event_persistence.py` and the classic task reads in the five named functions read 0, 0 and 0, against 5, 1 and 15 in a control tree of the chain before it; the `ruff` rows over the six files read 1 in each tree as a multiset with line and column dropped, none added. That worktree's first full run read 106 failed, 18329 passed, 29 skipped and 7 errors, 113 bad nodes, against 149 in the reviewer's fresh run of the chain before it: 36 fixed and none newly bad. In the same worktree, parsing the watchdog's job id with `UUID` again made `test_the_ledger_entry_carries_the_trip_payload_unchanged` and four more nodes of `tests/orchestration/test_watchdog.py` bad, and doing the same in `collect_milestone_evidence` made all 24 nodes of `tests/orchestration/test_mission_e2e.py` error. In the primary checkout at `a98d47c6` the canary read 42 and `ruff check .` read 26 rows; the open set stayed 88 with identical membership, `R-0809`, `R-0880` and `R-0883` open.
END RECORD98

── SLICE SLIPS98 ── target `.agent/prose_slips.md` ── APPEND ──
BEGIN SLIPS98 sha256=5967d10a4d592f571f0c9c17e241449bf5d9b6e3b728f0f66518f1e735e33b55

2026-09-14 · F275 R97 · SPEC O1 of the round 97 block named `act_on_trips` as the function holding the watchdog's `_as_uuid` call, while the call sits in `decide`, a function nested inside it; the worker placed the `normalize_job_id` import in `act_on_trips` and declared it. THE RULE THAT FOLLOWS: the function a block cites as holding a call is the innermost definition enclosing it, read with `ast`, never the outermost.
END SLIPS98

── SLICE DEC98 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC98 sha256=eb47782bc620227f9843ea7f6d96991d6d16265a24ef3040a570214aa2ff826d

## DECISION F275 D72 (2026-09-14, F275 round 98) — the ninth overlay: a job load whose `except Exception` handler stands for a missing job calls the raising loader, and the runtime test helper writes the unified record

CONTEXT. In the flipped tree at `844a7f21`, with eight overlays applied, 13 calls of `load_job_plan` sit in a `try` whose handler catches `Exception` and reports the job missing or unreadable, and the name each call binds is read after that `try` with no `None` test. The classic `storage.load_job` raised for an absent record, so those handlers ran; `load_job_plan` answers `None`, so the handler never runs and the `None` travels on to the next attribute read, where `contract inspect`, `contract check` and the repair loop's start stop with a traceback instead of reporting the job missing. DECISION F275 D66 routed the loads whose handler names `JobNotFoundError`; these name only `Exception`. Separately, `create_test_env` in `tests/cli/runtime_helpers.py` writes a classic job record, keyed `id` in a flat `.json` file under `jobs/`, which the unified store never reads, so every `test run` runtime test that uses it finds no job.

CHOSEN, FIRST: THE RAISING LOADER AT THOSE 13 CALLS. Each calls `require_job_plan` with the same arguments; its `JobNotFoundError` and `JobStoreError` are both an `Exception`, so every handler runs again for the case it was written for. ALTERNATIVE: a `None` test after each call, rejected as DECISION F275 D66 rejected it, as one contract copied into every caller. Loads whose bound name is read only inside the `try` are not in this overlay; where their `None` still matters, the residue will show it.

CHOSEN, SECOND: THE TEST HELPER WRITES WHAT THE FLIPPED STORE READS. `create_test_env` writes `job.json` in a directory named by the job id, with the unified record's `job_id`, `job_title` and `status` keys, and the two readers of that file in `tests/cli/test_test_run_runtime.py` follow its path. ALTERNATIVE: building the record with `JobPlan` and `save_job_plan`, rejected because the helper's module docstring says all orchestration state is created via direct JSON writes.

CONSEQUENCE. What the overlay fixes, and that it newly breaks nothing, is measured by the gates of round 98's block and recorded in the round 98 ledger entry by the round that books its verdict. `R-0809`, `R-0880` and `R-0883` stay open, and no finding is registered or resolved.

HOW TO REVERSE. Delete the round 98 overlay carriers under `.agent/authored/` and this paragraph block; in the flipped tree those handlers are dead again and the runtime helper's job cannot be read.
END DEC98

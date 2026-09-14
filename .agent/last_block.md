── STEP T003 — F275 — ROUND 97 ──
Goal: Commit the flip's eighth OVERLAY, applied after the first seven to the flipped tree at
`844a7f21`: the orchestrator loop and the watchdog load a mission's jobs through the job-id
shape check, the event writer checks a job id the same way, and a job's tasks are read by the
unified task record's names; measured by the full suite in fresh flipped trees.

Base commit: `a8f86e5c`. The chain's base stays `844a7f21`, per DECISION F275 D64. Round type:
SPLIT. No path under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/` changes; the overlay
edits production code only, carried in a diff, and G6 red-proves two of its loads.

THE FRAME RULE, per item 37 of §3, stated as the property MEASURED over the final bytes: NO LINE
of this block is a run of a single repeated character, and every box-drawing rule inside the
STEP and SLICE header lines is exactly two characters long.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f275-r97.md`             the block, saved verbatim
C0b `.agent/last_block.md`                    mirrored FROM THE COMMITTED C0a BLOB
C1  `.agent/plan.md`                          slice PLAN97, a full replacement
C2  `.agent/live_review.md`                   slice RECORD97 appended, the round 96 verdict
C3  `.agent/prose_slips.md`                   slice SLIPS97 appended
C4  `.agent/authored/f275-r97-overlay-<k>.md` the overlay carriers of SPEC C, ONE COMMIT EACH
C5  `.agent/decisions.md`                     slice DEC97 appended
C6  `.agent/handoff.md`                       the handback

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3.

## Change — exactly these paths and no others

The Bundle's paths, `<k>` running from 1 over the carriers SPEC C produces.

## SPEC O — the edits, made in the EDIT worktree of constraint 8 on top of the seventh overlay

SPEC O edits these paths and no others: `apps/cli/commands/mission_cmd.py`,
`packages/orchestration/event_persistence.py`, `packages/orchestration/orchestrator_loop.py`,
`packages/orchestration/ui_server.py`, `packages/orchestration/ui_view_model.py`,
`packages/orchestration/watchdog.py`. `normalize_job_id` is imported from
`packages.orchestration.data_paths` inside each function that calls it, placed where the
function's other local imports sort it.
O1 THE SHAPE CHECK. `_as_uuid` is deleted from `orchestrator_loop.py`. Its three calls there —
in `open_mission_decisions`, in `collect_milestone_evidence` and in
`escalate_repeated_refusal` — and the call `orchestrator_loop._as_uuid(link.job_id)` in
`act_on_trips` of `watchdog.py` read `normalize_job_id(...)` of the same argument.
O2 THE EVENT WRITER. `emit_important_event` in `event_persistence.py` checks the id with
`normalize_job_id(str(job_id))` where it called `UUID(str(job_id))`, under the same
`except (ValueError, TypeError)`, and its `from uuid import UUID` is removed.
O3 A JOB'S TASKS. These reads, and no others, change: in `_cmd_mission_continue` of
`mission_cmd.py`, `verify.description` twice and `t.description` once become `.title`; in
`escalate_repeated_refusal` of `orchestrator_loop.py`, `tasks[0].id` becomes `tasks[0].task_id`;
in `_build_job_plan_dashboard` of `ui_server.py`, `t.id` once becomes `t.task_id` and
`t.description` twice becomes `t.title`; in `_build_live_state_json` of `ui_server.py`, `t.id`
twice becomes `t.task_id`; in `build_checklist` of `ui_view_model.py`, `task.description` three
times becomes `task.title` and `task.id` three times becomes `task.task_id`.
The function names in O1 are the reviewer's reading of `844a7f21` flipped through seven
overlays; where one differs, the call is located by its argument and the difference declared.

## SPEC C — the carriers, at C4

The VERBATIM stdout of `git diff` in EDIT, against its index as constraint 8 stages it, is cut at
`diff --git` lines into consecutive parts in its own order, each part as many whole file diffs as
fit in 440 lines, a new part starting only when the next file diff would not fit. Part `<k>` is
`.agent/authored/f275-r97-overlay-<k>.md`: at most 40 lines of prose naming its base `844a7f21`,
that the flipped tree is built as G4 of `.agent/authored/f275-r97.md` orders, that the parts form
the EIGHTH overlay and apply after `.agent/authored/f275-r96-overlay-1.md` in `<k>` order, and
how to apply each — extract the fence, `git apply --check`, then `git apply`; then exactly ONE
fence, a line of three backticks and `diff`, the part, and a line of three backticks; nothing
after it but one newline. Joined in `<k>` order, the fences equal the whole diff byte for byte.

## Constraints

1. NO SLICE IS EDITED. PLAN97, RECORD97, SLIPS97 and DEC97 land byte for byte; a discrepancy
   inside one is DECLARED, never repaired.
2. SPEC O and SPEC C are the worker's OWN work. The reviewer's scratch `.remedy-wt/r90/` through
   `.remedy-wt/r97/` is not opened.
3. READ `.agent/STOP` before C0a and before C6, with real exit codes. If it appears, finish the
   commit in hand, write the handoff and end.
4. Every commit stages EXACTLY ONE path and stays under 500 insertions.
5. No `.py` file under `.agent/`; scratch under `.remedy-wt/r97w/`, uncommitted; every scratch
   output path absolute.
6. No landed record is rewritten: the `.agent/live_review.md`, `.agent/prose_slips.md` and
   `.agent/decisions.md` commits are APPENDS with a ZERO deletion column.
7. No `gh`, no `remedy`, no pull request, no branch created or deleted, no merge, NEVER a
   force-push, no history rewrite. Not even a version query.
8. THREE worktrees, each `git worktree add --detach` at `844a7f21` under `.remedy-wt/r97w/`:
   EDIT, CONTROL and OVERLAY. In each: the transform as G4 orders, `git add -A`, then for each of
   `.agent/authored/f275-r90-overlay.md`, `.agent/authored/f275-r91-overlay.md`,
   `.agent/authored/f275-r92-overlay-1.md` through `-4.md`, `.agent/authored/f275-r93-overlay-1.md`
   and `-2.md`, `.agent/authored/f275-r94-overlay-1.md` and `-2.md`,
   `.agent/authored/f275-r95-overlay-1.md` through `-4.md` and
   `.agent/authored/f275-r96-overlay-1.md`, overlay by overlay in that order, the fences of the
   COMMITTED carriers applied with `git apply --check` then `git apply`, and `git add -A` once
   after each overlay's parts. Only EDIT receives SPEC O, and any test may run there while it is
   made; before the diff is taken its `git diff --name-only` lists exactly SPEC O's paths. Only
   OVERLAY receives the C4 carriers. All three are REMOVED AND PRUNED before C5, without
   `--force`. The generator's trees are plain directories.
9. THE BLOCK'S OWN SIZE, measured on its final bytes: 273 lines TOTAL and 204 lines of
   PROSE, against the caps of 490 and 400.
10. GATE ORDER. G4's setup — the generator, the three worktrees, the chain — runs after C3 and
    before the first C4 commit, because the carriers are cut from EDIT; G4's readings, G5 and G6
    are taken after the last C4 commit and strictly before C5, per item 31 of §3. DEC97's
    measured figures, 5, 1 and 15, are G4(b)'s CONTROL readings; DEC97 quotes no G5 or G6
    reading. G1, G2, G3, G7 and G8 run at C5. No gate runs after C6; C6's own numbers are the
    reviewer's.
11. A RED G5 IS A STOP. Each node G5 finds bad only in OVERLAY is re-run by its node id alone in
    OVERLAY three times with G5's environment; unless every re-run passes, the worker commits
    nothing further after C4 except the handback, which lists every such node with its last
    `E   ` line. A node whose three re-runs all pass is reported FLAKY with the three tallies.

## Done when — the gates, each run for real and its exit code recorded

G1 TRANSPORT, BUDGET, SLICES. `.agent/authored/f275-r97.md` at C0a against the block as received,
by `cmp`; `.agent/last_block.md` at C0b byte-identical to the COMMITTED C0a blob. Extract the
slices by their markers, report how many were FOUND, check each against its BEGIN-marker
sha256, and re-measure TOTAL and PROSE against constraint 9.

G2 THE PLAN. `.agent/plan.md` at C1 byte-identical to PLAN97 from the COMMITTED C0a blob; at
most 50 lines; one `## Goal` and one `## Next Steps`.

G3 THE RECORD. For the appends at C2 into `.agent/live_review.md` and at C5 into
`.agent/decisions.md`, FULL FORENSICS: the pre-commit blob read with `git show` at the commit's
PARENT, its length printed — 1151875 and 1300377 — READER A with the arithmetic printed; READER B
over the file's LAST N blank-line units against the slice's N paragraphs IN ORDER, N counted by
the script; a letter flipped in the FIRST appended paragraph REJECTED by both readers; deletion
column 0. `.agent/prose_slips.md` at C3 equals its 303802-byte pre-commit blob followed by
exactly SLIPS97. Derive the ledger's `Gate:` header pattern from the file, report how many heads
it matches, and that RECORD97's header matches it and duplicates none.

G4 THE TREES, THE CHAIN AND THE CARRIERS, set up and read per constraint 10. The generator trees
and run exactly as G4 of `.agent/authored/f275-r90.md` orders, the pinned digests checked first,
with the readings that block states; the transform in each worktree reading 2183 resolving and 0
not, 264 files, 6097 rewrites and 0 broken; every earlier overlay applying with exit 0 in each.
Then: (a) the fences extracted from the COMMITTED C4 blobs: report the part count and each part's
line count, each at most 440; joined in `<k>` order they equal EDIT's diff; in OVERLAY each
applies with `git apply --check` and `git apply` exit 0, in order; `git diff --name-only` there,
against the index constraint 8 staged, lists exactly SPEC O's paths by name, each byte-identical
to EDIT's; report MISSING and EXTRA. (b) With `ast`, in CONTROL and in OVERLAY, names matched
EXACTLY: function definitions named `_as_uuid`, plus bare names and attribute nodes named
`_as_uuid`, under `packages/`, `apps/` and `tests/`, 5 and 0; calls of the bare name `UUID` in
`packages/orchestration/event_persistence.py`, 1 and 0; inside the five functions O3 names,
attribute reads in Load context named `id` or `description` off the bare names `verify`, `t` or
`task`, or off a subscript of the bare name `tasks`, 15 and 0. (c) `ruff check --output-format
concise`, run from inside each of CONTROL and OVERLAY over SPEC O's paths, rows compared as a
MULTISET of `<path>: <code> <message>` with line and column DROPPED: added 0 and removed 0. The
reviewer read 1 row in each; the exit is 1 in BOTH trees and is reported, never ordered.

G5 THE FULL SUITE IN FRESH FLIPPED TREES, per constraint 10, CONTROL first and OVERLAY second,
serially. Each is its worktree's FIRST pytest run of any kind, `apps/ui/node_modules` and
`apps/ui/dist` reported absent before it. `cwd` the worktree; `PYTHONPATH`, `REMEDY_PROJECT` and
`REMEDY_DATA_DIR` removed; `PYTHONDONTWRITEBYTECODE=1`;
`packages.orchestration.pingpong_job.__file__` printed and inside the worktree;
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`. A bad node is the
text after `FAILED ` or `ERROR ` up to the first ` - ` or the line's end. The reviewer measured
CONTROL `118 failed, 18293 passed, 29 skipped, 1 warning, 31 errors`, 149 bad nodes, and its own
dry run of SPEC O, before one import it left unsorted was moved,
`106 failed, 18329 passed, 29 skipped, 1 warning, 7 errors`, 113. REPORT OVERLAY's tally and
bad-node count. Bad only in OVERLAY: MUST be 0, per constraint 11. REPORT the fixed nodes'
count per test file.

G6 THE PROBES, per constraint 10, in OVERLAY after G5; `__pycache__` purged before each run;
G5's environment; flags `-q -p no:randomly -p no:cacheprovider --tb=short -rfE`. For each
mutation, the bytes it replaces counted in the file as 1 first, then the selection run UNMUTATED
and MUTATED, each tally and exit code reported with the node ids bad only under the mutation,
then the file restored and its bytes confirmed. M1 in `packages/orchestration/watchdog.py`, the
O1 call's `normalize_job_id(link.job_id)` becomes `str(__import__("uuid").UUID(link.job_id))`,
over `tests/orchestration/test_watchdog.py`: `test_the_ledger_entry_carries_the_trip_payload_unchanged`
MUST go bad; the reviewer's dry run read 37 passed unmutated and 5 bad mutated. M2 in
`packages/orchestration/orchestrator_loop.py`, the O1 call in `collect_milestone_evidence` changes the
same way, over `tests/orchestration/test_mission_e2e.py`: every node of that file MUST go bad;
the reviewer's dry run read 24 passed unmutated and 24 errors mutated.

G7 TREE, CANARY, LINT, PATH SET, OPEN SET, at C5. `git status --porcelain` prints `''`;
`git worktree list` one row; `git diff --name-only a8f86e5c C5 -- packages apps tests docs
scripts` empty; the canary `python3 -B -m pytest tests/cli/test_golden_path.py -q` exit 0, 42;
`ruff check . --output-format concise` rows as a MULTISET at `a8f86e5c`, read from a
`git archive` tree, and at C5, difference empty, 26 at `a8f86e5c`. The changed-path set of
`a8f86e5c`..C5 against the Bundle's paths MINUS `.agent/handoff.md`, MISSING and EXTRA by name.
The open set BY DISTINCT ID at `a8f86e5c` and at C5: 88 at both, membership identical;
`R-0809`, `R-0880` and `R-0883` open.

G8 THE INSERTION CAP over `a8f86e5c`..C5: one row per commit with insertions, deletions and
staged path count, and the number of commits reaching 500 insertions.

Handback: `.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 32 of feature F275 · round 97 · rounds so far 97`; the Commits table read from
`git show --numstat` and compared cell by cell against G8, C6's row carrying no numbers and
saying why; one Verification line per gate with its REAL exit code; External actions;
Authored-text proofs; Item-status; Deviations; `## Next` stating `Operator questions open: 1`.
NO SCOPE REPORT AND NO SESSION-LIMIT BANNER, by amendment amend0911-f275-to-scope.

── SLICE PLAN97 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN97 sha256=a50a3011c95a50ef8f218e89e44837530119c29c973f25e18d73772f9759c6b1
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

ROUND 97 ADDS THE FLIP'S EIGHTH OVERLAY, on top of the first seven, under DECISION F275 D64's
method. The orchestrator loop and the watchdog load a mission's jobs through the job-id shape
check instead of a `UUID` parse, the important-event writer checks a job id the same way, and
code reading a task it took from a job's tasks reads the unified task record's `task_id` and
`title`. The diff is carried in a carrier, so no path under `packages/`, `apps/` or `tests/`
moves; the round books the round 96 verdict and its prose slip.

## Next Steps

1. MORE OVERLAYS, one residue group each, every one applied on top of those before it:
   production code that hands a `JobPlan` a `JobBudgets` model where the record holds its
   serialized dict; the `mission` and `decision resolve --as-mission` commands finding no
   previous job; command-line tests whose job the flipped store does not find, among them the
   test-run, contract and self-dogfood runtimes; the classic-shaped tests of routed handlers in
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
END PLAN97

── SLICE RECORD97 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD97 sha256=de519e1b38fc57d6d67f88a98ad9b3e37d836ccfd47163fdd6840660d3826ade

Gate: F275 R96 — the F275 round 96 entry. VERDICT PASS. Written by the planner and reviewer of session 32 after reading the committed range `0fe76bb9`..`a8f86e5c` and RE-DERIVING EVERY GATE AND EVERY PROBE INDEPENDENTLY; the worker's report and its transcripts were evidence for no line below. It is booked here by the FIRST SUBSTANTIVE COMMIT of round 97 that writes the record, per operator amendment amend0827-process-diet rule 1. The round moved no path under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/`; its code is the diff carried in `.agent/authored/f275-r96-overlay-1.md`.

WHAT THE TRANSPORT PROOF COVERS, per item 37 of §3. The committed `.agent/authored/f275-r96.md` blob was identical to the reviewer's own original at 25466 bytes, `.agent/last_block.md` equalled it from its own commit through `a8f86e5c`, and all four slices matched their BEGIN-marker digests; `.agent/plan.md` equalled PLAN96. The three appends were exact under reader A — 1148938 plus 2937 into the review record, 303243 plus 559 into the prose slips and 1297335 plus 3042 into the decisions — with reader B holding at N counted from each slice as 3, 1 and 7, and a letter flipped in each FIRST appended paragraph rejected by both readers. Every commit staged one path, the largest the carrier at 363 insertions, and its one fence reads 325 lines.

THE OVERLAY HOLDS UNDER THE REVIEWER'S OWN RE-RUN. The reviewer transformed a worktree at `844a7f21` from its own generator run, applied and staged the committed overlays of rounds 90 to 95, and applied the committed round 96 fence: every `git apply --check` and `git apply` exited 0 and 10 paths changed, two of them production code. With `ast`, the pydantic class calls on `JobPlan`, the pydantic calls on a `job` local and the `created_at` keywords handed a `datetime` read 0, 0 and 0, against 9, 12 and 6 in a control tree of the chain before it; the `ruff` rows over the 10 files read 9 in each tree as a multiset with line and column dropped, none added. That worktree's first full run read 118 failed, 18293 passed, 29 skipped and 31 errors, 149 bad nodes, against 181 in the reviewer's fresh run of the chain before it: 32 fixed and none newly bad. In the same worktree, printing `job.model_dump_json` again in `_cmd_show_job` made `test_job_show_accepts_short_id` and three more nodes of `tests/cli/test_golden_path.py` bad, and dropping the restored `.isoformat()` made exactly `test_record_export_no_secrets` and `test_report_shows_completed` bad. In the primary checkout at `a8f86e5c` the canary read 42 and `ruff check .` read 26 rows; the open set stayed 88 with identical membership, `R-0809`, `R-0880` and `R-0883` open. The worker issued one `gh` command, which the block forbids; the permission layer refused it before it ran, and the worker declared it.
END RECORD97

── SLICE SLIPS97 ── target `.agent/prose_slips.md` ── APPEND ──
BEGIN SLIPS97 sha256=50c82316aa0b068458e6bbd9f8a14ff122b97e592d03d23624ea32f2a668beb3

2026-09-14 · F275 R96 · SPEC O4 of the round 96 block ordered all three budget tests to "export with `_export_job`, restore with `_import_job`", while the reviewer's own dry run restored the record in two of them and only exported it in `test_job_with_budgets_serializes`; the worker followed the words, added a restore and two checks to that test, and declared it. THE RULE THAT FOLLOWS: a SPEC sentence that groups several sites under one order is read against the dry-run edit of each site before it leaves.
END SLIPS97

── SLICE DEC97 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC97 sha256=b8aec3ec3ffeb44cfafe67feda3ba1bddf988ee26bd60eb5f1797eea8505c666

## DECISION F275 D71 (2026-09-14, F275 round 97) — the eighth overlay: the orchestrator loop and the watchdog load a mission's jobs through the job-id shape check, the event writer checks a job id the same way, and a job's tasks are read by the unified task record's names

CONTEXT. In the flipped tree at `844a7f21`, with seven overlays applied, `orchestrator_loop._as_uuid` — defined once and referenced three times in its module and once from `watchdog.py`, 5 references in all — turns a job id into a `UUID`, which the sixteen-hex id the unified store mints cannot become; every caller catches the error and treats the job as unreadable, so a mission's loop and its watchdog never see that job's decisions or its milestone evidence. `emit_important_event` refuses the same id through 1 `UUID` call and reports it invalid. And 15 reads of `.id` or `.description` off a task taken from a job's tasks, in five functions, still spell the classic task record.

CHOSEN, FIRST: THE SHAPE CHECK, NOT A PARSE. `_as_uuid` is deleted, its callers and the event writer pass the id through `normalize_job_id`, the disk-free shape check DECISION F275 D62 ruled for a job-store load under `packages/`, which accepts a UUID and a sixteen-hex id alike. ALTERNATIVE: keeping `_as_uuid` as a name for `normalize_job_id`, rejected because a second name for one function is how the two would drift apart again.

CHOSEN, SECOND: A JOB'S TASKS SPELL THE UNIFIED TASK RECORD. The 15 reads become `task_id` and `title`, as DECISION F275 D69 ruled for a job's own reads.

CONSEQUENCE. No probe of round 97's block red-proves a task read, so for those reads the full suite, per DECISION F275 D48, is the only backstop. What the overlay fixes, and that it newly breaks nothing, is measured by the gates of round 97's block and recorded in the round 97 ledger entry by the round that books its verdict. `R-0809`, `R-0880` and `R-0883` stay open, and no finding is registered or resolved.

HOW TO REVERSE. Delete the round 97 overlay carriers under `.agent/authored/` and this paragraph block; a mission's loop then cannot read its jobs in the flipped tree again.
END DEC97

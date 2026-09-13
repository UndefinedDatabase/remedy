── STEP T003 — F275 — ROUND 93 ──
Goal: Commit the flip's fourth OVERLAY, applied after the first three to the flipped tree at
`844a7f21`: test doubles installed by the classic store's names, and unified functions read off
the classic `storage` module, point at what the flipped code calls, and the retired-`status`
guard covers `require_job_plan`; measured by the full suite in fresh flipped trees.

Base commit: `dbab6b13`. The chain's base stays `844a7f21`, per DECISION F275 D64. Round type:
SPLIT. No path under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/` changes; the overlay
edits test code only, carried in a diff, and G6 probes the guard it widens.

THE FRAME RULE, per item 37 of §3, stated as the property MEASURED over the final bytes: NO LINE
of this block is a run of a single repeated character, and every box-drawing rule inside the
STEP and SLICE header lines is exactly two characters long.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f275-r93.md`             the block, saved verbatim
C0b `.agent/last_block.md`                    mirrored FROM THE COMMITTED C0a BLOB
C1  `.agent/plan.md`                          slice PLAN93, a full replacement
C2  `.agent/live_review.md`                   slice RECORD93 appended, the round 92 verdict
C3  `.agent/prose_slips.md`                   slice SLIPS93 appended
C4  `.agent/authored/f275-r93-overlay-<k>.md` the overlay carriers of SPEC C, ONE COMMIT EACH
C5  `.agent/decisions.md`                     slice DEC93 appended
C6  `.agent/handoff.md`                       the handback

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3.

## Change — exactly these paths and no others

The Bundle's paths, `<k>` running from 1 over the carriers SPEC C produces.

## SPEC O — the edits, made in the EDIT worktree of constraint 8 on top of the third overlay

Under `tests/` only; no assertion changes and no test is added or deleted, except as O4 says.
O1 DOTTED TARGETS. Every string constant fully matching `(apps|packages)\.[a-z_.]+\.([a-z_]+)`
whose last component is `load_job`, `load_job_safe`, `save_job`, `list_jobs` or `list_jobs_safe`
— the reviewer's count 53 — names instead the function the code under test calls in the flipped
tree, on the module whose binding that code reads at call time. For a handler's own module that
is the name the module binds (`require_job_plan` or `save_job_plan`); for
`packages.orchestration.storage` it is `packages.orchestration.pingpong_job.<name>`, `<name>`
being what the handler under test imports inside its function (`load_job_plan`,
`require_job_plan`, `save_job_plan` or `list_job_plans_safe`).
O2 SETATTR BY NAME. The `monkeypatch.setattr` calls whose second argument is one of those five
names — the reviewer's count 3 — follow the same rule: the spy `_spy_on_load_job` in
`tests/test_data_paths.py` is installed on `packages.orchestration.pingpong_job` as both
`load_job_plan` and `require_job_plan`; `tests/ui_server/test_command_dispatch.py` counts saves
through `pingpong_job.save_job_plan`; `tests/cli/test_patch_cmd.py` sets `save_job_plan` on the
module it patches.
O3 THE STORAGE MODULE. In `tests/orchestration/test_loop_run.py` and `tests/cli/test_loop_cmd.py`
the imported `storage` module becomes `pingpong_job`, and the attribute reads of
`load_job_plan`, `save_job_plan` and `list_job_plans_safe` off it — the reviewer's count 9 —
read them off `pingpong_job`.
O4 THE GUARD. In `tests/orchestration/test_job_plan_state_reads.py`, `JOB_PLAN_LOADER` becomes
`JOB_PLAN_LOADERS = ("load_job_plan", "require_job_plan")`, the finder binds a local from a call
of either, the module docstring's sentence naming the loader names both, and
`test_the_scan_sees_a_retired_read_when_one_is_there` is parametrized over `JOB_PLAN_LOADERS`,
planting its source with each.

## SPEC C — the carriers, at C4

The VERBATIM stdout of `git diff` in EDIT, against its index as constraint 8 stages it, is cut at
`diff --git` lines into consecutive parts in its own order, each part as many whole file diffs as
fit in 440 lines, a new part starting only when the next file diff would not fit. Part `<k>` is
`.agent/authored/f275-r93-overlay-<k>.md`: prose naming its base `844a7f21`, that the flipped
tree is built as G4 of `.agent/authored/f275-r93.md` orders, that the parts form the FOURTH
overlay and apply after `.agent/authored/f275-r92-overlay-4.md` in `<k>` order, and how to apply
each — extract the fence, `git apply --check`, then `git apply`; then exactly ONE fence, a line of
three backticks and `diff`, the part, and a line of three backticks; nothing after it but one
newline. Joined in `<k>` order, the fences equal the whole diff byte for byte.

## Constraints

1. NO SLICE IS EDITED. PLAN93, RECORD93, SLIPS93 and DEC93 land byte for byte; a discrepancy
   inside one is DECLARED, never repaired.
2. SPEC O and SPEC C are the worker's OWN work. The reviewer's scratch `.remedy-wt/r90/` through
   `.remedy-wt/r93/` is not opened.
3. READ `.agent/STOP` before C0a and before C6, with real exit codes. If it appears, finish the
   commit in hand, write the handoff and end.
4. Every commit stages EXACTLY ONE path and stays under 500 insertions.
5. No `.py` file under `.agent/`; scratch under `.remedy-wt/r93w/`, uncommitted; every scratch
   output path absolute.
6. No landed record is rewritten: the `.agent/live_review.md`, `.agent/prose_slips.md` and
   `.agent/decisions.md` commits are APPENDS with a ZERO deletion column.
7. No `gh`, no `remedy`, no pull request, no branch created or deleted, no merge, NEVER a
   force-push, no history rewrite.
8. THREE worktrees, each `git worktree add --detach` at `844a7f21` under `.remedy-wt/r93w/`:
   EDIT, CONTROL and OVERLAY. In each: the transform as G4 orders, `git add -A`, then for each of
   `.agent/authored/f275-r90-overlay.md`, `.agent/authored/f275-r91-overlay.md` and
   `.agent/authored/f275-r92-overlay-1.md` through `-4.md`, in that order, the fence of the
   COMMITTED carrier applied with `git apply --check` then `git apply`, and `git add -A` after
   each overlay. Only EDIT receives SPEC O, and any test may run there while it is made; before
   the diff is taken its `git diff --name-only` lists only paths SPEC O edited. Only OVERLAY
   receives the C4 carriers. All three are REMOVED AND PRUNED before C5, without `--force`. The
   generator's trees are plain directories.
9. THE BLOCK'S OWN SIZE, measured on its final bytes: 271 lines TOTAL and 198 lines of
   PROSE, against the caps of 490 and 400.
10. GATE ORDER. G4's setup — the generator, the three worktrees, the chain — runs after C3 and
    before the first C4 commit, because the carriers are cut from EDIT; G4's readings, G5 and G6
    are taken after the last C4 commit and strictly before C5, per item 31 of §3. DEC93's
    measured figures, 53, three and nine, are G4's; its 80 is the round 92 record's; DEC93
    quotes no G5 or G6 reading. G1, G2, G3, G7 and G8 run at C5. No gate runs after C6; C6's
    own numbers are the reviewer's.
11. A RED G5 IS A STOP. If G5 finds a node bad only in OVERLAY, the worker commits nothing further
    after C4 except the handback, which lists every such node with its last `E   ` line.

## Done when — the gates, each run for real and its exit code recorded

G1 TRANSPORT, BUDGET, SLICES. `.agent/authored/f275-r93.md` at C0a against the block as received,
by `cmp`; `.agent/last_block.md` at C0b byte-identical to the COMMITTED C0a blob. Extract the
slices by their markers, report how many were FOUND, check each against its BEGIN-marker
sha256, and re-measure TOTAL and PROSE against constraint 9.

G2 THE PLAN. `.agent/plan.md` at C1 byte-identical to PLAN93 from the COMMITTED C0a blob; at
most 50 lines; one `## Goal` and one `## Next Steps`.

G3 THE RECORD. For the appends at C2 into `.agent/live_review.md` and at C5 into
`.agent/decisions.md`, FULL FORENSICS: the pre-commit blob read with `git show` at the commit's
PARENT, its length printed — 1138457 and 1288099 — READER A with the arithmetic printed; READER B
over the file's LAST N blank-line units against the slice's N paragraphs IN ORDER, N counted by
the script; a letter flipped in the FIRST appended paragraph REJECTED by both readers; deletion
column 0. `.agent/prose_slips.md` at C3 equals its 300925-byte pre-commit blob followed by
exactly SLIPS93. Derive the ledger's `Gate:` header pattern from the file, report how many heads
it matches, and that RECORD93's header matches it and duplicates none.

G4 THE TREES, THE CHAIN AND THE CARRIERS, set up and read per constraint 10. The generator trees
and run exactly as G4 of `.agent/authored/f275-r90.md` orders, the pinned digests checked first,
with the readings that block states; the transform in each worktree reading 2183 resolving and 0
not, 264 files, 6097 rewrites and 0 broken; every earlier overlay applying with exit 0 in each.
Then: (a) the fences extracted from the COMMITTED C4 blobs: report the part count and each part's
line count, each at most 440; joined in `<k>` order they equal EDIT's diff; in OVERLAY each
applies with `git apply --check` and `git apply` exit 0, in order; `git diff --name-only` there,
against the index constraint 8 staged, lists exactly EDIT's paths, each byte-identical to EDIT's,
every one under `tests/`; report the list. (b) With `ast` over every `.py` under `tests/`, in
CONTROL and in OVERLAY: O1's string constants 53 and 0; O2's `setattr` calls, counted as calls of
an attribute named `setattr` whose second argument is a string constant among the five names, 3
and 0; attribute reads off a bare name `storage` whose attribute is `load_job_plan`,
`save_job_plan`, `list_job_plans_safe`, `list_job_plans`, `load_job_plan_safe` or
`require_job_plan`, 9 and 0. `def test_` counts equal per changed test file. (c) `ruff check
--output-format concise --select F401,F811,F821` over the changed paths in OVERLAY exits 0; and
`ruff check --output-format concise --stdin-filename <path> -`, run from inside each worktree,
over every changed path, rows compared as a MULTISET of `<path>: <code> <message>` with line and
column DROPPED: added 0.

G5 THE FULL SUITE IN FRESH FLIPPED TREES, per constraint 10, CONTROL first and OVERLAY second,
serially. Each is its worktree's FIRST full run, `apps/ui/node_modules` and `apps/ui/dist`
reported absent before it. `cwd` the worktree; `PYTHONPATH`, `REMEDY_PROJECT` and
`REMEDY_DATA_DIR` removed; `PYTHONDONTWRITEBYTECODE=1`;
`packages.orchestration.pingpong_job.__file__` printed and inside the worktree;
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`. A bad node is the
text after `FAILED ` or `ERROR ` up to the first ` - ` or the line's end. The reviewer measured
CONTROL `418 failed, 17990 passed, 29 skipped, 1 warning, 31 errors`, 449 bad nodes. REPORT
OVERLAY's tally and bad-node count. Bad only in OVERLAY: MUST be 0, per constraint 11. REPORT
the fixed nodes' count per test file.

G6 THE PROBES, per constraint 10, in OVERLAY after G5; `__pycache__` purged before each run;
G5's environment; flags `-q -p no:randomly -p no:cacheprovider --tb=short -rfE`. For each
mutation, the bytes it replaces counted in the file as 1 first, report the tally and the node ids
bad only under it, then restore and confirm the file's bytes. P1 over
`tests/orchestration/test_job_plan_state_reads.py`: unmutated; M1 the finder's membership test
narrowed to the first loader of `JOB_PLAN_LOADERS` alone, where exactly the planted case
parametrized with `require_job_plan` MUST go bad. P2 over
`tests/cli/test_change_proof_cli.py::test_handler_path_traversal_rejected`: unmutated; M2 that
test's patch target back to `apps.cli.commands.change.load_job`, where that node MUST go bad.

G7 TREE, CANARY, LINT, PATH SET, OPEN SET, at C5. `git status --porcelain` prints `''`;
`git worktree list` one row; `git diff --name-only dbab6b13 C5 -- packages apps tests docs
scripts` empty; the canary `python3 -B -m pytest tests/cli/test_golden_path.py -q` exit 0, 42;
`ruff check . --output-format concise` rows as a MULTISET at `dbab6b13`, read from a
`git archive` tree, and at C5, difference empty, 26 at `dbab6b13`. The changed-path set of
`dbab6b13`..C5 against the Bundle's paths MINUS `.agent/handoff.md`, MISSING and EXTRA by name.
The open set BY DISTINCT ID at `dbab6b13` and at C5: 88 at both, membership identical;
`R-0809`, `R-0880` and `R-0883` open.

G8 THE INSERTION CAP over `dbab6b13`..C5: one row per commit with insertions, deletions and
staged path count, and the number of commits reaching 500 insertions.

Handback: `.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 31 of feature F275 · round 93 · rounds so far 93`; the Commits table read from
`git show --numstat` and compared cell by cell against G8, C6's row carrying no numbers and
saying why; one Verification line per gate with its REAL exit code; External actions;
Authored-text proofs; Item-status; Deviations; `## Next` stating `Operator questions open: 1`.
NO SCOPE REPORT AND NO SESSION-LIMIT BANNER, by amendment amend0911-f275-to-scope.

── SLICE PLAN93 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN93 sha256=ea5fe5ca6959892671f8d49c8d3bd425027592f37c689e9609567a6be49e06d2
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

ROUND 93 ADDS THE FLIP'S FOURTH OVERLAY, on top of the first three, under DECISION F275 D64's
method. It touches tests only: a test double installed by name, or a unified function read off
the classic `storage` module, is pointed at the name the flipped code really calls, and the
guard against reading the retired `status` off a loaded plan also covers `require_job_plan`,
which the third overlay put out of its reach. The diff is carried in consecutive carriers. No
path under `packages/`, `apps/` or `tests/` moves. The round books the round 92 verdict and its
two prose slips.

## Next Steps

1. MORE OVERLAYS, one residue group each, every one applied on top of those before it: task
   records built without an id, which the classic `Task` minted by default; handlers resolving
   a minted id no store holds; the pydantic calls made on the unified records, such as
   `TaskEntry.model_validate` and `JobPlan.model_dump_json`; the classic `Task` constructions
   that pass `acceptance_checks`; what is left of the classic runner under `job resume`; and
   duck-typed test doubles, including the `_FakeJob` behind the ruled site at
   `packages/orchestration/project_registry.py:856`.
2. THE FLIP: the transform, then every overlay in round order, landed as a series of commits
   each under the 500-insertion cap inside one round, carrying DECISION F275 D48's obligations,
   unless the operator allows one more oversized commit.
3. Then the classic store, with the which-store branches and adapters the overlays leave
   unreached, then the closure sequence.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20
  sessions and 60 rounds without a replacement, so this feature closes only at full scope.
- THE FLIP IS NOT CLOSE: several hundred test nodes still fail in the flipped tree.
- AN OVERLAY IS A DIFF AGAINST A FIXED TREE: it holds only while the production tree stays at
  `844a7f21`, and it depends on the generator and transform staying reproducible from round
  77's two scratch JSON files.
- ONE ROUTED LOAD IS REACHED BY NO TEST until `R-0883` is repaired.
- The open set is 88 by distinct id at this round's base, with `R-0809`, `R-0880` and `R-0883`
  open. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END PLAN93

── SLICE RECORD93 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD93 sha256=561df7c6c534cddb3d280023566a1ccf3542d5545b1a15cbd0be3a58a7954545

Gate: F275 R92 — the F275 round 92 entry. VERDICT PASS. Written by the planner and reviewer of session 31 after reading the committed range `9d99ffb2`..`dbab6b13` and RE-DERIVING EVERY GATE AND EVERY PROBE INDEPENDENTLY; the worker's report and its transcripts were evidence for no line below. It is booked here by the FIRST SUBSTANTIVE COMMIT of round 93 that writes the record, per operator amendment amend0827-process-diet rule 1. The round moved no path under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/`; its production code is the diff carried in `.agent/authored/f275-r92-overlay-1.md` through `-4.md`.

WHAT THE TRANSPORT PROOF COVERS, per item 37 of §3. The committed `.agent/authored/f275-r92.md` blob was identical to the reviewer's own original at 25687 bytes, `.agent/last_block.md` equalled it from its own commit through `dbab6b13`, and all four slices matched their BEGIN-marker digests; `.agent/plan.md` equalled PLAN92. The three appends were exact under reader A — 1134899 plus 3558 into the review record, 300420 plus 505 into the prose slips and 1284587 plus 3512 into the decisions — with reader B holding at N counted from each slice as 4, 1 and 7, and a letter flipped in each FIRST appended paragraph rejected by both readers. Every commit staged one path, and the largest was the third carrier at 467 insertions. The four fences read 327, 422, 431 and 146 lines, which is exactly what cutting the joined diff greedily at 440 lines gives.

THE OVERLAY HOLDS UNDER THE REVIEWER'S OWN RE-RUN. The reviewer transformed a worktree at `844a7f21` from its own generator run, applied and staged the committed first and second overlays, and applied the four committed fences in order: every `git apply --check` and `git apply` exited 0 and 36 paths changed, three of them under `tests/`. Under `packages/` and `apps/`, calls inside a `try` whose handler names `JobNotFoundError` read `require_job_plan` 16 and 64 and the alias `_load_job` 1, with no `load_job_plan` left there, and neither `revert_repository_apply` nor `execute_test_run` holds a `UUID` parse. That worktree's first full run read 418 failed, 17990 passed, 29 skipped and 31 errors, 449 bad nodes, against 516 in the reviewer's fresh run of the chain before it: 67 fixed and none newly bad. In the same worktree `tests/orchestration/test_unified_store_parity.py` read 21 passed; deleting the `JobStoreError` branch made exactly `test_h3_an_unreadable_record_raises_job_store_error` bad, and returning `None` for an absent record made exactly `test_h2_an_absent_record_raises_job_not_found_naming_the_id_asked_for` bad. The two prefix nodes passed unmutated there, and dropping the id from the decision id or from the file name made the escalation node or the workspace node bad; in the reviewer's dry-run tree without the two fixture edits both mutations left both nodes green. In the primary checkout at `dbab6b13` the canary read 42 and `ruff check .` read 26 rows, a multiset equal to that of `844a7f21`, whose production tree it shares; the open set stayed 88 with identical membership, `R-0809`, `R-0880` and `R-0883` open.

A GUARD LEFT BEHIND, WHICH ROUND 93 WIDENS. `tests/orchestration/test_job_plan_state_reads.py` looks for reads of the retired `status` only off locals bound from `load_job_plan`, so the loads the third overlay routes through `require_job_plan` are outside its reach; the worker named it. The carrier holds the gap, not a path under `tests/`, so it is not a finding: round 93's overlay widens the guard and proves the widening red-able.
END RECORD93

── SLICE SLIPS93 ── target `.agent/prose_slips.md` ── APPEND ──
BEGIN SLIPS93 sha256=73b679069ee3df9d476631a6e75f68833467928bdabee229e62326367988a0fa

2026-09-13 · F275 R92 · G4(b) of the round 92 block counted calls in a `try` "with a handler naming `JobNotFoundError`", while the reviewer's own count matched any handler whose type contains that text, which includes the alias `_JobNotFoundError`; with an exact name the alias site reads 0, and the worker declared the reading it used. THE RULE THAT FOLLOWS: a structural count states its match rule — exact name or containment — in the words of the scan that produced the figure.

2026-09-13 · F275 R92 · The round 92 block ordered G4 "at the last C4 commit" while the same gate builds the flipped worktrees the C4 carriers are cut from, so its first half can only run before C4; the worker built them after C3 and declared it. THE RULE THAT FOLLOWS: a gate whose setup produces the input of a commit names two points, the one its setup runs at and the one its readings are taken at.
END SLIPS93

── SLICE DEC93 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC93 sha256=e527ea2d72c8acbae0331aa92b268bd5fb1fa6b366ce9020b57db49507bdd690

## DECISION F275 D67 (2026-09-13, F275 round 93) — the fourth overlay: a test double installed by name follows the name the flipped code calls, a unified function is read off the module that defines it, and the state-read guard covers the raising loader

CONTEXT. With three overlays applied to the flipped tree at `844a7f21`, tests still install doubles by the classic store's names: 53 dotted `patch` targets under `tests/` end in `load_job`, `save_job` or `list_jobs_safe`, three `monkeypatch.setattr` calls name `load_job` or `save_job`, and nine calls read a unified function such as `load_job_plan` off the classic `storage` module, a module whose attribute the transform renamed and which defines no such function. A double named for a function the flipped code no longer calls intercepts nothing, so the test runs the real loader against a job it never saved, or fails to install at all. And `tests/orchestration/test_job_plan_state_reads.py` finds reads of the retired `status` only off locals bound from `load_job_plan`, while the third overlay binds 80 loads from `require_job_plan`.

CHOSEN, FIRST: A DOUBLE FOLLOWS THE CALL. Each dotted target and each `setattr` names the function the code under test calls in the flipped tree — `require_job_plan` where the third overlay routed that call, `load_job_plan` or `save_job_plan` or `list_job_plans_safe` otherwise — on the module whose binding that code reads at call time; a unified function is read off `packages.orchestration.pingpong_job`. ALTERNATIVES: aliases of the unified names on the classic `storage` module, rejected because they are a compatibility reader AGENTS.md Scope Control forbids and the classic store is deleted after the flip; rewriting those tests onto saved fixtures, rejected as a change of what they test rather than of the name they reach.

CHOSEN, SECOND: THE GUARD COVERS BOTH LOADERS. `JOB_PLAN_LOADERS` names `load_job_plan` and `require_job_plan`, and the planted-source test runs once per loader, so narrowing the finder back to one loader turns the planted `require_job_plan` case red.

CONSEQUENCE. The tests only move their doubles; no assertion changes. What the overlay fixes, and that it newly breaks nothing, is measured by the gates of round 93's block and recorded in the round 93 ledger entry by the round that books its verdict. `R-0809`, `R-0880` and `R-0883` stay open, and no finding is registered or resolved.

HOW TO REVERSE. Delete the round 93 overlay carriers under `.agent/authored/` and this paragraph block; the doubles then name functions the flipped code does not call again, and the guard reads one loader.
END DEC93

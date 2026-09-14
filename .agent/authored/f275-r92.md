── STEP T003 — F275 — ROUND 92 ──
Goal: Commit the flip's third OVERLAY, applied after the first two to the flipped tree at
`844a7f21`: a raising loader on the unified store that every load catching `JobNotFoundError`
calls, the last two `UUID(...)` parses of a loaded id routed through `normalize_job_id`, and the
repair of the two prefix assertions round 91 left vacuous, measured by the full suite in fresh
flipped trees.

Base commit: `9d99ffb2`. The chain's base stays `844a7f21`, per DECISION F275 D64. Round type:
SPLIT. No path under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/` changes; the overlay
is production code carried in a diff, so G4 to G6 give it full forensics and mutation probes.

THE FRAME RULE, per item 37 of §3, stated as the property MEASURED over the final bytes: NO LINE
of this block is a run of a single repeated character, and every box-drawing rule inside the
STEP and SLICE header lines is exactly two characters long.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f275-r92.md`             the block, saved verbatim
C0b `.agent/last_block.md`                    mirrored FROM THE COMMITTED C0a BLOB
C1  `.agent/plan.md`                          slice PLAN92, a full replacement
C2  `.agent/live_review.md`                   slice RECORD92 appended, the round 91 verdict
C3  `.agent/prose_slips.md`                   slice SLIPS92 appended
C4  `.agent/authored/f275-r92-overlay-<k>.md` the overlay carriers of SPEC C, ONE COMMIT EACH
C5  `.agent/decisions.md`                     slice DEC92 appended
C6  `.agent/handoff.md`                       the handback

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3.

## Change — exactly these paths and no others

The Bundle's paths, `<k>` running from 1 over the carriers SPEC C produces.

## SPEC O — the edits, made in the EDIT worktree of constraint 8 on top of the second overlay

O1 `packages/orchestration/pingpong_job.py`: directly after `load_job_plan_safe`, a function
`require_job_plan(job_id: str, root: Path | None = None) -> JobPlan` with a docstring naming the
contract. It returns the plan `load_job_plan_safe(job_id, root)` reads; when that plan is `None`
it raises `JobStoreError` if the reader reported the record degraded, and otherwise
`JobNotFoundError(job_id)`; both classes are imported from `packages.orchestration.storage`
INSIDE the function. Nothing else in the file changes.
O2 Under `packages/` and `apps/`, every call of `load_job_plan` by that bare name that lies in
the body of a `try` with a handler whose type names `JobNotFoundError` calls `require_job_plan`
instead — the reviewer's count 81, 16 under `packages/` and 65 under `apps/` — and in
`revert_repository_apply` of `packages/orchestration/repository_snapshot.py` the import
`load_job_plan as _load_job` imports `require_job_plan as _load_job`. An import of
`load_job_plan` that the rename leaves unused imports `require_job_plan` in its place; one still
used also imports `require_job_plan`. In `apps/cli/commands/job_context_cmd.py` the rename leaves
a second call of the same id inside `if job is None:`; that `if` and its body, the now duplicate
`pingpong_job` import in that function, and the comment sentence beginning `WHY the unified
record is read` are deleted.
O3 In `revert_repository_apply`, `_UUID(job_id)` becomes `normalize_job_id(job_id)`, imported
from `packages.orchestration.data_paths` in that function, and the `_UUID` import is deleted; in
`execute_test_run` of `packages/orchestration/test_execution_service.py`,
`UUID(request.job_id)` becomes `normalize_job_id(request.job_id)`, imported at module level.
O4 `tests/orchestration/test_unified_store_parity.py` gains a class after
`TestCorruptionVisibilityOfOneRecord` with three tests of `require_job_plan` under `tmp_path`:
an absent record raises `JobNotFoundError` whose `job_id` is the id asked for; an unreadable
record written by `_corrupt` raises `JobStoreError`; a saved record comes back equal to what
`load_job_plan` reads.
O5 THE REPAIR. `make_job` in `tests/orchestration/test_escalation.py` passes
`task_id=f"T{i + 1:03d}"` to each `TaskEntry`; `_make_planned_job` in `tests/test_workspace.py`
passes `task_id="T001"`. Nothing else under `tests/` changes.

## SPEC C — the carriers, at C4

The VERBATIM stdout of `git diff` in EDIT, against its index as constraint 8 stages it, is cut at
`diff --git` lines into consecutive parts in its own order, each part as many whole file diffs as
fit in 440 lines, a new part starting only when the next file diff would not fit. Part `<k>` is
`.agent/authored/f275-r92-overlay-<k>.md`: prose naming its base `844a7f21`, that the flipped
tree is built as G4 of `.agent/authored/f275-r92.md` orders, that the parts form the THIRD
overlay and apply after `.agent/authored/f275-r91-overlay.md` in `<k>` order, and how to apply
each — extract the fence, `git apply --check`, then `git apply`; then exactly ONE fence, a line of
three backticks and `diff`, the part, and a line of three backticks; nothing after it but one
newline. Joined in `<k>` order, the fences equal the whole diff byte for byte.

## Constraints

1. NO SLICE IS EDITED. PLAN92, RECORD92, SLIPS92 and DEC92 land byte for byte; a discrepancy
   inside one is DECLARED, never repaired.
2. SPEC O and SPEC C are the worker's OWN work. The reviewer's scratch `.remedy-wt/r90/`,
   `.remedy-wt/r91/` and `.remedy-wt/r92/` are not opened.
3. READ `.agent/STOP` before C0a and before C6, with real exit codes. If it appears, finish the
   commit in hand, write the handoff and end.
4. Every commit stages EXACTLY ONE path and stays under 500 insertions.
5. No `.py` file under `.agent/`; scratch under `.remedy-wt/r92w/`, uncommitted; every scratch
   output path absolute.
6. No landed record is rewritten: the `.agent/live_review.md`, `.agent/prose_slips.md` and
   `.agent/decisions.md` commits are APPENDS with a ZERO deletion column.
7. No `gh`, no `remedy`, no pull request, no branch created or deleted, no merge, NEVER a
   force-push, no history rewrite.
8. THREE worktrees, each `git worktree add --detach` at `844a7f21` under `.remedy-wt/r92w/`:
   EDIT, CONTROL and OVERLAY. In each: the transform as G4 orders, `git add -A`, then for each of
   `.agent/authored/f275-r90-overlay.md` and `.agent/authored/f275-r91-overlay.md` in that order
   the fence of the COMMITTED carrier applied with `git apply --check` then `git apply`, and
   `git add -A`. Only EDIT receives SPEC O, and any test may run there while it is made; before
   the diff is taken its `git diff --name-only` lists only paths SPEC O edited. Only OVERLAY
   receives the C4 carriers. All three are REMOVED AND PRUNED before C5, without `--force`. The
   generator's trees are plain directories.
9. THE BLOCK'S OWN SIZE, measured on its final bytes: 284 lines TOTAL and 211 lines of
   PROSE, against the caps of 490 and 400.
10. GATE ORDER. G4, G5 and G6 run at the last C4 commit, strictly before C5, per item 31 of §3.
    DEC92's one measured figure, 81, is G4's; its other numerals — the ids `T001` and `T002`,
    and how many exceptions, parses, assertions and loader outcomes it names — are SPEC O's or
    the round 91 record's; DEC92 quotes no G5 or G6 reading. G1, G2, G3, G7 and G8 run at C5. No
    gate runs after C6; C6's own numbers are the reviewer's.
11. A RED G5 IS A STOP. If G5 finds a node bad only in OVERLAY, the worker commits nothing further
    after C4 except the handback, which lists every such node with its last `E   ` line.

## Done when — the gates, each run for real and its exit code recorded

G1 TRANSPORT, BUDGET, SLICES. `.agent/authored/f275-r92.md` at C0a against the block as received,
by `cmp`; `.agent/last_block.md` at C0b byte-identical to the COMMITTED C0a blob. Extract the
slices by their markers, report how many were FOUND, check each against its BEGIN-marker
sha256, and re-measure TOTAL and PROSE against constraint 9.

G2 THE PLAN. `.agent/plan.md` at C1 byte-identical to PLAN92 from the COMMITTED C0a blob; at
most 50 lines; one `## Goal` and one `## Next Steps`.

G3 THE RECORD. For the appends at C2 into `.agent/live_review.md` and at C5 into
`.agent/decisions.md`, FULL FORENSICS: the pre-commit blob read with `git show` at the commit's
PARENT, its length printed — 1134899 and 1284587 — READER A with the arithmetic printed; READER B
over the file's LAST N blank-line units against the slice's N paragraphs IN ORDER, N counted by
the script; a letter flipped in the FIRST appended paragraph REJECTED by both readers; deletion
column 0. `.agent/prose_slips.md` at C3 equals its 300420-byte pre-commit blob followed by
exactly SLIPS92. Derive the ledger's `Gate:` header pattern from the file, report how many heads
it matches, and that RECORD92's header matches it and duplicates none.

G4 THE TREES, THE CHAIN AND THE CARRIERS, at the last C4 commit. The generator trees and run
exactly as G4 of `.agent/authored/f275-r90.md` orders, the pinned digests checked first, with
the readings that block states; the transform in each worktree reading 2183 resolving and 0 not,
264 files, 6097 rewrites and 0 broken; both earlier overlays applying with exit 0 in each. Then:
(a) the fences extracted from the COMMITTED C4 blobs: report the part count and each part's
line count, each at most 440; joined in `<k>` order they equal EDIT's diff; in OVERLAY each
applies with `git apply --check` and `git apply` exit 0, in order; `git diff --name-only` there,
against the index constraint 8 staged, lists exactly EDIT's paths, each byte-identical to EDIT's;
report the list; under `tests/` it holds exactly `tests/orchestration/test_escalation.py`,
`tests/orchestration/test_unified_store_parity.py` and `tests/test_workspace.py`. (b) With `ast`,
under `packages/` and `apps/`, calls by the bare names `load_job_plan`, `require_job_plan` and
`_load_job` in the body of a `try` with a handler naming `JobNotFoundError`, per name and per
top directory, in CONTROL and in OVERLAY: the reviewer read `load_job_plan` 16 and 65 and
`_load_job` 1 and 0 in CONTROL, and `require_job_plan` 16 and 64 and `_load_job` 1 and 0 in
OVERLAY, with no `load_job_plan` left there. In `revert_repository_apply` the calls named `_UUID`
1 and 0 and `normalize_job_id` 0 and 1; in `execute_test_run` `UUID` 1 and 0 and
`normalize_job_id` 0 and 1; `def require_job_plan` 0 and 1, in `pingpong_job.py`. `def test_`
counts per changed test file: equal, except `test_unified_store_parity.py` 3 more. (c) `ruff check
--output-format concise --select F401,F811,F821` over the changed paths in OVERLAY exits 0; and
`ruff check --output-format concise --stdin-filename <path> -`, run from inside each worktree,
over every changed path, rows compared as a MULTISET of `<path>: <code> <message>` with line and
column DROPPED: added 0.

G5 THE FULL SUITE IN FRESH FLIPPED TREES, at the last C4 commit, CONTROL first and OVERLAY
second, serially. Each is its worktree's FIRST full run, `apps/ui/node_modules` and
`apps/ui/dist` reported absent before it. `cwd` the worktree; `PYTHONPATH`, `REMEDY_PROJECT` and
`REMEDY_DATA_DIR` removed; `PYTHONDONTWRITEBYTECODE=1`;
`packages.orchestration.pingpong_job.__file__` printed and inside the worktree;
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`. A bad node is the
text after `FAILED ` or `ERROR ` up to the first ` - ` or the line's end. The reviewer measured
CONTROL `485 failed, 17920 passed, 29 skipped, 1 warning, 31 errors`, 516 bad nodes. REPORT
OVERLAY's tally and bad-node count. Bad only in OVERLAY: MUST be 0, per constraint 11. REPORT
the fixed nodes' count per test file.

G6 THE PROBES, at the last C4 commit, in OVERLAY after G5 and then in CONTROL; `__pycache__`
purged before each run; G5's environment; flags `-q -p no:randomly -p no:cacheprovider
--tb=short -rfE`. For each mutation below, the bytes it replaces counted in the file as 1 first,
report the tally and the node ids bad only under it, then restore and confirm the file's bytes.
P1, in OVERLAY over `tests/orchestration/test_unified_store_parity.py`: unmutated; M1 the
`raise JobStoreError(...)` statement and the `if` guarding it deleted, where exactly the test
of an unreadable record MUST go bad; M2 the `raise JobNotFoundError(job_id)` statement becomes
`return None`, where exactly the test of an absent record MUST go bad. P2, over the two nodes
`tests/orchestration/test_escalation.py::TestEnqueue::test_the_decision_id_is_task_scoped_and_prefixed`
and `tests/test_workspace.py::test_materialize_filename_includes_short_task_id`, in OVERLAY and
then in CONTROL: unmutated; M3 in `_next_decision_id` of `packages/orchestration/escalation.py`
the line `        task_hex = task_str[:8]` becomes `        task_hex = "x"`; M4 in
`materialize_task_output` of `packages/orchestration/task_runner.py` the line
`    short_id = str(result.task_id)[:8]` becomes `    short_id = "x"`. Under M3 the escalation
node and under M4 the workspace node MUST go bad in OVERLAY and MUST stay green in CONTROL.

G7 TREE, CANARY, LINT, PATH SET, OPEN SET, at C5. `git status --porcelain` prints `''`;
`git worktree list` one row; `git diff --name-only 9d99ffb2 C5 -- packages apps tests docs
scripts` empty; the canary `python3 -B -m pytest tests/cli/test_golden_path.py -q` exit 0, 42;
`ruff check . --output-format concise` rows as a MULTISET at `9d99ffb2`, read from a
`git archive` tree, and at C5, difference empty, 26 at `9d99ffb2`. The changed-path set of
`9d99ffb2`..C5 against the Bundle's paths MINUS `.agent/handoff.md`, MISSING and EXTRA by name.
The open set BY DISTINCT ID at `9d99ffb2` and at C5: 88 at both, membership identical;
`R-0809`, `R-0880` and `R-0883` open.

G8 THE INSERTION CAP over `9d99ffb2`..C5: one row per commit with insertions, deletions and
staged path count, and the number of commits reaching 500 insertions.

Handback: `.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 31 of feature F275 · round 92 · rounds so far 92`; the Commits table read from
`git show --numstat` and compared cell by cell against G8, C6's row carrying no numbers and
saying why; one Verification line per gate with its REAL exit code; External actions;
Authored-text proofs; Item-status; Deviations; `## Next` stating `Operator questions open: 1`.
NO SCOPE REPORT AND NO SESSION-LIMIT BANNER, by amendment amend0911-f275-to-scope.

── SLICE PLAN92 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN92 sha256=537d34fe0163a15d6e62377b42ecded77f9175b09b081f5ab4aa98a7f2a979d4
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

ROUND 92 ADDS THE FLIP'S THIRD OVERLAY, on top of the first two, under DECISION F275 D64's
method. The unified store gains `require_job_plan`, which raises what the classic loader raised,
and every load that catches `JobNotFoundError` calls it; the last two `UUID(...)` parses of a
loaded id take `normalize_job_id`; and the two prefix assertions round 91 left comparing an
empty task id compare a real one again. The diff is carried in several consecutive carriers.
No path under `packages/`, `apps/` or `tests/` moves. The round books the round 91 verdict and
its prose slip.

## Next Steps

1. MORE OVERLAYS, one residue group each, every one applied on top of those before it: task
   records built without an id, which the classic `Task` minted by default; the pydantic calls
   made on the unified records, such as `TaskEntry.model_validate` and
   `JobPlan.model_dump_json`; the classic `Task` constructions that pass `acceptance_checks`;
   test doubles patched in by a name the flip renamed; what is left of the classic runner
   under `job resume`; and the duck-typed test doubles, including the `_FakeJob` behind the
   ruled site at `packages/orchestration/project_registry.py:856`.
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
END PLAN92

── SLICE RECORD92 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD92 sha256=734ca7f3409fcd62731f639121419bdd10a264a804674b3b8f9ed90db54d2dba

Gate: F275 R91 — the F275 round 91 entry. VERDICT PASS. Written by the planner and reviewer of session 31 after reading the committed range `1f7a52f9`..`9d99ffb2` and RE-DERIVING EVERY GATE AND THE PROBE INDEPENDENTLY; the worker's report and its transcripts were evidence for no line below. It is booked here by the FIRST SUBSTANTIVE COMMIT of round 92 that writes the record, per operator amendment amend0827-process-diet rule 1. The round moved no path under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/`; its production code is the diff inside `.agent/authored/f275-r91-overlay.md`.

WHAT THE TRANSPORT PROOF COVERS, per item 37 of §3. The committed `.agent/authored/f275-r91.md` blob was identical to the reviewer's own original at 23060 bytes, `.agent/last_block.md` equalled it from its own commit through `9d99ffb2`, and all four slices matched their BEGIN-marker digests; `.agent/plan.md` equalled PLAN91. The three appends were exact under reader A — 1131427 plus 3472 into the review record, 299259 plus 1161 into the prose slips and 1281959 plus 2628 into the decisions — with reader B holding at N counted from each slice as 4, 3 and 5, and a letter flipped in each FIRST appended paragraph rejected by both readers. Every commit staged one path, and the largest was the carrier at 412 insertions.

THE OVERLAY HOLDS UNDER THE REVIEWER'S OWN RE-RUN. The reviewer transformed a worktree at `844a7f21` from its own generator run, staged it, applied the committed first overlay and staged again, then applied the fence extracted from the committed round 91 carrier: `git apply --check` and `git apply` exited 0 and twelve paths changed, `packages/orchestration/task_runner.py`, `packages/orchestration/verifier.py` and `apps/cli/commands/job.py` among them and nine under `tests/`. `str(a.id) == ` read 2, 1 and 2 in those three files, the string append 1 and the raw append 0. That worktree's first full run read 485 failed, 17920 passed, 29 skipped and 31 errors, 516 bad nodes, against 560 in the reviewer's fresh run of the chain before it: 44 fixed and none newly bad, 42 of them among the 58 nodes whose section named a `UUID` in a JSON dump or a path join. In the same worktree the three-file selection read 1 failed and 136 passed unmutated; appending the raw artifact id again made 16 nodes newly bad in `tests/test_task_runner.py` and `tests/test_verifier.py`, and comparing `a.id` again in `verify_task_output` made 24 newly bad in `tests/test_verifier.py`. In the primary checkout at `9d99ffb2` the canary read 42 and `ruff check .` read 26 rows, a multiset equal to that of `844a7f21`, whose production tree it shares; the open set stayed 88 with identical membership, `R-0809`, `R-0880` and `R-0883` open.

THE OTHER TWO FIXES ARE VACUOUS, AND ROUND 92 OWES THEIR REPAIR. They are `TestEnqueue::test_the_decision_id_is_task_scoped_and_prefixed` in `tests/orchestration/test_escalation.py` and `test_materialize_filename_includes_short_task_id` in `tests/test_workspace.py`. SPEC O2 of the round 91 block turned each `task_id.hex[:8]` into `task_id[:8]`, and in the flipped tree both fixtures build a `TaskEntry` with no id, so each assertion asks whether the empty string occurs in a name, which it always does; the reviewer measured the escalation fixture's task id as the empty string, and the worker declared both. The defect sits in the carrier, not under `tests/`, so it is not a finding: the next overlay repairs both fixtures and proves each assertion red under a mutation that the tree before it leaves green.
END RECORD92

── SLICE SLIPS92 ── target `.agent/prose_slips.md` ── APPEND ──
BEGIN SLIPS92 sha256=1fe7609cc1c9ec87f5b9f425587f6e03062ee07ef10f0da1741d84bbf2b3744f

2026-09-13 · F275 R91 · SPEC O2 of the round 91 block ordered a prefix derived with `.hex` from a record field rewritten to the string form, without reading what the flipped fixtures put in that field; two fixtures build a task with no id, so the two rewritten assertions became true for every input. THE RULE THAT FOLLOWS: an ordered test rewrite is read against the fixture values it will compare, and a rewrite that can make an assertion hold for every input is ordered together with a red control.
END SLIPS92

── SLICE DEC92 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC92 sha256=dd523534464619eb8ff689fb28f9c1437937f3fab4b2a2f08f3f15d155b2b9ea

## DECISION F275 D66 (2026-09-13, F275 round 92) — the third overlay: the unified store's raising loader carries the classic loader's contract and every load that catches `JobNotFoundError` calls it, the last two `UUID(...)` parses of a loaded id take `normalize_job_id`, and the two vacuous prefix assertions get task ids

CONTEXT. With two overlays applied to the flipped tree at `844a7f21`, `load_job_plan` is called inside a `try` whose handler names `JobNotFoundError` at 81 sites under `packages/` and `apps/`, and `repository_snapshot.revert_repository_apply` reaches it once more through the alias `_load_job`. The classic `storage.load_job` raised `JobNotFoundError` for an absent record and `JobStoreError` for an unreadable one; `load_job_plan` returns `None` for both, so after the flip every such handler is dead and the `None` travels on into the next attribute read. `revert_repository_apply` and `test_execution_service.execute_test_run` also still parse the id with `UUID(...)`, which refuses the sixteen-hex id the flip mints.

CHOSEN, FIRST: A RAISING LOADER ON THE UNIFIED STORE, CARRIED IN THE OVERLAY. `pingpong_job.require_job_plan(job_id, root=None)` returns the plan `load_job_plan_safe` reads, raises `JobNotFoundError(job_id)` when no record exists and `JobStoreError` when one exists and cannot be read — the two classes its callers already catch, imported from `packages.orchestration.storage` inside the function. The flip round lands it in a commit of its own, ahead of its callers, because AGENTS.md's Commit Discipline keeps new code out of a refactoring commit. ALTERNATIVES: a `None` test at every call site, rejected as one contract copied into every caller; making `load_job_plan` raise, rejected because its other callers test its result for `None`; landing it in the production tree before the flip, rejected under DECISION F275 D64's second choice, since the chain's base would move for a function nothing calls until the flip.

CHOSEN, SECOND: THE CALLERS AND THE PARSES. Every such call calls `require_job_plan` and the alias imports it. In `apps/cli/commands/job_context_cmd.py` the rename leaves a fallback that loads the same id a second time when the first load answers `None`, a step between the two stores that can no longer run, so the fallback, the import it alone used and the comment sentence explaining its order are deleted. The two parses call `normalize_job_id`, whose `JobIdInvalid` is the `ValueError` both functions already handle.

CHOSEN, THIRD: THE REPAIR ROUND 91 LEFT OWED. `make_job` in `tests/orchestration/test_escalation.py` gives its tasks the ids `T001`, `T002` and onward, and `_make_planned_job` in `tests/test_workspace.py` gives its task `T001`, so the two prefix assertions compare a real id again. A mutation that drops the id from the decision id, and one that drops it from the materialised file name, each turn one of them red in the overlay's tree and leave it green in the tree before it.

CONSEQUENCE. `tests/orchestration/test_unified_store_parity.py` pins the new loader's three outcomes. What the overlay fixes, and that it newly breaks nothing, is measured by the gates of round 92's block and recorded in the round 92 ledger entry by the round that books its verdict. `R-0809`, `R-0880` and `R-0883` stay open, and no finding is registered or resolved.

HOW TO REVERSE. Delete the round 92 overlay carriers under `.agent/authored/` and this paragraph block; the flipped tree then reads `None` past those handlers again.
END DEC92

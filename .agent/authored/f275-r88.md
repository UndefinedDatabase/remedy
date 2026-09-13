── STEP T003 — F275 — ROUND 88 ──
Goal: Route every job-store load under `packages/` that parses its id with `UUID(...)` through a
new disk-free shape check, except two named sites; pin the change with a guard and a behaviour
test, each red-proved; and land the reviewer's flip dry run of the result in the record.

Base commit: `058bfa2d`. Round type: SPLIT. Production code changes, so G6's red-proofs are
mandatory in full.

THE FRAME RULE, per item 37 of §3, stated as the property MEASURED over the final bytes: NO LINE
of this block is a run of a single repeated character, and every box-drawing rule inside the
STEP and SLICE header lines is exactly two characters long.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f275-r88.md`             the block, saved verbatim
C0b `.agent/last_block.md`                    mirrored FROM THE COMMITTED C0a BLOB
C1  `.agent/plan.md`                          slice PLAN88, a full replacement
C2  `.agent/live_review.md`                   slice RECORD88 appended, the round 87 verdict
C3  `.agent/prose_slips.md`                   slice SLIPS88 appended
C4  `packages/orchestration/data_paths.py`    SPEC F1
C5  the modules of SPEC F2                    ONE commit
C6  `tests/test_data_paths.py`                SPEC T1
C7  `tests/orchestration/test_job_fulfillment.py`  SPEC T2
C8  `.agent/decisions.md`                     slice DEC88 appended
C9  `.agent/handoff.md`                       the handback

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3.

## Change — exactly these paths and no others

The Bundle's paths. `packages/orchestration/ui_server.py` and
`packages/orchestration/test_execution_service.py` are NOT changed.

## SPEC F1 — `packages/orchestration/data_paths.py`, at C4

Directly above `def lookup_job_id`, add a module constant `_JOB_ID_HEX16_RE =
re.compile(r"[0-9a-f]{16}")` and a public `normalize_job_id(raw: str) -> str`, with a one-line
WHY comment above them saying that `UUID(...)` was the id-shape check while every job id was a
UUID and refuses the sixteen-hex id `mint_job_id` mints. Behaviour: return `str(UUID(raw))` when
`UUID(raw)` succeeds; else return `raw` unchanged when `_JOB_ID_HEX16_RE.fullmatch(raw)`; else
raise `JobIdInvalid(f"invalid job ID: {raw!r}")`. It reads no disk and resolves no prefix, and its
docstring says so and names `lookup_job_id` as the function that does. Nothing else changes.

## SPEC F2 — the modules under `packages/orchestration/`, at C5

In each module below, every `UUID(<expr>)` call that is a POSITIONAL argument of a call to
`load_job`, `load_job_safe` or `_lj` becomes `normalize_job_id(<expr>)`, and so do three
assignments: `job_uuid = UUID(job_id)` in `proposed_tasks.py`'s `do_materialize` and
`reconcile_materialized`, and `uuid = UUID(str(job_id))` in `mission_state.py`'s
`mission_job_state_label`. The reviewer's count of changed calls per module: `do_continue.py` 7,
`gauntlet_runner.py` 1, `handoff.py` 1, `job_fulfillment.py` 5, `mission_readiness.py` 1,
`mission_state.py` 2, `orchestrator_brain.py` 1, `proposed_tasks.py` 3,
`real_test_execution.py` 4, `repair_loop.py` 4, `repair_request_builder.py` 1,
`self_dogfood.py` 3, `self_dogfood_execution.py` 2, `task_execution.py` 1, `token_economy.py` 1.
Each module gains a module-level `from packages.orchestration.data_paths import
normalize_job_id`; a `UUID` import left unused is deleted; imports sorted as ruff requires.
Nothing else changes.

## SPEC T1 — `tests/test_data_paths.py`, at C6

Class `TestNormalizeJobId` with three tests named EXACTLY
`test_a_uuid_comes_back_in_its_canonical_string_form` (upper-case and unhyphenated spellings of
one `uuid4()` both return its canonical string),
`test_a_minted_job_id_comes_back_unchanged_without_a_record_on_disk` (with `REMEDY_DATA_DIR` at
a path that does not exist, a `mint_job_id()` value returns unchanged and the path still does not
exist) and `test_a_short_prefix_is_not_a_job_id_and_raises_invalid` (`"abcd1234"` raises
`JobIdInvalid`, `"not-a-job-id"` raises `ValueError`). A module-level helper
`_uuid_parses_fed_to_a_job_load(source)` returning sorted `(line, function name)` pairs: inside
each function, a `UUID(...)` call that is a positional argument of `load_job`, `load_job_safe` or
`_lj`, and a bare name passed positionally to one of them that the same function assigned from a
`UUID(...)` call. Class `TestJobStoreLoadsDoNotParseTheirIdWithUuid` with a class-level exemption
set of exactly `("packages/orchestration/ui_server.py", "_load_job")` and
`("packages/orchestration/test_execution_service.py", "execute_test_run")`, a comment above it
giving DECISION F275 D62's reason for each, and two tests named EXACTLY
`test_no_job_store_load_under_packages_is_handed_a_uuid_parse` (the helper over every `.py` under
`packages/`, the repository root found from `data_paths.__file__`; the non-exempt findings are the
empty list) and `test_the_guard_sees_both_shapes_it_forbids` (on a planted source holding one
direct and one named shape in two functions, the helper returns exactly those two pairs).

## SPEC T2 — `tests/orchestration/test_job_fulfillment.py`, at C7

In the existing class `TestJobFulfillFixturePass`, a test named EXACTLY
`test_a_pingpong_job_id_reaches_the_store_instead_of_a_uuid_parse`: with `REMEDY_DATA_DIR` at
`tmp_path` and a repository from `create_demo_repo(tmp_path)`,
`run_job_fulfill("0123456789abcdef", repo, data_dir=tmp_path)` raises `JobNotFoundError`. The
file imports `pytest` at module level if it does not already.

## The pinned transcripts — the reviewer's, read by the worker, NEVER regenerated

Under `/home/decodeux/Repos/remedy/.remedy-wt/`; check each sha256 first and STOP on a mismatch.
 `r88/suite_applied.out`       sha256 c3b35c754e659344387fd1f4bae67b099b5e43f8f3bf03579800082c769a8bd0
 `r88/suite_flip88_short.out`  sha256 3f6f8088ef4fa7f1a2fd68a4c7a150a26bc9ba3f3f8c645b0539a920f6108a0f
Both are full-suite runs `python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short
-rfE` in reviewer worktrees since removed: the first over SPEC F1 and F2 applied to `058bfa2d`
without the tests; the second over SPEC F1, F2, T1 and T2 applied to `058bfa2d` and then flipped
by the committed generator and transform exactly as round 87's G4 ran them, TIP being that tree.
The flipped tree's prefix inside the second is `/home/decodeux/Repos/remedy/.remedy-wt/r88/wt_flip`.

## Constraints

1. NO SLICE IS EDITED. PLAN88, RECORD88, SLIPS88 and DEC88 land byte for byte; a discrepancy
   inside one is DECLARED, never repaired.
2. C4 to C7 are the worker's OWN code from the SPECs. The reviewer's dry-run files under
   `.remedy-wt/r88/` other than the two pinned transcripts are not opened.
3. READ `.agent/STOP` before C0a and before C9, with real exit codes. If it appears, finish the
   commit in hand, write the handoff and end.
4. Every commit stages EXACTLY ONE path, except C5, which stages the modules of SPEC F2; every
   commit stays under 500 insertions.
5. No `.py` file under `.agent/`; scratch under `.remedy-wt/r88w/`, uncommitted; every scratch
   output path absolute.
6. No landed record is rewritten: every `.agent/live_review.md`, `.agent/prose_slips.md` and
   `.agent/decisions.md` commit is an APPEND with a ZERO deletion column.
7. No `gh`, no `remedy`, no pull request, no branch created or deleted, no merge, NEVER a
   force-push, no history rewrite. No full suite: the flip transcripts are pinned.
8. The red-proof worktree is created with `git worktree add --detach` at C7 and REMOVED AND
   PRUNED before C8. The scoped suite runs in the PRIMARY checkout.
9. THE BLOCK'S OWN SIZE, measured on its final bytes: 283 lines TOTAL and 212 lines of
   PROSE, against the caps of 490 and 400.
10. GATE ORDER. G4, G5 and G6 run at C7, strictly before C8, because DEC88 quotes them, per item
    31 of §3; every figure DEC88 states is produced by one of those three gates. G1, G2, G3, G7
    and G8 run at C8. No gate runs after C9; C9's own numbers are the reviewer's.

## Done when — the gates, each run for real and its exit code recorded

G1 TRANSPORT, BUDGET, SLICES. `.agent/authored/f275-r88.md` at C0a against the block as received,
by `cmp`; `.agent/last_block.md` at C0b byte-identical to the COMMITTED C0a blob. Extract the
slices by their markers, report how many were FOUND, check each against its BEGIN-marker
sha256, and re-measure TOTAL and PROSE against constraint 9.

G2 THE PLAN. `.agent/plan.md` at C1 byte-identical to PLAN88 from the COMMITTED C0a blob; at
most 50 lines; one `## Goal` and one `## Next Steps`.

G3 THE RECORD. For the appends at C2 into `.agent/live_review.md` and at C8 into
`.agent/decisions.md`, FULL FORENSICS: the pre-commit blob read with `git show` at the commit's
PARENT, its length printed — 1123104 and 1270070 — READER A with the arithmetic printed; READER B
over the file's LAST N blank-line units against the slice's N paragraphs IN ORDER, N counted by
the script; a letter flipped in the FIRST appended paragraph REJECTED by both readers; deletion
column 0. `.agent/prose_slips.md` at C3 equals its 297865-byte pre-commit blob followed by
exactly SLIPS88. Derive the ledger's `Gate:` header pattern from the file, report how many heads
it matches, and that RECORD88's header matches it and duplicates none.

G4 THE CHANGE, STRUCTURALLY, at C7, with `ast`. The committed T1 helper, imported from the C7
test module, over every `.py` under `packages/` at `058bfa2d` read with `git show` into memory
and at C7: the reviewer measured 39 pairs in 17 files at `058bfa2d`, 2 of them exempt, and 2 at
C7, both exempt. Under `packages/`, calls to the bare name `UUID` and to `normalize_job_id`, with
`data_paths.py` included and import aliases not followed: 55 and 0 at `058bfa2d`; 19 and 37 at
C7, the 37 in the fifteen modules SPEC F2 names with its per-module counts. `ui_server.py` and
`test_execution_service.py` byte-identical at `058bfa2d` and C7. `ruff check` over every path C4
to C7 stage exits 0.

G5 THE BEHAVIOUR, at C7. (a) Every node id SPEC T1 and T2 add PASSED in the primary checkout,
their count reported. (b) The scoped suite `python3 -B -m pytest tests/test_data_paths.py
tests/cli/ tests/orchestration/ -q -p no:randomly` in the primary checkout, totals REPORTED AS
MEASURED, failure set EMPTY; the reviewer measured 13272 passed, 10 skipped and 0 failed on this
tree's production and test content at `bd2a75d5`; state and account for the difference. (c) THE
FLIP READING: verify the two pinned digests, then run the ONE fence of
`.agent/authored/f275-r87-residue.py.md` with `suite_applied.out` as the control and
`suite_flip88_short.out` as BOTH flipped transcripts, and the prefix. The reviewer measured:
flipped tally `721 failed, 17684 passed, 29 skipped, 1 warning, 31 errors`; 752 bad nodes;
flip-only 751; control-only 1; the pairs `data_paths.py::job_dir` TypeError 36 and
`job_fulfillment.py::run_job_fulfill` ValueError 46. Also report by node id the bad nodes the
two sets SHARE — the reviewer's one is
`tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes` —
and the count of lines in the flipped transcript equal, after stripping, to
`task_id=str(UUID(td["model_task_id"])),`: the reviewer's is 46.

G6 THE MUTATION RED-PROOFS, in the worktree of constraint 8, at C7. PRINT the `__file__` of
`packages.orchestration.data_paths` imported inside the worktree; it must lie inside it. Purge
`__pycache__` before each run. Selection: the two T1 classes and the T2 node id. CONTROL
unmutated: every test PASSES. Then ONE mutation at a time, each restored before the next, its
target's occurrence count reported first. M1 to M15: in each SPEC F2 module in the order F2 lists
them, the FIRST `normalize_job_id(` becomes `UUID(`. M16: in `run_job_fulfill`, its first
`load_job(normalize_job_id(job_id), data_dir)` becomes `load_job(UUID(job_id), data_dir)`. M17: in
`data_paths.py`, `[0-9a-f]{16}` becomes `[0-9a-f]{8,16}`. M18: the helper's set of loader names
reduced to `_lj` alone. M19: the helper's branch that follows an assigned name removed.
REQUIRED: M1 to M15 each fail ONLY `test_no_job_store_load_under_packages_is_handed_a_uuid_parse`;
M16 fails EXACTLY that test and the T2 test; M17 fails ONLY
`test_a_short_prefix_is_not_a_job_id_and_raises_invalid`; M18 and M19 each fail ONLY
`test_the_guard_sees_both_shapes_it_forbids`. Report every failing node id and exit code per run.

G7 TREE, CANARY, LINT, PATH SET, OPEN SET, at C8. `git status --porcelain` prints `''`;
`git worktree list` one row; the canary `python3 -B -m pytest tests/cli/test_golden_path.py -q`
exit 0, 42 at `058bfa2d`; `ruff check .` rows compared as a MULTISET at `058bfa2d` and at C8, the
difference empty, 26 at `058bfa2d`. The changed-path set of `058bfa2d`..C8 against the Bundle's
paths MINUS `.agent/handoff.md`, MISSING and EXTRA by name. The open set BY DISTINCT ID at
`058bfa2d` and at C8: 88 at both with identical membership; `R-0809`, `R-0880`, `R-0883` open.

G8 THE INSERTION CAP over `058bfa2d`..C8: one row per commit with insertions, deletions and
staged path count, and the number of commits reaching 500 insertions.

Handback: `.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 30 of feature F275 · round 88 · rounds so far 88`; the Commits table read from
`git show --numstat` and compared cell by cell against G8, C9's row carrying no numbers and
saying why; one Verification line per gate with its REAL exit code; External actions;
Authored-text proofs; Item-status; Deviations; `## Next` stating `Operator questions open: 1`.
NO SCOPE REPORT AND NO SESSION-LIMIT BANNER, by amendment amend0911-f275-to-scope.

── SLICE PLAN88 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN88 sha256=6f7beb9bec199e6ad61e3bcc5a38b005c8d01cc859617da49da4c2bc58faeb53
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

ROUND 88 ROUTES THE JOB-STORE LOADS UNDER `packages/` AWAY FROM `UUID(...)`. A new disk-free
`normalize_job_id` returns a UUID in canonical form or a sixteen-hex job id unchanged, and
raises `JobIdInvalid` for anything else. The parses that hand a job id to `load_job`,
`load_job_safe` or `_lj` go through it, except in `ui_server._load_job` and `execute_test_run`,
which keep theirs for reasons the guard names. A guard test pins the census by shape, one
behaviour test pins `run_job_fulfill`'s load, and the round books the round 87 verdict and
its prose slips.

## Next Steps

1. THE NEXT RESIDUE GROUPS OF THE FLIP'S DRY RUN, each a pre-flip production round or a
   transform rule: the task-id parses that feed `TaskEntry`, the `UUID` values
   `pingpong_job._persist_job` cannot serialise, and `ui_server`'s which-store loader and its
   adapter.
2. THE FLIP'S DRY RUN AGAIN after them, read for what remains.
3. THE FLIP, carrying DECISION F275 D48's obligations, as a series of commits each under the
   500-insertion cap inside one round, unless the operator allows one more oversized commit.
   The stale test double at `packages/orchestration/project_registry.py:856` moves with it.
4. Then the classic store, then the closure sequence.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20
  sessions and 60 rounds without a replacement, so this feature closes only at full scope.
- THE FLIP IS NOT CLOSE: flipped on this round's candidate the full suite has 752 bad nodes.
- MOST ROUTED LOADS ARE PINNED BY A SHAPE GUARD ALONE; only `run_job_fulfill`'s first load
  also has a behaviour test.
- ONE ROUTED LOAD IS REACHED BY NO TEST until `R-0883` is repaired.
- The open set is 88 by distinct id at this round's base, with `R-0809`, `R-0880` and `R-0883`
  open. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END PLAN88

── SLICE RECORD88 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD88 sha256=507d5fb28e751a9841f102dbf018be79a412a27f27e56706947a1b9c5280544c

Gate: F275 R87 — the F275 round 87 entry. VERDICT PASS. Written by the planner and reviewer of session 30 after reading the committed range `bd2a75d5`..`058bfa2d` and RE-DERIVING EVERY GATE INDEPENDENTLY; the worker's report and its transcripts were evidence for no line below. It is booked here by the FIRST SUBSTANTIVE COMMIT of round 88 that writes the record, per operator amendment amend0827-process-diet rule 1. The round changed no production path, and the reviewer ran the worker's committed instrument itself.

WHAT THE TRANSPORT PROOF COVERS, per item 37 of §3. The committed `.agent/authored/` blob was identical to the reviewer's own original at 29430 bytes, `.agent/last_block.md` equalled it, and all five slices matched their BEGIN-marker digests; `.agent/plan.md` equalled PLAN87 and `.agent/operator_questions.md` equalled OPQ87. The three appends were exact under reader A — 1119826 plus 3278 into the review record, 296513 plus 1352 into the prose slips, and 1264216 plus 5854 into the decisions — with reader B holding at N counted from each slice as 4, 3 and 9, and a letter flipped in each FIRST appended paragraph rejected by both readers. Ten paths changed across the range, the handback included, none under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/`; every commit staged one path and the largest was 300 insertions.

THE READING HOLDS UNDER THE REVIEWER'S OWN RE-RUN. The instrument committed at C4, extracted from its one fence and run twice by the reviewer over the three pinned transcripts, printed byte-identical stdout, and every line of it appears in order in the artefact at C5. It reproduces every figure the reviewer took before authoring, among them 826 flip-only nodes and none control-only, 826 sections, deepest frames 237 in production, 589 in tests and none unattributable, and the `data_paths.job_dir` pair at 80. Over the reviewer's own altered copies it reads 825 flip-only with one `FAILED` line removed, 1 control-only with one appended, and no `job_dir` pair once that pair's 80 frame lines are removed, so it fails in each way it is used. The tree objects of `apps/`, `packages/` and `tests/` at C8 equal those at `bd2a75d5`, so the canary's 42 and the 26 rows of `ruff check .` stand; the open set is 88 at both ends with identical membership, `R-0809`, `R-0880` and `R-0883` open.

TWO READINGS THE BLOCK SCHEDULED WRONG, AND THE WORKER KEPT THE RECORD TRUE. DEC87 at C6 quotes the history of commits above 500 insertions, which the block ordered measured only by G8 at C7, one commit later, and it quotes the 73 and 7 split of the server-side tracebacks, which no gate ordered at all. The worker ran the G8 command before C6 and read the split from the pinned transcript before C6, and both matched, so nothing false landed; the two slips are booked beside this entry.
END RECORD88

── SLICE SLIPS88 ── target `.agent/prose_slips.md` ── APPEND ──
BEGIN SLIPS88 sha256=882b2770656ed99208fdd84465104c1ec4234ef4590ab28b63f66f2beacafc10

2026-09-13 · F275 R87 · DECISION F275 D61 at C6 quotes the history of commits above 500 insertions, a reading the round 87 block ordered only in G8 at C7, one commit later, while the same block's constraint 10 cited item 31 of §3 for exactly that ordering; the worker ran the command before C6. THE RULE THAT FOLLOWS: before emission, every figure a slice states is traced to the gate that produces it, and that gate's commit is compared with the slice's.

2026-09-13 · F275 R87 · DECISION F275 D61 says 73 of the 80 lost ui-server connections end in the adapter's missing attribute and 7 in the path join, a split the reviewer read by hand after the gates were written and no gate of the round 87 block reproduces; the worker checked it against the pinned transcript unasked. THE RULE THAT FOLLOWS: a figure measured after the gates are written is added to a gate or left out of the slice.
END SLIPS88

── SLICE DEC88 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC88 sha256=587198a64c952e3576106c1be50ce4ac3ef268e5fde6ea9dfa63674b9e244a22

## DECISION F275 D62 (2026-09-13, F275 round 88) — a job-store load under `packages/` takes its id through a disk-free shape check instead of `UUID(...)`; two parses stay for named reasons, and a shape guard plus one behaviour test pins the rest

CONTEXT. DECISION F275 D61 found the flip's two largest production residue groups raising where a job id is parsed with `UUID(...)` on its way into the job store: in `run_job_fulfill`, and at the store's path join. At `058bfa2d` a guard that follows `UUID(...)` into `load_job`, `load_job_safe` or `_lj`, directly or through one assigned name, reports 39 sites in 17 files under `packages/`. Before this round was authored the reviewer applied the change below in a worktree at `058bfa2d`, ran the full suite there, restored each routed file's first parse and each guard branch one at a time, and flipped the result. The readings below are the reviewer's; the gates that constraint 10 of round 88's block runs before the commit landing this paragraph reproduce them.

CHOSEN, FIRST: A NEW FUNCTION, NOT `lookup_job_id`. `normalize_job_id` returns `str(UUID(raw))` for any string `UUID(...)` accepts and sixteen lowercase hex characters unchanged, and raises `JobIdInvalid` for anything else, reading no disk. Every id that loaded before therefore loads the same file, and every string refused before is still refused with a `ValueError`, except exactly the minted shape, which now reaches the store and is not found there. ALTERNATIVES: `lookup_job_id`, rejected because it resolves a prefix under the environment's data root while these callers pass their own `data_dir`, so a job held only under that directory would stop resolving once ids are sixteen hex characters; dropping the parse, rejected because `load_job` builds a path from whatever string it receives, and the shape check is what stands between a caller's string and that path.

CHOSEN, SECOND: THIRTY-SEVEN PARSES ARE ROUTED AND TWO ARE NOT. The routed ones are every positional `UUID(...)` argument of the three loaders under `packages/` and the three names bound from `UUID(...)` that reach only a loader. `ui_server._load_job` keeps its parse because the parse is its which-store switch: routed, a sixteen-hex id would be tried against the classic store and answered 404 before the ping-pong branch ran. `execute_test_run` keeps its parse because the parsed `UUID` goes on to event writers and a lease, a return domain this round does not widen. The guard names both, with those reasons.

CHOSEN, THIRD: THE PIN IS A SHAPE GUARD AND ONE BEHAVIOUR TEST, SAID PLAINLY. For every id the classic store holds the change is behaviour-neutral, so only the minted shape tells routed from unrouted, and reaching thirty-seven loads with it would take thirty-seven fixtures. The guard fails when the first routed parse of any one of the fifteen modules is restored, and it is shown to see the direct and the named shape on a planted source. `run_job_fulfill` given a minted id raises `JobNotFoundError` instead of `ValueError`, and restoring that load's parse fails that test together with the guard.

CONSEQUENCE. Flipped on top of this change and its tests, the full suite reads 721 failed and 31 errors, 752 bad nodes against 827 at `bd2a75d5`, and the one of them an unflipped run of the change also fails is the node that needs `apps/ui/node_modules`. The `data_paths.job_dir` group falls from 80 to 36. The `run_job_fulfill` group stays at 46 but now raises one step later, at `task_id=str(UUID(td["model_task_id"]))`: the same shape seam, reached through a task id. `R-0809`, `R-0880` and `R-0883` stay open, and no finding is registered or resolved.

HOW TO REVERSE. Restore the sixteen production files and the two test files from `058bfa2d` and delete this paragraph block; the loads then parse with `UUID(...)` again and a minted id dies in the parse.
END DEC88

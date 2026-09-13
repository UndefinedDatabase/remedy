── STEP T003 — F275 — ROUND 89 ──
Goal: Drop `run_job_fulfill`'s `UUID(...)` round trip of a task id it wrote itself, route the
test parses of a job id handed to a job-store load through `normalize_job_id`, and prove both in
flipped trees, where alone they are observable.

Base commit: `5bff6960`. Round type: SPLIT. Production code changes by one line, and G6 is its
red-proof in full.

THE FRAME RULE, per item 37 of §3, stated as the property MEASURED over the final bytes: NO LINE
of this block is a run of a single repeated character, and every box-drawing rule inside the
STEP and SLICE header lines is exactly two characters long.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f275-r89.md`             the block, saved verbatim
C0b `.agent/last_block.md`                    mirrored FROM THE COMMITTED C0a BLOB
C1  `.agent/plan.md`                          slice PLAN89, a full replacement
C2  `.agent/live_review.md`                   slice RECORD89 appended, the round 88 verdict
C3  `.agent/prose_slips.md`                   slice SLIPS89 appended
C4  `packages/orchestration/job_fulfillment.py`  SPEC F
C5  the test files of SPEC T                  ONE commit
C6  `.agent/decisions.md`                     slice DEC89 appended
C7  `.agent/handoff.md`                       the handback

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3.

## Change — exactly these paths and no others

The Bundle's paths. Nothing under `apps/`, `docs/` or `scripts/`; under `packages/` only C4's.

## SPEC F — `packages/orchestration/job_fulfillment.py`, at C4

In `run_job_fulfill`, the one line `            task_id=str(UUID(td["model_task_id"])),` becomes
EXACTLY `            task_id=td["model_task_id"],`. Nothing else in the file changes; its `UUID`
import stays, because other lines use it.

## SPEC T — the test files, at C5

In each file below, every call that is a POSITIONAL argument of a call to `load_job`,
`load_job_safe` or `append_run_event`, and that calls `UUID` by the bare name, by the name
`_UUID`, or as an attribute `.UUID` — `uuid.UUID(...)`, `__import__("uuid").UUID(...)` — keeps its
argument and becomes a call of `normalize_job_id`. The reviewer's count per file, under
`tests/`: `cli/test_propose_cli.py` 2, `cli/test_self_dogfood_cli.py` 1,
`orchestration/test_approval_queue.py` 2, `orchestration/test_do_continue.py` 3,
`orchestration/test_do_run.py` 1, `orchestration/test_dod_gate.py` 1,
`orchestration/test_job_fulfillment.py` 2, `orchestration/test_mission_e2e.py` 4,
`orchestration/test_mission_readiness.py` 1, `orchestration/test_orchestrator_brain.py` 4,
`orchestration/test_project_brain.py` 1, `orchestration/test_proposed_tasks.py` 2,
`orchestration/test_queue_executor_binding.py` 3, `orchestration/test_repair_apply_cycle.py` 5,
`orchestration/test_repair_loop_v1.py` 3, `orchestration/test_repair_request_builder.py` 10,
`orchestration/test_resume_kill.py` 1, `orchestration/test_watchdog.py` 1,
`orchestration/test_worker_execution.py` 12, `test_cli_main.py` 9. Each file gains a
module-level `from packages.orchestration.data_paths import normalize_job_id`; an import left
unused, and a blank line its removal leaves at the head of a function body, is deleted; imports
sorted as ruff requires. No assertion changes and no test is added or deleted.

## Constraints

1. NO SLICE IS EDITED. PLAN89, RECORD89, SLIPS89 and DEC89 land byte for byte; a discrepancy
   inside one is DECLARED, never repaired.
2. C4 and C5 are the worker's OWN edits from the SPECs. The reviewer's dry-run files under
   `.remedy-wt/r89/` are not opened.
3. READ `.agent/STOP` before C0a and before C7, with real exit codes. If it appears, finish the
   commit in hand, write the handoff and end.
4. Every commit stages EXACTLY ONE path, except C5, which stages the files of SPEC T; every
   commit stays under 500 insertions.
5. No `.py` file under `.agent/`; scratch under `.remedy-wt/r89w/`, uncommitted; every scratch
   output path absolute.
6. No landed record is rewritten: every `.agent/live_review.md`, `.agent/prose_slips.md` and
   `.agent/decisions.md` commit is an APPEND with a ZERO deletion column.
7. No `gh`, no `remedy`, no pull request, no branch created or deleted, no merge, NEVER a
   force-push, no history rewrite. No full suite.
8. G6's two worktrees are created with `git worktree add --detach` and REMOVED AND PRUNED before
   C6; its generator trees are plain directories. The scoped suite runs in the PRIMARY checkout.
9. THE BLOCK'S OWN SIZE, measured on its final bytes: 235 lines TOTAL and 166 lines of
   PROSE, against the caps of 490 and 400.
10. GATE ORDER. G4, G5 and G6 run at C5, strictly before C6, because DEC89 quotes them, per item
    31 of §3. The figures DEC89's CHOSEN paragraphs state are the ones G4, G5 and G6 name. G1,
    G2, G3, G7 and G8 run at C6. No gate runs after C7; C7's own numbers are the reviewer's.

## Done when — the gates, each run for real and its exit code recorded

G1 TRANSPORT, BUDGET, SLICES. `.agent/authored/f275-r89.md` at C0a against the block as received,
by `cmp`; `.agent/last_block.md` at C0b byte-identical to the COMMITTED C0a blob. Extract the
slices by their markers, report how many were FOUND, check each against its BEGIN-marker
sha256, and re-measure TOTAL and PROSE against constraint 9.

G2 THE PLAN. `.agent/plan.md` at C1 byte-identical to PLAN89 from the COMMITTED C0a blob; at
most 50 lines; one `## Goal` and one `## Next Steps`.

G3 THE RECORD. For the appends at C2 into `.agent/live_review.md` and at C6 into
`.agent/decisions.md`, FULL FORENSICS: the pre-commit blob read with `git show` at the commit's
PARENT, its length printed — 1125943 and 1273941 — READER A with the arithmetic printed; READER B
over the file's LAST N blank-line units against the slice's N paragraphs IN ORDER, N counted by
the script; a letter flipped in the FIRST appended paragraph REJECTED by both readers; deletion
column 0. `.agent/prose_slips.md` at C3 equals its 298762-byte pre-commit blob followed by
exactly SLIPS89. Derive the ledger's `Gate:` header pattern from the file, report how many heads
it matches, and that RECORD89's header matches it and duplicates none.

G4 THE CHANGE, STRUCTURALLY, at C5, with `ast`, reading `5bff6960` with `git show` into memory.
In `run_job_fulfill` at `5bff6960`, the line numbers of `td["model_task_id"] = str(task.id)` and
of the round trip: the reviewer's are 660 and 689. At C5 the round trip's count in the file is 0
and SPEC F's new line's is 1, and C4's numstat is 1 and 1. Under `tests/`, the calls SPEC T
defines: 68 in the twenty files it lists at `5bff6960`, 0 at C5; `normalize_job_id` calls in
those files 0 and 68. `ruff check` over every path C4 and C5 stage exits 0.

G5 THE BEHAVIOUR BEFORE THE FLIP, at C5. (a) `python3 -B -m pytest` over the twenty SPEC T files
with `-q -p no:randomly -p no:cacheprovider` in the primary checkout: the reviewer's candidate
read 711 passed. (b) The scoped suite `python3 -B -m pytest tests/test_data_paths.py tests/cli/
tests/orchestration/ -q -p no:randomly` in the primary checkout, totals REPORTED AS MEASURED,
failure set EMPTY; the reviewer measured 13278 passed, 10 skipped and 0 failed on this tree's
production and test content at `8cc8ec6a`; state and account for any difference.

G6 THE PROOF IN FLIPPED TREES, at C5. Build the generator's trees exactly as round 87's block
G4 orders — BASE from `ef75e213`, the shift and delete controls, the pinned
`/home/decodeux/Repos/remedy/.remedy-wt/r77_corrected.json` sha256 765b5ba9…, its owners file
sha256 670c6e95…, and `/home/decodeux/Repos/remedy/.remedy-wt/r61_status.json` sha256 a4c6cd63…
checked first — TWICE: once with TIP from `git archive 5bff6960`, once with TIP from `git
archive` of C5. For each, run the generator, then the transform over a detached worktree at that
same commit with that run's TIP re-keyed set and owners. (a) In both flipped worktrees run the
twenty SPEC T files with `-q -p no:randomly -p no:cacheprovider --tb=short -rfE`. The reviewer
measured: at `5bff6960` `148 failed, 532 passed, 31 errors`, 179 distinct bad node ids and 93
lines starting `E   ValueError: badly formed hexadecimal UUID string`; at the change `82 failed,
598 passed, 31 errors`, 113 bad node ids and 2 such lines; 66 node ids bad only at `5bff6960` and
0 bad only at the change. (b) THE RED-PROOF, in the flipped worktree at C5: print
`packages.orchestration.job_fulfillment.__file__`, which must lie inside it; purge `__pycache__`
before each run; selection `tests/orchestration/test_dod_gate.py` and
`tests/orchestration/test_job_fulfillment.py`. CONTROL: the reviewer's read `26 failed, 111
passed`. MUTATION: the one line `            task_id=td["model_task_id"],`, its count reported as 1
first, becomes `            task_id=str(__import__("uuid").UUID(td["model_task_id"])),`; the
reviewer's read `45 failed, 92 passed`, with 41 `E   ValueError: badly formed hexadecimal UUID
string` lines. Report tallies, exit codes and those counts; restore, confirm the file's bytes
equal the flipped control's, then remove and prune both worktrees.

G7 TREE, CANARY, LINT, PATH SET, OPEN SET, at C6. `git status --porcelain` prints `''`;
`git worktree list` one row; the canary `python3 -B -m pytest tests/cli/test_golden_path.py -q`
exit 0, 42 at `5bff6960`; `ruff check .` rows compared as a MULTISET at `5bff6960` and at C6, the
difference empty, 26 at `5bff6960`. The changed-path set of `5bff6960`..C6 against the Bundle's
paths MINUS `.agent/handoff.md`, MISSING and EXTRA by name. The open set BY DISTINCT ID at
`5bff6960` and at C6: 88 at both with identical membership; `R-0809`, `R-0880`, `R-0883` open.

G8 THE INSERTION CAP over `5bff6960`..C6: one row per commit with insertions, deletions and
staged path count, and the number of commits reaching 500 insertions.

Handback: `.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 30 of feature F275 · round 89 · rounds so far 89`; the Commits table read from
`git show --numstat` and compared cell by cell against G8, C7's row carrying no numbers and
saying why; one Verification line per gate with its REAL exit code; External actions;
Authored-text proofs; Item-status; Deviations; `## Next` stating `Operator questions open: 1`.
NO SCOPE REPORT AND NO SESSION-LIMIT BANNER, by amendment amend0911-f275-to-scope.

── SLICE PLAN89 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN89 sha256=44e5a60c5c1eca6a688ef07fc252dc7e9dba1f1cd091b2cab968fd98a46bf744
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

ROUND 89 CLEARS TWO RESIDUE GROUPS THE FLIP'S DRY RUN NAMED, BOTH INVISIBLE BEFORE THE FLIP.
`run_job_fulfill` stops passing a task id it wrote itself through `UUID(...)` and back, and the
tests that hand a job-store load or `append_run_event` a `UUID(...)` parse of a job id take
`normalize_job_id` instead. Before the flip both changes are value-identical, so they are proved
in flipped trees: the touched test files flipped at the base and at the change, and the round
trip restored inside the flipped change. The round books the round 88 verdict and its slip.

## Next Steps

1. THE NEXT RESIDUE GROUPS OF THE FLIP'S DRY RUN, each a pre-flip production round, a
   transform rule or a flip-time edit: `ui_server`'s which-store loader and its adapter;
   members the unified records lack, such as `TaskEntry`'s `acceptance_checks` and
   `JobPlan`'s `model_dump_json`; `UUID` values reaching the unified record; and what is left
   of the classic runner under `job resume`.
2. THE FLIP'S DRY RUN AGAIN after them, read for what remains.
3. THE FLIP, carrying DECISION F275 D48's obligations, as a series of commits each under the
   500-insertion cap inside one round, unless the operator allows one more oversized commit.
   The stale test double at `packages/orchestration/project_registry.py:856` moves with it.
4. Then the classic store, then the closure sequence.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20
  sessions and 60 rounds without a replacement, so this feature closes only at full scope.
- THE FLIP IS NOT CLOSE: DECISION F275 D62's flipped full suite had 752 bad nodes.
- A CHANGE PROVED ONLY IN A FLIPPED TREE depends on the generator and transform staying
  reproducible from round 77's two scratch JSON files.
- ONE ROUTED LOAD IS REACHED BY NO TEST until `R-0883` is repaired.
- The open set is 88 by distinct id at this round's base, with `R-0809`, `R-0880` and `R-0883`
  open. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END PLAN89

── SLICE RECORD89 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD89 sha256=698e96acfbf4fb007440a5095f6b25824de52a5686159ed4b2823acdba36578a

Gate: F275 R88 — the F275 round 88 entry. VERDICT PASS. Written by the planner and reviewer of session 30 after reading the committed range `058bfa2d`..`5bff6960` and RE-DERIVING EVERY GATE AND EVERY RED-PROOF INDEPENDENTLY; the worker's report and its transcripts were evidence for no line below. It is booked here by the FIRST SUBSTANTIVE COMMIT of round 89 that writes the record, per operator amendment amend0827-process-diet rule 1. The round changed production code and the reviewer ran its own nineteen mutations in its own worktree before writing this.

WHAT THE TRANSPORT PROOF COVERS, per item 37 of §3. The committed `.agent/authored/` blob was identical to the reviewer's own original at 24621 bytes, `.agent/last_block.md` equalled it, and all four slices matched their BEGIN-marker digests; `.agent/plan.md` equalled PLAN88. The three appends were exact under reader A — 1123104 plus 2839 into the review record, 297865 plus 897 into the prose slips, and 1270070 plus 3871 into the decisions — with reader B holding at N counted from each slice as 4, 2 and 7, and a letter flipped in each FIRST appended paragraph rejected by both readers. Every commit staged one path except C5, which staged the fifteen modules, and the largest commit was 283 insertions.

THE PRODUCTION CHANGE HOLDS UNDER THE REVIEWER'S OWN RE-RUN. `normalize_job_id` returns `str(UUID(raw))`, sixteen lowercase hex characters unchanged, or raises `JobIdInvalid`, and reads no disk. Read by the committed guard helper, the `UUID(...)` parses handed to a job-store load under `packages/` went from 39 pairs in 17 files at `058bfa2d` to 2 at C7, both the named exemptions; bare `UUID` calls under `packages/` went from 55 to 19 and `normalize_job_id` calls from 0 to 37; `ui_server.py` and `test_execution_service.py` are unchanged. In a worktree at `8cc8ec6a` whose module the reviewer printed as resolving inside it, the six new tests passed unmutated. Restoring the first routed parse of each of the fifteen modules failed only the census guard; restoring `run_job_fulfill`'s load failed the guard and the behaviour test; widening the sixteen-hex pattern failed only the short-prefix test; and narrowing the helper's loader names or removing its named-shape branch failed only the planted-source test. The scoped suite in the primary checkout read 13278 passed, 10 skipped and 0 failed, the base's 13272 plus exactly the six new tests; `ruff check .` rows compared as a multiset at `058bfa2d` and at the tip differ by nothing, at 26 each; the canary read 42; and the open set stayed 88 with identical membership, `R-0809`, `R-0880` and `R-0883` open.

ONE CONSTRAINT OF THE BLOCK WAS FALSE, AND THE WORKER SAID SO. Constraint 10 said every figure DEC88 states is produced by G4, G5 or G6, while DEC88 also quotes round 87's 827 bad nodes and the `job_dir` group's earlier 80. The worker declared it and checked both figures against the round 87 record, where they stand, so nothing false landed.
END RECORD89

── SLICE SLIPS89 ── target `.agent/prose_slips.md` ── APPEND ──
BEGIN SLIPS89 sha256=074160cea130e9f21557c444d256c26a9c47d7902ae9378f51776596ddbdd965

2026-09-13 · F275 R88 · Constraint 10 of the round 88 block says every figure DECISION F275 D62 carries is produced by that round's G4, G5 or G6, while the same slice quotes round 87's 827 bad nodes and the `job_dir` group's earlier 80; the worker declared the universal false and checked both figures against the round 87 record. THE RULE THAT FOLLOWS: a constraint quantifying over a slice's figures is written after the slice and checked figure by figure, or it names the figures it covers.
END SLIPS89

── SLICE DEC89 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC89 sha256=4c84811240773972243e934ebd059d972b8783a93cbbf25c87dbb6f957f5f3a9

## DECISION F275 D63 (2026-09-13, F275 round 89) — `run_job_fulfill` stops round-tripping a task id through `UUID(...)`, and test parses of a job id handed to a load take `normalize_job_id`; both are proved in flipped trees, because before the flip nothing tells them apart

CONTEXT. DECISION F275 D62's flip dry run left `run_job_fulfill`'s group at 46, raising at `task_id=str(UUID(td["model_task_id"]))`, and its transcript holds more failures raising in the tests' own `UUID(...)` parses of a job id. At `5bff6960` the reviewer applied the change below in a worktree, ran the touched test files there, flipped the base and the change with the committed generator and transform, ran the touched test files in both flipped trees, and restored the round trip inside the flipped change. The readings in CHOSEN, FIRST to THIRD are the reviewer's at `5bff6960` and at that change, and the gates constraint 10 of round 89's block runs before the commit landing this paragraph reproduce them.

CHOSEN, FIRST: THE TASK-ID ROUND TRIP IS DROPPED. Twenty-nine lines above it the same function assigns `td["model_task_id"] = str(task.id)`, already the canonical string, so `str(UUID(...))` of it returns the same string for every task the classic record holds and refuses the task id the unified record carries. ALTERNATIVE: a task-id shape check like `normalize_job_id`, rejected because this value is never input; it is a string the same function wrote.

CHOSEN, SECOND: SIXTY-EIGHT TEST PARSES IN TWENTY TEST FILES ARE ROUTED. Every `UUID(...)` call — by the bare name, by the alias `_UUID` or through an attribute `.UUID` — that is a positional argument of `load_job`, `load_job_safe` or `append_run_event` becomes `normalize_job_id(...)`. The tests keep asserting what they asserted, and after the flip they hand the store a string it can open. ALTERNATIVE: leave them to the flip's transform, rejected because that is a new transform rule with its own residue, while this edit is green before the flip and measurable after it.

CHOSEN, THIRD: THE PROOF IS TAKEN IN FLIPPED TREES. Before the flip both changes are value-identical, so undoing either reddens nothing and a red-proof ordered there could only come back green. The twenty touched test files pass unflipped at the change, 711 tests. Flipped at `5bff6960` they read 148 failed and 31 errors, 179 bad nodes, with 93 `badly formed hexadecimal UUID string` error lines; flipped at the change they read 82 failed and 31 errors, 113 bad nodes, with 2 — 66 nodes fixed and none newly bad. Inside the flipped change, restoring the round trip takes `test_dod_gate.py` and `test_job_fulfillment.py` from 26 failures to 45, with the parse error raised at that line 41 times.

CONSEQUENCE. Nothing else in the flip's residue is touched. `R-0809`, `R-0880` and `R-0883` stay open, and no finding is registered or resolved.

HOW TO REVERSE. Restore `packages/orchestration/job_fulfillment.py` and the twenty test files from `5bff6960` and delete this paragraph block; the flipped tree then fails at the round trip and at the tests' parses again.
END DEC89

── STEP T003/4 — F112 ────────────────────────────────────────
Goal: Book round 4's verdict and register+fix the one Low finding it
carries (an unused import round 4's own authored slice introduced),
then start T003 by adding a public single-task split seam to
`task_granularity.py` that the dispatch-time `cannot_fit` decision
(a later round) will call — without touching the split heuristics
themselves or the band/acceptance trigger `normalize_plan` owns.

Bundle:
1. Fix R-0792 (Low): remove the unused `ClassBudgetFit` import from
   `tests/orchestration/test_context_compiler.py`.
2. Book RECORD4 (round 4's verdict, including R-0792's registration
   and resolution) into `.agent/live_review.md`.
3. Add `split_one_task` to `packages/orchestration/task_granularity.py`.
4. Add 4 tests to `tests/orchestration/test_task_granularity.py`.

Change: exactly the 4 files named above, plus `.agent/plan.md`,
`.agent/authored/f112-r5.md` and `.agent/last_block.md`. Nothing else.

Constraints:
- Do NOT touch `_split_triggers`, `_cluster_acceptance`, `_split_task`,
  `_apply_splits`, `normalize_plan`, or any merge-side function — F016's
  "Do not touch" boundary (docs/roadmap/features/T3_F112.md) reaches
  this seam too: `split_one_task` calls the existing private helpers,
  it does not re-implement or alter them.
- Every pair below is APPEND-shaped: apply as
  `content = content.replace(FROM, TO, 1)` — FROM occurs exactly once in
  the current file, TO contains FROM as a literal prefix, and the file
  text after FROM's original span is untouched by construction.
- RECORD4 is ONE line (no internal newlines) ending in exactly one
  trailing newline, matching every existing `Gate:` entry's shape.
- `.agent/plan.md` stays under 50 lines (AGENTS.md).
- ruff availability is inconsistent this session: try the bare `ruff`
  binary first, fall back to `python3 -m ruff check <path>` if denied;
  report which one worked.

Done when: every gate in "Gates" below is run for real and its exact
output recorded in the handback; all 7 commits (C0a-C5, listed below)
plus the handback commit (C6) land in the stated order; tree is clean;
branch is pushed.

Handback: completion report + rewrite `.agent/handoff.md` per
AGENTS.md's `### handoff.md` section and
docs/agents/handback_template.md.
──────────────────────────────────────────────────────────────

<<<BEGIN PLAN5 (whole-file replacement of .agent/plan.md)>>>
# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001 and T002 complete as of round 4.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 5, session 2 — books round 4's verdict (R-0792, a Low ruff F401
fixed in this same round), then starts T003: `split_one_task` in
`packages/orchestration/task_granularity.py`, a public seam over the
existing `_cluster_acceptance`/`_split_task` clustering for a caller that
already decided (via T002's `cannot_fit`) a task needs to split, without
re-deciding the band/acceptance trigger `normalize_plan` owns.

## Next Steps

- T003 continued: wire `cannot_fit` into `enqueue_task_decision` (type
  `task_decision`, `escalation.py:211`) at the per-task dispatch loop in
  `pingpong_job.py` (~line 2307's `run_pingpong` call, the site with a
  live `Job`/`Task`). Needs: how `task_class` is resolved per task,
  how `compiled_context_paths`/`candidates` reach `run_pingpong` today,
  and a `Task`→`PlannedTask` reconstruction (`flight_plan.py:513-538`
  stashes title/depends_on/band/files_hint on `task.inputs["flight"]`;
  `goal` is not preserved separately — recover it from `task.description`).
- Unattended default `safe_default="split task"`, applied via
  `auto_apply_safe_default` when `unattended=True`
  (`long_run_executor.py:992` `_escalate_task` is the pattern). Omit the
  split option when `split_one_task` returns None (A9: real options only).
- Acceptance fixtures, the integration gate, then closure.

## Risks

- Dispatch-loop wiring is the highest-risk remaining slice — a live loop,
  not a pure function. Gets its own round, call site read in full first.
- `R-0767` stays OPEN on the model-routing seam this feature's config
  pattern borrows from; unrelated to F112, not absorbed.
- ruff is inconsistent this session; `python3 -m ruff check <path>` is
  the reliable form, re-measured every round.
<<<END PLAN5>>>

<<<BEGIN FIX_FROM>>>
    OMITTED_CONTEXT_FILENAME,
    ClassBudgetFit,
<<<END FIX_FROM>>>

<<<BEGIN FIX_TO>>>
    OMITTED_CONTEXT_FILENAME,
<<<END FIX_TO>>>

<<<BEGIN RECORD4 (append to .agent/live_review.md)>>>
Gate: F112 R4 — the round 4 entry. VERDICT PASS, over the range `3eae460d..4301efc2` plus the handback commit `a4c2570d`, independently re-verified by the reviewer. THE PRODUCTION CODE HELD: `git diff 3eae460d..HEAD -- packages/orchestration/context_compiler.py` reproduced by the reviewer matches the round's own CC_IMPORT and CC_MODULE pairs exactly, and `python3 -m ruff check packages/orchestration/context_compiler.py` reproduced as `All checks passed!`. THE TESTS HELD: `python3 -m pytest tests/orchestration/test_context_compiler.py -q` reproduced by the reviewer at 69 passed. THE CANARY HELD: `pytest tests/cli/test_golden_path.py -q` reproduced at 42 passed. `.agent/plan.md` reproduced at 40 lines with `## Goal` and `## Next Steps` both present. ONE FINDING IS OWED BY THIS ROUND: R-0792 (Low, tests/ — REGISTERED AND RESOLVED IN THIS BOOKING): the open set was searched first per checklist item 30 and held no existing entry for this defect class (the nearest, R-0364 and R-0468, are both about the repository's own pre-existing ruff debt, not a defect this branch introduced). `python3 -m ruff check tests/orchestration/test_context_compiler.py`, run independently by the reviewer at `4301efc2`, found one real defect round 4's own TEST_P1 slice introduced: F401, `ClassBudgetFit` imported but never referenced by name in any of round 4's four new tests, which only call `fit_task_context_to_class_cap` and read attributes off its return value. Root cause is the reviewing session's own authored TEST_P1 slice, not the worker's application of it, which correctly declared the defect rather than silently trimming an import it was ordered to apply byte for byte. Done: R-0792 — fixed in this round's own C2 (removing the unused import line), before this entry was written; `python3 -m ruff check tests/orchestration/test_context_compiler.py` reproduced by the reviewer as `All checks passed!` at the post-fix commit. THE G3 SHAPE DISCREPANCY round 4 declared in `.agent/prose_slips.md` is confirmed correctly classified: the pinned byte arithmetic 2250826 + 2 + 1739 = 2252567 holds exactly on disk, and the extra newline is a reviewer-authored-formula defect with no product effect, not wrong state under packages/, apps/, tests/ or docs/. NO OTHER FINDING IS OWED BY THIS ROUND.
<<<END RECORD4>>>

<<<BEGIN TG_FROM>>>
    return children


<<<END TG_FROM>>>

<<<BEGIN TG_TO>>>
    return children


def split_one_task(
    task: PlannedTask, used_ids: set[str] | None = None,
) -> list[PlannedTask] | None:
    """Split ONE already-dispatched task into acceptance-clustered children,
    or None when it cannot usefully split.

    This is the public seam plan-time normalization never needed: F016's own
    entry point is :func:`normalize_plan`, which decides FOR ITSELF (via
    ``_split_triggers``) whether a task is oversized. A caller here has
    already made that call for its own reason — F112's ``cannot_fit``
    outcome, for instance — and wants exactly the clustering
    ``_apply_splits`` already proved out, without re-deciding the
    band/acceptance-count trigger. Returns None for the same "cannot
    usefully split" case ``_apply_splits`` flags as ``unsplittable_flag``:
    fewer than 2 acceptance clusters, where a split would produce one child
    carrying everything the parent already carried.
    """
    clusters = _cluster_acceptance(task.acceptance, task.files_hint)
    if len(clusters) < 2:
        return None
    ids = used_ids if used_ids is not None else {task.id}
    return _split_task(task, clusters, ids)


<<<END TG_TO>>>

<<<BEGIN TGT_IMPORT_FROM>>>
    normalize_plan,
)
<<<END TGT_IMPORT_FROM>>>

<<<BEGIN TGT_IMPORT_TO>>>
    normalize_plan,
    split_one_task,
)
<<<END TGT_IMPORT_TO>>>

<<<BEGIN TGT_TESTS_FROM>>>
def test_invalid_split_band_is_rejected_loudly() -> None:
    with pytest.raises(ValueError, match="split_band"):
        GranularityConfig(split_band="huge")


<<<END TGT_TESTS_FROM>>>

<<<BEGIN TGT_TESTS_TO>>>
def test_invalid_split_band_is_rejected_loudly() -> None:
    with pytest.raises(ValueError, match="split_band"):
        GranularityConfig(split_band="huge")


def test_split_one_task_splits_by_acceptance_clusters() -> None:
    task = _task("T1", acceptance=["one", "two", "three", "four"], band="XL")

    children = split_one_task(task)

    assert children is not None
    assert [c.id for c in children] == ["T1a", "T1b", "T1c", "T1d"]
    assert [c.acceptance for c in children] == [["one"], ["two"], ["three"], ["four"]]


def test_split_one_task_returns_none_when_unsplittable() -> None:
    task = _task("T1", acceptance=["ship it"], band="XL")

    assert split_one_task(task) is None


def test_split_one_task_avoids_collisions_against_a_supplied_used_ids_set() -> None:
    task = _task("T1", acceptance=["one", "two"], band="XL")
    used = {"T1", "T1a"}

    children = split_one_task(task, used_ids=used)

    assert children is not None
    assert [c.id for c in children] == ["T1ax", "T1b"]
    assert used == {"T1", "T1a", "T1ax", "T1b"}


def test_split_one_task_matches_apply_splits_output_for_the_same_task() -> None:
    """No forked heuristic: the plan-time path (`normalize_plan`) and this
    single-task seam produce identical children for the same task."""
    plan = _plan([_task("T1", acceptance=["one", "two", "three", "four"], band="XL")])
    via_plan = normalize_plan(plan, GranularityConfig())

    via_seam = split_one_task(
        _task("T1", acceptance=["one", "two", "three", "four"], band="XL")
    )

    assert via_seam is not None
    assert list(via_plan.plan.tasks) == via_seam


<<<END TGT_TESTS_TO>>>

Gates (run every one for real, record exact output; exactly 8):

G1 TRANSPORT: byte-equality of `.agent/authored/f112-r5.md` and
`.agent/last_block.md` → equal.

G2 PLAN: extract PLAN5 from the committed authored file (between its
markers, programmatically, never retyped), byte-compare against
`.agent/plan.md` → equal. `wc -l .agent/plan.md` → must be < 50.
`grep -c '^## Goal' .agent/plan.md` → 1. `grep -c '^## Next Steps'
.agent/plan.md` → 1.

G3 FIX (R-0792): count occurrences of the line `    ClassBudgetFit,` in
`tests/orchestration/test_context_compiler.py` — must read 1 BEFORE the
fix commit and 0 AFTER. `ruff check tests/orchestration/test_context_compiler.py`
(or `python3 -m ruff check` if the bare binary is denied) → must read
clean AFTER the fix, and must show the F401 BEFORE it (run it once before
applying FIX, to prove the defect was real and not assumed).

G4 LEDGER: measure `.agent/live_review.md` size in bytes IMMEDIATELY
BEFORE the append commit (must read 2252567 — if it does not, STOP and
report the discrepancy). Extract RECORD4 from the committed authored file
programmatically; confirm its own byte length is 2300, zero internal
newlines, last byte a newline. Append as
`content_bytes + b"\n\n" + RECORD4_bytes` (matching round 4's own
convention exactly — note round 4 declared that this exact formula
produces a 3-newline gap rather than 2 when the base already ends in its
own trailing newline; apply the SAME formula again for consistency with
the established mechanical convention, and if the same shape mismatch
recurs, declare it in `.agent/prose_slips.md` exactly as round 4 did,
bundled into this commit, rather than deviating from the formula).
Confirm post-size == 2252567 + 2 + 2300 == 2254869 exactly.

G5 PRODUCTION CODE: `git show <BASE_SHA>:packages/orchestration/task_granularity.py`
into scratch, apply TG_FROM→TG_TO via `content.replace(FROM, TO, 1)`,
byte-compare the result against the committed
`packages/orchestration/task_granularity.py` → equal. Then
`ruff check packages/orchestration/task_granularity.py` (or the module
form) → must read clean.

G6 TEST FILE: same reconstruction technique — base blob of
`tests/orchestration/test_task_granularity.py` at BASE_SHA, apply
TGT_IMPORT_FROM→TGT_IMPORT_TO then TGT_TESTS_FROM→TGT_TESTS_TO in that
order, byte-compare against the committed file → equal. Then
`python3 -m pytest tests/orchestration/test_task_granularity.py -q` →
every test passes (report the exact count), and confirm by name that all
4 new tests ran and passed (`-k "split_one_task" -v`).

G7 MUTATION RED-PROOF (disposable git worktree only, never the primary
checkout — print the worktree's own module `__file__` path before
trusting any reading): inside the worktree, confirm the EXACT string
`    if len(clusters) < 2:\n        return None\n` (4-space indent —
this is `split_one_task`'s own line; `_apply_splits` has a
DIFFERENTLY-INDENTED occurrence of the bare substring `if len(clusters) < 2:`,
so match the indentation exactly to hit only the new function) occurs
exactly once in the file, then change that one `< 2` to `< 1`. Run
`python3 -m pytest <worktree>/tests/orchestration/test_task_granularity.py -q`
and confirm exactly ONE test fails, named
`test_split_one_task_returns_none_when_unsplittable`. Revert the
mutation, byte-compare the reverted file against the primary checkout's
copy to confirm exact match, re-run and confirm full green again. Remove
the worktree. `git status --porcelain` on the PRIMARY checkout must read
empty immediately after the mutation step and again after cleanup.

G8 FINAL (state readers, canary, tree, commits, sweep): four state
readers as four separate invocations —
`python3 -m pytest tests/ui_server/ -q`,
`python3 -m pytest tests/orchestration/test_test_runner.py -q`,
`python3 -m pytest tests/regression/test_resource_safety.py -q`,
`python3 -m pytest tests/orchestration/test_integrity_gate.py -q` — plus
the canary `python3 -m pytest tests/cli/test_golden_path.py -q`, each
reported with its real pass count. Then `git status --porcelain` empty
immediately before the handback commit is staged; `git ls-files
.remedy-wt` empty; per-commit `git show --numstat` `+` column for every
commit before the handback, cross-checked cell-by-cell against the
Commits table in your own handback; one staleness-sweep line per file
this round touched.

Commits, in this exact order:
- C0a: save the block verbatim to `.agent/authored/f112-r5.md`.
- C0b: mirror to `.agent/last_block.md`.
- C1: apply PLAN5 to `.agent/plan.md`.
- C2: apply FIX_FROM→FIX_TO to
  `tests/orchestration/test_context_compiler.py` (R-0792's fix).
- C3: append RECORD4 to `.agent/live_review.md` (declare the G4 shape
  note in `.agent/prose_slips.md` in the SAME commit if it recurs, per
  round 4's own precedent).
- C4: apply TG_FROM→TG_TO to
  `packages/orchestration/task_granularity.py`.
- C5: apply TGT_IMPORT and TGT_TESTS pairs to
  `tests/orchestration/test_task_granularity.py`.
- C6: the round 5 handback (rewrite `.agent/handoff.md`, commit, push).

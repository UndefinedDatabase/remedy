── STEP T003a/5 — F112 ────────────────────────────────────────
Goal: Book round 5's verdict, record DECISION F112 D1 splitting T003
into T003a/T003b (an investigation finding: the real dispatch loop has
no task_class on its task objects, never activates compiled-context
mode, and its JobPlan has no durable metadata field at all — so
`enqueue_task_decision`'s write would silently vanish on resume), then
ship T003a: a durable `metadata` field on `JobPlan`.

Bundle:
1. Book RECORD5 (round 5's verdict) into `.agent/live_review.md`.
2. Record DECISION F112 D1 into `.agent/decisions.md`.
3. Add a `metadata: dict` field to `JobPlan`
   (`packages/orchestration/pingpong_job.py`), exported/imported like
   `input_snapshot` already is.
4. Add 2 tests to `tests/orchestration/test_job_task_runner.py`
   confirming the field round-trips through persist/load and defaults
   to an empty dict.

Change: exactly the 4 files named above, plus `.agent/plan.md`,
`.agent/authored/f112-r6.md` and `.agent/last_block.md`. Nothing else —
in particular, do NOT touch `docs/roadmap/features/T3_F112.md` this
round (the DECISION is the durable record instead; editing the feature
file would trigger the docs-round gate for no reason this round).

Constraints:
- Do NOT touch anything in `_export_job`/`_import_job` other than the
  three named insertions — every other field's export/import logic is
  untouched.
- Every pair below is APPEND-shaped UNLESS its own instructions say
  otherwise: apply as `content = content.replace(FROM, TO, 1)` — FROM
  occurs exactly once in the current file, TO contains FROM as a
  literal prefix.
- RECORD5 is ONE line (no internal newlines) ending in exactly one
  trailing newline, matching every existing `Gate:` entry's shape in
  `.agent/live_review.md`.
- DECISION_F112_D1 is a MULTI-PARAGRAPH text (7 paragraphs: the heading
  line, then CONTEXT/MEASURED/CHOSEN/ALTERNATIVE CONSIDERED AND
  REJECTED/CONSEQUENCE/REVERSE), each paragraph separated from the next
  by exactly one blank line (matching every existing `## DECISION ...`
  entry's shape in `.agent/decisions.md`), and the whole text ends in
  exactly one trailing newline.
- IMPORTANT — the append formula for BOTH `.agent/live_review.md` and
  `.agent/decisions.md` in THIS round is `content_bytes + b"\n" +
  SLICE_bytes` — ONE newline byte, not two. (Rounds 4 and 5 used a
  `+ b"\n\n"` formula that produced an extra blank line each time,
  because the base file already ends in its own trailing newline; that
  was declared both times in `.agent/prose_slips.md` as a no-product-
  effect shape mismatch and is NOT being corrected retroactively — the
  append-only rule forbids rewriting landed entries. This round simply
  uses the CORRECT one-newline formula going forward, matching the
  files' own pre-existing convention, rather than repeating the same
  shape mismatch a third time.)
- `.agent/plan.md` stays under 50 lines (AGENTS.md).
- ruff availability is inconsistent this session: try the bare `ruff`
  binary first, fall back to `python3 -m ruff check <path>` if denied,
  then `subprocess.run([...])` inside `python3 -c` if both are denied
  as direct Bash invocations; report which one worked.

Done when: every gate in "Gates" below is run for real and its exact
output recorded in the handback; all 7 commits (C0a-C5) plus the
handback commit (C6) land in the stated order; tree is clean; branch is
pushed.

Handback: completion report + rewrite `.agent/handoff.md` per
AGENTS.md's `### handoff.md` section and
docs/agents/handback_template.md.
──────────────────────────────────────────────────────────────

<<<BEGIN PLAN6 (whole-file replacement of .agent/plan.md)>>>
# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001 and T002 complete as of round 4;
T003a (JobPlan.metadata persistence) complete as of round 6.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 6, session 2 — books round 5's verdict, records DECISION F112 D1
(`.agent/decisions.md`) splitting T003 into T003a/T003b after
investigation found the dispatch loop `pingpong_job.py` uses has no
`task_class` on its task objects, never passes compiled-context params to
`run_pingpong`, and its `JobPlan` has no durable `metadata` field at all
— so `enqueue_task_decision`'s write would silently vanish on resume.
This round ships T003a: a `metadata: dict` field on `JobPlan`, exported
and imported like `input_snapshot`, with a persistence round-trip test.

## Next Steps

- T003b: derive a `task_class` for a live `TaskEntry` (no existing
  precedent to reuse — every current caller supplies task_class as a bare
  string; investigate whether a title/body heuristic or a new field is
  right), wire `compiled_context_paths`/`compiled_context_candidates`
  into `pingpong_job.py`'s `run_pingpong(...)` call, then call
  `fit_task_context_to_class_cap` and `enqueue_task_decision` between
  `_build_task_prompt` and `task.status = TASK_RUNNING`
  (`pingpong_job.py`, per-task loop) — before the F006 checkpoint block,
  never after. `safe_default="split task"` via `auto_apply_safe_default`
  when unattended; omit the option when `split_one_task` returns None.
- Acceptance fixtures, the integration gate, then closure.

## Risks

- T003b remains the highest-risk remaining slice — a live dispatch loop
  plus a persistence-format change together. Its own round, call site
  re-read first.
- `R-0767` stays OPEN on the model-routing seam this feature's config
  pattern borrows from; unrelated to F112, not absorbed.
- ruff is inconsistent this session; `python3 -m ruff check <path>` is
  the reliable form, re-measured every round.
<<<END PLAN6>>>

<<<BEGIN RECORD5 (append to .agent/live_review.md)>>>
Gate: F112 R5 — the round 5 entry. VERDICT PASS, over the range `a4c2570d..7d7a0904` plus the handback commit `65ded999`, independently re-verified by the reviewer. THE FIX HELD: R-0792's removal of the unused `ClassBudgetFit` import from `tests/orchestration/test_context_compiler.py` reproduced by the reviewer as a byte-exact diff (`git diff a4c2570d..HEAD` shows exactly the one line removed), and `python3 -m ruff check tests/orchestration/test_context_compiler.py` reproduced as `All checks passed!`. THE PRODUCTION CODE HELD: `split_one_task` in `packages/orchestration/task_granularity.py` reproduced byte-exact against the round's own TG_FROM/TG_TO pair, and `python3 -m ruff check packages/orchestration/task_granularity.py` reproduced as `All checks passed!`. THE TESTS HELD: `python3 -m pytest tests/orchestration/test_task_granularity.py -q` reproduced by the reviewer at 30 passed. THE CANARY HELD: `pytest tests/cli/test_golden_path.py -q` reproduced at 42 passed. `.agent/plan.md` reproduced at 46 lines with `## Goal` and `## Next Steps` both present. `.agent/live_review.md` reproduced at 2254869 bytes immediately before this entry, matching round 5's own pinned G4 figure exactly. ONE PROSE-ONLY DEVIATION round 5 declared is correctly classified, not a finding: the block's own claim that the TGT_IMPORT_FROM/TGT_IMPORT_TO pair was append-shaped was wrong, since the new line inserts before the closing paren and TO does not contain FROM as a literal prefix — the worker correctly caught and declared this per checklist item 15, with zero effect on the actual byte-for-byte reconstruction proof, which held regardless of the label. NO FINDING IS OWED BY THIS ROUND: R-0792 was registered and resolved within round 5 itself, and this booking introduces none new.
<<<END RECORD5>>>

<<<BEGIN DECISION_F112_D1 (append to .agent/decisions.md)>>>
## DECISION F112 D1 (2026-09-03, F112 R6) — T003's dispatch-loop wiring is narrower this round than the feature file's Design section assumed; scope splits into T003a (this round) and T003b (deferred)

CONTEXT. T3_F112.md's Design section describes T003 as adding `enqueue_task_decision` at the point a task's `cannot_fit` outcome is known, with the split option seeded from the granularity machinery. Investigation before this round (reviewer, read-only, over `packages/orchestration/pingpong_job.py`, `pingpong_loop.py`, `escalation.py`, `long_run_executor.py`, `packages/core/models.py`) found three gaps the Design section does not name: (1) `run_pingpong`'s compiled-context parameters (`compiled_context_paths`/`compiled_context_candidates`) are never passed by `pingpong_job.py`'s per-task dispatch loop — the loop the feature actually needs to reach — so T002's `fit_task_context_to_class_cap` has no live caller today; (2) no `task_class` value is attached to a `TaskEntry`/`Task` at dispatch time anywhere in the codebase — F110's `task_class` is a bare string every existing caller supplies itself, never read off a task object; (3) `JobPlan` (the job type this loop persists via `_persist_job`/`_export_job`/`_import_job`) has no `metadata` field at all, so `enqueue_task_decision`'s `job.metadata["escalations"]` write would succeed in-process (via `escalation.py`'s `_metadata()` fallback) and then silently vanish on the next persist/resume cycle — a durability gap, not merely an unwired seam.

MEASURED. `grep -n "compiled_context_paths\|compiled_context_candidates" packages/orchestration/pingpong_job.py` returns zero hits. `packages/core/models.py` `Task` fields are `id, description, inputs, acceptance_checks, budget, status, output_artifact_ids` — no task_class. `packages/orchestration/pingpong_job.py`'s `JobPlan` dataclass (lines 202-277) has no `metadata` field; `_export_job`/`_import_job` (lines 530-718) name every persisted field explicitly and neither names `metadata`.

CHOSEN. Split T003 into T003a and T003b rather than attempt the full wiring in one round. T003a (this round): add a durable `metadata: dict` field to `JobPlan`, exported and imported like `input_snapshot` already is, with a round-trip test — the prerequisite `enqueue_task_decision` needs to persist correctly from this loop at all. T003b (a later round, after task_class derivation and compiled-context activation are separately designed): the actual `cannot_fit` → `enqueue_task_decision` call, inserted at the exact spot identified between `_build_task_prompt` and `task.status = TASK_RUNNING` in `pingpong_job.py`'s per-task loop.

ALTERNATIVE CONSIDERED AND REJECTED. Attempt the full wiring in this round, deriving task_class ad hoc (e.g. from task title keywords) and activating compiled-context mode inline. Rejected: three separate, non-trivial design decisions bundled into one round against a live, already-battle-tested per-task dispatch loop and job persistence format is exactly the kind of change AGENTS.md's Change Size Limits and this feature's own "Do not touch" boundary counsel against rushing; a wrong task_class heuristic or a persistence-format slip would cost far more to unwind than the round saves.

CONSEQUENCE. `docs/roadmap/features/T3_F112.md` is not edited this round (avoiding the docs-round gate for an in-progress feature file); this DECISION is the durable record instead, per AGENTS.md's decisions.md purpose ("temporary decisions that may later move to docs/"). `.agent/plan.md`'s Next Steps names task_class derivation and compiled-context activation as T003b's remaining open design questions.

REVERSE by deleting this DECISION and treating T003 as a single unsplit task again.
<<<END DECISION_F112_D1>>>

<<<BEGIN PPJ_FIELD_FROM>>>
    budget_prediction: dict | None = None
<<<END PPJ_FIELD_FROM>>>

<<<BEGIN PPJ_FIELD_TO>>>
    budget_prediction: dict | None = None
    # F112 T003: durable escalation/decision state (e.g. `enqueue_task_decision`'s
    # `job.metadata["escalations"]` list) — a plain dict, exported and imported
    # verbatim like `input_snapshot` above so a cannot_fit decision survives a
    # persist/resume cycle instead of vanishing as a Python-only attribute.
    metadata: dict = field(default_factory=dict)
<<<END PPJ_FIELD_TO>>>

<<<BEGIN PPJ_EXPORT_FROM>>>
        "budget_prediction": job.budget_prediction,
<<<END PPJ_EXPORT_FROM>>>

<<<BEGIN PPJ_EXPORT_TO>>>
        "budget_prediction": job.budget_prediction,
        "metadata": job.metadata,
<<<END PPJ_EXPORT_TO>>>

<<<BEGIN PPJ_IMPORT_FROM>>>
        budget_prediction=data.get("budget_prediction"),
    )
<<<END PPJ_IMPORT_FROM>>>

<<<BEGIN PPJ_IMPORT_TO>>>
        budget_prediction=data.get("budget_prediction"),
        metadata=dict(data.get("metadata") or {}),
    )
<<<END PPJ_IMPORT_TO>>>

<<<BEGIN TEST_IMPORT_FROM>>>
    run_job,
    validate_job_task_result,
<<<END TEST_IMPORT_FROM>>>

<<<BEGIN TEST_IMPORT_TO>>>
    run_job,
    save_job_plan,
    validate_job_task_result,
<<<END TEST_IMPORT_TO>>>

<<<BEGIN TEST_APPEND_FROM (NOT append-shaped for the outer pair — see note)>>>
    def test_load_nonexistent(self, isolate_data_root):
        assert load_job_plan("nonexistent_id") is None

<<<END TEST_APPEND_FROM>>>

<<<BEGIN TEST_APPEND_TO>>>
    def test_load_nonexistent(self, isolate_data_root):
        assert load_job_plan("nonexistent_id") is None

    def test_metadata_round_trips_through_persist_and_load(self, isolate_data_root):
        job = parse_job_file(_TWO_TASK_JOB, "/tmp/repo")
        job.metadata["escalations"] = [{"decision_id": "D1", "status": "open"}]
        save_job_plan(job)

        loaded = load_job_plan(job.job_id)

        assert loaded is not None
        assert loaded.metadata == {"escalations": [{"decision_id": "D1", "status": "open"}]}

    def test_metadata_defaults_to_an_empty_dict(self, isolate_data_root):
        job = parse_job_file(_TWO_TASK_JOB, "/tmp/repo")

        loaded = load_job_plan(job.job_id)

        assert loaded is not None
        assert loaded.metadata == {}

<<<END TEST_APPEND_TO>>>

Gates (run every one for real, record exact output; exactly 8):

G1 TRANSPORT: byte-equality of `.agent/authored/f112-r6.md` and
`.agent/last_block.md` → equal.

G2 PLAN: extract PLAN6 from the committed authored file (between its
markers, programmatically, never retyped), byte-compare against
`.agent/plan.md` → equal. `wc -l .agent/plan.md` → must be < 50.
`grep -c '^## Goal' .agent/plan.md` → 1. `grep -c '^## Next Steps'
.agent/plan.md` → 1.

G3 LEDGER (RECORD5): measure `.agent/live_review.md` size in bytes
IMMEDIATELY BEFORE the append commit (must read 2254869 — if it does
not, STOP and report). Extract RECORD5 from the committed authored file
programmatically; confirm its own byte length is 1787, zero internal
newlines, last byte a newline. Append as `content_bytes + b"\n" +
RECORD5_bytes` (ONE newline — see the block's constraint above). Confirm
post-size == 2254869 + 1 + 1787 == 2256657 exactly. Second reader: split
the whole post-append file on `\n\n` and confirm the last unit equals
RECORD5 exactly. Negative control: flip one byte inside RECORD5's own
text (in-memory only) and confirm the second reader then rejects it.

G4 DECISION (DECISION_F112_D1): measure `.agent/decisions.md` size in
bytes IMMEDIATELY BEFORE the append commit (must read 742368 — if it
does not, STOP and report). Extract DECISION_F112_D1 from the committed
authored file programmatically; confirm its own byte length is 3737,
ends in exactly one trailing newline, and splits into exactly 7
paragraphs on `\n\n`. Append as `content_bytes + b"\n" +
DECISION_bytes` (ONE newline). Confirm post-size == 742368 + 1 + 3737 ==
746106 exactly. Second reader (per checklist item 36 — the region has
more than one paragraph): split the WHOLE post-append file on `\n\n`
and confirm the LAST 7 units equal DECISION_F112_D1's own 7 paragraphs,
in order, exactly. Negative control: flip one byte inside the FIRST of
those 7 paragraphs (in-memory only, on a copy) and confirm the second
reader then rejects it.

G5 PRODUCTION CODE: `git show <BASE_SHA>:packages/orchestration/pingpong_job.py`
into scratch, apply PPJ_FIELD_FROM→PPJ_FIELD_TO, then
PPJ_EXPORT_FROM→PPJ_EXPORT_TO, then PPJ_IMPORT_FROM→PPJ_IMPORT_TO, each
via `content.replace(FROM, TO, 1)`, in that exact order; byte-compare
the result against the committed
`packages/orchestration/pingpong_job.py` → equal. Then
`ruff check packages/orchestration/pingpong_job.py` (module form or
subprocess fallback if denied) → must read clean.

G6 TEST FILE: same reconstruction technique — base blob of
`tests/orchestration/test_job_task_runner.py` at BASE_SHA, apply
TEST_IMPORT_FROM→TEST_IMPORT_TO then TEST_APPEND_FROM→TEST_APPEND_TO in
that order, byte-compare against the committed file → equal. Then
`python3 -m pytest tests/orchestration/test_job_task_runner.py -q` →
every test passes (report the exact count — this is a large, widely-
used test file, so a regression anywhere in it matters), and confirm by
name that both new tests ran and passed (`-k "metadata" -v`).

G7 MUTATION RED-PROOF (disposable git worktree only, never the primary
checkout — print the worktree's own module `__file__` path before
trusting any reading): inside the worktree, confirm the exact line
`        metadata=dict(data.get("metadata") or {}),` occurs exactly
once in the file, then change it to `        metadata={},` (always
discard persisted metadata). Run
`python3 -m pytest <worktree>/tests/orchestration/test_job_task_runner.py -q -k metadata`
and confirm exactly ONE test fails, named
`test_metadata_round_trips_through_persist_and_load` (the
defaults-to-empty-dict test must still pass, since `{}` is still its
expected result). Revert the mutation, byte-compare the reverted file
against the primary checkout's copy to confirm exact match, re-run and
confirm both pass again. Remove the worktree. `git status --porcelain`
on the PRIMARY checkout must read empty immediately after the mutation
step and again after cleanup.

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
- C0a: save the block verbatim to `.agent/authored/f112-r6.md`.
- C0b: mirror to `.agent/last_block.md`.
- C1: apply PLAN6 to `.agent/plan.md`.
- C2: append RECORD5 to `.agent/live_review.md`.
- C3: append DECISION_F112_D1 to `.agent/decisions.md`.
- C4: apply PPJ_FIELD, PPJ_EXPORT and PPJ_IMPORT pairs (in that order)
  to `packages/orchestration/pingpong_job.py`.
- C5: apply TEST_IMPORT and TEST_APPEND pairs to
  `tests/orchestration/test_job_task_runner.py`.
- C6: the round 6 handback (rewrite `.agent/handoff.md`, commit, push).

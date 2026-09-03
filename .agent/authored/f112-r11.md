## Authored texts

The block below (from "===AUTHORED BLOCK START===" to "===AUTHORED BLOCK END===") is what you save verbatim to `.agent/authored/f112-r11.md` in commit C0a.

===AUTHORED BLOCK START===

RECORD10 (append to .agent/live_review.md, one-newline formula — `content_bytes + b"\n" + RECORD10_bytes`, 2232 bytes):

Gate: F112 R10 — the round 10 entry. VERDICT PASS, over the range `58cfae0e..0ec9d2b9` (commits C0a through C6), independently reviewed by the reviewer at the start of session 4's round 11. THE PASSTHROUGH HELD: `git show c2bbc5f9 -- packages/orchestration/pingpong_loop.py` reproduced the exact Pair A (APPEND, compiled_context_token_budget parameter) and Pair B (REWRITE, conditional token_budget kwarg) C4 describes; `git show c2bbc5f9 -- tests/orchestration/test_pingpong.py` reproduced the exact TestCompiledContextTokenBudget class with its two tests. THE ADAPTER HELD: `git show 01864da1 -- packages/orchestration/pingpong_job.py` reproduced the task_entry_to_planned_task function plus the declared TYPE_CHECKING-guarded-import deviation (verified against the cited packages/orchestration/approval_queue.py precedent); `git show 01864da1 -- tests/orchestration/test_job_task_runner.py` reproduced the exact TestTaskEntryToPlannedTaskAdapter class (4 tests) and the two import-list REWRITE pairs. THE LEDGER APPENDS HELD BYTE-IDENTICAL: `.agent/authored/f112-r10.md` and `.agent/last_block.md` compare equal; `.agent/plan.md` (47 lines) matches PLAN10 exactly; `.agent/decisions.md`'s tail matches DECISION F112 D3 exactly; `.agent/live_review.md`'s tail matches RECORD9 exactly. THE TESTS HELD: `python3 -m pytest tests/orchestration/test_pingpong.py tests/orchestration/test_job_task_runner.py -q` reproduced at 236 passed. THE LINT HELD: `python3 -m ruff check packages/orchestration/pingpong_loop.py packages/orchestration/pingpong_job.py tests/orchestration/test_pingpong.py tests/orchestration/test_job_task_runner.py` read "All checks passed!". THE CANARY HELD: `pytest tests/cli/test_golden_path.py -q` reproduced at 42 passed. THE MUTATION CLEANUP HELD: `git worktree list` showed neither `f112-r10-mutation-c4` nor `f112-r10-mutation-c5`, and `git status --porcelain` read empty in the primary checkout both before this reading and throughout — the mutation runs themselves were not re-executed by the reviewer this round, corroborated by the handback's own detailed before/after transcripts (both directions of each guard reported) and by the clean worktree list, the same honesty shape as the digest fallback.

<<<END RECORD10>>>

PLAN11 (whole-file replacement of .agent/plan.md, no trailing newline, 2321 bytes):

# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001/T002/T003a/T003b1/T003b2a
complete and green as of round 10.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 11, session 4 — fresh investigation over T003b2b's own call site
(escalation.py's enqueue_task_decision/auto_apply_safe_default, the
piece T003b2a deliberately left untouched) found a second latent
incompatibility beyond DECISION F112 D2/D3's: _record_answer_on_task
reads task.id and task.inputs, fields pingpong JobPlan's TaskEntry has
never carried (only Core Job's Task has them) — calling
auto_apply_safe_default against a live JobPlan would raise
AttributeError (DECISION F112 D4). T003b2b splits into T003b2b1 (this
round: the escalation.py dual-shape fix + a new TaskEntry.inputs field)
and T003b2b2 (deferred: the live call-site wiring, now safe to build).

## Next Steps

- T003b2b2 (own dedicated round(s)): call fit_task_context_to_class_cap
  between _build_task_prompt and task.status = TASK_RUNNING; wire
  compiled_context_paths/candidates/token_budget into run_pingpong; on
  cannot_fit call enqueue_task_decision (options=["split task"] only
  when task_entry_to_planned_task(task) is not None and
  split_one_task on its result returns non-None) then
  auto_apply_safe_default under --yes, reading the answer off the
  returned record directly rather than off task.inputs (same
  dispatch-loop iteration, no resume needed for this path).
- Acceptance fixtures, the integration gate, then closure.

## Risks

- T003b2b2 is still the highest-risk remaining slice — first-time
  wiring against the live dispatch loop; re-read the call site fresh
  again before authoring it, per DECISION F112 D2/D3/D4.
- R-0767 stays OPEN on the model-routing seam this feature's config
  pattern borrows from; unrelated to F112, not absorbed.
- ruff is inconsistent this session; python3 -m ruff check <path> is the
  reliable form, re-measured every round.

<<<END PLAN11>>>

DECISION F112 D4 (append to .agent/decisions.md, one-newline formula, 5001 bytes):

## DECISION F112 D4 (2026-09-03, F112 R11) — escalation.py's _record_answer_on_task assumes Core Job's Task shape (task.id, task.inputs), which pingpong JobPlan's TaskEntry has never carried; T003b2b splits into T003b2b1 (this round) and T003b2b2 (deferred)

CONTEXT. DECISION F112 D3 (F112 R10) narrowed T003b2b to three pieces: the fit_task_context_to_class_cap call, the run_pingpong wiring, and the cannot_fit -> enqueue_task_decision -> auto_apply_safe_default chain. Fresh investigation this round (reviewer, read-only, over packages/orchestration/escalation.py's enqueue_task_decision/answer_task_decision/auto_apply_safe_default/_record_answer_on_task/_metadata, and packages/orchestration/pingpong_job.py's TaskEntry/JobPlan) found that the third piece cannot run against a live JobPlan today: auto_apply_safe_default unconditionally calls answer_task_decision, which unconditionally calls _record_answer_on_task, which reads task.id and task.inputs on every task in job.tasks — attributes Core Job's packages.core.models.Task carries (id: UUID, inputs: dict) that pingpong JobPlan's TaskEntry has never had (it carries task_id: str instead, and no inputs field of any kind). Calling the decision chain from the dispatch loop as D3 left it planned would raise AttributeError the first time a JobPlan's cannot_fit task tried to auto-apply its safe default.

MEASURED. escalation.py:102-115's _metadata() helper already documents and enacts dual-shape support — "Both Core Job and the pingpong JobPlan are accepted" — reading job.metadata via getattr with a graceful empty-dict fallback; a repo-wide grep confirms pingpong_job.py's JobPlan already carries a metadata: dict field (added ahead of this feature, comment at pingpong_job.py:320-323: "F112 T003: durable escalation/decision state... job.metadata[\"escalations\"] list"), so enqueue_task_decision's own write path (_stored_records, via _metadata) already works unmodified against a JobPlan. _record_answer_on_task (escalation.py:258-273) was never given the same dual-shape treatment: `str(task.id) != task_id` (line 266) has no getattr fallback, and `task.inputs` (line 268) assumes a dict field that does not exist on TaskEntry at all — confirmed by TaskEntry's full field list (pingpong_job.py:119-143), which has no `inputs` entry. No test in tests/orchestration/test_escalation.py constructs a JobPlan and calls any escalation.py function against it (grep for "JobPlan(" in that file: zero matches) — the dual-shape claim is proven for _metadata alone and untested for the answer-recording path.

CHOSEN. Split T003b2b into T003b2b1 and T003b2b2. T003b2b1 (this round): add `inputs: dict = field(default_factory=dict)` to TaskEntry, exported/imported like `task_class` (T003b1 precedent, same position — immediately after task_class in the field list, the export dict and the import call); fix `_record_answer_on_task` to resolve a task's identifier via `getattr(task, "id", None)` falling back to `getattr(task, "task_id", None)`, matching `_metadata()`'s own already-established "accept either shape" contract, with a new test in tests/orchestration/test_escalation.py proving the full enqueue_task_decision -> auto_apply_safe_default -> answer_task_decision chain against a real JobPlan/TaskEntry (not just Core Job). T003b2b2 (a later round): the live call-site wiring alone — fit_task_context_to_class_cap, the run_pingpong parameter wiring, and the cannot_fit decision call — now safe to build on a working escalation path instead of discovering the AttributeError mid-round.

ALTERNATIVE CONSIDERED AND REJECTED. Have the dispatch loop read the answer directly off the returned `record` dict (both enqueue_task_decision and auto_apply_safe_default return the record) and skip calling auto_apply_safe_default's task-recording side effect entirely, avoiding the crash without touching escalation.py. Rejected: auto_apply_safe_default calls answer_task_decision internally regardless of what the caller does with its return value, and answer_task_decision unconditionally calls _record_answer_on_task before returning — there is no call shape that reaches "the safe default is recorded as this decision's answer" without also reaching the AttributeError; the crash is not avoidable from the call site, only by fixing the function.

CONSEQUENCE. .agent/plan.md Next Steps is rewritten to name T003b2b1 (this round's scope) then T003b2b2 with the three-piece live-wiring list, now noting it should read the auto-applied answer off the returned record directly (same dispatch-loop iteration, no resume dependency on task.inputs). docs/roadmap/features/T3_F112.md stays unedited: its Design section names enqueue_task_decision as reused machinery without describing escalation.py's internals, so this fix contradicts no sentence there.

REVERSE by deleting this DECISION, reverting the TaskEntry.inputs field and the _record_answer_on_task fix, and treating T003b2b as D3 left it (a single three-piece round).

<<<END D4>>>

===AUTHORED BLOCK END===

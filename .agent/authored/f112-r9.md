## Authored texts

The block below (from "===AUTHORED BLOCK START===" to "===AUTHORED BLOCK END===") is what you save verbatim to `.agent/authored/f112-r9.md` in Step 0.

===AUTHORED BLOCK START===

RECORD8 (append to .agent/live_review.md, one-newline formula, 1786 bytes):

Gate: F112 R8 — the round 8 entry. VERDICT PASS, over the range `e5add7cd..00b02a4d` plus the handback commit `66401f61`, independently re-verified by the reviewer at the start of session 3 rather than at round 8's own end (session 2 ended at round 8 per its own strong recommendation; session 3 opened by re-reading this same range from disk, per docs/agents/self_drive_protocol.md Phase 0 and Phase 1 rule 4). THE FIX HELD: `git diff e5add7cd..HEAD -- tests/orchestration/test_f018_authority_integration.py` reproduced by the reviewer as the exact 7-line diff the handback's C2 describes (docstring rewrite plus the explicit `del job.metadata`), and `python3 -m pytest tests/orchestration/test_f018_authority_integration.py -q` reproduced at 114 passed. THE LINT HELD: `python3 -m ruff check tests/orchestration/test_f018_authority_integration.py` reproduced as `All checks passed!`. THE LEDGER APPEND HELD: RECORD7, appended in round 8's own C3, matches the tail of this file exactly at the byte offset round 8's own G4 pinned. THE CANARY HELD: `pytest tests/cli/test_golden_path.py -q` reproduced at 42 passed. THE FULL-FEATURE SPOT CHECK HELD: `python3 -m pytest tests/orchestration/test_class_prompt_budget.py tests/orchestration/test_context_compiler.py tests/orchestration/test_task_granularity.py -q` reproduced at 123 passed (24+69+30), matching round 8's own G6 figures. `.agent/plan.md` reproduced at 46 lines with `## Goal` and `## Next Steps` both present. `git status --porcelain` read empty at the start of this session, before any round-9 work began. NO FINDING IS OWED BY THIS BOOKING: it is a record of round 8's already-true verdict, carried forward into round 9's first substantive commit per amend0827-process-diet rule 1 rather than spending a round of its own.

<<<END RECORD8>>>

PLAN9 (whole-file replacement of .agent/plan.md, no trailing newline, 2053 bytes):

# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001/T002/T003a complete and green as
of round 8.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 9, session 3 — fresh investigation over the T003b call site found a
task-type mismatch DECISION F112 D2 records: split_one_task takes
schemas/models.py's PlannedTask, not pingpong_job.py's own TaskEntry.
T003b splits into T003b1 (this round: task_class field on TaskEntry,
defaulted to "standard_build", exported/imported like T003a's metadata)
and T003b2 (the adapter, call-site wiring and decision enqueue, deferred).

## Next Steps

- T003b2 (own dedicated round(s), fresh investigation already done in
  DECISION F112 D2): a TaskEntry->PlannedTask adapter
  (acceptance.splitlines(), empty files_hint — safe per D2's MEASURED),
  the fit_task_context_to_class_cap call between _build_task_prompt and
  task.status = TASK_RUNNING, wiring its compiled paths into this loop's
  run_pingpong(compiled_context_paths=..., compiled_context_candidates=...),
  and on cannot_fit calling enqueue_task_decision (options=["split task"]
  only when split_one_task via the adapter returns non-None) then
  auto_apply_safe_default under --yes.
- Acceptance fixtures, the integration gate, then closure.

## Risks

- T003b2 is still the highest-risk remaining slice (five first-time-wired
  pieces per DECISION F112 D2) — re-read the call site fresh again before
  authoring it.
- R-0767 stays OPEN on the model-routing seam this feature's config
  pattern borrows from; unrelated to F112, not absorbed.
- ruff is inconsistent this session; python3 -m ruff check <path> is the
  reliable form, re-measured every round.

<<<END PLAN9>>>

DECISION F112 D2 (append to .agent/decisions.md, one-newline formula, 4916 bytes):

## DECISION F112 D2 (2026-09-03, F112 R9) — T003b's granularity-split seam takes a different task type than the dispatch loop owns; scope splits into T003b1 (this round) and T003b2 (deferred)

CONTEXT. `.agent/plan.md`'s T003b entry (set by DECISION F112 D1) calls for deriving a `task_class` for a live `TaskEntry`, wiring `compiled_context_paths`/`compiled_context_candidates` into `pingpong_job.py`'s `run_pingpong` call, then calling `fit_task_context_to_class_cap` and `enqueue_task_decision` between `_build_task_prompt` and `task.status = TASK_RUNNING`, with `safe_default="split task"` via `auto_apply_safe_default` when unattended and the split option omitted when `split_one_task` returns `None`. Fresh investigation this round (reviewer, read-only, over `packages/orchestration/pingpong_job.py`, `context_compiler.py`, `escalation.py`, `task_granularity.py`, `packages/orchestration/schemas/models.py`) found that the granularity machinery's public seam, `split_one_task(task: PlannedTask, ...)`, takes `packages/orchestration/schemas/models.py`'s `PlannedTask` — a plan-time schema carrying `acceptance: list[str]`, `files_hint: list[str]`, `depends_on: list[str]`, `est_tokens_band` and `id`/`goal` fields — while `pingpong_job.py`'s own `TaskEntry` (the dispatch loop's actual per-task type, line 114) carries `acceptance` as a single newline-joined `str` (built at line 807 from `"\n".join(sec["acceptance_lines"])`) and has no `files_hint`, `depends_on` or `est_tokens_band` field at all. T3_F112.md's Design section names "seeding the granularity machinery's split on the task" without naming which task type, and DECISION F112 D1 carried the same gap forward into T003b's plan.md entry unnoticed.

MEASURED. `grep -n "class PlannedTask" packages/orchestration/schemas/models.py` locates it; `grep -n "class TaskEntry" packages/orchestration/pingpong_job.py` locates the dispatch type at line 114 with fields `task_id`, `title`, `body`, `acceptance` (`str`), `status`, and no `files_hint`/`depends_on`/`est_tokens_band`. `_cluster_acceptance` (`task_granularity.py:134-172`) takes `acceptance: list[str]` and `files_hint: list[str]`, and degrades safely to one cluster per acceptance item when `files_hint` is empty (`file_tokens` is then empty, so `matched=[]` for every item and each starts its own cluster) — an empty `files_hint` is a safe, not a broken, input. `run_pingpong` (`pingpong_loop.py:2848`) already declares `compiled_context_paths`/`compiled_context_candidates` keyword parameters; a repo-wide grep over `packages/` and `apps/` found no caller passing either one today. `fit_task_context_to_class_cap` (`context_compiler.py:952-995`) is complete and returns a `ClassBudgetFit(fits, tier1_tokens, cap_tokens, compiled)` T002 already tests.

CHOSEN. Split T003b into T003b1 and T003b2. T003b1 (this round): add `task_class: str = TASK_CLASS_DEFAULT` to `TaskEntry`, exported/imported like `metadata` (T003a precedent), where `TASK_CLASS_DEFAULT = "standard_build"` is a new module constant next to `TaskEntry`'s other string-constant siblings — a fixed, honestly-labeled default (F016's ping-pong build/repair tasks are exactly that seeded `model_routing.TASK_CLASS_TIERS` class) rather than an invented keyword classifier, matching D1's rejection of an ad hoc heuristic. T003b2 (a later round): the adapter from `TaskEntry` to `PlannedTask` (or an equivalent direct `TaskEntry`-shaped clustering path), the `fit_task_context_to_class_cap` call at the D1-pinned dispatch-loop site, the `compiled_context_paths`/`compiled_context_candidates` wiring into this loop's `run_pingpong` call, the `cannot_fit` -> `enqueue_task_decision` call with the split option decided by the adapter's `split_one_task` result, and `auto_apply_safe_default` under `--yes` — five still-untested, first-time-wired pieces against the live dispatch loop, correctly kept together as ONE round's scope but split away from T003b1's single, T003a-precedented field addition.

ALTERNATIVE CONSIDERED AND REJECTED. Build the `TaskEntry`-to-`PlannedTask` adapter, the call-site wiring and the decision-enqueue call in the same round as the `task_class` field. Rejected for the same reason D1 split T003 in the first place: a first-time-tested translation layer against the live dispatch loop, bundled with a second new field and a third new call site, is exactly the AGENTS.md Change Size Limits / Do-not-touch risk D1 already named — T003b1 alone is a full, precedented round; T003b2 is a full, novel one.

CONSEQUENCE. `.agent/plan.md` Next Steps is rewritten to name T003b1 (this round's own scope, done by its own handback) then T003b2 with the five items above, replacing the single T003b entry DECISION F112 D1 left there. `docs/roadmap/features/T3_F112.md` stays unedited this round, per D1's same reasoning.

REVERSE by deleting this DECISION and treating T003b as a single unsplit round again.

<<<END D2>>>

===AUTHORED BLOCK END===

# Context — F112 Prompt budget per task class

## Active Branch
feature/f112-prompt-budget-per-task-class, cut from `main` at the merge
commit of pull request 233.

## Scope
F112 (Tier 3, depends on F103 — done): every task class carries an
input-token cap; the context compiler fits under it via its documented
demotion cascade (distant signatures drop first) with full omission
disclosure; a context that CANNOT fit raises a task-split decision instead
of a truncated prayer. Task slicing: T001 config + validation + the
shared class vocabulary assertion + tests; T002 compiler cap enforcement
+ cannot_fit arithmetic + fixture; T003 the decision wiring + unattended
default (split) + an end-to-end where the split resolves the fit + tests.

## Do not touch
Calibration (F074), the demotion order itself, granularity heuristics
(reused, not modified) — all explicitly out of scope per
`docs/roadmap/features/T3_F112.md` Do not touch. Mid-file truncation stays
forbidden; enforcement lives inside the compiler, never as an outer
truncation.

## Assumptions
- `packages/orchestration/model_routing.TASK_CLASS_TIERS` is the ONE task
  class vocabulary; F112 reuses it rather than declaring a second one, and
  a cap for a class outside it is refused, not silently guessed.
- `packages/orchestration/context_compiler.py` already owns tiered
  selection, budget demotion (`compile_task_context`,
  `DEFAULT_CONTEXT_TOKEN_BUDGET = 24000`) and the omissions record
  (`OmissionRecord`, `write_omitted_context_json`); F112 gives it PER-CLASS
  caps and the hard-floor behavior, T002's job.

## Constraints
The bullets in this first group are STANDING project constraints, carried
forward from the context this file replaced.

- A round touching `docs/roadmap/**` also gates
  `tests/orchestration/test_roadmap_index.py` beside `tests/docs/`.
- A round rewriting `.agent/` state gates the four state readers:
  `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
  `tests/regression/test_resource_safety.py` and
  `tests/orchestration/test_integrity_gate.py`.
- Every handback runs the canary `pytest tests/cli/test_golden_path.py`.
- Destructive verification runs only inside a disposable git worktree,
  never in the primary checkout, which satisfies `git status --porcelain`
  empty at every verdict.
- THE FOUR STATE READERS ARE RUN AS FOUR, NOT AS THREE.
- `ruff check` is DENIED to this session's reviewer, measured at the F112
  claim (`ruff check <path>` answers "This command requires approval").
  F110's opposite constraint was measured for a DIFFERENT session and does
  NOT carry forward. A round of F112 that ships a `.py` file gates
  `python3 -m py_compile <path>` instead, and the worker attempts `ruff
  check` itself, reporting success or the exact refusal.

This round is NOT UI work — no design-reference binding applies.

## Steps
The item-status table for each round lives in that round's handback,
`.agent/handoff.md`, which AGENTS.md's "Completion Report — Item-Status
Table" section requires of every completion report. This file deliberately
does not restate it.

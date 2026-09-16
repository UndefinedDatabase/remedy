# Context — F280 CLI vocabulary v2, part two

## Active Branch
feature/f280-cli-vocabulary-v2-part-two, cut from `main` at
`9f1b6d250e68fb5ee3a2dd39d0a8ffef3eef0792`, the merge commit of pull request 251.

## Scope
F280 (Tier 2; depends on F259 and F261; blocks F266, F268, F269, F270, F271 and F263): what
F261 could not reach inside its soft limit, per DECISION F261 D25. Task slicing per
`docs/roadmap/features/T2_F280.md`: T001 finishes the prune to DECISION amend0905-vocab D4 in the
order of `.agent/f261_t003_inventory.md` rounds J to P, and T002 lands descriptions, role labels,
help wrapping, the visible group order and the catalog tests.

## Do not touch
The concept model (F259 owns the words), the job model (F260 owns what a job is), STATUS
semantics, and the behaviour behind a surviving name: this feature renames and prunes, and the
three places T001 must change a surviving command are each taken by a dated DECISION. Accepted
`[x]` evidence under `docs/roadmap/` stays byte-identical.

## Assumptions
- Cleanliness before compatibility (DECISION D-A of `docs/roadmap/features/T2_F261.md`): no
  alias and no migration shim; a deleted word's id joins `TestDeletedCommands` in
  `tests/test_command_catalog.py` in the same commit.
- A deletion that would break a surviving command is deferred to a round that can rule on it,
  never shipped with a finding.

## Constraints
The bullets below are STANDING project constraints, carried forward from the context this
file replaces.

- A round touching `docs/roadmap/**` also gates
  `tests/orchestration/test_roadmap_index.py` beside `tests/docs/`.
- A round rewriting `.agent/` state gates the four state readers, run as four:
  `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
  `tests/regression/test_resource_safety.py` and
  `tests/orchestration/test_integrity_gate.py`.
- Every handback runs the canary `pytest tests/cli/test_golden_path.py`.
- Destructive verification runs only inside a disposable git worktree, never in the primary
  checkout, which satisfies `git status --porcelain` empty at every verdict.
- Bare `ruff` is DENIED to this session's shell; `python3 -m ruff check <path>` is the spelling
  every gate of this feature orders.
- `remedy` (the built CLI) is DENIED to this session's reviewer, subagents included; a round
  needing it delegates the run to the worker and reports the exact output.
- The shell guard refuses shell loops, `$(...)` substitution and `$?` inside a compound
  command, so such checks are written in Python; a pipe into `tail` masks the real exit code.
- The editable install resolves `apps` and `packages` to the PRIMARY checkout, so a test run
  inside a worktree puts the worktree first on `sys.path` and proves where the modules loaded
  from before its result is read.
- A fresh worktree has neither `apps/ui/node_modules` nor a built `apps/ui/dist`.
- Never call `run_job` or any runner from inside a checkout: a job run creates a
  `remedy/job-*` branch there.

This feature is NOT UI work — no design-reference binding applies.

## Steps
The item-status table for each round lives in that round's handback, `.agent/handoff.md`,
which AGENTS.md's "Completion Report — Item-Status Table" section requires of every completion
report. This file deliberately does not restate it.

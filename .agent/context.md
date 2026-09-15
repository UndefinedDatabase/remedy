# Context — F261 CLI vocabulary v2 (rename & prune)

## Active Branch
feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Scope
F261 (Tier 2; depends on F259, F260, F272, F274 and F275; blocks F266, F268, F269, F270,
F271 and F263): the catalog equals DECISION amend0905-vocab D4. Task slicing per
`docs/roadmap/features/T2_F261.md`: T001 dissolves the plan triplet and the `job-*` family,
T002 makes `apply` replace `promote` and builds `job show --full`, T003 prunes to D4, and T004
lands descriptions, role labels, help wrapping and the catalog tests. DECISION F261 D1
re-scopes T001 against the catalog measured at `7cdde89b`.

## Do not touch
The concept model (F259 owns the words), the job model (F260 owns what a job is), STATUS
semantics, and the behaviour behind a surviving name: this feature renames and prunes.
Accepted `[x]` evidence under `docs/roadmap/` stays byte-identical.

## Assumptions
- Cleanliness before compatibility (DECISION D-A): no alias and no migration shim. A renamed
  command's old id is deleted in the same commit (DECISION D-B), and every test or script that
  depends on it is converted in that commit.
- One rename per commit, and `TestRenamedCommands` in `tests/test_command_catalog.py` gains
  that rename's pair in the same commit.

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

This feature is NOT UI work — no design-reference binding applies.

## Steps
The item-status table for each round lives in that round's handback, `.agent/handoff.md`,
which AGENTS.md's "Completion Report — Item-Status Table" section requires of every completion
report. This file deliberately does not restate it.

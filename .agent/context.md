# Context — F272 One world completion

## Active Branch
feature/f272-one-world-completion, cut from `main` at
`b18fad576252f7f2739a5807b6408031da8fcde6`, the merge commit of pull request 242.

## Scope
F272 (Tier 2; depends on F259's binding vocabulary page and on the record F260
closed at; blocks F261, F266, F268, F269, F270, F271 and F263): the scope
DECISION F260 D8 split off F260 at the seven-session soft limit. Task slicing
per `docs/roadmap/features/T2_F272.md`: T001 the plural run list and the run
re-key, T002 the rest of the unified record, T003 the eleven consumers, T004 the
classic runner and the resolver collapse, T005 the reachability test and the
prototype cluster deletion.

## Do not touch
Everything `T2_F260.md`'s "Do not touch" section names, unchanged: the
scope-fence builtin deny list (F017), the approval gate, STATUS semantics. No
command is RENAMED here — F261 owns renames. No module outside F260's Design
lists is deleted, and a module that turns out to be reachable is reported with
its import chain, never deleted.

## Assumptions
- Cleanliness before compatibility (DECISION D-A): no migration shim, no
  compatibility reader, no alias. Old `.data` content is deleted by the
  developer, not converted.
- F260's rulings D-A, D0, D1, D2, D4, D5, D6 and D7 stay binding here and are
  NOT restated; `docs/roadmap/features/T2_F260.md` keeps its Goal, Design,
  T-slice and Acceptance sections unedited for exactly that purpose.
- NEVER SPLIT INSIDE T005. A session reaching its own limit splits between T003
  and T004, or before T005, and never within it.

## Constraints
The bullets in this first group are STANDING project constraints, carried
forward from the context this file replaces.

- A round touching `docs/roadmap/**` also gates
  `tests/orchestration/test_roadmap_index.py` beside `tests/docs/`.
- A round rewriting `.agent/` state gates the four state readers:
  `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
  `tests/regression/test_resource_safety.py` and
  `tests/orchestration/test_integrity_gate.py`.
- THE FOUR STATE READERS ARE RUN AS FOUR, NOT AS THREE.
- Every handback runs the canary `pytest tests/cli/test_golden_path.py`.
- Destructive verification runs only inside a disposable git worktree, never in
  the primary checkout, which satisfies `git status --porcelain` empty at every
  verdict.
- Bare `ruff` is DENIED to this session's shell; `python3 -m ruff check <path>`
  runs and exited 0 over `packages/orchestration/pingpong_job.py` when the
  reviewer measured it at `b18fad57`. That spelling is the one every gate of
  this feature orders.
- `remedy` (the built CLI) is DENIED to this session's reviewer session-wide,
  subagents included; a round needing it delegates the run to the worker and
  reports the exact output.
- This session's shell guard refuses some command FORMS outright — shell loops,
  `$(...)` substitution, and `$?` inside a compound command — so checks of that
  shape are re-expressed in Python and the re-expression is reported.

This feature is NOT UI work — no design-reference binding applies.

## Steps
The item-status table for each round lives in that round's handback,
`.agent/handoff.md`, which AGENTS.md's "Completion Report — Item-Status Table"
section requires of every completion report. This file deliberately does not
restate it.

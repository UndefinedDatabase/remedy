# Context — F274 One world completion, part two

## Active Branch
feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, the merge commit of pull request 244.

## Scope
F274 (Tier 2; depends on F259's binding vocabulary page, on the record F260 closed at, and on
the run re-key and unified record F272 closed at; blocks F261, F266, F268, F269, F270, F271
and F263): the remainder DECISION F272 D16 split off F272 at its operator-set soft limit. Task
slicing per `docs/roadmap/features/T2_F274.md`: T001 measure the flip and rule the cap, T002
the classic runner and the resolver collapse, T003 the reachability test and the prototype
cluster deletion.

## Do not touch
Everything `T2_F272.md`'s "Do not touch" section names, unchanged: the scope-fence builtin
deny list (F017), the approval gate, STATUS semantics. No command is RENAMED here — F261 owns
renames. No module outside F260's Design lists is deleted, and a module that turns out to be
reachable is reported with its import chain, never deleted.

## Assumptions
- Cleanliness before compatibility: no migration shim, no compatibility reader, no alias. A
  helper accepting both records is what AGENTS.md Scope Control forbids by name.
- F272's rulings stay binding here and are NOT restated; `docs/roadmap/features/T2_F272.md`
  keeps its DECISION sections unedited for exactly that purpose. D13, D14 parts 1 and 3, and
  D15 are this feature's starting conditions.
- NEVER SPLIT INSIDE T003. A session reaching its own limit splits between T002 and T003, and
  never within T003.

## Constraints
The bullets in this first group are STANDING project constraints, carried forward from the
context this file replaces.

- A round touching `docs/roadmap/**` also gates
  `tests/orchestration/test_roadmap_index.py` beside `tests/docs/`.
- A round rewriting `.agent/` state gates the four state readers:
  `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
  `tests/regression/test_resource_safety.py` and
  `tests/orchestration/test_integrity_gate.py`.
- THE FOUR STATE READERS ARE RUN AS FOUR, NOT AS THREE.
- Every handback runs the canary `pytest tests/cli/test_golden_path.py`.
- Destructive verification runs only inside a disposable git worktree, never in the primary
  checkout, which satisfies `git status --porcelain` empty at every verdict.
- Bare `ruff` is DENIED to this session's shell; `python3 -m ruff check <path>` is the spelling
  every gate of this feature orders.
- `remedy` (the built CLI) is DENIED to this session's reviewer session-wide, subagents
  included; a round needing it delegates the run to the worker and reports the exact output.
- This session's shell guard refuses some command FORMS outright — shell loops, `$(...)`
  substitution, and `$?` inside a compound command — so checks of that shape are re-expressed
  in Python and the re-expression is reported.
- A fresh worktree has neither `apps/ui/node_modules` nor a built `apps/ui/dist`, so a full
  suite run there carries a known environment failure class that a control run must establish
  before any mutated run is read as evidence.

This feature is NOT UI work — no design-reference binding applies.

## Steps
The item-status table for each round lives in that round's handback, `.agent/handoff.md`,
which AGENTS.md's "Completion Report — Item-Status Table" section requires of every completion
report. This file deliberately does not restate it.

# Context — F260 One world: mission → job → run

## Active Branch
feature/f260-one-world, cut from `main` at b5cd6c20, the merge commit of pull
request 240.

## Scope
F260 (Tier 2, depends on F259's binding vocabulary page; blocks F261, F266,
F268, F269, F270, F271 and F263): make DECISION amend0905-vocab D2 real on disk
— one Mission record, one Job record, one Run evidence case, one id shape minted
by one function. Task slicing per T2_F260.md: T001 inventory and id shape, T002
the records and their writers, T003 the consumer list, T004 the classic runner's
deletion, T005 the reachability test and the prototype cluster deletion.

## Do not touch
The scope-fence builtin deny list (F017), the approval gate, STATUS semantics.
No command is RENAMED here — F261 owns renames; this feature changes what a job
IS, not what it is called. No module outside the T2_F260.md lists is deleted,
and a module that turns out to be reachable is reported, never deleted.

## Assumptions
- Cleanliness before compatibility (DECISION D-A): no migration shim, no
  compatibility reader, no alias. Old `.data` content is deleted by the
  developer, not converted.
- The inventory on disk as `.agent/f260_inventory.md` is the evidence D1 and D2
  are ruled from; no later round reconstructs those readings from memory.
- `<data_root>/runs/` is ALREADY the run-log area keyed by job id, so the
  feature file's "renamed to runs/" needs a ruling before any directory moves.
- Deletion is proved before it is performed: the T005 reachability test is green
  with the doomed modules absent from the reachable set BEFORE the first
  `git rm`.

## Constraints
The bullets in this first group are STANDING project constraints, carried
forward from the context this file replaced.

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
- `ruff check` is DENIED to this session's reviewer. A round of F260 that ships
  a `.py` file gates `python3 -m py_compile <path>` instead, and the worker
  attempts `ruff check` itself, reporting success or the exact refusal.
- `remedy` (the built CLI) is DENIED to this session's reviewer session-wide,
  subagents included; a round needing it delegates the run to the worker and
  reports the exact output.
- This session's shell guard refuses some command FORMS outright — shell loops,
  `$(...)` substitution, a `$` inside a `sed` range — so checks of that shape
  are re-expressed in Python and the re-expression is reported.

This feature is NOT UI work — no design-reference binding applies.

## Steps
The item-status table for each round lives in that round's handback,
`.agent/handoff.md`, which AGENTS.md's "Completion Report — Item-Status Table"
section requires of every completion report. This file deliberately does not
restate it.

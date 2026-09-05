# Context — F259 Vocabulary & concept model v1

## Active Branch
feature/f259-vocabulary, cut from `main` at 25961794, the merge commit of pull
request 239.

## Scope
F259 (Tier 2, depends on nothing; F260 and F261 both cite its page as binding,
F263 takes its command name from it, and F268–F271 take their words from it):
write `docs/system/vocabulary.md` as the binding vocabulary page and pin it
with a docs test that reads the shipped command catalog. Task slicing per
T2_F259.md: T001 the page written from the code as it is TODAY, T002 the two
rulings F259 settles itself onto the page, T003 the docs test in planned mode
with both red proofs, T004 the README diagram and the docs index registration.

## Do not touch
No command is renamed, no module is moved, no data shape changes, no catalog
description is edited (T2_F259.md, "Do not touch"). A rename inside this
feature is out of scope by construction: F261 owns renames and F260 owns the
data model.

## Assumptions
- The "code spelling today" column of the D1 table is READ from the seven
  modules T2_F259.md's T001 names, never reconstructed; round 1 puts that
  reading on disk as `.agent/f259_inventory.md` so later rounds copy from a
  measurement.
- The docs test reads the `GROUPS` dict and `CATALOG` list of
  `apps/cli/command_catalog.py` directly, never a captured transcript of
  `remedy --help`.
- The planned/enforced switch is a named module constant that F261 flips, never
  a skip marker (T2_F259.md, Goal & Done).
- The page's Mermaid block and the README's are byte-equal, and the test is
  what stops them drifting.

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
- `ruff check` is DENIED to this session's reviewer. A round of F259 that ships
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

# Context — F275 One world completion, part three

## Active Branch
feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Scope
F275 (Tier 2; depends on F259's binding vocabulary page, on the record F260 closed at, on the
run re-key and unified record F272 closed at, and on the deletion map, the import-reachability
ratchet and the consumer-edge cuts F274 closed at; blocks F261, F266, F268, F269, F270, F271
and F263): the remainder DECISION F274 D8 split off F274 at the standing soft limit. Task
slicing per `docs/roadmap/features/T2_F275.md`: T001 the reachability-gated cluster deletion
with its two carry-overs and DECISION F260 D3, T002 measure the flip and rule the cap, T003
the classic runner.

## Do not touch
Everything `T2_F272.md`'s and `T2_F274.md`'s "Do not touch" sections name, unchanged: the
scope-fence builtin deny list (F017), the approval gate, STATUS semantics. No command is
RENAMED here — F261 owns renames. No module outside F260's Design lists is deleted, and a
module the reachability probe REACHES is reported with its import chain and deferred in
DECISION F260 D3, never deleted.

## Assumptions
- Cleanliness before compatibility: no migration shim, no compatibility reader, no alias. A
  helper accepting both records is what AGENTS.md Scope Control forbids by name.
- F272's and F274's rulings stay binding here and are NOT restated; both feature files keep
  their DECISION sections unedited for exactly that purpose. F272 D13, D14 parts 1 and 3, and
  D15 are starting conditions, as are F274 D1 through D7.
- NEVER SPLIT INSIDE T001's DELETION. DECISION F274 D1 rules that this prohibition binds the
  `git rm` sequence and NOT its prerequisites: the carry-overs and DECISION F260 D3 leave the
  tree consistent at every commit boundary and may land across sessions.

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
- `remedy` (the built CLI) is DENIED to this session's reviewer, subagents included; a round
  needing it delegates the run to the worker and reports the exact output.
- This session's shell guard refuses some command FORMS outright — shell loops, `$(...)`
  substitution, and `$?` inside a compound command — so checks of that shape are re-expressed
  in Python and the re-expression is reported. A pipe into `tail` also MASKS the real exit
  code, so a gate reporting one redirects to a file instead of piping.
- A fresh worktree has neither `apps/ui/node_modules` nor a built `apps/ui/dist`, so a full
  suite run there carries a known environment failure class that a control run must establish
  before any mutated run is read as evidence.

This feature is NOT UI work — no design-reference binding applies.

## Steps
The item-status table for each round lives in that round's handback, `.agent/handoff.md`,
which AGENTS.md's "Completion Report — Item-Status Table" section requires of every completion
report. This file deliberately does not restate it.

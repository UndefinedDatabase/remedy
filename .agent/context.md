# Context — F262 List commands v2 (dates, sort, filter)

## Active Branch
feature/f262-list-commands-v2, cut from `main` at the merge commit of
pull request 235.

## Scope
F262 (Tier 2, depends on nothing, blocks nothing): every list command —
`job list`, the `do` run listings, `queue list`, `mission list`,
`memory list`, `event list` and the rest of the catalog's list-shaped
commands — shows a CREATED and an UPDATED date and supports the same
`--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags with the same spelling; default ordering is newest-first
everywhere, without a flag. Task slicing: T001 the shared listing-option
surface, defined once and pinned by a catalog-derived coverage test; T002
CREATED/UPDATED dates surfaced from each store; T003 the sort/filter/limit
behaviour plus the newest-first default.

## Do not touch
The stores' own schemas beyond adding a missing timestamp, and the
`--json` contract's existing keys — this feature ADDS keys, it does not
rename them (docs/roadmap/features/T2_F262.md, Do not touch).

## Assumptions
- The list-command set is derived MECHANICALLY from
  `apps/cli/command_catalog.py` in round 2, never hand-written; today's
  measurement (28 subcommands matching `list` or `*-list`) is a sizing
  signal for this file only, not the rule itself.
- `--sort <field>` validates against the CALLING list's own columns and
  fails non-zero naming the valid set, per the feature file's Design
  section — the valid-field set is therefore per-command, not global.
- Dates render human-readable in the text UI and ISO-8601 with a
  timezone under `--json`; any probe added by this feature reads the
  TEXT-UI value, never the internal one (feature file, Design).
- A list whose store cannot order by recency says so rather than
  presenting arbitrary order as newest-first (feature file, Design).

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
- `ruff check` is DENIED to this session's reviewer, re-measured at the
  F262 claim (`ruff check apps/cli/command_catalog.py` answers "This
  command requires approval"). A round of F262 that ships a `.py` file
  gates `python3 -m py_compile <path>` instead, and the worker attempts
  `ruff check` itself, reporting success or the exact refusal.
- `remedy` (the built CLI) is DENIED to this session's reviewer
  session-wide; a round needing to run it delegates that run to the
  worker and reports the exact output.

This round is NOT UI work — no design-reference binding applies.

## Steps
The item-status table for each round lives in that round's handback,
`.agent/handoff.md`, which AGENTS.md's "Completion Report — Item-Status
Table" section requires of every completion report. This file deliberately
does not restate it.
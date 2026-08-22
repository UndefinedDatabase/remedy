# Context — F021 Live activity feed + now-card

## Active Branch
feature/f021-live-activity-feed, cut from `main` at `4548995d`, the merge commit
of pull request #210, which the reviewer merged at the Open PR Gate before this
branch existed. Self-drive session per docs/agents/self_drive_protocol.md: the
main session plans and reviews and writes nothing in the work tree, and one
delegated worker per round makes every commit. The branch carries no pull
request; F021 opens one at its closure.

## Scope
In: the humanization catalog that maps every Part E event kind to a plain line
with an honest generic fallback for unknown kinds; the activity feed and its
rows, carrying seq and emitting focus to the graph store on click; the NowCard
over the ACTION-class subset with its recency-driven activity dot; the
scroll discipline that never yanks a reader who has scrolled up; and the
steering input rendered DISABLED with the tooltip its not-yet feature warrants.

Out, per the feature file's Do not touch: steering's backend, which is F030; the
event schema; and graph internals beyond the focus API.

## Constraints
- Merges only at the Open PR Gate; never force-push; never work on main.
- One SSE subscription feeds both graph and feed, with fan-out in the client
  store. A second EventSource is rejected rather than negotiated — the feature
  file's Orchestrator brief states it as an architecture line.
- docs/ui/design_reference/ is binding for every visual surface and
  assets_spec.md is the asset authority. No new font, icon, glyph style or asset
  source without an assets_spec.md update and an assumption_log entry.
- Verification is pytest, scoped per round, plus the canary
  tests/cli/test_golden_path.py. A round touching docs/roadmap/** also gates
  tests/docs/ and tests/orchestration/test_roadmap_index.py, the second because
  tests/docs/ asserts nothing about a roadmap row's own content (R-0493). A
  round rewriting .agent/ state also gates tests/ui_server/,
  tests/orchestration/test_test_runner.py,
  tests/regression/test_resource_safety.py and
  tests/orchestration/test_integrity_gate.py. Frontend rounds additionally gate
  the apps/ui suite the R2 inventory identifies.
- COUNT BY PASSED-PLUS-SKIPPED. Data-dependent skips in tests/ui_server/ make
  the split vary run to run at an unchanged tree.
- Destructive and red-proof checks run only inside a disposable git worktree
  under .remedy-wt/, so resource safety stays intact and the primary checkout
  satisfies an empty `git status --porcelain` at every verdict. Two pytest
  processes never run at once.
- Repository-wide `ruff check .` is RED at base and is NOT a gate (R-0364); ruff
  is gated scoped to the files a round touches, measured against the SAME files
  at the base. `npm run lint` in apps/ui is likewise red at base and is R-0622.

## Steps
Stated once, in `.agent/plan.md`. This file tracks scope and constraints only.

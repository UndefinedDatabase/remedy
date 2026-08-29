# Context — F033 Hunk-level diff approval

## Active Branch
feature/f033-hunk-approval-v2, cut from `main` at `bd8d9529`, the merge commit
of pull request 221. The parked branch `feature/f033-hunk-approval` at
`ed040812` is a previous attempt, retained as history under DECISION F033 D1 and
never checked out, merged or deleted by this feature.

## Scope
Feature F033, `docs/roadmap/features/T5_F033.md` — stable content-hash hunk ids,
the `approve_hunks` command with an all-or-nothing subset apply, and the
rejection-to-repair loop with truthful partial-state rendering.

## Do not touch
Applicator internals, fence rules and review verdict semantics, per the feature
file's own Do-not-touch. `packages/orchestration/diff_parser.py` stays PURE and
TOTAL as its docstring rules: text in, plain data out, no file system, no
subprocess, no network, and it NEVER raises on malformed input.
`docs/roadmap/ROADMAP.md` is not edited.

## Assumptions
- The hunk id is a hash of the path plus the old-side context normalised for
  whitespace, so an edit elsewhere in a file leaves other hunks' ids unchanged.
- `DIFF_VIEW_VERSION` is the declared seam for that change: the feature file and
  `packages/orchestration/diff_parser.py` both say so, and version 1 has never
  been served to an endpoint.
- One hunk identity spans repair and approval; the v1-local helper in
  `packages/orchestration/diff_repair.py` retires onto it.

## Constraints
The bullets in this first group are STANDING project constraints, carried
forward from the context this file replaced. They are not this feature's, and
deleting them with the rest of a rewrite is what cost an earlier round a red
CI run.

- A round touching `docs/roadmap/**` also gates
  `tests/orchestration/test_roadmap_index.py` beside `tests/docs/`.
- A round rewriting `.agent/` state gates the four state readers:
  `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
  `tests/regression/test_resource_safety.py` and
  `tests/orchestration/test_integrity_gate.py`.
- Every handback runs the canary `pytest tests/cli/test_golden_path.py`.
- Destructive verification runs only inside a disposable git worktree, never in
  the primary checkout, which satisfies `git status --porcelain` empty at every
  verdict.
- THE FOUR STATE READERS ARE RUN AS FOUR, NOT AS THREE. The full contract those
  readers hold over the three state files, so a rewrite is checked against it
  directly rather than rediscovered from a red: this file carries
  `## Active Branch`, a `feature/` branch name, a roadmap feature id matching
  `\bF\d{3}\b` and the word `Steps`; `.agent/plan.md` carries `## Goal`,
  `## Next Steps` and a feature id; `.agent/live_review.md` carries `Steps`.

- A new module under `packages/orchestration/` is swept by repo-wide guards that
  name no path: the `REMEDY_DATA_DIR` single-reader invariant, the path-utils
  single-implementation invariant, the bare-`except: pass` ban, and the
  development-artifact boundary.

## Steps
The item-status table for this feature lives in the `## Current Step` section
of `.agent/plan.md`. This file deliberately does not restate it — a second copy
of the map is what fell out of step and cost F022 a finding.

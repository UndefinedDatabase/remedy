# Context — F037 Rendered diff viewer

## Active Branch
feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495`, the merge
commit of pull request #217 which closed F032.

## Scope
Feature F037 per `docs/roadmap/features/T5_F037.md`: a versioned structured
diff JSON served as a read endpoint per task and attempt, and a client viewer
that renders files, hunks, lines and intraline spans with a file sidebar, hunk
collapse, virtual scrolling beyond 2k lines and lazily loaded language bundles.

## Do not touch
The feature file's own list: hunk-id stability, which is F033's contract; apply
mechanics; evidence formats. No approval logic is added early — the viewer
precedes hunk approval in STATUS deliberately. R1 additionally writes no file
under `packages/`, `apps/` or `tests/` at all.

## Assumptions
- Rule A5 chose F037: `docs/roadmap/STATUS.md` carried no `[~]` and no `[!]`
  line and F037 was the first `[ ]`, measured at `9dde5495`.
- `.agent/candidates.md` is EMPTY at the claim, so no block condition stands.
- The feature file's Design is a SUGGESTED shape, not a settled spec; the
  inventory measures the real one before T001 is planned.
- This is a UI feature, so `docs/ui/design_reference/` is binding from T002 on
  and any visual deviation is documented with a technical reason.

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
- Destructive verification runs only inside a disposable git worktree under
  `.remedy-wt/`, never in the primary checkout, which satisfies
  `git status --porcelain` empty at every verdict.
- THE FOUR STATE READERS ARE RUN AS FOUR, NOT AS THREE. The full contract those
  readers hold over the three state files, so a rewrite is checked against it
  directly rather than rediscovered from a red: this file carries
  `## Active Branch`, a `feature/` branch name, a roadmap feature id matching
  `\bF\d{3}\b` and the word `Steps`; `.agent/plan.md` carries `## Goal`,
  `## Next Steps` and a feature id; `.agent/live_review.md` carries `Steps`.

## Steps
The round map for this feature lives in the `## Steps` section of
`.agent/live_review.md`, and the current round's items in the `## Current Step`
table of `.agent/plan.md`. This file deliberately restates neither — a second
copy of the map is what fell out of step and cost F022 a finding.

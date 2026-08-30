# Context — F040 Completion/return digest

## Active Branch
feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge commit
of pull request 222, which is the commit that accepted F033 into the ledger.

## Scope
Feature F040, `docs/roadmap/features/T5_F040.md` — a digest endpoint that
composes state, cost with its basis, ownership sentences, open decisions and ONE
primary action, the hero card that renders it, and CLI parity through
`remedy job digest`.

## Do not touch
Report content, notification channels and the home grid, per the feature file's
own Do-not-touch. `docs/roadmap/ROADMAP.md` is not edited. The digest is a
COMPOSITION: it reads finished sources and owns no new storage.

## Assumptions
- The next-action rule table is ONE source. The digest's primary action imports
  `NEXT_ACTION_RULES` from `packages/orchestration/run_report.py` rather than
  restating it, so the CTA and the report's recommendation cannot disagree.
- The ownership source named in the feature file's Design is unbuilt — F035 is
  `[ ]` in the ledger. What the digest does about it is decided from the round-1
  inventory's measurement, not assumed here.

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

- This feature is UI work, so `docs/ui/design_reference/` is binding and any
  visual deviation is documented in the assumption log with a technical reason.

## Steps
The item-status table for this feature lives in the `## Current Step` section
of `.agent/plan.md`. This file deliberately does not restate it — a second copy
of the map is what fell out of step and cost F022 a finding.

# Context — F032 Approval with the evidence triple

## Active Branch
feature/f032-evidence-triple, cut from `main` at `a399a330`, the merge commit
of pull request #216 which closed the amend0827 process-diet order.

## Scope
Feature F032 per `docs/roadmap/features/T5_F032.md`: the evidence triple —
`evidence_refs[]`, `expected_outcome`, `downside` — becomes a required part of
every decision a human is asked to answer, enforced at the point the inventory
measures such a point to be, rendered by the inbox card, and pinned by a canary
producer that must fail CI when a field is missing.

## Do not touch
The feature file's own list: the decision ANSWERING flow, queue STORAGE and the
provenance RESOLVER. R1 additionally writes no file under `packages/`, `apps/`
or `tests/` at all.

## Assumptions
- Rule A5 chose F032: `docs/roadmap/STATUS.md` carried no `[~]` and no `[!]`
  line and F032 was the first `[ ]`, measured at `a399a330`.
- `.agent/candidates.md` is EMPTY at the claim, so no block condition stands.
- The feature file's Design is a SUGGESTED shape, not a settled spec; the
  inventory measures the real one before T001 is planned.

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

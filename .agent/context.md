# Context — F258 Self-use track v2

## Active Branch
feature/f258-self-use-v2, cut from `main` at `18ae7129`, the merge commit of
pull request 225, which is the commit that accepted F040 into the ledger.

## Scope
Feature F258, `docs/roadmap/features/T5_F258.md` — a self-replenishing queue
generator that fires at the closure consumption point whenever the queue is
empty (T001), executing the consumed item through the real job path under a
small dedicated budget to the normal approval gate rather than only planning
it (T002), and routing any defect a run surfaces into the standard finding
ledger (T003).

## Do not touch
The scope-fence builtin deny list (F017), the normal approval gate, and STATUS
semantics — a job must never check itself off — per the feature file's own
Do-not-touch. The v1 queue schema's existing fields (`id`, `title`, `why`,
`job_markdown`, `consumed_by`) are extended, never replaced, so
`packages/orchestration/self_use_queue.py`'s existing readers keep working
against a v2 queue file.

## Assumptions
- `next_self_use_item`/`plan_next_self_use_item` currently have NO production
  caller anywhere in `packages/` or `apps/`: precondition 6
  (`docs/roadmap/STATUS_closure_protocol.md`) today is a manual step a session
  performs by hand at every closure. What T001's generator hooks INTO is
  decided from the round-1 inventory's measurement, not assumed here.
- Consumption stays closure-only (DECISION F257 D2): T001 may append a new
  pending item to the queue but must never be the thing that sets
  `consumed_by`, and T002's execution must never auto-promote past the
  existing `--approve` barrier.

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

This feature is NOT UI work — no design-reference binding applies. The
Do-not-touch above carries the two constraints specific to F258 itself: no
self-consumption-marking, no auto-promotion past `--approve`.

## Steps
The item-status table for this feature lives in the `## Current Step` section
of `.agent/plan.md`. This file deliberately does not restate it — a second copy
of the map is what fell out of step and cost F022 a finding.

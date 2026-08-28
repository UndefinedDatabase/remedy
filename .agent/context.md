# Context — F257 Self-use track

## Active Branch
feature/f257-self-use-track, cut from `main` at the merge commit of pull
request #220.

## Scope
Feature F257, `docs/roadmap/features/T5_F257.md` — the standing self-use track
operator order amend0828-daily-driver registered. The pieces: a curated queue
file, exactly one item consumed per feature close, the run taken to the normal
approval gate, and findings recorded as operator findings in the feature file
that owns the surface.

## Do not touch
STATUS semantics — a job must never check itself off. The approval gate: the
`--approve` barrier in `packages/orchestration/job_promote.py` is unchanged. The
scope-fence builtin deny list in `packages/orchestration/scope_fences.py`.
`docs/roadmap/ROADMAP.md` is not edited.

## Assumptions
- The queue will store job-file TEXT in the format
  `packages/orchestration/pingpong_job.py:parse_job_file` accepts, so it cannot
  drift into a second task format.
- Shipped curated data lives in `scripts/` with one named loader under
  `packages/orchestration/`, the convention `scripts/dead_models.json` and
  `packages/orchestration/dead_model_list.py` already set.

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

- A new module under `packages/orchestration/` is swept by repo-wide guards that
  name no path: the `REMEDY_DATA_DIR` single-reader invariant, the path-utils
  single-implementation invariant, the bare-`except: pass` ban, and the
  development-artifact boundary.

## Steps
The item-status table for this feature lives in the `## Current Step` section
of `.agent/plan.md`. This file deliberately does not restate it — a second copy
of the map is what fell out of step and cost F022 a finding.

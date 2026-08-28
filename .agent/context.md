# Context — F256 Diff viewer completion

## Active Branch
feature/f256-diff-viewer-completion, cut from `main` at `0e8ab5b4`, the merge
commit of pull request #219.

## Scope
Feature F256, `docs/roadmap/features/T5_F256.md` — the scope DECISION F037 D11
split off F037 and operator order amend0828-daily-driver registered.
The pieces: wire the highlighting, measure the 10k-line fixture end to end and
record it, rule on the file sidebar's visual treatment.

## Do not touch
The diff JSON schema, the read endpoint, hunk-id stability (that is F033's
contract) and apply mechanics. Nothing F037 built is removed — DECISION F037
D11 says so in as many words. `docs/roadmap/ROADMAP.md` is not edited. The
server-side diff source under `packages/` is outside this feature.

## Assumptions
- No third-party syntax highlighter is reachable from this build environment,
  so DECISION F256 D1 rules that Remedy writes its own lazy bundles.
- No file under `docs/ui/design_reference/` contains the word "syntax", so no
  authority rules a token palette. The round that ships the stylesheet rules
  it, deriving it from custom properties already defined under `apps/ui/src`;
  `tests/ui_contracts/test_design_drift.py` fails any that is not.

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

- A `.ts` mutation red-proof follows DECISION F037 D10: vitest is spawned from
  the primary checkout so it resolves its own package there, `--root` points
  discovery at the worktree, and both flags are load-bearing.

## Steps
The item-status table for this feature lives in the `## Current Step` section
of `.agent/plan.md`. This file deliberately does not restate it — a second copy
of the map is what fell out of step and cost F022 a finding.

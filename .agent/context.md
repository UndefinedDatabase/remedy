# Context — amend0828-daily-driver

## Active Branch
feature/amend0828-daily-driver, cut from `main` at the merge commit of pull
request #218, which closed F037.

## Scope
Operator collective order amend0828-daily-driver: five numbered points, all
authorized in the order itself, none of them a question back to the operator.

1. Deliberate partial promotion on `remedy do job-promote` — a new
   `--skip-blocked` promotes every non-blocked file and provably leaves the
   blocked ones alone; blocked output always ends with an honest `Next:` line.
2. Cost truth on the job path — `remedy stats cost` must show at least one
   ledger row in the right project scope after a real `do job-run` with
   measured provider usage. Settles the open design choice in T2_F103.
3. Repair the R-0714 tautology test so the integration gate's one
   neutralisation lever is genuinely discriminated, and book R-0714 resolved.
4. Register the split-off F037 rest scope (DECISION F037 D11 / Amendment A6)
   as ONE new Package 1 feature line placed directly before F033.
5. Register the self-use track as a second new Package 1 line, directly after
   the F037-rest line. Registration and feature file only — not built.

## Do not touch
The blocked-path guardrail itself. `_is_blocked_path`, `_BLOCKED_EXACT` and
`_BLOCKED_PREFIXES` keep every entry they have, blocked files are never
written, and without `--skip-blocked` the promotion behaves exactly as it does
today. DECISION D16's per-finalized-task-run ledger granularity is not
reopened. `docs/roadmap/ROADMAP.md` is not edited. The `.agent/STOP` sentinel
is left exactly where it is: it halted the F033 self-drive loop, this order is
not a self-drive round, and the operator's own words are that the loop stands.

## Assumptions
- The Open PR Gate passed with ZERO open pull requests, which AGENTS.md tells
  the agent to continue normally from.
- Point 2's shape is the operator's ruling for least wiring depth: reuse the
  already-armed exporter rather than reopen D16 or add a second backfill source,
  because a second backfill source leaves `stats cost` empty until someone asks,
  which is not what the order requires to be visible after a run.

## Constraints
The bullets in this first group are STANDING project constraints, carried
forward from the context this file replaced. They are not this order's, and
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
The item-status table for this order lives in the `## Current Step` section of
`.agent/plan.md`. This file deliberately does not restate it — a second copy of
the map is what fell out of step and cost F022 a finding.

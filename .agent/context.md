# Context — F106 Session resume instead of rebuild

## Active Branch
feature/f106-session-resume, cut from `main` at `811c2d7e`.

## Scope
Feature F106, `docs/roadmap/features/T3_F106.md` — Tier 3, session resume
for repair rounds. T001 (this feature's first code round) adds an additive
`supports_resume` capability flag and `resume` parameter to the provider
call entry, plus `resume_used`/`resume_session_ref` evidence fields, with
zero behavior change on every adapter. T002 wires it into the repair path
with a fallback-once rule; T003 measures resume vs full-context tokens.
F106 also covers job/mission resume-from-persisted-state per the feature
file's own Scope note (F075 candidate routing, R-0201) — in scope, not
sliced into T001-T003 yet.

## Do not touch
Failover policy, provider adapter internals beyond the additive surface,
prompt content rules — the feature file's own Do-not-touch. No orchestrator
move schema `resume` kind exists; that is out of T001-T003's own slicing.

## Assumptions
- `ClaudeCliProvider` is the only adapter that populates `session_id` today
  (`UsageActuals.session_id`, `packages/orchestration/token_actuals.py:37`).
  T001 does not turn any adapter's `supports_resume` True — that is T002's
  call once real resume behavior is wired.
- Diff-only repair (F111) is accepted and merged; T002's gate on it is
  satisfied.

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
- Destructive verification runs only inside a disposable git worktree, never
  in the primary checkout, which satisfies `git status --porcelain` empty at
  every verdict.
- THE FOUR STATE READERS ARE RUN AS FOUR, NOT AS THREE. The full contract
  those readers hold over the three state files, so a rewrite is checked
  against it directly: this file carries `## Active Branch`, a `feature/`
  branch name, a roadmap feature id matching `\bF\d{3}\b` and the word
  `Steps`; `.agent/plan.md` carries `## Goal`, `## Next Steps` and a feature
  id; `.agent/live_review.md` carries `Steps`.
- A new module under `packages/orchestration/` is swept by repo-wide guards
  that name no path: the `REMEDY_DATA_DIR` single-reader invariant, the
  path-utils single-implementation invariant, the bare-`except: pass` ban,
  and the development-artifact boundary.

This feature is NOT UI work — no design-reference binding applies.

## Steps
The item-status table for this feature lives in the `## Current Step`
section of `.agent/plan.md`. This file deliberately does not restate it.

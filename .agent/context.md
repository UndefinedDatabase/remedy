# Context — F083 CI self-check

## Active Branch
feature/f083-ci-self-check, cut from main at f3fd96d7 after PR #201 merged. F083
is claimed `[~]` in docs/roadmap/STATUS.md and stays claimed until closure. No PR
exists for this branch yet; one is created at closure, not before.

## Scope
In: Remedy's own CI as one entrypoint plus thin hosted wrappers. Nothing is built
yet — this round only opens the record. The feature file T2_F083.md sets the
shape: `remedy ci [--stage NAME] [--json]` over the stages fast, standard,
determinism, ui and budgets; stages are MARKER SELECTIONS over the existing test
tree, not a new test organization; hosted workflow files call the same
entrypoint so there is one source of truth for what CI means; live-provider
tests and the F082 benchmark are excluded by marker and said so in the output
with their manual commands. Plus `.agent/**` round state and the one claimed
STATUS line.

Out: test contents, marker semantics, the bench's cost profile and release
packaging — the feature file's Do-not-touch list. CI never auto-retries a suite;
a flaky test is quarantined only by an explicit marker change in a reviewed diff.
A change that needs a test's CONTENT edited is a finding, not a fix.

## Constraints
- The main session writes nothing in the work tree; a delegated worker subagent
  makes every commit (docs/agents/self_drive_protocol.md).
- Merges only at the Open PR Gate; never force-push; never work on main.
- Verification is pytest, scoped per round, plus the canary
  tests/cli/test_golden_path.py. A round touching docs/roadmap/** also gates
  tests/docs/, and a round rewriting `.agent/` state also gates
  tests/regression/test_resource_safety.py and
  tests/orchestration/test_integrity_gate.py, which read that state live.
  Destructive and red-proof checks run only inside a disposable git worktree
  under .remedy-wt/, so resource safety stays intact.
- Repository-wide `ruff check` is RED on main with pre-existing errors and is
  NOT a round gate (R-0364); ruff is gated scoped to the files F083 owns.
- The reviewer measures its block mechanically on the final bytes before
  emission and keeps it under 400 lines (DECISION F105 D5), with 240 the
  preferred target so the block-save commit stays inside the 500-insertion
  limit (R-0381).
- R-0205 rides with this feature by the feature file's Carried findings section:
  contract tests that assert against LIVE `.agent/` state flip red for reasons
  unrelated to the round that trips them. Detecting a red main is this feature's
  own job, so the fixture-versus-live design question is answered inside it and
  not routed away.

## Steps
The round map is stated ONCE, in the Steps section of `.agent/live_review.md`,
and is deliberately not restated here: a map quoted in two places is the
contradiction R-0447 records. This file tracks scope and constraints only.

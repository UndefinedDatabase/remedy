# Context — amend0816 CI hosted green

## Active Branch
feature/amend0816-ci-hosted-green, cut from origin/main at 4e1fd006 after the
F083 closure PR #202 merged. This is an operator AMENDMENT to a closed feature,
not a new roadmap feature: it delivers the hosted half of F083's Acceptance,
which no session ever checked. Run in an ordinary interactive session, not the
self-drive loop, so the main session commits directly.

## Scope
In: making the hosted CI run GREEN with the same stage results as the local one.
That means test CONTENT this time — the ten `fast` failures are tests that mock
the provider path only halfway, so repairing them is the work, and F083's
Do-not-touch list does not bind an amendment written to fix exactly that. The
durable piece is the autouse fixture `tests/conftest.py::_no_live_ollama_reach`
(DECISION amend0816 D1). Plus a dated operator paragraph in
`docs/roadmap/features/T2_F083.md` and this `.agent/` state.

Out: STATUS.md and the README capability counters, which stay untouched — F083
is already closed and this amendment does not re-open its ledger line. No test is
deleted, no assertion weakened, no ceiling raised. A stage timeout on a slower
runner is NOT fixed by editing a budget in `ci_stages.py`: stop and show the
operator the measured times.

## Constraints
- Ordinary interactive session: the main session commits directly. The
  self-drive delegation rule of docs/agents/self_drive_protocol.md does not
  apply here.
- Merges only at the Open PR Gate; never force-push; never work on main.
- Verification is pytest, scoped per round, plus the canary
  tests/cli/test_golden_path.py. A round touching docs/roadmap/** also gates
  tests/docs/, and a round rewriting `.agent/` state also gates
  tests/regression/test_resource_safety.py and
  tests/orchestration/test_integrity_gate.py, which read that state live.
  Destructive and red-proof checks run only inside a disposable git worktree
  under .remedy-wt/, so resource safety stays intact.
- Repository-wide `ruff check` is RED on main with pre-existing errors and is
  NOT a gate (R-0364); ruff is gated scoped to the files this amendment touches,
  measured against the SAME files at origin/main so a pre-existing error is not
  read as a new one.
- The acceptance evidence is a HOSTED run, not a local one. A local green is
  necessary and not sufficient; `gh run watch` on the PR's workflow run is the
  measurement that F083 skipped.

## Steps
Stated once, in `.agent/plan.md`. This file tracks scope and constraints only.

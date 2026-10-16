# Context — amend1016sb (the tool sandbox)

## Active Branch
feature/pi-tool-sandbox, in the worktree .remedy-wt/pi-tool-sandbox; the supervisor keeps running
main from the main checkout until decodeux merges and restarts it.

## Scope
The Bubblewrap boundary around Pi and the `test`/`dod-process` classes, the provider relay, the
tool and call deadlines, the stop reaching a running call, the doctor self-test, tests and docs.
No frontend, no planner/builder/reviewer redesign, no unrelated refactor.

## Do not touch
`.agent/STOP` (untracked), F078 and the autonomous queue, Remedy's data root, the running
supervisor, the public API contract.

## Constraints
- Resource safety: one pytest run at a time, only through `scripts/remedy_pytest.sh`; after the
  one full run, decodeux's order: rerun only the failed tests.
- Structure ratchet: no listed function or file grows; `exec_guard.py` stays under 1,000 lines.
- Every commit at most 500 insertions. No real model call without decodeux's approval.

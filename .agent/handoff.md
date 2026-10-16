# Handoff — amend1016p (simple orders stay simple), branch feature/simple-orders-fast-lane

Operator order remedy-simple-orders (2026-10-16), one session. Finding R-1336 (High), DECISION
amend1016p D1 to D3. Not a roadmap feature; F078 stays Rule A5's next; `.agent/STOP` kept.

## Verification (python3 3.10.12)
- Targeted: 47 files of lane, do, mission, job plan, granularity, order file, HTTP gate paths, Pi,
  sandbox, docs and ratchet tests: 1447 passed, 1 failed (the import allowlist, then repaired and
  rerun: 3 passed); 27 further files that run `remedy do` or a planner: 796 passed. ruff clean.
- The app's incident order over HTTP (no `no_llm`, the model endpoint a closed port): one job, one
  task, deterministic plan, no prompt trace, project_tests in the contract, stopped before apply.
  The same test fails on main's `do_lane.py`.

| Item | Status | Reason |
|---|---|---|
| R-1336 | done | |
| The lab order sent again | skipped | waits for the merge, which waits for decodeux |

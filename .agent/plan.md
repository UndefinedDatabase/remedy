# Plan — F106 Session resume instead of rebuild

Branch: feature/f106-session-resume, cut from `main` at `811c2d7e`.
SESSION 6, round 21.

## Goal
Repair rounds stop resending the world: where the provider supports resuming
a session, a repair call resumes the original session and sends only the
findings delta, with an honest automatic fallback to full context when the
session is gone, flagged in evidence. Correctness never depends on resume
working.

## Current Step
Round 20 ran SU-003 for real (precondition 6) and found a genuine defect:
`create_provider()` (`packages/orchestration/pingpong_provider.py:1591`)
has no `"ollama"` branch, so `role_config.DEFAULT_PROVIDER` can never reach
a real provider through the ping-pong job path, blocking the run with
`provider_unavailable`. This round registers that defect as R-0761
(Medium) in `.agent/live_review.md`, discharging precondition 6's own
"every string `describe_self_use_run_defects` returns is registered"
requirement. R-0761 is NOT fixed this round — fixing it is out of F106's
own scope (a new provider adapter, or a DEFAULT_PROVIDER change, neither
named in T3_F106.md's Task slicing) — it is registered OPEN, exactly as
precondition 6 requires, and left for a future feature or self-use item.

## Next Steps
1. Precondition 6 is MET once R-0761 is registered (this round).
2. Precondition 1 requires every finding be Resolved or a documented
   Medium/Low risk — R-0761 stays OPEN as a documented Medium risk; the
   closure verdict will read PASS WITH RISKS, not PASS, for this reason.
3. Evidence job, review zip, STATUS line, PR — the closure algorithm's
   remaining steps. The closure commit also owes DECISION F106 D2's
   `.agent/candidates.md` entry (job/mission resume deferral).

## Risks
- R-0761 (Medium, OPEN): the self-use track's product-default provider
  path is unreachable for the ping-pong job path. Documented, not fixed,
  per Task-slicing scope.

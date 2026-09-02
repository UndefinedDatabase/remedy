# Plan — F106 Session resume instead of rebuild (CLOSED)

Branch: feature/f106-session-resume, cut from `main` at `811c2d7e`. F106
is CLOSED: `docs/roadmap/STATUS.md` carries its `[x]` line.

## Goal
Repair rounds stop resending the world: where the provider supports resuming
a session, a repair call resumes the original session and sends only the
findings delta, with an honest automatic fallback to full context when the
session is gone, flagged in evidence. Correctness never depends on resume
working. DONE.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| T001/T002/T003, integration gate | done | rounds 1-17 |
| all six closure preconditions | done | rounds 18-21 |
| the evidence bundle and the review zip | done | round 22, READY_FOR_REVIEW |
| the closure commit | done | this round, Rule A4's last commit |
| the candidates.md entry (DECISION F106 D2) | done | this round, DECISION amend0827 D2 carve-out |
| the pull request | pending | opened immediately following this commit |

## Next Steps
1. Open the pull request.
2. Nothing further on this branch after that. The next feature's Open PR
   Gate merges this pull request, or the operator merges it manually.
3. Rule A5 selects the next feature (F108) in a fresh session.

## Risks
- R-0761 (Medium, OPEN): the ping-pong provider factory has no `"ollama"`
  branch, so the resolved product-default provider can never reach a real
  call through the self-use/job-run path. Documented, not F106's own scope
  to fix. This is the sole reason the closure verdict is PASS WITH RISKS.
- The job/mission-resume half of the feature file's own Scope note is
  deferred, not built — carried forward as a closure candidate per
  DECISION F106 D2, not dropped.

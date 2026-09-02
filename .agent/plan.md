# Plan — F106 Session resume instead of rebuild

Branch: feature/f106-session-resume, cut from `main` at `811c2d7e`.
SESSION 5, round 16.

## Goal
Repair rounds stop resending the world: where the provider supports resuming
a session, a repair call resumes the original session and sends only the
findings delta, with an honest automatic fallback to full context when the
session is gone, flagged in evidence. Correctness never depends on resume
working.

## Current Step

T001, T002 (both sides) and T003 are ALL DONE (rounds 2-15) — F106's own
Task slicing has no open item. Work has moved to the closure sequence
(docs/roadmap/STATUS_closure_protocol.md); this round is precondition 2,
the dedicated integration gate (docs/agents/integration_gate.md).

## Next Steps
1. This round: integration gate (full suite, branch + base, `pytest -n
   auto`), per docs/agents/integration_gate.md steps 1-5.
2. Next: feature file Built State section (precondition 4) + resolve the
   feature file's own job/mission-resume scope note against Task slicing
   (a DECISION, since Acceptance never required it).
3. Then: self-use track consumption (precondition 6), evidence job, review
   zip, STATUS line, PR — the closure algorithm's remaining steps.

## Risks
- R-0736 (Medium, OPEN): the integration gate's own base-worktree parity
  recipe manufactures ~114 false `tests/ui_server/` failures unless the
  proactive mtime fix (advance `apps/ui/dist` mtimes past the worktree's
  checkout time, after a `symlinks=True` copy) is applied before the base
  run. Apply it proactively this round, per F040 R17/F258 R7 precedent.

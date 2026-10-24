# Plan — F162 Sandbox profiles per adapter

## Goal
What a worker process may touch becomes a named, testable profile: a profile file declares its
filesystem scope, network (deny or a host allowlist), resource limits, allowed binaries and a tmp
quota; each adapter declares its default profile; a project may tighten but never loosen below the
policy minimum; an optional container runner reads the same profile; and an honesty document tables
what each profile does and does not prevent, every row linked to a test
(`docs/roadmap/features/T8_F162.md`).

## Current Step
Round 9: repair R-1469 under DECISION F162 D9 — the honesty document says "no limit declared" for
an unlimited dimension and proves it with the record test that pins it. The building slices T001
to T003 are complete with this round.

## Next Steps
1. The closure sequence, in a fresh session (session 2): book round 9 after re-running
   `.remedy-wt/f162-r9/prep/verify.py`, then follow `docs/roadmap/STATUS_closure_protocol.md` —
   the self-use run, the integration gate (the one full suite), the evidence package and review
   zip, the Built State, the ledger rotation, the STATUS acceptance and the pull request.

## Risks
- The container fixtures need a local `python:3.12-slim`; where it is absent they skip, NOT VERIFIED.
- R-1467 (the runner's configuration key) is owned by F246, so F162 closes PASS_WITH_RISKS.

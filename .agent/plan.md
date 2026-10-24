# Plan — F162 Sandbox profiles per adapter

## Goal
What a worker process may touch becomes a named, testable profile: a profile file declares its
filesystem scope, network (deny or a host allowlist), resource limits, allowed binaries and a tmp
quota; each adapter declares its default profile; a project may tighten but never loosen below the
policy minimum; an optional container runner reads the same profile; and an honesty document tables
what each profile does and does not prevent, every row linked to a test
(`docs/roadmap/features/T8_F162.md`).

## Current Step
Round 11, the closure's evidence round (session 2): book round 10 (PASS) with R-1470 resolved, save
the evidence script, then the staging reclaim, the evidence job and the review package.

## Next Steps
1. The closing round: the Built State, the ledger rotation, SU-083's `consumed_by`, the STATUS
   acceptance with the README sync, and the pull request, left unmerged.

## Risks
- The container fixtures need a local `python:3.12-slim`; where it is absent they skip, NOT VERIFIED.
- R-1467 (the runner's configuration key) is owned by F246, so F162 closes PASS_WITH_RISKS.

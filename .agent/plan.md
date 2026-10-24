# Plan — F162 Sandbox profiles per adapter

## Goal
What a worker process may touch becomes a named, testable profile: a profile file declares its
filesystem scope, network (deny or a host allowlist), resource limits, allowed binaries and a tmp
quota; each adapter declares its default profile; a project may tighten but never loosen below the
policy minimum; an optional container runner reads the same profile; and an honesty document tables
what each profile does and does not prevent, every row linked to a test
(`docs/roadmap/features/T8_F162.md`).

## Current Step
Round 10, the closure's integration-gate round (session 2): book round 9 (PASS) with R-1469
resolved; register and repair R-1470, the docs index row whose type cell reads `system, generated`;
the checklist's one consolidation pass; the closure's self-use item run to its approval gate, never
applied; and the feature's one full suite with its CPU cost.

## Next Steps
1. Round 11: the reviewer books round 10, R-1470 and every self-use run defect; then a repair round
   naming every bad node id if the suite is red, else the evidence script, the evidence bundle and
   the review package.
2. The closing round: the Built State, the ledger rotation, the STATUS acceptance with the README
   sync and the self-use queue's `consumed_by`, and the pull request.

## Risks
- The container fixtures need a local `python:3.12-slim`; where it is absent they skip, NOT VERIFIED.
- R-1467 (the runner's configuration key) is owned by F246, so F162 closes PASS_WITH_RISKS.

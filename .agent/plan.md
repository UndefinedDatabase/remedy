# Plan — F162 Sandbox profiles per adapter

## Goal
What a worker process may touch becomes a named, testable profile: a profile file declares its
filesystem scope, network (deny or a host allowlist), resource limits, allowed binaries and a tmp
quota; each adapter declares its default profile; a project may tighten but never loosen below the
policy minimum; an optional container runner reads the same profile; and an honesty document tables
what each profile does and does not prevent, every row linked to a test
(`docs/roadmap/features/T8_F162.md`).

## Current Step
Round 12, the closing round (session 2): book round 11 (PASS), the Built State, the ledger rotation,
the STATUS acceptance with the README sync and SU-083's `consumed_by`, and the pull request, left
unmerged. F162 is accepted with this round.

## Next Steps
1. The next session: Phase 1 rule 1, then the Open PR Gate merges F162's pull request, then the
   first commit of the next feature books round 12's verdict, then Rule A5.

## Risks
- R-1467 (the container runner's configuration key) is owned by F246; F162 closes PASS_WITH_RISKS.

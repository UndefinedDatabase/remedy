# Plan — F157 Capability matrix & honest degradation

## Goal
A declarative register maps every capability-consuming feature to the capabilities it requires
and to one registered degradation; one central `require_or_degrade` call sits at each usage site;
the run's `capability_decisions.jsonl` evidence, a report section and a command-line line show
when a degradation ran; a guard fails a capability read outside the matrix
(`docs/roadmap/features/T8_F157.md`).

## Current Step
Round 11, the closing round: book round 10, the Built State, the ledger rotation, F157 accepted in
STATUS with the README sync and SU-081's `consumed_by`, and the pull request, left unmerged.

## Next Steps
1. The next session merges F157's pull request at the Open PR Gate, books round 11's verdict in the
   next feature's first commit, and claims the next feature by Rule A5.

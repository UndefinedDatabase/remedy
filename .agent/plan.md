# Plan — F157 Capability matrix & honest degradation

## Goal
A declarative register maps every capability-consuming feature to the capabilities it requires
and to one registered degradation; one central `require_or_degrade` call sits at each usage site;
the run's `capability_decisions.jsonl` evidence, a report section and a command-line line show
when a degradation ran; a guard fails a capability read outside the matrix
(`docs/roadmap/features/T8_F157.md`).

## Current Step
Round 6: book round 5's verdict and R-1453's resolution; the reduced-capability end-to-end of
DECISION F157 D3 (6), a one-task job run through the command handler with a reduced adapter,
its evidence, its job report and its run report golden, beside a control with the registry's
adapter.

## Next Steps
1. The closure sequence (`docs/roadmap/STATUS_closure_protocol.md`): the integration gate with the
   one full suite, the evidence package and review zip, the Built State, the checklist
   consolidation, the STATUS acceptance and the pull request.

## Risks
- `pingpong_provider.py`, `pingpong_loop.py` and `format_job_report_text` are structure-ledger
  rows; every edit keeps their length or lowers the row in the same commit.

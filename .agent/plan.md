# Plan — F157 Capability matrix & honest degradation

## Goal
A declarative register maps every capability-consuming feature to the capabilities it requires
and to one registered degradation; one central `require_or_degrade` call sits at each usage site;
the run's `capability_decisions.jsonl` evidence, a report section and a command-line line show
when a degradation ran; a guard fails a capability read outside the matrix
(`docs/roadmap/features/T8_F157.md`).

## Current Step
Round 7: book round 6's verdict, DECISION F157 D6, and repair R-1454 by stating in the contract
page, the route module's docstring and `routed_claude_cli_build`'s comment what a run's
degradations name.

## Next Steps
1. The closure sequence (`docs/roadmap/STATUS_closure_protocol.md`): book round 7 and R-1454's
   resolution, the integration gate with the one full suite, the evidence package and review zip,
   the Built State, the checklist consolidation, the STATUS acceptance and the pull request.

## Risks
- `pingpong_provider.py`, `pingpong_loop.py` and `format_job_report_text` are structure-ledger
  rows; every edit keeps their length or lowers the row in the same commit.

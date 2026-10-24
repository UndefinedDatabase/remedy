# Plan — F157 Capability matrix & honest degradation

## Goal
A declarative register maps every capability-consuming feature to the capabilities it requires
and to one registered degradation; one central `require_or_degrade` call sits at each usage site;
the run's `capability_decisions.jsonl` evidence, a report section and a command-line line show
when a degradation ran; a guard fails a capability read outside the matrix
(`docs/roadmap/features/T8_F157.md`).

## Current Step
Round 4: book round 3's verdict, R-1451's resolution and R-1452, DECISION F157 D4; repair R-1452;
route `reviewer_schema_gate` and `parked_session_resume` inside the claude-cli provider, every
decision of a build recorded by `routed_claude_cli_build`.

## Next Steps
1. The report section, the run's `Degradations:` line and the reduced-capability end-to-end
   (DECISION F157 D3 (5) and (6)).
2. The closure sequence: the integration gate, the evidence package, the STATUS acceptance.

## Risks
- `pingpong_provider.py` and `pingpong_loop.py` are structure-ledger file rows; every edit there
  keeps their length, and `create_role_provider` stays at or under 100 lines.

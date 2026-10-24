# Plan — F157 Capability matrix & honest degradation

## Goal
A declarative register maps every capability-consuming feature to the capabilities it requires
and to one registered degradation; one central `require_or_degrade` call sits at each usage site;
the run's `capability_decisions.jsonl` evidence, a report section and a command-line line show
when a degradation ran; a guard fails a capability read outside the matrix
(`docs/roadmap/features/T8_F157.md`).

## Current Step
Round 3: book round 2's verdict and R-1451, DECISION F157 D3; retire the planner entry and repair
R-1451; the route module `packages/orchestration/capability_routes.py` with its evidence file, and
`stream_evidence_capture` routed inside `create_role_provider`.

## Next Steps
1. Route `reviewer_schema_gate` and `parked_session_resume` inside the claude-cli provider by
   line-for-line swaps, their decisions joining the evidence file (DECISION F157 D3 (2)).
2. The report section, the run's `Degradations:` line and the reduced-capability end-to-end
   (DECISION F157 D3 (5) and (6)).
3. The closure sequence: the integration gate, the evidence package, the STATUS acceptance.

## Risks
- `pingpong_provider.py` and `pingpong_loop.py` are structure-ledger file rows; every edit there
  keeps their length, and `create_role_provider` stays at or under 100 lines.

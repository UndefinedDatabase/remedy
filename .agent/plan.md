# Plan — F157 Capability matrix & honest degradation

## Goal
A declarative register maps every capability-consuming feature to the capabilities it requires
and to one registered degradation; one central `require_or_degrade` call sits at each usage site;
the run's `capability_decisions.jsonl` evidence, a report section and a command-line line show
when a degradation ran; a guard fails a capability read outside the matrix
(`docs/roadmap/features/T8_F157.md`).

## Current Step
Round 5: book round 4's verdict, R-1452's resolution and R-1453, DECISION F157 D5; repair R-1453;
one wording for a degradation, the readers of a run's and a task's evidence, `remedy run show`'s
line and JSON list, and the job report's per-task line behind a structural step.

## Next Steps
1. The reduced-capability end-to-end: a job run through the loop with a reduced adapter whose
   evidence, run report and job report name exactly the degradations the register predicts
   (DECISION F157 D3 (6)).
2. The closure sequence: the integration gate, the evidence package, the STATUS acceptance.

## Risks
- `pingpong_provider.py`, `pingpong_loop.py` and `format_job_report_text` are structure-ledger
  rows; every edit keeps their length or lowers the row in the same commit.

# Plan — operator amendment amend1023-universe-trust

## Goal
Five parts from the operator's order of 2026-10-23: (1) the client property `host_tools`; (2) small
orders stay small; (3) the order's story; (4) the F133 and F151 follow-ups; (5) cancel the probe.

## Current Step
Done: all five parts built (C0–C9), the one full suite run read, repaired, and the affected test
files re-run green; pull request, merge on local evidence, handback.

## Next Steps
1. The operator restarts the supervisor on the merged code with its port, then grants
   `remedy client grant-host-tools orb-universe` and `orb-remedy` (DECISION amend1023 D10).
2. The next feature under Rule A5 is F315, "The loop runs through the adapter", registered thin.

## Risks
- Granting `host_tools` before the supervisor restarts locks every client out (D10).

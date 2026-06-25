# Plan — Steps 4887-4895: Job Target Guard Pre-Apply Closure v6

## Goal
Move job-level target repo guard before workspace apply. Add post-apply
defense-in-depth guard. Ensure target mutation blocks task without copying
staged files into job workspace.

## Current Step
Implementing all steps.

## Steps
- Step 4887: Move job-level target guard before workspace apply
- Step 4888: Add explicit pre-apply guard block manifest/evidence
- Step 4889: Add post-apply target guard sanity check
- Step 4890: Regression test: target mutation before apply blocks without workspace apply
- Step 4891: Regression test: report does not claim apply after target mutation
- Step 4892: Preserve result.target_mutated=True completion gate behavior
- Step 4893: Preserve continuation config, reviewer evidence gate, token policy
- Step 4894: Preserve successful job flow and existing safety
- Step 4895: Final architecture guard and handoff

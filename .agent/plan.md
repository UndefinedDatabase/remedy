# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001 and T002 are DONE, and the classic runner's whole
command surface is gone as of round 34.

## Current Step

ROUND 86 ROUTES THE LAST HANDLER JOB-ID PARSES. The twelve `load_job(UUID(...))` calls left under
`apps/cli/` stop parsing. Ten hand `load_job` what `lookup_job_id` resolves; `project attach-job`
resolves once and files the resolved id in the project; `job stop`'s loader loads the id exactly
as given, so its caller's normalisation still runs. Eleven of the twelve are pinned by a test
that fails when that site's parse is restored. The round registers `R-0883`, `dashboard project`
crashing on a module that never existed, for the findings paydown, and books the round 85
verdict and its prose slips.

## Next Steps

1. THE FLIP, carrying DECISION F275 D48's obligations: the full suite is the backstop, the input
   is re-derived by round 82's committed generator at the flip's own base, and any site fallen
   to zero witnesses is a stop. The stale test double at
   `packages/orchestration/project_registry.py:856` is updated in the flip's own commit.
2. Then the classic store, then the closure sequence.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20
  sessions and 60 rounds without a replacement, so this feature closes only at full scope.
- ONE ROUTED LOAD IS REACHED BY NO TEST. `dashboard project` dies at its first import, so its
  load stays unproven until `R-0883` is repaired.
- THE INPUT SET IS REPRODUCIBLE ONLY FROM ROUND 77's TWO SCRATCH JSON FILES, and the re-key
  cannot see a deleted ruled site.
- The open set is 87 by distinct id at this round's base, with `R-0809` and `R-0880` open. Four
  are High — R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.

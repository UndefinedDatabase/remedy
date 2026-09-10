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

ROUND 43 takes the reading DECISION F275 D22 took for the TASK records and nobody had taken
for the JOB records: both shipped classes IMPORTED and compared field by field, plus the
shape readings a name comparison cannot give. The pair is CLEAN — 13 shared names and the
only two `Job`-only names are the renames `id` and `name` — so there is no third unmeasured
record pair, and DECISION F272 D15's sentence holds for the job record where D22 disproved
it for the task record. DECISION F275 D24 records that, the `created_at` shape change at six
sites, and `budget`'s already-guarded nullability. No production line moves.

## Next Steps

1. THE FLIP. Its target API now exists (round 42) and its record shapes are now measured
   (this round), so it applies: `.agent/f275_t003_flip_sites.md` for the `.id` and `.name`
   sites, `.agent/f275_t003_flip_seam.md` for the classic store seam, and
   `.agent/f275_t003_record_shapes.md` for the type sites and the `created_at` rewrite. It
   lands as the one declared-oversize commit AGENTS.md permits per feature, with the
   inseparability reason AND the real size stated in the handback BEFORE review, and it
   registers `Task.acceptance_checks`'s structured form as a finding naming the feature that
   owns acceptance criteria, per amend0908-f275-finish rule 4.
2. The resolver collapse DECISION F260 D5 places in T003 — `resolve_any_job_id`, the "TWO
   job stores" paragraph, every which-store branch and the absence test — with the classic
   store, which is the same commit range by that decision's own terms.
3. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- Step 1 is the largest single commit this repository will take. Four rounds have now
  measured it and three found it larger: D17 sized it at 1766 changed lines, D21 at 3771
  across 263 files, D22 added a type pair, D23 found three pieces of its target API
  missing, and D24 is the first to find NOTHING new.
- The open set is 86 by distinct id at this round's base `7f8724c3`. This round registers
  none and resolves none. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's,
  per DECISION F272 D12.

# Plan — F255 Teacher role

Branch: feature/f255-teacher-role, cut from `main` at b35d350b, the merge commit
of pull request #207. No pull request is open for this branch; on this project
the PR is created by the closure round.
`.agent/live_review.md` is the source of truth for the open set, for the next
free finding id and for the round map; this file repeats none of them.

## Goal
A fourth configured role, `teacher`, that narrates a running mission and answers
operator questions about the operator's own code, and never influences the run.
DONE when passive narration keyed to an enumerated set of ledger events (Stage 1,
deterministic templates, zero tokens) and on-demand Q&A (Stage 2, through the
teacher role's own model) both work, the three grounding sources are never mixed
silently, teacher spend is reported as its own role in the F103 ledger, and the
read-only invariant is proven behaviourally.

## Current Step
R5: apply DECISION F255 D6 to `docs/agents/handback_template.md`, add checklist
item 30 so a duplicate id cannot be minted again, record the R4 verdict, and
resolve R-0462, R-0602 and R-0603. The feature file is not touched and no code
is written.

## Next Steps
1. R6 BUILDS T001 — the role vocabularies. `teacher` joins `KNOWN_ROLES` and
   `ConventionsRole`, with the renamed seven-to-eight pin in the SAME commit as
   the tuple it guards, plus a `teacher.model` config key modelled on
   `orchestrator.model`. This is the first round of this feature to touch source.
2. R7 BUILDS T002 AND T003 TOGETHER — Stage 1 narration and the behavioural
   read-only proof — because a read-only feature whose read-only-ness is
   unproven is this feature's likeliest failure.
3. T004, Stage 2 Q&A, comes last and only once the grounding-source labelling
   of T002 is real.

## Risks
- R6 IS THE FIRST SOURCE-TOUCHING ROUND OF THIS FEATURE. Its gate must include
  the tests that read the role vocabulary, not only the state-reader four, and
  the seven-to-eight pin is a deliberate tripwire rather than an accident.
- STAGE 1 MUST STAY ZERO-TOKEN TO BE WORTH HAVING. If narration quietly starts
  calling a model, the feature loses both its cost story and its offline story.
- THE AMENDMENT IS NOW THE SPEC. A T-slice that drifts from it is a finding
  rather than a preference, which is why it was written down before any build.

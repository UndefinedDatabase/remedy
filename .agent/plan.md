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
R6: register R-0604, record the R5 verdict, and build T001's first half — the
name `teacher` in `KNOWN_ROLES` with its frozen pin renamed and extended in the
SAME commit. The first source-touching round of this feature.

## Next Steps
1. R7 BUILDS T001'S SECOND HALF: `teacher` joins `ConventionsRole` with a
   conventions document under `docs/agents/`, and a `teacher.model` config key
   modelled on the existing `orchestrator.model` spec. The conventions loader
   caps such a document, so its size is measured before it is authored.
2. R8 BUILDS T002 AND T003 TOGETHER — Stage 1 narration over an enumerated
   event set, and the behavioural read-only proof — because a read-only feature
   whose read-only-ness is unproven is this feature's likeliest failure.
3. T004, Stage 2 Q&A, comes last and only once the grounding-source labelling
   of T002 is real.

## Risks
- FIVE ROLE LISTS EXIST AND ONLY ONE IS TOUCHED HERE. R2 measured them;
  DECISION F255 D1 rules that the CLI-override and token-cost lists are
  deliberately NOT extended, so a later reader finding `teacher` absent from
  them is seeing a decision rather than an omission.
- STAGE 1 MUST STAY ZERO-TOKEN TO BE WORTH HAVING. If narration quietly starts
  calling a model, the feature loses both its cost story and its offline story.
- THE AMENDMENT IS NOW THE SPEC. A T-slice that drifts from it is a finding
  rather than a preference, which is why it was written before any build.

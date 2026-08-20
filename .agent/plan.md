# Plan — F255 Teacher role

Branch: feature/f255-teacher-role, cut from `main` at b35d350b, the merge commit
of pull request #207. No pull request is open for this branch; on this project
the PR is created by the closure round.
`.agent/live_review.md` is the source of truth for the open set, for the next
free finding id and for the round map; this file repeats none of them.

## Goal
A fourth configured role, `teacher`, that narrates a running mission and answers
operator questions about the operator's own code, and never influences the run.
DONE when passive narration keyed to ledger events (Stage 1, deterministic
templates, zero tokens) and on-demand Q&A (Stage 2, through the teacher role's
own model) both work, the three grounding sources are never mixed silently,
teacher spend is reported as its own role in the F103 ledger, and the read-only
invariant is proven behaviourally.

## Current Step
R3: record the R2 verdict and land six DECISIONs — the role vocabularies, the
unmet event-vocabulary dependency, spend reporting, behavioural read-only proof,
`remedy teach` in place of `do watch`, and the withdrawal of the dead handback
token cap. Nothing is built and the feature file is not amended this round.

## Next Steps
1. R4 AMENDS `docs/roadmap/features/T5_F255.md` from these rulings, adding the
   Design, Task slicing, Acceptance and Do-not-touch sections its registration
   stub has never carried, and replacing the superseded `do watch` phrasing so
   the file and DECISION F255 D5 never disagree on disk.
2. THE DOCS ROUND AFTER IT applies DECISION F255 D6 to
   `docs/agents/handback_template.md`, removing the withdrawn token cap.
3. R6 ONWARD BUILDS THE T-SLICES the amendment names, Stage 1 before Stage 2,
   the role vocabularies first because everything else depends on them.

## Risks
- THE REGISTRATION NAMES GROUND THAT DOES NOT EXIST, and R2 measured exactly
  which: no stable event vocabulary, no budget pool, no `watch` command, and a
  read-only annotation nothing enforces. The DECISIONs rule each gap rather than
  building around it, but each ruling narrows what "DONE" can honestly mean.
- STAGE 1 MUST STAY ZERO-TOKEN TO BE WORTH HAVING. If narration quietly starts
  calling a model, the feature loses both its cost story and its offline story.
- READ-ONLY IS PROVEN BY ONE TEST SHAPE. If that test is weak, the feature's
  hardest invariant is decorative — DECISION F255 D4 is only as good as the
  test R6 writes.

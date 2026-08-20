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
R9: record the R8 verdict and build Stage 1 narration — the enumerated event
set, the deterministic templates and the unrecognised-event path — as one new
module with its own tests. T001 is complete as of R8.

## Next Steps
1. R10 BUILDS THE SURFACE AND THE PROOF TOGETHER: `remedy teach` printing the
   narration over a real run log through `timeline.load_run_events`, its
   command-catalog entry declaring `action_class="read_only"`, and T003's
   BEHAVIOURAL proof over that command — bytes on disk unchanged across the
   call. T002 and T003 were planned as one round; they are two because the
   module and its tests alone measure 221 lines, and a block carrying the CLI
   surface as well cannot fit the 490-line cap of DECISION F085 D6. The proof
   travels with the SURFACE because the module opens nothing and takes no path,
   so proving it read-only would prove the half that was never at risk.
2. T004, Stage 2 Q&A, follows: the small context, the source labelling, the
   level dial, and spend recorded under the role name `teacher`. It is also the
   round that gives `teacher.model` its first reader.
3. The integration gate and the closure round follow T004, per
   docs/roadmap/STATUS_closure_protocol.md.

## Risks
- STAGE 1 IS ZERO-TOKEN ONLY WHILE NOTHING CALLS A MODEL FROM IT. The module
  built here imports no provider and opens no file, and a test asserts both; if
  a later round routes narration through a model, that test is the tripwire.
- THE READ-ONLY INVARIANT IS NOT YET PROVEN BEHAVIOURALLY. Nothing an operator
  can invoke exists until R10, and this branch's pull request is created by the
  closure round, so no narration reaches an operator before its proof lands.
- NARRATION IS UNDOCUMENTED IN `docs/` UNTIL R10, deliberately: documenting a
  module nobody can call would describe a capability that does not exist.

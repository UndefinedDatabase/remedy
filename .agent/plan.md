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
R17 persists the R16 verdict and its three findings, then closes the one that is a
code defect: `remedy teach ask` gains `--file`, so grounding source (2) — the
workspace code the ruled Design puts in Stage 2's context — finally has a
production caller instead of only a test one.

## Next Steps
1. The INTEGRATION GATE round follows, per docs/agents/integration_gate.md: the
   full suite, because T002, T003 and T004 all touch the CLI catalog, which the
   parser and the help renderer both read.
2. The CLOSURE round follows, per docs/roadmap/STATUS_closure_protocol.md:
   evidence job, fresh review zip, the STATUS line, and the pull request.

## Risks
- T004 WAS REPORTED COMPLETE AT R16 WHILE SOURCE (2) HAD NO CALLER. That is
  R-0610, and this round closes the code half; the Fortschritt line stops
  claiming a completeness the CLI did not have until now.
- R-0608 AND R-0609 BIND FUTURE BLOCKS, NOT THIS CODE. They are reviewer gate
  defects — a reflog absence clause that reads a harmless `git reset` as history
  rewriting, and a block that ordered a source and its tests as one oversize
  commit — and each is answered by the shape of this block rather than by an edit.

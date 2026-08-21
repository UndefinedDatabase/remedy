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
R15: a RECORD round. It registers finding R-0607 against the R14 block's omitted
canary, persists the R14 verdict, and advances this plan. It builds nothing — the
session that reviewed R14 reached its limit, and a verdict that lives only in a
chat window is a verdict this project cannot audit.

## Next Steps
1. R16 FINISHES T004, the model half of Stage 2: `remedy teach ask` on the CLI
   over `teacher_qa.build_teacher_context`, the teacher model call through
   `resolve_role_config("teacher")`, the honest refusal when no model is
   configured, and the spend row written through the `teacher_spend` seam R13
   built. There is NO generic text-completion provider in this repository today:
   the providers under `packages/providers/` are role-specific and schema-bound,
   so R16 must DESIGN the teacher's model seam rather than discover one, and
   that design is the round's first and largest risk.
2. The INTEGRATION GATE round follows T004 — the full suite, per
   docs/agents/integration_gate.md — because T002 and T003 touch the CLI
   catalog, which the parser and the help renderer both read.
3. The CLOSURE round follows, per docs/roadmap/STATUS_closure_protocol.md:
   evidence job, fresh review zip, the STATUS line, and the pull request.

## Risks
- `teacher_spend.record_teacher_question` HAS NO CALLER YET. R13 built and
  red-proofed the seam; until R16 wires it, F255's cost acceptance is unmet.
- THE READ-ONLY PROOF COVERS NARRATE ONLY; `teach ask` needs its own, and it
  must exclude the ledger row R13 introduced by name rather than by silence.

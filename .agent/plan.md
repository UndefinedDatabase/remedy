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
R13: the BILLING half of T004. It rules how a teacher question is recorded
(DECISION F255 D7), amends `token_ledger`'s own module text so the ruling and the
module do not disagree on disk, and builds the one writer that records the row.
It calls NO model: the model call is R14, over this seam.

## Next Steps
1. R14 FINISHES T004, the model half of Stage 2: `remedy teach ask` on the CLI
   over `teacher_qa.build_teacher_context`, the teacher model call through
   `resolve_role_config("teacher")`, the honest refusal when no model is
   configured, and the spend row written through `teacher_spend`.
2. The INTEGRATION GATE round follows T004 — the full suite, per
   docs/agents/integration_gate.md — because T002 and T003 touch the CLI
   catalog, which the parser and the help renderer both read.
3. The CLOSURE round follows, per docs/roadmap/STATUS_closure_protocol.md:
   evidence job, fresh review zip, the STATUS line, and the pull request.

## Risks
- T004 WAS RESLICED INTO TWO ROUNDS by the reviewer at R13, because the billing
  ruling and the model call did not fit one block under the 490-line cap. The
  feature file's T004 is unchanged; only the round boundary moved.
- R14 IS WHERE THE COST STORY IS PROVEN OR LOST. R13 records a row from figures
  it is GIVEN; R14 must produce real ones from a real call, or D3 is unmet.
- THE READ-ONLY PROOF COVERS NARRATE ONLY; `teach ask` needs its own, and the
  ledger row R13 introduces is a WRITE that proof must exclude by name.

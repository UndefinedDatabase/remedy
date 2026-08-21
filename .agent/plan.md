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
R18 is the INTEGRATION GATE, per docs/agents/integration_gate.md: the full suite
on this branch and again at the merge base b35d350b, the two failure sets
compared, every difference attributed by direct evidence, and the whole record
committed under `.agent/gate_f255_r18/`. It also persists the R17 verdict. It
changes no source file and no test file.

## Next Steps
1. The CLOSURE round follows, per docs/roadmap/STATUS_closure_protocol.md:
   evidence job, FRESH review zip, the STATUS line authored by the reviewer and
   committed last, and the pull request — which is created there and merged at
   the NEXT feature's Open PR Gate, never in the session that creates it.

## Risks
- A BRANCH-ONLY FAILURE COUPLED TO FEATURE CODE IS A BLOCKER, not a repair to
  fold into this round: it ends the gate and earns its own reviewed round.
- BASE PARITY CAN BE VOIDED BY A REBUILD THE DIGEST CANNOT SEE. F085 R72 measured
  a byte-identical `apps/ui/dist` whose mtime had moved, and `_frontend_is_stale`
  decides by mtime, so this round reads BOTH and claims parity only if neither
  moved (finding R-0565).
- THE OPEN SET IS 183 AND NONE OF IT IS PAID DOWN HERE. R-0607, R-0608 and R-0609
  are reviewer-process findings; R-0610's code half landed at R17 and only the
  reviewer's own text may resolve it.

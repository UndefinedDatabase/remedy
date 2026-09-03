# Plan — F109 Semantic dedupe

Branch: feature/f109-semantic-dedupe, cut from `main` at
`5e18a8536afa086b591b5a2e13009d68d6227432` (pull request 231 merged).

## Goal

Within a RESUMED session only, stop resending context the model has
already provably received: segments whose hash already went to that exact
session are replaced by short reference markers. Everywhere else full
content wins, because only a resumed session guarantees the model still
holds the prior content. The scope rule of the whole feature is "resumed
session only, proven sends only".

## Current Step

Round 17, session 4. THE INTEGRATION GATE
(docs/agents/integration_gate.md): the full suite on this branch and at
the merge base, compared, with every branch-only failure attributed, and
the evidence landed under `.agent/gate_f109_r17/`. Also book round 16's
PASS, resolve `R-0780` and `R-0781`, and register and repair `R-0782` —
the `_capture_compositions` docstring, the third stale-prose site of the
same class, which still says the dedupe report has no consumer.

## Next Steps

- The closure sequence (docs/roadmap/STATUS_closure_protocol.md):
  evidence job, a FRESH review zip, the authored STATUS line, the PR.
  That sequence also runs the single consolidation pass on the checklist
  of docs/agents/planner_reviewer_prompt.md section 3.

## Risks

- A reproducible branch-only failure coupled to F109 code is a CLOSURE
  BLOCKER and earns its own reviewer-gated round; it is never repaired
  inside the gate round that found it.
- Nothing dedupes in production: every concrete adapter returns
  `supports_resume = False`, so the mechanism is suite-only today.
  `docs/system/semantic-dedupe-v1.md` states this plainly.
- The open finding set is a SET DIFFERENCE, not a subtraction: two ids
  carry two `Done:` lines each. That is `R-0778`.
- `R-0769` is registered, not fixed: its repair edits `README.md` and a
  docs test, neither of which F109 owns.

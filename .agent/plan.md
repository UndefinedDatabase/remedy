# Plan — F079 Context handoffs

Branch: feature/f079-context-handoffs

## Goal
Session and context-window boundaries stop losing knowledge — DONE in
substance: T001 composer (idempotent, pure), T002 triggers + loop
consumption + reference verification, T003 measured boundary recall
(100 % open-item threshold met, report archived). R-0199 fixed
(metadata-manifest digest, 11.4x). Spec: docs/roadmap/features/
T1_F079.md. What remains is proving the whole, then closing.

## Current Step
R3: the integration gate per docs/agents/integration_gate.md — full
suite at HEAD and at the merge base, per-id attribution of every
difference, evidence under .agent/gate_f079_r3/. The reviewer issues
the gate verdict.

## Next Steps
- R4: closure per docs/roadmap/STATUS_closure_protocol.md (own
  round): evidence job + fresh review zip + authored STATUS [x] line
  + PR. R-0200/R-0202 roll back to .agent/candidates.md if unbuilt.

## Risks
- The known mid-run-UI-rebuild flake class (R-0202) may reappear in
  the base run — integration_gate.md step 3 carries the mandatory
  dist-hash neutralization check.
- Full-suite wall clock ~2.5 min per run; two runs plus attribution.

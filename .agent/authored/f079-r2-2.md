# Plan — F079 Context handoffs

Branch: feature/f079-context-handoffs

## Goal
Session and context-window boundaries stop losing knowledge:
build_handoff composes dossier + checkpoint reference + open decisions
+ next intent into handoff.json + rendered handoff.md (idempotent,
pure artifact — done in T001); triggers + loop consumption with
reference verification (T002); measured recall eval on a fixture
mission (T003). Spec: docs/roadmap/features/T1_F079.md.

## Current Step
R2: R-0199 fix (data_root_digest becomes a metadata-manifest digest;
per-run frequency and evidence field names retained), T002 triggers +
loop consumption + reference verification, T003 boundary recall eval
+ threshold assertion + archived eval report.

## Next Steps
- R3: integration gate per docs/agents/integration_gate.md
- R4: closure per docs/roadmap/STATUS_closure_protocol.md (own round)

## Risks
- R-0203 constraint: consumption resolves ALL sources through one
  root discipline; document it at the consumption seam.
- Evidence-shape care in the R-0199 fix: digest definition changes,
  call frequency and field names do not; gauntlet evaluator/test
  consumers must be inspected before the edit.
- Do-not-touch unchanged: no automatic context-pressure detection, no
  cross-machine transport, no memory features beyond composition.

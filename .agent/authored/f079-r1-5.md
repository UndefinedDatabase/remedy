# Plan — F079 Context handoffs

Branch: feature/f079-context-handoffs (from main after PR #180 merged
at the Open PR Gate)

## Goal
Session and context-window boundaries stop losing knowledge:
build_handoff composes dossier + checkpoint reference + open decisions
+ next intent into handoff.json + rendered handoff.md (idempotent,
pure artifact — producing it changes no state); triggers + loop
consumption with reference verification; measured recall eval on a
fixture mission. Spec: docs/roadmap/features/T1_F079.md.

## Current Step
R1: candidate sweep persisted in live_review; R-0199 measured
diagnosis (raw numbers to handoff); reuse inspection
(mission_dossier renderer, checkpoints verification, recall harness);
T001 schema + composer + idempotence + unit tests.

## Next Steps
- T002: triggers (explicit CLI + loop-terminates-for-limits/stop) +
  loop consumption + stale-reference refusal + tests
- T003: boundary recall eval on a fake-provider mission + threshold
- R-0199 fix order once the diagnosis numbers are in
- Integration gate round, then closure (its own round)

## Risks
- Reuse is mandated: dossier renderer, checkpoint verification, recall
  harness — new implementations of existing pieces are rejects.
- Do not touch: automatic context-pressure detection, cross-machine
  transport, memory features beyond composition.
- Idempotence vs timestamps: provenance timestamps come from SOURCE
  artifacts, never wall clock — same state must hash identical.

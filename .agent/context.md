# Context — F079 Context handoffs (in progress)

## Active Branch
feature/f079-context-handoffs — claimed from main after the Open PR
Gate merged PR #180 (amend0805-v3).

## Scope
F079 (Context handoffs, Tier 1): handoff artifact composition
(dossier, checkpoint reference, open decisions, next intent) with
explicit + loop triggers, loop consumption with reference
verification, and a measured recall eval on a fixture mission. R1 also
carries the F075 candidate sweep and the R-0199 measured diagnosis.

## Constraints
- Round gates stay scoped pytest commands; the full-suite
  pytest -n auto run belongs to the integration gate, where the
  resource-safety rules of tests/regression apply.
- Building a handoff mutates nothing; missing sources render as
  explicit gaps, never invented content.

## Steps
R1: Open PR Gate + claim + candidate sweep + R-0199 diagnosis + reuse
inspection + T001. Then T002, T003, integration gate, closure.

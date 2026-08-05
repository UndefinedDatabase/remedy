# Context — F075 closed; next feature not yet claimed

## Active Branch
feature/f075-self-run-gauntlet — F075 closure PR open, NOT merged. The
next feature (F079, Context handoffs) starts from main AFTER the Open PR
Gate merges this PR.

## Scope
F075 is complete and accepted: gauntlet harness, evaluator, matrix,
frozen order set v4 + sample-project template, live runner, injection
driver, and the nine campaign-earned product changes, all reviewed round
by round. Built State is recorded in
docs/roadmap/features/T1_F075.md; STATUS.md carries the [x] line with
the evidence job, package and accepted HEAD.

## Constraints
- Nothing further ships on this branch. The closure commit was the last
  commit (Rule A4); do not append to it.
- ADR-0001 is PROPOSED, never applied by a machine: CYCLE_SAFETY_CAP
  stays 1 and three pinned assertions hold it there.
- .agent/candidates.md is non-empty by design and blocks the next
  feature claim until its first reviewed round registers or resolves
  each entry.
- Round gates stay scoped pytest commands; the full-suite
  pytest -n auto run belongs to the integration gate, where the
  resource-safety rules of tests/regression apply.

## Steps
R1-R11 built and reviewed (PASS x11) → R12 ADR/diff prep + integration
gate PASS → R13 closure (done) → next: F079 in a fresh session.

# Context — F079 closed; next feature not yet claimed

## Active Branch
feature/f079-context-handoffs — F079 closure PR open, NOT merged. The
next feature (F080, Machine-readable roadmap mirror & STATUS.md)
starts from main AFTER the Open PR Gate merges this PR.

## Scope
F079 is complete and accepted: handoff composer (idempotent, pure
artifact), `remedy mission handoff` + loop boundary triggers,
consumption with checkpoint-reference verification and the shared
worktree-drift wording, measured boundary recall (100 % of open
items), and the R-0199 metadata-manifest digest fix. Built State is
recorded in docs/roadmap/features/T1_F079.md; STATUS.md carries the
[x] line with the evidence job, package and accepted HEAD.

## Constraints
- Nothing further ships on this branch. The closure commit is the
  last commit (Rule A4); do not append to it.
- .agent/candidates.md is non-empty by design and blocks the next
  feature claim until its first reviewed round registers or resolves
  each entry.
- Round gates stay scoped pytest commands; the full-suite
  pytest -n auto run belongs to the integration gate, where the
  resource-safety rules of tests/regression apply.
- ADR-0001 stays PROPOSED; CYCLE_SAFETY_CAP stays 1 until a human
  applies it.

## Steps
R1–R2 build (PASS) → R3 integration gate PASS (full suite green) →
R4 evidence job + fresh zip → R5 closure commit + PR (this commit) →
next: F080 in a fresh session.

# Context — F080 closed (R5), self-drive skill next

## Active Branch
feature/f080-roadmap-mirror — the closure commit (STATUS `[x]` + README
sync + final .agent state) is the last commit on it, and the PR is
open. Not merged here by design: it merges at the NEXT feature's Open
PR Gate, which is the operator's manual-review window. Accepted HEAD
for the package is 0a22bcbf, the last content commit.

## Scope
F080 is complete: T001 parser + grammar validation + generated index +
the `plan` CLI group, T002 report-only consistency checks, T003 the
feature→mission adapter, the docs page, and the R-0206 repair in the
path scrubber. Nothing further belongs on this branch — the next work
(S1+S2 self-drive skill) starts on a fresh branch after the gate.

## Constraints
- The closure commit touched exactly docs/roadmap/STATUS.md, README.md
  and .agent/ state (R-0154 exact-paths rule); STATUS and README landed
  together so no committed state has them disagreeing.
- STATUS.md stays human-owned (A4); the generated index and the review
  zips are never committed.
- .agent/candidates.md is non-empty: one open closure candidate, a
  block condition at the next feature's claim.
- Verification here is pytest, per file: tests/docs/ (the gate that
  pins README against STATUS), tests/cli/test_golden_path.py,
  tests/ui_server/test_dashboard_contract.py and
  tests/regression/test_resource_safety.py. The full suite was green at
  the accepted HEAD (15951 passed, 19 skipped) and the R2 integration
  gate PASSed with zero branch-only failures.

## Steps
Authored texts applied (STATUS line, README pair, live review,
candidates) → four gates green → closure commit → push → PR created,
not merged → handoff rewrite with the grep proof that every applied
text is byte-identical to its receipt.

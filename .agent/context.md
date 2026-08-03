# Context — F071 Mission dossier

## Active Branch
feature/f071-mission-dossier (from main 097e4959, post reg0803
micro-round merge PR #177) — CLOSED at acb02acd, PR open, unmerged.

## Scope
Roadmap F071 (Tier 1, docs/roadmap/features/T1_F071.md): the
mission dossier module, its loop wiring and its tests. Production
code path → SPLIT rounds only; reviewer gated every merge.

## Constraints
- Round gate = scoped pytest command(s) authored in the step block;
  canary per handback: python3 -m pytest tests/cli/test_golden_path.py -q.
  Full-suite pytest -n auto ran at the R3 integration gate
  (resource budget: keep runs scoped; the resource-safety rules of
  tests/regression apply). Gate run logs are written OUTSIDE the
  repo during the run (R-0176).
- Commits < 500 lines; authored texts applied byte-exact from
  .agent/authored/f071-r<round>-<n>.md after sha256 verification.
- Do-not-touch: cross-session handoffs (F079), prompt ordering
  policy, memory systems beyond the dossier.

## Steps
R1 T001+T002 → R2 fixes + T003 → R3 fix + integration gate →
R4 closure (current, done). The PR merges at the next feature's
Open PR Gate; nothing here merges it.

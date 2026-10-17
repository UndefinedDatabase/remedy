# Handoff — scale correctness (audit remedy_scale_audit_2026-10-17), branch feature/scale-correctness-routing

Operator order 2026-10-17, one session. Finding R-1337 (High), DECISION scale-1017 D1 to D11.
Not a roadmap feature; F078 stays Rule A5's next; `.agent/STOP` kept. Not merged, not installed.

## Verification (python3 3.10.12)
- Full local run `python3 -m pytest -n auto -q` on the commit before the last: 21472 passed,
  1 failed (a context.md resource-safety word, repaired). The first run had 9 reds, all repaired.
  The final full run is recorded in the PR body with the commit SHA and tree.
- ruff clean. Matrix: 16 cases + 40 routing rows, all met.

| Item | Status | Reason |
|---|---|---|
| P0-1 path/alias scope, hold | done | resolve_order_path, lane hold |
| P0-2 repo-aware risk routing | done | order_risk floor; vocabulary is a floor, not a classifier |
| P1-3 check-only job and artifact filter | done | deliverable_check_task deleted |
| P1-4 one order budget | done | order_ledger; planning tokens estimated; waiting jobs keep the leftover |
| P1-5 stale study | done | study_stale_reason |
| P1-6 scale suite | done | fake providers; real Pi/Ollama calibration waits for approval |
| Verification scope by language/package | skipped | project_tests runs one command; not built |
| Release notes into CHANGELOG.md routed full | deviated | documentation target stays bounded |

Next: decodeux reviews the PR; a real Pi/Ollama calibration only on approval.

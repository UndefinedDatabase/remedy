# Plan — amend0831-vocab-registrations (registration round)

Branch: feature/amend0831-vocab-registrations, cut from `origin/main` at
`de8a58b1`. REGISTRATION ONLY — no feature in this order is implemented here.

## Goal
Register eight features (F259 vocabulary & concept model, F260 job/execution
marriage, F261 CLI vocabulary v2, F262 list commands v2, F263 human-change
absorption, F264 steering channel, F265 teacher learning UI v1, F266
`remedy study`): eight feature detail files, eight STATUS lines in Package 1 in
the operator's order, and the ledger counters moved 258 -> 266.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| Open PR Gate: PR #228 repaired and merged | done | its red CI was a README ledger drift; merged as `de8a58b1` |
| eight feature detail files | done | two commits, split under the 500-insertion cap |
| eight STATUS lines + TOTAL_FEATURES + README counters | done | one commit, ledger atomicity |
| tests/docs, test_roadmap_index, test_golden_path | green | 295 / 30 / 42 passed |
| push, PR, hosted CI, merge | pending | this round's remaining work |

## Next Steps
1. Push the branch and open the PR.
2. Watch the hosted CI run to the end; read the check status and merge only on
   green. A red run is this branch's work order, not a blocker.
3. Verify 0 open PRs, delete the remote branch, return to `main`.

## Risks
- The three tier headings added to `docs/roadmap/STATUS.md` are the only
  structural change to that file; a reviewer who expects a bare insertion after
  F114 should read the decision recorded in `.agent/decisions.md` for why a bare
  insertion would have reddened the filename/tier pin for all eight lines.

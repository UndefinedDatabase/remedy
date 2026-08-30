# Plan — amend0830-cost-first

Branch: feature/amend0830-cost-first, cut from `main` at the merge commit of
pull request #226 (F258). Operator-authored task, not a self-drive round.

## Goal
Pull the token-economy features forward in the roadmap execution order, fix
R-0757 (self-use runner silently ran under the fake provider on an unflagged
call instead of the product's real default), and move unreferenced/superseded
zips in the package archive into `superseded/`.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| Part 0 — preconditions, PR #226 merge | done | green CI, merged + branch cut |
| Part 1 — roadmap pull-forward | done | F106/F108/F109/F110/F112/F114 moved to a new Tier 3 heading ahead of Tier 0; `plan next` now proposes F106 |
| Part 2 — R-0757 fix | done | `self_use_runner.run_next_self_use_item` resolves role config, refuses on no real provider; ledger `Landed:` marker written |
| Part 3 — archive hygiene | done | 15 unreferenced zips moved to `remedy-history/zips/superseded/`, hashes recorded |
| Part 4 — verify, PR, merge | in progress | full verification green; committing now |

## Next Steps
1. Commit in small logical steps (roadmap+decisions, self_use_runner fix+tests, ledger note).
2. Push, open PR titled "amend0830: cost-first execution order + honest self-use provider".
3. Watch hosted CI; merge on green.
4. Restore ORIG_BRANCH (feature/f258-self-use-v2 — already merged/deleted, so land on `main`).

## Risks
- R-0757's own text claims `remedy do job-run` resolves a real provider by
  default; reading `do_cmd.py` shows the resolved role config is not actually
  threaded into its `run_job()` call either. Flagged in the ledger addition
  as an unverified deviation, not re-litigated — the self_use_runner fix does
  not depend on that claim either way.
- R-0570 (Low) and R-0736 (Medium) remain open, out of this task's scope.

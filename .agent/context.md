# Context — F252 Standing-red paydown

## Active Branch
`feature/f252-standing-red-paydown`
Base commit: `7baff1d` (main after PR #160 merge)

## Scope
Every id in `.agent/f251_baseline/class_map.txt` reaches an explicit
terminal state, one class per slice. R1 closed D8, D10, D11. R2 covers
R-0152 plus D9, D7, D5, D13, the two stopped F-A ids, D6, the D4
remainder, D1, D14, D3 (park), D12.

## Next Steps
See `.agent/plan.md` for the round's ordered slices; this file records the
boundaries they run inside.

## Constraints
- F251's quarantine rules unchanged: never deletion, never blanket
  directory skips, never weakened assertions; a marker needs a reason
  string and a backlog reference per test.
- A class whose honest fix exceeds its bucket stops and reports.
- Reviewer-authored texts under `.agent/authored/` are applied by copy and
  sha256-verified before any commit; `plan.md` and `live_review.md` are
  such texts this round and are never hand-edited.
- Every slice ends green against the baseline subset rule plus the
  `tests/cli/test_golden_path.py` canary, then commits and pushes.

## Resource safety
Tests run in ONE session at a time through `scripts/remedy_pytest.sh`;
never a background pytest, never a second parallel suite — see
`docs/reviewer-safety.md`. The real-runtime tests additionally hold a
cross-worker file lock and bind a per-worker port, never the product
default 5173.

## Do not touch
`docs/roadmap/ROADMAP.md`; STATUS entries other than the F252 line;
closure artifacts (evidence job, review zip, `[x]`) — those belong to a
later reviewer-gated round.

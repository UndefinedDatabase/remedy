# Live Review — F115 Prompt breakdown & cost report

> Round-by-round review record for F115, reset at the feature claim. The F111
> record is preserved in git history at its closure commit 98a49b5c. Finding
> IDs continue monotonically across features and are never renumbered.

## Steps
R1 claim, state reset and shape inventory → T001 manifest-alongside-actuals
persistence with backfill tolerance → T002 aggregation queries, the pure
renderer and its goldens → T003 CLI, period comparison and json schema →
integration gate → closure.

## Findings

- R-0320 — Low — carried forward from the F111 closure-candidates file under
  the disk-vehicle rule (docs/roadmap/STATUS_closure_protocol.md,
  "Closure-candidate findings"). A stop reason no code can ever emit:
  `STOP_REASONS` in `packages/orchestration/builder_bridge.py` declares
  `stale_diff_context`, and a repo-wide grep over every `.py` file finds that
  string in exactly one place — the frozenset itself. Nothing raises it,
  nothing tests it, nothing reads it. It predates the F111 branch (it is
  present at the merge base 4e0b762e), so it was not an F111 defect and was
  deliberately not fixed there. It is not fixed in F115 either: AGENTS.md bars
  mixing an unrelated fix into a feature branch, and F115 opens the token
  ledger and the report renderer, not the builder bridge. The remedy — wire it
  to the condition it names, or delete it — is a one-commit change that
  belongs to whichever feature next has a legitimate reason to open
  `builder_bridge.py`. Recording it here keeps it findable after
  `.agent/candidates.md` is emptied, which is the whole point of the
  carry-forward rule. OPEN.

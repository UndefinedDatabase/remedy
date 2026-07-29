# Live Review — F252 Standing-red paydown (154 ids, 13 classes)

Branch: feature/f252-standing-red-paydown
Scope: every catalogued standing-red id reaches an explicit terminal
state, class by class (catalog: .agent/f251_baseline/class_map.txt).

## Steps
- R1: claim + state reset + product-bug classes D8, D10, D11. Done.
- R2: R-0152 + all remaining classes; 143 fixed, 11 quarantined by
  decision; full suite 14295 passed / 0 failed / 19 skipped. Done.
- R3: persist this verdict + R-0153, fix R-0153, then the
  integration-gate round per docs/agents/integration_gate.md incl.
  the three-consecutive-runs determinism proof. In progress.

## Findings
- Done: R-0153 (nit): tests/docs/test_docs_consistency.py — in the
  rewritten README honesty pin, `assert unaccepted <= named` is a
  tautology (`unaccepted` is derived from `named`), a dead check
  that reads as coverage. Fix: delete the assertion and its comment
  line; the accepted-blocks loop above it is the real check.

## Verdicts
- R1: PASS (reviewer, 2026-07-29). Range 7baff1d..cc247fa. Details
  in git history of this file; LAST_REVIEWED_SHA was cc247fa.
- R2: PASS (reviewer, 2026-07-29). Range cc247fa..fc3e843, 14
  commits. Authored proofs disk-to-disk: cmp 0 for plan.md and both
  authored files; live_review.md deviates from f252-r2-1 by exactly
  the one instructed `Done: R-0152` edit. Diff reviewed bottom-up:
  product fixes (catalog action classes, do-planning fallback
  removal, evidence-packaging v1.1 + verdict read-back +
  self-check scope, provider-evidence zero counts, named exception
  catches, runtime port override) all carry in-code rationale; test
  edits are honest updates or strengthenings — D6 removed zero
  assertions, renames declared, quarantines are per-test skips with
  reason + backlog ref (10x D3, 1x D12 per the registered
  decisions). Full suite re-run by the reviewer: 14295 passed, 0
  failed, 19 skipped (11 quarantines + 8 pre-existing env-gated),
  matching the handback exactly; failing set empty, so all 154
  catalogued ids have left the standing set. R-0153 filed as nit,
  non-blocking. Verified tier: scoped gates + canary + a reviewer
  full-suite run (the official integration gate is R3).
  LAST_REVIEWED_SHA = fc3e843.

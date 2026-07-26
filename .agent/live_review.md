# Live Review — F016 Scaling task granularity
Branch: feature/f016-task-granularity
LAST_REVIEWED_SHA: cd13645
Finding IDs continue at R-0141.
## Findings

### R-0141 [low] Incomplete handback form (round 1) — Resolved (recorded)
Per-commit changed-files tables were ordered but only a net table
was delivered; commit cd13645 and .agent/decisions.md were absent
from the handoff tables. Substance was fully verifiable from the
real diff; no code change required. Future handbacks: per-commit
tables, every commit, every file.

## Round 1 verdict
PASS (round gate + canary tier). All T001-T003 gates independently
re-run by reviewer: 117 + 71 + 42 passed. Deviations declared in
.agent/decisions.md accepted. LAST_REVIEWED_SHA advances.

### R-0142 [low] Redaction pattern false-positives on "sk-" substrings — Documented risk (gap backlog)
FORBIDDEN_SECRET_PATTERNS entry `sk-[a-zA-Z0-9_-]{8,}` matches any
string containing "task-", "risk-", "disk-" + 8 more chars — the
branch name feature/f016-task-granularity trips
test_viewer_html_passes_precision (7 findings, reviewer-reproduced
standalone). Pre-existing pattern defect, not F016 code; vanishes
on main checkout. Fix (boundary before "sk") belongs to a
redaction-hygiene item, not this feature.

## Integration-gate round verdict
PASS (integration-gate tier). Base dcb8b1a: 181 failed. Branch:
162/158 across two runs, ~3 min wall with -n auto. The 10
first-run-only new failures: 9 xdist-flaky (empty intersection
with run 2; reviewer serial spot-check 3/3 pass), 1 = R-0142
(branch-name artifact). No full-suite regression attributable to
F016 code. Suite nondeterminism itself is pre-existing and
documented as residual risk (F052/F135 backlog).

## Final verdict
PASS_WITH_RISKS — ACCEPTED (2026-07-26, closure round)
R-0141 Resolved, R-0142 documented Low. Residual risks:
1. Full suite is nondeterministic under xdist and pre-existing RED
   on base (~160-181 failures churning; serial re-runs pass).
   Backlog: F135 flaky detector / F052 self-healing test rounds.
2. R-0142 redaction pattern false positive (Low, gap backlog).
3. Cross-group merge-cycle interactions are caught only by the
   final whole-plan revalidation (coarse abort, fail-open) — by
   design, documented in task_granularity.py.
LAST_REVIEWED_SHA: 2fad89295e11bc2aad51f7ae5f7de52b7542e9b5

### R-0143 [medium] Handback form defect repeated (R-0141 class)
The closure handback again omitted the ordered per-commit
changed-files tables (this time no changed-files table at all)
and the ordered grep proofs of byte-identical applied text.
Reviewer verified substance independently (STATUS line, zip
SHA-256, manifest head, live-review text) — the round FAILs on
form only. Second occurrence: next occurrence escalates and will
block until a handback template is adopted.
Resolution: handoff.md rewritten with per-commit changed-files
tables for every commit in dcb8b1a..HEAD and raw grep proofs.

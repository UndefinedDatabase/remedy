# Handback — F115 · R23 (CLOSURE retry) — HALTED again at the Built State

## Range
Review of 7bc57cd1..142e80c8 (branch feature/f115-prompt-cost-report).
STOPPED after ITEM A. ITEM B and ITEMs 3-7 NOT executed. No zip, no PR.

## Commits
### 1180fe7b chore(f115): save the R23 closure block and the R22 handoff
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f115-r23-1.md | +146/-0 | C0 block, verbatim, 146 lines |
| .agent/last_block.md | same bytes | cmp exit 0, sha256 5952dfc5… on both |
| .agent/handoff.md | rewrite | R22's handback, uncommitted until now |

### 142e80c8 docs(f115): register R-0342, the reviewer claim defect that halted R22
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | R-0342 appended; nothing above touched |

## THE STOP — ITEM B, two claims are false
Verified 54 claims mechanically against source (AST spans, not greps).
51 TRUE, 3 not. The two that block:

1. "The period is half-open … `prior_report_period` needs BOTH bounds
   (`token_ledger.py:1160-1161`)". FALSE citation. The both-bounds guard is
   1158 `if not since or not until:` / 1159 `return PriorReportPeriod(
   unavailable_reason=_PRIOR_REASON_OPEN_ENDED)`. Lines 1160-1161 are `try:`
   and `parsed_since = _parse_period_bound(since)` — the parse step, and not
   even both parses (`parsed_until` is 1162). Correct cite: `:1158-1159`.
2. "Three vocabulary decisions are load-bearing and pinned by tests:
   `COST_UNMEASURED_LABEL` … `COST_DEFAULT_LABEL` … `COST_UNNAMED_BUCKET_LABEL`".
   FALSE for two of the three. `grep -rniF` over ALL of `tests/` for
   `(unlabelled)`, `unlabelled`, `unlabeled`, `(unnamed)` and `unnamed`, and
   for the three constant NAMES, finds: nothing for `COST_DEFAULT_LABEL` and
   nothing for `COST_UNNAMED_BUCKET_LABEL` (the only `unnamed` hits are
   `"Unnamed job"` in test_trust_report.py and test_project_constitution.py,
   unrelated). Neither value appears in either golden fixture either. Only
   `COST_UNMEASURED_LABEL`'s value is pinned — test_cost_report.py plus both
   goldens. Changing `"(unlabelled)"` or `"(unnamed)"` turns no test red.
   Suggested repair: "…are load-bearing; `COST_UNMEASURED_LABEL` is pinned by
   the goldens and by tests/orchestration/test_cost_report.py, the other two
   only by the code that reads them."

Third, minor, not a blocker: `_cmd_stats_report` is cited as
`stats_ledger_cmd.py:509-568` in BOTH ITEM A and ITEM B; its real AST span is
509-566 (567-568 are the blank separator lines before the next `def` at 569).
Every content claim over the cited range holds, so ITEM A was committed as
authored; the reviewer may want `:509-566` in the Built State.

## Verification
- (a) `cmp .agent/authored/f115-r23-1.md .agent/last_block.md` → exit 0, no
  output. 146 lines, zero trailing-whitespace lines, sha256 identical.
- (b) ITEM A gates: `^- R-0342 — Low` → 1, exit 0 · `^## Steps` → 1, exit 0.
  Applied text sliced from the committed authored file: identical=True,
  2002 bytes both sides, preceding line blank.
- (c) `python3 -m pytest tests/docs/ -q` → `294 passed in 0.26s`, exit 0 — no
  regression, but the Built State section was NOT written or committed.
  Per-claim verification: 54 checked, 51 TRUE, 3 above. Scripts kept at
  `.remedy-wt/r23_verify{,2,3,4,5}.py` (gitignored).
- (d)-(g), (l) NOT RUN. No integrity check, no evidence job, no stash, no zip,
  no STATUS/README edit, no PR. DECISION F115 D7 still pends, so
  ` M scripts/make_review_zip.sh` is untouched. No stash was ever pushed —
  nothing to pop.
- (h)/(i) not applicable: STATUS.md still `[~] F115`, README still 44.
- (j) `git status --porcelain` → ` M scripts/make_review_zip.sh` only.
- (k) `git log --oneline 7bc57cd1..HEAD` → 142e80c8, 1180fe7b.
- `git rev-list --left-right --count origin/<branch>...HEAD` → `0	4`.

## Deviations & assumptions
| Item | Status | Reason |
|---|---|---|
| C0 | done | |
| ITEM A | done | |
| ITEM B | skipped | two false claims; stop-on-false-claim invoked |
| ITEM 3 | skipped | blocked by ITEM B |
| ITEM 4 | skipped | blocked by ITEM B |
| ITEM 5 | skipped | blocked by ITEM B |
| ITEM 6 | skipped | blocked by ITEM B |
| ITEM 7 | skipped | blocked by ITEM B |
Declared deviation: `.agent/plan.md` and this file are committed as a third
commit, which the block did not order. AGENTS.md If-Blocked mandates the plan
carry the exact blocker, and the closure ITEM 6 that would have rewritten both
was never reached; leaving them dirty would repeat the porcelain friction the
operator called out this round.
Deviations, declared: 93 lines, over the 60-line cap (AGENTS.md DECISION D15).
Cause is mandated content — three per-commit tables, the stop evidence with its
resolved file:line facts, the verification transcript and the eight-row
item-status table. No section was dropped.

## Next
Reviewer re-authors ITEM B's Built State with claims 1 and 2 corrected (and
optionally the span), then re-orders the closure from that item. ITEM A is
landed and must NOT be re-applied. Four commits await `git push`.

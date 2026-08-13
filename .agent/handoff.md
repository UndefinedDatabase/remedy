# Handback — F115 · R22 (CLOSURE) — HALTED on a false Built-State claim

## Range
Review of a43110ca..7bc57cd1 (branch feature/f115-prompt-cost-report).
STOPPED after ITEM 1. ITEMs 2-7 NOT executed, nothing further committed.

## Commits
### 593b86d4 chore(f115): save the R22 closure block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f115-r22-1.md | +221/-0 | C0 block, verbatim, 16455 bytes |
| .agent/last_block.md | +221/-156 | same bytes, cmp exit 0 |

### 7bc57cd1 docs(f115): record the R21 verdict and resolve R-0340
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | `Done: R-0340` + `Gate: R21 — PASS`, appended |

## THE STOP — ITEM 2, one claim is false
Authored clause: "Deliberately NOT built, and the report says so rather than
faking it: a per-role breakdown has ONE bucket ... a per-task-class breakdown
has no source at all".
The FACTS half is true. "the report says so" is FALSE — `remedy stats report`
prints NEITHER limit:
- `_cmd_stats_report` spans apps/cli/commands/stats_ledger_cmd.py:509-568 and
  its body contains no `_ROLE_LIMIT_NOTE`, no `role_limit`, no task-class text.
- `_ROLE_LIMIT_NOTE` (stats_ledger_cmd.py:373) has exactly TWO consumers, both
  owned by `stats cache`: `_cache_payload` (def :425, hit :436) and
  `_render_cache_human` (def :442, hit :489).
- F115's own guide states the refutation verbatim,
  docs/guides/cost-report-user-guide-v0.md:109-113: "`remedy stats report` does
  not print that limit itself — this page is where a reader meets it. The note
  has one owner, `remedy stats cache --by role`"; and :115-116 "The report stays
  silent rather than inventing a bucket."
This is R-0338's class again: a string was resolved to a module, not to its
enclosing function. Suggested repair for the reviewer to author: replace "and
the report says so rather than faking it" with "and the user guide says so
rather than the report faking it — `remedy stats report` stays silent, and the
role note's one owner is `remedy stats cache --by role`".

Secondary imprecision in the SAME paragraph block, worth one edit: the renderer
sentence says `render_cost_report_markdown` and `cost_report_json` /
`cost_report_json_bytes` "take report objects and return text".
`cost_report_json` returns `dict[str, Any]` (cost_report.py:292); only
`cost_report_json_bytes` (:341) and `render_cost_report_markdown` (:497) return
`str`.

## Verification
- (a) `cmp .agent/authored/f115-r22-1.md .agent/last_block.md` → exit 0, no
  output; both 16455 bytes; zero trailing-whitespace lines; 221 lines.
- (b) ITEM 1 gates: `^Done: R-0340` 1 · `^Gate: R21 — PASS` 1 · `^## Steps` 1.
  Three of three. Applied text sliced from the committed authored file, so the
  applied bytes ARE the authored bytes (identical=True for both entries).
- (c) ITEM 2 citations: 21 of 22 verified TRUE against source, 1 FALSE (above).
  `python3 -m pytest tests/docs/ -q` → `294 passed in 0.26s`, exit 0 — no
  regression, but the Built State section was NOT written or committed.
- (d)-(g) NOT RUN. No integrity check, no evidence job, no stash, no zip, no
  STATUS/README edit, no PR. The stash was never pushed, so
  ` M scripts/make_review_zip.sh` is untouched and DECISION F115 D7 still
  pends.
- (j) `git status --porcelain` → ` M scripts/make_review_zip.sh` and
  ` M .agent/handoff.md` (this file, deliberately uncommitted).
- (k) `git log --oneline a43110ca..HEAD` → 7bc57cd1, 593b86d4.
- `git rev-list --left-right --count origin/...HEAD` → `0	2` (2 unpushed).

## Deviations & assumptions
| Item | Status | Reason |
|---|---|---|
| C0 | done | |
| ITEM 1 | done | |
| ITEM 2 | skipped | false claim found; stop-on-false-claim invoked |
| ITEM 3 | skipped | blocked by ITEM 2 |
| ITEM 4 | skipped | blocked by ITEM 2 |
| ITEM 5 | skipped | blocked by ITEM 2 |
| ITEM 6 | skipped | blocked by ITEM 2 |
| ITEM 7 | skipped | blocked by ITEM 2 |
Declared deviation: this file is rewritten but NOT committed. AGENTS.md mandates
a handoff rewrite at every handback; the block mandates "commit nothing further".
Writing to disk satisfies both — the reviewer reads the working tree.
Deviations, declared: 88 lines, over the 60-line cap (AGENTS.md DECISION D15).
Cause is mandated content — two per-commit tables, the full stop evidence with
its file:line resolutions, the verification transcript and the eight-row
item-status table. No section was dropped.

## Next
Reviewer re-authors ITEM 2's Built State with the false clause corrected, then
re-orders the closure from ITEM 2. ITEM 1 is already landed and must NOT be
re-applied. Two commits await `git push`.

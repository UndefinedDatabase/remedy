# Handback — F115 · R24 (CLOSURE retry) — HALTED a THIRD time at the Built State

## Range
Review of 1df61a43..HEAD (branch feature/f115-prompt-cost-report).
STOPPED after C0. ITEM A, ITEM B and ITEMs 3-7 NOT executed. No integrity
check, no evidence job, no stash, no zip, no STATUS/README edit, no PR.

## Commits
### d4a27801 chore(f115): save the R24 closure block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f115-r24-1.md | +154/-0 | C0 block, verbatim, 154 lines |
| .agent/last_block.md | rewrite | cmp exit 0 against the authored file |

### <this commit> chore(f115): record the R24 halt in the plan and the handoff
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | rewrite | AGENTS.md If-Blocked: the exact blocker, 49 lines |
| .agent/handoff.md | rewrite | this file |

## THE STOP — ITEM B, two claims are false
41 claims checked mechanically against source and against the RUNNING CLI.
38 TRUE, 1 imprecise, 2 false. The two that block:

1. "the catalog entry's own description says why where `remedy stats --help`
   will print it". FALSE, and it is the R-0338/R-0342 class exactly.
   `apps/cli/help_renderer.py::_box` truncates every Commands row to
   BOX_WIDTH 78 and appends "…". RAW, `remedy stats --help`, exit 0:
     │  report           Cost report over ONE project's ledger: the cost table, whe…│
   The --all-projects rationale is never printed by that command. The command
   that prints the full description is `remedy stats report --help`, which
   goes through `render_command_help` and emits it un-boxed. Origin of the
   error: the source comment directly above the catalog entry in
   `apps/cli/command_catalog.py` itself asserts "`remedy stats --help` prints
   the description" — the reviewer copied a comment instead of running the
   command. Fix: name `remedy stats report --help`, or drop the where-clause.
2. "It also distinguishes … and one that existed but held no calls:
   `_PRIOR_REASON_UNPARSEABLE`, `_PRIOR_REASON_MIXED_AWARENESS` and
   `_PRIOR_REASON_EMPTY_PERIOD`". FALSE for the third. That constant reads
   "No previous period: this period ends at or before it starts, so it has no
   length and its prior window would have none either." and is returned when
   `length <= timedelta(0)` — a zero-length or inverted REPORT period, not a
   window that held calls. `prior_report_period`'s docstring says PURE — "no
   ledger, no clock, no I/O" — so none of its four reasons can mean "we looked
   and found nothing". That fact lives in `cost_report.py`:
   `COST_NO_COMPARISON_DEFAULT` vs `COST_EMPTY_COMPARISON` ("The previous
   period was read and holds no call at all…"), chosen by
   `_no_comparison_sentence`. The following sentence "…the report keeps them
   different" is TRUE of the report and FALSE of the constants it lists.

Imprecise, not a blocker: "one whose bounds contradict each other" for
`_PRIOR_REASON_MIXED_AWARENESS`. The real case is one bound offset-aware and
the other naive, whose difference is undefined — not contradictory bounds.

## Why ITEM A was blocked too
R-0343's own text certifies the R24 rewrite as carrying "no claim the reviewer
had not re-verified mechanically in the same session". Claim 1 above refutes
that certification. Committing ITEM A verbatim would write a false claim into
the permanent finding ledger — the one thing stop-on-false-claim exists to
prevent — and the worker may not edit an authored finding. So ITEM A is handed
back for re-authoring rather than applied. Its other claims all hold, verified:
`token_ledger.py:1160-1161` are `try:` / `parsed_since = …` with the guard at
1158-1159; a recursive grep over `tests/` for `unlabelled`,
`COST_DEFAULT_LABEL`, `COST_UNNAMED_BUCKET_LABEL` and `(unnamed)` returns
NOTHING, exit 1, goldens included; the repo carries five unrelated stashes.

## Verification
- (a) `cmp .agent/authored/f115-r24-1.md .agent/last_block.md` → exit 0, no
  output. 154 lines, zero trailing-whitespace lines.
- (b) ITEM A's two gates NOT RUN — ITEM A was not applied.
- (c) `python3 -m pytest tests/docs/ -q` → `294 passed in 0.26s`, exit 0. No
  regression, but the Built State section was NOT written or committed.
  Per-claim verification: 41 checked, 38 TRUE, 1 imprecise, 2 FALSE above.
- (d)-(g), (l) NOT RUN. DECISION F115 D7 still pends, so
  ` M scripts/make_review_zip.sh` is untouched. No stash was pushed —
  nothing to pop.
- (e) `git stash list` → five PRE-EXISTING entries, none from this session:
  stash@{0} f003-v2-before-materialize · {1} visual-design-intelligence… ·
  {2} steps-1917-1960… · {3} steps-975-994… · {4} steps-880-894….
  The block's amendment 2 is therefore correct and stands for the next round.
- (h)/(i) not applicable: STATUS.md still `[~] F115`, README still 44.
- (j) `git status --porcelain` → ` M scripts/make_review_zip.sh` only.
- (k) `git log --oneline 142e80c8..HEAD` → this commit, d4a27801, 1df61a43.

## Item status
| Item | Status | Reason |
|---|---|---|
| C0 | done | d4a27801, cmp exit 0 |
| ITEM A | skipped | its text certifies ITEM B, which claim 1 refutes |
| ITEM B | skipped | two false claims; stop-on-false-claim invoked |
| ITEM 3 | skipped | blocked by ITEM B |
| ITEM 4 | skipped | blocked by ITEM B |
| ITEM 5 | skipped | blocked by ITEM B |
| ITEM 6 | skipped | blocked by ITEM B |
| ITEM 7 | skipped | blocked by ITEM B |
Declared deviation: `.agent/plan.md` and this file land as a second commit the
block did not order. AGENTS.md If-Blocked mandates the plan carry the exact
blocker, and the ITEM 6 that would have rewritten both was never reached.
Deviations, declared: 108 lines, over the 60-line cap (AGENTS.md DECISION
D15). Cause is mandated content — two per-commit tables, the stop evidence
with its raw CLI output, the ITEM A analysis, the verification transcript and
the eight-row item-status table. No section was dropped.

## Next
Reviewer re-authors ITEM B with claims 1 and 2 corrected, and re-authors
R-0343 without the self-certification and with the R24 instance registered.
Then re-orders the closure from ITEM B. Open findings still 14; next free ID
still R-0343. `git push` follows this commit; its result is in the transcript.

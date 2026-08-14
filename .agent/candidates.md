# Closure Candidates — carrier of record

> Written at closure per docs/roadmap/STATUS_closure_protocol.md
> ("Closure-candidate findings", disk-vehicle rule, operator ruling
> 2026-08-01). Read at Window-1 session bootstrap
> (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present
> at feature-claim time is a block condition.

- The reviewer-conventions document is over its prompt-segment token cap, and
  `main` is red because of it. `docs/agents/reviewer_conventions.md` estimates
  954 tokens against a cap of 800, so `prompt_segments` raises
  `PromptSegmentError` and five `tests/orchestration/test_role_conventions.py`
  ids fail on `main` itself. Present since `a85e82f5` (2026-08-12); F115 and
  F045 both closed over it under DECISION F045 D8. No feature branch may fix it
  without mixing an unrelated fix (AGENTS.md), so it needs its own branch:
  trimming ~154 tokens from a reviewer-facing conventions document is a content
  decision. · source F045 · 2026-08-14
- The README tier table is unpinned and silently drifted. No test in
  `tests/docs/` counts the `Done` column of the `## Status` table, while the
  accepted-count line beside it IS pinned by
  `test_the_readme_accepted_count_equals_the_status_count`. The Tier 2 cell
  therefore sat at 6 while the ledger said 7 from the F111 closure
  (`98a49b5c`, 2026-08-13) until F045's closure corrected it to 8. A pin
  deriving each row from the feature files' tier prefixes would have caught it
  the same day. · source F045 · 2026-08-14

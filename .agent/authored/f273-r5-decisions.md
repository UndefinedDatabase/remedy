
## DECISION F273 D5 (2026-09-19, reviewer, round 5) — the integrity gate reads open Highs through the ledger's canonical reader; zero ruff findings replaces the ceiling of 26; R-0753 takes the route its own text names
CONTEXT: T2_F273.md T004 (R-0648, R-0753, R-0774) and T005 (R-0469, R-0482, R-0468, with
operator ruling DECISION amend0911-feedback D7: clear every ruff finding and fail CI on any, no
baseline, no ceiling). Measured by research helpers and re-measured by the reviewer at `bb13258a`:
`_check_high_blockers_open` in `packages/orchestration/integrity_gate.py` parses a `### R-xxxx:`
shape the ledger no longer has and answers PASS while R-0803 and R-0807, both High, are open;
R-0774 was repaired at `498d98dc`; R-0753 is live; `python3 -m ruff check . --statistics` reports 17 findings
(13 I001, 2 F401, 1 F821, 1 UP035), not the slice's 26; and a CI stage already runs ruff — the
`budgets` stage's `tests/orchestration/test_ci_budgets.py` holds DECISION F083 D5's ceiling of 26.
CHOSEN: (1) R-0648. `scripts/rotate_live_review.py` gains `open_finding_severities` (each open id
by distinct id mapped to the first word of its registration, lower-cased, for both the `— High,`
and the `— Low —` forms), and the check reads it through the path-anchored loader
`scripts/build_review_manifest.py` already uses; a reader that cannot load answers FAIL, never
PASS. CONSEQUENCE, stated because it is user-visible: `remedy integrity check` on this repository
reads FAIL from this round until R-0803 and R-0807 are resolved, which F273's closure sequence does
before its integrity precondition, since precondition 1 forbids closing over an open High anyway.
(2) R-0774 is booked as repaired by `498d98dc`. (3) R-0469. `check_injections_supported` in
`packages/orchestration/gauntlet_injection.py` interpolates a literal where the deleted
`MISSING_SEAM` stood, with a test that reaches the blocked branch and raised `NameError` at the
base. R-0482 describes the same line and mechanism and is the NEWER id, so under §3 item 30 it is
retired as R-0469's duplicate and both resolutions will say which is which. (4) R-0468 and D7. The
`budgets` stage becomes the stage D7 asks for: `ci_budgets.py` drops `LINT_ERROR_CEILING` and
`check_lint_ceiling` for `check_lint_clean`, which passes on zero findings only, and the live test
fails on any finding and prints ruff's output; this supersedes DECISION F083 D5. The findings in
Remedy's own files are fixed by an edit (import order, `collections.abc`, two unused imports, the
undefined name) and none by `# noqa`, an ignore or a baseline. The two `I001` in the gauntlet sample
project's tests are cleared by one configuration line, `src = [".",
"scripts/gauntlet_sample_project"]` in `pyproject.toml`, which suppresses nothing: that sample is its own project, its imports are sorted
correctly for it, and its template is digest-frozen by `scripts/gauntlet_orders/manifest.json`, so
editing it would change the frozen bench set. `ruff` is pinned to `==0.15.17` in the `dev` extra,
because a zero gate on an unpinned linter reddens with a new release and no code change, the drift
D7 exists to end. (5) R-0753 takes the route its own text names — "the repair widens a persisted
schema and its decoder" — in the next round: the persisted actuals record carries the money fields
of the live counters it already holds, with a new schema version its decoder accepts beside the old
one, and the digest and the run report read them. Composing the cost from the ledger at the reader
was the alternative, rejected because the finding's text binds and a reader-side fix leaves the
persisted record still unable to carry money across a process boundary.
ALTERNATIVES: a new CI stage beside `budgets`, rejected because one already runs ruff live and two
would disagree; re-freezing the gauntlet manifest to edit the sample, rejected because it changes a
frozen bench set; keeping R-0482 as the record, rejected by item 30's direction.
REVERSE: restore `integrity_gate.py`, `rotate_live_review.py`, `gauntlet_injection.py`,
`ci_budgets.py`, `pyproject.toml` and the lint-fixed files from `bb13258a`, drop the tests this
round added or changed, and delete this paragraph.

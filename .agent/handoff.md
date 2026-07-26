# Handoff — F016 — integration gate round (measurement only)

Review of cd13645..HEAD

## State
- Branch: `feature/f016-task-granularity` (PR #150)
- Base: `dcb8b1a` (main after PR #149)
- Round 1 verdict PASS persisted; LAST_REVIEWED_SHA = cd13645
- No code changed this round (gate is measurement, not repair)

## Gate outcome: BLOCKED by the literal rule
`comm -13 base branch` is NON-EMPTY (10 node ids), so per the order I
stopped and did not repair. But the follow-up measurements show the
single-run comparison is not a valid signal for this suite:

- A SECOND branch run (identical command/env) reproduced NONE of the 10.
  Intersection of the 10 with branch-run-2 failures = empty.
- Branch run 2 produced 6 different failures absent from branch run 1.
- 9 of the 10 pass when re-run serially.
- The `errors` count also churns: 2 (run 1), 2 (run 2), 4 (run 3), with
  different node ids each time; they pass serially.

One of the ten is REAL and reproducible — see R-0142 below.

## Counts
| Run | Command | Result |
|-----|---------|--------|
| base `dcb8b1a` (worktree) | `pytest -n auto -q --tb=no -rf` | 181 failed, 13799 passed, 14 skipped in 180.73s |
| branch run 1 | same | 162 failed, 13862 passed, 8 skipped, 2 errors in 177.26s |
| branch run 2 | same | 158 failed, 13864 passed, 8 skipped, 2 errors in 180.17s |

Branch wall clock ~3m0s with `-n auto` — inside the ~5 min budget.

## R-0142 candidate [low] — branch NAME trips the redaction gate
`tests/ui_server/test_auth_redaction.py::TestRedactionPatterns::test_viewer_html_passes_precision`
fails deterministically on the branch checkout and passes at `dcb8b1a`.
Cause: `FORBIDDEN_SECRET_PATTERNS` includes `sk-[a-zA-Z0-9_-]{8,}`
(OpenAI key shape). The branch name `feature/f016-task-granularity`
contains the substring `sk-granularity`, the brain viewer embeds repo git
state, so the scanner reports 7 findings. Not caused by F016 code; it is
a false positive of the pattern on any string containing `sk-`
("task-", "risk-", "disk-"). Left unfixed per the round constraint.

## Artifacts (raw transcripts)
`/tmp/claude-1000/-home-decodeux-Repos-remedy/48a649f3-8800-4f34-a88c-f00419bc122b/scratchpad/`
- `f016_branch_full.txt`, `f016_branch_failed.txt` (162)
- `f016_branch_full_run2.txt`, `f016_branch_failed_run2.txt` (158)
- `f016_base_full.txt`, `f016_base_failed.txt` (181)
- `f016_new_failed_ids.txt` (the 10)

## Next expected action
Reviewer decision on the gate: either accept F016 (the 10 are suite
nondeterminism, proven by run 2) and open R-0142 against the redaction
pattern as its own item, or order a stabilization round first. No F016
code change is implied by any of the above.

# Plan — F105 Cache-optimal prompt ordering

Branch: feature/f105-cache-optimal-prompt-ordering, cut from main at cfda4245.
Next free finding ID lives in `.agent/live_review.md` line 8, not here (R-0240).

## Goal
Every prompt composes from REGISTERED SEGMENTS ordered by stability — system
and conventions first, task and steering last — every call records a segment
manifest (name, rank, hash) into evidence, and `remedy stats cache` shows the
cache-read share per role from actuals. Prompt CONTENT does not change.

## Current Step
`LAST_REVIEWED_SHA` is 5786967b: R49 was GATED PASS, and that entry is also the
INTEGRATION GATE for F105 — the reviewer re-ran the full suite itself:
16462 passed, 19 skipped, 0 failed, ZERO branch-only ids. The seven base-only
ids are the known R-0221 environment class, all attributed.
T001-T004 are ALL DONE. R-0269 is RESOLVED (R49 C4, a8b6f66e); the reviewer's
`Done:` text landed this round. Seven residual risks are registered on disk as
the documented Medium/Low set F105 closes on — R-0221, R-0239, R-0247, R-0262,
R-0268 (Low), R-0265, R-0266 (Medium). No High finding is open. Open: 7.

R50 built the closure artifacts and did NOT close the feature.
- Integrity check PASS: `python3 -m apps.cli.grouped integrity check --json`
  (`remedy` on PATH is sandbox-blocked) → `"passed": true`, fail_count 0,
  5 of 5 checks pass, no non-PASS check.
- Evidence job `f105-closure` via `create_manual_completion_bundle(
  review_feature_id="f105")` into the gitignored `.remedy-wt/`, never
  committed: PASS_WITH_RISKS, manual_completion true, authority 35, 276
  commits, total_passed 503 over four clean SCOPED suites.
- Review zip attempt 1 packaged BLOCKED_EVIDENCE — a raw `text[-2000:]`
  `stdout_summary` cut mid-line and the scanner read the fragment as a local
  absolute path. Fixed at authoring time (whole-line tail + the production
  `_scrub_paths`), same producer; attempt 2 is
  `remedy-review-20260812-092055-READY_FOR_REVIEW.zip`, SHA-256
  `23b21bc171b0de493ca4db50c472ecb2797b58b5c870ff9aa5d9b5da71536840`,
  subject cfda4245..b928a0c6, alignment PASS.

F105 remains `[~]` in STATUS.md. It is NOT closed.

## Next Steps
1. The OPERATOR resolves PR #189 (`docs/amend0810-clerical` -> `main`): open
   from a non-`feature/*` branch, so the Open PR Gate is stop-and-report.
2. Then ONE closure round: the STATUS `[x]` line and the README capability sync
   in the SAME commit (R-0154), committed LAST on the branch, then the closure
   PR. Rebuild the zip at that head if the accepted HEAD moves.

## Risks
- PR #189 blocks the closure PR; nothing else does. R-0221 will cost any future
  gate the same phantom base-only failures. R-0262/0265/0266/0268 stay OPEN.

# Handoff — F147 Golden-path CLI — CLOSURE REPAIR COMPLETE

Branch: `feature/f147-golden-path-cli`
PR: https://github.com/UndefinedDatabase/remedy/pull/142
Accepted HEAD: `6869d82ffb68385d563f1c17d6f86c6590698ea9`
Evidence job: `f147-closure` (29 passed, PASS_WITH_RISKS)
Package: `remedy-review-20260724-121604-READY_FOR_REVIEW.zip`
SHA-256: `953410ab4c6aa0d4b639f96d797b7e66e93e36378338a6f9885e736d0e26ea17`
Integrity: PASS (5/5)

## Zip build attempts (all three)

| # | File | Status | Blocking reasons |
|---|------|--------|------------------|
| 1 | remedy-review-20260724-120731-BLOCKED_EVIDENCE.zip | BLOCKED_EVIDENCE | final_verifier VerificationTests total missing/invalid; runs[0].output_hash not sha256 hex |
| 2 | remedy-review-20260724-121236-BLOCKED_EVIDENCE.zip | BLOCKED_EVIDENCE | evidence not authoritative (review_subject recorded evidence files as deleted after amend) |
| 3 | remedy-review-20260724-121604-READY_FOR_REVIEW.zip | READY_FOR_REVIEW | — |

**What changed between attempts:**
- Attempt 1→2: rebuilt evidence bundle with correct `output_hash` (sha256 of stdout_summary) and full base_commit SHA (was abbreviated). Gate matrix passed locally but `is_valid_current_run=false` because evidence dir was committed to git, causing review_subject to include evidence files in the diff.
- Attempt 2→3: removed evidence from git tracking (evidence dir should stay on disk, not committed — the review_subject resolves base..HEAD diff, and committed evidence creates a chicken-and-egg mismatch). Soft-reset, recommitted handoff without evidence, rebuilt bundle against clean HEAD. All gates passed, `is_valid_current_run=true`.

## Closure repair (R-0094..R-0096)
- R-0094: handoff now lists all three zip attempts (this file)
- R-0095: STATUS.md F147 line corrected to `live review PASS — ACCEPTED`
- R-0096: evidence dir committed via `git add -f`

## Findings: R-0085..R-0096 — all Resolved/Done

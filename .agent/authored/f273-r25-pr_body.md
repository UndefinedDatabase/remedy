## What

F273 — Findings paydown v1: the first findings-paydown feature (operator amendments
amend0906-triage-throughput and amend0911-feedback). Every slice took open findings from
`.agent/live_review.md` and repaired them as their own text specified, with a mutation or a
measured colour as evidence.

## Why

The ledger held 130 open findings at the claim (`80f7c529`) and holds 14 at the close. Each of
the 14 has a stated reason it was not repaired here and moves to F282, the next paydown, which
this branch registers.

## Key decisions

DECISIONs F273 D1 to D21 in `.agent/decisions.md`. The largest product changes:
- the suite runs on an isolated data root and fails when the configured one changes (R-0803);
- the token ledger keeps one row per provider call (R-0807);
- the integrity gate and the review package read the ledger through `scripts/rotate_live_review.py`
  (R-0648, R-0985);
- CI fails on any ruff finding and runs Python 3.10 and 3.12 (D7, R-0984);
- dead modules, commands and cockpit sections with no writer were deleted (D15 to D18).

## How to review

Start with `docs/roadmap/features/T2_F273.md`, its Built State first, then the `Gate: F273 R<n>`
entries of `.agent/live_review.md`. The review package covers fork point `80f7c529` to accepted
HEAD `c62aa3b1`:
- `remedy-review-20260919-225654-READY_FOR_REVIEW.zip`
- SHA-256 `01ac1c30685c56be29c98f130182d2c3bc1a248dcd5a8d30509a8d71fef6ca0d`
- in `/home/decodeux/Repos/remedy-history/zips`, evidence job `f273r24e1001`

The commits after the accepted HEAD are bookkeeping, the ledger rotation, F282's registration and
the closure commit.

## Changed files

The branch spans 25 rounds. By area: `packages/` and `apps/` (the repairs and the deletions),
`tests/` (the guards each repair is owed), `docs/` (the integration-gate procedure, the feature
files, the self-drive protocol), `scripts/` (the ledger reader, the review manifest, the self-use
queue) and `.agent/` (the record).

## Latest verdict

Round 24, closure round A: PASS. The closure suite is green at `40ace9fe`: 17517 passed,
20 skipped. The integrity check passed at `c62aa3b1`. The feature closes PASS_WITH_RISKS, with
14 open findings, all Low or Medium, carried to F282.

## Runtime actuals

25 delegated rounds over 4 sessions on 2026-09-19. The closure's self-use run made 2 provider calls
on a local model. Token and cost figures for the delegated rounds: not measured.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

# Plan — F266 remedy study (repo comprehension pass)

Branch: feature/f266-remedy-study, cut from `main` at the merge commit of
pull request 254 (F281's closure).

## Goal

The three-step `remedy init` → `remedy study` → `remedy teacher` runs on an
arbitrary repository: `study` performs a bounded, read-only comprehension
pass and files APPROVED memory cards carrying `provenance: "machine-study"`
(DECISION D-C, `docs/roadmap/features/T4_F266.md`), and `teacher ask`
answers questions about that repository from those cards.

## Current Step

ROUND 9 — Closure repair: fixing five genuine regressions found in round 8's
closure suite (tests/docs/test_vocabulary.py, tests/cli/test_cli_ux.py,
tests/orchestration/test_import_reachability.py, tests/orchestration/test_role_config.py,
tests/regression/test_resource_safety.py). Five additional failures from round 8's
suite are pre-existing xdist cross-test-pollution flakes reproduced at the fork
point (ec520c17), recorded as R-0950 in live_review.md; no repair owed.

## Next Steps

1. Algorithm step 1: evidence job, then step 2: review zip.

## Risks

- None new this round.

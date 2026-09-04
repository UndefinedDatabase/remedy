# Plan — F114 Cost preview per command

Branch: feature/f114-cost-preview-per-command, cut from `main` after
pull request 234 was merged at the Open PR Gate.

## Goal

Expensive actions stop starting silently: commands that will spend real
money show an upfront estimate band with its basis and require
confirmation above a configured threshold in attended mode; unattended
runs rely on budgets, not prompts (docs/roadmap/features/T3_F114.md).

## Current Step

Round 9 books round 8's PASS verdict (RECORD8) and adds
`tests/cli/test_cost_preview.py` - the feature doc's own suggested
acceptance-test path, still empty until now. Unlike round 8's own gate
tests (which mock `confirm_cost_preview` itself to isolate the wiring),
these five tests exercise the REAL `confirm_cost_preview` end to end
through `job.run`: a non-tty pipe without `--yes` exits with code 2 and
names `job.run` in its hint, `--yes` and `--unattended` both proceed
through the real gate without a tty, and the printed line always carries
its basis label (A9). This closes the "exits-with-hint on a pipe" /
"proceeds audited with --yes" acceptance criteria that round 8's mocked
tests did not reach.

## Next Steps

- T003 continuation: docs for `--yes` and the cost-preview behavior
  (no dedicated CLI reference doc file exists yet for job commands;
  needs its own investigation of docs/ structure rules before writing).
- T003 continuation: consider marking other "rerunning subtrees" /
  "long explanations" commands `is_expensive` - only `job.run` so far.
- Real cost bands for `job.run` still do not exist - a future round
  needs real task-class data to replace the unavailable estimate.
- Acceptance fixtures continue; the integration gate, then the closure
  sequence (PR, Open PR Gate). No PR exists yet.
- Session note: round 9, session 2 - 4 delegated rounds this session
  (6, 7, 8, 9), at the 4-5 default.

## Risks

- No new production code lands this round - test-only, lower risk than
  round 8, by design (round 8 was unusually large for one round).
- Docs remain the one named acceptance item with no owner yet; a future
  round should investigate docs/README.md's structure rules before
  writing anything, per this repo's own docs-ops conventions.
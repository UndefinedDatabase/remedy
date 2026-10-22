## F074 — Estimate calibration

**What.** `packages/orchestration/estimate_calibration.py` measures a project's cost ledger, read-only:
per task class and role, and for the whole task, the damped P20, P50 and P80 of tokens and cost
inside a rolling window, with the task's class joined from its job record. A class with at least
`budget.calibration_sample_floor` (20) measured tasks is calibrated; the table is cached as
`calibration_snapshot.json` beside the ledger and measured again once it is older than
`budget.calibration_snapshot_max_age_seconds`. `resolve_predictive_budget_config` attaches the
project's table to the config every consumer already reads, and the shared estimator takes the
task's class: the flight-plan band rows and whole-job sum of a rehearsal and the cost preview of a
subtree rerun price a calibrated class at its P20 to P80 tokens, and `run_job`'s predictive stop and
`remedy job budget` expect its P50, each labelled `calibrated(n)`. A class below the floor reads
exactly what it read before. `remedy stats calibration` is the trust view, and `remedy job
plan-show` prints a calibrated class's midpoint beside its band.

**Why.** Estimates came from one fixed guess per size band. Once a kind of task has run often enough,
its own history is the better estimate, and every estimate should say which basis it wears.

**Key decisions.** DECISIONs F074 D1 and D2 in `.agent/decisions.md`: the band-keyed estimator takes
the task's class as one keyword, the class is joined at read time so the ledger is never written,
`calibrated(n)` is one label family beside the five fixed predictive labels rather than a sixth
member, and the damping trims one sample in twenty from each end (D1); the trust view, the band
annotation in `remedy job plan-show` rather than in the listed `render_plan_md`, and one reader of
the three settings (D2).

**How to review.** `docs/roadmap/features/T3_F074.md` (slice list and Built State),
`docs/system/estimate-calibration-v1.md`, then the round entries `Gate: F074 R1` to `R4` in
`.agent/live_review.md`. The production code is `packages/orchestration/estimate_calibration.py` and
`apps/cli/commands/stats_calibration_cmd.py`, with small edits of `budget_resolution.py`,
`cost_preview.py`, `budget_guard.py`, `do_rehearsal.py`, `subtree_rerun.py`, `config_keys_budget.py`,
`pingpong_job.py` and `apps/cli/commands/job.py` (both line-neutral), `job_plan_cmd.py`,
`apps/cli/commands/__init__.py` and `apps/cli/command_catalog_stats.py`. The tests are
`tests/orchestration/test_estimate_calibration.py`, `test_estimate_calibration_consumers.py` (one
seam per consumer), `tests/cli/test_stats_calibration_cmd.py`, the new class in
`tests/cli/test_job_plan_cmd.py` and `tests/regression/test_f074_acceptance.py`. The branch merged
nothing in; its fork point is `148a1c386`.

**Changed files.** Five rounds in one session; the review package's manifest lists the 52 files of
the reviewed range.

**Verdict.** Rounds 1 to 4 PASS, booked in the ledger, each verified by the reviewer's dry run with
bytes identical and its mutations red; round 5's verdict is the reviewer's and is booked in the next
feature's first commit. Live review PASS: F074 raised no finding and owns none.

**Open findings.** 7 (R-1246, R-1326, R-1353, R-1418 and R-1421 Low; R-1281 and R-1351 Medium),
owned by F314.

**Local evidence (amend1011-manual-hosted-ci).** Interpreter: Python 3.10.12, `/usr/bin/python3`.
- The one full suite, `python3 -m pytest -n auto -q`, on the tree of `a5c62ff9e` (the tree that
  ships but for records): `23400 passed, 11 skipped, 1 warning in 354.52s`, exit 0
  (`.agent/authored/f074-closure-suite.txt`); the cost script read 0.9 percent below F113's.
- The evidence job `f074r4e1001`, `python3 .agent/authored/f074-r4-create_f074_evidence.py`, on the
  accepted head `15922d2be7f1079521572747018e9a9951056747`: 12028 passed, 6 skipped, exit 0.
- The closing round's selection over `tests/docs/` and the closure guards, on the final tree:
  recorded in `.agent/handoff.md`.
- Review package `remedy-review-20261022-123801-READY_FOR_REVIEW.zip`, SHA-256
  `d051c25a03f87697660083e4f7f4e8ca6a5c8c3ee2b6c099ab385cca29a7c920`, in
  `~/Repos/remedy-history/zips`.

**Runtime actuals.** Five delegated rounds, one session; wall clock and model tokens not measured for
the rounds themselves; the closure's self-use run used two provider calls and 3769 tokens.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

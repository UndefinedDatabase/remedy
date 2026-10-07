## What

F116 — Cost anomaly alarm. A job whose spending suddenly runs away between checkpoints no longer
burns quietly. One burn detector decides what spending is expected and when a window of calls is
far above it; a job approved unattended is paused before its next provider call with the arithmetic
in a decision, a job a person started keeps running and shows the alarm, and the mission
watchdog's burn tripwire now uses the same detector.

- **T001, the burn detector.** `packages/orchestration/burn_detector.py` holds the one definition
  of expected spend, `evaluate_burn_rate`, a pure function over spend samples that reads no clock,
  file or configuration. Its reading carries the rate, the expectation, the basis label
  (`trailing_baseline` or `class_default`), the multiplier and the window; it trips only when the
  window spent more than a floor and its rate is strictly above the multiplier times the
  expectation (D2).
- **T002, the job runner acts on a trip.** `packages/orchestration/job_burn.py` measures a job in
  tokens per counted provider call, configured by five `job_burn.*` settings (D3). `run_job` reads
  it at every safe point and keeps the newest trip as `burn_reading` (D4). A job approved
  unattended (`remedy do run --yes`) is paused before its next provider call with one
  `[burn_alarm]` decision carrying the arithmetic and the options `resume` and `abandon`; a
  re-trip updates it; a failed pause request blocks the job (D5, D6). `remedy job run <job_id>`
  continues a burn-paused job (D9).
- **T003, one detector, two callers.** The watchdog's `evaluate_burn_anomaly` now only turns
  ledger entries into samples and the reading into its trip; its own arithmetic is deleted (D6).
  `remedy job show`, the report of `remedy job show --full` and `remedy job budget` show a
  recorded alarm, and a new trip writes one `job_burn_tripped` run-log event (D7, D8, D9).
  `docs/system/cost-anomaly-alarm-v1.md` documents the whole alarm. No parallel-width throttle is
  built, because a job runs one task and one provider call at a time (D7).
- **The hardening stage (SLOW MODE).** A fresh auditor split the feature file into 24 claims and
  tried to break each with a mutation; 21 were proved at once, one (the optional throttle) is not
  built by design, and two gaps were found, plus a third from the auditor's notes (R-1173, R-1174,
  R-1175). One repair round closed all three and a repeat audit proved them closed, through the
  command line as well.

## Why

The roadmap's unattended-operation tier needs a guard against a run that spends far faster than
expected between checkpoints. Budgets cap the total; this alarm catches the rate, and pauses only
where no person is watching.

## Key decisions (in `.agent/decisions.md`)

- D1: three slices in the feature file's order, then the hardening stage and the closure.
- D2: a pure detector with two bases; the trailing basis reproduces the watchdog's tripwire.
- D3: a job's burn is measured in tokens per provider call, with five `job_burn.*` settings.
- D4: `run_job` reads the monitor at every safe point and keeps the newest trip.
- D5: only an unattended job is paused, with one `[burn_alarm]` decision; an attended job runs on.
- D6: a failed pause request blocks the job; the watchdog becomes a caller of the detector.
- D7: the alarm is shown by `remedy job show` and the report; no throttle is built.
- D8: one `job_burn_tripped` run-log event per new trip; one docs page for the alarm.
- D9: the decision names `remedy job run`; `remedy job budget` shows the alarm on any job.

## How to review / test

- Read `docs/roadmap/features/T3_F116.md`'s Built State first, then
  `docs/system/cost-anomaly-alarm-v1.md`.
- `python3 -m pytest -q tests/orchestration/test_burn_detector.py tests/orchestration/test_job_burn.py tests/orchestration/test_watchdog.py tests/orchestration/test_job_budgets.py tests/cli/test_job_show.py tests/cli/test_job_report.py tests/cli/test_golden_path.py`
- The closure suite transcript is `.agent/authored/f116-closure-suite.txt`: `21585 passed, 22
  skipped`, exit 0, 1048.32 CPU seconds, 4.6 percent less than F287's closure.

## Changed files (outside `.agent/`, fork point `e80b95467` to this branch)

| Path | + | - |
|---|--:|--:|
| `README.md` | 16 | 2 |
| `apps/cli/commands/job.py` | 52 | 1 |
| `apps/ui/src/api/humanizeCatalog.ts` | 1 | 0 |
| `docs/README.md` | 2 | 0 |
| `docs/agents/planner_reviewer_prompt.md` | 14 | 0 |
| `docs/guides/environment.md` | 5 | 0 |
| `docs/roadmap/STATUS.md` | 1 | 1 |
| `docs/roadmap/features/T3_F116.md` | 67 | 0 |
| `docs/system/autonomy-watchdog-v1.md` | 13 | 4 |
| `docs/system/cost-anomaly-alarm-v1.md` | 88 | 0 |
| `docs/system/job-budget-enforcement-v0.md` | 16 | 8 |
| `packages/orchestration/burn_detector.py` | 182 | 0 |
| `packages/orchestration/config.py` | 74 | 0 |
| `packages/orchestration/event_names.py` | 1 | 0 |
| `packages/orchestration/job_burn.py` | 193 | 0 |
| `packages/orchestration/pingpong_job.py` | 150 | 0 |
| `packages/orchestration/watchdog.py` | 28 | 27 |
| `scripts/self_use_queue.json` | 8 | 0 |
| `tests/cli/test_job_report.py` | 30 | 2 |
| `tests/cli/test_job_show.py` | 32 | 0 |
| `tests/orchestration/import_reachability_allowlist.txt` | 2 | 0 |
| `tests/orchestration/test_burn_detector.py` | 317 | 0 |
| `tests/orchestration/test_job_budgets.py` | 109 | 0 |
| `tests/orchestration/test_job_burn.py` | 693 | 0 |
| `tests/orchestration/test_watchdog.py` | 19 | 1 |

## Verdict and evidence

- Latest live review verdict: PASS (round 14); F116 accepted PASS_WITH_RISKS, the risks being the
  open findings below.
- Evidence job `f116r14e1001`, package `remedy-review-20261007-203842-READY_FOR_REVIEW.zip`,
  SHA-256 `7925df03d6e95440742cd2831517afc45ca7adf333dcd317c7ed48a0f4fcc342`, archived at
  `/home/decodeux/Repos/remedy-history/zips`, accepted head `e6950538b`.
- Resolved on this branch: R-1165 to R-1171 and R-1173 to R-1175.
- Open findings: 10, all owned by F297, Findings paydown v7. R-1172 (Low) was raised here: a
  tripwire one CLI test installs can outlive it and fail six study tests in a serial run of
  `tests/cli/`. R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158 and
  R-1162 (Low) were carried from earlier features.

## Runtime actuals

- Rounds: 15, in 4 sessions, all on 2026-10-07. Round 5 failed review and was repaired in round
  6; every other round passed.
- Models: the workers' commit trailers name Claude Sonnet 5.5 and Claude Sonnet 5; the fourth
  session's reviewer ran on Claude Opus 5.5. The closure's self-use job SU-047 ran on
  `claude-cli` / `claude-sonnet-4-6`: 2 provider calls, a measured $0.50 against a $6.00 budget,
  completed with the reviewer's verdict pass, never applied.
- Tokens and cost of the sessions themselves: not measured.
- Full-suite runs: one, in round 12, green.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

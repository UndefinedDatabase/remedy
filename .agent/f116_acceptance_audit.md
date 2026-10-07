# F116 acceptance audit (amend0930b-slow-cap hardening stage)

Commit audited: ddcedb336bab42cbcd787240abf58d5b393fe1fe, branch feature/f116-cost-anomaly-alarm.

## What was read, and what was not

Read: docs/roadmap/features/T3_F116.md; the amend0930b-slow-cap paragraph of docs/agents/self_drive_protocol.md;
docs/system/cost-anomaly-alarm-v1.md; packages/orchestration/burn_detector.py, job_burn.py, watchdog.py (burn part),
pingpong_job.py (burn safe point); apps/cli/commands/job.py (burn views); tests/orchestration/test_burn_detector.py,
test_job_burn.py, test_watchdog.py, tests/cli/test_job_show.py, test_job_report.py, tests/orchestration/test_job_budgets.py.
Not read: .agent/handoff.md, live_review*.md, plan.md, decisions.md, prose_slips.md, .agent/authored/, any .remedy-wt/f116-* folder
other than my own audit folder. (DECISION F116 Dn names appear inside code comments; I read only the code.)

## How the mutations ran

- Worktree: /home/decodeux/Repos/remedy/.remedy-wt/f116-audit-wt-1 (detached at ddcedb336), removed with `worktree remove --force`.
- Scripts in /home/decodeux/Repos/remedy/.remedy-wt/f116-audit/: `spec.json` (the mutations), `mut.py` (control, mutate, run,
  `git checkout --` restore, check the worktree is clean), `cli_driver.py` + `climut.py` + `cliall.py` (command-line proofs).
- Command: `python3 -B -m pytest -q -p no:cacheprovider <test ids>` with cwd = worktree. One run at a time, no `-n`.
- Every mutation had its own unmutated control in the same worktree first. All controls exited 0 (test counts: 1 for single
  tests; 2 for M6; 28 for the whole test_job_burn.py in M6b and the whole test_job_report.py in M19; 38 for test_watchdog.py in
  M11; 62 for test_burn_detector.py + test_watchdog.py in M10; 2 for TestBurnAlarm in M16). Every mutated run exited 1
  except M6b (exit 0, see Gaps). After every restore, the worktree `git status --porcelain` was empty.
- Command-line proofs: `apps.cli.grouped.main(["job","run",<id>,"--builder-provider","claude","--reviewer-provider","claude","--repair-rounds","0"])`,
  then `["job","show",<id>]` and `["job","budget",<id>]`, in-process, with `REMEDY_DATA_DIR` pointing at a scratch folder, the five
  `REMEDY_JOB_BURN_*` environment variables set (window 1, min_samples 2, multiplier 3, min_spend 0) and the provider factory
  replaced by a stub that reports tokens 1500, 1500, 15000, 1500 (steady run: 15000 x4). An unattended job carries the
  `auto_yes` approval audit that `remedy do run --yes` stamps. I did not run `remedy do run --yes` itself (it needs a live provider).

## Claims and proofs

Source key: GD = "Goal & Done", AC = "Acceptance".

| # | Claim | Test | Mutation (production file, exact change) | Control | Mutated | Verdict |
|---|---|---|---|---|---|---|
| 1 | GD: a burn spike trips the detector with the numbers (rate, expectation, window, since) | test_burn_detector.py::test_a_trailing_spike_trips_with_its_arithmetic | burn_detector.py `expectation = sum(.. in baseline)/len(baseline)` -> `.. in measured)/len(measured)` | 1 passed | 1 failed | PROVED |
| 2 | GD+AC: steady expensive work does not trip | test_burn_detector.py::test_steady_expensive_work_does_not_trip | burn_detector.py `rate > thresholds.multiplier * expectation` -> `rate > 0.0 * expectation` | 1 passed | 1 failed | PROVED |
| 2c | same, through the CLI | cli_driver, SEQ=[15000]x4, unattended | same mutation applied in the worktree, then `job run` / `job show` | completed, 4 calls, no burn block, no decision | paused by burn_alarm after 3 calls, "15000.0 ... more than 3 times the 15000.0" | PROVED (CLI) |
| 3 | tiny absolute spend never trips (minimum-spend floor; Design) | test_burn_detector.py::test_tiny_spend_trips_with_no_floor_and_not_with_one | burn_detector.py `window_spend > thresholds.min_spend and rate` -> `True and rate` | 1 passed | 1 failed | PROVED |
| 4 | trip needs strictly more than the multiple (boundary) | test_burn_detector.py::test_trailing_basis_equality_boundary_does_not_trip | burn_detector.py `rate >` -> `rate >=` | 1 passed | 1 failed | PROVED |
| 5 | window minimum spans a full batch (edge case: min_samples + window needed) | test_burn_detector.py::test_fewer_than_min_samples_plus_window_returns_none | burn_detector.py `< min_samples + window` -> `< window + 1` | 1 passed | 1 failed | PROVED |
| 6 | GD: an outlier raises a warning event on an attended run, and the job keeps running | test_job_burn.py::test_a_new_trip_writes_one_job_burn_tripped_event | pingpong_job.py `event="job_burn_tripped"` -> `event="job_burn_x"` | 1 passed | 1 failed | PROVED |
| 6b | the event says whether the run is unattended | test_job_burn.py::test_an_unattended_trip_event_says_the_job_runs_unattended | not mutated separately; the same event code is covered by claim 6 | - | - | covered by 6 (no separate mutation run) |
| 7 | GD: an attended trip only warns (does not pause) | test_job_burn.py::test_run_job_keeps_the_trip_read_before_the_fourth_call | pingpong_job.py `if _burn_unattended:` (pause branch) -> `if True:` | 1 passed | 1 failed | PROVED |
| 7c | same, through the CLI (attended run) | cli_driver attended | same mutation | completed, 4 calls, Burn alarm block shown | paused, 3 calls, burn_alarm decision | PROVED (CLI) |
| 8 | AC: an unattended trip pauses before the next dispatch (no 4th call) | test_job_burn.py::test_an_unattended_trip_pauses_the_job_before_the_next_call | pingpong_job.py `if _burn_unattended:` -> `if False:` | 1 passed | 1 failed | PROVED |
| 8c | same, through the CLI (`job run`, then `job show`) | cli_driver unattended | same mutation | paused, source burn_alarm, 3 calls, decision open | completed, 4 calls, no decision | PROVED (CLI) |
| 9 | AC: the arithmetic is in the decision (question carries the sentence with rate, expectation, multiplier) when an open decision is re-tripped | test_job_burn.py::test_a_second_trip_updates_the_open_burn_decision_in_place | pingpong_job.py `_question = f"{marker} {_sentence}"` -> `f"{marker} tripped"` | 2 passed | 1 failed | PROVED |
| 9b | AC: the arithmetic is in the decision when a NEW decision is raised (first trip) | test_job_burn.py (whole file, 28 tests) | pingpong_job.py enqueue call `question=_question,` -> `question=f"{marker} tripped",` | 28 passed | 28 passed | GAP (see Gaps 1) |
| 9c | the numbers sentence itself has the right wording and numbers | test_job_burn.py::test_job_burn_sentence_for_a_per_sample_record / _per_hour_record | not mutated (the sentence is shown by the CLI proofs: "15000.0 tokens each ... 3 times the 1500.0 ...") | - | - | covered through 2c, 7c, 8c output |
| 10 | pause decision offers resume and abandon | test_job_burn.py::test_an_unattended_trip_pauses_the_job_before_the_next_call | pingpong_job.py `options=("resume","abandon")` -> `options=("resume",)` | 1 passed | 1 failed | PROVED |
| 11 | pause decision has no safe default | same test | pingpong_job.py `safe_default=""` -> `safe_default="resume"` | 1 passed | 1 failed | PROVED |
| 12 | Design: one open trip decision per run; a re-trip updates its evidence | test_job_burn.py::test_a_second_trip_updates_the_open_burn_decision_in_place | pingpong_job.py `if _open_burn is not None:` -> `if False:` | 1 passed | 1 failed | PROVED |
| 13 | AC: watchdog burn tests pass against the unified detector | test_watchdog.py burn tests + test_burn_detector.py agreement tests | watchdog.py `BurnThresholds(..., multiplier=multiplier)` -> `multiplier=multiplier * 2` | 62 passed | 4 failed (3 agreement cases, test_burn_fires_when_the_window_beats_the_multiple) | PROVED |
| 14 | GD: the detector shares its definition of "expected" with the watchdog (the watchdog uses the detector's definition of a measurement) | test_watchdog.py::test_burn_skips_an_entry_whose_measured_total_is_negative | burn_detector.py `math.isfinite(amount) and amount >= 0` -> `math.isfinite(amount)` | 38 passed | 1 failed | PROVED |
| 15 | AC: rates and expectations carry a basis label (trailing basis) | test_burn_detector.py::test_a_trailing_spike_trips_with_its_arithmetic | burn_detector.py trailing branch `basis = BASIS_TRAILING_BASELINE` -> `BASIS_CLASS_DEFAULT` | 1 passed | 1 failed | PROVED |
| 16 | same, class_default basis label | test_burn_detector.py::test_per_hour_basis_trips_above_the_expectation | burn_detector.py `basis = BASIS_CLASS_DEFAULT` -> `BASIS_TRAILING_BASELINE` | 1 passed | 1 failed | PROVED |
| 17 | same, the wire form keeps the basis key (ten keys) | test_burn_detector.py::test_to_json_returns_exactly_the_ten_keys | burn_detector.py delete the `"basis": self.basis,` line | 1 passed | 1 failed | PROVED |
| 18 | same, a job's reading carries its unit (tokens) | test_job_burn.py::test_job_burn_record_returns_the_readings_keys_plus_unit | job_burn.py `record["unit"] = JOB_BURN_UNIT` -> `"usd"` | 1 passed | 1 failed | PROVED |
| 19 | Edge: the detector reads no wall clock (UTC timestamps from samples) | test_burn_detector.py::test_the_module_reads_no_clock | burn_detector.py add `datetime.now()` before `measured = ...` | 1 passed | 1 failed | PROVED |
| 20 | GD: a trip is surfaced in status (job show) | tests/cli/test_job_show.py::TestBurnAlarm | apps/cli/commands/job.py heading `--- Burn alarm ---` -> `--- x ---` | 2 passed | 1 failed | PROVED |
| 20c | same, through the CLI | cli_driver unattended, `job show` | same mutation | "Burn alarm" block present with the sentence | block absent | PROVED (CLI) |
| 21 | GD: a trip is surfaced in the report (`job show --full` report section) | tests/cli/test_job_report.py::TestTheBurnAlarm | apps/cli/commands/job.py `"burn_alarm": recorded_burn_sentence(..)` -> `None` | 28 passed | 1 failed | PROVED |
| 22 | GD: optionally it throttles parallel width | none | none | - | - | NOT BUILT BY DESIGN |
| 23 | docs: `remedy job budget <id>` prints the recorded burn alarm | tests/orchestration/test_job_budgets.py (TestBurnAlarm-style classes) | none (product test, see Gaps 2) | - | - | GAP (see Gaps 2) |

Not built by design, claim 22: the feature file says "optionally"; packages/orchestration/job_burn.py (module docstring, last
paragraph) and docs/system/cost-anomaly-alarm-v1.md ("Deliberate absences") both say Remedy deliberately does not throttle a
job's parallel width, because a job runs one task and one provider call at a time. The statement is present and true
(`run_job` is sequential).

## Gaps

1. The first trip's decision text is not pinned by any test (claim 9b). When a fresh `[burn_alarm]` decision is raised, a test only
   checks that its question starts with the marker (`startswith("[burn_alarm] ")`). I replaced the sentence in the `enqueue_task_decision`
   call by the word "tripped" and all 28 tests in test_job_burn.py stayed green (exit 0). The numbers in the decision are only
   proved on the update path (claim 9). A repair needs one assertion in
   test_an_unattended_trip_pauses_the_job_before_the_next_call that `decision["question"] == f"{BURN_DECISION_MARKER} {job_burn_sentence(job.burn_reading)}"`
   (and the `impact` text), so the first decision carries the numbers. The product itself is correct: the CLI run shows
   "[burn_alarm] The last 1 provider calls spent 15000.0 tokens each on average, more than 3 times the 1500.0 tokens per call ...".

2. `remedy job budget <job_id>` hides the burn alarm on a job with no budgets (claim 23). docs/system/cost-anomaly-alarm-v1.md says
   the command prints the full numbers under "recorded burn alarm", and a code comment in apps/cli/commands/job.py says it is "shown
   whatever limits the job has". In `_cmd_job_budget` the early return `if _budgets is None and _budgets_dict is None:` prints
   "Job <id>: no budgets configured." (or JSON `{"budgets": null}` with no `burn_reading`) before the burn block is reached. I
   reproduced it through the CLI: an unattended spike job with no budgets was paused by the alarm, `job show` printed the block, but
   `remedy job budget <id>` printed only "no budgets configured." and `remedy job budget <id> --json` carried no `burn_reading`.
   The tests in test_job_budgets.py only use jobs that have a limit (`max_cost_usd` or `max_total_tokens`), so no test sees this.
   This is outside the feature file's Acceptance wording (the numbers stay visible in `job show` JSON, the decision and the run
   log), so it is a documentation-vs-product gap. A repair needs either the early return to still emit the recorded burn alarm
   (text and JSON) plus a test with a no-budget job, or the docs to say the block appears only for a job with a limit.

Minor note, not counted as a gap: the paused job's own "Next:" line says `remedy job run <id>`, while the decision impact and the docs
say `remedy job unpause <id>`; I did not run unpause.

## Totals

Claims audited: 24 (rows 1 to 23 with 9b; the "c" rows are the same claims through the CLI, and rows 6b and 9c are covered
rows, not counted).
- Proved at once with a proving test and a red mutation: 21 (all but 9b, 22, 23).
- Not built by design: 1 (claim 22).
- Gaps: 2 (claims 9b and 23).
- Command-line proofs: 4 (claims 2c, 7c, 8c, 20c), all reached `apps.cli.grouped.main` and changed under the mutation.

## Cleanup evidence

`git worktree list` after removal (the audit worktree f116-audit-wt-1 is gone; the job-* entries other than the primary are other
sessions' job workspaces; my CLI driver's first two runs briefly made job-1a1f21d2506545bc and job-39ab3c57316f4493 workspaces and
branches because the scratch repo had no commit and git fell back to the primary checkout; I removed both worktrees and both
`remedy/job-...` branches):

(see the final lines appended below)
/home/decodeux/Repos/remedy                                  ddcedb336 [feature/f116-cost-anomaly-alarm]
/home/decodeux/Repos/remedy/.remedy-wt/job-034ab8c2d9fa4013  218eaabd6 [remedy/job-034ab8c2d9fa4013]
/home/decodeux/Repos/remedy/.remedy-wt/job-129b3ad7206d4f8d  09441a92a [remedy/job-129b3ad7206d4f8d]
/home/decodeux/Repos/remedy/.remedy-wt/job-1fe227733cbf41eb  218eaabd6 [remedy/job-1fe227733cbf41eb]
/home/decodeux/Repos/remedy/.remedy-wt/job-6a38b3203cca4928  aab638e21 [remedy/job-6a38b3203cca4928]
/home/decodeux/Repos/remedy/.remedy-wt/job-d0f70d9d45dd4363  e4fa7d06f [remedy/job-d0f70d9d45dd4363]
/home/decodeux/Repos/remedy/.remedy-wt/job-e7268925db3a4831  cc8696a37 [remedy/job-e7268925db3a4831]
/home/decodeux/Repos/remedy/.remedy-wt/job-e7a145761bf04f86  03d435e59 [remedy/job-e7a145761bf04f86]
/home/decodeux/Repos/remedy/.remedy-wt/job-f03587d31f444b15  3f36bd811 [remedy/job-f03587d31f444b15]
/home/decodeux/Repos/remedy/.remedy-wt/job-f146c82a6d8e42ca  8b6e803f7 [remedy/job-f146c82a6d8e42ca]
/home/decodeux/Repos/remedy/.remedy-wt/job-f196d785124e48bc  3f36bd811 [remedy/job-f196d785124e48bc]
/home/decodeux/Repos/remedy/.remedy-wt/job-fd57a5d1dfe245b0  68c833e6c [remedy/job-fd57a5d1dfe245b0]

`git status --porcelain` of the primary checkout: (empty)

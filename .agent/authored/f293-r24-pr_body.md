## What

F293 — Test load diet. The operator's machine ran hot and drew a lot of power whenever the tests
ran, and he ordered the test load cut. This branch cuts the processor time of a full test run by
about a quarter and adds the checks that keep it down:

- **T001, the inventory.** One full run, ranked: `.agent/f293_inventory.md` holds six readings
  (collection cost, share per file, the hundred slowest tests, child processes, UI builds and
  browser starts, processes left alive).
- **T002, the cuts.** Each measured before and after in one tree, with a red-proof per changed test:
  the dead-command scan and its answers cached per search root; the review manifest's metadata scan
  cached per text; the run manifest's key check cached per key and use; Remedy's own checkout
  identity read once per test process; the mission tests' setup written in-process; two tests no
  longer start a paid model process; one retry test no longer sleeps through a 30-second backoff.
- **T003, keeping it down.** A test run that leaves a process behind fails, names the process and
  ends it. `scripts/closure_suite_cost.py` puts each closure run's processor time into its suite
  transcript and exits 1 when a closure costs more than 10 percent above the previous one.
- **T004, making it visible.** `remedy doctor core` says in one sentence how many test runs and
  processor minutes the last 24 hours cost, and says so in words when no record exists.
- **The hardening stage (SLOW MODE).** A fresh auditor checked every Acceptance and Goal statement
  with a mutation. The three gaps it found were repaired: the inventory was unguarded, nothing
  guarded that no assertion was lost, and the first guard counted assertions without reading them.
  `tests/regression/test_f293_acceptance.py` now holds, while F293 is open, that every unit of test
  code that existed where F293 began is unchanged or is a reviewed change pinned by a digest.
- **The closure's self-use item SU-040.** Remedy ran it on itself and its own reviewer passed it.
  The task-progress probe of `remedy dev status` now catches only the four errors it can meet,
  with two tests through the command line.
- **R-1124.** The closure suite's first run found a live UI test whose fake browser left a `sleep`
  running after every test run. The browser now runs in a session of its own, and closing the pipe
  ends the whole process group.

## Why

The measured result, from the test load record: T001's run used 1,246.09 CPU seconds and 355.02
wall seconds for 21,102 tests. The closure run used 940.64 CPU seconds and 276.83 wall seconds for
21,145 tests, 24.5 percent less CPU time. The target was 40 percent. The largest known remaining
cost is product work: the job runner starts about 210 git processes per `remedy do`. That work is
split off as **F294, Test load diet, part two**, registered directly after F293 (DECISION F293 D15).
Operator question Q2 records the split as a reversible ruling.

## Key decisions (in `.agent/decisions.md`)

- D1: T001's run and the closure's run are the two ends of the one comparison.
- D2 to D6, D10: the cuts and their before-and-after readings.
- D7: `remedy doctor core` reads the test load record as information only.
- D8: a run that leaves a process behind fails.
- D9: the closure suite transcript carries its CPU seconds and compares them with the previous
  closure's.
- D11 to D13: the acceptance audit's gaps and their guard.
- D14: SU-040 lands.
- D15: F293 closes at 24.5 percent; the rest is F294.

## How to review / test

- Read `docs/roadmap/features/T2_F293.md`'s Built State first; it names every piece and its
  DECISION.
- `python3 -m pytest tests/regression/test_f293_acceptance.py tests/regression/test_test_load_governor.py tests/orchestration/test_closure_suite_cost.py tests/orchestration/test_dead_command_check.py -q -n auto`
- `python3 -m apps.cli.main doctor core` prints the `test load:` line.
- The closure suite transcript is `.agent/authored/f293-closure-suite.txt`: `21125 passed, 20 skipped`,
  exit 0, no process left behind, `Test load: 940.64 CPU seconds`.

## Changed files (outside `.agent/`, fork point `8a067a3b9` to this branch)

| Path | + | - |
|---|--:|--:|
| `README.md` | 14 | 3 |
| `apps/cli/commands/dev.py` | 1 | 1 |
| `apps/cli/commands/worker_facade_cmd.py` | 63 | 1 |
| `docs/agents/integration_gate.md` | 5 | 0 |
| `docs/roadmap/STATUS.md` | 2 | 1 |
| `docs/roadmap/STATUS_closure_protocol.md` | 7 | 1 |
| `docs/roadmap/features/T2_F293.md` | 71 | 0 |
| `docs/roadmap/features/T2_F294.md` | 43 | 0 |
| `packages/orchestration/dead_command_check.py` | 59 | 13 |
| `packages/orchestration/run_manifest.py` | 11 | 1 |
| `scripts/build_review_manifest.py` | 6 | 1 |
| `scripts/closure_suite_cost.py` | 115 | 0 |
| `scripts/self_use_queue.json` | 8 | 0 |
| `tests/cli/test_mission_cmd.py` | 90 | 93 |
| `tests/cli/test_worker_facade_cmd.py` | 86 | 2 |
| `tests/conftest.py` | 40 | 1 |
| `tests/docs/test_docs_consistency.py` | 4 | 1 |
| `tests/load_governor.py` | 76 | 0 |
| `tests/orchestration/test_closure_suite_cost.py` | 130 | 0 |
| `tests/orchestration/test_dead_command_check.py` | 55 | 0 |
| `tests/orchestration/test_job_budgets.py` | 14 | 7 |
| `tests/orchestration/test_job_task_runner.py` | 53 | 2 |
| `tests/orchestration/test_review_gate_sensitive_metadata.py` | 22 | 0 |
| `tests/orchestration/test_run_manifest_security.py` | 28 | 0 |
| `tests/regression/test_f293_acceptance.py` | 207 | 0 |
| `tests/regression/test_named_bugs.py` | 44 | 0 |
| `tests/regression/test_test_load_governor.py` | 104 | 0 |
| `tests/runtimes/test_dev_server.py` | 18 | 13 |
| `tests/test_ble001_ratchet.py` | 1 | 1 |
| `tests/test_no_orphan_modules.py` | 2 | 0 |
| `tests/ui_server/test_story_export_file_live.py` | 50 | 2 |

## Verdict and evidence

- Latest live review verdict: PASS (round 23); F293 accepted PASS_WITH_RISKS, the risk being the
  split to F294.
- Evidence job `f293r23e1001`, package `remedy-review-20261001-005405-READY_FOR_REVIEW.zip`,
  SHA-256 `2c72c60f7058a7c2d9d7a0ad72a161115c282162a7ebc994bd7f0118ea704fb6`, archived at
  `/home/decodeux/Repos/remedy-history/zips`, accepted head `b59d42cc9`.
- Open findings: 2, both owned by F290, Findings paydown v6. R-1117 (Medium) is carried from F044.
  R-1125 (Low) is new: the README's Tier 5 row undercounts, and no test reads the tier rows.

## Runtime actuals

- Rounds: 24, in 6 sessions, from 2026-09-30 to 2026-10-01.
- Models: the reviewer ran on Claude Opus 5.5, and each round's worker was a delegated subagent.
  The self-use job ran on `claude-cli` / `claude-sonnet-4-6`: 2 provider calls, $0.69.
- Tokens and cost of the sessions themselves: not measured.
- Full-suite runs: T001's run, then the closure run twice (round 20 exited 1 on R-1124, and round
  21 re-ran on the repaired tree, per amend0921 rule 1).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

# F293 Test load diet — Acceptance audit (amend0930b-slow-cap hardening stage)

Auditor read only `docs/roadmap/features/T2_F293.md`, `AGENTS.md`, and the repository code/tests
(not `.agent/handoff.md`, `.agent/live_review.md`, `.agent/authored/`, `.agent/plan.md`,
`.agent/decisions.md`). All mutations ran in a disposable worktree,
`/home/decodeux/Repos/remedy/.remedy-wt/f293-audit-wt`, created at `git worktree add --detach`
from HEAD `65018abe6`. Every run used `python3 -B -m pytest ... -q -n auto -p no:cacheprovider`
on at most one or two files at a time; no full suite was run. No test run reported leaving a
process behind, except the one test whose whole subject is that mechanism, where the leftover
process is the expected fixture behaviour, always reaped by the test itself or by its assertions.

Total claims audited: 8. Proven at once: 4. Gaps: 2. Measurement-only (not run): 2.

---

## Claim 1 (T001) — the inventory file

> "T001: `.agent/f293_inventory.md` exists and holds the six readings named above from one run."

No test in the repository reads, checks the existence of, or checks the content of
`.agent/f293_inventory.md`. Grepped `tests/`, `scripts/`, and `docs/` for `f293_inventory`;
the only hit is the feature file itself (`docs/roadmap/features/T2_F293.md` lines 49 and 64).
Manual inspection shows the file does exist and does hold six `##` sections matching the six
readings named in T001's task text (cost of collection, CPU share per file, 100 slowest tests,
child-process count, UI-build/Chrome-start count, processes alive after the run) — the product
meets the claim — but nothing in the repository would turn red if the file were deleted or its
numbers were replaced with nonsense.

- Test node id(s): none found.
- Mutation: not applicable (no test to mutate against).
- Reaches the user: no.
- **Verdict: GAP.** The claim is met by the file's content today, but it is unguarded: a future
  edit or deletion of `.agent/f293_inventory.md` would pass every test in the repository.

---

## Claim 2 (T002, and Goal & Done's "DONE when..." sentence, and Goal & Done's "the full suite...
cost much less CPU time") — the 40 percent full-suite CPU reduction

> "T002: the full suite's CPU seconds in the test load record are at least 40 percent below T001's
> baseline, or a dated DECISION shows with numbers that what remains cannot be made cheaper
> without weakening a test."
> "DONE when the full suite's CPU seconds ... are at least 40 percent below the baseline T001
> measures, OR the ranking shows that what remains cannot be made cheaper without weakening a
> test, and a dated DECISION says so with the numbers."
> "The full suite ... cost much less CPU time ..."

These three sentences state one claim under three different headings/wordings: the full suite's
measured CPU seconds (read from `~/.remedy-loop/test_load.jsonl`, appended by
`tests/conftest.py`/`tests/load_governor.py`) must be ≥40% below T001's baseline of 1,288 CPU
seconds, OR a dated DECISION must record the numbers showing the remainder cannot be cut further
without weakening a test.

This is, by its nature, a full-suite measurement claim, and the audit's own rules forbid running
the full suite to decide it. No mutation can prove or disprove a CPU-seconds total.

What evidence exists in the repository, and where:
- The baseline number itself: `docs/roadmap/features/T2_F293.md` lines 34–44 ("used 1,288 CPU
  seconds (21.5 CPU minutes)").
- The mechanism that would record and compare a later run: `tests/load_governor.py`
  (`build_record`, `append_record`) and `scripts/closure_suite_cost.py` (reads the newest
  `pytest -n auto -q` line and compares it to the previous closure's transcript line, but that
  script's 10 percent rule is Claim 6 below — closure-to-closure drift, not the 40 percent
  T001-to-now target).
- No dated DECISION with the 40 percent numbers is visible from any file this audit is permitted
  to read (`.agent/decisions.md` is explicitly off limits, and no such numbers appear in
  `docs/roadmap/STATUS.md`, which still lists F293 as `[~]` — in progress, not accepted).
- No script or test in the repository computes "T001's baseline vs. today" as a 40 percent ratio;
  only the closure-to-closure 10 percent comparator (Claim 6) exists in code.

- Test node id(s): none for the 40 percent figure specifically.
- Mutation: not attempted (measurement claim).
- Reaches the user: n/a.
- **Verdict: MEASUREMENT-ONLY / cannot be decided by this audit.** The repository records the
  mechanism to measure this but no evidence this audit may read shows the current figure or a
  settling DECISION; `docs/roadmap/STATUS.md` marks F293 still open.

---

## Claim 3 (Goal & Done) — "the round selections cost much less CPU time"

> "The full suite and the round selections cost much less CPU time without losing a single
> assertion."

Read as a separate claim from Claim 2: round-scoped test selections (500–2,300 tests, up to three
times per round per the feature's "Why this exists" section) must also cost much less CPU.

The test load record (`tests/load_governor.py`) logs every pytest invocation's command and CPU
seconds, including round selections, so the raw data exists. But no script or test in the
repository computes or asserts a "round selection cost" trend or comparison — `scripts/
closure_suite_cost.py` filters specifically for the full-suite command (`FULL_SUITE_COMMAND =
"pytest -n auto -q"`, `scripts/closure_suite_cost.py` line 27) and ignores every other command
line, by design (`TestTheRunIsTheNewestFullSuiteLine::test_other_commands_and_lines_that_do_not_
parse_are_skipped` in `tests/orchestration/test_closure_suite_cost.py` explicitly asserts that a
`pytest tests/cli -q -n auto` line, i.e. a round selection, is skipped).

- Test node id(s): none that measure or compare round-selection cost.
- Mutation: not applicable.
- Reaches the user: n/a.
- **Verdict: MEASUREMENT-ONLY, and unguarded even as a measurement.** Round-selection cost is
  recorded per-run in the test load record but never aggregated, compared, or asserted anywhere in
  the repository; no evidence this audit may read shows whether round selections got cheaper.

---

## Claim 4 (Goal & Done) — "without losing a single assertion"

> "The full suite and the round selections cost much less CPU time without losing a single
> assertion."

Read as a claim distinct from the CPU claims: no test assertion anywhere in the suite was weakened
or deleted while cutting CPU cost.

Searched for any assertion-count guard, coverage-delta check, or collected-test-count regression
check tied to F293. None exists: `scripts/closure_suite_cost.py` and its tests compare CPU
seconds only, never assertion or test counts; no script in `scripts/` computes an assertion count
at all. The per-task rule that is meant to enforce this in practice — "every changed test keeps a
red-proof: a mutation of the production line it guards still turns it red" — lives under the
Tasks heading (T002), not under Acceptance or Goal & Done, and even there it is a per-round manual
discipline, not a single automated gate with a test node id.

- Test node id(s): none found.
- Mutation: not applicable (no mechanism to mutate against).
- Reaches the user: no.
- **Verdict: GAP.** Nothing in the repository would turn red if an assertion were quietly deleted
  during a CPU-cutting change; the claim rests entirely on per-round manual discipline recorded
  outside the files this audit may read.

---

## Claim 5 (T003, first half) — a closure costing >10% more than the previous one registers a finding

> "T003: a closure whose suite CPU exceeds the previous feature's by more than 10 percent
> registers a finding."

Implemented in `scripts/closure_suite_cost.py`, function `compare()` (lines 75–88): computes the
percent change against the previous closure's `cpu_seconds`, and when `percent > LIMIT_PERCENT`
(10.0), prints a sentence ending "...so this closure registers a finding owned by the rolling
findings paydown." and returns exit code 1.

- Test node id(s):
  - `tests/orchestration/test_closure_suite_cost.py::TestTheTenPercentLimit::test_more_than_ten_percent_above_owes_a_finding`
  - `tests/orchestration/test_closure_suite_cost.py::TestTheCommandLine::test_an_expensive_closure_prints_its_line_and_exits_one` (subprocess run of the real script — reaches the feature as a user does)
- Mutation: file `scripts/closure_suite_cost.py`.
  - Original line: `    if percent > LIMIT_PERCENT:`
  - Replacement: `    if False:`
- Green (unmutated), `tests/orchestration/test_closure_suite_cost.py -q -n auto -p no:cacheprovider`:
  exit 0, `11 passed in 0.85s`.
- Red (mutated), same command: exit 1, `2 failed, 9 passed in 0.83s` —
  `TestTheTenPercentLimit::test_more_than_ten_percent_above_owes_a_finding` (`assert 0 == 1`) and
  `TestTheCommandLine::test_an_expensive_closure_prints_its_line_and_exits_one` (subprocess
  returned 0 instead of 1, printing "...within the 10 percent limit." instead of the finding
  sentence) both failed.
- Mutation reverted; `git diff --stat` in the worktree empty afterward.
- Reaches the user as a CLI: yes — `TestTheCommandLine` runs `python3
  scripts/closure_suite_cost.py --feature F103 --record <path> --authored <path>` as a real
  subprocess and asserts on its exit code and stdout.
- **Verdict: PROVEN.**

---

## Claim 6 (T003, second half) — a test run that leaves a process behind fails

> "T003: ... a test run that leaves a process behind fails."

Implemented in `tests/conftest.py`, `pytest_sessionfinish` (lines 164–181): when
`load_governor.end_processes(load_governor.leftover_processes(...))` returns any ended process,
the session's exit status is forced to `pytest.ExitCode.TESTS_FAILED` and a red line is printed
via `load_governor.leftover_notice`.

- Test node id: `tests/regression/test_test_load_governor.py::TestNoProcessLeftBehind::test_a_run_that_leaves_a_process_behind_fails_and_the_process_is_ended`
  — this test itself spawns a real, separate `python3 -m pytest` subprocess against a throwaway
  test file that leaks a child process, and asserts on that subprocess's exit code and stdout, so
  it is itself the "real `python3 -m pytest` run of a small file" example the audit instructions
  name directly.
- Mutation: file `tests/conftest.py`.
  - Original:
    ```
            if ended:
                session.exitstatus = pytest.ExitCode.TESTS_FAILED
                exitstatus = session.exitstatus
    ```
  - Replacement (dropped the `session.exitstatus = ...` line):
    ```
            if ended:
                exitstatus = session.exitstatus
    ```
- Green (unmutated), `tests/regression/test_test_load_governor.py::TestNoProcessLeftBehind::test_a_run_that_leaves_a_process_behind_fails_and_the_process_is_ended -q -n auto -p no:cacheprovider`:
  exit 0, `1 passed in 4.16s`.
- Red (mutated), same command: exit 1, `1 failed in 4.21s` — the inner pytest run still printed
  "remedy tests: the run left 1 process(es) behind, now ended (F293 T003): pid ..." and still
  ended the leaked process, but returned exit code 0 ("1 passed") instead of 1, so the outer
  assertion `done.returncode == 1` failed.
- Mutation reverted; `git diff --stat` in the worktree empty afterward.
- Reaches the user as a CLI: yes, by construction (see above).
- **Verdict: PROVEN.**

---

## Claim 7 (T004, first half) — `remedy doctor core` prints the one sentence from the record

> "T004: `remedy doctor core` prints the one sentence, from the record ..."

Implemented in `apps/cli/commands/worker_facade_cmd.py`: `last_day_test_load()` (lines 146–187)
builds the sentence from the record's `cpu_seconds`/`utc` fields; `_cmd_doctor_core` (line 585)
prints it under a `test load:` heading.

- Test node id(s):
  - `tests/cli/test_worker_facade_cmd.py::TestDoctorCoreTestLoad::test_json_counts_the_cpu_of_the_last_24_hours_only`
  - `tests/cli/test_worker_facade_cmd.py::TestDoctorCoreTestLoad::test_text_mode_prints_the_sentence_before_the_dead_commands`
- Mutation: file `apps/cli/commands/worker_facade_cmd.py`.
  - Original line: `    cpu_minutes = round(cpu_seconds / 60, 1)`
  - Replacement: `    cpu_minutes = round(cpu_seconds / 6000, 1)`
- Green (unmutated), `tests/cli/test_worker_facade_cmd.py::TestDoctorCoreTestLoad -q -n auto -p no:cacheprovider` (run with `REMEDY_TEST_LOAD_LOG=""` to avoid touching the operator's real record):
  exit 0, `6 passed in 3.17s`.
- Red (mutated), same command: exit 1, `2 failed, 4 passed in 3.11s` — both node ids above failed,
  e.g. `'2 test runs used 0.0 CPU minutes...'` instead of `'...1.5 CPU minutes...'`.
- Mutation reverted; `git diff --stat` in the worktree empty afterward; re-run green (`6 passed in 3.07s`).
- Reaches the user as a CLI: yes — ran `python3 -B -m apps.cli.main doctor core` directly in the
  worktree. Unmutated it printed `test load:` / `207 test runs used 104.9 CPU minutes in the last
  24 hours.` (the operator's real record, read-only). Mutated it printed `test load:` / `208 test
  runs used 1.1 CPU minutes in the last 24 hours.` — visibly wrong, ~100x understated, while still
  exiting 0 (the doctor command never fails on this alone by design).
- **Verdict: PROVEN.**

---

## Claim 8 (T004, second half) — prints nothing wrong when the record is absent

> "T004: ... and prints nothing wrong when the record is absent."

Implemented in the same `last_day_test_load()`: when `path is None or not path.is_file()`, it
returns the `absent` dict with the plain sentence "No test load record was found on this machine,
so the test cost of the last 24 hours is unknown." rather than raising.

- Test node id: `tests/cli/test_worker_facade_cmd.py::TestDoctorCoreTestLoad::test_an_absent_record_is_said_plainly_and_changes_nothing_else`
  (also broke `test_the_default_record_lives_in_the_home_folder` and both parametrized cases of
  `test_a_record_that_cannot_be_read_is_unknown_and_changes_nothing_else`, all guarding the same
  code path).
- Mutation: file `apps/cli/commands/worker_facade_cmd.py`.
  - Original line: `    if path is None or not path.is_file():`
  - Replacement: `    if False:`
- Green (unmutated): see Claim 7's green run (same test class, `6 passed in 3.17s`).
- Red (mutated), `tests/cli/test_worker_facade_cmd.py::TestDoctorCoreTestLoad -q -n auto -p no:cacheprovider`
  (again with `REMEDY_TEST_LOAD_LOG=""`): exit 1, `4 failed, 2 passed in 3.14s` — every test that
  exercises an absent/unset record crashed with `AttributeError: 'NoneType' object has no
  attribute 'read_text'` instead of returning the plain sentence.
- Mutation reverted; `git diff --stat` in the worktree empty afterward.
- Reaches the user as a CLI: yes — ran `python3 -B -m apps.cli.main doctor core` with
  `REMEDY_TEST_LOAD_LOG=""` directly. Unmutated: exit 0, prints "No test load record was found on
  this machine, so the test cost of the last 24 hours is unknown." under `test load:`. Mutated:
  exit 1, the whole command crashes — `Error: AttributeError: 'NoneType' object has no attribute
  'read_text'` — the opposite of "prints nothing wrong."
- **Verdict: PROVEN.**

---

## Totals

- Claims audited: 8
- Claims with a proving test proven at once (mutation red, unmutated green, both in one worktree): 4
  - Claim 5 (T003 finding on >10% closure drift)
  - Claim 6 (T003 leftover-process failure)
  - Claim 7 (T004 sentence printed from record)
  - Claim 8 (T004 nothing wrong when record absent)
- Gaps: 2
  - Claim 1 (T001) — `.agent/f293_inventory.md` is unguarded by any test.
  - Claim 4 (Goal & Done "without losing a single assertion") — no automated check exists anywhere
    in the repository for this.
- Measurement-only, not decidable without running the full suite (not run, per the audit's own
  rule): 2
  - Claim 2 (T002 / Goal & Done DONE sentence / Goal & Done "cost much less CPU time") — the 40
    percent full-suite CPU reduction target; only the baseline number and the recording mechanism
    are visible to this audit, no current figure or settling DECISION.
  - Claim 3 (Goal & Done "the round selections cost much less CPU time") — recorded per-run but
    never aggregated or compared by any script or test.

## Worktree cleanup

Removed `/home/decodeux/Repos/remedy/.remedy-wt/f293-audit-wt` with `git worktree remove --force`.
`git worktree list` afterward shows only the primary checkout and the pre-existing `remedy/job-*`
worktrees that were present before this audit started and were never touched by it.
Primary checkout `git status --porcelain` is empty.

## What

F294 — Test load diet, part two. The operator's machine ran hot and drew a lot of power whenever
the tests ran, and he ordered the test load cut by 40 percent. The first diet, F293, reached about
a quarter; this branch carries the rest of that work and closes it with a ruling:

- **T002, the cuts.** Each was measured before and after in one tree, and each kept its red-proof.
  Reading which repository a job works in now discovers git's configured helpers once instead of
  before each of six git commands (D1), and runs `git submodule status` only when the index holds
  a submodule (D3); both make every real job start less work, not only the tests. Every test's data
  root comes from one parent per test process, so no test lists the whole base temporary directory
  to number its root (D2). The golden-path tests run `init`, `do` and `status` in the test process,
  and the scoped-listing tests their setup, through `tests/cli/in_process_cli.py`, while every other
  command those files assert on still runs as a child process (D4, D5). No assertion was removed.
- **The hardening stage (SLOW MODE).** A fresh auditor checked every Acceptance and Goal statement
  with a mutation. It audited eight statements; four had a proving test at once, one is read from
  the closure's full run, and three were gaps. `tests/regression/test_f294_acceptance.py` now
  guards that no assertion is lost from a file this feature changed (R-1126, resolved). The data
  root allocator's test was strengthened three times; what remains, a listing function bound to a
  name before the test runs, stays open as R-1127 for the next findings paydown (D7 to D10).
- **The closure's self-use item SU-041.** Remedy ran it on itself and its own reviewer passed it.
  The autocoder probe of `remedy dev status` now catches only the two errors it can meet, and two
  tests pin it through the command line (D11).

## Why

The measured result, from the test load record: T001's baseline was 1,246.09 CPU seconds; F293's
closure run used 940.64. This branch's closure run used 865.36 CPU seconds for 21,160 tests, exit 0:
8.0 percent below F293 and 30.55 percent below the baseline, so the 40 percent target of 747.65 is
missed by 117.71 CPU seconds. F294 closes on its Acceptance's second branch (D12): the costliest
tests left each run a real job and then change it, and what a job run still costs is the job
runner's own protective work, the absorb of a human change at every safe point and the
definition-of-done gate, which the tests can only skip by no longer checking a real job. No
follow-up feature is registered. Operator question Q3 records this as a reversible ruling and
offers the cheaper job run as a product change.

## Key decisions (in `.agent/decisions.md`)

- D1 to D5: the cuts and their before-and-after readings.
- D6: the measured map of what remains.
- D7 to D10: the acceptance audit, its repairs, and where the hardening stage stopped.
- D11: SU-041 lands.
- D12: F294 closes at 865.36 CPU seconds on its Acceptance's second branch.
- D13: the checklist's one consolidation pass adds nothing; the list stays at 34 items.

## How to review / test

- Read `docs/roadmap/features/T2_F294.md`'s Built State first; it names every piece and its
  DECISION.
- `python3 -m pytest tests/orchestration/test_run_manifest_integrity.py tests/test_data_root_isolation.py tests/regression/test_f294_acceptance.py tests/cli/test_golden_path.py tests/cli/test_scoped_listings.py -q -n auto`
- The closure suite transcript is `.agent/authored/f294-closure-suite.txt`: `21139 passed, 21
  skipped`, exit 0, no process left behind, 865.36 CPU seconds.

## Changed files (outside `.agent/`, fork point `020bc9a16` to this branch)

| Path | + | - |
|---|--:|--:|
| `README.md` | 13 | 3 |
| `apps/cli/commands/dev.py` | 1 | 1 |
| `docs/roadmap/STATUS.md` | 1 | 1 |
| `docs/roadmap/features/T2_F294.md` | 57 | 0 |
| `packages/orchestration/run_manifest.py` | 62 | 16 |
| `scripts/self_use_queue.json` | 8 | 0 |
| `tests/cli/in_process_cli.py` | 53 | 0 |
| `tests/cli/test_golden_path.py` | 7 | 15 |
| `tests/cli/test_scoped_listings.py` | 7 | 8 |
| `tests/conftest.py` | 23 | 2 |
| `tests/orchestration/test_run_manifest_integrity.py` | 130 | 0 |
| `tests/regression/test_f294_acceptance.py` | 83 | 0 |
| `tests/regression/test_named_bugs.py` | 42 | 0 |
| `tests/test_ble001_ratchet.py` | 1 | 1 |
| `tests/test_data_root_isolation.py` | 27 | 0 |

## Verdict and evidence

- Latest live review verdict: PASS (round 15); F294 accepted PASS_WITH_RISKS, the risks being the
  missed 40 percent number, closed by DECISION F294 D12, and R-1127.
- Evidence job `f294r15e1001`, package `remedy-review-20261001-050249-READY_FOR_REVIEW.zip`,
  SHA-256 `eab0f7f1935e9b57ca6020ba508bd391a190b335f20a2648196beb69a98c0116`, archived at
  `/home/decodeux/Repos/remedy-history/zips`, accepted head `5c7006583`.
- Open findings: 3, all owned by F290, Findings paydown v6. R-1117 (Medium) is carried from F044,
  R-1125 (Low) from F293, and R-1127 (Low) is new here: the data root allocator's test cannot see a
  listing function bound to a name before it runs.

## Runtime actuals

- Rounds: 16, in 3 sessions, all on 2026-10-01.
- Models: the reviewer ran on Claude Opus 5.5, and each round's worker was a delegated subagent.
  The self-use job ran on `claude-cli` / `claude-sonnet-4-6`: 4 provider calls, $0.93.
- Tokens and cost of the sessions themselves: not measured.
- Full-suite runs: one, the closure run in round 13.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

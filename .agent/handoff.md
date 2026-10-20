# Handoff — F310 round 2 (the working wall clock)

## Session

SESSION 1 of feature F310 · round 2 · rounds so far 2

Context self-assessment: the session stayed small; every file was read once, the prepared files were
copied by digest-checked byte copies, and the gates ran once on the final code tree.

State block:
Feature F310 (claimed `[~]`), branch `feature/f310-provider-budgets`, base `2986ffd4f`.
Fortschritt: ~55 % (claim, T001 and T002 landed · T003 and T004 open) — Schätzung

## Range

Review of `2986ffd4f`..HEAD (the four commits below, then this handback's own commit).

## Commits

### 93b7b9f8f F310 R2 C1: book round 1, DECISION F310 D4, the plan
258 insertions, 16 deletions (`git show --shortstat`).
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f310-r2.md` | +229 | byte copy of the block |
| `.agent/live_review.md` | +2 | round 1 booked |
| `.agent/prose_slips.md` | +3 | the reviewer's three slips |
| `.agent/decisions.md` | +10 | DECISION F310 D4 |
| `.agent/plan.md` | +14/-16 | rewritten |

### 4d6962e8a F310 R2 C2: the record decoder's start instant moves to budget_clock.py (structure step)
49 insertions, 28 deletions.
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/budget_clock.py` | +38 | new module, `decode_persisted_started_at`, moved unchanged |
| `packages/orchestration/budget_guard.py` | +2/-26 | the decoder calls it |
| `docs/system/structure-ledger-v1.md` | +7/-1 | boundary written, row 128 to 104 |
| `tests/test_structure_ratchet.py` | +1/-1 | `MAX_FUNCTION_LINES` 28962 to 28938 |
| `tests/orchestration/import_reachability_allowlist.txt` | +1 | new module listed |

### 4b2f6079f F310 R2 C3: the wall clock counts work and records every wait between runs
155 insertions, 41 deletions.
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/budget_clock.py` | +96 | error class, clock decoder, resume, working start |
| `packages/orchestration/budget_guard.py` | +7/-5 | version 3, clock fields, elapsed minus waiting |
| `packages/orchestration/pingpong_job.py` | +14/-21 | `run_job` resumes its clock; the record carries it |
| `packages/orchestration/pi_provider.py` | +4/-5 | the time bound reads the effective limits and the working start |
| `packages/orchestration/budget_profiles.py` | +4/-3 | `getattr` reads |
| `docs/system/job-budget-enforcement-v0.md` | +18 | clock section |
| `docs/roadmap/features/T12_F310.md` | +5 | amendment |
| `docs/system/structure-ledger-v1.md`, `tests/test_structure_ratchet.py` | rows and pins | see Verification |

### a60fae355 F310 R2 C4: the working wall clock, tested
236 insertions, 8 deletions.
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_budget_clock.py` | +228 | 29 tests |
| `tests/orchestration/test_budget_guard.py` | +4/-4 | version pins |
| `tests/orchestration/test_f018_authority_integration.py` | +2/-2 | version pin |
| `tests/orchestration/test_job_digest.py` | +2/-2 | version pins |

### this handback's commit (C5)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this file |

## External actions

- `git push origin feature/f310-provider-budgets` after C5; the result is in the worker's report.
- No pull request opened; no other gh command.

## Verification

All gates ran once, on the tree at `a60fae355`, before this commit.
1. `git status --porcelain` printed nothing. `python3 .remedy-wt/f310-r2/prep/verify.py .`: every
   line `True`, C5 `absent`, last line `ALL True`.
2. `python3 -m ruff check` over the 10 Python files of C2 to C4: `All checks passed!`
3. `run_selection.py`: `paths 114`, `exit 0`, `4939 passed, 2 skipped in 58.31s`; no FAILED, ERROR or
   "process(es) behind" line. SKIPPED: `tests/test_agent_tooling.py:43` (D12 quarantine, F252) and
   `tests/test_install_smoke.py:175` (opt-in install smoke).
4. `python3 -m apps.cli.main integrity check --json`: exit 1, `fail_count` 1, the one failing check
   `high_blockers_open` naming R-1335, R-1336, R-1337, R-1338, R-1345, R-1346, R-1348, R-1349,
   R-1359, R-1360, R-1361, R-1362 and R-1369 (thirteen, as at the base).
5. `open_finding_ids` of `scripts/rotate_live_review.py` over the ledger: `87`.

Structure ratchet rows lowered: `decode_persisted_budget_actuals` 128 to 104 (C2); `run_job` 1441 to
1434; `pingpong_job.py` 5338 to 5331 (C3); `MAX_FUNCTION_LINES` 28962 to 28938 (C2) to 28931 (C3);
`MAX_FILE_LINES` 64274 to 64267 (C3). No row rose, none was added. `budget_guard.py` is 973 lines.

## Authored-text proofs

Byte copies, sha256 equal to the source (checked by script before the write and by `verify.py` after):
block (`94a85b4f…2680`, 229 lines), the four prepared state files, the boundary text, the clock
section of `docs/system/job-budget-enforcement-v0.md` and the amendment of the feature file.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | this commit |
| Gate 1 | done | |
| Gate 2 | done | |
| Gate 3 | done | |
| Gate 4 | done | fail_count 1, the standing thirteen |
| Gate 5 | done | 87 |

## Deviations & assumptions

- C2 added one line to `tests/orchestration/import_reachability_allowlist.txt`, which the block permits
  when the reachability test asks (it did).
- C3: `pi_provider.py` also loses its `from datetime import datetime` line, because the edit left it
  unused and the linter would refuse it.
- C3 left three existing tests red until C4, as the block orders; C4 changed them (below).
- Existing tests changed, all as version pins of the record the runner writes (from `2.0.0` to `3.0.0`):
  `tests/orchestration/test_budget_guard.py::TestPersistedActualsCarryMoney::test_the_writer_writes_the_version_the_decoder_names`,
  `tests/orchestration/test_budget_guard.py::TestTheRunPersistsItsLiveMoney::test_the_stopped_run_persists_the_ledger_money_its_safe_point_read`,
  `tests/orchestration/test_f018_authority_integration.py` (the node asserting the stopped run's
  `schema_version`), and in `tests/orchestration/test_job_digest.py`
  `test_a_measured_run_prices_the_digest_through_the_persisted_route` and
  `test_an_unpriced_run_stays_absent_through_the_persisted_route`.
  Also `tests/orchestration/test_budget_guard.py::TestPersistedActualsCarryMoney::test_an_unknown_version_is_rejected`:
  its "unknown" version string `3.0.0` is now a known version, so it uses `4.0.0`. I read this as a
  version pin; flagged for the reviewer.
- The run_job tests of the new file use the local profile (480 minutes), so the stopped case is the
  nine-hour job last active a minute ago.

## For the operator

A job that is stopped and started again used to keep counting the hours it sat idle against its time
limit, so a job paused overnight could be stopped for time it never used. Now the clock counts only the
time a job actually works. Every gap between two runs is recorded as waiting and left out, and the
time limit on a model call is measured the same way. Jobs saved before this change keep working: the
gap since they were last stopped is counted as waiting the first time they resume.

## Next

In order: Phase 1 rule 1 (`.agent/STOP`), then rule 2 (Open PR Gate), then book round 2's verdict in
the next round's first commit, then T003, under DECISION F310 D5.
Operator questions open: 1. Open findings: 87 (gate 5, `open_finding_ids`, read at `a60fae355`).

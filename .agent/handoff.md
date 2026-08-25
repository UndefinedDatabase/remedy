# Handoff — amend0825 dogfooding findings

**Order:** operator collection order amend0825, no self-drive loop.
**Branch:** `feature/amend0825-dogfood-findings`, cut from `main` at `6325ac2f`
(the merge commit of pull request #213).

## Commits

| SHA | Subject |
|-----|---------|
| a653aedb | fix(do): budget the job-less ping-pong run without a job id |
| 307ed926 | fix(doctor): resolve the test lanes against the installation, not the cwd |
| c30e53fb | chore(models): repoint claude-flagship and claude-workhorse off dead ids |
| ea3748ba | feat(do): print the effective model in the bare do run header |
| 8222476e | fix(teach): resolve job ids across both job stores |
| dba53a93 | docs(roadmap): record three operator dogfooding findings |
| ecfd57e9 | docs(system): the shipped defaults are no longer on the dead list |

## Item status

| Item | Status | Reason |
|------|--------|--------|
| 1 — do run budget crash | done | repaired, red-proofed |
| 2 — teacher blind to job runs | done | resolver repaired; narration residue recorded in T5_F255.md |
| 3 — empty token ledger | deviated | design gap, not wiring — recorded in T2_F103.md |
| 4 — promotion dead end | done | recorded in T0_F017.md; guard untouched, as ordered |
| 5 — doctor lanes from a foreign cwd | done | repaired, red-proofed |
| 6 — dead built-in model ids | done | repointed; header names the effective model |

## Changed files

| Path | What |
|------|------|
| apps/cli/commands/do_cmd.py | budget-only safe point; effective-model header |
| apps/cli/commands/worker_facade_cmd.py | `remedy_scripts_dir`; advisory-tier docstring |
| apps/cli/commands/teach_cmd.py | both commands use `resolve_any_job_id` |
| packages/orchestration/data_paths.py | `task_jobs_dir`, `resolve_any_job_id`, shared matchers |
| packages/orchestration/pingpong_job.py | `_jobs_dir` routes through `task_jobs_dir` |
| packages/orchestration/model_aliases.py | two aliases repointed, dated |
| scripts/dead_models.json | reasons re-stated; `superseded_by` filled |
| docs/roadmap/features/{T0_F017,T2_F103,T5_F255}.md | the three recorded findings |
| docs/system/model-defaults-and-dead-model-check-v0.md | stale sentence corrected |
| tests/cli/test_do_cmd_pingpong_budget.py | new, 6 tests |
| tests/cli/test_worker_facade_cmd.py | +5 tests, fixture id read from the table |
| tests/cli/test_teach_cmd.py | +6 tests |

## Verification

| Gate | Command | Result |
|------|---------|--------|
| Canary | `pytest tests/cli/test_golden_path.py -q` | 42 passed |
| Docs round | `pytest tests/docs/ -q` | 295 passed |
| Fast lane | `scripts/remedy_test_fast.sh` | 594 passed |
| Touched suites | 10 files incl. ledger, aliases, teach, budget | 399 passed |
| Wider suites | pingpong_cli, do_job_flow, job_commands, do_run, safe_points | 529 passed |
| Lint | `ruff check` over every changed `.py` | All checks passed |

Red-proof: items 1, 2 and 5 each had their new tests run against the unfixed
code and fail there (2/2, 3/3 and 1/1 respectively).

Pre-existing and untouched: `tests/cli/test_plan_approval.py` carries 6 ruff
findings at `main` and still carries exactly those 6.

## Open

- The three recorded findings are claimed by nobody. No STATUS line was
  registered: each has an owning feature file.
- `remedy plan next` reports **F031 — Decision inbox**, not F022. F022 closed
  on 2026-08-23 with pull request #213.
- `.agent/STOP` remains on disk, untracked, from the stopped F031 R10 round.

## Next expected action
Push, open the pull request, watch the hosted run to green, merge it.

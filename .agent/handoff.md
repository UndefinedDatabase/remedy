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

## CI round 1 — RED, repaired

Run `32893880088` failed with SEVEN failures, all this round's own, in two
stages (`fast` 1, `standard` 6). Repairing them is this round's work per
AGENTS.md amend0820 gate autonomy. Nothing was weakened to reach green.

| Failure | Cause | Repair |
|---------|-------|--------|
| 5 x `tests/orchestration/test_role_config.py` | spelled `claude-opus-4-20250514` where it meant "the flagship alias" | read the id from `MODEL_ALIASES`, as the ollama cases in that file already did |
| `test_dashboard_contract.py::test_context_md_no_stale_steps` | the `context.md` rewrite dropped its `## Steps` section | section restored, stating this order's truth |
| `test_resource_safety.py::test_context_mentions_resource_safety` | the same rewrite dropped the STANDING constraint list | constraints carried forward and marked standing |

The deleted constraint list NAMED the four state readers a `.agent/` rewrite
must gate. The rule that would have prevented two of these failures was on
disk, in the file the rewrite overwrote.

Two process faults produced this, both the same habit — truncating output whose
purpose was completeness:
- `grep ... | head -20` hid `test_role_config.py` from the dead-id sweep.
- `gh run view --log-failed | tail -80` showed only the `standard` stage's six
  failures and hid the `fast` stage's one, which would have caused a second red
  run.

## Verification

| Gate | Command | Result |
|------|---------|--------|
| Canary | `pytest tests/cli/test_golden_path.py -q` | 42 passed |
| Docs round | `pytest tests/docs/ -q` | 295 passed |
| Fast lane | `scripts/remedy_test_fast.sh` | 594 passed |
| Touched suites | 10 files incl. ledger, aliases, teach, budget | 399 passed |
| Wider suites | pingpong_cli, do_job_flow, job_commands, do_run, safe_points | 529 passed |
| State readers | the four this order's constraints name | 559 passed |
| CI `fast` stage | `pytest -n auto -m "<fast marker>"` | 4040 passed, 7 skipped |
| CI `standard` stage | `pytest -n auto -m "<standard marker>"` | 13087 passed, 2 skipped, 1 teardown error |
| Lint | `ruff check` over every changed `.py` | All checks passed |

The one `standard` error is a teardown leak in
`tests/runtimes/test_supervisor_portability.py` — a `runtime stop` child
outlived its file. It is environmental, not this change set: nothing here
touches the supervisor path, the hosted run showed no such error, and the file
re-run alone is 99 passed. Its cause was a pytest killed mid-run earlier in
this session, which is the F085 R64 class of leaked port-bound supervisors.

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

## Deviations, declared

This handoff is 115 lines, over both the 60-line cap and the 100-line
allowance a per-commit table of more than five commits earns. The cause is
mandated content, not prose: the per-commit table of eight commits, the
item-status table the completion protocol requires for an ordered bundle of
six, the changed-files table, the verification table, and the CI-round-1
failure table that records a red gate and its repair. No section is dropped.

## Next expected action
Push, open the pull request, watch the hosted run to green, merge it.

# Handoff — F268 remedy do: the one-command start · Round 5 (R-0968/R-0969/R-0807)

## Session

SESSION 1 of feature F268 · round 5 · rounds so far 5

## Range

Review of 994f045a..HEAD — branch `feature/f268-remedy-do`.

## Summary

The round stopped once, after C1. The block's C2 ordered DECISION F268 D10's `--apply` chaining: job k+1 runs on top of job k's applied output. The dry run showed this cannot work:
- A job's workspace is a `git worktree` cut from the target's HEAD commit (`worktrees.py:330,366`).
- `job_apply` writes the working tree without committing.

So with D10 implemented as written, `remedy do "Write a CONTRIBUTING.md" --apply --force-mission` on the fake provider exited 1 both ways:
- untracked `docs/README.md`: `target_created_since_job`;
- tracked `docs/README.md`: `target_changed_since_job`.

Job 2's builder saw the HEAD content of the file. The reviewer ruled: resume from C1 and book DECISION F268 D12 in C1b. D12 amends D10, and C2 is amended per D12, with tests (2a) and (2b) replacing test (2).

- C2 (D12, R-0968): in a walk of two or more jobs, the run step runs job 1 only and reports `done`, naming the waiting jobs. The ui step opens the cockpit for job 1. The apply step applies job 1 with `--apply`; without it, it stops with job 1's apply command. Each waiting job gets a Next line with real ids: `commit job <predecessor>'s applied output in <repo>, then: remedy job run <id> <provider flags>`. `--json` adds `waiting_job_ids`. A one-job walk is unchanged.
- C2 (R-0969): `do.run` declares `may_mutate_repo=True`. `docs/guides/do-run-v1.md`'s stale catalog line is corrected.
- C3a (R-0912's guard half, needed by D11): `do` plans tasks with minted sixteen-hex ids, which `job_evidence`'s task-id guard refused. So every `do` job's evidence export, and with it the cost mirror, failed with `Unsafe task ID`. The guard now also accepts `mint_task_id`'s exact shape.
- C3 (D11, R-0807's F268 half): the run step mirrors each job it runs through `mirror_job_run_into_ledger`, the call `_cmd_job_run` makes. `do` ends with one `Tokens <role>: input …, output …, cache read … (n call(s))` line per role and one `Cost:` line. These are read through `query_cost(project_id=…, job_id=<id>, by="role")` and summed over the walk's jobs, and a figure no call reported stays `not reported` / null. `--json` carries `cost` with `roles`, `cost_usd`, `job_ids`, `mirror_failed_job_ids` and `mirror_errors`. `context_strategy.json` gains `builder_context`, one entry per task and round, and a `builder_context_note`.

## Commits

### 718696e8 F268 R5 C1: book round 4's verdict, R-0968, R-0969, R-0970 and DECISIONs F268 D10/D11
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f268-r5-block.md` | +108 / -0 | Byte copy of the step block |
| `.agent/authored/f268-r5-decisions.md` | +32 / -0 | Byte copy of the payload |
| `.agent/authored/f268-r5-f273_line.md` | +3 / -0 | Byte copy of the payload |
| `.agent/authored/f268-r5-ledger.md` | +12 / -0 | Byte copy of the payload |
| `.agent/authored/f268-r5-plan.md` | +26 / -0 | Byte copy of the payload |
| `.agent/decisions.md` | +32 / -0 | `git show 994f045a:` bytes + decisions.md (append) |
| `.agent/live_review.md` | +12 / -0 | `git show 994f045a:` bytes + ledger.md (append) |
| `.agent/plan.md` | +7 / -10 | := plan.md payload |
| `docs/roadmap/features/T2_F273.md` | +3 / -0 | f273_line.md inserted after the one line `  text, run before the commit that saves it.` (R-0970's owner line) |

### 9aba205d F268 R5 C1b: DECISION F268 D12 amends D10; prose slip; plan
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f268-r5-decisions_b.md` | +22 / -0 | Byte copy of the payload |
| `.agent/authored/f268-r5-plan_b.md` | +28 / -0 | Byte copy of the payload |
| `.agent/authored/f268-r5-prose_slip.md` | +1 / -0 | Byte copy of the payload |
| `.agent/decisions.md` | +22 / -0 | `git show 718696e8:` bytes + decisions_b.md (append) |
| `.agent/plan.md` | +4 / -2 | := plan_b.md payload |
| `.agent/prose_slips.md` | +1 / -0 | `git show 718696e8:` bytes + prose_slip.md (append) |

### c3cfdd31 F268 R5 C2: a multi-job walk runs job 1 and names the jobs that wait (DECISION F268 D12, R-0968); do.run declares may_mutate_repo (R-0969)
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/command_catalog.py` | +3 / -1 | R-0969: `do.run` `may_mutate_repo=True`, with the reason comment |
| `apps/cli/commands/do_cmd.py` | +4 / -1 | `--json` `waiting_job_ids`; docstring |
| `docs/guides/do-run-v1.md` | +6 / -1 | The stale `may_mutate_repo=False`, `may_execute_commands=False` line now states both True and why (R-0965, R-0969); the v1 flow it describes is unchanged |
| `packages/orchestration/do_sequence.py` | +61 / -14 | D12: `DoContext.waiting_job_ids` and `run_job_ids`. `_step_run` runs `run_job_ids` only and names the waiting jobs. `_step_ui` opens `run_job_ids[-1]`. `_step_apply` acts on `run_job_ids` and appends `do_waiting_job_next_lines`. Module docstring |
| `tests/cli/test_do_sequence_cli.py` | +76 / -14 | Three multi-job tests updated by design (table below), plus the new (2a) and (2b) |
| `tests/orchestration/test_do_run.py` | +11 / -7 | R-0969: the pinned test renamed and flipped. R-0965's sibling now compares `may_mutate_repo` via the new test (table below) |

### 09f63f40 F268 R5 C3a: job evidence accepts the minted task id every do job carries, so its cost mirror can run (R-0912's guard half)
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/job_evidence.py` | +8 / -3 | `_SAFE_TASK_ID_RE` = `^(?:T\d{3,}|[0-9a-f]{16})$`, with the why-comment. The docstring and error message name both shapes |
| `tests/orchestration/test_job_evidence.py` | +31 / -0 | The minted id is accepted, and its near misses (upper case, 15 characters, 17 characters, a trailing `/`) are rejected. A run job whose task carries the minted default exports `task_runs/<id>/provider_evidence.json` |

### d1acc2ae F268 R5 C3: do mirrors each job into the ledger and prints measured tokens per role and cost; the builder's context size per task and round reaches context_strategy.json (DECISION F268 D11, R-0807)
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/commands/do_cmd.py` | +10 / -1 | `cost = do_cost_summary(ctx)`; `--json` `cost`; text prints `do_cost_summary_lines` before the Next lines |
| `packages/orchestration/do_sequence.py` | +81 / -0 | `DoContext.cost_mirrors`; the mirror call after `run_job`; `_add_measured`, `do_cost_summary`, `_measured` and `do_cost_summary_lines`; docstring |
| `packages/orchestration/job_evidence.py` | +47 / -0 | `_BUILDER_CONTEXT_NOTE`, `_builder_context_by_round`; `context_strategy.json` gains `builder_context_note` and `builder_context` |
| `tests/cli/test_do_sequence_cli.py` | +47 / -0 | The cost test against `query_cost`, and the failed-mirror test |
| `tests/orchestration/test_job_evidence.py` | +22 / -0 | The `context_strategy.json` builder-context test |

### (this commit) F268 R5 C4: handoff — round 5
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This document (self-reference exception) |

### Pre-existing tests edited, one line each
| File | Test | Commit | Reason |
|------|------|--------|--------|
| `tests/orchestration/test_do_run.py` | `test_do_run_no_repo_mutation` → `test_do_run_declares_repo_mutation_like_job_apply` | C2 | R-0969's fix clause: it now asserts `may_mutate_repo is True` and equal to `job.apply`'s |
| `tests/orchestration/test_do_run.py` | `test_do_run_declares_command_execution_like_job_run` | C2 | Its tuple compared `may_mutate_repo` with `job.run`'s False, which R-0969 changes by design. It now compares `may_execute_commands` and `action_class` with `job.run`, and `may_mutate_repo` is asserted against `job.apply` by the test above (the reviewer's ruling) |
| `tests/cli/test_do_sequence_cli.py` | `test_force_mission_yields_linked_jobs_all_run_on_the_repo_and_leaves_it_untouched` → `…_runs_the_first_and_leaves_the_repo_untouched` | C2 | D12 by design: job 1 `COMPLETED`, the rest `PLANNED`, `waiting_job_ids == job_ids[1:]`, one apply line (job 1's) |
| `tests/cli/test_do_sequence_cli.py` | `test_without_no_ui_the_cockpit_opens_for_the_last_job_and_reports_its_url` → `…_for_the_job_that_ran_…` | C2 | D12 by design: the launcher is called with `job_ids[0]`, and the URL names it |
| `tests/cli/test_do_sequence_cli.py` | `test_apply_with_force_mission_applies_every_job_in_order` → `test_apply_with_force_mission_applies_the_job_that_ran_and_leaves_the_rest_waiting` | C2 | D12 by design: only job 1's file is applied, no other job id is in the apply detail, and the rest are `PLANNED` and waiting |

## External actions

- The D10 dry run, before the stop: a temporary `tests/cli/test_zz_r5_probe.py` and an uncommitted `do_sequence.py` edit, both removed or reverted with `git checkout --`. A second temporary probe of the same name dumped a fake `do` job's evidence and ledger; it was removed before C3a. Neither was committed.
- G5: `git worktree add --detach .remedy-wt/f268-r5/g5wt d1acc2ae`, removed with `git worktree remove --force` (exit 0). `git worktree list` showed only the main checkout before and after.
- `git push` after this commit (no force). C1 `718696e8` was local-only through the stop and was never amended. The push outcome and G6 are in the round report.
- No PR create, edit or merge.

## Verification

All runs at `d1acc2ae` (C3). C4 changes only this file.

- G1 transport + state (`.remedy-wt/f268-r5/g1.py`) → `REAL_EXIT=0`:
  - For all eight payloads (`block`, `ledger`, `decisions`, `plan`, `f273_line`, `decisions_b`, `prose_slip`, `plan_b`): `digest True authored-copy True`.
  - Against `994f045a`: `C1 live_review append True`, `C1 decisions append True`, `C1 T2_F273 insert (anchor count 1) True`.
  - Against `718696e8`: `C1b decisions append True`, `C1b prose_slips append True`, `C1b plan replace True`.
  - `cmp .agent/plan.md .remedy-wt/f268-r5/plan_b.md` → `CMP_EXIT=0`. The block's `cmp` against `plan.md` no longer holds, because C1b replaced it by ruling.
- G2 `python3 -m pytest -q -p no:cacheprovider` over the block's nine files (this includes every test file this round edited) → `521 passed in 102.34s (0:01:42)`, `REAL_EXIT=0`.
- G3 `python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/orchestration/test_roadmap_index.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py` → `457 passed in 6.69s`, `REAL_EXIT=0`.
- G4 `python3 -m ruff check` over `do_sequence.py`, `job_evidence.py`, `do_cmd.py`, `command_catalog.py`, `test_do_sequence_cli.py`, `test_do_run.py` and `test_job_evidence.py` → `All checks passed!`, `REAL_EXIT=0`.
- G5: one worktree `.remedy-wt/f268-r5/g5wt` at `d1acc2ae`, driven by `.remedy-wt/f268-r5/g5.py`.
  - Each run went from the worktree root with `python3 -B -m pytest -q -p no:cacheprovider tests/cli/test_do_sequence_cli.py tests/orchestration/test_job_evidence.py`. `__pycache__` was purged first, and each run printed `…/.remedy-wt/f268-r5/g5wt/packages/orchestration/do_sequence.py | …/g5wt/packages/orchestration/job_evidence.py`.
  - Each mutation was a single-occurrence replacement, reverted with `git checkout --` and then checked with an empty `git status --porcelain`.
  - control → `132 passed in 56.35s`, exit 0.
  - (a) `ctx.waiting_job_ids = list(ctx.job_ids[1:])` → `= []` (the run step runs every job) → `5 failed, 127 passed`, exit 1. Failing: `test_force_mission_yields_linked_jobs_runs_the_first_and_leaves_the_repo_untouched`, `test_without_no_ui_the_cockpit_opens_for_the_job_that_ran_and_reports_its_url`, `test_apply_with_force_mission_applies_the_job_that_ran_and_leaves_the_rest_waiting`, `test_apply_with_force_mission_on_the_stock_fake_applies_job_1_and_job_2_waits` (2a) and `test_without_apply_a_force_mission_walk_runs_job_1_and_prints_how_job_2_runs` (2b).
  - (b) the mirror call → `pass` → `2 failed, 130 passed`, exit 1. Failing: `test_the_json_cost_has_a_row_per_role_with_the_ledgers_own_numbers` and `test_a_job_whose_cost_mirror_failed_is_named_not_counted_as_zero`.
  - (c) `cs["builder_context"] = _builder_context_by_round(job)` → `= []` → `1 failed, 131 passed`, exit 1. Failing: `TestCompletedJobExport::test_context_strategy_carries_the_builders_context_per_task_and_round`.
  - The `remedy/job-*` branch count was 31 before and 31 after.
- C3a red check (in the checkout, before its commit): the guard reverted to `^T\d{3,}$` → both new `minted` tests failed (`2 failed, 93 deselected`). Restored.
- G6 (clean tree, HEAD == origin) runs after the push. It is in the round report.

## Authored-text proofs

All eight payloads were verified by sha256 before use. They were copied byte-exact to `.agent/authored/f268-r5-*`, and the post-copy comparisons print True (G1). The appends were built from `git show 994f045a:` bytes (C1) and `git show 718696e8:` bytes (C1b) plus the payload, never from a file being written. G1 proves the committed bytes.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | `718696e8` |
| C1b bookkeeping (ruling) | done | `9aba205d` |
| R-0968 | deviated | Repaired per D12, which amends D10 by ruling, not per D10. C2; red under G5 (a) |
| R-0969 | done | C2, with the guide correction |
| R-0807 F268 half | done | C3 (+ C3a). Red under G5 (b) and (c) |
| C4 handoff | done | This commit |

Landed: R-0968 — per DECISION F268 D12, a walk of two or more jobs runs job 1 only; the rest are listed in `waiting_job_ids`, and each gets a Next line, with real ids, to commit its predecessor's applied output and then `remedy job run <id>`. `--apply` applies job 1 and exits 0 on the stock fake provider, where every build writes the same file: `test_apply_with_force_mission_on_the_stock_fake_applies_job_1_and_job_2_waits`, and `test_without_apply_a_force_mission_walk_runs_job_1_and_prints_how_job_2_runs` for the path without `--apply`. Both are red when the run step runs every job (C2).
Landed: R-0969 — the `do.run` entry in `apps/cli/command_catalog.py` declares `may_mutate_repo=True`, pinned by `test_do_run_declares_repo_mutation_like_job_apply` in `tests/orchestration/test_do_run.py`, which also asserts it is equal to `job.apply`'s (C2).
Landed: R-0807's F268 half — `do` mirrors each job it runs into the F103 ledger and ends with measured tokens per role and a cost line, read through `token_ledger.query_cost(..., job_id=<id>, by="role")`. `--json` `cost` carries the same numbers and names any job whose mirror failed. `context_strategy.json` carries `builder_context`, one entry per task and round. Tests: `test_the_json_cost_has_a_row_per_role_with_the_ledgers_own_numbers`, `test_a_job_whose_cost_mirror_failed_is_named_not_counted_as_zero` and `test_context_strategy_carries_the_builders_context_per_task_and_round` (C3, C3a).

## Open findings

128 open by distinct id, derived with `.remedy-wt/f268-r4/count.py`. The ledger at HEAD holds 140 distinct `- R-nnnn —` registrations and 12 distinct `Done:` ids. Against round 4's 127, C1 registered three (R-0968, R-0969, R-0970) and booked two `Done:` lines (R-0967, R-0811). This round writes no `Done:` line and opens no finding.

## Deviations & assumptions

- **Commit sequence.** The block ordered C1–C4. The round ran C1, stop, C1b, C2 (amended), C3a, C3, C4:
  - The stop and C1b follow the reviewer's ruling; C2 follows D12, not D10.
  - C3a is an extra commit, not in the block, covered below.
  - C1 stayed local and unamended through the stop.
- **C3a repairs half of R-0912, an F273-owned finding, inside F268.** D11's mirror fails for every `do` job, because `job_evidence`'s task-id guard refused the minted ids `do`'s deterministic tasks carry. This was measured: `mirror_job_run_into_ledger` returned `ValueError: Unsafe task ID '215f0eeefa4f41a9'`, and `query_cost` read `ledger_exists=False`. So C3's cost test could not be met.
  - R-0912's own FIX clause allows "widen the guard"; `job_evidence.py` is in C3's change set and not on the do-not-touch list.
  - The shape accepted is exactly `[0-9a-f]{16}`. Every traversal case of the existing tests still raises.
  - R-0912's premise "a job made by the product's own flow is unaffected" no longer holds, since `do` makes such jobs.
  - What remains for its owner: the exit-with-message half; and the four other copies of `^T\d{3,}$` in `token_truth.py:36` (its `_task_ids` scan skips minted-id task runs; `token_ledger`'s backfill scan is unfiltered and unaffected), `missing_tests_gate.py`, `spec_compliance.py` and `scratch_file_guard.py`.
  - No `Done:` line is written. The reviewer decides whether R-0912 needs a note.
- **`builder_context` granularity.** D11 asks for the builder's reported input and cache-read tokens "for each task and round". The run record does not hold them per round:
  - Each round's `builder` dict carries only `tokens_used`.
  - Per-call `usage_actuals` stay in memory on `ProviderAttempt` and are written only as run-wide or per-role totals (`token_accounting.usage_actuals.by_role`, `pingpong_loop.py:4304-4434`).
  - Writing per-round figures would change the runner, which is outside the change set.
  - So each task-round entry carries `builder_tokens_used` (that round's own report) plus `task_builder_input_tokens` and `task_builder_cache_read_tokens`: the task run's builder totals, repeated on each of its rounds, and null where no builder call reported usage. `builder_context_note` says so in the file.
  - The fake provider reports `tokens_used=100` and no usage, so the test asserts 100 per round and null totals.
  - The reader is the task's own run record (`load_run`), the record `_write_task_run_evidence` exports; there is no parse of provider output.
- **Cost summation.** Per role and job, rows come straight from `query_cost`. Across jobs they are summed the way the ledger's `SUM` sums: None only when every value is None. The total cost is the sum of the role costs.
  - With one job, `cost_usd` equals `query_cost(...).total.cost_usd`, which the test asserts.
  - A job whose mirror failed contributes nothing and is named, with its error, in `mirror_failed_job_ids` and `mirror_errors`, and in a `Cost NOT recorded to the ledger for job <id>: <error>` text line.
  - The mirror runs after every `run_job`, whatever state the job ended in, as `_cmd_job_run` does.
- **Waiting-job Next lines name each job's predecessor.** For job 2 that is job 1, as ordered. For job 3 it is job 2: job 3 cannot run until job 2 is applied and committed, so naming job 1 there would be false. Test (2b) asserts job 2's exact line.
- **The ui step and the halt text.** With `--force-mission` and no `--no-ui`, the cockpit opens for job 1. The `--step-by-step` halt before job 1 still reads `(1 of <N jobs>)`, where N is the number of jobs in the walk.
- **`docs/guides/do-run-v1.md`** corrected in C2, per the ruling. It had no separate `may_mutate_repo` statement besides that one line.
- **Plan.** `.agent/plan.md` is the reviewer's `plan_b.md`, byte-exact. Its "Current Step" names round 5's work and was not rewritten to record completion, because G1 checks it byte-for-byte. `.agent/context.md` was not updated, because it is not in the change set.
- **Full suite** not run (amend0917-throughput).

## Next

Reviewer: review round 5 at this branch tip and book its verdict in the next round's first commit.

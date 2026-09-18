# Handoff — F268 remedy do: the one-command start · Round 1 (T001)

## Session

SESSION 1 of feature F268 · round 1 · rounds so far 1

## Range

Review of 8e075bbe..HEAD — branch `feature/f268-remedy-do`, cut from `main` at `8e075bbe`.

## Summary

F268 is claimed (STATUS `[~]`, live review re-headed, DECISIONs D1 to D4 appended) and T001
landed. `packages/orchestration/do_sequence.py` holds `DO_SEQUENCE` (init, study, plan,
shape, run, ui, apply), the step table and one walker. A bare `remedy do "<order>"` now walks
it: it registers the repo and writes its ignore entries (D2), studies once and records
`studied_at` / `studied_head` (D3), creates and plans the mission for the order, shapes ONE
job linked to the mission with `repo_path` = repo root, runs it on the chosen providers,
prints the real `remedy ui start` command unless `--no-ui`, and always stops before apply
(D4). `--json` carries `mission_id`, `job_ids`, `contract` (null, D1), `stopped_before_apply`
and `steps`. `--fixture-builder` is deleted (R-0933).

## Commits

### 12af9f4e F268 R1 C1: claim F268, re-head live review, land DECISIONs D1 to D4
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f268-r1-block.md` | +138 / -0 | Byte copy of the step block |
| `.agent/authored/f268-r1-context.md` | +43 / -0 | Byte copy of the payload |
| `.agent/authored/f268-r1-decisions.md` | +61 / -0 | Byte copy of the payload |
| `.agent/authored/f268-r1-live_review_head.md` | +26 / -0 | Byte copy of the payload |
| `.agent/authored/f268-r1-plan.md` | +31 / -0 | Byte copy of the payload |
| `.agent/authored/f268-r1-status_from.txt` | +1 / -0 | Byte copy of the payload |
| `.agent/authored/f268-r1-status_to.txt` | +1 / -0 | Byte copy of the payload |
| `.agent/context.md` | +29 / -53 | := context.md payload |
| `.agent/decisions.md` | +61 / -0 | Old bytes + DECISIONs F268 D1 to D4 (append) |
| `.agent/live_review.md` | +22 / -27 | Head payload + old bytes from `## Findings` to the end |
| `.agent/plan.md` | +22 / -15 | := plan.md payload |
| `docs/roadmap/STATUS.md` | +1 / -1 | F268 `[ ]` → `[~]` |

### 38351700 F268 R1 C2: shared repo ignore helpers and the study-once writer
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/commands/init_cmd.py` | +3 / -48 | The two ignore helpers leave; `_handle_init` imports them (behaviour unchanged) |
| `apps/cli/commands/study_cmd.py` | +8 / -1 | `study run` calls `record_study_pass` after a pass, for a registered project (D3) |
| `packages/orchestration/repo_ignore.py` | +57 / -0 | New: `ensure_ignore_entry`, `ignore_entries` (moved verbatim, D2) |
| `packages/orchestration/study.py` | +51 / -0 | `record_study_pass`: the one writer of `studied_at` / `studied_head` (D3) |
| `tests/cli/test_study_cmd.py` | +34 / -0 | `study run` writes the fields for a registered project, nothing when unscoped |
| `tests/orchestration/import_reachability_allowlist.txt` | +1 / -0 | `packages.orchestration.repo_ignore` (additive, see Deviations) |
| `tests/orchestration/test_study.py` | +69 / -0 | The writer: both fields saved, empty head outside git, unknown project writes nothing |

### affb365d F268 R1 C3a: move the golden-path job planning into do_sequence
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/commands/do_cmd.py` | +12 / -210 | The job-planning body of `_cmd_do_mission` leaves; the handler calls `plan_order_job` |
| `packages/orchestration/do_sequence.py` | +295 / -0 | `plan_order_job` / `OrderJobPlan` / `OrderJobPlanError`: the moved body (188 non-blank lines verbatim), plus `repo_path` on the job |
| `tests/orchestration/import_reachability_allowlist.txt` | +1 / -0 | `packages.orchestration.do_sequence` (additive) |

### 5e5c835c F268 R1 C3b: the do sequence as data, its step table and one walker
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/do_sequence.py` | +296 / -4 | `DO_SEQUENCE`, `DoContext`, `DoStepResult`, `walk_do_sequence`, the seven steps, `DO_STEP_TABLE` |
| `tests/orchestration/test_do_sequence.py` | +92 / -0 | The seven names in order; spy table called in order and nothing outside it; a stop or failure ends the walk |

### ef618eac F268 R1 C4: bare remedy do walks the sequence; provider flags reach the run
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/command_catalog.py` | +3 / -2 | `do.run`: `--builder-provider` (fake, claude, claude-cli, ollama; default None), new `--reviewer-provider` and `--yes`; `--fixture-builder` deleted |
| `apps/cli/commands/do_cmd.py` | +56 / -110 | `_cmd_do_order` walks the sequence; `_cmd_do_mission`, `_parse_builder_provider`, `_parse_fixture_builder` deleted |
| `apps/cli/grouped.py` | +8 / -5 | Bare route also accepts `--no-ui`, `--builder-provider`, `--reviewer-provider` (and `--flag=value`); `--fixture-builder` parser branch deleted |
| 12 pre-existing test files | see table below | Pinned behaviour changed by design |

### 70bcb43a F268 R1 C5: one test per do step boundary on the fake provider
| Path | +/- | Reason |
|------|-----|--------|
| `tests/cli/test_do_sequence_cli.py` | +173 / -0 | Tests (1) to (6) of the block, plus the R-0811 placeholder grep |

### (this commit) F268 R1 C6: handoff — round 1 T001
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This document (self-reference exception) |

### Pre-existing tests edited in C4, one line each
| File | +/- | Reason |
|------|-----|--------|
| `tests/cli/test_golden_path.py` | +102 / -95 | Bare `do` now runs its job: `_run_do` names the fake providers and `--no-ui`; `job_id` → `job_ids[0]`; "planned" → "completed"; the unregistered-repo test now expects registration (D2), not exit 3; the in-process intake tests call the moved `plan_order_job`; the three stop tests plan an unrun job, since `job stop` refuses a completed one; the smoke and short-id tests pin that refusal |
| `tests/cli/test_plan_approval.py` | +30 / -55 | Seven in-process `_cmd_do_mission` calls → `plan_order_job(...).to_json()` (same keys asserted); the parse failure expects `OrderJobPlanError`; the subprocess label test names the fake providers and reads the shape step |
| `tests/cli/test_decision_answers.py` | +7 / -7 | The unattended `--yes` helper calls `plan_order_job(yes=True)`; the unused `StringIO` import is dropped |
| `tests/cli/test_mission_cmd.py` | +39 / -19 | "do leaves no mission behind" is inverted by D4: `do` creates exactly one mission, carrying the order and linking its job; the `--yes` planning path still creates none |
| `tests/cli/test_scoped_listings.py` | +6 / -3 | `_create_job` names the fake providers and reads `job_ids[0]` |
| `tests/cli/test_job_commands.py` | +3 / -2 | `--fixture-builder` → `--builder-provider fake` in the all-flags parse test |
| `tests/test_cli_execution_loop_closure.py` | +29 / -32 | The five `--fixture-builder` parse tests → the deleted flag exits 2, both provider flags parse, the bare rewrite passes them, an invalid provider exits 2 |
| `tests/cli/test_do_cmd_summary.py` | +0 / -25 | `TestFixtureBuilderParse` removed together with `_parse_fixture_builder` (the replacement guard is in the file above) |
| `tests/test_repair_context_reviewer_memory.py` | +0 / -8 | `test_parse_fixture_builder_repair_loop` removed together with the parser; the package-level repair-loop tests stay |
| `tests/orchestration/test_provider_mode.py` | +14 / -11 | `TestBuilderProviderParse` now checks the new choices through `_validate_role_override`; `none`/`fixture` exit 2 |
| `tests/docs/test_vocabulary.py` | +2 / -1 | The `do.run --fixture-builder` synonym exemption leaves with the flag |
| `tests/test_install_smoke.py` | +3 / -1 | The opt-in smoke's `do` names the fake providers and `--no-ui` |

## External actions

- `git worktree add --detach .remedy-wt/f268-r1-g5 HEAD` at `70bcb43a` for G5, removed with `git worktree remove --force` after the three mutations; `git worktree list` then showed only the main checkout.
- `git push -u origin feature/f268-remedy-do` after this commit (first push of the branch, no force). The outcome is in the round report.
- No PR create, edit or merge.

## Verification

All gates run at `70bcb43a` (C5). C6 changes only this file.

- G1 transport + state: all six payload sha256 matched (`True` ×6). Block digest `62d22de32ff8c5027f9fa72699a8756e4f8d81fd7af552bf4d63bb3a0a316eea`. `live_review re-head True`, `decisions append True` (both against `git show 8e075bbe:<path>`). `cmp .agent/plan.md …/plan.md` → `REAL_EXIT=0`; `cmp .agent/context.md …/context.md` → `REAL_EXIT=0`.
- G2 `python3 -m pytest -q -p no:cacheprovider` on the block's 16 files plus `tests/cli/test_do_cmd_summary.py tests/test_repair_context_reviewer_memory.py tests/orchestration/test_provider_mode.py tests/docs/test_vocabulary.py tests/test_install_smoke.py` → `631 passed, 2 skipped in 156.44s (0:02:36)`, `REAL_EXIT=0`.
- G3 `python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/orchestration/test_roadmap_index.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py` → `457 passed in 6.63s`, `REAL_EXIT=0`.
- G4 `python3 -m ruff check` over the 24 `.py` files C2 to C5 touched (`git diff --name-only 12af9f4e..HEAD -- "*.py"`) → `All checks passed!`, `REAL_EXIT=0`.
- G5 one worktree `.remedy-wt/f268-r1-g5` at `70bcb43a`, `python3 -B -m pytest` from its root, `__pycache__` purged before each run. Each run first printed `module: /home/decodeux/Repos/remedy/.remedy-wt/f268-r1-g5/packages/orchestration/do_sequence.py` (and `…/study.py`, `…/apps/cli/grouped.py`).
  - control (unmutated), `tests/orchestration/test_do_sequence.py tests/cli/test_do_sequence_cli.py` → `19 passed in 11.56s`, `REAL_EXIT=0`
  - (a) `for name in reversed(DO_SEQUENCE):` → `8 failed, 4 passed in 0.23s`, `REAL_EXIT=1`: `test_the_walker_calls_the_table_in_sequence_order_and_nothing_outside_it`, `test_a_skipped_step_does_not_end_the_walk`, `test_a_step_that_stops_or_fails_ends_the_walk[init-stopped|init-failed|shape-stopped|shape-failed|run-stopped|run-failed]`; reverted by `git checkout -- packages/orchestration/do_sequence.py`
  - (b) `repo_path=ctx.repo_root,` deleted from the shape step → `1 failed in 0.44s`, `REAL_EXIT=1`: `test_do_sequence_cli.py::test_job_apply_accepts_the_job_do_ran` (`Error: run failed: job … has no target repository; nothing was run`); reverted
  - (c) `return None` as the first statement of `record_study_pass` → `1 failed in 1.69s`, `REAL_EXIT=1`: `test_do_sequence_cli.py::test_init_to_study_registers_studies_once_and_records_it`; reverted
  - `remedy/job-*` branch count 31 before and 31 after.
- G6 (clean tree, HEAD == origin) runs after the push. It is in the round report.

## Authored-text proofs

The seven payloads were verified by sha256 before use and copied byte-exact to
`.agent/authored/f268-r1-*` (the post-copy digests are identical). `.agent/plan.md` and
`.agent/context.md` pass `cmp` against their payloads. The live-review re-head and the
decisions append are byte-exact per G1. The STATUS line replacement matched exactly one line.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| T001 | done | C2 to C5 |
| R-0897 | done | Landed, see below; the ledger `Done:` is the reviewer's |
| R-0933 | done | Landed for bare `do`; one residual in Deviations |
| R-0811 | done | Landed for `do`'s output; `job show` is not touched this round |

Landed: R-0897 — every run bare `remedy do` starts belongs to a job linked to its mission with `repo_path` = repo root, and `job_apply.apply_job(<job>, <repo>, approve=True)` accepts it (`status == "applied"`), proved by `tests/cli/test_do_sequence_cli.py::test_job_apply_accepts_the_job_do_ran` (C3a/C3b/C5).
Landed: R-0933 — `--builder-provider` and the new `--reviewer-provider` reach `run_job` from bare `do`, and the job records them as `("fake", "cli")` in `execution_config`, proved by `test_shape_to_run_completes_on_the_named_fake_providers`; `--fixture-builder` is deleted with its parser and reads (C4/C5).
Landed: R-0811 — bare `do` inside a git repository attaches that repository with no flag, and every `Next:` line carries the real job id and path, with no `<job_id>`/`<path>`/`<mission>` placeholder; proved by `test_next_lines_carry_real_ids_and_paths_never_placeholders` (C3b/C4/C5).

## Open findings

128 open BY DISTINCT ID, unchanged (this round writes no `Done:` line and opens no finding).

## Deviations & assumptions

- Commit sequence: C3 was SPLIT into C3a (the pure move, 308 insertions of which 188 non-blank lines are verbatim from `_cmd_do_mission`) and C3b (the sequence, steps and unit tests, 388 insertions). As one commit it came to about 505 inserted lines excluding the move, against constraint 1's "< 500 excluding pure moves". There are six commits plus this handoff, not five.
- Allowlist: the two new modules were inserted additively, in sorted position. The generator's full output (header + `sorted(reachable_closure())`) would ALSO drop `agent_run_trace` and `redaction_patterns` and re-sort `job_plan` and `study`, which the base file already carries unsorted. The base allowlist is therefore not its own generator's output, and that is left to a round that owns it.
- Added and not named by the block: the run step refuses a job with an empty `repo_path`. Without that guard `run_job` falls back to a staging COPY of the process's working directory. The guard is also what makes mutation (b) observable at test (6).
- C5 has a seventh test beyond the block's six: the R-0811 placeholder grep. An autouse tripwire in the same file fails any test that reaches `make_provider_call_fn`, `make_structured_call_fn` or `study_call_fn`.
- R-0933 residual: an EXPLICIT `do run "<goal>"` (non-bare, the autorun path the block leaves untouched) now validates `--builder-provider` / `--reviewer-provider` against the new choices but still does not read them.
- Surfaces outside the change set still name the deleted flag or the retired `fixture`/`none` values. None was edited. `tests/cli/test_advertised_commands.py` is green over them.
  - `scripts/remedy_smoke.sh:1928`: section 12ao runs `remedy do … --fixture-builder repair-loop`, which now exits 2. The script is operator-run, not in CI.
  - `apps/cli/commands/dev.py:201`: the `dev status` hint.
  - `docs/guides/autocoder-usage.md`: `--builder-provider fixture` and "Legacy `--fixture-builder`".
  - `docs/system/first-perfect-job-demo-v0.md`.
- `do.run` still declares `may_execute_commands=False`, which is pinned "in v1" by `tests/orchestration/test_do_run.py`. Bare `do` now runs a job, so the flag understates it. Left untouched.
- `do`'s run step calls `run_job` only. It does not mirror the run's cost into the ledger as `job run` does. The block scoped the step to `run_job`, and the cost truth belongs with R-0807.
- A `do` outside any git repository now fails at init with exit 1 ("… is not a git repository"). The old golden path exited 3 ("No project registered").
- C1 working-tree slip, caught before commit: my first write of `.agent/decisions.md` truncated it (the file was opened for writing before it was read). It was rebuilt from `git show 8e075bbe:.agent/decisions.md` + payload, and G1's byte check proves the committed bytes.
- Full suite not run (amend0917-throughput).

## Next

Reviewer: review round 1 (T001) at this branch tip and book its verdict in the next round's first commit.

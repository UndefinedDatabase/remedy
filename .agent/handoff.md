# Handoff — F268 remedy do: the one-command start · Round 3 (T003 + R-0964/R-0966/R-0811)

## Session

SESSION 1 of feature F268 · round 3 · rounds so far 3

## Range

Review of 57ca6293..HEAD — branch `feature/f268-remedy-do`.

## Summary

C1 books round 2's verdict and R-0966, adds DECISION F268 D8, and replaces the plan.

C2 makes three repairs:
- R-0964's residue: the demo doc, the `autorun.py` comment and the `dev` hint.
- R-0966: the extractor now recognises extension-less file names and skips tokens inside URLs.
- R-0811's `job show` half: both `attach-repo` tips print the real job id. They add the project's repository when the job has one, and otherwise a sentence saying what to pass.

C3 lands T003 per D8:
- `--step-by-step` halts after every step that did work and before each job in the run step. At each halt it reads one line through `DoContext.read_line`, which the CLI sets to `input`. `q` or end of input stops the walk and calls `safe_points.request_stop(..., source="do")` for every job of the walk.
- `--plan-only` ends the walk after shape. The run step reports it stopped, with the reason `--plan-only`.
- Text output lists every job's tasks with their deliverables after the shape line. `--json` adds `jobs` and `mission_plan_path`.

C4 adds the five acceptance tests.

## Commits

### bd9f5e97 F268 R3 C1: book round 2's verdict, R-0966 and DECISION F268 D8
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f268-r3-block.md` | +114 / -0 | Byte copy of the step block |
| `.agent/authored/f268-r3-decisions.md` | +19 / -0 | Byte copy of the payload |
| `.agent/authored/f268-r3-ledger.md` | +12 / -0 | Byte copy of the payload |
| `.agent/authored/f268-r3-plan.md` | +29 / -0 | Byte copy of the payload |
| `.agent/decisions.md` | +19 / -0 | `git show 57ca6293:` bytes + decisions.md (append) |
| `.agent/live_review.md` | +12 / -0 | `git show 57ca6293:` bytes + ledger.md (append) |
| `.agent/plan.md` | +10 / -10 | := plan.md payload |

### bb422e99 F268 R3 C2: repair R-0964's residue, R-0966 and R-0811's job show half
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/commands/dev.py` | +1 / -1 | R-0964: the hint for bare `do` now reads "plan and run a job, stop before apply", not "repair E2E" |
| `docs/system/first-perfect-job-demo-v0.md` | +1 / -2 | R-0964: both `--fixture-builder true` uses dropped (`do run`'s `run_do` path is fixture-only) |
| `packages/orchestration/autonomy_readiness.py` | +3 / -1 | R-0811: the level-1 `attached_repo` tip is `job_attach_repo_tip(job)`, computed only when the signal is missing |
| `packages/orchestration/autorun.py` | +1 / -1 | R-0964: the comment names the parameters, not the deleted flag |
| `packages/orchestration/stop_reasons.py` | +30 / -1 | R-0811: new `job_attach_repo_tip` and `_job_project_repo_path` (job `project_id`, else `metadata["project_id"]` → `load_project` → `canonical_repo_path`); `sr:derived_no_repo` uses the tip |
| `packages/orchestration/task_deliverables.py` | +32 / -6 | R-0966: `EXTENSIONLESS_DELIVERABLE_NAMES` (named constant), `_EXTENSIONLESS_TOKEN_RE`, `_URL_RE` (a scheme or `www.`); both token regexes are merged in order of appearance; tokens inside a URL span are skipped; docstring updated |
| `tests/cli/test_open_decisions_view.py` | +3 / -1 | Pinned placeholder moved (pre-existing test table) |
| `tests/orchestration/test_stop_reasons.py` | +45 / -0 | R-0811: one test with a project (exact command), one without (sentence); both check the job id is there and no `<[a-z_]+>` is |
| `tests/orchestration/test_task_deliverables.py` | +25 / -0 | R-0966: a parametrized test per extension-less name, directory and order kept, three URL cases |
| `tests/test_autonomy_readiness.py` | +39 / -0 | R-0811: two tests over the rendered `summarize_readiness` line (with a project and without) |

### e515bca7 F268 R3 C3: --step-by-step and --plan-only, and every job's tasks in do's output (DECISION F268 D8)
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/command_catalog.py` | +2 / -0 | `do.run`: `--step-by-step`, `--plan-only` (flags). Their descriptions use no binding word, so the vocabulary guard passes |
| `apps/cli/commands/do_cmd.py` | +30 / -4 | `_cmd_do_order` / `_cmd_do` / the dispatch entry pass both flags, and `read_line=input` is looked up at call time. `--json` gains `mission_plan_path` and `jobs`. Text output prints one line per task after the shape line |
| `apps/cli/grouped.py` | +2 / -1 | Both flags join `_BARE_ALLOWED` |
| `packages/orchestration/do_sequence.py` | +99 / -3 | `DoContext` gains `step_by_step`, `plan_only`, `read_line`, `halt_reason` and `mission_plan_path`. `do_step_by_step_halt` added, called by the walker after each `done` step and by the run step before each job. `--plan-only` branch in `_step_run`. `do_job_task_listing` added |

### 1cde5fdb F268 R3 C4: acceptance tests for --step-by-step, --plan-only and the task listing
| Path | +/- | Reason |
|------|-----|--------|
| `tests/cli/test_do_sequence_cli.py` | +137 / -2 | Block tests (1) to (5). They use the same fixture and tripwire as rounds 1 and 2, and the reader is `builtins.input` monkeypatched. The module docstring now names T003 |

### (this commit) F268 R3 C5: handoff — round 3 T003
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This document (self-reference exception) |

### Pre-existing tests edited, one line each
| File | Commit | Reason |
|------|--------|--------|
| `tests/cli/test_open_decisions_view.py` | C2 | `test_the_block_is_queue_wide_not_task_decision_only` pinned `next_safe_action == "remedy job attach-repo <job_id> <path>"`, the placeholder R-0811 removes. It now asserts that the value starts with `remedy job attach-repo <real job id> ` and holds no `<` |
| `tests/orchestration/test_stop_reasons.py`, `tests/test_autonomy_readiness.py`, `tests/orchestration/test_task_deliverables.py`, `tests/cli/test_do_sequence_cli.py` | C2, C4 | New tests appended. No existing assertion changed |

## External actions

- G5: `git worktree add --detach .remedy-wt/f268-r3-g5 HEAD` at `1cde5fdb`, removed with `git worktree remove` afterwards. `git worktree list` showed only the main checkout before and after.
- `git push` after this commit (no force). The outcome and G6 are in the round report.
- No PR create, edit or merge.

## Verification

All runs at `1cde5fdb` (C4). C5 changes only this file.

- G1 transport + state: the `ledger`, `decisions`, `plan` and `block` payload digests all matched (`True`), and so did their `.agent/authored/f268-r3-*` copies. Block digest `be20fd3ea5648ed0915dca61008dc20b634780251c0a3a70e81bbe37db79135f`. Both byte checks printed `True`: `.agent/live_review.md` = `git show 57ca6293:.agent/live_review.md` + ledger.md, and `.agent/decisions.md` = `git show 57ca6293:.agent/decisions.md` + decisions.md. `cmp .agent/plan.md .remedy-wt/f268-r3/plan.md` → `REAL_EXIT=0`.
- G2 `python3 -m pytest -q -p no:cacheprovider` over the block's 11 files, plus `tests/orchestration/test_stop_reasons.py`, `tests/test_autonomy_readiness.py` (the two modules' test files) and `tests/cli/test_open_decisions_view.py` (edited) → `495 passed in 101.14s (0:01:41)`, `REAL_EXIT=0`. Before C2 was committed, a wider sweep also ran: every test file naming `stop_reasons`, `autonomy_readiness` or `next_safe_action` (41 files), `-n 4`, read `1472 passed, 6 skipped`, exit 0.
- G3 `python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/orchestration/test_roadmap_index.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py` → `457 passed in 6.74s`, `REAL_EXIT=0`.
- G4 `python3 -m ruff check` over the 14 `.py` files that `git diff --name-only 57ca6293 HEAD -- "*.py"` names → `All checks passed!`, `REAL_EXIT=0`.
- G5: one worktree, `.remedy-wt/f268-r3-g5`, at `1cde5fdb`. Every run went from the worktree root with `python3 -B -m pytest -q -p no:cacheprovider -rf tests/cli/test_do_sequence_cli.py`. `__pycache__` was purged before each run, and each run first printed the imported paths `…/.remedy-wt/f268-r3-g5/packages/orchestration/do_sequence.py` and `…/.remedy-wt/f268-r3-g5/apps/cli/commands/do_cmd.py`. After each mutation, `git checkout -- <path>` reverted it and a clean `git status` was asserted.
  - control (unmutated) → `18 passed in 17.01s`, `REAL_EXIT=0`
  - (a) in `do_step_by_step_halt`, `answer = ctx.read_line() if ctx.read_line is not None else None` → `return True` → `3 failed, 15 passed in 18.99s`, `REAL_EXIT=1`: `test_step_by_step_halts_at_least_three_times_and_completes_like_a_plain_run`, `test_no_provider_call_happens_while_a_halt_waits`, `test_q_at_the_first_halt_after_shape_runs_no_job_and_asks_every_job_to_stop`
  - (b) `request_stop(job_id, reason=reason, source="do")` → `pass` → `1 failed, 17 passed in 15.97s`, `REAL_EXIT=1`: `test_q_at_the_first_halt_after_shape_runs_no_job_and_asks_every_job_to_stop`
  - (c) in the `do.run` dispatch entry, `plan_only=bool(getattr(args, "plan_only", False))` → `plan_only=False` → `1 failed, 17 passed in 17.65s`, `REAL_EXIT=1`: `test_plan_only_writes_the_mission_plan_plans_the_jobs_and_runs_none`
  - `remedy/job-*` branch count: 31 before and 31 after.
- G6 (clean tree, HEAD == origin) runs after the push. It is in the round report.

## Authored-text proofs

All four files (`ledger.md`, `decisions.md`, `plan.md`, `block.md`) were verified by sha256 before use. They were copied byte-exact to `.agent/authored/f268-r3-*`, and the post-copy digests are identical. The two appends were built from `git show 57ca6293:<path>` bytes plus the payload, never by re-reading a file being written. G1's byte checks and `cmp` prove the committed bytes.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | |
| R-0964 residue | done | C2 |
| R-0966 | done | C2; the URL example is corrected in Deviations |
| R-0811 (`job show` half) | done | C2: the two tips the block names. Other placeholder tips remain, see Deviations |
| T003 `--step-by-step` / `--plan-only` | done | C3, C4 |
| Task listing in `do`'s output | done | C3, C4 test (5) |

Landed: R-0964 — no remaining surface the round 2 gate named still shows a rejected invocation or the deleted flag. `docs/system/first-perfect-job-demo-v0.md`'s two `do run` commands lost `--fixture-builder true`. The comment in `autorun.py` names the parameters rather than `--fixture-builder`, and the `dev status` hint describes bare `do` as "plan and run a job, stop before apply" (C2).
Landed: R-0966 — `extract_order_deliverables` recognises the names in `EXTENSIONLESS_DELIVERABLE_NAMES` (`Makefile`, `Dockerfile`, `LICENSE` and others), optionally under a directory, and skips every token inside a URL: one with a scheme, or one starting `www.`. `tests/orchestration/test_task_deliverables.py` has a test per name and three URL cases. At `57ca6293`, the name tests and two of the URL cases read the base extractor's wrong answer (C2).
Landed: R-0811 (`job show` half) — `sr:derived_no_repo` and the readiness `attached_repo` tip print `remedy job attach-repo <real job id> <project's canonical_repo_path>`. When the job has no project with a path, they print `remedy job attach-repo <real job id> followed by the path of the repository this job should change`. Four tests assert the real id and that no `<[a-z_]+>` survives. The `job show` status test now asserts the same (C2).

## Open findings

128 open BY DISTINCT ID, derived: the ledger at HEAD holds 136 distinct `- R-nnnn —` registrations and 8 distinct `Done:` ids. The same derivation at `57ca6293` reads 131, matching round 2's count. C1 booked R-0966 and four `Done:` lines (R-0963, R-0965, R-0808, R-0897). This round writes no `Done:` line and opens no finding.

## Deviations & assumptions

- Commit sequence: C1, C2, C3, C4, C5, as the block orders. No extra commit.
- R-0966's stated URL example does not reproduce. Measured at `57ca6293`: `extract_order_deliverables("See https://example.com/docs and write notes.md")` returns `['notes.md']`, because `_PATH_TOKEN_RE`'s lookbehind already rejects a token that follows `/`. Two URL forms do leak at base:
  - a file in a query string: `https://example.com/download?file=report.pdf` → `report.pdf`
  - a URL without a scheme: `www.example.com/page` → `www.example`

  The tests use those two as the discriminating cases, and keep the ledger's example as a control that passes at base. The ledger line is the reviewer's record and was not edited.
- R-0811 scope: only the two tips the block names were changed. Other placeholder next-actions still exist in these files:
  - `stop_reasons.py`: `remedy test run <job_id>` and `remedy patch approve <job_id> <intent_id>`
  - `autonomy_readiness.py`: `remedy do run "<goal>"` and several `<job_id>` tips
  - outside the change set: `self_dogfood_execution.py:493` and `test_execution_service.py:625,632` still print `attach-repo {id} <path>` / `<repo_path>`

  That is why the readiness tests check the rendered `attach-repo` line, not the whole summary.
- The tip helper `job_attach_repo_tip` lives in `stop_reasons.py`, and `autonomy_readiness.py` imports it lazily. It is one function for both tips, and `project_registry.py` is outside the change set. It calls `load_project`, which runs the existing legacy-record migration.
- D8 halt placement, read literally:
  - The walker halts after every `done` step, and the run step halts before each job. After shape there are therefore two back-to-back halts: "next: the run step", then "next: run job X (1 of N)".
  - Skipped steps (study on a studied repo, ui with `--no-ui`) do not halt.
  - Any line other than `q` (case-insensitive, trimmed) continues. D8 names only the empty line.
  - A `read_line` of `None` counts as end of input and stops the walk. Library callers get no hidden stdin read.
- Stop reporting: when `q` comes at a walker halt, the step that did not run is added to `results` as `stopped` with detail `not run: stopped by 'q' at the --step-by-step halt before the <step> step; a stop was requested for job(s) …`, so `--json` shows why the walk ended. When `q` comes inside the run step, the run step itself reports `stopped` with the same reason. Per the block's wording, `request_stop` goes to every job of the walk, including jobs that already completed. A `StopControlError` or `OSError` from it is caught and named in the reason instead of crashing the walk.
- Halt text goes to stderr, so `--json` stdout stays parseable.
- `--plan-only` also adds one `Next: remedy job run <id>[ provider flags]` line per job. Its run detail reads `--plan-only: no job was run; N job(s) planned, mission plan: <path>`.
- `--step-by-step` and `--plan-only` act only on the bare route (`_BARE_ALLOWED`). `remedy do run "<goal>" --plan-only` stays on the autorun path, which ignores them, as it does the force flags.
- Test (2): the reader reads the provider counter on entry and on exit. Because the reader is synchronous, the two are equal by construction. To show the counter is live, the test also asserts that the run made calls and that the last halt saw more than the first.
- Test (3) picks "the first halt after shape" by state: the reader answers `q` once `list_job_plans()` is non-empty. It also asserts that this was the fourth halt, with init, study, plan and shape each having done work. It runs with `--force-mission`, so "every job" means two or more.
- `jobs` in `--json` is `[]` when the walk ended before shape. A task without a recorded deliverable prints `(none)` in text output (none does on the deterministic path).
- `.agent/context.md` was not updated; it is not in the change set.
- Full suite not run (amend0917-throughput).

## Next

Reviewer: review round 3 at this branch tip and book its verdict in the next round's first commit.

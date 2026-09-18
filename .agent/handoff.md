# Handoff — F268 remedy do: the one-command start · Round 4 (T004 + R-0967/R-0811)

## Session

SESSION 1 of feature F268 · round 4 · rounds so far 4

## Range

Review of f831d374..HEAD — branch `feature/f268-remedy-do`.

## Summary

C1 books round 3's verdict, the `Done:` lines for R-0964 and R-0966, the registration of R-0967, and DECISION F268 D9. It also replaces the plan.

C2 makes two repairs:
- R-0967: a test in `tests/cli/test_do_sequence_cli.py` whose reader raises `EOFError` at a halt. It asserts that the walk stopped there, that no job ran and no provider was called, and that every job of the walk has a stop request.
- R-0811 remainder: every tip in `stop_reasons.py` and `autonomy_readiness.py` now names the real job id. The approve tip also names each real intent id, and no tip prints an angle-bracket placeholder or `"<goal>"`. `tasks_defined` is now `remedy job plan <real job id>`.

C3 lands T004 per D9:
- The ui step opens the cockpit for the last job through `DoContext.ui_launcher`. The CLI passes `launch_do_cockpit`, which spawns `sys.executable -m apps.cli.grouped ui start <job id> --port 0 --info-file <data root>/ui/sessions/do-<job id>.json` with `start_new_session=True` and output to `<data root>/ui/do_logs/<job id>.log`. It then waits up to 15 s for the info file. The step reports the URL and `remedy ui stop`. A launch that does not come up is `skipped`, with the reason and `remedy ui start <job id>`.
- `--apply`: the apply step calls `apply_job(<job id>, <repo root>, approve=True)` for each job in order. The first job whose status is not `applied` fails the walk, naming the job, the status and the reason. On success, `stopped_before_apply` is false.
- `--contract`, `--commit`, `--commit-auto`, `--commit-with-history` and `--push` are declared on `do.run` and are on the bare-route allow-list (`--contract` and `--commit` are also in the valued set). Each exits 2 before any step with `<flag> is not yet available; F269|F270 brings it`. `--with-history` does not exist.

C4 adds the acceptance tests (1) to (5), plus one test that `--with-history` is rejected.

## Commits

### e151e8bd F268 R4 C1: book round 3's verdict, R-0967 and DECISION F268 D9
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f268-r4-block.md` | +115 / -0 | Byte copy of the step block |
| `.agent/authored/f268-r4-decisions.md` | +22 / -0 | Byte copy of the payload |
| `.agent/authored/f268-r4-ledger.md` | +8 / -0 | Byte copy of the payload |
| `.agent/authored/f268-r4-plan.md` | +29 / -0 | Byte copy of the payload |
| `.agent/decisions.md` | +22 / -0 | `git show f831d374:` bytes + decisions.md (append) |
| `.agent/live_review.md` | +8 / -0 | `git show f831d374:` bytes + ledger.md (append) |
| `.agent/plan.md` | +11 / -11 | := plan.md payload |

### 6b1e1254 F268 R4 C2: repair R-0967 and R-0811's remaining placeholder tips
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/autonomy_readiness.py` | +9 / -6 | R-0811: `job_id = str(job.job_id)` in `_assess_level`. Changed tips: `tasks_defined` → `remedy job plan {job_id}`, the two `job permit` tips, `test discover`, `dev agent-loop` and `decision list` now carry the real id |
| `packages/orchestration/stop_reasons.py` | +16 / -3 | R-0811: new `_patch_approve_tips` (one `remedy patch approve {job_id} {intent_id}` per distinct intent id in the events; an event without an id adds `remedy patch list {job_id} names the intent ids to approve`). `remedy test run {job_id}`. The two plain sentences now name the job, and the dirty-repo sentence also names its target path |
| `tests/cli/test_do_sequence_cli.py` | +45 / -0 | R-0967: parametrized test, end of input at the first halt and at the first halt after shape |
| `tests/orchestration/test_stop_reasons.py` | +44 / -2 | R-0811: the two round 3 tests now check every derived next action, and there is a new all-four-reasons test (6 actions, no `<[a-z_]+>`, real job id in each, exact approve tips) |
| `tests/test_autonomy_readiness.py` | +24 / -2 | R-0811: the two round 3 tests check the whole summary, and there is a new test over the summary and all 7 level tips |

### 66d62854 F268 R4 C3: the detached cockpit, --apply, and the F269/F270 flags refusing as not yet available (DECISION F268 D9)
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/command_catalog.py` | +6 / -0 | `do.run`: `--apply`, `--commit-auto`, `--commit-with-history` and `--push` (flags); `--contract` and `--commit` (valued). Descriptions pass the vocabulary guard (`--apply` uses "job" with "mission", and avoids "in order", which would count as Order) |
| `apps/cli/commands/do_cmd.py` | +51 / -2 | `_DO_FLAGS_NOT_YET_AVAILABLE` table and `_refuse_do_flags_not_yet_available`, called first in `_cmd_do`. `apply` is threaded through to `DoContext`, with `ui_launcher=launch_do_cockpit`. The dispatch entry reads all six flags |
| `apps/cli/grouped.py` | +5 / -2 | All six flags are in `_BARE_ALLOWED`; `--contract` and `--commit` are also in `_BARE_VALUED` |
| `packages/orchestration/do_sequence.py` | +129 / -13 | `DoContext.apply` and `ui_launcher`. New `DO_COCKPIT_WAIT_SECONDS`, `DO_COCKPIT_STOP_COMMAND`, `DoCockpitLaunchError`, `do_cockpit_argv`, `do_cockpit_paths` and `launch_do_cockpit`. `_step_ui` and `_step_apply` are rewritten; the module docstring is updated |

### 2751135f F268 R4 C4: acceptance tests for the detached cockpit, --apply and the flags not yet available
| Path | +/- | Reason |
|------|-----|--------|
| `tests/cli/test_do_sequence_cli.py` | +234 / -0 | Block tests (1) to (5), plus `test_the_old_name_with_history_is_never_created`. Same fixture and tripwire as rounds 1 to 3; the launcher is replaced by monkeypatching `packages.orchestration.do_sequence.launch_do_cockpit` |

### (this commit) F268 R4 C5: handoff — round 4 T004
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This document (self-reference exception) |

### Pre-existing tests edited, one line each
| File | Commit | Reason |
|------|--------|--------|
| `tests/orchestration/test_stop_reasons.py` | C2 | In both round 3 no-repo tests, the placeholder check on the one `attach-repo` tip becomes a check over every derived next action (no `<[a-z_]+>`, real job id). This widens the check, as the block orders |
| `tests/test_autonomy_readiness.py` | C2 | In both `TestAttachRepoTip` tests, the placeholder check moves from the one `attach-repo` line to the whole rendered summary. The line's exact-text assertions are kept |
| `tests/cli/test_do_sequence_cli.py` | C2, C4 | New tests appended. No existing assertion changed |

## External actions

- Probes, not tests, run from `.remedy-wt/f268-r4/` with a scratch data root under it, deleted afterwards:
  - `probe_launch.py` called the real `launch_do_cockpit` for a saved job, through its `spawn` parameter with `--no-open` appended so that no browser opened. Output: a URL `http://127.0.0.1:46389/?job=…&token=…`. `ui status` showed `[RUNNING] job=… pid=2958701`, `ui stop` printed `Stopped 1 session(s).`, and `ps -p 2958701` then exited 1.
  - `probe_apply.py` ran `remedy do … --apply` as a subprocess on fixture repositories.
- G5: `git worktree add --detach .remedy-wt/f268-r4-g5 HEAD` at `2751135f`, removed with `git worktree remove --force`. `git worktree list` showed only the main checkout before and after.
- C2 was amended once before any push (see Deviations). No force-push.
- `git push` after this commit (no force). The outcome and G6 are in the round report.
- No PR create, edit or merge.

## Verification

All runs at `2751135f` (C4). C5 changes only this file.

- G1 transport + state: `ledger`, `decisions`, `plan` and `block` each printed `scratch True authored True`. Block digest `3a80270fed2db1fa0131ba0fd85531888ab049c3c32c4153c869f4c42e2890f2`. Both byte checks printed True (`live_review append True`, `decisions append True`), with `PY_EXIT=0`. `cmp .agent/plan.md .remedy-wt/f268-r4/plan.md` → `CMP_EXIT=0`.
- G2 `python3 -m pytest -q -p no:cacheprovider` over the block's 13 files → `473 passed, 6 skipped in 72.36s (0:01:12)`, `REAL_EXIT=0`. That set already includes every test file this round edited.
  - Before C2 was committed, a wider sweep ran every test file that names `derive_stop_reasons`, `assess_job_readiness`, `summarize_readiness`, `guidance`, `project_brain`, `decision_queue`, `autonomy_loop` or `memory_learn` (50 files): `2748 passed, 11 skipped`.
  - Before C4, a probe made `launch_do_cockpit` raise `AssertionError` and ran the 14 test files that reach the `do` walk: `452 passed, 1 skipped`. No existing test reaches the real launcher. The subprocess tests either pass `--no-ui` (`test_golden_path.py`, `test_install_smoke.py`) or take the non-bare path (`test_do_runtime.py`).
- G3 `python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/orchestration/test_roadmap_index.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py` → `457 passed in 6.71s`, `REAL_EXIT=0`.
- G4 `python3 -m ruff check` over the nine `.py` files C2 to C4 touched (`stop_reasons.py`, `autonomy_readiness.py`, `do_sequence.py`, `do_cmd.py`, `command_catalog.py`, `grouped.py`, `test_stop_reasons.py`, `test_autonomy_readiness.py`, `test_do_sequence_cli.py`) → `All checks passed!`, `RUFF_EXIT=0`.
- G5: one worktree, `.remedy-wt/f268-r4-g5`, at `2751135f`, driven by `.remedy-wt/f268-r4/g5.sh`. Every run went from the worktree root with `python3 -B -m pytest -q -p no:cacheprovider tests/cli/test_do_sequence_cli.py`. `__pycache__` was purged before each run, and each run first printed `IMPORTED …/.remedy-wt/f268-r4-g5/packages/orchestration/do_sequence.py` and `IMPORTED …/.remedy-wt/f268-r4-g5/apps/cli/commands/do_cmd.py`. Each mutation was a single-occurrence replacement, reverted with `git checkout -- <path>`, after which `git status --porcelain` printed nothing.
  - control (unmutated) → `32 passed in 26.35s`, `EXIT=0`
  - (a) in `do_step_by_step_halt`, `except EOFError: answer = None` → `answer = ""` → `2 failed, 30 passed in 28.73s`, `EXIT=1`: `test_end_of_input_at_a_halt_stops_the_walk_runs_no_job_and_asks_every_job_to_stop[the-first-halt]` and `[the-first-halt-after-shape]`
  - (b) in `_step_apply`, `if not ctx.apply:` → `if not False:` → `3 failed, 29 passed in 22.34s`, `EXIT=1`: `test_apply_applies_the_one_job_and_changes_the_targets_tracked_content`, `test_apply_with_force_mission_applies_every_job_in_order` and `test_an_apply_the_baseline_check_refuses_fails_the_walk_naming_the_job`
  - (c) the `("--push", "F270"),` line removed from `_DO_FLAGS_NOT_YET_AVAILABLE` → `1 failed, 31 passed in 23.94s`, `EXIT=1`: `test_a_flag_whose_feature_is_not_built_refuses_before_any_step[--push]`
  - `WORKTREE_REMOVED=0`. The `remedy/job-*` branch count was 31 before and 31 after.
- G6 (clean tree, HEAD == origin) runs after the push. It is in the round report.

## Authored-text proofs

All four files (`ledger.md`, `decisions.md`, `plan.md`, `block.md`) were verified by sha256 before use. They were copied byte-exact to `.agent/authored/f268-r4-*`, and the post-copy digests are identical (G1). The two appends were built from `git show f831d374:<path>` bytes plus the payload, never from a file being written. G1's byte checks and `cmp` prove the committed bytes.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | |
| R-0967 | done | C2. Red under G5 (a) |
| R-0811 remainder | done | C2: every tip in the two named modules |
| T004 (1) detached cockpit | done | C3, C4 tests (1) and (5) |
| T004 (2) `--apply` | done | C3, C4 tests (2) and (3). Red under G5 (b) |
| T004 (3) flags not yet available | done | C3, C4 test (4). Red under G5 (c) |

Landed: R-0967 — `test_end_of_input_at_a_halt_stops_the_walk_runs_no_job_and_asks_every_job_to_stop` in `tests/cli/test_do_sequence_cli.py` has a reader that raises `EOFError`. At the first halt it asserts the walk ended `study: stopped` with `not run: stopped by end of input`, with no job and no provider call. At the first halt after shape, with `--force-mission`, it asserts the walk ended `run: stopped` with ≥2 jobs still `PLANNED`, each carrying a `source="do"` stop request. Both cases fail when `EOFError` is read as an empty answer (G5 (a)) (C2).
Landed: R-0811 — `stop_reasons.derive_stop_reasons` and `autonomy_readiness._assess_level` no longer print any `<…>` placeholder or `"<goal>"`. Every next action names the real job id, and the approve tip names each real intent id. `tests/orchestration/test_stop_reasons.py` covers all four derived reasons, and `tests/test_autonomy_readiness.py` covers the whole rendered summary and all seven level tips; both assert no `<[a-z_]+>` and the real job id (C2).

## Open findings

127 open by distinct id, derived with `.remedy-wt/f268-r4/count.py`. The ledger at HEAD holds 137 distinct `- R-nnnn —` registrations and 10 distinct `Done:` ids. The same derivation at `f831d374` reads 136 / 8 / 128, which matches round 3's count. C1 booked R-0967 and two `Done:` lines (R-0964, R-0966). This round writes no `Done:` line and opens no finding.

## Deviations & assumptions

- Commit sequence: C1, C2, C3, C4, C5, as the block orders. C2 was first committed without R-0967's test (`574e7dc3`) and then amended, before any push, to `6b1e1254`, so that C2 holds both repairs as the block's bundle states. `574e7dc3` was never pushed, and no force-push happened.
- **`--apply` with more than one job, measured.** Every job of a mission runs against the unchanged target, because the run step runs all jobs before apply. So when two jobs write the same file, the second apply is refused by `job_apply`'s baseline check: `target_changed_since_job` for a tracked file, `target_created_since_job` for a new one.
  - The stock `FakeProvider()` writes `docs/README.md` for every build, so `remedy do "Write a CONTRIBUTING.md" --apply --force-mission` on the fake provider always exits 1. `probe_apply.py` measured `apply: failed — job 17c1… was not applied … (status blocked): baseline_check_failed: ['target_changed_since_job: docs/README.md']; applied before it: job 2733… applied 1 file(s)`.
  - That is D9's "stop at the first not applied, naming why", working as designed. It also means `--apply` cannot apply a mission whose jobs touch a common file. I did not register a finding: the reviewer decides.
  - C4 test (2)'s `--force-mission` case therefore monkeypatches `FakeProvider.__init__` so that each construction writes its own tracked file (`docs/job_NN.md`), and test (3) is the refused counterpart. Production code does not change for this.
- "Tracked content changes": the fake builder writes `docs/README.md`, which the round 1 fixture does not track. So the apply tests first commit that file (and `docs/job_NN.md`) into the target, and then assert `git diff --name-only`.
- R-0967's test is parametrized. The fix clause's "first halt" comes before any job exists, which would make "every job has a stop request" vacuous. The second case reads end of input at the first halt after shape (the round 3 `q`-test selector), so the stop requests are actually measured. Both cases go red under the mutation.
- R-0811 wording choices, all free of placeholders:
  - The two plain-sentence next actions now name the job, per the block's "every stop-reason next action … carry the real job id": `Review the failed test output of job <id>.` and `Commit or stash the changes in the target repository of job <id> (<target_repo>).`
  - An intent event without an id yields `remedy patch list <id> names the intent ids to approve`.
  - `tasks_defined` is `remedy job plan <id>`. `job.plan` is in the catalog, and `_cmd_plan_job_local` handles it.
- Cockpit info file location: `ui start --info-file X` writes its session record ONLY to X (`ui._cmd_ui_start`: `info_file or session_file`). The file therefore goes in `<data root>/ui/sessions/`, which makes the reported `remedy ui stop` true (probed, see External actions). A launch that times out terminates the child, and a child that exits early is reported with its exit code. Either way, the log path is named.
- A ui step that opens the cockpit reports `done` (it was `skipped`). A context without a launcher (library callers) reports `skipped` with the manual command. With `--step-by-step`, a `done` ui step is followed by one more halt before apply.
- `--apply` treats any status other than `applied` as not applied, including `applied_test_failed` and `applied_cleanup_failed`. A failure adds `Next: remedy job apply <id> --repo <root> --dry-run`.
- The refusal runs first in `_cmd_do`, so it covers both the bare route and `do run`, even before an empty goal is rejected. The table is static: the round that lands F269 or F270 removes its rows. It does not read `STATUS.md`.
- `do.run` still declares `may_mutate_repo=False`, although `--apply` writes the repository. `tests/orchestration/test_do_run.py:564` pins it false, so the reviewer decides.
- Added beyond the block: `test_the_old_name_with_history_is_never_created`, which checks that `--with-history` exits 2.
- Placeholders outside this change set remain: `timeline.py:435,505` (`remedy do run "<goal>"`), `trust_report.py:326` (`remedy patch approve <job_id> <intent_id>`), and the two round 3 named (`self_dogfood_execution.py`, `test_execution_service.py`).
- `--apply` on the non-bare `do run` path is ignored by the autorun path, as the other bare-only flags are.
- Docs: `docs/guides/do-run-v1.md`'s "v1 always stops before apply" describes the unchanged autorun path, so no doc was edited. `.agent/context.md` was not updated; it is not in the change set.
- Full suite not run (amend0917-throughput).

## Next

Reviewer: review round 4 at this branch tip and book its verdict in the next round's first commit.

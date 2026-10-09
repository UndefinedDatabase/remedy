## What and why

F299 makes a mission's acceptance checks work on a repository that is not Remedy's own. Until now
a contract criterion that named no test of its own was checked by `pytest tests` under Remedy's own
interpreter, so a Python project with its own virtual environment, a Node project and a project
without tests were all judged red, and a red contract refuses the push. Measured on three scratch
projects at `1acd5ac39` (`.agent/f299_inventory.md`): all three criteria ended `unmet`.

Now:
- **T002, the project's own command (DECISION F299 D1).** The new check kind `project_tests` finds
  the project's test command when the check runs, in the job's worktree: the `command` of the
  `[tests]` table in the project's own `.remedy/config.toml`, else `npm test` for a real `test`
  script in `package.json`, else pytest on the `tests` folder. It runs with the project's own
  virtual environment and `node_modules/.bin`, found in the worktree or in the repository's own
  checkout, through a new `env_overlay` of the guard's check seam. The closed list of executables
  is not widened. A contract's default check is this kind; Remedy's own repository runs the same
  argv under the same interpreter as before, and a test pins that.
- **T003, "no check ran" (DECISION F299 D2).** A criterion whose check finds no test command reads
  `unchecked`: neither met nor unmet. The gate lists the check under `not_run` and holds nothing on
  it; the criterion holds no mission and no push; the approval card says `review`. Every surface
  says "no check ran, because the project names no test command": the `Contract:` line, the
  contract tables, `remedy job show`, the run report, the guided tour and the push, which names
  the criterion under `push_unchecked_criteria` / `unchecked_blocking_criteria`.
- **T004, the page and the proof.** `docs/system/acceptance-checks-v1.md`, and
  `tests/cli/test_do_project_targets.py`, which drives `remedy do run` with the fake providers
  through `--commit --push` on four scratch projects: Python with its own venv (met, pushed),
  Node with `npm test` (met, pushed), no tests (`unchecked`, pushed and named), and Python whose
  own test fails (`unmet`, push refused — F270's rule unchanged).

## Key decisions
- DECISION F299 D1: the command comes from the project's config, then `package.json`, then a
  `tests` folder, found at run time; not from `remedy study` (no structured fact) nor from
  `command_discovery`'s ranked choice (measured: it passes a comment's words as arguments).
- DECISION F299 D2: the state `unchecked`, the gate's `not_run` list, the one phrase, the card's
  `review`, and a push that is never refused by an unchecked criterion but names it.

## How to review
Read `packages/orchestration/project_tests.py`, then `_run_project_tests` in
`packages/orchestration/dod_runners.py`, then the `unchecked` paths in `mission_contract.py`,
`dod_gate.py` and `job_apply.py`; the four scratch projects in `tests/cli/test_do_project_targets.py`
show the end-to-end behaviour.

## Changed files (at the accepted head `02f613d86`, against the fork point `1acd5ac39`)

| Path | Lines |
|---|---|
| `apps/cli/client_interface.py` | +3 / -1 |
| `apps/cli/commands/job.py` | +8 / -1 |
| `docs/README.md` | +2 / -0 |
| `docs/agents/planner_reviewer_prompt.md` | +12 / -0 |
| `docs/roadmap/STATUS.md` | +1 / -1 |
| `docs/roadmap/features/T7_F299.md` | +49 / -0 |
| `docs/system/acceptance-checks-v1.md` | +78 / -0 |
| `docs/system/machine-client-contract-v1.md` | +20 / -18 |
| `packages/orchestration/client_digest.py` | +9 / -4 |
| `packages/orchestration/do_sequence.py` | +43 / -20 |
| `packages/orchestration/dod_gate.py` | +12 / -1 |
| `packages/orchestration/dod_runners.py` | +84 / -19 |
| `packages/orchestration/dod_schema.py` | +6 / -1 |
| `packages/orchestration/exec_guard.py` | +13 / -3 |
| `packages/orchestration/job_apply.py` | +46 / -12 |
| `packages/orchestration/mission_contract.py` | +47 / -16 |
| `packages/orchestration/project_tests.py` | +247 / -0 |
| `packages/orchestration/result_tour.py` | +18 / -5 |
| `packages/orchestration/run_report.py` | +15 / -3 |
| `scripts/self_use_queue.json` | +8 / -0 |
| `tests/cli/test_client_interface.py` | +2 / -1 |
| `tests/cli/test_do_commit_flags.py` | +18 / -0 |
| `tests/cli/test_do_project_targets.py` | +178 / -0 |
| `tests/cli/test_do_sequence_cli.py` | +17 / -17 |
| `tests/cli/test_status_cmd.py` | +8 / -6 |
| `tests/orchestration/import_reachability_allowlist.txt` | +1 / -0 |
| `tests/orchestration/test_client_digest.py` | +6 / -2 |
| `tests/orchestration/test_contract_templates.py` | +3 / -2 |
| `tests/orchestration/test_dod_gate.py` | +79 / -2 |
| `tests/orchestration/test_dod_runners.py` | +203 / -4 |
| `tests/orchestration/test_exec_guard.py` | +21 / -0 |
| `tests/orchestration/test_job_apply_commit.py` | +28 / -0 |
| `tests/orchestration/test_mission_contract.py` | +86 / -5 |
| `tests/orchestration/test_orchestrator_loop.py` | +1 / -1 |
| `tests/orchestration/test_project_tests.py` | +241 / -0 |
| `tests/orchestration/test_result_tour.py` | +46 / -2 |
| `.agent/` (27 files: blocks, ledger, decisions, plan, inventory, self-use record, closure suite) | +2209 / -127 |

The closing round adds the ledger's rotation, the STATUS line, the README sync, SU-051's
`consumed_by` and the handoff.

## Verification
- The closure's one full suite on the repaired tree: `22246 passed, 22 skipped`, exit 0
  (`.agent/authored/f299-closure-suite.txt`), 1166.53 CPU seconds, 2.0 percent above F253's.
- Evidence job `f299r8e1001` on `02f613d86`: 2173 node ids, 2170 passed, 3 skipped,
  `is_valid_current_run True`.
- Package `remedy-review-20261009-192024-READY_FOR_REVIEW.zip`, SHA-256
  `6280e0aefab46067a191d9b5806625d6fe008961923ee45139590376583facf9`, `READY_FOR_REVIEW`, review
  subject `1acd5ac39`..`02f613d86`, in `/home/decodeux/Repos/remedy-history/zips`.
- Every production change was mutation-proved by the reviewer in a disposable worktree.

## Latest verdict and findings
Rounds 1 to 8 reviewed; round 9, the closing round, is reviewed on this pull request. F299 is
accepted PASS_WITH_RISKS: its own findings R-1227, R-1228, R-1229 and R-1231 are resolved, and 16
findings stay open, all owned by the findings paydown F297, among them R-1230, raised by this
closure's self-use run (its job was passed by Remedy's reviewer while its diff met none of its
item's acceptance lines).

## Runtime actuals
Nine delegated rounds in one session on 2026-10-09; the self-use job measured 4 provider calls,
15322 tokens and 2.04 USD on `claude-cli` with `claude-sonnet-4-6`; the session's own model calls
are not measured by Remedy's ledger.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

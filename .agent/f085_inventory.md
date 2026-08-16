# F085 — subprocess seam inventory (R2)

A RECORD of the current shape, produced for T2_F085's "inspect current shape
before building" step. It proposes no design, writes no `exec_guard.py`, fixes
nothing and renames nothing. Every value below was derived mechanically by an
AST walk over each file, never by eye.

Call-site set, defined by exactly this command run from the repository root:

    git grep -n -E 'subprocess\.(run|Popen|call|check_output|check_call)' -- packages/ apps/

Measured at this commit: **73 matching lines across 33 files** — the same 73 the
reviewer measured at `a5a70621` and at the R1 head `9ba3179e`.

## Seams

One row per line the command above prints. Six of the 73 lines are NOT calls —
four are prose inside a docstring or comment and two are type annotations
(`proc: subprocess.Popen`). Their `symbol` is still the AST-derived enclosing
scope; their remaining columns are `n/a`, because a line that is not a call has
no keywords to read and inventing `no` would assert a call that does not exist.

Column convention, which matters for reading `shell`: `cwd`, `env`, `timeout`,
`check` and `shell` are `yes` when the KEYWORD IS PASSED at that call, whatever
its value, exactly as the step block defines them. `capture` is `yes` when any of
`capture_output`, `stdout` or `stderr` is passed. All four `shell=yes` rows pass
the literal `False`; **no call site in this inventory runs a shell**.

| site | symbol | callee | cwd | env | timeout | capture | check | shell |
|---|---|---|---|---|---|---|---|---|
| apps/cli/commands/brain.py:217 | _cmd_brain_open | Popen | no | no | no | no | no | no |
| apps/cli/commands/brain.py:219 | _cmd_brain_open | Popen | no | no | no | no | no | no |
| apps/cli/commands/init_cmd.py:65 | _ensure_ignore_entry | run | yes | no | yes | yes | no | no |
| apps/cli/commands/job_context_cmd.py:48 | _repo_candidate_paths_with_source | run | yes | no | yes | yes | yes | no |
| apps/cli/commands/runtime_cmd.py:136 | _serve_supervisor | Popen | yes | yes | no | yes | no | no |
| apps/cli/commands/worker.py:134 | _cmd_worker_resources | run | no | no | yes | yes | no | no |
| apps/cli/commands/worker.py:153 | _cmd_worker_resources | run | no | no | yes | yes | no | no |
| apps/cli/commands/worker.py:224 | _cmd_worker_unload | run | no | no | yes | yes | no | no |
| apps/cli/commands/worker.py:241 | _cmd_worker_unload | run | no | no | yes | yes | no | no |
| packages/orchestration/autorun.py:382 | _run_fixture_builder | run | yes | no | yes | yes | no | no |
| packages/orchestration/autorun.py:510 | _run_repair_loop_fixture | run | yes | no | yes | yes | no | no |
| packages/orchestration/autorun.py:563 | _run_repair_loop_fixture | run | yes | no | yes | yes | no | no |
| packages/orchestration/builder_bridge.py:220 | run_builder_bridge | run | yes | yes | yes | yes | no | no |
| packages/orchestration/ci_run.py:79 | _run_via_subprocess | run | yes | yes | no | no | yes | no |
| packages/orchestration/command_discovery.py:190 | CommandCandidate | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| packages/orchestration/command_discovery.py:205 | argv_list | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| packages/orchestration/dod_runners.py:12 | <module> | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| packages/orchestration/dod_runners.py:302 | _run_process_check | run | yes | yes | yes | yes | no | no |
| packages/orchestration/dod_runners.py:575 | _run_app_once | Popen | yes | yes | no | yes | no | no |
| packages/orchestration/evidence_index.py:37 | _git | run | yes | no | yes | yes | no | no |
| packages/orchestration/evidence_index.py:53 | _git_raw | run | yes | no | yes | yes | no | no |
| packages/orchestration/gauntlet_runner.py:196 | materialise_sample_project | run | yes | yes | no | yes | yes | no |
| packages/orchestration/git_status.py:45 | _run_git | run | no | no | yes | yes | no | no |
| packages/orchestration/integrity_gate.py:187 | _check_relevant_untracked | run | no | no | yes | yes | no | no |
| packages/orchestration/integrity_gate.py:283 | _check_collect_only | run | no | no | yes | yes | no | no |
| packages/orchestration/job_evidence.py:2954 | _git | run | no | no | no | yes | no | no |
| packages/orchestration/job_promote.py:417 | _run_post_test | run | yes | no | yes | yes | no | no |
| packages/orchestration/job_promote.py:506 | _materialize_promotion_source_owned | run | yes | no | yes | yes | no | no |
| packages/orchestration/job_promote.py:515 | _materialize_promotion_source_owned | run | yes | no | yes | yes | no | no |
| packages/orchestration/job_promote.py:522 | _materialize_promotion_source_owned | run | yes | no | yes | yes | no | no |
| packages/orchestration/job_promote.py:542 | _run_cleanup_git | run | yes | no | yes | yes | no | no |
| packages/orchestration/job_promote.py:815 | _check_source_coverage | run | yes | no | yes | yes | no | no |
| packages/orchestration/managed_builder_execution.py:1160 | run_managed_builder | run | yes | yes | yes | yes | no | yes |
| packages/orchestration/mission_state.py:833 | runner | run | yes | no | yes | yes | no | no |
| packages/orchestration/pingpong_loop.py:3537 | _run_test_command | run | yes | no | yes | yes | no | no |
| packages/orchestration/pingpong_promote.py:326 | _run_post_test | run | yes | no | yes | yes | no | no |
| packages/orchestration/pingpong_provider.py:952 | _resolve_version | run | yes | no | yes | yes | no | no |
| packages/orchestration/pingpong_provider.py:1075 | _call | run | yes | no | yes | yes | no | no |
| packages/orchestration/pingpong_provider.py:1208 | _call_reviewer_structured | run | yes | no | yes | yes | no | no |
| packages/orchestration/project_registry.py:519 | _managed_worktree_parent | run | yes | no | yes | yes | no | no |
| packages/orchestration/repair_attest.py:198 | _git | run | yes | no | yes | yes | no | no |
| packages/orchestration/repair_attest.py:291 | collect_diff_stat | run | yes | no | yes | yes | no | no |
| packages/orchestration/repair_attest.py:295 | collect_diff_stat | run | yes | no | yes | yes | no | no |
| packages/orchestration/review_subject.py:187 | _git | run | yes | no | yes | yes | no | no |
| packages/orchestration/review_subject.py:256 | _toplevel | run | yes | no | yes | yes | no | no |
| packages/orchestration/run_manifest.py:203 | _run_probe | run | yes | no | yes | yes | no | yes |
| packages/orchestration/run_manifest.py:322 | _helper_neutralizing_args | run | yes | yes | yes | yes | no | yes |
| packages/orchestration/run_manifest.py:354 | _git_bytes | run | yes | yes | yes | yes | no | yes |
| packages/orchestration/safe_publish.py:193 | git_tracked_status | run | yes | no | yes | yes | no | no |
| packages/orchestration/stream_evidence.py:595 | run_streamed_command | Popen | yes | no | no | yes | no | no |
| packages/orchestration/test_execution_service.py:323 | _run_isolated_process | Popen | yes | yes | no | yes | no | no |
| packages/orchestration/test_execution_service.py:361 | <module> | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| packages/orchestration/test_runner.py:24 | <module> | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| packages/orchestration/test_runner.py:201 | run_tests_local | run | yes | no | yes | yes | no | no |
| packages/orchestration/ui_server.py:2787 | _auto_build_frontend | run | yes | no | yes | yes | yes | no |
| packages/orchestration/ui_server.py:2800 | _auto_build_frontend | run | yes | no | yes | yes | yes | no |
| packages/orchestration/ui_server.py:3156 | _try_open_browser | Popen | no | no | no | no | no | no |
| packages/orchestration/ui_server.py:3158 | _try_open_browser | Popen | no | no | no | no | no | no |
| packages/orchestration/worktrees.py:104 | _git | run | yes | no | yes | yes | no | no |
| packages/orchestration/worktrees.py:255 | _branch_exists | run | yes | no | no | yes | no | no |
| packages/orchestration/worktrees.py:279 | commit_exists | run | yes | no | no | yes | no | no |
| packages/orchestration/worktrees.py:294 | is_ancestor | run | yes | no | no | yes | no | no |
| packages/orchestration/worktrees.py:467 | write_tree_for_path | run | yes | yes | yes | yes | no | no |
| packages/orchestration/worktrees.py:471 | write_tree_for_path | run | yes | yes | yes | yes | no | no |
| packages/orchestration/worktrees.py:499 | write_tree | run | yes | yes | yes | yes | no | no |
| packages/orchestration/worktrees.py:505 | write_tree | run | yes | yes | yes | yes | no | no |
| packages/orchestration/worktrees.py:534 | blob_at | run | yes | no | yes | yes | no | no |
| packages/orchestration/worktrees.py:602 | resolve_checkpoint_ref | run | yes | no | no | yes | no | no |
| packages/orchestration/worktrees.py:613 | delete_checkpoint_ref | run | yes | no | no | yes | no | no |
| packages/orchestration/worktrees.py:625 | object_exists | run | yes | no | no | yes | no | no |
| packages/runtimes/dev_server.py:1440 | __init__ | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| packages/runtimes/dev_server.py:1484 | start | Popen | yes | yes | no | yes | no | no |
| packages/runtimes/runtime_supervisor.py:235 | run | Popen | yes | yes | no | yes | no | no |

Keyword totals over the 67 real call sites: cwd 55, env 16, timeout 48, capture 62,
check 5, shell 4 (all four literal `False`). Callees: run 57, Popen 10, and no
use of `call`, `check_output` or `check_call` anywhere. **19 of 67 real call sites
pass no `timeout`** and **12 pass no `cwd`**.

## Classes

Every site is assigned to exactly one class from the closed vocabulary. The rule
used, stated so it can be checked: a site takes the class of the PURPOSE its
enclosing helper serves, not of the binary it happens to exec. That is the block's
own reading — it names review-subject tooling as `packaging` although every spawn
in `review_subject.py` is git.

### builder — 5
- `packages/orchestration/managed_builder_execution.py`:1160
- `packages/orchestration/pingpong_provider.py`:952, 1075, 1208
- `packages/orchestration/stream_evidence.py`:595

### test — 12
- `packages/orchestration/autorun.py`:382, 510, 563
- `packages/orchestration/builder_bridge.py`:220
- `packages/orchestration/ci_run.py`:79
- `packages/orchestration/integrity_gate.py`:283
- `packages/orchestration/job_promote.py`:417
- `packages/orchestration/mission_state.py`:833
- `packages/orchestration/pingpong_loop.py`:3537
- `packages/orchestration/pingpong_promote.py`:326
- `packages/orchestration/test_execution_service.py`:323
- `packages/orchestration/test_runner.py`:201

### dod — 2
- `packages/orchestration/dod_runners.py`:302, 575

### runtime — 5
- `apps/cli/commands/runtime_cmd.py`:136
- `packages/orchestration/ui_server.py`:2787, 2800
- `packages/runtimes/dev_server.py`:1484
- `packages/runtimes/runtime_supervisor.py`:235

### git — 24
- `apps/cli/commands/init_cmd.py`:65
- `apps/cli/commands/job_context_cmd.py`:48
- `packages/orchestration/gauntlet_runner.py`:196
- `packages/orchestration/git_status.py`:45
- `packages/orchestration/integrity_gate.py`:187
- `packages/orchestration/job_promote.py`:506, 515, 522, 542, 815
- `packages/orchestration/project_registry.py`:519
- `packages/orchestration/safe_publish.py`:193
- `packages/orchestration/worktrees.py`:104, 255, 279, 294, 467, 471, 499, 505, 534, 602, 613, 625

### packaging — 11
- `packages/orchestration/evidence_index.py`:37, 53
- `packages/orchestration/job_evidence.py`:2954
- `packages/orchestration/repair_attest.py`:198, 291, 295
- `packages/orchestration/review_subject.py`:187, 256
- `packages/orchestration/run_manifest.py`:203, 322, 354

### other — 14

desktop file/URL opener, spawns no build or test tool:
- `apps/cli/commands/brain.py`:217, 219
- `packages/orchestration/ui_server.py`:3156, 3158

local model-daemon and GPU capacity probe, not a build or test spawn:
- `apps/cli/commands/worker.py`:134, 153, 224, 241

not a call site at all: the grep line is prose or a type annotation, so it spawns nothing:
- `packages/orchestration/command_discovery.py`:190, 205
- `packages/orchestration/dod_runners.py`:12
- `packages/orchestration/test_execution_service.py`:361
- `packages/orchestration/test_runner.py`:24
- `packages/runtimes/dev_server.py`:1440

Per-class counts: builder 5, test 12, dod 2, runtime 5, git 24, packaging 11, other 14.
They sum to 73, which equals the 73 rows of the `## Seams` table and the 73 lines
the defining grep prints. No site appears in two classes and none is missing.

## Guards already in force

The two the step block names both exist and both are real, but they are narrower
than their names suggest, and they are not the only guards over these paths. The
sweep below walked every `tests/**/*.py`, kept each `test*` function that both
reads source text (`read_text`, `.SRC`, `ast.parse`) and asserts about
`shell=True`/`subprocess`/`Popen`/`os.system`, and then matched it against the 33
inventory files. It is a sweep of the tests present at this commit, not a claim
that no other guard can ever exist.

Package-wide:

- `tests/orchestration/test_test_runner.py::test_no_shell_true_in_orchestration`
  — AST over `packages/orchestration/*.py`, no exemption; forbids a `shell`
  keyword whose constant value is `True`. Covers 26 of the 33 inventory files.
- `tests/orchestration/test_autonomy.py::test_no_shell_true_in_orchestration`
  — the same glob and the same assertion, but EXEMPTS `test_runner.py`.
- `tests/ui_server/test_dashboard_contract.py::test_no_shell_true_in_subprocess_calls`
  — a third copy of the same body, also exempting `test_runner.py`.

Per-file:

- `tests/orchestration/test_test_runner.py::test_no_subprocess_in_discovery_module`
  — forbids `subprocess.run` in `command_discovery.py`. It matches the attribute
  `run` only, so `Popen`, `call`, `check_output` and `check_call` are not
  forbidden by it; the module in fact calls none of them.
- `tests/orchestration/test_autonomy.py::test_no_shell_true` — text over
  `git_status.py`.
- `tests/orchestration/test_managed_builder_execution.py::test_no_shell_true` and
  `::test_no_forbidden_imports` — over `managed_builder_execution.py`.
- `tests/orchestration/test_test_execution_service.py::test_no_shell_true` and
  `::test_no_shell_true_in_service`, plus
  `tests/cli/test_test_run_runtime.py::test_no_shell_true_in_test_execution_service`
  — over `test_execution_service.py`.
- `tests/regression/test_named_bugs.py::test_no_shell_true_in_autorun` — over
  `autorun.py`.
- `tests/storage/test_persistence.py::test_no_shell_true_in_worker` and
  `tests/orchestration/test_command_discovery.py::test_no_shell_true` — both over
  `apps/cli/commands/worker.py`.
- `tests/ui_server/test_dashboard_contract.py::test_no_shell_true_in_server`,
  `tests/ui_server/test_live_state.py::test_server_no_shell_true` and
  `tests/ui_contracts/test_ux_quality.py::test_no_shell_true_in_new_modules` —
  over `ui_server.py`.
- `tests/runtimes/test_dev_server.py::test_no_shell_is_ever_used` — the strictest
  of them all: `dev_server.py` may pass no `shell` keyword at any value.
- `tests/test_command_discovery.py::test_run_tests_local_no_shell_true` — the only
  BEHAVIOURAL guard in the set: it asserts on the kwargs of the actual
  `subprocess.run` call made by `test_runner.run_tests_local`.

What is NOT guarded, measured rather than assumed:

- Six inventory files are covered by no `shell`/`subprocess` source guard at all:
  `apps/cli/commands/brain.py`, `init_cmd.py`, `job_context_cmd.py`,
  `runtime_cmd.py`, and `packages/runtimes/runtime_supervisor.py` (its only
  source guard,
  `tests/runtimes/test_supervisor_portability.py::test_every_supervisor_failure_path_uses_the_common_finalizer`,
  is about failure finalizers, not execution).
- Every guard found forbids a shell. NONE of them requires a `timeout`, a `cwd`,
  an environment allowlist, an output cap or any resource limit. The 19 call
  sites with no `timeout` and the 12 with no `cwd` are unguarded by construction.
- `tests/regression/test_resource_safety.py` constrains `scripts/` wrappers
  (flock, timeout, process-group kill), not any of the 33 files here.

## R-0202 — the REMEDY_UI_NO_AUTO_BUILD spawn path

`git grep -n REMEDY_UI_NO_AUTO_BUILD -- packages/ apps/ tests/ scripts/` returns
nine lines and no more. Every place the variable is read or set:

- READ, once, in the whole codebase:
  `packages/orchestration/ui_server.py:2772` in `_auto_build_frontend` —
  `os.environ.get("REMEDY_UI_NO_AUTO_BUILD") == "1"`, an early `return None`. It
  reads the CURRENT process's environment, so it binds only that process.
- `packages/orchestration/ui_server.py:2768` in `_auto_build_frontend`, `:2824`
  and `:2857` in `_load_frontend` — docstring and operator-help text, no read.
- SET, nowhere in `packages/`, `apps/` or `scripts/`. The only writers are two
  tests: `tests/ui_server/test_dashboard_contract.py:547` and `:555`
  (`patch.dict(os.environ, {"REMEDY_UI_NO_AUTO_BUILD": "1"})`), and one remover,
  `:536` (`env.pop(...)` followed by `patch.dict(..., clear=True)`).

Which spawn path can drop or ignore it — traced, not guessed. Sixteen of the 67
call sites pass `env=`; the rest inherit the parent environment and therefore
forward the variable unchanged. Of those sixteen, fourteen build their env from
`os.environ` (`dict(os.environ)`, `os.environ.copy()`, `{**os.environ, ...}`, or
`DevServerSpec.resolved_env`, which starts at `dict(os.environ)`) and so also
forward it. TWO replace the environment with an allowlist and therefore DROP it:

- `packages/orchestration/managed_builder_execution.py:1160` in
  `run_managed_builder`, via `_build_sanitized_env` (`:942`), which keeps only the
  twelve keys of `_ALLOWED_ENV_KEYS` — `PATH, HOME, LANG, LC_ALL, TERM, USER,
  LOGNAME, TMPDIR, TMP, TEMP, SHELL, XDG_RUNTIME_DIR`. `REMEDY_UI_NO_AUTO_BUILD`
  is not among them.
- `packages/orchestration/test_execution_service.py:323` in
  `_run_isolated_process`, via `_build_safe_env` (`:264`), which keeps only
  `_ALWAYS_KEEP` plus the `_SAFE_ENV_PREFIXES` list. A key beginning `remedy_`
  matches neither, so the variable is stripped from every spawned test process.

That is the seam-level answer the inventory can support: a builder tool or an
isolated test process spawned by those two sites runs with the variable ABSENT,
so any UI build reached from inside such a child sees `None != "1"` and proceeds.

The mechanism of the historical incidents is still NOT explained by this, and
this section does not guess one. What was checked: all nine occurrences of the
variable; the single reader and its scope; the env construction at all sixteen
`env=` sites; and the test that clears it. The best-documented alternative
remains in-process rather than spawned —
`tests/ui_server/test_dashboard_contract.py::TestAutoBuildBehavior::test_auto_build_runs_by_default`
(`:530`) pops the variable, replaces `os.environ` with `clear=True`, and calls
`_auto_build_frontend()` directly; in a real checkout `apps/ui/package.json`
exists, so that call reaches `npm install` and `npm run build` for real. That is
already registered as R-0221 and it is not a subprocess seam at all. Nothing here
connects either dropping seam to a recorded incident, and no fix is proposed.

## Premise check

The feature file states that subprocess execution "already flows through a small
number of helpers (test runner, DoD runners, provider transport, runtime
harness)". The measurement does not support that as written. There are 67 real
call sites across 33 files, sitting in 56 distinct enclosing functions — 43 of
them in `packages/orchestration` alone — not funnelled into a helper per class.
The four named helpers account for 24 of the 67: `test` 12, `dod` 2, `builder` 5
(provider transport), `runtime` 5 — and even those are not single seams, since
the 12 `test` sites live in 10 different modules. The remaining 43 are `git` 24,
`packaging` 11 and the 8 real calls in `other`. There IS a real
concentration inside the git class — 12 of its 24 sites are in `worktrees.py`
and 5 in `job_promote.py` — so git plumbing is the one area where a single
wrapper would cover most sites. Everywhere else the seams are many rather than
few, which is what T002's slicing assumes away. Consequences for the task
slicing are for R3 to rule on; this section only reports the numbers.

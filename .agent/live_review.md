# Live Review — F081 remedy init

Per-feature ledger. Findings are authored by the reviewer (Window 1) and
applied here verbatim by the worker. R-XXXX IDs continue monotonically
across features (last used: R-0076). History lives in git and in each
feature's evidence zip.

### R-0077: `remedy init` bare invocation breaks the group-help contract + real-registry side effects in tests
- **Status**: Open → Done: R-0077
- **Severity**: High
- **Area**: apps/cli/grouped.py (_ALWAYS_INJECT), tests/test_grouped_cli.py
- **Details**: `_ALWAYS_INJECT = {"init"}` makes `remedy init` with no
  subcommand EXECUTE `init.run` instead of printing the group-help box. The
  parametrized group-help contract tests in tests/test_grouped_cli.py iterate
  over GROUPS.keys(), so init fails 6 cases (test_group_help_exits_zero,
  test_group_help_lists_subcommands, test_main_entrypoint_delegates_group_help,
  test_group_help_has_usage, test_group_help_has_options,
  test_group_help_has_commands_box). Worse, those tests then run the real
  command against the repo cwd — test_group_help_has_commands_box[init] output
  was "[exists] project remedy", i.e. the help test read/wrote the real project
  registry. On a fresh CI checkout this registers a project as a side effect.
- **Evidence**: pytest tests/test_grouped_cli.py -q → 6 FAILED [init];
  captured stdout for has_commands_box[init] = "[exists] project remedy\n".
- **Expected fix**: `remedy init` running on bare invocation is the intended
  UX (feature file: `remedy init [flags]` is the primary form). Do NOT change
  the command to show help. Instead exempt always-inject single-command groups
  from the bare-help contract: in tests/test_grouped_cli.py parametrize over
  `[g for g in GROUPS if g not in grouped._ALWAYS_INJECT]` (or an equivalent
  shared constant) for every group-help test class. After the fix, no test may
  invoke bare `remedy init` against the real data dir. Re-verify:
  pytest tests/test_grouped_cli.py -q → 0 failures.

### R-0078: init tests are not data-dir-isolated; the idempotency mtime-proof is dead code
- **Status**: Open
- **Severity**: Medium
- **Area**: tests/cli/test_init_cmd.py
- **Details**: `_ENV` sets PYTHONPATH but not REMEDY_DATA_DIR, so every init
  subprocess writes into the REAL production data dir
  (packages/orchestration/data_paths.projects_dir honours REMEDY_DATA_DIR;
  unset → real dir). test_second_run_idempotent builds mtime_before from
  os.path.join(os.environ.get("REMEDY_DATA_DIR",""), "projects"); with the var
  unset this is the relative path "projects", os.path.isdir → False →
  mtime_before = {}. Furthermore no mtime_after is ever computed and no equality
  assertion exists, so the snapshot proves nothing. The feature done-condition
  "zero writes proven by mtime snapshot" is unmet; idempotency is asserted only
  via the "[exists]" stdout line. (Idempotency itself is sound by construction —
  resolve_project short-circuits before any write — so this is test-integrity,
  not a correctness bug.)
- **Evidence**: test_init_cmd.py:54-59 (mtime_before built, never compared);
  a manual `remedy init` run left "tmp-<rand>" in the real projects dir.
- **Expected fix**: In _ENV (or per subprocess call) set REMEDY_DATA_DIR to a
  per-test tmp dir under tmp_path so tests never touch the real registry. Then
  in test_second_run_idempotent snapshot the projects-dir file mtimes BEFORE and
  AFTER the second run and assert mtime_before == mtime_after, in addition to the
  "[exists]" assertion. Confirm the real ~/.../projects dir is untouched by a
  full run of the file.

### R-0079: false verification claim in the handoff
- **Status**: Open
- **Severity**: Low
- **Area**: .agent/handoff.md
- **Details**: Handoff states 'CLI suite (tests/cli): same failure pattern as
  main (pre-existing doc tests)' and 'remedy ui behavior preserved'. In fact 6
  test_grouped_cli.py[init] cases are NEW regressions from this branch (they fail
  on the init group only). The completion claim was not verified against a real
  run of tests/test_grouped_cli.py. Block condition: unverified completion claims.
- **Evidence**: pytest tests/test_grouped_cli.py -q run by the reviewer.
- **Expected fix**: After R-0077/R-0078, re-run tests/test_grouped_cli.py and
  tests/cli/test_init_cmd.py, paste real output, and rewrite the handoff
  verification section to the true re-verified state. Explicitly distinguish the
  3 genuinely pre-existing tests/test_command_catalog.py failures (job.budget,
  do.job-evidence, do.repair-attest — NOT to be fixed in F081) from this
  branch's results.

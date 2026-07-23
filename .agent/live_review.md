# Live Review — F081 remedy init

Per-feature ledger. Findings are authored by the reviewer (Window 1) and
applied here verbatim by the worker. R-XXXX IDs continue monotonically
across features (last used: R-0076). History lives in git and in each
feature's evidence zip.

### R-0077: `remedy init` bare invocation breaks the group-help contract + real-registry side effects in tests
- **Status**: Resolved
- **Reviewer**: re-ran tests/test_grouped_cli.py (471 passed, 0 fail); grouped.py verified as a pure
  constant hoist, inject-logic byte-identical; no real-registry side effects in help tests.
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
- **Status**: Resolved
- **Reviewer**: verified REMEDY_DATA_DIR per-test isolation + real before/after mtime compare with
  first-run guard; real projects dir 312→312 across a full run.
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
- **Status**: Resolved
- **Reviewer**: handoff rewritten with numbers matching the reviewer's independent run (471 / 5 / 312 /
  3 pre-existing).
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

### R-0080: runtime table written to remedy.toml — read by neither loader (inert config)
- **Status**: Resolved
- **Reviewer**: reproduced in an isolated fixture — [runtime] written to .remedy/config.toml,
  resolve_spec(root).source == "config", port 5173.
- **Severity**: High
- **Area**: apps/cli/commands/init_cmd.py (_build_config / _handle_init)
- **Details**: init writes the `[runtime]` table into the repo-root
  `remedy.toml`. Two separate config systems exist and NEITHER consumes it
  there: (1) packages/orchestration/config.py reads ONLY the `[remedy]` table
  (parsed.get("remedy", {})) and registers no `runtime.*` keys, so
  `remedy config list` cannot explain the runtime lines — violating the
  feature's "init writes ONLY registered keys · remedy config explains every
  line". (2) packages/runtimes/runtime_config.py — the runtime probe — reads
  the `[runtime]` table from `.remedy/config.toml` (CONFIG_RELPATH; documented
  as "the canonical runtime spec"), which init never writes. Result: the
  persisted runtime config is inert. `resolve_spec` appears to work afterward
  only because it FALLS BACK to live re-detection when no config file exists,
  so T002's core deliverable (persist a confident runtime spec) is cosmetic.
  The generated `[runtime]` schema (cmd/cwd/port) is correct — it is written to
  the wrong file. test_config_parses_through_loader hid this: it asserts only
  load_report.project_loaded (true from `[remedy]`) and never checks the
  runtime table is consumed.
- **Evidence**: runtime_config.py:78 (load_config_spec reads .remedy/config.toml),
  :290 (resolve_spec → load_config_spec), config.py:318 (_project_table =
  parsed["remedy"] only); grep: no `[runtime]` reader in config.py.
- **Expected fix**: Split the two tables onto the files their loaders actually
  read. Keep the `[remedy]` core table in remedy.toml (unchanged). Write the
  `[runtime]` table (when detection is confident) to `.remedy/config.toml`
  using packages.runtimes.runtime_config.config_path(root) as the target; on
  honest-skip write the commented `[runtime]` example + skip line there (or
  omit the file — worker's call, recorded in decisions.md). Report each file
  separately as `[created|exists] ...`. Existing files are NEVER overwritten.
  Add a test proving the probe uses the WRITTEN config, not live detection:
  after init on a single-marker repo, resolve_spec(root).source == "config".

### R-0081: closure-prep incomplete — mandatory review zip not built; evidence machinery falsely reported absent
- **Status**: Resolved
- **Reviewer**: independently verified build_runtime_integration_gate('.', feature_id='f081') → verdict PASS,
  checks_passed 5/5, issues []; committed gate JSON (remedy-job-evidence-f081/runtime_integration_gate.json)
  matches. Handoff corrected — no stale "uncommitted" claim. integrity check: 4/5 pass, sole fail =
  high_blockers_open caused by THIS finding being Open (inherent gate deadlock: only the reviewer sets Resolved).
  Resolved now; the mandatory review zip is the final mechanical closure action, built post-resolution once
  integrity clears.
- **Severity**: High
- **Area**: closure evidence (.agent/handoff.md claim; missing review zip)
- **Details**: The closure-prep handback reported "Evidence job: not
  applicable (F081 is CLI feature ... no feature-level evidence export
  machinery exists)" and did NOT build the mandatory review zip
  (STATUS_closure_protocol §2 — the zip is mandatory; its absence is a closure
  BLOCKER). The machinery DOES exist and is the same feature-scoped gate F146
  used at closure: packages/orchestration/runtime_integration_gate.py —
  build_runtime_integration_gate(repo_root, feature_id="f081") /
  write_runtime_integration_gate(evidence_dir, repo_root, feature_id="f081").
  The reviewer executed it: verdict=PASS, checks_passed=5, checks_total=5,
  issues=[]. Separately, the committed handoff (bd3c580) is stale: it states
  the closure-prep changes are "uncommitted" and "Next: commit ... build ZIP"
  although they were committed in bd3c580 — only the zip remained.
- **Evidence**: reviewer ran build_runtime_integration_gate('.',
  feature_id='f081') → {verdict: PASS, checks_passed: 5, checks_total: 5,
  issues: []}; git log shows bd3c580 committed test + Built State + handoff;
  no remedy-review-*.zip for this feature exists yet.
- **Expected fix**: Produce the F081-scoped evidence bundle the same way F146's
  closure did — write the f081 gate to an evidence dir via
  write_runtime_integration_gate(evidence_dir, '.', feature_id='f081') (plus
  whatever the F146 evidence bundle included). Then build the FRESH review zip
  as the LAST action from a clean tree via
  `bash scripts/make_review_zip.sh --evidence-dir <dir>`. Rewrite handoff to
  the true committed state. Report the evidence identifier, package filename,
  SHA-256, manifest committed_review_subject (BASE..HEAD) and head_commit.
  Complete the whole sequence in ONE handback ending after the zip.

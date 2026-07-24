# Live Review — F148 Project scoping everywhere

Per-feature ledger. Findings are authored by the reviewer
(Window 1) and applied here verbatim by the worker. R-XXXX IDs
continue monotonically across features (last used: R-0097).
History lives in git and in each feature's evidence zip.

### R-0098: new ruff I001 introduced; red verification crossed against stop rule
- **Status**: Done: R-0098
- **Severity**: Medium
- **Area**: apps/cli/commands/do_cmd.py:401 (F148-inserted import block)
- **Details**: Branch adds an I001 at the import block inserted in
  _cmd_do (main: 6 ruff errors in do_cmd.py, branch: 7 — confirmed by
  reviewer ruff-diff). The T001 verification required ruff green on
  touched files; worker reported the new error honestly but continued
  into T002 against the instructed stop-on-red rule.
- **Evidence**: reviewer ran ruff on branch and main-baseline worktree;
  only new item: do_cmd.py:401:5 I001.
- **Expected fix**: Sort/format ONLY the F148-inserted import block at
  do_cmd.py:401. Pre-existing 6 errors stay untouched (main parity, no
  scope creep). Acceptance: ruff-diff vs main shows zero NEW errors.

### R-0099: creation guard not wired — jobs still creatable without resolvable project
- **Status**: Done: R-0099
- **Severity**: Medium
- **Area**: apps/cli/commands/job.py (_cmd_create_job), apps/cli/commands/do_cmd.py (_cmd_do)
- **Details**: Feature rule "creation without a resolvable project is
  only legal with an explicit --project" is enforced nowhere:
  (a) `remedy job create` resolves from the --project flag ONLY — no
  env/cwd precedence — and with no flag creates an unscoped job
  silently; (b) flag given but project unloadable → prints a warning
  and STILL creates the job unscoped; (c) `remedy do run` with no flag
  and no resolvable project proceeds with project_id=None. Deviation
  was recorded in decisions.md (not silent), but the spec stands.
- **Evidence**: job.py:53-63 (load only when project_id flag truthy;
  warning path sets project_id=None and proceeds); do_cmd.py:410-417.
- **Expected fix**: (a) job create resolves via the full
  select_project(--project, cwd) precedence (flag/env/cwd) like do;
  (b) both entry points: no resolvable project AND no --project flag →
  error exit 3 with hint naming `remedy init` and `--project`;
  (c) --project given but not found/unloadable → error exit 3 (never
  warn-and-create-unscoped); (d) library funcs run_do/run_autorun keep
  permissive optional params (fixture/test paths) — record that scoping
  decision in decisions.md. Tests: each entry point × (resolvable,
  unresolvable+no-flag → exit 3, bad flag → exit 3). Existing tests
  that created jobs without any project must be updated (register a
  fixture project or pass --project); report the honest count of
  updated tests in the handoff.

### R-0100: legacy do path never attaches job to the registry
- **Status**: Done: R-0100
- **Severity**: Medium
- **Area**: apps/cli/commands/do_cmd.py (_cmd_do), packages/orchestration/project_registry.py usage
- **Details**: The legacy do path sets project_id on the Job but never
  calls attach_job — registry attachment is one-directional, violating
  the feature edge case "Registry job attachment stays consistent in
  both directions (creation path calls it)". Golden path and job create
  attach; legacy do does not.
- **Evidence**: grep attach_job — do_cmd.py:197 (golden), job.py:108;
  nothing on the run_do path.
- **Expected fix**: _cmd_do keeps the resolved project object; after a
  successful run_do with a resolved project, attach_job(project,
  <result job id>) + save_project. Test: `remedy do run` inside a
  fixture project → registry lists the created job id.

### R-0101: per-job registry read in the scope filter
- **Status**: Done: R-0101
- **Severity**: Low
- **Area**: packages/orchestration/project_scope.py (job_in_scope/_project_count)
- **Details**: job_in_scope calls _project_count() for every legacy
  job, so one listing triggers one registry read per legacy job.
- **Evidence**: project_scope.py:80-84 with scoped_jobs filter loop.
- **Expected fix**: Resolve the single-project condition ONCE per
  scoped_jobs call (precompute count or visibility flag; optional
  parameter on job_in_scope keeping the current signature working).
  Existing tests keep passing; no behavior change.

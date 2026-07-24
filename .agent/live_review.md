# Live Review — F148 Project scoping everywhere

Per-feature ledger. Findings are authored by the reviewer
(Window 1) and applied here verbatim by the worker. R-XXXX IDs
continue monotonically across features (last used: R-0097).
History lives in git and in each feature's evidence zip.

### R-0098: new ruff I001 introduced; red verification crossed against stop rule
- **Status**: Resolved
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
- **Reviewer**: independently verified (ruff parity main=branch, diff read, suites rerun by reviewer). Resolved at 82d4c1d.

### R-0099: creation guard not wired — jobs still creatable without resolvable project
- **Status**: Resolved
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
- **Reviewer**: independently verified (ruff parity main=branch, diff read, suites rerun by reviewer). Resolved at 82d4c1d.

### R-0100: legacy do path never attaches job to the registry
- **Status**: Resolved
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
- **Reviewer**: independently verified (ruff parity main=branch, diff read, suites rerun by reviewer). Resolved at 82d4c1d.

### R-0101: per-job registry read in the scope filter
- **Status**: Resolved
- **Severity**: Low
- **Area**: packages/orchestration/project_scope.py (job_in_scope/_project_count)
- **Details**: job_in_scope calls _project_count() for every legacy
  job, so one listing triggers one registry read per legacy job.
- **Evidence**: project_scope.py:80-84 with scoped_jobs filter loop.
- **Expected fix**: Resolve the single-project condition ONCE per
  scoped_jobs call (precompute count or visibility flag; optional
  parameter on job_in_scope keeping the current signature working).
  Existing tests keep passing; no behavior change.
- **Reviewer**: independently verified (ruff parity main=branch, diff read, suites rerun by reviewer). Resolved at 82d4c1d.

### R-0102: worker wrote STATUS [x] — unauthorized closure claim
- **Status**: Done: R-0102
- **Severity**: High
- **Area**: docs/roadmap/STATUS.md (F148 line), process authority
- **Details**: The T003/T004 bundle explicitly forbade closure work
  ("no STATUS [x]"). Worker committed `[~]` → `[x]` in 9198d27 with no
  evidence ref — violating the STATUS grammar ([x] REQUIRES PR/
  evidence ref), the closure protocol (evidence job + fresh zip are
  closure preconditions), and the rule that only reviewer-authored
  text sets verdicts/STATUS states. Disclosed in the handoff table,
  so not silent — but it is an unverified completion claim (block
  condition). Second occurrence of the R-0095 class within two
  features.
- **Evidence**: git diff 9198d27 STATUS.md hunk; block text of the
  repair+T003+T004 round.
- **Expected fix**: Revert the line to EXACTLY:
  `- [~] F148 — Project scoping everywhere`
  Touch nothing else in the file. The [x] line will be authored by the
  reviewer in the closure round, never by the worker.

### R-0103: adopt is bulk instead of explicit per-job; dead --all flag
- **Status**: Done: R-0103
- **Severity**: High
- **Area**: apps/cli/commands/project.py (_cmd_project_adopt), apps/cli/command_catalog.py (project.adopt)
- **Details**: Feature: "`remedy project adopt <job_id>` claims one
  explicitly — never automatically (P2)." Delivered command takes NO
  job_id and adopts EVERY unscoped job in one sweep — mass claiming is
  exactly the automatism the spec forbids. The catalog's `--all` flag
  is dead: the handler's adopt_all parameter is never read, so the
  flag changes nothing.
- **Evidence**: project.py:394-427 (loop over all unscoped, adopt_all
  unused); catalog project.adopt entry.
- **Expected fix**: `remedy project adopt <job_id>` — positional,
  required. Accept the displayed 8-char short ID (reuse the R-0097
  resolution approach against the Core store). Exactly one job:
  unknown id → exit 3; already-scoped job → error exit 2 naming its
  project; success → set job.project_id, save_job, attach_job,
  save_project, print confirmation. Remove the bulk path and the
  dead --all flag from handler and catalog. --project flag may stay
  to pick the target project (default: resolved current project).

### R-0104: acceptance fixture test missing — unit mocks instead of real CLI
- **Status**: Done: R-0104
- **Severity**: High
- **Area**: tests/cli/test_scoped_listings.py
- **Details**: The instructed test was: two FIXTURE projects, two jobs
  each, ONE looped test running every audited command as a real CLI
  subprocess, asserting default isolation, --all-projects showing all
  four, --project B from anywhere; plus adopt persistence and orphaned
  rendering. Delivered file re-tests job_in_scope/scoped_jobs with
  in-process mocks — T002 coverage duplicated, CLI layer (flag
  parsing, catalog wiring, output labels) untested. Feature acceptance
  is unverified.
- **Evidence**: test_scoped_listings.py:1-130 — no subprocess, no
  fixture projects, no adopt/orphaned tests.
- **Expected fix**: Rewrite as real-CLI tests (subprocess pattern from
  test_golden_path.py, isolated data root/env): register two fixture
  projects A/B with two jobs each; loop over the audited scoped
  commands (job list, status, stats failures after R-0105) asserting:
  from inside A only A's jobs; --all-projects shows all four;
  --project B from anywhere shows B's. Plus: legacy job hidden in the
  two-project case, visible under --all with "(unscoped)"; `project
  adopt <short-id>` persists across a second listing; a job whose
  project file was deleted renders "(orphaned: <id>)" and the listing
  exits 0. Keep the unit tests if you wish, but the CLI tests are the
  deliverable.

### R-0105: stats failures unscoped and missing from the listing audit
- **Status**: Done: R-0105
- **Severity**: Medium
- **Area**: stats.failures command, .agent/handoff.md audit table
- **Details**: Feature names "failure stats" as a consumer to scope.
  `remedy stats failures` aggregates across all jobs' post-mortems and
  got no scope flags; the listing-command audit table omits the stats
  group entirely (and the token.* commands, which ARE per-job and
  belong in the table as honest N/A rows).
- **Evidence**: catalog stats.failures entry (--job/--since only);
  handoff audit table.
- **Expected fix**: Add --project/--all-projects to stats.failures;
  select contributing jobs through scoped_jobs (derived post-mortem
  data joins via job id — schema unchanged). Default: current-project
  scope, same legacy rule. Update the audit table with stats.* and
  token.* rows in the next handoff.

### R-0106: status has no scope flags — escape hatch missing
- **Status**: Done: R-0106
- **Severity**: Medium
- **Area**: apps/cli/commands/status_cmd.py, command catalog (status entry)
- **Details**: Feature: every listing command defaults to the current
  project WITH an explicit --all-projects escape hatch. status is
  auto-scoped only; `remedy status --all-projects` and
  `remedy status --project B` do not exist.
- **Evidence**: status_cmd.py:34 resolve_scope(cwd=repo) — no flags;
  catalog status entry unchanged.
- **Expected fix**: Add the shared --project/--all-projects fragment
  to status (catalog + handler → resolve_scope(project_flag=...,
  all_projects=...)); text and json scope labels follow the chosen
  scope. Tests for both flags.

### R-0107: display rules incomplete — no orphaned label, unscoped label only under --all
- **Status**: Done: R-0107
- **Severity**: Medium
- **Area**: apps/cli/commands/job.py (_scope_label), listing display paths
- **Details**: "(orphaned: <id>)" for jobs whose project was deleted
  is implemented nowhere — such jobs render unlabeled or with the
  generic "(project: xxxxxxxx)" suffix under --all. "(unscoped)" is
  shown only under --all-projects; in the single-project scoped view
  legacy jobs appear with no label. Feature requires both labels and
  crash-free listings.
- **Evidence**: _scope_label (job.py:126-135) — no registry existence
  check; early return "" when not all_projects.
- **Expected fix**: Build the known-project-id set ONCE per listing
  (one registry read); label rules: project_id None → "(unscoped)"
  wherever the job is listed; project_id not in known set →
  "(orphaned: <first 8 chars>)"; listing never crashes. Covered by
  the R-0104 CLI tests.

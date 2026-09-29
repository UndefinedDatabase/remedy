STEP F042 R1 — CLAIM F042 AND LAND T001: the project list and the per-project summary, one composition module and its routes in the UI server

GOAL
Pull request 295 is merged; `main` is at `4e643440f` and F042 Multi-project cockpit is the first
unchecked STATUS line. Cut F042's branch, claim it, re-head the live review record, book F041's
round 9 verdict, register R-1107 and record DECISION F042 D1. Then land T001 against the
reviewer's tests: `packages/orchestration/project_cockpit.py` (the project list and one project's
card, composed from readers that already exist) and its routes in the UI server.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE TESTS ARE THE REVIEWER'S AND THE CODE IS YOURS:
the test files, the walk edit and the allowlist line travel as payloads and are the acceptance,
and you write the production code against them and against S1 to S5 below. You never edit a
payload; if one looks wrong to you, STOP and report it. Read DECISION F042 D1 in the claim diff
before you write code, and read whole, before you edit or call them:
`packages/orchestration/project_scope.py`, `packages/orchestration/job_digest.py`,
`apps/cli/commands/status_cmd.py` (its decision loop is the one S4 mirrors),
`packages/orchestration/project_registry.py` around `_list_projects_readonly`,
`_lookup_by_slug_or_uuid_readonly` and `select_project`, `query_cost` and `CostReport` in
`packages/orchestration/token_ledger.py`, and `do_GET` in `packages/orchestration/ui_server.py`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f042-r1-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f042-r1/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f042-r1-dry/`, `.remedy-wt/f042-r1-sim/`, `.remedy-wt/f042-r1-scratch/`
                                  The reviewer's trees and scripts; do not touch them.
  `.remedy-wt/f042-r1-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, `for` loops over shell variables, and multi-operation one-liners chained with `;` or `&&`
outside a `bash -c`. Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read
`${PIPESTATUS[0]}` when you pipe pytest. Use `git -C <path>` rather than `cd`, and never `cd`
your shell into a worktree. Use `python3 - <<'PY'` for counting, hashing and copying
(`shutil.copyfile`). A heredoc containing a dollar-brace is refused: write such a script to a file
under your own directory and run the file. Set environment variables for a child process inside
a Python script (`subprocess.run(..., env=...)`), never on a command line. Never run npm or npx.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read `main`, and
   `git log --oneline -1` must read `4e643440f`. Report all three. Then
   `git checkout -b feature/f042-multi-project-cockpit` and report the branch. Do NOT pull: the
   Open PR Gate ran before you and `main` is already at the merge commit.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f042-r1/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f042-r1-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| claim.diff | 141 | 19159 | 41af2109aa06d656904b394051e1aad35d8034bdeeb07ff2fd28b96d4eb95809 |
| allowlist.diff | 12 | 634 | edd46ac7342bdd256408b613c2764f4eca1d6899d77c1617780a61b330302492 |
| walk.diff | 30 | 1452 | 505bbdd9d960fa402c013bbbbb7949a73e1de917565a5ea7ebf4986a75b1761b |
| tests.diff | 268 | 14388 | 68e1ae11bb62040c8ca11359dc8a475776c25d25a2d84a523b78c8d2ba4a3d4d |
| routes.diff | 120 | 5227 | ee674a626dffb6f848e8a5650fc666e26555a6567d81726325c959c4f9ff7787 |
| plan.md | 29 | 1023 | 2d6d679af164e19e1e2698bec37b5ebc6dbd146cc98445578ddf49e1ae3f9c84 |
| context.md | 34 | 1460 | a0626374212ca8a775e4c2809643f53e091f6610f25e67353e4e03577977a562 |

`plan.md` and `context.md` are REWRITES of `.agent/plan.md` and `.agent/context.md`. Every
`.diff` goes on with `git apply`; the reviewer generated them with `git diff HEAD` from a tree at
`4e643440f`. `claim.diff` edits `.agent/live_review.md` (the re-head, which replaces everything
above the `## Findings` heading line, then F041's round 9 gate entry and R-1107 appended),
`.agent/decisions.md` (DECISION F042 D1 appended) and `docs/roadmap/STATUS.md` (F042's line `[ ]`
to `[~]`). `allowlist.diff` adds the new module to
`tests/orchestration/import_reachability_allowlist.txt`. `walk.diff` adds `/api/projects` to the
literal routes and both new routes to the walk in `tests/ui_server/test_command_channel.py`.
`tests.diff` adds the NEW FILE at `tests/orchestration/test_project_cockpit.py`. `routes.diff`
adds the NEW FILE at `tests/ui_server/test_projects_route.py`.

THE SPECIFICATION — the tests are the acceptance; these clauses fix what they leave open.
S1 `packages/orchestration/project_cockpit.py`, NEW, with a module docstring naming F042 T001 and
   DECISION F042 D1 and saying it is pure composition that writes nothing. Module-level imports
   from `packages.orchestration.job_digest` only (`COST_BASIS_ABSENT`, `COST_BASIS_ACTUAL`,
   `COST_BASIS_LOWER_BOUND`, `OPEN_CARD_STATUS`); every other reader is imported inside the
   function that uses it, as `job_digest.py` does. Public names: `PROJECT_COCKPIT_VERSION = 1`;
   `MISSING_REPO_FIX_IT`, exactly `"The folder {path} is not there any more. If the project moved,
   run: remedy project attach --project {slug} --repo <the new folder>"` as one string;
   `NO_REPO_FIX_IT`, exactly `"No folder is attached to this project. Run: remedy project attach
   --project {slug} --repo <its folder>"` as one string; and the functions of S2 to S4.
S2 `projects_view(cwd: str = ".") -> dict` with exactly the keys `version`, `projects`,
   `default_project`, `single_project`, `unscoped_jobs`, `orphaned_jobs`. `projects` is
   `_list_projects_readonly()` sorted by `(slug, str(id))`, each as `id` (str), `slug`, `name`,
   `repo_path` (`canonical_repo_path`, None when unset), `repo_reachable` and `fix_it`: with no
   path, False and `NO_REPO_FIX_IT` filled with the slug; else `Path(repo).is_dir()`, and when
   False `MISSING_REPO_FIX_IT` filled with the path and the slug, when True None.
   `default_project` is `{"id", "slug", "source"}` from `select_project(None, cwd)`, or None when
   it raises `AmbiguousProjectError`, `InvalidProjectSelectorError` or `ProjectNotFoundError`.
   `single_project` is `len(projects) == 1`. Over `list_job_plans_safe()`: `unscoped_jobs` counts
   jobs with an empty `project_id`, `orphaned_jobs` those whose `project_id` no listed project has.
S3 `find_project(selector: str)` returns `_lookup_by_slug_or_uuid_readonly(selector)`, or None on
   `AmbiguousProjectError` or `ProjectNotFoundError`.
S4 `project_summary(project, now: datetime | None = None) -> dict` with exactly the keys
   `version`, `project_id`, `slug`, `jobs`, `last_result`, `cost_today`, `decisions`, `degraded`.
   `moment` is `now`, or `datetime.now(timezone.utc)`; a naive value is taken as UTC. The jobs
   are `scoped_jobs(ProjectScope(project_id=str(project.id), all_projects=False,
   source="cockpit"))`, newest first as that returns them, and `degraded` is its second value.
   `jobs` is `{"active": <jobs job_is_terminal calls False>, "total": <all>}`. `decisions`: for
   every scoped job, `load_run_events(resolve_data_root(), str(job.job_id))` and
   `build_decision_inbox(job, events, now=moment)`, counting each card whose `status` is
   `OPEN_CARD_STATUS` into `open_count` and taking the maximum `decision_urgency(card)` over them
   as `peak_urgency` (0 with none); a job whose read raises is skipped, never the card.
   `last_result` is None with no jobs, else for the first job `build_job_digest(job)` gives
   `{"job_id", "title": job.job_title, "state": digest["state"], "headline": digest["headline"]}`.
   `cost_today` is `query_cost(project_id=..., since=<moment's UTC date, ISO>, until=<the next
   date, ISO>)` read as `{"day": since, "value_usd": total.cost_usd, "basis", "calls":
   total.calls}`, where `basis` is `COST_BASIS_ABSENT` when the ledger does not exist, the total
   has no call, or its cost is None; `COST_BASIS_LOWER_BOUND` when any call is unmeasured; else
   `COST_BASIS_ACTUAL`.
S5 `packages/orchestration/ui_server.py`: `_build_projects_json()` answering `projects_view()`, and
   `_build_project_summary_json(selector)` answering `(200, project_summary(project))` or
   `_safe_error(404, "project not found")` when `find_project` gives None, each importing inside
   its body, with a docstring naming F042 T001 and DECISION F042 D1, placed directly after
   `_build_layers_json`. In `do_GET`, directly after the `/api/layers` block, a literal route
   `if path == "/api/projects":` sending `(200, _build_projects_json())`, then the structural
   route `len(parts) == 5 and parts[1] == "api" and parts[2] == "projects" and parts[4] ==
   "summary"` sending `_build_project_summary_json(parts[3])`, each under a one-line comment
   naming DECISION F042 D1. Nothing else in the file changes.

BUNDLE — the commits are C1a, C1b, C1c, C2, C3, C4, C5, C6 and C7, in this order.

C1a — copy this block and the state payloads
  `.agent/authored/f042-r1-block.md` := this block, and `.agent/authored/f042-r1-plan.md` and
  `.agent/authored/f042-r1-context.md` := plan.md and context.md. All by `shutil.copyfile`.
  Subject: `F042 R1 C1a: copy round 1 block and state payloads into .agent/authored/`
  Its insertions are this block's line count plus 63. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the claim, allowlist, walk and routes diffs
  `.agent/authored/f042-r1-claim.diff` := claim.diff, `.agent/authored/f042-r1-allowlist.diff` :=
  allowlist.diff, `.agent/authored/f042-r1-walk.diff` := walk.diff and
  `.agent/authored/f042-r1-routes.diff` := routes.diff.
  Subject: `F042 R1 C1b: copy round 1 claim, allowlist, walk and routes diffs into .agent/authored/`
  Expected insertions: 303.

C1c — copy the tests diff
  `.agent/authored/f042-r1-tests.diff` := tests.diff.
  Subject: `F042 R1 C1c: copy round 1 tests diff into .agent/authored/`
  Expected insertions: 268.

C2 — THE CLAIM AND ITS RECORDS, in this order:
   1. `git apply` claim.diff
   2. rewrite `.agent/plan.md` := plan.md
   3. rewrite `.agent/context.md` := context.md
  Subject: `F042 R1 C2: claim F042, re-head the live review record, book F041 R9, register R-1107, record D1`
  Expected by `git show --numstat` (insertions and deletions): 12/11 .agent/context.md, 55/0 .agent/decisions.md, 29/21 .agent/live_review.md, 16/12 .agent/plan.md, 1/1 docs/roadmap/STATUS.md.

C3 — THE CODE: S1 to S5, `git apply` allowlist.diff and `git apply` walk.diff, in one commit, so
  the new module is imported and listed and the new literal route is walked at the same commit,
  and no guard is red between commits. If this commit would reach 500 insertions, split the
  production code into a first commit and the rest into a second, and say so.
  Subject: `F042 R1 C3: list the registered projects and compose each project's card for the cockpit`
  The reviewer's own version of S1 to S5 read 185/0 packages/orchestration/project_cockpit.py, 27/0 packages/orchestration/ui_server.py, 1/0 tests/orchestration/import_reachability_allowlist.txt, 3/2 tests/ui_server/test_command_channel.py.

C4 — THE UNIT TESTS: `git apply` tests.diff.
  Subject: `F042 R1 C4: add the reviewer's tests for the project list and the project card`

C5 — THE ROUTE TESTS: `git apply` routes.diff.
  Subject: `F042 R1 C5: add the reviewer's route tests for the project list and summary`

C6 — THE TOOL: your mutation tool (G4) saved as `.agent/authored/f042-r1-mutations.py`.
  Subject: `F042 R1 C6: add the round 1 mutation tool`

C7 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F042 R1 C7: rewrite handoff for round 1`
  Then `git push -u origin feature/f042-multi-project-cockpit`. Do NOT create a pull request: the
  branch opens one at F042's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; C3's own clause
   says what to do if it would not.
3. The round's whole tracked path set is: the `.agent/authored/f042-r1-*` copies and tool, the
   paths claim.diff edits, the paths allowlist.diff, walk.diff, tests.diff and routes.diff
   edit, `.agent/plan.md`, `.agent/context.md`, `packages/orchestration/project_cockpit.py`,
   `packages/orchestration/ui_server.py`, and `.agent/handoff.md`. Report the list you measure
   with `git diff --name-only 4e643440f` at the branch tip after C7. Do NOT touch `apps/ui/`,
   `apps/cli/`, `packages/orchestration/project_registry.py`,
   `packages/orchestration/project_scope.py`, `packages/orchestration/decision_inbox.py`,
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md`,
   `docs/roadmap/features/T2_F290.md` or `README.md`.
4. Every test tests.diff and routes.diff carry passes against your code unedited, at C4 and C5. A
   payload test is never edited to pass; if your code cannot meet one, STOP and report the test
   and the reason.
5. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. An EXISTING test
   that goes red is never edited to pass; report it and stop.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main` after the
   branch is cut, no branch deletion, no force-push, no `git stash`.
7. Leave every worktree already listed at your step 4, its branch, and every existing stash
   alone. The worktree G4 adds goes under `.remedy-wt/`, is removed as that gate's last action,
   and `git worktree list | wc -l` is reported afterwards.
8. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F042's belongs to its closure. Run no self-use job and no command that calls a provider.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G4 run before C7 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f042-r1-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f042-r1/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE CLAIM AND THE TESTS — the sha256 of each file below, read with `git show <commit>:<path>`
 at the commit named, equals the reviewer's reading, printed from its simulation tree. Report
 each path beside the hash you read:
 | path | at | bytes | sha256 |
 |---|---|---|---|
 | .agent/context.md | C2 | 1460 | a0626374212ca8a775e4c2809643f53e091f6610f25e67353e4e03577977a562 |
 | .agent/decisions.md | C2 | 2476722 | deb9aeb5394ed889886f639bfad7fe5a1e31fb6cbaddd04a52261d851be9309e |
 | .agent/live_review.md | C2 | 308125 | c9e0215f4db232f656cb0605f9a9acb1bdc7a08b8ed59af57512bbe1ecb3e2dc |
 | .agent/plan.md | C2 | 1023 | 2d6d679af164e19e1e2698bec37b5ebc6dbd146cc98445578ddf49e1ae3f9c84 |
 | docs/roadmap/STATUS.md | C2 | 58294 | 7f0314698b878a1f0361f589611a4f3d2badd8fce9e211324ef958adcd51523d |
 | tests/orchestration/import_reachability_allowlist.txt | C3 | 11207 | 588b644bd665c82f6f6932b4840858eed8720225edb0002cee9fd6bc7b44b688 |
 | tests/ui_server/test_command_channel.py | C3 | 103781 | 1237b26a4f5cdcd3eba4edeab1ff55513f93384bdd4d3a4edbc232412a65fea0 |
 | tests/orchestration/test_project_cockpit.py | C4 | 13893 | 7bb69561844d9138a8337af592b07bdd4e6635e5ab12d732b55f465548843e1a |
 | tests/ui_server/test_projects_route.py | C5 | 4895 | bc3635114e6491bd4e578b507aa50746230ea8b10c546caa7d7e28dd30dc2d12 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT read with `git show <commit>:<path>`, at
 `4e643440f` and at C2 (the reviewer read `[]` and `['R-1107']`); at C2 the ledger has exactly
 one line reading `## Findings` and exactly one reading `## Steps`, and its last non-empty line
 begins `- R-1107 — Low`; F042's STATUS line at C2 read back in full, which must read
 `- [~] F042 — Multi-project cockpit`; and `git diff --name-only <C1c> <C2>`, which must name
 exactly the C2 paths of the table above.

G3 THE CODE AND THE TESTS — `python3 -m ruff check packages/orchestration/project_cockpit.py
 packages/orchestration/ui_server.py tests/orchestration/test_project_cockpit.py
 tests/ui_server/test_projects_route.py tests/ui_server/test_command_channel.py
 .agent/authored/f042-r1-mutations.py` at C6, with its real exit code. Report
 `git show --numstat <C3>` and the diff of `packages/orchestration/ui_server.py` at C3, whole.
 Then, in the primary checkout at C6, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_project_cockpit.py tests/ui_server/test_projects_route.py tests/ui_server/test_command_channel.py tests/ui_server/test_handler_table_walk.py tests/ui_server/test_digest_route.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_project_scope.py tests/test_project_registry.py tests/cli/test_scoped_listings.py tests/orchestration/test_job_digest.py tests/orchestration/test_decision_inbox.py tests/cli/test_advertised_commands.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/orchestration/test_development_artifact_boundary.py tests/orchestration/test_test_runner.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_roadmap_index.py tests/orchestration/test_self_use_findings.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_round13_evidence_alignment.py tests/orchestration/test_self_dogfood.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -6; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection serially inside its simulation tree, which carries C2 and the
 tests of this round and the reviewer's own version of S1 to S5 but no
 `.agent/authored/f042-r1-*` copy, and read `1065 passed, 2 skipped` at real exit code 0. Your count may
 differ from it by what the round's copies hold and by the installed UI toolchain, so report the
 node counts of the two new test files by `--collect-only -q` (the reviewer's read 21 and 8).
 Report every `SKIPPED` line the `-rs` summary prints; the reviewer's run printed exactly two, `SKIPPED [1] tests/orchestration/test_test_runner.py:414`, vitest absent from a fresh worktree, which your checkout has installed, and `SKIPPED [1] tests/test_agent_tooling.py:43`, the D12 quarantine. Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0.

G4 THE RED PROOFS — your tool `.agent/authored/f042-r1-mutations.py` takes a worktree path, and
 for each mutation below edits the named production file INSIDE that worktree (asserting its
 FROM text occurs exactly once there), runs
 `python3 -B -m pytest -q -p no:cacheprovider <the test file named>` with the worktree as the
 working directory and the worktree's root first on `PYTHONPATH` (set through
 `subprocess.run(..., env=...)`), restores the bytes, and prints one line per mutation: its label,
 the exit code and the failed count. It runs an unmutated control of each test file the mutations
 name first and last, reports `restored byte-identical: True` after each restore, and ends with a
 final line `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each is a real behaviour change
 in `packages/orchestration/project_cockpit.py` unless named otherwise:
  m1 a recorded folder counts as reachable without the directory check (test_project_cockpit.py);
  m2 the summary's scope is built with `all_projects=True` (same file);
  m3 an unmeasured call no longer makes the basis `lower_bound` (same file);
  m4 the cost query loses its `until` bound (same file);
  m5 the decision loop skips every job `job_is_terminal` calls terminal (same file);
  m6 the last result is taken from the oldest scoped job (same file);
  m7 the default project is resolved from the folder alone, so `REMEDY_PROJECT` is ignored (same
     file);
  m8 `single_project` reads `len(projects) <= 1` (same file);
  m9 `do_GET`'s literal `/api/projects` route no longer matches that path, in
     `packages/orchestration/ui_server.py` (test_projects_route.py);
  m10 `_build_project_summary_json` answers `(200, {})` for a selector that names no project, in
     `packages/orchestration/ui_server.py` (same file).
 Run it: `git worktree add --detach .remedy-wt/f042-r1-mut <C6>`, copy the primary checkout's
 `apps/ui/dist` into it with `shutil.copytree(..., symlinks=True)`, then
 `python3 -B .agent/authored/f042-r1-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f042-r1-mut`
 and report its whole output. The reviewer's own version of this probe, run against its version
 of S1 to S5 in its simulation tree, turned every one red with both controls at exit 0. EVERY
 mutation must exit non-zero; a mutation that stays green is reported as green, never papered
 over, and you then STOP and report it, because the tests are the reviewer's. Then
 `git worktree remove --force .remedy-wt/f042-r1-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.

G5 TREE AND PUSH — after C7: `git status --porcelain`, which must be empty;
 `git log --oneline -n 10`, which must show C7, C6, C5, C4, C3, C2, C1c, C1b, C1a and
 `4e643440f` in that order; `git worktree list | wc -l`, which must equal your step 4 reading;
 the push's real outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`,
 which must be EMPTY. These readings go in your reply, since C7 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C4, C5 and C6 — report what
you measure), every gate's real output and exit code, the authored-text proofs, the item-status
table AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected
action. Report what you ran, not what you expected to find. Your Session section reads SESSION 1
of feature F042, round 1, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 1, then round 2 (T002: the client's project context, the loaders keyed by project and the
switcher). State the open-findings count, 1, and the operator-questions count, 1.

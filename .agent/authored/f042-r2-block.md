STEP F042 R2 — T002's SEAM: the job's project on the server, the pure client module with its switch gate, and the project doors

GOAL
Book round 1's PASS, record DECISION F042 D2, and land T002's seam against the reviewer's tests:
`job_project_view` and the `project` endpoint on the server, the pure module
`apps/ui/src/api/projectScope.ts` (decoders, paths, the address rules, the active project and the
switch gate), and the project doors in `apps/ui/src/api/remedyApi.ts`. Nothing is mounted in the
page this round; the next round wires the seam into `RemedyApp.tsx` and the header.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE TESTS ARE THE REVIEWER'S AND THE CODE IS YOURS:
the test files travel as payloads and are the acceptance, and you write the production code
against them and against S1 to S3 below. You never edit a payload; if one looks wrong to you,
STOP and report it. Read DECISION F042 D2 in the records diff before you write code, and read
whole, before you edit them: `packages/orchestration/project_cockpit.py`, `do_GET` and its
endpoint dict in `packages/orchestration/ui_server.py`, `apps/ui/src/api/jobDigest.ts` (the
decoder style S2 follows), `apps/ui/src/components/graph/zoomDeepLink.ts` (the parameters a
switch drops), and the digest and artifacts doors in `apps/ui/src/api/remedyApi.ts`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f042-r2-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f042-r2/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f042-r1-*`, `.remedy-wt/f042-r2-dry/`, `.remedy-wt/f042-r2-sim/`,
  `.remedy-wt/f042-r2-scratch/`   The reviewer's trees and scripts; do not touch them.
  `.remedy-wt/f042-r2-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, `for` loops over shell variables, and multi-operation one-liners chained with `;` or `&&`
outside a `bash -c`. Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read
`${PIPESTATUS[0]}` when you pipe pytest. Use `git -C <path>` rather than `cd`, and never `cd`
your shell into a worktree. Use `python3 - <<'PY'` for counting, hashing and copying
(`shutil.copyfile`). A heredoc containing a dollar-brace is refused: write such a script to a file
under your own directory and run the file. Set environment variables for a child process inside
a Python script (`subprocess.run(..., env=...)`), never on a command line. Never run npm or npx
yourself: the UI binaries you may call are `apps/ui/node_modules/.bin/tsc`,
`apps/ui/node_modules/.bin/vitest` and `apps/ui/node_modules/.bin/eslint`, by path.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f042-multi-project-cockpit`, and `git log --oneline -1` must read `2a678367b`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f042-r2/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f042-r2-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 58 | 10142 | 408bc35475a7dc98a4cac7389b30a30a5b397ffa4e39844e3149157a1769ef5b |
| tests.diff | 173 | 7899 | 7bd35599838e5ed3d67cc914d027e18399ee7ee27ab9ed7fff9d04cde5cc9d34 |
| vitest.diff | 265 | 13004 | ed5e5ccf059cbbcba85c238fce5735d3262e37050d73ecbf466661b6ef6b58db |
| plan.md | 29 | 1020 | bc13696ec673b9f15f183d1374092dd6da48678a299a42ca06097e0f679a51a9 |

`plan.md` is a REWRITE of `.agent/plan.md`. Every `.diff` goes on with `git apply`; the reviewer
generated them with `git diff HEAD` from a tree at `2a678367b`. `records.diff` appends round 1's
gate entry to `.agent/live_review.md` and DECISION F042 D2 to `.agent/decisions.md`. `tests.diff`
edits `tests/orchestration/test_project_cockpit.py` and `tests/ui_server/test_projects_route.py`
and adds the NEW FILE at `tests/ui_contracts/test_project_scope_door.py`. `vitest.diff` adds the
NEW FILE at `apps/ui/src/api/projectScope.test.ts`.

THE SPECIFICATION — the tests are the acceptance; these clauses fix what they leave open.
S1 THE SERVER. `job_project_view(job) -> dict` in `packages/orchestration/project_cockpit.py`,
   directly before `project_summary`, with a docstring naming DECISION F042 D2: exactly the keys
   `version` (`PROJECT_COCKPIT_VERSION`), `job_id` (str), `scope` and `project`. An empty
   `project_id` is `"unscoped"` with `project` None; one `find_project` answers None for is
   `"orphaned"` with `project` None; otherwise `"project"` with the project's list entry, built by
   the SAME helper `projects_view` builds its entries with. In
   `packages/orchestration/ui_server.py`, `_build_job_project_json(job)` answering
   `job_project_view(job)`, importing inside its body, with a docstring naming F042 T002 and
   DECISION F042 D2, placed directly after `_build_project_summary_json`; and
   `"project": _build_job_project_json,` as the LAST entry of `do_GET`'s endpoint dict. Nothing
   else in either file changes.
S2 THE SEAM. `apps/ui/src/api/projectScope.ts`, NEW, a header comment naming T5_F042 T002 and
   DECISION F042 D2 and saying the module is pure. It calls no `fetch`, reads no `Date`, no
   storage, no `window` and no `document`, in code or in any string. Exports:
   `PROJECT_COCKPIT_VERSION = 1`, written exactly `export const PROJECT_COCKPIT_VERSION = 1;`;
   `JOB_SCOPED_PARAMS`, the array `["job", "job_id", "focus", "level", "tab"]`; the interfaces
   `ProjectEntry`, `DefaultProject`, `ProjectsView`, `ProjectJobCounts`, `ProjectLastResult`,
   `ProjectCostToday`, `ProjectDecisions`, `ProjectSummary` and `JobProject`, each written
   `export interface <Name> {` with one field per line named exactly as the server's key, the
   nested sections of `ProjectSummary` typed by the four named interfaces; the type
   `JobProjectScope` of the three scopes; and the functions below.
   `decodeProjectsView`, `decodeProjectSummary` and `decodeJobProject` never throw. Each answers
   null for a value that is not a plain object or whose `version` is not 1; the list also for a
   `projects` that is not an array, the card for a `project_id` that is not a string, and the
   job's project for a `job_id` that is not a string, a `scope` outside the three, or scope
   `project` without a decodable entry. A list entry without a string `id` and `slug` is dropped.
   A `default_project` without a string `id` and `slug` is null. Counts that are not finite
   non-negative numbers read 0, strings that are not strings read "", booleans read true only for
   `true`, `repo_path` and `fix_it` keep null, `value_usd` keeps null for anything but a finite
   number, `basis` reads `"absent"` when empty, and a `last_result` without a string `job_id` is
   null. `projectsViewPath({token, baseUrl?})`, `projectSummaryPath({project, token, baseUrl?})`
   and `jobProjectPath({jobId, token, baseUrl?})` build `/api/projects?token=…`,
   `/api/projects/<project>/summary?token=…` and `/api/jobs/<jobId>/project?token=…` after the
   base, every part through `encodeURIComponent`. `projectFromSearch(search)` is the trimmed
   `project` parameter or "". `searchForProjectSwitch(search, slug, jobId)` deletes every name in
   `JOB_SCOPED_PARAMS`, sets `project`, sets `job` when `jobId` is not "", and answers `?` plus the
   parameters' text. `resolveActiveProject(view, urlProject, jobProject)` answers the entry whose
   slug or id equals a non-empty `urlProject`, else the entry whose id is the job's project's id,
   else the entry whose id is the default project's id, else null. `switcherVisible(view)` is true
   only for a view that is not null, not `single_project`, with more than one project.
   `switchTargetJob(summary)` is the last result's job id or "". `createSwitchGate(initialKey =
   "")` answers `{current(), begin(key)}`; `begin` makes `key` current and answers a ticket
   `{key, isCurrent()}` that is current until the NEXT `begin`, whatever key that one names.
   `switchProject(slug, gate, loadSummary, apply)` takes a ticket, awaits `loadSummary(slug)`
   (a throw reads as null), answers false without calling `apply` when the ticket is no longer
   current, and otherwise calls `apply({slug, jobId: switchTargetJob(summary), summary})` and
   answers true; `ProjectSwitch`, `SwitchTicket` and `SwitchGate` are its exported types.
S3 THE DOORS. In `apps/ui/src/api/remedyApi.ts`, one import line for the decoders and paths and
   one `import type` line for the three envelope types, directly after the `./chatTurn` imports;
   and at the end of the file, under a comment block naming F042 T002 and DECISION F042 D2,
   `export type ProjectFetcher = (path: string) => Promise<unknown>;` and
   `loadProjectsView(request, fetchPayload = fetchJson)`, `loadProjectSummary(...)` and
   `loadJobProject(...)`, each shaped exactly like `loadArtifactsView`: decode what the path
   answers, and answer null from a `catch`.

BUNDLE — the commits are C1a, C1b, C1c, C2, C3, C4, C5, C6 and C7, in this order.

C1a — copy this block and the plan
  `.agent/authored/f042-r2-block.md` := this block and `.agent/authored/f042-r2-plan.md` :=
  plan.md, by `shutil.copyfile`.
  Subject: `F042 R2 C1a: copy round 2 block and plan into .agent/authored/`
  Its insertions are this block's line count plus 29. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the records and vitest diffs
  `.agent/authored/f042-r2-records.diff` := records.diff and `.agent/authored/f042-r2-vitest.diff`
  := vitest.diff.
  Subject: `F042 R2 C1b: copy round 2 records and vitest diffs into .agent/authored/`
  Expected insertions: 323.

C1c — copy the tests diff
  `.agent/authored/f042-r2-tests.diff` := tests.diff.
  Subject: `F042 R2 C1c: copy round 2 tests diff into .agent/authored/`
  Expected insertions: 173.

C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F042 R2 C2: book F042 R1, record D2, advance the plan`
  Expected by `git show --numstat` (insertions and deletions): 40/0 .agent/decisions.md, 2/0 .agent/live_review.md, 6/6 .agent/plan.md.

C3 — THE CODE: S1 to S3 in one commit. If it would reach 500 insertions, split the server (S1)
  into a first commit and the client (S2, S3) into a second, and say so.
  Subject: `F042 R2 C3: name a job's project on the server and give the client its project seam`
  The reviewer's own version of S1 to S3 read 298/0 apps/ui/src/api/projectScope.ts, 49/0 apps/ui/src/api/remedyApi.ts, 18/0 packages/orchestration/project_cockpit.py, 7/0 packages/orchestration/ui_server.py.

C4 — THE PYTHON TESTS: `git apply` tests.diff.
  Subject: `F042 R2 C4: add the reviewer's tests for a job's project and the client's key parity`

C5 — THE VITEST FILE: `git apply` vitest.diff.
  Subject: `F042 R2 C5: add the reviewer's tests for the project seam and the switch gate`

C6 — THE TOOL: your mutation tool (G4) saved as `.agent/authored/f042-r2-mutations.py`.
  Subject: `F042 R2 C6: add the round 2 mutation tool`

C7 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F042 R2 C7: rewrite handoff for round 2`
  Then `git push`. Do NOT create a pull request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; C3's own clause
   says what to do if it would not.
3. The round's whole tracked path set is: the `.agent/authored/f042-r2-*` copies and tool, the
   paths records.diff, tests.diff and vitest.diff edit, `.agent/plan.md`,
   `packages/orchestration/project_cockpit.py`, `packages/orchestration/ui_server.py`,
   `apps/ui/src/api/projectScope.ts`, `apps/ui/src/api/remedyApi.ts`, and `.agent/handoff.md`.
   Report the list you measure with `git diff --name-only 2a678367b` at the branch tip after C7.
   Do NOT touch `apps/ui/src/RemedyApp.tsx`, `apps/ui/src/components/`, `apps/ui/package.json`,
   `apps/ui/package-lock.json`, `apps/cli/`, `.agent/context.md`, `.agent/prose_slips.md`,
   `.agent/candidates.md`, `.agent/operator_questions.md`, `docs/` or `README.md`.
4. Every test the payloads carry passes against your code unedited, at C4 and C5. A payload test
   is never edited to pass; if your code cannot meet one, STOP and report the test and the reason.
5. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. An EXISTING test
   that goes red is never edited to pass; report it and stop.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no branch switch, no branch
   deletion, no force-push, no `git stash`.
7. Leave every worktree already listed at your step 4, its branch, and every existing stash
   alone. The worktree G4 adds goes under `.remedy-wt/`, is removed as that gate's last action,
   and `git worktree list | wc -l` is reported afterwards.
8. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F042's belongs to its closure. Run no self-use job and no command that calls a provider.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G4 run before C7 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f042-r2-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f042-r2/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS AND THE TESTS — the sha256 of each file below, read with
 `git show <commit>:<path>` at the commit named, equals the reviewer's reading, printed from its
 simulation tree. Report each path beside the hash you read:
 | path | at | bytes | sha256 |
 |---|---|---|---|
 | .agent/decisions.md | C2 | 2480206 | 19d47d9efb919284e1c36c9e4c36c72c3cb54932b266ac9c91383c931ab5a632 |
 | .agent/live_review.md | C2 | 310277 | e10aa1cfdeb1a33816540e751334f7221cd2c35c979d43a4dec7e7885632ccd8 |
 | .agent/plan.md | C2 | 1020 | bc13696ec673b9f15f183d1374092dd6da48678a299a42ca06097e0f679a51a9 |
 | tests/orchestration/test_project_cockpit.py | C4 | 15423 | d07ac25353e3688b8905e972cf7cf2770945b6995111825aec9d35d2508a0218 |
 | tests/ui_server/test_projects_route.py | C4 | 5308 | a3e9eb8b13b76d22d8e208841360943b67440a6308e5161224da8bde6d5496cd |
 | tests/ui_contracts/test_project_scope_door.py | C4 | 3991 | a796b8556ef94181d2d1a64612dc53d3021c65f0a7970a56d6f41f9ddfb91e5c |
 | apps/ui/src/api/projectScope.test.ts | C5 | 12533 | 700e68d000ba54273bb91a1a9b43d9a44f8694061abacfe265e123fb1a28fda1 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT read with `git show <commit>:<path>` at
 C2 (the reviewer read `['R-1107']`); the ledger's last non-empty line at C2 begins
 `Gate: F042 R1 — the F042 round 1 entry`; and `git diff --name-only <C1c> <C2>`, which must name
 exactly the C2 paths of the table above.

G3 THE CODE AND THE TESTS — at C6: `python3 -m ruff check packages/orchestration/project_cockpit.py
 packages/orchestration/ui_server.py tests/orchestration/test_project_cockpit.py
 tests/ui_server/test_projects_route.py tests/ui_contracts/test_project_scope_door.py
 .agent/authored/f042-r2-mutations.py`, and
 `apps/ui/node_modules/.bin/eslint src/api/projectScope.ts src/api/projectScope.test.ts src/api/remedyApi.ts`
 run with `apps/ui` as its working directory, each with its real exit code. Report
 `git show --numstat <C3>` and the diffs of `packages/orchestration/ui_server.py` and
 `apps/ui/src/api/remedyApi.ts` at C3, whole. Then, in the primary checkout at C6, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_project_cockpit.py tests/ui_server/test_projects_route.py tests/ui_contracts/test_project_scope_door.py tests/ui_server/test_handler_table_walk.py tests/ui_server/test_command_channel.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/ui_contracts/test_diff_envelope_door.py tests/ui_contracts/test_task_run_rounds_door.py tests/ui_contracts/test_artifact_preview.py tests/ui_contracts/test_job_digest_card_contract.py tests/ui_contracts/test_ux_quality.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_live_review_rotation.py tests/regression/test_resource_safety.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -8; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 This selection's `test_typescript_compiles` runs `tsc --noEmit` over `apps/ui` and its
 `test_vitest_passes` runs the whole vitest suite, the new file included; name both nodes'
 outcomes in your report. The reviewer ran the selection serially inside its simulation tree,
 which carries C2 and this round's tests and the reviewer's own version of S1 to S3 but no
 `.agent/authored/f042-r2-*` copy and no `node_modules`, and read `879 passed, 4 skipped` at real exit code
 0; there, the `-rs` summary named four skips: `tests/orchestration/test_test_runner.py:414`, vitest absent from a fresh worktree, which your checkout has installed; `tests/ui_contracts/test_ux_quality.py:507` and `:543`, the D3 quarantine; and `tests/test_agent_tooling.py:43`, the D12 quarantine. Report every `SKIPPED` line yours prints. In the same tree, through the primary's binaries, `tsc` over the tree's
 `apps/ui/src` read exit 0 and the whole vitest suite read `1931 passed | 5 skipped` over 95 files at exit 0. Report the node
 counts of the three payload test files by `--collect-only -q` (the reviewer's read 25, 9 and 4)
 and the vitest count of `src/api/projectScope.test.ts` (the reviewer's read 24). Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0.

G4 THE RED PROOFS — your tool `.agent/authored/f042-r2-mutations.py` takes a worktree path, and
 for each mutation below edits the named production file INSIDE that worktree (asserting its
 FROM text occurs exactly once there), runs the named test file, restores the bytes, and prints
 one line per mutation: its label, the exit code and the failed count. A pytest file runs as
 `python3 -B -m pytest -q -p no:cacheprovider <file>` with the worktree as the working directory
 and the worktree's root first on `PYTHONPATH` (set through `subprocess.run(..., env=...)`). The
 vitest file runs as `<primary>/apps/ui/node_modules/.bin/vitest run --root <worktree>/apps/ui
 --config <primary>/apps/ui/vitest.config.ts src/api/projectScope.test.ts` with
 `<worktree>/apps/ui` as the working directory, the primary being
 `/home/decodeux/Repos/remedy`, scoped to that one file (checklist item 33). The tool runs an
 unmutated control of each test file the mutations name first and last, reports
 `restored byte-identical: True` after each restore, and ends with a final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each is a real behaviour change:
  v1 a switch ticket stays current while the gate's current key equals its own key, rather
     than until the next `begin` (`apps/ui/src/api/projectScope.ts`, projectScope.test.ts);
  v2 `switchProject` calls `apply` without asking whether its ticket is current (same);
  v3 a switch keeps the `focus` parameter (same);
  v4 `resolveActiveProject` never takes the address's project (same);
  v5 the card decoder reads a null `value_usd` as 0 (same);
  v6 `switcherVisible` answers true for every view that is not null (same);
  v7 `decodeJobProject` accepts a scope outside the three (same);
  v8 `loadProjectsView` lets a failed read throw instead of answering null
     (`apps/ui/src/api/remedyApi.ts`, projectScope.test.ts);
  p1 `job_project_view` labels a job with no project `"project"`
     (`packages/orchestration/project_cockpit.py`, test_project_cockpit.py);
  p2 the `project` entry is removed from `do_GET`'s endpoint dict
     (`packages/orchestration/ui_server.py`, test_projects_route.py).
 Run it: `git worktree add --detach .remedy-wt/f042-r2-mut <C6>`, copy the primary checkout's
 `apps/ui/dist` into it with `shutil.copytree(..., symlinks=True)`, then
 `python3 -B .agent/authored/f042-r2-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f042-r2-mut`
 and report its whole output. The reviewer's own version of this probe, run against its version
 of S1 to S3 in its dry tree, turned every one red with every control at exit 0. EVERY mutation
 must exit non-zero; a mutation that stays green is reported as green, never papered over, and
 you then STOP and report it, because the tests are the reviewer's. Then
 `git worktree remove --force .remedy-wt/f042-r2-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.

G5 TREE AND PUSH — after C7: `git status --porcelain`, which must be empty;
 `git log --oneline -n 10`, which must show C7, C6, C5, C4, C3, C2, C1c, C1b, C1a and
 `2a678367b` in that order; `git worktree list | wc -l`, which must equal your step 4 reading;
 the push's real outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`,
 which must be EMPTY. These readings go in your reply, since C7 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3's own files, C4, C5 and
C6 — report what you measure), every gate's real output and exit code, the authored-text proofs,
the item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F042, round 2, and says in one sentence how much context you
had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 2, then round 3 (mount the seam: the provider in `RemedyApp.tsx`, the re-keyed shell and
the header switcher). State the open-findings count, 1, and the operator-questions count, 1.

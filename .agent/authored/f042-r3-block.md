STEP F042 R3 — MOUNT THE SEAM: one address, one project provider around every face, the shell keyed by project and job, Back and Forward, and the switcher in the brand rail's kicker

GOAL
Book round 2's PASS, record DECISION F042 D3 with its assumption-log line, and mount T002's
seam in the page against the reviewer's tests and a render harness that proves it in a real
browser: `apps/ui/src/api/cockpitAddress.ts`, `ProjectProvider.tsx`, `ProjectSwitcher.tsx` with
its sheet, and the changes to `RemedyApp.tsx` and `LeftBrandRail.tsx`.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE TESTS ARE THE REVIEWER'S AND THE CODE IS YOURS:
the test files and the render harness travel as payloads and are the acceptance, and you write
the production code against them and against S1 to S5 below. You never edit a payload; if one
looks wrong to you, STOP and report it. Read DECISION F042 D3 in the records diff before you
write code, and read whole, before you edit or call them: `apps/ui/src/RemedyApp.tsx`,
`apps/ui/src/components/rail/LeftBrandRail.tsx` with its sheet,
`apps/ui/src/components/shell/ReducedMotionProvider.tsx` (the context style S2 follows),
`apps/ui/src/api/projectScope.ts`, and the tests that read `RemedyApp.tsx`:
`tests/ui_contracts/test_decision_answer_wiring.py`, `tests/ui_server/test_live_state.py`,
`tests/ui_contracts/test_ux_quality.py` and `tests/ui_contracts/test_raw_colour_ratchet.py`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f042-r3-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f042-r3/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f042-r1-*`, `.remedy-wt/f042-r2-*`, `.remedy-wt/f042-r3-dry/`,
  `.remedy-wt/f042-r3-sim/`, `.remedy-wt/f042-r3-scratch/`
                                  The reviewer's trees and scripts; do not touch them.
  `.remedy-wt/f042-r3-worker/`    YOURS for logs and scripts; create it if absent. All are
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
yourself: call `apps/ui/node_modules/.bin/tsc`, `.bin/vitest`, `.bin/eslint` and `.bin/vite` by
path. Never stop a process with `pkill -f`; the harness stops what it started by pid.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f042-multi-project-cockpit`, and `git log --oneline -1` must read `fc744e0e0`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f042-r3/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f042-r3-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 68 | 15078 | ad06cd990f407fc6f33c7315509cd782d4a13bee39bb1be05c6f8d0a1b078744 |
| tests.diff | 134 | 5862 | 53bf5b398814a6819f26277f1d96aefff6367158d63743c385bb3df39ef6d821 |
| plan.md | 28 | 952 | 68325b9727ea9db1c5d7d3658aea96a4e61c87b3f6afdc27ee333602b40256fa |
| render_index.html | 11 | 243 | 224210b87c232ba002b0371bc54a6bb871dabaf13f23784ecd06573303d83363 |
| render_main.tsx | 61 | 3029 | 32178e171a74d09949494198421bc5a585d2a0dac8b887e8a7969100597ee7e9 |
| render_vite.config.mjs | 28 | 744 | 6c9d24558a507a827d445c793cd6203f7f0f24ac2659dcfe3cff96c20b7d1c6a |
| render_drive.mjs | 176 | 8416 | 318bb9178f81094465d84384bb752011a196866e4f401f9d17bc71e3aec62681 |
| render_measure.py | 187 | 6499 | 263344b3e2e569a16118bb2330945ce0462b2beb8a4b18977080fc5f4edc7232 |

`plan.md` is a REWRITE of `.agent/plan.md`. The two `.diff` files go on with `git apply`; the
reviewer generated them with `git diff HEAD` from a tree at `fc744e0e0`. `records.diff` appends
round 2's gate entry to `.agent/live_review.md`, DECISION F042 D3 to `.agent/decisions.md`, and
one line to `docs/ui/design_reference/assumption_log.md`. `tests.diff` adds the NEW FILE at
`apps/ui/src/api/cockpitAddress.test.ts` and the NEW FILE at
`tests/ui_contracts/test_project_switcher_wiring.py`. The five `render_*` files are the render
harness; they are copied, never applied, and run from their copies.

THE SPECIFICATION — the tests are the acceptance; these clauses fix what they leave open.
S1 `apps/ui/src/api/cockpitAddress.ts`, NEW, pure, a header comment naming T5_F042 T002 and
   DECISION F042 D3. Exports: the interface `CockpitAddress` (`jobId`, `project`, `token`); the
   type `CockpitFace` = `"missing" | "empty_project" | "job"`; `MISSING_ADDRESS_LINE` =
   `"Missing job or token in the URL."`; `EMPTY_PROJECT_LINE` = `"This project has no jobs
   yet."`; `addressFromSearch(search)`, reading `job` then `job_id`, the trimmed `project`, and
   `token`, each "" when absent; `cockpitFaceOf(address)`: `missing` without a token, else `job`
   with a job, else `empty_project` with a project, else `missing`; and `shellKeyOf(address)` =
   `JSON.stringify([address.project, address.jobId])`.
S2 `apps/ui/src/components/shell/ProjectProvider.tsx`, NEW, a header comment naming DECISION
   F042 D3. Exports the interface `ProjectContextValue` (`view`, `active`, `switchTo(slug)`),
   `ProjectProvider({token, jobId, project, onSwitched, children})` and `useProjectContext()`.
   The provider loads `loadProjectsView({token})` in an effect keyed by the token, and
   `loadJobProject({jobId, token})` in an effect keyed by the job and the token, each skipped when
   its key is "" and each dropping a late answer through a `cancelled` flag; it keeps ONE gate,
   `useRef(createSwitchGate(project))`, the file's only `createSwitchGate(` call; an effect keyed
   by `project` calls `gate.current.begin(project)` when `gate.current.current()` differs; the
   job's project counts only while it belongs to the current `jobId`; `active` is
   `resolveActiveProject(view, project, <the job's project>)` or null without a view; `switchTo`
   is `void switchProject(slug, gate.current, (next) => loadProjectSummary({ project: next,
   token }), onSwitched)`, with that `switchProject(slug, gate.current,` text; the context value
   is memoised.
S3 `apps/ui/src/components/shell/ProjectSwitcher.tsx` and `ProjectSwitcher.module.css`, NEW, no
   `@mui`, no colour literal, only `--remedy-*` tokens. Exports `PROJECT_SWITCHER_LABEL =
   "Project"`, `MISSING_FOLDER_MARK = " (folder missing)"`, `NO_ACTIVE_PROJECT_OPTION = "Choose a
   project"` and `ProjectSwitcher({fallback})`. When the view is null or
   `switcherVisible(view)` is false, it renders the active project's name (or slug when the name
   is "") in a `data-ui="project-kicker"` element, or `fallback` with no active project. Otherwise
   a `<label data-ui="project-switcher">` holds a span reading the label and a native `<select>`
   with `aria-label={PROJECT_SWITCHER_LABEL}`, valued by the active slug or "", holding a disabled
   first option `NO_ACTIVE_PROJECT_OPTION` with value "" only while no project is active, then
   one option per project valued by its slug and reading the slug, plus `MISSING_FOLDER_MARK`
   when `repo_reachable` is false; a change to a non-empty slug other than the active one calls
   `switchTo`. The kicker text takes the rail's kicker type (10px, weight 800, letter-spacing
   .12em, uppercase, `--remedy-muted`) and the select a visible `:focus-visible` outline.
S4 `apps/ui/src/components/rail/LeftBrandRail.tsx`: one import line for `ProjectSwitcher` after
   the `./SideIconDock` import, and the kicker line becomes exactly
   `<ProjectSwitcher fallback={<div className={styles.concept}>CONCEPT 01 OF 10</div>} />`.
   Nothing else in the file changes.
S5 `apps/ui/src/RemedyApp.tsx`. `readUrlState()` answers `addressFromSearch(window.location.search)`
   and seeds an `address` state. `openAddress(search)` clears the dashboard, the error and the
   selection and sets the address from `search`. A `popstate` listener, added as
   `window.addEventListener("popstate", onPopState)` and removed as
   `window.removeEventListener("popstate", onPopState)`, calls it with
   `window.location.search`. `onSwitched(target)` computes
   `searchForProjectSwitch(window.location.search, target.slug, target.jobId)`, calls
   `window.history.pushState(window.history.state, "", <pathname + that search + hash>)` — the
   file's only `pushState(`, and no `replaceState` — then `openAddress` with it. The dashboard
   loads and polls with `setInterval` exactly as before, but only on the `job` face, keyed by the
   face, the job and the token. The faces: `missing` shows `MISSING_ADDRESS_LINE` in the existing
   centred `data-ui="remedy-app"` div, which keeps the file's one colour literal `#14254b` and the
   only one; `empty_project` shows, centred, `<ProjectSwitcher fallback={null} />` above a
   `<p data-ui="empty-project">` reading `EMPTY_PROJECT_LINE`; an error shows its text in that
   centred div coloured by a `--remedy-*` token; no dashboard shows the progress spinner; and a
   dashboard shows `<RemedyShell key={shellKeyOf(address)} dashboard={dashboard}
   serverToken={token} selectedNodeId={selectedNodeId} onSelectNode={setSelectedNodeId} />`. The
   chosen face is a `body` variable rendered as `{body}` inside ONE `<ProjectProvider
   token={token} jobId={jobId} project={address.project} onSwitched={onSwitched}>` inside the
   `ReducedMotionProvider`. Keep `useState<string | null>(null)` and the comment on the token.

BUNDLE — the commits are C1a, C1b, C1c, C2, C3, C4, C5 and C6, in this order.

C1a — copy this block and the plan
  `.agent/authored/f042-r3-block.md` := this block and `.agent/authored/f042-r3-plan.md` :=
  plan.md, by `shutil.copyfile`.
  Subject: `F042 R3 C1a: copy round 3 block and plan into .agent/authored/`
  Its insertions are this block's line count plus 28. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the records and tests diffs
  `.agent/authored/f042-r3-records.diff` := records.diff and `.agent/authored/f042-r3-tests.diff`
  := tests.diff.
  Subject: `F042 R3 C1b: copy round 3 records and tests diffs into .agent/authored/`
  Expected insertions: 202.

C1c — copy the render harness
  Each `render_<x>` payload := `.agent/authored/f042-r3-render_<x>`, all five.
  Subject: `F042 R3 C1c: copy the round 3 render harness into .agent/authored/`
  Expected insertions: 463.

C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F042 R3 C2: book F042 R2, record D3 and its assumption line, advance the plan`
  Expected by `git show --numstat` (insertions and deletions): 41/0 .agent/decisions.md, 2/0 .agent/live_review.md, 8/9 .agent/plan.md, 1/0 docs/ui/design_reference/assumption_log.md.

C3 — THE CODE: S1 to S5 in one commit. If it would reach 500 insertions, split S1 to S3 into a
  first commit and S4 and S5 into a second, and say so.
  Subject: `F042 R3 C3: mount one project context, key the shell by project and job, switch in the rail`
  The reviewer's own version of S1 to S5 read 64/13 apps/ui/src/RemedyApp.tsx, 45/0 apps/ui/src/api/cockpitAddress.ts, 2/1 apps/ui/src/components/rail/LeftBrandRail.tsx, 66/0 apps/ui/src/components/shell/ProjectProvider.tsx, 30/0 apps/ui/src/components/shell/ProjectSwitcher.module.css, 44/0 apps/ui/src/components/shell/ProjectSwitcher.tsx.

C4 — THE TESTS: `git apply` tests.diff.
  Subject: `F042 R3 C4: add the reviewer's tests for the cockpit address and the switcher wiring`

C5 — THE TOOL: your mutation tool (G5) saved as `.agent/authored/f042-r3-mutations.py`.
  Subject: `F042 R3 C5: add the round 3 mutation tool`

C6 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F042 R3 C6: rewrite handoff for round 3`
  Then `git push`. Do NOT create a pull request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; C3's own clause
   says what to do if it would not.
3. The round's whole tracked path set is: the `.agent/authored/f042-r3-*` copies and tool, the
   paths records.diff and tests.diff edit, `.agent/plan.md`, the files S1 to S5 name, and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only fc744e0e0` at the
   branch tip after C6. Do NOT touch `apps/ui/src/components/shell/RemedyShell.tsx`,
   `apps/ui/src/api/projectScope.ts`, `apps/ui/src/api/remedyApi.ts`, `packages/`, `apps/cli/`,
   `apps/ui/package.json`, `apps/ui/package-lock.json`, `.agent/context.md`,
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md`,
   `docs/roadmap/` or `README.md`.
4. Every test the payloads carry passes against your code unedited, at C4, and the render
   harness reads every check passing at C4. A payload is never edited to pass; if your code
   cannot meet one, STOP and report it and the reason.
5. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. An EXISTING test
   that goes red is never edited to pass; report it and stop.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no branch switch, no branch
   deletion, no force-push, no `git stash`.
7. Leave every worktree already listed at your step 4, its branch, and every existing stash
   alone. The worktree G5 adds goes under `.remedy-wt/`, is removed as that gate's last action,
   and `git worktree list | wc -l` is reported afterwards.
8. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F042's belongs to its closure. Run no self-use job and no command that calls a provider.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C6 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f042-r3-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f042-r3/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS AND THE TESTS — the sha256 of each file below, read with
 `git show <commit>:<path>` at the commit named, equals the reviewer's reading, printed from its
 simulation tree. Report each path beside the hash you read:
 | path | at | bytes | sha256 |
 |---|---|---|---|
 | .agent/decisions.md | C2 | 2483692 | be0127feff848dbc95fde2bd2a44939f0d82a7bf869b04f117aedf60737a2623 |
 | .agent/live_review.md | C2 | 312699 | 72c16195ab1033610fef80782503bdf20e0d444ddd425d59689a9159976f900e |
 | .agent/plan.md | C2 | 952 | 68325b9727ea9db1c5d7d3658aea96a4e61c87b3f6afdc27ee333602b40256fa |
 | docs/ui/design_reference/assumption_log.md | C2 | 29374 | 25fa266deedf7468356516ffc7cacccd9b22c0ab94b558fe6fa5bf1e40adec4e |
 | apps/ui/src/api/cockpitAddress.test.ts | C4 | 2708 | e6ecb94effd833120eeac570b22f506fc5e16fddbe4715137547c6b280b01329 |
 | tests/ui_contracts/test_project_switcher_wiring.py | C4 | 2562 | 84937461a784e2817d3ea0d6edd79280b5fe1773bf63dba5cf91fee91ba28eb3 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT read with `git show <commit>:<path>` at
 C2 (the reviewer read `['R-1107']`), and `git diff --name-only <C1c> <C2>`, which must name
 exactly the C2 paths of the table above.

G3 THE CODE AND THE TESTS — at C5: `python3 -m ruff check
 tests/ui_contracts/test_project_switcher_wiring.py .agent/authored/f042-r3-mutations.py
 .agent/authored/f042-r3-render_measure.py`, and `apps/ui/node_modules/.bin/eslint
 src/RemedyApp.tsx src/api/cockpitAddress.ts src/api/cockpitAddress.test.ts
 src/components/shell/ProjectProvider.tsx src/components/shell/ProjectSwitcher.tsx
 src/components/rail/LeftBrandRail.tsx` run with `apps/ui` as its working directory, each with
 its real exit code. Report `git show --numstat <C3>` and the diffs of `RemedyApp.tsx` and
 `LeftBrandRail.tsx` at C3, whole. Then, in the primary checkout at C5, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_live_state.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_project_brain.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_live_review_rotation.py tests/regression/test_resource_safety.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -10; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 This selection runs `tsc --noEmit` (`test_typescript_compiles`), the whole vitest suite
 (`test_vitest_passes`) and eslint over `apps/ui/src` (`tests/ui_contracts/test_ui_lint.py`);
 name each of those nodes' outcomes. The reviewer ran the selection serially inside its
 simulation tree, which carries C2, this round's tests and the reviewer's own version of S1 to
 S5 but no `.agent/authored/f042-r3-*` copy and no `node_modules`, and read `1754 passed, 8 skipped` at real
 exit code 0, its skips the vitest node, `tests/ui_contracts/test_ui_lint.py:30` twice and the D12 quarantine, all four for a toolchain your checkout has installed or a standing quarantine, and the four D3 quarantine nodes of `test_graph_architecture.py` and `test_ux_quality.py`; through the primary's binaries in the same tree, `tsc` read
 exit 0 and the whole vitest suite `1940 passed | 5 skipped` over 96 files at exit 0. Report every `SKIPPED` line yours prints,
 the node count of the wiring test by `--collect-only -q` (the reviewer's read 5) and the vitest
 count of `src/api/cockpitAddress.test.ts` (the reviewer's read 9). Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0.

G4 THE RENDER — at C5, in the primary checkout:
 `python3 -B .agent/authored/f042-r3-render_measure.py /home/decodeux/Repos/remedy`, which builds
 the harness page over the checkout's own `apps/ui/src`, serves it on 127.0.0.1 port 9000, drives
 `/usr/bin/google-chrome --headless=new` over CDP port 9370, stops both by pid and removes its work
 dir. Report its whole output from the first `PASS` or `FAIL` line on, and its exit code; it must
 print `RENDER: 8 of 8 checks pass` and exit 0. Read the screenshot it writes to
 `/home/decodeux/Repos/remedy/.remedy-wt/f042-r3-render-switcher.png` and say in one sentence
 what it shows. The reviewer's own run over its version of S1 to S5 read 8 of 8.

G5 THE RED PROOFS — your tool `.agent/authored/f042-r3-mutations.py` takes a worktree path, and
 for each mutation below edits the named production file INSIDE that worktree (asserting its
 FROM text occurs exactly once there), runs the named check, restores the bytes, and prints one
 line per mutation: its label, the exit code, and the failed count or the harness's
 `RENDER: <n> of 8` reading. Vitest runs as `<primary>/apps/ui/node_modules/.bin/vitest run
 --root <worktree>/apps/ui --config <primary>/apps/ui/vitest.config.ts
 src/api/cockpitAddress.test.ts` with `<worktree>/apps/ui` as the working directory (checklist
 item 33); pytest as `python3 -B -m pytest -q -p no:cacheprovider
 tests/ui_contracts/test_project_switcher_wiring.py` with the worktree as the working directory
 and first on `PYTHONPATH`; the harness as `python3 -B <worktree>/.agent/authored/f042-r3-render_measure.py
 <worktree>`. The primary is `/home/decodeux/Repos/remedy`. The tool runs an unmutated control of
 each of the three checks first and last, reports `restored byte-identical: True` after each
 restore, and ends with `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each is a real
 behaviour change:
  a1 `addressFromSearch` reads `job_id` before `job` (`cockpitAddress.ts`, vitest);
  a2 `cockpitFaceOf` opens a job's face without a token (same);
  a3 `shellKeyOf` joins the project and the job with a `|` (same);
  w1 the `key` is removed from the `RemedyShell` element (`RemedyApp.tsx`, the wiring test);
  h1 `switchTo` hands `switchProject` a fresh `createSwitchGate(slug)` instead of the one gate
     (`ProjectProvider.tsx`, the harness);
  h2 the `popstate` listener is never added (`RemedyApp.tsx`, the harness);
  h3 a switch calls `replaceState` instead of `pushState` (`RemedyApp.tsx`, the harness) — the
     reviewer's run ended with no RENDER line, because Back then leaves the harness page and the
     driver fails, which is an exit 1 all the same;
  h4 the switcher shows for every view that is not null (`ProjectSwitcher.tsx`, the harness).
 Run it: `git worktree add --detach .remedy-wt/f042-r3-mut <C5>`, then in Python
 `os.symlink("/home/decodeux/Repos/remedy/apps/ui/node_modules",
 "/home/decodeux/Repos/remedy/.remedy-wt/f042-r3-mut/apps/ui/node_modules",
 target_is_directory=True)`, so the harness build resolves the app's own imports, then
 `python3 -B .agent/authored/f042-r3-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f042-r3-mut`
 and report its whole output. The reviewer's own version of this probe turned every one red
 with every control passing. EVERY mutation must exit non-zero; one that stays green is reported
 as green, never papered over, and you then STOP and report it. Then remove the symlink with
 `os.unlink`, `git worktree remove --force .remedy-wt/f042-r3-mut`, `git worktree prune`, and
 report `git worktree list | wc -l`.

G6 TREE AND PUSH — after C6: `git status --porcelain`, which must be empty;
 `git log --oneline -n 9`, which must show C6, C5, C4, C3, C2, C1c, C1b, C1a and `fc744e0e0` in
 that order; `git worktree list | wc -l`, which must equal your step 4 reading; the push's real
 outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which
 must be EMPTY. These readings go in your reply, since C6 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3's own files, C4 and C5 —
report what you measure), every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and the
next expected action. Report what you ran, not what you expected to find. Your Session section
reads SESSION 1 of feature F042, round 3, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 3, then T003 (the home grid, the cards, the empty-state invite, deep links across projects
and the end-to-end run). State the open-findings count, 1, and the operator-questions count, 1.

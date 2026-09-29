STEP F042 R4 — T003's HOME GRID: the home face, the card rules, the grid with its pages, the single-project skip, "All projects", and the repairs of R-1108 and R-1109

GOAL
Book round 3's PASS with the registrations of R-1108 and R-1109, record DECISION F042 D4, and
land T003's home grid against the reviewer's tests and render harness: the `home` face and its
address in `cockpitAddress.ts`, the pure `homeGrid.ts`, `components/home/HomeGrid.tsx` with its
sheet, the provider's three new members, "All projects" beside the switcher, and the one address
writer in `RemedyApp.tsx`, with R-1108's grouping of the empty project's page.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE TESTS ARE THE REVIEWER'S AND THE CODE IS YOURS:
the test files and the render harness travel as payloads and are the acceptance, and you write
the production code against them and against S1 to S6 below. You never edit a payload; if one
looks wrong to you, STOP and report it. Read DECISION F042 D4 and R-1108 and R-1109 in the
records diff before you write code, and read whole, before you edit them, every file S1 to S6
names and `apps/ui/src/api/projectScope.ts`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f042-r4-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f042-r4/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f042-r1-*` to `.remedy-wt/f042-r3-*`, `.remedy-wt/f042-r4-dry/`,
  `.remedy-wt/f042-r4-sim/`, `.remedy-wt/f042-r4-scratch/`
                                  The reviewer's trees and scripts; do not touch them.
  `.remedy-wt/f042-r4-worker/`    YOURS for logs and scripts; create it if absent. All are
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
   `feature/f042-multi-project-cockpit`, and `git log --oneline -1` must read `9d45d7491`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f042-r4/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f042-r4-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 63 | 13611 | dfc11d226046c160a7704fe2e24f6abc732184323dcaf126190f71fe1619d05a |
| tests.diff | 213 | 10363 | 421f45430cf920e627d063321df52c284f68af3447ce0bd7e8ff2fe571bd4af3 |
| plan.md | 29 | 1018 | fc5092260eae70ca569d9ab9ac3794f708cc5930bdbfadb8fb46e29a394472e6 |
| render_index.html | 11 | 243 | 15a938debcf50845e623d6aed54b5a4013a69047679f3e8c22cb46c51a6dd14f |
| render_main.tsx | 66 | 3472 | 7d6d5a67ce64c2843ed45ac7d3002e84a002f89dfa4466fd2ef67f274691421f |
| render_vite.config.mjs | 28 | 744 | 6c9d24558a507a827d445c793cd6203f7f0f24ac2659dcfe3cff96c20b7d1c6a |
| render_drive.mjs | 277 | 15333 | 55386b1a6e27bc001415ae007a6dd3c74ddddf2cdd059e74c361a8f6972b9fa0 |
| render_measure.py | 187 | 6528 | facbbbd2113c6031c5922c0e51525f64ae9fdcf13e977ac733839f6257f19d30 |

`plan.md` is a REWRITE of `.agent/plan.md`. The two `.diff` files go on with `git apply`; the
reviewer generated them with `git diff HEAD` from a tree at `9d45d7491`. `records.diff` appends
round 3's gate entry with R-1108 and R-1109 to `.agent/live_review.md` and DECISION F042 D4 to
`.agent/decisions.md`. `tests.diff` edits `apps/ui/src/api/cockpitAddress.test.ts` and
`tests/ui_contracts/test_project_switcher_wiring.py` and adds the NEW FILE at
`apps/ui/src/api/homeGrid.test.ts`. The five `render_*` files are the round's render harness;
they are copied, never applied, and run from their copies.

THE SPECIFICATION — the tests are the acceptance; these clauses fix what they leave open.
S1 `apps/ui/src/api/cockpitAddress.ts`: `CockpitFace` gains `"home"`, which `cockpitFaceOf`
   answers for a token with neither a job nor a project; and `homeSearch(search)` deletes
   `project` and every name in `JOB_SCOPED_PARAMS` (imported from `./projectScope`) and answers
   `?` plus the rest, or "" when nothing is left. Its header comments name the fourth face.
S2 `apps/ui/src/api/homeGrid.ts`, NEW, pure, a header naming T5_F042 T003 and DECISION F042
   D4. Exports `HOME_PAGE_SIZE = 12`; `NO_PROJECTS_LINE` = `"No projects yet. Run remedy init
   in a project's folder to add it."`; `SUMMARY_UNAVAILABLE_LINE` = `"This project's summary
   could not be read."`; `NO_JOBS_LINE` = `"No jobs yet."`; `DEGRADED_LINE` = `"Some job
   records could not be read."`; `NO_FOLDER_HINT` = `"No folder attached"`;
   `homePage(items, page)` answering `{items, page, pages}`, pages at least 1, page clamped into
   range; the type `ResultTone`; `resultToneOf(state)`, lowercased: completed or done `done`,
   running `current`, blocked, failed or cancelled `blocked`, "" `none`, anything else `open`;
   `costTodayLine(cost)`: `Cost today: not measured` for basis `absent` or a null value, else
   `$` and the value to two places, after `at least ` for `lower_bound`; the interface
   `ProjectCard` with the fields the test names; and `projectCardOf(entry, summary)` as the test
   pins it, the name falling back to the slug, the fix-it only for an unreachable folder, and an
   unreadable summary drawn with empty chips and lines and `SUMMARY_UNAVAILABLE_LINE`.
S3 `apps/ui/src/components/home/HomeGrid.tsx` and `HomeGrid.module.css`, NEW, only
   `--remedy-*` tokens, no colour literal, no `@mui`. Exports `HOME_TITLE = "Projects"`,
   `HOME_LOADING_LINE = "Reading your projects…"` and `HomeGrid()`, which reads `view`,
   `switchTo`, `enterProject` and `readSummary` from `useProjectContext()`. While the view is null
   or a single project is being entered it shows the loading line in `data-ui="home-loading"`;
   with no project, `NO_PROJECTS_LINE` in `data-ui="home-empty"`. With exactly one project
   (`single_project` and one entry) it calls `enterProject(slug)` from an effect, ONCE per slug,
   guarded by a ref. Otherwise a `<section data-ui="home-grid">` headed by an `h1` reading
   `HOME_TITLE`, one `<button data-ui="project-card" data-slug=… data-reachable="true|false">`
   per project of `homePage(view.projects, page)`, whose click calls `switchTo(slug)`; each card
   shows the name, the folder hint, the fix-it in `data-ui="card-fix-it"`, and once its summary
   has been read, the result line in `data-ui="card-result"` with `data-tone`, the active chip in
   `data-ui="card-active"` and the decisions chip in `data-ui="card-decisions"` with
   `data-urgent="true|false"`, the cost line in `data-ui="card-cost"`, and `DEGRADED_LINE` when
   degraded. The page's summaries are read together with `readSummary`, in an effect keyed by the
   page's slugs and dropped through a `cancelled` flag. With more than one page, a
   `<nav data-ui="home-pager">` holds Previous and Next buttons, disabled at the ends, around
   `data-ui="home-page"` reading `Page <n> of <pages>`. Cards sit in a grid of columns at least
   240 pixels wide; the result line's left border takes the `--remedy-state-*` token of its tone.
S4 `apps/ui/src/components/shell/ProjectProvider.tsx`: the context gains `enterProject(slug)`,
   `goHome()` and `readSummary(slug)`; the props gain `onHome` and `onSwitched` becomes
   `(result, replace) => void`. `readSummary` is `loadProjectSummary({ project: slug, token })`;
   `switchTo` calls `switchProject(slug, gate.current, readSummary, (result) =>
   onSwitched(result, false))` and `enterProject` the same with `(result) => onSwitched(result,
   true)`; `goHome` calls `gate.current.begin("")` and then `onHome()`. Every member is memoised
   and the file keeps its one `createSwitchGate(`.
S5 `apps/ui/src/components/shell/ProjectSwitcher.tsx` and its sheet: `ALL_PROJECTS_LABEL =
   "All projects"`; the switcher's label and a `<button type="button" data-ui="project-home">`
   reading it, whose click calls `goHome`, sit in ONE `<div data-ui="project-switcher-group">`,
   a grid with a small gap whose items start at its left edge; the button takes a link's look
   and a `:focus-visible` outline.
S6 `apps/ui/src/RemedyApp.tsx`: `const writeAddress = useCallback(` taking `(search, replace)`
   holds the file's only `window.history.pushState(` and its only
   `window.history.replaceState(`, replacing when `replace` is true, and then calls
   `openAddress(search)`. `const onSwitched = useCallback(` writes
   `searchForProjectSwitch(window.location.search, target.slug, target.jobId)` with its
   `replace`; `const onHome = useCallback(` calls `writeAddress(homeSearch(window.location.search),
   false)`; the provider receives `onSwitched={onSwitched} onHome={onHome}`. The `home` face is a
   `data-ui="remedy-home"` div, full height and scrolling, holding the file's one `<HomeGrid />`.
   R-1108: the empty project's div adds `alignContent: "center"` and `gap: 16` beside its
   `placeItems: "center"`. Everything else S5 of round 3 fixed stays.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C2, C3, C4, C5 and C6, in this order.

C1a — `.agent/authored/f042-r4-block.md` := this block and `.agent/authored/f042-r4-plan.md` :=
  plan.md, by `shutil.copyfile`. Subject: `F042 R4 C1a: copy round 4 block and plan into .agent/authored/`
  Its insertions are this block's line count plus 29; STOP rather than commit at 500.
C1b — `.agent/authored/f042-r4-records.diff` and `.agent/authored/f042-r4-tests.diff` := the two
  diffs. Subject: `F042 R4 C1b: copy round 4 records and tests diffs into .agent/authored/`
  Expected insertions: 276.
C1c — `.agent/authored/f042-r4-render_drive.mjs` := render_drive.mjs.
  Subject: `F042 R4 C1c: copy the round 4 render driver into .agent/authored/`
  Expected insertions: 277.
C1d — the other four `render_<x>` := `.agent/authored/f042-r4-render_<x>`.
  Subject: `F042 R4 C1d: copy the rest of the round 4 render harness into .agent/authored/`
  Expected insertions: 292.
C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F042 R4 C2: book F042 R3, register R-1108 and R-1109, record D4, advance the plan`
  Expected by `git show --numstat` (insertions and deletions): 41/0 .agent/decisions.md, 6/0 .agent/live_review.md, 9/8 .agent/plan.md.
C3 — THE CODE: S1 to S6 in one commit. If it would reach 500 insertions, split S1 to S3 into a
  first commit and S4 to S6 into a second, and say so.
  Subject: `F042 R4 C3: open a home grid of project cards, skip it for one project, group the empty page`
  The reviewer's own version of S1 to S6 read 24/8 apps/ui/src/RemedyApp.tsx, 15/4 apps/ui/src/api/cockpitAddress.ts, 97/0 apps/ui/src/api/homeGrid.ts, 118/0 apps/ui/src/components/home/HomeGrid.module.css, 103/0 apps/ui/src/components/home/HomeGrid.tsx, 27/6 apps/ui/src/components/shell/ProjectProvider.tsx, 23/0 apps/ui/src/components/shell/ProjectSwitcher.module.css, 8/1 apps/ui/src/components/shell/ProjectSwitcher.tsx.
C4 — THE TESTS: `git apply` tests.diff.
  Subject: `F042 R4 C4: add the reviewer's tests for the home face, the card rules and the wiring`
C5 — THE TOOL: your mutation tool (G5) saved as `.agent/authored/f042-r4-mutations.py`.
  Subject: `F042 R4 C5: add the round 4 mutation tool`
C6 — THE HANDBACK: `.agent/handoff.md`, rewritten, its own commit, per
  `docs/agents/handback_template.md`. Subject: `F042 R4 C6: rewrite handoff for round 4`
  Then `git push`. Do NOT create a pull request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; C3's own clause
   says what to do if it would not.
3. The round's whole tracked path set is: the `.agent/authored/f042-r4-*` copies and tool, the
   paths records.diff and tests.diff edit, `.agent/plan.md`, the files S1 to S6 name, and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only 9d45d7491` at the
   branch tip after C6. Do NOT touch `apps/ui/src/components/shell/RemedyShell.tsx`,
   `apps/ui/src/components/rail/`, `apps/ui/src/api/projectScope.ts`,
   `apps/ui/src/api/remedyApi.ts`, `packages/`, `apps/cli/`, `apps/ui/package.json`,
   `apps/ui/package-lock.json`, `docs/`, `.agent/context.md`, `.agent/prose_slips.md`,
   `.agent/candidates.md`, `.agent/operator_questions.md` or `README.md`. Write no `Landed:` or
   `Done:` line: the reviewer books R-1108 and R-1109 at its gate.
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
 against the PAYLOADS table. Then compare each `.agent/authored/f042-r4-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f042-r4/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS AND THE TESTS — the sha256 of each file below, read with
 `git show <commit>:<path>` at the commit named, equals the reviewer's reading, printed from its
 simulation tree. Report each path beside the hash you read:
 | path | at | bytes | sha256 |
 |---|---|---|---|
 | .agent/decisions.md | C2 | 2487090 | 30c4c7492fa436877e1108fe68b2c5f459612fa05cf5a5a792bfc91e08ec5a1a |
 | .agent/live_review.md | C2 | 317572 | 339ed1ef27e7af3959d2335b6537719666649560a9c927b29136959d3c1e954d |
 | .agent/plan.md | C2 | 1018 | fc5092260eae70ca569d9ab9ac3794f708cc5930bdbfadb8fb46e29a394472e6 |
 | apps/ui/src/api/cockpitAddress.test.ts | C4 | 3565 | d098eebf3f08907d9cbe4d92001dc20c677e3955615b3639989cd4f6ef0fb446 |
 | apps/ui/src/api/homeGrid.test.ts | C4 | 4687 | dc68708ffc442cb13863a4a7c485aec189dc26c5573323dec7ce6b3852169b60 |
 | tests/ui_contracts/test_project_switcher_wiring.py | C4 | 3792 | 9c27a67507ad6f0313dbc8dbe08d4091fcedc701d1db7ed927d836009d304728 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT read with `git show <commit>:<path>` at
 C2 (the reviewer read `['R-1107', 'R-1108', 'R-1109']`), and `git diff --name-only <C1d> <C2>`,
 which must name exactly the C2 paths of the table above.

G3 THE CODE AND THE TESTS — at C5: `python3 -m ruff check
 tests/ui_contracts/test_project_switcher_wiring.py .agent/authored/f042-r4-mutations.py
 .agent/authored/f042-r4-render_measure.py`, and `apps/ui/node_modules/.bin/eslint
 src/RemedyApp.tsx src/api/cockpitAddress.ts src/api/homeGrid.ts src/api/homeGrid.test.ts
 src/components/home/HomeGrid.tsx src/components/shell/ProjectProvider.tsx
 src/components/shell/ProjectSwitcher.tsx` run with `apps/ui` as its working directory, each
 with its real exit code. Report `git show --numstat <C3>` and the diff of `RemedyApp.tsx` at
 C3, whole. Then, in the primary checkout at C5, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_live_state.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_project_brain.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_live_review_rotation.py tests/regression/test_resource_safety.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -10; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 Name the outcomes of `test_typescript_compiles`, `test_vitest_passes` and
 `tests/ui_contracts/test_ui_lint.py`. The reviewer ran the selection serially inside its
 simulation tree, which carries C2, this round's tests and the reviewer's own version of S1 to S6
 but no `.agent/authored/f042-r4-*` copy and no `node_modules`, and read `1756 passed, 8 skipped` at real
 exit code 0, with round 3's eight skips; through the primary's binaries in the same tree, `tsc`
 read exit 0 and the whole vitest suite `1954 passed | 5 skipped` over 97 files at exit 0. Report every `SKIPPED` line yours
 prints, and the vitest counts of `src/api/homeGrid.test.ts` and `src/api/cockpitAddress.test.ts`
 (the reviewer's read 10 and 13). Then `python3 -m apps.cli.main integrity check --json`, which
 must read all six checks `pass` at `fail_count` 0.

G4 THE RENDER — at C5, in the primary checkout:
 `python3 -B .agent/authored/f042-r4-render_measure.py /home/decodeux/Repos/remedy`. Report its
 whole output from the first `PASS` or `FAIL` line on, and its exit code; it must print
 `RENDER: 17 of 17 checks pass` and exit 0. Read both screenshots it writes,
 `/home/decodeux/Repos/remedy/.remedy-wt/f042-r4-render-switcher.png` and
 `/home/decodeux/Repos/remedy/.remedy-wt/f042-r4-render-home.png`, and say in one sentence each
 what it shows. The reviewer's own run over its version of S1 to S6 read 17 of 17.

G5 THE RED PROOFS — your tool `.agent/authored/f042-r4-mutations.py` takes a worktree path, and
 for each mutation below edits the named production file INSIDE that worktree (asserting its
 FROM text occurs exactly once there), runs the named check, restores the bytes, and prints one
 line per mutation: its label, the exit code, and the failed count or the harness's
 `RENDER: <n> of 17` reading with the names of its failing checks. Vitest runs as
 `<primary>/apps/ui/node_modules/.bin/vitest run --root <worktree>/apps/ui --config
 <primary>/apps/ui/vitest.config.ts <the file>` with `<worktree>/apps/ui` as the working
 directory (checklist item 33); pytest as `python3 -B -m pytest -q -p no:cacheprovider
 tests/ui_contracts/test_project_switcher_wiring.py` with the worktree as the working directory
 and first on `PYTHONPATH`; the harness as `python3 -B
 <worktree>/.agent/authored/f042-r4-render_measure.py <worktree>`. The primary is
 `/home/decodeux/Repos/remedy`. The tool runs an unmutated control of each check first and last,
 reports `restored byte-identical: True` after each restore, and ends with
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each is a real behaviour change:
  g1 `costTodayLine` reads an `absent` basis with a figure as that figure (`homeGrid.ts`,
     `src/api/homeGrid.test.ts`);
  g2 `HOME_PAGE_SIZE` is 10 (same);
  g3 a running state takes the `open` tone (same);
  a1 `homeSearch` keeps the project (`cockpitAddress.ts`, `src/api/cockpitAddress.test.ts`);
  w1 `onHome` is a plain function rebuilt on every render (`RemedyApp.tsx`, the wiring test);
  x1 R-1109: the provider's effect no longer advances the gate on a new project
     (`ProjectProvider.tsx`, the harness, whose R-j must fail);
  x2 R-1108: the empty project's div loses `alignContent` and its gap (`RemedyApp.tsx`, the
     harness, whose R-i must fail);
  h1 `writeAddress` pushes even when asked to replace (`RemedyApp.tsx`, the harness);
  h2 a card's click does nothing (`HomeGrid.tsx`, the harness);
  h3 the page's summaries are read but never stored (`HomeGrid.tsx`, the harness).
 Run it: `git worktree add --detach .remedy-wt/f042-r4-mut <C5>`, then in Python
 `os.symlink("/home/decodeux/Repos/remedy/apps/ui/node_modules",
 "/home/decodeux/Repos/remedy/.remedy-wt/f042-r4-mut/apps/ui/node_modules",
 target_is_directory=True)`, then
 `python3 -B .agent/authored/f042-r4-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f042-r4-mut`
 and report its whole output. The reviewer's own version of this probe turned every one red with
 every control passing, x1 failing R-j alone and x2 failing R-i alone. EVERY mutation must exit
 non-zero; one that stays green is reported as green, never papered over, and you then STOP and
 report it. Then remove the symlink with `os.unlink`, `git worktree remove --force
 .remedy-wt/f042-r4-mut`, `git worktree prune`, and report `git worktree list | wc -l`.

G6 TREE AND PUSH — after C6: `git status --porcelain`, which must be empty;
 `git log --oneline -n 10`, which must show C6, C5, C4, C3, C2, C1d, C1c, C1b, C1a and
 `9d45d7491` in that order; `git worktree list | wc -l`, which must equal your step 4 reading;
 the push's real outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`,
 which must be EMPTY. These readings go in your reply, since C6 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3's own files, C4 and C5 —
report what you measure), every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and the
next expected action. Report what you ran, not what you expected to find. Your Session section
reads SESSION 1 of feature F042, round 4, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 4, then the next round (deep links across projects, the dashboard's old project summary
re-pointed, a way home at every width, and the end-to-end run).
State the open-findings count, 3, and the operator-questions count, 1.

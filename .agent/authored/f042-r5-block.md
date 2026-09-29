STEP F042 R5 — DEEP LINKS, THE DASHBOARD'S PROJECT LINE, A WAY HOME AT EVERY WIDTH, AND R-1110

GOAL
Book round 4's PASS with the resolutions of R-1108 and R-1109 and the registration of R-1110,
record DECISION F042 D5, and land against the reviewer's tests and render harness: the dock's
Overview opening the home grid, the home card's stateless result keeping a transparent border
(R-1110), and the dashboard's project line reading the job's own project and counting
`scoped_jobs`. Deep links across projects gain a test and no code.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE TESTS ARE THE REVIEWER'S AND THE CODE IS YOURS:
the test edits and the render harness travel as payloads and are the acceptance, and you write
the production code against them and against S1 to S3 below. You never edit a payload; if one
looks wrong to you, STOP and report it. Read DECISION F042 D5 and R-1110 in the records diff
before you write code, and read whole, before you edit them, every file S1 to S3 names and
`tests/ui_server/test_pipeline_contract.py`'s `TestProjectSummaryModelConfidence`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f042-r5-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f042-r5/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f042-r1-*` to `.remedy-wt/f042-r4-*`, `.remedy-wt/f042-r5-dry/`,
  `.remedy-wt/f042-r5-sim/`, `.remedy-wt/f042-r5-scratch/`
                                  The reviewer's trees and scripts; do not touch them.
  `.remedy-wt/f042-r5-worker/`    YOURS for logs and scripts; create it if absent. All are
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
   `feature/f042-multi-project-cockpit`, and `git log --oneline -1` must read `1d5a64b3a`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f042-r5/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f042-r5-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 57 | 10435 | 582afa51fc74dd0936c3ea0fb2e3d3895e2ce4f63a364d0b8efa9a1468620ea2 |
| tests.diff | 65 | 3598 | 1872d1735b50fedbe16b54d003b9b3bf5c743118b73d3996d63157e0ac2624d0 |
| plan.md | 27 | 911 | 61877627084cba8cc86bf5538b4b6aaaaa286cfc4e4123c79bb25bfb6e8136c4 |
| render_index.html | 11 | 243 | 48f7d0b2ee38d585b45fe87e9d62daf2bcd4eba07995972a90a1503d6b47ea7f |
| render_main.tsx | 66 | 3472 | 8afd5abcde87a0aeeb46ab26904db891a7170c9066302daaed1c26be6740bf80 |
| render_vite.config.mjs | 28 | 744 | 6c9d24558a507a827d445c793cd6203f7f0f24ac2659dcfe3cff96c20b7d1c6a |
| render_drive.mjs | 308 | 17416 | c9551a69df8b44140d3c04007881933295520d80aed0616dea45f06c7efcb921 |
| render_measure.py | 187 | 6528 | d9caa35ebddfad32188761510f32d9972d913551d4861b41ef07f5fd57defbf9 |

`plan.md` is a REWRITE of `.agent/plan.md`. The two `.diff` files go on with `git apply`; the
reviewer generated them with `git diff HEAD` from a tree at `1d5a64b3a`. `records.diff` appends
round 4's gate entry, the `Done:` resolutions of R-1108 and R-1109 and the registration of R-1110
to `.agent/live_review.md`, and DECISION F042 D5 to `.agent/decisions.md`. `tests.diff` edits
`apps/ui/src/components/graph/zoomDeepLink.test.ts` and `tests/ui_server/test_projects_route.py`.
The five `render_*` files are the round's render harness; they are copied, never applied, and run
from their copies.

THE SPECIFICATION — the tests are the acceptance; these clauses fix what they leave open.
S1 `apps/ui/src/components/rail/SideIconDock.tsx`: export `OVERVIEW_TITLE = "All projects"` under
   a comment naming DECISION F042 D5; the component reads `goHome` from `useProjectContext()`
   (imported from `../shell/ProjectProvider`), and the first button, Overview, gets
   `title={OVERVIEW_TITLE}` and `onClick={goHome}`; the other six buttons are unchanged, the
   seven labels, their order and the `aria-label` on each stay, and no colour literal is added.
S2 `apps/ui/src/components/home/HomeGrid.tsx`, R-1110: the result line's inline
   `borderLeftColor` is set only for the tones `done`, `current`, `blocked` and `open`; a
   result whose tone is `none` carries no inline style, so the sheet's transparent border holds,
   under a one-line comment naming R-1110. Nothing else in the file changes.
S3 `packages/orchestration/ui_server.py`, `_build_project_summary_section`: its docstring gains
   a paragraph naming DECISION F042 D5; the project id is
   `str(getattr(job, "project_id", "") or job.metadata.get("project_id") or "")`; the linked
   jobs are the first value of `scoped_jobs(ProjectScope(project_id=str(project.id),
   all_projects=False, source="dashboard"))`, imported inside the function from
   `packages.orchestration.project_scope`, and the now unused `list_job_plans` import is
   dropped. The section's keys, their order and the rest of the function are unchanged.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C2, C3, C4, C5 and C6, in this order.

C1a — `.agent/authored/f042-r5-block.md` := this block and `.agent/authored/f042-r5-plan.md` :=
  plan.md, by `shutil.copyfile`. Subject: `F042 R5 C1a: copy round 5 block and plan into .agent/authored/`
  Its insertions are this block's line count plus 27; STOP rather than commit at 500.
C1b — `.agent/authored/f042-r5-records.diff` and `.agent/authored/f042-r5-tests.diff` := the two
  diffs. Subject: `F042 R5 C1b: copy round 5 records and tests diffs into .agent/authored/`
  Expected insertions: 122.
C1c — `.agent/authored/f042-r5-render_drive.mjs` := render_drive.mjs.
  Subject: `F042 R5 C1c: copy the round 5 render driver into .agent/authored/`
  Expected insertions: 308.
C1d — the other four `render_<x>` := `.agent/authored/f042-r5-render_<x>`.
  Subject: `F042 R5 C1d: copy the rest of the round 5 render harness into .agent/authored/`
  Expected insertions: 292.
C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F042 R5 C2: book F042 R4, resolve R-1108 and R-1109, register R-1110, record D5`
  Expected by `git show --numstat` (insertions and deletions): 33/0 .agent/decisions.md, 8/0 .agent/live_review.md, 7/9 .agent/plan.md.
C3 — THE CODE: S1 to S3 in one commit.
  Subject: `F042 R5 C3: open the grid from the dock, keep a stateless result plain, count the project's own jobs`
  The reviewer's own version of S1 to S3 read 3/1 apps/ui/src/components/home/HomeGrid.tsx, 8/1 apps/ui/src/components/rail/SideIconDock.tsx, 10/5 packages/orchestration/ui_server.py.
C4 — THE TESTS: `git apply` tests.diff.
  Subject: `F042 R5 C4: add the reviewer's tests for deep links across projects and the project line`
C5 — THE TOOL: your mutation tool (G5) saved as `.agent/authored/f042-r5-mutations.py`.
  Subject: `F042 R5 C5: add the round 5 mutation tool`
C6 — THE HANDBACK: `.agent/handoff.md`, rewritten, its own commit, per
  `docs/agents/handback_template.md`. Subject: `F042 R5 C6: rewrite handoff for round 5`
  Then `git push`. Do NOT create a pull request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading.
3. The round's whole tracked path set is: the `.agent/authored/f042-r5-*` copies and tool, the
   paths records.diff and tests.diff edit, `.agent/plan.md`, the files S1 to S3 name, and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only 1d5a64b3a` at the
   branch tip after C6. Do NOT touch `apps/ui/src/components/graph/zoomDeepLink.ts`,
   `apps/ui/src/RemedyApp.tsx`, `apps/ui/src/api/`, `apps/cli/`, `apps/ui/package.json`,
   `apps/ui/package-lock.json`, `docs/`, `.agent/context.md`, `.agent/prose_slips.md`,
   `.agent/candidates.md`, `.agent/operator_questions.md` or `README.md`, and write no
   `Landed:` or `Done:` line.
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
 against the PAYLOADS table. Then compare each `.agent/authored/f042-r5-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f042-r5/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS AND THE TESTS — the sha256 of each file below, read with
 `git show <commit>:<path>` at the commit named, equals the reviewer's reading, printed from its
 simulation tree. Report each path beside the hash you read:
 | path | at | bytes | sha256 |
 |---|---|---|---|
 | .agent/decisions.md | C2 | 2489869 | bcf06d750d134cdb997e135568e9b058a2b89c594d7737eb78a148839ffb3cde |
 | .agent/live_review.md | C2 | 322281 | a23329e702857e8fcebec2306e166401995eac3d90ff6916c58a86d1a6eabb9b |
 | .agent/plan.md | C2 | 911 | 61877627084cba8cc86bf5538b4b6aaaaa286cfc4e4123c79bb25bfb6e8136c4 |
 | apps/ui/src/components/graph/zoomDeepLink.test.ts | C4 | 4397 | 53a4a98d403c1b8d5ee1df2ac2f9dbe7d225227fe1f34b1e0d3e9d72fc604457 |
 | tests/ui_server/test_projects_route.py | C4 | 6615 | 909cf7d0f74e3c92bacffaf5e52d6c059a9bd2a4ade02f87a0a47c0464a511dd |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT read with `git show <commit>:<path>` at
 C2 (the reviewer read `['R-1107', 'R-1110']`), and `git diff --name-only <C1d> <C2>`, which
 must name exactly the C2 paths of the table above.

G3 THE CODE AND THE TESTS — at C5: `python3 -m ruff check packages/orchestration/ui_server.py
 tests/ui_server/test_projects_route.py .agent/authored/f042-r5-mutations.py
 .agent/authored/f042-r5-render_measure.py`, and `apps/ui/node_modules/.bin/eslint
 src/components/rail/SideIconDock.tsx src/components/home/HomeGrid.tsx
 src/components/graph/zoomDeepLink.test.ts` run with `apps/ui` as its working directory, each
 with its real exit code. Report `git show --numstat <C3>` and C3's diff, whole. Then, in the
 primary checkout at C5, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_live_state.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_project_brain.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_live_review_rotation.py tests/regression/test_resource_safety.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py tests/ui_server/test_projects_route.py tests/ui_server/test_pipeline_contract.py 2>&1 | tail -10; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 Name the outcomes of `test_typescript_compiles`, `test_vitest_passes` and
 `tests/ui_contracts/test_ui_lint.py`. The reviewer ran the selection serially inside its
 simulation tree, which carries C2, this round's tests and the reviewer's own version of S1 to S3
 but no `.agent/authored/f042-r5-*` copy and no `node_modules`, and read `1780 passed, 8 skipped` at real
 exit code 0, with round 4's eight skips; through the primary's binaries in the same tree, `tsc`
 read exit 0 and the whole vitest suite `1956 passed | 5 skipped` over 97 files at exit 0. Report every `SKIPPED` line yours
 prints and the vitest count of `src/components/graph/zoomDeepLink.test.ts` (the reviewer's read
 22). Then `python3 -m apps.cli.main integrity check --json`, which must read all six checks
 `pass` at `fail_count` 0.

G4 THE RENDER — at C5, in the primary checkout:
 `python3 -B .agent/authored/f042-r5-render_measure.py /home/decodeux/Repos/remedy`. Report its
 whole output from the first `PASS` or `FAIL` line on, and its exit code; it must print
 `RENDER: 19 of 19 checks pass` and exit 0. Read both screenshots it writes,
 `/home/decodeux/Repos/remedy/.remedy-wt/f042-r5-render-switcher.png` and
 `/home/decodeux/Repos/remedy/.remedy-wt/f042-r5-render-home.png`, and say in one sentence each
 what it shows. The reviewer's own run over its version of S1 to S3 read 19 of 19.

G5 THE RED PROOFS — your tool `.agent/authored/f042-r5-mutations.py` takes a worktree path, and
 for each mutation below edits the named file INSIDE that worktree (asserting its FROM text
 occurs exactly once there), runs the named check, restores the bytes, and prints one line per
 mutation: its label, the exit code, and the failed count or the harness's `RENDER: <n> of 19`
 reading with the names of its failing checks. Vitest runs as
 `<primary>/apps/ui/node_modules/.bin/vitest run --root <worktree>/apps/ui --config
 <primary>/apps/ui/vitest.config.ts src/components/graph/zoomDeepLink.test.ts` with
 `<worktree>/apps/ui` as the working directory (checklist item 33); pytest as `python3 -B -m
 pytest -q -p no:cacheprovider tests/ui_server/test_projects_route.py` with the worktree as the
 working directory and first on `PYTHONPATH`; the harness as `python3 -B
 <worktree>/.agent/authored/f042-r5-render_measure.py <worktree>`. The primary is
 `/home/decodeux/Repos/remedy`. The tool runs an unmutated control of each check first and last,
 reports `restored byte-identical: True` after each restore, and ends with
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each is a real behaviour change:
  p1 the section reads only `job.metadata["project_id"]` (`ui_server.py`, pytest);
  p2 the section counts only the jobs the registry record's `job_ids` lists (same);
  z1 `searchWithZoom` also deletes `project`, in `apps/ui/src/components/graph/zoomDeepLink.ts`,
     which this round does not otherwise touch (vitest);
  h1 R-1110: every tone, `none` included, sets the inline border colour (`HomeGrid.tsx`, the
     harness, whose H-h must fail);
  h2 the Overview button's click does nothing (`SideIconDock.tsx`, the harness, whose H-i must
     fail).
 Run it: `git worktree add --detach .remedy-wt/f042-r5-mut <C5>`, then in Python
 `os.symlink("/home/decodeux/Repos/remedy/apps/ui/node_modules",
 "/home/decodeux/Repos/remedy/.remedy-wt/f042-r5-mut/apps/ui/node_modules",
 target_is_directory=True)`, then
 `python3 -B .agent/authored/f042-r5-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f042-r5-mut`
 and report its whole output. The reviewer's own version of this probe turned every one red with
 every control passing, h1 failing H-h alone and h2 H-i alone. EVERY mutation must exit
 non-zero; one that stays green is reported as green, never papered over, and you then STOP and
 report it. Then remove the symlink with `os.unlink`, `git worktree remove --force
 .remedy-wt/f042-r5-mut`, `git worktree prune`, and report `git worktree list | wc -l`.

G6 TREE AND PUSH — after C6: `git status --porcelain`, which must be empty;
 `git log --oneline -n 10`, which must show C6, C5, C4, C3, C2, C1d, C1c, C1b, C1a and
 `1d5a64b3a` in that order; `git worktree list | wc -l`, which must equal your step 4 reading;
 the push's real outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`,
 which must be EMPTY. These readings go in your reply, since C6 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3's own files, C4 and C5 —
report what you measure), every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and the
next expected action. Report what you ran, not what you expected to find. Your Session section
reads SESSION 1 of feature F042, round 5, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 5, then the next round (the end-to-end run over a real UI server with two projects).
State the open-findings count, 2, and the operator-questions count, 1.

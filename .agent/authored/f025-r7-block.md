STEP F025 R7 — BOOK ROUND 6, REPAIR R-1053 AND R-1054, THEN THE END-TO-END: PAUSE A LIVE JOB, RELAUNCH IT THROUGH `remedy job run`, AND MATCH AN UNPAUSED CONTROL

GOAL
Round 6 PASSED with two findings against its own specification; the payload `ledger.md` books the
verdict and registers R-1053, R-1054 and R-1055 — read all three whole, the FIX clauses of the
first two are this round's first spec. Persist them, repair R-1053 and R-1054, assign R-1055 to
F285, then land DECISION F025 D5 — the payload `d5.md`, read it whole before writing code: the
live end-to-end test of both scopes against an unpaused control run.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, write the handback. You never
issue a verdict, never merge, and never write a `Done:` line. THE PRODUCTION CHANGE IS SPECIFIED,
NOT SLICED: you write the code and tests against the FIX clauses and E1 to E5. Read first:
`apps/ui/src/api/pauseView.ts` with its test, `apps/ui/src/components/detail/DetailPopover.tsx`,
`tests/ui_contracts/test_pause_controls_contract.py`; `tests/ui_server/test_pause_door_live.py`
whole (its runner template, `_start_ui_server_for_job`, `_post`, `_test_owned_children`);
`tests/orchestration/test_pause_resume.py`'s control-run test; `_normalize` in
`tests/orchestration/test_long_run_executor.py`; `_cmd_job_run` in `apps/cli/commands/do_cmd.py`;
`run_job`, `park_job_pause`, `lift_job_pause` and `_export_job` in
`packages/orchestration/pingpong_job.py`; `create_provider` and `FakeProvider` in
`packages/orchestration/pingpong_provider.py`; and `.agent/authored/f025-r4-mutations.py`, whose
route for running the live door tests inside a worktree you reuse, beside
`.agent/authored/f025-r6-mutations.py`'s vitest route.

THE DIRECTORIES
  `.remedy-wt/f025-r7/`          READ-ONLY. This block, its payloads and the reviewer's scripts.
  `.remedy-wt/f025-r7-worker/`   YOURS for logs and scripts; create it if absent. Both gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, command substitution, `cd <dir> && git ...`, and
multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `git -C <path>`, never `cd` your shell into a worktree.
Copy and hash with python (`shutil.copyfile`). A heredoc containing a dollar-brace is refused: write
such a script under your own directory and run the file. Never run npm or npx.

COMMIT TRAILER — every commit ends with exactly this line:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop.
2. In the primary checkout `/home/decodeux/Repos/remedy`: report `pwd`; `git status --porcelain`
   must be empty, `git branch --show-current` must read `feature/f025-pause-resume`, and
   `git log --oneline -1` must read `218eaabd`.
3. Measure this block's line count and sha256 (`.remedy-wt/f025-r7/block.md`) and compare both
   with your delegation message's readings; stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f025-r7/`, lines = newline count; verify each BEFORE use:
| file | lines | bytes | sha256 |
|---|---|---|---|
| d5.md | 40 | 3598 | ed1e3cbe9bb6260a34b62566e37dbb212d7f9ca2ca42a1d05731c2758e3658ed |
| f285_from.txt | 2 | 158 | 6a0b143fdfd9174e0207e23204a77ea665a6c7f47304f95fa2855e7246ba6b16 |
| f285_to.txt | 5 | 420 | 0042628780e7b0cbc005834af82df2b147ecf8f7f68b589252542f2e961b6bb7 |
| ledger.md | 8 | 6832 | 8ad8cf41fc8c8ab374f794508144cde7a9d3584d609c9a547afbd394aa33b580 |
| plan.md | 29 | 994 | f8850294770e67af6117dd6e8f75c5cc9c0bf471b0bad6b5865e456281a52a19 |
`ledger.md` is appended to `.agent/live_review.md` and `d5.md` to `.agent/decisions.md` (each
starts with its own blank line); `plan.md` REWRITES `.agent/plan.md`. In
`docs/roadmap/features/T2_F285.md`, the bytes of `f285_from.txt` are replaced by the bytes of
`f285_to.txt` — containment test: TO contains FROM: true, so the pair is an APPEND: FROM occurs
exactly once in the file before the edit, and after it TO occurs exactly once and the file equals
its `218eaabd` bytes with FROM replaced by TO.

THE END-TO-END, DECISION F025 D5
E1 THE FILE: NEW `tests/ui_server/test_pause_e2e_live.py`, marked as `test_pause_door_live.py`'s
   live tests are, with its own copies of that file's helpers as that file's own header rules.
E2 THE FIRST RUNNER is a script the test writes and starts with `subprocess.Popen`, as the door
   test's is: it runs `run_job` on a three-task job with a `FakeProvider` subclass that keeps the
   CLI's own fake defaults — the values `create_provider("fake")` uses — and the CLI's own repair
   rounds, adding only a per-call sleep. Read `_cmd_job_run` and `create_provider` for those
   values; never assume them.
E3 JOB SCOPE: once the first task is applied the test sends `job.pause` through the real door; the
   process exits with the job `paused` and `_test_owned_children` empty; `job.unpause` answers
   `parked` with `next` equal to `remedy job run <job id>`; the test runs exactly that command as
   `python3 -m apps.cli.main job run <job id>` in a subprocess with the test's data root and the
   worktree's own root on its `PYTHONPATH`; it exits 0, the job is `completed` with exactly one
   `job_resumed`, no process of the test's own is left, and the task finished before the park keeps
   its run id — it was not run again.
   TASK SCOPE: the third task is paused through the door before it starts; the process exits with
   the job `paused`; `job.unpause` with that task answers `released`; the same relaunch completes
   the job with no process left.
E4 THE CONTROL: the same job file run once, unpaused, by the same first runner. EQUALITY, for each
   scope against its control: the `_export_job` record with one written-once list of fields removed
   or renumbered, each entry carrying a one-line reason — the job id and every value that contains
   it, timestamps, run ids and run references, artifact ids, the run manifest's episodes and episode
   fields, and any pause-event metadata — compared whole; every workspace file's bytes; and the
   ordered task-level event names without `job_paused`, `job_resumed`, `task_paused` and
   `task_resumed`. A field you find differing that is not in that class is a FINDING for the
   handback, never a new entry in the list.
E5 R-1053'S FIX and R-1054'S FIX, each exactly as its FIX clause states, with the tests it names.

BUNDLE — commits in this order; split any that would reach 500 insertions and say so.
C1a COPIES: `.agent/authored/f025-r7-block.md` := this block and each payload as
    `.agent/authored/f025-r7-<name>`. Subject `F025 R7 C1a: copy round 7 block and payloads`.
    Expected by `git show --numstat`: this block's line count plus 84, that is the block copy's own lines and 40/0 `.agent/authored/f025-r7-d5.md`, 2/0 `.agent/authored/f025-r7-f285_from.txt`, 5/0 `.agent/authored/f025-r7-f285_to.txt`, 8/0 `.agent/authored/f025-r7-ledger.md`, 29/0 `.agent/authored/f025-r7-plan.md`.
C1b RECORDS, one commit, the findings persisted FIRST: the ledger and decisions appends, the plan
    rewrite and the F285 pair. Subject `F025 R7 C1b: book round 6, register R-1053 to R-1055,
    record D5`. Expected: 40/0 `.agent/decisions.md`, 8/0 `.agent/live_review.md`, 8/9 `.agent/plan.md`, 3/0 `docs/roadmap/features/T2_F285.md`.
C2 R-1053's FIX with its tests. C3 R-1054's FIX with its test. C4 E1 to E4. C5 THE MUTATION TOOL,
    `.agent/authored/f025-r7-mutations.py`. Subjects are yours, each beginning `F025 R7 C<n>: `.
C6 THE HANDBACK, `.agent/handoff.md`. Subject `F025 R7 C6: rewrite handoff for round 7`. Then
    `git push origin feature/f025-pause-resume`.

CONSTRAINTS
1. Never edit or retype a payload. Append and replace by python, bytes to bytes.
2. Every commit under 500 insertions by `git show --numstat`. No `# noqa: BLE001` is added.
3. The round's tracked path set is: the `.agent/authored/f025-r7-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `.agent/handoff.md`,
   `docs/roadmap/features/T2_F285.md`, `apps/ui/src/api/pauseView.ts` with its test,
   `apps/ui/src/components/detail/DetailPopover.tsx`,
   `tests/ui_contracts/test_pause_controls_contract.py`, and `tests/ui_server/test_pause_e2e_live.py`.
   Never weaken an assertion or delete a test. NO PRODUCTION FILE under `packages/` or `apps/cli/`
   changes: if E3 or E4 cannot pass without one, STOP under constraint 4 and report the field, the
   command and the reading.
4. A red gate: STOP, commit and push what is verified, write the handoff under AGENTS.md "If
   Blocked". Nothing is merged; no `gh pr create`; no force-push; no `git stash`.
5. Leave every existing worktree alone; the one G5 adds is removed as that step's last action.
6. DO NOT run the full suite (amend0917 rule 1).

DONE-WHEN — every gate executed, every reading reported with its real exit code. G1 to G5 run
before C6 is written.
G1 TRANSPORT: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f025-r7-*` payload copy byte-equal to its source by `git show <C1a>:<path>`
   (the block copy against `.remedy-wt/f025-r7/block.md`); at C1b the appended files equal their
   `218eaabd` bytes plus their payloads, `.agent/plan.md` equals plan.md, and the F285 pair holds as
   PAYLOADS states; and `open_finding_ids` over the ledger at C1b — the reviewer's simulation read
   `['R-1008', 'R-1053', 'R-1054', 'R-1055']`.
G2 THE CODE: `python3 -m ruff check` over every Python file C2 to C5 changed; `git diff --stat
   218eaabd <C5> -- packages apps/cli` empty; the count of `noqa: BLE001` marks the range adds under
   `packages`, `apps` and `scripts`, which must be 0; and `git diff --name-only <C1b> <C5>`, every
   path inside constraint 3.
G3 THE TESTS NEAREST THE CHANGE, serially: `python3 -m pytest -q -p no:cacheprovider
   tests/ui_server/test_pause_e2e_live.py tests/ui_server/test_pause_door_live.py
   tests/orchestration/test_pause_resume.py tests/ui_contracts/test_pause_controls_contract.py
   tests/ui_contracts/test_ui_lint.py tests/ui_server/test_dashboard_contract.py
   tests/orchestration/test_test_runner.py tests/cli/test_golden_path.py tests/docs/` — exit 0,
   with the tsc, eslint and vitest nodes PASSING, not skipped; report the summary line and every
   `SKIPPED` line. Then the e2e file alone twice more, serially, each summary reported.
G4 THE NEIGHBOURS: first `python3 -m pytest -q -p no:cacheprovider
   tests/ui_server/test_command_channel.py` alone, serially; then `python3
   .remedy-wt/f025-r7/run_sel.py /home/decodeux/Repos/remedy 8` in the primary checkout at C5 —
   round 6's selection plus the e2e file, with 8 xdist workers. At `218eaabd` the reviewer read
   `9697 passed, 13 skipped` at exit 0 over round 6's 144 files, the e2e file not yet existing. Report its output; re-run any failing node's file alone, serially, and report both
   readings. Then `python3 -m apps.cli.main integrity check --json`: six `pass`, `fail_count` 0.
G5 THE RED PROOFS: your tool takes a worktree path, edits the named file INSIDE that worktree
   (asserting each FROM occurs exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider`
   over the files named per mutation from the worktree root after purging `__pycache__`, or vitest
   over `pauseView.test.ts` by `.agent/authored/f025-r6-mutations.py`'s route, and prepares the
   worktree for the live tests by `.agent/authored/f025-r4-mutations.py`'s route. It restores, and
   prints per mutation its label, runner, exit code, failed count and failing test names, with an
   unmutated control of BOTH runners first and last, `restored byte-identical: True` per file, and
   a final `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Mutations:
    m1 `taskPauseAction` answers `pause` for a task in state `current` [vitest];
    m2 the popover's `key={task.id}` is deleted [pytest, the contract test];
    m3 `lift_job_pause`'s body is replaced by `raise RuntimeError("m3 probe")` [pytest, the e2e];
    m4 `unpause_job_command` answers `not_paused` where it answers `parked` [pytest, the e2e];
    m5 the park leaves `job.pause` empty — in `park_job_pause`, the pause record is assigned `{}`
       [pytest, the e2e].
   `git worktree add --detach .remedy-wt/f025-r7-mut <C5>`, run
   `python3 -B .agent/authored/f025-r7-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f025-r7-mut`,
   report the whole output. EVERY mutation must be red; one that stays green is reported green, the
   catching test is added in a further commit before C6, and the tool re-run. Then undo the tool's
   worktree preparation, `git worktree remove --force .remedy-wt/f025-r7-mut`, `git worktree
   prune`, `git worktree list`.
G6 AFTER C6 AND THE PUSH, in your final reply only: `git status --porcelain` empty, the local tip
   equal to `origin/feature/f025-pause-resume`, `git log --oneline -n 10`, the push's real outcome,
   and `gh pr list --state open --json number` EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the `git show --numstat` counts you measured (compared with
C1a's and C1b's expectations above), every gate's real output, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, the
removed-field list of E4 with its reasons, and the next action. Session section: SESSION 2 of
feature F025, round 7, plus one sentence on how much context you had left. `## Next`: Phase 1 rule
1, the review of round 7, then F025's closure sequence. State the open-findings count as the script
reads it at C1b, and "Operator questions open: <the count of `### Q` headings in the file at C1b>".

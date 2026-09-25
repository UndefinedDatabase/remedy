STEP F025 R4 — T002: `job.pause` AND `job.unpause` IN THE CATALOG, THE CLI AND THE WRITE DOOR, WITH LIVE FAKE-JOB TESTS OF BOTH SCOPES

GOAL
Round 3 PASSED (booked by C1b below, with R-1049's and R-1050's resolutions). Land T002 exactly as
DECISION F025 D2 rules it — the payload `d2.md`, which C1b appends to `.agent/decisions.md`; read
it whole before writing code: two catalog ids with an optional task, one set of effects shared by
the CLI and the door, the task pause events, the door's audited clauses and import guard, and live
tests that drive both scopes of a real fake-provider job through the real door.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, write the handback. You never
issue a verdict, never merge, and never write a `Done:` line. THE PRODUCTION CHANGE IS SPECIFIED,
NOT SLICED: you write the code and tests against D2 and P1 to P7. Read first:
`apps/cli/commands/job_stop_cmd.py` and `tests/cli/test_job_stop.py` (the CLI template); the door's
`_handle_command_submission`, `_dispatch_job_stop` and `_dispatch_chat_send` in
`packages/orchestration/ui_server.py`; `TestCommandDoorImportGuard` and `TestUiExposedCommands` in
`tests/ui_server/test_command_channel.py`; `tests/ui_server/test_command_dispatch.py`;
`tests/cli/test_job_refusal_envelope.py`; `tests/cli/test_advertised_commands.py`;
`packages/orchestration/pause_control.py`; and the live-runner helpers of
`tests/orchestration/test_job_stop_integration.py` (`_RUNNER`, `SlowProvider`,
`_test_owned_children`).

THE DIRECTORIES
  `.remedy-wt/f025-r4/`          READ-ONLY. This block, its payloads and the reviewer's scripts.
  `.remedy-wt/f025-r4-worker/`   YOURS for logs and scripts; create it if absent. Both gitignored.

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
   `git log --oneline -1` must read `62e43ee8`.
3. Measure this block's line count and sha256 (`.remedy-wt/f025-r4/block.md`) and compare both
   with your delegation message's readings; stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f025-r4/`, lines = newline count; verify each BEFORE use:
| file | lines | bytes | sha256 |
|---|---|---|---|
| d2.md | 49 | 4324 | 2a4cb7e224ede77e05fef88b9b4b990974724dc08ff1d3f38813c48c6758eca3 |
| ledger.md | 6 | 4199 | b906f739fdf6eb9ea9c96bfa4ee2f3e18848551d28ce606063a777eb2518879a |
| plan.md | 33 | 1155 | 7f428ae0fb39c8e2c58850c33eabc559c653a91cf1f3321892c51de2f77d4061 |
| q4.md | 25 | 1845 | ce9bf59e31b6ee4333d67336949806fd8a98793c44f080079c72ff948b090275 |
`ledger.md` is appended to `.agent/live_review.md`, `d2.md` to `.agent/decisions.md`, and `q4.md`
to `.agent/operator_questions.md` (each starts with its own blank line); `plan.md` REWRITES
`.agent/plan.md`.

THE SPECIFICATION
P1 THE CATALOG. `job.pause` and `job.unpause` in `apps/cli/command_catalog.py`, `write_metadata`,
   no repo mutation, no command execution, exit codes `(0, 1, 2, 3)` as `job.stop`; `job.pause`
   takes the job id, `--task`, `--reason`, `--source` (default `cli`) and `--json`; `job.unpause`
   the job id, `--task`, `--source` and `--json`. Both join `UI_EXPOSED_COMMANDS`, whose comment
   cites DECISION F025 D2.
P2 THE EFFECTS, in `packages/orchestration/pause_control.py`, called by the CLI and the door alike:
   `pause_job_command(job, *, task_id=None, reason="", source)` and
   `unpause_job_command(job, *, task_id=None, source)`, where `job` is a loaded `JobPlan`. Each
   RETURNS a JSON-ready dict with an `outcome` and never raises for a refusal: a job whose state is
   completed, failed or cancelled, or a task id the plan does not hold, returns outcome `refused`
   with a `reason` naming the state or the task. The accepted outcomes are D2 clause (2)'s:
   `requested` (job pause), `paused` (task), `released`, `withdrawn`, `parked` (with a `next` field
   holding `remedy job run <job id>`) and `not_paused`, plus the request ids and scope. A task
   pause writes `task_paused`, and a release writes `task_resumed`, EXACTLY ONCE per task pause
   request id — only when the call created, or released, the entry — each an inline literal
   through `RunLogWriter`, the ledger the UI's event stream reads. A `PauseControlError` propagates.
P3 THE CLI. A NEW FILE at `apps/cli/commands/job_pause_cmd.py`, modelled on `job_stop_cmd.py` —
   its job id resolution, its usage and unknown-job exits 2 and 3, its JSON envelope with
   `schema_version` 1 — registered in its `COMMAND_HANDLERS` and in
   `apps/cli/commands/__init__.py`. A `refused` outcome exits 1; every other outcome exits 0. The
   human lines are plain sentences: a job pause says it takes effect at the next safe point; a
   `parked` answer says the job is paused and saved and names the command that continues it.
P4 THE DOOR. A clause per id in `_handle_command_submission`, in DECISION F009 D18's order, and a
   dispatch method per id calling P2 with the loaded job, the task from `args.task` when it is a
   string, the reason from `args.reason` likewise, and the door's own source. A `refused` outcome
   is answered 409 and audited `rejected_state`; a raised effect keeps the existing
   `rejected_effect` path. `TestCommandDoorImportGuard.DOOR_METHODS` gains the two methods and its
   `ALLOWED_IMPORTS` the two effect names, each commented `# F025 D2`; the exact-set test of
   `UI_EXPOSED_COMMANDS` gains the two ids.
P5 THE REGISTRIES. `task_paused` and `task_resumed` join `EVENT_NAMES` and
   `apps/ui/src/api/humanizeCatalog.ts` (`"A task was paused."`, `"A task was resumed."`) in the
   commit that writes them.
P6 THE DOCS. `docs/guides/exit-codes.md` lists `remedy job stop` in its per-command table; add a
   row for each new verb in the same shape.
P7 SIZE. Every commit under 500 inserted lines; split a commit and say so rather than exceed it.

THE TESTS
T1 A NEW FILE at `tests/cli/test_job_pause.py`, modelled on `tests/cli/test_job_stop.py`: each
   outcome of P2 through the dispatcher with `--json`, idempotence of a second pause, the task
   pause and release writing their events exactly once, exit 2 for a malformed id, exit 3 for an
   unknown job, exit 1 with the named state for a completed job and with the named task for an
   unknown task, and the catalog, handler and parser wiring.
T2 A NEW FILE at `tests/ui_server/test_pause_door_live.py`: a fake-provider job running in its OWN
   PROCESS (the live-runner pattern of `test_job_stop_integration.py`) and a UI server for it (the
   helpers of `test_command_dispatch.py`), driven through real HTTP:
   L1 JOB SCOPE — POST `job.pause` answers 200; the runner process exits by itself; the job reads
      `paused` with `pause.scope` `job`; the provider call in flight finished and no next call
      started; `_test_owned_children` is empty; POST `job.unpause` answers `parked` with the
      relaunch command; running that command completes the job with one `job_resumed`;
   L2 TASK SCOPE — on a three-task job, POST `job.pause` naming the third task while the first
      runs: the first two complete, the job parks withholding the third, one `task_paused`; POST
      `job.unpause` naming it answers `released` with one `task_resumed`; the relaunch completes;
   L3 REFUSALS — an unknown task and a completed job each answer 409, audited `rejected_state`;
   L4 WITHDRAW — a pause requested on a job not running, then POST `job.unpause`, answers
      `withdrawn`, and a later `remedy job run` completes the job without parking.

BUNDLE — commits in this order; split any that would reach 500 insertions and say so.
C1a COPIES: `.agent/authored/f025-r4-block.md` := this block, and each payload copied as
    `.agent/authored/f025-r4-<name>`. Subject `F025 R4 C1a: copy round 4 block and payloads`.
    Expected by `git show --numstat`: this block's line count plus 113, that is the block copy's own lines and 49/0 `.agent/authored/f025-r4-d2.md`, 6/0 `.agent/authored/f025-r4-ledger.md`, 33/0 `.agent/authored/f025-r4-plan.md`, 25/0 `.agent/authored/f025-r4-q4.md`.
C1b RECORDS, one commit: the three appends and the plan rewrite. Subject `F025 R4 C1b: book round
    3, resolve R-1049 and R-1050, record D2 and operator question Q4`. Expected: 49/0 `.agent/decisions.md`, 6/0 `.agent/live_review.md`, 25/0 `.agent/operator_questions.md`, 11/13 `.agent/plan.md`.
C2 THE CATALOG AND THE CLI (P1, P3). C3 THE EFFECTS AND THE REGISTRIES (P2, P5). C4 THE DOOR (P4).
C5 THE DOCS (P6). C6 THE CLI TESTS (T1). C7 THE LIVE DOOR TESTS (T2). C8 THE MUTATION TOOL,
    `.agent/authored/f025-r4-mutations.py`. Order C2 and C3 as your imports require.
C9 THE HANDBACK, `.agent/handoff.md`. Subject `F025 R4 C9: rewrite handoff for round 4`. Then
    `git push origin feature/f025-pause-resume`.
Subjects for C2 to C8 are yours, each beginning `F025 R4 C<n>: `.

CONSTRAINTS
1. Never edit or retype a payload. Append by python, bytes to bytes.
2. Every commit under 500 insertions by `git show --numstat`. No `# noqa: BLE001` is added.
3. The round's tracked path set is: the `.agent/authored/f025-r4-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/operator_questions.md`, `.agent/plan.md`,
   `.agent/handoff.md`, `apps/cli/command_catalog.py`, `apps/cli/commands/job_pause_cmd.py`,
   `apps/cli/commands/__init__.py`, `packages/orchestration/pause_control.py`,
   `packages/orchestration/ui_server.py`, `packages/orchestration/event_names.py`,
   `apps/ui/src/api/humanizeCatalog.ts`, `docs/guides/exit-codes.md`,
   `tests/orchestration/import_reachability_allowlist.txt`, the two new test files, and any
   EXISTING test or generated list whose only edit adds the new ids, handler module, methods,
   imports or event names to a set it pins — each named in the handback with what it widened.
   Never weaken an assertion or delete a test. Do NOT touch `safe_points.py`, `pingpong_job.py`,
   `pingpong_loop.py`, `long_run_executor.py`, `packages/common/secure_fs.py`, `apps/ui/src/`
   beyond the humanize catalog, or `docs/roadmap/`.
4. A red gate: STOP, commit and push what is verified, write the handoff under AGENTS.md "If
   Blocked". Nothing is merged; no `gh pr create`; no force-push; no `git stash`.
5. Leave every existing worktree alone; the one G5 adds is removed as that step's last action.
6. DO NOT run the full suite (amend0917 rule 1).

DONE-WHEN — every gate executed, every reading reported with its real exit code. G1 to G5 run
before C9 is written.
G1 TRANSPORT: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f025-r4-*` payload copy byte-equal to its source by `git show <C1a>:<path>`
   (the block copy against `.remedy-wt/f025-r4/block.md`); at C1b the three appended files equal
   their `62e43ee8` bytes plus their payloads and `.agent/plan.md` equals plan.md; and
   `open_finding_ids` over the ledger at C1b — the reviewer's simulation read `['R-1008']`.
G2 THE CODE: `python3 -m ruff check` over every Python file C2 to C8 changed; `git diff --stat
   62e43ee8 <C8> -- packages/orchestration/safe_points.py packages/orchestration/pingpong_job.py
   packages/orchestration/pingpong_loop.py packages/orchestration/long_run_executor.py
   packages/common/secure_fs.py` empty; the count of `noqa: BLE001` marks the range adds under
   `packages`, `apps` and `scripts`, which must be 0; and `git diff --name-only <C1b> <C8>`, every
   path inside constraint 3.
G3 THE NEW TESTS, serially: `python3 -m pytest -q -p no:cacheprovider tests/cli/test_job_pause.py
   tests/ui_server/test_pause_door_live.py tests/ui_server/test_command_channel.py
   tests/ui_server/test_command_dispatch.py` — exit 0; report the summary line and the
   `--collect-only -q` count of each new file.
G4 THE NEIGHBOURS: `python3 .remedy-wt/f025-r4/run_sel.py /home/decodeux/Repos/remedy 8` in the
   primary checkout at C8 — round 3's selection plus `tests/cli`, `tests/ui_server` and
   `tests/docs` whole, with 8 xdist workers. At `62e43ee8` the reviewer read `6 failed, 8709 passed,
   9 skipped`: the six are `tests/cli/test_study_cmd.py` nodes that fail the same way in this
   combined run at `49624d5c` and all pass when that file runs alone, an ordering effect of the
   combined run and not this feature's. Report its output; re-run every failing node's FILE alone,
   serially, and report both readings; any failure outside `test_study_cmd.py` is this round's.
   Then `python3 -m apps.cli.main integrity check --json`: six `pass`, `fail_count` 0.
G5 THE RED PROOFS: your tool takes a worktree path, edits the named production file INSIDE that
   worktree (asserting each FROM occurs exactly once), purges `__pycache__`, runs `python3 -B -m
   pytest -q -p no:cacheprovider tests/cli/test_job_pause.py tests/ui_server/test_pause_door_live.py`
   from the worktree root with the primary checkout's `apps/ui/node_modules` symlinked into the
   worktree if a node needs it (removing the link afterwards), restores, and prints per mutation its
   label, exit code, failed count and failing node ids, with an unmutated control first and last,
   `restored byte-identical: True` per file, and a final `ALL MUTATIONS CAUGHT AND RESTORED
   CLEANLY: <bool>`. Mutations:
    m1 the door's pause ignores `args.task` and always pauses the job;
    m2 the terminal-state refusal is removed from `pause_job_command`;
    m3 a task id the plan does not hold is accepted;
    m4 `unpause_job_command` on a parked job answers `not_paused`;
    m5 `task_paused` is written on every call, not only when the entry is created;
    m6 `task_resumed` is never written;
    m7 the door answers a `refused` outcome 500 `rejected_effect` instead of 409 `rejected_state`;
    m8 the CLI exits 0 on a `refused` outcome.
   `git worktree add --detach .remedy-wt/f025-r4-mut <C8>`, run
   `python3 -B .agent/authored/f025-r4-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f025-r4-mut`,
   report the whole output. EVERY mutation must be red; one that stays green is reported green, the
   catching test is added in a further commit before C9, and the tool re-run. Then
   `git worktree remove --force .remedy-wt/f025-r4-mut`, `git worktree prune`, `git worktree list`.
G6 AFTER C9 AND THE PUSH, in your final reply only: `git status --porcelain` empty, the local tip
   equal to `origin/feature/f025-pause-resume`, `git log --oneline -n 14`, the push's real outcome,
   and `gh pr list --state open --json number` EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the `git show --numstat` counts you measured (compared with
C1a's and C1b's expectations above), every gate's real output, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations — including
every file constraint 3 led you to widen — and the next action. Session section: SESSION 1 of
feature F025, round 4, plus one sentence on how much context you had left. `## Next`: Phase 1 rule
1, the review of round 4, then T003 — the paused states, the banner, the NowCard line, the browser's
pause and resume, and the end-to-end against an unpaused control run. State the open-findings count
as the script reads it at C1b, and "Operator questions open: <the count of `### Q` headings you
read in the file at C1b>".

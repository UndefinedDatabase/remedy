STEP F025 R3 — REPAIR R-1049 AND R-1050, THEN THE PAUSE IN THE CYCLE EXECUTOR `run_cycles`

GOAL
Round 2 FAILED on two findings its payload `ledger.md` registers (read both, whole: their FIX
clauses are this round's first spec). Persist them first, repair them, then bring DECISION F025
D1's pause to the cycle executor, `run_cycles` in `packages/orchestration/long_run_executor.py`
(reached by `remedy job resume` with more than one cycle and by the mission loop), sharing the
linear runner's park record and events, with its tests in a NEW FILE at
`tests/orchestration/test_pause_resume_cycles.py` and a mutation tool proving them.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, write the handback. You never
issue a verdict, never merge, and never write a `Done:` line. THE PRODUCTION CHANGE IS SPECIFIED,
NOT SLICED: you write the code and tests against the findings' FIX clauses and E1 to E7. Read
DECISION F025 D1 (search `.agent/decisions.md` for its heading), `pause_control.py`, round 2's
`_park_job`, `_lift_job_pause` and the pause events in `pingpong_job.py`, and `run_cycles`,
`ready_tasks`, `CycleRecord`, `_apply_terminal` and the helpers of
`tests/orchestration/test_long_run_executor.py` before writing.

THE DIRECTORIES
  `.remedy-wt/f025-r3/`          READ-ONLY. This block, its payloads and the reviewer's scripts.
  `.remedy-wt/f025-r3-worker/`   YOURS for logs and scripts; create it if absent. Both gitignored.

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
   `git log --oneline -1` must read `312b9512`.
3. Measure this block's line count and sha256 (`.remedy-wt/f025-r3/block.md`) and compare both
   with your delegation message's readings; stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f025-r3/`, lines = newline count; verify each BEFORE use:
| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.md | 6 | 5390 | 05c8f31ef429dee4c5d6d9ad0ff83ea22c1e797eadad9c6c003d6d2256e8303b |
| plan.md | 35 | 1415 | 6c812aff48496b1a336e75d730db1ecd057b979ba34d4e05b936df90e39360af |
| slip.txt | 1 | 329 | 2cf3c7e78b4d4213a359200b63e5833f530cf192d6854c71eebbe69846018f29 |
`ledger.md` is appended to `.agent/live_review.md` (it starts with its own blank line), `slip.txt`
is appended to `.agent/prose_slips.md`, and `plan.md` REWRITES `.agent/plan.md`.

THE SPECIFICATION FOR THE EXECUTOR
E1 ONE PARK. The pause record, the `job_paused` event with its exactly-once check and R-1050's
   failure handling, and the lift with its `job_resumed` event are the linear runner's. Factor them
   out of `_park_job` and `_lift_job_pause` into shared functions in `pingpong_job.py` that take the
   persist step as an argument, so `run_cycles` persists through its own `save` seam and both
   runners write one record shape through one writer. Name the shared functions in the handback.
E2 THE JOB PAUSE. A new terminal `TERMINAL_PAUSED_BY_OPERATOR = "paused_by_operator"` maps to
   `JOB_PAUSED` in `TERMINAL_JOB_STATUS` and `RunState.PAUSED` in `TERMINAL_RUN_STATE`, and is NOT
   in `REPORTED_TERMINALS`, because a paused run is not over. At the cycle safe point, only when
   `_should_stop` does not fire, `pause_control.pause_requested` is read; a pending request ends the
   loop with that terminal, `stop_reason` `operator_pause: <reason>`, and the E1 park with scope
   `job`, whose request is settled `served` only after the job is saved. The job pause is ALSO read
   before each task pick inside a cycle: a pending one ends the batch (a task step already running
   finishes first) and the next safe point parks.
E3 THE TASK MASK. `ready_tasks` gains `paused_ids: Collection[str] = ()`, withheld exactly like
   the blocked and awaiting seeds, with their transitive dependents. `run_cycles` reads
   `pause_control.paused_tasks` at every batch boundary and before every task pick, as it re-derives
   the awaiting ids. `CycleRecord` gains `paused_task_ids` and `paused_downstream_task_ids`, in plan
   order, in its JSON. When the batch is empty, the job is not green, no task awaits a decision, and
   the paused ids withhold at least one pending task, the loop ends with `paused_by_operator`,
   `stop_reason` `paused_tasks=<ids joined by commas>`, and the E1 park with scope `task` naming the
   paused and withheld ids. When a task awaits a decision, the existing awaiting terminal stands and
   the record still names the paused ids.
E4 THE RELAUNCH. `run_cycles` on a job whose state is `paused` with a non-empty `pause`: before the
   first cycle, if a job pause is pending or no pending task is ready because the mask withholds it,
   the loop ends `paused_by_operator` with zero task steps and no event; otherwise the E1 lift writes
   one `job_resumed` and the run continues.
E5 A `PauseControlError` at any of these reads ends the loop `blocked` with `stop_reason`
   `pause_control_error: <detail>` and no further task step.
E6 THE CONSUMERS. Find every reader of the executor's terminal statuses (`TERMINAL_JOB_STATUS`,
   `REPORTED_TERMINALS`, `render_cycle_summary_line`, the `remedy job resume` output in
   `apps/cli/commands/job.py`, `packages/orchestration/run_report.py`, the mission loop) and make
   each treat `paused_by_operator` as it treats `stopped_by_operator`, except that no final report
   is written; name every file you changed and why.
E7 SIZE. Every commit under 500 inserted lines; split a commit and say so rather than exceed it.

THE TESTS — `tests/orchestration/test_pause_resume_cycles.py`, reusing
`tests/orchestration/test_long_run_executor.py`'s helpers (import them), at least one test each:
 c1 a job pause pending at the first safe point ends `paused_by_operator` with zero task steps; the
    state is `paused`, `pause.scope` is `job`, one `job_paused`, the request archived `served`;
 c2 a job pause requested during the first task step of a two-task batch lets that step finish and
    never picks the second task; the next safe point parks;
 c3 on the diamond A -> (B, C) -> D with B paused: A and C run, D is withheld, the cycle record
    names B as paused and D as paused-downstream, and the loop ends `paused_by_operator` with
    `paused_tasks=` naming B;
 c4 after `release_task_pause` of B, a relaunch writes one `job_resumed`, runs B then D, and ends
    `all_green`;
 c5 a stop and a job pause both pending end `stopped_by_operator`, the pause archived
    `superseded_by_stop`, and no `job_paused`;
 c6 a branch awaiting a decision beside a paused branch ends with the awaiting terminal and a
    record naming both;
 c7 a corrupt `paused_tasks` entry ends `blocked` with `pause_control_error` and zero task steps;
 c8 a parked job whose persisted `first_running_at` is a day back, with persisted budget actuals
    and a one-hour deadline, ends `deadline_reached` at its relaunch with zero task steps;
 c9 a relaunch while B is still paused ends `paused_by_operator` with zero steps and no new event;
 c10 `paused_by_operator` writes no final report.
And for R-1050, in `tests/orchestration/test_pause_resume.py`: a `job_paused` write that raises
leaves `event_error` in the persisted pause record and the job-scope request pending, and the next
run writes exactly one `job_paused`, settles the request and clears `event_error`; a `job_resumed`
write that raises leaves `metadata["pause_event_error"]` persisted and the run completes. And for
R-1049: a settle that raises `PauseControlError` inside a served stop still ends the job `stopped`.

BUNDLE — commits in this order; split any that would reach 500 insertions and say so.
C1 BOOKKEEPING, one commit, the findings persisted FIRST: `.agent/authored/f025-r3-block.md` :=
   this block, the payloads copied as `.agent/authored/f025-r3-ledger.md`, `-plan.md`,
   `-slip.txt`; then the two appends and the plan rewrite. Subject `F025 R3 C1: book round 2's
   FAIL, register R-1049 and R-1050, copy round 3 block and payloads`. Expected by
   `git show --numstat`: this block's line count plus 60, that is the block copy's own lines and 6/0 `.agent/authored/f025-r3-ledger.md`, 35/0 `.agent/authored/f025-r3-plan.md`, 1/0 `.agent/authored/f025-r3-slip.txt`, 6/0 `.agent/live_review.md`, 11/12 `.agent/plan.md`, 1/0 `.agent/prose_slips.md`.
C2 R-1049's FIX. Subject `F025 R3 C2: catch only the pause errors a stop's settle raises (R-1049)`.
C3 R-1050's FIX with its tests and R-1049's test. Subject `F025 R3 C3: record a pause event that
   fails and keep its request pending (R-1050)`.
C4 THE EXECUTOR (E1 to E6). Subject `F025 R3 C4: pause the cycle executor at its safe points and
   in its ready set`.
C5 THE EXECUTOR'S TESTS. Subject `F025 R3 C5: test the pause on the cycle executor`.
C6 THE MUTATION TOOL, `.agent/authored/f025-r3-mutations.py`. Subject `F025 R3 C6: add the
   mutation tool for round 3`.
C7 THE HANDBACK, `.agent/handoff.md`. Subject `F025 R3 C7: rewrite handoff for round 3`. Then
   `git push origin feature/f025-pause-resume`.

CONSTRAINTS
1. Never edit or retype a payload. Append by python, bytes to bytes.
2. Every commit under 500 insertions by `git show --numstat`. No `# noqa: BLE001` is added.
3. The round's tracked path set is: the `.agent/authored/f025-r3-*` copies and tool,
   `.agent/live_review.md`, `.agent/prose_slips.md`, `.agent/plan.md`, `.agent/handoff.md`,
   `packages/orchestration/pingpong_job.py`, `packages/orchestration/long_run_executor.py`,
   `packages/orchestration/pause_control.py` (small helpers only), the E6 consumers you name,
   `tests/orchestration/test_pause_resume.py`, `tests/orchestration/test_pause_resume_cycles.py`,
   and any EXISTING test whose only edit adds the new terminal or record fields to a set it pins —
   each named in the handback with the assertion it widened. Never weaken an assertion or delete a
   test. Do NOT touch `packages/orchestration/safe_points.py`, `pingpong_loop.py`,
   `checkpoints.py`, `escalation.py`, `dag_schedule.py`, `packages/common/secure_fs.py`, `docs/`,
   `README.md` or `.agent/decisions.md`.
4. A red gate: STOP, commit and push what is verified, write the handoff under AGENTS.md "If
   Blocked". Nothing is merged; no `gh pr create`; no force-push; no `git stash`.
5. Leave every existing worktree alone; the one G5 adds is removed as that step's last action.
6. DO NOT run the full suite (amend0917 rule 1).

DONE-WHEN — every gate executed, every reading reported with its real exit code. G1 to G5 run
before C7 is written.
G1 TRANSPORT: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f025-r3-*` payload copy byte-equal to its source by `git show <C1>:<path>` (the
   block copy against `.remedy-wt/f025-r3/block.md`); at C1 `.agent/live_review.md` equals its
   `312b9512` bytes plus ledger.md, `.agent/prose_slips.md` its `312b9512` bytes plus slip.txt, and
   `.agent/plan.md` equals plan.md; and `open_finding_ids` over the ledger at C1 — the reviewer's
   simulation read `['R-1008', 'R-1049', 'R-1050']`.
G2 THE CODE: `python3 -m ruff check` over every Python file C2 to C6 changed; `git diff --stat
   312b9512 <C6> -- packages/orchestration/safe_points.py packages/orchestration/pingpong_loop.py
   packages/orchestration/checkpoints.py packages/orchestration/escalation.py
   packages/orchestration/dag_schedule.py packages/common/secure_fs.py` empty; the count of
   `noqa: BLE001` marks added by `git diff 312b9512 <C6> -- packages apps scripts`, which must be
   0; and `git diff --name-only <C1> <C6>`, every path inside constraint 3.
G3 THE NEW TESTS, serially: `python3 -m pytest -q -p no:cacheprovider
   tests/orchestration/test_pause_resume_cycles.py tests/orchestration/test_pause_resume.py
   tests/orchestration/test_pause_control.py tests/test_ble001_ratchet.py` — exit 0; report the
   summary line and the `--collect-only -q` count per file.
G4 THE NEIGHBOURS: `python3 .remedy-wt/f025-r3/run_sel.py /home/decodeux/Repos/remedy 8` in the
   primary checkout at C6. It runs the files of `.remedy-wt/f025-r3/selection.txt` — round 2's
   selection, every root guard `tests/test_*.py`, `tests/regression`, and every test file naming
   the executor — with 8 xdist workers. At `312b9512` the reviewer read `1 failed, 6105 passed,
   9 skipped`, the failure being `tests/test_ble001_ratchet.py::test_the_count_of_excused_handlers_never_rises`
   (R-1049); at C6 it must read 0 failed. Report its output; a node that fails is re-run alone,
   serially, and both readings reported. Then `python3 -m apps.cli.main integrity check --json`:
   six `pass`, `fail_count` 0.
G5 THE RED PROOFS: your tool takes a worktree path, edits the named production file INSIDE that
   worktree (asserting each FROM occurs exactly once), purges `__pycache__`, runs `python3 -B -m
   pytest -q -p no:cacheprovider tests/orchestration/test_pause_resume_cycles.py
   tests/orchestration/test_pause_resume.py` from the worktree root, restores, and prints per
   mutation its label, exit code, failed count and failing node ids, with an unmutated control
   first and last, `restored byte-identical: True` per file, and a final line
   `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Mutations:
    m1 the executor reads the job pause before `_should_stop`;
    m2 `ready_tasks` ignores `paused_ids`;
    m3 `ready_tasks` withholds the paused seeds but not their dependents;
    m4 `paused_by_operator` is added to `REPORTED_TERMINALS`;
    m5 the relaunch runs while the mask still withholds every pending task;
    m6 the relaunch never lifts the pause;
    m7 the job pause is not read before a task pick inside a cycle;
    m8 a `PauseControlError` in the executor is swallowed and the task step runs;
    m9 the park settles a job-scope request although the `job_paused` write failed;
    m10 the park drops `event_error` instead of recording it;
    m11 a settle raising `PauseControlError` inside a served stop propagates out of the stop.
   `git worktree add --detach .remedy-wt/f025-r3-mut <C6>`, run
   `python3 -B .agent/authored/f025-r3-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f025-r3-mut`,
   report the whole output. EVERY mutation must be red; one that stays green is reported green, the
   catching test is added in a further commit before C7, and the tool re-run. Then
   `git worktree remove --force .remedy-wt/f025-r3-mut`, `git worktree prune`, `git worktree list`.
G6 AFTER C7 AND THE PUSH, in your final reply only: `git status --porcelain` empty, the local tip
   equal to `origin/feature/f025-pause-resume`, `git log --oneline -n 12`, the push's real outcome,
   and `gh pr list --state open --json number` EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the `git show --numstat` counts you measured (compared with
C1's expectation above), every gate's real output, the authored-text proofs, the item-status table
AGENTS.md requires (one row per commit and per gate), the deviations — including every file E6 or
constraint 3 led you to change — and the next action. Session section: SESSION 1 of feature F025,
round 3, plus one sentence on how much context you had left. `## Next`: Phase 1 rule 1, the review
of round 3, then T002 — the channel commands with their audit, the CLI verbs and live fake-job
tests of both scopes. State the open-findings count as the script reads it at C1, and the
operator-questions count, 3.

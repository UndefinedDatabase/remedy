STEP F025 R2 — T001's SECOND HALF IN THE LINEAR RUNNER: the pause at `run_job`'s safe points, the park, the relaunch that resumes, a stop beating a pause, and the deadline through a pause

GOAL
Round 1 landed `packages/orchestration/pause_control.py` (PASS, booked by C1 below). Wire it into
the linear runner, `run_job` in `packages/orchestration/pingpong_job.py`, so that every row of
DECISION F025 D1's semantics table (clause 5) holds for `remedy job run`, `remedy do` and the UI's
live fake job, each row proved by a test in a NEW FILE at `tests/orchestration/test_pause_resume.py`
and each rule proved to bite by a mutation. The cycle executor is the NEXT round; do not touch it.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you write the code
and its tests against S1 to S8. Only the `.agent/` records travel as payloads. Read DECISION F025 D1
in `.agent/decisions.md` (search its heading) and `pause_control.py` before you start.

THE DIRECTORIES
  `.remedy-wt/f025-r2/`          READ-ONLY. This block, its payloads and the reviewer's scripts.
  `.remedy-wt/f025-r2-worker/`   YOURS for logs and scripts; create it if absent. Both gitignored.

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
   `git log --oneline -1` must read `e9824ebe`.
3. Measure this block's line count and sha256 (`.remedy-wt/f025-r2/block.md`) and compare both
   with your delegation message's readings; stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f025-r2/`, lines = newline count; verify each BEFORE use:
| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.md | 2 | 2839 | 85e94e9efa2834cb90978ed1de615c1f5a3282996fd45304ae275fe70339a418 |
| plan.md | 36 | 1427 | a586b8a56001cb877473ec1b1953ba9eae70d7a4847fed21f1820405368b01f8 |
| slip.txt | 1 | 273 | 2ba22d9e5c9a13762d9332189ffb3ee5921ceb0b94e6530d4a276e56ab6d2185 |
`ledger.md` is appended to `.agent/live_review.md` (it starts with its own blank line), `slip.txt`
is appended to `.agent/prose_slips.md`, and `plan.md` REWRITES `.agent/plan.md`.

THE SPECIFICATION
S1 THE RECORD. `JobPlan` gains `pause: dict` (empty when no operator pause holds the job), wired
   explicitly through `_export_job` and `_import_job` as the key `"pause"`, a missing key loading as
   `{}`. When the job leaves `paused` for any other state the record is emptied. The task cap's
   `paused` (`max_tasks`) never writes it.
S2 THE CHECK. `run_job`'s `_stop_check` keeps every stop it serves today and their order — the
   operator stop, the reactive budget, the predictive budget — and a stop ALWAYS wins. Only when none
   fires does it read, through `pause_control`: the job pause (`pause_requested`), then the task mask.
   At the PRE-TASK safe point the mask is `withheld_task_ids` over the plan's order and its pending
   tasks (linear, no `depends_on`); if the task about to be dispatched is withheld the job parks with
   scope `task`. At the IN-TASK safe point (`_run_stop_check`, handed to `run_pingpong`) a paused
   in-flight task halts before its next provider call and the job parks with scope `task`: the
   in-flight task counts as pending for this reading, because it goes back to pending. The signal
   handed to `run_pingpong` needs `request_id`, `reason`, `source`, `requested_at` (it reads them by
   attribute), and its reason reads `operator_pause: <reason>`. `pingpong_loop.py` is NOT edited.
   A `PauseControlError` at any safe point dispatches nothing: the job BLOCKS with
   `error = "pause_control_error: <detail>"`.
S3 THE PARK, one function, in this order: (1) the in-flight task, if any and not yet applied, goes
   back to `pending` with `task_attempt_state = "active"`, exactly as `_stop_job` does; (2) the state
   becomes `JOB_PAUSED` and `pause` records `scope` (`job` or `task`), `request_id`, `reason`,
   `source`, `requested_at`, `paused_at`, `paused_task_ids` and `withheld_task_ids`; (3) the budget
   actuals and the job are persisted; (4) one `job_paused` event per request id — check the ledger
   first, as `_job_stopped_event_exists` does — written with an INLINE string literal through the
   same writer `job_stopped` uses, outcome `paused`, carrying scope, request id, reason, source, the
   withheld task ids and the pending count; (5) for scope `job` only, `settle_pause(..., "served")`.
   Nothing of the stop runs: no stop archive, post-mortem, `job_stopped`, stopped manifest or stop
   field. A failure at (5) leaves the request pending and the job parked; the next run re-parks on
   the same request without a second event and settles it.
S4 STOP BEATS PAUSE. When a stop is served and a job pause is pending, the stop finishes first and
   the pause is then settled `superseded_by_stop`; no `job_paused` is written. A stop requested on a
   parked job is served by the relaunch's existing pre-work check, so the job ends `stopped` with zero
   provider calls, never resumed.
S5 THE RELAUNCH IS THE RESUME. `run_job` on a job whose state is `paused` with a non-empty `pause`
   runs every gate a run already runs, unchanged. At the pre-work point (beside the existing pre-work
   stop check) it then decides: if a job pause is pending, or the first pending task is still
   withheld, the job STAYS parked — no event, no state change, no provider call — and the run
   returns; otherwise it lifts the pause: one `job_resumed` event per lifted request id (inline
   literal, same writer, outcome `resumed`, carrying the lifted record and `resumed_at`), `pause`
   emptied, and the run continues from the first pending task. `first_running_at` is never reset by a
   park or a relaunch, so a deadline that passed while parked is spent.
S6 THE WORDS. The job summary that prints `Paused: N tasks pending` adds, for a job whose `pause` is
   non-empty, one line `Paused by <source>: <reason>`, and for scope `task` one line naming the
   withheld tasks. `_suggest_next_command` is unchanged (`remedy job run <id>`).
S7 THE REGISTRIES. `job_paused` and `job_resumed` join `EVENT_NAMES` in
   `packages/orchestration/event_names.py` in the commit that writes them, and join
   `apps/ui/src/api/humanizeCatalog.ts` as `"job_paused": "The job paused."` and
   `"job_resumed": "The job resumed."`, one line each in that file's entry format (its guard
   `tests/ui_contracts/test_humanize_catalog.py` requires the catalog to equal the emitted set).
   `packages.orchestration.pause_control` joins `tests/orchestration/import_reachability_allowlist.txt`
   in the commit that first imports it from the runner.
S8 SIZE. Every commit under 500 inserted lines; split a commit and say so rather than exceed it.

THE TESTS — `tests/orchestration/test_pause_resume.py`, reusing the fake providers and fixtures of
`tests/orchestration/test_job_stop_integration.py` (import them), one test per row at least:
 1 a job pause requested DURING build call N lets call N finish and starts no call N+1; the task is
   back to `pending`; the state is `paused`; `pause.scope` is `job`; exactly one `job_paused`; the
   request is archived `served` and no `pause.json` remains;
 2 a job pause requested before the run parks it with zero provider calls;
 3 the relaunch of 1 writes exactly one `job_resumed`, completes every task, and ends with the same
   task statuses as an unpaused control run of the same plan;
 4 a task pause of the second of three tasks, before the run: the first runs and applies, the job
   parks with scope `task` and `withheld_task_ids` naming the second and third, and no provider call
   is made for them;
 5 a task pause of the IN-FLIGHT task halts it before its next provider call and parks; a relaunch
   while it is still paused stays parked with no event and zero calls; after `release_task_pause` a
   relaunch resumes and completes;
 6 a stop and a job pause both pending: the job ends `stopped`, the pause is archived
   `superseded_by_stop`, and no `job_paused` exists; and a stop requested on a parked job ends it
   `stopped` at the relaunch with zero provider calls;
 7 a parked job whose `first_running_at` is moved a day back, relaunched with a wall-clock budget of
   an hour, makes zero provider calls and ends as a budget stop whose reason names the wall-clock
   limit; `first_running_at` equals the moved value afterwards;
 8 a failure of the park's settle leaves the job `paused` and the request pending; the next run
   re-parks without a second `job_paused` and settles the request;
 9 an unreadable `paused_tasks` entry blocks the job with `pause_control_error` and dispatches
   nothing;
 10 the `max_tasks` pause leaves `pause` empty, and the summary lines of S6 for both scopes;
 11 a relaunch whose plan approval no longer holds is refused exactly as an unpaused run of the same
   job is, and the pause record stays (find the gate `run_job` applies to an approved plan; if no
   such gate reaches a parked job, report that instead of inventing one).

BUNDLE — commits in this order: C1, C2, C3 (or C3a, C3b), C4 (or C4a, C4b), C5, C6.
C1 BOOKKEEPING, one commit: `.agent/authored/f025-r2-block.md` := this block, and the three payloads
   copied as `.agent/authored/f025-r2-ledger.md`, `-plan.md`, `-slip.txt`; then the two appends and
   the plan rewrite. Subject `F025 R2 C1: book round 1, copy round 2 block and payloads`. Expected by
   `git show --numstat`: this block's line count plus 49, that is the block copy's own lines and 2/0 `.agent/authored/f025-r2-ledger.md`, 36/0 `.agent/authored/f025-r2-plan.md`, 1/0 `.agent/authored/f025-r2-slip.txt`, 2/0 `.agent/live_review.md`, 7/7 `.agent/plan.md`, 1/0 `.agent/prose_slips.md`.
C2 THE RECORD AND THE WORDS (S1, S6). Subject `F025 R2 C2: record an operator pause on the job and
   say who paused it`.
C3 THE RUNNER (S2 to S5, S7). Subject `F025 R2 C3: pause the linear runner at its safe points,
   park, resume on relaunch, and let a stop win`.
C4 THE TESTS. Subject `F025 R2 C4: test every row of the pause semantics on the linear runner`.
C5 THE MUTATION TOOL, `.agent/authored/f025-r2-mutations.py`. Subject `F025 R2 C5: add the mutation
   tool for the linear runner's pause`.
C6 THE HANDBACK, `.agent/handoff.md`. Subject `F025 R2 C6: rewrite handoff for round 2`. Then
   `git push origin feature/f025-pause-resume`.

CONSTRAINTS
1. Never edit or retype a payload. Append by python, bytes to bytes.
2. Every commit under 500 insertions by `git show --numstat`.
3. The round's tracked path set is: the `.agent/authored/f025-r2-*` copies and tool,
   `.agent/live_review.md`, `.agent/prose_slips.md`, `.agent/plan.md`, `.agent/handoff.md`,
   `packages/orchestration/pingpong_job.py`, `packages/orchestration/pause_control.py` (small helpers
   only, named in the handback), `packages/orchestration/event_names.py`,
   `apps/ui/src/api/humanizeCatalog.ts`, `tests/orchestration/import_reachability_allowlist.txt`,
   `tests/orchestration/test_pause_resume.py`, and any EXISTING test whose only edit adds the new
   record key or event names to a set it pins — each such file named in the handback with the
   assertion it widened. Nothing else. Never weaken an assertion or delete a test.
   Do NOT touch `packages/orchestration/safe_points.py`, `packages/orchestration/pingpong_loop.py`,
   `packages/orchestration/long_run_executor.py`, `packages/orchestration/checkpoints.py`,
   `packages/common/secure_fs.py`, `docs/`, `README.md` or `.agent/decisions.md`.
4. A red gate: STOP, commit and push what is verified, write the handoff under AGENTS.md "If
   Blocked". Nothing is merged; no `gh pr create`; no force-push; no `git stash`; no branch changes.
5. Leave every existing worktree (the reviewer's `f025-r1-dry`, `f024-r9-sim` and the older
   `f015-*`, `f020-*`, `f023-*`, `f024-*`, `f284-*` and `job-*` ones) alone. The worktree G5 adds is
   removed as that step's last action.
6. DO NOT run the full suite (amend0917 rule 1).

DONE-WHEN — every gate executed, every reading reported with its real exit code. G1 to G5 run
before C6 is written.
G1 TRANSPORT: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f025-r2-*` payload copy byte-equal to its source by `git show <C1>:<path>` (the
   block copy against `.remedy-wt/f025-r2/block.md`); `.agent/live_review.md` at C1 equals its
   `e9824ebe` bytes plus ledger.md, `.agent/prose_slips.md` its `e9824ebe` bytes plus slip.txt,
   `.agent/plan.md` equals plan.md; and `open_finding_ids` over the ledger at C1 — the reviewer read
   `['R-1008']`.
G2 THE CODE: `python3 -m ruff check` over every Python file C2 to C5 changed; `git diff --stat
   e9824ebe <C5> -- packages/orchestration/safe_points.py packages/orchestration/pingpong_loop.py
   packages/orchestration/long_run_executor.py packages/common/secure_fs.py` empty; and
   `git diff --name-only <C1> <C5>` listed, every path inside constraint 3.
G3 THE NEW TESTS, serially: `python3 -m pytest -q -p no:cacheprovider
   tests/orchestration/test_pause_resume.py tests/orchestration/test_pause_control.py` — exit 0;
   report the summary line and `--collect-only -q` counts per file.
G4 THE NEIGHBOURS: `python3 .remedy-wt/f025-r2/run_sel.py /home/decodeux/Repos/remedy 8` in the
   primary checkout at C5. It runs the 76 files of `.remedy-wt/f025-r2/selection.txt` — every test
   file that calls `run_job`, plus the stop, budget, event-name, humanize, reachability, job-record,
   job CLI, toolchain and golden-path guards — with 8 xdist workers. The reviewer read `exit 0` and
   `2445 passed` at `e9824ebe`. Report its output; any node that fails is re-run alone, serially, and
   both readings reported. Then `python3 -m apps.cli.main integrity check --json`: six `pass`,
   `fail_count` 0.
G5 THE RED PROOFS: your tool takes a worktree path, edits `pingpong_job.py` (and
   `pause_control.py` where a mutation lives there) INSIDE that worktree, asserting each FROM occurs
   exactly once, purges `__pycache__`, runs `python3 -B -m pytest -q -p no:cacheprovider
   tests/orchestration/test_pause_resume.py` from the worktree root, restores, and prints per
   mutation its label, exit code, failed count and failing node ids, with an unmutated control first
   and last, `restored byte-identical: True` per file, and a final line
   `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Mutations:
    m1 the job pause is read BEFORE the operator stop;
    m2 the park settles the request BEFORE it persists the job;
    m3 the park writes `job_paused` without checking the ledger for that request id;
    m4 the park leaves the in-flight task `running`;
    m5 the relaunch never lifts the pause;
    m6 the relaunch dispatches a task that is still withheld;
    m7 the pre-task safe point ignores the task mask;
    m8 the in-task safe point ignores a pause of the in-flight task;
    m9 the relaunch re-stamps `first_running_at`;
    m10 a `PauseControlError` at a safe point is swallowed and the task dispatched;
    m11 a served stop leaves a pending job pause unsettled.
   `git worktree add --detach .remedy-wt/f025-r2-mut <C5>`, run
   `python3 -B .agent/authored/f025-r2-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f025-r2-mut`,
   report the whole output. EVERY mutation must be red; one that stays green is reported green, the
   catching test is added in a further commit before C6, and the tool re-run. Then
   `git worktree remove --force .remedy-wt/f025-r2-mut`, `git worktree prune`, `git worktree list`.
G6 AFTER C6 AND THE PUSH, in your final reply only: `git status --porcelain` empty, the local tip
   equal to `origin/feature/f025-pause-resume`, `git log --oneline -n 10`, the push's real outcome,
   and `gh pr list --state open --json number` EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the `git show --numstat` counts you measured (compared with
C1's expectation above), every gate's real output, the authored-text proofs, the item-status table
AGENTS.md requires (one row per commit and per gate), the deviations — including every existing test
file you widened under constraint 3 — and the next action. Session section: SESSION 1 of feature
F025, round 2, plus one sentence on how much context you had left. `## Next`: Phase 1 rule 1, the
review of round 2, then the same pause in the cycle executor `run_cycles`. State the open-findings
count, 1, and the operator-questions count, 3.

STEP F025 R8 — BOOK ROUND 7'S FAIL, THEN REPAIR R-1056: A PARK RECORDS THE EPISODE IT ENDS, SO A RELAUNCHED JOB WRITES ITS RUN MANIFEST

GOAL
Round 7 FAILED on one finding; the payload `ledger.md` books that verdict, registers R-1056 and
resolves R-1053 and R-1054 — read it whole, R-1056's FIX clause is this round's spec. Persist it,
then land DECISION F025 D6 — the payload `d6.md`, read it whole before writing code: the run
manifest's new status `paused`, written by `run_job`'s parks, and the end-to-end test that then
compares the manifest's error too.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, write the handback. You never
issue a verdict, never merge, and never write a `Done:` line. THE PRODUCTION CHANGE IS SPECIFIED,
NOT SLICED: you write the code and tests against M1 to M4. Read first: in
`packages/orchestration/run_manifest.py`, `_VALID_STATUS`, `_LIFECYCLE_MATRIX` with the comment
above it, `build_run_manifest`, the call-expectation builder around `EXPECT_PRIOR_EPISODE`, and the
validator's `stop_request_id` rule; in `packages/orchestration/pingpong_job.py`,
`_write_run_manifest_record`, `_park_job`, `_stop_job`, `park_job_pause`, the pre-work stop branch
of `run_job` that captures the snapshot under `_PHASE_PRE_WORK_STOP`, and the task cap's
`JOB_PAUSED` beside the completion's manifest write; `tests/orchestration/test_pause_resume.py`,
`tests/orchestration/test_run_manifest_prework_resume.py`,
`tests/orchestration/test_run_manifest_reference_coverage.py`; and
`tests/ui_server/test_pause_e2e_live.py` with `.agent/authored/f025-r7-mutations.py`, whose live
route you reuse.

THE DIRECTORIES
  `.remedy-wt/f025-r8/`          READ-ONLY. This block, its payloads and the reviewer's scripts.
  `.remedy-wt/f025-r8-worker/`   YOURS for logs and scripts; create it if absent. Both gitignored.

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
   `git log --oneline -1` must read `3f36bd81`.
3. Measure this block's line count and sha256 (`.remedy-wt/f025-r8/block.md`) and compare both
   with your delegation message's readings; stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f025-r8/`, lines = newline count; verify each BEFORE use:
| file | lines | bytes | sha256 |
|---|---|---|---|
| d6.md | 42 | 3553 | e13bf1650d7984ace350cf6a0f011bc0b1980db6e44849e3ac32a50d0b345105 |
| ledger.md | 8 | 6383 | 7795684e9664648d965784c736e125e9f50384d12285b6ca7b5d7d3622a83fec |
| plan.md | 29 | 953 | c957d58d7f273b049f2d855d5813db791ccce861a09ee0e92321ab042a6a37c8 |
`ledger.md` is appended to `.agent/live_review.md` and `d6.md` to `.agent/decisions.md` (each
starts with its own blank line); `plan.md` REWRITES `.agent/plan.md`.

THE SPECIFICATION, DECISION F025 D6
M1 THE STATUS: `paused` joins `_VALID_STATUS`; `_LIFECYCLE_MATRIX` gains a `paused` row for each
   phase `stopped` has a row for, each equal to that `stopped` row except `stop_request` False; the
   comment above the matrix is corrected to say a park records its episode as `paused`. The rule
   that only a stopped manifest carries a `stop_request_id` is unchanged. Every other place in
   `run_manifest.py` that branches on `stopped` is read and given `paused` where the branch is about
   an episode that ended before completion, and left alone where it is about the stop request.
M2 THE PARKS: `_park_job` writes the episode's manifest with status `paused` through
   `_write_run_manifest_record`, after it returns the interrupted task to `pending` and before it
   calls `park_job_pause`, first capturing the episode snapshot when it is not yet bound, as the
   pre-work stop branch does; the task cap's pause writes `paused` where the completion writes
   `completed`. A failed write is kept in `run_manifest_error` and the park proceeds.
   `park_job_pause`, `long_run_executor.py` and `safe_points.py` are unchanged.
M3 THE READERS: grep `packages/`, `apps/`, `scripts/` and `docs/` for any closed set of manifest
   statuses (`"completed", "stopped"` and their kin); widen each that describes manifest statuses,
   and name each one you read and left alone, with why, in the handback.
M4 THE END-TO-END: `run_manifest.error` leaves `E4_REMOVED_FIELDS` in
   `tests/ui_server/test_pause_e2e_live.py`, and both scopes additionally assert that the relaunched
   job's `run_manifest_error` is empty and that its episode list names two episodes, the first
   with status `paused` and the second `completed`.

THE TESTS
T1 NEW `tests/orchestration/test_pause_manifest.py`, in-process, reusing the fixtures of
   `tests/orchestration/test_pause_resume.py` by import: a job-scope park mid-build, a task-scope
   park, a pause requested before any work, and a task-cap pause — each leaves a `paused` episode
   manifest and an empty `run_manifest_error`, and each relaunch completes with a `completed`
   manifest over both episodes and an empty error; plus a `paused` manifest given a
   `stop_request_id` is refused by the validator.
T2 Any existing test whose only edit widens a status set it pins to `paused`, each named in the
   handback with what it widened.

BUNDLE — commits in this order; split any that would reach 500 insertions and say so.
C1a COPIES: `.agent/authored/f025-r8-block.md` := this block and each payload as
    `.agent/authored/f025-r8-<name>`. Subject `F025 R8 C1a: copy round 8 block and payloads`.
    Expected by `git show --numstat`: this block's line count plus 79, that is the block copy's own lines and 42/0 `.agent/authored/f025-r8-d6.md`, 8/0 `.agent/authored/f025-r8-ledger.md`, 29/0 `.agent/authored/f025-r8-plan.md`.
C1b RECORDS, one commit, the finding persisted FIRST: the ledger and decisions appends and the plan
    rewrite. Subject `F025 R8 C1b: book round 7's FAIL, register R-1056, record D6`. Expected:
    42/0 `.agent/decisions.md`, 8/0 `.agent/live_review.md`, 7/7 `.agent/plan.md`.
C2 M1 with T2. C3 M2 and M3 with T1. C4 M4. C5 THE MUTATION TOOL,
    `.agent/authored/f025-r8-mutations.py`. Subjects are yours, each beginning `F025 R8 C<n>: `.
C6 THE HANDBACK, `.agent/handoff.md`. Subject `F025 R8 C6: rewrite handoff for round 8`. Then
    `git push origin feature/f025-pause-resume`.

CONSTRAINTS
1. Never edit or retype a payload. Append by python, bytes to bytes.
2. Every commit under 500 insertions by `git show --numstat`. No `# noqa: BLE001` is added.
3. The round's tracked path set is: the `.agent/authored/f025-r8-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `.agent/handoff.md`,
   `packages/orchestration/run_manifest.py`, `packages/orchestration/pingpong_job.py`, the readers
   M3 widens, `tests/orchestration/test_pause_manifest.py`, `tests/ui_server/test_pause_e2e_live.py`,
   and the tests T2 widens. Never weaken an assertion or delete a test. Do NOT touch
   `long_run_executor.py`, `safe_points.py`, `pingpong_loop.py`, `checkpoints.py`, `apps/ui/`, or
   `docs/roadmap/`.
4. A red gate: STOP, commit and push what is verified, write the handoff under AGENTS.md "If
   Blocked". Nothing is merged; no `gh pr create`; no force-push; no `git stash`.
5. Leave every existing worktree alone; the one G5 adds is removed as that step's last action.
6. DO NOT run the full suite (amend0917 rule 1).

DONE-WHEN — every gate executed, every reading reported with its real exit code. G1 to G5 run
before C6 is written.
G1 TRANSPORT: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f025-r8-*` payload copy byte-equal to its source by `git show <C1a>:<path>`
   (the block copy against `.remedy-wt/f025-r8/block.md`); at C1b the appended files equal their
   `3f36bd81` bytes plus their payloads and `.agent/plan.md` equals plan.md; and `open_finding_ids`
   over the ledger at C1b — the reviewer's simulation read `['R-1008', 'R-1055', 'R-1056']`.
G2 THE CODE: `python3 -m ruff check` over every Python file C2 to C5 changed; `git diff --stat
   3f36bd81 <C5> -- packages/orchestration/long_run_executor.py packages/orchestration/safe_points.py
   packages/orchestration/pingpong_loop.py packages/orchestration/checkpoints.py apps/ui docs/roadmap`
   empty; the count of `noqa: BLE001` marks the range adds under `packages`, `apps` and `scripts`,
   which must be 0; and `git diff --name-only <C1b> <C5>`, every path inside constraint 3.
G3 THE TESTS NEAREST THE CHANGE, serially: `python3 -m pytest -q -p no:cacheprovider
   tests/orchestration/test_pause_manifest.py tests/orchestration/test_pause_resume.py
   tests/orchestration/test_pause_resume_cycles.py tests/orchestration/test_job_stop_integration.py
   tests/orchestration/test_run_manifest.py tests/orchestration/test_run_manifest_prework_resume.py
   tests/orchestration/test_run_manifest_call_expectation_lifecycle.py
   tests/orchestration/test_run_manifest_reference_coverage.py
   tests/orchestration/test_run_manifest_terminal_consistency.py
   tests/orchestration/test_run_manifest_writer_postconditions.py
   tests/ui_server/test_pause_e2e_live.py tests/ui_server/test_pause_door_live.py
   tests/test_ble001_ratchet.py tests/cli/test_golden_path.py` — exit 0; report the summary line
   and every `SKIPPED` line. Then the e2e file alone twice more, serially, each summary reported.
G4 THE NEIGHBOURS: first `python3 -m pytest -q -p no:cacheprovider
   tests/ui_server/test_command_channel.py` alone, serially; then `python3
   .remedy-wt/f025-r8/run_sel.py /home/decodeux/Repos/remedy 8` in the primary checkout at C5 —
   round 7's selection plus every manifest and episode test and T1, with 8 xdist workers. At
   `3f36bd81` the reviewer ran the same list without T1 and read `6 failed, 10358 passed, 13 skipped` at exit 1 over 181 files, the six failures all in `tests/cli/test_study_cmd.py`, the known ordering class, whose file alone read `12 passed`. Report its output; re-run
   any failing node's file alone, serially, and report both readings. Then `python3 -m apps.cli.main
   integrity check --json`: six `pass`, `fail_count` 0.
G5 THE RED PROOFS: your tool takes a worktree path, edits the named file INSIDE that worktree
   (asserting each FROM occurs exactly once), prepares it for the live tests by
   `.agent/authored/f025-r7-mutations.py`'s route, and runs `python3 -B -m pytest -q -p
   no:cacheprovider` over T1 and the e2e file from the worktree root after purging `__pycache__`.
   It restores, and prints per mutation its label, exit code, failed count and failing test names,
   with an unmutated control first and last, `restored byte-identical: True` per file, and a final
   `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Mutations:
    m1 `_park_job` writes no manifest;
    m2 `paused` is removed from `_VALID_STATUS`;
    m3 the worked-phase `paused` row loses `EXPECT_NOT_DISPATCHED` from its expectations;
    m4 the task cap's pause writes no manifest;
    m5 `_park_job`'s manifest write passes the pause request id as `stop_request_id`.
   `git worktree add --detach .remedy-wt/f025-r8-mut <C5>`, run
   `python3 -B .agent/authored/f025-r8-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f025-r8-mut`,
   report the whole output. EVERY mutation must be red; one that stays green is reported green, the
   catching test is added in a further commit before C6, and the tool re-run. Then undo the tool's
   worktree preparation, `git worktree remove --force .remedy-wt/f025-r8-mut`, `git worktree
   prune`, `git worktree list`.
G6 AFTER C6 AND THE PUSH, in your final reply only: `git status --porcelain` empty, the local tip
   equal to `origin/feature/f025-pause-resume`, `git log --oneline -n 10`, the push's real outcome,
   and `gh pr list --state open --json number` EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the `git show --numstat` counts you measured (compared with
C1a's and C1b's expectations above), every gate's real output, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, M3's list
of readers read with what was done to each, and the next action. Session section: SESSION 2 of
feature F025, round 8, plus one sentence on how much context you had left. `## Next`: Phase 1 rule
1, the review of round 8, then F025's closure sequence. State the open-findings count as the script
reads it at C1b, and "Operator questions open: <the count of `### Q` headings in the file at C1b>".

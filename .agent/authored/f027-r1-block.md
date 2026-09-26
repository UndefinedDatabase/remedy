STEP F027 R1 — CLAIM F027 AND LAND THE VETO CONTROL PROTOCOL: the mandatory verbatim reason, the pure gate, the unreachable set, the create-only control file per vetoed task, and the command effect with its `task_vetoed` event

GOAL
Pull request 282 is merged; `main` is at `557cbbcc` and F027 is the next unchecked line. Cut its
branch, claim it, re-head the live review record, book F285's round 6 verdict, record DECISION
F027 D1, and land the first part of T001: the task status `vetoed`, and a new module
`packages/orchestration/task_veto.py` holding the reason rule, the state gate, the unreachable set,
the control files and the command effect, with its unit tests in
`tests/orchestration/test_task_veto.py` and a mutation tool proving the tests bite.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests yourself against the specification S1 to S9 below. Only the
`.agent/` records and the STATUS line travel as payloads.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f027-r1-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f027-r1/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f027-r1-dry/`       The reviewer's authoring tree; do not touch it.
  `.remedy-wt/f027-r1-drafts/`    The reviewer's drafts; do not touch them.
  `.remedy-wt/f027-review/`       The reviewer's scripts; do not touch them.
  `.remedy-wt/f027-r1-worker/`    YOURS for logs and scripts; create it if absent. All six are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, command substitution, `cd <dir> && git ...`,
and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit
codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Never run npm or npx.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read `main`, and
   `git log --oneline -1` must read `557cbbcc`. Report all three. Then
   `git checkout -b feature/f027-task-veto` and report the branch. Do NOT pull: the Open PR Gate
   ran before you and `main` is already at the merge commit.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f027-r1/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f027-r1-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| claim.diff | 163 | 18444 | 2a11dfd715557f45a84c0eb49383f7302207d74865f0f178a04672639378bfbe |
| context.md | 37 | 1520 | d3ca4f450887b6c9456dc33456fd676775b5257ba4ec037923c9f26de2f51841 |
| plan.md | 37 | 1533 | de29e39ca1a1b9b6d15106d2be7a97df66deb469de618c05080465fcaaa8a392 |

`plan.md` and `context.md` are REWRITES of `.agent/plan.md` and `.agent/context.md`.
`claim.diff` goes on with `git apply`; the reviewer generated it with `git diff HEAD` from a tree at
`557cbbcc` into which it wrote the edits. It edits `.agent/live_review.md` (the re-head, which
replaces everything above the `## Findings` heading line, then F285's round 6 gate entry
appended), `docs/roadmap/STATUS.md` (F027's line `[ ]` to `[~]`) and `.agent/decisions.md`
(DECISION F027 D1 appended). Read D1 before you write code: it is the design this specification
implements, and it records what was measured at `557cbbcc`.

THE SPECIFICATION
S1 THE STATUS. `packages/orchestration/pingpong_job.py` gains `TASK_VETOED = "vetoed"` directly
   after `TASK_SPLIT`, with a comment above it naming DECISION F027 D1 and saying the status is
   terminal for the task and written by a runner's fold, never by the veto command. Nothing else
   in that file changes; `TASK_DONE_STATUSES` does not gain it.
S2 THE MODULE. A NEW FILE at `packages/orchestration/task_veto.py`, with a docstring naming
   DECISION F027 D1 and stating, in a sentence each, why a veto is a control file and never a
   write of `job.json`, why the reason is refused rather than stored altered, and why there is no
   un-veto. It imports from `packages.common.secure_fs`, `packages.orchestration.safe_points`,
   `packages.orchestration.stream_evidence` (`redact_text`), `packages.orchestration.dag_schedule`
   (`blocked_downstream`) and `packages.orchestration.pingpong_job` (the `TASK_*` constants), and
   imports `RunLogWriter` and `run_log_dir` inside the functions that use them, as
   `pause_control.py` does. No import of `pause_control`, `subprocess`, `signal` or `threading`.
   Two exception classes: `TaskVetoRefused(Exception)` carrying `code` and `detail`, raised or
   returned for a refusal an operator can act on, and `TaskVetoError(RuntimeError)` for a control
   area or an on-disk entry that cannot be used or trusted; a `StopControlError` from
   `safe_points.open_job_control_fd` is re-raised as `TaskVetoError`.
S3 THE REASON. `MAX_VETO_REASON_CHARS = 500`. `validate_veto_reason(reason) -> str` raises
   `TaskVetoRefused` and otherwise returns `reason` UNCHANGED — never stripped, never bounded,
   never redacted. In this order: not a `str`, or empty after `strip()`, is `reason_required`;
   longer than 500 characters is `reason_too_long`; holding any character of
   `[\x00-\x1f\x7f]`, newline and tab included, or differing from `redact_text(reason)`, is
   `reason_invalid`, whose detail says that such text is refused rather than stored altered.
S4 THE GATE, pure — no I/O. `VETOABLE_TASK_STATUSES = (TASK_PENDING, TASK_RUNNING, TASK_BLOCKED,
   TASK_FAILED, TASK_SKIPPED)`. `veto_refusal(job_state, task_status, *, already_vetoed) ->
   TaskVetoRefused | None`, reading both states by their string value (a `RunState` or a plain
   string). In this order: a job state of `completed`, `failed` or `cancelled` is
   `job_not_vetoable`; `already_vetoed`, or a task status of `vetoed`, is `task_already_vetoed`;
   a task status outside `VETOABLE_TASK_STATUSES` is `task_not_vetoable`. Each refusal's `detail`
   names the state or status it refused. Every other combination, a `running` job included,
   answers None.
S5 THE UNREACHABLE SET, pure. `veto_unreachable(tasks, vetoed_ids) -> tuple[str, ...]`:
   `blocked_downstream(tasks, vetoed_ids)` minus the vetoed ids, keeping only tasks whose status,
   read by its string value, is in `VETOABLE_TASK_STATUSES`, in the order of `tasks`.
S6 THE CONTROL FILES. `VETOED_TASKS_DIRNAME = "vetoed_tasks"`, a subdirectory of the job's control
   directory reached through `safe_points.open_job_control_fd` and verified and created as
   `pause_control._open_named_dir` does it (write your own helper; do not import that one). A
   frozen dataclass `TaskVeto` of `job_id`, `task_id`, `request_id`, `reason`, `actor`,
   `requested_at` and `status_at_veto`, whose `to_json()` also writes `"task_veto_v": 1`.
   `record_task_veto(job_id, task_id, reason, actor, status_at_veto, *, control_root_path=None)
   -> tuple[TaskVeto, bool]`: validates the reason with S3 (a refusal raises `TaskVetoRefused`),
   validates the task id as `pause_control._validate_task_id` does (raising `TaskVetoError`),
   bounds the actor with `safe_text` to `safe_points.MAX_SOURCE_CHARS` with `"unknown"` as the
   fallback, names the file `<first 32 hex chars of sha256(task id)>.json`, and publishes it
   create-only with `secure_fs.write_file_atomically(..., create_only=True)` at
   `safe_points.CONTROL_FILE_MODE`. It answers the new veto and True, or — when an entry already
   exists, before the write or after losing the publication race — that entry read back unchanged
   and False. `vetoed_tasks(job_id, *, control_root_path=None) -> tuple[TaskVeto, ...]` answers
   every entry ordered by `requested_at` then `task_id`, and () when the control root, the job's
   directory or `vetoed_tasks/` does not exist; an entry that cannot be read, is not a JSON object,
   lacks a task id or a request id, or whose stored reason fails S3, RAISES `TaskVetoError` —
   dropping it would dispatch a task the operator vetoed. The stored reason is read back verbatim.
S7 THE COMMAND EFFECT. `veto_task_command(job, *, task_id, reason, actor, control_root_path=None)
   -> dict`, `job` a loaded `JobPlan`. It never raises for a refusal: it answers
   `{"outcome": "refused", "code", "detail", "task_id"}`, checking in this order S3's reason, a
   task id no entry of `job.tasks` holds (`unknown_task`), and S4's gate, with `already_vetoed`
   true when `vetoed_tasks` holds an entry for the task. Otherwise it calls `record_task_veto` with
   the task's status as `status_at_veto`; when that answers False the result is
   `task_already_vetoed`, carrying the existing entry's `request_id`. On success it answers
   `{"outcome": "vetoed", "request_id", "task_id", "reason", "actor", "status_at_veto",
   "unreachable"}`, where `unreachable` is `veto_unreachable(job.tasks, [task_id])` without every
   task another entry of `vetoed_tasks` already holds, as a list. It NEVER writes `job.json`.
S8 THE EVENT. Whenever the command answers `vetoed`, AND whenever it answers
   `task_already_vetoed` because an entry exists, it first reads the job's ledger for a
   `task_vetoed` event carrying that entry's `request_id`, the way
   `pause_control._task_pause_event_exists` does (write your own reader), and writes one through
   `RunLogWriter(job.job_id).log("task_vetoed", outcome="vetoed", scope="task", task_id=...,
   request_id=..., reason=..., actor=..., status_at_veto=..., requested_at=...,
   unreachable_task_ids=[...])` only when the ledger could be read and holds none; so a retry after
   a failed event write repairs the audit line exactly once. `"task_vetoed"` joins `EVENT_NAMES` in
   `packages/orchestration/event_names.py`, in its sorted place.
S9 THE ORPHAN GUARD. Nothing imports the new module until a later round wires it into the runners
   and the door, so `ALLOWED_UNWIRED` in `tests/test_no_orphan_modules.py` gains its entry, with the
   reason "F027 T001: the veto control protocol; the runners' fold and the write door wire it in
   later rounds".

THE TESTS — a NEW FILE at `tests/orchestration/test_task_veto.py`, over a control root under
`tmp_path` and `REMEDY_DATA_DIR` monkeypatched to `tmp_path` for the ledger. Build graph tasks with
`flight_task`, and tasks without plan metadata with `legacy_task`, from
`tests/orchestration/test_dag_schedule.py`, imported, as `tests/orchestration/test_pause_control.py`
does. Build any secret-shaped reason at run time from
parts, so no secret-shaped literal sits in the source. It must cover at least: S3's every code,
including a whitespace-only reason, exactly 500 and 501 characters, a newline, a tab and a DEL, a
secret-shaped reason, and a reason with leading and trailing spaces and a path returned unchanged;
S4 as a parametrized matrix over every `TASK_*` constant of `pingpong_job` and every `RunState`
job state, each refusal's code and that its detail names the state; S5 over the diamond (veto B:
D; veto A: B, C and D; veto B and C: D) and over tasks without plan metadata (veto the second of
four: the last two), with a done task and an already vetoed task left out; S6's create-only file,
its digest name and content, a second record answering the first entry and False, a forced
publication race converging on the winner, a symlinked control area refused, an unparsable entry
and an entry with a tampered reason each raising, the ordering, and () on a missing root; S7's
answer, every refusal in its order (a blank reason with an unknown task answers
`reason_required`), nothing written by a refusal, the unreachable set without another veto's
tasks, and the job's `job.json` byte-identical after a successful veto; S8's one event with the
reason verbatim, no second event on a repeated veto, and the repair of a missing event on the
retry after a failed event write.

BUNDLE — the commits are C1a, C1b, C2, C3, C4 and C5, in this order.

C1a — copy this block and the state payloads
  `.agent/authored/f027-r1-block.md` := this block, and `.agent/authored/f027-r1-plan.md` and
  `.agent/authored/f027-r1-context.md` := plan.md and context.md. All by `shutil.copyfile`.
  Subject: `F027 R1 C1a: copy round 1 block and state payloads into .agent/authored/`
  Its insertions are this block's line count plus 74. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the claim diff
  `.agent/authored/f027-r1-claim.diff` := claim.diff.
  Subject: `F027 R1 C1b: copy round 1 claim diff into .agent/authored/`
  Expected insertions: 163.

C2 — THE CLAIM AND ITS RECORDS, in this order:
   1. `git apply` claim.diff
   2. rewrite `.agent/plan.md` := plan.md
   3. rewrite `.agent/context.md` := context.md
  Subject: `F027 R1 C2: claim F027, re-head the live review record, book F285 R6, record D1`
  Expected by `git show --numstat` (insertions and deletions): 15/11 context.md, 84/0 decisions.md, 22/20 live_review.md, 24/13 plan.md, 1/1 STATUS.md.

C3 — THE CODE: S1 to S9 — `packages/orchestration/pingpong_job.py`,
  `packages/orchestration/task_veto.py` (`git add`ed: an untracked module fails
  `integrity check`'s `relevant_untracked`), `packages/orchestration/event_names.py` and the
  `ALLOWED_UNWIRED` entry.
  Subject: `F027 R1 C3: add the task veto control protocol and the vetoed task status`

C4 — THE TESTS AND THE MUTATION TOOL: `tests/orchestration/test_task_veto.py`, and your mutation
  tool (G5) saved as `.agent/authored/f027-r1-mutations.py`.
  Subject: `F027 R1 C4: test the task veto control protocol and add the mutation tool`

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F027 R1 C5: rewrite handoff for round 1`
  Then `git push -u origin feature/f027-task-veto`. Do NOT create a pull request: the branch
  opens one at F027's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects (C3a and C3b, C4a and C4b), and say so.
3. The round's whole tracked path set is: the `.agent/authored/f027-r1-*` copies and tool,
   `.agent/live_review.md`, `docs/roadmap/STATUS.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `.agent/context.md`, `packages/orchestration/pingpong_job.py`,
   `packages/orchestration/task_veto.py`, `packages/orchestration/event_names.py`,
   `tests/test_no_orphan_modules.py`, `tests/orchestration/test_task_veto.py`, and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only 557cbbcc` and the
   branch tip after C5. Do NOT touch `packages/orchestration/pause_control.py`,
   `packages/orchestration/safe_points.py`, `packages/orchestration/dag_schedule.py`,
   `packages/orchestration/ui_server.py`, `apps/cli/command_catalog.py`, anything under
   `apps/ui/`, `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md`,
   `README.md` or `docs/roadmap/features/T5_F027.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main` after the
   branch is cut, no branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4 (`.remedy-wt/f027-r1-dry` and the older `f015-*`, `f020-*`, `f023-*`,
   `f024-*`, `f025-*` and `f284-*` ones), and every existing stash alone. The worktree G5 adds goes
   under `.remedy-wt/`, is removed as that step's last action, and `git worktree list` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F027's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f027-r1-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f027-r1/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE CLAIM — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its authoring tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 290468 | 1e4eb4d2416b960468b2d89354973daf307609ce18755bba2d69a95493146382 |
 | docs/roadmap/STATUS.md | 53437 | b52bb1a587aee8d6d2e664de7b19df8b71445a7e7453b7f91c24325509f1222e |
 | .agent/decisions.md | 2155629 | fd65eba3d42c5bc139d2bf498decaada8d89fb2969038be479de2434ac9d8418 |
 | .agent/plan.md | 1533 | de29e39ca1a1b9b6d15106d2be7a97df66deb469de618c05080465fcaaa8a392 |
 | .agent/context.md | 1520 | d3ca4f450887b6c9456dc33456fd676775b5257ba4ec037923c9f26de2f51841 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `557cbbcc` and at C2 (the reviewer read
 it empty at both); at C2 the ledger has exactly one line reading `## Findings` and exactly one
 reading `## Steps`, and its last line begins `Gate: F285 R6 — `; F027's STATUS line at C2 read
 back in full, which must read `- [~] F027 — Task veto`; and `git diff --name-only <C1b> <C2>`,
 which must name exactly the paths of the table above.

G3 THE CODE — `python3 -m ruff check packages/orchestration/pingpong_job.py
 packages/orchestration/task_veto.py packages/orchestration/event_names.py
 tests/test_no_orphan_modules.py tests/orchestration/test_task_veto.py` at C4;
 `git diff -U0 <C2> <C3> -- packages/orchestration/pingpong_job.py
 packages/orchestration/event_names.py`, reported whole, which must add the constant with its
 comment and the one event name and nothing else; and a python `ast` reading at C4 of every
 module `task_veto.py` imports (each `Import` and `ImportFrom` node, at any depth), which must name
 none of `subprocess`, `threading`, `signal` or `packages.orchestration.pause_control`.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_task_veto.py tests/orchestration/test_pause_control.py tests/orchestration/test_dag_schedule.py tests/orchestration/test_event_names.py tests/test_no_orphan_modules.py tests/orchestration/test_task_edit_runtime.py tests/orchestration/test_task_expectation_status_truth.py tests/orchestration/test_import_reachability.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the new test file and the golden path, serially,
 inside its authoring tree carrying the claim's records, and read `789 passed, 3 skipped` at real
 exit code 0. TWO of those skips are toolchain nodes a worktree cannot run and the primary
 checkout can, and each must PASS in your run, not skip: the typescript node in
 `tests/ui_server/test_dashboard_contract.py` and the vitest node in
 `tests/orchestration/test_test_runner.py`. The third, the D12 quarantine in
 `tests/test_agent_tooling.py`, stays skipped. Report every `SKIPPED` line the `-rs` summary
 prints, the number of nodes your new file contributes (`--collect-only -q` on it), and account
 for any other difference from the reviewer's count. Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0.

G5 THE RED PROOFS — your tool `.agent/authored/f027-r1-mutations.py` takes a worktree path, and
 for each mutation below edits the named module INSIDE that worktree (asserting its FROM text
 occurs exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider` over the worktree's
 `tests/orchestration/test_task_veto.py` from the worktree's root after purging its
 `__pycache__` directories, restores the bytes, and prints one line per mutation: its label, the
 exit code, the failed count and the failing node ids. It runs an unmutated control first and last
 and ends with `restored byte-identical: True` per file and a final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. The mutations, each a real behaviour change
 in `task_veto.py`:
  m1 a whitespace-only reason is accepted;
  m2 a 501-character reason is accepted;
  m3 a reason holding a control character is accepted;
  m4 a secret-shaped reason is accepted;
  m5 an accepted reason is returned stripped;
  m6 the gate admits a `completed` job;
  m7 the gate admits an `applied_to_job_workspace` task;
  m8 the gate refuses a `skipped` task;
  m9 the gate ignores `already_vetoed`;
  m10 the control file is named by the task id itself instead of its digest;
  m11 the unreachable set keeps a task whose work is done;
  m12 the control file is published without `create_only`, so a second veto replaces the first;
  m13 the command writes the event without reading the ledger first;
  m14 the command checks the task before the reason;
  m15 the command's unreachable set keeps another veto's tasks.
 Run it: `git worktree add --detach .remedy-wt/f027-r1-mut <C4>`, then
 `python3 -B .agent/authored/f027-r1-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f027-r1-mut`
 and report its whole output. EVERY mutation must be red with at least one failing node; a
 mutation that stays green is reported as green, never papered over, and you then add the test
 that catches it in C4 before C5 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f027-r1-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 7`, which must show C5, C4, C3, C2, C1b, C1a and `557cbbcc` in that order
 (more lines if constraint 2 split a commit); `git worktree list`, which must show the primary
 checkout and the worktrees constraint 6 names, and nothing else; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the insertion count you MEASURED beside the one this
block expected (none is expected for C3 and C4 — report what you measure), every gate's real
output and exit code, the authored-text proofs, the item-status table AGENTS.md requires (one row
per commit and per gate), the deviations, and the next expected action. Report what you ran, not
what you expected to find. Your Session section reads SESSION 1 of feature F027, round 1, and says
in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 1, then the rest of T001 — the runners fold a veto at their safe points, the in-progress
finish rule, and the terminal accounting. State the open-findings count, 0, and the
operator-questions count, 5.

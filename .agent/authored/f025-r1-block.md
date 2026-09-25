STEP F025 R1 — CLAIM F025 AND LAND T001's FIRST HALF: the pause control files of both scopes and the mask arithmetic

GOAL
Pull request 279 is merged; `main` is at `49624d5c` and F025 is the next unchecked line. Cut its
branch, claim it, re-head the live review record, book F024's round 9 verdict and R-1048's
resolution, record DECISION F025 D1, and land the first half of T001: a new module
`packages/orchestration/pause_control.py` — the job-scope pause request, the task-scope pause
files, and the pure mask arithmetic — with its unit tests in
`tests/orchestration/test_pause_control.py`, and a mutation tool proving the tests bite.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write `pause_control.py` and its tests yourself against the specification S1 to S9 below. Only the
`.agent/` records and the STATUS line travel as payloads.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f025-r1-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f025-r1/`           READ-ONLY. The reviewer's block and scripts.
  `.remedy-wt/f025-r1-dry/`       The reviewer's authoring tree; do not touch it.
  `.remedy-wt/f025-r1-worker/`    YOURS for logs and scripts; create it if absent. All four are
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
   `git log --oneline -1` must read `49624d5c`. Report all three. Then
   `git checkout -b feature/f025-pause-resume` and report the branch. Do NOT pull: the Open PR
   Gate ran before you and `main` is already at the merge commit.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f025-r1/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f025-r1-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| claim.diff | 171 | 20176 | 506a8c85a23624a68ec2a9aba95866a0f782b605169f9ca2230179a2e3c83053 |
| context.md | 35 | 1544 | 9f6e71a9ae0000d7ae04cabcf5f4bfbd31ef41b7d0262fc0a5a1065c70a6f414 |
| plan.md | 36 | 1410 | d4fedcab75d5384f8d043bee85fc135660671ffbae7b500bb61a465233c2b11e |

`plan.md` and `context.md` are REWRITES of `.agent/plan.md` and `.agent/context.md`.
`claim.diff` goes on with `git apply`; the reviewer generated it with `git diff HEAD` from a tree at
`49624d5c` into which it wrote the edits. It edits `.agent/live_review.md` (the re-head, which
replaces everything above the `## Findings` heading line, then F024's round 9 gate entry and
R-1048's `Done:` paragraph appended), `docs/roadmap/STATUS.md` (F025's line `[ ]` to `[~]`) and
`.agent/decisions.md` (DECISION F025 D1 appended). Read D1 before you write code: it is the
design this specification implements.

THE SPECIFICATION — `packages/orchestration/pause_control.py`
S1 SHAPE. A NEW FILE at `packages/orchestration/pause_control.py`, with a docstring naming DECISION F025 D1 and stating, in a sentence each,
   why the pause lives beside the kill switch rather than inside it and why a pause is never a
   waiting process. It imports from `packages/orchestration/safe_points.py` (its anchored
   `open_job_control_fd`, `validate_job_id`, `new_request_id`, `utc_now_iso`, the bounds
   `MAX_REASON_CHARS`, `MAX_SOURCE_CHARS`, `MAX_CONTROL_BYTES`, the file and directory modes) and
   from `packages/common/secure_fs.py`, and EDITS NEITHER. No import of `subprocess`, `signal`,
   `threading` or `time.sleep`; no I/O outside the job's control directory.
S2 RECORDS. `PauseControlError(RuntimeError)`. Frozen dataclasses with `to_json()`:
   `PauseSignal(job_id, request_id, reason, source, requested_at, pause_signal_v=1)` and
   `TaskPause(job_id, task_id, request_id, reason, source, requested_at)`. Reason and source are
   bounded and cleaned exactly as `request_stop` bounds its own (read `_bounded` there and reuse or
   mirror it; an over-long reason is truncated, never refused).
S3 JOB SCOPE, the file `pause.json` in the job's control directory:
   `request_pause(job_id, reason="", source="cli", *, control_root_path=None) -> PauseSignal` —
   create-only publication with the stop's race rule: a pending request is returned unchanged,
   and two concurrent callers converge on one request id.
   `pause_requested(job_id, *, control_root_path=None) -> PauseSignal | None` — the cheap check:
   one directory open, one read; a control root or job directory that does not exist is None.
   `settle_pause(job_id, signal, outcome, *, control_root_path=None) -> str` — `outcome` is one
   of `served`, `withdrawn`, `superseded_by_stop` (anything else raises). It first publishes the
   archived copy, `pause_archive/<request_id>.json`, holding the request plus `outcome` and
   `settled_at`, and ONLY THEN removes the pending file, and only if the pending file holds that
   request id; it returns the control-relative path of the archived copy. When an archived copy
   with that request id already exists (a second settle, or a crash after the archive and before
   the removal), it writes no new archive, still removes a pending file holding that id, and
   returns the existing copy's path. If publishing the archive fails, the pending file stays.
   `withdraw_pause(job_id, *, control_root_path=None) -> PauseSignal | None` — settles a pending
   request as `withdrawn`; None when nothing is pending.
   Nothing this module writes goes under the stop's `archive/` directory: after a pause is
   served, `safe_points.stop_status(job_id).consumed_count` still reads 0.
S4 TASK SCOPE, one create-only file per paused task under `paused_tasks/` in the job's control
   directory, named `<first 32 hex chars of sha256(task_id)>.json` and holding the `TaskPause`:
   `request_task_pause(job_id, task_id, reason="", source="cli", *, control_root_path=None) ->
   TaskPause` — pausing a paused task returns its existing entry unchanged.
   `release_task_pause(job_id, task_id, *, control_root_path=None) -> TaskPause | None` —
   archives the entry under `pause_archive/tasks/`, with `outcome` `released` and `settled_at`,
   then removes it; None, and nothing written, when the task is not paused.
   `paused_tasks(job_id, *, control_root_path=None) -> tuple[TaskPause, ...]` — every entry,
   ordered by `requested_at` then `task_id`; an empty tuple when nothing exists. An entry that
   cannot be read or parsed RAISES `PauseControlError`: dropping it would dispatch a task the
   operator paused.
   A task id is any non-empty string of at most 200 characters with no control character; any
   other value raises `PauseControlError`. Because the file name is a digest, an id holding `/`,
   `..` or a NUL-free oddity is stored safely and round-trips exactly.
S5 THE MASK, pure — no I/O, no clock:
   `withheld_task_ids(order, pending, paused, *, depends_on=None) -> WithheldTasks`, where
   `order` is the plan's task ids in plan order, `pending` the ids whose status is pending,
   `paused` any iterable of ids, and `depends_on` a mapping from task id to the ids it depends
   on, or None for the linear runner. `WithheldTasks` is a frozen dataclass of four tuples in plan
   order: `withheld` (every id not to dispatch), `paused` (the paused ids that are pending),
   `downstream` (withheld only because of a paused task), `inert` (paused ids naming no pending
   task, in the order given, de-duplicated). LINEAR (`depends_on` None): the first paused pending
   task in plan order and every pending task after it are withheld; tasks before it are not.
   GRAPH: the paused pending tasks and every pending task that depends on one of them,
   transitively. A task that is not pending is never withheld and never propagates.
S6 SIZE. Every commit stays under 500 inserted lines. If the module alone would reach that, land
   it as C3a (S2 and S3) and C3b (S4 and S5), each with its own subject.

THE TESTS — a NEW FILE at `tests/orchestration/test_pause_control.py`, against a `tmp_path` control root, one
class per scope and one for the mask. It must cover at least: S3's idempotence, convergence of
two requests, the cheap check's None on a missing root, the archive-before-remove order (make the
archive publication fail and show the request still pending), a settle that leaves a pending
request with another id in place, the refusal of an unknown outcome, the stop's
`consumed_count` staying 0; S4's idempotence, release of an unpaused task writing nothing, the
ordering of `paused_tasks`, a corrupt entry raising, an id with `/` and `..` round-tripping with
every file inside `paused_tasks/`, a refused empty and over-long id; S2's truncation of an
over-long reason; S5's linear rows (paused first, middle and last; a paused task already done
is inert and withholds nothing; two paused tasks) and graph rows on the `diamond` shape of
`tests/orchestration/test_dag_schedule.py`, whose `downstream` must EQUAL
`dag_schedule.blocked_downstream` over the same plan and seeds — build the plan with that file's
own `flight_task` helper, imported, so the two readings cannot drift apart; and a refusal of a
symlinked `paused_tasks` directory.

BUNDLE — the commits are C1a, C1b, C2, C3 (or C3a and C3b), C4 and C5, in this order.

C1a — copy this block and the state payloads
  `.agent/authored/f025-r1-block.md` := this block, and `.agent/authored/f025-r1-plan.md` and
  `.agent/authored/f025-r1-context.md` := plan.md and context.md. All by `shutil.copyfile`.
  Subject: `F025 R1 C1a: copy round 1 block and state payloads into .agent/authored/`
  Its insertions are this block's line count plus 71. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C1b — copy the claim diff
  `.agent/authored/f025-r1-claim.diff` := claim.diff.
  Subject: `F025 R1 C1b: copy round 1 claim diff into .agent/authored/`
  Expected insertions: 171.

C2 — THE CLAIM AND ITS RECORDS, in this order:
   1. `git apply` claim.diff
   2. rewrite `.agent/plan.md` := plan.md
   3. rewrite `.agent/context.md` := context.md
  Subject: `F025 R1 C2: claim F025, re-head the live review record, book F024 R9, record D1`
  Expected by `git show --numstat` (insertions and deletions): 15/17 context.md, 82/0 decisions.md, 29/24 live_review.md, 23/20 plan.md, 1/1 STATUS.md.

C3 — THE MODULE, `packages/orchestration/pause_control.py`, `git add`ed (an untracked module
  fails `integrity check`'s `relevant_untracked`).
  Subject: `F025 R1 C3: add the pause control files and the mask arithmetic`

C4 — THE TESTS AND THE MUTATION TOOL: `tests/orchestration/test_pause_control.py`, and your
  mutation tool (G5) saved as `.agent/authored/f025-r1-mutations.py`.
  Subject: `F025 R1 C4: test the pause control files and the mask, and add the mutation tool`

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F025 R1 C5: rewrite handoff for round 1`
  Then `git push -u origin feature/f025-pause-resume`. Do NOT create a pull request: the branch
  opens one at F025's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading.
3. The round's whole tracked path set is: the `.agent/authored/f025-r1-*` copies and tool,
   `.agent/live_review.md`, `docs/roadmap/STATUS.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `.agent/context.md`, `packages/orchestration/pause_control.py`,
   `tests/orchestration/test_pause_control.py`, and `.agent/handoff.md`. Report the list you
   measure with `git diff --name-only 49624d5c HEAD` after C5. Do NOT touch
   `packages/orchestration/safe_points.py`, `packages/orchestration/pingpong_job.py`,
   `packages/orchestration/long_run_executor.py`, `packages/orchestration/dag_schedule.py`,
   `packages/orchestration/event_names.py`, `.agent/prose_slips.md`, `.agent/candidates.md`,
   `.agent/operator_questions.md`, `README.md` or `docs/roadmap/features/T5_F025.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main` after the
   branch is cut, no branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4 (`.remedy-wt/f025-r1-dry`, `.remedy-wt/f024-r9-sim` and the older
   `f015-*`, `f020-*`, `f023-*`, `f024-*` and `f284-*` ones), and every existing stash alone. The
   worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last action, and
   `git worktree list` is reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F025's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f025-r1-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f025-r1/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE CLAIM — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its authoring tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 298345 | 4657ecfc6446ccf3891e0850edfc1b11fe0bbfb794bc878d37b1b1cb1cd96110 |
 | docs/roadmap/STATUS.md | 52107 | b96ba6d2412d48aada739351d9e4a6a8db46f4c103e90320616b1793f24a7bd8 |
 | .agent/decisions.md | 2100860 | 24b15c68325ccf9f333faf8f942556f70814c0ba056265e8f48beea6b025c7ab |
 | .agent/plan.md | 1410 | d4fedcab75d5384f8d043bee85fc135660671ffbae7b500bb61a465233c2b11e |
 | .agent/context.md | 1544 | 9f6e71a9ae0000d7ae04cabcf5f4bfbd31ef41b7d0262fc0a5a1065c70a6f414 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `49624d5c` and at C2 (the reviewer read
 R-1008 and R-1048 at the first and R-1008 alone at the second); at C2 the ledger has exactly one
 line reading `## Findings` and exactly one reading `## Steps`, and its last line begins
 `Done: R-1048 — `; F025's STATUS line at C2 read back in full, which must read
 `- [~] F025 — Pause/resume (global & per node)`; and `git diff --name-only <C1b> <C2>`, which
 must name exactly the paths of the table above.

G3 THE MODULE — `python3 -m ruff check packages/orchestration/pause_control.py
 tests/orchestration/test_pause_control.py` at C4; `git diff --name-only` between C2 and C4 naming
 exactly the module, the test file and the mutation tool; a python `ast` reading at C4 of every
 module the new module imports (each `Import` and `ImportFrom` node), which must name none of
 `subprocess`, `threading`, `signal` or `time`; and that
 `git diff --stat 49624d5c <C4> -- packages/orchestration/safe_points.py
 packages/common/secure_fs.py` is empty.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_pause_control.py tests/orchestration/test_safe_points.py tests/orchestration/test_dag_schedule.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/orchestration/test_block_lint.py tests/orchestration/test_import_reachability.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the new test file and the golden path, serially,
 inside its authoring tree carrying the claim's records, and read `686 passed, 3 skipped` at real
 exit code 0. TWO of those skips are toolchain nodes a worktree cannot run and the primary checkout
 can, and each must PASS in your run, not skip: the typescript node in
 `tests/ui_server/test_dashboard_contract.py` (`tsc --noEmit`) and the vitest node in
 `tests/orchestration/test_test_runner.py`. The third, the D12 quarantine in
 `tests/test_agent_tooling.py`, stays skipped. Report every `SKIPPED` line the `-rs` summary
 prints, the number of nodes your new file contributes (`--collect-only -q` on it), and account
 for any other difference from the reviewer's count. Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0.

G5 THE RED PROOFS — your tool `.agent/authored/f025-r1-mutations.py` takes a worktree path, and
 for each mutation below edits `pause_control.py` INSIDE that worktree (asserting its FROM text
 occurs exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider` over the worktree's
 `tests/orchestration/test_pause_control.py` from the worktree's root after purging its
 `__pycache__` directories, restores the bytes, and prints one line per mutation: its label,
 the exit code, the failed count and the failing node ids. It runs an unmutated control first
 and last and ends with `restored byte-identical: True` per file and a final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. The mutations, each a real behaviour change:
  m1 `request_pause` overwrites a pending request with a new id;
  m2 `pause_requested` always returns None;
  m3 `settle_pause` removes the pending file BEFORE publishing the archive;
  m4 `settle_pause` removes a pending file whose request id differs from the signal's;
  m5 the pause archive is written under the stop's `archive/` directory;
  m6 `settle_pause` accepts an unknown outcome;
  m7 `request_task_pause` replaces an existing entry with a new request id;
  m8 `release_task_pause` of an unpaused task writes an archive entry;
  m9 `paused_tasks` skips an entry it cannot parse;
  m10 the task file is named by the raw task id instead of its digest;
  m11 the linear mask withholds only the paused task, not the tasks after it;
  m12 the linear mask also withholds the pending tasks BEFORE the paused one;
  m13 the graph mask withholds direct dependents only, not transitive ones;
  m14 a paused task that is not pending still withholds its dependents;
  m15 the reason is stored unbounded.
 Run it: `git worktree add --detach .remedy-wt/f025-r1-mut <C4>`, then
 `python3 -B .agent/authored/f025-r1-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f025-r1-mut`
 and report its whole output. EVERY mutation must be red with at least one failing node; a
 mutation that stays green is reported as green, never papered over, and you then add the test
 that catches it in C4 before C5 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f025-r1-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 8`, which must show C5, C4, C3 (or C3b and C3a), C2, C1b, C1a and
 `49624d5c` in that order; `git worktree list`, which must show the primary checkout and the
 worktrees constraint 6 names, and nothing else; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the insertion count you MEASURED beside the one this
block expected (none is expected for C3 and C4 — report what you measure), every gate's real
output and exit code, the authored-text proofs, the item-status table AGENTS.md requires (one row
per commit and per gate), the deviations, and the next expected action. Report what you ran, not
what you expected to find. Your Session section reads SESSION 1 of feature F025, round 1, and says
in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 1, then T001's second half — the pause at the linear runner's and the cycle executor's safe
points and ready sets, parking, the relaunch, a stop beating a pause, and the deadline counting
through a pause. State the open-findings count, 1, and the operator-questions count, 3.

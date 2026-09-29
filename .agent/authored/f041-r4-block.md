STEP F041 R4 — T002 THROUGH THE DOOR: the preview pair on the write door, the UI server's preview worker with its revalidation and idle stop, and a view that links only while live

GOAL
Round 3 passed at `468b3a36`. Book it and record DECISION F041 D4 in one commit, then land D4
against the reviewer's tests: four functions added to `packages/orchestration/preview_control.py`
and a gate on its view, the new `packages/orchestration/preview_worker.py`, and in
`packages/orchestration/ui_server.py` the door's preview clause, the `preview` endpoint and the
worker's life inside `start_ui_server`, wired by the reviewer's wiring payload.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE TESTS AND THE WIRING ARE THE REVIEWER'S AND THE
CODE IS YOURS: tests.diff and worker_tests.diff are the acceptance, wiring.diff is applied as it
is, and you write the code against both and S1 to S3 below. You never edit a payload; if one looks
wrong to you, STOP and report it. Read DECISION F041 D4 in records.diff before you write code,
and read whole before you edit: `packages/orchestration/preview_control.py`, and in
`packages/orchestration/ui_server.py` the class attributes of `_RemedyHandler`,
`_handle_command_submission` from its `job.pause` clause to its `job.veto-task` clause,
`_dispatch_job_pause`, `_build_artifacts_json` and `start_ui_server`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f041-r4-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f041-r4/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f041-r4-dry/`, `.remedy-wt/f041-r4-sim/`, `.remedy-wt/f041-r1-scratch/`
                                  The reviewer's trees and scripts; do not touch them.
  `.remedy-wt/f041-r4-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Set environment variables for a child process inside a Python script (`subprocess.run(...,
env=...)`), never on a command line. Never run npm or npx. Before every commit, run
`git diff --cached --stat` and confirm the index holds exactly that commit's paths. Every comment
and docstring you write names a command only as a whole real command, never with a placeholder in
place of a word, because `tests/cli/test_advertised_commands.py` refuses such a line.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f041-artifact-preview`, and `git log --oneline -1` must read `468b3a36e`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f041-r4/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f041-r4-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 28 | 9399 | 19a417ff7e3702d772d3181a1814f2857c2b57241b6e3dfddfa5efe481584bd7 |
| wiring.diff | 60 | 3936 | 44226ff3ae012f5ce068ab0ff2932e2962a7f146b146d59b0ef97c7f2022132b |
| tests.diff | 297 | 13679 | af450c75305957d5c21e0141dd51f681aedb8c003def2e265b7c77c64f15a048 |
| worker_tests.diff | 217 | 8278 | 351d9c4a60e7d6d621f2041cc2c5cb4f5eb70183c97c986b0b153c8784254583 |
| plan.md | 28 | 918 | e5c186ceb181bd44b681b8433bc6ab01b69332165a7d3db2608fb1e4cc48f372 |

`plan.md` is a REWRITE of `.agent/plan.md`. Every `.diff` goes on with `git apply`; the reviewer
generated them with `git diff HEAD` from a tree at `468b3a36e`. `records.diff` appends round 3's
gate entry to `.agent/live_review.md` and DECISION F041 D4 to `.agent/decisions.md`.
`wiring.diff` adds the preview pair to `UI_EXPOSED_COMMANDS` in `apps/cli/command_catalog.py`,
the `preview.idle_ttl_seconds` key to `packages/orchestration/config.py` with its line in
`docs/guides/environment.md`, and `preview_worker` to
`tests/orchestration/import_reachability_allowlist.txt`. `tests.diff` extends
`tests/orchestration/test_preview_control.py` and `tests/ui_server/test_command_channel.py` and adds
the NEW FILE at `tests/ui_server/test_preview_commands.py`. `worker_tests.diff` adds the
NEW FILE at `tests/orchestration/test_preview_worker.py`.

THE SPECIFICATION — the tests are the acceptance; these clauses fix what they leave open.
S1 `packages/orchestration/preview_control.py`: `preview_view` answers `url` and `port` only when
   the state is `live`, else "" and 0. New, each with a docstring: `mark_viewed(job_id, *, now,
   data_root=None)` sets `viewed_at` of a live record to `now.isoformat()` and persists it, and
   leaves any other record unwritten; `idle_stop_due(record, *, now, ttl_seconds) -> bool`, false
   unless the state is live and `ttl_seconds > 0`, true when `viewed_at` (else `updated_at`) is
   `ttl_seconds` or more before `now`, and true when neither parses; `stop_if_idle(job, runner, *,
   now, ttl_seconds, data_root=None)`, which when due runs `stop` and settles `stopped` with the
   reason "stopped after <ttl_seconds> seconds without a viewer", or `failed` with "could not
   stop: <message>"; and `revalidate_live(job, runner, *, now, data_root=None)`, which for a live
   record runs `probe`, keeps the record untouched when it is ok, and otherwise runs `stop` and
   settles `failed` with "the app stopped answering: <message>". Settling clears the link and the
   request and stamps `updated_at`, as the module's existing settle does. Nothing else changes.
S2 `packages/orchestration/preview_worker.py`, NEW, module docstring naming F041 T002 and DECISION
   F041 D4. `PREVIEW_TICK_SECONDS = 15`; class `PreviewWorker(*, ttl_seconds, runner=None,
   load_job=None, clock=None, data_root=None)`: `runner` None means `preview_runner.
   run_runtime_verb` looked up on the module at each call; `load_job` None means
   `pingpong_job.load_job_plan`; `clock` None means the current UTC time. Members: `live_jobs` (a
   frozenset property), `submit(job_id)` (queues once, wakes the thread, runs nothing),
   `adopt_live()` (every `<jobs dir>/*/preview.json` whose record is live), `step()` (D4 (2): the
   queued requests with `run_pending`, then for each other live job `stop_if_idle` and, while
   still live, `revalidate_live`; a job `load_job` answers None for leaves the live set),
   `stop_all()` (records a stop for each live job and runs it), `start(tick_seconds=
   PREVIEW_TICK_SECONDS)` (one daemon thread named `remedy-preview-worker` that steps, then waits
   on the wake event up to `tick_seconds`, until stopped) and `close(timeout=5.0)` (stops and
   joins the thread, then `stop_all`). A lock guards the queue and the live set.
S3 `packages/orchestration/ui_server.py`: `JOB_PREVIEW_START_COMMAND_ID = "job.preview-start"`,
   `JOB_PREVIEW_STOP_COMMAND_ID = "job.preview-stop"` and `JOB_PREVIEW_COMMAND_IDS` beside the other
   ids; a class attribute `preview_worker: Any = None` on `_RemedyHandler`; a door clause, placed
   directly before the `job.veto-task` clause, taking the D18 order of the `job.stop` clause with
   no declining branch; `_dispatch_job_preview(self, job, payload)`, placed directly before
   `_dispatch_job_pause`, importing `datetime`, `timezone` and `request_preview` in its body and
   answering `{"command": ..., "outcome": "accepted", "state": <the recorded state>}` after
   calling `self.preview_worker.submit(job_id)` when a worker is set; `_build_preview_json(job)`
   after `_build_artifacts_json`, calling `mark_viewed` then answering `preview_view`, registered
   as `"preview"` in `do_GET`'s `handlers` dict after `"artifacts"`; and in `start_ui_server`, a
   `PreviewWorker(ttl_seconds=int(get_config().get("preview.idle_ttl_seconds")))` created before
   the handler class and bound on it as `preview_worker`, `adopt_live()` and `start()` called
   directly after the `ThreadingHTTPServer` is created, and `close()` called in the `finally` after
   `server_close()`. Each addition carries a comment or docstring naming DECISION F041 D4.

BUNDLE — the commits are C1a, C1b, C1c, C2, C3, C4, C5 and C6, in this order.

C1a — `.agent/authored/f041-r4-block.md` := this block, and `.agent/authored/f041-r4-plan.md`,
  `.agent/authored/f041-r4-records.diff` and `.agent/authored/f041-r4-wiring.diff` := plan.md,
  records.diff and wiring.diff, by `shutil.copyfile`.
  Subject: `F041 R4 C1a: copy round 4 block, plan, records and wiring into .agent/authored/`
  Its insertions are this block's line count plus 116.
C1b — `.agent/authored/f041-r4-tests.diff` := tests.diff.
  Subject: `F041 R4 C1b: copy round 4 tests diff into .agent/authored/`
  Expected insertions: 297.
C1c — `.agent/authored/f041-r4-worker_tests.diff` := worker_tests.diff.
  Subject: `F041 R4 C1c: copy round 4 worker tests diff into .agent/authored/`
  Expected insertions: 217.
C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F041 R4 C2: book round 3, record D4`
  Expected by `git show --numstat` (insertions and deletions): 10/0 .agent/decisions.md, 2/0 .agent/live_review.md, 7/7 .agent/plan.md.
C3 — THE CODE: S1 to S3 and `git apply` wiring.diff, in one commit. The wiring paths' numstat is
  expected as 4/0 apps/cli/command_catalog.py, 1/0 docs/guides/environment.md, 10/0 packages/orchestration/config.py, 1/0 tests/orchestration/import_reachability_allowlist.txt. IF THIS COMMIT WOULD REACH 500 INSERTIONS, split it at this point and no
  other: C3a = S1 alone, C3b = everything else of C3, and say which you did.
  Subject: `F041 R4 C3: take preview requests at the door and act on them on the server's worker`
  (a split uses the same subject with `C3a` and `C3b`).
C4 — THE TESTS: `git apply` tests.diff, then `git apply` worker_tests.diff, in one commit.
  Subject: `F041 R4 C4: add the reviewer's door, worker, view and idle-stop tests`
  Expected by `git show --numstat`: 93/0 tests/orchestration/test_preview_control.py, 211/0 tests/orchestration/test_preview_worker.py, 9/2 tests/ui_server/test_command_channel.py, 128/0 tests/ui_server/test_preview_commands.py.
C5 — THE TOOL: your mutation tool (G4) saved as `.agent/authored/f041-r4-mutations.py`.
  Subject: `F041 R4 C5: add the round 4 mutation tool`
C6 — THE HANDBACK: `.agent/handoff.md`, rewritten, its own commit, per
  `docs/agents/handback_template.md`. Subject: `F041 R4 C6: rewrite handoff for round 4`
  Then `git push`. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; C3's own clause
   names its one split point.
3. The round's whole tracked path set is: the `.agent/authored/f041-r4-*` copies and tool, the
   paths the four diffs edit, `.agent/plan.md`, `packages/orchestration/preview_control.py`,
   `packages/orchestration/preview_worker.py`, `packages/orchestration/ui_server.py`, and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only 468b3a36e` at the
   branch tip after C6. Do NOT touch `apps/ui/`, `packages/runtimes/`,
   `apps/cli/commands/runtime_cmd.py`, `packages/orchestration/preview_runner.py`,
   `.agent/context.md`, `.agent/candidates.md`, `.agent/operator_questions.md` or `README.md`.
4. Every test the payloads carry passes against your code unedited, at C4.
5. You write no `Done:` line and no `Landed:` line.
6. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. An EXISTING test that goes red is never edited to pass.
   A fix to your own code after it is committed is its own declared commit, never a rewrite.
7. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch
   deletion, no force-push, no `git stash`, and no reset of a pushed commit.
8. Leave every worktree already listed at your step 4, its branch, and every existing stash
   alone. The worktree G4 adds goes under `.remedy-wt/`, is removed as that gate's last action,
   and `git worktree list | wc -l` is reported afterwards.
9. DO NOT run the full suite (amend0917 rule 1). Run no self-use job, no command that calls a
   provider, and never a preview or `remedy runtime serve` against a real project.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G4 run before C6 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f041-r4-*` payload copy byte for
 byte with its source, read back with `git show <commit>:<path>` from the commit that added it.

G2 THE RECORDS, THE WIRING AND THE TESTS — the sha256 of each file below, read with
 `git show <commit>:<path>` at the commit named (C3 meaning C3b if you split), equals the
 reviewer's reading from its simulation tree:
 | path | at | bytes | sha256 |
 |---|---|---|---|
 | .agent/decisions.md | C2 | 2462820 | 25b48dbd47231ba1195c57cce37d5a82f84cef5f73609bd4809f8fc7e046c105 |
 | .agent/live_review.md | C2 | 302538 | 2725e3e6b068a32048e1965b3027aa255a9c339d5b2c6ecd2b87c07db13cfec4 |
 | .agent/plan.md | C2 | 918 | e5c186ceb181bd44b681b8433bc6ab01b69332165a7d3db2608fb1e4cc48f372 |
 | apps/cli/command_catalog.py | C3 | 134399 | 38833ea8236d72035ba33baa9e5bf22b97ecb4c21af70f290f1e339c3ff0657a |
 | packages/orchestration/config.py | C3 | 65646 | 56b99a8b1e28be2e946894ed7acc62bce3aa7c9b91a980d0d06ff3bf113c52b9 |
 | docs/guides/environment.md | C3 | 22844 | fe87ae0aa810ac9f7a51bcac2d04ad080809be71e8238e5ca779da54d53adca0 |
 | tests/orchestration/import_reachability_allowlist.txt | C3 | 11168 | 114fbf717811e1df30368ae4b5374fc3ea476617cbf95c14f9cb00d23a709130 |
 | tests/orchestration/test_preview_control.py | C4 | 13036 | fbc079a6afd3e85b77b3593c5f60752500b1eb719b1968f1a31e4002d4b9529f |
 | tests/ui_server/test_command_channel.py | C4 | 103698 | 2d3d83136c5782e75a4c7b652182f26aa7b32b651471fb5ab286c71dfe50f722 |
 | tests/orchestration/test_preview_worker.py | C4 | 7837 | efb391ed28cb9bbd13e3c75b125c530a9eaac7fb743fd40c5d42dd28c35d6e69 |
 | tests/ui_server/test_preview_commands.py | C4 | 5602 | a11c71701aac2e496aa28acf18e3a67bfac9dd5bd4909506260aeac0b6e8f0e0 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT read with `git show`, at `468b3a36e` and at
 C2 (the reviewer read `[]` at both).

G3 THE CODE AND THE TESTS — `python3 -m ruff check packages/orchestration/preview_control.py
 packages/orchestration/preview_worker.py packages/orchestration/ui_server.py
 packages/orchestration/config.py apps/cli/command_catalog.py
 tests/orchestration/test_preview_control.py tests/orchestration/test_preview_worker.py
 tests/ui_server/test_preview_commands.py tests/ui_server/test_command_channel.py
 .agent/authored/f041-r4-mutations.py` at C5, with its real exit code. Report the diff of the
 three code files at C3 (C3a and C3b), whole. Then, in the primary checkout at C5, SERIALLY (it
 takes about ten minutes):
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_preview_control.py tests/orchestration/test_preview_worker.py tests/ui_server tests/cli tests/docs tests/orchestration/test_config.py tests/orchestration/test_env_registry.py tests/test_subprocess_timeouts.py tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py 2>&1 | tail -6; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran it serially in its simulation tree, which carries C2, the wiring, the tests and
 its own version of S1 to S3 but no `.agent/authored/f041-r4-*` copy and no
 `apps/ui/node_modules`, and read `3453 passed, 2 skipped` at real exit code 0, the skips being
 `tests/test_agent_tooling.py:43`, the D12 quarantine, and `tests/ui_server/test_timeline_scrub_live.py:31`,
 which runs where `apps/ui/node_modules` exists, as it does in the primary checkout. Report your
 count and every `SKIPPED` line, and the node counts of `tests/orchestration/test_preview_control.py`,
 `tests/orchestration/test_preview_worker.py` and `tests/ui_server/test_preview_commands.py` by
 `--collect-only -q` (the reviewer's read 29, 11 and 3). Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0.

G4 THE RED PROOFS — your tool `.agent/authored/f041-r4-mutations.py` takes a worktree path, and
 for each mutation below edits the named production file INSIDE that worktree (asserting its FROM
 text occurs exactly once there), runs `python3 -B -m pytest -q -p no:cacheprovider <the test file
 named>` with the worktree as the working directory and its root first on `PYTHONPATH` (through
 `subprocess.run(..., env=...)`), restores the bytes, and prints one line per mutation: its label,
 the exit code and the failed count. A mutation counts as caught only at exit code 1 with at
 least one failed test: a collection error is a broken edit, not a reading, and you repair the
 edit. It runs an unmutated control of each test file the mutations name first and last, reports
 `restored byte-identical: True` after each restore, and ends with
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each is a real behaviour change:
  q1 `preview_view` answers the stored link in every state (test_preview_control.py);
  q2 `mark_viewed` writes a record that is not live (same file);
  q3 `idle_stop_due` expires a preview whose ttl is zero or less (same file);
  q4 `revalidate_live` no longer stops a preview that stopped answering (same file);
  q5 `step` no longer revalidates a live preview (test_preview_worker.py);
  q6 `close` no longer stops the previews the worker keeps live (same file);
  q7 the door no longer hands the job to the worker (tests/ui_server/test_preview_commands.py);
  q8 `adopt_live` takes on a record whatever its state (test_preview_worker.py).
 Run it: `git worktree add --detach .remedy-wt/f041-r4-mut <C5>`, then
 `python3 -B .agent/authored/f041-r4-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f041-r4-mut`
 and report its whole output. EVERY mutation must be caught; one that stays green is reported as
 green and you STOP, because the tests are the reviewer's. Then
 `git worktree remove --force .remedy-wt/f041-r4-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.

G5 TREE AND PUSH — after C6: `git status --porcelain`, which must be empty;
 `git log --oneline -n 9` (one more if C3 was split), which must show C6, C5, C4, C3, C2, C1c,
 C1b, C1a and `468b3a36e` in that order; `git worktree list | wc -l`, which must equal your step 4
 reading; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C6 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for the code files and C5),
every gate's real output and exit code, the authored-text proofs, the item-status table AGENTS.md
requires (one row per commit and per gate), the deviations, and the next expected action. Your
Session section reads SESSION 1 of feature F041, round 4, and says in one sentence how much
context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 4, then T003 (the preview panel, the lightbox and the app card). State the open-findings
count, 0, and the operator-questions count, 1.

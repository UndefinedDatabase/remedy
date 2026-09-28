STEP F038 R6 — BOOK ROUND 5, THEN SEND A CONFIRMED CARD THROUGH THE WRITE DOOR: the chat posts to a running cockpit's door, so the door's own checks, nonce and audit line apply unchanged

GOAL
Round 5 is reviewed PASS at `8b01ece3`. Book it, record DECISION F038 D7, and land a NEW module
`packages/orchestration/chat_door.py`: `send_card_through_door` takes a card built by
`packages/orchestration/chat_intent.py`, refuses one that is not confirmable before anything is
sent, and posts the door's own request body to `POST /api/jobs/<id>/commands` of a running
cockpit on `127.0.0.1`, with the two credentials the browser sends. It answers the door's status
and JSON body. It writes no file itself: the door's audit line is the record. Nothing imports the
new module yet.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests yourself against S1 to S5 below. Only the `.agent/` records travel
as payloads. Read DECISION F038 D7 in the records diff before you write code: it is the design
this specification implements. Before you write anything, read whole:
`packages/orchestration/chat_intent.py`; `is_safe_id` in `packages/orchestration/safe_points.py`;
`COMMAND_CSRF_HEADER`, `_handle_command_submission`, `_bearer_token_accepted` and
`start_ui_server` in `packages/orchestration/ui_server.py`; `AUDIT_FILENAME` in
`packages/orchestration/command_audit.py`; `pause_requested` in
`packages/orchestration/pause_control.py`; `tests/ui_server/test_steer_task_door.py` (its
`_start_ui_server_for_job` and its job fixture are the model for yours);
`tests/ui_server/server_start.py`; and `tests/test_no_orphan_modules.py`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f038-r6-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f038-r6/`           READ-ONLY. The reviewer's block.
  every other `.remedy-wt/f038-*` directory except your own, and `.remedy-wt/f038-review/`
                                  The reviewer's; do not touch them.
  `.remedy-wt/f038-r6-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Set `REMEDY_DATA_DIR` inside tests with `monkeypatch.setenv`, never on a command line.
Never run npm or npx.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f038-grounded-chat`, and `git log --oneline -1` must read `8b01ece36`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f038-r6/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f038-r6-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 56 | 11850 | ac3a728650801700d78140df6647bd36af764b32e09d23defd0fd6ef6f703e65 |
| plan.md | 29 | 974 | 070a1ab0544c826e8b30e140ff521574222877171f737dd31a0291c154b9a37d |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `8b01ece3` into which it wrote the edits. It
appends round 5's gate entry to `.agent/live_review.md` and DECISION F038 D7 to
`.agent/decisions.md`.

THE SPECIFICATION, a NEW FILE at `packages/orchestration/chat_door.py`. No `except Exception`
anywhere and no `# noqa: BLE001`.
S1 THE MODULE. A docstring naming F038 T002 and DECISION F038 D7, with one sentence stating that
   Remedy deliberately does not let the chat run a command's effect itself. At module level it
   imports the standard library and, from `packages.orchestration`, only `chat_intent`
   (`ChatActionCard`, `ChatIntentError`, `card_command_payload`) and `safe_points.is_safe_id`.
   `COMMAND_CSRF_HEADER` is imported from `packages.orchestration.ui_server` INSIDE the send
   function, the idiom `ui_server.py` itself uses for heavy imports; nothing is imported from
   `apps`. Constants `CHAT_DOOR_HOST = "127.0.0.1"` and `CHAT_DOOR_TIMEOUT_S = 10.0`.
S2 THE ANSWER. A frozen dataclass `ChatDoorAnswer(status: int, body: dict[str, Any] = <empty>)`
   with a property `accepted`, true exactly when `status == 200`.
S3 THE SEND. `send_card_through_door(card, *, job_id, client_nonce, port, token) ->
   ChatDoorAnswer`, in this order, raising `ChatIntentError` before any connection is opened:
   (a) the body is `card_command_payload(card, client_nonce=client_nonce)`, so a card that is not
   confirmable or a nonce the door would refuse raises with that function's own message;
   (b) a `job_id` that `is_safe_id` refuses raises with a message containing `job_id`;
   (c) a `port` that is not an `int`, is a `bool`, or is outside 1 to 65535 raises with a message
   containing `port`; (d) an empty `token` raises with a message containing `token`.
   Then ONE `http.client.HTTPConnection(CHAT_DOOR_HOST, port, timeout=CHAT_DOOR_TIMEOUT_S)` sends
   `POST /api/jobs/<job_id>/commands` with the body as JSON and exactly the headers
   `Authorization: Bearer <token>`, `<COMMAND_CSRF_HEADER>: <token>` and
   `Content-Type: application/json`; the connection is closed in a `finally`. The answer is the
   response's status and its body parsed as JSON, or `{}` when the body is not JSON or not a JSON
   object. An `OSError` from the connection (no cockpit listening) is NOT caught: it reaches the
   caller, which the chat command will turn into a sentence in a later round.
S4 NO FILE. The module opens no file and writes nothing; every record of a send is the door's.
S5 THE GUARD. In `ALLOWED_UNWIRED` of `tests/test_no_orphan_modules.py`, the
   `packages/orchestration/chat_intent.py` entry is REPLACED, in the same place, by
   `("packages/orchestration/chat_door.py", "F038's send of a confirmed chat card through the
   write door; the chat command wires it in a later round (DECISION F038 D7) and removes this
   line")`, split over lines as its neighbours are. `chat_intent.py` is imported by the new
   module, so `test_every_allowed_unwired_entry_is_a_live_orphan` reds on its old line — the
   reviewer measured exactly that. Nothing else in that file changes.

THE TESTS — a NEW FILE `tests/orchestration/test_chat_door.py`; no existing test changes. A
fixture sets `REMEDY_DATA_DIR` to `tmp_path`, saves a RUNNING job with one task
(`flight_task("T1")` from `tests.orchestration.test_dag_schedule`, as the steer door's test
does), starts a real server in a thread as `_start_ui_server_for_job` in
`tests/ui_server/test_steer_task_door.py` does, and reads the audit file at
`tmp_path / "control" / "jobs" / <job_id> / AUDIT_FILENAME`. Every card is built by
`parse_chat_intent` and `build_action_card`, never by hand. At least, one each: before any send
the audit file is absent; a "pause" card sent answers 200, `accepted` true, body `command`
`job.pause`, the audit file holds exactly one line whose `command`, `nonce` and `outcome` are
`job.pause`, the nonce sent and `accepted`, and `pause_requested(job_id)` is no longer None; the
same card sent twice with one nonce answers the same status and body both times and the audit
outcomes read `accepted` then `replayed`; "tell the builder: use X" with the task focused answers
200 with `command` `job.steer` and that `task_id`; "note: keep it small" with no focus answers
200 with `command` `chat.send`; a wrong token answers 403 with `accepted` false; a "veto it"
card, which is not confirmable, raises `ChatIntentError` and the audit file stays absent; a
`job_id` of `../x`, a port of 0, of 70000 and of `True`, and an empty token each raise
`ChatIntentError` with the audit file still absent.

BUNDLE — the commits are C1a, C1b, C2, C3, C4 and C5, in this order.

C1a — copy this block and the plan payload
  `.agent/authored/f038-r6-block.md` := this block and `.agent/authored/f038-r6-plan.md` :=
  plan.md, by `shutil.copyfile`.
  Subject: `F038 R6 C1a: copy round 6 block and plan payload into .agent/authored/`
  Its insertions are this block's line count plus 29. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C1b — copy the records diff
  `.agent/authored/f038-r6-records.diff` := records.diff.
  Subject: `F038 R6 C1b: copy round 6 records diff into .agent/authored/`
  Expected insertions: 56.

C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F038 R6 C2: book round 5 and record DECISION F038 D7`
  Expected by `git show --numstat` (insertions and deletions): 38/0 decisions.md, 2/0
  live_review.md, 7/7 plan.md.

C3 — THE CODE: `packages/orchestration/chat_door.py` and S5's replacement.
  Subject: `F038 R6 C3: send a confirmed chat card through the cockpit's write door`

C4 — THE TESTS AND THE TOOL: `tests/orchestration/test_chat_door.py` and your mutation tool (G5)
  saved as `.agent/authored/f038-r6-mutations.py`.
  Subject: `F038 R6 C4: test the door send, its refusals and its audit line`

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F038 R6 C5: rewrite handoff for round 6`
  Then `git push origin feature/f038-grounded-chat`. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects (C4a and C4b), and say so.
3. The round's whole tracked path set is: the `.agent/authored/f038-r6-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `packages/orchestration/chat_door.py`, `tests/test_no_orphan_modules.py`,
   `tests/orchestration/test_chat_door.py`, and `.agent/handoff.md`. Report the list you measure
   with `git diff --name-only 8b01ece36` at the branch tip after C5. Do NOT touch anything under
   `apps/` or `docs/`, any other file under `packages/`, `README.md`,
   `tests/orchestration/import_reachability_allowlist.txt`, `.agent/context.md`,
   `.agent/prose_slips.md`, `.agent/candidates.md` or `.agent/operator_questions.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong, or this round's own mutation tool, may be corrected before C5 in a
   new commit, and the correction is declared. An EXISTING test that goes red is never edited to
   pass; report it and stop.
5. NOTHING IS MERGED OR REWRITTEN, AND NOTHING IS SENT OUTSIDE THE TESTS. No `gh pr merge`, no
   `gh pr create`, no checkout of `main`, no branch deletion, no force-push, no `git stash`, no
   request to any server this round's tests did not start themselves, and no `git commit --amend`
   or any other rewrite of a commit, pushed or not: a wrong commit subject is declared, never
   amended.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F038's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f038-r6-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f038-r6/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree. Report each path beside the hash you read:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2397195 | 00c4a36ebadb5091bb5ea9b910668eb3def49f8e6c7c2ff56f5e2605d66d68fd |
 | .agent/live_review.md | 323385 | 2e6b9eed1c6354f9a04842acfb10093e1a10d84ecd6b701a8d8e38269fd724e0 |
 | .agent/plan.md | 974 | 070a1ab0544c826e8b30e140ff521574222877171f737dd31a0291c154b9a37d |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT read with `git show <C2>:<path>` (the
 reviewer read `[]`); and `git diff --name-only <C1b> <C2>`, which must name exactly the paths of
 the table above.

G3 THE CODE — `python3 -m ruff check packages/orchestration/chat_door.py
 tests/orchestration/test_chat_door.py tests/test_no_orphan_modules.py` at C4, with its real exit
 code. Then report, quoted from `git show <C3>`, the whole of `send_card_through_door` and
 `ChatDoorAnswer`.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_chat_door.py tests/orchestration/test_chat_intent.py tests/orchestration/test_chat_answer.py tests/orchestration/test_chat_evidence.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_subprocess_timeouts.py tests/regression/test_named_bugs.py tests/test_path_utils.py tests/test_data_paths.py tests/orchestration/test_env_registry.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py tests/ui_server/test_command_channel.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/cli/test_golden_path.py 2>&1 | tail -9; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection, less `tests/orchestration/test_chat_door.py`, serially in the
 primary checkout at `8b01ece36` and read `611 passed, 6 skipped` at exit code 0, the six skips
 being the F252 quarantine; over its simulation tree, a fresh worktree carrying this round's
 records and its own version of the code and tests, the whole selection read
 `621 passed, 7 skipped` at exit code 0, the further skip being a vitest test of
 `tests/orchestration/test_test_runner.py`, which runs in the primary checkout. Report the node
 count of `tests/orchestration/test_chat_door.py` by `--collect-only -q` at C4, every `SKIPPED`
 line and the summary, and account for any difference from 611 passed by that count. Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0.

G5 THE RED PROOFS — your tool `.agent/authored/f038-r6-mutations.py` takes a worktree path, and
 for each mutation below edits `packages/orchestration/chat_door.py` INSIDE that worktree
 (asserting its FROM text occurs exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider
 -rf tests/orchestration/test_chat_door.py` from the worktree's root after purging its
 `__pycache__` directories, with the worktree's root first on `PYTHONPATH`, restores the bytes,
 and prints one line per mutation: its label, the exit code, the failed count and the failing
 node ids, both read from the `FAILED` lines `-rf` prints. It runs an unmutated control first and
 last and ends with `restored byte-identical: True` and a final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each is a real behaviour change:
  r1 the CSRF header is not sent;
  r2 the `Authorization` header is not sent;
  r3 a card that is not confirmable is sent anyway, its body built without
     `card_command_payload`;
  r4 the job id is not checked;
  r5 the port is not checked;
  r6 the token is not checked;
  r7 every answer reads as accepted;
  r8 the nonce sent is a fixed string rather than the one given.
 Run it: `git worktree add --detach .remedy-wt/f038-r6-mut <C4>`, then
 `python3 -B .agent/authored/f038-r6-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f038-r6-mut`
 and report its whole output. EVERY mutation must be red with at least one failing node; a
 mutation that stays green is reported as green, never papered over, and you then add the test
 that catches it in a commit before C5 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f038-r6-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 7`, which must show C5, C4, C3, C2, C1b, C1a and `8b01ece36` in that
 order (more lines if a commit was split or a declared correction added); `git worktree list |
 wc -l`, which must equal your step 4 reading; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3 and C4 — report what you
measure), every gate's real output and exit code, the authored-text proofs, the item-status table
AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected
action. Report what you ran, not what you expected to find. Your Session section reads SESSION 2
of feature F038, round 6, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 6, then T002's last part: a model-written parse for the exposed commands a sentence cannot
fill, behind `chat.model_written`, off by default. State the open-findings count, 0, and the
operator-questions count, 1.

STEP F038 R5 — BOOK ROUND 4, THEN LAND T002's FIRST HALF: the mechanical intent parse, the action card and the write door's request body, with nothing sent

GOAL
Round 4 is reviewed PASS at `8aff505d`. Book it, record DECISION F038 D6, and land a NEW module
`packages/orchestration/chat_intent.py`: a typed request becomes a QUESTION for the read path, an
ACTION for exactly one command of `UI_EXPOSED_COMMANDS` — stop, pause, resume, a note to the
builder, veto or rerun — or UNKNOWN; an action becomes a card a person confirms, stating what it
would send and asking for what is missing; and only a complete card yields the write door's
request body, in the door's own argument names. Nothing is sent, no file is written, no model is
called, and nothing imports the new module.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests yourself against S1 to S6 below. Only the `.agent/` records travel
as payloads. Read DECISION F038 D6 in the records diff before you write code: it is the design
this specification implements. Before you write anything, read whole: `UI_EXPOSED_COMMANDS` in
`apps/cli/command_catalog.py`; `nonce_is_valid` in `packages/orchestration/command_nonce.py`;
`_read_command_payload` and the `job.stop`, `job.pause`, `job.unpause`, `job.veto-task`,
`job.steer`, `chat.send` and `job.rerun-subtree` branches of `_handle_command_submission` in
`packages/orchestration/ui_server.py`; `apps/ui/src/api/steeringSend.ts`; and
`tests/test_no_orphan_modules.py`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f038-r5-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f038-r5/`           READ-ONLY. The reviewer's block.
  every other `.remedy-wt/f038-*` directory except your own, and `.remedy-wt/f038-review/`
                                  The reviewer's; do not touch them.
  `.remedy-wt/f038-r5-worker/`    YOURS for logs and scripts; create it if absent. All are
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
   `feature/f038-grounded-chat`, and `git log --oneline -1` must read `8aff505d6`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f038-r5/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f038-r5-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 63 | 13152 | 6a5d4a2f8afdb1269d1e720ccc0a9b6e4081cdc7ad846f358b64efa9a00b5ebf |
| plan.md | 29 | 974 | 571c99b525980bfcbdd99259e3aba263928f043be52321dd738602a68f1b2565 |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `8aff505d` into which it wrote the edits. It
appends round 4's gate entry to `.agent/live_review.md` and DECISION F038 D6 to
`.agent/decisions.md`.

THE SPECIFICATION, a NEW FILE at `packages/orchestration/chat_intent.py`. No `except Exception`
anywhere and no `# noqa: BLE001`.
S1 THE MODULE. A docstring naming F038 T002 and DECISION F038 D6, with one sentence stating that
   Remedy deliberately does not let the chat act on its own. At module level it imports the
   standard library and, from `packages.orchestration`, only `command_nonce.nonce_is_valid` —
   nothing from `apps`, `ui_server` or any other package module. Constants
   `CHAT_INTENT_QUESTION = "question"`, `CHAT_INTENT_ACTION = "action"`,
   `CHAT_INTENT_UNKNOWN = "unknown"`, `CHAT_UNKNOWN_TITLE = "I can't do that yet"`,
   `CHAT_AVAILABLE_ACTIONS = ("stop", "pause", "resume", "a note to the builder", "veto",
   "rerun")`, `CHAT_VERB_REQUIRED_ARGS`, a dict in this order — `job.stop` (), `job.pause` (),
   `job.unpause` (), `job.steer` ("task_id", "message"), `chat.send` ("message",),
   `job.veto-task` ("task_id", "reason"), `job.rerun-subtree` ("task_id",) — and
   `CHAT_VERB_TITLES` over the same keys: "Stop the job", "Pause the job", "Resume the job",
   "Send a note to the task's builder", "Send a message to the job", "Veto the task", "Rerun the
   task and the tasks after it". `class ChatIntentError(ValueError)`.
S2 THE SHAPES. Frozen dataclasses `ChatIntent(kind: str, verb: str = "", args: dict[str, str] =
   <empty>, missing: tuple[str, ...] = ())` and `ChatActionCard(verb: str, title: str, lines:
   tuple[str, ...], args: dict[str, str], missing: tuple[str, ...], confirmable: bool)`. An
   action's `args` keeps only its non-empty values; its `missing` lists, in the verb's order, the
   required names whose value is empty.
S3 THE PARSE. `parse_chat_intent(text, *, focused_task_id="") -> ChatIntent`. Fold the text's
   whitespace runs to single spaces and strip it; drop a leading `please ` (any case). An empty
   result is UNKNOWN. A result that ends with `?`, or whose lower-cased form starts with one of the
   whole words what, why, how, when, where, which, who, did, does, do, is, are, was, were, can,
   could, has, have, is a QUESTION with no verb. Otherwise, by the lower-cased first word, the
   first rule that matches decides; "the reason" is the text after the first whole word `because`,
   stripped, or empty: stop, cancel or abort → `job.stop` with `reason`; pause → `job.pause`;
   resume, unpause or continue → `job.unpause`; a text starting with `tell the builder`, `tell it`,
   `note` or `steer` as whole words, then any run of spaces, `:` or `,`, is a note whose message
   is the rest, in the writer's own case → `job.steer` with `task_id` = the focused task and
   `message` when a task is focused, else `chat.send` with `message`; veto, skip or drop →
   `job.veto-task` with `task_id` = the focused task and `reason`; rerun or retry, or a text
   starting with `run again` → `job.rerun-subtree` with `task_id` = the focused task. Anything
   else is UNKNOWN.
S4 THE CARD. `build_action_card(intent, *, job_id) -> ChatActionCard`. A QUESTION raises
   `ChatIntentError` with a message containing `read path`. An UNKNOWN intent gives verb "",
   title `CHAT_UNKNOWN_TITLE`, the one line `Available: stop, pause, resume, a note to the
   builder, veto, rerun.` (from the constant), no args, nothing missing, not confirmable. An
   ACTION gives its verb, its title, and the lines `Job: <job_id>`; then `Task: <task_id>`,
   `Message: <message>` and `Reason: <reason>`, each only when present, in that order; then, when
   anything is missing, `Needs: <names joined by ", ">. Say it again with them.`; then
   `Command: <verb>`. It is confirmable exactly when nothing is missing.
S5 THE PAYLOAD. `card_command_payload(card, *, client_nonce) -> dict` answers
   `{"command": card.verb, "client_nonce": client_nonce, "args": <a copy of card.args>}`. A card
   that is not confirmable raises `ChatIntentError` with a message containing `no command`; a
   nonce `nonce_is_valid` refuses raises it with a message containing `client_nonce`.
S6 THE GUARD. `ALLOWED_UNWIRED` in `tests/test_no_orphan_modules.py` gains, between the
   `chat_answer.py` and `ci_budgets.py` entries, `("packages/orchestration/chat_intent.py",
   "F038's intent parse, action cards and their door payload; the chat command wires it in a later
   round (DECISION F038 D6) and removes this line")`, split over lines as its neighbours are.
   Nothing else in that file changes.

THE TESTS — a NEW FILE `tests/orchestration/test_chat_intent.py`, `REMEDY_DATA_DIR` under
`tmp_path`; no existing test changes. At least, one each: every key of `CHAT_VERB_REQUIRED_ARGS` is
in `UI_EXPOSED_COMMANDS` (imported in the test from `apps.cli.command_catalog`) and
`CHAT_VERB_TITLES` has the same keys; "What changed?", "did the tests pass", "Can you stop it?",
"  why  " and "stop it?" are each a question; "Stop the job because it loops" is `job.stop` with
reason "it loops", "please cancel" is `job.stop` with no args, "Pause" is `job.pause`, and
"resume", "Unpause now" and "continue" are `job.unpause`; "Tell the builder: use the New API"
with focus `abc` is `job.steer` with `task_id` "abc" and `message` "use the New API", "note: keep
it small" with no focus is `chat.send`, and "tell it" is `chat.send` missing `message`; "Veto this
because it is out of scope" with focus is complete, "skip this task" with focus misses `reason`,
"veto it" without focus misses `task_id` and `reason`, "rerun" with focus is complete and "Run
again" without focus misses `task_id`; "deploy to production", "" and "   " are unknown; the note
card's lines are exactly `Job: J1`, `Task: abc`, `Message: use X`, `Command: job.steer` and it is
confirmable; the focused "veto" card's lines are exactly `Job: J1`, `Task: abc`, `Needs: reason.
Say it again with them.`, `Command: job.veto-task` and it is not confirmable; the unknown card is
titled and lined as S4 states; a question card raises; a stop card's payload is exactly
`{"command": "job.stop", "client_nonce": "chat-1", "args": {"reason": "done"}}`, a bad nonce and
an incomplete or unknown card each raise; and parsing and building cards writes no file under
`tmp_path`.

BUNDLE — the commits are C1a, C1b, C2, C3, C4 and C5, in this order.

C1a — copy this block and the plan payload
  `.agent/authored/f038-r5-block.md` := this block and `.agent/authored/f038-r5-plan.md` :=
  plan.md, by `shutil.copyfile`.
  Subject: `F038 R5 C1a: copy round 5 block and plan payload into .agent/authored/`
  Its insertions are this block's line count plus 29. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C1b — copy the records diff
  `.agent/authored/f038-r5-records.diff` := records.diff.
  Subject: `F038 R5 C1b: copy round 5 records diff into .agent/authored/`
  Expected insertions: 63.

C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F038 R5 C2: book round 4 and record DECISION F038 D6`
  Expected by `git show --numstat` (insertions and deletions): 45/0 decisions.md, 2/0
  live_review.md, 6/5 plan.md.

C3 — THE CODE: `packages/orchestration/chat_intent.py` and S6's line.
  Subject: `F038 R5 C3: parse a chat request into a question, an action card or unknown`

C4 — THE TESTS AND THE TOOL: `tests/orchestration/test_chat_intent.py` and your mutation tool (G5)
  saved as `.agent/authored/f038-r5-mutations.py`.
  Subject: `F038 R5 C4: test the intent parse, the cards and the door payload`

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F038 R5 C5: rewrite handoff for round 5`
  Then `git push origin feature/f038-grounded-chat`. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects (C4a and C4b), and say so.
3. The round's whole tracked path set is: the `.agent/authored/f038-r5-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `packages/orchestration/chat_intent.py`, `tests/test_no_orphan_modules.py`,
   `tests/orchestration/test_chat_intent.py`, and `.agent/handoff.md`. Report the list you measure
   with `git diff --name-only 8aff505d6` at the branch tip after C5. Do NOT touch anything under
   `apps/` or `docs/`, any other file under `packages/`, `README.md`,
   `tests/orchestration/import_reachability_allowlist.txt`, `.agent/context.md`,
   `.agent/prose_slips.md`, `.agent/candidates.md` or `.agent/operator_questions.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong may be corrected before C5, and the correction is declared. An
   EXISTING test that goes red is never edited to pass; report it and stop.
5. NOTHING IS MERGED, SENT OR REWRITTEN. No `gh pr merge`, no `gh pr create`, no checkout of
   `main`, no branch deletion, no force-push, no `git stash`, no request to any running server,
   and no `git commit --amend` or any other rewrite of a commit, pushed or not: a wrong commit
   subject is declared, never amended.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F038's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f038-r5-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f038-r5/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree. Report each path beside the hash you read:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2394024 | 8d4cbb3eb1c3b5efd266cbf632f376acfa1ce61825ef732b2e4626af76418c62 |
 | .agent/live_review.md | 320874 | 29156a4a862e8f4dff6ace0536ca125bab671ab28090cf6bcf394f0743625338 |
 | .agent/plan.md | 974 | 571c99b525980bfcbdd99259e3aba263928f043be52321dd738602a68f1b2565 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT read with `git show <C2>:<path>` (the
 reviewer read `[]`); and `git diff --name-only <C1b> <C2>`, which must name exactly the paths of
 the table above.

G3 THE CODE — `python3 -m ruff check packages/orchestration/chat_intent.py
 tests/orchestration/test_chat_intent.py tests/test_no_orphan_modules.py` at C4, with its real exit
 code. Then report, quoted from `git show <C3>`, the whole of `parse_chat_intent`,
 `build_action_card` and `card_command_payload`.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_chat_intent.py tests/orchestration/test_chat_answer.py tests/orchestration/test_chat_evidence.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_subprocess_timeouts.py tests/regression/test_named_bugs.py tests/test_path_utils.py tests/test_data_paths.py tests/orchestration/test_env_registry.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/cli/test_golden_path.py 2>&1 | tail -4; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection, less `tests/orchestration/test_chat_intent.py`, serially in the
 primary checkout at `8aff505d6` and read `468 passed, 6 skipped` at exit code 0, the six skips
 being the F252 quarantine; over its simulation tree, a fresh worktree carrying this round's
 records and its own version of the code and tests, the whole selection read
 `481 passed, 8 skipped` at exit code 0, the two further skips being the vitest tests of
 `tests/orchestration/test_test_runner.py`, which run in the primary checkout. Report the node
 count of `tests/orchestration/test_chat_intent.py` by `--collect-only -q` at C4, every `SKIPPED`
 line and the summary, and account for any difference from 468 passed by that count. Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0.

G5 THE RED PROOFS — your tool `.agent/authored/f038-r5-mutations.py` takes a worktree path, and
 for each mutation below edits `packages/orchestration/chat_intent.py` INSIDE that worktree
 (asserting its FROM text occurs exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider
 tests/orchestration/test_chat_intent.py` from the worktree's root after purging its
 `__pycache__` directories, with the worktree's root first on `PYTHONPATH`, restores the bytes,
 and prints one line per mutation: its label, the exit code, the failed count and the failing
 node ids. It runs an unmutated control first and last and ends with
 `restored byte-identical: True` and a final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each is a real behaviour change:
  r1 nothing is ever a question;
  r2 a text ending in `?` is a question only when it starts with a question word;
  r3 a note goes to the job even when a task is focused;
  r4 nothing is ever missing;
  r5 an unknown request is read as a question;
  r6 a card that is not confirmable still yields a payload;
  r7 the nonce is not checked;
  r8 the reason after `because` is never taken;
  r9 a note's message is lower-cased;
  r10 a leading `please ` is kept.
 Run it: `git worktree add --detach .remedy-wt/f038-r5-mut <C4>`, then
 `python3 -B .agent/authored/f038-r5-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f038-r5-mut`
 and report its whole output. EVERY mutation must be red with at least one failing node; a
 mutation that stays green is reported as green, never papered over, and you then add the test
 that catches it in C4 before C5 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f038-r5-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 7`, which must show C5, C4, C3, C2, C1b, C1a and `8aff505d6` in that
 order (more lines if constraint 2 split a commit); `git worktree list | wc -l`, which must equal
 your step 4 reading; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3 and C4 — report what you
measure), every gate's real output and exit code, the authored-text proofs, the item-status table
AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected
action. Report what you ran, not what you expected to find. Your Session section reads SESSION 1
of feature F038, round 5, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 5, then T002's second half: a confirmed card sent through the write door, and a
model-written parse for the verbs a sentence cannot fill. State the open-findings count, 0, and
the operator-questions count, 1.

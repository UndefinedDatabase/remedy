STEP F038 R9 — BOOK ROUND 8, RESOLVE R-1092, REGISTER AND REPAIR R-1093, THEN `remedy chat ask`: one line of the chat on the command line, a question answered with its evidence, a card sent through the running cockpit only once confirmed

GOAL
Round 8 is reviewed PASS at `72ba3b2e`, with R-1092 resolved and one Low finding, R-1093. Book them,
record DECISION F038 D10, repair R-1093 with one test, and land the subcommand `chat.ask`:
`remedy chat ask <job_id> "<text>" [--task <task id>] [--yes] [--json]` runs one chat turn; a
question prints its scope, its checked answer and its numbered evidence; a card prints its title
and lines and is sent through the job's running cockpit only when complete and confirmed by
`--yes` or a `y` typed on a terminal. The six chat modules become reachable from the command line.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict, never merge, and never write a `Done:` line. THE PRODUCTION CHANGE IS
SPECIFIED, NOT SLICED: you write the code and its tests yourself against S1 to S7 below. Only the
`.agent/` records travel as payloads. Read R-1093 and DECISION F038 D10 in the records diff before
you write code. Before you write anything, read whole: `apps/cli/commands/chat_cmd.py`;
`apps/cli/cost_preview_confirm.py` (the confirm idiom you follow); `apps/cli/commands/ui.py`; the
`chat.send` and `chat.show` entries of `apps/cli/command_catalog.py`; `run_chat_turn` in
`packages/orchestration/chat_turn.py`; `send_card_through_door` in
`packages/orchestration/chat_door.py`; `render_chat_answer` in
`packages/orchestration/chat_answer.py`; `docs/guides/exit-codes.md`; `tests/cli/test_chat_cmd.py`;
`tests/cli/test_exit_codes.py`; the meaning table of `docs/system/vocabulary.md` and
`tests/docs/test_vocabulary.py`; `tests/test_no_orphan_modules.py`; and
`tests/orchestration/test_import_reachability.py` with its allowlist.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f038-r9-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f038-r9/`           READ-ONLY. The reviewer's block.
  every other `.remedy-wt/f038-*` directory except your own, and `.remedy-wt/f038-review/`
                                  The reviewer's; do not touch them.
  `.remedy-wt/f038-r9-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace or a brace next to a quote is refused: write such a script to a file under your own
directory and run the file. Set environment variables inside tests with `monkeypatch.setenv`,
never on a command line. Never run npm or npx.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f038-grounded-chat`, and `git log --oneline -1` must read `7627663b7`, the session-2
   STOP handoff, which changed only `.agent/handoff.md` over `72ba3b2e5`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f038-r9/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f038-r9-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 60 | 9723 | 5f5de100d2694da50402517b6b6b48c71c7d7f305bf5fd64f296a1b3a0bd1cb9 |
| plan.md | 29 | 968 | 4343ab72f525a060e53bfb517d52504b16fb982803abda5243c13f36a7c486e3 |
| landed.diff | 10 | 2121 | caaea37932ac90fb6fca2e669685f81c45dab629cf17a3b020bf71f173286346 |

`plan.md` is a REWRITE of `.agent/plan.md`. Both diffs go on with `git apply`; the reviewer
generated them with `git diff HEAD` from a tree at `72ba3b2e` into which it wrote the edits.
`records.diff` appends round 8's gate entry, R-1092's `Done:` and R-1093's registration to
`.agent/live_review.md` and DECISION F038 D10 to `.agent/decisions.md`. `landed.diff` appends one
`Landed: R-1093 — ` line; it applies on top of C2's ledger and goes in with C4's tests.

THE SPECIFICATION. No `except Exception` anywhere and no `# noqa: BLE001`.
S1 R-1093's REPAIR. `tests/orchestration/test_chat_turn.py` gains, at its end, the one test
   R-1093's FIX names; read the cited item's number off a first turn asked with
   `answer_call_fn=None`, never type it. Nothing else in that file changes.
S2 THE LOOKUP. `apps/cli/commands/ui.py` gains a public
   `live_ui_session_for_job(job_id) -> dict | None`: among `_read_sessions()`, those whose
   `job_id` equals the given one and whose `pid` `_is_pid_alive` accepts, the one with the
   greatest `started_at`, or None. It reads only: it prunes, archives and writes nothing.
S3 THE CATALOG. After the `chat.show` entry, `CommandEntry(command_id="chat.ask",
   group_id="chat", subcommand="ask", action_class="write_metadata", supports_json=True,
   may_mutate_repo=False, may_execute_commands=False, related=("chat.send", "chat.show",
   "ui.start"), exit_codes=(0, 1, 2, 3))` with args `job_id`, `text`, `--task` (an option taking
   a value), `--yes` (`is_flag=True`, as the catalog's other `--yes` flags are) and `_JSON_OPT`.
   Word every description so `tests/docs/test_vocabulary.py` passes: a description saying "job"
   also says "task" (or mission, budget, fence), and one saying "task" also says "job plan",
   "step" or "run" — the reviewer's first wording failed exactly there.
S4 THE HANDLER. `_cmd_chat_ask(job_id, text, *, task_id="", yes=False, json_output=False)` in
   `chat_cmd.py`, registered as `"chat.ask"` in `COMMAND_HANDLERS`; its imports inside the
   function, as its neighbours'. It resolves the job as `_cmd_chat_send` does (an unreadable
   record exits `EXIT_NOT_READY`), runs `run_chat_turn(job, text, task_id=<stripped>)`, and a
   `ChatTurnError` exits 2 (`invalid_task`). The module docstring gains one paragraph for it.
S5 AN ANSWER. Text: `Scope: <scope> <subject>` (the subject `no registered project` when empty),
   then `render_chat_answer(answer)`, then one `[<n>] <kind> <ref>` line per evidence item. JSON:
   `emit_ok` with `job_id`, `kind="answer"`, `scope`, `subject`, `generator`, `sentences` (each
   `text`, `citations`, `supported`), `evidence` (each `number`, `kind`, `ref`) and `omitted`.
S6 A CARD. Its title, then each line indented, on stdout, or on stderr under `--json` (the
   idiom's rule). Nothing is sent, and the reason is kept, when the card is not confirmable;
   when neither `--yes` is given nor standard input is a terminal (asked through a module-level
   `_chat_stdin_is_a_tty()`, the idiom's shape, so a test can replace it), the reason naming
   `--yes`; or when the answer typed at `Send it? [y/N] ` is not `y` or `yes`. Otherwise it is
   SENT: `live_ui_session_for_job(job.job_id)`; None exits 3 (`cockpit_not_running`) with a
   sentence naming `remedy ui start <job id>`; else `send_card_through_door(card, job_id=...,
   client_nonce="chat-" + secrets.token_hex(8), port=int(session["port"]),
   token=str(session["token"]))`; an `OSError` exits 3 (`cockpit_unreachable`); an answer that is
   not accepted exits 1 (`door_refused`) with its status and the body's `error`. Text ends with
   `Sent: <verb>. The cockpit answered: <outcome>.` or `Not sent: <reason>.`; JSON is `emit_ok`
   with `job_id`, `kind="card"`, `verb`, `title`, `lines`, `confirmable`, `sent`, `door` (the
   door's body, or `{}`) and `not_sent_reason`. Exit 0 whether or not it was sent.
S7 THE GUARDS AND THE GUIDE. `docs/guides/exit-codes.md` gains a row for `remedy chat ask` with
   exit code 3, shaped as its neighbours, directly after the `remedy chat show` row. In `ALLOWED_UNWIRED` the `chat_door.py` and `chat_turn.py` entries are
   REMOVED. `tests/orchestration/import_reachability_allowlist.txt` gains exactly six lines, in
   sorted place between `change_set` and `checkpoints`: `packages.orchestration.chat_answer`,
   `chat_door`, `chat_evidence`, `chat_intent`, `chat_intent_model` and `chat_turn`, each with
   the `packages.orchestration.` prefix; no other line of it changes (a regenerated file would
   also drop `do_run`, which this round must not touch).

THE TESTS — a NEW FILE `tests/cli/test_chat_ask.py`, modelled on `tests/cli/test_chat_cmd.py`'s
`_run` and data-root fixture, with a saved RUNNING job of one task (title "Write the README",
status "done", `test_passed` True, `metadata={"target_repo": "/tmp/repo"}`). A live cockpit is a
real server started in a thread as `tests/orchestration/test_chat_door.py` does, whose info file
is written INTO the registry, `<data root>/ui/sessions/<name>.json`, so its `pid` is this process.
At least, one each: a focused question under `--json` answers `kind` `answer`, scope `node`,
subject the task; an unfocused question in text prints `Scope: project` and `Not in evidence.`;
"pause" under `--json` with no `--yes` (pytest's stdin is not a terminal) answers `sent` false, a
reason naming `--yes`, and no audit file; "pause --yes" with no cockpit exits 3 and writes no
audit file; with a live cockpit, "pause --yes --json" answers `sent` true, `door.command`
`job.pause`, and the audit reads one `accepted` `job.pause` line; with `_chat_stdin_is_a_tty`
replaced to answer True, an input of `n` prints `Not sent: not confirmed.` with no audit line and
an input of `y` prints `Sent: job.pause.` with one; a live session registered for ANOTHER job id
is not used (exit 3); a registry file naming this job with the pid of a child process that has
already exited is not used (exit 3); a registry file with this cockpit's port and a WRONG token
exits 1; `--task 0123456789abcdef` exits 2; "deploy it --yes --json" answers `sent` false and
`confirmable` false; and the bare `remedy chat <job> "<message>"` still records a steering message.

BUNDLE — the commits are C1a, C1b, C2, C3, C4 and C5, in this order.

C1a — copy this block and the plan payload
  `.agent/authored/f038-r9-block.md` := this block and `.agent/authored/f038-r9-plan.md` :=
  plan.md, by `shutil.copyfile`.
  Subject: `F038 R9 C1a: copy round 9 block and plan payload into .agent/authored/`
  Its insertions are this block's line count plus 29. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C1b — copy the two diffs
  `.agent/authored/f038-r9-records.diff` := records.diff and
  `.agent/authored/f038-r9-landed.diff` := landed.diff.
  Subject: `F038 R9 C1b: copy round 9 records and landed diffs into .agent/authored/`
  Expected insertions: 70.

C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F038 R9 C2: book round 8, resolve R-1092, register R-1093, record DECISION F038 D10`
  Expected by `git show --numstat` (insertions and deletions): 38/0 decisions.md, 6/0
  live_review.md, 7/7 plan.md.

C3 — THE CODE: S2 to S7.
  Subject: `F038 R9 C3: add remedy chat ask, one chat turn on the command line`

C4 — THE TESTS, THE LANDED LINE AND THE TOOL: S1's test, `tests/cli/test_chat_ask.py`,
  `git apply` landed.diff, and your mutation tool (G5) saved as `.agent/authored/f038-r9-mutations.py`.
  Subject: `F038 R9 C4: test remedy chat ask and repair R-1093`

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F038 R9 C5: rewrite handoff for round 9`
  Then `git push origin feature/f038-grounded-chat`. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects (C4a and C4b), and say so.
3. The round's whole tracked path set is: the `.agent/authored/f038-r9-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `apps/cli/command_catalog.py`, `apps/cli/commands/chat_cmd.py`, `apps/cli/commands/ui.py`,
   `docs/guides/exit-codes.md`, `tests/test_no_orphan_modules.py`,
   `tests/orchestration/import_reachability_allowlist.txt`, `tests/cli/test_chat_ask.py`,
   `tests/orchestration/test_chat_turn.py`, and `.agent/handoff.md`. Report the list you measure
   with `git diff --name-only 7627663b7` at the branch tip after C5. Touch nothing else: no other
   file under `apps/`, `packages/` or `docs/`, no `README.md`, no `.agent/context.md`,
   `.agent/prose_slips.md`, `.agent/candidates.md` or `.agent/operator_questions.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong, or this round's own mutation tool, may be corrected before C5 in a
   new commit, and the correction is declared. An EXISTING test that goes red is never edited to
   pass; report it and stop.
5. NOTHING IS MERGED, SENT OR REWRITTEN. No `gh pr merge`, no `gh pr create`, no checkout of
   `main`, no branch deletion, no force-push, no `git stash`, no request to any server this
   round's tests did not start themselves or to any model, and no `git commit --amend` or any
   other rewrite of a commit, pushed or not: a wrong commit subject is declared, never amended.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F038's belongs to its closure. G4's selection is long, about ten minutes; run it once.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f038-r9-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f038-r9/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS — the sha256 of each file below, read with `git show <commit>:<path>` at the commit
 named, equals the reviewer's reading, printed from its simulation tree. Report each beside the
 hash you read:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/decisions.md | 2406736 | d5a308fc82bd2fbe14a2308f373fbd22eff8130ce578d1d8aa39fbada7f711a7 |
 | C2 | .agent/live_review.md | 334333 | 03ab5768a1953e50dff041b574af6a1706482000f22151133c7a42b3da76356b |
 | C2 | .agent/plan.md | 968 | 4343ab72f525a060e53bfb517d52504b16fb982803abda5243c13f36a7c486e3 |
 | C4 | .agent/live_review.md | 334559 | a6a84ced9ac8f2ae3a9db612fa860e95fb5d267fe9bbd667add1172632ad8e67 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT read with `git show` at C2 and at C4 (the
 reviewer read `['R-1093']` at both); and `git diff --name-only <C1b> <C2>`, which must name
 exactly the three C2 paths of the table.

G3 THE CODE — `python3 -m ruff check apps/cli/command_catalog.py apps/cli/commands/chat_cmd.py
 apps/cli/commands/ui.py tests/cli/test_chat_ask.py tests/orchestration/test_chat_turn.py
 tests/test_no_orphan_modules.py` at C4, with its real exit code. Then report, quoted from
 `git show <C3>`, the whole of `_cmd_chat_ask`, `live_ui_session_for_job` and the `chat.ask`
 catalog entry, and `git show <C3> -- tests/orchestration/import_reachability_allowlist.txt`.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_chat_turn.py tests/orchestration/test_chat_intent_model.py tests/orchestration/test_chat_door.py tests/orchestration/test_chat_intent.py tests/orchestration/test_chat_answer.py tests/orchestration/test_chat_evidence.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_subprocess_timeouts.py tests/regression/test_named_bugs.py tests/test_path_utils.py tests/test_data_paths.py tests/orchestration/test_env_registry.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py tests/ui_server/test_command_channel.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/orchestration/test_model_routing.py tests/orchestration/test_contract_hygiene.py tests/orchestration/test_decision_inbox.py tests/test_no_interactive_guard.py tests/cli/ tests/docs/ 2>&1 | tail -12; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection serially in the primary checkout at `72ba3b2e5` and read
 `3637 passed, 9 skipped` at exit code 0, the skips being the six of the F252 quarantine and three
 of `tests/orchestration/test_model_routing.py`; over its simulation tree, with its own versions
 of the code and tests (10 new nodes), it read `3649 passed, 10 skipped` at exit code 0: three
 nodes more are catalog-parametrized cases the new entry adds —
 `test_declared_codes_are_the_floor_plus_named_codes[chat.ask]`,
 `test_declared_codes_equal_the_codes_the_handler_reaches[chat.ask]` and
 `TestInvalidArgumentSweep::test_an_unrecognised_option_answers_the_envelope[chat.ask]` — and the
 further skip is a vitest test that runs only in the primary checkout. Report the node counts of
 `tests/cli/test_chat_ask.py` and `tests/orchestration/test_chat_turn.py` by `--collect-only -q`
 at C4, every `SKIPPED` line and the summary, and account for any difference from 3637 passed by
 those counts and the three cases above. Then `python3 -m apps.cli.main integrity check --json`,
 which must read all six checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — your tool `.agent/authored/f038-r9-mutations.py` takes a worktree path, and
 for each mutation below edits the named file INSIDE that worktree (asserting its FROM text occurs
 exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider -rf tests/cli/test_chat_ask.py
 tests/orchestration/test_chat_turn.py` from the worktree's root after purging its `__pycache__`
 directories, with the worktree's root first on `PYTHONPATH`, restores the bytes, and prints one
 line per mutation: its label, the exit code, the failed count and the failing node ids, both read
 from the `FAILED` lines `-rf` prints. It runs an unmutated control first and last and ends with
 `restored byte-identical: True` and a final line `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY:
 <bool>`. Each is a real behaviour change, in `chat_cmd.py` unless named:
  r1 `--yes` is ignored; r2 a card is sent with neither `--yes` nor a terminal;
  r3 a card that is not confirmable is sent; r4 an answer other than `y` sends;
  r5 (`ui.py`) the lookup ignores the job id; r6 (`ui.py`) the lookup ignores a dead pid;
  r7 a refused card exits 0; r8 no cockpit exits 0; r9 a `ChatTurnError` is not caught;
  r10 (`packages/orchestration/chat_turn.py`) a handed-in `answer_call_fn` is dropped (R-1093).
 Run it: `git worktree add --detach .remedy-wt/f038-r9-mut <C4>`, then
 `python3 -B .agent/authored/f038-r9-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f038-r9-mut`
 and report its whole output. EVERY mutation must be red with at least one failing node; a
 mutation that stays green is reported as green, never papered over, and you then add the test
 that catches it in a commit before C5 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f038-r9-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 7`, which must show C5, C4, C3, C2, C1b, C1a and `7627663b7` in that
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
action. Report what you ran, not what you expected to find. Your Session section reads SESSION 3
of feature F038, round 9, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 9, then T003's next part: the cockpit panel asks the same chat turn through a route and
confirms a card through the write door. State the open-findings count, 1 (R-1093, landed and
awaiting the review), and the operator-questions count, 1.

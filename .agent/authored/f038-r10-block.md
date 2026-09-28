STEP F038 R10 — BOOK ROUND 9, RESOLVE R-1093, REGISTER AND REPAIR R-1094, THEN THE COCKPIT'S CHAT ROUTE: one chat turn answered over a read route, in the one wire shape the command line shares

GOAL
Round 9 is reviewed PASS at `c1c3f636`, with R-1093 resolved and one Low finding, R-1094. Book
them, record DECISION F038 D11, repair R-1094 with tests, and land the read route
`GET /api/jobs/<job_id>/chat?text=<line>&task=<task id>`: it runs one chat turn and answers it
in the wire shape `chat_turn_view` gives, which `remedy chat ask --json` then emits too. The
route sends nothing; confirming a card stays the write door's, which the next round's panel uses.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict, never merge, and never write a `Done:` line. THE PRODUCTION CHANGE IS
SPECIFIED, NOT SLICED: you write the code and its tests yourself against S1 to S5 below. Only the
`.agent/` records travel as payloads. Read R-1094 and DECISION F038 D11 in the records diff before
you write code. Before you write anything, read whole: `packages/orchestration/chat_turn.py`;
`apps/cli/commands/chat_cmd.py`; in `packages/orchestration/ui_server.py`, `do_GET`, the
`_build_*_json` builders around `_build_tour_json`, and the `_RemedyHandler` docstring;
`tests/ui_server/test_lessons_route.py` (the socketless `do_GET` idiom you follow);
`tests/ui_server/test_handler_table_walk.py`; in `tests/ui_server/test_command_channel.py`,
`_do_get_route_facts`, `_walkable_paths` and `TestCommandDoorImportGuard`;
`tests/cli/test_chat_ask.py`; and `tests/orchestration/test_chat_turn.py`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f038-r10-payloads/` READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f038-r10/`          READ-ONLY. The reviewer's block.
  every other `.remedy-wt/f038-*` directory except your own, and `.remedy-wt/f038-review/`
                                  The reviewer's; do not touch them.
  `.remedy-wt/f038-r10-worker/`   YOURS for logs and scripts; create it if absent. All are
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
   `feature/f038-grounded-chat`, and `git log --oneline -1` must read `c1c3f636a`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f038-r10/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f038-r10-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 62 | 10502 | eea4a65fc9a5e2e64372bb027aafe50db944237191e02d334ca721daf3c13eb5 |
| plan.md | 29 | 971 | 2e291954bb13be542e2e0180ad9d1ae8e7795c17dda14f1e6a876322834b68ff |
| landed.diff | 10 | 2507 | 3621f6841a99ebdab8dcf6e99e4f79ae87dc65a9f8d2140dc3b85d94b8b28e4a |

`plan.md` is a REWRITE of `.agent/plan.md`. Both diffs go on with `git apply`; the reviewer
generated them with `git diff HEAD` from a tree at `c1c3f636` into which it wrote the edits.
`records.diff` appends round 9's gate entry, R-1093's `Done:` and R-1094's registration to
`.agent/live_review.md` and DECISION F038 D11 to `.agent/decisions.md`. `landed.diff` appends one
`Landed: R-1094 — ` line; it applies on top of C2's ledger and goes in with C4's tests.

THE SPECIFICATION. No `except Exception` anywhere and no `# noqa: BLE001`.
S1 R-1094's REPAIR. Tests that go red under each of its six rules. In `tests/cli/test_chat_ask.py`:
   two or more live sessions registered for one job with different `started_at`, the newest
   returned by `live_ui_session_for_job`; two cards confirmed with `--yes` to ONE running cockpit
   ("pause", then "resume"), both audited `accepted`; the text form of a focused question printing
   one `[<n>] <kind> <ref>` line per evidence item its `--json` form lists; and a `--task` padded
   with spaces answered in the node scope with the bare id as subject. In
   `tests/orchestration/test_chat_turn.py`, over `chat_turn_view` (S2): the evidence numbered 1 to
   n, and a sentence with no citation reported `supported` false beside a cited one reported true
   (an `answer_call_fn` stub, as R-1093's test uses; read the cited number and item off a first
   turn asked with `answer_call_fn=None`, never type them). Existing tests in both files are not
   edited.
S2 THE VIEW. `chat_turn_view(turn: ChatTurn) -> dict[str, Any]` in
   `packages/orchestration/chat_turn.py`, after `run_chat_turn`. An answer: `kind` `answer`,
   `scope`, `subject`, `question`, `generator`, `sentences` (each `text`, `citations` as a list,
   `supported`, `problem`), `evidence` (each `number` from 1 in the evidence set's order, `kind`,
   `ref`, `text`) and `omitted`. A card: `kind` `card`, `verb`, `title`, `lines` (a list), `args`
   (a dict), `missing` (a list) and `confirmable`. Nothing else is added or changed in the module.
S3 THE COMMAND LINE. In `apps/cli/commands/chat_cmd.py`, `remedy chat ask --json` emits the view:
   an answer as `emit_ok(job_id=<job id>, **chat_turn_view(turn))`, a card as the same plus
   `sent`, `door` and `not_sent_reason`, so the card path is handed the turn. Every text output,
   every exit code and every other behaviour of the command stays as it is.
S4 THE ROUTE. In `packages/orchestration/ui_server.py`, a module function
   `_build_chat_turn_json(job, text, task_id) -> dict[str, Any]`, placed among the `_build_*_json`
   builders, importing from `chat_turn` inside its body: a `text` that is empty after strip answers
   `{"available": False, "reason": "empty_text"}`; otherwise `run_chat_turn(job, text,
   task_id=<task_id stripped>)`, where a `ChatTurnError` answers `{"available": False, "reason":
   "unknown_task"}`, and a turn answers `{"available": True, **chat_turn_view(turn)}`. In `do_GET`,
   directly after the `events-since` branch and in its shape, `if endpoint == "chat":` reads `text`
   and `task` from `qs` (each defaulting to `""`) and answers 200 with the builder's dict, under a
   one-line comment naming DECISION F038 D11. Nothing else in the file changes: no POST route, no
   change to the write door or to the `_RemedyHandler` docstring, which stays true.
S5 THE 405 WALK. In `tests/ui_server/test_command_channel.py`, `_walkable_paths` gains
   `f"/api/jobs/{self.job_id}/chat",` directly after its `events-since` line; nothing else in that
   file changes. Why, read at `c1c3f636`: `_do_get_route_facts` derives only dict keys and `path`
   literals, so a route matched by `endpoint ==` is walked only when listed by hand, while
   `tests/ui_server/test_handler_table_walk.py` DOES derive it from the `endpoint ==` comparison and
   requires it to answer 200 for a real job with no query at all, which S4's `empty_text` answers.
   `TestCommandDoorImportGuard` scans only the door's methods, so the builder's import is outside it.

THE TESTS — a NEW FILE `tests/ui_server/test_chat_route.py`, reading the route with `do_GET` on a
handler built without a socket as `tests/ui_server/test_lessons_route.py` does, over a saved
RUNNING job of one task (title "Write the README", status "done", `test_passed` True,
`metadata={"target_repo": "/tmp/repo"}`) in a temporary data root, with the query values
URL-quoted. At least, one each: a focused question answers 200, `available` true, `kind` `answer`,
scope `node`, subject the task, evidence numbered 1 to n; for that line and for "pause", every key
of the route's body except `available` equals the same key of `remedy chat ask --json`'s output;
an unfocused question answers scope `project`, no evidence, and the one sentence
`Not in evidence.`; "pause" answers a card, verb `job.pause`, confirmable, and the data root's
files hash identically before and after; a focused "note: use tabs" answers verb `job.steer` with
`args` exactly `{"task_id": <the task>, "message": "use tabs"}` and no `missing`; no `text` and a
blank `text` each answer `empty_text`; `task=0123456789abcdef` answers `unknown_task`; a padded
`task` answers the node scope; and two questions leave the data root's files hashing identically.

BUNDLE — the commits are C1a, C1b, C2, C3, C4 and C5, in this order.

C1a — copy this block and the plan payload
  `.agent/authored/f038-r10-block.md` := this block and `.agent/authored/f038-r10-plan.md` :=
  plan.md, by `shutil.copyfile`.
  Subject: `F038 R10 C1a: copy round 10 block and plan payload into .agent/authored/`
  Its insertions are this block's line count plus 29. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C1b — copy the two diffs
  `.agent/authored/f038-r10-records.diff` := records.diff and
  `.agent/authored/f038-r10-landed.diff` := landed.diff.
  Subject: `F038 R10 C1b: copy round 10 records and landed diffs into .agent/authored/`
  Expected insertions: 72.

C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F038 R10 C2: book round 9, resolve R-1093, register R-1094, record DECISION F038 D11`
  Expected by `git show --numstat` (insertions and deletions): 40/0 decisions.md, 6/0
  live_review.md, 7/7 plan.md.

C3 — THE CODE: S2 to S4.
  Subject: `F038 R10 C3: answer one chat turn over the cockpit's read route`

C4 — THE TESTS, THE WALK, THE LANDED LINE AND THE TOOL: S1, S5, `tests/ui_server/test_chat_route.py`,
  `git apply` landed.diff, and your mutation tool (G5) saved as
  `.agent/authored/f038-r10-mutations.py`.
  Subject: `F038 R10 C4: test the chat route and repair R-1094`

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F038 R10 C5: rewrite handoff for round 10`
  Then `git push origin feature/f038-grounded-chat`. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects (C4a and C4b), and say so.
3. The round's whole tracked path set is: the `.agent/authored/f038-r10-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `apps/cli/commands/chat_cmd.py`, `packages/orchestration/chat_turn.py`,
   `packages/orchestration/ui_server.py`, `tests/ui_server/test_chat_route.py`,
   `tests/ui_server/test_command_channel.py`, `tests/cli/test_chat_ask.py`,
   `tests/orchestration/test_chat_turn.py`, and `.agent/handoff.md`. Report the list you measure
   with `git diff --name-only c1c3f636a` at the branch tip after C5. Touch nothing else: no other
   file under `apps/`, `packages/`, `tests/` or `docs/`, no `README.md`, no `.agent/context.md`,
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
   F038's belongs to its closure. G4's selection takes about three minutes; run it once.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f038-r10-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f038-r10/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS — the sha256 of each file below, read with `git show <commit>:<path>` at the commit
 named, equals the reviewer's reading, printed from its simulation tree. Report each beside the
 hash you read:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/decisions.md | 2410035 | d0c1611cfffb33f18d1268a6693b36a5827228fde2b9aeac595669bdc0129b08 |
 | C2 | .agent/live_review.md | 339555 | 28651e704757f6cda3fdd3c5cd70059a7dfcd48e1d98485c49d528c6b257232c |
 | C2 | .agent/plan.md | 971 | 2e291954bb13be542e2e0180ad9d1ae8e7795c17dda14f1e6a876322834b68ff |
 | C4 | .agent/live_review.md | 339924 | 5a7565821894795a6987e52c5424106237e79c7ed9e4a22e965aa5bde31d5c92 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT read with `git show` at C2 and at C4 (the
 reviewer read `['R-1094']` at both); and `git diff --name-only <C1b> <C2>`, which must name
 exactly the three C2 paths of the table.

G3 THE CODE — `python3 -m ruff check apps/cli/commands/chat_cmd.py
 packages/orchestration/chat_turn.py packages/orchestration/ui_server.py
 tests/ui_server/test_chat_route.py tests/ui_server/test_command_channel.py
 tests/cli/test_chat_ask.py tests/orchestration/test_chat_turn.py
 .agent/authored/f038-r10-mutations.py` at C4, with its real exit code. Then report, quoted from
 `git show <C3>`, the whole of `chat_turn_view`, `_build_chat_turn_json` and the `chat` branch of
 `do_GET`.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_server/ tests/orchestration/test_chat_turn.py tests/orchestration/test_chat_intent_model.py tests/orchestration/test_chat_door.py tests/orchestration/test_chat_intent.py tests/orchestration/test_chat_answer.py tests/orchestration/test_chat_evidence.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_subprocess_timeouts.py tests/orchestration/test_contract_hygiene.py tests/test_no_interactive_guard.py tests/cli/test_chat_ask.py tests/cli/test_chat_cmd.py tests/cli/test_exit_codes.py tests/cli/test_golden_path.py 2>&1 | tail -12; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection serially in the primary checkout at `c1c3f636a` and read
 `1245 passed` with no skip at exit code 0; over its simulation tree, with its own versions of the
 code and tests (13 new nodes), it read `1257 passed, 1 skipped` at exit code 0, the skip being
 `tests/ui_server/test_timeline_scrub_live.py`, which needs `apps/ui/node_modules` and so runs
 only in the primary checkout. At `c1c3f636a` the reviewer's `--collect-only -q` read 13 nodes in
 `tests/cli/test_chat_ask.py` and 9 in `tests/orchestration/test_chat_turn.py`. Report the node
 counts of `tests/ui_server/test_chat_route.py` and those two files by `--collect-only -q` at C4,
 every `SKIPPED` line and the summary, and account for any difference from 1245 passed by those
 counts. Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0.

G5 THE RED PROOFS — your tool `.agent/authored/f038-r10-mutations.py` takes a worktree path, and
 for each mutation below edits the named file INSIDE that worktree (asserting its FROM text occurs
 exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider -rf
 tests/ui_server/test_chat_route.py tests/orchestration/test_chat_turn.py
 tests/cli/test_chat_ask.py` from the worktree's root after purging its `__pycache__`
 directories, with the worktree's root first on `PYTHONPATH`, restores the bytes, and prints one
 line per mutation: its label, the exit code, the failed count and the failing node ids, both read
 from the `FAILED` lines `-rf` prints. It runs an unmutated control first and last and ends with
 `restored byte-identical: True` and a final line `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY:
 <bool>`. Each is a real behaviour change: in `ui_server.py`, m1 a blank `text` runs a turn;
 m2 a `ChatTurnError` is not caught; m3 the task is dropped; m4 the task is not stripped. In
 `chat_turn.py`, m5 the view numbers evidence from 0; m6 every sentence is reported supported;
 m7 a card's `args` come back empty. In `apps/cli/commands/ui.py`, m8 the lookup returns the
 oldest session. In `chat_cmd.py`, m9 every send uses one fixed nonce; m10 the text form's evidence
 lines are dropped; m11 `--task` is not stripped; m12 the `--json` answer's `question` is blanked.
 Run it: `git worktree add --detach .remedy-wt/f038-r10-mut <C4>`, then
 `python3 -B .agent/authored/f038-r10-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f038-r10-mut`
 and report its whole output. EVERY mutation must be red with at least one failing node; a
 mutation that stays green is reported as green, never papered over, and you then add the test
 that catches it in a commit before C5 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f038-r10-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 7`, which must show C5, C4, C3, C2, C1b, C1a and `c1c3f636a` in that
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
of feature F038, round 10, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 10, then T003's next part: the cockpit's chat panel, with citation chips, unsupported marks
and cards confirmed through the write door, and its DOM audit. State the open-findings count, 1
(R-1094, landed and awaiting the review), and the operator-questions count, 1.

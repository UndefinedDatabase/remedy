STEP F038 R8 — BOOK ROUND 7, REGISTER AND REPAIR R-1092, THEN ONE CHAT TURN: a line becomes a grounded answer or an action card, through one module both doors will call, sending nothing

GOAL
Round 7 is reviewed PASS at `61cf423a`, with one Low finding, R-1092: two rules of the model-written
parse have no test. Book the verdict, register R-1092 and record DECISION F038 D9; repair R-1092
with two tests; and land a NEW module `packages/orchestration/chat_turn.py` whose `run_chat_turn`
reads one line of a job's chat with the model-written parse and the job's open decisions, answers
a question from the focused task's evidence or from the project's, and turns anything else into
an action card. It writes no file and sends nothing. Nothing imports the new module yet.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge, and you never write a `Done:` line. THE PRODUCTION
CHANGE IS SPECIFIED, NOT SLICED: you write the code and its tests yourself against S1 to S5
below. Only the `.agent/` records travel as payloads. Read R-1092 and DECISION F038 D9 in the
records diff before you write code. Before you write anything, read whole:
`packages/orchestration/chat_intent_model.py` and `tests/orchestration/test_chat_intent_model.py`;
`node_evidence_set`, `project_evidence_set` and `compose_chat_evidence` in
`packages/orchestration/chat_evidence.py`; `answer_chat_question` and `CHAT_NOT_IN_EVIDENCE` in
`packages/orchestration/chat_answer.py`; `build_action_card` in
`packages/orchestration/chat_intent.py`; `build_decision_inbox` in
`packages/orchestration/decision_inbox.py`; `enqueue_task_decision` and `answer_task_decision` in
`packages/orchestration/escalation.py`; `load_run_events` in `packages/orchestration/timeline.py`;
`find_project_by_repo` in `packages/orchestration/project_registry.py`; and
`tests/test_no_orphan_modules.py`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f038-r8-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f038-r8/`           READ-ONLY. The reviewer's block.
  every other `.remedy-wt/f038-*` directory except your own, and `.remedy-wt/f038-review/`
                                  The reviewer's; do not touch them.
  `.remedy-wt/f038-r8-worker/`    YOURS for logs and scripts; create it if absent. All are
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
   `feature/f038-grounded-chat`, and `git log --oneline -1` must read `61cf423a3`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f038-r8/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f038-r8-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 52 | 12395 | 99697a9d245aff8f1ebfb85811fb2af8f36182010ed60ad1837336aa64aad9c2 |
| plan.md | 29 | 928 | 33e711de71476e3de000fca594b23726f4464871f0b122c5529b5154e4cdd623 |
| landed.diff | 10 | 4685 | aba389e17460c864cc8bf6461b23d391f63056873b3b620ee18fdee12e717bce |

`plan.md` is a REWRITE of `.agent/plan.md`. Both diffs go on with `git apply`; the reviewer
generated them with `git diff HEAD` from a tree at `61cf423a` into which it wrote the edits.
`records.diff` appends round 7's gate entry and R-1092's registration to `.agent/live_review.md`
and DECISION F038 D9 to `.agent/decisions.md`. `landed.diff` appends one `Landed: R-1092 — ` line
to `.agent/live_review.md`; it applies on top of C2's ledger and goes in with C4's tests.

THE SPECIFICATION. No `except Exception` anywhere and no `# noqa: BLE001`.
S1 R-1092's REPAIR. `tests/orchestration/test_chat_intent_model.py` gains, at its end, exactly
   the two tests R-1092's FIX names: a reply whose confidence is the JSON token `NaN` is unknown;
   and a `decision.resolve` reply whose decision id and answer carry spaces around them, with the
   id in the open set, comes back with both stripped and nothing missing. Nothing else in that
   file changes.
S2 THE NEW MODULE, `chat_turn.py`. A docstring naming F038 T003 and DECISION F038 D9, with one
   sentence stating that Remedy deliberately does not let a chat turn send anything: confirming a
   card is its caller's step. At module level it imports the standard library and, from
   `packages.orchestration`, only `chat_answer`, `chat_evidence`, `chat_intent` and
   `chat_intent_model`, each name imported BY NAME so a test can replace
   `chat_turn.parse_chat_intent_with_model`; `decision_inbox`, `timeline`, `data_paths` and
   `project_registry` are imported inside the functions that use them. Constants
   `CHAT_TURN_ANSWER = "answer"` and `CHAT_TURN_CARD = "card"`; `class ChatTurnError(ValueError)`;
   a frozen dataclass `ChatTurn(kind: str, evidence: ChatEvidenceSet | None = None,
   answer: ChatAnswer | None = None, card: ChatActionCard | None = None)`.
S3 THE OPEN DECISIONS. `chat_open_decision_ids(job) -> tuple[str, ...]`: the `id` of every card of
   `build_decision_inbox(job, load_run_events(resolve_data_root(), job.job_id))["decisions"]`
   whose `answerable_by_decision_resolve` is true, in the inbox's order.
S4 THE PROJECT. `chat_project_for_job(job)`: None when `job.repo_path` is empty, otherwise
   `find_project_by_repo(os.path.realpath(job.repo_path))`.
S5 THE TURN. `run_chat_turn(job, text, *, task_id="", intent_call_fn=<unset>,
   answer_call_fn=<unset>) -> ChatTurn`, one module sentinel meaning unset for both: (a) a
   non-empty `task_id` that is not the `task_id` of one of `job.tasks` raises `ChatTurnError`
   with a message containing `task_id`, before anything is read; (b) the intent is
   `parse_chat_intent_with_model(text, focused_task_id=task_id,
   open_decision_ids=chat_open_decision_ids(job))`, with `call_fn=intent_call_fn` passed only
   when it is set; (c) anything but a QUESTION is `ChatTurn(kind=CHAT_TURN_CARD,
   card=build_action_card(intent, job_id=str(job.job_id)))`; (d) a QUESTION's evidence is
   `node_evidence_set(job, task_id)` when a task is focused; otherwise
   `project_evidence_set(project)` for `chat_project_for_job(job)`, or, when that is None,
   `compose_chat_evidence(CHAT_SCOPE_PROJECT, "", [])`; the answer is
   `answer_chat_question(text, evidence)`, with `call_fn=answer_call_fn` passed only when it is
   set; and the turn is `ChatTurn(kind=CHAT_TURN_ANSWER, evidence=..., answer=...)`.
S6 THE GUARD. In `ALLOWED_UNWIRED` of `tests/test_no_orphan_modules.py` the
   `packages/orchestration/chat_intent_model.py` entry is REPLACED, in the same place, by
   `("packages/orchestration/chat_turn.py", "F038's one chat turn, a grounded answer or an action
   card; the chat command wires it in a later round (DECISION F038 D9) and removes this line")`,
   split over lines as its neighbours are; the reviewer measured the old line going stale once
   `chat_turn.py` imports that module. Nothing else in that file changes.

THE TESTS — a NEW FILE `tests/orchestration/test_chat_turn.py`, with `REMEDY_DATA_DIR` set to
`tmp_path` by an autouse fixture; the only existing test file that changes is S1's. A job there is
a saved `JobPlan` with one `TaskEntry` (title "Write the README", status "done", `test_passed`
True) and `metadata={"target_repo": "/tmp/repo"}`. No test reaches a real model: a call function
that must not be called raises `AssertionError`, and a model reply is a stub returning fixed JSON.
At least, one each: "pause" is a card for `job.pause` with no answer and no evidence, the stub
never called; "deploy it" with `intent_call_fn=None` is the unknown card, not confirmable; "Did
the tests pass?" with the task focused and `answer_call_fn=None` is an answer whose evidence scope
is `node` and whose subject is that task; "What is the roadmap position?" with no task and no
registered project is an answer from an empty `project` set whose one sentence is
`CHAT_NOT_IN_EVIDENCE`; a task id of `0123456789abcdef` raises `ChatTurnError`; a task decision
enqueued with `enqueue_task_decision` (its `now` given) is the one id `chat_open_decision_ids`
lists, and after `answer_task_decision` answers it the list is empty; with that decision open, a
stub reply of `decision.resolve` naming its id with answer "postgres" at confidence 0.9 gives a
confirmable card whose args are exactly that id and answer; and, with
`chat_turn.parse_chat_intent_with_model` replaced by a recorder, the open decision ids it received
equal `chat_open_decision_ids(job)`.

BUNDLE — the commits are C1a, C1b, C2, C3, C4 and C5, in this order.

C1a — copy this block and the plan payload
  `.agent/authored/f038-r8-block.md` := this block and `.agent/authored/f038-r8-plan.md` :=
  plan.md, by `shutil.copyfile`.
  Subject: `F038 R8 C1a: copy round 8 block and plan payload into .agent/authored/`
  Its insertions are this block's line count plus 29. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C1b — copy the two diffs
  `.agent/authored/f038-r8-records.diff` := records.diff and
  `.agent/authored/f038-r8-landed.diff` := landed.diff.
  Subject: `F038 R8 C1b: copy round 8 records and landed diffs into .agent/authored/`
  Expected insertions: 62.

C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F038 R8 C2: book round 7, register R-1092 and record DECISION F038 D9`
  Expected by `git show --numstat` (insertions and deletions): 32/0 decisions.md, 4/0
  live_review.md, 6/6 plan.md.

C3 — THE CODE: `packages/orchestration/chat_turn.py` and S6's replacement.
  Subject: `F038 R8 C3: run one chat turn, a grounded answer or an action card`

C4 — THE TESTS, THE LANDED LINE AND THE TOOL: S1's two tests, `tests/orchestration/test_chat_turn.py`,
  `git apply` landed.diff, and your mutation tool (G5) saved as `.agent/authored/f038-r8-mutations.py`.
  Subject: `F038 R8 C4: test the chat turn and repair R-1092`

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F038 R8 C5: rewrite handoff for round 8`
  Then `git push origin feature/f038-grounded-chat`. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects (C4a and C4b), and say so.
3. The round's whole tracked path set is: the `.agent/authored/f038-r8-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `packages/orchestration/chat_turn.py`, `tests/test_no_orphan_modules.py`,
   `tests/orchestration/test_chat_turn.py`, `tests/orchestration/test_chat_intent_model.py`, and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only 61cf423a3` at the
   branch tip after C5. Do NOT touch anything under `apps/` or `docs/`, any other file under
   `packages/`, `README.md`, `tests/orchestration/import_reachability_allowlist.txt`,
   `.agent/context.md`, `.agent/prose_slips.md`, `.agent/candidates.md` or
   `.agent/operator_questions.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong, or this round's own mutation tool, may be corrected before C5 in a
   new commit, and the correction is declared. An EXISTING test that goes red is never edited to
   pass; report it and stop.
5. NOTHING IS MERGED, SENT OR REWRITTEN. No `gh pr merge`, no `gh pr create`, no checkout of
   `main`, no branch deletion, no force-push, no `git stash`, no request to any server or model,
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
 against the PAYLOADS table. Then compare each `.agent/authored/f038-r8-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f038-r8/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS — the sha256 of each file below, read with `git show <commit>:<path>` at the commit
 named, equals the reviewer's reading, printed from its simulation tree. Report each beside the
 hash you read:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/decisions.md | 2403519 | e8ba4321f2bb15ce6d2528da531bb4f2cc4ceb3eaec36d9fb740256d77f7dc2c |
 | C2 | .agent/live_review.md | 329922 | e0324aab061203332f700f8b7780367eaa7c270a5d7a670c0e44ec0d9c542a9b |
 | C2 | .agent/plan.md | 928 | 33e711de71476e3de000fca594b23726f4464871f0b122c5529b5154e4cdd623 |
 | C4 | .agent/live_review.md | 330171 | 3dd74a66f67bc685ae0d596b69db7956cceea1956fe2b7210b637ea3558e64c0 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT read with `git show` at C2 and at C4 (the
 reviewer read `['R-1092']` at both, because a `Landed:` line resolves nothing); and
 `git diff --name-only <C1b> <C2>`, which must name exactly the three C2 paths of the table.

G3 THE CODE — `python3 -m ruff check packages/orchestration/chat_turn.py
 tests/orchestration/test_chat_turn.py tests/orchestration/test_chat_intent_model.py
 tests/test_no_orphan_modules.py` at C4, with its real exit code. Then report, quoted from
 `git show <C3>`, the whole of `run_chat_turn`, `chat_open_decision_ids` and
 `chat_project_for_job`.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_chat_turn.py tests/orchestration/test_chat_intent_model.py tests/orchestration/test_chat_door.py tests/orchestration/test_chat_intent.py tests/orchestration/test_chat_answer.py tests/orchestration/test_chat_evidence.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_subprocess_timeouts.py tests/regression/test_named_bugs.py tests/test_path_utils.py tests/test_data_paths.py tests/orchestration/test_env_registry.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py tests/ui_server/test_command_channel.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/cli/test_golden_path.py tests/orchestration/test_model_routing.py tests/orchestration/test_contract_hygiene.py tests/orchestration/test_decision_inbox.py tests/test_no_interactive_guard.py 2>&1 | tail -12; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection, less `tests/orchestration/test_chat_turn.py`, serially in the
 primary checkout at `61cf423a3` and read `1135 passed, 9 skipped` at exit code 0, the skips being
 the six of the F252 quarantine and three of `tests/orchestration/test_model_routing.py`; over its
 simulation tree, carrying this round's records and an EARLIER version of its own tests with 8
 nodes in the new file and S1's two, the whole selection read `1144 passed, 10 skipped` at exit
 code 0, the further skip being a vitest test of `tests/orchestration/test_test_runner.py`, which
 runs in the primary checkout. Report the node counts of `tests/orchestration/test_chat_turn.py`
 and `tests/orchestration/test_chat_intent_model.py` by `--collect-only -q` at C4, every `SKIPPED`
 line and the summary, and account for any difference from 1135 passed by those counts. Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0 (R-1092 is Low, so `high_blockers_open` passes).

G5 THE RED PROOFS — your tool `.agent/authored/f038-r8-mutations.py` takes a worktree path, and
 for each mutation below edits the named file INSIDE that worktree (asserting its FROM text occurs
 exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider -rf
 tests/orchestration/test_chat_turn.py tests/orchestration/test_chat_intent_model.py` from the
 worktree's root after purging its `__pycache__` directories, with the worktree's root first on
 `PYTHONPATH`, restores the bytes, and prints one line per mutation: its label, the exit code, the
 failed count and the failing node ids, both read from the `FAILED` lines `-rf` prints. It runs an
 unmutated control first and last and ends with `restored byte-identical: True` and a final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each is a real behaviour change, the first
 six in `chat_turn.py` and the last two in `chat_intent_model.py`:
  r1 a task id that names no task of the job is not refused;
  r2 the parse is handed no open decisions;
  r3 every inbox card's id is listed, answerable or not;
  r4 a question with a focused task is answered from the project scope;
  r5 an action is answered as if it were a question;
  r6 with no registered project, `project_evidence_set` is called with None;
  r7 a confidence that is not a finite number is kept (R-1092);
  r8 argument values are not stripped (R-1092).
 Run it: `git worktree add --detach .remedy-wt/f038-r8-mut <C4>`, then
 `python3 -B .agent/authored/f038-r8-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f038-r8-mut`
 and report its whole output. EVERY mutation must be red with at least one failing node; a
 mutation that stays green is reported as green, never papered over, and you then add the test
 that catches it in a commit before C5 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f038-r8-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 7`, which must show C5, C4, C3, C2, C1b, C1a and `61cf423a3` in that
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
of feature F038, round 8, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 8, then T003's next part: the chat command runs a turn, prints the answer or the card, and
sends a confirmed card through the running cockpit. State the open-findings count, 1 (R-1092,
landed and awaiting the review), and the operator-questions count, 1.

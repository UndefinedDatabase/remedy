STEP F038 R7 — BOOK ROUND 6, THEN THE MODEL-WRITTEN INTENT PARSE: asked only when the words alone read as unknown and `chat.model_written` is on, with answering a decision and adding a task as two new chat verbs

GOAL
Round 6 is reviewed PASS at `bd080286`. Book it, record DECISION F038 D8, and land: two new verbs
in `packages/orchestration/chat_intent.py` (`decision.resolve` and `job.inject`) with their card
lines; a schema argument on `chat_call_fn` in `packages/orchestration/chat_answer.py`, so the chat
keeps ONE role call site; and a NEW module `packages/orchestration/chat_intent_model.py` whose
`parse_chat_intent_with_model` returns the mechanical parse unless it reads unknown, and otherwise,
with the switch on, asks the `summary` model for a verb, its arguments and a confidence, then
filters, grounds and checks every part of the reply before `chat_action_intent` builds the intent.
A low-confidence or unusable reply is unknown. Nothing is sent and nothing imports the new module.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests yourself against S1 to S6 below. Only the `.agent/` records travel
as payloads. Read DECISION F038 D8 in the records diff before you write code: it is the design
this specification implements. Before you write anything, read whole:
`packages/orchestration/chat_intent.py`; `packages/orchestration/chat_answer.py`;
`tests/orchestration/test_chat_intent.py` and `tests/orchestration/test_chat_answer.py` (their
`_stub_call_fn` and the `chat_model_written` and `chat_call_fn` tests are your model);
`run_structured_call` in `packages/orchestration/structured_outputs.py`; `PROVIDER_CALL_ERRORS`
in `packages/orchestration/result_tour.py`; `ROLE_CONFIG_CALL_SITES` in
`packages/orchestration/model_routing.py`; and `tests/test_no_orphan_modules.py`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f038-r7-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f038-r7/`           READ-ONLY. The reviewer's block.
  every other `.remedy-wt/f038-*` directory except your own, and `.remedy-wt/f038-review/`
                                  The reviewer's; do not touch them.
  `.remedy-wt/f038-r7-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Set environment variables inside tests with `monkeypatch.setenv`, never on a command line.
Never run npm or npx.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f038-grounded-chat`, and `git log --oneline -1` must read `bd0802867`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f038-r7/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f038-r7-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 60 | 12117 | 9c15d34ed02976cc0b5c5b665a93032fc0fb3d85df304ea597b992904f24ac35 |
| plan.md | 29 | 935 | 1f1e17daa7ee14f23cfad40d46b299ab1911f913feddd6d0e378fed16f20d05c |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `bd080286` into which it wrote the edits. It
appends round 6's gate entry to `.agent/live_review.md` and DECISION F038 D8 to
`.agent/decisions.md`.

THE SPECIFICATION. No `except Exception` anywhere and no `# noqa: BLE001`.
S1 `chat_intent.py`. (a) `CHAT_VERB_REQUIRED_ARGS` gains, after `job.rerun-subtree`,
   `"decision.resolve": ("decision_id", "answer")` and `"job.inject": ("text",)`;
   `CHAT_VERB_TITLES` gains, in the same order, "Answer the decision" and "Add a task to the
   plan". (b) `_action_intent` is renamed `chat_action_intent`, public, with a one-line comment
   above it saying the model-written parse builds its intents through the same missing-argument
   rule; every call site follows the rename and its body does not change. (c) `build_action_card`
   states, in this order and each only when present: `Task:`, `Decision: <decision_id>`,
   `Answer: <answer>`, `Message:`, `Text: <text>`, `After: <after>`, `Reason:`; the lines before
   and after these are unchanged. `CHAT_AVAILABLE_ACTIONS`, the parse and everything else stay as
   they are: the two new verbs are reached through the model only (D8 (1)).
S2 `chat_answer.py`. `chat_call_fn` takes `schema: type[BaseModel] = GeneratedChatAnswer` and
   hands it to `make_structured_call_fn` in place of the fixed class; its docstring gains one
   sentence that the intent parse asks for its own schema through this same call site. Nothing
   else in that file changes, and `ROLE_CONFIG_CALL_SITES` must not change.
S3 THE NEW MODULE, `chat_intent_model.py`. A docstring naming F038 T002 and DECISION F038 D8,
   with one sentence stating that Remedy deliberately does not let a model's reply choose a task
   or a decision. At module level it imports the standard library, `pydantic.BaseModel`, and from
   `packages.orchestration` only `chat_answer` (`chat_call_fn`, `chat_model_written`),
   `chat_intent`, `result_tour.PROVIDER_CALL_ERRORS` and `structured_outputs.run_structured_call`
   — imported BY NAME, so a test replaces `chat_intent_model.chat_call_fn`. Constants
   `GENERATED_CHAT_INTENT_SCHEMA_V = "generated_chat_intent_v1"`,
   `CHAT_MODEL_MIN_CONFIDENCE = 0.7` and `CHAT_VERB_OPTIONAL_ARGS = {"job.stop": ("reason",),
   "job.inject": ("after",)}`. `class GeneratedChatIntent(BaseModel)` with
   `SCHEMA_V: ClassVar[str] = GENERATED_CHAT_INTENT_SCHEMA_V` and fields `verb: str`,
   `args: dict[str, str]`, `confidence: float`.
S4 THE PROMPT. `build_intent_prompt(text, *, focused_task_id, open_decision_ids) -> str` states
   the request; then one line per verb of `CHAT_VERB_REQUIRED_ARGS`, in its order, naming the
   verb, its title and its argument names, required then optional; then the focused task, or
   `(none)`; then the open decision ids joined by ", ", or `(none)`; then the rules: exactly one
   listed command or an empty verb when none fits, only that command's argument names, never
   invent a task id or a decision id, a confidence from 0 to 1.
S5 THE PARSE. `parse_chat_intent_with_model(text, *, focused_task_id="", open_decision_ids=(),
   call_fn=<a module sentinel meaning unset>) -> ChatIntent`, never raising for a reply:
   (a) `parse_chat_intent(text, focused_task_id=...)` first; anything but UNKNOWN is returned
   as it is, and the model is not called. (b) An unset `call_fn` becomes
   `chat_call_fn(GeneratedChatIntent)` when `chat_model_written()` is true and None otherwise; a
   `call_fn` handed in, None included, is used as given; None returns the unknown intent.
   (c) `run_structured_call(GeneratedChatIntent, <the S4 prompt>, call_fn,
   allow_parse_retry=True)`; an exception of `PROVIDER_CALL_ERRORS`, or an outcome that is not
   ok, is UNKNOWN. (d) A verb not in `CHAT_VERB_REQUIRED_ARGS`, or a confidence that is not a
   finite number or is under `CHAT_MODEL_MIN_CONFIDENCE`, is UNKNOWN. (e) The arguments are the
   verb's required and optional names only, each the reply's string stripped, or empty; any other
   name is dropped. `task_id`, where the verb has one, is ALWAYS `focused_task_id`, whatever the
   reply said; `decision_id` is kept only when it is one of `open_decision_ids`, else emptied.
   (f) The answer is `chat_action_intent(verb, args)`, so an emptied required argument is
   missing and the card asks for it.
S6 THE GUARD. In `ALLOWED_UNWIRED` of `tests/test_no_orphan_modules.py` the
   `packages/orchestration/chat_answer.py` entry is REMOVED (the new module imports it, so
   `test_every_allowed_unwired_entry_is_a_live_orphan` would red on it — the reviewer measured
   that) and, after the `chat_door.py` entry, `("packages/orchestration/chat_intent_model.py",
   "F038's model-written intent parse behind chat.model_written; the chat command wires it in a
   later round (DECISION F038 D8) and removes this line")` is added, split over lines as its
   neighbours are. Nothing else in that file changes.

THE TESTS — a NEW FILE `tests/orchestration/test_chat_intent_model.py`; no existing test changes.
No test reaches a real model: every call function is a stub returning a fixed text, as
`_stub_call_fn` in `tests/orchestration/test_chat_answer.py` is, and records the prompts it got.
At least, one each: every key of `CHAT_VERB_REQUIRED_ARGS` is in `UI_EXPOSED_COMMANDS` and the
keys of `CHAT_VERB_OPTIONAL_ARGS` are among them; "pause" and "what changed?" come back as the
mechanical parse gives them with the stub never called; a reply of `job.pause` at confidence 0.9
for "hold on a moment" is `job.pause` with nothing missing, after exactly one call; the same at
0.5 is unknown; a reply naming `job.plan-delete-task` at 0.99 is unknown; a `decision.resolve`
reply naming a decision id not in the open set comes back missing `decision_id` with only its
answer kept, and naming one in the set is complete, its card lines exactly `Job: J1`,
`Decision: D-1`, `Answer: yes`, `Command: decision.resolve` and confirmable; a
`job.veto-task` reply naming task `zzz` comes back with the focused task `abc`, and with no
focus it misses `task_id`; a `job.inject` reply carrying `text`, `after` and a name no verb takes
keeps only `text` and `after`, its card lines exactly `Job: J1`, `Text: write docs`, `After: T1`,
`Command: job.inject`; a reply that is not JSON and one whose verb is not a string are each
unknown; a call function raising `ConnectionError` is unknown; with `chat_call_fn` replaced by a
recorder, an unset call function asks nothing while `REMEDY_CHAT_MODEL_WRITTEN` is unset and asks
exactly once, with `GeneratedChatIntent`, once it is set to `1` (call `reset_config()` from
`packages.orchestration.config` after each change, and restore it); and the prompt names every
verb, the focused task and the open decision ids joined by ", ".

BUNDLE — the commits are C1a, C1b, C2, C3, C4 and C5, in this order.

C1a — copy this block and the plan payload
  `.agent/authored/f038-r7-block.md` := this block and `.agent/authored/f038-r7-plan.md` :=
  plan.md, by `shutil.copyfile`.
  Subject: `F038 R7 C1a: copy round 7 block and plan payload into .agent/authored/`
  Its insertions are this block's line count plus 29. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C1b — copy the records diff
  `.agent/authored/f038-r7-records.diff` := records.diff.
  Subject: `F038 R7 C1b: copy round 7 records diff into .agent/authored/`
  Expected insertions: 60.

C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F038 R7 C2: book round 6 and record DECISION F038 D8`
  Expected by `git show --numstat` (insertions and deletions): 42/0 decisions.md, 2/0
  live_review.md, 7/7 plan.md.

C3 — THE CODE: S1, S2, the new module and S6's change.
  Subject: `F038 R7 C3: ask the summary model for an intent the words alone cannot read`

C4 — THE TESTS AND THE TOOL: `tests/orchestration/test_chat_intent_model.py` and your mutation
  tool (G5) saved as `.agent/authored/f038-r7-mutations.py`.
  Subject: `F038 R7 C4: test the model-written intent parse and its grounding`

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F038 R7 C5: rewrite handoff for round 7`
  Then `git push origin feature/f038-grounded-chat`. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects (C4a and C4b), and say so.
3. The round's whole tracked path set is: the `.agent/authored/f038-r7-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `packages/orchestration/chat_intent.py`, `packages/orchestration/chat_answer.py`,
   `packages/orchestration/chat_intent_model.py`, `tests/test_no_orphan_modules.py`,
   `tests/orchestration/test_chat_intent_model.py`, and `.agent/handoff.md`. Report the list you
   measure with `git diff --name-only bd0802867` at the branch tip after C5. Do NOT touch anything
   under `apps/` or `docs/`, any other file under `packages/`, `README.md`,
   `tests/orchestration/import_reachability_allowlist.txt`, `.agent/context.md`,
   `.agent/prose_slips.md`, `.agent/candidates.md` or `.agent/operator_questions.md`.
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
 against the PAYLOADS table. Then compare each `.agent/authored/f038-r7-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f038-r7/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree. Report each path beside the hash you read:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2400957 | 9a8a02bc72f1b00d71d8b4ef295f2c3ee54b4d58a428255e42f22043f0cb1063 |
 | .agent/live_review.md | 325739 | a75da8a4a3fcc1b7e17519c624f6b56f9bfe5dc24d7e10e1d5d27176241247e7 |
 | .agent/plan.md | 935 | 1f1e17daa7ee14f23cfad40d46b299ab1911f913feddd6d0e378fed16f20d05c |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT read with `git show <C2>:<path>` (the
 reviewer read `[]`); and `git diff --name-only <C1b> <C2>`, which must name exactly the paths of
 the table above.

G3 THE CODE — `python3 -m ruff check packages/orchestration/chat_intent.py
 packages/orchestration/chat_answer.py packages/orchestration/chat_intent_model.py
 tests/orchestration/test_chat_intent_model.py tests/test_no_orphan_modules.py` at C4, with its
 real exit code. Then report, quoted from `git show <C3>`, the whole of
 `parse_chat_intent_with_model`, `build_intent_prompt` and `chat_call_fn`, and the diff C3 makes
 to `chat_intent.py`.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_chat_intent_model.py tests/orchestration/test_chat_door.py tests/orchestration/test_chat_intent.py tests/orchestration/test_chat_answer.py tests/orchestration/test_chat_evidence.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_subprocess_timeouts.py tests/regression/test_named_bugs.py tests/test_path_utils.py tests/test_data_paths.py tests/orchestration/test_env_registry.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py tests/ui_server/test_command_channel.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/cli/test_golden_path.py tests/orchestration/test_model_routing.py tests/orchestration/test_contract_hygiene.py 2>&1 | tail -12; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection, less `tests/orchestration/test_chat_intent_model.py`, serially
 in the primary checkout at `bd0802867` and read `1068 passed, 9 skipped` at exit code 0, the
 skips being the six of the F252 quarantine and three of `tests/orchestration/test_model_routing.py`
 ("covered by the violating fixture above"); over its simulation tree, a fresh worktree carrying
 this round's records and its own version of the code and tests, the whole selection read
 `1080 passed, 10 skipped` at exit code 0, the further skip being a vitest test of
 `tests/orchestration/test_test_runner.py`, which runs in the primary checkout. Report the node
 count of `tests/orchestration/test_chat_intent_model.py` by `--collect-only -q` at C4, every
 `SKIPPED` line and the summary, and account for any difference from 1068 passed by that count.
 Then `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass`
 at `fail_count` 0.

G5 THE RED PROOFS — your tool `.agent/authored/f038-r7-mutations.py` takes a worktree path, and
 for each mutation below edits the named file INSIDE that worktree (asserting its FROM text occurs
 exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider -rf
 tests/orchestration/test_chat_intent_model.py` from the worktree's root after purging its
 `__pycache__` directories, with the worktree's root first on `PYTHONPATH`, restores the bytes,
 and prints one line per mutation: its label, the exit code, the failed count and the failing
 node ids, both read from the `FAILED` lines `-rf` prints. It runs an unmutated control first and
 last and ends with `restored byte-identical: True` and a final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each is a real behaviour change, the first
 nine in `chat_intent_model.py` and the last in `chat_intent.py`:
  r1 the model is asked even when the mechanical parse read an action or a question;
  r2 no confidence floor is applied;
  r3 the reply's task id is kept instead of the focused task;
  r4 a decision id outside the open set is kept;
  r5 argument names the verb does not take are kept;
  r6 a provider error escapes the parse;
  r7 an unset call function asks the model whatever the switch reads;
  r8 the call site is asked for the answer schema rather than `GeneratedChatIntent`;
  r9 a verb outside the chat's tables is not refused before the arguments are built;
  r10 a card never states its `Decision:` line.
 Run it: `git worktree add --detach .remedy-wt/f038-r7-mut <C4>`, then
 `python3 -B .agent/authored/f038-r7-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f038-r7-mut`
 and report its whole output. EVERY mutation must be red with at least one failing node; a
 mutation that stays green is reported as green, never papered over, and you then add the test
 that catches it in a commit before C5 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f038-r7-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 7`, which must show C5, C4, C3, C2, C1b, C1a and `bd0802867` in that
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
of feature F038, round 7, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 7, then T003's first part: the chat command finds the running cockpit, answers a question,
and confirms a card on a y/N line. State the open-findings count, 0, and the operator-questions
count, 1.

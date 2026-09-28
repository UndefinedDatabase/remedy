STEP F038 R4 — BOOK ROUND 3, THEN LAND T001's MODEL-WRITTEN ANSWER: the claim check, a switch that is off by default, the summary-role call and the mechanical fallback

GOAL
Round 3 is reviewed PASS at `47747a49`. Book it, record DECISION F038 D5, and extend
`packages/orchestration/chat_answer.py`: a cited sentence may state a number, a backtick span or a
URL only when an item it cites holds it; a new registered switch `chat.model_written`, off by
default, lets the summary model write the answer through one `resolve_role_config("summary")`
call; its reply passes the same check; and the mechanical answer, labelled with its reason,
stands in whenever the switch is off, the call fails, the reply does not parse or no sentence of
it is supported. The new call site joins `ROLE_CONFIG_CALL_SITES`. No test reaches a live model,
no file is written, and nothing imports the module yet.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests yourself against S1 to S7 below. Only the `.agent/` records travel
as payloads. Read DECISION F038 D5 in the records diff before you write code: it is the design
this specification implements. Before you write anything, read whole:
`packages/orchestration/chat_answer.py` and `tests/orchestration/test_chat_answer.py` as they
stand at `47747a49`; in `packages/orchestration/result_tour.py`, `GeneratedTourContent`,
`build_tour_prompt`, `PROVIDER_CALL_ERRORS`, `generate_result_tour`, `tour_model_written`,
`tour_call_fn` and `write_result_tour`'s use of `_UNSET_CALL_FN`; `make_structured_call_fn` in
`packages/orchestration/intake.py`; `run_structured_call` and `StructuredOutcome` in
`packages/orchestration/structured_outputs.py`; `FailureSignals` and `classify` in
`packages/orchestration/failure_postmortem.py`; the `tour.model_written` entry of
`_CONFIG_KEY_SPECS` and `write_environment_guide` in `packages/orchestration/config.py`;
`ROLE_CONFIG_CALL_SITES` in `packages/orchestration/model_routing.py`;
`TestTheCallSiteInventoryIsChecked` in `tests/orchestration/test_model_routing.py`; and the
switch tests of `tests/orchestration/test_result_tour.py` around
`test_unset_calls_tour_call_fn_only_when_the_switch_is_on`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f038-r4-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f038-r4/`           READ-ONLY. The reviewer's block.
  every other `.remedy-wt/f038-*` directory except your own, and `.remedy-wt/f038-review/`
                                  The reviewer's; do not touch them.
  `.remedy-wt/f038-r4-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Set environment variables inside tests with `monkeypatch.setenv` followed by
`reset_config()` from `packages.orchestration.config`, never on a command line. Never run npm or
npx.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f038-grounded-chat`, and `git log --oneline -1` must read `47747a499`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f038-r4/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f038-r4-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 67 | 11444 | bca963df465362b2a2bc1c6b0555a52bb7459335c83ee806b74ac5280dc389ce |
| plan.md | 28 | 937 | 5ed12bfd0216e26fb11446797cc7e57e76ad40bb7cec1f82b84b3433486ad3a7 |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `47747a49` into which it wrote the edits. It
appends round 3's gate entry to `.agent/live_review.md` and DECISION F038 D5 to
`.agent/decisions.md`.

THE SPECIFICATION. No `except Exception` anywhere and no `# noqa: BLE001`.
S1 THE CLAIM CHECK, in `check_answer_sentence`, AFTER the check that every citation resolves and
   BEFORE a sentence is found supported: the text searched is the ref and the text of each CITED
   item, and only those. Each claim token of the sentence with its citations removed — a URL
   (`https?://` and the non-space run after it), a backtick span, or a number (digits, optionally
   a decimal point and digits) — is taken without its backticks and without trailing `.`, `,`,
   `;`, `:`, `)`, `!` or `?`; the first one that does not occur in that text makes the sentence
   unsupported with `states <the token as taken>, which its cited items do not hold`. The refusal
   sentence and the other two outcomes are unchanged.
S2 THE REPLY SCHEMA AND LABELS. `CHAT_GENERATOR_SUMMARY_ROLE = "summary-role"`,
   `CHAT_NO_SUPPORTED_SENTENCE = "no_supported_sentence"`,
   `GENERATED_CHAT_ANSWER_SCHEMA_V = "generated_chat_answer_v1"`, and a pydantic model
   `GeneratedChatAnswer` with `SCHEMA_V: ClassVar[str] = GENERATED_CHAT_ANSWER_SCHEMA_V` and one
   field `answer: str`.
S3 THE PROMPT. `build_chat_prompt(question, evidence) -> str` joins with "\n", in order:
   `Question: <question>`; ""; `Evidence, each item numbered:`; `render_chat_evidence(evidence)`,
   or `(no items)` when that is ""; ""; `Rules:`; `- answer only from the numbered evidence
   above`; `- end every sentence with the number of each item it restates, as [n]`; `- copy
   numbers, names and paths exactly as the items hold them`; `- at most 5 sentences` (spelled
   from `CHAT_MECHANICAL_MAX_SENTENCES`); `- when no item answers the question, reply exactly:
   Not in evidence.` (spelled from `CHAT_NOT_IN_EVIDENCE`).
S4 THE SWITCH AND THE CALL. `chat_model_written() -> bool` reads the config key
   `chat.model_written` the way `tour_model_written` reads its own, the config import kept inside
   the function. `chat_call_fn()` is `make_structured_call_fn(GeneratedChatAnswer,
   model=resolve_role_config("summary").model)`, as `tour_call_fn` is built.
S5 THE ANSWER. `answer_chat_question(question, evidence, call_fn=<a private sentinel>) ->
   ChatAnswer`. With the sentinel, `call_fn` becomes `chat_call_fn()` when `chat_model_written()`
   and None otherwise. None → `mechanical_answer(question, evidence)` unchanged, labelled
   `mechanical`. Otherwise `run_structured_call(GeneratedChatAnswer, build_chat_prompt(...),
   call_fn, allow_parse_retry=True)`: an exception of `PROVIDER_CALL_ERRORS`, imported from
   `result_tour`, gives the mechanical answer with `generator` `mechanical:<classify(
   FailureSignals(exception=exc)).failure_class.value>`; an outcome that is not `ok` gives it with
   `mechanical:<classify(FailureSignals(error_class=outcome.error_class,
   error_text=outcome.hint)).failure_class.value>`; otherwise the reply's `answer` goes through
   `check_answer(..., generator=CHAT_GENERATOR_SUMMARY_ROLE)` and is returned when at least one
   sentence is supported, else the mechanical answer with `generator`
   `mechanical:no_supported_sentence`. The mechanical answer's sentences never change; only its
   label does (`dataclasses.replace`).
S6 THE KEY. In `_CONFIG_KEY_SPECS` of `packages/orchestration/config.py`, directly BEFORE the
   `tour.model_written` entry: `ConfigKeySpec(key="chat.model_written",
   env_var="REMEDY_CHAT_MODEL_WRITTEN", description=("Let the summary model write the grounded
   chat's answers (F038). Off by default: each answer is one summary model call, and a question
   makes no call the operator did not switch on; with it off, the chat answers from its evidence
   mechanically."), value_type=bool, default=False)`, the description split over string lines as
   its neighbour's is. Then regenerate the guide, never by hand: `python3 -c "from
   packages.orchestration.config import write_environment_guide; write_environment_guide()"`.
S7 THE INVENTORY. `ROLE_CONFIG_CALL_SITES` gains `("packages/orchestration/chat_answer.py",
   "summary")` directly after the `artifact_summary.py` pair. In
   `test_most_call_sites_still_pass_no_role_literal` the two pinned counts become 11 and 6, and
   its comment reads eleven call sites and six literal roles and adds "and F038 added
   chat_answer.py's `summary`" to its list. In `tour_call_fn`'s docstring in `result_tour.py`,
   "one of the ten entries" becomes "one of the eleven entries". Nothing else in those files
   changes.

THE TESTS, in `tests/orchestration/test_chat_answer.py`; no existing test changes. At least, one
each: over a two-item set — the first `Round 2 (repair): tests passed` at ref `T001#2`, the second
`The Definition of Done ran: pytest -q` — the sentences `Round 2 passed [1].`, `3 tests failed
[1].`, ``Run `pytest -q` [2].``, ``Run `make all` [2].``, `See https://deploy.example/app [1].` and
``Round 2 ran `pytest -q` [1].`` read supported, then unsupported naming `3`, supported,
unsupported naming `make all`, unsupported naming the URL, and unsupported naming `pytest -q`
(its cited item does not hold it, though the other item does); the prompt starts with the
question line, holds `[1] node:T001 — Tests: passed` for a one-item set, ends with the refusal
rule, and holds `(no items)` for an empty set; the switch reads False by default and True after
`REMEDY_CHAT_MODEL_WRITTEN=1` is set and the config reset; `chat_call_fn` asks the `summary` role
and hands `GeneratedChatAnswer` and the role's model to `make_structured_call_fn` (both replaced
on the module by stand-ins); with no call function handed in, a spy standing in for
`chat_call_fn` is not called while the switch is off and called once when it is on; a stub reply
`Tests passed [1]. It was quick.` is kept, labelled `summary-role`, supported then unsupported; a
stub reply `It shipped [4].` falls back to `mechanical:no_supported_sentence` with the mechanical
sentence; a stub raising `ConnectionError` and a stub replying `not json` each fall back with a
`mechanical:` label other than `mechanical:no_supported_sentence`; and THE MODEL CANARY — for each
of the round 3 node canary questions, a stub replying `The deployment URL is
https://deploy.example/app [1].` over a real node scope yields exactly the one supported sentence
"Not in evidence.", labelled `mechanical:no_supported_sentence`. Stubs are plain functions
`(prompt, attempt) -> str` returning JSON such as `{"answer": "..."}`; no test calls
`chat_call_fn` unreplaced with the switch on.

BUNDLE — the commits are C1a, C1b, C2, C3, C4 and C5, in this order.

C1a — copy this block and the plan payload
  `.agent/authored/f038-r4-block.md` := this block and `.agent/authored/f038-r4-plan.md` :=
  plan.md, by `shutil.copyfile`.
  Subject: `F038 R4 C1a: copy round 4 block and plan payload into .agent/authored/`
  Its insertions are this block's line count plus 28. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C1b — copy the records diff
  `.agent/authored/f038-r4-records.diff` := records.diff.
  Subject: `F038 R4 C1b: copy round 4 records diff into .agent/authored/`
  Expected insertions: 67.

C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F038 R4 C2: book round 3 and record DECISION F038 D5`
  Expected by `git show --numstat` (insertions and deletions): 49/0 decisions.md, 2/0
  live_review.md, 6/9 plan.md.

C3 — THE CODE: S1 to S5 in `chat_answer.py`, S6 in `config.py` and the regenerated
  `docs/guides/environment.md`, and S7 in `model_routing.py`, `result_tour.py` and
  `tests/orchestration/test_model_routing.py`.
  Subject: `F038 R4 C3: let the summary model answer the chat behind a switch, with a claim check`

C4 — THE TESTS AND THE TOOL: `tests/orchestration/test_chat_answer.py` and your mutation tool (G5)
  saved as `.agent/authored/f038-r4-mutations.py`.
  Subject: `F038 R4 C4: test the claim check, the switch and the model answer's fallbacks`

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F038 R4 C5: rewrite handoff for round 4`
  Then `git push origin feature/f038-grounded-chat`. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects (C4a and C4b), and say so.
3. The round's whole tracked path set is: the `.agent/authored/f038-r4-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `packages/orchestration/chat_answer.py`, `packages/orchestration/config.py`,
   `docs/guides/environment.md`, `packages/orchestration/model_routing.py`,
   `packages/orchestration/result_tour.py`, `tests/orchestration/test_model_routing.py`,
   `tests/orchestration/test_chat_answer.py`, and `.agent/handoff.md`. Report the list you
   measure with `git diff --name-only 47747a499` at the branch tip after C5. Do NOT touch
   anything under `apps/`, any other file under `packages/` or `docs/`, `README.md`,
   `tests/orchestration/import_reachability_allowlist.txt`, `tests/test_no_orphan_modules.py`,
   `.agent/context.md`, `.agent/prose_slips.md`, `.agent/candidates.md` or
   `.agent/operator_questions.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong may be corrected before C5, and the correction is declared. An
   EXISTING test other than the one S7 names that goes red is never edited to pass; report it and
   stop.
5. NOTHING IS MERGED OR REWRITTEN. No `gh pr merge`, no `gh pr create`, no checkout of `main`, no
   branch deletion, no force-push, no `git stash`, and no `git commit --amend` or any other
   rewrite of a commit, pushed or not: a wrong commit subject is declared, never amended.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F038's belongs to its closure. Never switch the chat's model on outside a test's own
   environment, and never run anything that reaches a live model.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f038-r4-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f038-r4/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree. Report each path beside the hash you read:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2390061 | f8ddcf879acf3c37c598c53e9455c8b485d6d1f31b5741cfa5857899be2115b1 |
 | .agent/live_review.md | 318007 | ca0fba7a18f16d905bf9265e10cab007bdcc5164dda2e4f66582393a575fe42a |
 | .agent/plan.md | 937 | 5ed12bfd0216e26fb11446797cc7e57e76ad40bb7cec1f82b84b3433486ad3a7 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT read with `git show <C2>:<path>` (the
 reviewer read `[]`); and `git diff --name-only <C1b> <C2>`, which must name exactly the paths of
 the table above.

G3 THE CODE — `python3 -m ruff check packages/orchestration/chat_answer.py
 packages/orchestration/config.py packages/orchestration/model_routing.py
 packages/orchestration/result_tour.py tests/orchestration/test_model_routing.py
 tests/orchestration/test_chat_answer.py` at C4, with its real exit code. Then report, quoted from
 `git show <C3>`, the claim check of S1, the whole of `answer_chat_question`, and the lines C3
 adds to `docs/guides/environment.md`.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_chat_answer.py tests/orchestration/test_chat_evidence.py tests/orchestration/test_model_routing.py tests/orchestration/test_config.py tests/orchestration/test_env_registry.py tests/orchestration/test_result_tour.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_subprocess_timeouts.py tests/regression/test_named_bugs.py tests/test_path_utils.py tests/test_data_paths.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -12; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection serially in the primary checkout at `47747a499` and read
 `1328 passed, 9 skipped, 1 warning` at exit code 0; over its simulation tree, a fresh worktree
 carrying this round's records and its own version of the code and tests, it read
 `1337 passed, 11 skipped, 1 warning` at exit code 0, the two further skips being the vitest
 tests of `tests/orchestration/test_test_runner.py`, which run in the primary checkout. Report
 the node count of `tests/orchestration/test_chat_answer.py` by `--collect-only -q` at
 `47747a499` and at C4, every `SKIPPED` line and the summary, and account for any difference from
 1328 passed by those counts. Then `python3 -m apps.cli.main integrity check --json`, which must
 read all six checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — your tool `.agent/authored/f038-r4-mutations.py` takes a worktree path, and
 for each mutation below edits the named module INSIDE that worktree (asserting its FROM text
 occurs exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider
 tests/orchestration/test_chat_answer.py` from the worktree's root after purging its
 `__pycache__` directories, with the worktree's root first on `PYTHONPATH`, restores the bytes,
 and prints one line per mutation: its label, the exit code, the failed count and the failing
 node ids. It runs an unmutated control first and last and ends with
 `restored byte-identical: True` and a final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each is a real behaviour change in
 `chat_answer.py` unless named otherwise:
  q1 the claim check never finds a token missing;
  q2 the claim check reads every item of the set instead of the cited ones;
  q3 with no call function handed in, `chat_call_fn()` is asked whatever the switch;
  q4 `chat_call_fn` asks the `planner` role;
  q5 only `KeyError` is caught around the call;
  q6 a reply with no supported sentence is kept;
  q7 a fallback's label omits its reason;
  q8 the prompt omits the refusal rule;
  q9 an outcome that is not `ok` is not a fallback;
  q10 in `config.py`, the switch defaults to on.
 Run it: `git worktree add --detach .remedy-wt/f038-r4-mut <C4>`, then
 `python3 -B .agent/authored/f038-r4-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f038-r4-mut`
 and report its whole output. EVERY mutation must be red with at least one failing node; a
 mutation that stays green is reported as green, never papered over, and you then add the test
 that catches it in C4 before C5 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f038-r4-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 7`, which must show C5, C4, C3, C2, C1b, C1a and `47747a499` in that
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
of feature F038, round 4, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 4, then T002: the intent parse over the exposed commands, the action cards and their
confirmation. State the open-findings count, 0, and the operator-questions count, 1.

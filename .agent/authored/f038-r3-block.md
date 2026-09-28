STEP F038 R3 — BOOK ROUND 2, THEN LAND T001's GROUNDED ANSWER: the citation check, the mechanical answer and the canary suite in both scopes

GOAL
Round 2 is reviewed PASS at `fe18ab6d`. Book it, record DECISION F038 D4, and land a NEW module
`packages/orchestration/chat_answer.py`: the check that marks every sentence of an answer
supported or unsupported against a composed evidence set, the renderer that marks the unsupported
ones, and the mechanical answer that restates the items a question names or says
"Not in evidence." — with the canary suite of absent-fact questions over a real node scope and a
real project scope. Align the prompt trace's run-id check in `chat_evidence.py` with
`run_rounds_view`'s. No model is called, no file is written, and nothing imports the new module.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests yourself against S1 to S6 below. Only the `.agent/` records travel
as payloads. Read DECISION F038 D4 in the records diff before you write code: it is the design
this specification implements. Before you write anything, read whole:
`packages/orchestration/chat_evidence.py`, `tests/orchestration/test_chat_evidence.py` and
`tests/test_no_orphan_modules.py` as they stand at `fe18ab6d`, and `build_task_run_rounds` in
`packages/orchestration/run_rounds_view.py`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f038-r3-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f038-r3/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f038-r1-*`, `.remedy-wt/f038-r2-*`, `.remedy-wt/f038-r3-dry/`,
  `.remedy-wt/f038-r3-sim/`, `.remedy-wt/f038-r3-src/`, `.remedy-wt/f038-review/`
                                  The reviewer's; do not touch them.
  `.remedy-wt/f038-r3-worker/`    YOURS for logs and scripts; create it if absent. All are
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
   `feature/f038-grounded-chat`, and `git log --oneline -1` must read `fe18ab6d8`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f038-r3/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f038-r3-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 56 | 10275 | 289b865a0a118f2ef66ad7b5da752fa42c925c6fd99cfe3eb91cc9b1a0ecdb01 |
| plan.md | 31 | 1058 | 424443393cfee0196203a8e46ec338cf226cc02a208ebb8206c3db0b3791d566 |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `fe18ab6d` into which it wrote the edits. It
appends round 2's gate entry to `.agent/live_review.md` and DECISION F038 D4 to
`.agent/decisions.md`.

THE SPECIFICATION. No `except Exception` anywhere and no `# noqa: BLE001`.
S1 THE MODULE, a NEW FILE at `packages/orchestration/chat_answer.py`. A docstring naming F038 T001
   and DECISION F038 D4, with one sentence stating that Remedy deliberately does not let an
   answer's honesty rest on a prompt. At module level it imports the standard library and, from
   `packages.orchestration`, only `chat_evidence.ChatEvidenceSet`. Constants
   `CHAT_NOT_IN_EVIDENCE = "Not in evidence."`, `CHAT_UNSUPPORTED_MARK = "[unsupported]"`,
   `CHAT_GENERATOR_MECHANICAL = "mechanical"`, `CHAT_MECHANICAL_MAX_SENTENCES = 5`,
   `CHAT_KEYWORD_MIN_CHARS = 3`, and `CHAT_QUESTION_STOPWORDS`, a frozenset of exactly: about,
   and, any, are, can, did, does, for, from, had, has, have, how, its, the, that, there, this, was,
   were, what, when, where, which, who, why, with, you, your. A citation is `[<digits>]`.
S2 THE SHAPES. Frozen dataclasses `ChatAnswerSentence(text: str, citations: tuple[int, ...],
   supported: bool, problem: str)` and `ChatAnswer(scope: str, subject: str, question: str,
   generator: str, sentences: tuple[ChatAnswerSentence, ...])`, the latter with a property
   `unsupported_count`, the number of sentences not supported.
S3 THE SPLIT. `split_answer_sentences(text) -> list[str]`: each line of `text`, stripped, is split
   after every `.`, `!` or `?` that whitespace follows; each fragment is stripped and an empty one
   dropped; a fragment that, with its citations removed and then stripped of spaces, `.`, `!` and
   `?`, is empty joins the sentence before it with one space (when there is one); every other
   fragment is a sentence. So `"A [1]. B [2]! C?\nD [3]"` gives `A [1].`, `B [2]!`, `C?`, `D [3]`,
   and `"A. [1] [2]"` gives the one sentence `A. [1] [2]`.
S4 THE CHECK. `check_answer_sentence(sentence, evidence) -> ChatAnswerSentence`: `citations` are
   the sentence's citation numbers in order. A sentence that, stripped, equals
   `CHAT_NOT_IN_EVIDENCE` and cites nothing is supported with problem "". Otherwise a sentence
   citing nothing is unsupported with `cites no evidence item`; one citing any number outside 1 to
   the set's item count is unsupported with `cites <those numbers as [n], joined by ", ">, which
   the evidence set does not hold`; else it is supported with problem "". `check_answer(text,
   evidence, *, question, generator) -> ChatAnswer` checks every sentence of
   `split_answer_sentences(text)`, or the one sentence `CHAT_NOT_IN_EVIDENCE` when that list is
   empty, and takes `scope` and `subject` from the set. `render_chat_answer(answer) -> str` joins
   the sentences with one space, each unsupported one followed by a space and
   `CHAT_UNSUPPORTED_MARK`.
S5 THE MECHANICAL ANSWER. `question_keywords(question) -> tuple[str, ...]`: the lower-cased
   question's runs of `[a-z0-9]`, kept when at least `CHAT_KEYWORD_MIN_CHARS` long and not a
   stopword, each once, in first-seen order. `mechanical_answer(question, evidence) -> ChatAnswer`
   scores each item by how many keywords BEGIN at least one of the `[a-z0-9]` runs of its lower-
   cased text and ref together; keeps the items scoring at least 1, highest score first and the
   lower item number first on a tie, at most `CHAT_MECHANICAL_MAX_SENTENCES`; and makes each kept
   item ONE sentence, `<its text with trailing full stops removed> [<n>].`, checked WHOLE by
   `check_answer_sentence` and never split again, because an item's text may itself hold a full
   stop. With no item kept, the one sentence is `CHAT_NOT_IN_EVIDENCE`. `generator` is
   `CHAT_GENERATOR_MECHANICAL`; `scope` and `subject` come from the set.
S6 THE COMPANIONS. In `packages/orchestration/chat_evidence.py`, the prompt trace's run-id check
   calls `fullmatch` instead of `match`, as `run_rounds_view` does, so a run id with a trailing
   newline is no run; nothing else in that file changes. In `ALLOWED_UNWIRED` of
   `tests/test_no_orphan_modules.py`, the `chat_evidence.py` line is REMOVED, because
   `chat_answer.py` now imports it, and in its place, between the `bench_run.py` and
   `ci_budgets.py` entries, comes `("packages/orchestration/chat_answer.py", "F038's grounded
   answer, the citation check and the mechanical answer; the chat command wires it in a later
   round (DECISION F038 D4) and removes this line")`, split over lines as its neighbours are.

THE TESTS. A NEW FILE `tests/orchestration/test_chat_answer.py`, `REMEDY_DATA_DIR` under
`tmp_path`, at least one test each: the two split examples of S3 and a blank text; an answer of
four sentences over a two-item set — citing [1], citing [2], citing [3], citing nothing — reads
supported, supported, unsupported with the [3] problem, unsupported with the no-citation problem,
`unsupported_count` 2, scope, subject, question and generator as given, and renders with the
mark after the last two; "Not in evidence.", an empty text and a text of one newline each check
to the one supported sentence "Not in evidence."; `question_keywords` of a question holding a
stopword, a two-letter word and a repeated word; over a three-item set, a question sharing one
keyword with the second item's text and one with the third's ref-and-text gives those two
sentences in item order, supported, and an item text holding an inner full stop stays one
sentence; eight matching items give five sentences; "Did the tests pass?" over a real node scope
cites the item `Tests: passed`; and THE CANARY SUITE — "What was the deployment URL?", "Who
approved the invoice?" and "Which database migration ran in production?" over a real node scope,
and "What is the office address?", "Which customer paid the invoice?" and "How many employees
work there?" over a real project scope linking one saved job — each answered by
`mechanical_answer` with exactly the one supported sentence "Not in evidence.". In
`tests/orchestration/test_chat_evidence.py`, one new test: a task whose `run_id` is `abcdef01`
followed by a newline yields `Prompt trace: not recorded (no_run_recorded)`. No existing test
changes.

BUNDLE — the commits are C1a, C1b, C2, C3, C4 and C5, in this order.

C1a — copy this block and the plan payload
  `.agent/authored/f038-r3-block.md` := this block and `.agent/authored/f038-r3-plan.md` :=
  plan.md, by `shutil.copyfile`.
  Subject: `F038 R3 C1a: copy round 3 block and plan payload into .agent/authored/`
  Its insertions are this block's line count plus 31. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C1b — copy the records diff
  `.agent/authored/f038-r3-records.diff` := records.diff.
  Subject: `F038 R3 C1b: copy round 3 records diff into .agent/authored/`
  Expected insertions: 56.

C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F038 R3 C2: book round 2 and record DECISION F038 D4`
  Expected by `git show --numstat` (insertions and deletions): 38/0 decisions.md, 2/0
  live_review.md, 7/6 plan.md.

C3 — THE CODE: `packages/orchestration/chat_answer.py`, S6's line in `chat_evidence.py` and S6's
  change to `tests/test_no_orphan_modules.py`.
  Subject: `F038 R3 C3: check a chat answer's citations and answer mechanically`

C4 — THE TESTS AND THE TOOL: `tests/orchestration/test_chat_answer.py`, the new test in
  `tests/orchestration/test_chat_evidence.py`, and your mutation tool (G5) saved as
  `.agent/authored/f038-r3-mutations.py`.
  Subject: `F038 R3 C4: test the answer check, the mechanical answer and the canary suite`

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F038 R3 C5: rewrite handoff for round 3`
  Then `git push origin feature/f038-grounded-chat`. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects (C4a and C4b), and say so.
3. The round's whole tracked path set is: the `.agent/authored/f038-r3-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `packages/orchestration/chat_answer.py`, `packages/orchestration/chat_evidence.py`,
   `tests/test_no_orphan_modules.py`, `tests/orchestration/test_chat_answer.py`,
   `tests/orchestration/test_chat_evidence.py`, and `.agent/handoff.md`. Report the list you
   measure with `git diff --name-only fe18ab6d8` at the branch tip after C5. Do NOT touch
   anything under `apps/` or `docs/`, any other file under `packages/`,
   `tests/orchestration/import_reachability_allowlist.txt`, `.agent/context.md`,
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md` or
   `README.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong may be corrected before C5, and the correction is declared. An
   EXISTING test that goes red is never edited to pass; report it and stop.
5. NOTHING IS MERGED OR REWRITTEN. No `gh pr merge`, no `gh pr create`, no checkout of `main`, no
   branch deletion, no force-push, no `git stash`, and no `git commit --amend` or any other
   rewrite of a commit, pushed or not: a wrong commit subject is declared, never amended.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F038's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f038-r3-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f038-r3/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree. Report each path beside the hash you read:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2385590 | fa55e0b8e0050b8afff21549e497bf09821ef394f079f7ae0be86bcb236094f8 |
 | .agent/live_review.md | 315369 | d8369556b1ed80a387b11d3af10bd2e39987aec2d30fff6b59d3d2daa4108e93 |
 | .agent/plan.md | 1058 | 424443393cfee0196203a8e46ec338cf226cc02a208ebb8206c3db0b3791d566 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT read with `git show <C2>:<path>` (the
 reviewer read `[]`); and `git diff --name-only <C1b> <C2>`, which must name exactly the paths of
 the table above.

G3 THE CODE — `python3 -m ruff check packages/orchestration/chat_answer.py
 packages/orchestration/chat_evidence.py tests/orchestration/test_chat_answer.py
 tests/orchestration/test_chat_evidence.py tests/test_no_orphan_modules.py` at C4, with its real
 exit code. Then report, quoted from `git show <C3>`, the whole of `split_answer_sentences`,
 `check_answer_sentence` and `mechanical_answer`.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_chat_answer.py tests/orchestration/test_chat_evidence.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_subprocess_timeouts.py tests/regression/test_named_bugs.py tests/test_path_utils.py tests/test_data_paths.py tests/orchestration/test_env_registry.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/cli/test_golden_path.py 2>&1 | tail -4; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection, less `tests/orchestration/test_chat_answer.py`, serially in the
 primary checkout at `fe18ab6d8` and read `437 passed, 6 skipped` at exit code 0, the six skips
 being the F252 quarantine; over its simulation tree, a fresh worktree carrying this round's
 records and its own version of the code and tests, the whole selection read
 `449 passed, 8 skipped` at exit code 0, the two further skips being the vitest tests of
 `tests/orchestration/test_test_runner.py`, which run in the primary checkout. Report the node
 counts of `tests/orchestration/test_chat_answer.py` and `tests/orchestration/test_chat_evidence.py`
 by `--collect-only -q` at C4, every `SKIPPED` line and the summary, and account for any
 difference from 437 passed by those counts (`test_chat_evidence.py` holds 22 at `fe18ab6d8`).
 Then `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0.

G5 THE RED PROOFS — your tool `.agent/authored/f038-r3-mutations.py` takes a worktree path, and
 for each mutation below edits the named module INSIDE that worktree (asserting its FROM text
 occurs exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider
 tests/orchestration/test_chat_answer.py tests/orchestration/test_chat_evidence.py` from the
 worktree's root after purging its `__pycache__` directories, with the worktree's root first on
 `PYTHONPATH`, restores the bytes, and prints one line per mutation: its label, the exit code,
 the failed count and the failing node ids. It runs an unmutated control first and last and ends
 with `restored byte-identical: True` and a final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each is a real behaviour change in
 `chat_answer.py` unless named otherwise:
  p1 a sentence citing nothing reads supported;
  p2 a citation outside the set is accepted;
  p3 "Not in evidence." needs a citation;
  p4 a fragment of citation markers stands as its own sentence;
  p5 an empty answer has no sentence;
  p6 a keyword matches whole words only;
  p7 on a tied score the higher item number comes first;
  p8 the mechanical answer restates every matching item;
  p9 the mechanical answer's sentences are split again;
  p10 the renderer omits the unsupported mark;
  p11 stopwords count as keywords;
  p12 in `chat_evidence.py`, the run-id check calls `match` again.
 Run it: `git worktree add --detach .remedy-wt/f038-r3-mut <C4>`, then
 `python3 -B .agent/authored/f038-r3-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f038-r3-mut`
 and report its whole output. EVERY mutation must be red with at least one failing node; a
 mutation that stays green is reported as green, never papered over, and you then add the test
 that catches it in C4 before C5 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f038-r3-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 7`, which must show C5, C4, C3, C2, C1b, C1a and `fe18ab6d8` in that
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
of feature F038, round 3, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 3, then T001's model-written answer: a chat routing class, a switch that is off by default,
the same check over its reply, and the mechanical answer as its fallback. State the open-findings
count, 0, and the operator-questions count, 1.

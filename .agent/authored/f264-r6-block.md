STEP F264 R6 — T003's FIRST HALF: the acknowledgement, on the stream and in `remedy chat show`

GOAL
Book round 5's PASS, record DECISION F264 D6, and land T003's first half: the consumption event
becomes the acknowledgement — it and its sealed marker gain `understood`, a restatement that
quotes the message verbatim with the task round it took effect from and, for a mission's job,
the contract criterion and mission round; the stream carries exactly that on that event kind
alone; and `remedy chat show <job_id>` lists every message as acknowledged, waiting or not taken
in, read from the same run-log events the stream carries.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

WHY THIS ROUND
T5_F264.md T003 is "the acceptance-visible half": an acknowledgement that names what was
understood and the round it applies from, in the CLI and the cockpit, from one event. DECISION
F264 D6 (in the records.diff payload) fixes the event, the restatement, the stream field and the
three statuses. The cockpit's rendering follows next round.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f264-r6-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f264-r6-scratch/`   The reviewer's scripts; do not edit or delete them.
  `.remedy-wt/f264-r6-worker/`    YOURS for logs and scripts. All three are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, `cd <dir> && git ...`, and multi-operation
one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe pytest.
Use `git -C <path>` rather than `cd`. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`). A heredoc containing a dollar-brace is refused: write such a
script to a file under your own directory and run the file.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`: report `pwd`
   and use absolute paths or `git -C /home/decodeux/Repos/remedy` throughout.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f264-steering-channel`, and `git log --oneline -1` must read `70664b29`. Report
   all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f264-r6-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f264-r6-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 49 | 10233 | 345dcc4ffe5d585b0dfa98a39e36cf0118684d4ca93ce6128ed47b51bbf2dd46 |
| plan.md | 28 | 980 | 98a6d8e4b283d42a6a2e06038d0baa54037aa6390f9f179278b676366658885a |
| product.diff | 287 | 14726 | d52703711fa4507727e1653f95d45d979be8eed75aee334a294f963ee90d2185 |
| mutations.py | 71 | 2768 | 1c4df10115929279db0ea932a54e8518fc44b426fbbf9b6a8d71323eec79795b |
| tests.diff | 119 | 6801 | 943005eb26cf357ba988e351bb05568c79960df059805236de2b28cc3f87bb42 |

`plan.md` is a REWRITE of `.agent/plan.md`. The `.diff` files go on with `git apply`; the
reviewer generated every one from a tree at `70664b29` and applied all of them, in the commit
order below, to a fresh worktree at `70664b29` with `git apply --check` then `git apply`, every
one at real exit code 0. `records.diff` appends the `Gate: F264 R5 —` entry to
`.agent/live_review.md` and DECISION F264 D6 to `.agent/decisions.md`. `product.diff` edits
`apps/cli/command_catalog.py`, `apps/cli/commands/chat_cmd.py`, `docs/guides/exit-codes.md`,
`packages/orchestration/steering.py` and `packages/orchestration/ui_server.py`. `tests.diff`
edits `tests/cli/test_chat_cmd.py`, `tests/orchestration/test_steering.py`,
`tests/orchestration/test_steering_mission.py` and `tests/ui_server/test_sse_stream.py`.
`mutations.py` is a TOOL for G5: it is run, never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C2, C3, C4 and C5, in this order.

C1a — copy this block and the bookkeeping payloads
  `.agent/authored/f264-r6-block.md` := this block, and one
  `.agent/authored/f264-r6-<name>` for each of records.diff and plan.md, keeping each
  payload's own file name. All by `shutil.copyfile`.
  Subject: `F264 R6 C1a: copy round 6 block and bookkeeping payloads into .agent/authored/`
  Its insertions are this block's line count plus 77. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the product and test payloads
  `.agent/authored/f264-r6-<name>` for each of product.diff, mutations.py and tests.diff.
  Subject: `F264 R6 C1b: copy round 6 product and test payloads into .agent/authored/`
  Expected insertions: 477.

C2 — THE RECORDS, in ONE commit (amend0917-throughput rule 4):
   1. `git apply` records.diff  → `.agent/live_review.md` and `.agent/decisions.md`
   2. rewrite `.agent/plan.md` := plan.md
  Subject: `F264 R6 C2: book round 5's PASS, record DECISION F264 D6 and advance the plan`
  Expected insertions by `git show --numstat`: 31 decisions.md, 2 live_review.md, 7 plan.md.

C3 — THE PRODUCT: `git apply` product.diff, then `git add` its five paths.
  Subject: `F264 R6 C3: acknowledge a steering message with its restatement and round`
  Expected insertions: 15 command_catalog.py, 49 chat_cmd.py, 1 exit-codes.md, 85 steering.py,
  19 ui_server.py.

C4 — THE TESTS: `git apply` tests.diff and `git add` its four paths.
  Subject: `F264 R6 C4: test the acknowledgement on the stream and in remedy chat show`
  Expected insertions: 36 test_chat_cmd.py, 25 test_steering.py, 9 test_steering_mission.py,
  14 test_sse_stream.py.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F264 R6 C5: rewrite handoff for round 6`
  Then `git push origin feature/f264-steering-channel`. Do NOT create a pull request: the
  branch opens one at F264's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f264-r6-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, the five paths
   product.diff edits and the four paths tests.diff edits (both listed under PAYLOADS), and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only 70664b29 HEAD`
   after C5. Do NOT touch `.agent/prose_slips.md`, `.agent/candidates.md`,
   `.agent/operator_questions.md`, `.agent/context.md`, `README.md`, `docs/roadmap/STATUS.md`
   or `docs/roadmap/features/T5_F264.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch
   deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees, their branches, the reviewer's worktrees whose
   names begin `.remedy-wt/f264-`, and every existing stash alone. The worktree G5 adds goes
   under `.remedy-wt/`, is removed as that step's last action, and `git worktree list` is
   reported afterwards (finding R-0940).
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run
   and F264's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f264-r6-*` copy byte for
 byte with its source (the block copy against `.remedy-wt/f264-r6-block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS — at C2, the sha256 of each file below, read with `git show <C2>:<path>`,
 equals the reviewer's reading, which its simulation printed from a tree it built by applying
 these payloads at `70664b29`:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 320467 | 38cee9eec59dc84c44e8d084d94b2810ebad7131212b2ffecc9d97f4691bfe50 |
 | .agent/decisions.md | 1953336 | a35641fe23260ab419be247da1444fc3257440aab05e570361d292403bd6d8c7 |
 | .agent/plan.md | 980 | 98a6d8e4b283d42a6a2e06038d0baa54037aa6390f9f179278b676366658885a |
 Also: among the lines C2's diff ADDS to `.agent/live_review.md`, the count of those beginning
 `Gate: F264 R5 — ` (the reviewer's simulation read 1); the open set by distinct id, computed
 with `open_finding_ids` from `scripts/rotate_live_review.py` over the file's TEXT, at
 `70664b29` and at C2, with the set difference in both directions (the reviewer read 3 and 3 —
 R-0499, R-0950 and R-1008 — both differences empty); and `git diff --name-only <C1b> <C2>`,
 which must name exactly the three record paths C2 writes.

G3 THE PRODUCT — at C4, the sha256 of each file below, read with `git show <C4>:<path>`,
 equals the reviewer's simulated reading:
 | path | bytes | sha256 |
 |---|---|---|
 | apps/cli/command_catalog.py | 113604 | e436dd90b5ac3377d14a6fb5441c1fe2b61910b6b6b7466a97b725af80485334 |
 | apps/cli/commands/chat_cmd.py | 5462 | 563652648043b24734c270cd4ed0d47a36d7b98323992a1131c27202977b602a |
 | docs/guides/exit-codes.md | 3983 | 4d7a5e257ac8798f369a48ad96bc77fe41f67499f5419b1c85af19031742585d |
 | packages/orchestration/steering.py | 19122 | 51d5dcca6a442aa38af27ea9fec399dc6a699e8773db3de9eb2ca5723380ea0c |
 | packages/orchestration/ui_server.py | 152364 | 5751ab162bf3b5c1528646b8c74e0bc7f30b87253b982850ad29c17260b97845 |
 | tests/cli/test_chat_cmd.py | 5003 | 6bb088c4a307da1dc6faee9e4f288308d143f1f7ad72c9399f4cf62e778be7e2 |
 | tests/orchestration/test_steering.py | 10360 | bc46230ad83a6370813074f266b912d34ff7a86d7f6040e87869202fa53ce277 |
 | tests/orchestration/test_steering_mission.py | 3982 | 1379084fc5fe394fbf8f3e607e69d64ab73643502fec5f38193c94b81528a9d2 |
 | tests/ui_server/test_sse_stream.py | 28427 | c684d8ecb0226a43bbd3e03d2f354a3233d4072b1257c9b211d50345da0876f3 |
 Also `git diff --name-only <C2> <C3>` and `<C3> <C4>`, which must name exactly the paths C3
 and C4 list.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_steering.py tests/orchestration/test_steering_mission.py tests/orchestration/test_steering_consumption.py tests/cli/test_chat_cmd.py tests/cli/test_cli_ux.py tests/cli/test_exit_codes.py tests/cli/test_advertised_commands.py tests/test_command_catalog.py tests/ui_server/test_sse_stream.py tests/ui_server/test_command_channel.py tests/ui_server/test_command_dispatch.py tests/orchestration/test_event_names.py tests/ui_contracts/test_humanize_catalog.py tests/docs/ tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path, serially, inside its sim
 worktree carrying C2 to C4 and read `1243 passed, 1 skipped` at real exit code 0; the primary
 checkout carries the UI toolchain a worktree lacks, so a skip may pass there. Report what you
 read. Then `python3 -m ruff check packages/orchestration/steering.py
 packages/orchestration/ui_server.py apps/cli/commands/chat_cmd.py apps/cli/command_catalog.py
 tests/orchestration/test_steering.py tests/orchestration/test_steering_mission.py
 tests/cli/test_chat_cmd.py tests/ui_server/test_sse_stream.py`, real exit code 0, and
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f264-r6-mut <C4>`, then
 `python3 -B .remedy-wt/f264-r6-payloads/mutations.py .remedy-wt/f264-r6-mut` and report its
 whole output. The script asserts each FROM occurs exactly once, applies it, runs
 `tests/orchestration/test_steering.py`, `tests/orchestration/test_steering_mission.py`,
 `tests/cli/test_chat_cmd.py` and `tests/ui_server/test_sse_stream.py` under `python3 -B`,
 restores the bytes, and runs an unmutated control first and last. The reviewer read, over the
 same script against its own tree carrying C2 to C4:
 control_before `114 passed` at exit 0;
 m1 (the event carries no restatement) 2 failed at exit 1;
 m2 (the restatement names no round) 2 failed at exit 1;
 m3 (the mission half left out of the restatement) 1 failed at exit 1;
 m4 (a message an ended job never took in shown as waiting) 2 failed at exit 1;
 m5 (the stream drops the acknowledgement) 1 failed at exit 1;
 m6 (the task read only from the event's metadata) 2 failed at exit 1;
 control_after `114 passed` at exit 0; every `restored byte-identical` line True.
 Then `git worktree remove --force .remedy-wt/f264-r6-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 7`, which must show C5, C4, C3, C2, C1b, C1a and `70664b29` in that
 order; `git worktree list`, which must show the primary checkout, the `.remedy-wt/job-*`
 worktrees and the reviewer's `.remedy-wt/f264-*` worktrees constraint 6 names, and nothing
 else; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be
 EMPTY. These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F264, round 6, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 6, then T003's second half — the cockpit renders the acknowledgement from the stream,
under the steering input. State the open-findings count, 3, and the operator-questions count, 0.

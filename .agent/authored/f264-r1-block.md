STEP F264 R1 — CLAIM F264 AND LAND T001's FIRST HALF: the sealed steering record and `remedy chat`

GOAL
Pull request 270 is merged; `main` is at `ef4cb503` and F264 is the next unchecked line. Cut
its branch, claim it, re-head the live review record, record DECISION F264 D1, and land the
first half of T001: `packages/orchestration/steering.py`, which accepts a steering message,
writes it as a sealed record under the job's evidence and only then certifies it into the run
log, and `remedy chat <job_id> "<message>"`, its first caller, with the tests and red proofs.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

WHY THIS IS FIRST
T5_F264.md's Orchestrator brief: T001 first and alone, because a persisted, certified message
with no consumer is a complete, testable thing. DECISION F264 D1 (the decisions.diff payload)
fixes the record: job-keyed, sealed, create-once, certified by one run-log event written after
the record is on disk, refused for an ended job. The cockpit's route is next round's work.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f264-r1-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f264-r1-scratch/`   The reviewer's scripts; do not edit or delete them.
  `.remedy-wt/f264-r1-worker/`    YOURS for logs and scripts. All three are gitignored.

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
2. `git status --porcelain` must be empty, `git branch --show-current` must read `main`,
   and `git log --oneline -1` must read `ef4cb503`. Report all three. Then
   `git checkout -b feature/f264-steering-channel` and report the branch. Do NOT pull: the
   Open PR Gate ran before you and `main` is already at the merge commit.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f264-r1-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f264-r1-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| status.diff | 13 | 519 | f446613eb65d820d17632eb21fab10f30ed90be69b4d9bd064b2fc011c3846cc |
| rehead.diff | 62 | 6609 | 2a024fdb0fb93bb16a4efd93a12b322c5acc353d7b93a67b3e125388b72af77c |
| plan.md | 33 | 1186 | 5f1928decf859545d33bc454751f62ad6da8c57ed44ba5950c6ee1d7a0886600 |
| context.md | 50 | 2468 | 63f5b98a9124bf0d105e8bb492ef752e5ef6d63aa61ad7518532bc8ede5dd9cc |
| decisions.diff | 43 | 3577 | b131fec6a3e98bb1c7a86a99e3946a4a5cae9b33f1b14a091d186d6cf2afee22 |
| product.diff | 213 | 11189 | 68387cc190bd9618e44b6bf2af1677dcb95654428140682f121ac9f6738a647c |
| steering.py | 186 | 7827 | c4dc05ac8209ef3549d9270e36f40faa19ef8bde97605f10f847b017e53d553a |
| chat_cmd.py | 68 | 3120 | 3b4a913172da9e6c52fc7269985a01cb7001d64ebe02b475f1499efcb69c63c4 |
| mutations.py | 85 | 2974 | 0ffccbb1d9f4666481ac692944d904a631a475f2ce557062653b07296b5a78e2 |
| test_steering.py | 133 | 5673 | f3f6c557fc0facee305ff5954021a966a452cfa870faa07b7152fb4f33751fcc |
| test_chat_cmd.py | 78 | 2995 | 287f1a5b296da240802192857ddb50da4a61ccba0b8660209c5d2ddebd3074e6 |

`plan.md` and `context.md` are REWRITES of `.agent/plan.md` and `.agent/context.md`.
`steering.py` is a NEW FILE at `packages/orchestration/steering.py`, `chat_cmd.py` a NEW FILE
at `apps/cli/commands/chat_cmd.py`, `test_steering.py` a NEW FILE at
`tests/orchestration/test_steering.py` and `test_chat_cmd.py` a NEW FILE at
`tests/cli/test_chat_cmd.py`, each copied whole. The `.diff` files go on with `git apply`; the
reviewer generated every one from a tree at `ef4cb503` and applied all of them, in the commit
order below, to a fresh worktree at `ef4cb503` with `git apply --check` then `git apply`, every
one at real exit code 0. `product.diff` edits `apps/cli/command_catalog.py`,
`apps/cli/commands/__init__.py`, `apps/cli/grouped.py`, `apps/ui/src/api/humanizeCatalog.ts`,
`docs/guides/exit-codes.md`, `packages/orchestration/event_names.py`,
`tests/cli/test_cli_ux.py`, `tests/cli/test_golden_path.py`,
`tests/orchestration/import_reachability_allowlist.txt` and `tests/test_command_catalog.py` —
the four test-side paths are the guards a new visible group, a new event name and a new module
force, so they land with the product. `mutations.py` is a TOOL for G5: it is run, never applied
to a tracked file.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C2, C3, C4, C5 and C6, in this order.

C1a — copy this block and the bookkeeping payloads
  `.agent/authored/f264-r1-block.md` := this block, and one
  `.agent/authored/f264-r1-<name>` for each of status.diff, rehead.diff, plan.md,
  context.md and decisions.diff, keeping each payload's own file name. All by
  `shutil.copyfile`.
  Subject: `F264 R1 C1a: copy round 1 block and bookkeeping payloads into .agent/authored/`
  Its insertions are this block's line count plus 201. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the product diff and the mutation tool
  `.agent/authored/f264-r1-<name>` for each of product.diff and mutations.py.
  Subject: `F264 R1 C1b: copy round 1 product diff and mutation tool into .agent/authored/`
  Expected insertions: 298.

C1c — copy the new product modules
  `.agent/authored/f264-r1-<name>` for each of steering.py and chat_cmd.py.
  Subject: `F264 R1 C1c: copy round 1 product modules into .agent/authored/`
  Expected insertions: 254.

C1d — copy the test payloads
  `.agent/authored/f264-r1-<name>` for each of test_steering.py and test_chat_cmd.py.
  Subject: `F264 R1 C1d: copy round 1 test payloads into .agent/authored/`
  Expected insertions: 211.

C2 — THE CLAIM, in this order:
   1. `git apply` rehead.diff  → `.agent/live_review.md`
   2. `git apply` status.diff  → `docs/roadmap/STATUS.md`
   3. rewrite `.agent/plan.md` := plan.md
   4. rewrite `.agent/context.md` := context.md
  Subject: `F264 R1 C2: claim F264 and re-head the live review record`
  Expected insertions by `git show --numstat`: 25 context.md, 26 live_review.md, 20 plan.md,
  1 STATUS.md.

C3 — THE DECISION
  `git apply` decisions.diff → `.agent/decisions.md`.
  Subject: `F264 R1 C3: record DECISION F264 D1, the steering record's shape and route`
  Expected insertions: 35.

C4 — THE PRODUCT: copy steering.py to `packages/orchestration/steering.py` and chat_cmd.py to
  `apps/cli/commands/chat_cmd.py`, then `git apply` product.diff, then `git add` all twelve
  paths — an untracked module fails `integrity check`'s `relevant_untracked`.
  Subject: `F264 R1 C4: accept, seal and certify a steering message, and add remedy chat`
  Expected insertions: 186 steering.py, 68 chat_cmd.py, 24 command_catalog.py,
  2 commands/__init__.py, 2 grouped.py, 1 humanizeCatalog.ts, 1 exit-codes.md,
  1 event_names.py, 5 test_cli_ux.py, 1 test_golden_path.py, 2 import_reachability_allowlist.txt,
  2 test_command_catalog.py.

C5 — THE TESTS: copy test_steering.py to `tests/orchestration/test_steering.py` and
  test_chat_cmd.py to `tests/cli/test_chat_cmd.py`, and `git add` both.
  Subject: `F264 R1 C5: test the steering record and remedy chat`
  Expected insertions: 133 test_steering.py, 78 test_chat_cmd.py.

C6 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F264 R1 C6: rewrite handoff for round 1`
  Then `git push -u origin feature/f264-steering-channel`. Do NOT create a pull request: the
  branch opens one at F264's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f264-r1-*` copies,
   `.agent/live_review.md`, `docs/roadmap/STATUS.md`, `.agent/plan.md`, `.agent/context.md`,
   `.agent/decisions.md`, `packages/orchestration/steering.py`,
   `apps/cli/commands/chat_cmd.py`, the ten paths product.diff edits (listed under PAYLOADS),
   `tests/orchestration/test_steering.py`, `tests/cli/test_chat_cmd.py` and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only ef4cb503 HEAD`
   after C6. Do NOT touch `.agent/prose_slips.md`, `.agent/candidates.md`,
   `.agent/operator_questions.md`, `README.md` or `docs/roadmap/features/T5_F264.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main` after the
   branch is cut, no branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees, their branches, the reviewer's worktrees
   `.remedy-wt/f264-r1-dry` and `.remedy-wt/f264-r1-sim`, and every existing stash alone. The
   worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last action, and
   `git worktree list` is reported afterwards (finding R-0940).
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run
   and F264's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C6 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f264-r1-*` copy byte for
 byte with its source (the block copy against `.remedy-wt/f264-r1-block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE BOOKKEEPING — the sha256 of each file below, read with `git show <commit>:<path>` at
 the commit named, equals the reviewer's reading, which its simulation printed from a tree it
 built by applying these payloads at `ef4cb503`:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/live_review.md | 309547 | b0b29bde1e5e4ce93b8a7cbf1031d900a1e00ea1cac25cdba388cfc6bb1aa8aa |
 | C2 | docs/roadmap/STATUS.md | 48679 | b078c6d9c695e6593c9d8d867776892788f6e9588e88f8b27ed5e86a13b28a48 |
 | C2 | .agent/plan.md | 1186 | 5f1928decf859545d33bc454751f62ad6da8c57ed44ba5950c6ee1d7a0886600 |
 | C2 | .agent/context.md | 2468 | 63f5b98a9124bf0d105e8bb492ef752e5ef6d63aa61ad7518532bc8ede5dd9cc |
 | C3 | .agent/decisions.md | 1939657 | 234f0931e7cca34f3ebfb3ca9c32102f7f33794a6d932f0abf926b678cef2ca4 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `ef4cb503` and at C2, with the set
 difference in both directions (the reviewer read 3 and 3 — R-0499, R-0950 and R-1008 — both
 differences empty); F264's STATUS line at C2 read back in full, which must read
 `- [~] F264 — Steering channel (remedy chat)`; and `git diff --name-only <C1d> <C2>` and
 `git diff --name-only <C2> <C3>`, which must name exactly the paths C2 and C3 list.

G3 THE PRODUCT — at C5, the sha256 of each file below, read with `git show <C5>:<path>`,
 equals the reviewer's simulated reading:
 | path | bytes | sha256 |
 |---|---|---|
 | packages/orchestration/steering.py | 7827 | c4dc05ac8209ef3549d9270e36f40faa19ef8bde97605f10f847b017e53d553a |
 | apps/cli/commands/chat_cmd.py | 3120 | 3b4a913172da9e6c52fc7269985a01cb7001d64ebe02b475f1499efcb69c63c4 |
 | apps/cli/command_catalog.py | 112930 | 77492d456d9816ca7bf8746891fb81cc28c327ba8d0d724c4109ac3184c75c4b |
 | apps/cli/commands/__init__.py | 2093 | 1c54e18b3e9aa23057708bbfd749aff265620a53012af77b3b37b2262094dc9e |
 | apps/cli/grouped.py | 28954 | 74e6aed43b0e7dc0911d60c3d78823c9b8652a22ebd1c4a58c42d261d7c96160 |
 | apps/ui/src/api/humanizeCatalog.ts | 6631 | dcc0b96f2aec2a7084e0cb13a2c616e0a4294fd6e860710ec9cbe4b3eaa97ac9 |
 | docs/guides/exit-codes.md | 3956 | 04ff98a8ae980de0984b2bfe49a207a53135d57bf19e934d4db728ed3dae3346 |
 | packages/orchestration/event_names.py | 8797 | 420438c805ec07ac9f10b89840474a1d75c79ebd5f5aedfdcf1964067380ef65 |
 | tests/cli/test_cli_ux.py | 39216 | e04df0f75a77220f5d9df18eb73e8855a0327fa7892ccd65dd14125a49bca171 |
 | tests/cli/test_golden_path.py | 34693 | 868f45dc33f9e9348d5a1b1702ca77e0dfbf80d2a98b48b9d81fc8d2f14642f2 |
 | tests/orchestration/import_reachability_allowlist.txt | 9991 | 2842cccfa3f82645302b14de8efc8dbf580c38521561471b5f4d379832be28da |
 | tests/test_command_catalog.py | 22937 | 144ea9cc6538ebfa73d2424484ec2f1cf616914c52d32adcdf9f3fbcbd279429 |
 | tests/orchestration/test_steering.py | 5673 | f3f6c557fc0facee305ff5954021a966a452cfa870faa07b7152fb4f33751fcc |
 | tests/cli/test_chat_cmd.py | 2995 | 287f1a5b296da240802192857ddb50da4a61ccba0b8660209c5d2ddebd3074e6 |
 Also `git diff --name-only <C3> <C4>` and `<C4> <C5>`, which must name exactly the paths C4
 and C5 list.

G4 THE TESTS — in the primary checkout at C5, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_steering.py tests/cli/test_chat_cmd.py tests/cli/test_cli_ux.py tests/test_command_catalog.py tests/cli/test_exit_codes.py tests/cli/test_advertised_commands.py tests/orchestration/test_event_names.py tests/ui_contracts/test_humanize_catalog.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/docs/ tests/orchestration/test_roadmap_index.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path, serially, inside its sim
 worktree carrying C2 to C5 and read `1051 passed, 2 skipped` at real exit code 0, and the
 golden path alone there at `42 passed`; the primary checkout carries the UI toolchain a
 worktree lacks, so a skip may pass there. Report what you read. Then `python3 -m ruff check
 packages/orchestration/steering.py apps/cli/commands/chat_cmd.py apps/cli/commands/__init__.py
 apps/cli/command_catalog.py apps/cli/grouped.py packages/orchestration/event_names.py
 tests/orchestration/test_steering.py tests/cli/test_chat_cmd.py tests/cli/test_cli_ux.py
 tests/cli/test_golden_path.py tests/test_command_catalog.py`, real exit code 0, and
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0 (the reviewer read `handlers=149` in its sim tree).

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f264-r1-mut <C5>`, then
 `python3 -B .remedy-wt/f264-r1-payloads/mutations.py .remedy-wt/f264-r1-mut` and report its
 whole output. The script asserts each FROM occurs exactly once, applies it, runs
 `tests/orchestration/test_steering.py` and `tests/cli/test_chat_cmd.py` under `python3 -B`,
 restores the bytes, and runs an unmutated control first and last. The reviewer read, over the
 same script against its own tree carrying C2 to C5:
 control_before `28 passed` at exit 0;
 m1 (an ended job accepts a message) 4 failed at exit 1;
 m2 (a taken record id is overwritten) 2 failed at exit 1;
 m3 (the record seal never checked) 1 failed at exit 1;
 m4 (records listed by file name, not number) 1 failed at exit 1;
 m5 (the length limit off by one) 1 failed at exit 1;
 m6 (the run-log event carries no seal) 1 failed at exit 1;
 m7 (a record's file name never checked against its id) 1 failed at exit 1;
 m8 (the CLI records the wrong channel) 1 failed at exit 1;
 m9 (the bare `remedy chat <job_id> ...` form not routed to `send`) 4 failed at exit 1;
 control_after `28 passed` at exit 0; every `restored byte-identical` line True.
 Then `git worktree remove --force .remedy-wt/f264-r1-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C6: `git status --porcelain`, which must be empty;
 `git log --oneline -n 10`, which must show C6, C5, C4, C3, C2, C1d, C1c, C1b, C1a and
 `ef4cb503` in that order; `git worktree list`, which must show the primary checkout, the
 `.remedy-wt/job-*` worktrees and the reviewer's two that constraint 6 names, and nothing
 else; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be
 EMPTY. These readings go in your reply, since C6 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F264, round 1, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 1, then T001's second half — `chat.send` exposed on F009's write channel as the
cockpit's route. State the open-findings count, 3, and the operator-questions count, 0.

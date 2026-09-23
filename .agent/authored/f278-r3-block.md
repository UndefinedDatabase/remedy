STEP F278 R3 — BOOK ROUND 2, MIGRATE THE BOOLEAN HELPERS

GOAL
Book round 2's PASS and DECISION F278 D2, then migrate T002's boolean helpers onto
`durable_write` — `real_test_execution._atomic_write`, `self_dogfood_execution._atomic_write`
and `token_economy._atomic_write` — one module per commit, each DELETED in the commit that
moves its callers, each removing its entry from the guard's `STILL_TO_MIGRATE` set, and each
adding a test class to its module's own test file.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

WHAT CHANGES FOR A CALLER, per DECISION F278 D2 in this round's `decisions.md` payload.
Each deleted helper swallowed every `OSError` and returned False. `save_attempt` and
`save_token_budget_profile` return that boolean and keep it. `create_snapshot_proof` (two
sites) and `_store_request` ignored it, so a failed write returned an artifact whose record
was never on disk; they now let the error propagate. Every site writes the same bytes as
before. The two modules that chmodded the parent to 0o700 now create it with
`mkdir(mode=0o700, ...)`. `import os` goes from `self_dogfood_execution.py` and
`token_economy.py`, where nothing else uses it.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f278-r3-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f278-r3-scratch/`   The reviewer's scripts; do not edit or delete them. Put
      your own logs under `.remedy-wt/f278-r3-worker/`. All are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, `cd <dir> && git ...`, and multi-operation
one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe pytest.
Use `git -C <path>` rather than `cd`. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`).

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f278-durable-writes-loud-failures`, and `git log --oneline -1` must read
   `b449d7b2`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f278-r3-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f278-r3-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| decisions.md | 32 | 2269 | 512871fca8a7b016973a32ed8d3fe01f99e817cc3564a635505ffddd66c7eb31 |
| ledger.md | 2 | 3018 | d1d0c98b55187eed0874269f8df91474128b6314cd19712514637434e0cb64f5 |
| plan.md | 31 | 1234 | 31cab2fd08429194bd8a035b0cce9e8a56121adeb857e7e76cffcca92992d816 |
| revert_probes.py | 47 | 1897 | 3d2c990aba71a72ffdb1865d3228f37d25db219b7658026ac4b95ad3581d726a |
| rte.diff | 114 | 5450 | 61f19b21cd9d51b2bb62ea31fc856aea076d53e44455d16eb7f007e20b7f7346 |
| sd.diff | 121 | 5042 | 3310d8622d2b8fd7791ede331e1a4efe93a143e7ae0eaf4b988d295d2fdb56ec |
| te.diff | 112 | 4846 | 910c943cf0d1f33b5a20060d11460c8b7e83afa23596f20271622c2d131f81e0 |

`ledger.md` and `decisions.md` are APPENDS by byte concatenation, each beginning with the
single newline that separates records. `plan.md` is a REWRITE of `.agent/plan.md`. The
`.diff` payloads go on with `git apply`, in the order C3, C4, C5, because each removes one
line of the guard file and the next one's context assumes the one before it; the reviewer
generated each from the tree it applies to. `revert_probes.py` is a TOOL for G5: it is run,
never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C2, C3, C4, C5 and C6, in this order.

C1a — copy this block and the bookkeeping payloads
  `.agent/authored/f278-r3-block.md` := this block, and one `.agent/authored/f278-r3-<name>`
  for each of decisions.md, ledger.md and plan.md, keeping each payload's own file name.
  All by `shutil.copyfile`.
  Subject: `F278 R3 C1a: copy round 3 block and bookkeeping payloads into .agent/authored/`
  Its insertions are this block's line count plus 65. STOP rather than commit at 500 or more.

C1b — copy the product payloads
  One `.agent/authored/f278-r3-<name>` for each of rte.diff, sd.diff, te.diff and
  revert_probes.py, by `shutil.copyfile`.
  Subject: `F278 R3 C1b: copy round 3 product payloads into .agent/authored/`
  Expected insertions: 394.

C2 — THE BOOKING, one commit: append ledger.md to `.agent/live_review.md`, append
  decisions.md to `.agent/decisions.md`, and rewrite `.agent/plan.md` := plan.md.
  Subject: `F278 R3 C2: book round 2's PASS and DECISION F278 D2`
  Expected insertions: 45 (32 decisions, 2 live review, 11 plan).

C3 — REAL TEST EXECUTION: `git apply --check` then `git apply` rte.diff.
  Subject: `F278 R3 C3: move the snapshot proof record onto durable_write`
  Expected insertions: 35.

C4 — SELF-USE EXECUTION: `git apply --check` then `git apply` sd.diff.
  Subject: `F278 R3 C4: move the self-use attempt and request records onto durable_write`
  Expected insertions: 44.

C5 — TOKEN ECONOMY: `git apply --check` then `git apply` te.diff.
  Subject: `F278 R3 C5: move the token budget profile onto durable_write`
  Expected insertions: 34.

C6 — THE HANDBACK: `.agent/handoff.md`, rewritten, its own commit, per
  `docs/agents/handback_template.md`, WITH the item-status table AGENTS.md requires — one
  row per commit and per gate. Subject: `F278 R3 C6: rewrite handoff for round 3`
  Then `git push origin feature/f278-durable-writes-loud-failures` and report its outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Report every `git apply --check` exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading.
3. The round's whole tracked path set is: the `.agent/authored/f278-r3-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `packages/orchestration/real_test_execution.py`,
   `packages/orchestration/self_dogfood_execution.py`,
   `packages/orchestration/token_economy.py`,
   `tests/orchestration/test_durable_write_guard.py`,
   `tests/orchestration/test_real_test_execution.py`,
   `tests/orchestration/test_self_dogfood_execution.py`,
   `tests/orchestration/test_token_economy.py` and `.agent/handoff.md`. Report the list
   `git diff --name-only b449d7b2 <C6>` gives. Nothing under `docs/`, no other module.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no branch deletion, no
   force-push, no `git stash`, no checkout of another branch.
6. Leave `.remedy-wt/job-129b3ad7206d4f8d`, its branch and every existing stash alone. The
   worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last action, and
   `git worktree list` is reported afterwards (finding R-0940).
7. DO NOT run the full suite (amend0917 rule 1); F278's one run belongs to its closure.
8. Report each commit's insertion count in your handback's `## Commits` table as
   `git show --numstat` gives it, and the handback commit's own count in your reply.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C6 is written.

G1 TRANSPORT — each payload's line count, byte count and sha256 against the PAYLOADS table;
 then each `.agent/authored/f278-r3-*` copy, read with `git show <commit>:<path>` from the
 commit that added it, compared byte for byte with its source (the block copy against
 `.remedy-wt/f278-r3-block.md`). One reading per copy.

G2 THE BOOKING — at C2: each appended file equals its `b449d7b2` bytes plus its payload's
 bytes, by strict concatenation, and `.agent/plan.md` equals plan.md; then the sha256 read
 with `git show <C2>:<path>` equals the reviewer's dry-run reading:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 430456 | 9e5fd03a7c7e3ec308268fc3ca25276f8ee30156585c661efb5ae0f7a34bfbee |
 | .agent/decisions.md | 1844455 | 228754110918a12a5e4add02145e566a92dbe7dcfef74e10ec75a90e5345d853 |
 | .agent/plan.md | 1234 | 31cab2fd08429194bd8a035b0cce9e8a56121adeb857e7e76cffcca92992d816 |
 And the open set by distinct id with `open_finding_ids` from `scripts/rotate_live_review.py`
 at `b449d7b2` and at C2, with both set differences (the reviewer read 26, 26, both empty).

G3 THE PRODUCT BYTES — at C5, the sha256 of each file read with `git show <C5>:<path>`:
 | path | bytes | sha256 |
 |---|---|---|
 | packages/orchestration/real_test_execution.py | 20693 | 71e2937dce02ff262b72987f5959817887ea3649c98af25d26feedb78c4e69a1 |
 | packages/orchestration/self_dogfood_execution.py | 32243 | 26bcba0716070a7d788586c860a1772cceacabcfe218782041aebe6b85ebf22f |
 | packages/orchestration/token_economy.py | 36221 | 42bc47d864411c12a3f3e7c57ff312b44656850f9d49e25d1688825ebe75bcaa |
 | tests/orchestration/test_durable_write_guard.py | 3214 | a7324ec24a9ab0376f4abc3c9f8d6952ae9744ff9b8e02c3b43ab74d5fa9cb8b |
 | tests/orchestration/test_real_test_execution.py | 11575 | c6515d5de9e4d6c0c249e0db6b37c9999c3f1df2280ddb08086dbf1cc8bf8b18 |
 | tests/orchestration/test_self_dogfood_execution.py | 12989 | 2802c9cced19f7bc0c59dcd2ff6a54f17975908ee2a90c628d1a93ca40ea6975 |
 | tests/orchestration/test_token_economy.py | 18052 | fafcc0b7161737b906fd0ab55b0c2130c0f26db919425750491a739344dc5bb8 |

G4 THE TESTS — in the primary checkout at C5, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_durable_write_guard.py tests/orchestration/test_real_test_execution.py tests/orchestration/test_self_dogfood_execution.py tests/orchestration/test_token_economy.py tests/cli/test_real_test_execution_cli.py tests/cli/test_self_dogfood_execution_cli.py tests/cli/test_self_dogfood_cli.py tests/orchestration/test_self_dogfood.py tests/test_token_policy.py tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection WITHOUT the golden path in a disposable worktree carrying
 C2 to C5 and read `265 passed, 1 skipped` at real exit code 0; report what you read. Then
 `python3 -m ruff check` over every Python path of the G3 table, real exit code 0, and
 `python3 -m apps.cli.main integrity check --json`, all five checks `pass` at `fail_count` 0.

G5 THE REVERT PROBES — `git worktree add --detach .remedy-wt/f278-r3-probe <C5>`, then
 `python3 .remedy-wt/f278-r3-payloads/revert_probes.py .remedy-wt/f278-r3-probe b449d7b2`
 and report its whole output. Each probe restores one production file from `b449d7b2` while
 the tests stay at C5. The reviewer read, over the same script against its own tree:
 control_before `92 passed` at exit 0;
 p1 (`real_test_execution.py`) `5 failed, 87 passed` at exit 1 — the guard's
   `test_no_private_atomic_write_helper_outside_packages_common` and the four cases of
   `TestSnapshotRecordIsDurableAndLoud`;
 p2 (`self_dogfood_execution.py`) `4 failed, 88 passed` at exit 1 — that guard test and the
   three tests of `TestAttemptRecordsAreDurable`;
 p3 (`token_economy.py`) `3 failed, 89 passed` at exit 1 — that guard test and the two
   tests of `TestProfileWriteIsDurable`;
 control_after `92 passed` at exit 0, with every `restored clean` line `True`.
 Then `git worktree remove --force .remedy-wt/f278-r3-probe`, `git worktree prune`, and
 report `git worktree list`.

G6 TREE AND PUSH — after C6, in your reply: `git status --porcelain`, empty;
 `git log --oneline -n 8`, showing C6 back to C1a and then `b449d7b2`; `git worktree list`,
 the primary checkout and `.remedy-wt/job-129b3ad7206d4f8d` only; the push's real outcome;
 and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: the state block, the per-commit
changed-files table with the insertion count you MEASURED beside the one this block
expected, every gate's real output and exit code, the ITEM-STATUS TABLE, the deviations,
and the next expected action. Your Session section reads SESSION 1 of feature F278,
round 3, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 3, then T002's last group — `dev_server`'s helpers with `runtime_supervisor` and
`runtime_cmd`, and the inline writers in `repository_snapshot` and `project_registry`.
State the open-findings count, 26, and the operator-questions count, 0.

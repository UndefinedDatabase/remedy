STEP F279 R7 — T004, THE ORDER HALF: the toolchain refresh order and the fourteen-day tier

GOAL
Book round 6's PASS, record DECISION F279 D7, and land T004's order half:
`docs/orders/toolchain-refresh.md`, written as a job file of five tasks, indexed in
`docs/README.md` and pinned by a docs test; and the self-use generator's order tier, which
queues that file verbatim, before the ledger tier, at most once every fourteen days. With this
round every slice of F279 is built. Each new behaviour carries a red proof.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

WHAT THE REVIEWER FOUND WHILE AUTHORING (DECISION F279 D7, the decisions.diff payload)
A self-use item is a job file, so the order is written as one and queued byte for byte. A queue
entry carries no date, so the day an order item was queued is stamped into its `provenance`.
The ledger tier always has a finding to offer, so the order tier comes first. The tier reads the
repository's own order file by default, so the tests of the other tiers point that default at a
missing file (the test_self_use_generator.diff payload adds an autouse fixture), and the one
end-to-end runner test names a missing order file (the test_self_use_runner.diff payload).

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f279-r7-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f279-r7-scratch/`   YOURS for logs and scripts. Each is gitignored; create
      the scratch directory if it is absent.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, `cd <dir> && git ...`, and multi-operation
one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe pytest.
Use `git -C <path>` rather than `cd`. An inline heredoc with braces or a dollar sign is often
refused too: write any helper script to a file under your scratch directory and run the file.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f279-configuration-toolchain-truth`, and `git log --oneline -1` must read
   `564b54e3`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f279-r7-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git stash list | head -1` as found.

PAYLOADS — under `.remedy-wt/f279-r7-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| decisions.diff | 42 | 3122 | 941b08c5eb22441ab526f4ee6ee2f9006dd4c67d0b5732805754c04dd24acd3c |
| docs_index.diff | 28 | 1549 | 08a9658fd4351525e559c361ab7b0f562b537cfbb3d5bcd42024c549a0d8251c |
| ledger.diff | 10 | 6198 | 85cc5f5f6523d7a14d35fac650a0a17faa6043f38ff31847fbf8218e7213cf2e |
| mutations.py | 60 | 2384 | 60869cbcb9e20bcd9bc48c5bbabef36d8ae0fe9697f5a2c5fad3fdeac9ee21c8 |
| plan.md | 32 | 1381 | dda84bb0a8c205056b8be083a7eeb92f71d74e5ff3938686e3fc481a329121de |
| self_use_generator.diff | 147 | 6618 | 3ae43fb10d7ce2f8968283af195594ddf3d72a8c4dbbdebef1d1ea4eaedb55ab |
| test_self_use_generator.diff | 96 | 5312 | efb8b13c7d59e6e9655979e49f926546181604f1876adaf20d7b1720522ee42a |
| test_self_use_runner.diff | 16 | 961 | 88222882ec9b6caa962d355bf2203317c6576d55df5cffd50c09960b7699d20a |
| test_toolchain_refresh_order.py | 51 | 2143 | 366ddef540fe8430a15b542cfd29b70338c3b5348d7e19cc32d0c016f6012ece |
| toolchain-refresh.md | 66 | 3444 | d95d0772bc9afb7d6ac46514fb7caefbf8120171cbfa97037144c1e93e8cded8 |

`plan.md` is a REWRITE of `.agent/plan.md`. `toolchain-refresh.md` is a NEW FILE at
`docs/orders/toolchain-refresh.md` (a new directory) and `test_toolchain_refresh_order.py` a
NEW FILE at `tests/docs/test_toolchain_refresh_order.py`, each copied whole. Every `.diff` goes
on with `git apply`; the reviewer generated each from a tree at `564b54e3` and applied all of
them, in the commit order below, to a fresh worktree at `564b54e3` with `git apply --check`
then `git apply`, every one at real exit code 0. `ledger.diff` appends round 6's `Gate:` entry
and `decisions.diff` appends DECISION F279 D7. `mutations.py` is a TOOL for G5, never applied.

BUNDLE — the commits are C1a, C1b, C2, C3 and C4, in this order. The copies are two commits
because together with this block they exceed the 500-line cap.

C1a — copy this block and the bookkeeping payloads
  `.agent/authored/f279-r7-block.md` := this block, and one `.agent/authored/f279-r7-<name>`
  for each of ledger.diff, plan.md and decisions.diff, keeping each payload's own file name.
  All by `shutil.copyfile`.
  Subject: `F279 R7 C1a: copy round 7 block and bookkeeping payloads into .agent/authored/`
  Its insertions are this block's line count plus 84. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the product payloads
  `.agent/authored/f279-r7-<name>` for each of toolchain-refresh.md,
  test_toolchain_refresh_order.py, self_use_generator.diff, test_self_use_generator.diff,
  test_self_use_runner.diff, docs_index.diff and mutations.py, by `shutil.copyfile`.
  Subject: `F279 R7 C1b: copy round 7 product payloads into .agent/authored/`
  Expected insertions: 464.

C2 — THE BOOKKEEPING, one commit (amend0917-throughput rule 4), in this order:
   1. `git apply` ledger.diff     → `.agent/live_review.md`
   2. rewrite `.agent/plan.md` := plan.md
   3. `git apply` decisions.diff  → `.agent/decisions.md`
  Subject: `F279 R7 C2: book round 6's PASS and record DECISION F279 D7`
  Expected insertions by `git show --numstat`: 34 decisions.md, 2 live_review.md, 11 plan.md.

C3 — THE ORDER, ITS TIER AND THEIR TESTS in one commit, because the tests verify them
  Copy toolchain-refresh.md and test_toolchain_refresh_order.py to their paths, creating
  `docs/orders/`, and `git add` both — an untracked file fails `integrity check`'s
  `relevant_untracked` — then `git apply` self_use_generator.diff,
  test_self_use_generator.diff, test_self_use_runner.diff and docs_index.diff.
  Subject: `F279 R7 C3: add the toolchain refresh order and queue it every fourteen days`
  Expected insertions: 10 docs/README.md, 66 toolchain-refresh.md, 79 self_use_generator.py,
  51 test_toolchain_refresh_order.py, 81 test_self_use_generator.py, 4 test_self_use_runner.py.

C4 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F279 R7 C4: rewrite handoff for round 7`
  Then `git push origin feature/f279-configuration-toolchain-truth`. Do NOT create a pull
  request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading. F279's one
   declared oversize commit was round 1's C5; there is no second.
3. The round's whole tracked path set is: the `.agent/authored/f279-r7-*` copies,
   `.agent/live_review.md`, `.agent/plan.md`, `.agent/decisions.md`,
   `docs/orders/toolchain-refresh.md`, `tests/docs/test_toolchain_refresh_order.py`,
   `packages/orchestration/self_use_generator.py`,
   `tests/orchestration/test_self_use_generator.py`,
   `tests/orchestration/test_self_use_runner.py`, `docs/README.md` and `.agent/handoff.md`.
   Report the list you measure with `git diff --name-only 564b54e3 HEAD` after C4. Do NOT
   touch `scripts/self_use_queue.json`, `.agent/prose_slips.md`, `.agent/candidates.md`,
   `.agent/operator_questions.md`, `.agent/context.md`, `docs/roadmap/**`, or any module not
   in that list. Do NOT run the generator against the real queue: the closure does that.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash` — the stash list is shared by every
   worktree of this repository.
6. Leave `.remedy-wt/job-129b3ad7206d4f8d`, `.remedy-wt/job-e7268925db3a4831`, their branches
   and every existing stash alone. The worktree G5 adds goes under `.remedy-wt/`, is removed
   as that step's last action, and `git worktree list` is reported afterwards (R-0940).
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run
   and F279's belongs to its closure. Run G4 serially, never with `-n`.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C4 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f279-r7-*` copy byte for
 byte with its source (the block copy against `.remedy-wt/f279-r7-block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE BOOKKEEPING — at C2, the sha256 of each file below, read with `git show <C2>:<path>`,
 equals the reviewer's simulated reading:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 386693 | b51cd4adc45da4c870374491cb3f25ab7741f5104a9c331b6abe79b20fc50413 |
 | .agent/plan.md | 1381 | dda84bb0a8c205056b8be083a7eeb92f71d74e5ff3938686e3fc481a329121de |
 | .agent/decisions.md | 1874787 | 40244b32dfb24e09d635af015a8a696c35aceca78f9f47995d11779824e82b93 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `564b54e3` and at C2, with the set
 difference in both directions (the reviewer read 26 and 26, both differences empty); the
 count of lines beginning `Gate: F279 R6 — ` at `564b54e3` and at C2 (the reviewer read 0 and
 1); and `git diff --name-only <C1b> <C2>`, which must name exactly the paths C2 lists.

G3 THE ORDER — at C3, `git diff --name-only <C2> <C3>` names exactly the paths C3 lists, and
 the sha256 of each, read with `git show <C3>:<path>`, equals the reviewer's simulated reading:
 | path | bytes | sha256 |
 |---|---|---|
 | docs/orders/toolchain-refresh.md | 3444 | d95d0772bc9afb7d6ac46514fb7caefbf8120171cbfa97037144c1e93e8cded8 |
 | tests/docs/test_toolchain_refresh_order.py | 2143 | 366ddef540fe8430a15b542cfd29b70338c3b5348d7e19cc32d0c016f6012ece |
 | packages/orchestration/self_use_generator.py | 19096 | a10fbf7e4f012a4e578c57e1bda14fc0d57f7a51632e2d8e82c14544b4537f24 |
 | tests/orchestration/test_self_use_generator.py | 25328 | d1fe7505d28a1a7c6a7887801e581abe5864d32cc897a03015634142b5965048 |
 | tests/orchestration/test_self_use_runner.py | 18703 | 0ab919d4298d65bdf0b3603d0b358b5b778b0f60212677b5f81596d3cd203491 |
 | docs/README.md | 18552 | c828e72ee745d6abadfc32b3f9365c79f56aeda9c5c7dbae5b37e98f5c071b67 |

G4 THE TESTS — in the primary checkout at C3, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_runner.py tests/orchestration/test_self_use_queue.py tests/orchestration/test_self_use_job.py tests/orchestration/test_self_use_findings.py tests/docs/ tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py tests/orchestration/test_integrity_gate.py tests/test_ble001_ratchet.py tests/orchestration/test_live_review_rotation.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path inside a disposable worktree
 carrying C2 and C3 and read `605 passed, 2 skipped` at real exit code 0; the primary
 checkout carries the UI toolchain a worktree lacks, so a skip may pass there. Report what
 you read. Then `python3 -m ruff check` over the Python paths C3 lists, real exit code 0;
 `python3 -m apps.cli.main integrity check --json`, which must read every check `pass` at
 `fail_count` 0; and `python3 -m apps.cli.main integrity block .remedy-wt/f279-r7-block.md`,
 which the reviewer ran on this block before emitting it and read every item OK at exit 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f279-r7-mut <C3>`, then
 `python3 -B .remedy-wt/f279-r7-payloads/mutations.py .remedy-wt/f279-r7-mut` and report its
 whole output. The script asserts each FROM occurs exactly once, applies it, runs the affected
 test files under `python3 -B`, restores the bytes, and runs an unmutated control first and
 last. The reviewer read, over the same script against its own tree carrying C2 and C3:
 control_before `42 passed` at exit 0;
 m1 (no cadence) 1 failed at exit 1, at
   `TestOrderTier::test_within_fourteen_days_the_ledger_tier_answers_instead`;
 m2 (the order tier never answers) 3 failed at exit 1, at
   `TestOrderTier::test_the_real_order_file_is_a_job_the_tier_accepts`,
   `TestOrderTier::test_an_order_never_queued_comes_before_the_ledger` and
   `TestOrderTier::test_after_fourteen_days_the_order_is_due_again`;
 m3 (any file taken as a job) 1 failed at exit 1, at
   `TestOrderTier::test_an_order_file_that_is_not_a_job_is_refused`;
 m4 (an order heading reworded) 1 failed at exit 1, at
   `test_the_order_carries_exactly_the_pinned_headings_in_order`;
 control_after `42 passed` at exit 0.
 Then `git worktree remove --force .remedy-wt/f279-r7-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C4: `git status --porcelain`, which must be empty;
 `git log --oneline -n 6`, which must show C4, C3, C2, C1b, C1a and `564b54e3` in that order;
 `git worktree list`, which must show the primary checkout and the `.remedy-wt/job-*`
 worktrees constraint 6 names, and nothing else; `git stash list | head -1`, unchanged from
 the reading item 4 took; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be
 EMPTY. These readings go in your reply, since C4 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F279, round 7, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 7, then F279's closure sequence per `docs/roadmap/STATUS_closure_protocol.md`. State
the open-findings count, 26, and the operator-questions count, 0.

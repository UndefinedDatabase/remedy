STEP F015 R6 — THE CLOSURE'S FIRST REPAIR ROUND: BOOK ROUND 5, REPAIR THE SUITE'S TWO BAD NODES, RUN THE SUITE AGAIN

GOAL
Book round 5's PASS and record DECISION F015 D5; repair the two bad nodes of round 5's full suite —
`runtime stop` waits out a supervisor that has already recorded its application's exit, and the
CLI subprocess hang guard of `tests/cli/runtime_helpers.py` becomes 30 seconds — with a regression
test and red proofs; then run the full suite again, whose transcript replaces
`.agent/authored/f015-closure-suite.txt` at the same path (operator amendment amend0917-throughput
rule 2, first repair round).

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. This round closes nothing.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f015-r6-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f015-r6-scratch/`   The reviewer's scripts; do not edit or delete them.
  `.remedy-wt/f015-r6-worker/`    YOURS for logs and scripts; create it if absent. All three are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, `ln`, `npm ci`, `npm install`, process substitution,
`cd <dir> && git ...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`.
Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when
you pipe. Use `git -C <path>` rather than `cd`. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`). A heredoc containing a dollar-brace is refused: write such a script to a
file under your own directory and run the file. Never use `git stash` in any form.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f015-interactive-plan-editing`, and `git log --oneline -1` must read `11eb90c9`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f015-r6-block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f015-r6-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every reading.
Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 57 | 10467 | deecf7ac1ad444954edf6828e9b68c8fe3ac58303f8e15c07479b1ba73d44735 |
| product.diff | 67 | 3555 | a3867f6bba9603c4b64d7edd0b8289c9be22d9d042b0babffcc73e1645c42f50 |
| tests.diff | 74 | 3410 | 5d5cabde9c47c2ba0cda1ed512fa14310d2dd9fb9d95c4641a70ef1d3944649a |
| plan.md | 32 | 1293 | 13537bb4fbc9a488fc571d6731e46147dc03d8079fe466c39c21d4d8f6cdb249 |
| mutations.py | 52 | 2176 | 5dc39d451a93af0bee53c21b67c66c9f557eaa8513f1dc139e3906994b9a8c98 |

`plan.md` is a REWRITE of `.agent/plan.md`. The `.diff` files go on with `git apply`; the reviewer
generated all three from a tree at `11eb90c9` and applied them, in the commit order below, to a
fresh detached worktree at `11eb90c9` with `git apply --check` then `git apply`, each at real exit
code 0. `records.diff` appends the `Gate: F015 R5 —` entry to `.agent/live_review.md` and DECISION
F015 D5 to `.agent/decisions.md`. `product.diff` edits `packages/runtimes/dev_server.py` and
`tests/cli/runtime_helpers.py`. `tests.diff` edits `tests/runtimes/test_supervisor_portability.py`.
`mutations.py` is a TOOL for G4: it is run, never applied to a tracked file.

BUNDLE — the commits are C1, C2, C3, C4 and C5, in this order.

C1 — copy this block and every payload: `.agent/authored/f015-r6-block.md` := this block, and one
  `.agent/authored/f015-r6-<name>` for each payload, keeping its own file name, by
  `shutil.copyfile`.
  Subject: `F015 R6 C1: copy round 6 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 282. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F015 R6 C2: book round 5's PASS and record D5`
  Expected insertions by `git show --numstat`: 39 decisions.md, 2 live_review.md, 6 plan.md.

C3 — THE REPAIRS: `git apply` product.diff and `git add` its two paths.
  Subject: `F015 R6 C3: wait out an exiting supervisor at stop; a 30-second CLI hang guard`
  Expected insertions: 15 dev_server.py, 17 runtime_helpers.py.

C4 — THE REGRESSION TEST: `git apply` tests.diff and `git add` its path.
  Subject: `F015 R6 C4: test a stop that lands while the supervisor is still exiting`
  Expected insertions: 56.

C5 — THE SUITE AGAIN AND THE HANDBACK, in the PRIMARY checkout, after G1 to G4:
  (a) `bash -c 'npm --prefix apps/ui run build 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'`;
      a refused or failing build is a STOP under constraint 4. Then `git status --porcelain`,
      which must still be empty.
  (b) `python3 -m pytest -n auto -q`, its log written to `.remedy-wt/f015-r6-worker/full-suite.log`.
      REWRITE `.agent/authored/f015-closure-suite.txt` with the command, the real exit code, the
      summary line, the FULL list of bad node ids (failed plus errors) or the literal `NONE`, and a
      shrinking comparison against round 5's bad set — the two node ids DECISION F015 D5 names —
      stating which of them are gone and whether any node is newly bad.
  (c) Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`, and commit it TOGETHER
      with the transcript.
  Subject: `F015 R6 C5: record the repaired closure suite and rewrite handoff for round 6`
  Then `git push origin feature/f015-interactive-plan-editing` and report its real outcome. Do NOT
  create a pull request.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1.
3. The round's whole tracked path set is: the `.agent/authored/f015-r6-*` copies, the paths C2, C3
   and C4 name, `.agent/authored/f015-closure-suite.txt` and `.agent/handoff.md`. Report the list
   you measure with `git diff --name-only 11eb90c9 HEAD` after C5.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. THE ONE
   EXCEPTION is the full suite in C5: a red suite is committed exactly as measured with every bad
   node id and handed back. Never weaken an assertion, delete a test or mark anything xfail.
5. NOTHING IS MERGED, NOTHING IS CLOSED. No `gh pr merge`, no `gh pr create`, no checkout of another
   branch, no branch deletion, no force-push, no STATUS edit, no evidence job, no review package.
6. Leave the `.remedy-wt/job-*` worktrees, their branches, the reviewer's worktrees whose names
   begin `.remedy-wt/f015-`, the worktrees under `.claude/worktrees/`, the local branch
   `sim/f267-r1`, and every existing stash alone. The worktree G4 adds goes under `.remedy-wt/`,
   is removed as that step's last action, and `git worktree list` is reported afterwards.
7. The full suite runs ONCE, in C5, and nowhere else this round.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G4 run before C5, and G5 is C5's suite.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured against
 the PAYLOADS table. Then compare each `.agent/authored/f015-r6-*` copy byte for byte with its
 source (the block copy against `.remedy-wt/f015-r6-block.md`), read back with
 `git show <C1>:<path>`. Report one reading per copy.

G2 THE RECORDS AND THE REPAIRS — the sha256 of each file below, read with `git show <commit>:<path>`
 at the commit named, equals the reviewer's reading, which its simulation printed from a tree it
 built by applying these payloads at `11eb90c9`:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/live_review.md | 302633 | 2ea716f15a2640e2de4ab6ffd306875bb2265b10e38349042fdbd30ac1128207 |
 | C2 | .agent/decisions.md | 1991385 | 89eb0fbb593f3c43a4f955da4dcc781a57686b79abfea0e0a81fd0fc843ac3b5 |
 | C2 | .agent/plan.md | 1293 | 13537bb4fbc9a488fc571d6731e46147dc03d8079fe466c39c21d4d8f6cdb249 |
 | C4 | packages/runtimes/dev_server.py | 89203 | dba88dd52e163cf3a9b3c80f097b697f036f8ecbf0ad25a52ad2209251b29764 |
 | C4 | tests/cli/runtime_helpers.py | 10704 | e3f5ac6c4793e6267f3e80a84dbe23451c550f76311db00a98cc49287f9491c5 |
 | C4 | tests/runtimes/test_supervisor_portability.py | 108760 | 5b1e749c2da11a69876dfb8652d362a3fb418f47ea2a1a8ba28793494abb544c |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT, at `11eb90c9` and at C2 (the reviewer read
 4 at both — R-0499, R-0950, R-1008 and R-1046 — both differences empty); the count of lines C2's
 diff adds to `.agent/live_review.md` that begin `Gate: F015 R5 — `, which must be 1; and
 `git diff --name-only` between consecutive commits from C1 to C4, which must name exactly the
 paths each commit lists.

G3 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash .remedy-wt/f015-r6-scratch/g4.sh /home/decodeux/Repos/remedy
```
 The reviewer ran the same script inside its sim worktree carrying C1 (without the block copy) to C4
 and read `833 passed, 3 skipped` at pytest exit 0, ruff at exit 0, and all six integrity checks `pass` at
 `fail_count` 0. The primary checkout carries the UI toolchain a worktree lacks, so a skip may
 pass there. Report the pytest summary line and exit code, ruff's exit code, and whether all six
 integrity checks read `pass` at `fail_count` 0.

G4 THE RED PROOFS — `git worktree add --detach .remedy-wt/f015-r6-mut <C4>`, then
 `python3 -B .remedy-wt/f015-r6-payloads/mutations.py .remedy-wt/f015-r6-mut` and report its whole
 output. The reviewer read, over the same script against its sim tree carrying C1 to C4:
 control_before: `4 passed` at exit 0;
 m1_stop_never_waits_for_the_exiting_supervisor: `1 failed, 3 passed` at exit 1;
 m2_a_zero_hang_guard_reproduces_the_suite_failure: `1 failed, 3 passed` at exit 1;
 control_after: `4 passed` at exit 0; every `restored byte-identical` line True.
 Then `git worktree remove --force .remedy-wt/f015-r6-mut`, `git worktree prune`, report
 `git worktree list`, and report `ps aux | grep -c "[r]untime_supervisor"`, which must read 0.

G5 THE SUITE AGAIN — the UI build's last line and real exit code, `git status --porcelain` after it,
 then the full suite's real exit code, summary line, every bad node id and the shrinking comparison,
 all of it in `.agent/authored/f015-closure-suite.txt`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 6`, which must show C5, C4, C3, C2, C1 and `11eb90c9` in that order;
 `git worktree list`; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the insertion count you MEASURED beside the one this block
expected, every gate's real output and exit code, the full suite's summary line, bad node ids and
shrinking comparison, the authored-text proofs, the item-status table AGENTS.md requires (one row
per commit and per gate), the deviations, and the next expected action. Report what you ran, not
what you expected to find. Your Session section reads SESSION 1 of feature F015, round 6, and says
in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round
6, then — if the suite is green — the closure's evidence half, the evidence job and the review
package, and then the closing round; if it is red, the next repair round. State the
open-findings count, 4, and the operator-questions count, 1.

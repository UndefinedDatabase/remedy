STEP F015 R7 — BOOK ROUND 6's FAIL AND FINISH THE FIRST REPAIR ROUND: ITS TESTS, ITS RED PROOFS AND THE SUITE AGAIN

GOAL
Round 6 landed both repairs of DECISION F015 D5 (`a31481b7`, `41e355ba`) and stopped at its G3,
because two research worktrees the reviewer had left under `.claude/worktrees/` reddened
`tests/test_agent_tooling.py`; the reviewer has removed them. Book round 6's FAIL and one prose
slip, run round 6's tests and red proofs over the same repairs, then run the full suite again,
whose transcript replaces `.agent/authored/f015-closure-suite.txt` at the same path (operator
amendment amend0917-throughput rule 2, the first repair round's re-run).

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. This round closes nothing.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f015-r7-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f015-r6-scratch/` and `.remedy-wt/f015-r6-payloads/`  The reviewer's round 6 script
                                  and mutation tool, run unchanged; do not edit them.
  `.remedy-wt/f015-r7-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, `ln`, `npm ci`, `npm install`, process substitution,
`cd <dir> && git ...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`.
Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when
you pipe. Use `git -C <path>` rather than `cd`. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`). Never use `git stash` in any form.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f015-interactive-plan-editing`, and `git log --oneline -1` must read `149f9bab`.
   Report all three, and report `ls .claude/worktrees`, which must list nothing.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f015-r7-block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f015-r7-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype or edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 19 | 7745 | c59bfb9f114c6a32666959c7c932fe0e81b7b28897fad9a37750ecad842da0e1 |
| plan.md | 32 | 1235 | 322ebf35bfa1ba881dbef9e73040f85cd20a9e556b63aec954ef576f269620ab |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; the reviewer
generated it from a tree at `149f9bab` and applied it to a fresh detached worktree at `149f9bab`
with `git apply --check` then `git apply`, both at real exit code 0. It appends the
`Gate: F015 R6 —` entry to `.agent/live_review.md` and one dated line to `.agent/prose_slips.md`.

BUNDLE — the commits are C1, C2 and C3, in this order.

C1 — copy this block and both payloads: `.agent/authored/f015-r7-block.md` := this block, and
  `.agent/authored/f015-r7-<name>` for each payload, by `shutil.copyfile`.
  Subject: `F015 R7 C1: copy round 7 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 51; STOP rather than commit if 500 or more.

C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F015 R7 C2: book round 6's FAIL and one prose slip`
  Expected insertions by `git show --numstat`: 2 live_review.md, 6 plan.md, 1 prose_slips.md.

C3 — THE SUITE AGAIN AND THE HANDBACK, in the PRIMARY checkout, after G1 to G4:
  (a) `bash -c 'npm --prefix apps/ui run build 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'`;
      a refused or failing build is a STOP under constraint 4. Then `git status --porcelain`,
      which must still be empty.
  (b) `python3 -m pytest -n auto -q`, its log written to `.remedy-wt/f015-r7-worker/full-suite.log`.
      REWRITE `.agent/authored/f015-closure-suite.txt` with the command, the real exit code, the
      summary line, the FULL list of bad node ids (failed plus errors) or the literal `NONE`, and a
      shrinking comparison against round 5's bad set — the two node ids DECISION F015 D5 names —
      stating which of them are gone and whether any node is newly bad.
  (c) Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`, and commit it TOGETHER
      with the transcript.
  Subject: `F015 R7 C3: record the repaired closure suite and rewrite handoff for round 7`
  Then `git push origin feature/f015-interactive-plan-editing` and report its real outcome. Do NOT
  create a pull request.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real `git apply`
   and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1.
3. The round's whole tracked path set is: the `.agent/authored/f015-r7-*` copies,
   `.agent/live_review.md`, `.agent/prose_slips.md`, `.agent/plan.md`,
   `.agent/authored/f015-closure-suite.txt` and `.agent/handoff.md`. Report the list you measure
   with `git diff --name-only 149f9bab HEAD` after C3.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. THE ONE EXCEPTION is the full suite in C3: a red suite is
   committed exactly as measured with every bad node id and handed back. Never weaken an assertion,
   delete a test or mark anything xfail.
5. NOTHING IS MERGED, NOTHING IS CLOSED. No `gh pr merge`, no `gh pr create`, no checkout of another
   branch, no branch deletion, no force-push, no STATUS edit, no evidence job, no review package.
6. Leave the `.remedy-wt/job-*` worktrees, their branches, the reviewer's worktrees whose names
   begin `.remedy-wt/f015-`, every `worktree-agent-*` branch, the local branch `sim/f267-r1`, and
   every existing stash alone. The worktree G4 adds goes under `.remedy-wt/`, is removed as that
   step's last action, and `git worktree list` is reported afterwards.
7. The full suite runs ONCE, in C3, and nowhere else this round.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G4 run before C3, and G5 is C3's suite.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured against
 the PAYLOADS table. Then compare each `.agent/authored/f015-r7-*` copy byte for byte with its
 source (the block copy against `.remedy-wt/f015-r7-block.md`), read back with
 `git show <C1>:<path>`. Report one reading per copy.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, which its simulation printed from a tree it built at `149f9bab`:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 304045 | 35f550ea37066b44e1ec72770971f070c019d9c0cbf0f7fd95da2f975427d662 |
 | .agent/prose_slips.md | 367044 | 9dc08b9d1ec7540c6111846fa8df0b4187805ecea7fe0d300376e350c9c1e7f5 |
 | .agent/plan.md | 1235 | 322ebf35bfa1ba881dbef9e73040f85cd20a9e556b63aec954ef576f269620ab |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT, at `149f9bab` and at C2 (the reviewer read
 4 at both — R-0499, R-0950, R-1008 and R-1046 — both differences empty); and the count of lines
 C2's diff adds to `.agent/live_review.md` that begin `Gate: F015 R6 — `, which must be 1.

G3 THE TESTS — in the primary checkout at C2, SERIALLY, with real exit codes:
```
bash .remedy-wt/f015-r6-scratch/g4.sh /home/decodeux/Repos/remedy
```
 The reviewer ran the same script inside its sim worktree carrying C1 (without the block copy) and
 C2 and read `833 passed, 3 skipped` at pytest exit 0, ruff at exit 0, and all six integrity checks `pass` at
 `fail_count` 0. The primary checkout carries the UI toolchain a worktree lacks, so a skip may
 pass there. Report the pytest summary line and exit code, ruff's exit code, and whether all six
 integrity checks read `pass` at `fail_count` 0.

G4 THE RED PROOFS — `git worktree add --detach .remedy-wt/f015-r7-mut <C2>`, then
 `python3 -B .remedy-wt/f015-r6-payloads/mutations.py .remedy-wt/f015-r7-mut` and report its whole
 output. The reviewer read, over the same tool against its sim tree carrying C1 and C2:
 control_before: `4 passed` at exit 0;
 m1_stop_never_waits_for_the_exiting_supervisor: `1 failed, 3 passed` at exit 1;
 m2_a_zero_hang_guard_reproduces_the_suite_failure: `1 failed, 3 passed` at exit 1;
 control_after: `4 passed` at exit 0; every `restored byte-identical` line True.
 Then `git worktree remove --force .remedy-wt/f015-r7-mut`, `git worktree prune`, report
 `git worktree list`, and report `ps aux | grep -c "[r]untime_supervisor"`, which must read 0.

G5 THE SUITE AGAIN — the UI build's last line and real exit code, `git status --porcelain` after it,
 then the full suite's real exit code, summary line, every bad node id and the shrinking comparison,
 all of it in `.agent/authored/f015-closure-suite.txt`.

G6 TREE AND PUSH — after C3: `git status --porcelain`, which must be empty;
 `git log --oneline -n 4`, which must show C3, C2, C1 and `149f9bab` in that order;
 `git worktree list`; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C3 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the insertion count you MEASURED beside the one this block
expected, every gate's real output and exit code, the full suite's summary line, bad node ids and
shrinking comparison, the authored-text proofs, the item-status table AGENTS.md requires (one row
per commit and per gate), the deviations, and the next expected action. Report what you ran, not
what you expected to find. Your Session section reads SESSION 1 of feature F015, round 7, and says
in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round
7, then — if the suite is green — the closure's evidence half, the evidence job and the review
package, and then the closing round; if it is red, the next repair round. State the
open-findings count, 4, and the operator-questions count, 1.

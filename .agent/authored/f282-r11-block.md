STEP F282 R11 — THE CLOSURE SUITE'S FIRST REPAIR ROUND: BOOK ROUND 10, GIVE EACH PACKER RUN ITS OWN STAMP, RUN THE SUITE AGAIN

GOAL
Book round 10's PASS and the resolutions of R-0662, R-0819 and R-0820; record DECISION F282 D11;
repair the closure suite's one bad node,
`tests/orchestration/test_review_zip_hygiene.py::TestThePackerRefusesRootLeftovers::test_the_packages_own_output_directory_is_not_its_own_detritus`,
whose two packer runs could derive one archive name inside one wall-clock second; and run the full
suite again, replacing the closure transcript at its path (amend0917-throughput rule 2).

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. This round closes nothing: no commit may touch
`docs/roadmap/STATUS.md`, `README.md` or `scripts/self_use_queue.json`, and there is no evidence
job and no review zip.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f282-r11-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f282-r11-scratch/`   The reviewer's scripts; do not edit or delete them.
  `.remedy-wt/f282-r11-worker/`    YOURS for logs and scripts. All three are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, `ln`, `npm ci`, `npm install`, process substitution,
`cd <dir> && git ...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`.
Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when
you pipe. Use `git -C <path>` rather than `cd`. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`). A heredoc containing a dollar-brace is refused: write such a script to a
file under your own directory and run the file. The `remedy` CLI is denied: run
`python3 -m apps.cli.main ...`. Never use `git stash` in any form.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f282-findings-paydown-v2`, and `git log --oneline -1` must read `720e15e6`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f282-r11-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f282-r11-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.diff | 16 | 6694 | c095df0fdb73040f60f9b113a4143a6d1c84e6f6de07e642663413f2af026d02 |
| decisions.diff | 30 | 2503 | 5ff1117c1a146ff5097e7af7a489cec6d19f5ce264e736a01bd4834094cfa8bb |
| plan.md | 30 | 1148 | 8d267f9997a0b582873f9ffca770e8ea977376602aad1cb457f0960d874d3802 |
| product.diff | 53 | 2880 | 715296464bfbd7f8ce7224d5a7d6b23f98cb0a20eb90b9389b5c064136f9e737 |
| mutations.py | 44 | 1951 | c4c143fdfe11165df5cba12ab39f2f2ef9656edc0e7ae73fb9466bf517b49c5a |

`plan.md` is a REWRITE of `.agent/plan.md`, copied whole. The `.diff` files go on with
`git apply`; the reviewer generated every one from a tree at `720e15e6` and applied all of
them, in the commit order below, to a fresh worktree at `720e15e6` with `git apply --check`
then `git apply`, every one at real exit code 0. `ledger.diff` appends four paragraphs to
`.agent/live_review.md` — the `Gate: F282 R10` entry and the `Done:` lines of R-0662, R-0819 and
R-0820. `product.diff` edits `tests/orchestration/test_review_zip_hygiene.py` only: the one bad
node's two packer runs each get their own archive stamp through a `date` on PATH. `mutations.py`
is a TOOL for G4: it is run, never applied.

BUNDLE — the commits are C1, C2, C3 and C4, in this order.

C1 — copy this block and every payload: `.agent/authored/f282-r11-block.md` := this block, and one
  `.agent/authored/f282-r11-<name>` for each payload, keeping its own file name. All by
  `shutil.copyfile`.
  Subject: `F282 R11 C1: copy round 11 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 173. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C2 — THE BOOKKEEPING, in this order:
   1. `git apply` ledger.diff     → `.agent/live_review.md`
   2. `git apply` decisions.diff  → `.agent/decisions.md`
   3. rewrite `.agent/plan.md` := plan.md
  Subject: `F282 R11 C2: book round 10, resolve R-0662, R-0819 and R-0820 and record DECISION F282 D11`
  Expected by `git show --numstat` (insertions/deletions): 22/0 decisions.md,
  8/0 live_review.md, 7/9 plan.md.

C3 — THE REPAIR: `git apply` product.diff.
  Subject: `F282 R11 C3: give each packer run of the output-directory test its own archive stamp`
  Expected (insertions/deletions): 24/14 test_review_zip_hygiene.py.

C4 — THE SUITE AGAIN AND THE HANDBACK, in the PRIMARY checkout, after G1 to G4:
  (a) `python3 -m pytest -n auto -q`, its log written to `.remedy-wt/f282-r11-worker/full-suite.log`.
      Rewrite `.agent/authored/f282-closure-suite.txt` WHOLE, in the shape round 10 gave it: the
      summary line, the real exit code and the FULL list of bad node ids, or the literal `NONE`.
  (b) Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`, and commit it TOGETHER
      with the transcript.
  Subject: `F282 R11 C4: record the repaired closure suite and rewrite handoff for round 11`
  Then `git push origin feature/f282-findings-paydown-v2` and report its real outcome. Do NOT
  create a pull request.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1.
3. The round's whole tracked path set is: the `.agent/authored/f282-r11-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `tests/orchestration/test_review_zip_hygiene.py`, `.agent/authored/f282-closure-suite.txt` and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only 720e15e6 HEAD`
   after C4.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. THE ONE
   EXCEPTION is the full suite in C4: a red suite is committed exactly as measured with every bad
   node id, and the round hands back. Never weaken an assertion, delete a test or mark anything
   xfail on your own initiative.
5. NOTHING IS MERGED, NOTHING IS CLOSED. No `gh pr merge`, no `gh pr create`, no checkout of
   `main`, no branch deletion, no force-push, no STATUS edit, no evidence job, no review zip.
6. Leave `.remedy-wt/job-129b3ad7206d4f8d`, `.remedy-wt/job-6a38b3203cca4928`,
   `.remedy-wt/job-e7268925db3a4831`, `.remedy-wt/job-e7a145761bf04f86`, the reviewer's
   `.remedy-wt/f282-r11-dry` and `.remedy-wt/f282-r11-sim`, their branches and every existing
   stash alone. The worktree G4 adds goes under `.remedy-wt/`, is removed as that step's last
   action, and `git worktree list` is reported afterwards (finding R-0940).
7. The full suite runs ONCE, in C4, and nowhere else this round: the repair round's one run
   amend0917-throughput rule 2 requires to show the bad set shrinking.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G4 run before C4 is written, and G5
is the suite C4 runs.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f282-r11-*` copy byte for
 byte with its source (the block copy against `.remedy-wt/f282-r11-block.md`), read back with
 `git show <C1>:<path>`. Report one reading per copy.

G2 THE BOOKKEEPING AND THE REPAIR — the sha256 of each file below, read with
 `git show <commit>:<path>` at the commit named, equals the reviewer's reading, which its
 simulation printed from a tree it built by applying these payloads at `720e15e6`:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/live_review.md | 434178 | dd09d9ddef4080eecd6a09c8a59888b1997303da83b89e5868d4bf732ce4e298 |
 | C2 | .agent/decisions.md | 1936565 | 1b5be316ad586800aa90266bb847dea7421b6ff9a3d7995bd5635c84fae6f745 |
 | C2 | .agent/plan.md | 1148 | 8d267f9997a0b582873f9ffca770e8ea977376602aad1cb457f0960d874d3802 |
 | C3 | tests/orchestration/test_review_zip_hygiene.py | 52845 | f7f90cc4a4f26b7ee25eeb2518e2516607e738cd3fe0f20d5d99c6fd1d19c14c |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `720e15e6` and at C2, with the set
 difference in both directions (the reviewer read 6 and 3, R-0662, R-0819 and R-0820 leaving and
 none arriving); and `git diff --name-only` between C1 and C2 and between C2 and C3, which must
 name exactly the paths each commit lists.

G3 THE LINTER ON THIS BLOCK AND THE TESTS — at C3, in the primary checkout:
 `python3 -m apps.cli.main integrity block .remedy-wt/f282-r11-block.md`, real exit code 0,
 every item `[OK]`, its whole output reported. Then:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_review_zip_hygiene.py tests/docs/ tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection under `-n 8` inside its simulation tree at the C3 it built
 and read `481 passed` at real exit code 0. Then `python3 -m ruff check
 tests/orchestration/test_review_zip_hygiene.py`, real exit code 0; and
 `python3 -m apps.cli.main integrity check --json`, all six checks `pass` at `fail_count` 0.

G4 THE RED PROOFS — `git worktree add --detach .remedy-wt/f282-r11-mut <C3>`, then
 `python3 -B .remedy-wt/f282-r11-payloads/mutations.py .remedy-wt/f282-r11-mut` and report its
 whole output. The reviewer read, over the same script against a tree byte-identical to C3:
 control_before `1 passed` at exit 0;
 m1 (both runs read one second, the closure suite's own failure) 1 failed at exit 1;
 m2 (the stamp shim is not on PATH) 1 failed at exit 1;
 control_after `1 passed` at exit 0; every `restored byte-identical` line True. Then
 `git worktree remove --force .remedy-wt/f282-r11-mut`, `git worktree prune`, and report
 `git worktree list`.

G5 THE SUITE AGAIN — its real exit code, its summary line and every bad node id, all of it in
 `.agent/authored/f282-closure-suite.txt`. Round 10's run read one bad node, the one repaired
 here; report whether that node is absent and whether any node is newly bad (the shrinking rule).

G6 TREE AND PUSH — after C4: `git status --porcelain`, which must be empty;
 `git log --oneline -n 5`, which must show C4, C3, C2, C1 and `720e15e6` in that order;
 `git worktree list`, which must show the primary checkout and exactly the worktrees constraint 6
 names; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C4 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the insertion count you MEASURED beside the one this block
expected, every gate's real output and exit code, the suite's summary line and bad node ids, the
authored-text proofs, the item-status table AGENTS.md requires (one row per commit and per gate),
the deviations, and the next expected action. Report what you ran, not what you expected to find.
Your Session section reads SESSION 2 of feature F282, round 11, and says in one sentence how much
context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round
11, then the evidence job and the review package, then the closing round. State the
open-findings count, 3, and the operator-questions count, 0.

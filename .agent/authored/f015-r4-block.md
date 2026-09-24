STEP F015 R4 — BOOK R3 AND LAND T003: the approved plan is the plan that runs, proven by hash

GOAL
Round 3 passed at `e48fa989`. Book its verdict, record DECISION F015 D4, and land T003: an
approval records the plan's content hash, `run_job` refuses at every start a job whose plan or
task list is not the one its approval covered, an edit may not put a task before a task it
waits for (a job runs its tasks in plan order), an edited revision's `plan_v<n>.md` names its
edits, three frozen revision goldens, and an end-to-end run proving an edited, split and
reordered plan runs in exactly its edited shape — with tests and red proofs.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge.

WHY THIS IS NEXT
T5_F015.md's last slice. DECISION F015 D4 (in records.diff) fixes the shape. The closure
sequence follows.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f015-r4-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f015-r4-scratch/`   The reviewer's scripts; do not edit or delete them.
  `.remedy-wt/f015-r4-worker/`    YOURS for logs and scripts; create it if absent. All three are
                                  gitignored.

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
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f015-interactive-plan-editing`, and `git log --oneline -1` must read `e48fa989`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f015-r4-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f015-r4-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 63 | 10942 | b4081ab055839ff6590caa9b3ec08f65838c3bf4c0573f562e4e462ef9b103ff |
| product.diff | 224 | 10920 | c3d28acc3f9d9cb7633d8bd84a59fe95f3f9f8914f6d19de7f72b8efbfd5eb86 |
| tests.diff | 14 | 1017 | c1e790f0c74170b4de045617d01b1b0d68c64e60e0b067b2919602a10d735b6a |
| mutations.py | 93 | 3384 | 2c128692ae7f9d9cbeb53496c11d40d45edc5a380428606978cfa3f9ba094fdc |
| plan.md | 32 | 1130 | 6c0e0c62b5cbf8e56ccfede940b41a66ed70c0b9fa9b277cb6690ec88b5b53d2 |
| test_plan_edit_execution.py | 205 | 8201 | c19fefdfee8306a47338edb06ad374c4a445bdf0766c484163c6247bb8cdc20a |
| plan_v2.md | 60 | 900 | 5e4a6fb1a03bcc279d156dd14078dbe89d99449b4c647391e911b01cb8f72dd4 |
| plan_v3.md | 61 | 937 | 0c16e932b6237b5c3900db3eaaebadd9c9274ad6fec9d3a78f3ba689064a8008 |
| plan_v4.md | 63 | 1006 | c8f6df3fcd30e870ec06cebe9d1d4289402acf2072e8b6a0e462bd49b8be69cb |

`plan.md` is a REWRITE of `.agent/plan.md`. `test_plan_edit_execution.py` is a NEW FILE at
`tests/orchestration/test_plan_edit_execution.py`, and `plan_v2.md`, `plan_v3.md` and
`plan_v4.md` are NEW FILES under `tests/orchestration/fixtures/plan_editing/golden/`, each
copied whole under its own name. The `.diff` files go on with `git apply`; the reviewer
generated all three from a tree at `e48fa989` and applied them, in the commit order below, to a
fresh detached worktree at `e48fa989` with `git apply --check` then `git apply`, every one at
real exit code 0. `records.diff` appends the `Gate: F015 R3 —` entry to `.agent/live_review.md`
and DECISION F015 D4 to `.agent/decisions.md`. `product.diff` edits the paths C3 lists; its edit
of `tests/ui_server/test_command_dispatch.py` moves round 3's door fixture onto a plan the new
order rule admits, so it lands with the rule. `tests.diff` edits
`tests/orchestration/test_plan_editing.py`. `mutations.py` is a TOOL for G5: it is run, never
applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C1c, C2, C3, C4 and C5, in this order.

C1a — copy this block, the plan payload and the mutation tool
  `.agent/authored/f015-r4-block.md` := this block, and `.agent/authored/f015-r4-<name>` for each
  of plan.md and mutations.py. All by `shutil.copyfile`.
  Subject: `F015 R4 C1a: copy round 4 block, plan payload and mutation tool into .agent/authored/`
  Its insertions are this block's line count plus 125. Report the number you measure
  and STOP rather than commit if it is 500 or more.

C1b — copy the three diffs
  `.agent/authored/f015-r4-<name>` for each of records.diff, product.diff and tests.diff.
  Subject: `F015 R4 C1b: copy round 4 diffs into .agent/authored/`
  Expected insertions: 301.

C1c — copy the new test module and the goldens
  `.agent/authored/f015-r4-<name>` for each of test_plan_edit_execution.py, plan_v2.md,
  plan_v3.md and plan_v4.md.
  Subject: `F015 R4 C1c: copy round 4 new test module and goldens into .agent/authored/`
  Expected insertions: 389.

C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F015 R4 C2: book round 3's PASS and record D4`
  Expected insertions by `git show --numstat`: 45 decisions.md, 2 live_review.md, 9 plan.md.

C3 — THE PRODUCT: `git apply` product.diff and `git add` every path it edits:
  `packages/orchestration/job_plan.py`, `packages/orchestration/pingpong_job.py`,
  `packages/orchestration/plan_editing.py` and `tests/ui_server/test_command_dispatch.py`.
  Subject: `F015 R4 C3: record the approved plan's hash and refuse to run any other plan`
  Expected insertions: 63 job_plan.py, 11 pingpong_job.py, 16 plan_editing.py, 6 test_command_dispatch.py.

C4 — THE TESTS: `git apply` tests.diff; copy test_plan_edit_execution.py to
  `tests/orchestration/test_plan_edit_execution.py` and plan_v2.md, plan_v3.md and plan_v4.md
  into `tests/orchestration/fixtures/plan_editing/golden/` (create the directory); `git add` the
  five paths.
  Subject: `F015 R4 C4: prove an edited plan runs in its edited shape, with its goldens`
  Expected insertions: 60 plan_v2.md, 61 plan_v3.md, 63 plan_v4.md, 205 test_plan_edit_execution.py, 3 test_plan_editing.py.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F015 R4 C5: rewrite handoff for round 4`
  Then `git push origin feature/f015-interactive-plan-editing`. Do NOT create a pull request:
  the branch opens one at F015's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f015-r4-*` copies, the paths C2,
   C3 and C4 name, and `.agent/handoff.md`. Report the list you measure with
   `git diff --name-only e48fa989 HEAD` after C5. Do NOT touch `.agent/candidates.md`,
   `.agent/operator_questions.md`, `.agent/context.md`, `README.md`, `docs/` or any path not
   named here.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees, their branches, the reviewer's worktrees
   `.remedy-wt/f015-r<n>-dry` and `.remedy-wt/f015-r<n>-sim` for rounds 1 to 4, the local
   branch `sim/f267-r1`, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that step's last action, and `git worktree list` is reported
   afterwards (finding R-0940).
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F015's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f015-r4-*` copy byte for byte
 with its source (the block copy against `.remedy-wt/f015-r4-block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, which its simulation printed from a tree it built by applying these
 payloads at `e48fa989`:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 298319 | 3827eabed3ca1ee56eb9e7789127d87f2ea65ce3275c98ab996c7c77403c8c39 |
 | .agent/decisions.md | 1988277 | 0cb5f6ddcf5408027c41176cdf10a19fdc28b75b79e2f554e59f1898d4d5f093 |
 | .agent/plan.md | 1130 | 6c0e0c62b5cbf8e56ccfede940b41a66ed70c0b9fa9b277cb6690ec88b5b53d2 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT, at `e48fa989` and at C2, with the set
 difference in both directions (the reviewer read 4 at both — R-0499, R-0950, R-1008 and
 R-1046 — and both differences empty); and the count of lines C2's diff adds to
 `.agent/live_review.md` that begin `Gate: F015 R3 — `, which must be 1.

G3 THE PRODUCT AND ITS TESTS — at C4, the sha256 of each file below, read with
 `git show <C4>:<path>`, equals the reviewer's simulated reading:
 | path | bytes | sha256 |
 |---|---|---|
 | packages/orchestration/job_plan.py | 33772 | e7f4b8259758db797b268acefba5ffbbb38749cb2dfd591e81f4309d7a8c9a82 |
 | packages/orchestration/pingpong_job.py | 203981 | 8e731a4479fd4b7aeb517a231114a49472b3c17a5e72e2a6310f5533ab0d913a |
 | packages/orchestration/plan_editing.py | 20915 | 9d40a0f26b7707690254deb5f2944a53e36953e955aba5f7655b9c6b3cfe6354 |
 | tests/ui_server/test_command_dispatch.py | 37631 | 07d38fe7b5b63b2c53135d1c01be358fa20c09d3c2ab0b7f55c3ac75e9c74e99 |
 | tests/orchestration/test_plan_editing.py | 17333 | d393703d78f6b251a354d4c4e2e282b911a154e788cbd52a38324f6ed09e2b82 |
 | tests/orchestration/test_plan_edit_execution.py | 8201 | c19fefdfee8306a47338edb06ad374c4a445bdf0766c484163c6247bb8cdc20a |
 | tests/orchestration/fixtures/plan_editing/golden/plan_v2.md | 900 | 5e4a6fb1a03bcc279d156dd14078dbe89d99449b4c647391e911b01cb8f72dd4 |
 | tests/orchestration/fixtures/plan_editing/golden/plan_v3.md | 937 | 0c16e932b6237b5c3900db3eaaebadd9c9274ad6fec9d3a78f3ba689064a8008 |
 | tests/orchestration/fixtures/plan_editing/golden/plan_v4.md | 1006 | c8f6df3fcd30e870ec06cebe9d1d4289402acf2072e8b6a0e462bd49b8be69cb |
 Also `git diff --name-only <C2> <C3>` and `<C3> <C4>`, which must name exactly the paths C3 and
 C4 list.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash .remedy-wt/f015-r4-scratch/g4.sh /home/decodeux/Repos/remedy
```
 The script runs one pytest selection (the execution-fidelity, plan-editing and plan tests; the
 job runner, worktree hand-off, stop, clarification, self-use, approval, CLI and door tests
 that reach `run_job`, the approval or the renderer; the BLE001 and durable-write guards;
 `tests/docs/`, the roadmap index, the state-file readers, the ledger and block-lint tests and
 `tests/cli/test_golden_path.py`), then `ruff check` over the touched Python files, then
 `python3 -m apps.cli.main integrity check --json`, each followed by its real exit code. The
 reviewer ran the same script inside its sim worktree carrying C1a (without the block copy) to C4
 and read `1282 passed, 2 skipped` at pytest exit 0, ruff at exit 0, and all six integrity checks `pass` at
 `fail_count` 0 with `handlers=157`. The primary checkout carries the UI toolchain a worktree
 lacks, so a skip may pass there, and your tree carries the block copy the sim lacked, which a
 test parametrized over the saved blocks may count once more. Report the three readings you get:
 the pytest summary line and exit code, ruff's exit code, and whether all six integrity checks
 read `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f015-r4-mut <C4>`, then
 `python3 -B .remedy-wt/f015-r4-payloads/mutations.py .remedy-wt/f015-r4-mut` and report its
 whole output. The script asserts each FROM occurs exactly once, applies it, runs the three test
 files it names under `python3 -B`, restores the bytes, and runs an unmutated control first and
 last. The reviewer read, over the same script against its sim tree carrying C1a to C4:
 control_before `80 passed` at exit 0;
 m1 (a task may precede a task it waits for) 1 failed at exit 1;
 m2 (the human approval records no hash) 3 failed at exit 1;
 m3 (a rejection records a hash) 1 failed at exit 1;
 m4 (the unattended approval records no hash) 1 failed at exit 1;
 m5 (the hash covers the bookkeeping keys) 5 failed at exit 1;
 m6 (the task list is not compared) 1 failed at exit 1;
 m7 (a plan approved before the hash is refused) 1 failed at exit 1;
 m8 (the start never checks the plan) 2 failed at exit 1;
 m9 (a revision names no edit) 3 failed at exit 1;
 m10 (an edited plan says it is used as generated) 3 failed at exit 1;
 control_after `80 passed` at exit 0; every `restored byte-identical` line True (10 of them).
 Then `git worktree remove --force .remedy-wt/f015-r4-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 8`, which must show C5, C4, C3, C2, C1c, C1b, C1a and `e48fa989` in that
 order; `git worktree list`, which must show the primary checkout, the `.remedy-wt/job-*`
 worktrees and the reviewer's worktrees constraint 6 names, and nothing else; the push's real
 outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which
 must be EMPTY. These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F015, round 4, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 4, then the closure sequence's first half — the Built State of
`docs/roadmap/features/T5_F015.md`, the checklist consolidation, the self-use track and the one
full suite. State the open-findings count, 4, and the operator-questions count, 1.

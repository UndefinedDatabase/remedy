STEP F015 R3 — BOOK R2 AND LAND T002's SECOND HALF: the six plan edits through the write door

GOAL
Round 2 passed at `1a95e306`. Book its verdict, record DECISION F015 D3, and land T002's second
half: the write door exposes `job.plan-edit-task`, `job.plan-delete-task`, `job.plan-reorder`,
`job.plan-merge-tasks`, `job.plan-split-task` and `job.plan-edit-acceptance`, each run through
`plan_editing.edit_plan` with a required `args.expected_version`, attributed to the request's
token fingerprint, and each refusal answered with the status and reason D3 rules, with tests
and red proofs.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge.

WHY THIS IS NEXT
T5_F015.md orders T002's channel wiring after the edit window, and the backend and catalog ids
are in place. DECISION F015 D3 (in records.diff) fixes the door's shape. T003, execution
fidelity, follows.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f015-r3-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f015-r3-scratch/`   The reviewer's scripts; do not edit or delete them.
  `.remedy-wt/f015-r3-worker/`    YOURS for logs and scripts; create it if absent. All three are
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
   `feature/f015-interactive-plan-editing`, and `git log --oneline -1` must read `1a95e306`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f015-r3-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f015-r3-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 55 | 10308 | 34bf7105e76e56942c46005ebb8322c095bc90373e5362bfcd3b1189b705da1c |
| product.diff | 195 | 11252 | 873f43772a0236ab1a0a86767f7336c1f6fcc6c5e1c626b03e9f2f480a73df9f |
| tests.diff | 178 | 9299 | 78277c4557900c227ba38fae0d59fbe7acf58a9e88bd323c0981bd1768e38286 |
| mutations.py | 91 | 3662 | 13ea901afcdf7efb6c239014b4e5b1a1360af70c888c2877a814f5cba5aa481f |
| plan.md | 30 | 1040 | a2c3be5945057825c6412baf35c29b1c938cc3848b14c5acf7a4748f0112a013 |

`plan.md` is a REWRITE of `.agent/plan.md`. The `.diff` files go on with `git apply`; the
reviewer generated all three from a tree at `1a95e306` and applied them, in the commit order
below, to a fresh detached worktree at `1a95e306` with `git apply --check` then `git apply`,
every one at real exit code 0. `records.diff` appends the `Gate: F015 R2 —` entry to
`.agent/live_review.md` and DECISION F015 D3 to `.agent/decisions.md`. `product.diff` edits the
paths C3 lists. `tests.diff` edits `tests/ui_server/test_command_dispatch.py`. `mutations.py` is
a TOOL for G5: it is run, never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C2, C3, C4 and C5, in this order.

C1a — copy this block, the plan payload and the mutation tool
  `.agent/authored/f015-r3-block.md` := this block, and `.agent/authored/f015-r3-<name>` for each
  of plan.md and mutations.py. All by `shutil.copyfile`.
  Subject: `F015 R3 C1a: copy round 3 block, plan payload and mutation tool into .agent/authored/`
  Its insertions are this block's line count plus 121. Report the number you measure
  and STOP rather than commit if it is 500 or more.

C1b — copy the three diffs
  `.agent/authored/f015-r3-<name>` for each of records.diff, product.diff and tests.diff.
  Subject: `F015 R3 C1b: copy round 3 diffs into .agent/authored/`
  Expected insertions: 428.

C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F015 R3 C2: book round 2's PASS and record D3`
  Expected insertions by `git show --numstat`: 37 decisions.md, 2 live_review.md, 7 plan.md.

C3 — THE PRODUCT: `git apply` product.diff and `git add` every path it edits:
  `apps/cli/command_catalog.py`, `packages/orchestration/ui_server.py` and
  `tests/ui_server/test_command_channel.py`.
  Subject: `F015 R3 C3: expose the six job plan edits through the write door`
  Expected insertions: 7 command_catalog.py, 96 ui_server.py, 9 test_command_channel.py.

C4 — THE TESTS: `git apply` tests.diff and `git add` `tests/ui_server/test_command_dispatch.py`.
  Subject: `F015 R3 C4: test each door edit, its refusals and its replay`
  Expected insertions: 170.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F015 R3 C5: rewrite handoff for round 3`
  Then `git push origin feature/f015-interactive-plan-editing`. Do NOT create a pull request:
  the branch opens one at F015's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f015-r3-*` copies, the paths C2,
   C3 and C4 name, and `.agent/handoff.md`. Report the list you measure with
   `git diff --name-only 1a95e306 HEAD` after C5. Do NOT touch `.agent/candidates.md`,
   `.agent/operator_questions.md`, `.agent/context.md`, `README.md`, `docs/` or any path not
   named here.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees, their branches, the reviewer's worktrees
   `.remedy-wt/f015-r1-dry`, `.remedy-wt/f015-r1-sim`, `.remedy-wt/f015-r2-dry`,
   `.remedy-wt/f015-r2-sim`, `.remedy-wt/f015-r3-dry` and `.remedy-wt/f015-r3-sim`, the local
   branch `sim/f267-r1`, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that step's last action, and `git worktree list` is reported
   afterwards (finding R-0940).
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F015's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f015-r3-*` copy byte for byte
 with its source (the block copy against `.remedy-wt/f015-r3-block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, which its simulation printed from a tree it built by applying these
 payloads at `1a95e306`:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 296098 | cc40dce56989d91a9fa340ee6a31bfa45b427f7ac2548b5f25c6a906a0504738 |
 | .agent/decisions.md | 1984549 | 6b2efb6b7e5933eec3469d22a3748a12c655435c426db551cb48277d756a88db |
 | .agent/plan.md | 1040 | a2c3be5945057825c6412baf35c29b1c938cc3848b14c5acf7a4748f0112a013 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT, at `1a95e306` and at C2, with the set
 difference in both directions (the reviewer read 4 at both — R-0499, R-0950, R-1008 and
 R-1046 — and both differences empty); and the count of lines C2's diff adds to
 `.agent/live_review.md` that begin `Gate: F015 R2 — `, which must be 1.

G3 THE PRODUCT AND ITS TESTS — at C4, the sha256 of each file below, read with
 `git show <C4>:<path>`, equals the reviewer's simulated reading:
 | path | bytes | sha256 |
 |---|---|---|
 | apps/cli/command_catalog.py | 119725 | abe715b074a51d70b87463fa2c5fec1d5a481135736fefa5f3a977f7b2ffd654 |
 | packages/orchestration/ui_server.py | 160376 | 013fb11911304f7c8d141ea4b8ae1c7ce4822ef237a560889d87af49d3ab9307 |
 | tests/ui_server/test_command_channel.py | 95157 | f629afd8ecde1820d2ccf9f685d181cff46b08e86b774a622142085696e6c329 |
 | tests/ui_server/test_command_dispatch.py | 37468 | 1bb3e1a4a492c34a4698693fc0cdf529692748c1cd4d6a935c5d3c146d3e9558 |
 Also `git diff --name-only <C2> <C3>` and `<C3> <C4>`, which must name exactly the paths C3 and
 C4 list.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash .remedy-wt/f015-r3-scratch/g4.sh /home/decodeux/Repos/remedy
```
 The script runs one pytest selection (the door, channel and UI-contract tests; the
 plan-editing, CLI, approval, catalog, exit-code, audit, nonce and decision-inbox tests the door
 reaches; the orphan and reachability guards; `tests/docs/`, the roadmap index, the state-file
 readers, the ledger and block-lint tests and `tests/cli/test_golden_path.py`), then
 `ruff check` over the touched Python files, then `python3 -m apps.cli.main integrity check
 --json`, each followed by its real exit code. The reviewer ran the same script inside its sim
 worktree carrying C1a (without the block copy) to C4 and read `2184 passed, 6 skipped` at pytest exit 0,
 ruff at exit 0, and all six integrity checks `pass` at `fail_count` 0 with `handlers=157`. The
 primary checkout carries the UI toolchain a worktree lacks, so a skip may pass there, and your
 tree carries the block copy the sim lacked, which a test parametrized over the saved blocks may
 count once more. Report the three readings you get: the pytest summary line and exit code,
 ruff's exit code, and whether all six integrity checks read `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f015-r3-mut <C4>`, then
 `python3 -B .remedy-wt/f015-r3-payloads/mutations.py .remedy-wt/f015-r3-mut` and report its
 whole output. The script asserts each FROM occurs exactly once, applies it, runs the two test
 files it names under `python3 -B`, restores the bytes, and runs an unmutated control first and
 last. The reviewer read, over the same script against its sim tree carrying C1a to C4:
 control_before `141 passed` at exit 0;
 m1 (a door id runs the wrong edit) 3 failed at exit 1;
 m2 (a missing version reaches the backend) 2 failed at exit 1;
 m3 (`expected_version` rides into the edit log) 6 failed at exit 1;
 m4 (the editor is not the token's fingerprint) 6 failed at exit 1;
 m5 (a conflict is worded as a closed plan) 1 failed at exit 1;
 m6 (argument refusals are not shape errors) 2 failed at exit 1;
 m7 (an invalid plan hides its violation) 1 failed at exit 1;
 m8 (a closed plan is a server fault) 1 failed at exit 1;
 m9 (refusals fall to the generic clause) 5 failed at exit 1;
 m10 (an edit is not exposed) 2 failed at exit 1;
 control_after `141 passed` at exit 0; every `restored byte-identical` line True (10 of them).
 Then `git worktree remove --force .remedy-wt/f015-r3-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 7`, which must show C5, C4, C3, C2, C1b, C1a and `1a95e306` in that
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
section reads SESSION 1 of feature F015, round 3, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 3, then T003 — the plan's content hash recorded when the approval is consumed and
asserted when the job starts, the `plan.md` revision goldens, and the end-to-end run of an
edited plan. State the open-findings count, 4, and the operator-questions count, 1.

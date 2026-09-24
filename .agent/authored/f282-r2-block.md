STEP F282 R2 — BOOK ROUND 1, RESOLVE T002 BY EVIDENCE AND LAND T003, R-1041's OPEN-SET RULE

GOAL
Book round 1's PASS and R-0998's resolution; resolve R-1009, R-1043, R-1044 and R-0880 by the
evidence the reviewer measured; record DECISION F282 D2; and land T003: `check_open_set` in
`packages/orchestration/block_lint.py` checks a stated open-findings count against the open set
AFTER the round, reading the ids the block's ledger payloads register and resolve (R-1041).

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f282-r2-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f282-r2-scratch/`   The reviewer's scripts; do not edit or delete them.
  `.remedy-wt/f282-r2-worker/`    YOURS for logs and scripts. All three are gitignored.

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
2. `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f282-findings-paydown-v2`, and `git log --oneline -1` must read `5f9e4725`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f282-r2-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f282-r2-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.diff | 20 | 13589 | 2de23ae4808b8f7a935b506e0836f899ddd26f641eb2e36a4b5a14c77d07ab71 |
| decisions.diff | 27 | 2192 | 66ead76ea5874f4e7b9be097208273254dfc445c6a4e15f70f2f402d254935b9 |
| plan.md | 30 | 1166 | ede3d94c9d60ecf0bd262783e8b093956306de29294cde4caa8be3eb58cf7e2d |
| product.diff | 69 | 3571 | 43e4ac04a6883ee7ea99c75394aaf773673b3ab8f740eccb1890da606afde6e4 |
| tests.diff | 45 | 2968 | 607132b6326b070d20aa6ecda7e6915e543f1ddee28698bb1145ed3693e5c8c2 |
| mutations.py | 76 | 3362 | efb16d96e7bacfb330099b82ffd209520f1bd2ed586942e0faa1771c2cf6ee23 |

`plan.md` is a REWRITE of `.agent/plan.md`, copied whole. The `.diff` files go on with
`git apply`; the reviewer generated every one from a tree at `5f9e4725` and applied all of
them, in the commit order below, to a fresh worktree at `5f9e4725` with `git apply --check`
then `git apply`, every one at real exit code 0. `ledger.diff` appends six paragraphs to
`.agent/live_review.md` — the `Gate: F282 R1` entry and the `Done:` lines of R-0998, R-1009,
R-1043, R-1044 and R-0880. `mutations.py` is a TOOL for G5: it is run, never applied.

BUNDLE — the commits are C1a, C1b, C2, C3, C4 and C5, in this order.

C1a — copy this block and the bookkeeping payloads
  `.agent/authored/f282-r2-block.md` := this block, and one `.agent/authored/f282-r2-<name>`
  for each of ledger.diff, decisions.diff and plan.md, keeping each payload's own file name.
  All by `shutil.copyfile`.
  Subject: `F282 R2 C1a: copy round 2 block and bookkeeping payloads into .agent/authored/`
  Its insertions are this block's line count plus 77. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the product payloads
  `.agent/authored/f282-r2-<name>` for each of product.diff, tests.diff and mutations.py,
  by `shutil.copyfile`.
  Subject: `F282 R2 C1b: copy round 2 product payloads into .agent/authored/`
  Expected insertions: 190.

C2 — THE BOOKKEEPING, in this order:
   1. `git apply` ledger.diff     → `.agent/live_review.md`
   2. `git apply` decisions.diff  → `.agent/decisions.md`
   3. rewrite `.agent/plan.md` := plan.md
  Subject: `F282 R2 C2: book round 1, resolve five findings and record DECISION F282 D2`
  Expected insertions by `git show --numstat`: 19 decisions.md, 12 live_review.md, 8 plan.md.

C3 — THE PRODUCT: `git apply` product.diff → `packages/orchestration/block_lint.py`.
  Subject: `F282 R2 C3: count the open set after the round from the block's ledger payloads`
  Expected insertions: 42 (4 deletions).

C4 — THE TESTS: `git apply` tests.diff → `tests/orchestration/test_block_lint.py`.
  Subject: `F282 R2 C4: test the open-set rule against a block's ledger payloads, R-1041`
  Expected insertions: 34.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F282 R2 C5: rewrite handoff for round 2`
  Then `git push origin feature/f282-findings-paydown-v2` and report its real outcome. Do
  NOT create a pull request.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f282-r2-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `packages/orchestration/block_lint.py`, `tests/orchestration/test_block_lint.py` and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only 5f9e4725 HEAD`
   after C5. Do NOT touch `.agent/prose_slips.md`, `.agent/candidates.md`,
   `.agent/operator_questions.md`, `.agent/context.md`, `README.md` or anything under `docs/`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch
   deletion, no force-push, no `git stash`.
6. Leave `.remedy-wt/job-129b3ad7206d4f8d`, `.remedy-wt/job-6a38b3203cca4928`,
   `.remedy-wt/job-e7268925db3a4831`, `.remedy-wt/job-e7a145761bf04f86`, the reviewer's
   `.remedy-wt/f282-r1-dry`, `.remedy-wt/f282-r1-sim`, `.remedy-wt/f282-r2-dry` and
   `.remedy-wt/f282-r2-sim`, their branches and every existing stash alone. The worktree G5
   adds goes under `.remedy-wt/`, is removed as that step's last action, and
   `git worktree list` is reported afterwards (finding R-0940).
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run
   and F282's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f282-r2-*` copy byte for
 byte with its source (the block copy against `.remedy-wt/f282-r2-block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE BOOKKEEPING AND THE PRODUCT — the sha256 of each file below, read with
 `git show <commit>:<path>` at the commit named, equals the reviewer's reading, which its
 simulation printed from a tree it built by applying these payloads at `5f9e4725`:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/live_review.md | 392954 | fab69ca590883fc0681edb0c533b774038141d0c8d1ce63370d232153d62a5db |
 | C2 | .agent/decisions.md | 1916192 | 3d3a8e448ff027a57a7378b5f5f6d2c12f454f50f0a9ce76393fe43b4fcb8a1e |
 | C2 | .agent/plan.md | 1166 | ede3d94c9d60ecf0bd262783e8b093956306de29294cde4caa8be3eb58cf7e2d |
 | C3 | packages/orchestration/block_lint.py | 10350 | 7db58f0e5e0abbabc03c4c9ca153c94a555bc9b25ad18d8726ae394d8121baba |
 | C4 | tests/orchestration/test_block_lint.py | 9647 | 2d4f0e0157a1e5cd46ce3e3302691248bcc490fc5da7b692137c6c85123921cd |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `5f9e4725` and at C2, with the set
 difference in both directions (the reviewer read 29 and 24, the ids leaving exactly R-0880,
 R-0998, R-1009, R-1043 and R-1044, none arriving); and `git diff --name-only` between
 consecutive commits from C1b to C4, which must name exactly the paths each commit lists.

G3 THE LINTER ON THIS BLOCK — at C4, in the primary checkout:
 `python3 -m apps.cli.main integrity block .remedy-wt/f282-r2-block.md`, real exit code 0,
 every item `[OK]`. Report the whole output. At C4 the ledger already carries C2's
 resolutions, so the reviewer's reading of its item 10 line in a tree byte-identical to C4 is
 `states 24; .agent/live_review.md holds 24 open by distinct id, and the block registers 0
 and resolves 0, leaving 24`. The reviewer also ran the C3 rule against the ledger as it
 stands at `5f9e4725` and read `states 24; ... holds 29 open by distinct id, and the block
 registers 0 and resolves 5, leaving 24`, while the rule at `5f9e4725` refuses this same
 block with `states 24; .agent/live_review.md holds 29 open by distinct id`.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_block_lint.py tests/orchestration/test_development_artifact_boundary.py tests/orchestration/test_integrity_gate.py tests/test_ble001_ratchet.py tests/orchestration/test_final_audit_evidence.py tests/orchestration/test_live_review_rotation.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path, serially, inside a disposable
 worktree carrying C2 to C4 and read `237 passed, 2 skipped` at real exit code 0; a skip may
 pass in the primary checkout. Then `python3 -m ruff check packages/orchestration/block_lint.py
 tests/orchestration/test_block_lint.py`, real exit code 0;
 `python3 -m apps.cli.main integrity check --json`, all six checks `pass` at `fail_count` 0;
 and, for R-0880's static bound, `python3 -m mypy --no-pretty --ignore-missing-imports
 --no-error-summary --follow-imports=silent packages apps` with its output filtered for lines
 matching `has no attribute "(job_id|task_id)"`: the reviewer read exactly two, at
 `packages/orchestration/token_economy.py:324` and `packages/orchestration/self_use_runner.py:390`,
 and 288 `error:` lines in all. Report the matching lines and the total.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f282-r2-mut <C4>`, then
 `python3 -B .remedy-wt/f282-r2-payloads/mutations.py .remedy-wt/f282-r2-mut` and report its
 whole output; it runs about fifteen minutes. The reviewer read, over the same script against a
 tree byte-identical to C4:
 control_before_lint `28 passed` at exit 0; control_before_self_use `319 passed` at exit 0;
 m1 (the payloads never read) 1 failed at exit 1;
 m2 (every diff section counted, not only the ledger's) 1 failed at exit 1;
 m3 (every whole payload counted, not only a ledger slice) 1 failed at exit 1;
 r1 (`block_lint.py` at `5f9e4725`) 2 failed at exit 1;
 r2 (`self_use_runner.py`, `pingpong_job.py` and `docs/orders/toolchain-refresh.md` at
 `d80f12c1`, before amend0923's repairs) 17 failed at exit 1;
 control_after_lint `28 passed` and control_after_self_use `319 passed`, each at exit 0;
 every `restored byte-identical` line True. Then
 `git worktree remove --force .remedy-wt/f282-r2-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 7`, which must show C5, C4, C3, C2, C1b, C1a and `5f9e4725` in that
 order; `git worktree list`, which must show the primary checkout and exactly the worktrees
 constraint 6 names; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be
 EMPTY. These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F282, round 2, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 2, then T004 and T005, R-1040 and R-1005. State the open-findings count, 24, and
the operator-questions count, 0.

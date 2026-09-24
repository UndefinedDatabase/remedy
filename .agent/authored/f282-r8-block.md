STEP F282 R8 — BOOK ROUND 7, RESOLVE R-0892 BY EVIDENCE AND LAND T017: R-0866's PARKED RAIL ENDS

GOAL
Book round 7's PASS and the resolutions of R-0622 and R-1029, resolve R-0892 by the evidence
F268 and amend0920-selfuse-real already landed (T014), record DECISION F282 D8, and land T017:
a self-improvement attempt stops `blocked` with the stop reason `external_candidate_route_removed`
once its request is prepared, instead of waiting in `awaiting_external_candidate` for a candidate
no command can bring (R-0866).

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f282-r8-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f282-r8-scratch/`   The reviewer's scripts; do not edit or delete them.
  `.remedy-wt/f282-r8-worker/`    YOURS for logs and scripts. All three are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, `ln`, `npm`, process substitution, `cd <dir> && git ...`, and
multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit
codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`). A heredoc containing a dollar-brace is refused: write such a
script to a file under your own directory and run the file.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f282-findings-paydown-v2`, and `git log --oneline -1` must read `7932b7c1`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f282-r8-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f282-r8-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.diff | 16 | 7207 | 61128474799cffe0a7cb34eeeef25da32c5b7ee9419bd7ff023ab64ea4ec7eef |
| decisions.diff | 36 | 3066 | c8ff68c82fc5d0f329f938509d20d9e0a1f3ef23f9ad1b0825f5200621b858b2 |
| plan.md | 31 | 1124 | c55bb0b2d1fe586439c4ac360107f98c040459de630487bdf501996b9cf14f8f |
| product.diff | 147 | 9330 | 6a5287363c6dae5782eaa88c948e83ab7baf7463f7fb96d37cffd9fd4c6ce683 |
| tests.diff | 99 | 5473 | 8e94003b0b8201ed552b78f040e9a319fe0928a33b4ba257c38b1e3364bb9500 |
| mutations.py | 75 | 3404 | c2173f8204af9fc472ff2e5a20039a410a41a899f4de70804bbfe44427b856c8 |

`plan.md` is a REWRITE of `.agent/plan.md`, copied whole. The `.diff` files go on with
`git apply`; the reviewer generated every one from a tree at `7932b7c1` and applied all of
them, in the commit order below, to a fresh worktree at `7932b7c1` with `git apply --check`
then `git apply`, every one at real exit code 0. `ledger.diff` appends four paragraphs to
`.agent/live_review.md` — the `Gate: F282 R7` entry and the `Done:` lines of R-0622, R-1029
and R-0892. `product.diff` edits `packages/orchestration/self_dogfood_execution.py` and
`docs/system/self-dogfood-execution-v0.md`. `tests.diff` edits
`tests/orchestration/test_self_dogfood_execution.py` and
`tests/cli/test_self_dogfood_execution_cli.py`. `mutations.py` is a TOOL for G5: it is run,
never applied.

BUNDLE — the commits are C1a, C1b, C2, C3, C4 and C5, in this order.

C1a — copy this block and the bookkeeping payloads
  `.agent/authored/f282-r8-block.md` := this block, and one `.agent/authored/f282-r8-<name>`
  for each of ledger.diff, decisions.diff and plan.md, keeping each payload's own file name.
  All by `shutil.copyfile`.
  Subject: `F282 R8 C1a: copy round 8 block and bookkeeping payloads into .agent/authored/`
  Its insertions are this block's line count plus 83. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the product and test payloads: `.agent/authored/f282-r8-product.diff`,
  `.agent/authored/f282-r8-tests.diff` and `.agent/authored/f282-r8-mutations.py`, by
  `shutil.copyfile`.
  Subject: `F282 R8 C1b: copy round 8 product and test payloads into .agent/authored/`
  Expected insertions: 321.

C2 — THE BOOKKEEPING, in this order:
   1. `git apply` ledger.diff     → `.agent/live_review.md`
   2. `git apply` decisions.diff  → `.agent/decisions.md`
   3. rewrite `.agent/plan.md` := plan.md
  Subject: `F282 R8 C2: book round 7, resolve R-0622, R-1029 and R-0892 and record DECISION F282 D8`
  Expected by `git show --numstat` (insertions/deletions): 28/0 decisions.md,
  8/0 live_review.md, 10/9 plan.md.

C3 — THE PRODUCT: `git apply` product.diff.
  Subject: `F282 R8 C3: end a self-improvement attempt at the removed candidate route, R-0866`
  Expected (insertions/deletions): 11/7 self-dogfood-execution-v0.md,
  38/15 self_dogfood_execution.py.

C4 — THE TESTS: `git apply` tests.diff.
  Subject: `F282 R8 C4: pin the stop at the removed candidate route, R-0866`
  Expected (insertions/deletions): 4/3 test_self_dogfood_execution_cli.py,
  42/6 test_self_dogfood_execution.py.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F282 R8 C5: rewrite handoff for round 8`
  Then `git push origin feature/f282-findings-paydown-v2` and report its real outcome. Do
  NOT create a pull request.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f282-r8-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, the two product-diff
   paths and the two test paths named above, and `.agent/handoff.md`. Report the list you
   measure with `git diff --name-only 7932b7c1 HEAD` after C5. Do NOT touch
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md`,
   `.agent/context.md`, `README.md` or anything under `docs/roadmap/`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch
   deletion, no force-push, no `git stash`.
6. Leave `.remedy-wt/job-129b3ad7206d4f8d`, `.remedy-wt/job-6a38b3203cca4928`,
   `.remedy-wt/job-e7268925db3a4831`, `.remedy-wt/job-e7a145761bf04f86`, the reviewer's
   `.remedy-wt/f282-r8-dry` and `.remedy-wt/f282-r8-sim`, their branches and every existing
   stash alone. The worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last
   action, and `git worktree list` is reported afterwards (finding R-0940).
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run
   and F282's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f282-r8-*` copy byte for
 byte with its source (the block copy against `.remedy-wt/f282-r8-block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE BOOKKEEPING AND THE PRODUCT — the sha256 of each file below, read with
 `git show <commit>:<path>` at the commit named, equals the reviewer's reading, which its
 simulation printed from a tree it built by applying these payloads at `7932b7c1`:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/live_review.md | 421889 | 46107c56f9b30782ac52de4bf7c458a07bd491532c77ac41db2f3f89964f4ed8 |
 | C2 | .agent/decisions.md | 1929153 | d848f0c46081cfc8f1710253149901a9a6661f28c3b60804d83761e2760234e7 |
 | C2 | .agent/plan.md | 1124 | c55bb0b2d1fe586439c4ac360107f98c040459de630487bdf501996b9cf14f8f |
 | C3 | packages/orchestration/self_dogfood_execution.py | 33836 | 6f0fb4eacf7f62438175a625a4d2191233813ee0f78936b658c448c14950e69d |
 | C3 | docs/system/self-dogfood-execution-v0.md | 4735 | e8da49499a50ce5c5b3cad5e82173d409742684fafb6636c58b66b3f1287f20d |
 | C4 | tests/orchestration/test_self_dogfood_execution.py | 15314 | 0b8a4871d380601497840bd8aa3f640729429a775d568988c8049ebdaaec32f2 |
 | C4 | tests/cli/test_self_dogfood_execution_cli.py | 5541 | 2af5b2aa2fc8d1e32085a58b57803dd6afe17a65b8d444ccf5c90de1967d28f2 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `7932b7c1` and at C2, with the set
 difference in both directions (the reviewer read 11 and 8, R-0622, R-0892 and R-1029 leaving
 and none arriving); and `git diff --name-only` between consecutive commits from C1b to C4,
 which must name exactly the paths each commit lists.

G3 THE LINTER ON THIS BLOCK — at C4, in the primary checkout:
 `python3 -m apps.cli.main integrity block .remedy-wt/f282-r8-block.md`, real exit code 0,
 every item `[OK]`. Report the whole output.

G4 THE TESTS AND THE LINT — in the primary checkout at C4, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_self_dogfood_execution.py tests/cli/test_self_dogfood_execution_cli.py tests/ui_server/test_dashboard_cockpit_truth.py tests/cli/test_do_evidence_package.py tests/docs/ tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection under `-n 8` inside its simulation tree at the C4 it
 built and read `515 passed, 1 skipped` at real exit code 0. Then `python3 -m ruff check`
 over `packages/orchestration/self_dogfood_execution.py` and the two test files, real exit
 code 0; and `python3 -m apps.cli.main integrity check --json`, all six checks `pass` at
 `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f282-r8-mut <C4>`, then
 `python3 -B .remedy-wt/f282-r8-payloads/mutations.py .remedy-wt/f282-r8-mut` and report its
 whole output. The reviewer read, over the same script against a tree byte-identical to C4:
 control_before `31 passed` at exit 0;
 m1 (a started attempt parks again) 3 failed at exit 1;
 m2 (reconcile leaves the parked attempt) 1 failed at exit 1;
 m3 (reconcile ends an attempt whose intent is on disk) 1 failed at exit 1;
 m4 (a second start prepares a second attempt) 2 failed at exit 1;
 m5 (the next action sends the operator to reconcile again) 3 failed at exit 1;
 r1 (`self_dogfood_execution.py` at `7932b7c1`) 5 failed at exit 1;
 control_after `31 passed` at exit 0; every `restored byte-identical` line True. Then
 `git worktree remove --force .remedy-wt/f282-r8-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 7`, which must show C5, C4, C3, C2, C1b, C1a and `7932b7c1` in
 that order; `git worktree list`, which must show the primary checkout and exactly the
 worktrees constraint 6 names; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be
 EMPTY. These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 2 of feature F282, round 8, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 8, then T018 — R-0950, R-1028 and R-0499. State the open-findings count, 8, and
the operator-questions count, 0.

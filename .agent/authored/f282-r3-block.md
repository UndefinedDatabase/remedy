STEP F282 R3 — BOOK ROUND 2 AND LAND T004 AND T005: R-1040's KEPT COST AND R-1005's DEADLINE STOP

GOAL
Book round 2's PASS and R-1041's resolution, record DECISION F282 D3, and land two repairs:
`_cmd_job_budget` in `apps/cli/commands/job.py` keeps the cost a job recorded when the cost
ledger names no call for it (R-1040), and `packages/orchestration/run_manifest.py` lets a
deadline budget stop write its run manifest and finalize (R-1005), with tests and red proofs.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f282-r3-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f282-r3-scratch/`   The reviewer's scripts; do not edit or delete them.
  `.remedy-wt/f282-r3-worker/`    YOURS for logs and scripts. All three are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, `cd <dir> && git ...`, and
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
   `feature/f282-findings-paydown-v2`, and `git log --oneline -1` must read `59fa1bd8`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f282-r3-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f282-r3-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.diff | 12 | 6461 | 99417883121d3bd7b48ebbe6baa8401d61db9be7fad087e41203d2118c05f628 |
| decisions.diff | 28 | 2167 | 2bd7b1f1057ed961c90b951fe49170cdcebd032533e3a39103bdd46067a5370f |
| plan.md | 30 | 1122 | 275cdc933df06af8694ee6ebae6bc6bf7ff96113e61cb37279a9f055d6a63e03 |
| product.diff | 66 | 3984 | 6a8c45ee4e0cf6162871c04caba7351d723302cba3a6b9eb460d9a5ce953f047 |
| tests.diff | 65 | 3803 | 7eabfde0bb65e4106b69981352839c9afaf52b2bb6d19caf3dd685ddcbcb4550 |
| mutations.py | 62 | 2676 | e51b2fde46f42f4662b3a0c8bd0f2e85cbc67a327048005f89885e4f43650682 |

`plan.md` is a REWRITE of `.agent/plan.md`, copied whole. The `.diff` files go on with
`git apply`; the reviewer generated every one from a tree at `59fa1bd8` and applied all of
them, in the commit order below, to a fresh worktree at `59fa1bd8` with `git apply --check`
then `git apply`, every one at real exit code 0. `ledger.diff` appends two paragraphs to
`.agent/live_review.md` — the `Gate: F282 R2` entry and the `Done:` line of R-1041.
`product.diff` edits `apps/cli/commands/job.py` and `packages/orchestration/run_manifest.py`;
`tests.diff` edits `tests/orchestration/test_job_budgets.py` and
`tests/orchestration/test_predictive_budget.py`. `mutations.py` is a TOOL for G5: it is run,
never applied.

BUNDLE — the commits are C1a, C1b, C2, C3, C4 and C5, in this order.

C1a — copy this block and the bookkeeping payloads
  `.agent/authored/f282-r3-block.md` := this block, and one `.agent/authored/f282-r3-<name>`
  for each of ledger.diff, decisions.diff and plan.md, keeping each payload's own file name.
  All by `shutil.copyfile`.
  Subject: `F282 R3 C1a: copy round 3 block and bookkeeping payloads into .agent/authored/`
  Its insertions are this block's line count plus 70. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the product payloads
  `.agent/authored/f282-r3-<name>` for each of product.diff, tests.diff and mutations.py,
  by `shutil.copyfile`.
  Subject: `F282 R3 C1b: copy round 3 product payloads into .agent/authored/`
  Expected insertions: 193.

C2 — THE BOOKKEEPING, in this order:
   1. `git apply` ledger.diff     → `.agent/live_review.md`
   2. `git apply` decisions.diff  → `.agent/decisions.md`
   3. rewrite `.agent/plan.md` := plan.md
  Subject: `F282 R3 C2: book round 2, resolve R-1041 and record DECISION F282 D3`
  Expected insertions by `git show --numstat`: 20 decisions.md, 4 live_review.md, 6 plan.md.

C3 — THE PRODUCT: `git apply` product.diff.
  Subject: `F282 R3 C3: keep a recorded cost over an empty ledger, and let a deadline stop finalize`
  Expected by `git show --numstat`: 13 insertions and 9 deletions in `apps/cli/commands/job.py`,
  7 and 1 in `packages/orchestration/run_manifest.py`.

C4 — THE TESTS: `git apply` tests.diff.
  Subject: `F282 R3 C4: test the kept cost and the deadline stop, R-1040 and R-1005`
  Expected insertions: 27 in `test_job_budgets.py`, 16 in `test_predictive_budget.py`.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F282 R3 C5: rewrite handoff for round 3`
  Then `git push origin feature/f282-findings-paydown-v2` and report its real outcome. Do
  NOT create a pull request.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f282-r3-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `apps/cli/commands/job.py`, `packages/orchestration/run_manifest.py`,
   `tests/orchestration/test_job_budgets.py`, `tests/orchestration/test_predictive_budget.py`
   and `.agent/handoff.md`. Report the list you measure with
   `git diff --name-only 59fa1bd8 HEAD` after C5. Do NOT touch `.agent/prose_slips.md`,
   `.agent/candidates.md`, `.agent/operator_questions.md`, `.agent/context.md`, `README.md`
   or anything under `docs/`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch
   deletion, no force-push, no `git stash`.
6. Leave `.remedy-wt/job-129b3ad7206d4f8d`, `.remedy-wt/job-6a38b3203cca4928`,
   `.remedy-wt/job-e7268925db3a4831`, `.remedy-wt/job-e7a145761bf04f86`, the reviewer's
   `.remedy-wt/f282-r2-dry`, `.remedy-wt/f282-r2-sim`, `.remedy-wt/f282-r3-dry` and
   `.remedy-wt/f282-r3-sim`, their branches and every existing stash alone. The worktree G5
   adds goes under `.remedy-wt/`, is removed as that step's last action, and
   `git worktree list` is reported afterwards (finding R-0940).
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run
   and F282's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f282-r3-*` copy byte for
 byte with its source (the block copy against `.remedy-wt/f282-r3-block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE BOOKKEEPING AND THE PRODUCT — the sha256 of each file below, read with
 `git show <commit>:<path>` at the commit named, equals the reviewer's reading, which its
 simulation printed from a tree it built by applying these payloads at `59fa1bd8`:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/live_review.md | 396563 | c9fa23da07d1d1f073dab2feec319e5c09ab86e35e61887446307ac664cb8bd6 |
 | C2 | .agent/decisions.md | 1917838 | e1f9ba0508c70b11ca15a987407860f83d58b319593f191fc8db01b357aa1ab6 |
 | C2 | .agent/plan.md | 1122 | 275cdc933df06af8694ee6ebae6bc6bf7ff96113e61cb37279a9f055d6a63e03 |
 | C3 | apps/cli/commands/job.py | 100878 | 5bf304f1195d14dd2e7712a62fd052778e9f4e8aa53355db0f8b2f2cdd9675d7 |
 | C3 | packages/orchestration/run_manifest.py | 339525 | 74687303a118b03937172ef9153fcb3fdab4652e8dbc1ed2ca0302bb9d4c7950 |
 | C4 | tests/orchestration/test_job_budgets.py | 68482 | d28ddf04b792707c3e21b2659a13786de939ce86abddc29ecb96de0f57de2a5a |
 | C4 | tests/orchestration/test_predictive_budget.py | 53741 | 711c6615b419acfb53f2658bde1f56c303a288d00998c7477afbb1aae5eace9f |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `59fa1bd8` and at C2, with the set
 difference in both directions (the reviewer read 24 and 23, R-1041 the only id leaving and
 none arriving); and `git diff --name-only` between consecutive commits from C1b to C4,
 which must name exactly the paths each commit lists.

G3 THE LINTER ON THIS BLOCK — at C4, in the primary checkout:
 `python3 -m apps.cli.main integrity block .remedy-wt/f282-r3-block.md`, real exit code 0,
 every item `[OK]`. Report the whole output.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_job_budgets.py tests/orchestration/test_predictive_budget.py tests/orchestration/test_budget_guard.py tests/orchestration/test_budget_stop_integration.py tests/orchestration/test_job_digest.py tests/orchestration/test_f018_authority_integration.py tests/cli/test_job_refusal_envelope.py tests/cli/test_job_budget_set.py tests/orchestration/test_material_input_fields.py tests/orchestration/test_run_manifest.py tests/orchestration/test_run_manifest_ledger_semantics.py tests/orchestration/test_run_manifest_episode_graph.py tests/orchestration/test_run_manifest_call_task_binding.py tests/orchestration/test_run_manifest_prework_resume.py tests/orchestration/test_run_manifest_task_lifecycle_binding.py tests/orchestration/test_run_manifest_zero_call_expectations.py tests/orchestration/test_integrity_gate.py tests/test_ble001_ratchet.py tests/orchestration/test_live_review_rotation.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path, serially, inside a disposable
 worktree carrying C2 to C4 and read `1025 passed, 2 skipped` at real exit code 0; a skip may
 pass in the primary checkout. (Every `tests/orchestration/test_run_manifest*.py` file, not
 only the ones named, read `1300 passed` together with the budget suites in the reviewer's
 dry run.) Then `python3 -m ruff check apps/cli/commands/job.py
 packages/orchestration/run_manifest.py tests/orchestration/test_job_budgets.py
 tests/orchestration/test_predictive_budget.py`, real exit code 0, and
 `python3 -m apps.cli.main integrity check --json`, all six checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f282-r3-mut <C4>`, then
 `python3 -B .remedy-wt/f282-r3-payloads/mutations.py .remedy-wt/f282-r3-mut` and report its
 whole output. The reviewer read, over the same script against a tree byte-identical to C4:
 control_before `220 passed` at exit 0;
 m1 (an empty ledger answer replacing the cost) 1 failed at exit 1;
 m2 (the decoder unable to read its own `Z`) 3 failed at exit 1;
 m3 (the builder binding the raw budgets) 2 failed at exit 1;
 r1 (`apps/cli/commands/job.py` at `59fa1bd8`) 1 failed at exit 1;
 r2 (`packages/orchestration/run_manifest.py` at `59fa1bd8`) 3 failed at exit 1;
 control_after `220 passed` at exit 0; every `restored byte-identical` line True. Then
 `git worktree remove --force .remedy-wt/f282-r3-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 7`, which must show C5, C4, C3, C2, C1b, C1a and `59fa1bd8` in that
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
section reads SESSION 1 of feature F282, round 3, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 3, then T006 to T008 — R-1007, then R-1016, R-1027 and R-1035, then R-0999. State
the open-findings count, 23, and the operator-questions count, 0.

STEP F282 R4 — BOOK ROUND 3 AND LAND T006 AND T007: R-1007's KEPT VERDICT AND THE TIMEOUT STATUS

GOAL
Book round 3's PASS and the resolutions of R-1040 and R-1005, record DECISION F282 D4, and land
two slices: a budget-stopped task keeps the reviewer's last verdict and the self-use runner's
default call ceiling clears what its loop can spend (T006, R-1007), and a provider call that timed
out ends `provider_timeout` rather than `provider_unavailable` (T007, R-1016, R-1027, R-1035).

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f282-r4-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f282-r4-scratch/`   The reviewer's scripts; do not edit or delete them.
  `.remedy-wt/f282-r4-worker/`    YOURS for logs and scripts. All three are gitignored.

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
   `feature/f282-findings-paydown-v2`, and `git log --oneline -1` must read `a5715ae8`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f282-r4-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f282-r4-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.diff | 14 | 8254 | 0276319ed4136bc9b516edf3ebff4eb1ecc6bac42943d39da4fd9375930d05b5 |
| decisions.diff | 37 | 3085 | e23ca07d12a403a44f02b8079b7d3bbe09d59950e5b21c4fc8e31c2d9cc91962 |
| plan.md | 30 | 1120 | 77bfe2995455430e3de3cf31bcb1c3055c2007c76e3616f231fe581ac1c2bfe9 |
| product.diff | 141 | 8098 | c21bae32bb1a8e524da22693cc297bf10f870babc40e3e955cdaa5c5ab982f78 |
| tests.diff | 90 | 5085 | 4433779a2f2990e049c7cbf524212e2dbd96cd124ac06e528ec87a03e5bf9e04 |
| mutations.py | 77 | 3402 | ac7d7772a957e69f713a2fb0e89316f33c2c1d05c41ee823d529af74162e34c6 |

`plan.md` is a REWRITE of `.agent/plan.md`, copied whole. The `.diff` files go on with
`git apply`; the reviewer generated every one from a tree at `a5715ae8` and applied all of
them, in the commit order below, to a fresh worktree at `a5715ae8` with `git apply --check`
then `git apply`, every one at real exit code 0. `ledger.diff` appends three paragraphs to
`.agent/live_review.md` — the `Gate: F282 R3` entry and the `Done:` lines of R-1040 and
R-1005. `product.diff` edits five files under `packages/orchestration/`: `pingpong_loop.py`,
`pingpong_job.py`, `self_use_runner.py`, `run_manifest.py` and `failure_postmortem.py`.
`tests.diff` edits `tests/orchestration/test_predictive_budget.py` and
`tests/orchestration/test_self_use_runner.py`. `mutations.py` is a TOOL for G5: it is run,
never applied.

BUNDLE — the commits are C1a, C1b, C2, C3, C4 and C5, in this order.

C1a — copy this block and the bookkeeping payloads
  `.agent/authored/f282-r4-block.md` := this block, and one `.agent/authored/f282-r4-<name>`
  for each of ledger.diff, decisions.diff and plan.md, keeping each payload's own file name.
  All by `shutil.copyfile`.
  Subject: `F282 R4 C1a: copy round 4 block and bookkeeping payloads into .agent/authored/`
  Its insertions are this block's line count plus 81. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the product payloads
  `.agent/authored/f282-r4-<name>` for each of product.diff, tests.diff and mutations.py,
  by `shutil.copyfile`.
  Subject: `F282 R4 C1b: copy round 4 product payloads into .agent/authored/`
  Expected insertions: 308.

C2 — THE BOOKKEEPING, in this order:
   1. `git apply` ledger.diff     → `.agent/live_review.md`
   2. `git apply` decisions.diff  → `.agent/decisions.md`
   3. rewrite `.agent/plan.md` := plan.md
  Subject: `F282 R4 C2: book round 3, resolve R-1040 and R-1005 and record DECISION F282 D4`
  Expected insertions by `git show --numstat`: 29 decisions.md, 6 live_review.md, 8 plan.md.

C3 — THE PRODUCT: `git apply` product.diff.
  Subject: `F282 R4 C3: record a provider timeout as one, and keep a stopped task's verdict`
  Expected by `git show --numstat`: 1/0 failure_postmortem.py, 11/4 pingpong_job.py,
  15/3 pingpong_loop.py, 1/0 run_manifest.py, 15/2 self_use_runner.py (insertions/deletions).

C4 — THE TESTS: `git apply` tests.diff.
  Subject: `F282 R4 C4: test the timeout status, the kept verdict and the call ceiling`
  Expected insertions: 53 in `test_predictive_budget.py`, 15 in `test_self_use_runner.py`.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F282 R4 C5: rewrite handoff for round 4`
  Then `git push origin feature/f282-findings-paydown-v2` and report its real outcome. Do
  NOT create a pull request.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f282-r4-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, the five product files
   named above, the two test files named above and `.agent/handoff.md`. Report the list you
   measure with `git diff --name-only a5715ae8 HEAD` after C5. Do NOT touch
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md`,
   `.agent/context.md`, `README.md` or anything under `docs/`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch
   deletion, no force-push, no `git stash`.
6. Leave `.remedy-wt/job-129b3ad7206d4f8d`, `.remedy-wt/job-6a38b3203cca4928`,
   `.remedy-wt/job-e7268925db3a4831`, `.remedy-wt/job-e7a145761bf04f86`, the reviewer's
   `.remedy-wt/f282-r4-dry` and `.remedy-wt/f282-r4-sim`, their branches and every existing
   stash alone. The worktree G5
   adds goes under `.remedy-wt/`, is removed as that step's last action, and
   `git worktree list` is reported afterwards (finding R-0940).
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run
   and F282's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f282-r4-*` copy byte for
 byte with its source (the block copy against `.remedy-wt/f282-r4-block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE BOOKKEEPING AND THE PRODUCT — the sha256 of each file below, read with
 `git show <commit>:<path>` at the commit named, equals the reviewer's reading, which its
 simulation printed from a tree it built by applying these payloads at `a5715ae8`:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/live_review.md | 400952 | 287376fec350faf71787ebbcf1023e958b8bdf6d895d07b8f8444a1cea77c919 |
 | C2 | .agent/decisions.md | 1920363 | 666e060e71a68d8f121ba8af835bc64b43e58da9e026b9711387d515867d0c9d |
 | C2 | .agent/plan.md | 1120 | 77bfe2995455430e3de3cf31bcb1c3055c2007c76e3616f231fe581ac1c2bfe9 |
 | C3 | packages/orchestration/pingpong_loop.py | 226964 | eaa0f5629ccdbf0d0ab753d870ac2ce6ef947c14769958ed19e08dd8f109bf88 |
 | C3 | packages/orchestration/pingpong_job.py | 201022 | c050ab7e6863294a38983b7372f924b6578d607ef3280dac2e8eaea8cd7a930b |
 | C3 | packages/orchestration/self_use_runner.py | 20929 | ec1a97c4fc2ae000f135438188d308af8d4e414d1be033e6ca869b0e2c62959d |
 | C3 | packages/orchestration/run_manifest.py | 339619 | 49f912964180279cb16b17947a708b90e0b4f25989f13edb683f4d1132d76ffb |
 | C3 | packages/orchestration/failure_postmortem.py | 41466 | cacb7e1d8959918f7318964f9e405e0faa170fc17a29c639c8bd7e9a563b9cdd |
 | C4 | tests/orchestration/test_predictive_budget.py | 56834 | 7c2cc2665c2b2f6cec7c3bbc4c91b0436dc2b32edf5c5f3418dd0db955ac2973 |
 | C4 | tests/orchestration/test_self_use_runner.py | 27681 | cd857e88b06992b185fc3ddecade71690c1ce9f9c22346fc0693539ee4d56c50 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `a5715ae8` and at C2, with the set
 difference in both directions (the reviewer read 23 and 21, R-1005 and R-1040 leaving and
 none arriving); and `git diff --name-only` between consecutive commits from C1b to C4,
 which must name exactly the paths each commit lists.

G3 THE LINTER ON THIS BLOCK — at C4, in the primary checkout:
 `python3 -m apps.cli.main integrity block .remedy-wt/f282-r4-block.md`, real exit code 0,
 every item `[OK]`. Report the whole output.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_predictive_budget.py tests/orchestration/test_self_use_runner.py tests/orchestration/test_claude_cli_failure_detail.py tests/orchestration/test_pingpong.py tests/orchestration/test_failure_postmortem.py tests/orchestration/test_failure_wiring.py tests/orchestration/test_worktree_cleanup_paths.py tests/orchestration/test_orchestrator_loop.py tests/orchestration/test_run_manifest_ledger_semantics.py tests/orchestration/test_job_task_runner.py tests/orchestration/test_self_use_findings.py tests/orchestration/test_budget_stop_integration.py tests/orchestration/test_job_digest.py tests/orchestration/test_applicator_fences.py tests/orchestration/test_project_summary.py tests/orchestration/test_event_replay.py tests/orchestration/test_stop_reasons.py tests/orchestration/test_integrity_gate.py tests/test_ble001_ratchet.py tests/orchestration/test_live_review_rotation.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path, serially, inside a disposable
 worktree carrying the round's edits and read `1261 passed, 2 skipped` at real exit code 0; a
 skip may pass in the primary checkout. Then `python3 -m ruff check` over the five product
 files and the two test files, real exit code 0, and
 `python3 -m apps.cli.main integrity check --json`, all six checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f282-r4-mut <C4>`, then
 `python3 -B .remedy-wt/f282-r4-payloads/mutations.py .remedy-wt/f282-r4-mut` and report its
 whole output. The reviewer read, over the same script against a tree byte-identical to C4:
 control_before `133 passed` at exit 0;
 m1 (a timeout still read as unavailable) 1 failed at exit 1;
 m2 (a timeout recording no detail) 1 failed at exit 1;
 m3 (the stop keeping only the last round's verdict) 1 failed at exit 1;
 m4 (the default ceiling tying the loop) 1 failed at exit 1;
 m5 (a passed ceiling raised too) 3 failed at exit 1;
 r1, r2 and r3 (`pingpong_loop.py`, `pingpong_job.py` and `self_use_runner.py` each at
 `a5715ae8`) 1, 2 and 1 failed, each at exit 1;
 control_after `133 passed` at exit 0; every `restored byte-identical` line True. The
 script's filter also prints one source line of a test that contains the word "failed"; it
 is part of the output, not a result. Then `git worktree remove --force
 .remedy-wt/f282-r4-mut`, `git worktree prune`, and report `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 7`, which must show C5, C4, C3, C2, C1b, C1a and `a5715ae8` in that
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
section reads SESSION 1 of feature F282, round 4, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 4, then T008 to T011 — R-0999, R-1015, R-1034 and R-1000. State the open-findings
count, 21, and the operator-questions count, 0.

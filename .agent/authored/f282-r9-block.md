STEP F282 R9 — BOOK ROUND 8 AND LAND T018: R-1028's SCAN MATCHES A PATH AS A PATH, R-0950's REAL RUNS FREEZE THE CHECKOUT

GOAL
Book round 8's PASS and the resolution of R-0866, record DECISION F282 D9, and land T018's two
repairs: the runtime cleanup scans in `tests/runtimes/runtime_cleanup.py` match a temporary path
only as a path, so worker gw1 no longer counts gw10's live runtimes as its own survivors
(R-1028), and `TestTwoRealRunsShareLogicalIdentity` freezes Remedy's own checkout identity, so a
neighbour writing into the shared checkout cannot change the hash it compares (R-0950).

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f282-r9-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f282-r9-scratch/`   The reviewer's scripts; do not edit or delete them.
  `.remedy-wt/f282-r9-worker/`    YOURS for logs and scripts. All three are gitignored.

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
   `feature/f282-findings-paydown-v2`, and `git log --oneline -1` must read `5c43004f`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f282-r9-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f282-r9-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.diff | 12 | 5621 | bd9b99d84ffca388cb6347373ad9fe63035f9005b71df792b44ffd5ac5812a14 |
| decisions.diff | 44 | 3698 | 5b5bdf886258f03180564048d9df324ecde9199a3175c6cc961279fc5dba337e |
| plan.md | 30 | 1148 | cebf3383e2d5a74ced8c9ab98ac3082eae332266f5dae566c80fc485557ebefd |
| product.diff | 100 | 4726 | 41a4695d0d47e1974b7d62d6594ee36f70fa2aa3788e4ff65fe8bd8bb2cbefd1 |
| tests.diff | 95 | 3157 | d7f1ab0a63781a4a6ea455458c05c81e822b9bd591845b0c038865dbd83f8190 |
| mutations.py | 63 | 2832 | 36b968bb6799f1346c05a1e42ecaa2b170880289c1a3e18705229e574ec7928e |

`plan.md` is a REWRITE of `.agent/plan.md`, copied whole. The `.diff` files go on with
`git apply`; the reviewer generated every one from a tree at `5c43004f` and applied all of
them, in the commit order below, to a fresh worktree at `5c43004f` with `git apply --check`
then `git apply`, every one at real exit code 0. `ledger.diff` appends two paragraphs to
`.agent/live_review.md` — the `Gate: F282 R8` entry and the `Done:` line of R-0866.
`product.diff` edits `tests/runtimes/runtime_cleanup.py` and
`tests/orchestration/test_run_manifest_logical_identity.py`; it is named product because it is
the repair, though both paths are test harness. `tests.diff` creates the NEW FILE at
`tests/runtimes/test_runtime_cleanup_scope.py`. `mutations.py` is a TOOL for G5: it is run,
never applied.

BUNDLE — the commits are C1a, C1b, C2, C3, C4 and C5, in this order.

C1a — copy this block and the bookkeeping payloads
  `.agent/authored/f282-r9-block.md` := this block, and one `.agent/authored/f282-r9-<name>`
  for each of ledger.diff, decisions.diff and plan.md, keeping each payload's own file name.
  All by `shutil.copyfile`.
  Subject: `F282 R9 C1a: copy round 9 block and bookkeeping payloads into .agent/authored/`
  Its insertions are this block's line count plus 86. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the product and test payloads: `.agent/authored/f282-r9-product.diff`,
  `.agent/authored/f282-r9-tests.diff` and `.agent/authored/f282-r9-mutations.py`, by
  `shutil.copyfile`.
  Subject: `F282 R9 C1b: copy round 9 product and test payloads into .agent/authored/`
  Expected insertions: 258.

C2 — THE BOOKKEEPING, in this order:
   1. `git apply` ledger.diff     → `.agent/live_review.md`
   2. `git apply` decisions.diff  → `.agent/decisions.md`
   3. rewrite `.agent/plan.md` := plan.md
  Subject: `F282 R9 C2: book round 8, resolve R-0866 and record DECISION F282 D9`
  Expected by `git show --numstat` (insertions/deletions): 36/0 decisions.md,
  4/0 live_review.md, 10/11 plan.md.

C3 — THE REPAIR: `git apply` product.diff.
  Subject: `F282 R9 C3: match a temporary path as a path and freeze the checkout under real runs, R-1028 and R-0950`
  Expected (insertions/deletions): 33/0 test_run_manifest_logical_identity.py,
  17/3 runtime_cleanup.py.

C4 — THE TESTS: `git apply` tests.diff, then `git add` the new file.
  Subject: `F282 R9 C4: pin the cleanup scans to their own worker, R-1028`
  Expected (insertions/deletions): 89/0 test_runtime_cleanup_scope.py.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F282 R9 C5: rewrite handoff for round 9`
  Then `git push origin feature/f282-findings-paydown-v2` and report its real outcome. Do
  NOT create a pull request.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f282-r9-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, the two product-diff
   paths and the one test path named above, and `.agent/handoff.md`. Report the list you
   measure with `git diff --name-only 5c43004f HEAD` after C5. Do NOT touch
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md`,
   `.agent/context.md`, `README.md` or anything under `docs/roadmap/`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch
   deletion, no force-push, no `git stash`.
6. Leave `.remedy-wt/job-129b3ad7206d4f8d`, `.remedy-wt/job-6a38b3203cca4928`,
   `.remedy-wt/job-e7268925db3a4831`, `.remedy-wt/job-e7a145761bf04f86`, the reviewer's
   `.remedy-wt/f282-r9-dry` and `.remedy-wt/f282-r9-sim`, their branches and every existing
   stash alone. The worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last
   action, and `git worktree list` is reported afterwards (finding R-0940).
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run
   and F282's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f282-r9-*` copy byte for
 byte with its source (the block copy against `.remedy-wt/f282-r9-block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE BOOKKEEPING AND THE REPAIR — the sha256 of each file below, read with
 `git show <commit>:<path>` at the commit named, equals the reviewer's reading, which its
 simulation printed from a tree it built by applying these payloads at `5c43004f`:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/live_review.md | 425229 | 9d00783c64d38ba671a11cc8d333388e235bb3d2991425fa23de065dbd32c19d |
 | C2 | .agent/decisions.md | 1932265 | 5d2f6a3494c0ac1e0e1c6b0688e21648a74297a5caec48effc53d3a754ce8fdc |
 | C2 | .agent/plan.md | 1148 | cebf3383e2d5a74ced8c9ab98ac3082eae332266f5dae566c80fc485557ebefd |
 | C3 | tests/runtimes/runtime_cleanup.py | 9576 | b87c08f90f37265c9bd5a1687724d58a745d9eeea235ef9b928f7c34975b8500 |
 | C3 | tests/orchestration/test_run_manifest_logical_identity.py | 7408 | 990a5425aae5840c01359251a4a0239172530e63364b58745be8ef8bdc7c9d68 |
 | C4 | tests/runtimes/test_runtime_cleanup_scope.py | 2835 | 19ef6cf2594791ccd1c8629e90599508686ed0fb7b04e6d3b52dc91cdfbf3b63 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `5c43004f` and at C2, with the set
 difference in both directions (the reviewer read 8 and 7, R-0866 leaving and none
 arriving); and `git diff --name-only` between consecutive commits from C1b to C4, which must
 name exactly the paths each commit lists.

G3 THE LINTER ON THIS BLOCK — at C4, in the primary checkout:
 `python3 -m apps.cli.main integrity block .remedy-wt/f282-r9-block.md`, real exit code 0,
 every item `[OK]`. Report the whole output.

G4 THE TESTS, THE FLAKE AND THE LINT — in the primary checkout at C4. First SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/runtimes/test_runtime_cleanup_scope.py tests/orchestration/test_run_manifest_logical_identity.py tests/runtimes/test_supervisor_portability.py tests/runtimes/test_runtime_cli_process_boundary.py tests/cli/test_job_rerun_manifest.py tests/docs/ tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection serially inside its simulation tree at the C4 it built
 and read `590 passed, 1 skipped` at real exit code 0 in about 200 seconds. Then the flake's
 own reproduction, THREE separate runs, each reported with its summary line and exit code:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -n auto -rfE tests/orchestration/test_run_manifest_logical_identity.py tests/runtimes/test_supervisor_portability.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 At `5c43004f` the reviewer read `109 passed, 1 error` at exit 1 in four runs of four; over its
 simulation's C4 it read `110 passed` at exit 0 in three runs of three. Report every run as it
 comes; a red run is reported with its ERROR or FAILED line and is a STOP under constraint 4.
 Then `python3 -m ruff check` over `tests/runtimes/runtime_cleanup.py`,
 `tests/runtimes/test_runtime_cleanup_scope.py` and
 `tests/orchestration/test_run_manifest_logical_identity.py`, real exit code 0; and
 `python3 -m apps.cli.main integrity check --json`, all six checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f282-r9-mut <C4>`, then
 `python3 -B .remedy-wt/f282-r9-payloads/mutations.py .remedy-wt/f282-r9-mut` and report its
 whole output. The reviewer read, over the same script against a tree byte-identical to C4:
 control_before `19 passed` at exit 0;
 m1 (a root matches as a substring again) 5 failed at exit 1;
 m2 (the working-directory branch matches as a substring again) 1 failed at exit 1;
 m3 (the real runs see the live checkout again) 1 failed at exit 1;
 r1 (`runtime_cleanup.py` at `5c43004f`) `1 error` at exit 2, the new test module unable to
 import `names_path`;
 control_after `19 passed` at exit 0; every `restored byte-identical` line True. Then
 `git worktree remove --force .remedy-wt/f282-r9-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 7`, which must show C5, C4, C3, C2, C1b, C1a and `5c43004f` in
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
section reads SESSION 2 of feature F282, round 9, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 9, then the closure sequence. State the open-findings count, 7, and the
operator-questions count, 0.

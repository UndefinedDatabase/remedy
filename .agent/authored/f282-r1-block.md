STEP F282 R1 — CLAIM F282, WRITE ITS SLICE LIST, RESOLVE R-0984 AND LAND T001, R-0998's VERDICT READER

GOAL
No pull request is open; `main` is at `b8fa02ba` and F282 is the next unchecked line. Cut its
branch, claim it, re-head the live review record (carrying F263's round 9 verdict), write the
slice list into the feature file, book R-0984's resolution and DECISION F282 D1, and land T001:
`_check_live_review_verdict` in `packages/orchestration/integrity_gate.py` reads the ledger's
last `Gate:` record through `latest_gate_verdict`, with its tests and red proofs.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f282-r1-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f282-r1-scratch/`   The reviewer's scripts; do not edit or delete them.
  `.remedy-wt/f282-r1-worker/`    YOURS for logs and scripts. All three are gitignored.

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
2. `git status --porcelain` must be empty, `git branch --show-current` must read `main`,
   and `git log --oneline -1` must read `b8fa02ba`. Report all three. Then
   `git checkout -b feature/f282-findings-paydown-v2` and report the branch. Do NOT pull:
   the Open PR Gate found nothing open and `main` is already at the merge commit.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f282-r1-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f282-r1-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.diff | 63 | 12713 | 1b1f5c8f79bb73e788e29e68f8a2224a5308c9b9ad46355b3b20cac2add462ad |
| status.diff | 13 | 1016 | c1059294a5639f05e1702508c890b76dbfaf60028216763ed551fadfdb5b3010 |
| feature.diff | 58 | 4336 | 8181d7d545e8e7465f341a69665d2525ce1a11e4c44c8ca5b789dbd4b65df527 |
| plan.md | 32 | 1319 | 5ddde8adadfeec3d03b159c6152a67e26e83492e10a6aace5dad2bbab0e5b94a |
| context.md | 44 | 2046 | 4e947e0f9f4755bb986487d36e986b657cfe9c7a9d444825325aa735ec62f48c |
| decisions.diff | 38 | 3203 | 29f3aa34d19c2d88c38044c8f5c312bec8388286ab12b874c25ad7df2c5bd55f |
| product.diff | 83 | 4334 | 34225b7a26ee24d37d05d57f2b7a104a0ec0b21f388882294304817d8962ba0d |
| tests.diff | 88 | 4711 | 36611b508d45fc8da4835831d78fa497368c0fe324c99962c6085e10bc93e8ae |
| mutations.py | 66 | 2654 | 484c6ce44c281be39585332a2891f46e68a28529b525b8dcf0efcad02cb7bc43 |

`plan.md` and `context.md` are REWRITES of `.agent/plan.md` and `.agent/context.md`, each
copied whole. The `.diff` files go on with `git apply`; the reviewer generated every one from a
tree at `b8fa02ba` and applied all of them, in the commit order below, to a fresh worktree at
`b8fa02ba` with `git apply --check` then `git apply`, every one at real exit code 0.
`ledger.diff` edits `.agent/live_review.md` in two places — the re-head at the top and one
`Done: R-0984` paragraph appended at the end. `mutations.py` is a TOOL for G5: it is run,
never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C2, C3, C4, C5 and C6, in this order.

C1a — copy this block and the ledger-side payloads
  `.agent/authored/f282-r1-block.md` := this block, and one `.agent/authored/f282-r1-<name>`
  for each of ledger.diff, status.diff, feature.diff and decisions.diff, keeping each
  payload's own file name. All by `shutil.copyfile`.
  Subject: `F282 R1 C1a: copy round 1 block and ledger payloads into .agent/authored/`
  Its insertions are this block's line count plus 172. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the remaining payloads
  `.agent/authored/f282-r1-<name>` for each of plan.md, context.md, product.diff,
  tests.diff and mutations.py, by `shutil.copyfile`.
  Subject: `F282 R1 C1b: copy round 1 state and product payloads into .agent/authored/`
  Expected insertions: 313.

C2 — THE CLAIM, in this order:
   1. `git apply` ledger.diff   → `.agent/live_review.md`
   2. `git apply` status.diff   → `docs/roadmap/STATUS.md`
   3. `git apply` feature.diff  → `docs/roadmap/features/T2_F282.md`
   4. rewrite `.agent/plan.md` := plan.md
   5. rewrite `.agent/context.md` := context.md
  Subject: `F282 R1 C2: claim F282, write its slice list and re-head the live review record`
  Expected insertions by `git show --numstat`: 32 context.md, 27 live_review.md, 19 plan.md,
  1 STATUS.md, 40 T2_F282.md.

C3 — THE DECISION
  `git apply` decisions.diff → `.agent/decisions.md`.
  Subject: `F282 R1 C3: record DECISION F282 D1, the slice list and R-0998's reading`
  Expected insertions: 30.

C4 — THE PRODUCT: `git apply` product.diff → `packages/orchestration/integrity_gate.py`.
  Subject: `F282 R1 C4: read the integrity check's verdict from the last Gate record`
  Expected insertions: 28 (28 deletions).

C5 — THE TESTS: `git apply` tests.diff → `tests/orchestration/test_integrity_gate.py`.
  Subject: `F282 R1 C5: test the verdict reader against Gate records, R-0998`
  Expected insertions: 77.

C6 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F282 R1 C6: rewrite handoff for round 1`
  Then `git push -u origin feature/f282-findings-paydown-v2`. Do NOT create a pull
  request: the branch opens one at F282's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f282-r1-*` copies,
   `.agent/live_review.md`, `docs/roadmap/STATUS.md`, `docs/roadmap/features/T2_F282.md`,
   `.agent/plan.md`, `.agent/context.md`, `.agent/decisions.md`,
   `packages/orchestration/integrity_gate.py`, `tests/orchestration/test_integrity_gate.py`
   and `.agent/handoff.md`. Report the list you measure with
   `git diff --name-only b8fa02ba HEAD` after C6. Do NOT touch `.agent/prose_slips.md`,
   `.agent/candidates.md`, `.agent/operator_questions.md` or `README.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main` after the
   branch is cut, no branch deletion, no force-push, no `git stash`.
6. Leave `.remedy-wt/job-129b3ad7206d4f8d`, `.remedy-wt/job-6a38b3203cca4928`,
   `.remedy-wt/job-e7268925db3a4831`, `.remedy-wt/job-e7a145761bf04f86`, the reviewer's
   `.remedy-wt/f282-r1-dry` and `.remedy-wt/f282-r1-sim`, their branches and every existing
   stash alone. The worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last
   action, and `git worktree list` is reported afterwards (finding R-0940).
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run
   and F282's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C6 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f282-r1-*` copy byte for
 byte with its source (the block copy against `.remedy-wt/f282-r1-block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE BOOKKEEPING — the sha256 of each file below, read with `git show <commit>:<path>` at
 the commit named, equals the reviewer's reading, which its simulation printed from a tree it
 built by applying these payloads at `b8fa02ba`:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/live_review.md | 384366 | b9fd940b0a6384d9b803f36b09303885063a22cc7e6c0a059643e4fb28f3f149 |
 | C2 | docs/roadmap/STATUS.md | 48067 | 303e18ef3b70f6186be9d99e19782f97d0d3ea4b26e0f2e99d81f30bc70fc5c7 |
 | C2 | docs/roadmap/features/T2_F282.md | 6989 | e0a2352c5e37dc9a28d4e8fcdcb39ef4852182927b9b4e465cb9dcc987d3a691 |
 | C2 | .agent/plan.md | 1319 | 5ddde8adadfeec3d03b159c6152a67e26e83492e10a6aace5dad2bbab0e5b94a |
 | C2 | .agent/context.md | 2046 | 4e947e0f9f4755bb986487d36e986b657cfe9c7a9d444825325aa735ec62f48c |
 | C3 | .agent/decisions.md | 1914552 | 25a4977802996c36b34abe173de60ec132533bbc9def762a213d1fc1b14711a6 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `b8fa02ba` and at C2, with the set
 difference in both directions (the reviewer read 30 and 29, `R-0984` the only id leaving and
 none arriving); F282's STATUS line at C2 read back in full, which must read
 `- [~] F282 — Findings paydown v2`; and `git diff --name-only <C1b> <C2>` and
 `git diff --name-only <C2> <C3>`, which must name exactly the paths C2 and C3 list.

G3 THE PRODUCT — the sha256 of each file below, read with `git show <commit>:<path>`, equals
 the reviewer's simulated reading:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C4 | packages/orchestration/integrity_gate.py | 17588 | 83c33bacb0e118f2bdbabeeacdb6ea3fbf66f964dea03db2bef13ecfe939d28f |
 | C5 | tests/orchestration/test_integrity_gate.py | 19215 | 918feffaee449ee1e2206e04c20afc89091b7784d6820f38fc67008ad167c878 |
 Also `git diff --name-only <C3> <C4>` and `<C4> <C5>`, which must name exactly the path C4
 and the path C5 list.

G4 THE TESTS — in the primary checkout at C5, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_integrity_gate.py tests/orchestration/test_job_fulfillment.py tests/orchestration/test_development_artifact_boundary.py tests/test_ble001_ratchet.py tests/orchestration/test_final_audit_evidence.py tests/orchestration/test_live_review_rotation.py tests/docs/ tests/orchestration/test_roadmap_index.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path, serially, inside a disposable
 worktree carrying C2 to C5 and read `580 passed, 2 skipped` at real exit code 0; the primary
 checkout carries the UI toolchain a worktree lacks, so a skip may pass there. Report what you
 read. Then `python3 -m ruff check packages/orchestration/integrity_gate.py
 tests/orchestration/test_integrity_gate.py`, real exit code 0, and
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0, with `live_review_verdict` reading the message `last Gate verdict PASS`.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f282-r1-mut <C5>`, then
 `python3 -B .remedy-wt/f282-r1-payloads/mutations.py .remedy-wt/f282-r1-mut` and report its
 whole output. The script asserts each FROM occurs exactly once, applies it, runs
 `tests/orchestration/test_integrity_gate.py` under `python3 -B`, restores the bytes, and runs
 an unmutated control first and last. The reviewer read, over the same script against its own
 tree carrying C2 to C5:
 control_before `31 passed` at exit 0;
 m1 (a complete context never checked) 3 failed at exit 1;
 m2 (every verdict counted a pass) 3 failed at exit 1;
 m3 (an unreadable ledger reader answering PASS) 1 failed at exit 1;
 m4 (a missing Gate record answering PASS) 1 failed at exit 1;
 control_after `31 passed` at exit 0; every `restored byte-identical` line True.
 The reviewer also ran C5's test file against `integrity_gate.py` at `b8fa02ba`, the OLD
 reader, and read 6 failed, 25 passed: every new test red, no old one. Then
 `git worktree remove --force .remedy-wt/f282-r1-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C6: `git status --porcelain`, which must be empty;
 `git log --oneline -n 8`, which must show C6, C5, C4, C3, C2, C1b, C1a and `b8fa02ba` in
 that order; `git worktree list`, which must show the primary checkout and exactly the
 worktrees constraint 6 names; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be
 EMPTY. These readings go in your reply, since C6 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F282, round 1, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 1, then T002's remaining evidence resolutions with T003, R-1041 in
`packages/orchestration/block_lint.py`. State the open set this round leaves by distinct
id — the base's 30 less R-0984, so 29 — and the operator-questions count, 0.

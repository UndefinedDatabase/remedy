STEP F263 R1 — CLAIM F263 AND LAND T001's FOUNDATION: the last known state and the human change record

GOAL
Pull request 267 is merged; `main` is at `54a23101` and F263 is the next unchecked line. Cut
its branch, claim it, re-head the live review record, record DECISION F263 D1, and land the
first half of T001: `packages/orchestration/human_change.py`, the target checkout's last known
state recorded on every git job behind its own checkpoint ref, and the human change record,
certified into the job's evidence BEFORE any re-base, with the tests and their red proofs.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

WHY THIS IS FIRST
T2_F263.md's Orchestrator brief: T001 is where the evidence shape is decided, settled before
either caller exists. DECISION F263 D1 (the decisions.diff payload) states the shape: one tree
object of the target checkout as the last known state, a sealed JSON record beside its diff,
one record per transition, and an `absorb` that writes the record and only then calls the
re-base step it is given, catching nothing. This round ships no re-base.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f263-r1-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f263-r1-scratch/`   The reviewer's scripts; do not edit or delete them.
  `.remedy-wt/f263-r1-worker/`    YOURS for logs and scripts. All three are gitignored.

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
   and `git log --oneline -1` must read `54a23101`. Report all three. Then
   `git checkout -b feature/f263-human-change-absorption` and report the branch. Do NOT
   pull: the Open PR Gate ran before you and `main` is already at the merge commit.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f263-r1-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f263-r1-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| status.diff | 13 | 527 | dd1fc7c78d8475b7bb0ee5d0b9d22523b6483f5581e37204fa17b2b9e6240233 |
| rehead.diff | 50 | 5681 | e1ad10a8d712dead547777cce61906bdccbc2ccea1719a8d168dfc78d3c7fe2c |
| plan.md | 34 | 1463 | 950c6d0cac5f01b3d044c3b0b42ce563aa140f7da99996f1245c62c4b92b3c39 |
| context.md | 45 | 2166 | 7de6b47f63e030961043ab0210c5a90f739d5b800add2c49e093320dd1e5ac10 |
| decisions.diff | 50 | 3839 | 7e0212b41c3c659c882a3aedd81efcd4dc306f001a74b75bd297a21e13ddbee5 |
| product.diff | 106 | 5611 | ae031318faae54498aa5b102c47d9caa6c286127991e37aa38120a163a8d84e6 |
| human_change.py | 255 | 9853 | 09a885ea94200cae771cf754d4ac4d50d3fb5e8b4d2f2c233a59de0c470ce8aa |
| test_human_change.py | 206 | 9046 | e51f21d1d4664e4e45f6eb5ffe895fd7734a8070cdab58b16ceabad57c464ebd |
| mutations.py | 84 | 3191 | a78734cae866a522c274e3a71b483ab0cfea630febd49faf7b33576ecfd83e83 |

`plan.md` and `context.md` are REWRITES of `.agent/plan.md` and `.agent/context.md`.
`human_change.py` is a NEW FILE at `packages/orchestration/human_change.py` and
`test_human_change.py` a NEW FILE at `tests/orchestration/test_human_change.py`, each copied
whole. The `.diff` files go on with `git apply`; the reviewer generated every one from a tree
at `54a23101` and applied all of them, in the commit order below, to a fresh worktree at
`54a23101` with `git apply --check` then `git apply`, every one at real exit code 0.
`product.diff` edits `packages/orchestration/worktrees.py`,
`packages/orchestration/pingpong_job.py` and
`tests/orchestration/import_reachability_allowlist.txt`. `mutations.py` is a TOOL for G5: it
is run, never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C1c, C2, C3, C4, C5 and C6, in this order.

C1a — copy this block and the bookkeeping payloads
  `.agent/authored/f263-r1-block.md` := this block, and one
  `.agent/authored/f263-r1-<name>` for each of status.diff, rehead.diff, plan.md,
  context.md and decisions.diff, keeping each payload's own file name. All by
  `shutil.copyfile`.
  Subject: `F263 R1 C1a: copy round 1 block and bookkeeping payloads into .agent/authored/`
  Its insertions are this block's line count plus 192. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the product payloads
  `.agent/authored/f263-r1-<name>` for each of product.diff, human_change.py and
  mutations.py, by `shutil.copyfile`.
  Subject: `F263 R1 C1b: copy round 1 product payloads into .agent/authored/`
  Expected insertions: 445.

C1c — copy the test payload
  `.agent/authored/f263-r1-test_human_change.py`, by `shutil.copyfile`.
  Subject: `F263 R1 C1c: copy round 1 test payload into .agent/authored/`
  Expected insertions: 206.

C2 — THE CLAIM, in this order:
   1. `git apply` rehead.diff  → `.agent/live_review.md`
   2. `git apply` status.diff  → `docs/roadmap/STATUS.md`
   3. rewrite `.agent/plan.md` := plan.md
   4. rewrite `.agent/context.md` := context.md
  Subject: `F263 R1 C2: claim F263 and re-head the live review record`
  Expected insertions by `git show --numstat`: 15 context.md, 17 live_review.md, 21 plan.md,
  1 STATUS.md.

C3 — THE DECISION
  `git apply` decisions.diff → `.agent/decisions.md`.
  Subject: `F263 R1 C3: record DECISION F263 D1, the human change record's shape`
  Expected insertions: 42.

C4 — THE PRODUCT: copy human_change.py to `packages/orchestration/human_change.py`, then
  `git apply` product.diff, then `git add` all four paths — an untracked module fails
  `integrity check`'s `relevant_untracked`.
  Subject: `F263 R1 C4: record the target's last known state and certify human changes`
  Expected insertions: 255 human_change.py, 12 pingpong_job.py, 12 worktrees.py,
  1 import_reachability_allowlist.txt.

C5 — THE TESTS: copy test_human_change.py to `tests/orchestration/test_human_change.py`
  and `git add` it.
  Subject: `F263 R1 C5: test the human change record and the job's last known state`
  Expected insertions: 206.

C6 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F263 R1 C6: rewrite handoff for round 1`
  Then `git push -u origin feature/f263-human-change-absorption`. Do NOT create a pull
  request: the branch opens one at F263's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f263-r1-*` copies,
   `.agent/live_review.md`, `docs/roadmap/STATUS.md`, `.agent/plan.md`, `.agent/context.md`,
   `.agent/decisions.md`, `packages/orchestration/human_change.py`,
   `packages/orchestration/worktrees.py`, `packages/orchestration/pingpong_job.py`,
   `tests/orchestration/import_reachability_allowlist.txt`,
   `tests/orchestration/test_human_change.py` and `.agent/handoff.md`. Report the list you
   measure with `git diff --name-only 54a23101 HEAD` after C6. Do NOT touch
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md`,
   `README.md` or `docs/roadmap/features/T2_F263.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main` after the
   branch is cut, no branch deletion, no force-push, no `git stash`.
6. Leave `.remedy-wt/job-129b3ad7206d4f8d`, `.remedy-wt/job-e7268925db3a4831`,
   `.remedy-wt/job-e7a145761bf04f86`, their branches and every existing stash alone. The
   worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last action, and
   `git worktree list` is reported afterwards (finding R-0940).
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run
   and F263's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C6 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f263-r1-*` copy byte for
 byte with its source (the block copy against `.remedy-wt/f263-r1-block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE BOOKKEEPING — the sha256 of each file below, read with `git show <commit>:<path>` at
 the commit named, equals the reviewer's reading, which its simulation printed from a tree it
 built by applying these payloads at `54a23101`:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/live_review.md | 371115 | 91e52c57179dbaa45202395a19e579bed218cdde5d02f4dccc00e4daa0a8f52b |
 | C2 | docs/roadmap/STATUS.md | 47565 | a20a6b0f0c2c1455deec99960a699950467ed09948024583f023eedc8b6806ea |
 | C2 | .agent/plan.md | 1463 | 950c6d0cac5f01b3d044c3b0b42ce563aa140f7da99996f1245c62c4b92b3c39 |
 | C2 | .agent/context.md | 2166 | 7de6b47f63e030961043ab0210c5a90f739d5b800add2c49e093320dd1e5ac10 |
 | C3 | .agent/decisions.md | 1878109 | 5dc8da8b9d3dc6942673204b6ce0541c0b6d19439b2eea763545397c6bfcbc2b |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `54a23101` and at C2, with the set
 difference in both directions (the reviewer read 28 and 28, both differences empty); F263's
 STATUS line at C2 read back in full, which must read `- [~] F263 — Human-change absorption
 (absorb)`; and `git diff --name-only <C1c> <C2>` and `git diff --name-only <C2> <C3>`, which
 must name exactly the paths C2 and C3 list.

G3 THE PRODUCT — at C5, the sha256 of each file below, read with `git show <C5>:<path>`,
 equals the reviewer's simulated reading:
 | path | bytes | sha256 |
 |---|---|---|
 | packages/orchestration/human_change.py | 9853 | 09a885ea94200cae771cf754d4ac4d50d3fb5e8b4d2f2c233a59de0c470ce8aa |
 | packages/orchestration/worktrees.py | 31800 | ffc40789051c932e170f77630742330b65818ee63874c69d1481cfa3af760928 |
 | packages/orchestration/pingpong_job.py | 195753 | 37ae4d72c83aa6421c724d0fc98843dc76e8be65386b17e2cc7ea67fc31ddb19 |
 | tests/orchestration/import_reachability_allowlist.txt | 9903 | 0f629c137afdfb54e9bfd0f386d6906e159dd60e3eff8e347511d66ab9b56382 |
 | tests/orchestration/test_human_change.py | 9046 | e51f21d1d4664e4e45f6eb5ffe895fd7734a8070cdab58b16ceabad57c464ebd |
 Also `git diff --name-only <C3> <C4>` and `<C4> <C5>`, which must name exactly the paths C4
 and C5 list.

G4 THE TESTS — in the primary checkout at C5, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_human_change.py tests/orchestration/test_job_worktree_integrity.py tests/orchestration/test_job_worktree_handoff.py tests/orchestration/test_job_worktree_integration.py tests/orchestration/test_worktrees.py tests/orchestration/test_job_plan.py tests/orchestration/test_job_administrative_fields.py tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/docs/ tests/orchestration/test_roadmap_index.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path, serially, inside a disposable
 worktree carrying C2 to C5 and read `693 passed, 2 skipped` at real exit code 0; the primary
 checkout carries the UI toolchain a worktree lacks, so a skip may pass there. Report what you
 read. Then `python3 -m ruff check packages/orchestration/human_change.py
 packages/orchestration/worktrees.py packages/orchestration/pingpong_job.py
 tests/orchestration/test_human_change.py`, real exit code 0, and
 `python3 -m apps.cli.main integrity check --json`, which must read all five checks `pass`
 at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f263-r1-mut <C5>`, then
 `python3 -B .remedy-wt/f263-r1-payloads/mutations.py .remedy-wt/f263-r1-mut` and report its
 whole output. The script asserts each FROM occurs exactly once, applies it, runs
 `tests/orchestration/test_human_change.py` under `python3 -B`, restores the bytes, and runs
 an unmutated control first and last. The reviewer read, over the same script against its own
 tree carrying C2 to C5:
 control_before `17 passed` at exit 0;
 m1 (the re-base called before the record is written) 2 failed at exit 1;
 m2 (`git add -u` in place of `git add -A`, so untracked files escape) 5 failed at exit 1;
 m3 (tool-cache noise counted as the human's) 1 failed at exit 1;
 m4 (the diff digest never checked) 1 failed at exit 1;
 m5 (the record seal never checked) 1 failed at exit 1;
 m6 (an existing record rewritten) 1 failed at exit 1;
 m7 (the job records no last known state) 2 failed at exit 1;
 m8 (the import drops the last known state) 1 failed at exit 1;
 control_after `17 passed` at exit 0; every `restored byte-identical` line True.
 Then `git worktree remove --force .remedy-wt/f263-r1-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C6: `git status --porcelain`, which must be empty;
 `git log --oneline -n 9`, which must show C6, C5, C4, C3, C2, C1c, C1b, C1a and `54a23101`
 in that order; `git worktree list`, which must show the primary checkout and the
 `.remedy-wt/job-*` worktrees constraint 6 names, and nothing else; the push's real outcome;
 and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be
 EMPTY. These readings go in your reply, since C6 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F263, round 1, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 1, then T001's second half — the human change record joining the job's exported
evidence and its verification. State the open-findings count, 28, and the operator-questions
count, 0.

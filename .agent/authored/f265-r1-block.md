STEP F265 R1 — CLAIM F265 AND LAND T001's SUBSTANCE: a sealed lesson per Run, from its real diff

GOAL
Pull request 271 is merged; `main` is at `0236e3c3` and F265 is the next unchecked line. Cut
its branch, claim it, re-head the live review record, register finding R-1046, record DECISION
F265 D1 and operator question Q1, and land T001's substance: `packages/orchestration/lessons.py`,
which writes one sealed lesson per completed Run from that Run's own `result.diff`, billed as
role `teacher` inside the teacher's own budget pot per job, and the hook in `run_job` that writes
one after every applied task while the new `teacher.lessons` key is on, with tests and red proofs.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge.

WHY THIS IS FIRST
T5_F265.md's Orchestrator brief: T001 is the substance and the budget risk, so the lesson's shape
is settled before any UI exists. DECISION F265 D1 (in claim.diff) fixes it: a sealed record
beside the Run's diff, the whole diff or no call, constructs grounded in the diff's added lines,
a per-job pot read from the ledger, and lessons off unless `teacher.lessons` is on. The event
stream, a read-only route and `remedy do`'s mission path are next round's work.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f265-r1-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f265-r1-scratch/`   The reviewer's scripts; do not edit or delete them.
  `.remedy-wt/f265-r1-worker/`    YOURS for logs and scripts. All three are gitignored.

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
   `git status --porcelain` must be empty, `git branch --show-current` must read `main`, and
   `git log --oneline -1` must read `0236e3c3`. Report all three. Then
   `git checkout -b feature/f265-teacher-learning-ui` and report the branch. Do NOT pull: the
   Open PR Gate ran before you and `main` is already at the merge commit.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f265-r1-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f265-r1-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| claim.diff | 179 | 19828 | e64c5ce628acebd69e9ea8f415353d3848191a632b818a39eaef420facd90d78 |
| plan.md | 37 | 1508 | d3c22982e12c023db35f3903205825c4922a04f7d2caeb135ebc8d911c49d40d |
| context.md | 49 | 2380 | 93335fabd1b7fe9c72e7724840ec2f59ea290784acf4946db8fa6a36de0f9fb9 |
| product.diff | 119 | 7288 | 0937fd7cba208ffe6dea5d55c5a37f6e08a39e1e3d602f36ef07434ffe168aca |
| mutations.py | 101 | 3623 | 7372e0f45eada65d2b785153c664963d7ffaba83ccf29a9edc3396ff0a4d120c |
| lessons.py | 360 | 17032 | 8a3c60e89c13c7fc3b78f2a04cf452a6e7117c2c5d89029868e5e5e5f1fa3324 |
| test_lessons.py | 391 | 16372 | ad4fca0bcfc036f6598c922938ec41fb91578ed43733406c64c6ac7d9696e1bf |

`plan.md` and `context.md` are REWRITES of `.agent/plan.md` and `.agent/context.md`.
`lessons.py` is a NEW FILE at `packages/orchestration/lessons.py` and `test_lessons.py` a NEW
FILE at `tests/orchestration/test_lessons.py`, each copied whole. The `.diff` files go on with
`git apply`; the reviewer generated both from a tree at `0236e3c3` and applied them, in the
commit order below, to a fresh worktree at `0236e3c3` with `git apply --check` then `git apply`,
every one at real exit code 0. `claim.diff` edits `.agent/live_review.md` (the re-head, and
R-1046 appended at the end), `docs/roadmap/STATUS.md`, `.agent/decisions.md` (DECISION F265 D1
appended) and `.agent/operator_questions.md` (Q1 in place of the empty line). `product.diff`
edits `packages/orchestration/pingpong_job.py`, `packages/orchestration/config.py`,
`docs/guides/environment.md` (regenerated from the registry) and
`tests/orchestration/import_reachability_allowlist.txt`. `mutations.py` is a TOOL for G5: it is
run, never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C2, C3, C4 and C5, in this order.

C1a — copy this block and the state payloads
  `.agent/authored/f265-r1-block.md` := this block, and `.agent/authored/f265-r1-plan.md` and
  `.agent/authored/f265-r1-context.md` := plan.md and context.md. All by `shutil.copyfile`.
  Subject: `F265 R1 C1a: copy round 1 block and state payloads into .agent/authored/`
  Its insertions are this block's line count plus 86. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C1b — copy the two diffs and the mutation tool
  `.agent/authored/f265-r1-<name>` for each of claim.diff, product.diff and mutations.py.
  Subject: `F265 R1 C1b: copy round 1 diffs and mutation tool into .agent/authored/`
  Expected insertions: 399.

C1c — copy the new product module
  `.agent/authored/f265-r1-lessons.py` := lessons.py.
  Subject: `F265 R1 C1c: copy round 1 product module into .agent/authored/`
  Expected insertions: 360.

C1d — copy the test payload
  `.agent/authored/f265-r1-test_lessons.py` := test_lessons.py.
  Subject: `F265 R1 C1d: copy round 1 test payload into .agent/authored/`
  Expected insertions: 391.

C2 — THE CLAIM AND ITS RECORDS, in this order:
   1. `git apply` claim.diff
   2. rewrite `.agent/plan.md` := plan.md
   3. rewrite `.agent/context.md` := context.md
  Subject: `F265 R1 C2: claim F265, re-head the live review record, record D1, Q1 and R-1046`
  Expected insertions by `git show --numstat`: 22 context.md, 55 decisions.md, 29 live_review.md, 23 operator_questions.md, 24 plan.md, 1 STATUS.md.

C3 — THE PRODUCT: copy lessons.py to `packages/orchestration/lessons.py`, then `git apply`
  product.diff, then `git add` the new module and every path product.diff edits — an untracked
  module fails `integrity check`'s `relevant_untracked`.
  Subject: `F265 R1 C3: write a sealed lesson per completed Run from its real diff`
  Expected insertions: 3 environment.md, 32 config.py, 360 lessons.py, 32 pingpong_job.py, 1 import_reachability_allowlist.txt.

C4 — THE TESTS: copy test_lessons.py to `tests/orchestration/test_lessons.py` and `git add` it.
  Subject: `F265 R1 C4: test the lesson generator, its pot and its hook`
  Expected insertions: 391.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F265 R1 C5: rewrite handoff for round 1`
  Then `git push -u origin feature/f265-teacher-learning-ui`. Do NOT create a pull request: the
  branch opens one at F265's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f265-r1-*` copies,
   `.agent/live_review.md`, `docs/roadmap/STATUS.md`, `.agent/decisions.md`,
   `.agent/operator_questions.md`, `.agent/plan.md`, `.agent/context.md`,
   `packages/orchestration/lessons.py`, every path product.diff edits (listed under
   PAYLOADS), `tests/orchestration/test_lessons.py` and `.agent/handoff.md`. Report the list you
   measure with `git diff --name-only 0236e3c3 HEAD` after C5. Do NOT touch
   `.agent/prose_slips.md`, `.agent/candidates.md`, `README.md` or
   `docs/roadmap/features/T5_F265.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main` after the
   branch is cut, no branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees, their branches, the reviewer's worktrees
   `.remedy-wt/f265-r1-dry` and `.remedy-wt/f265-r1-sim`, and every existing stash alone. The
   worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last action, and
   `git worktree list` is reported afterwards (finding R-0940).
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F265's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f265-r1-*` copy byte for byte
 with its source (the block copy against `.remedy-wt/f265-r1-block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE CLAIM — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, which its simulation printed from a tree it built by applying these
 payloads at `0236e3c3`:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 304905 | 05107e03d54300713846df65ce8c03abbcf73ecfc359e4f4ad2abfeb3514e28f |
 | docs/roadmap/STATUS.md | 49035 | d791bef9ad1244b971fa521c0b86856e333d076bdf11c6bb843826b6826f7b3e |
 | .agent/decisions.md | 1960311 | b5743b7a2b4d351f5ca7cbaac0702657d332d768782d0c320a674203e6e87485 |
 | .agent/operator_questions.md | 2192 | 3f28314a50fa2ad56cde60573b78b46b899db55e04c892369083d409a133dbc7 |
 | .agent/plan.md | 1508 | d3c22982e12c023db35f3903205825c4922a04f7d2caeb135ebc8d911c49d40d |
 | .agent/context.md | 2380 | 93335fabd1b7fe9c72e7724840ec2f59ea290784acf4946db8fa6a36de0f9fb9 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `0236e3c3` and at C2, with the set
 difference in both directions (the reviewer read 3 at `0236e3c3` — R-0499, R-0950 and R-1008 —
 and 4 at C2, the difference being R-1046 alone); F265's STATUS line at C2 read back in full,
 which must read `- [~] F265 — Teacher learning UI v1 (post-task lessons)`; and
 `git diff --name-only <C1d> <C2>`, which must name exactly `.agent/context.md`,
 `.agent/decisions.md`, `.agent/live_review.md`, `.agent/operator_questions.md`,
 `.agent/plan.md` and `docs/roadmap/STATUS.md`.

G3 THE PRODUCT — at C4, the sha256 of each file below, read with `git show <C4>:<path>`,
 equals the reviewer's simulated reading:
 | path | bytes | sha256 |
 |---|---|---|
 | packages/orchestration/lessons.py | 17032 | 8a3c60e89c13c7fc3b78f2a04cf452a6e7117c2c5d89029868e5e5e5f1fa3324 |
 | packages/orchestration/pingpong_job.py | 202583 | 230ab34cdafee9cffff331fc4b62b8c2a479984a7691b1ec4214622c293b60e7 |
 | packages/orchestration/config.py | 63325 | 6180ae0c4f3f43ccdf292771aebb7f8fb38c17e5a4fe0b012c641c0e96dcf469 |
 | docs/guides/environment.md | 21327 | f8f139654b7e8c20cd7b77151101cc3752b9ed3293327268f4e32b5af4138fd5 |
 | tests/orchestration/import_reachability_allowlist.txt | 10022 | d9ffe3df68fb828a7fba7920af04a230549f6f36ccb97789531e21f219a89597 |
 | tests/orchestration/test_lessons.py | 16372 | ad4fca0bcfc036f6598c922938ec41fb91578ed43733406c64c6ac7d9696e1bf |
 Also `git diff --name-only <C2> <C3>` and `<C3> <C4>`, which must name exactly the paths C3
 and C4 list.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash .remedy-wt/f265-r1-scratch/g4.sh /home/decodeux/Repos/remedy
```
 The script runs one pytest selection (the lesson tests, the teacher, config and env-registry
 tests, the ratchet and guard tests the new handler and module reach, the reachability pair,
 `tests/orchestration/test_job_worktree_handoff.py`, `tests/docs/`, the state-file readers and
 `tests/cli/test_golden_path.py`), then `ruff check` over the touched Python files, then
 `python3 -m apps.cli.main integrity check --json`, each followed by its real exit code. The
 reviewer ran the same script inside its sim worktree carrying C1a to C4 and read
 `992 passed, 3 skipped` at pytest exit 0, ruff at exit 0, and all six integrity checks `pass` at
 `fail_count` 0 with `handlers=150`; the primary checkout carries the UI toolchain a worktree lacks, so a skip may pass
 there. Report the three readings you get: the pytest summary line and exit code, ruff's exit
 code, and whether all six integrity checks read `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f265-r1-mut <C4>`, then
 `python3 -B .remedy-wt/f265-r1-payloads/mutations.py .remedy-wt/f265-r1-mut` and report its
 whole output. The script asserts each FROM occurs exactly once, applies it, runs
 `tests/orchestration/test_lessons.py` under `python3 -B`, restores the bytes, and runs an
 unmutated control first and last. The reviewer read, over the same script against its sim tree
 carrying C1a to C4:
 control_before `29 passed` at exit 0;
 m1 (a construct no added line names is taught) 2 failed at exit 1;
 m2 (a removed line counts as added) 2 failed at exit 1;
 m3 (a stored lesson is generated again) 1 failed at exit 1;
 m4 (a spent pot still calls the model) 2 failed at exit 1;
 m5 (the pot counts every role's calls) 1 failed at exit 1;
 m6 (an oversize diff is sent) 1 failed at exit 1;
 m7 (a job with no ledger still calls the model) 1 failed at exit 1;
 m8 (the lesson's seal is never checked) 1 failed at exit 1;
 m9 (the ledger row is not keyed on the Run) 1 failed at exit 1;
 m10 (the hook ignores `teacher.lessons`) 1 failed at exit 1;
 m11 (the hook is never called from `run_job`) 1 failed at exit 1;
 m12 (the hook names the task as the Run) 2 failed at exit 1;
 control_after `29 passed` at exit 0; every `restored byte-identical` line True.
 Then `git worktree remove --force .remedy-wt/f265-r1-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 9`, which must show C5, C4, C3, C2, C1d, C1c, C1b, C1a and `0236e3c3` in
 that order; `git worktree list`, which must show the primary checkout, the `.remedy-wt/job-*`
 worktrees and the reviewer's worktrees constraint 6 names, and nothing else; the push's real
 outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which
 must be EMPTY. These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F265, round 1, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 1, then T001's reach — the lesson on the job's event stream, a read-only route listing a
job's lessons, and `remedy do`'s mission path proved end to end. State the open-findings count,
4, and the operator-questions count, 1.

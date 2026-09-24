STEP F015 R1 — CLAIM F015 AND LAND T001: the plan-editing backend, one transaction per edit

GOAL
Pull request 273 is merged; `main` is at `fce49ce0` and F015 is the next unchecked line. Cut its
branch, claim it, re-head the live review record with F267's closing verdict, record DECISION
F015 D1, and land T001: `packages/orchestration/plan_editing.py`, which applies one edit to a
job's stored task plan while its approval is open — edit, delete (dependents inherit the deleted
task's dependencies), reorder, merge, split and edit acceptance — revalidates it with the
planner's own checks, and writes the plan, its bumped version, its edit log and the regenerated
task list in one write of the job record, with tests and red proofs.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge.

WHY THIS IS FIRST
T5_F015.md's Orchestrator brief: T001's transactional atomicity and the delete-rewiring rule come
first, and the revision-conflict discipline is tested before any door exists. DECISION F015 D1
(in claim.diff) fixes the shape: one locked write of the job record, the planner's own schema,
DAG and deliverable checks, `_version` and the whole-list `_edits` log. T002 wires the write
channel and `remedy plan edit` and removes the module's `ALLOWED_UNWIRED` line.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f015-r1-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f015-r1-scratch/`   The reviewer's scripts; do not edit or delete them.
  `.remedy-wt/f015-r1-worker/`    YOURS for logs and scripts; create it if absent. All three are
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
   `git status --porcelain` must be empty, `git branch --show-current` must read `main`, and
   `git log --oneline -1` must read `fce49ce0`. Report all three. Then
   `git checkout -b feature/f015-interactive-plan-editing` and report the branch. Do NOT pull:
   the Open PR Gate ran before you and `main` is already at the merge commit.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f015-r1-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f015-r1-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| claim.diff | 143 | 14183 | 6aad52ebd60d60070ba3d7858498b2e91ee712f3ebd2a72dd7c3e89cd2af7c0e |
| plan.md | 35 | 1331 | 81a51c418677d3e81a3cd7d4e6499f585da3fe492b5c6703048115df23fbb431 |
| context.md | 38 | 1802 | f6f2e4e8ca52786781adf08b45b869db092a38f93a354e9ead2f0e2da1f8422b |
| product.diff | 13 | 865 | 894db85d19bbae15a344ddcc56b411c47d9fd5fa593bcb99eb33a2944d238f8e |
| mutations.py | 115 | 4250 | acb57eba98ac1ed1282172ed9d1e15260dea341287c118e9a1758305fce300c0 |
| plan_editing.py | 430 | 18064 | 0d55c5bac8231e452724701c786c90ff9a516c4fc986b202c1d92f7961f0b18f |
| test_plan_editing.py | 283 | 14738 | e47b2a1552fc7ea9778e55499e3c11d84431266f9d4d8f5ea468cac11d23a401 |

`plan.md` and `context.md` are REWRITES of `.agent/plan.md` and `.agent/context.md`.
`plan_editing.py` is a NEW FILE at `packages/orchestration/plan_editing.py` and
`test_plan_editing.py` a NEW FILE at `tests/orchestration/test_plan_editing.py`, each copied
whole. The `.diff` files go on with `git apply`; the reviewer generated both from a tree at
`fce49ce0` and applied them, in the commit order below, to a fresh detached worktree at
`fce49ce0` with `git apply --check` then `git apply`, every one at real exit code 0.
`claim.diff` edits `.agent/live_review.md` (the re-head), `docs/roadmap/STATUS.md` (F015's line
`[ ]` to `[~]`) and `.agent/decisions.md` (DECISION F015 D1 appended). `product.diff` edits
`tests/test_no_orphan_modules.py` (the backend's one `ALLOWED_UNWIRED` entry, D1 (8)).
`mutations.py` is a TOOL for G5: it is run, never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C2, C3, C4 and C5, in this order.

C1a — copy this block and the state payloads
  `.agent/authored/f015-r1-block.md` := this block, and `.agent/authored/f015-r1-plan.md` and
  `.agent/authored/f015-r1-context.md` := plan.md and context.md. All by `shutil.copyfile`.
  Subject: `F015 R1 C1a: copy round 1 block and state payloads into .agent/authored/`
  Its insertions are this block's line count plus 73. Report the number you measure
  and STOP rather than commit if it is 500 or more.

C1b — copy the two diffs and the mutation tool
  `.agent/authored/f015-r1-<name>` for each of claim.diff, product.diff and mutations.py.
  Subject: `F015 R1 C1b: copy round 1 diffs and mutation tool into .agent/authored/`
  Expected insertions: 271.

C1c — copy the new product module
  `.agent/authored/f015-r1-plan_editing.py` := plan_editing.py.
  Subject: `F015 R1 C1c: copy round 1 product module into .agent/authored/`
  Expected insertions: 430.

C1d — copy the test payload
  `.agent/authored/f015-r1-test_plan_editing.py` := test_plan_editing.py.
  Subject: `F015 R1 C1d: copy round 1 test payload into .agent/authored/`
  Expected insertions: 283.

C2 — THE CLAIM AND ITS RECORDS, in this order:
   1. `git apply` claim.diff
   2. rewrite `.agent/plan.md` := plan.md
   3. rewrite `.agent/context.md` := context.md
  Subject: `F015 R1 C2: claim F015, re-head the live review record, record D1`
  Expected insertions by `git show --numstat`: 14 context.md, 53 decisions.md, 27 live_review.md, 22 plan.md, 1 STATUS.md.

C3 — THE PRODUCT: copy plan_editing.py to `packages/orchestration/plan_editing.py`, then
  `git apply` product.diff, then `git add` the new module and `tests/test_no_orphan_modules.py`
  — an untracked module fails `integrity check`'s `relevant_untracked`.
  Subject: `F015 R1 C3: edit a stored task plan as one revalidated, versioned transaction`
  Expected insertions: 430 plan_editing.py, 2 test_no_orphan_modules.py.

C4 — THE TESTS: copy test_plan_editing.py to `tests/orchestration/test_plan_editing.py` and
  `git add` it.
  Subject: `F015 R1 C4: test every edit kind, the rewiring rule, the window and the log`
  Expected insertions: 283.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F015 R1 C5: rewrite handoff for round 1`
  Then `git push -u origin feature/f015-interactive-plan-editing`. Do NOT create a pull request:
  the branch opens one at F015's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f015-r1-*` copies,
   `.agent/live_review.md`, `docs/roadmap/STATUS.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `.agent/context.md`, `packages/orchestration/plan_editing.py`,
   `tests/test_no_orphan_modules.py`, `tests/orchestration/test_plan_editing.py` and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only fce49ce0 HEAD`
   after C5. Do NOT touch `.agent/prose_slips.md`, `.agent/candidates.md`,
   `.agent/operator_questions.md`, `README.md` or `docs/roadmap/features/T5_F015.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main` after the
   branch is cut, no branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees, their branches, the reviewer's worktrees
   `.remedy-wt/f015-r1-dry` and `.remedy-wt/f015-r1-sim`, the local branch `sim/f267-r1`, and
   every existing stash alone. The worktree G5 adds goes under `.remedy-wt/`, is removed as that
   step's last action, and `git worktree list` is reported afterwards (finding R-0940).
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F015's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f015-r1-*` copy byte for byte
 with its source (the block copy against `.remedy-wt/f015-r1-block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE CLAIM — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, which its simulation printed from a tree it built by applying these
 payloads at `fce49ce0`:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 291908 | 3ceb7b517423a8e4a7f986c2401f069551bac65991bee12690617cbf80d470ce |
 | docs/roadmap/STATUS.md | 49747 | cf15a8771e7db8c44d8aa31948f4a37a39f41e61b3bd2df78f41ddb21bdbe388 |
 | .agent/decisions.md | 1977833 | e2a3776b095be9973e3131ec9e5079c8111a352b42ed9721dcd13b1722f5b73b |
 | .agent/plan.md | 1331 | 81a51c418677d3e81a3cd7d4e6499f585da3fe492b5c6703048115df23fbb431 |
 | .agent/context.md | 1802 | f6f2e4e8ca52786781adf08b45b869db092a38f93a354e9ead2f0e2da1f8422b |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `fce49ce0` and at C2, with the set
 difference in both directions (the reviewer read 4 at both — R-0499, R-0950, R-1008 and
 R-1046 — and both differences empty); F015's STATUS line at C2 read back in full, which must
 read `- [~] F015 — Interactive plan editing`; and `git diff --name-only <C1d> <C2>`, which must
 name exactly `.agent/context.md`, `.agent/decisions.md`, `.agent/live_review.md`,
 `.agent/plan.md` and `docs/roadmap/STATUS.md`.

G3 THE PRODUCT — at C4, the sha256 of each file below, read with `git show <C4>:<path>`,
 equals the reviewer's simulated reading:
 | path | bytes | sha256 |
 |---|---|---|
 | packages/orchestration/plan_editing.py | 18064 | 0d55c5bac8231e452724701c786c90ff9a516c4fc986b202c1d92f7961f0b18f |
 | tests/test_no_orphan_modules.py | 16092 | 325cab3efa5f1feca2c97b80aa9c265ec02bf95a291e5f12621c431d96829b7b |
 | tests/orchestration/test_plan_editing.py | 14738 | e47b2a1552fc7ea9778e55499e3c11d84431266f9d4d8f5ea468cac11d23a401 |
 Also `git diff --name-only <C2> <C3>` and `<C3> <C4>`, which must name exactly the paths C3
 and C4 list.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash .remedy-wt/f015-r1-scratch/g4.sh /home/decodeux/Repos/remedy
```
 The script runs one pytest selection (the new tests; the granularity, plan, plan-schema,
 approval, deliverable, scheduler and mission-compiler tests the module reaches; the orphan,
 reachability, durable-write and BLE001 guards; `tests/docs/`, the roadmap index, the
 state-file readers, the ledger and block-lint tests and `tests/cli/test_golden_path.py`), then
 `ruff check` over the touched Python files, then `python3 -m apps.cli.main integrity check
 --json`, each followed by its real exit code. The reviewer ran the same script inside its sim
 worktree carrying C1a (without the block copy) to C4 and read `988 passed, 3 skipped` at pytest exit 0, ruff
 at exit 0, and all six integrity checks `pass` at `fail_count` 0 with `handlers=150`. The
 primary checkout carries the UI toolchain a worktree lacks, so a skip may pass there, and your
 tree carries the block copy the sim lacked, which a test parametrized over the saved blocks may
 count once more. Report the three readings you get: the pytest summary line and exit code,
 ruff's exit code, and whether all six integrity checks read `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f015-r1-mut <C4>`, then
 `python3 -B .remedy-wt/f015-r1-payloads/mutations.py .remedy-wt/f015-r1-mut` and report its
 whole output. The script asserts each FROM occurs exactly once, applies it, runs
 `tests/orchestration/test_plan_editing.py` under `python3 -B`, restores the bytes, and runs an
 unmutated control first and last. The reviewer read, over the same script against its sim tree
 carrying C1a to C4:
 control_before `36 passed` at exit 0;
 m1 (a deleted task's dependents lose its dependencies) 1 failed at exit 1;
 m2 (the edited plan skips the schema and DAG check) 14 failed at exit 1;
 m3 (the edited plan skips the deliverable check) 1 failed at exit 1;
 m4 (an approved plan is still editable) 1 failed at exit 1;
 m5 (a started job's plan is still editable) 2 failed at exit 1;
 m6 (a stale version is written) 1 failed at exit 1;
 m7 (the job's task list is not regenerated) 2 failed at exit 1;
 m8 (the log keeps only the last edit) 3 failed at exit 1;
 m9 (the version is not bumped) 5 failed at exit 1;
 m10 (the plan-edit lock is never taken) 1 failed at exit 1;
 m11 (a split's dependents wait for the chain's start) 1 failed at exit 1;
 m12 (a merge leaves dependents on a dropped task) 1 failed at exit 1;
 m13 (an edit that changes nothing is written) 1 failed at exit 1;
 m14 (the evidence export omits the log) 1 failed at exit 1;
 m15 (the replay never checks the logged result) 1 failed at exit 1;
 control_after `36 passed` at exit 0; every `restored byte-identical` line True (15 of them).
 Then `git worktree remove --force .remedy-wt/f015-r1-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 9`, which must show C5, C4, C3, C2, C1d, C1c, C1b, C1a and `fce49ce0` in
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
section reads SESSION 1 of feature F015, round 1, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 1, then T002 — the write-channel door for the six edit commands, the edit window closed
by the approval under the plan-edit lock, the race and stale-version tests, and `remedy plan
edit`. State the open-findings count, 4, and the operator-questions count, 1.

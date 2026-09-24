STEP F015 R2 — BOOK R1 AND LAND T002's FIRST HALF: the approval under the edit lock, and `job plan-*`

GOAL
Round 1 passed at `9bad6428`. Book its verdict, record DECISION F015 D2 and one prose slip, and
land T002's first half: `plan_editing.consume_plan_approval`, which consumes a plan approval
under the plan-edit lock against the record as it stands NOW, called by both approval doors so
an edit landing after a door loaded the job is approved rather than written over; and
`remedy job plan-show` with the six `job plan-*` edit commands, thin wrappers over `edit_plan`,
with tests and red proofs.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge.

WHY THIS IS NEXT
T5_F015.md orders T002: the edit window closed atomically by the approval, the race tested, and
CLI parity. DECISION F015 D2 (in records.diff) fixes the shape: the lock at both doors, the CLI
under the `job` group because `plan` is the retired roadmap word, 0-based criterion indexes, and
the exit codes. The write door's own plan-edit commands are the next round.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f015-r2-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f015-r2-scratch/`   The reviewer's scripts; do not edit or delete them.
  `.remedy-wt/f015-r2-worker/`    YOURS for logs and scripts; create it if absent. All three are
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
   `feature/f015-interactive-plan-editing`, and `git log --oneline -1` must read `9bad6428`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f015-r2-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f015-r2-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 72 | 12662 | 8600ce3b2c66f93e57997544df84d96c5ee338b487d24b62fedcbb49e33112bb |
| tests.diff | 138 | 7096 | 0466ba8cceac19b5041b016f557751316819a7fbccbc23baeb6b7fe165029e54 |
| mutations.py | 103 | 4133 | 3bf36e2d5bcbeb05da7a815f2da3d61f590e03497075c54ee087852d9b86ec31 |
| product.diff | 459 | 28542 | aacd3fe38b70a808fd53e43d7937b7348000a59af7eb928b017c6aead9aed7e5 |
| plan.md | 33 | 1221 | f21147e0c05e3bb822c186e87c1780fbb9e2f57dfdc4387ef31c0314561f2028 |
| context.md | 40 | 1953 | 2eb751ca96b52b4bc0346d4931fb0eff708e3ddd8f177095d3ebb06392efcaf6 |
| job_plan_cmd.py | 191 | 9114 | 8b1a66f961b7b97e8b2ddd3823adb298c0769d236ffaabca0de00d9caf4bb062 |
| test_job_plan_cmd.py | 204 | 9573 | 7d5137fe7535cbeb9533051e5139c78207f7e850a5e4c0a5ab2f461325ef8a91 |

`plan.md` and `context.md` are REWRITES of `.agent/plan.md` and `.agent/context.md`.
`job_plan_cmd.py` is a NEW FILE at `apps/cli/commands/job_plan_cmd.py` and `test_job_plan_cmd.py`
a NEW FILE at `tests/cli/test_job_plan_cmd.py`, each copied whole. The `.diff` files go on with
`git apply`; the reviewer generated all three from a tree at `9bad6428` and applied them, in the
commit order below, to a fresh detached worktree at `9bad6428` with `git apply --check` then
`git apply`, every one at real exit code 0. `records.diff` appends the `Gate: F015 R1 —` entry to
`.agent/live_review.md`, DECISION F015 D2 to `.agent/decisions.md` and one line to
`.agent/prose_slips.md`. `product.diff` edits the paths C3 lists other than `job_plan_cmd.py`.
`tests.diff` edits `tests/orchestration/test_plan_editing.py` and
`tests/ui_server/test_command_dispatch.py`. `mutations.py` is a TOOL for G5: it is run, never
applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C2, C3, C4 and C5, in this order.

C1a — copy this block and the state payloads
  `.agent/authored/f015-r2-block.md` := this block, and `.agent/authored/f015-r2-plan.md` and
  `.agent/authored/f015-r2-context.md` := plan.md and context.md. All by `shutil.copyfile`.
  Subject: `F015 R2 C1a: copy round 2 block and state payloads into .agent/authored/`
  Its insertions are this block's line count plus 73. Report the number you measure
  and STOP rather than commit if it is 500 or more.

C1b — copy the record and test diffs and the mutation tool
  `.agent/authored/f015-r2-<name>` for each of records.diff, tests.diff and mutations.py.
  Subject: `F015 R2 C1b: copy round 2 record and test diffs and mutation tool into .agent/authored/`
  Expected insertions: 313.

C1c — copy the product diff
  `.agent/authored/f015-r2-product.diff` := product.diff.
  Subject: `F015 R2 C1c: copy round 2 product diff into .agent/authored/`
  Expected insertions: 459.

C1d — copy the new CLI module and its tests
  `.agent/authored/f015-r2-<name>` for each of job_plan_cmd.py and test_job_plan_cmd.py.
  Subject: `F015 R2 C1d: copy round 2 new CLI module and its tests into .agent/authored/`
  Expected insertions: 191 f015-r2-job_plan_cmd.py, 204 f015-r2-test_job_plan_cmd.py.

C2 — THE RECORDS, in this order:
   1. `git apply` records.diff
   2. rewrite `.agent/plan.md` := plan.md
   3. rewrite `.agent/context.md` := context.md
  Subject: `F015 R2 C2: book round 1's PASS, record D2 and one prose slip`
  Expected insertions by `git show --numstat`: 3 context.md, 45 decisions.md, 2 live_review.md, 8 plan.md, 1 prose_slips.md.

C3 — THE PRODUCT: copy job_plan_cmd.py to `apps/cli/commands/job_plan_cmd.py`, then `git apply`
  product.diff, then `git add` the new module and every path product.diff edits — an untracked
  module fails `integrity check`'s `relevant_untracked`.
  Subject: `F015 R2 C3: consume the plan approval under the edit lock and add job plan-*`
  Expected insertions: 125 command_catalog.py, 2 __init__.py, 24 decision.py, 191 job_plan_cmd.py, 7 exit-codes.md, 1 vocabulary.md, 52 plan_editing.py, 19 ui_server.py, 2 import_reachability_allowlist.txt, 0 test_no_orphan_modules.py, 4 test_command_channel.py.

C4 — THE TESTS: copy test_job_plan_cmd.py to `tests/cli/test_job_plan_cmd.py`, `git apply`
  tests.diff, and `git add` the three test files.
  Subject: `F015 R2 C4: test the approval race at both doors and every job plan-* command`
  Expected insertions: 204 test_job_plan_cmd.py, 46 test_plan_editing.py, 66 test_command_dispatch.py.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F015 R2 C5: rewrite handoff for round 2`
  Then `git push origin feature/f015-interactive-plan-editing`. Do NOT create a pull request:
  the branch opens one at F015's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f015-r2-*` copies, the paths C2,
   C3 and C4 list, and `.agent/handoff.md`. Report the list you measure with
   `git diff --name-only 9bad6428 HEAD` after C5. Do NOT touch `.agent/candidates.md`,
   `.agent/operator_questions.md`, `README.md`, `docs/roadmap/` or any path not named here.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees, their branches, the reviewer's worktrees
   `.remedy-wt/f015-r1-dry`, `.remedy-wt/f015-r1-sim`, `.remedy-wt/f015-r2-dry` and
   `.remedy-wt/f015-r2-sim`, the local branch `sim/f267-r1`, and every existing stash alone.
   The worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last action, and
   `git worktree list` is reported afterwards (finding R-0940).
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F015's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f015-r2-*` copy byte for byte
 with its source (the block copy against `.remedy-wt/f015-r2-block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, which its simulation printed from a tree it built by applying these
 payloads at `9bad6428`:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 293981 | f835b62b59fdf136c1bdacac8083bf893bb2ddf6d035195e92ecec82653320bb |
 | .agent/decisions.md | 1981536 | 63b749f32768b98b046a1fc0c1523f63db252d41dd291e60a33ac052790e4ceb |
 | .agent/prose_slips.md | 366582 | f757bac33cd5945fd157d671b16c54e0545d4083dfe2ccda9a3a5e77236d406f |
 | .agent/plan.md | 1221 | f21147e0c05e3bb822c186e87c1780fbb9e2f57dfdc4387ef31c0314561f2028 |
 | .agent/context.md | 1953 | 2eb751ca96b52b4bc0346d4931fb0eff708e3ddd8f177095d3ebb06392efcaf6 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT, at `9bad6428` and at C2, with the set
 difference in both directions (the reviewer read 4 at both — R-0499, R-0950, R-1008 and
 R-1046 — and both differences empty); and the count of lines C2's diff adds to
 `.agent/live_review.md` that begin `Gate: F015 R1 — `, which must be 1.

G3 THE PRODUCT AND ITS TESTS — at C4, the sha256 of each file below, read with
 `git show <C4>:<path>`, equals the reviewer's simulated reading:
 | path | bytes | sha256 |
 |---|---|---|
 | apps/cli/command_catalog.py | 119466 | c0e0c363fca8de3cadb5b06390dea18248ea0dafb0c800ea4be19a8f529731ac |
 | apps/cli/commands/__init__.py | 2129 | 4bec55003a7305da73bcce99e880149d677ff1e19c3dda63ca22821946b744ce |
 | apps/cli/commands/decision.py | 24919 | bbdbf121694fb55fd02fd186dc49673b95491778a43d205dfb000dff4c7444ea |
 | apps/cli/commands/job_plan_cmd.py | 9114 | 8b1a66f961b7b97e8b2ddd3823adb298c0769d236ffaabca0de00d9caf4bb062 |
 | docs/guides/exit-codes.md | 4239 | c65a6185db395557f99b83a468bfad52bab2ae3a952614050b18e2aed22803d3 |
 | docs/system/vocabulary.md | 30738 | 3a2741aa920b8ee17d0b3fc34a3b7bd83bc5618a9692b3907e635046eb6897ee |
 | packages/orchestration/plan_editing.py | 20079 | b01ac07e52bdd60c2141ee3408342343b0655f73946d7de41b48cdb1a940686a |
 | packages/orchestration/ui_server.py | 154260 | 5f89ae5d2e40d6dc1400937f1a2940a1a09d6dc5eeaceee50118f4da6c20b1df |
 | tests/orchestration/import_reachability_allowlist.txt | 10089 | 62faecb08a703da5788b4c678492772c68c780a161b1c9274915db3849cdaf53 |
 | tests/test_no_orphan_modules.py | 15936 | 365a75ca49a8fa1d18eafb252c23535ea876af8532c851608179c3537f84d2ba |
 | tests/ui_server/test_command_channel.py | 94627 | b8deb14dc49cb58d0a212f287c1b6b317ff3e63c1c16d95e19680fda7f56e029 |
 | tests/cli/test_job_plan_cmd.py | 9573 | 7d5137fe7535cbeb9533051e5139c78207f7e850a5e4c0a5ab2f461325ef8a91 |
 | tests/orchestration/test_plan_editing.py | 17101 | 36601ee603ead7d255f31ffb338c285eefaff0c8456df86506c1cda37a3614d3 |
 | tests/ui_server/test_command_dispatch.py | 28815 | 8b8a3cd84ec4d8c6b284b3096bbaf50c738238760f5839c67627b921cbfa6352 |
 Also `git diff --name-only <C2> <C3>` and `<C3> <C4>`, which must name exactly the paths C3 and
 C4 list.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash .remedy-wt/f015-r2-scratch/g4.sh /home/decodeux/Repos/remedy
```
 The script runs one pytest selection (the plan-editing, CLI and door tests; the approval,
 catalog, exit-code, help and envelope tests the new commands reach; the decision-inbox and
 clarification tests; the orphan, reachability, durable-write and BLE001 guards; `tests/docs/`,
 the roadmap index, the state-file readers, the ledger and block-lint tests and
 `tests/cli/test_golden_path.py`), then `ruff check` over the touched Python files, then
 `python3 -m apps.cli.main integrity check --json`, each followed by its real exit code. The
 reviewer ran the same script inside its sim worktree carrying C1a (without the block copy) to C4
 and read `1483 passed, 2 skipped` at pytest exit 0, ruff at exit 0, and all six integrity checks `pass` at
 `fail_count` 0 with `handlers=157`. The primary checkout carries the UI toolchain a worktree
 lacks, so a skip may pass there, and your tree carries the block copy the sim lacked, which a
 test parametrized over the saved blocks may count once more. Report the three readings you get:
 the pytest summary line and exit code, ruff's exit code, and whether all six integrity checks
 read `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f015-r2-mut <C4>`, then
 `python3 -B .remedy-wt/f015-r2-payloads/mutations.py .remedy-wt/f015-r2-mut` and report its
 whole output. The script asserts each FROM occurs exactly once, applies it, runs the three test
 files it names under `python3 -B`, restores the bytes, and runs an unmutated control first and
 last. The reviewer read, over the same script against its sim tree carrying C1a to C4:
 control_before `81 passed` at exit 0;
 m1 (the door's own older copy is approved) 3 failed at exit 1;
 m2 (a closed approval is consumed again) 2 failed at exit 1;
 m3 (the CLI door bypasses the lock) 1 failed at exit 1;
 m4 (the write door bypasses the lock) 2 failed at exit 1;
 m5 (a not-ready refusal exits 1) 3 failed at exit 1;
 m6 (a usage refusal exits 1) 2 failed at exit 1;
 m7 (plan-show calls every plan editable) 1 failed at exit 1;
 m8 (plan-reorder reads no sequence) 1 failed at exit 1;
 m9 (plan-split-task hands over no groups) 2 failed at exit 1;
 m10 (`--band` is not the backend's field) 2 failed at exit 1;
 m11 (a missing `--plan-version` is not named) 1 failed at exit 1;
 control_after `81 passed` at exit 0; every `restored byte-identical` line True (11 of them).
 Then `git worktree remove --force .remedy-wt/f015-r2-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 9`, which must show C5, C4, C3, C2, C1d, C1c, C1b, C1a and `9bad6428` in
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
section reads SESSION 1 of feature F015, round 2, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 2, then T002's second half — the write door's six plan-edit commands, exposed and
dispatched through `edit_plan` with their argument checks, refusals and stale-version
conflicts. State the open-findings count, 4, and the operator-questions count, 1.

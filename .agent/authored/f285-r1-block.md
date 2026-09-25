STEP F285 R1 — CLAIM F285 AND LAND T001 AND T002: the self-use Acceptance asks for the repair alone (R-1058), and the self-use cost cap is derived from the dearest measured call (R-1057)

GOAL
Pull request 281 is merged; `main` is at `83d3bb95` and F285 is the next unchecked line. Cut its
branch, claim it, re-head the live review record, book F026's round 8 verdict, record DECISION
F285 D1 and write F285's slice list, then land T001, R-1058's repair: the generated self-use job
asks for the repair its finding names and tells the builder to leave `.agent/` alone, and
`describe_self_use_run_defects` names a pass whose reviewed work changed no path outside
`.agent/`; and T002, R-1057's repair: the self-use cost cap is 6.00, derived from the dearest
measured call, with an operator-questions entry for the raised spend. Red proofs for both.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f285-r1-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f285-r1/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f285-r1-drafts/`    READ-ONLY. The reviewer's drafts and builders.
  `.remedy-wt/f285-r1-dry/`       The reviewer's dry tree; do not touch it.
  `.remedy-wt/f285-r1-sim/`       The reviewer's simulated tree; do not touch it.
  `.remedy-wt/f285-r1-worker/`    YOURS for logs and scripts; create it if absent. All of these
                                  are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, `cd <dir> && git ...`, and multi-operation
one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe pytest.
Use `git -C <path>` rather than `cd`. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`). A heredoc containing a dollar-brace or a brace next to a quote is
refused: write such a script to a file under your own directory and run the file. Never run npm
or npx.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read `main`, and
   `git log --oneline -1` must read `83d3bb95`. Report all three. Then
   `git checkout -b feature/f285-findings-paydown-v4` and report the branch. Do NOT pull: the
   Open PR Gate ran before you and `main` is already at the merge commit.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f285-r1/block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f285-r1-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| claim.diff | 167 | 16877 | f095c14408968f698a63dc5ff9fe825b7a7a39bc4c04f77fa81e1d3c6e35605e |
| plan.md | 30 | 1159 | 7dabdb7911c5e51708d2c671ad519cfe847bd4a0526e9518f36c1416bde4b5de |
| context.md | 33 | 1366 | aa332a74318c443435bc3def307b77b9041b5f554f07f3be3ca5a3eec521f93d |
| t001.diff | 235 | 11424 | 6fcc14675a64dd073e07851688ddb9cf73ecc6cbbf166ac230df10ecae71439f |
| t002.diff | 201 | 13606 | ccc179ae65fa37bd2950ec2777828b58e34d58f27b9f25b40c3c99fc5633e8ea |
| mutations.py | 68 | 2958 | 260e14da6082685ec09cbdd3c4bca5d3d36ea91b6696d6bbc6b5e86130284450 |

`plan.md` and `context.md` are REWRITES of `.agent/plan.md` and `.agent/context.md`. The three
`.diff` payloads go on with `git apply`; the reviewer generated each with `git diff HEAD` from a
tree at `83d3bb95` into which it wrote the edits. `claim.diff` edits `.agent/live_review.md` (the
re-head, then F026's round 8 gate entry appended), `.agent/decisions.md` (DECISION F285 D1
appended), `docs/roadmap/STATUS.md` (F285's line `[ ]` to `[~]`) and
`docs/roadmap/features/T2_F285.md` (the slice list). `t001.diff` edits
`packages/orchestration/self_use_findings.py`, `packages/orchestration/self_use_generator.py`,
`tests/orchestration/test_self_use_findings.py` and `tests/orchestration/test_self_use_generator.py`.
`t002.diff` edits `.agent/operator_questions.md`, `docs/guides/environment.md`,
`docs/system/self-use-track-v1.md`, `packages/orchestration/config.py`,
`packages/orchestration/self_use_runner.py` and `tests/orchestration/test_self_use_runner.py`.
`mutations.py` is a TOOL for G4: it is run, never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C1c, C2, C3, C4 and C5, in this order.

C1a — copy this block and the claim payloads
  `.agent/authored/f285-r1-block.md` := this block, and `.agent/authored/f285-r1-claim.diff`,
  `.agent/authored/f285-r1-plan.md` and `.agent/authored/f285-r1-context.md` := claim.diff,
  plan.md and context.md. All by `shutil.copyfile`.
  Subject: `F285 R1 C1a: copy round 1 block and claim payloads into .agent/authored/`
  Expected insertions: 460 (this block's 230 lines plus 230 for the three payloads). Report the number you measure and STOP rather than commit if any
  commit of this round would reach 500 insertions.

C1b — copy the T001 payload
  `.agent/authored/f285-r1-t001.diff` := t001.diff.
  Subject: `F285 R1 C1b: copy round 1 T001 payload into .agent/authored/`
  Expected insertions: 235.

C1c — copy the T002 payload and the tool
  `.agent/authored/f285-r1-t002.diff` and `.agent/authored/f285-r1-mutations.py` := t002.diff and
  mutations.py.
  Subject: `F285 R1 C1c: copy round 1 T002 payload and mutation tool into .agent/authored/`
  Expected insertions: 269.

C2 — THE CLAIM AND ITS RECORDS, in this order:
   1. `git apply` claim.diff
   2. rewrite `.agent/plan.md` := plan.md
   3. rewrite `.agent/context.md` := context.md
  Subject: `F285 R1 C2: claim F285, re-head the live review record, book F026 R8, record D1`
  Expected insertions by `git show --numstat`: 11 .agent/context.md, 58 .agent/decisions.md, 23 .agent/live_review.md, 17 .agent/plan.md, 1 docs/roadmap/STATUS.md, 17 docs/roadmap/features/T2_F285.md.

C3 — T001, R-1058: `git apply` t001.diff.
  Subject: `F285 R1 C3: ask the self-use builder for the repair alone and name a pass confined to .agent/`
  Expected insertions: 37 packages/orchestration/self_use_findings.py, 14 packages/orchestration/self_use_generator.py, 63 tests/orchestration/test_self_use_findings.py, 41 tests/orchestration/test_self_use_generator.py.

C4 — T002, R-1057: `git apply` t002.diff.
  Subject: `F285 R1 C4: derive the self-use cost cap from the dearest measured call`
  Expected insertions: 25 .agent/operator_questions.md, 1 docs/guides/environment.md, 3 docs/system/self-use-track-v1.md, 1 packages/orchestration/config.py, 25 packages/orchestration/self_use_runner.py, 20 tests/orchestration/test_self_use_runner.py.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F285 R1 C5: rewrite handoff for round 1`
  Then `git push -u origin feature/f285-findings-paydown-v4`. Do NOT create a pull request:
  the branch opens one at F285's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f285-r1-*` copies, the four
   paths claim.diff edits, `.agent/plan.md`, `.agent/context.md`, the four paths t001.diff
   edits, the six paths t002.diff edits, and `.agent/handoff.md`. Report the list you measure
   with `git diff --name-only 83d3bb95 HEAD` after C5. Do NOT touch `.agent/prose_slips.md`,
   `.agent/candidates.md` or `README.md`.
4. You write no `Done:` line and no `Landed:` line: the reviewer authors R-1057's and R-1058's
   resolutions at the next gate.
5. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main` after the
   branch is cut, no branch deletion, no force-push, no `git stash`.
7. Leave every existing worktree under `.remedy-wt/` and its branch alone, and every existing
   stash. The worktree G4 adds goes under `.remedy-wt/`, is removed as that step's last action,
   and `git worktree list` is reported afterwards.
8. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F285's belongs to its closure. Run no self-use job and no `remedy` command that calls a
   provider: a self-use run spends real money and F285's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f285-r1-*` copy byte for byte
 with its source (the block copy against `.remedy-wt/f285-r1/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE CLAIM AND THE CODE — the sha256 of each file below, read with `git show <commit>:<path>`
 at the commit the table names, equals the reviewer's reading, which its builder printed from
 the simulated tree:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/context.md | 1366 | aa332a74318c443435bc3def307b77b9041b5f554f07f3be3ca5a3eec521f93d |
 | C2 | .agent/decisions.md | 2144886 | b541f6c5d36c940386101a8777cd790c13a8e706d4dd803418289c8ddbb28aa4 |
 | C2 | .agent/live_review.md | 307014 | 3dc070a5cf71e91da85737320a3f55640d4aaa5b23a624763d824ce2a6c8e8a5 |
 | C2 | .agent/plan.md | 1159 | 7dabdb7911c5e51708d2c671ad519cfe847bd4a0526e9518f36c1416bde4b5de |
 | C2 | docs/roadmap/STATUS.md | 52859 | b2a4d5f786d07799070eee29bd137c158e35aa63a8dd63549088969565284c28 |
 | C2 | docs/roadmap/features/T2_F285.md | 4593 | b1845fa8abc9882b423796bede0d46e03dcec980b848209303a7e1184422e5b1 |
 | C3 | packages/orchestration/self_use_findings.py | 6133 | 8b2b194de9f4d7c6536ee95be095b13122f1ce1678f02f53c86497aa0363947d |
 | C3 | packages/orchestration/self_use_generator.py | 20406 | 84ec6f57096b8f16979de349e4f441150b024022a2a19aa0d8b3db0a6b6bc5f6 |
 | C3 | tests/orchestration/test_self_use_findings.py | 8967 | 38b45f0eb613f5ed9d8dcdc92a354757a747e1e600fb61e96fc86062dd3fe038 |
 | C3 | tests/orchestration/test_self_use_generator.py | 27998 | 6e3966f0ebb13f4d058bf6a76e8a0516f1e6d809174ece5025bf5885e41a2ff5 |
 | C4 | .agent/operator_questions.md | 9169 | 3c62fe61c21655526f78de42e1c6cf0443a8448ba6979c79730c5956014ce404 |
 | C4 | docs/guides/environment.md | 21268 | 0da2f91362e07b21f81bf99ccd9e1fa1a18a0aaf5e55506e6cb3ae9b031a369a |
 | C4 | docs/system/self-use-track-v1.md | 8139 | ffe11d211ebdea0dc031d5157b9a2362f6400f968eb0b694f5b9139d03086a8c |
 | C4 | packages/orchestration/config.py | 63251 | f909e1cba0d613f64294a29bb12968a87cb5de7d191dc0029c85baab63ee41bd |
 | C4 | packages/orchestration/self_use_runner.py | 21902 | 321b660fb2371c29feac7288d1b377a462c9898e2691255d0cb936fcc22e0cf7 |
 | C4 | tests/orchestration/test_self_use_runner.py | 28503 | 33bca9f522fd4877e8acd2d54d4d3106da92de71542ba5c26c3dc5fbb41e9871 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `83d3bb95` and at C2 (the reviewer
 read R-1008, R-1055, R-1057, R-1058 and R-1064 at both); F285's STATUS line at C2 read back in
 full, which must read `- [~] F285 — Findings paydown v4`; and `git diff --name-only` between
 each pair of consecutive commits from C1c to C4, each of which must name exactly the paths that
 commit's entry above lists.

G3 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_self_use_findings.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_runner.py tests/orchestration/test_self_use_queue.py tests/orchestration/test_predictive_budget.py tests/orchestration/test_config.py tests/orchestration/test_role_config.py tests/orchestration/test_development_artifact_boundary.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection, serially, inside its simulated tree at C4 and read
 `900 passed, 1 skipped` at real exit code 0. Report every `SKIPPED` line the `-rs` summary prints; the
 reviewer's run printed exactly one, `SKIPPED [1] tests/test_agent_tooling.py:43`, the D12 quarantine. Then `python3 -m ruff check` over every `.py` file t001.diff and
 t002.diff edit, named one by one, which must read `All checks passed!`; and
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0.

G4 THE RED PROOFS — `git worktree add --detach .remedy-wt/f285-r1-mut <C4>`, then
 `python3 -B .remedy-wt/f285-r1-payloads/mutations.py
 /home/decodeux/Repos/remedy/.remedy-wt/f285-r1-mut` and report its whole output. The tool
 asserts each FROM occurs exactly once, restores the bytes after each run, and runs unmutated
 controls first and last. The reviewer read, over the same tool against its simulated tree at
 C4 (timings vary):
 control first: exit 0: 94 passed in 8.98s
 m1 (the ledger note is offered again): FROM occurs 1x in packages/orchestration/self_use_generator.py
 m1: exit 1: 2 failed, 92 passed in 8.94s; restored byte-identical: True
 m2 (the builder is not told to leave the record alone): FROM occurs 1x in packages/orchestration/self_use_generator.py
 m2: exit 1: 1 failed, 93 passed in 9.50s; restored byte-identical: True
 m3 (a pass confined to .agent/ is not named): FROM occurs 1x in packages/orchestration/self_use_findings.py
 m3: exit 1: 2 failed, 92 passed in 9.43s; restored byte-identical: True
 m4 (the stopped job's applied manifests are not read): FROM occurs 1x in packages/orchestration/self_use_findings.py
 m4: exit 1: 3 failed, 91 passed in 8.64s; restored byte-identical: True
 m5 (the cost cap is one dollar again): FROM occurs 1x in packages/orchestration/self_use_runner.py
 m5: exit 1: 3 failed, 91 passed in 9.26s; restored byte-identical: True
 control last: exit 0: 94 passed in 9.35s
 ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
 Then `git worktree remove --force .remedy-wt/f285-r1-mut`, `git worktree prune`, and report
 `git worktree list`.

G5 SIZES — `git show --numstat --format= <commit>` for C1a, C1b, C1c, C2, C3 and C4, each
 reported beside the expected insertions of its entry above, and placed in the handback's
 `## Commits` table exactly as the tool printed it.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 8`, which must show C5, C4, C3, C2, C1c, C1b, C1a and `83d3bb95` in that
 order; `git worktree list`, which must show no worktree this round added; the push's real
 outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which
 must be EMPTY. These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F285, round 1, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 1, then T003 — R-1055's provider-session resume across a relaunch. State the
open-findings count, 5, and the operator-questions count, 5.

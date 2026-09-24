STEP F284 R1 — CLAIM F284 AND LAND T001 AND T002: `teacher.model` reaches `teacher ask` (R-1046), and the vitest node's skip gate (R-0499)

GOAL
Pull request 275 is merged; `main` is at `a36a8759` and F284 is the next unchecked line. Cut its
branch, claim it, re-head the live review record, book F019's round 9 verdict, record DECISION
F284 D1 and write F284's slice list, then land T001, R-1046's repair: one helper,
`teacher_role_overrides` in `packages/orchestration/teacher_model.py`, reads `teacher.model` for
`ask_teacher` and for the lessons path, with the key's description and `docs/guides/environment.md`
corrected; and T002, R-0499's repair: `test_vitest_passes` skips on
`apps/ui/node_modules/.bin/vitest`, not on the directory. Red proofs for both.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f284-r1-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f284-r1/`           READ-ONLY. The reviewer's block, texts and builders.
  `.remedy-wt/f284-r1-dry/`       The reviewer's dry tree; do not touch it.
  `.remedy-wt/f284-r1-sim/`       The reviewer's simulated tree; do not touch it.
  `.remedy-wt/f284-r1-worker/`    YOURS for logs and scripts; create it if absent. All of these
                                  are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, `cd <dir> && git ...`, and multi-operation
one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe pytest.
Use `git -C <path>` rather than `cd`. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`). A heredoc containing a dollar-brace is refused: write such a
script to a file under your own directory and run the file. Never run npm or npx.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read `main`, and
   `git log --oneline -1` must read `a36a8759`. Report all three. Then
   `git checkout -b feature/f284-findings-paydown-v3` and report the branch. Do NOT pull: the
   Open PR Gate ran before you and `main` is already at the merge commit.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f284-r1/block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f284-r1-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| claim.diff | 161 | 16484 | b3081565b0b236688352e8caaa116278daec6680219b95fa992bada889577204 |
| plan.md | 30 | 1017 | 3d1d514742beb4849b92ce114e0096b44587189aa9985c2eed0963ae48d6234b |
| context.md | 36 | 1469 | 082b2105331af24ae6894c2addf00ddc8cb7b5c322c10a41d8788d4f1357db92 |
| r1046.diff | 166 | 10481 | fbe2063fd3a547820acfb470b03155c520059f395972cfc604e180b9b9a3fe76 |
| r0499.diff | 22 | 1325 | 85e6bf172fe437cf01a88f4d8664b8cd8382dfb5b44eaca5a6d7c0d988119d96 |
| mutations.py | 85 | 3686 | d3caa395f704dc5d83e4f72a4133c078364d2cc3948d3f584e873f9d4a141b6f |

`plan.md` and `context.md` are REWRITES of `.agent/plan.md` and `.agent/context.md`. The three
`.diff` payloads go on with `git apply`; the reviewer generated each with `git diff HEAD` from a
tree at `a36a8759` into which it wrote the edits. `claim.diff` edits `.agent/live_review.md` (the
re-head, then F019's round 9 gate entry appended), `.agent/decisions.md` (DECISION F284 D1
appended), `docs/roadmap/STATUS.md` (F284's line `[ ]` to `[~]`) and
`docs/roadmap/features/T2_F284.md` (the slice list and R-1046's Acceptance line). `r1046.diff`
edits `packages/orchestration/config.py`, `docs/guides/environment.md`,
`packages/orchestration/teacher_model.py`, `packages/orchestration/lessons.py`,
`packages/orchestration/pingpong_job.py`, `tests/orchestration/test_teacher_model.py` and
`tests/orchestration/test_lessons.py`. `r0499.diff` edits
`tests/orchestration/test_test_runner.py`. `mutations.py` is a TOOL for G5: it is run, never
applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C2, C3, C4 and C5, in this order.

C1a — copy this block and the claim payloads
  `.agent/authored/f284-r1-block.md` := this block, and `.agent/authored/f284-r1-plan.md`,
  `.agent/authored/f284-r1-context.md` and `.agent/authored/f284-r1-claim.diff` := plan.md,
  context.md and claim.diff. All by `shutil.copyfile`.
  Subject: `F284 R1 C1a: copy round 1 block and claim payloads into .agent/authored/`
  Expected insertions: 453 (this block's 226 lines plus 227 for the three payloads). Report the number you measure and STOP rather than commit if
  it is 500 or more.

C1b — copy the code payloads and the tool
  `.agent/authored/f284-r1-r1046.diff`, `.agent/authored/f284-r1-r0499.diff` and
  `.agent/authored/f284-r1-mutations.py` := r1046.diff, r0499.diff and mutations.py.
  Subject: `F284 R1 C1b: copy round 1 code payloads and mutation tool into .agent/authored/`
  Expected insertions: 273.

C2 — THE CLAIM AND ITS RECORDS, in this order:
   1. `git apply` claim.diff
   2. rewrite `.agent/plan.md` := plan.md
   3. rewrite `.agent/context.md` := context.md
  Subject: `F284 R1 C2: claim F284, re-head the live review record, book F019 R9, record D1`
  Expected insertions by `git show --numstat`: 12 .agent/context.md, 49 .agent/decisions.md, 28 .agent/live_review.md, 17 .agent/plan.md, 1 docs/roadmap/STATUS.md, 19 docs/roadmap/features/T2_F284.md.

C3 — T001, R-1046: `git apply` r1046.diff.
  Subject: `F284 R1 C3: read teacher.model for teacher ask and lessons through one helper`
  Expected insertions: 1 docs/guides/environment.md, 2 packages/orchestration/config.py, 0 packages/orchestration/lessons.py, 2 packages/orchestration/pingpong_job.py, 13 packages/orchestration/teacher_model.py, 3 tests/orchestration/test_lessons.py, 28 tests/orchestration/test_teacher_model.py.

C4 — T002, R-0499: `git apply` r0499.diff.
  Subject: `F284 R1 C4: gate the vitest node on the installed runner, as the tsc node is gated`
  Expected insertions: 6 tests/orchestration/test_test_runner.py.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F284 R1 C5: rewrite handoff for round 1`
  Then `git push -u origin feature/f284-findings-paydown-v3`. Do NOT create a pull request:
  the branch opens one at F284's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f284-r1-*` copies, the four
   paths claim.diff edits, `.agent/plan.md`, `.agent/context.md`, the seven paths r1046.diff
   edits, the one path r0499.diff edits, and `.agent/handoff.md`. Report the list you measure
   with `git diff --name-only a36a8759 HEAD` after C5. Do NOT touch `.agent/prose_slips.md`,
   `.agent/candidates.md`, `.agent/operator_questions.md` or `README.md`.
4. You write no `Done:` line and no `Landed:` line: the reviewer authors R-1046's and R-0499's
   resolutions at the next gate.
5. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main` after the
   branch is cut, no branch deletion, no force-push, no `git stash`.
7. Leave every existing worktree under `.remedy-wt/` and its branch alone, and every existing
   stash. The worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last action,
   and `git worktree list` is reported afterwards.
8. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F284's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f284-r1-*` copy byte for byte
 with its source (the block copy against `.remedy-wt/f284-r1/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE CLAIM AND THE CODE — the sha256 of each file below, read with `git show <commit>:<path>`
 at the commit the table names, equals the reviewer's reading, which its builder printed from
 the simulated tree:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/context.md | 1469 | 082b2105331af24ae6894c2addf00ddc8cb7b5c322c10a41d8788d4f1357db92 |
 | C2 | .agent/decisions.md | 2019743 | 299a06c6e8cd885a0010ff5c24e1b6dad7ea4626033c553f5ff5e9a98cb73ae3 |
 | C2 | .agent/live_review.md | 304288 | 5aa0bf8e247302296bd4732c8647edf38f409cb6fa6f37985bf8f67de383ecd9 |
 | C2 | .agent/plan.md | 1017 | 3d1d514742beb4849b92ce114e0096b44587189aa9985c2eed0963ae48d6234b |
 | C2 | docs/roadmap/STATUS.md | 50463 | 793f290bb77a95b81a1e53b53e070f258428062da98e558f402423bd7d167498 |
 | C2 | docs/roadmap/features/T2_F284.md | 4015 | 64f2ed62eb2a0ea8c632507562f11c7d2b6e4f6c4c0471273b5da395089fce25 |
 | C3 | docs/guides/environment.md | 21268 | d7688798816cb53884b90a4de6bd06ad67a4e20b6d3146e7716d2cdbac582621 |
 | C3 | packages/orchestration/config.py | 63251 | d55c56c5c21babc05f2fe2983db49fce114ef90d14630da0c648c16e89115fa1 |
 | C3 | packages/orchestration/lessons.py | 21150 | c46965d3e53e231995b2d3ca0ce82faf69397a0886e99ebb7fbd512ec8ad53a2 |
 | C3 | packages/orchestration/pingpong_job.py | 204054 | f491f5021ca227c3cae902b78a010e7f83e7dc032aa6bd46ff3d75767d48082e |
 | C3 | packages/orchestration/teacher_model.py | 10626 | bfd025b795a38a4b27a3005c0ddf81f0b86a671829c21a1f2bcd6ee14f07f1b1 |
 | C3 | tests/orchestration/test_lessons.py | 20517 | 961a32ee96167b7925e2cf27e225eacde531c860b32aa7df028a03f594d11db3 |
 | C3 | tests/orchestration/test_teacher_model.py | 12399 | 28ec4b0684d14d08efbc5d45c24a7922b2037a85cfa53a15c9f1f2b71a0f334e |
 | C4 | tests/orchestration/test_test_runner.py | 37844 | 757d684049f940d151fa9f9dcf7a3c92be1331e1fb20a40bb4a3edb645f5f4fa |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `a36a8759` and at C2 (the reviewer
 read R-0499, R-0950, R-1008 and R-1046 at both); F284's STATUS line at C2 read back in full,
 which must read `- [~] F284 — Findings paydown v3`; and `git diff --name-only` between each
 pair of consecutive commits from C1b to C4, each of which must name exactly the paths that
 commit's entry above lists.

G3 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_teacher_model.py tests/orchestration/test_lessons.py tests/orchestration/test_test_runner.py tests/cli/test_teacher_cmd.py tests/ui_server/test_lessons_route.py tests/cli/test_study_teacher_e2e.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection, serially, inside its sim tree at C4 and read
 `625 passed, 3 skipped` at real exit code 0. TWO of those skips are toolchain nodes a worktree cannot run and the primary
 checkout can, and each must PASS in your run, not skip: `test_vitest_passes` in
 `tests/orchestration/test_test_runner.py` and `test_typescript_compiles` in
 `tests/ui_server/test_dashboard_contract.py`. Report every `SKIPPED` line the `-rs` summary
 prints. Then `python3 -m ruff check` over every `.py` file r1046.diff and r0499.diff edit,
 named one by one, which must read `All checks passed!`; and `python3 -m apps.cli.main integrity check --json`, which must read
 all six checks `pass` at `fail_count` 0.

G4 THE RED PROOFS — `git worktree add --detach .remedy-wt/f284-r1-mut <C4>`, then
 `python3 -B .remedy-wt/f284-r1-payloads/mutations.py
 /home/decodeux/Repos/remedy/.remedy-wt/f284-r1-mut` and report its whole output. The tool
 asserts each FROM occurs exactly once, restores the bytes after each run, and runs unmutated
 controls first and last; m5 and the controls create an EMPTY `apps/ui/node_modules` inside the
 worktree for the vitest node and delete it again. The reviewer read, over the same tool
 against its simulated tree at C4:
 control first R-1046 tests: exit 0: 55 passed in 1.61s
 control first vitest node over an empty node_modules: exit 0: 1 skipped in 0.10s
 m1 (ask_teacher reads no override): FROM occurs 1x in packages/orchestration/teacher_model.py
 m1: exit 1: 1 failed, 54 passed in 1.72s; restored byte-identical: True
 m2 (the transport ignores the override): FROM occurs 1x in packages/orchestration/teacher_model.py
 m2: exit 1: 1 failed, 54 passed in 1.53s; restored byte-identical: True
 m3 (the lessons path hands in no override): FROM occurs 1x in packages/orchestration/pingpong_job.py
 m3: exit 1: 1 failed, 54 passed in 1.65s; restored byte-identical: True
 m4 (the helper never reads the key): FROM occurs 1x in packages/orchestration/teacher_model.py
 m4: exit 1: 3 failed, 52 passed in 2.09s; restored byte-identical: True
 m5 (the vitest gate reads the directory again): FROM occurs 1x in tests/orchestration/test_test_runner.py
 m5: exit 1: 1 failed in 0.87s; restored byte-identical: True
 control last R-1046 tests: exit 0: 55 passed in 1.97s
 control last vitest node over an empty node_modules: exit 0: 1 skipped in 0.15s
 ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
 Then `git worktree remove --force .remedy-wt/f284-r1-mut`, `git worktree prune`, and report
 `git worktree list`.

G5 SIZES — `git show --numstat --format= <commit>` for C1a, C1b, C2, C3 and C4, each reported
 beside the expected insertions of its entry above, and placed in the handback's `## Commits`
 table exactly as the tool printed it.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 7`, which must show C5, C4, C3, C2, C1b, C1a and `a36a8759` in that
 order; `git worktree list`, which must show no worktree this round added; the push's real
 outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which
 must be EMPTY. These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F284, round 1, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 1, then T003 — R-0950's zombie-process node in
`tests/orchestration/test_product_smoke.py`. State the open-findings count, 4, and the
operator-questions count, 3.

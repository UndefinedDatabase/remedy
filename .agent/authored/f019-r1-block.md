STEP F019 R1 — CLAIM F019 AND LAND T001: the brain graph's pure reducer, its goldens and its snapshot rebuild

GOAL
Pull request 274 is merged; `main` is at `92b7f5f1` and F019 is the next unchecked line. Cut its
branch, claim it, re-head the live review record, book F015's round 10 verdict and resolve
R-1047, record DECISION F019 D1 and the operator note it implies, and land T001:
`apps/ui/src/components/graph/brainOntology.ts` and `brainReducer.ts`, the pure reducer from the
stream's frames to the graph's nodes and links — idempotent per seq, with the snapshot rebuild,
the derived core state and the cluster view — and its fixtures and vitest tests, with red proofs.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f019-r1-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f019-r1/`           READ-ONLY. The reviewer's block, texts and builder.
  `.remedy-wt/f019-r1-sim/`       The reviewer's simulated tree; do not touch it.
  `.remedy-wt/f019-r1-worker/`    YOURS for logs and scripts; create it if absent. All three are
                                  gitignored.

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
   `git log --oneline -1` must read `92b7f5f1`. Report all three. Then
   `git checkout -b feature/f019-live-node-materialization` and report the branch. Do NOT
   pull: the Open PR Gate ran before you and `main` is already at the merge commit.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f019-r1/block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f019-r1-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| claim.diff | 195 | 23811 | 04a5e0c6ee5dd785bfa950c27ff8f61fa6e99c37ca9cc2aa4cefd706d4cb7aa5 |
| plan.md | 36 | 1532 | eb06fb3096482ca29d35127900f1662692f79afb361c201b57b14ff53406e17c |
| context.md | 40 | 1825 | 4abc1dc732f7c3fd1f7b36cdab232f3755988f4c48c121009c5ed91fc109e1a0 |
| mutations.py | 364 | 15075 | 325446c5c4cb51eb0db915c48108488f606a7e874cd451275c0b2fe040c64bbd |
| brainOntology.ts | 109 | 4317 | fb1997c381f6095b55f2e079a730ab7faf61a38204c92d9eadf8b8e5ba70fb4f |
| brainReducer.ts | 363 | 16360 | f2a3baa40c33c7c0ca4fe76b490334aaa28c070a5ca949c52596af5a7e6c8ad1 |
| brainReducer.fixtures.ts | 227 | 12383 | b1afe24bc6ac29029f3bb0f7178f7020f1f35c04492174f42d93bbe0ef13fd3c |
| brainReducer.test.ts | 246 | 11137 | 276f3d385b689586e526cb4d09dc70ae9e8b6359306870e72b3ef6a3e8e0cc2e |

`plan.md` and `context.md` are REWRITES of `.agent/plan.md` and `.agent/context.md`. The four
`.ts` payloads are NEW FILES under `apps/ui/src/components/graph/`, each copied whole.
`claim.diff` goes on with `git apply`; the reviewer generated it with `git diff` from a tree at
`92b7f5f1` into which its builder wrote the edits. It edits `.agent/live_review.md` (the re-head,
then F015's round 10 gate entry and R-1047's `Done:` line appended), `docs/roadmap/STATUS.md`
(F019's line `[ ]` to `[~]`), `.agent/decisions.md` (DECISION F019 D1 appended) and
`.agent/operator_questions.md` (entry Q2 appended). `mutations.py` is a TOOL for G5: it is run,
never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C1e, C2, C3, C4 and C5, in this order.

C1a — copy this block and the state payloads
  `.agent/authored/f019-r1-block.md` := this block, and `.agent/authored/f019-r1-plan.md` and
  `.agent/authored/f019-r1-context.md` := plan.md and context.md. All by `shutil.copyfile`.
  Subject: `F019 R1 C1a: copy round 1 block and state payloads into .agent/authored/`
  Its insertions are this block's line count plus 76. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C1b — copy the claim diff
  `.agent/authored/f019-r1-claim.diff` := claim.diff.
  Subject: `F019 R1 C1b: copy round 1 claim diff into .agent/authored/`
  Expected insertions: 195.

C1c — copy the mutation tool
  `.agent/authored/f019-r1-mutations.py` := mutations.py.
  Subject: `F019 R1 C1c: copy round 1 mutation tool into .agent/authored/`
  Expected insertions: 364.

C1d — copy the product payloads
  `.agent/authored/f019-r1-brainOntology.ts` and `.agent/authored/f019-r1-brainReducer.ts`.
  Subject: `F019 R1 C1d: copy round 1 product modules into .agent/authored/`
  Expected insertions: 472.

C1e — copy the test payloads
  `.agent/authored/f019-r1-brainReducer.fixtures.ts` and
  `.agent/authored/f019-r1-brainReducer.test.ts`.
  Subject: `F019 R1 C1e: copy round 1 test payloads into .agent/authored/`
  Expected insertions: 473.

C2 — THE CLAIM AND ITS RECORDS, in this order:
   1. `git apply` claim.diff
   2. rewrite `.agent/plan.md` := plan.md
   3. rewrite `.agent/context.md` := context.md
  Subject: `F019 R1 C2: claim F019, re-head the live review record, book F015 R10, record D1`
  Expected insertions by `git show --numstat`: 23 context.md, 62 decisions.md, 32
  live_review.md, 26 operator_questions.md, 23 plan.md, 1 STATUS.md.

C3 — THE PRODUCT: copy brainOntology.ts and brainReducer.ts into
  `apps/ui/src/components/graph/`, then `git add` both — an untracked module fails
  `integrity check`'s `relevant_untracked`.
  Subject: `F019 R1 C3: reduce stream frames into the brain graph's nodes and links`
  Expected insertions: 109 brainOntology.ts, 363 brainReducer.ts.

C4 — THE TESTS: copy brainReducer.fixtures.ts and brainReducer.test.ts into
  `apps/ui/src/components/graph/` and `git add` both.
  Subject: `F019 R1 C4: pin the reducer with goldens, replays, gaps and the cluster view`
  Expected insertions: 227 brainReducer.fixtures.ts, 246 brainReducer.test.ts.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F019 R1 C5: rewrite handoff for round 1`
  Then `git push -u origin feature/f019-live-node-materialization`. Do NOT create a pull
  request: the branch opens one at F019's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f019-r1-*` copies,
   `.agent/live_review.md`, `docs/roadmap/STATUS.md`, `.agent/decisions.md`,
   `.agent/operator_questions.md`, `.agent/plan.md`, `.agent/context.md`, the four `.ts` files
   under `apps/ui/src/components/graph/` that the payloads name, and `.agent/handoff.md`.
   Report the list you measure with `git diff --name-only 92b7f5f1 HEAD` after C5. Do NOT touch
   `.agent/prose_slips.md`, `.agent/candidates.md`, `README.md` or
   `docs/roadmap/features/T5_F019.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main` after the
   branch is cut, no branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, the reviewer's worktrees
   (`.remedy-wt/f019-r1-sim`, `.remedy-wt/f019-r1-proto` and the older `.remedy-wt/f015-r*`
   ones), and every existing stash alone. The worktree G5 adds goes under `.remedy-wt/`, is
   removed as that step's last action, and `git worktree list` is reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F019's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f019-r1-*` copy byte for byte
 with its source (the block copy against `.remedy-wt/f019-r1/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE CLAIM — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, which its builder printed from the simulated tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 307206 | 021ec908280fa432070fc6442d5789fffe6b61107d46c16fbd5adf82daaee9ed |
 | docs/roadmap/STATUS.md | 50105 | 685f3992d537f74d9f423d3b24828903cbb87489f5371246d094bc5029b42510 |
 | .agent/decisions.md | 1996695 | c61b005155a4ca965ac7f372189249d2efd8a0886adc855a8ec2118d78727731 |
 | .agent/operator_questions.md | 4006 | 56eb03148206a634485dd33e6eb2e1b15608d6b2c357ba9918a8cdf06b0e614b |
 | .agent/plan.md | 1532 | eb06fb3096482ca29d35127900f1662692f79afb361c201b57b14ff53406e17c |
 | .agent/context.md | 1825 | 4abc1dc732f7c3fd1f7b36cdab232f3755988f4c48c121009c5ed91fc109e1a0 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `92b7f5f1` and at C2 (the reviewer
 read R-0499, R-0950, R-1008, R-1046 and R-1047 at `92b7f5f1`, and the same less R-1047 at C2);
 F019's STATUS line at C2 read back in full, which must read
 `- [~] F019 — Live node materialization`; and `git diff --name-only <C1e> <C2>`, which must
 name exactly the six paths of the table above.

G3 THE PRODUCT — at C4, the sha256 of each of the four `.ts` files under
 `apps/ui/src/components/graph/`, read with `git show <C4>:<path>`, equals its payload's sha256
 in the PAYLOADS table. Also `git diff --name-only <C2> <C3>` and `<C3> <C4>`, which must name
 exactly the paths C3 and C4 list.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path, serially, inside its sim tree
 carrying C2 to C4 and read `1346 passed, 10 skipped` at real exit code 0. FOUR of those skips
 are toolchain nodes a worktree cannot run and the primary checkout can, and each must PASS in
 your run, not skip: the two in `tests/ui_contracts/test_ui_lint.py` (eslint at zero
 warnings), the typescript node in `tests/ui_server/test_dashboard_contract.py`
 (`tsc --noEmit`) and the vitest node in `tests/orchestration/test_test_runner.py`, which runs
 the UI's whole unit suite and so the new tests. Report every `SKIPPED` line the `-rs` summary
 prints. Then `python3 -m apps.cli.main integrity check --json`, which must read all six checks
 `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f019-r1-mut <C4>`, then
 `python3 -B .remedy-wt/f019-r1-payloads/mutations.py
 /home/decodeux/Repos/remedy/.remedy-wt/f019-r1-mut` and report its whole output. For each
 mutation the tool runs vitest over the WORKTREE's `brainReducer.test.ts` from the primary
 `apps/ui` with a scratch config under `.remedy-wt/f019-r1-mutscratch/`, asserts each FROM
 occurs exactly once, restores the bytes, and runs an unmutated control first and last. The
 reviewer read, over the same tool against its sim tree:
 control first `36 passed` at exit 0;
 m1 (the replay guard removed) 9 failed at exit 1;
 m2 (a new start leaves the previous run open) 1 failed at exit 1;
 m3 (`needs_repair` read as pass) 6 failed at exit 1;
 m4 (the rebuild does not sort by seq) 2 failed at exit 1;
 m5 (the last row of a repeated seq wins) 1 failed at exit 1;
 m6 (the core never leaves `planned`) 17 failed at exit 1;
 m7 (the cluster keeps one run too many) 1 failed at exit 1;
 m8 (an unmapped kind is not counted) 3 failed at exit 1;
 m9 (`builder_started` counted) 3 failed at exit 1;
 m10 (a task the seed lacks is not born) 4 failed at exit 1;
 m11 (`job_stopped` leaves runs open) 1 failed at exit 1;
 m12 (`applied_to_job_workspace` read as planned) 1 failed at exit 1;
 m13 (run ids from a per-task counter) 6 failed at exit 1;
 control last `36 passed` at exit 0; every `restored byte-identical` line True, and the final
 line `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`.
 Then `git worktree remove --force .remedy-wt/f019-r1-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 10`, which must show C5, C4, C3, C2, C1e, C1d, C1c, C1b, C1a and
 `92b7f5f1` in that order; `git worktree list`, which must show the primary checkout and the
 worktrees constraint 6 names, and nothing else; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F019, round 1, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 1, then T002 — rendering the reducer's model on react-force-graph-2d by extending
`buildForceBrainModel.ts`, the layout, the glyph slots, the motion tokens and the demo
recording. State the open-findings count, 4, and the operator-questions count, 2.

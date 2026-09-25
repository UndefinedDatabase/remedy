STEP F020 R4 — T003 FIRST HALF: state crossfade and completion ripple, the pulse, frames only on a visible page, and the demo recording replayed

GOAL
Book round 3's PASS and record DECISION F020 D4, then land the first half of T003:
`apps/ui/src/components/graph/renderers/stateMotion.ts`, which schedules a 300 ms crossfade for
every state change and a completion ripple into `pass`, and decides whether the canvas needs
frames at all, never on a hidden page; the pulse multiplier `pulseScaleAt` in
`renderers/nodeStates.ts`; the motion-aware painter `paintBrainNodeInMotion` in
`renderers/paintNode.ts`; `usePageVisible.ts`; and `ForceBrainGraph.tsx` wired to them, its edge
particles stopping with the page. With the replay of F019's demo recording, contract tests and
red proofs.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f020-r4-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f020-r4/`           READ-ONLY. The reviewer's block and scripts.
  `.remedy-wt/f020-r4-sim/`       The reviewer's simulated tree; do not touch it.
  `.remedy-wt/f020-r4-dry/`       The reviewer's authoring tree; do not touch it.
  `.remedy-wt/f020-r4-worker/`    YOURS for logs and scripts; create it if absent. All five are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, command substitution, `cd <dir> && git ...`,
and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit
codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`). A heredoc containing a dollar-brace is refused: write such a
script to a file under your own directory and run the file. Never run npm or npx.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f020-node-lifecycle-glyph-language`, and `git log --oneline -1` must read
   `6f43c63a`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f020-r4/block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f020-r4-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| book.diff | 64 | 11647 | c0f4f0750ccda20105cd82615e49063f4f6c729705bd83081e14ce9d2d10fd5b |
| mutations.py | 187 | 10093 | 7533d95038ea65645b979ff4482a37520574482f99c8582577920d0771020b81 |
| plan.md | 30 | 1116 | 7c10e770db7b24c290866d2c3c3280feeb20a14aba54803ed8530c332cb0d72d |
| product.diff | 233 | 12343 | 86945bd38e5d7e39388c4e17ec2a1e1e5d7c224fafcf7201b2a08412019c11d1 |
| stateMotion.test.ts | 151 | 7514 | f33a61a8ae450d327ed7f2a59b5ae35824157eb01080a06bfc1dd2fc50748d01 |
| stateMotion.ts | 101 | 4173 | 3228d4d97bb77aaba636e783626d5745ae339c70c6b546d99cde3d89821c685a |
| test_brain_motion_wiring.py | 57 | 3085 | 5c85828096ceeceeed2dff223a42b19bf692957ea617a7429c1afc52cf22e2d5 |
| tests.diff | 113 | 5759 | d4970a9e7c61ce6e5c3838779d76328205a02edaa5227d9cb805f3c4a1dfc8ea |
| usePageVisible.ts | 15 | 768 | 4e034c48d00949c5171e50eda04efb4748c477e52785df2cc37339b873312ff4 |

`plan.md` is a REWRITE of `.agent/plan.md`. These are NEW FILES, each copied whole:
`stateMotion.ts` and `stateMotion.test.ts` under `apps/ui/src/components/graph/renderers/`;
`usePageVisible.ts` under `apps/ui/src/components/graph/`; and `test_brain_motion_wiring.py` under
`tests/ui_contracts/`. The three diffs go on with `git apply`; the reviewer generated each with
`git diff HEAD` from a tree at `6f43c63a` into which it wrote the edits. `book.diff` appends round
3's gate entry to `.agent/live_review.md` and DECISION F020 D4 to `.agent/decisions.md`.
`product.diff` edits `apps/ui/src/components/graph/ForceBrainGraph.tsx`, `renderers/nodeStates.ts`
and `renderers/paintNode.ts`. `tests.diff` edits `renderers/nodeStates.test.ts`,
`renderers/paintNode.test.ts` and `tests/ui_contracts/test_node_glyph_tokens.py`. `mutations.py`
is a TOOL for G5: it is run, never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C1e, C2, C3, C4 and C5, in this order.

C1a — copy this block and the plan payload
  `.agent/authored/f020-r4-block.md` := this block, `.agent/authored/f020-r4-plan.md` := plan.md.
  Both by `shutil.copyfile`.
  Subject: `F020 R4 C1a: copy round 4 block and plan payload into .agent/authored/`
  Its insertions are this block's line count plus 30. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C1b — copy the three diffs
  `.agent/authored/f020-r4-book.diff`, `.agent/authored/f020-r4-product.diff` and
  `.agent/authored/f020-r4-tests.diff`.
  Subject: `F020 R4 C1b: copy round 4 diffs into .agent/authored/`
  Expected insertions: 410.

C1c — copy the mutation tool
  `.agent/authored/f020-r4-mutations.py` := mutations.py.
  Subject: `F020 R4 C1c: copy round 4 mutation tool into .agent/authored/`
  Expected insertions: 187.

C1d — copy the new product files
  `.agent/authored/f020-r4-stateMotion.ts` and `.agent/authored/f020-r4-usePageVisible.ts`.
  Subject: `F020 R4 C1d: copy round 4 product files into .agent/authored/`
  Expected insertions: 116.

C1e — copy the new test files
  `.agent/authored/f020-r4-stateMotion.test.ts` and
  `.agent/authored/f020-r4-test_brain_motion_wiring.py`.
  Subject: `F020 R4 C1e: copy round 4 test payloads into .agent/authored/`
  Expected insertions: 208.

C2 — THE BOOKKEEPING, in this order: `git apply` book.diff, then rewrite `.agent/plan.md` :=
  plan.md.
  Subject: `F020 R4 C2: book round 3's PASS, record D4, advance the plan`
  Expected insertions by `git show --numstat`: 46 decisions.md, 2 live_review.md, 6 plan.md.

C3 — THE PRODUCT: `git apply` product.diff, then copy stateMotion.ts and usePageVisible.ts to
  their paths and `git add` both — an untracked module fails `integrity check`'s
  `relevant_untracked`.
  Subject: `F020 R4 C3: crossfade state changes, ripple completions, pulse, and draw frames only on a visible page`
  Expected insertions: 56 ForceBrainGraph.tsx, 12 nodeStates.ts, 46 paintNode.ts, 101
  stateMotion.ts, 15 usePageVisible.ts.

C4 — THE TESTS: `git apply` tests.diff, then copy stateMotion.test.ts and
  test_brain_motion_wiring.py to their paths and `git add` both.
  Subject: `F020 R4 C4: pin the motion, the frame rule, the replayed recording and the canvas wiring`
  Expected insertions: 21 nodeStates.test.ts, 47 paintNode.test.ts, 151 stateMotion.test.ts, 57
  test_brain_motion_wiring.py, 1 test_node_glyph_tokens.py.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F020 R4 C5: rewrite handoff for round 4`
  Then `git push origin feature/f020-node-lifecycle-glyph-language`. Do NOT create a pull
  request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f020-r4-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, the paths C3 and C4 list, and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only 6f43c63a HEAD`
   after C5. Do NOT touch `.agent/context.md`, `.agent/prose_slips.md`, `.agent/candidates.md`,
   `.agent/operator_questions.md`, `README.md`, `docs/roadmap/STATUS.md` or
   `docs/roadmap/features/T5_F020.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch
   deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, the reviewer's worktrees (the
   `-sim` and `-dry` trees of rounds 1 to 4 under the `.remedy-wt/f020-r` prefix, and the older
   `.remedy-wt/f015-r*` and `.remedy-wt/f284-r*` ones), and every existing stash alone. The
   worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last action, and
   `git worktree list` is reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F020's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f020-r4-*` copy byte for byte
 with its source (the block copy against `.remedy-wt/f020-r4/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE BOOKKEEPING — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, which its builder printed from the simulated tree:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/live_review.md | 295964 | a5f11b1f31bf69f8979c82d3488bd927d87ce9b563f0d999c5376647a87f0c44 |
 | C2 | .agent/decisions.md | 2040394 | b8589c84a33ecd767c9323bcfb9955c37efaa36bc550c4da2501a1b815536e81 |
 | C2 | .agent/plan.md | 1116 | 7c10e770db7b24c290866d2c3c3280feeb20a14aba54803ed8530c332cb0d72d |
 Also: the number of lines C2's diff of `.agent/live_review.md` adds that begin
 `Gate: F020 R3 — ` (the reviewer read 1); the open set by distinct id, computed with
 `open_finding_ids` from `scripts/rotate_live_review.py` over the file's TEXT at C2 (the reviewer
 read R-1008 alone); and `git diff --name-only <C1e> <C2>`, which must name exactly the paths of
 the table above.

G3 THE PRODUCT AND THE TESTS — the sha256 of each file below, read with `git show` at the commit
 named, equals the reviewer's reading from the simulated tree (paths under
 `apps/ui/src/components/graph/` are written from that directory down):
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C3 | ForceBrainGraph.tsx | 16279 | 1b426ee1e69ddd674016fa97ece8a4e6a41282334204f6c5b6e09be1fc8c3e9c |
 | C3 | renderers/nodeStates.ts | 7016 | 6bb616d191f910664f484de5761a55268e724cd576024c293cd3b33899bea4be |
 | C3 | renderers/paintNode.ts | 8098 | df2cf6105056588dc1ae5e73bc07fc4e6923eca7594547f989d9091be62d238a |
 | C3 | renderers/stateMotion.ts | 4173 | 3228d4d97bb77aaba636e783626d5745ae339c70c6b546d99cde3d89821c685a |
 | C3 | usePageVisible.ts | 768 | 4e034c48d00949c5171e50eda04efb4748c477e52785df2cc37339b873312ff4 |
 | C4 | renderers/nodeStates.test.ts | 6774 | 0e6ad9051ddec719a9fe4c82965756fb18f7cdb1ce5b04f746a62b8e036bb34a |
 | C4 | renderers/paintNode.test.ts | 12429 | 7375c307d99ec579ebc32a62a510124ced596d6458d521cd0edb3c9b9b963763 |
 | C4 | tests/ui_contracts/test_node_glyph_tokens.py | 6142 | c3f1710c162944e773945ec18b097bbbb2d7fc0b1076249908f69c717528a584 |
 | C4 | renderers/stateMotion.test.ts | 7514 | f33a61a8ae450d327ed7f2a59b5ae35824157eb01080a06bfc1dd2fc50748d01 |
 | C4 | tests/ui_contracts/test_brain_motion_wiring.py | 3085 | 5c85828096ceeceeed2dff223a42b19bf692957ea617a7429c1afc52cf22e2d5 |
 Also `git diff --name-only <C2> <C3>` and `<C3> <C4>`, which must name exactly the paths C3 and
 C4 list; and `python3 -m ruff check tests/ui_contracts/test_brain_motion_wiring.py
 tests/ui_contracts/test_node_glyph_tokens.py` at C4.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py tests/regression/test_named_bugs.py tests/test_agent_tooling.py tests/cli/test_golden_path.py 2>&1 | tail -20; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path, serially, inside its sim tree
 carrying C2 to C4 and read `1127 passed, 16 skipped` at real exit code 0. FOUR of those skips
 are toolchain nodes a worktree cannot run and the primary checkout can, and each must PASS in
 your run, not skip: the two in `tests/ui_contracts/test_ui_lint.py` (eslint at zero
 warnings), the typescript node in `tests/ui_server/test_dashboard_contract.py`
 (`tsc --noEmit`) and the vitest node in `tests/orchestration/test_test_runner.py`, which runs
 the UI's whole unit suite and so this round's test files. Report every `SKIPPED` line the `-rs`
 summary prints. Then `python3 -m apps.cli.main integrity check --json`, which must read all six
 checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f020-r4-mut <C4>`, then
 `python3 -B .remedy-wt/f020-r4-payloads/mutations.py
 /home/decodeux/Repos/remedy/.remedy-wt/f020-r4-mut` and report its whole output. For each
 mutation the tool runs vitest over the WORKTREE's three `.test.ts` files this round touches or
 adds, from the primary `apps/ui` with a scratch config under `.remedy-wt/f020-r4-mutscratch/`,
 and pytest over the worktree's two Python contract files; it asserts each FROM occurs exactly
 once, restores the bytes, and runs an unmutated control first and last. The reviewer read, over
 the same tool against its sim tree (v = vitest failed, g = contract tests failed, each red at
 exit 1 wherever its count is not 0):
 control first vitest 56 passed and contract tests 12 passed, both at exit 0;
 m1 (reduced motion still schedules state changes) v2 g0;
 m2 (the job core's state change is scheduled) v2 g0;
 m3 (every state change ripples) v3 g0;
 m4 (a node just born is scheduled as a change) v2 g0;
 m5 (the crossfade runs backwards) v2 g0;
 m6 (the ripple travels linearly) v1 g0;
 m7 (a hidden page still asks for frames) v1 g0;
 m8 (the pulse draws frames under reduced motion) v1 g0;
 m9 (the core counts as a pulsing node) v1 g0;
 m10 (the pulse multiplier ignores reduced motion) v2 g0;
 m11 (the old state is painted at full alpha during a change) v1 g0;
 m12 (the ripple is never painted) v1 g0;
 m13 (the painter ignores the pulse multiplier) v1 g0;
 m14 (the canvas redraws only for births again) v0 g1;
 m15 (particles flow on a hidden page) v0 g1;
 m16 (the frame rule is told the page is always visible) v0 g1;
 m17 (the canvas paints every node without its motion) v0 g1;
 m18 (the visibility hook never listens) v0 g1;
 control last as first; every `restored byte-identical` reading True, and the final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`.
 Then `git worktree remove --force .remedy-wt/f020-r4-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 10`, which must show C5, C4, C3, C2, C1e, C1d, C1c, C1b, C1a and
 `6f43c63a` in that order; `git worktree list`, which must show the primary checkout and the
 worktrees constraint 6 names, and nothing else; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F020, round 4, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 4, then T003's second half — the conformance assertions over the matrix fixture's pixels,
with the headless harness that reads them. State the open-findings count, 1, and the
operator-questions count, 3.

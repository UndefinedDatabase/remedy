STEP F020 R3 — T002 SECOND HALF: the legend generated from the glyph and state modules, the cluster's count, and the matrix fixture

GOAL
Book round 2's PASS and record DECISION F020 D3, then land the second half of T002:
`apps/ui/src/components/graph/renderers/legendModel.ts`, the legend's rows enumerated from the
glyph and state modules; `GraphLegend.tsx` and its stylesheet, a "Legend" dialog opened from the
graph's chrome that renders those rows and writes no name, path or colour of its own, mounted by
`BrainGraphStage.tsx`; a cluster's `+n` count, from the layout's label and written by the
painter in a font the palette bridge resolves; and `renderers/glyphMatrix.ts`, every non-core
kind in every state painted by the live painter. With tests and red proofs.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f020-r3-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f020-r3/`           READ-ONLY. The reviewer's block and scripts.
  `.remedy-wt/f020-r3-sim/`       The reviewer's simulated tree; do not touch it.
  `.remedy-wt/f020-r3-dry/`       The reviewer's authoring tree; do not touch it.
  `.remedy-wt/f020-r3-worker/`    YOURS for logs and scripts; create it if absent. All five are
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
   `1d954ef5`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f020-r3/block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f020-r3-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| GraphLegend.module.css | 60 | 1508 | 0f14ff256eba21b459a7dd35c0e30e951b24871db87ea5f1900e2435830bdbee |
| GraphLegend.tsx | 83 | 3143 | ad0c565b5e3f973aa3128fa76a1b2951edeb6a268638a2cf1986fe0fbca739de |
| book.diff | 58 | 10093 | 4b4a1f748c5a109eb763e757fd8f842e62f441c9f255bdae0469e319ab4ef147 |
| glyphMatrix.test.ts | 69 | 3253 | 69726b35ede404be10bbc327143591c9ceb63e10a3ddd3b71d299eb45a399d33 |
| glyphMatrix.ts | 76 | 3139 | a386296e9408fac82eff5fa5e1b0aca3b7471b95eaf65987217089ed31a78e84 |
| legendModel.test.ts | 63 | 2649 | 8649a311c069b5adb1a6dfa3785409d2361f52b8900c5a6439f79143ef738d38 |
| legendModel.ts | 72 | 2609 | 133d45264c4858edd3432ac65af4d6590bf7c6bdbe7a945ff7147e1df7b74e16 |
| mutations.py | 195 | 10532 | b17af969d6349d43152df6b7c2591bba585268ac4a25ce61ccc48f89e7649623 |
| plan.md | 31 | 1155 | c79de02923262d0d6dd2329e284175816375650aad7edb80abdc46103bc4bc4f |
| product.diff | 187 | 9353 | 58175cd16fd3e55bd83037bab733bc2ada099677e00950e6904975aec367a909 |
| test_graph_legend_contract.py | 68 | 3056 | 1ad5d9063894f72aa59bae789077d96f72ac068a9c21c57e0c1174b0643b4e03 |
| tests.diff | 126 | 6631 | 03c25f5d259c95a837b844ca12b3221a9b89fb5630b320d24e052cb306701dc8 |

`plan.md` is a REWRITE of `.agent/plan.md`. These are NEW FILES, each copied whole:
`GraphLegend.tsx` and `GraphLegend.module.css` under `apps/ui/src/components/graph/`;
`legendModel.ts`, `glyphMatrix.ts`, `legendModel.test.ts` and `glyphMatrix.test.ts` under
`apps/ui/src/components/graph/renderers/`; and `test_graph_legend_contract.py` under
`tests/ui_contracts/`. The three diffs go on with `git apply`; the reviewer generated each with
`git diff HEAD` from a tree at `1d954ef5` into which it wrote the edits. `book.diff` appends round
2's gate entry to `.agent/live_review.md` and DECISION F020 D3 to `.agent/decisions.md`.
`product.diff` edits `BrainGraphStage.tsx`, `BrainGraphStage.module.css` and
`buildForceBrainModel.ts` under `apps/ui/src/components/graph/`, and `renderers/paintNode.ts` and
`renderers/palette.ts`. `tests.diff` edits `buildForceBrainModel.test.ts`,
`renderers/paintNode.test.ts` and `renderers/palette.test.ts`. `mutations.py` is a TOOL for G5:
it is run, never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C1e, C2, C3, C4 and C5, in this order.

C1a — copy this block and the plan payload
  `.agent/authored/f020-r3-block.md` := this block, `.agent/authored/f020-r3-plan.md` := plan.md.
  Both by `shutil.copyfile`.
  Subject: `F020 R3 C1a: copy round 3 block and plan payload into .agent/authored/`
  Its insertions are this block's line count plus 31. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C1b — copy the three diffs
  `.agent/authored/f020-r3-book.diff`, `.agent/authored/f020-r3-product.diff` and
  `.agent/authored/f020-r3-tests.diff`.
  Subject: `F020 R3 C1b: copy round 3 diffs into .agent/authored/`
  Expected insertions: 371.

C1c — copy the mutation tool
  `.agent/authored/f020-r3-mutations.py` := mutations.py.
  Subject: `F020 R3 C1c: copy round 3 mutation tool into .agent/authored/`
  Expected insertions: 195.

C1d — copy the new product files
  `.agent/authored/f020-r3-legendModel.ts`, `.agent/authored/f020-r3-glyphMatrix.ts`,
  `.agent/authored/f020-r3-GraphLegend.tsx` and `.agent/authored/f020-r3-GraphLegend.module.css`.
  Subject: `F020 R3 C1d: copy round 3 product files into .agent/authored/`
  Expected insertions: 291.

C1e — copy the new test files
  `.agent/authored/f020-r3-legendModel.test.ts`, `.agent/authored/f020-r3-glyphMatrix.test.ts` and
  `.agent/authored/f020-r3-test_graph_legend_contract.py`.
  Subject: `F020 R3 C1e: copy round 3 test payloads into .agent/authored/`
  Expected insertions: 200.

C2 — THE BOOKKEEPING, in this order: `git apply` book.diff, then rewrite `.agent/plan.md` :=
  plan.md.
  Subject: `F020 R3 C2: book round 2's PASS, record D3, advance the plan`
  Expected insertions by `git show --numstat`: 40 decisions.md, 2 live_review.md, 8 plan.md.

C3 — THE PRODUCT: `git apply` product.diff, then copy the four new product files to their paths
  and `git add` all four — an untracked module fails `integrity check`'s `relevant_untracked`.
  Subject: `F020 R3 C3: generate the graph legend from the glyph and state modules, count clusters, paint the matrix`
  Expected insertions: 1 BrainGraphStage.module.css, 2 BrainGraphStage.tsx, 60
  GraphLegend.module.css, 83 GraphLegend.tsx, 10 buildForceBrainModel.ts, 76 glyphMatrix.ts, 72
  legendModel.ts, 23 paintNode.ts, 6 palette.ts.

C4 — THE TESTS: `git apply` tests.diff, then copy the three new test files to their paths and
  `git add` all three.
  Subject: `F020 R3 C4: pin the legend's rows, its wiring, the cluster count and the matrix`
  Expected insertions: 8 buildForceBrainModel.test.ts, 69 glyphMatrix.test.ts, 63
  legendModel.test.ts, 30 paintNode.test.ts, 4 palette.test.ts, 68
  test_graph_legend_contract.py.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F020 R3 C5: rewrite handoff for round 3`
  Then `git push origin feature/f020-node-lifecycle-glyph-language`. Do NOT create a pull
  request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f020-r3-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, the paths C3 and C4 list, and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only 1d954ef5 HEAD`
   after C5. Do NOT touch `.agent/context.md`, `.agent/prose_slips.md`, `.agent/candidates.md`,
   `.agent/operator_questions.md`, `README.md`, `docs/roadmap/STATUS.md`,
   `docs/roadmap/features/T5_F020.md` or `apps/ui/src/components/graph/ForceBrainGraph.tsx`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch
   deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, the reviewer's worktrees
   (`.remedy-wt/f020-r1-sim`, `-r1-dry`, `-r2-sim`, `-r2-dry`, `-r3-sim` and `-r3-dry`, each
   with the `.remedy-wt/f020` prefix, and the older `.remedy-wt/f015-r*` and `.remedy-wt/f284-r*`
   ones), and every existing stash alone. The worktree G5 adds goes under `.remedy-wt/`, is
   removed as that step's last action, and `git worktree list` is reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F020's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f020-r3-*` copy byte for byte
 with its source (the block copy against `.remedy-wt/f020-r3/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE BOOKKEEPING — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, which its builder printed from the simulated tree:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/live_review.md | 293386 | 8565fe941e7222e08f633ffdcf0e3a6c08b386f2e73c7c060c938134dedeef94 |
 | C2 | .agent/decisions.md | 2036559 | b30351b7139ca97ee81b05e19a158bc2b2192c96208c590fe2ec0fa143834b4f |
 | C2 | .agent/plan.md | 1155 | c79de02923262d0d6dd2329e284175816375650aad7edb80abdc46103bc4bc4f |
 Also: the number of lines C2's diff of `.agent/live_review.md` adds that begin
 `Gate: F020 R2 — ` (the reviewer read 1); the open set by distinct id, computed with
 `open_finding_ids` from `scripts/rotate_live_review.py` over the file's TEXT at C2 (the reviewer
 read R-1008 alone); and `git diff --name-only <C1e> <C2>`, which must name exactly the paths of
 the table above.

G3 THE PRODUCT AND THE TESTS — the sha256 of each file below, read with `git show` at the commit
 named, equals the reviewer's reading from the simulated tree (paths under
 `apps/ui/src/components/graph/` are written from that directory down):
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C3 | BrainGraphStage.tsx | 3438 | 996eb59cfdd062dbdacfa004c006a22149789040d70f7974ea34f67ff30b76ee |
 | C3 | BrainGraphStage.module.css | 1112 | 8d15d5450a2811b5cef68a6934d18064397d26709f6d5755578d9e9b65ba6944 |
 | C3 | buildForceBrainModel.ts | 8422 | 4c93b0dc7287a91ebc6a5fe52efe3183a482858a5a62bc392c2d742a39b8a274 |
 | C3 | renderers/paintNode.ts | 6057 | 6828b4a51eff6f2d19e5b7e3c5dd058e4340a70b82bde482c9c610c2e8beb47f |
 | C3 | renderers/palette.ts | 2348 | 4926d3d0b2dcd90803dba48a6d2b743e2f896adf7d5f5ac2654fee2bdb1d8b31 |
 | C3 | renderers/legendModel.ts | 2609 | 133d45264c4858edd3432ac65af4d6590bf7c6bdbe7a945ff7147e1df7b74e16 |
 | C3 | renderers/glyphMatrix.ts | 3139 | a386296e9408fac82eff5fa5e1b0aca3b7471b95eaf65987217089ed31a78e84 |
 | C3 | GraphLegend.tsx | 3143 | ad0c565b5e3f973aa3128fa76a1b2951edeb6a268638a2cf1986fe0fbca739de |
 | C3 | GraphLegend.module.css | 1508 | 0f14ff256eba21b459a7dd35c0e30e951b24871db87ea5f1900e2435830bdbee |
 | C4 | buildForceBrainModel.test.ts | 10378 | ad72e789e7c6e8d84bac13cde2645412b73730154c3e1cdf431b14d863dfc294 |
 | C4 | renderers/paintNode.test.ts | 10285 | dd49b85750b5c2b417c11cb78ef7e8f30d99d9114695078da7132490793b526c |
 | C4 | renderers/palette.test.ts | 1367 | b5d43d7e1695c4d73b5b5b94de8526049ca36f72b7cda9805d550ae2815c66bb |
 | C4 | renderers/legendModel.test.ts | 2649 | 8649a311c069b5adb1a6dfa3785409d2361f52b8900c5a6439f79143ef738d38 |
 | C4 | renderers/glyphMatrix.test.ts | 3253 | 69726b35ede404be10bbc327143591c9ceb63e10a3ddd3b71d299eb45a399d33 |
 | C4 | tests/ui_contracts/test_graph_legend_contract.py | 3056 | 1ad5d9063894f72aa59bae789077d96f72ac068a9c21c57e0c1174b0643b4e03 |
 Also `git diff --name-only <C2> <C3>` and `<C3> <C4>`, which must name exactly the paths C3 and
 C4 list; and `python3 -m ruff check tests/ui_contracts/test_graph_legend_contract.py` at C4.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py tests/regression/test_named_bugs.py tests/test_agent_tooling.py tests/cli/test_golden_path.py 2>&1 | tail -20; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path, serially, inside its sim tree
 carrying C2 to C4 and read `1123 passed, 16 skipped` at real exit code 0. FOUR of those skips
 are toolchain nodes a worktree cannot run and the primary checkout can, and each must PASS in
 your run, not skip: the two in `tests/ui_contracts/test_ui_lint.py` (eslint at zero
 warnings), the typescript node in `tests/ui_server/test_dashboard_contract.py`
 (`tsc --noEmit`) and the vitest node in `tests/orchestration/test_test_runner.py`, which runs
 the UI's whole unit suite and so this round's test files. Report every `SKIPPED` line the `-rs`
 summary prints. Then `python3 -m apps.cli.main integrity check --json`, which must read all six
 checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f020-r3-mut <C4>`, then
 `python3 -B .remedy-wt/f020-r3-payloads/mutations.py
 /home/decodeux/Repos/remedy/.remedy-wt/f020-r3-mut` and report its whole output. For each
 mutation the tool runs vitest over the WORKTREE's five `.test.ts` files this round touches or
 adds, from the primary `apps/ui` with a scratch config under `.remedy-wt/f020-r3-mutscratch/`,
 and pytest over the worktree's two Python contract files; it asserts each FROM occurs exactly
 once, restores the bytes, and runs an unmutated control first and last. The reviewer read, over
 the same tool against its sim tree (v = vitest failed, g = contract tests failed, each red at
 exit 1 wherever its count is not 0):
 control first vitest 51 passed and contract tests 13 passed, both at exit 0;
 m1 (the kind rows ignore the module they are given) v1 g0;
 m2 (a kind row carries its fill path as its stroke) v1 g0;
 m3 (a state row's mark takes another mark's path) v1 g0;
 m4 (tokenVar writes the bare token) v1 g0;
 m5 (the matrix columns run in reverse state order) v1 g0;
 m6 (the matrix grows a core row) v3 g0;
 m7 (the matrix paints at a zoom that hides run glyphs) v1 g0;
 m8 (a cluster cell carries no count) v1 g0;
 m9 (the painter writes any kind's label) v1 g0;
 m10 (the count is written in the fill colour) v1 g0;
 m11 (the count's font names no resolved family) v1 g0;
 m12 (the count's font leaves the palette) v2 g0;
 m13 (the layout gives a cluster no label) v1 g0;
 m14 (the cluster label drops its plus sign) v1 g0;
 m15 (the legend draws a path literal of its own) v0 g1;
 m16 (the legend paints a colour that is not a token) v0 g1;
 m17 (the legend writes a kind's name by hand) v0 g1;
 m18 (the legend no longer closes on Escape) v0 g1;
 m19 (the stage no longer mounts the legend) v0 g1;
 control last as first; every `restored byte-identical` reading True, and the final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`.
 Then `git worktree remove --force .remedy-wt/f020-r3-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 10`, which must show C5, C4, C3, C2, C1e, C1d, C1c, C1b, C1a and
 `1d954ef5` in that order; `git worktree list`, which must show the primary checkout and the
 worktrees constraint 6 names, and nothing else; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F020, round 3, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 3, then T003 — transition and pulse motion with visibility pausing, the conformance
assertions over the matrix fixture's pixels, and the live fixture pass on a streamed fake job.
State the open-findings count, 1, and the operator-questions count, 3.

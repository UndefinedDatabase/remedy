STEP F020 R1 — CLAIM F020 AND LAND T001: one glyph source per node kind, one state table in tokens, and the token guard

GOAL
Pull request 276 is merged; `main` is at `955a6240` and F020 is the next unchecked line. Cut its
branch, claim it, re-head the live review record, book F284's round 4 verdict, record DECISION
F020 D1, and land T001: `apps/ui/src/components/graph/renderers/glyphPaths.ts`, every node kind's
glyph as SVG path strings from which the canvas builds its Path2D, and `nodeStates.ts`, every node
state's treatment naming design tokens only; the two tokens they need; their vitest tests; and
the token guard `tests/ui_contracts/test_node_glyph_tokens.py`, with red proofs.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f020-r1-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f020-r1/`           READ-ONLY. The reviewer's block and scripts.
  `.remedy-wt/f020-r1-sim/`       The reviewer's simulated tree; do not touch it.
  `.remedy-wt/f020-r1-dry/`       The reviewer's authoring tree; do not touch it.
  `.remedy-wt/f020-r1-worker/`    YOURS for logs and scripts; create it if absent. All five are
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
   `git status --porcelain` must be empty, `git branch --show-current` must read `main`, and
   `git log --oneline -1` must read `955a6240`. Report all three. Then
   `git checkout -b feature/f020-node-lifecycle-glyph-language` and report the branch. Do NOT
   pull: the Open PR Gate ran before you and `main` is already at the merge commit.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f020-r1/block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f020-r1-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| claim.diff | 127 | 15248 | 9597baf5746e1586792d9c69a2f72c7d8b9e8ad3ec7845af805dd416faf7fd46 |
| context.md | 38 | 1676 | cb92943f462e868eb1dbc33943d594536b30a16bf48248ae5a396c0f3e7c7b4a |
| glyphPaths.test.ts | 225 | 8816 | b60ecd4aecba5d2a840bf07ed368d99b2d8fa7e35e739ccb4056aa9250968699 |
| glyphPaths.ts | 181 | 6541 | 4c440b9217718edff780fddac75e8a413fd86bdf52104ad4c2e74dc8a348c8e2 |
| mutations.py | 182 | 9233 | ddb9db2dc73e2165913b7d861e2696a3bd30fd836629c75ca127b2094456e5a4 |
| nodeStates.test.ts | 129 | 5165 | 34063c8af201ff4f7832d81a439abab0ebf1364bc2edbdfb3688a8b34ab3c885 |
| nodeStates.ts | 156 | 5831 | 74b81d8f8d4cec4be3e6e375d96fb2fa4bb12813a04e48942eab82a9c5e21316 |
| plan.md | 33 | 1317 | 5e20ffbf9c71497548e91949ee7a739ae15db35a153cbc25a7897a712debc386 |
| test_node_glyph_tokens.py | 110 | 4719 | e7daf334a6d45461a6646f1cf62a65794362a8bc60a24f071b1c83e9f215e5db |
| tokens.diff | 41 | 2186 | 13160072813b7ca734b3eb98f7c3426749b45cd792d3eb123b3d2e46239d8f1e |

`plan.md` and `context.md` are REWRITES of `.agent/plan.md` and `.agent/context.md`. The two
module payloads and the two `.test.ts` payloads are NEW FILES under
`apps/ui/src/components/graph/renderers/` (a new directory), and `test_node_glyph_tokens.py` is a
NEW FILE under `tests/ui_contracts/`, each copied whole. `claim.diff` and `tokens.diff` go on
with `git apply`; the reviewer generated both with `git diff HEAD` from a tree at `955a6240` into
which it wrote the edits. `claim.diff` edits `.agent/live_review.md` (the re-head, then F284's
round 4 gate entry appended), `docs/roadmap/STATUS.md` (F020's line `[ ]` to `[~]`) and
`.agent/decisions.md` (DECISION F020 D1 appended). `tokens.diff` adds `--remedy-state-vetoed` and
`--remedy-graph-node-ring` to `apps/ui/src/styles/tokens.css`, `--remedy-state-vetoed` to
`docs/ui/design_reference/tokens.css`, and its two lines to
`docs/ui/design_reference/tokens_rules.md`. `mutations.py` is a TOOL for G5: it is run, never
applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C1e, C2, C3, C4 and C5, in this order.

C1a — copy this block and the state payloads
  `.agent/authored/f020-r1-block.md` := this block, and `.agent/authored/f020-r1-plan.md` and
  `.agent/authored/f020-r1-context.md` := plan.md and context.md. All by `shutil.copyfile`.
  Subject: `F020 R1 C1a: copy round 1 block and state payloads into .agent/authored/`
  Its insertions are this block's line count plus 71. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C1b — copy the two diffs
  `.agent/authored/f020-r1-claim.diff` := claim.diff, `.agent/authored/f020-r1-tokens.diff` :=
  tokens.diff.
  Subject: `F020 R1 C1b: copy round 1 claim and token diffs into .agent/authored/`
  Expected insertions: 168.

C1c — copy the mutation tool
  `.agent/authored/f020-r1-mutations.py` := mutations.py.
  Subject: `F020 R1 C1c: copy round 1 mutation tool into .agent/authored/`
  Expected insertions: 182.

C1d — copy the product payloads
  `.agent/authored/f020-r1-glyphPaths.ts` and `.agent/authored/f020-r1-nodeStates.ts`.
  Subject: `F020 R1 C1d: copy round 1 product modules into .agent/authored/`
  Expected insertions: 337.

C1e — copy the test payloads
  `.agent/authored/f020-r1-glyphPaths.test.ts`, `.agent/authored/f020-r1-nodeStates.test.ts` and
  `.agent/authored/f020-r1-test_node_glyph_tokens.py`.
  Subject: `F020 R1 C1e: copy round 1 test payloads into .agent/authored/`
  Expected insertions: 464.

C2 — THE CLAIM AND ITS RECORDS, in this order:
   1. `git apply` claim.diff
   2. rewrite `.agent/plan.md` := plan.md
   3. rewrite `.agent/context.md` := context.md
  Subject: `F020 R1 C2: claim F020, re-head the live review record, book F284 R4, record D1`
  Expected insertions by `git show --numstat`: 13 context.md, 56 decisions.md, 28
  live_review.md, 20 plan.md, 1 STATUS.md.

C3 — THE PRODUCT: `git apply` tokens.diff, then copy glyphPaths.ts and nodeStates.ts into
  `apps/ui/src/components/graph/renderers/`, then `git add` both — an untracked module fails
  `integrity check`'s `relevant_untracked`.
  Subject: `F020 R1 C3: draw every node kind from one glyph source and every state from tokens`
  Expected insertions: 181 glyphPaths.ts, 156 nodeStates.ts, 5 apps/ui/src/styles/tokens.css,
  1 docs/ui/design_reference/tokens.css, 2 docs/ui/design_reference/tokens_rules.md.

C4 — THE TESTS: copy glyphPaths.test.ts and nodeStates.test.ts into
  `apps/ui/src/components/graph/renderers/` and test_node_glyph_tokens.py into
  `tests/ui_contracts/`, and `git add` all three.
  Subject: `F020 R1 C4: pin the glyph goldens, the state language and the token guard`
  Expected insertions: 225 glyphPaths.test.ts, 129 nodeStates.test.ts, 110
  test_node_glyph_tokens.py.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F020 R1 C5: rewrite handoff for round 1`
  Then `git push -u origin feature/f020-node-lifecycle-glyph-language`. Do NOT create a pull
  request: the branch opens one at F020's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f020-r1-*` copies,
   `.agent/live_review.md`, `docs/roadmap/STATUS.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `.agent/context.md`, `apps/ui/src/styles/tokens.css`, `docs/ui/design_reference/tokens.css`,
   `docs/ui/design_reference/tokens_rules.md`, the four files under
   `apps/ui/src/components/graph/renderers/` that the payloads name,
   `tests/ui_contracts/test_node_glyph_tokens.py`, and `.agent/handoff.md`. Report the list you
   measure with `git diff --name-only 955a6240 HEAD` after C5. Do NOT touch
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md`, `README.md`,
   `apps/ui/src/components/graph/ForceBrainGraph.tsx` or `docs/roadmap/features/T5_F020.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main` after the
   branch is cut, no branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, the reviewer's worktrees
   (`.remedy-wt/f020-r1-sim`, `.remedy-wt/f020-r1-dry` and the older `.remedy-wt/f015-r*` and
   `.remedy-wt/f284-r*` ones), and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that step's last action, and `git worktree list` is reported
   afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F020's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f020-r1-*` copy byte for byte
 with its source (the block copy against `.remedy-wt/f020-r1/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE CLAIM — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, which its builder printed from the simulated tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 288899 | 2a3e1c928766677821aff55f37cefaf6128dccda1672a51b0be86c4743b9cecb |
 | docs/roadmap/STATUS.md | 51033 | def827f05e4cf8a0d569a793db20324df78e293ce539b890677777cd1d541e6c |
 | .agent/decisions.md | 2029556 | 774b744d0a0007770aedc48fcef3f0856440f9a7879a565245aa0d08161a5e12 |
 | .agent/plan.md | 1317 | 5e20ffbf9c71497548e91949ee7a739ae15db35a153cbc25a7897a712debc386 |
 | .agent/context.md | 1676 | cb92943f462e868eb1dbc33943d594536b30a16bf48248ae5a396c0f3e7c7b4a |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `955a6240` and at C2 (the reviewer
 read R-1008 alone at both); F020's STATUS line at C2 read back in full, which must read
 `- [~] F020 — Node lifecycle & glyph language`; and `git diff --name-only <C1e> <C2>`, which
 must name exactly the paths of the table above.

G3 THE PRODUCT AND THE TESTS — the sha256 of each file below, read with `git show` at the commit
 named, equals the reviewer's reading from the simulated tree:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C3 | apps/ui/src/styles/tokens.css | 4224 | 58c22798a2a1f12ba65d08986349d96b0e43f330479e5749ff138490d4e7bbf9 |
 | C3 | docs/ui/design_reference/tokens.css | 7109 | 912c39cb4d7e8a11e9bc2819a0f0dac09294ae89741d2c6417de5b37302d52a5 |
 | C3 | docs/ui/design_reference/tokens_rules.md | 3158 | d0ef701deb923f1c74ef7e4cf9daa5a3b8f9a9b1b676e8fda7d14c0ef00962b5 |
 | C3 | apps/ui/src/components/graph/renderers/glyphPaths.ts | 6541 | 4c440b9217718edff780fddac75e8a413fd86bdf52104ad4c2e74dc8a348c8e2 |
 | C3 | apps/ui/src/components/graph/renderers/nodeStates.ts | 5831 | 74b81d8f8d4cec4be3e6e375d96fb2fa4bb12813a04e48942eab82a9c5e21316 |
 | C4 | apps/ui/src/components/graph/renderers/glyphPaths.test.ts | 8816 | b60ecd4aecba5d2a840bf07ed368d99b2d8fa7e35e739ccb4056aa9250968699 |
 | C4 | apps/ui/src/components/graph/renderers/nodeStates.test.ts | 5165 | 34063c8af201ff4f7832d81a439abab0ebf1364bc2edbdfb3688a8b34ab3c885 |
 | C4 | tests/ui_contracts/test_node_glyph_tokens.py | 4719 | e7daf334a6d45461a6646f1cf62a65794362a8bc60a24f071b1c83e9f215e5db |
 Also `git diff --name-only <C2> <C3>` and `<C3> <C4>`, which must name exactly the paths C3 and
 C4 list; and `python3 -m ruff check tests/ui_contracts/test_node_glyph_tokens.py` at C4.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path, serially, inside its sim tree
 carrying C2 to C4 and read `1435 passed, 10 skipped` at real exit code 0. FOUR of those skips
 are toolchain nodes a worktree cannot run and the primary checkout can, and each must PASS in
 your run, not skip: the two in `tests/ui_contracts/test_ui_lint.py` (eslint at zero
 warnings), the typescript node in `tests/ui_server/test_dashboard_contract.py`
 (`tsc --noEmit`) and the vitest node in `tests/orchestration/test_test_runner.py`, which runs
 the UI's whole unit suite and so the two new test files. Report every `SKIPPED` line the `-rs`
 summary prints. Then `python3 -m apps.cli.main integrity check --json`, which must read all six
 checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f020-r1-mut <C4>`, then
 `python3 -B .remedy-wt/f020-r1-payloads/mutations.py
 /home/decodeux/Repos/remedy/.remedy-wt/f020-r1-mut` and report its whole output. For each
 mutation the tool runs vitest over the WORKTREE's two `.test.ts` files from the primary
 `apps/ui` with a scratch config under `.remedy-wt/f020-r1-mutscratch/`, and pytest over the
 worktree's token guard; it asserts each FROM occurs exactly once, restores the bytes, and runs an
 unmutated control first and last. The reviewer read, over the same tool against its sim tree
 (v = vitest failed, g = guard failed, each red at exit 1 wherever its count is not 0):
 control first vitest 31 passed and guard 6 passed, both at exit 0;
 m1 (the builder glyph's geometry drifts) v1 g0;
 m2 (the flask's declared bounds stop short of its base) v1 g0;
 m3 (glyphPath2D rebuilds its paths on every call) v1 g0;
 m4 (the canvas stroke is built from the fill string) v1 g0;
 m5 (run glyphs show from a lower zoom than L1) v1 g0;
 m6 (glyphTransform scales the box to the radius, not the diameter) v1 g0;
 m7 (a failed node loses its status dot) v3 g0;
 m8 (a veto no longer dims what hangs below it) v1 g0;
 m9 (a planned node is drawn full size) v2 g0;
 m10 (reduced motion still pulses) v1 g0;
 m11 (the in-progress state is painted with the open token) v1 g1;
 m12 (the vetoed state names a token the sheet never declares) v2 g1;
 m13 (the pulse constant drifts from --remedy-dur-pulse) v1 g1;
 m14 (a raw colour literal enters the state module) v0 g1;
 m15 (the app sheet's vetoed grey drifts from the reference) v0 g1;
 m16 (the glyph module's header misquotes the precedence rule) v0 g1;
 control last as first; every `restored byte-identical` reading True, and the final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`.
 Then `git worktree remove --force .remedy-wt/f020-r1-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 10`, which must show C5, C4, C3, C2, C1e, C1d, C1c, C1b, C1a and
 `955a6240` in that order; `git worktree list`, which must show the primary checkout and the
 worktrees constraint 6 names, and nothing else; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F020, round 1, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 1, then T002 — the canvas painter reading both modules in place of F019's glyph slots
through the palette bridge `renderers/palette.ts`, the legend generated from the same source,
and the kind-by-state matrix fixture. State the open-findings count, 1, and the
operator-questions count, 3.

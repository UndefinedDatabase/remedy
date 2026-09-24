STEP F020 R2 — T002 FIRST HALF: the palette bridge, one node painter from the glyph and state modules, and the canvas wired to it

GOAL
Book round 1's PASS and record DECISION F020 D2, then land the first half of T002:
`apps/ui/src/components/graph/renderers/palette.ts`, which resolves every token the painter reads
once per mount; `renderers/paintNode.ts`, which paints every non-core node from its kind's glyph
and its state's treatment and holds no colour, shape or state rule of its own; the state table's
glyph ink and body-line colours in `renderers/nodeStates.ts`; and `ForceBrainGraph.tsx` painting
every non-core kind through the painter in place of F019's placeholder sphere, with the token
guard pinning that wiring. With tests and red proofs.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f020-r2-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f020-r2/`           READ-ONLY. The reviewer's block and scripts.
  `.remedy-wt/f020-r2-sim/`       The reviewer's simulated tree; do not touch it.
  `.remedy-wt/f020-r2-dry/`       The reviewer's authoring tree; do not touch it.
  `.remedy-wt/f020-r2-worker/`    YOURS for logs and scripts; create it if absent. All five are
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
   `06d185c6`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f020-r2/block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f020-r2-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| book.diff | 61 | 9624 | 756f6e8b8a856a36c9bc8d99d8887f42f2d7409fc05f28819f5e07aec97cd763 |
| mutations.py | 181 | 9454 | 9d77bca61444f306536bf571c1675c448c86293bc13d15c4ed062a764a9ce6c5 |
| paintNode.test.ts | 206 | 9071 | 8fdbfc95754e45c1535582de5b22ad9d45e07f99cbefc48215eaa2f76c282add |
| paintNode.ts | 132 | 5450 | 5fe0bf691ba79df127b4fa3c444c4b4fb94317468d15a956274f3e86c14313bc |
| palette.test.ts | 26 | 1207 | 2f019b3a80a234d30d887636d46e1a857fe1fda6938aaefbaffe43e68c89e604 |
| palette.ts | 45 | 2048 | 0059fca296472cb660a26b809933054d365d0cf9aebfd78ab1de9babe0e8be7e |
| plan.md | 34 | 1325 | 60d57a350b0e0f8c93b4115df553e07d6bb0b6e81a8d048dffde0bb23cf2d88e |
| product.diff | 268 | 13052 | 5ab9a90a27d3faa1ee13b50002adbea53febd8e70016dde78e67ac62c4b889c6 |
| tests.diff | 88 | 4781 | 66c15fe332b73ca51264c37f6b684404f2d42aac1a6dbbd5387d7fe080140040 |

`plan.md` is a REWRITE of `.agent/plan.md`. `palette.ts`, `paintNode.ts`, `palette.test.ts` and
`paintNode.test.ts` are NEW FILES under `apps/ui/src/components/graph/renderers/`, each copied
whole. The three diffs go on with `git apply`; the reviewer generated each with `git diff HEAD`
from a tree at `06d185c6` into which it wrote the edits. `book.diff` appends round 1's gate entry
to `.agent/live_review.md` and DECISION F020 D2 to `.agent/decisions.md`. `product.diff` edits
`apps/ui/src/components/graph/ForceBrainGraph.tsx` and `renderers/nodeStates.ts`. `tests.diff`
edits `renderers/nodeStates.test.ts` and `tests/ui_contracts/test_node_glyph_tokens.py`.
`mutations.py` is a TOOL for G5: it is run, never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C1e, C2, C3, C4 and C5, in this order.

C1a — copy this block and the plan payload
  `.agent/authored/f020-r2-block.md` := this block, `.agent/authored/f020-r2-plan.md` := plan.md.
  Both by `shutil.copyfile`.
  Subject: `F020 R2 C1a: copy round 2 block and plan payload into .agent/authored/`
  Its insertions are this block's line count plus 34. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C1b — copy the three diffs
  `.agent/authored/f020-r2-book.diff`, `.agent/authored/f020-r2-product.diff` and
  `.agent/authored/f020-r2-tests.diff`.
  Subject: `F020 R2 C1b: copy round 2 diffs into .agent/authored/`
  Expected insertions: 417.

C1c — copy the mutation tool
  `.agent/authored/f020-r2-mutations.py` := mutations.py.
  Subject: `F020 R2 C1c: copy round 2 mutation tool into .agent/authored/`
  Expected insertions: 181.

C1d — copy the new product modules
  `.agent/authored/f020-r2-palette.ts` and `.agent/authored/f020-r2-paintNode.ts`.
  Subject: `F020 R2 C1d: copy round 2 product modules into .agent/authored/`
  Expected insertions: 177.

C1e — copy the new test files
  `.agent/authored/f020-r2-palette.test.ts` and `.agent/authored/f020-r2-paintNode.test.ts`.
  Subject: `F020 R2 C1e: copy round 2 test payloads into .agent/authored/`
  Expected insertions: 232.

C2 — THE BOOKKEEPING, in this order: `git apply` book.diff, then rewrite `.agent/plan.md` :=
  plan.md.
  Subject: `F020 R2 C2: book round 1's PASS, record D2, advance the plan`
  Expected insertions by `git show --numstat`: 43 decisions.md, 2 live_review.md, 8 plan.md.

C3 — THE PRODUCT: `git apply` product.diff, then copy palette.ts and paintNode.ts into
  `apps/ui/src/components/graph/renderers/` and `git add` both — an untracked module fails
  `integrity check`'s `relevant_untracked`.
  Subject: `F020 R2 C3: paint every non-core node from the glyph and state modules in a resolved palette`
  Expected insertions: 40 ForceBrainGraph.tsx, 23 nodeStates.ts, 132 paintNode.ts, 45 palette.ts.

C4 — THE TESTS: `git apply` tests.diff, then copy palette.test.ts and paintNode.test.ts into
  `apps/ui/src/components/graph/renderers/` and `git add` both.
  Subject: `F020 R2 C4: pin the painter, the palette bridge, the glyph ink and the canvas wiring`
  Expected insertions: 17 nodeStates.test.ts, 206 paintNode.test.ts, 26 palette.test.ts, 28
  test_node_glyph_tokens.py.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F020 R2 C5: rewrite handoff for round 2`
  Then `git push origin feature/f020-node-lifecycle-glyph-language`. Do NOT create a pull
  request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f020-r2-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `apps/ui/src/components/graph/ForceBrainGraph.tsx`, the six files under
   `apps/ui/src/components/graph/renderers/` that C3 and C4 name,
   `tests/ui_contracts/test_node_glyph_tokens.py`, and `.agent/handoff.md`. Report the list you
   measure with `git diff --name-only 06d185c6 HEAD` after C5. Do NOT touch `.agent/context.md`,
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md`, `README.md`,
   `docs/roadmap/STATUS.md` or `docs/roadmap/features/T5_F020.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch
   deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, the reviewer's worktrees
   (`.remedy-wt/f020-r1-sim`, `.remedy-wt/f020-r1-dry`, `.remedy-wt/f020-r2-sim`,
   `.remedy-wt/f020-r2-dry` and the older `.remedy-wt/f015-r*` and `.remedy-wt/f284-r*` ones), and
   every existing stash alone. The worktree G5 adds goes under `.remedy-wt/`, is removed as that
   step's last action, and `git worktree list` is reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F020's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f020-r2-*` copy byte for byte
 with its source (the block copy against `.remedy-wt/f020-r2/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE BOOKKEEPING — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, which its builder printed from the simulated tree:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/live_review.md | 290916 | f7b088ac3f7677c3f33edc88aa56f5b35cd44a5601e051c7945e95bf23bdc65e |
 | C2 | .agent/decisions.md | 2033260 | d4910bc8630f45ebfb3817b4b6cdd3685e200658fd4a1e26a25dbc9c226d3f79 |
 | C2 | .agent/plan.md | 1325 | 60d57a350b0e0f8c93b4115df553e07d6bb0b6e81a8d048dffde0bb23cf2d88e |
 Also: the number of lines C2's diff of `.agent/live_review.md` adds that begin
 `Gate: F020 R1 — ` (the reviewer read 1); the open set by distinct id, computed with
 `open_finding_ids` from `scripts/rotate_live_review.py` over the file's TEXT at C2 (the reviewer
 read R-1008 alone); and `git diff --name-only <C1e> <C2>`, which must name exactly the paths of
 the table above.

G3 THE PRODUCT AND THE TESTS — the sha256 of each file below, read with `git show` at the commit
 named, equals the reviewer's reading from the simulated tree:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C3 | apps/ui/src/components/graph/ForceBrainGraph.tsx | 13868 | 4fa15823837f45dd142f7d06b0bbd4c88bd73e3915178338b563c7975572aeff |
 | C3 | apps/ui/src/components/graph/renderers/nodeStates.ts | 6770 | de1a08c87eb9dfcf1b3004fd78da1d97a483153c5edab9d67a8996b6f5ad7b58 |
 | C3 | apps/ui/src/components/graph/renderers/palette.ts | 2048 | 0059fca296472cb660a26b809933054d365d0cf9aebfd78ab1de9babe0e8be7e |
 | C3 | apps/ui/src/components/graph/renderers/paintNode.ts | 5450 | 5fe0bf691ba79df127b4fa3c444c4b4fb94317468d15a956274f3e86c14313bc |
 | C4 | apps/ui/src/components/graph/renderers/nodeStates.test.ts | 5947 | e7102241a14d818001d2318c4b3b254dd8160d613278086e31776c7a6faae1c5 |
 | C4 | tests/ui_contracts/test_node_glyph_tokens.py | 6134 | f96925c2e51f7267b891f7ec3636597298bb94c0670dec7649e6b4c5df05b442 |
 | C4 | apps/ui/src/components/graph/renderers/palette.test.ts | 1207 | 2f019b3a80a234d30d887636d46e1a857fe1fda6938aaefbaffe43e68c89e604 |
 | C4 | apps/ui/src/components/graph/renderers/paintNode.test.ts | 9071 | 8fdbfc95754e45c1535582de5b22ad9d45e07f99cbefc48215eaa2f76c282add |
 Also `git diff --name-only <C2> <C3>` and `<C3> <C4>`, which must name exactly the paths C3 and
 C4 list; and `python3 -m ruff check tests/ui_contracts/test_node_glyph_tokens.py` at C4.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py tests/regression/test_named_bugs.py tests/test_agent_tooling.py tests/cli/test_golden_path.py 2>&1 | tail -20; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path, serially, inside its sim tree
 carrying C2 to C4 and read `1118 passed, 16 skipped` at real exit code 0. FOUR of those skips
 are toolchain nodes a worktree cannot run and the primary checkout can, and each must PASS in
 your run, not skip: the two in `tests/ui_contracts/test_ui_lint.py` (eslint at zero
 warnings), the typescript node in `tests/ui_server/test_dashboard_contract.py`
 (`tsc --noEmit`) and the vitest node in `tests/orchestration/test_test_runner.py`, which runs
 the UI's whole unit suite and so this round's test files. Report every `SKIPPED` line the `-rs`
 summary prints. Then `python3 -m apps.cli.main integrity check --json`, which must read all six
 checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f020-r2-mut <C4>`, then
 `python3 -B .remedy-wt/f020-r2-payloads/mutations.py
 /home/decodeux/Repos/remedy/.remedy-wt/f020-r2-mut` and report its whole output. For each
 mutation the tool runs vitest over the WORKTREE's four `.test.ts` files under `renderers/` from
 the primary `apps/ui` with a scratch config under `.remedy-wt/f020-r2-mutscratch/`, and pytest
 over the worktree's token guard; it asserts each FROM occurs exactly once, restores the bytes,
 and runs an unmutated control first and last. The reviewer read, over the same tool against its
 sim tree (v = vitest failed, g = guard failed, each red at exit 1 wherever its count is not 0):
 control first vitest 50 passed and guard 8 passed, both at exit 0;
 m1 (the halo is drawn at full alpha) v1 g0;
 m2 (the painter ignores the state's size factor) v1 g0;
 m3 (a run's glyph is drawn at every zoom) v1 g0;
 m4 (the state marks are never drawn) v3 g0;
 m5 (a mark's outline is never drawn) v2 g0;
 m6 (the artifact is drawn as a sphere) v3 g0;
 m7 (the sphere's gloss starts from the fill, not the highlight) v1 g0;
 m8 (a token that resolves to nothing is not named) v1 g0;
 m9 (a resolved value keeps the stylesheet's whitespace) v2 g0;
 m10 (the canvas paints builder runs with the core's painter) v0 g1;
 m11 (the palette is resolved again on every layout) v0 g1;
 m12 (the canvas passes a fixed zoom to the painter) v0 g1;
 m13 (a raw colour literal enters the painter) v0 g1;
 m14 (the canvas paints a state colour of its own again) v0 g1;
 m15 (a planned glyph is inked in the planned white) v3 g0;
 m16 (the sphere glyph is stroked in the highlight, not the state's ink) v1 g0;
 m17 (a shape kind is lined in its fill colour) v1 g0;
 control last as first; every `restored byte-identical` reading True, and the final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`.
 Then `git worktree remove --force .remedy-wt/f020-r2-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 10`, which must show C5, C4, C3, C2, C1e, C1d, C1c, C1b, C1a and
 `06d185c6` in that order; `git worktree list`, which must show the primary checkout and the
 worktrees constraint 6 names, and nothing else; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F020, round 2, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 2, then T002's second half — the legend popover from the graph's chrome, enumerated from
the glyph and state modules, the cluster's count, and the kind-by-state matrix fixture. State
the open-findings count, 1, and the operator-questions count, 3.

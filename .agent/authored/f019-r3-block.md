STEP F019 R3 — BOOK ROUND 2 AND MOUNT THE LIVE RENDERER: the stage paints the reducer's model, and the SVG picture becomes the simple view

GOAL
Book round 2's PASS, record DECISION F019 D3 and operator note Q3, and land the first part of
T002's painted half: the new pure module `apps/ui/src/components/graph/brainView.ts`, the rewritten
`ForceBrainGraph.tsx` that paints `buildBrainLayout`'s output, and a `BrainGraphStage.tsx` that
mounts it by default and keeps `BrainGraphCanvas.tsx` as the simple view, with vitest tests, a
source guard and red proofs.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f019-r3-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f019-r3/`           READ-ONLY. The reviewer's block, texts and builder.
  `.remedy-wt/f019-r3-sim/`, `.remedy-wt/f019-r3-proto/`, `.remedy-wt/f019-r3-helper/`
                                  The reviewer's trees and tools; do not touch.
  `.remedy-wt/f019-r3-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, `cd <dir> && git ...`, and multi-operation
one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe pytest.
Use `git -C <path>` rather than `cd`. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`). A heredoc containing a dollar-brace or an f-string brace is refused:
write such a script to a file under your own directory and run the file. Never run npm or npx.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f019-live-node-materialization`, and `git log --oneline -1` must read `fd976586`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f019-r3/block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.

PAYLOADS — under `.remedy-wt/f019-r3-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 106 | 12760 | 268e5cdb6eca78f2e580ad53e6e101bbde81ba0d73abed4bf07a725150a3005a |
| plan.md | 37 | 1495 | 80ac140ae3a98e9ed83530f313ea10639f9224906ce28d4106a7da9ad48facf7 |
| renderer.diff | 467 | 20766 | 2f63160e5083507d5233bab7ecbc274a9b2bbeddd1e45a659305cfc05fc0a207 |
| product.diff | 252 | 12490 | ae15a39f9445ef74b31f5dbee0f57333010b114b89335ebbfac610c65441a98f |
| tests.diff | 350 | 13864 | 706881818b66022c0347298113a374c5e5d79f4ee9c42914b05b7006031333fe |
| mutations.py | 331 | 13896 | cbc4242f3b7f83315efe2cc18dcee311b69f3402af78be6027ce5bd815dd76ad |

`plan.md` is a REWRITE of `.agent/plan.md`. The four `.diff` files go on with `git apply`; the
reviewer generated each with `git diff` from a tree at `fd976586` into which its builder copied
the reviewed prototype. `records.diff` appends the `Gate: F019 R2 — ` entry to
`.agent/live_review.md`, DECISION F019 D3 to `.agent/decisions.md` and entry Q3 to
`.agent/operator_questions.md`. `renderer.diff` rewrites `ForceBrainGraph.tsx`. `product.diff`
creates `brainView.ts` and edits `BrainGraphStage.tsx`, `BrainGraphStage.module.css`,
`buildForceBrainModel.ts` and `apps/ui/src/types/react-force-graph-2d.d.ts`. `tests.diff` creates
`brainView.test.ts` and `tests/ui_contracts/test_brain_stage_mount.py`. `mutations.py` is a TOOL
for G5: it is run, never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C1e, C2, C3, C4 and C5, in this order.

C1a — `.agent/authored/f019-r3-block.md` := this block and `.agent/authored/f019-r3-plan.md` :=
  plan.md, by `shutil.copyfile`.
  Subject: `F019 R3 C1a: copy round 3 block and plan into .agent/authored/`
  Its insertions are this block's line count plus 37; STOP rather than commit if 500 or more.
C1b — `.agent/authored/f019-r3-records.diff` and `.agent/authored/f019-r3-product.diff`.
  Subject: `F019 R3 C1b: copy round 3 records and product diffs into .agent/authored/`
  Expected insertions: 358.
C1c — `.agent/authored/f019-r3-renderer.diff`.
  Subject: `F019 R3 C1c: copy round 3 renderer diff into .agent/authored/`
  Expected insertions: 467.
C1d — `.agent/authored/f019-r3-tests.diff`.
  Subject: `F019 R3 C1d: copy round 3 tests diff into .agent/authored/`
  Expected insertions: 350.
C1e — `.agent/authored/f019-r3-mutations.py`.
  Subject: `F019 R3 C1e: copy round 3 mutation tool into .agent/authored/`
  Expected insertions: 331.
C2 — THE BOOKING: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F019 R3 C2: book round 2's PASS, record DECISION F019 D3 and operator note Q3`
  Expected insertions by `git show --numstat`: 55 decisions.md, 2 live_review.md,
  25 operator_questions.md, 10 plan.md.
C3 — THE PRODUCT: `git apply` renderer.diff, then `git apply` product.diff, then `git add` the new
  `brainView.ts`.
  Subject: `F019 R3 C3: paint the reducer's model on the stage, keep the SVG picture as simple view`
  Expected insertions: 261 ForceBrainGraph.tsx, 132 brainView.ts, 40 BrainGraphStage.tsx,
  16 BrainGraphStage.module.css, 1 buildForceBrainModel.ts, 4 react-force-graph-2d.d.ts.
C4 — THE TESTS: `git apply` tests.diff, then `git add` the two new test files.
  Subject: `F019 R3 C4: pin the stage glue, the mount and the selection mapping`
  Expected insertions: 223 brainView.test.ts, 115 test_brain_stage_mount.py.
C5 — THE HANDBACK: `.agent/handoff.md`, rewritten, its own commit, per
  `docs/agents/handback_template.md`. Subject: `F019 R3 C5: rewrite handoff for round 3`. Then
  `git push origin feature/f019-live-node-materialization` and report its real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading.
3. The round's whole tracked path set is: the `.agent/authored/f019-r3-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/operator_questions.md`,
   `.agent/plan.md`, the files the renderer, product and test diffs name, and
   `.agent/handoff.md`. Report `git diff --name-only fd976586 HEAD` after C5.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr` command of any kind, no checkout of `main`, no branch
   deletion, no force-push, no `git stash`.
6. Leave every existing worktree, branch and stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that step's last action, and `git worktree list` is reported.
7. DO NOT run the full suite (amend0917 rule 1).

DONE-WHEN — every gate executed, every reading reported with its real exit code. "Green" as a
word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — each payload's line count, byte count and sha256 against the PAYLOADS table;
 then each `.agent/authored/f019-r3-*` copy byte for byte against its source (the block copy
 against `.remedy-wt/f019-r3/block.md`), read back with `git show <commit>:<path>`.

G2 THE BOOKING — at C2, read with `git show <C2>:<path>`, each equals the reviewer's simulated
 reading:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2005325 | a3b512551ff10e96413676aa3782f9a6f6db72d2ad7cda18cb028c8a3e4e9ffc |
 | .agent/live_review.md | 311422 | 447a154146f1ce0fe2071d27b1e4eb26764f72aa0bfe72f7a5037d685b85838b |
 | .agent/operator_questions.md | 5681 | 3c7f2c772af005e7bc961e6b086e73abf028da3e7603b817aaf0d119076b0aee |
 | .agent/plan.md | 1495 | 80ac140ae3a98e9ed83530f313ea10639f9224906ce28d4106a7da9ad48facf7 |
 Then the count of lines C2 adds to the ledger beginning `Gate: F019 R2 — `, which must be 1,
 and `open_finding_ids` of `scripts/rotate_live_review.py` over the ledger's text at `fd976586`
 and at C2, which the reviewer read as R-0499, R-0950, R-1008 and R-1046 at both.

G3 THE PRODUCT AND TESTS — at C4, read with `git show <C4>:<path>`, each equals the reviewer's
 simulated reading:
 | path | bytes | sha256 |
 |---|---|---|
 | apps/ui/src/components/graph/ForceBrainGraph.tsx | 14829 | a82f720018c171991ce35eeb17ef7c73fb9b8a44f8e9378835d7b9d4162067fb |
 | apps/ui/src/components/graph/brainView.ts | 6725 | bfb7b24d5ec21705f61242de85f23af1fdab695379c0a027583945f245334510 |
 | apps/ui/src/components/graph/BrainGraphStage.tsx | 2647 | acdd4c0cc49dbc839cdfdd95774781dabffc6f061c4469c2d05ec292447f434e |
 | apps/ui/src/components/graph/BrainGraphStage.module.css | 1087 | 58a86323b5ffc0daa11d073a44c16b212d6bc8e449593dcf21517cb40720fdb4 |
 | apps/ui/src/components/graph/buildForceBrainModel.ts | 13461 | 6df2cd42d5847a8c570d4b385f3a0556a04f017e074836be39c9852271df31aa |
 | apps/ui/src/types/react-force-graph-2d.d.ts | 2767 | 7eb3cd724698809ef8d441caef51dab11699b9c5db842da099d324707e032156 |
 | apps/ui/src/components/graph/brainView.test.ts | 8721 | 6cf9fa18922701340be7330571ba6936e2500fb35d4b0ce867f260daef5d5750 |
 | tests/ui_contracts/test_brain_stage_mount.py | 4327 | 0b78cacc4de86f7d666eb70b54ea7299578ca43f443b3f26d7f0cac8e8c5404f |

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path inside its sim tree and read
 `1370 passed, 10 skipped` at exit 0. The two eslint nodes of `tests/ui_contracts/test_ui_lint.py`,
 the tsc node of `tests/ui_server/test_dashboard_contract.py` and the vitest node of
 `tests/orchestration/test_test_runner.py` skip in a worktree and must PASS in your run. Report
 every `SKIPPED` line. Then `python3 -m ruff check tests/ui_contracts/test_brain_stage_mount.py`,
 real exit 0, and `python3 -m apps.cli.main integrity check --json`, which must read all six
 checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f019-r3-mut <C4>`, then
 `python3 -B .remedy-wt/f019-r3-payloads/mutations.py
 /home/decodeux/Repos/remedy/.remedy-wt/f019-r3-mut` and report its whole output. The reviewer
 read, over the same tool against its prototype tree, whose product and test files equal the
 G3 readings: vitest control `89 passed` and pytest control `19 passed`, both at exit 0, first
 and last; failed counts at exit 1 of V1 1, V2 1, V3 1, V4 1, V5 1, V6 1, V7 1, V8 2, V9 1,
 V10 1, V11 1, S1 2, S2 1 and S3 1; every mutation restored byte-identical, and the final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`. Then
 `git worktree remove --force .remedy-wt/f019-r3-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty; `git log --oneline
 -n 10`, which must show C5, C4, C3, C2, C1e, C1d, C1c, C1b, C1a and `fd976586` in that order;
 the push's real outcome; and `git worktree list`. These readings go in your reply.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertions you MEASURED beside the ones this
block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and the
next expected action. Your Session section reads SESSION 2 of feature F019, round 3, and says in
one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 3, then the rest of T002 as DECISION F019 D3 (7) names it: the old decorative dashboard
builder replaced with its source pins, and the demo recording. State the open-findings count, 4,
and the operator-questions count, 3.

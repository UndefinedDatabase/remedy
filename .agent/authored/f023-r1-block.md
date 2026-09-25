STEP F023 R1 — CLAIM F023 AND LAND T001: the pure semantic-zoom machine, its wheel adapter, their goldens and guard

GOAL
Pull request 277 is merged; `main` is at `441f4e8e` and F023 is the next unchecked line. Cut its
branch, claim it, re-head the live review record, book F020's round 8 verdict, record DECISION
F023 D1, and land T001: `apps/ui/src/components/graph/semanticZoom.ts`, the pure state machine
{level, focusId, tab} over L0 to L3, and `zoomWheel.ts`, the wheel adapter that holds the
hysteresis; their vitest goldens over the whole transition matrix; and the guard
`tests/ui_contracts/test_semantic_zoom_contract.py`, with red proofs.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f023-r1-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f023-r1/`           READ-ONLY. The reviewer's block and scripts.
  `.remedy-wt/f023-r1-sim/`       The reviewer's simulated tree; do not touch it.
  `.remedy-wt/f023-r1-dry/`       The reviewer's authoring tree; do not touch it.
  `.remedy-wt/f023-r1-worker/`    YOURS for logs and scripts; create it if absent. All five are
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
   `git log --oneline -1` must read `441f4e8e`. Report all three. Then
   `git checkout -b feature/f023-semantic-zoom-l0-l3` and report the branch. Do NOT pull: the
   Open PR Gate ran before you and `main` is already at the merge commit.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f023-r1/block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f023-r1-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| claim.diff | 172 | 17767 | 659cf8f1d1080926921e7c0cd007cb76dd536f0c390ccfa9fc1bfd83bd862ae0 |
| context.md | 39 | 1646 | 713a4568129bd9c528b77cf394cec3cbaace8e18a76b640b2a5e0a41ac58414d |
| mutations.py | 175 | 9085 | 07b35d4125539f752afaa5cf19c3c12a51a31e43a6980763f029ce376ac27ea7 |
| plan.md | 36 | 1424 | 0308117f152c80e1e9209794938242e80f7ef21d529eddd33631165fe4f0531f |
| semanticZoom.test.ts | 272 | 12686 | 51253e54709e6ff05ad5ba8dd06100f29af8208d2021a32676ac2e17ac96a131 |
| semanticZoom.ts | 214 | 9293 | 6bb4890fdb6e00d54b67c1b57d4d1bc2833fd382f1d283736bbc0d4708ea2ac7 |
| test_semantic_zoom_contract.py | 62 | 2773 | 9006b678df2a4d72a1383a33f21afc4ce80749b341abd4a51c957ae3aa3d8582 |
| zoomWheel.test.ts | 63 | 2816 | 1c15f3e7ed74bf2ec227e233ebefaabd6a26b14c09712724ce3c8350a0952f0c |
| zoomWheel.ts | 29 | 1566 | 7529d95b59e57e953be6446a7deab63c70911cda95f03785f7121286ad822ae2 |

`plan.md` and `context.md` are REWRITES of `.agent/plan.md` and `.agent/context.md`. The two
module payloads and the two `.test.ts` payloads are NEW FILES under
`apps/ui/src/components/graph/`, and `test_semantic_zoom_contract.py` is a NEW FILE under
`tests/ui_contracts/`, each copied whole. `claim.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `441f4e8e` into which it wrote the edits. It
edits `.agent/live_review.md` (the re-head, which replaces everything above the `## Findings`
heading line, then F020's round 8 gate entry appended), `docs/roadmap/STATUS.md` (F023's line
`[ ]` to `[~]`) and `.agent/decisions.md` (DECISION F023 D1 appended). `mutations.py` is a TOOL
for G5: it is run, never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C1e, C2, C3, C4 and C5, in this order.

C1a — copy this block and the state payloads
  `.agent/authored/f023-r1-block.md` := this block, and `.agent/authored/f023-r1-plan.md` and
  `.agent/authored/f023-r1-context.md` := plan.md and context.md. All by `shutil.copyfile`.
  Subject: `F023 R1 C1a: copy round 1 block and state payloads into .agent/authored/`
  Its insertions are this block's line count plus 75. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C1b — copy the claim diff
  `.agent/authored/f023-r1-claim.diff` := claim.diff.
  Subject: `F023 R1 C1b: copy round 1 claim diff into .agent/authored/`
  Expected insertions: 172.

C1c — copy the mutation tool
  `.agent/authored/f023-r1-mutations.py` := mutations.py.
  Subject: `F023 R1 C1c: copy round 1 mutation tool into .agent/authored/`
  Expected insertions: 175.

C1d — copy the product payloads
  `.agent/authored/f023-r1-semanticZoom.ts` and `.agent/authored/f023-r1-zoomWheel.ts`.
  Subject: `F023 R1 C1d: copy round 1 product modules into .agent/authored/`
  Expected insertions: 243.

C1e — copy the test payloads
  `.agent/authored/f023-r1-semanticZoom.test.ts`, `.agent/authored/f023-r1-zoomWheel.test.ts`
  and `.agent/authored/f023-r1-test_semantic_zoom_contract.py`.
  Subject: `F023 R1 C1e: copy round 1 test payloads into .agent/authored/`
  Expected insertions: 397.

C2 — THE CLAIM AND ITS RECORDS, in this order:
   1. `git apply` claim.diff
   2. rewrite `.agent/plan.md` := plan.md
   3. rewrite `.agent/context.md` := context.md
  Subject: `F023 R1 C2: claim F023, re-head the live review record, book F020 R8, record D1`
  Expected by `git show --numstat` (insertions and deletions): 15/14 context.md, 51/0 decisions.md, 28/55 live_review.md, 23/16 plan.md, 1/1 STATUS.md.

C3 — THE PRODUCT: copy semanticZoom.ts and zoomWheel.ts into `apps/ui/src/components/graph/`,
  then `git add` both — an untracked module fails `integrity check`'s `relevant_untracked`.
  Subject: `F023 R1 C3: add the semantic-zoom state machine and its wheel adapter`
  Expected insertions: 214 semanticZoom.ts, 29 zoomWheel.ts.

C4 — THE TESTS: copy semanticZoom.test.ts and zoomWheel.test.ts into
  `apps/ui/src/components/graph/` and test_semantic_zoom_contract.py into `tests/ui_contracts/`,
  and `git add` all three.
  Subject: `F023 R1 C4: golden the zoom transition matrix and guard the spec thresholds`
  Expected insertions: 272 semanticZoom.test.ts, 63 zoomWheel.test.ts, 62 test_semantic_zoom_contract.py.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F023 R1 C5: rewrite handoff for round 1`
  Then `git push -u origin feature/f023-semantic-zoom-l0-l3`. Do NOT create a pull request:
  the branch opens one at F023's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f023-r1-*` copies,
   `.agent/live_review.md`, `docs/roadmap/STATUS.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `.agent/context.md`, the four files under `apps/ui/src/components/graph/` that the payloads
   name, `tests/ui_contracts/test_semantic_zoom_contract.py`, and `.agent/handoff.md`. Report
   the list you measure with `git diff --name-only 441f4e8e HEAD` after C5. Do NOT touch
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md`, `README.md`,
   `apps/ui/src/components/graph/ForceBrainGraph.tsx` or `docs/roadmap/features/T5_F023.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main` after the
   branch is cut, no branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4 (`.remedy-wt/f023-r1-sim`, `.remedy-wt/f023-r1-dry` and the older
   `f015-*`, `f020-*` and `f284-*` ones), and every existing stash alone. The worktree G5 adds
   goes under `.remedy-wt/`, is removed as that step's last action, and `git worktree list` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F023's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f023-r1-*` copy byte for byte
 with its source (the block copy against `.remedy-wt/f023-r1/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE CLAIM — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, which its builder printed from the simulated tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 295718 | fd6ee039a2240cd15f7876bcb26b2db6667240470782ff993cc84720267a4868 |
 | docs/roadmap/STATUS.md | 51391 | 5cc4cafed1138ee7e07e046ff9bfc7b9bf9296ae6c65bbc77e2d58468d648a50 |
 | .agent/decisions.md | 2048114 | fbe2d18335b57c2ebd6cadc6a5caa23c49795422b92d3a1a1a8b463182b38a2d |
 | .agent/plan.md | 1424 | 0308117f152c80e1e9209794938242e80f7ef21d529eddd33631165fe4f0531f |
 | .agent/context.md | 1646 | 713a4568129bd9c528b77cf394cec3cbaace8e18a76b640b2a5e0a41ac58414d |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `441f4e8e` and at C2 (the reviewer
 read R-1008 alone at both); at C2 the ledger has exactly one line reading `## Findings` and
 exactly one reading `## Steps`, and its last line begins `Gate: F020 R8 — `; F023's STATUS
 line at C2 read back in full, which must read `- [~] F023 — Semantic zoom L0–L3`; and
 `git diff --name-only <C1e> <C2>`, which must name exactly the paths of the table above.

G3 THE PRODUCT AND THE TESTS — the sha256 of each file below, read with `git show` at the commit
 named, equals the reviewer's reading from the simulated tree:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C3 | apps/ui/src/components/graph/semanticZoom.ts | 9293 | 6bb4890fdb6e00d54b67c1b57d4d1bc2833fd382f1d283736bbc0d4708ea2ac7 |
 | C3 | apps/ui/src/components/graph/zoomWheel.ts | 1566 | 7529d95b59e57e953be6446a7deab63c70911cda95f03785f7121286ad822ae2 |
 | C4 | apps/ui/src/components/graph/semanticZoom.test.ts | 12686 | 51253e54709e6ff05ad5ba8dd06100f29af8208d2021a32676ac2e17ac96a131 |
 | C4 | apps/ui/src/components/graph/zoomWheel.test.ts | 2816 | 1c15f3e7ed74bf2ec227e233ebefaabd6a26b14c09712724ce3c8350a0952f0c |
 | C4 | tests/ui_contracts/test_semantic_zoom_contract.py | 2773 | 9006b678df2a4d72a1383a33f21afc4ce80749b341abd4a51c957ae3aa3d8582 |
 Also `git diff --name-only <C2> <C3>` and `<C3> <C4>`, which must name exactly the paths C3 and
 C4 list; and `python3 -m ruff check tests/ui_contracts/test_semantic_zoom_contract.py` at C4.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path, serially, inside its sim tree
 carrying C1a to C4 with this block's copy, and read `1450 passed, 10 skipped` at real exit code 0. FOUR of
 those skips are toolchain nodes a worktree cannot run and the primary checkout can, and each
 must PASS in your run, not skip: the two in `tests/ui_contracts/test_ui_lint.py` (eslint at
 zero warnings), the typescript node in `tests/ui_server/test_dashboard_contract.py`
 (`tsc --noEmit`) and the vitest node in `tests/orchestration/test_test_runner.py`, which runs
 the UI's whole unit suite and so the two new test files. Report every `SKIPPED` line the `-rs`
 summary prints. Then `python3 -m apps.cli.main integrity check --json`, which must read all six
 checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f023-r1-mut <C4>`, then
 `python3 -B .remedy-wt/f023-r1-payloads/mutations.py
 /home/decodeux/Repos/remedy/.remedy-wt/f023-r1-mut` and report its whole output. For each
 mutation the tool runs vitest over the WORKTREE's two `.test.ts` files from the primary
 `apps/ui` with a scratch config under `.remedy-wt/f023-r1-mutscratch/`, and pytest over the
 worktree's guard; it asserts each FROM occurs exactly once, restores the bytes, and runs an
 unmutated control first and last. The reviewer read, over the same tool against its sim tree
 (v = vitest failed, g = guard failed, each red at exit 1 wherever its count is not 0):
 control first vitest 109 passed and guard 4 passed, both at exit 0;
 m1 (Escape at L3 skips run detail) v3 g0;
 m2 (an empty transition returns a new object) v4 g0;
 m3 (the wheel leaves run detail) v8 g0;
 m4 (a run click opens its task, not the run) v9 g0;
 m5 (a deeper breadcrumb is not refused with its note) v4 g0;
 m6 (evidence opens from task focus) v3 g0;
 m7 (reconcile leaves a dangling focus) v3 g0;
 m8 (a later node list overwrites an earlier one) v1 g0;
 m9 (the run crumb is current at L3) v1 g0;
 m10 (a wheel crossing out walks back one level only) v2 g0;
 m11 (the machine imports React state) vitest exit 1 with its counts unparsed, printed as -1, g1;
 m12 (reaching 1.6 already zooms in) v2 g1;
 m13 (the dead band collapses: out at the in threshold) v6 g1;
 m14 (the in threshold drifts from graph_spec) v4 g1;
 m15 (a wheel-in over empty space still zooms in) v1 g0;
 control last as first; every `restored byte-identical` reading True, and the final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`.
 Then `git worktree remove --force .remedy-wt/f023-r1-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 10`, which must show C5, C4, C3, C2, C1e, C1d, C1c, C1b, C1a and
 `441f4e8e` in that order; `git worktree list`, which must show the primary checkout and the
 worktrees constraint 6 names, and nothing else; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F023, round 1, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 1, then T002's first half — the `useSemanticZoom.ts` hook driving the canvas from the
machine, the render effects (sibling dimming, branch glow, run fan-out), the breadcrumbs and
Escape. State the open-findings count, 1, and the operator-questions count, 3.

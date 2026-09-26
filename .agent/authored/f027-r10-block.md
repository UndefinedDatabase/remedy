STEP F027 R10 — THE CLOSURE SEQUENCE'S FIRST ROUND: book round 9, resolve R-1069 and R-1070, write the Built State, consolidate the checklist, ask the self-use generator for the closure's item, and take the feature's one full suite

GOAL
Book round 9's PASS and the resolutions of R-1069 and R-1070, append the Built State to
`docs/roadmap/features/T5_F027.md`, run the checklist consolidation pass (it joins nothing and keeps
`docs/agents/planner_reviewer_prompt.md` §3 at 34 items), ask the self-use generator for the closure's
item (closure precondition 6), and run this feature's ONE full suite on the tree that ships,
committing its transcript. The evidence bundle, the review package, the ledger rotation, the STATUS
line and the pull request belong to later rounds.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, write the handback. You never issue a
verdict, never merge, and never write a `Done:` line. Read first:
`docs/roadmap/STATUS_closure_protocol.md` preconditions 2, 3, 6 and 7, and
`docs/agents/integration_gate.md`.

THE DIRECTORIES
  `.remedy-wt/f027-r10-payloads/` and `.remedy-wt/f027-r10/`  READ-ONLY. The reviewer's.
  `.remedy-wt/f027-r10-drafts/`, `.remedy-wt/f027-r8-dry/`, `.remedy-wt/f027-r8-render/`,
  `.remedy-wt/f027-review/` and every older `f027-*` path: the reviewer's; do not touch them.
  `.remedy-wt/f027-r10-worker/`   YOURS for logs and scripts; create it if absent. All are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR: `VAR=x cmd`, `env VAR=x cmd`, `export VAR=x; cmd`,
`cp`, process and command substitution, `cd <dir> && git ...`, `for` loops, and one-liners chained
with `;` or `&&` outside a `bash -c`. Capture exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`,
read `${PIPESTATUS[0]}` when you pipe. Use `git -C <path>`; never `cd` into a worktree. Write any
script holding a dollar-brace or a brace-quote shape to a file under your own directory and run it.
The ONE npm command this round may run is C4's `npm --prefix apps/ui run build`; never `npm install`,
`npm ci` or `npx`. Never `git stash`, never `pkill -f`, never `git worktree prune`.

COMMIT TRAILER — every commit ends with exactly this line:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop.
2. In `/home/decodeux/Repos/remedy`: report `pwd`; `git status --porcelain` empty,
   `git branch --show-current` `feature/f027-task-veto`, `git log --oneline -1` `45cf5b9f`.
3. Measure this block's line count and sha256 (`.remedy-wt/f027-r10/block.md`) against your
   delegation message's readings; stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*'` as found.

PAYLOADS — under `.remedy-wt/f027-r10-payloads/`; verify each one's line count, byte count and sha256
BEFORE use and report every reading. Never retype or edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| closure_docs.diff | 117 | 9219 | f2fe14d7bc563a0cd64faec8b040b7813d0e5154ece8c96c13746f875e837ec4 |
| plan.md | 30 | 1127 | 6de8d94dd410c2ddfb98a0c0b33bbe8537c58fe05904316835cbc3bbeb284b84 |
| records.diff | 23 | 5784 | 2b6e01f37b675129c80107db4bf4c0680f103a151b8d0baade24f57b3f9b3745 |

`plan.md` REWRITES `.agent/plan.md`. `records.diff` (`git diff HEAD` from a tree at `45cf5b9f`)
appends round 9's gate entry and the `Done:` paragraphs of R-1069 and R-1070 to
`.agent/live_review.md`, and one line to `.agent/prose_slips.md`. `closure_docs.diff`, generated in the
same tree, appends the Built State to `docs/roadmap/features/T5_F027.md` and replaces, in
`docs/agents/planner_reviewer_prompt.md`, the line `  The next consolidation measures against 34.`
with the consolidation paragraph that ends with it (containment test: TO contains FROM: true — an
APPEND; the line occurs once before and once after).

BUNDLE — commits in this order.
C1 COPIES: `.agent/authored/f027-r10-block.md` := this block and each payload as
   `.agent/authored/f027-r10-<name>`, by `shutil.copyfile`. Subject `F027 R10 C1: copy round 10 block
   and payloads`. Its insertions are this block's line count plus 170.
C2 RECORDS: `git apply` records.diff, then `.agent/plan.md` := plan.md. Subject
   `F027 R10 C2: book round 9, resolve R-1069 and R-1070`. Expected by `git show --numstat`:
   6/0 .agent/live_review.md, 10/9 .agent/plan.md, 1/0 .agent/prose_slips.md.
C3 THE BUILT STATE AND THE CONSOLIDATION: `git apply` closure_docs.diff. Subject
   `F027 R10 C3: write the Built State and consolidate the checklist`. Expected by
   `git show --numstat`: 9/0 docs/agents/planner_reviewer_prompt.md, 89/0
   docs/roadmap/features/T5_F027.md.
C4 THE SELF-USE ITEM AND THE INTEGRATION GATE, in the PRIMARY checkout, after C3. (a) From a scratch
   Python file of yours: `packages.orchestration.self_use_generator.generate_and_append_if_empty()`
   with no arguments, then `packages.orchestration.self_use_queue.next_self_use_item()`; report both
   return values verbatim. The reviewer's dry run on a tree byte-equal to C3's read `None` for both,
   because the queue holds no pending item and the ledger no open finding. If yours reads `None` too,
   nothing is written and closure precondition 6 reads `self-use NONE (queue exhausted)`; if it
   appends an item instead, STOP after this step, commit `scripts/self_use_queue.json` alone with
   subject `F027 R10 C4a: the generator appended a self-use item`, and hand back without running it.
   (b) `bash -c 'npm --prefix apps/ui run build 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'` —
   a failing build is a STOP — then `git status --porcelain`, still empty. (c)
   `python3 -m pytest -n auto -q`, its log under `.remedy-wt/f027-r10-worker/`; measure its wall
   time. Write `.agent/authored/f027-closure-suite.txt` holding the command, the real exit code, the
   wall time, the summary line, the FULL list of bad node ids (failed plus errors) or the literal
   `NONE`, and one line naming the tree it ran on (C3's SHA). (d) Rewrite `.agent/handoff.md` per
   `docs/agents/handback_template.md` and commit it TOGETHER with the transcript. Subject
   `F027 R10 C4: record the closure suite transcript and rewrite handoff for round 10`. Then
   `git push origin feature/f027-task-veto`. No pull request.

CONSTRAINTS
1. Never edit or retype a payload; `git apply --check` before each `git apply`, exit codes reported.
2. Every commit under 500 insertions by `git show --numstat`.
3. The round's tracked path set: the `.agent/authored/f027-r10-*` copies, `.agent/live_review.md`,
   `.agent/prose_slips.md`, `.agent/plan.md`, `docs/roadmap/features/T5_F027.md`,
   `docs/agents/planner_reviewer_prompt.md`, `.agent/authored/f027-closure-suite.txt` and
   `.agent/handoff.md`, and `scripts/self_use_queue.json` only in C4(a)'s stop case. No edit to
   `README.md`, `docs/roadmap/STATUS.md`, `.agent/decisions.md`, `.agent/candidates.md`,
   `.agent/operator_questions.md` or any file under `packages/`, `apps/` or `tests/`.
4. A RED full suite in C4 is this feature's work, not a stop: commit the transcript exactly as
   measured, report every bad node id, and hand back; the repair rounds are the reviewer's to order
   (amend0917-throughput rule 2). Never weaken an assertion, delete a test or mark anything xfail.
5. Any other red gate: STOP, commit and push what is verified, hand back under AGENTS.md "If
   Blocked". Nothing is merged; no `gh pr create`; no force-push; no evidence job; no zip.
6. Leave every existing worktree, branch and stash alone.
7. The full suite runs ONCE, in C4, and nowhere else this round (amend0917 rule 1).

DONE-WHEN — every gate executed, every reading reported with its real exit code. G1 to G4 run before
C4 is written; G5 is C4's suite.
G1 TRANSPORT: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f027-r10-*` payload copy byte-equal to its source by `git show <C1>:<path>`.
G2 THE RECORDS: `git show <read at>:<path>` of each file below hashes to the reviewer's simulation:
   | read at | path | bytes | sha256 |
   |---|---|---|---|
   | C2 | .agent/live_review.md | 327838 | 9cd2dc7ef014b75a7c00048fc27032f7cc83095f9f5345df5af888d41bc8786a |
   | C2 | .agent/prose_slips.md | 369961 | c8c152823b7bc09fd5b352fbe831202e27485d8c189010e23922317441764876 |
   | C2 | .agent/plan.md | 1127 | 6de8d94dd410c2ddfb98a0c0b33bbe8537c58fe05904316835cbc3bbeb284b84 |
   | C3 | docs/roadmap/features/T5_F027.md | 11679 | 3f91b25c8dfd2a9b899241544284104936fc730f8edc47418a1f109bccd5dea5 |
   | C3 | docs/agents/planner_reviewer_prompt.md | 104549 | 49b5ace22ace6074c1e5cff11ef6c1d2e7cd95e04b76fb22d8888cac5941d504 |
   `open_finding_ids` over the ledger reads `[]` at C2; and `live_checklist_items` of
   `packages/orchestration/block_lint.py` over the planner prompt reads the same 34 numbers at
   `45cf5b9f` and at C3.
G3 THE LINTER: `python3 -m apps.cli.main integrity block .remedy-wt/f027-r10/block.md` at C3, real
   exit code 0, whole output.
G4 THE TESTS AND THE TREE, in the primary checkout at C3, serially:
   `bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/orchestration/test_block_lint.py
   tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py
   tests/orchestration/test_self_use_generator.py tests/orchestration/test_roadmap_index.py
   tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'` — exit 0, the
   summary line reported (the reviewer read the same selection without the golden path at 471 passed
   on its simulated tree); then `python3 -m apps.cli.main integrity check --json`, six `pass` at
   `fail_count` 0; and `git status --porcelain` empty with no untracked file (closure precondition 3).
G5 THE INTEGRATION GATE: C4(a)'s two return values; the UI build's last line and real exit code;
   `git status --porcelain` after it; then the full suite's real exit code, wall time, summary line
   and every bad node id, all in `.agent/authored/f027-closure-suite.txt`; and whether
   `tests/orchestration/test_import_reachability.py` or `tests/test_no_orphan_modules.py` holds a bad
   node (closure precondition 7).
G6 AFTER C4 AND THE PUSH, in your final reply only: `git status --porcelain` empty, the local tip equal
   to `origin/feature/f027-task-veto`, `git log --oneline -n 6`, `git worktree list`,
   `git branch --list 'remedy/job-*'`, the push's real outcome, and `gh pr list --state open --json
   number` EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block, the
per-commit changed-files table with the `git show --numstat` counts you measured beside the ones
above, every gate's real output, the self-use readings, the full suite's summary line and bad node
ids, the authored-text proofs, the item-status table AGENTS.md requires (one row per commit and per
gate), the deviations, and the next action. Session section: SESSION 2 of feature F027, round 10,
plus one sentence on how much context you had left. `## Next`: Phase 1 rule 1, the review of round
10, then the closure's evidence round — the booking of round 10, any repair the suite requires, the
evidence bundle and the review package — and then the closing round. State the open-findings count,
0, and "Operator questions open: 5".

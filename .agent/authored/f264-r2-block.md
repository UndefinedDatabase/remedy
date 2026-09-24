STEP F264 R2 — T001's SECOND HALF: `chat.send` on F009's write door, the cockpit's steering route

GOAL
Book round 1's PASS, record DECISION F264 D2, and land T001's second half: `chat.send` joins
the UI-exposed subset and F009's write door dispatches it to `steering.record_steering_message`
with channel `cockpit` — the same function `remedy chat` calls — with the door's own refusals,
its effect tests and their red proofs. No new route, no new outcome token.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

WHY THIS ROUND
T5_F264.md's Design: the write path is F009's single write channel and no second mutating
route is created. DECISION F264 D2 (the decisions.diff payload) fixes the route, the accepted
body, the three refusals and the four import-guard entries the door's new imports require.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f264-r2-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f264-r2-scratch/`   The reviewer's scripts; do not edit or delete them.
  `.remedy-wt/f264-r2-worker/`    YOURS for logs and scripts. All three are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, `cd <dir> && git ...`, and multi-operation
one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe pytest.
Use `git -C <path>` rather than `cd`. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`). A heredoc containing a dollar-brace is refused: write such a
script to a file under your own directory and run the file.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f264-steering-channel`, and `git log --oneline -1` must read `f3d0a4bf`. Report
   all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f264-r2-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f264-r2-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.diff | 10 | 6608 | 874790a241d29e10f174719e1fe39caed474faa2e06267432801f8c04b9e873b |
| plan.md | 32 | 1182 | 234b492da36e1adcecac5603ef0fb0773d9712135d3dfedeeeb23cce749d0f95 |
| decisions.diff | 39 | 3273 | b21e7e5518eb4bde801aee9b342198b2886a675061df289af1fec5a3a2b74e11 |
| product.diff | 187 | 10539 | 62877c5b50608565b27ca8e4e0a5b480ae3f66173a87ec825db9df5f71714ce4 |
| tests.diff | 117 | 5822 | 9c13b767fedad94c25fd10d849741f888834015b4785a110333f810528ffbe54 |
| mutations.py | 71 | 2582 | 181cdfc7f9c1000d9c767aa42d1dcfcf68dbb8c815a20a392d2d9108d9cf79b3 |

`plan.md` is a REWRITE of `.agent/plan.md`. The `.diff` files go on with `git apply`; the
reviewer generated every one from a tree at `f3d0a4bf` and applied all of them, in the commit
order below, to a fresh worktree at `f3d0a4bf` with `git apply --check` then `git apply`, every
one at real exit code 0. `ledger.diff` appends the `Gate: F264 R1 —` entry to
`.agent/live_review.md`. `product.diff` edits `apps/cli/command_catalog.py`,
`packages/orchestration/ui_server.py` and `tests/ui_server/test_command_channel.py` — the last
is the door's import guard and exposed-set pins, which the product change forces, so it lands
with the product. `tests.diff` adds one test class to `tests/ui_server/test_command_dispatch.py`.
`mutations.py` is a TOOL for G5: it is run, never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C2, C3, C4, C5 and C6, in this order.

C1a — copy this block and the bookkeeping payloads
  `.agent/authored/f264-r2-block.md` := this block, and one
  `.agent/authored/f264-r2-<name>` for each of ledger.diff, plan.md and decisions.diff,
  keeping each payload's own file name. All by `shutil.copyfile`.
  Subject: `F264 R2 C1a: copy round 2 block and bookkeeping payloads into .agent/authored/`
  Its insertions are this block's line count plus 81. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the product and test payloads
  `.agent/authored/f264-r2-<name>` for each of product.diff, tests.diff and mutations.py.
  Subject: `F264 R2 C1b: copy round 2 product and test payloads into .agent/authored/`
  Expected insertions: 375.

C2 — THE BOOKING, the round's first substantive commit:
   1. `git apply` ledger.diff  → `.agent/live_review.md`
   2. rewrite `.agent/plan.md` := plan.md
  Subject: `F264 R2 C2: book round 1's PASS and advance the plan to round 2`
  Expected insertions by `git show --numstat`: 2 live_review.md, 7 plan.md.

C3 — THE DECISION
  `git apply` decisions.diff → `.agent/decisions.md`.
  Subject: `F264 R2 C3: record DECISION F264 D2, the cockpit's steering route`
  Expected insertions: 31.

C4 — THE PRODUCT: `git apply` product.diff, then `git add` its three paths.
  Subject: `F264 R2 C4: expose chat.send on the write door as the cockpit's steering route`
  Expected insertions: 2 command_catalog.py, 74 ui_server.py, 14 test_command_channel.py.

C5 — THE TESTS: `git apply` tests.diff and `git add` its path.
  Subject: `F264 R2 C5: test what an accepted, refused or failed chat.send writes`
  Expected insertions: 109.

C6 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F264 R2 C6: rewrite handoff for round 2`
  Then `git push origin feature/f264-steering-channel`. Do NOT create a pull request: the
  branch opens one at F264's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f264-r2-*` copies,
   `.agent/live_review.md`, `.agent/plan.md`, `.agent/decisions.md`,
   `apps/cli/command_catalog.py`, `packages/orchestration/ui_server.py`,
   `tests/ui_server/test_command_channel.py`, `tests/ui_server/test_command_dispatch.py` and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only f3d0a4bf HEAD`
   after C6. Do NOT touch `.agent/prose_slips.md`, `.agent/candidates.md`,
   `.agent/operator_questions.md`, `.agent/context.md`, `README.md`,
   `docs/roadmap/STATUS.md` or `docs/roadmap/features/T5_F264.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch
   deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees, their branches, the reviewer's worktrees whose
   names begin `.remedy-wt/f264-`, and every existing stash alone. The worktree G5 adds goes
   under `.remedy-wt/`, is removed as that step's last action, and `git worktree list` is
   reported afterwards (finding R-0940).
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run
   and F264's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C6 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f264-r2-*` copy byte for
 byte with its source (the block copy against `.remedy-wt/f264-r2-block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE BOOKKEEPING — the sha256 of each file below, read with `git show <commit>:<path>` at
 the commit named, equals the reviewer's reading, which its simulation printed from a tree it
 built by applying these payloads at `f3d0a4bf`:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/live_review.md | 311577 | 01d5e337e4b1b039e89aa3ae8907871ecd9e03427b8035bc49b24db6bad74faa |
 | C2 | .agent/plan.md | 1182 | 234b492da36e1adcecac5603ef0fb0773d9712135d3dfedeeeb23cce749d0f95 |
 | C3 | .agent/decisions.md | 1942454 | aade59ebef70cd2ccca7fe65bd67d03c63c12da502a487afbcf023b27d835613 |
 Also: among the lines C2's diff ADDS to `.agent/live_review.md`, the count of those beginning
 `Gate: F264 R1 — ` (the reviewer's simulation read 1); the open set by distinct id, computed
 with `open_finding_ids` from `scripts/rotate_live_review.py` over the file's TEXT, at
 `f3d0a4bf` and at C2, with the set difference in both directions (the reviewer read 3 and 3 —
 R-0499, R-0950 and R-1008 — both differences empty); and `git diff --name-only <C1b> <C2>` and
 `git diff --name-only <C2> <C3>`, which must name exactly the paths C2 and C3 list.

G3 THE PRODUCT — at C5, the sha256 of each file below, read with `git show <C5>:<path>`,
 equals the reviewer's simulated reading:
 | path | bytes | sha256 |
 |---|---|---|
 | apps/cli/command_catalog.py | 113011 | 06ec9898da12dbe7bcae0e698f1ac16bc8fce8b2e953f9c00cd06d99dfc9e437 |
 | packages/orchestration/ui_server.py | 151408 | ef7f194cb3c681a6b1d361e5e2f658b4edb83cbe99a1a9bb7824f94752a25648 |
 | tests/ui_server/test_command_channel.py | 94498 | 5d92b06da5abf97aea7f6d148d2627b5cfc83d78ab1885ec081d507e1bb950bb |
 | tests/ui_server/test_command_dispatch.py | 25413 | 4fab7c1e32279389fe25da8ba3ff10fee9e77eadae4588edcc849a3f9d5ee885 |
 Also `git diff --name-only <C3> <C4>` and `<C4> <C5>`, which must name exactly the paths C4
 and C5 list.

G4 THE TESTS — in the primary checkout at C5, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/ui_server/test_command_dispatch.py tests/ui_server/test_command_channel.py tests/test_command_catalog.py tests/orchestration/test_steering.py tests/cli/test_chat_cmd.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/orchestration/test_event_names.py tests/ui_contracts/test_humanize_catalog.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path, serially, inside its sim
 worktree carrying C2 to C5 and read `432 passed, 1 skipped` at real exit code 0; the primary
 checkout carries the UI toolchain a worktree lacks, so a skip may pass there. Report what you
 read. Then `python3 -m ruff check packages/orchestration/ui_server.py
 apps/cli/command_catalog.py tests/ui_server/test_command_channel.py
 tests/ui_server/test_command_dispatch.py`, real exit code 0, and
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f264-r2-mut <C5>`, then
 `python3 -B .remedy-wt/f264-r2-payloads/mutations.py .remedy-wt/f264-r2-mut` and report its
 whole output. The script asserts each FROM occurs exactly once, applies it, runs the
 `TestChatSendDispatchEffects` class of `tests/ui_server/test_command_dispatch.py` and the whole
 of `tests/ui_server/test_command_channel.py` under `python3 -B`, restores the bytes, and runs
 an unmutated control first and last. The reviewer read, over the same script against its own
 tree carrying C2 to C5:
 control_before `114 passed` at exit 0;
 m1 (the route's id never matched, so nothing dispatches it) 6 failed at exit 1;
 m2 (the door records channel `cli`) 1 failed at exit 1;
 m3 (the message's shape never checked) 2 failed at exit 1;
 m4 (a write failure answered as an ended job) 1 failed at exit 1;
 m5 (an ended job answered as a write failure) 1 failed at exit 1;
 m6 (`chat.send` absent from the exposed subset) 5 failed at exit 1;
 control_after `114 passed` at exit 0; every `restored byte-identical` line True.
 Then `git worktree remove --force .remedy-wt/f264-r2-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C6: `git status --porcelain`, which must be empty;
 `git log --oneline -n 8`, which must show C6, C5, C4, C3, C2, C1b, C1a and `f3d0a4bf` in that
 order; `git worktree list`, which must show the primary checkout, the `.remedy-wt/job-*`
 worktrees and the reviewer's `.remedy-wt/f264-*` worktrees constraint 6 names, and nothing
 else; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be
 EMPTY. These readings go in your reply, since C6 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F264, round 2, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 2, then the cockpit's input field — the request builder, the send flow and the
component. State the open-findings count, 3, and the operator-questions count, 0.

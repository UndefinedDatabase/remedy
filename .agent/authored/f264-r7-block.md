STEP F264 R7 — T003's SECOND HALF: the cockpit's activity feed shows each steering acknowledgement

GOAL
Book round 6's PASS, record DECISION F264 D7, and land T003's second half: a new pure module
`apps/ui/src/api/steeringAck.ts` reads the stream's `steering` field on a
`steering_message_consumed` frame, checking every value, and `feedRowOf` shows that row as
"Steering taken in at round <n>: <restatement>." in the activity feed directly above the
steering input. A Python guard pins the reader's keys and event kind to the server's stream
field. With this round T001 to T003 are built.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

WHY THIS ROUND
T5_F264.md's Done wants the acknowledgement in the cockpit and in the CLI, from the same stream
event; round 6 put it on the stream and in `remedy chat show`. DECISION F264 D7 (in the
records.diff payload) fixes the reader, the line and where it shows. This is UI work under
`docs/ui/design_reference/`; it adds no component and no layout, so it adds no assumption-log
entry.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f264-r7-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f264-r7-scratch/`   The reviewer's scripts; do not edit or delete them.
  `.remedy-wt/f264-r7-worker/`    YOURS for logs and scripts. All three are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, `cd <dir> && git ...`, and multi-operation
one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe pytest.
Use `git -C <path>` rather than `cd`. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`). A heredoc containing a dollar-brace is refused: write such a
script to a file under your own directory and run the file. Do NOT run `npm` or `npx`
yourself: every UI check below reaches the toolchain through a pytest node or through the
reviewer's `mutations.py`, both of which run the primary checkout's installed tools.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`: report `pwd`
   and use absolute paths or `git -C /home/decodeux/Repos/remedy` throughout.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f264-steering-channel`, and `git log --oneline -1` must read `e420be13`. Report
   all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f264-r7-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f264-r7-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 44 | 9006 | 28fd35118229911baf9795913bf1c1668357cf126f6b08b31ffce54b821e2dd6 |
| plan.md | 31 | 1118 | a16f75fcefaaaaffc52222695f4794ad923ac2b1ced0b8dc68036adcb11d39f3 |
| product.diff | 29 | 1330 | 21c2aea51524e1e27cbe2d2422d445b2a0ee54ee527f5e612ac93260544c4408 |
| steeringAck.ts | 50 | 2431 | 784083ecf18c7c677cdcdb371bf9d919a72730c88ee4cf727531bfb80699e75e |
| mutations.py | 81 | 3577 | 2143d380794cdf1887f854abf6acd7a6f5229dbdffedc60e3bc430cbd4f48edd |
| tests.diff | 50 | 2513 | 72e612417c46ccb5f24290ba8d52df00327606afcfca3841c5e958c852d01b6e |
| steeringAck.test.ts | 41 | 1829 | 39a86cd1b90301301854d9c9932244a3b6ef27d665a8ffeab6548b8117e7fdbf |

`plan.md` is a REWRITE of `.agent/plan.md`. `steeringAck.ts` is a NEW FILE at
`apps/ui/src/api/steeringAck.ts` and `steeringAck.test.ts` a NEW FILE at
`apps/ui/src/api/steeringAck.test.ts`, each copied whole. The `.diff` files go on with
`git apply`; the reviewer generated every one from a tree at `e420be13` and applied all of them,
in the commit order below, to a fresh worktree at `e420be13` with `git apply --check` then
`git apply`, every one at real exit code 0. `records.diff` appends the `Gate: F264 R6 —` entry to
`.agent/live_review.md` and DECISION F264 D7 to `.agent/decisions.md`. `product.diff` edits
`apps/ui/src/api/feedRow.ts`. `tests.diff` edits `apps/ui/src/api/feedRow.test.ts` and
`tests/ui_contracts/test_steering_send_contract.py`. `mutations.py` is a TOOL for G5: it is run,
never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C2, C3, C4 and C5, in this order.

C1a — copy this block and the bookkeeping payloads
  `.agent/authored/f264-r7-block.md` := this block, and one
  `.agent/authored/f264-r7-<name>` for each of records.diff and plan.md, keeping each
  payload's own file name. All by `shutil.copyfile`.
  Subject: `F264 R7 C1a: copy round 7 block and bookkeeping payloads into .agent/authored/`
  Its insertions are this block's line count plus 75. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the product and test payloads
  `.agent/authored/f264-r7-<name>` for each of product.diff, steeringAck.ts, mutations.py,
  tests.diff and steeringAck.test.ts.
  Subject: `F264 R7 C1b: copy round 7 product and test payloads into .agent/authored/`
  Expected insertions: 251.

C2 — THE RECORDS, in ONE commit (amend0917-throughput rule 4):
   1. `git apply` records.diff  → `.agent/live_review.md` and `.agent/decisions.md`
   2. rewrite `.agent/plan.md` := plan.md
  Subject: `F264 R7 C2: book round 6's PASS, record DECISION F264 D7 and advance the plan`
  Expected insertions by `git show --numstat`: 26 decisions.md, 2 live_review.md, 11 plan.md.

C3 — THE PRODUCT: copy steeringAck.ts to `apps/ui/src/api/steeringAck.ts`, then `git apply`
  product.diff, then `git add` both paths.
  Subject: `F264 R7 C3: show each steering acknowledgement in the cockpit's activity feed`
  Expected insertions: 50 steeringAck.ts, 6 feedRow.ts.

C4 — THE TESTS: copy steeringAck.test.ts to `apps/ui/src/api/steeringAck.test.ts`, then
  `git apply` tests.diff, then `git add` all three paths.
  Subject: `F264 R7 C4: test the acknowledgement reader, the feed line and the stream pin`
  Expected insertions: 41 steeringAck.test.ts, 22 feedRow.test.ts,
  12 test_steering_send_contract.py.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F264 R7 C5: rewrite handoff for round 7`
  Then `git push origin feature/f264-steering-channel`. Do NOT create a pull request: the
  branch opens one at F264's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f264-r7-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `apps/ui/src/api/steeringAck.ts`, `apps/ui/src/api/feedRow.ts`,
   `apps/ui/src/api/steeringAck.test.ts`, `apps/ui/src/api/feedRow.test.ts`,
   `tests/ui_contracts/test_steering_send_contract.py` and `.agent/handoff.md`. Report the list
   you measure with `git diff --name-only e420be13 HEAD` after C5. Do NOT touch
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md`,
   `.agent/context.md`, `README.md`, `docs/roadmap/STATUS.md`,
   `docs/roadmap/features/T5_F264.md`, `apps/ui/package.json` or `apps/ui/package-lock.json`.
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
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f264-r7-*` copy byte for
 byte with its source (the block copy against `.remedy-wt/f264-r7-block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS — at C2, the sha256 of each file below, read with `git show <C2>:<path>`,
 equals the reviewer's reading, which its simulation printed from a tree it built by applying
 these payloads at `e420be13`:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 322329 | 5cb85dd31b1011c14bbe2eefc562ae9dad08e677e0d7b04c8ce2c854d25ee075 |
 | .agent/decisions.md | 1955579 | 0d33643528359dc3417f5a77548e5d9356fbee0aa938ddd35b8a54f730004b4e |
 | .agent/plan.md | 1118 | a16f75fcefaaaaffc52222695f4794ad923ac2b1ced0b8dc68036adcb11d39f3 |
 Also: among the lines C2's diff ADDS to `.agent/live_review.md`, the count of those beginning
 `Gate: F264 R6 — ` (the reviewer's simulation read 1); the open set by distinct id, computed
 with `open_finding_ids` from `scripts/rotate_live_review.py` over the file's TEXT, at
 `e420be13` and at C2, with the set difference in both directions (the reviewer read 3 and 3 —
 R-0499, R-0950 and R-1008 — both differences empty); and `git diff --name-only <C1b> <C2>`,
 which must name exactly the three record paths C2 writes.

G3 THE PRODUCT — at C4, the sha256 of each file below, read with `git show <C4>:<path>`,
 equals the reviewer's simulated reading:
 | path | bytes | sha256 |
 |---|---|---|
 | apps/ui/src/api/steeringAck.ts | 2431 | 784083ecf18c7c677cdcdb371bf9d919a72730c88ee4cf727531bfb80699e75e |
 | apps/ui/src/api/feedRow.ts | 3281 | 7e1310d8942d3628919bcb13b2a03d80e69cf05c78564201c818c42f6992ff54 |
 | apps/ui/src/api/steeringAck.test.ts | 1829 | 39a86cd1b90301301854d9c9932244a3b6ef27d665a8ffeab6548b8117e7fdbf |
 | apps/ui/src/api/feedRow.test.ts | 3962 | 320875e2baf0c97e11d0b96ef5859e226abc067ca244d997db92a5370d0802eb |
 | tests/ui_contracts/test_steering_send_contract.py | 3531 | 1b5bc2b7fa84df40e91b19e7d5e2976bc5fcf16df51313e28bba88b4781e3774 |
 Also `git diff --name-only <C2> <C3>` and `<C3> <C4>`, which must name exactly the paths C3
 and C4 list.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/ui_server/test_sse_stream.py tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path, serially, inside its sim
 worktree carrying C2 to C4 and read `1057 passed, 9 skipped` at real exit code 0. Of those
 skips, FOUR are toolchain nodes a worktree cannot run and the primary checkout can, and each
 of them must PASS in your run, not skip: the two in `tests/ui_contracts/test_ui_lint.py`
 (eslint at zero warnings), the typescript node in `tests/ui_server/test_dashboard_contract.py`
 (`tsc --noEmit`) and the vitest node in `tests/orchestration/test_test_runner.py`. Report
 every `SKIPPED` line the `-rs` summary prints. Then `python3 -m ruff check
 tests/ui_contracts/test_steering_send_contract.py`, real exit code 0, and
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f264-r7-mut <C4>`, then
 `python3 -B .remedy-wt/f264-r7-payloads/mutations.py .remedy-wt/f264-r7-mut` and report its
 whole output. For each mutation the script runs vitest over the WORKTREE's
 `steeringAck.test.ts` and `feedRow.test.ts` from the primary `apps/ui` with a scratch config
 under `.remedy-wt/`, and pytest over the worktree's
 `tests/ui_contracts/test_steering_send_contract.py`; it asserts each FROM occurs exactly once,
 restores the bytes, and runs an unmutated control first and last. The reviewer read, over the
 same script against its own tree carrying C2 to C4:
 control_before vitest `15 passed` at exit 0 and pytest at exit 0;
 u1 (the feed keeps the catalog line) vitest 1 failed at exit 1, pytest exit 0;
 u2 (the round left unchecked) vitest 1 failed at exit 1, pytest exit 0;
 u3 (any kind read as an acknowledgement) vitest 1 failed at exit 1, pytest exit 0;
 u4 (the restatement dropped from the line) vitest 2 failed at exit 1, pytest exit 0;
 p1 (the reader's key drifted from the stream's) vitest 2 failed at exit 1 AND pytest exit 1;
 control_after as control_before; every `restored byte-identical` line True.
 Then `git worktree remove --force .remedy-wt/f264-r7-mut`, `git worktree prune`, and report
 `git worktree list` and `git status --porcelain`, which must be empty.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 7`, which must show C5, C4, C3, C2, C1b, C1a and `e420be13` in that
 order; `git worktree list`, which must show the primary checkout, the `.remedy-wt/job-*`
 worktrees and the reviewer's `.remedy-wt/f264-*` worktrees constraint 6 names, and nothing
 else; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be
 EMPTY. These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F264, round 7, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 7, then the closure sequence's first half — the user-facing docs for `remedy chat`,
the feature file's Built State, the checklist consolidation, the self-use track and the
feature's one full suite. State the open-findings count, 3, and the operator-questions count, 0.

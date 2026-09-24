STEP F264 R3 — THE COCKPIT'S STEERING INPUT GOES LIVE: `steeringSend.ts`, the input and its card

GOAL
Book round 2's PASS, record DECISION F264 D3 and the round's two prose slips, and put the
cockpit's steering input live: `apps/ui/src/api/steeringSend.ts` builds, sends and describes a
`chat.send` through the decision inbox's existing path, nonce and submit modules; `ChatInput`
holds the typed text and says what became of each message; `ActivityFeedCard` renders one
composer in both branches, live only for an addressed job that can still run. The design
reference's assumption log records what the reference does not settle, and Python guards pin
the browser's mirrored rules to the server's.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

WHY THIS ROUND
T5_F264.md's Goal names "a cockpit input field" beside `remedy chat`, and round 2 exposed its
route. This is UI work: `docs/ui/design_reference/` binds it, and each deviation or assumption
it ships is an entry in that folder's `assumption_log.md`, landed in the same commit.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f264-r3-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f264-r3-scratch/`   The reviewer's scripts; do not edit or delete them.
  `.remedy-wt/f264-r3-worker/`    YOURS for logs and scripts. All three are gitignored.

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
   `feature/f264-steering-channel`, and `git log --oneline -1` must read `61e6dd70`. Report
   all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f264-r3-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f264-r3-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 57 | 12156 | 7acfb2725de74ea12787263c6e7ed0b5076f766aa53a3e91b502058894f468eb |
| plan.md | 30 | 1088 | b25f57bbfbfc1218e250f443ca50a10f5ff71eaf327e0a22cbe6f84f0ef95a78 |
| product.diff | 319 | 17577 | 4ab7e2a9798de1602c04760c31e50b2a58f5e1b2f2c8a83a1ab5d08effa31212 |
| steeringSend.ts | 182 | 8304 | a37b3e376a86ddcd00d8995a0e8a87354df1c720fbacb6e93cdbfa2d2a3a52cb |
| mutations.py | 95 | 4010 | 5b378ea8d8c2ecd305dd3ccaf0d93202dc9e6f870c8ccbfc64b43d909eb32cf9 |
| steeringSend.test.ts | 179 | 6928 | 34918e07c0c846a99ac5eaf9652199449620e996e54514ee9c1fcc9742a64f05 |
| test_steering_send_contract.py | 64 | 2778 | d23d40816fc83d18c98d41276a1fc2090c673aca577538e7b03cbcdf11985fdd |

`plan.md` is a REWRITE of `.agent/plan.md`. `steeringSend.ts` is a NEW FILE at
`apps/ui/src/api/steeringSend.ts`, `steeringSend.test.ts` a NEW FILE at
`apps/ui/src/api/steeringSend.test.ts`, and `test_steering_send_contract.py` a NEW FILE at
`tests/ui_contracts/test_steering_send_contract.py`, each copied whole. The `.diff` files go on
with `git apply`; the reviewer generated every one from a tree at `61e6dd70` and applied all of
them, in the commit order below, to a fresh worktree at `61e6dd70` with `git apply --check` then
`git apply`, every one at real exit code 0. `records.diff` appends to `.agent/live_review.md`
(the `Gate: F264 R2 —` entry), `.agent/decisions.md` (DECISION F264 D3) and
`.agent/prose_slips.md` (two dated lines). `product.diff` edits
`apps/ui/src/components/panels/ActivityFeedCard.tsx`,
`apps/ui/src/components/panels/ChatInput.tsx`,
`apps/ui/src/components/panels/RightLivePanel.module.css`,
`apps/ui/src/components/panels/RightLivePanel.tsx`,
`docs/ui/design_reference/assumption_log.md` and
`tests/ui_contracts/test_brain_stream_ring.py` — the last rewrites the guard class that pinned
the input as disabled, which the product change forces, so it lands with the product.
`mutations.py` is a TOOL for G5: it is run, never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C1c, C2, C3, C4 and C5, in this order.

C1a — copy this block and the bookkeeping payloads
  `.agent/authored/f264-r3-block.md` := this block, and one
  `.agent/authored/f264-r3-<name>` for each of records.diff and plan.md, keeping each
  payload's own file name. All by `shutil.copyfile`.
  Subject: `F264 R3 C1a: copy round 3 block and bookkeeping payloads into .agent/authored/`
  Its insertions are this block's line count plus 87. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the product diff and the mutation tool
  `.agent/authored/f264-r3-<name>` for each of product.diff and mutations.py.
  Subject: `F264 R3 C1b: copy round 3 product diff and mutation tool into .agent/authored/`
  Expected insertions: 414.

C1c — copy the new module and the test payloads
  `.agent/authored/f264-r3-<name>` for each of steeringSend.ts, steeringSend.test.ts and
  test_steering_send_contract.py.
  Subject: `F264 R3 C1c: copy round 3 module and test payloads into .agent/authored/`
  Expected insertions: 425.

C2 — THE RECORDS, in ONE commit (amend0917-throughput rule 4):
   1. `git apply` records.diff  → the three `.agent/` record files above
   2. rewrite `.agent/plan.md` := plan.md
  Subject: `F264 R3 C2: book round 2's PASS, record DECISION F264 D3 and advance the plan`
  Expected insertions by `git show --numstat`: 29 decisions.md, 2 live_review.md, 7 plan.md,
  2 prose_slips.md.

C3 — THE PRODUCT: copy steeringSend.ts to `apps/ui/src/api/steeringSend.ts`, then
  `git apply` product.diff, then `git add` all seven paths.
  Subject: `F264 R3 C3: put the cockpit's steering input live in the activity card`
  Expected insertions: 182 steeringSend.ts, 27 ActivityFeedCard.tsx, 59 ChatInput.tsx,
  12 RightLivePanel.module.css, 1 RightLivePanel.tsx, 5 assumption_log.md,
  23 test_brain_stream_ring.py.

C4 — THE TESTS: copy steeringSend.test.ts to `apps/ui/src/api/steeringSend.test.ts` and
  test_steering_send_contract.py to `tests/ui_contracts/test_steering_send_contract.py`, and
  `git add` both.
  Subject: `F264 R3 C4: test the steering sender and pin its rules to the server's`
  Expected insertions: 179 steeringSend.test.ts, 64 test_steering_send_contract.py.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F264 R3 C5: rewrite handoff for round 3`
  Then `git push origin feature/f264-steering-channel`. Do NOT create a pull request: the
  branch opens one at F264's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f264-r3-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/prose_slips.md`, `.agent/plan.md`,
   `apps/ui/src/api/steeringSend.ts`, the six paths product.diff edits (listed under
   PAYLOADS), `apps/ui/src/api/steeringSend.test.ts`,
   `tests/ui_contracts/test_steering_send_contract.py` and `.agent/handoff.md`. Report the
   list you measure with `git diff --name-only 61e6dd70 HEAD` after C5. Do NOT touch
   `.agent/candidates.md`, `.agent/operator_questions.md`, `.agent/context.md`, `README.md`,
   `docs/roadmap/STATUS.md`, `docs/roadmap/features/T5_F264.md`, `apps/ui/package.json` or
   `apps/ui/package-lock.json`.
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
 against the PAYLOADS table. Then compare each `.agent/authored/f264-r3-*` copy byte for
 byte with its source (the block copy against `.remedy-wt/f264-r3-block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS — at C2, the sha256 of each file below, read with `git show <C2>:<path>`,
 equals the reviewer's reading, which its simulation printed from a tree it built by applying
 these payloads at `61e6dd70`:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 313792 | fbfd98d1184dbf030c4d8d18f0fd2f8715812b7e8b15ad9b5e53ae59274dbd44 |
 | .agent/decisions.md | 1945107 | a5871a9e5673d0e9f418017f7c39f563e9a87c95f9f8cd9312335ef0b0d8c019 |
 | .agent/prose_slips.md | 365777 | ce66ed20b98c517d2f30c08b6fe5e455e06107133c62c463ab3479a2b0a94207 |
 | .agent/plan.md | 1088 | b25f57bbfbfc1218e250f443ca50a10f5ff71eaf327e0a22cbe6f84f0ef95a78 |
 Also: among the lines C2's diff ADDS to `.agent/live_review.md`, the count of those beginning
 `Gate: F264 R2 — ` (the reviewer's simulation read 1); the open set by distinct id, computed
 with `open_finding_ids` from `scripts/rotate_live_review.py` over the file's TEXT, at
 `61e6dd70` and at C2, with the set difference in both directions (the reviewer read 3 and 3 —
 R-0499, R-0950 and R-1008 — both differences empty); and `git diff --name-only <C1c> <C2>`,
 which must name exactly the four record paths C2 writes.

G3 THE PRODUCT — at C4, the sha256 of each file below, read with `git show <C4>:<path>`,
 equals the reviewer's simulated reading:
 | path | bytes | sha256 |
 |---|---|---|
 | apps/ui/src/api/steeringSend.ts | 8304 | a37b3e376a86ddcd00d8995a0e8a87354df1c720fbacb6e93cdbfa2d2a3a52cb |
 | apps/ui/src/components/panels/ActivityFeedCard.tsx | 8867 | 5669288859bf43b24dfb7e1cb73d7cd430529bd4dd1c59467151a73b5e30bf6c |
 | apps/ui/src/components/panels/ChatInput.tsx | 2836 | 3fcd36247eb6199d2c7920640e22e9a41eec6137a1b883c27bd72eb5a4dd386b |
 | apps/ui/src/components/panels/RightLivePanel.module.css | 25148 | 7ccd0b1d98496560025b89f7b50bde7aa53220ce9e14c41d2b68325864761f3c |
 | apps/ui/src/components/panels/RightLivePanel.tsx | 2914 | f15bcd8dc0e7176448b45d6cf4b6f014ddc905e26681ab7e41d645dc7080e428 |
 | docs/ui/design_reference/assumption_log.md | 2951 | a6a3b7230ee7be6e3f668bb03128516b36ceba6294240fb3cf793ee6fae2474b |
 | tests/ui_contracts/test_brain_stream_ring.py | 31346 | 70261cc25ee5f470a24c2cb1cefca9653be86b135e567cc7a4963ea84d238d94 |
 | apps/ui/src/api/steeringSend.test.ts | 6928 | 34918e07c0c846a99ac5eaf9652199449620e996e54514ee9c1fcc9742a64f05 |
 | tests/ui_contracts/test_steering_send_contract.py | 2778 | d23d40816fc83d18c98d41276a1fc2090c673aca577538e7b03cbcdf11985fdd |
 Also `git diff --name-only <C2> <C3>` and `<C3> <C4>`, which must name exactly the paths C3
 and C4 list.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path, serially, inside its sim
 worktree carrying C2 to C4 and read `1316 passed, 9 skipped` at real exit code 0. Of those
 skips, FOUR are toolchain nodes a worktree cannot run and the primary checkout can, and each
 of them must PASS in your run, not skip: the two in `tests/ui_contracts/test_ui_lint.py`
 (eslint at zero warnings), the typescript node in `tests/ui_server/test_dashboard_contract.py`
 (`tsc --noEmit`) and the vitest node in `tests/orchestration/test_test_runner.py`. Report
 every `SKIPPED` line the `-rs` summary prints. Then `python3 -m ruff check
 tests/ui_contracts/test_brain_stream_ring.py tests/ui_contracts/test_steering_send_contract.py`,
 real exit code 0, and `python3 -m apps.cli.main integrity check --json`, which must read all
 six checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f264-r3-mut <C4>`, then
 `python3 -B .remedy-wt/f264-r3-payloads/mutations.py .remedy-wt/f264-r3-mut` and report its
 whole output. For each mutation the script runs vitest over the WORKTREE's
 `steeringSend.test.ts` from the primary `apps/ui` with a scratch config under `.remedy-wt/`,
 and pytest over the worktree's `tests/ui_contracts/test_steering_send_contract.py` and
 `tests/ui_contracts/test_brain_stream_ring.py`; it asserts each FROM occurs exactly once,
 restores the bytes, and runs an unmutated control first and last. The reviewer read, over the
 same script against its own tree carrying C2 to C4:
 control_before vitest `17 passed` at exit 0 and pytest `74 passed` at exit 0;
 u1 (every job state open) vitest 2 failed at exit 1;
 u2 (the limit counted in UTF-16 units, not code points) vitest 1 failed at exit 1;
 u3 (the untrimmed message sent) vitest 1 failed at exit 1;
 u4 (an ended job's refusal not named) vitest 1 failed at exit 1;
 u5 (a request built with no job or token) vitest 1 failed at exit 1;
 p1 (a refused message's text cleared) pytest 1 failed at exit 1;
 p2 (the browser's limit drifted from the server's) pytest 1 failed at exit 1;
 p3 (the card never closes the input) pytest 1 failed at exit 1;
 each of u1 to u5 with pytest still at exit 0, each of p1 to p3 with vitest still at exit 0;
 control_after as control_before; every `restored byte-identical` line True.
 Then `git worktree remove --force .remedy-wt/f264-r3-mut`, `git worktree prune`, and report
 `git worktree list` and `git status --porcelain`, which must be empty.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 8`, which must show C5, C4, C3, C2, C1c, C1b, C1a and `61e6dd70` in that
 order; `git worktree list`, which must show the primary checkout, the `.remedy-wt/job-*`
 worktrees and the reviewer's `.remedy-wt/f264-*` worktrees constraint 6 names, and nothing
 else; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be
 EMPTY. These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
assumption-log entries this round made (three rows, all in product.diff), the item-status table
AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected
action. Report what you ran, not what you expected to find. Your Session section reads SESSION 1
of feature F264, round 3, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 3, then T002 — consumption at the run's next safe point, with a red proof that a
mid-call message waits. State the open-findings count, 3, and the operator-questions count, 0.

STEP F264 R5 — T002's MISSION HALF: a consumed steering message amends its mission's contract

GOAL
Book round 4's PASS, record DECISION F264 D5, and land T002's mission half: when
`steering.consume_pending_steering` consumes a message of a job that belongs to a mission, it
first amends that mission's contract through F269's `amend_mission_contract` — once per message,
before the consumption marker is published — and the marker and the `steering_message_consumed`
event name the amendment. A job with no mission amends nothing; a failed amendment is loud and
leaves the message pending.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

WHY THIS ROUND
DECISION amend0905-vocab D9 makes every operator message an amendment "recorded on the mission,
DoD recompiled", and DECISION F264 D1 left that to T002. DECISION F264 D5 (in the records.diff
payload) fixes when, how often, and what happens on failure.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f264-r5-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f264-r5-scratch/`   The reviewer's scripts; do not edit or delete them.
  `.remedy-wt/f264-r5-worker/`    YOURS for logs and scripts. All three are gitignored.

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
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`: report `pwd`
   and use absolute paths or `git -C /home/decodeux/Repos/remedy` throughout.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f264-steering-channel`, and `git log --oneline -1` must read `68f4273b`. Report
   all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f264-r5-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f264-r5-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 46 | 10274 | 6d4231852b7877e324606306ceae5c4f92a5e5a71dcdf0397f6f971c9896d701 |
| plan.md | 30 | 1145 | a9bf00c3da4eb744e39d2cf80030a755c9721b57c5df747c3a3d4780e9c7dc98 |
| product.diff | 96 | 5078 | cf7ee5f3171c118db519ea7f93e43e070b6675518e8b3da5711bede4fc027d96 |
| mutations.py | 64 | 2618 | e8bfb81d664dafbcf6c678d4968c0fcb51ad399c0fdb5929189d6318107c9605 |
| test_steering_mission.py | 95 | 3524 | 019243c0417b070db0071caedcc5ba9ed33019ff718be58cfcfffe92cbffb44d |

`plan.md` is a REWRITE of `.agent/plan.md`. `test_steering_mission.py` is a NEW FILE at
`tests/orchestration/test_steering_mission.py`, copied whole. The `.diff` files go on with
`git apply`; the reviewer generated every one from a tree at `68f4273b` and applied all of them,
in the commit order below, to a fresh worktree at `68f4273b` with `git apply --check` then
`git apply`, every one at real exit code 0. `records.diff` appends the `Gate: F264 R4 —` entry to
`.agent/live_review.md` and DECISION F264 D5 to `.agent/decisions.md`. `product.diff` edits
`packages/orchestration/mission_contract.py` (one docstring) and
`packages/orchestration/steering.py`. `mutations.py` is a TOOL for G5: it is run, never applied
to a tracked file.

BUNDLE — the commits are C1a, C1b, C2, C3, C4 and C5, in this order.

C1a — copy this block and the bookkeeping payloads
  `.agent/authored/f264-r5-block.md` := this block, and one
  `.agent/authored/f264-r5-<name>` for each of records.diff and plan.md, keeping each
  payload's own file name. All by `shutil.copyfile`.
  Subject: `F264 R5 C1a: copy round 5 block and bookkeeping payloads into .agent/authored/`
  Its insertions are this block's line count plus 76. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the product and test payloads
  `.agent/authored/f264-r5-<name>` for each of product.diff, mutations.py and
  test_steering_mission.py.
  Subject: `F264 R5 C1b: copy round 5 product and test payloads into .agent/authored/`
  Expected insertions: 255.

C2 — THE RECORDS, in ONE commit (amend0917-throughput rule 4):
   1. `git apply` records.diff  → `.agent/live_review.md` and `.agent/decisions.md`
   2. rewrite `.agent/plan.md` := plan.md
  Subject: `F264 R5 C2: book round 4's PASS, record DECISION F264 D5 and advance the plan`
  Expected insertions by `git show --numstat`: 28 decisions.md, 2 live_review.md, 7 plan.md.

C3 — THE PRODUCT: `git apply` product.diff, then `git add` its two paths.
  Subject: `F264 R5 C3: amend a mission's contract when its job consumes a steering message`
  Expected insertions: 4 mission_contract.py, 40 steering.py.

C4 — THE TESTS: copy test_steering_mission.py to
  `tests/orchestration/test_steering_mission.py` and `git add` it.
  Subject: `F264 R5 C4: test that a consumed message amends its mission once, and loudly`
  Expected insertions: 95.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F264 R5 C5: rewrite handoff for round 5`
  Then `git push origin feature/f264-steering-channel`. Do NOT create a pull request: the
  branch opens one at F264's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f264-r5-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `packages/orchestration/mission_contract.py`, `packages/orchestration/steering.py`,
   `tests/orchestration/test_steering_mission.py` and `.agent/handoff.md`. Report the list you
   measure with `git diff --name-only 68f4273b HEAD` after C5. Do NOT touch
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md`,
   `.agent/context.md`, `README.md`, `docs/roadmap/STATUS.md` or
   `docs/roadmap/features/T5_F264.md`.
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
 against the PAYLOADS table. Then compare each `.agent/authored/f264-r5-*` copy byte for
 byte with its source (the block copy against `.remedy-wt/f264-r5-block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS — at C2, the sha256 of each file below, read with `git show <C2>:<path>`,
 equals the reviewer's reading, which its simulation printed from a tree it built by applying
 these payloads at `68f4273b`:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 318623 | 1a9c1dc89473e849dafc8eacc8753230574adc70b99e1f3d958cfecb94107ce0 |
 | .agent/decisions.md | 1950501 | 39e5c8d66ade329cd9f9e293bfe73208bbfd96e759bb5e12e2a3eee2a2d85b03 |
 | .agent/plan.md | 1145 | a9bf00c3da4eb744e39d2cf80030a755c9721b57c5df747c3a3d4780e9c7dc98 |
 Also: among the lines C2's diff ADDS to `.agent/live_review.md`, the count of those beginning
 `Gate: F264 R4 — ` (the reviewer's simulation read 1); the open set by distinct id, computed
 with `open_finding_ids` from `scripts/rotate_live_review.py` over the file's TEXT, at
 `68f4273b` and at C2, with the set difference in both directions (the reviewer read 3 and 3 —
 R-0499, R-0950 and R-1008 — both differences empty); and `git diff --name-only <C1b> <C2>`,
 which must name exactly the three record paths C2 writes.

G3 THE PRODUCT — at C4, the sha256 of each file below, read with `git show <C4>:<path>`,
 equals the reviewer's simulated reading:
 | path | bytes | sha256 |
 |---|---|---|
 | packages/orchestration/mission_contract.py | 43776 | a1b9fae672eb2bc3fff08ec4b05791c2b7eda69e30915814287edbadf5564d23 |
 | packages/orchestration/steering.py | 15065 | 25f070898ff5a65fba97917ad961c9b04c7ef81bf3e41aac54ff9f993813135a |
 | tests/orchestration/test_steering_mission.py | 3524 | 019243c0417b070db0071caedcc5ba9ed33019ff718be58cfcfffe92cbffb44d |
 Also `git diff --name-only <C2> <C3>` and `<C3> <C4>`, which must name exactly the paths C3
 and C4 list.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_steering_mission.py tests/orchestration/test_steering.py tests/orchestration/test_steering_consumption.py tests/orchestration/test_mission_contract.py tests/orchestration/test_mission_state.py tests/orchestration/test_orchestrator_loop.py tests/orchestration/test_event_names.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/test_ble001_ratchet.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path, serially, inside its sim
 worktree carrying C2 to C4 and read `675 passed, 2 skipped` at real exit code 0; the primary
 checkout carries the UI toolchain a worktree lacks, so a skip may pass there. Report what you
 read. Then `python3 -m ruff check packages/orchestration/steering.py
 packages/orchestration/mission_contract.py tests/orchestration/test_steering_mission.py`, real
 exit code 0, and `python3 -m apps.cli.main integrity check --json`, which must read all six
 checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f264-r5-mut <C4>`, then
 `python3 -B .remedy-wt/f264-r5-payloads/mutations.py .remedy-wt/f264-r5-mut` and report its
 whole output. The script asserts each FROM occurs exactly once, applies it, runs
 `tests/orchestration/test_steering_mission.py`, `tests/orchestration/test_steering.py` and
 `tests/orchestration/test_steering_consumption.py` under `python3 -B`, restores the bytes, and
 runs an unmutated control first and last. The reviewer read, over the same script against its
 own tree carrying C2 to C4:
 control_before `41 passed` at exit 0;
 m1 (the mission never amended) 3 failed at exit 1;
 m2 (an already consumed message amended again) 1 failed at exit 1;
 m3 (the marker names no amendment) 2 failed at exit 1;
 m4 (a failed amendment swallowed) 1 failed at exit 1;
 control_after `41 passed` at exit 0; every `restored byte-identical` line True.
 Then `git worktree remove --force .remedy-wt/f264-r5-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 7`, which must show C5, C4, C3, C2, C1b, C1a and `68f4273b` in that
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
section reads SESSION 1 of feature F264, round 5, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 5, then T003 — the acknowledgement event, what was understood and from which round, in
the cockpit and in `remedy chat`. State the open-findings count, 3, and the operator-questions
count, 0.

STEP F264 R4 — T002: A STEERING MESSAGE IS CONSUMED AT THE NEXT ROUND'S SAFE POINT, EXACTLY ONCE

GOAL
Book round 3's PASS, record DECISION F264 D4, and land T002: `run_pingpong` reads pending
steering messages as its own step directly after each round's first safe point — never through
`stop_check`, which also fires inside a call — consumes each exactly once through a sealed,
create-once marker naming its task and round, writes a `steering_message_consumed` event, and
carries every consumed message verbatim in the builder prompt's new `builder_steering` segment.
The acceptance fixture compares round 2's prompt with and without a message sent while round 1's
call was in flight.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

WHY THIS ROUND
T5_F264.md's Orchestrator brief: T002 is the risky slice, because the safe-point boundary is the
property most likely to be quietly violated, so it needs a red proof that a mid-call message
WAITS. DECISION F264 D4 (in the records.diff payload) fixes the point, the marker, the event and
the segment.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f264-r4-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f264-r4-scratch/`   The reviewer's scripts; do not edit or delete them.
  `.remedy-wt/f264-r4-worker/`    YOURS for logs and scripts. All three are gitignored.

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
   `feature/f264-steering-channel`, and `git log --oneline -1` must read `889c556b`. Report
   all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f264-r4-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f264-r4-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 51 | 10595 | c6417d61be0b0c2984f572b6118db6f0741c1c4770e9d0a65aeccec424a363b9 |
| plan.md | 31 | 1238 | 08b916e270dc80ba485c3eb59b77c95a7a641bf94dae556c127b9faacd079833 |
| product.diff | 235 | 12142 | 3ada9914207183d789ae22aef7cd0a3fb7edc8c15e0becbb06d52a16a2fb7c7a |
| mutations.py | 73 | 2798 | 01edd6733d5a49d41ad8f897b5855f1752b4cacde0ee22976d79c85663d452ee |
| tests.diff | 77 | 3799 | 989c3a767970679c40efdf69a162bebacfbc7a7b85dc43e48c847f3c95921c6f |
| test_steering_consumption.py | 121 | 5944 | 90c7e9584a5cbe331924d0816eb4e0a6e5958b536243e43749fcafd8c47d8f91 |

`plan.md` is a REWRITE of `.agent/plan.md`. `test_steering_consumption.py` is a NEW FILE at
`tests/orchestration/test_steering_consumption.py`, copied whole. The `.diff` files go on with
`git apply`; the reviewer generated every one from a tree at `889c556b` and applied all of them,
in the commit order below, to a fresh worktree at `889c556b` with `git apply --check` then
`git apply`, every one at real exit code 0. `records.diff` appends the `Gate: F264 R3 —` entry to
`.agent/live_review.md` and DECISION F264 D4 to `.agent/decisions.md`. `product.diff` edits
`apps/ui/src/api/humanizeCatalog.ts`, `packages/orchestration/event_names.py`,
`packages/orchestration/pingpong_loop.py` and `packages/orchestration/steering.py`. `tests.diff`
adds two test classes to `tests/orchestration/test_steering.py`. `mutations.py` is a TOOL for G5:
it is run, never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C1c, C2, C3, C4 and C5, in this order.

C1a — copy this block and the bookkeeping payloads
  `.agent/authored/f264-r4-block.md` := this block, and one
  `.agent/authored/f264-r4-<name>` for each of records.diff and plan.md, keeping each
  payload's own file name. All by `shutil.copyfile`.
  Subject: `F264 R4 C1a: copy round 4 block and bookkeeping payloads into .agent/authored/`
  Its insertions are this block's line count plus 82. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the product diff and the mutation tool
  `.agent/authored/f264-r4-<name>` for each of product.diff and mutations.py.
  Subject: `F264 R4 C1b: copy round 4 product diff and mutation tool into .agent/authored/`
  Expected insertions: 308.

C1c — copy the test payloads
  `.agent/authored/f264-r4-<name>` for each of tests.diff and test_steering_consumption.py.
  Subject: `F264 R4 C1c: copy round 4 test payloads into .agent/authored/`
  Expected insertions: 198.

C2 — THE RECORDS, in ONE commit (amend0917-throughput rule 4):
   1. `git apply` records.diff  → `.agent/live_review.md` and `.agent/decisions.md`
   2. rewrite `.agent/plan.md` := plan.md
  Subject: `F264 R4 C2: book round 3's PASS, record DECISION F264 D4 and advance the plan`
  Expected insertions by `git show --numstat`: 33 decisions.md, 2 live_review.md, 9 plan.md.

C3 — THE PRODUCT: `git apply` product.diff, then `git add` its four paths.
  Subject: `F264 R4 C3: consume steering at the top of each round and carry it in the prompt`
  Expected insertions: 1 humanizeCatalog.ts, 1 event_names.py, 32 pingpong_loop.py,
  118 steering.py.

C4 — THE TESTS: `git apply` tests.diff, copy test_steering_consumption.py to
  `tests/orchestration/test_steering_consumption.py`, and `git add` both paths.
  Subject: `F264 R4 C4: prove a mid-call message waits for the next round and steers it`
  Expected insertions: 69 test_steering.py, 121 test_steering_consumption.py.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F264 R4 C5: rewrite handoff for round 4`
  Then `git push origin feature/f264-steering-channel`. Do NOT create a pull request: the
  branch opens one at F264's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f264-r4-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, the four paths
   product.diff edits (listed under PAYLOADS), `tests/orchestration/test_steering.py`,
   `tests/orchestration/test_steering_consumption.py` and `.agent/handoff.md`. Report the list
   you measure with `git diff --name-only 889c556b HEAD` after C5. Do NOT touch
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
 against the PAYLOADS table. Then compare each `.agent/authored/f264-r4-*` copy byte for
 byte with its source (the block copy against `.remedy-wt/f264-r4-block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS — at C2, the sha256 of each file below, read with `git show <C2>:<path>`,
 equals the reviewer's reading, which its simulation printed from a tree it built by applying
 these payloads at `889c556b`:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 316339 | 02e44b2e6f79bc99cedf4a794361b26a56dfa5f1ead9063a79b8c7101aae6f95 |
 | .agent/decisions.md | 1948088 | c8b9d4ce7da60338e385c206fd5fc66b3bd1b163f57de56b2f54fe853ce1b7f8 |
 | .agent/plan.md | 1238 | 08b916e270dc80ba485c3eb59b77c95a7a641bf94dae556c127b9faacd079833 |
 Also: among the lines C2's diff ADDS to `.agent/live_review.md`, the count of those beginning
 `Gate: F264 R3 — ` (the reviewer's simulation read 1); the open set by distinct id, computed
 with `open_finding_ids` from `scripts/rotate_live_review.py` over the file's TEXT, at
 `889c556b` and at C2, with the set difference in both directions (the reviewer read 3 and 3 —
 R-0499, R-0950 and R-1008 — both differences empty); and `git diff --name-only <C1c> <C2>`,
 which must name exactly the three record paths C2 writes.

G3 THE PRODUCT — at C4, the sha256 of each file below, read with `git show <C4>:<path>`,
 equals the reviewer's simulated reading:
 | path | bytes | sha256 |
 |---|---|---|
 | apps/ui/src/api/humanizeCatalog.ts | 6723 | 2d77359ef1f253d6f9cfeec7c4f2b723c97e78799a785600f19960d4ad6a1328 |
 | packages/orchestration/event_names.py | 8834 | 5c08ce7745d9dc7ea2ff7419d7235a04a7acc0fb4777b5a9b506d839f0189a59 |
 | packages/orchestration/pingpong_loop.py | 229941 | a6f6c74c58f570a84fbc59ca8735ccf6988868de8dd121c85373b129d5ce033c |
 | packages/orchestration/steering.py | 13123 | e91e7357d169f39ed86edd3fbc9e76a9fd2bd113c27d18d09e312064bb7f76ea |
 | tests/orchestration/test_steering.py | 8987 | 563aa54f035a85bb7a252d89af8acf8af0b92082dadcfbafdf39703de59023d5 |
 | tests/orchestration/test_steering_consumption.py | 5944 | 90c7e9584a5cbe331924d0816eb4e0a6e5958b536243e43749fcafd8c47d8f91 |
 Also `git diff --name-only <C2> <C3>` and `<C3> <C4>`, which must name exactly the paths C3
 and C4 list.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_steering.py tests/orchestration/test_steering_consumption.py tests/orchestration/test_builder_prompt_golden.py tests/orchestration/test_builder_prompt_hunk_rejections.py tests/orchestration/test_prompt_trace.py tests/orchestration/test_repair_loop.py tests/orchestration/test_pingpong.py tests/orchestration/test_job_stop_integration.py tests/orchestration/test_session_resume.py tests/orchestration/test_semantic_dedupe.py tests/orchestration/test_provider_retry.py tests/orchestration/test_event_names.py tests/ui_contracts/test_humanize_catalog.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path, serially, inside its sim
 worktree carrying C2 to C4 and read `726 passed, 2 skipped` at real exit code 0; the primary
 checkout carries the UI toolchain a worktree lacks, so a skip may pass there. Report what you
 read. Then `python3 -m ruff check packages/orchestration/steering.py
 packages/orchestration/pingpong_loop.py packages/orchestration/event_names.py
 tests/orchestration/test_steering.py tests/orchestration/test_steering_consumption.py`, real
 exit code 0, and `python3 -m apps.cli.main integrity check --json`, which must read all six
 checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f264-r4-mut <C4>`, then
 `python3 -B .remedy-wt/f264-r4-payloads/mutations.py .remedy-wt/f264-r4-mut` and report its
 whole output. The script asserts each FROM occurs exactly once, applies it, runs
 `tests/orchestration/test_steering_consumption.py` and `tests/orchestration/test_steering.py`
 under `python3 -B`, restores the bytes, and runs an unmutated control first and last. The
 reviewer read, over the same script against its own tree carrying C2 to C4:
 control_before `37 passed` at exit 0;
 m1 (the loop never reads steering) 4 failed at exit 1;
 m2 (the steering segment never registered) 3 failed at exit 1;
 m3 (a message consumed again every round) 2 failed at exit 1;
 m4 (the consumption round recorded one early) 4 failed at exit 1;
 m5 (a consumption marker's seal never checked) 1 failed at exit 1;
 m6 (only newly consumed messages carried, so a correction is forgotten) 2 failed at exit 1;
 control_after `37 passed` at exit 0; every `restored byte-identical` line True.
 Then `git worktree remove --force .remedy-wt/f264-r4-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 8`, which must show C5, C4, C3, C2, C1c, C1b, C1a and `889c556b` in that
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
section reads SESSION 1 of feature F264, round 4, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 4, then T002's mission half — a consumed message for a job that belongs to a mission
also amends the mission's contract. State the open-findings count, 3, and the
operator-questions count, 0.

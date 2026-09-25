STEP F023 R7 — T003 LAST PART: the live end-to-end, the frame budget at 500 nodes over every zoom level, and the round rule's missing golden

GOAL
Book round 6's PASS, record DECISION F023 D7, and land: `tests/ui_server/test_semantic_zoom_live.py`,
which runs a fake job and proves, task by task, that the rounds its stream logged since its last
start are exactly the rounds its run report serves; one golden in `runDetailModel.test.ts` for a
task that started again; the zoom's performance tool kept as evidence under
`.agent/authored/f023-r7-perf-*`; and your own run of that tool at 500 nodes over every zoom
level, committed as `.agent/authored/f023-r7-perf.txt`. This round changes no product code.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f023-r7-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f023-r7/`           READ-ONLY. The reviewer's block and scripts.
  `.remedy-wt/f023-r7-sim/`       The reviewer's simulated tree; do not touch it.
  `.remedy-wt/f023-r7-dry/`       The reviewer's authoring tree; do not touch it.
  `.remedy-wt/f023-r7-worker/`    YOURS for logs and scripts; create it if absent. All five are
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
   `feature/f023-semantic-zoom-l0-l3`, and `git log --oneline -1` must read `7405cf35`. Report
   all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f023-r7/block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f023-r7-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.diff | 63 | 10674 | aefc59674ab33bb5d2a2f66a9d7424d9cfee8d754642745d50ba423d7b11a5a3 |
| mutations.py | 146 | 6384 | 0b0c4e5b7ff6dfcdea697e2d42e4990a94269ad074150f00830c219c79ddfbb4 |
| perf-drive_chrome.mjs | 94 | 3712 | eeff3e6c142871ecef959fc725ab12053bcf78d3e76fd8f4dfa3f14f34ba0e0c |
| perf-index.html | 14 | 350 | 0bd59ba1d900f935e8e9b0ec5234cdb4b83ec4f29790f7930470cc0009cd6423 |
| perf-main.tsx | 124 | 6418 | 5cd453ff9f8ea0246771555852582d97ef1b3c973b65cf1d698f6b7d9d7bdf3d |
| perf-measure.py | 185 | 6267 | d1ba1621ebb4b79efb8638776c3d1398343ce7b1a610d7acaf314e864f60335a |
| perf-vite.config.mjs | 28 | 766 | 82b2d0f857c6821f6136d323d41d43ad94e6e4993ff192f17ee5425f9a74c6a9 |
| plan.md | 35 | 1329 | a8bbd02bbbd5fedebca23d09f0fd6a6fde0892949cac887a199e333a9771c321 |
| test_semantic_zoom_live.py | 57 | 3203 | 35b82ea5ae3aba3578196f6e95662089cebfcd4d8c7351e65ce0de9156a69759 |
| tests.diff | 16 | 955 | 5a8f68acea4dc57741f76cf93b0ff45a2e298335d2a4ed8d6aeafe06c5dda08a |

`plan.md` is a REWRITE of `.agent/plan.md`. `test_semantic_zoom_live.py` is a NEW FILE at
`tests/ui_server/test_semantic_zoom_live.py`, copied whole. `ledger.diff` and `tests.diff` go on
with `git apply`; the reviewer generated both with `git diff HEAD` from a tree at `7405cf35` into
which it wrote the edits. `ledger.diff` appends round 6's gate entry to `.agent/live_review.md` and
DECISION F023 D7 to `.agent/decisions.md`; `tests.diff` adds one golden to
`apps/ui/src/components/graph/runDetailModel.test.ts`. The five `perf-*` payloads are the zoom's
performance TOOL, and `mutations.py` is the TOOL for G5: both are run, never applied to a tracked
file.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C2, C3, C4 and C5, in this order.

C1a — copy this block and the plan payload
  `.agent/authored/f023-r7-block.md` := this block, and `.agent/authored/f023-r7-plan.md` :=
  plan.md. Both by `shutil.copyfile`.
  Subject: `F023 R7 C1a: copy round 7 block and plan payload into .agent/authored/`
  Expected insertions: 269. Report the number you measure and STOP rather than commit if it is
  500 or more.

C1b — copy the two diffs and the mutation tool
  `.agent/authored/f023-r7-ledger.diff`, `-tests.diff` and `-mutations.py`, each prefixed
  `f023-r7-` like the others.
  Subject: `F023 R7 C1b: copy round 7 diffs and mutation tool into .agent/authored/`
  Expected insertions: 225.

C1c — copy the performance tool
  each `perf-<name>` payload to `.agent/authored/f023-r7-perf-<name>`, for the five names
  `measure.py`, `main.tsx`, `drive_chrome.mjs`, `index.html` and `vite.config.mjs`.
  Subject: `F023 R7 C1c: copy the zoom performance tool into .agent/authored/`
  Expected insertions: 445.

C1d — copy the test payload
  `.agent/authored/f023-r7-test_semantic_zoom_live.py` := test_semantic_zoom_live.py.
  Subject: `F023 R7 C1d: copy round 7 test payload into .agent/authored/`
  Expected insertions: 57.

C2 — THE RECORDS, in this order: `git apply` ledger.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F023 R7 C2: book round 6's PASS, record D7, advance the plan`
  Expected by `git show --numstat` (insertions and deletions): 45/0 decisions.md, 2/0 live_review.md, 14/12 plan.md.

C3 — THE TESTS: `git apply` tests.diff, then copy test_semantic_zoom_live.py into
  `tests/ui_server/` and `git add` it.
  Subject: `F023 R7 C3: prove the run detail's round rule on a live job and pin a restarted task`
  Expected by `git show --numstat`: 5/0 runDetailModel.test.ts, 57/0 test_semantic_zoom_live.py.

C4 — THE PERFORMANCE TRANSCRIPT, after G4 and G5 have run at C3:
  1. create `.remedy-wt/f023-r7-worker/perf/` and copy each `perf-<name>` payload into it under
     its bare `<name>` by `shutil.copyfile` — `measure.py` copies its siblings by those names;
  2. in the primary checkout run
     `bash -c 'python3 -B .remedy-wt/f023-r7-worker/perf/measure.py /home/decodeux/Repos/remedy > .agent/authored/f023-r7-perf.txt 2>&1; echo "REAL_EXIT=$?"'`
     and report the REAL_EXIT line; the tool builds a harness under `.remedy-wt/f023-perf-run`,
     drives headless Chrome for about three minutes and removes its work directory itself;
  3. `git add .agent/authored/f023-r7-perf.txt` and commit it alone.
  Subject: `F023 R7 C4: record the zoom's frame budget at 500 nodes over every level`

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F023 R7 C5: rewrite handoff for round 7`
  Then `git push origin feature/f023-semantic-zoom-l0-l3`. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f023-r7-*` copies,
   `.agent/authored/f023-r7-perf.txt`, `.agent/live_review.md`, `.agent/decisions.md`,
   `.agent/plan.md`, `apps/ui/src/components/graph/runDetailModel.test.ts`,
   `tests/ui_server/test_semantic_zoom_live.py`, and `.agent/handoff.md`. Report the list you
   measure with `git diff --name-only 7405cf35 HEAD` after C5. Do NOT touch any other file: this
   round changes no product code.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A performance
   transcript whose BUDGET line reads FAIL is committed as it is and reported, never re-run until
   it passes.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch
   deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that step's last action, and `git worktree list` is reported
   afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F023's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written, G4 and
G5 at C3, before C4 is committed.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f023-r7-*` copy byte for byte
 with its source (the block copy against `.remedy-wt/f023-r7/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, which its builder printed from the simulated tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 307292 | 2b8a804876db75d897aed463f7691087eb123f15457dba5fcca22bed4a75da88 |
 | .agent/decisions.md | 2071508 | f9986143422c81583e6b70f3e585556c6424427d85d49035abed26e303b125f2 |
 | .agent/plan.md | 1329 | a8bbd02bbbd5fedebca23d09f0fd6a6fde0892949cac887a199e333a9771c321 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `7405cf35` and at C2 (the reviewer
 read R-1008 alone at both); the ledger's last line at C2 begins `Gate: F023 R6 — `; and
 `git diff --name-only <C1d> <C2>`, which must name exactly the paths of the table above.

G3 THE TESTS' BYTES — the sha256 of each file below, read with `git show <C3>:<path>`, equals the
 reviewer's reading from the simulated tree:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C3 | apps/ui/src/components/graph/runDetailModel.test.ts | 8118 | ff83ce6abf82e98969a9435ad2dad523e334354c822a01f12e5570a700ce0952 |
 | C3 | tests/ui_server/test_semantic_zoom_live.py | 3203 | 35b82ea5ae3aba3578196f6e95662089cebfcd4d8c7351e65ce0de9156a69759 |
 Also `git diff --name-only <C2> <C3>`, which must name exactly those two paths; and
 `python3 -m ruff check tests/ui_server/test_semantic_zoom_live.py` at C3.

G4 THE TESTS — in the primary checkout at C3, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_server/test_semantic_zoom_live.py tests/ui_server/test_brain_demo_recording_live.py tests/ui_server/test_task_run_rounds.py tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path, serially, inside its sim tree
 carrying C1a to C3 with this block's copy, and read `1438 passed, 4 skipped` at real exit code 0, on its
 second run: during the first, a test in this selection installed the UI toolchain and a built
 `dist/` into the sim tree, so that reading's skips are the four standing quarantines of
 `test_graph_architecture.py` and `test_ux_quality.py` alone. The toolchain nodes
 must PASS in your run, not skip: the two in `tests/ui_contracts/test_ui_lint.py` (eslint at zero
 warnings), the typescript node in `tests/ui_server/test_dashboard_contract.py` (`tsc --noEmit`)
 and the vitest node in `tests/orchestration/test_test_runner.py`, which runs the UI's whole unit
 suite and so the new golden. Report every `SKIPPED` line the `-rs` summary prints. Then `python3 -m apps.cli.main integrity check --json`, which must read all six checks
 `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f023-r7-mut <C3>`, then
 `python3 -B .remedy-wt/f023-r7-payloads/mutations.py
 /home/decodeux/Repos/remedy/.remedy-wt/f023-r7-mut` and report its whole output. For each
 mutation the tool runs vitest over the WORKTREE's `runDetailModel.test.ts` from the primary
 `apps/ui` with a scratch config under `.remedy-wt/f023-r7-mutscratch/`, and pytest over the
 worktree's live test; it asserts each FROM occurs exactly once, restores the bytes, and runs an
 unmutated control first and last. The reviewer read, over the same tool against its sim tree
 (v = vitest failed, g = live test failed, each red at exit 1 wherever its count is not 0):
 control first: vitest 14 passed at exit 0, guard 1 passed at exit 0;
 m1 (the rounds route numbers its rounds from two) v0 g1;
 m2 (the rounds route drops the reviewer's verdict) v0 g1;
 m3 (the rounds route drops a round's duration) v0 g1;
 m4 (the rounds route names another run) v0 g1;
 m5 (the run detail counts rounds from before the task's last start) v1 g0;
 control last: vitest 14 passed at exit 0, guard 1 passed at exit 0;
 every `restored byte-identical` reading True, and the final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`.
 Then `git worktree remove --force .remedy-wt/f023-r7-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 THE TRANSCRIPT, TREE AND PUSH — after C4: `.agent/authored/f023-r7-perf.txt` read at C4 holds
 twelve lines beginning `{"level":`, three for each level 0 to 3, each with `"reachedLevel"` equal
 to its `"level"` and `"nodeCount":500`, four lines beginning `LEVEL L`, and the line
 `BUDGET 500 nodes, every zoom level: PASS`; the reviewer's own run of the same tool read every
 run at 481 frames and 60 frames a second with a worst 95th-percentile frame of 16.8 ms. Report
 those counts and the BUDGET line as you read them. After C5: `git status --porcelain`, which must
 be empty; `git log --oneline -n 9`, which must show C5, C4, C3, C2, C1d, C1c, C1b, C1a and
 `7405cf35` in that order; `git worktree list`, which must show the primary checkout and the
 worktrees constraint 6 names, and nothing else; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 The after-C5 readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F023, round 7, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 7, then the closure sequence's first half — the Built State, the checklist consolidation,
the self-use track and the one full suite. State the open-findings count, 1, and the
operator-questions count, 3.

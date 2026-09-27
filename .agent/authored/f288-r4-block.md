STEP F288 R4 — THE REPAIR OF ROUND 3: the four vitest files that read the demo recording or the widened row are brought to the new recording and row, and the vitest suite is green again

GOAL
Round 3 failed on one gate: `tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes`
reads 4 files and 8 tests red at `55820841`, all readers of the demo recording round 3 captured
again or of the two fields it added to every row. Book round 3's FAIL, record DECISION F288 D4,
and bring those four files' failing expectations to the new recording and row, derived again by
hand. No production file changes.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. Read DECISION F288 D4 and R-1075 in the records diff
first: D4 is the whole design of this round.

THE DIRECTORIES
  `.remedy-wt/f288-r4-payloads/` and `.remedy-wt/f288-r4/` are READ-ONLY; every other
  `.remedy-wt/f288-*` directory and `.remedy-wt/f288-review/` belongs to the reviewer.
  `.remedy-wt/f288-r4-worker/` is YOURS; create it if absent. All are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Never run npm or npx; the one Node binary you may run is
`/home/decodeux/Repos/remedy/apps/ui/node_modules/.bin/vitest`, from
`/home/decodeux/Repos/remedy/apps/ui`, as `vitest run <files>` while you work and as G5 orders.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f288-event-stream-completeness`, and `git log --oneline -1` must read `55820841`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f288-r4/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` and `git stash list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f288-r4-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 54 | 11102 | 8a9b25a2d01a0e10666c20fc38b6a238361c506117d0f9269dcc23eb9bb8eb6a |
| plan.md | 29 | 1093 | ce0f362c21212ac8b368107cfdbef283f29d741889cfc756e01663c090d975ab |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `55820841`. It appends round 3's gate entry to
`.agent/live_review.md`, DECISION F288 D4 to `.agent/decisions.md` and one dated line to
`.agent/prose_slips.md`.

THE REPAIR
The failing tests, as the reviewer read them at `55820841` with
`vitest run src/components/graph/brainLedger.test.ts src/components/graph/renderers/stateMotion.test.ts src/components/timeline/timelineView.test.ts src/components/timeline/timelineIndex.test.ts`:
  `brainLedger.test.ts` — "brainLedgerPage > reads rows and cursor from a payload shaped like
  _build_events_since_json's" and "THE GAP SCENARIO (brainDemoRecording) > holds the prefix at the
  state before the hole, then matches the whole model once it is filled";
  `timelineIndex.test.ts` — "the index equals the plain fold at every position > over the demo
  recording";
  `timelineView.test.ts` — "the bar over the demo recording > at the head: every phase done,
  Finalized current and full", "> scrubbed to seq 3: Review half filled, Finalized ahead, later
  glyphs not reached", "> a glyph exactly at the handle counts as reached", and "the track's
  geometry > puts the handle at the end of its event's slot in its segment";
  `renderers/stateMotion.test.ts` — "the demo recording's state changes > animates every state
  change the recorded job made, frame by frame, and ripples each completion".
For each, change ONLY the expected values (and the comments that walk them) so they state what
the test's own rules give for the new recording and the new row: derive each by hand from the
frames of `apps/ui/src/components/graph/brainDemoRecording.ts` at `55820841` and from the rules
the code under test documents, write the derivation into the comment beside it the way the file's
existing comments walk the old frames, and never paste a value the code printed. Where a test's
title names a seq or a position that no longer describes the same moment in the new recording
(for example "scrubbed to seq 3"), keep the moment the test is about — Review half filled,
Finalized ahead, later glyphs not reached — and move the seq and the title's number to where the
new recording holds that moment. A test's assertion shape, its tolerance and the number of its
assertions do not change. No other test and no production file changes, and every test green at
`55820841` stays green.

BUNDLE — the commits are C1, C2, C3 and C4, in this order.
C1 — `.agent/authored/f288-r4-block.md` := this block, `.agent/authored/f288-r4-records.diff` :=
  records.diff, `.agent/authored/f288-r4-plan.md` := plan.md, all by `shutil.copyfile`.
  Subject: `F288 R4 C1: copy round 4 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 83; STOP rather than commit if that is 500 or more.
C2 — `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F288 R4 C2: book round 3's FAIL, record D4 and the round 4 plan`
  Expected by `git show --numstat`: 27/0 decisions.md, 2/0 live_review.md, 9/16 plan.md, 1/0 prose_slips.md.
C3 — THE REPAIR: the four test files, and your probe tool (G5) saved as
  `.agent/authored/f288-r4-probes.py` (a lettered split if C3 would reach 500 insertions).
  Subject: `F288 R4 C3: bring the recording's and the row's four vitest readers to the new recording (R-1075, D4)`
C4 — THE HANDBACK: `.agent/handoff.md`, rewritten, per `docs/agents/handback_template.md`.
  Subject: `F288 R4 C4: rewrite handoff for round 4`
  Then `git push`. Do NOT create a pull request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading.
3. The round's whole tracked path set is: the `.agent/authored/f288-r4-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/prose_slips.md`, `.agent/plan.md`,
   `apps/ui/src/components/graph/brainLedger.test.ts`,
   `apps/ui/src/components/graph/renderers/stateMotion.test.ts`,
   `apps/ui/src/components/timeline/timelineIndex.test.ts`,
   `apps/ui/src/components/timeline/timelineView.test.ts`, and `.agent/handoff.md`. Report the list
   you measure with `git diff --name-only 55820841` at the branch tip after C4.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. If an expectation cannot be derived by hand from the
   frames and the documented rules, say so for that test and leave it red rather than printing
   the value from the code.
5. NOTHING IS MERGED, AND THE PRIMARY CHECKOUT NEVER LEAVES THE BRANCH: no `gh pr merge` or
   `gh pr create`, no `git checkout` or `git switch` in the primary checkout, no branch deletion,
   no force-push, no `git stash` of any kind. Read an older commit with `git show <sha>:<path>`.
6. Leave every existing worktree, branch and stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: F288's one run belongs to its closure.

DONE-WHEN — every gate executed, every reading reported with its real exit code. G1 to G5 run
before C4 is written.

G1 TRANSPORT — each payload's line count, byte count and sha256 against the table; then each
 `.agent/authored/f288-r4-*` payload copy compared byte for byte with its source (the block copy
 against `.remedy-wt/f288-r4/block.md`), read back with `git show <C1>:<path>`.

G2 THE BOOKING — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2236302 | 8168fa8db604d7a54439ec6c46653648b1d00ee8ed45f757244beff42180a2b5 |
 | .agent/live_review.md | 311964 | a3fb95d98d72893287da8a8bd25838fccf890c600ebea818c373a693866f5dcf |
 | .agent/prose_slips.md | 372141 | 1d186a8dd16460555b690b3ac9ba02b5abc0dbd03b78737d213a17793a917493 |
 | .agent/plan.md | 1093 | ce0f362c21212ac8b368107cfdbef283f29d741889cfc756e01663c090d975ab |
 Also the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT at C2 (the reviewer read `R-1075` alone).

G3 THE REPAIR — `git diff 55820841 <C3> -- apps/ui/src` reported whole, and for each of the eight
 tests one line naming it and the expectation it changed from and to.

G4 THE TESTS — in the primary checkout at C3, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_self_healing_cycles.py tests/orchestration/test_long_run_executor.py tests/ui_server/test_sse_stream.py tests/ui_server/test_budget_tick_envelope.py tests/ui_contracts tests/ui_server/test_brain_demo_recording_live.py tests/ui_server/test_semantic_zoom_live.py tests/ui_server/test_timeline_scrub_live.py tests/ui_server/test_live_state.py tests/orchestration/test_event_names.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/test_ble001_ratchet.py tests/test_imports.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran it at `55820841` and read `1 failed, 1824 passed, 5 skipped` at real exit code 1,
 the failure being `test_vitest_passes`; at C3 it must read `1825 passed, 5 skipped` at real exit
 code 0, the same five skips. Also `vitest run` over the whole suite from
 `/home/decodeux/Repos/remedy/apps/ui`, whose `Test Files` and `Tests` lines must read no failure
 (the reviewer read `4 failed | 70 passed | 1 skipped (75)` files and `8 failed | 1431 passed |
 5 skipped (1444)` tests at `55820841`). Then `python3 -m apps.cli.main integrity check --json`,
 all six checks `pass` at `fail_count` 0.

G5 THE PROBES — your tool `.agent/authored/f288-r4-probes.py` takes a worktree path, edits the
 named file INSIDE it (asserting its FROM text occurs exactly once), runs
 `/home/decodeux/Repos/remedy/apps/ui/node_modules/.bin/vitest run --config <scratch config>` from
 `/home/decodeux/Repos/remedy/apps/ui` with a PLAIN-OBJECT scratch config under your own directory
 (`root` the primary `apps/ui`, `cacheDir` under `.remedy-wt/`, `test: { environment: "node",
 include: [<the worktree's four repaired .test.ts files by absolute path>] }`), restores the bytes,
 and prints per probe its label, exit code, failed count and failing test names, with an unmutated
 control first and last and `restored byte-identical: True` per file. p2 and p3 must each turn at
 least one of the four files red; p1 is a probe whose colour you report as it reads, and if it
 stays green you say which of the four files could see it and why none does:
  p1 in the worktree's `brainDemoRecording.ts`, the frame at seq 2's outcome `changed` becomes
     `unchanged`;
  p2 in the worktree's `feedRow.ts`, `feedRowOf` stops setting `planTaskIds`;
  p3 in the worktree's `brainDemoRecording.ts`, the frame at seq 9 is removed.
 Run it in `git worktree add --detach .remedy-wt/f288-r4-mut <C3>` and report its whole output;
 then remove the worktree, `git worktree prune`, and report `git worktree list | wc -l`; and
 `git status --porcelain` must be empty, a stray `.vite/` included.

G6 TREE AND PUSH — after C4: `git status --porcelain` empty; `git log --oneline 55820841..HEAD`;
 `git worktree list | wc -l` and `git stash list | wc -l`, equal to your step 4 readings; the
 push's real outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`,
 which must be EMPTY. These readings go in your reply, since C4 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the insertion count you MEASURED beside the one this block
expected (none is expected for C3), every gate's real output and exit code, the authored-text
proofs, the item-status table AGENTS.md requires (one row per commit and per gate), the deviations,
and the next expected action. Your Session section reads SESSION 1 of feature F288, round 4, and
says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round
4 with R-1075's resolution, then T003 — the prompt node kind, its look, and its mouse and keyboard
reach. State the open-findings count, 1 (R-1075, landed and awaiting the reviewer's `Done:`), and
the operator-questions count, 0.
